"""Inventory of old-word tokens on the LIVE surface of the vocabulary worktree.

Usage:
  python inv.py tokens STEM [STEM...]     distinct tokens holding a stem, by area
  python inv.py files  REGEX              per-file counts of a regex (live files)
  python inv.py lines  REGEX [PATHGLOB]   matching lines, file:line: text
  python inv.py areas                     file counts per area

"Live" is check_vocab.in_scope's answer, so records are left out exactly where
the kit's own vocabulary check leaves them out.
"""

import fnmatch
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Projects\ai-template-wt-vocabulary")
sys.path.insert(0, str(ROOT / "project-trajectory" / "scripts"))
import check_vocab  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*")


def area(rel):
    if rel.startswith("project-trajectory/scripts/"):
        return "kit-scripts"
    if rel.startswith("scripts/"):
        return "repo-scripts"
    if rel.startswith("tests/"):
        return "tests"
    if rel.startswith("project-trajectory/"):
        return "kit-prose"
    if rel.startswith(("docs/requirements/", "docs/test/")):
        return "registries"
    if rel.startswith((".claude/", ".agents/")):
        return "skill-mirrors"
    if rel.startswith("docs/"):
        return "repo-docs"
    return "root"


sys.path.insert(0, str(Path(__file__).parent))
from common import RECORDS  # noqa: E402

LEAVE = tuple(RECORDS) + ("project-trajectory/RESYNC_PACK.md", "docs/plans/*", "PROJECT_STATE.html")


def _left(rel):
    for g in LEAVE:
        if fnmatch.fnmatch(rel, g) or (g.endswith("/*") and rel.startswith(g[:-1])):
            return True
    return False


def snippets(regex, glob=None, width=70):
    """Each match with `width` characters either side: for long registry cells."""
    pat = re.compile(regex)
    n = 0
    for rel, path in live_files():
        if glob and not fnmatch.fnmatch(rel, glob):
            continue
        for i, line in enumerate(read(path).split("\n"), 1):
            for m in pat.finditer(line):
                n += 1
                a, b = max(0, m.start() - width), min(len(line), m.end() + width)
                print("{}:{}: ...{}...".format(rel, i, line[a:b]))
    print("# matches={}".format(n))


def live_files():
    for rel, path in _all_live():
        if not _left(rel):
            yield rel, path


def _all_live():
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout.splitlines()
    for rel in out:
        path = ROOT / rel
        if not path.is_file():
            continue
        if path.name in ("OWNER_SCRATCHPAD.md", "OPERATOR_SCRATCHPAD.md"):
            continue
        _, reason = check_vocab.in_scope(path, ROOT)
        if reason == "LIVE":
            yield rel, path


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def cmd_tokens(stems):
    pat = re.compile("|".join(re.escape(s) for s in stems), re.I)
    by_area = defaultdict(Counter)
    for rel, path in live_files():
        a = area(rel)
        for tok in TOKEN_RE.findall(read(path)):
            if pat.search(tok):
                by_area[a][tok] += 1
    total = Counter()
    for c in by_area.values():
        total.update(c)
    areas = sorted(by_area)
    print("token\ttotal\t" + "\t".join(areas))
    for tok, n in sorted(total.items(), key=lambda kv: (-kv[1], kv[0])):
        print("{}\t{}\t{}".format(tok, n, "\t".join(str(by_area[a][tok]) for a in areas)))
    print("# distinct={} occurrences={}".format(len(total), sum(total.values())))


def cmd_files(regex):
    pat = re.compile(regex)
    rows = []
    for rel, path in live_files():
        n = len(pat.findall(read(path)))
        if n:
            rows.append((n, rel))
    for n, rel in sorted(rows, reverse=True):
        print("{}\t{}".format(n, rel))
    print("# files={} occurrences={}".format(len(rows), sum(n for n, _ in rows)))


def cmd_lines(regex, glob=None):
    pat = re.compile(regex)
    n = 0
    for rel, path in live_files():
        if glob and not fnmatch.fnmatch(rel, glob):
            continue
        for i, line in enumerate(read(path).split("\n"), 1):
            if pat.search(line):
                n += 1
                print("{}:{}: {}".format(rel, i, line.strip()[:220]))
    print("# lines={}".format(n))


def cmd_areas():
    c = Counter(area(rel) for rel, _ in live_files())
    for a, n in sorted(c.items()):
        print("{}\t{}".format(a, n))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "tokens":
        cmd_tokens(sys.argv[2:])
    elif cmd == "files":
        cmd_files(sys.argv[2])
    elif cmd == "lines":
        cmd_lines(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "areas":
        cmd_areas()
    elif cmd == "snip":
        snippets(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
