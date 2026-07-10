#!/usr/bin/env python3
"""Duplicate-code lint — copy-paste blocks violate one-fact-one-home (Thread 53).

An OPT-IN, product-layer harness step (stdlib-only, adapted from the proven
gilbert detector): tokenizes every Python source under --src and reports any
window of --min-tokens consecutive *significant* tokens (comments, blank lines,
and indentation excluded) that appears at more than one location. Copy-paste is
the failure mode this guards (the AGENTS working agreement: "one fact, one home
— in code too"); renamed-identifier near-duplicates are out of scope — exact
token equality keeps the check fast, deterministic, and free of false positives
worth arguing with.

Opt in per repo via a stack-profile step (docs/stack.ini — survives re-sync):

    [step:dupes]
    command = {py} scripts/check_dupes.py --src {src}

The tokenizer is the Python reference — swap it for your stack like the rest of
the harness. Legitimate repetition is allowlisted, not fought: docs/dupes-allow
holds one substring per line (# comments fine), matched against the finding's
line-number-free form ("a.py == b.py"), so an allowed pair stays allowed as the
files grow. Exit: 0 clean (or all findings allowlisted); 1 with one line per
duplicated block naming both file:line locations and the block length.
"""

from __future__ import annotations

import argparse
import sys
import tokenize
from pathlib import Path

# Shortest duplicated run worth failing on, in significant tokens — the
# --min-tokens default. Tuned upstream (gilbert): a canonical lifted helper
# (a copy-pasted _load_csv-style function) measures ~38 significant tokens, so
# 30 catches it with margin, while idiomatic repetition — import blocks,
# dataclass field lists, argparse boilerplate — stays under the bar.
MIN_TOKENS = 30

ALLOWLIST = "docs/dupes-allow"

# Token types that carry no duplicated *logic*: layout, comments, and the
# encoding/EOF bookkeeping tokens. NEWLINE (logical line end) is kept so a
# window can't stitch unrelated statements into a phantom duplicate — dropped
# NEWLINEs would let "end of one function + start of the next" look identical
# across files that merely share adjacent short functions.
_INSIGNIFICANT = {
    tokenize.COMMENT,
    tokenize.NL,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.ENCODING,
    tokenize.ENDMARKER,
}


def significant_tokens(path):
    """(kind, text, line) for each significant token in the file, in order."""
    with open(path, "rb") as handle:
        return [
            (tok.type, tok.string, tok.start[0])
            for tok in tokenize.tokenize(handle.readline)
            if tok.type not in _INSIGNIFICANT
        ]


def _windows(tokens, min_tokens):
    """Hashable min_tokens-wide windows keyed to their starting line."""
    signature = [(kind, text) for kind, text, _line in tokens]
    for i in range(len(signature) - min_tokens + 1):
        yield tuple(signature[i : i + min_tokens]), tokens[i][2]


def find_duplicates(files, min_tokens):
    """Duplicated blocks across the given files.

    Returns a sorted list of ((file_a, line_a), (file_b, line_b), token_len)
    with overlapping windows of the same duplicate merged, so one lifted
    helper reports once, not once per sliding-window offset.
    """
    seen = {}  # window -> (file, line) of first occurrence
    # (file_a, file_b) -> {line_a - line_b offset -> [(line_a, line_b)]}:
    # windows from one duplicated block share their line offset, so grouping
    # by offset merges the sliding-window hits into a single finding.
    pairs = {}
    for path in files:
        for window, line in _windows(significant_tokens(path), min_tokens):
            if window in seen:
                first_file, first_line = seen[window]
                if (first_file, first_line) == (path, line):
                    continue  # a repeated window inside one physical block
                key = (first_file, path)
                pairs.setdefault(key, {}).setdefault(first_line - line, []).append(
                    (first_line, line)
                )
            else:
                seen[window] = (path, line)
    findings = []
    for (file_a, file_b), by_offset in pairs.items():
        for hits in by_offset.values():
            line_a, line_b = min(hits)
            # Window count approximates extent: N overlapping windows span
            # roughly min_tokens + N - 1 tokens.
            length = min_tokens + len(hits) - 1
            findings.append(((file_a, line_a), (file_b, line_b), length))
    return sorted(findings)


def read_allowlist(path):
    """Substring patterns (one per line, # comments and blanks skipped), or []."""
    if not path.exists():
        return []
    return [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII path / title / registry cell can't raise UnicodeEncodeError on a
    legacy Windows cp1252 console (REVIEW_GRIND_FULL C5; verbatim across the
    kit). Python 3.7+ streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argv=None) -> int:
    _utf8_console()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--src", default="src", help="source root to scan")
    parser.add_argument(
        "--min-tokens",
        type=int,
        default=MIN_TOKENS,
        help="shortest duplicated run that fails, in significant tokens "
        "(default {})".format(MIN_TOKENS),
    )
    parser.add_argument(
        "--allowlist",
        default=ALLOWLIST,
        help="allowlist file; substrings matched against the finding's "
        "line-number-free 'a.py == b.py' form (default {})".format(ALLOWLIST),
    )
    args = parser.parse_args(argv)
    files = sorted(Path(args.src).rglob("*.py"))
    allowed = read_allowlist(Path(args.allowlist))
    failures = 0
    for (file_a, line_a), (file_b, line_b), length in find_duplicates(
        files, args.min_tokens
    ):
        # POSIX-normalized in the finding AND the allowlist match, so one
        # recorded pair holds on Windows and Linux alike.
        file_a, file_b = Path(file_a).as_posix(), Path(file_b).as_posix()
        pair = "{} == {}".format(file_a, file_b)
        if any(pat in pair for pat in allowed):
            continue  # recorded-legitimate repetition (docs/dupes-allow)
        failures += 1
        print(
            "check_dupes: duplicate block (~{} tokens): {}:{} == {}:{}".format(
                length, file_a, line_a, file_b, line_b
            ),
            file=sys.stderr,
        )
    if failures:
        return 1
    print("check_dupes: OK - no duplicate blocks in {} file(s).".format(len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
