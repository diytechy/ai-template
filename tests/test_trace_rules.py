"""trace.py — the pure registry-rule decisions, unit-checked in process
(WI-277: split verbatim from tests/test_trace.py by behavior boundary).

The spine-prose predicates (a row states the system not its own history; one
testable obligation; the paraphrase advisory that warns but never gates; the
optional LLR Rationale column), SR supersession integrity incl. WI-364's
superseded-parent rule, the WI-129 LLR/TC status-coherence lint, the WI-146(a)
--ratify hierarchy view, and the WI-081 Slice C render/exit helpers
(_bucket_by_ref pre-indexing + the exit_code gate policy).
"""

from conftest import KIT, load_script, make_minimal_project, run_py


def test_a_spine_row_states_the_system_not_its_own_history():
    # Owner-raised at the first re-attestation sitting, on LLR-050's `WI-316:`
    # changelog prefix: a spine row must be stand-alone — a reader with none of
    # this repo's history reads one row and knows what the system does and why.
    # Provenance has better homes (work-items.csv, the log's Decisions), and the
    # row OBEYS the process rather than citing it.
    from conftest import load_script

    trace = load_script("trace")

    def flags(sr=None, llr=None, tc=None):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.provenance_findings(
            rows(sr, "SR-ID", "SR-101"),
            rows(llr, "LLR-ID", "LLR-101"),
            rows(tc, "TC-ID", "TC-101"),
        )

    # The two token shapes, in the normative cells of all THREE registries — the
    # scope the SR-only version could not see, and where 43 of the 45 rows lived.
    assert flags(sr={"Requirement": "Shall resume (WI-210, one path)."})
    assert flags(sr={"AcceptanceCriteria": "Modified (WI-316) rows re-attest."})
    assert flags(sr={"Rationale": "Re-scoped by WI-210 to one path."})
    assert flags(sr={"Title": "Resume authority (WI-210)"})
    assert flags(llr={"Detail": "WI-316: is_modified recognized."})
    assert flags(llr={"Title": "Derived gate (WI-316)"})
    # The LLR's `Rationale` is normative text like its `Detail`, so the rule
    # reaches it. Without this the new column would be a provenance loophole —
    # exactly the "largest pocket is the layer the rule cannot see" failure the
    # SR-only scope already made once.
    assert flags(llr={"Rationale": "Chosen in WI-300's option (f) ruling."})
    assert flags(llr={"Rationale": "Required by process.md section 3."})
    assert flags(tc={"Method": "Ported from the tracks suite, WI-210."})
    assert flags(tc={"Expected": "Live set as of the WI-314 binding."})
    assert flags(tc={"Parameters": "the 109-character WI-308 clause"})
    assert flags(sr={"Requirement": "The gate derives per process.md section 7."})
    assert flags(llr={"Detail": "See process-options.md 'Phased delivery'."})
    # The NEGATIVE half, and the whole reason the rule can be narrow: 65 SR rows
    # name a script, 6 an artifact path and 5 a rubric, and every one is
    # legitimate — this kit's product IS its scripts, so the name is the system
    # under specification. A rule that fired on those gets scrolled past.
    assert not flags(sr={"Requirement": "trace.py --strict shall exit nonzero."})
    assert not flags(sr={"Requirement": "The derived gate caches to docs/gate."})
    assert not flags(sr={"AcceptanceCriteria": "Judged against docs/rubrics/x.md."})
    assert not flags(llr={"Detail": "gen_trajectory.py renders PROJECT_STATE.html."})
    assert not flags(sr={"Requirement": "Bounded by SR-055; decomposed to LLR-050."})
    assert not flags(tc={"Method": "Run tests/test_trace.py against a scaffold."})
    # Not a WI id merely because the letters occur, and not any .md file.
    assert not flags(sr={"Requirement": "A SWITCH-210 dial selects the tier."})
    assert not flags(llr={"Detail": "Documented in ADOPTING.md section 6."})
    # Pointer columns are out of scope BY DESIGN — they exist to point.
    assert not flags(llr={"Detail": "x", "Module": "wi_210.py", "TestRefs": "WI-210"})
    # A placeholder row never gates a scaffold.
    assert not flags(sr={"SR-ID": "SR-000", "Requirement": "Example (WI-210)."})
    # It reports the registry, the row, the cell and WHAT it cited.
    (msg,) = flags(llr={"Detail": "Resumes (WI-210) per process.md."})
    assert msg.startswith("LLR LLR-101 Detail")
    assert "'WI-210'" in msg and "'process.md'" in msg


