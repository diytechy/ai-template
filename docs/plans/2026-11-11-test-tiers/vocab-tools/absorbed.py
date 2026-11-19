"""Name every accepted cell a copy of the acceptance record would absorb (D13).

  python absorbed.py REGISTRY_REL [...]      e.g. docs/requirements/system-requirements.toml

Compares the live TOML registry with its copy under docs/archive/last_approved/
row by row: for each row the copy records as `Approved`, every cell whose value
differs, `status` left out. A row present only in the live file is listed as
new (a snapshot copies it, whatever its status).
"""

import sys
import tomllib
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
RECORD = ROOT / "docs/archive/last_approved"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rows(path):
    data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    out = {}
    for tier in data.values():
        if isinstance(tier, dict):
            for rid, row in tier.items():
                if isinstance(row, dict):
                    out[rid] = row
    return out


for rel in sys.argv[1:]:
    live, copy = rows(ROOT / rel), rows(RECORD / rel)
    for rid in sorted(set(live) - set(copy)):
        print("{}: {} new ({})".format(rel, rid, live[rid].get("status")))
    for rid in sorted(set(copy) & set(live)):
        if copy[rid].get("status") != "Approved":
            continue
        cells = sorted(
            k for k in set(copy[rid]) | set(live[rid])
            if k != "status" and copy[rid].get(k) != live[rid].get(k)
        )
        if cells:
            print("{}: {} accepted, absorbs {}".format(rel, rid, ", ".join(cells)))
    for rid in sorted(set(copy) - set(live)):
        print("{}: {} only in the copy".format(rel, rid))
