# -*- coding: utf-8 -*-
import json
import logging
import typing
from collections import abc


def get_exc_info(record: logging.LogRecord, formatter: logging.Formatter) -> str:
    if record.exc_text:
        val = record.exc_text
    elif record.exc_info:
        val = formatter.formatException(record.exc_info)
        record.exc_text = val
    else:
        val = None

    return val


Finalizer = typing.Optional[typing.Callable[[typing.MutableMapping], typing.Mapping]]
Serializer = typing.Optional[typing.Callable[[typing.Mapping], str]]


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        keys: typing.Optional[typing.Iterable[str]] = None,
        formatters: typing.Mapping[str, typing.Callable] = None,
        finalizer: Finalizer = None,
        serializer: Serializer = None,
        datefmt: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
    ):
        special_keys = {
            "stack_info": lambda record: self.formatStack(record.stack_info),  # does this get the stack info and format, or just format it?
            "exc_info": lambda record: get_exc_info(record, self),
            "asctime": lambda record: self.formatTime(record, self.datefmt)  # does this format then get the time, or just format it?
        }  # need to determine what to do if a user tries to format these as well - chain them together? user(default(key))?

        keys = tuple(keys) if keys is not None else ()

        self.keys = {
            key: special_keys.get(key, lambda record, k=key: getattr(record, k))
            for key in keys
        }

        self.fmt = dict(formatters) if formatters is not None else {}
        self.serializer = serializer if serializer is not None else json.dumps
        self.prefix = prefix if prefix is not None else ""

        no_op = lambda x: x
        self.finalizer = finalizer if finalizer is not None else no_op

        logging.Formatter.__init__(self, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        try:
            message_dict = dict(
                getattr(record, "json_message", {})
            )
        except ValueError as e:  # trying to cast a non-mapping raises ValueError
            raise ValueError("Json message needs to be a mapping") from e

        if isinstance(record.msg, abc.Mapping):
            message_dict.update(record.msg)
            record.message = None
        else:
            record.message = record.getMessage()

        log_message = {
            **message_dict,
            **{k: getter(record) for k, getter in self.keys.items()}
        }

        for key, formatter in self.fmt.items():
            log_message[key] = formatter(log_message[key])

        msg = self.finalizer(log_message)

        return f"{self.prefix}{self.serializer(msg)}"
