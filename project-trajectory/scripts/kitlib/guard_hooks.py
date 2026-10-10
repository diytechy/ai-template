"""The coordinator guard's hooks in a Claude Code settings object: which of its
commands are the guard's own, and how switching them on merges into settings
that already hold hooks.

WHY THIS EXISTS (WI-834, round 7). dev-setup's consented opt-in
(`coordinator_guard.py hooks --enable`) copies the guard's hook groups from the
kit's inert example into a machine-local settings file, bound to the
interpreter the opt-in runs on (decision D-019). That merge must own the
guard's commands and nothing else. Owning whole groups deleted a user's command
sharing a group with the guard's (round 018 F2). Owning any command that
mentions the guard's file deleted a user's `ruff check …/coordinator_guard.py`
(round 020 O2). So what the guard owns is defined once, here, from the
example's own commands, and the merge and the guard's on/off reading both use
it. Pure functions over JSON-shaped values: the file reading and writing stay
in `coordinator_guard.py` (decomposed out of it at its 1000-line ratchet).
"""

import json
import os
from pathlib import Path

GUARD_SCRIPT = "coordinator_guard.py"


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


def command_shapes(groups):
    """The guard's own commands as the example writes them: `{(interpreter
    word, rest)}`, the rest being the guard's script and its hook
    subcommand. `groups` is `guard_groups`' result.

    Implements: SR-032, LLR-322
    """
    return {
        _split_interpreter(hook.get("command") or "")
        for event_groups in groups.values()
        for group in event_groups
        for hook in group.get("hooks") or ()
    }


def merged(hooks, wanted, shapes):
    """A settings `hooks` object with the guard owned command by command:
    for each event in `wanted`, every existing group loses only the guard's
    own commands (`shapes`; a group left with none is dropped), keeping its
    other commands and its configuration, then the bound groups
    `wanted[event]` are added. Idempotent.

    Implements: SR-032, LLR-322
    """
    result = dict(hooks)
    for event, groups in wanted.items():
        rest = (_without_guard(g, shapes) for g in result.get(event) or [])
        result[event] = [group for group in rest if group is not None] + groups
    return result


def _split_interpreter(command):
    """`(interpreter word, rest)` of a hook command: a leading double-quoted
    path is one word (what `bind` writes), else the first word."""
    if command.startswith('"') and '"' in command[1:]:
        end = command.index('"', 1) + 1
    else:
        end = command.find(" ") if " " in command else len(command)
    return command[:end], command[end:].lstrip(" ")


def _owns(hook, shapes):
    """Whether a settings hook command is the guard's own: exactly one of
    `shapes`, run by the example's own interpreter word (an older or copied
    install) or by a double-quoted absolute path (`bind`'s). A command that
    merely names the guard's file is not."""
    interpreter, rest = _split_interpreter(hook.get("command") or "")
    bound = len(interpreter) > 2 and interpreter[0] == interpreter[-1] == '"'
    bound = bound and os.path.isabs(interpreter[1:-1])
    return any(rest == r and (interpreter == i or bound) for i, r in shapes)


def _without_guard(group, shapes):
    """`group` without the guard's own commands (`_owns`), every other
    command and the group's configuration kept; None when only the guard's
    commands were in it."""
    if not isinstance(group, dict):
        return group
    hooks = group.get("hooks") or []
    kept = [hook for hook in hooks if not _owns(hook, shapes)]
    if len(kept) == len(hooks):
        return group
    return dict(group, hooks=kept) if kept else None
