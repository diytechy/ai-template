"""`Hat-Refs`: the perspective record as a resolvable cell (SR-161 / LLR-183).

The convention this replaces asked an author to name a derived requirement's
deriving perspective as PROSE inside `Rationale`. That reads correctly to a
human and resolves against nothing — no check could tell a live hat from one
deleted a month ago — so the attribution became a cell whose values resolve
against the declared roster.

Four claims are checked here, and the second and third are the ones that decide
whether the rule is adoptable rather than merely correct:

1. RESOLUTION IS A FINDING — a `Hat-Refs` naming a hat the roster does not
   declare joins the `--strict` failure set, like an SR citing a deleted SN.
2. THE LAYER IS OPT-OUT — no roster, or a roster that will not parse, and the
   whole rule goes VACUOUS. A malformed roster reddening every row in the spine
   would punish the wrong file, and `hats.py` raises on that same file the
   moment any composer touches it.
3. COVERAGE NEVER GATES — the cell is empty on nearly every row the day it
   exists, so presence is one advisory count and never a finding. A rule that is
   100% red on the day it ships is a rule somebody switches off.
4. THE EFFECTIVE SET IS DERIVED — `effective_hats` unions a row's own refs with
   its parents', so re-ruling one SR moves every child's answer with no child
   cell edited.

Plus the anti-drift pin the design's one deliberate compromise needs: `trace.py`
reads the roster a second time (for NAMES only — `hats.py` stays the sole
validator of roster CONTENT) rather than importing `hats`, because the declared
crossing between those two components already runs the other way. A TEST may
import both, so the two paths are pinned equal here.

Every green below is demonstrated able to fail: the vacuity cases are driven
over a tree that reds when the roster is present, so "reported nothing" is never
confused with "looked at nothing".
"""

from __future__ import annotations

import types

from conftest import ROOT, load_script, make_minimal_project, run_py

trace = load_script("trace")
hats = load_script("hats")

ROSTER = """
[hat.SECURITY]
applies_when = "always"
asks = "What secret does this touch?"
listens_for = "A secret spent with no requirement naming the authority."

[hat.MAINTAINER]
applies_when = "always"
asks = "Can a reader two years from now tell why this exists?"
listens_for = "A requirement whose reason lives only in the session that wrote it."
"""


def write_roster(root, text=ROSTER):
    path = root / "docs" / "requirements" / "hats.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def sr(sid, hat_refs="", sr_id_col="SR-ID"):
    return {sr_id_col: sid, "Hat-Refs": hat_refs}


def llr(lid, hat_refs="", sr_refs=""):
    return {"LLR-ID": lid, "Hat-Refs": hat_refs, "SR-Refs": sr_refs}


# --- 1. resolution is a finding ----------------------------------------------


def test_an_undeclared_hat_name_is_a_finding():
    findings, _ = trace.hat_findings(
        [sr("SR-001", "SECURITY"), sr("SR-002", "SECRUITY")],
        [],
        {"SECURITY", "MAINTAINER"},
    )
    assert len(findings) == 1, findings
    assert "SR-002" in findings[0]
    assert "SECRUITY" in findings[0]
    # The label names the CELL, so a reader of the console line knows which
    # column to open — the frame bundle's own rule about labels that lie.
    assert "Hat-Refs" in findings[0]


def test_the_design_tier_is_checked_too_and_names_its_own_id():
    findings, _ = trace.hat_findings([], [llr("LLR-009", "NOSUCH")], {"SECURITY"})
    assert len(findings) == 1, findings
    assert findings[0].startswith("LLR LLR-009"), findings[0]


def test_a_declared_name_is_silent():
    findings, _ = trace.hat_findings(
        [sr("SR-001", "SECURITY;MAINTAINER")], [], {"SECURITY", "MAINTAINER"}
    )
    assert findings == []


# --- 2. the layer is opt-out --------------------------------------------------


