#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
from codecs import open

from setuptools import setup, find_packages

about = {}
about_fid = (
    pathlib.Path(__file__)
    .parent.absolute()
    .joinpath("src", "log_to_json", "__about__.py")
)
with about_fid.open(mode="r") as f:
    exec(f.read(), about)


def read_files(path):
    with open(path, encoding="utf-8") as fid:
        return fid.read()


requirements_doc = read_files("requirements_doc.txt").splitlines()
requirements_dev = read_files("requirements_dev.txt").splitlines()
requirements = read_files("requirements.txt").splitlines()
readme = read_files("README.md")

setup(
    author="Ry Whittington",
    author_email="rwhitt2049@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Yet another package to convert log messages to JSON.",
    extras_require={"dev": requirements_dev, "doc": requirements_doc},
    include_package_data=True,
    install_requires=requirements,
    keywords="log_to_json",
    license="MIT license",
    long_description=readme,
    name="log_to_json",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    test_suite="tests",
    tests_require=requirements_dev,
    url="https://github.com/rwhitt2049/log_to_json",
    version=about["__version__"],
    zip_safe=False,
)
