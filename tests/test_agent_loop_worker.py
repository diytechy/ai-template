"""Explicit worker assignment mode — scripts/agent_loop.py --wi/--train
(WI-181, SR-060/LLR-061/TC-061; docs/specs/parallel-wi-dispatch.md §6).

Exercised the kit way: the real loop as a subprocess against a fake agent in
throwaway git repos, plus the pure helpers direct. The load-bearing guarantees
a broken edit here would silently violate — each the failure mode that would
corrupt a parallel dispatch run:

  - pure helpers: --wi/--train validation (no traversal, no half-assignment),
    the trailer-evidence reader (the worker's ONLY result channel), and the
    assignment prompt (WI row + SpecRef + predecessors + train diff + rework —
    never a status.md resume);
  - a worker runs from the explicit assignment with NO lane files: it never
    reads/writes run-state, never regenerates the iteration index, and its
    committed evidence (trailers) is what makes it DONE — judged from git;
  - two concurrent workers in linked worktrees write non-colliding, train-
    prefixed session logs (collision-safe evidence, SR-060);
  - a Blocked-WI trailer exits 3 (the durable disposition is the integrator's,
    Slice F) — never a silent DONE;
  - preflight fails closed: half a pair, wrong branch, --track combination,
    an unknown or already-done WI;
  - legacy --track still runs its old behavior but warns deprecated (one
    compatibility window; TC-061), and managed review evidence in worker mode
    lands at reviews/<train>/NNN-<PHASE>-<sha7>.md naming the reviewed HEAD.
"""

import csv
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, run_py

agent_loop = load_script("agent_loop")

pytestmark = pytest.mark.skipif(
    not __import__("shutil").which("git"), reason="needs git on PATH"
)


# --- pure helpers -------------------------------------------------------------


@pytest.mark.parametrize("good", ["v4-g2-WI-201-a31f", "t1", "A.B_c-9"])
def test_sanitize_train_accepts_slugs(good):
    assert agent_loop.sanitize_train(good) == good


@pytest.mark.parametrize("bad", ["../x", "x/y", "-x", "x y", "", ".hidden"])
def test_sanitize_train_rejects_traversal_and_junk(bad):
    with pytest.raises(ValueError):
        agent_loop.sanitize_train(bad)


def test_parse_wi_list_orders_and_validates():
    assert agent_loop.parse_wi_list("WI-201") == ["WI-201"]
    assert agent_loop.parse_wi_list("WI-201;WI-204") == ["WI-201", "WI-204"]
    for bad in ("", "WI-", "wi-201", "WI-201;WI-201", "WI-201;junk"):
        with pytest.raises(ValueError):
            agent_loop.parse_wi_list(bad)


# --- repo scaffolding -----------------------------------------------------------

REGISTRY_HEADER = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "Campaign",
    "BuildTier",
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


def _write_registry(repo, rows):
    reg = repo / "docs" / "requirements"
    reg.mkdir(parents=True, exist_ok=True)
    with open(str(reg / "work-items.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(REGISTRY_HEADER)
        w.writerows(rows)


def _make_train_repo(tmp_path, train="t1", wis=("WI-201",)):
    """A throwaway repo on branch llm/train/<train> with a registry carrying
    the assigned WIs (+ a done predecessor for context). Returns (repo, base)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    rows = [
        [
            "WI-200",
            "Predecessor work",
            "ws",
            "SR-001",
            "",
            "done",
            "the shipped predecessor deliverable",
            "docs/specs/thing.md",
            "camp",
            "",
        ]
    ]
    for wid in wis:
        rows.append(
            [
                wid,
                "Scoped work for " + wid,
                "ws",
                "SR-060",
                "WI-200",
                "queued",
                "",
                "docs/specs/thing.md",
                "camp",
                "medium",
            ]
        )
    _write_registry(repo, rows)
    (repo / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    # The scaffold's rule: out/ (locks, raw run logs) is runtime state, never
    # tracked — the worker's clean-tree DONE check depends on it.
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "checkout", "-q", "-b", "llm/train/" + train)
    return repo, _git(repo, "rev-parse", "HEAD")


# The fake worker driver: reads its assignment (WI/train/base) out of the
# prompt the loop composed, does one unit of work, and commits it with the
# trailer protocol — the worker contract's result channel. Control knobs:
# `mode=blocked` commits a Blocked-WI trailer instead; `mode=notrailer`
# commits without any trailer (an incomplete session).
FAKE_WORKER = r"""
import argparse, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "prompts.txt"), "a", encoding="utf-8") as fh:
    fh.write("=== session ===\n" + args.prompt + "\n")
