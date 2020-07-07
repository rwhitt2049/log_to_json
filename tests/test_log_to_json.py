#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

import pytest

from log_to_json import JsonFormatter

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def test_message_is_mapping(caplog):
    formatter = JsonFormatter()
    message = {"int": 1, "string": "hey"}
    expected = json.dumps(message)
    logger.critical(message)
    for record in caplog.records:
        actual = formatter.format(record)

        assert actual == expected


def test_json_message(caplog):
    formatter = JsonFormatter()
    message = {"int": 1, "string": "hey"}
    expected = json.dumps(message)
    logger.critical("test", extra={"json_message": message})
    for record in caplog.records:
        actual = formatter.format(record)

        assert actual == expected


@pytest.mark.parametrize(
    "key, expected",
    argvalues=(
        ("asctime", None),
        ("created", None),
        ("exc_info", None),
        ("filename","test_log_to_json.py"),
        ("funcName", "test_default_record_attributes"),
        ("levelname", "INFO"),
        ("levelno", 20),
        ("lineno", None),
        ("message", "test"),
        ("module", None),
        ("msecs", None),
        ("msg", "test"),
        ("name", "root"),
        ("process", None),
        ("relativeCreated", None),
        ("stack_info", None),
        ("thread", None),
        ("threadName", None),
    )
)
def test_default_record_attributes(caplog, key, expected):
    keys = (key,)
    formatter = JsonFormatter(keys=keys)
    logger.info("test")
    record = next(iter(caplog.records))
    formatted_msg = formatter.format(record)
    message = json.loads(formatted_msg)
    assert key in message
    if expected is not None:
        assert message[key] == expected


def test_formatter(caplog):
    message_formatter = lambda val: 2 * val
    formatter = JsonFormatter(
        keys=("message",),
        formatters={"message": message_formatter}
    )
    logger.info(2)
    expected = json.dumps({"message": "22"})  # seems numbers get cast to strings, is this caplog, or logging?
    record = next(iter(caplog.records))
    actual = formatter.format(record)
    assert actual == expected


def test_finalizer(caplog):
    def finalizer(message):
        message["new_message"] = message["message"]
        del message["message"]
        return message
    formatter = JsonFormatter(
        keys=("message",),
        finalizer=finalizer,
    )
    logger.info("test")
    expected = json.dumps(
        {"new_message": "test"})
    record = next(iter(caplog.records))
    actual = formatter.format(record)
    assert actual == expected


def test_prefix(caplog):
    prefix = "TEST -> "
    formatter = JsonFormatter(
        keys=("message",),
        prefix=prefix
    )
    logger.info("test")
    expected = prefix + json.dumps({"message": "test"})
    record = next(iter(caplog.records))
    actual = formatter.format(record)
    assert  actual == expected


if __name__ == '__main__':
    pytest.main()
