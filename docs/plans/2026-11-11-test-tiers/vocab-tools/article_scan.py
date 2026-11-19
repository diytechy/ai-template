"""Find "a" / "A" ending one line with a vowel-sound word opening the next.

  python article_scan.py WORD [WORD...]      e.g. operator acceptance

The article rule in a rule file works line by line, so "needs a\\n  human)"
became "needs a\\n  operator)". This lists every such pair in the files git
reports as changed, so each can be fixed by hand.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fix = "--fix" in sys.argv
words = [w for w in sys.argv[1:] if w != "--fix"] or ["operator"]
END = re.compile(r"(?<![A-Za-z0-9_'])([Aa])\s*(?:\x22|')?\s*$")
START = re.compile(
    r"^[\s#>*\x22'`(/-]*(?:REM\s+)?[\x22']?\s*(?:" + "|".join(words) + r")\b",
    re.I,
)

changed = subprocess.run(
    ["git", "-C", str(ROOT), "diff", "--name-only"],
    capture_output=True, text=True, encoding="utf-8", check=True,
).stdout.splitlines()
n = 0
for rel in changed:
    path = ROOT / rel
    if not path.is_file():
        continue
    try:
        lines = path.read_text(encoding="utf-8").split("\n")
    except UnicodeDecodeError:
        continue
    hit = False
    for i in range(len(lines) - 1):
        m = END.search(lines[i])
        if m and START.search(lines[i + 1]):
            n += 1
            hit = True
            if fix:
                a = m.start(1)
                lines[i] = lines[i][:a] + lines[i][a] + "n" + lines[i][a + 1 :]
            print("{}:{}: {!r}".format(rel, i + 1, lines[i][-40:]))
            print("{}:{}: {!r}".format(rel, i + 2, lines[i + 1][:60]))
    if fix and hit:
        path.write_bytes("\n".join(lines).encode("utf-8"))
print("# pairs={}{}".format(n, " (fixed)" if fix else ""))
