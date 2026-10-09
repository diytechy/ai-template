"""plan_coverage.py — the dual-plan coverage pre-pass (WI-190).

Exercises the commensurability contract end-to-end the way a dispatcher would:
a goal brief with C# clauses, two rival plan tables, the optional SR/IF
registries — asserting the computed coverage diff, the findings (unknown refs,
rationale-less Proposed seams, cycles), and the honest degradation when a
registry is absent.
"""

from pathlib import Path

from conftest import ROOT, SCRIPTS, run_py

SCRIPT = SCRIPTS / "plan_coverage.py"

GOAL = """# Goal brief

- C1: the dispatcher launches two planner sessions.
- C2: briefs are redacted by construction.
- **C3**: the verdict file records ports.
- C4: budgets bound every session.
"""

PLAN_A = """## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Launch planner sessions | C1 | IF-001 | |
| P2 | Redacted brief builder | C2; SR-001 | intra-module | P1 |

## Notes
- C3, C4 excluded: out of scope for the pilot.
"""

PLAN_B = """| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| Q1 | Session launcher | C1 | IF-001 | |
| Q2 | Verdict writer | C3 | Proposed: nearest is IF-001, wrong direction - a new Provides row is needed | Q1 |
"""

# WI-803 (dispute-1 ruling (a)): an unexplained DUAL gap fails the gate, so a
# test whose purpose is not gaps runs on these gated variants; the originals
# above stay byte-identical as the pre-gate fixtures.
PLAN_A_GATED = PLAN_A + "\nExcludes: C3; C4 — out of scope for the pilot.\n"
PLAN_B_GATED = PLAN_B + "\nExcludes: C2; C4 — another plan's scope.\n"
GATED = (PLAN_A_GATED, PLAN_B_GATED)

IFS = (
    "[interface.IF-001]\n"
    'owner = "scripts/a"\n'
    'consumers = ["scripts/b"]\n'
    'channel = "call"\n'
    'version = "v1"\n'
    'status = "Approved"\n'
)
SRS = "SR-ID,Title,Requirement\nSR-001,One,shall\n"


