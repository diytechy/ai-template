"""spine_rules.py: the PURE RULE LIBRARY both derived axes read.

WHAT THIS MODULE IS NOW. `derive_gate.py` was renamed `spine_rules.py` and gutted
at WI-498 slice 5: the three-value BAR axis, the `docs/gate` writer/reader and the
whole CLI are gone, and what remains is a library with no `main()`, no file
writing and no output. So this suite no longer drives a script — it calls the
surviving functions directly, and it re-points every claim that used to be made
about a BAR onto the eight-rung STAGE ladder those same rows now derive.

WHAT IT COVERS.

  * `phase_num` — the one phase-parse the kit shares.
  * `load_spine` + `spine_stage` — the rung fall-through over a real scaffold:
    the SN-coverage rung, the `-000` example-row filter, and the walk of a
    project up the ladder from a drafted requirement to DevStg-Impl.
  * the meta-repo DOGFOOD — this repo's own per-phase rungs, checked against a
    deliberate SECOND implementation re-derived straight from the registry TOML
    (the adversarial review's F3: comparing a subprocess to the same function is
    tautological).
  * the derived current PHASE, read off `derive_stage.derive`'s record — the
    field is derived from `spine_rules.phase_num` over the same rows.

WHAT LIVES ELSEWHERE. The stage axis's own producer contract (`docs/stage`,
`--check`, the draft counterfactual, the floor) is `tests/test_derive_stage.py`;
the exhaustive rung sweep over the closed Status enum is
`tests/test_approval_level.py`; the pure carrier half is
`tests/test_kitlib_stage.py`; the equal-predicate pins against `trace.py` are
`tests/test_rule_sync.py`.
"""

