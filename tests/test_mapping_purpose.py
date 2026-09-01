"""TC-204 — the direct test on SR-163 ("Every shipped file maps to a stakeholder
outcome"), owned by WI-543 under OI-72's ruling (docs/log.md 2026-08-31).

SR-163 is mechanism-first: the shipped-file inventory (`bootstrap.MAPPING`) may
carry a requirement reference as a tolerant third element, and a checker
(`gen_arch_map.mapping_purpose_findings`) runs the four finding classes over it
under a declared warn-vs-gate policy. This module proves the CHECKER catches
each of the four classes on a planted scaffold — remove a file, plant a bogus
reference, leave a bare pair, and add a stale exclusion — so the test claims
exactly what it exercises. Its green over the REAL MAPPING is the standing
every-file-maps evidence.
"""

from conftest import ROOT, load_script

bootstrap = load_script("bootstrap")
gen_arch_map = load_script("gen_arch_map")


# ── a tiny synthetic spine the resolver can be graded against, no I/O ──
SR_BY_ID = {
    "SR-900": {"SR-ID": "SR-900", "SN-Refs": "SN-900"},  # resolves to a live need
    "SR-901": {"SR-ID": "SR-901", "SN-Refs": "SN-404"},  # cites a dead need
}
SN_IDS = {"SN-900"}


def _findings_by_class(findings):
    out = {}
    for cls, dst, detail in findings:
        out.setdefault(cls, []).append(dst)
    return out


# ── the tolerant cell ──


def test_mapping_entries_reads_pairs_and_triples_tolerantly():
    entries = bootstrap.mapping_entries()
    # every row normalizes to a 3-tuple; a bare pair yields ref None.
    assert all(len(e) == 3 for e in entries)
    refs = [ref for _s, _d, ref in entries]
    assert None in refs, "a bare pair must survive as ref=None (no flag day)"
    assert any(ref is not None for ref in refs), "the burn-down has begun"


def test_mapping_entries_matches_the_raw_mapping_rows():
    # The reader adds no rows and drops none — it only normalizes arity.
    assert len(bootstrap.mapping_entries()) == len(bootstrap.MAPPING)
    for (src, dst, ref), row in zip(bootstrap.mapping_entries(), bootstrap.MAPPING):
        assert (src, dst) == (row[0], row[1])
        assert ref == (row[2] if len(row) > 2 else None)


# ── the resolver, the SR-163 join in one direction ──


def test_resolve_reference_accepts_a_live_join():
    assert (
        gen_arch_map.resolve_requirement_reference("SR-900", SR_BY_ID, SN_IDS) is None
    )


def test_resolve_reference_rejects_a_missing_sr():
    reason = gen_arch_map.resolve_requirement_reference("SR-404", SR_BY_ID, SN_IDS)
    assert reason and "no live system requirement" in reason


def test_resolve_reference_rejects_an_sr_with_no_live_need():
    reason = gen_arch_map.resolve_requirement_reference("SR-901", SR_BY_ID, SN_IDS)
    assert reason and "no live stakeholder need" in reason


def test_resolve_reference_rejects_an_empty_reference():
    assert gen_arch_map.resolve_requirement_reference("", SR_BY_ID, SN_IDS)


# ── the checker catches each of the four classes, on a planted scaffold ──


def _plant_scaffold():
    """One synthetic inventory carrying exactly one defect of each class, plus a
    clean control row, and the environment facts to grade them against."""
    entries = [
        ("clean.tmpl", "docs/clean", "SR-900"),  # control: mapped + present
        ("bare.tmpl", "docs/bare", None),  # UNMAPPED FILE (bare pair)
        ("bogus.tmpl", "docs/bogus", "SR-404"),  # UNRESOLVED REFERENCE
        ("gone.tmpl", "docs/gone", "SR-900"),  # MISSING FILE (dest absent)
    ]
    present_set = {"docs/clean", "docs/bare", "docs/bogus", "docs/present-exclusion"}
    absences = {
        "docs/present-exclusion": "backfilled; the exclusion is now STALE",
        "docs/legit-absence": "genuinely not shipped here",
        "docs/live-claim": "LIFECYCLE: present only while work is claimed",
    }
    # docs/live-claim is present AND lifecycle-marked — the bite: not stale.
    present_set.add("docs/live-claim")
    findings = gen_arch_map.mapping_purpose_findings(
        entries,
        present=lambda dst: dst in present_set,
        sr_by_id=SR_BY_ID,
        sn_ids=SN_IDS,
        declared_absences=absences,
    )
    return _findings_by_class(findings)


