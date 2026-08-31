"""integrate.py — the local integrator: the station protocol and its merge slot.

The default backend of the one integration flow (concurrency-restructure
§1.2), rebuilt on ONE constraint (docs/concurrency-v2.md §A2):

    A branch may not enter the merge queue unless trunk is already an
    ancestor of it.

`git merge-base --is-ancestor` — exact, cheap, mechanical. Everything else
here follows from that line. A merge CONFLICT becomes unrepresentable (if
trunk is an ancestor, the --no-ff merge is trivially clean and its tree is
byte-identical to the branch tip), so there is no conflict arm, no `merge
--abort` path and no half-merge to park. The composed tree IS the branch
tree, so the bar runs ONCE per WI — on the branch, at refresh — instead of
once by the builder and again by the integrator on a candidate worktree.
Class C composition failures are still caught, and better: whichever branch
merges second must refresh onto a trunk containing the first and bar THERE,
so every pair composes exactly once, on the real tree, with the red
attributable to the refresh that caused it.

THREE TERMINAL OUTCOMES, NO FOURTH (§A3). Every lane ends in a merge: `merged`
(specs -> complete/), `cancelled` (specs -> cancelled/, so the cancellation is a
trunk fact and the id stays retired) and `handback` (the work so far committed
as-is, the specs back in queued/ carrying a `## Handback` section and a
blockref). The outcome is not a flag anyone sets: it IS the folder the branch
moved its specs into, read back by `branch_outcomes` off the same move that made
the branch finished - so a merge queue that reads the outcome cannot disagree
with the tree it is merging.

Four operations here; the two lane closes that are NOT a merge (`hand_back`,
`quarantine`) live in the sibling handback.py:

  claim      the §2.3 claim protocol, step 1+2: move a queued spec to
             docs/work/active/<branch>/, write that bookkeeping commit as an
             OBJECT, point the work branch at it, and only then advance trunk
             (§A3 - the order is what makes a crash between the two writes
             benign, see `claim`). Refuses while the tracked
             docs/work/pause is present (§5.6: pause = stop claiming), while
             hand-authored docs/status.md prose names the claimed id
             (WI-358: that R-D debt is paid before the branch exists, since a
             branch cannot scrub trunk-owned status.md at merge time), and
             when the spec carries no in-repo-resolving SpecRef (WI-370:
             the R-E debt is unpayable once the closing branch exists).
  refresh    the STATION REFRESH (§A2), lane-side and mechanical: in the
             branch's own lane worktree, merge trunk IN, run trunk_step.py
             (compile the fragments, then regenerate), run the DECLARED bar
             --trunk-lane, and commit the result carrying a `Bar-Green:`
             trailer. The order is fixed and load-bearing (§A2.1). The
             refresh commit is DISPOSABLE: a retry resets to the last work
             commit and redoes the whole sequence, never stacks a second
             merge on the first — docs/log.md is append-compiled from
             docs/log.d/ fragments, and a stacked refresh would conflict on
             the file end, the exact failure the constraint abolishes.
  integrate  THE MERGE SLOT: the exclusive turn to advance trunk, and the
             whole merge queue. It takes the coordinator lock ONCE (the one
             acquisition site in this file, see `_slot`) and, per FINISHED
             claimed branch, reads the lane's OUTCOME off the tree
             (`branch_outcomes`), REFUSES a branch whose docs/work/ delta mints
             a work-item id outside its claimed set (RULING R1, see
             `_minted_id_refusal` - minting is trunk-side and serial, so a
             collision two lanes could produce is unrepresentable), requires the
             policy verdicts the outcome
             owes (RULING-7 keyed off §A3, not off the claim), checks
             the ancestor relation and VERIFIES the `Bar-Green:` attestation
             at the branch tip, then merges --no-ff. A branch that is not
             merge-ready is refreshed RIGHT THERE, inside the slot — which is
             the pessimistic sequence (take slot -> refresh -> bar -> merge)
             and is why that path can never rot: every drain that merges a
             second branch reaches it, because the first merge moved trunk
             out from under it. The merged branch is then UNLOADED: a clean
             lane worktree holding it is GC'd, while a dirty one (ignored
             files included) and the MAIN checkout are reported by path and
             left alone. §5.6's stop is drained AND unloaded, so a run that
             merged everything but left a branch held names it on stderr and
             exits NONZERO - the merges stand, the code reports the unpaid
             remainder.
  audit      the RULING-6 window check over the integrator's own operation:
             every trunk commit in --since..HEAD that touches product paths
             must be a merge commit. Scoped to a window because the
             always-on form would flag attended serial work (RULING-8's
             workers=1 flow) — widening the scope is an owner ruling, not
             this script's call.

Fail-closed by construction, against the dispatcher's recorded fail-open: a
missing docs/stack.ini, an absent or EMPTY [product] test declaration, or
any SKIP in the bar's own report is a REFUSAL, never a pass — exit 0 alone
is not evidence the bar ran (the `bar_failures: 0` lesson, §4.4 of the
Phase 4 inventory). The bar is attested to a TREE, and the attestation NAMES
that tree: the refresh commit carries `Bar-Green: tree=<sha> work=<sha>
<summary>`, and the slot re-derives both names from git before it merges. A
message alone would prove nothing — amend, rebase, cherry-pick and copy all
carry words onto content nobody barred — so the trailer is checked, never
read. That closes ACCIDENT, not INTENT: a lane that deliberately names the
tree and the parent (four git invocations) merges unbarred, and the design
accepts it because DECISION 3 ruled out a slot-side bar and a lane is trusted
code (`refresh_attestation` states the bound in full). Verdict freshness is
git-derived the same way: the
verdict's last commit on the branch must be no older than the branch's last
non-review, non-fragment WORK commit (the disposable refresh is peeled off
first — mechanical bookkeeping must not stale an honest APPROVE).

Never pushes; the trunk only ever moves inside the slot, to a branch whose
own bar passed on this exact tree.

Contracts: IF-080, IF-154, IF-173 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-080: this module's CLI is the local integration seam, and each
    subcommand's refusal is the contract. `claim` performs the serial trunk
    claim — a queued spec moves to `docs/work/active/<branch>/` in one
    bookkeeping commit and the branch is cut from that commit — refusing
    before it writes anything on a declared pause, a dirty tree, an existing
    branch, an unsafe branch name, a non-ordinary spec or an off-frontier row.
    `refresh` runs the station refresh on a claimed branch. `integrate` is the
    serial fail-closed merge queue: a `--no-ff` merge onto a candidate
    worktree, the trunk step folded in, then the DECLARED bar on the composed
    tree — a missing or empty declaration, or any SKIP in it, refuses — and
    the verdict gate with git-derived freshness before the fast-forward-only
    trunk advance. `audit` is the non-merge product-commit window check. The
    trunk only ever moves inside the slot, to a branch whose own bar passed on
    exactly the tree being advanced, and nothing here ever pushes. Every
    subcommand exits nonzero on refusal with the reason named; the caller
    needs no other channel to know what happened.
Contract IF-154: the argv surface, one required subcommand deep. `--root`
    (default the cwd) precedes the subcommand; `claim` requires `--wi` (one id,
    or several `;`-separated) and `--branch`; `refresh` requires `--branch` and
    takes `--tier` (default `all`, the full gate bar); `integrate` takes
    `--tier` alone and drains every finished claimed branch there is; `audit`
    requires `--since`, the window's base revision. Nothing here accepts a
    remote, push or force option: the only repository it can move is `--root`.
Contract IF-173: this module as the library its three siblings drive
    in-process, the same ladder the CLI drives with no argv between. The
    dispatcher takes the claim-and-merge vocabulary — `claim` (with
    `dispatch_lock_held=True`, holding the coordinator lock itself),
    `refresh`, `integrate`, `finished_branches`, `branch_outcomes`,
    `_merge_ready`, `_claimed_wi_ids`, `_claimed_specs`, `_spec_frontmatter`,
    `ACTIVE`. The handback takes the worktree and revision readers —
    `lane_worktree`, `_worktree_holding`, `_head`, `_rev`, `_claimed_specs`,
    `_spec_frontmatter`, `WORK`, `ACTIVE`. The lane takes `lane_worktree`
    alone. Every refusal is a RETURN VALUE, never a raise: a code from `claim`
    and `integrate`, a `(sha, refusal)` pair from `refresh`, a `(ready, why)`
    pair from `_merge_ready`. The `_`-prefixed names above are named on the
    row and are part of the promise, not private detail a caller reached
    past; nothing here pushes, and the trunk moves only inside the slot.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import agent_common as ac
import score_reviews
import spec_move
from kitlib.station import (
    BAR_GREEN,
    OUTCOME_DIRS,
    Outcome,
    outcome_of,
    read_toml_block,
    report_path,
    report_refusal,
)

SCRIPTS = Path(__file__).resolve().parent
WORK = "docs/work"
ACTIVE = WORK + "/active"
# Terminal history's home since WI-504 (OI-55 ruled (a)): a lane closes into
# `docs/archive/work/<outcome>/` now, one directory deeper than `docs/work/`
# itself — `branch_outcomes` below reads BOTH prefixes so a branch that closed
# before or after the relocation is read identically.
ARCHIVE_WORK = "docs/archive/work"

# THE THREE TERMINAL OUTCOMES (§A3 as amended by SR-144) live in
# `kitlib.station` and are re-exported here, unchanged, for every caller that
# already reads them off this module. WI-483 moved the DEFINITION down: the
# vocabulary depends on nothing, while this module claims lanes, merges branches
# and moves specs, so a reader that only wants the table used to have to import
# a mutation coordinator to get it — the dashboard did exactly that, and that
# import was an edge of the seven-module cycle (repo review 2026-08-19, H-02).
# `kitlib/station.py`'s docstring carries the vocabulary's own reasoning; what
# stays here is the git-tree READ that applies it.

# One LANE worktree home per repo, sibling to the checkout; one subdirectory per
# claimed branch. The worker builds there and the station refresh runs there —
# the same tree, on purpose: a red refresh has to be fixable where the lane
# already lives. §5.6's unload GCs a clean one after its merge.
LANE_WORKTREE_SUFFIX = "-drive"

_ATTEST_RE = re.compile(
    r"^Bar-Green:\s+tree=([0-9a-f]{40})\s+work=([0-9a-f]{40})\s+(\S.*)$"
)


def _refresh_subject(branch):
    """The refresh commit's subject prefix for `branch` - one home, because the
    writer and the verifier must agree on it exactly."""
    return "refresh: {} onto trunk ".format(branch)


# How far back `_work_tip` will peel refresh commits. The disposable-commit rule
# means at most ONE can ever sit on the tip, so this is a guard against a
# hand-made pathological history, not an expected depth.
_MAX_REFRESH_PEEL = 8

# RULING-6 bookkeeping surfaces: the paths a NON-merge trunk commit may touch
# during integrator operation. docs/log.md is here because the trunk step
# compiles fragments into it; docs/status.md and the other generated homes are
# read from stack.ini [generated] at audit time so the declared set stays the
# one home (§5.2).
#   docs/id-watermark is here and NOT in [generated], deliberately. The mint
# raises the mark in the same bookkeeping commit that files the specs
# (intake.py, "RAISE THE MARK IN THE SAME COMMIT"), so an integrator run that
# mints anything touches this path — and without it declared, the run's own
# audit flags its own bookkeeping and the queue fails on a false red. It does
# not belong in [generated] because every artifact there is REGENERABLE from
# the tree, while the watermark is the only record of ids that have been
# DELETED; regenerating it from live rows is precisely the id re-use the mark
# exists to prevent.
BOOKKEEPING_PREFIXES = (WORK + "/", "docs/log.d/", "docs/log.md", "docs/id-watermark")


def fail(msg):
    print("integrate: REFUSED - {}".format(msg), file=sys.stderr)
    return 1


def _spec_frontmatter(path):
    """The TOML frontmatter dict of a spec file (between +++ lines)."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\+\+\+\n(.*?)\n\+\+\+", text, re.S)
    if not m:
        raise ValueError("{}: no +++ frontmatter".format(path))
    return tomllib.loads(m.group(1))


def _queued_spec(root, wi_id):
    hits = sorted((root / WORK / "queued").glob(wi_id + "-*.md"))
    if len(hits) != 1:
        raise ValueError(
            "{} queued spec(s) match {} - claim needs exactly one".format(
                len(hits), wi_id
            )
        )
    return hits[0]


# The R-D id-token shape and the generated-block split, matched HERE rather than
# imported from check_trajectory: that module's `status_forward_only_findings`
# flags only ids whose registry status is already `done`, and a claimed id is
# still queued - the debt only becomes a red at close. The regex and the
# BEGIN/END sentinels are kept identical to it so claim-time and merge-time agree
# on what is a token and what is hand prose.
_WI_TOKEN_RE = re.compile(r"\bWI-\d+\b")

# A work-item SPEC filename, `WI-<n>-<slug>.md` - the shape `claim` writes and
# the shape every state folder holds. See `_spec_id`.
_SPEC_NAME_RE = re.compile(r"^(WI-\d+)-.+\.md$")


def normalize_wi_id(wi_id):
    """`wi-401`/`Wi-401` -> `WI-401`; anything else is returned unchanged.

    One normalization at the CLI boundary, because the rungs below disagree
    about case: `Path.glob` casefolds on Windows (so a lowercase --wi still
    resolves its spec) while the scheduler frontier and the WI-358 status scan
    match the canonical uppercase token - which silently skipped the scan and
    then refused with the wrong reason ("not on the ready frontier").
    """
    return re.sub(r"^wi-", "WI-", wi_id.strip(), flags=re.IGNORECASE)


def _status_prose_hits(root, wi_id):
    """Hand-authored docs/status.md lines naming `wi_id` as a token: (lineno, text).

    Lines inside a generated block (`<!-- BEGIN GENERATED ... -->` through
    `<!-- END GENERATED ... -->`) are excluded - the generated frontier
    legitimately names queued ids, and R-D stands down there too.

    Raises OSError when status.md exists but cannot be read - the caller turns
    that into a refusal rather than a silently skipped scan (fail closed).
    """
    path = root / "docs" / "status.md"
    if not path.exists():
        return []
    hits = []
    generated = False
    text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        if "<!-- BEGIN GENERATED" in line:
            generated = True
        if not generated and wi_id in _WI_TOKEN_RE.findall(line):
            hits.append((lineno, line.strip()))
        if "<!-- END GENERATED" in line:
            generated = False
    return hits


