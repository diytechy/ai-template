"""The expected-failure marker: the strict mark that proves a test failed
before its code existed, as `docs/stack.ini` `[product]
expected_failure_marker` declares it, and the two checks `integrate.py record-checks`
and its refresh make of it (WI-996). It is read beside the commit checks'
command, the other value a passed-checks record needs.

WHY THIS EXISTS. A lane's tests-first commit lands each new test under the
declared marker, and its record of passing commit checks is that test's
failing-first proof: a strictly marked test the checks run passes them only by
failing at an assertion. The code commit removes the marker. So a marker may
be added only where the round's test set will run it, removed only against the
lane's last commit record over the same test set, and never landed: a marked
test passes the landing checks while it is failing. One home holds the
declaration's states, the count and the per-file table, so the two verbs that
ask cannot disagree.

WHERE THE TWO VALUES ARE DECLARED, each read from the tree the verb runs on.
The marker is `[product] expected_failure_marker` in `docs/stack.ini`, a fact
about the test framework. The commit checks are named, not spelled:
`docs/process.toml` `[required-checks] commit` names a check suite, and
`docs/stack.ini` `[check-suites]` holds that suite's shell line, so the policy
file says which suite a commit must pass and the stack file says how this
stack runs it. There is no default and no fallback key: a `[bars]` section,
the retired home of both, is named in the refusal and never read.

A count is the number of non-overlapping occurrences of the declared text in a
file's bytes, ASCII whitespace removed from both, so a formatter-wrapped
marker counts and no file is ever decoded. The trees are read by object id
from git, never from a worktree, so an ignored file or a stale cache is never
counted. Every unread tree or range refuses, naming the read: an unread delta
is not an empty one. Nothing here writes a ref or the index (`git write-tree`
only adds the object naming what is staged).
"""

import tomllib
from pathlib import Path
from typing import NamedTuple

from . import config as kconfig
from . import git as kgit
from . import spine as kspine
from . import verdict as kverdict

__all__ = [
    "CommitCheckSettings",
    "read_commit_check_settings",
    "count",
    "tree_counts",
    "findings",
    "record_checks_refusal",
    "landing_refusal",
]

DECLARATION = "docs/stack.ini"
POLICY = "docs/process.toml"
# Where each value is declared, as a refusal names it.
MARKER = ("product", "expected_failure_marker")
REQUIRED = ("required-checks", "commit")
SUITES = "check-suites"
# The section both values lived in before they were renamed and moved, and
# the key each had there. Never read; named when it is still declared.
RETIRED = "bars"
# ASCII whitespace, removed from the file and the declared text alike.
_ASCII_WS = b" \t\n\r\x0b\x0c"
_MARKER_MEANS = (
    "the text of the strict expected-failure marker, as the shipped template's "
    "comment states it"
)
_SUITE_MEANS = "the shell line of the check suite {} [{}] {} names".format(
    POLICY, *REQUIRED
)


class CommitCheckSettings(NamedTuple):
    """What a passed-checks record needs from the lane at `lane`: `commit_checks`, the
    shell line of the check suite a commit must pass; `marker`, the declared
    expected-failure marker; the tests root's path prefix; and, per value that
    is undeclared (`""`), the line naming where it belongs and why it is not
    there.

    Implements: SR-156, LLR-368
    """

    lane: str
    commit_checks: str
    marker: str
    tests_prefix: str
    causes: dict

    def refusal(self, *keys):
        """The refusal naming each of `keys` that is undeclared, with its
        cause, or None when all of them are declared.

        Implements: SR-156, LLR-368
        """
        named = [self.causes[key] for key in keys if key in self.causes]
        if not named:
            return None
        return "undeclared in {}, each required with no default: {}".format(
            self.lane, "; ".join(named)
        )


def _cause(profile, section, key):
    """Why `[section] key` is undeclared in the parsed `profile`, or None.

    Implements: SR-156, LLR-368
    """
    if not profile.has_section(section):
        return "the section is absent"
    if not profile.has_option(section, key):
        return "the key is absent"
    if not profile.get(section, key).strip():
        return "the value is empty"
    return None


def _moved(profile, old):
    """The note that the retired `[bars]` section still declares a value under
    its old key `old`, or `""`. A re-synced repository reads why its
    declaration stopped counting in the refusal itself.

    Implements: SR-156, LLR-368
    """
    if profile is None or not profile.has_option(RETIRED, old):
        return ""
    return "; the retired [{}] {} still declares it and is no longer read".format(
        RETIRED, old
    )


