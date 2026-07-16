"""Parallel telemetry + downstream migration + generated surfaces — Slice H
(WI-186, SR-065/SR-059/LLR-066/LLR-060/TC-066/TC-060;
docs/specs/parallel-wi-dispatch.md §13/§14).

The load-bearing guarantees:

  - telemetry is reason-coded and aggregated by (run, train, WI, session) with
    NO cross-run id collision; the end-of-run summary reports the required
    measurements; the banner reports lanes/frontier/queue/ceiling;
  - the two-worker promotion is GATED: a repo holds at --jobs 1 until BOTH the
    SafetyClass audit (every open WI classified) and the soft-edge audit
    (signed via docs/parallel-ready) pass — a fresh scaffold passes by
    construction, and the deliberate flip is recorded;
  - legacy `active` rows reconcile to queued with a logged finding, and
    docs/tracks/* is flagged within the one compatibility window;
  - SR-059: a fresh scaffold ships no next-wi/run-phase and parallel-by-default,
    status.md is integrator-generated + marker-gated, run-state is a generated
    dispatcher outcome;
  - a non-adopting repo (no --jobs / AGENT_JOBS) is completely unaffected.
"""

import csv
import json
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, run_py

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
        "SR-065",
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
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
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


def _dispatch(repo, template, jobs="2"):
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
        ],
        cwd=repo,
    )


def _events(repo):
    p = repo / "out" / "dispatch" / "events.jsonl"
    if not p.exists():
        return []
    return [
        json.loads(ln)
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


# --- telemetry (SR-065 first half) ----------------------------------------------


def test_events_carry_a_run_id_and_no_cross_run_collision(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    _dispatch(repo, template)
    # A second launch over fresh work: a distinct run id, appended to the same
    # journal — so aggregation by run never conflates the two.
    (repo / "docs" / "requirements" / "work-items.csv").write_text(
        (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
        + "WI-203,Work WI-203,ws,SR-065,,queued,,docs/specs/thing.md,"
        "medium,ordinary\n",
        encoding="utf-8",
    )
    _git(repo, "commit", "-qam", "add WI-203")
    _dispatch(repo, template)

    events = _events(repo)
    runs = {e["run"] for e in events}
    assert len(runs) == 2, "each launch is a distinct run id"
    assert all(e.get("run") for e in events), "every event is run-stamped"
    # The telemetry summary is per-run: the second summary counts only its own
    # single reservation, never the first run's two.
    tel = json.loads((repo / "out" / "dispatch" / "telemetry.json").read_text("utf-8"))
    assert tel["reservations"] == 1 and tel["integrations"] == 1


def test_telemetry_summary_and_banner_content(tmp_path):
    repo, ctl, template = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202"), _wi_row("WI-203")]
    )
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    # The banner reports lanes / frontier / integration-queue / ceiling.
    assert "dispatch banner |" in proc.stdout
    assert "ceiling 2" in proc.stdout
    # The end-of-run telemetry rollup (the required measurements).
    assert "dispatch telemetry |" in proc.stdout
    tel = json.loads((repo / "out" / "dispatch" / "telemetry.json").read_text("utf-8"))
    for key in (
        "reservations",
        "integrations",
        "conflicts",
        "re_reviews_needed",
        "reconciles",
        "quarantines",
        "bar_failures",
    ):
        assert key in tel
    assert tel["reservations"] == 3 and tel["integrations"] == 3
    assert tel["bar_failures"] == 0


# --- the migration gate (SR-065 second half) ------------------------------------


def test_assess_migration_fresh_scaffold_passes(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    a = agent_loop.assess_migration(repo)
    assert a["safetyclass_ok"] and a["softedge_ok"]
    assert a["soft_edges"] == [] and a["legacy_active"] == []


def test_unclassified_open_wi_holds_the_ceiling(tmp_path):
    repo, ctl, template = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202", safety="")]
    )
    proc = _dispatch(repo, template, jobs="2")
    assert "MIGRATION HOLD" in proc.stdout
    assert "ceiling 1" in proc.stdout
    events = _events(repo)
    holds = [e for e in events if e["event"] == "migration-hold"]
    assert holds and "unclassified-open-wi:WI-202" in holds[0]["reason"]
    # No parallel-enabled promotion was recorded while held.
    assert not any(e["event"] == "parallel-enabled" for e in events)


def test_soft_edge_holds_until_signed_then_records_flip(tmp_path):
    # A soft (~) predecessor edge is optimistic-run-together evidence that must
    # be human-audited before first parallel enable.
    repo, ctl, template = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202", preds="~WI-201")]
    )
    a = agent_loop.assess_migration(repo)
    assert a["soft_edges"] == [("WI-202", "WI-201")] and not a["softedge_ok"]

    proc = _dispatch(repo, template, jobs="2")
    assert "MIGRATION HOLD" in proc.stdout
    holds = [e for e in _events(repo) if e["event"] == "migration-hold"]
    assert holds and "soft-edge-audit-unsigned" in holds[0]["reason"]

    # Sign off: docs/parallel-ready records the human audit. Now the flip is
    # allowed and recorded as a deliberate promotion.
    (repo / "docs" / "parallel-ready").write_text(
        "soft-edge audit signed 2026-07-16\n", encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "sign parallel-ready")
    proc = _dispatch(repo, template, jobs="2")
    assert "MIGRATION HOLD" not in proc.stdout
    flips = [e for e in _events(repo) if e["event"] == "parallel-enabled"]
    assert flips and flips[-1]["ceiling"] == 2


def test_legacy_active_rows_and_tracks_reconcile(tmp_path):
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201", status="active"), _wi_row("WI-202")],
    )
    (repo / "docs" / "tracks" / "oldlane").mkdir(parents=True)
    (repo / "docs" / "tracks" / "oldlane" / "status.md").write_text("x", "utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "legacy residue")

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    events = _events(repo)
    recon = [e for e in events if e["event"] == "legacy-active-reconciled"]
    assert recon and "WI-201" in recon[0]["wis"]
    assert any(e["event"] == "legacy-tracks-flagged" for e in events)
    # The reconciled row is queued (and then built) — never left `active`.
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert ",active," not in reg


def test_non_adopting_repo_is_unaffected(tmp_path):
    # No --jobs / AGENT_JOBS: the legacy single-session resume loop runs, and
    # not a single parallel-dispatch artifact appears.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    (repo / "docs" / "status.md").write_text(
        "# Status\n\n## Current State\n\n- nothing\n", encoding="utf-8"
    )
    (repo / "docs" / "run-state").write_text("DONE\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "status")
    proc = run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template.replace("{prompt}", "ignored"),
            "--pause",
            "0",
            "--model",
            "test",
            "--max-iterations",
            "1",
        ],
        cwd=repo,
    )
    # The legacy loop reads the pre-set run-state=DONE and exits; no dispatcher.
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert not (repo / "out" / "dispatch").exists()
    assert not agent_loop.list_reservations(repo)


