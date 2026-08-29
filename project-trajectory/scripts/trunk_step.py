#!/usr/bin/env python3
"""The serial trunk step — compile the log fragments, regenerate the trunk artifacts.

The one deliberately serial actor of the concurrency model
(`docs/concurrency-restructure.md` §5.5). Work branches never write `docs/log.md`
and never commit a generated artifact; they drop a **fragment** at
`docs/log.d/<WI-id>-<slug>.md` (unique name -> conflict-free by construction),
and this step — run on the trunk, by the coordinator or a post-merge Action —
folds those fragments into the log (§5.1) and re-derives the generated surfaces
(§5.2). Hand-merging the log ends here.

Its three rules, straight from §5.5, are the whole design brief:

    **tiny** — two operations, no state of its own, stdlib only.
    **idempotent** — a second run on a clean trunk is a no-op ("0 fragments",
      every generator already fresh), so re-running is always safe.
    **fails loudly** — ANY problem exits nonzero with the offending file named.
      A red trunk lane halts claiming; it must never fail open (the fail-open
      lesson applied to the new machinery on day one).

It never commits. Staging and committing belong to the caller (the integrator,
the Action, or a human), so this step composes with whatever wraps it.

Compile-log (`--compile-log`)
    Every fragment is validated BEFORE anything is written — all-or-nothing, so a
    half-compiled log can never exist. A fragment must be named
    `<id>-<slug>.md`, must open with a `## ` heading, and must not claim one of
    `docs/log.md`'s three reserved section headings. It must also be COMMITTED:
    this step is trunk bookkeeping over committed state, and an uncommitted
    fragment has no merge position.

    Order is DERIVED, never asserted (§5.1): fragments are appended oldest-first
    by the commit date of the commit that ADDED each file, ties broken by
    filename. That is why git is a hard requirement here rather than a
    best-effort nicety — off git there is no merge order to read, so the step
    refuses instead of inventing one (PROCESS.md declares git a required
    substrate).

    A fragment's own relative links are rebased on the way in: it was written to
    sit in `docs/log.d/`, and it lands in `docs/log.md` one directory up, so
    `](../work/queued/WI-9-x.md)` becomes `](work/queued/WI-9-x.md)`. Anchors,
    URLs and root-absolute paths resolve independently of the holding directory
    and are left exactly as written.

Regen (`--regen`)
    Re-derives the generated artifacts in DEPENDENCY order (see REGEN_STEPS): a
    generator that reads another's output must run after it, or one pass leaves
    the tree stale and the next `check.py` reds the trunk for no real defect. A
    generator whose artifact family this repo does not carry is skipped with a
    printed notice — a non-adopter pays nothing, and the skip is visible rather
    than silent.

Usage:  python scripts/trunk_step.py [--root .] [--compile-log] [--regen] [--dry-run]
        (no operation flag = both, compile first, then regen)
Exit codes: 0 all clean, 1 any failure (the §5.5 loud-block contract).

Contracts: IF-081, IF-155 — the interface seams this module declares (process.md
§8; rows of record in docs/requirements/interfaces.toml).

Contract IF-081: the serial trunk lane's exit alphabet, and there are only two
    letters in it. 0 is all clean — every selected operation finished, or found
    nothing to do, which is the same answer here because a second run on a
    clean trunk is a no-op. 1 is ANY failure, with the offending file named on
    stderr: a fragment that fails validation, an unreadable merge order (off
    git the order cannot be read and is never invented), or a generator that
    returned nonzero and stopped the rest. There is no partial success to
    report — the compile is all-or-nothing and the regen halts at the first
    failure — because a red trunk lane must halt claiming rather than fail
    open. It never commits, so the caller reading this code owns what is left
    staged.
Contract IF-155: the argv surface of the trunk step. `--root` (default the cwd)
    names the repository; `--compile-log` selects the fold and `--regen` the
    re-derivation, and NEITHER flag runs both — compile first, because it can
    move docs/log.md, which the generators then read. `--dry-run` applies to
    whichever operations are selected: each prints what it would do and writes
    nothing. No flag selects a subset of fragments or of generated families,
    and none of them commits.
"""

