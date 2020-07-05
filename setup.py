#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
import glob


def read_files(path):
    with open(path, encoding="utf-8") as fid:
        return fid.read()


requirements_doc = read_files("requirements_doc.txt").splitlines()
requirements_dev = read_files("requirements_dev.txt").splitlines()
requirements = read_files("requirements.txt").splitlines()
readme = read_files("README.md")
version = read_files("VERSION").strip()

setup(
    author="Ry Whittington",
    author_email="rwhitt2049@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Yet another package to convert log messages to JSON.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="log_to_json",
    name="log_to_json",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    test_suite="tests",
    tests_require=requirements_dev,
    url="https://github.com/rwhitt2049/log_to_json",
    version=version,
    zip_safe=False,
)
