"""The coordinator's codex call, in process (`scripts/coordinator/codex_call.py`,
this repository's own tooling): the role's route and launch template, the
change check's judge and the resumed turn's carrier walk.

The judge and the walk are pure functions, driven here over hand-built
snapshots, ranges and log texts; the real-repository cases, with a stand-in
`codex` process, are in `test_codex_call_git.py`.
"""

from pathlib import Path

import agent_session
import pytest
from conftest import claimed_lane, fixture_git

import codex_call_fixtures as fx

cc = fx.load_codex_call()


HEX = "0123456789abcdef0123456789abcdef"
CALL_LOG = "docs/iteration/call_{}-20261022-101010.log".format(HEX)
OTHER_CALL_LOG = "docs/iteration/call_{}-20261022-111111.log".format(HEX[::-1])
GATE_LOG = "docs/iteration/001-20261022-101010.log"
A, B, C = "a" * 40, "b" * 40, "c" * 40
SOL_ROLES = ("REVIEW-A", "CRITIQUE")


def snap(head=A, **paths):
    return cc.Snapshot(head, dict(paths))


def snap_of(head, paths):
    return cc.Snapshot(head, dict(paths))


def commit(*changes, parents=(A,)):
    return cc.Commit(B, tuple(parents), tuple(changes))


def span(*commits, descendant=True):
    return cc.Span(descendant, tuple(commits))


def judged(role, before, after, rng=None):
    return cc.judge_changes(role, before, after, rng or span()).state


# --- the role's route and launch -------------------------------------------------


def _prompt(tmp_path):
    path = tmp_path / "prompt.md"
    path.write_text("review the lane", encoding="utf-8")
    return path


def test_each_role_launches_its_enabled_roster_row(tmp_path, capsys):
    """Adequacy witness: an entry point that launched one fixed model, or
    that read a disabled row off the registry, gives the wrong row here."""
    root = fx.write_route_files(tmp_path / "root")
    expected = {
        "REVIEW-A": ("OPENAI-SOL", fx.SOL_MODEL, "strong"),
        "CRITIQUE": ("OPENAI-SOL", fx.SOL_MODEL, "strong"),
        "AUTHOR": ("OPENAI-TERRA", fx.TERRA_MODEL, "medium"),
    }
    for role, (route, model, tier) in expected.items():
        launch, why = cc.resolve_role(root, role)
        assert why is None, role
        assert (launch.route_id, launch.model, launch.tier, launch.provider) == (
            route,
            model,
            tier,
            "OPENAI",
        ), role
    for entry in ("OPENAI-LUNA", "OPENAI-NOPE"):
        launch, why = cc.resolve_role(root, "REVIEW-A", entry=entry)
        assert launch is None and entry in why
    launch, why = cc.resolve_role(root, "BUILD")
    assert launch is None and why
    prompt, out = _prompt(tmp_path), tmp_path / "out.md"
    common = ["--root", root, "--prompt-file", prompt, "--out", out]
    assert cc.main(["REVIEW-A", *map(str, common), "--route", "OPENAI-LUNA"]) == 2
    assert cc.main(["BUILD", *map(str, common)]) == 2
    assert cc.main(["REVIEW-A", "--resume", *map(str, common)]) == 2
    assert not out.exists()


def _c_values(argv):
    return [argv[i + 1] for i, tok in enumerate(argv) if tok == "-c"]


def test_the_launch_keeps_the_wrappers_sandbox(tmp_path):
    """Adequacy witness: a launch on the roster row's own template (which
    bypasses the sandbox) or with the scratch root taken from the script's
    own location fails here."""
    lane = claimed_lane(tmp_path, files=fx.route_files())
    scratch = (tmp_path / "primary.wt" / "review-tmp").resolve()
    launch, why = cc.resolve_role(lane, "REVIEW-A", effort="high")
    assert why is None and launch.template
    argv, stdin = agent_session.build_argv(launch.template, launch.model, "PROMPT")
    assert argv[:2] == ["codex", "exec"]
    values = _c_values(argv)
    assert "model_reasoning_effort=high" in values
    assert "windows.sandbox=unelevated" in values
    assert "sandbox_mode=workspace-write" in values
    roots = [
        v for v in values if v.startswith("sandbox_workspace_write.writable_roots=")
    ]
    assert len(roots) == 1
    written = roots[0].split("=", 1)[1].strip("[]").strip("'\"")
    assert Path(written).resolve() == scratch
    assert "--skip-git-repo-check" in argv
    assert argv[argv.index("--model") + 1] == fx.SOL_MODEL
    assert stdin == "PROMPT"
    assert not any("dangerously" in tok for tok in argv)
    assert "-C" not in argv