# --- TOMBSTONE: what WI-498 slice 5 deleted from this file, and where it went --
#
# THIS IS AN ACT, NOT A DRIFT. Twenty-one of the thirty-two tests in this module
# (then `tests/test_derive_gate.py`) were removed in one commit because their
# SUBJECT retired, not because they were inconvenient. Two more MOVED. Each
# guarantee they carried is named below with the surface that carries it now; if
# a reader finds one of these claims unpinned anywhere, that is a regression in
# this deletion and not a licence to re-weaken the rule.
#
#   `test_sr_gate_rules`, `test_maturity_and_sn_gate_rules`
#       `sr_bar`, `maturity_bar` and `sn_bar` were deleted with the BAR axis.
#       The per-artifact rules they asserted are the STAGE ladder's rungs now and
#       are driven through `spine_stage` here (the SN-coverage rung, the
#       decomposition rungs) and exhaustively in
#       `tests/test_approval_level.py`. The one claim that was NOT a bar
#       claim — that `SPINE_TRANSITIONAL` and `SPINE_MATURITY` never overlap — is
#       pinned harder by VALUE in `tests/test_rule_sync.py`
#       (`test_no_declared_status_vocabulary_still_lists_a_RETIRED_word`:
#       `set(SPINE_MATURITY) == {drafted, approved, founded}` exactly, and no
#       retired word may appear in it).
#
#   `test_minimal_project_derives_the_ceilinged_top`, `test_draft_sr_drops_the_gate`,
#   `test_undecomposed_sr_is_g1`, `test_decomposed_unverified_is_g2`,
#   `test_no_real_srs_is_g1`
#       All five called `compute()`, which is deleted. Each aggregation shape they
#       drove is re-driven on the stage axis: the fresh scaffold in
#       `tests/test_derive_stage.py::test_a_fresh_scaffold_reads_a_DEFINED_non_raising_selection_value`,
#       the all-draft spine in `::test_an_ALL_DRAFT_spine_also_lands_on_the_floor`,
#       and the undecomposed / decomposed / settled ladder in
#       `test_requirement_first_lifecycle_end_to_end` below.
#
#   `test_the_modified_basis_counter_RETIRED_with_its_predicate`,
#   `test_the_basis_line_still_parses_under_its_SURVIVING_consumer`
#       The `# basis:` line and `basis_line()` are gone with `docs/gate`, and so
#       is every field on it. The producer/consumer ROUND TRIP the second one
#       existed for now runs over `docs/stage` in
#       `tests/test_derive_stage.py` (`test_the_written_file_is_LF_and_parses_back`
#       drives render->parse; `test_write_then_check_roundtrips` drives
#       write->read) and over `kitlib.stage`'s own field block in
#       `tests/test_kitlib_stage.py`.
#       ONE ORPHANED HALF, RECORDED RATHER THAN GLOSSED: that test also pinned
#       `check_trajectory` has no `read_derived_phases` and no `GATE_FILE`
#       ("retired, not merely unreferenced"). Both are genuinely absent from the
#       source and the SUCCESSOR behaviour is driven —
#       `tests/test_stage_event_detectors.py` exercises `phase_stages` over
#       `per-phase-live` — but the negative structural pin has no home now. Its
#       `check.py` twin does: `tests/test_selection_at_or_above.py::
#       test_the_floor_and_the_advisory_tier_are_RETIRED_not_merely_unused`.
#
#   `test_write_then_check_roundtrips`, `test_check_detects_state_drift`,
#   `test_check_legacy_gate_compares_value_only`,
#   `test_a_cache_carrying_the_RETIRED_vocabulary_reports_STALE`
#       The `docs/gate` cache and its `--check` rot guard. The file itself is
#       deleted from the repo AND from the scaffold. Successors already exist and
#       are driven against `docs/stage`:
#       `tests/test_derive_stage.py::test_write_then_check_roundtrips`,
#       `::test_check_detects_state_drift`,
#       `::test_check_on_an_ABSENT_file_asks_for_the_first_generation` and
#       `::test_a_freshly_scaffolded_repo_is_GREEN_on_the_placeholder` (the
#       smooth-transition path the legacy-marker test used to hold).
#
#   `test_draft_sn_drops_the_gate`
#       (A NOTE ON THE BRIEF THAT COMMISSIONED THIS DELETION, because a wrong
#       reason recorded as fact is worse than no reason: the brief called this
#       name "defined twice, at roughly lines 227 and 446". It was not. Line 227
#       was `test_draft_SR_drops_the_gate` and line 446 was
#       `test_draft_SN_drops_the_gate` — two different rows of the spine, one
#       letter apart. Both are deleted, so the outcome is unchanged, but there
#       was no shadowed duplicate `def` and no silently skipped test.)
#       THE CLAIM INVERTS on the stage axis: a draft deliberately CANNOT drop the
#       effective stage any more — that was C-01, and refusing it is the whole
#       point of the settled subset. The new truth is pinned by
#       `tests/test_derive_stage.py::test_ONE_drafted_row_does_not_drop_the_effective_stage`
#       and `::test_a_draft_that_OPENS_A_NEW_PHASE_does_not_drop_it_either`; the
#       honest LIVE reading, which still does drop, is asserted there beside it.
#
#   the four `test_ex_draft_*` tests
#       `ex_draft` and the product floor it fed both retired at WI-498 slice 2.
#       The counterfactual itself did not die — it moved onto its own axis and is
#       `derive_stage`'s settled subset, driven in `tests/test_derive_stage.py`.
#
#   the three OI-30 D2 ceiling tests
#       (`test_sr_bar_CEILINGS_at_DevStg_Tests_and_impl_is_unreachable_by_cell`,
#       `test_the_ceiling_note_has_exactly_ONE_rendering_home`,
#       `test_the_ceiling_note_never_reaches_the_MACHINE_value`)
#       `_RELEASE_CEILING`, `_CEILING_NOTE` and `bar_label` retired with the bar.
#       THE RULE THEY PROTECTED IS UNCHANGED AND IS NOW ENFORCED MORE STRONGLY:
#       **a Status cell may never claim the test evidence passed.** On the bar
#       axis that needed a ceiling flag; on the stage axis DevStg-Release simply
#       has no producer, which is a stronger guarantee than a cap — pinned by
#       `tests/test_approval_level.py::test_NO_status_combination_reaches_the_RELEASE_rung`
#       (exhaustive over 128 spines) and
#       `::test_the_RELEASE_rung_has_no_PRODUCER_in_the_source` (structural, so a
#       `return STAGE_RELEASE` behind a condition no fixture builds is caught
#       too).
#
#   MOVED, not deleted: `test_next_phase_prints_max_plus_one` and
#   `test_next_phase_on_an_unphased_spine` are now in
#   `tests/test_derive_stage.py`, re-keyed to `derive_stage.py --next-phase` —
#   the CLI they drove was rehomed there when this module's CLI retired. The
#   WI-402 ruling they record is still live and `--next-phase` is still taught in
#   PROCESS.md, PROCESS_OPTIONS.md and RESYNC_PACK.md.

