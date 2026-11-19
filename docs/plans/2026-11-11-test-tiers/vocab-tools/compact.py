"""Compact a vapply review file: each changed span with a little context.

  python compact.py REVIEW.txt [WIDTH] > OUT.txt

One line per change: `file:line: ...before[old -> new]after...`. Lines whose
changes are all identical to an earlier (old -> new) pair in the same file are
still listed, so nothing is hidden; long registry rows shrink to their edits.
"""

import difflib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOK = re.compile(r"\w+|\W")


def spans(old, new, width):
    a, b = TOK.findall(old), TOK.findall(new)
    out = []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        pre = "".join(a[:i1])[-width:]
        post = "".join(a[i2:])[:width]
        out.append("{}[{} -> {}]{}".format(pre, "".join(a[i1:i2]), "".join(b[j1:j2]), post))
    return out


def main():
    path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("=== ") or not line or line.startswith("  "):
            i += 1
            continue
        loc = line
        old = lines[i + 1][4:] if i + 1 < len(lines) else ""
        new = lines[i + 2][4:] if i + 2 < len(lines) else ""
        for s in spans(old, new, width):
            print("{}: {}".format(loc, s))
        i += 3


main()
