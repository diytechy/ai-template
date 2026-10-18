"""The coordinator guard's hooks in a Claude Code settings object, checked by
name and never shared.

WHY THIS EXISTS. The kit ships the guard's hook groups inert; dev-setup's offer
and the coordinator lease's take write them into a machine-local settings file
only with a terminal yes, each bound to the interpreter the install runs on.
The slot is each guard event the example uses, and it is either empty, exactly
the guard's own command (its script's file name and the `hook` subcommand,
whatever the interpreter word), or something else. So the reading answers
none (the example registers no guard group), absent, on or occupied, naming
what is in the way; only absent is ever written, and nothing is merged beside
another hook. The reading itself is pure over JSON-shaped values; the file
side below it (`hooks_state`, `install_hooks`, `consent_install`) reads the
settings and writes them, moved whole out of `coordinator_guard.py` at its
1000-line ratchet.
"""

import json
import sys
from pathlib import Path
from typing import NamedTuple

from .observation import write_atomic

GUARD_SCRIPT = "coordinator_guard.py"
HOOK_WORD = "hook"
FIX = (
    "Fix: move those hooks to another settings file, such as your user "
    "~/.claude/settings.json, or remove them, then run again."
)
# What the reading holds for a settings file or a guard event that is not
# there. It is never a parsed JSON value, so a JSON `null` stays the malformed
# shape it is.
ABSENT = object()


class Problem(NamedTuple):
    """A settings or example file that could not be read or parsed: `text`
    names the error."""

    text: str


class Reading(NamedTuple):
    """The guard hooks' state: `word` is none, absent, on or occupied, and
    `problems` names what is in the way (empty unless occupied)."""

    word: str
    problems: tuple = ()


def read_state(example, settings):
    """The guard hooks' state over the parsed example and machine-local
    settings. `example` is the example object or a `Problem`; `settings` is
    the parsed settings value, `ABSENT` when there is no file, or a `Problem`. Only
    the example's guard events are read; every other event and key is not.

    Implements: SR-032, LLR-322
    """
    if isinstance(example, Problem):
        return Reading("occupied", ("the shipped example: " + example.text,))
    events = sorted(guard_groups(example))
    if not events:
        return Reading("none")
    hooks, fault = _settings_hooks(settings)
    if fault:
        return Reading("occupied", (fault,))
    problems, empty = [], []
    for event in events:
        held = _event_problems(event, hooks.get(event, ABSENT))
        if held is None:
            empty.append(event)
        problems.extend(held or ())
    if len(empty) == len(events):
        return Reading("absent")
    problems.extend(event + ": the guard's hook is missing" for event in empty)
    return Reading("occupied", tuple(problems)) if problems else Reading("on")


def is_guard_command(command):
    """Whether a hook command is the guard's by name: after its interpreter
    word, its last two words are a path whose base name (quotes stripped) is
    the guard's script, then the `hook` subcommand. The interpreter word is
    not checked.

    Implements: SR-032, LLR-322
    """
    if not isinstance(command, str):
        return False
    rest = _split_interpreter(command.strip())[1]
    head, _, last = rest.rpartition(" ")
    if last != HOOK_WORD or not head.strip():
        return False
    path = _last_word(head.rstrip()).strip('"').replace("\\", "/")
    return path.rsplit("/", 1)[-1] == GUARD_SCRIPT


def refusal_text(path, reading):
    """The one complaint every route prints at occupied: the settings file,
    each problem, and the fix.

    Implements: SR-032, LLR-322
    """
    lines = ["{}: the coordinator's guard hooks cannot go here:".format(path)]
    lines += ["  " + problem for problem in reading.problems]
    return "\n".join(lines + [FIX])


def _settings_hooks(settings):
    """`(hooks object, None)` from the parsed settings, or `(None, fault)`
    when the settings or their `hooks` are not the expected shapes."""
    if isinstance(settings, Problem):
        return None, "the settings file does not parse: " + settings.text
    if settings is ABSENT:
        return {}, None
    if not isinstance(settings, dict):
        return None, "the settings file is not a JSON object"
    hooks = settings.get("hooks", {})
    if not isinstance(hooks, dict):
        return None, "the settings file's `hooks` is not a JSON object"
    return hooks, None


def _event_problems(event, groups):
    """None when a guard event holds nothing, `[]` when it holds exactly the
    guard's command, else the problems found in it, each naming the event."""
    if groups is ABSENT or groups == []:
        return None
    if not isinstance(groups, list):
        return [event + ": its value is not a list"]
    problems = []
    if len(groups) != 1:
        problems.append("{}: holds {} hook groups".format(event, len(groups)))
    for group in groups:
        problems.extend(_group_problems(event, group))
    return problems


def _group_problems(event, group):
    """The problems in one hook group of a guard event: no `hooks` list, more
    than one command, a command that is not a string, or one that is not the
    guard's (quoted)."""
    entries = group.get("hooks") if isinstance(group, dict) else None
    if not isinstance(entries, list):
        return [event + ": a group has no `hooks` list"]
    problems = []
    if len(entries) != 1:
        problems.append("{}: a group holds {} commands".format(event, len(entries)))
    for entry in entries:
        command = entry.get("command") if isinstance(entry, dict) else None
        if not isinstance(command, str):
            problems.append(event + ": a command is not a string")
        elif not is_guard_command(command):
            problems.append(
                "{}: {} is not the guard's".format(event, json.dumps(command))
            )
    return problems


