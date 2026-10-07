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

Contracts: IF-242, IF-286 - the seams this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-242: a spec's Done-when as comparable items. `items` / `has_done_when`
    read a spec text; `changes` compares a claim-time text with a later one
    and returns `("changed", claim item)` / `("added", later item)` pairs;
    `describe` renders them as the lines the reviewer's brief and the minted
    adjudication both quote; `claimed_text` reads the claim-time copy out of
    git at a rev. Pure functions plus one thin read through `kitlib.git`; an
    unreadable claim copy is None, and each caller says what that means.

BLESSED IN THE LANE (WI-841, owner direction 2026-10-06). A lane may edit its
own Done-when, and an adjudicator, not a guard, blesses the change before what
consumes the Done-when uses it: the lane's next build dispatch, and its close
and merge. The verdict is BOUND to the exact text it judged by a digest
(`digest`), as an approval act binds registry bytes, so a text changed after
the verdict is unblessed again. An owner ruling counts as that verdict: a
`docs/decisions/*.toml` entry the owner has confirmed or overruled that
carries the same digest under `done_when`. `blessing_owed` is THE predicate,
one rule asked at every hold point and by the merge-time mint; `lane_hold`
reads it off a tree (a commit, or the index a hand close stages). The commit
that edits the Done-when is never refused, and nothing here gates the test
suite: tests are evidence.

