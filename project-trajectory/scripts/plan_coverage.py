#!/usr/bin/env python3
"""The plan gate: make a plan's coverage of what it must deliver a checkable
verdict (process-options.md "Dual-plan decomposition", step 3).

Two runs, one grammar:

  * DUAL (`--goal`): two independent planners decompose one goal into rival
    plans. Reviews merge mechanically; rival plans do not — so the
    reconciliation is select-and-port, and the selection needs an *external,
    computed* signal: what each plan covers, and what one covers that the other
    misses. The clauses are the goal's `C#` lines; an uncovered clause is a
    finding unless an `Excludes:` line names it with a reason.
  * SINGLE (`--item`): one plan for one claimed work item. The clauses are the
    item's Done-when items, `D1…Dn` in order (`kitlib.done_when.items`, the
    one reading of a Done-when — never re-parsed here), plus the open review
    findings `F1…` a replan answers (`--findings`). The run also diffs the
    item's SRs and the TCs that verify them against the rows (the SR/TC diff
    below).

In both runs coverage IS the gate: every clause is covered by a row or
excluded with a reason, and an unexplained gap is a finding.

It never judges plan quality — solvability, honest coverage, and seam
duplication are the rubric's job (docs/rubrics/, the plan-critic hat).

    python scripts/plan_coverage.py (--goal GOAL.md | --item SPEC.md
                                    [--findings FINDINGS.md])
                                    PLAN.md [PLAN.md ...]
                                    [--root .] [--out coverage.md]

The commensurability contract it parses:

  - the goal brief declares numbered clauses — lines like `C1: <text>`
    (optionally list-marked or bold); a findings file declares `F1: <text>`
    the same way, or is a review verdict whose finding lines become F1..Fn in
    order (`finding_clauses`, the one step the coordinator's attended rework
    round uses and WI-805's loop replan is to call — WI-853);
  - each plan holds one markdown table with a `Plan-WI` header column:
    `| Plan-WI | Title | Covers | Interfaces | Predecessors |`, plus an
    optional `Tier` column (carried for the consumer that applies it, never
    validated here) — `Covers` cites clause ids and `SR-###` ids
    (`;`-separated; a SINGLE plan also names `TC-###` ids it runs or amends),
    `Interfaces` cites `IF-###` ids from docs/requirements/interfaces.toml,
    or `Proposed:` plus a nearest-existing-IF rationale, or the intra-module
    escape;
  - anywhere in a plan, `Excludes: <ref>[; <ref>] — <reason>` lines name what
    the plan deliberately leaves out (an em dash, an en dash, or a spaced
    hyphen separates the reason).

Findings (exit 1):
    - a `Covers` cite of an undeclared clause or (when the registry exists)
      an unknown SR-### / TC-###; a row citing nothing;
    - an `IF-###` cite that resolves to no interfaces.csv row; a `Proposed:`
      seam with no rationale text; an empty `Interfaces` cell with no
      intra-module escape;
    - a duplicate `Plan-WI` id, an unknown `Predecessors` id, or a
      predecessor cycle;
    - an `Excludes:` line with no reason, or naming an undeclared clause;
    - an `F#` exclusion whose reason cites a dispute verdict
      (`.../NNN-ADJUDICATE-<sha>.md`, optionally `#<the sitting's id>`) that
      is not an accepted dispute verdict ruling that finding DISMISS — only a
      dismissal resolves a finding; a FIX is covered by a row — or whose
      ruled finding is not shown to be that `F#` finding: every dispute
      findings file beside the verdict requesting the ids its call requested
      must record the ruled finding as the review wrote it (no such file, or
      one recording another finding, refuses);
    - a clause neither covered by a row nor excluded with a reason;
    - SINGLE only: an item SR no row cites (an item SR cannot be excluded);
      a TC verifying one of those SRs that no row names and no line excludes.

Malformed inputs (no clauses in the goal, no Done-when in the item, no
findings in a findings file or one mixing both shapes, no plan table) exit 2.

Contracts: IF-060, IF-152, IF-153 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-060: the exit alphabet the coverage step decides on. 0 clean, 1
    findings, 2 malformed input, and the three are kept distinct because they
    mean different things to a round — 1 says the plans were read and something
    in them is wrong, so the `plan_coverage: FAIL - <planfile>:` lines on
    stdout name which plan is implicated; 2 says the inputs could not be read
    at all (no numbered clauses in the goal, no Done-when in the item, a
    missing file, no `Plan-WI` table in a plan) and the caller bounces the
    plans rather than reading a stale report. In either run an unexplained
    clause gap is a finding, so a plan cannot narrow its goal or item
    silently; a rival plan that is honestly incomplete says so with an
    `Excludes:` line.
Contract IF-152: the headless argv surface. Exactly one of `--goal GOAL.md`
    (DUAL) or `--item SPEC.md` (SINGLE) is required, and one or more plan
    paths are positional; `--findings FINDINGS.md` adds the `F#` clauses and
    is only valid with `--item`; `--root` (default `.`) names the repo root
    holding docs/requirements/ and docs/test/ for the SR, IF and TC reference
    checks, and `--out` names a file to write the report to as well as stdout.
    No other flag exists, and an absent input file is a malformed run rather
    than a finding.
Contract IF-153: the `--out` report file. It is the same markdown the run
    prints — per-plan rows, covered, UNCOVERED and excluded clause lists,
    multi-covered clauses, a SINGLE run's SR/TC diff, then a pairwise
    `only A / only B / both / neither` diff — with the FAIL, OK and note lines
    deliberately left out, so it is the clean payload a critic brief embeds.
    It is written on a clean or findings run and NOT on a malformed one, which
    is why a leftover file from an earlier stage must never be read as this
    run's.
"""