import argparse
import configparser
import posixpath
import re
import subprocess
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# THE SHIPPED SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`, executed
# WI-448): the best-effort-off-git subprocess pattern this module used to spell
# out itself. Run as a subprocess this script's own dir is sys.path[0] so a
# plain import resolves; the guard covers an in-process import (a test) whose
# sys.path does not yet carry scripts/.
try:
    from kitlib import git as _kitgit
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import git as _kitgit

# Sibling: the registry CARRIER, for the one question this module asks of a
# registry — which carrier is live. Naming `.csv` inline instead would make the
# open-items step SKIP silently on a migrated repo, and a skipped freshness
# step is the shape SN-008 forbids: the generated surface simply stops being
# regenerated and nothing says so.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

_SCRIPTS = Path(__file__).resolve().parent

# The fragment drop-box and its scaffold marker (bootstrap lays down
# `docs/log.d/.gitkeep`, since git does not track an empty directory).
LOG_D = "docs/log.d"

# `docs/log.md`'s three history sections (pinned by tests/test_bootstrap.py). A
# fragment claiming one of them would splice narrative INTO a structural section
# — the log's shape is not a work branch's to redefine.
#
# `## Gate Sign-offs` BECAME `## Sittings` at OI-21 (contract break 6): sittings
# are their own axis under the eight-rung ladder — a project holds fewer sittings
# than it has rungs, so a row names the RUNG RANGE it certifies rather than being
# one-per-boundary. This constant, `LOG.template.md`'s heading and
# tests/test_trunk_step.py move together; an adopter's existing log renames the
# heading at re-sync (the rows underneath stay verbatim — they are attestations).
RESERVED_HEADINGS = ("## Sittings", "## Decisions log", "## Audit log")

# `<id>-<slug>.md`. The `WI-<n>-<slug>` form is the house convention; a bare
# `<token>-<slug>` is accepted too (a repo whose work ids are not `WI-` still
# gets fragments), but a nonempty slug and the `.md` suffix are required — the
# uniqueness that makes fragments conflict-free lives in the slug.
FRAGMENT_NAME_RE = re.compile(
    r"^(?:[A-Za-z][A-Za-z0-9]*-\d+|[A-Za-z0-9]+)-[A-Za-z0-9][A-Za-z0-9._-]*\.md$"
)

# Inline markdown link targets, and the "not a repo-relative path" exclusions.
# Kept LOCAL on purpose: the dispatcher's mirror pair proved these edge cases,
# and this step outlived that module (retired at Phase 5).
MD_LINK_TARGET_RE = re.compile(r"(\]\()([^)\s]+)(\))")
URL_SCHEME_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)


# stdout of a git command under `root`, or None on ANY failure (no git binary,
# not a repo, unknown rev/path, non-zero exit) — the house best-effort-off-git
# pattern. ONE HOME since WI-448 (`kitlib.git`): it was written out three times,
# in check.py, trace.py and trunk_step.py, each docstring pointing at the others
# as though one of them were the original. Kept under its own long-standing
# private name so no call site below moves.
_git_out = _kitgit.git_out
# Callers HERE turn a None into a LOUD error rather than degrading:
# merge order is the one thing this step cannot guess — the
# fail-direction stays with the caller, which is why `kitlib.git`
# deliberately does not decide what an absent answer means.


def _err(message):
    print("trunk_step: " + message, file=sys.stderr)


# --- compile-log --------------------------------------------------------------


def fragment_paths(root):
    """The fragment files awaiting compilation, filename-sorted. Dotfiles are
    skipped so the scaffold marker (`.gitkeep`) is never mistaken for one, and
    so is the directory's own `README.md` — the declaration home of the
    `docs/log.d/` interface row (a directory owner states its contract in its
    README), which is neither a session fragment nor a name the fragment
    grammar could accept. By NAME, exactly, so any other badly named file still
    refuses the whole compile."""
    d = Path(root) / LOG_D
    if not d.is_dir():
        return []
    return sorted(
        (
            p
            for p in d.glob("*.md")
            if p.is_file() and not p.name.startswith(".") and p.name != "README.md"
        ),
        key=lambda p: p.name,
    )


