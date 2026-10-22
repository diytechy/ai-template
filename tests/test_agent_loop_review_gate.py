"""The loop's review gate and its red-round cap (WI-958).

A managed worker draws a review only over a tip its declared review bar
attested green. A red bar draws no review: the red is recorded in the build's
committed session log, keyed by the build commit, and the next build carries
the bar's failure tail. The red count lives in those committed logs, so it
survives a resume and resets at a verified green attestation; at
`[build] red_rounds_max` consecutive reds the worker ends with its own exit
code, and the dispatcher closes the lane partial
(`tests/test_dispatch.py`).

Driven end to end against a fake CLI that plays builder, reviewer and
adjudicator, on the topology a dispatched worker meets: the train branch in
a linked lane worktree, `main` in the primary, a stand-in review bar declared
in `docs/stack.ini` (`conftest.declare_review_bar`). Every case runs the real
loop as a subprocess, so the module is filed in `SLOW_MODULES`; the family's
in-process pins are the setting's reader in `tests/test_process_config.py`
and the count reader, called in-process here against the committed logs.
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
    SCRIPTS,
    claim_on_branch,
    declare_review_bar,
    declare_trunk,
    hooks_on,
    lane_checkout,
    load_script,
    pin_autocrlf,
    run_py,
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
# stand-in bar red or green from `bar_plan` (one R or G per build), commits
# `work.txt` with the WI trailer and records its sha; under `record_last` it
# then commits a record-only log fragment on top; under `no_commit` it records
# the launch and commits nothing.
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
    plan = (ctl / "bar_plan").read_text(encoding="utf-8").strip() \
        if (ctl / "bar_plan").exists() else ""
    if n < len(plan):
        red = ctl / "bar_red"
        if plan[n] == "R":
            red.write_text("on\n", encoding="utf-8")
        elif red.exists():
            red.unlink()
    pathlib.Path("work.txt").write_text("build " + str(n), encoding="utf-8")
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

_BAR_RED_RE = re.compile(r"^# bar-red:[ \t]*([0-9a-f]{40})[ \t]*$", re.M)
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
    lane worktree, with the stand-in review bar declared and WI-201 queued
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
    declare_review_bar(lane, ctl)
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


def _cap(value):
    return "\n[build]\nred_rounds_max = {}\n".format(value)


def _set_cap(lane, value):
    """Rewrite the declared `red_rounds_max` and commit it."""
    path = lane / "docs" / "process.toml"
    text = re.sub(
        r"(?m)^red_rounds_max = .*$",
        "red_rounds_max = {}".format(value),
        path.read_text(encoding="utf-8"),
    )
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


def _hand_build(lane, ctl, red):
    """A build commit carrying the WI trailer, with no attestation and no red
    record: the state a run stopped between the build and its bar leaves.
    Returns its sha."""
    if red:
        (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    (lane / "work.txt").write_text("built by hand\n", encoding="utf-8")
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
    return kverdict.red_rounds(str(lane), "HEAD", "main")


def _build_prompts(ctl):
    text = (ctl / "prompts.txt").read_text(encoding="utf-8")
    return text.split("=== builda ===\n")[1:]


# --- D2 and D3: the gate at the event ------------------------------------------


def test_red_bar_draws_no_review_records_a_red_round_and_rebuilds_with_the_tail(
    tmp_path,
):
    # TC-375. A committed build whose review bar is red draws no review: the
    # red is written into that build's committed session log, keyed by its
    # sha, and the next build's prompt carries the bar's failure tail.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
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
        for sha in _BAR_RED_RE.findall(text)
    ]
    assert first in reds, _out(proc)
    prompts = _build_prompts(ctl)
    assert len(prompts) >= 2, _out(proc)
    assert "BAR-FAIL-MARKER" in prompts[1]


LONG_BAR = r"""
import pathlib, sys
ctl = pathlib.Path(sys.argv[1])
with open(str(ctl / "bar_runs.txt"), "a", encoding="utf-8") as fh:
    fh.write("run\n")
