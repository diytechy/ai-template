"""The id watermark across `bootstrap --force`: the one case of the watermark
suite that has to bootstrap a real repository, twice.

Split out of `test_id_watermark.py` so the rest of that suite, which calls the
watermark rules in-process, stays in the per-commit smoke tier while this case
runs at slice/phase close and in CI. It is registered in `tests/conftest.py`'s
`SLOW_MODULES`: two full `bootstrap.py` subprocesses per run made it the single
most expensive test the tier carried.
"""

from conftest import KIT, load_script, run_py

TRACE = load_script("trace")


def test_force_never_overwrites_a_live_repos_marks(tmp_path):
    # `bootstrap --force` re-lays every scaffold file. For every OTHER target
    # that costs at most re-doing an edit — they are templates to fill, or are
    # regenerable from the tree. The watermark is the only one whose content is
    # HISTORY (which ids were allocated and then deleted), so forcing the
    # fresh-scaffold marks over a live repo frees every id above them and
    # nothing can rebuild what was lost.
    dest = tmp_path / "repo"
    dest.mkdir()
    run_py([KIT / "scripts" / "bootstrap.py", "--dest", str(dest)], cwd=tmp_path)
    mark = dest / TRACE.WATERMARK
    mark.write_text(
        mark.read_text(encoding="utf-8").replace("SR = 0", "SR = 146"),
        encoding="utf-8",
    )
    run_py(
        [KIT / "scripts" / "bootstrap.py", "--dest", str(dest), "--force"],
        cwd=tmp_path,
    )
    assert "SR = 146" in mark.read_text(encoding="utf-8")
