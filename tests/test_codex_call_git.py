"""The coordinator's codex call on real repositories
(`scripts/coordinator/codex_call.py`, this repository's own tooling), with a
stand-in `codex` first on PATH (`codex_call_fixtures.stand_in_codex`).

Each case builds a claimed lane (`conftest.claimed_lane`: a primary checkout
and a linked worktree on a branch whose claim is committed) or one of the
roots outside a lane, runs the entry point as a process, and reads what it
left: its exit code and output, the commits, the session logs and the spool.
The stand-in performs the case's git act during the call. Its in-process pin
is `test_codex_call.py`.
"""

import datetime
import os
import stat
import sys
from pathlib import Path

import agent_common
import pytest
from conftest import claimed_lane, fixture_commit, fixture_git, load_script

import codex_call_fixtures as fx

svc = load_script("session_service")


MONDAY_INSIDE = datetime.datetime(2026, 7, 13, 14)  # inside 12:00-19:00 UTC


@pytest.fixture
def standin(tmp_path):
    """`(bindir, records)` of a stand-in `codex` under `tmp_path`."""
    return fx.stand_in_codex(tmp_path / "standin")


def _lane(where):
    return claimed_lane(where, files=fx.route_files())


def _primary(lane):
    return lane.with_name(lane.name[: -len("-lane")])


def _run(tmp_path, standin, role, root, *extra, act="none", arg="", thread=""):
    """One call through the entry point: `(exit code, output, out file)`."""
    prompt = tmp_path / "prompt.md"
    prompt.write_text("judge the lane", encoding="utf-8")
    out = tmp_path / "out-{}.md".format(len(fx.launches(standin[1])))
    env = fx.stand_in_env(*standin, act=act, arg=arg, thread=thread)
    args = [role, "--root", root, "--prompt-file", prompt, "--out", out, *extra]
    code, text = fx.run_call(args, env)
    return code, text, out


def _head(root):
    return fixture_git(root, "rev-parse", "HEAD")


def _state(root):
    """What a call outside a lane must leave unchanged: every ref, HEAD and
    the status."""
    return (
        fixture_git(root, "for-each-ref", "--format=%(refname) %(objectname)"),
        fixture_git(root, "rev-parse", "HEAD"),
        fixture_git(root, "status", "--porcelain", "--untracked-files=all"),
    )


def _tracked_call_logs(root):
    listed = fixture_git(root, "ls-files", "--", "docs/iteration")
    return sorted(p for p in listed.splitlines() if "/call_" in p)


def _untracked(root):
    listed = fixture_git(root, "ls-files", "--others", "--exclude-standard")
    return sorted(listed.splitlines())


def _spooled(root):
    spool = _primary_of(root) / "out" / "sessions" / "spool"
    return sorted(p.name for p in spool.glob("call_*.log")) if spool.is_dir() else []


def _primary_of(root):
    common = fixture_git(
        root, "rev-parse", "--path-format=absolute", "--git-common-dir"
    )
    return Path(common).parent


