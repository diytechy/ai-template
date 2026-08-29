#!/usr/bin/env python3
"""Design-time runtime-flow check: the DevStg-Tests reviewer reads diagrams, not CSV rows.

The derived architecture views exist only once code exists (DevStg-Impl+). But the
behavior most often misread at DevStg-Tests — concurrency, background work, what blocks
on what — is decided *with the LLRs*. So PROCESS.md §3 requires a hand-authored
**"Runtime flows"** section in `docs/runtime-flows.md` at DevStg-Tests: Mermaid
sequence diagrams of the key runtime scenarios, each citing the SR/LLR ids it
renders, so a human can verify intended behavior by reading the flow instead of
inferring it from registry rows. (The flows doc is the authored-narrative half
of the architecture record; it lived inside the retired `docs/architecture.md`
until the sitting-2 decision-8 program moved it — the obligation follows the
home, it does not die with the file. The dashboard embeds the flows.)

This checker keeps that section honest (stdlib only, like trace.py):

    python scripts/check_flows.py [--doc docs/runtime-flows.md] [--docs docs]
                                  [--require N] [--no-placeholders]

Failures (exit 1):
    - the doc has no "Runtime flows" section heading *inside* it (the document
      title does not count, so a doc merely NAMED "Runtime flows" whose section
      was deleted fails, as it must);
    - the section contains fewer than N (default 1) ```mermaid blocks;
    - a diagram cites no SR/LLR id at all (flows must stay traceable);
    - a cited SR/LLR/SN/TC id does not exist in the registries.

Placeholder ids ending in "-000" (the templates' examples) satisfy the
"cites an id" rule and are never validated, so a fresh scaffold starts green.
--no-placeholders (wire it in from DevStg-Tests on) instead *flags* every cited "-000"
id, so a real authored flow can't keep citing the template's example ids.

Contracts: IF-003 — the interface seam this module declares (process.md §8; row of record in docs/requirements/interfaces.toml).

Contract IF-003: the harness runs this CLI as one gate step and reads its exit
    code: 0 the Runtime flows section is present, carries at least `--require`
    mermaid diagrams, every diagram cites an SR or LLR id, and every cited
    SR/LLR/SN/TC id exists in the registries; 1 any of those fails, with one
    `check_flows: FAIL - ...` line per problem naming it; 2 a usage error. A
    missing doc and a doc whose section heading was deleted both fail — the
    document TITLE does not satisfy the heading — so the step cannot pass by
    finding nothing to check. `-000` placeholder ids satisfy the cites-an-id
    rule and are never validated, until `--no-placeholders` flags them instead.
"""

import argparse
import csv
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


def _headings(lines):
    """`[(line index, level, lowercased title)]` for every ATX heading."""
    out = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip().lower()))
    return out


def flows_section(text):
    """Return the 'Runtime flows' section body, or None when the section is
    absent.

    The document's own TITLE never counts as the section — the first heading in
    the file is skipped. Otherwise a doc *titled* "Runtime flows" (both this
    repo's and the shipped template's are) would have its title heading swallow
    the whole file, and the gate could never fail on a deleted flows section:
    any stray mermaid block anywhere in the doc would satisfy it. So a doc
    titled "Runtime flows" must still carry a Runtime-flows *section* inside it.

    Among the remaining candidates an exact "Runtime flows" heading wins over a
    longer "Runtime flows ..." one; ties go to the first in file order. The
    section runs to the next heading of the same or higher level."""
    lines = text.splitlines()
    # [1:] drops the document title - see the docstring; this one slice is what
    # makes a deleted section fail on a doc that is *named* for the section.
    cands = [h for h in _headings(lines)[1:] if h[2].startswith(SECTION_TITLE)]
    if not cands:
        return None
    exact = [h for h in cands if h[2] == SECTION_TITLE]
    head, level = (exact or cands)[0][:2]
    start = head + 1
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
        default="docs/runtime-flows.md",
        help="doc holding the Runtime flows section (default: docs/runtime-flows.md)",
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
        help="flag cited '-000' template ids instead of ignoring them (DevStg-Tests on)",
    )
    args = ap.parse_args()

    doc = Path(args.doc)
    if not doc.exists():
        print(f"check_flows: FAIL - {doc} does not exist")
        sys.exit(1)

    section = flows_section(doc.read_text(encoding="utf-8"))
    if section is None:
        print(
            f'check_flows: FAIL - no "Runtime flows" section heading in {doc} '
            "(the document TITLE does not count - the section must be a heading "
            "inside the doc; required at DevStg-Tests; see process.md §3 "
            "'Design-time runtime flows')"
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
