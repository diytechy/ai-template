"""gen_verdict_rollup.py's scope set and rendering, called in-process.

The rollup's freshness and exclusive-writer arms are driven on real git repos
and linked worktrees in `test_verdict_record.py`, which is registered in
`tests/conftest.py`'s `SLOW_MODULES`. What those arms regenerate comes from
plain functions over a `tmp_path` tree (`scopes`, `render`, `targets`), pinned
here so the rollup keeps a test in the per-commit smoke tier.
"""

from conftest import load_script

vr = load_script("gen_verdict_rollup")

APPROVE = "# Review A\n\nModel: m\n\nVERDICT: APPROVE findings=0\n"
CHANGES = (
    "# Review A\n\nModel: m\n\n- [MAJOR] a.py:1 -> x -> y -> @o\n\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)


def _reviews(root):
    home = root / "docs" / "reviews"
    lane = home / "wi-401-lane"
    lane.mkdir(parents=True)
    (lane / "001-REVIEW-A-abc1234.md").write_text(APPROVE, encoding="utf-8")
    (lane / "002-REVIEW-A-def5678.md").write_text(CHANGES, encoding="utf-8")
    (lane / "notes.md").write_text("not a round file\n", encoding="utf-8")
    (home / "003-REVIEW-A-0123abc.md").write_text(APPROVE, encoding="utf-8")
    # The generator's own output is never read back as a scope.
    (home / "rollup").mkdir()
    (home / "rollup" / "wi-401-lane.md").write_text("old\n", encoding="utf-8")
    return root


def test_the_scope_set_is_the_round_files_own_train_field(tmp_path):
    found = vr.scopes(_reviews(tmp_path))
    assert sorted(found) == ["", "wi-401-lane"], found
    assert [p.name for p in found["wi-401-lane"]] == [
        "001-REVIEW-A-abc1234.md",
        "002-REVIEW-A-def5678.md",
    ]
    assert [p.name for p in found[""]] == ["003-REVIEW-A-0123abc.md"]


def test_a_scope_renders_one_row_per_round_and_disowns_the_gate(tmp_path):
    root = _reviews(tmp_path)
    text = vr.render(root, "wi-401-lane", vr.scopes(root)["wi-401-lane"])
    assert "The merge gate does\nnot read this file." in text
    assert "| 1 | REVIEW-A | `abc1234` | APPROVE | 0 |" in text
    assert "| 2 | REVIEW-A | `def5678` | CHANGES-REQUESTED | 1 |" in text
    assert "notes.md" not in text


def test_the_flat_layout_gets_the_reserved_stem(tmp_path):
    names = [path.name for path, _text in vr.targets(_reviews(tmp_path))]
    assert names == [vr.FLAT_SCOPE + ".md", "wi-401-lane.md"]
