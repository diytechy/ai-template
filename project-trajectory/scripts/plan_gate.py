#!/usr/bin/env python3
"""plan_gate.py - a `single` row builds only after its plan passes (WI-913).

WHY THIS EXISTS (review-churn plan item 9 step 3; WI-788's design, chapter 3
§4.1, §4.5 and §4.7). A row the scope critique marks `planmode = "single"`
plans in its lane after the claim: a plan, the coverage gate, one independent
cross-family critique, at most one revision, and at the cap a dispute sitting
or the owner. A build starts only after a passing verdict. Advice that is not
held at the commit is advice a hand landing or a `--no-verify` commit skips,
so the hold is a commit rule, asked where every lane commit is made and again
where it lands (the owner's 2026-10-03 rule: enforce at the commit):

  * the pre-commit hook's `plan-gate` step (`staged_lines`), of the commit
    being made in a lane, and, on trunk, of each lane commit a `git merge
    --squash` landing carries (a squashed tip no local branch contains holds
    by name while any claim copy the gate reads is `single` or outside the
    set: the branch is its only key to the claim copies);
  * the merge slot (`landing_refusal`), of each lane commit, riding the one
    lane-commit walk (`text_then_act.lane_commit_walk`) with its own judge.

THE ONE PREDICATE, `commit_lines`, judges one lane commit against its
parents, for each row the lane itself claimed whose claim copy declares
`single` (`kitlib.plan_pass.gate_rows`; another lane's claim copy its tree
carries is never read):

  * a commit that changes, as its own, a path outside the record homes is
    refused unless a parent holds a pass record binding the row's plan and
    Done-when as the commit leaves them. The homes are the lane's plan
    homes (`docs/plans/<WI>/`), `docs/reviews/`, `docs/decisions/`, the
    session logs under `docs/iteration/`, the log fragments under
    `docs/log.d/`, the row's own spec under `docs/work/active/<branch>/`, a
    close of the row (the spec's move out of `active/`, its report under
    `docs/handbacks/`, and the move's own inbound-link edits,
    `spec_move.exact_relink`, byte-exact), and, as a merge's own changes,
    what the station refresh writes: the compiled `docs/log.md` and the
    views `trunk_step.regen_writes` lists;
  * a commit that adds or changes a pass record is checked against its
    parent (`record_problems`, the rule the filing step applies too).

A merge is judged by what NEITHER parent carried, as text then act judges
one, and every binding is by content digest, so a rebase keeps it. Trunk, a
lane with no `single` row, and a commit before the first are never held.

WHAT A REBASE CANNOT CHANGE is all the landing re-checks (`deep=False`): the
record's grammar and digests, and the records it cites in the parent. The
critique's own tree (the commit it reviewed, by sha) is compared only at the
hook and the filing step, before any rebase can orphan that commit.

Contracts: IF-295 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-295: the plan gate's step, as a command.
    `plan_gate.py [--root <dir>]` judges the commit being made in the
    checkout at `<dir>` (default: the working directory) and, on a squash
    landing, each lane commit it carries. It prints one step line, `FAIL`
    with each hold (the row held, and the remedy) or `ok`, and exits 1 when
    any commit is held, else 0. It reads git and the lane's records and
    writes nothing. `check.py` runs it as the built-in `plan-gate` step.
    It judges a commit made on a branch named for a claim folder and, on a
    squash landing, each carried lane commit that such a branch contains. It
    does not judge a build commit made on a detached HEAD in a lane worktree,
    a lane merged into trunk by hand (a merge finished by commit, or one git
    commits itself, for which git runs no pre-commit hook), a squash whose
    commits only an alias branch contains, a squash after `git stash` has
    removed the squash message, or a landing made by copying files. No
    landing recipe makes any of these; under process.md §6, "Review threat
    model", they are residue.

Stdlib only, Python 3.11+, Windows/POSIX.

Usage:
    python scripts/plan_gate.py [--root DIR]

exits 0 when the staged commit is not held, 1 naming each hold (the
pre-commit hook's `plan-gate` step).
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_common  # noqa: E402  (path set above; the script-sibling idiom)
import score_reviews  # noqa: E402
import spec_move  # noqa: E402
import text_then_act  # noqa: E402
import trunk_step  # noqa: E402
from kitlib import dispute as _dispute  # noqa: E402
from kitlib import done_when as _kdone  # noqa: E402
from kitlib import git as _kitgit  # noqa: E402
from kitlib import plan_pass  # noqa: E402
from kitlib import sitting as _sitting  # noqa: E402
from kitlib import station as _station  # noqa: E402
from kitlib import verdict as _kverdict  # noqa: E402
from kitlib.config import utf8_console  # noqa: E402

_HOME_PREFIXES = (
    "docs/reviews/",
    "docs/decisions/",
    "docs/iteration/",
    trunk_step.LOG_D + "/",
)
# The log the station refresh compiles the fragments into (`trunk_step
# compile_log`, one directory above them).
_COMPILED_LOG = "docs/log.md"
_BLOCKING = ("BLOCKER", "MAJOR")
REMEDY = (
    "plan first: commit the plan, file its critique, then write the pass "
    "record (`review_brief.py plan-file --pass`) in its own commit, and build "
    "only on top of it"
)


def _own_changes(root, rev, parents):
    """`({path: status}, None)`: every path the commit `rev` (None: the
    index) changes as its OWN, one differing from EVERY parent, with its
    status against the first parent (`A`, `M`, `D`); `(None, why)` when a
    diff cannot be read, which holds rather than skips.

    Implements: SR-154, LLR-337
    """
    own = None
    for i, parent in enumerate(parents):
        args = ["diff", "--name-status", "--no-renames", "-z"]
        args += ["--cached", parent] if rev is None else [parent, rev]
        out = _kitgit.git_bytes(root, args)
        if out is None:
            return None, "cannot read the diff against {}".format(parent[:10])
        fields = out.decode("utf-8", "surrogateescape").split("\0")
        found = {path: st[:1] for st, path in zip(fields[0::2], fields[1::2]) if path}
        own = found if i == 0 else {p: s for p, s in own.items() if p in found}
    return own or {}, None


def _close_homes(own, branch, wi):
    """`(paths, remap)` a close of `wi` in this commit may write besides its
    spec: the closed copy and its report, and the remap its inbound-link
    edits follow. Empty when the commit does not move the spec out of
    `active/<branch>/` into a closed folder.

    Implements: SR-154, LLR-337
    """
    gone = [
        p
        for p, st in own.items()
        if st == "D" and p.startswith("docs/work/active/{}/{}-".format(branch, wi))
    ]
    landed = [
        p
        for p, st in own.items()
        if st == "A" and (m := _kdone._CLOSED_SPEC_RE.match(p)) and m.group(1) == wi
    ]
    if not gone or not landed:
        return set(), {}
    report = _station.report_path(branch, wi)
    return {landed[0], report}, {gone[0]: landed[0]}


def _regenerated(path, parents):
    """Is `path`, changed by a merge as its own, what the station refresh
    writes (trunk merged in, then the trunk step): the compiled log, or a
    view `trunk_step.regen_writes` lists (a `/`-terminated entry a prefix)?
    Outside a merge, never.

    Implements: SR-154, LLR-337
    """
    if len(parents) < 2:
        return False
    if path == _COMPILED_LOG:
        return True
    return any(
        path.startswith(w) if w.endswith("/") else path == w
        for w in trunk_step.regen_writes()
    )


def _is_home(path, branch, claimed):
    """Is `path` a record home of the lane (a plan home, a review, decision or
    session record, a log fragment, or a claimed row's own spec)?

    Implements: SR-154, LLR-337
    """
    if path.startswith(_HOME_PREFIXES):
        return True
    if any(path.startswith(plan_pass.plan_dir(w) + "/") for w in claimed):
        return True
    folder = "docs/work/active/{}/".format(branch)
    name = path[len(folder) :] if path.startswith(folder) else ""
    return any(re.match(r"^{}-[^/]*\.md$".format(w), name) for w in claimed)


def build_paths(root, rev, parents, own, branch, claimed):
    """The paths of `own` (the commit's own changes) outside every record
    home and every claimed row's close: its build output.

    Implements: SR-154, LLR-337
    """
    homes, remap = set(), {}
    for wi in claimed:
        paths, moves = _close_homes(own, branch, wi)
        homes |= paths
        remap.update(moves)
    out = []
    for path, status in sorted(own.items()):
        if _is_home(path, branch, claimed) or path in homes:
            continue
        if _regenerated(path, parents):
            continue
        relink = remap and status == "M" and path.endswith(".md")
        if relink and spec_move.exact_relink(
            plan_pass.blob(root, parents[0], path)[0],
            plan_pass.blob(root, rev, path)[0],
            path,
            remap,
        ):
            continue
        out.append(path)
    return out


def binding_problem(root, parents, rev, branch, wi, claimed_text):
    """None when a parent holds a pass record binding `wi`'s plan and
    Done-when as the commit `rev` (None: the index) leaves them, else why:
    no record, a record outside its grammar, or one naming another row, plan
    or Done-when.

    Implements: SR-154, LLR-337
    """
    plan, _delta, why = plan_pass.plan_digest(root, rev, wi)
    if why and plan is None:
        return why
    done, why = plan_pass.done_when_digest(root, rev, branch, wi, claimed_text)
    if why:
        return why
    reasons = []
    for parent in parents:
        data, why = plan_pass.blob(root, parent, plan_pass.record_path(wi))
        if data is None:
            reasons.append(why or "no pass record at {}".format(parent[:10]))
            continue
        fields, why = plan_pass.parse(data.decode("utf-8", "replace"))
        if why:
            reasons.append("its pass record is malformed: {}".format(why))
            continue
        want = {"wi": wi, "plan": plan, "done_when": done}
        bad = [k for k, v in want.items() if fields[k] != v]
        if not bad:
            return None
        reasons.append(_unbound(bad))
    return "; ".join(reasons)


def _unbound(keys):
    """Why a readable record binds nothing, by the keys that differ.

    Implements: SR-154, LLR-337
    """
    if "wi" in keys:
        return "its pass record names another row"
    return (
        "its pass record binds another {} (it changed after the verdict): a new "
        "critique must pass the changed plan".format(
            " and ".join(k.replace("_", "-") for k in keys)
        )
    )


def record_problems(root, at, fields, branch, wi, claimed_text, deep=True):
    """THE PASS RULE, stated once: every reason the pass record `fields` is
    not supported by the tree at the commit `at` (the record's parent at the
    commit, HEAD at the filing step), [] when it is. Its digests are `at`'s
    plan and Done-when; its delta is `none` or `within` and is the plan's
    own line; the critique it cites is in `at`, byte for byte, bound to the
    commit it reviewed and in the verdict format; that critique reads as an
    APPROVE (`kitlib.verdict.effective_verdict`), or, as the second critique
    at the cap, every BLOCKER and MAJOR finding of it is ruled DISMISS by the
    accepted dispute verdict the record cites. With `deep`, the reviewed
    commit's tree holds the same plan bytes and Done-when digest.

    Implements: SR-154, LLR-337
    """
    problems = []
    plan, delta, why = plan_pass.plan_digest(root, at, wi)
    if why:
        problems.append(why)
    elif delta not in plan_pass.PASSING_DELTAS:
        problems.append("the plan's delta is `{}`, which never passes".format(delta))
    elif (fields["plan"], fields["delta"]) != (plan, delta):
        problems.append(
            "its plan digest or delta is not the plan's at {}".format(at[:10])
        )
    done, why = plan_pass.done_when_digest(root, at, branch, wi, claimed_text)
    if why or fields["done_when"] != done:
        problems.append(why or "its Done-when digest is not the one at " + at[:10])
    if fields["wi"] != wi:
        problems.append("it names {}, not {}".format(fields["wi"], wi))
    if deep:
        problems += _reviewed_problems(root, fields, branch, wi, claimed_text)
    return problems + _critique_problems(root, at, fields)


def _reviewed_problems(root, fields, branch, wi, claimed_text):
    """Why the commit the critique reviewed does not hold the plan bytes and
    Done-when digest the record binds, compared by content, or [].

    Implements: SR-154, LLR-337
    """
    reviewed = fields["reviewed"]
    plan, _delta, why = plan_pass.plan_digest(root, reviewed, wi)
    done, why2 = plan_pass.done_when_digest(root, reviewed, branch, wi, claimed_text)
    if plan is None or why2:
        return [
            "the reviewed commit {} cannot be read: {}".format(
                reviewed[:10], why or why2
            )
        ]
    if (plan, done) != (fields["plan"], fields["done_when"]):
        return [
            "the critique reviewed other plan bytes or another Done-when than "
            "the record binds: a fresh critique must judge the changed inputs"
        ]
    return []


def _critique_problems(root, at, fields):
    """Why the critique (and any dispute verdict) the record cites does not
    support a pass at `at`, or [].

    Implements: SR-154, LLR-337
    """
    data, why = plan_pass.blob(root, at, fields["critique"])
    if data is None:
        return ["the critique {} is not in {}".format(fields["critique"], at[:10])]
    if plan_pass.bytes_digest(data) != fields["critique_digest"]:
        return [
            "the critique {} is not the one the record cites".format(fields["critique"])
        ]
    text = data.decode("utf-8", "replace")
    why = _kverdict.filing_refusal(
        text, fields["reviewed"], score_reviews.parse_verdict
    )
    if why:
        return ["the critique is not a filed verdict: {}".format(why)]
    parsed = score_reviews.parse_verdict(text)
    word = _kverdict.effective_verdict(parsed.verdict, parsed.findings)
    if word == "APPROVE":
        return ["an approved critique cites no dispute"] if fields["dispute"] else []
    return _cap_problems(root, at, fields, parsed.findings)


def blocking_ids(findings):
    """The `F#` ids (in finding order, `plan_coverage.finding_clauses`') of a
    critique's BLOCKER and MAJOR findings.

    Implements: SR-154, LLR-337
    """
    return [
        "F{}".format(n)
        for n, f in enumerate(findings, 1)
        if str(f.severity).upper() in _BLOCKING
    ]


def _cap_problems(root, at, fields, findings):
    """A critique that does not read as an APPROVE passes only as the second
    one, at the cap, whose every BLOCKER and MAJOR finding the cited accepted
    dispute verdict rules DISMISS.

    The set of BLOCKER and MAJOR findings is never empty here. The only
    caller, `_critique_problems`, first refuses a CHANGES-REQUESTED that names
    no finding (`kitlib.verdict.filing_refusal`) and reads one whose findings
    are all MINOR as an APPROVE (`kitlib.verdict.effective_verdict`), and a
    finding's severity is always BLOCKER, MAJOR or MINOR.

    Implements: SR-154, LLR-337
    """
    if (
        plan_pass.critique_round(fields["wi"], fields["critique"])
        < plan_pass.MAX_CRITIQUES
    ):
        return [
            "the first critique requests changes: revise once, and a second "
            "fresh critique judges the revision"
        ]
    blocking = blocking_ids(findings)
    if not fields["dispute"]:
        return [
            "the second critique's BLOCKER and MAJOR findings go to one "
            "dispute sitting; the record cites none"
        ]
    data, _why = plan_pass.blob(root, at, fields["dispute"])
    if data is None or plan_pass.bytes_digest(data) != fields["dispute_digest"]:
        return [
            "the dispute verdict {} is not in {} as cited".format(
                fields["dispute"], at[:10]
            )
        ]
    return _dismissals(root, at, fields, blocking)


def _dismissals(root, at, fields, blocking):
    """Why the cited dispute verdict, read at `at` with its binding, is not
    an ACCEPTED dispute verdict ruling each blocking finding DISMISS, or [].
    A FIX or an ESCALATE is the owner's, never the build's. Which finding the
    sitting ruled, as the findings file beside it records it, is checked once,
    at the filing step (`plan_coverage.ruling_problem`); this re-reads what a
    rebase cannot change.

    Implements: SR-154, LLR-337
    """
    path = fields["dispute"]
    verdict, _why = plan_pass.blob(root, at, path)
    binding, _why = plan_pass.blob(root, at, _sitting.requested_path(path))
    bound = binding and _sitting.read_requested(binding.decode("utf-8", "replace"))
    if not bound or bound[0] != _dispute.BRIEF:
        return ["{} is not a dispute verdict with its binding".format(path)]
    if bound[2] != "accepted":
        return ["the dispute call {} has outcome {}".format(path, bound[2])]
    rulings, why = _dispute.parse(verdict.decode("utf-8", "replace"), bound[1], path)
    if why:
        return ["the dispute verdict is refused: {}".format(why)]
    return [
        "{}: the dispute verdict rules it {}; only a DISMISS lets the plan "
        "pass, and anything else is the owner's".format(
            fid, (rulings.get(fid) or ("nothing",))[0]
        )
        for fid in blocking
        if (rulings.get(fid) or ("",))[0] != "DISMISS"
    ]


def _record_lines(root, rev, parent, branch, wi, claimed_text, deep):
    """The pass-record commit's own check against its parent.

    Implements: SR-154, LLR-337
    """
    data, why = plan_pass.blob(root, rev, plan_pass.record_path(wi))
    if data is None:
        return [why] if why else []
    fields, why = plan_pass.parse(data.decode("utf-8", "replace"))
    if why:
        return ["its pass record is malformed: {}".format(why)]
    return record_problems(root, parent, fields, branch, wi, claimed_text, deep)


def commit_lines(root, rev, parents, branch, claim_rev, deep=True):
    """THE GATE: one line per hold on the lane commit `rev` (None: the index)
    against `parents`, for the rows `branch` claimed whose claim copy at
    `claim_rev` declares `single`; [] when nothing holds.

    Implements: SR-154, LLR-337
    """
    rows, claimed, lines = plan_pass.gate_rows(root, claim_rev, branch)
    if not rows or not parents:
        return lines
    own, why = _own_changes(root, rev, parents)
    if why:
        return lines + ["{}: {}".format(", ".join(w for w, _t in rows), why)]
    build = build_paths(root, rev, parents, own, branch, claimed)
    for wi, claimed_text in rows:
        if own.get(plan_pass.record_path(wi), "D") != "D":
            found = _record_lines(root, rev, parents[0], branch, wi, claimed_text, deep)
            lines += ["{}: {}".format(wi, w) for w in found]
        why = build and binding_problem(root, parents, rev, branch, wi, claimed_text)
        if why:
            lines.append(
                "{}: build output ({}) before a pass record binds its plan: {}; "
                "{}".format(wi, ", ".join(build[:3]), why, REMEDY)
            )
    return lines


def _parents(root, rev):
    """`rev`'s parents, read off the commit, or None when git cannot.

    Implements: SR-154, LLR-337
    """
    out = _kitgit.git_out(root, ["rev-list", "--parents", "-n", "1", rev])
    return None if out is None else out.split()[1:]


def lane_rider(claim_rev, branch, deep=False):
    """A `lane_commit_walk` rider judging each lane commit of `branch`
    against its own parents, its claim copies read at `claim_rev`.

    Implements: SR-154, LLR-337
    """

    def rule(root, rev):
        parents = _parents(root, rev)
        if parents is None:
            return ["commit {}: its parents cannot be read".format(rev[:10])]
        found = commit_lines(root, rev, parents, branch, claim_rev, deep)
        return ["commit {}: {}".format(rev[:10], line) for line in found]

    return rule


def landing_refusal(root, trunk, branch):
    """THE PLAN GATE AT THE SLOT: the refusal for the first commit of
    `trunk..branch` the gate holds, or None. A range git cannot list is a
    refusal, never a skip.

    Implements: SR-154, LLR-337
    """
    out = _kitgit.git_out(
        root, ["rev-list", "--reverse", "--topo-order", trunk + ".." + branch]
    )
    if out is None:
        return "cannot read {}'s commits to check its plan gate; nothing was merged".format(
            branch
        )
    walk = text_then_act.lane_commit_walk(
        root, out.split(), (lane_rider(trunk, branch),)
    )
    found = next(walk, None)
    return found and "{}: {}; nothing was merged".format(branch, "; ".join(found[1]))


def _squash_lines(root, head, tip):
    """The holds on each lane commit a squash of `tip` onto `head` carries,
    for every local branch containing `tip` (the lane being landed), its
    claim copies read at `head`, trunk's own.

    Implements: SR-154, LLR-337
    """
    lanes = _kitgit.git_out(
        root,
        ["for-each-ref", "--format=%(refname:short)", "--contains", tip, "refs/heads/"],
    )
    commits = _kitgit.git_out(
        root, ["rev-list", "--reverse", "--topo-order", head + ".." + tip]
    )
    if lanes is None or commits is None:
        return ["the squashed commits of {} cannot be read".format(tip[:10])]
    if not lanes.split():
        return _unattributed_squash(root, head, tip)
    out = []
    for lane in lanes.split():
        rider = lane_rider(head, lane)
        out += [
            ln
            for _r, lines in text_then_act.lane_commit_walk(
                root, commits.split(), (rider,)
            )
            for ln in lines
        ]
    return out


def _unattributed_squash(root, head, tip):
    """The hold on a squash of `tip` that no local branch contains (a deleted
    branch, a remote-tracking ref, a bare sha): the lane is the gate's only
    key to its claim copies, so while `head`'s tree carries any claim copy
    the gate would hold or gate (a `single` row, or a value outside the set),
    the squash holds by name; with none, nothing here could be held.

    Implements: SR-154, LLR-337
    """
    root_dir = "docs/work/active/"
    listing = _kitgit.git_out(root, ["ls-tree", "--name-only", head, root_dir])
    if listing is None:
        return ["{} cannot be read at {}".format(root_dir, head[:10])]
    for lane in (p[len(root_dir) :] for p in listing.splitlines()):
        rows, _claimed, holds = plan_pass.gate_rows(root, head, lane)
        if rows or holds:
            return [
                "no local branch contains the squashed tip {}, so the plan gate "
                "cannot tell whose claim copies to read; squash the lane's own "
                "branch (or, with no squash in progress, remove the stale "
                "SQUASH_MSG)".format(tip[:10])
            ]
    return []


def _claim_base(root, branch):
    """The lane's claim base: its integration base, or HEAD when that cannot
    be read and the lane holds no claim folder (trunk). None holds. With the
    trunk undeclared, a branch whose HEAD holds no claim folder is judged
    against HEAD, so a commit there is not refused over a key it does not
    need; any other branch raises `agent_common.TrunkUndeclared`, for the
    caller to hold naming the line.

    Implements: SR-154, LLR-337
    """
    folder = "docs/work/active/{}/".format(branch)
    try:
        base = agent_common.default_base(root)
    except agent_common.TrunkUndeclared:
        listed = _kitgit.git_out(root, ["ls-tree", "--name-only", "HEAD", "--", folder])
        if listed == "":
            return "HEAD"
        raise
    if base:
        return base
    listed = _kitgit.git_out(root, ["ls-tree", "--name-only", "HEAD", "--", folder])
    return "HEAD" if listed == "" else None


def staged_lines(root):
    """The `plan-gate` step's judgement of the commit being made: the index
    against HEAD (and MERGE_HEAD while a merge is in progress) for the
    current branch's own `single` rows; on a squash landing, also each lane
    commit it carries. Off git, or before the first commit, nothing holds.

    Implements: SR-154, LLR-337
    """
    head = (
        _kitgit.git_out(root, ["rev-parse", "--verify", "--quiet", "HEAD"]) or ""
    ).strip()
    if not head:
        return []
    merging = (
        _kitgit.git_out(root, ["rev-parse", "-q", "--verify", "MERGE_HEAD"]) or ""
    ).strip()
    squashed = [] if merging else _kitgit.squash_commits(root)
    lines = _squash_lines(root, head, squashed[0]) if squashed else []
    branch = (_kitgit.git_out(root, ["branch", "--show-current"]) or "").strip()
    if branch:
        parents = [head] + ([merging] if merging else [])
        try:
            base = _claim_base(root, branch)
        except agent_common.TrunkUndeclared as exc:
            return lines + [str(exc)]
        lines += commit_lines(root, None, parents, branch, base, deep=True)
    return lines


def main(argv=None):
    """The pre-commit hook's `plan-gate` step: exit 1 naming each hold, 0
    when the staged commit is not held.

    Implements: SR-154, LLR-337
    """
    utf8_console()
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--root", default=".", help="the checkout (default: cwd)")
    args = ap.parse_args(argv)
    lines = staged_lines(args.root)
    msg = (
        "\n".join(lines) or "no `single` row of this lane builds before its plan passes"
    )
    print("  {:5} plan-gate  {}".format("FAIL" if lines else "ok", msg))
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main())