def read_fragment(path):
    """A fragment's text with line endings normalised to `\\n`.

    `newline=""` reads the bytes verbatim; the CRLF collapse happens here so the
    downstream link rewrite and heading checks see one shape, and
    `plan_artifacts.append_log_summary` re-applies `docs/log.md`'s OWN newline
    convention when it appends (a CRLF log stays CRLF)."""
    with path.open("r", encoding="utf-8", newline="") as fh:
        text = fh.read()
    return text.replace("\r\n", "\n").replace("\r", "\n")


def validate_fragment(path, text):
    """The reasons `path` cannot be compiled, as a list of one-line strings (empty
    = valid). Every fragment is run through this before ANY of them is appended,
    which is what makes the compile all-or-nothing."""
    problems = []
    if not FRAGMENT_NAME_RE.match(path.name):
        problems.append("filename is not <id>-<slug>.md (e.g. WI-401-log-fragments.md)")
    first = text.split("\n", 1)[0].strip()
    if not first.startswith("## "):
        problems.append(
            "must open with a `## ` heading line; found: {!r}".format(first)
        )
    elif first in RESERVED_HEADINGS:
        problems.append(
            "claims the reserved log section heading {!r} — pick a fragment "
            "heading of your own".format(first)
        )
    return problems


def added_at(root, path):
    """The commit date (unix seconds) of the commit that ADDED `path`, `None` off
    git, or `""` when no commit added it (uncommitted).

    Merge order is derived from git history rather than asserted (§5.1), so this
    single query answers both "where does it sort?" and "is it committed?" —
    a file that is merely staged has no adding commit and is rejected by the same
    fact that would have ordered it. One deliberate widening: DURING a merge
    composition (MERGE_HEAD set — the integrator folds this step into the merge
    commit, so the branch's history is not yet reachable from HEAD) the query
    retries against MERGE_HEAD, where the fragment's adding commit genuinely
    lives. A fragment with no adding commit on either side is still refused."""
    rel = Path(path).relative_to(root).as_posix()
    out = _git_out(root, ["log", "--diff-filter=A", "--format=%ct", "-1", "--", rel])
    if out is None:
        return None
    out = out.strip()
    if not out:
        merging = _git_out(root, ["rev-parse", "--verify", "--quiet", "MERGE_HEAD"])
        if merging and merging.strip():
            out = _git_out(
                root,
                [
                    "log",
                    "--diff-filter=A",
                    "--format=%ct",
                    "-1",
                    "MERGE_HEAD",
                    "--",
                    rel,
                ],
            )
            out = (out or "").strip()
    return int(out.splitlines()[0]) if out else ""


def ordered_fragments(root, paths):
    """`(ordered, errors)` — the fragments in merge order, or the loud reasons they
    cannot be ordered/compiled. `ordered` is `[(path, text)]` oldest-first, ties
    broken by filename (deterministic within one commit)."""
    errors = []
    keyed = []
    for path in paths:
        rel = Path(path).relative_to(root).as_posix()
        text = read_fragment(path)
        for problem in validate_fragment(path, text):
            errors.append("{}: {}".format(rel, problem))
        stamp = added_at(root, path)
        if stamp is None:
            errors.append(
                "{}: cannot read git history — this step compiles COMMITTED "
                "fragments and derives their order from git (a required "
                "substrate); run it on a git checkout".format(rel)
            )
        elif stamp == "":
            errors.append(
                "{}: uncommitted — a fragment has no merge position until a "
                "commit adds it; commit it (or delete it) and re-run".format(rel)
            )
        else:
            keyed.append((stamp, path.name, path, text))
    if errors:
        return [], errors
    keyed.sort(key=lambda item: (item[0], item[1]))
    return [(path, text) for _, _, path, text in keyed], []


