"""Growth of the kit over its history (stdlib only; needs full git history).

Run from the repository root: `python docs/reviews/rolling-review-2026-11-05/trend.py`.
One row per snapshot date: the commit at or before that date on the current
branch, then the size of each surface at that commit. Registry rows are counted
from the TOML table headers (or, before the TOML carrier, CSV data rows); the
`-000` example rows are excluded. The kit's own vision is a kit a downstream
team can read and re-sync, so the derivative of each column is the finding.
"""

import datetime
import re
import subprocess
import sys

DATES = ["2026-06-15", "2026-07-15", "2026-08-15", "2026-09-15", "2026-10-15", "2026-11-05"]
REGISTRIES = {
    "SR": ("docs/requirements/system-requirements", r"^\[requirement\.SR-\d+\]"),
    "LLR": ("docs/requirements/low-level-requirements", r"^\[design\.LLR-\d+\]"),
    "TC": ("docs/test/test-cases", r"^\[test\.TC-\d+\]"),
    "IF": ("docs/requirements/interfaces", r"^\[interface\.IF-\d+\]"),
    "OI": ("docs/requirements/open-items", r"^\[[a-z_]+\.OI-\d+\]"),
}


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout


def show(commit, path):
    return git("show", f"{commit}:{path}")


def rows(commit, base, pattern):
    toml = show(commit, base + ".toml")
    if toml:
        return sum(1 for line in toml.splitlines() if re.match(pattern, line) and not line.rstrip("]").endswith("-000"))
    csv = show(commit, base + ".csv")
    if csv:
        lines = [l for l in csv.splitlines()[1:] if l.strip() and "-000" not in l.split(",")[0]]
        return len(lines)
    return 0


def files(commit, prefix, suffix=""):
    out = git("ls-tree", "-r", "--name-only", commit, "--", prefix)
    return [p for p in out.splitlines() if p.endswith(suffix)]


def lines(commit, paths):
    return sum(show(commit, p).count("\n") for p in paths)


def main():
    cols = ["date", "commit", "SR", "LLR", "TC", "IF", "OI", "py", "pyLines", "tests", "testLines", "PROCESS_KB", "OPTIONS_KB", "check.py", "skills", "commits/30d"]
    print("\t".join(cols))
    for date in DATES:
        commit = git("rev-list", "-1", f"--before={date}", "HEAD").strip()
        if not commit:
            continue
        py = [p for p in files(commit, "project-trajectory/scripts", ".py")]
        tests = [p for p in files(commit, "tests", ".py") if p.split("/")[-1].startswith("test_")]
        skills = {p.split("/")[2] for p in files(commit, "project-trajectory/skills") if p.count("/") >= 3}
        start = (datetime.date.fromisoformat(date) - datetime.timedelta(days=30)).isoformat()
        since = git("rev-list", "--count", f"--after={start}", f"--before={date}", "HEAD").strip()
        row = [
            date, commit[:8],
            *[str(rows(commit, *REGISTRIES[k])) for k in ("SR", "LLR", "TC", "IF", "OI")],
            str(len(py)), str(lines(commit, py)),
            str(len(tests)), str(lines(commit, tests)),
            str(len(show(commit, "project-trajectory/PROCESS.md").encode()) // 1024),
            str(len(show(commit, "project-trajectory/PROCESS_OPTIONS.md").encode()) // 1024),
            str(show(commit, "project-trajectory/scripts/check.py").count("\n")),
            str(len(skills)),
            since or "0",
        ]
        print("\t".join(row))


if __name__ == "__main__":
    sys.exit(main())
