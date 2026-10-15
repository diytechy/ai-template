"""Row M: build baseline-files.csv and baseline-findings.csv, and print the counts.

Inputs (all in M/): _files.json (enumerate.py), _regress.tsv (regress.py),
_redtip2.tsv (redtip2.py), _adjudications.json (disputes.py), classify.py.
Read-only against the repository (git show / ls-tree / log only).
"""
import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from classify import C  # noqa: E402

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()  # run from the repository root
TRUNK = "45d867e51"
LANDED_IN_WINDOW = True  # every trunk-cohort WI landed in the window (squash commits dated 10-09..10-11)


def git(*args):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def cohort(r):
    if r["kind"].startswith("REVIEW"):
        return "primary"
    if r["slug"] == "wi-848-coordinator-cycle-skill":
        return "legacy-duplicate"
    return "legacy-alt"


def quote(text, n=15):
    t = re.sub(r"^\s*-\s*", "", text)
    t = re.sub(r"^\[(BLOCKER|MAJOR|MINOR)\]\s*", "", t)
    return " ".join(t.split()[:n])


def lane_commit(r):
    """The commit on the WI's own lane branch that added this file (trunk files only)."""
    if r["branch"] != "trunk" or not r["wi"]:
        return ""
    br = "wi-" + r["wi"][3:]
    mb = git("merge-base", TRUNK, br).strip()
    out = git("log", "--diff-filter=A", "--format=%h %aI", f"{mb}..{br}", "--", r["path"]).split("\n")
    return out[0].strip() if out and out[0].strip() else ""


def sittings(slug, ref):
    """[(nnn, is_dispute)] for the lane directory's ADJUDICATE files."""
    res = []
    for p in git("ls-tree", "--name-only", ref, f"docs/reviews/{slug}/").split():
        m = re.match(r".*/(\d{3})-ADJUDICATE-[0-9a-f]{7}\.md$", p)
        if m:
            t = git("show", f"{ref}:{p}")
            disp = bool(re.search(r"^RULING:", t, re.M)) or "dispute" in t.splitlines()[0].lower()
            res.append((m.group(1), disp))
    return sorted(res)


