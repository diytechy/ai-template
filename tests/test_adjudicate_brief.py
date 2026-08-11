"""scripts/adjudicate_brief.py — the evidence an adjudication session's brief is
filled with, and the refusal that keeps a half-filled one from ever being sent
(WI-424; SN-026 x SN-032).

Four templates shipped, catalogued and consumed by NOTHING: every non-review
session, `ADJUDICATE` included, composed from the generic worker assignment, so
a row routed to a strong cross-family judge and then received an implementer's
instructions. These tests pin the seam that closed that, and — more
importantly — the two properties that make the seam safe to have at all:

  - **fill in full or refuse.** A judge's brief with a thin evidence section
    reads as an investigation that was run and found nothing, which is worse
    than the honest generic prompt. So every assembler is all-or-nothing, and
    the refusal names the missing derivation.
  - **the discriminator is DECLARED.** `Brief` is a typed cell, not a shape
    inferred from `SpecRef` — because that inference is provably ambiguous
    (an amended test-case row and a red-TC census row both cite the TC
    registry) and inferring from the Title is the `NEEDS-HUMAN` fold.

The two unrouted templates are pinned as unrouted ON PURPOSE: a test that
asserted they compose would be asserting that a slot got filled with something,
which is the failure mode.
"""

import re
import subprocess
import sys

import pytest
from conftest import env_gate_skipif, load_script, run_py, SCRIPTS

ab = load_script("adjudicate_brief")
agent_loop = load_script("agent_loop")
wi_convert = load_script("wi_convert")
intake = load_script("intake")

pytestmark = env_gate_skipif("git")


def _git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    # The scaffold's rule: out/ (locks, raw run logs) is runtime state, never
    # tracked — the session's clean-tree DONE check depends on it.
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    return repo


def _write_rows(repo, rows):
    work = repo / "docs" / "work"
    work.mkdir(parents=True, exist_ok=True)
    for cells in rows:
        row = {column: "" for column in wi_convert.COLUMNS}
        row.update(cells)
        row["Status"] = row.get("Status") or "queued"
        wi_convert.write_spec_file(work, row)


SPINE_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Priority,"
    "Verification,Status,Phase,Area\n"
    "SR-001,Adds,SN-001,The system shall add two numbers.,arithmetic is the "
    "demo,the sum is right,Must,Test,Verified,P1,core\n"
)
SPINE_LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component,Phase\n"
    "LLR-001,SR-001,add impl,src/demo.py,add,add() returns a + b.,TC-001,"
    "Verified,,P1\n"
)
SPINE_TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,Phase\n"
    'TC-001,LLR-001,unit,run pytest,fast,"add(2, 2) == 4",yes,'
    "tests/test_demo.py::test_add,Planned,P1\n"
)


# --- the disposition brief (SN-031) -------------------------------------------


