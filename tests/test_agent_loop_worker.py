"""Explicit worker assignment mode — scripts/agent_loop.py --wi/--train
(WI-181, SR-026/LLR-061/TC-061; docs/specs/parallel-wi-dispatch.md §6).

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
    prefixed session logs (collision-safe evidence, LLR-061);
  - a Blocked-WI trailer exits 3 (the durable disposition is the integrator's,
    Slice F) — never a silent DONE;
  - preflight fails closed: half a pair, wrong branch, an unknown or
    already-done WI;
  - the retired --track flag is refused as an unknown flag (TC-061), and
    managed review evidence in worker mode lands at
    reviews/<train>/NNN-<PHASE>-<sha7>.md naming the reviewed HEAD.

Implements: TC-061
"""

import argparse
import csv
import functools
import subprocess
import sys

import pytest
from conftest import (
    declare_review_bar,
    declare_trunk,
    hooks_on,
    env_gate_skipif,
    claim_on_trunk,
    lane_checkout,
    relocate_as_lane,
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
    hooks_on(repo)  # every route refuses a checkout without hooks
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    declare_trunk(repo)
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


# --- one work item per assignment ---------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "",
        "WI-201;WI-204",
        "WI-201,WI-204",
        "WI-201 WI-204",
        "WI-201;WI-201",
        # Adequacy witness: a parser that took any token, or read a
        # separator-only value as no assignment, would raise no failure for
        # these three.
        ";",
        "WI-",
        "wi-201",
    ],
)
def test_the_worker_refuses_any_assignment_but_one_id(tmp_path, value):
    """Implements: TC-061"""
    # The worker's assignment is exactly one well-formed work-item id. Any
    # other value (empty, separator-only, a list in any separator, a repeated
    # id, a malformed token) is one preflight failure naming the value, before
    # a provider launches. Both rows exist in the registry, so a list value
    # cannot be refused for naming an unknown row.
    repo, _base = _make_train_repo(tmp_path, wis=("WI-201", "WI-204"))
    template = '"{}" -p {{prompt}}'.format(sys.executable)
    args = argparse.Namespace(wi=value, train=None, interactive=False)
    failures = agent_loop.agent_common.preflight(repo, template, args)
    assert len(failures) == 1, failures
    assert repr(value) in failures[0], failures


def test_the_worker_accepts_one_well_formed_id(tmp_path):
    # The one allowed form passes the assignment preflight. Adequacy witness:
    # a refusal that read every assignment as malformed, or that refused a
    # row for sharing the registry with another, would add a failure here.
    repo, _base = _make_train_repo(tmp_path, wis=("WI-201", "WI-204"))
    template = '"{}" -p {{prompt}}'.format(sys.executable)
    args = argparse.Namespace(wi="WI-201", train=None, interactive=False)
    assert agent_loop.agent_common.preflight(repo, template, args) == []


def test_a_list_assignment_exits_preflight_before_a_provider_launches(tmp_path):
    """Implements: TC-061"""
    # The CLI's assignment argument takes one id; a list exits on the preflight
    # code, naming the value, and the fake provider records no launch at all.
    repo, base, ctl, fake = _setup(tmp_path, wis=("WI-201", "WI-204"))
    relocate_as_lane(repo)  # a worker records from its claimed lane (WI-960)
    proc = _worker(repo, fake, ctl, "--wi", "WI-201;WI-204", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, proc.stdout + proc.stderr
    assert "WI-201;WI-204" in proc.stdout + proc.stderr
    assert not (ctl / "prompts.txt").exists()


def test_the_wi_help_names_one_work_item(monkeypatch, capsys):
    # The assignment argument's help says it takes one work item and offers
    # no list example.
    monkeypatch.setattr(sys, "argv", ["agent_loop.py", "--help"])
    with pytest.raises(SystemExit):
        agent_loop.parse_args()
    lines = capsys.readouterr().out.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("  --wi "))
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("  -")),
        len(lines),
    )
    wi_help = " ".join(ln.strip() for ln in lines[start:end])
    assert "WI-201;WI-204" not in wi_help, wi_help
    assert " one " in " {} ".format(wi_help), wi_help


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


def test_the_worker_template_has_no_assignment_block_slot():
    # The worker brief names the one assigned row; the multi-row assignment
    # block and its slot are gone from the shipped template.
    text = (SCRIPTS.parent / "prompts" / "worker.template.md").read_text(
        encoding="utf-8"
    )
    assert "{assignment_block}" not in text


_ONE_ROW_GOLDEN = (
    SCRIPTS.parent.parent / "tests" / "golden" / "worker-prompt-one-row.txt"
)


