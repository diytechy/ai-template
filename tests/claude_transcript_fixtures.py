"""The Claude Code transcript fixtures and the tmp-copy builders the reader
and the usage-ingest tests share. Not a test module (no `test_` prefix).

The fixtures in `tests/golden/sessions/claude-transcripts/` are cut from
real transcripts on the authoring box (Claude Code 2.1.29x, 2026-10-20 and
2026-10-22) by a throwaway script kept outside the repository. The cut keeps
each record's `type`, `uuid`, `parentUuid`, `isSidechain`, `sessionId`,
`agentId`, `timestamp` and `requestId`; each assistant record's message id,
model, usage and stop reason, and only the type of each content block; and
the numbers of a parent's tool-result summary (`toolUseResult.usage`) and of
an attachment's `usage`. Of the records that evidence an agent finished it
keeps only the ids: a user record's tool-result blocks keep their
`tool_use_id`, and a `queue-operation` task notification keeps only the
agent id it names. It removes all text, tool inputs and outputs, `cwd`
and `gitBranch`, and a meta's `description`, and it moves the project slug to
a neutral `projects/work/`. Two sessions:

- `NESTED` (2026-10-20): a session, its depth-1 agent and that agent's two
  depth-2 children, each transcript cut to a prefix ending on a stop record.
  One depth-2 agent (`AF7`) holds a message with no stop record that a later
  message follows.
- `CHAIN` (2026-10-22, the depth probe): a `claude -p` session whose
  sub-agent started one, which started one more (depths 1, 2 and 3), kept
  whole. Each sub-agent ends on its hand-back message, which has no stop
  record. `result-usage.json` keeps the four counts of the session's own JSON
  result.
"""

import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

FIXTURES = Path(__file__).parent / "golden" / "sessions" / "claude-transcripts"
SLUG = "work"

NESTED = "a9702b22-87dd-4225-a8ed-6bcb0f50ff5b"
A23 = "a23fb99a1cbf26cd0"  # depth 1
A7B = "a7b5ec7e25fa81ae4"  # depth 2, parent A23
AF7 = "af7af850ede96a6fe"  # depth 2, parent A23; holds the no-stop message
AF7_NO_STOP = "msg_011CgDDtzftpKogRCT3EY9od"
AF7_LAST = "msg_011CgDDuXy4bvBfrgfBpkqFt"
A23_THIRD = "msg_011CgD8mgMYYq69sE6qvpnqm"

CHAIN = "125152ca-33e0-45be-93dd-a7820b0bf88a"
C1 = "a8ec19fa90d465496"  # depth 1
C2 = "a6dfd1d19f92f4751"  # depth 2, parent C1
C3 = "ad5873fd539451867"  # depth 3, parent C2
# Each CHAIN agent's last message: its hand-back, with no stop record. Each
# agent is foreground, and its parent's tool result for the meta's
# `toolUseId` follows that message: the evidence that the agent finished.
C1_LAST = "msg_011CgJ77RWB6B29mRzrxUEyU"
C2_LAST = "msg_011CgJ77E5anins2BcZLvXiF"
C3_LAST = "msg_011CgJ775SRGz3kEmip3bqB8"
C3_TOOL_USE = "toolu_016AAe54xMxEqWBa1ie3goMh"  # in C2's transcript

COUNTS = (
    "input_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
    "output_tokens",
)


def home_copy(tmp_path):
    """A writable Claude home under `tmp_path` holding both fixture sessions
    at `projects/work/`. Returns the home."""
    home = Path(tmp_path) / "claude-home"
    shutil.copytree(FIXTURES / "projects", home / "projects")
    return home


def session_dir(home):
    return Path(home) / "projects" / SLUG


def transcript(home, session, agent=""):
    """The path of the session's own transcript, or one sub-agent's."""
    if not agent:
        return session_dir(home) / (session + ".jsonl")
    return session_dir(home) / session / "subagents" / ("agent-%s.jsonl" % agent)


def meta(home, session, agent):
    return session_dir(home) / session / "subagents" / ("agent-%s.meta.json" % agent)


def result_usage():
    """The four counts of the CHAIN session's own `claude -p` JSON result."""
    data = json.loads((FIXTURES / "result-usage.json").read_text(encoding="utf-8"))
    return data["session_id"], data["usage"]


def read_lines(path):
    return Path(path).read_text(encoding="utf-8").splitlines(keepends=True)


def write_lines(path, lines):
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        fh.write("".join(lines))


