#!/usr/bin/env python3
"""Retired-vocabulary check: keep the retired `G*` gate tags, and the retired
`ratif*` word family (WI-499), from growing back.

OI-21 (ruled 2026-08-13) retired the `G0`/`G1`/`G2`/`G3`/`G-Release`/`G-Final`
TAGS for the eight-rung stage ladder. A second ruling (2026-08-18) retired the
`DevBar-<Label>` half of what replaced them: there is now ONE vocabulary,
`DevStg-<Label>`, and the VERB carries the axis — a repo is IN a stage and
CLEARS a stage. The three clearable stages are a strict subset of the eight
rungs, and `DevBar-Release` resolved to `DevStg-Impl`, not `DevStg-Release`. The ruling made this check a
CONDITION of the conversion, not a follow-up: "the sweep lands WITH its enforcer
or attention becomes the only thing holding 2,538 edits in place." The evidence
for that condition is on the record — the retired `at G1` construct regenerated
in this repo's own open-items registry within days of being swept out.

Stdlib only, like trace.py / check_docs.py:

    python scripts/check_vocab.py [--root .] [--strict] [--list-scope]

WHAT IT REFUSES. The TAGS, matched as whole words: `G0`, `G1`, `G2`, `G3`,
`G-Release`, `G-Final` — and, since the 2026-08-18 one-vocabulary ruling, any
`DevBar-*` token. Since WI-499 (owner-ruled 2026-08-21, "ratification holds a
weight to it that the semantics here don't need"), also any inflection of
`ratif*` (`ratify`, `ratified`, `ratification`, `ratifying`, `ratifies`,
`ratifiable`, `ratifier`, ...) — EXCEPT the literal `docs/ratify/` path, which
kept its name as a record home for the immutable dated re-attestation briefs
that already lived there; that one spelling is not retired vocabulary, it is a
directory name. Nothing else.

WHAT IT DOES NOT TOUCH — and this is the load-bearing half. **The word "gate"
survives wherever it means a check that can fail.** `test_env_gates`,
`subagent_gate`, `check_perf`'s budget gates, "the freshness gate", `docs/gate`
and `spine_rules.py` themselves are all correct English and correct filenames; a
blanket find-replace over the word would destroy working code and rename paths
adopters invoke literally. The sweep this check enforces was TAG-SCOPED, so this
check is too.

THE CARVE-OUTS, and why each one is a carve-out rather than an oversight:

  - **History is not rewritten.** `docs/archive/`, `docs/log.md`, the iteration
    logs, the review records, the dated handoffs/plans/repo-reviews, and the
    closed/cancelled WI specs are DATED RECORDS. D-4 refuses re-pointing a
    citation, and rewriting a record of what happened makes it a record of
    something else. A reader searching their own history needs the vocabulary
    that history was written in.
  - **Attestation quotes are not rewritten** — the strongest case. `docs/ratify/`
    briefs quote registry cells byte-for-byte at a pinned baseline, and the log's
    dated sign-off entries record a NAMED HUMAN approving a thing that was called
    `G1` at the time. Rewriting those makes a signed record claim something was
    signed that was not. The ruled remedy is a one-line header note naming the
    retired vocabulary, not a rewrite.
  - **Generated artifacts are not authored.** `docs/okf/`, `docs/open-items.html`
    and `PROJECT_STATE.html` regenerate from sources this check DOES cover, so
    checking them would report the same fact twice and could only ever be fixed
    upstream. `docs/gate` is generated too, and its own format migrated with the
    conversion (one forced regenerate — the proven precedent).
  - **The owner's scratchpad is nobody's working surface.**

DECLARATION SITES. Some live code must NAME the retired tags — the translation
tables that let an adopter's `--gate G2`, `gates = G2 G3` and `bar: G3` keep
working across the re-sync. Those carry an explicit marker rather than being
guessed at:

    check_vocab: allow-file     anywhere in a file  -> the whole file is exempt
    check_vocab: allow          on a line           -> that line is exempt

An explicit marker, not a heuristic like "the line also says 'retired'": a
heuristic that can be satisfied by accident is how the vocabulary grows back
through the enforcer meant to stop it.

SEVERITY IS WARN-FIRST, promoted by `--strict` (the harness wires `--strict` from
the `DevStg-Tests` bar on, exactly like `check_trajectory`). A repo mid-conversion
should see every site without being blocked; a repo past its requirements bar has
no excuse. `--list-scope` prints the scope decision for every file it considered,
so an argument about whether a surface is live or historical is settled by running
the tool rather than by reading this docstring.

Contracts: IF-118 — the interface seam this module declares (process.md §8; rows
of record in docs/requirements/interfaces.toml).
"""