def write_inputs(tmp_path, goal=GOAL, plans=(PLAN_A, PLAN_B), registries=True):
    (tmp_path / "goal.md").write_text(goal, encoding="utf-8")
    names = []
    for i, text in enumerate(plans):
        name = "plan-{}.md".format("AB"[i] if i < 2 else i)
        (tmp_path / name).write_text(text, encoding="utf-8")
        names.append(name)
    if registries:
        req = tmp_path / "docs" / "requirements"
        req.mkdir(parents=True)
        (req / "interfaces.toml").write_text(IFS, encoding="utf-8")
        (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    return names


def run(tmp_path, names, extra=()):
    return run_py(
        [SCRIPT, "--goal", tmp_path / "goal.md", "--root", tmp_path]
        + [tmp_path / n for n in names]
        + list(extra),
        cwd=tmp_path,
    )


def test_two_plans_green_with_coverage_diff(tmp_path):
    names = write_inputs(tmp_path, plans=GATED)
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "only plan-A.md: C2" in out
    assert "only plan-B.md: C3" in out
    assert "both: C1" in out
    assert "neither: C4" in out
    assert "plan_coverage: OK" in out


def test_out_writes_the_report_file(tmp_path):
    names = write_inputs(tmp_path, plans=GATED)
    proc = run(tmp_path, names, extra=["--out", tmp_path / "coverage.md"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (tmp_path / "coverage.md").read_text(encoding="utf-8")
    assert "# Plan coverage report" in report
    assert "## Coverage diff: plan-A.md vs plan-B.md" in report


def test_unknown_clause_and_sr_refs_fail(tmp_path):
    bad = PLAN_A.replace("C2; SR-001", "C9; SR-999")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "cites undeclared clause C9" in proc.stdout
    assert "cites unknown SR-999" in proc.stdout


def test_unresolvable_if_and_rationale_less_proposed_fail(tmp_path):
    bad = PLAN_B.replace(
        "Proposed: nearest is IF-001, wrong direction - a new Provides row is needed",
        "Proposed:",
    ).replace("IF-001", "IF-042")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "IF-042 which resolves to no interfaces.toml row" in proc.stdout
    assert "proposes a seam with no rationale" in proc.stdout


def test_empty_interfaces_cell_without_escape_fails(tmp_path):
    bad = PLAN_A.replace("intra-module", "")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "states no intra-module escape" in proc.stdout


def test_predecessor_cycle_and_unknown_pred_fail(tmp_path):
    bad = PLAN_A.replace(
        "| P1 | Launch planner sessions | C1 | IF-001 | |",
        "| P1 | Launch planner sessions | C1 | IF-001 | P2 |",
    )
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "predecessor cycle" in proc.stdout


def test_unknown_predecessor_fails(tmp_path):
    bad = PLAN_B.replace("| Q1 |\n", "| Q9 |\n")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "names unknown predecessor Q9" in proc.stdout


def test_duplicate_plan_wi_id_fails(tmp_path):
    bad = PLAN_A.replace("| P2 |", "| P1 |")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "duplicate Plan-WI id P1" in proc.stdout


def test_absent_registries_degrade_to_notes_not_findings(tmp_path):
    names = write_inputs(tmp_path, plans=GATED, registries=False)
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no system-requirements.csv; SR refs unvalidated" in proc.stdout
    assert "no interfaces.toml; IF refs unvalidated" in proc.stdout


def test_goal_without_clauses_is_a_malformed_input(tmp_path):
    names = write_inputs(tmp_path, goal="# just prose\n")
    proc = run(tmp_path, names)
    assert proc.returncode == 2
    assert "declares no clauses" in proc.stdout


def test_plan_without_table_is_a_malformed_input(tmp_path):
    names = write_inputs(tmp_path, plans=("no table here\n",))
    proc = run(tmp_path, names)
    assert proc.returncode == 2
    assert "has no Plan-WI table" in proc.stdout


def test_multi_covered_clause_is_reported_not_failed(tmp_path):
    plan = PLAN_A_GATED.replace("C2; SR-001", "C1; C2").replace(
        "Excludes: C3; C4", "Excludes: C2; C3; C4"
    )
    names = write_inputs(tmp_path, plans=(plan,))
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "multi-covered: C1 (P1, P2)" in proc.stdout


# --- WI-803: the SINGLE plan gate (Done-when D#, findings F#, Excludes:, the
# SR/TC diff, the optional Tier column). The item is a claimed spec; its
# Done-when items are the D# clauses (kitlib.done_when.items, never re-parsed).

ITEM = """+++
id = "WI-001"
title = "Two planner sessions"
sr_refs = ["SR-001"]
+++

## Done-when

- The dispatcher launches two planner sessions.
- Briefs are redacted by construction.
- The verdict file records ports.
"""

SINGLE_PLAN = """## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors | Tier |
|---|---|---|---|---|---|
| S1 | Launch planner sessions | D1; SR-001; TC-001 | IF-001 | | medium |
| S2 | Redacted brief builder | D2; TC-002 | intra-module | S1 | quick |

Excludes: D3 — the verdict writer lands with the dual pickup row.
"""

TCS = (
    "[test.TC-001]\n"
    'verifies = ["SR-001"]\n'
    'status = "Approved"\n'
    "\n"
    "[test.TC-002]\n"
    'verifies = ["SR-001"]\n'
    'status = "Approved"\n'
)

FINDINGS = """# Open review findings

- F1: the launcher ignores the session budget.
"""


def write_single(tmp_path, plan=SINGLE_PLAN, item=ITEM, findings=None, tcs=None):
    tmp_path.mkdir(parents=True, exist_ok=True)
    write_inputs(tmp_path, plans=(plan,))
    (tmp_path / "item.md").write_text(item, encoding="utf-8")
    tests = tmp_path / "docs" / "test"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "test-cases.toml").write_text(tcs or TCS, encoding="utf-8")
    extra = []
    if findings is not None:
        (tmp_path / "findings.md").write_text(findings, encoding="utf-8")
        extra = ["--findings", tmp_path / "findings.md"]
    return run_py(
        [SCRIPT, "--item", tmp_path / "item.md", "--root", tmp_path]
        + extra
        + [tmp_path / "plan-A.md", "--out", tmp_path / "coverage.md"],
        cwd=tmp_path,
    )


def test_single_plan_covering_or_excluding_every_clause_passes(tmp_path):
    """An excluded clause with a reason passes; a Tier column is allowed."""
    proc = write_single(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Goal: item.md - 3 clause(s): D1 D2 D3" in proc.stdout
    assert "- excluded: D3 - the verdict writer lands" in proc.stdout
    assert "plan_coverage: OK" in proc.stdout
    report = (tmp_path / "coverage.md").read_text(encoding="utf-8")
    assert "## SR/TC diff: plan-A.md" in report


def test_single_plan_missing_a_done_when_item_exits_1_naming_it(tmp_path):
    plan = SINGLE_PLAN.replace(
        "Excludes: D3 — the verdict writer lands with the dual pickup row.\n", ""
    )
    proc = write_single(tmp_path, plan=plan)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "plan_coverage: FAIL - plan-A.md: D3 is neither covered by a row nor "
        "excluded with a reason: 'The verdict file records ports.'"
    ) in proc.stdout


def test_an_exclusion_without_a_reason_is_a_finding(tmp_path):
    plan = SINGLE_PLAN.replace(
        "Excludes: D3 — the verdict writer lands with the dual pickup row.",
        "Excludes: D3",
    )
    proc = write_single(tmp_path, plan=plan)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "plan-A.md: Excludes: D3 gives no reason" in proc.stdout
    assert "D3 is neither covered by a row nor excluded" in proc.stdout


def test_an_exclusion_of_an_undeclared_clause_is_a_finding(tmp_path):
    plan = SINGLE_PLAN.replace("Excludes: D3 —", "Excludes: D3; D7 —")
    proc = write_single(tmp_path, plan=plan)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "plan-A.md: Excludes: names undeclared clause D7" in proc.stdout


def test_single_sr_tc_diff_names_an_uncovered_sr_and_an_unnamed_tc(tmp_path):
    plan = SINGLE_PLAN.replace("D1; SR-001; TC-001", "D1").replace("D2; TC-002", "D2")
    proc = write_single(tmp_path, plan=plan)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    out = proc.stdout
    assert (
        "plan-A.md: the item's SR-001 is cited by no row "
        "(an item SR cannot be excluded)"
    ) in out
    assert (
        "plan-A.md: TC-001 verifies SR-001 and is named by no row nor excluded"
    ) in out
    assert "TC-002 verifies SR-001 and is named by no row nor excluded" in out


def test_single_tc_excluded_with_a_reason_passes(tmp_path):
    plan = SINGLE_PLAN.replace("D2; TC-002", "D2") + (
        "Excludes: TC-002 — its fixture is unchanged by this item.\n"
    )
    proc = write_single(tmp_path, plan=plan)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_open_review_findings_are_clauses_on_a_replan(tmp_path):
    proc = write_single(tmp_path, findings=FINDINGS)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "plan-A.md: F1 is neither covered by a row nor excluded with a reason"
    ) in proc.stdout
    covered = SINGLE_PLAN.replace("D1; SR-001; TC-001", "D1; F1; SR-001; TC-001")
    proc = write_single(tmp_path / "again", plan=covered, findings=FINDINGS)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_an_item_without_done_when_is_a_malformed_input(tmp_path):
    item = ITEM.split("## Done-when")[0]
    proc = write_single(tmp_path, item=item)
    assert proc.returncode == 2
    assert "declares no Done-when items" in proc.stdout


DUAL_REPORT = """# Plan coverage report

Goal: goal.md - 4 clause(s): C1 C2 C3 C4

## plan-A.md

- rows: 2
- covers: C1 C2 (2/4)
- uncovered: C3 C4

## plan-B.md

- rows: 2
- covers: C1 C3 (2/4)
- uncovered: C2 C4

## Coverage diff: plan-A.md vs plan-B.md

- only plan-A.md: C2
- only plan-B.md: C3
- both: C1
- neither: C4
"""


DUAL_GAP_FAILS = (
    "plan_coverage: FAIL - plan-A.md: C3 is neither covered by a row nor "
    "excluded with a reason: 'the verdict file records ports.'\n"
    "plan_coverage: FAIL - plan-A.md: C4 is neither covered by a row nor "
    "excluded with a reason: 'budgets bound every session.'\n"
    "plan_coverage: FAIL - plan-B.md: C2 is neither covered by a row nor "
    "excluded with a reason: 'briefs are redacted by construction.'\n"
    "plan_coverage: FAIL - plan-B.md: C4 is neither covered by a row nor "
    "excluded with a reason: 'budgets bound every session.'\n"
)


def test_dual_report_bytes_unchanged_and_unexplained_dual_gaps_fail(tmp_path):
    """WI-803, dispute-1 ruling (a): over the pre-gate DUAL fixture the
    `--out` report is byte-identical to the one the pre-gate script wrote, and
    each unexplained C# gap is now a finding. PLAN_A's prose "C3, C4 excluded"
    note is not an `Excludes:` line, so it explains nothing."""
    names = write_inputs(tmp_path)
    proc = run(tmp_path, names, extra=["--out", tmp_path / "coverage.md"])
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (tmp_path / "coverage.md").read_bytes() == DUAL_REPORT.encode("utf-8")
    stdout = proc.stdout.replace("\r\n", "\n")
    assert stdout == DUAL_REPORT + "\n" + DUAL_GAP_FAILS


def test_a_dual_gap_excluded_with_a_reason_passes(tmp_path):
    """The DP-001 case: a rival plan declares what it leaves out, with why."""
    names = write_inputs(tmp_path, plans=GATED)
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "- excluded: C3 - out of scope for the pilot." in proc.stdout


def test_a_dual_gap_fails_naming_only_its_plan(tmp_path):
    names = write_inputs(tmp_path, plans=(PLAN_A_GATED, PLAN_B))
    proc = run(tmp_path, names)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    gaps = [ln for ln in proc.stdout.splitlines() if "is neither covered" in ln]
    assert len(gaps) == 2, proc.stdout
    assert all(ln.startswith("plan_coverage: FAIL - plan-B.md: ") for ln in gaps)


def test_an_item_sr_cannot_be_excluded_only_cited(tmp_path):
    """ch.3 §4.5: every item SR is cited by a row; only a TC may be excluded."""
    plan = SINGLE_PLAN.replace("D1; SR-001; TC-001", "D1; TC-001") + (
        "Excludes: SR-001 — deferred to another item.\n"
    )
    proc = write_single(tmp_path, plan=plan)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "plan-A.md: the item's SR-001 is cited by no row "
        "(an item SR cannot be excluded)"
    ) in proc.stdout
    assert "- SR-001: missing" in proc.stdout


