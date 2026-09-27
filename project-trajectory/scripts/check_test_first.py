#!/usr/bin/env python3
"""check_test_first.py — the test-first order, read from committed history.

WHY THE ORDER IS THE EVIDENCE. A test written after the code tends to describe
what the code does rather than what was required, so a passing run stops being
evidence that the requirement is met. The stage ladder puts test cases before
implementation for a project as a whole, but not requirement by requirement: a
project whose derived stage still reads DevStg-Tests can already carry
requirements whose code landed before their test cases were approved. This
reads that order per requirement, from the one record of order that no registry
cell can restate after the fact: the commits on trunk.

TWO EVENTS, BOTH READ FROM TRUNK'S FIRST-PARENT HISTORY, OLDEST FIRST.

  * A requirement's implementation LANDS at the earliest first-parent commit
    that adds a line declaring it implements the requirement or one of its
    design rows. A declaration is what `gen_arch_map.backlink_ids` says it is,
    over the declared source surface (`--src`; the harness passes
    `docs/stack.ini` `[paths] src`) and the file types the reverse back-link
    scan reads, so a landing and the coverage number cannot disagree about what
    counts. Tests and documents are not code declaring an implementation. The
    earlier of the requirement's own line and any design row's line is the
    landing. A merge lands everything it brings at the merge.
  * A test case is APPROVED FOR A REQUIREMENT at the earliest commit in which
    it reads approved AND names the requirement or one of its design rows, the
    design rows being those whose `SR-Refs` name the requirement at that
    commit. Approval alone is not enough: a test case approved for something
    else and re-pointed at the requirement after its code landed would bring
    an order it never had, and re-pointing a design row is the same move one
    tier down. Each commit touching the test-case or design registry is parsed
    on both sides through `acceptance_record`'s row reader and approval-act
    rule, never counted: a commit that approves one test case while
    withdrawing another leaves the number of approved rows unchanged, and a
    count would see nothing happen. These approvals are read over the whole
    readable history, never from the declared start: SR-217 scopes only the
    requirement's approval, so a test case approved after the code landed
    stays late even when both happened before the start.

A requirement is judged when its own first approval falls after the declared
start and its implementation has landed. Its test cases are those whose
`Verifies` names it or one of its design rows at the tip; WHEN each became its
approved test case is read from history as above. Each one approved for it
after the landing is reported, naming the requirement, the implementation
commit and the approval commit. Each one that does not read approved at the tip
is reported by name: whatever its run says, it says it against text nobody has
approved. Every test case the report names carries the warning that its result
may not reflect the intended behaviour, since that is what the order is
evidence of. Nothing here stops a test from running. A requirement whose
implementation has not landed is not judged yet. No cell is ever read for WHEN
anything happened.

AN APPROVAL WITHOUT AN EXACT DATE. The TOML registries are the readable
history. A row already approved when its registry arrived under TOML from an
older carrier, and a row moved into `Approved` from a word outside the closed
status vocabulary (a rename, not the act), was approved AT OR BEFORE that
commit. Such a date still settles the order when it falls at or before the
landing (for a requirement's own approval, at or before the start); when it
falls after, the order cannot be read, and the requirement is reported as
unread, never passed.

THE DECLARED START is `[checks] test_first_since` in `docs/process.toml`: a
commit id. A project that adopts the rule declares where its judgement begins,
so requirements approved in history written before the rule are not judged
against it. The shipped template declares the key empty, and an empty or
absent key judges the whole history.

UNREADABLE IS NEVER A PASS. A shallow clone, a declared start that names no
commit or never stood on trunk's first-parent line, a declared start before the
TOML registries, and registries still under an older carrier are each reported
as unreadable, and nothing is judged. A rewrite that keeps the start on trunk
is read as the history it now is.

WARN-ONLY IN THE SHIPPED WIRING. The harness's `test-first` step runs this at
every rung without `--strict`, so a finding is reported and never refuses a
commit: the order is evidence a reviewer weighs, and promoting it to a gate is a
project's own ruling. `--strict` makes that ruling for one run.

Contracts: IF-198 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-198: the test-first verdict the harness reads back from the
    `test-first` step. Each requirement with a test case approved for it after
    its implementation landed, or not approved, prints one WARN line naming the
    requirement, the implementation commit, every late approval commit and
    every test case not approved, with the warning that their results may not
    reflect the intended behaviour, and one summary line follows; a history with none prints one OK line. An unreadable history, and
    a declared start that cannot be read, each print one WARN line saying the
    order was not judged and that this is not a pass. A requirement whose
    order rests on an approval with no exact date is named on its WARN line as
    one whose order cannot be read, and counts in the summary. The exit is 0
    for every one of those. `--strict` prints FAIL instead of WARN and exits 1 for each
    of them but the OK line; the shipped step never passes it. argparse's own
    exit 2 for a malformed command line is the one other code.
"""

