"""A lane's Done-when is fixed at claim (S13, review pack B3): the pure half.

What an item IS, and what counts as a CHANGE to one, decided over text alone so
the three readers that ask - the claim (does this row HAVE a Done-when?), the
reviewer's brief and the merge-time mint (did the lane MOVE it?) - cannot
answer differently. In-memory only: no repository, no subprocess.

Each rule is driven beside its opposite, because a comparison that never flags
and one that flags every tick are both useless, and ticking with evidence is the
normal convention: `- [x] item` and `~~item~~ - LANDED ...` must read as the
item unchanged, while a reworded, deleted or added item must not.
"""

import sys

from conftest import SCRIPTS

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import done_when as kdw  # noqa: E402

SPEC = """+++
id = "WI-401"
title = "Widget"
+++

## Context

Some context, with a list that is NOT the Done-when:

- not an item

## Done-when

- The widget renders at 60 fps on the reference box.
- A test shows the widget refusing an empty frame,
  named in its own module.

### From WI-399 (Done-when, verbatim)

1. The legacy path is deleted.

## Deliverable

Not yet.
"""


def test_the_items_are_the_done_when_sections_own_and_nothing_else():
    items = kdw.items(SPEC)
    assert items == [
        "The widget renders at 60 fps on the reference box.",
        "A test shows the widget refusing an empty frame, named in its own module.",
        "The legacy path is deleted.",
    ], "a continuation line joins its item; a subsection's items belong to it"
    assert kdw.items("+++\nid = 'WI-1'\n+++\n\n## Context\n\n- a bullet\n") == []
    assert kdw.items("") == []


def test_a_row_with_no_done_when_has_none_and_a_prose_one_counts():
    assert not kdw.has_done_when("## Context\n\nwork\n")
    assert not kdw.has_done_when("## Done-when\n\n## Deliverable\n\nx\n"), (
        "an empty section declares nothing"
    )
    assert kdw.has_done_when("## Done when\n\nThe row closes when X ships.\n"), (
        "a prose criterion is still a criterion; the heading is tolerant"
    )


def test_a_tick_with_trailing_evidence_does_not_flag():
    ticked = (
        SPEC.replace(
            "- The widget renders at 60 fps on the reference box.",
            "- [x] The widget renders at 60 fps on the reference box. — "
            "measured 61 fps (docs/log.d/widget.md)",
        )
        .replace(
            "- A test shows",
            "- ~~A test shows",
        )
        .replace(
            "named in its own module.",
            "named in its own module.~~ — **LANDED** "
            "tests/test_widget.py::test_empty_frame",
        )
        .replace("1. The legacy path is deleted.", "1. [X] The legacy path is deleted.")
    )
    assert kdw.changes(SPEC, ticked) == []


def test_a_reworded_item_flags_and_names_both_texts():
    reworded = SPEC.replace("at 60 fps", "at 30 fps")
    assert kdw.changes(SPEC, reworded) == [
        ("changed", "The widget renders at 60 fps on the reference box."),
        ("added", "The widget renders at 30 fps on the reference box."),
    ]


def test_appending_a_qualification_is_not_evidence():
    # Evidence is a FORM, not whatever follows the item: an evidence separator
    # (a dash, an arrow, a bracket, a check mark) AND an evidence token (a
    # completion word, a path or test id, a backticked name, a commit sha).
    # Appended prose that narrows the item is a rewording, punctuation or not.
    narrowed = SPEC.replace("on the reference box.", "on the reference box only")
    assert ("changed", "The widget renders at 60 fps on the reference box.") in (
        kdw.changes(SPEC, narrowed)
    )
    item = "## Done-when\n\n- Tests pass.\n"
    for later in (
        "- Tests pass. Only on Linux.",
        "- [x] Tests pass. Only on Linux.",
        "- [x] Tests pass (only on Linux).",
        "- [x] Tests pass. - except on Windows",
        "- Tests pass on Linux.",
    ):
        assert kdw.changes(item, "## Done-when\n\n" + later + "\n"), later
    for later in (
        "- [x] Tests pass.",
        "- [x] Tests pass. (tests/test_widget.py::test_empty)",
        "- [x] Tests pass. — **LANDED 2026-08-22** (slice 2)",
        "- ~~Tests pass.~~ — DONE in `a1b2c3d`",
        "- [x] Tests pass. -> tests/test_widget.py",
        "- [x] Tests pass. ✓ run 42 at 9f8e7d6c",
    ):
        assert not kdw.changes(item, "## Done-when\n\n" + later + "\n"), later


def test_a_deleted_or_added_item_flags():
    dropped = SPEC.replace("1. The legacy path is deleted.\n", "")
    assert kdw.changes(SPEC, dropped) == [("changed", "The legacy path is deleted.")]
    grown = SPEC.replace(
        "1. The legacy path is deleted.",
        "1. The legacy path is deleted.\n2. The docs say so.",
    )
    assert kdw.changes(SPEC, grown) == [("added", "The docs say so.")]


def test_a_row_that_had_no_done_when_at_claim_reports_what_it_gained():
    assert kdw.changes("## Context\n\nx\n", SPEC) == [
        ("added", item) for item in kdw.items(SPEC)
    ]


def test_the_flag_lines_quote_the_texts_they_compare():
    lines = kdw.describe(kdw.changes(SPEC, SPEC.replace("60 fps", "30 fps")))
    assert lines[0].startswith("- at claim, no longer present as written: ")
    assert "60 fps" in lines[0] and "30 fps" in lines[1]
    assert lines[1].startswith("- added since claim: ")
