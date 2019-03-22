#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3, 7, 0):
    print("Python 3.7+ is required")
    exit(1)
import io  # noqa E402
import os  # noqa E402
from setuptools import find_packages, setup  # noqa E402
from pathlib import Path  # noqa E402
from typing import List  # noqa E402
import ast  # noqa E402
import re  # noqa E402

CURDIR = Path(__file__).parent

REQUIRED: List[str] = ['putio.py', 'colorama']

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version() -> str:
    main_file = CURDIR / "gcea" / "__init__.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="gcea",
    version=get_version(),
    author="Dave Williams",
    author_email="dave@dave.io",
    description="Convert files stored on put.io to mp4",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/daveio/gcea",
    license="License :: OSI Approved :: MIT License",
    packages=find_packages(),
    include_package_data=True,
    keywords=["putio", "put.io", "convert", "video", "mp4"],
    scripts=[],
    entry_points={"console_scripts": ["gcea = gcea.main:cli"]},
    extras_require={},
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=REQUIRED,
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