import re as _re
import tomllib as _toml

from conftest import (
    ROOT,
    load_script,
    make_minimal_project,
    record_ids,
    run_py,
)

RULES = load_script("spine_rules")
DS = load_script("derive_stage")

# Registry helpers -------------------------------------------------------------
SRS_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status\n"
)
LLRS_H = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
TCS_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
)


def _sr(sid, verification="Test", status="Approved", sn="SN-001"):
    return '{},T,{},"r","why","ac",,M,{},{}\n'.format(sid, sn, verification, status)


def _write(scaffold, srs="", llrs="", tcs=""):
    req = scaffold / "docs" / "requirements"
    if srs:
        (req / "system-requirements.csv").write_text(SRS_H + srs, encoding="utf-8")
    if llrs:
        (req / "low-level-requirements.csv").write_text(LLRS_H + llrs, encoding="utf-8")
    if tcs:
        (scaffold / "docs" / "test" / "test-cases.csv").write_text(
            TCS_H + tcs, encoding="utf-8"
        )


def _no_frame(scaffold):
    """Drop the two off-spine registries the ladder's INSERTED rungs read.

    Not a convenience, and the same helper `tests/test_derive_stage.py` needs for
    the same reason: those two rungs are REPO-GLOBAL and sit BELOW every spine
    rung, so a scaffold's blank-but-present `external.toml` pins the reading at
    DevStg-Boundary and no spine-rung difference is observable at all. The frame
    rungs have their own tests over there; here they would mask the rung under
    test. Deleting the file (rather than emptying it) is what the applies-when
    reads — an ABSENT registry skips the rung, an EMPTY one holds it open."""
    for name in ("external", "components"):
        for suffix in (".toml", ".csv"):
            path = scaffold / "docs" / "requirements" / (name + suffix)
            if path.exists():
                path.unlink()


def _stage(scaffold):
    """The LIVE repo-global rung for a scaffold, straight through the library.

    `load_spine` returns exactly the keyword arguments `spine_stage` takes, so
    this is the whole derivation with nothing between it and the registries — the
    replacement for the deleted `compute()` wrapper every aggregation test used
    to call."""
    return RULES.spine_stage(**RULES.load_spine(scaffold / "docs"))


# --- the meta-repo dogfood ----------------------------------------------------
LLR_EXEMPT_METHODS = {"Analysis", "Inspection", "Attest"}


def _meta_text(rel):
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def _meta_rows(rel, table, prefix):
    tables = _toml.loads(_meta_text(rel)).get(table, {})
    return [
        dict(cells, _id=rid)
        for rid, cells in tables.items()
        if rid.startswith(prefix) and not rid.endswith("-000")
    ]


def _meta_status(row):
    return str(row.get("status") or "").strip().lower()


def _meta_phase(row):
    # `phase` is a real int under the TOML carrier; the derivation buckets by its
    # text, and a blank cell is the implicit `(default)` bucket.
    return str(row.get("phase", "")).strip() or "(default)"


def _meta_refs(value):
    """A multi-ref cell as a list of ids, tolerating BOTH shapes the raw TOML can
    hold: a real array (`sn_refs = ["SN-004", "SN-008"]`) or a delimited string.
    Deliberately not `spine_rules.refs` — reading these rows without the module's
    own helpers is the independence this side is for."""
    parts = (
        value
        if isinstance(value, (list, tuple))
        else _re.split(r"[;,\s]+", str(value or "").strip())
    )
    return [str(p).strip() for p in parts if str(p).strip()]