# --- the change check's judge ----------------------------------------------------


def test_sol_reads_any_change_but_the_discount_as_an_edit():
    """Adequacy witness: a judge that compared HEAD alone, or that discounted
    every log-shaped name, reads one of these edits as clean."""
    for role in SOL_ROLES:
        assert judged(role, snap(), snap()) == cc.CLEAN
        verdict = cc.judge_changes(role, snap(), snap(**{"work.txt": "h1"}), span())
        assert (verdict.state, verdict.edits) == (cc.EDIT, ("work.txt",))
        assert (
            judged(role, snap(**{"src.py": "h0"}), snap(**{"src.py": "h1"})) == cc.EDIT
        )
        assert judged(role, snap(**{"src.py": "h0"}), snap()) == cc.EDIT
        assert judged(role, snap(), snap_of(A, {CALL_LOG: "h"})) == cc.CLEAN
        assert judged(role, snap(), snap_of(A, {GATE_LOG: "h"})) == cc.EDIT
        outside = "notes/call_{}-20261022-101010.log".format(HEX)
        assert judged(role, snap(), snap_of(A, {outside: "h"})) == cc.EDIT


def test_only_a_commit_adding_standard_call_logs_is_discounted():
    """Adequacy witness: a discount over any commit touching
    `docs/iteration/`, or over a merge, passes one of these edits."""
    moved = snap(B)
    added = ("A", CALL_LOG, "b1")
    for role in (*SOL_ROLES, "AUTHOR"):
        assert judged(role, snap(), moved, span(commit(added))) == cc.CLEAN
        two = span(commit(added), commit(("A", OTHER_CALL_LOG, "b2")))
        assert judged(role, snap(), moved, two) == cc.CLEAN
        for changes in (
            [("A", GATE_LOG, "b1")],
            [("M", CALL_LOG, "b1")],
            [("D", CALL_LOG, "b1")],
            [("A", "src.py", "b1")],
            [added, ("A", "src.py", "b2")],
        ):
            assert judged(role, snap(), moved, span(commit(*changes))) == cc.EDIT
        merge = commit(added, parents=(A, C))
        assert judged(role, snap(), moved, span(merge)) == cc.EDIT


def test_an_uncommitted_call_log_committed_during_the_call_is_discounted_only_unchanged():
    """Adequacy witness: a judge that discounted any vanished call log, or
    did not compare the committed blob with the waiting log's identity,
    passes the modified or deleted variant."""
    before = snap_of(A, {CALL_LOG: "blob1"})
    for role in SOL_ROLES:
        own = span(commit(("A", CALL_LOG, "blob1")))
        assert judged(role, before, snap(B), own) == cc.CLEAN
        changed = span(commit(("A", CALL_LOG, "blob2")))
        assert judged(role, before, snap(B), changed) == cc.EDIT
        assert judged(role, before, snap(A), span()) == cc.EDIT
        assert judged(role, before, snap_of(A, {CALL_LOG: "blob2"}), span()) == cc.EDIT
        mixed = span(commit(("A", CALL_LOG, "blob1"), ("A", "src.py", "b")))
        assert judged(role, before, snap(B), mixed) == cc.EDIT


def test_terra_keeps_uncommitted_output_and_reads_only_an_undiscounted_head_move():
    """Adequacy witness: a judge that applied Sol's rule to Terra reads its
    output as an edit; one that ignored HEAD for Terra misses its commit."""
    assert judged("AUTHOR", snap(), snap(**{"work.txt": "h1"})) == cc.CLEAN
    assert judged("AUTHOR", snap(**{"a.md": "h0"}), snap(**{"a.md": "h1"})) == cc.CLEAN
    discounted = span(commit(("A", CALL_LOG, "b1")))
    assert judged("AUTHOR", snap(), snap(B), discounted) == cc.CLEAN
    work = span(commit(("A", "docs/x.toml", "b1")))
    verdict = cc.judge_changes("AUTHOR", snap(), snap(B), work)
    assert verdict.state == cc.EDIT and "docs/x.toml" in verdict.edits


