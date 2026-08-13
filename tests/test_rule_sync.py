"""Pin the gate-policy that trace.py and derive_gate.py each carry to be equal.

The F5 rule lets the kit's scripts duplicate *plumbing* (small CSV/heading loaders)
so each stays an independently-copyable drop-in. But the two files also duplicate
*policy* — which SR Verification methods are LLR-exempt, and what "Draft" means —
and policy disagreement is a false green or false red at a gate, the exact failure
class the kit exists to prevent (repo-review-2026-07-12b.md M1 -> WI-099). These
tests mechanize the "kept in sync" promise the two files used to make only in prose:
import both modules and assert they agree.

THE F5 RULE'S LIVE HOME, AND THE ANTI-DRIFT TOOL OF RECORD (owner ruling
2026-08-10, repo-lock D-7; executed WI-426). F5 is the kit's standing ruling
(owner, 2026-07-12) that a shared `_kitcommon.py` is REJECTED: each kit script
must stay stdlib-only and independently copy-able, so small stable helpers —
`_utf8_console`, the one-line declared-policy readers, argparse/exit
scaffolding, the spec-folder registry reader — are duplicated on purpose. That
ruling used to be stated in the duplication census's header (`docs/dupes-allow`,
read by `check_dupes.py`), which BOUNDED the duplication by fingerprinting every
sanctioned block. D-7 tore the census down: one real catch at the one-time
triage and none since, structurally blind to a DIVERGED copy (which is the
dangerous case, and no longer an identical token block), and 93% of its lines
registering accepted idioms.

So the ruling now reads, in full:

  * duplicated PLUMBING is accepted UNBOUNDED — no census, no allowlist, no
    count. This was its de-facto state anyway; the census recorded it rather
    than restraining it.
  * duplicated POLICY requires a BEHAVIOURAL PIN IN THIS FILE. A second copy of
    a decision — what counts as Draft, which methods are LLR-exempt, what a
    tier's table looks like — is licensed only once these tests assert the
    copies agree BY VALUE. Equality alone can be vacuous — the `_sn_fields`
    case proved it — so pin the value, not just the sameness.

`tests/test_wi_loader_sync.py` is the same instrument aimed at the WI-registry
readers; extend either rather than reaching for a new census.
"""

from conftest import KIT, ROOT, load_script, make_minimal_project, run_py

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


# --- the spine carrier vocabulary ---------------------------------------------
# THREE modules now encode the same carrier: trace.py and check_trajectory.py
# each carry a reader (the F5 independently-copyable rule), and
# migrate_carrier.py carries the WRITER. A reader that disagrees with the writer
# about which key a column became does not fail loudly — it hands back a row
# missing that cell, which reads downstream as "the cell is empty". That is a
# silent content loss on a registry whose whole job is to be trustworthy, so the
# agreement is pinned rather than promised in a docstring.

CHECK_TRAJ = load_script("check_trajectory")
SPINE = load_script("spine_carrier")
MIGRATE = load_script("migrate_carrier")


def test_the_two_spine_carrier_readers_agree():
    # trace.py owns the ratify brief's baseline read; check_trajectory.py owns
    # the two-tree amendment scan. Both resolve a registry to a tier and a
    # column vocabulary, and both are consulted about the SAME commit.
    assert TRACE.SPINE_TABLE == CHECK_TRAJ.SPINE_TABLE
    assert TRACE.SPINE_COLUMN == CHECK_TRAJ.SPINE_COLUMN
    for rel in ("docs/test/test-cases.csv", "docs/test/test-cases.toml"):
        assert (
            TRACE._spine_stem(rel)
            == CHECK_TRAJ._spine_stem(rel)
            == "docs/test/test-cases"
        )


