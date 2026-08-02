#!/usr/bin/env python3
"""Declared-figure provenance — a driven figure carries its command and revision
(WI-392, rung 1).

A driven figure — a test total, a census count, a measured wall-clock — is
evidence only at the revision it was driven on, and a record that omits the
command and revision leaves a stale figure indistinguishable from a live one.
Three false figures in one session (2026-08-01) each cost a review round
because a reviewer's diligence was the only detector. This check makes the
class cheap instead: a figure that OPTS IN by carrying the `fig:` marker on
its own line must name its provenance, and a marker that doesn't is flagged.

THE HONEST CLAIM IS "DECLARED FIGURES CARRY PROVENANCE", NOT "ALL FIGURES DO".
Detection was rejected deliberately: a regex over digits drowns in ids, dates,
section numbers and byte budgets (and one of the three false figures — "two
false positives" — has no digits at all), so the marker is opt-in, the kit's
usual declare-don't-infer move. An unmarked figure is out of scope by design.

The convention (one home: process-options.md "Signed measurements"; this
docstring only enforces it):

  measured   fig: cmd="<command>" rev=<revision>
             The exact command that produced the number and the revision it
             was driven at. When the figure is a count over a population, the
             command is one that ENUMERATES that population (`git log … |
             wc -l` does); a hand-picked input set names its selection
             principle inside the cmd string.
  derived    fig: derived="<how, from which declared figures>"
             A figure computed from declared figures (the remainder, the
             percentage) is itself declared — the 2026-08-01 fifth case was a
             complement mis-derived in the very paragraph explaining the
             hazard.
  exempt     a line carrying `fig-ok` is prose ABOUT the convention, never a
             declaration (the `path-ok`/`privacy-ok` idiom).

In markdown the marker rides an HTML comment so it never renders; the check is
line-based, so a `#` ini comment carries it the same way. Scan surface = root
*.md + docs/**/*.md (the check_docs surface, via check_doc_refs.doc_files, so
the two doc checks agree on it — generated trees and GENERATED marker blocks
are skipped) plus `docs/stack.ini`, whose measured budgets are the motivating
declared-numbers surface.

PRESENCE, NEVER TRUTH. The check never runs the recorded command and never
compares the figure — that is RUNG 2 (re-derivation), DELIBERATELY NOT BUILT
(WI-392, drain plan 2026-08-01 row 6): commands read out of documents are an
execution surface needing an allow-list; most figures are legitimately
historical — true at the recorded revision, different now — so re-derivation
is only valid against a revision that may not even be reachable; and some
recorded commands are expensive (tests+coverage is 634 s) or non-
deterministic. Decide rung 2 separately, after this rung shows how many
figures declare a re-runnable command. The truth of a declared figure stays
Reviewer-tier (docs/enforcement-audit.md records both the split and this
declared absence).

Ships WARN-FIRST and product-layer like check_stubs.py: exit 0 with warnings
unless --strict; NOT wired into check.py's required floor. Opt in per repo:

    [step:figures]
    command = {py} scripts/check_figures.py --strict

Stdlib only.

Contracts: IF-086, IF-087 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import re
import sys
from pathlib import Path

from check_doc_refs import authored_lines, doc_files

# The opt-in marker. `(?<![\w-])` keeps `config:` / `reconfig:` (any word
# ending in "fig") out of scope; `fig-ok` never reaches this test — the line
# exemption is checked first.
MARKER = re.compile(r"(?<![\w-])fig:")
CMD = re.compile(r'\bcmd="([^"]*)"')
REV = re.compile(r"\brev=([^\s>\"']+)")
DERIVED = re.compile(r'\bderived="([^"]*)"')
# Beside the markdown walk: the declared-budgets surface whose re-measure note
# asked a human to re-derive its numbers and had no enforcer (the WI-392
# motivating case). Line-based, so `#` comments carry the marker unchanged.
EXTRA_SURFACES = ("docs/stack.ini",)


def judge_line(line):
    """None when the declared figure carries its provenance, else the reason.

    Presence only: non-empty cmd= AND rev=, or a non-empty derived=. Empty
    values count as missing — `cmd=""` names nothing a reader could rerun."""
    derived = DERIVED.search(line)
    if derived is not None:
        if derived.group(1).strip():
            return None
        return (
            "carries an empty derivation — name the declared figures it is "
            "computed from"
        )
    cmd = CMD.search(line)
    rev = REV.search(line)
    has_cmd = bool(cmd and cmd.group(1).strip())
    has_rev = bool(rev and rev.group(1).strip())
    if has_cmd and has_rev:
        return None
    if has_cmd:
        return (
            "carries cmd= but no rev= — a figure is evidence only at the "
            "revision it was driven on"
        )
    if has_rev:
        return "carries rev= but no cmd= — name the command that produced it"
    return 'carries neither cmd="…" rev=… nor derived="…"'


def findings_for(doc, root):
    """`(findings, declared)` for one surface: the flagged marker lines and the
    count of declared figures seen (flagged or not), so the summary can always
    report how many figures are under the convention at all."""
    out, declared = [], 0
    rel = doc.relative_to(root).as_posix()
    for n, line in authored_lines(doc):
        if "fig-ok" in line:
            continue
        if not MARKER.search(line):
            continue
        declared += 1
        why = judge_line(line)
        if why:
            snippet = line.strip()
            if len(snippet) > 80:
                snippet = snippet[:77] + "…"
            out.append('{}:{}: declared figure {} — "{}"'.format(rel, n, why, snippet))
    return out, declared


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII path / quoted line can't raise UnicodeEncodeError on a legacy
    Windows cp1252 console (verbatim across the kit). Python 3.7+ streams
    expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 on a declared figure missing provenance "
        "(default: warn-first, exit 0)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()
    surfaces = doc_files(root)
    surfaces += [root / p for p in EXTRA_SURFACES if (root / p).is_file()]
    findings, declared = [], 0
    for doc in surfaces:
        found, seen = findings_for(doc, root)
        findings += found
        declared += seen
    for f in findings:
        print("check_figures: WARN - " + f, file=sys.stderr)
    if findings:
        print(
            "check_figures: {} declared figure(s) missing provenance of {} "
            "declared{}.".format(
                len(findings),
                declared,
                "" if args.strict else " (warn-first; --strict gates)",
            )
        )
        return 1 if args.strict else 0
    if declared:
        print(
            "check_figures: OK - {} declared figure(s), every one carrying its "
            "command and revision (or derivation).".format(declared)
        )
    else:
        print(
            "check_figures: OK - no declared figures (the fig: marker is "
            "opt-in; unmarked figures are out of scope by design)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
