"""The absolute-term advisory, called on in-memory rows (TC-273).

`absolute_terms.py` is a pure text rule beside `trace_text.py`: rows in,
advisories out, no file read. The last test drives one through `trace.analyze`
to pin the pipe it rides and that it never joins the exit code; the report
section's bytes are pinned by the golden runs in `tests/test_trace_golden.py`.

The ruled matrix: a need's `need` and `acceptance`, a requirement's
`Requirement` and `AcceptanceCriteria`, a design row's `Detail`; the waiver in
the tier's reason cell (`why`, `Rationale`); a test case never, because it
states a method, not an obligation.
"""

import inspect

from conftest import load_script

ABS = load_script("absolute_terms")


def _need(nid="SN-101", need="", acceptance="", why=""):
    return {"id": nid, "need": need, "acceptance": acceptance, "why": why}


def _sr(sid="SR-101", requirement="", ac="", rationale=""):
    return {
        "SR-ID": sid,
        "Requirement": requirement,
        "AcceptanceCriteria": ac,
        "Rationale": rationale,
    }


def _llr(lid="LLR-101", detail="", rationale=""):
    return {"LLR-ID": lid, "Detail": detail, "Rationale": rationale}


def _terms(cell):
    return [term for term, _ in ABS.absolutes(cell)]


# --- the matrix: which cells, which tiers --------------------------------------


def test_each_tier_scans_exactly_its_ruled_cells():
    open_world = "A team is protected in every repo."
    need_hits = ABS.absolute_advisories(
        [_need(need=open_world), _need("SN-102", acceptance=open_world)], [], []
    )
    assert [a.split()[:3] for a in need_hits] == [
        ["SN", "SN-101", "need"],
        ["SN", "SN-102", "acceptance"],
    ]
    sr_hits = ABS.absolute_advisories(
        [], [_sr(requirement=open_world), _sr("SR-102", ac=open_world)], []
    )
    assert [a.split()[:3] for a in sr_hits] == [
        ["SR", "SR-101", "Requirement"],
        ["SR", "SR-102", "AcceptanceCriteria"],
    ]
    llr_hits = ABS.absolute_advisories([], [], [_llr(detail=open_world)])
    assert [a.split()[:3] for a in llr_hits] == [["LLR", "LLR-101", "Detail"]]


def test_the_reason_cells_are_never_scanned():
    open_world = "Nothing breaks in every repo, and it never waits."
    assert ABS.absolute_advisories([_need(why=open_world)], [], []) == []
    assert ABS.absolute_advisories([], [_sr(rationale=open_world)], []) == []
    assert ABS.absolute_advisories([], [], [_llr(rationale=open_world)]) == []


def test_a_test_case_is_never_scanned():
    # A test case states a method, not an obligation, and carries no reason
    # cell to hold a waiver in: the tier table has no test-case entry and the
    # rule takes no test-case rows at all.
    assert set(ABS.ABSOLUTE_CELLS) == {"SN", "SR", "LLR"}
    assert list(inspect.signature(ABS.absolute_advisories).parameters) == [
        "needs",
        "srs",
        "llrs",
    ]


def test_a_placeholder_row_is_a_blank_form_not_a_row():
    open_world = "It never waits."
    assert (
        ABS.absolute_advisories(
            [_need("SN-000", need=open_world)],
            [_sr("SR-000", requirement=open_world)],
            [_llr("LLR-000", detail=open_world)],
        )
        == []
    )


# --- the suppression predicate: a closed domain, an open one, a waiver ----------


def test_an_absolute_over_a_closed_domain_is_suppressed():
    for cell in (
        "Every declared step runs.",  # a declared set
        "Every row in the registry resolves.",  # a registry
        "An id is never re-issued.",  # an id space, for a temporal absolute
        "Each need names its stakeholder.",  # a spine registry noun
        "Any SR-101 child is reported.",  # an id token
        "Every interface row names both endpoints.",
        "Each test case so named carries a warning.",  # a two-word row noun
        "Any work item it supersedes is closed.",
    ):
        assert ABS.absolutes(cell) == [], cell


def test_an_absolute_over_the_open_world_or_open_time_warns():
    assert _terms("A secret is caught before it publishes, in every repo.") == ["every"]
    assert _terms("A missing required tool fails, never silently skips.") == ["never"]
    assert _terms("The check is always on.") == ["always"]
    assert _terms("It fails on any broken link.") == ["any"]
    assert _terms("All tools stay usable offline.") == ["all"]
    # The pair is read as adjacent words, never as two loose ones.
    assert _terms("Every case a test reaches passes.") == ["every"]


def test_a_recorded_waiver_in_the_reason_cell_suppresses_the_row():
    waived = "recorded waiver: every adopter repository is the stakeholder's own scope"
    assert (
        ABS.absolute_advisories([_need(need="in every repo", why=waived)], [], []) == []
    )
    assert (
        ABS.absolute_advisories(
            [], [_sr(requirement="in every repo", rationale=waived)], []
        )
        == []
    )
    assert (
        ABS.absolute_advisories(
            [], [], [_llr(detail="in every repo", rationale=waived)]
        )
        == []
    )


def test_the_waiver_marker_counts_only_in_the_reason_cell():
    # Written into the scanned cell itself, the marker is prose about a waiver,
    # not a recorded one: the row still warns.
    row = _sr(requirement="Recorded waiver: none. It runs in every repo.")
    assert len(ABS.absolute_advisories([], [row], [])) == 1
    # And a sentence that merely mentions waivers, with no marker, waives nothing.
    row = _sr(requirement="It runs in every repo.", rationale="No waiver applies.")
    assert len(ABS.absolute_advisories([], [row], [])) == 1


