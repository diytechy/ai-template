"""The parallel dispatcher — scripts/agent_loop.py --jobs (WI-182,
SR-061/LLR-062/TC-062; docs/specs/parallel-wi-dispatch.md §4/§6).

Exercised end-to-end: the real dispatcher as a subprocess, spawning REAL
Slice-C workers (agent_loop.py --wi/--train in linked worktrees), which drive
the same fake agent the worker suite uses. The load-bearing guarantees:

  - up-to-ceiling concurrency in separate linked worktrees, with dynamic
    refill (a third traincar dispatches only when a lane frees) — proven both
    from the event journal and by a rendezvous fake that deadlocks unless two
    workers genuinely overlap;
  - the atomic all-or-none reservation: one pre-existing constituent ref makes
    the whole traincar transaction fail with nothing created;
  - spine-class work serializes whole-project (runs first and alone);
  - docs/pause stops new reservations at the next boundary (zero refs made);
  - --jobs 1 (explicit serial mode) builds the same result set;
  - unclassified WIs fail closed (never dispatched) without stopping
    classified disjoint work;
  - a reconciled incomplete train resumes from its durable reservation.
"""

import csv
import json
import os
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, run_py, seed_venv

agent_loop = load_script("agent_loop")

pytestmark = pytest.mark.skipif(
    not __import__("shutil").which("git"), reason="needs git on PATH"
)

HEADER = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "SafetyClass",
]


def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout.strip()


def _wi_row(wid, preds="", safety="ordinary", status="queued"):
    return [
        wid,
        "Work " + wid,
        "ws",
        "SR-061",
        preds,
        status,
        "shipped" if status == "done" else "",
        "docs/specs/thing.md",
        "medium",
        safety,
    ]


