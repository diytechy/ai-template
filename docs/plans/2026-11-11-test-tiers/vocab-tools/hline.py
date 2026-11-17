"""Apply hand edits addressed by line: each replaces text inside one line.

  python hline.py EDITS.py

EDITS.py defines LINES = [(relpath, line_no, old, new), ...]: in line
`line_no` (1-based) of `relpath`, every occurrence of `old` becomes `new`.
Nothing is written unless every `old` is found on its line. Line numbers are
those of the file as it stands when the edit file is applied, so an edit file
is written against one state of the tree and applied once. Added in the
§10.7 session (HANDOFF 9.11) for the long tail of one-word sense fixes, where
an exact-string edit per line would repeat the line.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    spec = importlib.util.spec_from_file_location("edits", sys.argv[1])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    texts, problems = {}, []
    for rel, number, old, new in mod.LINES:
        if rel not in texts:
            texts[rel] = (ROOT / rel).read_bytes().decode("utf-8").split("\n")
        lines = texts[rel]
        if number > len(lines) or old not in lines[number - 1]:
            problems.append("{}:{}: {!r} not on the line".format(rel, number, old))
            continue
        lines[number - 1] = lines[number - 1].replace(old, new)
    if problems:
        print("\n".join(problems))
        print("NOTHING WRITTEN")
        return 1
    for rel, lines in texts.items():
        (ROOT / rel).write_bytes("\n".join(lines).encode("utf-8"))
    print("{}: {} edit(s) in {} file(s)".format(Path(sys.argv[1]).name, len(mod.LINES), len(texts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
