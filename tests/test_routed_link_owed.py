"""A row whose adjudicated link moved is owed on the acceptance surfaces
(WI-1069; LLR-484, TC-571).

An adjudicated link is a routed traced cell: a requirement's `SN-Refs`,
`Boundary-Refs` and `Constrains`, a design row's `SR-Refs` and `Constrains`,
and a test case's `Verifies`. It carries no prose, so it is not accepted text,
but an acceptance act leaves a row whose link moved at its recorded text until
an act names it. The acceptance model therefore lists such a row's chain even
when no accepted cell moved, and the two operator surfaces built on the model
(the acceptance brief and the open-items page) show the link, before and
after, under a label saying it goes to a sitting. A row whose only moved
cells are trace cells no adjudicator judges still lists nothing.

In process over `tests/routed_link_fixtures.py`'s four chains.
"""

import pytest
import routed_link_fixtures as fx
from conftest import load_script

gen_open_items = load_script("gen_open_items")
record_rows = load_script("record_rows")
spine_carrier = load_script("spine_carrier")
trace = load_script("trace")


def _moved(tmp_path):
    root = tmp_path / "repo"
    fx.move_all(root, fx.seed(root))
    return root


@pytest.mark.parametrize(
    "key",
    sorted(fx.LINK_MOVES),
    ids=lambda k: "{}:{}".format(k[0].split("/")[-1], k[1]),
)
def test_a_link_moved_alone_puts_its_chain_in_the_model(tmp_path, key):
    """Implements: TC-571"""
    root = tmp_path / "repo"
    rows = fx.seed(root)
    assert fx.model(root) == []  # the premise: nothing owes before the move
    fx.move_link(root, rows, key)
    rid = fx.LINK_MOVES[key][0]
    row = fx.chain_row(fx.model(root), "SR-001", rid)
    assert row is not None, "SR-001's chain is not listed for {}".format(key)
    assert row["state"] == "changed", row
    assert row["routed"] == frozenset({key[1]}), row
    assert row["accepted"] == frozenset(), row


def test_the_moved_links_are_the_routing_table():
    """Implements: TC-571"""
    table = {
        (spine_carrier.stem(rel), cell)
        for rel, cells in record_rows.ROUTED_TRACED_CELLS.items()
        for cell in cells
    }
    moved = {(spine_carrier.stem(rel), cell) for rel, cell in fx.LINK_MOVES}
    assert moved == table


def test_a_row_moving_only_unjudged_trace_cells_lists_no_chain(tmp_path):
    """Implements: TC-571"""
    root = tmp_path / "repo"
    rows = fx.seed(root)
    rows[fx.LLR_REL]["LLR-004"]["phase"] = 2
    rows[fx.LLR_REL]["LLR-004"]["hat_refs"] = ["SECURITY"]
    fx.write(root, rows)
    assert fx.model(root) == []


def test_the_model_lists_the_moved_chains_and_not_the_unjudged_one(tmp_path):
    """Implements: TC-571"""
    entries = fx.model(_moved(tmp_path))
    assert [e["id"] for e in entries] == ["SR-001", "SR-002", "SR-003"]


def test_each_row_carries_its_accepted_cells_and_links_apart(tmp_path):
    """Implements: TC-571"""
    entries = fx.model(_moved(tmp_path))
    first = fx.chain_row(entries, "SR-001", "LLR-001")
    assert first["accepted"] == {"Detail"} and first["routed"] == frozenset()
    link = fx.chain_row(entries, "SR-002", "LLR-002")
    assert link["accepted"] == frozenset() and link["routed"] == {"Constrains"}
    assert link["cells"] == [("Constrains", "", "IF-001")]
    both = fx.chain_row(entries, "SR-003", "LLR-003")
    assert both["accepted"] == {"Detail"} and both["routed"] == {"Constrains"}
    # Accepted cells first, then the links.
    assert [c[0] for c in both["cells"]] == ["Detail", "Constrains"]


def test_a_rows_other_trace_cells_come_last(tmp_path):
    """Implements: TC-571"""
    root = tmp_path / "repo"
    rows = fx.seed(root)
    llr = rows[fx.LLR_REL]["LLR-003"]
    llr.update(detail=fx.DETAIL_MOVED.format(3), constrains=["IF-002"], phase=2)
    fx.write(root, rows)
    row = fx.chain_row(fx.model(root), "SR-003", "LLR-003")
    assert [c[0] for c in row["cells"]] == ["Detail", "Constrains", "Phase"]


def _brief(root):
    reg = trace.load_registries(root / "docs")
    return "\n".join(trace.reaccept_lines(root, reg.srs, reg.llrs, reg.tcs))


def _section(text, head):
    """The lines from heading `head` to the next heading of any level."""
    lines = text.splitlines()
    start = lines.index(head)
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("#")),
        len(lines),
    )
    return "\n".join(lines[start:end])


def test_the_acceptance_brief_lists_a_link_only_row_naming_its_link(tmp_path):
    """Implements: TC-571"""
    text = _brief(_moved(tmp_path))
    assert "## SR-002 — Requirement 2" in text, text
    block = _section(text, "### LLR LLR-002")
    assert "_{}_".format(fx.SITTING) in block, block
    assert "- **Constrains**\n  - before: (empty)\n  - after: IF-001" in block, block
    assert fx.REACCEPT not in block, block


def test_the_acceptance_brief_labels_a_row_with_both(tmp_path):
    """Implements: TC-571"""
    text = _brief(_moved(tmp_path))
    block = _section(text, "### LLR LLR-003")
    assert block.index(fx.REACCEPT) < block.index("**Detail**")
    assert block.index(fx.SITTING) < block.index("**Constrains**")
    # A row of accepted cells alone keeps today's unlabelled list.
    alone = _section(text, "### LLR LLR-001")
    assert "**Detail**" in alone and fx.REACCEPT not in alone, alone


def test_the_operator_page_lists_a_link_only_row_naming_its_link(tmp_path):
    """Implements: TC-571"""
    page = gen_open_items.render(_moved(tmp_path))
    assert 'id="SR-002-accept"' in page
    card = page.split('id="SR-002-accept"', 1)[1].split("</article>", 1)[0]
    assert '<div class="cellgroup">{}</div>'.format(fx.SITTING) in card, card
    assert "Constrains" in card and "IF-001" in card, card


@pytest.mark.parametrize("surface", ["brief", "page"])
def test_both_surfaces_label_the_three_groups_alike(tmp_path, surface):
    """Implements: TC-571"""
    root = tmp_path / "repo"
    rows = fx.seed(root)
    llr = rows[fx.LLR_REL]["LLR-003"]
    llr.update(detail=fx.DETAIL_MOVED.format(3), constrains=["IF-002"], phase=2)
    fx.write(root, rows)
    text = _brief(root) if surface == "brief" else gen_open_items.render(root)
    positions = [text.index(label) for label in (fx.REACCEPT, fx.SITTING, fx.NO_ACT)]
    assert positions == sorted(positions), positions
    # The rendered row's moved phase cell, before and after, sits under the
    # label owing no act.
    under = {
        "brief": "_{}_\n- **Phase**\n  - before: 1\n  - after: 2",
        "page": '{}</div><div class="cellname">Phase ',
    }[surface].format(fx.NO_ACT)
    assert under in text, text[positions[-1] - 200 : positions[-1] + 200]
