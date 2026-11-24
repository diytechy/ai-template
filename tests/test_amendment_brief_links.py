"""The amendment brief shows each moved adjudicated link (WI-1069).

An adjudicated link (a routed traced cell) carries no prose, but an act
naming its row records it with the row's accepted text, so a sitting judging
that row is shown each moved link beside the moved accepted cells, a row
whose only change is a link included, and is asked of a link the question its
routing exists for. A scoped row with nothing to judge is named, never
dropped unnamed; a scope with nothing at all still refuses by name. The
verdict's row grammar is unchanged, and the identity line of a shown row
covers its links (LLR-359).

A row with a moved link is shown with its whole accepted text, and each id a
moved link names is listed once as context, by its tier's identifying cells,
outside every identity (WI-1070).

In process over `tests/routed_link_fixtures.py`'s four chains; the git-backed
amendment-brief suite is `tests/test_adjudicate_brief.py`.
"""

import re
import shutil

import pytest
import routed_link_fixtures as fx
from conftest import ROOT, load_script

ab = load_script("adjudicate_brief")
acceptance_record = load_script("acceptance_record")
spine_carrier = load_script("spine_carrier")
from kitlib import verdict as kverdict  # noqa: E402  (scripts/ is on the path)

amendment_brief = ab.amendment_brief
_JUDGED = re.compile(r"^JUDGED-TEXT: (\S+) (\S+)$", re.M)
_SHOWN = re.compile(r"^- (?:SR|LLR|TC) (\S+)", re.M)
NOT_SHOWN = "Scoped, nothing to judge (not shown; rule no line for them): {}."
LINK_QUESTION = "does the row's text state what the link now points at?"
UNMOVED = (
    "  - Unmoved accepted cells (with the cells above, the row's whole accepted text):"
)


def _moved(tmp_path):
    root = tmp_path / "repo"
    fx.move_all(root, fx.seed(root))
    return root


def _row(scope, brief="amendment"):
    return {"WI-ID": "WI-301", "Brief": brief, "Adjudicates": scope}


def _values(root, scope):
    values, why = amendment_brief.amendment_values(root, _row(scope))
    assert why is None, why
    return values


