"""trace.py — the pure registry-rule decisions, unit-checked in process
(WI-277: split verbatim from tests/test_trace.py by behavior boundary).

The spine-prose predicates (a row states the system not its own history; one
testable obligation; the paraphrase advisory that warns but never gates; the
optional LLR Rationale column), the WI-129 LLR/TC status-coherence lint, the WI-146(a)
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
    # A Drafted row is pre-ratification and process.md §4 already exempts it from
    # the decomposition rules — 'TBD' in a Drafted acceptance criterion is what
    # Drafted MEANS, so flagging it would break the state's whole purpose.
    assert not flags(
        sr={
            "Status": "Drafted",
            "Requirement": "x shall a.",
            "AcceptanceCriteria": "TBD",
        }
    )
    assert flags(
        sr={
            "Status": "Approved",
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
        "Status": "Approved",
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
        "Status": "Approved",
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


# --- WI-129: LLR/TC status-coherence warn (registry lint) ---------------------
def test_llr_status_coherence_predicate():
    # Done-when 1-3: the coherence predicate itself, unit-level.
    from conftest import load_script

    trace = load_script("trace")

    def warns(llrs, tcs):
        return trace.llr_status_advisories(llrs, tcs)

    # RE-POINTED AT D-9 STEP 5, NOT DROPPED: this lint's subject is a
    # BELOW-APPROVED LLR, and the fold left exactly one such value (`Drafted`),
    # so the fixture moves onto it rather than onto the `Approved` the raw value
    # map would have produced — which would have made the test assert its own
    # negative case.
    impl = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Drafted"}
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Approved"}

    # (1) Drafted LLR, sole citing TC Approved -> exactly the warn.
    found = warns([impl], [ver_tc])
    assert len(found) == 1, found
    assert "LLR LLR-010 reads 'Drafted'" in found[0]
    assert "every citing TC is Approved" in found[0]

    # (1, cont.) Lifting the LLR to Approved silences it.
    assert warns([{**impl, "Status": "Approved"}], [ver_tc]) == []

    # (3) Case-insensitive via the shared is_approved() predicate: a lowercase
    # 'approved' LLR is silent, and a lowercase citing TC still counts as approved.
    assert warns([{**impl, "Status": "approved"}], [ver_tc]) == []
    assert len(warns([impl], [{**ver_tc, "Status": "approved"}])) == 1

    # (2) Quiet: one citing TC is not Approved -> not "every citing TC".
    planned_tc = {"TC-ID": "TC-011", "Verifies": "LLR-010", "Status": "Drafted"}
    assert warns([impl], [ver_tc, planned_tc]) == []

    # (2) Quiet: an LLR with no citing TC is the orphan rules' job, not this lint's.
    assert warns([impl], []) == []


def test_modified_llr_is_exempt_from_the_status_advisory():
    # WI-316: a Modified LLR under fully-Approved TCs is DELIBERATE (a
    # post-approval amendment awaiting re-attest), so the "lift to Approved"
    # nag must stay silent — it would tell the owner to erase the marker the
    # sitting needs. Mutation proof: the same row as Drafted DOES warn, so
    # the exemption is the Modified value, not a broken lint.
    from conftest import load_script

    trace = load_script("trace")
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Approved"}
    modified = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Modified"}
    assert trace.llr_status_advisories([modified], [ver_tc]) == []
    impl = {**modified, "Status": "Drafted"}
    assert len(trace.llr_status_advisories([impl], [ver_tc])) == 1


def test_llr_status_advisory_is_warn_only_and_reported(scaffold):
    # Done-when 1+4: a below-`Approved` LLR-001 under an `Approved` TC-001 makes
    # trace emit the warn on stdout and in the report — but it never changes the
    # --strict or --strict-integrity exit code.
    #
    # THE FIXTURE IS SET HERE RATHER THAN SHIPPED BY `make_minimal_project`
    # (D-9 step 5). The shared project used to ship `Planned`, which was
    # below-`Verified` AND non-capping; the fold left one below-approval value
    # (`Drafted`) and that one DOES cap the derived gate, so leaving it in the
    # shared fixture would have dropped the gate for every test built on it.
    make_minimal_project(scaffold)
    llr_csv0 = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv0.write_text(
        llr_csv0.read_text(encoding="utf-8").replace(
            ",(see TC),Approved", ",(see TC),Drafted"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING (advisory): LLR LLR-001 reads 'Drafted'" in proc.stdout
    assert "llr-status-advisories=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Status-coherence advisories" in report
    assert "LLR-001 reads 'Drafted'" in report

    # --strict-integrity likewise unaffected (the warn never joins the integrity set).
    proc2 = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr

    # Lifting LLR-001 to Approved silences the warn.
    llr_csv = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv.write_text(
        llr_csv.read_text(encoding="utf-8").replace(",Drafted", ",Approved"),
        encoding="utf-8",
    )
    proc3 = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc3.returncode == 0, proc3.stdout + proc3.stderr
    assert "reads 'Drafted'" not in proc3.stdout
    assert "llr-status-advisories" not in proc3.stdout
    report3 = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "None. No unlifted LLRs." in report3


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
    "M,Critique,Approved,v9\n"
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
    # A non-matching phase is REFUSED, not rendered empty (D-9 §F2). Until this
    # hardening it fell through to a brief that read "there is nothing to
    # ratify" at exit 0 — the most expensive way for this tool to be wrong,
    # because a typo, a retired phase tag or an unknown reserved word all
    # produced a document a human then signed.
    empty = run_py(["scripts/trace.py", "--ratify", "v1"], cwd=scaffold)
    assert empty.returncode != 0
    combined = empty.stdout + empty.stderr
    assert "matches no SR" in combined and "refusing to emit an empty" in combined
    # ...and NOTHING is written to stdout: the old behaviour emitted a document
    # whose own body said "no SR matched this scope", which is a brief a human
    # can read and act on. A refusal must leave no artifact at all.
    assert empty.stdout == ""


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
        "frame_backlink_findings",
        "provenance",
        "form",
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


# --- Re-tier v2 R2/R3: the two warn-first tiering detectors -------------------
# Owner ruling 2026-08-15 (log `2026-08-15p`). Both report a TIERING smell — a
# requirement that decided which artifact carries a capability, and a row whose
# fan of children says it merged several decisions — and both stay advisory
# forever, because clearing them means re-writing requirements, which is the
# campaign's schedule and not the checker's.


def test_a_row_stating_two_verification_methods_warns():
    """The verification-coherence lint (log `2026-08-16p`). The occasion: two
    rows flipped `Critique`->`Test` when their anchors were bound to tests, and
    their prose went on demanding an APPROVE verdict from rubrics that by then
    declared themselves RETIRED. Every strict gate passed at rc=0 for three
    weeks, because nothing compared the `Verification` field against the prose
    that says how anyone would know the row is satisfied."""
    trace = load_script("trace")

    # The defect, in both cells that can carry it.
    ac_rot = {
        "SR-ID": "SR-101",
        "Verification": "Test",
        "AcceptanceCriteria": "A fresh CRITIQUE session returns APPROVE citing "
        "numbered anchors.",
    }
    rationale_rot = {
        "SR-ID": "SR-102",
        "Verification": "Test",
        "Rationale": "Acceptance is adjudicated by an independent critical eye "
        "against a written rubric instead.",
    }
    assert len(trace.verification_coherence_advisories([ac_rot])) == 1
    assert len(trace.verification_coherence_advisories([rationale_rot])) == 1
    assert "AcceptanceCriteria" in trace.verification_coherence_advisories([ac_rot])[0]
    assert "Rationale" in trace.verification_coherence_advisories([rationale_rot])[0]

    # A row that DECLARES Critique is naming its own instrument, not contradicting
    # itself — the lint runs one direction only.
    assert (
        trace.verification_coherence_advisories(
            [dict(ac_rot, **{"Verification": "Critique"})]
        )
        == []
    )

    # The NEGATIVE half, and the reason the vocabulary is case-split: lowercase
    # "verdict"/"approve" are ordinary prose the corpus really uses (SR-137 and
    # SR-148 both say "the integrator's verdict gate" about a subsystem), so
    # matching them case-insensitively would put standing false accusations on
    # correct rows and teach an author to skip the pipe.
    for prose in (
        "Refusals fire at the integrator's verdict gate and intake's adjudication arm.",
        "The owner approves the split before it lands.",
    ):
        clean = {"SR-ID": "SR-103", "Verification": "Test", "Rationale": prose}
        assert trace.verification_coherence_advisories([clean]) == []

    # `Requirement` is deliberately NOT scanned: SR-040's shall enumerates the
    # session phases a coordinator routes (PLAN/BUILD/.../CRITIQUE), where the
    # word NAMES a phase rather than claiming a verdict.
    phase_list = {
        "SR-ID": "SR-104",
        "Verification": "Test",
        "Requirement": "The coordinator shall route each phase "
        "(PLAN/BUILD/REVIEW-A/CRITIQUE) through its declared template.",
    }
    assert trace.verification_coherence_advisories([phase_list]) == []

    # A row with no declared method cannot contradict one.
    assert (
        trace.verification_coherence_advisories([dict(ac_rot, **{"Verification": ""})])
        == []
    )
    # A `-000` example row is a blank form, not a requirement.
    assert (
        trace.verification_coherence_advisories([dict(ac_rot, **{"SR-ID": "SR-000"})])
        == []
    )


def test_a_requirement_that_names_a_concrete_artifact_warns():
    from conftest import load_script

    trace = load_script("trace")

    # A bare script name and a path-qualified one both read as one artifact
    # binding stated in the tier that has no business holding it.
    bare = {
        "SR-ID": "SR-101",
        "Requirement": "trace.py shall exit nonzero when an orphan exists.",
    }
    pathed = {
        "SR-ID": "SR-102",
        "Requirement": "The harness shall run scripts/check.py at every commit.",
    }
    assert len(trace.sr_artifact_advisories([bare])) == 1
    assert len(trace.sr_artifact_advisories([pathed])) == 1
    assert "'trace.py'" in trace.sr_artifact_advisories([bare])[0]
    assert "'scripts/check.py'" in trace.sr_artifact_advisories([pathed])[0]

    # The NEGATIVE half, and the reason the rule can be this cheap: the signal is
    # the literal `.py` EXTENSION, never the letters. A word that merely ends in
    # "py" is not an artifact, and a rule that said otherwise would fire on
    # ordinary English and get scrolled past (the check_doc_refs lesson).
    for word in ("numpy", "happy", "occupy", "copy"):
        clean = {
            "SR-ID": "SR-103",
            "Requirement": "The delivered harness shall be {} to run.".format(word),
        }
        assert trace.sr_artifact_advisories([clean]) == []
    # Capability voice — the wording R2 asks for — is silent.
    assert (
        trace.sr_artifact_advisories(
            [
                {
                    "SR-ID": "SR-104",
                    "Requirement": "The delivered harness shall refuse a commit "
                    "whose registries carry an orphan.",
                }
            ]
        )
        == []
    )
    # A `-000` example row is a blank form, not a requirement.
    assert trace.sr_artifact_advisories([dict(bare, **{"SR-ID": "SR-000"})]) == []


def test_a_recorded_waiver_silences_the_row_but_not_a_shared_artifact():
    from conftest import load_script

    trace = load_script("trace")

    waived = {
        "SR-ID": "SR-101",
        "Requirement": "trace.py shall exit nonzero when an orphan exists.",
        "Rationale": "One-shall waiver (13v): the carrier and the name it "
        "verifies are one contract, and splitting them separates a claim from "
        "the proof that makes it checkable.",
    }
    # The recorded per-row valve — the SAME token the one-`shall` waivers use,
    # not a second grammar an author has to learn.
    assert trace.sr_artifact_advisories([waived]) == []
    # An unwaived row with the same text is not silenced, so the suppression is
    # the Rationale's doing and not an accident of the token regex.
    assert trace.sr_artifact_advisories(
        [{k: v for k, v in waived.items() if k != "Rationale"}]
    )

    # The SECOND census, deliberately not folded into the first: two rows sharing
    # one artifact identity is a different defect (R1's "one home per method"),
    # and a waiver excusing one row's naming says nothing about it — so WAIVED
    # ROWS STILL COUNT here.
    other = {
        "SR-ID": "SR-102",
        "Requirement": "The launcher shall invoke trace.py before every push.",
    }
    shared = [
        a for a in trace.sr_artifact_advisories([waived, other]) if "all name" in a
    ]
    assert len(shared) == 1
    assert "SR-101" in shared[0] and "SR-102" in shared[0] and "'trace.py'" in shared[0]
    # One row naming one artifact is not a shared identity.
    assert [a for a in trace.sr_artifact_advisories([other]) if "all name" in a] == []


def test_the_fanout_detector_fires_past_the_declared_bound_only():
    from conftest import load_script

    trace = load_script("trace")
    # The bound is DECLARED on the rule's own module (trace.py re-exports the
    # predicates, never the dial — a second name for one number is how two
    # bounds start disagreeing).
    trace_text = load_script("trace_text")

    # A DECLARED DIAL of the TOP_VIEW_MAX family, not a hard cap.
    assert trace_text.SR_FANOUT_MAX == 7

    sr = {"SR-ID": "SR-101", "Requirement": "The harness shall report coverage."}

    def children(n):
        return [
            {"LLR-ID": "LLR-{:03d}".format(i), "SR-Refs": "SR-101"}
            for i in range(1, n + 1)
        ]

    # AT the bound is silent; one past it warns. The boundary is the whole
    # contract of a declared number, so it is asserted from both sides.
    assert trace.sr_fanout_advisories([sr], children(trace_text.SR_FANOUT_MAX)) == []
    over = trace.sr_fanout_advisories([sr], children(trace_text.SR_FANOUT_MAX + 1))
    assert len(over) == 1
    assert "SR-101" in over[0] and "8 direct LLR children" in over[0]
    assert "declared bound of 7" in over[0] and "not a cap" in over[0]
    # A downstream project declares its own bound without editing the rule.
    assert trace.sr_fanout_advisories([sr], children(9), bound=20) == []

    # The per-row escape is a RE-STAMP with a stated reason, matched
    # case-insensitively as the multi-word phrase authors actually write.
    stamped = dict(
        sr,
        Rationale="Fan-out re-stamp: the eight children are one observable "
        "class each, and merging any two would hide a distinct failure mode.",
    )
    assert trace.sr_fanout_advisories([stamped], children(8)) == []
    # An unrelated Rationale does not silence it.
    assert trace.sr_fanout_advisories(
        [dict(sr, Rationale="Coverage is the only honest readout.")], children(8)
    )
    # Children are counted per DIRECT parent ref: an LLR under another SR is not
    # this row's fan-out.
    elsewhere = [
        {"LLR-ID": "LLR-{:03d}".format(i), "SR-Refs": "SR-999"} for i in range(9)
    ]
    assert trace.sr_fanout_advisories([sr], elsewhere) == []


def test_the_two_tiering_detectors_warn_but_never_gate():
    # Mirrors the paraphrase advisory's never-gates half. Warn-first is the
    # RULING, not an implementation convenience: the live registries trip both
    # today (seven fan-out offenders, several rows naming a script), and a gate
    # that is red on the day it ships is a gate someone turns off.
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    for attr in ("sr_artifact_advis", "sr_fanout_advis"):
        loud = _findings_stub(trace, **{attr: ["SR-101 tripped the detector"]})
        # Under the LOUDEST flag the kit has, and under the always-on integrity
        # floor, and with no flag at all: still 0.
        assert trace.exit_code(loud, ns(strict=True)) == 0
        assert trace.exit_code(loud, ns(strict_integrity=True)) == 0
        assert trace.exit_code(loud, ns()) == 0


# --- Re-tier v2 R4: ThisProject is derivable, so first prove it agrees --------
# Owner ruling 2026-08-15 (log `2026-08-15p`), slice S5. `ThisProject` dies once
# it is derivable as owner -> LLR -> `Module` (wi455 owns the removal); a cell can
# be deleted as REDUNDANT but not while its two spellings still DISAGREE, so this
# advisory runs first and makes the disagreements visible.

_LLR = {"LLR-014": "project-trajectory/scripts/check_perf.py"}


def _if_row(**over):
    row = {
        "IF-ID": "IF-101",
        "Direction": "Provides",
        "ThisProject": "scripts/check_perf",
        "Counterpart": "scripts/check",
        "Owner": "LLR-014",
    }
    row.update(over)
    return row


def test_an_endpoint_that_disagrees_with_its_owner_llrs_module_warns():
    from conftest import load_script

    trace = load_script("trace")
    llrs = [{"LLR-ID": k, "Module": v} for k, v in _LLR.items()]

    # A `Provides` row: the owner answers for THIS side, and this side names a
    # different module than the owner LLR implements — so the derivation R4 rests
    # on would silently change the row's meaning.
    fires = trace.if_this_project_advisories(
        [_if_row(ThisProject="scripts/derive_gate")], llrs
    )
    assert len(fires) == 1
    assert "IF-101" in fires[0] and "ThisProject='scripts/derive_gate'" in fires[0]
    assert "LLR-014" in fires[0] and "check_perf.py" in fires[0]
    assert "derivable as owner→LLR→module" in fires[0]
    assert "wi455" in fires[0] and "warn-only, never the exit code" in fires[0]
    # THE FINDING NAMES THE CELL IT ACTUALLY COMPARED (S6 second-read M7). On a
    # `Provides` row that cell IS `ThisProject`, so the derivation claim and the
    # comparison agree — the case that made the old wording look right everywhere.
    assert "ThisProject is the endpoint this owner answers for" in fires[0]

    # AGREEMENT IS SILENT IN BOTH SPELLINGS — the arch-map short form and the full
    # repo path with its extension are one module, and a rule that read them as two
    # would report every correctly-filed row in the registry.
    assert trace.if_this_project_advisories([_if_row()], llrs) == []
    assert (
        trace.if_this_project_advisories(
            [_if_row(ThisProject="project-trajectory/scripts/check_perf.py")], llrs
        )
        == []
    )
    # A `;`-joined cell matches on ANY endpoint: a bundle naming the owner's module
    # among several is filed correctly, not misfiled.
    assert (
        trace.if_this_project_advisories(
            [_if_row(ThisProject="scripts/derive_gate; scripts/check_perf")], llrs
        )
        == []
    )


def test_a_bundle_moduled_owner_matches_on_any_of_its_modules():
    from conftest import load_script

    trace = load_script("trace")
    # THE OWNER SIDE SPLITS ON `;` TOO (log 2026-08-17e): an LLR whose `Module`
    # cell bundles several modules (the live LLR-035 names three) matches an
    # endpoint naming ANY one of them. Before the fix the whole cell went
    # through `norm_module` unsplit, so a bundle-moduled owner could NEVER
    # match its endpoint — the docstring promised the split, the code did not.
    llrs = [
        {
            "LLR-ID": "LLR-014",
            "Module": "project-trajectory/scripts/check_perf.py;"
            "project-trajectory/scripts/derive_gate.py",
        }
    ]
    # Provides: `ThisProject` names one module of the bundle — silent.
    assert trace.if_this_project_advisories([_if_row()], llrs) == []
    # Consumes (the live IF-088 shape): `Counterpart` names one — silent.
    consuming = _if_row(
        Direction="Consumes",
        ThisProject="scripts/trunk_step",
        Counterpart="scripts/derive_gate",
    )
    assert trace.if_this_project_advisories([consuming], llrs) == []
    # An endpoint naming NONE of the bundle's modules still fires.
    fires = trace.if_this_project_advisories(
        [_if_row(ThisProject="scripts/trace")], llrs
    )
    assert len(fires) == 1
    assert "IF-101" in fires[0] and "check_perf.py;" in fires[0]


def test_the_derivability_advisory_ranges_over_llr_owned_module_endpoints_only():
    from conftest import load_script

    trace = load_script("trace")
    llrs = [{"LLR-ID": k, "Module": v} for k, v in _LLR.items()]

    # An SR owner names no module, so nothing is derivable and nothing disagrees.
    assert (
        trace.if_this_project_advisories(
            [_if_row(Owner="SR-014", ThisProject="scripts/derive_gate")], llrs
        )
        == []
    )
    # A dangling owner is `if_ownership_advisories`' finding ("Owner references
    # unknown LLR-999"), and reporting it twice under two headings would make one
    # defect look like two.
    assert (
        trace.if_this_project_advisories(
            [_if_row(Owner="LLR-999", ThisProject="scripts/derive_gate")], llrs
        )
        == []
    )
    # NON-MODULE ENDPOINTS ARE NOT A DISAGREEMENT — they are wi455's
    # counterpart-transform business (45 of 122 counterparts are non-module facts).
    for endpoint in (
        "docs/requirements/performance-budgets.csv",
        "docs/gate",
        "external:downstream adopter",
        "agent CLI",
        ".github/workflows/check.yml",
    ):
        assert (
            trace.if_this_project_advisories([_if_row(ThisProject=endpoint)], llrs)
            == []
        ), endpoint
    # An owner LLR with no Module cell is the required-field rule's finding.
    assert (
        trace.if_this_project_advisories(
            [_if_row(ThisProject="scripts/derive_gate")], [{"LLR-ID": "LLR-014"}]
        )
        == []
    )
    # A `-000` example row is a blank form, not a seam.
    assert (
        trace.if_this_project_advisories(
            [_if_row(**{"IF-ID": "IF-000", "ThisProject": "scripts/derive_gate"})], llrs
        )
        == []
    )


def test_a_consumes_row_is_answered_for_on_the_counterpart_side():
    from conftest import load_script

    trace = load_script("trace")
    llrs = [{"LLR-ID": k, "Module": v} for k, v in _LLR.items()]

    # THE SIDE THE OWNER ANSWERS FOR IS THE PROVIDING SIDE (Q2, 2026-08-15): a
    # `Consumes` row is a coverage declaration written from the consumer's
    # viewpoint, so its `ThisProject` is the CONSUMER and the owner's module is in
    # `Counterpart`. Reading `ThisProject` here would invert the whole rule.
    consuming = _if_row(
        Direction="Consumes",
        ThisProject="scripts/derive_gate",
        Counterpart="scripts/check_perf",
    )
    assert trace.if_this_project_advisories([consuming], llrs) == []
    mismatched = dict(consuming, Counterpart="scripts/spine_carrier")
    fires = trace.if_this_project_advisories([mismatched], llrs)
    assert len(fires) == 1
    assert "Counterpart='scripts/spine_carrier'" in fires[0]
    # AND THE FINDING SAYS SO (S6 second-read M7). The message used to compare
    # `Counterpart` while asserting that `this_project` was thereby derivable —
    # true only under the OTHER, still-unruled reading of `Owner`, and on 30 live
    # rows the exact inverse of the truth: there `ThisProject` is the CONSUMER,
    # which no owner→LLR→module derivation reaches. The comparison was never
    # wrong; the sentence about it was, and a sitting reads the sentence.
    assert "Counterpart is the endpoint this owner answers for" in fires[0]
    assert "this_project is derivable" not in fires[0]
    # A Direction outside the closed vocabulary decides no side: the enum rule owns
    # that row, and guessing a side would report a disagreement nobody declared.
    assert (
        trace.if_this_project_advisories([dict(mismatched, Direction="")], llrs) == []
    )


def test_the_derivability_advisory_warns_but_never_gates():
    # The same never-gates half the S2 detectors carry, for the same reason: the
    # live registry trips it today, and clearing it means re-pointing owners across
    # the corpus — the campaign's schedule, not the checker's.
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    loud = _findings_stub(
        trace, if_this_project_advis=["IF-101 disagrees with its owner"]
    )
    assert trace.exit_code(loud, ns(strict=True)) == 0
    assert trace.exit_code(loud, ns(strict_integrity=True)) == 0
    assert trace.exit_code(loud, ns()) == 0
