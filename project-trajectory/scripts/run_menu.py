#!/usr/bin/env python3
"""The run capability menu — one launcher that presents every major capability.

The root `run.cmd` / `run.sh` / `run.command` launchers are thin delegates to
this script (process.md §7, "the evaluator's rungs"): running the product must
never depend on recalling a command. Capabilities are **declared once** in
`docs/stack.ini`'s `[run]` section and read here, so the launch command lives in
exactly one place instead of being duplicated across the platform launchers.

`docs/stack.ini` `[run]` section format:

    [run]
    serve = docker compose up -d && python -m webbrowser http://localhost:8080
    serve.desc = start the app and open its page
    iso = ./build_iso.sh
    iso.desc = build the bootable ISO and launch the burner

One `<name> = <command>` line per capability (in declaration order), plus an
optional `<name>.desc = <one line>`. Each command is a full **shell line** — a
multi-step capability keeps its steps in a project script and names it here once.

Usage (what the launchers invoke as `run_menu.py "$@"`):
    run_menu.py            no args  -> a numbered interactive menu (pick one)
    run_menu.py <name>     direct launch of that capability (exit code passes through)
    run_menu.py --list     stable machine-readable listing (the agent surface)

`--list` prints one capability per line as `name<TAB>desc` (desc empty when none),
in declaration order — a parse-stable contract for agents/scripts; it exits 0 with
empty output when nothing is declared. The interactive and direct paths instead
print the same "no run capability wired yet" guidance and exit 1 on an absent or
empty `[run]` section, exactly as the pre-menu launchers did — a pure library
simply deletes the `run.*` launchers.

Stdlib-only, Python 3.8+, Windows + POSIX (the same portability contract as the
rest of the kit). The command is run with `shell=True`: the value is the user's
own declared shell line from their own `docs/stack.ini` (the same trust boundary
as the `RUN_CMD` this replaced — the user edits their own file), and a capability
is deliberately a full shell command (pipes, `&&`, redirects), so it is handed to
the shell verbatim rather than split into argv.

Contracts: IF-048, IF-049 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import configparser
import subprocess
import sys
from pathlib import Path

# The declared toolchain, read at repo root when present (the launchers cd there
# first). Same file check.py reads; this script only ever touches its [run]
# section, which check.py ignores.
DEFAULT_STACK_INI = Path("docs/stack.ini")


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII capability name / desc / command banner can't raise
    UnicodeEncodeError on a legacy Windows cp1252 console (the sibling scripts'
    guard). Python 3.7+ streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def load_capabilities(path):
    """Parse the `[run]` section of a stack.ini into an ordered list of
    (name, command, desc). Returns [] when the file or section is absent/empty.

    Declaration order is preserved (configparser is insertion-ordered), key case
    is preserved (a capability may be `Serve`), and `interpolation=None` keeps a
    literal `%`/`{}` in a command untouched. A malformed profile fails LOUDLY —
    a typo can't quietly hide a capability. A `<name>.desc` with no matching
    `<name> =` command, or a command with an empty value, is ignored."""
    if not path.exists():
        return []
    cp = configparser.ConfigParser(interpolation=None)
    cp.optionxform = str  # preserve capability-name case
    try:
        cp.read_string(path.read_text(encoding="utf-8"), source=str(path))
    except configparser.Error as exc:
        sys.exit("run_menu: {} is malformed: {}".format(path, exc))
    if not cp.has_section("run"):
        return []
    descs = {}
    commands = []
    for key, val in cp.items("run"):
        if key.endswith(".desc"):
            descs[key[: -len(".desc")]] = val.strip()
        else:
            commands.append((key, val.strip()))
    return [(name, cmd, descs.get(name, "")) for name, cmd in commands if cmd]


NO_CAPABILITIES = (
    "run_menu: no run capabilities declared yet.\n"
    "Declare them in docs/stack.ini under a [run] section, one line each:\n"
    "  [run]\n"
    "  serve = python -m yourapp\n"
    "  serve.desc = start the app\n"
    "The README 'Run it' section documents the underlying commands.\n"
    "(A pure library has none — delete the run.* launchers.)"
)


def launch(command, extra):
    """Run a capability's shell line, returning its exit code (passthrough).

    `extra` (trailing args the launcher forwarded) is appended to the command
    line, mirroring the old `exec $RUN_CMD "$@"` passthrough. shell=True is
    intentional — see the module docstring."""
    full = command if not extra else command + " " + " ".join(extra)
    print("Running: {}".format(full), flush=True)
    return subprocess.run(full, shell=True).returncode


def direct(capabilities, name, extra):
    """Launch the named capability, or report the valid names and exit 2."""
    for cap_name, command, _desc in capabilities:
        if cap_name == name:
            return launch(command, extra)
    print(
        "run_menu: no capability named {!r}. Declared: {}".format(
            name, ", ".join(n for n, _, _ in capabilities) or "(none)"
        ),
        file=sys.stderr,
    )
    return 2


def interactive_menu(capabilities):
    """Present the numbered menu, read a pick from stdin, launch it.

    Reads from stdin (a TTY when double-clicked, a piped selection otherwise);
    an EOF (closed/exhausted stdin) ends the loop rather than hanging, so an
    unattended invocation is safe. `q`/`quit`/blank quits with exit 0."""
    print("Run — available capabilities:\n")
    for i, (name, _command, desc) in enumerate(capabilities, 1):
        line = "  {}) {}".format(i, name)
        if desc:
            line += " — " + desc
        print(line)
    print()
    while True:
        try:
            raw = input("Select [1-{}] (q to quit): ".format(len(capabilities)))
        except EOFError:
            print("run_menu: no selection (input closed).", file=sys.stderr)
            return 1
        raw = raw.strip()
        if raw.lower() in ("", "q", "quit"):
            return 0
        try:
            choice = int(raw)
        except ValueError:
            choice = 0
        if 1 <= choice <= len(capabilities):
            _name, command, _desc = capabilities[choice - 1]
            return launch(command, [])
        print("  not a valid choice; enter 1-{} or q.".format(len(capabilities)))


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="Present/launch the capabilities declared in docs/stack.ini [run].",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--list",
        action="store_true",
        help="print a stable machine listing (name<TAB>desc, one per line) and exit 0",
    )
    ap.add_argument(
        "--file",
        default=str(DEFAULT_STACK_INI),
        help="stack.ini to read the [run] section from (default: docs/stack.ini)",
    )
    ap.add_argument(
        "name",
        nargs="?",
        help="a capability name to launch directly (no name = the interactive menu)",
    )
    ap.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="trailing args forwarded to the launched command",
    )
    ns = ap.parse_args(argv)

    capabilities = load_capabilities(Path(ns.file))

    if ns.list:
        # The agent surface: parse-stable, empty when nothing is declared (an
        # agent reads zero lines rather than guidance prose on stdout).
        for name, _command, desc in capabilities:
            print("{}\t{}".format(name, desc))
        return 0

    if not capabilities:
        print(NO_CAPABILITIES, file=sys.stderr)
        return 1

    if ns.name is not None:
        return direct(capabilities, ns.name, ns.args)
    return interactive_menu(capabilities)


if __name__ == "__main__":
    sys.exit(main())