import argparse
import sys
from collections import namedtuple
from pathlib import Path

import acceptance_record
import gen_arch_map
import spine_carrier
from kitlib.config import process_check_text, utf8_console
from kitlib.git import git_out
from kitlib.spine import STATUS_VALUES, is_approved, is_founded, refs

START_KEY = "test_first_since"

# The registries, from the approval-act readers' own table so a path has one
# home; the history is judged over the requirement and test-case tiers, and the
# design tier joins a requirement to the code lines that name its design rows
# and to the test cases that reach it through them.
_REGISTRY = {col: path for path, col in acceptance_record.SPINE_CSVS}
REQUIREMENTS = (_REGISTRY["SR-ID"], "SR-ID")
DESIGN_ROWS = (_REGISTRY["LLR-ID"], "LLR-ID")
TEST_CASES = (_REGISTRY["TC-ID"], "TC-ID")
# Every registry the order is read from, so each is held to the TOML history.
READ = (REQUIREMENTS, DESIGN_ROWS, TEST_CASES)

# `late` is ((test case id, approval commit), ...) in trunk order; `unread` is
# the same shape for each approval with no exact date whose order is unknown;
# `unapproved` is (test case id, ...) for each that does not read approved.
Finding = namedtuple("Finding", "requirement implementation late unread unapproved")

# A row's first approval: the commit, and whether it is the act itself (True)
# or only a commit the row was approved at or before (False).
Approval = namedtuple("Approval", "commit exact")

# A flip from one of these words is the approval act; from any other, a rename.
_VOCABULARY = {word.lower() for word in STATUS_VALUES}


class HistoryUnreadable(Exception):
    """The history cannot show the order. Raised rather than returned so no
    caller can take an unreadable history for one with nothing to report."""


def _commit(root, rev):
    """The full id of the commit `rev` names, or None."""
    out = git_out(root, ["rev-parse", "--verify", "--quiet", rev + "^{commit}"])
    return out.strip() if out and out.strip() else None


def _first_parent(root, rev):
    """Trunk's first-parent line ending at `rev`, oldest first."""
    out = git_out(root, ["rev-list", "--first-parent", "--reverse", rev])
    return out.split() if out else []


def _span(start, rev):
    """The first-parent range after `start`, or the whole line without one."""
    return "{}..{}".format(start, rev) if start else rev


def _older_carriers(registries):
    """The non-TOML carrier paths of `registries` ((path, id column) pairs)."""
    return [
        c
        for path, _col in registries
        for c in spine_carrier.carriers(path)
        if c != path
    ]


def _held(root, rev, paths):
    """The `paths` present in `rev`'s tree."""
    return [
        p for p in paths if git_out(root, ["cat-file", "-e", rev + ":" + p]) is not None
    ]


def _older_carrier_paths(root, start, rev):
    """The read registries' non-TOML carrier paths the walks from `start`
    would read: held in the start commit's tree, or changed by a first-parent
    commit after it."""
    paths = _older_carriers(READ)
    args = ["rev-list", "--first-parent", _span(start, rev), "--", *paths]
    return _held(root, start, paths) or (
        paths if (git_out(root, args) or "").split() else []
    )