def _required_suite(lane):
    """`(name, None)` for the check suite `docs/process.toml`
    `[required-checks] commit` names in `lane`, or `(None, cause)`.

    Implements: SR-156, LLR-368
    """
    try:
        text = (Path(lane) / POLICY).read_text(encoding="utf-8-sig")
        data = tomllib.loads(text)
    except FileNotFoundError:
        return None, "the file is absent"
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        return None, "the file does not parse ({})".format(exc)
    table = data.get(REQUIRED[0])
    if not isinstance(table, dict):
        return None, "the table is absent"
    if REQUIRED[1] not in table:
        return None, "the key is absent"
    name = table[REQUIRED[1]]
    if not isinstance(name, str) or not name.strip():
        return None, "the value is not a suite's name"
    return name.strip(), None


def _at(path, section, key, cause, means):
    """One undeclared value's line: where it belongs, why it is not there and
    what to declare.

    Implements: SR-156, LLR-368
    """
    return "{} [{}] {} - {} (declare {})".format(path, section, key, cause, means)


def read_commit_check_settings(lane):
    """The commit checks' shell line and the expected-failure marker, with the
    tests root, as the lane at `lane` declares them, as a `CommitCheckSettings`: the marker
    from `[product] expected_failure_marker` and the suite's line from
    `[check-suites]`, both through the one parse of `lane`'s `docs/stack.ini`,
    and the suite's name from `docs/process.toml` `[required-checks] commit`.
    An absent file, one that does not parse, an absent section, table or key,
    or a value empty after stripping is undeclared, and its line is kept for
    `CommitCheckSettings.refusal`.

    Implements: SR-156, LLR-368
    """
    try:
        profile = kconfig.read_stack_ini(Path(lane) / DECLARATION)
    except kconfig.StackIniError as exc:
        profile, unread = None, "the file does not parse ({})".format(exc)
    else:
        unread = "the file is absent"
    causes = {}
    name, why = _required_suite(lane)
    if name is None:
        why += _moved(profile, "review")
        means = "the name of the check suite a commit must pass"
        causes["commit_checks"] = _at(POLICY, *REQUIRED, why, means)
    if profile is None:
        if name:
            causes["commit_checks"] = _at(
                DECLARATION, SUITES, name, unread, _SUITE_MEANS
            )
        causes["marker"] = _at(DECLARATION, *MARKER, unread, _MARKER_MEANS)
        return CommitCheckSettings(str(lane), "", "", "", causes)
    marker_cause = _cause(profile, *MARKER)
    if marker_cause:
        why = marker_cause + _moved(profile, "red_mark")
        causes["marker"] = _at(DECLARATION, *MARKER, why, _MARKER_MEANS)
    suite_cause = _cause(profile, SUITES, name) if name else None
    if suite_cause:
        why = suite_cause + _moved(profile, "review")
        causes["commit_checks"] = _at(DECLARATION, SUITES, name, why, _SUITE_MEANS)
    commit_checks = (
        "" if "commit_checks" in causes else profile.get(SUITES, name).strip()
    )
    marker = "" if marker_cause else profile.get(*MARKER).strip()
    prefix = kspine.root_prefix(kspine.declared_roots(profile)[1])
    return CommitCheckSettings(str(lane), commit_checks, marker, prefix, causes)


def count(data, mark):
    """The non-overlapping occurrences of the text `mark` in the bytes `data`,
    ASCII whitespace removed from both. `mark` is a declared value, so it is
    non-empty after stripping and its needle is never empty.

    Implements: SR-156, LLR-368
    """
    needle = mark.encode("utf-8").translate(None, _ASCII_WS)
    return data.translate(None, _ASCII_WS).count(needle)


def tree_counts(root, tree, prefix, mark):
    """`{path: count}` for every test file under the tests root `prefix` in
    the tree-ish `tree`, zeros included, so a present file with no mark
    differs from an absent one. A test file is what the review set reads as
    one (`kspine.is_test_file`, relative to the root), so the declaration
    holding the mark's text, or a document quoting it, is never counted, even
    under a root of `.`. A link or a submodule is not a file. Raises
    `kgit.ArchiveError` when git cannot list or read the tree.

    Implements: SR-156, LLR-368
    """
    blobs = kgit.read_blobs(root, tree, [prefix] if prefix else [])
    return {
        path: count(data, mark)
        for path, data in blobs.items()
        if kspine.is_test_file(path[len(prefix) :])
    }