def rebased_link_target(target):
    """The rewritten target for ONE inline link inside a fragment, or None to leave
    it alone: the fragment is authored in `docs/log.d/` and lands in `docs/`.

    Left alone, because each resolves independently of the holding directory: a
    bare `#fragment`, any scheme-ish or protocol-relative URL, and a root-absolute
    `/path`. Everything else is resolved against `docs/log.d` and re-relativised
    against `docs`; a `#fragment` suffix and the link TEXT survive untouched."""
    if target.startswith("#") or target.startswith("/"):
        return None
    if URL_SCHEME_RE.match(target):
        return None
    base, sep, frag = target.partition("#")
    if not base:
        return None
    resolved = posixpath.normpath(posixpath.join(LOG_D, base))
    new = posixpath.relpath(resolved, "docs")
    return None if new == base else new + sep + frag


def rebase_links(text):
    """`text` with every rebasable inline link target moved from log.d-relative to
    docs-relative. Text-in, text-out: the fragment is appended, never rewritten in
    place, so there is no file to keep line-ending discipline over here."""

    def _sub(match):
        new = rebased_link_target(match.group(2))
        return match.group(0) if new is None else match.group(1) + new + match.group(3)

    return MD_LINK_TARGET_RE.sub(_sub, text)


def _plan_artifacts():
    """The sibling module that owns appending to `docs/log.md` (its newline
    detection and blank-line separation are not restated here). Imported lazily,
    the sanctioned sibling-import idiom: `scripts/` is on `sys.path[0]` as a
    subprocess, and the fallback covers an in-process import."""
    try:
        import plan_artifacts
    except ImportError:  # pragma: no cover - exercised via the sys.path fallback
        sys.path.insert(0, str(_SCRIPTS))
        import plan_artifacts
    return plan_artifacts


def compile_log(root, dry_run=False):
    """Fold `docs/log.d/*.md` into `docs/log.md` in merge order and delete them.
    Returns an exit code: 0 clean (including the no-op), 1 with every reason
    printed.

    Implements: SR-173, LLR-137"""
    paths = fragment_paths(root)
    if not paths:
        print("trunk_step: compile-log — 0 fragments; nothing to do.")
        return 0
    ordered, errors = ordered_fragments(root, paths)
    if errors:
        for line in errors:
            _err(line)
        _err(
            "compile-log REFUSED: {} problem(s); docs/log.md is unchanged and "
            "every fragment is still on disk (all-or-nothing).".format(len(errors))
        )
        return 1
    names = [p.name for p, _ in ordered]
    if dry_run:
        print(
            "trunk_step: compile-log (dry run) would append {} fragment(s) in "
            "merge order: {}".format(len(names), ", ".join(names))
        )
        return 0
    pa = _plan_artifacts()
    for path, text in ordered:
        pa.append_log_summary(root, rebase_links(text))
    for path, _ in ordered:
        path.unlink()
    print(
        "trunk_step: compile-log — appended {} fragment(s) to docs/log.md in "
        "merge order: {}".format(len(names), ", ".join(names))
    )
    return 0


# --- regen --------------------------------------------------------------------


def _profile(root):
    """`docs/stack.ini` parsed, or None. check.py's parser settings verbatim
    (`interpolation=None` so a `%` in a value needs no escaping; utf-8-sig for a
    Notepad BOM). A malformed profile is a loud failure there; here it degrades to
    the built-in defaults rather than blocking a regen on a file this step does
    not own."""
    path = Path(root) / "docs" / "stack.ini"
    if not path.exists():
        return None
    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read_string(path.read_text(encoding="utf-8-sig", errors="replace"))
    except configparser.Error:
        return None
    return cp


def _pget(profile, section, option, fallback):
    if profile is None or not profile.has_section(section):
        return fallback
    return (
        profile.get(section, option)
        if profile.has_option(section, option)
        else fallback
    )


def _cmd(name, *args):
    return lambda root: [sys.executable, str(_SCRIPTS / name), "--root", ".", *args]


