"""Pin the gate-policy that trace.py and derive_gate.py each carry to be equal.

The F5 rule lets the kit's scripts duplicate *plumbing* (small CSV/heading loaders)
so each stays an independently-copyable drop-in. But the two files also duplicate
*policy* — which SR Verification methods are LLR-exempt, and what "Draft" means —
and policy disagreement is a false green or false red at a gate, the exact failure
class the kit exists to prevent (repo-review-2026-07-12b.md M1 -> WI-099). These
tests mechanize the "kept in sync" promise the two files used to make only in prose:
import both modules and assert they agree.
"""

from conftest import load_script, make_minimal_project, run_py

TRACE = load_script("trace")
GATE = load_script("derive_gate")


def test_llr_exempt_sets_agree():
    # The one policy set: SR Verification methods that decompose to a TC but no
    # LLR. If one file adds a method to the exempt set and the other does not, the
    # orphan report and the derived gate disagree about what "decomposed" means.
    assert set(TRACE.LLR_EXEMPT) == set(GATE.LLR_EXEMPT)
    assert set(TRACE.LLR_EXEMPT) == {"Analysis", "Inspection", "Attest"}


def test_is_draft_agrees():
    # Both files decide the pre-ratification Draft state (Status open-vocab, only
    # "draft" acts). Pin them equivalent across the casing/whitespace/None battery.
    cases = [
        {"Status": "Draft"},
        {"Status": "draft"},
        {"Status": "  DRAFT  "},
        {"Status": "Verified"},
        {"Status": "Planned"},
        {"Status": ""},
        {"Status": None},
        {},
    ]
    for row in cases:
        assert TRACE.is_draft(row) == GATE.is_draft(row), row


def test_is_verified_agrees():
    # Both files decide the terminal Verified state (the G3 --require-verified
    # criterion in trace.py, the gate derivation in derive_gate.py). Matched
    # case-insensitively — the one Status-casing rule (M3 -> WI-101) — so pin the
    # two equivalent across the same casing/whitespace/None battery as is_draft.
    cases = [
        {"Status": "Verified"},
        {"Status": "verified"},
        {"Status": "  VERIFIED  "},
        {"Status": "Draft"},
        {"Status": "Planned"},
        {"Status": ""},
        {"Status": None},
        {},
    ]
    for row in cases:
        assert TRACE.is_verified(row) == GATE.is_verified(row), row


def test_is_modified_agrees():
    # Both files recognize the post-attestation Modified state (WI-316): trace.py
    # for the chain-consistency warns + the --ratify modified brief, derive_gate.py
    # for the modified=N basis count. Divergence would let a pending re-attest hide
    # from one surface while the other reports it — the same false-green class the
    # is_draft/is_verified pins exist for. Same casing/whitespace/None battery,
    # plus the two sibling magic values (each must read NOT-modified in both).
    cases = [
        {"Status": "Modified"},
        {"Status": "modified"},
        {"Status": "  MODIFIED  "},
        {"Status": "Verified"},
        {"Status": "Draft"},
        {"Status": "Planned"},
        {"Status": ""},
        {"Status": None},
        {},
    ]
    for row in cases:
        assert TRACE.is_modified(row) == GATE.is_modified(row), row
    # The three recognized values are mutually exclusive on any single row.
    for val in ("Modified", "Draft", "Verified"):
        row = {"Status": val}
        assert (
            sum(
                (
                    TRACE.is_draft(row),
                    TRACE.is_verified(row),
                    TRACE.is_modified(row),
                )
            )
            == 1
        ), row


def test_llr_exempt_agrees():
    # Both files decide the LLR-exemption at their own decision point (trace's
    # orphan rule, derive_gate's sr_gate). Review 017 caught them disagreeing on
    # a whitespace-padded valid method (derive_gate stripped, trace did not) —
    # the exact false-green/false-red divergence WI-099 promised away. Pin the
    # predicate equivalent, and pin the padded case to the fixed direction.
    cases = [
        {"Verification": "Analysis"},
        {"Verification": " Analysis "},
        {"Verification": "Inspection"},
        {"Verification": "Attest"},
        {"Verification": "analysis"},  # closed vocab stays case-sensitive
        {"Verification": "Test"},
        {"Verification": ""},
        {"Verification": None},
        {},
    ]
    for row in cases:
        assert TRACE.llr_exempt(row) == GATE.llr_exempt(row), row
    # the 017 case itself: whitespace-padded valid method IS exempt, in both
    assert TRACE.llr_exempt({"Verification": " Analysis "}) is True
    assert GATE.llr_exempt({"Verification": "Attest  "}) is True