print("context " * 80 + "ACTIONABLE-END-DIAGNOSTIC")
sys.exit(1)
"""


def test_a_resumed_build_receives_the_tail_of_a_long_recorded_refusal(tmp_path):
    # TC-375. A red bar whose output runs far past the recorded summary's
    # bound, its diagnostic last: a fresh process resuming the lane reads the
    # failure from the committed record alone, and the build it routes still
    # receives that final diagnostic.
    lane, ctl, cmd = _lane(tmp_path)
    script = ctl / "long_bar.py"
    script.write_text(LONG_BAR, encoding="utf-8")
    stack = lane / "docs" / "stack.ini"
    declared = '"{}" "{}" "{}"'.format(
        Path(sys.executable).as_posix(), script.as_posix(), ctl.as_posix()
    )
    text = re.sub(
        r"(?m)^review = .*$",
        lambda _m: "review = " + declared,
        stack.read_text(encoding="utf-8"),
    )
    stack.write_text(text, encoding="utf-8", newline="\n")
    _configure(lane, _cap(5))
    first = _run(lane, cmd, 1)
    seen = len(_build_prompts(ctl))
    (ctl / "no_commit").write_text("on\n", encoding="utf-8")

    second = _run(lane, cmd, 1)

    assert len(_lines(ctl, "bar_runs.txt")) == 1, _out(first) + _out(second)
    resumed = _build_prompts(ctl)[seen:]
    assert resumed, _out(second)
    assert "ACTIONABLE-END-DIAGNOSTIC" in resumed[0], resumed[0]
    assert _red_count(lane).count == 1


def test_green_bar_attests_once_then_draws_the_review(tmp_path):
    # TC-376. A committed build whose review bar is green gets exactly one
    # `review` attestation commit, and the review round is drawn after it.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)

    proc = _run(lane, cmd, 4)

    assert proc.returncode == agent_loop.EXIT_DONE, _out(proc)
    attested = [
        (sha, kverdict.bar_attestation(str(lane), sha))
        for sha in _git(lane, "rev-list", "main..HEAD").split()
    ]
    attested = [(sha, att) for sha, att in attested if att is not None]
    assert len(attested) == 1, _out(proc)
    sha, att = attested[0]
    assert (att.bar, att.tests) == ("review", "none")
    verdict_commit = _git(
        lane, "log", "-1", "--format=%H", "--diff-filter=A", "--", "docs/reviews"
    )
    older = subprocess.run(
        ["git", "-C", str(lane), "merge-base", "--is-ancestor", sha, verdict_commit],
        capture_output=True,
    )
    assert older.returncode == 0 and sha != verdict_commit, (sha, verdict_commit)
    assert len(_lines(ctl, "bar_runs.txt")) == 1


# --- D4: every draw, one choke point --------------------------------------------


@pytest.mark.parametrize("bar", ["green", "red"])
def test_resumed_round_on_an_unattested_tip_runs_the_producer_once(tmp_path, bar):
    # TC-377. A resumed lane whose committed build owes a round but carries no
    # attestation runs the review bar once at the draw: green draws the round
    # and an ATTEST log records the result, red draws no reviewer.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)
    _hand_build(lane, ctl, red=(bar == "red"))
    if bar == "red":
        (ctl / "no_commit").write_text("on\n", encoding="utf-8")

    proc = _run(lane, cmd, 2)

    assert len(_lines(ctl, "bar_runs.txt")) == 1, _out(proc)
    models = _lines(ctl, "models.txt")
    if bar == "green":
        # The hand build left no session log, so no builder family is known
        # and the reviewer is any medium entry: the round is its REVIEW log.
        logs = _committed_logs(lane).values()
        assert any(_phase(t) == "REVIEW-A" for t in logs), _out(proc)
        attests = [t for t in logs if _phase(t) == "ATTEST"]
        assert len(attests) == 1, _out(proc)
        assert not _BAR_RED_RE.search(attests[0])
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
    """CHANGES-REQUESTED, a green rework, a narrow APPROVE and the fresh full
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
    _configure(lane, '\n[attestation]\nadjudication_review = "always"\n')
    return lane, ctl, _run(lane, cmd, 4, wi="WI-301")


@pytest.mark.parametrize("route", ["post-narrow", "adjudication"])
def test_post_narrow_and_adjudication_rounds_draw_only_over_a_verified_attestation(
    tmp_path, route
):
    # TC-377. The rounds `complete_review_round` and
    # `schedule_adjudication_round` queue pass the same draw: every review
    # session's reviewed commit carries a verified `review` attestation, and
    # the narrow-to-full transition runs no bar of its own.
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
        attested, cause = kverdict.review_attestation(str(lane), sha, [])
        assert attested is not None, cause
    builds = len(_lines(ctl, "builds.txt"))
    assert len(_lines(ctl, "bar_runs.txt")) == (builds or 1), _out(proc)


# --- D5: the count survives a resume; the cap -----------------------------------


