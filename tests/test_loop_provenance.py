"""Loop provenance: the `Loop-Session` trailer, the loop marker, and the history
check for a loop commit that changed a human-held status (TC-242, TC-243).

A status change on a rung the approval level holds for a human is supposed to
mean a human judged. The loop's commits can be told apart from a person's only
if every one of them says it is the loop's, so the pieces pinned here are one
chain rather than four features:

  * the trailer's own grammar (`kitlib.provenance`) — format and parse round
    trip, the last trailer wins, and a missing, malformed or other-session
    trailer is refused naming the commit's subject;
  * the MARKER that tells a commit floor which commits are the loop's: set in
    the dispatcher's and the loop entry's own process environment, so every
    child they start inherits it, and never in a launcher script, so a person's
    shell does not;
  * the floors that hold a marked commit to the trailer: the merge ladder
    re-checks every commit in a lane's range (plumbing and --no-verify commits
    never reach a hook, and hooks are opt-in per checkout); the commit-msg hook
    half lives in tests/test_pre_commit_hook.py beside its siblings;
  * every loop writer's message carrying the trailer — the claim, the refresh,
    the merge, the mint's bookkeeping commit, the handback close and the
    telemetry commit — and a refused telemetry commit reported, not swallowed;
  * the HISTORY CHECK (`check_trajectory.loop_held_status_findings`): each
    trailer-carrying commit that changed a status on a rung its OWN tree's dial
    holds is one advisory, merges skipped, a root commit diffed against the
    empty tree, and the pure dial comparison (`kitlib.authority`) on each rung.

Every git fixture is a real repository and the loop's own entry points run for
real; the only stand-ins are the two harness scripts a lane's refresh runs,
which record nothing and pass, because what is asserted is the message the
refresh commits, not the bar it ran.
"""

import os
import stat
import subprocess
import sys

from conftest import (
    ROOT,
    SCRIPTS,
    env_gate_skipif,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
    write_wi_registry,
)
from integrate_fixtures import (
    T_BASE,
    T_CODE,
    T_LATER,
    T_VERDICT,
    _commit,
    _git,
    _rev,
    claim_repo,
    declare_generated,
    git_repo,
    integ,
)
from kitlib import authority, ladder, provenance
from kitlib import stage as kitstage

pytestmark = env_gate_skipif("git")

ac = integ.ac
ctraj = load_script("check_trajectory")
dispatch = load_script("dispatch")
handback = load_script("handback")
intake = load_script("intake")

SESSION = "20260926T101500Z-a1b2c3"
OTHER = "20260926T111500Z-d4e5f6"
MARK = provenance.LOOP_SESSION_ENV

FRAME = "docs/requirements/external.toml"
INTERFACES = "docs/requirements/interfaces.toml"
POLICY = "docs/process.toml"

GAP = "SR-001 is not Approved (Status=Drafted)"


def _trailered(message, session=SESSION):
    """A commit message ending in the loop's trailer — a session's own commit."""
    return "{}\n\n{}".format(message, provenance.format_loop_trailer(session))


def _message(root, rev="HEAD"):
    return _git(root, "log", "-1", "--format=%B", rev)


# --- TC-242: the trailer's own grammar -----------------------------------------


def test_format_and_parse_round_trip():
    for session in (SESSION, OTHER, "s1", "run.7_b-2"):
        line = provenance.format_loop_trailer(session)
        assert line == "{}: {}".format(provenance.LOOP_TRAILER, session)
        assert provenance.parse_loop_trailer("fix it\n\nbody\n\n" + line) == session
    # A value the grammar refuses cannot be FORMATTED either, so no writer can
    # emit a trailer its own reader would call malformed.
    for bad in ("", "two words", "-leading-dash", "x" * 65):
        try:
            provenance.format_loop_trailer(bad)
        except ValueError:
            continue
        raise AssertionError("formatted a malformed session {!r}".format(bad))


def test_the_trailer_joins_the_existing_trailer_block_git_reads(tmp_path):
    # Git reads trailers from the LAST paragraph only, so appending a new
    # paragraph after `WI: WI-401` would hide the WI trailer from every
    # `%(trailers)` reader the loop has. The writers' helper therefore extends
    # an existing block instead of starting a second one — checked with git's
    # own parser rather than with ours.
    root = git_repo(tmp_path)
    for message in ("close: WI-401\n\nbody\n\nWI: WI-401", "plain subject"):
        marked = provenance.with_loop_trailer(message, SESSION)
        parsed = subprocess.run(
            ["git", "-C", str(root), "interpret-trailers", "--parse"],
            input=marked,
            capture_output=True,
            encoding="utf-8",
        ).stdout
        assert "Loop-Session: {}".format(SESSION) in parsed
        if "WI:" in message:
            assert "WI: WI-401" in parsed, parsed
        assert provenance.parse_loop_trailer(marked) == SESSION
    # Unmarked and given no session, a message is left exactly as it was.
    assert provenance.with_loop_trailer("plain subject") == "plain subject"