import argparse
import fnmatch
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The retired TAGS, as whole words. `G-Release`/`G-Final` are matched before the
# bare digits by putting them first in the alternation.
#
# THE `DevBar-*` PREFIX JOINED THIS SET 2026-08-18 (owner ruling: one vocabulary).
# It rides the SAME regex rather than a second checker for the reason the `G*`
# tags ride one: a reader who trips either has made ONE mistake — a retired
# spelling for a live concept — and two findings for one mistake is how a checker
# gets scrolled past. The ruling that created this file made the enforcer a
# CONDITION of the sweep rather than a follow-up ("the sweep lands WITH its
# enforcer or attention becomes the only thing holding the edits in place"); that
# condition binds this sweep identically, which is why the prefix is refused in
# the same commit that converts it.
# `[g1]`/`[g2]` are refused BARE: the token has no other meaning in this repo.
# The set is EXACTLY the anchor vocabulary `check_trajectory.PHASE_ANCHOR_RE`
# accepts (`g[12]`) — there was never a `g3` anchor, and matching one would have
# been a finding with no translation to offer (see the SUGGEST pin below).
# `[reqs]`/`[tests]` are refused only in the ANCHOR POSITION (`]-[reqs]`), and
# the asymmetry is deliberate rather than tidy — those two spellings are ordinary
# English in square brackets, so a bare match reds every markdown link whose text
# happens to be "tests". A checker that cries wolf on link text is a checker
# people learn to scroll past, which is the failure this file's own docstring
# names.
RETIRED_TAG_RE = re.compile(
    r"\bG(?:-Release|-Final|0|1|2|3)\b"
    r"|\bDevBar-\w+"
    r"|\[g[12]\]"
    r"|(?<=\]-)\[(?:reqs|tests)\]"
    # WI-499 (owner-ruled 2026-08-21): "ratification holds a weight to it that
    # the semantics here don't need" — the kit's vocabulary unifies on
    # "approval". The `ratif*` word family is retired the same way the G* tags
    # were, riding the same enforcer for the same reason (one checker, one
    # mistake). Carve-outs for the ONE surviving spelling: the `docs/ratify/`
    # directory itself KEPT its name as a record home (the dated
    # re-attestation briefs already live there and are immutable), so a live
    # file naming that real path is not quoting retired vocabulary — whether
    # written as the one string `"docs/ratify/..."` (the `docs/` lookbehind),
    # as a markdown-relative link from a doc that already lives under
    # `docs/` (`ratify/2026-...-x.md`, the `/` lookahead), or as Python's
    # split-literal path-building idiom, `Path(x) / "docs" / "ratify"` (the
    # quote lookaround). Only the BARE, unsuffixed word gets these carve-outs
    # — every inflected form (`ratified`, `ratification`, ...) is never a
    # directory name.
    r"|\b(?<!docs/)(?i:ratif(?:ying|ies|ied|ication|ications|iable|ier)\w*)\b"
    r"|\b(?<!docs/)(?<![\"'])(?i:ratify)\b(?![\"'/])"
)

