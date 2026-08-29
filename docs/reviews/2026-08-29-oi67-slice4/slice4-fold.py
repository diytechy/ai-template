"""Fold the three slice-4 worker reports into docs/requirements/interfaces.toml:
new rows minted beside the row they split from, the two duplicate rows
collapsed, far sides and channels re-measured, tie-backs and components set.
Text-level, block by block, so the header and every untouched cell survive
byte-for-byte. Dry-runs without --write."""

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
S = Path(__file__).parent
REG = ROOT / "docs/requirements/interfaces.toml"
CHANNELS = {"cli", "exit-code", "stdout", "file", "call", "env", "git", "bytes"}
KEY_RE = re.compile(r"^([a-z_]+)\s*=\s*(.*)$")

worklist = {
    r["id"]: r
    for r in json.loads((S / "slice4-worklist.json").read_text(encoding="utf-8"))["rows"]
}
reports = {}
for b in "ABC":
    p = S / f"slice4-report-{b}.json"
    if not p.exists():
        print("missing report", p.name)
        continue
    for r in json.loads(p.read_text(encoding="utf-8")):
        assert r["id"] not in reports, ("duplicate", r["id"])
        assert r["id"] in worklist, ("unknown id", r["id"])
        reports[r["id"]] = r
missing = sorted(set(worklist) - set(reports))
print("reports for", len(reports), "rows; unreported:", missing)


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


def toml_list(items):
    return "[" + ", ".join(toml_str(x) for x in items) + "]"


def far_of(rep, rid):
    far_key = rep["far_key"].strip()
    assert far_key in ("requestors", "consumers"), (rid, far_key)
    far = [str(x).strip() for x in rep["far"] if str(x).strip()]
    assert far, (rid, "empty far side")
    assert not isinstance(rep["far"], str), (rid, "far is a string")
    return far_key, far


def check_common(rep, rid):
    assert rep["channel"].strip() in CHANNELS, (rid, rep["channel"])
    data = (rep.get("data") or "").strip()
    assert len(data) <= 160, (rid, len(data))
    return data


def new_block(rid, rep):
    far_key, far = far_of(rep, rid)
    data = check_common(rep, rid)
    owner = rep["owner"].strip()
    assert owner and not owner.startswith("MEASURE"), (rid, owner)
    lines = [f"[interface.{rid}]\n"]
    lines.append(f"owner = {toml_str(owner)}\n")
    lines.append(f"{far_key} = {toml_list(far)}\n")
    lines.append(f'channel = "{rep["channel"].strip()}"\n')
    if data:
        lines.append(f"data = {toml_str(data)}\n")
    lines.append('version = "v1"\n')
    lines.append('status = "Drafted"\n')
    if (rep.get("component") or "").strip():
        lines.append(f"component = {toml_str(rep['component'].strip())}\n")
    if (rep.get("tie_from") or "").strip():
        lines.append(f"interface_from_external = {toml_str(rep['tie_from'].strip())}\n")
    if (rep.get("tie_to") or "").strip():
        lines.append(f"interface_to_external = {toml_str(rep['tie_to'].strip())}\n")
    if (rep.get("notes") or "").strip():
        lines.append(f"notes = {toml_str(rep['notes'].strip())}\n")
    lines.append("\n")
    return "".join(lines)


def edit_block(blk, rid, rep):
    lines = blk.splitlines(keepends=True)
    cells = cells_of(lines)
    far_key, far = far_of(rep, rid)
    data = check_common(rep, rid)
    drop = set()
    for key in (
        "requestors",
        "consumers",
        "channel",
        "data",
        "interface_from_external",
        "interface_to_external",
    ):
        if key in cells:
            s, e = cells[key]
            drop.update(range(s, e + 1))
    if rep.get("notes_moot") and "notes" in cells:
        s, e = cells["notes"]
        drop.update(range(s, e + 1))
    if rep.get("rationale_moot") and "rationale" in cells:
        s, e = cells["rationale"]
        drop.update(range(s, e + 1))
    set_component = (rep.get("component") or "").strip() and "component" not in cells
    tie_from = (rep.get("tie_from") or "").strip()
    tie_to = (rep.get("tie_to") or "").strip()
    new = []
    for idx, line in enumerate(lines):
        if idx in drop:
            continue
        # A new owner spelling (an edit row whose owner the worker corrected).
        if idx == cells["owner"][0] and rep.get("owner", "").strip():
            line = f"owner = {toml_str(rep['owner'].strip())}\n"
        new.append(line)
        if idx == cells["owner"][0]:
            new.append(f"{far_key} = {toml_list(far)}\n")
            new.append(f'channel = "{rep["channel"].strip()}"\n')
            if data:
                new.append(f"data = {toml_str(data)}\n")
        if idx == cells["status"][0]:
            if set_component:
                new.append(f"component = {toml_str(rep['component'].strip())}\n")
            if tie_from:
                new.append(f"interface_from_external = {toml_str(tie_from)}\n")
            if tie_to:
                new.append(f"interface_to_external = {toml_str(tie_to)}\n")
    return "".join(new)


text = REG.read_text(encoding="utf-8")
blocks = re.split(r"(?m)^(?=\[interface\.)", text)
out = []
seen = set()
pending_new = {}  # parent id -> [new blocks]
tail_new = []
for rid, rep in reports.items():
    if rep["action"] != "new":
        continue
    parent = worklist[rid].get("split_from")
    (pending_new.setdefault(parent, []) if parent else tail_new).append(
        (rid, new_block(rid, rep))
    )

for blk in blocks:
    m = re.match(r"\[interface\.(IF-\d+)\]", blk)
    if not m:
        out.append(blk)
        continue
    rid = m.group(1)
    seen.add(rid)
    rep = reports.get(rid)
    if rep is None:
        out.append(blk)
    elif rep["action"] == "delete":
        print("deleted", rid, "->", rep.get("into"))
        continue
    elif rep["action"] == "edit":
        out.append(edit_block(blk, rid, rep))
    else:
        raise SystemExit(f"{rid}: a `new` row already exists in the registry")
    for nid, nb in pending_new.pop(rid, []):
        out.append(nb)
        print("minted", nid, "after", rid)
for parent, items in pending_new.items():
    raise SystemExit(f"parent {parent} not found for {[i for i, _ in items]}")
for nid, nb in tail_new:
    out.append(nb)
    print("minted", nid, "at the end")

new_text = "".join(out)
if not new_text.endswith("\n"):
    new_text += "\n"
parsed = tomllib.loads(new_text)["interface"]
print("rows after fold:", len(parsed))
legacy = [k for k, v in parsed.items() if v.get("contract")]
print("legacy contract cells remaining:", legacy)
both = [k for k, v in parsed.items() if ("requestors" in v) == ("consumers" in v)]
print("rows with both/neither far side:", both)
for rid, rep in reports.items():
    if rep["action"] != "delete":
        assert rid in parsed, ("missing after fold", rid)
        assert parsed[rid]["channel"] == rep["channel"].strip(), rid
for rid in [r for r, rep in reports.items() if rep["action"] == "delete"]:
    assert rid not in parsed, ("still present", rid)
if "--write" in sys.argv:
    REG.write_bytes(new_text.encode("utf-8").replace(b"\r\n", b"\n"))
    print("written")
else:
    print("dry run — pass --write to apply")