def test_a_requirement_states_one_testable_obligation():
    # WI-328. The stand-alone rule says a row must not carry its own HISTORY;
    # this says what is left must be DECIDABLE — 29148's individual-requirement
    # characteristics, restricted to the half a checker settles without judgement.
    from conftest import load_script

    trace = load_script("trace")

    def flags(sr=None, llr=None, tc=None):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.form_findings(
            rows(sr, "SR-ID", "SR-101"),
            rows(llr, "LLR-ID", "LLR-101"),
            rows(tc, "TC-ID", "TC-101"),
        )

    # SINGULAR — measured at 13 of 110, the only pattern with a real population.
    assert flags(sr={"Requirement": "x shall a. y shall b."})
    # UNAMBIGUOUS — 'shall' is the obligation; the rest are goal/permission/fact.
    assert flags(sr={"Requirement": "trace.py should exit nonzero."})
    assert flags(sr={"Requirement": "trace.py shall exit; it will also warn."})
    # VERIFIABLE — an actorless passive names nobody to fail.
    assert flags(sr={"Requirement": "The gate shall be computed at each run."})
    # UNFALSIFIABLE terms and OPEN-ENDED scope, in any registry.
    assert flags(sr={"Requirement": "x shall be robust."})
    assert flags(sr={"AcceptanceCriteria": "Overhead stays minimal."})
    assert flags(llr={"Detail": "Handles the cases, such as a missing file."})
    assert flags(tc={"Expected": "Exit 0, etc."})
    # An LLR decomposes; it does not re-state the obligation a tier below where
    # it is traced.
    assert flags(llr={"Detail": "The loader shall reject a malformed row."})

    # The NEGATIVE half. A correct requirement, and the shapes that look like
    # defects and are not — this is what keeps the rule from crying wolf.
    assert not flags(sr={"Requirement": "trace.py shall exit nonzero on an orphan."})
    # A multi-clause AC enumerates how ONE obligation is checked. 110 rows do
    # this and gating on it would be the check_doc_refs failure again.
    assert not flags(
        sr={
            "Requirement": "trace.py shall join the registries.",
            "AcceptanceCriteria": "--strict exits 0 on a linked chain and 1 when "
            "any SR lacks an LLR, any LLR lacks a parent, or any SN lacks an SR; "
            "the orphan list names each at-fault id.",
        }
    )
    # Passive WITH a named actor is fine — the actor is what was missing.
    assert not flags(
        sr={"Requirement": "The gate shall be computed by derive_gate.py."}
    )
    # ZERO 'shall' is NOT a finding. A placeholder, or a project whose obligation
    # keyword is not the English word "shall", is following a different convention
    # rather than making an error — and this rule ships downstream, where flagging
    # it would red a legitimate scaffold on its first re-sync.
    assert not flags(sr={"Requirement": "x does a."})
    # 'must' likewise: 29148 reserves `shall`, but a repo that standardised on
    # 'must' would have EVERY row flagged, which is the cry-wolf failure.
    assert not flags(sr={"Requirement": "trace.py must exit nonzero."})
    # A Draft row is pre-ratification and process.md §4 already exempts it from
    # the decomposition rules — 'TBD' in a Draft acceptance criterion is what
    # Draft MEANS, so flagging it would break the state's whole purpose.
    assert not flags(
        sr={
            "Status": "Draft",
            "Requirement": "x shall a.",
            "AcceptanceCriteria": "TBD",
        }
    )
    assert flags(
        sr={
            "Status": "Verified",
            "Requirement": "y shall b.",
            "AcceptanceCriteria": "TBD",
        }
    )
    # A Rationale legitimately says 'would' (the consequence of the alternative
    # that lost) and an AC legitimately says 'may' (a permitted outcome), so the
    # modal rule is scoped to Requirement ALONE.
    assert not flags(sr={"Rationale": "Polling would miss a mid-run amendment."})
    assert not flags(sr={"AcceptanceCriteria": "The run may emit either form."})
    # 'minimal' is vague; 'minimum' inside a measured bound is not vocabulary the
    # rule owns, and a placeholder row never gates a scaffold.
    assert not flags(sr={"SR-ID": "SR-000", "Requirement": "Example shall shall."})
    # It reports the registry, the row, the cell, and what it found.
    (msg,) = flags(sr={"Requirement": "x shall a and y shall b."})
    assert msg.startswith("SR SR-101 Requirement carries 2 'shall'")