def _disposition_repo(tmp_path, with_report=True):
    """A repo whose lane closed into `partial/` and (optionally) left the
    immutable per-close report the disposition brief is built around."""
    repo = _repo(tmp_path)
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "half.txt").write_text("half\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "half the ask")
    tip = _git(repo, "rev-parse", "HEAD")

    _write_rows(
        repo,
        [
            {"WI-ID": "WI-300", "Title": "the whole ask", "Status": "partial"},
            {
                "WI-ID": "WI-301",
                "Title": "dispose: the close recorded at docs/handbacks/",
                "SafetyClass": "adjudication",
                "Brief": "disposition",
                "SpecRef": "docs/work/partial/WI-300-the-whole-ask.md",
            },
        ],
    )
    if with_report:
        reports = repo / "docs" / "handbacks"
        reports.mkdir(parents=True)
        (reports / "WI-300-lane.md").write_text(
            "+++\n"
            'wi = "WI-300"\n'
            'branch = "lane"\n'
            'claimed_outcome = "partial"\n'
            'reason = "ran out of runway"\n'
            'commit_range = "{}..{}"\n'
            'suggested_tier = "medium"\n'
            'keep_commits = ["{}"]\n'
            "discard_commits = []\n"
            'split_decided_by = "lane"\n'
            "+++\n\n## What happened\n\nDelivered half of it.\n".format(
                base[:10], tip[:10], tip[:10]
            ),
            encoding="utf-8",
        )
    return repo


DISPOSITION_ROW = {
    "WI-ID": "WI-301",
    "SafetyClass": "adjudication",
    "Brief": "disposition",
    "SpecRef": "docs/work/partial/WI-300-the-whole-ask.md",
}


def test_the_disposition_brief_carries_the_report_the_spec_and_the_commit_facts(
    tmp_path,
):
    """Every slot from a real derivation: `SpecRef` names the closed spec, the
    spec's id finds the IMMUTABLE per-close report (the event's identity —
    SR-144), and the report's TYPED `commit_range` field drives the git facts.
    No slot is a placeholder and none is left unfilled."""
    repo = _disposition_repo(tmp_path)
    text, why = ab.compose(repo, DISPOSITION_ROW, repo / "docs/reviews/v.md")
    assert why is None, why
    # The brief, not the worker assignment.
    assert "You are an INDEPENDENT adjudicator" in text
    assert "the thing under judgement, not a premise" in text
    # The report, verbatim and labelled as a CLAIM.
    assert 'claimed_outcome = "partial"' in text
    assert "Delivered half of it." in text
    # The spec as the lane received it, and the commit facts (log + name-status).
    assert 'title = "the whole ask"' in text
    assert "half the ask" in text and "A\thalf.txt" in text
    # Fill is strict in both directions, so a leftover slot cannot survive —
    # this asserts the OUTPUT carries no hole, which is the property that
    # matters to the session that reads it.
    assert re.findall(r"\{[a-z_]+\}", text) == []
    # The typed verdict line, and the path it must be written to.
    assert "OUTCOME: COMPLETE|PARTIAL|CANCELLED successors=N" in text
    assert str(repo / "docs/reviews/v.md") in text


def test_a_clean_close_has_no_report_so_the_disposition_brief_is_refused(tmp_path):
    """`intake._complete_spot_checks` mints a disposition row for a GREEN close,
    which writes no report. The brief is built around the lane's report, so
    composing one here would ask the judge to rule on an absence — the refusal
    names what is missing and the caller sends the worker assignment."""
    repo = _disposition_repo(tmp_path, with_report=False)
    text, why = ab.compose(repo, DISPOSITION_ROW, repo / "docs/reviews/v.md")
    assert text is None
    assert "no per-close report" in why and "docs/handbacks" in why


def test_a_report_without_a_typed_commit_range_is_refused(tmp_path):
    """`commit_range` is a TYPED frontmatter field, and `{evidence}` is derived
    from it alone — never from a substring search of the report body. An
    unreadable range refuses rather than shipping a brief whose COMMIT FACTS
    section is empty."""
    repo = _disposition_repo(tmp_path)
    report = repo / "docs" / "handbacks" / "WI-300-lane.md"
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            "commit_range", "not_the_commit_range"
        ),
        encoding="utf-8",
    )
    text, why = ab.compose(repo, DISPOSITION_ROW, repo / "docs/reviews/v.md")
    assert text is None
    assert "commit_range" in why


# --- the red-TC brief (SN-030 rung 6) -----------------------------------------