import argparse
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console
from kitlib import dispute as _dispute
from kitlib import done_when as _done_when
from kitlib import sitting as _sitting
from kitlib import spine as _kitspine
from kitlib.registry import parse_spec_frontmatter, plan_table_rows

# Sibling: the spine's registry CARRIER — the one home for
# the TOML tier tables, the key->column vocabulary and both readers. Run as a
# subprocess this script's own dir is sys.path[0] so a plain import resolves;
# the guard covers an in-process import (a test) whose sys.path does not yet
# carry scripts/ — the sanctioned-sibling idiom trace.py uses for trace_text.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier
# Sibling: the one reader of a review verdict's finding lines (IF-046).
import score_reviews  # noqa: E402  (path set above; the script-sibling idiom)


_CLAUSE_DECL = r"^\s*(?:[-*]\s+)?\**({}\d+)\**\s*[:.]\s*(\S.*)$"
CLAUSE_DECL_RE = re.compile(_CLAUSE_DECL.format("C"))
FINDING_DECL_RE = re.compile(_CLAUSE_DECL.format("F"))
# A cited clause: a goal's C#, a Done-when item's D#, an open finding's F#.
CLAUSE_REF_RE = re.compile(r"^[CDF]\d+$")
# A cited registry row: the SR tier always, the TC tier in a SINGLE run.
REGISTRY_REF_RE = re.compile(r"^(SR|TC)-\d+$")
IF_REF_RE = re.compile(r"\bIF-\d+\b")
# The same escape hatch specs use (PROCESS.md §8): a WI acting inside one
# module states that instead of inventing a seam.
INTRA_MODULE_RE = re.compile(
    r"intra-module|single-module|no (?:cross-module )?seam|no interface", re.I
)
# `Excludes: <refs> — <reason>`, optionally list-marked or bold.
EXCLUDES_RE = re.compile(r"^\s*(?:[-*]\s+)?\**Excludes\**\s*:\**\s*(.*)$")
EXCLUDES_SEP_RE = re.compile(r"\s*[—–]\s*|\s+-\s+|\s+-$")
# A dispute verdict an F# exclusion cites as its resolution: the recorded
# `NNN-ADJUDICATE-<sha>.md` path, optionally `#<the sitting's finding id>`.
RULING_CITE_RE = re.compile(
    r"(?P<path>[\w./\-]*ADJUDICATE-[0-9a-f]+\.md)(?:#(?P<id>[A-Za-z][\w.-]*))?"
)
# What a hand copy of a finding may change without changing the finding
# (`_finding_key`): its leading list marker and `[SEVERITY]` tag, and the
# typographic forms of quotes, dashes and the finding line's arrow.
_COMPARE_RE = re.compile(r"^\s*(?:[-*]\s+)?(?:\[[A-Za-z]+\]\s*)?")
_TYPOGRAPHIC = str.maketrans(
    {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "→": "->",
    }
)
# The table columns a row carries besides its id; `tier` is optional.
ROW_KEYS = ("title", "covers", "interfaces", "predecessors", "tier")