def test_the_readers_are_the_exact_inverse_of_the_writer():
    # The reader map is `migrate_carrier.KEY` turned around. Asserting the
    # INVERSE rather than "every reader key is known to the writer" is what
    # catches the asymmetric half: a column the writer emits under a key no
    # reader maps back is a cell that converts and then disappears.
    #
    # Pinned over the WHOLE vocabulary (`REGISTRY_COLUMN`, spine + batch-2),
    # never the spine half alone: batch-2 put `open-items` and `agents` through
    # the same converter, and a rule that checked only the spine would have let
    # exactly those new columns drift — the columns with no history of being
    # right.
    assert SPINE.REGISTRY_COLUMN == {key: col for col, key in MIGRATE.KEY.items()}
    assert len(MIGRATE.KEY) == len(SPINE.REGISTRY_COLUMN), (
        "the writer maps two columns onto one key"
    )
    # ...and the spine half is still exactly the spine's, so widening the
    # vocabulary cannot quietly redefine a tier's column.
    assert TRACE.SPINE_COLUMN == SPINE.SPINE_COLUMN
    assert set(SPINE.SPINE_COLUMN) < set(SPINE.REGISTRY_COLUMN)


def test_the_schema_of_record_covers_every_registry_the_carrier_names():
    # `REGISTRY_KEYS` is what `tests/test_dogfood_sync.py` checks templates and
    # live registries against, so a registry the carrier can READ but the schema
    # does not STATE is a registry whose template is pinned by nothing.
    assert set(SPINE.REGISTRY_KEYS) == set(SPINE.REGISTRY_TABLE)
    for id_col, keys in SPINE.REGISTRY_KEYS.items():
        assert keys, id_col  # an empty schema passes everything
        for key in keys:
            assert key in SPINE.REGISTRY_COLUMN, (id_col, key)


def test_bootstraps_scaffolded_brief_uses_the_converters_own_keys():
    # `bootstrap.py` runs BEFORE the kit is copied and can import no sibling
    # (repo-lock §8.2), so it carries its own TOML emitter and its own copy of
    # the open-items key names. That duplication is DECLARED; this is the
    # behavioural pin D-7 requires of it, because the failure it prevents is
    # silent: a scaffolded OI-3 written under a key the reader does not map
    # comes back as a brief with no text, and `check_docs` S-3 then reports the
    # owner ask as briefed.
    BOOTSTRAP = load_script("bootstrap")
    keys = {key for key, _cell in BOOTSTRAP.STACK_OI3_ROW}
    assert keys, "the scaffolded brief writes no cells"
    assert keys <= set(SPINE.REGISTRY_KEYS["OI-ID"]), sorted(
        keys - set(SPINE.REGISTRY_KEYS["OI-ID"])
    )
    assert BOOTSTRAP.STACK_OI3_ID.startswith("OI-")


def test_every_live_spine_column_round_trips_through_the_carrier_vocabulary():
    # The maps above could agree with each other and still both be missing a
    # column that actually exists — the vacuous-agreement failure this suite
    # keeps finding. So drive the LIVE registries' own columns through the pair.
    #
    # Asked through `spine_carrier.columns`, not `csv.DictReader`: over the TOML
    # carrier the reader returns `['[requirement.SR-001]']` as the header, which
    # is not a column, and the loop would then assert a nonsense name into
    # MIGRATE.KEY and fail for the wrong reason — or, had the name happened to
    # be absent from the header, check nothing at all.
    CARRIER = load_script("spine_carrier")
    checked = 0
    for rel, id_col in TRACE.SPINE_FILES:
        columns = CARRIER.columns(ROOT / rel, id_col)
        if not columns:
            continue
        for column in columns:
            if column == id_col:
                continue  # the id is the TABLE KEY, not a field
            assert column in MIGRATE.KEY, "{}: {} has no carrier key".format(
                rel, column
            )
            assert TRACE.SPINE_COLUMN[MIGRATE.KEY[column]] == column
            checked += 1
    # Non-vacuous by construction: the three live tiers carry ~30 columns
    # between them, so a resolver that quietly found nothing reds here.
    assert checked > 20, checked