# The canonical replacements, printed in the finding so the fix is in the message.
SUGGEST = {
    "G0": "DevStg-Below (the internal sentinel) / DevStg-Needs (the rung)",
    "G1": "DevStg-Reqs (cleared) / DevStg-Reqs (the rung in work)",
    "G2": "DevStg-Tests (cleared) / DevStg-Tests (the rung in work)",
    "G3": "DevStg-Impl (cleared) / DevStg-Impl or DevStg-Release (the rung)",
    "G-Release": "DevStg-Impl (cleared) / DevStg-Release (the rung)",
    "G-Final": "the owner's final read (final_review), which is its own dial",
    # The prefix swap is 1:1 EXCEPT for Release, and that exception is the whole
    # reason these are spelled out rather than described as "drop the Bar".
    "DevBar-Reqs": "DevStg-Reqs",
    "DevBar-Tests": "DevStg-Tests",
    "DevBar-Below": "DevStg-Below",
    "DevBar-Release": "DevStg-Impl - NOT DevStg-Release: that bar closes the Impl "
    "rung, and DevStg-Release sits outside the derived range entirely",
    # THE PHASE-ANCHOR GRAMMAR (WI-498 slices 4-5). A phase anchor is a WI TITLE,
    # `[<phase>]-[<token>]`, and the canonical token is now the RUNG the phase
    # stands at once that anchor closes: `[4]-[DevStg-LLReqs]`.
    #
    # THESE FOUR MAPPINGS ARE REVIEWED, NOT MECHANICAL, and that is the whole
    # reason they are spelled out one by one. Three spellings are SHARED between
    # the retired bar axis and the live ladder (`DevStg-Reqs`, `DevStg-Tests`,
    # `DevStg-Impl` name a bar in one reading and a rung in the other), so
    # "translate the token to the same-named rung" is available, obvious, and
    # WRONG — it records a reach BELOW where the phase actually stands, which is
    # the failure direction that loses the event a drop detector exists to
    # report. Closing a `reqs`/`g1` anchor means the phase's SRs are authored AND
    # approved, which is the LLReqs rung — two above the token's spelling.
    #
    # `check_trajectory` TRANSLATES these on read and never rewrites a committed
    # title; what this table refuses is AUTHORING one afresh, or a live doc
    # TEACHING the retired spelling. A declaration site that must name them (the
    # translation table itself, a re-sync note) carries `check_vocab: allow`.
    "[g1]": "[DevStg-LLReqs] - the rung the phase stands at once its SRs are "
    "approved, NOT [DevStg-Reqs], which is two rungs below it",
    "[reqs]": "[DevStg-LLReqs] - same reading as [g1]; the token names what the "
    "anchor CLOSED, the rung names where the phase now stands",
    "[g2]": "[DevStg-Impl] - LLRs and TCs authored and non-Drafted, NOT "
    "[DevStg-Tests], which is one rung below it",
    "[tests]": "[DevStg-Impl] - same reading as [g2]",
}

# The `ratif*` family (WI-499) has too many inflections to spell out one by
# one the way the G* set was — this is a suffix map instead of a fixed dict,
# checked after `SUGGEST` misses (case-insensitively, keeping the finding's
# own casing out of the suggestion).
RATIF_SUGGEST_SUFFIX = {
    "ication": "approval",
    "ications": "approvals",
    "y": "approve",
    "ying": "approving",
    "ies": "approves",
    "ied": "approved",
    "iable": "approvable",
    "ier": "approver",
}


def _suggestion_for(tag):
    """The fix text for one retired-tag match: the `SUGGEST` dict for a G*/
    DevBar-* tag, or the `ratif*` suffix map (WI-499) for that family."""
    if tag in SUGGEST:
        return SUGGEST[tag]
    lower = tag.lower()
    if lower.startswith("ratif"):
        suffix = lower[len("ratif") :]
        word = RATIF_SUGGEST_SUFFIX.get(suffix)
        if word is not None:
            return '{} (WI-499 retired "ratif*" for "approv*")'.format(word)
        return 'approve/approval (WI-499 retired "ratif*" for "approv*")'
    return "(no suggestion on file — check_vocab.SUGGEST)"