def _status_prose_refusal(root, wi_id):
    """The WI-358 claim rung: a refusal string, or None.

    status.md is trunk-owned and forward-only, so an id named in its HAND prose
    reds R-D on the composed tree the moment the WI closes - and the work branch
    cannot scrub a file it does not own. Refuse (not warn): the debt is payable
    now, in one trunk commit, and a warn would only resurface as a red merge
    after the whole branch was built.
    """
    try:
        hits = _status_prose_hits(root, wi_id)
    except OSError as exc:
        # A status.md that exists but will not read (a directory, a permission
        # denial) must not skip the scan - an unscanned file is exactly where
        # the debt hides.
        return (
            "docs/status.md exists but cannot be read ({}) - the forward-only "
            "scan cannot run, and an unscanned status.md is not a clean one; "
            "fix the file, then claim".format(exc)
        )
    if not hits:
        return None
    return (
        "{} is named in hand-authored docs/status.md prose (line{} {}) - "
        "status.md is forward-only, so this id reds R-D on the composed tree "
        "the moment the WI closes, and the work branch cannot scrub "
        "trunk-owned status.md. Move that prose to its home (docs/log.md, or "
        "the generated block) in a trunk commit, then claim:\n{}".format(
            wi_id,
            "" if len(hits) == 1 else "s",
            ", ".join(str(n) for n, _ in hits),
            "\n".join("  {}: {}".format(n, t) for n, t in hits),
        )
    )


def _specref_refusal(root, meta, wi_id):
    """The WI-370 claim rung: a refusal string, or None.

    R-E, hoisted to claim time - the WI-358 shape again. An open WI without a
    resolving SpecRef reds --strict on every composed tree that sees it, and
    the debt is unpayable once the closing branch exists: open wants the ref
    and terminal wants it cleared, so a trunk-side repair rename-merges the
    ref INTO the closed copy and trips R-F instead. The rung checks the
    PATH part only; anchor resolution stays check_trajectory's job.
    """
    ref = str(meta.get("specref", "") or "").strip()
    if not ref:
        return (
            "{} carries no SpecRef - an open WI without one reds R-E under "
            "--strict on every composed tree, from a file the closing branch "
            "cannot amend (WI-370). Name the spec-of-record in the queued "
            "spec in one trunk commit, then claim".format(wi_id)
        )
    path_part = ref.split("#", 1)[0]
    if not path_part:
        return (
            "{} SpecRef {!r} has no path part (a bare #anchor) - R-E wants "
            "an in-repo document; fix the queued spec, then claim "
            "(WI-370)".format(wi_id, ref)
        )
    if not (root / path_part).is_file():
        return (
            "{} SpecRef {!r} does not resolve to an in-repo FILE (R-E: a "
            "directory or missing path reds the bar) - fix the queued spec, "
            "then claim (WI-370)".format(wi_id, ref)
        )
    return None


def _claim_subject(wi_ids, branch):
    """The claim commit's subject - one home, because the writer and the
    abandoned-claim reader below must agree on it exactly. A spine BATCH
    (WI-381, §A4: all spine WIs admit together) joins its ids with ";", so the
    single-WI form is byte-identical to what it always was. Accepts one id or
    the list, like `claim` itself."""
    wi_ids = [wi_ids] if isinstance(wi_ids, str) else list(wi_ids)
    return "claim: {} -> active/{} (bookkeeping)".format(";".join(wi_ids), branch)


def _name_status(out):
    """`(status, path)` per record of a `git diff --name-status` run, paths
    posix-normalised; unreadable records are skipped.

    ONE parse of that porcelain, because the two readers of it here both
    AUTHORISE something off what a commit touched - `_abandoned_claim` a branch
    deletion, `_minted_id_refusal` a merge refusal - and two parsers that
    disagreed about the tab split or about backslashes would disagree about the
    facts those authorisations rest on. Both callers pass `--no-renames`, so a
    record is `<status>\\t<path>` and `parts[-1]` is that path.
    """
    for line in out.splitlines():
        parts = line.strip().split("\t")
        if len(parts) < 2:
            continue
        yield parts[0], parts[-1].replace("\\", "/")


def _abandoned_claim(root, wi_ids, branch):
    """Is `branch` the orphan a CRASHED claim leaves behind - and nothing else?

    This function authorises a `git branch -D`, so it has to convict, not
    resemble. Four facts, and every one of them has to hold:

      * the tip's subject is EXACTLY `_claim_subject(wi_id, branch)`. The one
        home is one home - an earlier version tested only that the subject
        ENDED with `-> active/<branch> (bookkeeping)`, which a hand-written
        `wip: nearly done -> active/wi-401 (bookkeeping)` satisfies, and
        REVIEW-A round 1 drove that branch being deleted with its work on it;
      * the tip is NOT an ancestor of trunk - nothing of it reached trunk;
      * the tip's parent IS, so the branch is exactly ONE commit past a point
        trunk has; and
      * that one commit IS THE MOVE THIS CLAIM WOULD MAKE, and nothing else:
        it ADDS this WI's spec under `active/<branch>/`, and every path it
        touches is that spec's move, a DECLARED generated artifact, or an
        `.md` MODIFICATION that is byte-for-byte the inbound relink of that
        move (WI-393: the claim's move is the link-aware ritual, so its commit
        carries the redirect writes — `_relinked_exactly` re-derives them from
        the commit's own move pair and `spec_move.expected_relink`; an edit
        the oracle cannot reproduce is somebody's work). Being one
        commit ahead proves nothing about what the commit carries - round 1
        drove a one-commit branch adding `real-work.txt` - and "only
        bookkeeping surfaces" was still too wide: round 2 drove a commit adding
        only `docs/log.d/WI-401-hours.md` being convicted and the fragment
        lost. The claim writes a spec move plus its regeneration and relinks,
        so that is the whole of what a claim commit may contain.

    Any branch failing any of the four is a real collision and still refuses.

    THE FAILURE DIRECTION, stated as narrowly as the code behaves: a repo that
    has declared no `[generated]` artifacts refuses its OWN crashed claims,
    because the regeneration this claim folds in lands on undeclared paths. It
    never deletes something it should not; it declines to re-cut something it
    could have. Same declaration `audit` reads.

    SCOPE OF "CONTENT" (the WI-461 lesson): every compare below runs over
    COMMITTED BLOBS (`_blob_bytes`), so the repo's own clean filters define
    what content is — an EOL-only working-tree edit that `core.autocrlf`
    normalizes away never enters the commit and is rightly invisible to a
    commit-scoped oracle (scaffolded repos pin this via the shipped
    .gitattributes' `* text=auto eol=lf`).

    Implements: SR-156, LLR-151
    """
    wi_ids = [wi_ids] if isinstance(wi_ids, str) else list(wi_ids)
    tip = _rev(root, "refs/heads/" + branch)
    if tip is None:
        return False
    subject = _commit_message(root, tip).splitlines()[:1]
    if not subject or subject[0].strip() != _claim_subject(wi_ids, branch):
        return False
    head = _head(root)
    if ac.git(root, "merge-base", "--is-ancestor", tip, head)[0] == 0:
        return False
    if ac.git(root, "merge-base", "--is-ancestor", tip + "^1", head)[0] != 0:
        return False
    delta = _claim_delta(root, tip, branch, wi_ids)
    if delta is None:
        return False
    moved, relinked = delta
    # A commit that regenerated artifacts but moved fewer specs than THIS
    # claim would move is not this claim (a batch is one commit, whole).
    if any(moved[wid].get("dest") is None for wid in wi_ids):
        return False
    remap = {
        moved[wid]["src"]: moved[wid]["dest"] for wid in wi_ids if moved[wid].get("src")
    }
    return not relinked or _relinked_exactly(root, tip, remap, relinked)


def _claim_delta(root, tip, branch, wi_ids):
    """Classify the candidate claim commit's own diff, or None to convict.

    `(moved, relinked)` where `moved` maps each claimed id to its own move
    pair — the A under active/<branch>/ (`dest`) and the D under queued/
    (`src`) — and `relinked` is every other `.md` MODIFICATION, the paths only
    the WI-393 oracle may excuse. A batch claim (WI-381) is ONE commit moving
    every batched spec, so every id gets its own pair. Any path outside those
    shapes is somebody's work and the whole read is None."""
    # --no-renames because the claim's `git mv` would otherwise arrive as ONE
    # rename record and hide the queued side of the move; split, both paths are
    # named and each is judged on its own.
    code, out = ac.git(root, "diff", "--name-status", "--no-renames", tip + "^1", tip)
    if code != 0:
        return None  # a diff nobody could read is not evidence of anything
    generated = _generated_paths(root)
    claimed = {wid: "{}/{}/{}-".format(ACTIVE, branch, wid) for wid in wi_ids}
    queued = {wid: "{}/queued/{}-".format(WORK, wid) for wid in wi_ids}
    moved = {wid: {"src": None, "dest": None} for wid in wi_ids}
    relinked = []
    for status, path in _name_status(out):
        wid_a = next((w for w, pre in claimed.items() if path.startswith(pre)), None)
        wid_d = next((w for w, pre in queued.items() if path.startswith(pre)), None)
        if wid_a is not None:
            if status.startswith("A"):
                moved[wid_a]["dest"] = path
        elif wid_d is not None:
            if status.startswith("D"):
                moved[wid_d]["src"] = path
        elif any(path == g.rstrip("/") or path.startswith(g) for g in generated):
            continue
        elif status.startswith("M") and path.endswith(".md"):
            relinked.append(path)
        else:
            return None
    return moved, relinked


def _blob_bytes(root, rev_path):
    """The raw bytes of `<rev>:<path>` (`git cat-file blob`), or None.

    NOT `ac.git`: that helper is text-mode — universal-newlines decode folds
    `\\r\\n`/`\\r` to `\\n` and its success path `.strip()`s — which is exactly
    the mangle WI-393 REVIEW-A finding 1 drove through the oracle below (a
    trailing-newline-only hand edit and a whole-file CRLF relay both excused
    as "relink-identical"). A byte-for-byte compare needs byte reads."""
    proc = subprocess.run(
        ["git", "-C", str(root), "cat-file", "blob", rev_path],
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )
    return proc.stdout if proc.returncode == 0 else None


def _relinked_exactly(root, tip, remap, paths):
    """Are these `.md` modifications EXACTLY the inbound relink the claim's own
    move would write (WI-393)? The remap is re-derived from the commit's own
    A/D pair, and each path's new BYTES must equal `spec_move.expected_relink`
    over its parent bytes — byte-for-byte LITERALLY (WI-403): both sides are
    read raw, the parent side decoded strictly and the expectation re-encoded,
    so nothing is stripped or EOL-folded before the compare and the clause
    excuses only what the ritual provably wrote. A hand edit riding in a
    claim-shaped commit convicts even at the whitespace/EOL margin, where this
    repo's own discipline (WI-234/WI-337) says the bytes are load-bearing —
    and the ritual preserves line endings (`newline=""`), so a genuine relink
    on a CRLF checkout still matches without any folding. A parent that does
    not decode as UTF-8 convicts too: `_rewrite_md_links` SKIPS such a file,
    so a modification to it cannot be the ritual's write. `remap` is the
    commit's own src->dest move pairs — one entry per batched spec (WI-381),
    re-derived by the caller from the A/D records themselves."""
    if not remap:
        return False
    for path in paths:
        old = _blob_bytes(root, "{}^1:{}".format(tip, path))
        new = _blob_bytes(root, "{}:{}".format(tip, path))
        if old is None or new is None:
            return False
        try:
            old_text = old.decode("utf-8")
        except UnicodeDecodeError:
            return False
        doc_dir = path.rsplit("/", 1)[0] if "/" in path else ""
        if spec_move.expected_relink(old_text, doc_dir, remap).encode("utf-8") != new:
            return False
    return True


def _drop_abandoned(root, branch):
    """Delete the abandoned claim branch the ladder let through, if there is
    one. A refusal string, or None.

    Only an abandoned claim survives `_claim_refusal`'s branch rung, so this is
    the re-claim §A3 asks for rather than a clobber. Two things it does that a
    one-liner did not: it prints the SHA and the restore command, because a
    deletion the operator cannot reach by reflog is a deletion they cannot
    audit; and it READS THE RETURN CODE, because `git branch -D` refuses a
    branch a worktree has checked out. Round 2 announced
    `deleted the abandoned claim branch ...` over a branch that still existed
    and then refused with an unrelated message - the same
    reports-success-on-failure shape as the rename mis-parse it sat eight lines
    from, so the holder is named here and the caller stops.
    """
    orphan = _rev(root, "refs/heads/" + branch)
    if not orphan:
        return None
    code, out = ac.git(root, "branch", "-D", branch)
    if code != 0:
        holder, is_primary = _worktree_holding(root, branch)
        where = (
            "no registered worktree holds it"
            if holder is None
            else "it is checked out in {}{}".format(
                holder, " (the MAIN checkout)" if is_primary else ""
            )
        )
        return (
            "{} is an abandoned claim but will not delete - {}. Free the branch "
            "(git worktree remove <path> / git -C <path> checkout <trunk>) then "
            "re-run; nothing was claimed:\n{}".format(
                branch, where, ac._failure_tail(out)
            )
        )
    print(
        "integrate: deleted the abandoned claim branch {} (was {}; recoverable "
        "via git reflog / git branch {} {})".format(
            branch, orphan[:10], branch, orphan[:10]
        )
    )
    return None