def test_the_need_reader_agrees_with_both_heading_scrapers():
    # The SN tier's id universe and draft set were SIX bespoke scanners over
    # markdown, two of them F5 twins. spine_carrier now reads the tier through
    # the carrier; before it replaces them it has to answer identically over the
    # live registry, or the migration would move the gate.
    md = ROOT / "docs/requirements/stakeholder-needs.md"
    if not md.is_file():
        return  # post-cutover: the twins are gone and this pin retires with them
    text = md.read_text(encoding="utf-8")
    needs = SPINE.load_needs(md)
    assert SPINE.need_ids(needs) == TRACE.sn_all_ids(text) == GATE.sn_all_ids(text)
    assert (
        SPINE.draft_need_ids(needs)
        == TRACE.sn_draft_ids(text)
        == GATE.sn_draft_ids(text)
    )
    assert needs, "the fixture read no needs — the agreement would be vacuous"


def test_the_edge_case_fold_is_not_titled_by_its_lifecycle_phase():
    # The live regression F-6 records, now pinned on the ONE copy of the fold.
    # traj_parse._sn_rows and gen_okf.sn_rows each carried their own, pinned by
    # nothing but a docstring saying "change both together" — they drifted, and
    # the dashboard rendered a phantom SN-000 root.
    edge = {
        "id": "SN-013",
        "kind": "edge",
        "lifecycle": "Provision",
        "scenario": "No Python 3 on PATH",
        "expected": "Probe and fail with a remedy",
    }
    assert SPINE.folded(edge) == {
        "id": "SN-013",
        "need": "No Python 3 on PATH",
        "why": "Provision",
        "priority": "n/a",
        "acceptance": "Probe and fail with a remedy",
    }
    # A core need passes through unchanged — the fold is edge-only.
    core = {
        "id": "SN-001",
        "kind": "core",
        "need": "n",
        "why": "w",
        "priority": "M",
        "acceptance": "a",
    }
    assert SPINE.folded(core) == {k: core[k] for k in ("id",) + SPINE.SN_CORE}


def test_draft_ness_reads_by_the_rule_the_file_was_written_under():
    # The two carriers are deliberately NOT unified. Under markdown a bare prose
    # mention under a draft heading counts (section-as-state, warts and all);
    # under TOML draft-ness is a FIELD, which is what retires the sharp edge the
    # 2026-08-10 sitting hit. Reading legacy text by the new rule would silently
    # un-draft needs in every un-migrated repo and float the derived gate.
    legacy = "## Draft needs\nSN-000 SN-005\n"
    assert SPINE.draft_ids_from_text(legacy) == {"SN-005"}
    assert TRACE.sn_draft_ids(legacy) == GATE.sn_draft_ids(legacy) == {"SN-005"}

    # The same claim under the new carrier is a field, and a MENTION does not
    # set it: SN-006 is named in SN-005's prose and stays ratified.
    modern = (
        '[need.SN-005]\nkind = "draft"\nneed = "n"\n\n'
        '[need.SN-006]\nkind = "core"\nneed = "supersedes SN-005"\n'
    )
    assert SPINE.draft_ids_from_text(modern) == {"SN-005"}
    assert TRACE.sn_draft_ids(modern) == GATE.sn_draft_ids(modern) == {"SN-005"}

    # And the id UNIVERSE keeps working unchanged across both, because the
    # prefixed token survives into the table key — the measured reason D-5 kept
    # the prefix rather than taking a bare numeric one.
    assert TRACE.sn_all_ids(modern) == {"SN-005", "SN-006"}


# --- the [checks] enablement readers (WI-432) ----------------------------------
# THREE modules now carry a local `tomllib` read of `docs/process.toml`'s
# `[checks]` section: `check_trajectory.py` (three dials), `gen_okf.py` (one) and
# `subagent_gate.py` (one). That duplication is the price the owner's 2026-08-11
# overturn of WI-423 weighed and accepted — F5 keeps each of those scripts
# independently copy-able, so none of them may import the coordinator layer that
# already knows how to read this file.
#
# It is duplicated POLICY, not plumbing: each copy decides "is this check on",
# and a copy that drifts does not fail loudly — it silently stops running a
# check, or silently starts running one an adopter switched off. So the D-7 bar
# applies: pin the copies BY VALUE over one table of file shapes, including the
# one place they deliberately disagree.
CT = load_script("check_trajectory")
OKF = load_script("gen_okf")
SGATE = load_script("subagent_gate")

