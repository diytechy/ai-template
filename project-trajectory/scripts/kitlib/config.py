"""Declared-policy files and console encoding — the kit's declared-policy readers.

TWO READERS, ONE THEME: `first_declared_line` (and its two adapters) for the
one-word `docs/<dial>` files, and `process_check` for a `[checks]` toggle in
`docs/process.toml` (with `process_check_text` beside it for a `[checks]` key
whose value is text, such as a declared start commit). They are the two halves
of the SN-028 dual-read window — the same question asked of the legacy file
and of the TOML that supersedes it — so a caller resolving a dial reaches for
exactly one module. `assumption_gate_enabled` reads one more `[checks]` toggle,
the one that ships off and so fails off rather than on.

THE BEHAVIOUR THAT HAD FIVE HOMES (census 2026-08-12, `repo-lock.md` §8.2;
confirmed independently by the 2026-08-19 review, H-09). A declared-policy file
under `docs/` — `docs/subagent-gate` and the legacy one-word dials — states
ONE word, and every reader answers the same question: what is the first
line that is neither blank nor a comment? That question was answered by
`agent_common.read_declared`, `subagent_gate.read_declared`, and three separate
`_first_declared_line` copies in `bootstrap.py`, `check_privacy.py` and
`check_trajectory.py`. The copies carried a prose claim of equivalence that was
FALSE in two of the five, and `tests/test_rule_sync.py` had to pin them equal
by value to contain the drift.

`first_declared_line` below is that rule, stated once. The two other signatures
are kept as THIN ADAPTERS rather than harmonized away, because both of their
divergences are deliberate contracts their call sites depend on:

  * `read_declared(path, default)` substitutes a caller-supplied default for the
    absent/empty case instead of `None`.
  * `read_declared_lower(path)` lowercases and answers `""` — not `None` — for
    absent, so it composes with a closed, case-folded vocabulary without a
    None-check at every call site.

Making them adapters over one rule is what the pins were standing in for: the
copies can no longer disagree, so drift is UNREPRESENTABLE rather than detected.
"""

import sys
import tomllib
from pathlib import Path

__all__ = [
    "assumption_gate_enabled",
    "first_declared_line",
    "process_check",
    "process_check_text",
    "read_declared",
    "read_declared_lower",
    "utf8_console",
]


def first_declared_line(path):
    """The first non-empty, non-comment line of a declared-policy file, or None.

    None means NOTHING IS DECLARED — the file is absent, unreadable, empty, or
    holds only blanks and `#` comments. It never means "the file declares the
    empty string": a policy file with nothing to say and a policy file that does
    not exist are the same statement to every caller, which is why one sentinel
    covers both.

    Reads with `errors="replace"` and catches `OSError`, so an unreadable or
    mis-encoded dial degrades to "undeclared" rather than crashing a check —
    the fail-direction each caller then decides for itself.

    Contract:
      Inputs:  path: path-like to a declared-policy file (may not exist)
      Outputs: str | None — the declared token, stripped; None if undeclared
    """
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def process_check(root, key):
    """One `[checks]` toggle out of `docs/process.toml`, or None when that file
    has nothing to say about `key` (the caller falls through to its legacy
    one-word file — the SN-028 dual-read window).

    THE SECOND BEHAVIOUR THIS MODULE COLLECTS, and the copies' own stated reason
    for staying apart did not describe them. `check_trajectory._process_check`
    and `gen_okf._process_check` each argued that the `[checks]` POLICY — "which
    key, which fail-direction, which residual" — was the caller's and not a
    library's. Only the first of those three is the caller's, and it is a
    PARAMETER; the fail-direction and the residual were hardcoded identically in
    both bodies, so nothing module-specific was ever being encoded. What the
    duplication actually bought was a `tests/test_rule_sync.py` pin holding two
    identical bodies equal (WI-448 slice 4 retires it).

    `subagent_gate.read_process_policy` is deliberately NOT a third copy folded
    in here: its dial is a WORD, not a bool, and it answers a distinct
    `UNPARSEABLE` sentinel so `decide()` can fail closed. Same file, different
    question.

    A file that exists but does not parse, or a key whose value is not a bool,
    reads ON: a check that silently stops running is the failure worth avoiding,
    so the residual is loud rather than permissive.

    Contract:
      Inputs:  root: path-like repo root; key: the `[checks]` key to read
      Outputs: bool | None — the declared toggle; None if undeclared
    """
    path = Path(root) / "docs" / "process.toml"
    if not path.is_file():
        return None
    try:
        # utf-8-sig: a BOM is not legal TOML but is invisible to a shell read.
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return True  # unparseable but present: fail loud, never a quiet opt-out
    table = data.get("checks")
    value = table.get(key) if isinstance(table, dict) else None
    if value is None:
        return None
    return value if isinstance(value, bool) else True


