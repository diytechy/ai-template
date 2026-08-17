#!/usr/bin/env python3
"""Traceability join + orphan report for the SN->SR->LLR->TC registries.

Stack-agnostic reference implementation (Python 3, standard library only — no
pip installs). Drop it in a new repo as `scripts/trace.py` and wire it into the
check harness / CI. It is the generated "traceability matrix" referenced by
PROCESS.md: it never needs hand-maintaining.

Usage:
    python scripts/trace.py [--strict] [--strict-integrity] [--require-verified]
                            [--phase LIST] [--no-placeholders] [--strict-schema]
                            [--html] [--ratify SCOPE [--out FILE]]
                            [--root DIR] [--docs DIR]

Reads (under --docs, default "<root>/docs"; --root defaults to "."): the spine —
    requirements/{system-requirements,low-level-requirements}.csv,
    test/test-cases.csv, and requirements/stakeholder-needs.md (SN ids scraped;
    an SN under a heading containing "draft" is unratified, §4a) — plus the
    OPTIONAL off-spine registries requirements/{performance-budgets,repos,
    procurement,assets,components,interfaces}.csv (PB/REPO/PART/ASSET/CMP/IF, each
    documented on its own *.template.csv and in process.md §8/§9 +
    process-options.md; the legacy modules.csv/MOD- form is still read). Absent
    optional files and "-000" example rows are ignored, so a fresh scaffold is
    green.

Writes:
    test/report.md — counts, the SR->LLR->TC matrix, the orphan/integrity/
        advisory sections, and two rendered views of the same join: a
        line-reviewable SN->SR->LLR->TC outline and a small, diff-friendly Mermaid
        DAG colored by orphan/draft state.
    test/report.html (only with --html) — a dependency-free, collapsible <details>
        tree of the full graph (inline CSS, zero JS). A gitignored composite
        artifact, never the review surface — review the registry CSVs (process.md
        §3 "Reviewability").

Exit: 0 normally; --strict -> 1 on any orphan / status / off-spine finding;
--strict-integrity -> 1 on an integrity finding ONLY (the always-valid floor the
pre-commit hook runs on every commit — a duplicate/malformed id is wrong at any
stage, while orphans are a DevBar-Tests+ gate criterion).

The method rules this script mechanizes are stated ONCE elsewhere — they are NOT
restated here (the kit's decompose-don't-paraphrase rule applied to itself):
    - the orphan rules (an SR needs an LLR unless Verification is
      Analysis/Inspection/Attest, a TC, and — when a needs file exists — an SN;
      LLR/TC parentage), the Drafted child-completeness exemption, and the
      Drafted->Approved ladder: process.md §4 + the derived-gate model
      (docs/archive/specs/derived-gate-model.2026-07-20.md §3, and §4a for section-as-state SN
      maturity).
    - the always-on structural-integrity floor (a CSV data row whose column count
      differs from its header, a duplicate/malformed SR/LLR/TC/PB/REPO/CMP/IF id,
      and the SR;LLR citation-coherence rule) and the off-spine back-link rules
      (every PB/REPO/CMP/IF row resolves to the spine): process.md §4/§8/§9 +
      process-options.md.
    - phased delivery (--phase scopes --require-verified to listed/blank-Phase
      SRs and reports the rest as phase-deferred; orphan rules stay phase-blind)
      and the closed vocabularies --strict-schema enforces (SR Verification, TC
      Tier): process.md §4.

Flags in brief: --require-verified adds the DevBar-Release criterion "an SR is
Status=Approved" — any Verification method (Drafted SRs exempt); --no-placeholders flags leftover "-000"
example rows (wire in from DevBar-Tests on); --strict-schema adds required-field,
closed-vocabulary, and "Automated=Yes cites Evidence" checks over the real rows;
--ratify SCOPE emits ONLY the batch-scoped ratification hierarchy (a phase tag or
an SR-id list) to stdout or --out and runs no checks (WI-146); the reserved scope
`modified` (WI-316) emits the re-attestation brief instead — per-cell
before/after for every row owing a human act, against its copy in the
`docs/archive/last_approved/` snapshot (`baseline_snapshot.py`). Warn-only
advisories (loud on stdout + in the report, never gating): an unpinned
comparative acceptance-criterion, an LLR reading below Approved while every
citing TC is Approved (WI-129), a missing knowledge pack, and an interface
endpoint that resolves to no LLR Module. The report always carries the
attested-vs-mechanized approval split (process.md §4 "Attest") and, when the SR
registry tags Aspect, a per-aspect count.

Contracts: IF-001, IF-021, IF-042 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

# Sibling: the spine-row TEXT layer (WI-329). Run as a subprocess this script's
# own dir is sys.path[0] so a plain import resolves; the guard covers an
# in-process import (a test) whose sys.path does not yet carry scripts/ — the
# same sanctioned-sibling-import idiom agent_loop and gen_trajectory use.
#
# `baseline_snapshot` and (through it) `check_trajectory` joined at D-9 step 4:
# the re-attestation model's baseline is the `last_approved` snapshot, and its
# cell comparison is `check_trajectory.split_changed_cells` — the SAME function
# the amend-without-flip warn reads, which is what stops the brief and the warn
# from ever disagreeing about which cells are normative. This is the one new
# import edge the snapshot design declares.
try:
    import baseline_snapshot
    import check_trajectory
    import spine_carrier
    from trace_text import (
        EXTERNAL_ENDPOINT_PREFIX,
        ac_advisories,
        form_findings,
        if_this_project_advisories,
        is_drafted,
        is_example,
        norm_module,
        paraphrase_advisories,
        provenance_findings,
        refs,
        sr_artifact_advisories,
        sr_fanout_advisories,
        verification_coherence_advisories,
    )
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import baseline_snapshot
    import check_trajectory
    import spine_carrier
    from trace_text import (
        EXTERNAL_ENDPOINT_PREFIX,
        ac_advisories,
        form_findings,
        if_this_project_advisories,
        is_drafted,
        is_example,
        norm_module,
        paraphrase_advisories,
        provenance_findings,
        refs,
        sr_artifact_advisories,
        sr_fanout_advisories,
        verification_coherence_advisories,
    )


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is. Kit
    scripts print non-ASCII (an em-dash WARNING, `§` refs) that a legacy Windows
    cp1252 console raises UnicodeEncodeError on — wedging the run, not just
    mojibaking. Python 3.7+ streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def load_csv(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


def is_approved(row):
    """The approved state: the row's TEXT is blessed by a human in a reviewed
    Status-change commit. Matched case-insensitively so it follows the SAME rule
    as is_drafted (the one Status-casing rule, process.md §4).

    RENAMED AT D-9 MIGRATION STEP 5 from `is_verified`, and the rename carries a
    RULING, not just a word. `Verified` used to make TWO claims at once — the
    text is ratified AND the evidence passed — and the second claim was a
    hand-set cell asserting a test run nobody re-ran. D-9 deletes the pass claim
    from the vocabulary: `Approved` says only that the text is blessed, and
    whether the tests pass is the harness's answer, not a cell's. `Planned`
    (ratified text, evidence pending) folded into this same value at the same
    act under OI-30 D1 — the two named one rung and one of them named it more
    clearly. The consequence the fold created (a decomposed ex-`Planned` row
    would have read DevBar-Release under the old `sr_bar`) is closed by the
    `sr_bar` ceiling ruled at OI-30 D2.

    Duplicated in derive_gate.py per the F5 rule; pinned equal by
    test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "approved"


