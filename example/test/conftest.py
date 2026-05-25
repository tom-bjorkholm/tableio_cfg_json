#! /usr/bin/env python3
"""Pytest configuration for the teaching examples."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path


EXAMPLE_SRC = Path(__file__).resolve().parents[1] / 'src'
sys.path.insert(0, str(EXAMPLE_SRC))
