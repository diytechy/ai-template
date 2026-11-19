"""The loop's review gate and its commit-check failure cap (WI-958).

A managed worker draws a review only over a tip whose declared commit checks
are recorded as passed. Failing checks draw no review: the failure is recorded in the build's
committed session log, keyed by the build commit, and the next build carries
the checks' failure tail. The failure count lives in those committed logs, so it
survives a resume and resets at a verified passed-checks record; at
`[build] stop_lane_after_consecutive_commit_check_failures` consecutive failures
the worker ends with its own exit code, and the dispatcher closes the lane
partial (`tests/test_dispatch.py`).

Driven end to end against a fake CLI that plays builder, reviewer and
adjudicator, on the topology a dispatched worker meets: the train branch in
a linked lane worktree, `main` in the primary, stand-in commit checks declared
in `docs/stack.ini` and named in `docs/process.toml`
(`conftest.declare_commit_checks`). Every case runs the real loop as a
subprocess, so the module is filed in `SLOW_MODULES`; the family's in-process
pins are the setting's reader in `tests/test_process_config.py` and the count
reader, called in-process here against the committed logs.
"""

import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from conftest import (
    COMMIT_SUITE,
    SCRIPTS,
    claim_on_branch,
    declare_commit_checks,
    declare_stack_key,
    declare_trunk,
    hooks_on,
    lane_checkout,
    load_script,
    pin_autocrlf,
    run_py,
    seed_row,
    write_wi_registry,
)

agent_loop = load_script("agent_loop")
dispatch = load_script("dispatch")
wi_convert = load_script("wi_convert")
# Imported after `load_script` has put scripts/ on sys.path.
from kitlib import verdict as kverdict  # noqa: E402

TRAIN = "llm/train/t1"

# The fake CLI. It records the model and prompt it was handed, then acts by
# role. An adjudicator (its brief names the INDEPENDENT adjudicator) writes the
# scripted typed verdict and commits with the row's trailer. A reviewer (its
# brief names a verdict path) writes the next scripted verdict body and
# commits. Anything else builds: before committing, the n-th build sets the
# stand-in checks to fail or pass from `checks_plan` (one R or G per build), commits
# `work.txt` with the WI trailer and records its sha; under `code_work` it
# writes `src/work.py` beside it; under `record_last` it then commits a
# record-only log fragment on top; under `no_commit` it records the launch and
# commits nothing.
FAKE = r"""
import argparse, json, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)


def append(name, text):
    with open(str(ctl / name), "a", encoding="utf-8") as fh:
        fh.write(text)


def commit(msg):
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


append("models.txt", args.model + "\n")
append("prompts.txt", "=== " + args.model + " ===\n" + args.prompt + "\n")
verdict = re.search(r"Write your verdict to (\S+)", args.prompt)
if "INDEPENDENT adjudicator" in args.prompt:
    vpath = pathlib.Path(verdict.group(1).rstrip(":."))
    wi = re.search(r"trailer .WI: (WI-\d+).", args.prompt).group(1)
    line = (ctl / "adjudication").read_text(encoding="utf-8").strip()
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text("- [MINOR] the claim -> why -> the change\n" + line + "\n",
                     encoding="utf-8")
    commit("adjudication verdict\n\nWI: " + wi + "\n")
elif verdict:
    queue = ctl / "verdicts.json"
    bodies = json.loads(queue.read_text(encoding="utf-8")) if queue.exists() else []
    body = bodies.pop(0) if bodies else "VERDICT: APPROVE findings=0\n"
    queue.write_text(json.dumps(bodies), encoding="utf-8")
    vpath = pathlib.Path(verdict.group(1))
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text(body, encoding="utf-8")
    commit("review verdict")
else:
    builds = ctl / "builds.txt"
    n = len(builds.read_text(encoding="utf-8").splitlines()) if builds.exists() else 0
    append("builds.txt", "b\n")
    if (ctl / "no_commit").exists():
        sys.exit(0)
    plan = (ctl / "checks_plan").read_text(encoding="utf-8").strip() \
        if (ctl / "checks_plan").exists() else ""
    if n < len(plan):
        red = ctl / "checks_fail"
        if plan[n] == "R":
            red.write_text("on\n", encoding="utf-8")
        elif red.exists():
            red.unlink()
    pathlib.Path("work.txt").write_text("build " + str(n), encoding="utf-8")
    if (ctl / "code_work").exists():
        pathlib.Path("src").mkdir(exist_ok=True)
        pathlib.Path("src/work.py").write_text("n = " + str(n) + "\n",
                                               encoding="utf-8")
    commit("build " + str(n) + "\n\nWI: WI-201")
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                         text=True, check=True).stdout.strip()
    append("build_shas.txt", sha + "\n")
    if (ctl / "record_last").exists():
        fragment = pathlib.Path("docs/log.d/build-" + str(n) + ".md")
        fragment.parent.mkdir(parents=True, exist_ok=True)
        fragment.write_text("- build " + str(n) + "\n", encoding="utf-8")
        commit("log: build " + str(n) + "\n\nWI: WI-201")
sys.exit(0)
"""

STATUS_MD = "# Status\n\n## Current State\n\n- **Open items:** none\n"

