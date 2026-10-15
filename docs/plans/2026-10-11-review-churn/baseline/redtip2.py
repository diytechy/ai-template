"""Row M: per review round, the lane's own test report nearest the reviewed sha (read-only git).

Walks back from the reviewed sha (first-parent) until a commit message carries a
test report (smoke/passed/failed), listing the intermediate commits and whether
any of them touched code (a path outside docs/, telemetry and registries).
Writes M/_redtip2.tsv.
"""
import json
import re
import subprocess
from pathlib import Path

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()  # run from the repository root
OUT = Path(__file__).resolve().parent
REPORT = re.compile(r"(smoke|Smoke)[^\n]*?(\d+\s+passed|\d+\s+failed)|(\d+\s+failed)|Verified[^\n]*smoke", re.S)
NONCODE = re.compile(r"^(docs/|PROJECT_STATE\.html$|\.claude/telemetry|docs/log)")


def git(*args):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def main():
    recs = json.load(open(OUT / "_files.json", encoding="utf-8"))
    rows = []
    for r in recs:
        shas = git("rev-list", "--first-parent", "-15", r["reviewed"]).split()
        inter, found = [], None
        for s in shas:
            msg = git("log", "-1", "--format=%B", s)
            subj = msg.splitlines()[0] if msg else ""
            m = [l.strip() for l in msg.splitlines() if re.search(r"(\d+\s+passed|\d+\s+failed)", l) and re.search(r"(?i)smoke|verified|focused|re-run|passed", l)]
            if m:
                found = (s[:9], subj[:90], " | ".join(m)[:300])
                break
            files = git("diff-tree", "--no-commit-id", "--name-only", "-r", s).split()
            code = [f for f in files if not NONCODE.match(f)]
            inter.append(f"{s[:9]}{'*' if code else ''}:{subj[:60]}")
        rows.append([r["path"][13:], r["reviewed"][:9], r["verdict"], str(r["findings_n"]),
                     found[0] if found else "-", found[1] if found else "-", found[2] if found else "-",
                     " ; ".join(inter)])
    (OUT / "_redtip2.tsv").write_text("\n".join("\t".join(x) for x in rows), encoding="utf-8")
    for x in rows:
        print(" || ".join(x))


if __name__ == "__main__":
    main()