def _make_repo(tmp_path, rows):
    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    with open(
        str(repo / "docs" / "requirements" / "work-items.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)
    (repo / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (repo / ".gitignore").write_text("out/\n.venv/\n", encoding="utf-8")
    seed_venv(repo)  # WI-286: the dispatcher preflight requires a ≥3.11 root .venv
    # The fixtures grind autonomously; the attended ratification exit has its
    # own dedicated test below.
    (repo / "docs" / "gate-policy").write_text("autonomous\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


# The fake agent the WORKERS run. Modes (ctl/mode): `build` commits the WI
# trailer; `rendezvous` writes its start marker, waits for another worker's
# marker (proving genuine overlap), then commits.
FAKE = r"""
import argparse, pathlib, re, subprocess, sys, time
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
wi = re.search(r"- WI: (WI-\d+)", args.prompt).group(1)
train = re.search(r"- Train: (\S+) \(branch", args.prompt).group(1)
base = re.search(r"integration base ([0-9a-f]+)\)", args.prompt).group(1)
mode = (ctl / "mode").read_text().strip() if (ctl / "mode").exists() else "build"
if mode == "rendezvous":
    (ctl / (wi + ".started")).write_text("x", encoding="utf-8")
    deadline = time.time() + 60
    while time.time() < deadline:
        others = [p for p in ctl.glob("WI-*.started") if p.stem != wi]
        if others:
            break
        time.sleep(0.2)
    else:
        sys.exit(9)  # no overlap: the dispatcher ran us serially
pathlib.Path("work-" + wi + ".txt").write_text("work", encoding="utf-8")
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(
    ["git", "commit", "-q", "-m",
     "build " + wi + "\n\nWI: " + wi + "\nTrain: " + train + "\nBase: " + base + "\n"],
    check=True,
)
sys.exit(0)
"""


def _dispatch(repo, fake, ctl, *extra, jobs="2", timeout=300):
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--poll-seconds",
            "0.2",
            "--model",
            "test",
            "--jobs",
            jobs,
            *extra,
        ],
        cwd=repo,
    )


def _setup(tmp_path, rows):
    repo = _make_repo(tmp_path, rows)
    ctl = tmp_path / "ctl"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    return repo, ctl, fake


def _events(repo):
    p = repo / "out" / "dispatch" / "events.jsonl"
    if not p.exists():
        return []
    return [
        json.loads(ln)
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


def _reservations(repo):
    out = _git(repo, "for-each-ref", "--format=%(refname)", "refs/llm/reservations")
    return {ln.rsplit("/", 1)[1] for ln in out.splitlines() if ln.strip()}


# --- the fan-out engine end-to-end ---------------------------------------------


def test_dispatcher_builds_frontier_with_refill(tmp_path):
    # Three independent ordinary WIs, ceiling 2: all three build, in three
    # separate trains/worktrees, and the third dispatches only after a lane
    # frees (dynamic refill, SR-061 AC).
    repo, ctl, fake = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202"), _wi_row("WI-203")]
    )
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    # All three built AND integrated (Slice F): rows done on the published
    # development branch, reservation refs released after the durable
    # disposition advanced, and the integration commits carry the trailers.
    assert _reservations(repo) == set()
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    for wid in ("WI-201", "WI-202", "WI-203"):
        assert wid + ",Work " + wid + ",ws,SR-061,,done," in reg
        assert "Integrated from train" in reg
    events = _events(repo)
    starts = [e for e in events if e["event"] == "worker-start"]
    dones = [e for e in events if e["event"] == "worker-done"]
    assert len(starts) == 3 and len(dones) == 3
    assert sum(1 for e in events if e["event"] == "integrated") == 3
    # Refill: the third start comes after the first done (ceiling 2 held).
    idx = {id(e): i for i, e in enumerate(events)}
    assert idx[id(starts[2])] > idx[id(dones[0])]
    # Linked worktrees in the sibling pool (3 trains + staging worktrees).
    pool = agent_loop.worktree_root(repo)
    assert len([p for p in pool.iterdir() if not p.name.startswith("integrate-")]) == 3
    # run-state is a generated dispatcher outcome: everything integrated.
    assert (repo / "docs" / "run-state").read_text().startswith("DONE")
    # SR-059's generation half: the integrator-generated status snapshot.
    status = (repo / "docs" / "status.md").read_text("utf-8")
    assert agent_loop.STATUS_GENERATED_MARKER in status


def test_two_workers_genuinely_overlap(tmp_path):
    # The rendezvous fake exits 9 (never committing) unless the OTHER worker
    # starts while it waits — deterministic proof of real concurrency.
    repo, ctl, fake = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    (ctl / "mode").write_text("rendezvous", encoding="utf-8")
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    events = _events(repo)
    assert sum(1 for e in events if e["event"] == "worker-done") == 2


def test_jobs_1_is_serial_with_the_same_result_set(tmp_path):
    repo, ctl, fake = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202"), _wi_row("WI-203")]
    )
    proc = _dispatch(repo, fake, ctl, jobs="1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    # The same integrated result set as the parallel run (SR-061 AC).
    assert _reservations(repo) == set()
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert reg.count(",done,") >= 3
    events = _events(repo)
    # Strictly serial: every start after the first is preceded by a done.
    order = [e["event"] for e in events if e["event"].startswith("worker-")]
    active = 0
    peak = 0
    for ev in order:
        if ev == "worker-start":
            active += 1
        elif ev in ("worker-done", "worker-blocked", "worker-quarantined"):
            active -= 1
        peak = max(peak, active)
    assert peak == 1


def test_spine_class_serializes_whole_project(tmp_path):
    # A spine-class WI runs FIRST (lowest-gate-first) and ALONE — no ordinary
    # worker starts between its start and its done (spec §5.1).
    repo, ctl, fake = _setup(
        tmp_path,
        [
            _wi_row("WI-201"),
            _wi_row("WI-202"),
            _wi_row("WI-210", safety="spine"),
        ],
    )
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    events = [e for e in _events(repo) if e["event"].startswith("worker-")]
    assert events[0]["event"] == "worker-start" and "WI-210" in events[0]["wis"]
    assert events[1]["event"] == "worker-done", (
        "the spine train must finish before any other worker starts: %s" % events
    )


def test_spine_train_exits_for_ratification_under_attended(tmp_path):
    # gate-policy attended: a built spine/gate train EXITS FOR RATIFICATION
    # (spec §4.2) — the ordinary WI does not dispatch past the gate.
    repo, ctl, fake = _setup(
        tmp_path, [_wi_row("WI-210", safety="spine"), _wi_row("WI-201")]
    )
    (repo / "docs" / "gate-policy").write_text("attended\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "attended gate policy")
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert "needs ratification" in proc.stdout
    assert _reservations(repo) == {"WI-210"}, "build-out must not continue"
    assert (repo / "docs" / "run-state").read_text().startswith("NEEDS-HUMAN")


def test_spine_batch_one_train_no_pause_under_autonomous(tmp_path):
    # WI-204 (the SR-058 amendment + the owner's pause-free pin, 2026-07-17):
    # (1) ready spine-serial WIs — a spine and a gate row here — ride ONE
    # spine-only traincar (drafted together, reviewed together, attested
    # together), and the worker's §7 continuation re-check permits the
    # homogeneous batch instead of ending the train early; (2) under
    # gate-policy autonomous the built batch triggers NO ratification exit —
    # the run continues straight into ordinary build-out and ends DONE.
    repo, ctl, fake = _setup(
        tmp_path,
        [
            _wi_row("WI-210", safety="spine"),
            _wi_row("WI-211", safety="gate"),
            _wi_row("WI-201"),
        ],
    )
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "needs ratification" not in proc.stdout, "no human pause up to G-Final"
    events = _events(repo)
    assert not any(e["event"] == "gate-ratification-exit" for e in events)
    starts = [e for e in events if e["event"] == "worker-start"]
    assert len(starts) == 2, "one spine batch train + one ordinary train: %s" % starts
    assert starts[0]["wis"] == "WI-210;WI-211", "the batch rides ONE train"
    assert starts[1]["wis"] == "WI-201"
    # the batch train genuinely finished before ordinary build-out began
    order = [e["event"] for e in events if e["event"].startswith("worker-")]
    assert order == ["worker-start", "worker-done", "worker-start", "worker-done"]


def test_spine_batch_still_exits_for_ratification_under_attended(tmp_path):
    # The batch changes packing, not gate authority: under attended the built
    # spine-only train still EXITS FOR RATIFICATION exactly per §4.2.
    repo, ctl, fake = _setup(
        tmp_path,
        [
            _wi_row("WI-210", safety="spine"),
            _wi_row("WI-211", safety="gate"),
            _wi_row("WI-201"),
        ],
    )
    (repo / "docs" / "gate-policy").write_text("attended\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "attended gate policy")
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert "needs ratification" in proc.stdout
    assert _reservations(repo) == {"WI-210", "WI-211"}, (
        "the whole batch is one ratification scope; build-out must not continue"
    )


def test_pause_stops_new_reservations_at_the_boundary(tmp_path):
    repo, ctl, fake = _setup(tmp_path, [_wi_row("WI-201")])
    (repo / "docs" / "pause").write_text("owner pause\n", encoding="utf-8")
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_PAUSED, proc.stdout + proc.stderr
    assert _reservations(repo) == set(), "paused run must reserve nothing"


def test_unclassified_wi_fails_closed_without_stopping_others(tmp_path):
    # WI-202 carries no SafetyClass: it must never dispatch, while the
    # classified WI-201 proceeds (SR-058's fail-closed scoped to the WI).
    repo, ctl, fake = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202", safety="")]
    )
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    # WI-201 built AND integrated (reservation released); the unclassified
    # WI-202 was never dispatched and keeps the run RUNNING.
    assert _reservations(repo) == set()
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert "WI-201,Work WI-201,ws,SR-061,,done," in reg
    assert "WI-202,Work WI-202,ws,SR-061,,queued," in reg
    assert (repo / "docs" / "run-state").read_text().startswith("RUNNING")


def test_reservation_transaction_is_all_or_none(tmp_path):
    # Pre-claim one constituent; the two-WI traincar transaction must create
    # NEITHER the other reservation nor the train branch (SR-061 AC).
    repo, ctl, fake = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202", preds="WI-201")]
    )
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/llm/reservations/WI-202", head)
    err = agent_loop.reserve_traincar(repo, "t-atomic", ["WI-201", "WI-202"], head)
    assert err is not None and "transaction failed" in err
    assert _reservations(repo) == {"WI-202"}, "nothing else may be created"
    code = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "--verify",
            "--quiet",
            "refs/heads/llm/train/t-atomic",
        ],
        capture_output=True,
    ).returncode
    assert code != 0, "the train branch must not exist after a failed txn"