CHANGES_REQUESTED = (
    "- [MAJOR] work.txt:1 -> broken -> fix -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)

_CHECKS_FAILED_RE = re.compile(r"^# checks-failed:[ \t]*([0-9a-f]{40})[ \t]*$", re.M)
_PHASE_RE = re.compile(r"^# phase:[ \t]*(.*)$", re.M)
_SCOPE_RE = re.compile(r"^# review-scope:[ \t]*\S+[ \t]+\S+\.\.([0-9a-f]{40})", re.M)


def _git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _wi_201():
    return [
        "WI-201",
        "Scoped work for WI-201",
        "ws",
        "",
        "",
        "queued",
        "",
        "",
        "medium",
        "ordinary",
    ]


def _lane(tmp_path, rows=None):
    """A managed-routing repo whose train branch is checked out in a linked
    lane worktree, with the stand-in commit checks declared and WI-201 queued
    (or `rows`, written through `rows(repo)`). Returns `(lane, ctl, cmd)`;
    nothing is committed past the seed until `_configure`."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (repo / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    if rows is None:
        write_wi_registry(repo, [_wi_201()])
    else:
        rows(repo)
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    _git(repo, "init")
    hooks_on(repo)
    pin_autocrlf(repo)
    _git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    declare_trunk(repo)
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    # The worker records from its claimed lane (WI-960); `_configure` moves
    # trunk to the lane's tip, so the claim rides the branch.
    lane = claim_on_branch(lane_checkout(repo, TRAIN))

    ctl = tmp_path / "control"
    ctl.mkdir()
    declare_commit_checks(lane, ctl)
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows_csv = [
        ["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, ""],
        ["PROVB-REV-1", "PROVB", "revb", "1", "medium", cmd, ""],
        ["PROVC-REV-1", "PROVC", "revc", "1", "medium", cmd, ""],
        ["PROVA-STRONG-1", "PROVA", "stronga", "1", "strong", cmd, ""],
    ]
    with open(
        str(lane / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows_csv)
    (lane / "docs" / "agents-enabled").write_text(
        "PROVA-BUILD-1\nPROVB-REV-1\nPROVC-REV-1\nPROVA-STRONG-1\n", encoding="utf-8"
    )
    (lane / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    return lane, ctl, cmd


def _configure(lane, toml=""):
    """Append `toml` to the lane's `docs/process.toml`, commit the
    configuration and move `main` up to it: the lane's starting point, so its
    integration base sits after it."""
    if toml:
        with (lane / "docs" / "process.toml").open(
            "a", encoding="utf-8", newline="\n"
        ) as fh:
            fh.write(toml)
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "--allow-empty", "-m", "test config")
    _git(lane, "update-ref", "refs/heads/main", "HEAD")


# The commit-check failure cap's key, under `[build]`.
CAP_KEY = "stop_lane_after_consecutive_commit_check_failures"
# The stop banner's label: the count's words follow a dash.
CAP_BANNER = "COMMIT-CHECK FAILURE CAP"


def _cap(value, key=CAP_KEY):
    return "\n[build]\n{} = {}\n".format(key, value)


def _capped(count):
    """The words the stop banner counts the lane's failed rounds in."""
    return "{} consecutive failed rounds".format(count)


def _set_cap(lane, value):
    """Rewrite the declared cap and commit it."""
    path = lane / "docs" / "process.toml"
    text, found = re.subn(
        r"(?m)^{} = .*$".format(CAP_KEY),
        "{} = {}".format(CAP_KEY, value),
        path.read_text(encoding="utf-8"),
    )
    assert found == 1, text
    path.write_text(text, encoding="utf-8", newline="\n")
    _git(lane, "commit", "-q", "-am", "the cap, re-declared")


def _run(lane, cmd, iterations, *extra, wi="WI-201"):
    """The real worker loop on the lane; nothing is committed first."""
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            lane,
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            str(iterations),
            "--wi",
            wi,
            "--train",
            "t1",
            *extra,
        ],
        cwd=lane,
    )


def _lines(ctl, name):
    path = ctl / name
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def _out(proc):
    return proc.stdout + proc.stderr


def _hand_build(lane, ctl, red, rel="work.txt"):
    """A build commit carrying the WI trailer, with no passed-checks record and no
    failed-checks record: the state a run stopped between the build and its checks leave.
    Returns its sha."""
    if red:
        (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    (lane / rel).parent.mkdir(parents=True, exist_ok=True)
    (lane / rel).write_text("built by hand\n", encoding="utf-8")
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "-m", "build by hand\n\nWI: WI-201")
    return _git(lane, "rev-parse", "HEAD")


def _committed_logs(lane):
    """`{path: text}` for every session log in the lane's HEAD tree."""
    listed = _git(lane, "ls-tree", "-r", "--name-only", "HEAD", "--", "docs/iteration")
    return {
        path: _git(lane, "show", "HEAD:" + path)
        for path in listed.splitlines()
        if path.endswith(".log")
    }


def _phase(text):
    found = _PHASE_RE.search(text)
    return found.group(1).strip() if found else ""


def _red_count(lane):
    return kverdict.failed_rounds(str(lane), "HEAD", "main")


def _build_prompts(ctl):
    text = (ctl / "prompts.txt").read_text(encoding="utf-8")
    return text.split("=== builda ===\n")[1:]


# --- D2 and D3: the gate at the event ------------------------------------------


