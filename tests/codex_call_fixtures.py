"""Shared fixtures for the coordinator's codex call
(`scripts/coordinator/codex_call.py`, this repository's own tooling), used by
`test_codex_call.py` (in-process) and `test_codex_call_git.py` (real lanes and
a stand-in `codex` process).

  * `load_codex_call()` imports the entry point from its folder;
  * `route_files()` are the roster rows, the enable-list and the ignore line a
    lane fixture commits (`conftest.claimed_lane(files=...)`);
  * `call_log()` writes one standard-call session log through the kit's own
    writer, and `cut_before()` truncates one, for the resume carrier's cases;
  * `stand_in_codex()` puts a `codex` executable first on a PATH: it records
    its argv, cwd and prompt, writes the `--output-last-message` file, prints
    the live codex stream and performs its scenario's git act in its cwd.

No `test_` prefix, so it is never collected.
"""

import importlib.util
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import agent_common
from conftest import ROOT, SCRIPTS

TOOLS = ROOT / "scripts" / "coordinator"
CALL_TOOL = TOOLS / "codex_call.py"
GOLDEN_STREAM = ROOT / "tests" / "golden" / "sessions" / "codex-exec-json.jsonl"
FINAL_TEXT = "STANDIN FINAL TEXT"
SOL_MODEL, TERRA_MODEL = "gpt-6.1-sol", "gpt-5.6-terra"
TEMPLATE = (
    "codex exec -c model_reasoning_effort=medium --model {model} "
    "--dangerously-bypass-approvals-and-sandbox"
)
AGENTS = """[agent.OPENAI-SOL]
family = "OPENAI"
model = "gpt-6.1-sol"
version = "6.1"
tier = "strong"
cmd_template = "{t}"
env = ""
notes = "test row"

[agent.OPENAI-TERRA]
family = "OPENAI"
model = "gpt-5.6-terra"
version = "5.6"
tier = "medium"
cmd_template = "{t}"
env = ""
notes = "test row"

[agent.OPENAI-LUNA]
family = "OPENAI"
model = "gpt-5.6-luna"
version = "5.6"
tier = "quick"
cmd_template = "{t}"
env = ""
notes = "a row the enable-list does not name"
""".replace("{t}", TEMPLATE)
ENABLED = "OPENAI-SOL\nOPENAI-TERRA\n"


