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

import csv
import io
import re
import shlex
import subprocess
import sys

import pytest
from conftest import (
    env_gate_skipif,
    load_script,
    pin_autocrlf,
    run_py,
    set_process_key,
    SCRIPTS,
)

ab = load_script("adjudicate_brief")
baseline_snapshot = load_script("baseline_snapshot")
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
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
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
    "demo,the sum is right,Must,Test,Approved,P1,core\n"
)
SPINE_LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component,Phase\n"
    "LLR-001,SR-001,add impl,src/demo.py,add,add() returns a + b.,TC-001,"
    "Approved,,P1\n"
)
SPINE_TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,Phase\n"
    'TC-001,LLR-001,unit,run pytest,fast,"add(2, 2) == 4",yes,'
    "tests/test_demo.py::test_add,Approved,P1\n"
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
    names what is missing, and the caller HOLDS the row rather than
    downgrading it to a build."""
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


# THE RED-TC FIXTURE'S DEFAULT MOVED OUT OF VOCABULARY AT D-9 STEP 5, and the
# move is a finding rather than a tidy-up. `red_tc_census` names a red TC by
# EXEMPTION — anything outside `dispatch._TC_NOT_RED` is red — and this fixture
# used `Planned`, the one LIVE value that sat outside it. OI-30 D1 folded
# `Planned` into `Approved`, and the narrowed enum is now EXACTLY the exempt set,
# so no conformant repo can carry a red TC any more. `Implemented` is the honest
# remaining population: the value a downstream repo mid-migration still carries,
# which the integrity floor names and this rung still judges. That the rung is
# otherwise vacuous on a migrated tree is recorded for the sitting (log
# 2026-08-15m) — it is the step-2 note's own "deleted feature" hazard arriving
# through the rename rather than through the exempt set.
def _red_tc_repo(tmp_path, tc_status="Implemented"):
    repo = _repo(tmp_path)
    req = repo / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(SPINE_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(SPINE_LLRS, encoding="utf-8")
    tests = repo / "docs" / "test"
    tests.mkdir(parents=True)
    (tests / "test-cases.csv").write_text(
        SPINE_TCS.replace(",Approved,", "," + tc_status + ","), encoding="utf-8"
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
    assert "- TC-001 — verifies LLR-001 — Status Implemented" in text
    assert "Method/Expected: run pytest / add(2, 2) == 4" in text
    assert "tests/test_demo.py::test_add" in text
    # The obligation the test exists to prove.
    assert "- LLR-001 — add() returns a + b." in text
    assert re.findall(r"\{[a-z_]+\}", text) == []
    assert "OUTCOME: DRAFTED|NEEDS-JUDGEMENT cases=N drafts=M" in text


# `Founded` replaced `Modified` at D-9 steps 7/8: the exempt set is the whole
# closed enum, so the parametrization is the enum itself.
@pytest.mark.parametrize("green", ["Approved", "Drafted", "Founded"])
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


# `Verifies` is required too, but it cannot be driven through the census: a row
# with no targets is not red by definition (`red_tc_census` skips it), so the
# empty-census refusal fires first. It stays in `TC_CELLS` as a guard for any
# future caller that does not come through the census.
@pytest.mark.parametrize("cell", [c for c in ab.TC_CELLS if c != "Verifies"])
def test_a_tc_row_missing_any_listed_cell_refuses_rather_than_rendering_a_dash(
    tmp_path, cell
):
    """The empty-census refusal, one level down. A dash in an evidence listing
    reads as "looked for, not applicable" when the truth is "the registry never
    said" — and this brief's whole method is *run the cited evidence and say
    what you observed*, which a row missing its Evidence/Method/Expected cannot
    support. So every listed cell is required, and the refusal names it."""
    repo = _red_tc_repo(tmp_path)
    tcs = repo / "docs" / "test" / "test-cases.csv"
    header, row = tcs.read_text(encoding="utf-8").splitlines()[:2]
    cells = next(csv.reader([row]))
    cells[next(csv.reader([header])).index(cell)] = ""
    out = io.StringIO()
    csv.writer(out, lineterminator="\n").writerows([next(csv.reader([header])), cells])
    tcs.write_text(out.getvalue(), encoding="utf-8")
    text, why = ab.compose(repo, RED_TC_ROW, repo / "v.md")
    assert text is None
    assert cell in why and "placeholder" in why


def test_a_target_with_no_normative_text_refuses(tmp_path):
    """A target that does not resolve — or whose normative cell is empty — is
    RETURNED by `_spine_excerpt`, never silently dropped. A dropped target
    leaves a `{spine}` section that still looks complete, which is the
    half-filled brief in its quietest form."""
    repo = _red_tc_repo(tmp_path)
    llrs = repo / "docs" / "requirements" / "low-level-requirements.csv"
    llrs.write_text(
        llrs.read_text(encoding="utf-8").replace("add() returns a + b.", ""),
        encoding="utf-8",
    )
    text, why = ab.compose(repo, RED_TC_ROW, repo / "v.md")
    assert text is None
    assert "LLR-001" in why and "placeholder" in why


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


def test_every_shipped_brief_is_routed_and_the_retired_one_is_gone(tmp_path):
    """There is no unrouted brief any more, and that is a claim worth pinning
    both ways.

    `conflict` was unrouted for THREE reasons at once — nothing minted such a
    row, no assembler filled its slots, and nothing read the `needs=` its own
    grammar demanded — so it was retired rather than filled, and `consolidate`
    carries its three questions plus the exit it lacked. A row declaring the
    retired key must therefore refuse as an UNKNOWN brief, not as one whose
    assembler is missing: the kit no longer ships it at all.

    `amendment` was the other unrouted one until D-9 step 4b — see the tests
    below, which are its positive successors."""
    repo = _repo(tmp_path)
    assert set(ab.ROUTED) == set(ab.BRIEF_PROMPTS)
    text, why = ab.compose(repo, {"WI-ID": "WI-9", "Brief": "conflict"}, repo / "v.md")
    assert text is None and "unknown brief" in why
    assert "conflict" not in ab.BRIEF_PROMPTS
    # ...and the no-brief refusal is still reachable, so the rule-3 HOLD does
    # not quietly become dead code.
    assert ab.compose(repo, {"WI-ID": "WI-9"}, repo / "v.md")[1]


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


def test_no_mint_can_declare_a_brief_the_kit_does_not_ship():
    """The declaration is written where the knowledge is — the mint knows which
    judgement it is asking for — and it is now LOAD-BEARING in the expensive
    direction: a declared brief the kit cannot compose HOLDS the row for a
    human. So a typo'd or invented value would not degrade quietly, it would
    stop an unattended run.

    Deliberately NOT asserted: that every mint site declares one. Two arms
    (the report-less cancellation, the clean-close spot check) declare none on
    purpose, because the kit ships no brief for them and a false declaration
    would page a human for routine work.

    BOTH MINT SOURCES ARE SCANNED, not just `intake`: the consolidation census
    lives in its own module (its decision half is testable with no repository)
    and declares `consolidate` there, so a guard reading `intake.py` alone would
    have gone vacuous for the newest brief on the day it landed."""
    declared = set()
    for module in (intake, load_script("consolidate")):
        source = (module.__file__ or "").strip()
        assert source
        with open(source, encoding="utf-8") as handle:
            text = handle.read()
        declared |= set(re.findall(r'"brief":\s*"([^"]*)"', text))
        declared |= set(re.findall(r'^BRIEF = "([^"]*)"', text, re.M))
    assert declared, "no brief declarations found — guard vacuous"
    assert declared <= set(ab.BRIEF_PROMPTS), sorted(declared - set(ab.BRIEF_PROMPTS))
    # Every brief the kit can actually serve must be declared somewhere, or the
    # routed briefs would have no producer of rows at all.
    assert set(ab.ROUTED) <= declared


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
    # `.` joins `:` in the strip set: the amendment template ends its sentence
    # with a period, so the greedy \S+ swallows it and the verdict landed at
    # "<path>." — a file the checker never looks at, so the row stayed open.
    vpath = pathlib.Path(where.rstrip(":."))
    wi = re.search(r"trailer .WI: (WI-\d+).", args.prompt).group(1)
    line = (ctl / "verdict").read_text(encoding="utf-8").strip()
    # NONE models the judge that commits but never rules: the WI trailer that
    # makes a WORKER done, with no verdict artifact behind it.
    if line != "NONE":
        vpath.parent.mkdir(parents=True, exist_ok=True)
        vpath.write_text(
            "- [MINOR] the claim -> why -> the concrete change\n" + line + "\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", str(vpath)], check=True)
    else:
        pathlib.Path("ruled-on-nothing.txt").write_text("", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], check=True)
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
    assert "- TC-001 — verifies LLR-001 — Status Implemented" in prompts
    assert "- LLR-001 — add() returns a + b." in prompts
    assert "- WI: WI-301 —" not in prompts
    verdicts = sorted((repo / "docs" / "reviews").rglob("*ADJUDICATE*.md"))
    assert len(verdicts) == 1, verdicts
    assert "OUTCOME: DRAFTED" in verdicts[0].read_text(encoding="utf-8")


def test_an_unfillable_declared_brief_HOLDS_rather_than_dispatching_a_builder(
    tmp_path,
):
    """FAIL CLOSED, end to end. A row that declares a brief the kit cannot
    assemble never reaches a session at all: the loop pages instead.

    This is the property the whole seam turns on. Falling back to the ordinary
    assignment here would re-open the defect WI-424 exists to close — the judge
    briefed as a builder — on a routinely minted path, and it would do it
    QUIETLY, since a builder session ends DONE like any other. `EXIT_NEEDS_HUMAN`
    is also what makes the hold durable: `dispatch._lane_close` turns it into a
    `handback.close_partial`, whose `blockref` keeps an unattended run from
    re-picking the row."""
    repo = _disposition_repo(tmp_path, with_report=False)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "registry")
    proc, prompts = _session(tmp_path, repo, "WI-301", "unused")
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    # No session ran at all — not a judge's, and emphatically not a builder's.
    assert prompts == ""
    assert "no usable brief" in proc.stdout
    assert "no per-close report" in proc.stdout
    assert "would brief the judge as a builder" in proc.stdout
    # ...and no work was committed under the row.
    assert "WI-301" not in _git(repo, "log", "--format=%(trailers:key=WI,valueonly)")


def test_the_live_amendment_mint_is_now_BRIEFED_not_held(tmp_path):
    """THE CAPABILITY UNLOCK (D-9 step 4b). `intake._amendment_drafts` mints
    `brief = "amendment"` routinely, and until the snapshot landed every one of
    those rows HELD for a human — the largest live hold in the machinery. Two
    things blocked it, and the snapshot answers both: the `{rows}` producer
    selected on a status literal that the minting condition excluded by
    construction, and `{baseline}` resolved to the amendment commit itself, i.e.
    the text under judgement as its own accepted anchor.

    This is the inverse of the test it replaces: the row now composes."""
    repo = _amendment_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    proc, prompts = _session(tmp_path, repo, "WI-301", "VERDICT: MEANING rows=1")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    # The judge received the amendment brief, with the snapshot as its anchor
    # and the before/after the model computed — not the generic worker prompt.
    assert "Did this amendment change the requirement's MEANING" in prompts
    assert baseline_snapshot.SNAPSHOT_DIR in prompts
    assert "The system shall add two numbers." in prompts  # the blessed text
    assert "refuse floats" in prompts  # the text under judgement


def _spine_repo(tmp_path):
    """A repo carrying the demo spine and nothing else — the base both the
    red-TC and the amendment fixtures build on. Written separately from
    `_red_tc_repo` because that one also mints its OWN `WI-301`, and a second
    row with the same id would leave the loader picking between two briefs."""
    repo = _repo(tmp_path)
    req = repo / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(SPINE_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(SPINE_LLRS, encoding="utf-8")
    tests = repo / "docs" / "test"
    tests.mkdir(parents=True)
    (tests / "test-cases.csv").write_text(SPINE_TCS, encoding="utf-8")
    return repo


def _amend(repo):
    """Move SR-001's `Requirement` — an APPROVED cell — leaving its Status put.
    This is the D-9 shape exactly: the text changed and nothing flipped."""
    srs = repo / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(
            "The system shall add two numbers.",
            "The system shall add two integers and refuse floats.",
        ),
        encoding="utf-8",
    )


def _amendment_repo(tmp_path):
    """A repo with a spine, an approved snapshot, an amended approved cell, and
    the adjudication row `intake` would have minted for it."""
    repo = _spine_repo(tmp_path)
    baseline_snapshot.copy_live(repo, seed=True)
    _amend(repo)
    _write_rows(
        repo,
        [
            {
                "WI-ID": "WI-301",
                "Title": "adjudicate: SR-001 - approved cell(s) amended",
                "SafetyClass": "adjudication",
                "Brief": "amendment",
                "SpecRef": "docs/requirements/system-requirements.toml",
            }
        ],
    )
    return repo


def test_the_amendment_brief_carries_the_snapshot_as_its_anchor(tmp_path):
    # Rule 1, mechanized for this brief: the anchor must be the text a human
    # blessed BEFORE the change, never the change itself. Both halves are
    # asserted — the before text is present, and it is labelled as not being
    # the thing under judgement.
    repo = _amendment_repo(tmp_path)
    values, why = ab.amendment_values(repo, {"WI-ID": "WI-301", "Brief": "amendment"})
    assert why is None, why
    assert baseline_snapshot.SNAPSHOT_DIR in values["baseline"]
    assert "not the change under judgement" in values["baseline"]
    assert "The system shall add two numbers." in values["rows"]  # before
    assert "refuse floats" in values["rows"]  # after


def test_only_APPROVED_cells_reach_the_judge(tmp_path):
    # A traced cell is ruled non-attesting (§A5.1), so asking a judge to rule
    # "meaning or clarity" on a re-pointed Phase cell asks a question the
    # ruling already answers. Drive it: move ONLY a traced cell.
    repo = _spine_repo(tmp_path)
    baseline_snapshot.copy_live(repo, seed=True)
    srs = repo / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(
            ",Test,Approved,P1,", ",Test,Approved,P9,"
        ),
        encoding="utf-8",
    )
    values, why = ab.amendment_values(repo, {"WI-ID": "WI-301", "Brief": "amendment"})
    # Stronger than "the cell is filtered out of the listing": a traced-only
    # change never makes the row DRIFT in the first place, so it does not reach
    # the model, the brief, or a judge. One ruling (§A5.1), enforced once.
    assert values is None
    assert "differs from its" in why, why


def test_with_no_snapshot_the_brief_HOLDS_and_says_FIRST_APPROVAL(tmp_path):
    # The honest degrade, and it is a HOLD rather than a brief. A repo that has
    # never signed has no accepted anchor at all, so "did this amendment change
    # the meaning?" is not the question its rows pose. Fabricating an anchor is
    # the failure rule 1 exists to prevent; rendering a before/after with an
    # empty before is the failure rule 2 exists to prevent. Naming the state is
    # neither.
    repo = _spine_repo(tmp_path)
    assert not baseline_snapshot.exists(repo)
    values, why = ab.amendment_values(repo, {"WI-ID": "WI-301", "Brief": "amendment"})
    assert values is None
    assert "FIRST-APPROVAL" in why and "no accepted anchor" in why


def test_the_MEANING_aftermath_is_DERIVED_from_the_dial_not_left_to_the_judge(tmp_path):
    # done-when 3 (owner ruling 2026-09-01). This template used to end "the
    # flip, if one is owed, is the mechanical tool's act, not yours" — true when
    # written, and FALSE since OI-45 ruled (b) retired that tool
    # (intake._apply_flips writes nothing, permanently). So a MEANING verdict on
    # a loop-held rung ended at a brief nobody was owed, which contradicts the
    # loop-held doctrine. What replaces it is not a longer sentence but a
    # DERIVED one: the dial is a repo declaration the judge would otherwise have
    # to go read mid-verdict, which is the shape that produces a session
    # confidently performing the owner's act.
    repo = _amendment_repo(tmp_path)
    row = {"WI-ID": "WI-301", "Brief": "amendment"}

    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Needs")
    values, why = ab.amendment_values(repo, row)
    assert why is None, why
    assert "RELEASED" in values["aftermath"]
    assert "re-attested BY YOU, in this session" in values["aftermath"]

    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Release")
    values, why = ab.amendment_values(repo, row)
    assert why is None, why
    assert "still HOLDS for a human" in values["aftermath"]
    assert "the signature is the owner's" in values["aftermath"]

    # ...and the retired sentence never reaches the JUDGE, which is the property
    # that matters: a brief that says both things is worse than one that says
    # the wrong thing. It survives in the dispatcher notes — stripped before
    # sending — as the record of why this slot exists at all.
    text, why = ab.compose(repo, row, repo / "docs/reviews/v.md")
    assert why is None, why
    assert "the mechanical tool's act, not yours" not in text
    assert "the signature is the owner's" in text  # the aftermath landed instead
    assert re.findall(r"\{[a-z_]+\}", text) == []
    template = (
        SCRIPTS.parent / "prompts" / "adjudicate-amendment.template.md"
    ).read_text(encoding="utf-8")
    assert "the mechanical tool's act, not yours" in template  # in the NOTES only


# --- the first-approval brief (owner ruling 2026-09-01) -----------------------


def _first_approval_repo(tmp_path):
    """A repo whose lane left a `Drafted` LLR under an `Approved` SR — the exact
    population the ruling hands to the adjudicator, and the one no drift arm can
    see: a row below approval has made no claim to fall from.

    THE DIAL IS DECLARED, and it has to be. This arm exists only for rungs the
    declared gate authority has RELEASED; with no `docs/process.toml` the dial
    falls back to the shipped `DevStg-Release`, which holds every rung, so an
    undeclared fixture is not this arm's scenario at all — it is the owner's.
    That omission is what let the first cut ship a brief with no dial filter and
    a green test beside it (WI-572 REVIEW-A).

    AND THE SCOPE IS DECLARED, for the same class of reason. The mint writes the
    rows it handed over into `Adjudicates`; a fixture that omitted the cell would
    exercise a row `intake` cannot produce, and the assembler now refuses one."""
    repo = _spine_repo(tmp_path)
    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Needs")
    baseline_snapshot.copy_live(repo, seed=True)
    llrs = repo / "docs" / "requirements" / "low-level-requirements.csv"
    llrs.write_text(
        llrs.read_text(encoding="utf-8").replace("TC-001,Approved,", "TC-001,Drafted,"),
        encoding="utf-8",
    )
    _write_rows(
        repo,
        [
            {
                "WI-ID": "WI-301",
                "Title": "adjudicate: LLR-001 - await a FIRST APPROVAL",
                "SafetyClass": "adjudication",
                "Brief": "first-approval",
                "Adjudicates": "LLR-001",
                "SpecRef": "docs/requirements/low-level-requirements.toml",
            }
        ],
    )
    return repo


# The adjudication row as `intake` mints it — brief AND scope, because the
# assembler needs both and a bare `{"Brief": ...}` dict is a row this mint
# cannot produce.
def _fa_row(**over):
    row = {"WI-ID": "WI-301", "Brief": "first-approval", "Adjudicates": "LLR-001"}
    row.update(over)
    return row


def test_the_first_approval_brief_carries_the_WHOLE_CHAIN(tmp_path):
    # The owner's CONTEXT reason, mechanized: approving a row means holding its
    # whole chain — the parent SR, the sibling LLRs, the tests — which is the
    # thing one work item does not hold and is therefore why the act is the
    # adjudicator's. So the brief must show the chain, not the changed cells.
    repo = _first_approval_repo(tmp_path)
    values, why = ab.first_approval_values(repo, _fa_row())
    assert why is None, why
    chain = values["chain"]
    assert "SR-001" in chain and "LLR-001" in chain and "TC-001" in chain
    # The row awaiting the act is MARKED as such — a chain rendered without
    # saying which rows are the question reads as a report, not a brief.
    assert "LLR-001 [AWAITING FIRST APPROVAL]" in chain
    assert "SR-001 [approved]" in chain
    # ...and the act's own argument is DERIVED, so the approving commit records
    # the scope it actually touched rather than whatever the session typed.
    assert (
        values["registries"] == "docs/requirements/low-level-requirements.toml=WI-301"
    )
    assert baseline_snapshot.SNAPSHOT_DIR in values["baseline"]

    # ...and the whole brief composes with NO hole. Strict fill makes the
    # template's slots and this assembler's keys ONE contract, so a slot added
    # to either side without the other refuses instead of shipping a judge a
    # prompt with `{chain}` still in it.
    text, why = ab.compose(repo, _fa_row(), repo / "docs/reviews/v.md")
    assert why is None, why
    assert re.findall(r"\{[a-z_]+\}", text) == []
    assert "You are an INDEPENDENT adjudicator" in text
    assert "OUTCOME: APPROVE|RETURN rows=N" in text
    # The act itself is spelled out, because nothing downstream performs it for
    # the session: the mechanical writer retired (OI-45 ruled (b)), so the flip
    # and its anchoring copy are this session's own reviewed commit.
    assert "python scripts/intake.py snapshot --approves" in text
    assert "one reviewed commit" in text


def test_the_first_approval_brief_cannot_stop_before_its_approved_act(tmp_path):
    repo = _first_approval_repo(tmp_path)
    text, why = ab.compose(repo, _fa_row(), repo / "docs/reviews/v.md")
    assert why is None, why
    terminal = text.split("THEN, AND ONLY AFTER THAT VERDICT IS RECORDED", 1)[1]
    assert "If ANY row line says `APPROVE`" in terminal
    assert "mixed batch whose `OUTCOME` is `RETURN`" in terminal
    assert "Stop only after that approval commit is recorded" in terminal
    assert (
        "Only when EVERY row line says `RETURN` may you stop without changing"
        in terminal
    )


def test_the_first_approval_brief_REFUSES_once_the_rows_are_ruled(tmp_path):
    # Rule 2, and `red_tc_values`' live-recompute rule applied to this arm: the
    # row is minted at a merge and claimed later, so by composition time another
    # act may have approved or withdrawn every row it was minted for. A brief
    # built from the mint's remembered listing would ask the judge to rule on a
    # world that no longer exists; an emptied population refuses instead.
    repo = _first_approval_repo(tmp_path)
    llrs = repo / "docs" / "requirements" / "low-level-requirements.csv"
    llrs.write_text(
        llrs.read_text(encoding="utf-8").replace("TC-001,Drafted,", "TC-001,Approved,"),
        encoding="utf-8",
    )
    baseline_snapshot.copy_live(repo, seed=True)  # the act's own anchor moved too
    values, why = ab.first_approval_values(repo, _fa_row())
    assert values is None
    assert "still awaiting a first approval" in why, why


def test_the_first_approval_brief_never_hands_the_judge_a_HELD_row(tmp_path):
    # WI-572 REVIEW-A, the MAJOR finding. The mint filters the population by the
    # dial (`intake._released_drafted_rows`); this assembler RE-RESOLVES it live
    # from `reattest_model`, which is dial-blind by design — and the first cut
    # did not put the filter back. Under a MIXED dial that is not a cosmetic
    # gap: the brief rendered a held `Drafted` SR beside a released `Drafted`
    # LLR, marked both as awaiting the act, and derived a `--approves` argument
    # naming BOTH registries — a prompt instructing an adjudicator to perform a
    # signature the owner owes. The filter now lives in ONE table both ends read.
    repo = _first_approval_repo(tmp_path)
    srs = repo / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(
            ",Approved,P1,core", ",Drafted,P1,core"
        ),
        encoding="utf-8",
    )
    # `DevStg-Reqs` holds the SR tier for the owner and releases the LLR tier
    # below it — the exact mixed dial the finding names. The scope names BOTH
    # rows, which is the honest shape of this scenario: the mint filtered by the
    # dial it saw (`DevStg-Needs`, releasing both), and the owner TIGHTENED it
    # afterwards. The dial is therefore re-checked at composition as well as at
    # the mint — a scope check alone would have handed over the SR.
    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Reqs")
    row = _fa_row(Adjudicates="SR-001;LLR-001")
    values, why = ab.first_approval_values(repo, row)
    assert why is None, why

    # Both halves. The held row is SHOWN — it is the chain, and holding the
    # chain is the whole reason this act is the adjudicator's — but it is shown
    # as the owner's...
    assert "SR-001 [AWAITING FIRST APPROVAL - HELD FOR THE OWNER" in values["chain"]
    assert "LLR-001 [AWAITING FIRST APPROVAL]" in values["chain"]
    # ...and it contributes NO registry, so the act's own recorded scope cannot
    # carry it even if the session ignored every word of the prose.
    assert (
        values["registries"] == "docs/requirements/low-level-requirements.toml=WI-301"
    )
    text, why = ab.compose(repo, row, repo / "docs/reviews/v.md")
    assert why is None, why
    assert "never a `HELD FOR THE OWNER` one" in text

    # And when the dial holds EVERY rung — the kit's shipped default, so this is
    # what an adopter who has declared nothing gets — the arm has no question at
    # all and REFUSES, rather than composing the owner's sitting as a session's
    # to-do list.
    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Release")
    values, why = ab.first_approval_values(repo, row)
    assert values is None
    assert "HOLDS for a human" in why, why


def test_the_first_approval_act_formats_a_multi_registry_batch_for_the_cli(tmp_path):
    repo = _first_approval_repo(tmp_path)
    srs = repo / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(
            ",Approved,P1,core", ",Drafted,P1,core"
        ),
        encoding="utf-8",
    )
    values, why = ab.first_approval_values(repo, _fa_row(Adjudicates="SR-001;LLR-001"))
    assert why is None, why
    assert values["registries"] == (
        "docs/requirements/low-level-requirements.toml=WI-301;"
        "docs/requirements/system-requirements.toml=WI-301"
    )
    assert baseline_snapshot.parse_approves(values["registries"]) == {
        "docs/requirements/low-level-requirements.toml": "WI-301",
        "docs/requirements/system-requirements.toml": "WI-301",
    }


def _two_registry_repo(tmp_path):
    """`_first_approval_repo` with its SR withdrawn too, so the act spans TWO
    registries — the batch shape that makes both round-7 findings reachable."""
    repo = _first_approval_repo(tmp_path)
    srs = repo / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(
            ",Approved,P1,core", ",Drafted,P1,core"
        ),
        encoding="utf-8",
    )
    return repo


def _shell_command_count(line):
    """How many commands a POSIX shell would read `line` as.

    `shlex` with `punctuation_chars` yields an unquoted `;` as its own token and
    keeps a quoted one inside its string, which is exactly the distinction under
    test. `shlex.split` alone cannot serve: it is a lexer, not a parser, and
    returns the whole `a;b` run as ONE token whether it is quoted or not — so a
    test written on it would have passed against the defect."""
    lex = shlex.shlex(line, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    return sum(1 for token in lex if token == ";") + 1


def test_the_rendered_snapshot_command_survives_a_shell(tmp_path):
    # WI-572 REVIEW-A round 7, MAJOR 2. `{registries}` is `;`-joined by
    # `format_approves` and rendered into a SHELL command line in the template.
    # Unquoted, a two-registry batch is two commands: the first snapshots one
    # registry, the second runs `docs/test/test-cases.toml=WI-301` as a program
    # — so only half the act is anchored and the merge then refuses it. The
    # template quotes the argument; this pins that the rendered line is ONE
    # command, which is the property that actually matters.
    repo = _two_registry_repo(tmp_path)
    row = _fa_row(Adjudicates="SR-001;LLR-001")
    text, why = ab.compose(repo, row, tmp_path / "verdict.md")
    assert why is None, why
    line = next(ln for ln in text.splitlines() if "intake.py snapshot --approves" in ln)
    command = line[line.index("`python") + 1 :]
    command = command[: command.index("`")]
    # The premise: this batch really does span two registries, so an unquoted
    # render WOULD split. Without it the assertion below is vacuous.
    assert ";" in command
    assert _shell_command_count(command) == 1, command
    # ...and the same string unquoted is the defect, proving the guard bites.
    assert _shell_command_count(command.replace('"', "")) == 2


def test_a_mixed_batch_can_tell_which_rows_each_approves_token_covers(tmp_path):
    # WI-572 REVIEW-A round 7, MAJOR 3. `{registries}` is fixed at COMPOSITION
    # time, but the template blesses a MIXED verdict ("approve the rows that are
    # ready, return the rest") and the approve/return split exists only after
    # it. An adjudication that returned one registry's rows in full still ran
    # the composed command, re-anchoring that registry's unreviewed live text —
    # and `acceptance_record.adjudication_approval_refusal` then stopped the
    # merge as WIDENED. The session can only DROP a token if the brief says
    # which rows it stands for, so the brief derives that mapping.
    repo = _two_registry_repo(tmp_path)
    values, why = ab.first_approval_values(repo, _fa_row(Adjudicates="SR-001;LLR-001"))
    assert why is None, why
    covers = values["approves_rows"]
    assert (
        "`docs/requirements/low-level-requirements.toml=WI-301` covers LLR-001"
        in covers
    )
    assert "`docs/requirements/system-requirements.toml=WI-301` covers SR-001" in covers
    # EVERY token of the derived argument is accounted for. A mapping that named
    # only some of them would leave the session guessing on the rest, which is
    # the state this replaces.
    for rel in baseline_snapshot.parse_approves(values["registries"]):
        assert "`{}=".format(rel) in covers, rel


def test_a_row_hanging_under_two_SRs_is_named_once_in_its_token(tmp_path):
    # The dedupe half of MAJOR 3, found by DRIVING the fix against this repo's
    # live spine rather than against a fixture: `_render_chain` visits a row
    # ONCE PER SR CHAIN it hangs under, so an LLR with two parents rendered as
    # `covers LLR-001, LLR-001`. A token that names one row twice reads as two
    # rows, and the whole point of the mapping is that the session can count
    # what it returned against what a token covers.
    repo = _first_approval_repo(tmp_path)
    req = repo / "docs" / "requirements"
    srs = req / "system-requirements.csv"
    # A SECOND approved parent for the same Drafted LLR — the two-chain shape.
    srs.write_text(
        srs.read_text(encoding="utf-8")
        + "SR-002,Adds again,SN-001,The system shall also add.,a second parent,"
        "the sum is right,Must,Test,Approved,P1,core\n",
        encoding="utf-8",
    )
    llrs = req / "low-level-requirements.csv"
    llrs.write_text(
        llrs.read_text(encoding="utf-8").replace(
            "LLR-001,SR-001,", "LLR-001,SR-001;SR-002,"
        ),
        encoding="utf-8",
    )
    values, why = ab.first_approval_values(repo, _fa_row())
    assert why is None, why
    # The premise: the row really is rendered under BOTH chains, so a walk that
    # appended per visit would have listed it twice. Without this the assertion
    # below passes on a one-chain fixture and proves nothing.
    assert values["chain"].count("chain of SR-") == 2
    assert values["chain"].count("LLR-001 [AWAITING FIRST APPROVAL]") == 2
    assert values["approves_rows"].count("LLR-001") == 1


def test_the_first_approval_act_cannot_widen_past_the_rows_the_merge_handed_over(
    tmp_path,
):
    # WI-572 REVIEW-A round 4, the MAJOR finding. The assembler re-derives its
    # population LIVE from `trace.reattest_model`, which walks EVERY SR in the
    # repo — so with nothing to intersect against, a merge that staged ONE
    # `Drafted` LLR minted a row whose brief then told its session it held the
    # approval authority for the whole repo's `Drafted` backlog, and derived a
    # `--approves` argument naming every registry those rows live in. That
    # contradicts the doctrine ("over the `Drafted` rows the lane handed over")
    # and the owner's concurrency reason for moving the act to trunk: the
    # approval snapshot must not move across a workstream.
    repo = _first_approval_repo(tmp_path)
    req = repo / "docs" / "requirements"
    # Two other lanes' rows, both `Drafted` on released rungs, neither in this
    # act's scope. LLR-003 sits in the SAME chain this act must render (so the
    # brief has to label it, not hide it); SR-002's chain is entirely somebody
    # else's (so the brief must not render it at all).
    llrs = req / "low-level-requirements.csv"
    llrs.write_text(
        llrs.read_text(encoding="utf-8")
        + "LLR-003,SR-001,carry impl,src/demo.py,carry,carry() handles overflow.,,"
        "Drafted,,P1\n"
        + "LLR-002,SR-002,sub impl,src/demo.py,sub,sub() returns a - b.,,Drafted,,P1\n",
        encoding="utf-8",
    )
    srs = req / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8")
        + "SR-002,Subtracts,SN-001,The system shall subtract.,arithmetic,the "
        "difference is right,Must,Test,Drafted,P1,core\n",
        encoding="utf-8",
    )

    values, why = ab.first_approval_values(repo, _fa_row())
    assert why is None, why
    chain = values["chain"]
    # The scoped row is still the question, and it is the ONLY one.
    assert "LLR-001 [AWAITING FIRST APPROVAL]\n" in chain + "\n"
    assert chain.count("[AWAITING FIRST APPROVAL]") == 1, chain
    # The sibling in the same chain is SHOWN — it is evidence — and labelled with
    # the reason that is actually true of it. Saying "HELD FOR THE OWNER" here
    # would tell the session to wait on a signature nobody owes.
    assert "LLR-003 [AWAITING FIRST APPROVAL - OUTSIDE THIS ACT'S SCOPE" in chain
    # The unrelated chain is dropped WHOLE: it is not this act's question and it
    # is not this act's evidence either.
    for rid in ("SR-002", "LLR-002"):
        assert rid not in chain, chain
    # And the act's RECORDED scope carries only the scoped row's registry — the
    # half a session that ignored every word of the prose still cannot widen.
    assert (
        values["registries"] == "docs/requirements/low-level-requirements.toml=WI-301"
    )


def test_an_adjudication_with_no_declared_scope_is_REFUSED_not_widened(tmp_path):
    # The unstated boundary. An empty `Adjudicates` cell cannot be read as
    # "every `Drafted` row in the repo" — that IS the widening — so it fails
    # toward the human (rule 3) and the reason names the cell.
    repo = _first_approval_repo(tmp_path)
    values, why = ab.first_approval_values(repo, _fa_row(Adjudicates=""))
    assert values is None
    assert "declares no `Adjudicates` scope" in why, why
    # ...and the caller HOLDS it rather than composing a partial brief.
    text, why = ab.compose(repo, _fa_row(Adjudicates=""), repo / "docs/reviews/v.md")
    assert text is None and "Adjudicates" in why


def test_a_scope_whose_rows_are_all_settled_REFUSES_by_naming_them(tmp_path):
    # The second-order harm of the widening: merge B's adjudication, minted
    # while merge A's was still queued, used to find "no spine row awaits a
    # first approval any more" — one repo-wide sentence for three different
    # states. The refusal now names WHICH filter emptied the population, because
    # "ruled on already" (drop the row), "the owner holds the rung" (sign it)
    # and "the scope names rows this spine no longer has" (the mint and the tree
    # disagree) take three different actions.
    repo = _first_approval_repo(tmp_path)
    values, why = ab.first_approval_values(repo, _fa_row(Adjudicates="LLR-404"))
    assert values is None
    assert "LLR-404" in why, why
    assert "no longer has a subject" in why, why


def test_the_first_approval_brief_is_ROUTED_and_demands_its_own_verdict(tmp_path):
    # The seam, both halves. The brief has an assembler (so a row declaring it
    # is DISPATCHED, not held for a human), and its verdict grammar is its own:
    # the amendment arm's MEANING/CLARITY cannot answer "approve or return", and
    # a checker still expecting the old enum is exactly the drift the table
    # prevents.
    assert "first-approval" in ab.ROUTED
    assert ab.VERDICT_GRAMMAR["first-approval"] == (
        "OUTCOME",
        ("APPROVE", "RETURN"),
        ("rows",),
    )
    verdict = tmp_path / "v.md"
    verdict.write_text("OUTCOME: MEANING rows=1\n", encoding="utf-8")
    assert "not one of APPROVE|RETURN" in ab.verdict_refusal("first-approval", verdict)
    verdict.write_text("OUTCOME: APPROVE rows=2\n", encoding="utf-8")
    assert ab.verdict_refusal("first-approval", verdict) is None


def test_an_adjudication_row_declaring_no_brief_still_builds(tmp_path):
    """The complement, and the reason the hold keys on the DECLARATION rather
    than on `adjudicating()`: a clean-close spot check and a report-less
    cancellation are adjudication classes the kit has never authored a brief
    for. Holding those would page a human for routine work, and their empty
    `brief` cell is an honest statement rather than an unhonoured claim."""
    repo = _disposition_repo(tmp_path, with_report=False)
    spec = next((repo / "docs" / "work").rglob("WI-301-*.md"))
    spec.write_text(
        spec.read_text(encoding="utf-8").replace('brief = "disposition"\n', ""),
        encoding="utf-8",
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "registry")
    proc, prompts = _session(tmp_path, repo, "WI-301", "unused")
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert "INDEPENDENT adjudicator" not in prompts
    assert "- WI: WI-301 —" in prompts


# --- the ADJUDICATE validation arm (the verdict is the deliverable) -----------


@pytest.mark.parametrize(
    "brief,line",
    [
        ("disposition", "OUTCOME: PARTIAL successors=1"),
        ("red-tc", "OUTCOME: DRAFTED cases=2 drafts=1"),
        ("amendment", "VERDICT: MEANING rows=3"),
        ("consolidate", "OUTCOME: QUEUE-WITH-EDGE needs=WI-009 absorbs=-"),
        ("consolidate", "OUTCOME: CONSOLIDATE needs=- absorbs=WI-1;WI-2"),
    ],
)
def test_a_well_formed_typed_line_is_accepted_for_every_brief(tmp_path, brief, line):
    """The grammar lives beside the assemblers because the brief and the verdict
    it demands are ONE contract — a template whose enum moved and a checker that
    did not is the drift this table prevents. All four briefs are covered,
    including the one with no assembler: an unrouted brief still has a verdict
    shape. `consolidate` appears twice because both of its counters are
    required on EVERY alternative, not only on the one that uses them."""
    path = tmp_path / "v.md"
    path.write_text("- [MINOR] a finding -> why -> the change\n" + line + "\n")
    assert ab.verdict_refusal(brief, path) is None


@pytest.mark.parametrize(
    "line,expect",
    [
        (None, "no verdict was written"),
        ("the lane did fine, I think", "no `OUTCOME:` machine line"),
        ("OUTCOME: LOOKS-OK successors=1", "not one of"),
        ("OUTCOME: PARTIAL", "omits successors"),
    ],
)
def test_an_unusable_verdict_is_refused_and_says_which_way(tmp_path, line, expect):
    """Four ways to fail, four distinct reasons. "The verdict is invalid" is not
    something a human can act on at 3am, so each arm names what is wrong."""
    path = tmp_path / "v.md"
    if line is not None:
        path.write_text(line + "\n")
    why = ab.verdict_refusal("disposition", path)
    assert why and expect in why


def test_the_review_scorer_cannot_serve_this_grammar():
    """Why the table exists rather than reusing `score_reviews.parse_verdict`:
    that parser knows only the REVIEW vocabulary, so three of the four
    adjudicator lines (which say `OUTCOME:`) and the fourth (which says
    `VERDICT: MEANING`) would all read as unparseable — and an unparseable
    verdict is treated as no verdict."""
    scorer = load_script("score_reviews")
    parsed = scorer.parse_verdict("OUTCOME: PARTIAL successors=1\n")
    assert parsed.verdict is None


def test_a_judge_that_commits_without_ruling_does_not_complete(tmp_path):
    """M5, end to end. The session commits the `WI:` trailer that makes a WORKER
    done — and stays incomplete, because an adjudication's deliverable is the
    verdict artifact, not the commit. Without this arm the loop reported a
    ruling that was never made."""
    repo = _disposition_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "registry + report")
    proc, prompts = _session(tmp_path, repo, "WI-301", "NONE")
    assert "INDEPENDENT adjudicator" in prompts, "the brief was not even sent"
    assert proc.returncode != agent_loop.EXIT_DONE, proc.stdout
    assert "not complete — no verdict was written" in proc.stdout
    # The trailer IS there — which is exactly why the trailer alone is not the bar.
    assert "WI-301" in _git(repo, "log", "--format=%(trailers:key=WI,valueonly)")


def test_a_malformed_outcome_line_does_not_complete(tmp_path):
    """The other half: the artifact exists, so a presence check would pass, but
    its machine line is outside the closed enum. A prose verdict is not a typed
    one — the whole reason these briefs end in a closed enum."""
    repo = _disposition_repo(tmp_path)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "registry + report")
    proc, _prompts = _session(tmp_path, repo, "WI-301", "OUTCOME: PROBABLY-FINE")
    assert proc.returncode != agent_loop.EXIT_DONE, proc.stdout
    assert "not complete" in proc.stdout and "not one of" in proc.stdout


# --- the consolidation brief (the 2026-09-02 restructure plan §1.4) -----------


def _consolidate_repo(tmp_path, extra=(), digests=None, scope="WI-401;WI-402"):
    """A repo whose queue holds an overlapping pair and the `consolidate` row an
    idle-station census minted over it."""
    consolidate = load_script("consolidate")
    repo = _repo(tmp_path)
    req = repo / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(SPINE_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(SPINE_LLRS, encoding="utf-8")
    (repo / "docs" / "test").mkdir(parents=True)
    (repo / "docs" / "test" / "test-cases.csv").write_text(SPINE_TCS, encoding="utf-8")
    rows = [
        {
            "WI-ID": "WI-401",
            "Title": "harden the adder",
            "SR-Refs": "SR-001",
            "SpecRef": "docs/plans/adder.md",
        },
        {
            "WI-ID": "WI-402",
            "Title": "rewrite the adder tests",
            "SR-Refs": "SR-001",
            "SpecRef": "docs/plans/adder.md",
        },
        {"WI-ID": "WI-410", "Title": "something unrelated"},
    ] + list(extra)
    _write_rows(repo, rows)
    live = consolidate.read_rows(repo)
    cell = consolidate.digests(repo, live) if digests is None else digests
    _write_rows(
        repo,
        [
            {
                "WI-ID": "WI-420",
                "Title": "adjudicate queue overlap",
                "SafetyClass": "adjudication",
                "Brief": "consolidate",
                "SpecRef": "docs/work/README.md",
                "Adjudicates": scope,
                "Digests": cell,
                "Priority": "9",
            }
        ],
    )
    return repo, {
        r["WI-ID"]: r
        for r in load_script("agent_common").read_spec_rows(repo / "docs" / "work")
    }


def test_the_consolidate_brief_composes_every_slot_from_the_registry(tmp_path):
    repo, rows = _consolidate_repo(tmp_path)
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert why is None, why
    assert set(values) == {
        "candidate",
        "open_rows",
        "spine",
        "mechanical",
        "digests",
        "prior",
    }
    # The cluster is rendered WHOLE — the verdict quotes each absorbed row's
    # Done-when into the successor verbatim, and a judge shown a summary
    # paraphrases.
    assert "=== WI-401" in values["candidate"] and "=== WI-402" in values["candidate"]
    # ...and the rows that are NOT the cluster are the other evidence, once.
    assert "- WI-410" in values["open_rows"]
    assert "WI-401" not in values["open_rows"]
    # The spine the cluster cites, at both tiers.
    assert "SR-001" in values["spine"] and "LLR-001" in values["spine"]
    assert "shall add two numbers" in values["spine"]
    # The pre-filter's findings, re-derived live rather than replayed.
    assert "share one spec of record" in values["mechanical"]
    # BOTH digest pairs: a recorded pair alone is a number with nothing to
    # compare against, and the slot exists to make staleness detectable.
    assert "recorded at the mint" in values["digests"]
    assert "as the tree is now" in values["digests"]
    assert values["prior"] == ab.NO_PRIOR
    text, why = ab.compose(repo, rows["WI-420"], repo / "docs/reviews/v.md")
    assert why is None, why
    assert "INDEPENDENT adjudicator" in text and "CONSOLIDATE" in text
    assert "consolidate" in ab.ROUTED


def test_a_cluster_citing_no_spine_still_composes_with_the_literal(tmp_path):
    """Plan §1.4: `{spine}` is then the literal, STATED and never blank —
    contradiction with the spine is one of three questions and the other two
    remain, so this composes rather than refusing."""
    repo, rows = _consolidate_repo(
        tmp_path,
        extra=[
            {"WI-ID": "WI-403", "Title": "one plan row", "SpecRef": "docs/plans/x.md"},
            {
                "WI-ID": "WI-404",
                "Title": "other plan row",
                "SpecRef": "docs/plans/x.md",
            },
        ],
        scope="WI-403;WI-404",
    )
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert why is None, why
    assert values["spine"] == ab.NO_SPINE
    assert "share one spec of record" in values["mechanical"]


def test_a_consolidation_declaring_no_scope_refuses(tmp_path):
    """An unstated boundary read as "every queued row" would let one verdict
    absorb the whole backlog — the same widening `Adjudicates` closed for the
    first-approval brief."""
    repo, rows = _consolidate_repo(tmp_path, scope="")
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert values is None and "declares no `Adjudicates` scope" in why


def test_a_consolidation_with_no_digests_cell_refuses(tmp_path):
    """Without the pair, the verdict cannot be told stale from fresh and the
    census cannot tell that this queue state has been judged — so the row is
    HELD for a human rather than briefed."""
    repo, rows = _consolidate_repo(tmp_path, digests="")
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert values is None and "no usable `Digests` cell" in why


def test_a_cluster_row_that_left_the_queue_refuses_by_name(tmp_path):
    """EVERY row of the cluster or none. A consolidation ABSORBS the rows it is
    shown, so a brief over the survivors produces a verdict whose `supersedes`
    silently omits one — which the close cannot detect, because the absent row
    is absent from the verdict too."""
    repo, rows = _consolidate_repo(tmp_path)
    spec = repo / "docs" / "work" / "queued" / "WI-402-rewrite-the-adder-tests.md"
    assert spec.is_file(), sorted(p.name for p in spec.parent.iterdir())
    spec.unlink()
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert values is None and "WI-402" in why and "no longer queued" in why


def test_a_cluster_whose_overlap_dissolved_refuses_rather_than_briefing(tmp_path):
    """`red_tc_values`' rule, one brief over: the census is RE-RUN at
    composition time, so a judge rules on the state of the world it is actually
    in. A cluster whose overlap is gone would otherwise brief a session about a
    contradiction that no longer exists."""
    repo, rows = _consolidate_repo(tmp_path)
    work = repo / "docs" / "work" / "queued"
    for name, spec_line in (
        ("WI-401-harden-the-adder.md", 'specref = "docs/plans/one.md"'),
        ("WI-402-rewrite-the-adder-tests.md", 'specref = "docs/plans/two.md"'),
    ):
        path = work / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^specref = .*$", spec_line, text)
        text = re.sub(r"(?m)^sr_refs = .*$", "sr_refs = []", text)
        path.write_text(text, encoding="utf-8")
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert values is None and "dissolved" in why


def test_prior_names_what_earlier_consolidations_absorbed(tmp_path):
    """`{prior}` is read from the REGISTRY — the absorbed rows' own status and
    lineage — and never from a verdict file: rule 1, a judge's evidence is a
    record and not a claim."""
    repo, rows = _consolidate_repo(
        tmp_path,
        extra=[
            {
                "WI-ID": "WI-390",
                "Title": "absorbed a",
                "Status": "restructured",
                "Supersedes": "WI-395",
            },
            {
                "WI-ID": "WI-391",
                "Title": "absorbed b",
                "Status": "restructured",
                "Supersedes": "WI-395",
            },
            {
                "WI-ID": "WI-395",
                "Title": "the successor",
                "Supersedes": "WI-390;WI-391",
            },
        ],
    )
    values, why = ab.consolidate_values(repo, rows["WI-420"])
    assert why is None, why
    assert values["prior"] == "- WI-395 absorbed WI-390;WI-391"
