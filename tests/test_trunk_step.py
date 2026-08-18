"""trunk_step.py — the serial trunk step (docs/concurrency-restructure.md §5.1/§5.5).

Exercises both operations of the one deliberately serial actor: compiling
`docs/log.d/*.md` fragments into `docs/log.md` in git-derived merge order (the
validation gate, the all-or-nothing write, the link rebase, the delete, the
idempotent no-op) and the dependency-ordered regen (skip-with-a-notice for an
absent artifact family, loud nonzero on a failing generator).

Every test builds its scaffolding under `tmp_path` — including a REAL git repo,
because merge order is *derived* from history rather than asserted, so a fake
would test the wrong thing. The real `docs/` is never written.
"""

import subprocess

from conftest import load_script

ts = load_script("trunk_step")

SEED_LOG = "# Log\n\n## Seed entry\n\n- the log existed before any fragment.\n"


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    """Commit everything staged/untracked, optionally at an EXACT timestamp.

    `when` (a unix-seconds int) pins author+committer date: git records whole
    seconds, so two commits made back-to-back in a test tie — and a tie would
    silently fall through to the filename tie-break, hiding whether the ordering
    under test is really history-derived."""
    import os

    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)  # git's raw date format
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(
        root,
        "-c",
        "user.email=t@t",
        "-c",
        "user.name=t",
        "commit",
        "-qm",
        message,
        env=env,
    )