def test_a_bold_exclusion_label_is_an_exclusion(tmp_path):
    """`**Excludes:** C# — why` reads like `Excludes:` (the closing marker is
    consumed, not read as a ref)."""
    plan = PLAN_A.replace("C2; SR-001", "C1") + (
        "**Excludes:** C2; C3; C4 — deliberately deferred.\n"
    )
    names = write_inputs(tmp_path, plans=(plan,))
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "- excluded: C2 - deliberately deferred." in proc.stdout


def test_a_tc_verifying_only_a_non_item_sr_stays_out_of_the_single_diff(tmp_path):
    """The SR/TC diff asks only for the TCs that verify one of the item's own
    SRs; a TC on another SR is not this plan's to name or exclude."""
    other = TCS + '\n[test.TC-003]\nverifies = ["SR-002"]\nstatus = "Approved"\n'
    proc = write_single(tmp_path, tcs=other)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "TC-003" not in proc.stdout
    assert "- TC-002 (verifies SR-001): cited" in proc.stdout


def test_a_row_citing_nothing_is_a_finding(tmp_path):
    """The commensurability contract: every row says what it covers."""
    plan = PLAN_A_GATED.replace("| C2; SR-001 |", "| |").replace(
        "Excludes: C3; C4", "Excludes: C2; C3; C4"
    )
    names = write_inputs(tmp_path, plans=(plan,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "plan-A.md: P2 cites no clause/SR" in proc.stdout


# --- WI-853: a review verdict's findings are the F# clauses a rework plan must
# cover before the fix is dispatched. One shared step (`finding_clauses`) turns
# the verdict's finding lines into those clauses, for the coordinator's attended
# rework round (and, once WI-805 wires it, the loop's replan); a finding an
# adjudicator dismissed in a dispute sitting counts when the plan cites that
# ruling and the findings file beside it shows the ruled finding is this one.

REVIEW = """- [MAJOR] scripts/launch.py:10 -> the launcher ignores the session budget -> enforce it -> @owner
- [MINOR] docs/brief.md:3 -> stale wording -> reword it -> @owner
VERDICT: CHANGES-REQUESTED findings=2
"""

REWORK_PLAN = SINGLE_PLAN.replace("D1; SR-001; TC-001", "D1; F1; SR-001; TC-001")
DISPUTE_VERDICT = "docs/reviews/wi-001/003-ADJUDICATE-abc1234.md"


# Each REVIEW finding exactly as the reviewer wrote it, as a dispute sitting's
# findings file records it.
LAUNCHER = REVIEW.splitlines()[0]
WORDING = REVIEW.splitlines()[1]


def findings_toml(findings, name="002-DISPUTE-findings.toml"):
    """`(name, text)` of a dispute findings file ruling `findings`, an ordered
    {id: the finding as the reviewer wrote it}."""
    tables = "".join(
        '\n[[finding]]\nid = "{}"\nheld_by = "builder"\n'
        "finding = '''\n{}\n'''\nposition = '''\nContested.\n'''\n".format(fid, text)
        for fid, text in findings.items()
    )
    return name, 'range = "aaaaaaa..bbbbbbb"\n' + tables


def write_dispute(root, ruling, outcome="accepted", kinds="F2", findings=()):
    """A recorded dispute verdict and its binding, as the coordinator's
    adjudication entry point leaves them, beside the findings files
    (`findings_toml`) the sitting ruled."""
    verdict = root / DISPUTE_VERDICT
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text("Judged.\n\n{}\n".format(ruling), encoding="utf-8")
    Path(str(verdict) + ".requested").write_text(
        "brief = dispute\nkinds = {}\noutcome = {}\n".format(kinds, outcome),
        encoding="utf-8",
    )
    for name, text in findings:
        (verdict.parent / name).write_text(text, encoding="utf-8")


def test_the_shared_step_turns_a_real_verdict_into_F_clauses():
    """A real REVIEW-A verdict's finding lines become F1..Fn, in order, each
    carrying the finding as written."""
    import plan_coverage

    text = (ROOT / "docs" / "reviews" / "054-REVIEW-A.md").read_text(encoding="utf-8")
    clauses = plan_coverage.finding_clauses(text)
    assert list(clauses) == ["F1", "F2", "F3", "F4"]
    assert clauses["F1"].startswith("[MAJOR] docs/next-wi:23 -> selects WI-110")
    assert clauses["F4"].startswith("[MINOR] docs/status.md:46 -> adds a 12-line")
    assert plan_coverage.finding_clauses(FINDINGS) == {
        "F1": "the launcher ignores the session budget."
    }


def test_a_findings_file_mixing_both_shapes_is_malformed(tmp_path):
    proc = write_single(tmp_path, plan=REWORK_PLAN, findings=FINDINGS + REVIEW)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "both" in proc.stdout


def test_an_uncovered_review_finding_refuses_the_dispatch(tmp_path):
    proc = write_single(tmp_path, plan=REWORK_PLAN, findings=REVIEW)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "plan-A.md: F2 is neither covered by a row nor excluded with a reason: "
        "'[MINOR] docs/brief.md:3 -> stale wording -> reword it -> @owner'"
    ) in proc.stdout
    assert "F1 is neither" not in proc.stdout


def test_covered_or_excluded_review_findings_pass(tmp_path):
    covered = REWORK_PLAN.replace("D2; TC-002", "D2; F2; TC-002")
    proc = write_single(tmp_path, plan=covered, findings=REVIEW)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    excluded = REWORK_PLAN + "Excludes: F2 — the wording is WI-999's rewrite.\n"
    proc = write_single(tmp_path / "x", plan=excluded, findings=REVIEW)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "- excluded: F2 - the wording is WI-999's rewrite." in proc.stdout


def test_a_dismissed_dispute_citing_its_ruling_passes(tmp_path):
    write_dispute(
        tmp_path,
        "RULING: F2 DISMISS refuted the wording matches",
        findings=[findings_toml({"F2": WORDING})],
    )
    plan = REWORK_PLAN + "Excludes: F2 — dismissed by {}\n".format(DISPUTE_VERDICT)
    proc = write_single(tmp_path, plan=plan, findings=REVIEW)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_dispute_ruling_cited_by_its_own_id_passes(tmp_path):
    """A dispute sitting may name the finding by its own id: `<verdict>#<id>`."""
    write_dispute(
        tmp_path,
        "RULING: B DISMISS out-of-scope contrived",
        kinds="B",
        findings=[findings_toml({"B": WORDING})],
    )
    plan = REWORK_PLAN + "Excludes: F2 — dismissed: {}#B\n".format(DISPUTE_VERDICT)
    proc = write_single(tmp_path, plan=plan, findings=REVIEW)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_ruling_of_the_same_finding_passes_through_typographic_drift(tmp_path):
    """The sitting's copy of the finding may differ from the review only in
    list marker, severity tag, whitespace and typographic quotes, dashes and
    arrows (a hand copy); it is still the same finding."""
    drifted = "[MINOR]  docs/brief.md:3 → stale\n  wording → reword it → @owner"
    write_dispute(
        tmp_path,
        "RULING: A FIX the budget\nRULING: B DISMISS refuted the wording matches",
        kinds="A;B",
        findings=[findings_toml({"A": LAUNCHER, "B": drifted})],
    )
    plan = REWORK_PLAN + "Excludes: F2 — dismissed: {}#B\n".format(DISPUTE_VERDICT)
    proc = write_single(tmp_path, plan=plan, findings=REVIEW)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_dismissal_of_an_unrelated_finding_refuses(tmp_path):
    """REVIEW-A WI-853 round 1 (Sol): F1 concerns the launcher budget, F2 the
    wording; the sitting dismissed only F1. Citing that ruling by its id to
    exclude F2 must not resolve F2."""
    write_dispute(
        tmp_path,
        "RULING: F1 DISMISS refuted the budget is enforced\n"
        "RULING: F2 FIX the wording is stale",
        kinds="F1;F2",
        findings=[findings_toml({"F1": LAUNCHER, "F2": WORDING})],
    )
    plan = REWORK_PLAN + "Excludes: F2 — dismissed: {}#F1\n".format(DISPUTE_VERDICT)
    proc = write_single(tmp_path, plan=plan, findings=REVIEW)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "F1 is not this review's F2" in proc.stdout, proc.stdout


def test_a_dismissal_from_another_round_under_the_same_id_refuses(tmp_path):
    """A sitting that dismissed round 1's F2 does not resolve round 2's
    different F2, cited with or without the fragment."""
    round_one = "- [MINOR] docs/other.md:9 -> an old typo -> fix it -> @owner"
    for cite in ("", "#F2"):
        root = tmp_path / ("x" + cite[1:])
        write_dispute(
            root,
            "RULING: F2 DISMISS not-worth-cost a typo",
            findings=[findings_toml({"F2": round_one})],
        )
        plan = REWORK_PLAN + "Excludes: F2 — dismissed: {}{}\n".format(
            DISPUTE_VERDICT, cite
        )
        proc = write_single(root, plan=plan, findings=REVIEW)
        assert proc.returncode == 1, (cite, proc.stdout + proc.stderr)
        assert "F2 is not this review's F2" in proc.stdout, proc.stdout


def test_a_dismissal_whose_finding_cannot_be_shown_refuses(tmp_path):
    """No findings file beside the verdict, or two beside it that request the
    same ids but record different findings: correspondence is not shown."""
    write_dispute(tmp_path / "none", "RULING: F2 DISMISS refuted no")
    write_dispute(
        tmp_path / "two",
        "RULING: F2 DISMISS refuted no",
        findings=[
            findings_toml({"F2": WORDING}),
            findings_toml({"F2": LAUNCHER}, name="004-DISPUTE-findings.toml"),
        ],
    )
    plan = REWORK_PLAN + "Excludes: F2 — dismissed: {}\n".format(DISPUTE_VERDICT)
    for case, says in (("none", "no findings file"), ("two", "is not this")):
        proc = write_single(tmp_path / case, plan=plan, findings=REVIEW)
        assert proc.returncode == 1, (case, proc.stdout + proc.stderr)
        assert says in proc.stdout, (case, proc.stdout)


def test_a_cited_ruling_that_does_not_dismiss_refuses(tmp_path):
    """A FIX or ESCALATE ruling, an unaccepted call, a ruling of another
    finding and a missing verdict each refuse the exclusion that cites them."""
    cases = (
        ("RULING: F2 FIX the wording is wrong", "accepted", "F2", "rules F2 FIX"),
        ("RULING: F2 ESCALATE high risk", "accepted", "F2", "rules F2 ESCALATE"),
        ("RULING: F2 DISMISS refuted no", "pending", "F2", "outcome pending"),
        ("RULING: F1 DISMISS refuted no", "accepted", "F1", "does not rule F2"),
    )
    for n, (ruling, outcome, kinds, says) in enumerate(cases):
        root = tmp_path / str(n)
        root.mkdir()
        write_dispute(root, ruling, outcome, kinds)
        plan = REWORK_PLAN + "Excludes: F2 — dismissed by {}\n".format(DISPUTE_VERDICT)
        proc = write_single(root, plan=plan, findings=REVIEW)
        assert proc.returncode == 1, (says, proc.stdout + proc.stderr)
        assert says in proc.stdout, (says, proc.stdout)
    plan = REWORK_PLAN + "Excludes: F2 — dismissed by {}\n".format(DISPUTE_VERDICT)
    proc = write_single(tmp_path / "absent", plan=plan, findings=REVIEW)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "does not exist" in proc.stdout


def test_a_real_dispute_verdict_ruling_FIX_refuses_its_exclusion(tmp_path):
    """WI-852's recorded dispute verdict ruled A FIX: citing it to exclude a
    finding refuses, read through the real verdict and binding."""
    src = ROOT / "docs" / "reviews" / "wi-852-coordinator-renders-kit-briefs"
    rel = "docs/reviews/wi-852/006-ADJUDICATE-cb444fd.md"
    dest = tmp_path / rel
    dest.parent.mkdir(parents=True)
    for suffix in ("", ".requested"):
        name = "006-ADJUDICATE-cb444fd.md" + suffix
        Path(str(dest) + suffix).write_bytes((src / name).read_bytes())
    plan = REWORK_PLAN + "Excludes: F2 — see {}#A\n".format(rel)
    proc = write_single(tmp_path, plan=plan, findings=REVIEW)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "rules A FIX" in proc.stdout