def _has(rel):
    return lambda root: (Path(root) / rel).exists()


def _work_registry(root):
    return (Path(root) / "docs" / "work").is_dir() or (
        Path(root) / "docs" / "requirements" / "work-items.csv"
    ).exists()


def _status_block(root):
    """The status snapshot is spliced between markers; without the pair there is
    nothing to regenerate (the opt-in posture check.py's `status-map` step reads
    the same way)."""
    path = Path(root) / "docs" / "status.md"
    if not path.exists():
        return False
    return "BEGIN GENERATED STATUS" in path.read_text(
        encoding="utf-8", errors="replace"
    )


def _components(root):
    return (
        spine_carrier.resolve(Path(root) / "docs/requirements/components.toml")
        is not None
        or (Path(root) / "docs/requirements/components.derived.toml").exists()
    )


CLI_REFERENCE_REL = "docs/cli-reference.md"
INTERFACE_REFERENCE_REL = "docs/interface-reference.md"


def _interface_reference(root):
    """Opt-in on the same reading as `_cli_reference`: no doc or no markers
    means nothing to splice, so the step does not apply."""
    path = Path(root) / INTERFACE_REFERENCE_REL
    if not path.exists():
        return False
    return "BEGIN GENERATED INTERFACE REFERENCE" in path.read_text(
        encoding="utf-8", errors="replace"
    )


def _interface_reference_cmd(root):
    """Its own argv builder, for `_cli_reference_cmd`'s reason: this generator
    scans SOURCE, so it needs the declared `[paths] src`."""
    src = _pget(_profile(root), "paths", "src", "src")
    return [
        sys.executable,
        str(_SCRIPTS / "gen_arch_map.py"),
        "--root",
        ".",
        "--src",
        src,
        "--contracts-doc",
        INTERFACE_REFERENCE_REL,
    ]


def _cli_reference(root):
    """The CLI reference applies only where the doc exists AND carries its
    marker pair — the same opt-in reading `_status_block` gives the status
    snapshot, and for the same reason: without the markers there is nothing to
    splice, so a regen would be a hard error rather than a no-op."""
    path = Path(root) / CLI_REFERENCE_REL
    if not path.exists():
        return False
    return "BEGIN GENERATED CLI REFERENCE" in path.read_text(
        encoding="utf-8", errors="replace"
    )


def _cli_reference_cmd(root):
    """Its own argv builder rather than `_cmd`: this generator needs the
    declared `[paths] src` (it scans SOURCE, not registries), and the profile
    is only readable per-root."""
    src = _pget(_profile(root), "paths", "src", "src")
    return [
        sys.executable,
        str(_SCRIPTS / "gen_arch_map.py"),
        "--root",
        ".",
        "--src",
        src,
        "--cli-doc",
        CLI_REFERENCE_REL,
    ]


def _open_items(root):
    return (
        spine_carrier.resolve(Path(root) / "docs/requirements/open-items.toml")
        is not None
        or (Path(root) / "docs" / "open-items.html").exists()
    )