# (contents of docs/process.toml, expected reading) for a BOOL dial. None means
# "this file declares nothing — fall through to the legacy one-word file".
_CHECK_TOML_CASES = [
    ("[checks]\ntrajectory_check = true\n", True),
    ("[checks]\ntrajectory_check = false\n", False),
    # Undeclared, in every shape that is not a declaration.
    ('[policies]\npush = "human"\n', None),
    ("[checks]\ninterfaces_check = false\n", None),
    ("", None),
    ("# trajectory_check = false\n", None),
    # Declared under the WRONG section: `tomllib` puts it nowhere this reader
    # looks, so it is undeclared — and must be, or the legacy fallback would be
    # skipped on the strength of a key nobody reads.
    ("[policies]\ntrajectory_check = false\n", None),
    # Present but broken, and present-but-wrong-typed: ON. A check that quietly
    # stops running is the failure worth avoiding, so the residual is loud.
    ("[checks]\ntrajectory_check = \n", True),
    ("[checks\ntrajectory_check = false\n", True),
    ('[checks]\ntrajectory_check = "false"\n', True),
    ("[checks]\ntrajectory_check = 0\n", True),
]


def _write_toml(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "process.toml").write_text(text, encoding="utf-8")


def test_the_three_local_checks_readers_agree_by_value(tmp_path):
    # The copies are pinned against the SAME table, and against the literal
    # expectation — equality alone can be vacuous (the `_sn_fields` case proved
    # it), so the value is pinned, not just the sameness.
    for i, (text, want) in enumerate(_CHECK_TOML_CASES):
        root = tmp_path / "case{}".format(i)
        _write_toml(root, text)
        got_ct = CT._process_check(root, "trajectory_check")
        # gen_okf's copy reads a different KEY out of the same section, so drive
        # it on its own key with the same shapes.
        _write_toml(root, text.replace("trajectory_check", "okf_export"))
        got_okf = OKF._process_check(root, "okf_export")
        assert got_ct is want, (text, got_ct, want)
        assert got_okf is want, (text, got_okf, want)


def test_an_absent_process_toml_is_undeclared_in_all_three_copies(tmp_path):
    # The migration-window hinge: no file at all must read as "nothing declared"
    # in every copy, or a repo that never adopted process.toml loses its legacy
    # one-word file's declaration.
    assert CT._process_check(tmp_path, "trajectory_check") is None
    assert OKF._process_check(tmp_path, "okf_export") is None
    assert SGATE.read_process_policy(tmp_path) is None


def test_the_subagent_copy_diverges_only_where_its_module_says_it_does(tmp_path):
    # subagent_gate's dial is a WORD, not a bool, and its module contract is
    # "fail OPEN with a paper trail" — a broken gate must never wedge the tools.
    # So on an unparseable file it reads UNDECLARED where the other two read ON.
    # Pinned here because a later reader "harmonizing" the three copies would be
    # turning an unreadable config into `ask` on every spawn.
    _write_toml(tmp_path, '[checks]\nsubagent_gate = "deny"\n')
    assert SGATE.read_process_policy(tmp_path) == "deny"
    _write_toml(tmp_path, '[checks]\nSUBAGENT_GATE = "deny"\n')
    assert SGATE.read_process_policy(tmp_path) is None

    broken = tmp_path / "broken"
    _write_toml(broken, '[checks\nsubagent_gate = "deny"\n')
    assert SGATE.read_process_policy(broken) is None  # undeclared, not `ask`
    assert CT._process_check(broken, "trajectory_check") is True  # ON, loudly
    assert OKF._process_check(broken, "okf_export") is True

    # A non-string value is RENDERED, not dropped, so `decide` reaches its
    # "unrecognized … asking" arm rather than reading a garbled dial as off.
    _write_toml(tmp_path, "[checks]\nsubagent_gate = true\n")
    assert SGATE.read_process_policy(tmp_path) == "true"
    assert SGATE.decide("Task", "true", "")[0] == "ask"