# In-file markers. Kept as plain strings so a file can carry one in whatever
# comment syntax it uses.
ALLOW_FILE = "check_vocab: allow-file"
ALLOW_LINE = "check_vocab: allow"

# --- THE SCOPE, declared as data ------------------------------------------------
# Directories never scanned at all (tool/VCS noise, and vendored trees whose
# vocabulary is not ours to rule).
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    # Agent worktrees are OTHER checkouts parked under this tree — their files
    # are scanned in their own checkout, and a stale worktree must not red
    # this one (found the day the enforcer shipped: a leftover worktree's
    # scratchpad carried pre-sweep vocabulary).
    "worktrees",
    "out",
}

# HISTORICAL AND GENERATED SURFACES — the ruled carve-out, as repo-root-relative
# globs. Each entry names its class in the comment above it so a later reader can
# tell a ruled exemption from a convenient one.
EXEMPT_GLOBS = (
    # history: the kit's design archive
    "docs/archive/*",
    # history: the append-only project log, including its dated sign-off and
    # approval entries (the attestation carve-out's other half)
    "docs/log.md",
    # history: the per-branch log FRAGMENTS `trunk_step.py` compiles into
    # docs/log.md in merge order. They are the same record one merge earlier, so
    # exempting the compiled log and scanning its inputs was a boundary that only
    # held while no fragment happened to quote a retired tag (WI-498 slice 5 found
    # it the moment the anchor grammar joined the refused set — three of its own
    # slice records tripped it, correctly, for quoting what they translated).
    "docs/log.d/*",
    # citations: a rubric records the anchor it was AUTHORED at (D-4 — a WI title
    # is a citation, and a citation names the thing as it was called)
    "docs/rubrics/*",
    # attestation quotes: registry cells quoted byte-for-byte at a pinned baseline
    "docs/ratify/*",
    # history, ROW-GRANULAR: open-items.toml mixes RULED rows (records of a
    # dated decision, in the vocabulary of when it was ruled — WI-499's own
    # Context names these "records untouched") with live PENDING rows in the
    # same file. There is no row-level carve-out mechanism here (unlike a
    # whole exempt directory), and the ruled majority so outnumbers the
    # pending remainder that per-line `check_vocab: allow` marking every
    # ruled decision would be noise, not signal — the same
    # append-only-history posture `docs/log.md` gets above. A freshly
    # authored pending row is expected to use the live word on its own
    # discipline, the same as a fresh `docs/log.md` entry is.
    "docs/requirements/open-items.toml",
    # history: a partial close's spec, whose immutable report is the close event.
    # WI-504 (OI-55 ruled (a)) relocated the live population to
    # docs/archive/work/partial/* — already covered by the generic
    # "docs/archive/*" row above — but this row STAYS: it is what keeps a
    # citation of the PRE-migration path exempt (a downstream repo mid-move, or
    # this repo's own history quoting where a row used to live), the same
    # never-rewrite-history posture the sibling two rows below keep.
    "docs/work/partial/*",
    # history: closed and cancelled work-item specs (D-4 — a WI title is a
    # citation). Same WI-504 note as `docs/work/partial/*` immediately above —
    # the live population moved to docs/archive/work/*, this row stays to keep
    # a pre-migration citation exempt.
    "docs/work/complete/*",
    "docs/work/cancelled/*",
    # history: dated session transcripts and review records
    "docs/iteration/*",
    "docs/reviews/*",
    "docs/handbacks/*",
    # history: dated design documents, superseded by the live surfaces
    "docs/plans/*",
    "docs/handoff-*.md",
    "docs/repo-review-*.md",
    # generated: regenerate from sources this check does cover
    "docs/okf/*",
    "docs/open-items.html",
    "PROJECT_STATE.html",
    "docs/test/report.md",
    "docs/test/report.html",
    # generated: the derived stage record (`derive_stage.py` writes it, and its
    # own `--check` is what keeps it honest). It replaced `docs/gate` at WI-498
    # slice 5, and the swap is not just a rename in this table: the predecessor
    # was ALSO out of `TEXT_NAMES`, so `--list-scope` reported it as "not a text
    # surface" and this exemption never actually fired. Naming the successor in
    # both places is what makes the skip say WHY.
    "docs/stage",
    # owner-only, never a working surface
    "OWNER_SCRATCHPAD.md",
)

