"""Row M: for each finding, blame its first cited path:line at the reviewed sha (read-only git).

Prints, per finding: lane, file, finding index, cited site, the commit that last
changed that line, its author date and subject, and whether that commit is
pre-lane (an ancestor of trunk 45d867e51) or a lane commit, and whether it is
dated before or after the lane's first review round was filed.
Writes M/_regress.tsv.
"""
import json
import re
import subprocess
from pathlib import Path

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()  # run from the repository root
OUT = Path(__file__).resolve().parent
TRUNK = "45d867e51"
SITE = re.compile(r"((?:[\w.\-]+/)*[\w.\-]+\.(?:py|toml|md|json|cmd|sh|ps1|txt|ini)):(\d+)")


def git(*args, check=False):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    if check and r.returncode:
        raise RuntimeError(r.stderr.decode())
    return r.returncode, r.stdout.decode("utf-8", "replace")


def main():
    recs = json.load(open(OUT / "_files.json", encoding="utf-8"))
    lanes = {}
    for r in recs:
        lanes.setdefault(r["wi"], []).append(r)
    rows = []
    for wi, rs in lanes.items():
        rs = [r for r in rs if r["kind"] != "legacy-sol-review" or "848" not in wi]
        rs.sort(key=lambda r: (r["nnn"] or "", r["name"]))
        first = rs[0]
        _, fdate = git("log", "-1", "--format=%aI", first["reviewed"])
        fdate = fdate.strip()
        for r in rs:
            for i, f in enumerate(r["findings"], 1):
                m = SITE.search(f["text"])
                if not m:
                    rows.append([wi, r["path"], str(i), "-", "-", "-", "-", "-", "-"])
                    continue
                path, line = m.group(1), m.group(2)
                rc, out = git("blame", "--porcelain", "-L", f"{line},{line}", r["reviewed"], "--", path)
                if rc or not out:
                    rows.append([wi, r["path"], str(i), f"{path}:{line}", "blame-failed", "-", "-", "-", "-"])
                    continue
                sha = out.split()[0]
                _, meta = git("log", "-1", "--format=%aI%x09%s", sha)
                adate, subj = (meta.strip().split("\t", 1) + [""])[:2]
                anc = git("merge-base", "--is-ancestor", sha, TRUNK)[0] == 0
                # pre-lane if an ancestor of the reviewed sha's merge-base with trunk
                _, mb = git("merge-base", r["reviewed"], TRUNK)
                pre = git("merge-base", "--is-ancestor", sha, mb.strip())[0] == 0
                where = "pre-lane" if pre else ("lane" if not anc else "lane(landed)")
                when = "-" if pre else ("before-first-review" if adate < fdate else "after-first-review")
                rows.append([wi, r["path"], str(i), f"{path}:{line}", sha[:9], adate, where, when, subj[:150]])
    (OUT / "_regress.tsv").write_text("\n".join("\t".join(x) for x in rows), encoding="utf-8")
    for x in rows:
        print(" | ".join(x))


if __name__ == "__main__":
    main()
