"""Crash safety + git-as-authority recovery — the fault-injected crash matrix
(WI-185, SR-064/LLR-065/TC-065; docs/specs/parallel-wi-dispatch.md §11/§16).

Each matrix test crashes a REAL dispatcher run (AGENT_FAULT_POINT hard-kills
the process with os._exit at the named lifecycle boundary — no cleanup, no
atexit), then relaunches WITHOUT the fault and asserts the §16 invariants:

  - restart reconstructs exactly one owner (never a re-reserve of a held WI,
    never a double-run);
  - no WI is falsely done, and no unintegrated commit or dirty tree is
    deleted;
  - llm/integration is atomically either ENTIRELY before or ENTIRELY after an
    integration — a crash on either side of the CAS recovers to exactly one
    integration of the train;
  - the development ref/worktree is always in one of the three recoverable
    publication states (fully unpublished / fully synchronized / in-between
    with a valid intent), and recovery finishes the publish idempotently;
  - deleting ALL of out/dispatch/ before the restart changes nothing — Git is
    the authority, the journal is cache;
  - unprovable ownership (a train claiming a WI outside its reservation)
    quarantines that train only, while disjoint proven work proceeds.
"""

import csv
import os
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, seed_venv

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
        "SR-064",
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
    (repo / "docs" / "gate-policy").write_text("autonomous\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


FAKE = r"""
import argparse, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "sessions.txt"), "a", encoding="utf-8") as fh:
    fh.write("s\n")
wi = re.search(r"- WI: (WI-\d+)", args.prompt).group(1)
train = re.search(r"- Train: (\S+) \(branch", args.prompt).group(1)
base = re.search(r"integration base ([0-9a-f]+)\)", args.prompt).group(1)
pathlib.Path("work-" + wi + ".txt").write_text("work", encoding="utf-8")
subprocess.run(["git", "add", "-A"], check=True)
msg = "build " + wi + "\n\nWI: " + wi + "\nTrain: " + train + "\nBase: " + base + "\n"
subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
sys.exit(0)
"""


def _setup(tmp_path, rows):
    repo = _make_repo(tmp_path, rows)
    ctl = tmp_path / "ctl"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    return repo, ctl, template


def _dispatch(repo, template, fault=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("AGENT_")}
    if fault:
        env["AGENT_FAULT_POINT"] = fault
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "agent_loop.py"),
            "--root",
            str(repo),
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--poll-seconds",
            "0.2",
            "--model",
            "test",
            "--jobs",
            "2",
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
    )


def _reservations(repo):
    out = _git(repo, "for-each-ref", "--format=%(refname)", "refs/llm/reservations")
    return {ln.rsplit("/", 1)[1] for ln in out.splitlines() if ln.strip()}


def _done_rows(repo, ref="HEAD"):
    show = _git(repo, "show", ref + ":docs/requirements/work-items.csv")
    return [
        ln.split(",", 1)[0]
        for ln in show.splitlines()
        if ",done," in ln and ln.startswith("WI-")
    ]


def _integrations_for(repo, ref="HEAD"):
    log = _git(repo, "log", "--format=%s", ref)
    return [ln for ln in log.splitlines() if ln.startswith("integrate: train")]


def _crash_then_recover(tmp_path, fault, wipe_journal=False):
    """Run the matrix step: crash at `fault`, optionally wipe out/dispatch/,
    relaunch clean, and return (repo, ctl, crash_proc, recover_proc)."""
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    crash = _dispatch(repo, template, fault=fault)
    assert crash.returncode == agent_loop.FAULT_EXIT, (
        "the fault must hard-kill the run: " + crash.stdout + crash.stderr
    )
    if wipe_journal:
        import shutil

        shutil.rmtree(str(repo / "out" / "dispatch"), ignore_errors=True)
    recover = _dispatch(repo, template)
    assert recover.returncode == agent_loop.EXIT_DONE, recover.stdout + recover.stderr
    return repo, ctl, crash, recover


# --- the crash matrix -------------------------------------------------------------