def test_the_rule_is_vacuous_without_a_roster():
    # The SAME rows that red above report nothing when no roster is declared:
    # absence is opt-out for the whole hats layer, so there is no declared name
    # a row could fail to cite.
    findings, advisories = trace.hat_findings([sr("SR-002", "SECRUITY")], [], set())
    assert findings == []
    assert advisories == []


def test_an_absent_roster_file_reads_as_no_names(tmp_path):
    assert trace.load_hat_names(tmp_path) == (set(), {})


def test_an_unparseable_roster_is_vacuous_not_loud(tmp_path):
    write_roster(tmp_path, "[hat.SECURITY\nthis will not parse = = =\n")
    # Deliberately NOT a raise: this is a findings pass, not the roster's load
    # path. `hats.py` is what refuses a broken roster, loudly, to every composer.
    assert trace.load_hat_names(tmp_path) == (set(), {})


def test_a_well_formed_roster_yields_its_names(tmp_path):
    write_roster(tmp_path)
    assert trace.load_hat_names(tmp_path) == ({"SECURITY", "MAINTAINER"}, {})


def test_a_roster_whose_hat_table_is_not_a_table_is_vacuous(tmp_path):
    write_roster(tmp_path, 'hat = "not a table"\n')
    assert trace.load_hat_names(tmp_path) == (set(), {})


# --- 3. coverage never gates --------------------------------------------------


def test_coverage_is_one_advisory_and_never_a_finding():
    findings, advisories = trace.hat_findings(
        [sr("SR-001"), sr("SR-002"), sr("SR-003", "SECURITY")],
        [llr("LLR-001")],
        {"SECURITY", "MAINTAINER"},
    )
    assert findings == []
    coverage = [a for a in advisories if a.startswith("hat coverage:")]
    assert len(coverage) == 1, advisories
    # Three of four rows carry nothing — and the line says NOT RECORDED, which
    # is the whole difference between this cell and a claim.
    assert "3 of 4" in coverage[0]
    assert "NOT RECORDED" in coverage[0]


def test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories():
    # The first-run-adopter case, and the reason both advisories are gated: a
    # freshly bootstrapped project ships the roster and no Hat-Refs anywhere.
    # Greeting a stranger with "every row records nothing" plus sixteen hats
    # called ceremony is noise about a layer they have not opted into.
    findings, advisories = trace.hat_findings(
        [sr("SR-001"), sr("SR-002")], [llr("LLR-001")], {"SECURITY", "MAINTAINER"}
    )
    assert findings == []
    assert advisories == []


def test_one_filled_cell_lights_both_advisories_up():
    # ...and the gate is not a mute: the moment the layer IS in use, the
    # question becomes answerable and both lines appear.
    _, advisories = trace.hat_findings(
        [sr("SR-001", "SECURITY"), sr("SR-002")], [], {"SECURITY", "MAINTAINER"}
    )
    assert any(a.startswith("hat coverage:") for a in advisories), advisories
    assert any("attributed to NO row" in a for a in advisories), advisories


def test_coverage_counts_effective_sets_not_cells():
    # A design row whose PARENT carries hats IS attributable to them. Counting
    # its blank cell as unattributed would report the derived half of the feature
    # as if it did not exist — and would push an author toward the copy-down the
    # derivation exists to forbid.
    parent = sr("SR-001", "SECURITY")
    child = llr("LLR-001", sr_refs="SR-001")  # blank cell, non-empty effective set
    _, advisories = trace.hat_findings(
        [parent], [child], {"SECURITY"}, {"SR-001": parent}
    )
    assert [a for a in advisories if a.startswith("hat coverage:")] == [], advisories
    # Without the parent index the same tree over-reports — the documented
    # degrade, pinned so it cannot silently become the only reading.
    _, degraded = trace.hat_findings([parent], [child], {"SECURITY"})
    assert any(a.startswith("hat coverage: 1 of 2") for a in degraded), degraded


