#!/usr/bin/env python3
"""Design-time runtime-flow check: the DevBar-Tests reviewer reads diagrams, not CSV rows.

The generated code map and `--flow` exist only once code exists (DevBar-Release+). But the
behavior most often misread at DevBar-Tests — concurrency, background work, what blocks
on what — is decided *with the LLRs*. So PROCESS.md §3 requires a hand-authored
**"Runtime flows"** section in the architecture doc at DevBar-Tests: Mermaid sequence
diagrams of the key runtime scenarios, each citing the SR/LLR ids it renders,
so a human can verify intended behavior by reading the flow instead of
inferring it from registry rows.

This checker keeps that section honest (stdlib only, like trace.py):

    python scripts/check_flows.py [--doc docs/architecture.md] [--docs docs]
                                  [--require N] [--no-placeholders]

Failures (exit 1):
    - the doc has no "Runtime flows" heading;
    - the section contains fewer than N (default 1) ```mermaid blocks;
    - a diagram cites no SR/LLR id at all (flows must stay traceable);
    - a cited SR/LLR/SN/TC id does not exist in the registries.

Placeholder ids ending in "-000" (the templates' examples) satisfy the
"cites an id" rule and are never validated, so a fresh scaffold starts green.
--no-placeholders (wire it in from DevBar-Tests on) instead *flags* every cited "-000"
id, so a real authored flow can't keep citing the template's example ids.

Contracts: IF-003, IF-029, IF-105 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import re
import sys
from pathlib import Path

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


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII heading echoed in a finding can't raise UnicodeEncodeError on a
    legacy Windows cp1252 console. Python 3.7+ streams expose `.reconfigure`;
    guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


ID_RE = re.compile(r"\b(SR|LLR|SN|TC)-\d+\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SECTION_TITLE = "runtime flows"


def load_ids(docs):
    """Collect the known ids per kind from the registries (trace.py's sources)."""

    def col(path, key):
        if not path.exists():
            return set()
        with path.open(newline="", encoding="utf-8-sig") as f:
            return {r[key] for r in csv.DictReader(f) if r.get(key)}

    def spine_col(path, key):
        """The id set of a spine tier, through the carrier, so it answers
        whichever of TOML/CSV is live. Under TOML the ids are the
        TABLE KEYS, so this is the one reader that needs no column vocabulary
        at all."""
        return {r[key] for r in spine_carrier.load(path, key) if r.get(key)}

    known = {
        "SR": spine_col(docs / "requirements" / "system-requirements.toml", "SR-ID"),
        "LLR": spine_col(
            docs / "requirements" / "low-level-requirements.toml", "LLR-ID"
        ),
        "TC": spine_col(docs / "test" / "test-cases.toml", "TC-ID"),
        "SN": set(),
    }
    # The need tier resolves through the carrier too. The id
    # SCRAPE itself is carrier-blind — `SN-001` is the token under a markdown
    # row and under `[need.SN-001]` alike — but an existence test on one suffix
    # is not: it would report an EMPTY known-SN set for a repo still on
    # markdown, and every `SN-###` a runtime flow cites would read as unknown.
    sn_md = spine_carrier.resolve(
        docs / "requirements" / "stakeholder-needs.toml", spine_carrier.NEED_CARRIERS
    )
    if sn_md is not None:
        known["SN"] = set(re.findall(r"\bSN-\d+\b", sn_md.read_text(encoding="utf-8")))
    return known


def flows_section(text):
    """Return the 'Runtime flows' section body, or None when the heading is
    absent. The section runs to the next heading of the same or higher level."""
    lines = text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and m.group(2).strip().lower().startswith(SECTION_TITLE):
            start, level = i + 1, len(m.group(1))
            break
    if start is None:
        return None
    for j in range(start, len(lines)):
        m = HEADING_RE.match(lines[j])
        if m and len(m.group(1)) <= level:
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


def mermaid_blocks(section):
    """The ```mermaid fenced blocks inside the section, in order."""
    return re.findall(r"```mermaid\s*\n(.*?)```", section, flags=re.DOTALL)


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--doc",
        default="docs/architecture.md",
        help="doc holding the Runtime flows section (default: docs/architecture.md)",
    )
    ap.add_argument("--docs", default="docs", help="docs directory (default: docs)")
    ap.add_argument(
        "--require",
        type=int,
        default=1,
        metavar="N",
        help="minimum number of flow diagrams (default: 1)",
    )
    ap.add_argument(
        "--no-placeholders",
        action="store_true",
        help="flag cited '-000' template ids instead of ignoring them (DevBar-Tests on)",
    )
    args = ap.parse_args()

    doc = Path(args.doc)
    if not doc.exists():
        print(f"check_flows: FAIL - {doc} does not exist")
        sys.exit(1)

    section = flows_section(doc.read_text(encoding="utf-8"))
    if section is None:
        print(
            f'check_flows: FAIL - no "Runtime flows" heading in {doc} '
            "(required at DevBar-Tests; see process.md §3 'Design-time runtime flows')"
        )
        sys.exit(1)

    blocks = mermaid_blocks(section)
    problems = []
    if len(blocks) < args.require:
        problems.append(
            f"section has {len(blocks)} mermaid diagram(s); {args.require} required"
        )

    known = load_ids(Path(args.docs))
    for n, block in enumerate(blocks, 1):
        kinds = {m.group(1) for m in ID_RE.finditer(block)}
        if not kinds & {"SR", "LLR"}:
            problems.append(
                f"diagram {n} cites no SR/LLR id - every flow must say which "
                "requirements it renders"
            )
    for m in ID_RE.finditer(section):
        rid, kind = m.group(0), m.group(1)
        if rid.endswith("-000"):
            if args.no_placeholders:
                problems.append(
                    f"placeholder id still cited: {rid} (replace the template "
                    "example flow with real SR/LLR ids before this gate)"
                )
            continue  # otherwise a template placeholder - never validated
        if rid not in known[kind]:
            problems.append(f"unknown id cited: {rid}")

    if problems:
        for p in sorted(set(problems)):
            print(f"check_flows: FAIL - {p}")
        sys.exit(1)
    cited_total = len({m.group(0) for m in ID_RE.finditer(section)})
    print(
        f"check_flows: OK - {len(blocks)} flow diagram(s), "
        f"{cited_total} requirement id(s) cited, all known."
    )


if __name__ == "__main__":
    main()
