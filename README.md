# Logging to JSON

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Yet another log to JSON library for Python.
I needed a library that integrated well with applications that mixed logging using built-in logging outputs and JSON output.
I was also unable to find a library that worked with `logging.QueueHandler`
Thus this library was born.

# Install

`pip install log_to_json`

or

`conda install log_to_json -c conda-forge`

# Example

### Basic Usage

```python
from log_to_json import JsonFormatter
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
json_formatter = JsonFormatter(keys=("name",))
handler.setFormatter(json_formatter)

logger.critical({"app-name": "my-app", "app_version": "1.0"})

# produces the log
{"app-name": "my-app", "app_version": "1.0", "name": "root"}
```

### Slightly more advanced Usage

```python
from log_to_json import JsonFormatter
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()

def finalizer(message_dict):
    """rename name to logger_name"""
    message_dict["logger_name"] = message_dict.pop("name")
    return message_dict

json_formatter = JsonFormatter(
    keys=("message", "name", "user"),
    formatters={"user": str.upper},
    finalizer=finalizer
)
handler.setFormatter(json_formatter)

logger.critical("critical failure", extra={"user": "guest"})

# produces the message

{"message": "critical failure", "user": "GUEST", "logger_name": "root"}
```

# Notable Features

## Individual Key Formatters

## Finalizer

## Per Message Prefix

## Integrates with non-JSON Logging

## Pluggable Serializer
