#!/usr/bin/env python3
"""check_test_first.py — the test-first order, read from committed history.

WHY THE ORDER IS THE EVIDENCE. A test written after the code tends to describe
what the code does rather than what was required, so a passing run stops being
evidence that the requirement is met. The stage ladder puts test cases before
implementation for a project as a whole, but not requirement by requirement: a
project whose derived stage still reads DevStg-Tests can already carry
requirements whose code landed before their test cases were accepted. This
reads that order per requirement, from the one record of order that no registry
cell can restate after the fact: the commits on trunk.

TWO EVENTS, BOTH ORDERED ON TRUNK'S FIRST-PARENT LINE.

  * A requirement's implementation LANDS at the earliest first-parent commit
    that adds a line declaring it implements the requirement or one of its
    design rows. A declaration is what `gen_arch_map.backlink_ids` says it is,
    over the declared source surface (`--src`; the harness passes
    `docs/stack.ini` `[paths] src`) and the file types the reverse back-link
    scan reads, so a landing and the coverage number cannot disagree about what
    counts. Tests and documents are not code declaring an implementation. The
    earlier of the requirement's own line and any design row's line is the
    landing. A merge lands everything it brings at the merge.
  * A test case is ACCEPTED FOR A REQUIREMENT at the earliest acceptance act
    whose copy in the acceptance record holds it accepted AND naming the
    requirement or one of its design rows, the design rows being those whose
    `SR-Refs` name the requirement in that same copy. Acceptance alone is not
    enough: a test case accepted for something else and re-pointed at the
    requirement after its code landed would bring an order it never had, and
    re-pointing a design row is the same move one tier down; a re-pointing is
    accepted at the act that re-accepts it. A requirement's own acceptance is
    read the same way, from the record's copy of the requirement registry.

WHEN A ROW WAS ACCEPTED IS READ WHERE IT WAS RECORDED (PROCESS.md §3), never
recomputed by replaying the registries. Acceptance happens only in an act, and
each act appends its entry to the act ledger in its own commit, beside the
registry copies it wrote (IF-220). So the commits that wrote the record are
walked (`baseline_snapshot`'s ledger walk, over the ledger and the copies), and
each one's copies are read against its parents' through `acceptance_record`'s
row reader and acceptance-act rule, never counted: an act that accepts one test
case while withdrawing another leaves the number of accepted rows unchanged,
and a count would see nothing happen. An act made on a side branch reaches
trunk at the first first-parent commit that contains it, and is ordered there,
as a landing is; the report names the act's own commit. Test-case acceptances
are read over the whole record, never from the declared start: SR-217 scopes
only the requirement's acceptance, so a test case accepted after the code
landed stays late even when both happened before the start.

A requirement is judged when its own first acceptance falls after the declared
start and its implementation has landed. Its test cases are those whose
`Verifies` names it or one of its design rows at the tip; WHEN each became its
accepted test case is read from the record as above. Each one accepted for it
after the landing is reported, naming the requirement, the implementation
commit and the acceptance commit. Each one that does not read accepted at the
tip, or that no act has yet accepted while it names the requirement, is
reported by name: whatever its run says, it says it against text nobody has
accepted. Every test case the report names carries the warning that its result
may not reflect the intended behaviour, since that is what the order is
evidence of. Nothing here stops a test from running. A requirement whose
implementation has not landed is not judged yet. No cell is ever read for WHEN
anything happened.

AN ACCEPTANCE WITHOUT AN EXACT DATE. The record's first commit at its current
path is its CUT. Nothing before it is read, in whatever spelling the record had
then (D3: no compatibility readers; formats in git history are cut cleanly),
and each acceptance its copies carry was made AT OR BEFORE it, while its act
ledger records an act: a first copy cannot tell an acceptance it made from
one it found. With no ledger at the cut, an empty one or a malformed one, no
act stands behind the copies, and what they carry is unread. In this
repository the cut is the vocabulary move, which reached trunk at the
declared start. A row
moved into `Accepted` from a word outside the closed status vocabulary (a
rename, not the act) was likewise accepted at or before its act. Such a date
still settles the order when it falls at or before the landing (for a
requirement's own acceptance, at or before the start); when it falls after,
the order cannot be read, and the requirement is reported as unread, never
passed.

A CHANGE NO ACT MADE. A commit after the cut that changes the record's copies,
flipping a row into acceptance or bringing a new accepted pair, without adding
a ledger entry is a gap, and so is one whose ledger, or its parent's, is
malformed. What it carries is unread: never a pass, and never dated at a later
act. So is a row reading accepted at the tip that no act in the record
accepted, as with no ledger or an empty one.

THE DECLARED START is `[checks] test_first_since` in `docs/process.toml`: a
commit id. A project that adopts the rule declares where its judgement begins,
so requirements accepted in history written before the rule are not judged
against it. The shipped template declares the key empty, and an empty or
absent key judges the whole history.

UNREADABLE IS NEVER A PASS. A shallow clone (whose window may leave out an
act's commit), a declared start that names no commit or never stood on trunk's
first-parent line, a declared start before the TOML registries, and registries
still under an older carrier are each reported as unreadable, and nothing is
judged. A rewrite that keeps the start on trunk is read as the history it now
is.

WARN-ONLY IN THE SHIPPED WIRING. The harness's `test-first` step runs this at
every rung without `--strict`, so a finding is reported and never refuses a
commit: the order is evidence a reviewer weighs, and promoting it to a gate is a
project's own ruling. `--strict` makes that ruling for one run.

Component: CMP-007

Contracts: IF-198 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-198: the test-first verdict the harness reads back from the
    `test-first` step. Each requirement with a test case accepted for it after
    its implementation landed, or not accepted, prints one WARN line naming the
    requirement, the implementation commit, every late acceptance commit and
    every test case not accepted, with the warning that their results may not
    reflect the intended behaviour, and one summary line follows; a history with none prints one OK line. An unreadable history, and
    a declared start that cannot be read, each print one WARN line saying the
    order was not judged and that this is not a pass. A requirement whose
    order rests on an acceptance with no exact date is named on its WARN line as
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
import baseline_snapshot
import gen_arch_map
import spine_carrier
from kitlib.config import process_check_text, utf8_console
from kitlib.git import git_out
from kitlib.spine import STATUS_VALUES, is_accepted, is_founded, llr_tree, refs

START_KEY = "test_first_since"

# The registries, from the acceptance-act readers' own table so a path has one
# home; the history is judged over the requirement and test-case tiers, and the
# design tier joins a requirement to the code lines that name its design rows
# and to the test cases that reach it through them.
_REGISTRY = {col: path for path, col in acceptance_record.SPINE_CSVS}
REQUIREMENTS = (_REGISTRY["SR-ID"], "SR-ID")
DESIGN_ROWS = (_REGISTRY["LLR-ID"], "LLR-ID")
TEST_CASES = (_REGISTRY["TC-ID"], "TC-ID")
# Every registry the order is read from, so each is held to the TOML history.
READ = (REQUIREMENTS, DESIGN_ROWS, TEST_CASES)

# `late` is ((test case id, acceptance commit), ...) in trunk order; `unread` is
# ((row id, Acceptance), ...) for each acceptance with no exact date whose order
# is unknown; `unaccepted` is (test case id, ...) for each that does not read
# accepted, or that no act has accepted for the requirement.
Finding = namedtuple("Finding", "requirement implementation late unread unaccepted")

# A row's first acceptance: the record commit, and whether it is the act itself
# (True) or only a commit the row was accepted at or before (False). `unread`
# says why no act in the record can date it at all; `commit` is then the record
# change that carried it, or None when the record never held it accepted.
Acceptance = namedtuple("Acceptance", "commit exact unread", defaults=(None,))

# Why an acceptance is unread (`Acceptance.unread`).
NO_ACT = "a change to the acceptance record that no act made"
LEDGER_UNREADABLE = "a change whose act ledger cannot be read"
UNRECORDED = "no act on record accepted it"

# What the acceptance record says. `requirements`, `tests` and `pairs` map a
# requirement, a test case, or a (test case, requirement) pair to its first
# `Acceptance`; `places` puts each record commit on trunk's first-parent line;
# `cuts` and `gaps` are the record commits read as the cut and as a change no
# act made (the completeness check's findings).
Record = namedtuple("Record", "requirements tests pairs places cuts gaps")

# The record's files the walk reads, at its current path: the act ledger and
# the copies of the read registries, under either carrier.
_SNAPSHOT = baseline_snapshot.SNAPSHOT_DIR
_LEDGER = "{}/{}".format(_SNAPSHOT, baseline_snapshot.ACTS)
_COPIES = tuple(
    "{}/{}".format(_SNAPSHOT, c)
    for path, _col in READ
    for c in spine_carrier.carriers(path)
)
_EMPTY = {path: {} for path, _col in READ}

# A flip from one of these words is the acceptance act; from any other, a rename.
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
    an acceptance or a landing sits on; a start that names no commit, or one that
    never stood on trunk's first-parent line, gives nothing to order after; and
    registries under the older carrier were written in an older status
    vocabulary, so a first acceptance read across them would date the rename
    rather than the act. That excludes registries still under the older carrier
    at `rev`, and a declared start before the TOML registries; with no start,
    the history before the cutover is simply not read, and an acceptance the
    record's cut carries has no exact date (`record_acceptances`). The design registry is
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
            "status vocabulary cannot date an acceptance; move them to "
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


def _record_first(first, registry, befores, after, at):
    """Record in `first` each row's first acceptance act into `after` from
    every one of `befores` (a merge brings nothing its branch already dated),
    at `at`: exact only when `at` is and the act is a birth or a flip from a
    word of the closed status vocabulary (anything else is a rename). The
    number of acts found, recorded first or not."""
    acts = None
    for before in befores:
        found = {
            act["id"]: act
            for act in acceptance_record.acceptance_acts_between(
                registry, before, after
            )
        }
        acts = found if acts is None else {k: v for k, v in acts.items() if k in found}
    for rid, act in (acts or {}).items():
        if rid not in first:
            exact = at.exact and (
                act["act"] == "born" or act["before"].lower() in _VOCABULARY
            )
            first[rid] = at._replace(exact=exact)
    return len(acts or {})


def _associations(tests, design):
    """`{(test case id, requirement id): test-case row}` for every test case
    and each requirement it names, directly or through a design row below it
    in that commit's requirement tree (`SR-Refs` on a top-level row, a child's
    read up its parent chain). An id no design row carries stands for itself,
    so a requirement named directly is its own key.

    Implements: SR-217, LLR-257"""
    srs_of = llr_tree(design.values()).srs_of
    owners = {lid: srs_of.get(lid, []) for lid in design}
    return {
        (tid, rid): row
        for tid, row in tests.items()
        for vid in refs(row.get("Verifies"))
        for rid in owners.get(vid, [vid])
    }


def _record_at(root, rev, cache):
    """`{registry path: rows}`: the record's copies of the read registries at
    `rev`, through either carrier, or None when that tree holds neither the act
    ledger nor any of those copies at the record's current path."""
    if rev not in cache:
        listed = git_out(
            root, ["ls-tree", "-r", "--name-only", rev, "--", _LEDGER, *_COPIES]
        )
        cache[rev] = (
            {
                path: acceptance_record.rows_at(root, rev, _SNAPSHOT + "/" + path, col)
                for path, col in READ
            }
            if (listed or "").strip()
            else None
        )
    return cache[rev]


