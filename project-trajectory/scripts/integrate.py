"""integrate.py — the local integrator: a serial, fail-closed merge queue.

The default backend of the one integration flow (concurrency-restructure
§1.2): branch -> change request -> required checks on the composed tree ->
merge. Three operations:

  claim      the §2.3 claim protocol, step 1+2: move a queued spec to
             docs/work/active/<branch>/ in a trunk bookkeeping commit, then
             cut the work branch from that commit. Refuses while the tracked
             docs/work/pause is present (§5.6: pause = stop claiming), and
             while hand-authored docs/status.md prose names the claimed id
             (WI-358: that R-D debt is paid before the branch exists, since a
             branch cannot scrub trunk-owned status.md at merge time).
  integrate  the serial queue: for each FINISHED claimed branch (its tip
             moved every claimed spec out of active/<branch>/), merge
             --no-ff onto a candidate worktree, fold the §5.1/§5.2 trunk
             step into the merge commit (the commit must pass its own
             pre-commit floor — the dispatcher's proven shape), run the
             DECLARED bar on the composed tree, require the policy verdicts
             (RULING-7), fast-forward the trunk on green, and refuse LOUDLY
             on red (§4) — broken work is never force-merged to satisfy a
             drain, and a red queue stops rather than skips (§5.5). The
             merged branch is then UNLOADED: a clean worker worktree holding
             it is GC'd, while a dirty one (ignored files included) and the
             MAIN checkout are reported by path and left alone. §5.6's stop
             is drained AND unloaded, so a run that merged everything but
             left a branch held names it on stderr and exits NONZERO - the
             merges stand, the code reports the unpaid remainder.
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
Phase 4 inventory). Verdict freshness is git-derived: under the WI-scoped
naming (§5.4) the verdict's last commit on the branch must be no older than
the branch's last non-review, non-fragment commit, or a stale APPROVE from
an earlier iteration would silently clear the gate.

Serial on purpose: one candidate, one merge at a time, the coordinator lock
held throughout — composed-tree gating falls out by construction (§1.2).
Never pushes; the trunk only ever fast-forwards to a candidate the bar
passed.
"""

from __future__ import annotations

import argparse
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
CANDIDATE_BRANCH = "integrate/candidate"

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

    The closing commit's move to archive/ IS the finished signal (§2.3 step 3)
    - no state file, no ref, just the tree.
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


