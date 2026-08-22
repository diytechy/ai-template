"""Declared-policy files and console encoding — the kit's one declared-line rule.

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
from pathlib import Path

__all__ = [
    "first_declared_line",
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