def _placed(root, sha, line, index):
    """The position on trunk's first-parent `line` (oldest first; `index` maps
    it) of the first commit there that contains `sha`: where a commit made on
    a side branch reached trunk, as a landing is dated at the merge that
    brings it. Ancestry only grows along the line, so it is a binary search."""
    if sha in index:
        return index[sha]
    lo, hi = 0, len(line) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if git_out(root, ["merge-base", "--is-ancestor", sha, line[mid]]) is None:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _cut_ledger_unread(root, sha):
    """Why the cut at `sha` cannot vouch for what its copies carry, or None
    when its act ledger records an act: with no ledger, an empty one or a
    malformed one, no act stands behind the copies (the Trust ruling)."""
    text = git_out(root, ["show", "{}:{}".format(sha, _LEDGER)])
    try:
        acts = baseline_snapshot.parse_acts(text)
    except baseline_snapshot.ActLedgerError:
        return LEDGER_UNREADABLE
    return None if acts else UNRECORDED


def _what_commit(root, sha, befores):
    """`(kind, at)` for one record commit, `befores` being its parents' record
    (None for a parent without one): the CUT when no parent holds the record,
    whose copies carry acceptances made at or before it while its ledger
    records an act, and unread acceptances when it holds no ledger, an empty
    one or a malformed one (`_cut_ledger_unread`); an ACT when it added a
    ledger entry, which dates what it carries exactly; otherwise a GAP, a
    change no act made, and a malformed ledger at it or its parent reads the
    same way, since which acts it added cannot be read."""
    if all(b is None for b in befores):
        return "cut", Acceptance(sha, False, _cut_ledger_unread(root, sha))
    try:
        added = baseline_snapshot._acts_at(root, sha)
    except baseline_snapshot.ActLedgerError:
        return "gap", Acceptance(sha, False, LEDGER_UNREADABLE)
    if added:
        return "act", Acceptance(sha, True)
    return "gap", Acceptance(sha, False, NO_ACT)