def _independent_meta_expectations():
    """Per-phase STAGE expectations for THIS repo, re-derived straight from the
    registry TOML with none of spine_rules's machinery — a deliberate second
    implementation of the rung ladder, so the dogfood can catch `spine_stage`
    breaking (the adversarial review's F3: comparing a subprocess to the same
    function is tautological).

    RE-KEYED FROM BARS TO RUNGS AT WI-498 SLICE 5. The previous version expected
    DevStg-Below / DevStg-Reqs / DevStg-Tests out of `sr_bar`'s three-value
    arithmetic; that axis is deleted, so this side now transcribes the RUNG
    fall-through from its stated rules instead:

      needs drafted or absent -> Needs; declared boundary in work -> Boundary; a
      Drafted requirement in the phase -> Reqs; an approved need no requirement
      cites -> Needs; the declared partition in work -> Arch; a requirement with
      no LLR (unless LLR-exempt) or a Drafted LLR -> LLReqs; a requirement no TC
      verifies or a Drafted TC -> Tests; otherwise Impl.

    Read with STDLIB `tomllib` straight off the files, not through
    `spine_carrier`: the independence covers the carrier as well as the rung
    arithmetic — if the kit's own loader ever mis-read a `status` or a `phase`, a
    `want` side built on it would agree with the bug. The id UNIVERSE for needs is
    a whole-TEXT scrape, because that is what `sn_all_ids` documents (an approved
    prose mention counts exactly like a row); draft-ness is the `status` FIELD,
    because under TOML it is a field and not section-as-state.

    THE FRAME RUNGS CURRENTLY SHORT-CIRCUIT THE SPINE ONES: every CMP row in this
    repo is Drafted today, so `Arch` is the answer for every phase that gets past
    `Reqs`, and the LLReqs/Tests/Impl arms below are not exercised by the meta
    repo right now. They are written anyway — the expectations must stay correct
    when the partition settles, not only for today's registry state."""
    needs_rel = "docs/requirements/stakeholder-needs.toml"
    sn_text = _meta_text(needs_rel)
    sn_ids = {u for u in _re.findall(r"\bSN-\d+\b", sn_text) if not u.endswith("-000")}
    sn_draft = {
        r["_id"]
        for r in _meta_rows(needs_rel, "need", "SN-")
        if _meta_status(r) == "drafted"
    }

    srs = _meta_rows("docs/requirements/system-requirements.toml", "requirement", "SR-")
    llrs = _meta_rows("docs/requirements/low-level-requirements.toml", "design", "LLR-")
    tcs = _meta_rows("docs/test/test-cases.toml", "test", "TC-")
    bifs = _meta_rows("docs/requirements/external.toml", "boundary", "B-")
    cmps = _meta_rows("docs/requirements/components.toml", "component", "CMP-")
    assert srs, "no SR rows read — the re-derivation would be vacuous"
    assert sn_ids, "no SN ids read — the re-derivation would be vacuous"

    # The three REPO-GLOBAL facts. Each is stated as "anything not settled holds
    # the rung", which is also the module's fail-honest default: an unrecognized
    # maturity caps rather than clears.
    needs_in_work = (not sn_ids) or bool(sn_ids & sn_draft)
    boundary_in_work = (not bifs) or any(_meta_status(r) != "approved" for r in bifs)
    arch_in_work = (not cmps) or any(
        _meta_status(r) not in ("approved", "founded")
        # `standing` is the LIFECYCLE axis; only `active`/`deprecated` clear rung
        # 3, and an ABSENT cell is the declared `active` shorthand.
        or str(r.get("standing") or "active").strip().lower()
        not in ("active", "deprecated")
        for r in cmps
    )
    cited = {x for r in srs for x in _meta_refs(r.get("sn_refs"))}
    uncovered = any(u not in cited for u in sn_ids)

    # The phase buckets, associated BY REFERENCE rather than by the child's own
    # `phase` cell: an LLR belongs to the phase of the SR it decomposes, and a TC
    # that cites only its LLR resolves back through that LLR's SRs.
    sr_phase = {r["_id"]: _meta_phase(r) for r in srs}
    llr_srs = {r["_id"]: _meta_refs(r.get("sr_refs")) for r in llrs}
    buckets = {label: ([], [], []) for label in sr_phase.values()}
    for row in srs:
        buckets[sr_phase[row["_id"]]][0].append(row)
    for row in llrs:
        for label in {sr_phase[s] for s in llr_srs[row["_id"]] if s in sr_phase}:
            buckets[label][1].append(row)
    for row in tcs:
        labels = set()
        for ref in _meta_refs(row.get("verifies")):
            for s in llr_srs.get(ref, [ref]):
                if s in sr_phase:
                    labels.add(sr_phase[s])
        for label in labels:
            buckets[label][2].append(row)

    expect = {}
    for label, (p_srs, p_llrs, p_tcs) in buckets.items():
        if needs_in_work or not p_srs:
            expect[label] = RULES.STAGE_NEEDS
        elif boundary_in_work:
            expect[label] = RULES.STAGE_BOUNDARY
        elif any(_meta_status(r) == "drafted" for r in p_srs):
            expect[label] = RULES.STAGE_REQS
        elif uncovered:
            expect[label] = RULES.STAGE_NEEDS
        elif arch_in_work:
            expect[label] = RULES.STAGE_ARCH
        else:
            answered = {x for r in p_llrs for x in _meta_refs(r.get("sr_refs"))}
            verified = {x for r in p_tcs for x in _meta_refs(r.get("verifies"))}
            if any(
                str(r.get("verification") or "").strip() not in LLR_EXEMPT_METHODS
                and r["_id"] not in answered
                for r in p_srs
            ) or any(_meta_status(r) == "drafted" for r in p_llrs):
                expect[label] = RULES.STAGE_LLREQS
            elif any(r["_id"] not in verified for r in p_srs) or any(
                _meta_status(r) == "drafted" for r in p_tcs
            ):
                expect[label] = RULES.STAGE_TESTS
            else:
                expect[label] = RULES.STAGE_IMPL
    return expect