def _close_on_branch(lane, branch="wi-1", wi="WI-1"):
    """The lane's close-first move: its spec leaves `active/<branch>/` on the
    branch, while trunk still holds it."""
    (lane / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    fixture_git(
        lane,
        "mv",
        "docs/work/active/{}/{}-x.md".format(branch, wi),
        "docs/work/complete/{}-x.md".format(wi),
    )
    fixture_git(lane, "commit", "-q", "--no-verify", "-m", "close " + wi)


def _drop_from_trunk(primary, branch="wi-1", wi="WI-1"):
    fixture_git(primary, "rm", "-q", "docs/work/active/{}/{}-x.md".format(branch, wi))
    fixture_git(primary, "commit", "-q", "--no-verify", "-m", "drop the claim")


def _primary_on_claimed_branch(where):
    """A primary checkout sitting on `wi-2`, whose claim both `wi-2` and trunk
    hold."""
    primary = _primary(_lane(where))
    claim = primary / "docs" / "work" / "active" / "wi-2" / "WI-2-x.md"
    claim.parent.mkdir(parents=True)
    claim.write_text("+++\nid = 'WI-2'\n+++\n", encoding="utf-8", newline="\n")
    fixture_commit(primary, "claim WI-2")
    fixture_git(primary, "checkout", "-q", "-b", "wi-2")
    return primary


# --- a call in a lane ------------------------------------------------------------


def test_a_sol_review_in_a_lane_commits_one_call_log_with_codex_usage(
    tmp_path, standin
):
    """Adequacy witness: a route that left the log uncommitted, recorded no
    usage, or wrote the stream instead of the final text fails here."""
    lane = _lane(tmp_path)
    base = _head(lane)
    code, text, out = _run(tmp_path, standin, "REVIEW-A", lane)
    assert code == 0, text
    assert len(fx.launches(standin[1])) == 1
    assert len(fixture_git(lane, "rev-list", base + "..HEAD").split()) == 1
    assert fixture_git(lane, "log", "-1", "--format=%s").startswith("telemetry:")
    changes = fixture_git(
        lane,
        "diff-tree",
        "--no-commit-id",
        "--name-status",
        "-r",
        "--no-renames",
        "HEAD",
    ).splitlines()
    assert len(changes) == 1 and changes[0].startswith("A\tdocs/iteration/call_")
    meta = agent_common.read_log_meta(lane / changes[0].split("\t", 1)[1])
    assert meta["gen_ai.usage.input_tokens"] == "30378"
    assert meta["gen_ai.usage.output_tokens"] == "47"
    assert (meta["cli"], meta["provider"], meta["roster-row"]) == (
        "codex",
        "OPENAI",
        "OPENAI-SOL",
    )
    assert out.read_text(encoding="utf-8") == fx.FINAL_TEXT


def test_a_committed_work_file_is_an_edit_and_the_log_is_still_recorded(
    tmp_path, standin
):
    """Adequacy witness: a check that compared only the status, or a route
    that skipped the record after an edit, fails here."""
    lane = _lane(tmp_path)
    code, text, _ = _run(tmp_path, standin, "REVIEW-A", lane, act="commit-work")
    assert code == 3, text
    assert "work.txt" in text
    assert len(_tracked_call_logs(lane)) == 1
    assert (lane / "work.txt").is_file()  # nothing is reverted


def test_an_uncommitted_work_file_is_an_edit_for_sol_and_output_for_terra(
    tmp_path, standin
):
    """Adequacy witness: one rule for both roles reads one of them wrong."""
    sol = _lane(tmp_path / "sol")
    code, text, _ = _run(tmp_path, standin, "REVIEW-A", sol, act="leave-work")
    assert code == 3 and "work.txt" in text, text
    terra = _lane(tmp_path / "terra")
    code, text, _ = _run(
        tmp_path, standin, "AUTHOR", terra, "--wi", "WI-1", act="leave-work"
    )
    assert code == 0, text
    assert "work.txt" in _untracked(terra)
    assert len(_tracked_call_logs(terra)) == 1


@pytest.mark.parametrize(
    "role, staged, act, expected",
    [
        ("REVIEW-A", False, "stage", 3),
        ("REVIEW-A", True, "unstage", 3),
        ("AUTHOR", False, "stage", 0),
    ],
)
def test_an_index_only_change_is_an_edit_for_sol_and_output_for_terra(
    tmp_path, standin, role, staged, act, expected
):
    """A work file modified before the call, then only staged (or unstaged)
    by the model: its content on disk is unchanged and its index entry is
    not. For Sol that is an edit, named; for Terra it is uncommitted output.
    Adequacy witness: a check that compared only the files on disk reads the
    Sol cases as clean."""
    lane = _lane(tmp_path)
    (lane / "work.txt").write_text("work\n", encoding="utf-8", newline="\n")
    fixture_commit(lane, "a work file", "work.txt")
    (lane / "work.txt").write_text("changed\n", encoding="utf-8", newline="\n")
    if staged:
        fixture_git(lane, "add", "--", "work.txt")
    extra = ["--wi", "WI-1"] if role == "AUTHOR" else []
    code, text, _ = _run(tmp_path, standin, role, lane, *extra, act=act, arg="work.txt")
    assert code == expected, text
    assert ("EDIT work.txt" in text) == (expected == 3), text
    assert len(fx.launches(standin[1])) == 1
    assert len(_tracked_call_logs(lane)) == 1
    assert (lane / "work.txt").read_text(encoding="utf-8") == "changed\n"


@pytest.mark.parametrize(
    "act, expected",
    [
        ("record-call", 0),
        ("commit-gate-log", 3),
        ("modify-log", 3),
        ("commit-work-path", 3),
    ],
)
def test_another_calls_log_commit_during_the_run_is_not_an_edit(
    tmp_path, standin, act, expected
):
    """Another call's `record` committing its own standard-call log during
    this call is not an edit; a commit of any other shape is. Adequacy
    witness: a check without the discount reads the first as an edit, and a
    discount by subject line or directory passes the others."""
    lane = _lane(tmp_path)
    old = fx.call_log(lane / "docs" / "iteration", role="CRITIQUE", route="OPENAI-SOL")
    fixture_commit(lane, "telemetry: an older call", fx.rel(lane, old))
    before = len(_tracked_call_logs(lane))
    code, text, _ = _run(
        tmp_path, standin, "REVIEW-A", lane, act=act, arg=fx.rel(lane, old)
    )
    assert code == expected, text
    assert len(fx.launches(standin[1])) == 1
    own_and_other = 2 if act == "record-call" else 1
    assert len(_tracked_call_logs(lane)) == before + own_and_other


@pytest.mark.parametrize(
    "act, expected",
    [("commit-waiting", 0), ("modify-waiting", 3), ("delete-waiting", 3)],
)
def test_a_waiting_call_log_committed_by_its_own_record_is_not_an_edit(
    tmp_path, standin, act, expected
):
    """A second call's log, uncommitted at the first snapshot and committed
    unchanged by its own record during the run, is not an edit; modified or
    deleted instead, it is. Adequacy witness: a judge that discounted any
    vanished call log passes the modified and deleted variants."""
    lane = _lane(tmp_path)
    waiting = fx.call_log(
        lane / "docs" / "iteration", role="CRITIQUE", route="OPENAI-SOL"
    )
    code, text, _ = _run(
        tmp_path, standin, "REVIEW-A", lane, act=act, arg=fx.rel(lane, waiting)
    )
    assert code == expected, text
    assert len(fx.launches(standin[1])) == 1


# --- the resumed turn ------------------------------------------------------------


def _carrier_case(lane, case):
    """Lay out one bad-carrier case in the lane; returns the log name the
    refusal must name ("" for none)."""
    iter_dir = lane / "docs" / "iteration"
    older = fx.call_log(iter_dir, stamp="20261022-100000", session_id="T-OLD")
    newer = fx.call_log(iter_dir, stamp="20261022-110000", session_id="T-NEW")
    text = newer.read_text(encoding="utf-8")
    if case == "absent":
        older.unlink()
        newer.unlink()
        review = fx.call_log(iter_dir, role="REVIEW-A", route="OPENAI-SOL")
        fixture_commit(lane, "telemetry: a review", fx.rel(lane, review))
        return ""
    if case == "header-cut":
        older.unlink()
        newer.write_text(fx.cut_before(text, "role"), encoding="utf-8", newline="\n")
    elif case == "newer-damaged":
        newer.write_text(fx.cut_before(text, "role"), encoding="utf-8", newline="\n")
    elif case == "garbage":
        newer.write_bytes(b"\xff\xfe\x00garbage\n")
    if case == "uncommitted-newer":
        fixture_commit(lane, "telemetry: the carrier", fx.rel(lane, older))
    else:
        fixture_commit(lane, "telemetry: the logs")
    return newer.name


@pytest.mark.parametrize(
    "case", ["absent", "header-cut", "newer-damaged", "uncommitted-newer", "garbage"]
)
def test_a_resumed_turn_with_a_bad_carrier_never_launches(tmp_path, standin, case):
    """Adequacy witness: a resume that fell back to a fresh thread, or to the
    newest readable log, launches here."""
    lane = _lane(tmp_path)
    named = _carrier_case(lane, case)
    code, text, _ = _run(tmp_path, standin, "AUTHOR", lane, "--wi", "WI-1", "--resume")
    assert code == 2, text
    assert fx.launches(standin[1]) == []
    if named:
        assert named in text


@pytest.mark.parametrize("role, expected", [("AUTHOR", 2), ("REVIEW-A", 0)])
def test_an_author_turn_naming_a_work_item_outside_the_lane_is_refused(
    tmp_path, standin, role, expected
):
    """An AUTHOR turn whose work item is not one the lane holds claimed is
    refused before launch, naming the id and the lane's ids; another role's
    work item is attribution only. Adequacy witness: an entry point that
    took the typed id on trust launches the AUTHOR turn here, and its log is
    one the next resumed turn skips as another lane's."""
    lane = _lane(tmp_path)
    code, text, out = _run(tmp_path, standin, role, lane, "--wi", "WI-9")
    assert code == expected, text
    if expected == 2:
        assert "WI-9" in text and "WI-1" in text, text
        assert fx.launches(standin[1]) == [] and not out.exists()
        assert _tracked_call_logs(lane) == []
    else:
        assert len(fx.launches(standin[1])) == 1


def test_a_second_terra_turn_resumes_the_first_turns_thread(tmp_path, standin):
    """Adequacy witness: a resume that read the id typed into the decisions
    record, or started a fresh thread, launches the wrong form here."""
    lane = _lane(tmp_path)
    code, text, _ = _run(
        tmp_path, standin, "AUTHOR", lane, "--wi", "WI-1", thread="T-FIRST"
    )
    assert code == 0, text
    decisions = lane / "docs" / "decisions" / "wi-1.toml"
    decisions.parent.mkdir(parents=True, exist_ok=True)
    decisions.write_text('session = "T-TYPED"\n', encoding="utf-8", newline="\n")
    fixture_commit(lane, "decisions", "docs/decisions/wi-1.toml")
    first_logs = set(_tracked_call_logs(lane))
    code, text, _ = _run(
        tmp_path,
        standin,
        "AUTHOR",
        lane,
        "--wi",
        "WI-1",
        "--resume",
        thread="T-FIRST",
    )
    assert code == 0, text
    launched = fx.launches(standin[1])
    assert len(launched) == 2
    first, second = launched
    assert "resume" not in first["argv"]
    argv = second["argv"]
    assert argv[:3] == ["exec", "resume", "T-FIRST"] and "-C" not in argv
    # The second turn's log is the one its call added: a log's name leads
    # with a random invocation id, so name order says nothing of time.
    added = sorted(set(_tracked_call_logs(lane)) - first_logs)
    assert len(added) == 1, added
    meta = agent_common.read_log_meta(lane / added[0])
    assert (meta["session-mode"], meta["session-id"]) == ("resumed", "T-FIRST")


# --- history and git ---------------------------------------------------------------


def test_a_rewritten_history_is_an_edit(tmp_path, standin):
    """Adequacy witness: a check that listed only `before..after` (empty after
    a reset) reads a rewritten history as clean."""
    lane = _lane(tmp_path)
    (lane / "extra.txt").write_text("x\n", encoding="utf-8")
    fixture_commit(lane, "an extra lane commit", "extra.txt")
    code, text, _ = _run(tmp_path, standin, "REVIEW-A", lane, act="reset-hard")
    assert code == 3, text


def test_git_unreadable_after_the_call_is_never_success(tmp_path, standin):
    """Adequacy witness: a check that read a failed git call as an empty
    answer exits 0 here."""
    lane = _lane(tmp_path)
    code, text, _ = _run(tmp_path, standin, "REVIEW-A", lane, act="break-git")
    assert code == 5, text
    assert "could not run" in text


# --- outside a lane ----------------------------------------------------------------


def _outside_roots(tmp_path):
    """The four roots outside a lane: the primary on trunk, the primary on a
    claimed branch, a detached linked worktree and a linked worktree on an
    unclaimed branch."""
    primary = _primary(_lane(tmp_path / "a"))
    detached, unclaimed = tmp_path / "a" / "detached", tmp_path / "a" / "scratch"
    fixture_git(primary, "worktree", "add", "-q", "--detach", str(detached), "main")
    fixture_git(
        primary, "worktree", "add", "-q", "-b", "scratch", str(unclaimed), "main"
    )
    on_branch = _primary_on_claimed_branch(tmp_path / "b")
    return {
        "primary on trunk": primary,
        "primary on a claimed branch": on_branch,
        "detached linked worktree": detached,
        "unclaimed branch": unclaimed,
    }


def test_a_call_outside_a_lane_spools_and_changes_nothing(tmp_path, standin):
    """Adequacy witness: a record that committed wherever it was rooted
    moves a ref or HEAD here, and one that refused leaves no log."""
    for label, root in _outside_roots(tmp_path).items():
        before, spooled = _state(root), _spooled(root)
        code, text, _ = _run(tmp_path, standin, "CRITIQUE", root)
        assert code == 0, (label, text)
        assert _state(root) == before, label
        new = sorted(set(_spooled(root)) - set(spooled))
        assert len(new) == 1, label
        assert new[0] in text, label


def test_concurrent_calls_from_one_detached_checkout_each_spool_their_own_log(
    tmp_path, standin
):
    """Adequacy witness: a spool keyed by anything but the call's own name
    loses two of the three logs."""
    primary = _primary(_lane(tmp_path))
    detached = tmp_path / "detached"
    fixture_git(primary, "worktree", "add", "-q", "--detach", str(detached), "main")
    before = _state(detached)
    env = fx.stand_in_env(*standin)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("critique the spec", encoding="utf-8")
    procs = [
        fx.start_call(
            [
                "CRITIQUE",
                "--root",
                detached,
                "--prompt-file",
                prompt,
                "--out",
                tmp_path / "o{}.md".format(n),
            ],
            env,
        )
        for n in range(3)
    ]
    outputs = [(p.wait(timeout=600), p.stdout.read()) for p in procs]
    assert [code for code, _ in outputs] == [0, 0, 0], outputs
    assert len(set(_spooled(detached))) == 3
    assert _state(detached) == before


# --- a lost commit and the blackout window ------------------------------------------


def test_a_refused_telemetry_commit_exits_nonzero_naming_the_log(tmp_path, standin):
    """Adequacy witness: a route that discarded `commit_telemetry`'s refusal
    exits 0 with the log left dangling."""
    lane = _lane(tmp_path)
    head = _head(lane)
    code, text, _ = _run(tmp_path, standin, "REVIEW-A", lane, act="lock-index")
    lock = fixture_git(lane, "rev-parse", "--git-path", "index.lock")
    lock = Path(lock) if Path(lock).is_absolute() else lane / lock
    lock.unlink(missing_ok=True)
    assert code == 4, text
    waiting = [p for p in _untracked(lane) if "/call_" in p]
    assert len(waiting) == 1
    assert Path(waiting[0]).name in text
    assert _head(lane) == head


def test_a_call_inside_the_blackout_window_is_refused_before_launch(
    tmp_path, standin, monkeypatch, capsys
):
    """Each role is refused before launch inside the window, as every
    non-adjudication call is. In process, so the window's clock can be set.
    Adequacy witness: a route that bypassed the service's launch refusal
    launches the stand-in here."""
    lane = _lane(tmp_path)
    (lane / "docs" / "process.toml").write_text(
        '[policies]\ntrunk = "main"\nblackout = "12:00-19:00"\n',
        encoding="utf-8",
        newline="\n",
    )
    monkeypatch.setattr(sys.modules["agent_policy"], "_utcnow", lambda: MONDAY_INSIDE)
    for name, value in fx.stand_in_env(*standin).items():
        monkeypatch.setenv(name, value)
    cc = fx.load_codex_call()
    prompt = tmp_path / "prompt.md"
    prompt.write_text("judge", encoding="utf-8")
    common = ["--root", str(lane), "--prompt-file", str(prompt)]
    for role, extra in (
        ("REVIEW-A", []),
        ("CRITIQUE", []),
        ("AUTHOR", ["--wi", "WI-1"]),
    ):
        out = tmp_path / "{}.md".format(role)
        assert cc.main([role, *common, "--out", str(out), *extra]) == 2, role
    assert fx.launches(standin[1]) == []
    assert list((lane / "docs" / "iteration").glob("call_*.log")) == []
    assert _spooled(lane) == []
    assert "blackout" in capsys.readouterr().out.casefold()


# --- the lane reading ---------------------------------------------------------------


def _loose_tree_gone(primary):
    """Trunk's root tree made unreadable: a commit only trunk holds, whose
    loose tree object is then removed, so `ls-tree` of trunk fails while the
    ref still resolves."""
    (primary / "trunk-only.txt").write_text("t\n", encoding="utf-8")
    fixture_commit(primary, "a trunk-only commit", "trunk-only.txt")
    tree = fixture_git(primary, "rev-parse", "main^{tree}")
    obj = primary / ".git" / "objects" / tree[:2] / tree[2:]
    os.chmod(obj, stat.S_IWRITE | stat.S_IREAD)
    obj.unlink()


def _lane_matrix(tmp_path):
    """Every root of the claim-state matrix, built for real; `{label: root}`."""
    roots = {}
    roots["primary on trunk"] = _primary(claimed_lane(tmp_path / "r1"))
    roots["primary on claimed B"] = _primary_on_claimed_branch(tmp_path / "r2")
    primary = _primary(claimed_lane(tmp_path / "r3"))
    fixture_git(
        primary,
        "worktree",
        "add",
        "-q",
        "--detach",
        str(tmp_path / "r3" / "det"),
        "main",
    )
    roots["detached linked worktree"] = tmp_path / "r3" / "det"
    roots["B: claim on both"] = claimed_lane(tmp_path / "r4")
    closed = claimed_lane(tmp_path / "r5")
    _close_on_branch(closed)
    roots["B: closed on the branch, held on trunk"] = closed
    dropped = claimed_lane(tmp_path / "r6")
    _drop_from_trunk(_primary(dropped))
    roots["B: on the branch, dropped from trunk"] = dropped
    neither = claimed_lane(tmp_path / "r7")
    _close_on_branch(neither)
    _drop_from_trunk(_primary(neither))
    roots["B: on neither"] = neither
    roots["no trunk: on the branch"] = claimed_lane(tmp_path / "r8", trunk=False)
    untrunked = claimed_lane(tmp_path / "r9", trunk=False)
    _close_on_branch(untrunked)
    roots["no trunk: closed on the branch"] = untrunked
    unreadable = claimed_lane(tmp_path / "r10")
    _close_on_branch(unreadable)
    _loose_tree_gone(_primary(unreadable))
    roots["trunk unreadable: closed on the branch"] = unreadable
    held = claimed_lane(tmp_path / "r11")
    _loose_tree_gone(_primary(held))
    roots["trunk unreadable: claim on the branch"] = held
    return roots


def test_lane_ness_follows_the_written_predicate_and_the_close_first_case(tmp_path):
    """The lane reading over the claim-state matrix: the primary checkout and
    a detached HEAD are never a lane; a linked worktree on B is a lane while
    B's tree or trunk's committed tree holds its claim (the close-first
    case); a claim read that cannot be read adds no claim, so a root that
    neither readable tree shows claimed is not a lane. Adequacy witness: a
    reading of B's tree alone misses the close-first row, one of trunk's
    tree alone misses the dropped-from-trunk row, and one that lets an
    unreadable trunk read decide "not a lane" misses the trunk-unreadable
    row whose claim is on the branch."""
    expected = {
        "primary on trunk": None,
        "primary on claimed B": None,
        "detached linked worktree": None,
        "B: claim on both": "wi-1",
        "B: closed on the branch, held on trunk": "wi-1",
        "B: on the branch, dropped from trunk": "wi-1",
        "B: on neither": None,
        "no trunk: on the branch": "wi-1",
        "no trunk: closed on the branch": None,
        "trunk unreadable: closed on the branch": None,
        "trunk unreadable: claim on the branch": "wi-1",
    }
    roots = _lane_matrix(tmp_path)
    assert {label: svc.lane_branch(root) for label, root in roots.items()} == expected
