"""The atomic serialized integrator — scripts/agent_loop.py (WI-184,
SR-063/LLR-064/TC-064; docs/specs/parallel-wi-dispatch.md §9).

The load-bearing guarantees:

  - overlapping trains compose serially against the CURRENT integration HEAD
    and the combined bar always runs (a red declared bar blocks integration
    and leaves the integration ref untouched);
  - a clean 3-way apply integrates WITHOUT re-review, while ANY textual
    conflict parks the train for a focused re-review — never a silent pick;
  - the integration ref advances only by CAS (a stale expected-old fails
    harmlessly), and reservation refs release only AFTER the durable
    disposition advanced;
  - a blocked disposition changes ONLY its WI (Status=blocked + BlockRef +
    trailers) through the same CAS discipline;
  - review verdicts are verified against the EXACT reviewed head — a train
    whose verdict names an older commit does not integrate;
  - publication to the development branch: deferred (untouched, reported) on
    a dirty worktree; resumed idempotently on relaunch; guarded by the
    durable publish-intent ref so a crash between the dev-ref CAS and the
    worktree sync finishes idempotently instead of reading as user dirt;
  - an absent integration ref with dispatcher-owned evidence fails closed
    (never silently re-seeded from the development branch).
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
    "BlockRef",
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
        "SR-063",
        preds,
        status,
        "shipped" if status == "done" else "",
        "docs/specs/thing.md",
        "medium",
        safety,
        "",
    ]


def _make_repo(tmp_path, rows, stack_test=None):
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
    if stack_test:
        (repo / "docs" / "stack.ini").write_text(
            "[stack]\ntest = {}\n".format(stack_test), encoding="utf-8"
        )
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


# Fake worker: commits the trailer protocol. `shared` mode also writes a
# SHARED path with train-specific content (the overlap/conflict fixture).
FAKE = r"""
import argparse, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
wi = re.search(r"- WI: (WI-\d+)", args.prompt).group(1)
train = re.search(r"- Train: (\S+) \(branch", args.prompt).group(1)
base = re.search(r"integration base ([0-9a-f]+)\)", args.prompt).group(1)
mode = (ctl / "mode").read_text().strip() if (ctl / "mode").exists() else ""
pathlib.Path("work-" + wi + ".txt").write_text("work", encoding="utf-8")
if mode == "shared":
    pathlib.Path("shared.txt").write_text("content from " + wi, encoding="utf-8")
