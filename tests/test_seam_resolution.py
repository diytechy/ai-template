"""The IF tier's row shape and the invariants it rests on (OI-67 ruled (a)).

One row is ONE OWNER, its CONSUMERS and a TYPED STATEMENT: `owner` is the
providing thing in the one spelling `consumers` uses, `channel` is closed, and
nothing on the row is derived from a design row any more. The shape is only
honest while four things hold, so they are asserted here over the LIVE
registry rather than argued in a log:

* **no retired cell survives** — a row still carrying `provider`, `req_refs`,
  `signal`, `signal_note` or `component` (or the WI-455 trio before them)
  would read as empty to every updated reader while looking authored to a
  human;
* **the far side is exactly one of `requestors` / `consumers`** — the key is
  the direction, and a row naming both or neither has none;
* **every owner is one component, never a requirement id or a file** — an
  `SR-###`/`LLR-###` or a path in the cell is a shape the rulings retired;
* **every endpoint resolves** — a component id a live row has, or an
  `external:` party the registry header declares (revision 35); a component
  may sit on both sides of its own row, files of it reading what it emits;
* **every channel is in the closed set**, so the typed statement types.

The legacy `contract` cell is deliberately NOT asserted absent here: it is
counted by `trace.py` and leaves row by row as the definitions move into the
owners' headers; the arming slice is where its absence becomes a rule.
"""

import re
import tomllib

from conftest import ROOT, load_script

CARRIER = load_script("spine_carrier")

# `kitlib` is a package beside the scripts, so it imports directly once
# loading a script has put scripts/ on sys.path.
from kitlib import spine as KIT  # noqa: E402

LIVE_IFS = ROOT / "docs" / "requirements" / "interfaces.toml"

RETIRED = {
    "provider",
    "req_refs",
    "signal",
    "signal_note",
    "direction",
    "this_project",
    "counterpart",
    "component",
}
_ID_SHAPED = re.compile(r"^(?:SN|SR|LLR|TC|IF|B|EXT|REL)-\d+$")
LIVE_CMPS = ROOT / "docs" / "requirements" / "components.toml"
TRACE_TEXT = load_script("trace_text")


def _live_rows():
    return [
        r
        for r in CARRIER.load(LIVE_IFS, "IF-ID", keep_examples=False)
        if (r.get("IF-ID") or "").startswith("IF-")
    ]


def _resolves(endpoint):
    cmps = set(tomllib.loads(LIVE_CMPS.read_text(encoding="utf-8"))["component"])
    parties = TRACE_TEXT.declared_parties(LIVE_IFS.read_text(encoding="utf-8"))
    return TRACE_TEXT.endpoint_problem(endpoint, cmps, parties) is None


def test_no_live_row_carries_a_retired_cell():
    raw = tomllib.loads(LIVE_IFS.read_text(encoding="utf-8"))["interface"]
    retired = {
        rid: sorted(set(cells) & RETIRED)
        for rid, cells in raw.items()
        if set(cells) & RETIRED
    }
    assert retired == {}
    # And every row carries the two required endpoint cells, the consumers as
    # a LIST and the channel as a plain string.
    assert [rid for rid, cells in raw.items() if not cells.get("owner")] == []
    # The far side is EXACTLY one of the two keys, and a list either way.
    assert [
        rid
        for rid, cells in raw.items()
        if bool(cells.get("requestors")) == bool(cells.get("consumers"))
    ] == []
    assert [
        rid
        for rid, cells in raw.items()
        if not isinstance(cells.get("requestors") or cells.get("consumers"), list)
    ] == []
    assert [rid for rid, cells in raw.items() if not cells.get("channel")] == []


def test_every_endpoint_is_a_live_component_or_a_declared_party():
    for row in _live_rows():
        rid = row["IF-ID"]
        owner = KIT.seam_owner(row)
        assert owner and ";" not in owner, rid
        assert not _ID_SHAPED.match(owner), rid
        _inbound, far = KIT.seam_far_side(row)
        assert far, rid
        for endpoint in [owner] + far:
            assert _resolves(endpoint), (rid, endpoint)


def test_every_channel_is_in_the_closed_set():
    for row in _live_rows():
        assert (row.get("Channel") or "").strip() in KIT.IF_CHANNELS, row["IF-ID"]


def test_seam_owner_reads_the_cell_verbatim_and_derives_nothing():
    # Precedence is gone with the derivation: the cell IS the answer. A row
    # with no cell answers '' — the required-field rule's finding, never this
    # reader's guess.
    assert KIT.seam_owner({"IF-ID": "IF-001", "Owner": "scripts/b"}) == "scripts/b"
    assert KIT.seam_owner({"IF-ID": "IF-001", "Owner": "  docs/stack.ini "}) == (
        "docs/stack.ini"
    )
    assert KIT.seam_owner({"IF-ID": "IF-001"}) == ""
    assert not hasattr(KIT, "seam_provider")
    # The far side comes back with its direction, requestors first.
    assert KIT.seam_far_side({"Requestors": "a;b"}) == (True, ["a", "b"])
    assert KIT.seam_far_side({"Consumers": "c"}) == (False, ["c"])
    assert KIT.seam_far_side({}) == (False, [])
