"""Coordinator lock and durable session-log support behavior.

Split byte-for-byte from ``test_agent_loop`` at WI-545's support boundary. The
fake-agent orchestration harness stays in the source module; cross-process lock
semantics and the session log/index regressions live here.
"""

import os
import subprocess
import sys

import pytest

from conftest import SCRIPTS, load_script

# --- the per-checkout coordinator lock (SR-027) --------------------------------
# Ported from the retired tracks suite (WI-210): the lock outlives the track
# lanes — the dispatcher, every worker, and an --interactive sitting take it.

# A probe that takes the lock in a SEPARATE process (the only way to observe the
# real cross-process kernel-lock contract). With `hard`, it dies without any
# release/atexit (os._exit) — modelling a crash so the caller can prove the OS
# auto-released the lock.
_LOCK_PROBE = """
import importlib.util, os, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("agent_loop", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
err = m.acquire_lock(Path(sys.argv[2]))
sys.stdout.write("REFUSED" if err else "ACQUIRED")
sys.stdout.flush()
if len(sys.argv) > 3 and sys.argv[3] == "hard":
    os._exit(0)
"""


def _probe_acquire(lock, hard_exit=False):
    argv = [
        sys.executable,
        "-c",
        _LOCK_PROBE,
        str(SCRIPTS / "agent_loop.py"),
        str(lock),
    ]
    if hard_exit:
        argv.append("hard")
    return subprocess.run(argv, capture_output=True, text=True).stdout.strip()


def test_lock_excludes_a_second_process(tmp_path):
    # The real contract: one coordinator per checkout. This process holds the
    # kernel lock; a separate process is refused, then succeeds once it's freed.
    agent_loop = load_script("agent_loop")
    lock = tmp_path / "out" / "agent-loop.lock"
    assert agent_loop.acquire_lock(lock) is None
    try:
        assert _probe_acquire(lock) == "REFUSED"
    finally:
        agent_loop.release_lock(lock)
    assert _probe_acquire(lock) == "ACQUIRED"


def test_lock_auto_released_when_holder_dies(tmp_path):
    # A holder that crashes without releasing must not wedge the next run —
    # the OS drops the advisory lock on process death. The probe acquires then
    # hard-exits (no release/atexit); this process must then acquire cleanly.
    agent_loop = load_script("agent_loop")
    lock = tmp_path / "out" / "agent-loop.lock"
    assert _probe_acquire(lock, hard_exit=True) == "ACQUIRED"
    assert agent_loop.acquire_lock(lock) is None
    agent_loop.release_lock(lock)


def test_lock_refuses_on_contention_errno(tmp_path, monkeypatch):
    # A genuine "held" errno (EWOULDBLOCK) must REFUSE — the guard is never
    # dropped on contention, and an unknown error stays a refusal too (fail-safe).
    import errno

    agent_loop = load_script("agent_loop")
    # The lock family lives in agent_common (WI-218 slice C): acquire_lock
    # resolves _take_os_lock in ITS namespace, so patch the instance
    # agent_loop actually imported (load_script would mint a fresh copy).
    agent_common = agent_loop.agent_common

    def _held(fd):
        raise OSError(errno.EWOULDBLOCK, "held")

    lock = tmp_path / "out" / "agent-loop.lock"
    monkeypatch.setattr(agent_common, "_take_os_lock", _held)
    err = agent_loop.acquire_lock(lock)
    assert err and "refusing to run two" in err


@pytest.mark.skipif(os.name == "nt", reason="advisory-lock degrade is POSIX-only")
def test_lock_degrades_on_unsupported_filesystem(tmp_path, monkeypatch, capsys):
    # A filesystem that cannot lock (ENOLCK) must DEGRADE — warn and proceed, not
    # fail closed on a legitimate run (Windows local FS always locks, so N/A there).
    import errno

    agent_loop = load_script("agent_loop")
    agent_common = agent_loop.agent_common  # the lock family's home (WI-218)

    def _unsupported(fd):
        raise OSError(errno.ENOLCK, "no locks available")

    lock = tmp_path / "out" / "agent-loop.lock"
    monkeypatch.setattr(agent_common, "_take_os_lock", _unsupported)
    assert agent_loop.acquire_lock(lock) is None  # proceeds, unguarded
    assert "without the one-coordinator" in capsys.readouterr().err.lower()
    agent_loop.release_lock(lock)


# --- repo-review 2026-07-21 regressions ---------------------------------------


