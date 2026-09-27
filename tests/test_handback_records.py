"""handback.py's pure text seams: the name-status record reader and the
terminal close's spec rewrite.

`test_handback.py` drives the close and the quarantine through real git lanes
and is registered in `tests/conftest.py`'s `SLOW_MODULES`. The functions here
take strings and return strings, so they are pinned in the per-commit smoke
tier: the record reader was moved out of that module verbatim, and the close
text rewrite is exercised directly.
"""

import pytest

from conftest import load_script

hb = load_script("handback")


def test_the_name_status_stream_is_read_as_records_not_pairs():
    # THE PARSE ITSELF, on the exact field list REVIEW-A round 1 drove. Read two
    # at a time this pairs as ('R100','Aold.py'), ('Anew.py','D'), … — paths in
    # the status slot, the bookkeeping filter blind, and `z_broken.py` (the
    # failing file) past the loop bound. A rename is THREE fields, and
    # `diff.renames` has defaulted true since Git 2.9, so this is ordinary
    # output rather than an exotic case.
    fields = [
        "R100",
        "Aold.py",
        "Anew.py",
        "D",
        "docs/work/active/wi-401/WI-401-widget.md",
        "A",
        "docs/work/queued/WI-401-widget.md",
        "M",
        "z_broken.py",
    ]
    assert hb.diff_records(fields) == [
        ("R100", ["Aold.py", "Anew.py"]),
        ("D", ["docs/work/active/wi-401/WI-401-widget.md"]),
        ("A", ["docs/work/queued/WI-401-widget.md"]),
        ("M", ["z_broken.py"]),
    ]
    # A copy is the other three-field form.
    assert hb.diff_records(["C75", "src/a.py", "src/b.py"]) == [
        ("C75", ["src/a.py", "src/b.py"])
    ]
    # A stream that ends mid-record is a TRUNCATED READ, not an empty diff:
    # None, so the caller refuses rather than quarantining a partial list.
    assert hb.diff_records(["R100", "Aold.py"]) is None
    assert hb.diff_records(["M"]) is None


def test_the_terminal_close_rewrites_the_spec_text_and_only_that():
    # The adjudication row's mechanical close is a text rewrite before it is a
    # move: `specref` is cleared (a closed row carries no forward bridge) and a
    # `## Deliverable` goes in AHEAD of `## Dispositions`, which the merge
    # reads to mint the successors. Idempotent on the Deliverable, so a row an
    # agent already self-closed keeps its own.
    spec = (
        '+++\nid = "WI-9"\nspecref = "docs/log.d/x.md"\n+++\n\n'
        "## Context\n\nc\n\n## Dispositions\n\n- d\n"
    )
    fm, body = hb.spec_move_split(spec)
    assert fm == 'id = "WI-9"\nspecref = "docs/log.d/x.md"\n'
    assert body.startswith("\n## Context")

    closed = hb._adjudication_close_text(spec, "DELIVERED")
    assert 'specref = ""' in closed and "docs/log.d/x.md" not in closed
    assert closed.index("## Deliverable") < closed.index("## Dispositions")
    assert "DELIVERED" in closed and "- d" in closed
    assert hb._adjudication_close_text(closed, "A SECOND ONE") == closed

    # A spec without its fences is refused, never rewritten into a new shape.
    with pytest.raises(ValueError):
        hb.spec_move_split("## Context\n")
