#!/usr/bin/env python3
"""review_set.py - a lane's review test set, derived from its row (WI-995).

A review bar's named tests come from the spine, never from whoever asks for the
attestation. The row's SRs reach their LLRs, both reach their test cases, and
the test-file tags reach the files: `derive` reads those inputs from one lane
and `kitlib.spine.review_scope` walks them. `integrate.attest`, the loop's draw
and the review render all call `derive`, so a record, a draw and a brief cannot
disagree about what a row's set is. The answer is the set or one named refusal,
and the set never widens to the whole bar: an empty set runs the review bar
alone, and the floor (`[bars] review`, the landing bar) stays as it is.

WHAT IS READ FROM WHERE. The claim listing and the row's text come from git
(HEAD, the merge base, the index), the changed paths from the index against the
merge base, and the registries, `docs/stack.ini` and the tags from the lane
checkout. `attest` has already refused a worktree that differs from the index,
so there the two agree; at the render and the draw a working-tree edit can only
change the derived list, and the record's digest then refuses it.

Contracts: IF-309 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-309: `derive(lane, branch)` answers `(ReviewSet, None)` or `(None,
    refusal)` and never raises for a bad input: a refusal is a value, opening
    with its kind (`names no SR`, `malformed`, `empty`, `partial`), so the loop
    can route it as a red. `ReviewSet` supplies `files` (the sorted test paths,
    the list a record digests), `listed` (evidence beside the set, never run),
    `gaps` (reported on a row touching no code), `code_touching`, and the
    printed `lines()` and `notes()`. Requestors do not interpret the derivation
    or take a hand list.
"""

import dataclasses
from pathlib import Path

import agent_common
import gen_arch_map
import spine_carrier
from kitlib import config as kconfig
from kitlib import done_when as kdone
from kitlib import git as kgit
from kitlib import registry as kregistry
from kitlib import spine as kspine