def _removal_failures(path, named, tests, digest):
    """Each condition a mark removal from `path` fails, in the table's order.

    Implements: SR-156, LLR-368
    """
    failed = []
    if digest is None:
        failed.append("no commit record stands for the marked tree")
    elif digest != kverdict.tests_digest(tests):
        failed.append("the record is for another test set")
    if path not in named:
        failed.append("the round's test set does not name it")
    return failed


def findings(before, after, tests, digest):
    """The table, one finding per refused file: each test file's count at the
    reference (`before`) against the staged tree (`after`), for the round's
    test set `tests` and the reference record's tests digest (`digest`, None
    when the reference carries no record). An equal count, or a file gone
    from the staged tree, is not judged; a raised count needs the set to name
    the file; a lowered one needs a record over the same set and the set to
    name it. A node id or a directory names no file.

    Implements: SR-156, LLR-368
    """
    named = kverdict.normal_test_paths(tests)
    found = []
    for path in sorted(after):
        m0, m1 = before.get(path, 0), after[path]
        if m1 > m0 and path not in named:
            failed = [
                "markers added, but the round's test set does not name it, so "
                "the commit checks would not run its marked tests and their "
                "failing first is unproven"
            ]
        elif m1 < m0:
            failed = _removal_failures(path, named, tests, digest)
        else:
            failed = []
        if failed:
            found.append("{} ({} -> {}): {}".format(path, m0, m1, "; ".join(failed)))
    return found


def _staged_tree(wt):
    """The tree `wt`'s index stages, or None when git cannot write it.

    Implements: SR-156, LLR-368
    """
    tree = kgit.git_out(wt, ["write-tree"])
    return tree.strip() if tree and tree.strip() else None


def _read_counts(root, tree, settings, what):
    """`(counts, None)` for `tree`, or `(None, refusal)` naming `what` as the
    read that failed.

    Implements: SR-156, LLR-368
    """
    if tree is None:
        return None, "cannot read the {}: git could not name it".format(what)
    try:
        return tree_counts(root, tree, settings.tests_prefix, settings.marker), None
    except kgit.ArchiveError as exc:
        return None, "cannot read the {} ({})".format(what, exc)


def _refusal(lead, found):
    """`lead`, then one indented line per refused file.

    Implements: SR-156, LLR-368
    """
    return "{} ({} [{}] {}):\n{}".format(
        lead, DECLARATION, *MARKER, "\n".join("  " + line for line in found)
    )


def record_checks_refusal(root, wt, branch, base, settings, tests):
    """Why `record-checks` may not record the tree `wt` stages, by the table, or
    None. The reference is the newest verified commit record in
    `base..branch`, else `base` with no record; `tests` is the round's test
    set. An unreadable range, reference tree or staged tree refuses, naming
    the read. Raises nothing, and moves neither the branch nor the index.

    Implements: SR-156, LLR-368
    """
    record = kverdict.last_commit_record(root, branch, base)
    if record is None:
        return (
            "cannot read the range {}..{}, so the lane's last commit record is "
            "unknowable".format(base[:10], branch)
        )
    sha, passed = record
    after, refusal = _read_counts(wt, _staged_tree(wt), settings, "staged tree")
    if refusal:
        return refusal
    reference = passed.tree if passed else base + "^{tree}"
    before, refusal = _read_counts(root, reference, settings, "reference tree")
    if refusal:
        return refusal
    found = findings(before, after, tests, passed.tests if passed else None)
    if not found:
        return None
    where = (
        "the lane's last commit record {}".format(sha[:10])
        if passed
        else "the lane base {}, which carries no commit record".format(base[:10])
    )
    return _refusal(
        "a test file's count of the declared expected-failure marker changed "
        "against {}, and "
        "the change is not proven".format(where),
        found,
    )


def landing_refusal(wt):
    """Why the tree `wt` stages may not land, or None: the expected-failure
    marker is undeclared there, the tree cannot be read, or a file under its
    tests root holds the marker, each named with its count. The way out is
    the code commit that removes the markers, or a quarantine.

    Implements: SR-156, LLR-368
    """
    settings = read_commit_check_settings(wt)
    refusal = settings.refusal("marker")
    if refusal:
        return refusal
    counts, refusal = _read_counts(wt, _staged_tree(wt), settings, "staged tree")
    if refusal:
        return refusal
    marked = ["{}: {} marked".format(p, n) for p, n in sorted(counts.items()) if n]
    if not marked:
        return None
    return _refusal(
        "the tree holds the declared expected-failure marker, and a landing "
        "tree holds none: "
        "remove each in the code commit that turns its tests green, or "
        "quarantine the lane",
        marked,
    )