def _red_tc_repo(tmp_path, tc_status="Planned"):
    repo = _repo(tmp_path)
    req = repo / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(SPINE_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(SPINE_LLRS, encoding="utf-8")
    tests = repo / "docs" / "test"
    tests.mkdir(parents=True)
    (tests / "test-cases.csv").write_text(
        SPINE_TCS.replace(",Planned,", "," + tc_status + ","), encoding="utf-8"
    )
    _write_rows(
        repo,
        [
            {
                "WI-ID": "WI-200",
                "Title": "shipped the adder",
                "Status": "done",
                "SR-Refs": "SR-001",
                "Deliverable": "shipped",
            },
            {
                "WI-ID": "WI-301",
                "Title": "adjudicate red TC TC-001",
                "SafetyClass": "adjudication",
                "Brief": "red-tc",
                "SpecRef": "docs/test/test-cases.toml",
            },
        ],
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


RED_TC_ROW = {
    "WI-ID": "WI-301",
    "SafetyClass": "adjudication",
    "Brief": "red-tc",
    "SpecRef": "docs/test/test-cases.toml",
}


def test_the_red_tc_brief_carries_the_live_census_and_the_obligation_it_covers(
    tmp_path,
):
    """`{tcs}` is assembled from the TC REGISTRY — the census line alone carries
    no Method/Expected/Evidence — and `{spine}` from the SR/LLR rows its
    parsed targets name. The census is RE-RUN here, not remembered, so the
    judge rules on the state of the world it is actually in."""
    repo = _red_tc_repo(tmp_path)
    text, why = ab.compose(repo, RED_TC_ROW, repo / "docs/reviews/v.md")
    assert why is None, why
    assert "the registry stores no test RESULT" in text
    # The TC row's own cells, joined from the registry.
    assert "- TC-001 — verifies LLR-001 — Status Planned" in text
    assert "Method/Expected: run pytest / add(2, 2) == 4" in text
    assert "tests/test_demo.py::test_add" in text
    # The obligation the test exists to prove.
    assert "- LLR-001 — add() returns a + b." in text
    assert re.findall(r"\{[a-z_]+\}", text) == []
    assert "OUTCOME: DRAFTED|NEEDS-JUDGEMENT cases=N drafts=M" in text


@pytest.mark.parametrize("green", ["Verified", "Draft", "Modified"])
def test_a_census_that_has_come_clean_refuses_rather_than_briefing_an_empty_one(
    tmp_path, green
):
    """The gap can close between the mint and the claim. Re-running the census
    is what makes that observable: an empty `{tcs}` would read as "we looked
    and there is nothing", which is exactly the hollow section the fill rule
    exists to prevent."""
    repo = _red_tc_repo(tmp_path, tc_status=green)
    text, why = ab.compose(repo, RED_TC_ROW, repo / "docs/reviews/v.md")
    assert text is None
    assert "census is now empty" in why


# --- the discriminator, and the two briefs that stay unrouted ------------------


def test_the_discriminator_is_the_declared_cell_not_the_specref(tmp_path):
    """THE MEASURED REASON the schema cost was paid. `intake._amendment_drafts`
    sets `specref` to the amended registry, so an amendment to a TEST-CASE row
    carries exactly the `SpecRef` a red-TC census row carries. Under a
    SpecRef-derived discriminator the amendment row would receive the red-TC
    brief — two briefs whose instructions contradict each other. The declared
    cell tells them apart on identical SpecRefs."""
    repo = _red_tc_repo(tmp_path)
    same_specref = dict(RED_TC_ROW, Brief="amendment")
    routed, _why = ab.compose(repo, RED_TC_ROW, repo / "v.md")
    other, why = ab.compose(repo, same_specref, repo / "v.md")
    assert "the registry stores no test RESULT" in routed
    assert other is None and "amendment" in why


@pytest.mark.parametrize("brief", ["amendment", "conflict"])
def test_the_two_unrouted_briefs_refuse_and_name_themselves(tmp_path, brief):
    """Left unrouted on purpose (see adjudicate_brief.py's header): `conflict`
    has no minting path and a `{digests}` slot no function computes, and
    `amendment`'s `{rows}` producer selects the rows its own minting condition
    excludes. Wiring either would mean filling a slot with something, which is
    the failure this whole module is shaped around."""
    repo = _repo(tmp_path)
    text, why = ab.compose(repo, {"WI-ID": "WI-9", "Brief": brief}, repo / "v.md")
    assert text is None
    assert brief in why and "no evidence assembler" in why
    assert brief not in ab.ROUTED


def test_an_absent_or_unknown_brief_refuses_rather_than_guessing(tmp_path):
    repo = _repo(tmp_path)
    _text, why = ab.compose(repo, {"WI-ID": "WI-9"}, repo / "v.md")
    assert "declares no `brief`" in why
    _text, why = ab.compose(repo, {"WI-ID": "WI-9", "Brief": "typo"}, repo / "v.md")
    assert "unknown brief" in why


def test_every_routed_brief_names_a_shipped_template():
    """`ROUTED` is derived from the assembler table, so a brief cannot be
    declared routed without one — and every key must resolve to a real
    shipped prompt."""
    assert set(ab.ROUTED) <= set(ab.BRIEF_PROMPTS)
    prompts = load_script("prompts")
    for brief in ab.BRIEF_PROMPTS:
        assert prompts.load(ab.BRIEF_PROMPTS[brief])


# --- the mint declares it (intake) --------------------------------------------


def test_every_minted_adjudication_row_declares_which_brief_it_wants():
    """The declaration is written where the knowledge is: the mint knows which
    judgement it is asking for, and nothing downstream has to re-derive it.
    A mint site that forgot would produce an adjudication row that silently
    falls back to the worker assignment."""
    source = (intake.__file__ or "").strip()
    assert source
    with open(source, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    sites = [i for i, ln in enumerate(lines) if ln.strip() == '"kind": "adjudication",']
    assert sites, "no adjudication mint sites found — guard vacuous"
    for i in sites:
        assert lines[i + 1].strip().startswith('"brief": "'), lines[i + 1]
        declared = lines[i + 1].split('"')[3]
        assert declared in ab.BRIEF_PROMPTS, declared


# --- the session provably receives it (fake-CLI prompts.txt capture) ----------

# The fake agent CLI: it records every prompt it is handed, then behaves as the
# brief it was given tells it to. An ADJUDICATOR session writes the typed
# verdict line to the declared path and ends its commit with the result
# trailer; anything else is a worker assignment and builds. Which branch it
# takes is decided by the brief's own words, so a session that received the
# WRONG prompt cannot accidentally satisfy the assertion.
FAKE_AGENT = r"""
import argparse, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "prompts.txt"), "a", encoding="utf-8") as fh:
    fh.write("=== session ===\n" + args.prompt + "\n")
if "INDEPENDENT adjudicator" in args.prompt:
    where = re.search(r"Write your verdict to (\S+)", args.prompt).group(1)
    vpath = pathlib.Path(where.rstrip(":"))
    wi = re.search(r"trailer .WI: (WI-\d+).", args.prompt).group(1)
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text(
        "- [MINOR] the claim -> why -> the concrete change\n"
        + (ctl / "verdict").read_text(encoding="utf-8").strip() + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", str(vpath)], check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "adjudication verdict\n\nWI: " + wi + "\n"],
        check=True,
    )
    sys.exit(0)
wi = re.search(r"- WI: (WI-\d+)", args.prompt).group(1)
pathlib.Path("work-" + wi + ".txt").write_text("built", encoding="utf-8")
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(
    ["git", "commit", "-q", "-m", "build " + wi + "\n\nWI: " + wi + "\n"], check=True
)
sys.exit(0)
"""


def _session(tmp_path, repo, wi, verdict_line):
    """Run the real loop against the fake CLI on a claimed train branch;
    return `(proc, prompts_text, control_dir)`."""
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")
    ctl = tmp_path / "ctl"
    ctl.mkdir()
    (ctl / "verdict").write_text(verdict_line, encoding="utf-8")
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
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
            "3",
            "--wi",
            wi,
            "--train",
            "t1",
        ],
        cwd=repo,
    )
    captured = ctl / "prompts.txt"
    return proc, (captured.read_text(encoding="utf-8") if captured.is_file() else "")


def test_a_disposition_rows_session_receives_the_disposition_brief(tmp_path):
    """The end-to-end bar: a claimed adjudication row's session is handed ITS
    OWN brief — not the worker assignment — and the typed verdict line the
    brief demands lands at the declared path."""
    repo = _disposition_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "registry + report")
    proc, prompts = _session(tmp_path, repo, "WI-301", "OUTCOME: PARTIAL successors=1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    # The disposition brief, with its assembled evidence — and NOT the worker
    # assignment's assignment block.
    assert "wearing a DIFFERENT hat from the lane that stopped" in prompts
    assert 'claimed_outcome = "partial"' in prompts
    assert "A\thalf.txt" in prompts
    assert "- WI: WI-301 —" not in prompts
    assert "resume from docs/status.md" not in prompts
    # The verdict is a recorded, committed artefact at the path the brief named.
    verdicts = sorted((repo / "docs" / "reviews").rglob("*ADJUDICATE*.md"))
    assert len(verdicts) == 1, verdicts
    assert "OUTCOME: PARTIAL successors=1" in verdicts[0].read_text(encoding="utf-8")


def test_a_red_tc_rows_session_receives_the_red_tc_brief(tmp_path):
    repo = _red_tc_repo(tmp_path)
    proc, prompts = _session(
        tmp_path, repo, "WI-301", "OUTCOME: DRAFTED cases=1 drafts=1"
    )
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "the registry stores no test RESULT" in prompts
    assert "- TC-001 — verifies LLR-001 — Status Planned" in prompts
    assert "- LLR-001 — add() returns a + b." in prompts
    assert "- WI: WI-301 —" not in prompts
    verdicts = sorted((repo / "docs" / "reviews").rglob("*ADJUDICATE*.md"))
    assert len(verdicts) == 1, verdicts
    assert "OUTCOME: DRAFTED" in verdicts[0].read_text(encoding="utf-8")


def test_an_unfillable_brief_sends_the_worker_assignment_and_says_why(tmp_path):
    """The fallback, end to end. A clean close's disposition row has no report,
    so the session gets the ordinary assignment — and the loop PRINTS the
    refusal rather than swapping the brief silently."""
    repo = _disposition_repo(tmp_path, with_report=False)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "registry")
    proc, prompts = _session(tmp_path, repo, "WI-301", "unused")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "INDEPENDENT adjudicator" not in prompts
    assert "- WI: WI-301 —" in prompts
    assert "route [ADJUDICATE]: worker assignment —" in proc.stdout
    assert "no per-close report" in proc.stdout
