#! /usr/bin/env python3
"""Shared constants for the TableIO JSON config read/write tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys

from tableio import FileAccess, access_capabilities

FILE_ACCESS = FileAccess.CREATE
CAPABILITIES = access_capabilities(FILE_ACCESS, error_file=sys.stderr)