def test_crash_during_reservation_transaction(tmp_path):
    # Before the atomic transaction lands: no refs, no branch — only an
    # unreachable metadata object. Recovery is a clean re-derive.
    repo, ctl, crash, recover = _crash_then_recover(tmp_path, "reserve-pre-txn")
    assert _done_rows(repo) == ["WI-201"]
    assert _reservations(repo) == set()
    assert len(_integrations_for(repo)) == 1, "exactly one integration"


def test_crash_after_reservation_before_first_commit(tmp_path):
    # The §16 point: every constituent reservation reconstructs from
    # refs/llm/reservations/* INCLUDING before its first WI commit — the
    # relaunch resumes the same train, never double-reserving.
    repo, ctl, crash, recover = _crash_then_recover(tmp_path, "reserve-post-txn")
    assert _done_rows(repo) == ["WI-201"]
    assert _reservations(repo) == set()
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert '"state": "resume"' in events, "recovery resumes the reserved train"
    assert '"reserve"' not in events.replace('"reserve-failed"', ""), (
        "a held reservation is never re-reserved"
    )
    assert len(_integrations_for(repo)) == 1


def test_crash_immediately_before_integration_cas(tmp_path):
    # The staging commit exists but the CAS never ran: llm/integration is
    # ENTIRELY BEFORE the integration; recovery recomposes and lands it once.
    repo, ctl, crash, recover = _crash_then_recover(tmp_path, "pre-integration-cas")
    assert _done_rows(repo) == ["WI-201"]
    assert len(_integrations_for(repo)) == 1, "recomposition must not double-integrate"
    assert _reservations(repo) == set()


def test_crash_immediately_after_integration_cas(tmp_path):
    # The CAS advanced but reservations were never released and nothing
    # published: llm/integration is ENTIRELY AFTER. Recovery restores
    # `integrated` from the registry ON the ref (never a second integration),
    # finishes the release, and publishes idempotently.
    repo, ctl, crash, recover = _crash_then_recover(tmp_path, "post-integration-cas")
    assert _done_rows(repo) == ["WI-201"]
    assert len(_integrations_for(repo)) == 1, "never re-integrated"
    assert _reservations(repo) == set()
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert '"state": "integrated"' in events, "restored, not re-run"
    # The worker ran in the FIRST process only — one session total.
    assert (ctl / "sessions.txt").read_text("utf-8").count("s") == 1, (
        "the WI was double-run"
    )


def test_crash_after_intent_before_dev_cas(tmp_path):
    # The intent ref exists, the dev ref never moved: fully unpublished with a
    # valid intent — recovery reuses the identical intent and publishes.
    repo, ctl, crash, recover = _crash_then_recover(tmp_path, "post-intent")
    assert _done_rows(repo) == ["WI-201"]
    code = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "--verify",
            "--quiet",
            "refs/llm/publish-intent",
        ],
        capture_output=True,
    ).returncode
    assert code != 0, "exactly one intent lifecycle — deleted after the sync"
    assert _git(repo, "rev-parse", "HEAD") == _git(
        repo, "rev-parse", "refs/heads/llm/integration"
    )


def test_crash_between_dev_cas_and_sync(tmp_path):
    # The dev ref moved to the target but the worktree still sits at the old
    # hash: the in-between state, provable ONLY through the intent. Recovery
    # syncs idempotently — never classifying the stale checkout as user dirt.
    repo, ctl, crash, recover = _crash_then_recover(tmp_path, "post-dev-cas")
    assert _done_rows(repo) == ["WI-201"]
    assert _git(repo, "rev-parse", "HEAD") == _git(
        repo, "rev-parse", "refs/heads/llm/integration"
    )
    status = _git(repo, "status", "--porcelain")
    tracked = [ln for ln in status.splitlines() if ln and not ln.startswith("??")]
    assert not tracked, "the sync completed cleanly"
    code = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "--verify",
            "--quiet",
            "refs/llm/publish-intent",
        ],
        capture_output=True,
    ).returncode
    assert code != 0