def _dispatch_lock(root):
    """REQUIRE the dispatch lock for a claim: `(release_callable, None)` when
    taken, `(None, refusal)` when a dispatcher holds it.

    The §A4.1 authority flip (WI-381). Admission is the DISPATCHER's scheduling
    decision, and the old `safety_class != ordinary` refusal below it is
    deleted — a hard stop replaced by a wait. What closes the remaining hole
    (`integrate claim` is a hand-runnable CLI) is a CONSTRAINT, not a check:
    the claim takes `out/agent-loop.lock` — the lock the live dispatcher holds
    for its whole process lifetime — so a hand claim during live lanes is
    UNREPRESENTABLE (the lock cannot be acquired), while a hand claim on an
    idle station still works (attended-serial per RULING-8). THE ONE
    ACQUISITION SITE for this lock in this file, mirroring `_slot`'s
    discipline for the merge slot's own lock: two locks, one site each.

    A private descriptor on purpose: `ac.acquire_lock` keeps ONE held-
    descriptor slot for the process (the coordinator's), and a claim inside a
    live dispatcher never reaches here (it passes `dispatch_lock_held=True`),
    so this path is the hand/CLI path only and must not disturb that slot.

    Implements: SR-156, LLR-151
    """
    path = ac.dispatch_lock_path(root)
    fd, exc = ac._open_lock_fd(path)
    if exc is not None:
        os.close(fd)
        return None, (
            "the dispatch lock {} is held - a dispatcher's lanes are live, and "
            "a hand claim mid-flight is unrepresentable (WI-381, §A4.1: "
            "admission is the dispatcher's decision). Wait for the run to "
            "finish, or stop it, then claim (held by: {})".format(
                path, ac._read_holder(path) or "unknown"
            )
        )

    def release():
        os.close(fd)
        # Best-effort removal so a HAND claim leaves no untracked residue for
        # the next clean-trunk rung on a repo whose ignore rules predate out/
        # (the same hazard `integrate` documents for its own lock). Only the
        # successful holder unlinks, and the guard that matters — hand claim
        # vs LIVE dispatcher — never reaches here: the dispatcher's lock is
        # the coordinator's (never unlinked for its process lifetime), so a
        # hand claim always contends against the real file.
        try:
            os.unlink(str(path))
        except OSError:
            pass

    return release, None


def _claim_refusal(root, wi_ids, branch):
    """The claim's refusal ladder: the first reason this claim may not happen,
    or None. Every reason is named; order is cheapest-first. `wi_ids` is the
    admitted batch (WI-381: all spine WIs admit together as ONE claim); the
    per-spec rungs run for every id.

    The `safety_class != ordinary` arm that used to live here is DELETED
    (§A4.1, owner question B): the dispatcher admits, so the claim rung has no
    class authority — what replaced the hard stop is the dispatch-lock
    constraint (`_dispatch_lock`) plus the barrier's wait.

    Implements: SR-156, LLR-151
    """
    paused = ac.tracked_pause(root / "docs")
    if paused is not None:
        return (
            "docs/work/pause is present (since {}: {}) - pause means stop "
            "claiming; unpausing is a reviewed deletion commit".format(
                paused.get("since", ""), paused.get("reason", "")
            )
        )
    if ac.working_tree_dirty(root):
        return "the trunk working tree is dirty - a claim is a clean serial commit"
    code, _ = ac.git(root, "rev-parse", "--verify", "--quiet", "refs/heads/" + branch)
    if code == 0 and not _abandoned_claim(root, wi_ids, branch):
        return "branch {} already exists".format(branch)
    if ".." in branch or "/" in branch or "\\" in branch:
        return (
            "branch name {!r} does not map to a flat claim directory - the queue "
            "handles single-segment branch names".format(branch)
        )
    for wi_id in wi_ids:
        try:
            meta = _spec_frontmatter(_queued_spec(root, wi_id))
        except ValueError as exc:
            return str(exc)
        refusal = _specref_refusal(root, meta, wi_id)  # WI-370
        if refusal:
            return refusal
        refusal = _status_prose_refusal(root, wi_id)  # WI-358
        if refusal:
            return refusal
    import schedule  # sibling; deferred so the cheap refusals above stay cheap

    ready = {r["id"] for r in schedule.frontier(schedule._load(root))}
    missing = [w for w in wi_ids if w not in ready]
    if missing:
        return "{} is not on the ready frontier (unmet needs or not queued)".format(
            ";".join(missing)
        )
    return None


def claim(root, wi_ids, branch, dispatch_lock_held=False):
    """§2.3 steps 1+2 in the order that makes a half-claim BENIGN (§A3).

    `wi_ids` is a single id or the admitted BATCH (WI-381, §A4: all spine WIs
    admit together — one branch, ONE claim commit moving every batched spec).
    `dispatch_lock_held=True` is the live dispatcher's path: it already holds
    `out/agent-loop.lock` for its process lifetime, so the claim must not
    re-acquire (kernel locks are not re-entrant across descriptors). Every
    other caller — the CLI, a hand run, a test — acquires the lock here and
    releases it when the claim ends (`_dispatch_lock` states the authority
    model). A parameter, not a probe, because a held flock cannot be detected
    from inside the same process without conflicting with itself; the threat
    model is the file's usual one (drift and accident, not a caller that
    lies).

    THREE interesting points, not two - the first version of this docstring
    said two and was wrong (REVIEW-A round 1, driven).

    1. Before `commit-tree`. The spec is already `git mv`d and the regen output
       already staged, so a crash here leaves a DIRTY TRUNK with the spec
       moved and no branch. That window is unchanged by the inversion (the old
       order had it too) and it is not this function's to close: the next
       claim's `working_tree_dirty` rung refuses it by name, and dispatch.py's
       cycle-top check turns it into EXIT_PREFLIGHT. Hand repair, but LOUD and
       already fronted.
    2. Between `git branch` and the trunk advance - THE WINDOW THE INVERSION
       MOVES, and the entire reason the driver's `_stranded_claims` existed. TRUNK
       FIRST left a claim no lane could reach: the spec sat in
       `active/<branch>/` on trunk with no branch to build it, invisible to
       the frontier (the WI is no longer queued) and to the parked-resume read
       (no ref). BRANCH FIRST leaves trunk holding the WI in `queued/` while a
       branch sits on a claim commit trunk never took - definitionally an
       abandoned claim, which `_abandoned_claim` convicts and the next claim
       deletes and re-cuts. That is the failure moving to the benign side, and
       the check deleted with it.
    3. After the trunk advance: the claim is complete.

    THE HONEST COST OF THE PLUMBING. `write-tree` + `commit-tree` skip the
    pre-commit hook entirely, and that is more than the freshness floor. The
    regen below covers six of the hook's ten `--run-steps` (arch-map, okf,
    derived-gate, trajectory-map, status-map, open-items); it does NOT cover
    `registry-integrity`, the `trajectory` SSOT check, `skills-sync` or
    `approval-fresh`, and outside `--run-steps` the commit also skips
    `check_privacy --author`, the ALWAYS-ON secrets floor, the `format` step
    and the `commit-msg` hook. Most are vacuous for a pure bookkeeping commit
    whose parent just passed them, but two are not: `approval-fresh` reads the
    registry this commit MUTATES, and the secrets floor would otherwise scan
    the regenerated artifacts. So trunk advances to a commit no hook inspected,
    and the next thing to bar it is a lane's §A2 refresh. Accepted for the
    window it buys, not because nothing is given up.

    Implements: SR-156, LLR-140, LLR-151
    """
    wi_ids = [wi_ids] if isinstance(wi_ids, str) else list(wi_ids)
    # The ladder runs BEFORE the lock for the same reason `integrate` checks
    # dirt before `_slot`: taking the lock creates its own untracked file, and
    # the ladder's clean-trunk rung must not refuse over it on a repo whose
    # ignore rules predate out/. The lock protects the WRITES; the reads it
    # leaves outside cannot race a live dispatcher, because a live dispatcher
    # makes the acquisition below fail outright.
    refusal = _claim_refusal(root, wi_ids, branch)
    if refusal:
        return fail(refusal)
    release = None
    if not dispatch_lock_held:
        release, refusal = _dispatch_lock(root)
        if refusal:
            return fail(refusal)
    try:
        return _claim_locked(root, wi_ids, branch)
    finally:
        if release is not None:
            release()


def _claim_locked(root, wi_ids, branch):
    """`claim` past its ladder, with the dispatch lock settled — the write
    sequence itself."""
    refusal = _drop_abandoned(root, branch)
    if refusal:
        return fail(refusal)
    dest_dir = root / ACTIVE / branch
    dest_dir.mkdir(parents=True, exist_ok=True)
    # The move is the link-aware ritual (WI-393), not a bare `git mv`: the
    # spec's own relative links rebase onto active/<branch>/ and every inbound
    # link follows the move, all inside this one claim commit — the 2026-08-01
    # claim that broke the backlog plan's row links is the driven instance.
    # A batch is the same ritual per spec, all staged into the ONE commit.
    for wi_id in wi_ids:
        spec = _queued_spec(root, wi_id)
        _touched, refusal = spec_move.move_spec(
            root,
            spec.relative_to(root).as_posix(),
            (dest_dir / spec.name).relative_to(root).as_posix(),
        )
        if refusal:
            ac.git(root, "reset", "--hard", "HEAD")
            return fail("the claim move failed (tree restored): {}".format(refusal))
    # The claim changes the registry, which is a generated-artifact input, so
    # the regeneration folds into the claim commit (RULING-6: claims and
    # regeneration are the one bookkeeping lane) - otherwise the claim is
    # blocked by its own freshness floor, which the acceptance run proved live.
    code, out = _run(
        [
            str(ac.harness_python(root)),
            str(SCRIPTS / "trunk_step.py"),
            "--root",
            ".",
            "--regen",
        ],
        root,
    )
    if code != 0:
        ac.git(root, "reset", "--hard", "HEAD")
        return fail(
            "claim regeneration failed (tree restored):\n{}".format(
                ac._failure_tail(out)
            )
        )
    ac.git(root, "add", "-A")
    # The dispatch lock's own file must never ride the claim commit: on a repo
    # whose ignore rules predate out/ the `add -A` above sweeps it in, and the
    # hand-path release then unlinks a now-TRACKED file (WI-381). `reset --`
    # restores the index entry to HEAD's view — unstaged when HEAD has none,
    # untouched when a repo deliberately tracks one.
    ac.git(
        root,
        "reset",
        "-q",
        "--",
        ac.dispatch_lock_path(root).relative_to(root).as_posix(),
    )

    def restore(reason, detail):
        ac.git(root, "reset", "--hard", "HEAD")
        return fail("{} (trunk restored):\n{}".format(reason, ac._failure_tail(detail)))

    code, tree = ac.git(root, "write-tree")
    if code != 0 or not tree.strip():
        return restore("the claim tree could not be named", tree)
    code, commit = ac.git(
        root,
        "commit-tree",
        tree.strip(),
        "-p",
        _head(root),
        "-m",
        "{}\n\nThe §2.3 claim with its regeneration folded in, written BEFORE the\nbranch and before trunk moves onto it (§A3): a crash between the two\nwrites leaves at worst an orphan branch this claim re-cuts, never a\nclaim no lane can reach.".format(
            _claim_subject(wi_ids, branch)
        ),
    )
    if code != 0 or not commit.strip():
        return restore("the claim commit object could not be written", commit)
    commit = commit.strip()
    code, out = ac.git(root, "branch", branch, commit)
    if code != 0:
        return restore("branch cut failed", out)
    code, out = ac.git(root, "reset", "--hard", commit)
    if code != 0:
        # The branch is already correct, so this leaves the benign shape the
        # inversion exists to produce - not a state anyone has to repair.
        return fail(
            "the trunk advance onto claim commit {} failed; {} holds the claim "
            "and trunk did not move, which is the abandoned-claim shape a "
            "re-claim resolves:\n{}".format(commit[:10], branch, out)
        )
    print(
        "integrate: claimed {} on {} (branch cut + trunk advance)".format(
            ";".join(wi_ids), branch
        )
    )
    return 0


def _branch_tree_paths(root, ref, prefix):
    code, out = ac.git(root, "ls-tree", "-r", "--name-only", ref, prefix)
    if code != 0:
        return None
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def finished_branches(root):
    """Claimed branches whose tip moved every spec out of active/<branch>/.

    The closing commit's move to a TERMINAL directory (complete/ or
    cancelled/) IS the finished signal (§2.3 step 3) - no state file, no ref,
    just the tree.

    Implements: SR-156, LLR-140
    """
    active = root / ACTIVE
    if not active.is_dir():
        return []
    done = []
    for spec_dir in sorted(p for p in active.iterdir() if p.is_dir()):
        branch = spec_dir.name
        code, _ = ac.git(
            root, "rev-parse", "--verify", "--quiet", "refs/heads/" + branch
        )
        if code != 0:
            continue
        left = _branch_tree_paths(root, branch, ACTIVE + "/" + branch)
        if left == []:
            done.append(branch)
    return done


def _spec_id(name):
    """The WI id a spec FILENAME carries (`WI-397-slug.md` -> `WI-397`), or None.

    ONE home for the filename->id read, because the claimed set below and the
    R1 mint rung (`_minted_id_refusal`) have to agree exactly on what id a name
    carries: the rung's whole question is "is this id in that set", and two
    parsers that disagree would answer it wrongly in one direction or the other.
    Strict on purpose - the `.md` suffix is required, so a handback's bar-inert
    `docs/work/handback/<branch>.patch` is not a spec by the same extension rule
    that makes it inert to every other checker (handback.ARTEFACTS).
    """
    matched = _SPEC_NAME_RE.match(name)
    return matched.group(1) if matched else None


def _claimed_specs(root, branch):
    """`[(WI id, spec filename)]` the TRUNK holds claimed for this branch."""
    out = []
    for spec in sorted((root / ACTIVE / branch).glob("WI-*.md")):
        # A glob hit carrying no id is not a claimed spec: `claim` only ever
        # writes `WI-<n>-<slug>.md` (it resolves the queued spec by that shape),
        # so anything else here is hand-made residue, and calling it an id would
        # put a non-id in the refusals and the merge message.
        wi_id = _spec_id(spec.name)
        if wi_id:
            out.append((wi_id, spec.name))
    return out


def _claimed_wi_ids(root, branch):
    """The WI ids the TRUNK holds claimed for this branch."""
    return [wi_id for wi_id, _name in _claimed_specs(root, branch)]


