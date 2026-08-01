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

Four operations:

  claim      the §2.3 claim protocol, step 1+2: move a queued spec to
             docs/work/active/<branch>/ in a trunk bookkeeping commit, then
             cut the work branch from that commit. Refuses while the tracked
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
             claimed branch, requires the policy verdicts (RULING-7), checks
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

SCRIPTS = Path(__file__).resolve().parent
WORK = "docs/work"
ACTIVE = WORK + "/active"

# One LANE worktree home per repo, sibling to the checkout; one subdirectory per
# claimed branch. The worker builds there and the station refresh runs there —
# the same tree, on purpose: a red refresh has to be fixable where the lane
# already lives. §5.6's unload GCs a clean one after its merge.
LANE_WORKTREE_SUFFIX = "-drive"

# The bar's attestation, carried as a git trailer in the refresh commit, NAMING
# the tree and the work commit it attests so both can be checked against git.
# See `refresh_attestation` for why the names are the whole point: a message
# alone rides through amend, rebase and cherry-pick onto trees nobody barred.
BAR_GREEN = "Bar-Green:"
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
BOOKKEEPING_PREFIXES = (WORK + "/", "docs/log.d/", "docs/log.md")


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


def _claim_refusal(root, wi_id, branch):
    """The claim's refusal ladder: the first reason this claim may not happen,
    or None. Every reason is named; order is cheapest-first."""
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
    if code == 0:
        return "branch {} already exists".format(branch)
    if ".." in branch or "/" in branch or "\\" in branch:
        return (
            "branch name {!r} does not map to a flat claim directory - the queue "
            "handles single-segment branch names".format(branch)
        )
    try:
        meta = _spec_frontmatter(_queued_spec(root, wi_id))
    except ValueError as exc:
        return str(exc)
    safety = meta.get("safety_class", "unclassified")
    if safety != "ordinary":
        return (
            "{} is safety_class={!r} - the integrator claims ordinary work only; "
            "spine/gate classes run attended as the §3.2 barrier".format(wi_id, safety)
        )
    refusal = _specref_refusal(root, meta, wi_id)  # WI-370
    if refusal:
        return refusal
    refusal = _status_prose_refusal(root, wi_id)  # WI-358
    if refusal:
        return refusal
    import schedule  # sibling; deferred so the cheap refusals above stay cheap

    ready = {r["id"] for r in schedule.frontier(schedule._load(root))}
    if wi_id not in ready:
        return "{} is not on the ready frontier (unmet needs or not queued)".format(
            wi_id
        )
    return None