def test_out_dispatch_deletion_does_not_prevent_reconstruction(tmp_path):
    # The §16 capstone: the journal is cache — wipe ALL of out/dispatch/
    # after the crash and recovery still reconstructs from Git alone.
    repo, ctl, crash, recover = _crash_then_recover(
        tmp_path, "post-integration-cas", wipe_journal=True
    )
    assert _done_rows(repo) == ["WI-201"]
    assert len(_integrations_for(repo)) == 1
    assert _reservations(repo) == set()
    assert (ctl / "sessions.txt").read_text("utf-8").count("s") == 1


def test_unprovable_ownership_quarantines_only_that_train(tmp_path):
    # A train branch carrying a WI trailer OUTSIDE its reservation set is
    # unprovable ownership: that train quarantines (nothing deleted), while
    # the disjoint classified WI builds and integrates normally.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t-rogue", ["WI-202"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-rogue")
    (wt / "rogue.txt").write_text("rogue", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        # Claims WI-201, which t-rogue does NOT hold.
        "build WI-201\n\nWI: WI-201\nTrain: t-rogue\nBase: {}\n".format(head),
    )
    proc = _dispatch(repo, template)
    # The rogue train needs attention (quarantine) => EXIT_STALL, but the
    # disjoint WI-201 still built and integrated through its OWN train.
    assert proc.returncode == agent_loop.EXIT_STALL, proc.stdout + proc.stderr
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert "claims-unreserved-wi:WI-201" in events
    assert "WI-201" in _done_rows(repo, "refs/heads/llm/integration")
    # Nothing was deleted: the rogue branch, its commit, and its reservation
    # survive for a human to rule on (conservative cleanup).
    assert _git(repo, "rev-parse", "--verify", "refs/heads/llm/train/t-rogue")
    assert _reservations(repo) == {"WI-202"}
    rows = _done_rows(repo, "refs/heads/llm/integration")
    assert "WI-202" not in rows, "a quarantined claim is never falsely done"


def _reserve(repo, tid, wis, base):
    assert agent_loop.reserve_traincar(repo, tid, wis, base) is None


def _integration_commit(iwt, wid, base):
    # A commit on llm/integration carrying WI-<wid>'s trailer — integrated dev
    # history, the shape an owner sync imports into a reserved train.
    (iwt / (wid + ".txt")).write_text("dev", encoding="utf-8")
    _git(iwt, "add", "-A")
    _git(
        iwt,
        "commit",
        "-q",
        "-m",
        "integrate {0}\n\nWI: {0}\nTrain: dev\nBase: {1}\n".format(wid, base),
    )


def _owner_synced_train(tmp_path, repo):
    # The WI-237 field shape: llm/integration carries two integrated dev
    # commits (WI-808/WI-809); a train reserves WI-201 with a base PREDATING
    # them, commits its own novel WI-201 work, then the owner merges the
    # integrated dev history in as a content-only sync. Returns (base, ihead,
    # train worktree).
    base = _git(repo, "rev-parse", "HEAD")  # the reservation base predates the merge
    iwt = tmp_path / "iwt"
    _git(repo, "worktree", "add", "-b", "llm/integration", str(iwt), base)
    for wid in ("WI-808", "WI-809"):
        _integration_commit(iwt, wid, base)
    ihead = _git(repo, "rev-parse", "refs/heads/llm/integration")
    _reserve(repo, "t-sync", ["WI-201"], base)
    twt = tmp_path / "twt"
    _git(repo, "worktree", "add", str(twt), "llm/train/t-sync")
    (twt / "wi201.txt").write_text("own work", encoding="utf-8")
    _git(twt, "add", "-A")
    _git(
        twt,
        "commit",
        "-q",
        "-m",
        "build WI-201\n\nWI: WI-201\nTrain: t-sync\nBase: {}\n".format(base),
    )
    _git(twt, "merge", "--no-edit", "-m", "owner sync: dev into t-sync", ihead)
    return base, ihead, twt


