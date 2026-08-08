#!/usr/bin/env python3
"""Answer ONE declared configuration key, for callers that cannot parse TOML.

Stack-agnostic, standard-library only. The git hooks defend privacy and review
policy before any Python tooling runs, and they are POSIX `sh`: they used to
read a policy by grepping the first non-comment line out of a one-word file.
That parse is gone with the file (contracts §1), and no shell can read TOML —
so the hooks ask this entry point instead.

Three properties, each deliberate:

  - **One key per invocation.** The hook's call site stays one line and its
    failure mode is unambiguous: a value on stdout with exit 0, or nothing on
    stdout and a named refusal on stderr. There is no "answered partially".
  - **It FAILS CLOSED.** Any refusal — an interpreter below the declared floor,
    an undeclared key, a config that does not validate — exits non-zero, and
    the hooks treat a non-zero exit as a block. This is strictly stronger than
    the grep it replaces (decision D-1): the grep answered "absent" on a box
    with no Python and let the commit proceed, which is exactly the shape of
    dishonest green the privacy gate exists to prevent. The recorded trade is
    real and is the ratified one: a box that cannot run this script cannot
    commit.
  - **It is CHEAP.** The floor check runs before anything else is imported, so
    a below-floor interpreter refuses by name instead of dying inside
    `import tomllib`; `config` is imported lazily for the same reason. Nothing
    here reaches for argparse or the rest of the kit.

Deliberately NOT done here: the mixed-source refusal (`config.mixed_source_
findings`). That belongs to the configuration PREFLIGHT, which runs once per
session — and since P14 it HAS that call site, inside
`agent_common.declared_config`. A repo mid-migration legitimately carries both a
canonical key and its retired source for the length of the migration, and
folding that refusal into the per-commit hook read would stop the migration from
ever being committed: the commit that DELETES the retired file is itself made
from a tree that still has it.

Deliberately DONE here, since the P13 cutover: the **unconverted** refusal
(`config.unconverted_findings`), which is the opposite state and the dangerous
one. Both-present is a repo mid-migration; retired-present-and-canonical-unset
is a repo whose declared policy nothing obeys, and answering it with a schema
default is the measured fail-open this entry point exists to end.

Usage:
    python scripts/config_query.py [--root DIR] policy.privacy_check

Booleans print as `true`/`false` (the vocabulary the retired one-word files
used, so a shell comparison reads the same); arrays print one element per line.

The interpreter floor below is duplicated from `agent_common.MIN_PYTHON` per the
kit's independently-copyable-script rule (F5) — this script must answer BEFORE
anything heavy is importable — and `tests/test_config_query.py` pins the two
equal.
"""

import sys

MIN_PYTHON = (3, 11)

USAGE = "usage: config_query.py [--root DIR] <dotted.key>"


def floor_refusal(version=None):
    """The refusal string when `version` (default: this interpreter's
    `(major, minor)`) is below the declared floor, else None.

    Taken as a parameter-free global read so a test can simulate a below-floor
    box by moving the FLOOR — there is no other way to exercise the branch on a
    machine that satisfies it, and a hidden test-only argument would be a
    second contract."""
    ver = tuple(version if version is not None else sys.version_info[:2])
    if ver >= MIN_PYTHON:
        return None
    return (
        "config_query: REFUSED - interpreter Python {} (below the declared "
        "floor Python {}+, so the configuration cannot be read; a policy this "
        "script cannot read is never treated as absent)".format(
            ".".join(str(p) for p in ver), ".".join(str(p) for p in MIN_PYTHON)
        )
    )


def render(value):
    """The printable form of a resolved value: `true`/`false` for booleans (the
    vocabulary the retired declared-policy files used), one element per line for
    an array, `str()` otherwise."""
    if value is True or value is False:
        return "true" if value else "false"
    if isinstance(value, (tuple, list)):
        return "\n".join(str(v) for v in value)
    return str(value)


def parse_args(argv):
    """`(root, key, error)` from the tiny hand-rolled command line. Hand-rolled
    rather than argparse: this runs on every commit, and the whole grammar is
    one optional flag and one positional."""
    root, key, rest = ".", None, list(argv)
    while rest:
        arg = rest.pop(0)
        if arg == "--root":
            if not rest:
                return None, None, "--root needs a directory"
            root = rest.pop(0)
        elif arg.startswith("--root="):
            root = arg.split("=", 1)[1]
        elif arg.startswith("-"):
            return None, None, "unknown option {!r}".format(arg)
        elif key is None:
            key = arg
        else:
            return None, None, "expected exactly one key, also got {!r}".format(arg)
    if key is None:
        return None, None, "no key given"
    return root, key, None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)

    # Before ANY other import: a below-floor interpreter must refuse by name,
    # not die inside `import tomllib` with a traceback a hook cannot interpret.
    refusal = floor_refusal()
    if refusal is not None:
        print(refusal, file=sys.stderr)
        return 1

    # Emit UTF-8 whatever the console codepage is — the same guard every other
    # kit CLI takes (`config_migrate.main`, `check.py`, `derive_gate.py`). It
    # earns its place here specifically: a refusal QUOTES the converter's own
    # reason strings, which carry non-ASCII punctuation, and on a cp1252 console
    # that raised instead of printing. A refusal that cannot be printed is a
    # refusal nobody reads. No import — `reconfigure` is a method on the stream.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    root, key, error = parse_args(argv)
    if error is not None:
        print("config_query: REFUSED - {} ({})".format(error, USAGE), file=sys.stderr)
        return 1

    import config  # deferred: it imports tomllib, which the floor check guards

    cfg, findings = config.load_config(root)
    if findings:
        for line in config.refusal_lines(findings, module="config_query"):
            print(line, file=sys.stderr)
        return 1

    try:
        value = cfg.get(key)
    except KeyError:
        section = key.split(".", 1)[0]
        siblings = sorted(p for p in config.DEFAULTS if p.startswith(section + "."))
        print(
            "config_query: REFUSED - {} (not a declared key{})".format(
                key,
                "; declared in this section: " + ", ".join(siblings)
                if siblings
                else "",
            ),
            file=sys.stderr,
        )
        return 1

    # THE CUTOVER'S FAIL-CLOSED RUNG. An unconverted repo — one whose retired
    # file still declares this dial while the canonical key is unset — is
    # REFUSED, never answered with the default. This is the exact fail-open the
    # program measured: a tree carrying `docs/privacy-check = true` was answered
    # `false` and lost its privacy gate in silence. A repo that has converted, or
    # that never declared anything different, pays nothing (config.py's
    # `unconverted_findings` states the three cases).
    unconverted = config.unconverted_findings(root, (key,), cfg=cfg)
    if unconverted:
        for line in config.refusal_lines(unconverted, module="config_query"):
            print(line, file=sys.stderr)
        return 1

    print(render(value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
