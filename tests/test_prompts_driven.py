"""The shipped prompt templates reach a bootstrapped scaffold and load there.

Split out of `test_prompts.py`, whose slot-filling, preflight and catalogue
cases run in-process and stay in the per-commit smoke tier. This case runs a
full `bootstrap.py` subprocess, so it is registered in `tests/conftest.py`'s
`SLOW_MODULES` and runs at slice/phase close and in CI.
"""

from conftest import SCRIPTS, load_script, run_py

pr = load_script("prompts")


def test_a_scaffold_gets_every_template_and_loads_them_from_there(tmp_path):
    """The `prompts/` declared-absence says this repo's own home is
    project-trajectory/prompts/ and the SCAFFOLD destination is <repo>/prompts/.
    That promise is worth exactly as much as this test: bootstrap a real
    scaffold, point the loader at it, and load every key."""
    dest = tmp_path / "repo"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    scaffolded = dest / "prompts"
    assert (scaffolded / "README.md").is_file()
    for filename in pr.KIT_PROMPTS.values():
        assert (scaffolded / filename).is_file(), filename

    # And the loader resolves them from a scaffold's layout, where scripts/ is
    # at the repo root so KIT is the repo root itself.
    scaffold_pr = load_script("prompts")
    scaffold_pr.PROMPTS = scaffolded
    assert scaffold_pr.preflight() == []
    assert scaffold_pr.load(scaffold_pr.WORKER) == pr.load(pr.WORKER)