def test_owner_dev_merge_into_reserved_train_is_not_a_foreign_claim(tmp_path):
    # WI-237, the WI-229 field shape. Merging the development branch INTO a
    # reserved train (a content-only sync to preempt stage-3 conflicts) imports
    # the integrated commits' WI trailers. Those commits are reachable from
    # llm/integration — integrated history, NOT claims this train is making —
    # so reconcile must park the train for integration, never quarantine it.
    repo = _make_repo(
        tmp_path,
        [
            _wi_row("WI-201"),
            _wi_row("WI-808", status="done"),
            _wi_row("WI-809", status="done"),
        ],
    )
    base, _ihead, _twt = _owner_synced_train(tmp_path, repo)

    # The scan is bounded ^<integration-head>: only the train's OWN novel work.
    built, blocked = agent_loop.train_branch_evidence(repo, "t-sync", base)
    assert built == {"WI-201"}, built
    assert blocked == {}

    dispatcher = agent_loop.agent_dispatch
    journal = dispatcher._Journal(repo)
    parked, quarantined = dispatcher._reconcile_owned_trains(repo, journal)
    assert "WI-201" not in quarantined, "a content sync must not quarantine"
    assert parked["t-sync"]["state"] == "ready-to-integrate"
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert "claims-unreserved-wi" not in events


def test_novel_foreign_claim_after_owner_sync_still_quarantines(tmp_path):
    # WI-237 boundary: the exclusion is precise. Integration-reachable imports
    # are ignored, but a genuine foreign claim in a NOVEL (unintegrated) commit
    # still quarantines with the same reason, naming ONLY the novel WI — never
    # the merged-in dev WIs.
    repo = _make_repo(
        tmp_path,
        [
            _wi_row("WI-201"),
            _wi_row("WI-808", status="done"),
            _wi_row("WI-809", status="done"),
        ],
    )
    base, _ihead, twt = _owner_synced_train(tmp_path, repo)
    # A novel commit claiming WI-999, which t-sync does NOT hold.
    (twt / "rogue.txt").write_text("rogue", encoding="utf-8")
    _git(twt, "add", "-A")
    _git(
        twt,
        "commit",
        "-q",
        "-m",
        "build WI-999\n\nWI: WI-999\nTrain: t-sync\nBase: {}\n".format(base),
    )

    built, _blocked = agent_loop.train_branch_evidence(repo, "t-sync", base)
    assert built == {"WI-201", "WI-999"}, built

    dispatcher = agent_loop.agent_dispatch
    journal = dispatcher._Journal(repo)
    parked, quarantined = dispatcher._reconcile_owned_trains(repo, journal)
    assert parked["t-sync"]["state"] == "quarantined"
    assert "WI-201" in quarantined, "the reserved WI's ambiguous train quarantines"
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert "claims-unreserved-wi:WI-999" in events
    assert "WI-808" not in events and "WI-809" not in events


# --- WI-239: a cured blocker is survivable (latest trailer wins + resume-once) ---


def _reserve_train_with_trailers(tmp_path, repo, tid, order, wid="WI-201"):
    """Reserve a single-WI train off the integration head and commit its trailer
    evidence in `order` (a list of 'block'/'complete', OLDEST first). Returns the
    reservation base. Block evidence and completion work touch DISJOINT files so
    both commits coexist on the branch — only their trailer ORDER differs."""
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, tid, [wid], head) is None
    wt = tmp_path / ("wt-" + tid)
    _git(repo, "worktree", "add", str(wt), "llm/train/" + tid)
    for kind in order:
        if kind == "block":
            (wt / (wid + "-why.txt")).write_text("stuck", encoding="utf-8")
            _git(wt, "add", "-A")
            _git(
                wt,
                "commit",
                "-q",
                "-m",
                "blocked {0}\n\nBlocked-WI: {0}\nBlockRef: OI-42\n".format(wid),
            )
        else:
            (wt / ("work-" + wid + ".txt")).write_text("done", encoding="utf-8")
            _git(wt, "add", "-A")
            _git(
                wt,
                "commit",
                "-q",
                "-m",
                "build {0}\n\nWI: {0}\nTrain: {1}\nBase: {2}\n".format(wid, tid, head),
            )
    return head


