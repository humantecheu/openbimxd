# SPDX-License-Identifier: MIT
# Copyright (c) 2024 the HumanTech project

"""Python library for IFC BIM interaction and scan-to-BIM workflows."""

from contextlib import suppress
from importlib.metadata import PackageNotFoundError, version

with suppress(PackageNotFoundError):
    __version__ = version("openbimxd")