def repo(tmp_path):
    """A committed git repo carrying `docs/log.md` and an empty `docs/log.d/`
    (its `.gitkeep` marker included, exactly as bootstrap scaffolds it)."""
    (tmp_path / "docs" / "log.d").mkdir(parents=True)
    (tmp_path / "docs" / "log.md").write_text(SEED_LOG, encoding="utf-8")
    (tmp_path / "docs" / "log.d" / ".gitkeep").write_text("", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _commit(tmp_path, "seed", when=1_000_000)
    return tmp_path


def fragment(root, name, text, when=None):
    path = root / "docs" / "log.d" / name
    path.write_text(text, encoding="utf-8")
    if when is not None:
        _commit(root, "add " + name, when=when)
    return path


def log_text(root):
    return (root / "docs" / "log.md").read_text(encoding="utf-8")


def test_no_fragments_is_a_clean_idempotent_noop(tmp_path, capsys):
    # The steady state of a quiet trunk: the step runs on every merge, so the
    # empty case must be cheap, silent-ish and green — never a "nothing to do"
    # nonzero that would red the lane for doing its job.
    root = repo(tmp_path)
    assert ts.compile_log(root) == 0
    assert "0 fragments" in capsys.readouterr().out
    assert log_text(root) == SEED_LOG


def test_fragments_compile_in_git_order_and_are_deleted(tmp_path):
    # The heart of §5.1: merge order is DERIVED from history, not asserted. The
    # names are deliberately anti-sorted against the commit order, so a
    # filename-sorted implementation would fail this test.
    root = repo(tmp_path)
    fragment(root, "WI-2-second.md", "## WI-2 — landed first\n", when=1_000_100)
    fragment(root, "WI-1-first.md", "## WI-1 — landed second\n", when=1_000_200)

    assert ts.compile_log(root) == 0

    text = log_text(root)
    assert text.startswith(SEED_LOG)
    assert text.index("WI-2 — landed first") < text.index("WI-1 — landed second")
    # Compiled fragments leave the drop-box; the scaffold marker stays.
    assert ts.fragment_paths(root) == []
    assert (root / "docs" / "log.d" / ".gitkeep").exists()


def test_second_run_is_idempotent(tmp_path):
    # §5.5's idempotence rule: re-running after a successful compile must not
    # duplicate an entry — the fragments are gone, so there is nothing to append.
    root = repo(tmp_path)
    fragment(root, "WI-3-once.md", "## WI-3 — exactly once\n", when=1_000_100)
    assert ts.compile_log(root) == 0
    after_first = log_text(root)
    assert ts.compile_log(root) == 0
    assert log_text(root) == after_first
    assert after_first.count("WI-3 — exactly once") == 1


def test_relative_links_are_rebased_out_of_log_d(tmp_path):
    # A fragment is authored in docs/log.d/ and lands in docs/log.md one
    # directory up. Only the targets whose meaning DEPENDS on the holding
    # directory move; an anchor, a URL and a root-absolute path are untouched,
    # and a #fragment on a rebased target survives.
    root = repo(tmp_path)
    fragment(
        root,
        "WI-4-links.md",
        "## WI-4 — links\n\n"
        "- spec [WI-9](../work/queued/WI-9-x.md)\n"
        "- deep [anchored](../work/queued/WI-9-x.md#done-when)\n"
        "- self [anchor](#wi-4-links)\n"
        "- out [site](https://example.com/a)\n"
        "- abs [rooted](/docs/status.md)\n",
        when=1_000_100,
    )
    assert ts.compile_log(root) == 0

    text = log_text(root)
    assert "](work/queued/WI-9-x.md)" in text
    assert "](work/queued/WI-9-x.md#done-when)" in text
    assert "](#wi-4-links)" in text
    assert "](https://example.com/a)" in text
    assert "](/docs/status.md)" in text
    assert "](../work/" not in text


def test_uncommitted_fragment_is_a_loud_error(tmp_path, capsys):
    # The step is trunk bookkeeping over COMMITTED state: an uncommitted file has
    # no merge position, so ordering it would be inventing one. Loud, named, and
    # the log is untouched.
    root = repo(tmp_path)
    fragment(root, "WI-5-untracked.md", "## WI-5 — not yet committed\n")
    assert ts.compile_log(root) == 1
    err = capsys.readouterr().err
    assert "WI-5-untracked.md" in err and "uncommitted" in err
    assert log_text(root) == SEED_LOG
    assert (root / "docs" / "log.d" / "WI-5-untracked.md").exists()


def test_a_merge_staged_fragment_compiles_from_merge_head_history(tmp_path, capsys):
    # The integrator folds the trunk step into the merge commit (--no-ff
    # --no-commit), so a branch's fragment is staged but its adding commit is
    # not yet reachable from HEAD - it lives on MERGE_HEAD. The committed-state
    # rule widens to exactly that case and no further.
    root = repo(tmp_path)
    _git(root, "branch", "-m", "main")
    _git(root, "checkout", "-q", "-b", "work")
    fragment(root, "WI-7-branch-work.md", "## WI-7 - branch work\n", when=1_000_100)
    _git(root, "checkout", "-q", "main")
    (root / "trunk-file.txt").write_text("trunk moved\n", encoding="utf-8")
    _commit(root, "trunk moves on", when=1_000_200)
    _git(root, "merge", "--no-ff", "--no-commit", "work")
    assert ts.compile_log(root) == 0, capsys.readouterr().err
    assert "WI-7 - branch work" in log_text(root)
    assert not (root / "docs" / "log.d" / "WI-7-branch-work.md").exists()


def test_missing_heading_is_rejected(tmp_path, capsys):
    # The fragment carries the narrative AND its own `## ` heading — the log
    # append is verbatim, so a heading-less fragment would fuse into whatever
    # section preceded it.
    root = repo(tmp_path)
    fragment(root, "WI-6-noheading.md", "just a paragraph\n", when=1_000_100)
    assert ts.compile_log(root) == 1
    err = capsys.readouterr().err
    assert "WI-6-noheading.md" in err and "`## ` heading" in err
    assert log_text(root) == SEED_LOG


def test_reserved_section_headings_are_rejected(tmp_path, capsys):
    # docs/log.md's three structural sections (pinned by test_bootstrap) are not
    # a work branch's to re-open: a fragment claiming one would append a SECOND
    # "## Audit log" and split the surface readers grep.
    root = repo(tmp_path)
    for i, heading in enumerate(ts.RESERVED_HEADINGS):
        fragment(
            root,
            "WI-7{}-reserved.md".format(i),
            heading + "\n\n- narrative\n",
            when=1_000_100 + i,
        )
        assert ts.compile_log(root) == 1
        err = capsys.readouterr().err
        assert "reserved log section heading" in err and heading in err
        assert log_text(root) == SEED_LOG
        (root / "docs" / "log.d" / "WI-7{}-reserved.md".format(i)).unlink()
        _commit(root, "drop the bad fragment", when=1_000_150 + i)


def test_one_bad_fragment_blocks_the_whole_batch(tmp_path, capsys):
    # All-or-nothing: validation runs over EVERY fragment before the first
    # append, so a half-compiled log — some fragments folded in, some still on
    # disk, no record of which — is structurally impossible.
    root = repo(tmp_path)
    fragment(root, "WI-8-good.md", "## WI-8 — perfectly fine\n", when=1_000_100)
    fragment(root, "not a fragment.md", "## WI-9 — badly named\n", when=1_000_200)
    assert ts.compile_log(root) == 1
    assert "not a fragment.md" in capsys.readouterr().err
    assert log_text(root) == SEED_LOG
    assert len(ts.fragment_paths(root)) == 2


def test_dry_run_plans_both_operations_without_writing(tmp_path, capsys):
    # No operation flag = the whole step (compile, then regen); --dry-run prints
    # the plan and touches nothing, so the order is inspectable before it runs.
    root = repo(tmp_path)
    fragment(root, "WI-10-planned.md", "## WI-10 — planned\n", when=1_000_100)
    assert ts.main(["--root", str(root), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "would append 1 fragment(s)" in out and "WI-10-planned.md" in out
    assert "regen" in out
    assert log_text(root) == SEED_LOG
    assert len(ts.fragment_paths(root)) == 1


def test_regen_skips_absent_artifact_families(tmp_path, capsys):
    # A repo that carries none of the generated surfaces pays nothing — and the
    # skip is PRINTED, so "nothing regenerated" is never mistaken for "all fresh".
    assert ts.regen(tmp_path) == 0
    out = capsys.readouterr().out
    for name in (
        "arch-map",
        "okf",
        "derived-gate",
        "trajectory",
        "status",
        "open-items",
    ):
        assert "skipping {}".format(name) in out


def test_regen_fails_loudly_on_a_broken_generator(tmp_path, capsys):
    # The §5.5 fail-loud contract on the regen half: a red generator stops the
    # step at that step (a later one may read its output), exits nonzero, and
    # prints the child's own diagnosis rather than summarizing it away.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "architecture.md").write_text("# Arch\n", encoding="utf-8")
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n", encoding="utf-8"
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "broken.py").write_text("def (:\n", encoding="utf-8")

    assert ts.regen(tmp_path) == 1
    err = capsys.readouterr().err
    assert "regen FAILED at arch-map" in err
    assert "trunk lane is RED" in err


def test_regen_runs_in_declared_dependency_order(tmp_path, capsys):
    # SR-173: a producer runs before every consumer that reads it — arch-map
    # before okf (the Knowledge bundle bakes the map), derived-gate before
    # trajectory and status (both read docs/gate), open-items last (nothing
    # reads it back). Asserted on the EXECUTED surface (the printed per-step
    # lines of a real run), not on the REGEN_STEPS table, so a reorder of the
    # table shows up here even though every family skips.
    assert ts.regen(tmp_path) == 0
    out = capsys.readouterr().out
    pos = [
        out.index("skipping {}".format(name))
        for name in (
            "arch-map",
            "okf",
            "derived-gate",
            "trajectory",
            "status",
            "open-items",
        )
    ]
    assert pos == sorted(pos), "regen must execute in declared dependency order"


def test_regen_failure_after_green_steps_commits_nothing(tmp_path, capsys):
    # Round-2 F9 pin — the failure half of the SR-173 no-partial-set claim,
    # EXECUTED rather than inferred from the green path: an earlier step runs
    # green and dirties the tree, then a MID-RUN step fails — the run exits
    # nonzero, HEAD has not moved, the green step's output is still sitting
    # uncommitted in the working tree, and the steps AFTER the failure never
    # ran at all.
    #
    # THE FAILURE IS PLANTED MID-LIST, DELIBERATELY (2026-08-17 desk round,
    # F14). The first version planted it in `open-items`, which is the LAST
    # entry of REGEN_STEPS — so "a later step fails" was vacuous and the early
    # `return 1` skipped nothing observable. A mutation making regen carry on
    # past a failure (`_rc = 1; continue`) left this test green, i.e. the
    # documented invariant that protects downstream generators from a RED
    # upstream was pinned nowhere. Here `derived-gate` (step 3 of 6) fails
    # while `open-items` (step 6) is APPLICABLE and would run green if reached,
    # so the stop-at-first-failure contract is what the assertions turn on.
    _git(tmp_path, "init", "-q")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "architecture.md").write_text(
        "# Arch\n\n<!-- BEGIN GENERATED MODULE MAP -->\n"
        "<!-- END GENERATED MODULE MAP -->\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n", encoding="utf-8"
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "ok.py").write_text(
        '"""A fine module."""\n\n\ndef fine():\n    return 1\n', encoding="utf-8"
    )
    (tmp_path / "docs" / "gate").write_text("DevBar-Reqs\n", encoding="utf-8")
    (tmp_path / "docs" / "requirements").mkdir()
    # The mid-list failure: `derive_gate.py` cannot parse its own spine.
    (tmp_path / "docs" / "requirements" / "system-requirements.toml").write_text(
        "this = is not [ valid toml\n", encoding="utf-8"
    )
    # ...and a LATER step that is applicable and would succeed, so "it never
    # ran" is a real observation rather than a step that was skipped anyway.
    (tmp_path / "docs" / "requirements" / "open-items.toml").write_text(
        '[open_item.OI-001]\ntitle = "t"\n', encoding="utf-8"
    )
    _commit(tmp_path, "seed")
    head_before = _git(tmp_path, "rev-parse", "HEAD").strip()

    assert ts.regen(tmp_path) == 1
    captured = capsys.readouterr()
    assert "regen — arch-map ok" in captured.out, "a green step must precede"
    assert "regen FAILED at derived-gate" in captured.err
    # THE CONTINUATION ASSERTION — the one the last-step placement could not
    # make. `open-items` applies, so had regen carried on it would have printed
    # either an `ok` or a `FAILED at open-items`; neither may appear, and it
    # must not even have been announced as skipped.
    assert "open-items" not in captured.out + captured.err, captured.out + captured.err
    assert _git(tmp_path, "rev-parse", "HEAD").strip() == head_before, (
        "a mid-run failure must never leave a partially regenerated set in history"
    )
    assert _git(tmp_path, "status", "--porcelain").strip(), (
        "the green steps' output must still be uncommitted in the tree"
    )


def test_regen_never_commits_the_caller_owns_the_commit(tmp_path):
    # SR-173: no partially regenerated set is ever left COMMITTED, because the
    # regen itself never commits at all — a green step's output stays in the
    # working tree for the caller's one serial commit, so a later step's failure
    # cannot strand half a set in history. Here arch-map runs green (real
    # markers, valid source) and every other family skips: HEAD must not move,
    # and the regenerated doc must sit uncommitted in the tree.
    _git(tmp_path, "init", "-q")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "architecture.md").write_text(
        "# Arch\n\n<!-- BEGIN GENERATED MODULE MAP -->\n"
        "<!-- END GENERATED MODULE MAP -->\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n", encoding="utf-8"
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "ok.py").write_text(
        '"""A fine module."""\n\n\ndef fine():\n    return 1\n', encoding="utf-8"
    )
    _commit(tmp_path, "seed")
    head_before = _git(tmp_path, "rev-parse", "HEAD").strip()

    assert ts.regen(tmp_path) == 0
    assert _git(tmp_path, "rev-parse", "HEAD").strip() == head_before
    assert _git(tmp_path, "status", "--porcelain").strip(), (
        "the green step's output must be left in the working tree "
        "for the caller's serial commit"
    )
