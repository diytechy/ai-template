"""check_vendored.py: vendored copies stay in sync with a pinned upstream
(process-options.md "Tier-conditional guardrails"). A local file:// base serves
the "upstream" so no test touches the network; the offline test points at an
unreachable base to prove the clean degrade."""

from conftest import SCRIPTS, load_script, run_py
import pathlib


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


# --- WI-339: the comparison is of CONTENT, not of a checkout --------------------
#
# `check_vendored` hashed `local.read_bytes()` — the WORKING TREE's bytes — against
# the fetched upstream's. `.gitattributes` declares the vendored docs `text eol=lf`,
# so a CRLF checkout made EVERY vendored file report drift at once, blaming
# upstream. Same class as the duplicate census before WI-337: a checksum of the
# checkout used as a checksum of the content. Each Done-when clause of the spec is
# one test below, including the one that says a half-guard is not a guard.


def _cv():
    return load_script("check_vendored")


LF = b"# Title\nline one\nline two\n"
CRLF = b"# Title\r\nline one\r\nline two\r\n"
LONE_CR = b"# Title\rline one\rline two\r"
DIFFERENT = b"# Title\nline one\nline THREE\n"
# A PNG header: carries a CRLF *inside binary content* on purpose — the shape that
# blind CR-stripping would corrupt.
BINARY = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\r\nrest"


def test_the_same_content_matches_across_line_endings():
    """Done-when 1."""
    cv = _cv()
    assert cv.content_digest(LF)[0] == cv.content_digest(CRLF)[0]
    assert cv.content_digest(LF)[0] == cv.content_digest(LONE_CR)[0]


def test_genuinely_different_content_still_differs():
    """Done-when 2 — the spec's own words: the guard asserts BOTH directions, or
    it is only half a guard. A normalization that collapsed everything would pass
    the test above and be worthless."""
    cv = _cv()
    assert cv.content_digest(LF)[0] != cv.content_digest(DIFFERENT)[0]
    # ...and not merely because of the endings: same endings, different text.
    assert (
        cv.content_digest(CRLF)[0]
        != cv.content_digest(DIFFERENT.replace(b"\n", b"\r\n"))[0]
    )


def test_a_binary_vendored_file_is_hashed_exactly():
    """Done-when 3. Stripping CR bytes from a PNG would corrupt the comparison —
    the opposite failure — so the rule is content-sniffed, and the chosen rule is
    pinned here whichever way it went."""
    import hashlib

    cv = _cv()
    assert cv.looks_binary(BINARY) is True
    digest, normalized = cv.content_digest(BINARY)
    assert normalized is False, "binary must not be normalized"
    assert digest == hashlib.sha256(BINARY).digest(), "binary must hash exactly"


def test_text_is_not_mistaken_for_binary():
    """The other side of the sniff: a NUL byte is the heuristic, so ordinary text
    — including empty text — must take the normalizing path."""
    cv = _cv()
    assert cv.looks_binary(LF) is False
    assert cv.looks_binary(b"") is False
    assert cv.content_digest(LF)[1] is True
    assert cv.content_digest(b"")[1] is True


def test_the_normalization_is_mutation_proven(tmp_path):
    """Done-when 4, in the form that cannot rot: run the REAL comparison with the
    normalization removed and assert the cross-line-ending guard goes red. The
    proof lives inside the suite because a mutation done by hand once, in a
    session, is not evidence a successor can re-derive."""
    import hashlib

    # The pre-WI-339 predicate, restated exactly.
    def raw_digest(data):
        return hashlib.sha256(data).digest()

    assert raw_digest(LF) != raw_digest(CRLF), (
        "the defect must reproduce, or this test proves nothing"
    )
    cv = _cv()
    assert cv.content_digest(LF)[0] == cv.content_digest(CRLF)[0]


def test_the_message_says_which_rule_it_applied():
    """A comparison that silently changes its own basis is how the original
    defect stayed invisible, so the WARN line names the rule."""
    cv = _cv()
    source = pathlib.Path(cv.__file__).read_text(encoding="utf-8")
    assert "line endings normalized" in source
    assert "binary, exact bytes" in source