def parse_goal(text, decl=CLAUSE_DECL_RE):
    """The declared clauses (a goal's `C#`, or with `FINDING_DECL_RE` a
    findings file's `F#`): ordered {id: text}. Duplicate declarations are a
    malformed brief (ValueError) — ids must be citable."""
    clauses = {}
    for line in text.splitlines():
        m = decl.match(line)
        if not m:
            continue
        cid = m.group(1)
        if cid in clauses:
            raise ValueError("goal brief declares {} twice".format(cid))
        clauses[cid] = m.group(2).strip()
    return clauses


def finding_clauses(text):
    """THE SHARED STEP (WI-853): a findings file's `F#` clauses, ordered
    {id: text}. A review verdict's finding lines (`- [SEVERITY] <anchor> ->
    ...`, read by `score_reviews.parse_verdict`, their one reader) become F1..Fn
    in the order written, each carrying the finding as written; a file that
    already declares `F1: <text>` lines is read as declared. The coordinator's
    attended rework round uses it today, through `--findings`; it is the step
    WI-805's loop replan is to call, not yet wired. A file mixing the two shapes is malformed (ValueError): which
    finding is F1 would depend on the shape read.

    Implements: SR-236, LLR-069
    """
    declared = parse_goal(text, FINDING_DECL_RE)
    lines = score_reviews.parse_verdict(text).findings
    if declared and lines:
        raise ValueError(
            "the findings file carries both declared F# lines and review "
            "finding lines; give one shape"
        )
    if declared:
        return declared
    return {
        "F{}".format(n): "[{}] {}".format(f.severity, f.raw.split("]", 1)[1].strip())
        for n, f in enumerate(lines, 1)
    }


def parse_plan(text):
    """The plan's proposed-WI rows from the first table whose header carries a
    `Plan-WI` column. Returns a list of dicts (id plus `ROW_KEYS` — cells raw,
    split done by the caller; an absent optional column reads as ""), or []
    when no such table exists. The table walk is `kitlib.registry`'s
    (`plan_table_rows`, shared with the filer since WI-821); this picks the
    cells the coverage pass reads."""
    return [
        dict(id=row["plan-wi"], **{k: row.get(k, "") for k in ROW_KEYS})
        for row in plan_table_rows(text)
    ]


def parse_excludes(text):
    """Every `Excludes:` line in a plan as `(refs, reason)`; the reason is ""
    when the line gives none.

    Implements: SR-155, LLR-069
    """
    found = []
    for line in text.splitlines():
        m = EXCLUDES_RE.match(line)
        if m:
            parts = EXCLUDES_SEP_RE.split(m.group(1).strip(), maxsplit=1)
            reason = parts[1].strip() if len(parts) > 1 else ""
            found.append((split_refs(parts[0]), reason))
    return found


# Ref tokens from a table cell — ids separated by `;`, `,` or whitespace. ONE
# HOME since WI-448 slice 4 (`kitlib.spine.refs`). THIS is the copy that had
# drifted to `[;,]` alone (B10 in the part-A census, 2026-08-13), so a
# whitespace-separated pair in an LLM-authored plan cell read as ONE garbage
# token and silently matched nothing — the same splitting defect class as the
# SN-001/SN-002 orphan bug OI-12 records. A pin repaired it and then held it
# equal to `check_trajectory._split_refs`; the shared home makes the drift
# unrepresentable instead, and the pin retires.
split_refs = _kitspine.refs


def spine_ids(path, key):
    """The id column of a registry, read through the CARRIER so it answers
    whichever of TOML/CSV is live.

    (Its CSV-only twin `load_registry_ids` went dead at WI-443, when the IF tier
    — the last caller — moved to the carrier with `interfaces.toml`.)

    Absent means 'cannot validate', never 'everything is unknown': None when the
    registry does not exist under either carrier, never an empty set. The
    distinction is the whole value of this function — an empty set would report
    every SR reference in a proposed plan as unknown."""
    if spine_carrier.resolve(path) is None:
        return None
    return {r[key] for r in spine_carrier.load(path, key) if r.get(key)}


