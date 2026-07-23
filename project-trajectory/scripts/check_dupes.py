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
records it one entry per line (# comments fine). Two entry forms are honored:

  * FINGERPRINTED (preferred) — "<fp>  a.py == b.py": a 12-hex block fingerprint
    (a hash of the duplicated tokens, line-number-free) followed by the pair.
    It sanctions THAT block in THAT pair; NEW copy-paste between the same two
    files gets a different fingerprint and so is NOT exempt — it fails until a
    deliberate census line is added. Regenerate the fingerprints with
    --emit-census (WI-276).
  * BARE PAIR (legacy, coarse) — "a.py == b.py": the whole file pair is
    exempt, so any later duplication between the two files passes automatically.
    Kept for backward compatibility; prefer the fingerprinted form.

Both forms match the finding's POSIX pair as a substring, so an allowed pair
stays allowed as the files grow. Exit: 0 clean (or all findings allowlisted);
1 with one line per duplicated block naming both file:line locations, its length,
and the census line that would sanction it.

Contracts: IF-007, IF-027 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

from __future__ import annotations

import argparse
import hashlib
import re
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

# Length of the hex block fingerprint recorded in the census (WI-276). 12 hex =
# 48 bits: collision-free at the hundreds-of-blocks scale a real census reaches,
# short enough to stay readable on a census line. A fingerprint keys the block's
# COMPLETE normalized (kind, text) token signature — every token in the merged
# block, not merely its first window — line-number-free (survives the files
# growing) but fully content-sensitive, so new or edited copy-paste between an
# already-listed pair changes the fingerprint and is no longer exempt.
_FP_LEN = 12
_FP_RE = re.compile(r"^[0-9a-f]{%d}$" % _FP_LEN)


def fingerprint(block):
    """Stable 12-hex fingerprint of a duplicated block's COMPLETE normalized
    token signature — every (kind, text) token in the merged block, not merely
    its first --min-tokens window. A first-window-plus-extent hash collided
    whenever two blocks shared their opening window and total token count but
    diverged after it, silently exempting the changed copy from the census
    (WI-276 rework); hashing the whole sequence closes that hole. Deterministic
    across runs and OSes (a hash of a repr of str pairs) and independent of line
    numbers, whitespace, and comments (those never enter the signature)."""
    payload = repr(tuple(block)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:_FP_LEN]


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
    """(kind, text, line) for each significant token in the file, or None when
    the file can't be tokenized (unterminated string/bracket, bad coding
    cookie, non-UTF-8). A lint surfaces bad input, never crashes on it — the
    kit's own convention (gen_arch_map catches SyntaxError).

    `kind` is the token-type NAME (tokenize.tok_name[...]), not its integer id:
    the integers are not stable across Python releases (e.g. OP is 54 on 3.11
    and 55 on 3.12), so hashing them would make a fingerprint census generated
    on one interpreter fail on another (the gate job may run a newer Python than
    a developer). The names ("OP", "NAME", "STRING", …) are stable, so the
    fingerprint is portable across the version matrix (WI-276)."""
    try:
        with open(path, "rb") as handle:
            return [
                (tokenize.tok_name[tok.type], tok.string, tok.start[0])
                for tok in tokenize.tokenize(handle.readline)
                if tok.type not in _INSIGNIFICANT
            ]
    except (tokenize.TokenError, SyntaxError, UnicodeDecodeError) as exc:
        print(
            "check_dupes: WARN - {}: could not tokenize ({}); skipped".format(
                Path(path).as_posix(), exc
            ),
            file=sys.stderr,
        )
        return None


def _windows(tokens, min_tokens):
    """Hashable min_tokens-wide windows with their source line and token offset."""
    signature = [(kind, text) for kind, text, _line in tokens]
    for i in range(len(signature) - min_tokens + 1):
        yield tuple(signature[i : i + min_tokens]), tokens[i][2], i


def find_duplicates(files, min_tokens):
    """Duplicated blocks across the given files.

    Returns a sorted list of ((file_a, line_a), (file_b, line_b), token_len, fp)
    with overlapping windows of the same duplicate merged, so one lifted
    helper reports once, not once per sliding-window offset. `fp` is the block's
    fingerprint() (line-number-free hash of its COMPLETE token signature), used
    to key census exemptions to a specific block, not the whole file pair, and
    to catch edits anywhere in the block, not just its prefix or extent (WI-276).
    """
    seen = {}  # window -> (file, line, token offset) of first occurrence
    # (file_a, file_b) -> {line_a - line_b -> hits}: preserve the established
    # line-offset grouping for the census. Each hit also carries its token
    # offsets: line offsets find candidate regions, but only step-1 token
    # offsets prove that two sliding windows are one overlapping block.
    pairs = {}
    for path in files:
        toks = significant_tokens(path)
        if toks is None:
            continue  # un-tokenizable file — warned, skipped (A1)
        for window, line, token_offset in _windows(toks, min_tokens):
            if window in seen:
                first_file, first_line, first_offset = seen[window]
                if (first_file, first_offset) == (path, token_offset):
                    continue  # a repeated window inside one physical block
                key = (first_file, path)
                pairs.setdefault(key, {}).setdefault(first_line - line, []).append(
                    (first_line, line, first_offset, token_offset, window)
                )
            else:
                seen[window] = (path, line, token_offset)
    findings = []
    for (file_a, file_b), by_offset in pairs.items():
        for hits in by_offset.values():
            # Split a line-offset group into genuinely overlapping step-1 token
            # runs. This keeps two separate expressions on the same line from
            # sharing a merged signature/census fingerprint.
            for run in _contiguous_runs(sorted(hits, key=lambda h: (h[2], h[3]))):
                line_a, line_b, _offset_a, _offset_b, _first_window = run[0]
                # Window count approximates extent: N overlapping windows span
                # roughly min_tokens + N - 1 tokens.
                length = min_tokens + len(run) - 1
                fp = fingerprint(_merged_signature(run))
                findings.append(((file_a, line_a), (file_b, line_b), length, fp))
    return sorted(findings)


def _merged_signature(run):
    """The full (kind, text) token signature of a merged duplicated block,
    reconstructed from its overlapping windows: the first window in full, then
    the single new trailing token each subsequent step-1 window contributes.
    find_duplicates appends a pair's windows in the scanned file's token order
    and the (line_a, line_b) sort is stable, so `run` is in token order and this
    yields the block's exact token sequence (length min_tokens + len(run) - 1).
    Fingerprinting THIS — every token, not just run[0]'s window — makes the
    census key change on any interior or trailing edit, not only a prefix or
    extent edit (WI-276)."""
    first_window = run[0][4]
    return tuple(first_window) + tuple(hit[4][-1] for hit in run[1:])


def _contiguous_runs(hits):
    """Split one token-offset group at every non-overlapping window boundary.

    `hits` holds (line_a, line_b, token_a, token_b, window) tuples sorted by
    token offsets. Consecutive sliding windows overlap only when BOTH starts
    advance exactly one token; line adjacency is neither required nor enough.
    """
    run = []
    for pair in hits:
        if run and (pair[2] != run[-1][2] + 1 or pair[3] != run[-1][3] + 1):
            yield run
            run = []
        run.append(pair)
    if run:
        yield run


def _canonical_pair(text):
    """`a == b` with each side stripped, so a census pair matches a finding's
    pair regardless of incidental spacing around the `==`."""
    left, _, right = text.partition("==")
    return "{} == {}".format(left.strip(), right.strip())


def read_allowlist(path):
    """Parse the census into (fingerprint_or_None, pair) entries, one per
    non-comment line (blanks and # comments skipped), or [].

    A line whose first whitespace-delimited token is a 12-hex fingerprint and
    whose remainder holds a "==" pair is a FINGERPRINTED entry — it sanctions
    ONE block of that fingerprint in that (canonicalized, exact) pair; listing
    the same fingerprint+pair N times sanctions N identical copies. Any other
    line is a legacy BARE-PAIR entry (fingerprint None) that coarsely sanctions
    the whole file pair as a substring, so it survives the files growing."""
    if not path.exists():
        return []
    entries = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split(None, 1)
        head = parts[0]
        rest = parts[1].strip() if len(parts) > 1 else ""
        if _FP_RE.match(head) and "==" in rest:
            entries.append((head, _canonical_pair(rest)))
        else:
            entries.append((None, s))
    return entries


def unallowed(findings, entries):
    """The findings NOT sanctioned by the census, in order.

    Count-aware (WI-276): each fingerprinted entry sanctions ONE matching block,
    so N census lines for the same fingerprint+pair sanction exactly N identical
    copies — an (N+1)th copy between an already-listed pair is reported, closing
    the "growth inside a trusted pair passes automatically" hole. A legacy
    bare-pair entry matches any block in the pair (substring) and is never
    consumed. Each finding is (posix_pair, length, fp, file_a, line_a, file_b,
    line_b).
    """
    budget = {}  # (fp, pair) -> remaining sanctioned copies
    bare = []
    for entry_fp, entry_pair in entries:
        if entry_fp is None:
            bare.append(entry_pair)
        else:
            budget[(entry_fp, entry_pair)] = budget.get((entry_fp, entry_pair), 0) + 1
    out = []
    for finding in findings:
        (file_a, line_a), (file_b, line_b), length, fp = finding
        file_a, file_b = Path(file_a).as_posix(), Path(file_b).as_posix()
        pair = "{} == {}".format(file_a, file_b)
        if any(sub in pair for sub in bare):
            continue  # legacy coarse pair exemption
        key = (fp, pair)
        if budget.get(key, 0) > 0:
            budget[key] -= 1
            continue  # a recorded copy of this block
        out.append((pair, length, fp, file_a, line_a, file_b, line_b))
    return out


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII path / title / registry cell can't raise UnicodeEncodeError on a
    legacy Windows cp1252 console (verbatim across the
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
        help="census file; each line is a '<fp>  a.py == b.py' fingerprinted "
        "entry or a legacy bare 'a.py == b.py' pair, matched against the "
        "finding's line-number-free form (default {})".format(ALLOWLIST),
    )
    parser.add_argument(
        "--emit-census",
        action="store_true",
        help="print a fingerprinted census line ('<fp>  a.py == b.py') for "
        "every duplicated block and exit 0 — the census-regeneration workflow: "
        "review the lines and keep the sanctioned ones (WI-276)",
    )
    args = parser.parse_args(argv)
    files = sorted(Path(args.src).rglob("*.py"))
    findings = find_duplicates(files, args.min_tokens)

    if args.emit_census:
        for (file_a, _la), (file_b, _lb), _length, fp in findings:
            file_a, file_b = Path(file_a).as_posix(), Path(file_b).as_posix()
            print("{}  {} == {}".format(fp, file_a, file_b))
        return 0

    entries = read_allowlist(Path(args.allowlist))
    failures = unallowed(findings, entries)
    for pair, length, fp, file_a, line_a, file_b, line_b in failures:
        # POSIX-normalized in the finding AND the census match, so one recorded
        # pair holds on Windows and Linux alike.
        print(
            "check_dupes: duplicate block (~{} tokens): {}:{} == {}:{}".format(
                length, file_a, line_a, file_b, line_b
            ),
            file=sys.stderr,
        )
        # The exact census line that would sanction this block — paste it into
        # docs/dupes-allow to make the exemption a deliberate baseline change.
        print(
            "check_dupes:   sanction with census line:  {}  {}".format(fp, pair),
            file=sys.stderr,
        )
    if failures:
        return 1
    print("check_dupes: OK - no duplicate blocks in {} file(s).".format(len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
