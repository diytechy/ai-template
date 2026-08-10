#!/usr/bin/env python3
"""Traceability join + orphan report for the SN->SR->LLR->TC registries.

Stack-agnostic reference implementation (Python 3, standard library only — no
pip installs). Drop it in a new repo as `scripts/trace.py` and wire it into the
check harness / CI. It is the generated "traceability matrix" referenced by
PROCESS.md: it never needs hand-maintaining.

Usage:
    python scripts/trace.py [--strict] [--strict-integrity] [--require-verified]
                            [--phase LIST] [--no-placeholders] [--strict-schema]
                            [--html] [--ratify SCOPE [--out FILE] [--since REV]]
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
stage, while orphans are a G2+ gate criterion).

The method rules this script mechanizes are stated ONCE elsewhere — they are NOT
restated here (the kit's decompose-don't-paraphrase rule applied to itself):
    - the orphan rules (an SR needs an LLR unless Verification is
      Analysis/Inspection/Attest, a TC, and — when a needs file exists — an SN;
      LLR/TC parentage), the Draft child-completeness exemption, and the
      Draft->Planned->Verified ladder: process.md §4 + the derived-gate model
      (docs/specs/derived-gate-model.md §3, and §4a for section-as-state SN
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

Flags in brief: --require-verified adds the G3 criterion "a Verification=Test SR
is Status=Verified" (Draft SRs exempt); --no-placeholders flags leftover "-000"
example rows (wire in from G2 on); --strict-schema adds required-field,
closed-vocabulary, and "Automated=Yes cites Evidence" checks over the real rows;
--ratify SCOPE emits ONLY the batch-scoped ratification hierarchy (a phase tag or
an SR-id list) to stdout or --out and runs no checks (WI-146); the reserved scope
`modified` (WI-316) emits the re-attestation brief instead — per-cell
before/after for every `Modified` SR's chain against its attested baseline (the
newest revision where the SR row read `Verified`; `--since REV` overrides). Warn-only
advisories (loud on stdout + in the report, never gating): an unpinned
comparative acceptance-criterion, an LLR reading below Verified while every
citing TC is Verified (WI-129), a missing knowledge pack, and an interface
endpoint that resolves to no LLR Module. The report always carries the
attested-vs-mechanized Verified split (process.md §4 "Attest") and, when the SR
registry tags Area, a per-Area count.

Contracts: IF-001, IF-021, IF-042 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

# Sibling: the spine-row TEXT layer (WI-329). Run as a subprocess this script's
# own dir is sys.path[0] so a plain import resolves; the guard covers an
# in-process import (a test) whose sys.path does not yet carry scripts/ — the
# same sanctioned-sibling-import idiom agent_loop and gen_trajectory use.
try:
    from trace_text import (
        ac_advisories,
        form_findings,
        is_draft,
        is_example,
        paraphrase_advisories,
        provenance_findings,
        refs,
    )
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from trace_text import (
        ac_advisories,
        form_findings,
        is_draft,
        is_example,
        paraphrase_advisories,
        provenance_findings,
        refs,
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


def is_verified(row):
    """The terminal `Verified` state, matched case-insensitively so it follows the
    SAME rule as is_draft (the one Status-casing rule, process.md §4): both magic
    Status values are recognized in any case. Status is open-vocabulary; `Verified`
    is the value the G3 --require-verified criterion and the gate derivation act on.
    Duplicated in derive_gate.py per the F5 rule; pinned equal by test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "verified"