def verifying_tcs(path):
    """{TC id: [SR ids it verifies]} from the test-case registry, or None when
    the registry does not exist (the same absent-is-unvalidated rule as
    `spine_ids`).

    Implements: SR-155, LLR-069
    """
    if spine_carrier.resolve(path) is None:
        return None
    return {
        r["TC-ID"]: split_refs(r.get("Verifies") or "")
        for r in spine_carrier.load(path, "TC-ID")
        if r.get("TC-ID")
    }


def proposed_rationale_present(cell):
    """True when a `Proposed:` interfaces cell carries rationale text beyond
    ids and the marker itself — a PRESENCE check; whether the rationale is
    honest is the rubric's seam-duplication anchor."""
    residue = IF_REF_RE.sub("", cell)
    residue = re.sub(r"(?i)proposed|[-*:()\[\].,;]", "", residue)
    return len(residue.strip()) >= 8


def find_cycle(rows):
    """A predecessor cycle among plan rows (list of ids), or None. Iterative
    DFS over the plan-local edge set; unknown ids are reported separately and
    skipped here."""
    ids = {r["id"] for r in rows}
    edges = {
        r["id"]: [p for p in split_refs(r["predecessors"]) if p in ids] for r in rows
    }
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    for start in sorted(ids):
        if color[start] != WHITE:
            continue
        stack = [(start, iter(edges[start]))]
        color[start] = GRAY
        path = [start]
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[node] = BLACK
                stack.pop()
                path.pop()
                continue
            if color[nxt] == GRAY:
                return path[path.index(nxt) :] + [nxt]
            if color[nxt] == WHITE:
                color[nxt] = GRAY
                path.append(nxt)
                stack.append((nxt, iter(edges[nxt])))
    return None


def ref_problem(ref, clauses, ref_ids):
    """What is wrong with one cited ref, or None when it resolves.

    `ref_ids` maps each citable registry tier (`SR`, and `TC` in a SINGLE run)
    to its id set, or None when that registry is absent (unvalidated, never
    unknown). A tier not in `ref_ids` is not part of this run's grammar.

    Implements: SR-155, LLR-069
    """
    if CLAUSE_REF_RE.match(ref):
        return None if ref in clauses else "undeclared clause {}".format(ref)
    m = REGISTRY_REF_RE.match(ref)
    if m and m.group(1) in ref_ids:
        ids = ref_ids[m.group(1)]
        return None if ids is None or ref in ids else "unknown {}".format(ref)
    kinds = sorted({c[0] + "#" for c in clauses}) + [
        "{}-###".format(k) for k in ref_ids
    ]
    return "unparseable ref {!r} ({} expected)".format(ref, " or ".join(kinds))


def _covers_findings(name, row, clauses, ref_ids, covered):
    """One row's `Covers` findings; records each clause it covers.

    Implements: SR-155, LLR-069
    """
    rid = row["id"]
    refs = split_refs(row["covers"])
    if not refs:
        return [
            "{}: {} cites no clause/SR - every row must say what it "
            "covers (the commensurability contract)".format(name, rid)
        ]
    findings = []
    for ref in refs:
        problem = ref_problem(ref, clauses, ref_ids)
        if problem is None:
            if ref in clauses:
                covered.setdefault(ref, []).append(rid)
        elif problem.startswith("unparseable"):
            findings.append("{}: {} Covers cell has {}".format(name, rid, problem))
        else:
            findings.append("{}: {} cites {}".format(name, rid, problem))
    return findings


def _interfaces_findings(name, rid, cell, if_ids):
    """One row's `Interfaces` findings.

    Implements: SR-155, LLR-069
    """
    findings = []
    cited = IF_REF_RE.findall(cell)
    is_proposed = re.search(r"(?i)\bproposed\b", cell)
    for iid in cited:
        if if_ids is not None and iid not in if_ids:
            findings.append(
                "{}: {} cites {} which resolves to no interfaces.toml row".format(
                    name, rid, iid
                )
            )
    if is_proposed and not proposed_rationale_present(cell):
        findings.append(
            "{}: {} proposes a seam with no rationale - name the nearest "
            "existing IF-### and why it falls short".format(name, rid)
        )
    if not cited and not is_proposed and not INTRA_MODULE_RE.search(cell):
        findings.append(
            "{}: {} Interfaces cell cites no IF-###, proposes nothing, "
            "and states no intra-module escape".format(name, rid)
        )
    return findings