def test_every_checks_dial_falls_back_to_its_legacy_file_and_toml_wins(tmp_path):
    # The SN-028 migration window, driven end to end through the PUBLIC readers
    # (not the private `_process_check`): with no process.toml the legacy word
    # still governs, and once the key exists it wins. `config_conflicts` is what
    # refuses that mixed state upstream — these readers cannot refuse, they must
    # answer, so "TOML wins" is the answer pinned here.
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    legacy = {
        "trajectory-check": (CT.read_trajectory_enabled, "trajectory_check"),
        "interfaces-check": (CT.read_interfaces_check_enabled, "interfaces_check"),
        "components-check": (CT.read_components_check_enabled, "components_check"),
        "okf-export": (OKF.read_enabled, "okf_export"),
    }
    for name, (reader, key) in legacy.items():
        assert reader(tmp_path) is True  # absent everywhere = on
        (docs / name).write_text("off\n", encoding="utf-8")
        assert reader(tmp_path) is False, name  # legacy file alone still governs
    _write_toml(
        tmp_path,
        "[checks]\n" + "".join("{} = true\n".format(k) for _, k in legacy.values()),
    )
    for name, (reader, _) in legacy.items():
        assert reader(tmp_path) is True, name  # the key wins over the file

    # The subagent gate's own fallback, same two steps.
    (docs / "subagent-gate").write_text("deny\n", encoding="utf-8")
    (docs / "process.toml").unlink()
    assert SGATE.read_process_policy(tmp_path) is None
    assert SGATE.read_declared(docs / "subagent-gate") == "deny"
    _write_toml(tmp_path, '[checks]\nsubagent_gate = "off"\n')
    assert SGATE.read_process_policy(tmp_path) == "off"


def test_the_shipped_template_declares_every_checks_dial_at_todays_default():
    # The overturn's whole content: the six are VISIBLE. Absence used to be the
    # declaration, which is exactly what the owner called confusing — so the
    # anti-regression here is that a key is not quietly dropped again, and that
    # the two opt-in dials did not get flipped on the way in.
    text = (KIT / "process.toml.template").read_text(encoding="utf-8")
    import tomllib

    checks = tomllib.loads(text)["checks"]
    assert checks == {
        "trajectory_check": True,
        "interfaces_check": True,
        "components_check": True,
        "okf_export": True,
        "live_status": False,
        "subagent_gate": "off",
    }
    # And this repo's own instance says the same thing, since it declared none
    # of the six files and therefore ran exactly these values.
    live = tomllib.loads((ROOT / "docs" / "process.toml").read_text(encoding="utf-8"))
    assert live["checks"] == checks


def test_the_migration_table_and_the_converter_name_the_same_six():
    # Three tables have to agree about these dials or a migration half-happens:
    # agent_common.PROCESS_KEYS (the value reader + the mixed-config refusal),
    # bootstrap.LEGACY_CONFIG (the converter), and the shipped template. A dial
    # migrated in one and forgotten in another is a policy that silently reverts.
    ac = load_script("agent_common")
    boot = load_script("bootstrap")
    six = {
        "trajectory-check": ("checks", "trajectory_check", "bool"),
        "interfaces-check": ("checks", "interfaces_check", "bool"),
        "components-check": ("checks", "components_check", "bool"),
        "okf-export": ("checks", "okf_export", "bool"),
        "live-status": ("checks", "live_status", "bool"),
        "subagent-gate": ("checks", "subagent_gate", "str"),
    }
    for name, row in six.items():
        assert ac.PROCESS_KEYS[name] == row, name
    converter = {n: (s, k) for n, s, k, _ in boot.LEGACY_CONFIG}
    for name, (section, key, _) in six.items():
        assert converter[name] == (section, key), name