def test_failed_checks_draw_no_review_record_a_failed_round_and_rebuild_with_the_tail(
    tmp_path,
):
    """Implements: TC-375"""
    # TC-375. A committed build whose commit checks fail draws no review: the
    # failure is written into that build's committed session log, keyed by its
    # sha, and the next build's prompt carries the checks' failure tail.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    _configure(lane)

    proc = _run(lane, cmd, 2)

    models = _lines(ctl, "models.txt")
    assert "revb" not in models and "revc" not in models, _out(proc)
    assert not list((lane / "docs" / "reviews").rglob("*-REVIEW-A-*.md"))
    first = _lines(ctl, "build_shas.txt")[0]
    reds = [
        sha
        for text in _committed_logs(lane).values()
        if _phase(text) == "BUILD"
        for sha in _CHECKS_FAILED_RE.findall(text)
    ]
    assert first in reds, _out(proc)
    prompts = _build_prompts(ctl)
    assert len(prompts) >= 2, _out(proc)
    assert "CHECKS-FAIL-MARKER" in prompts[1]


LONG_CHECKS = r"""
import pathlib, sys
ctl = pathlib.Path(sys.argv[1])
with open(str(ctl / "check_runs.txt"), "a", encoding="utf-8") as fh:
    fh.write("run\n")
print("context " * 80 + "ACTIONABLE-END-DIAGNOSTIC")
sys.exit(1)
"""


def test_a_resumed_build_receives_the_tail_of_a_long_recorded_refusal(tmp_path):
    """Implements: TC-375"""
    # TC-375. failing checks whose output runs far past the recorded summary's
    # bound, its diagnostic last: a fresh process resuming the lane reads the
    # failure from the committed record alone, and the build it routes still
    # receives that final diagnostic.
    lane, ctl, cmd = _lane(tmp_path)
    script = ctl / "long_checks.py"
    script.write_text(LONG_CHECKS, encoding="utf-8")
    stack = lane / "docs" / "stack.ini"
    declared = '"{}" "{}" "{}"'.format(
        Path(sys.executable).as_posix(), script.as_posix(), ctl.as_posix()
    )
    text, found = re.subn(
        r"(?m)^{} = .*$".format(COMMIT_SUITE),
        lambda _m: "{} = {}".format(COMMIT_SUITE, declared),
        stack.read_text(encoding="utf-8"),
    )
    assert found == 1, text
    stack.write_text(text, encoding="utf-8", newline="\n")
    _configure(lane, _cap(5))
    first = _run(lane, cmd, 1)
    seen = len(_build_prompts(ctl))
    (ctl / "no_commit").write_text("on\n", encoding="utf-8")

    second = _run(lane, cmd, 1)

    assert len(_lines(ctl, "check_runs.txt")) == 1, _out(first) + _out(second)
    resumed = _build_prompts(ctl)[seen:]
    assert resumed, _out(second)
    assert "ACTIONABLE-END-DIAGNOSTIC" in resumed[0], resumed[0]
    assert _red_count(lane).count == 1


def test_passed_commit_checks_are_recorded_once_then_the_review_is_drawn(tmp_path):
    """Implements: TC-376"""
    # TC-376. A committed build whose commit checks pass gets exactly one
    # `commit` record commit, and the review round is drawn after it.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)

    proc = _run(lane, cmd, 4)

    assert proc.returncode == agent_loop.EXIT_DONE, _out(proc)
    passed = [
        (sha, kverdict.passed_checks(str(lane), sha))
        for sha in _git(lane, "rev-list", "main..HEAD").split()
    ]
    passed = [(sha, rec) for sha, rec in passed if rec is not None]
    assert len(passed) == 1, _out(proc)
    sha, rec = passed[0]
    assert (rec.checks, rec.tests) == ("commit", "none")
    verdict_commit = _git(
        lane, "log", "-1", "--format=%H", "--diff-filter=A", "--", "docs/reviews"
    )
    older = subprocess.run(
        ["git", "-C", str(lane), "merge-base", "--is-ancestor", sha, verdict_commit],
        capture_output=True,
    )
    assert older.returncode == 0 and sha != verdict_commit, (sha, verdict_commit)
    assert len(_lines(ctl, "check_runs.txt")) == 1


# --- D4: every draw, one choke point --------------------------------------------


@pytest.mark.parametrize("outcome", ["passed", "failed"])
def test_resumed_round_on_an_unrecorded_tip_runs_the_producer_once(tmp_path, outcome):
    """Implements: TC-377"""
    # TC-377. A resumed lane whose committed build owes a round but carries no
    # passed-checks record runs the commit checks once at the draw: a pass draws the round
    # and a CHECKS log records the result, a failure draws no reviewer.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)
    _hand_build(lane, ctl, red=(outcome == "failed"))
    if outcome == "failed":
        (ctl / "no_commit").write_text("on\n", encoding="utf-8")

    proc = _run(lane, cmd, 2)

    assert len(_lines(ctl, "check_runs.txt")) == 1, _out(proc)
    models = _lines(ctl, "models.txt")
    if outcome == "passed":
        # The hand build left no session log, so no builder family is known
        # and the reviewer is any medium entry: the round is its REVIEW log.
        logs = _committed_logs(lane).values()
        assert any(_phase(t) == "REVIEW-A" for t in logs), _out(proc)
        checks_logs = [t for t in logs if _phase(t) == "CHECKS"]
        assert len(checks_logs) == 1, _out(proc)
        assert not _CHECKS_FAILED_RE.search(checks_logs[0])
    else:
        assert "revb" not in models and "revc" not in models, _out(proc)