def check_plan(name, rows, clauses, ref_ids, if_ids):
    """One plan's findings + its covered-clause set."""
    findings = []
    covered = {}  # clause id -> [row ids]
    seen = set()
    ids = {row["id"] for row in rows}
    for r in rows:
        rid = r["id"]
        if rid in seen:
            findings.append("{}: duplicate Plan-WI id {}".format(name, rid))
        seen.add(rid)
        findings += _covers_findings(name, r, clauses, ref_ids, covered)
        findings += _interfaces_findings(name, rid, r["interfaces"], if_ids)
        findings += [
            "{}: {} names unknown predecessor {}".format(name, rid, p)
            for p in split_refs(r["predecessors"])
            if p not in ids
        ]
    cycle = find_cycle(rows)
    if cycle:
        findings.append("{}: predecessor cycle {}".format(name, " -> ".join(cycle)))
    return findings, covered


def check_excludes(name, excludes, clauses, ref_ids):
    """A plan's `Excludes:` findings and what it validly excludes,
    `{ref: reason}`. A line with no reason excludes nothing.

    Implements: SR-155, LLR-069
    """
    findings, excluded = [], {}
    for refs, reason in excludes:
        if not reason:
            findings.append(
                "{}: Excludes: {} gives no reason".format(name, " ".join(refs))
            )
            continue
        for ref in refs:
            problem = ref_problem(ref, clauses, ref_ids)
            if problem:
                findings.append("{}: Excludes: names {}".format(name, problem))
            else:
                excluded[ref] = reason
    return findings, excluded


def gap_findings(name, clauses, covered, excluded):
    """Each clause no row covers and no line excludes — the gate.

    Implements: SR-155, LLR-069
    """
    return [
        "{}: {} is neither covered by a row nor excluded with a reason: {!r}".format(
            name, cid, text
        )
        for cid, text in clauses.items()
        if cid not in covered and cid not in excluded
    ]


def _finding_key(text):
    """A finding's text as compared across copies: no leading list marker or
    `[SEVERITY]` tag, typographic quotes, dashes and arrows as ASCII, and
    whitespace runs as one space - what a hand copy of the reviewer's line
    may change without changing the finding.

    Implements: SR-236, LLR-069
    """
    text = _COMPARE_RE.sub("", text.translate(_TYPOGRAPHIC))
    return " ".join(text.split())


def _ruled_texts(verdict, ids, rid):
    """The text of the finding `rid` in every dispute findings file
    (`kitlib.dispute.read_findings`) beside `verdict` whose ids, in order,
    are the `ids` its call requested: the files that sitting can have ruled.

    Implements: SR-236, LLR-069
    """
    texts = []
    for path in sorted(verdict.parent.glob("*.toml")):
        found, _why = _dispute.read_findings(
            path.read_text(encoding="utf-8", errors="replace"), path.name
        )
        if found and tuple(f["id"] for f in found["findings"]) == tuple(ids):
            texts += [f["finding"] for f in found["findings"] if f["id"] == rid]
    return texts


def _correspondence_problem(path, verdict, ids, rid, fid, text):
    """Why the finding `rid` the verdict at `path` ruled is not shown to be
    this review's `fid` (whose clause text is `text`), or None. The repo
    records no link from a verdict to the findings file its sitting read, so
    every candidate beside it (`_ruled_texts`) must record that finding as
    `fid`'s text (`_finding_key`); none, or one that differs, refuses.

    Implements: SR-236, LLR-069
    """
    texts = _ruled_texts(verdict, ids, rid)
    if not texts:
        return (
            "cites {}, beside which no findings file requesting {} records "
            "the finding {} it ruled".format(path, ";".join(ids), rid)
        )
    want = _finding_key(text)
    if any(_finding_key(t) != want for t in texts):
        return "cites {}, whose finding {} is not this review's {}".format(
            path, rid, fid
        )
    return None


