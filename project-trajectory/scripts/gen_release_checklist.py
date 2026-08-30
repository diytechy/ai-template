#!/usr/bin/env python3
"""Generate the human release checklist from the registries.

Stack-agnostic kit, stdlib-only (Python 3.11+). Most of the harness is machine-
checkable, but a release still needs a human to *exercise the real product* —
the Demonstration / Manual / Inspection items that no automated test can honestly
cover (the owner's final read in process.md). This script collects exactly those, back-linked to
their requirement ids, into a tick-box checklist so the release sign-off is
concrete and traceable instead of a vibe.

It pulls, from `docs/`:
    - Stakeholder needs (SN) + their acceptance intent -> "Does the product meet the need?"
    - System requirements whose Verification is Demonstration / Manual / Inspection
    - Release-tier test cases, and any non-automated (manual) test cases
    - Provided cross-project interfaces (IF, if present) -> contract still honored?
    - Performance budgets (PB, if present) -> still within allocation? (§9; the
      warn-tier runtime budgets never fail the gate, so a human confirms them here)

Each line is `- [ ] <ID> — <what to confirm> (refs)`. The output is a *generated
record*: regenerate it per release and keep the ticked copy as the sign-off
artifact (use --version to file it under docs/releases/).

Usage:
    python scripts/gen_release_checklist.py [--docs docs] [--version X]
                                            [--phase LIST] [--out PATH]

    --version  Stamp the checklist and write to docs/releases/checklist-<X>.md.
    --phase    Phased delivery (process.md §4): include only SRs whose Phase is
               blank or listed (e.g. v1 or v1,v2), and only the release-tier /
               manual TCs that verify an in-scope SR (or an LLR under one).
    --out      Explicit output path (overrides the default/--version location).
    default    Writes docs/release-checklist.md.

Contracts: IF-018 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-018: the human release checklist, written as a Markdown document
    whose every item is `- [ ] <ID> — <what to confirm> (refs)`. It collects
    exactly the rows a machine cannot honestly close: stakeholder needs and
    their acceptance intent, system requirements whose Verification is
    Demonstration, Manual or Inspection, release-tier and manual test cases,
    the declared interface seams, and the performance budgets whose runtime
    tier never fails a gate. `--phase` narrows to the listed phases while the
    foundation phase is never deferred; `--version` files the output under
    `docs/releases/checklist-<X>.md`, `--out` overrides the path, and the
    default is `docs/release-checklist.md`. Every optional registry is
    absent-tolerant, so a repo without one simply has no section for it. The
    output is a generated RECORD: regenerate it per release and keep the ticked
    copy as the sign-off artifact.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The spine ROW vocabulary — the `-000` placeholder test.
from kitlib import spine as _kitspine

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

HUMAN_METHODS = {"Demonstration", "Manual", "Inspection"}


def load_csv(path):
    """The off-spine rows of a registry CSV, `[]` when absent; a leading `#`
    declaration header is skipped by the one shared reader."""
    if not path.exists():
        return []
    return _kitspine.csv_rows(path.read_text(encoding="utf-8-sig"))


# The `-000` placeholder-row convention. THE THIRD HOME, retired at WI-448
# slice 4: `kitlib.spine.is_example` is the one the pair already shares, and
# `tests/test_rule_sync.py` had to pin this copy against it by value — including
# a `None` case, because one of the three copies used to crash on it.
is_example = _kitspine.is_example


def read_stakeholder_needs(md_path):
    """`(SN-ID, need, acceptance)` per need, through the CARRIER.

    Was a bespoke markdown table parse that discovered its own `Need` and
    `Acceptance` columns by header text. Under one carrier those are fields, and
    the edge-case fold — which this reader never had, so an edge row's need read
    as its Lifecycle word here too — comes from the single home the fold now
    has."""
    return [
        (n["id"], n["need"], n["acceptance"])
        for n in spine_carrier.folded_needs(md_path)
    ]


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--version", default=None)
    ap.add_argument(
        "--phase",
        default=None,
        help="comma-separated phases in scope (blank Phase = every phase)",
    )
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    docs = Path(args.docs)

    needs = read_stakeholder_needs(docs / "requirements" / "stakeholder-needs.toml")
    srs = [
        r
        for r in spine_carrier.load(
            docs / "requirements" / "system-requirements.toml", "SR-ID"
        )
        if r.get("SR-ID") and not is_example(r["SR-ID"])
    ]
    tcs = [
        r
        for r in spine_carrier.load(docs / "test" / "test-cases.toml", "TC-ID")
        if r.get("TC-ID") and not is_example(r["TC-ID"])
    ]
    ifs = [
        r
        for r in spine_carrier.load(docs / "requirements" / "interfaces.toml", "IF-ID")
        if r.get("IF-ID") and not is_example(r["IF-ID"])
    ]
    # Performance budgets (process.md §9): the warn-tier runtime budgets never
    # fail the gate, so the release checklist is where a human confirms them.
    pbs = [
        r
        for r in load_csv(docs / "requirements" / "performance-budgets.csv")
        if r.get("PB-ID") and not is_example(r["PB-ID"])
    ]

    phases = (
        {p for p in re.split(r"[;,\s]+", args.phase.strip()) if p}
        if args.phase
        else None
    )

    def _phase_num(tag):
        m = re.search(r"\d+", tag or "")
        return int(m.group()) if m else None

    # The foundation (minimum) phase is never phase-deferred (the phase doctrine,
    # process.md §4) — the same rule trace.py's --phase filter applies, so a foundation
    # SR stays on the release checklist under any --phase. Digit-parse (`v2`/`2` -> 2)
    # so the minimum compares numerically; an all-blank registry has no parseable phase
    # and the blank rule carries it unchanged.
    foundation_phase = min(
        (
            n
            for n in (_phase_num((r.get("Phase") or "").strip()) for r in srs)
            if n is not None
        ),
        default=None,
    )

    def in_phase(sr_row):
        tag = (sr_row.get("Phase") or "").strip()
        if phases is None or not tag or tag in phases:
            return True
        n = _phase_num(tag)
        return n is not None and n == foundation_phase

    in_scope_sr_ids = {r["SR-ID"] for r in srs if in_phase(r)}
    # An LLR is in scope when any of its parent SRs is, so TC `Verifies` cells
    # that cite only LLR ids still resolve to the right phase.
    llrs = [
        r
        for r in spine_carrier.load(
            docs / "requirements" / "low-level-requirements.toml", "LLR-ID"
        )
        if r.get("LLR-ID") and not is_example(r["LLR-ID"])
    ]
    in_scope_ids = set(in_scope_sr_ids)
    for r in llrs:
        parents = [p for p in re.split(r"[;,\s]+", r.get("SR-Refs", "")) if p]
        if any(p in in_scope_sr_ids for p in parents):
            in_scope_ids.add(r["LLR-ID"])

    def tc_in_scope(tc_row):
        cited = [x for x in re.split(r"[;,\s]+", tc_row.get("Verifies", "")) if x]
        return phases is None or any(x in in_scope_ids for x in cited)

    human_srs = [
        r for r in srs if r.get("Verification", "") in HUMAN_METHODS and in_phase(r)
    ]
    # A blank Automated cell intentionally counts as manual: an unclassified test
    # must show up on the human checklist rather than silently drop off it.
    manual_tcs = [
        r
        for r in tcs
        if (
            r.get("Tier", "") == "Release"
            or (r.get("Automated", "").strip().lower() in ("no", "false", ""))
        )
        and tc_in_scope(r)
    ]
    # A cross-project contract is a seam this tree OWNS and an `external:`
    # party reads (OI-67: the row is owner -> consumers, and there is no
    # direction column to key on).
    provided_ifs = [
        r
        for r in ifs
        if not (r.get("Owner") or "").strip().startswith("external:")
        and any(
            c.strip().startswith("external:")
            for c in (r.get("Requestors") or r.get("Consumers") or "").split(";")
        )
    ]

    stamp = args.version or "(unreleased)"
    if phases:
        stamp += " — phase {}".format(args.phase)
    today = datetime.date.today().isoformat()
    L = [
        "# Release Checklist — {}".format(stamp),
        "",
        "_Generated by `scripts/gen_release_checklist.py` on {}. Tick each box "
        "after exercising the real product; keep the completed copy as the "
        "DevStg-Impl sign-off record._".format(today),
        "",
        "- Version / build under test: __________   Date: __________   "
        "Signed-off by: __________",
        "",
    ]

    L += ["## 1. Stakeholder needs met (acceptance)", ""]
    if needs:
        for uid, need, acc in needs:
            detail = acc or need or "confirm the need is met"
            L.append("- [ ] **{}** — {} ({})".format(uid, detail, uid))
    else:
        L.append("- [ ] _(no stakeholder needs registered)_")

    L += [
        "",
        "## 2. Human-verified requirements (Demonstration / Manual / Inspection)",
        "",
    ]
    if human_srs:
        for r in human_srs:
            L.append(
                "- [ ] **{}** [{}] — {} (AcceptanceCriteria of {})".format(
                    r["SR-ID"],
                    r.get("Verification", ""),
                    r.get("Title", "").strip(),
                    r["SR-ID"],
                )
            )
    else:
        L.append("- [ ] _(every requirement is automated — nothing manual to verify)_")

    L += ["", "## 3. Release-tier & manual test cases", ""]
    if manual_tcs:
        for r in manual_tcs:
            L.append(
                "- [ ] **{}** [{}] — {} (verifies {})".format(
                    r["TC-ID"],
                    r.get("Tier", "") or "Manual",
                    r.get("Method", "").strip(),
                    r.get("Verifies", ""),
                )
            )
    else:
        L.append("- [ ] _(no release-tier or manual test cases)_")

    if provided_ifs:
        L += ["", "## 4. Cross-project contracts still honored", ""]
        for r in provided_ifs:
            L.append(
                "- [ ] **{}** ({} {}) — {} still satisfies the published "
                "contract ({} to {})".format(
                    r["IF-ID"],
                    r.get("Version", ""),
                    r.get("Status", ""),
                    r.get("Owner", ""),
                    r.get("Channel", ""),
                    r.get("Requestors") or r.get("Consumers", ""),
                )
            )

    if pbs:
        L += ["", "## 5. Performance budgets within allocation (§9)", ""]
        for r in pbs:
            arrow = "≤" if (r.get("Direction") or "").strip() == "lower-better" else "≥"
            L.append(
                "- [ ] **{}** — {} {} {}{} ({}; refs {})".format(
                    r["PB-ID"],
                    r.get("Metric", "").strip(),
                    arrow,
                    r.get("Budget", "").strip(),
                    r.get("Unit", "").strip(),
                    r.get("Gate", "").strip() or "warn",
                    r.get("Refs", "").strip(),
                )
            )

    L += [
        "",
        "## 6. Release hygiene",
        "",
        "- [ ] `python scripts/check.py --stage DevStg-Impl --tier release` is green "
        "(paste the output in the audit log).",
        "- [ ] CHANGELOG / release notes updated.",
        "- [ ] Version bumped; any changed `Approved` interface versions "
        "communicated to counterparts.",
        "- [ ] Docs (README / quick-reference) match the shipped behavior.",
        "- [ ] README `sn-inventory` bullets still reflect the current "
        "stakeholder needs (wording, not just ids — the gate checks ids).",
        "",
    ]

    if args.out:
        out = Path(args.out)
    elif args.version:
        out = docs / "releases" / "checklist-{}.md".format(args.version)
    else:
        out = docs / "release-checklist.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

    print(
        "Release checklist -> {}  (SN={} human-SR={} manual-TC={} IF={} PB={})".format(
            out,
            len(needs),
            len(human_srs),
            len(manual_tcs),
            len(provided_ifs),
            len(pbs),
        )
    )


if __name__ == "__main__":
    main()
