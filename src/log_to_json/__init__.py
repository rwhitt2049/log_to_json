# -*- coding: utf-8 -*-

"""Top-level package for Log to JSON."""

import pathlib

__author__ = """Ry Whittington"""
__email__ = "rwhitt2049@gmail.com"


with pathlib.Path(__file__).parent.joinpath("..", "..", "VERSION").open() as version_file:
    __version__ = version_file.read().strip()