def test_a_child_that_rewords_its_parent_warns_but_never_gates():
    # WI-328. 'Decompose, don't paraphrase' made visible. Lexical overlap is a
    # HEURISTIC — 38 of 118 LLRs trip it and most are legitimate, which is
    # precisely why it warns forever instead of gating.
    from conftest import load_script

    trace = load_script("trace")

    sr = {
        "SR-ID": "SR-101",
        "Requirement": "The exporter shall write records to a comma separated "
        "values file using an atomic rename.",
    }
    echo = {
        "LLR-ID": "LLR-101",
        "SR-Refs": "SR-101",
        "Detail": "The exporter writes records to a comma separated values file "
        "using an atomic rename.",
    }
    assert trace.paraphrase_advisories([sr], [echo])
    # A real decomposition names the module and the mechanism, so it does NOT
    # trip: the check must reward the thing the process actually asks for.
    real = {
        "LLR-ID": "LLR-102",
        "SR-Refs": "SR-101",
        "Detail": "src/export/io.write_atomic buffers to <path>.tmp then renames; "
        "the temp is removed on any error and the rename is atomic within one "
        "volume.",
    }
    assert not trace.paraphrase_advisories([sr], [real])
    # An SR whose Rationale merely re-words its own Requirement.
    dup = dict(
        sr,
        Rationale="The exporter shall write records to a comma "
        "separated values file using an atomic rename.",
    )
    assert trace.paraphrase_advisories([dup], [])
    assert not trace.paraphrase_advisories(
        [dict(sr, Rationale="A half-written file reads as valid to the next run.")],
        [],
    )
    # And it NEVER gates, whatever it finds — the whole point of the tier.
    findings = trace.Findings()
    for attr in vars(trace.Findings()):
        setattr(findings, attr, None)
    findings.paraphrase = trace.paraphrase_advisories([sr], [echo])
    assert findings.paraphrase


def test_the_llr_carries_a_rationale_column_and_it_is_optional():
    # WI-328. `Detail` was the LLR's ONLY prose cell, so the what, the why, the
    # ruled-out alternatives and the authoring history were structurally forced
    # into one field — measured: 75 of 118 Details under 300 chars, but the 24
    # walls (one over 3,000) all in the rows whose reasons were richest. Rationale
    # is a requirement attribute at EVERY level in 29148; the SR had one and the
    # LLR did not, and that asymmetry was the bug.
    from conftest import ROOT, load_script

    trace = load_script("trace")

    # The column exists in BOTH the shipped template and the kit's own registry.
    # Read through the CARRIER, which is what "the registry has this column"
    # means now: TOML has no header, so the question is whether the key is set
    # — by the template's `-000` schema row, and by at least one live row. The
    # "sits beside Detail" half is retired with the header: key order inside a
    # TOML table carries no meaning, so asserting it would pin a non-fact.
    carrier = load_script("spine_carrier")
    for path in (
        ROOT / "project-trajectory/registries/low-level-requirements.template.toml",
        ROOT / "docs/requirements/low-level-requirements.toml",
    ):
        columns = carrier.columns(path, "LLR-ID")
        assert columns, path  # an empty column set would make this vacuous
        assert "Rationale" in columns, path
        assert "Detail" in columns, path

    # The deliberate asymmetry: required on the SR, optional on the LLR. A short
    # decomposition row's why IS its parent SR's, so requiring one everywhere
    # would manufacture the restatement the column exists to prevent.
    assert "Rationale" in trace.REQUIRED_FIELDS["SR"]
    assert "Rationale" not in trace.REQUIRED_FIELDS["LLR"]

    # Which means an LLR with no Rationale is clean...
    bare = {
        "LLR-ID": "LLR-101",
        "SR-Refs": "SR-1",
        "Title": "t",
        "Module": "m",
        "CodeSymbol": "c",
        "Detail": "d",
        "Status": "Verified",
    }
    assert trace.schema_findings("LLR", [bare]) == []
    # ...and an SR with an empty one is not (zero-to-zero: all 110 carry one).
    sr = {
        "SR-ID": "SR-101",
        "Title": "t",
        "SN-Refs": "SN-1",
        "Requirement": "r",
        "Rationale": "",
        "AcceptanceCriteria": "a",
        "Priority": "1",
        "Verification": "Test",
        "Status": "Verified",
    }
    (found,) = trace.schema_findings("SR", [sr])
    assert "empty required field Rationale" in found

    # A pre-migration registry that lacks the COLUMN entirely still validates —
    # the same graceful path TC's Evidence column documents (ADOPTING.md §6).
    del bare["Detail"]
    legacy = trace.schema_findings("LLR", [bare])
    assert legacy == ["LLR LLR-101 has empty required field Detail"], legacy


