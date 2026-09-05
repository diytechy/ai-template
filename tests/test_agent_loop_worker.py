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

import argparse
import csv
import functools
import subprocess
import sys

import pytest
from conftest import (
    env_gate_skipif,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    wi_registry_header,
    write_wi_registry,
)

agent_loop = load_script("agent_loop")

pytestmark = env_gate_skipif("git")


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

# Worker mode is exercised against a registry that PREDATES the SafetyClass
# column (9 wide) — that shape is load-bearing here, not staleness: the worker
# never classifies, so it must run on a registry that carries no class.
REGISTRY_HEADER = wi_registry_header(9)
_write_registry = functools.partial(write_wi_registry, header=REGISTRY_HEADER)


def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout.strip()


def _make_train_repo(tmp_path, train="t1", wis=("WI-201",)):
    """A throwaway repo on branch llm/train/<train> with a registry carrying
    the assigned WIs (+ a done predecessor for context). Returns (repo, base)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
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
train = re.search(r"- Branch: (\S+) \(its claim", args.prompt).group(1)
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


def test_worker_prompt_carries_the_context_block_computed_fresh(tmp_path):
    # WI-388 clause 4, consumer 2: `worker_prompt` computes the context block
    # FRESH at claim for every WI (pure registry joins, advisory) and carries
    # the one new instruction line. A repo with no joinable registries gets no
    # block and no dangling header — advisory means absent, never broken.
    work = tmp_path / "docs" / "work"
    (work / "cancelled").mkdir(parents=True)
    (work / "cancelled" / "WI-002-refuted.md").write_text(
        '+++\nid = "WI-002"\ntitle = "refuted"\nsr_refs = ["SR-001"]\n+++\n'
        "\n## Deliverable\n\ncancelled: REFUTED - no driving necessity\n",
        encoding="utf-8",
        newline="\n",
    )
    row = {
        "WI-ID": "WI-005",
        "Title": "the assignment",
        "SR-Refs": "SR-001",
        "Predecessors": "",
        "SpecRef": "seed.txt",
    }
    prompt = agent_loop.worker_prompt(
        tmp_path, {"WI-005": row}, "WI-005", "wi-005", "0" * 7
    )
    assert "read the Context refs below before starting" in prompt
    assert "WI-002" in prompt and "REFUTED" in prompt

    bare = tmp_path / "bare"
    bare.mkdir()
    prompt2 = agent_loop.worker_prompt(bare, {"WI-005": row}, "WI-005", "w", "0" * 7)
    assert "Context refs" not in prompt2


def test_worker_prompt_single_row_carries_no_assignment_block(tmp_path):
    # WI-580 Done-when 2, the byte-identity half: `{assignment_block}` renders
    # EMPTY for a one-row lane, so the single-row brief is what it was — the
    # `- WI:`/`- SR-Refs:`/`- Branch:` lines already say everything the block
    # would repeat. Driven through the real function, and through the block
    # helper directly so the emptiness is the mechanism's, not a coincidence of
    # this fixture's registry.
    row = {
        "WI-ID": "WI-005",
        "Title": "the assignment",
        "SR-Refs": "SR-001",
        "Predecessors": "",
        "SpecRef": "seed.txt",
    }
    rows = {"WI-005": row}
    assert (
        agent_loop.assignment_block(tmp_path, rows, "WI-005", "0" * 7, ["WI-005"]) == ""
    )
    prompt = agent_loop.worker_prompt(tmp_path, rows, "WI-005", "wi-005", "0" * 7)
    assert "WHOLE assignment" not in prompt
    # An explicit one-element assignment renders the same bytes as the default.
    assert prompt == agent_loop.worker_prompt(
        tmp_path, rows, "WI-005", "wi-005", "0" * 7, assigned=["WI-005"]
    )
    # The opening sentence no longer claims ONE work item (it was false for a
    # batch, which is how a session lost a sibling row — plan §0).
    assert "assigned ONE work item" not in prompt
    assert "this session's focus" in prompt


def test_worker_batch_prompt_names_every_assigned_row_and_its_state(tmp_path):
    # WI-580 Done-when 2: a two-id assignment lists BOTH rows with id, title
    # and SpecRef, and the evidence state moves with the walk — session 001
    # sees `this session's focus` / `not started`, session 002 sees the first
    # row as `built` off its committed trailer. Measured defect (2026-09-02,
    # lane `wi-569-…`): the human saw `wi=WI-569;WI-575` in the banner and the
    # session that took WI-569 never learned WI-575 was on its lane.
    repo, base, ctl, fake = _setup(tmp_path, wis=("WI-201", "WI-204"))
    proc = _worker(repo, fake, ctl, "--wi", "WI-201;WI-204", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    first, second = prompts.split("=== session ===\n")[1:3]

    assert "- The WHOLE assignment (2 rows claimed on this lane" in first
    assert (
        "  - WI-201 [this session's focus] Scoped work for WI-201 — "
        "SpecRef: docs/specs/thing.md" in first
    )
    assert "  - WI-204 [not started] Scoped work for WI-204 — SpecRef:" in first
    # Session 002 took WI-204; WI-201's committed `WI:` trailer is the same
    # evidence `current_assignment_wi` walked past it on.
    assert "  - WI-201 [built] Scoped work for WI-201 — SpecRef:" in second
    assert "  - WI-204 [this session's focus] Scoped work for WI-204" in second


def test_worker_brief_names_the_one_turn_close_bar_scratch_and_amendments(tmp_path):
    # WI-580 Done-when 1 / 4 / 5 (WI-559 item 1, WI-560 item 2, WI-562 item 2):
    # three clauses the shipped brief must carry, asserted on the RENDERED
    # prompt so an edit that drops one from the template fails here.
    #   1. the close bar fits in one turn — refresh runs the stage-declared bar
    #      in the merge slot and the full suite belongs to phase close
    #      (WI-540 lost three sessions ending their turn to await an ~11-minute
    #      suite against a 10-minute cap, and a finished row closed `partial`);
    #   2. an AMENDMENT of an approved cell stales the approval brief exactly
    #      as a mint does (WI-538 / LLR-206, an `approval-fresh` red);
    #   3. scratch has a home, so the lane unload stops refusing it by name.
    row = {"WI-ID": "WI-005", "Title": "t", "SR-Refs": "", "Predecessors": ""}
    prompt = agent_loop.worker_prompt(tmp_path, {"WI-005": row}, "WI-005", "w", "0" * 7)
    assert "THE CLOSE BAR IS THE COMMIT BAR, and it must fit in ONE turn" in prompt
    assert "You do NOT owe the full unfiltered suite at close" in prompt
    assert "NEVER end a turn waiting on one" in prompt
    assert "AMENDED THE TEXT OF AN ALREADY-APPROVED CELL" in prompt
    assert "Scratch belongs OUTSIDE the worktree" in prompt


def test_worker_brief_resolves_close_commands_at_the_runtime_scripts_path(tmp_path):
    # REVIEW-A rework: the close ritual used the scaffold's literal `scripts/`
    # command in this meta-repo, which has only `project-trajectory/scripts/`.
    # The worker composition boundary owns the runtime path, as reviewer_prompt
    # already does for its slots; no caller can now emit an unusable command.
    row = {"WI-ID": "WI-005", "Title": "t", "SR-Refs": "", "Predecessors": ""}
    prompt = agent_loop.worker_prompt(tmp_path, {"WI-005": row}, "WI-005", "w", "0" * 7)
    assert "python project-trajectory/scripts/trace.py --approve modified" in prompt
    assert "python project-trajectory/scripts/spec_move.py" in prompt

    scaffold = tmp_path / "scaffold"
    (scaffold / "scripts").mkdir(parents=True)
    (scaffold / "scripts" / "check.py").write_text("", encoding="utf-8")
    prompt = agent_loop.worker_prompt(scaffold, {"WI-005": row}, "WI-005", "w", "0" * 7)
    assert "python scripts/trace.py --approve modified" in prompt
    assert "python scripts/spec_move.py" in prompt


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
    # (The resume-from-status DEFAULT_PROMPT is retired outright, WI-210 —
    # the assignment prompt is the only build prompt by construction.)


def test_worker_multi_wi_assignment_builds_in_order(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path, wis=("WI-201", "WI-204"))
    proc = _worker(repo, fake, ctl, "--wi", "WI-201;WI-204", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    prompt = (ctl / "prompts.txt").read_text(encoding="utf-8")
    # Ordered: WI-201's session first, then WI-204's — and WI-204's prompt
    # carries the train diff of the accepted-but-unintegrated WI-201 commit.
    assert prompt.index("- WI: WI-201") < prompt.index("- WI: WI-204")
    assert "Current branch diff" in prompt
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
    spec = next((repo / "docs" / "work" / "queued").glob("WI-201-*.md")).read_text(
        encoding="utf-8"
    )
    assert "blockref" not in spec.lower()  # still queued, no durable block


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


def test_wi_without_train_defaults_tag_to_the_branch(tmp_path):
    # Phase 5 re-grounding: --wi alone is a full assignment; the session tag
    # defaults to the current branch name (flattened), so the evidence lands
    # tag-scoped without any dispatcher-era --train.
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(repo, fake, ctl, "--wi", "WI-201")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "branch=llm-train-t1" in proc.stdout  # derived from llm/train/t1


def test_train_without_wi_is_preflight_failure(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(repo, fake, ctl, "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "--train without --wi" in (proc.stdout + proc.stderr)


def test_track_flag_is_gone(tmp_path):
    # WI-210: --track is retired outright — argparse refuses it as an unknown
    # flag (exit 2), so no code path can reach the old lane plumbing.
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(
        repo, fake, ctl, "--wi", "WI-201", "--train", "t1", "--track", "lane"
    )
    assert proc.returncode == 2
    assert "--track" in (proc.stdout + proc.stderr)


def test_worker_on_detached_head_fails_closed(tmp_path):
    # A claim is a branch (§2.3), so a detached HEAD is an unverifiable
    # checkout — the assignment refuses up front. (The dispatcher-era
    # llm/train/<train> branch-equality guard retired with the naming at
    # Phase 5; the fail-closed core — a worker runs on a branch — survives.)
    repo, base, ctl, fake = _setup(tmp_path, train="t1")
    _git(repo, "checkout", "-q", "--detach", "HEAD")
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "could not be determined" in (proc.stdout + proc.stderr)


def test_worker_unknown_or_done_wi_fails_closed(tmp_path):
    repo, base, ctl, fake = _setup(tmp_path)
    proc = _worker(repo, fake, ctl, "--wi", "WI-999", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "not in the docs/work/ registry" in (proc.stdout + proc.stderr)
    proc = _worker(repo, fake, ctl, "--wi", "WI-200", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    out = proc.stdout + proc.stderr
    assert "already done" in out and "terminal status" in out


def test_worker_cancelled_wi_fails_closed(tmp_path):
    # WI-267 (respelled by WI-384): a WI CANCELLED after it was assigned to this
    # worker is terminal — the preflight guard must fail closed just like a done
    # WI, so the worker never builds a WON'T-BUILD row (the narrow
    # cancel-mid-assignment race the done-only check missed). Cancel the assigned
    # WI-201 on its train branch (reason in Deliverable, SpecRef cleared — the
    # terminal shape), then assign.
    repo, base, ctl, fake = _setup(tmp_path)
    _write_registry(
        repo,
        [
            [
                "WI-200",
                "Predecessor work",
                "ws",
                "SR-001",
                "",
                "done",
                "the shipped predecessor deliverable",
                "docs/specs/thing.md",
                "",
            ],
            [
                "WI-201",
                "Scoped work for WI-201",
                "ws",
                "SR-060",
                "WI-200",
                "cancelled",
                "superseded — will not be built",
                "",
                "medium",
            ],
        ],
    )
    _git(repo, "commit", "-aqm", "cancel WI-201")
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    out = proc.stdout + proc.stderr
    assert "already cancelled" in out and "terminal status" in out


# --- WI-080 Slice D/E: worker end-state + the assignment seam ------------------
# WI-277 moved this block here VERBATIM from tests/test_agent_loop.py, where it
# had grown up beside the coordinator's own tests: worker_endstate and the
# git-backed build_worker_assignment cases are the WORKER leg, which is this
# module's subject. `_git` is already defined above (same shape).
#
# ONLY git-dependent tests were moved here. This module carries a module-wide
# `pytestmark = env_gate_skipif("git")` (:45), which would ADD a gate to any
# pure test placed under it — REVIEW-A round 1 caught exactly that: three pure
# seams landed here on the first cut and went 3 passed -> 3 SKIPPED with git off
# PATH, silently losing coverage on an ungated machine. They now live in
# tests/test_agent_loop_policy.py. Do not park an ungated test in this module.


def _train_repo(tmp_path, train="t1", assigned=("WI-201",)):
    """A throwaway repo: a seed commit (the integration base), then branch
    llm/train/<train>. Returns (repo, base, worker-dict) — the worker carries
    exactly the keys worker_endstate reads."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "-b", "llm/train/" + train)
    worker = {"train": train, "assigned": list(assigned), "base": base, "rework": ""}
    return repo, base, worker