def test_the_one_row_prompt_renders_as_today(tmp_path):
    """Implements: TC-061"""
    # The one-row worker prompt renders byte for byte as the golden file
    # tests/golden/worker-prompt-one-row.txt, with the integration base written
    # there as <BASE>.
    # Adequacy witness: a template edit that dropped, reordered or reworded an
    # Assignment line, a rule or the trailer protocol would differ from the
    # golden and fail here.
    _git(tmp_path, "init", "-q")
    hooks_on(tmp_path)
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "T")
    _git(tmp_path, "commit", "-q", "--allow-empty", "-m", "seed")
    base = _git(tmp_path, "rev-parse", "HEAD")
    row = {
        "WI-ID": "WI-005",
        "Title": "the assignment",
        "SR-Refs": "SR-001",
        "Predecessors": "",
        "SpecRef": "seed.txt",
    }
    prompt = agent_loop.worker_prompt(
        tmp_path, {"WI-005": row}, "WI-005", "wi-005", base
    )
    expected = _ONE_ROW_GOLDEN.read_text(encoding="utf-8").replace("<BASE>", base)
    assert prompt == expected


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
    relocate_as_lane(repo)  # a worker records from its claimed lane (WI-960)
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "worker t1 [WI-201]: DONE" in proc.stdout

    # The result is committed evidence: the WI trailer on the train branch.
    trailers = _git(repo, "log", "--format=%(trailers:key=WI,valueonly)", "HEAD")
    assert "WI-201" in trailers.split()
    # Collision-safe train-prefixed session log; NO lane files, NO generated
    # index, NO run-state, NO tracks lane (LLR-061).
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
    # Each worker records from its claimed lane (WI-960).
    claim_on_trunk(wt1, "WI-8")
    claim_on_trunk(wt2, "WI-9")
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
    # HEAD (LLR-061 — a verdict belongs to the exact commit, never a branch
    # tip), and the scoreboard is train-scoped too.
    repo, base, ctl, fake = _setup(tmp_path)
    # The worker runs in its lane worktree, `main` staying in the primary.
    repo = lane_checkout(repo, "llm/train/t1")
    declare_review_bar(repo, ctl)
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
    # The wiring is the lane's starting point, not its work: the declared
    # trunk moves up to it, so the lane's integration base sits after it. The
    # trunk is checked out in the primary, so its ref is moved directly.
    _git(repo, "update-ref", "refs/heads/main", "HEAD")
    proc = _worker(repo, fake, ctl, "--wi", "WI-201", "--train", "t1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    verdicts = list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*.md"))
    assert len(verdicts) == 1, "expected one train-scoped verdict"
    sha7 = verdicts[0].stem.rsplit("-", 1)[1]
    # The named sha is the exact reviewed commit: the review bar's attestation
    # of the implementer's commit, sitting directly on it with its tree.
    subjects = _git(repo, "log", "--format=%h %s", "HEAD")
    build_line = [ln for ln in subjects.splitlines() if "build WI-201" in ln][0]
    reviewed = _git(repo, "rev-parse", sha7)
    assert agent_loop.kverdict.bar_attestation(str(repo), reviewed) is not None
    assert _git(repo, "rev-parse", reviewed + "^").startswith(build_line.split()[0])
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
    hooks_on(repo)  # every route refuses a checkout without hooks
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "symbolic-ref", "HEAD", "refs/heads/main")
    declare_trunk(repo)
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
def test_build_worker_assignment_refuses_an_unreadable_default_base(
    tmp_path, capsys, monkeypatch
):
    al = load_script("agent_loop")
    repo, _base, _worker = _train_repo(tmp_path)
    monkeypatch.setattr(al.agent_common, "default_base", lambda _root: None)
    args = argparse.Namespace(wi="WI-201", train="t1", base=None, rework=None)
    worker, err = al.build_worker_assignment(args, repo)
    assert worker is None
    assert err == al.EXIT_PREFLIGHT
    assert "no resolvable --base" in capsys.readouterr().err


@env_gate_skipif("git")
def test_build_worker_assignment_good_base_takes_one_id(tmp_path):
    al = load_script("agent_loop")
    repo, base, _worker = _train_repo(tmp_path)
    args = argparse.Namespace(wi="WI-201", train="t1", base=base, rework=None)
    worker, err = al.build_worker_assignment(args, repo)
    assert err is None
    assert worker["train"] == "t1"
    assert worker["assigned"] == ("WI-201",)
    assert worker["base"] == base
    assert worker["rework"] == ""
    # A list value is refused on the preflight code, never parsed into rows.
    args = argparse.Namespace(wi="WI-201;WI-204", train="t1", base=base, rework=None)
    worker, err = al.build_worker_assignment(args, repo)
    assert worker is None
    assert err == al.EXIT_PREFLIGHT