def history_unreadable(root, start=None, rev="HEAD"):
    """Why the history ending at `rev` cannot show the order, or None when it
    can. `start` is the declared start commit, or None for the whole history.

    Each answer here is a history in which a finding could be missing or false,
    so each is reported rather than read: a shallow clone has lost the commits
    an approval or a landing sits on; a start that names no commit, or one that
    never stood on trunk's first-parent line, gives nothing to order after; and
    registries under the older carrier were written in an older status
    vocabulary, so a first approval read across them would date the rename
    rather than the act. That bars registries still under the older carrier
    at `rev`, and a declared start before the TOML registries; with no start,
    the history before the cutover is simply not read, and an approval it held
    carries no exact date (`first_approval_commits`). The design registry is
    held to the same rule as the two judged ones: a test case reaches a
    requirement through a design row, so a design registry the TOML reader
    cannot see would drop that test case in silence rather than report it. A
    history rewritten with the start still on trunk reads as the history it
    now is.

    Implements: SR-217, LLR-257
    """
    if _commit(root, rev) is None:
        return (
            "no commit history at {} (not a git repository, git is not on "
            "PATH, or nothing is committed yet)".format(rev)
        )
    shallow = git_out(root, ["rev-parse", "--is-shallow-repository"])
    if (shallow or "").strip() == "true":
        return (
            "this is a shallow clone, so the commits before its graft are "
            "missing (git fetch --unshallow restores them)"
        )
    if start:
        sha = _commit(root, start)
        if sha is None:
            return (
                "the declared start {} names no commit in this repository "
                "(rewritten away, or never fetched)".format(start)
            )
        if sha not in set(_first_parent(root, rev)):
            return (
                "the declared start {} is not on {}'s first-parent history: it "
                "never stood on trunk, so nothing is ordered after it".format(
                    start, rev
                )
            )
    still = _held(root, rev, _older_carriers(READ))
    if still:
        return (
            "the registries at {} are still under an older carrier ({}), whose "
            "status vocabulary cannot date an approval; move them to "
            "TOML".format(rev, ", ".join(still))
        )
    older = _older_carrier_paths(root, start, rev) if start else []
    if older:
        return (
            "the history from {} reaches back before the TOML registries ({} "
            "under an older carrier); declare [checks] {} at or after the "
            "commit that moved them to TOML".format(start, ", ".join(older), START_KEY)
        )
    return None


def first_approval_commits(root, registry, id_col, since=None, rev="HEAD"):
    """`{row id: Approval}` — the commit at which each row of one spine
    registry (its TOML carrier) first reads approved, on the first-parent line
    ending at `rev`, walked from `since` or from the root when None.

    Walks the commits that touch the registry oldest first, reading each one's
    rows through `acceptance_record.rows_at` and judging the move from the
    rows before it with `acceptance_record.approval_acts_between`. The before
    side of each commit is the previous touching commit's rows: nothing
    between them on the first-parent line changed the file, so it is the same
    text a second read would return. A row's later re-approvals are not its
    first.

    An approval is EXACT when it is the act: a birth into a registry that
    already stood under TOML or that no carrier held before, or a flip from a
    word of the closed status vocabulary. Otherwise the row was approved at or
    before the commit and the date is not exact: a row already approved at
    `since`, one already approved when the registry arrived from an older
    carrier (whose history is not read), and one moved into `Approved` from a
    retired word, which is a rename rather than the act.

    Implements: SR-217, LLR-257
    """
    before = acceptance_record.rows_at(root, since, registry, id_col) if since else {}
    first = {
        act["id"]: Approval(since, False)
        for act in acceptance_record.approval_acts_between(registry, {}, before)
    }
    out = git_out(
        root,
        ["rev-list", "--first-parent", "--reverse", _span(since, rev), "--", registry],
    )
    if out is None:
        raise HistoryUnreadable("git could not list the commits touching " + registry)
    shas = out.split()
    # From the root, the first commit touching the TOML carrier either creates
    # the registry or moves it from an older one; only the move hides a date.
    carried = not since and _carried_at(root, shas, (registry, id_col))
    for sha in shas:
        after = acceptance_record.rows_at(root, sha, registry, id_col)
        _record_first(first, registry, before, after, Approval(sha, not carried))
        before, carried = after, False
    return first


def _carried_at(root, shas, registry):
    """True when the first of `shas` (the commits touching `registry`, a
    (path, id column) pair, oldest first) moved it from an older carrier."""
    return bool(shas and _held(root, shas[0] + "^", _older_carriers([registry])))