def branch_outcomes(root, branch):
    """`({WI id: outcome}, [claimed filenames naming other than ONE outcome])`.

    Read off the BRANCH's own tree against `OUTCOME_DIRS`, so the outcome is
    derived from the same move that made the branch FINISHED - one fact, read
    twice, never two facts to keep in agreement.

    EXACTLY ONE folder, or nothing. A spec that landed in no declared folder
    names none of the three; a spec left in TWO declared folders names two, and
    resolving that silently is worse than either - a dict keyed on the basename
    used to let the last `ls-tree` line win, which is plain alphabetical
    precedence and put `queued` (handback, no verdict owed) ahead of `complete`
    (merged, an APPROVE owed). REVIEW-A round 1 drove it. Both shapes go to
    `unresolved` and the caller refuses, here, where the outcome is read -
    rather than leaning on the duplicate-id ERROR a different script happens to
    raise later.

    That last rule is `kitlib.station.outcome_of` (WI-483): reading the branch
    tree is an EFFECT and stays here, deciding what the read means is a pure
    function over a set of directory names and is testable without a repo.

    Reads BOTH `WORK` and `ARCHIVE_WORK` (WI-504): a close lands its terminal
    move under the archive now, one directory deeper, so the outcome-dir index
    into `path.split("/")` differs per prefix (`docs/work/<outcome>/...` vs
    `docs/archive/work/<outcome>/...`) — stated once per prefix rather than
    inferred, so a spec that happens to land in BOTH trees (never legitimate)
    still resolves to `unresolved` exactly like landing in two dirs of one
    tree always has.
    """
    landed = {}
    for prefix, depth in ((WORK, 2), (ARCHIVE_WORK, 3)):
        for path in _branch_tree_paths(root, branch, prefix) or []:
            parts = path.split("/")
            if len(parts) > depth + 1 and parts[depth] in OUTCOME_DIRS:
                landed.setdefault(parts[-1], set()).add(parts[depth])
    outcomes, unresolved = {}, []
    for wi_id, name in _claimed_specs(root, branch):
        outcome = outcome_of(landed.get(name) or ())
        if outcome is None:
            unresolved.append(name)
        else:
            outcomes[wi_id] = outcome
    return outcomes, unresolved


def _minted_id_refusal(root, branch, claimed):
    """RULING R1 (owner, 2026-08-01): the merge slot's MINT refusal - a refusal
    string, or None.

    A WORK BRANCH NEVER MINTS A WORK-ITEM ID; minting is a serial TRUNK-side act
    only. A new work item takes `max(existing id) + 1`, and a lane can only see
    its own tree - so on 2026-08-01 two lanes independently minted the same
    `WI-392`, while three rows existed only on one unmerged branch and held
    trunk's max BELOW them, which would have re-collided on the next trunk mint.
    The alternatives coordinate that state (a reservation table in the
    dispatcher, lane-namespaced ids renumbered at merge); this deletes it. An id
    a branch cannot create cannot collide, and the id-reservation question
    leaves the dispatcher's scope before that row is built.

    THE SAME SHAPE AS `_claim_refusal`, AT THE OTHER END OF THE LANE'S LIFE: one
    named refusal, read off git, in front of the one act that would make the bad
    state real.

    WHAT IS READ. The branch's OWN `docs/work/` delta - `merge-base(trunk,
    branch)` to the tip - so trunk-side minting stays exactly as free as it is
    today (the claim's bookkeeping commit, WI-388's mechanical adjudication
    mint, a human commit): whatever trunk did sits in the BASE, not in the diff.
    Only ADDS count, and only of a spec FILENAME (`_spec_id`), which is what
    leaves every allowed move alone without a second policy engine to say so:

      * a terminal-outcome move (`active/<branch>/` -> `complete/`, `cancelled/`)
        and a handback's return to `queued/` both re-ADD a file whose id the
        branch already holds claimed, so the id is in the set;
      * an EDIT to a claimed row's body arrives as `M`, never `A`;
      * a handback's bar-inert `docs/work/handback/<branch>.patch` carries no
        spec filename at all.

    `--no-renames` is load-bearing, not tidiness: with rename detection on, git
    is free to pair a newly minted spec against the DELETE side of the branch's
    own close - spec files are short and near-identical in shape - and the mint
    would arrive as one `R` record with no add left to see. `_abandoned_claim`
    splits its diff for the same reason.

    THE HONEST BOUND, the same one `refresh_attestation` states: this defeats
    the accident (a lane filing a follow-up where it is working) and not a lane
    that means to. A branch can still commit an id-bearing row as prose in some
    other file, and nothing here reads a file that is not a spec. That is the
    threat model the rest of this script holds - drift and a lane that goes
    wrong, not a lane that lies - and the remedy for the accident is what the
    ruling asked for: lane-discovered findings are recorded as PROSE and take an
    id at or after merge.
    """
    head = _head(root)
    code, base = ac.git(root, "merge-base", head, branch)
    if code != 0 or not base.strip():
        # Fail closed: an unread delta is not an empty one.
        return (
            "cannot read the merge base of trunk {} and {}, so the {} delta the "
            "R1 mint rung reads is unknowable; nothing was merged:\n{}".format(
                head[:10], branch, WORK, ac._failure_tail(base)
            )
        )
    code, out = ac.git(
        root,
        "diff",
        "--name-status",
        "--no-renames",
        base.strip(),
        branch,
        "--",
        WORK,
    )
    if code != 0:
        return "cannot read {}'s {} delta against {}; nothing was merged:\n{}".format(
            branch, WORK, base.strip()[:10], ac._failure_tail(out)
        )
    foreign = []
    for status, path in _name_status(out):
        if not status.startswith("A"):
            continue
        wi_id = _spec_id(path.rsplit("/", 1)[-1])
        if wi_id and wi_id not in claimed:
            foreign.append((wi_id, path))
    if not foreign:
        return None
    return (
        "{} ADDS work-item spec(s) carrying {} outside its claimed set ({}) - a "
        "WORK BRANCH NEVER MINTS A WORK-ITEM ID (owner ruling R1, 2026-08-01: "
        "minting is a serial TRUNK-side act only, so an id two lanes could pick "
        "at once is unrepresentable rather than coordinated around). Record the "
        "finding as PROSE - the spec body, the log fragment, the review record - "
        "and let it take its id at or after merge, on trunk; nothing was "
        "merged:\n{}".format(
            branch,
            "an id" if len(foreign) == 1 else "ids",
            ", ".join(sorted(claimed)) or "empty",
            "\n".join("  {} minted at {}".format(w, p) for w, p in foreign),
        )
    )


def _last_commit_time(root, ref, *pathspec):
    code, out = ac.git(root, "log", "-1", "--format=%ct", ref, "--", *pathspec)
    if code != 0 or not out.strip():
        return None
    return int(out.strip().splitlines()[0])


def _commit_message(root, rev):
    """The full commit message of `rev`, or "" when it cannot be read."""
    code, out = ac.git(root, "log", "-1", "--format=%B", rev)
    return out if code == 0 else ""


def _rev(root, rev):
    """`rev` resolved to a full sha, or None."""
    code, out = ac.git(root, "rev-parse", "--verify", "--quiet", rev)
    return out.strip() if code == 0 and out.strip() else None


def refresh_attestation(root, branch, rev=None):
    """`(work_tip_sha, bar summary)` if `rev` is a GENUINE refresh commit for
    `branch`, else None. `rev` defaults to the branch tip.

    The bar is attested to a TREE, and this is where that sentence is made
    true rather than merely written down. A commit message is not evidence: it
    can be copied, hand-written, amended onto different content, cherry-picked
    or rebased, and every one of those carries the words onto a tree nobody
    barred (REVIEW-A round 1, driven both ways - a forged trailer on an
    ordinary work commit, and `commit --amend` adding a file to a real one).

    So the trailer NAMES what it attests and all three names are verified
    against git:

        Bar-Green: tree=<40 hex> work=<40 hex> <bar summary>

      * `tree=` must equal the commit's OWN tree. This is the load-bearing one:
        no edit that changes content can keep it, because the tree sha IS the
        content. `git write-tree` is what lets the refresh know the value
        before it commits - the index it barred is the tree it commits.
      * `work=` must equal the commit's first parent, so the disposable-commit
        peel below has a stated target rather than a guessed one, and a
        cherry-pick or rebase (new parent) is rejected.
      * the SUBJECT must be this branch's own `refresh: <branch> onto trunk`,
        so a refresh commit merged in from elsewhere is not read as this
        branch's.

    THE HONEST BOUND: this defeats ACCIDENT, not INTENT. Every accidental
    carrier refuses - a copied message, an amend, a rebase, a cherry-pick, a
    trailer quoted in an ordinary commit. But forging one deliberately is FOUR
    git invocations in the lane worktree and no bar at all: `add -A`, `T=$(git
    write-tree)`, `P=$(git rev-parse <branch>)`, and the `commit` that carries
    those two values in the trailer. REVIEW-A round 2 drove exactly that and landed an
    unbarred file on trunk. The format is printed in every refresh commit, so
    the cost is reading, not reverse-engineering.

    That is accepted, deliberately. The only structural closure is a bar the
    slot itself runs and cannot skip, and DECISION 3 (owner ruling 2026-07-31)
    deleted the merge bar outright: a kept-just-in-case bar is exactly the
    shape §0's governing principle warns against. So the threat model here is
    the same one the rest of this script holds - bugs, drift and a lane that
    goes wrong, not a lane that lies on purpose. A lane is trusted code the
    operator chose to run. If that ever stops being true, the answer is a
    slot-side bar and a reopened DECISION 3, not a longer trailer.
    """
    rev = rev or branch
    message = _commit_message(root, rev)
    lines = message.splitlines()
    if not lines or not lines[0].strip().startswith(_refresh_subject(branch)):
        return None
    matched = None
    for line in lines:
        matched = _ATTEST_RE.match(line.strip())
        if matched:
            break
    if not matched:
        return None
    tree, work, summary = matched.group(1), matched.group(2), matched.group(3)
    if _rev(root, rev + "^{tree}") != tree:
        return None  # the message rode onto a tree it does not describe
    if _rev(root, rev + "^1") != work:
        return None  # ...or onto a different parent than the one it names
    return work, summary.strip()


def _work_tip(root, branch):
    """The branch's last WORK commit as a sha: the tip, with any refresh commit
    peeled off at the work sha that refresh ITSELF recorded.

    Two callers, one meaning. `refresh` resets here before it merges (the
    §A2.1 disposable-commit rule: a retry never stacks a second merge on the
    first, because docs/log.md is append-compiled and the stack would conflict
    on the file end). `_verdict_gate` measures code-time here, because the
    refresh is MECHANICAL bookkeeping - it rewrites the compiled log and the
    generated artifacts, and if that counted as code it would stale the honest
    APPROVE that had to precede it.

    The peel is why `refresh_attestation` had to become a verification rather
    than a substring test: this function feeds a `reset --hard`, so peeling one
    commit too far DESTROYS committed work. A work commit whose message merely
    quoted the trailer used to be peeled, and its file left the branch (REVIEW-A
    round 1, driven). Now nothing is peeled that does not carry its own tree and
    parent, which an ordinary commit cannot do by accident.
    """
    rev = branch
    for _ in range(_MAX_REFRESH_PEEL):
        attested = refresh_attestation(root, branch, rev)
        if attested is None:
            return _rev(root, rev)
        rev = attested[0]
    return _rev(root, rev)


def _verdict_gate(root, branch, outcomes):
    """RULING-7: the dialed verdict artifacts, fresh at the branch's work tip.

    review-policy >= 1 demands docs/reviews/WI-<n>-REVIEW-A.md per closed WI,
    carrying an APPROVE machine line, whose last commit on the branch is no
    older than the last non-review, non-fragment commit - the git-derived
    replacement for the old sha7-in-filename binding (§5.4 left it open).

    `docs/work/` is NOT excluded, deliberately, and WI-378 measured the price
    before leaving it that way. The population is derivable, not chosen - all
    three steps, so this is re-runnable from what ships:

        # 1. the commit that introduced this comparison
        git log --reverse -S"_verdict_gate" -- <path to this file>
        # 2. every integrator merge
        git log --format="%H %s" --grep="^integrate: merge"
        # 3. keep the ones the predicate governed
        git merge-base --is-ancestor <commit from 1> <merge from 2>

    That gave 20 merges as of 2026-08-01, `review-policy` at 1 throughout.
    Replaying the predicate over all 20 found 13 staled APPROVEs: nine staled by
    a real change to shipping code or a declared doc, one by a hand trunk merge,
    and three by a record-only edit that followed its own verdict. Adding
    `docs/work/` here would buy back those three (23.1%) and nothing else, at
    the cost of letting a spec's `safety_class`, `needs` and `Deliverable` - the
    claims the verdict is ABOUT - change after the APPROVE, unseen. One of the
    three is exactly that: a `Deliverable` prose fix the verdict demanded. The
    ordering rules that shrink the class - close before the final verdict round,
    never hand-merge trunk - are in process-options.md, "The LLM-gate verdict
    protocol"; they are necessary, not sufficient, since a verdict's own finding
    can demand a record edit no ordering could have placed earlier. Follow them
    and the case is weaker still: they retire 2 of the 13, leaving 11 of which
    the exclusion would buy back 2 (18.2%) - and both of those rounds caught a
    false claim in the record.

    `docs/log.d/` differs on purpose: a log fragment is the narrative of work
    the verdict already read, carries no key any reader gates on, and is
    append-compiled on the trunk rather than merged.

    KEYED OFF THE OUTCOME, NOT OFF THE CLAIM (§A3). Only `merged` asserts the
    work is done, and only an assertion of done owes a verdict; `cancelled` and
    `handback` assert the opposite - this will never be built, or this is coming
    back unfinished - so an APPROVE would be an approval of nothing. Reading the
    requirement off the claim instead would deadlock the commonest handback
    cause on itself: a review escalation is precisely the case where no APPROVE
    exists, and the lane would be unable to return the work it could not get
    approved.

    THE TWO RULES MEET AT ONE POINT, stated so nobody has to re-derive it from
    the loop: the freshness comparison above only ever runs for an id whose
    outcome is `merged`, because the others are skipped before reaching it. So
    WI-378's `docs/work/` reasoning governs exactly the branches that assert
    done - which is also the only place its ordering rule ("close before the
    final verdict round") can bite, since the closing MOVE is itself a
    `docs/work/` change. Neither rule weakens the other: a returned or
    cancelled spec moves under `docs/work/` too, and owes no verdict for that
    move to stale.

    Implements: SR-156, LLR-140
    """
    # SN-028: the mixed-config refusal first - a repo declaring the reviewer
    # dial in BOTH homes must not have the merge slot pick one of them.
    conflicts = ac.config_conflicts(root / "docs")
    if conflicts:
        return conflicts[0]
    dial = ac.declared_policy(root / "docs", "review-policy", "0")
    try:
        required = int(dial or "0") >= 1
    except ValueError:
        # The message still names the LEGACY file: it is the shape an operator
        # can be holding either way, and `declared_policy` renders the TOML int
        # in the same string vocabulary, so a non-integer here means a
        # hand-edited legacy file (a TOML non-int falls back to the default).
        return "docs/review-policy is not an integer: {!r} (fail closed)".format(dial)
    if not required:
        return None
    code_time = _last_commit_time(
        root,
        _work_tip(root, branch),
        ".",
        ":(exclude)docs/reviews",
        ":(exclude)docs/log.d",
    )
    for wi in sorted(outcomes):
        if outcomes[wi] != Outcome.MERGED:
            continue
        rel = "docs/reviews/{}-REVIEW-A.md".format(wi)
        code, text = ac.git(root, "show", "{}:{}".format(branch, rel))
        if code != 0:
            return "required verdict {} is absent from {}".format(rel, branch)
        word = score_reviews.parse_verdict(text).verdict
        if word != "APPROVE":
            return "{} is not an APPROVE (parsed: {!r})".format(rel, word)
        vtime = _last_commit_time(root, branch, rel)
        if vtime is None or (code_time is not None and vtime < code_time):
            return (
                "{} predates the branch's last code commit - a stale APPROVE "
                "does not clear the gate".format(rel)
            )
    return None