subprocess.run(["git", "add", "-A"], check=True)
msg = "build " + wi + "\n\nWI: " + wi + "\nTrain: " + train + "\nBase: " + base + "\n"
subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
sys.exit(0)
"""


def _setup(tmp_path, rows, stack_test=None):
    repo = _make_repo(tmp_path, rows, stack_test=stack_test)
    ctl = tmp_path / "ctl"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    return repo, ctl, template


def _dispatch(repo, template, *extra, jobs="2"):
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


# --- composition, bar, trailers ---------------------------------------------------


def test_serial_composition_with_trailers_and_bar(tmp_path):
    # Two disjoint trains integrate serially; each integration commit carries
    # Integrated-WI/Train-Head trailers, the declared bar runs on the composed
    # tree, and the dev branch receives BOTH via publication.
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201"), _wi_row("WI-202")],
        stack_test='"{}" -c "import sys; sys.exit(0)"'.format(sys.executable),
    )
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    log = _git(repo, "log", "--format=%s%n%(trailers)", "HEAD")
    assert log.count("integrate: train") == 2
    assert "Integrated-WI: WI-201" in log and "Integrated-WI: WI-202" in log
    assert "Train-Head:" in log
    bars = [e for e in _events(repo) if e["event"] == "integration-bar"]
    assert len(bars) == 2 and all(b["result"] == "pass" for b in bars)
    # Durable evidence landed: log entries + regenerated artifacts on dev.
    assert "integrated train" in (repo / "docs" / "log.md").read_text("utf-8")
    assert (repo / "docs" / "iteration_index.md").exists()
    assert _reservations(repo) == set()


def test_red_combined_bar_blocks_integration_and_cas(tmp_path):
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201")],
        stack_test='"{}" -c "import sys; sys.exit(1)"'.format(sys.executable),
    )
    before = _git(repo, "rev-parse", "HEAD")
    proc = _dispatch(repo, template)
    # The train parks for rework; nothing integrates, the integration ref and
    # the dev branch stay exactly where they were, the reservation is HELD.
    assert proc.returncode == agent_loop.EXIT_STALL, proc.stdout + proc.stderr
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == before
    assert _git(repo, "rev-parse", "HEAD") == before
    assert _reservations(repo) == {"WI-201"}
    events = _events(repo)
    assert any(
        e["event"] == "integration-parked" and e["state"] == "rework" for e in events
    )
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert ",done," not in reg, "a red bar must never produce a done row"


def test_conflict_forces_focused_re_review_clean_apply_does_not(tmp_path):
    # Two trains write DIFFERENT content to the SAME path: the first composes
    # cleanly (no re-review), the second hits a textual conflict and parks
    # needs-re-review — its WIs never done, its reservations held.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    (ctl / "mode").write_text("shared", encoding="utf-8")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_STALL, proc.stdout + proc.stderr

    events = _events(repo)
    integrated = [e for e in events if e["event"] == "integrated"]
    conflicts = [e for e in events if e["event"] == "integration-conflict"]
    assert len(integrated) == 1, "the first train takes the clean fast path"
    assert len(conflicts) >= 1, "the second must hit the conflict, not a pick"
    parked = [
        e
        for e in events
        if e["event"] == "integration-parked" and e["state"] == "needs-re-review"
    ]
    assert parked, "a conflict demands a focused re-review"
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert reg.count(",done,") == 1, "only the cleanly-applied WI is done"
    assert len(_reservations(repo)) == 1, "the conflicted train keeps its claim"


# --- CAS + fail-closed unit surfaces ----------------------------------------------


def test_cas_ref_stale_old_fails_harmlessly(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    a = _git(repo, "rev-parse", "HEAD")
    (repo / "x.txt").write_text("x", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "second")
    b = _git(repo, "rev-parse", "HEAD")
    assert agent_loop.cas_ref(repo, "refs/heads/llm/integration", a, None)
    # Stale expected-old: the ref already moved to a — a CAS from b must fail
    # without touching it.
    assert not agent_loop.cas_ref(repo, "refs/heads/llm/integration", b, b)
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == a
    # And the honest CAS succeeds.
    assert agent_loop.cas_ref(repo, "refs/heads/llm/integration", b, a)


def test_absent_integration_ref_with_evidence_fails_closed(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    err = agent_loop.reserve_traincar(repo, "t-orphan", ["WI-201"], head)
    assert err is None
    # Reservation evidence exists but no integration ref: the dispatcher must
    # fail closed, never silently re-seed from the development branch.
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "fails closed" in (proc.stdout + proc.stderr)


def test_stale_review_verdict_does_not_integrate(tmp_path):
    # A verdict naming an OLDER head than the reviewed train tip must not
    # count (spec §8: a verdict belongs to the exact reviewed commit).
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t-stale", ["WI-201"], head) is None
    # Build the WI on the train branch with a verdict naming a BOGUS sha.
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-stale")
    (wt / "work.txt").write_text("w", encoding="utf-8")
    vdir = wt / "docs" / "reviews" / "t-stale"
    vdir.mkdir(parents=True)
    (vdir / "001-REVIEW-A-0000000.md").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "build WI-201\n\nWI: WI-201\nTrain: t-stale\nBase: {}\n".format(head),
    )
    state, detail = agent_loop.integrate_train(
        repo,
        repo / "docs",
        agent_loop._Journal(repo),
        "t-stale",
        ["WI-201"],
        head,
        required_verdicts=1,
    )
    assert state == "rework" and "0 approval(s)" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == head


# --- publication + the intent protocol --------------------------------------------


def test_dirty_dev_worktree_defers_publication_then_relaunch_publishes(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    # Tracked dirt in the primary worktree (untracked files never count).
    (repo / "AGENTS.md").write_text("# agents (edited, uncommitted)\n", "utf-8")
    dev_before = _git(repo, "rev-parse", "HEAD")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    # Integration advanced; publication deferred; checkout untouched.
    integ = _git(repo, "rev-parse", "refs/heads/llm/integration")
    assert integ != dev_before
    assert _git(repo, "rev-parse", "HEAD") == dev_before
    assert (repo / "AGENTS.md").read_text("utf-8").startswith("# agents (edited"), (
        "a dirty checkout is never reset or stashed"
    )
    assert any(e["event"] == "publish-deferred" for e in _events(repo))
    # run-state stays RUNNING: the published projection lags the authority.
    assert (repo / "docs" / "run-state").read_text().startswith("RUNNING")

    # Clean the dirt and relaunch: recovery resumes the publication
    # idempotently (spec §11 "llm/integration ahead of the development ref").
    _git(repo, "checkout", "--", "AGENTS.md")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert _git(repo, "rev-parse", "HEAD") == integ
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
    assert code != 0, "a completed publication deletes its intent"
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert "WI-201,Work WI-201,ws,SR-063,,done," in reg


def test_crash_between_dev_cas_and_sync_recovers_idempotently(tmp_path):
    # Simulate the §11 row: the dev ref already equals the intent's target but
    # the worktree/index still sit at the expected OLD hash. Recovery must
    # finish the sync (reset to target + delete the intent) — never classify
    # the mechanically stale checkout as user dirt.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    old = _git(repo, "rev-parse", "HEAD")
    # Build a target commit on the integration ref.
    (repo / "landed.txt").write_text("landed", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integrated content")
    target = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", old)  # dev checkout back at the old hash
    _git(repo, "update-ref", "refs/heads/llm/integration", target)
    # The crash left: intent ref written, dev ref CAS'd to target, sync unrun.
    tree = _git(repo, "rev-parse", target + "^{tree}")
    meta = json.dumps(
        {
            "train": "publish",
            "wis": ["publish"],
            "base": target,
            "target": target,
            "old": old,
            "ref": "refs/heads/" + _git(repo, "branch", "--show-current"),
        },
        sort_keys=True,
    )
    intent = _git(repo, "commit-tree", tree, "-p", target, "-m", meta)
    _git(repo, "update-ref", "refs/llm/publish-intent", intent)
    branch = _git(repo, "branch", "--show-current")
    _git(repo, "update-ref", "refs/heads/" + branch, target)

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state in ("noop", "published"), detail
    assert _git(repo, "rev-parse", "HEAD") == target
    assert (repo / "landed.txt").exists(), "the sync completed"
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
    assert code != 0, "the finished intent is deleted"


def test_publish_refuses_a_non_descendant_integration_target(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    base = _git(repo, "rev-parse", "HEAD")
    branch = _git(repo, "branch", "--show-current")

    (repo / "integration-only.txt").write_text("integration", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integration side")
    integration_head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", base)

    (repo / "development-only.txt").write_text("development", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "development side")
    development_head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", integration_head)

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state == "deferred"
    assert integration_head in detail and development_head in detail
    assert _git(repo, "rev-parse", "refs/heads/" + branch) == development_head
    event = [e for e in _events(repo) if e["event"] == "publish-deferred"][-1]
    assert event["reason"] == "non-descendant-target"
    assert event["integration_head"] == integration_head
    assert event["development_head"] == development_head


def test_relaunch_pages_before_work_when_integration_and_dev_diverge(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    base = _git(repo, "rev-parse", "HEAD")

    (repo / "integration-only.txt").write_text("integration", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integration side")
    integration_head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", base)

    dev_commits = []
    for number in (1, 2):
        (repo / "dev-{}.txt".format(number)).write_text(
            "development {}".format(number), encoding="utf-8"
        )
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "development {}".format(number))
        dev_commits.append(_git(repo, "rev-parse", "HEAD"))
    development_head = dev_commits[-1]
    _git(repo, "update-ref", "refs/heads/llm/integration", integration_head)

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert _git(repo, "rev-parse", "HEAD") == development_head
    for commit in dev_commits:
        assert _git(repo, "merge-base", "--is-ancestor", commit, "HEAD") == ""
    assert not list((repo / "out" / "dispatch" / "trains").glob("*.json"))

    run_state = (repo / "docs" / "run-state").read_text(encoding="utf-8")
    assert run_state.startswith("NEEDS-HUMAN") and "ask:" in run_state
    assert integration_head in run_state and development_head in run_state
    event = [e for e in _events(repo) if e["event"] == "integration-diverged"][-1]
    assert event["integration_head"] == integration_head
    assert event["development_head"] == development_head


def test_disposition_regeneration_is_artifact_gated_and_ordered(tmp_path, monkeypatch):
    worktree = tmp_path / "wt"
    (worktree / "docs" / "okf").mkdir(parents=True)
    (worktree / "PROJECT_STATE.html").write_text("dashboard", encoding="utf-8")
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((__import__("pathlib").Path(argv[1]).name, kwargs["cwd"]))
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(agent_loop.agent_dispatch.subprocess, "run", fake_run)
    ok, detail = agent_loop.agent_dispatch._regenerate_disposition_artifacts(worktree)
    assert ok and detail == ""
    assert [name for name, cwd in calls] == ["gen_okf.py", "gen_trajectory.py"]
    assert all(cwd == str(worktree) for name, cwd in calls)

    calls[:] = []
    (worktree / "docs" / "okf").rename(worktree / "docs" / "okf-disabled")
    (worktree / "PROJECT_STATE.html").unlink()
    ok, detail = agent_loop.agent_dispatch._regenerate_disposition_artifacts(worktree)
    assert ok and detail == "" and calls == []


def test_dual_plan_regen_failure_salvages_round_evidence(tmp_path, monkeypatch):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    def fake_round(worktree, wid, row, template, model, timeout, prompt_map):
        round_dir = worktree / "docs" / "plans" / "DP-001-wi-201"
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT A", encoding="utf-8")
        return "SELECTED", "plan A"

    monkeypatch.setattr(agent_loop.agent_dispatch, "run_dual_plan_round", fake_round)
    monkeypatch.setattr(
        agent_loop.agent_dispatch,
        "_regenerate_disposition_artifacts",
        lambda worktree: (
            False,
            "disposition regen failed (gen_okf.py): injected failure",
        ),
    )
    state, detail = agent_loop.dual_plan_disposition(
        repo,
        agent_loop._Journal(repo),
        "t-dual",
        "WI-201",
        {},
        "unused",
        "unused",
        1,
        {},
    )
    assert state == "error"
    assert "disposition regen failed (gen_okf.py): injected failure" in detail
    assert "round evidence salvaged to" in detail
    salvaged = (
        repo
        / "out"
        / "dispatch"
        / "salvage"
        / "t-dual"
        / "DP-001-wi-201"
        / "verdict.md"
    )
    assert salvaged.read_text(encoding="utf-8") == "SELECT A"


def test_select_disposition_passes_the_kit_freshness_hook(tmp_path, monkeypatch):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    req = repo / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(
        "# Stakeholder Needs\n\n"
        "| SN-ID | Need | Why | Priority | Acceptance intent |\n"
        "|---|---|---|---|---|\n"
        "| SN-063 | Safe disposition commits. | Preserve work. | Must | "
        "Fresh generated views. |\n",
        encoding="utf-8",
    )
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        "SR-063,Safe disposition,SN-063,The system shall preserve disposition "
        "work.,Safety.,Generated views are fresh.,,M,Test,Verified\n",
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
        "LLR-063,SR-063,Disposition,src,disposition,Regenerates views.,"
        "(see TC-063),Verified\n",
        encoding="utf-8",
    )
    (repo / "docs" / "test").mkdir()
    (repo / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
        "Evidence,Status\n"
        "TC-063,SR-063;LLR-063,Integration,commit,Full,,Fresh views,Yes,"
        "tests/test_agent_loop_integrate.py,Verified\n",
        encoding="utf-8",
    )
    for generator in ("gen_okf.py", "gen_trajectory.py"):
        proc = run_py([SCRIPTS / generator, "--root", repo], cwd=repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed generated artifacts")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    # Enable the shipped hook itself. KIT_SCRIPTS_DIR is its documented
    # downstream override and points it at this checkout's kit scripts.
    _git(repo, "config", "core.hooksPath", str(SCRIPTS.parent / "hooks"))
    monkeypatch.setenv("KIT_SCRIPTS_DIR", str(SCRIPTS))

    def fake_round(worktree, wid, row, template, model, timeout, prompt_map):
        round_dir = worktree / "docs" / "plans" / "DP-001-wi-201"
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT A", encoding="utf-8")
        with (worktree / "docs" / "requirements" / "work-items.csv").open(
            "a", encoding="utf-8", newline=""
        ) as fh:
            csv.writer(fh).writerow(_wi_row("WI-202", preds="WI-201"))
        return "SELECTED", "plan A"

    monkeypatch.setattr(agent_loop.agent_dispatch, "run_dual_plan_round", fake_round)
    state, detail = agent_loop.dual_plan_disposition(
        repo,
        agent_loop._Journal(repo),
        "t-hook",
        "WI-201",
        {},
        "unused",
        "unused",
        1,
        {},
    )
    assert state == "SELECTED", detail
    staging = repo / "out" / "dispatch" / "worktrees" / "integrate-t-hook"
    for generator in ("gen_okf.py", "gen_trajectory.py"):
        proc = run_py([SCRIPTS / generator, "--root", staging, "--check"], cwd=repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr


def test_blocked_disposition_changes_only_its_wi(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t-blk", ["WI-201"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-blk")
    (wt / "evidence.txt").write_text("why it is stuck", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "blocked WI-201\n\nBlocked-WI: WI-201\nBlockRef: OI-42\n",
    )
    journal = agent_loop._Journal(repo)
    state, new_head = agent_loop.blocked_disposition(
        repo, repo / "docs", journal, "t-blk", ["WI-201"], head
    )
    assert state == "integrated", new_head
    # ONLY WI-201 changed, with its BlockRef; the trailers are on the commit.
    show = _git(
        repo, "show", "refs/heads/llm/integration:docs/requirements/work-items.csv"
    )
    assert "WI-201,Work WI-201,ws,SR-063,,blocked" in show and "OI-42" in show
    assert "WI-202,Work WI-202,ws,SR-063,,queued" in show
    log = _git(repo, "log", "-1", "--format=%(trailers)", "refs/heads/llm/integration")
    assert "Blocked-WI: WI-201" in log and "BlockRef: OI-42" in log
    assert _reservations(repo) == set(), "released only after the CAS"
