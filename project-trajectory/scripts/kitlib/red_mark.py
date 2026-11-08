"""The red mark: the strict expected-failure mark that proves a test's
red-before, as `docs/stack.ini` `[bars] red_mark` declares it, and the two
checks `integrate.py attest` and its refresh make of it (WI-996).

WHY THIS EXISTS. A lane's tests-first commit lands each new test under the
declared mark, and its review attestation's green bar is that test's
red-before: a strictly marked test the bar runs passes it only by failing at
an assertion. The code commit removes the mark. So a mark may be added only
where the round's test set will run it, removed only against the lane's last
review record over the same test set, and never landed: a marked test passes
the landing bar while it is red. One home holds the declaration's states, the
count and the per-file table, so the two verbs that ask cannot disagree.

The declaration is read with `[bars] review` through the one parse of
`docs/stack.ini`, from the tree the verb runs on. There is no default and no
fallback key. A count is the number of non-overlapping occurrences of the
declared text in a file's bytes, ASCII whitespace removed from both, so a
formatter-wrapped mark counts and no file is ever decoded. The trees are read
by object id from git, never from a worktree, so an ignored file or a stale
cache is never counted. Every unread tree or range refuses, naming the read:
an unread delta is not an empty one. Nothing here writes a ref or the index
(`git write-tree` only adds the object naming what is staged).
"""

from pathlib import Path
from typing import NamedTuple

from . import config as kconfig
from . import git as kgit
from . import spine as kspine
from . import verdict as kverdict

__all__ = [
    "Bars",
    "read_bars",
    "count",
    "tree_counts",
    "findings",
    "attest_refusal",
    "landing_refusal",
]

DECLARATION = "docs/stack.ini"
# ASCII whitespace, removed from the file and the declared text alike.
_ASCII_WS = b" \t\n\r\x0b\x0c"
_KEYS = ("review", "red_mark")
# What each key declares, for the refusal that names it undeclared.
_MEANS = {
    "review": "the shell line a review attestation runs",
    "red_mark": "the text of the strict expected-failure mark, as the shipped "
    "template's comment states it",
}


class Bars(NamedTuple):
    """`[bars]` as the lane at `lane` declares it: each key's stripped value
    (`""` when undeclared), the tests root's path prefix and the cause per
    undeclared key.

    Implements: SR-156, LLR-368
    """

    lane: str
    review: str
    red_mark: str
    tests_prefix: str
    causes: dict

    def refusal(self, *keys):
        """The refusal naming each of `keys` that is undeclared, with its
        cause, or None when all of them are declared.

        Implements: SR-156, LLR-368
        """
        named = [key for key in keys if key in self.causes]
        if not named:
            return None
        return "undeclared in {}, each required with no default: {}".format(
            self.lane,
            "; ".join(
                "{} [bars] {} - {} (declare {})".format(
                    DECLARATION, key, self.causes[key], _MEANS[key]
                )
                for key in named
            ),
        )


def _cause(profile, key):
    """Why `[bars] <key>` is undeclared in the parsed `profile`, or None.

    Implements: SR-156, LLR-368
    """
    if not profile.has_section("bars"):
        return "the section is absent"
    if not profile.has_option("bars", key):
        return "the key is absent"
    if not profile.get("bars", key).strip():
        return "the value is empty"
    return None


def read_bars(lane):
    """`[bars] review` and `[bars] red_mark`, with the tests root, from the
    one parse of `lane`'s `docs/stack.ini`, as a `Bars`. An absent file, one
    that does not parse, an absent section or key, or a value empty after
    stripping is undeclared, and its cause is kept for `Bars.refusal`.

    Implements: SR-156, LLR-368
    """
    try:
        profile = kconfig.read_stack_ini(Path(lane) / DECLARATION)
    except kconfig.StackIniError as exc:
        profile, cause = None, "the file does not parse ({})".format(exc)
    else:
        cause = "the file is absent"
    if profile is None:
        return Bars(str(lane), "", "", "", {key: cause for key in _KEYS})
    causes = {key: _cause(profile, key) for key in _KEYS}
    values = [profile.get("bars", key, fallback="").strip() for key in _KEYS]
    prefix = kspine.root_prefix(kspine.declared_roots(profile)[1])
    return Bars(str(lane), *values, prefix, {k: c for k, c in causes.items() if c})


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
        failed.append("no review record stands for the marked tree")
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
                "marks added, but the round's test set does not name it, so the "
                "bar would not run its marked tests and their red is unproven"
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


def _read_counts(root, tree, bars, what):
    """`(counts, None)` for `tree`, or `(None, refusal)` naming `what` as the
    read that failed.

    Implements: SR-156, LLR-368
    """
    if tree is None:
        return None, "cannot read the {}: git could not name it".format(what)
    try:
        return tree_counts(root, tree, bars.tests_prefix, bars.red_mark), None
    except kgit.ArchiveError as exc:
        return None, "cannot read the {} ({})".format(what, exc)


def _refusal(lead, found):
    """`lead`, then one indented line per refused file.

    Implements: SR-156, LLR-368
    """
    return "{} ({} [bars] red_mark):\n{}".format(
        lead, DECLARATION, "\n".join("  " + line for line in found)
    )


def attest_refusal(root, wt, branch, base, bars, tests):
    """Why `attest` may not record the tree `wt` stages, by the table, or
    None. The reference is the newest verified review record in
    `base..branch`, else `base` with no record; `tests` is the round's test
    set. An unreadable range, reference tree or staged tree refuses, naming
    the read. Raises nothing, and moves neither the branch nor the index.

    Implements: SR-156, LLR-368
    """
    record = kverdict.last_review_record(root, branch, base)
    if record is None:
        return (
            "cannot read the range {}..{}, so the lane's last review record is "
            "unknowable".format(base[:10], branch)
        )
    sha, attested = record
    after, refusal = _read_counts(wt, _staged_tree(wt), bars, "staged tree")
    if refusal:
        return refusal
    reference = attested.tree if attested else base + "^{tree}"
    before, refusal = _read_counts(root, reference, bars, "reference tree")
    if refusal:
        return refusal
    found = findings(before, after, tests, attested.tests if attested else None)
    if not found:
        return None
    where = (
        "the lane's last review record {}".format(sha[:10])
        if attested
        else "the lane base {}, which carries no review record".format(base[:10])
    )
    return _refusal(
        "a test file's count of the declared red mark changed against {}, and "
        "the change is not proven".format(where),
        found,
    )


def landing_refusal(wt):
    """Why the tree `wt` stages may not land, or None: the red mark is
    undeclared there, the tree cannot be read, or a file under its tests
    root holds the mark, each named with its count. The way out is the code
    commit that removes the marks, or a quarantine.

    Implements: SR-156, LLR-368
    """
    bars = read_bars(wt)
    refusal = bars.refusal("red_mark")
    if refusal:
        return refusal
    counts, refusal = _read_counts(wt, _staged_tree(wt), bars, "staged tree")
    if refusal:
        return refusal
    marked = ["{}: {} marked".format(p, n) for p, n in sorted(counts.items()) if n]
    if not marked:
        return None
    return _refusal(
        "the tree holds the declared red mark, and a landing tree holds none: "
        "remove each in the code commit that turns its tests green, or "
        "quarantine the lane",
        marked,
    )