def test_ordinary_unary_chain_packs_one_traincar(tmp_path):
    # WI-202 hard-depends on WI-201 (both ordinary): the packer clusters them
    # into ONE traincar (one train branch, both trailers on it) instead of
    # stranding WI-202 waiting for an integrator that runs later (Slice F).
    repo, ctl, fake = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202", preds="WI-201")]
    )
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert _reservations(repo) == set()
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert reg.count(",done,") >= 2
    starts = [e for e in _events(repo) if e["event"] == "worker-start"]
    assert len(starts) == 1 and starts[0]["wis"] == "WI-201;WI-202"


def test_reconciled_incomplete_train_resumes(tmp_path):
    # A durable reservation + train branch with no evidence (a crashed run):
    # the relaunched dispatcher resumes it rather than double-reserving.
    repo, ctl, fake = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    # The crashed run had already initialized the integration ref — without
    # it, reservations alone make the dispatcher fail closed (spec §11; that
    # guard has its own test in the F suite).
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    err = agent_loop.reserve_traincar(repo, "p0-g0-WI-201-dead", ["WI-201"], head)
    assert err is None
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    events = _events(repo)
    assert any(e["event"] == "reconcile" and e.get("state") == "resume" for e in events)
    reserves = [e for e in events if e["event"] == "reserve"]
    assert not reserves, "a reserved WI must never be re-reserved"
    dones = [e for e in events if e["event"] == "worker-done"]
    assert len(dones) == 1 and dones[0]["train"] == "p0-g0-WI-201-dead"