def _record_first(first, registry, before, after, at):
    """Record in `first` each row's first approval act from `before` to
    `after`, at `at`: exact only when `at` is and the act is a birth or a flip
    from a word of the closed status vocabulary (anything else is a rename)."""
    for act in acceptance_record.approval_acts_between(registry, before, after):
        if act["id"] not in first:
            exact = at.exact and (
                act["act"] == "born" or act["before"].lower() in _VOCABULARY
            )
            first[act["id"]] = Approval(at.commit, exact)


def _touching(root, paths, rev):
    """The first-parent commits ending at `rev` that touch any of `paths`,
    oldest first."""
    args = ["rev-list", "--first-parent", "--reverse", rev, "--", *paths]
    out = git_out(root, args)
    if out is None:
        raise HistoryUnreadable("git could not list the commits touching " + paths[0])
    return out.split()


def _associations(tests, design):
    """`{(test case id, requirement id): test-case row}` for every test case
    and each requirement it names, directly or through a design row whose
    `SR-Refs` names it, in one commit's rows. An id no design row carries
    stands for itself, so a requirement named directly is its own key."""
    owners = {lid: refs(row.get("SR-Refs")) for lid, row in design.items()}
    return {
        (tid, rid): row
        for tid, row in tests.items()
        for vid in refs(row.get("Verifies"))
        for rid in owners.get(vid, [vid])
    }


def first_association_commits(root, rev="HEAD"):
    """`{(test case id, requirement id): Approval}` — the commit at which each
    test case first reads approved AND names the requirement or one of its
    design rows, on the first-parent line ending at `rev`, walked from the
    root.

    Approval alone does not make a test case a requirement's: re-pointing a
    test case approved for something else at a requirement whose code has
    already landed, or re-pointing the design row it names, would otherwise
    lend the requirement an order it never had. So the pair is the row: each
    commit touching the test-case or design registry is read through
    `acceptance_record.rows_at`, the pairs it holds are built from both
    registries as they stand at that commit, and the move from the pairs
    before is judged with the same approval-act rule as a single row's. A pair
    arriving while its test case already reads approved is born approved, at
    that commit; a test case flipping to approved while it names the
    requirement flips its pairs. Exactness is `first_approval_commits`' rule,
    and a pair that first shows at the commit either registry moved from an
    older carrier is dated at or before that commit.

    Implements: SR-217, LLR-257
    """
    registries = (TEST_CASES, DESIGN_ROWS)
    touching, carried = {}, set()
    for reg in registries:
        shas = _touching(root, [reg[0]], rev)
        touching[reg[0]] = set(shas)
        if _carried_at(root, shas, reg):
            carried.add(shas[0])
    rows = {path: {} for path, _col in registries}
    before, first = {}, {}
    for sha in _touching(root, [path for path, _col in registries], rev):
        for path, col in registries:
            if sha in touching[path]:
                rows[path] = acceptance_record.rows_at(root, sha, path, col)
        after = _associations(rows[TEST_CASES[0]], rows[DESIGN_ROWS[0]])
        at = Approval(sha, sha not in carried)
        _record_first(first, TEST_CASES[0], before, after, at)
        before = after
    return first


def _declared_ids(patch):
    """Yields `(commit, id)` in patch order for each id an ADDED line of a
    `git log -p` over the source surface declares, in the file types the
    back-link scan reads. Hunk bodies are told from file headers by state, so
    an added line whose text starts with `++` is still a line."""
    exts = tuple(e.lower() for e in gen_arch_map.BACKLINK_EXTS)
    sha, readable, in_hunk = None, False, False
    # Split on newlines only: `splitlines` would also break a source line at a
    # form feed, and the tail would lose the `+` that marks it added.
    for line in patch.split("\n"):
        if line.startswith("\0"):
            sha, readable, in_hunk = line[1:].strip(), False, False
        elif line.startswith("diff --git "):
            readable, in_hunk = False, False
        elif not in_hunk and line.startswith("+++ "):
            path = line[4:].strip().strip('"')
            readable = path.lower().endswith(exts)
        elif line.startswith("@@"):
            in_hunk = True
        elif in_hunk and readable and line.startswith("+"):
            for rid in gen_arch_map.backlink_ids(line[1:]):
                yield sha, rid


