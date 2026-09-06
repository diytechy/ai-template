"""Typed, read-only display facts shared by status and the HTML dashboard.

The status splice and dashboard both display the committed stage record and
spine totals.  Keep that small common read at one boundary; HTML-only layout,
source inventory, and work-item rendering remain with their consumers.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from kitlib import stage as _kitstage
from traj_parse import spine_stats


@dataclass(frozen=True)
class DisplaySnapshot:
    """Recorded facts that both display surfaces project without recomputing."""

    stage: Mapping[str, object]
    spine: Mapping[str, int]


def load_stage_record(root: Path) -> Mapping[str, object]:
    """Read the committed stage record alone; malformed or absent is empty."""
    path = root / _kitstage.STAGE_FILE
    if not path.exists():
        return {}
    try:
        return _kitstage.parse(path.read_text(encoding="utf-8", errors="replace")) or {}
    except ValueError:
        return {}


def load_display_snapshot(root: Path) -> DisplaySnapshot:
    """Read the committed display facts once; display never self-heals stage."""
    return DisplaySnapshot(stage=load_stage_record(root), spine=spine_stats(root))
