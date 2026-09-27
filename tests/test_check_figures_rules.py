"""check_figures.py's marker judgement, called in-process.

`test_check_figures.py` drives the checker as a subprocess over temp repos
(every case pays interpreter startup) and is registered in
`tests/conftest.py`'s `SLOW_MODULES`. The judgement those runs rest on is two
pure functions over one line of text, pinned here so the declared-figure
convention keeps a test in the per-commit smoke tier.
"""

from conftest import load_script

figs = load_script("check_figures")


def test_a_marker_needs_both_halves_or_a_derivation():
    assert figs.judge_marker(' cmd="python -m pytest -q" rev=abc1234') is None
    assert figs.judge_marker(' derived="the two runs above, summed"') is None
    assert "no rev=" in figs.judge_marker(' cmd="python -m pytest -q"')
    assert "no cmd=" in figs.judge_marker(" rev=abc1234")
    # An empty value names nothing a reader could rerun: it counts as absent.
    assert "no cmd=" in figs.judge_marker(' cmd="" rev=abc1234')
    assert "empty derivation" in figs.judge_marker(' derived=""')


def test_a_dirty_rev_is_judged_not_waved_through():
    why = figs.judge_marker(' cmd="python -m pytest -q" rev=abc1234-dirty')
    assert why and "DIRTY rev" in why


def test_the_conventions_own_grammar_declares_nothing():
    assert figs.judge_marker(' cmd="<command>" rev=<revision>') is figs.GRAMMAR_EXAMPLE
    # A MIXED marker is a real, half-filled declaration, not grammar.
    why = figs.judge_marker(' cmd="python -m pytest -q" rev=<revision>')
    assert why is not figs.GRAMMAR_EXAMPLE and "no rev=" in why


def test_each_marker_on_a_line_is_judged_on_its_own_text():
    segments = figs.marker_segments('a fig: cmd="x" and fig: rev=abc')
    assert segments == [' cmd="x" and ', " rev=abc"]
    assert all(figs.judge_marker(s) for s in segments), "halves must not merge"