def test_red_count_survives_a_resume_and_a_green_resets_it(tmp_path):
    # TC-378. The red count is read from the lane's committed logs: a fresh
    # process continues it, and its first build carries the recorded failure
    # tail. A verified green attestation resets it.
    lane, ctl, cmd = _lane(tmp_path / "a")
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(5))
    first = _run(lane, cmd, 2)
    seen = len(_build_prompts(ctl))
    second = _run(lane, cmd, 1)

    assert _red_count(lane).count == 3, _out(first) + _out(second)
    resumed = _build_prompts(ctl)[seen:]
    assert resumed and "BAR-FAIL-MARKER" in resumed[0], _out(second)

    # red, green (its round asks for changes), red, red: two since the green.
    lane, ctl, cmd = _lane(tmp_path / "b")
    (ctl / "bar_plan").write_text("RGRR\n", encoding="utf-8")
    (ctl / "verdicts.json").write_text(json.dumps([CHANGES_REQUESTED]), "utf-8")
    _configure(lane, _cap(5))
    proc = _run(lane, cmd, 5)
    assert _red_count(lane).count == 2, _out(proc)


def test_red_count_survives_a_resume_to_the_cap_and_exits_12(tmp_path):
    # TC-378. Two reds in one run and a third in a fresh process reach a cap
    # of 3: the resumed worker ends with the cap's own code and banner.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(3))
    _run(lane, cmd, 2)

    proc = _run(lane, cmd, 1)

    assert proc.returncode == 12, _out(proc)
    assert "RED CAP" in proc.stdout and "3 consecutive red rounds" in proc.stdout


@pytest.mark.parametrize("reds", ["at-the-cap", "one-fewer"])
def test_a_lane_resumed_at_the_cap_exits_12_before_any_session(tmp_path, reds):
    # TC-378, TC-381. A lane resumed with the cap's count of red records
    # already committed (a stop after the record and before the exit) ends at
    # run start: no builder, reviewer or bar runs and nothing is committed,
    # whatever round its committed trailer owes. One red fewer is no cap: the
    # resumed run launches a build (one that commits nothing, so it records no
    # further red); its run is given one session, since a build that commits
    # nothing does not end the run and a second session would build again.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    if reds == "at-the-cap":
        _configure(lane, _cap(5))
        _run(lane, cmd, 3)
        _set_cap(lane, 3)
    else:
        _configure(lane, _cap(3))
        _run(lane, cmd, 2)
        (ctl / "no_commit").write_text("on\n", encoding="utf-8")
    models, runs = _lines(ctl, "models.txt"), _lines(ctl, "bar_runs.txt")
    builds = len(_lines(ctl, "builds.txt"))
    commits = _git(lane, "rev-list", "--count", "HEAD")

    proc = _run(lane, cmd, 2 if reds == "at-the-cap" else 1)

    if reds == "at-the-cap":
        assert proc.returncode == 12, _out(proc)
        assert "RED CAP" in proc.stdout and "3 consecutive red rounds" in proc.stdout
        assert _lines(ctl, "models.txt") == models
        assert _lines(ctl, "bar_runs.txt") == runs
        assert _git(lane, "rev-list", "--count", "HEAD") == commits
    else:
        assert proc.returncode != 12, _out(proc)
        assert len(_lines(ctl, "builds.txt")) == builds + 1, _out(proc)
        assert "revb" not in _lines(ctl, "models.txt")[len(models) :]


# --- D6: an interrupted record --------------------------------------------------


def test_an_interrupted_red_is_rechecked_once_at_the_draw_and_counted_once(tmp_path):
    # TC-379. A build commit left with neither an attestation nor a red record
    # is re-checked once at the next draw, and the ATTEST log records its red;
    # the same red recorded twice for one build commit counts once.
    lane, ctl, cmd = _lane(tmp_path)
    _configure(lane)
    build = _hand_build(lane, ctl, red=True)
    (ctl / "no_commit").write_text("on\n", encoding="utf-8")

    proc = _run(lane, cmd, 1)

    assert len(_lines(ctl, "bar_runs.txt")) == 1, _out(proc)
    attests = [t for t in _committed_logs(lane).values() if _phase(t) == "ATTEST"]
    assert any(build in _BAR_RED_RE.findall(t) for t in attests), _out(proc)

    # The same red, recorded a second time in a log of its own.
    again = lane / "docs" / "iteration" / "t1-090-20261021-000000.log"
    again.write_text(
        "# agent session log\n# session: 090\n# train: t1\n# phase: ATTEST\n"
        "# outcome: RED\n# bar-red: {}\n# bar-summary: BAR-FAIL-MARKER\n".format(build),
        encoding="utf-8",
    )
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "-m", "telemetry: the red, recorded twice")
    assert _red_count(lane).count == 1


