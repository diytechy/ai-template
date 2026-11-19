"""Rename Python names by token, never inside a string or a comment.

  python pyname.py NAMES.py [--dry] [--review OUT.txt]

NAMES.py defines NAMES = [(relpath, {old: new}, lines), ...]. `lines` is None
for the whole file, or a (first, last) pair of 1-based line numbers the
rename is limited to. Only `tokenize.NAME` tokens equal to `old` change: an
attribute (`x.bar`), a parameter, a keyword argument and a local alike, and
nothing a sweep of text would also reach (a docstring, a message, a comment).
Added in the sixth vocabulary concept (HANDOFF 9.10), for locals such as
`attested` and the trailer field `bar`, which share their spelling with prose
and with other senses of the word in the same files.

Every changed line is written to the review file as old/new pairs, in
vapply's format.
"""

import importlib.util
import io
import sys
import tokenize
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rename(text, mapping, span):
    """`(new text, [(line no, old line, new line)])` for one file."""
    edits = {}
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type != tokenize.NAME or tok.string not in mapping:
            continue
        row, col = tok.start
        if span and not span[0] <= row <= span[1]:
            continue
        edits.setdefault(row, []).append((col, tok.string, mapping[tok.string]))
    lines = text.split("\n")
    hits = []
    for row, cuts in sorted(edits.items()):
        line = lines[row - 1]
        new = line
        for col, old, repl in sorted(cuts, reverse=True):
            assert new[col : col + len(old)] == old, (row, col, old)
            new = new[:col] + repl + new[col + len(old) :]
        hits.append((row, line, new))
        lines[row - 1] = new
    return "\n".join(lines), hits


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    review = Path(args[args.index("--review") + 1]) if "--review" in args else None
    spec = importlib.util.spec_from_file_location("names", args[0])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    log, files, total = [], 0, 0
    for rel, mapping, span in mod.NAMES:
        path = ROOT / rel
        text = path.read_bytes().decode("utf-8")
        new, hits = rename(text, mapping, span)
        if not hits:
            print("NO CHANGE: {} {}".format(rel, sorted(mapping)))
            continue
        files += 1
        total += len(hits)
        log.append("=== {} ({})".format(rel, len(hits)))
        for row, old, repl in hits:
            log.append("{}:{}".format(rel, row))
            log.append("  - " + old.strip())
            log.append("  + " + repl.strip())
        if not dry:
            path.write_bytes(new.encode("utf-8"))
    if review:
        review.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("{}: {} file(s), {} line(s){}".format(
        Path(args[0]).name, files, total, " (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
