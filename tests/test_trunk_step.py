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

from conftest import load_script, pin_autocrlf

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
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
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
        "okf",
        "derived-stage",
        "trajectory",
        "status",
        "open-items",
    ):
        assert "skipping {}".format(name) in out


def test_regen_fails_loudly_on_a_broken_generator(tmp_path, capsys):
    # The §5.5 fail-loud contract on the regen half: a red generator stops the
    # step at that step (a later one may read its output), exits nonzero, and
    # prints the child's own diagnosis rather than summarizing it away.
    # The okf family arms on docs/okf/ presence; a registry the generator
    # cannot parse makes the regen fail loudly at that step.
    (tmp_path / "docs" / "okf").mkdir(parents=True)
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "system-requirements.toml").write_text(
        "[system_requirement.SR-001]\nthis is not TOML =\n", encoding="utf-8"
    )

    assert ts.regen(tmp_path) == 1
    err = capsys.readouterr().err
    assert "regen FAILED at okf" in err
    assert "trunk lane is RED" in err


def test_regen_runs_in_declared_dependency_order(tmp_path, capsys):
    # SR-173: a producer runs before every consumer that reads it — okf first
    # (the dashboard's Knowledge tab reads the BUNDLE), derived-stage before
    # trajectory and status (both read docs/stage), open-items last (nothing
    # reads it back). Asserted on the EXECUTED surface (the printed per-step
    # lines of a real run), not on the REGEN_STEPS table, so a reorder of the
    # table shows up here even though every family skips.
    #
    # `arch-map` LED this list until WI-455 retired it: the module map derives
    # live from the source AST, so there is no committed block to regenerate
    # and no producer edge into okf left to assert.
    assert ts.regen(tmp_path) == 0
    out = capsys.readouterr().out
    pos = [
        out.index("skipping {}".format(name))
        for name in (
            "okf",
            "derived-stage",
            "trajectory",
            "status",
            "open-items",
        )
    ]
    assert pos == sorted(pos), "regen must execute in declared dependency order"


def test_regen_really_writes_the_verdict_rollup(tmp_path, capsys):
    # SR-170's exclusive-writer clause, DRIVEN through the writer it names.
    # LLR-208 says the rollup is "regenerated by the trunk step" and TC-206 that
    # "the serial merge step runs" the regenerator — and that pairing is the whole
    # contract: a work branch commits the round files but stands the rollup step
    # down, so if the trunk step does not run this generator, the artifact is
    # written by nobody and the freshness gate is a permanent red.
    #
    # WHY IT IS DRIVEN AND NOT READ OFF THE TABLE (WI-588). Deleting the entire
    # `verdict-rollup` row from REGEN_STEPS leaves this module syntactically
    # valid, with zero `verdict-rollup` occurrences in it — and TC-206's four
    # cited evidence nodes plus the whole of this file passed under that
    # mutation. They could not catch it: the generator's own test CALLS the
    # generator, the wiring guards check the `[generated]` declaration and the
    # check.py step, and the stand-down set is about the branch. None of them
    # asks whether the trunk step regenerates it, so the answer here has to come
    # from `regen()` writing the file and from nothing else.
    #
    # `docs/reviews/` is the only armed family in this fixture, so exactly one
    # generator runs and the arm stays as cheap as the skip tests above it.
    scope = tmp_path / "docs" / "reviews" / "wi-401-lane"
    scope.mkdir(parents=True)
    (scope / "001-REVIEW-A-abc1234.md").write_text(
        "# Review A\n\nModel: test/reviewer\n\nVERDICT: APPROVE findings=0\n",
        encoding="utf-8",
        newline="\n",
    )
    rollup = tmp_path / "docs" / "reviews" / "rollup" / "wi-401-lane.md"
    assert not rollup.exists(), "the fixture must not pre-write what regen writes"

    assert ts.regen(tmp_path) == 0, capsys.readouterr().err
    captured = capsys.readouterr()
    assert "regen — verdict-rollup ok" in captured.out, captured.out + captured.err
    assert rollup.exists(), (
        "the trunk step ran without regenerating the rollup: "
        + captured.out
        + captured.err
    )
    # The row it wrote is the round file's, so this is the real generator's real
    # output and not an empty file that happens to exist.
    assert "001-REVIEW-A-abc1234.md" in rollup.read_text(encoding="utf-8")