Contract IF-286: a Done-when change's blessing. `digest(wi_id, claimed,
    current)` binds the current items, each claim-time item it only ticks or
    evidences read as that item; `covering(root, rev)` reads every bound
    verdict line (`DONE-WHEN: <outcome> ... digest=<d>`) under the review
    records and every owner-ruled `done_when` digest in the decisions records,
    at a commit or (rev None) the index; `blessing_owed(root, rev, wi_id,
    claimed, current)` is None when nothing changed or a covering verdict or
    ruling binds the text, else `(digest, changes)` (`blessing` also returns
    the covering entry, for the merge-time mint); `lane_hold(root, rev,
    base, branch, wi_ids)` is the hold reason for a lane's tree, or None. An
    unreadable tree reads as uncovered: the hold fails closed.
"""

import hashlib
import re
import tomllib

from . import decisions as kdecisions
from . import sitting as _kitsitting
from .git import git_out
from .registry import done_when_section

__all__ = [
    "items",
    "has_done_when",
    "changes",
    "describe",
    "claimed_text",
    "claim_copy",
    "unreadable_reason",
    "bound_items",
    "digest",
    "covering",
    "blessing",
    "blessing_owed",
    "hold_reason",
    "spec_at",
    "lane_hold",
    "staged_closes",
]

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
    `docs/work/active/<branch>/` at `rev` - or None when there is none to read
    (absent or unreadable; `claim_copy` tells the two apart).

    Implements: SR-156, LLR-262
    """
    return claim_copy(root, rev, branch, wi_id)[0]


def claim_copy(root, rev, branch, wi_id):
    """The claim copy, told apart from its two absences (WI-841 round 4):

      * `(text, None)` - the spec under `docs/work/active/<branch>/` at `rev`;
      * `(None, None)` - ABSENT: `rev` reads and holds no spec of `wi_id`
        under that folder (a row never claimed through this lane: a hand-cut
        lane, or an attended run on a row it did not claim). There is no
        claimed Done-when, so there is nothing to bless;
      * `(None, why)` - UNREADABLE: no revision was given, `rev` cannot be
        read, or the listed copy cannot be. Whether the Done-when changed is
        unknown: every hold point holds on it and the mint refuses.

    Implements: SR-156, LLR-307
    """
    if not rev:
        return None, "the claim copy cannot be read at (no revision)"
    _path, text, why = _copy_at(root, rev, ["{}/{}".format(_ACTIVE, branch)], wi_id)
    return text, why


def _copy_at(root, rev, folders, wi_id):
    """THE ONE SHAPE both sides of a Done-when comparison are read in (WI-841
    round 7): `(path, text, None)` for `wi_id`'s spec in the last of `folders`
    holding one at `rev` (None: the index); `(None, None, None)` when `rev`
    reads and none of `folders` holds it (ABSENT); `(None, None, why)` when
    the listing or the copy cannot be read (UNREADABLE), never read as absent.

    Implements: SR-156, LLR-307
    """
    args = (
        ["ls-files", "--"]
        if rev is None
        else ["ls-tree", "-r", "--name-only", rev, "--"]
    )
    listing = git_out(root, args + list(folders))
    if listing is None:
        at = "the index" if rev is None else str(rev)[:10]
        return None, None, "{} cannot be read at {}".format(", ".join(folders), at)
    hits = [
        (folders.index(path.rpartition("/")[0]), path)
        for path in listing.splitlines()
        if path.rpartition("/")[0] in folders
        and path.rpartition("/")[2].startswith(wi_id + "-")
    ]
    if not hits:
        return None, None, None
    path = max(hits)[1]
    text = _show(root, rev, path)
    return path, text, None if text is not None else "{} cannot be read".format(path)


# --- the in-lane blessing (WI-841) ---------------------------------------------

# The verdict line a Done-when judgement ends in, and its outcomes. Every
# outcome covers the text its digest names: CLARITY (each change only
# clarifies), BLESSED (the scope moved and the adjudicator blesses it) and
# SUCCESSOR (the moved scope is not blessed and is drafted as a successor,
# never a reversal, which the merge mints from the verdict's own drafts).
# Their one home is the sitting grammar (`kitlib.sitting.GRAMMAR`).
VERDICT_KEYWORD = _kitsitting.GRAMMAR["done-when"][0]
OUTCOMES = _kitsitting.DONE_WHEN_OUTCOMES
# The key an owner-ruled decisions entry binds a Done-when text by.
RULING_KEY = "done_when"
REVIEWS = _kitsitting.REVIEWS
DECISIONS = kdecisions.DECISIONS_DIR
_DIGEST_CHARS = 16
_HOMES = ("docs/archive/work", "docs/work")
_CLOSED = ("complete", "partial", "cancelled")
_ACTIVE_SPEC_RE = re.compile(r"^docs/work/active/([^/]+)/(WI-\d+)-[^/]*\.md$")
# A close lands in either spec home: `spec_move`'s terminal destination under
# the archive, or the legacy one under docs/work (WI-841 round 2).
_CLOSED_SPEC_RE = re.compile(
    r"^(?:{})/(?:{})/(WI-\d+)-[^/]*\.md$".format("|".join(_HOMES), "|".join(_CLOSED))
)


def bound_items(claimed, current):
    """The current items, each one that only ticks or evidences a claim-time
    item read as that item: the text a verdict binds.

    Implements: SR-156, LLR-307
    """
    before = items(claimed)
    out = []
    for item in items(current):
        base = next((c for c in before if _extends(item, c)), None)
        out.append(base if base is not None else item)
    return out


def digest(wi_id, claimed, current):
    """`sha256:<16 hex>` over the work item's id and its bound items: the
    identity a verdict or a ruling names, so a text changed after it is not
    the text it judged. Evidence appended to a claim-time item does not move
    it; evidence appended to an item the lane added does.

    Implements: SR-156, LLR-307
    """
    body = "\n".join([wi_id] + bound_items(claimed, current))
    return "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()[:_DIGEST_CHARS]


def _grep(root, rev, pattern, path):
    """`[(path, line)]` where `pattern` matches a line under `path` at the
    commit `rev`, or in the index when `rev` is None. No match and an
    unreadable tree both answer [], which the caller reads as uncovered."""
    args = ["grep", "-I", "-E", "-z"] + (["--cached"] if rev is None else [])
    args += ["-e", pattern] + ([] if rev is None else [rev]) + ["--", path]
    prefix = "" if rev is None else rev + ":"
    out = []
    for line in (git_out(root, args) or "").splitlines():
        head, _sep, text = line.partition("\0")
        out.append((head[len(prefix) :] if head.startswith(prefix) else head, text))
    return out


def _show(root, rev, path):
    """A file's text at the commit `rev`, or in the index when `rev` is None."""
    return git_out(root, ["show", "{}:{}".format("" if rev is None else rev, path)])


def _verdicts(root, rev):
    """`{digest: (outcome, path)}` for every ACCEPTED Done-when verdict under
    the review records (WI-841 round 11): read through the one reader,
    `kitlib.sitting.accepted`, which answers only for a verdict whose binding
    records it accepted by the route that ran the call and which parses as
    valid against that binding. A failed or pending call, an unbound verdict,
    an invalid sitting and another brief class all cover nothing."""
    found = {}
    pattern = "^[[:space:]]*{}:".format(VERDICT_KEYWORD)
    for path in sorted({p for p, _line in _grep(root, rev, pattern, REVIEWS)}):
        verdict = _kitsitting.accepted_at(root, rev, path) or {}
        label, fields, _body, _rows = verdict.get("done-when", (None, {}, "", {}))
        if label:
            found[fields["digest"]] = (label, path)
    return found


def _rulings(root, rev):
    """`{digest: (owner verdict, citation)}` for every decisions entry the
    owner has confirmed or overruled that binds a Done-when digest."""
    found = {}
    pattern = "^[[:space:]]*{}[[:space:]]*=".format(RULING_KEY)
    for path in sorted({p for p, _line in _grep(root, rev, pattern, DECISIONS)}):
        try:
            data = tomllib.loads(_show(root, rev, path) or "")
        except tomllib.TOMLDecodeError:
            continue
        entries = data.get("decision")
        for entry_id, entry in (entries if isinstance(entries, dict) else {}).items():
            found.update(_ruling(path, entry_id, entry))
    return found


def _ruling(path, entry_id, entry):
    """`{digest: (owner verdict, citation)}` for one entry, or {} when it binds
    no digest or the owner has not ruled on it (an entry still carrying the
    retired key reads as not yet seen)."""
    if not isinstance(entry, dict) or kdecisions.RETIRED_KEY in entry:
        return {}
    state = kdecisions.owner_state(entry.get(kdecisions.OWNER_KEY))
    bound = entry.get(RULING_KEY)
    if state not in kdecisions.OWNER_VALUES or not isinstance(bound, str):
        return {}
    return {bound.strip(): (state, kdecisions.citation(path, entry_id))}


def covering(root, rev):
    """`{digest: (outcome or owner verdict, where)}`: every Done-when text a
    verdict or an owner ruling in the tree at `rev` (None: the index) binds.

    Implements: SR-156, LLR-307
    """
    return {**_verdicts(root, rev), **_rulings(root, rev)}


def blessing(root, rev, wi_id, claimed, current):
    """`(digest, changes, cover)` for a Done-when that differs from the claimed
    one (ticks and evidence aside), `cover` being the verdict or owner ruling
    in the tree at `rev` that binds its exact text (`covering`'s value) or
    None; None when nothing changed. A claim copy or a current text that
    cannot be read has no change to bless (the merge-time arm's reading), and
    each caller says what that means.

    Implements: SR-156, LLR-307
    """
    if claimed is None or current is None:
        return None
    found = changes(claimed, current)
    if not found:
        return None
    bound = digest(wi_id, claimed, current)
    return bound, found, covering(root, rev).get(bound)


def blessing_owed(root, rev, wi_id, claimed, current):
    """THE predicate every hold point asks: `(digest, changes)` while the
    current Done-when differs from the claimed one and no verdict or owner
    ruling binds its exact text, else None.

    Implements: SR-156, LLR-307
    """
    found = blessing(root, rev, wi_id, claimed, current)
    return found[:2] if found and found[2] is None else None


def hold_reason(wi_id, owed):
    """The one wording every hold point prints for an unblessed change.

    Implements: SR-156, LLR-307
    """
    bound, found = owed
    return (
        "{}: its Done-when differs from the claimed one and no verdict or owner "
        "ruling binds its text (digest {}): sit the done-when adjudication, or "
        'record the owner\'s ruling as `{} = "{}"` on a docs/decisions entry, '
        "before the lane builds on it or closes:\n{}".format(
            wi_id, bound, RULING_KEY, bound, "\n".join(describe(found))
        )
    )


def spec_at(root, rev, branch, wi_id):
    """`(path, text, why)` of `wi_id`'s spec in the lane's tree at `rev`
    (None: the index), in `_copy_at`'s shape: its closed copy once the lane
    has closed it, else its copy under `active/<branch>/`; absent, or
    unreadable naming why.

    Implements: SR-156, LLR-307
    """
    subs = ["{}/{}".format(_ACTIVE, branch)] + [
        "{}/{}".format(home, sub) for sub in _CLOSED for home in _HOMES
    ]
    return _copy_at(root, rev, subs, wi_id)


def lane_hold(root, rev, base, branch, wi_ids):
    """The hold for a lane's tree at `rev` (None: the index) against the claim
    copy under `active/<branch>/` at `base`: one `hold_reason` per work item
    whose Done-when change no verdict or ruling at `rev` binds, joined; None
    when none is owed.

    Implements: SR-156, LLR-307
    """
    reasons = []
    for wi_id in sorted(wi_ids):
        reason = _wi_hold(root, rev, base, branch, wi_id)
        if reason:
            reasons.append(reason)
    return "\n".join(reasons) or None


_NO_COPY = "no copy of its spec sits under docs/work/active/{}/ or a closed folder"


def _wi_hold(root, rev, base, branch, wi_id):
    """One work item's hold, or None. An ABSENT claim (a row never claimed
    through this lane) releases; an unreadable claim, an unreadable current
    copy, or a claimed row with NO current copy in the lane (its claimed
    Done-when gone, which no close accounts for) holds, naming why.

    Implements: SR-156, LLR-307
    """
    claimed, why = claim_copy(root, base, branch, wi_id)
    if claimed is None and why is None:
        return None
    current = None
    if why is None:
        _path, current, why = spec_at(root, rev, branch, wi_id)
        why = why or (None if current is not None else _NO_COPY.format(branch))
    if why:
        return unreadable_reason(wi_id, why)
    owed = blessing_owed(root, rev, wi_id, claimed, current)
    return hold_reason(wi_id, owed) if owed else None


def unreadable_reason(wi_id, why):
    """The one wording every hold point (and the merge-time mint's refusal)
    prints when either side of the comparison cannot be read (`_copy_at`'s
    UNREADABLE), or a claimed row has no current copy.

    Implements: SR-156, LLR-307
    """
    return (
        "{}: its claimed Done-when cannot be compared, because {}; whether the "
        "lane changed it is unknown, so it is held until the claim copy "
        "reads".format(wi_id, why)
    )


def staged_closes(root):
    """`[(branch, wi_id)]` for each spec the index moves out of
    `active/<branch>/` into a closed folder - a close being committed.

    Implements: SR-156, LLR-307
    """
    delta = git_out(root, ["diff", "--cached", "--name-status", "--no-renames"])
    removed, closed = [], set()
    for line in (delta or "").splitlines():
        status, _tab, path = line.partition("\t")
        active = _ACTIVE_SPEC_RE.match(path)
        landed = _CLOSED_SPEC_RE.match(path)
        if status.startswith("D") and active:
            removed.append((active.group(1), active.group(2)))
        elif status.startswith("A") and landed:
            closed.add(landed.group(1))
    return [(branch, wi_id) for branch, wi_id in removed if wi_id in closed]
