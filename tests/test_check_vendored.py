"""check_vendored.py: vendored copies stay in sync with a pinned upstream
(process-options.md "Tier-conditional guardrails"). A local file:// base serves
the "upstream" so no test touches the network; the offline test points at an
unreachable base to prove the clean degrade."""

from conftest import SCRIPTS, run_py


def _vendor(tmp_path, upstream_body, local_body):
    """A repo with one vendored file + an UPSTREAM manifest whose base is a
    file:// URL for a local upstream dir. Returns (repo, local_file)."""
    up = tmp_path / "upstream"
    up.mkdir()
    (up / "CLAUDE.md").write_text(upstream_body, encoding="utf-8")
    repo = tmp_path / "repo"
    g = repo / "docs" / "guardrails"
    g.mkdir(parents=True)
    local = g / "core.md"
    local.write_text(local_body, encoding="utf-8")
    (g / "UPSTREAM").write_text(
        "# pinned upstream\nbase = {}\ndocs/guardrails/core.md = CLAUDE.md\n".format(
            up.as_uri()
        ),
        encoding="utf-8",
    )
    return repo, local


def test_matching_copy_is_ok(tmp_path):
    repo, _ = _vendor(tmp_path, "core content\n", "core content\n")
    proc = run_py([SCRIPTS / "check_vendored.py", "--root", repo], cwd=repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_drift_warns_and_strict_fails(tmp_path):
    repo, local = _vendor(tmp_path, "core content\n", "core content\n")
    local.write_text("locally tampered\n", encoding="utf-8")
    warn = run_py([SCRIPTS / "check_vendored.py", "--root", repo], cwd=repo)
    assert warn.returncode == 0, warn.stdout + warn.stderr  # warn-only
    assert "WARN" in warn.stdout and "differs" in warn.stdout
    strict = run_py(
        [SCRIPTS / "check_vendored.py", "--root", repo, "--strict"], cwd=repo
    )
    assert strict.returncode == 1
    assert "FAIL" in strict.stdout


def test_offline_degrades_to_skip(tmp_path):
    # An unreachable base must skip (exit 0), not fail — no egress in CI.
    repo = tmp_path / "repo"
    g = repo / "docs" / "guardrails"
    g.mkdir(parents=True)
    (g / "core.md").write_text("x\n", encoding="utf-8")
    (g / "UPSTREAM").write_text(
        "base = http://127.0.0.1:9/nope\ndocs/guardrails/core.md = CLAUDE.md\n",
        encoding="utf-8",
    )
    proc = run_py(
        [SCRIPTS / "check_vendored.py", "--root", repo, "--timeout", "1"], cwd=repo
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipped" in proc.stdout


def test_missing_vendored_file_warns(tmp_path):
    repo = tmp_path / "repo"
    g = repo / "docs" / "guardrails"
    g.mkdir(parents=True)
    (g / "UPSTREAM").write_text(
        "base = {}\ndocs/guardrails/core.md = CLAUDE.md\n".format(tmp_path.as_uri()),
        encoding="utf-8",
    )
    proc = run_py([SCRIPTS / "check_vendored.py", "--root", repo], cwd=repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "missing" in proc.stdout


def test_no_manifest_is_a_noop(tmp_path):
    proc = run_py([SCRIPTS / "check_vendored.py", "--root", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing vendored" in proc.stdout