def is_modified(row):
    """The post-attestation `Modified` state (WI-316, process.md §7): the row
    landed `Verified` but its content changed after the last attestation, so a
    re-attest is owed — `Modified`→`Verified` blesses the amendment (existing
    evidence still verifies the amended text), `Modified`→`Planned` when the
    amendment invalidated the evidence. Recognized for SURFACING, not gate
    arithmetic: a Modified SR is simply not Verified, so `derive_gate.sr_gate`
    already reads it as decomposed-unverified G2 with no code of its own — this
    predicate exists for the `modified=N` basis count, the pending-owner-actions
    projection, the chain-consistency warns, and the `--ratify modified` brief.
    Same case-insensitive one-casing rule as the other two recognized values;
    duplicated in derive_gate.py per the F5 rule; pinned equal by test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "modified"


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
}

# The only *closed* vocabularies the method defines (process.md §4). Priority and
# Status are intentionally left open, so they are not validated here.
ENUM_FIELDS = {
    "SR": {
        "Verification": {
            "Test",
            "Demonstration",
            "Manual",
            "Analysis",
            "Inspection",
            "Attest",
            "Critique",
        }
    },
    "TC": {"Tier": {"Smoke", "Full", "Release"}},
}

# --- Acceptance-criteria testability advisory (warn-only) --------------------
# A comparative/absolute claim in an AcceptanceCriteria cell is untestable until
# it names its predicate: identical *in what*, judged *how*. (Gilbert's SR-013
# shipped "cannot distinguish source by schema" through G1 and had to be pinned
# by hand at G2.) Both lists are heuristics — the advisory WARNS and never joins
# a failure set; the G1 consistency review (process.md §4) makes the call.


def llr_status_advisories(llrs, tcs):
    """Warn-only findings (WI-129): an LLR whose Status reads below `Verified`
    while *every* TC that cites it is already `Verified`. The evidence to lift it
    exists, so the gap is a readout drift, not a coverage hole — mechanically
    harmless (the derived gate ignores LLR/TC Status past `Draft`; only the SR's
    `Verified` drives G2->G3, derive_gate.maturity_gate), but confusing at a
    ratification review, where an `Implemented` LLR under a `Verified` SR reads
    like an unfinished decomposition. Warn only: never promoted to an error (not
    under --strict or --strict-integrity), because making LLR status gate would
    re-introduce the exact LLR-status coupling the derived-gate model dropped.
    An LLR with no citing TC is the orphan rules' job, not this lint's; matching
    is case-insensitive via the shared is_verified() predicate. A `Modified` LLR
    is exempt (WI-316): its below-Verified status is DELIBERATE — a
    post-attestation amendment awaiting re-attest, not a readout drift — so the
    "lift to Verified" nag would tell the owner to erase the very marker the
    sitting needs."""
    citing = {}  # LLR id -> [is_verified(tc) for each citing TC]
    for r in tcs:
        tc_ok = is_verified(r)
        for x in refs(r.get("Verifies")):
            if ID_PATTERNS["LLR"].match(x):
                citing.setdefault(x, []).append(tc_ok)
    out = []
    for r in llrs:
        lid = r.get("LLR-ID")
        if not lid or is_verified(r) or is_modified(r):
            continue
        verdicts = citing.get(lid)
        if verdicts and all(verdicts):
            out.append(
                "LLR {} reads '{}' but every citing TC is Verified — lift to "
                "Verified (the evidence already exists)".format(
                    lid, (r.get("Status") or "").strip()
                )
            )
    return out


def modified_chain_advisories(srs, llrs, tcs):
    """Warn-only findings (WI-316): a `Modified` LLR/TC whose owning SR is neither
    `Modified` nor `Draft`. The SR is the ATTESTATION UNIT (process.md §7) — the
    re-attest sitting, the pending-owner-actions projection, and the
    `--ratify modified` brief all key off the SR row — so a chain amendment
    marked only on a child is INVISIBLE to every surface the marker exists to
    feed. Flip the owning SR (the amendment's real scope) or the child's flag is
    dead weight. Warn only, same tier as llr_status_advisories: never joins the
    exit code, even under --strict — a warn-tier checker feature mints no SR and
    gates nothing (WI-129/132). A TC's owning SRs resolve through both its
    direct `Verifies` SR cites and the SR-Refs of every LLR it cites."""
    sr_by_id = {r.get("SR-ID"): r for r in srs if r.get("SR-ID")}
    llr_srs = {}  # LLR id -> [owning SR ids]
    for r in llrs:
        lid = r.get("LLR-ID")
        if lid:
            llr_srs[lid] = [x for x in refs(r.get("SR-Refs")) if x in sr_by_id]

    def _flagged(sr_ids):
        return any(
            is_modified(sr_by_id[s]) or is_draft(sr_by_id[s])
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
                "LLR {} is Modified but its owning SR ({}) is not Modified/Draft "
                "— flip the attestation unit (the SR) or the amendment is "
                "invisible to the re-attest sitting".format(lid, ";".join(owners))
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
                "TC {} is Modified but its owning SR ({}) is not Modified/Draft "
                "— flip the attestation unit (the SR) or the amendment is "
                "invisible to the re-attest sitting".format(
                    tid, ";".join(sorted(set(owners)))
                )
            )
    return out


# Verification methods whose "Verified" state rests on a recorded human judgment,
# not a runnable check (process.md §4 "Attest"). --require-verified accepts these
# as legitimately Verified but the report surfaces them distinctly (the
# verification-basis split), so an audit can always see how much rests on trust.
ATTESTED_METHODS = {"Attest"}
# The one method whose "Verified" rests on a runnable, re-executable check
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


def _supersession_targets(row, ids):
    """Return one row's validated targets plus its local findings."""
    sid = row.get("SR-ID")
    value = (row.get("SupersededBy") or "").strip()
    if not sid or not value:
        return [], []
    targets = [target.strip() for target in value.split(";")]
    malformed = any(not target for target in targets) or any(
        "," in target or any(ch.isspace() for ch in target) for target in targets
    )
    if malformed:
        return [], [f"SR {sid} SupersededBy must be a semicolon-separated SR-id list"]
    found = []
    for target in set(targets):
        if targets.count(target) > 1:
            found.append(f"SR {sid} SupersededBy repeats {target}")
        if not ID_PATTERNS["SR"].match(target) or target not in ids:
            found.append(f"SR {sid} SupersededBy references unknown {target}")
        elif target == sid:
            found.append(f"SR {sid} SupersededBy self-links")
    return targets, found


def _supersession_cycle_findings(edges):
    # Report one deterministic finding per cyclic component. A DFS path is
    # enough because supersession targets outside the linking subset are leaves.
    state = {}
    stack = []
    reported = set()
    found = []

    def visit(node):
        state[node] = 1
        stack.append(node)
        for target in edges.get(node, []):
            if target not in edges:
                continue
            if state.get(target, 0) == 0:
                visit(target)
            elif state.get(target) == 1:
                start = stack.index(target)
                cycle = stack[start:] + [target]
                key = frozenset(cycle)
                if key not in reported:
                    reported.add(key)
                    found.append("SR SupersededBy cycle: " + " -> ".join(cycle))
        stack.pop()
        state[node] = 2

    for sid in sorted(edges):
        if state.get(sid, 0) == 0:
            visit(sid)
    return found


def _llr_supersession_findings(llrs, superseded, ids):
    # Scoped to LLR SR-Refs on purpose: a TC citing a superseded SR is legal and
    # required — a non-draft superseded SR still owes a TC (see LLR_EXEMPT), and
    # that TC is the retained evidence record proving nothing live hangs on the
    # dead scope. Only a decomposition grounds new work on the dead id.
    # A Draft LLR is NOT exempt: grounding on a dead SR is wrong at any stage,
    # not a maturity question — the same tier as a duplicated id.
    found = []
    for row in llrs:
        lid = row.get("LLR-ID")
        if not lid:
            continue
        for sid in sorted(set(refs(row.get("SR-Refs")))):
            if sid in superseded:
                # Name only successors that exist — an unknown target already
                # has its own SR-side finding, and pointing the reader at a
                # nonexistent successor would compound the error.
                real = [t for t in superseded[sid] if t in ids]
                where = (
                    "SupersededBy " + ";".join(real)
                    if real
                    else "SupersededBy names no existing successor"
                )
                found.append(
                    f"LLR {lid} SR-Refs cites superseded {sid} ({where}) — "
                    "re-ground on the successor or delete the LLR"
                )
    return found


def sr_supersession_findings(srs, llrs=()):
    """Validate the optional SR ``SupersededBy`` extension.

    A populated cell is a semicolon-separated list of other, existing SR ids.
    Supersession is identity history rather than decomposition, so malformed
    targets, self-links, and cycles are always-invalid integrity findings.
    An LLR whose ``SR-Refs`` cites an SR with a populated cell is the same
    class of error (WI-364, owner ruling 2026-07-29): the registry is the live
    surface and the supersession history lives in git, so a live decomposition
    must re-ground on the successor or be deleted. TC citations of a superseded
    SR stay legal — they are the retained evidence record.
    Registries without the optional column remain byte-for-byte compatible.
    """
    ids = {r.get("SR-ID") for r in srs if r.get("SR-ID")}
    edges = {}
    found = []
    for row in srs:
        targets, row_findings = _supersession_targets(row, ids)
        found.extend(row_findings)
        if targets:
            edges[row["SR-ID"]] = targets
    return (
        found
        + _supersession_cycle_findings(edges)
        + _llr_supersession_findings(llrs, edges, ids)
    )


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


# Source-file extensions stripped when normalizing a module path so the two
# module-naming conventions in play align: an LLR `Module` cell carries the full
# repo path with extension (`project-trajectory/scripts/check.py`) while the
# arch-map / an IF `ThisProject` endpoint may use the shorter map form
# (`scripts/check`). Normalization strips a leading `project-trajectory/` segment
# and any one of these tails so both collapse to the same key.
_MODULE_EXTS = (".py", ".sh", ".ps1", ".ts", ".js", ".go", ".rs", ".cmd")


def _norm_module(path):
    """A module path reduced to a naming-convention-neutral key (see _MODULE_EXTS):
    strip a leading `project-trajectory/`, any source extension, and `/__init__`."""
    p = (path or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/") :]
    for ext in _MODULE_EXTS:
        if p.endswith(ext):
            p = p[: -len(ext)]
            break
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p


def interface_findings(ifs, sr_ids, module_ids):
    """The IF-### seam tier's back-link checks (process.md §8), closing the gap
    where trace.py never read the interface catalog (WI-056). Returns
    ``(findings, advisories)``: *findings* join the --strict failure set like PB's
    back-links (an IF row's SR-Refs is empty or names an unknown SR — every seam
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
        srrefs = refs(r.get("SR-Refs"))
        if not srrefs:
            findings.append(f"IF {iid} links no SR (SR-Refs is empty)")
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
    """Sorted unique '-000' SN ids still present in stakeholder-needs.md (if it exists)."""
    if not sn_md.exists():
        return []
    text = sn_md.read_text(encoding="utf-8-sig", errors="replace")
    return sorted({u for u in re.findall(r"\bSN-\d+\b", text) if is_example(u)})


# SN maturity lives in section-as-state (derived-gate model §4a): a stakeholder-
# needs.md heading whose text contains "draft" (case-insensitive, e.g. `## Draft
# needs (unratified)`) marks the SNs under it as Draft (unratified, G0); SNs under
# any other heading are ratified (G1). No new column — the state IS the section,
# and the ratification date is git-derived (the commit that moved the row out of
# the draft section). This is the SN analogue of the `Status=Draft` bit on
# SR/LLR/TC rows.
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)")


def sn_all_ids(text):
    """The SN id UNIVERSE: every `SN-###` token anywhere in stakeholder-needs.md
    `text`, whole-text — a prose mention counts exactly like a table row, which
    is the sharp edge registry-machinery-reference §2.1 records (ratified +
    uncited caps the derived gate at G0 since WI-401). `-000` placeholders
    excluded. Duplicated in derive_gate.py per the F5 rule; pinned equal by
    test_rule_sync (WI-408), because this scrape decides which ids BOTH
    surfaces run their rules over."""
    return {u for u in re.findall(r"\bSN-\d+\b", text) if not is_example(u)}


def sn_draft_ids(text):
    """The set of Draft SN ids in stakeholder-needs.md `text` (section-as-state):
    every SN-### that appears under a heading whose text contains "draft". `-000`
    placeholders are excluded. Line-scanned, tracking the current heading — an SN
    under a draft heading is Draft until the next heading changes the section."""
    draft, in_draft = set(), False
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            in_draft = "draft" in m.group(1).lower()
            continue
        if in_draft:
            for u in re.findall(r"\bSN-\d+\b", line):
                if not is_example(u):
                    draft.add(u)
    return draft


def sn_cited_ids(srs):
    """Every SN id cited by >=1 SR row's `SN-Refs` cell — the coverage set the
    "SN has no SR" orphan rule reads (and, since WI-401, the gate input behind
    derive_gate.py's SN-coverage rung: that rung caps the raw level, this
    listing itemizes the ids at G2 strictness). No filtering here: -000 rows
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


def phase_ratified_findings(real):
    """The ratified-phase NUMERIC-ONLY rule (process.md §4 "Phased delivery"; owner
    ruling 2026-08-01, WI-402): once the project phases ANY spine row (digit-parse
    arming — a legacy `v2` cell arms it too), every RATIFIED (non-Draft) SR/LLR/TC
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
    so a fully-blank downstream registry stays green (a `Draft` row may always
    leave `Phase` blank). SN is covered transitively: at G1+ every ratified SN
    has >=1 SR (the orphan rule) and SRs are phased; pre-G1 it is vacuously
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
            if is_draft(r) or re.fullmatch(r"[0-9]+", cell):
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
    """A node's view class: orphan (a trace finding) outranks draft (a status)."""
    if rid in orphan_ids:
        return "orphan"
    if status.lower() == "draft":
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
    `sn_draft` (section-as-state, §4a) labels those SNs `Draft` so the views flag
    them like a `Status=Draft` SR/LLR/TC row."""
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
        roots.append(_node(sn, "Draft" if sn in sn_draft else "", "", orphan_ids, kids))
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
# Method/Expected, and any rubric it cites) so a G1/G2 ratification brief can
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


def _scope_srs(scope, srs):
    """Resolve a `--ratify` scope to an ordered SR-row list. The scope is either a
    comma/space list of `SR-###` ids (used verbatim) or one-or-more phase tags
    (every SR whose `Phase` cell is one of them). Detection: if *any* token looks
    like an SR id the whole scope is treated as ids, else as phases."""
    tokens = refs(scope)
    as_ids = any(re.fullmatch(r"SR-\d+", t, re.IGNORECASE) for t in tokens)
    if as_ids:
        want = {t.upper() for t in tokens}
        return [s for s in srs if s.get("SR-ID", "").upper() in want]
    phases = {t.lower() for t in tokens}
    return [s for s in srs if _cell(s, "Phase").lower() in phases]


def _sn_fields(cells):
    """The four prose fields of one SN row, resolved BY TABLE SHAPE.

    `stakeholder-needs.md` carries two row widths, and reading both at the same
    fixed offsets is what garbled the edge-case tier for its whole life:

    - Core / Draft needs — `Need | Why it matters | Priority | Acceptance intent`
    - Edge-case expectations — `Lifecycle | Scenario | Expected behavior`, three
      cells and NO priority.

    Indexed at the core offsets, an edge-case row yielded `need` = the Lifecycle
    word (SN-013 rendered as "Provision") and `acceptance` = empty, in every
    generated surface. So the edge-case row maps by MEANING instead: its Scenario
    is the need, its Lifecycle is why it matters, its Expected behavior is the
    acceptance intent, and `priority` is the literal `n/a` — the table declares
    none, and inventing one would put a value in the export that no author wrote.

    Widths above the core shape take the core mapping: it is the common form, and
    a wider row means a stray `|` in a cell rather than a third table.

    Duplicated verbatim in gen_okf.sn_rows and trace._sn_prose (F5) — change all
    three together; tests/test_rule_sync.py pins them equal AND pins the values.
    """
    if len(cells) > 4:
        return {
            "need": cells[0],
            "why": cells[1],
            "priority": cells[2],
            "acceptance": cells[3],
        }
    return {
        "need": cells[1] if len(cells) > 1 else "",
        "why": cells[0] if cells else "",
        "priority": "n/a",
        "acceptance": cells[2] if len(cells) > 2 else "",
    }


def _sn_prose(sn_text):
    """Parse each SN row's prose (Need / Why it matters / Acceptance intent) from
    stakeholder-needs.md so the ratify view renders the *top* of the chain, not a
    bare SN id (WI-146 REVIEW-A). Mirrors gen_okf.sn_rows / traj_parse._sn_rows
    via the duplicated `_sn_fields` mapping; example `-000` rows are skipped.
    Change all three together if the SN table columns move."""
    meta = {}
    for line in sn_text.splitlines():
        m = re.match(r"\|\s*(SN-\d+)\s*\|(.*)", line)
        if not m or m.group(1).endswith("-000"):
            continue
        cells = [re.sub(r"\*\*|`", "", c).strip() for c in m.group(2).split("|")]
        meta[m.group(1)] = _sn_fields(cells)
    return meta


# --- the re-attestation brief (--ratify modified, WI-316) ----------------------
# A sitting cannot bless a delta it cannot see: for each `Modified` SR the brief
# shows every chain row's changed cells as BEFORE (the row at the attested
# baseline revision) vs AFTER (the working tree). The baseline is git-derived —
# the newest commit at which the SR row read `Verified` — which is correct under
# the amend+flip-same-commit regime the staged warn enforces; `--since REV`
# overrides it for pre-regime streaks (amendments that landed while the row
# stayed Verified, e.g. the WI-316 backfill batch). Git archaeology lives HERE,
# on demand, never in the pending projection (pointer-only per its charter).

SPINE_FILES = (
    ("docs/requirements/system-requirements.csv", "SR-ID"),
    ("docs/requirements/low-level-requirements.csv", "LLR-ID"),
    ("docs/test/test-cases.csv", "TC-ID"),
)


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


def _rows_at(root, rev, rel_path, id_col):
    """{id: row} of a registry CSV at `rev` (`git show`, csv-parsed — spine cells
    are long, never line-split; -000 example rows dropped). {} when the file does
    not exist at that revision (nothing existed = an empty baseline)."""
    text = _git_out(root, ["show", "{}:{}".format(rev, rel_path)])
    if text is None:
        return {}
    # Adversarial-review F4: `git show` preserves a committed BOM, and a BOM'd
    # header glues to the first column name so every row hides — the same
    # hazard trace's own loaders read utf-8-sig for. Strip it before parsing.
    text = text.lstrip("﻿")
    return {
        r[id_col]: r
        for r in csv.DictReader(io.StringIO(text))
        if r.get(id_col) and not r[id_col].endswith("-000")
    }


def _attested_baseline(root, sr_id):
    """The commit whose text `sr_id` was last attested against — DERIVED: the
    newest commit at which the SR row read `Verified`.

    THE DERIVATION IS ONCE AGAIN THE ONLY PATH (docs/repo-lock.md D-1). SN-029
    put a read of `attestations.csv` in front of this walk, so an anchor written
    at acceptance time won over a reconstruction. That ledger is retired and its
    replacement — the anchor recorded on the SR's OWN ROW — waits on the carrier
    ruling (OI-12), so the ledger-first arm is removed rather than left pointing
    at a file that no longer exists. Nothing regresses: the ledger never held a
    row, so this walk is what every caller has actually been getting.

    The walk's known blind spot is unchanged and is why the anchor is owed at
    all: it is correct by construction ONLY while every amendment flips its
    row's Status in the same commit, and the SANCTIONED amend+flip path is
    precisely the one `check_trajectory.staged_spine_amendments` deliberately
    ignores. Callers that need to say so have `no_baseline_reason`.

    Walks the SR registry's commits newest-first; bounded in practice by the
    streak depth (typically 1-2 revisions). None: off-git, or the row was never
    Verified in committed history (first attestation still pending)."""
    log = _git_out(root, ["log", "--format=%H", "--", SPINE_FILES[0][0]])
    if log is None:
        return None
    for rev in log.split():
        row = _rows_at(root, rev, SPINE_FILES[0][0], SPINE_FILES[0][1]).get(sr_id)
        if row is not None and is_verified(row):
            return rev
    return None


def _changed_cells(before, after):
    """(cell, before, after) triples for every differing cell, in column order —
    EXCEPT the `Verified`→`Modified` Status flip itself: the marker is not the
    amendment, and listing it would bury the real delta under N identical lines.
    Every other Status movement (a supersession, the →Planned evidence
    downgrade) is a real change and shows."""
    before = before or {}
    after = after or {}
    keys = list(dict.fromkeys(list(after) + list(before)))
    out = []
    for k in keys:
        b = (before.get(k) or "").strip()
        a = (after.get(k) or "").strip()
        if b == a:
            continue
        if k == "Status" and b.lower() == "verified" and a.lower() == "modified":
            continue
        out.append((k, b, a))
    return out


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


def _cell_diff_lines(changed):
    lines = []
    for cell, b, a in changed:
        lines.append("- **{}**".format(cell))
        lines.append("  - before: {}".format(b or "(empty)"))
        lines.append("  - after: {}".format(a or "(empty)"))
    return lines


def reattest_model(root, srs, llrs, tcs, since=None, statuses=("modified",)):
    """The STRUCTURED attestation model: one entry per SR owing an attestation,
    with its baseline, its chain rows, and each row's changed cells.

    Split out of `reattest_lines` (WI-322) so the computation runs ONCE and two
    renderers consume it — the markdown brief here, and the generated
    `open-items.html` owner view in `gen_open_items.py`. Duplicating the git
    archaeology in a second module is exactly the paraphrase-not-decompose
    failure the kit preaches against; the seam is this function.

    `statuses` selects which rows owe an attestation: `("modified",)` is the
    re-attest brief's scope (a post-attestation amendment), `("draft",)` is a
    first ratification, and both together is what the owner view renders — "new
    or changed requirement rows awaiting a human". A `draft` SR has no attested
    baseline BY DEFINITION, so its entry carries `baseline=None` and its rows
    carry full current content rather than a diff; that is the same honest
    degrade path an off-git repo takes, not a special case.

    Returns `[{id, title, kind, baseline, baseline_date, from_since,
    no_baseline_reason, rows:[{kind, id, state, cells, full}]}]` where `state`
    is `changed` | `added` | `removed` | `current`, `cells` is the
    `(name, before, after)` triples, and `full` is the row dict for the states
    that render whole rows. Deterministic given HEAD + the working tree."""
    wanted = tuple(s.strip().lower() for s in statuses)

    def owes(row):
        state = (row.get("Status") or "").strip().lower()
        return state in wanted

    pending_srs = sorted((r for r in srs if owes(r)), key=lambda r: r.get("SR-ID", ""))
    if not pending_srs:
        return []
    git_ok = _git_out(root, ["rev-parse", "HEAD"]) is not None
    if since:
        resolved = _git_out(root, ["rev-parse", "--verify", since + "^{commit}"])
        if resolved is None:
            raise SystemExit(
                "trace: --since {!r} does not resolve to a commit in this "
                "repository — refusing to render a brief against a fabricated "
                "baseline".format(since)
            )
        since = resolved.strip()
    base_cache = {}

    def rows_at_cached(rev, rel_path, id_col):
        per_rev = base_cache.setdefault(rev, {})
        if rel_path not in per_rev:
            per_rev[rel_path] = _rows_at(root, rev, rel_path, id_col)
        return per_rev[rel_path]

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

    model = []
    for sr in pending_srs:
        sid = sr.get("SR-ID", "")
        state = (sr.get("Status") or "").strip().lower()
        entry = {
            "id": sid,
            "title": (sr.get("Title") or "").strip(),
            "kind": "ratify" if state == "draft" else "reattest",
            "baseline": None,
            "baseline_date": "",
            "from_since": bool(since),
            "no_baseline_reason": "",
            "rows": [],
        }
        current_chain = chain_of(sid, srs, llrs_by_sr, tcs_by_ref)
        # A Draft row has never been attested, so there is no baseline to diff
        # against — asking git for one would be a category error, not a miss.
        baseline = None
        if state != "draft":
            baseline = (
                since if since else (_attested_baseline(root, sid) if git_ok else None)
            )
        if baseline is None:
            entry["no_baseline_reason"] = (
                "awaiting its FIRST ratification — no attested baseline exists"
                if state == "draft"
                else (
                    "no git history available"
                    if not git_ok
                    else "the row was never `Verified` in committed history"
                    " (first attestation pending)"
                )
            )
            entry["rows"] = [
                {"kind": k, "id": i, "state": "current", "cells": [], "full": r}
                for k, i, r in current_chain
            ]
            model.append(entry)
            continue
        entry["baseline"] = baseline
        entry["baseline_date"] = (
            _git_out(root, ["show", "-s", "--format=%cs", baseline]) or ""
        ).strip()
        base_srs = list(rows_at_cached(baseline, *SPINE_FILES[0]).values())
        base_llrs = list(rows_at_cached(baseline, *SPINE_FILES[1]).values())
        base_tcs = list(rows_at_cached(baseline, *SPINE_FILES[2]).values())
        base_chain = chain_of(
            sid,
            base_srs,
            _bucket_by_ref(base_llrs, "SR-Refs"),
            _bucket_by_ref(base_tcs, "Verifies"),
        )
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
                        "full": row,
                    }
                )
                continue
            changed = _changed_cells(before, row)
            if changed:
                entry["rows"].append(
                    {
                        "kind": kind,
                        "id": rid,
                        "state": "changed",
                        "cells": changed,
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
# THE CONSTRAINT THAT MAKES THIS HARDER THAN ITS SIBLINGS: the brief SELF-STAMPS
# its baseline and reuses it, so `--check` must compare against the baseline the
# FILE declares and must NOT re-derive one. Re-deriving is precisely the WI-322
# review BLOCKER — a regeneration that silently collapsed 43 chain-row diffs to 18
# while `--check` certified the loss. A gate that re-derives its own expectation
# cannot detect the drift it exists to detect.
_DECLARED_BASELINE_RE = re.compile(
    r"^_Baseline `([0-9a-fA-F]+)`[^\n]*?— from `--since`\._$", re.M
)


def declared_since(text):
    """The `--since` revision a brief declares, or None when it derived its own.

    Only a brief written WITH `--since` pins a baseline that a re-derivation
    could move; without it each section is baselined at the git-derived
    last-Verified revision of its own SR, which is a function of history and is
    stable as long as history is. So None means "let the renderer derive", not
    "no baseline".

    More than one distinct `--since` revision cannot come from one run, so it
    means the file has been hand-edited or spliced: returned as a finding rather
    than resolved, because guessing which one is current is exactly the silent
    substitution this whole check exists to prevent."""
    revs = {m.group(1) for m in _DECLARED_BASELINE_RE.finditer(text)}
    if len(revs) > 1:
        return sorted(revs)  # a list signals "ambiguous" to the caller
    return revs.pop() if revs else None


def ratify_check(root, srs, llrs, tcs, out_path, since=None):
    """`(code, message)` for `--ratify modified --check`.

    Fails CLOSED on a difference — a stale brief is read by a human about to
    attest, and the cost of a false green here is an owner blessing rows they
    were never shown.

    Two silences, both the arming idiom the component checks use rather than
    exceptions carved for this repo:

      - **no file at `--out`** — a project with no `docs/ratify/` pays nothing;
      - **no `Modified` SR** — the window is CLOSED, so nothing owes a re-attest
        and the committed brief is a historical record of a finished sitting, not
        a surface that can go stale. Checking it against a registry whose rows
        have since been blessed would fail forever, which is how a check earns
        its own ignore.
    """
    if not out_path.exists():
        return 0, "no brief at {} — nothing to gate".format(out_path)
    if not any(is_modified(r) for r in srs):
        return 0, "no `Modified` SR — the re-attest window is closed"
    try:
        with out_path.open("r", encoding="utf-8", newline="") as fh:
            existing = fh.read()
    except OSError as exc:
        return 1, "cannot read {}: {}".format(out_path, exc)

    baseline = since or declared_since(existing)
    if isinstance(baseline, list):
        return 1, (
            "{} declares {} different `--since` baselines ({}) — one run cannot "
            "produce that, so the file has been hand-edited; regenerate it".format(
                out_path, len(baseline), ", ".join(baseline)
            )
        )
    rendered = "\n".join(reattest_lines(root, srs, llrs, tcs, since=baseline)) + "\n"
    if rendered == existing:
        return 0, "{} is current (baseline {})".format(
            out_path, baseline or "git-derived"
        )
    return 1, (
        "{} is STALE against the registry (compared at the baseline the file "
        "itself declares{}, never a re-derived one). Regenerate it with "
        "`trace.py --ratify modified{} --out {}` and re-read it BEFORE "
        "attesting — an owner blessing a short brief blesses rows they were "
        "never shown.".format(
            out_path,
            ": " + baseline if baseline else "",
            " --since " + baseline if baseline else "",
            out_path,
        )
    )


def reattest_lines(root, srs, llrs, tcs, since=None):
    """Markdown for the re-attestation brief (`--ratify modified`, WI-316): one
    section per `Modified` SR — the attestation unit — with per-cell
    before/after for every chain row (the SR + its LLRs + their/its TCs) that
    changed since the attested baseline, plus rows ADDED to or REMOVED from the
    chain. Baseline = `--since` when given, else the git-derived newest
    still-Verified revision of the SR row. Off-git (or a never-Verified row) it
    degrades honestly: current state only, with a stated no-before note.
    Deterministic given HEAD + the working tree; a generator mode like
    ratify_lines — runs no checks.

    The markdown RENDERER over `reattest_model` (WI-322): the model owns the git
    archaeology and the cell comparison, this owns the prose."""
    lines = [
        "# Re-attestation brief — `Modified` spine rows",
        "",
        "_Generated by `trace.py --ratify modified` (WI-316). One section per"
        " `Modified` SR (the attestation unit); each chain row shows only its"
        " CHANGED cells, before (the attested baseline revision) vs after (the"
        " working tree). The `Verified`→`Modified` Status flip itself is not"
        " listed — the marker is not the amendment. Baseline: `--since` when"
        " given, else the newest revision where the SR row still read"
        " `Verified` (correct under the amend+flip-same-commit rule the staged"
        " warn enforces — use `--since` for a pre-regime streak). Rule on each"
        " section: bless → `Verified`; evidence no longer verifies the amended"
        " text → `Planned` (process.md §7)._",
        "",
    ]
    if not any(is_modified(r) for r in srs):
        lines.append("_No `Modified` SR — nothing owes a re-attest._")
        return lines
    for entry in reattest_model(root, srs, llrs, tcs, since, statuses=("modified",)):
        sid, title = entry["id"], entry["title"]
        lines += ["", "## {} — {}".format(sid, title or "(untitled)"), ""]
        if entry["baseline"] is None:
            lines.append(
                "_No attested baseline — {}; current state only._".format(
                    entry["no_baseline_reason"]
                )
            )
            for row in entry["rows"]:
                lines += ["", "### {} {} (current)".format(row["kind"], row["id"])]
                lines += _full_row_bullets(row)
            continue
        lines.append(
            "_Baseline `{}`{}{}._".format(
                entry["baseline"][:9],
                " ({})".format(entry["baseline_date"])
                if entry["baseline_date"]
                else "",
                " — from `--since`"
                if entry["from_since"]
                else " — newest revision where {} read `Verified`".format(sid),
            )
        )
        for row in entry["rows"]:
            if row["state"] == "added":
                lines += [
                    "",
                    "### {} {} — ADDED since baseline".format(row["kind"], row["id"]),
                ]
                lines += _full_row_bullets(row)
            elif row["state"] == "changed":
                lines += ["", "### {} {}".format(row["kind"], row["id"])]
                lines += _cell_diff_lines(row["cells"])
            elif row["state"] == "removed":
                lines += [
                    "",
                    "### {} {} — REMOVED since baseline".format(row["kind"], row["id"]),
                    "_In this SR's chain at the baseline, out of it in the working"
                    " tree — the row was deleted, re-parented, or superseded"
                    " (a superseded row keeps existing; it leaves the chain)._",
                ]
        if not entry["rows"]:
            lines.append(
                "_No cell differs from the baseline beyond the Status flip —"
                " if that is unexpected, the streak may predate the regime;"
                " re-run with `--since <rev>`._"
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
    raw_srs = load_csv(docs / "requirements" / "system-requirements.csv")
    raw_llrs = load_csv(docs / "requirements" / "low-level-requirements.csv")
    raw_tcs = load_csv(docs / "test" / "test-cases.csv")
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
    raw_cmps = load_csv(docs / "requirements" / "components.csv")
    # Optional interface-seam registry (IF-###, process.md §8): one row per
    # directed seam (ThisProject module -> Counterpart module/file/external). Off
    # the joined spine like PART/ASSET, but its SR-Refs back-link and its endpoint
    # join keep it traceable (WI-056 closed the SR-002-era gap). Absent file -> [].
    raw_ifs = load_csv(docs / "requirements" / "interfaces.csv")

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

    sn_ids = set()
    sn_draft = set()
    sn_meta = {}
    sn_integrity = []
    sn_md = docs / "requirements" / "stakeholder-needs.md"
    if sn_md.exists():
        # utf-8-sig + replace: a BOM must not glue to line 1 (defeating the
        # heading regexes) and one stray cp1252 byte must degrade, not crash
        # the gate chain (the C8 convention, applied to content reads too).
        sn_text = sn_md.read_text(encoding="utf-8-sig", errors="replace")
        sn_ids = sn_all_ids(sn_text)
        # Section-as-state maturity (derived-gate §4a): SNs under a "draft" heading
        # are unratified (G0) and exempt from the "SN with no SR" child rule below.
        sn_draft = sn_draft_ids(sn_text)
        sn_meta = _sn_prose(sn_text)
        sn_integrity = sn_integrity_findings(sn_text)
    reg = Registries()
    reg.raw_srs, reg.raw_llrs, reg.raw_tcs = raw_srs, raw_llrs, raw_tcs
    reg.raw_pbs, reg.raw_repos, reg.raw_mods = raw_pbs, raw_repos, raw_mods
    reg.raw_parts, reg.raw_assets = raw_parts, raw_assets
    reg.raw_cmps, reg.raw_ifs = raw_cmps, raw_ifs
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
        # A Draft SR is being drafted requirement-first (derived-gate model §3):
        # exempt from the child-completeness rules (no LLR / no TC) so it lives in
        # the live spine without orphaning. Its SN linkage and every integrity
        # rule still apply.
        draft = is_draft(r)
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
        # G1's "every SR links >=1 SN", machine-checked — but only when the SN
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
        # A Draft LLR is exempt from the child-completeness (no TC) rule, like a
        # Draft SR — its SR parent + id integrity still apply (derived-gate §3).
        if not is_draft(r) and lid not in tc_refs:
            orphans.append(f"LLR {lid} has no test (TC)")
            orphan_ids.add(lid)

    for tid, finding in tc_citation_findings(tcs, sr_ids | llr_ids, ifs):
        orphans.append(finding)
        orphan_ids.add(tid)

    for u in sorted(sn_ids):
        # A Draft SN (section-as-state, §4a) is being drafted requirement-first and
        # is exempt from the child-completeness rule, like a Draft SR. The gate
        # half of this rule is derive_gate's SN-coverage rung (WI-401): same
        # cited set (sn_cited_ids), same Draft exemption — this lists the ids,
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

    # Interface seams (IF-###, process.md §8): SR-Refs back-links join the
    # --strict failure set like PB's; the ThisProject-vs-LLR-Module endpoint join
    # is a warn-only advisory (module_ids reused from the PB back-link check above).
    interface_backlink_findings, interface_advisories = interface_findings(
        ifs, sr_ids, module_ids
    )

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
    # reports Verified, how was each reached? Three kinds, most-to-least runnable —
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
        if not is_verified(r):
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
            # The G3 status bar applies to every ratified SR regardless of
            # Verification method — matching derive_gate.sr_gate, which already
            # demands is_verified for any decomposed SR before G3 with no
            # per-method carve-out (WI-259, review-2026-07-21 M-5: a Demonstration/
            # Analysis/Inspection SR left Implemented can never derive G3 yet used
            # to pass this Test-only check — the two scripts disagreeing about the
            # gate is the false-green the kit exists to prevent). A Draft SR is
            # pre-ratification (below G1, derived-gate §3): it makes no Verified
            # claim yet, so the bar stands down — surfaced in the draft count so
            # the exemption stays auditable. Pinned equivalent to sr_gate's
            # is_verified-for-decomposed rule by test_rule_sync.
            if is_draft(r):
                continue
            if not in_phase(r):
                phase_deferred.append(
                    f"SR {r['SR-ID']} (Phase={r.get('Phase', '').strip()}) — "
                    "status check deferred to its own phase"
                )
                continue
            if not is_verified(r):
                val = (r.get("Status") or "").strip()
                method = (r.get("Verification") or "").strip() or "(blank)"
                status_findings.append(
                    f"SR {r['SR-ID']} is Verification={method} but Status="
                    f"{val or '(blank)'} (G3 requires Verified for every ratified "
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
    # The SN tier's duplicate protection (prose registry — see
    # sn_integrity_findings): integrity-class like a duplicated CSV id.
    integrity += getattr(reg, "sn_integrity", [])
    integrity += sr_supersession_findings(srs, llrs)
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
    # SR-Refs back-link and endpoint join are checked below.
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
    # Warn-only, always on (WI-129): an LLR reading below Verified while every
    # citing TC is Verified — a readout drift, never a failure (LLR status is
    # non-gating under the derived-gate model). Never joins a failure set below.
    llr_status_advis = llr_status_advisories(llrs, tcs)
    # Warn-only, always on (WI-316): a Modified LLR/TC whose owning SR is not
    # flagged — the amendment is invisible to the re-attest surfaces, which all
    # key off the SR row. Same never-gating tier as the status-coherence lint;
    # rendered through the same channel (one advisory pipe, two lints).
    llr_status_advis = llr_status_advis + modified_chain_advisories(srs, llrs, tcs)

    # Draft artifacts (derived-gate model §3): the rows exempted from the
    # child-completeness orphan rules + the --require-verified criterion. Listed
    # so the exemption stays auditable (the whole point of the model is that a
    # Draft row lives in the live spine while being drafted, not silently).
    draft_srs = [r for r in srs if is_draft(r)]
    draft_llrs = [r for r in llrs if is_draft(r)]
    draft_tcs = [r for r in tcs if is_draft(r)]
    n_draft = len(draft_srs) + len(draft_llrs) + len(draft_tcs) + len(sn_draft)

    # Optional Area column (owner-hat/domain tag, process.md §1): count real SRs
    # per Area so hat coverage is visible. Report-only — never a finding, never
    # an exit-code change; a registry without the column contributes nothing.
    area_counts = {}
    for r in srs:
        area = (r.get("Area") or "").strip()
        if area:
            area_counts[area] = area_counts.get(area, 0) + 1
    findings = Findings()
    findings.orphans = orphans
    findings.orphan_ids = orphan_ids
    findings.integrity = integrity
    findings.placeholders = placeholders
    findings.schema = schema
    findings.advisories = advisories
    findings.provenance = provenance
    findings.form = form
    findings.paraphrase = paraphrase
    findings.llr_status_advis = llr_status_advis
    findings.budget_findings = budget_findings
    findings.module_findings = module_findings
    findings.component_findings = component_findings
    findings.knowledge_advisories = knowledge_advisories
    findings.interface_backlink_findings = interface_backlink_findings
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
    budget_findings = findings.budget_findings
    module_findings = findings.module_findings
    component_findings = findings.component_findings
    knowledge_advisories = findings.knowledge_advisories
    interface_backlink_findings = findings.interface_backlink_findings
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
            f"| Verified SRs — mechanized (Test) | {len(mechanized_verified)} |",
            f"| Verified SRs — demonstrated/observed | {len(demonstrated_verified)} |",
            f"| Verified SRs — attested (human, §4) | {len(attested_verified)} |",
        ]
        + (
            [f"| Draft artifacts (decomposition-exempt) | {n_draft} |"]
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
    # criteria wording that names no predicate. The G1 consistency review
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
    # below Verified whose citing TCs are all Verified (lift the Status cell by
    # hand — registries are hand-owned SSOT, no generator writes them back), and
    # Modified LLR/TC rows whose owning SR is not flagged (flip the attestation
    # unit or the amendment is invisible to the re-attest sitting).
    lines += ["", "## Status-coherence advisories (warn-only)", ""]
    lines += (
        ["None. No unlifted LLRs, no orphaned Modified chain rows."]
        if not llr_status_advis
        else [f"- {f}" for f in llr_status_advis]
    )
    # Verification-basis surface (process.md §4): make the project's trust
    # footprint auditable — of what is "Verified", how much rests on a runnable
    # check (Test), on a human observing an outcome (Demonstration/Manual/Analysis/
    # Inspection/Critique), or on a named human's recorded judgment (Attest)? Split
    # three ways (WI-259) so non-Test Verified claims are never folded into
    # "mechanized"; the demonstrated and attested ids are listed so an audit can
    # see exactly which rows rest on something other than a runnable check.
    lines += ["", "## Verification basis (mechanized / demonstrated / attested)", ""]
    lines += [
        "_Of the SRs reported `Verified`: `Test` rows rest on a runnable, "
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
        lines += ["", "## Draft artifacts (decomposition-exempt)", ""]
        lines += [
            "_`Draft` rows are exempt from the child-completeness orphan rules and "
            "the G3 Verified criterion (derived-gate model §3): a requirement lives "
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
            "## SRs by Area (report-only)",
            "",
            "_Optional owner-hat/domain tag (process.md §1). Counts only — "
            "never a gate; blank cells are simply untagged._",
            "",
        ]
        lines += [f"- {a}: {n}" for a, n in sorted(area_counts.items())]
        if untagged:
            lines.append(f"- (no Area): {untagged}")
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
            [f"{len(ifs)} interface-seam row(s); every SR-Refs resolves to a real SR."]
            if not interface_backlink_findings
            else [f"- {f}" for f in interface_backlink_findings]
        )
        if interface_advisories:
            lines += ["", "### Interface endpoint advisories (warn-only)", ""]
            lines += [f"- {a}" for a in interface_advisories]
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
            ["None. Every in-scope ratified SR is Verified (any method)."]
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
    orphans = findings.orphans
    integrity = findings.integrity
    advisories = findings.advisories
    provenance = findings.provenance
    form = findings.form
    paraphrase = findings.paraphrase
    interface_advisories = findings.interface_advisories
    knowledge_advisories = findings.knowledge_advisories
    llr_status_advis = findings.llr_status_advis
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
        or findings.provenance
        or findings.form
    ):
        return 1
    if args.strict_integrity and findings.integrity:
        return 1
    return 0


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict", action="store_true", help="exit 1 if any orphan / status finding"
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
        help="G3 criterion: flag Verification=Test SRs not Status=Verified",
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
        help="flag any leftover '-000' template example row (use from G2 on)",
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
        "(e.g. 'SR-052,SR-053'); a G1/G2 brief links this instead of hand-copying "
        "rows (WI-146). The reserved scope 'modified' (WI-316) emits the "
        "RE-ATTESTATION brief instead: per-cell before/after for every Modified "
        "SR's chain vs its attested baseline (see --since). Prints to stdout "
        "unless --out is given; runs no checks",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="with --ratify modified: FRESHNESS mode. Re-render the brief and "
        "compare it against the committed file (--out, else the newest "
        "docs/ratify/*.md), exiting nonzero when they differ. The comparison "
        "uses the baseline THAT FILE declares, never a re-derived one (WI-325). "
        "Silent no-op when there is no brief, or when no SR is Modified (the "
        "window is closed and the brief is a record, not a live surface)",
    )
    ap.add_argument(
        "--since",
        metavar="REV",
        default=None,
        help="with --ratify modified, override the attested-baseline revision "
        "for every Modified SR (default: the newest revision where each SR row "
        "still read Verified — correct under the amend+flip-same-commit rule; "
        "use this for a pre-regime streak whose amendments landed while the row "
        "stayed Verified)",
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

    reg = load_registries(docs)

    # --ratify is a generator mode, not a checker: emit the batch-scoped
    # ratification hierarchy and exit 0 without running any orphan/integrity pass
    # (WI-146a). It reuses the loaded, example-filtered working sets above.
    # The reserved scope `modified` (WI-316) emits the re-attestation brief
    # instead: per-cell before/after for every Modified SR's chain, baselined at
    # the git-derived last-Verified revision (or --since).
    if args.ratify is not None:
        if args.ratify.strip().lower() == "modified" and args.check:
            # WI-325: freshness, not generation — compare the committed brief
            # against a render at the baseline THAT FILE declares.
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
                since=args.since,
            )
            print("trace: ratify-check — {}".format(message), file=sys.stderr)
            # `main()` is called bare at the bottom of this module, so a plain
            # `return` sets no exit status — this check must sys.exit like the
            # analyze path does, or it reports STALE and exits 0. (It did.)
            if code:
                sys.exit(code)
            return 0
        if args.ratify.strip().lower() == "modified":
            body = reattest_lines(
                Path(args.root), reg.srs, reg.llrs, reg.tcs, since=args.since
            )
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