def test_duplicate_of_malformed_id_reports_duplicated():
    # WI-106 L4: a malformed id appearing twice must report "duplicated" for its
    # second occurrence, not "malformed" a second time.
    from conftest import load_script

    trace = load_script("trace")
    found = trace.integrity_findings("SR", [{"SR-ID": "SR-bad"}, {"SR-ID": "SR-bad"}])
    assert any("malformed" in f for f in found), found
    assert any("duplicated" in f for f in found), found
    # A well-formed duplicate still reports only "duplicated" (no regression).
    dup = trace.integrity_findings("SR", [{"SR-ID": "SR-001"}, {"SR-ID": "SR-001"}])
    assert dup == ["SR id SR-001 is duplicated"], dup


# --- WI-229: optional SR supersession links ---------------------------------


def test_sr_supersession_integrity_predicate():
    trace = load_script("trace")

    rows = [
        {"SR-ID": "SR-001", "SupersededBy": "SR-002;SR-003"},
        {"SR-ID": "SR-002", "SupersededBy": ""},
        {"SR-ID": "SR-003", "SupersededBy": ""},
    ]
    assert trace.sr_supersession_findings(rows) == []
    # The extension is optional: an adopted registry without the column stays
    # compatible, while every populated-cell failure joins the integrity floor.
    assert trace.sr_supersession_findings([{"SR-ID": "SR-001"}]) == []
    bad = trace.sr_supersession_findings(
        [
            {"SR-ID": "SR-001", "SupersededBy": "SR-002,SR-003"},
            {"SR-ID": "SR-002", "SupersededBy": "SR-004"},
            {"SR-ID": "SR-003", "SupersededBy": "SR-003"},
        ]
    )
    assert any("semicolon-separated" in finding for finding in bad)
    assert any("unknown SR-004" in finding for finding in bad)
    assert any("self-links" in finding for finding in bad)
    assert any("cycle" in finding for finding in bad)
    cycle = trace.sr_supersession_findings(
        [
            {"SR-ID": "SR-001", "SupersededBy": "SR-002"},
            {"SR-ID": "SR-002", "SupersededBy": "SR-001"},
        ]
    )
    assert cycle == ["SR SupersededBy cycle: SR-001 -> SR-002 -> SR-001"]


# --- WI-364: an LLR grounded on a superseded SR is an integrity error ---------


def test_llr_citing_a_superseded_sr_is_an_integrity_finding():
    trace = load_script("trace")

    srs = [
        {"SR-ID": "SR-061", "SupersededBy": "SR-132"},
        {"SR-ID": "SR-062", "SupersededBy": "SR-131;SR-132"},
        {"SR-ID": "SR-131", "SupersededBy": ""},
        {"SR-ID": "SR-132", "SupersededBy": ""},
    ]
    found = trace.sr_supersession_findings(
        srs,
        [
            {"LLR-ID": "LLR-014", "SR-Refs": "SR-061"},
            {"LLR-ID": "LLR-015", "SR-Refs": "SR-062; SR-132"},
            {"LLR-ID": "LLR-016", "SR-Refs": "SR-132"},
        ],
    )
    # The message must name the LLR, the dead SR, and its successor(s) — the
    # remediation is unreadable without all three.
    assert found == [
        "LLR LLR-014 SR-Refs cites superseded SR-061 (SupersededBy SR-132) — "
        "re-ground on the successor or delete the LLR",
        "LLR LLR-015 SR-Refs cites superseded SR-062 (SupersededBy SR-131;SR-132) — "
        "re-ground on the successor or delete the LLR",
    ], found
    # Clean both ways: LLRs grounded only on live SRs, and a registry with no
    # supersession column at all (the optional-extension compatibility contract).
    assert (
        trace.sr_supersession_findings(
            srs, [{"LLR-ID": "LLR-016", "SR-Refs": "SR-131;SR-132"}]
        )
        == []
    )
    assert (
        trace.sr_supersession_findings(
            [{"SR-ID": "SR-061"}, {"SR-ID": "SR-132"}],
            [{"LLR-ID": "LLR-014", "SR-Refs": "SR-061"}],
        )
        == []
    )
    # TC citations of a superseded SR stay legal (the TC-099/TC-133 evidence
    # pattern requires them), so the sweep must not reach the TC registry: the
    # LLR arg defaults empty and no TC rows are ever passed.
    assert trace.sr_supersession_findings(srs) == []