def _adjudication_rows(repo):
    """WI-300 closed partial, and WI-301 the disposition row judging it."""
    work = repo / "docs" / "work"
    work.mkdir(parents=True, exist_ok=True)
    for cells in (
        {"WI-ID": "WI-300", "Title": "the whole ask", "Status": "partial"},
        {
            "WI-ID": "WI-301",
            "Title": "dispose: the close recorded at docs/handbacks/",
            "SafetyClass": "adjudication",
            "Brief": "disposition",
            "SpecRef": "docs/work/partial/WI-300-the-whole-ask.md",
            "Status": "queued",
        },
    ):
        row = {column: "" for column in wi_convert.COLUMNS}
        row.update(cells)
        wi_convert.write_spec_file(work, row)


def _post_narrow_round(tmp_path):
    """CHANGES-REQUESTED, a passing rework, a narrow APPROVE and the fresh full
    round. Returns `(lane, ctl, proc)`."""
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "verdicts.json").write_text(
        json.dumps([CHANGES_REQUESTED, "VERDICT: APPROVE findings=0\n"]),
        encoding="utf-8",
    )
    _configure(lane)
    return lane, ctl, _run(lane, cmd, 8)


def _adjudication_round(tmp_path):
    """A committing ADJUDICATE session whose dial owes a review round.
    Returns `(lane, ctl, proc)`."""
    lane, ctl, cmd = _lane(tmp_path, rows=_adjudication_rows)
    (ctl / "adjudication").write_text("OUTCOME: PARTIAL successors=1\n", "utf-8")
    # The per-close report the disposition brief is built around; its typed
    # range names the seed, and an empty range composes.
    seed = _git(lane, "rev-parse", "--short=10", "HEAD")
    reports = lane / "docs" / "handbacks"
    reports.mkdir(parents=True)
    (reports / "WI-300-lane.md").write_text(
        "+++\n"
        'wi = "WI-300"\n'
        'branch = "lane"\n'
        'claimed_outcome = "partial"\n'
        'reason = "ran out of runway"\n'
        'commit_range = "{0}..{0}"\n'
        'suggested_tier = "medium"\n'
        "keep_commits = []\n"
        "discard_commits = []\n"
        'split_decided_by = "lane"\n'
        "+++\n\n## What happened\n\nDelivered half of it.\n".format(seed),
        encoding="utf-8",
    )
    _configure(lane, '\n[authority]\nadjudication_review = "always"\n')
    return lane, ctl, _run(lane, cmd, 4, wi="WI-301")


@pytest.mark.parametrize("route", ["post-narrow", "adjudication"])
def test_post_narrow_and_adjudication_rounds_draw_only_over_a_verified_passed_checks_record(
    tmp_path, route
):
    """Implements: TC-377"""
    # TC-377. The rounds `complete_review_round` and
    # `schedule_adjudication_round` queue pass the same draw: every review
    # session's reviewed commit carries a verified `commit` record, and
    # the narrow-to-full transition runs no checks of its own.
    make = _post_narrow_round if route == "post-narrow" else _adjudication_round
    lane, ctl, proc = make(tmp_path)

    reviewed = [
        _SCOPE_RE.search(text).group(1)
        for text in _committed_logs(lane).values()
        if _phase(text) in kverdict.REVIEW_PHASES and _SCOPE_RE.search(text)
    ]
    assert reviewed, _out(proc)
    if route == "post-narrow":
        assert len(reviewed) >= 3, _out(proc)
    for sha in reviewed:
        passed, cause = kverdict.commit_passed_checks(str(lane), sha, [])
        assert passed is not None, cause
    builds = len(_lines(ctl, "builds.txt"))
    assert len(_lines(ctl, "check_runs.txt")) == (builds or 1), _out(proc)


# --- D5: the count survives a resume; the cap -----------------------------------


def test_the_failure_count_survives_a_resume_and_a_pass_resets_it(tmp_path):
    """Implements: TC-378"""
    # TC-378. The failure count is read from the lane's committed logs: a fresh
    # process continues it, and its first build carries the recorded failure
    # tail. A verified passed-checks record resets it.
    lane, ctl, cmd = _lane(tmp_path / "a")
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(5))
    first = _run(lane, cmd, 2)
    seen = len(_build_prompts(ctl))
    second = _run(lane, cmd, 1)

    assert _red_count(lane).count == 3, _out(first) + _out(second)
    resumed = _build_prompts(ctl)[seen:]
    assert resumed and "CHECKS-FAIL-MARKER" in resumed[0], _out(second)

    # failing, passing (its round asks for changes), failing, failing: two since the pass.
    lane, ctl, cmd = _lane(tmp_path / "b")
    (ctl / "checks_plan").write_text("RGRR\n", encoding="utf-8")
    (ctl / "verdicts.json").write_text(json.dumps([CHANGES_REQUESTED]), "utf-8")
    _configure(lane, _cap(5))
    proc = _run(lane, cmd, 5)
    assert _red_count(lane).count == 2, _out(proc)


def test_the_failure_count_survives_a_resume_to_the_cap_and_exits_12(tmp_path):
    """Implements: TC-378"""
    # TC-378. Two failures in one run and a third in a fresh process reach a cap
    # of 3: the resumed worker ends with the cap's own code and banner.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(3))
    _run(lane, cmd, 2)

    proc = _run(lane, cmd, 1)

    assert proc.returncode == 12, _out(proc)
    assert CAP_BANNER in proc.stdout and _capped(3) in proc.stdout