def test_require_verified_bar_matches_sr_gate_regardless_of_method(scaffold):
    # WI-259 (repo-review-2026-07-21 M-5): trace's --require-verified G3 bar and
    # derive_gate.sr_gate must agree about which SRs must be Verified before G3.
    # sr_gate has always demanded is_verified for ANY decomposed SR with no
    # per-method carve-out; trace's bar used to fire only for Verification=Test, so
    # a decomposed Demonstration/Analysis/Inspection SR left Implemented could never
    # derive G3 yet passed trace's check — two scripts disagreeing about the gate.
    # Option A widened trace's bar: its loop now gates only on is_draft (skip) then
    # is_verified (pass) and NEVER reads Verification, so it is method-blind exactly
    # like sr_gate. Pin the equivalence on the predicates each side actually uses,
    # across the full Verification vocabulary, so neither re-grows a method filter.
    methods = [
        "Test",
        "Demonstration",
        "Manual",
        "Analysis",
        "Inspection",
        "Attest",
        "Critique",
    ]
    for m in methods:
        implemented = {"Verification": m, "Status": "Implemented"}
        verified = {"Verification": m, "Status": "Verified"}
        # trace's widened bar applies to every ratified (non-Draft) row — the skip
        # is is_draft, which is method-blind — and then passes iff is_verified. So
        # a ratified SR of ANY method flags exactly when it is not Verified.
        assert TRACE.is_draft(implemented) is False, m  # bar applies (ratified)
        assert TRACE.is_draft(verified) is False, m  # bar applies (ratified)
        assert TRACE.is_verified(verified) is True, m  # Verified -> passes
        assert TRACE.is_verified(implemented) is False, m  # not Verified -> flagged
        # sr_gate's G3 for a decomposed SR is the SAME is_verified predicate, also
        # method-blind: Verified reaches G3, Implemented caps at G2 — every method.
        assert GATE.sr_gate(verified, True, True) == GATE.G3, m
        assert GATE.sr_gate(implemented, True, True) == GATE.G2, m
    # A Draft SR is pre-ratification and exempt from BOTH: trace's bar stands down
    # (is_draft True, so the loop `continue`s) and sr_gate returns G0 (below G1).
    draft = {"Verification": "Test", "Status": "Draft"}
    assert TRACE.is_draft(draft) is True
    assert GATE.sr_gate(draft, True, True) == GATE.G0

    # The predicate pins above are necessary but not sufficient: because is_draft/
    # is_verified read Status (not Verification), restoring a Verification=="Test"
    # guard INSIDE analyze()'s --require-verified loop would leave them all green.
    # So drive the real loop end-to-end — a decomposed, non-Test (Demonstration) SR
    # left Implemented MUST produce a status finding. This is the assertion that
    # actually pins the loop side method-blind: restore the Test-only guard and it
    # fails (Demonstration skipped -> status-findings=0 -> exit 0).
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ",M,Demonstration,Implemented"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "status-findings=1" in proc.stdout
    assert "Verification=Demonstration but Status=Implemented" in proc.stdout


def test_sn_draft_ids_agrees():
    # Both files scan stakeholder-needs.md for SNs under a "draft" heading
    # (section-as-state maturity). Pin them equivalent across headings, -000
    # placeholders, and section boundaries.
    texts = [
        "## Draft\nSN-010 something\n## Ratified\nSN-011 done\n",
        "# Needs\nSN-001\n### Draft candidates\nSN-020\nSN-021\n",
        "## DRAFT (in review)\nSN-030 SN-000 SN-031\n",
        "## Ratified only\nSN-040\n",
        "SN-050 no heading at all\n",
        "",
    ]
    for text in texts:
        assert TRACE.sn_draft_ids(text) == GATE.sn_draft_ids(text), text