def ruling_problem(root, cite, fid, text):
    """Why the dispute verdict `cite` names does not resolve the finding `fid`
    (clause text `text`), or None when it does. `cite` is a `RULING_CITE_RE`
    match: the verdict's path under `root` and, optionally, the sitting's own
    id for the finding (default `fid`). It resolves only as a recorded,
    ACCEPTED dispute verdict (its binding beside it) whose ruling of that id is
    DISMISS - a FIX ruling is work a row covers, and an ESCALATE ruling is the
    owner's to decide - AND whose ruled finding is `fid` itself, as the
    findings file beside the verdict records it (`_correspondence_problem`):
    a dismissal of another finding, or of another round's finding under the
    same id, resolves nothing.

    Implements: SR-236, LLR-069
    """
    path, rid = cite.group("path"), cite.group("id") or fid
    verdict = Path(root) / path
    binding = Path(_sitting.requested_path(verdict))
    if not verdict.is_file() or not binding.is_file():
        return "cites {}, which does not exist with its binding".format(path)
    bound = _sitting.read_requested(binding.read_text(encoding="utf-8"))
    if bound is None or bound[0] != _dispute.BRIEF:
        return "cites {}, which is not a dispute verdict".format(path)
    if bound[2] != "accepted":
        return "cites {}, whose call has outcome {}".format(path, bound[2])
    rulings, why = _dispute.parse(verdict.read_text(encoding="utf-8"), bound[1], path)
    if why:
        return "cites a refused verdict: {}".format(why)
    if rid not in rulings:
        return "cites {}, which does not rule {}".format(path, rid)
    if rulings[rid][0] != "DISMISS":
        return "cites {}, which rules {} {}; only a DISMISS resolves a finding".format(
            path, rid, rulings[rid][0]
        )
    return _correspondence_problem(path, verdict, bound[1], rid, fid, text)


def resolution_findings(name, excluded, root, clauses):
    """Each `F#` exclusion whose reason cites a dispute verdict that does not
    resolve it (`ruling_problem`, judged against the clause's text in
    `clauses`). An exclusion citing no verdict is a plain reasoned exclusion
    and is left as one.

    Implements: SR-236, LLR-069
    """
    out = []
    for fid, reason in excluded.items():
        cite = RULING_CITE_RE.search(reason) if fid.startswith("F") else None
        problem = cite and ruling_problem(root, cite, fid, clauses[fid])
        if problem:
            out.append("{}: Excludes: {} {}".format(name, fid, problem))
    return out


def spine_diff(rows, item_srs, tcs, excluded):
    """SINGLE: the item's SRs and the TCs verifying them, each with how the
    plan answers it — `cited` by a row, `excluded`, or `missing`. An item SR
    is only ever `cited` or `missing`: ch.3 §4.5 lets a TC be excluded with a
    reason, never one of the item's own SRs. Returns
    `[(ref, verified SRs or [], state)]`, SRs first; `tcs` None means no TC
    registry, so only the SRs are diffed.

    Implements: SR-155, LLR-069
    """
    named = {ref for r in rows for ref in split_refs(r["covers"])}

    def state(ref):
        return (
            "cited" if ref in named else ("excluded" if ref in excluded else "missing")
        )

    diff = [(sr, [], "cited" if sr in named else "missing") for sr in item_srs]
    for tc, verifies in sorted((tcs or {}).items()):
        hit = [sr for sr in item_srs if sr in verifies]
        if hit:
            diff.append((tc, hit, state(tc)))
    return diff


def diff_findings(name, diff):
    """SINGLE: a finding per `missing` entry of `spine_diff`.

    Implements: SR-155, LLR-069
    """
    out = []
    for ref, verified, state in diff:
        if state != "missing":
            continue
        if verified:
            out.append(
                "{}: {} verifies {} and is named by no row nor excluded".format(
                    name, ref, ", ".join(verified)
                )
            )
        else:
            out.append(
                "{}: the item's {} is cited by no row (an item SR cannot be excluded)".format(
                    name, ref
                )
            )
    return out