def _carried(first, befores, after, at):
    """Record what one record commit carries into `first` (`requirements`,
    `tests`, `pairs`); the number of acceptance acts it carries."""
    sides = [b or _EMPTY for b in befores]
    after = after or _EMPTY
    tc, llr, sr = TEST_CASES[0], DESIGN_ROWS[0], REQUIREMENTS[0]
    moved = _record_first(first.requirements, sr, [b[sr] for b in sides], after[sr], at)
    moved += _record_first(first.tests, tc, [b[tc] for b in sides], after[tc], at)
    return moved + _record_first(
        first.pairs,
        tc,
        [_associations(b[tc], b[llr]) for b in sides],
        _associations(after[tc], after[llr]),
        at,
    )


def record_acceptances(root, rev="HEAD", line=None):
    """`Record`: when each requirement, each test case and each pair of a test
    case and a requirement it names was first accepted, as the acceptance
    record says, at the commits ending at `rev`. `line` is trunk's first-parent
    line, oldest first, when the caller has it.

    The commits that wrote the record (`baseline_snapshot._ledger_commits`, the
    act ledger's one walk, given the copies of the read registries too) are
    read oldest first in trunk order, each one's copies against its parents'
    (`_what_commit`, `_carried`). Each is placed on trunk where it arrived
    (`_placed`). A pair is new at the act whose copy first holds the test case
    accepted while it names the requirement, directly or through a design row
    whose `SR-Refs` name it in that same copy, so a re-pointing is dated at
    the act that re-accepts it. The cut dates what it carries at or before
    itself while its ledger records an act, and nothing before it is read; a
    cut whose ledger records none, and a gap, leave what they carry unread,
    and a later act never re-dates a row or pair already recorded.

    Implements: SR-217, LLR-257
    """
    shas, _shallow = baseline_snapshot._ledger_commits(root, also=_COPIES, rev=rev)
    if shas is None:
        raise HistoryUnreadable("git could not list the commits that wrote the record")
    line = _first_parent(root, rev) if line is None else line
    index = {sha: i for i, sha in enumerate(line)}
    places = {sha: _placed(root, sha, line, index) for sha in shas}
    record = Record({}, {}, {}, places, [], [])
    cache = {}
    # Trunk order; within one arrival, the walk's own order reversed.
    for sha in sorted(reversed(shas), key=places.__getitem__):
        parents = (git_out(root, ["rev-parse", sha + "^@"]) or "").split()
        befores = [_record_at(root, p, cache) for p in parents] or [None]
        kind, at = _what_commit(root, sha, befores)
        moved = _carried(record, befores, _record_at(root, sha, cache), at)
        if kind == "cut":
            record.cuts.append(sha)
        elif kind == "gap" and moved:
            record.gaps.append(sha)
    return record


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
    start: a requirement accepted after the start can still have code that
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


