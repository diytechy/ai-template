"""Row M baseline: enumerate review files added in the window (read-only git).

Writes only into this directory (M/). Never touches the repository.
Usage: python enumerate.py   (prints a summary; writes M/_files.json, M/_findings.json)
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()  # run from the repository root
OUT = Path(__file__).resolve().parent
TRUNK = "45d867e51"
LANES = {"wi-798": "9437d0a1f", "wi-902": "d3d301216"}
START = datetime.fromisoformat("2026-10-09T00:00:00-05:00")
END = datetime.fromisoformat("2026-10-11T23:59:59-05:00")

REVIEW_A = re.compile(r"^(?P<nnn>\d{3})-REVIEW-(?P<rk>[AB])-(?P<sha7>[0-9a-f]{7})(?P<narrow>-narrow)?\.md$")
LEGACY = re.compile(r"^sol-review-(?P<scope>full|r\d+|full-r\d+|full-lane-\d+)\.md$")
SEV = re.compile(r"^\s*(?:[-*]\s+)?\[(BLOCKER|MAJOR|MINOR)\]")
VERDICT = re.compile(r"^VERDICT:\s*(APPROVE|CHANGES-REQUESTED)\s+findings=(\d+)\s*$", re.M)


def git(*args):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.decode('utf-8', 'replace')}")
    return r.stdout.decode("utf-8", "replace")


def added(rev_range, since=None):
    """[(path, sha, author_date, committer_date, subject)] for files added under docs/reviews/."""
    args = ["log", "--diff-filter=A", "--name-only", "--date=iso-strict",
            "--format=@@%H|%ad|%cd|%s"]
    args += rev_range
    args += ["--", "docs/reviews/"]
    out = git(*args)
    rows, cur = [], None
    for line in out.splitlines():
        if line.startswith("@@"):
            sha, ad, cd, subj = line[2:].split("|", 3)
            cur = (sha, ad, cd, subj)
        elif line.strip():
            rows.append((line.strip(), *cur))
    return rows


def main():
    files = []
    # trunk: the whole history of the snapshot; filter by committer date in Python
    for path, sha, ad, cd, subj in added([TRUNK]):
        d = datetime.fromisoformat(cd)
        if START <= d <= END:
            files.append(dict(path=path, branch="trunk", commit=sha, author_date=ad,
                              commit_date=cd, subject=subj, ref=TRUNK))
    for lane, tip in LANES.items():
        mb = git("merge-base", TRUNK, tip).strip()
        for path, sha, ad, cd, subj in added([f"{mb}..{tip}"]):
            files.append(dict(path=path, branch=lane, commit=sha, author_date=ad,
                              commit_date=cd, subject=subj, ref=tip, merge_base=mb))
    recs = []
    for f in files:
        name = f["path"].rsplit("/", 1)[-1]
        slug = f["path"].split("/")[2] if f["path"].count("/") >= 3 else ""
        m = REVIEW_A.match(name)
        lm = LEGACY.match(name)
        if not (m or lm):
            continue
        text = git("show", f"{f['ref']}:{f['path']}")
        rec = dict(f, slug=slug, name=name)
        wi = re.match(r"wi-(\d{3})", slug)
        rec["wi"] = f"WI-{wi.group(1)}" if wi else ""
        if m:
            rec["kind"] = f"REVIEW-{m.group('rk')}"
            rec["nnn"] = m.group("nnn")
            rec["scope"] = "narrow" if m.group("narrow") else "full"
            first = text.splitlines()[0] if text else ""
            rm = re.match(r"Reviewed:\s*([0-9a-f]{7,40})", first)
            rec["reviewed"] = rm.group(1) if rm else ""
            vs = VERDICT.findall(text)
            rec["verdict_lines"] = len(vs)
            rec["verdict"], rec["findings_n"] = (vs[0][0], int(vs[0][1])) if vs else ("", -1)
        else:
            rec["kind"] = "legacy-sol-review"
            rec["nnn"] = ""
            rec["scope"] = "full"
            first = text.splitlines()[0] if text else ""
            rm = re.match(r"(?:Reviewed:\s*)?([0-9a-f]{7,40})\s*(.*)$", first)
            rec["reviewed"] = rm.group(1) if rm else ""
            v = VERDICT.findall(text)
            if v:
                rec["verdict"], rec["findings_n"] = v[0][0], int(v[0][1])
                rec["verdict_lines"] = len(v)
            else:
                rec["verdict"] = (rm.group(2).strip() if rm else "")
                rec["findings_n"] = -1
                rec["verdict_lines"] = 0
        # findings: severity-tagged lines (REVIEW-A) or bullets under severity headings (legacy)
        finds = []
        lines = text.splitlines()
        if rec["kind"].startswith("REVIEW"):
            for i, ln in enumerate(lines, 1):
                sm = SEV.match(ln)
                if sm:
                    finds.append(dict(line=i, severity=sm.group(1), text=ln.strip()))
        else:
            sec = None
            for i, ln in enumerate(lines, 1):
                hm = re.match(r"^##\s+(BLOCKER|MAJOR|MINOR)\s*$", ln)
                if hm:
                    sec = hm.group(1)
                    continue
                if ln.startswith("## "):
                    sec = None
                    continue
                sm = SEV.match(ln)
                if sm:
                    finds.append(dict(line=i, severity=sm.group(1), text=ln.strip()))
                elif sec and re.match(r"^\s*[-*]\s+\S", ln):
                    finds.append(dict(line=i, severity=sec, text=ln.strip()))
            if rec["findings_n"] < 0:
                rec["findings_n"] = len(finds)
        rec["parsed_findings"] = len(finds)
        rec["findings"] = finds
        recs.append(rec)
    recs.sort(key=lambda r: (r["slug"], r["nnn"] or "999", r["name"]))
    (OUT / "_files.json").write_text(json.dumps(recs, indent=1), encoding="utf-8")
    # summary
    by_kind = {}
    for r in recs:
        by_kind.setdefault(r["kind"], []).append(r)
    for k, rs in by_kind.items():
        print(k, len(rs), "files;", len({r['wi'] for r in rs}), "WIs;",
              sum(r["findings_n"] for r in rs), "findings (verdict n);",
              sum(r["parsed_findings"] for r in rs), "parsed")
    bad = [r for r in recs if r["findings_n"] != r["parsed_findings"] or (r["kind"].startswith("REVIEW") and r["verdict_lines"] != 1)]
    for r in bad:
        print("MISMATCH", r["path"], r["verdict"], r["findings_n"], r["parsed_findings"], r["verdict_lines"])


if __name__ == "__main__":
    main()