v = re.search(r"Write your verdict to (\S+)", args.prompt)
if v:
    vpath = pathlib.Path(v.group(1))
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text(
        "- [MINOR] work.txt:1 -> a nit -> tidy it -> @owner\n"
        "VERDICT: APPROVE findings=1\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", str(vpath)], check=True)
    subprocess.run(["git", "commit", "-q", "-m", "review verdict"], check=True)
    sys.exit(0)
wi = re.search(r"- WI: (WI-\d+)", args.prompt).group(1)
train = re.search(r"- Train: (\S+) \(branch", args.prompt).group(1)
base = re.search(r"integration base ([0-9a-f]+)\)", args.prompt).group(1)
mode = (ctl / "mode").read_text().strip() if (ctl / "mode").exists() else "build"
work = pathlib.Path("work-" + wi + ".txt")
work.write_text("work for " + wi, encoding="utf-8")
subprocess.run(["git", "add", "-A"], check=True)
if mode == "blocked":
    msg = "blocked " + wi + "\n\nBlocked-WI: " + wi + "\nBlockRef: OI-99\n"
elif mode == "notrailer":
    msg = "wip " + wi + " (no trailer yet)"
else:
    msg = "build " + wi + "\n\nWI: " + wi + "\nTrain: " + train + "\nBase: " + base + "\n"
subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
sys.exit(0)
"""


def _worker(repo, fake, ctl, *extra, max_iterations=6):
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
            "--model",
            "test",
            "--max-iterations",
            str(max_iterations),
            *extra,
        ],
        cwd=repo,
    )


def _setup(tmp_path, train="t1", wis=("WI-201",)):
    repo, base = _make_train_repo(tmp_path, train=train, wis=wis)
    ctl = tmp_path / "ctl"
    ctl.mkdir()
    fake = tmp_path / "fake_worker.py"
    fake.write_text(FAKE_WORKER, encoding="utf-8")
    return repo, base, ctl, fake


# --- the worker contract end-to-end -------------------------------------------


def test_worker_builds_assignment_and_exits_done(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "worker t1 [WI-201]: DONE" in proc.stdout

    # The result is committed evidence: the WI trailer on the train branch.
    trailers = _git(repo, "log", "--format=%(trailers:key=WI,valueonly)", "HEAD")
    assert "WI-201" in trailers.split()
    # Collision-safe train-prefixed session log; NO lane files, NO generated
    # index, NO run-state, NO tracks lane (SR-060 AC).
    assert list((repo / "docs" / "iteration").glob("t1-001-*.log"))
    assert not (repo / "docs" / "iteration_index.md").exists()
    assert not (repo / "docs" / "run-state").exists()
    assert not (repo / "docs" / "tracks").exists()
    # The prompt was assembled from the assignment — WI row + SpecRef +
    # predecessor context + trailer protocol — never a status.md resume.
    prompt = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert "- WI: WI-201 — Scoped work for WI-201" in prompt
    assert "SpecRef: docs/specs/thing.md" in prompt
    assert "WI-200 [done]" in prompt  # predecessor context
    assert "resume from docs/status.md and do not" in prompt  # the prohibition
    assert "WI: WI-201" in prompt  # the trailer protocol
    assert agent_loop.DEFAULT_PROMPT[:60] not in prompt  # never the resume prompt


def test_worker_multi_wi_assignment_builds_in_order(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path, wis=("WI-201", "WI-204"))
    proc = _worker(repo, fake, ctl, "--wi", "WI-201;WI-204", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    prompt = (ctl / "prompts.txt").read_text(encoding="utf-8")
    # Ordered: WI-201's session first, then WI-204's — and WI-204's prompt
    # carries the train diff of the accepted-but-unintegrated WI-201 commit.
    assert prompt.index("- WI: WI-201") < prompt.index("- WI: WI-204")
    assert "Current train diff" in prompt
    trailers = _git(repo, "log", "--format=%(trailers:key=WI,valueonly)", "HEAD")
    assert {"WI-201", "WI-204"} <= set(trailers.split())
    # Two sessions, two train-scoped logs.
    logs = sorted((repo / "docs" / "iteration").glob("t1-*.log"))
    assert len(logs) == 2 and logs[0].name.startswith("t1-001-")


def test_worker_blocked_trailer_exits_blocked(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    (ctl / "mode").write_text("blocked", encoding="utf-8")
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_BLOCKED, proc.stdout + proc.stderr
    assert "BlockRef: OI-99" in proc.stdout
    # The worker never writes the durable disposition — the registry row on
    # the train branch is untouched (the integrator owns Status, Slice F).
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text(
        encoding="utf-8"
    )
    assert "blocked" not in reg.splitlines()[2].lower()


def test_worker_resume_with_complete_evidence_spends_no_session(tmp_path):
    # Recovery semantics (spec §11): a relaunched worker whose train already
    # carries the trailer evidence exits DONE from git alone — no session.
    repo, base, ctl, fake = _setup(tmp_path)
    (repo / "work-WI-201.txt").write_text("done earlier", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(
        repo,
        "commit",
        "-q",
        "-m",
        "build WI-201\n\nWI: WI-201\nTrain: t1\nBase: {}\n".format(base),
    )
    # The dispatcher passes the reservation's base explicitly; the HEAD-at-start
    # default cannot see evidence committed before this relaunch.
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1", "--base", base)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert not (ctl / "prompts.txt").exists(), "spent a session on done work"


def test_worker_stall_guard_still_applies(tmp_path):
    # A session that commits WITHOUT the trailer makes progress commits but
    # never completes the assignment; the budget ceiling must end the run
    # (never an infinite worker), reporting the still-RUNNING state.
    repo, base, ctl, fake = _setup(tmp_path)
    (ctl / "mode").write_text("notrailer", encoding="utf-8")
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1", max_iterations=2)
    assert proc.returncode == agent_loop.EXIT_BUDGET, proc.stdout + proc.stderr


# --- two concurrent workers: collision-safe evidence (TC-061) -------------------


def test_two_concurrent_workers_write_non_colliding_evidence(tmp_path):
    repo, base = _make_train_repo(tmp_path, train="t1", wis=("WI-201", "WI-204"))
    # Second train branch + linked worktrees, one per worker (spec §6). The
    # primary checkout returns to the development branch — a train branch is
    # checked out ONLY in its leased worktree.
    _git(repo, "checkout", "-q", "-")
    _git(repo, "branch", "llm/train/t2", base)
    wt1 = tmp_path / "wt1"
    wt2 = tmp_path / "wt2"
    _git(repo, "worktree", "add", str(wt1), "llm/train/t1")
    _git(repo, "worktree", "add", str(wt2), "llm/train/t2")
    fake = tmp_path / "fake_worker.py"
    fake.write_text(FAKE_WORKER, encoding="utf-8")
    ctl1, ctl2 = tmp_path / "c1", tmp_path / "c2"
    ctl1.mkdir()
    ctl2.mkdir()

    def spawn(wt, ctl, wi, train):
        template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
            sys.executable, fake, ctl
        )
        return subprocess.Popen(
            [
                sys.executable,
                str(SCRIPTS / "agent_loop.py"),
                "--root",
                str(repo),
                "--worktree",
                str(wt),
                "--agent-cmd",
                template,
                "--pause",
                "0",
                "--model",
                "test",
                "--max-iterations",
                "4",
                "--wi",
                wi,
                "--train",
                train,
            ],
            cwd=str(wt),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
        )

    p1 = spawn(wt1, ctl1, "WI-201", "t1")
    p2 = spawn(wt2, ctl2, "WI-204", "t2")
    out1, _ = p1.communicate(timeout=180)
    out2, _ = p2.communicate(timeout=180)
    assert p1.returncode == agent_loop.EXIT_DONE, out1
    assert p2.returncode == agent_loop.EXIT_DONE, out2

    # Non-colliding committed evidence: each train's session log is prefixed
    # with ITS train id, so the two branches integrate without a path clash.
    logs1 = {p.name for p in (wt1 / "docs" / "iteration").glob("*.log")}
    logs2 = {p.name for p in (wt2 / "docs" / "iteration").glob("*.log")}
    assert logs1 and logs2 and not (logs1 & logs2)
    assert all(n.startswith("t1-") for n in logs1)
    assert all(n.startswith("t2-") for n in logs2)
    # Neither worker touched the primary worktree's docs/ or any lane file.
    assert not (repo / "docs" / "iteration").exists()
    assert not (repo / "docs" / "run-state").exists()


# --- managed routing in worker mode: review evidence names the reviewed HEAD ----


def test_worker_review_evidence_names_exact_reviewed_commit(tmp_path):
    # Managed mode + review-policy 1 inside a worker: the verdict file lands at
    # reviews/<train>/NNN-REVIEW-A-<sha7>.md where <sha7> is the reviewed code
    # HEAD (SR-060 — a verdict belongs to the exact commit, never a branch
    # tip), and the scoreboard is train-scoped too.
    repo, base, ctl, fake = _setup(tmp_path)
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows = [
        ["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", template, ""],
        ["PROVB-REV-1", "PROVB", "revb", "1", "medium", template, ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text(
        "PROVA-BUILD-1\nPROVB-REV-1\n", encoding="utf-8"
    )
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "wire managed routing")
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    verdicts = list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*.md"))
    assert len(verdicts) == 1, "expected one train-scoped verdict"
    sha7 = verdicts[0].stem.rsplit("-", 1)[1]
    # The named sha is the implementer's commit — the exact reviewed HEAD.
    subjects = _git(repo, "log", "--format=%h %s", "HEAD")
    build_line = [ln for ln in subjects.splitlines() if "build WI-201" in ln][0]
    assert build_line.startswith(sha7[:7])
    assert (repo / "docs" / "reviews" / "t1" / "scoreboard.txt").exists()
    # And no un-scoped lane verdict escaped the train directory.
    assert not list((repo / "docs" / "reviews").glob("*.md"))


# --- preflight fails closed ------------------------------------------------------


def test_wi_without_train_is_preflight_failure(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(repo, fake, ctl, "--wi", "WI-201")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "come as a pair" in (proc.stdout + proc.stderr)


def test_worker_plus_track_is_preflight_failure(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(
        repo, fake, ctl, "--wi", "WI-201", "--train", "t1", "--track", "lane"
    )
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "mutually exclusive" in (proc.stdout + proc.stderr)


def test_worker_off_its_train_branch_fails_closed(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path, train="t1")
    _git(repo, "checkout", "-q", "-b", "llm/train/other", base)
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "must run on its train branch" in (proc.stdout + proc.stderr)


def test_worker_unknown_or_done_wi_fails_closed(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(repo, fake, ctl, "--wi", "WI-999", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "not in docs/requirements" in (proc.stdout + proc.stderr)
    proc = _worker(repo, fake, ctl, "--wi", "WI-200", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "already integrated done" in (proc.stdout + proc.stderr)


# --- the legacy --track compatibility window -------------------------------------


def test_track_still_runs_but_warns_deprecated(tmp_path):
    # TC-061: legacy --track keeps its old behavior within the compatibility
    # window — and now says it is deprecated. (The old behavior itself is
    # pinned by test_agent_loop_tracks.py; here we assert the warning.)
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / "seed.txt").write_text("seed", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "checkout", "-q", "-b", "llm/lane")
    fake = tmp_path / "fake.py"
    fake.write_text(
        "import json, pathlib, subprocess, sys, argparse, time\n"
        "ap = argparse.ArgumentParser()\n"
        "ap.add_argument('--runstate', required=True)\n"
        "ap.add_argument('--model', default='')\n"
        "ap.add_argument('-p', '--prompt', default='')\n"
        "a, _ = ap.parse_known_args()\n"
        "pathlib.Path('w.txt').write_text(str(time.time()))\n"
        "subprocess.run(['git', 'add', '-A'], check=True)\n"
        "subprocess.run(['git', 'commit', '-q', '-m', 'w'], check=True)\n"
        "rs = pathlib.Path(a.runstate)\n"
        "rs.parent.mkdir(parents=True, exist_ok=True)\n"
        "rs.write_text('DONE\\n')\n",
        encoding="utf-8",
    )
    lane = repo / "docs" / "tracks" / "lane"
    template = '"{}" "{}" --runstate "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, lane / "run-state"
    )
    proc = run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--model",
            "test",
            "--max-iterations",
            "2",
            "--track",
            "lane",
        ],
        cwd=repo,
    )
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "--track is deprecated" in proc.stderr