REGISTRIES = (
    ("docs/requirements/system-requirements.toml", "SR-ID"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID"),
    ("docs/test/test-cases.toml", "TC-ID"),
)


class _Refused(Exception):
    """One read's refusal, its `str` the whole text; `derive` returns it.

    Implements: SR-241, LLR-367
    """


@dataclasses.dataclass(frozen=True)
class ReviewSet:
    """One row's review test set: what runs, what stands beside it unrun, and
    what a row touching no code reports.

    Implements: SR-241, LLR-367
    """

    files: tuple
    listed: tuple
    gaps: tuple
    code_touching: bool

    def notes(self):
        """The facts beside the files: listed evidence and reported gaps.

        Implements: SR-241, LLR-367
        """
        lines = []
        if self.listed:
            lines.append("listed beside the set, never run:")
            lines += ["  " + item for item in self.listed]
        if self.gaps:
            lines.append("reported gaps (the row touches no code):")
            lines += ["  " + gap for gap in self.gaps]
        return lines

    def lines(self):
        """The set as printed: its files, then `notes`.

        Implements: SR-241, LLR-367
        """
        head = "review set: {} test file(s)".format(len(self.files))
        return [head] + ["  " + path for path in self.files] + self.notes()


def _base(lane):
    """The lane's merge base with the declared trunk.

    Implements: SR-241, LLR-367
    """
    base, why = agent_common.worker_base(lane)
    if why:
        raise _Refused("malformed: {}".format(why))
    return base


def _claimed_id(lane, branch, base):
    """The one work item claimed for `branch`, at HEAD or at the merge base. A
    lane closed in its own tree holds its claim at the base alone.

    Implements: SR-241, LLR-367
    """
    folder = "{}/{}/".format(kgit.ACTIVE_DIR, branch)
    ids = set()
    for rev in ("HEAD", base):
        claims = kgit.claimed_specs(lane, rev, branch)
        if claims is None:
            raise _Refused("malformed: {} cannot be read at {}".format(folder, rev))
        ids.update(wi for _owner, wi, _name in claims)
    if len(ids) != 1:
        found = ", ".join(sorted(ids)) or "none"
        raise _Refused(
            "malformed: {} must hold one claim, found {}".format(folder, found)
        )
    return ids.pop()


def _row_srs(lane, branch, wi):
    """The sorted SR ids of `wi`'s row, read from its closed copy once the lane
    has closed it, else its claim copy; `[]` for a row naming none.

    Implements: SR-241, LLR-367
    """
    path, text, why = kdone.spec_at(lane, None, branch, wi)
    if path is None or why:
        raise _Refused(
            "malformed: {}".format(why or "no copy of {}'s spec is staged".format(wi))
        )
    try:
        data, _body = kregistry.parse_spec_frontmatter(text, path)
    except ValueError as exc:
        raise _Refused("malformed: {}".format(exc)) from None
    srs = data.get("sr_refs", [])
    if not isinstance(srs, list) or not all(isinstance(sr, str) for sr in srs):
        raise _Refused(
            "malformed: {}: sr_refs is not a list of ids ({!r})".format(path, srs)
        )
    return sorted(set(srs))


def _changed(lane, base):
    """The paths changed from the merge base to the staged tree. A rename
    counts at both ends, so a move out of a root still touches it.

    Implements: SR-241, LLR-367
    """
    paths = kgit.git_paths(
        lane, ["diff", "--no-renames", "--name-only", "--cached", base]
    )
    if paths is None:
        raise _Refused("malformed: the changes since {} cannot be read".format(base))
    return paths


def _roots(lane):
    """`(src, tests)` as `docs/stack.ini` `[paths]` declares them, with the
    defaults a bar's command reads.

    Implements: SR-241, LLR-367
    """
    try:
        profile = kconfig.read_stack_ini(Path(lane) / "docs" / "stack.ini")
    except kconfig.StackIniError as exc:
        raise _Refused("malformed: {}".format(exc)) from None
    if profile is None:
        raise _Refused("malformed: docs/stack.ini is absent")
    return (
        profile.get("paths", "src", fallback="").strip() or "src",
        profile.get("paths", "tests", fallback="").strip() or "tests",
    )


def _registry(lane, rel, id_col):
    """The live rows of the registry at `rel`. An absent registry refuses, and
    the carrier's `SystemExit` becomes a refusal, so an unparseable registry
    takes the loop's red route instead of ending it.

    Implements: SR-241, LLR-367
    """
    try:
        live = spine_carrier.resolve(Path(lane) / rel)
        if live is None:
            raise _Refused("malformed: {} is absent".format(rel))
        return spine_carrier.load(live, id_col, keep_examples=False)
    except (SystemExit, OSError) as exc:
        raise _Refused("malformed: {}: {}".format(rel, exc)) from None


def _tags(lane, tests, tcs):
    """`{TC id: node ids}` from the tag reader, any finding refusing with its
    file, line and text.

    Implements: SR-241, LLR-367
    """
    live = {(row.get("TC-ID") or "").strip() for row in tcs}
    tags, findings = gen_arch_map.read_test_tags(lane, tests, live)
    if findings:
        raise _Refused(
            "malformed: the test-file tags refuse:\n"
            + "\n".join(
                "  {}:{}: {}: {}".format(f["file"], f["line"], f["shape"], f["detail"])
                for f in findings
            )
        )
    return tags


def _touches_code(changed, src, tests):
    """Whether any of `changed` sits under the source or tests root.

    Implements: SR-241, LLR-367
    """
    roots = (kspine.root_prefix(src), kspine.root_prefix(tests))
    return any(path.startswith(roots) for path in changed)


def _walk(lane, wi, srs, tests, touches):
    """The set of a row naming `srs`, or the refusal its answer is.

    Implements: SR-241, LLR-367
    """
    sr_rows, llrs, tcs = (_registry(lane, *entry) for entry in REGISTRIES)
    known = {row.get("SR-ID") for row in sr_rows}
    unknown = [sr for sr in srs if sr not in known]
    if unknown:
        raise _Refused(
            "malformed: {} names {}, which the SR registry lacks".format(
                wi, ", ".join(unknown)
            )
        )
    tags = _tags(lane, tests, tcs)
    files, listed, gaps = kspine.review_scope(
        srs, llrs, tcs, tags, tests, lambda path: (Path(lane) / path).exists()
    )
    if touches and gaps:
        raise _Refused(
            "partial: {} gap(s) in {}'s review set:\n{}".format(
                len(gaps), wi, "\n".join("  " + gap for gap in gaps)
            )
        )
    if touches and not files:
        raise _Refused(
            "empty: {} touches code, and its SRs ({}) reach no tagged test file".format(
                wi, ", ".join(srs)
            )
        )
    return ReviewSet(tuple(files), tuple(listed), tuple(gaps), touches)


def _answer(lane, branch):
    """The set, in the order of the reads: the row, its changed paths and the
    roots first, so a row naming no SR is answered before any registry is read;
    then every other input, so an unreadable one outranks partial and empty.

    Implements: SR-241, LLR-367
    """
    base = _base(lane)
    wi = _claimed_id(lane, branch, base)
    srs = _row_srs(lane, branch, wi)
    changed = _changed(lane, base)
    src, tests = _roots(lane)
    touches = _touches_code(changed, src, tests)
    if srs:
        return _walk(lane, wi, srs, tests, touches)
    if touches:
        raise _Refused(
            "names no SR: {} touches code and its sr_refs names no requirement; "
            "amend the row's sr_refs on trunk".format(wi)
        )
    return ReviewSet((), (), (), False)


def derive(lane, branch):
    """`(ReviewSet, None)` for the lane checkout `lane` on `branch`, or `(None,
    refusal)`: the review test set of the row the lane claims.

    A row touching code refuses when it names no SR, when any gap stands
    (`partial`, naming each) and when no tagged file is reached with no gap
    (`empty`). A row touching no code reports its gaps and may be empty. Any
    input that cannot be read refuses as `malformed`, naming it.

    Implements: SR-241, LLR-367

    Contract:
      Inputs:  lane: the lane checkout; branch: the branch it is on
      Outputs: (ReviewSet | None, str | None) — exactly one is None
    """
    try:
        return _answer(Path(lane), branch), None
    except _Refused as exc:
        return None, str(exc)
