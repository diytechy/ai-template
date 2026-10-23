#!/usr/bin/env python3
"""Record the usage of a Claude Code session and its sub-agents, once per
invocation, from the session's transcripts.

A coordinator's own session, and every sub-agent it or its workers spawn at
any depth, makes model calls the kit never launched, so the session service
never recorded them. Claude Code keeps each one's transcript on disk; this
command reads them through `session_adapters.claude_session` and records each
transcript's not-yet-recorded final messages as one contribution: one session
log, written by `session_service.record` (committed in a claimed lane,
spooled anywhere else), under an invocation id derived from the transcript's
identity, so a repeated, resumed or interrupted run adds only what no earlier
log holds. A session whose main transcript the service already recorded is
not counted twice. The logs carry a usage summary only, never transcript
text, and a role no gate reads (`COORDINATOR`, `SUBAGENT`).

Stdlib only, Python 3.11+, Windows/POSIX. A coordinator-layer command.

Contracts: IF-305, IF-306, IF-307 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-305: the usage-ingest command line.
    `usage_ingest.py [--session ID] [--root DIR]` ingests the session ID,
    else the one `CLAUDE_CODE_SESSION_ID` names, from the ambient Claude
    home (`CLAUDE_CONFIG_DIR` when set, else `~/.claude`); it never selects
    an account home. DIR (default the working directory) is the root the
    contributions are recorded from.

Contract IF-306: the command's stdout readings. It prints one line per
    invocation, naming the role, agent type and agent id: `recorded`
    (message count, input and output totals, `known` or `partial`, the
    log's path, and spooled, committed or commit refused), `unchanged`,
    `open <message id>` (the transcript's last message, left for a later
    ingest), `skipped` (with the service log that recorded the session),
    `refused`, `absent`, or `parent unresolved`. A transcript refused for
    its shape is printed as `refused <file>: <field>`, with no prefix.

Contract IF-307: the command's exit codes. Exit 0 when nothing was
    refused or absent and no commit was refused (an `open` line does not
    change it), 1 on a refusal, an absent transcript or a refused record
    commit, and 2 when no session is named.
"""

import argparse
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import agent_common
import session_adapters
import session_service

# The namespace every invocation id is derived in: a fixed constant, so one
# transcript always gets the same id, on every box and every run.
INGEST_NAMESPACE = uuid.UUID("4f1d6c0e-9b3a-5e27-8c41-7a2d9e6b0f53")

COORDINATOR = "COORDINATOR"
SUBAGENT = "SUBAGENT"
OUTCOME = "INGESTED"
STAMP = "%Y%m%d-%H%M%S"


class _Refused(Exception):
    """One invocation refused, naming the file and the cause."""


def invocation_id(session_id, agent_id):
    """The invocation id of one transcript: 32 hex digits, a uuid5 of the
    session id and the agent id ("" for the session's own transcript), so a
    re-read of the same transcript keys the same invocation.

    Implements: SR-244, LLR-348
    """
    return uuid.uuid5(INGEST_NAMESPACE, "{}/{}".format(session_id, agent_id)).hex


def record_dirs(root):
    """Every directory a contribution of this root may already sit in: the
    primary checkout's spool, the root's own `docs/iteration/`, and the
    `docs/iteration/` of every worktree git lists.

    Implements: SR-244, LLR-350
    """
    dirs = [session_service.spool_dir(root), Path(root) / "docs" / "iteration"]
    for path, _branch in agent_common.worktree_records(root):
        dirs.append(Path(path) / "docs" / "iteration")
    return dirs


def recorded_logs(root):
    """`{name: path}` of every session log in `record_dirs(root)`,
    de-duplicated by file name.

    Implements: SR-244, LLR-350
    """
    logs = {}
    for directory in record_dirs(root):
        if directory.is_dir():
            for path in sorted(directory.glob("*.log")):
                logs.setdefault(path.name, path)
    return logs


def _header(path):
    """The header of one log, refused when unreadable or cut short."""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            meta, terminated = agent_common.log_meta_text(handle)
    except OSError:
        raise _Refused("{}: its header cannot be read".format(path)) from None
    if not terminated:
        raise _Refused("{}: its header has no `# ---` terminator".format(path))
    return meta