def test_completion_supersedes_older_block_and_integrates_without_disposition(tmp_path):
    # WI-239 regression 1. A train that blocked and was then CURED (an older
    # Blocked-WI, a newer WI: completion in a later novel commit) classifies
    # ready-to-integrate and integrates through the successful path — never the
    # blocked disposition. The completed work is preserved, not discarded.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    base = _reserve_train_with_trailers(tmp_path, repo, "t-cure", ["block", "complete"])
    # The latest trailer wins: the newer completion supersedes the older block.
    built, blocked = agent_loop.train_branch_evidence(repo, "t-cure", base)
    assert built == {"WI-201"} and blocked == {}, (built, blocked)

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "WI-201" in _done_rows(repo, "refs/heads/llm/integration")
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert "blocked-disposition" not in events, "a cured blocker takes the DONE path"
    assert len(_integrations_for(repo)) == 1, "the train integrated once"
    assert _reservations(repo) == set()


def test_older_completion_then_newer_block_still_classifies_blocked(tmp_path):
    # WI-239 regression 2. The supersede is directional: an OLDER WI: completion
    # followed by a NEWER Blocked-WI (the block is newer truth) stays blocked —
    # the completion does NOT retract a subsequent block.
    repo = _make_repo(tmp_path, [_wi_row("WI-201")])
    base = _reserve_train_with_trailers(tmp_path, repo, "t-blk", ["complete", "block"])
    built, blocked = agent_loop.train_branch_evidence(repo, "t-blk", base)
    assert built == set() and blocked == {"WI-201": "OI-42"}, (built, blocked)
    dispatcher = agent_loop.agent_dispatch
    state, foreign = dispatcher._train_evidence_decision(["WI-201"], built, blocked)
    assert state == "blocked" and foreign == ()


