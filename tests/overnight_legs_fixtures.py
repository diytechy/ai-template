"""Shared fixtures for the overnight-leg launcher's tests
(`scripts/coordinator/overnight_legs.py`, this repository's own tooling).

Three things live here, used by `test_overnight_legs.py` (in-process) and
`test_overnight_legs_git.py` (a real git repository per case):

  * `load_launcher()` imports the launcher from its folder, with that folder on
    `sys.path` for its `layout` import, since it is not a kit script;
  * `stub_claude()` puts a `claude` shim on a PATH that holds the stub and git
    only, so no installed agent CLI can ever be reached from a test. Each leg
    the shim runs appends one JSON record (the marker it saw, the prompt it got,
    its argv) and then performs the case's scripted git actions;
  * `handoff_repo()` builds a committed repository holding one handoff, and
    `lane_setup()` claims a lane `wi-1` in it and adds its commits.

No `test_` prefix, so it is never collected.
"""

import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

from conftest import ROOT

TOOLS = ROOT / "scripts" / "coordinator"
BLOCK = TOOLS / "headless-leg.md"
LOOP_SESSION_ENV = "KIT_LOOP_SESSION"


def load_launcher():
    """A fresh import of the launcher module."""
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(
        "overnight_legs", TOOLS / "overnight_legs.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def handoff_text(n):
    """A handoff whose session prompt names its leg."""
    return "# Handoff {0}\n\n## Session prompt\n\n```text\nYou are the coordinator, leg {0}.\n```\n".format(
        n
    )


def handoff_repo(root):
    """A committed repository on `main` holding `docs/handoff-001.md`."""
    from integrate_fixtures import _commit, git_repo

    root.mkdir(parents=True, exist_ok=True)
    git_repo(root)
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "handoff-001.md").write_text(
        handoff_text(1), encoding="utf-8", newline="\n"
    )
    _commit(root, "handoff 1")
    return root


# The stub leg. It reads the prompt from argv when the launcher passes it
# there, else from stdin, so a launcher that puts it in argv is judged on its
# record and never leaves the stub waiting on a terminal.
STUB = r"""
import json, os, subprocess, sys
from pathlib import Path

records = Path(os.environ["STUB_RECORDS"])
argv = sys.argv[1:]
if "-p" in argv and argv.index("-p") + 1 < len(argv) and not argv[argv.index("-p") + 1].startswith("--"):
    prompt = argv[argv.index("-p") + 1]
else:
    prompt = sys.stdin.read()
marker = os.environ.get("KIT_LOOP_SESSION")
done = records.read_text(encoding="utf-8").count("\n") if records.exists() else 0
with records.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps({"marker": marker, "prompt": prompt, "argv": argv}) + "\n")
if not marker:
    sys.exit(0)
leg = done + 1


OTHER = "20250101T000000Z-0a0b0c"
TRUNK = "refs/heads/main"
LANE = "refs/heads/wi-1"
ARCHIVE = "refs/heads/archive/lanes"


def git(*args):
    out = subprocess.run(["git", *args], check=True, capture_output=True, encoding="utf-8")
    return out.stdout.strip()


def marked(subject, session=None):
    return "{}\n\nLoop-Session: {}".format(subject, session or marker)


def trunk(message):
    git("commit", "-q", "--allow-empty", "-m", message)


def plumb(ref, message):
    # A commit on `ref` (created at HEAD when absent) through commit-tree, as
    # the archive recipe makes one; the working tree is never touched.
    parent = git("rev-parse", "--verify", "-q", ref) if ref_exists(ref) else git("rev-parse", "HEAD")
    sha = git("commit-tree", parent + "^{tree}", "-p", parent, "-m", message)
    git("update-ref", ref, sha)


def ref_exists(ref):
    return subprocess.run(["git", "rev-parse", "--verify", "-q", ref], capture_output=True).returncode == 0


def handoff():
    path = Path("docs") / "handoff-{:03d}.md".format(leg + 1)
    text = "# Handoff {0}\n\n## Session prompt\n\n```text\nYou are the coordinator, leg {0}.\n```\n"
    path.write_text(text.format(leg + 1), encoding="utf-8", newline="\n")
    git("add", "-A")
    git("commit", "-qm", marked("handoff: leg {}".format(leg)))


def claim_marked():
    trunk(marked("claim: WI-1 -> active/wi-1 (bookkeeping)"))
    git("branch", "wi-1")


def replay_lane():
    # The lane's commits re-made on trunk's tip: same messages, new parents.
    base = git("merge-base", "HEAD", LANE)
    shas = git("rev-list", "--reverse", "--topo-order", base + ".." + LANE).split()
    parent = git("rev-parse", "HEAD")
    for sha in shas:
        message = git("log", "-1", "--format=%B", sha)
        parent = git("commit-tree", parent + "^{tree}", "-p", parent, "-m", message)
    git("update-ref", LANE, parent)


def drop_lane_parent():
    # Remove the loose object of the commit below the lane's tip.
    sha = git("rev-parse", LANE + "~1")
    path = Path(git("rev-parse", "--git-dir")) / "objects" / sha[:2] / sha[2:]
    os.chmod(path, 0o666)
    path.unlink()


def archive_reset_unrelated():
    # The archive moved to a marked commit off trunk's tip: it does not
    # descend from the archive's old tip, and its one new commit is marked.
    parent = git("rev-parse", "HEAD")
    sha = git("commit-tree", parent + "^{tree}", "-p", parent, "-m", marked("archive reset"))
    git("update-ref", ARCHIVE, sha)


ACTIONS = {
    "handoff": handoff,
    "trunk_unmarked": lambda: trunk("unmarked trunk work"),
    "trunk_foreign": lambda: trunk(marked("foreign trunk work", OTHER)),
    "archive_unmarked": lambda: plumb(ARCHIVE, "unmarked archive record"),
    "archive_marked": lambda: plumb(ARCHIVE, marked("archive record")),
    "rewind": lambda: git("reset", "-q", "--hard", "HEAD~1"),
    "claim_marked": claim_marked,
    "lane_unmarked": lambda: plumb(LANE, "unmarked lane work"),
    "lane_marked": lambda: plumb(LANE, marked("marked lane work")),
    "telemetry_marked": lambda: plumb(LANE, marked("telemetry: session wi-1 sitting")),
    "squash_marked": lambda: (
        subprocess.run(["git", "merge", "--squash", LANE], capture_output=True),
        trunk(marked("squash: wi-1 landed")),
    ),
    "replay_lane": replay_lane,
    "drop_lane_parent": drop_lane_parent,
    "checkout_elsewhere": lambda: git("checkout", "-q", "-b", "elsewhere"),
    "main_unmarked": lambda: plumb(TRUNK, "unmarked trunk work"),
    "archive_rewind": lambda: git("update-ref", ARCHIVE, ARCHIVE + "~1"),
    "archive_reset_unrelated": archive_reset_unrelated,
    "archive_delete": lambda: git("update-ref", "-d", ARCHIVE),
}
plan = json.loads(os.environ.get("STUB_PLAN", "[]"))
for name in (plan[leg - 1] if leg <= len(plan) else ["handoff"]):
    ACTIONS[name]()
"""