def test_sn_all_ids_agrees():
    # WI-408 (WI-401 REVIEW-A finding 2): the SN id-UNIVERSE scrape is the third
    # SN policy duplicate in the pair — both files decide WHICH ids the draft and
    # coverage rules run over with the same whole-text scrape, and it was the one
    # duplicate the WI-401 "both surfaces read the same state" promise rested on
    # that no pin held. If the two scrapes diverge, the gate and the itemized
    # listing can disagree about which ids exist — the exact WI-099 class the
    # sn_cited_ids pin exists to prevent. Pin the parse equivalent across prose
    # mentions, table rows, draft sections, -000 placeholders, and empty text.
    texts = [
        "",
        "SN-001 mentioned in prose, no table row at all\n",
        "| SN-002 | a table row |\n\n## Draft\n\nSN-003\n",
        "SN-000 placeholder only\n",
        "## Ratified\n\nSN-004 twice SN-004, then SN-005.\nAnd SN-006#frag.\n",
        "no ids here\n",
    ]
    for text in texts:
        assert TRACE.sn_all_ids(text) == GATE.sn_all_ids(text), text
    # Semantics pins: the scrape is WHOLE-TEXT — a prose-mentioned id is in the
    # universe exactly like a table row (the §2.1 sharp edge: ratified + uncited
    # means the coverage rung caps the gate at G0). Draft-section ids are
    # included (the draft/coverage split happens later, on sn_draft_ids); only
    # -000 placeholders are excluded.
    assert GATE.sn_all_ids("prose SN-010\n## Draft\nSN-011 and SN-000\n") == {
        "SN-010",
        "SN-011",
    }


def test_sn_cited_ids_agrees():
    # WI-401: the SN-coverage rung made SR SN-Refs a GATE input, so "which SN ids
    # do the SRs cite" is policy duplicated across the pair — trace.py's
    # "SN has no SR" orphan listing and derive_gate.py's coverage rung must read
    # the SAME set, or the gate and the itemized findings contradict on one
    # registry state (the exact WI-099 divergence class). Pin the parse
    # equivalent across separators, empties, and absent cells.
    batteries = [
        [],
        [{"SN-Refs": "SN-001"}],
        [{"SN-Refs": "SN-001;SN-002"}, {"SN-Refs": "SN-002, SN-003"}],
        [{"SN-Refs": " SN-004  SN-005 "}],
        [{"SN-Refs": ""}, {"SN-Refs": None}, {}],
        [{"SN-Refs": "SN-000"}],
        [{"SN-Refs": "SN-006", "Status": "Draft"}],
    ]
    for rows in batteries:
        assert TRACE.sn_cited_ids(rows) == GATE.sn_cited_ids(rows), rows
    # Semantics pins: every separator splits; the function filters NOTHING itself.
    # -000 rows are excluded by the CALLER's row filter (compute/analyze), and a
    # Draft SR's citation is deliberately IN the set — the raw-view exemption the
    # double-counting seam manages (derive_gate's ex-draft view re-runs the same
    # parse on the non-draft subset instead of special-casing it here).
    assert GATE.sn_cited_ids([{"SN-Refs": "SN-001;SN-002 SN-003,SN-000"}]) == {
        "SN-001",
        "SN-002",
        "SN-003",
        "SN-000",
    }
    assert TRACE.sn_cited_ids([{"SN-Refs": "SN-006", "Status": "Draft"}]) == {"SN-006"}


def test_the_legacy_ratification_translation_agrees():
    # SN-029. `bootstrap.py` imports no kit sibling — it is the one script an
    # adopter may run from a bare download — so it carries its own copy of the
    # retired gate-authority enum's translation. This is duplicated POLICY, not
    # plumbing: if the migrator and the readers disagreed about what
    # `single-ratify` meant, a repo would scaffold with one posture and run with
    # another, which is precisely the shadowing defect SN-029 removed.
    BOOT = load_script("bootstrap")
    COMMON = load_script("agent_common")
    assert BOOT.LEGACY_RATIFICATION == COMMON.LEGACY_RATIFICATION
    assert set(BOOT.LEGACY_RATIFICATION) == {"attended", "single-ratify", "autonomous"}
    # And the two ends are what the words always meant, stated here so a future
    # edit to either copy has to argue with a named expectation rather than
    # merely keeping two dictionaries equal to each other.
    assert BOOT.LEGACY_RATIFICATION["attended"]["human_ratification_through"] == 4
    assert BOOT.LEGACY_RATIFICATION["autonomous"]["human_ratification_through"] == 0


