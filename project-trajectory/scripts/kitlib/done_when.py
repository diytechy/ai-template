"""A lane's Done-when, fixed at claim: what an item IS, and what counts as a CHANGE.

WHY THIS EXISTS (owner ruling S13, 2026-09-24; review pack B3). A reviewer maps
each Done-when item to its covering test, so the list is the checklist a lane
is judged against - and nothing stopped the lane being judged from rewriting
it. Across the repository's history builders edited their own Done-when in 14
commits over 10 work items, and three of those changed what it meant: one
weakened an item and ticked it, one redefined one, one narrowed one (caught by a
review round and reverted). Two rules answer it, and no new role:

  * every claimable work item HAS a Done-when, written before claim by whoever
    files it (`has_done_when`, read by the claim);
  * at merge, each item's text AT CLAIM is compared with its text AT MERGE,
    ticks and trailing evidence stripped, and any change is flagged to the
    reviewer and the adjudicator (`changes`, read by the reviewer's brief and
    by the merge-time mint).

TICKING WITH EVIDENCE IS THE NORMAL CONVENTION, so a comparison that fired on
every tick would be noise: `- [x] item`, `~~item~~ - LANDED ...` and
`item. (tests/test_x.py::test_y)` all read as the item unchanged. EVIDENCE IS
A FORM, the one the repository's closed specs use: text appended after the item
that opens with an evidence separator (a dash, an arrow, a bracket, a bar or a
check mark) AND carries an evidence token - a completion word in capitals
(LANDED, DONE, MET, VERIFIED, SHIPPED, PASSED, FIXED, COVERED), a path or test
id, a backticked name, or a commit sha. Anything else appended is prose, and
prose is a rewording, because that is how an item gets narrowed: `Tests pass.`
becoming `Tests pass. Only on Linux.` or `Tests pass (only on Linux)` flags,
closing punctuation or not. The rule is a reading, not a proof - `DONE except
on Windows` still reads as evidence - and the reviewer and the adjudicator are
the judges of whatever this surfaces. It exists to make the change VISIBLE,
never to decide it.

WHERE THE CLAIM COPY LIVES. The claim moves a spec into `docs/work/active/<branch>/`
on trunk and cuts the branch from that commit, so the text at claim is that
file at the lane's fork point - the claim commit itself, or trunk's untouched
copy at merge (`claimed_text`). If the claim ever moves off trunk, "at claim"
is still the spec at the lane's fork point.

The section is `kitlib.registry.done_when_section`'s, not a second tolerant
pattern here: the heading has four live spellings, and a reader matching fewer
reports the rest as absent.

Contracts: IF-242 - the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-242: a spec's Done-when as comparable items. `items` / `has_done_when`
    read a spec text; `changes` compares a claim-time text with a later one
    and returns `("changed", claim item)` / `("added", later item)` pairs;
    `describe` renders them as the lines the reviewer's brief and the minted
    adjudication both quote; `claimed_text` reads the claim-time copy out of
    git at a rev. Pure functions plus one thin read through `kitlib.git`; an
    unreadable claim copy is None, and each caller says what that means.
"""

import re

from .git import git_out
from .registry import done_when_section

__all__ = ["items", "has_done_when", "changes", "describe", "claimed_text"]

# A list item's opening: `-`, `*`, `+` or `1.` / `1)`, then an optional checkbox.
_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s*)?")
_HEADING_RE = re.compile(r"^\s*#{1,6}\s")
# The evidence form (see the module docstring): an opening separator, then a
# token that names what was done or where it shows.
_EVIDENCE_OPENERS = ("—", "–", "-", "(", "[", "->", "→", "✓", "|")
_EVIDENCE_TOKEN_RE = re.compile(
    r"\b(?:LANDED|DONE|MET|VERIFIED|SHIPPED|PASSED|FIXED|COVERED)\b"
    r"|[\w.-]+/[\w./-]+|::|`[^`]+`|\b(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}\b"
)
_ACTIVE = "docs/work/active"


def _normalize(text):
    """An item's text with its tick and strikethrough stripped and its
    whitespace collapsed - what is compared, never what is shown."""
    text = text.replace("~~", "").replace("✅", " ").replace("☑", " ")
    return " ".join(text.split())


def items(text):
    """The Done-when section's items, normalized, in order; [] when none.

    A list item starts at a list marker and runs over its continuation lines; a
    prose paragraph is one item; a blank line or a subsection heading ends the
    current item, and a subsection's own items belong to the section.

    Implements: SR-156, LLR-262
    """
    found, current = [], None
    for line in done_when_section(text):
        if not line.strip() or _HEADING_RE.match(line):
            current = None
            continue
        marker = _MARKER_RE.match(line)
        if marker or current is None:
            current = [line[marker.end() :] if marker else line]
            found.append(current)
        else:
            current.append(line)
    return [n for n in (_normalize(" ".join(parts)) for parts in found) if n]


def has_done_when(text):
    """Does the spec declare at least one Done-when item?

    Implements: SR-156, LLR-262
    """
    return bool(items(text))


def _extends(later, claimed):
    """Is `later` the item `claimed`, possibly ticked and followed by evidence?"""
    if later == claimed:
        return True
    if not later.startswith(claimed):
        return False
    rest = later[len(claimed) :].lstrip()
    return rest.startswith(_EVIDENCE_OPENERS) and bool(_EVIDENCE_TOKEN_RE.search(rest))


def changes(claimed, later):
    """How the Done-when of `later` differs from the one in `claimed`.

    `("changed", item)` for each claim-time item no later item carries as
    written (reworded, narrowed or deleted), then `("added", item)` for each
    later item that carries no claim-time one. [] when every item survives,
    ticked or with evidence appended.

    Implements: SR-156, LLR-262
    """
    before, after = items(claimed), items(later)
    kept = [c for c in before if any(_extends(a, c) for a in after)]
    lost = [("changed", c) for c in before if c not in kept]
    gained = [("added", a) for a in after if not any(_extends(a, c) for c in before)]
    return lost + gained


def describe(found):
    """One quoted line per change, the wording both flags share.

    Implements: SR-156, LLR-262
    """
    label = {
        "changed": "at claim, no longer present as written",
        "added": "added since claim",
    }
    return ["- {}: {!r}".format(label[kind], text) for kind, text in found]


def claimed_text(root, rev, branch, wi_id):
    """The spec for `wi_id` as the claim wrote it - under
    `docs/work/active/<branch>/` at `rev` - or None when that copy cannot be
    read (not a claimed lane, an unreadable rev).

    Implements: SR-156, LLR-262
    """
    folder = "{}/{}/".format(_ACTIVE, branch)
    listing = git_out(root, ["ls-tree", "--name-only", rev, folder])
    for path in (listing or "").splitlines():
        if path.rsplit("/", 1)[-1].startswith(wi_id + "-"):
            return git_out(root, ["show", "{}:{}".format(rev, path)])
    return None