def prior_contributions(logs, inv_id):
    """`(cursors, latest stamp)` of the contributions already recorded for
    one invocation, found by name; refused, naming the log, when a header is
    unreadable, cut short, or lacks its cursor or contribution key. Reads
    only.

    Implements: SR-244, LLR-350
    """
    prefix = "call_{}-".format(inv_id)
    cursors, latest = [], ""
    for name in sorted(n for n in logs if n.startswith(prefix)):
        named = session_service.CALL_LOG_RE.match(name)
        if named is None:
            continue
        meta = _header(logs[name])
        for key in ("message-cursor", "contribution-key"):
            if not meta.get(key):
                raise _Refused("{}: its header has no {}".format(logs[name], key))
        cursors.append((meta["message-cursor"], logs[name]))
        latest = max(latest, named.group("stamp"))
    return cursors, latest


def service_record(logs, session_id, own):
    """`(service log name or "", unreadable log or "")` for a session: the
    first log, among those not named for one of this session's own
    invocations (`own`), whose header carries the session id with a usage
    source other than `transcript`, a record the session service wrote.

    Implements: SR-244, LLR-351
    """
    unreadable = ""
    for name, path in sorted(logs.items()):
        if any(name.startswith("call_{}-".format(inv)) for inv in own):
            continue
        try:
            meta = _header(path)
        except _Refused as refused:
            unreadable = unreadable or str(refused)
            continue
        if (
            meta.get("session-id") == session_id
            and meta.get("usage-source") != "transcript"
        ):
            return name, unreadable
    return "", unreadable


def new_messages(inv, cursors):
    """The final messages after the furthest recorded cursor, in the
    transcript's order; refused, naming the log, when a cursor is not in the
    transcript.

    Implements: SR-244, LLR-350
    """
    ids = [m.id for m in inv.messages]
    start = 0
    for cursor, path in cursors:
        if cursor not in ids:
            raise _Refused(
                "{}: its cursor {} is not in the transcript".format(path, cursor)
            )
        start = max(start, ids.index(cursor) + 1)
    return inv.messages[start:]


def _local(timestamp):
    """A transcript timestamp in local time, through the adapter's parse."""
    return session_adapters.transcript_time(timestamp).astimezone()


def name_stamp(last_message, latest):
    """The log name's stamp: the last counted message's local time, or one
    second after the latest stamp an earlier contribution of the invocation
    holds when that is not earlier, so names rise and never collide.

    Implements: SR-244, LLR-349
    """
    stamp = _local(last_message.ended_at).strftime(STAMP)
    if latest and latest >= stamp:
        later = datetime.strptime(latest, STAMP) + timedelta(seconds=1)
        stamp = later.strftime(STAMP)
    return stamp


def _role(inv):
    return COORDINATOR if not inv.agent_id else SUBAGENT


def contribution_row(inv, messages, latest):
    """The session-log row of one contribution: its identity, range, usage
    record and status; every other column empty.

    Implements: SR-244, LLR-348, LLR-349, LLR-354
    """
    inv_id = invocation_id(inv.session_id, inv.agent_id)
    first, last = messages[0], messages[-1]
    usage = session_adapters.transcript_usage(messages)
    row = dict(usage)
    row.update(
        {
            "session": "call_" + inv_id,
            "stamp": name_stamp(last, latest),
            "date": _local(last.ended_at).strftime("%Y-%m-%d %H:%M"),
            "phase": _role(inv),
            "role": _role(inv),
            "outcome": OUTCOME,
            "model": usage["gen_ai.response.model"],
            "gen_ai.request.model": inv.request_model,
            "gen_ai.conversation.id": inv.session_id,
            "session-id": inv.session_id,
            "invocation-id": inv_id,
            "usage-source": "transcript",
            "usage-scope": "contribution",
            "usage-status": "known" if all(m.stopped for m in messages) else "partial",
            "raw-usage": "",
            "agent-id": inv.agent_id,
            "parent-agent-id": inv.parent_agent_id,
            "spawn-depth": inv.depth,
            "agent-type": inv.agent_type,
            "message-count": len(messages),
            "message-cursor": last.id,
            "contribution-key": "{}:{}:{}".format(inv_id, first.id, last.id),
            "started-at": first.started_at,
            "ended-at": last.ended_at,
        }
    )
    return row


def summary(inv, messages, row):
    """The log body: counts, message ids and timestamps only, never any
    transcript text.

    Implements: SR-244, LLR-354
    """
    unstopped = sum(1 for m in messages if not m.stopped)
    return "\n".join(
        [
            "usage ingest of one transcript contribution",
            "role: {}".format(row["role"]),
            "messages counted: {} ({} without a stop record)".format(
                len(messages), unstopped
            ),
            "first message: {} at {}".format(messages[0].id, messages[0].started_at),
            "last message: {} at {}".format(messages[-1].id, messages[-1].ended_at),
            "fresh input: {}".format(row["fresh-input-tokens"]),
            "cache read: {}".format(row["gen_ai.usage.cache_read.input_tokens"]),
            "cache write: {}".format(row["gen_ai.usage.cache_write.input_tokens"]),
            "output: {}".format(row["gen_ai.usage.output_tokens"]),
            "open message: {}".format(inv.open_message or "none"),
        ]
    )