def _last_word(text):
    """The last word of `text`, a trailing double-quoted path kept whole."""
    if text.endswith('"') and text.count('"') >= 2:
        return text[text.rindex('"', 0, len(text) - 1) :]
    return text.rsplit(None, 1)[-1] if text else ""


def guard_groups(example):
    """`{event: [group, ...]}`: the hook groups of the kit's inert example
    settings `example` whose commands run the guard.

    Implements: SR-032, LLR-322
    """
    hooks = example.get("hooks") if isinstance(example, dict) else None
    found = {}
    for event, groups in (hooks if isinstance(hooks, dict) else {}).items():
        mine = [g for g in groups or () if GUARD_SCRIPT in json.dumps(g)]
        if mine:
            found[event] = mine
    return found


def bind(group, interpreter):
    """An example guard group with each command's leading interpreter word
    (the example's portable `python`) replaced by `interpreter`, as a
    double-quoted forward-slash path (read alike by the POSIX shell and cmd
    a hook command runs through, and safe for a path with spaces).

    Implements: SR-032, LLR-322
    """
    bound = json.loads(json.dumps(group))
    for hook in bound.get("hooks") or ():
        rest = _split_interpreter(hook.get("command") or "")[1]
        hook["command"] = '"{}" {}'.format(Path(interpreter).as_posix(), rest)
    return bound


def _split_interpreter(command):
    """`(interpreter word, rest)` of a hook command: a leading double-quoted
    path is one word (what `bind` writes), else the first word."""
    if command.startswith('"') and '"' in command[1:]:
        end = command.index('"', 1) + 1
    else:
        end = command.find(" ") if " " in command else len(command)
    return command[:end], command[end:].lstrip(" ")


# --- the file side: read the settings, and install with consent -------------------

ASK = (
    "Write the coordinator's Claude Code hooks into the machine-local "
    ".claude/settings.local.json? [y/N] "
)
NO_TERMINAL = (
    "the coordinator's Claude Code guard hooks are not installed in {}, and no "
    "terminal can consent here: run dev-setup at a terminal (the bare `run`, or "
    "its install tier: `--baseline` or `-Baseline`, which the kit's own repository "
    "names `--install` or `-Install`) and answer yes, then take again."
)
# What a consented install that did not take tells the person to do.
INSTALL_FIX = "Fix: move or repair that file, then run again."


def local_settings(root):
    """The machine-local Claude Code settings the install writes: their hook
    commands name this machine's interpreter, so they never go in the
    committed `.claude/settings.json`.

    Implements: SR-032, LLR-322
    """
    return Path(root) / ".claude" / "settings.local.json"


def _parsed(path, absent):
    """The JSON value at `path`; `absent` when there is no file; a `Problem`
    naming the file and the error when it cannot be read or parsed."""
    path = Path(path)
    try:
        if not path.exists():
            return absent
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return Problem("{}: {}".format(path, exc))


def hooks_state(root, example):
    """The guard hooks' `Reading` (none, absent, on or occupied) over the
    inert config `example` (absent: none) and the machine-local settings. A
    file that cannot be read or parsed reads occupied, named.

    Implements: SR-032, LLR-322
    """
    example = _parsed(example, {})
    return read_state(example, _parsed(local_settings(root), ABSENT))


def install_hooks(root, example, interpreter=None):
    """From absent only: write every guard group of `example` into the
    machine-local settings, each bound to `interpreter` (this process's own
    by default: the floor-resolved one), keeping every other key and event;
    then return the re-read. Any other state is returned unwritten.

    Implements: SR-032, LLR-322
    """
    reading = hooks_state(root, example)
    if reading.word != "absent":
        return reading
    path = local_settings(root)
    settings = _parsed(path, {})
    hooks = dict(settings.get("hooks", {}))
    for event, groups in guard_groups(_parsed(example, {})).items():
        hooks[event] = [bind(g, interpreter or sys.executable) for g in groups]
    settings["hooks"] = hooks
    path.parent.mkdir(parents=True, exist_ok=True)
    write_atomic(path, json.dumps(settings, indent=2) + "\n")
    return hooks_state(root, example)


def consent_install(root, example, ask):
    """The one consented install both first runs use. Returns a refusal
    text (occupied; absent with no terminal, `ask` None; an install that
    failed or whose re-read is not on), else the `Reading`: none or on, or
    absent after a no. Only an answer starting `y` or `Y` is a yes.

    Implements: SR-032, LLR-322
    """
    path = local_settings(root)
    reading = hooks_state(root, example)
    if reading.word == "occupied":
        return refusal_text(path, reading)
    if reading.word != "absent":
        return reading
    if ask is None:
        return NO_TERMINAL.format(path)
    if not _said_yes(ask):
        return reading
    try:
        reading = install_hooks(root, example)
    except OSError as exc:
        return "{}: the coordinator's hooks could not be written: {}. {}".format(
            path, exc, INSTALL_FIX
        )
    if reading.word == "on":
        return reading
    problems = "; ".join(reading.problems) or "it reads " + reading.word
    return "{}: the install did not read on: {}. {}".format(path, problems, INSTALL_FIX)


def _said_yes(ask):
    """Whether `ask(ASK)` answers yes; end of input is a no."""
    try:
        answer = ask(ASK)
    except EOFError:
        answer = ""
    return answer.startswith(("y", "Y"))
