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

Contracts: IF-120 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.csv).
"""

import argparse
import configparser
import posixpath
import re
import subprocess
import sys
from pathlib import Path

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
RESERVED_HEADINGS = ("## Gate Sign-offs", "## Decisions log", "## Audit log")

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


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is (the same
    guard as trace.py / check.py — a non-ASCII path can't wedge a cp1252 console)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _git_out(root, args):
    """stdout of a git command under `root`, or None on ANY failure (no git
    binary, not a repo, unknown rev/path) — trace.py's best-effort-off-git
    pattern. Callers here turn a None into a LOUD error rather than degrading:
    merge order is the one thing this step cannot guess."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _err(message):
    print("trunk_step: " + message, file=sys.stderr)


# --- compile-log --------------------------------------------------------------


def fragment_paths(root):
    """The fragment files awaiting compilation, filename-sorted. Dotfiles are
    skipped so the scaffold marker (`.gitkeep`) is never mistaken for one."""
    d = Path(root) / LOG_D
    if not d.is_dir():
        return []
    return sorted(
        (p for p in d.glob("*.md") if p.is_file() and not p.name.startswith(".")),
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
    printed."""
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


def _arch_map_cmd(root):
    """gen_arch_map's argv, built from `docs/stack.ini` the way check.py builds
    its `--check` twin ([paths] src, [arch-map] mode/comment-prefixes) — the same
    declared source, so the write and the freshness gate can't disagree. Kept
    minimal on purpose; gen_arch_map is the only generator with no `--root`, so
    every step here runs with `cwd=root`."""
    profile = _profile(root)
    cmd = [
        sys.executable,
        str(_SCRIPTS / "gen_arch_map.py"),
        "--strict-parse",
        "--src",
        _pget(profile, "paths", "src", "src"),
        "--doc",
        "docs/architecture.md",
    ]
    if _pget(profile, "arch-map", "mode", "symbols") == "files":
        cmd += ["--mode", "files"]
        for tok in _pget(profile, "arch-map", "comment-prefixes", "").split():
            cmd += ["--comment-prefix", tok]
    return cmd


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


def _open_items(root):
    return (
        spine_carrier.resolve(Path(root) / "docs/requirements/open-items.toml")
        is not None
        or (Path(root) / "docs" / "open-items.html").exists()
    )


# (name, applies(root) -> bool, argv(root) -> list, why-skipped).
#
# DEPENDENCY ORDER, and every edge in it is real:
#   arch-map     reads source only.
#   okf          reads the registries; the dashboard's Knowledge tab reads the
#                BUNDLE, so a stale bundle would bake stale knowledge into the
#                dashboard (PROCESS_OPTIONS.md "arch-map -> okf -> trajectory").
#   derived-gate reads artifact STATES only — nothing generated — and both
#                surfaces below read its `docs/gate` output.
#   trajectory   the dashboard highlights the current gate from `docs/gate`.
#   status       the snapshot projects the derived gate + spine counts.
#   open-items   reads the registry + git; nothing reads it back.
REGEN_STEPS = (
    (
        "arch-map",
        _has("docs/architecture.md"),
        _arch_map_cmd,
        "docs/architecture.md absent",
    ),
    (
        "okf",
        lambda root: (Path(root) / "docs" / "okf").is_dir(),
        _cmd("gen_okf.py"),
        "docs/okf/ absent",
    ),
    (
        "derived-gate",
        _has("docs/gate"),
        _cmd("derive_gate.py"),
        "docs/gate absent",
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
)


def regen(root, dry_run=False):
    """Re-derive the trunk's generated artifacts, in REGEN_STEPS order. Stops at
    the FIRST failure — a later generator may read an earlier one's output, so
    carrying on would pile a second, derived failure on top of the real one.
    Returns an exit code."""
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
