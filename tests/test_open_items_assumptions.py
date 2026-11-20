"""The operator's open-items page shows the assumptions and surrogates owing an
acceptance (WI-1010): the rows the acceptance brief's assumption section
renders, taken from the one model both read, each card carrying the row's
cells whole, or a drifted row's moved cells before and after, and the
requirements relying on it.

In-process over a plain file tree, with no git and no subprocess: the brief
tests' own assumption fixture (`test_trace_briefs._assumption_tree`), in which
DA-001 and DA-002 are `Drafted` (DA-002 a fidelity assumption on the `Drafted`
SUR-001), SUR-002 is a `Drafted` surrogate named only by the `Accepted` DA-003,
and SR-001 relies on DA-001.

Implements: TC-448
"""

import re

import pytest
from conftest import load_script
from test_trace_briefs import _ASSUMPTIONS, _assumption_tree

GI = load_script("gen_open_items")
TRACE = load_script("trace")
SNAP = load_script("baseline_snapshot")

ASSUMPTIONS_REL = "docs/requirements/assumptions.toml"
OWING = ["DA-001", "DA-002", "SUR-001", "SUR-002"]
# The page's empty message for section 2, printed only when nothing owes.
EMPTY_SECTION_2 = "no SR owes an acceptance or a re-accept"


def _cards(page):
    """The assumption and surrogate ids the page carries a card for, in order."""
    return re.findall(r'<article class="card" id="((?:DA|SUR)-\d+)-accept">', page)


def _card(page, rid):
    """The `<article>` the page renders for `rid`, failing the test (not
    raising a lookup error) when the page has none."""
    found = re.search(
        r'<article class="card" id="{}-accept">.*?</article>'.format(re.escape(rid)),
        page,
        re.S,
    )
    if found is None:
        pytest.fail("no card for {} on the open-items page".format(rid))
    return found.group(0)


def test_each_row_owing_a_first_acceptance_has_its_card_with_its_cells_whole(
    tmp_path,
):
    """A first acceptance rules on every cell of the row, so each cell is shown
    to its end, past the clip the page's context blocks use; the requirements
    relying on an assumption are named with their text, and a surrogate's card
    names the assumptions naming it. An accepted row that has not moved owes
    nothing and has no card."""
    long_holds = (
        "the operator is at the console " * (TRACE.CELL_TRUNCATE_LIMIT // 30 + 20)
        + "END-OF-HOLDS"
    )
    _assumption_tree(
        tmp_path,
        _ASSUMPTIONS.replace(
            'holds_when = "An operator is at the console."',
            'holds_when = "{}"'.format(long_holds),
        ),
    )
    page = GI.render(tmp_path)
    assert _cards(page) == OWING, _cards(page)
    da1 = _card(page, "DA-001")
    assert ">Drafted, never accepted<" in da1, da1
    for cell in (
        "The operator reads the console after each run.",
        "END-OF-HOLDS",
        "The run is unattended.",
        "A run whose verdict nobody acknowledged.",
        "B-01",
        "OPERATOR-HAT",
    ):
        assert cell in da1, cell
    assert "more chars" not in da1, da1
    assert "<del>" not in da1 and "<ins>" not in da1, da1
    # Relied on by: the citing requirement's id, title and text.
    for needle in ("SR-001", "Show the verdict", "The system shall print each run"):
        assert needle in da1, needle
    sur2 = _card(page, "SUR-002")
    for needle in (
        "Console capture",
        "EXT-001",
        "DA-003",
        "The console stand-in prints as the operator",
    ):
        assert needle in sur2, needle
    assert "DA-003-accept" not in page


def test_an_accepted_assumption_whose_text_moved_shows_it_before_and_after(
    tmp_path,
):
    """An accepted assumption whose accepted cell moved after its copy was
    recorded owes a re-accept: its card is marked DRIFTED and shows the moved
    words both ways, and the header's drifted count takes it in."""
    _assumption_tree(tmp_path)
    SNAP.copy_live(tmp_path, seed=True)
    path = tmp_path / ASSUMPTIONS_REL
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "prints as the operator's terminal does.",
            "prints as the operator's own terminal does.",
        ),
        encoding="utf-8",
        newline="\n",
    )
    page = GI.render(tmp_path)
    card = _card(page, "DA-003")
    assert ">DRIFTED<" in card, card
    assert '<div class="cellname">Assumption' in card, card
    assert "<ins>own </ins>" in card, card
    assert "1 row(s) drifted" in page


def test_the_page_renders_the_briefs_model_and_counts_it(tmp_path):
    """One home for what is owed: the page's cards are the rows of the model
    the acceptance brief renders, in its order, the brief's own headings name
    the same rows, and the header counts them. With only assumptions owing,
    section 2 does not say that nothing is owed."""
    _assumption_tree(tmp_path)
    assert hasattr(TRACE, "assumption_owing_model"), "no shared owing model"
    reg = TRACE.load_registries(tmp_path / "docs")
    model = TRACE.assumption_owing_model(tmp_path, reg.srs, reg.tcs)
    brief = "\n".join(TRACE.assumption_brief_lines(tmp_path, reg.srs, reg.tcs))
    page = GI.render(tmp_path)
    assert [entry[0] for entry in model] == OWING
    assert re.findall(r"^### ((?:DA|SUR)-\d+)", brief, re.M) == OWING
    assert _cards(page) == OWING
    assert "4 assumption(s) or surrogate(s)" in page
    assert EMPTY_SECTION_2 not in page