def assumption_gate_enabled(docs):
    """Whether `[checks] assumption_gate` in `<docs>/process.toml` turns the
    assumption gate on: true only when the key reads `true`.

    THE THIRD FAIL-DIRECTION, and deliberately not `process_check`'s. That
    reader answers ON for a file it cannot parse, because the checks it
    toggles are on by default and a silent opt-out is the failure it guards
    against. This gate is OFF by default: it asks every requirement for a
    written argument, a cost a project opts into. So an absent file, an
    unparseable one, an absent key and any value but `true` all read off, and
    the gate's steps print their findings as advisories instead of failing.

    Implements: SR-205, LLR-242

    Contract:
      Inputs:  docs: path-like to the project's `docs/` directory
      Outputs: bool — True only for a readable `assumption_gate = true`
    """
    try:
        data = tomllib.loads(
            (Path(docs) / "process.toml").read_text(encoding="utf-8-sig")
        )
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return False
    table = data.get("checks")
    return isinstance(table, dict) and table.get("assumption_gate") is True


def process_check_text(root, key):
    """One text-valued `[checks]` key out of `docs/process.toml` — a commit id,
    say — or None when the file declares nothing for it.

    A SECOND READER BESIDE `process_check`, NOT A MODE OF IT, because the two
    fail in opposite directions. A toggle has a conservative answer to fall back
    on when it cannot be read (ON: the check keeps running). A declared text
    has none: a start commit the file meant but this reader cannot see is not
    "no start", and treating it as one would judge a different history than the
    one declared. So an unparseable file, or a value that is not a string,
    RAISES and the caller says what it could not do; it never guesses.

    An empty or blank string is the same statement as an absent key: the
    shipped template declares the key visibly at `""`, and that must read as
    "nothing declared" rather than as a value to act on.

    Contract:
      Inputs:  root: path-like repo root; key: the `[checks]` key to read
      Outputs: str | None — the declared text, stripped; None if undeclared
               or empty
      Raises:  ValueError — the file is present but does not parse, or the
               key holds something other than a string
    """
    path = Path(root) / "docs" / "process.toml"
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ValueError("{} does not parse: {}".format(path, exc)) from exc
    table = data.get("checks")
    value = table.get(key) if isinstance(table, dict) else None
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(
            "{} [checks] {} = {!r} is not a string".format(path, key, value)
        )
    return value.strip() or None


def read_declared(path, default):
    """`first_declared_line`, with `default` for the undeclared case.

    The reader for the LEGACY half of the SN-028 dual-read window; new policy
    reads go through `agent_common.declared_policy`, which prefers
    `docs/process.toml`.

    NOT A READER OF `docs/gate`, though this docstring said so until WI-498
    slice 4 (the gate schedule map's reader E). No call site has ever put it to
    that file — `docs/gate` is a deliberate NON-row in `PROCESS_KEYS`, and every
    live gate reader spelled its own one-line parse out locally. The function is
    unchanged and undeprecated; only the claim was false.

    Contract:
      Inputs:  path: path-like; default: value to answer when undeclared
      Outputs: str | type(default) — the declared token, else `default`
    """
    value = first_declared_line(path)
    return default if value is None else value


def read_declared_lower(path):
    """`first_declared_line` lowercased, with `""` for the undeclared case.

    The subagent-gate reader's contract: it compares the token against a closed,
    case-folded vocabulary and documents its own `policy` parameter as
    `"" = off`, so the empty string has to be the sentinel for it to compose
    without a None-check at every call site. Deliberate divergence, not a bug to
    harmonize away — and now expressed as an adapter over the shared rule rather
    than as a fifth copy of it.

    Contract:
      Inputs:  path: path-like to a declared-policy file (may not exist)
      Outputs: str — the declared token, lowercased; `""` if undeclared
    """
    return (first_declared_line(path) or "").lower()


def utf8_console():
    """Emit UTF-8 on stdout/stderr whatever the OS console codepage is.

    A non-ASCII work-item title, path or box-drawing character must not raise
    `UnicodeEncodeError` on a legacy Windows cp1252 console. Python 3.7+ streams
    expose `.reconfigure`; the guard covers a stream that does not (a captured
    or already-wrapped stream), where there is nothing to do and nothing to fail.

    Contract:
      Inputs:  none
      Outputs: None — best-effort, never raises
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
