"""The three-level requirement tree the WI-1027 cases walk (a helper, not a
test module).

Two requirements in two phases: SR-001 holds a top-level design row LLR-001,
its child LLR-002 and its grandchild LLR-003; SR-002 holds the top-level row
LLR-009. Each design row has one test case, the parent's naming the parent
itself (its integration case). Rows are spelled as the registry carrier hands
them back (column names), and `write` lays them into a repository as the TOML
registries, so a reader that loads from disk sees the same tree.
"""

import copy
from pathlib import Path

SR1, SR2 = "SR-001", "SR-002"
TOP, CHILD, GRAND, OTHER = "LLR-001", "LLR-002", "LLR-003", "LLR-009"
TREE = (TOP, CHILD, GRAND)

_SRS = [
    {
        "SR-ID": SR1,
        "Title": "Export records",
        "SN-Refs": "SN-001",
        "Requirement": "The kit shall export the records a reviewer selects.",
        "Rationale": "Reviewers read records outside the tool.",
        "AcceptanceCriteria": "A selected record appears in the export.",
        "Priority": "M",
        "VerificationMethod": "Test",
        "Status": "Accepted",
        "Phase": "1",
    },
    {
        "SR-ID": SR2,
        "Title": "Import records",
        "SN-Refs": "SN-001",
        "Requirement": "The kit shall import the records a reviewer supplies.",
        "Rationale": "Reviewers bring records from elsewhere.",
        "AcceptanceCriteria": "A supplied record appears in the registry.",
        "Priority": "M",
        "VerificationMethod": "Test",
        "Status": "Accepted",
        "Phase": "2",
    },
]

_LLRS = [
    {
        "LLR-ID": TOP,
        "SR-Refs": SR1,
        "Title": "Export pipeline",
        "Detail": "Selects the rows, then hands them to the writer.",
        "Status": "Accepted",
        "Phase": "1",
    },
    {
        "LLR-ID": CHILD,
        "Parent": TOP,
        "Title": "Row selection",
        "Detail": "Keeps the rows whose flag is set, in their file order.",
        "Status": "Accepted",
        "Phase": "1",
    },
    {
        "LLR-ID": GRAND,
        "Parent": CHILD,
        "Title": "Flag parsing",
        "Detail": "Reads a flag cell as set when it holds yes, in any case.",
        "Status": "Accepted",
        "Phase": "1",
    },
    {
        "LLR-ID": OTHER,
        "SR-Refs": SR2,
        "Title": "Import reader",
        "Detail": "Parses each supplied line into one row.",
        "Status": "Accepted",
        "Phase": "2",
    },
]

_TCS = [
    {"TC-ID": "TC-001", "Verifies": SR1 + ";" + TOP, "Phase": "1"},
    {"TC-ID": "TC-002", "Verifies": CHILD, "Phase": "1"},
    {"TC-ID": "TC-003", "Verifies": GRAND, "Phase": "1"},
    {"TC-ID": "TC-009", "Verifies": SR2 + ";" + OTHER, "Phase": "2"},
]
for _tc in _TCS:
    _tc.update(
        {
            "Level": "Unit",
            "Method": "Run the case.",
            "Tier": "Smoke",
            "Expected": "It passes.",
            "Automated": "Yes",
            "Evidence": "tests/test_{}.py".format(
                _tc["TC-ID"].lower().replace("-", "_")
            ),
            "Status": "Accepted",
        }
    )


def srs():
    """The two requirements, fresh copies."""
    return copy.deepcopy(_SRS)


def llrs(**status):
    """The four design rows, fresh copies; `status` maps a row id to the
    Status it should carry instead of `Accepted`."""
    rows = copy.deepcopy(_LLRS)
    for row in rows:
        row["Status"] = status.get(row["LLR-ID"], row["Status"])
    return rows


def tcs(drop=()):
    """The four test cases, fresh copies, less the ids in `drop`."""
    return [row for row in copy.deepcopy(_TCS) if row["TC-ID"] not in drop]


def row(rid, rows):
    """The row of `rows` whose id is `rid`."""
    return next(
        r for r in rows if rid in (r.get("LLR-ID"), r.get("TC-ID"), r.get("SR-ID"))
    )


# The carrier's key for each column the rows above use.
_KEY = {
    "Title": "title",
    "SN-Refs": "sn_refs",
    "SR-Refs": "sr_refs",
    "Parent": "parent",
    "Requirement": "requirement",
    "Rationale": "rationale",
    "AcceptanceCriteria": "acceptance_criteria",
    "Priority": "priority",
    "VerificationMethod": "verification_method",
    "Status": "status",
    "Phase": "phase",
    "Detail": "detail",
    "Verifies": "verifies",
    "Level": "level",
    "Method": "method",
    "Tier": "tier",
    "Expected": "expected",
    "Automated": "automated",
    "Evidence": "evidence",
}
_LISTS = {"SN-Refs", "SR-Refs", "Verifies"}


def _value(col, value):
    """One cell spelled as the TOML carrier stores it."""
    if col in _LISTS:
        items = [v for v in str(value).split(";") if v]
        return "[{}]".format(", ".join('"{}"'.format(v) for v in items))
    if col == "Phase":
        return str(int(value))
    return '"{}"'.format(value)


def _toml(table, id_col, rows):
    out = []
    for r in rows:
        out.append("[{}.{}]".format(table, r[id_col]))
        out += [
            "{} = {}".format(_KEY[col], _value(col, value))
            for col, value in r.items()
            if col != id_col and value not in ("", None)
        ]
        out.append("")
    return "\n".join(out)


def write(root, sr_rows=None, llr_rows=None, tc_rows=None):
    """Lay the registries into `root` (the tree above unless rows are given)
    and return `root` as a Path."""
    root = Path(root)
    req = root / "docs" / "requirements"
    test = root / "docs" / "test"
    req.mkdir(parents=True, exist_ok=True)
    test.mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.toml").write_text(
        '[need.SN-001]\nstatus = "Accepted"\nneed = "Reviewers move records."\n'
        'why = "Records live in two tools."\nacceptance = "A moved record reads the same."\n',
        encoding="utf-8",
    )
    (req / "system-requirements.toml").write_text(
        _toml("requirement", "SR-ID", srs() if sr_rows is None else sr_rows),
        encoding="utf-8",
    )
    (req / "low-level-requirements.toml").write_text(
        _toml("design", "LLR-ID", llrs() if llr_rows is None else llr_rows),
        encoding="utf-8",
    )
    (test / "test-cases.toml").write_text(
        _toml("test", "TC-ID", tcs() if tc_rows is None else tc_rows),
        encoding="utf-8",
    )
    return root