def test_meta_repo_phases_match_an_independent_derivation():
    # The kit's north star, phase-aware since phase 2 opened (WI-116), re-scoped
    # by WI-316, re-anchored by the adversarial review's F3 and RE-KEYED FROM THE
    # BAR AXIS TO THE STAGE LADDER at WI-498 slice 5. The per-phase values are
    # checked against an INDEPENDENT re-derivation from the raw registry TOML
    # (never against the deriver itself — that comparison could never fail), so a
    # broken rung in `spine_stage` reds the dogfood.
    #
    # THE LIVE READING is the comparable one: it is the same fold over the same
    # rows the retired `_per_phase` did. The SETTLED (draft-excluded) reading is
    # the stage axis's own invention and is driven in tests/test_derive_stage.py.
    #
    # THE CACHE-FRESHNESS HALF OF THIS TEST MOVED WITH ITS FILE. It used to run
    # `--check` against the committed `docs/gate`; that file is deleted, and the
    # successor claim on `docs/stage` is
    # tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current.
    expect = _independent_meta_expectations()
    record = DS.derive(ROOT)
    assert record["per-phase-live"] == expect, (record["per-phase-live"], expect)
    # A deliberate SNAPSHOT of the meta-repo's own derived phase, so a silent
    # phase drift reds here rather than passing unnoticed. Bump it when a
    # approval legitimately advances the phase (4 -> 5 at the 2026-08-13
    # re-attest sitting, which approved the last draft SNs and SR-137..149).
    assert record["phase"] == 5
    # ...and the RETIRED counter is absent from the record. `modified=` left with
    # `is_modified` at D-9 step 7 (a count of a value the closed enum no longer
    # admits is a count of an integrity error, not of a pending state), and the
    # stage record must not quietly grow it back on the new axis.
    assert "modified" not in record


# --- WI-401: the SN-coverage rung ---------------------------------------------
def _append_approved_sn(scaffold, row):
    """Append one table row to the fixture's approved needs table (no draft
    heading above it, so the id is approved by section-as-state — this fixture
    writes the LEGACY markdown carrier)."""
    sn = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(sn.read_text(encoding="utf-8") + row, encoding="utf-8")


def test_uncovered_approved_sn_holds_the_NEEDS_rung(scaffold):
    # WI-401 (owner ruling 2026-08-01): an approved SN cited by zero SR SN-Refs is
    # an unanswered need. RE-KEYED FROM THE BAR AXIS — the claim used to be "the
    # raw level caps at DevStg-Below and the runnable value floors to
    # DevStg-Reqs"; on the stage ladder the same fact reads DIRECTLY, as the rung
    # the work is at: DevStg-Needs. That is strictly more informative than the
    # floored bar was, and it is the same rung the fixture would report for a
    # drafted need — so the second assertion is what keeps the two causes apart
    # (drafted=0 here: the cause is coverage, not a draft).
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    _append_approved_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    assert _stage(scaffold) == RULES.STAGE_NEEDS
    assert DS.derive(scaffold)["drafted"] == 0