@pytest.mark.parametrize("reds", ["at-the-cap", "one-fewer"])
def test_a_lane_resumed_at_the_cap_exits_12_before_any_session(tmp_path, reds):
    """Implements: TC-378, TC-381"""
    # TC-378, TC-381. A lane resumed with the cap's count of failed-checks records
    # already committed (a stop after the record and before the exit) ends at
    # run start: no builder, reviewer or checks run and nothing is committed,
    # whatever round its committed trailer owes. One failure fewer is no cap: the
    # resumed run launches a build (one that commits nothing, so it records no
    # further failure); its run is given one session, since a build that commits
    # nothing does not end the run and a second session would build again.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    if reds == "at-the-cap":
        _configure(lane, _cap(5))
        _run(lane, cmd, 3)
        _set_cap(lane, 3)
    else:
        _configure(lane, _cap(3))
        _run(lane, cmd, 2)
        (ctl / "no_commit").write_text("on\n", encoding="utf-8")
    models, runs = _lines(ctl, "models.txt"), _lines(ctl, "check_runs.txt")
    builds = len(_lines(ctl, "builds.txt"))
    commits = _git(lane, "rev-list", "--count", "HEAD")

    proc = _run(lane, cmd, 2 if reds == "at-the-cap" else 1)

    if reds == "at-the-cap":
        assert proc.returncode == 12, _out(proc)
        assert CAP_BANNER in proc.stdout and _capped(3) in proc.stdout
        assert _lines(ctl, "models.txt") == models
        assert _lines(ctl, "check_runs.txt") == runs
        assert _git(lane, "rev-list", "--count", "HEAD") == commits
    else:
        assert proc.returncode != 12, _out(proc)
        assert len(_lines(ctl, "builds.txt")) == builds + 1, _out(proc)
        assert "revb" not in _lines(ctl, "models.txt")[len(models) :]


# --- D6: an interrupted record --------------------------------------------------


def test_an_interrupted_failure_is_rechecked_once_at_the_draw_and_counted_once(
    tmp_path,
):
    """Implements: TC-379"""
    # TC-379. A build commit left with neither a passed-checks record nor a failed-checks record
    # is re-checked once at the next draw, and the CHECKS log records its failure;
    # the same failure recorded twice for one build commit counts once.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)
    build = _hand_build(lane, ctl, red=True)
    (ctl / "no_commit").write_text("on\n", encoding="utf-8")

    proc = _run(lane, cmd, 1)

    assert len(_lines(ctl, "check_runs.txt")) == 1, _out(proc)
    checks_logs = [t for t in _committed_logs(lane).values() if _phase(t) == "CHECKS"]
    assert any(build in _CHECKS_FAILED_RE.findall(t) for t in checks_logs), _out(proc)

    # The same failure, recorded a second time in a log of its own.
    again = lane / "docs" / "iteration" / "t1-090-20261021-000000.log"
    again.write_text(
        "# agent session log\n# session: 090\n# train: t1\n# phase: CHECKS\n"
        "# outcome: FAILED\n# checks-failed: {}\n# checks-summary: CHECKS-FAIL-MARKER\n".format(
            build
        ),
        encoding="utf-8",
    )
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "-m", "telemetry: the failure, recorded twice")
    assert _red_count(lane).count == 1


def test_a_build_ending_in_a_record_only_commit_is_recorded_and_counted_once(
    tmp_path,
):
    """Implements: TC-379"""
    # TC-379. A build session whose last commit touches only records (its log
    # fragment) is the same build commit at the event and at the draw: the failure
    # recorded at the event is found again on resume, so the checks do not run
    # twice for it and two failing builds count two.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    (ctl / "record_last").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(5))
    first = _run(lane, cmd, 1)
    second = _run(lane, cmd, 1)

    builds = _lines(ctl, "build_shas.txt")
    assert len(builds) == 2, _out(first) + _out(second)
    assert len(_lines(ctl, "check_runs.txt")) == 2, _out(first) + _out(second)
    keyed = {
        sha
        for text in _committed_logs(lane).values()
        for sha in _CHECKS_FAILED_RE.findall(text)
    }
    assert keyed == set(builds), (keyed, builds)
    assert _red_count(lane).count == 2


def test_checks_phase_is_inert_to_every_phase_reader(tmp_path):
    """Implements: TC-379"""
    # TC-379. The loop's own CHECKS log is no build for the heterogeneity key,
    # no review round for the round evidence, and still a session number.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)
    _hand_build(lane, ctl, red=False)
    iteration = lane / "docs" / "iteration"
    iteration.mkdir(parents=True, exist_ok=True)
    (iteration / "t1-001-20261021-000000.log").write_text(
        "# agent session log\n# session: 001\n# train: t1\n# phase: BUILD\n"
        "# model: builda\n# outcome: COMMITTED\n",
        encoding="utf-8",
    )
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "-m", "telemetry: the hand build's session log")

    proc = _run(lane, cmd, 2)

    logs = _committed_logs(lane)
    checks_logs = [path for path, text in logs.items() if _phase(text) == "CHECKS"]
    assert len(checks_logs) == 1, _out(proc)
    registry = {
        "PROVA-BUILD-1": SimpleNamespace(
            id="PROVA-BUILD-1", model="builda", family="PROVA"
        )
    }
    assert agent_loop.last_build_family(iteration, registry) == "PROVA"
    rounds = kverdict.review_logs(str(lane), "HEAD", "main", sorted(logs))
    assert checks_logs[0] not in [entry[0] for entry in rounds]
    ordinal = int(re.match(r"t1-(\d+)-", Path(checks_logs[0]).name).group(1))
    assert agent_loop.next_session_number(iteration, "t1") > ordinal