OTHER_SESSION = "20250101T000000Z-0a0b0c"


def lane_setup(repo, claim_session=None, sessions=()):
    """Claim `wi-1` on trunk, with the trailer naming `claim_session` when
    given, then add one lane commit per entry of `sessions` (None: unmarked)."""
    from integrate_fixtures import _git

    claim = "claim: WI-1 -> active/wi-1 (bookkeeping)"
    _git(repo, "commit", "-q", "--allow-empty", "-m", trailed(claim, claim_session))
    _git(repo, "branch", "wi-1")
    for n, session in enumerate(sessions, start=1):
        lane_commit(repo, trailed("lane work {}".format(n), session))


def lane_commit(repo, message):
    """A commit on `wi-1` through commit-tree; its sha."""
    from integrate_fixtures import _git

    parent = _git(repo, "rev-parse", "refs/heads/wi-1").strip()
    sha = _git(repo, "commit-tree", parent + "^{tree}", "-p", parent, "-m", message)
    _git(repo, "update-ref", "refs/heads/wi-1", sha.strip())
    return sha.strip()


def trailed(subject, session):
    """`subject`, with a `Loop-Session` trailer naming `session` when given."""
    return "{}\n\nLoop-Session: {}".format(subject, session) if session else subject


def stub_claude(tmp_path, monkeypatch, plan=None):
    """Put the stub `claude` first on a PATH holding only it, git and sh, and
    return the path of the JSON-lines record file its legs append to."""
    bindir = tmp_path / "stub-bin"
    bindir.mkdir()
    program = bindir / "stub_claude.py"
    program.write_text(STUB, encoding="utf-8")
    if os.name == "nt":
        shim = bindir / "claude.cmd"
        shim.write_text(
            '@"{}" "{}" %*\r\n'.format(sys.executable, program), encoding="ascii"
        )
    else:
        shim = bindir / "claude"
        shim.write_text(
            '#!/bin/sh\nexec "{}" "{}" "$@"\n'.format(sys.executable, program),
            encoding="ascii",
        )
        shim.chmod(0o755)
    gitdir = str(Path(shutil.which("git")).parent)
    # The fixture checkout's commit hooks are on, and git runs them through
    # sh, so the shell's directory joins git's.
    shdir = str(Path(shutil.which("sh")).parent)
    path = os.pathsep.join([str(bindir), gitdir, shdir])
    assert Path(shutil.which("claude", path=path)).parent == bindir
    monkeypatch.setenv("PATH", path)
    records = tmp_path / "legs.jsonl"
    monkeypatch.setenv("STUB_RECORDS", str(records))
    monkeypatch.setenv("STUB_PLAN", json.dumps(plan or []))
    return records


def leg_records(records):
    """The records the stub legs wrote, in order."""
    if not records.exists():
        return []
    return [
        json.loads(line) for line in records.read_text(encoding="utf-8").splitlines()
    ]