def test_a_fully_covered_spine_reports_no_coverage_line():
    _, advisories = trace.hat_findings([sr("SR-001", "SECURITY")], [], {"SECURITY"})
    assert [a for a in advisories if a.startswith("hat coverage:")] == []


def test_a_hat_no_row_is_attributable_to_is_reported():
    _, advisories = trace.hat_findings(
        [sr("SR-001", "SECURITY")], [], {"SECURITY", "MAINTAINER"}
    )
    unattributed = [a for a in advisories if "attributed to NO row" in a]
    assert len(unattributed) == 1, advisories
    assert "MAINTAINER" in unattributed[0]
    assert "SECURITY" not in unattributed[0]


# --- 4. the effective set is derived, never copied ----------------------------


def test_effective_hats_unions_the_parents():
    parents = {"SR-001": sr("SR-001", "SECURITY")}
    row = llr("LLR-001", hat_refs="MAINTAINER", sr_refs="SR-001")
    assert trace.effective_hats(row, parents) == ["MAINTAINER", "SECURITY"]


def test_a_parent_re_ruling_moves_the_child_with_no_child_cell_edited():
    row = llr("LLR-001", hat_refs="MAINTAINER", sr_refs="SR-001")
    before = trace.effective_hats(row, {"SR-001": sr("SR-001", "SECURITY")})
    # The SR is re-ruled. THE CHILD ROW IS NOT TOUCHED — `row` is the same dict.
    after = trace.effective_hats(row, {"SR-001": sr("SR-001", "PERFORMANCE")})
    assert before == ["MAINTAINER", "SECURITY"]
    assert after == ["MAINTAINER", "PERFORMANCE"]


def test_multiple_parents_all_contribute_and_duplicates_collapse():
    parents = {
        "SR-001": sr("SR-001", "SECURITY"),
        "SR-002": sr("SR-002", "SECURITY;MAINTAINER"),
    }
    row = llr("LLR-001", hat_refs="SECURITY", sr_refs="SR-001;SR-002")
    assert trace.effective_hats(row, parents) == ["MAINTAINER", "SECURITY"]


def test_a_dangling_parent_contributes_nothing_rather_than_raising():
    # Parentage is already a reported finding of its own; a derivation that
    # crashed here would report the same defect twice, the second time as a
    # stack trace.
    row = llr("LLR-001", hat_refs="SECURITY", sr_refs="SR-404")
    assert trace.effective_hats(row, {}) == ["SECURITY"]


def test_a_row_with_no_refs_anywhere_derives_the_empty_set():
    assert trace.effective_hats(llr("LLR-001"), {}) == []


# --- the anti-drift pin for the second reader ---------------------------------


def test_the_roster_path_matches_the_hats_module():
    # `trace.py` may not import `hats` (the declared crossing between those two
    # components runs the other way), so nothing in the SHIPPED code holds these
    # two constants together. A test may import both, and does.
    assert trace.HAT_ROSTER_REL == hats.ROSTER_REL


def test_the_live_roster_resolves_every_hat_the_live_spine_cites():
    # Not a fixture — the kit's own registries. A backfilled attribution naming
    # a hat this repo does not declare would be exactly the rot the cell exists
    # to make visible.
    names, _speaks_for = trace.load_hat_names(ROOT)
    assert names, "the kit declares a roster; an empty read means the path moved"
    reg = trace.load_registries(ROOT / "docs")
    findings, _ = trace.hat_findings(reg.srs, reg.llrs, names)
    assert findings == [], findings


# --- the end-to-end wiring: the finding reaches the exit code ------------------