# --- D5 and D6: the count reader, in-process --------------------------------------


def _reader_lane(tmp_path):
    """A plain repository on a `t1` branch one commit past `main`, for the
    count reader alone: no loop, no worktree. Returns its path."""
    repo = tmp_path / "reader"
    repo.mkdir()
    _git(repo, "init", "-q")
    pin_autocrlf(repo)
    _git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / "work.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "checkout", "-q", "-b", "t1")
    return repo


def _reader_build(repo, n):
    """A build commit changing the work; returns its sha."""
    (repo / "work.txt").write_text("build {}\n".format(n), encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "build {}\n\nWI: WI-201".format(n))
    return _git(repo, "rev-parse", "HEAD")


def _reader_log(repo, n, phase, red=None):
    """One session log written and committed through the loop's own writer;
    `red` is `(build sha, summary)` for a failed-checks record."""
    meta = {
        "session": "{:03d}".format(n),
        "stamp": "20261021-0000{:02d}".format(n),
        "train": "t1",
        "phase": phase,
        "outcome": "FAILED" if red else "COMMITTED",
    }
    if red:
        meta.update(kverdict.format_failed_record(*red))
    agent_loop.agent_common.write_session_log(
        repo / "docs" / "iteration", meta, "transcript\n# checks-failed: " + "f" * 40
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "telemetry: session {}".format(n))


def _reader_green(repo):
    """An empty commit carrying a verified `commit` record of the tip."""
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    work = _git(repo, "rev-parse", "HEAD")
    line = kverdict.format_passed_checks(tree, work, "commit", "none", "passed")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "record-checks\n\n" + line)


def test_failed_rounds_counts_distinct_failed_builds_and_a_passed_checks_record_resets_it(
    tmp_path,
):
    """Implements: TC-378"""
    # TC-378. The count is read from the committed logs alone, so a fresh
    # process reads what an earlier one recorded; the newest verified commit
    # record resets it, and the last summary is the newest failure's.
    repo = _reader_lane(tmp_path)
    first = _reader_build(repo, 1)
    _reader_log(repo, 1, "BUILD", (first, "checks failed:\n  one"))
    second = _reader_build(repo, 2)
    _reader_log(repo, 2, "BUILD", (second, "checks failed: two"))

    counted = kverdict.failed_rounds(str(repo), "t1", "main")
    assert counted == kverdict.FailedCount(2, "checks failed: two")

    _reader_build(repo, 3)
    _reader_green(repo)
    _reader_log(repo, 3, "BUILD")
    assert kverdict.failed_rounds(str(repo), "t1", "main").count == 0

    fourth = _reader_build(repo, 4)
    _reader_log(repo, 4, "BUILD", (fourth, "checks failed: four"))
    assert kverdict.failed_rounds(str(repo), "t1", "main") == kverdict.FailedCount(
        1, "checks failed: four"
    )


def test_a_long_failure_summary_keeps_its_cause_and_its_final_diagnostic():
    """Implements: TC-375"""
    # TC-375. The one persisted summary of a failing result is bounded, and a
    # refusal longer than the bound keeps both ends: the cause at its head and
    # the diagnostic a check run prints last. A short one is kept whole.
    sha = "a" * 40
    refusal = (
        "record-checks REFUSED - CAUSE-AT-HEAD:\n" + "context\n" * 80 + "FINAL-LINE"
    )
    fields = kverdict.format_failed_record(sha, refusal)
    line = fields["checks-summary"]
    assert len(line) <= 240
    assert line.startswith("record-checks REFUSED - CAUSE-AT-HEAD:")
    assert line.endswith("context FINAL-LINE")
    assert kverdict.parse_failed_record(
        "# checks-failed: {}\n# checks-summary: {}\n# ---\n".format(sha, line)
    ) == (sha, line)
    short = kverdict.format_failed_record(sha, "checks failed:\n  one line")
    assert short["checks-summary"] == "checks failed: one line"


def test_a_header_in_the_earlier_form_is_not_a_failed_checks_record():
    """Implements: TC-379"""
    # TC-379. The vocabulary cut (2026-11-16): the record was once written
    # `# bar-red:` / `# bar-summary:`. A header in that form is no record, so
    # a log holding one counts toward nothing and the failure count restarts
    # at the cut, as the passed-checks record that would reset it is cut too.
    sha = "b" * 40
    old = "# bar-red: {}\n# bar-summary: checks failed\n# ---\n".format(sha)
    assert kverdict.parse_failed_record(old) is None
    new = old.replace("# bar-red:", "# checks-failed:").replace(
        "bar-summary", "checks-summary"
    )
    assert kverdict.parse_failed_record(new) == (sha, "checks failed")