# --- SR-059: fresh-scaffold generated surfaces ----------------------------------


def test_fresh_scaffold_ships_no_next_wi_or_run_phase_and_parallel_default(tmp_path):
    dest = tmp_path / "scaffold"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--stack", "python"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # No retired coordination pointers anywhere in the scaffold.
    assert not (dest / "docs" / "next-wi").exists()
    assert not (dest / "docs" / "run-phase").exists()
    # The launcher ships parallel-by-default (AGENT_JOBS=2).
    sh = (dest / "agent-resume.sh").read_text("utf-8")
    assert 'AGENT_JOBS="2"' in sh
    assert "export" in sh and "AGENT_JOBS" in sh.split("export", 1)[1]
    cmd = (dest / "agent-resume.cmd").read_text("utf-8")
    assert 'set "AGENT_JOBS=2"' in cmd


def test_generated_status_is_marker_gated(tmp_path):
    # SR-059: a hand-authored status.md is NEVER overwritten by the generator
    # (only an absent or already-generated-marked file is), so a migrating repo
    # keeps its authored status until it deliberately adopts the generated one.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    authored = "# My hand-written status\n\nDo not clobber me.\n"
    (repo / "docs" / "status.md").write_text(authored, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "authored status")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    # The authored file survived the integration (marker absent => left alone).
    assert (repo / "docs" / "status.md").read_text("utf-8") == authored

    # Whereas a generated-marked status IS refreshed by the integrator.
    (repo / "docs" / "status.md").write_text(
        "<!-- " + agent_loop.STATUS_GENERATED_MARKER + " -->\nstale\n",
        encoding="utf-8",
    )
    (repo / "docs" / "requirements" / "work-items.csv").write_text(
        (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
        + "WI-202,Work WI-202,ws,SR-065,,queued,,docs/specs/thing.md,"
        "medium,ordinary\n",
        encoding="utf-8",
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "generated-marked status + WI-202")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    regenerated = (repo / "docs" / "status.md").read_text("utf-8")
    assert agent_loop.STATUS_GENERATED_MARKER in regenerated
    assert "Work items:" in regenerated and "stale" not in regenerated