def first_implementation_commits(root, src="src", rev="HEAD"):
    """`{spine id: commit}` — the earliest first-parent commit ending at `rev`
    that adds a line under `src` declaring it implements that id.

    One `git log` over the whole first-parent history, not from the declared
    start: a requirement approved after the start can still have code that
    declared it before, and that earlier line is where it landed. `-G` keeps
    the patch to the files whose added or removed lines carry the marker, and
    only added lines are read. Merges are diffed against their first parent,
    so everything a merge brings to trunk lands at the merge. The `-c` pins
    keep a user's own log configuration (a hidden root diff, a combined merge
    diff, quoted paths) from changing what is read.

    Implements: SR-217, LLR-257
    """
    surface = src.strip().replace("\\", "/").strip("/")
    args = [
        "-c",
        "core.quotepath=off",
        "-c",
        "log.diffMerges=first-parent",
        "-c",
        "log.showRoot=true",
        "log",
        "--first-parent",
        "-m",
        "--reverse",
        "-p",
        "-U0",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        "--no-renames",
        "-G" + gen_arch_map.IMPLEMENTS_MARKER,
        "--format=%x00%H",
        rev,
    ]
    if surface and surface != ".":
        args += ["--", surface]
    patch = git_out(root, args)
    if patch is None:
        raise HistoryUnreadable("git could not read the history under " + src)
    first = {}
    for sha, rid in _declared_ids(patch):
        first.setdefault(rid, sha)
    return first


def _id_key(rid):
    prefix, _, number = rid.rpartition("-")
    return (prefix, int(number) if number.isdigit() else 0, rid)


def _members(root, rev):
    """`(design rows by requirement, test cases by verified id, the test cases
    reading approved)` at the tip."""
    design, tests, standing = {}, {}, set()
    for lid, row in acceptance_record.rows_at(root, rev, *DESIGN_ROWS).items():
        for sr in refs(row.get("SR-Refs")):
            design.setdefault(sr, []).append(lid)
    for tid, row in acceptance_record.rows_at(root, rev, *TEST_CASES).items():
        for vid in refs(row.get("Verifies")):
            tests.setdefault(vid, []).append(tid)
        if is_approved(row) or is_founded(row):
            standing.add(tid)
    return design, tests, standing


def test_first_findings(root, src="src", start=None, rev="HEAD"):
    """One `Finding` per requirement first approved after `start` whose
    implementation first landed on trunk before one of its test cases was
    approved for it, or with one of them not approved — the requirement, the
    implementation commit, each late test case with its approval commit in
    trunk order, and each test case not approved — or whose order cannot be
    read.

    Raises `HistoryUnreadable` for any history `history_unreadable` names, so
    an unreadable history can never come back as an empty, passing list. A
    test case approved at the same commit the implementation landed is not
    after it. The start scopes only which requirements are judged: test-case
    approvals are read over the whole readable history, so one approved after
    the landing is late wherever the start sits. A requirement's test cases
    are its chain's members at the tip; a test case not reading approved there
    has no approval for it, whatever its history, and each one that does is
    dated at its first approved-and-associated commit (see the module
    docstring).

    Implements: SR-217, LLR-257
    """
    reason = history_unreadable(root, start, rev)
    if reason:
        raise HistoryUnreadable(reason)
    start = _commit(root, start) if start else None
    order = {sha: i for i, sha in enumerate(_first_parent(root, rev))}
    approved = first_approval_commits(root, *REQUIREMENTS, since=start, rev=rev)
    landed = first_implementation_commits(root, src, rev)
    design, tests, standing = _members(root, rev)
    tc_approved = {
        pair: at
        for pair, at in first_association_commits(root, rev).items()
        if pair[0] in standing
    }
    out = []
    for sr in sorted(approved, key=_id_key):
        own = approved[sr]
        if own.commit == start:
            continue  # approved at or before the start: not in scope
        judged = _judged([sr, *design.get(sr, [])], landed, tests, tc_approved, order)
        if judged is None:
            continue
        landing, late, unread, unapproved = judged
        if start and not own.exact:
            # Approved at or before a commit after the start: whether it
            # entered scope at all cannot be read.
            late, unread, unapproved = (), ((sr, own.commit),), ()
        if late or unread or unapproved:
            out.append(Finding(sr, landing, late, unread, unapproved))
    return out


