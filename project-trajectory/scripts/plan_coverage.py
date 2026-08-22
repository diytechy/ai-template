#!/usr/bin/env python3
"""Dual-plan coverage pre-pass: make rival WI decompositions mechanically
comparable (process-options.md "Dual-plan decomposition", step 3).

Two independent planners decompose one goal into rival plans. Reviews merge
mechanically; rival plans do not — so the reconciliation is select-and-port,
and the arbiter needs an *external, computed* signal: what does each plan
cover, and what does one cover that the other misses. This checker computes
that signal. It never judges plan quality — solvability, honest coverage, and
seam duplication are the rubric's job (docs/rubrics/, the plan-critic and
arbiter hats).

    python scripts/plan_coverage.py --goal GOAL.md PLAN.md [PLAN.md ...]
                                    [--root .] [--out coverage.md]

The commensurability contract it parses:

  - the goal brief declares numbered clauses — lines like `C1: <text>`
    (optionally list-marked or bold);
  - each plan holds one markdown table with a `Plan-WI` header column:
    `| Plan-WI | Title | Covers | Interfaces | Predecessors |` — `Covers`
    cites `C#`/`SR-###` ids (`;`-separated), `Interfaces` cites `IF-###`
    ids from docs/requirements/interfaces.csv, or `Proposed:` plus a
    nearest-existing-IF rationale, or the intra-module escape.

Findings (exit 1):
    - a `Covers` cite of an undeclared clause or (when the registry exists)
      an unknown SR-###; a row citing nothing;
    - an `IF-###` cite that resolves to no interfaces.csv row; a `Proposed:`
      seam with no rationale text; an empty `Interfaces` cell with no
      intra-module escape;
    - a duplicate `Plan-WI` id, an unknown `Predecessors` id, or a
      predecessor cycle.

Uncovered clauses are the report's *payload*, never findings — showing the
gap to the critics and the arbiter is the tool's purpose. Malformed inputs
(no clauses in the goal, no plan table) exit 2.

Contracts: IF-057 — the interface seam this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

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


CLAUSE_DECL_RE = re.compile(r"^\s*(?:[-*]\s+)?\**(C\d+)\**\s*[:.]\s*(\S.*)$")
CLAUSE_REF_RE = re.compile(r"^C\d+$")
SR_REF_RE = re.compile(r"^SR-\d+$")
IF_REF_RE = re.compile(r"\bIF-\d+\b")
# The same escape hatch specs use (PROCESS.md §8): a WI acting inside one
# module states that instead of inventing a seam.
INTRA_MODULE_RE = re.compile(
    r"intra-module|single-module|no (?:cross-module )?seam|no interface", re.I
)


def parse_goal(text):
    """The goal brief's declared clauses: ordered {id: text}. Duplicate
    declarations are a malformed brief (ValueError) — ids must be citable."""
    clauses = {}
    for line in text.splitlines():
        m = CLAUSE_DECL_RE.match(line)
        if not m:
            continue
        cid = m.group(1)
        if cid in clauses:
            raise ValueError("goal brief declares {} twice".format(cid))
        clauses[cid] = m.group(2).strip()
    return clauses


def parse_plan(text):
    """The plan's proposed-WI rows from the first table whose header carries a
    `Plan-WI` column. Returns a list of dicts (id/title/covers/interfaces/
    predecessors — cells raw, split done by the caller), or [] when no such
    table exists."""
    lines = text.splitlines()
    header = None
    rows = []
    for line in lines:
        if "|" not in line:
            if header is not None and rows:
                break  # table ended
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if any(c.lower() == "plan-wi" for c in cells):
                header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue  # the |---|---| separator line
        row = dict(zip(header, cells))
        if row.get("plan-wi"):
            rows.append(
                {
                    "id": row.get("plan-wi", ""),
                    "title": row.get("title", ""),
                    "covers": row.get("covers", ""),
                    "interfaces": row.get("interfaces", ""),
                    "predecessors": row.get("predecessors", ""),
                }
            )
    return rows


def split_refs(cell):
    """Ref tokens from a table cell — ids separated by `;`, `,` or whitespace.

    The separator set matches `check_trajectory._split_refs` EXACTLY and the
    two are pinned equal by `tests/test_rule_sync.py`: this function had
    drifted to `[;,]` alone (B10 in the part-A census, 2026-08-13), so a
    whitespace-separated pair in an LLM-authored plan cell read as ONE garbage
    token and silently matched nothing — the same splitting defect class as
    the SN-001/SN-002 orphan bug OI-12 records."""
    return [t for t in re.split(r"[;,\s]+", (cell or "").strip()) if t]


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


def check_plan(name, rows, clauses, sr_ids, if_ids):
    """One plan's findings + its covered-clause set."""
    findings = []
    covered = {}  # clause id -> [row ids]
    seen = set()
    for r in rows:
        rid = r["id"]
        if rid in seen:
            findings.append("{}: duplicate Plan-WI id {}".format(name, rid))
        seen.add(rid)
        refs = split_refs(r["covers"])
        if not refs:
            findings.append(
                "{}: {} cites no clause/SR - every row must say what it "
                "covers (the commensurability contract)".format(name, rid)
            )
        for ref in refs:
            if CLAUSE_REF_RE.match(ref):
                if ref not in clauses:
                    findings.append(
                        "{}: {} cites undeclared clause {}".format(name, rid, ref)
                    )
                else:
                    covered.setdefault(ref, []).append(rid)
            elif SR_REF_RE.match(ref):
                if sr_ids is not None and ref not in sr_ids:
                    findings.append("{}: {} cites unknown {}".format(name, rid, ref))
            else:
                findings.append(
                    "{}: {} Covers cell has unparseable ref {!r} "
                    "(C# or SR-### expected)".format(name, rid, ref)
                )
        cell = r["interfaces"]
        cited = IF_REF_RE.findall(cell)
        is_proposed = re.search(r"(?i)\bproposed\b", cell)
        if cited:
            for iid in cited:
                if if_ids is not None and iid not in if_ids:
                    findings.append(
                        "{}: {} cites {} which resolves to no interfaces.toml "
                        "row".format(name, rid, iid)
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
        for p in split_refs(r["predecessors"]):
            if p not in {row["id"] for row in rows}:
                findings.append(
                    "{}: {} names unknown predecessor {}".format(name, rid, p)
                )
    cycle = find_cycle(rows)
    if cycle:
        findings.append("{}: predecessor cycle {}".format(name, " -> ".join(cycle)))
    return findings, covered


def format_report(goal_name, clauses, plans):
    """The markdown coverage report: per-plan coverage + the pairwise diff.
    `plans` is [(name, rows, covered)]."""
    out = ["# Plan coverage report", ""]
    out.append(
        "Goal: {} - {} clause(s): {}".format(
            goal_name, len(clauses), " ".join(sorted(clauses, key=_clause_key))
        )
    )
    for name, rows, covered in plans:
        out += ["", "## {}".format(name), ""]
        out.append("- rows: {}".format(len(rows)))
        cov = sorted(covered, key=_clause_key)
        out.append(
            "- covers: {} ({}/{})".format(
                " ".join(cov) or "(none)", len(cov), len(clauses)
            )
        )
        uncovered = sorted(set(clauses) - set(covered), key=_clause_key)
        out.append("- uncovered: {}".format(" ".join(uncovered) or "(none)"))
        multi = {c: r for c, r in covered.items() if len(r) > 1}
        for c in sorted(multi, key=_clause_key):
            out.append(
                "- multi-covered: {} ({}) - a split reason or a duplicated "
                "scope; the rubric decides".format(c, ", ".join(multi[c]))
            )
    for i in range(len(plans)):
        for j in range(i + 1, len(plans)):
            (na, _, ca), (nb, _, cb) = plans[i], plans[j]
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
    return int(cid[1:]) if cid[1:].isdigit() else 0


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="dual-plan coverage pre-pass (see module docstring)"
    )
    ap.add_argument("plans", nargs="+", metavar="PLAN.md", help="plan file(s)")
    ap.add_argument("--goal", required=True, help="the goal brief (C# clauses)")
    ap.add_argument(
        "--root",
        default=".",
        help="repo root holding docs/requirements/ (default: .)",
    )
    ap.add_argument("--out", help="also write the report to this file")
    args = ap.parse_args()

    goal_path = Path(args.goal)
    if not goal_path.exists():
        print("plan_coverage: ERROR - {} does not exist".format(goal_path))
        sys.exit(2)
    try:
        clauses = parse_goal(goal_path.read_text(encoding="utf-8"))
    except ValueError as e:
        print("plan_coverage: ERROR - {}".format(e))
        sys.exit(2)
    if not clauses:
        print(
            "plan_coverage: ERROR - {} declares no clauses (lines like "
            "'C1: ...' make plans commensurable)".format(goal_path)
        )
        sys.exit(2)

    req = Path(args.root) / "docs" / "requirements"
    sr_ids = spine_ids(req / "system-requirements.toml", "SR-ID")
    if_ids = spine_ids(req / "interfaces.toml", "IF-ID")

    findings, plans = [], []
    for p in args.plans:
        path = Path(p)
        if not path.exists():
            print("plan_coverage: ERROR - {} does not exist".format(path))
            sys.exit(2)
        rows = parse_plan(path.read_text(encoding="utf-8"))
        if not rows:
            print(
                "plan_coverage: ERROR - {} has no Plan-WI table (the "
                "commensurability contract)".format(path)
            )
            sys.exit(2)
        f, covered = check_plan(path.name, rows, clauses, sr_ids, if_ids)
        findings += f
        plans.append((path.name, rows, covered))

    report = format_report(goal_path.name, clauses, plans)
    print(report)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8", newline="\n")
    if sr_ids is None:
        print("plan_coverage: note - no system-requirements.csv; SR refs unvalidated")
    if if_ids is None:
        print("plan_coverage: note - no interfaces.toml; IF refs unvalidated")
    if findings:
        for f in findings:
            print("plan_coverage: FAIL - {}".format(f))
        sys.exit(1)
    print(
        "plan_coverage: OK - {} plan(s), {} clause(s), refs resolve.".format(
            len(plans), len(clauses)
        )
    )


if __name__ == "__main__":
    main()
