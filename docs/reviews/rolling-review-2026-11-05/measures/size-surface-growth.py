"""Growth trend at monthly snapshots over git history (read-only: git rev-list / git show).

For each date: SR/LLR/TC rows, .py files under project-trajectory/scripts, test modules,
PROCESS.md and PROCESS_OPTIONS.md bytes, check.py lines, check.py floor steps, plus a few
extras (skills, prompts, RESYNC_PACK bytes, kitlib files, scripts lines, tests lines,
registry file bytes, docs/log.md bytes, PROJECT_STATE.html bytes).
"""
import re
import subprocess
import sys

ROOT = sys.argv[1]
DATES = ["2026-06-15", "2026-07-15", "2026-08-15", "2026-09-15", "2026-10-15", "2026-11-05"]


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, errors="replace")


def commit_before(date):
    r = git("rev-list", "-1", "--before=" + date + "T23:59:59", "HEAD")
    return r.stdout.strip()


def ls_tree(commit, path=""):
    r = git("ls-tree", "-r", "--name-only", commit, path) if path else git("ls-tree", "-r", "--name-only", commit)
    return [l for l in r.stdout.splitlines() if l]


def show(commit, path):
    r = subprocess.run(["git", "-C", ROOT, "show", f"{commit}:{path}"], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def nbytes(commit, path):
    b = show(commit, path)
    return len(b) if b is not None else 0


def nlines(commit, path):
    b = show(commit, path)
    return b.count(b"\n") if b is not None else 0


def count_rows(commit, candidates, pattern):
    """Count registry rows: try several carriers (toml table headers / csv rows)."""
    for path in candidates:
        b = show(commit, path)
        if b is None:
            continue
        text = b.decode("utf-8", "replace")
        if path.endswith(".toml"):
            n = len(re.findall(pattern, text, re.M))
            return n, path
        if path.endswith(".csv"):
            lines = [l for l in text.splitlines() if l.strip()]
            n = max(0, len(lines) - 1)
            n -= sum(1 for l in lines[1:] if re.match(r"^[A-Z]+-000\b", l))
            return n, path
    return 0, None


def check_steps(commit):
    b = show(commit, "project-trajectory/scripts/check.py")
    if b is None:
        return 0, 0
    text = b.decode("utf-8", "replace")
    lines = text.count("\n")
    # count step registrations: tuples/entries like ("name", fn) in a STEPS list, or @step decorators
    # a step tuple opens as `("name", requires, cmd, ...)` possibly split over lines
    n = len(re.findall(r'\(\s*"([a-z][a-z0-9-]*)",\s*(?:\(|_requires|\[|None|[a-z_]+\s*,)', text))
    return lines, n


SR = ["docs/requirements/system-requirements.toml", "docs/requirements/system-requirements.csv"]
LLR = ["docs/requirements/low-level-requirements.toml", "docs/requirements/low-level-requirements.csv"]
TC = ["docs/test/test-cases.toml", "docs/test/test-cases.csv"]
SN = ["docs/requirements/stakeholder-needs.toml", "docs/requirements/stakeholder-needs.csv", "docs/requirements/user-needs.toml", "docs/requirements/user-needs.csv"]
IFC = ["docs/requirements/interfaces.toml", "docs/requirements/interfaces.csv"]
OI = ["docs/requirements/open-items.toml", "docs/requirements/open-items.csv", "docs/open-items.md"]

print("| date | commit | SN | SR | LLR | TC | IF | OI | scripts .py | kitlib .py | scripts lines | test modules | tests lines | PROCESS B | PROCESS_OPTIONS B | check.py lines | check.py steps(regex) | skills | prompts | RESYNC_PACK B | log.md B | PROJECT_STATE B | tracked files | docs files |")
print("|" + "---|" * 25)
for d in DATES:
    c = commit_before(d)
    files = ls_tree(c)
    scripts = [f for f in files if f.startswith("project-trajectory/scripts/") and f.endswith(".py")]
    kitlib = [f for f in scripts if "/kitlib/" in f]
    tests = [f for f in files if f.startswith("tests/") and f.endswith(".py") and f.split("/")[-1].startswith("test_")]
    skills = [f for f in files if f.startswith("project-trajectory/skills/") and f.endswith("SKILL.md")]
    prompts = [f for f in files if f.startswith("project-trajectory/prompts/") and f.endswith(".md")]
    docs = [f for f in files if f.startswith("docs/")]
    sn = count_rows(c, SN, r"^\[(?:need|stakeholder_need|user_need)\.[A-Z]+-(?!000\])\d+\]")
    sr = count_rows(c, SR, r"^\[(?:requirement|system_requirement|sr)\.[A-Z]+-(?!000\])\d+\]")
    llr = count_rows(c, LLR, r"^\[(?:design|low_level_requirement|llr)\.[A-Z]+-(?!000\])\d+\]")
    tc = count_rows(c, TC, r"^\[(?:test|test_case|tc)\.[A-Z]+-(?!000\])\d+\]")
    ifc = count_rows(c, IFC, r"^\[(?:interface|if)\.[A-Z]+-(?!000\])\d+\]")
    oi = count_rows(c, OI, r"^\[open_item\.OI-\d+\]|^\[\[open_items?\]\]")
    scr_lines = sum(nlines(c, f) for f in scripts)
    test_lines = sum(nlines(c, f) for f in tests)
    chk_lines, chk_steps = check_steps(c)
    print(f"| {d} | {c[:9]} | {sn[0]} | {sr[0]} | {llr[0]} | {tc[0]} | {ifc[0]} | {oi[0]} | {len(scripts)-len(kitlib)} | {len(kitlib)} | {scr_lines} | {len(tests)} | {test_lines} | {nbytes(c,'project-trajectory/PROCESS.md')} | {nbytes(c,'project-trajectory/PROCESS_OPTIONS.md')} | {chk_lines} | {chk_steps} | {len(skills)} | {len(prompts)} | {nbytes(c,'project-trajectory/RESYNC_PACK.md')} | {nbytes(c,'docs/log.md')} | {max(nbytes(c,'PROJECT_STATE.html'), nbytes(c,'docs/trajectory.html'))} | {len(files)} | {len(docs)} |")
    print(f"<!-- {d}: carriers SN={sn[1]} SR={sr[1]} LLR={llr[1]} TC={tc[1]} IF={ifc[1]} OI={oi[1]} -->", file=sys.stderr)