def test_checker_catches_unmapped_file():
    assert "docs/bare" in _plant_scaffold().get("unmapped_file", [])


def test_checker_catches_unresolved_reference():
    assert "docs/bogus" in _plant_scaffold().get("unresolved_reference", [])


def test_checker_catches_missing_file():
    assert "docs/gone" in _plant_scaffold().get("missing_file", [])


def test_checker_catches_stale_entry():
    assert "docs/present-exclusion" in _plant_scaffold().get("stale_entry", [])


def test_checker_clears_the_control_row():
    # The mapped-and-present row raises nothing — no false positive.
    for cls, dsts in _plant_scaffold().items():
        assert "docs/clean" not in dsts, "control row wrongly flagged {}".format(cls)


def test_stale_arm_exempts_the_lifecycle_marker():
    # A present, LIFECYCLE-marked exclusion is a legal state, never stale;
    # a legitimately-absent exclusion never fires either.
    stale = _plant_scaffold().get("stale_entry", [])
    assert "docs/live-claim" not in stale
    assert "docs/legit-absence" not in stale


# ── the declared warn-vs-gate policy ──


def test_policy_is_warn_first_for_the_reference_classes():
    policy = gen_arch_map.MAPPING_FINDING_POLICY
    assert policy["unmapped_file"] == "warn"
    assert policy["unresolved_reference"] == "warn"
    assert policy["missing_file"] == "gate"
    assert policy["stale_entry"] == "gate"


def test_report_gates_only_on_gate_classed_findings():
    # A warn-only inventory passes; one gate-class finding fails it.
    warn_only = [
        ("unmapped_file", "docs/a", "x"),
        ("unresolved_reference", "docs/b", "y"),
    ]
    _lines, ok = gen_arch_map.mapping_purpose_report(warn_only)
    assert ok
    gated = warn_only + [("missing_file", "docs/c", "z")]
    _lines, ok = gen_arch_map.mapping_purpose_report(gated)
    assert not ok


# ── the standing evidence: the checker over the REAL inventory, every run ──


def _real_mapping_findings():
    # Drive the ONE delivered path — the same `mapping_purpose_over_repo` the
    # `--mapping-purpose` CLI mode runs — so the standing evidence and the shipped
    # command grade the real inventory through identical code, not two copies.
    return gen_arch_map.mapping_purpose_over_repo(ROOT)


def test_real_mapping_has_no_gate_class_findings():
    # The every-file-maps standing evidence: over the real MAPPING no missing
    # file and no stale exclusion survives, so the checker passes. Unmapped
    # bare pairs remain (warn-only) — the burn-down, not a failure.
    findings = _real_mapping_findings()
    gate = [
        (cls, dst, detail)
        for cls, dst, detail in findings
        if gen_arch_map.MAPPING_FINDING_POLICY.get(cls) == "gate"
    ]
    assert not gate, "SR-163 gate-class finding(s) over the real MAPPING: {}".format(
        gate
    )


def test_every_filled_reference_resolves():
    # Each reference the burn-down has filled must resolve SR -> live need;
    # an unresolved one is the class the checker exists to surface.
    sr_by_id, sn_ids = gen_arch_map.load_spine_index(ROOT)
    unresolved = []
    for _src, dst, ref in bootstrap.mapping_entries():
        if ref is None:
            continue
        reason = gen_arch_map.resolve_requirement_reference(ref, sr_by_id, sn_ids)
        if reason:
            unresolved.append((dst, ref, reason))
    assert not unresolved, "filled reference(s) do not resolve: {}".format(unresolved)


def test_burndown_has_begun_and_the_baseline_is_measurable():
    # The reference cell is a burn-down: some rows are filled, most remain, and
    # the remaining count is exactly the unmapped-warning tally.
    entries = bootstrap.mapping_entries()
    filled = [e for e in entries if e[2] is not None]
    assert filled, "no reference has been filled — the burn-down has not begun"
    unmapped = [
        dst for cls, dst, _d in _real_mapping_findings() if cls == "unmapped_file"
    ]
    assert len(unmapped) == len(entries) - len(filled)
