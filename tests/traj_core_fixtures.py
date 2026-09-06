"""Core-only fixtures for trajectory parsing and text-status tests."""

import csv
import sys
from pathlib import Path

from conftest import SCRIPTS, load_script

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kitlib import ladder as _ladder  # noqa: E402
from kitlib import stage as _kitstage  # noqa: E402

WI_HEADER = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"
SN_MD = """# Stakeholder Needs (SN-###)

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Do the thing well. | Users need it. | M | works end to end. |
"""
SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Core add,SN-001,"Shall add.",R,"add works",,M,Test,Approved
SR-002,Core sub,SN-001,"Shall sub.",R,"sub works",,M,Test,Drafted
"""
LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Adder,src/m,add,"a+b",(see TC),Approved
LLR-002,SR-001,Adder edge,src/m,add,"overflow guard",(see TC),Approved
LLR-003,SR-002,Subber,src/m,sub,"a-b",(see TC),Approved
"""
TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,call add,Smoke,"a=1",ok,Yes,Approved
TC-002,LLR-001,Unit,call add,Smoke,"a=2",ok,Yes,Approved
TC-003,LLR-002,Unit,call add,Full,"a=3",ok,Yes,Approved
TC-004,SR-002;LLR-003,Unit,call sub,Full,"a=4",ok,No,Drafted
"""
GOOD_WIS = (
    "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
    "WI-002,Harness,scripts,SR-001,WI-001,active,harness green\n"
    "WI-003,Subtraction,scripts,SR-002,WI-001;~WI-002,queued,the subber\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped\n"
)


def write_wis(root, wis_body=GOOD_WIS, header=WI_HEADER):
    wc = load_script("wi_convert")
    cols = next(csv.reader([header.strip("\n")]))
    work = root / "docs" / "work"
    work.mkdir(parents=True, exist_ok=True)
    for order, cells in enumerate(csv.reader(wis_body.splitlines()), 1):
        if not cells:
            continue
        row = dict.fromkeys(wc.COLUMNS, "")
        row.update({c: (v or "") for c, v in zip(cols, cells) if c in row})
        status = row["Status"] or "queued"
        if status == "active":
            row["Status"] = "queued"
        wid = row["WI-ID"]
        for old in list(work.glob("*/{}-*.md".format(wid))) + list(
            work.glob("active/*/{}-*.md".format(wid))
        ):
            old.unlink()
        relpath = wc.write_spec_file(work, row, order=order)
        if status == "active":
            claim = work / "active" / wid.lower() / Path(relpath).name
            claim.parent.mkdir(parents=True, exist_ok=True)
            (work / relpath).replace(claim)


def make_repo(root, wis_body=GOOD_WIS, readme=True, header=WI_HEADER):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(TCS, encoding="utf-8")
    write_wis(root, wis_body, header)
    if readme:
        (root / "README.md").write_text(
            '# demoproj\n\n<a id="vision"></a>\n'
            "**PROJECT-VISION:** Stay correct over time.\n\n## What\n",
            encoding="utf-8",
        )
    return root


def write_stage(root, stage="DevStg-Tests", **over):
    record = {
        "stage": stage,
        "stage-ord": _ladder.stage_ord(stage),
        "stage-of": _ladder.STAGE_OF,
        "floored": False,
        "settled-stage": stage,
        "live-stage": stage,
        "phase": None,
        "per-phase": {"1": stage},
        "per-phase-live": {"1": stage},
        "drafted": 0,
        "fingerprint": _kitstage.fingerprint(root),
    }
    record.update(over)
    path = root / _kitstage.STAGE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        _kitstage.render(record, "fixture0", "2026-08-21"), encoding="utf-8"
    )
    return root


FRAME = """
[entity.EXT-001]
name = "Downstream adopter"
class = "operational"
description = "The team that adopts the package."
status = "Drafted"

[entity.EXT-002]
name = "Vendored upstream"
class = "enabling"
description = "A source this project vendors from."
status = "Drafted"

[boundary.B-01]
entity = "EXT-001"
direction = "out"
carries = "the delivered package"
status = "Drafted"

[boundary.B-02]
entity = "EXT-001"
direction = "in"
carries = "adopter feedback"
status = "Drafted"

[relationship.REL-001]
from = "EXT-002"
to = "EXT-001"
kind = "hands-off"
flow = "a flow this system is not a party to"
status = "Drafted"
"""


def write_frame(root, text=FRAME):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "external.toml").write_text(text, encoding="utf-8")
    return root
