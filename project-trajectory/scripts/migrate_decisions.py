#!/usr/bin/env python3
"""Rewrite every delegated-decisions record off the retired `reviewed` key
(WI-818), in place.

WHY A MIGRATOR AND NOT A READER. WI-818 gives the owner's verdict on a
delegated decision its own key, `owner` (`confirmed` or `overruled`; absent is
not yet seen), and retires WI-790's `reviewed`. The owner ruled out legacy
paths: no reader reads `reviewed` beside `owner`, so a record still carrying it
reads as not yet seen and reports a format finding until it is rewritten. This
script is that rewrite, run once by a repository at its next resync:
`reviewed = true` (or any word that read as reviewed) becomes
`owner = "confirmed"` in the same place, a not-reviewed value is dropped, and
every other line — each `review` note, every comment — is kept byte for byte
(`kitlib.decisions.migrate_text`). It rewrites complete top-level
assignments only, never a string's contents, and re-parses the result: a
record whose re-parse would differ in anything but the verdict keys is left
untouched and named. A value outside the retired vocabulary is
left where it is and named, because guessing the owner's verdict is the one
thing a migration must not do.

Usage:
    python scripts/migrate_decisions.py [--root .] [--check]

`--check` writes nothing and exits 1 when any record still needs the rewrite;
otherwise the records are rewritten and the script exits 0, or 1 when a record
does not parse (it is left untouched and named). Idempotent.
"""

import argparse
import sys
from pathlib import Path

from kitlib import decisions as _kitdecisions


def _migrate_one(path, check):
    """`(changed, problems)` for one record file: whether it needed the
    rewrite (and, unless `check`, was rewritten), and the lines naming what it
    could not do. The file's own line endings are kept.

    Implements: SR-225, LLR-304
    """
    raw = path.read_bytes().decode("utf-8")
    try:
        new, left = _kitdecisions.migrate_text(raw)
    except ValueError as exc:
        return False, ["{}: {}; left untouched".format(path.name, exc)]
    problems = [
        "{}: {} keeps a `reviewed` value outside the retired vocabulary; set "
        "its `owner` by hand".format(path.name, eid)
        for eid in left
    ]
    if new == raw:
        return False, problems
    if not check:
        path.write_bytes(new.encode("utf-8"))
    return True, problems


def main(argv=None):
    """Rewrite (or, with `--check`, report) every record under
    `docs/decisions/`; exit 0 when nothing is left to do, else 1.

    Implements: SR-225, LLR-304
    """
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--check", action="store_true", help="report records owing the rewrite"
    )
    args = ap.parse_args(argv)
    folder = Path(args.root) / _kitdecisions.DECISIONS_DIR
    changed, problems = [], []
    for path in sorted(folder.glob("*.toml")) if folder.is_dir() else ():
        did, why = _migrate_one(path, args.check)
        changed += [path.name] if did else []
        problems += why
    verb = "owes the rewrite" if args.check else "rewritten"
    for name in changed:
        print("migrate_decisions: {} {}".format(name, verb))
    for line in problems:
        print("migrate_decisions: {}".format(line))
    if not changed and not problems:
        print("migrate_decisions: no record carries the retired `reviewed` key")
    unparsed = any(p.endswith("left untouched") for p in problems)
    return 1 if (args.check and changed) or unparsed else 0


if __name__ == "__main__":
    sys.exit(main())