def test_a_head_that_is_not_a_descendant_is_an_edit():
    """Adequacy witness: a judge that read only the commits listed in the
    range (none, after a rewrite) reads a rewritten history as clean."""
    for role in (*SOL_ROLES, "AUTHOR"):
        assert judged(role, snap(), snap(C), span(descendant=False)) == cc.EDIT


def test_an_unreadable_snapshot_never_reads_clean():
    """Adequacy witness: a judge that treated an unreadable read as empty
    reads these as clean."""
    for role in (*SOL_ROLES, "AUTHOR"):
        assert judged(role, cc.Snapshot(None, {}), snap()) == cc.UNABLE
        assert judged(role, snap(), cc.Snapshot(A, None)) == cc.UNABLE
        assert judged(role, snap(), snap(B), cc.Span(None, ())) == cc.UNABLE
        assert judged(role, snap(), snap(B), cc.Span(True, None)) == cc.UNABLE
        work = span(commit(("A", "src.py", "b")))
        assert judged(role, cc.Snapshot(None, {}), snap(B), work) == cc.UNABLE


def test_an_index_only_change_is_an_edit_for_sol_and_output_for_terra():
    """A path whose file on disk is unchanged while its index entry changed
    (staged, unstaged, or staged with other content) is an edit for Sol and
    uncommitted output for Terra; an unreadable index reading never reads
    clean. Adequacy witness: a judge that compared only the files on disk
    reads every Sol case here as clean."""
    disk = {"work.txt": "h1"}
    tracked = frozenset(disk)
    unstaged = cc.Snapshot(A, disk, tracked, {"work.txt": " M " + "0" * 40})
    for index in ("M  h1", "MM h0"):
        staged = cc.Snapshot(A, disk, tracked, {"work.txt": index})
        for before, after in ((unstaged, staged), (staged, unstaged)):
            for role in SOL_ROLES:
                verdict = cc.judge_changes(role, before, after, span())
                assert (verdict.state, verdict.edits) == (cc.EDIT, ("work.txt",))
            assert judged("AUTHOR", before, after) == cc.CLEAN
    assert judged("REVIEW-A", unstaged, unstaged) == cc.CLEAN
    blind = cc.Snapshot(A, disk, tracked, None)
    for role in (*SOL_ROLES, "AUTHOR"):
        assert judged(role, unstaged, blind) == cc.UNABLE


