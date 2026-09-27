"""check_need_form.py's need-cell rule, called in-process.

`test_check_need_form.py` runs the checker as a subprocess over temp
registries (every case pays interpreter startup) and is registered in
`tests/conftest.py`'s `SLOW_MODULES`. The rule those runs rest on,
`need_findings`, takes rows and an exception set and returns findings, so it is
pinned here and keeps the need-form check in the per-commit smoke tier.
"""

from conftest import load_script

nf = load_script("check_need_form")

DIRTY = (
    "A user can resume work from docs/status.md by setting "
    "human_approval_through, as SR-137 describes."
)


def test_each_class_is_named_with_its_row_and_phrase():
    found = nf.need_findings([{"id": "SN-050", "need": DIRTY}], set())
    assert ("SN-050", "internal path", "docs/status.md") in found
    assert ("SN-050", "implementation identifier", "human_approval_through") in found
    assert ("SN-050", "process citation", "SR-137") in found
    # One token, one finding: the path's inner filename is not a second one.
    assert not any(phrase == "status.md" for _, _, phrase in found)


def test_the_exception_list_silences_exactly_its_token():
    found = nf.need_findings([{"id": "SN-050", "need": DIRTY}], {"docs/status.md"})
    phrases = {phrase for _, _, phrase in found}
    assert "docs/status.md" not in phrases
    assert {"human_approval_through", "SR-137"} <= phrases


def test_pairs_urls_cross_refs_and_example_rows_report_nothing():
    rows = [
        {"id": "SN-051", "need": "A requirement/test pair, as SN-003 states."},
        {"id": "SN-052", "need": "See https://example.test/docs/guide.md for it."},
        {"id": "SN-000", "need": DIRTY},
    ]
    assert nf.need_findings(rows, set()) == []