def claim(root, wi_id, branch):
    """§2.3 steps 1+2: the serial trunk claim, then the branch cut."""
    refusal = _claim_refusal(root, wi_id, branch)
    if refusal:
        return fail(refusal)
    spec = _queued_spec(root, wi_id)
    dest_dir = root / ACTIVE / branch
    dest_dir.mkdir(parents=True, exist_ok=True)
    code, out = ac.git(
        root,
        "mv",
        str(spec.relative_to(root)),
        str((dest_dir / spec.name).relative_to(root)),
    )
    if code != 0:
        return fail("git mv failed: {}".format(out))
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
    code, out = ac.git(
        root,
        "commit",
        "-m",
        "claim: {} -> active/{} (bookkeeping)\n\nThe §2.3 serial trunk claim with its regeneration folded in; the work\nbranch is cut from this commit.".format(
            wi_id, branch
        ),
    )
    if code != 0:
        return fail(
            "claim commit failed (the floor is the gate working):\n{}".format(out)
        )
    code, out = ac.git(root, "branch", branch, "HEAD")
    if code != 0:
        return fail("branch cut failed: {}".format(out))
    print(
        "integrate: claimed {} on {} (trunk commit + branch cut)".format(wi_id, branch)
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


def _claimed_wi_ids(root, branch):
    """The WI ids the TRUNK holds claimed for this branch."""
    ids = []
    for spec in sorted((root / ACTIVE / branch).glob("WI-*.md")):
        ids.append(spec.name.split("-", 2)[0] + "-" + spec.name.split("-", 2)[1])
    return ids


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


def _verdict_gate(root, branch, wi_ids):
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
    """
    dial = ac.read_declared(root / "docs" / "review-policy", "0")
    try:
        required = int(dial or "0") >= 1
    except ValueError:
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
    for wi in wi_ids:
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
    trunk-vintage whenever drive.py drives the loop in-process, so this cannot
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


def _run_bar(wt, root, tier):
    """check.py at the derived gate on the refreshed branch; fail-closed reading.

    Green means: exit 0 AND the report carries no SKIP line. `--trunk-lane` is
    passed because the tree being barred IS the tree that becomes trunk (the
    --no-ff merge of a branch containing trunk reproduces it byte for byte), so
    the §5.2 freshness gates - which stand down on a work branch, and which
    this very step just regenerated - have to run here or nothing checks them.
    """
    py = ac.harness_python(root)
    check = _branch_tree_script(wt, root, "check.py")
    code, out = _run(
        [str(py), str(check), "--jobs", "0", "--tier", tier, "--trunk-lane"], wt
    )
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
        "bar PASS ({} steps, tier {})".format(len(_passed_steps(out)), tier),
    )


def _run_trunk_step(wt, root):
    py = ac.harness_python(root)
    step = _branch_tree_script(wt, root, "trunk_step.py")
    return _run([str(py), str(step), "--root", "."], wt)


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


def _unload_branch(root, branch):
    """§5.6 unload of a merged work branch: (fully_unloaded, message).

    `git branch -d` refuses a branch checked out in a linked worktree, and
    swallowing that refusal is how the old dispatcher accumulated 36 stale
    worktrees - so every outcome is reported by branch AND by holding path.

    The GC is owned only where it is safe: a CLEAN linked worktree is removed
    and the delete retried; a DIRTY one is reported and LEFT, never forced, and
    the MAIN checkout is never removed at all. A worktree can hold orphaned
    files that exist nowhere else (2026-07-26), so dirt is evidence, not
    garbage.
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
    """
    code, out = ac.git(wt, "ls-files", "-o", "-i", "--exclude-standard", "-z")
    if code != 0:
        return None
    return {p.replace("\\", "/") for p in out.split("\0") if p.strip()}


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
    deterministic given the same trunk.

    Called from TWO places, deliberately the same code: drive.py runs it
    speculatively OUTSIDE the merge slot (the ruled DECISION 4 - the 11-minute
    bar must not hold the exclusive turn to advance trunk), and `integrate_one`
    runs it INSIDE the slot for any branch that arrives un-refreshed or stale,
    which is the pessimistic sequence and is why that sequence never rots.
    """
    wt, work_tip, refusal = _refresh_preflight(root, branch)
    if refusal:
        return None, refusal

    # The ignored-FILE baseline, read BEFORE anything runs: see `_shed_residue`.
    baseline = ignored_files(wt)
    baseline_dirs = existing_directories(wt)

    def undo(reason, detail):
        _shed_residue(wt, baseline, baseline_dirs)
        ac.git(wt, "reset", "--hard", work_tip)
        return None, "refresh REFUSED for {} - {}:\n{}".format(
            branch, reason, ac._failure_tail(detail)
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
    ok, bar_out, summary = _run_bar(wt, root, tier)
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


def integrate_one(root, branch, tier, held=None):
    """One branch through the merge slot. Returns None on green, else the refusal.

    Runs with the slot HELD (see `integrate`), so everything here is either
    sub-second or the deliberate pessimistic fallback.

    `held` is an out-parameter list collecting the branch names whose §5.6
    unload did NOT complete. The merge itself stands (the trunk has already
    moved), so an incomplete unload is not a refusal - but nothing ever retries
    it (a merged branch no longer appears in `finished_branches`), which is why
    the caller has to carry the remainder to the run's exit code.
    """
    wi_ids = _claimed_wi_ids(root, branch)
    if not wi_ids:
        return "trunk holds no claimed specs for {}".format(branch)
    refusal = _declared_bar_or_refusal(root)
    if refusal:
        return refusal
    refusal = _verdict_gate(root, branch, wi_ids)
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
    code, out = ac.git(
        root,
        "merge",
        "--no-ff",
        "-m",
        "integrate: merge {} ({})\n\nThe §A2 merge: trunk was already an ancestor of this branch, so the\nmerge is trivially clean and its tree IS the branch tip's - the tree the\nbranch's own refresh bar passed ({}).".format(
            branch, ", ".join(wi_ids), why
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
    print("integrate: {} merged ({}); {}".format(branch, ", ".join(wi_ids), why))
    # An incomplete unload goes to stderr rather than being swallowed - the §5.6
    # drained-and-unloaded stop is not reached while a branch or worktree lingers.
    print("integrate: {}".format(note), file=sys.stdout if unloaded else sys.stderr)
    if not unloaded and held is not None:
        held.append(branch)
    return None


def _slot(root):
    """TAKE THE SLOT - the exclusive turn to advance trunk. Error string or None.

    THE ONE ACQUISITION SITE IN THIS FILE, and it must stay that way (§A2.0
    requirement 1). The design is speculative: the 11-minute bar runs OUTSIDE
    this lock, and only the ancestor check plus the merge run inside it, so the
    slot is held for well under a second and extra lanes buy throughput instead
    of queueing behind one bar. Restricting the design to pessimistic - the
    owner's recorded caveat - is then a ONE-LINE change: delete drive.py's
    speculative `integrate.refresh(...)` call, and every refresh happens under
    this already-held lock via `integrate_one`'s not-merge-ready arm. Nothing
    else moves, and no dial is added for a decision nobody has yet needed to
    change.
    """
    return ac.acquire_lock(root / "out" / "integrate.lock")


def integrate(root, tier):
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
        branches = finished_branches(root)
        if not branches:
            print("integrate: no finished claimed branches - nothing to merge.")
            return 0
        held = []
        for branch in branches:
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
    serial work (RULING-8); widening it is an owner ruling."""
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
        return claim(root, normalize_wi_id(args.wi), args.branch)
    if args.op == "refresh":
        _sha, refusal = refresh(root, args.branch, args.tier)
        return fail(refusal) if refusal else 0
    if args.op == "integrate":
        return integrate(root, args.tier)
    return audit(root, args.since)


if __name__ == "__main__":
    sys.exit(main())