def test_the_retired_enum_key_is_no_longer_shipped():
    # The shadowing defect, pinned so it cannot come back: the template used to
    # ship BOTH `gate_policy = "attended"` and `human_ratification_through = 4`,
    # and since `ratification_level` prefers the ordinal, every repo that chose
    # a non-default posture scaffolded as fully attended with no diagnostic.
    from conftest import KIT

    text = (KIT / "process.toml.template").read_text(encoding="utf-8")
    declared = [
        ln
        for ln in text.splitlines()
        if ln.strip().startswith("gate_policy") and "=" in ln
    ]
    assert declared == [], declared
    assert "human_ratification_through = 4" in text


def test_sn_field_mapping_agrees_across_all_three_readers(tmp_path):
    # THE TWIN, PINNED. `traj_parse._sn_rows`, `gen_okf.sn_rows` and
    # `trace._sn_prose` each parse stakeholder-needs.md independently. They were
    # held equal by a docstring, drifted once already (one kept `-000`, one did
    # not, rendering a phantom SN-000 root in the dashboard icicle), and nothing
    # in tests/ called any of them.
    #
    # Equality ALONE would be a vacuous green and this test would be theatre: the
    # three were byte-identical AND all three wrong the same way, so
    # `a == b == c` was already True over the real registry while every
    # edge-case row rendered its Lifecycle word as the need. So the battery pins
    # the VALUES too, on a fixture carrying both table shapes — the same
    # equality-plus-absolute-value discipline the rest of this module uses.
    PARSE = load_script("traj_parse")
    OKF = load_script("gen_okf")
    TR = load_script("trace")

    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "stakeholder-needs.md").write_text(
        "## Core needs\n"
        "| SN-ID | Need | Why it matters | Priority | Acceptance intent |\n"
        "|---|---|---|---|---|\n"
        "| SN-000 | example | example | M | example |\n"
        "| SN-001 | **The need** | The why | M | The acceptance |\n"
        "\n## Edge-case expectations\n"
        "| SN-ID | Lifecycle | Scenario | Expected behavior |\n"
        "|---|---|---|---|\n"
        "| SN-002 | Provision | The scenario | The expected behavior |\n",
        encoding="utf-8",
    )
    rows = PARSE._sn_rows(tmp_path)
    assert rows == OKF.sn_rows(tmp_path)
    prose = TR._sn_prose((reg / "stakeholder-needs.md").read_text(encoding="utf-8"))
    assert prose == {r["id"]: {k: v for k, v in r.items() if k != "id"} for r in rows}

    # The `-000` placeholder is skipped by all three — the drift that happened.
    assert [r["id"] for r in rows] == ["SN-001", "SN-002"]

    # Core shape: four content cells, read at their own offsets.
    assert rows[0] == {
        "id": "SN-001",
        "need": "The need",  # `**` stripped
        "why": "The why",
        "priority": "M",
        "acceptance": "The acceptance",
    }
    # Edge-case shape: THREE content cells and no priority column. Pinned by
    # value because this is the mapping that was wrong — `need` must be the
    # Scenario, never the Lifecycle word, and `acceptance` must not be empty.
    assert rows[1] == {
        "id": "SN-002",
        "need": "The scenario",
        "why": "Provision",
        "priority": "n/a",
        "acceptance": "The expected behavior",
    }


def test_sn_edge_case_rows_are_not_titled_by_their_lifecycle_phase(tmp_path):
    # The live regression, stated as itself: for its whole life the edge-case
    # tier rendered `need` = the Lifecycle word, so SN-013 published as
    # "Provision" in docs/okf/ and PROJECT_STATE.html. A future edit that
    # restores fixed-offset indexing passes the equality test above (all three
    # would move together) but fails here.
    PARSE = load_script("traj_parse")
    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "stakeholder-needs.md").write_text(
        "| SN-ID | Lifecycle | Scenario | Expected behavior |\n"
        "|---|---|---|---|\n"
        "| SN-013 | Provision | No Python 3 on PATH | Probe and fail with a remedy |\n",
        encoding="utf-8",
    )
    (row,) = PARSE._sn_rows(tmp_path)
    assert row["need"] != "Provision"
    assert row["need"] == "No Python 3 on PATH"
    assert row["acceptance"] == "Probe and fail with a remedy"