def is_modified(row):
    """The post-approval `Modified` state (WI-316, process.md §7): the row landed
    `Approved` but its content changed after the last approval, so a re-attest is
    owed — `Modified`→`Approved` blesses the amendment. Recognized for
    SURFACING, not gate arithmetic: a Modified SR is simply not Approved, so
    `derive_gate.sr_gate` already reads it as decomposed-unapproved DevBar-Tests
    with no code of its own — this predicate exists for the `modified=N` basis
    count, the pending-owner-actions projection, the chain-consistency warns, and
    the `--ratify modified` brief.

    TRANSITIONAL, AND STILL LIVE. It survives step 5's rename deliberately: its
    successor (`baseline_snapshot`-backed drift) has to run alongside it through
    the owner's signing act before the marker can retire, or the migration would
    delete the only drift detector in the same commit that renames everything it
    reads. Step 7 retires the word once the last `Modified` row is signed.

    Same case-insensitive one-casing rule as its two live siblings; duplicated in
    derive_gate.py per the F5 rule; pinned equal by test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "modified"


# `is_planned` WAS DELETED AT D-9 MIGRATION STEP 5, not re-keyed — the deletion
# its own docstring promised. It was step-2 INSURANCE: `Planned` sat on 14 live
# spine rows while no predicate in the kit recognized it (it read identically to
# `Bananas`), so it was surfaced for the interval between the closure and the
# ruling. OI-30 D1 ruled the fold — `Planned` IS `Approved` — so every site that
# read the predicate now reads `is_approved`, `is_drafted` or `is_modified`, and
# the word itself is out of `STATUS_VALUES`. `tests/test_rule_sync.py` asserts
# NEGATIVELY that no predicate in any script honours `Draft`, `Planned` or
# `Verified` again.


# SR Verification methods that decompose to a TC but no LLR — there is no code to
# write, only its acceptance to analyze/inspect/attest, so the orphan rule below
# exempts them from the "SR with no LLR" finding. The derived gate mirrors this
# exact set as derive_gate.LLR_EXEMPT; tests/test_rule_sync.py pins the two equal
# (WI-099) so the orphan report and the gate computation never disagree about what
# "decomposed" means. (Critique is NOT here: its artifact is produced by code, only
# its acceptance is subjective.)
LLR_EXEMPT = ("Analysis", "Inspection", "Attest")


def llr_exempt(row):
    """SR Verification method in LLR_EXEMPT, matched on the stripped cell so a
    whitespace-padded valid method exempts here exactly as it does in the gate
    derivation (the two decision points must agree — a divergence is a false
    green or false red at a gate).
    Duplicated in derive_gate.py per the F5 rule; pinned equal by test_rule_sync."""
    return (row.get("Verification") or "").strip() in LLR_EXEMPT


def phase_num(row):
    """The integer a row's free-form `Phase` cell digit-parses to (`v2`->2, `2`->2);
    None when blank/unparseable. The one phase-parse the kit uses — the ratified-phase
    schema rule and the `--phase` foundation filter share it, so a downstream repo that
    kept `vN` labels parses identically (the phase doctrine, process.md §4).
    Duplicated in derive_gate.py per the F5 rule."""
    m = re.search(r"\d+", (row.get("Phase") or ""))
    return int(m.group()) if m else None


def structure_findings(path, display=None):
    """Column-count structural check over one registry CSV: every data row must
    parse (RFC-4180 quoting) to exactly the header's column count. This is the
    integrity-class guard for the misquoted-cell failure mode (an unquoted comma
    shifts every later column and the join silently reads the wrong cells), so
    it fails --strict and --strict-integrity — wrong at any stage, like a
    duplicated id. Fully blank rows are skipped (a trailing newline is not a
    finding); '-000' example rows are NOT skipped, because a template row must
    parse correctly too."""
    if not path.exists():
        return []
    name = display or path.name
    out = []
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return out
        expected = len(header)
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            if len(row) != expected:
                rid = (row[0].strip() if row else "") or "(no id)"
                out.append(
                    "{}: row {} (line {}) parses to {} column(s); header has "
                    "{} — quote any cell containing a comma".format(
                        name, rid, reader.line_num, len(row), expected
                    )
                )
    return out


# Id syntax per registry (for the always-on integrity check).
ID_PATTERNS = {
    "SR": re.compile(r"^SR-\d+$"),
    "LLR": re.compile(r"^LLR-\d+$"),
    "TC": re.compile(r"^TC-\d+$"),
    "PB": re.compile(r"^PB-\d+$"),  # optional performance-budgets registry (§9)
    "REPO": re.compile(
        r"^REPO-\d+$"
    ),  # optional coordinator repo-delegation registry (MULTI_REPO.md)
    "MOD": re.compile(
        r"^MOD-\d+$"
    ),  # legacy name for REPO (pre-rename modules.csv rows, still read)
    "PART": re.compile(
        r"^PART-\d+$"
    ),  # optional purchased/external parts registry (process-options.md)
    "ASSET": re.compile(
        r"^ASSET-\d+$"
    ),  # optional binary/large-asset provenance registry (process-options.md)
    "CMP": re.compile(
        r"^CMP-\d+$"
    ),  # optional domain-neutral component registry (process-options.md)
    "IF": re.compile(
        r"^IF-\d+$"
    ),  # optional intra-repo/cross-project interface registry (process.md §8)
}

# Fields that must be non-empty under --strict-schema. Omits the optional columns
# (Permutations, Phase, TestRefs, Parameters) and the LLR's `Rationale`: a short
# decomposition row's why IS its parent SR's, so requiring one everywhere would
# manufacture the restatement the column exists to prevent. The SR's `Rationale`
# IS required — every row already carries one, so it guards zero-to-zero. A legacy
# CSV without the column reads as empty (the ADOPTING.md §6 migration adds it).
REQUIRED_FIELDS = {
    "SR": [
        "SR-ID",
        "Title",
        "SN-Refs",
        "Requirement",
        "Rationale",
        "AcceptanceCriteria",
        "Priority",
        "Verification",
        "Status",
    ],
    "LLR": ["LLR-ID", "SR-Refs", "Title", "Module", "CodeSymbol", "Detail", "Status"],
    "TC": [
        "TC-ID",
        "Verifies",
        "Level",
        "Method",
        "Tier",
        "Expected",
        "Automated",
        "Status",
    ],
    # IF and CMP joined at WI-443 (OI-14 part B), and their tier is ADVISORY:
    # `schema_advisories` reads these same two dicts and never joins a failure
    # set, so the exit code is untouched at any gate. That is the ruled
    # warn-first sequencing, not a softer rule — the vocabularies are closed the
    # moment they are stated, and the promotion to ERROR is a later, separate
    # decision taken once the corpus has converged.
    #
    # `Rationale` is deliberately NOT required on an IF row: B1 migrates cells as
    # rows are touched, so demanding one everywhere would manufacture 113 rushed
    # sentences — the bulk rewrite the ruling refused. `SignalNote`, `Component`
    # and `Notes` are optional by design.
    # WI-442 replaced `Stability` with `Approval` here. The two
    # `Interface*External` tie-backs are deliberately NOT required — a row
    # carries one only when it realizes a boundary crossing, and requiring them
    # would demand every internal seam claim to be a boundary.
    # `Direction`/`Counterpart` are HELD pending WI-455 — evidence and removal
    # owner: docs/requirements/interfaces.toml's header.
    "IF": [
        "IF-ID",
        "Direction",
        "ThisProject",
        "Counterpart",
        "Contract",
        "Signal",
        "Req-Refs",
        "Owner",
        "Version",
        "Approval",
    ],
    "CMP": ["CMP-ID", "Name", "Category", "State"],
    # WI-442 — the depth-0 frame's three tiers (docs/requirements/external.toml).
    # `Absorbs` and `Notes` are optional provenance and are not required.
    "EXT": ["EXT-ID", "Name", "Class", "Description", "Approval"],
    "B": ["B-ID", "Entity", "Direction", "Carries", "Approval"],
    "REL": ["REL-ID", "From", "To", "Kind", "Flow", "Approval"],
}

# The only *closed* vocabularies the method defines (process.md §4). `Priority`
# is intentionally left open, so it is not validated here.
#
# `Status` CLOSED AT ITS LIVE TRUTH (D-9 migration step 1, 2026-08-15) and
# NARROWED TO THE LADDER AT STEP 5 (the rename, 2026-08-15). It was
# open-vocabulary until step 1, and the cost was measurable: a value no
# predicate recognizes — `Planned` was exactly that, and `Bananas` would have
# read identically — sat in the registry announcing nothing. The enum-close-first
# rule the migration runs under is stated executably: *at every commit, the
# declared Status enum equals exactly the set of values at least one live
# predicate recognizes, and that set narrows monotonically*.
#
# `Draft`→`Drafted`, `Verified`→`Approved`, and `Planned`→`Approved` (OI-30 D1:
# ratified-text-awaiting-evidence and ratified-text-with-evidence are ONE rung
# once the pass claim leaves the vocabulary). `Modified` survives as the
# TRANSITIONAL third value and retires at step 7, when the last row it marks has
# been signed and the snapshot-backed drift rule is armed as its successor.
STATUS_VALUES = frozenset({"Drafted", "Approved", "Modified"})

# The enum columns whose out-of-vocabulary findings are INTEGRITY-class, not
# schema-class (D-9 migration correction C1). `schema_findings` only runs under
# `--strict-schema`, which `check.py` appends at DevBar-Release alone — so a
# Status vocabulary declared there would be INERT for every repo below the top
# bar, which is every repo the migration is being run for. A retired Status word
# is wrong at ANY stage, exactly like a duplicated id, so it joins the always-on
# `--strict-integrity` floor (and therefore the pre-commit hook) instead. The
# vocabulary still has ONE home — `ENUM_FIELDS` below — and this names only
# which pipe reads it.
INTEGRITY_ENUM_COLS = frozenset({"Status"})

ENUM_FIELDS = {
    "SR": {
        "Status": STATUS_VALUES,
        # The ruled aspect vocabulary (sitting-2 decision 10, executed by the
        # WI-451 re-tier). `Area` was a 31-value free-text column of which 25
        # values were a component by another name; those were DROPPED at
        # conversion rather than remapped, and the six SPANNING values — the
        # cross-cutting concerns no partition can express — became this closed
        # set. An aspect is a REVIEW grouping, not an ownership claim, so a row
        # carrying none is normal and never a finding (only a non-empty
        # out-of-vocabulary value is). NOT the D-9/D12 Status vocabulary, which
        # is held for its own atomic act (2026-08-14e).
        "Aspect": {
            "process",
            "trajectory",
            "unattended-loop",
            "connectivity",
            "perf",
            "portability",
        },
        "Verification": {
            "Test",
            "Demonstration",
            "Manual",
            "Analysis",
            "Inspection",
            "Attest",
            "Critique",
        },
    },
    # The LLR tier had NO entry here at all until the Status closure — its
    # `Status` cell was the one spine vocabulary nothing declared and nothing
    # validated, which is how seven LLR amendments came to ride `Planned`
    # (WI-458) with no surface reading them.
    "LLR": {"Status": STATUS_VALUES},
    "TC": {"Status": STATUS_VALUES, "Tier": {"Smoke", "Full", "Release"}},
    # WI-443 / OI-14 part B — the IF tier's first closed vocabularies, advisory
    # like its required fields above.
    #
    # `Signal` is the owner's ruled discrete-vs-variable typing and is NEW: all
    # 113 live rows were searched before the ruling and NOTHING in the registry
    # typed a signal at all, in any column. `Stability` was DECLARED by
    # process.md §8 from the start and validated nowhere, which is how four rows
    # came to carry `Provisional` — a value that was never in the shipped
    # vocabulary. There is no `Status` entry because that column RETIRED: it was
    # undeclared, it overlapped `Stability` (the word `Stable` appeared in both
    # on one row meaning different things), and its only consumer was the LLM
    # planning-brief surface, which was being handed it as fact.
    #
    # `Stability` LEFT this map at WI-442 and `Approval` took its place — the one
    # maturity field for both the IF tier and the frame tiers below, which is
    # what decision 12's "one shared status vocabulary, per-registry subsets"
    # buys. The subset here is the two-value one; it is PROVISIONAL pending
    # D-9's ladder, and the migration is stated in
    # docs/requirements/external.toml's header rather than guessed at here.
    #
    # `Direction` joined at the 2026-08-15 interface rework (plan step 1). It was
    # the one IF column carrying a vocabulary that §8 states and nothing checked,
    # and it is stated here with its RULED meaning (Q2, 2026-08-15a): the cell is
    # the seam's FLOW/COVERAGE declaration, never an ownership claim — ownership
    # is the `Owner` cell. A `Provides` row says this side authors the contract;
    # a `Consumes` row is a coverage declaration (this cross-component edge is
    # intended, and this row discharges it), which is exactly what
    # check_trajectory's `_declared_seam_pairs` reads the 74 of them for.
    "IF": {
        "Direction": {"Provides", "Consumes"},
        "Signal": {"discrete", "variable"},
        "Approval": {"drafted", "approved"},
    },
    "CMP": {"State": {"planned", "built", "verified", "has-gap", "deprecated"}},
    # WI-442 — the depth-0 frame. `Class` is the entity vocabulary §1R.7 item 2
    # confirmed (`deliverable` was the ruled addition); `Direction` is read from
    # the SYSTEM's point of view, which is why it is in|out|inout and not the
    # IF tier's retired Provides/Consumes.
    "EXT": {
        "Class": {"operational", "enabling", "interoperating", "deliverable"},
        "Approval": {"drafted", "approved"},
    },
    "B": {
        "Direction": {"in", "out", "inout"},
        "Approval": {"drafted", "approved"},
    },
    "REL": {"Approval": {"drafted", "approved"}},
}

# --- the IF `Contract` negative rules (WI-443, warn-first) --------------------
# Whether a sentence is a specification or a story CANNOT be mechanized — no
# check reads intent. These four read FORM instead, and between them they make
# it impossible for a `Contract` cell to be a CHANGELOG, which is the failure the
# census actually measured (requirement voice 1% -> 7.1%, cross-registry
# citations 14% -> 24%, median cell 260 -> 325 characters, all in three days
# while the rule existed only as prose).
#
# The first two are REFUSE-CLASS — they name what may never appear, and they
# read as errors that have not been promoted yet. The last two are genuinely
# advisory: a long cell may be honest, and `since` has a temporal sense.
_IF_WI_RE = re.compile(r"\bWI-\d+\b")
#
# The decision pattern is `D-<n>` EXACTLY, not a general `<LETTER>-<n>`: the
# broader shape was tried and it read the data pack's own crossing ids (`M-10`)
# as rulings, which is a check inventing a rule nobody wrote. What was ruled is
# the repo-lock decision citation, and that is what this matches.
_IF_DECISION_RE = re.compile(r"\bD-\d+\b")
_IF_CONNECTIVE_RE = re.compile(r"\b(because|rather than|so that|since)\b", re.I)
IF_CONTRACT_MAX = 500

# --- Acceptance-criteria testability advisory (warn-only) --------------------
# A comparative/absolute claim in an AcceptanceCriteria cell is untestable until
# it names its predicate: identical *in what*, judged *how*. (Gilbert's LLR-013
# shipped "cannot distinguish source by schema" through DevBar-Reqs and had to be pinned
# by hand at DevBar-Tests.) Both lists are heuristics — the advisory WARNS and never joins
# a failure set; the DevBar-Reqs consistency review (process.md §4) makes the call.


def llr_status_advisories(llrs, tcs):
    """Warn-only findings (WI-129): an LLR whose Status reads below `Approved`
    while *every* TC that cites it is already `Approved`. The evidence to lift it
    exists, so the gap is a readout drift, not a coverage hole — mechanically
    harmless (the derived gate ignores LLR/TC Status past `Drafted`; only the SR's
    `Approved` drives DevBar-Tests->DevBar-Release, derive_gate.maturity_gate), but confusing at a
    ratification review, where a below-`Approved` LLR under an `Approved` SR reads
    like an unfinished decomposition. Warn only: never promoted to an error (not
    under --strict or --strict-integrity), because making LLR status gate would
    re-introduce the exact LLR-status coupling the derived-gate model dropped.
    An LLR with no citing TC is the orphan rules' job, not this lint's; matching
    is case-insensitive via the shared is_approved() predicate. A `Modified` LLR
    is exempt (WI-316): its below-`Approved` status is DELIBERATE — a
    post-approval amendment awaiting re-attest, not a readout drift — so the
    "lift to Approved" nag would tell the owner to erase the very marker the
    sitting needs."""
    citing = {}  # LLR id -> [is_approved(tc) for each citing TC]
    for r in tcs:
        tc_ok = is_approved(r)
        for x in refs(r.get("Verifies")):
            if ID_PATTERNS["LLR"].match(x):
                citing.setdefault(x, []).append(tc_ok)
    out = []
    for r in llrs:
        lid = r.get("LLR-ID")
        if not lid or is_approved(r) or is_modified(r):
            continue
        verdicts = citing.get(lid)
        if verdicts and all(verdicts):
            out.append(
                "LLR {} reads '{}' but every citing TC is Approved — lift to "
                "Approved (the evidence already exists)".format(
                    lid, (r.get("Status") or "").strip()
                )
            )
    return out


def modified_chain_advisories(srs, llrs, tcs):
    """Warn-only findings (WI-316): a `Modified` LLR/TC whose owning SR is neither
    `Modified` nor `Drafted` — under the closed enum, a parent reading `Approved`.
    The SR is the ATTESTATION UNIT (process.md §7) — the re-attest sitting, the
    pending-owner-actions projection, and the `--ratify modified` brief all key
    off the SR row — and the snapshot drift arm cannot stand in: `is_drifted`
    fires only for a row whose live Status claims approval, so a `Modified`
    child never counts as drifted while the `Approved` parent's own text has
    not moved. Neither arm surfaces the amendment (re-measured at the
    2026-08-15 sitting sweep: the `is_planned` repair briefly discharged this,
    then D-9's fold deleted that predicate and re-opened the seam — durably,
    by construction). Flip the owning SR (the amendment's real scope) or the
    child's flag is dead weight. Warn only, same tier as llr_status_advisories:
    never joins the exit code, even under --strict — a warn-tier checker
    feature mints no SR and gates nothing (WI-129/132). A TC's owning SRs
    resolve through both its direct `Verifies` SR cites and the SR-Refs of
    every LLR it cites."""
    sr_by_id = {r.get("SR-ID"): r for r in srs if r.get("SR-ID")}
    llr_srs = {}  # LLR id -> [owning SR ids]
    for r in llrs:
        lid = r.get("LLR-ID")
        if lid:
            llr_srs[lid] = [x for x in refs(r.get("SR-Refs")) if x in sr_by_id]

    def _flagged(sr_ids):
        return any(
            is_modified(sr_by_id[s]) or is_drafted(sr_by_id[s])
            for s in sr_ids
            if s in sr_by_id
        )

    out = []
    for r in llrs:
        lid = r.get("LLR-ID")
        if not lid or not is_modified(r):
            continue
        owners = llr_srs.get(lid, [])
        if not owners:
            # Adversarial-review F8: a Modified child with NO resolvable owning
            # SR is the maximally-invisible case — no SR line to ride, no gate
            # pull, no brief section. The dangling ref itself is the orphan
            # rules' finding; THIS warn is about the marker having no surface.
            out.append(
                "LLR {} is Modified but resolves NO owning SR — the marker "
                "rides no surface (no projection line, no gate pull, no brief "
                "section); fix the SR-Refs and flip the owning SR".format(lid)
            )
        elif not _flagged(owners):
            out.append(
                "LLR {} is Modified but its owning SR ({}) reads Approved — the "
                "SR is the attestation unit and a Modified row never counts as "
                "drifted, so no brief, projection or gate carries this "
                "amendment; flip the owning SR".format(lid, ";".join(owners))
            )
    for r in tcs:
        tid = r.get("TC-ID")
        if not tid or not is_modified(r):
            continue
        owners = []
        for x in refs(r.get("Verifies")):
            if x in sr_by_id:
                owners.append(x)
            elif x in llr_srs:
                owners.extend(llr_srs[x])
        if not owners:
            out.append(
                "TC {} is Modified but resolves NO owning SR — the marker "
                "rides no surface (no projection line, no gate pull, no brief "
                "section); fix the Verifies chain and flip the owning "
                "SR".format(tid)
            )
        elif not _flagged(owners):
            out.append(
                "TC {} is Modified but its owning SR ({}) reads Approved — the "
                "SR is the attestation unit and a Modified row never counts as "
                "drifted, so no brief, projection or gate carries this "
                "amendment; flip the owning SR".format(
                    tid, ";".join(sorted(set(owners)))
                )
            )
    return out


# Verification methods whose approval rests on a recorded human judgment,
# not a runnable check (process.md §4 "Attest"). --require-verified accepts these
# as legitimately approved but the report surfaces them distinctly (the
# verification-basis split), so an audit can always see how much rests on trust.
ATTESTED_METHODS = {"Attest"}
# The one method whose approval rests on a runnable, re-executable check
# (process.md §4 "Test"). Everything that is neither Test nor an ATTESTED_METHOD
# (Demonstration/Manual/Analysis/Inspection/Critique) rests on a human observing
# an outcome — repeatable, but not a runnable check — and is reported as its own
# "demonstrated/observed" category, so the audit never over-counts what rests on
# runnable checks (WI-259: the split is three-way, not attested-vs-everything-else).
MECHANIZED_METHODS = {"Test"}


def id_key(label):
    return label + "-ID"


def id_sort_key(rid):
    """Numeric-then-lexical sort key for a registry id, so SR-9 orders before
    SR-10: ids are `<TIER>-<digits>` with no zero-padding contract, so a plain
    string sort mis-orders once a tier crosses a digit width."""
    m = re.search(r"\d+", rid or "")
    return (0, int(m.group()), rid) if m else (1, 0, rid or "")


def integrity_findings(label, raw_rows):
    """Duplicated or malformed ids in one registry (example '-000' rows skipped —
    those are the placeholder check's job, never an integrity error)."""
    key, pattern = id_key(label), ID_PATTERNS[label]
    found, seen = [], set()
    for r in raw_rows:
        rid = r.get(key)
        if not rid or not rid.strip():
            # A row with content but a blank id is a live requirement that just
            # vanished from every join (a one-cell edit slip) — integrity-class,
            # wrong at any stage. Fully blank rows stay a non-finding.
            if any((v or "").strip() for k, v in r.items() if k != key):
                found.append(f"{label} row with non-empty cells but no {key}")
            continue
        if is_example(rid):
            continue
        # Duplication is checked FIRST so a repeated id reports "duplicated" even
        # when it is also malformed — otherwise a malformed id seen twice
        # re-reported "malformed" and never "duplicated" (both are integrity
        # failures, but the second occurrence's fact is that it repeats).
        if rid in seen:
            found.append(f"{label} id {rid} is duplicated")
        elif not pattern.match(rid):
            found.append(f"{label} id {rid!r} is malformed (expected {label}-<digits>)")
        seen.add(rid)
    return found


def enum_integrity_findings(label, rows):
    """Out-of-vocabulary values in the INTEGRITY_ENUM_COLS columns of one
    registry — today that is `Status` and nothing else.

    THE SAME `ENUM_FIELDS` TABLE `schema_findings` reads, deliberately: a tier's
    vocabulary has ONE home whatever pipe enforces it, so this is a change to
    *which list a value's finding is appended to*, never a second copy of the
    allowed set that can drift from the first. The split exists because the two
    pipes run at different gates — schema at DevBar-Release only, integrity
    always — and a retired Status word is wrong at every stage (D-9 correction
    C1).

    Placeholder `-000` rows are skipped, like every other rule here: a shipped
    template's example row is the placeholder check's business."""
    key = id_key(label)
    out = []
    for r in rows:
        rid = (r.get(key) or "").strip()
        if not rid or is_example(rid):
            continue
        for col in sorted(INTEGRITY_ENUM_COLS):
            allowed = ENUM_FIELDS.get(label, {}).get(col)
            if not allowed:
                continue
            val = (r.get(col) or "").strip()
            if val and val not in allowed:
                out.append(
                    "{} {} has {}={!r}, which is not in the closed vocabulary "
                    "(allowed: {})".format(
                        label, rid, col, val, ", ".join(sorted(allowed))
                    )
                )
    return out


# --- the id watermark: an id is allocated once, for the life of the repo -------
# Duplicate ids already error (integrity_findings above, sn_integrity_findings for
# the prose tier, check_trajectory.load_wis for WI). REUSE does not: every one of
# those checks reads only the LIVE tree, so an id freed by deleting its row is
# invisible and can be minted again. That matters because a reused id silently
# re-points history — every commit message, log entry and archived document that
# cites it now names a different thing — and no check can see it after the fact.
#
# The mark closes that. It is machine-written, machine-read, never hand-authored
# (the §6 F-3 `anchor` class), and it is the SOURCE a mint counts from, rather
# than `max(live) + 1`.
WATERMARK = "docs/id-watermark"
# Every id space in the repo: the ten this module already patterns, plus the four
# it does not (SN is the prose tier, WI is directory-as-state, OI is the owner
# queue, DP is a plan-round directory). Keyed off ID_PATTERNS so a space added
# there cannot be silently exempt here — tests/test_id_watermark.py pins the set.
WATERMARK_SPACES = tuple(sorted(set(ID_PATTERNS) | {"SN", "WI", "OI", "DP"}))
_WATERMARK_LINE = re.compile(r"^([A-Z]+)\s*=\s*(\d+)\s*$")
_ANY_ID = re.compile(r"^([A-Z]+)-(\d+)$")


def _csv_ids(docs):
    """`(space, number)` for the id cell of every row in every registry CSV.

    Swept by LOCATION, not by a known-file list: a registry this script never
    joins, a project's own addition, and a legacy `work-items.csv` no reader
    looks at all still HOLD their numbers."""
    for sub in ("requirements", "test"):
        directory = docs / sub
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.csv")):
            rows = load_csv(path)
            if not rows:
                continue
            # The row's OWN id is its FIRST column, never "the first id-shaped
            # cell". Those differ the moment a registry puts a reference column
            # first (`SN-Refs` before `SR-ID`): the scan would then yield the
            # CITATION and skip the id, leaving that row's number unmarked and
            # therefore free — an UNDER-count, the one direction this scan must
            # not fail in. Surplus cells land under the `None` key as a list, so
            # only the named first column is read.
            id_col = next(iter(rows[0]))
            for row in rows:
                match = _ANY_ID.match((row.get(id_col) or "").strip())
                if match:
                    yield match.group(1), int(match.group(2))


def _spine_ids(docs):
    """`(space, number)` per SR/LLR/TC row, through the CARRIER.

    `_csv_ids` above sweeps by LOCATION, and that caught the three row tiers only
    while they were CSVs. The D-5 carrier cutover moved them to TOML and the
    glob then matched NOTHING for them — silently — so rule 2 ("no live id
    exceeds its mark") went VACUOUS on three of the four spine tiers, which are
    precisely the tiers with NO minter: a hand-authored id arriving past the
    mark is the only signal there is. It was already false-green when found
    (LLR-167 and TC-161 stood above their marks, zero findings reported).

    So this reads through `spine_carrier` — the sanctioned reader, which
    resolves whichever carrier is live — instead of assuming a suffix. A path
    glob can be un-wired by moving a file; a carrier resolve cannot.

    `SPINE_FILES` is defined further down the module and referenced at CALL
    time, which is deliberate: the paths belong beside the joins that use them,
    and duplicating them here is exactly the second home this scan is being
    fixed for."""
    for rel, id_col in SPINE_FILES:
        # `SPINE_FILES` holds repo-root-relative paths; `docs` is <root>/docs.
        for row in spine_carrier.load(docs.parent / rel, id_col):
            match = _ANY_ID.match(str(row.get(id_col) or "").strip())
            if match:
                yield match.group(1), int(match.group(2))


def _offspine_ids(docs):
    """`(space, number)` per row of the numbered OFF-SPINE registries.

    The same hole `_spine_ids` documents, one carrier batch later and found the
    same way — by minting past the mark and getting no finding. Batch-2 moved
    `open-items` off CSV, so `_csv_ids`' `requirements/*.csv` glob stopped
    matching it and rule 2 went VACUOUS for the `OI` space: OI-26 was live
    against a mark of 14 with `--strict` reporting nothing. That space has no
    minter either, so a hand-authored id past the mark is again the only signal.

    Read through `spine_carrier` for the same reason `_spine_ids` does — a glob
    is un-wired by moving a file, a carrier resolve is not. `agents` is
    deliberately absent: its ids are names (`ANTHROPIC-FABLE`), not numbers, so
    it holds no watermark space to lose."""
    # interfaces + components joined the TOML carrier at WI-443, which un-wired
    # them from `_csv_ids`' glob exactly as batch-2 did to open-items — found
    # the same way again (WI-454 minted IF-121/122 past a mark of 120 and got
    # no finding). external.toml is deliberately absent: its B/EXT/REL spaces
    # are not watermark spaces.
    for rel, id_col in (
        ("docs/requirements/open-items.toml", "OI-ID"),
        ("docs/requirements/interfaces.toml", "IF-ID"),
        ("docs/requirements/components.toml", "CMP-ID"),
    ):
        for row in spine_carrier.load(docs.parent / rel, id_col):
            match = _ANY_ID.match(str(row.get(id_col) or "").strip())
            if match:
                yield match.group(1), int(match.group(2))


def _sn_ids(docs):
    """`("SN", number)` per declared stakeholder need, through the CARRIER.

    Was a markdown-row regex, which over the TOML carrier matches NOTHING —
    silently, and the id-watermark check it feeds would then never see an SN at
    all: the mark could not rise, and a retired number could be handed out
    again with nothing to say so. `load_needs` answers whichever
    carrier is live and yields the same ids the markdown rows did."""
    path = docs / "requirements" / "stakeholder-needs.toml"
    for need in spine_carrier.load_needs(path):
        match = re.match(r"SN-(\d+)$", str(need.get("id") or "").strip())
        if match:
            yield "SN", int(match.group(1))


def _wi_ids(docs):
    """`("WI", number)` per spec FILENAME under docs/work — filenames, never row
    contents, because `read_spec_rows` drops a malformed spec silently while its
    id stays taken."""
    work = docs / "work"
    if not work.is_dir():
        return
    for path in work.rglob("WI-*.md"):
        match = re.match(r"^WI-(\d+)-", path.name)
        if match:
            yield "WI", int(match.group(1))


def _dp_ids(docs):
    """`("DP", number)` per dual-plan round directory."""
    plans = docs / "plans"
    if not plans.is_dir():
        return
    for path in plans.iterdir():
        match = re.match(r"^DP-(\d+)-", path.name) if path.is_dir() else None
        if match:
            yield "DP", int(match.group(1))


def live_max_ids(root):
    """`{space: highest id number currently present}` over the WHOLE repo.

    Deliberately broader than any loader, and `-000` placeholders are COUNTED:
    for a mark that is the safe direction, since counting something extra only
    raises the floor while missing something lowers it and frees an id.
    (`intake.next_wi_id` states the same rule for its own mint: "for a MINT, an
    id held anywhere is an id taken".)"""
    docs = Path(root) / "docs"
    top = {}
    for reader in (_csv_ids, _spine_ids, _offspine_ids, _sn_ids, _wi_ids, _dp_ids):
        for space, num in reader(docs):
            if space in WATERMARK_SPACES and num > top.get(space, 0):
                top[space] = num
    return top


def read_watermark(root):
    """`{space: int}` from `docs/id-watermark`. RAISES on absent or malformed.

    Every other declared-file reader in this kit degrades to empty on a missing
    file, and that is right for a floor, an allowlist or a census — the absence
    means "nothing declared". Here it would mean "no id is taken", which frees
    every space at once and is exactly the failure the mark exists to prevent.
    So this one fails LOUD, and a malformed line is refused rather than skipped:
    a line nobody can parse is a space with no mark, which is the same hole."""
    path = Path(root) / WATERMARK
    if not path.is_file():
        raise ValueError(
            "{} is missing — the id watermark is the only record of which ids "
            "have ever been allocated, and without it a deleted id can be "
            "re-minted. Regenerate with `trace.py --bump-ids`.".format(WATERMARK)
        )
    marks = {}
    for lineno, line in enumerate(
        path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1
    ):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        m = _WATERMARK_LINE.match(text)
        if not m:
            raise ValueError(
                "{}:{}: not a `<SPACE> = <int>` line: {!r}".format(
                    WATERMARK, lineno, line
                )
            )
        marks[m.group(1)] = int(m.group(2))
    return marks


def _mark_covers_live_findings(marks, live):
    """Rules 1 and 2, read from the working tree alone: every space is marked,
    and no live id stands above its mark."""
    out = []
    for space in WATERMARK_SPACES:
        if space not in marks:
            out.append(
                "id watermark declares no mark for {} — every id space must be "
                "marked, or that space is unguarded".format(space)
            )
        elif live.get(space, 0) > marks[space]:
            out.append(
                "{}-{:03d} exists but the id watermark stands at {} — record it "
                "with `trace.py --bump-ids` (the spine tiers have no minter, so a "
                "hand-authored id is expected to arrive this way; the mark is what "
                "stops the number being handed out again after the row is "
                "deleted)".format(space, live[space], marks[space])
            )
    return out


def _mark_history_findings(marks, live, previous):
    """Rules 3 and 4, which need the COMMITTED mark: it never falls, and it never
    rises past what history justifies.

    Both directions matter and for opposite reasons. A mark that FALLS re-opens
    every id above the new value. A mark that RISES by hand retires that space's
    guard permanently and silently — it would still pass "every space is marked"
    and still pass "the mark rose". Headroom left by a DELETED row stays legal,
    because the committed mark is what carries it."""
    out = []
    for space in WATERMARK_SPACES:
        now = marks.get(space)
        if now is None:
            continue
        was = previous.get(space, 0)
        if now < was:
            out.append(
                "id watermark for {} moved DOWN {} -> {}; a mark only ever "
                "rises, or a retired id becomes mintable again".format(space, was, now)
            )
            continue
        justified = max(was, live.get(space, 0))
        if now > justified:
            out.append(
                "id watermark for {} stands at {} but nothing justifies more than "
                "{} (the highest committed mark, or the highest live id) — a mark "
                "rises by allocating an id, never by hand".format(space, now, justified)
            )
    return out


def watermark_findings(root, previous=None):
    """The id-watermark rules, integrity-class.

    `previous` is the committed mark (see `committed_watermark`). When git cannot
    supply one, the history rules DO NOT RUN and the caller says so — an unrun
    rule that prints nothing is indistinguishable from one that passed."""
    try:
        marks = read_watermark(root)
    except ValueError as exc:
        return [str(exc)]
    live = live_max_ids(root)
    out = _mark_covers_live_findings(marks, live)
    if previous is not None:
        out += _mark_history_findings(marks, live, previous)
    return out


def render_watermark(marks, basis=""):
    """The file's text. One `<SPACE> = <int>` per line, deliberately: a merge
    conflicts per SPACE rather than per file, and a bump can be a line rewrite."""
    head = [
        "# ID WATERMARK — generated by scripts/trace.py --bump-ids (do not hand-edit).",
        "#",
        "# The highest id ever allocated in each space. A mint counts from HERE,",
        "# never from max(live): deleting a row frees its number in the live tree,",
        "# and re-using it silently re-points every commit message, log entry and",
        "# archived document that cites that id at a different thing.",
        "#",
        "# A mark only ever RISES. Lowering one is refused by trace.py's integrity",
        "# pass, which also refuses a live id above its mark and a missing space.",
        "#",
    ]
    if basis:
        head.append("# basis: {}".format(basis))
        head.append("#")
    body = ["{} = {}".format(space, marks.get(space, 0)) for space in WATERMARK_SPACES]
    return "\n".join(head + body) + "\n"


def _watermark_at(root, rev):
    """The mark as recorded at `rev`, or None when git cannot produce it."""
    text = _git_out(root, ["show", "{}:{}".format(rev, WATERMARK)])
    if not text:
        return None
    marks = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = _WATERMARK_LINE.match(stripped)
        if not m:
            # A line the reader would REFUSE must not be dropped here. Skipping
            # it silently disables monotonicity for that space alone, which is
            # the per-space version of the hole this rule exists to close.
            return None
        marks[m.group(1)] = int(m.group(2))
    return marks or None


def committed_watermark(root):
    """The highest mark per space across HEAD **and every other parent**.

    Monotonicity cannot be read from the working tree — a lowered mark looks
    exactly like a correct one — so it is read from git. But `HEAD:` alone is
    FIRST-PARENT ONLY, and a merge is exactly where marks get lost: two branches
    each allocate ids, `docs/id-watermark` conflicts (by design, one line per
    space), and resolving it `--ours` discards the other side's marks while
    every commit message on that branch still cites them. Comparing against the
    max over all parents makes that resolution a finding instead of a silent
    re-issue.

    `MERGE_HEAD` covers the in-progress case (the conflict is being resolved
    right now); `HEAD^1..^n` covers the commit after it landed. Returns None
    only when git can supply NO baseline at all — off-git, a shallow clone, or
    before the file's first commit — and the caller then reports the rule as
    SKIPPED rather than passing it quietly."""
    revs = ["HEAD"]
    merge_head = _git_out(root, ["rev-parse", "--verify", "--quiet", "MERGE_HEAD"])
    if merge_head:
        revs.append(merge_head.strip())
    parents = _git_out(root, ["rev-list", "--parents", "-n", "1", "HEAD"]) or ""
    revs.extend(parents.split()[1:])
    best = {}
    seen_any = False
    for rev in revs:
        marks = _watermark_at(root, rev)
        if marks is None:
            continue
        seen_any = True
        for space, value in marks.items():
            best[space] = max(best.get(space, 0), value)
    return best if seen_any else None


def bump_watermark(root):
    """Raise every mark to the live maximum. Returns `(marks, raised)`.

    A MALFORMED file propagates its error. Only an ABSENT one starts from zero,
    and only because that is the file's first creation. The distinction is the
    whole safety of the writer: this is the one artifact in the repo whose
    content cannot be recomputed, so "I could not read it" must never become "I
    will replace it with the live maximum" — that discards every mark for an id
    already deleted, which is precisely the record the file exists to keep. The
    trap is real rather than theoretical, because `read_watermark`'s own error
    text sends the reader here to regenerate."""
    live = live_max_ids(root)
    path = Path(root) / WATERMARK
    marks = read_watermark(root) if path.is_file() else {}
    raised = {}
    for space in WATERMARK_SPACES:
        was = marks.get(space, 0)
        now = max(was, live.get(space, 0))
        if now != was:
            raised[space] = (was, now)
        marks[space] = now
    basis = " ".join(
        "{}={}".format(s, live.get(s, 0)) for s in WATERMARK_SPACES if live.get(s)
    )
    (Path(root) / WATERMARK).write_text(
        render_watermark(marks, basis), encoding="utf-8", newline="\n"
    )
    return marks, raised


def triangle_findings(tcs, llrs):
    """SR/LLR citation coherence. A TC may cite an
    SR and an LLR together so one test discharges both the "SR needs a TC" and
    "LLR needs a TC" rules; the SR<->LLR relationship itself is recorded
    canonically on the LLR's SR-Refs. This keeps the derived citation honest: when
    a TC cites both an SR and an LLR, each cited LLR must descend from one of the
    SRs the same TC cites (its SR-Refs must intersect them). An incoherent pairing
    (a TC citing LLR-1 next to SR-2 when LLR-1 decomposes SR-1) is wrong at any
    stage, so it joins the integrity floor, not the gate-scoped orphan set. A TC
    that cites only LLRs (no SR) has no SR to contradict — the orphan rules cover
    it. An LLR with no SR-Refs is already an orphan, so it is not double-reported."""
    llr_parents = {
        r["LLR-ID"]: set(refs(r.get("SR-Refs"))) for r in llrs if r.get("LLR-ID")
    }
    out = []
    for r in tcs:
        tid = r.get("TC-ID")
        if not tid:
            continue
        cited = refs(r.get("Verifies"))
        cited_srs = {x for x in cited if ID_PATTERNS["SR"].match(x)}
        if not cited_srs:
            continue
        for x in cited:
            parents = llr_parents.get(x)
            if parents and not (parents & cited_srs):
                out.append(
                    "TC {} cites {} alongside SR {} but {} decomposes {} (its "
                    "SR-Refs) — an SR/LLR pair in one TC must share the parent "
                    "link recorded on the LLR".format(
                        tid,
                        x,
                        ", ".join(sorted(cited_srs)),
                        x,
                        ", ".join(sorted(parents)),
                    )
                )
    return out


# The module-path normalizer MOVED TO trace_text.py at re-tier v2 S5 (WI-464),
# unchanged: `if_this_project_advisories` compares the same two naming conventions
# and is a pure row predicate, so keeping one home there beat a fourth copy here.
# Aliased back under the private name so this module's call sites read as before.
_norm_module = norm_module


def interface_findings(ifs, sr_ids, module_ids):
    """The IF-### seam tier's back-link checks (process.md §8), closing the gap
    where trace.py never read the interface catalog (WI-056). Returns
    ``(findings, advisories)``: *findings* join the --strict failure set like PB's
    back-links (an IF row's Req-Refs is empty or names an unknown SR — every seam
    links the spine so it stays transitively TC-covered); *advisories* are
    warn-only (an IF row's ThisProject endpoint resolves to no LLR Module after
    normalization). The endpoint join is best-effort: the LLR Module set is a
    partial, differently-named inventory, so the authoritative module-coverage
    check lives in check_trajectory against the full arch-map."""
    findings, advisories = [], []
    norm_modules = {_norm_module(m) for m in module_ids}
    norm_modules.discard("")
    for r in ifs:
        iid = r["IF-ID"]
        srrefs = refs(r.get("Req-Refs"))
        if not srrefs:
            findings.append(f"IF {iid} links no SR (Req-Refs is empty)")
        for x in srrefs:
            if x not in sr_ids:
                findings.append(f"IF {iid} references unknown {x}")
        endpoint = (r.get("ThisProject") or "").strip()
        if norm_modules and endpoint and _norm_module(endpoint) not in norm_modules:
            advisories.append(
                f"IF {iid} ThisProject={endpoint!r} matches no LLR Module "
                "(best-effort join; a module with no LLR is legitimate — "
                "check_trajectory's arch-map coverage is the full check)"
            )
    return findings, advisories


def tc_citation_findings(tcs, spine_ids, ifs):
    """Every TC-`Verifies` orphan rule, as ``[(at_fault_id, finding), ...]``.

    The vocabulary is SR/LLR spine ids **plus** `IF-###` seam ids (WI-065). The
    seam-TC rule (process-options.md "Intra-repo interfaces & the architecture
    graph") asks an `Active` seam to be cited by a TC, and `check_trajectory`
    reads that citation out of **this same cell** — so rejecting `IF-###` here
    made the documented citation unsatisfiable: it passed one check and orphaned
    under the other. Ruled in favour of ONE citation cell rather than a second
    column: a TC states everything it verifies in one place, and trace already
    loads `interfaces.csv`, so the join is free.

    Two rules keep the widened vocabulary from becoming a hole: an unresolvable
    IF token is as wrong as an unknown SR, and a seam citation **supplements**
    the spine citation — a TC naming only seam ids no longer says which
    requirement it discharges."""
    if_ids = {r["IF-ID"] for r in ifs}
    out = []
    for r in tcs:
        tid = r["TC-ID"]
        verified = refs(r.get("Verifies"))
        if not verified:
            out.append((tid, f"TC {tid} verifies nothing"))
        elif not spine_ids & set(verified):
            out.append(
                (
                    tid,
                    f"TC {tid} cites only seam id(s) — a seam citation "
                    "supplements the spine citation, so name the SR and/or LLR "
                    "this test verifies",
                )
            )
        for x in verified:
            if x not in spine_ids and x not in if_ids:
                out.append((tid, f"TC {tid} references unknown {x}"))
    return out


def placeholder_findings(label, raw_rows):
    """Leftover template example rows (ids ending '-000') in one registry."""
    key = id_key(label)
    return [
        f"{label} placeholder row {r[key]} still present "
        "(replace the template example before this gate)"
        for r in raw_rows
        if r.get(key) and is_example(r[key])
    ]


def scan_sn_placeholders(sn_md):
    """Sorted unique '-000' SN ids still present in the needs registry.

    `sn_md` is the CARRIER-RESOLVED path the loader found, so None here means
    the registry is genuinely absent rather than "not under the suffix I
    guessed"."""
    if sn_md is None or not sn_md.exists():
        return []
    text = sn_md.read_text(encoding="utf-8-sig", errors="replace")
    return sorted({u for u in re.findall(r"\bSN-\d+\b", text) if is_example(u)})


# SN maturity lives in section-as-state (derived-gate model §4a): a stakeholder-
# needs.md heading whose text contains "draft" (case-insensitive, e.g. `## Draft
# needs (unratified)`) marks the SNs under it as Draft (unratified, DevBar-Below); SNs under
# any other heading are ratified (DevBar-Reqs). No new column — the state IS the section,
# and the ratification date is git-derived (the commit that moved the row out of
# the draft section). This is the SN analogue of the `Status=Draft` bit on
# SR/LLR/TC rows.
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)")


def sn_all_ids(text):
    """The SN id UNIVERSE: every `SN-###` token anywhere in stakeholder-needs.md
    `text`, whole-text — a prose mention counts exactly like a table row, which
    is the sharp edge registry-machinery-reference §2.1 records (ratified +
    uncited caps the derived gate at DevBar-Below since WI-401). `-000` placeholders
    excluded. Duplicated in derive_gate.py per the F5 rule; pinned equal by
    test_rule_sync (WI-408), because this scrape decides which ids BOTH
    surfaces run their rules over."""
    return {u for u in re.findall(r"\bSN-\d+\b", text) if not is_example(u)}


def sn_draft_ids(text):
    """The set of Draft SN ids in a needs registry's `text`, through whichever
    CARRIER wrote it.

    Under TOML draft-ness is a FIELD on the need (`kind = "draft"`); under the
    legacy markdown it was SECTION-AS-STATE — every `SN-###` appearing under a
    heading containing the word "draft". Both are read; the dispatch is
    `spine_carrier.needs_from_text`, and it is load-bearing rather than tidy: a
    heading scan over a TOML file finds NO headings, reports ZERO drafts, and
    every draft need reads as ratified — which floats the derived gate upward.
    A migration whose failure mode is "the gate rises" is the one shape this
    repo can least afford, so the carrier is sniffed rather than assumed.

    Retiring section-as-state also closes a live sharp edge the 2026-08-10
    sitting hit: a prose MENTION of an id under the draft heading silently
    re-drafted an already-attested need, because the id universe is a whole-text
    scrape while draft-ness was a heading scan. A field cannot be set by
    mentioning the id in a sentence. `-000` placeholders stay excluded.
    Duplicated in derive_gate.py per the F5 rule; pinned equal by
    test_rule_sync."""
    return spine_carrier.draft_ids_from_text(text)


def sn_cited_ids(srs):
    """Every SN id cited by >=1 SR row's `SN-Refs` cell — the coverage set the
    "SN has no SR" orphan rule reads (and, since WI-401, the gate input behind
    derive_gate.py's SN-coverage rung: that rung caps the raw level, this
    listing itemizes the ids at DevBar-Tests strictness). No filtering here: -000 rows
    are excluded by the caller's row filter, and a Draft SR's citation is
    deliberately in the set. Duplicated in derive_gate.py per the F5 rule;
    pinned equal by test_rule_sync."""
    return {x for r in srs for x in refs(r.get("SN-Refs"))}


def sn_integrity_findings(sn_text):
    """Duplicate-id protection for the SN tier — the one tier stored as prose,
    and until now the one tier without it (every CSV tier gets
    integrity_findings). Two shapes are wrong at any stage: an SN id on more
    than one `|SN-###|` table row (a copy-pasted row; _sn_prose last-wins
    silently otherwise), and an id under BOTH a draft and a non-draft heading
    (simultaneously exempt from the child rules and ratified — sn_draft_ids
    marks it draft, silently exempting a ratified need)."""
    row_counts = {}
    draft_rows, ratified_rows = set(), set()
    in_draft = False
    for line in sn_text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            in_draft = "draft" in m.group(1).lower()
            continue
        rm = re.match(r"\|\s*(SN-\d+)\s*\|", line)
        if not rm or is_example(rm.group(1)):
            continue
        rid = rm.group(1)
        row_counts[rid] = row_counts.get(rid, 0) + 1
        (draft_rows if in_draft else ratified_rows).add(rid)
    out = []
    for rid in sorted(row_counts, key=id_sort_key):
        if row_counts[rid] > 1:
            out.append(f"SN id {rid} is duplicated ({row_counts[rid]} table rows)")
    for rid in sorted(draft_rows & ratified_rows, key=id_sort_key):
        out.append(f"SN id {rid} appears under both a draft and a non-draft heading")
    return out


def schema_findings(label, rows):
    """Empty required fields and out-of-vocabulary Verification/Tier values, over
    the real (non-placeholder) rows of one registry."""
    key = id_key(label)
    out = []
    for r in rows:
        rid = r[key]
        for col in REQUIRED_FIELDS[label]:
            if not (r.get(col) or "").strip():
                out.append(f"{label} {rid} has empty required field {col}")
        for col, allowed in ENUM_FIELDS.get(label, {}).items():
            if col in INTEGRITY_ENUM_COLS:
                continue  # `enum_integrity_findings` owns these — see that name
            val = (r.get(col) or "").strip()
            if val and val not in allowed:
                out.append(
                    f"{label} {rid} has {col}={val!r} (allowed: "
                    f"{', '.join(sorted(allowed))})"
                )
        # A TC claiming Automated=Yes must
        # cite its Evidence (pytest node / path / procedure link) — a
        # claimed-automated test with no cited location is a soft false-green.
        # Conditional on the claim, so it can't live in REQUIRED_FIELDS; a
        # legacy CSV without the column reads as empty and is flagged the same
        # way (the ADOPTING §6 migration adds the column).
        if label == "TC" and (r.get("Automated") or "").strip().lower() == "yes":
            if not (r.get("Evidence") or "").strip():
                out.append(
                    f"TC {rid} is Automated=Yes but cites no Evidence "
                    "(name the test: a pytest node, script path, or "
                    "procedure-doc link)"
                )
    return out


def schema_advisories(label, rows):
    """`schema_findings`' warn-first twin, for the tiers whose schema is stated
    but not yet promoted to a gate (IF, CMP — WI-443 / OI-14 part B).

    SAME two dictionaries, deliberately: the vocabulary of a tier has ONE home
    whatever the enforcement level reads it at, so promoting IF to ERROR later is
    a change to which list a caller appends to, never a second copy of the
    allowed values that can drift from this one. Returns advisory strings; the
    caller routes them into the warn pipe, and nothing here reaches an exit
    code.

    An adversarial round proposed HARDENING the required-field half to match
    the CSV era and the proposal was REFUTED on measurement: the IF tier had
    NO cell-level guarantee on CSV (no schema tier existed at all — the OI-14
    finding), and the structural floor's TOML equivalent is the carrier parse
    error plus the dual-carrier refusal, both already hard. Hardening
    cell-emptiness here would red every migrating adopter for a guarantee the
    registry never had; the ruled warn-first-then-promote path stands."""
    key = id_key(label)
    out = []
    for r in rows:
        rid = r.get(key) or "(unnamed row)"
        for col in REQUIRED_FIELDS[label]:
            if not (r.get(col) or "").strip():
                out.append(f"{label} {rid} has empty required field {col}")
        for col, allowed in ENUM_FIELDS.get(label, {}).items():
            val = (r.get(col) or "").strip()
            if val and val not in allowed:
                out.append(
                    f"{label} {rid} has {col}={val!r}, which is not in the closed "
                    f"vocabulary (allowed: {', '.join(sorted(allowed))})"
                )
    return out


def frame_findings(exts, bifs, rels):
    """Reference resolution inside `external.toml` (WI-442, §1R.5) as a list of
    finding strings — the frame's own join rules.

    PLAIN STRINGS, not the `(at_fault_id, finding)` pairs the spine's older rules
    return. The pair shape was written here first and NO caller ever read the id,
    which documents a contract that does not exist; `tc_citation_findings` keeps
    its pairs because its caller genuinely keys on them.

    It checks three reference fields — a boundary row's `Entity`, and a
    relationship's `From` and `To` — and they are the only structural claims the
    ruled schema makes. Everything else about the frame — is it the RIGHT frame,
    are the crossings complete — is a human ruling, and a check that pretended
    otherwise would be inventing a rule nobody wrote.

    FAILURE CLASS, not advisory, unlike the schema tier beside it. A tie-back to
    an entity that does not exist is not a maturing corpus converging on a
    vocabulary; it is a dangling reference, exactly like an SR citing an SN that
    was deleted, and the spine's other reference rules have been hard since they
    shipped. Note what it does NOT check: a relationship carries no interface
    vocabulary by design, so there is nothing here that could grow one.

    NO ENTITIES IS ONLY VACUOUS WHEN NOTHING REFERENCES THEM, and getting that
    wrong was a false green — the one failure this file exists to prevent. The
    first version returned `[]` on an empty entity set, reasoning that the rules
    below had nothing to resolve against. They did: 6 crossings referencing 5
    entities that do not exist resolved to silence, and `_frame_report_section`
    then printed "every crossing Entity ... resolves" over the top of it. That is
    the natural state of a half-authored frame (you draw the boundary, then name
    who is on the far side) and of a refactor that drops an entity block. An
    empty frame is still vacuous; an empty entity set under a non-empty crossing
    or relationship set is a finding of its own."""
    out = []
    ext_ids = {r["EXT-ID"] for r in exts}
    if not ext_ids:
        if bifs or rels:
            out.append(
                "external.toml declares {} crossing(s) and {} relationship(s) "
                "but NO entity — every reference in them resolves to "
                "nothing".format(len(bifs), len(rels))
            )
        return out
    for r in bifs:
        bid = r["B-ID"]
        for x in refs(r.get("Entity")):
            if x not in ext_ids:
                out.append(f"boundary {bid} Entity references unknown {x}")
    for r in rels:
        rid = r["REL-ID"]
        for col in ("From", "To"):
            for x in refs(r.get(col)):
                if x not in ext_ids:
                    out.append(f"relationship {rid} {col} references unknown {x}")
    return out


def sr_boundary_findings(srs, bifs, ifs):
    """SN-037's SR->boundary rule (WI-442), as `(findings, advisories)` — both
    plain lists of strings, per `frame_findings`' note on the pair shape.

    SN-037's ratified acceptance asks that *"every system-requirement input and
    output references a declared interface"* and that *"unresolved references ...
    are mechanical findings"*. Those are two obligations at two severities, and
    conflating them is what would make this check either useless or unshippable:

      * RESOLUTION IS HARD. An SR whose `Boundary-Refs` names a crossing that is not
        declared is a dangling reference, exactly like an SR citing a deleted SN,
        and it joins the --strict failure set with the spine's other reference
        rules. It is also the only half that can be true today.

      * COVERAGE IS ADVISORY, and deliberately so. Making "every SR names a
        crossing" an error would red 148 rows the moment the column existed, for
        work that belongs to the re-tier campaign (WI-451 slice 2) and under a
        form rule that is itself a GUIDELINE with recorded per-row waivers
        (2026-08-13v). A gate that is 100% red on the day it ships is a gate
        someone turns off. So the uncovered count is reported as ONE summary
        line — the number the campaign has to move — and never as 148 findings.

    THE THIRD CLAUSE IS NOT ENFORCED HERE. "Every declared component-boundary
    crossing has an interface row" is decision 6 (a BIF with no realizing IF),
    deferred BY RULING to post-schema, so this reports the realization gap as an
    advisory and gates nothing on it. `ifs` is read for exactly that count, and
    the same restraint is why `derive_gate.boundary_incomplete` reads approval
    and not realization.

    Vacuous with no frame registry: a project that declares no boundary has no
    crossing an SR could name."""
    findings, advisories = [], []
    bif_ids = {r["B-ID"] for r in bifs}
    if not bif_ids:
        return findings, advisories
    named = set()
    for r in srs:
        sid = r["SR-ID"]
        cited = refs(r.get("Boundary-Refs"))
        named.update(x for x in cited if x in bif_ids)
        for x in cited:
            if x not in bif_ids:
                findings.append(
                    f"SR {sid} Boundary-Refs references unknown crossing {x}"
                )
    uncovered = sum(1 for r in srs if not refs(r.get("Boundary-Refs")))
    if uncovered:
        advisories.append(
            "SR->boundary coverage: {} of {} requirement(s) name no crossing in "
            "Boundary-Refs (SN-037; the re-tier campaign is what moves this number, "
            "and a row that legitimately states no boundary observable records "
            "its reason rather than leaving a blank cell)".format(uncovered, len(srs))
        )
    unnamed = sorted(bif_ids - named)
    if unnamed:
        advisories.append(
            "boundary crossing(s) named by NO requirement: {} — a crossing with "
            "no SR is a frame nobody has stated an observable at".format(
                ", ".join(unnamed)
            )
        )
    realized = {
        x
        for r in ifs
        for col in ("InterfaceFromExternal", "InterfaceToExternal")
        for x in refs(r.get(col))
    }
    unrealized = sorted(bif_ids - realized)
    if unrealized:
        advisories.append(
            "boundary crossing(s) realized by NO interface row: {} — decision 6's "
            "question, deferred by ruling; reported, never gated".format(
                ", ".join(unrealized)
            )
        )
    return findings, advisories


def tieback_findings(ifs, bifs):
    """An IF row's directional tie-back must name a DECLARED crossing (WI-442,
    owner naming 13m), as a list of finding strings.

    Vacuous with no frame registry, which is the applies-when: a project without
    `external.toml` has no crossings to name, and a stray tie-back there is a
    schema question, not a resolution one.

    WHAT THIS CANNOT CATCH, said out loud because the template says it too: a
    tie-back that RESOLVES but does not belong — an internal seam claiming to
    realize B-05 — is indistinguishable from a correct one to any check. That
    judgment is the re-tier's and the reviewer's."""
    out = []
    bif_ids = {r["B-ID"] for r in bifs}
    if not bif_ids:
        return out
    for r in ifs:
        iid = r["IF-ID"]
        for col in ("InterfaceFromExternal", "InterfaceToExternal"):
            for x in refs(r.get(col)):
                if x not in bif_ids:
                    out.append(f"IF {iid} {col} references unknown crossing {x}")
    return out


def _frame_report_section(exts, bifs, rels, findings):
    """The report's depth-0 frame block (WI-442), or `[]` when no frame is
    declared — a named helper rather than another arm inside `render_report`,
    which the complexity ratchet holds at its committed count and which is
    already a long list-builder."""
    if not (exts or bifs or rels):
        return []
    body = (
        [
            "{} entity, {} boundary-crossing and {} relationship row(s); every "
            "crossing Entity, relationship From/To and IF tie-back "
            "resolves.".format(len(exts), len(bifs), len(rels))
        ]
        if not findings
        else ["- {}".format(f) for f in findings]
    )
    return ["", "## The depth-0 frame (external.toml resolution)", ""] + body


def if_contract_advisories(ifs):
    """The four ruled negative rules on an IF `Contract` cell (WI-443), all
    warn-first. See the `_IF_*` constants above for why form is the only thing a
    check can honestly read here."""
    out = []
    for r in ifs:
        iid = r.get("IF-ID") or "(unnamed row)"
        cell = (r.get("Contract") or "").strip()
        if not cell:
            continue
        for token in dict.fromkeys(_IF_WI_RE.findall(cell)):
            out.append(
                f"IF {iid} Contract names {token} — a work-item id belongs in the "
                "log, not in a live contract cell: it ages, and a cancelled id "
                "still reads as authority. Move it to Rationale or drop it."
            )
        for token in dict.fromkeys(_IF_DECISION_RE.findall(cell)):
            out.append(
                f"IF {iid} Contract cites decision {token} — a contract states "
                "what crosses, not which ruling shaped it. Move the citation to "
                "Rationale."
            )
        connective = _IF_CONNECTIVE_RE.search(cell)
        if connective:
            out.append(
                f"IF {iid} Contract argues ({connective.group(0)!r}) — that "
                "sentence is a rationale; the Rationale column is its home "
                "(process.md §8)."
            )
        if len(cell) > IF_CONTRACT_MAX:
            out.append(
                f"IF {iid} Contract is {len(cell)} characters (ceiling "
                f"{IF_CONTRACT_MAX}) — an interface states what crosses, typed; "
                "at this length it is carrying something else."
            )
    return out


# `EXTERNAL_ENDPOINT_PREFIX` (the declared "deliberately outside this tree" marker
# and the reasoning for a value-prefix over a column) MOVED TO trace_text.py at
# re-tier v2 S5 (WI-464), unchanged and imported back above: `_module_shaped` has
# to skip a marked endpoint too, and the endpoint value GRAMMAR is a text rule.


def if_endpoint_class_advisories(ifs, module_ids, root):
    """Classify every IF endpoint that is NOT an arch-map module, warn-first.

    THIS EXISTS BECAUSE THOSE ROWS WERE POLICED BY NOTHING, measured at
    `81a142c2`: 45 of 113 IF rows have at least one endpoint carrying no
    component tag, which makes `check_trajectory.cross_component_findings`
    VACUOUS for them — and the containment rule that was assumed to cover them
    cannot, because the two rules range over disjoint object classes. Containment
    tests that every arch-map MODULE is in some CMP; the untagged endpoints are
    data files, directories and external actors, which are never arch-map
    modules. So a green from either rule said nothing at all about these rows.

    THE RULE, since the 2026-08-15 rework (plan step 2): an endpoint — in
    `ThisProject` **or** `Counterpart` — that resolves to no module, no file and
    no directory AND carries no `external:` marker is a NAMED finding. A
    file/directory endpoint and a marked external one are both legitimate and
    stay counted-not-named; the summary still reports every class, because the
    vacuity it records is real whatever the endpoint turns out to be.

    Warn-first, like every rule in this pipe: it never joins a failure set at any
    gate. Promotion is a later, separate decision, and the reason to hold is that
    the marker is a NEW convention — an adopter mid-migration would be red for a
    vocabulary their registry predates."""
    norm_modules = {_norm_module(m) for m in module_ids}
    norm_modules.discard("")
    absences = _declared_absences(root)
    files, external, unknown, rows_hit = [], [], [], set()
    for r in ifs:
        iid = r.get("IF-ID") or "(unnamed row)"
        for col in ("ThisProject", "Counterpart"):
            # A `;`-joined cell is SEVERAL endpoints, and reading it as one is
            # how a real seam gets reported as a dangling path (IF-097 names
            # three modules). Split on `;` only — an endpoint may legitimately
            # contain a space (`downstream adopter`) or a comma.
            cell = (r.get(col) or "").strip()
            for endpoint in [e.strip() for e in cell.split(";") if e.strip()]:
                if endpoint.startswith(EXTERNAL_ENDPOINT_PREFIX):
                    rows_hit.add(iid)
                    named = endpoint[len(EXTERNAL_ENDPOINT_PREFIX) :].strip()
                    if named:
                        external.append(named)
                    else:
                        # A bare marker names nobody, which is the one way this
                        # convention can be worse than the guess it replaced.
                        unknown.append((iid, col, endpoint))
                    continue
                if _norm_module(endpoint) in norm_modules:
                    continue
                rows_hit.add(iid)
                if _resolves_in_tree(root, endpoint) or endpoint in absences:
                    files.append(endpoint)
                else:
                    unknown.append((iid, col, endpoint))
    if not rows_hit:
        return []
    out = [
        "IF endpoint coverage: {} of {} row(s) carry an endpoint that is not an "
        "arch-map module, so the cross-component rules are VACUOUS for them — "
        "{} resolve to a file or directory in the tree, {} are marked "
        "`external:`, {} resolve to nothing".format(
            len(rows_hit), len(ifs), len(files), len(external), len(unknown)
        )
    ]
    for iid, col, endpoint in unknown:
        out.append(
            "IF {} {}={!r} resolves to no module, file or directory — name a "
            "real endpoint, or mark it `{}<actor>` if it is deliberately "
            "outside this tree".format(iid, col, endpoint, EXTERNAL_ENDPOINT_PREFIX)
        )
    return out


def if_ownership_advisories(ifs, sr_ids, llr_ids):
    """The `Owner` cell's resolution + uniqueness rules, warn-first (Q1, ruled
    2026-08-15a; plan step 5).

    THE INVARIANT IS "EXACTLY ONE OWNER PER INTERFACE", and the ruling is what
    makes it hard to state in a column type: an owner may be a requirement
    (`SR-###`) **or** a design row (`LLR-###`), because *"requirements are just
    decomposition of needs into measurable objectives, and modules are just
    physical implementations at a lower level that do the same thing"*. So the
    cell is id-typed and POLYMORPHIC, resolved against whichever registry its
    prefix names, and the two failure modes are the two halves of "exactly one":
    naming nobody, and naming several.

    It is not the same question as `Req-Refs`. That cell lists every requirement
    the seam realizes or relies on — 21 of this repo's 115 rows list more than
    one — and none of them is thereby answerable FOR the seam. `Owner` names the
    one that is. Deriving it instead was the plan's first recommendation and Q1
    overturned it: a derived view can only surface what is already encoded, and
    `ThisProject` holds a module PATH, not a resolvable id.

    Warn-first, with the whole set: the cells were seeded mechanically from
    `Req-Refs` and every multi-ref pick is a provisional judgement recorded in
    the log, so a gate that reds on them would be gating on a guess."""
    out = []
    for r in ifs:
        iid = r.get("IF-ID") or "(unnamed row)"
        cell = (r.get("Owner") or "").strip()
        if not cell:
            continue  # the empty-required-field rule already says this
        owners = refs(cell)
        if len(owners) != 1:
            out.append(
                "IF {} Owner={!r} names {} owners — exactly one row is "
                "answerable for an interface (Q1, 2026-08-15); Req-Refs is "
                "where the several requirements it realizes or relies on "
                "go".format(iid, cell, len(owners))
            )
            continue
        oid = owners[0]
        if ID_PATTERNS["SR"].match(oid):
            known, tier = sr_ids, "system-requirements"
        elif ID_PATTERNS["LLR"].match(oid):
            known, tier = llr_ids, "low-level-requirements"
        else:
            out.append(
                "IF {} Owner={!r} is not an SR-### or LLR-### id — an owner is "
                "a requirement or a design row, id-typed (Q1, "
                "2026-08-15)".format(iid, oid)
            )
            continue
        if oid not in known:
            out.append(f"IF {iid} Owner references unknown {oid} ({tier})")
    return out


# The carriage depth this repo warns past. PROVISIONAL, and stated as a number
# rather than left implicit because Q3 created the obligation ("the carriage
# graph must be acyclic and its depth bounded") without fixing the bound. Two is
# the depth the ruling's own worked shape needs — *"6 IFs could have a
# destination of a larger IF"* is one carrier over its constituents — so a third
# level is a bundle inside a bundle, which may be right and should be looked at.
IF_CARRIAGE_MAX_DEPTH = 2


def if_carriage_advisories(ifs):
    """`CarriedBy` — interface composition, warn-first (Q3, ruled 2026-08-15a;
    plan step 7).

    *"An IF could feasibly have a destination of another IF, so 6 IFs could have
    a destination of a larger IF to carry them in a single definable signal."*
    A constituent names its carrier; several constituents riding one bundle name
    the same carrier id. Granularity stops being a forced choice — declare the
    bundle AND its parts, related by this link, and decompose only as far as is
    useful.

    THE OBLIGATION THE RULING CREATED is checked here, because a link that may
    point at another row of its own tier is representable as `IF-A carried by
    IF-B carried by IF-A`: the carriage graph must RESOLVE, must be ACYCLIC, and
    its depth is bounded. A cycle is reported once per row on it rather than once
    per traversal, so a two-row cycle reads as two findings and not as an
    infinite one.

    A row carrying itself is called out separately: it is a cycle, but the useful
    sentence is not "there is a cycle", it is "this cell should be empty"."""
    out = []
    ids = {r.get("IF-ID") for r in ifs if r.get("IF-ID")}
    carrier = {}
    for r in ifs:
        iid = r.get("IF-ID")
        cell = (r.get("CarriedBy") or "").strip()
        if not iid or not cell:
            continue
        named = refs(cell)
        if len(named) != 1:
            out.append(
                "IF {} CarriedBy={!r} names {} carriers — one constituent rides "
                "one bundle (Q3, 2026-08-15)".format(iid, cell, len(named))
            )
            continue
        cid = named[0]
        if not ID_PATTERNS["IF"].match(cid):
            out.append(f"IF {iid} CarriedBy={cid!r} is not an IF-### id")
            continue
        if cid == iid:
            out.append(f"IF {iid} CarriedBy names itself — leave the cell empty")
            continue
        if cid not in ids:
            out.append(f"IF {iid} CarriedBy references unknown {cid}")
            continue
        carrier[iid] = cid
    for start in sorted(carrier):
        seen, node, depth = {start}, carrier[start], 1
        while node in carrier:
            if node in seen:
                out.append(
                    "IF {} sits on a CarriedBy CYCLE — a bundle cannot be "
                    "carried by something it carries".format(start)
                )
                break
            seen.add(node)
            node, depth = carrier[node], depth + 1
        else:
            if depth > IF_CARRIAGE_MAX_DEPTH:
                out.append(
                    "IF {} is {} carriers deep (bound {}) — a bundle inside a "
                    "bundle may be right, but say why in Rationale (the bound "
                    "is provisional, Q3 2026-08-15)".format(
                        start, depth, IF_CARRIAGE_MAX_DEPTH
                    )
                )
    return out


def _declared_absences(root):
    """The paths `docs/declared-absences` says this repo deliberately does NOT
    carry — the THIRD reader of a file whose whole point is that the fact is
    stated once (`test_dogfood_sync` and `check_doc_refs` are the other two).

    An endpoint naming one of them is neither rot nor external: the layer is
    opt-in and switched off, and the row is honest about what the module would
    read if it were on. This repo's worked case is
    `docs/requirements/performance-budgets.csv` — check_perf's declared budgets
    registry, absent because process.md §9's perf layer is not enabled, with the
    reason already written down one directory up. Reporting it as a dangling
    endpoint would have been the checker demanding the repo delete a true
    statement.

    Fail-soft in the quiet direction (no file -> no declarations), because that
    is the state of every repo that has never needed one."""
    try:
        text = (root / "docs" / "declared-absences").read_text(encoding="utf-8")
    except (OSError, ValueError, UnicodeDecodeError):
        return frozenset()
    out = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # `<path> — <reason>`, the em-dash separator the file's own header
        # declares; a line with no separator is a path with no reason and is
        # deliberately NOT honoured (the file requires the reason).
        path, sep, _reason = line.partition("—")
        if sep:
            out.add(path.strip())
    return frozenset(out)


def _resolves_in_tree(root, endpoint):
    """True when an IF endpoint names something that exists under `root`.

    Tries the endpoint verbatim and under the kit's own script home, then with
    each source suffix appended — `scripts/trace` is how the registry spells
    `project-trajectory/scripts/trace.py`, and a classifier that could not see
    that would report every module endpoint as missing."""
    if not endpoint or root is None:
        return False
    bases = (endpoint, "project-trajectory/" + endpoint)
    for base in bases:
        for suffix in ("", ".py", ".md", ".toml", ".csv", ".ini", ".html", ".yml"):
            try:
                if (root / (base + suffix)).exists():
                    return True
            except (OSError, ValueError):  # pragma: no cover - exotic path text
                return False
    return False


def phase_ratified_findings(real):
    """The ratified-phase NUMERIC-ONLY rule (process.md §4 "Phased delivery"; owner
    ruling 2026-08-01, WI-402): once the project phases ANY spine row (digit-parse
    arming — a legacy `v2` cell arms it too), every RATIFIED (non-`Drafted`) SR/LLR/TC
    must carry a `Phase` that is a BARE INTEGER — digits only, full cell. Numeric-
    only because two joins match the cell LITERALLY, not by parse: the `--phase` /
    `--ratify` scope filters (`in_phase` / `_scope_srs`) and check_trajectory's
    phase-drop join of docs/gate's `per-phase=` labels against `[phase]-[g<N>]` WI
    anchors — a prefixed cell like `P1`/`v2` goes silently vacuous there, a
    disarmed warn no one is told about, which is worse than a crash. The digit-
    extract parsers (phase_num + its F5 copies) stay lenient on purpose —
    grandfathering, so historical labels still parse in the filters and the
    derived max while this rule migrates the live cells. The rule is **vacuous
    until >=1 artifact is phased** — the arming idiom the component checks use —
    so a fully-blank downstream registry stays green (a `Drafted` row may always
    leave `Phase` blank). SN is covered transitively: at DevBar-Reqs+ every ratified SN
    has >=1 SR (the orphan rule) and SRs are phased; pre-DevBar-Reqs it is vacuously
    exempt. Part of --strict-schema; extends the schema tier rather than forking
    it."""
    all_rows = [r for label in real for r in real[label]]
    if not any(phase_num(r) is not None for r in all_rows):
        return []  # unarmed: nothing is phased yet
    out = []
    for label in ("SR", "LLR", "TC"):
        key = id_key(label)
        for r in real.get(label, []):
            cell = (r.get("Phase") or "").strip()
            if is_drafted(r) or re.fullmatch(r"[0-9]+", cell):
                continue
            shown = f"={cell!r}" if cell else " (blank)"
            out.append(
                f"{label} {r[key]} is ratified but its Phase{shown} is not a bare "
                "integer — a ratified row's phase is digits only, full cell; a "
                "prefixed label silently misses the literal --phase/--ratify and "
                "phase-drop joins (process.md §4 'Phased delivery')"
            )
    return out


# --- Generated traceability views --------------------------------------------
# The registries are the reviewed source of truth; everything below is a
# *rendering* of the same join, regenerated every run (process.md §3
# "Reviewability"). Three views because none is both line-reviewable and
# big-graph-scalable: the text outline reviews line-by-line and scales to any
# size; the Mermaid DAG is small and diff-friendly; the HTML tree browses the
# full graph at any size. All are stdlib string-building — no dependency.


def _cell(row, col):
    return (row.get(col) or "").strip()


def _node_class(rid, status, orphan_ids):
    """A node's view class: orphan (a trace finding) outranks drafted (a status).
    The returned token is a CSS/mermaid CLASS NAME, not a Status value — it stays
    `draft` across D-9's rename because the stylesheet and the mermaid classDef
    key off it, while the cell it reads is now `Drafted`."""
    if rid in orphan_ids:
        return "orphan"
    if status.lower() == "drafted":
        return "draft"
    return ""


def _node(rid, status, title, orphan_ids, children=None):
    return {
        "id": rid,
        "status": status,
        "title": title,
        "cls": _node_class(rid, status, orphan_ids),
        "children": children or [],
    }


def _group(label, children):
    """A synthetic, unflagged parent for rows with no valid parent, so both tree
    views surface the same orphan tails the Orphans section lists."""
    return {"id": label, "status": "", "title": "", "cls": "", "children": children}


def _bucket_by_ref(rows, ref_col):
    """Index rows by each id named in their `ref_col` cell — parent-id -> [rows
    that reference it], child rows kept in input order, each cell parsed once.
    Replaces the per-parent refs() rescans that made the report joins quadratic
    (WI-081, M8: O(SR×LLR + SR×TC + LLR×TC) -> O(N))."""
    index = {}
    for row in rows:
        for parent in refs(row.get(ref_col)):
            index.setdefault(parent, []).append(row)
    return index


def build_forest(sn_ids, srs, llrs, tcs, orphan_ids, sn_draft=frozenset()):
    """The SN -> SR -> LLR -> TC chain as nested nodes, plus synthetic groups for
    rows with no valid parent. Shared by the text outline and the HTML tree.
    `sn_draft` (section-as-state, §4a) labels those SNs `Drafted` so the views
    flag them like a `Status=Drafted` SR/LLR/TC row."""
    llrs_by_sr = _bucket_by_ref(llrs, "SR-Refs")
    tcs_by_ref = _bucket_by_ref(tcs, "Verifies")
    srs_by_sn = _bucket_by_ref(srs, "SN-Refs")
    tc_verifies = {t["TC-ID"]: set(refs(t.get("Verifies"))) for t in tcs}

    def tc_node(t):
        return _node(t["TC-ID"], _cell(t, "Status"), _cell(t, "Method"), orphan_ids)

    def llr_node(lr):
        lid = lr["LLR-ID"]
        kids = [tc_node(t) for t in tcs_by_ref.get(lid, [])]
        return _node(lid, _cell(lr, "Status"), _cell(lr, "Title"), orphan_ids, kids)

    def sr_node(s):
        sid = s["SR-ID"]
        own = llrs_by_sr.get(sid, [])
        own_llrs = {lr["LLR-ID"] for lr in own}
        kids = [llr_node(lr) for lr in own]
        # TCs verifying the SR directly but none of its LLRs (so a TC that already
        # appears under an LLR of this SR is not also repeated under the SR).
        for t in tcs_by_ref.get(sid, []):
            if not tc_verifies[t["TC-ID"]] & own_llrs:
                kids.append(tc_node(t))
        return _node(sid, _cell(s, "Status"), _cell(s, "Title"), orphan_ids, kids)

    sr_ids = {s["SR-ID"] for s in srs}
    llr_ids = {lr["LLR-ID"] for lr in llrs}
    roots = []
    for sn in sorted(sn_ids):
        kids = [sr_node(s) for s in srs_by_sn.get(sn, [])]
        roots.append(
            _node(sn, "Drafted" if sn in sn_draft else "", "", orphan_ids, kids)
        )
    rootless_srs = [s for s in srs if not sn_ids & set(refs(s.get("SN-Refs")))]
    if rootless_srs:
        label = (
            "(SRs with no linked stakeholder need)"
            if sn_ids
            else "(system requirements)"
        )
        roots.append(_group(label, [sr_node(s) for s in rootless_srs]))
    rootless_llrs = [lr for lr in llrs if not sr_ids & set(refs(lr.get("SR-Refs")))]
    if rootless_llrs:
        roots.append(
            _group("(LLRs with no SR parent)", [llr_node(lr) for lr in rootless_llrs])
        )
    valid = sr_ids | llr_ids
    rootless_tcs = [t for t in tcs if not valid & set(refs(t.get("Verifies")))]
    if rootless_tcs:
        roots.append(
            _group("(TCs verifying nothing valid)", [tc_node(t) for t in rootless_tcs])
        )
    return roots


def _flag_suffix(node):
    """The inline ` [Status] [orphan] — Title` tail shared by both tree views."""
    bits = []
    if node["status"]:
        bits.append("[{}]".format(node["status"]))
    if node["cls"] == "orphan":
        bits.append("[orphan]")
    suffix = (" " + " ".join(bits)) if bits else ""
    if node["title"]:
        suffix += " — " + node["title"]
    return suffix


def outline_lines(roots):
    """Indented Markdown list of the forest — pure text, so it reviews line-by-
    line and scales to any project size."""
    out = []

    def walk(node, depth):
        out.append("{}- {}{}".format("  " * depth, node["id"], _flag_suffix(node)))
        for child in node["children"]:
            walk(child, depth + 1)

    for r in roots:
        walk(r, 0)
    return out or ["_(no requirements yet)_"]


# --- ratification hierarchy view (WI-146) --------------------------------------
# A batch-scoped SN->SR->LLR->TC tree that, unlike the whole-spine outline above,
# carries the *prose* a ratifier needs (SR Requirement/AC, LLR Detail, TC
# Method/Expected, and any rubric it cites) so a DevBar-Reqs/DevBar-Tests ratification brief can
# *link* the generated view instead of hand-copying registry rows. Generated, so
# it never drifts from the CSVs — review the CSVs, not this render (process.md §3).

RUBRIC_RE = re.compile(r"[\w./-]*rubrics/[\w./-]+\.md")


def _rubrics_cited(*cells):
    """Sorted unique `docs/rubrics/*.md` paths named anywhere in the given SR
    prose cells — the ratify view names the rubric a Critique/Attest SR is judged
    against (there is no dedicated Rubric column; the path lives in the prose)."""
    found = set()
    for c in cells:
        found.update(RUBRIC_RE.findall(c or ""))
    return sorted(found)


# The `--ratify` scopes that are NOT a phase tag or an id list — a CLOSED set,
# routed to the re-attestation brief instead of the hierarchy view. Held as a set
# rather than as a literal comparison so the rename at migration step 5
# (`modified` -> `drifted`) is one edit here plus `check.py`'s `ratify-fresh`
# step in the same commit, and so a scope that is neither reserved nor
# resolvable cannot fall through to an empty brief.
_RESERVED_RATIFY_SCOPES = frozenset({"modified"})


def _scope_srs(scope, srs):
    """Resolve a `--ratify` scope to an ordered SR-row list. The scope is either a
    comma/space list of `SR-###` ids (used verbatim) or one-or-more phase tags
    (every SR whose `Phase` cell is one of them). Detection: if *any* token looks
    like an SR id the whole scope is treated as ids, else as phases.

    RAISES on a scope that resolves to NOTHING (migration plan §F2). Until now
    an unmatched scope fell through to an empty brief at exit 0 — a typo, a
    retired phase tag, or a reserved word this function does not know produced a
    document that reads "there is nothing to ratify", which is the most
    expensive way for this tool to be wrong: an owner reads a short brief and
    blesses a batch they were never shown. An empty resolution is a REFUSAL, not
    an output."""
    tokens = refs(scope)
    as_ids = any(re.fullmatch(r"SR-\d+", t, re.IGNORECASE) for t in tokens)
    if as_ids:
        want = {t.upper() for t in tokens}
        matched = [s for s in srs if s.get("SR-ID", "").upper() in want]
    else:
        phases = {t.lower() for t in tokens}
        matched = [s for s in srs if _cell(s, "Phase").lower() in phases]
    if not matched:
        raise SystemExit(
            "trace: --ratify {!r} matches no SR — refusing to emit an empty "
            "brief. A scope is an SR-id list, a phase tag, or one of the "
            "reserved scopes ({}); an empty brief reads as 'nothing to ratify' "
            "to the human about to sign it.".format(
                scope, ", ".join(sorted(_RESERVED_RATIFY_SCOPES))
            )
        )
    return matched


_SN_EMPHASIS = re.compile(r"\*\*|`")


def _sn_prose(sn_text):
    """Parse each SN row's prose (Need / Why it matters / Acceptance intent) from
    stakeholder-needs.md so the ratify view renders the *top* of the chain, not a
    bare SN id (WI-146 REVIEW-A). Reads `spine_carrier`, the ONE home the fold
    now has — it was the third copy of a rule three modules
    promised in a docstring to change together, and did not. Takes TEXT rather
    than a path because the ratify view already holds the registry's contents;
    example `-000` rows are skipped."""
    needs = spine_carrier.needs_from_text(sn_text)
    return {
        row["id"]: {k: v for k, v in row.items() if k != "id"}
        for row in (
            {
                k: _SN_EMPHASIS.sub("", v).strip()
                for k, v in spine_carrier.folded(n).items()
            }
            for n in needs
            if not is_example(n.get("id", ""))
        )
    }


# --- the re-attestation brief (--ratify modified, WI-316) ----------------------
# A sitting cannot bless a delta it cannot see: for each SR owing a human act the
# brief shows every chain row's changed cells as BEFORE (the row in the
# `docs/archive/last_approved/` snapshot) vs AFTER (the working tree).
#
# THE BASELINE STOPPED BEING GIT ARCHAEOLOGY AT D-9 STEP 4 (owner directive
# 2026-08-15). It used to be the newest commit at which the SR row read
# `Verified` (now `Approved`), which is correct only while every amendment flips its row in the
# same commit — and D-9 deletes the flip, so that walk returns HEAD and the diff
# is empty by construction. The snapshot is a baseline OUTSIDE the live file,
# which is what the walk could never be.
#
# `_rows_at` and `_toml_rows_text` — the carrier-aware history readers that
# survived step 4 with no caller — ARE GONE (2026-08-15, log 2026-08-15h). The
# previous revision named them DEAD rather than describing them as reserved,
# which is the mistake the retired `current_digests` docstring made ("do not
# delete them for being unreferenced"), and this is that note being honoured:
# the only readers left were their own three tests. Nothing is lost by the
# deletion — `check_trajectory._spine_rows_at` is the surviving carrier-aware
# `git show` reader, still exercised by the cutover suite, so the D-5 hazard
# those tests guarded (a baseline read that knows only the live carrier reports
# every pre-migration revision as an EMPTY baseline, and the owner re-blesses
# full text with no diff) is still covered where the reader actually lives.

SPINE_FILES = (
    ("docs/requirements/system-requirements.toml", "SR-ID"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID"),
    ("docs/test/test-cases.toml", "TC-ID"),
)

# --- the spine carrier (repo-lock D-5/D-6) -----------------------------------
# The vocabulary and both readers live in `spine_carrier.py`, imported as a
# sibling. The full argument for that home — and why it AMENDS the F5 ruling
# rather than ignoring it (owner ruling 2026-08-10) — is in that module's
# docstring; the short version is that a duplicated VOCABULARY fails
# silently, by returning a row with a cell missing, which every consumer reads
# as "the cell is empty".
SPINE_TABLE = spine_carrier.SPINE_TABLE
SPINE_COLUMN = spine_carrier.SPINE_COLUMN
_spine_stem = spine_carrier.stem


def _git_out(root, args):
    """stdout of a git command under `root`, or None on ANY failure (no git
    binary, not a repo, unknown rev/path) — the best-effort-off-git pattern."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _full_row_bullets(row):
    """The `- **Cell**: value` bullets for a WHOLE registry row, non-empty cells
    only — how the re-attestation brief renders a row it has no baseline to diff
    against. Both arms that need it (no attested baseline, and a row ADDED since
    the baseline) rendered it identically in place (WI-347); same file, so the
    cross-script F5 sanction never covered the copy."""
    return [
        "- **{}**: {}".format(k, v.strip())
        for k, v in row["full"].items()
        if (v or "").strip()
    ]


def _cell_diff_lines(changed, ratified=frozenset()):
    """The per-cell before/after bullets, split into the §A5.1 two groups.

    The split is a capability the snapshot comparison hands the reader for free
    (D-9 step 4): a RATIFIED cell that moved owes an attestation, a TRACED one
    routes to adjudication and arms no window. Rendering them in one
    undifferentiated list asked the owner to make that judgement per cell, from
    memory, mid-sitting. Headings appear only when BOTH groups are present —
    a lone heading over the only group is noise."""
    groups = [
        ("ratified — re-attestation owed", [c for c in changed if c[0] in ratified]),
        (
            "traced — routes to adjudication",
            [c for c in changed if c[0] not in ratified],
        ),
    ]
    show_headings = all(rows for _label, rows in groups)
    lines = []
    for label, rows in groups:
        if not rows:
            continue
        if show_headings:
            lines.append("_{}_".format(label))
        for cell, b, a in rows:
            lines.append("- **{}**".format(cell))
            lines.append("  - before: {}".format(b or "(empty)"))
            lines.append("  - after: {}".format(a or "(empty)"))
    return lines


def _entry_kind(state):
    """What the model's entry OWES, from the SR's Status: a first approval, or a
    re-attestation of text that moved after it was blessed.

    BACK TO TWO ARMS AT D-9 STEP 5. The third (`plan`, for a `Planned` row whose
    text was ratified and whose evidence was never established) went out with the
    word: OI-30 D1 ruled `Planned` IS `Approved`, so there is no longer a state
    that means "blessed text, no evidence" — evidence is the harness's answer,
    not a cell's. A `Drafted` row owes a first approval and has no baseline to
    diff against; anything else in the model is here because its text moved after
    it was blessed, whether it says so (`Modified`) or the snapshot does
    (drift)."""
    if state == "drafted":
        return "ratify"
    return "reattest"


# "the caller passed nothing" vs "the caller passed None". `None` is a REAL
# argument here — it means "compare against no snapshot at all", which is the
# pre-signing state and a legitimate thing to ask for — so the default cannot
# also be None or a caller could never express the difference.
_UNSET = object()


def sr_chain_drifts(sid, chain, snapshot):
    """True when ANY row in this SR's chain has drifted from the snapshot.

    The attestation unit is the SR, so a drifted LLR or TC pulls its owning SR
    into the brief. This closes only the UNMARKED half of the WI-316 hole — a
    child amended while still claiming approval. The marked half stays open by
    construction: `is_drifted` fires only for a row whose live Status claims
    approval, so a `Modified` child never counts as drifted and its amendment
    rides no surface — which is exactly what the chain-consistency warn still
    shouts about."""
    return any(
        baseline_snapshot.is_drifted(
            rel, id_col, row, baseline_snapshot.rows_for(snapshot, rel, id_col)
        )
        for kind, _rid, row in chain
        for rel, id_col in (SPINE_FILES[_KIND_IX[kind]],)
    )


# `chain_of`'s row kinds -> their index in SPINE_FILES. Stated rather than
# derived from the id prefix: the prefix is data and this is a lookup into a
# constant, and a mis-derived index would compare an LLR against the SR
# registry's snapshot rows — which reads as "every cell changed".
_KIND_IX = {"SR": 0, "LLR": 1, "TC": 2}


def reattest_model(root, srs, llrs, tcs, snapshot=_UNSET):
    """The STRUCTURED attestation model: one entry per SR owing a human act,
    with its chain rows and each row's changed cells.

    Split out of `reattest_lines` (WI-322) so the computation runs ONCE and two
    renderers consume it — the markdown brief here, and the generated
    `open-items.html` owner view in `gen_open_items.py`.

    THE SELECTOR IS NO LONGER A LIST OF STATUS WORDS (D-9 step 4). It used to
    be `statuses=("modified",)` — the "hard coupling" the migration plan named,
    because a brief that selects a literal returns a clean bill forever once
    that literal is retired, at exit 0, with nothing to notice. A row now owes
    an act when it is `Drafted` (first approval) or `Modified` (the transitional
    marker, still honoured until step 7 retires it) — or when its chain has
    DRIFTED from
    `docs/archive/last_approved/`, which is a property of two files rather than
    of a word, and which no rename can silence.

    `snapshot` defaults to reading the live one. Pass an explicit `None` to
    compare against nothing (the vacuous state, which is also every
    pre-signing repo's): drift then answers False everywhere and the selector
    falls back to exactly the status arms, which is today's behaviour.

    Returns `[{id, title, kind, baseline, baseline_date, no_baseline_reason,
    rows:[{kind, id, state, cells, ratified, full}]}]` where `state` is
    `changed` | `added` | `removed` | `current`, `cells` is the
    `(name, before, after)` triples ORDERED ratified-first, `ratified` is the
    subset of those names §A5.1 rules ratified (so a renderer groups by one
    membership test rather than re-deriving the split), and `full` is the row
    dict for the states that render whole rows. Deterministic given the working
    tree and the snapshot."""
    if snapshot is _UNSET:
        snapshot = baseline_snapshot.load_all(root)

    llrs_by_sr = _bucket_by_ref(llrs, "SR-Refs")
    tcs_by_ref = _bucket_by_ref(tcs, "Verifies")

    def chain_of(sr_id, chain_srs, chain_llrs_by_sr, chain_tcs_by_ref):
        out = []
        sr_row = next((r for r in chain_srs if r.get("SR-ID") == sr_id), None)
        if sr_row is not None:
            out.append(("SR", sr_id, sr_row))
        child_llrs = sorted(
            chain_llrs_by_sr.get(sr_id, []), key=lambda r: r.get("LLR-ID", "")
        )
        seen_tcs = {}
        for lr in child_llrs:
            out.append(("LLR", lr["LLR-ID"], lr))
        for key in [sr_id] + [lr["LLR-ID"] for lr in child_llrs]:
            for t in chain_tcs_by_ref.get(key, []):
                seen_tcs.setdefault(t.get("TC-ID"), t)
        for tid in sorted(k for k in seen_tcs if k):
            out.append(("TC", tid, seen_tcs[tid]))
        return out

    def owes(sr):
        if is_drafted(sr) or is_modified(sr):
            return True
        return sr_chain_drifts(
            sr.get("SR-ID", ""),
            chain_of(sr.get("SR-ID", ""), srs, llrs_by_sr, tcs_by_ref),
            snapshot,
        )

    pending_srs = sorted((r for r in srs if owes(r)), key=lambda r: r.get("SR-ID", ""))
    if not pending_srs:
        return []
    stamp_rev, stamp_date = baseline_snapshot.stamp(root) if snapshot else ("", "")

    snap_rows = {
        kind: baseline_snapshot.rows_for(snapshot, *SPINE_FILES[ix])
        for kind, ix in _KIND_IX.items()
    }
    base_srs = list(snap_rows["SR"].values())
    base_llrs_by_sr = _bucket_by_ref(list(snap_rows["LLR"].values()), "SR-Refs")
    base_tcs_by_ref = _bucket_by_ref(list(snap_rows["TC"].values()), "Verifies")

    model = []
    for sr in pending_srs:
        sid = sr.get("SR-ID", "")
        entry = {
            "id": sid,
            "title": (sr.get("Title") or "").strip(),
            "kind": _entry_kind((sr.get("Status") or "").strip().lower()),
            "baseline": "",
            "baseline_date": stamp_date,
            "no_baseline_reason": "",
            "rows": [],
        }
        current_chain = chain_of(sid, srs, llrs_by_sr, tcs_by_ref)
        # A row ABSENT from the snapshot has no baseline to diff against — and
        # under the snapshot that is a statement about a FILE, checkable by
        # opening it, rather than the old "the row was never approved in
        # committed history", which was a claim about a git walk.
        if snapshot is None or sid not in snap_rows["SR"]:
            entry["no_baseline_reason"] = (
                "no {} snapshot exists yet — this repo has approved nothing, so "
                "every row awaits a first approval".format(
                    baseline_snapshot.SNAPSHOT_DIR
                )
                if snapshot is None
                else "absent from the {} snapshot — awaiting its first approval".format(
                    baseline_snapshot.SNAPSHOT_DIR
                )
            )
            entry["rows"] = [
                {
                    "kind": k,
                    "id": i,
                    "state": "current",
                    "cells": [],
                    "ratified": frozenset(),
                    "full": r,
                }
                for k, i, r in current_chain
            ]
            model.append(entry)
            continue
        entry["baseline"] = stamp_rev
        base_chain = chain_of(sid, base_srs, base_llrs_by_sr, base_tcs_by_ref)
        base_by_id = {(k, i): r for k, i, r in base_chain}
        cur_by_id = {(k, i): r for k, i, r in current_chain}
        for kind, rid, row in current_chain:
            before = base_by_id.get((kind, rid))
            if before is None:
                entry["rows"].append(
                    {
                        "kind": kind,
                        "id": rid,
                        "state": "added",
                        "cells": [],
                        "ratified": frozenset(),
                        "full": row,
                    }
                )
                continue
            rel, id_col = SPINE_FILES[_KIND_IX[kind]]
            split = check_trajectory.split_changed_cells(rel, id_col, before, row)
            # RATIFIED FIRST, then traced — the reader's question is "what do I
            # have to re-bless?", and the §A5.1 split answers it: a ratified
            # cell owes attestation, a traced one routes to adjudication and
            # arms no window (the WI-388 ruling).
            cells = [
                (name, split[half][name][0], split[half][name][1])
                for half in ("ratified", "traced")
                for name in sorted(split[half])
            ]
            if cells:
                entry["rows"].append(
                    {
                        "kind": kind,
                        "id": rid,
                        "state": "changed",
                        "cells": cells,
                        "ratified": frozenset(split["ratified"]),
                        "full": row,
                    }
                )
        for kind, rid, row in base_chain:
            if (kind, rid) not in cur_by_id:
                entry["rows"].append(
                    {
                        "kind": kind,
                        "id": rid,
                        "state": "removed",
                        "cells": [],
                        "ratified": frozenset(),
                        "full": row,
                    }
                )
        model.append(entry)
    return model


def newest_ratify_brief(root):
    """The live re-attestation brief — the newest `docs/ratify/*.md` — or None.

    DERIVED rather than configured: briefs are date-stamped per sitting, so a
    fixed path in `docs/stack.ini` would have to be edited at every sitting and
    would silently gate the wrong file when it was not. Newest by NAME, which is
    the stamped date, not by mtime — a checkout re-writes mtimes and the whole
    point of this check is not to trust the working tree's incidentals."""
    ratify = root / "docs" / "ratify"
    if not ratify.is_dir():
        return None
    briefs = sorted(p for p in ratify.glob("*.md") if p.name.lower() != "readme.md")
    return briefs[-1] if briefs else None


# --- WI-325: the re-attestation brief gets the freshness gate everything else has
# Every other generated surface here is freshness-gated (`gen_trajectory --check`,
# the status snapshot, `gen_okf --check`, `gen_open_items --check`); the brief was
# generated the same way and gated by nothing, so it silently drifted behind the
# registry it summarizes. Observed twice in one day: at 121-CRITIQUE it was
# missing LLR-105/TC-108 and SR-054's later amendment (an owner would have blessed
# six rows having seen four), and again at 123-CRITIQUE it was three chain rows
# short. Both were caught by a human noticing — the weakest enforcement tier
# `docs/enforcement-audit.md` names.
#
# THE CONSTRAINT THAT MADE THIS HARDER THAN ITS SIBLINGS IS GONE (D-9 step 4).
# The brief used to SELF-STAMP a git-derived baseline, so `--check` had to
# compare against the baseline the FILE declared and must not re-derive one —
# because re-deriving was the WI-322 review BLOCKER, a regeneration that
# silently collapsed 43 chain-row diffs to 18 while `--check` certified the
# loss. `_DECLARED_BASELINE_RE` and `declared_since` existed only to read that
# self-stamp back.
#
# Under the snapshot there is nothing to re-derive: the baseline is a directory
# of files that a regeneration cannot move. So this is now the plain
# regenerate-and-compare its siblings always were, and the WI-325 blocker
# dissolves rather than being guarded against.


def ratify_check(root, srs, llrs, tcs, out_path):
    """`(code, message)` for `--ratify modified --check` — a plain
    regenerate-and-compare, like every other freshness gate in the kit.

    Fails CLOSED on a difference — a stale brief is read by a human about to
    attest, and the cost of a false green here is an owner blessing rows they
    were never shown.

    Two silences, both the arming idiom the component checks use rather than
    exceptions carved for this repo:

      - **no file at `--out`** — a project with no `docs/ratify/` pays nothing;
      - **no row owes an act** — the window is CLOSED, so the committed brief is
        a historical record of a finished sitting rather than a surface that can
        go stale. Checking it against a registry whose rows have since been
        blessed would fail forever, which is how a check earns its own ignore.

    THE `--since` / `declared_since` MACHINERY IS GONE (D-9 step 4). It existed
    because the brief self-stamped a git-derived baseline that a re-derivation
    could move, so `--check` had to read the file's own declaration back rather
    than compute one. The snapshot is a directory of files; regenerating cannot
    move it, so the comparison is honest without the self-stamp — and the WI-325
    "a gate that re-derives its own expectation" blocker dissolves."""
    if not out_path.exists():
        return 0, "no brief at {} — nothing to gate".format(out_path)
    model = reattest_model(root, srs, llrs, tcs)
    if not model:
        return 0, "no row owes a ratification or a re-attest — the window is closed"
    try:
        with out_path.open("r", encoding="utf-8", newline="") as fh:
            existing = fh.read()
    except OSError as exc:
        return 1, "cannot read {}: {}".format(out_path, exc)
    rendered = "\n".join(reattest_lines(root, srs, llrs, tcs)) + "\n"
    if rendered == existing:
        return 0, "{} is current".format(out_path)
    return 1, (
        "{} is STALE against the registry and the {} snapshot. Regenerate it "
        "with `trace.py --ratify modified --out {}` and re-read it BEFORE "
        "attesting — an owner blessing a short brief blesses rows they were "
        "never shown.".format(out_path, baseline_snapshot.SNAPSHOT_DIR, out_path)
    )


def reattest_lines(root, srs, llrs, tcs):
    """Markdown for the re-attestation brief (`--ratify modified`, WI-316): one
    section per SR owing a human act — the attestation unit — with per-cell
    before/after for every chain row (the SR + its LLRs + their/its TCs) that
    differs from the `docs/archive/last_approved/` snapshot, plus rows ADDED to
    or REMOVED from the chain.

    THE BASELINE IS A DIRECTORY, NOT A REVISION (D-9 step 4). It used to be the
    newest commit at which the SR row still read `Verified` (now `Approved`), with `--since` as
    the escape hatch for a streak that walk could not see. Both are gone: the
    walk dies by construction once an approved row stops flipping on amendment,
    and a snapshot cannot sit after the amendment it is supposed to precede.

    Each changed row renders its RATIFIED cells first and its TRACED cells
    after, under their own heading — the capability the split buys a reader:
    ratified cells owe an attestation, traced cells route to adjudication and
    arm no window (§A5.1, the WI-388 ruling).

    Deterministic given the working tree and the snapshot; a generator mode like
    `ratify_lines` — runs no checks. The markdown RENDERER over `reattest_model`
    (WI-322): the model owns the comparison, this owns the prose."""
    model = reattest_model(root, srs, llrs, tcs)
    stamp_rev, stamp_date = baseline_snapshot.stamp(root)
    lines = [
        "# Re-attestation brief — spine rows owing a human act",
        "",
        "_Generated by `trace.py --ratify modified` (WI-316). One section per SR"
        " (the attestation unit) that is `Drafted` or `Modified`, or whose"
        " chain has DRIFTED from the approved snapshot; each chain row"
        " shows only its CHANGED cells, before (the snapshot) vs after (the"
        " working tree), ratified cells first. `Status` itself is never listed —"
        " the marker is not the amendment. Rule on each section: bless → set"
        " `Status` to `Approved` (process.md §7) — and from the first signing"
        " onward, run `intake.py snapshot` in the SAME commit, or the record of"
        " what was blessed does not move._",
        "",
        "_Baseline: `{}` — {}._".format(
            baseline_snapshot.SNAPSHOT_DIR,
            "copied {} ({}), the reviewed commit that last moved an approval".format(
                stamp_date, stamp_rev
            )
            if stamp_rev
            else "no snapshot exists yet, so every row below awaits a FIRST "
            "approval and renders its current text in full",
        ),
        "",
    ]
    if not model:
        lines.append(
            "_No spine row differs from its `{}` copy, and no row awaits a first"
            " approval._".format(baseline_snapshot.SNAPSHOT_DIR)
        )
        return lines
    for entry in model:
        sid, title = entry["id"], entry["title"]
        lines += ["", "## {} — {}".format(sid, title or "(untitled)"), ""]
        if entry["no_baseline_reason"]:
            lines.append(
                "_No approved baseline — {}; current state only._".format(
                    entry["no_baseline_reason"]
                )
            )
            for row in entry["rows"]:
                lines += ["", "### {} {} (current)".format(row["kind"], row["id"])]
                lines += _full_row_bullets(row)
            continue
        for row in entry["rows"]:
            if row["state"] == "added":
                lines += [
                    "",
                    "### {} {} — ADDED since the snapshot".format(
                        row["kind"], row["id"]
                    ),
                ]
                lines += _full_row_bullets(row)
            elif row["state"] == "changed":
                lines += ["", "### {} {}".format(row["kind"], row["id"])]
                lines += _cell_diff_lines(row["cells"], row["ratified"])
            elif row["state"] == "removed":
                lines += [
                    "",
                    "### {} {} — REMOVED since the snapshot".format(
                        row["kind"], row["id"]
                    ),
                    "_In this SR's chain in the snapshot, out of it in the working"
                    " tree — the row was deleted, re-parented, or superseded"
                    " (a superseded row keeps existing; it leaves the chain)._",
                ]
        if not entry["rows"]:
            lines.append(
                "_No cell differs from the approved snapshot. The row is here"
                " because its own `Status` asks for a human, not because its"
                " text moved._"
            )
    return lines


def ratify_lines(scope, sn_ids, srs, llrs, tcs, sn_meta=None):
    """Markdown for the batch-scoped ratification hierarchy (WI-146a). Groups the
    in-scope SRs under their primary (first-listed) stakeholder need — rendering
    that need's own prose (Need/Why/Acceptance from `sn_meta`, WI-146 REVIEW-A) —
    then nests each SR's LLRs and TCs with their prose. Deterministic, stdlib-only."""
    sn_meta = sn_meta or {}
    in_scope = _scope_srs(scope, srs)
    # Bucketed joins (WI-081's _bucket_by_ref), not per-parent refs() rescans —
    # a phase-scoped ratify over a large registry was the one path still doing
    # the quadratic O(SR×LLR + LLR×TC) scans the report path already dropped.
    llrs_by_sr = _bucket_by_ref(llrs, "SR-Refs")
    tcs_by_ref = _bucket_by_ref(tcs, "Verifies")

    def tc_block(t):
        auto = " · Automated" if _cell(t, "Automated").lower() in ("yes", "y") else ""
        out = ["##### {} [{}]{}".format(t["TC-ID"], _cell(t, "Status") or "?", auto)]
        if _cell(t, "Method"):
            out.append("**Method.** {}".format(_cell(t, "Method")))
        if _cell(t, "Expected"):
            out.append("**Expected.** {}".format(_cell(t, "Expected")))
        return out

    def llr_block(lr):
        out = [
            "#### {} — {} [{}]".format(
                lr["LLR-ID"],
                _cell(lr, "Title") or "(untitled)",
                _cell(lr, "Status") or "?",
            )
        ]
        meta = []
        if _cell(lr, "Module"):
            meta.append("Module: {}".format(_cell(lr, "Module")))
        if _cell(lr, "Component"):
            meta.append("Component: {}".format(_cell(lr, "Component")))
        if meta:
            out.append("_({})_".format(" · ".join(meta)))
        if _cell(lr, "Detail"):
            out.append(_cell(lr, "Detail"))
        for t in tcs_by_ref.get(lr["LLR-ID"], []):
            out += tc_block(t)
        return out

    def sr_block(s):
        sid = s["SR-ID"]
        out = [
            "### {} — {} [{}] [{}]".format(
                sid,
                _cell(s, "Title") or "(untitled)",
                _cell(s, "Status") or "?",
                _cell(s, "Verification") or "?",
            )
        ]
        if _cell(s, "Requirement"):
            out.append("**Requirement.** {}".format(_cell(s, "Requirement")))
        if _cell(s, "AcceptanceCriteria"):
            out.append(
                "**Acceptance criteria.** {}".format(_cell(s, "AcceptanceCriteria"))
            )
        rubrics = _rubrics_cited(
            _cell(s, "Requirement"),
            _cell(s, "AcceptanceCriteria"),
            _cell(s, "Rationale"),
        )
        if rubrics:
            out.append("**Rubrics.** {}".format("; ".join(rubrics)))
        own_llrs = llrs_by_sr.get(sid, [])
        own_ids = {lr["LLR-ID"] for lr in own_llrs}
        for lr in own_llrs:
            out += llr_block(lr)
        # TCs verifying the SR directly (not via one of its LLRs).
        for t in tcs_by_ref.get(sid, []):
            if not set(refs(t.get("Verifies"))) & own_ids:
                out += tc_block(t)
        if not own_llrs and not tcs_by_ref.get(sid):
            out.append("_(no LLR/TC yet)_")
        return out

    lines = [
        "# Ratification hierarchy — scope: {}".format(scope),
        "",
        "_Generated by `trace.py --ratify {}` from the registries — {} SR(s). "
        "Review the registry CSVs, not this render (process.md §3)._".format(
            scope, len(in_scope)
        ),
        "",
    ]
    if not in_scope:
        lines.append("_(no SR matched this scope)_")
        return lines
    # Group under the SR's primary (first) SN ref; SRs with no SN ref group last.
    by_sn = {}
    for s in sorted(in_scope, key=lambda r: id_sort_key(r["SR-ID"])):
        sn_refs = [x for x in refs(s.get("SN-Refs")) if x in sn_ids]
        key = sn_refs[0] if sn_refs else None
        by_sn.setdefault(key, []).append(s)
    ordered = sorted((k for k in by_sn if k), key=id_sort_key) + (
        [None] if None in by_sn else []
    )
    for sn in ordered:
        lines.append("## {}".format(sn if sn else "(no linked stakeholder need)"))
        prose = sn_meta.get(sn) if sn else None
        if prose:
            if prose.get("need"):
                lines.append("**Need.** {}".format(prose["need"]))
            if prose.get("why"):
                lines.append("**Why it matters.** {}".format(prose["why"]))
            if prose.get("acceptance"):
                lines.append("**Acceptance intent.** {}".format(prose["acceptance"]))
        for s in by_sn[sn]:
            extra = [x for x in refs(s.get("SN-Refs")) if x != sn]
            block = sr_block(s)
            if extra:
                block.insert(1, "_(also realizes {})_".format("; ".join(extra)))
            lines += block
    return lines


MERMAID_CLASSDEFS = [
    "    classDef orphan fill:#ffd6d6,stroke:#cc0000,color:#000;",
    "    classDef draft fill:#fff3cd,stroke:#cc9900,color:#000;",
]


def _mermaid_id(rid):
    # Mermaid node ids can't carry '-'/'.'-style separators — sanitize to '_'.
    return re.sub(r"\W", "_", rid)


def _mermaid_label(rid, title):
    if not title:
        return rid
    short = title if len(title) <= 40 else title[:39] + "…"
    return "{} — {}".format(rid, short).replace('"', "'")


def mermaid_graph(sn_ids, srs, llrs, tcs, orphan_ids, sn_draft=frozenset()):
    """A `graph LR` DAG of the chain (a TC verifies its SR *and* its LLR), colored
    by orphan/draft state via classDef. Kept small/diff-friendly on purpose — the
    HTML view is the one that scales. `sn_draft` colors unratified SNs (§4a)."""
    sr_ids = {s["SR-ID"] for s in srs}
    llr_ids = {lr["LLR-ID"] for lr in llrs}
    nodes = {}  # rid -> (label, cls); dict insertion order keeps output stable
    edges = set()

    def add(rid, label, cls):
        nodes[rid] = (label, cls)

    for sn in sorted(sn_ids):
        add(
            sn,
            sn,
            "orphan" if sn in orphan_ids else ("draft" if sn in sn_draft else ""),
        )
    for s in srs:
        sid = s["SR-ID"]
        add(sid, _mermaid_label(sid, _cell(s, "Title")),
            _node_class(sid, _cell(s, "Status"), orphan_ids))  # fmt: skip
        for u in refs(s.get("SN-Refs")):
            if u in sn_ids:
                edges.add((u, sid))
    for lr in llrs:
        lid = lr["LLR-ID"]
        add(lid, _mermaid_label(lid, _cell(lr, "Title")),
            _node_class(lid, _cell(lr, "Status"), orphan_ids))  # fmt: skip
        for p in refs(lr.get("SR-Refs")):
            if p in sr_ids:
                edges.add((p, lid))
    for t in tcs:
        tid = t["TC-ID"]
        add(tid, tid, _node_class(tid, _cell(t, "Status"), orphan_ids))
        for x in refs(t.get("Verifies")):
            if x in sr_ids or x in llr_ids:
                edges.add((x, tid))

    lines = ["```mermaid", "graph LR"] + MERMAID_CLASSDEFS
    if not nodes:
        lines.append("    empty[No requirements yet]")
    for rid, (label, _cls) in nodes.items():
        lines.append('    {}["{}"]'.format(_mermaid_id(rid), label))
    for a, b in sorted(edges):
        lines.append("    {} --> {}".format(_mermaid_id(a), _mermaid_id(b)))
    for rid, (_label, cls) in nodes.items():
        if cls:
            lines.append("    class {} {};".format(_mermaid_id(rid), cls))
    lines.append("```")
    return lines


def _esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Traceability map</title>
<style>
  body { font: 14px/1.5 system-ui, sans-serif; margin: 2rem; color: #222; }
  h1 { font-size: 1.3rem; }
  details { margin: 0.15rem 0 0.15rem 1.1rem; }
  summary { cursor: pointer; }
  .leaf { margin: 0.15rem 0 0.15rem 1.1rem; }
  .orphan { color: #b00020; font-weight: 600; }
  .draft { color: #8a6d00; }
  .note { color: #666; }
</style>
</head>
<body>
<h1>Traceability map</h1>
<p class="note">Generated by <code>scripts/trace.py --html</code>. Do not edit by
hand; review the registry CSVs, not this render (process.md §3 "Reviewability").</p>
"""

HTML_TAIL = "</body>\n</html>\n"


def html_document(roots):
    """A dependency-free, collapsible <details> tree of the full graph — inline
    CSS, zero JS, self-contained — for browse/onboard/audit at any size."""

    def walk(node, depth):
        pad = "  " * depth
        label = _esc(node["id"]) + _esc(_flag_suffix(node))
        if node["children"]:
            cls = ' class="{}"'.format(node["cls"]) if node["cls"] else ""
            out = ["{}<details open><summary{}>{}</summary>".format(pad, cls, label)]
            for child in node["children"]:
                out += walk(child, depth + 1)
            out.append("{}</details>".format(pad))
            return out
        leaf_cls = ("leaf " + node["cls"]).strip()
        return ['{}<div class="{}">{}</div>'.format(pad, leaf_cls, label)]

    body = []
    for r in roots:
        body += walk(r, 0)
    if not body:
        body = ['<p class="note">No requirements yet.</p>']
    return HTML_HEAD + "\n".join(body) + "\n" + HTML_TAIL


def _repo_id(r):
    return r.get("REPO-ID") or r.get("MOD-ID")


class Registries:
    """Loaded spine + off-spine registries: raw rows (kept for the integrity/
    placeholder sweeps), example-filtered working sets for the join, and the SN
    ids/draft/prose scraped from stakeholder-needs.md. Produced by
    load_registries; consumed by --ratify, analyze, and the report render."""


class Findings:
    """The analyze() output — every finding list + derived set the report,
    console summary, and exit policy read. Produced by analyze()."""


def load_registries(docs):
    """Load the spine + off-spine registries under docs (loading only — no analysis)."""
    # The three spine tiers read through the CARRIER — as do the IF and CMP
    # tiers since WI-443 (OI-14 part B). `load_csv` stays for the off-spine
    # registries below that have not moved yet (PB/REPO/PART/ASSET).
    raw_srs = spine_carrier.load(
        docs / "requirements" / "system-requirements.toml", "SR-ID"
    )
    raw_llrs = spine_carrier.load(
        docs / "requirements" / "low-level-requirements.toml", "LLR-ID"
    )
    raw_tcs = spine_carrier.load(docs / "test" / "test-cases.toml", "TC-ID")
    # Optional, off-spine coordination registry (process.md §9); absent file -> [].
    raw_pbs = load_csv(docs / "requirements" / "performance-budgets.csv")
    # Optional coordinator repo-delegation registry (REPO-###, MULTI_REPO.md, the
    # multi-repo layer). Formerly MOD-### in modules.csv — a delegated *repo* was
    # never a component, so the id freed "module" for other uses; the legacy
    # file + ids are still read (never breaking). Absent files -> [].
    raw_repos = load_csv(docs / "requirements" / "repos.csv")
    raw_mods = load_csv(docs / "requirements" / "modules.csv")
    # Optional purchased/external parts registry (process-options.md); absent
    # file -> []. Integrity-checked only (IF-Ref points at the off-spine IF-###
    # tier, which trace.py does not read).
    raw_parts = load_csv(docs / "requirements" / "procurement.csv")
    # Optional binary/large-asset provenance registry (process-options.md "Binary
    # assets"); absent file -> []. Integrity-checked only (its Refs back-link the
    # SR/LLR the asset realizes, but like PART it is off the joined spine — the
    # asset's provenance/license/hash is what matters, tracked in text even when
    # the binary itself can't be diffed).
    raw_assets = load_csv(docs / "requirements" / "assets.csv")
    # Optional domain-neutral component registry (CMP-###, process-options.md
    # "Component layer"): the set-grained knowledge + lifecycle home. Structure
    # is derived — membership is a `Component` tag on the primitive rows
    # (LLR/IF/ASSET/PART), never restated on the CMP row; absent file -> [].
    raw_cmps = spine_carrier.load(docs / "requirements" / "components.toml", "CMP-ID")
    # Optional interface-definition registry (IF-###, process.md §8): one row per
    # interface, stating what it concretely IS. Off the joined spine like
    # PART/ASSET, but its Req-Refs back-link and its endpoint join keep it
    # traceable (WI-056 closed the LLR-002-era gap). Absent file -> [].
    raw_ifs = spine_carrier.load(docs / "requirements" / "interfaces.toml", "IF-ID")
    # Optional depth-0 FRAME registry (WI-442, sitting-2 §1R.5): three tiers in
    # one file — who is outside (EXT-###), what crosses the system boundary
    # (B-##), and the external-to-external flows the system is not a party to
    # (REL-###). One `load` per tier; the carrier keys by ID COLUMN, so the
    # shared path needs no new loader. It is NOT free, and saying so beats an
    # unbacked "costs nothing": `load` reads and parses the file twice per call
    # (once for the rows, once for the nested-table check), so three tiers is six
    # reads and six parses of one small file per run — negligible at this size,
    # and the number to revisit if the frame ever stops being small. Absent
    # file -> [] three times, and every rule below is then vacuous, which is the
    # applies-when a project that declares no boundary needs.
    raw_exts = spine_carrier.load(docs / "requirements" / "external.toml", "EXT-ID")
    raw_bifs = spine_carrier.load(docs / "requirements" / "external.toml", "B-ID")
    raw_rels = spine_carrier.load(docs / "requirements" / "external.toml", "REL-ID")

    # The working sets exclude template example rows (ids ending "-000") so a
    # fresh scaffold has nothing to orphan; the raw lists above keep them for the
    # placeholder and integrity checks below.
    srs = [r for r in raw_srs if r.get("SR-ID") and not is_example(r["SR-ID"])]
    llrs = [r for r in raw_llrs if r.get("LLR-ID") and not is_example(r["LLR-ID"])]
    tcs = [r for r in raw_tcs if r.get("TC-ID") and not is_example(r["TC-ID"])]
    pbs = [r for r in raw_pbs if r.get("PB-ID") and not is_example(r["PB-ID"])]

    mods = [
        r for r in raw_repos + raw_mods if _repo_id(r) and not is_example(_repo_id(r))
    ]
    parts = [r for r in raw_parts if r.get("PART-ID") and not is_example(r["PART-ID"])]
    assets = [
        r for r in raw_assets if r.get("ASSET-ID") and not is_example(r["ASSET-ID"])
    ]
    cmps = [r for r in raw_cmps if r.get("CMP-ID") and not is_example(r["CMP-ID"])]
    ifs = [r for r in raw_ifs if r.get("IF-ID") and not is_example(r["IF-ID"])]
    exts = [r for r in raw_exts if r.get("EXT-ID") and not is_example(r["EXT-ID"])]
    bifs = [r for r in raw_bifs if r.get("B-ID") and not is_example(r["B-ID"])]
    rels = [r for r in raw_rels if r.get("REL-ID") and not is_example(r["REL-ID"])]

    sn_ids = set()
    sn_draft = set()
    sn_meta = {}
    sn_integrity = []
    # Resolved through the CARRIER, not by literal suffix: a
    # `.toml`-only existence test reads a markdown needs registry as ABSENT, and
    # an absent needs tier makes every SR orphan-clean, every draft need
    # ratified, and the whole SN half of `--strict` vacuous.
    sn_md = spine_carrier.resolve(
        docs / "requirements" / "stakeholder-needs.toml", spine_carrier.NEED_CARRIERS
    )
    if sn_md is not None:
        # utf-8-sig + replace: a BOM must not glue to line 1 (defeating the
        # heading regexes) and one stray cp1252 byte must degrade, not crash
        # the gate chain (the C8 convention, applied to content reads too).
        sn_text = sn_md.read_text(encoding="utf-8-sig", errors="replace")
        sn_ids = sn_all_ids(sn_text)
        # Section-as-state maturity (derived-gate §4a): SNs under a "draft" heading
        # are unratified (DevBar-Below) and exempt from the "SN with no SR" child rule below.
        sn_draft = sn_draft_ids(sn_text)
        sn_meta = _sn_prose(sn_text)
        sn_integrity = sn_integrity_findings(sn_text)
    reg = Registries()
    reg.raw_srs, reg.raw_llrs, reg.raw_tcs = raw_srs, raw_llrs, raw_tcs
    reg.raw_pbs, reg.raw_repos, reg.raw_mods = raw_pbs, raw_repos, raw_mods
    reg.raw_parts, reg.raw_assets = raw_parts, raw_assets
    reg.raw_cmps, reg.raw_ifs = raw_cmps, raw_ifs
    reg.raw_exts, reg.raw_bifs, reg.raw_rels = raw_exts, raw_bifs, raw_rels
    reg.exts, reg.bifs, reg.rels = exts, bifs, rels
    reg.srs, reg.llrs, reg.tcs, reg.pbs = srs, llrs, tcs, pbs
    reg.mods, reg.parts, reg.assets = mods, parts, assets
    reg.cmps, reg.ifs = cmps, ifs
    reg.sn_ids, reg.sn_draft, reg.sn_meta, reg.sn_md = sn_ids, sn_draft, sn_meta, sn_md
    reg.sn_integrity = sn_integrity
    reg.docs = docs
    return reg


def analyze(reg, args):
    """The whole checker pass over loaded registries: orphan rules, off-spine
    back-link/membership checks, the --require-verified status criterion
    (phase-scoped), the integrity/placeholder/schema sweeps, and the always-on
    advisories. Pure — reads reg + args flags, returns a Findings bag. No I/O."""
    srs, llrs, tcs = reg.srs, reg.llrs, reg.tcs
    pbs, mods, parts = reg.pbs, reg.mods, reg.parts
    assets, cmps, ifs = reg.assets, reg.cmps, reg.ifs
    exts, bifs, rels = reg.exts, reg.bifs, reg.rels
    sn_ids, sn_draft, sn_md = reg.sn_ids, reg.sn_draft, reg.sn_md
    raw_srs, raw_llrs, raw_tcs = reg.raw_srs, reg.raw_llrs, reg.raw_tcs
    raw_pbs, raw_repos, raw_mods = reg.raw_pbs, reg.raw_repos, reg.raw_mods
    raw_parts, raw_assets = reg.raw_parts, reg.raw_assets
    raw_cmps, raw_ifs = reg.raw_cmps, reg.raw_ifs
    docs = reg.docs
    sr_ids = {r["SR-ID"] for r in srs}
    llr_ids = {r["LLR-ID"] for r in llrs}
    llr_sr_refs = {x for r in llrs for x in refs(r.get("SR-Refs"))}
    tc_refs = {x for r in tcs for x in refs(r.get("Verifies"))}
    sr_sn_refs = sn_cited_ids(srs)

    # orphan_ids collects the at-fault id for each finding, so the rendered views
    # below (outline/graph/HTML) can flag the same nodes the text list reports.
    orphans = []
    orphan_ids = set()
    for r in srs:
        sid = r["SR-ID"]
        # A Drafted SR is being drafted requirement-first (derived-gate model §3):
        # exempt from the child-completeness rules (no LLR / no TC) so it lives in
        # the live spine without orphaning. Its SN linkage and every integrity
        # rule still apply.
        draft = is_drafted(r)
        analytic = llr_exempt(r)
        if not draft and not analytic and sid not in llr_sr_refs:
            orphans.append(
                f"SR {sid} has no LLR (and Verification not in "
                "Analysis/Inspection/Attest)"
            )
            orphan_ids.add(sid)
        if not draft and sid not in tc_refs:
            orphans.append(f"SR {sid} has no test (TC)")
            orphan_ids.add(sid)
        sn_parents = refs(r.get("SN-Refs"))
        # DevBar-Reqs's "every SR links >=1 SN", machine-checked — but only when the SN
        # registry actually provides real ids (a project without a needs file,
        # or one holding only -000 placeholders, has no SN tier to link yet).
        if sn_ids and not sn_parents:
            orphans.append(f"SR {sid} links no SN (every SR needs >=1 SN-Ref)")
            orphan_ids.add(sid)
        for u in sn_parents:
            if sn_ids and u not in sn_ids:
                orphans.append(f"SR {sid} references unknown {u}")
                orphan_ids.add(sid)

    for r in llrs:
        lid = r["LLR-ID"]
        parents = refs(r.get("SR-Refs"))
        if not parents:
            orphans.append(f"LLR {lid} has no SR parent")
            orphan_ids.add(lid)
        for p in parents:
            if p not in sr_ids:
                orphans.append(f"LLR {lid} references unknown {p}")
                orphan_ids.add(lid)
        # A Drafted LLR is exempt from the child-completeness (no TC) rule, like a
        # Drafted SR — its SR parent + id integrity still apply (derived-gate §3).
        if not is_drafted(r) and lid not in tc_refs:
            orphans.append(f"LLR {lid} has no test (TC)")
            orphan_ids.add(lid)

    for tid, finding in tc_citation_findings(tcs, sr_ids | llr_ids, ifs):
        orphans.append(finding)
        orphan_ids.add(tid)

    for u in sorted(sn_ids):
        # A Drafted SN (section-as-state, §4a) is being drafted requirement-first and
        # is exempt from the child-completeness rule, like a Drafted SR. The gate
        # half of this rule is derive_gate's SN-coverage rung (WI-401): same
        # cited set (sn_cited_ids), same Drafted exemption — this lists the ids,
        # that caps the level, and neither fires twice on one fact.
        if u not in sr_sn_refs and u not in sn_draft:
            orphans.append(f"SN {u} has no SR")
            orphan_ids.add(u)

    # Performance budgets (process.md §9) sit off the spine but stay traceable:
    # each row's Refs must resolve to a real SR/LLR id or an LLR Module path.
    module_ids = {(lr.get("Module") or "").strip() for lr in llrs}
    module_ids.discard("")
    budget_targets = sr_ids | llr_ids | module_ids
    budget_findings = []
    for r in pbs:
        pid = r["PB-ID"]
        targets = refs(r.get("Refs"))
        if not targets:
            budget_findings.append(f"PB {pid} back-links nothing (Refs is empty)")
        for x in targets:
            if x not in budget_targets:
                budget_findings.append(f"PB {pid} references unknown {x}")

    # Coordinator module registry (MULTI_REPO.md, the multi-repo layer) sits off the
    # spine like PB, but its DelegatedSRs stay traceable *within* the coordinator
    # repo: each must name a real coordinator SR (delegation is at the SR tier,
    # §3.1). The cross-boundary link (a module SN's ParentRef back to this SR) points
    # into another repo, so no single trace.py run validates it — that reconciliation
    # is the deferred cross-repo join. An external/reused part referenced only via the
    # IF-### catalog may delegate nothing, so an empty back-link is allowed here.
    module_findings = []
    for r in mods:
        mid = _repo_id(r)
        for x in refs(r.get("DelegatedSRs")):
            if x not in sr_ids:
                module_findings.append(
                    f"{mid.split('-')[0]} {mid} delegates unknown {x}"
                )

    # Component registry (CMP-###, process-options.md "Component layer") sits off
    # the spine like PART/ASSET, but its two structural cells stay traceable:
    # PartOf (nesting — tag primitives at the finest CMP, coarser membership
    # derives) and SupersededBy (lifecycle identity across a rewrite) must name
    # real CMP ids. And the membership join is checked from the primitive side:
    # a `Component` tag on an LLR/IF/PART/ASSET row must resolve to a real CMP
    # row (the IF tier joined the sweep at WI-064 — trace.py has read
    # interfaces.csv since WI-056, so its tags were the one unvalidated cell).
    cmp_ids = {r["CMP-ID"] for r in cmps}
    component_findings = []
    for r in cmps:
        cid = r["CMP-ID"]
        for col in ("PartOf", "SupersededBy"):
            for x in refs(r.get(col)):
                if x not in cmp_ids:
                    component_findings.append(f"CMP {cid} {col} references unknown {x}")
    if cmp_ids:
        for label, rows_, key in (
            ("LLR", llrs, "LLR-ID"),
            ("IF", ifs, "IF-ID"),
            ("PART", parts, "PART-ID"),
            ("ASSET", assets, "ASSET-ID"),
        ):
            for r in rows_:
                for x in refs(r.get("Component")):
                    if x not in cmp_ids:
                        component_findings.append(
                            f"{label} {r[key]} Component tag references unknown {x}"
                        )

    # Knowledge-pack refs on a CMP row's `Knowledge` cell (process-options.md
    # "Research track & knowledge packs"): a `docs/knowledge/<label>`-shaped ref
    # names a hand-owned pack file. Resolve those to real files — a missing pack
    # is a warn-only advisory, NEVER a gate finding (a pack is advisory context,
    # research-knowledge.md §3a). Skill names and URLs share the cell and are not
    # file-checkable, so only the `docs/knowledge/` prefix is resolved; anything
    # else is left alone. Uses `docs` (not root) so a custom --docs still resolves.
    knowledge_advisories = []
    kn_prefix = "docs/knowledge/"
    for r in cmps:
        cid = r["CMP-ID"]
        for ref in refs(r.get("Knowledge")):
            label = ref.replace("\\", "/")
            if not label.startswith(kn_prefix):
                continue
            label = label[len(kn_prefix) :]
            if not label:
                continue
            rel = label if label.endswith(".md") else label + ".md"
            pack_root = (docs / "knowledge").resolve()
            candidate = (pack_root / rel).resolve()
            try:
                candidate.relative_to(pack_root)
                contained = True
            except ValueError:
                contained = False
            if not contained or not candidate.is_file():
                knowledge_advisories.append(
                    f"CMP {cid} Knowledge ref '{ref}' names no pack ({kn_prefix}{rel})"
                )

    # Interface seams (IF-###, process.md §8): Req-Refs back-links join the
    # --strict failure set like PB's; the ThisProject-vs-LLR-Module endpoint join
    # is a warn-only advisory (module_ids reused from the PB back-link check above).
    interface_backlink_findings, interface_advisories = interface_findings(
        ifs, sr_ids, module_ids
    )
    # The depth-0 FRAME's own resolution rules (WI-442): a crossing's Entity and
    # a relationship's From/To must name declared entities, and an IF row's
    # directional tie-back must name a declared crossing. Its own class rather
    # than folded into the interface findings above, because the report reads
    # them out by name and "Interface findings: relationship REL-002 From
    # references unknown EXT-009" would be a label lying about its contents.
    sr_frame, sr_frame_advisories = sr_boundary_findings(srs, bifs, ifs)
    frame_backlink_findings = (
        frame_findings(exts, bifs, rels) + tieback_findings(ifs, bifs) + sr_frame
    )
    # The IF/CMP schema tier and the IF `Contract` negative rules (WI-443 / OI-14
    # part B) — ALWAYS ON and ALWAYS WARN. They ride the interface advisory pipe
    # rather than `schema` on purpose: `schema` joins the --strict failure set,
    # and the ruled sequencing is warn-first until the corpus converges. Not
    # gated behind --strict-schema either, because a rule nobody runs is the
    # state this item spent three days measuring the drift of.
    interface_advisories += (
        schema_advisories("IF", ifs)
        + schema_advisories("CMP", cmps)
        + schema_advisories("EXT", exts)
        + schema_advisories("B", bifs)
        + schema_advisories("REL", rels)
        + sr_frame_advisories
        + if_contract_advisories(ifs)
        + if_endpoint_class_advisories(ifs, module_ids, docs.parent)
        + if_ownership_advisories(ifs, sr_ids, llr_ids)
        + if_carriage_advisories(ifs)
    )
    # Warn-only, always on (re-tier v2 R4, owner ruling 2026-08-15): an IF row
    # whose owner-side endpoint disagrees with its owner LLR's `Module`. Its OWN
    # pipe rather than the interface-advisory bundle above, for the reason the S2
    # pair got theirs: this is the pre-condition for DELETING a column (`ThisProject`
    # is derivable as owner->LLR->module, wi455 owns the removal), so it is read as
    # a countdown to a schema change and not as one more seam lint. Never joins a
    # failure set below.
    if_this_project_advis = if_this_project_advisories(ifs, llrs)

    phases = set(refs(args.phase)) if args.phase else None
    # The foundation (minimum) phase is never phase-deferred — it is in scope for
    # every delivery filter, which is exactly what a blank Phase bought before the
    # phase back-fill (the phase doctrine, process.md §4). Digit-parse (`v2`/`2` ->
    # 2 — the same parse derive_gate uses) so the minimum compares numerically; an
    # all-blank downstream registry has no parseable phase, so the blank rule below
    # still carries it. The `tag in phases` match stays literal (CLI label-agnostic).
    foundation_phase = min(
        (n for n in (phase_num(s) for s in srs) if n is not None), default=None
    )

    def in_phase(r):
        """In scope when there is no filter, the SR's Phase is blank (downstream
        compat), its phase is listed, or it is the foundation (minimum) phase."""
        tag = (r.get("Phase") or "").strip()
        if phases is None or not tag or tag in phases:
            return True
        n = phase_num(r)
        return n is not None and n == foundation_phase

    status_findings = []
    phase_deferred = []
    # Verification-basis audit surface (process.md §4): of the SRs the project
    # reports Approved, how was each reached? Three kinds, most-to-least runnable —
    # Test rests on a runnable check (mechanized); Demonstration/Manual/Analysis/
    # Inspection/Critique rest on a human observing an outcome (demonstrated/
    # observed — repeatable, but not a runnable check); Attest rests on a named
    # human's recorded judgment (attested — trust-based). Split three ways, not
    # binary (WI-259): once non-Test methods are gate-required, folding them into
    # "mechanized" would overstate how much rests on runnable checks. Independent
    # of --require-verified so the footprint is always visible. The cell is
    # stripped once per row (M-1) before every classification. A blank or
    # unrecognized method falls to the demonstrated/observed else-bucket — the
    # conservative default, so an unknown method is never counted as a runnable
    # check (--strict-schema separately flags an out-of-vocabulary method).
    mechanized_verified, demonstrated_verified, attested_verified = [], [], []
    for r in srs:
        if not is_approved(r):
            continue
        method = (r.get("Verification") or "").strip()
        if method in MECHANIZED_METHODS:
            mechanized_verified.append(r["SR-ID"])
        elif method in ATTESTED_METHODS:
            attested_verified.append(r["SR-ID"])
        else:
            demonstrated_verified.append(r["SR-ID"])
    if args.require_verified:
        for r in srs:
            # The DevBar-Release status bar applies to every ratified SR regardless of
            # Verification method — matching derive_gate.sr_gate, which already
            # demands is_approved for any decomposed SR before DevBar-Release with no
            # per-method carve-out (WI-259, review-2026-07-21 M-5: a Demonstration/
            # Analysis/Inspection SR left Implemented can never derive DevBar-Release yet used
            # to pass this Test-only check — the two scripts disagreeing about the
            # gate is the false-green the kit exists to prevent). A Drafted SR is
            # pre-approval (below DevBar-Reqs, derived-gate §3): it makes no approval
            # claim yet, so the bar stands down — surfaced in the draft count so
            # the exemption stays auditable. Pinned equivalent to sr_gate's
            # is_approved-for-decomposed rule by test_rule_sync.
            if is_drafted(r):
                continue
            if not in_phase(r):
                phase_deferred.append(
                    f"SR {r['SR-ID']} (Phase={r.get('Phase', '').strip()}) — "
                    "status check deferred to its own phase"
                )
                continue
            if not is_approved(r):
                val = (r.get("Status") or "").strip()
                method = (r.get("Verification") or "").strip() or "(blank)"
                status_findings.append(
                    f"SR {r['SR-ID']} is Verification={method} but Status="
                    f"{val or '(blank)'} (DevBar-Release requires Approved for every ratified "
                    "SR regardless of method — the magic Status values are matched "
                    "case-insensitively, so this is a real mismatch, not a casing "
                    "near-miss)"
                )

    raw = {"SR": raw_srs, "LLR": raw_llrs, "TC": raw_tcs}
    real = {"SR": srs, "LLR": llrs, "TC": tcs}
    # CSV structure first (a misaligned row can make every later finding
    # misleading): every registry CSV — spine, off-spine, and project-added —
    # must have each data row parse to the header's column count. Swept by
    # location, not by a known-file list, so a registry this script never joins
    # (interfaces.csv, a project's own additions) is still guarded.
    integrity = [
        f
        for d in (docs / "requirements", docs / "test")
        if d.is_dir()
        for p in sorted(d.glob("*.csv"))
        for f in structure_findings(p, p.relative_to(docs.parent).as_posix())
    ]
    integrity += [f for label in raw for f in integrity_findings(label, raw[label])]
    # The closed `Status` vocabulary (D-9 step 1). INTEGRITY-class rather than
    # schema-class on purpose: `--strict-schema` runs at DevBar-Release only, so
    # a Status closure routed there would never execute in the repos this rule
    # exists for. A row carrying a word no predicate recognizes is invisible to
    # every surface — the re-attest brief, the pending projection, the basis
    # counters — which is a silent, not a loud, failure.
    integrity += [
        f for label in raw for f in enum_integrity_findings(label, raw[label])
    ]
    # The SN tier's duplicate protection (prose registry — see
    # sn_integrity_findings): integrity-class like a duplicated CSV id.
    integrity += getattr(reg, "sn_integrity", [])
    # SR/LLR citation coherence: a TC that cites an SR and an LLR
    # together must not pair an LLR with an SR it does not decompose. Integrity-
    # class (wrong at any stage), so it joins the --strict-integrity floor.
    integrity += triangle_findings(tcs, llrs)
    # PB ids are integrity-checked too, but PB is kept out of the placeholder/
    # schema sweeps above: the budgets registry is optional (like interfaces.csv),
    # so a leftover PB-000 must never block a gate the project doesn't use.
    integrity += integrity_findings("PB", raw_pbs)
    # The coordinator repo-delegation registry (REPO-###, MULTI_REPO.md) is the
    # same kind of optional off-spine registry — integrity-checked, but out of the
    # placeholder/schema sweeps, so a REPO-000 placeholder never blocks it. The
    # legacy modules.csv (MOD-###) rows are integrity-checked under their own key.
    integrity += integrity_findings("REPO", raw_repos)
    integrity += integrity_findings("MOD", raw_mods)
    # The purchased/external parts registry (PART-###, process-options.md) is the
    # same kind of optional off-spine registry — integrity-checked (malformed/
    # duplicate id), but out of the placeholder/schema sweeps and with no back-link
    # resolution (its IF-Ref points at the IF-### tier trace.py doesn't read), so a
    # project that buys nothing keeps its PART-000 placeholder without blocking a gate.
    integrity += integrity_findings("PART", raw_parts)
    # The binary-asset provenance registry (ASSET-###, process-options.md) is the
    # same optional off-spine kind — integrity-checked (malformed/duplicate id),
    # out of the placeholder/schema sweeps and with no back-link resolution, so a
    # project with no binary assets keeps its ASSET-000 placeholder without
    # blocking a gate.
    integrity += integrity_findings("ASSET", raw_assets)
    # The component registry (CMP-###, process-options.md "Component layer") is
    # the same optional off-spine kind — integrity-checked (malformed/duplicate
    # id), out of the placeholder/schema sweeps, so a CMP-000 placeholder never
    # blocks a gate; its PartOf/SupersededBy/membership joins are checked above.
    integrity += integrity_findings("CMP", raw_cmps)
    # The interface-seam registry (IF-###, process.md §8) is the same optional
    # off-spine kind — integrity-checked (malformed/duplicate id), out of the
    # placeholder/schema sweeps, so an IF-000 placeholder never blocks a gate; its
    # Req-Refs back-link and endpoint join are checked below.
    integrity += integrity_findings("IF", raw_ifs)
    placeholders = (
        [f for label in raw for f in placeholder_findings(label, raw[label])]
        + [f"SN placeholder {u} still present" for u in scan_sn_placeholders(sn_md)]
        if args.no_placeholders
        else []
    )
    schema = (
        [f for label in real for f in schema_findings(label, real[label])]
        + phase_ratified_findings(real)
        if args.strict_schema
        else []
    )
    # Warn-only, always on: comparative AcceptanceCriteria terms with no pinned
    # predicate (see the module docstring). Never joins a failure set below.
    advisories = ac_advisories(srs)
    # GATING (owner ruling 2026-07-27): a spine row whose text carries its own
    # provenance. Its own pipe, not folded into the AC advisories above — that
    # counter names the acceptance-criteria lint, and a shared count would say
    # "ac-advisories" about a finding that is not one. Joins exit_code.
    provenance = provenance_findings(srs, llrs, tcs)
    # GATING (WI-328): requirement FORM — one `shall` per requirement, no weak
    # modal, no actorless passive, no unfalsifiable term, no open-ended clause, no
    # `shall` in an LLR. Same pipe as provenance: both are "is this row readable
    # and decidable on its own", and splitting them across two counters would make
    # a reader check two places for one answer. Joins exit_code.
    form = form_findings(srs, llrs, tcs)
    # Warn-only, always on (WI-328): a child cell that re-words its parent. A
    # heuristic (lexical overlap), so it warns FOREVER — 38 of 118 LLRs trip it
    # and most are legitimate. Never joins a failure set below.
    paraphrase = paraphrase_advisories(srs, llrs)
    # Warn-only, always on (WI-129): an LLR reading below Approved while every
    # citing TC is Approved — a readout drift, never a failure (LLR status is
    # non-gating under the derived-gate model). Never joins a failure set below.
    llr_status_advis = llr_status_advisories(llrs, tcs)
    # Warn-only, always on (WI-316): a Modified LLR/TC whose owning SR is not
    # flagged — the amendment is invisible to the re-attest surfaces, which all
    # key off the SR row. Same never-gating tier as the status-coherence lint;
    # rendered through the same channel (one advisory pipe, two lints).
    llr_status_advis = llr_status_advis + modified_chain_advisories(srs, llrs, tcs)
    # Warn-only, always on (re-tier v2 R2/R3, owner ruling 2026-08-15): an SR
    # `Requirement` naming a concrete artifact, and an SR whose direct-LLR fan-out
    # is over the declared bound. Their own pipes — they are TIERING detectors,
    # not prose lints, and folding them into the AC/paraphrase counters would
    # report a tiering defect under a wording heading. Never joins a failure set
    # below: warn-first by ruling, cleared by the re-tier campaign, not by a gate.
    sr_artifact_advis = sr_artifact_advisories(srs)
    sr_fanout_advis = sr_fanout_advisories(srs, llrs)
    # Warn-only, always on: a row whose prose names a critique instrument while
    # its Verification says otherwise. Its own pipe for the same reason the two
    # above have theirs — this is a METHOD-coherence finding, not a wording one,
    # and reporting it under the acceptance-criteria counter would mis-name it
    # (it scans Requirement and Rationale too). Never joins a failure set.
    verif_coherence_advis = verification_coherence_advisories(srs)

    # Drafted artifacts (derived-gate model §3): the rows exempted from the
    # child-completeness orphan rules + the --require-verified criterion. Listed
    # so the exemption stays auditable (the whole point of the model is that a
    # Drafted row lives in the live spine while being drafted, not silently).
    draft_srs = [r for r in srs if is_drafted(r)]
    draft_llrs = [r for r in llrs if is_drafted(r)]
    draft_tcs = [r for r in tcs if is_drafted(r)]
    n_draft = len(draft_srs) + len(draft_llrs) + len(draft_tcs) + len(sn_draft)

    # Optional Aspect column (the ruled cross-cutting review grouping): count
    # real SRs per aspect so coverage is visible. Report-only — never a finding,
    # never an exit-code change; a registry without the column contributes
    # nothing. The VALUE set is closed and checked by --strict-schema
    # (ENUM_FIELDS); this is only the count.
    area_counts = {}
    for r in srs:
        area = (r.get("Aspect") or "").strip()
        if area:
            area_counts[area] = area_counts.get(area, 0) + 1
    findings = Findings()
    findings.orphans = orphans
    findings.orphan_ids = orphan_ids
    findings.integrity = integrity
    findings.placeholders = placeholders
    findings.schema = schema
    findings.advisories = advisories
    # Filled after analyze() returns: the id-watermark rules read the
    # filesystem and git, which analyze()'s pure contract forbids.
    findings.watermark_advisories = []
    # Filled after analyze() returns, for the same reason: the snapshot's
    # unanchored rule reads the `docs/archive/last_approved/` tree.
    findings.snapshot_advisories = []
    findings.provenance = provenance
    findings.form = form
    findings.paraphrase = paraphrase
    findings.llr_status_advis = llr_status_advis
    findings.sr_artifact_advis = sr_artifact_advis
    findings.sr_fanout_advis = sr_fanout_advis
    findings.verif_coherence_advis = verif_coherence_advis
    findings.if_this_project_advis = if_this_project_advis
    findings.budget_findings = budget_findings
    findings.module_findings = module_findings
    findings.component_findings = component_findings
    findings.knowledge_advisories = knowledge_advisories
    findings.interface_backlink_findings = interface_backlink_findings
    findings.frame_backlink_findings = frame_backlink_findings
    findings.interface_advisories = interface_advisories
    findings.status_findings = status_findings
    findings.phase_deferred = phase_deferred
    findings.phases = phases
    findings.mechanized_verified = mechanized_verified
    findings.demonstrated_verified = demonstrated_verified
    findings.attested_verified = attested_verified
    findings.draft_srs = draft_srs
    findings.draft_llrs = draft_llrs
    findings.draft_tcs = draft_tcs
    findings.n_draft = n_draft
    findings.area_counts = area_counts
    return findings


def render_report(reg, findings, args, forest):
    """Assemble the full report.md text (the metric table, the SR->LLR->TC matrix, the outline + mermaid views over `forest`, the orphan/integrity/advisory sections, and the flag-gated off-spine/draft/area/status sections). Pure — returns the text; the caller writes it."""
    srs, llrs, tcs = reg.srs, reg.llrs, reg.tcs
    pbs, mods, parts = reg.pbs, reg.mods, reg.parts
    assets, cmps, ifs = reg.assets, reg.cmps, reg.ifs
    exts, bifs, rels = reg.exts, reg.bifs, reg.rels
    sn_ids, sn_draft = reg.sn_ids, reg.sn_draft
    orphans = findings.orphans
    orphan_ids = findings.orphan_ids
    integrity = findings.integrity
    placeholders = findings.placeholders
    schema = findings.schema
    advisories = findings.advisories
    provenance = findings.provenance
    form = findings.form
    paraphrase = findings.paraphrase
    llr_status_advis = findings.llr_status_advis
    sr_artifact_advis = findings.sr_artifact_advis
    sr_fanout_advis = findings.sr_fanout_advis
    verif_coherence_advis = findings.verif_coherence_advis
    if_this_project_advis = findings.if_this_project_advis
    budget_findings = findings.budget_findings
    module_findings = findings.module_findings
    component_findings = findings.component_findings
    knowledge_advisories = findings.knowledge_advisories
    interface_backlink_findings = findings.interface_backlink_findings
    frame_backlink_findings = findings.frame_backlink_findings
    interface_advisories = findings.interface_advisories
    status_findings = findings.status_findings
    phase_deferred = findings.phase_deferred
    phases = findings.phases
    mechanized_verified = findings.mechanized_verified
    demonstrated_verified = findings.demonstrated_verified
    attested_verified = findings.attested_verified
    draft_srs = findings.draft_srs
    draft_llrs = findings.draft_llrs
    draft_tcs = findings.draft_tcs
    n_draft = findings.n_draft
    area_counts = findings.area_counts

    lines = (
        [
            "# Coverage & Traceability Report",
            "",
            "_Generated by `scripts/trace.py`. Do not edit by hand._",
            "",
            "| Metric | Count |",
            "|---|---|",
            f"| Stakeholder needs (SN) | {len(sn_ids)} |",
            f"| System requirements (SR) | {len(srs)} |",
            f"| Low-level requirements (LLR) | {len(llrs)} |",
            f"| Test cases (TC) | {len(tcs)} |",
            f"| Orphans | {len(orphans)} |",
            f"| Integrity findings | {len(integrity)} |",
            f"| Approved SRs — mechanized (Test) | {len(mechanized_verified)} |",
            f"| Approved SRs — demonstrated/observed | {len(demonstrated_verified)} |",
            f"| Approved SRs — attested (human, §4) | {len(attested_verified)} |",
        ]
        + (
            [f"| Drafted artifacts (decomposition-exempt) | {n_draft} |"]
            if n_draft
            else []
        )
        + (
            [f"| Status findings | {len(status_findings)} |"]
            if args.require_verified
            else []
        )
        + (
            [f"| Placeholder findings | {len(placeholders)} |"]
            if args.no_placeholders
            else []
        )
        + ([f"| Schema findings | {len(schema)} |"] if args.strict_schema else [])
        + (
            [
                f"| Performance budgets (PB) | {len(pbs)} |",
                f"| Budget findings | {len(budget_findings)} |",
            ]
            if pbs
            else []
        )
        + (
            [
                f"| Delegated repos (REPO) | {len(mods)} |",
                f"| Delegation findings | {len(module_findings)} |",
            ]
            if mods
            else []
        )
        + ([f"| Purchased parts (PART) | {len(parts)} |"] if parts else [])
        + ([f"| Binary assets (ASSET) | {len(assets)} |"] if assets else [])
        + (
            [
                f"| Components (CMP) | {len(cmps)} |",
                f"| Component findings | {len(component_findings)} |",
            ]
            if cmps
            else []
        )
        + (
            [
                f"| Interface seams (IF) | {len(ifs)} |",
                f"| Interface findings | {len(interface_backlink_findings)} |",
            ]
            if ifs
            else []
        )
        + (
            [
                f"| Frame: entities/crossings/relationships | "
                f"{len(exts)}/{len(bifs)}/{len(rels)} |",
                f"| Frame findings | {len(frame_backlink_findings)} |",
            ]
            if exts or bifs or rels
            else []
        )
        + [
            "",
            "## SR -> LLR -> TC matrix",
            "",
            "| SR | LLRs | TCs | Status |",
            "|---|---|---|---|",
        ]
    )
    llrs_by_sr = _bucket_by_ref(llrs, "SR-Refs")
    tcs_by_sr = _bucket_by_ref(tcs, "Verifies")
    for r in srs:
        sid = r["SR-ID"]
        kids = " ".join(x["LLR-ID"] for x in llrs_by_sr.get(sid, []))
        tests = " ".join(x["TC-ID"] for x in tcs_by_sr.get(sid, []))
        lines.append(f"| {sid} | {kids} | {tests} | {r.get('Status', '')} |")

    lines += [
        "",
        "## Traceability outline",
        "",
        "_`SN -> SR -> LLR -> TC`; `[Status]` and `[orphan]` flags are inline._",
        "",
    ]
    lines += outline_lines(forest)
    lines += [
        "",
        "## Traceability graph",
        "",
        "_The chain as a DAG, colored by state (orphan/draft stand out). Small and "
        "diff-friendly; run `--html` for the scalable full-graph view._",
        "",
    ]
    lines += mermaid_graph(sn_ids, srs, llrs, tcs, orphan_ids, sn_draft)

    lines += ["", "## Orphans", ""]
    lines += ["None. Full coverage."] if not orphans else [f"- {o}" for o in orphans]
    lines += ["", "## Integrity", ""]
    lines += (
        ["None. Ids are unique and well-formed."]
        if not integrity
        else [f"- {f}" for f in integrity]
    )
    # Warn-only advisory section (never a failure): comparative acceptance-
    # criteria wording that names no predicate. The DevBar-Reqs consistency review
    # (process.md §4) decides — pin the predicate or accept it knowingly.
    lines += ["", "## Acceptance-criteria advisories (warn-only)", ""]
    lines += (
        ["None. No unpinned comparative terms."]
        if not advisories
        else [f"- {f}" for f in advisories]
    )
    # GATING section: a spine row states the system, not its own history. Failing
    # under --strict rather than warning, because a warn nobody must act on is how
    # 43 rows accumulated before anyone looked below the SR layer.
    lines += ["", "## Spine stand-alone findings (gating under --strict)", ""]
    lines += (
        ["None. No spine row cites a work item or a process doc in its text."]
        if not provenance
        else [f"- {f}" for f in provenance]
    )
    # GATING section (WI-328): requirement form — one testable obligation per row.
    lines += ["", "## Requirement form findings (gating under --strict)", ""]
    lines += (
        ["None. Every requirement states one obligation in decidable terms."]
        if not form
        else [f"- {f}" for f in form]
    )
    # Warn-only section: a child cell re-wording its parent. Heuristic, never gates.
    lines += ["", "## Paraphrase advisories (warn-only heuristic)", ""]
    lines += (
        ["None flagged by the overlap heuristic."]
        if not paraphrase
        else [f"- {f}" for f in paraphrase]
    )
    # Warn-only advisory section (never a failure, WI-129 + WI-316): LLRs reading
    # below Approved whose citing TCs are all Approved (lift the Status cell by
    # hand — registries are hand-owned SSOT, no generator writes them back), and
    # Modified LLR/TC rows whose owning SR is not flagged (flip the attestation
    # unit — no brief, projection or gate carries a Modified child under an
    # Approved SR).
    lines += ["", "## Status-coherence advisories (warn-only)", ""]
    lines += (
        [
            "None. No unlifted LLRs, no Modified chain rows riding an unflagged "
            "or unresolvable owning SR."
        ]
        if not llr_status_advis
        else [f"- {f}" for f in llr_status_advis]
    )
    # Warn-only sections (re-tier v2 R2/R3): the two tiering detectors. Never a
    # failure under any flag — a merged row and a mis-tiered artifact name are
    # cleared by re-writing requirements, which is the campaign's schedule, not
    # the checker's.
    lines += ["", "## Artifact-naming advisories (warn-only)", ""]
    lines += (
        ["None. No requirement cell names a concrete artifact."]
        if not sr_artifact_advis
        else [f"- {f}" for f in sr_artifact_advis]
    )
    lines += ["", "## Verification-coherence advisories (warn-only)", ""]
    lines += (
        ["None. No requirement states two verification methods."]
        if not verif_coherence_advis
        else [f"- {f}" for f in verif_coherence_advis]
    )
    lines += ["", "## Fan-out advisories (warn-only)", ""]
    lines += (
        ["None. No SR's direct-LLR fan-out exceeds the declared bound."]
        if not sr_fanout_advis
        else [f"- {f}" for f in sr_fanout_advis]
    )
    # Warn-only (re-tier v2 R4): the countdown to dropping `ThisProject` — every
    # row where the cell and its owner LLR's Module still disagree, so the
    # derivation that makes the column redundant cannot yet be trusted.
    lines += ["", "## ThisProject derivability advisories (warn-only)", ""]
    lines += (
        [
            "None. Every LLR-owned row's owner-side endpoint agrees with its "
            "owner's Module."
        ]
        if not if_this_project_advis
        else [f"- {f}" for f in if_this_project_advis]
    )
    # Verification-basis surface (process.md §4): make the project's trust
    # footprint auditable — of what is `Approved`, how much rests on a runnable
    # check (Test), on a human observing an outcome (Demonstration/Manual/Analysis/
    # Inspection/Critique), or on a named human's recorded judgment (Attest)? Split
    # three ways (WI-259) so non-Test approval claims are never folded into
    # "mechanized"; the demonstrated and attested ids are listed so an audit can
    # see exactly which rows rest on something other than a runnable check.
    lines += ["", "## Verification basis (mechanized / demonstrated / attested)", ""]
    lines += [
        "_Of the SRs reported `Approved`: `Test` rows rest on a runnable, "
        "re-executable check (mechanized); `Demonstration`/`Manual`/`Analysis`/"
        "`Inspection`/`Critique` rows rest on a human observing an outcome "
        "(demonstrated/observed — repeatable, but not a runnable check); `Attest` "
        "rows rest on a named human's recorded judgment (trust-based — the box can "
        "be checked without the work having happened, process.md §4). Only the "
        "first is a runnable check. A row whose method is blank or unrecognized is "
        "counted as demonstrated/observed, never as mechanized (the conservative "
        "default — it does not rest on a runnable check unless proven so)._",
        "",
        f"- Mechanized (Test): {len(mechanized_verified)}",
        "- Demonstrated/observed (Demonstration/Manual/Analysis/Inspection/"
        f"Critique, or unspecified): {len(demonstrated_verified)}"
        + (f" — {', '.join(demonstrated_verified)}" if demonstrated_verified else ""),
        f"- Attested (Attest): {len(attested_verified)}"
        + (f" — {', '.join(attested_verified)}" if attested_verified else ""),
    ]
    if n_draft:
        lines += ["", "## Drafted artifacts (decomposition-exempt)", ""]
        lines += [
            "_`Drafted` rows are exempt from the child-completeness orphan rules and "
            "the DevBar-Release approval criterion (derived-gate model §3): a requirement lives "
            "in the live spine while it is drafted. Listed so the exemption is "
            "auditable._",
            "",
        ]
        lines += [f"- {u} (SN, unratified section)" for u in sorted(sn_draft)]
        lines += [
            f"- {r[id_key(label)]} — {_cell(r, 'Title') or _cell(r, 'Method')}"
            for label, rows_ in (
                ("SR", draft_srs),
                ("LLR", draft_llrs),
                ("TC", draft_tcs),
            )
            for r in rows_
        ]
    if area_counts:
        untagged = len(srs) - sum(area_counts.values())
        lines += [
            "",
            "## SRs by aspect (report-only)",
            "",
            "_The ruled cross-cutting review grouping. Counts only — never a "
            "gate; a row carrying no aspect is simply not cross-cutting, which "
            "is normal rather than a gap._",
            "",
        ]
        lines += [f"- {a}: {n}" for a, n in sorted(area_counts.items())]
        if untagged:
            lines.append(f"- (no aspect): {untagged}")
    if pbs:
        lines += ["", "## Performance budgets (§9 back-links)", ""]
        lines += (
            [f"{len(pbs)} budget row(s); every Refs resolves to a real SR/LLR/Module."]
            if not budget_findings
            else [f"- {f}" for f in budget_findings]
        )
    if mods:
        lines += ["", "## Delegated repos (MULTI_REPO.md delegation back-links)", ""]
        lines += (
            [
                f"{len(mods)} delegated-repo row(s); every DelegatedSRs resolves "
                "to a real SR."
            ]
            if not module_findings
            else [f"- {f}" for f in module_findings]
        )
    if parts:
        lines += ["", "## Purchased parts (process-options.md)", ""]
        lines += [
            f"{len(parts)} part row(s); each IF-Ref names its owning interface row "
            "of record (MULTI_REPO.md §3.3), integrity-checked only."
        ]
    if assets:
        lines += ["", "## Binary assets (process-options.md)", ""]
        lines += [
            f"{len(assets)} asset row(s); provenance/license/hash tracked in text "
            "(the ideal-not-requirement stance), integrity-checked only."
        ]
    if cmps:
        lines += ["", "## Components (process-options.md component layer)", ""]
        lines += (
            [
                f"{len(cmps)} component row(s); PartOf/SupersededBy resolve and "
                "every primitive `Component` tag names a real CMP row."
            ]
            if not component_findings
            else [f"- {f}" for f in component_findings]
        )
        if knowledge_advisories:
            lines += ["", "### Knowledge-pack advisories (warn-only)", ""]
            lines += [f"- {a}" for a in knowledge_advisories]
    if ifs:
        lines += ["", "## Interface seams (process.md §8 back-links)", ""]
        lines += (
            [f"{len(ifs)} interface-seam row(s); every Req-Refs resolves to a real SR."]
            if not interface_backlink_findings
            else [f"- {f}" for f in interface_backlink_findings]
        )
        if interface_advisories:
            lines += ["", "### Interface endpoint advisories (warn-only)", ""]
            lines += [f"- {a}" for a in interface_advisories]
    lines += _frame_report_section(exts, bifs, rels, frame_backlink_findings)
    if args.no_placeholders:
        lines += ["", "## Placeholders (--no-placeholders)", ""]
        lines += (
            ["None. No '-000' template rows remain."]
            if not placeholders
            else [f"- {f}" for f in placeholders]
        )
    if args.strict_schema:
        lines += ["", "## Schema findings (--strict-schema)", ""]
        lines += (
            ["None. Required fields present; Verification/Tier in vocabulary."]
            if not schema
            else [f"- {f}" for f in schema]
        )
    if args.require_verified:
        scope = f" — phase scope: {args.phase}" if phases else ""
        lines += ["", f"## Status findings (--require-verified{scope})", ""]
        lines += (
            ["None. Every in-scope ratified SR is Approved (any method)."]
            if not status_findings
            else [f"- {s}" for s in status_findings]
        )
        if phase_deferred:
            lines += ["", "### Phase-deferred (explicitly out of scope)", ""]
            lines += [f"- {s}" for s in phase_deferred]
    return "\n".join(lines) + "\n"


def render_console(reg, findings, args, out, html_out):
    """Print the warn-only advisory lines and the one-line Traceability summary to stdout (loud but never gating)."""
    sn_ids = reg.sn_ids
    srs, llrs, tcs = reg.srs, reg.llrs, reg.tcs
    pbs, mods, parts = reg.pbs, reg.mods, reg.parts
    assets, cmps, ifs = reg.assets, reg.cmps, reg.ifs
    exts, bifs, rels = reg.exts, reg.bifs, reg.rels
    orphans = findings.orphans
    integrity = findings.integrity
    advisories = findings.advisories
    provenance = findings.provenance
    form = findings.form
    paraphrase = findings.paraphrase
    interface_advisories = findings.interface_advisories
    knowledge_advisories = findings.knowledge_advisories
    llr_status_advis = findings.llr_status_advis
    sr_artifact_advis = findings.sr_artifact_advis
    sr_fanout_advis = findings.sr_fanout_advis
    verif_coherence_advis = findings.verif_coherence_advis
    if_this_project_advis = findings.if_this_project_advis
    watermark_advis = findings.watermark_advisories
    snapshot_advis = findings.snapshot_advisories
    mechanized_verified = findings.mechanized_verified
    demonstrated_verified = findings.demonstrated_verified
    attested_verified = findings.attested_verified
    status_findings = findings.status_findings
    n_draft = findings.n_draft
    placeholders = findings.placeholders
    schema = findings.schema
    phases = findings.phases
    phase_deferred = findings.phase_deferred
    budget_findings = findings.budget_findings
    module_findings = findings.module_findings
    component_findings = findings.component_findings
    interface_backlink_findings = findings.interface_backlink_findings
    frame_backlink_findings = findings.frame_backlink_findings

    # Advisories are loud (stdout, not just the report) but never fail the run.
    # One loop over the ordered concatenation, not one loop per pipe: the pipes
    # stay separate where it matters (their own report sections and counters) and
    # a fifth lint no longer costs this routine a branch.
    for a in (
        advisories
        + interface_advisories
        + knowledge_advisories
        + llr_status_advis
        + paraphrase
        + sr_artifact_advis
        + sr_fanout_advis
        + verif_coherence_advis
        + if_this_project_advis
        + watermark_advis
        + snapshot_advis
    ):
        print(f"WARNING (advisory): {a}")
    for f in provenance:
        print(f"FINDING (spine stand-alone): {f}")
    for f in form:
        print(f"FINDING (requirement form): {f}")
    # Gating findings print here too, not only as counts: the report file is
    # gitignored, and the harness bar is "print the real output — never
    # summarize a failure away" (check.py). Mirrors exit_code()'s composition;
    # capped per class, the report holds the full lists.
    cap = 10
    if args.strict:
        failing = [
            ("orphan", orphans),
            ("integrity", integrity),
            ("status", status_findings),
            ("placeholder", placeholders),
            ("schema", schema),
            ("budget", budget_findings),
            ("delegation", module_findings),
            ("component", component_findings),
            ("interface", interface_backlink_findings),
            ("frame", frame_backlink_findings),
        ]
    elif args.strict_integrity:
        failing = [("integrity", integrity)]
    else:
        failing = []
    for label, items in failing:
        for f in items[:cap]:
            print(f"FINDING ({label}): {f}")
        if len(items) > cap:
            print(f"... +{len(items) - cap} more {label} finding(s) in the report")
    print(
        f"Traceability: SN={len(sn_ids)} SR={len(srs)} LLR={len(llrs)} "
        f"TC={len(tcs)} orphans={len(orphans)} integrity={len(integrity)}"
        + (
            f" verified-mechanized={len(mechanized_verified)}"
            f" verified-demonstrated={len(demonstrated_verified)}"
            f" verified-attested={len(attested_verified)}"
            if (demonstrated_verified or attested_verified)
            else ""
        )
        + (f" status-findings={len(status_findings)}" if args.require_verified else "")
        + (f" drafts={n_draft}" if n_draft else "")
        + (f" placeholders={len(placeholders)}" if args.no_placeholders else "")
        + (f" schema-findings={len(schema)}" if args.strict_schema else "")
        + (f" phase-deferred={len(phase_deferred)}" if phases else "")
        + (f" budgets={len(pbs)} budget-findings={len(budget_findings)}" if pbs else "")
        + (
            f" repos={len(mods)} delegation-findings={len(module_findings)}"
            if mods
            else ""
        )
        + (f" parts={len(parts)}" if parts else "")
        + (f" assets={len(assets)}" if assets else "")
        + (
            f" components={len(cmps)} component-findings={len(component_findings)}"
            if cmps
            else ""
        )
        + (
            f" knowledge-advisories={len(knowledge_advisories)}"
            if knowledge_advisories
            else ""
        )
        + (
            f" interfaces={len(ifs)} "
            f"interface-findings={len(interface_backlink_findings)}"
            if ifs
            else ""
        )
        + (f" ac-advisories={len(advisories)}" if advisories else "")
        + (f" provenance-findings={len(provenance)}" if provenance else "")
        + (f" form-findings={len(form)}" if form else "")
        + (f" paraphrase-advisories={len(paraphrase)}" if paraphrase else "")
        + (
            f" llr-status-advisories={len(llr_status_advis)}"
            if llr_status_advis
            else ""
        )
        + (f" watermark-advisories={len(watermark_advis)}" if watermark_advis else "")
        + (f" unanchored-advisories={len(snapshot_advis)}" if snapshot_advis else "")
        + f". Report -> {out}"
        + (f" + {html_out}" if html_out else "")
    )


def exit_code(findings, args):
    """The gate exit code: 1 under --strict if any orphan/status/integrity/placeholder/schema/off-spine finding exists; 1 under --strict-integrity if any integrity finding exists; else 0."""
    if args.strict and (
        findings.orphans
        or findings.status_findings
        or findings.integrity
        or findings.placeholders
        or findings.schema
        or findings.budget_findings
        or findings.module_findings
        or findings.component_findings
        or findings.interface_backlink_findings
        or findings.frame_backlink_findings
        or findings.provenance
        or findings.form
    ):
        return 1
    if args.strict_integrity and findings.integrity:
        return 1
    return 0


def _cmd_bump_ids(root):
    """`--bump-ids`: raise every mark to the live maximum and report what moved."""
    marks, raised = bump_watermark(root)
    for space, (was, now) in sorted(raised.items()):
        print("trace: id watermark {} {} -> {}".format(space, was, now))
    print(
        "trace: id watermark written -> {} ({} space(s), {} raised)".format(
            WATERMARK, len(marks), len(raised)
        )
    )
    return 0


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict", action="store_true", help="exit 1 if any orphan / status finding"
    )
    ap.add_argument(
        "--bump-ids",
        action="store_true",
        help="raise every id-watermark mark to the live maximum and exit — the "
        "regeneration workflow for docs/id-watermark (a mark only ever rises)",
    )
    ap.add_argument(
        "--strict-integrity",
        action="store_true",
        help="exit 1 only on integrity findings (duplicate/malformed ids) — the "
        "always-valid floor the pre-commit hook runs; orphans stay gate-scoped",
    )
    ap.add_argument(
        "--require-verified",
        action="store_true",
        help="DevBar-Release criterion: flag non-Drafted SRs not Status=Approved "
        "(any Verification method)",
    )
    ap.add_argument(
        "--phase",
        default=None,
        help="comma-separated phases in scope (e.g. v1 or v1,v2): scopes "
        "--require-verified to SRs whose Phase is blank or listed",
    )
    ap.add_argument(
        "--no-placeholders",
        action="store_true",
        help="flag any leftover '-000' template example row (use from DevBar-Tests on)",
    )
    ap.add_argument(
        "--strict-schema",
        action="store_true",
        help="also require non-empty required fields and valid "
        "Verification/Tier values on the real rows",
    )
    ap.add_argument(
        "--html",
        action="store_true",
        help="also write test/report.html — a dependency-free collapsible tree "
        "of the full graph (gitignored composite artifact)",
    )
    ap.add_argument(
        "--ratify",
        metavar="SCOPE",
        default=None,
        help="emit ONLY the batch-scoped ratification hierarchy (SN->SR->LLR->TC "
        "with prose) for SCOPE — a phase tag (e.g. v3) or an SR-id list "
        "(e.g. 'SR-052,SR-053'); a DevBar-Reqs/DevBar-Tests brief links this instead of hand-copying "
        "rows (WI-146). The reserved scope 'modified' (WI-316) emits the "
        "RE-ATTESTATION brief instead: per-cell before/after for every row owing "
        "a human act, against its copy in docs/archive/last_approved/. A scope "
        "matching nothing is REFUSED, never rendered empty. Prints to stdout "
        "unless --out is given; runs no checks",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="with --ratify modified: FRESHNESS mode. Re-render the brief and "
        "compare it against the committed file (--out, else the newest "
        "docs/ratify/*.md), exiting nonzero when they differ. A plain "
        "regenerate-and-compare — the baseline is a directory of files, so "
        "there is nothing a re-render could move (WI-325's blocker dissolved "
        "with the git-derived baseline). Silent no-op when there is no brief, "
        "or when no row owes an act (the window is closed and the brief is a "
        "record, not a live surface)",
    )
    ap.add_argument(
        "--out",
        metavar="FILE",
        default=None,
        help="with --ratify, write the view to FILE (parent dirs created) instead "
        "of stdout, so a brief can link a stable path",
    )
    # --root/--docs path flags: here and in check_perf.py an explicit --docs is
    # a PATH used as-is (--root ignored); check_docs.py instead treats --docs as
    # a name joined under --root (absolute paths still win via pathlib join).
    # The three agree for the default and for absolute --docs; they differ for a
    # relative explicit --docs — state it rather than claim a uniformity that
    # isn't there (repo-review 2026-07-21 L-1; full unification is a
    # coordinated change across check_flows/gen_release_checklist too).
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--docs",
        default=None,
        help="docs directory path, used as-is (default: <root>/docs)",
    )
    args = ap.parse_args()
    docs = Path(args.docs) if args.docs else Path(args.root) / "docs"

    # --bump-ids is a WRITER, not a checker: raise the marks and exit before any
    # pass runs, so regenerating never depends on the tree already being clean.
    if args.bump_ids:
        return _cmd_bump_ids(args.root)

    reg = load_registries(docs)

    # --ratify is a generator mode, not a checker: emit the batch-scoped
    # ratification hierarchy and exit 0 without running any orphan/integrity pass
    # (WI-146a). It reuses the loaded, example-filtered working sets above.
    # A RESERVED scope (`_RESERVED_RATIFY_SCOPES` — `modified` today) emits the
    # re-attestation brief instead: per-cell before/after for every row owing a
    # human act, against its copy in the `last_approved` snapshot. Anything else
    # is a phase tag or an id list, and `_scope_srs` REFUSES one that matches
    # nothing rather than rendering an empty brief.
    if args.ratify is not None:
        reserved = args.ratify.strip().lower() in _RESERVED_RATIFY_SCOPES
        if reserved and args.check:
            # WI-325: freshness, not generation. A plain regenerate-and-compare
            # now that the baseline is a directory rather than a self-stamp.
            code, message = ratify_check(
                Path(args.root),
                reg.srs,
                reg.llrs,
                reg.tcs,
                Path(args.out)
                if args.out
                else (
                    newest_ratify_brief(Path(args.root))
                    or Path(args.root) / "docs" / "ratify" / "(none)"
                ),
            )
            print("trace: ratify-check — {}".format(message), file=sys.stderr)
            # `main()` is called bare at the bottom of this module, so a plain
            # `return` sets no exit status — this check must sys.exit like the
            # analyze path does, or it reports STALE and exits 0. (It did.)
            if code:
                sys.exit(code)
            return 0
        if reserved:
            body = reattest_lines(Path(args.root), reg.srs, reg.llrs, reg.tcs)
        else:
            body = ratify_lines(
                args.ratify, reg.sn_ids, reg.srs, reg.llrs, reg.tcs, reg.sn_meta
            )
        text = "\n".join(body) + "\n"
        if args.out:
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8", newline="\n")
            print("trace: wrote ratification view -> {}".format(out_path))
        else:
            sys.stdout.write(text)
        return 0

    findings = analyze(reg, args)
    # The id-watermark rules read the FILESYSTEM and GIT, so they cannot live in
    # analyze() — that function's contract is "Pure … No I/O", and the whole
    # value of the contract is that it stays true. Integrity-class all the same:
    # appended here so --strict-integrity (the always-on pre-commit floor) gates
    # on it exactly like a duplicated id.
    # Follow --docs. `WATERMARK` is docs-relative, so a run pointed at another
    # docs tree must read THAT tree's mark; using args.root regardless would
    # check an unrelated (often empty) tree and then report integrity=0 about a
    # spine it never looked at.
    wm_root = docs.parent if args.docs else Path(args.root)
    committed = committed_watermark(wm_root)
    findings.integrity += watermark_findings(wm_root, committed)
    if committed is None:
        # SILENCE IS NOT SUCCESS. "A mark only ever rises" cannot be read from the
        # working tree — a lowered mark looks exactly like a correct one — so with
        # no committed baseline the rule did not run. Say so: an unrun rule that
        # prints nothing is indistinguishable from one that passed.
        # ITS OWN PIPE, for the reason stated where `advisories` is built:
        # that counter names the acceptance-criteria lint, and folding an
        # unrelated notice into it reports "ac-advisories=1" about a row whose
        # AcceptanceCriteria is fine — which is exactly what it did until now.
        findings.watermark_advisories.append(
            "id-watermark monotonicity NOT checked — no committed {} to compare "
            "against (first commit, shallow clone, or off a work tree); the "
            "live-id and complete-space rules still ran".format(WATERMARK)
        )
    # THE UNANCHORED RULE (snapshot design §B4), as an ALWAYS-ON ADVISORY.
    # A row whose live maturity claims approval-or-above, with no copy in
    # `docs/archive/last_approved/` recording it — or a copy that reads below it
    # — is an approval that never rode a copy, which is the laundering the whole
    # mechanism exists to make visible. It was DEFINED and CALLED BY NOTHING
    # until adversarial round 2 (2026-08-15) measured that: an approval could
    # bypass the record and no live check would say so.
    #
    # ADVISORY, and the deferral is the design's, not a softening: §B4 arms this
    # as an integrity ERROR at migration step 7 and DELIBERATELY NOT BEFORE,
    # because against a pre-seed snapshot (there is none yet) or a pre-rename one
    # it reds every row in the repo, and a check that reds everything is a check
    # that gets switched off. Warn-first is what lets it run in the meantime, and
    # running is what makes the step-7 promotion a one-line change to a rule
    # already proven quiet rather than a rule nobody has ever seen fire.
    # Vacuous today by construction: no snapshot directory exists, so the
    # function returns [] and this pipe adds nothing to live output.
    # `wm_root` rather than `args.root` for the reason stated just above it: the
    # snapshot root is `<root>/docs/archive/last_approved`, so a run pointed at
    # another docs tree must read THAT tree's record, not this one's.
    findings.snapshot_advisories = baseline_snapshot.unanchored_findings(wm_root)
    forest = build_forest(
        reg.sn_ids, reg.srs, reg.llrs, reg.tcs, findings.orphan_ids, reg.sn_draft
    )

    out = docs / "test" / "report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        render_report(reg, findings, args, forest), encoding="utf-8", newline="\n"
    )

    html_out = None
    if args.html:
        html_out = docs / "test" / "report.html"
        html_out.write_text(html_document(forest), encoding="utf-8", newline="\n")

    render_console(reg, findings, args, out, html_out)

    code = exit_code(findings, args)
    if code:
        sys.exit(code)


if __name__ == "__main__":
    main()
