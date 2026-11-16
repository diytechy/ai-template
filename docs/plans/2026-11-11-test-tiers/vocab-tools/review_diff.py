"""Compare two vapply review files for the same rule file.

  python review_diff.py FIRST.txt SECOND.txt

Prints the lines the second run no longer changes, the lines it newly
changes, and the lines whose result differs, each with its new text. This is
what to read after refining a rule file, instead of the whole review again.
"""

import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load(path):
    out, lines, i = {}, open(path, encoding="utf-8").read().split("\n"), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("=== ") or not line or line.startswith("  "):
            i += 1
            continue
        out[line] = (lines[i + 1][4:], lines[i + 2][4:])
        i += 3
    return out


a, b = load(sys.argv[1]), load(sys.argv[2])
for key in sorted(set(a) - set(b)):
    print("DROPPED {}: {}".format(key, a[key][0][:160]))
for key in sorted(set(b) - set(a)):
    print("ADDED   {}: {}".format(key, b[key][1][:160]))
for key in sorted(set(a) & set(b)):
    if a[key][1] != b[key][1]:
        print("CHANGED {}: {}".format(key, b[key][1][:200]))
