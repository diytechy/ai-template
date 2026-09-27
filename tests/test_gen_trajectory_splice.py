"""gen_trajectory.py's two panel splices, called in-process.

Every other dashboard test runs the generator over a temp project as a
subprocess and is registered in `tests/conftest.py`'s `SLOW_MODULES`. The two
splices that place the authored Runtime flows and the derived System-context
view into the How-SW panel are pure string functions, pinned here so the
dashboard generator keeps a test in the per-commit smoke tier. Each refuses a
panel it cannot splice rather than emitting an unspliced one.
"""

import pytest

from conftest import load_script

gt = load_script("gen_trajectory")


def test_the_flows_block_goes_in_before_the_panel_closes():
    out = gt._splice_flows_into_panel("<section>x</section>", "<div>F</div>")
    assert out == "<section>x<div>F</div>\n</section>"
    with pytest.raises(ValueError, match="does not end in </section>"):
        gt._splice_flows_into_panel("<section>x", "<div>F</div>")


def test_the_context_view_goes_in_directly_under_the_heading():
    panel = "<section>\n" + gt._SW_HEADING + "structure</section>"
    out = gt._splice_context_into_panel(panel, "<p>C</p>")
    assert out == "<section>\n" + gt._SW_HEADING + "<p>C</p>\nstructure</section>"
    with pytest.raises(ValueError, match="does not open on the architecture"):
        gt._splice_context_into_panel("<section>no heading</section>", "<p>C</p>")