# --- the tokenization -----------------------------------------------------------


def test_a_hyphenated_compound_is_one_token_and_names_a_mode():
    assert ABS.absolutes("The always-on floor applies a never-by-value rule.") == []
    assert ABS.absolutes("An all-or-nothing write lands.") == []


def test_a_negative_counts_only_where_it_opens_a_clause():
    # "no" inside a clause describes one case's input or outcome ("a repo with
    # no commits", "produces no report"); opening a clause it states a
    # universal negative.
    assert ABS.absolutes("A repo with no commits produces no report.") == []
    assert _terms("No information is encoded by colour alone.") == ["no"]
    assert _terms("It stays fast; nothing waits on the network.") == ["nothing"]
    assert _terms("It stays fast (none of it waits on the network).") == ["none"]
    # After a comma a negative usually continues a list describing one case.
    assert ABS.absolutes("A case with no inputs, no lifetime, fails.") == []


def test_no_followed_by_a_comparative_is_a_bound_not_an_absolute():
    assert ABS.absolutes("No more than two workers run.") == []
    assert ABS.absolutes("No later than the next commit, it reports.") == []


def test_all_after_at_is_emphasis_not_a_quantifier():
    assert ABS.absolutes("It does not wait at all.") == []
    assert _terms("It waits for all tools.") == ["all"]


def test_a_quantifier_domain_is_a_bounded_window_inside_its_own_clause():
    # The closed-domain word must fall within the window after the quantifier...
    far = "Every change made by any person anywhere at all ever is a declared one."
    assert "every" in _terms(far)
    # ...and inside the same segment: a registry named after a clause break or
    # a comma is not the quantifier's domain.
    assert _terms("It holds in every repo; the registry is separate.") == ["every"]
    assert _terms("It holds in every repo, the registry aside.") == ["every"]


def test_a_temporal_absolute_reads_its_whole_clause():
    # "never" and "always" have no following noun: their domain is the clause's
    # own subject, wherever it stands.
    assert ABS.absolutes("A deleted id is never re-issued.") == []
    assert _terms("A deleted file is never re-issued.") == ["never"]
    # A comma does not end the clause, so the subject before it still counts.
    assert ABS.absolutes("A retired id, once deleted, is never re-issued.") == []


def test_matching_is_whole_word_and_case_insensitive():
    assert _terms("NEVER silently.") == ["never"]
    assert ABS.absolutes("Nevertheless, the allowance is anyway nominal.") == []


# --- the finding and its console summary ----------------------------------------


def test_one_finding_per_row_cell_naming_each_term_in_context():
    [finding] = ABS.absolute_advisories(
        [],
        [_sr(requirement="It never waits, and runs in every repo.")],
        [],
    )
    assert finding.startswith("SR SR-101 Requirement ")
    assert "'never' (never waits)" in finding
    assert "'every' (every repo)" in finding
    assert "recorded waiver: <reason>" in finding and "Rationale" in finding
    assert "warn-only" in finding


def test_the_need_finding_points_its_waiver_at_why():
    [finding] = ABS.absolute_advisories([_need(need="in every repo")], [], [])
    assert "in `why`" in finding


def test_the_console_summary_is_one_line_counted_per_tier_or_nothing():
    assert ABS.absolute_summary([]) == []
    findings = ABS.absolute_advisories(
        [_need(need="in every repo")],
        [_sr(requirement="in every repo"), _sr("SR-102", ac="never waits")],
        [_llr(detail="always on")],
    )
    [line] = ABS.absolute_summary(findings)
    assert "4 absolute-term advisories" in line
    assert "SN 1, SR 2, LLR 1" in line
    assert "Absolute-term advisories" in line


def test_the_report_section_lists_every_advisory_or_says_none():
    assert ABS.absolute_report_lines([]) == [
        "",
        "## Absolute-term advisories (warn-only)",
        "",
        "None. No absolute names an open domain.",
    ]
    findings = ABS.absolute_advisories([_need(need="in every repo")], [], [])
    lines = ABS.absolute_report_lines(findings)
    assert lines[1] == "## Absolute-term advisories (warn-only)"
    assert lines[3:] == ["- " + findings[0]]


# --- through the checker ----------------------------------------------------------


def test_a_positive_advisory_rides_its_own_pipe_through_analyze_and_never_gates(
    tmp_path,
):
    """A planted open-world absolute driven through `trace.analyze` lands in
    `absolute_advis` and in no other list, and that list joins no exit code
    under any flag."""
    import argparse
    import dataclasses

    trace = load_script("trace")
    empty = trace.load_registries(tmp_path / "docs")
    row = dict(_sr(requirement="The harness shall catch a secret in every repo."))
    row.update(Verification="Test", Status="Drafted")
    findings = trace.analyze(
        dataclasses.replace(empty, srs=[row]), trace.AnalysisFlags()
    )
    [line] = findings.absolute_advis
    assert line.startswith("SR SR-101 Requirement ") and "'every' (every repo)" in line
    holding = [
        f.name
        for f in dataclasses.fields(findings)
        if isinstance(getattr(findings, f.name), list)
        and line in getattr(findings, f.name)
    ]
    assert holding == ["absolute_advis"]
    for strict, strict_integrity in ((True, False), (False, True), (False, False)):
        flags = argparse.Namespace(strict=strict, strict_integrity=strict_integrity)
        assert trace.exit_code(findings, flags) == 0