def main():
    recs = json.load(open(OUT / "_files.json", encoding="utf-8"))
    regress = {}
    for line in (OUT / "_regress.tsv").read_text(encoding="utf-8").splitlines():
        x = line.split("\t")
        regress[(x[1], int(x[2]))] = x
    red = {}
    for line in (OUT / "_redtip2.tsv").read_text(encoding="utf-8").splitlines():
        x = line.split("\t")
        red["docs/reviews/" + x[0]] = x

    # per-WI review ordering (primary cohort and legacy-alt kept apart)
    by_wi = defaultdict(list)
    for r in recs:
        r["cohort"] = cohort(r)
        if r["cohort"] == "legacy-duplicate":
            continue
        by_wi[(r["wi"], r["cohort"])].append(r)
    legacy_order = {  # pre-convention files have no NNN: order and sitting context from the lane log
        "sol-review-full-r1.md": 1, "sol-review-full.md": 2,
    }
    legacy_after_sitting = {  # spine sitting between the previous round (or lane start) and this one
        ("WI-853", "sol-review-full-r1.md"): "yes (001)", ("WI-853", "sol-review-full.md"): "yes (004)",
        ("WI-870", "sol-review-full-r1.md"): "yes (001)", ("WI-870", "sol-review-full.md"): "no",
        ("WI-869", "sol-review-full.md"): "yes (001)", ("WI-875", "sol-review-full.md"): "yes (001)",
    }
    files_rows, find_rows = [], []
    sit_cache = {}
    for (wi, coh), rs in sorted(by_wi.items()):
        if coh == "primary":
            rs.sort(key=lambda r: r["nnn"])
        else:
            rs.sort(key=lambda r: legacy_order.get(r["name"], 9))
        prev = None
        for k, r in enumerate(rs, 1):
            r["ordinal"] = k
            # checkpoint context
            after_na = bool(prev and prev["scope"] == "narrow" and prev["verdict"] == "APPROVE")
            if coh == "primary":
                key = (r["slug"], r["ref"])
                if key not in sit_cache:
                    sit_cache[key] = sittings(*key)
                lo = prev["nnn"] if prev else "000"
                between = [n for n, d in sit_cache[key] if lo < n < r["nnn"] and not d]
                after_sit = ("yes (" + ",".join(between) + ")") if between else "no"
            else:
                after_sit = legacy_after_sitting.get((wi, r["name"]), "no")
            majors = sum(1 for f in r["findings"] if f["severity"] in ("BLOCKER", "MAJOR"))
            reopen = r["scope"] == "full" and majors > 0 and (after_na or after_sit.startswith("yes"))
            # tip state
            x = red.get(r["path"])
            tip, tip_ev = "unknown", "no lane test report covers the reviewed tree"
            if x:
                rep, inter, rtext = x[4], x[7], x[6]
                fail_segs = [s for s in rtext.split(" | ") if re.search(r"\d+\s+failed", s)
                             and not re.search(r"(?i)red first|red-first|red before|before \(", s)]
                if rep != "-" and "*" not in inter and re.search(r"(?i)full suite", rtext):
                    tip_ev = f"nearest report {rep} records a full-suite run of another commit"
                elif rep != "-" and "*" not in inter:
                    if fail_segs:
                        tip, tip_ev = "red", f"lane report {rep}: {fail_segs[0][:120]}"
                    elif "OVER" in rtext:
                        tip, tip_ev = "budget-over", f"lane report {rep}: results green, 60 s smoke budget read OVER under load"
                    else:
                        tip, tip_ev = "green", f"lane report {rep} covers the reviewed tree"
                elif rep != "-":
                    tip_ev = f"nearest lane report {rep} predates a code commit"
            if r["path"].endswith("wi-834/001-REVIEW-A-785a004.md"):
                # the lane's later commit message says so: an ancestor of the reviewed sha reddened smoke
                tip, tip_ev = "red", ("commit 73ad57436 (round-1 fix): IF-292's channel value 'reddened the smoke tier "
                                      "since ec95154b', an ancestor of the reviewed 785a004d6")
            text = git("show", f"{r['ref']}:{r['path']}")
            fails = re.findall(r"(\d+) failed", text)
            sandbox = bool(re.search(r"CreateFileMapping|sandbox", text))
            if r["path"].endswith("wi-881/006-REVIEW-A-0960348.md"):
                rev = "2 failures also failing at base (not worsened)"
            elif re.search(r"\d+ passed", text):
                rev = "targeted tests reported; failures only sandbox-attributed" if (fails and sandbox) else "targeted tests reported passing"
            else:
                rev = "no test run reported"
            files_rows.append(dict(
                lane_slug=r["slug"], wi=wi, path=r["path"], added_commit=r["commit"][:9],
                added_date=r["commit_date"], on=("trunk" if r["branch"] == "trunk" else "lane " + r["branch"]),
                lane_branch_commit=lane_commit(r), round_nnn=r["nnn"], review_ordinal=k, kind=r["kind"],
                scope=r["scope"], reviewed_sha=r["reviewed"], verdict=r["verdict"], findings_n=r["findings_n"],
                cohort=coh, wi_status=("landed in window" if r["branch"] == "trunk" else "in flight"),
                after_narrow_approve="yes" if after_na else "no", after_spine_sitting=after_sit,
                full_reopen_after_checkpoint="yes" if reopen else "no",
                tip_state=tip, tip_evidence=tip_ev, reviewer_tests=rev))
            for i, f in enumerate(r["findings"], 1):
                c = C[(r["path"], i)]
                g = regress.get((r["path"], i))
                find_rows.append(dict(
                    path=r["path"], finding_index=i, severity=f["severity"], quote=quote(f["text"]),
                    late="yes" if k >= 2 else "no",
                    full_after_narrow_approve="yes" if (r["scope"] == "full" and after_na) else "no",
                    primary_class=c[0], secondary_tags=c[1], disposition=c[2], reason=c[4], evidence=c[5],
                    regression_basis=c[3] or "no", cited_site=(g[3] if g else ""),
                    site_last_changed_by=(g[4] if g else ""), cohort=coh, wi=wi,
                    wi_status=("landed in window" if r["branch"] == "trunk" else "in flight"),
                    review_ordinal=k, scope=r["scope"], line_in_file=f["line"]))
            prev = r
    # the duplicate legacy file: listed, excluded from every count
    for r in recs:
        if r["cohort"] == "legacy-duplicate":
            files_rows.append(dict(
                lane_slug=r["slug"], wi=r["wi"], path=r["path"], added_commit=r["commit"][:9],
                added_date=r["commit_date"], on="trunk", lane_branch_commit="", round_nnn="", review_ordinal="",
                kind=r["kind"], scope=r["scope"], reviewed_sha=r["reviewed"], verdict=r["verdict"],
                findings_n=r["findings_n"], cohort="legacy-duplicate", wi_status="landed in window",
                after_narrow_approve="", after_spine_sitting="", full_reopen_after_checkpoint="",
                tip_state="", tip_evidence="duplicate of wi-848/001-REVIEW-A-993deee.md", reviewer_tests=""))
            for i, f in enumerate(r["findings"], 1):
                c = C[(r["path"], i)]
                find_rows.append(dict(
                    path=r["path"], finding_index=i, severity=f["severity"], quote=quote(f["text"]),
                    late="", full_after_narrow_approve="", primary_class=c[0], secondary_tags=c[1],
                    disposition=c[2], reason=c[4], evidence=c[5], regression_basis="", cited_site="",
                    site_last_changed_by="", cohort="legacy-duplicate", wi=r["wi"], wi_status="landed in window",
                    review_ordinal="", scope=r["scope"], line_in_file=f["line"]))
    order = {"primary": 0, "legacy-alt": 1, "legacy-duplicate": 2}
    files_rows.sort(key=lambda d: (order[d["cohort"]], d["wi"], str(d["review_ordinal"]).zfill(3)))
    find_rows.sort(key=lambda d: (order[d["cohort"]], d["wi"], str(d["review_ordinal"]).zfill(3), d["finding_index"]))
    with open(OUT / "baseline-files.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(files_rows[0].keys()))
        w.writeheader()
        w.writerows(files_rows)
    with open(OUT / "baseline-findings.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(find_rows[0].keys()))
        w.writeheader()
        w.writerows(find_rows)
    json.dump(dict(files=files_rows, findings=find_rows), open(OUT / "_built.json", "w", encoding="utf-8"), indent=1)
    print(len(files_rows), "file rows;", len(find_rows), "finding rows")


if __name__ == "__main__":
    main()