def test_failed_rounds_counts_one_build_recorded_twice_once(tmp_path):
    """Implements: TC-379"""
    # TC-379. A failure recorded for one build commit in two logs (the build's own
    # and a later re-check's) counts once; the record's grammar round-trips,
    # its summary folded to one line, and a transcript line is no record.
    repo = _reader_lane(tmp_path)
    build = _reader_build(repo, 1)
    _reader_log(repo, 1, "BUILD", (build, "checks failed:\n  one"))
    _reader_log(repo, 2, "CHECKS", (build, "checks failed: again"))
    _reader_log(repo, 3, "BUILD")

    assert kverdict.failed_rounds(str(repo), "t1", "main") == kverdict.FailedCount(
        1, "checks failed: again"
    )
    logs = sorted((repo / "docs" / "iteration").glob("*.log"))
    first = logs[0].read_text(encoding="utf-8")
    assert kverdict.parse_failed_record(first) == (build, "checks failed: one")
    assert kverdict.parse_failed_record(logs[2].read_text(encoding="utf-8")) is None


def test_failed_rounds_counts_an_unreadable_log_and_answers_none_for_no_history(
    tmp_path, monkeypatch
):
    """Implements: TC-378"""
    # TC-378. A log git cannot show counts as one failure keyed by its path,
    # toward the cap; a range git cannot list answers None.
    repo = _reader_lane(tmp_path)
    build = _reader_build(repo, 1)
    _reader_log(repo, 1, "BUILD", (build, "checks failed: one"))
    _reader_log(repo, 2, "BUILD")
    real = kverdict.git_out

    def no_show(root, args, stdin=None):
        return None if args[0] == "show" else real(root, args, stdin)

    monkeypatch.setattr(kverdict, "git_out", no_show)
    assert kverdict.failed_rounds(str(repo), "t1", "main").count == 2
    monkeypatch.setattr(kverdict, "git_out", real)

    assert kverdict.failed_rounds(str(repo), "t1", "no-such-base") is None


# --- the draw over the row's derived set (WI-995) --------------------------------

TEST_A = "tests/test_a.py"

NAMED_STUB = r"""
import json, pathlib, sys
pathlib.Path(sys.argv[1], "named_args.json").write_text(
    json.dumps(sys.argv[2:]), encoding="utf-8"
)
"""


def _row_lane(tmp_path, tags):
    """`_lane` with the claimed row naming SR-001, verified by TC-001 whose
    evidence is `TEST_A`, `tags` writing the test files, and a `[product] test`
    recording the files it is handed in `ctl/named_args.json`. Each build
    touches code. Returns `(lane, ctl, cmd)`."""
    lane, ctl, cmd = _lane(tmp_path)
    seed_row(
        lane,
        srs=["SR-001"],
        tcs={"TC-001": (["SR-001"], TEST_A)},
        tags=tags,
        sr_refs=["SR-001"],
    )
    stub = ctl / "named.py"
    stub.write_text(NAMED_STUB, encoding="utf-8")
    # `[product]` already holds the marker `_lane` declared: the key joins it.
    declare_stack_key(
        lane,
        "product",
        "test",
        '{{py}} "{}" "{}"'.format(stub.as_posix(), ctl.as_posix()),
    )
    (ctl / "code_work").write_text("on\n", encoding="utf-8")
    return lane, ctl, cmd


def _records(lane):
    """The verified passed-checks records on the lane, newest first."""
    found = [
        kverdict.passed_checks(str(lane), sha)
        for sha in _git(lane, "rev-list", "main..HEAD").split()
    ]
    return [rec for rec in found if rec is not None]


def _named_args(ctl):
    path = ctl / "named_args.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def test_a_code_lane_with_an_untagged_tc_draws_no_round(tmp_path):
    """Implements: TC-418"""
    lane, ctl, cmd = _row_lane(tmp_path, {TEST_A: []})
    _configure(lane, _cap(5))

    proc = _run(lane, cmd, 2)

    models = _lines(ctl, "models.txt")
    assert "revb" not in models and "revc" not in models, _out(proc)
    assert "partial" in _red_count(lane).last_summary, _out(proc)
    prompts = _build_prompts(ctl)
    assert len(prompts) >= 2 and "TC-001" in prompts[1], _out(proc)


def test_a_derivation_refusal_counts_toward_the_failure_cap(tmp_path):
    """Implements: TC-418"""
    lane, ctl, cmd = _row_lane(tmp_path, {TEST_A: []})
    _configure(lane, _cap(2))

    proc = _run(lane, cmd, 3)

    assert proc.returncode == 12, _out(proc)
    assert CAP_BANNER in proc.stdout, _out(proc)
    assert _red_count(lane).count == 2, _out(proc)


def test_the_draw_runs_the_derived_files_and_compares_their_digest(tmp_path):
    """Implements: TC-418"""
    # The tip carries a verified record for no tests, which is not this row's
    # set, so the draw records the checks again rather than trusting it.
    lane, ctl, cmd = _row_lane(tmp_path, {TEST_A: ["TC-001"]})
    _configure(lane)
    _hand_build(lane, ctl, red=False, rel="src/work.py")
    _reader_green(lane)

    proc = _run(lane, cmd, 2)

    assert len(_lines(ctl, "check_runs.txt")) == 1, _out(proc)
    assert TEST_A in _named_args(ctl), _out(proc)
    assert _records(lane)[0].tests == kverdict.tests_digest([TEST_A]), _out(proc)
    logs = _committed_logs(lane).values()
    assert any(_phase(text) == "REVIEW-A" for text in logs), _out(proc)


