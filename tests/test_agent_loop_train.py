"""Change-train continuation — one review cycle per traincar, early-end
release, fork/join (WI-183, SR-062/LLR-063/TC-063;
docs/specs/parallel-wi-dispatch.md §7).

Worker-level and dispatcher-level, against the same fake agents the C/D suites
use. The load-bearing guarantees:

  - a multi-WI traincar is ONE review scope: the round dispatches only after
    the LAST constituent commits, over the combined base..HEAD train diff —
    exactly one verdict per required reviewer, named on the train head;
  - the §7 continuation re-check ends a train EARLY (exit 10) when the
    classifier no longer permits the next constituent in a multi-WI grouping;
  - a blocked constituent ends the train with built evidence kept and every
    UNSTARTED constituent's reservation transactionally released (the traincar
    DAG recompute) — and no WI row is marked done/blocked by anyone but the
    integrator;
  - the unary-chain cap (default 4) bounds packing;
  - a FORK integrates the parent first, then both children take separate
    lanes; a JOIN starts only from the combined integration HEAD (simulated
    integration until Slice F lands the integrator).
"""

import csv
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, run_py

agent_loop = load_script("agent_loop")
schedule = load_script("schedule")

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
    "Campaign",
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
        "SR-062",
        preds,
        status,
        "shipped" if status == "done" else "",
        "docs/specs/thing.md",
        "camp",
        "medium",
        safety,
    ]