def append_lines(path, lines):
    with Path(path).open("a", encoding="utf-8", newline="") as fh:
        fh.write("".join(lines))


def records(path):
    return [json.loads(line) for line in read_lines(path)]


def _is_record_of(line, message_id):
    rec = json.loads(line)
    return rec.get("type") == "assistant" and rec["message"]["id"] == message_id


def cut_after_first_record(path, message_id):
    """Cut the transcript at `path` just after the first record of
    `message_id` (a record with no stop reason), as a read made while the
    message was being written sees it. Returns the removed lines."""
    lines = read_lines(path)
    for n, line in enumerate(lines):
        if _is_record_of(line, message_id):
            assert json.loads(line)["message"]["stop_reason"] is None, line
            write_lines(path, lines[: n + 1])
            return lines[n + 1 :]
    raise AssertionError("no record of {} in {}".format(message_id, path))


def cut_after_message(path, message_id):
    """Cut the transcript at `path` just after the last record of
    `message_id`. Returns the removed lines."""
    lines = read_lines(path)
    last = max(n for n, line in enumerate(lines) if _is_record_of(line, message_id))
    write_lines(path, lines[: last + 1])
    return lines[last + 1 :]


def tool_result_line(path, tool_use_id):
    """The index of the `user` record at `path` carrying the tool result
    for `tool_use_id`."""
    for n, rec in enumerate(records(path)):
        content = (rec.get("message") or {}).get("content")
        if rec.get("type") == "user" and isinstance(content, list):
            if any(b.get("tool_use_id") == tool_use_id for b in content):
                return n
    raise AssertionError("no tool result for {} in {}".format(tool_use_id, path))


def task_notice(session, agent, timestamp):
    """A `queue-operation` line announcing that the background agent
    `agent` finished, in the shape the cut keeps."""
    content = "<task-notification><task-id>{}</task-id></task-notification>"
    return (
        json.dumps(
            {
                "type": "queue-operation",
                "sessionId": session,
                "timestamp": timestamp,
                "content": content.format(agent),
            }
        )
        + "\n"
    )


def restamp(lines, second):
    """`lines` with every record timestamp moved into the UTC second
    `second` (`YYYY-mm-ddTHH:MM:SS`), its fraction kept."""
    out = []
    for line in lines:
        rec = json.loads(line)
        if "timestamp" in rec:
            fraction = rec["timestamp"][19:]
            rec["timestamp"] = second + fraction
        out.append(json.dumps(rec) + "\n")
    return out


def last_timestamp(path):
    """The timestamp of the last assistant record at `path`."""
    stamps = [r["timestamp"] for r in records(path) if r.get("type") == "assistant"]
    return stamps[-1]


def local_stamp(timestamp):
    """A transcript timestamp as a log name's local `YYYYmmdd-HHMMSS`."""
    when = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone()
    return when.strftime("%Y%m%d-%H%M%S")


def next_second(stamp):
    """The log name stamp one second after `stamp`."""
    when = datetime.strptime(stamp, "%Y%m%d-%H%M%S") + timedelta(seconds=1)
    return when.strftime("%Y%m%d-%H%M%S")


def message_sums(path, which="last"):
    """An independent count over the transcript at `path`: the four counts
    summed once per message id from each message's `last` or `first`
    record, or over `all` records."""
    first, last, every = {}, {}, [0, 0, 0, 0]
    for rec in records(path):
        if rec.get("type") != "assistant":
            continue
        mid = rec["message"]["id"]
        counts = [rec["message"]["usage"][k] for k in COUNTS]
        first.setdefault(mid, counts)
        last[mid] = counts
        every = [a + b for a, b in zip(every, counts)]
    if which == "all":
        return tuple(every)
    chosen = first if which == "first" else last
    return tuple(sum(c[i] for c in chosen.values()) for i in range(4))


def four(usage):
    """The four counts of a usage record, in `COUNTS` order: fresh input,
    cache read, cache write and output."""
    return (
        usage["fresh-input-tokens"],
        usage["gen_ai.usage.cache_read.input_tokens"],
        usage["gen_ai.usage.cache_write.input_tokens"],
        usage["gen_ai.usage.output_tokens"],
    )


def header_four(meta_):
    """The four counts of a log header, as ints."""
    keys = (
        "fresh-input-tokens",
        "gen_ai.usage.cache_read.input_tokens",
        "gen_ai.usage.cache_write.input_tokens",
        "gen_ai.usage.output_tokens",
    )
    return tuple(int(meta_[k]) for k in keys)