def lane_worktree(root, branch):
    """The lane worktree holding `branch`: `(path, error)`, created if needed.

    Order matters. A REGISTERED holder wins - the worker's own tree, wherever
    the operator put it - because the refresh must land where the lane can fix
    a red. Only when nothing holds the branch is one added at the lane home,
    which is the ordinary case for work built by hand between runs; §5.6's
    unload GCs it after the merge, so the creation owns no teardown of its own.

    The MAIN checkout can be that holder (attended serial work), and this
    function still returns it - but `refresh` refuses that case outright, since
    a main checkout sitting on the branch means the repo has no trunk checked
    out to merge in. The refusal lives there rather than here because the
    worker has no such problem.
    """
    holder, _is_primary = _worktree_holding(root, branch)
    if holder is not None:
        return holder, None
    wt = root.parent / (root.name + LANE_WORKTREE_SUFFIX) / branch
    if wt.is_dir():
        return None, "{} exists but does not hold {} - refusing to clobber it".format(
            wt, branch
        )
    ac.git(root, "worktree", "prune")
    code, out = ac.git(root, "worktree", "add", str(wt), branch)
    if code != 0:
        return None, "worktree add failed for {}: {}".format(
            branch, ac._failure_tail(out)
        )
    return wt, None


def trunk_is_ancestor(root, branch):
    """THE CONSTRAINT (§A2): is the trunk's HEAD already an ancestor of `branch`?

    One git command, and git is the arbiter - which is the whole difference
    between this and the speculation that failed historically (§A2.0): there is
    no reservation ref, no compare-and-swap, no run-state file to reconcile. A
    lost race has nothing to undo, because the loser simply redoes a refresh it
    would have owed anyway going second.
    """
    code, _ = ac.git(root, "merge-base", "--is-ancestor", _head(root), branch)
    return code == 0


def _head(root):
    code, out = ac.git(root, "rev-parse", "HEAD")
    if code != 0:
        raise RuntimeError("rev-parse HEAD failed: {}".format(out))
    return out.strip()


def _declared_bar_or_refusal(root):
    """§4: a missing or EMPTY check declaration is a refusal, never a skip - and
    so is a declared bar with no floor-satisfying interpreter to run it on.

    WI-361: this is the surviving home of the WI-286 harness floor, which had
    exactly one enforcement point (the deleted dispatcher's preflight). It runs
    HERE, ahead of the compose/merge/bar sequence in `integrate_one`, so a
    declared-toolchain repo without its pinned .venv is a named refusal rather
    than a silent ambient-Python bar run whose green may be false. The guard
    arms only on a repo that declares the pinned toolchain - see
    `agent_common.harness_floor_failures`."""
    ini = root / "docs" / "stack.ini"
    if not ini.exists():
        return "docs/stack.ini is absent - the required bar is undeclared"
    argv = ac._declared_test_command(ini)
    if argv is None:
        return "no [product] test declaration - the required bar is undeclared"
    if argv == []:
        return "[product] test is declared but EMPTY - a misconfiguration, not a skip"
    floor = ac.harness_floor_failures(root)
    if floor:
        return "the harness floor REFUSES this bar run: " + floor[0]
    return None


def _run(argv, cwd):
    """One captured child run: (returncode, stdout+stderr folded). The single
    subprocess seam for the bar and the trunk step, so the capture keywords
    have one home in this file."""
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, out


def _branch_tree_script(wt, root, name):
    """The BRANCH tree's copy of harness script `name`, else the invoker's.

    The trunk step and the bar must be the refreshed branch's own: a work
    branch may change a generator or the harness itself, and regenerating that
    tree with the invoker's trunk-vintage copy writes artifacts the refresh
    commit's own floor - which runs the branch's version - then refuses them as
    stale (WI-368, first hit by WI-366's renderer change). The invoker is
    trunk-vintage whenever dispatch.py drives the loop in-process, so this cannot
    be simplified to "the module that is running". Discovery mirrors the
    shipped hook's scripts-dir probe: the invoker's root-relative layout first,
    then the known layouts; the invoker's copy is the fallback so a branch that
    predates the script (or a root the invoker sits outside of) still
    integrates.
    """
    rels = []
    try:
        rels.append(SCRIPTS.relative_to(root))
    except ValueError:
        pass
    rels.extend((Path("scripts"), Path("project-trajectory") / "scripts"))
    for rel in rels:
        cand = wt / rel / name
        if cand.is_file():
            return cand
    return SCRIPTS / name


def _passed_steps(out):
    """The DISTINCT step names check.py's output reports as PASS.

    Counted by name, not by line (WI-377): under --jobs each step's status
    line prints twice - once by the lane runner as it finishes, once in the
    final summary block - so a line count reported a 20-step bar as "40
    steps", a false measurement in the merge record. Distinct names give the
    same answer at --jobs 1 and --jobs N.
    """
    names = set()
    for ln in out.splitlines():
        if re.match(r"\s*PASS\s", ln):
            parts = ln.split()
            if len(parts) >= 2:
                names.add(parts[1])
    return names


def _run_bar(wt, root, tier, gate=None):
    """check.py at the derived gate on the refreshed branch; fail-closed reading.

    Green means: exit 0 AND the report carries no SKIP line. `--trunk-lane` is
    passed because the tree being barred IS the tree that becomes trunk (the
    --no-ff merge of a branch containing trunk reproduces it byte for byte), so
    the §5.2 freshness gates - which stand down on a work branch, and which
    this very step just regenerated - have to run here or nothing checks them.

    `gate` (WI-388, the `bar` frontmatter key) pins check.py's --gate: a row
    claimed to deliver evidence at a level still bars at that level if
    docs/gate moves mid-flight. None keeps check.py on its own derived-gate
    read, exactly as before.
    """
    py = ac.harness_python(root)
    check = _branch_tree_script(wt, root, "check.py")
    argv = [str(py), str(check), "--jobs", "0", "--tier", tier, "--trunk-lane"]
    if gate:
        argv += ["--stage", gate]
    code, out = _run(argv, wt)
    skips = [ln for ln in out.splitlines() if re.match(r"\s*SKIP\s", ln)]
    if code != 0:
        return False, out, "bar exit {}".format(code)
    if skips:
        return (
            False,
            out,
            "bar reported SKIP - a skip is a refusal here:\n" + "\n".join(skips),
        )
    return (
        True,
        out,
        "bar PASS ({} steps, tier {}{})".format(
            len(_passed_steps(out)), tier, ", gate " + gate if gate else ""
        ),
    )


def _run_trunk_step(wt, root):
    py = ac.harness_python(root)
    step = _branch_tree_script(wt, root, "trunk_step.py")
    return _run([str(py), str(step), "--root", "."], wt)


# The `bar` frontmatter key's vocabulary (WI-388; the stage-ladder names since
# OI-21): bar declares verification strictness for this row's lane; it never
# affects scheduling. Ordered weakest to strictest so a batch takes the
# STRICTEST — by LADDER POSITION, never by `max()` on the string. The retired
# tags alphabetized, so `max()` was accidentally right; `DevStg-Tests` sorts
# above `DevStg-Impl`, so it is now accidentally WRONG in the permissive
# direction, which is exactly the class of bug the label carrier makes loud.
_BAR_GATES = ("DevStg-Reqs", "DevStg-Tests", "DevStg-Impl")

# A WI `bar:` is AUTHOR-WRITTEN, so the retired tags translate on read (OI-21
# contract break 3) — silently, because check_vocab.py sees the spec file and can
# name the line. Duplicated from intake.normalize_bar per the F5 rule.
_RETIRED_BARS = {
    "g1": "DevStg-Reqs",
    "g2": "DevStg-Tests",
    "g3": "DevStg-Impl",
    # The `DevBar-*` prefix, retired 2026-08-18 (one vocabulary; the verb
    # carries the axis). Keyed lower-case like the rows above, since this
    # table is looked up case-insensitively. The Release row translates to
    # `DevStg-Impl`, NOT to `DevStg-Release`: that bar closed the Impl rung
    # and `DevStg-Release` is not clearable at all, so the alias carries the
    # correction rather than a bare prefix swap.
    "devbar-reqs": "DevStg-Reqs",  # check_vocab: allow
    "devbar-tests": "DevStg-Tests",  # check_vocab: allow
    "devbar-release": "DevStg-Impl",  # check_vocab: allow
}


