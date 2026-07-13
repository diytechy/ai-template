#!/usr/bin/env python3
"""Traceability join + orphan report for the SN->SR->LLR->TC registries.

Stack-agnostic reference implementation (Python 3, standard library only — no
pip installs). Drop it in a new repo as `scripts/trace.py` and wire it into the
check harness / CI. It is the generated "traceability matrix" referenced by
PROCESS.md: it never needs hand-maintaining.

Usage:
    python scripts/trace.py [--strict] [--strict-integrity] [--require-verified]
                            [--phase LIST] [--no-placeholders] [--strict-schema]
                            [--html] [--root DIR] [--docs DIR]

Reads (relative to --docs, default "<root>/docs"; --root defaults to "."):
    requirements/system-requirements.csv   (cols: SR-ID, SN-Refs, Verification, Status, ...)
    requirements/low-level-requirements.csv (cols: LLR-ID, SR-Refs, ...)
    test/test-cases.csv                     (cols: TC-ID, Verifies, ...)
    requirements/stakeholder-needs.md       (optional; SN-### ids scraped for SN->SR coverage.
                                             SN maturity is section-as-state: SNs under a heading
                                             containing "draft" are unratified/Draft (§4a) and
                                             exempt from the SN-with-no-SR orphan rule)
    requirements/performance-budgets.csv    (optional; PB-### perf/resource budgets, §9 —
                                             each row's Refs must back-link a real SR/LLR/Module)
    requirements/repos.csv                   (optional; REPO-### coordinator repo-delegation
                                             registry, MULTI_REPO.md — each row's DelegatedSRs
                                             must name a real coordinator SR; the multi-repo
                                             layer only. The legacy modules.csv / MOD-### form
                                             is still read)
    requirements/procurement.csv             (optional; PART-### purchased/external parts,
                                             process-options.md — each row's IF-Ref names the
                                             owning interface row of record (MULTI_REPO.md §3.3);
                                             integrity-checked only, like a MOD row with no
                                             DelegatedSRs)
    requirements/assets.csv                  (optional; ASSET-### binary/large-asset provenance,
                                             process-options.md "Binary assets" — provenance,
                                             license, attribution, contract link + a pointer/hash;
                                             integrity-checked only, like PART)
    requirements/components.csv              (optional; CMP-### domain-neutral components,
                                             process-options.md "Component layer" — the
                                             set-grained knowledge + lifecycle home; PartOf/
                                             SupersededBy must name real CMP ids, and a
                                             `Component` tag on an LLR/PART/ASSET row must
                                             resolve to a real CMP row)
    requirements/interfaces.csv              (optional; IF-### directed interface seams,
                                             process.md 8 — one row per directed seam
                                             (ThisProject module -> Counterpart module/file/
                                             external actor); each row's SR-Refs must resolve
                                             to a real SR, and ThisProject is best-effort
                                             joined to the LLR Module inventory. The seam
                                             registry is off the joined spine but must stay
                                             traceable to it (WI-056 closed the SR-002-era gap
                                             where trace.py never read the IF tier))

Writes:
    test/report.md  — counts, the SR->LLR->TC matrix, the orphan list, and two
        rendered views of the same join: a line-reviewable SN->SR->LLR->TC text
        outline and a small, diff-friendly Mermaid `graph LR` DAG colored by
        orphan/draft state.
    test/report.html (only with --html) — a dependency-free, collapsible
        <details> tree of the full graph (inline CSS, zero JS) that scales to any
        size. A generated composite artifact: gitignored, never the review
        surface — review the registry CSVs (process.md §3 "Reviewability").

Exit code: 0 normally; with --strict, 1 if any orphan (or, with
--require-verified, any status finding) exists — use in gates.

Orphan rules (the method rules are stated once, in process.md §4):
    - SR with no LLR (unless Verification is Analysis/Inspection/Attest — those
      have no code to decompose; Demonstration/Manual SRs still describe behavior
      the software implements, so they keep the LLR requirement. Attest is the
      human-attestation kind — a named person's recorded judgment, often over a
      subjective/binary asset with no code symbol, so it is LLR-exempt too.
      Critique is NOT LLR-exempt: the artifact it judges is *produced by code*
      (a render/generation pipeline) and only its acceptance is subjective, so a
      Critique SR keeps the LLR like Demonstration/Manual — a genuinely code-less
      subjective requirement is an Attest, not a Critique)
    - SR with no TC (every SR needs ≥1 TC row regardless of method; for human
      methods the TC records the procedure with Automated=No)
    - SR with no SN link (only when stakeholder-needs.md provides real SN ids —
      the G1 "every SR links ≥1 SN" criterion, machine-checked)
    - LLR with no SR parent, or referencing an unknown SR
    - LLR with no TC
    - TC that verifies nothing, or references an unknown SR/LLR
    - SN with no SR (only when stakeholder-needs.md is present; a Draft SN — see
      below — is exempt)
Draft exemption (derived-gate model, docs/specs/derived-gate-model.md §3): an
artifact in the pre-ratification `Draft` state is exempt from the
*child-completeness* rules above — a Draft SR needs no LLR/TC, a Draft LLR needs
no TC, and a Draft SN needs no SR — so a requirement can be drafted in the live
spine before it is decomposed (retiring the -000/off-spine workaround). SR/LLR/TC
maturity is the open-vocabulary `Status` value `Draft` (the ladder is Draft ->
Planned -> Verified); SN maturity is **section-as-state** (§4a): an SN under a
stakeholder-needs.md heading whose text contains "draft" (e.g. `## Draft needs
(unratified)`) is Draft, all other SNs ratified. Parent-linkage and integrity
rules still apply (a Draft SR still links an SN; ids stay unique/well-formed), and
a Draft SR is exempt from the --require-verified criterion below (it is
pre-ratification, below G1).
--require-verified adds the G3 status criterion:
    - SR with Verification=Test whose Status is not Verified (Draft SRs exempt)
--phase scopes that status criterion to a delivery phase (process.md §4
"Phased delivery"): SRs may carry an optional `Phase` column (e.g. v1, v2);
`--phase v1` (or a cumulative list, `--phase v1,v2`) exempts SRs tagged with
*other* phases from --require-verified and reports them as phase-deferred —
the exemption is explicit, never silent. A blank/absent Phase means the SR is
in scope for every phase. Orphan rules are phase-blind: every SR keeps its
LLR + TC rows regardless of phase.

Always (independent of --strict-schema), structural integrity is checked:
    - a registry CSV data row whose parsed column count differs from its
      header's. An unquoted comma (inside a Permutations set like `set{a,b,c}`
      or a free-text Rationale cell) silently shifts every later column, so the
      DictReader-based join reads misaligned cells for two gates before
      --strict-schema would notice. Checked for EVERY *.csv under
      docs/requirements/ and docs/test/ — spine, off-spine (interfaces,
      procurement, ...), and project-added registries alike — since the check
      needs no knowledge of a file's semantics, only its header
    - a duplicated SR/LLR/TC/PB/REPO/CMP/IF id (the join would otherwise silently dedupe it)
    - a malformed id (not "PREFIX-<digits>")
    - a performance-budget row (PB-###, §9) whose Refs name an unknown
      SR/LLR/Module, or that back-links nothing — the budgets registry is off the
      spine but must stay traceable to it (the PB-000 example row is ignored, so
      the optional registry never blocks a gate a project doesn't use)
    - a coordinator repo-delegation row (REPO-###, MULTI_REPO.md — the multi-repo
      layer; legacy MOD-###/modules.csv still read) whose DelegatedSRs name an
      unknown coordinator SR; an external/reused part
      referenced only via the IF-### catalog may delegate nothing, so an empty
      back-link is allowed here (unlike PB). The MOD-000 example row is ignored,
      so the optional registry never blocks a single-repo project's gate
    - a purchased/external part row (PART-###, process-options.md) with a
      malformed/duplicate PART- id. Its IF-Ref names the owning interface row of
      record (MULTI_REPO.md §3.3) but is NOT resolved here (the interface tier is
      checked in its own pass, below), so PART is integrity-checked only — like a
      MOD row that delegates nothing. The PART-000 example row is ignored, so the
      optional registry never blocks a gate
    - an interface seam row (IF-###, process.md §8 — the intra-repo/cross-project
      interface catalog) with a malformed/duplicate IF- id (the always-on floor),
      whose SR-Refs is empty or names an unknown SR (a --strict finding, like PB's
      back-links: every seam links the spine so it stays transitively TC-covered),
      or whose ThisProject endpoint resolves to no LLR Module after normalization
      (a warn-only advisory — the LLR Module set is a partial, differently-named
      inventory, so the full module-coverage check lives in check_trajectory
      against the arch-map). WI-056 closed the SR-002-era gap (trace.py never read
      the IF tier); the IF-000 example row is ignored, so the optional registry
      never blocks a gate
    - a binary/large-asset provenance row (ASSET-###, process-options.md "Binary
      assets") with a malformed/duplicate ASSET- id. Off the spine like PART:
      integrity-checked only, its provenance/license/hash tracked in text even
      though the asset itself can't be diffed. The ASSET-000 example row is
      ignored, so the optional registry never blocks a gate
    - a test case (TC) that cites an SR and an LLR together whose LLR does not
      decompose that SR (the LLR's SR-Refs excludes every SR the same TC cites).
      The combined `SR;LLR` citation is a convenience so one test discharges both
      the "SR needs a TC" and "LLR needs a TC" rules, but it must not contradict
      the SR<->LLR link recorded canonically on the LLR's SR-Refs — an incoherent
      pairing is wrong at any stage, like a malformed id (IMPROVEMENT_PLAN.md
      Thread 50). A TC citing only LLRs (no SR) has no SR to contradict and is
      left to the orphan rules
These join `--strict`'s failure set like orphans do. `--strict-integrity` fails
on *only* this integrity class: it is the always-valid floor the pre-commit hook
runs on every commit — a duplicated or malformed id is wrong at any stage, while
orphans are a G2+ *gate* criterion (a mid-G1 registry legitimately has SRs with
no LLR/TC yet, and must still be committable).

--no-placeholders flags any leftover template example row (id ending "-000") as
a finding — wire it in from G2 on (a fresh scaffold is exempt only until you
claim a gate). Without it, "-000" example rows are ignored so a fresh scaffold
starts green.

--strict-schema adds data-quality checks over the real (non-placeholder) rows:
    - required fields are non-empty (SR: SR-ID, Title, SN-Refs, Requirement,
      AcceptanceCriteria, Priority, Verification, Status; LLR: LLR-ID, SR-Refs,
      Title, Module, CodeSymbol, Detail, Status; TC: TC-ID, Verifies, Level,
      Method, Tier, Expected, Automated, Status);
    - a TC claiming Automated=Yes cites its Evidence (Thread 51, owner-ruled
      2026-07-09): the `Evidence` column names the concrete test — a pytest
      node, a script path, or a procedure-doc link. Inspection-only text, never
      a mechanized resolve (node ids aren't filesystem paths). Conditional, not
      a flat required field: Automated=No/blank rows may leave it empty, and
      `Parameters` stays reserved for dimensional inputs (the gen_cases
      grammar), which the pre-Evidence `node=` overload was polluting;
    - the two *closed* vocabularies the method defines (process.md §4) hold:
      SR Verification in {Test, Demonstration, Manual, Analysis, Inspection,
      Attest, Critique}, TC Tier in {Smoke, Full, Release}. Priority/Status are
      deliberately NOT enumerated — the method leaves them open (e.g. Priority S,
      Status Planned).

Always (warn-only, never an exit-code change), acceptance-criteria testability
is advised on: a comparative/absolute term in an SR's AcceptanceCriteria
("identical", "indistinguishable", "equivalent", "same as", "matches", ...)
with no pinned predicate nearby in the cell is flagged as a WARNING on stdout
and in the report. A comparative is untestable until it names its predicate —
identical *in what*, judged *how* ("cannot distinguish source by schema" vs
"identical field names and dtypes per IF-003"). The predicate heuristic looks
for pinning markers (i.e./e.g./defined/listed/per/measured/tolerance/golden/
byte-for-byte/byte-identical/bit-identical/== ...), so it is deliberately a
*lint*, not a gate: the G1
consistency review (process.md §4) makes the call, and the reviewer either
pins the predicate or accepts the wording knowingly.

When the SR registry carries the optional `Area` column (owner-hat/domain tag,
process.md §1) with real values, the report adds a per-Area SR count section —
report-only, never an exit-code change; blank cells and registries without the
column are simply not counted.

The report always includes a "Verification basis (attested vs mechanized)"
count (process.md §4 "Attest"): of the SRs reported Verified, how many rest on a
runnable check vs a named human's recorded judgment (Verification=Attest). This
keeps the project's trust footprint auditable — attestation is honest but
trust-based (the box can be checked without the work having happened), so the
report never lets it hide inside a bare "Verified".

Contracts: IF-001, IF-021, IF-042 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import re
import sys
from pathlib import Path


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
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def refs(value):
    """Split a multi-ref cell (';', ',' or whitespace separated) into ids."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