def load_codex_call():
    """A fresh import of the entry point."""
    spec = importlib.util.spec_from_file_location("codex_call", CALL_TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def route_files():
    """The files a lane fixture commits for the entry point: the roster rows,
    the enable-list (Sol and Terra on, Luna off) and `out/` ignored, as a
    set-up checkout ignores it."""
    return {
        "docs/agents.toml": AGENTS,
        "docs/agents-enabled": ENABLED,
        ".gitignore": "out/\n",
    }


def write_route_files(root):
    """`route_files()` written under `root`, uncommitted."""
    for rel, text in route_files().items():
        path = Path(root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    return root


def new_invocation():
    return uuid.uuid4().hex


def call_log(
    iter_dir,
    *,
    role="AUTHOR",
    wi="WI-1",
    route="OPENAI-TERRA",
    session_id="T-OLD",
    stamp="20261022-100000",
    invocation=None,
):
    """One standard-call session log, written by the kit's own writer under
    `iter_dir` with the name `_call_row` gives (`call_<invocation>-<stamp>`).
    Returns its path."""
    invocation = invocation or new_invocation()
    meta = {
        "session": "call_" + invocation,
        "stamp": stamp,
        "date": "2026-10-22 10:00",
        "phase": role,
        "wi": wi,
        "outcome": "COMPLETED",
        "session-id": session_id,
        "invocation-id": invocation,
        "role": role,
        "provider": "OPENAI",
        "roster-row": route,
        "started-at": "2026-10-22T10:00:00Z",
    }
    return agent_common.write_session_log(Path(iter_dir), meta, "transcript\n")


def cut_before(text, key):
    """`text` cut just before its `# <key>:` header line, as a write killed
    there leaves it."""
    marker = "\n# {}:".format(key) if key != "---" else "\n# ---"
    return text[: text.index(marker) + 1]


def drop_line(text, key):
    """`text` without its `# <key>:` header line."""
    return "".join(
        line
        for line in text.splitlines(keepends=True)
        if not line.startswith("# {}:".format(key))
    )


def rel(root, path):
    """`path` relative to `root`, in git's spelling."""
    return Path(path).relative_to(root).as_posix()


# The stand-in. Its scenario is read from the environment, so one shim serves
# every case:
#   CODEX_STANDIN_RECORDS  a JSON-lines file each launch appends to
#   CODEX_STANDIN_ACT      the git act performed in its cwd (see ACTS)
#   CODEX_STANDIN_ARG      the act's path argument, where it takes one
#   CODEX_STANDIN_THREAD   the thread id its stream reports
#   CODEX_STANDIN_KIT      the kit's scripts, for the acts that record a log
STAND_IN = r"""
import json, os, subprocess, sys, uuid
from pathlib import Path

argv = sys.argv[1:]
prompt = sys.stdin.read()
cwd = Path.cwd()
with open(os.environ["CODEX_STANDIN_RECORDS"], "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"argv": argv, "cwd": str(cwd), "prompt": prompt}) + "\n")
if "--output-last-message" in argv:
    out = argv[argv.index("--output-last-message") + 1]
    Path(out).write_text("STANDIN FINAL TEXT", encoding="utf-8")
thread = os.environ.get("CODEX_STANDIN_THREAD", "")
for line in Path(os.environ["CODEX_STANDIN_STREAM"]).read_text(encoding="utf-8").splitlines():
    event = json.loads(line)
    if thread and event.get("type") == "thread.started":
        event["thread_id"] = thread
    print(json.dumps(event))
act = os.environ.get("CODEX_STANDIN_ACT", "none")
arg = os.environ.get("CODEX_STANDIN_ARG", "")


def git(*args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def commit(message, *paths):
    git("add", "--", *paths)
    git("commit", "-q", "--no-verify", "-m", message)


def kit():
    sys.path.insert(0, os.environ["CODEX_STANDIN_KIT"])
    import agent_common, session_service
    return agent_common, session_service


if act == "commit-work":
    (cwd / "work.txt").write_text("work\n", encoding="utf-8")
    commit("work", "work.txt")
elif act == "leave-work":
    (cwd / "work.txt").write_text("work\n", encoding="utf-8")
elif act == "stage":
    git("add", "--", arg)
elif act == "unstage":
    git("reset", "-q", "--", arg)
elif act == "record-call":
    _, svc = kit()
    metrics = {"invocation-id": uuid.uuid4().hex, "role": "CRITIQUE"}
    outcome = svc.Outcome(cwd, 0, "", False, "", metrics)
    svc.record(outcome, svc._call_row(metrics, "COMPLETED"))
elif act == "commit-gate-log":
    log = cwd / "docs" / "iteration" / "001-20261022-101010.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("# session: 001\n# ---\n", encoding="utf-8")
    commit("telemetry: session 001", "docs/iteration/001-20261022-101010.log")
elif act == "modify-log":
    with open(cwd / arg, "a", encoding="utf-8") as fh:
        fh.write("changed\n")
    commit("telemetry: changed", arg)
elif act == "commit-work-path":
    (cwd / "src.txt").write_text("src\n", encoding="utf-8")
    commit("telemetry: src", "src.txt")
elif act == "commit-waiting":
    common, _ = kit()
    common.commit_telemetry(cwd, "waiting", "CRITIQUE COMPLETED", [cwd / arg])
elif act == "modify-waiting":
    common, _ = kit()
    with open(cwd / arg, "a", encoding="utf-8") as fh:
        fh.write("changed\n")
    common.commit_telemetry(cwd, "waiting", "CRITIQUE COMPLETED", [cwd / arg])
elif act == "delete-waiting":
    (cwd / arg).unlink()
elif act == "reset-hard":
    git("reset", "-q", "--hard", "HEAD~1")
elif act == "lock-index":
    lock = git("rev-parse", "--git-path", "index.lock").stdout.strip()
    lock = Path(lock) if Path(lock).is_absolute() else cwd / lock
    lock.write_text("", encoding="utf-8")
elif act == "break-git":
    (cwd / ".git").unlink()  # hidden on Windows, which refuses a rewrite
    (cwd / ".git").write_text("not a git file\n", encoding="utf-8")
sys.exit(0)
"""


def stand_in_codex(base):
    """A `codex` stand-in under `base/bin` (a shim on Windows), and the
    records file it appends to. Returns `(bindir, records)`."""
    bindir = Path(base) / "bin"
    bindir.mkdir(parents=True, exist_ok=True)
    script = bindir / "standin_codex.py"
    script.write_text(STAND_IN, encoding="utf-8", newline="\n")
    if os.name == "nt":
        (bindir / "codex.cmd").write_text(
            '@echo off\r\n"{}" "{}" %*\r\n'.format(sys.executable, script),
            encoding="ascii",
        )
    else:
        shim = bindir / "codex"
        shim.write_text(
            '#!/bin/sh\nexec "{}" "{}" "$@"\n'.format(sys.executable, script),
            encoding="ascii",
        )
        shim.chmod(0o755)
    return bindir, Path(base) / "launched.jsonl"


def stand_in_env(bindir, records, act="none", arg="", thread=""):
    """The environment a call runs the stand-in under."""
    env = dict(os.environ)
    env["PATH"] = str(bindir) + os.pathsep + env.get("PATH", "")
    env.update(
        CODEX_STANDIN_RECORDS=str(records),
        CODEX_STANDIN_STREAM=str(GOLDEN_STREAM),
        CODEX_STANDIN_ACT=act,
        CODEX_STANDIN_ARG=arg,
        CODEX_STANDIN_THREAD=thread,
        CODEX_STANDIN_KIT=str(SCRIPTS),
        PYTHONIOENCODING="utf-8",
    )
    return env


def launches(records):
    """The stand-in's records, one per launch."""
    if not Path(records).exists():
        return []
    return [
        json.loads(line)
        for line in Path(records).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def run_call(args, env, cwd=None):
    """The entry point as a process: `(exit code, stdout + stderr)`."""
    proc = subprocess.run(
        [sys.executable, str(CALL_TOOL), *[str(a) for a in args]],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=str(cwd) if cwd else None,
        stdin=subprocess.DEVNULL,
        timeout=600,
    )
    return proc.returncode, proc.stdout + proc.stderr


def start_call(args, env):
    """The entry point as a process left running (for concurrent calls)."""
    return subprocess.Popen(
        [sys.executable, str(CALL_TOOL), *[str(a) for a in args]],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        stdin=subprocess.DEVNULL,
    )