def _seed_regen_repo(root):
    """A git repo where `okf` regenerates green AND EMITS: the `docs/okf/`
    arming directory plus a minimal but non-vacuous four-tier spine (the
    bundle's vacuity gate emits nothing for a placeholder-only registry, so a
    thinner spine would leave the tree clean and the dirtiness assertions
    below vacuous). `open-items` is armed too, as the later applicable family."""
    _git(root, "init", "-q")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    (root / "docs" / "okf").mkdir(parents=True)
    (root / "docs" / "requirements").mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    reqs = root / "docs" / "requirements"
    (reqs / "stakeholder-needs.toml").write_text(
        '[need.SN-001]\ntitle = "n"\nstatus = "Drafted"\n', encoding="utf-8"
    )
    (reqs / "system-requirements.toml").write_text(
        '[system_requirement.SR-001]\ntitle = "t"\nstatus = "Drafted"\n',
        encoding="utf-8",
    )
    (reqs / "low-level-requirements.toml").write_text(
        '[design.LLR-001]\ntitle = "l"\nstatus = "Drafted"\nsr_refs = ["SR-001"]\n',
        encoding="utf-8",
    )
    (root / "docs" / "test" / "test-cases.toml").write_text(
        '[test_case.TC-001]\ntitle = "tc"\nstatus = "Drafted"\nverifies = ["SR-001"]\n',
        encoding="utf-8",
    )
    (reqs / "open-items.toml").write_text(
        '[open_item.OI-001]\ntitle = "t"\n', encoding="utf-8"
    )


def test_regen_failure_after_green_steps_commits_nothing(tmp_path, capsys):
    # Round-2 F9 pin — the failure half of the SR-173 no-partial-set claim,
    # EXECUTED rather than inferred from the green path: an earlier step runs
    # green and dirties the tree, then a MID-RUN step fails — the run exits
    # nonzero, HEAD has not moved, the green step's output is still sitting
    # uncommitted in the working tree, and the steps AFTER the failure never
    # ran at all.
    #
    # THE FAILURE IS PLANTED MID-LIST, DELIBERATELY (2026-08-17 desk round,
    # F14). A failure planted in the LAST entry makes "a later step fails"
    # vacuous — the early `return 1` would skip nothing observable, and a
    # mutation making regen carry on (`_rc = 1; continue`) would leave this
    # test green. Here `derived-stage` (step 2 of 5) fails while `open-items`
    # (step 5) is APPLICABLE and would run green if reached, so the
    # stop-at-first-failure contract is what the assertions turn on.
    #
    # WHY THE FAILURE IS AN UNWRITABLE OUTPUT (WI-455): the green step used to
    # be `arch-map` and the mid-list failure a registry the deriver could not
    # parse. `arch-map` retired, which makes `okf` step 1 — and `okf` reads
    # every registry, so a malformed-registry failure now lands FIRST, with no
    # green step before it. Occupying the output path is the remaining way to
    # fail a generator strictly after a green one; the contract under test is
    # unchanged.
    _seed_regen_repo(tmp_path)
    _commit(tmp_path, "seed")
    head_before = _git(tmp_path, "rev-parse", "HEAD").strip()
    # `docs/stage` EXISTS (so the family arms) but cannot be written. It was
    # `docs/gate` until WI-498 slice 5 retired that file and its regen step; the
    # successor occupies the same position in the list, so the mid-list
    # placement this test turns on is unchanged.
    (tmp_path / "docs" / "stage").mkdir()

    assert ts.regen(tmp_path) == 1
    captured = capsys.readouterr()
    assert "regen — okf ok" in captured.out, "a green step must precede"
    assert "regen FAILED at derived-stage" in captured.err
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
    # cannot strand half a set in history. Here the generators run green over a
    # real spine: HEAD must not move, and their output must sit uncommitted in
    # the tree.
    _seed_regen_repo(tmp_path)
    _commit(tmp_path, "seed")
    head_before = _git(tmp_path, "rev-parse", "HEAD").strip()

    assert ts.regen(tmp_path) == 0
    assert _git(tmp_path, "rev-parse", "HEAD").strip() == head_before
    assert _git(tmp_path, "status", "--porcelain").strip(), (
        "the green step's output must be left in the working tree "
        "for the caller's serial commit"
    )


def test_the_directorys_readme_is_its_declaration_home_not_a_fragment(tmp_path):
    # OI-67 slice 4: `docs/log.d/` owns an interface row (the fragment grammar
    # trunk_step consumes), and a directory owner declares through its
    # README.md. A README is not a session fragment: it is neither compiled
    # into the log nor refused for its name — the one file the drop-box keeps
    # beside `.gitkeep`. Any OTHER badly named file still refuses the whole
    # compile, so the exemption is by name, not by shape.
    root = repo(tmp_path)
    fragment(
        root,
        "README.md",
        "<!--\nContracts: IF-156\n\nContract IF-156: one fragment per session.\n-->\n"
        "# The log drop-box\n",
        when=1_000_050,
    )
    fragment(root, "WI-11-real.md", "## WI-11 — a real fragment\n", when=1_000_100)
    assert [p.name for p in ts.fragment_paths(root)] == ["WI-11-real.md"]
    assert ts.compile_log(root) == 0
    assert "WI-11 — a real fragment" in log_text(root)
    assert "The log drop-box" not in log_text(root)
    assert (root / "docs" / "log.d" / "README.md").exists()
    assert ts.fragment_paths(root) == []