def test_a_build_ending_in_a_record_only_commit_is_recorded_and_counted_once(
    tmp_path,
):
    # TC-379. A build session whose last commit touches only records (its log
    # fragment) is the same build commit at the event and at the draw: the red
    # recorded at the event is found again on resume, so the bar does not run
    # twice for it and two red builds count two.
    lane, ctl, cmd = _lane(tmp_path)
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    (ctl / "record_last").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(5))
    first = _run(lane, cmd, 1)
    second = _run(lane, cmd, 1)

    builds = _lines(ctl, "build_shas.txt")
    assert len(builds) == 2, _out(first) + _out(second)
    assert len(_lines(ctl, "bar_runs.txt")) == 2, _out(first) + _out(second)
    keyed = {
        sha
        for text in _committed_logs(lane).values()
        for sha in _BAR_RED_RE.findall(text)
    }
    assert keyed == set(builds), (keyed, builds)
    assert _red_count(lane).count == 2


def test_attest_phase_is_inert_to_every_phase_reader(tmp_path):
    # TC-379. The loop's own ATTEST log is no build for the heterogeneity key,
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
    attests = [path for path, text in logs.items() if _phase(text) == "ATTEST"]
    assert len(attests) == 1, _out(proc)
    registry = {
        "PROVA-BUILD-1": SimpleNamespace(
            id="PROVA-BUILD-1", model="builda", family="PROVA"
        )
    }
    assert agent_loop.last_build_family(iteration, registry) == "PROVA"
    rounds = kverdict.review_logs(str(lane), "HEAD", "main", sorted(logs))
    assert attests[0] not in [entry[0] for entry in rounds]
    ordinal = int(re.match(r"t1-(\d+)-", Path(attests[0]).name).group(1))
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
    `red` is `(build sha, summary)` for a red record."""
    meta = {
        "session": "{:03d}".format(n),
        "stamp": "20261021-0000{:02d}".format(n),
        "train": "t1",
        "phase": phase,
        "outcome": "RED" if red else "COMMITTED",
    }
    if red:
        meta.update(kverdict.format_red_record(*red))
    agent_loop.agent_common.write_session_log(
        repo / "docs" / "iteration", meta, "transcript\n# bar-red: " + "f" * 40
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "telemetry: session {}".format(n))


def _reader_green(repo):
    """An empty commit carrying a verified `review` attestation of the tip."""
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    work = _git(repo, "rev-parse", "HEAD")
    line = kverdict.format_bar_green(tree, work, "review", "none", "green")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "attest\n\n" + line)


def test_red_rounds_counts_distinct_red_builds_and_a_green_attestation_resets_it(
    tmp_path,
):
    # TC-378. The count is read from the committed logs alone, so a fresh
    # process reads what an earlier one recorded; the newest verified review
    # attestation resets it, and the last summary is the newest red's.
    repo = _reader_lane(tmp_path)
    first = _reader_build(repo, 1)
    _reader_log(repo, 1, "BUILD", (first, "bar failed:\n  one"))
    second = _reader_build(repo, 2)
    _reader_log(repo, 2, "BUILD", (second, "bar failed: two"))

    counted = kverdict.red_rounds(str(repo), "t1", "main")
    assert counted == kverdict.RedCount(2, "bar failed: two")

    _reader_build(repo, 3)
    _reader_green(repo)
    _reader_log(repo, 3, "BUILD")
    assert kverdict.red_rounds(str(repo), "t1", "main").count == 0

    fourth = _reader_build(repo, 4)
    _reader_log(repo, 4, "BUILD", (fourth, "bar failed: four"))
    assert kverdict.red_rounds(str(repo), "t1", "main") == kverdict.RedCount(
        1, "bar failed: four"
    )


def test_a_long_red_summary_keeps_its_cause_and_its_final_diagnostic():
    # TC-375. The one persisted summary of a red result is bounded, and a
    # refusal longer than the bound keeps both ends: the cause at its head and
    # the diagnostic a bar prints last. A short one is kept whole.
    sha = "a" * 40
    refusal = "attest REFUSED - CAUSE-AT-HEAD:\n" + "context\n" * 80 + "FINAL-LINE"
    fields = kverdict.format_red_record(sha, refusal)
    line = fields["bar-summary"]
    assert len(line) <= 240
    assert line.startswith("attest REFUSED - CAUSE-AT-HEAD:")
    assert line.endswith("context FINAL-LINE")
    assert kverdict.parse_red_record(
        "# bar-red: {}\n# bar-summary: {}\n# ---\n".format(sha, line)
    ) == (sha, line)
    short = kverdict.format_red_record(sha, "bar failed:\n  one line")
    assert short["bar-summary"] == "bar failed: one line"


def test_red_rounds_counts_one_build_recorded_twice_once(tmp_path):
    # TC-379. A red recorded for one build commit in two logs (the build's own
    # and a later re-check's) counts once; the record's grammar round-trips,
    # its summary folded to one line, and a transcript line is no record.
    repo = _reader_lane(tmp_path)
    build = _reader_build(repo, 1)
    _reader_log(repo, 1, "BUILD", (build, "bar failed:\n  one"))
    _reader_log(repo, 2, "ATTEST", (build, "bar failed: again"))
    _reader_log(repo, 3, "BUILD")

    assert kverdict.red_rounds(str(repo), "t1", "main") == kverdict.RedCount(
        1, "bar failed: again"
    )
    logs = sorted((repo / "docs" / "iteration").glob("*.log"))
    first = logs[0].read_text(encoding="utf-8")
    assert kverdict.parse_red_record(first) == (build, "bar failed: one")
    assert kverdict.parse_red_record(logs[2].read_text(encoding="utf-8")) is None


def test_red_rounds_counts_an_unreadable_log_and_answers_none_for_no_history(
    tmp_path, monkeypatch
):
    # TC-378. A log git cannot show counts as one red keyed by its path,
    # toward the cap; a range git cannot list answers None.
    repo = _reader_lane(tmp_path)
    build = _reader_build(repo, 1)
    _reader_log(repo, 1, "BUILD", (build, "bar failed: one"))
    _reader_log(repo, 2, "BUILD")
    real = kverdict.git_out

    def no_show(root, args, stdin=None):
        return None if args[0] == "show" else real(root, args, stdin)

    monkeypatch.setattr(kverdict, "git_out", no_show)
    assert kverdict.red_rounds(str(repo), "t1", "main").count == 2
    monkeypatch.setattr(kverdict, "git_out", real)

    assert kverdict.red_rounds(str(repo), "t1", "no-such-base") is None


# --- D7 and D9: the setting is refused before any session -----------------------

_UNPARSEABLE = '[policies]\ntrunk = "main"\n[build\nred_rounds_max = 3\n'
_NON_TABLE = 'build = 3\n\n[policies]\ntrunk = "main"\n'


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


@pytest.mark.parametrize("value", ["0", "-1", "true", '"3"', "3.0"])
def test_a_bad_red_rounds_max_refuses_before_any_session(tmp_path, value):
    # TC-380. A declared `red_rounds_max` that is not an int, is a bool, or is
    # below 1 is refused at the loop's preflight, naming its line, before any
    # session starts.
    lane, ctl, cmd = _lane(tmp_path)
    path = lane / "docs" / "process.toml"
    line = len(path.read_text(encoding="utf-8").splitlines()) + 3
    _configure(lane, _cap(value))

    proc = _run(lane, cmd, 2)

    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, _out(proc)
    assert "docs/process.toml:{}".format(line) in proc.stderr, proc.stderr
    assert "red_rounds_max" in proc.stderr
    assert not (ctl / "models.txt").exists()


# --- D8: the worker's cap -------------------------------------------------------


def test_red_cap_exits_with_its_own_code_and_one_fewer_does_not(tmp_path):
    # TC-381. Two consecutive reds under a cap of 2 end the worker with exit
    # 12 and the RED CAP banner; the same two reds under a cap of 3 end on
    # the iteration budget instead. The cap closes partial rather than
    # escalating through the declared approval level: the worker never
    # consults the page ladder (no failure-action line, no PAGE-HUMAN stop)
    # and its exit is not the NEEDS-HUMAN code. A cap that paged the human
    # first, then exited 12 whatever the hold decided, fails here.
    lane, ctl, cmd = _lane(tmp_path / "capped")
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(2))
    proc = _run(lane, cmd, 2)
    assert proc.returncode == 12, _out(proc)
    assert "RED CAP" in proc.stdout and "2 consecutive red rounds" in proc.stdout
    assert "route/failure" not in proc.stdout, _out(proc)
    assert "PAGE-HUMAN" not in proc.stdout, _out(proc)

    lane, ctl, cmd = _lane(tmp_path / "below")
    (ctl / "bar_red").write_text("on\n", encoding="utf-8")
    _configure(lane, _cap(3))
    proc = _run(lane, cmd, 2)
    assert proc.returncode == agent_loop.EXIT_BUDGET, _out(proc)
    assert "RED CAP" not in proc.stdout