# What the tip holds: design rows by requirement, test cases by verified id,
# the test cases reading accepted, the requirements reading accepted, and every
# (test case, requirement) pair the tip's rows name.
Tip = namedtuple("Tip", "design tests standing requirements pairs")


def _members(root, rev):
    """The `Tip` at `rev`: who belongs to a requirement's chain, and who reads
    accepted there. It says who, never when."""
    design_rows = acceptance_record.rows_at(root, rev, *DESIGN_ROWS)
    test_rows = acceptance_record.rows_at(root, rev, *TEST_CASES)
    tip = Tip({}, {}, set(), set(), set(_associations(test_rows, design_rows)))
    srs_of = llr_tree(design_rows.values()).srs_of
    for lid in design_rows:
        for sr in srs_of.get(lid, ()):
            tip.design.setdefault(sr, []).append(lid)
    for tid, row in test_rows.items():
        for vid in refs(row.get("Verifies")):
            tip.tests.setdefault(vid, []).append(tid)
        if is_accepted(row) or is_founded(row):
            tip.standing.add(tid)
    for sid, row in acceptance_record.rows_at(root, rev, *REQUIREMENTS).items():
        if is_accepted(row) or is_founded(row):
            tip.requirements.add(sid)
    return tip


def _dated(record, tip):
    """`(requirements, pairs)`: each requirement's first acceptance, and each
    first acceptance of a (test case, requirement) pair whose test case reads
    accepted at the tip. A requirement reading accepted at the tip that no act
    in the record accepted is unread. So is a tip pair whose test case the
    record never held accepted at all (no ledger, or an empty one); one the
    record holds accepted only while it named something else gets no date,
    since no act has yet accepted it for this requirement."""
    requirements = dict(record.requirements)
    for sr in tip.requirements - set(requirements):
        requirements[sr] = Acceptance(None, False, UNRECORDED)
    pairs = {pair: at for pair, at in record.pairs.items() if pair[0] in tip.standing}
    for pair in tip.pairs:
        if pair[0] in tip.standing and pair[0] not in record.tests:
            pairs.setdefault(pair, Acceptance(None, False, UNRECORDED))
    return requirements, pairs


