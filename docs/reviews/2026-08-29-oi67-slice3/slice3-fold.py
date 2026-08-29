"""Fold the four worker reports into docs/requirements/interfaces.toml:
channel / far side / data confirmed, the legacy `contract` cell deleted, the
moot notes and rationale cells deleted. Text-level, block by block, so the
header and every other cell survive byte-for-byte."""
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(r"c:\Projects\ai-template")
S = Path(__file__).parent
REG = ROOT / "docs/requirements/interfaces.toml"
CHANNELS = {"cli", "exit-code", "stdout", "file", "call", "env", "git", "bytes"}

reports = {}
for b in "ABCD":
    p = S / f"slice3-report-{b}.json"
    if not p.exists():
        print("missing report", p.name)
        continue
    for r in json.loads(p.read_text(encoding="utf-8")):
        assert r["id"] not in reports, ("duplicate", r["id"])
        reports[r["id"]] = r
print("reports for", len(reports), "rows")

KEY_RE = re.compile(r"^([a-z_]+)\s*=\s*(.*)$")


def cells_of(lines):
    cells, i = {}, 1
    while i < len(lines):
        km = KEY_RE.match(lines[i])
        if km:
            start, val = i, km.group(2)
            if val.startswith('"""') and val.count('"""') == 1:
                i += 1
                while '"""' not in lines[i]:
                    i += 1
            cells[km.group(1)] = (start, i)
        i += 1
    return cells


def toml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


text = REG.read_text(encoding="utf-8")
blocks = re.split(r"(?m)^(?=\[interface\.)", text)
out, unfolded, problems = [], [], []
for blk in blocks:
    m = re.match(r"\[interface\.(IF-\d+)\]", blk)
    if not m:
        out.append(blk)
        continue
    rid = m.group(1)
    rep = reports.get(rid)
    if rep is None:
        unfolded.append(rid)
        out.append(blk)
        continue
    if not rep.get("body_written") and not (rep.get("far") and str(rep.get("far"))):
        problems.append((rid, "no body and no far side"))
    lines = blk.splitlines(keepends=True)
    cells = cells_of(lines)
    drop = set()
    for key in ("contract",):
        if key in cells and rep.get("body_written"):
            s, e = cells[key]
            drop.update(range(s, e + 1))
    if rep.get("notes_moot") and "notes" in cells:
        s, e = cells["notes"]
        drop.update(range(s, e + 1))
    if rep.get("rationale_moot") and "rationale" in cells:
        s, e = cells["rationale"]
        drop.update(range(s, e + 1))
    for key in ("requestors", "consumers", "data", "channel"):
        if key in cells:
            s, e = cells[key]
            drop.update(range(s, e + 1))
    channel = rep["channel"].strip()
    assert channel in CHANNELS, (rid, channel)
    far_key = rep["far_key"].strip()
    assert far_key in ("requestors", "consumers"), (rid, far_key)
    far = [str(x).strip() for x in rep["far"] if str(x).strip()]
    assert far, (rid, "empty far side")
    data = (rep.get("data") or "").strip()
    assert len(data) <= 160, (rid, len(data))
    new = []
    inserted = False
    for idx, line in enumerate(lines):
        if idx in drop:
            continue
        new.append(line)
        if idx == cells["owner"][0] and not inserted:
            new.append("{} = [{}]\n".format(far_key, ", ".join(toml_str(x) for x in far)))
            new.append('channel = "{}"\n'.format(channel))
            if data:
                new.append("data = {}\n".format(toml_str(data)))
            inserted = True
    assert inserted, (rid, "no owner line")
    out.append("".join(new))

new_text = "".join(out)
parsed = tomllib.loads(new_text)["interface"]
legacy = [k for k, v in parsed.items() if v.get("contract")]
print("unfolded rows:", unfolded)
print("problems:", problems)
print("legacy contract cells remaining:", len(legacy), legacy[:10])
if "--write" in sys.argv:
    REG.write_bytes(new_text.encode("utf-8").replace(b"\r\n", b"\n"))
    print("written")
else:
    print("dry run — pass --write to apply")