def _normalize_bar(value):
    """A `bar:` cell as a canonical `DevStg-*` name ("" when blank), retired tags
    translated. Matched case-insensitively — the retired reader did `.upper()`,
    which would turn a correctly-authored `DevStg-Reqs` into `DEVBAR-REQS` and
    refuse it."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    low = raw.lower()
    if low in _RETIRED_BARS:
        return _RETIRED_BARS[low]
    for canonical in _BAR_GATES:
        if low == canonical.lower():
            return canonical
    return raw


# The surfaces an adjudication lane's non-refresh delta may touch and still
# take the NO-BAR path (WI-388 REVIEW-A finding 1) — §A5.2's premise ("it
# touches Status cells and the work registry, nothing a product bar can speak
# to") made CHECKED rather than asserted. Derived from what the kind's ruled
# outcomes actually write: the work registry (spec moves, dispositions,
# drafted follow-ups), the three spine registries (the Status flip — the
# path-level bound is the honest checkable one; the cell-level judgement
# belongs to the amendment seam and the verdict round), the open-items
# registry ("surface an open item" is a ruled R3 outcome), the derived stage
# the flip recovers, and the record surfaces (the log fragment, the review
# verdicts). The declared [generated] set joins at read time — the trunk step
# owns those and a lane's refresh regenerates them anyway, which is why
# `docs/stage` needs NO row of its own here: it is declared `[generated]`, so
# it arrives with that set. (Its predecessor `docs/gate` was listed literally
# and RETIRED at WI-498 slice 5; a dead pathspec silently NARROWS this
# allowlist, failing lanes toward the full bar for no reason.)
_ADJUDICATION_SURFACES = (
    "docs/work/",
    # WI-504 (OI-55 ruled (a)): a disposition's terminal close now moves the
    # spec under the archive, one directory deeper — without this row that
    # exact move (spec moves are named above as a ruled disposition outcome)
    # would fail an adjudication lane off the no-bar path.
    "docs/archive/work/",
    "docs/log.d/",
    "docs/reviews/",
    # BOTH carrier paths per spine tier: this is a pathspec
    # allowlist matched against `git diff --name-only`, and a repo that has not
    # migrated stages the `.csv` name. Naming one suffix would fail the lane
    # TOWARD the full bar there — safe, but wrong, and invisible until someone
    # wonders why adjudication never takes the cheap path.
    "docs/requirements/system-requirements.toml",
    "docs/requirements/system-requirements.csv",
    "docs/requirements/low-level-requirements.toml",
    "docs/requirements/low-level-requirements.csv",
    "docs/test/test-cases.toml",
    "docs/test/test-cases.csv",
    "docs/requirements/open-items.toml",
    "docs/requirements/open-items.csv",
    # SR-144's per-close reports: an adjudication lane READS them and, on an
    # override, may write a corrective one. Without this row a lane that
    # touches a report falls off the no-bar path into the full bar — a
    # ~11-minute penalty for editing a document no product bar can speak to.
    "docs/handbacks/",
)


def _adjudication_scope_ok(root, branch):
    """May this adjudication-only lane take the no-bar path? True only when
    the branch's NON-REFRESH delta — merge-base(trunk, branch) to the peeled
    work tip, the same branch-delta read `_minted_id_refusal` makes at the
    same slot — touches nothing outside `_ADJUDICATION_SURFACES` plus the
    declared [generated] set.

    ANY other path — product code above all — fails TOWARD the full bar:
    REVIEW-A drove a product file with a red check harness through the no-bar
    arm onto trunk with the harness never invoked, an un-run green against
    §A8's fixed points ("no un-run greens; the harness is still the bar").
    Unreadable git answers False, the same direction."""
    code, base = ac.git(root, "merge-base", _head(root), branch)
    if code != 0 or not base.strip():
        return False
    code, out = ac.git(
        root,
        "diff",
        "--name-only",
        "--no-renames",
        base.strip(),
        _work_tip(root, branch),
    )
    if code != 0:
        return False
    allowed = list(_ADJUDICATION_SURFACES) + _generated_paths(root)
    for raw in out.splitlines():
        path = raw.strip().replace("\\", "/")
        if path and not any(
            path == entry.rstrip("/")
            or (entry.endswith("/") and path.startswith(entry))
            for entry in allowed
        ):
            return False
    return True


def _lane_bar_directives(root, branch):
    """The claimed rows' say over the refresh bar (WI-388): `(skip, gate,
    refusal)`.

    * `skip` — True when EVERY claimed spec declares the `adjudication` kind:
      adjudication runs NO bar (§A5.2 — its outputs are Status cells and the
      work registry, nothing a product bar can speak to; that is why the kind
      needs its own no-bar arm rather than a tier). Fails TOWARD the bar: an
      unreadable frontmatter or a mixed batch runs it.
    * `gate` — the strictest `bar` key among the claimed rows (DevStg-Reqs < DevStg-Tests < DevStg-Impl),
      handed to check.py --gate. None when no row declares one.
    * `refusal` — a malformed bar value. Refused loudly rather than silently
      barred at whatever the derived gate happens to read (the drift the key
      exists to pin); the claimed spec is on the branch, so the fix is a
      lane-side edit.

    Read off the TRUNK's claimed specs — the same one-home read the merge slot
    and `dispatch._branch_exclusive` use — so the directive cannot disagree
    with the claim being merged.

    Implements: SR-174, LLR-154
    """
    kinds, bars = [], []
    for _wid, name in _claimed_specs(root, branch):
        try:
            meta = _spec_frontmatter(root / ACTIVE / branch / name)
        except (OSError, ValueError):
            return False, None, None  # unreadable: run the bar, fail toward it
        kinds.append(str(meta.get("safety_class") or "").strip().lower())
        declared = _normalize_bar(meta.get("bar"))
        if declared and declared not in _BAR_GATES:
            return (
                False,
                None,
                "{} declares bar = {!r} ({}), which is not one of {} - the bar "
                "key declares verification strictness for this row's lane (it "
                "never affects scheduling), so a value check.py cannot run is "
                "refused rather than silently dropped; fix the claimed spec on "
                "the branch, then refresh".format(
                    branch, str(meta.get("bar")), name, "|".join(_BAR_GATES)
                ),
            )
        if declared:
            bars.append(declared)
    skip = bool(kinds) and all(kind == "adjudication" for kind in kinds)
    # The scope rung (REVIEW-A finding 1): the kind alone never earns the
    # no-bar path — the branch's delta must LOOK like adjudication too.
    if skip and not _adjudication_scope_ok(root, branch):
        skip = False
    strictest = max(bars, key=_BAR_GATES.index) if bars else None
    return skip, strictest, None


def _worktree_holding(root, branch):
    """The registered worktree with `branch` checked out: `(path, is_primary)`,
    or `(None, False)`.

    Reads `ac.worktree_records` (the one shared porcelain walk). Git always
    lists the MAIN checkout first, so record index 0 identifies the primary -
    which can never be `git worktree remove`d and must not be described to
    the operator as a worker worktree."""
    for i, (path, held) in enumerate(ac.worktree_records(root)):
        if held == branch:
            return (Path(path) if path else None), i == 0
    return None, False


def _worktree_dirt(wt):
    """The GC-safety read for one worktree: the `git status --porcelain
    --ignored=matching` lines, or a synthetic line when git itself could not
    answer. Non-empty means DO NOT REMOVE.

    IGNORED files are counted here, unlike `ac.working_tree_dirty` (whose
    tracked-dirt contract other callers depend on and which stays as it is): a
    worker worktree's only unique content is routinely ignored - the unredacted
    `out/run-logs/` session stream, a local `.env` - and `git worktree remove`
    deletes it without a word.

    Fail direction: a NONZERO git exit reads as DIRTY, never clean. An
    unreachable, corrupt or permission-denied worktree is the last thing to
    delete on a guess, and a fail-open read here would be the one fail-open in
    a fail-closed script.
    """
    code, out = ac.git(wt, "status", "--porcelain", "--ignored=matching")
    if code != 0:
        return [
            "!! git status could not read this worktree (treated as dirty): {}".format(
                out.strip() or "(no output)"
            )
        ]
    return [ln for ln in out.splitlines() if ln.strip()]


# The DECLARED tool-residue set §5.6's unload may shed before judging dirt
# (WI-400). Measured 2026-08-01: every lane of that day's drain arrived at the
# merge slot holding the IDENTICAL six ignored paths - .pytest_cache/,
# .ruff_cache/, __pycache__/ trees and the gitignored generated trace report -
# so every worker-built lane ended UNLOAD INCOMPLETE forever, and each unload
# was finished by hand. None of these names can hold evidence that exists
# nowhere else: the caches are rebuilt by the next tool run, the report by the
# next trace.py run. A short enumerated list on purpose - not a glob
# configuration surface and not a dial; everything outside it stays evidence.
# Widened on measurement, once (WI-407): check.py passes --html to its trace
# step at DevStg-Tests/DevStg-Impl, so the declared bar writes docs/test/report.html in whatever
# lane it runs in, and on 2026-08-02 the wi-402 lane was measured holding
# exactly that file at unload - same class as report.md, rebuilt by the next
# bar run, sole-copy evidence never.
_RESIDUE_DIR_NAMES = frozenset({".pytest_cache", ".ruff_cache", "__pycache__"})
_RESIDUE_FILES = frozenset({"docs/test/report.md", "docs/test/report.html"})
# The loop's OWN artifacts (C6, docs/plans/2026-08-30-stall-guard-plan.md):
# the raw per-session streams agent_loop itself wrote for THIS lane under
# out/run-logs/ (their clipped, tracked copies live under docs/iteration/),
# and out/review-owed, the C2 parked-state marker, moot once the lane merged.
# Measured 2026-08-30: every mechanized lane ended UNLOAD INCOMPLETE over
# exactly these, ending the run after every merge. Same double lock as the
# caches: ignored by git AND declared here — never sole-copy evidence.
#
# Declared BY NAME, never by directory (WI-548 round 4): a stream is
# `<train>-<NNN>-<YYYYMMDD>-<HHMMSS>.log`, the shape `agent_loop.write_raw_stream`
# produces, and ONLY that shape is the loop's. Anything else under
# out/run-logs/ — an operator's notes, a foreign log — is a surprise, and a
# surprise is evidence that refuses the unload by name.
# out/agent-loop.lock is the loop's OWN per-checkout coordinator lock, dead once
# its process exited (measured 2026-08-31: it held WI-547's lane after the shed).
_RESIDUE_STREAM_RE = re.compile(r"^out/run-logs/[^/]+-\d{3}-\d{8}-\d{6}\.log$")
_RESIDUE_STREAM_DIRS = ("out/run-logs/",)
_RESIDUE_OUT_FILES = frozenset({"out/review-owed", "out/agent-loop.lock"})


def _is_declared_residue(rel):
    """True when repo-relative posix path `rel` is DECLARED tool-residue.

    Two shapes only: an exact generated-report path, or a file anywhere inside
    a directory carrying one of the declared cache names (the caches appear at
    every depth the tools run at - `__pycache__/` beside each package,
    `.pytest_cache/` at the rootdir). The file's own NAME never matches - a
    file merely named `.pytest_cache` is a surprise, and a surprise is
    evidence."""
    if rel in _RESIDUE_FILES or rel in _RESIDUE_OUT_FILES:
        return True
    if _RESIDUE_STREAM_RE.match(rel):
        return True
    return any(part in _RESIDUE_DIR_NAMES for part in rel.split("/")[:-1])


def _shed_declared_residue(wt):
    """Delete the declared tool-residue from a merged lane worktree.

    `_shed_residue` cannot cover this case by design: it sheds only what the
    REFRESH'S OWN bar added (a before/after baseline), while the residue that
    held every 2026-08-01 lane was the WORKER'S - written before the station
    ever saw the branch. So the unload gets its own shed, locked twice: a path
    must be IGNORED by git (`ignored_files`; a trackable file is evidence) AND
    match the declared set. Nothing is deleted when git cannot enumerate - the
    fail direction stays closed, like `_worktree_dirt`'s.

    Directories go the same way: after the files, `_sweep_residue_dirs` clears
    the emptied cache trees (git status --ignored reports an empty ignored
    directory, so leaving the husk would re-refuse the unload over nothing).
    The caller re-reads the dirt afterwards and judges on what is actually
    left - this function returns nothing.
    """
    ignored = ignored_files(wt)
    if ignored is None:
        return
    for rel in sorted(ignored):
        if not _is_declared_residue(rel):
            continue
        target = wt / rel
        try:
            if target.is_file() or target.is_symlink():
                target.unlink()
        except OSError:
            # Left behind rather than fought over: the re-read reports it as
            # dirt, which is a loud, recoverable outcome.
            continue
    _sweep_residue_dirs(wt)


def _sweep_residue_dirs(wt):
    """`_shed_declared_residue`'s directory half, split out to keep each half
    under the complexity ceiling: rmdir every now-EMPTY directory inside a
    declared cache tree, bottom-up. `rmdir` refuses a non-empty directory, so
    a cache dir still holding an undeclared or unremovable file survives to be
    reported as dirt. Locked twice like the files (WI-407, REVIEW-A finding
    3): the name lock AND `git check-ignore` - emptiness git does not ignore
    is the lane's, because emptiness can be load-bearing (this repo's own
    `docs/work/deferred/` is an empty directory a link resolves through). The
    fail direction stays closed: a check git cannot answer skips the rmdir."""
    for parent, _dirs, _files in os.walk(wt, topdown=False):
        directory = Path(parent)
        if directory == wt:
            continue
        rel_parts = directory.relative_to(wt).parts
        rel_posix = "/".join(rel_parts) + "/"
        # A directory inside a declared prefix (out/run-logs/) — or an
        # ancestor of one (out/ itself, once the streams are shed and nothing
        # else lives there) — is sweepable exactly like the named cache trees;
        # rmdir still refuses anything non-empty, so a surprise survives.
        declared_prefix = any(
            rel_posix.startswith(p) or p.startswith(rel_posix)
            for p in _RESIDUE_STREAM_DIRS
        )
        if ".git" in rel_parts or not (
            declared_prefix or any(part in _RESIDUE_DIR_NAMES for part in rel_parts)
        ):
            continue
        if ac.git(wt, "check-ignore", "-q", "--", "/".join(rel_parts))[0] != 0:
            continue
        try:
            directory.rmdir()
        except OSError:
            continue


def _unload_branch(root, branch):
    """§5.6 unload of a merged work branch: (fully_unloaded, message).

    `git branch -d` refuses a branch checked out in a linked worktree, and
    swallowing that refusal is how the old dispatcher accumulated 36 stale
    worktrees - so every outcome is reported by branch AND by holding path.

    The GC is owned only where it is safe: a CLEAN linked worktree is removed
    and the delete retried; a DIRTY one is reported and LEFT, never forced, and
    the MAIN checkout is never removed at all. A worktree can hold orphaned
    files that exist nowhere else (2026-07-26), so dirt is evidence, not
    garbage - but the DECLARED tool-residue set is shed first (WI-400), because
    a cache the bar rebuilds on every run is the one kind of dirt that
    provably is.
    """
    code, out = ac.git(root, "branch", "-d", branch)
    if code == 0:
        ac.git(root, "worktree", "prune")
        return True, "unloaded {} (branch deleted)".format(branch)
    holder, is_primary = _worktree_holding(root, branch)
    if holder is None:
        return False, (
            "UNLOAD INCOMPLETE - branch {} survives the merge (git branch -d "
            "refused) and no registered worktree holds it; delete it by hand "
            "after reading:\n{}".format(branch, ac._failure_tail(out))
        )
    if is_primary:
        # `git worktree remove` refuses the primary FOREVER, so prescribing it
        # would send the operator after a command that can never work.
        return False, (
            "UNLOAD INCOMPLETE - branch {} is held by the MAIN checkout at {}, "
            "which is not a removable worktree. Switch that checkout off the "
            "branch (git -C {} checkout <trunk>), then run: git branch -d "
            "{}".format(branch, holder, holder, branch)
        )
    dirty = _worktree_dirt(holder)
    if dirty:
        # Shed the declared residue, then judge again on what is actually
        # there: a lane dirty ONLY with tool caches unloads clean, a lane
        # holding one real file still refuses below, naming it.
        _shed_declared_residue(holder)
        dirty = _worktree_dirt(holder)
    if dirty:
        return False, (
            "UNLOAD INCOMPLETE - branch {} is held by the worker worktree {}, "
            "which is DIRTY ({} uncommitted or ignored path(s)) - NOT removed "
            "and NOT forced, because a worktree can hold files that exist "
            "nowhere else (an ignored out/run-logs/ session stream counts). "
            "Salvage or commit them, then run: git worktree remove {} && "
            "git branch -d {}\n{}".format(
                branch,
                holder,
                len(dirty),
                holder,
                branch,
                "\n".join("  " + ln for ln in dirty[:10]),
            )
        )
    # Measured 2026-08-01 (the WI-397 close): `git worktree remove` run from
    # INSIDE the lane fails "Permission denied" AFTER half-unregistering the
    # worktree, leaving an empty directory - and on platforms where it
    # succeeds, the process is left standing in a deleted directory. The
    # removal must run from outside the lane, so step out first.
    try:
        cwd = Path.cwd().resolve()
    except OSError:
        cwd = None
    lane = holder.resolve()
    if cwd is not None and (cwd == lane or lane in cwd.parents):
        os.chdir(root)
    code, rm_out = ac.git(root, "worktree", "remove", str(holder))
    if code != 0:
        return False, (
            "UNLOAD INCOMPLETE - branch {} is held by the worker worktree {}, "
            "which reads clean but would not remove; run: git worktree remove {} "
            "&& git branch -d {}\n{}".format(
                branch, holder, holder, branch, ac._failure_tail(rm_out)
            )
        )
    ac.git(root, "worktree", "prune")
    code, out = ac.git(root, "branch", "-d", branch)
    if code != 0:
        return False, (
            "UNLOAD INCOMPLETE - the clean worker worktree {} was removed but "
            "branch {} still will not delete; run: git branch -d {}\n{}".format(
                holder, branch, branch, ac._failure_tail(out)
            )
        )
    return True, "unloaded {} (branch deleted; GC'd clean worker worktree {})".format(
        branch, holder
    )


def ignored_files(wt):
    """Every IGNORED FILE under `wt` as a set of repo-relative posix paths, or
    None when git could not answer.

    Deliberately NOT `_worktree_dirt`'s listing. `git status --ignored=matching`
    collapses an ignored directory to one `!! dir/` line whatever is inside it,
    at any `-u` setting - so a before/after diff of those lines cannot see a
    file added to a directory that already existed (REVIEW-A round 1: driven,
    and it is the NORMAL case, because the worker builds in the same lane
    worktree the refresh then bars). `ls-files -o -i` enumerates the files
    themselves. `-z` because a path with an odd character would otherwise come
    back quoted and have to be guessed at.

    The two readings coexist on purpose: §5.6's unload asks "is there anything
    here at all?" and the collapsed answer is right for that; this asks "which
    files exactly?", because it is about to delete some.

    The separator normalization is WINDOWS-ONLY (WI-407). git itself emits "/"
    on every platform, so the replace is pure defense - and on POSIX "\\" is an
    ordinary filename byte, not a separator, so replacing it MINTS an alias: a
    git-ignored file literally named `x\\__pycache__\\evil.pyc` came back as
    `x/__pycache__/evil.pyc`, `_is_declared_residue` matched the mangled
    segments, and the shed unlinked whatever REAL file sat at that path - the
    tracked twin the double-lock exists to protect (WI-400 REVIEW-A finding 1,
    driven). On POSIX the path passes through untouched.
    """
    code, out = ac.git(wt, "ls-files", "-o", "-i", "--exclude-standard", "-z")
    if code != 0:
        return None
    if os.name == "nt":
        return {p.replace("\\", "/") for p in out.split("\0") if p.strip()}
    return {p for p in out.split("\0") if p.strip()}


def existing_directories(wt):
    """Every directory under `wt` right now, as a set of paths.

    The other half of `_shed_residue`'s baseline. An empty ignored directory
    IS reported by `git status --ignored` (measured), so a directory the bar
    emptied has to be removed or §5.6's unload refuses over it - but a
    directory that was already there, empty, belongs to the lane and must
    survive. Only a snapshot can tell those apart: git lists no empty
    directory as "pre-existing" because git does not track directories at all.

    Cheap relative to what it guards - one tree walk beside an eleven-minute
    bar. `.git` is skipped because nothing under it is ever the bar's residue.
    """
    found = set()
    for parent, dirs, _files in os.walk(wt):
        if ".git" in dirs:
            dirs.remove(".git")
        for name in dirs:
            found.add(Path(parent) / name)
    return found


def _shed_residue(wt, baseline, baseline_dirs):
    """Delete the ignored FILES this refresh's own bar added to `wt`.

    The refresh's promise is that it leaves the lane worktree as it found it
    plus (at most) one commit. Without this the promise breaks in one specific
    way: the bar runs in the lane worktree now, and a declared bar leaves tool
    residue - `.pytest_cache/`, `__pycache__/`, a coverage report - which git
    ignores and which §5.6's unload reads, correctly, as DIRT.

    What this does NOT do, stated because the first version's comment implied
    otherwise: it does not make a lane worktree clean. A lane the worker
    already built in carries ITS residue, this function will not touch it, and
    §5.6 will still report the branch as held. That is WI-359's rule working as
    designed and it predates this WI; what changed is only that the refresh no
    longer ADDS to the pile.

    Narrow on purpose, because deleting files is the one thing §5.6 exists to
    be careful about: only IGNORED files (an untracked-but-trackable file is a
    surprise, and a surprise is evidence), only ones absent before the refresh
    started, and nothing at all if git could not enumerate them.
    """
    now = ignored_files(wt)
    if now is None or baseline is None:
        return
    emptied = set()
    for rel in sorted(now - baseline):
        target = wt / rel
        try:
            if target.is_file():
                target.unlink()
                emptied.add(target.parent)
        except OSError:
            # Left behind rather than fought over: the unload will report it as
            # dirt, which is a loud, recoverable outcome.
            continue
    # A directory the bar CREATED is residue too, once it is empty - otherwise
    # git reports the emptied directory and the unload refuses over it. Two
    # stops, and the second is the one REVIEW-A round 2 added: a directory that
    # still holds a pre-existing file is the lane's (rmdir simply fails), and a
    # directory that predates this refresh is the lane's even when it is EMPTY.
    # Emptiness can be load-bearing - this repo's own `docs/work/deferred/` is
    # an empty untracked directory that a link resolves through.
    for directory in sorted(emptied, key=lambda p: len(p.parts), reverse=True):
        while directory != wt and wt in directory.parents:
            if directory in baseline_dirs:
                break
            try:
                directory.rmdir()
            except OSError:
                break
            directory = directory.parent


def _refresh_preflight(root, branch):
    """Everything that must hold before the refresh sequence may start:
    `(lane worktree, work tip sha, None)`, or `(None, None, refusal)`.

    Ends by resetting the lane to its work tip, so the caller begins from a
    known state whatever the previous run left. Split out from `refresh` so the
    sequence itself reads as the four steps §A2.1 fixes the order of, with the
    preconditions - a declared bar, a trunk to merge in, a lane that is not
    holding uncommitted work - stated once, here.
    """
    refusal = _declared_bar_or_refusal(root)
    if refusal:
        return None, None, refusal
    holder, is_primary = _worktree_holding(root, branch)
    if is_primary:
        # Trunk is "whatever the main checkout has out", so a main checkout
        # sitting ON the branch makes trunk BE the branch: the refresh would
        # merge the branch into itself, report "refreshed onto trunk <its own
        # sha>" and attest a composition that never happened (REVIEW-A round 1,
        # driven). Refuse instead of resolving trunk some other way - there is
        # no trunk to resolve while nothing has it checked out.
        return (
            None,
            None,
            "the MAIN checkout at {} has {} checked out, so this repo has no "
            "trunk checked out to merge IN - refreshing there would merge the "
            "branch into itself. Switch it back (git -C {} checkout <trunk>) "
            "and re-run: a lane worktree is added automatically.".format(
                holder, branch, holder
            ),
        )
    wt, err = lane_worktree(root, branch)
    if err:
        return None, None, "cannot refresh {}: {}".format(branch, err)
    if ac.working_tree_dirty(wt):
        return (
            None,
            None,
            "the lane worktree {} is dirty - the refresh resets to the last "
            "work commit, so it refuses rather than discard uncommitted work; "
            "commit or stash it, then refresh".format(wt),
        )
    work_tip = _work_tip(root, branch)
    code, out = ac.git(wt, "reset", "--hard", work_tip)
    if code != 0:
        return (
            None,
            None,
            "cannot reset {} to its last work commit {}:\n{}".format(
                branch, work_tip[:10], ac._failure_tail(out)
            ),
        )
    return wt, work_tip, None


def _keep_refused_output(root, branch, detail):
    """Retain a refused refresh's FULL output; returns the sentence naming it.

    The refusal message carries only `_failure_tail`'s bounded window, and the
    undo resets the very tree that produced the evidence — so before WI-398 a
    red's full diagnosis survived NOWHERE (the WI-387 refresh red was diagnosed
    three times and lost three times, each refusal all that remained). One
    retained file per branch in the ROOT checkout's gitignored `out/run-logs/`
    home — outside the lane worktree, so neither the reset nor `_shed_residue`
    can sweep it, and overwritten by the branch's next refusal. Deliberately no
    rotation, indexing or pruning (WI-398's scope guard): the latest refusal is
    the one being fixed. Fail-soft — a log that cannot be written must not mask
    the refusal it documents — and empty output keeps nothing (a message naming
    an empty file would send the reader to a second dead end)."""
    if not (detail or "").strip():
        return ""
    name = re.sub(r"[^A-Za-z0-9._-]", "-", branch)
    path = Path(root) / "out" / "run-logs" / "refresh-refused-{}.log".format(name)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(detail, encoding="utf-8", errors="replace", newline="\n")
    except OSError:
        return ""
    return "\n(full output kept at {})".format(path)


def refresh(root, branch, tier):
    """The §A2 station refresh. Returns `(branch tip sha, None)` or `(None, refusal)`.

    Mechanical - no agent, no judgement. In the branch's own lane worktree:

        merge trunk IN  ->  trunk_step (compile, then regen)  ->  bar  ->  commit

    That order is fixed and load-bearing (§A2.1): the compile has to see the
    trunk's log before it appends, and the bar has to see what the compile and
    the regen wrote. The commit carries a `Bar-Green:` trailer NAMING the tree
    it barred and the work commit it sits on, and refuses to exist unless it
    verifies against git - see `refresh_attestation`.

    EVERY failure path leaves the branch back at its last work commit, clean.
    That is the disposable-commit rule doing double duty: it is what makes a
    retry safe (a second merge stacked on the first would conflict on
    docs/log.md's appended end), and it is why a failed refresh parks nothing
    for a human to unpick. Reproduce a red by running the refresh again - it is
    deterministic given the same trunk. The refusal carries the failing step's
    own output window and NAMES the retained full log (`_keep_refused_output`),
    because the undo erases the tree that produced the evidence (WI-398).

    Called from TWO places, deliberately the same code: the dispatcher runs it
    speculatively OUTSIDE the merge slot (via lane.py's refresh subprocess or
    dispatch.py's drain) (the ruled DECISION 4 - the 11-minute
    bar must not hold the exclusive turn to advance trunk), and `integrate_one`
    runs it INSIDE the slot for any branch that arrives un-refreshed or stale,
    which is the pessimistic sequence and is why that sequence never rots.
    """
    # The claimed rows' say over the bar (WI-388): the adjudication no-bar arm
    # and the `bar` strictness pin, both read before anything runs so a
    # malformed key refuses with the lane untouched.
    skip_bar, bar_gate, refusal = _lane_bar_directives(root, branch)
    if refusal:
        return None, "refresh REFUSED for {} - {}".format(branch, refusal)

    wt, work_tip, refusal = _refresh_preflight(root, branch)
    if refusal:
        return None, refusal

    # The ignored-FILE baseline, read BEFORE anything runs: see `_shed_residue`.
    baseline = ignored_files(wt)
    baseline_dirs = existing_directories(wt)

    def undo(reason, detail):
        _shed_residue(wt, baseline, baseline_dirs)
        ac.git(wt, "reset", "--hard", work_tip)
        return None, "refresh REFUSED for {} - {}:\n{}{}".format(
            branch,
            reason,
            ac._failure_tail(detail),
            _keep_refused_output(root, branch, detail),
        )

    trunk = _head(root)
    code, out = ac.git(wt, "merge", "--no-ff", "--no-commit", trunk)
    if code != 0:
        # The ONE place a conflict can still exist, and it is the right place:
        # the lane owns being current with trunk, and the lane worktree is
        # where the person (or agent) who wrote the code is working. The merge
        # slot never sees this - by the time a branch reaches it, trunk is an
        # ancestor and a conflict is unrepresentable.
        return undo(
            "merging trunk {} in CONFLICTS; resolve it on the branch in {} "
            "(git merge {}), commit, then refresh again".format(
                trunk[:10], wt, trunk[:10]
            ),
            out,
        )
    code, out = _run_trunk_step(wt, root)
    if code != 0:
        return undo("the trunk step failed on the refreshed tree", out)
    # STAGE, then bar, then commit the staged index. The bar is the last thing
    # to touch this tree, and a declared bar is the adopter's command: staging
    # first means whatever it writes (a coverage report, a cache) can never be
    # swept into the attested commit by an `add -A` that ran after it. The
    # committed tree is therefore exactly the tree the bar was handed.
    ac.git(wt, "add", "-A")
    ok, bar_out, summary = _refresh_bar(wt, root, tier, skip_bar, bar_gate)
    _shed_residue(wt, baseline, baseline_dirs)
    if not ok:
        return undo(
            "the bar is RED on the refreshed tree ({}) - fix it on the branch, "
            "then refresh again".format(summary),
            bar_out,
        )
    # The tree the bar was just handed, named BEFORE the commit that carries the
    # name. `write-tree` writes the index - the same index `commit` will use -
    # so the value is knowable in advance and is not a prediction. Anything that
    # changes the tree afterwards (an amend, a rebase, a hook that rewrites a
    # file) leaves the trailer describing a tree that is no longer there, and
    # the self-check below refuses rather than shipping a false attestation.
    code, tree = ac.git(wt, "write-tree")
    if code != 0 or not tree.strip():
        return undo("could not name the barred tree (git write-tree failed)", tree)
    code, out = ac.git(
        wt,
        "commit",
        "--allow-empty",
        "-m",
        "{}{}\n\nThe §A2 station refresh: trunk merged in, the §5.1 fragment compile and\n§5.2 regeneration folded on, and the declared bar run on THIS tree. The\ntrailer NAMES what it attests - the tree the bar saw and the work commit it\nsits on - so the merge slot verifies both against git instead of trusting a\nmessage. A --no-ff merge of a branch that contains trunk reproduces this\ntree byte for byte, which is why no second bar is owed at the slot.\n\n{} tree={} work={} {}".format(
            _refresh_subject(branch),
            trunk[:10],
            BAR_GREEN,
            tree.strip(),
            work_tip,
            summary,
        ),
    )
    if code != 0:
        return undo("the refresh commit was refused by its own floor", out)
    if refresh_attestation(root, branch) is None:
        # Fail CLOSED on our own output: an attestation this script cannot
        # verify is worth less than none at all, because the slot would refuse
        # it later with a far more confusing message.
        return undo(
            "the refresh commit does not verify as its own attestation - the "
            "committed tree or parent is not the one the bar saw (a rewriting "
            "commit hook?); nothing is attested and the branch is restored",
            out,
        )
    sha = _head(wt)
    print(
        "integrate: refreshed {} onto trunk {} - {} @ {}".format(
            branch, trunk[:10], summary, sha[:10]
        )
    )
    return sha, None


def _refresh_bar(wt, root, tier, skip_bar, bar_gate):
    """The refresh's bar step, with the WI-388 no-bar arm: `(ok, out, summary)`.

    `skip_bar` is the adjudication arm (§A5.2): the trunk step still ran and
    the refresh commit still attests THIS tree — the trailer verifies the same
    way — but no product bar is invoked, and the summary says so honestly,
    because the kind has nothing a product bar can speak to. Extracted from
    `refresh` so the sequence stays readable under the complexity ratchet.

    Implements: SR-174, LLR-154
    """
    if skip_bar:
        return True, "", "no-bar (adjudication, §A5.2)"
    return _run_bar(wt, root, tier, bar_gate)


def _merge_ready(root, branch):
    """`(ready, why)` - may `branch` enter the merge queue? (§A2)

    Two facts, both read off git: trunk is already an ancestor, and the tip
    carries the bar's attestation FOR THAT TIP. The second is not a second
    check bolted onto the first - it is what makes the first sufficient, since
    an ancestor relation alone says nothing about whether anyone barred the
    composition.
    """
    if not trunk_is_ancestor(root, branch):
        return False, "trunk {} is not an ancestor of it".format(_head(root)[:10])
    attested = refresh_attestation(root, branch)
    if attested is None:
        return False, (
            "its tip is not a verified refresh commit - no {} trailer naming "
            "this exact tree and parent".format(BAR_GREEN)
        )
    return True, attested[1]


def _partial_report_refusal(root, branch, outcomes):
    """SR-144: a `partial` close must carry a readable report that states the
    KEEP/DISCARD split. A refusal string, or None.

    This rung exists because of a live incident (2026-08-03): a lane handed
    work back, the branch merged green, and the code the lane had REJECTED
    landed on trunk as-is — because nothing had asked which of its commits
    should survive. The split turns that into the adjudicator's explicit call
    instead of a hand cleanup someone has to notice is owed.

    Read off the BRANCH's tree, like `branch_outcomes`, so the report and the
    move it describes are one fact read once.

    The report's path, its frontmatter parse and the refusal itself all come
    from `kitlib.station`, the read model this rung's vocabulary already lives
    in. Until WI-483 slice 2 they came from `handback` through a deferred
    `import handback` right here — a back edge of the runtime scripts' cycle,
    for a path built from two strings and a rule over a dict. The WRITES stay in
    `handback`, which is what this module is not allowed to reach into."""
    for wi_id in sorted(w for w, o in (outcomes or {}).items() if o == Outcome.PARTIAL):
        rel = report_path(branch, wi_id)
        code, text = ac.git(root, "show", "{}:{}".format(branch, rel))
        meta = read_toml_block(text) if code == 0 else None
        refusal = report_refusal(meta)
        if refusal:
            return "{} closed {} as `partial` but {} ({}); nothing was merged".format(
                branch, wi_id, refusal, rel
            )
    return None


def _merge_refusal(root, branch, wi_ids):
    """The merge slot's refusal ladder: `(outcomes, refusal)` - the first reason
    this branch may not merge, or the outcomes the merge needs and None.

    `_claim_refusal`'s shape at the other end of the lane's life, and extracted
    for the same reason that one was: the ladder grew a rung (RULING R1) and
    `integrate_one` went over the C901 baseline, which this repo's ratchet
    answers by extraction rather than by a bigger number. Order is
    cheapest-first, and every rung is read off the tree or off git - nothing
    here consults a state file.
    """
    if not wi_ids:
        return {}, "trunk holds no claimed specs for {}".format(branch)
    outcomes, unresolved = branch_outcomes(root, branch)
    if unresolved:
        return outcomes, (
            "{} left claimed spec(s) without exactly ONE declared state "
            "directory ({}) - the folder a spec lands in IS the lane's outcome "
            "(§A3), so one that landed nowhere names none of the three and one "
            "that landed twice names two; nothing was merged. The three are "
            "{}. If this lane stopped early, close it into partial/ with a "
            "per-close report (SR-144 retired the close-into-queued/ "
            "handback).".format(
                branch,
                ", ".join(unresolved),
                " | ".join(d + "/" for d in sorted(OUTCOME_DIRS)),
            )
        )
    # Sequential, not a tuple of calls: a tuple would EVALUATE every rung before
    # testing the first, which is exactly the cheapest-first ordering thrown away.
    refusal = _partial_report_refusal(root, branch, outcomes)  # SR-144
    if refusal:
        return outcomes, refusal
    refusal = _minted_id_refusal(root, branch, wi_ids)  # RULING R1
    if refusal:
        return outcomes, refusal
    refusal = _declared_bar_or_refusal(root)
    if refusal:
        return outcomes, refusal
    return outcomes, _verdict_gate(root, branch, outcomes)


def integrate_one(root, branch, tier, held=None):
    """One branch through the merge slot. Returns None on green, else the refusal.

    Runs with the slot HELD (see `integrate`), so everything here is either
    sub-second or the deliberate pessimistic fallback.

    `held` is an out-parameter list collecting the branch names whose §5.6
    unload did NOT complete. The merge itself stands (the trunk has already
    moved), so an incomplete unload is not a refusal - but nothing ever retries
    it (a merged branch no longer appears in `finished_branches`), which is why
    the caller has to carry the remainder to the run's exit code.

    THE POST-MERGE ARM IS THE INTAKE (WI-388, §A5.2): once the merge lands —
    and only then — the unified mint helper reads what landed (the approved/
    routed spine diff, a returned spec's `## Handback`, a merged adjudication
    row's `## Dispositions` drafts) and mints the rows the event forces, as
    ONE bookkeeping commit on trunk, inside this same held slot (serial by
    construction; rulings R1/R3: a WI id is created only by a human trunk
    commit or that helper). A mint refusal stops the run LOUDLY but the merge
    stands; recovery is a trunk-side fix plus `python intake.py sweep`.

    Implements: SR-156, SR-174, LLR-140, LLR-154
    """
    wi_ids = _claimed_wi_ids(root, branch)
    outcomes, refusal = _merge_refusal(root, branch, wi_ids)
    if refusal:
        return refusal

    ready, why = _merge_ready(root, branch)
    if not ready:
        # THE PESSIMISTIC SEQUENCE - slot already held, so this is exactly
        # "take slot -> merge trunk in -> bar -> merge". It is reached on every
        # drain that merges a SECOND branch (the first merge moved trunk out
        # from under it) and by any branch that never refreshed at all, so it
        # is production code that runs and passes, not a fallback that rots
        # waiting for the day someone restricts the design to pessimistic.
        print(
            "integrate: {} is not merge-ready ({}) - refreshing inside the "
            "slot, which is the pessimistic sequence.".format(branch, why)
        )
        _sha, refusal = refresh(root, branch, tier)
        if refusal:
            return refusal
        ready, why = _merge_ready(root, branch)
        if not ready:
            return (
                "{} is still not merge-ready after its in-slot refresh ({}) - "
                "the refresh reported green, so this is a real anomaly, not a "
                "lost race; nothing was merged".format(branch, why)
            )
    pre_merge_head = _head(root)
    code, out = ac.git(
        root,
        "merge",
        "--no-ff",
        "-m",
        "integrate: merge {} ({})\n\nThe §A2 merge: trunk was already an ancestor of this branch, so the\nmerge is trivially clean and its tree IS the branch tip's - the tree the\nbranch's own refresh bar passed ({}).\n\nOutcomes (§A3): {}".format(
            branch,
            ", ".join(wi_ids),
            why,
            ", ".join("{}={}".format(w, outcomes[w]) for w in wi_ids),
        ),
        branch,
    )
    if code != 0:
        # Unreachable by construction: `_merge_ready` just proved trunk is an
        # ancestor, and such a merge cannot conflict. So this is not a conflict
        # arm - it is the loud stop for a git failure nobody has a model for,
        # and it deliberately repairs nothing.
        return (
            "the --no-ff merge of {} FAILED although trunk is an ancestor of "
            "it - that should be impossible, so this run repairs nothing and "
            "stops for a human to read:\n{}".format(branch, ac._failure_tail(out))
        )
    unloaded, note = _unload_branch(root, branch)
    print(
        "integrate: {} merged ({}); {}".format(
            branch,
            ", ".join("{}={}".format(w, outcomes[w]) for w in wi_ids),
            why,
        )
    )
    # An incomplete unload goes to stderr rather than being swallowed - the §5.6
    # drained-and-unloaded stop is not reached while a branch or worktree lingers.
    print("integrate: {}".format(note), file=sys.stdout if unloaded else sys.stderr)
    if not unloaded and held is not None:
        held.append(branch)
    # The WI-388 intake, at the one honest hook point: the merge has landed,
    # the slot is still held, trunk is serial. A DOWNWARD call — this said
    # ABOVE until WI-483 slice 7, true only while the cycle made it so; the
    # order lives once, in `tests/test_import_layers.py` LIFECYCLE_RANK, which
    # reads function bodies, so deferring to skip the mint family hides nothing.
    import intake

    _minted, mint_refusal = intake.intake_after_merge(
        root, pre_merge_head, _head(root), outcomes, branch
    )
    if mint_refusal:
        return mint_refusal
    return None


def _slot(root):
    """TAKE THE SLOT - the exclusive turn to advance trunk. Error string or None.

    THE ONE ACQUISITION SITE IN THIS FILE, and it must stay that way (§A2.0
    requirement 1). The design is speculative: the 11-minute bar runs OUTSIDE
    this lock, and only the ancestor check plus the merge run inside it, so the
    slot is held for well under a second and extra lanes buy throughput instead
    of queueing behind one bar. Restricting the design to pessimistic - the
    owner's recorded caveat - is then a ONE-LINE change: delete dispatch.py's
    speculative refresh call, and every refresh happens under
    this already-held lock via `integrate_one`'s not-merge-ready arm. Nothing
    else moves, and no dial is added for a decision nobody has yet needed to
    change.
    """
    return ac.acquire_lock(root / "out" / "integrate.lock")


def integrate(root, tier, branches=None):
    # `branches` (WI-381): an optional restriction to a subset of the finished
    # claimed branches — the dispatcher merges each lane's branch as its OWN
    # refresh completes, and must not pull a branch whose lane is still
    # mid-refresh into the slot. None keeps the whole-queue drain unchanged.
    # Dirty check BEFORE the lock: the lock file itself is untracked (and
    # gitignored - out/integrate.lock in the shipped template), so taking it
    # first would make the queue refuse itself on any repo whose ignore rules
    # predate it.
    if ac.working_tree_dirty(root):
        return fail("the trunk working tree is dirty - the queue needs a clean trunk")
    lock_err = _slot(root)
    if isinstance(lock_err, str) and lock_err:
        return fail(lock_err)
    try:
        base = _head(root)
        finished = finished_branches(root)
        if branches is not None:
            wanted = set(branches)
            finished = [b for b in finished if b in wanted]
        if not finished:
            print("integrate: no finished claimed branches - nothing to merge.")
            return 0
        held = []
        for branch in finished:
            refusal = integrate_one(root, branch, tier, held)
            if refusal:
                # A red queue STOPS (§5.5) - it never skips to the next branch,
                # because later merges would compose against a tree the red one
                # was supposed to reach first.
                return fail(refusal)
        code = audit(root, base)
        if code != 0:
            return fail("the RULING-6 window audit flagged this run's own history")
        if held:
            return _held_summary(root, held)
        return 0
    finally:
        ac.release_lock()


def _held_summary(root, held):
    """The run's unpaid remainder: every still-held branch by name and path, and
    a NONZERO exit. Always returns 1.

    §5.6's stop is drained AND unloaded, so a run that merged everything but
    left a branch behind must not report 0 - nothing retries the unload (a
    merged branch is no longer a finished claimed branch), so this exit code is
    the only surviving signal. The merges STAND; the code reports the
    remainder, it does not undo work.
    """
    for branch in held:
        holder, is_primary = _worktree_holding(root, branch)
        where = (
            "no worktree - the branch alone"
            if holder is None
            else "{}{}".format(holder, " (MAIN checkout)" if is_primary else "")
        )
        print("integrate: STILL HELD - {} at {}".format(branch, where), file=sys.stderr)
    print(
        "integrate: INCOMPLETE - {} merged branch(es) NOT unloaded ({}); the "
        "queue drained but the §5.6 stop is not reached. The merges STAND - "
        "this exit code reports the remainder, it does not undo work.".format(
            len(held), ", ".join(held)
        ),
        file=sys.stderr,
    )
    return 1


def _generated_paths(root):
    """The stack.ini [generated] keys - the §5.2 declared trunk-only set."""
    import configparser

    ini = root / "docs" / "stack.ini"
    if not ini.exists():
        return []
    cp = configparser.ConfigParser(interpolation=None)
    # Keys are PATHS: configparser's default optionxform lowercases, which
    # would make PROJECT_STATE.html unmatchable and red the audit on the very
    # bookkeeping it exists to permit.
    cp.optionxform = str
    try:
        cp.read_string(ini.read_text(encoding="utf-8-sig", errors="replace"))
    except configparser.Error:
        return []
    if not cp.has_section("generated"):
        return []
    return [k.strip() for k in cp.options("generated")]


def audit(root, since):
    """RULING-6 over a window: non-merge trunk commits must stay on bookkeeping
    surfaces. Scoped to --since because the always-on form would flag attended
    serial work (RULING-8); widening it is an owner ruling.

    Implements: SR-156, LLR-140
    """
    allowed = list(BOOKKEEPING_PREFIXES) + _generated_paths(root)
    code, out = ac.git(
        root,
        "log",
        "--first-parent",
        "--no-merges",
        "--format=::%H",
        "--name-only",
        "{}..HEAD".format(since),
    )
    if code != 0:
        print(
            "integrate: audit skipped - git log failed: {}".format(out), file=sys.stderr
        )
        return 1
    bad = {}
    sha = None
    for ln in out.splitlines():
        if ln.startswith("::"):
            sha = ln[2:12]
            continue
        path = ln.strip().replace("\\", "/")
        if not path or sha is None:
            continue
        if not any(path == a.rstrip("/") or path.startswith(a) for a in allowed):
            bad.setdefault(sha, []).append(path)
    for sha, paths in bad.items():
        print(
            "integrate: AUDIT - non-merge trunk commit {} touches product paths: {}".format(
                sha, ", ".join(sorted(paths)[:5])
            ),
            file=sys.stderr,
        )
    if not bad:
        print(
            "integrate: audit clean ({}..HEAD - product changes arrived by merge only).".format(
                since[:10]
            )
        )
    return 1 if bad else 0


def main(argv=None):
    ac._utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    sub = ap.add_subparsers(dest="op", required=True)
    p_claim = sub.add_parser("claim", help="the §2.3 trunk claim + branch cut")
    p_claim.add_argument("--wi", required=True)
    p_claim.add_argument("--branch", required=True)
    p_ref = sub.add_parser(
        "refresh", help="the §A2 station refresh (merge trunk in, regen, bar, commit)"
    )
    p_ref.add_argument("--branch", required=True)
    p_ref.add_argument(
        "--tier",
        default="all",
        help="declared bar tier for the refresh bar (default: all - the full gate bar)",
    )
    p_int = sub.add_parser("integrate", help="the merge slot")
    p_int.add_argument(
        "--tier",
        default="all",
        help="declared bar tier for an in-slot refresh (default: all - the full gate bar)",
    )
    p_audit = sub.add_parser("audit", help="RULING-6 window check")
    p_audit.add_argument("--since", required=True, help="the window's base revision")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if args.op == "claim":
        wi_ids = [normalize_wi_id(w) for w in args.wi.split(";") if w.strip()]
        return claim(root, wi_ids, args.branch)
    if args.op == "refresh":
        _sha, refusal = refresh(root, args.branch, args.tier)
        return fail(refusal) if refusal else 0
    if args.op == "integrate":
        return integrate(root, args.tier)
    return audit(root, args.since)


if __name__ == "__main__":
    sys.exit(main())