# Only these suffixes are read (plus the extensionless files named outright
# below): a binary would be noise and a lockfile is nobody's prose.
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".toml",
    ".csv",
    ".ini",
    ".yml",
    ".yaml",
    ".sh",
    ".ps1",
    ".cmd",
    ".command",
    ".html",
    ".template",
    ".txt",
    ".json",
}
# Extensionless live files that are still authored surfaces.
TEXT_NAMES = {"stage", "gate-policy", "declared-absences", "pre-commit", "pre-push"}


def is_exempt(rel):
    """True when a repo-root-relative POSIX path is a carve-out.

    A glob ending in `/*` matches the directory's whole subtree, not just its
    immediate children — `fnmatch` alone would let `docs/archive/specs/x.md`
    through, which is precisely the deep-history case the carve-out is for."""
    for pattern in EXEMPT_GLOBS:
        if fnmatch.fnmatch(rel, pattern):
            return True
        if pattern.endswith("/*") and rel.startswith(pattern[:-1]):
            return True
    return False


def in_scope(path, root):
    """`(rel, reason)` — the scope decision for one file, with the reason stated
    either way so `--list-scope` can print it."""
    rel = path.relative_to(root).as_posix()
    if set(path.relative_to(root).parts) & SKIP_DIRS:
        return rel, "skip: tool/VCS directory"
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
        return rel, "skip: not a text surface"
    if is_exempt(rel):
        return rel, "exempt: historical or generated (carve-out)"
    return rel, "LIVE"


def findings_for(text, rel):
    """The retired-tag findings in one file's text, one per offending line.

    ONE FINDING PER LINE, not per tag: a line naming `G1`, `G2` and `G3` is one
    sentence to rewrite, and three findings would make the report look three times
    worse than the work is."""
    if ALLOW_FILE in text:
        return []
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        if ALLOW_LINE in line:
            continue
        tags = RETIRED_TAG_RE.findall(line)
        if not tags:
            continue
        first = tags[0]
        out.append(
            "{}:{}: retired vocabulary {} — use {} (OI-21 retired the G* tags, "
            'WI-499 retired "ratif*"; if this line must quote the retired '
            "vocabulary, mark it `{}`)".format(
                rel, n, "/".join(sorted(set(tags))), _suggestion_for(first), ALLOW_LINE
            )
        )
    return out


def scan(root, list_scope=False):
    """`(findings, scanned_count)` over the whole tree."""
    root = Path(root).resolve()
    findings, scanned = [], 0
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel, reason = in_scope(path, root)
        if reason != "LIVE":
            if list_scope and not reason.startswith("skip: tool"):
                print("  {:<8} {}".format("skip", rel))
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        scanned += 1
        if list_scope:
            print("  {:<8} {}".format("live", rel))
        findings.extend(findings_for(text, rel))
    return findings, scanned


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="promote findings from WARN to ERROR (exit 1). The harness wires "
        "this from the DevStg-Tests bar on, like check_trajectory.",
    )
    ap.add_argument(
        "--list-scope",
        action="store_true",
        help="print the live/skip decision for every file considered, then the "
        "findings — so a scope argument is settled by running the tool",
    )
    args = ap.parse_args()

    findings, scanned = scan(args.root, args.list_scope)
    label = "check_vocab: ERROR" if args.strict else "check_vocab: WARN"
    for f in findings:
        print("{} - {}".format(label, f))
    if not findings:
        print(
            "check_vocab: clean ({} live authored file(s); no retired gate "
            "tags).".format(scanned)
        )
        return 0
    print(
        "check_vocab: {} finding(s) across {} live authored file(s){}".format(
            len(findings), scanned, "" if args.strict else " (warn-first)"
        )
    )
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