def test_the_last_trailer_wins():
    message = "fix the widget\n\nLoop-Session: {}\nLoop-Session: {}\n".format(
        OTHER, SESSION
    )
    assert provenance.parse_loop_trailer(message) == SESSION
    assert provenance.loop_trailer_refusal(message, SESSION) is None
    refusal = provenance.loop_trailer_refusal(message, OTHER)
    assert refusal and "fix the widget" in refusal and SESSION in refusal


def test_a_missing_trailer_is_refused_naming_the_subject():
    for message in (
        "fix the widget\n\nWI: WI-401\n",
        "fix the widget",
        # Quoted in the body, not in the final trailer block: git does not
        # read it as a trailer, and neither does the floor.
        "fix the widget\n\nLoop-Session: {}\n\nmore words after it\n".format(SESSION),
    ):
        assert provenance.parse_loop_trailer(message) is None
        refusal = provenance.loop_trailer_refusal(message, SESSION)
        assert refusal and "fix the widget" in refusal, message
        assert "no Loop-Session trailer" in refusal


def test_a_malformed_trailer_is_refused_naming_the_subject():
    for value in ("", "two words", "-dash", "x" * 65):
        message = "fix the widget\n\nWI: WI-401\nLoop-Session: {}\n".format(value)
        assert provenance.parse_loop_trailer(message) is None, value
        for session in (SESSION, None):
            refusal = provenance.loop_trailer_refusal(message, session)
            assert refusal and "fix the widget" in refusal, value
            assert "malformed" in refusal, refusal
    # The LAST trailer is the one judged: a good one before a bad one is bad.
    message = "fix the widget\n\nLoop-Session: {}\nLoop-Session: bad value\n".format(
        SESSION
    )
    assert "malformed" in provenance.loop_trailer_refusal(message, SESSION)


def test_a_trailer_naming_another_session_is_refused_naming_the_subject():
    message = _trailered("fix the widget", OTHER)
    refusal = provenance.loop_trailer_refusal(message, SESSION)
    assert refusal and "fix the widget" in refusal and OTHER in refusal
    # Asked with no session (the merge slot, where a lane may span runs), any
    # well-formed trailer is the loop's.
    assert provenance.loop_trailer_refusal(message, None) is None
    assert provenance.loop_trailer_refusal(_trailered("fix", SESSION), SESSION) is None


# --- TC-242: the marker reaches every child the loop starts ---------------------

PRINT_MARKER = "import os; print(os.environ.get({!r}, '<ABSENT>'))".format(MARK)


def test_a_child_the_dispatcher_starts_sees_the_marker(tmp_path, capfd):
    root = claim_repo(tmp_path)
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "ignore the lock directory", when=T_CODE)
    assert MARK not in os.environ  # nothing inherited from this test's own shell
    seen = []

    def worker(r, branch, wi_ids, args):
        child = subprocess.run(
            [sys.executable, "-c", PRINT_MARKER], capture_output=True, text=True
        )
        seen.append(child.stdout.strip())
        return 0

    args = dispatch_args(stall_limit=1)
    dispatch.run(root, args, worker=worker, tier="smoke")
    assert len(seen) == 1 and seen[0] != "<ABSENT>", seen
    assert provenance.parse_loop_trailer(_trailered("x", seen[0])) == seen[0]
    # The claim the dispatcher committed on the child's behalf names the same
    # session, so one run's marker and its commits cannot disagree.
    claim = _git(root, "log", "-1", "--format=%B", "--grep=^claim: ", "main")
    assert provenance.parse_loop_trailer(claim) == seen[0], claim


def dispatch_args(**kw):
    """The argparse surface `dispatch.run` reads (tests/test_dispatch.py's
    shape, copied per this suite's no-cross-test-import idiom)."""
    import argparse

    ns = argparse.Namespace(
        agent_cmd="stub-agent",
        session_timeout=0,
        no_session_echo=False,
        live_status=False,
        max_iterations=10,
        stall_limit=3,
        lanes=None,
        model="",
        model_map="",
        cmd_map="",
        prompt_map="",
        tier_map="",
        prefer_map="",
        wait_on_limit=0,
        limit_retry_fallback=3600,
    )
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


