"""Apply hand edits: exact strings, each asserted to occur the stated number of times.

  python hand.py EDITS.py

EDITS.py defines EDITS = [(relpath_or_glob_list, old, new[, count]), ...].
A relpath may be a tuple of paths: the same edit is applied to each (mirrors).
Nothing is written unless every edit in the file matches as stated.
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
    for n, edit in enumerate(mod.EDITS, 1):
        rels, old, new = edit[0], edit[1], edit[2]
        count = edit[3] if len(edit) > 3 else 1
        if isinstance(rels, str):
            rels = (rels,)
        for rel in rels:
            if rel not in texts:
                texts[rel] = (ROOT / rel).read_bytes().decode("utf-8")
            found = texts[rel].count(old)
            if found != count:
                problems.append(
                    "edit {} in {}: expected {} match(es), found {}: {!r}".format(
                        n, rel, count, found, old[:70]
                    )
                )
                continue
            texts[rel] = texts[rel].replace(old, new)
    if problems:
        print("\n".join(problems))
        print("NOTHING WRITTEN")
        return 1
    for rel, text in texts.items():
        (ROOT / rel).write_bytes(text.encode("utf-8"))
    print("{}: {} edit(s) in {} file(s)".format(Path(sys.argv[1]).name, len(mod.EDITS), len(texts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