def test_read_csv_rows_tolerates_a_bom(tmp_path):
    # M-23: an Excel-written BOM renamed the first header key to '﻿WI-ID',
    # so load_wi_registry returned {} while schedule.load_rows (utf-8-sig)
    # parsed fine — the dispatcher and the worker held two different views of
    # one registry, and a BOM'd system-requirements.csv silently vacated the
    # critique gate. The reader must strip the BOM and keep quoted multi-line
    # cells parseable. (The WI registry left CSV at Phase 5, so this reader now
    # serves the SR/TC registries — the regression it pins is the reader's, and
    # the original WI-shaped fixture is kept as the defect's own shape.)
    ac = load_script("agent_common")
    p = tmp_path / "work-items.csv"
    p.write_bytes(b'\xef\xbb\xbfWI-ID,Title,Status\nWI-001,"two\nline title",active\n')
    rows = ac._read_csv_rows(p)
    assert rows and rows[0].get("WI-ID") == "WI-001"  # not '﻿WI-ID'
    assert rows[0]["Title"] == "two\nline title"  # quoted newline survives


def test_session_log_header_carries_no_trailing_whitespace(tmp_path):
    # An empty header value used to render as `# guardrails: ` — a trailing
    # space in a TRACKED file, so every reviewer running `git diff --check`
    # over a lane range flagged the loop's own telemetry (three lanes in a
    # row on 2026-08-30). The header line is right-stripped.
    ac = load_script("agent_common")
    meta = {"session": "007", "stamp": "test", "guardrails": "", "commits": ""}
    path = ac.write_session_log(tmp_path, meta, "transcript\n")
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("# "):
            assert line == line.rstrip(), repr(line)
    assert "# guardrails:\n" in text


def test_session_log_header_carries_the_wi535_context_columns(tmp_path):
    ac = load_script("agent_common")
    meta = {
        "session": "007",
        "stamp": "test",
        "session-id": "cc77a65f-c2f7-4779-bd42-0be7e188a717",
        "context-used": 232598,
        "context-window": 1000000,
        "context-pct": 23,
    }
    path = ac.write_session_log(tmp_path, meta, "transcript\n")
    text = path.read_text(encoding="utf-8")
    assert "# session-id: cc77a65f-c2f7-4779-bd42-0be7e188a717\n" in text
    assert "# context-used: 232598\n" in text
    assert "# context-window: 1000000\n" in text
    assert "# context-pct: 23\n" in text
    meta_back = ac.read_log_meta(path)
    assert meta_back["context-pct"] == "23"


def test_regenerate_index_renders_the_ctx_pct_column(tmp_path):
    ac = load_script("agent_common")
    docs = tmp_path / "docs"
    (docs / "iteration").mkdir(parents=True)
    ac.write_session_log(
        docs / "iteration",
        {"session": "007", "stamp": "test", "context-pct": 23},
        "transcript\n",
    )
    ac.write_session_log(
        docs / "iteration",
        {"session": "008", "stamp": "test", "context-pct": ""},
        "transcript\n",
    )
    ac.regenerate_index(docs)
    text = (docs / "iteration_index.md").read_text(encoding="utf-8")
    assert "| Ctx % |" in text
    assert "| 23% |" in text
    assert "| — |" in text  # the blank row still renders a placeholder, not ""


def test_session_log_redacts_credential_shapes(tmp_path):
    # M-19: session transcripts are committed to tracked history; well-known
    # credential shapes must not land there verbatim (a CLI auth error echoing
    # a key was permanent history with only push-policy in the way).
    ac = load_script("agent_common")
    transcript = (
        "auth failed: invalid x-api-key sk-ant-api03-{}\n"
        "also: Bearer {} and AKIA{} here\n"
        "normal line stays intact\n"
    ).format("A" * 30, "B" * 30, "BCDEFGHIJKLMNOPQ")
    meta = {"session": "007", "stamp": "test"}
    path = ac.write_session_log(tmp_path, meta, transcript)
    text = path.read_text(encoding="utf-8")
    assert "[REDACTED]" in text
    assert "sk-ant-api03" not in text
    assert "AKIA" + "BCDEFGHIJKLMNOPQ" not in text  # split so the floor stays clean
    assert "normal line stays intact" in text
    assert "# redacted: 3 credential-shaped token(s)" in text


def test_session_log_redacts_credential_shapes_in_header_values(tmp_path):
    # The header is committed history too, and a verbatim raw-usage line can
    # carry the result text: header values pass the same redaction seam, and
    # the finding is still named by class and count, never by value.
    ac = load_script("agent_common")
    key = "sk-ant-api03-{}".format("C" * 30)
    meta = {
        "session": "008",
        "stamp": "test",
        "raw-usage": '[{"type":"result","result":"echo ' + key + '"}]',
    }
    path = ac.write_session_log(tmp_path, meta, "clean transcript\n")
    text = path.read_text(encoding="utf-8")
    header = text.split("# ---")[0]
    assert key not in text and "sk-ant-api03" not in header
    assert "[REDACTED]" in header
    assert "# redacted: 1 credential-shaped token(s)" in header
    assert "clean transcript" in text