def test_trailer_ordering_direction_latest_wins_both_ways(tmp_path):
    # WI-239 regression 3 — the off-by-one guard. `git log` emits newest-first;
    # classification must read that direction so the LATEST trailer wins in BOTH
    # commit orders. Reading oldest-first (or first-seen from the wrong end)
    # would invert exactly one of these.
    repo = _make_repo(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    b1 = _reserve_train_with_trailers(
        tmp_path, repo, "t-bc", ["block", "complete"], wid="WI-201"
    )
    built_bc, blocked_bc = agent_loop.train_branch_evidence(repo, "t-bc", b1)
    b2 = _reserve_train_with_trailers(
        tmp_path, repo, "t-cb", ["complete", "block"], wid="WI-202"
    )
    built_cb, blocked_cb = agent_loop.train_branch_evidence(repo, "t-cb", b2)
    # block→complete: newest is the completion -> built. complete→block: newest
    # is the block -> blocked. The two orders yield OPPOSITE verdicts.
    assert (built_bc, blocked_bc) == ({"WI-201"}, {})
    assert (built_cb, blocked_cb) == (set(), {"WI-202": "OI-42"})


def test_blocked_train_resume_is_idempotent_until_the_head_advances(tmp_path):
    # WI-239 regression 4. A reserved train classified blocked gets ONE resume
    # per changed input, keyed on the integration head recorded at each
    # blocked-exit. A first sighting resumes (the base may have moved since the
    # block); an UNCHANGED head then dispositions (no infinite resume); an
    # ADVANCED head (the cure shape) resumes once more and re-records.
    repo = _make_repo(tmp_path, [_wi_row("WI-201")])
    base = _reserve_train_with_trailers(tmp_path, repo, "t-idem", ["block"])
    dispatcher = agent_loop.agent_dispatch

    # First sighting (no record): resume, and the head is recorded durably.
    assert dispatcher._blocked_recovery_state(repo, "t-idem") == "resume"
    rec = dispatcher.read_blocked(repo, "t-idem")
    assert rec is not None and rec["ihead"] == base, rec
    blocked_refs = _git(
        repo, "for-each-ref", "--format=%(refname)", "refs/llm/blocked"
    ).splitlines()
    assert blocked_refs, "the blocked-exit head is recorded durably in git"

    # Unchanged head since the recorded exit -> disposition (never loops).
    assert dispatcher._blocked_recovery_state(repo, "t-idem") == "blocked"
    assert dispatcher._blocked_recovery_state(repo, "t-idem") == "blocked"

    # The integration head advances (a parallel train fixed the base): the cure
    # shape -> resume once more, re-recording the new head; then it converges.
    ihead = _git(repo, "rev-parse", "refs/heads/llm/integration")
    tree = _git(repo, "rev-parse", ihead + "^{tree}")
    moved = _git(repo, "commit-tree", tree, "-p", ihead, "-m", "parallel base fix")
    _git(repo, "update-ref", "refs/heads/llm/integration", moved)
    assert dispatcher._blocked_recovery_state(repo, "t-idem") == "resume"
    assert dispatcher.read_blocked(repo, "t-idem")["ihead"] == moved
    assert dispatcher._blocked_recovery_state(repo, "t-idem") == "blocked"


def test_wi229_field_shape_resumed_worker_supersedes_and_integrates(tmp_path):
    # WI-239 regression 5 — the WI-229 field shape end-to-end. A train blocked on
    # a base defect is left reserved; the base is fixed out-of-band (the
    # integration head advances, the sanctioned resync). On the next dispatch the
    # reserved blocked train's head has advanced, so reconcile RESUMES the worker
    # rather than dispositioning; the resumed worker re-runs green and commits the
    # WI: completion, superseding its own block; the train integrates through the
    # DONE path — no disposition, no discarded work.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    base = _reserve_train_with_trailers(tmp_path, repo, "t-229", ["block"])
    # A prior blocked-exit was recorded at the block's head (the disposition was
    # deferred — the WI-229 shape). The base is then fixed out-of-band.
    agent_loop.agent_dispatch.record_blocked(repo, "t-229", base)
    iwt = tmp_path / "iwt"
    _git(repo, "worktree", "add", str(iwt), "llm/integration")
    (iwt / "basefix.txt").write_text("the dupes-census race, fixed", encoding="utf-8")
    _git(iwt, "add", "-A")
    _git(iwt, "commit", "-q", "-m", "fix the base defect (dupes-census race)")
    _git(repo, "worktree", "remove", "--force", str(iwt))

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert '"state": "resume"' in events, "the cured blocked train is resumed"
    assert "blocked-disposition" not in events, "the cure superseded the block"
    # The resumed worker ran a real session and superseded with a completion.
    assert (ctl / "sessions.txt").read_text("utf-8").count("s") == 1
    assert "WI-201" in _done_rows(repo, "refs/heads/llm/integration")
    # No work discarded: the block's evidence file rode into the integration.
    show = _git(repo, "ls-tree", "-r", "--name-only", "refs/heads/llm/integration")
    assert "WI-201-why.txt" in show and "work-WI-201.txt" in show
    assert _reservations(repo) == set()
    assert not _git(
        repo, "for-each-ref", "--format=%(refname)", "refs/llm/blocked"
    ).strip(), "the spent blocked-exit record is cleared on integrate"


def test_fault_points_exist_for_every_matrix_boundary(tmp_path):
    # The matrix's own coverage guard: every boundary named by TC-065 has a
    # wired fault point (a renamed constant would silently skip a test). The
    # reservation/integration/publish machinery lives in agent_dispatch.py
    # since the WI-218 split.
    src = (SCRIPTS / "agent_dispatch.py").read_text(encoding="utf-8")
    for point in (
        "reserve-pre-txn",
        "reserve-post-txn",
        "pre-integration-cas",
        "post-integration-cas",
        "post-intent",
        "post-dev-cas",
    ):
        assert '_fault("{}")'.format(point) in src, point