def _plan_section(plan, clauses):
    """One plan's report lines. `plan` is (name, rows, covered, excluded,
    diff); diff is None in a DUAL run.

    Implements: SR-155, LLR-069
    """
    name, rows, covered, excluded, diff = plan
    cov = sorted(covered, key=_clause_key)
    out = ["", "## {}".format(name), "", "- rows: {}".format(len(rows))]
    out.append(
        "- covers: {} ({}/{})".format(" ".join(cov) or "(none)", len(cov), len(clauses))
    )
    uncovered = sorted(set(clauses) - set(covered), key=_clause_key)
    out.append("- uncovered: {}".format(" ".join(uncovered) or "(none)"))
    out += ["- excluded: {} - {}".format(r, why) for r, why in excluded.items()]
    multi = {c: r for c, r in covered.items() if len(r) > 1}
    for c in sorted(multi, key=_clause_key):
        out.append(
            "- multi-covered: {} ({}) - a split reason or a duplicated "
            "scope; the rubric decides".format(c, ", ".join(multi[c]))
        )
    if diff is not None:
        out += ["", "## SR/TC diff: {}".format(name), ""]
        out += [
            "- {}{}: {}".format(
                ref, " (verifies {})".format(", ".join(v)) if v else "", state
            )
            for ref, v, state in diff
        ] or ["- (the item carries no SR)"]
    return out


def format_report(goal_name, clauses, plans):
    """The markdown coverage report: per-plan coverage + the pairwise diff.
    `plans` is [(name, rows, covered, excluded, diff)]."""
    out = ["# Plan coverage report", ""]
    out.append(
        "Goal: {} - {} clause(s): {}".format(
            goal_name, len(clauses), " ".join(sorted(clauses, key=_clause_key))
        )
    )
    for plan in plans:
        out += _plan_section(plan, clauses)
    for i in range(len(plans)):
        for j in range(i + 1, len(plans)):
            na, ca, nb, cb = plans[i][0], plans[i][2], plans[j][0], plans[j][2]
            only_a = sorted(set(ca) - set(cb), key=_clause_key)
            only_b = sorted(set(cb) - set(ca), key=_clause_key)
            both = sorted(set(ca) & set(cb), key=_clause_key)
            neither = sorted(set(clauses) - set(ca) - set(cb), key=_clause_key)
            out += [
                "",
                "## Coverage diff: {} vs {}".format(na, nb),
                "",
                "- only {}: {}".format(na, " ".join(only_a) or "(none)"),
                "- only {}: {}".format(nb, " ".join(only_b) or "(none)"),
                "- both: {}".format(" ".join(both) or "(none)"),
                "- neither: {}".format(" ".join(neither) or "(none)"),
            ]
    return "\n".join(out) + "\n"


def _clause_key(cid):
    """Clauses sort by kind, then number: D1 D2 D10 F1."""
    return (cid[:1], int(cid[1:]) if cid[1:].isdigit() else 0)


def _malformed(message):
    """A malformed run: say why and exit 2 (IF-060).

    Implements: SR-155, LLR-069
    """
    print("plan_coverage: ERROR - {}".format(message))
    sys.exit(2)


def _read(path):
    """An input file's text, or a malformed run when it does not exist.

    Implements: SR-155, LLR-069
    """
    if not path.exists():
        _malformed("{} does not exist".format(path))
    return path.read_text(encoding="utf-8")


def _declared(path, read, what):
    """The clauses `read` takes from `path`'s text; a malformed run when it
    finds none, one twice, or (findings) both shapes.

    Implements: SR-155, LLR-069
    """
    try:
        clauses = read(_read(path))
    except ValueError as e:
        _malformed(e)
    if not clauses:
        _malformed("{} declares no {}".format(path, what))
    return clauses


def load_item(item_path, findings_path):
    """SINGLE: the clauses (`D#` from the item's Done-when, then `F#` from the
    findings file) and the item's `sr_refs`.

    Implements: SR-155, LLR-069
    """
    text = _read(item_path)
    try:
        meta, _body = parse_spec_frontmatter(text, item_path.name)
    except ValueError as e:
        _malformed(e)
    clauses = {
        "D{}".format(n): item for n, item in enumerate(_done_when.items(text), 1)
    }
    if not clauses:
        _malformed(
            "{} declares no Done-when items (the plan gate's D# clauses)".format(
                item_path
            )
        )
    if findings_path:
        clauses.update(
            _declared(
                findings_path,
                finding_clauses,
                "findings (review finding lines, or lines like 'F1: ...')",
            )
        )
    return clauses, list(meta.get("sr_refs") or [])


