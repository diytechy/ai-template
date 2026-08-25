"""The best-effort-off-git subprocess pattern — one home for "git, or None".

Most of the kit's git reads are ENRICHMENT, not gating: a commit clock behind a
staleness warn, a short SHA in a stamp, the branch behind a status line. Every
one of them must degrade to "I don't know" rather than crash, because the kit
has to run in three environments where git legitimately answers nothing — no
git binary on PATH, a directory that is not a repository (a tarball adopter,
a scaffold before its first `git init`), and a shallow or detached checkout
where the rev exists but the history does not.

`git_out` is that degrade, stated once. It was copied into `check.py`,
`trace.py` and `trunk_step.py`, each carrying a docstring that pointed at the
others as the pattern's home — three homes and no owner, which is the shape D-8
(`OI-16`) retired. A FOURTH copy survived that pass and is folded in here at
WI-521 slice 1: `check_trajectory._git`, which was the same body plus an
optional `stdin`. The `stdin` argument is the whole reason it was missed — it
looked like a different function — so it is a parameter here rather than a
private variant, and both readers of it (`check_trajectory`, `acceptance_record`)
now alias this one home the way `check.py` already did.

WHAT THIS MODULE DELIBERATELY DOES NOT DO: it never decides what an absent
answer MEANS. `None` is "git had nothing to say"; whether that is benign (skip
the enrichment) or fatal (a gate that requires history) is the caller's
fail-direction to declare, and folding that choice in here would hide it.
"""

import subprocess

__all__ = ["git_out"]


def git_out(root, args, stdin=None):
    """stdout of `git -C <root> <args>`, or None on ANY failure.

    None covers all of: no git binary (`OSError`), a bad argument vector
    (`ValueError`), not a repository, an unknown rev or path, and any non-zero
    exit. Decoded as UTF-8 with `errors="replace"`, so a commit message or path
    in another encoding degrades to replacement characters instead of raising
    inside a check that only wanted a SHA.

    `stdin` feeds a BATCH command — `cat-file --batch-check` is the live caller
    — which is how a scan asks about many blobs in ONE subprocess instead of two
    per file. It matters where the scan rides an always-on floor rather than a
    gate. `None` (the default) passes nothing, which is byte-for-byte the
    no-input behaviour every other caller already had.

    Not a security boundary and not a general git wrapper: `args` is passed as
    a list to a non-shell `subprocess.run`, so nothing here interpolates into a
    shell, but a caller passing attacker-controlled `args` owns that choice.

    Contract:
      Inputs:  root: path-like repo root; args: sequence of git arguments;
               stdin: str | None — batch input, or nothing
      Outputs: str | None — stdout on success; None on any failure
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            input=stdin,
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None