def _build_commit(repo, wi, train, base):
    (repo / ("work-" + wi + ".txt")).write_text("work " + wi, encoding="utf-8")
    _git(repo, "add", "-A")
    msg = "build {}\n\nWI: {}\nTrain: {}\nBase: {}\n".format(wi, wi, train, base)
    _git(repo, "commit", "-q", "-m", msg)


@env_gate_skipif("git")
def test_worker_endstate_done_names_branch(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    end = al.worker_endstate(str(repo), worker, False, False, 1)
    assert end is not None
    code, label, detail = end
    assert code == al.EXIT_DONE
    assert label == "DONE"
    assert "branch t1" in detail


@env_gate_skipif("git")
def test_worker_endstate_review_open_defers(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    # Built + clean, but the caller reports the train's review cycle still open.
    assert al.worker_endstate(str(repo), worker, True, False, 1) is None


@env_gate_skipif("git")
def test_worker_endstate_rework_pending_defers(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    worker["rework"] = "a CHANGES-REQUESTED verdict is pending"
    assert al.worker_endstate(str(repo), worker, False, False, 1) is None


@env_gate_skipif("git")
def test_worker_endstate_blocked_trailer_exits_blocked(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    (repo / "work-WI-201.txt").write_text("stuck", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(
        repo,
        "commit",
        "-q",
        "-m",
        "blocked WI-201\n\nBlocked-WI: WI-201\nBlockRef: OI-99\n",
    )
    end = al.worker_endstate(str(repo), worker, False, False, 1)
    assert end is not None
    code, label, detail = end
    assert code == al.EXIT_BLOCKED
    assert label == "BLOCKED"
    assert "OI-99" in detail


@env_gate_skipif("git")
def test_worker_endstate_dirty_tree_defers(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    # Committed evidence is complete, but an uncommitted path means not-done.
    (repo / "scratch.txt").write_text("uncommitted", encoding="utf-8")
    assert al.worker_endstate(str(repo), worker, False, False, 1) is None


def test_worker_endstate_owner_scratchpad_stays_done(tmp_path):
    # WI-203: an owner-only-dirty tree (OWNER_SCRATCHPAD.md) is not interrupted
    # work — done detection must not read it as not-done (contrast the scratch.txt
    # case above, which still defers).
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    (repo / "OWNER_SCRATCHPAD.md").write_text("owner notes", encoding="utf-8")
    end = al.worker_endstate(str(repo), worker, False, False, 1)
    assert end is not None and end[0] == al.EXIT_DONE


# --- WI-080 Slice E: main() composed from module-level seams ------------------
# main() is now orchestration-only (parse -> setup -> mode select -> loop); the
# setup phases (parse_args / map_preflight / build_worker_assignment /
# track_preamble_text / print_run_banner / run_interactive) and the loop body
# (route_session / session_bookkeeping / run_iteration over a LoopContext) are
# module functions. The e2e net pins behavior; these lean units pin the three
# newly unit-addressable seams.
#
# Only the git-dependent half of the Slice lives here — the pure units
# (worker_exit_banner, the no-assignment build_worker_assignment case,
# parse_args defaults) are in tests/test_agent_loop_policy.py, which carries no
# module-wide gate. See the WI-277 note on the block header above.


@env_gate_skipif("git")
def test_build_worker_assignment_bad_base_fails_closed(tmp_path, capsys):
    al = load_script("agent_loop")
    repo, _base, _worker = _train_repo(tmp_path)
    args = argparse.Namespace(wi="WI-201", train="t1", base="deadbeef", rework=None)
    worker, err = al.build_worker_assignment(args, repo)
    assert worker is None
    assert err == al.EXIT_PREFLIGHT
    assert "does not resolve to a commit" in capsys.readouterr().err


@env_gate_skipif("git")
def test_build_worker_assignment_good_base_parses_wi_list(tmp_path):
    al = load_script("agent_loop")
    repo, base, _worker = _train_repo(tmp_path)
    args = argparse.Namespace(wi="WI-201;WI-204", train="t1", base=base, rework=None)
    worker, err = al.build_worker_assignment(args, repo)
    assert err is None
    assert worker["train"] == "t1"
    assert worker["assigned"] == ["WI-201", "WI-204"]
    assert worker["base"] == base
    assert worker["rework"] == ""


# --- the batch walk: a trailer alone is not a closed row ------------------------
# Measured 2026-09-03 on the four-row spine batch `wi-589-…`: session 001
# committed WI-589's build WITH its `WI:` trailer and ran out before the close
# ritual, so `current_assignment_wi` — which asked the trailer alone — stepped
# past the row for the rest of the lane and nothing ever moved its spec out of
# `active/<branch>/`. `integrate.finished_branches` asks the tree, so it never
# counted the branch finished either, and the lane stranded after its review
# round. The walk now asks BOTH halves, which is the same question the
# integrator asks.


def _batch_repo(tmp_path, branch="wi-batch", wis=("WI-201", "WI-204")):
    """A lane branch carrying a spec per assigned row in `active/<branch>/`."""
    repo, base, worker = _train_repo(tmp_path, assigned=wis)
    _git(repo, "checkout", "-q", "-b", branch)
    active = repo / "docs" / "work" / "active" / branch
    active.mkdir(parents=True)
    for wid in wis:
        (active / "{}-row.md".format(wid)).write_text(
            '+++\nid = "{}"\n+++\n\n## Context\n\nwork.\n'.format(wid),
            encoding="utf-8",
            newline="\n",
        )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "claim " + ";".join(wis))
    worker["base"] = base
    return repo, worker, active


@env_gate_skipif("git")
def test_a_built_but_unclosed_row_is_still_the_walks_next_row(tmp_path):
    al = load_script("agent_loop")
    repo, worker, _active = _batch_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", worker["base"])
    # The trailer is committed for WI-201, but its spec never left active/ — the
    # walk must come back to it rather than move on to the untouched WI-204.
    assert al.current_assignment_wi(str(repo), worker) == "WI-201"
    # MUTATION NOTE: without the tree half this reads "WI-204" (the defect), so
    # the assertion is not vacuous — and the trailer half still matters, which
    # the closed case below drives.


@env_gate_skipif("git")
def test_a_row_with_both_halves_done_lets_the_walk_move_on(tmp_path):
    al = load_script("agent_loop")
    repo, worker, active = _batch_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", worker["base"])
    complete = repo / "docs" / "work" / "complete"
    complete.mkdir(parents=True, exist_ok=True)
    (active / "WI-201-row.md").rename(complete / "WI-201-row.md")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "close WI-201")
    assert al.current_assignment_wi(str(repo), worker) == "WI-204"


@env_gate_skipif("git")
def test_a_one_row_lane_answers_its_row_either_way(tmp_path):
    # The behaviour-preserving half: with a single assignment both arms answer
    # the same row, so only a batch can observe the new read.
    al = load_script("agent_loop")
    repo, worker, _active = _batch_repo(tmp_path, wis=("WI-201",))
    assert al.current_assignment_wi(str(repo), worker) == "WI-201"
    _build_commit(repo, "WI-201", "t1", worker["base"])
    assert al.current_assignment_wi(str(repo), worker) == "WI-201"


@env_gate_skipif("git")
def test_the_brief_never_calls_an_unclosed_row_built(tmp_path):
    # WI-580 review A (MAJOR): the brief block derived doneness from the
    # trailer ALONE while the walk asked both halves, so a batch that committed
    # a trailer for a row and never ran its close ritual told the next session
    # that row was `built` — the same silent-completion miss the walk's two-part
    # test exists to prevent. Both readers now go through `lane_completion`.
    al = load_script("agent_loop")
    repo, worker, active = _batch_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", worker["base"])
    _build_commit(repo, "WI-204", "t1", worker["base"])
    rows = {w: {"WI-ID": w, "Title": "row " + w} for w in ("WI-201", "WI-204")}
    focus = al.current_assignment_wi(str(repo), worker)
    assert focus == "WI-201"  # neither spec left active/, so the walk holds
    block = al.assignment_block(
        str(repo), rows, focus, worker["base"], worker["assigned"]
    )
    # MUTATION NOTE: on the trailer-alone predicate this line read `[built]`.
    assert "  - WI-204 [started, not closed] row WI-204" in block
    assert "[built]" not in block
    # And the closed half still reads `built`, so the new state is not a
    # blanket downgrade of every trailer-bearing row.
    complete = repo / "docs" / "work" / "complete"
    complete.mkdir(parents=True, exist_ok=True)
    (active / "WI-204-row.md").rename(complete / "WI-204-row.md")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "close WI-204")
    block = al.assignment_block(
        str(repo), rows, focus, worker["base"], worker["assigned"]
    )
    assert "  - WI-204 [built] row WI-204" in block


# --- the resumed BATCH preflight: a row this branch closed is not stale ---------
# Measured 2026-09-03 on the four-row spine batch `wi-589-…`. The lane closed
# three of its rows, so the registry read `done` for them — and the resumed
# worker's preflight refused all three with "a terminal status (done/cancelled);
# a stale assignment, so the dispatcher must re-derive the frontier", over rows
# that were terminal precisely BECAUSE this lane made them so. The status alone
# cannot tell a stale assignment from a partly-finished batch; this branch's own
# `WI:` trailer can.


def _lane_worktree_repo(tmp_path, branch="wi-batch"):
    """A primary checkout holding the TRUNK plus a linked lane worktree on
    `branch` — the real topology, and the only one where `merge-base(trunk,
    HEAD)` is anything but HEAD."""
    repo, _base = _make_train_repo(tmp_path, wis=("WI-201", "WI-204"))
    lane_wt = tmp_path / "lane"
    _git(repo, "worktree", "add", "-q", "-b", branch, str(lane_wt))
    return repo, lane_wt


@env_gate_skipif("git")
def test_a_row_this_branch_closed_is_not_a_stale_assignment(tmp_path):
    ac = load_script("agent_common")
    _repo, lane_wt = _lane_worktree_repo(tmp_path)
    (lane_wt / "work-WI-201.txt").write_text("built\n", encoding="utf-8")
    _git(lane_wt, "add", "-A")
    _git(lane_wt, "commit", "-q", "-m", "build WI-201\n\nWI: WI-201")
    done = {"Status": "done"}
    # THE LANE'S OWN CLOSE: terminal, with this branch's trailer -> not stale.
    assert ac.stale_terminal_assignment(lane_wt, "WI-201", done) is False
    # TERMINAL ON THE TRUNK: no trailer in this branch's own range -> stale, and
    # the refusal stands exactly as it did (WI-267's cancel-mid-flight race).
    assert ac.stale_terminal_assignment(lane_wt, "WI-204", done) is True
    assert ac.stale_terminal_assignment(lane_wt, "WI-204", {"Status": "cancelled"})
    # A non-terminal row was never this guard's business.
    assert (
        ac.stale_terminal_assignment(lane_wt, "WI-201", {"Status": "queued"}) is False
    )


@env_gate_skipif("git")
def test_a_single_checkout_worker_keeps_the_terminal_refusal(tmp_path):
    # The behaviour-preserving half. In an attended single checkout the trunk
    # IS the branch, so `default_base` merge-bases to HEAD, the evidence range
    # is empty, and every terminal row still refuses — which is what the
    # existing done/cancelled preflight tests above assert end to end.
    ac = load_script("agent_common")
    repo, _base = _make_train_repo(tmp_path)
    (repo / "work.txt").write_text("built\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "build WI-201\n\nWI: WI-201")
    assert ac.stale_terminal_assignment(repo, "WI-201", {"Status": "done"}) is True