def test_covering_the_sn_releases_the_NEEDS_rung(scaffold):
    # The counter-half: citing the need from an SR's SN-Refs releases the rung —
    # the same registry state otherwise climbs to the top rung anything derives.
    # (DevStg-Impl, not DevStg-Release: a fully settled spine reads Impl, because
    # leaving Impl means the declared tests PASS and no cell may claim that.)
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    _append_approved_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    _write(scaffold, srs=_sr("SR-001", sn="SN-001;SN-002"))
    assert _stage(scaffold) == RULES.STAGE_IMPL


def test_example_rows_are_ignored_by_the_coverage_rung(scaffold):
    # -000 rows on BOTH sides of the join are out of scope: an SN-000 placeholder
    # never fires the rung, and an example SR-000 row is filtered before the
    # coverage set is built, so its SN-Refs cannot fake coverage of a real need.
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    _append_approved_sn(scaffold, "| SN-000 | Example placeholder. | M | n/a |\n")
    assert _stage(scaffold) == RULES.STAGE_IMPL
    # A real approved need answered ONLY by an example SR row stays uncovered.
    _append_approved_sn(scaffold, "| SN-002 | Real need. | M | tbd |\n")
    _write(scaffold, srs=_sr("SR-001") + _sr("SR-000", sn="SN-002"))
    assert _stage(scaffold) == RULES.STAGE_NEEDS


def test_per_phase_resolves_tc_citing_only_its_llr(scaffold):
    # Repo-review 2026-07-21 M-6: a Drafted TC citing only its LLR (a legal shape
    # the orphan rules accept) dropped the repo's global reading while the
    # per-phase view stayed green — the phase-drop detector then pointed at
    # nothing. TC refs resolve through the LLR->SR map, so the phase bucket sees
    # it.
    #
    # RE-KEYED TWICE OVER. The per-phase breakdown moved to `derive_stage` with
    # the stage axis, so this reads `per-phase-live`. And the FIXTURE had to be
    # sharpened to stay non-vacuous: on the bar axis one Drafted TC citing only
    # its LLR was enough, but on the rung ladder an SR whose only TC cites the
    # LLR is unverified EITHER WAY, so the bucket would read DevStg-Tests whether
    # or not the resolution worked. So SR-001 is given a properly-citing TC-001
    # first (the control below reads DevStg-Impl), and the LLR-only TC-002 is the
    # single row under test: it can only lower the phase's rung by LANDING IN THE
    # BUCKET AT ALL.
    make_minimal_project(scaffold)
    _no_frame(scaffold)
    llrs = 'LLR-001,SR-001,Adder,src/demo,add,"d",(see TC-001),Approved\n'
    settled_tc = 'TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests,Approved\n'
    _write(
        scaffold,
        srs=_sr("SR-001", status="Approved"),
        llrs=llrs,
        tcs=settled_tc,
    )
    control = DS.derive(scaffold)
    assert control["per-phase-live"]["(default)"] == RULES.STAGE_IMPL

    _write(
        scaffold,
        srs=_sr("SR-001", status="Approved"),
        llrs=llrs,
        tcs=settled_tc + 'TC-002,LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests,Drafted\n',
    )
    assert _stage(scaffold) == RULES.STAGE_TESTS  # the repo-global reading drops...
    result = DS.derive(scaffold)
    assert (
        result["per-phase-live"]["(default)"] == RULES.STAGE_TESTS
    )  # ...and so must the phase view, which is what M-6 found it did not


# --- WI-188: the derived current phase ----------------------------------------
def test_phase_num_digit_parses():
    # The one phase-parse the kit shares: bare integers and vN both digit-parse.
    assert RULES.phase_num({"Phase": "v2"}) == 2
    assert RULES.phase_num({"Phase": "3"}) == 3
    assert RULES.phase_num({"Phase": ""}) is None
    assert RULES.phase_num({"Phase": "later"}) is None
    assert RULES.phase_num({}) is None


def _phased_srs(scaffold):
    """Three SRs at phases 1, 3 and 4, the last one Drafted."""
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        SRS_H.rstrip("\n")
        + ",Phase\n"
        + _sr("SR-001").rstrip("\n")
        + ",1\n"
        + _sr("SR-002").rstrip("\n")
        + ",3\n"
        + _sr("SR-003", status="Drafted").rstrip("\n")
        + ",4\n",
        encoding="utf-8",
    )


