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


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        keys: typing.Optional[typing.Iterable[str]] = None,  # if none, then record.msg has to be mapping already, or json_message was passed
        fmt: typing.Mapping[str, typing.Callable] = None,
        finalizer: typing.Optional[typing.Callable[[typing.Mapping], typing.Mapping]] = None,
        serializer: typing.Optional[typing.Callable] = None,
        datefmt: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
    ):
        default_key_formatters = {
            "stack_info": lambda record: self.formatStack(record.stack_info),  # does this get the stack info and format, or just format it?
            "exc_info": lambda record: get_exc_info(record, self),
            "asctime": lambda record: self.formatTime(record, self.datefmt)  # does this format then get the time, or just format it?
        }  # need to determine what to do if a user tries to format these as well - chain them together? user(default(key))?

        keys = tuple(keys) if keys is not None else ()

        key_getters = {k: default_key_formatters.get(k, lambda record, key=k: getattr(record, key)) for k in keys}
        fmt = dict(fmt) if fmt is not None else {}

        formats = {k: lambda record, fmter=v: for k, v in fmt.items()}

        for k, default_formatter in default_key_formatters.items():
            if k in fmt:
                fmt[k] = lambda record, user_fmt=fmt[k], default_fmt=default_formatter: user_fmt(default_fmt(record))  # maybe use toolz.compose here?

        fmt = {**fmt_from_keys, **fmt}  # does this work on 3.6? # ultimately, should be key: callable where callable is getter, then formatter if provided


        self.fmt = {key: fmt.get(key, lambda rec, k=key: getattr(rec, k)) for key in keys}
        self.serializer = serializer if serializer is not None else json.dumps
        self.prefix=prefix

        no_op = lambda x: x
        self.finalizer = finalizer if finalizer is not None else no_op

        logging.Formatter.__init__(self, datefmt=datefmt)


    def format(self, record: logging.LogRecord) -> str:
        try:
            message_dict = dict(
                getattr(record, "json_message", {})
            )
        except ValueError as e:
            raise ValueError("Json message needs to be a mapping") from e

        if isinstance(record.msg, abc.Mapping):
            message_dict.update(record.msg)
            record.message = None
        else:
            record.message = record.getMessage()

        log_message = {**message_dict, **{k: v(record) for k, v in self.fmt.items()}}

        msg = self.finalizer(log_message)

        return f"{self.prefix}{self.serializer(msg)}"