# --- the declared-line reader, 5-way (repo-lock.md §8.2, 2026-08-12 census) ---
# "The first non-empty, non-comment line of a one-word policy file" is written
# out FIVE times: agent_common.read_declared and subagent_gate.read_declared
# (same name, two different signatures), plus a third name for the identical
# rule — `_first_declared_line` — in bootstrap.py, check_privacy.py and
# check_trajectory.py. Plumbing this small is licensed unbounded under F5, but
# a silent divergence between copies would mean the git hooks, the bootstrap
# migration, agent_common's docs/gate reader and the subagent fan-out gate
# read the SAME on-disk file five different ways. Pinned by value, over one
# table of file shapes, so a sixth copy — or a "harmonizing" edit to one of
# the five — has to argue with a value table rather than a prose promise.
AGENT_COMMON = load_script("agent_common")
SUBAGENT = load_script("subagent_gate")
BOOTSTRAP_DECL = load_script("bootstrap")
CHECK_PRIVACY = load_script("check_privacy")

# (file contents, the declared line every None-sentinel reader returns).
# `want` is what bootstrap/check_privacy/check_trajectory's `_first_declared_line`
# and agent_common.read_declared(path, None) all return; None means "nothing
# declared" (comments-only, blank, or absent), not "the file holds empty text".
_DECLARED_LINE_CASES = [
    ("comments-only", "# nothing here\n# still nothing\n", None),
    ("blank", "", None),
    ("leading-whitespace", "   deny\n", "deny"),
    ("mixed-case-value", "# a leading comment\nDeNy\n", "DeNy"),
    ("trailing-whitespace", "off   \n", "off"),
]


def test_the_three_first_declared_line_copies_agree_exactly(tmp_path):
    # bootstrap.py, check_privacy.py and check_trajectory.py each carry their
    # own literal `_first_declared_line` — F5 plumbing, unbounded — but a
    # divergence here would mean git-hook enforcement (check_privacy,
    # check_trajectory) and the bootstrap legacy-config migration read the
    # SAME file two different ways. Pin byte-for-byte equal, including the
    # absent-file case none of the three signatures distinguish from empty.
    for name, text, want in _DECLARED_LINE_CASES:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        assert BOOTSTRAP_DECL._first_declared_line(path) == want, name
        assert CHECK_PRIVACY._first_declared_line(path) == want, name
        assert CT._first_declared_line(path) == want, name
    missing = tmp_path / "does-not-exist"
    assert BOOTSTRAP_DECL._first_declared_line(missing) is None
    assert CHECK_PRIVACY._first_declared_line(missing) is None
    assert CT._first_declared_line(missing) is None


def test_agent_common_read_declared_agrees_modulo_its_default(tmp_path):
    # agent_common.read_declared is the same rule with a fourth signature: a
    # caller-supplied `default` in place of a hard-coded `None`. Called with
    # default=None it must read identically to the three copies above — this
    # is the function `docs/gate` (a generated cache) is read through, and it
    # has to agree with the hooks' reader about the same file.
    for name, text, want in _DECLARED_LINE_CASES:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        assert AGENT_COMMON.read_declared(path, None) == want, name
    missing = tmp_path / "does-not-exist"
    assert AGENT_COMMON.read_declared(missing, None) is None
    # Its own documented divergence — a caller default rather than a
    # hard-coded None on absence — pinned as itself, not just "not None".
    assert AGENT_COMMON.read_declared(missing, "fallback") == "fallback"