def _shown(root, path):
    try:
        return Path(path).relative_to(root).as_posix()
    except ValueError:
        return str(path)


def record_contribution(root, inv, messages, latest):
    """Record one contribution through the session service; `(line, failed)`.

    Implements: SR-244, LLR-349, LLR-354, LLR-355
    """
    row = contribution_row(inv, messages, latest)
    outcome = session_service.Outcome(
        root, 0, "", False, summary(inv, messages, row), {}
    )
    report = {}
    path = session_service.record(outcome, row, report=report)
    where = "spooled" if report.get("spooled") else "committed"
    if report.get("refusal"):
        where = "commit refused: " + " ".join(report["refusal"].split())
    line = "recorded {} messages, input {}, output {}, {}, {}, {}".format(
        len(messages),
        row["gen_ai.usage.input_tokens"],
        row["gen_ai.usage.output_tokens"],
        row["usage-status"],
        _shown(root, path),
        where,
    )
    return line, bool(report.get("refusal"))


def ingest_one(root, inv, logs):
    """The report lines of one invocation, and whether it failed.

    Implements: SR-244, LLR-350, LLR-355
    """
    lines, failed = [], False
    try:
        cursors, latest = prior_contributions(
            logs, invocation_id(inv.session_id, inv.agent_id)
        )
        messages = new_messages(inv, cursors)
    except _Refused as refused:
        return ["refused " + str(refused)], True
    if messages:
        line, failed = record_contribution(root, inv, messages, latest)
        lines.append(line)
    else:
        lines.append("unchanged")
    if inv.open_message:
        lines.append("open " + inv.open_message)
    if not inv.parent_resolved:
        lines.append("parent unresolved " + inv.parent_agent_id)
    return lines, failed


def _prefix(role, agent_type, agent_id):
    return "{} {} {}:".format(role, agent_type or "-", agent_id or "-")


def _skip(inv, service, unreadable):
    """The line that holds an invocation back from the service-recorded
    session check, or None; and whether it is a refusal."""
    governed = not inv.agent_id or session_adapters.CLAUDE_RESULT_COUNTS_SUBAGENTS
    if not governed:
        return None, False
    if service:
        return "skipped (the service log {} holds it)".format(service), False
    if unreadable:
        return "refused " + unreadable, True
    return None, False


def ingest(root, home, session_id, emit=print):
    """Ingest one session's transcripts; the exit code.

    Implements: SR-244, LLR-350, LLR-351, LLR-353, LLR-355
    """
    read = session_adapters.claude_session(home, session_id)
    failed = False
    for refused in read.refusals:
        emit("refused {}: {}".format(refused.path, refused.field))
        failed = True
    for path in read.absent:
        emit("{} absent {}".format(_prefix(COORDINATOR, "", ""), path))
        failed = True
    logs = recorded_logs(root)
    own = [invocation_id(session_id, inv.agent_id) for inv in read.invocations]
    own.append(invocation_id(session_id, ""))
    service, unreadable = service_record(logs, session_id, own)
    for inv in read.invocations:
        prefix = _prefix(_role(inv), inv.agent_type, inv.agent_id)
        held, refused = _skip(inv, service, unreadable)
        if held:
            emit("{} {}".format(prefix, held))
            failed = failed or refused
            continue
        lines, bad = ingest_one(root, inv, logs)
        for line in lines:
            emit("{} {}".format(prefix, line))
        failed = failed or bad
    return 1 if failed else 0


def main(argv=None):
    """The command line (Contract IF-305).

    Implements: SR-244, LLR-348, LLR-353, LLR-355
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--session", default="", help="the session id to ingest")
    parser.add_argument("--root", default=".", help="the root to record from")
    args = parser.parse_args(argv)
    session_id = args.session or os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if not session_id:
        print(
            "usage_ingest: no session: pass --session ID, or run inside a "
            "Claude Code session (CLAUDE_CODE_SESSION_ID)."
        )
        return 2
    root = Path(args.root).resolve()
    return ingest(root, session_adapters.claude_home(os.environ), session_id)


if __name__ == "__main__":
    sys.exit(main())
