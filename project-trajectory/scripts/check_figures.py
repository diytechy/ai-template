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
  grammar    a marker whose values are wholly placeholder tokens (`<command>`,
             `…`) is the convention quoting itself and declares nothing — ALL
             of its values (WI-409): a MIXED marker, one real value beside an
             unfilled `rev=<revision>`, is a real half-filled declaration
             judged on completeness, its placeholder value counting as
             ABSENT; a metacharacter inside a longer value (`sort < in.txt`)
             is command text, and the marker is judged (WI-404); each marker
             on a line owns only the attributes that follow it, so two
             half-carrying markers never cross-satisfy; rev= takes a bare
             token or a quoted string, and its value must carry a word
             character (a flush `rev=-->` is punctuation, not a revision).
             Recorded corner (WI-404 REVIEW-A note 2): the unclosed-token
             alternative exists for the bare rev= capture but applies per
             value, so a marker ALL of whose values are whitespace-free
             `<`-leading tokens (a lone `cmd="<in.txt"`) is excused — no
             runnable command has that shape.

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

Contracts: IF-086, IF-087 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import re
import sys
from pathlib import Path

from check_doc_refs import authored_lines, doc_files

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The opt-in marker. `(?<![\w-])` keeps `config:` / `reconfig:` (any word
# ending in "fig") out of scope; `fig-ok` never reaches this test — the line
# exemption is checked first.
MARKER = re.compile(r"(?<![\w-])fig:")
CMD = re.compile(r'\bcmd="([^"]*)"')
# rev= takes a bare token or a quoted string (REVIEW-A finding 2: the quoted
# form used to fail closed). Backticks are excluded from the bare form so
# prose naming `rev=` never reads as a value, and the captured value must
# still carry a word character (judge_marker) so a flush `rev=-->` cannot
# pass on punctuation debris.
REV = re.compile(r"\brev=(?:\"([^\"]*)\"|([^\s>\"'`]+))")
DERIVED = re.compile(r'\bderived="([^"]*)"')
# A marker ALL of whose values are placeholder-shaped is GRAMMAR PROSE quoting
# the convention (`<command>`, `…`), not a declaration — the check_doc_refs
# `{placeholder}`/`NNN` stance (REVIEW-A finding 1: the convention text ships
# in every scaffold and must not read as undeclared figures there). A value is
# placeholder-shaped only when the WHOLE value is the convention's own example
# grammar: an angle-bracket-wrapped token (`<command>`, `<how, from which
# declared figures>`; the bare rev= capture stops before `>`, so a
# whitespace-free token may arrive without its closing bracket) or the bare
# ellipsis. A metacharacter INSIDE a longer value is legitimate command text
# (`pytest -q 2>&1 | tail -1`, `sort < in.txt`), so the marker is judged on
# its own attributes — the old any-char proxy excused defective markers and
# uncounted real redirecting declarations, both silently (WI-404, REVIEW-A
# round-2 finding 4). One placeholder beside a real value does NOT excuse the
# marker (WI-404 REVIEW-A finding 1): the half-filled template is judged, its
# unfilled field counting as absent (WI-409).
PLACEHOLDER_VALUE = re.compile(r"…|<[^<>]*>|<[^<>\s]*")
WORD = re.compile(r"[0-9A-Za-z]")
# Beside the markdown walk: the declared-budgets surface whose re-measure note
# asked a human to re-derive its numbers and had no enforcer (the WI-392
# motivating case). Line-based, so `#` comments carry the marker unchanged.
EXTRA_SURFACES = ("docs/stack.ini",)
# A verdict record quotes findings — including bare and half-carrying markers
# — verbatim as evidence, and judging the quotation convicts the quoter: every
# branch a review lands on would red on the review's own repro lines. Reviews
# are records, not declaration surfaces (the check_doc_refs record stance),
# so they are out of scope by design. The log is deliberately NOT here: its
# watched totals are exactly the figures this convention exists to cover.
SKIP_PREFIXES = ("docs/reviews/",)


# The sentinel judge_marker returns for grammar prose: the marker declares
# nothing, so it neither flags nor counts toward the declared-figures census.
GRAMMAR_EXAMPLE = "placeholder-grammar example"


def marker_segments(line):
    """The text each `fig:` marker on a line owns: from its own match to the
    next marker (or end of line). Judged separately (REVIEW-A finding 2), so
    a cmd=-only marker and a rev=-only marker on one line are two findings,
    never one cross-satisfied declaration."""
    ms = list(MARKER.finditer(line))
    return [
        line[m.end() : ms[i + 1].start()] if i + 1 < len(ms) else line[m.end() :]
        for i, m in enumerate(ms)
    ]


def _placeholder(value):
    """Whether the WHOLE value is the convention's own example grammar — an
    unfilled field. Judged twice: every value placeholder-shaped makes the
    marker grammar prose; one inside a judged marker counts as absent."""
    return bool(PLACEHOLDER_VALUE.fullmatch(value.strip()))


def judge_marker(segment):
    """None when the declared figure carries its provenance, GRAMMAR_EXAMPLE
    when the marker is convention prose, else the flag reason.

    Presence only: non-empty cmd= AND rev=, or a non-empty derived=. Empty or
    wordless values count as missing — `cmd=""` names nothing a reader could
    rerun, and a flush `rev=-->` is punctuation, not a revision. A marker is
    example grammar only when ALL its values are placeholders (`<command>`,
    `…` — each the whole value, PLACEHOLDER_VALUE): grammar quoted in prose
    declares nothing, but a MIXED marker — one real value beside an unfilled
    `<token>` — is a real, half-filled declaration (WI-409). In that judgment
    a placeholder-shaped value counts as ABSENT, never as satisfying: the
    bare rev= capture arrives unclosed (`<revision`), which carries word
    characters and would otherwise pass the half-filled template as
    complete. A metacharacter inside a longer value is command text, and the
    marker is judged (WI-404)."""
    derived = DERIVED.search(segment)
    cmd = CMD.search(segment)
    rev = REV.search(segment)
    rev_val = None
    if rev:
        rev_val = rev.group(1) if rev.group(1) is not None else rev.group(2)
    values = [
        v
        for v in (
            cmd.group(1) if cmd else None,
            rev_val,
            derived.group(1) if derived else None,
        )
        if v is not None
    ]
    if values and all(_placeholder(v) for v in values):
        return GRAMMAR_EXAMPLE
    if derived is not None and not _placeholder(derived.group(1)):
        if derived.group(1).strip():
            return None
        return (
            "carries an empty derivation — name the declared figures it is "
            "computed from"
        )
    has_cmd = bool(cmd and cmd.group(1).strip() and not _placeholder(cmd.group(1)))
    has_rev = bool(rev_val and WORD.search(rev_val) and not _placeholder(rev_val))
    if has_rev and rev_val.strip().endswith("-dirty"):
        # A DIRTY REV IS NOT A REVISION (ROUND-SOL-RAW 9). `git describe`-style
        # `<sha>-dirty` names a working tree that existed on one machine for a
        # few minutes and cannot be checked out, so the figure it stamps is not
        # reproducible by the reader it exists for — which is the whole content
        # of the convention. Presence is satisfied and provenance is not, so
        # this is judged rather than waved through.
        return (
            "carries a DIRTY rev ({}) — `<sha>-dirty` is a working tree, not a "
            "tree anyone can check out, so the figure cannot be reproduced. "
            "Commit first and stamp the resulting revision, or re-drive the "
            "figure at a committed one".format(rev_val.strip())
        )
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
        for segment in marker_segments(line):
            why = judge_marker(segment)
            if why is GRAMMAR_EXAMPLE:
                continue  # convention prose — declares nothing, counts nothing
            declared += 1
            if why:
                snippet = line.strip()
                if len(snippet) > 80:
                    snippet = snippet[:77] + "…"
                out.append(
                    '{}:{}: declared figure {} — "{}"'.format(rel, n, why, snippet)
                )
    return out, declared


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
    surfaces = [
        d
        for d in doc_files(root)
        if not d.relative_to(root).as_posix().startswith(SKIP_PREFIXES)
    ]
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
