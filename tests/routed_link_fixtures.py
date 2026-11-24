"""The four-chain project the routed-link suites share (WI-1069).

Four accepted requirements, SR-001 to SR-004, each with one accepted design
row (LLR-00n) and one accepted test case (TC-00n) verifying it, written on
the TOML carrier and recorded in a first acceptance copy. `move_all` then
moves one row of each chain the four ways a row can differ from its copy:

  * LLR-001: its `detail` alone (accepted text only);
  * LLR-002: an interface added to its `constrains` cell (a routed link only);
  * LLR-003: both;
  * LLR-004: its `phase` and `hat_refs` alone (trace cells no adjudicator
    judges).

`LINK_MOVES` moves one routed link of one tier instead, one per cell of the
routing table. `seed(root, context=True)` also writes, before the record is
taken, the rows a link can name beyond the four chains (WI-1070): two needs,
a boundary crossing and its entity, and two interfaces, IF-001 with a data
cell alone and IF-002 whose contract a module under the default scan root
states. No `test_` prefix, so it is never collected.
"""

from conftest import load_script

from kitlib import spine  # noqa: E402  (scripts/ is on the path)

snap = load_script("baseline_snapshot")
trace = load_script("trace")

SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"

DETAIL_MOVED = "Design row {} now rounds the result."
SITTING = "adjudicated link — goes to a sitting"
REACCEPT = "accepted — re-acceptance owed"
NO_ACT = "other trace cell — owes no act"


def _sr(n):
    return {
        "sn_refs": ["SN-001"],
        "title": "Requirement {}".format(n),
        "requirement": "The system shall do thing {}.".format(n),
        "rationale": "the demo",
        "acceptance_criteria": "thing {} is done".format(n),
        "verification_method": "Test",
        "status": "Accepted",
        "phase": 1,
    }


def _llr(n):
    return {
        "sr_refs": ["SR-00{}".format(n)],
        "title": "Design {}".format(n),
        "detail": "Design row {} adds.".format(n),
        "status": "Accepted",
        "phase": 1,
    }


def _tc(n):
    return {
        "verifies": ["LLR-00{}".format(n)],
        "level": "Unit",
        "method": "run case {}".format(n),
        "tier": "Smoke",
        "expected": "case {} passes".format(n),
        "automated": "Yes",
        "evidence": "tests/test_demo.py",
        "status": "Accepted",
        "phase": 1,
    }


def base_rows():
    """`{registry: {id: cells}}` of the four chains, every row accepted."""
    ns = range(1, 5)
    return {
        SR_REL: {"SR-00{}".format(n): _sr(n) for n in ns},
        LLR_REL: {"LLR-00{}".format(n): _llr(n) for n in ns},
        TC_REL: {"TC-00{}".format(n): _tc(n) for n in ns},
    }


_TABLES = {SR_REL: "requirement", LLR_REL: "design", TC_REL: "test"}


def write(root, rows):
    """Write each registry of `rows` (`base_rows`' shape) under `root`."""
    for rel, table in _TABLES.items():
        text = "".join(
            "[{}.{}]\n{}\n".format(table, rid, spine.toml_fields(cells.items()))
            for rid, cells in rows[rel].items()
        )
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))


def seed(root, context=False, rows=None, **named):
    """The four chains (`rows`, else `base_rows()`) written under `root`, with
    the rows a link names when `context` (`write_context`, given `named`),
    and recorded whole. `rows`."""
    rows = rows or base_rows()
    write(root, rows)
    if context:
        write_context(root, **named)
    snap.copy_live(root, seed=True)
    return rows


SN_REL = "docs/requirements/stakeholder-needs.toml"
EXT_REL = "docs/requirements/external.toml"
IF_REL = "docs/requirements/interfaces.toml"
NEEDS = ("A user is served one.", "A user is served two.")
CARRIES = "Read: the demo report."
IF_DATA = ("the demo record, one per call", "the demo seam's typed summary")
CONTRACT = "the demo seam's stated form: one record per call, never two."