def test_derived_current_phase(scaffold):
    # The derived current phase = the highest phase over APPROVED rows; a Drafted
    # in a not-yet-approved higher phase does not bump it. RE-KEYED onto the
    # `phase` field of the stage record, which `derive_stage` computes with
    # `spine_rules.phase_num` over exactly the rows the retired basis line used.
    make_minimal_project(scaffold)
    _phased_srs(scaffold)
    assert DS.derive(scaffold)["phase"] == 3  # SR-003's phase 4 is Drafted, so excluded


def test_derived_phase_none_when_unphased(scaffold):
    # An unphased spine (no Phase column) reads phase=None — a non-adopter is
    # unaffected, exactly like the all-blank --strict-schema case.
    make_minimal_project(scaffold)
    assert DS.derive(scaffold)["phase"] is None


def test_requirement_first_lifecycle_end_to_end(scaffold):
    """The full lifecycle on a fixture: draft a requirement in the LIVE spine,
    then approve -> decompose -> author its test, and watch the derived rung climb
    the ladder, with trace.py clean at the requirement-first step.

    RE-KEYED FROM BARS TO RUNGS (WI-498 slice 5), and the walk got LONGER rather
    than shorter. The bar axis had three runnable values, so the whole climb was
    DevStg-Reqs -> DevStg-Tests -> DevStg-Tests (the ceiling) and the last two
    steps were indistinguishable. The ladder discriminates each missing artifact
    at the rung that artifact belongs to, so the same fixture now walks four
    distinct rungs. The retired `Modified` fixture that step 2 used to carry is
    gone with the word; the claim it made (an approved-but-unblessed row reads at
    the decomposed rung) is pinned exhaustively, `Modified` included, by
    tests/test_approval_level.py::test_NO_status_combination_reaches_the_RELEASE_rung.
    """
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    srs = req / "system-requirements.csv"
    llrs = req / "low-level-requirements.csv"
    tcs = scaffold / "docs" / "test" / "test-cases.csv"

    # 1) Requirement-first: a Drafted SR-002 with no LLR/TC. trace stays clean
    #    (the draft is exempt from the orphan rule) and the derived rung drops to
    #    DevStg-Reqs — a requirement is what is being written.
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Drafted"), encoding="utf-8"
    )
    record_ids(scaffold)
    trace = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert trace.returncode == 0, trace.stdout + trace.stderr
    # The frame registries go only AFTER the trace run: the two inserted rungs are
    # repo-global and sit below every spine rung, so a blank-but-present
    # external.toml would report DevStg-Boundary at every step below and mask the
    # whole climb. trace.py reads them, so it runs first.
    _no_frame(scaffold)
    assert _stage(scaffold) == RULES.STAGE_REQS

    # 2) Approve SR-002 without decomposing it. The requirement rung is cleared and
    #    the rung the MISSING artifact belongs to takes over: an SR with no LLR is
    #    DevStg-LLReqs, because what is being written next is an LLR.
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Approved"), encoding="utf-8"
    )
    assert _stage(scaffold) == RULES.STAGE_LLREQS

    # 3) Decompose: LLR-002 exists, its TC does not. DevStg-Tests.
    llrs.write_text(
        LLRS_H
        + 'LLR-001,SR-001,Adder,src/demo,add,"d",(see TC),Approved\n'
        + 'LLR-002,SR-002,Part,src/demo,two,"d",(see TC),Approved\n',
        encoding="utf-8",
    )
    assert _stage(scaffold) == RULES.STAGE_TESTS

    # 4) Author the test case. Every SR is decomposed and every TC is authored and
    #    non-Drafted, so the test set is LAID and making it pass is the work in
    #    progress: DevStg-Impl, the terminal rung of the derivation.
    tcs.write_text(
        TCS_H
        + 'TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Approved\n'
        + 'TC-002,SR-002;LLR-002,Unit,m,Full,,"e",Yes,tests/test_demo.py::t2,Approved\n',
        encoding="utf-8",
    )
    assert _stage(scaffold) == RULES.STAGE_IMPL

    # ...and NOT DevStg-Release, however settled the cells are. The top rung is
    # evidence-gated and has no producer; a reader seeing DevStg-Impl on a
    # finished-looking spine is being told the truth (WI-498 slice 3).
    assert _stage(scaffold) != RULES.STAGE_RELEASE