def test_first_findings(root, src="src", start=None, rev="HEAD"):
    """One `Finding` per requirement first accepted after `start` whose
    implementation first landed on trunk before one of its test cases was
    accepted for it, or with one of them not accepted — the requirement, the
    implementation commit, each late test case with its acceptance commit in
    trunk order, and each test case not accepted — or whose order cannot be
    read.

    Raises `HistoryUnreadable` for any history `history_unreadable` names, so
    an unreadable history can never come back as an empty, passing list. A
    test case accepted at the same commit the implementation landed is not
    after it. The start scopes only which requirements are judged: test-case
    acceptances are read over the whole record, so one accepted after the
    landing is late wherever the start sits. A requirement's test cases are its
    chain's members at the tip; a test case not reading accepted there has no
    acceptance for it, whatever its history, and each one that does is dated
    at the first act that accepted it while it named the requirement
    (`record_acceptances`; see the module docstring).

    Implements: SR-217, LLR-257
    """
    reason = history_unreadable(root, start, rev)
    if reason:
        raise HistoryUnreadable(reason)
    line = _first_parent(root, rev)
    order = {sha: i for i, sha in enumerate(line)}
    record = record_acceptances(root, rev, line)
    order.update(record.places)
    landed = first_implementation_commits(root, src, rev)
    tip = _members(root, rev)
    accepted, tc_accepted = _dated(record, tip)
    since = order[_commit(root, start)] if start else -1
    out = []
    for sr in sorted(accepted, key=_id_key):
        own = accepted[sr]
        if own.unread is None and order[own.commit] <= since:
            continue  # accepted at or before the start: not in scope
        chain = [sr, *tip.design.get(sr, [])]
        judged = _judged(chain, landed, tip.tests, tc_accepted, order)
        if judged is None:
            continue
        landing, late, unread, unaccepted = judged
        if start and not own.exact:
            # Accepted at or before a commit after the start, or on no date
            # at all: whether it entered scope cannot be read.
            late, unread, unaccepted = (), ((sr, own),), ()
        if late or unread or unaccepted:
            out.append(Finding(sr, landing, late, unread, unaccepted))
    return out