# (name, applies(root) -> bool, argv(root) -> list, why-skipped).
#
# DEPENDENCY ORDER, and every edge in it is real (the arch-map step retired
# at WI-455 — the module map derives live from the source AST, so there is no
# committed block left to regenerate):
#   okf          reads the registries; the dashboard's Knowledge tab reads the
#                BUNDLE, so a stale bundle would bake stale knowledge into the
#                dashboard (PROCESS_OPTIONS.md "okf -> trajectory").
#   derived-stage reads artifact STATES only — nothing generated — and both
#                surfaces below read its `docs/stage` output. It sits BEFORE
#                the dashboards rather than after them so that the derived
#                cache and the surfaces projecting it are always written from
#                the SAME tree state: split across the regen sequence they
#                could straddle an edit and record two different spines. (It
#                arrived at slice 1 beside a `derived-gate` twin over
#                `docs/gate`, feeding nothing generated until slice 2 re-keyed
#                the readers; slice 5 deleted that twin and its file.)
#   trajectory   the dashboard highlights the current stage from `docs/stage`.
#   status       the snapshot projects the derived stage + spine counts.
#   open-items   reads the registry + git; nothing reads it back.
#   component-view reads the CMP/LLR/SR/IF registries; nothing reads it back
#                (it is a LEAF, like open-items, so its position is free — it
#                sits last because it was added last, not because anything
#                downstream of it exists).
#   cli-reference reads the SOURCE TREE only — no registry, no generated file —
#                so it has no edge at all and its position is free for the same
#                reason component-view's is.
REGEN_STEPS = (
    (
        "okf",
        lambda root: (Path(root) / "docs" / "okf").is_dir(),
        _cmd("gen_okf.py"),
        "docs/okf/ absent",
    ),
    (
        "derived-stage",
        _has("docs/stage"),
        _cmd("derive_stage.py"),
        "docs/stage absent",
    ),
    (
        "trajectory",
        _work_registry,
        _cmd("gen_trajectory.py"),
        "no work-item registry (docs/work/ or work-items.csv)",
    ),
    (
        "status",
        _status_block,
        _cmd("gen_trajectory.py", "--status"),
        "docs/status.md absent or carries no generated-status markers",
    ),
    (
        "open-items",
        _open_items,
        _cmd("gen_open_items.py"),
        "neither docs/requirements/open-items.{toml,csv} nor docs/open-items.html",
    ),
    (
        "component-view",
        _components,
        _cmd("gen_components.py"),
        "neither docs/requirements/components.{toml,csv} nor the derived view",
    ),
    (
        "cli-reference",
        _cli_reference,
        _cli_reference_cmd,
        "docs/cli-reference.md absent or carries no CLI REFERENCE markers",
    ),
    (
        "interface-reference",
        _interface_reference,
        _interface_reference_cmd,
        "docs/interface-reference.md absent or carries no INTERFACE REFERENCE markers",
    ),
)


def regen(root, dry_run=False):
    """Re-derive the trunk's generated artifacts, in REGEN_STEPS order. Stops at
    the FIRST failure — a later generator may read an earlier one's output, so
    carrying on would pile a second, derived failure on top of the real one.
    Returns an exit code.

    Implements: SR-148, SR-170, LLR-060, LLR-124"""
    for name, applies, argv, why in REGEN_STEPS:
        if not applies(root):
            print("trunk_step: regen — skipping {} ({}).".format(name, why))
            continue
        cmd = argv(root)
        if dry_run:
            print(
                "trunk_step: regen (dry run) would run {}: {}".format(
                    name, " ".join(cmd)
                )
            )
            continue
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode != 0:
            _err(
                "regen FAILED at {} (exit {}): {}".format(
                    name, proc.returncode, " ".join(cmd)
                )
            )
            for stream in (proc.stdout, proc.stderr):
                if stream and stream.strip():
                    print(stream.rstrip(), file=sys.stderr)
            _err("the trunk lane is RED — fix this before claiming resumes (§5.5).")
            return 1
        print("trunk_step: regen — {} ok.".format(name))
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--compile-log",
        action="store_true",
        help="fold docs/log.d/*.md into docs/log.md in git-derived merge order "
        "and delete them (all-or-nothing; requires committed fragments)",
    )
    ap.add_argument(
        "--regen",
        action="store_true",
        help="re-derive the generated artifacts in dependency order",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="print what each selected operation would do; write nothing",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        _err("--root {} is not a directory".format(root))
        return 1
    # No operation flag = the whole step, compile BEFORE regen: the compile can
    # move `docs/log.md`, which the generated surfaces read.
    do_compile = args.compile_log or not (args.compile_log or args.regen)
    do_regen = args.regen or not (args.compile_log or args.regen)
    rc = 0
    if do_compile:
        rc = compile_log(root, dry_run=args.dry_run)
        if rc:
            return rc
    if do_regen:
        rc = regen(root, dry_run=args.dry_run)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