def _parse_args():
    """The argv surface (IF-152): one of --goal / --item, then the plans.

    Implements: SR-155, LLR-069
    """
    ap = argparse.ArgumentParser(description="the plan gate (see module docstring)")
    ap.add_argument("plans", nargs="+", metavar="PLAN.md", help="plan file(s)")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--goal", help="DUAL: the goal brief (C# clauses)")
    mode.add_argument("--item", help="SINGLE: the claimed item's spec (D# clauses)")
    ap.add_argument("--findings", help="SINGLE replan: open findings (F# clauses)")
    ap.add_argument(
        "--root",
        default=".",
        help="repo root holding docs/requirements/ (default: .)",
    )
    ap.add_argument("--out", help="also write the report to this file")
    args = ap.parse_args()
    if args.findings and not args.item:
        ap.error("--findings is only valid with --item")
    return args


def _check_one(path, gate):
    """One plan's findings and its report tuple.

    Implements: SR-155, LLR-069
    """
    text = _read(path)
    rows = parse_plan(text)
    if not rows:
        _malformed(
            "{} has no Plan-WI table (the commensurability contract)".format(path)
        )
    clauses, ref_ids = gate["clauses"], gate["ref_ids"]
    findings, covered = check_plan(path.name, rows, clauses, ref_ids, gate["if_ids"])
    more, excluded = check_excludes(path.name, parse_excludes(text), clauses, ref_ids)
    findings += more
    findings += resolution_findings(path.name, excluded, gate["root"], clauses)
    findings += gap_findings(path.name, clauses, covered, excluded)
    diff = None
    if gate["item_srs"] is not None:
        diff = spine_diff(rows, gate["item_srs"], gate["tcs"], excluded)
        findings += diff_findings(path.name, diff)
    return findings, (path.name, rows, covered, excluded, diff)


def _load_gate(args):
    """The run's clauses, citable registries and (SINGLE) item SRs and TCs.

    Implements: SR-155, LLR-069
    """
    root = Path(args.root)
    req = root / "docs" / "requirements"
    gate = {
        "root": root,
        "if_ids": spine_ids(req / "interfaces.toml", "IF-ID"),
        "ref_ids": {"SR": spine_ids(req / "system-requirements.toml", "SR-ID")},
        "item_srs": None,
        "tcs": None,
    }
    if args.goal:
        gate["label"] = Path(args.goal).name
        gate["clauses"] = _declared(
            Path(args.goal),
            parse_goal,
            "clauses (lines like 'C1: ...' make plans commensurable)",
        )
        return gate
    item = Path(args.item)
    gate["label"] = item.name
    gate["clauses"], gate["item_srs"] = load_item(
        item, Path(args.findings) if args.findings else None
    )
    gate["tcs"] = verifying_tcs(root / "docs" / "test" / "test-cases.toml")
    gate["ref_ids"]["TC"] = None if gate["tcs"] is None else set(gate["tcs"])
    return gate


def main():
    _utf8_console()
    args = _parse_args()
    gate = _load_gate(args)
    findings, plans = [], []
    for p in args.plans:
        f, plan = _check_one(Path(p), gate)
        findings += f
        plans.append(plan)

    report = format_report(gate["label"], gate["clauses"], plans)
    print(report)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8", newline="\n")
    if gate["ref_ids"]["SR"] is None:
        print("plan_coverage: note - no system-requirements.csv; SR refs unvalidated")
    if gate["if_ids"] is None:
        print("plan_coverage: note - no interfaces.toml; IF refs unvalidated")
    if gate["item_srs"] is not None and gate["tcs"] is None:
        print("plan_coverage: note - no test-cases registry; the TC diff is empty")
    if findings:
        for f in findings:
            print("plan_coverage: FAIL - {}".format(f))
        sys.exit(1)
    print(
        "plan_coverage: OK - {} plan(s), {} clause(s), refs resolve.".format(
            len(plans), len(gate["clauses"])
        )
    )


if __name__ == "__main__":
    main()