def _judged(chain, landed, tests, acceptances, order):
    """`(landing, late, unread, unaccepted)` for one requirement's chain — the
    requirement first, then its design rows: the earliest landing among them;
    each test case of the chain accepted for the requirement strictly after
    it, as `(test case, commit)`; each whose acceptance has no exact date and
    falls after it, or has no date at all, whose order cannot be read, as
    `(test case, Acceptance)`; and each with no acceptance for the requirement
    in `acceptances`, keyed `(test case, requirement)`. Both lists are in
    trunk order. None when nothing in the chain has landed, which is not
    judged yet."""
    landings = [landed[i] for i in chain if i in landed]
    if not landings:
        return None
    landing = min(landings, key=order.__getitem__)
    members = {tid for i in chain for tid in tests.get(i, [])}
    dated = {
        t: acceptances[(t, chain[0])] for t in members if (t, chain[0]) in acceptances
    }

    def placed(item):
        return (order.get(item[1], len(order)), _id_key(item[0]))

    late = [(t, a.commit) for t, a in dated.items() if a.exact]
    unread = [(t, a) for t, a in dated.items() if not a.exact]
    late = [p for p in late if order[p[1]] > order[landing]]
    unread = [(t, a) for t, a in unread if a.unread or order[a.commit] > order[landing]]
    unaccepted = tuple(sorted(members - set(dated), key=_id_key))
    return (
        landing,
        tuple(sorted(late, key=placed)),
        tuple(sorted(unread, key=lambda p: placed((p[0], p[1].commit)))),
        unaccepted,
    )


def _report(findings, since, level):
    """The printed report's lines for a readable history."""
    lines = ["test-first: {} - {}".format(level, _finding_text(f)) for f in findings]
    if findings:
        lines.append(
            "test-first: {} requirement(s) accepted since {} had a test case "
            "accepted after the implementation landed or not accepted, or an "
            "order that cannot be read".format(len(findings), since)
        )
    else:
        lines.append(
            "test-first: OK - no requirement accepted since {} has a test case "
            "accepted after its implementation landed or not accepted".format(since)
        )
    return lines


def _unread_text(rid, at):
    """One unread acceptance, as its report line names it."""
    if at.unread is None:
        return "{} at or before {}".format(rid, at.commit[:10])
    if at.commit is None:
        return "{} ({})".format(rid, at.unread)
    return "{} ({}, {})".format(rid, at.unread, at.commit[:10])


def _finding_text(f):
    """One finding as the words of its one report line."""
    landed = "{} landed at {} (its first declaring line)".format(
        f.requirement, f.implementation[:10]
    )
    parts = []
    if f.late:
        parts.append(
            "{} test case(s) were accepted after it: {}".format(
                len(f.late),
                ", ".join("{} at {}".format(tid, sha[:10]) for tid, sha in f.late),
            )
        )
    if f.unaccepted:
        parts.append(
            "{} test case(s) are not accepted: {}".format(
                len(f.unaccepted), ", ".join(f.unaccepted)
            )
        )
    if f.late or f.unaccepted:
        parts.append(
            "a result from those test cases may not reflect the intended behaviour"
        )
    if f.unread:
        parts.append(
            "the order against {} cannot be read, since no act dates it exactly".format(
                ", ".join(_unread_text(rid, at) for rid, at in f.unread)
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