def test_an_interrupted_call_is_recorded_as_the_service_records_it(
    tmp_path, monkeypatch
):
    """A Ctrl-C during the launch: the entry point lets it propagate, and the
    call's log is still written and committed in the lane, recorded
    INTERRUPTED, as the service's own act-then-record records one.
    Adequacy witness: an act-then-record of the entry point's own that
    caught only `Exception` leaves no log here."""
    lane = claimed_lane(tmp_path, files=fx.route_files())

    def interrupted(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(cc.session_service, "_launch", interrupted)
    prompt, out = _prompt(tmp_path), tmp_path / "out.md"
    argv = ["REVIEW-A", "--root", str(lane), "--prompt-file", str(prompt)]
    with pytest.raises(KeyboardInterrupt):
        cc.main([*argv, "--out", str(out)])
    logs = list((lane / "docs" / "iteration").glob("call_*.log"))
    assert len(logs) == 1
    assert "# outcome: INTERRUPTED" in logs[0].read_text(encoding="utf-8")
    tracked = fixture_git(lane, "ls-files", "--", "docs/iteration")
    assert fx.rel(lane, logs[0]) in tracked.splitlines()


# --- the resumed turn's carrier walk ---------------------------------------------


def _log(tmp_path, **kw):
    """`(repo-relative path, text)` of one standard-call log."""
    iter_dir = tmp_path / "docs" / "iteration"
    path = fx.call_log(iter_dir, **kw)
    return fx.rel(tmp_path, path), path.read_text(encoding="utf-8")


def _walk(committed, uncommitted=None):
    return cc.resume_carrier(committed, uncommitted or {}, {"WI-1"}, "OPENAI-TERRA")


def _bad_carrier(tmp_path, case):
    """`(committed, uncommitted, the paths the refusal must name)` for one
    bad-carrier case, each behind an older valid lane carrier where one
    could be stepped back to."""
    older = _log(tmp_path, stamp="20261022-100000")
    newer = dict(stamp="20261022-110000")
    if case == "no-author-log":
        path, text = _log(tmp_path, role="REVIEW-A", route="OPENAI-SOL", **newer)
        return {path: text}, {}, []
    if case == "unreadable-blob":
        path, _ = _log(tmp_path, **newer)
        return {older[0]: older[1], path: None}, {}, [path]
    path, text = _log(tmp_path, **newer)
    if case == "no-terminator":
        text = fx.cut_before(text, "---")
    elif case.startswith("no-"):
        text = fx.drop_line(text, case[3:])
    elif case == "empty-session-id":
        path, text = _log(tmp_path, session_id="", **newer)
    elif case == "another-route":
        path, text = _log(tmp_path, route="OPENAI-SOL", **newer)
    elif case == "same-stamp":
        twin, twin_text = _log(tmp_path, session_id="T-TWIN", **newer)
        return {older[0]: older[1], path: text, twin: twin_text}, {}, [path, twin]
    elif case == "uncommitted-newer":
        return {older[0]: older[1]}, {path: text}, [path]
    return {older[0]: older[1], path: text}, {}, [path]


BAD_CARRIERS = (
    "no-author-log",
    "unreadable-blob",
    "no-terminator",
    "no-role",
    "no-roster-row",
    "no-wi",
    "no-started-at",
    "empty-session-id",
    "another-route",
    "same-stamp",
    "uncommitted-newer",
)


@pytest.mark.parametrize("case", BAD_CARRIERS)
def test_the_resume_walk_refuses_each_bad_carrier(tmp_path, case):
    """Adequacy witness: a walk that stepped over a log it cannot classify,
    or took the first log whose role reads AUTHOR, continues a thread here."""
    committed, uncommitted, named = _bad_carrier(tmp_path, case)
    carrier = _walk(committed, uncommitted)
    assert carrier.session_id == ""
    assert carrier.refusal
    for path in named:
        assert path in carrier.refusal, path


def test_an_older_valid_carrier_behind_a_newer_damaged_log_is_never_continued(tmp_path):
    """Adequacy witness: a walk that found candidates by content (`# role:
    AUTHOR`) never sees the damaged log and continues the older thread."""
    older = _log(tmp_path, stamp="20261022-100000", session_id="T-OLD")
    path, text = _log(tmp_path, stamp="20261022-110000", session_id="T-NEW")
    cut = fx.cut_before(text, "role")
    for committed, uncommitted in (
        ({older[0]: older[1], path: cut}, {}),
        ({older[0]: older[1]}, {path: cut}),
        ({older[0]: older[1], path: "�\x00garbage\n"}, {}),
    ):
        carrier = _walk(committed, uncommitted)
        assert carrier.session_id == "" and path in carrier.refusal


def test_newer_well_formed_logs_of_other_roles_or_lanes_are_skipped(tmp_path):
    """Adequacy witness: a walk that refused every newer log, or took the
    newest AUTHOR log of any lane, does not continue the lane's own thread."""
    older = _log(tmp_path, stamp="20261022-100000", session_id="T-OLD")
    review = _log(
        tmp_path, role="REVIEW-A", route="OPENAI-SOL", stamp="20261022-110000"
    )
    foreign = _log(tmp_path, wi="WI-2", session_id="T-FOREIGN", stamp="20261022-120000")
    waiting = _log(tmp_path, wi="WI-2", session_id="T-WAIT", stamp="20261022-130000")
    committed = dict((older, review, foreign))
    carrier = _walk(committed, dict((waiting,)))
    assert (carrier.session_id, carrier.path, carrier.refusal) == (
        "T-OLD",
        older[0],
        "",
    )