def test_an_undeclared_hat_reds_a_real_run_under_strict(scaffold):
    make_minimal_project(scaffold)
    write_roster(scaffold)
    csv = scaffold / "docs" / "requirements" / "system-requirements.csv"
    text = csv.read_text(encoding="utf-8").splitlines()
    # Append the column to the header and a bad value to the first data row.
    text[0] += ",Hat-Refs"
    text[1] += ",SECRUITY"
    csv.write_text("\n".join(text) + "\n", encoding="utf-8")

    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FINDING (hat)" in proc.stdout, proc.stdout
    assert "SECRUITY" in proc.stdout

    # And it is non-vacuous in the other direction: the SAME tree with the name
    # spelled correctly exits zero.
    text[1] = text[1].replace("SECRUITY", "SECURITY")
    csv.write_text("\n".join(text) + "\n", encoding="utf-8")
    ok = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "FINDING (hat)" not in ok.stdout


# --- a perspective's `speaks_for`, resolved against the stakeholder list -------
# (SR-213; TC-245, the rule half.) The roster's shape is `hats.py`'s to judge
# (tests/test_hats.py); what the checker answers is whether the stakeholder a
# perspective speaks for is DECLARED. `load_hat_names` hands the map back beside
# the names, because the checker may not import `hats`.

SPEAKING_ROSTER = (
    ROSTER
    + """
[hat.FIRST-RUN-ADOPTER]
applies_when = "always"
asks = "Can a new adopter complete this from the shipped guidance?"
listens_for = "A requirement satisfiable only with undocumented knowledge."
speaks_for = "STK-01"
"""
)


def test_the_roster_read_returns_each_speaks_for_beside_the_names(tmp_path):
    write_roster(tmp_path, SPEAKING_ROSTER)
    names, speaks_for = trace.load_hat_names(tmp_path)
    assert names == {"SECURITY", "MAINTAINER", "FIRST-RUN-ADOPTER"}
    # Only the perspective that records one appears: most voice no one.
    assert speaks_for == {"FIRST-RUN-ADOPTER": "STK-01"}


def test_a_declared_stakeholder_passes():
    findings, _ = trace.hat_findings(
        [],
        [],
        {"FIRST-RUN-ADOPTER"},
        speaks_for={"FIRST-RUN-ADOPTER": "STK-01"},
        stakeholders={"STK-01", "STK-02"},
    )
    assert findings == []


def test_an_undeclared_stakeholder_fails_naming_the_hat_and_the_stakeholder():
    findings, _ = trace.hat_findings(
        [],
        [],
        {"FIRST-RUN-ADOPTER", "MAINTAINER"},
        speaks_for={"FIRST-RUN-ADOPTER": "STK-09", "MAINTAINER": "STK-01"},
        stakeholders={"STK-01"},
    )
    assert len(findings) == 1, findings
    assert "FIRST-RUN-ADOPTER" in findings[0], findings[0]
    assert "STK-09" in findings[0], findings[0]
    assert "speaks_for" in findings[0], findings[0]


def test_a_hat_with_no_speaks_for_passes():
    findings, _ = trace.hat_findings(
        [], [], {"SECURITY", "MAINTAINER"}, speaks_for={}, stakeholders={"STK-01"}
    )
    assert findings == []


def test_with_no_stakeholder_list_the_speaks_for_rule_produces_nothing():
    # The SAME map that fails above against a declared list is silent with no
    # list at all: a project declaring no stakeholders has no one to resolve.
    for stakeholders in (set(), None):
        findings, _ = trace.hat_findings(
            [],
            [],
            {"FIRST-RUN-ADOPTER"},
            speaks_for={"FIRST-RUN-ADOPTER": "STK-09"},
            stakeholders=stakeholders,
        )
        assert findings == [], (stakeholders, findings)


# --- both perspective rules, through the checker's own load and compose -------
# (SR-213, SR-214.) The rule cases above and in tests/test_assumption_rules.py
# call `hat_findings` and `obstacle_hat_findings` directly, so they stay green
# if `load_registries` stops reading a hat's `speaks_for` or `analyze` stops
# composing either rule. These drive the checker in process over a tree on
# disk: the registries are loaded, analyzed, gated and reported the way a
# `--strict` run does, so a finding that never reaches the `hat` class, the
# exit code or the report's summary count reds here.

