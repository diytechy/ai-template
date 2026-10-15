"""Row M: list each cohort lane's dispute files and adjudication rulings (read-only git).

Writes M/_disputes.txt and M/_adjudications.json.
"""
import json
import re
import subprocess
from pathlib import Path

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()  # run from the repository root
OUT = Path(__file__).resolve().parent
TRUNK = "45d867e51"
LANE_REFS = {"wi-798": "9437d0a1f", "wi-902": "d3d301216"}


def git(*args):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def main():
    recs = json.load(open(OUT / "_files.json", encoding="utf-8"))
    slugs = sorted({(r["slug"], r["ref"]) for r in recs})
    lines, adj = [], []
    for slug, ref in slugs:
        names = git("ls-tree", "--name-only", ref, f"docs/reviews/{slug}/").split()
        for p in names:
            n = p.rsplit("/", 1)[-1]
            if n.endswith("DISPUTE-findings.toml"):
                t = git("show", f"{ref}:{p}")
                rng = re.search(r'^range\s*=\s*"([^"]+)"', t, re.M)
                lines.append(f"## {p} range={rng.group(1) if rng else '?'}")
                for blk in re.split(r"^\[\[finding\]\]\s*$", t, flags=re.M)[1:]:
                    fid = re.search(r'^id\s*=\s*"([^"]+)"', blk, re.M)
                    held = re.search(r'^held_by\s*=\s*"([^"]+)"', blk, re.M)
                    fm = re.search(r"finding\s*=\s*'''\s*(.*?)'''", blk, re.S)
                    ftxt = " ".join(fm.group(1).split())[:220] if fm else ""
                    lines.append(f"  {fid.group(1) if fid else '?'} held_by={held.group(1) if held else '?'} :: {ftxt}")
            elif re.match(r"\d{3}-ADJUDICATE-[0-9a-f]{7}\.md$", n):
                t = git("show", f"{ref}:{p}")
                title = t.splitlines()[0] if t else ""
                rulings = re.findall(r"^RULING:\s*(.*)$", t, re.M)
                verdict_lines = re.findall(r"^(?:VERDICT|Verdict|##\s*Verdict)[: ].*$", t, re.M)
                adj.append(dict(path=p, ref=ref, title=title, rulings=rulings,
                                verdicts=verdict_lines[:6], size=len(t)))
                lines.append(f"## {p} :: {title}")
                for rl in rulings:
                    lines.append(f"  RULING: {rl[:260]}")
                for vl in verdict_lines[:6]:
                    lines.append(f"  {vl[:200]}")
    (OUT / "_disputes.txt").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "_adjudications.json").write_text(json.dumps(adj, indent=1), encoding="utf-8")
    print(len(lines), "lines;", len(adj), "adjudication files")


if __name__ == "__main__":
    main()