def _block(rows, rid):
    """The block of shown row `rid`: its head line and its indented lines."""
    lines = rows.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("- LLR " + rid))
    end = next(
        (i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def test_the_brief_shows_each_moved_link_beside_its_accepted_cells(tmp_path):
    """Implements: TC-161"""
    rows = _values(_moved(tmp_path), "LLR-001;LLR-002;LLR-003")["rows"]
    assert _SHOWN.findall(rows) == ["LLR-001", "LLR-002", "LLR-003"], rows
    only_text = _block(rows, "LLR-001")
    assert "  - Detail\n" in only_text and "(link)" not in only_text, only_text
    assert _block(rows, "LLR-002") == (
        "- LLR LLR-002 (chain of SR-002)\n"
        "  - Constrains (link)\n"
        "    - before: (empty)\n"
        "    - after: IF-001\n" + UNMOVED + "\n"
        "    - Detail: Design row 2 adds.\n"
        "    - Title: Design 2"
    )
    both = _block(rows, "LLR-003")
    assert both.index("  - Detail\n") < both.index("  - Constrains (link)\n"), both
    assert "    - after: IF-002" in both, both


def test_a_link_only_scope_composes_instead_of_refusing(tmp_path):
    """Implements: TC-161"""
    values = _values(_moved(tmp_path), "LLR-002")
    assert _SHOWN.findall(values["rows"]) == ["LLR-002"]
    assert [rid for rid, _d in _JUDGED.findall(values["identity"])] == ["LLR-002"]


def test_an_unjudged_trace_cell_never_reaches_the_judge(tmp_path):
    """Implements: TC-161"""
    root = _moved(tmp_path)
    values, why = amendment_brief.amendment_values(root, _row("LLR-004"))
    assert values is None
    assert "(LLR-004)" in why and "adjudicated link" in why, why
    shown = _values(root, "LLR-003")["rows"]
    assert "Phase" not in shown and "Hat-Refs" not in shown


def test_a_scoped_row_with_nothing_to_judge_is_named_not_dropped(tmp_path):
    """Implements: TC-161"""
    rows = _values(_moved(tmp_path), "LLR-001;LLR-004;TC-002")["rows"]
    assert _SHOWN.findall(rows) == ["LLR-001"], rows
    assert rows.splitlines()[-1] == NOT_SHOWN.format("LLR-004, TC-002"), rows


def test_a_combined_sitting_shows_a_link_only_amendment_row(tmp_path):
    """Implements: TC-161"""
    root = _moved(tmp_path)
    row = _row("amendment:LLR-002;amendment:LLR-003", brief="combined")
    text, why = ab.compose(root, row, root / "docs/reviews/v.md")
    assert why is None, why
    assert "  - Constrains (link)\n    - before: (empty)\n    - after: IF-001" in text
    assert set(ab.requested_identities(text)) == {"LLR-002", "LLR-003"}


def test_the_brief_asks_the_link_question(tmp_path):
    """Implements: TC-161"""
    root = _moved(tmp_path)
    text, why = ab.compose(root, _row("LLR-002"), root / "docs/reviews/v.md")
    assert why is None, why
    assert LINK_QUESTION in text, text
    assert "--- AMENDED CELLS AND MOVED LINKS (before/after, per row) ---" in text


def test_a_link_only_rows_verdict_line_reads_as_any_rows():
    """Implements: TC-161"""
    part = (
        "- [CLARITY] LLR-002 Constrains -> constrains nothing -> constrains "
        "IF-001 -> the detail already states it\n\nVERDICT: CLARITY rows=1\n"
    )
    assert kverdict.row_rulings(part, "amendment") == {"LLR-002": "CLARITY"}


def test_a_shown_link_only_rows_identity_covers_its_link(tmp_path):
    """Implements: TC-398"""
    root = _moved(tmp_path)
    identity = dict(_JUDGED.findall(_values(root, "LLR-002")["identity"]))
    loaded = spine_carrier.load(root / fx.LLR_REL, "LLR-ID", keep_examples=False)
    live = {r["LLR-ID"]: r for r in loaded}["LLR-002"]
    digest = acceptance_record.accepted_text_digest
    assert identity["LLR-002"] == digest(fx.LLR_REL, "LLR-ID", live)
    unlinked = dict(live, Constrains="")
    assert identity["LLR-002"] != digest(fx.LLR_REL, "LLR-ID", unlinked)


def test_the_template_states_the_link_question_once():
    """Implements: TC-161"""
    template = (
        ROOT / "project-trajectory/prompts/adjudicate-amendment.template.md"
    ).read_text(encoding="utf-8")
    body = template.split("-->", 1)[1]
    assert body.count(LINK_QUESTION) == 1, body


# --- WI-1070: the row's whole text and the rows its links name ----------------

LINKED_HEAD = (
    "--- ROWS THE MOVED LINKS NAME (context for the LINKS question: not under "
    "judgement, and in no JUDGED-TEXT identity) ---"
)
IDENTITY_HEAD = (
    "--- JUDGED TEXT (the identity of each row shown for judgement: its accepted "
    "cells and adjudicated links; the rows listed as context above are not in "
    "it) ---"
)
NO_LINK = "(no moved link in this brief names a row)"


def _context(tmp_path, moves, rows=None, **named):
    """The four chains and the rows a link names, recorded, then each
    `(registry, row id, key, value)` of `moves` written over them."""
    root = tmp_path / "repo"
    rows = fx.seed(root, context=True, rows=rows, **named)
    for rel, rid, key, value in moves:
        rows[rel][rid][key] = value
    fx.write(root, rows)
    return root


def _listed(linked, rid):
    """The listing's entry for `rid`: its head line and its indented lines."""
    lines = linked.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("- " + rid + " "))
    end = next(
        (i for i in range(start + 1, len(lines)) if not lines[i].startswith(" ")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def test_a_link_only_row_is_shown_with_its_whole_accepted_text(tmp_path):
    """Implements: TC-161"""
    block = _block(_values(_moved(tmp_path), "LLR-002")["rows"], "LLR-002")
    assert block.splitlines()[-3:] == [
        UNMOVED,
        "    - Detail: Design row 2 adds.",
        "    - Title: Design 2",
    ], block
    for absent in ("Phase", "Status", "LLR-ID", "SR-Refs"):
        assert absent not in block, block


def test_a_row_with_both_lists_its_unmoved_cells_after_its_moved_ones(tmp_path):
    """Implements: TC-161"""
    block = _block(_values(_moved(tmp_path), "LLR-003")["rows"], "LLR-003")
    assert block.index("  - Detail\n") < block.index("  - Constrains (link)\n")
    assert block.index("  - Constrains (link)\n") < block.index(UNMOVED), block
    assert block.split(UNMOVED, 1)[1] == "\n    - Title: Design 3", block


def test_a_row_whose_accepted_cell_alone_moved_lists_no_unmoved_cells(tmp_path):
    """Implements: TC-161"""
    block = _block(_values(_moved(tmp_path), "LLR-001")["rows"], "LLR-001")
    assert UNMOVED not in block and "Title" not in block, block


def test_a_linked_row_whose_every_accepted_cell_moved_lists_none(tmp_path):
    """Implements: TC-161"""
    root = _context(
        tmp_path,
        [
            (fx.LLR_REL, "LLR-002", "constrains", ["IF-001"]),
            (fx.LLR_REL, "LLR-002", "detail", fx.DETAIL_MOVED.format(2)),
            (fx.LLR_REL, "LLR-002", "title", "Design two"),
        ],
    )
    block = _block(_values(root, "LLR-002")["rows"], "LLR-002")
    assert block.splitlines()[-2:] == [UNMOVED, "    - (none)"], block


def _shown_cells(block):
    """`{cell: text}` a shown block states as the row's current text: each
    moved cell's and link's `after`, and each unmoved cell."""
    cells, name = {}, None
    for line in block.splitlines()[1:]:
        if line.startswith("    - after: "):
            after = line[len("    - after: ") :]
            cells[name] = "" if after == "(empty)" else after
        elif line.startswith("  - ") and line != UNMOVED:
            name = line[4:].replace(" (link)", "")
        elif line.startswith("    - ") and not line.startswith("    - before: "):
            key, _, text = line[6:].partition(": ")
            cells[key] = text
    return cells


def test_each_shown_rows_cells_digest_to_its_identity_line(tmp_path):
    """Implements: TC-161"""
    values = _values(_moved(tmp_path), "LLR-001;LLR-002;LLR-003")
    identity = dict(_JUDGED.findall(values["identity"]))
    loaded = spine_carrier.load(
        tmp_path / "repo" / fx.LLR_REL, "LLR-ID", keep_examples=False
    )
    live = {r["LLR-ID"]: r for r in loaded}
    for rid in ("LLR-002", "LLR-003"):
        shown = _shown_cells(_block(values["rows"], rid))
        # The identity also covers the row's unmoved links, which the brief
        # does not show (its head names the chains); every accepted cell it
        # covers is shown.
        shown["SR-Refs"] = live[rid]["SR-Refs"]
        digest = acceptance_record.accepted_text_digest(fx.LLR_REL, "LLR-ID", shown)
        assert digest == identity[rid], (rid, shown)


# One move per routed cell (`fx.LINK_MOVES`), with the entries it lists.
_TIER_ENTRIES = {
    (fx.SR_REL, "SN-Refs"): [
        "- SN-001 (need), named by SR-001 SN-Refs (before, after)\n"
        "  - Need: A user is served one.",
        "- SN-002 (need), named by SR-001 SN-Refs (after)\n"
        "  - Need: A user is served two.",
    ],
    (fx.SR_REL, "Boundary-Refs"): [
        "- B-01 (boundary crossing), named by SR-001 Boundary-Refs (after)\n"
        "  - Direction: out\n"
        "  - Entity: EXT-001 (Person)\n"
        "  - Carries: " + fx.CARRIES,
    ],
    (fx.SR_REL, "Constrains"): [
        "- IF-001 (interface), named by SR-001 Constrains (after)\n"
        "  - Channel: file\n"
        "  - Owner: CMP-001\n"
        "  - Data: " + fx.IF_DATA[0],
    ],
    (fx.LLR_REL, "SR-Refs"): [
        "- SR-001 (requirement), named by LLR-001 SR-Refs (before, after)\n"
        "  - Title: Requirement 1\n"
        "  - Requirement: The system shall do thing 1.",
        "- SR-002 (requirement), named by LLR-001 SR-Refs (after)\n"
        "  - Title: Requirement 2\n"
        "  - Requirement: The system shall do thing 2.",
    ],
    (fx.LLR_REL, "Constrains"): [
        "- IF-001 (interface), named by LLR-001 Constrains (after)\n"
        "  - Channel: file\n"
        "  - Owner: CMP-001\n"
        "  - Data: " + fx.IF_DATA[0],
    ],
    (fx.TC_REL, "Verifies"): [
        "- SR-001 (requirement), named by TC-001 Verifies (after)\n"
        "  - Title: Requirement 1\n"
        "  - Requirement: The system shall do thing 1.",
        "- LLR-001 (design row), named by TC-001 Verifies (before, after)\n"
        "  - Title: Design 1\n"
        "  - Detail: Design row 1 adds.",
    ],
}


@pytest.mark.parametrize("key", sorted(fx.LINK_MOVES), ids="-".join)
def test_each_tier_a_link_names_is_listed_by_its_identifying_cells(tmp_path, key):
    """Implements: TC-161"""
    rid, cell, value = fx.LINK_MOVES[key]
    root = _context(tmp_path, [(key[0], rid, cell, value)])
    linked = _values(root, rid)["linked"]
    entries = _TIER_ENTRIES[key]
    assert linked == "\n".join(entries), linked


def test_an_interface_with_a_stated_contract_is_listed_by_it(tmp_path):
    """Implements: TC-161"""
    root = _context(tmp_path, [(fx.LLR_REL, "LLR-002", "constrains", ["IF-002"])])
    assert _listed(_values(root, "LLR-002")["linked"], "IF-002") == (
        "- IF-002 (interface), named by LLR-002 Constrains (after)\n"
        "  - Channel: file\n"
        "  - Owner: CMP-001\n"
        "  - Contract: " + fx.CONTRACT
    )
    shutil.rmtree(root / "src")  # no scan root: no contract can be read
    entry = _listed(_values(root, "LLR-002")["linked"], "IF-002")
    assert entry.endswith("  - Data: " + fx.IF_DATA[1]), entry
    assert "Contract" not in entry, entry


def test_an_id_naming_no_live_row_is_listed_as_naming_none(tmp_path):
    """Implements: TC-161"""
    root = _context(tmp_path, [(fx.LLR_REL, "LLR-002", "constrains", ["IF-009"])])
    assert _values(root, "LLR-002")["linked"] == (
        "- IF-009 (interface), named by LLR-002 Constrains (after): names no live row"
    )
    # With no interfaces registry at all, every interface id names none.
    bare = _values(_moved(tmp_path / "bare"), "LLR-002")["linked"]
    assert bare == (
        "- IF-001 (interface), named by LLR-002 Constrains (after): names no live row"
    )


def test_a_row_named_by_several_links_is_listed_once_naming_each(tmp_path):
    """Implements: TC-161"""
    rows = fx.base_rows()
    rows[fx.LLR_REL]["LLR-004"]["constrains"] = ["IF-002"]
    root = _context(
        tmp_path,
        [
            (fx.LLR_REL, "LLR-002", "constrains", ["IF-001"]),
            (fx.LLR_REL, "LLR-003", "constrains", ["IF-001"]),
            (fx.LLR_REL, "LLR-004", "constrains", ["IF-001"]),
        ],
        rows=rows,
    )
    linked = _values(root, "LLR-002;LLR-003;LLR-004")["linked"]
    heads = [ln for ln in linked.splitlines() if ln.startswith("- ")]
    assert heads == [
        "- IF-001 (interface), named by LLR-002 Constrains (after); "
        "LLR-003 Constrains (after); LLR-004 Constrains (after)",
        "- IF-002 (interface), named by LLR-004 Constrains (before)",
    ], linked


def test_a_long_listed_cell_is_clipped_stating_the_clip_and_its_length(tmp_path):
    """Implements: TC-161"""
    words = " ".join("word{}".format(n) for n in range(600))
    contract = words[:1500] + "\n" + words[1500:]
    root = _context(
        tmp_path,
        [(fx.LLR_REL, "LLR-002", "constrains", ["IF-002"])],
        contract=contract,
        needs=("A user is\nserved one.", fx.NEEDS[1]),
    )
    entry = _listed(_values(root, "LLR-002")["linked"], "IF-002")
    line = entry.splitlines()[-1]
    flat = " ".join(contract.split())
    clip = " … [clipped at 2400 of {} characters]".format(len(flat))
    assert line.startswith("  - Contract: ") and line.endswith(clip), line
    shown = line[len("  - Contract: ") : -len(clip)]
    assert len(shown) <= 2400 and flat.startswith(shown + " "), shown[-40:]
    moved = _context(
        tmp_path / "need",
        [(fx.SR_REL, "SR-001", "sn_refs", ["SN-001", "SN-002"])],
        needs=("A user is\nserved one.", fx.NEEDS[1]),
    )
    assert "  - Need: A user is served one." in _values(moved, "SR-001")["linked"]


def test_a_named_row_shown_for_judgement_is_listed_as_shown_above(tmp_path):
    """Implements: TC-161"""
    root = _context(
        tmp_path,
        [
            (fx.TC_REL, "TC-001", "verifies", ["LLR-001", "SR-001"]),
            (fx.LLR_REL, "LLR-001", "detail", fx.DETAIL_MOVED.format(1)),
        ],
    )
    linked = _values(root, "TC-001;LLR-001")["linked"]
    assert _listed(linked, "LLR-001") == (
        "- LLR-001 (design row), named by TC-001 Verifies (before, after): "
        "shown above for judgement"
    ), linked
    assert "  - Requirement: The system shall do thing 1." in _listed(linked, "SR-001")


def test_a_brief_moving_no_link_says_so_in_its_listing(tmp_path):
    """Implements: TC-161"""
    assert _values(_moved(tmp_path), "LLR-001")["linked"] == NO_LINK


def test_no_listed_row_gets_an_identity_line(tmp_path):
    """Implements: TC-161"""
    forged = "JUDGED-TEXT: SN-002 sha256:0123456789abcdef"
    root = _context(
        tmp_path,
        [(fx.SR_REL, "SR-001", "sn_refs", ["SN-001", "SN-002"])],
        needs=(fx.NEEDS[0], "A user is served two.\n" + forged),
    )
    text, why = ab.compose(root, _row("SR-001"), root / "docs/reviews/v.md")
    assert why is None, why
    assert "  - Need: A user is served two. " + forged in text, text
    assert set(ab.requested_identities(text)) == {"SR-001"}


def test_the_template_labels_the_listing_as_context_outside_the_identity():
    """Implements: TC-161"""
    template = (
        ROOT / "project-trajectory/prompts/adjudicate-amendment.template.md"
    ).read_text(encoding="utf-8")
    body = template.split("-->", 1)[1]
    assert body.index("{rows}") < body.index(LINKED_HEAD) < body.index("{linked}")
    assert body.index("{linked}") < body.index(IDENTITY_HEAD) < body.index("{identity}")
    assert "write no verdict line for a listed row" in body, body


def test_a_combined_sitting_lists_the_rows_its_links_name(tmp_path):
    """Implements: TC-161"""
    root = _context(
        tmp_path,
        [
            (fx.LLR_REL, "LLR-002", "constrains", ["IF-001"]),
            (fx.LLR_REL, "LLR-003", "constrains", ["IF-001", "IF-002"]),
            (fx.LLR_REL, "LLR-003", "detail", fx.DETAIL_MOVED.format(3)),
        ],
    )
    row = _row("amendment:LLR-002;amendment:LLR-003", brief="combined")
    text, why = ab.compose(root, row, root / "docs/reviews/v.md")
    assert why is None, why
    section = text.split("=== SECTION `## amendment` ===", 1)[1]
    assert UNMOVED + "\n    - Detail: Design row 2 adds." in section, section
    named = "- IF-001 (interface), named by LLR-002 Constrains (after); LLR-003"
    assert text.count(named) == 1 and text.count("- IF-002 (interface)") == 1
    assert text.index(LINKED_HEAD) < text.index(named) < text.index(IDENTITY_HEAD)
    assert "  - Contract: " + fx.CONTRACT in section
