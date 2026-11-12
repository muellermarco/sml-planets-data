#!/usr/bin/env python3
"""Deterministic generator for the planets_data AtScale SML model.

Spec in, YAML out.  Changes are made by editing the spec modules and re-running,
never by hand-editing emitted YAML - anything hand-edited is silently reverted on
the next run.  The emitter and all nineteen build gates live in
``utilities/birdsml``; this file only wires the spec to them.

Usage:
    python3 dry_run.py && python3 generate.py
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "utilities"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import birdsml                                          # noqa: E402
import spec                                             # noqa: E402

if __name__ == "__main__":
    sys.exit(birdsml.build(spec, pathlib.Path(__file__).resolve().parent.parent))