def test_the_subagent_copy_diverges_only_where_its_docstring_now_says(tmp_path):
    # subagent_gate.read_declared's docstring used to call itself "the same
    # declared-policy parse the hooks and agent_loop use" with no further
    # qualification. Measured here: the LINE-SELECTION rule is the same —
    # comments and blank lines are skipped identically — but the RETURN VALUE
    # diverges in TWO ways, not the one the name ("lowercased") advertises:
    #   1. lowercased — deliberate: this module compares the token against a
    #      closed, case-folded vocabulary ("off"/"ask"/"deny").
    #   2. "" instead of None on absent/blank/comments-only — also deliberate:
    #      decide() below documents its own `policy` param as `"" = off`, so
    #      this reader has to hand back "" to compose with that contract.
    # Both are load-bearing (this module's fail-open posture is owner-ruled
    # 2026-08-11 — do NOT "fix" either away), so the docstring was corrected
    # to name divergence 2 rather than leaving the "same parse" claim to imply
    # casing is the only difference.
    for name, text, want in _DECLARED_LINE_CASES:
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        expect = "" if want is None else want.lower()
        assert SUBAGENT.read_declared(path) == expect, name
    missing = tmp_path / "does-not-exist"
    assert SUBAGENT.read_declared(missing) == ""  # not None, unlike its siblings
    # And the sentinel is exactly what decide() below needs: "" resolves to
    # the gate's OFF branch, the same branch a bare absent file resolves to.
    assert SUBAGENT.decide("Task", SUBAGENT.read_declared(missing), "")[0] == "allow"


# --- the carrier value round trip (repo-lock.md §8.2, 2026-08-12 census) -------
# migrate_carrier.value_to_cell is the migration's own round-trip self-check —
# `compare()` re-derives a cell from the just-written TOML value and diffs it
# against the original CSV cell. spine_carrier.value_to_cell is the READER
# every production consumer of the TOML carrier goes through (`rows_from_toml`,
# hence `spine_carrier.load`). Both docstrings claim to be `cell_to_value`'s
# inverse, and spine_carrier's explicitly claims to match "deliberately the
# same rules" migrate_carrier's writes by — but nothing compared them. The
# census found a real drift: the reader stringifies each list element
# (`";".join(str(v) for v in value)`), the writer joined raw
# (`";".join(value)`), which raises TypeError the moment a ref array holds a
# non-str element. Fixed here (one line, migrate_carrier.py) so the pin below
# passes honestly rather than pinning the crash as a "divergence".
def test_the_carrier_value_writer_and_reader_are_the_exact_inverse():
    cases = [
        "plain string",
        "a;b;c",  # a string that merely CONTAINS the ref separator
        [],
        ["a", "b", "c"],
        ["a", 2, "c"],  # a ref array with a non-str element — the crash case
    ]
    for value in cases:
        assert MIGRATE.value_to_cell("SN-Refs", value) == SPINE.value_to_cell(value), (
            value
        )

    # And the concrete round trip both docstrings describe: a CSV ref cell,
    # converted to a value by cell_to_value, converted back by each
    # value_to_cell, recovers the ORIGINAL cell text — semicolon-joined,
    # exactly as the live registries write it (WI-431's measured 271-of-271).
    original = "a;b;c"
    value = MIGRATE.cell_to_value("SN-Refs", original)
    assert value == ["a", "b", "c"]
    assert MIGRATE.value_to_cell("SN-Refs", value) == original
    assert SPINE.value_to_cell(value) == original


# --- is_example, including None (repo-lock.md §8.2, 2026-08-12 census) ---------
def test_is_example_agrees_across_all_three_copies_including_none():
    # derive_gate.is_example and gen_release_checklist.is_example both guard
    # `(rid or "").endswith(...)`; trace_text.is_example (imported into
    # trace.py's own namespace as `is_example`, so `TRACE.is_example` IS this
    # function) did not, and crashed on None. Every current call site
    # pre-guards (`r.get(...) and not is_example(...)`), so the crash was
    # latent — unreached by any live path, and unpinned. Guarded here
    # (trace_text.py) so the three genuinely agree rather than agreeing by
    # omission of the one case that would have told them apart.
    RELEASE = load_script("gen_release_checklist")
    TEXT = load_script("trace_text")
    cases = ["SR-000", "SR-123", "", None]
    for rid in cases:
        want = GATE.is_example(rid)
        assert RELEASE.is_example(rid) == want, rid
        assert TEXT.is_example(rid) == want, rid
    # The values themselves, not just agreement — equality alone can be
    # vacuous if all three are wrong the same way.
    assert GATE.is_example("SR-000") is True
    assert GATE.is_example("SR-123") is False
    assert GATE.is_example("") is False
    assert GATE.is_example(None) is False
