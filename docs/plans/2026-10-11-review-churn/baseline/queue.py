"""Row M: net queue over the window from trunk's docs/work history (read-only git).

Equivalent command:
  git log 45d867e51 --first-parent --since=2026-10-09T00:00:00-05:00 \
      --until=2026-10-11T23:59:59-05:00 -M --name-status --format='@@%h %ad %s' \
      --date=iso-strict -- docs/work/ docs/archive/work/
Counts: A under docs/work/{queued,draft}/ (split: 'mint:' commits = successors
minted, others = filed); closes = any A/R whose destination is under
docs/archive/work/ (the measure's rule), plus the alternative that also counts
moves into docs/work/{complete,cancelled,partial,restructured}/.
"""
import re
import subprocess
from collections import Counter

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()  # run from the repository root


def main():
    out = subprocess.run(
        ["git", "-C", REPO, "log", "45d867e51", "--first-parent",
         "--since=2026-10-09T00:00:00-05:00", "--until=2026-10-11T23:59:59-05:00",
         "-M", "--name-status", "--format=@@%h %ad %s", "--date=iso-strict",
         "--", "docs/work/", "docs/archive/work/"],
        capture_output=True).stdout.decode("utf-8", "replace")
    c = Counter()
    rows = {"filed": [], "minted": [], "closed_archive": [], "closed_other": [], "cancel_or_partial": []}
    subj = ""
    for line in out.splitlines():
        if line.startswith("@@"):
            subj = line.split(" ", 2)[2] if line.count(" ") >= 2 else ""
            continue
        if not line.strip():
            continue
        parts = line.split("\t")
        st = parts[0]
        dest = parts[-1]
        src = parts[1] if len(parts) > 2 else ""
        wi = re.search(r"WI-\d+", dest)
        wid = wi.group(0) if wi else dest
        if st == "A" and re.match(r"docs/work/(queued|draft)/WI-", dest):
            key = "minted" if subj.startswith("mint:") else "filed"
            rows[key].append(wid)
        elif dest.startswith("docs/archive/work/") and (st == "A" or st.startswith("R")) and not src.startswith("docs/archive/work/"):
            rows["closed_archive"].append(f"{wid}<-{src.split('/')[2] if src else 'new'}->{dest.split('/')[3]}")
        elif st.startswith("R") and re.match(r"docs/work/(complete|cancelled|partial|restructured)/", dest) and not re.match(r"docs/work/(complete|cancelled|partial|restructured)/", src):
            rows["closed_other"].append(f"{wid}->{dest.split('/')[2]}")
    for k, v in rows.items():
        print(f"{k}: {len(v)} {v}")
    filed, minted = len(rows["filed"]), len(rows["minted"])
    ca, co = len(rows["closed_archive"]), len(rows["closed_other"])
    net = filed + minted - ca
    print(f"net (measure rule) = {filed} + {minted} - {ca} = {net} over 3 days -> {net*7/3:.1f}/week")
    net2 = filed + minted - ca - co
    print(f"net (alt, any terminal folder) = {filed} + {minted} - {ca} - {co} = {net2} -> {net2*7/3:.1f}/week")


if __name__ == "__main__":
    main()