# The fake agent the loop's main entry launches: record the marker it was
# started with, commit one build carrying the trailer the session prompt asks
# for, and stop.
FAKE_AGENT = r"""
import argparse, os, pathlib, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
seen = os.environ.get("KIT_LOOP_SESSION", "<ABSENT>")
ctl = pathlib.Path(args.control)
with open(str(ctl / "marker-seen.txt"), "a", encoding="utf-8") as fh:
    fh.write(seen + "\n")
with open(str(ctl / "prompt.txt"), "w", encoding="utf-8") as fh:
    fh.write(args.prompt)
pathlib.Path("work.txt").write_text("built", encoding="utf-8")
subprocess.run(["git", "add", "work.txt"], check=True)
message = "build done\n\nWI: WI-201\nLoop-Session: " + seen
subprocess.run(["git", "commit", "-q", "-m", message], check=True)
sys.exit(0)
"""


def _loop_repo(tmp_path):
    """A worker-mode repo for one agent_loop.py session (tests/
    test_agent_loop_env.py's harness, copied per the no-cross-import idiom)."""
    import csv

    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(
        "# Status\n\n## Current State\n\n- nothing pending\n", encoding="utf-8"
    )
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    row = ["WI-201", "Scoped work for WI-201", "ws", "", "", "queued", "", ""]
    write_wi_registry(repo, [row + ["medium", "ordinary"]])
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows = [
        ["Id", "Family", "Model", "Version", "Tier", "CmdTemplate", "Env", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, "", ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text("PROVA-BUILD-1\n", encoding="utf-8")
    for args in (
        ("init", "-q"),
        ("config", "user.email", "loop@example.com"),
        ("config", "user.name", "Loop Test"),
        ("config", "commit.gpgsign", "false"),
    ):
        _git(repo, *args)
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")
    return repo, ctl, cmd


def test_a_child_the_loops_main_entry_starts_sees_the_marker(tmp_path):
    repo, ctl, cmd = _loop_repo(tmp_path)
    assert MARK not in os.environ
    proc = run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "4",
            "--wi",
            "WI-201",
            "--train",
            "t1",
        ],
        cwd=repo,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    seen = (ctl / "marker-seen.txt").read_text(encoding="utf-8").split()
    assert len(seen) == 1 and seen[0] != "<ABSENT>", seen
    # The session is told the trailer it owes, with the value it must write.
    prompt = (ctl / "prompt.txt").read_text(encoding="utf-8")
    assert provenance.format_loop_trailer(seen[0]) in prompt
    # The loop's own telemetry commit names the same session.
    log = _git(repo, "log", "--format=%B%x1e", "llm/train/t1").split("\x1e")
    telemetry = [m for m in log if m.strip().startswith("telemetry:")]
    assert telemetry, log
    for message in telemetry:
        assert provenance.parse_loop_trailer(message) == seen[0], message
    # ...and the person's shell that launched it never held one.
    assert MARK not in os.environ


def test_the_launcher_scripts_never_set_the_marker():
    # The marker is set by the loop's own process, once per run. A launcher
    # that exported it would leave it in a PERSON's shell (the .command and
    # .sh launchers can be sourced), and every commit that person then made
    # would read as the loop's.
    launchers = sorted(SCRIPTS.glob("*.template.*")) + sorted(
        ROOT.glob("agent-resume.*")
    )
    assert len(launchers) >= 6, launchers
    for path in launchers:
        text = path.read_text(encoding="utf-8", errors="replace")
        assert MARK not in text, path


# --- TC-242: the merge ladder re-checks every commit in a lane's range ---------


def _closed_lane(tmp_path, monkeypatch, plumbing=True, loop=True):
    """A claimed lane holding one trailered build commit, then (optionally) a
    PLUMBING commit written with `commit-tree` and no trailer - the shape that
    never reaches a commit hook - then a trailered close into `complete/`.
    `loop` claims it under the marker, which is what makes it the LOOP's lane;
    the marker is gone again afterwards, so each test says who runs the slot."""
    root = claim_repo(tmp_path)
    if loop:
        monkeypatch.setenv(MARK, SESSION)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    monkeypatch.delenv(MARK, raising=False)
    _git(root, "checkout", "-q", "wi-401")
    (root / "a.txt").write_text("a\n", encoding="utf-8", newline="\n")
    _commit(root, _trailered("WI-401: build"), when=T_CODE)
    if plumbing:
        (root / "b.txt").write_text("b\n", encoding="utf-8", newline="\n")
        _git(root, "add", "-A")
        tree = _git(root, "write-tree").strip()
        sha = _git(
            root,
            "commit-tree",
            tree,
            "-p",
            "HEAD",
            "-m",
            "plumbing: the unmarked write",
        ).strip()
        _git(root, "update-ref", "refs/heads/wi-401", sha)
    src = "docs/work/active/wi-401/WI-401-widget.md"
    dest = root / "docs" / "work" / "complete" / "WI-401-widget.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    _git(root, "mv", src, "docs/work/complete/WI-401-widget.md")
    _commit(root, _trailered("close: WI-401 -> complete"), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")
    return root


def test_the_merge_ladder_refuses_a_lane_holding_an_unmarked_plumbing_commit(
    tmp_path, monkeypatch
):
    root = _closed_lane(tmp_path, monkeypatch)
    head = _rev(root, "HEAD")
    monkeypatch.setenv(MARK, SESSION)  # the slot runs inside the loop

    refusal = integ._loop_trailer_refusal(root, "wi-401")
    assert refusal and "plumbing: the unmarked write" in refusal, refusal
    assert "no Loop-Session trailer" in refusal
    merged = integ.integrate_one(root, "wi-401", "smoke")
    assert merged and "plumbing: the unmarked write" in merged, merged
    assert _rev(root, "HEAD") == head  # nothing merged


def test_the_merge_ladder_admits_a_lane_whose_every_commit_is_marked(
    tmp_path, monkeypatch
):
    root = _closed_lane(tmp_path, monkeypatch, plumbing=False)
    monkeypatch.setenv(MARK, SESSION)
    assert integ._loop_trailer_refusal(root, "wi-401") is None


def test_a_slot_run_by_a_person_judges_a_loop_lane_too(tmp_path, monkeypatch):
    # No marker in the slot's own process, and the rung is armed anyway: the
    # slot sees commits, not processes, and hooks are opt-in, so the slot is
    # the one place the floor always runs. A loop lane's commits are judged
    # whoever merges it; a person's commit belongs in the person's own lane.
    root = _closed_lane(tmp_path, monkeypatch)
    refusal = integ._loop_trailer_refusal(root, "wi-401")
    assert refusal and "plumbing: the unmarked write" in refusal, refusal


def test_a_person_s_own_lane_is_not_judged_whoever_merges_it(tmp_path, monkeypatch):
    # Claimed and built by a person, and nothing of the loop's in it: neither
    # the claim nor any commit a loop writer makes carries the trailer. Its
    # commits were never the loop's, with or without the marker at the slot.
    root = _closed_lane(tmp_path, monkeypatch, loop=False)
    assert integ._loop_trailer_refusal(root, "wi-401") is None
    monkeypatch.setenv(MARK, SESSION)
    assert integ._loop_trailer_refusal(root, "wi-401") is None


def _loop_writer_commit(root, when):
    """A commit one of the loop's own writers makes INTO a lane - a session's
    telemetry - carrying the loop's trailer."""
    log = root / "docs" / "iteration" / "001-test.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("# phase: BUILD\n", encoding="utf-8", newline="\n")
    _commit(root, _trailered("telemetry: session 001 iteration log"), when=when)


def test_a_lane_the_loop_later_builds_is_judged_from_its_first_marked_loop_commit(
    tmp_path, monkeypatch
):
    # Claimed and started by a person (its unmarked plumbing commit), then built
    # by the loop: the first marked loop-writer commit makes the lane the
    # loop's. What came before it is the migration window, exempt from the
    # trailer rung (never from the held-status rung); what comes after is judged.
    root = _closed_lane(tmp_path, monkeypatch, loop=False)
    _git(root, "checkout", "-q", "wi-401")
    _loop_writer_commit(root, T_LATER)
    _git(root, "checkout", "-q", "main")
    assert integ._loop_trailer_refusal(root, "wi-401") is None

    _git(root, "checkout", "-q", "wi-401")
    (root / "after.txt").write_text("after\n", encoding="utf-8", newline="\n")
    _commit(root, "a person's commit inside the loop's lane", when=T_LATER + 1)
    _git(root, "checkout", "-q", "main")
    refusal = integ._loop_trailer_refusal(root, "wi-401")
    assert refusal and "a person's commit inside the loop's lane" in refusal
    assert "plumbing: the unmarked write" not in refusal  # the window's own


# --- TC-242: every loop writer's message carries the trailer -------------------

STUB_TRUNK_STEP = (
    'import pathlib\npathlib.Path("regenerated.txt").write_text("fresh\\n")\n'
)
STUB_CHECK_GREEN = 'print("  PASS  format           0.1s")\n'


def _station_repo(tmp_path):
    """WI-401 queued on a trunk whose lane refresh runs stand-in harness
    scripts (tests/test_integrate_station.py's `station_repo` shape, copied per
    the no-cross-import idiom): everything the slot reads is real."""
    root = claim_repo(tmp_path)
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n", encoding="utf-8", newline="\n"
    )
    declare_generated(root)
    (root / "docs" / "review-policy").write_text("0\n", encoding="utf-8", newline="\n")
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(STUB_TRUNK_STEP, encoding="utf-8")
    (scripts / "check.py").write_text(STUB_CHECK_GREEN, encoding="utf-8")
    _commit(root, "chore: the stub harness and the declared bar", when=T_CODE)
    return root


def test_the_claim_refresh_merge_and_mint_writers_carry_the_trailer(
    tmp_path, monkeypatch
):
    root = _station_repo(tmp_path)
    monkeypatch.setenv(MARK, SESSION)

    # The claim.
    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert provenance.parse_loop_trailer(_message(root, "HEAD")) == SESSION
    # A session's own lane work, as the prompt tells it to write it.
    wt, err = integ.lane_worktree(root, "wi-401")
    assert err is None, err
    (wt / "wi-401.txt").write_text("1\n", encoding="utf-8", newline="\n")
    src = wt / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    dst = wt / "docs" / "work" / "complete" / "WI-401-widget.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        src.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
        encoding="utf-8",
        newline="\n",
    )
    _git(wt, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(wt, _trailered("WI-401: build + close"), when=T_VERDICT)

    # The refresh: the trailer rides beside Bar-Green, which still verifies.
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert provenance.parse_loop_trailer(_message(root, sha)) == SESSION
    assert integ.refresh_attestation(root, "wi-401", sha)
    # ...and the slot reads it as one of the loop's own writers' commits, the
    # mark that makes a lane the loop's.
    assert integ._marked_loop_writer(_message(root, sha), "wi-401")

    # The merge.
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    merge = _git(root, "log", "-1", "--merges", "--format=%B", "main")
    assert merge.startswith("integrate: merge wi-401"), merge
    assert provenance.parse_loop_trailer(merge) == SESSION

    # The mint's bookkeeping commit.
    minted, refusal = intake.mint_gap_rows(root, [GAP])
    assert refusal is None and minted, refusal
    assert provenance.parse_loop_trailer(_message(root, "HEAD")) == SESSION


def test_the_handback_close_and_telemetry_writers_carry_the_trailer(
    tmp_path, monkeypatch
):
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    wt, err = integ.lane_worktree(root, "wi-401")
    assert err is None, err
    (wt / "half-built.txt").write_text("residue\n", encoding="utf-8", newline="\n")
    monkeypatch.setenv(MARK, SESSION)

    tip = _rev(root, "wi-401")
    closed, refusal = handback.close_partial(root, "wi-401", "the lane stopped")
    assert refusal is None and closed == ["WI-401"], refusal
    written = _git(root, "log", "--format=%B%x1e", tip + "..wi-401").split("\x1e")
    written = [m for m in written if m.strip()]
    assert len(written) == 2, written  # the residue, then the partial close
    for message in written:
        assert provenance.parse_loop_trailer(message) == SESSION, message
        assert integ._marked_loop_writer(message, "wi-401"), message

    # The quarantine, driven for real: the residue left a product file on the
    # lane, which is what a red close reverts.
    tip = _rev(root, "wi-401")
    assert handback.quarantine(root, "wi-401", "bar exit 1") is None
    message = _message(root, "wi-401")
    assert _rev(root, "wi-401") != tip
    assert message.startswith("handback: revert wi-401 to a bar-inert artefact")
    assert provenance.parse_loop_trailer(message) == SESSION
    assert integ._marked_loop_writer(message, "wi-401"), message

    # The mechanical adjudication close composes its subject through the one
    # shared composer, which is what `close_adjudication` commits; a multi-row
    # close joins the ids.
    for closed in (["WI-401"], ["WI-401", "WI-402"]):
        message = provenance.with_loop_trailer(
            handback.mechanical_close_subject(closed) + "\n\nWI: WI-401", SESSION
        )
        assert integ._marked_loop_writer(message, "wi-401"), message

    log = root / "docs" / "iteration" / "001-test.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("# phase: BUILD\n", encoding="utf-8", newline="\n")
    head = _rev(root, "HEAD")
    assert ac.commit_telemetry(root, "001", "iteration log", [log]) is None
    assert _rev(root, "HEAD") != head
    message = _message(root, "HEAD")
    assert message.startswith("telemetry: session 001")
    assert provenance.parse_loop_trailer(message) == SESSION
    assert integ._marked_loop_writer(message, "wi-401")


def test_a_refused_telemetry_commit_is_reported(tmp_path, monkeypatch, capsys):
    skip_without_env_gates("posix-shell", "git")
    root = git_repo(tmp_path)
    hooks = tmp_path / "veto-hooks"
    hooks.mkdir()
    veto = hooks / "pre-commit"
    veto.write_text(
        "#!/bin/sh\necho 'vetoed by the test hook' >&2\nexit 1\n",
        encoding="utf-8",
        newline="\n",
    )
    veto.chmod(veto.stat().st_mode | stat.S_IEXEC)
    _git(root, "config", "core.hooksPath", str(hooks).replace("\\", "/"))
    log = root / "docs" / "iteration" / "001-test.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("# phase: BUILD\n", encoding="utf-8", newline="\n")
    monkeypatch.setenv(MARK, SESSION)
    head = _rev(root, "HEAD")

    refusal = ac.commit_telemetry(root, "001", "iteration log", [log])
    assert refusal and "vetoed by the test hook" in refusal, refusal
    assert "telemetry commit skipped" in capsys.readouterr().err
    assert _rev(root, "HEAD") == head
    assert _git(root, "diff", "--cached", "--name-only").strip() == ""  # unstaged
    assert log.is_file()  # left exactly as found


# --- TC-243: loop commits that changed a held status, found in history ----------


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _dial(value):
    return '[attestation]\nhuman_approval_through = "{}"\n'.format(value)


def _rows(table, **statuses):
    return "".join(
        '[{}.{}]\nstatus = "{}"\n\n'.format(table, rid.replace("_", "-"), status)
        for rid, status in statuses.items()
    )


def _bare(root):
    root.mkdir(parents=True, exist_ok=True)
    for args in (
        ("init", "-q"),
        ("config", "user.email", "t@example.com"),
        ("config", "user.name", "T"),
        ("config", "commit.gpgsign", "false"),
    ):
        _git(root, *args)
    pin_autocrlf(root)
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    return root


def _commit_all(root, message, when):
    _commit(root, message, when=when)
    return _rev(root, "HEAD")


def _history(tmp_path):
    """Three trunk commits after a seed, and a merged lane:

    c1  trailer   B-01 Drafted -> Approved   Boundary, held by its dial
    c2  trailer   IF-001 Drafted -> Approved  Arch, released by its dial
    c3  none      B-01 Approved -> Drafted   held, but a person's commit
    l1  trailer   B-01 Drafted -> Approved   inside a lane, merged by m
    m   trailer   the --no-ff merge of the lane: its changes are l1's
    """
    root = _bare(tmp_path / "history")
    _write(root, POLICY, _dial("DevStg-Boundary"))
    _write(root, FRAME, _rows("boundary", B_01="Drafted"))
    _write(root, INTERFACES, _rows("interface", IF_001="Drafted"))
    shas = {"seed": _commit_all(root, "seed: the frame", T_BASE)}
    _write(root, FRAME, _rows("boundary", B_01="Approved"))
    shas["c1"] = _commit_all(root, _trailered("loop: approve B-01"), T_BASE + 1)
    _write(root, INTERFACES, _rows("interface", IF_001="Approved"))
    shas["c2"] = _commit_all(root, _trailered("loop: approve IF-001"), T_BASE + 2)
    _write(root, FRAME, _rows("boundary", B_01="Drafted"))
    shas["c3"] = _commit_all(root, "owner: reopen B-01", T_BASE + 3)
    _git(root, "checkout", "-q", "-b", "lane")
    _write(root, FRAME, _rows("boundary", B_01="Approved"))
    shas["l1"] = _commit_all(root, _trailered("lane: approve B-01"), T_BASE + 4)
    _git(root, "checkout", "-q", "main")
    _write(root, "notes.txt", "trunk moved\n")
    shas["c4"] = _commit_all(root, "owner: a note", T_BASE + 5)
    _git(
        root,
        "merge",
        "-q",
        "--no-ff",
        "-m",
        _trailered("integrate: merge lane"),
        "lane",
    )
    shas["m"] = _rev(root, "HEAD")
    return root, shas


def test_each_loop_commit_that_changed_a_held_status_is_reported_once(tmp_path):
    root, shas = _history(tmp_path)
    findings = ctraj.loop_held_status_findings(root)
    assert len(findings) == 2, findings
    by_commit = {sha: [f for f in findings if sha[:10] in f] for sha in shas.values()}
    for name in ("c1", "l1"):
        hit = by_commit[shas[name]]
        assert len(hit) == 1, (name, findings)
        assert "B-01" in hit[0] and "DevStg-Boundary" in hit[0], hit[0]
    for name in ("seed", "c2", "c3", "c4", "m"):
        assert by_commit[shas[name]] == [], (name, findings)
    # The harness reports them, warn-only: the exit code does not move.
    proc = run_py([SCRIPTS / "check_trajectory.py", "--root", root], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for line in findings:
        assert line in proc.stderr, proc.stderr


def test_raising_the_dial_later_does_not_change_an_earlier_verdict(tmp_path):
    root, shas = _history(tmp_path)
    before = ctraj.loop_held_status_findings(root)
    # Every rung held from here on: c2's Arch change would now be held, but c2
    # is judged against the dial ITS OWN tree declared.
    _write(root, POLICY, _dial("DevStg-Release"))
    _commit_all(root, _trailered("loop: raise the dial"), T_LATER)
    assert ctraj.loop_held_status_findings(root) == before


def test_a_root_commit_is_compared_with_the_empty_tree(tmp_path):
    root = _bare(tmp_path / "rooted")
    _write(root, POLICY, _dial("DevStg-Boundary"))
    _write(root, FRAME, _rows("boundary", B_01="Approved"))
    sha = _commit_all(root, _trailered("loop: the first frame"), T_BASE)
    findings = ctraj.loop_held_status_findings(root)
    assert len(findings) == 1 and sha[:10] in findings[0], findings
    assert "B-01" in findings[0] and "DevStg-Boundary" in findings[0]


def test_a_commit_with_no_dial_is_judged_most_held_and_warns_nothing(tmp_path, capsys):
    root = _bare(tmp_path / "undialled")
    _write(root, POLICY, "[policies]\nreview_rounds = 0\n")
    _write(root, INTERFACES, _rows("interface", IF_001="Drafted"))
    _commit_all(root, "seed", T_BASE)
    _write(root, INTERFACES, _rows("interface", IF_001="Approved"))
    no_dial = _commit_all(root, _trailered("loop: approve IF-001"), T_BASE + 1)
    # A LEGACY ordinal reads as most-held too. The live reader would translate
    # `1` to DevStg-Boundary and release Arch; the history check must not guess.
    _write(root, POLICY, "[attestation]\nhuman_approval_through = 1\n")
    _write(root, INTERFACES, _rows("interface", IF_001="Drafted"))
    legacy = _commit_all(root, _trailered("loop: reopen IF-001"), T_BASE + 2)
    capsys.readouterr()

    findings = ctraj.loop_held_status_findings(root)
    assert len(findings) == 2, findings
    assert any(no_dial[:10] in f for f in findings)
    assert any(legacy[:10] in f for f in findings)
    assert all("DevStg-Arch" in f and "IF-001" in f for f in findings)
    out = capsys.readouterr()
    assert out.out == "" and out.err == "", out


def test_the_dial_comparison_holds_every_rung_at_or_below_it():
    rungs = ladder.STAGE_ORDER
    for i, dial in enumerate(rungs):
        for j, rung in enumerate(rungs):
            assert authority.holds_under(dial, rung) is (j <= i), (dial, rung)
    for rung in rungs:
        assert authority.holds_under(kitstage.BELOW, rung) is False, rung
    # The two unreadable ends fail toward the human.
    assert authority.holds_under(ladder.STAGE_NEEDS, "DevStg-Nowhere") is True
    assert authority.holds_under("devstg-needs", ladder.STAGE_RELEASE) is True
    assert authority.holds_under(ladder.STAGE_RELEASE, None) is True


def test_the_dial_is_read_from_a_parsed_policy_and_fails_toward_most_held(capsys):
    def table(**att):
        return {"attestation": att}

    read = authority.dial_from_config
    for rung in list(ladder.STAGE_ORDER) + [kitstage.BELOW]:
        assert read(table(human_approval_through=rung)) == rung
    most = ladder.STAGE_RELEASE
    for policy in (
        {},
        {"attestation": "not a table"},
        table(),
        table(human_approval_through=1),
        table(human_approval_through="devstg-arch"),
        table(human_ratification_through="DevStg-Arch"),
        None,
    ):
        assert read(policy) == most, policy
    out = capsys.readouterr()
    assert out.out == "" and out.err == "", out


def test_the_rung_map_names_every_off_spine_status_registry():
    # The assumptions registry joins the frame at DevStg-Boundary; the shared
    # coordinator re-exports the one table rather than keeping a copy.
    assert authority.APPROVAL_RUNGS["assumptions"] == ladder.STAGE_BOUNDARY
    assert authority.APPROVAL_RUNGS["external"] == ladder.STAGE_BOUNDARY
    assert ac.APPROVAL_RUNGS is authority.APPROVAL_RUNGS
    assert ac.SPINE_APPROVAL_RUNGS is authority.SPINE_APPROVAL_RUNGS


# --- the review's rulings: the needs' rung, and one meaning of the live dial ----

NEEDS = "docs/requirements/stakeholder-needs.toml"


def test_needs_and_stakeholder_statuses_are_held_at_the_needs_rung(tmp_path):
    # The needs file carries the needs (a spine tier) and the stakeholder list
    # (an off-spine one), both approved at DevStg-Needs. Each move is reported
    # once where that rung is held, although both walks read the one file, and
    # nothing is reported where the dial holds nothing.
    for dial, held in (("DevStg-Needs", True), ("DevStg-Below", False)):
        root = _bare(tmp_path / dial)
        _write(root, POLICY, _dial(dial))
        _write(
            root,
            NEEDS,
            _rows("need", SN_001="Drafted") + _rows("stakeholder", STK_01="Drafted"),
        )
        _commit_all(root, "seed: the needs", T_BASE)
        _write(
            root,
            NEEDS,
            _rows("need", SN_001="Approved") + _rows("stakeholder", STK_01="Approved"),
        )
        sha = _commit_all(root, _trailered("loop: approve the needs"), T_BASE + 1)
        findings = ctraj.loop_held_status_findings(root)
        if not held:
            assert findings == [], findings
            continue
        assert len(findings) == 2, findings
        assert sum("SN-001" in f for f in findings) == 1, findings
        assert sum("STK-01" in f for f in findings) == 1, findings
        assert all(sha[:10] in f and "DevStg-Needs" in f for f in findings)


def test_the_needs_file_is_read_at_the_needs_rung_by_the_authority_alone():
    # The authority judgement reads both of the needs file's tiers at
    # DevStg-Needs; the mint's own table, which decides which Drafted rows a
    # merge hands an adjudicator, is left exactly as it was.
    assert authority.rung_for(NEEDS) == ladder.STAGE_NEEDS
    assert authority.rung_for("docs/requirements/stakeholder-needs") == (
        ladder.STAGE_NEEDS
    )
    assert "docs/requirements/stakeholder-needs" not in authority.SPINE_APPROVAL_RUNGS


def test_the_live_dial_reads_every_legacy_spelling_silently_from_a_chosen_tree(
    tmp_path, capsys
):
    root = _bare(tmp_path / "dials")
    cases = (
        ('[attestation]\nhuman_approval_through = "DevStg-Arch"\n', "DevStg-Arch"),
        # the retired 0-4 ordinal, translated rather than guessed
        ("[attestation]\nhuman_approval_through = 1\n", "DevStg-Boundary"),
        # the retired key name
        ('[attestation]\nhuman_ratification_through = "DevStg-Reqs"\n', "DevStg-Reqs"),
        # the retired enum, where no dial is declared at all
        ('[attestation]\ngate_policy = "autonomous"\n', "DevStg-Below"),
        # a value no reader recognises, and no policy at all: the most held
        ('[attestation]\nhuman_approval_through = "devstg-arch"\n', "DevStg-Release"),
        ("", "DevStg-Release"),
    )
    for i, (text, rung) in enumerate(cases):
        _write(root, POLICY, text)
        sha = _commit_all(root, "dial {}".format(i), T_BASE + i)
        assert authority.dial_at(root, sha) == rung, text
        assert authority.dial_at(root, "HEAD") == rung, text
    # The retired one-word FILE, where the policy file says nothing.
    _write(root, POLICY, "[policies]\nreview_rounds = 0\n")
    _write(root, "docs/gate-policy", "# the old enum\nsingle-approve\n")
    _commit_all(root, "the old gate-policy file", T_LATER)
    assert authority.dial_at(root, "HEAD") == "DevStg-Below"
    # An explicitly chosen tree: the index answers for itself.
    _write(root, POLICY, "[attestation]\nhuman_approval_through = 1\n")
    _git(root, "add", "--", POLICY)
    assert authority.dial_at(root, None) == "DevStg-Boundary"
    assert authority.dial_at(root, "HEAD") == "DevStg-Below"
    out = capsys.readouterr()
    assert out.out == "" and out.err == "", out  # silent, every time
    # The live reader of the working tree gives the same rung; its migration
    # note is presentation, printed by it alone.
    assert ac.approval_through(root / "docs") == "DevStg-Boundary"
    assert "RETIRED" in capsys.readouterr().err
