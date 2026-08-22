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

Stdlib-only, Python 3.11+, Windows + POSIX (the same portability contract as the
rest of the kit). The command is run with `shell=True`: the value is the user's
own declared shell line from their own `docs/stack.ini` (the same trust boundary
as the `RUN_CMD` this replaced — the user edits their own file), and a capability
is deliberately a full shell command (pipes, `&&`, redirects), so it is handed to
the shell verbatim rather than split into argv.

**Trailing arguments** the launchers forward (`run_menu.py <name> arg…`, the old
`exec $RUN_CMD "$@"`) are treated as **data values, not shell text** (the WI-227
ruling): the recipe is trusted, an evaluator's `"$@"` is a value. Each is
appended to the recipe *quoted for the platform shell* (`_quote_extra`) so a
value with spaces, quotes, or an `&`/`|` reaches the program as one literal
argument rather than splitting or executing. POSIX uses `shlex.quote` (total).
Windows is total for shell syntax too: `_win_quote` MSVCRT-quotes each value and
then caret-escapes every cmd.exe metacharacter (`_CMD_META`), so a separator can
never be re-parsed as a command operator — even combined with a literal `"`. One
Windows-only limit is documented rather than fought (this is an ordinary
convenience layer, not the dispatcher): cmd.exe still expands a `%VAR%` (and a
`!VAR!` under delayed expansion) in a value, because it does that pass before
caret processing and a single `cmd /c` line cannot suppress it. The recipe lines
themselves stay trusted shell text.

Contracts: IF-048, IF-049 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import configparser
import os
import shlex
import subprocess
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The declared toolchain, read at repo root when present (the launchers cd there
# first). Same file check.py reads; this script only ever touches its [run]
# section, which check.py ignores.
DEFAULT_STACK_INI = Path("docs/stack.ini")


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


# cmd.exe's own shell operators plus the double quote. After the MSVCRT argv
# quoting in _win_quote, every one of these in the result is caret-escaped so
# cmd.exe passes the token through literally instead of re-parsing an embedded
# separator as a command operator (the WI-227 data contract). `%` is deliberately
# absent: cmd.exe expands `%VAR%` in an earlier pass, before caret processing, so
# it can't be suppressed on a single `cmd /c` line — the one documented limit.
_CMD_META = frozenset('()^"<>&|')


def _win_quote(arg):
    """Quote one trailing DATA argument for a cmd.exe command line (Windows,
    shell=True) so it reaches the program as exactly one literal token that
    cmd.exe never re-parses as shell syntax. Two phases:

    1. MSVCRT argv quoting — wrap in double quotes and escape for the target
       program's own argv parser: each run of backslashes preceding a `"` is
       doubled and the quote backslash-escaped, and a trailing run before the
       closing quote is doubled too.
    2. cmd.exe caret escaping — prefix `^` to every cmd.exe metacharacter in the
       phase-1 result, *including the double quotes phase 1 added*. cmd.exe then
       treats each as a non-toggling literal, so a separator (`&` `|` `<` `>` `(`
       `)` `^`) inside the value stays literal even when the value also contains
       a `"`. This closes the cmd.exe-vs-MSVCRT quote-state gap where a `"` used
       to end cmd.exe's quoted region early and re-expose a following `&`/`|` to
       the shell.

    Residual limit (documented, not fought — this is an ordinary convenience
    layer): a `%VAR%` (and a `!VAR!` under delayed expansion) in a value is still
    expanded, because cmd.exe does that pass before caret processing and a single
    `cmd /c` line cannot suppress it. POSIX (`shlex.quote`) has no such limit."""
    msvcrt = ['"']
    backslashes = 0
    for ch in arg:
        if ch == "\\":
            backslashes += 1
            msvcrt.append(ch)
            continue
        if ch == '"':
            msvcrt.append("\\" * backslashes)  # double the run already emitted
            msvcrt.append('\\"')
        else:
            msvcrt.append(ch)
        backslashes = 0
    msvcrt.append("\\" * backslashes)  # double a trailing run before the close quote
    msvcrt.append('"')
    quoted = "".join(msvcrt)
    return "".join(("^" + ch) if ch in _CMD_META else ch for ch in quoted)


def _quote_extra(extra):
    """Quote trailing DATA arguments so the shell line receives each as exactly
    one literal token — the WI-227 data-argument contract (module docstring
    'Trailing arguments'). POSIX uses shlex.quote (total); Windows uses the
    cmd.exe/MSVCRT quoting above."""
    quote = _win_quote if os.name == "nt" else shlex.quote
    return " ".join(quote(a) for a in extra)


def launch(command, extra):
    """Run a capability's shell line, returning its exit code (passthrough).

    The declared command is the trusted shell recipe; `extra` (trailing args the
    launcher forwarded, the old `exec $RUN_CMD "$@"`) are DATA values, each quoted
    per-platform (`_quote_extra`) so the shell can't re-split a value on
    whitespace or a metacharacter. shell=True is intentional for the recipe — see
    the module docstring."""
    full = command if not extra else command + " " + _quote_extra(extra)
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