def test_llr_citing_a_superseded_sr_is_strict_integrity(scaffold):
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    rows = srs.read_text(encoding="utf-8").splitlines()
    rows[0] += ",SupersededBy"
    rows[1] += ",SR-002"
    # A real successor row, so the only integrity finding under test is the new
    # one (an unknown target would red the run on its own).
    rows.append(
        'SR-002,Subtraction,SN-001,"The system shall subtract two numbers.",'
        '"Realizes SN-001.","sub(3,1) == 2",,M,Test,Verified,'
    )
    srs.write_text("\n".join(rows) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert (
        "LLR LLR-001 SR-Refs cites superseded SR-001 (SupersededBy SR-002)" in report
    ), report


def test_sr_supersession_failures_are_strict_integrity_findings(scaffold):
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    rows = srs.read_text(encoding="utf-8").splitlines()
    rows[0] += ",SupersededBy"
    rows[1] += ",SR-999"
    srs.write_text("\n".join(rows) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-001 SupersededBy references unknown SR-999" in report


def test_meta_supersession_rows_preserve_the_ratified_evidence_map():
    trace = load_script("trace")
    root = KIT.parent
    # Read through the CARRIER: this reads the KIT'S OWN registries, which are
    # TOML since the cutover (repo-lock D-5), and a csv.DictReader over them
    # would hand back one nonsense row and make the whole map vacuously absent.
    carrier = load_script("spine_carrier")
    srs = carrier.load(root / "docs/requirements/system-requirements.toml", "SR-ID")
    llrs = carrier.load(
        root / "docs/requirements/low-level-requirements.toml", "LLR-ID"
    )
    tcs = carrier.load(root / "docs/test/test-cases.toml", "TC-ID")
    assert srs and llrs and tcs  # a missing registry would make this vacuous

    expected = {
        "SR-037": "SR-067;SR-068;SR-069",
        "SR-038": "SR-070;SR-071;SR-072",
        "SR-044": "SR-073;SR-074;SR-075;SR-076;SR-077;SR-078",
        "SR-045": "SR-079;SR-080;SR-081;SR-082;SR-083",
        "SR-047": "SR-084;SR-085;SR-086",
        "SR-048": "SR-087;SR-088",
        "SR-051": "SR-089;SR-090;SR-091;SR-092",
        "SR-058": "SR-093;SR-094;SR-095",
        "SR-063": "SR-096;SR-097;SR-098",
        "SR-064": "SR-099;SR-100;SR-101",
        "SR-066": "SR-102;SR-103;SR-104;SR-105;SR-106;SR-107;SR-108",
    }
    linked = {row["SR-ID"]: row.get("SupersededBy", "") for row in srs}
    assert {sid: linked[sid] for sid in expected} == expected
    # WI-364: the same call now also reds an LLR grounded on any superseded SR,
    # so passing the live LLRs proves this repo stays green under the new rule.
    assert not trace.sr_supersession_findings(srs, llrs)
    old = set(expected)
    assert not any(old.intersection(trace.refs(row.get("SR-Refs"))) for row in llrs)
    tc99 = next(row for row in tcs if row["TC-ID"] == "TC-099")
    assert set(trace.refs(tc99["Verifies"])) == old


def test_phase5_supersession_rows_preserve_the_ratified_evidence_map():
    """TC-133: the fifteen dispatcher-era SRs superseded at concurrency-
    restructure Phase 5 all link to SR-132 (the local integrator), retain no
    LLR (their machinery was deleted, not re-homed), and are cited by TC-133
    exactly — the TC-099 pattern, re-applied to the deletion phase."""
    trace = load_script("trace")
    root = KIT.parent
    # Read through the CARRIER: this reads the KIT'S OWN registries, which are
    # TOML since the cutover (repo-lock D-5), and a csv.DictReader over them
    # would hand back one nonsense row and make the whole map vacuously absent.
    carrier = load_script("spine_carrier")
    srs = carrier.load(root / "docs/requirements/system-requirements.toml", "SR-ID")
    llrs = carrier.load(
        root / "docs/requirements/low-level-requirements.toml", "LLR-ID"
    )
    tcs = carrier.load(root / "docs/test/test-cases.toml", "TC-ID")
    assert srs and llrs and tcs  # a missing registry would make this vacuous

    phase5 = {
        "SR-061",
        "SR-062",
        "SR-065",
        "SR-095",
        "SR-096",
        "SR-097",
        "SR-098",
        "SR-099",
        "SR-100",
        "SR-101",
        "SR-117",
        "SR-118",
        "SR-119",
        "SR-120",
        "SR-121",
    }
    by_id = {row["SR-ID"]: row for row in srs}
    for sid in sorted(phase5):
        row = by_id[sid]
        assert row.get("SupersededBy", "") == "SR-132", sid
        assert row.get("Title", "").startswith("Superseded: "), sid
        # Inspection is what exempts a machinery-less legacy row from the
        # SR-needs-an-LLR orphan rule (trace.LLR_EXEMPT).
        assert row.get("Verification") == "Inspection", sid
    assert not trace.sr_supersession_findings(srs, llrs)
    assert not any(phase5.intersection(trace.refs(row.get("SR-Refs"))) for row in llrs)
    tc133 = next(row for row in tcs if row["TC-ID"] == "TC-133")
    assert set(trace.refs(tc133["Verifies"])) == phase5


# --- WI-129: LLR/TC status-coherence warn (registry lint) ---------------------
# An LLR reading below Verified while every TC that cites it is Verified is a
# readout drift, not a coverage hole (LLR status is non-gating under the
# derived-gate model). Warn-only; never touches an exit code.


def test_llr_status_coherence_predicate():
    # Done-when 1-3: the coherence predicate itself, unit-level.
    from conftest import load_script

    trace = load_script("trace")

    def warns(llrs, tcs):
        return trace.llr_status_advisories(llrs, tcs)

    impl = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Implemented"}
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Verified"}

    # (1) Implemented LLR, sole citing TC Verified -> exactly the warn.
    found = warns([impl], [ver_tc])
    assert len(found) == 1, found
    assert "LLR LLR-010 reads 'Implemented'" in found[0]
    assert "every citing TC is Verified" in found[0]

    # (1, cont.) Lifting the LLR to Verified silences it.
    assert warns([{**impl, "Status": "Verified"}], [ver_tc]) == []

    # (3) Case-insensitive via the shared is_verified() predicate: a lowercase
    # 'verified' LLR is silent, and a lowercase citing TC still counts as Verified.
    assert warns([{**impl, "Status": "verified"}], [ver_tc]) == []
    assert len(warns([impl], [{**ver_tc, "Status": "verified"}])) == 1

    # (2) Quiet: one citing TC is not Verified -> not "every citing TC".
    planned_tc = {"TC-ID": "TC-011", "Verifies": "LLR-010", "Status": "Planned"}
    assert warns([impl], [ver_tc, planned_tc]) == []

    # (2) Quiet: an LLR with no citing TC is the orphan rules' job, not this lint's.
    assert warns([impl], []) == []


def test_modified_llr_is_exempt_from_the_status_advisory():
    # WI-316: a Modified LLR under fully-Verified TCs is DELIBERATE (a
    # post-attestation amendment awaiting re-attest), so the "lift to Verified"
    # nag must stay silent — it would tell the owner to erase the marker the
    # sitting needs. Mutation proof: the same row as Implemented DOES warn, so
    # the exemption is the Modified value, not a broken lint.
    from conftest import load_script

    trace = load_script("trace")
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Verified"}
    modified = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Modified"}
    assert trace.llr_status_advisories([modified], [ver_tc]) == []
    impl = {**modified, "Status": "Implemented"}
    assert len(trace.llr_status_advisories([impl], [ver_tc])) == 1


def test_modified_chain_advisory_flags_the_orphaned_child():
    # WI-316: a Modified LLR/TC whose owning SR is not flagged is invisible to
    # every re-attest surface (they key off the SR row), so it warns; flipping
    # the owning SR to Modified (or Draft) silences it. The TC path resolves
    # owners through both direct SR cites and cited-LLR SR-Refs.
    from conftest import load_script

    trace = load_script("trace")
    sr_ok = {"SR-ID": "SR-010", "Status": "Verified"}
    sr_mod = {"SR-ID": "SR-010", "Status": "Modified"}
    llr = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Modified"}
    tc = {"TC-ID": "TC-010", "Verifies": "LLR-010", "Status": "Modified"}

    found = trace.modified_chain_advisories([sr_ok], [llr], [tc])
    assert len(found) == 2, found
    assert any("LLR LLR-010 is Modified" in f and "SR-010" in f for f in found)
    assert any("TC TC-010 is Modified" in f and "SR-010" in f for f in found)

    # Flipping the attestation unit silences both; Draft counts as flagged too.
    assert trace.modified_chain_advisories([sr_mod], [llr], [tc]) == []
    sr_draft = {"SR-ID": "SR-010", "Status": "Draft"}
    assert trace.modified_chain_advisories([sr_draft], [llr], [tc]) == []

    # A Verified child never warns — the lint watches Modified children only.
    ok_llr = {**llr, "Status": "Verified"}
    ok_tc = {**tc, "Status": "Verified"}
    assert trace.modified_chain_advisories([sr_ok], [ok_llr], [ok_tc]) == []

    # A TC citing its SR directly resolves the owner without an LLR hop.
    tc_direct = {"TC-ID": "TC-011", "Verifies": "SR-010", "Status": "Modified"}
    assert len(trace.modified_chain_advisories([sr_ok], [], [tc_direct])) == 1
    assert trace.modified_chain_advisories([sr_mod], [], [tc_direct]) == []

    # Adversarial-review F8: the OWNERLESS Modified child is the
    # maximally-invisible case (no SR line to ride, no gate pull, no brief
    # section) — it must warn, not fall through the owners-exist guard.
    orphan_llr = {"LLR-ID": "LLR-020", "SR-Refs": "", "Status": "Modified"}
    ghost_llr = {"LLR-ID": "LLR-021", "SR-Refs": "SR-999", "Status": "Modified"}
    ghost_tc = {"TC-ID": "TC-020", "Verifies": "LLR-999", "Status": "Modified"}
    found_orphans = trace.modified_chain_advisories(
        [sr_ok], [orphan_llr, ghost_llr], [ghost_tc]
    )
    assert len(found_orphans) == 3, found_orphans
    assert all("NO owning SR" in f for f in found_orphans)


def test_modified_chain_advisory_is_warn_only(scaffold):
    # The chain warn joins the shared advisory pipe: loud on stdout, in the
    # report, never an exit-code change even under --strict.
    make_minimal_project(scaffold)
    llr_csv = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv.write_text(
        llr_csv.read_text(encoding="utf-8").replace(",Implemented", ",Modified"),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "LLR LLR-001 is Modified" in proc.stdout
    assert "flip the attestation unit" in proc.stdout


def test_llr_status_advisory_is_warn_only_and_reported(scaffold):
    # Done-when 1+4: the minimal project ships LLR-001 Implemented under a
    # Verified TC-001, so trace emits the warn on stdout and in the report — but
    # it never changes the --strict or --strict-integrity exit code.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING (advisory): LLR LLR-001 reads 'Implemented'" in proc.stdout
    assert "llr-status-advisories=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Status-coherence advisories" in report
    assert "LLR-001 reads 'Implemented'" in report

    # --strict-integrity likewise unaffected (the warn never joins the integrity set).
    proc2 = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr

    # Lifting LLR-001 to Verified silences the warn.
    llr_csv = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv.write_text(
        llr_csv.read_text(encoding="utf-8").replace(",Implemented", ",Verified"),
        encoding="utf-8",
    )
    proc3 = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc3.returncode == 0, proc3.stdout + proc3.stderr
    assert "reads 'Implemented'" not in proc3.stdout
    assert "llr-status-advisories" not in proc3.stdout
    report3 = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "None. No unlifted LLRs, no orphaned Modified chain rows." in report3


# --- WI-146(a): the --ratify batch-scoped ratification hierarchy view ---------
# A generated SN->SR->LLR/TC tree carrying the prose a ratifier needs (Requirement/
# AC, LLR Detail, TC Method/Expected, cited rubric), scoped by an SR-id list or a
# phase tag. A generator mode: it runs no checks and always exits 0.

# An SR with a Phase cell and a rubric citation, still traced to LLR-001/TC-001.
PHASED_RUBRIC_SR = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase\n"
    'SR-001,Addition,SN-001,"The system shall add two numbers.",'
    '"Realizes SN-001.","Judged against docs/rubrics/adder.md",,'
    "M,Critique,Planned,v9\n"
)


def test_ratify_sr_list_emits_prose(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--ratify", "SR-001"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "# Ratification hierarchy" in out and "scope: SR-001" in out
    assert "1 SR(s)" in out
    assert "SR-001" in out and "Addition" in out
    # The stakeholder need's own prose heads its subtree, not a bare SN id
    # (WI-146 REVIEW-A): Need / Why it matters / Acceptance intent from the SN row.
    assert "## SN-001" in out
    assert "**Need.** Add two numbers." in out
    assert "**Why it matters.** Demo." in out
    assert "**Acceptance intent.** add(1,2) gives 3." in out
    assert "The system shall add two numbers." in out  # SR Requirement prose
    assert "Pure function: two numbers -> sum." in out  # LLR Detail prose
    assert "TC-001" in out and "Satisfies SR-001 AcceptanceCriteria" in out  # TC


def test_ratify_phase_scope_and_rubric(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        PHASED_RUBRIC_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--ratify", "v9"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in proc.stdout and "Addition" in proc.stdout
    assert "**Rubrics.** docs/rubrics/adder.md" in proc.stdout
    # A non-matching phase resolves to an empty batch (no crash, exit 0).
    empty = run_py(["scripts/trace.py", "--ratify", "v1"], cwd=scaffold)
    assert empty.returncode == 0
    assert "no SR matched this scope" in empty.stdout


def test_ratify_out_writes_linkable_file(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--ratify", "SR-001", "--out", "docs/ratify/x.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "x.md").read_text(encoding="utf-8")
    assert "# Ratification hierarchy" in written
    assert "The system shall add two numbers." in written
    assert "trace: wrote ratification view" in proc.stdout


# --- WI-081 Slice C: the render/exit extraction + M8 pre-indexing --------------
# The report render/console/exit block moved out of main() into render_report /
# render_console / exit_code (byte-identity pinned by test_trace_golden.py). These
# unit-check the two new pure helpers the golden net does not isolate: the M8
# ref-bucket index and the gate exit-code policy.


def test_bucket_by_ref_groups_preserves_order_and_parses_multi():
    from conftest import load_script

    trace = load_script("trace")
    rows = [
        {"LLR-ID": "LLR-001", "SR-Refs": "SR-001"},
        {"LLR-ID": "LLR-002", "SR-Refs": "SR-002"},
        {"LLR-ID": "LLR-003", "SR-Refs": "SR-001;SR-002"},
    ]
    index = trace._bucket_by_ref(rows, "SR-Refs")
    # Grouped by each referenced id, children kept in input order.
    assert [r["LLR-ID"] for r in index["SR-001"]] == ["LLR-001", "LLR-003"]
    assert [r["LLR-ID"] for r in index["SR-002"]] == ["LLR-002", "LLR-003"]
    # A row whose ref cell names two parents appears under BOTH (cell parsed once).
    assert rows[2] in index["SR-001"] and rows[2] in index["SR-002"]
    # An id nobody references is simply absent (no empty buckets); a blank/absent
    # ref cell contributes nothing.
    assert "SR-999" not in index
    assert trace._bucket_by_ref([{"SR-Refs": ""}, {"SR-Refs": None}], "SR-Refs") == {}


def _findings_stub(trace, **overrides):
    """A Findings bag with every attribute exit_code reads defaulted to empty."""
    f = trace.Findings()
    for attr in (
        "orphans",
        "status_findings",
        "integrity",
        "placeholders",
        "schema",
        "budget_findings",
        "module_findings",
        "component_findings",
        "interface_backlink_findings",
    ):
        setattr(f, attr, [])
    for attr, value in overrides.items():
        setattr(f, attr, value)
    return f


def test_exit_code_gate_policy():
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    # --strict fails on any gated finding (orphans here)...
    orphaned = _findings_stub(trace, orphans=["SR-002 has no test (TC)"])
    assert trace.exit_code(orphaned, ns(strict=True)) == 1
    # ...and on integrity (integrity is in the strict set too).
    bad_id = _findings_stub(trace, integrity=["SR id SR-001 is duplicated"])
    assert trace.exit_code(bad_id, ns(strict=True)) == 1
    # --strict-integrity fails on integrity...
    assert trace.exit_code(bad_id, ns(strict_integrity=True)) == 1
    # ...but the integrity floor ignores orphans (a gate criterion, not always-invalid).
    assert trace.exit_code(orphaned, ns(strict_integrity=True)) == 0
    # No gating flag -> always 0, even with findings present.
    loud = _findings_stub(trace, orphans=["x"], integrity=["y"], status_findings=["z"])
    assert trace.exit_code(loud, ns()) == 0