def is_example(rid):
    return rid.endswith("-000")


def is_draft(row):
    """A row in the pre-ratification `Draft` state (derived-gate model §3): exempt
    from the child-completeness orphan rules (a Draft SR needs no LLR/TC, a Draft
    LLR needs no TC) and from the --require-verified criterion, so a requirement
    lives in the live spine while it is being drafted. Status is open-vocabulary;
    `Draft` is the one value the orphan/status passes act on."""
    return (row.get("Status") or "").strip().lower() == "draft"


# SR Verification methods that decompose to a TC but no LLR — there is no code to
# write, only its acceptance to analyze/inspect/attest, so the orphan rule below
# exempts them from the "SR with no LLR" finding. The derived gate mirrors this
# exact set as derive_gate.LLR_EXEMPT; tests/test_rule_sync.py pins the two equal
# (WI-099) so the orphan report and the gate computation never disagree about what
# "decomposed" means. (Critique is NOT here: its artifact is produced by code, only
# its acceptance is subjective.)
LLR_EXEMPT = ("Analysis", "Inspection", "Attest")


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
    with path.open(newline="", encoding="utf-8-sig") as f:
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

# Fields that must be non-empty under --strict-schema. Deliberately omits the
# optional columns (Rationale, Permutations, Phase, TestRefs, Parameters).
REQUIRED_FIELDS = {
    "SR": [
        "SR-ID",
        "Title",
        "SN-Refs",
        "Requirement",
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

# Comparative/absolute terms that demand a predicate. Matched on word
# boundaries, case-insensitive ("schema-identical" matches "identical";
# "mismatches" does not match "matches").
COMPARATIVE_TERMS = (
    "identical",
    "indistinguishable",
    "equivalent",
    "interchangeable",
    "same as",
    "matches",
    "cannot distinguish",
    "cannot be distinguished",
    "no difference",
)
_TERM_RES = {
    t: re.compile(r"(?<!\w)" + re.escape(t).replace(r"\ ", r"\s+") + r"(?!\w)", re.I)
    for t in COMPARATIVE_TERMS
}

# Markers that (heuristically) pin a predicate in the same cell: an explicit
# definition/enumeration, a measurement/tolerance, or an exact-comparison basis.
# Word markers match on a WORD BOUNDARY, so "per"/"within" pin "as per the list"
# / "within 1 ULP" but NOT "proper"/"wrapper"/"notwithstanding" — a bare
# substring silently over-suppressed the advisory (warn-only, so this only
# sharpens lint quality). Symbol/abbreviation markers carry their own boundaries
# and match literally.
_PREDICATE_WORDS = (
    "namely",
    "defined",
    "specified",
    "listed",
    "enumerated",
    "per",
    "measured",
    "within",
    "tolerance",
    "predicate",
    "byte-for-byte",
    "bit-for-bit",
    # Self-pinning comparatives: "byte-identical"/"bit-identical" *name* their
    # predicate (the comparison basis is raw bytes/bits), exactly like
    # "byte-for-byte" — the bare comparative "identical" alone still warns.
    "byte-identical",
    "bit-identical",
    "golden",
    "regex",
    "checksum",
)
_PREDICATE_SYMBOLS = ("i.e.", "e.g.", "±", "==")
_PREDICATE_RE = re.compile(
    "|".join(
        [r"\b" + re.escape(w) + r"\b" for w in _PREDICATE_WORDS]
        + [re.escape(s) for s in _PREDICATE_SYMBOLS]
    ),
    re.IGNORECASE,
)


def ac_advisories(srs):
    """Warn-only findings: real SR rows whose AcceptanceCriteria uses a
    comparative term with no pinning marker anywhere in the cell."""
    out = []
    for r in srs:
        cell = (r.get("AcceptanceCriteria") or "").strip()
        if not cell:
            continue
        terms = [t for t, rx in _TERM_RES.items() if rx.search(cell)]
        if terms and not _PREDICATE_RE.search(cell):
            out.append(
                "SR {} AcceptanceCriteria uses {} without a named predicate — "
                "say identical/equivalent *in what*, judged *how* (process.md "
                "§4 consistency review; heuristic, warn-only)".format(
                    r["SR-ID"], ", ".join(repr(t) for t in sorted(terms))
                )
            )
    return out


# Verification methods whose "Verified" state rests on a recorded human judgment,
# not a runnable check (process.md §4 "Attest"). --require-verified accepts these
# as legitimately Verified but the report surfaces them distinctly ("attested vs
# mechanized"), so an audit can always see how much of the project rests on trust.
ATTESTED_METHODS = {"Attest"}


def id_key(label):
    return label + "-ID"


def integrity_findings(label, raw_rows):
    """Duplicated or malformed ids in one registry (example '-000' rows skipped —
    those are the placeholder check's job, never an integrity error)."""
    key, pattern = id_key(label), ID_PATTERNS[label]
    found, seen = [], set()
    for r in raw_rows:
        rid = r.get(key)
        if not rid or is_example(rid):
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


def triangle_findings(tcs, llrs):
    """SR/LLR citation coherence (IMPROVEMENT_PLAN.md Thread 50). A TC may cite an
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
    text = sn_md.read_text(encoding="utf-8")
    return sorted({u for u in re.findall(r"\bSN-\d+\b", text) if is_example(u)})


# SN maturity lives in section-as-state (derived-gate model §4a): a stakeholder-
# needs.md heading whose text contains "draft" (case-insensitive, e.g. `## Draft
# needs (unratified)`) marks the SNs under it as Draft (unratified, G0); SNs under
# any other heading are ratified (G1). No new column — the state IS the section,
# and the ratification date is git-derived (the commit that moved the row out of
# the draft section). This is the SN analogue of the `Status=Draft` bit on
# SR/LLR/TC rows.
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)")


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
        # Thread 51 (owner-ruled 2026-07-09): a TC claiming Automated=Yes must
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


def build_forest(sn_ids, srs, llrs, tcs, orphan_ids, sn_draft=frozenset()):
    """The SN -> SR -> LLR -> TC chain as nested nodes, plus synthetic groups for
    rows with no valid parent. Shared by the text outline and the HTML tree.
    `sn_draft` (section-as-state, §4a) labels those SNs `Draft` so the views flag
    them like a `Status=Draft` SR/LLR/TC row."""

    def tc_node(t):
        return _node(t["TC-ID"], _cell(t, "Status"), _cell(t, "Method"), orphan_ids)

    def llr_node(lr):
        lid = lr["LLR-ID"]
        kids = [tc_node(t) for t in tcs if lid in refs(t.get("Verifies"))]
        return _node(lid, _cell(lr, "Status"), _cell(lr, "Title"), orphan_ids, kids)

    def sr_node(s):
        sid = s["SR-ID"]
        own_llrs = {lr["LLR-ID"] for lr in llrs if sid in refs(lr.get("SR-Refs"))}
        kids = [llr_node(lr) for lr in llrs if sid in refs(lr.get("SR-Refs"))]
        # TCs verifying the SR directly but none of its LLRs (so a TC that already
        # appears under an LLR of this SR is not also repeated under the SR).
        for t in tcs:
            verifies = set(refs(t.get("Verifies")))
            if sid in verifies and not verifies & own_llrs:
                kids.append(tc_node(t))
        return _node(sid, _cell(s, "Status"), _cell(s, "Title"), orphan_ids, kids)

    sr_ids = {s["SR-ID"] for s in srs}
    llr_ids = {lr["LLR-ID"] for lr in llrs}
    roots = []
    for sn in sorted(sn_ids):
        kids = [sr_node(s) for s in srs if sn in refs(s.get("SN-Refs"))]
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
    # --root/--docs are the uniform path flags across trace.py, check_docs.py,
    # and check_perf.py: --docs is the docs dir; --root (default ".") is its
    # parent, so a repo whose docs live elsewhere passes one --root. An explicit
    # --docs wins; otherwise it is <root>/docs.
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--docs",
        default=None,
        help="docs directory (default: <root>/docs)",
    )
    args = ap.parse_args()
    docs = Path(args.docs) if args.docs else Path(args.root) / "docs"

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

    def _repo_id(r):
        return r.get("REPO-ID") or r.get("MOD-ID")

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
    sn_md = docs / "requirements" / "stakeholder-needs.md"
    if sn_md.exists():
        sn_text = sn_md.read_text(encoding="utf-8")
        sn_ids = {u for u in re.findall(r"\bSN-\d+\b", sn_text) if not is_example(u)}
        # Section-as-state maturity (derived-gate §4a): SNs under a "draft" heading
        # are unratified (G0) and exempt from the "SN with no SR" child rule below.
        sn_draft = sn_draft_ids(sn_text)

    sr_ids = {r["SR-ID"] for r in srs}
    llr_ids = {r["LLR-ID"] for r in llrs}
    llr_sr_refs = {x for r in llrs for x in refs(r.get("SR-Refs"))}
    tc_refs = {x for r in tcs for x in refs(r.get("Verifies"))}
    sr_sn_refs = {x for r in srs for x in refs(r.get("SN-Refs"))}

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
        analytic = r.get("Verification", "") in LLR_EXEMPT
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

    valid = sr_ids | llr_ids
    for r in tcs:
        tid = r["TC-ID"]
        verified = refs(r.get("Verifies"))
        if not verified:
            orphans.append(f"TC {tid} verifies nothing")
            orphan_ids.add(tid)
        for x in verified:
            if x not in valid:
                orphans.append(f"TC {tid} references unknown {x}")
                orphan_ids.add(tid)

    for u in sorted(sn_ids):
        # A Draft SN (section-as-state, §4a) is being drafted requirement-first and
        # is exempt from the child-completeness rule, like a Draft SR.
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
    # a `Component` tag on an LLR/PART/ASSET row must resolve to a real CMP row
    # (IF rows carry the tag too, but the IF tier is off trace.py's read set).
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
            ("PART", parts, "PART-ID"),
            ("ASSET", assets, "ASSET-ID"),
        ):
            for r in rows_:
                for x in refs(r.get("Component")):
                    if x not in cmp_ids:
                        component_findings.append(
                            f"{label} {r[key]} Component tag references unknown {x}"
                        )

    # Interface seams (IF-###, process.md §8): SR-Refs back-links join the
    # --strict failure set like PB's; the ThisProject-vs-LLR-Module endpoint join
    # is a warn-only advisory (module_ids reused from the PB back-link check above).
    interface_backlink_findings, interface_advisories = interface_findings(
        ifs, sr_ids, module_ids
    )

    phases = set(refs(args.phase)) if args.phase else None

    def in_phase(r):
        """Blank Phase = every phase; otherwise the SR's phase must be listed."""
        tag = (r.get("Phase") or "").strip()
        return phases is None or not tag or tag in phases

    status_findings = []
    phase_deferred = []
    # Attested-vs-mechanized audit surface (process.md §4 "Attest"): of the SRs
    # the project reports as Verified, how many rest on a runnable check vs a
    # recorded human judgment (Attest)? Independent of --require-verified so the
    # trust footprint is always visible in the report.
    mechanized_verified = [
        r["SR-ID"]
        for r in srs
        if r.get("Status", "") == "Verified"
        and r.get("Verification", "") not in ATTESTED_METHODS
    ]
    attested_verified = [
        r["SR-ID"]
        for r in srs
        if r.get("Status", "") == "Verified"
        and r.get("Verification", "") in ATTESTED_METHODS
    ]
    if args.require_verified:
        for r in srs:
            if r.get("Verification", "") != "Test":
                continue
            # A Draft SR is pre-ratification (below G1, derived-gate §3): it makes
            # no Verified claim yet, so the G3 criterion does not apply. Surfaced
            # in the draft count so the exemption stays auditable.
            if is_draft(r):
                continue
            if not in_phase(r):
                phase_deferred.append(
                    f"SR {r['SR-ID']} (Phase={r.get('Phase', '').strip()}) — "
                    "status check deferred to its own phase"
                )
                continue
            if r.get("Status", "") != "Verified":
                status_findings.append(
                    f"SR {r['SR-ID']} is Verification=Test but Status="
                    f"{r.get('Status', '') or '(blank)'} (G3 requires Verified)"
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
    # SR/LLR citation coherence (Thread 50): a TC that cites an SR and an LLR
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
        if args.strict_schema
        else []
    )
    # Warn-only, always on: comparative AcceptanceCriteria terms with no pinned
    # predicate (see the module docstring). Never joins a failure set below.
    advisories = ac_advisories(srs)

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
            f"| Verified SRs — mechanized | {len(mechanized_verified)} |",
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
    for r in srs:
        sid = r["SR-ID"]
        kids = " ".join(x["LLR-ID"] for x in llrs if sid in refs(x.get("SR-Refs")))
        tests = " ".join(x["TC-ID"] for x in tcs if sid in refs(x.get("Verifies")))
        lines.append(f"| {sid} | {kids} | {tests} | {r.get('Status', '')} |")

    forest = build_forest(sn_ids, srs, llrs, tcs, orphan_ids, sn_draft)
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
    # Attested-vs-mechanized surface (process.md §4 "Attest"): make the project's
    # trust footprint auditable — how much of what is "Verified" rests on a named
    # human's recorded judgment rather than a runnable check.
    lines += ["", "## Verification basis (attested vs mechanized)", ""]
    lines += [
        "_Of the SRs reported `Verified`: `Attest` rows rest on a named human's "
        "recorded judgment (trust-based — the box can be checked without the work "
        "having happened, process.md §4); all others rest on a runnable check._",
        "",
        f"- Mechanized (Test/Demonstration/Manual/Analysis/Inspection): "
        f"{len(mechanized_verified)}",
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
            ["None. Every in-scope Verification=Test SR is Verified."]
            if not status_findings
            else [f"- {s}" for s in status_findings]
        )
        if phase_deferred:
            lines += ["", "### Phase-deferred (explicitly out of scope)", ""]
            lines += [f"- {s}" for s in phase_deferred]

    out = docs / "test" / "report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    html_out = None
    if args.html:
        html_out = docs / "test" / "report.html"
        html_out.write_text(html_document(forest), encoding="utf-8")

    # Advisories are loud (stdout, not just the report) but never fail the run.
    for a in advisories:
        print(f"WARNING (advisory): {a}")
    for a in interface_advisories:
        print(f"WARNING (advisory): {a}")
    print(
        f"Traceability: SN={len(sn_ids)} SR={len(srs)} LLR={len(llrs)} "
        f"TC={len(tcs)} orphans={len(orphans)} integrity={len(integrity)}"
        + (
            f" verified-mechanized={len(mechanized_verified)}"
            f" verified-attested={len(attested_verified)}"
            if attested_verified
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
            f" interfaces={len(ifs)} "
            f"interface-findings={len(interface_backlink_findings)}"
            if ifs
            else ""
        )
        + (f" ac-advisories={len(advisories)}" if advisories else "")
        + f". Report -> {out}"
        + (f" + {html_out}" if html_out else "")
    )
    if args.strict and (
        orphans
        or status_findings
        or integrity
        or placeholders
        or schema
        or budget_findings
        or module_findings
        or component_findings
        or interface_backlink_findings
    ):
        sys.exit(1)
    if args.strict_integrity and integrity:
        sys.exit(1)


if __name__ == "__main__":
    main()