def _judged(chain, landed, tests, approvals, order):
    """`(landing, late, unread, unapproved)` for one requirement's chain — the
    requirement first, then its design rows: the earliest landing among them;
    each test case of the chain approved for the requirement strictly after
    it; each whose approval has no exact date and falls after it, whose order
    cannot be read; and each with no approval for the requirement in
    `approvals`, keyed `(test case, requirement)`. Pairs are
    `(test case, commit)` in trunk order. None when nothing in the chain has
    landed, which is not judged yet."""
    landings = [landed[i] for i in chain if i in landed]
    if not landings:
        return None
    landing = min(landings, key=order.__getitem__)
    members = {tid for i in chain for tid in tests.get(i, [])}
    dated = {t: approvals[(t, chain[0])] for t in members if (t, chain[0]) in approvals}
    after = {(t, a) for t, a in dated.items() if order[a.commit] > order[landing]}

    def ordered(exact):
        pairs = {(tid, a.commit) for tid, a in after if a.exact is exact}
        return tuple(sorted(pairs, key=lambda p: (order[p[1]], _id_key(p[0]))))

    unapproved = tuple(sorted(members - set(dated), key=_id_key))
    return landing, ordered(True), ordered(False), unapproved


def _report(findings, since, level):
    """The printed report's lines for a readable history."""
    lines = ["test-first: {} - {}".format(level, _finding_text(f)) for f in findings]
    if findings:
        lines.append(
            "test-first: {} requirement(s) approved since {} had a test case "
            "approved after the implementation landed or not approved, or an "
            "order that cannot be read".format(len(findings), since)
        )
    else:
        lines.append(
            "test-first: OK - no requirement approved since {} has a test case "
            "approved after its implementation landed or not approved".format(since)
        )
    return lines


def _finding_text(f):
    """One finding as the words of its one report line."""
    landed = "{} landed at {} (its first declaring line)".format(
        f.requirement, f.implementation[:10]
    )
    parts = []
    if f.late:
        parts.append(
            "{} test case(s) were approved after it: {}".format(
                len(f.late),
                ", ".join("{} at {}".format(tid, sha[:10]) for tid, sha in f.late),
            )
        )
    if f.unapproved:
        parts.append(
            "{} test case(s) are not approved: {}".format(
                len(f.unapproved), ", ".join(f.unapproved)
            )
        )
    if f.late or f.unapproved:
        parts.append(
            "a result from those test cases may not reflect the intended behaviour"
        )
    if f.unread:
        parts.append(
            "the order against {} cannot be read (approved at or before a later "
            "commit, with no exact date)".format(
                ", ".join(
                    "{} at or before {}".format(rid, sha[:10]) for rid, sha in f.unread
                )
            )
        )
    return "{}; {}".format(landed, "; ".join(parts))


def _not_judged(what, why, strict):
    """Print the one line for a history the order was not read from; the exit
    code. Worded so the line can never be read as a clean result."""
    print(
        "test-first: {} - {}: {}. The order was not judged, which is not a "
        "pass.".format("FAIL" if strict else "WARN", what, why)
    )
    return 1 if strict else 0


def main(argv=None):
    """The `test-first` step's entry point: reads the declared start, then
    prints the report and returns the exit code IF-198 states.

    Implements: SR-217
    """
    utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--src",
        default="src",
        help="the declared source surface a landing is read under (default: "
        "src; the harness passes docs/stack.ini [paths] src)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="print FAIL and exit 1 for a finding, or for a history or declared "
        "start that cannot be read (the shipped step omits it: warn-only)",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    level = "FAIL" if args.strict else "WARN"
    try:
        start = process_check_text(root, START_KEY)
    except ValueError as exc:
        return _not_judged("the declared start cannot be read", exc, args.strict)
    try:
        findings = test_first_findings(root, src=args.src, start=start)
    except HistoryUnreadable as exc:
        return _not_judged("history unreadable", exc, args.strict)
    since = (
        "the declared start {}".format(start[:10])
        if start
        else "the root (no [checks] {} declared)".format(START_KEY)
    )
    print("\n".join(_report(findings, since, level)))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
