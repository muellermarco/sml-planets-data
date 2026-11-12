#!/usr/bin/env python3
"""Warehouse dry-run gate for planets_data: every derived dataset runs, the
declared grain is unique, and every live count quoted in a published description
is pinned to the data.  See birdsml.dryrun for the harness and spec.PINNED for
the constants."""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "utilities"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from birdsml import dryrun                              # noqa: E402
import spec                                             # noqa: E402

if __name__ == "__main__":
    sys.exit(dryrun.run(spec))