STAKEHOLDERS = """
[stakeholder.STK-01]
name = "Adopting team"
description = "A team that adds the package to its own work."
party = "EXT-001"
status = "Approved"
"""

# The party the stakeholder names, declared so the tree is otherwise clean:
# a strict exit of 1 below is then the hat class's alone.
PARTY = """
[entity.EXT-001]
name = "Downstream adopter"
class = "operational"
description = "The team that adopts the package."
status = "Drafted"
"""


def _speaking(stakeholder):
    return (
        "[hat.FIRST-RUN-ADOPTER]\n"
        'applies_when = "always"\n'
        'asks = "Can a new adopter complete this from the shipped guidance?"\n'
        'listens_for = "A requirement satisfiable only with undocumented '
        'knowledge."\n'
        'speaks_for = "{}"\n'.format(stakeholder)
    )


def _assumption(obstacle_hats=None):
    text = (
        "[assumption.DA-001]\n"
        'assumption = "An adopter reads the shipped guide first."\n'
        'status = "Drafted"\n'
    )
    if obstacle_hats is not None:
        text += "obstacle_hats = {}\n".format(
            "[" + ", ".join('"{}"'.format(n) for n in obstacle_hats) + "]"
        )
    return text


def _check(root, roster, assumption):
    """Load, analyze, gate and report `root` as `trace.py --strict` does:
    `(hat findings, strict exit code, report text)`. `roster` None means the
    project declares no hats roster."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.toml").write_text(STAKEHOLDERS, encoding="utf-8")
    (req / "external.toml").write_text(PARTY, encoding="utf-8")
    (req / "assumptions.toml").write_text(assumption, encoding="utf-8")
    if roster is None:
        (req / "hats.toml").unlink(missing_ok=True)
    else:
        write_roster(root, roster)
    reg = trace.load_registries(root / "docs")
    flags = trace.AnalysisFlags()
    findings = trace.analyze(reg, flags)
    gate = types.SimpleNamespace(strict=True, strict_integrity=False)
    forest = trace.build_forest(
        reg.sn_ids, reg.srs, reg.llrs, reg.tcs, findings.orphan_ids, reg.sn_draft
    )
    report = trace.render_report(reg, findings, flags, forest)
    return findings.hat_dangling, trace.exit_code(findings, gate), report


def test_the_checker_loads_and_fails_an_undeclared_speaks_for(tmp_path):
    hat, code, report = _check(tmp_path, _speaking("STK-09"), _assumption())
    assert len(hat) == 1, hat
    assert "FIRST-RUN-ADOPTER" in hat[0] and "STK-09" in hat[0], hat
    assert code == 1
    assert "| Hat findings | 1 |" in report, report
    # The SAME roster voicing the declared stakeholder passes.
    hat, code, report = _check(tmp_path, _speaking("STK-01"), _assumption())
    assert hat == [] and code == 0, hat
    assert "| Hat findings | 0 |" in report, report


def test_the_checker_fails_and_counts_an_obstacle_perspective_with_no_roster(
    tmp_path,
):
    hat, code, report = _check(tmp_path, None, _assumption(["SECURITY"]))
    assert len(hat) == 1, hat
    assert "DA-001" in hat[0] and "SECURITY" in hat[0], hat
    assert code == 1
    # No roster, and still summarized: a strict failure listed in the report's
    # section must carry its count in the metric table too.
    assert "| Hat findings | 1 |" in report, report
    assert "| Declared hats | 0 |" in report, report
    # An empty cell with no roster is not recorded, and fails nothing; with no
    # roster and no finding the metric rows stay out.
    hat, code, report = _check(tmp_path, None, _assumption())
    assert hat == [] and code == 0, hat
    assert "Hat findings" not in report, report


def test_the_checker_passes_an_obstacle_perspective_the_roster_declares(tmp_path):
    hat, code, _ = _check(tmp_path, ROSTER, _assumption(["SECURITY"]))
    assert hat == [] and code == 0, hat