# --- the walk: a lane's one row, built or not ----------------------------------
# A lane builds one work item, so the walk answers that row. Whether the row is
# done with asks both halves (its committed `WI:` trailer AND its spec gone from
# `active/<branch>/`), the same question the integrator asks, read through
# `lane_completion`.


def _lane_repo(tmp_path, branch="wi-201", wi="WI-201"):
    """A lane branch carrying its one assigned row's spec in `active/<branch>/`."""
    repo, base, worker = _train_repo(tmp_path, assigned=(wi,))
    _git(repo, "checkout", "-q", "-b", branch)
    active = repo / "docs" / "work" / "active" / branch
    active.mkdir(parents=True)
    (active / "{}-row.md".format(wi)).write_text(
        '+++\nid = "{}"\n+++\n\n## Context\n\nwork.\n'.format(wi),
        encoding="utf-8",
        newline="\n",
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "claim " + wi)
    worker["base"] = base
    return repo, worker, active


@env_gate_skipif("git")
def test_a_one_row_lane_answers_its_row_either_way(tmp_path):
    # The walk answers the lane's one row before its build commit and after it.
    al = load_script("agent_loop")
    repo, worker, _active = _lane_repo(tmp_path)
    assert al.current_assignment_wi(str(repo), worker) == "WI-201"
    _build_commit(repo, "WI-201", "t1", worker["base"])
    assert al.current_assignment_wi(str(repo), worker) == "WI-201"


@env_gate_skipif("git")
def test_the_false_partial_class_turns_only_on_the_close_ritual(tmp_path):
    """WI-559 Done-when 3, first half — the built-and-verified lane read as a
    stall (WI-540: three sessions each verified their rework, each ended the
    turn waiting on a ~11-minute suite, and the FINISHED row closed `partial`).

    Both readers of that state are driven on ONE scaffold, because the class is
    the gap between them. With the trailer committed and the spec still in
    `active/<branch>/`, `lane_completion` calls the row built but not done and
    `integrate.finished_branches` does not name the branch — so `dispatch`
    takes the `_lane_close` arm (the stall candidate) over the refresh arm.
    Moving the spec to a terminal directory, and NOTHING else, flips both
    reads. The close ritual alone separates a merge from a `partial`, which is
    why the shipped brief's close bar has to fit inside one turn.

    The `== []` is not an empty scan: the identical call on the identical
    scaffold answers `["wi-201"]` four lines later, so the reader is live and
    the first read is a real negative.
    """
    al = load_script("agent_loop")
    integrate = load_script("integrate")
    repo, worker, active = _lane_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", worker["base"])

    built, done = al.lane_completion(str(repo), worker["base"])
    assert built == {"WI-201"}  # built AND verified …
    assert done == set()  # … and not closed
    assert integrate.finished_branches(repo) == []  # -> the stall candidate

    complete = repo / "docs" / "work" / "complete"
    complete.mkdir(parents=True, exist_ok=True)
    (active / "WI-201-row.md").rename(complete / "WI-201-row.md")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "close the lane")

    built, done = al.lane_completion(str(repo), worker["base"])
    assert built == done == {"WI-201"}
    assert integrate.finished_branches(repo) == ["wi-201"]


# --- the resumed preflight: a row this branch closed is not stale --------------
# A lane that closed its one row and still owes a review round resumes with the
# registry reading `done` for that row. The preflight's stale-assignment refusal
# ("a terminal status (done/cancelled); a stale assignment, so the dispatcher
# must re-derive the frontier") must not fire on a row that is terminal
# precisely BECAUSE this lane made it so. The status alone cannot tell that
# from a row closed elsewhere; this branch's own `WI:` trailer can.


def _lane_worktree_repo(tmp_path, branch="wi-201"):
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
    # The single-checkout half. With the trunk declared, a worker in a single
    # checkout on its lane branch reads the same base a linked lane does, the
    # merge base with the trunk: the row this branch closed is not stale, and
    # a row terminal for any other reason still refuses.
    ac = load_script("agent_common")
    repo, base = _make_train_repo(tmp_path)
    (repo / "work.txt").write_text("built\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "build WI-201\n\nWI: WI-201")
    assert ac.default_base(repo) == base
    assert ac.stale_terminal_assignment(repo, "WI-201", {"Status": "done"}) is False
    assert ac.stale_terminal_assignment(repo, "WI-200", {"Status": "done"}) is True