def _table(kind, rid, pairs):
    return "[{}.{}]\n{}\n".format(kind, rid, spine.toml_fields(pairs))


def write_context(root, needs=NEEDS, contract=CONTRACT):
    """The rows a link can name beyond the chains: needs SN-001 and SN-002
    (`needs`), the entity EXT-001 and the crossing B-01, the interfaces
    IF-001 (data only) and IF-002, whose `contract` the module `src/demo.py`
    states (each line of it indented as a continuation)."""
    texts = {
        SN_REL: "".join(
            _table(
                "need",
                "SN-00{}".format(n),
                [
                    ("status", "Accepted"),
                    ("need", text),
                    ("why", "why"),
                    ("priority", "M"),
                    ("acceptance", "ac"),
                ],
            )
            for n, text in enumerate(needs, 1)
        ),
        EXT_REL: _table(
            "entity",
            "EXT-001",
            [
                ("name", "Person"),
                ("class", "operational"),
                ("description", "The person."),
                ("status", "Accepted"),
            ],
        )
        + _table(
            "boundary",
            "B-01",
            [
                ("entity", "EXT-001"),
                ("direction", "out"),
                ("system", "operation"),
                ("carries", CARRIES),
                ("status", "Accepted"),
            ],
        ),
        IF_REL: "".join(
            _table(
                "interface",
                "IF-00{}".format(n),
                [
                    ("owner", "CMP-001"),
                    ("consumers", ["CMP-002"]),
                    ("channel", "file"),
                    ("data", data),
                    ("version", "v1"),
                    ("status", "Drafted"),
                ],
            )
            for n, data in enumerate(IF_DATA, 1)
        ),
        "src/demo.py": '"""A demo module stating one seam.\n\nContracts: IF-002 '
        '— the demo seam.\n\nContract IF-002: {}\n"""\n'.format(
            "\n    ".join(contract.splitlines())
        ),
    }
    for rel, text in texts.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))


def move_all(root, rows):
    """The four moves of this module's docstring, written over `rows`."""
    llrs = rows[LLR_REL]
    llrs["LLR-001"]["detail"] = DETAIL_MOVED.format(1)
    llrs["LLR-002"]["constrains"] = ["IF-001"]
    llrs["LLR-003"]["detail"] = DETAIL_MOVED.format(3)
    llrs["LLR-003"]["constrains"] = ["IF-002"]
    llrs["LLR-004"]["phase"] = 2
    llrs["LLR-004"]["hat_refs"] = ["SECURITY"]
    write(root, rows)


# One move per routed cell: `(registry, cell) -> (row id, key, value)`, each
# keeping the moved row in SR-001's chain.
LINK_MOVES = {
    (SR_REL, "SN-Refs"): ("SR-001", "sn_refs", ["SN-001", "SN-002"]),
    (SR_REL, "Boundary-Refs"): ("SR-001", "boundary_refs", ["B-01"]),
    (SR_REL, "Constrains"): ("SR-001", "constrains", ["IF-001"]),
    (LLR_REL, "SR-Refs"): ("LLR-001", "sr_refs", ["SR-001", "SR-002"]),
    (LLR_REL, "Constrains"): ("LLR-001", "constrains", ["IF-001"]),
    (TC_REL, "Verifies"): ("TC-001", "verifies", ["LLR-001", "SR-001"]),
}


def move_link(root, rows, key):
    """Move the one routed link `LINK_MOVES[key]` names, written over `rows`."""
    rid, cell, value = LINK_MOVES[key]
    rows[key[0]][rid][cell] = value
    write(root, rows)


def model(root):
    """The acceptance model over `root`'s live registries."""
    reg = trace.load_registries(root / "docs")
    return trace.reaccept_model(root, reg.srs, reg.llrs, reg.tcs)


def chain_row(entries, sid, rid):
    """The row `rid` of SR `sid`'s entry in `entries`, or None."""
    for entry in entries:
        if entry["id"] == sid:
            return next((r for r in entry["rows"] if r["id"] == rid), None)
    return None