def test_a_closed_lane_draws_over_its_closed_copy(tmp_path):
    """Implements: TC-418"""
    lane, ctl, cmd = _row_lane(tmp_path, {TEST_A: ["TC-001"]})
    _configure(lane)
    claim = next((lane / "docs" / "work" / "active").rglob("WI-9-*.md"))
    closed = lane / "docs" / "archive" / "work" / "complete" / claim.name
    closed.parent.mkdir(parents=True)
    _git(lane, "mv", str(claim), str(closed))
    _hand_build(lane, ctl, red=False, rel="src/work.py")

    proc = _run(lane, cmd, 2)

    records = _records(lane)
    assert records and records[0].tests == kverdict.tests_digest([TEST_A]), _out(proc)


# --- D7 and D9: the setting is refused before any session -----------------------

_UNPARSEABLE = '[policies]\ntrunk = "main"\n[build\n{} = 3\n'.format(CAP_KEY)
_NON_TABLE = 'build = 3\n\n[policies]\ntrunk = "main"\n'
# The cap's key before it was renamed: refused where it is still declared.
RETIRED_CAP_KEY = "red_rounds_max"


@pytest.mark.parametrize(
    "text, cause",
    [
        pytest.param(_UNPARSEABLE, ("does not parse",), id="unparseable"),
        pytest.param(_NON_TABLE, ("build", "table"), id="non-table"),
    ],
)
def test_unparseable_process_toml_and_a_non_table_build_refuse_at_preflight(
    tmp_path, text, cause
):
    """Implements: TC-380"""
    # TC-380. A `docs/process.toml` that does not parse, and one whose `build`
    # is not a table, are refused by the worker's preflight (exit 2, no
    # session) and by the dispatcher's pre-claim rung, each naming the file
    # and the cause. The unparseable file is refused already, by the mixed-
    # config check both preflights run; its adequacy witness is a preflight
    # that reads past a file it cannot parse, which starts a session here.
    lane, ctl, cmd = _lane(tmp_path)
    (lane / "docs" / "process.toml").write_text(text, encoding="utf-8", newline="\n")
    _configure(lane)
    head = _git(lane, "rev-parse", "HEAD")

    proc = _run(lane, cmd, 2)

    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, _out(proc)
    for word in ("docs/process.toml", *cause):
        assert word in proc.stderr, proc.stderr
    assert not (ctl / "models.txt").exists()
    refusal = dispatch._session_config_refusal(
        lane, SimpleNamespace(agent_cmd="stub-agent")
    )
    for word in ("docs/process.toml", *cause):
        assert refusal and word in refusal, refusal
    assert _git(lane, "rev-parse", "HEAD") == head


@pytest.mark.parametrize(
    "key, value",
    [
        (CAP_KEY, "0"),
        (CAP_KEY, "-1"),
        (CAP_KEY, "true"),
        (CAP_KEY, '"3"'),
        (CAP_KEY, "3.0"),
        (RETIRED_CAP_KEY, "3"),
    ],
    ids=["0", "-1", "true", '"3"', "3.0", "retired-key"],
)
def test_a_bad_failure_cap_refuses_before_any_session(tmp_path, key, value):
    """Implements: TC-380"""
    # TC-380. A declared cap that is not an int, is a bool, or is below 1 is
    # refused at the loop's preflight, naming its line and the key, before any
    # session starts. So is a usable value still declared under the key's
    # retired name, which names the key to rename it to: read as absent, it
    # would start the session under the shipped cap instead.
    lane, ctl, cmd = _lane(tmp_path)
    path = lane / "docs" / "process.toml"
    line = len(path.read_text(encoding="utf-8").splitlines()) + 3
    _configure(lane, _cap(value, key))

    proc = _run(lane, cmd, 2)

    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, _out(proc)
    assert "docs/process.toml:{}".format(line) in proc.stderr, proc.stderr
    assert CAP_KEY in proc.stderr
    if key == RETIRED_CAP_KEY:
        renamed = "[build] {} was renamed {}".format(RETIRED_CAP_KEY, CAP_KEY)
        assert renamed in proc.stderr, proc.stderr
    assert not (ctl / "models.txt").exists()


# --- D8: the worker's cap -------------------------------------------------------


def test_failure_cap_exits_with_its_own_code_and_one_fewer_does_not(tmp_path):
    """Implements: TC-381"""
    # TC-381. Two consecutive failures under a cap of 2 end the worker with exit
    # 12 and the cap's stop banner, which names the count, the declared key
    # and its value; the same two failures under a cap of 3 end on
    # the iteration budget instead. The cap closes partial rather than
    # escalating through the declared acceptance level: the worker never
    # consults the page ladder (no failure-action line, no PAGE-OPERATOR stop)
    # and its exit is not the NEEDS-OPERATOR code. A cap that paged the operator
    # first, then exited 12 whatever the hold decided, fails here.
    lane, ctl, cmd = _lane(tmp_path / "capped")
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(2))
    proc = _run(lane, cmd, 2)
    assert proc.returncode == 12, _out(proc)
    assert CAP_BANNER in proc.stdout and _capped(2) in proc.stdout
    assert "[build] {} = 2; last run: ".format(CAP_KEY) in proc.stdout, _out(proc)
    assert "The lane closes partial." in proc.stdout, _out(proc)
    assert "route/failure" not in proc.stdout, _out(proc)
    assert "PAGE-OPERATOR" not in proc.stdout, _out(proc)

    lane, ctl, cmd = _lane(tmp_path / "below")
    (ctl / "checks_fail").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(3))
    proc = _run(lane, cmd, 2)
    assert proc.returncode == agent_loop.EXIT_BUDGET, _out(proc)
    assert CAP_BANNER not in proc.stdout