def _verdict_gate(root, branch, wi_ids):
    """RULING-7: the dialed verdict artifacts, fresh at the branch tip.

    review-policy >= 1 demands docs/reviews/WI-<n>-REVIEW-A.md per closed WI,
    carrying an APPROVE machine line, whose last commit on the branch is no
    older than the last non-review, non-fragment commit - the git-derived
    replacement for the old sha7-in-filename binding (§5.4 left it open).
    """
    dial = ac.read_declared(root / "docs" / "review-policy", "0")
    try:
        required = int(dial or "0") >= 1
    except ValueError:
        return "docs/review-policy is not an integer: {!r} (fail closed)".format(dial)
    if not required:
        return None
    code_time = _last_commit_time(
        root, branch, ".", ":(exclude)docs/reviews", ":(exclude)docs/log.d"
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


def _candidate_worktree(root):
    """The candidate worktree, created or REUSED. A refusal deliberately parks
    the worktree for inspection, so the next run must reuse the registration
    (git refuses to re-add a live worktree path) — a parked half-merge is
    aborted and the tree hard-reset to the current trunk either way."""
    wt = root.parent / (root.name + "-integrate") / "candidate"
    code, out = (
        ac.git(wt, "rev-parse", "--abbrev-ref", "HEAD") if wt.is_dir() else (1, "")
    )
    if code == 0 and out.strip() == CANDIDATE_BRANCH:
        ac.git(wt, "merge", "--abort")  # best-effort: clear a parked half-merge
    else:
        if wt.is_dir():
            raise RuntimeError(
                "{} exists but is not the candidate worktree - refusing to "
                "clobber it".format(wt)
            )
        ac.git(root, "worktree", "prune")
        code, _ = ac.git(
            root, "rev-parse", "--verify", "--quiet", "refs/heads/" + CANDIDATE_BRANCH
        )
        if code == 0:
            cmd = ["worktree", "add", "--force", str(wt), CANDIDATE_BRANCH]
        else:
            cmd = ["worktree", "add", "-b", CANDIDATE_BRANCH, str(wt), "HEAD"]
        code, out = ac.git(root, *cmd)
        if code != 0:
            raise RuntimeError("candidate worktree add failed: {}".format(out))
    trunk_sha = _head(root)
    code, out = ac.git(wt, "reset", "--hard", trunk_sha)
    if code != 0:
        raise RuntimeError("candidate reset failed: {}".format(out))
    return wt


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


def _run_bar(wt, root, tier):
    """check.py at the derived gate on the composed tree; fail-closed reading.

    Green means: exit 0 AND the report carries no SKIP line. The candidate is
    not a claimed work branch, so the §5.2 freshness steps all run - which is
    the point: the composed tree is checked at the full trunk bar.
    """
    py = ac.harness_python(root)
    code, out = _run(
        [str(py), str(SCRIPTS / "check.py"), "--jobs", "0", "--tier", tier], wt
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
    passes = len([ln for ln in out.splitlines() if re.match(r"\s*PASS\s", ln)])
    return True, out, "bar PASS ({} steps, tier {})".format(passes, tier)


def _run_trunk_step(wt, root):
    py = ac.harness_python(root)
    return _run([str(py), str(SCRIPTS / "trunk_step.py"), "--root", "."], wt)


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


def integrate_one(root, branch, tier, held=None):
    """One branch through the queue. Returns None on green, else the refusal.

    `held` is an out-parameter list collecting the branch names whose §5.6
    unload did NOT complete. The merge itself stands (the trunk has already
    fast-forwarded), so an incomplete unload is not a refusal - but nothing ever
    retries it (a merged branch no longer appears in `finished_branches`), which
    is why the caller has to carry the remainder to the run's exit code.
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

    wt = _candidate_worktree(root)
    code, out = ac.git(wt, "merge", "--no-ff", "--no-commit", branch)
    if code != 0:
        ac.git(wt, "merge", "--abort")
        return "merge conflict against the composed tree (a rebase is the worker's):\n{}".format(
            ac._failure_tail(out)
        )
    # Fold the §5.1/§5.2 trunk step INTO the merge commit so the commit passes
    # its own pre-commit floor (the WI-283 lesson; freshness gates all run on
    # the candidate because it is not a claimed work branch).
    code, out = _run_trunk_step(wt, root)
    if code != 0:
        ac.git(wt, "merge", "--abort")
        return "trunk step failed on the composed tree:\n{}".format(
            ac._failure_tail(out)
        )
    ac.git(wt, "add", "-A")
    code, out = ac.git(
        wt,
        "commit",
        "-m",
        "integrate: merge {} ({})\n\nComposed-tree merge (--no-ff) with the §5.1 fragment compile and §5.2\nregeneration folded in; the declared bar runs on this tree before the\ntrunk fast-forwards.".format(
            branch, ", ".join(wi_ids)
        ),
    )
    if code != 0:
        ac.git(wt, "merge", "--abort")
        return "merge commit refused by its own floor:\n{}".format(
            ac._failure_tail(out)
        )

    ok, bar_out, summary = _run_bar(wt, root, tier)
    if not ok:
        ac.git(root, "branch", "-f", CANDIDATE_BRANCH + "-red", CANDIDATE_BRANCH)
        return "the composed-tree bar is RED for {} - parked on {} for inspection:\n{}\n{}".format(
            branch, CANDIDATE_BRANCH + "-red", summary, ac._failure_tail(bar_out)
        )

    candidate_sha = _head(wt)
    code, out = ac.git(root, "merge", "--ff-only", candidate_sha)
    if code != 0:
        return "trunk fast-forward refused (trunk moved under the queue?):\n{}".format(
            out
        )
    unloaded, note = _unload_branch(root, branch)
    print("integrate: {} merged ({}); {}".format(branch, ", ".join(wi_ids), summary))
    # An incomplete unload goes to stderr rather than being swallowed - the §5.6
    # drained-and-unloaded stop is not reached while a branch or worktree lingers.
    print("integrate: {}".format(note), file=sys.stdout if unloaded else sys.stderr)
    if not unloaded and held is not None:
        held.append(branch)
    return None


def integrate(root, tier):
    # Dirty check BEFORE the lock: the lock file itself is untracked (and
    # gitignored - out/integrate.lock in the shipped template), so taking it
    # first would make the queue refuse itself on any repo whose ignore rules
    # predate it.
    if ac.working_tree_dirty(root):
        return fail("the trunk working tree is dirty - the queue needs a clean trunk")
    lock_err = ac.acquire_lock(root / "out" / "integrate.lock")
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
        _teardown(root)
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


def _teardown(root):
    wt = root.parent / (root.name + "-integrate") / "candidate"
    if wt.is_dir():
        ac.git(root, "worktree", "remove", "--force", str(wt))
    ac.git(root, "worktree", "prune")
    ac.git(root, "branch", "-D", CANDIDATE_BRANCH)


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
    p_int = sub.add_parser("integrate", help="the serial merge queue")
    p_int.add_argument(
        "--tier",
        default="all",
        help="declared bar tier for the composed-tree check (default: all - the full gate bar)",
    )
    p_audit = sub.add_parser("audit", help="RULING-6 window check")
    p_audit.add_argument("--since", required=True, help="the window's base revision")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if args.op == "claim":
        return claim(root, normalize_wi_id(args.wi), args.branch)
    if args.op == "integrate":
        return integrate(root, args.tier)
    return audit(root, args.since)


if __name__ == "__main__":
    sys.exit(main())
