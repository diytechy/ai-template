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
import subprocess
import sys

import pytest
from conftest import env_gate_skipif, load_script, pin_autocrlf, run_py, SCRIPTS

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


def test_the_one_unrouted_brief_refuses_and_names_itself(tmp_path):
    """`conflict` is left unrouted on purpose (see adjudicate_brief.py's
    header): nothing mints a queue-conflict row at all, and its `{digests}` slot
    names a pair no function computes. Wiring it would mean filling a slot with
    something, which is the failure this whole module is shaped around.

    `amendment` was the second one until D-9 step 4b — see the tests below,
    which are its positive successors."""
    repo = _repo(tmp_path)
    text, why = ab.compose(repo, {"WI-ID": "WI-9", "Brief": "conflict"}, repo / "v.md")
    assert text is None
    assert "conflict" in why and "no evidence assembler" in why
    assert "conflict" not in ab.ROUTED


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
    would page a human for routine work."""
    source = (intake.__file__ or "").strip()
    assert source
    with open(source, encoding="utf-8") as handle:
        text = handle.read()
    declared = set(re.findall(r'"brief":\s*"([^"]*)"', text))
    assert declared, "no brief declarations found — guard vacuous"
    assert declared <= set(ab.BRIEF_PROMPTS), sorted(declared - set(ab.BRIEF_PROMPTS))
    # The two the kit can actually serve must still be declared somewhere, or
    # the routed briefs would have no producer of rows at all.
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
    """Move SR-001's `Requirement` — a RATIFIED cell — leaving its Status put.
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
    """A repo with a spine, an approved snapshot, an amended ratified cell, and
    the adjudication row `intake` would have minted for it."""
    repo = _spine_repo(tmp_path)
    baseline_snapshot.copy_live(repo, seed=True)
    _amend(repo)
    _write_rows(
        repo,
        [
            {
                "WI-ID": "WI-301",
                "Title": "adjudicate: SR-001 - ratified cell(s) amended",
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


def test_only_RATIFIED_cells_reach_the_judge(tmp_path):
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
        ("conflict", "OUTCOME: QUEUE-WITH-EDGE needs=WI-009"),
    ],
)
def test_a_well_formed_typed_line_is_accepted_for_every_brief(tmp_path, brief, line):
    """The grammar lives beside the assemblers because the brief and the verdict
    it demands are ONE contract — a template whose enum moved and a checker that
    did not is the drift this table prevents. All four are covered, including
    the two with no assembler: an unrouted brief still has a verdict shape."""
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