def test_bad_jobs_value_is_preflight_failure(tmp_path):
    repo, ctl, fake = _setup(tmp_path, [_wi_row("WI-201")])
    proc = _dispatch(repo, fake, ctl, jobs="zero")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT


def test_dispatcher_refuses_a_below_floor_harness_interpreter(tmp_path):
    # WI-286: a repo whose ./.venv interpreter cannot report a ≥3.11 version is
    # refused at preflight, before any worker is spawned or the integrator bar
    # runs — a below-floor run must never silently produce a green. A garbage file
    # named python(.exe) fails to execute on both OSes (WinError 193 / a
    # non-executable file), so interpreter_version returns None -> fail closed.
    import shutil

    repo, ctl, fake = _setup(tmp_path, [_wi_row("WI-201")])
    # Replace the fixture's real seeded .venv (seed_venv) with a garbage one. Wipe
    # it first: venv.create makes bin/python a SYMLINK to the base interpreter on
    # POSIX, so writing THROUGH it would truncate the system python — rmtree, then
    # plant a plain non-executable file.
    shutil.rmtree(repo / ".venv")
    if os.name == "nt":
        vpy = repo / ".venv" / "Scripts" / "python.exe"
    else:
        vpy = repo / ".venv" / "bin" / "python"
    vpy.parent.mkdir(parents=True)
    vpy.write_text("not a real interpreter\n", encoding="utf-8")
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, proc.stdout + proc.stderr
    assert "could not be run" in (proc.stdout + proc.stderr)


def test_dispatcher_refuses_a_venvless_root(tmp_path):
    # REVIEW-A MAJOR, end-to-end: a root with NO ./.venv is refused at preflight
    # even though the ambient interpreter (this test's own) is >= the floor. The
    # old check fell through to ambient and produced a green worker run; the harness
    # must run under the repo's OWN pinned .venv, never ambient (whose pinned dev
    # tools may be absent). Wipe the fixture's seeded venv to reproduce the exact
    # venv-less worktree that run 20260723T0202 hit.
    import shutil

    repo, ctl, fake = _setup(tmp_path, [_wi_row("WI-201")])
    shutil.rmtree(repo / ".venv")
    proc = _dispatch(repo, fake, ctl)
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, proc.stdout + proc.stderr
    assert "no runnable ./.venv" in (proc.stdout + proc.stderr)


def test_lease_worktree_survives_a_hand_deleted_worktree(tmp_path):
    # Repo-review 2026-07-21 M-32: `git worktree list` keeps naming a directory
    # deleted by hand until a prune, so leasing the ghost handed Popen a
    # nonexistent cwd — an uncaught crash with reservations held, repeated on
    # every relaunch. The lease must prune the stale registration and re-add.
    import shutil as _shutil

    ad = agent_loop.agent_dispatch
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "branch", ad.TRAIN_BRANCH_PREFIX + "t9")
    wt1, err = ad.lease_worktree(repo, "t9")
    assert err is None and wt1.is_dir()
    _shutil.rmtree(wt1)
    wt2, err2 = ad.lease_worktree(repo, "t9")
    assert err2 is None, err2
    assert wt2 is not None and wt2.is_dir()  # pruned + freshly re-added