def _write_registry(repo, rows):
    reg = repo / "docs" / "requirements"
    reg.mkdir(parents=True, exist_ok=True)
    with open(str(reg / "work-items.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)


def _make_repo(tmp_path, rows):
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_registry(repo, rows)
    (repo / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    (repo / "docs" / "gate-policy").write_text("autonomous\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


# Builder + reviewer fake: builds commit the trailer protocol; a reviewer
# prompt (names a verdict path) writes an APPROVE verdict and commits it.
# `block:<WI-ID>` in ctl/mode makes that WI commit a Blocked-WI trailer.
FAKE = r"""
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
mode = (ctl / "mode").read_text().strip() if (ctl / "mode").exists() else ""
pathlib.Path("work-" + wi + ".txt").write_text("work", encoding="utf-8")
subprocess.run(["git", "add", "-A"], check=True)
if mode == "block:" + wi:
    msg = "blocked " + wi + "\n\nBlocked-WI: " + wi + "\nBlockRef: OI-77\n"
else:
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


def _worker(repo, template, *extra):
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
            "10",
            *extra,
        ],
        cwd=repo,
    )


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


def _reservations(repo):
    out = _git(repo, "for-each-ref", "--format=%(refname)", "refs/llm/reservations")
    return {ln.rsplit("/", 1)[1] for ln in out.splitlines() if ln.strip()}


def _wire_managed(repo, template, review_policy="1"):
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
    (repo / "docs" / "review-policy").write_text(review_policy + "\n", "utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "wire managed routing")


# --- one review cycle per traincar (worker level) -------------------------------


def test_multi_wi_traincar_takes_one_review_cycle_at_the_end(tmp_path):
    repo, ctl, template = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-202", preds="WI-201")]
    )
    _wire_managed(repo, template, review_policy="1")
    base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")
    proc = _worker(
        repo, template, "--wi", "WI-201;WI-202", "--train", "t1", "--base", base
    )
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    # Exactly ONE review round, dispatched only after BOTH constituents built.
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert prompts.count("Write your verdict to") == 1
    assert prompts.index("- WI: WI-202") < prompts.index("Write your verdict to")
    verdicts = list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*.md"))
    assert len(verdicts) == 1
    # The verdict names the TRAIN HEAD — the last build commit (WI-202's).
    sha7 = verdicts[0].stem.rsplit("-", 1)[1]
    subjects = _git(repo, "log", "--format=%h %s", "HEAD")
    line = [ln for ln in subjects.splitlines() if "build WI-202" in ln][0]
    assert line.startswith(sha7[:7])
    assert "over the whole train diff" in proc.stdout
    # No constituent became done: the registry rows are untouched on-branch.
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert reg.count(",done,") == 0


def test_continuation_recheck_ends_train_early(tmp_path):
    # The dispatcher would never pack this (a spine successor); a worker handed
    # such an assignment must refuse the successor AFTER building the ordinary
    # head — the §7 "classifier still permits" runtime condition.
    repo, ctl, template = _setup(
        tmp_path, [_wi_row("WI-201"), _wi_row("WI-210", safety="spine")]
    )
    base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")
    proc = _worker(
        repo, template, "--wi", "WI-201;WI-210", "--train", "t1", "--base", base
    )
    assert proc.returncode == agent_loop.EXIT_TRAIN_END, proc.stdout + proc.stderr
    assert "continuation refused at WI-210" in proc.stdout
    trailers = _git(repo, "log", "--format=%(trailers:key=WI,valueonly)", "HEAD")
    assert "WI-201" in trailers.split() and "WI-210" not in trailers


# --- early end releases unstarted reservations (dispatcher level) ---------------


def test_blocked_constituent_releases_unstarted_and_keeps_built(tmp_path):
    # One packed 3-chain; the middle WI blocks. Built WI-201 and blocked
    # WI-202 keep their reservations (integrator evidence); unstarted WI-203
    # is transactionally released and the WI registry rows stay untouched.
    repo, ctl, template = _setup(
        tmp_path,
        [
            _wi_row("WI-201"),
            _wi_row("WI-202", preds="WI-201"),
            _wi_row("WI-203", preds="WI-202"),
        ],
    )
    (ctl / "mode").write_text("block:WI-202", encoding="utf-8")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    assert _reservations(repo) == {"WI-201", "WI-202"}
    events = (repo / "out" / "dispatch" / "events.jsonl").read_text("utf-8")
    assert '"release-unstarted"' in events and "WI-203" in events
    assert '"worker-blocked"' in events
    # Released WI-203 stays queued and untouched — it re-enters the frontier
    # only when its predecessor's durable disposition advances (Slice F).
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert "WI-203,Work WI-203,ws,SR-062,WI-202,queued" in reg


# --- cap, fork, join -------------------------------------------------------------


def test_unary_chain_packs_to_the_cap(tmp_path):
    # Five-WI unary chain, cap 4 (spec §7 default): one 4-car + the tail.
    wis = [
        {
            "id": "WI-20%d" % i,
            "status": "queued",
            "preds": ["WI-20%d" % (i - 1)] if i > 1 else [],
            "soft": [],
            "srs": [],
            "priority": 0,
            "exclusive": [],
            "blockref": "",
            "est_tokens": 0,
            "safetyclass": "ordinary",
            "title": "w",
        }
        for i in range(1, 6)
    ]
    records = schedule.evaluate(wis)
    cars = agent_loop.pack_traincars(records, {w["id"]: w for w in wis})
    assert [c["wis"] for c in cars] == [
        ["WI-201", "WI-202", "WI-203", "WI-204"],
    ], "the waiting tail WI-205 is not ready until the car integrates"


def test_fork_parent_integrates_then_children_take_separate_lanes(tmp_path):
    # WI-201 forks into WI-202 + WI-203: the packer never chains past a fork,
    # so run 1 builds the parent alone; after (simulated, Slice F) integration
    # the children dispatch on TWO separate trains.
    repo, ctl, template = _setup(
        tmp_path,
        [
            _wi_row("WI-201"),
            _wi_row("WI-202", preds="WI-201"),
            _wi_row("WI-203", preds="WI-201"),
        ],
    )
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert _reservations(repo) == {"WI-201"}, "children wait for integration"

    # Simulate the integrator: durable done + reservation release (Slice F).
    rows = [
        _wi_row("WI-201", status="done"),
        _wi_row("WI-202", preds="WI-201"),
        _wi_row("WI-203", preds="WI-201"),
    ]
    _write_registry(repo, rows)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integrate WI-201 (simulated)")
    assert agent_loop.release_reservations(repo, ["WI-201"]) is None

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    starts = [
        ln
        for ln in (repo / "out" / "dispatch" / "events.jsonl")
        .read_text("utf-8")
        .splitlines()
        if '"worker-start"' in ln
    ]
    child_starts = [ln for ln in starts if "WI-202" in ln or "WI-203" in ln]
    assert len(child_starts) == 2
    assert not any("WI-202" in ln and "WI-203" in ln for ln in child_starts), (
        "children of a fork take SEPARATE lanes"
    )


def test_join_starts_from_the_combined_integration_head(tmp_path):
    # WI-203 joins WI-201 + WI-202 (independent parents): it never dispatches
    # while either parent is unintegrated, and its train base is the combined
    # integration HEAD once both are done.
    repo, ctl, template = _setup(
        tmp_path,
        [
            _wi_row("WI-201"),
            _wi_row("WI-202"),
            _wi_row("WI-203", preds="WI-201;WI-202"),
        ],
    )
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert _reservations(repo) == {"WI-201", "WI-202"}, "the join must wait"

    rows = [
        _wi_row("WI-201", status="done"),
        _wi_row("WI-202", status="done"),
        _wi_row("WI-203", preds="WI-201;WI-202"),
    ]
    _write_registry(repo, rows)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integrate WI-201+WI-202 (simulated)")
    assert agent_loop.release_reservations(repo, ["WI-201", "WI-202"]) is None
    combined_head = _git(repo, "rev-parse", "HEAD")

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    claims = agent_loop.list_reservations(repo)
    assert set(claims) == {"WI-203"}
    meta = agent_loop.reservation_meta(repo, claims["WI-203"])
    assert meta["base"] == combined_head, "the join builds from the combined HEAD"
