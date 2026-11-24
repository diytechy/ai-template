"""The amendment brief shows each moved adjudicated link (WI-1069).

An adjudicated link (a routed traced cell) carries no prose, but an act
naming its row records it with the row's accepted text, so a sitting judging
that row is shown each moved link beside the moved accepted cells, a row
whose only change is a link included, and is asked of a link the question its
routing exists for. A scoped row with nothing to judge is named, never
dropped unnamed; a scope with nothing at all still refuses by name. The
verdict's row grammar is unchanged, and the identity line of a shown row
covers its links (LLR-359).

In process over `tests/routed_link_fixtures.py`'s four chains; the git-backed
amendment-brief suite is `tests/test_adjudicate_brief.py`.
"""

import re

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
        "    - after: IF-001"
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
