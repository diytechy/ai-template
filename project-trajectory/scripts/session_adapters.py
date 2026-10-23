#!/usr/bin/env python3
"""One adapter per provider CLI: the only place a CLI's differences live.

The kit launches three agent CLIs (claude, codex, opencode) and each speaks
differently: which flag makes it emit structured output, where its final text
is, which events carry its token usage, and how full its context window is.
Scattered through role code those differences would multiply. Each CLI gets
ONE adapter here, so every route preserves its usage and computes context
occupancy from the latest request, and every other module asks the adapter
instead of knowing the CLI.

An adapter is chosen by the CLI actually launched (the argv's executable
name), not by the routed family: the flags and the output grammar belong to
the program, and a stand-in agent (a test double, an adopter's wrapper) that
is none of the three gets the plain adapter, which changes nothing.

Stdlib only, Python 3.11+, Windows/POSIX. A coordinator-layer module: the
session service (`session_service`) imports it, and it imports no kit sibling.

Contracts: IF-245, IF-266 — the interface seam this module declares (process.md §8;
row of record in docs/requirements/interfaces.toml).

Contract IF-245: the per-CLI adapter surface. `adapter_for(argv)` returns the
    adapter for the executable `argv[0]` names (claude, codex or opencode by
    basename prefix, case-insensitive), else the plain adapter. Every adapter
    carries `cli` (its name, "" for the plain one) and five calls:
    `prepare(argv)` returns `(argv, scratch)` with the CLI's structured-output
    flags added once (codex `--json` and an `--output-last-message` temp file,
    whose path is `scratch`; opencode `--format json`); `final_text(stream,
    scratch, code)` returns the session's result text and removes the scratch
    file; `raw_usage(stream)` returns the CLI's usage-bearing events as a JSON
    array whose members are the CLI's own lines, byte for byte, or "" when it
    emitted none (claude's raw usage is the whole result event line verbatim;
    the line carries result text, so the log writer redacts header values);
    `usage(stream)` returns the usage record, one dict with exactly the keys
    of `USAGE_KEYS` for every CLI: the OpenTelemetry GenAI usage names pinned
    by `OTEL_SEMCONV`, input counted inclusive of cached input, the derived
    `fresh-input-tokens`, `cost-usd`, `raw-usage`, `usage-scope`, and the
    `cli` and `semconv` columns, a count the CLI does not report being ""
    (never 0); `context(stream, env, session_id)` returns
    `(session_id, used, window, pct)`, the context occupancy of the session's
    LATEST model request, each field "" where the CLI does not report it.
    The adapter reads the environment the call composed and never selects,
    replaces or infers an account home. The account home variables are an
    adapter fact (WI-798): `HOME_VARIABLES` per CLI (claude
    `CLAUDE_CONFIG_DIR`, codex `CODEX_HOME`, opencode `XDG_DATA_HOME` and
    `OPENCODE_CONFIG`, gemini `GEMINI_CLI_HOME`), `home_env(cli, home)` their
    values for one home, `cli_named(executable)` the CLI an executable
    launches, and `TOKEN_VARIABLES` the variable a token-account CLI reads its
    long-lived token from (claude `CLAUDE_CODE_OAUTH_TOKEN`).
    The Claude Code transcript reader: `claude_session(home, session_id)`
    reads the one session its caller names under the Claude home `home`
    (`<home>/projects/*/<id>.jsonl` and its `<id>/subagents/` transcripts
    and metas, never writing there) and returns a `SessionRead`: the
    session's own invocation, then each sub-agent's by depth and id, each
    with its identity, its final messages (each message id counted once, at
    its last record) and its open last message's id (a last message with no
    stop record, unless a sub-agent's finish notice in the session's
    transcripts was written at or after it); the refusals
    (`TranscriptRefused`, naming the file and the field of a shape outside
    the closed one, `TRANSCRIPT_TYPES` the record types it knows); and the
    transcripts named absent. `transcript_usage(messages)` returns the usage
    record of a run of counted messages, scoped `contribution`.
    `CLAUDE_RESULT_COUNTS_SUBAGENTS` states whether a `claude -p` result's
    usage already includes its sub-agents' (it does not). `claude_home(env)`
    is the ambient Claude home (the claude home variable when `env` sets
    it, else `~/.claude`), and `transcript_time(value)` the one parse of a
    transcript timestamp (an aware datetime, or None).

Contract IF-266: retained-call compaction observations. `compaction(stream,
env, session_id)` returns an empty mapping for other runners; codex returns
`reported` (a compacted rollout entry), `prompts` (rollout request inputs)
and `totals` (exec turn.completed running inputs). The keep operation owns
differencing across calls and clears its baseline on a kit reset.
"""

import json
import os
import re
import tempfile
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

# The usage vocabulary the record follows, PINNED to one commit: every name in
# the OpenTelemetry GenAI conventions is still at development stability, and
# they moved to their own repository in June 2026 with no tagged release, so
# "the latest" names nothing fixed. A later move is a rename plus a
# re-derivation from the raw usage every row keeps.
# Implements: SR-222, LLR-268
OTEL_SEMCONV = (
    "open-telemetry/semantic-conventions-genai@e57c543b4889619eb2a05702471937db5119165d"
)

# The token counts of the usage record, in the convention's inclusive form:
# `input_tokens` counts cached input for every provider, and the cache and
# reasoning counts are subsets of the input and output totals.
# Implements: SR-222, LLR-268
USAGE_COUNT_KEYS = (
    "gen_ai.usage.input_tokens",
    "gen_ai.usage.cache_read.input_tokens",
    "gen_ai.usage.cache_write.input_tokens",
    "gen_ai.usage.output_tokens",
    "gen_ai.usage.reasoning.output_tokens",
)

# Every column of the usage record, the same for every CLI.
# Implements: SR-222, LLR-268
USAGE_KEYS = (
    (
        "cli",
        "semconv",
        "gen_ai.provider.name",
        "gen_ai.response.model",
        "gen_ai.conversation.id",
    )
    + USAGE_COUNT_KEYS
    + (
        "fresh-input-tokens",
        "cost-usd",
        "usage-scope",
        "raw-usage",
    )
)


def json_events(stream):
    """The JSON-object lines of a CLI's newline-delimited output, in order,
    each paired with its original text: `[(event, line), ...]`.

    Non-JSON lines are skipped rather than fatal, because stderr is merged into
    the captured stream (a banner, a warning, a stack trace) and a CLI's
    diagnostics must not cost the events around them. Order is load-bearing:
    every "latest" rule below reads the last matching event.

    Implements: SR-222, LLR-266
    """
    events = []
    for line in (stream or "").splitlines():
        text = line.strip()
        if not text.startswith("{"):
            continue
        try:
            event = json.loads(text)
        except ValueError:
            continue
        if isinstance(event, dict):
            events.append((event, line))  # the line as written, not stripped
    return events


def _verbatim(lines):
    """A JSON array whose members are the given lines exactly as the CLI wrote
    them. Each line is already one JSON value, so joining them is valid JSON
    and loses nothing — a wrong later mapping is re-derived from here."""
    return "[" + ",".join(lines) + "]" if lines else ""


def _dig(node, *keys):
    """Walk nested mappings, returning None on any miss or non-mapping."""
    for key in keys:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def _count(value):
    """An int token count, or None: a bool or a string is not a count."""
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _pct(used, window):
    """`used` as a rounded percent of `window`, or "" unless both are counts
    and the window is positive — a missing window is never guessed."""
    if _count(used) is None or not _count(window):
        return ""
    return round(used * 100 / window)


def _sum(values):
    """The sum of the counts among `values`, or "" when none is a count."""
    counts = [v for v in values if _count(v) is not None]
    return sum(counts) if counts else ""


def usage_record(
    cli, provider, *, fresh, cache_read, cache_write, output, reasoning=None, **rest
):
    """One usage record from a CLI's own counts, so every adapter derives the
    inclusive input and the fresh input by ONE formula:

      input_tokens = fresh + cache read + cache write (inclusive)
      fresh-input-tokens = input_tokens - cache read - cache write

    `fresh`, the cache counts and `output` are the CLI's counts or None when
    it does not report them; input is blank only when none of its parts was
    reported. `rest` carries the non-count columns (`model`, `conversation`,
    `cost`, `scope`, `raw`).

    Implements: SR-222, LLR-268
    """
    parts = (fresh, cache_read, cache_write)
    total = _sum(parts)
    return {
        "cli": cli,
        "semconv": OTEL_SEMCONV,
        "gen_ai.provider.name": provider,
        "gen_ai.response.model": rest.get("model") or "",
        "gen_ai.conversation.id": rest.get("conversation") or "",
        "gen_ai.usage.input_tokens": total,
        "gen_ai.usage.cache_read.input_tokens": _blank(cache_read),
        "gen_ai.usage.cache_write.input_tokens": _blank(cache_write),
        "gen_ai.usage.output_tokens": _blank(output),
        "gen_ai.usage.reasoning.output_tokens": _blank(reasoning),
        "fresh-input-tokens": (
            total - (_count(cache_read) or 0) - (_count(cache_write) or 0)
            if total != ""
            else ""
        ),
        "cost-usd": _blank(rest.get("cost")),
        "usage-scope": rest.get("scope") or "unknown",
        "raw-usage": rest.get("raw") or "",
    }


def _blank(value):
    """A reported value as-is, an unreported one ("", never 0) as ""."""
    return "" if value is None else value


def _ensure(argv, *tokens):
    """`argv` with `tokens` appended unless its first token is already there."""
    return list(argv) if tokens[0] in argv else list(argv) + list(tokens)


class PlainAdapter:
    """The adapter for a CLI the kit does not know: it adds no flag, returns
    the stream as the result, and reads a claude-shaped result event if one
    is there. A stand-in therefore keeps its argv, final text and usage in the
    shape the claude reader returns."""

    cli = ""

    def prepare(self, argv):
        return list(argv), None

    def final_text(self, stream, scratch, code):
        return stream

    provider = ""

    def raw_usage(self, stream):
        return ""

    def usage(self, stream):
        """Read a stand-in's claude-shaped result; leave its provider unnamed."""
        return _claude_usage(self.cli, self.provider, stream)

    def context(self, stream, env=None, session_id=""):
        return "", "", "", ""

    def compaction(self, stream, env, session_id):
        """No compaction observation for an unknown or non-codex runner."""
        return {}

    def mint(self, argv):
        """`(argv, minted_id)` for a retained session's first call. A CLI
        the kit does not know is launched as it is: nothing minted."""
        return list(argv), ""

    def resume(self, argv, session_id):
        """The argv resuming `session_id`; unchanged for an unknown CLI."""
        return list(argv)

    def one_turn(self, argv):
        """The argv bounded to one model turn; unchanged where the CLI has
        no such bound."""
        return list(argv)

    def bounds_one_turn(self):
        """Whether this adapter overrides the no-bound `one_turn` default.

        Implements: SR-227, LLR-270
        """
        return type(self).one_turn is not PlainAdapter.one_turn


def _result_event(stream):
    """The `type: result` event of a stream-json transcript, else the last
    JSON object line, else `{}` (the historical `parse_json_result` rule: a
    trailing diagnostic never shadows the result)."""
    events = [event for event, _ in json_events(stream)]
    whole = (stream or "").strip()
    if not events and whole.startswith("{"):
        try:
            data = json.loads(whole)
        except ValueError:
            data = None
        events = [data] if isinstance(data, dict) else []
    for event in reversed(events):
        if event.get("type") == "result":
            return event
    return events[-1] if events else {}


def _claude_raw(stream):
    """claude's usage as emitted: its usage-bearing line, the result event,
    exactly as the CLI wrote it. Kept beside the parsed counts, never rebuilt
    from them, so a key order, a spacing or a field the adapter does not read
    survives. The line also carries the result text; the log writer redacts
    header values as it does the transcript."""
    lines = [ln for event, ln in json_events(stream) if event.get("type") == "result"]
    return _verbatim(lines[-1:])


def _claude_usage(cli, provider, stream):
    """The usage record of a claude-shaped result event.

    claude reports cached input APART from input (`input_tokens` is the fresh
    part), so the inclusive input is their sum. Its reasoning count is
    `usage.output_tokens_details.thinking_tokens`. The response model is the
    model the session's last assistant event named, else the result's own
    `model`, else the one `modelUsage` entry whose counters match the result's
    usage — never blank merely because a background model's entry sits beside
    it.

    Implements: SR-222, LLR-268
    """
    events = [event for event, _ in json_events(stream)]
    result = _result_event(stream)
    usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
    thinking = _dig(usage, "output_tokens_details", "thinking_tokens")
    return usage_record(
        cli,
        provider,
        fresh=_count(usage.get("input_tokens")),
        cache_read=_count(usage.get("cache_read_input_tokens")),
        cache_write=_count(usage.get("cache_creation_input_tokens")),
        output=_count(usage.get("output_tokens")),
        reasoning=_count(thinking),
        model=_claude_model(events, result, usage),
        conversation=result.get("session_id") or result.get("session-id") or "",
        cost=result.get("total_cost_usd"),
        scope="invocation" if usage else "",
        raw=_claude_raw(stream),
    )


def _claude_model(events, result, usage):
    """The model that answered: see `_claude_usage`."""
    for event in reversed(events):
        model = _dig(event, "message", "model")
        if event.get("type") == "assistant" and isinstance(model, str) and model:
            return model
    if isinstance(result.get("model"), str) and result["model"]:
        return result["model"]
    entries = result.get("modelUsage")
    entries = entries if isinstance(entries, dict) else {}
    pairs = (("input_tokens", "inputTokens"), ("output_tokens", "outputTokens"))
    matches = [
        name
        for name, entry in entries.items()
        if isinstance(entry, dict)
        and all(entry.get(b) == usage.get(a) for a, b in pairs)
    ]
    return matches[0] if len(matches) == 1 else ""


def _last_of(events, kind):
    """The last event of type `kind`, else `{}`."""
    return next((e for e in reversed(events) if e.get("type") == kind), {})


def _claude_last_request(events, result):
    """`(usage, model)` of the session's final model request: the last
    `assistant` event carrying `message.usage`, else the result's last
    `usage.iterations` entry (model unknown), else `({}, "")`."""
    for event in reversed(events):
        usage = _dig(event, "message", "usage")
        if event.get("type") == "assistant" and isinstance(usage, dict):
            return usage, _dig(event, "message", "model") or ""
    iterations = _dig(result, "usage", "iterations")
    last = iterations[-1] if isinstance(iterations, list) and iterations else None
    return (last if isinstance(last, dict) else {}), ""


class ClaudeAdapter(PlainAdapter):
    """claude `-p --output-format stream-json`: the route already emits
    structured output, so no flag is added; the stream is the result text the
    callers parse, and the result event carries the session's usage."""

    cli = "claude"
    provider = "anthropic"

    def mint(self, argv):
        """claude takes the session id at launch: `--session-id <uuid4>`.

        Implements: SR-227, LLR-270
        """
        minted = str(uuid.uuid4())
        return list(argv) + ["--session-id", minted], minted

    def resume(self, argv, session_id):
        """`--resume <id>`; the prompt still rides stdin.

        Implements: SR-227, LLR-270
        """
        return list(argv) + ["--resume", session_id]

    def one_turn(self, argv):
        """`--max-turns 1`: a keep-warm ping is one turn, never a session.

        Implements: SR-227, LLR-270
        """
        return list(argv) + ["--max-turns", "1"]

    def raw_usage(self, stream):
        return _claude_raw(stream)

    def context(self, stream, env=None, session_id=""):
        """Occupancy of the session's final model request.

        Source field: the LAST `assistant` event's `message.usage`, summing
        `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`
        — the prompt that request sent, which is how full the context was.
        Output tokens are not in it (they are the reply), and the result
        event's `usage` is not the source: it is CUMULATIVE over every model
        call in the session, so dividing it by the window read up to 34,836%.
        A stream with no assistant usage falls back to the result's last
        `usage.iterations` entry, the same per-request shape.

        The window is the `contextWindow` of the `modelUsage` entry for the
        model that request named; a background model's entry beside it is
        never taken for the session's own.

        Implements: SR-222, LLR-267
        """
        events = [event for event, _ in json_events(stream)]
        result = _last_of(events, "result")
        sid = session_id or result.get("session_id") or ""
        last, model = _claude_last_request(events, result)
        keys = (
            "input_tokens",
            "cache_read_input_tokens",
            "cache_creation_input_tokens",
        )
        if all(_count(last.get(k)) is None for k in keys):
            return sid, "", "", ""
        used = sum(_count(last.get(k)) or 0 for k in keys)
        window = _count(_dig(result, "modelUsage", model, "contextWindow")) or ""
        return sid, used, window, _pct(used, window)


# --- Claude Code transcripts: one session and its sub-agents, read from disk ---
#
# Claude Code writes each session's transcript to `<home>/projects/<cwd slug>/
# <session id>.jsonl`, and each sub-agent's, at any depth, flat beside it as
# `<session id>/subagents/agent-<agent id>.jsonl` with its
# `agent-<agent id>.meta.json`. The format is Claude Code's, not the kit's, so
# this reader is the only code that knows it: the shape it accepts is closed,
# and anything else is refused by file and field, never skipped.

# Whether a `claude -p` result's usage already includes the usage of the
# sub-agents the session spawned. Probed on Claude Code 2.1.296: a session
# with a foreground sub-agent reported exactly its main transcript's usage,
# not the sum with its sub-agent's, so it does not.
# Implements: SR-244, LLR-351
CLAUDE_RESULT_COUNTS_SUBAGENTS = False

# The record types a transcript may hold, surveyed over Claude Code 2.1.276
# to 2.1.306. A sub-agent's transcript holds six of them (`user`,
# `attachment`, `assistant` and the three `api-request*`). Only `assistant`
# records carry usage the reader counts; `usage` elsewhere (a parent's
# tool-result summary, an attachment) is never read. A type Claude Code adds
# later is refused until it is added here.
# Implements: SR-244, LLR-352
TRANSCRIPT_TYPES = frozenset(
    {
        "queue-operation",
        "user",
        "attachment",
        "file-history-snapshot",
        "atis-latch",
        "last-prompt",
        "ai-title",
        "assistant",
        "file-history-delta",
        "system",
        "cost-state",
        "mode",
        "bridge-session",
        "api-request-shape",
        "api-request-blob",
        "api-request",
        "artifact-comment-monitor",
        "artifact-autoreact-ledger",
        "frame-link",
        "custom-title",
        "agent-name",
    }
)

# The four counts of an assistant record's `message.usage`, every one required.
_TRANSCRIPT_COUNTS = (
    "input_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
    "output_tokens",
)

# A task notification names the agent it reports finished in this tag.
_TASK_ID = re.compile(r"<task-id>([^<]+)</task-id>")

_SUBAGENT_ENTRY = re.compile(
    r"^agent-(?P<id>[A-Za-z0-9_-]+)\.(?P<kind>jsonl|meta\.json)$"
)


class TranscriptRefused(Exception):
    """A transcript, meta or entry the reader does not know, naming the file
    (`path`) and the field (`field`) at fault.

    Implements: SR-244, LLR-352
    """

    def __init__(self, path, field):
        self.path = str(path)
        self.field = field
        super().__init__("{}: {}".format(self.path, field))


@dataclass(frozen=True)
class TranscriptMessage:
    """One final assistant message, counted once: its id and model, the
    timestamps of its first and last records, the four counts of its last
    record (`fresh` is `input_tokens`), the thinking count its stop record
    reports (None when it reports none), and whether a record of it carried a
    stop reason.

    Implements: SR-244, LLR-347
    """

    id: str
    model: str
    started_at: str
    ended_at: str
    fresh: int
    cache_read: int
    cache_write: int
    output: int
    thinking: object
    stopped: bool


@dataclass(frozen=True)
class TranscriptInvocation:
    """One transcript of a session: the session's own (`agent_id` "", depth
    0) or one sub-agent's, with its meta's identity, the model its spawner
    requested ("" when none), its final messages in order, its open last
    message's id ("" when none), and whether its parent agent is in the same
    directory.

    Implements: SR-244, LLR-347, LLR-348
    """

    session_id: str
    agent_id: str
    parent_agent_id: str
    depth: int
    agent_type: str
    request_model: str
    path: str
    messages: tuple
    open_message: str
    parent_resolved: bool


@dataclass(frozen=True)
class SessionRead:
    """What `claude_session` read: the invocations in order (the session's
    own, then the sub-agents by depth and id), the refusals
    (`TranscriptRefused`), and the transcripts named absent.

    Implements: SR-244, LLR-347
    """

    invocations: tuple = ()
    refusals: tuple = ()
    absent: tuple = ()


def _is_count(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _record_of(path, number, line):
    """One transcript line as a record of a known type, or refused."""
    try:
        record = json.loads(line)
    except ValueError:
        raise TranscriptRefused(path, "line {}: not JSON".format(number)) from None
    if not isinstance(record, dict):
        raise TranscriptRefused(path, "line {}: not a JSON object".format(number))
    kind = record.get("type")
    if kind not in TRANSCRIPT_TYPES:
        raise TranscriptRefused(
            path, "line {}: type {!r} is unknown".format(number, kind)
        )
    return record


def _assistant_fields(path, number, record, session_id, agent_id):
    """The checked `message` of one assistant record: every field the reader
    counts or keys on, typed, and bound to its session and transcript."""
    where = "line {}: ".format(number)
    message = record.get("message")
    if not isinstance(message, dict):
        raise TranscriptRefused(path, where + "message")
    for key in ("id", "model"):
        if not isinstance(message.get(key), str):
            raise TranscriptRefused(path, where + "message." + key)
    if not isinstance(record.get("timestamp"), str):
        raise TranscriptRefused(path, where + "timestamp")
    stop = message.get("stop_reason", ())
    if not (stop is None or isinstance(stop, str)):
        raise TranscriptRefused(path, where + "message.stop_reason")
    usage = message.get("usage")
    if not isinstance(usage, dict):
        raise TranscriptRefused(path, where + "message.usage")
    for key in _TRANSCRIPT_COUNTS:
        if not _is_count(usage.get(key)):
            raise TranscriptRefused(path, where + "message.usage." + key)
    _bind(path, where, record, session_id, agent_id)
    return message


def _bind(path, where, record, session_id, agent_id):
    """Refuse an assistant record of another session or transcript: the
    session's own carries `isSidechain` false and no `agentId`; a sub-agent's
    carries `isSidechain` true and its own file's `agentId`."""
    if record.get("sessionId") != session_id:
        raise TranscriptRefused(path, where + "sessionId")
    if record.get("isSidechain") is not bool(agent_id):
        raise TranscriptRefused(path, where + "isSidechain")
    if record.get("agentId", None) != (agent_id or None):
        raise TranscriptRefused(path, where + "agentId")


def _thinking(message):
    value = _dig(message, "usage", "output_tokens_details", "thinking_tokens")
    return value if _is_count(value) else None


def claude_home(env):
    """The ambient Claude home: the claude home variable
    (`HOME_VARIABLES["claude"]`) when the environment `env` sets it, else
    `~/.claude`, the home Claude Code itself uses there. It never selects an
    account home.

    Implements: SR-244, LLR-353
    """
    declared = env.get(HOME_VARIABLES["claude"][0], "")
    return Path(declared) if declared else Path.home() / ".claude"


def transcript_time(value):
    """A transcript timestamp as an aware datetime (UTC when it names no
    zone), or None when it is not one: the one parse of the timestamps
    Claude Code writes.

    Implements: SR-244, LLR-347
    """
    try:
        when = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def _finish_keys(record):
    """The finish notices one record carries: `("agent", id)` for each agent
    a task notification names (a `queue-operation` record), and `("call",
    tool use id)` for each tool result a `user` record holds."""
    if record["type"] == "queue-operation":
        content = record.get("content")
        found = _TASK_ID.findall(content) if isinstance(content, str) else []
        return [("agent", agent_id) for agent_id in found]
    if record["type"] == "user":
        content = _dig(record, "message", "content")
        return [
            ("call", block["tool_use_id"])
            for block in (content if isinstance(content, list) else ())
            if isinstance(block, dict)
            and block.get("type") == "tool_result"
            and isinstance(block.get("tool_use_id"), str)
        ]
    return []


def _note_finishes(record, evidence):
    """Record in `evidence` the latest time each finish notice in `record`
    was written."""
    keys = _finish_keys(record)
    when = transcript_time(record.get("timestamp")) if keys else None
    for key in keys if when is not None else ():
        evidence[key] = max(evidence.get(key, when), when)


def _transcript_messages(path, session_id, agent_id, evidence):
    """Every message of one transcript, each counted once, from its LAST
    record in file order (a message's records repeat, and only
    `output_tokens` grows across them), in the order of its first
    appearance. The finish notices the transcript carries are added to
    `evidence`; which messages are final is `_settled`'s call."""
    seen = {}
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            record = _record_of(path, number, line)
            _note_finishes(record, evidence)
            if record["type"] != "assistant":
                continue
            message = _assistant_fields(path, number, record, session_id, agent_id)
            entry = seen.setdefault(message["id"], {"first": record["timestamp"]})
            entry.update(last=record["timestamp"], message=message)
            if message.get("stop_reason") is not None:
                entry.update(stopped=True, thinking=_thinking(message))
    return tuple(_message(mid, entry) for mid, entry in seen.items())


def _settled(invocation, keys, evidence):
    """The invocation with its final messages and its open last message.

    A message is final when a record of it carries a stop reason, when a
    later assistant message follows it, or, for a sub-agent's last message,
    when the session's transcripts hold a notice that the agent finished,
    written at or after that message's last record: a task notification
    naming the agent, or, for an agent its spawner waited on, the spawner's
    tool result for the agent's call. A notice older than the message is no
    evidence (the agent was resumed after it). Only the last message can be
    none of these; it is left open: not counted, its id named.
    """
    messages = invocation.messages
    if not messages or messages[-1].stopped:
        return invocation
    ended = transcript_time(messages[-1].ended_at)
    if ended is not None and any(k in evidence and evidence[k] >= ended for k in keys):
        return invocation
    return replace(invocation, messages=messages[:-1], open_message=messages[-1].id)


def _message(mid, entry):
    message = entry["message"]
    usage = message["usage"]
    return TranscriptMessage(
        id=mid,
        model=message["model"],
        started_at=entry["first"],
        ended_at=entry["last"],
        fresh=usage["input_tokens"],
        cache_read=usage["cache_read_input_tokens"],
        cache_write=usage["cache_creation_input_tokens"],
        output=usage["output_tokens"],
        thinking=entry.get("thinking"),
        stopped=entry.get("stopped", False),
    )


def _meta(path):
    """`(agent type, depth, parent agent id, requested model, finish keys)`
    of one sub-agent meta, or refused naming the field. The finish keys are
    the notices that would show the agent finished: a task notification
    naming it, and, when its spawner waited on it (`requestShape`
    `foreground`), the tool result for its call (`toolUseId`)."""
    try:
        meta = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise TranscriptRefused(path, "meta: not readable JSON") from None
    if not isinstance(meta, dict):
        raise TranscriptRefused(path, "meta: not a JSON object")
    if not isinstance(meta.get("agentType"), str):
        raise TranscriptRefused(path, "agentType")
    depth = meta.get("spawnDepth")
    if not _is_count(depth) or depth < 1:
        raise TranscriptRefused(path, "spawnDepth")
    parent = meta.get("parentAgentId", "")
    if depth >= 2 and not (isinstance(parent, str) and parent):
        raise TranscriptRefused(path, "parentAgentId")
    model = meta.get("model")
    call = meta.get("toolUseId")
    waited = meta.get("requestShape") == "foreground" and isinstance(call, str)
    return (
        meta["agentType"],
        depth,
        parent or "",
        model if isinstance(model, str) else "",
        [("call", call)] if waited else [],
    )


def _subagent_files(directory):
    """`({agent id: {kind: path}}, refusals)` of a session's `subagents/`
    directory: every entry must be an `agent-<id>.jsonl` or
    `agent-<id>.meta.json` file, and each id must have both."""
    agents, refusals = {}, []
    if not directory.is_dir():
        return agents, refusals
    for entry in sorted(directory.iterdir()):
        matched = _SUBAGENT_ENTRY.match(entry.name)
        if not matched or not entry.is_file():
            refusals.append(
                TranscriptRefused(entry, "an entry the reader does not know")
            )
            continue
        agents.setdefault(matched.group("id"), {})[matched.group("kind")] = entry
    for agent_id, files in sorted(agents.items()):
        for kind, field in (("jsonl", "transcript"), ("meta.json", "meta")):
            if kind not in files:
                name = "agent-{}.{}".format(agent_id, kind)
                refusals.append(TranscriptRefused(directory / name, field))
    return agents, refusals


def _subagent(session_id, agent_id, files, present, evidence):
    """One sub-agent's unsettled invocation and its finish keys, or
    refused."""
    agent_type, depth, parent, model, keys = _meta(files["meta.json"])
    messages = _transcript_messages(files["jsonl"], session_id, agent_id, evidence)
    invocation = TranscriptInvocation(
        session_id=session_id,
        agent_id=agent_id,
        parent_agent_id=parent,
        depth=depth,
        agent_type=agent_type,
        request_model=model,
        path=str(files["jsonl"]),
        messages=messages,
        open_message="",
        parent_resolved=depth < 2 or parent in present,
    )
    return invocation, [("agent", agent_id)] + keys


def _holders(home, session_id):
    """The project directories under `home` holding the session's transcript
    or its directory."""
    projects = Path(home) / "projects"
    if not projects.is_dir():
        return []
    return [
        project
        for project in sorted(projects.iterdir())
        if (project / (session_id + ".jsonl")).is_file()
        or (project / session_id).is_dir()
    ]


def _main_invocation(main, session_id, evidence):
    """The session's own unsettled invocation; no notice finishes it."""
    messages = _transcript_messages(main, session_id, "", evidence)
    invocation = TranscriptInvocation(
        session_id=session_id,
        agent_id="",
        parent_agent_id="",
        depth=0,
        agent_type="",
        request_model="",
        path=str(main),
        messages=messages,
        open_message="",
        parent_resolved=True,
    )
    return invocation, []


def claude_session(home, session_id):
    """The session `session_id`'s transcripts under the Claude home `home`.

    The session is found as `<home>/projects/*/<id>.jsonl` and its
    `<id>/subagents/` directory. Held in two project directories, it is
    refused naming both; found in none, its transcript is named absent; a
    missing main transcript beside present sub-agents is named absent and the
    sub-agents are read. Each transcript, meta or entry of a shape the reader
    does not know is refused by file and field and nothing of that transcript
    is read; the others are. Every `spawnDepth` of 1 or more is accepted, and
    a parent that names no agent in the directory is kept as written and
    marked unresolved. Each transcript's last message is settled final or
    open (`_settled`) once every transcript's finish notices are read.

    Implements: SR-244, LLR-347, LLR-352
    """
    holders = _holders(home, session_id)
    if len(holders) > 1:
        both = "; ".join(str(h) for h in holders)
        refused = TranscriptRefused(
            both, "the session is held in more than one project directory"
        )
        return SessionRead(refusals=(refused,))
    if not holders:
        absent = Path(home) / "projects" / "*" / (session_id + ".jsonl")
        return SessionRead(absent=(str(absent),))
    read, absent, evidence = [], [], {}
    main = holders[0] / (session_id + ".jsonl")
    agents, refusals = _subagent_files(holders[0] / session_id / "subagents")
    if main.is_file():
        _collect(read, refusals, _main_invocation, main, session_id, evidence)
    else:
        absent.append(str(main))
    for agent_id, files in agents.items():
        if len(files) == 2:
            args = (session_id, agent_id, files, agents, evidence)
            _collect(read, refusals, _subagent, *args)
    settled = [_settled(inv, keys, evidence) for inv, keys in read]
    settled.sort(key=lambda inv: (inv.depth, inv.agent_id))
    return SessionRead(tuple(settled), tuple(refusals), tuple(absent))


def _collect(read, refusals, reader, *args):
    try:
        read.append(reader(*args))
    except TranscriptRefused as refused:
        refusals.append(refused)
    except OSError as error:
        refusals.append(TranscriptRefused(error.filename or args[0], "not readable"))


def transcript_usage(messages):
    """The usage record of a run of counted messages, through the one usage
    builder: fresh input, cache read, cache write and output summed; the
    reasoning count summed only when every message's stop record reports it
    (a partial sum is never shown as a count); the response model that of the
    last message not named `<synthetic>`.

    Implements: SR-244, LLR-347
    """
    messages = tuple(messages)
    if not messages:
        return usage_record(
            "claude",
            "anthropic",
            fresh=None,
            cache_read=None,
            cache_write=None,
            output=None,
            scope="contribution",
        )
    thinking = [m.thinking for m in messages]
    reported = all(m.stopped and t is not None for m, t in zip(messages, thinking))
    model = next((m.model for m in reversed(messages) if m.model != "<synthetic>"), "")
    return usage_record(
        "claude",
        "anthropic",
        fresh=sum(m.fresh for m in messages),
        cache_read=sum(m.cache_read for m in messages),
        cache_write=sum(m.cache_write for m in messages),
        output=sum(m.output for m in messages),
        reasoning=sum(thinking) if reported else None,
        model=model,
        scope="contribution",
    )


class CodexAdapter(PlainAdapter):
    """codex `exec`: `--json` makes stdout an event stream carrying the thread
    id and the turn's usage, and `--output-last-message` is still the final
    text. The two work together, so the usage is kept AND the result stays
    the CLI's own final-message contract (codex echoes its banner and the whole
    prompt into the captured stream, so the stream is never the result).

    Implements: SR-222, LLR-266
    """

    cli = "codex"

    def resume(self, argv, session_id):
        """`codex exec resume <id> ...`: the id goes right after `exec`, and
        a working-directory (`-C`) or `--ephemeral` flag is dropped, since the
        resumed thread must run in the repository and be kept. The first call
        mints nothing: codex reports its thread id in the `--json` stream.

        Implements: SR-227, LLR-270
        """
        argv = _without(_without(argv, "-C", value=True), "--ephemeral")
        if "exec" not in argv:
            return argv
        at = argv.index("exec") + 1
        return argv[:at] + ["resume", session_id] + argv[at:]

    def prepare(self, argv):
        argv, path = _codex_lastmsg_setup(_ensure(argv, "--json"))
        return argv, path

    def final_text(self, stream, scratch, code):
        last = _codex_lastmsg_read(scratch)
        return last if last and code == 0 else stream

    def raw_usage(self, stream):
        return _verbatim(
            [
                line
                for event, line in json_events(stream)
                if isinstance(event.get("usage"), dict)
            ]
        )

    provider = "openai"

    def usage(self, stream):
        """The usage record of a codex `exec --json` call.

        Source: the LAST event carrying a `usage` object (`turn.completed`).
        Cached input is inside `input_tokens`; cache writes are taken as
        included too, as the usage shape implies (not yet verified live).
        Fresh is input less cache read and write, clamped at zero.
        Cache write stays blank when absent; no response model is reported.
        Its turn usage is cumulative over the thread, which is one call for a
        fresh session (scope `thread`).

        Implements: SR-222, LLR-268
        """
        usage, thread = {}, ""
        for event, _ in json_events(stream):
            if isinstance(event.get("usage"), dict):
                usage = event["usage"]
            if event.get("type") == "thread.started":
                thread = event.get("thread_id") or thread
        total = _count(usage.get("input_tokens"))
        cached = _count(usage.get("cached_input_tokens"))
        written = _count(usage.get("cache_write_input_tokens"))
        return usage_record(
            self.cli,
            self.provider,
            fresh=(
                None
                if total is None
                else max(0, total - (cached or 0) - (written or 0))
            ),
            cache_read=cached,
            cache_write=written,
            output=_count(usage.get("output_tokens")),
            reasoning=_count(usage.get("reasoning_output_tokens")),
            conversation=thread,
            scope="thread" if usage else "",
            raw=self.raw_usage(stream),
        )

    def context(self, stream, env=None, session_id=""):
        """Occupancy of the thread's final model request.

        The `exec --json` stream's `turn.completed.usage` is CUMULATIVE over
        the thread, so it is never read as occupancy. The source field is the
        LAST rollout `token_count` event's `info.last_token_usage.input_tokens`
        (codex counts cached input inside input), read from the rollout file
        for exactly this thread id under the codex home `_codex_home` resolves
        (the launch's `CODEX_HOME`, else codex's own default), with
        `info.model_context_window` as the window. With no rollout for this
        thread there, occupancy stays blank.

        Implements: SR-222, LLR-267
        """
        sid = session_id
        for event, _ in json_events(stream):
            if event.get("type") == "thread.started" and event.get("thread_id"):
                sid = event["thread_id"]
        used, window = "", ""
        for event, _ in json_events(_codex_rollout(env, sid)):
            info = _dig(event, "payload", "info")
            if _dig(event, "payload", "type") != "token_count":
                continue
            value = _count(_dig(info, "last_token_usage", "input_tokens"))
            if value is not None:
                used = value
                window = _count(_dig(info, "model_context_window")) or window
        return sid, used, window, _pct(used, window)

    def compaction(self, stream, env, session_id):
        """Reported rollout compaction and prompt observations, kept apart
        from billed usage and occupancy. Exec inputs are running totals.

        Implements: SR-227, LLR-290
        """
        rollout = [e for e, _ in json_events(_codex_rollout(env, session_id))]
        prompts = [
            _dig(e, "payload", "info", "last_token_usage", "input_tokens")
            for e in rollout
            if _dig(e, "payload", "type") == "token_count"
        ]
        totals = [
            _dig(e, "usage", "input_tokens")
            for e, _ in json_events(stream)
            if e.get("type") == "turn.completed"
        ]
        return {
            "reported": any(e.get("type") == "compacted" for e in rollout),
            "prompts": [p for p in prompts if _count(p) is not None],
            "totals": [t for t in totals if _count(t) is not None],
        }


# The launch-environment variable codex takes its default home from: `HOME` on
# POSIX ("${CODEX_HOME:-$HOME/.codex}"). On Windows codex reads the OS profile
# and ignores a launch's HOME and USERPROFILE (`codex doctor` reports the same
# home under either override), so no launch variable applies there.
LAUNCH_HOME_VARIABLE = None if os.name == "nt" else "HOME"


def _codex_home(env):
    """The codex home a launch under `env` writes its rollouts to: its
    `CODEX_HOME` when set and non-empty, else codex's own default, `.codex`
    in the user's home (codex documents "default `CODEX_HOME` is
    `~/.codex`"). That home is the launch's `LAUNCH_HOME_VARIABLE` when it
    sets one, else this process's home. None when no home can be found."""
    env = env or {}
    if env.get("CODEX_HOME"):
        return Path(env["CODEX_HOME"])
    if LAUNCH_HOME_VARIABLE and env.get(LAUNCH_HOME_VARIABLE):
        return Path(env[LAUNCH_HOME_VARIABLE]) / ".codex"
    try:
        return Path.home() / ".codex"
    except (RuntimeError, OSError):
        return None


def _codex_rollout(env, thread_id):
    """The newest rollout file's text for exactly `thread_id` under the codex
    home `env` resolves to, or "" — the id makes the lookup exact, so no other
    thread is read."""
    home = _codex_home(env)
    if home is None or not thread_id:
        return ""
    try:
        pattern = "**/rollout-*-{}.jsonl".format(thread_id)
        found = list((home / "sessions").glob(pattern))
        if not found:
            return ""
        newest = max(found, key=lambda p: (p.stat().st_mtime_ns, str(p)))
        return newest.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _codex_lastmsg_setup(argv):
    """If argv launches codex, append its `--output-last-message` temp file and
    return (augmented_argv, path); otherwise (argv, None). codex echoes its banner
    + the whole prompt into stdout, so that file — its own final-message contract —
    is the deterministic session result (WI-217, gilbert 9add15b).

    Detection is a basename-prefix heuristic (accepted trade-off): a lookalike
    CLI named codex-* would receive the flag too, and a template that already
    declares its own -o/--output-last-message gets a second one (codex
    last-wins, so the kit's temp file is the one read back). Revisit as a
    declared registry column only if that ever bites a real registry.

    Implements: SR-026, LLR-026
    """
    if not (argv and _basename(argv[0]).startswith("codex")):
        return argv, None
    fd, path = tempfile.mkstemp(prefix="codex-lastmsg-", suffix=".txt")
    os.close(fd)
    return argv + ["--output-last-message", path], path


def _codex_lastmsg_read(path):
    """Read then delete the codex last-message file (`path` None for a non-codex
    session -> None). Best-effort: a missing/unreadable file reads as empty."""
    if path is None:
        return None
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        text = ""
    try:
        os.unlink(path)
    except OSError:
        pass
    return text


class OpencodeAdapter(PlainAdapter):
    """opencode `run`: `--format json` makes stdout an event stream whose
    `step_finish` events carry each model request's usage and whose `text`
    events carry the reply, so the final text is read out of the stream.

    Implements: SR-222, LLR-266
    """

    cli = "opencode"

    def resume(self, argv, session_id):
        """`--session <id>`. The first call mints nothing: opencode reports
        its `sessionID` in the `--format json` stream.

        Implements: SR-227, LLR-270
        """
        return list(argv) + ["--session", session_id]

    def prepare(self, argv):
        return _ensure(argv, "--format", "json"), None

    def final_text(self, stream, scratch, code):
        """The text of the last step that said anything. A stream with no
        JSON event at all (an error printed before the CLI started, or a CLI
        that ignored the flag) is returned as it came, so it stays visible."""
        events = json_events(stream)
        if not events:
            return stream
        steps, current = [], []
        for event, _ in events:
            if event.get("type") == "step_start":
                current = []
                steps.append(current)
            elif event.get("type") == "text":
                text = _dig(event, "part", "text")
                if isinstance(text, str):
                    if not steps:
                        steps.append(current)
                    current.append(text)
        spoken = [step for step in steps if "".join(step).strip()]
        return "".join(spoken[-1]) if spoken else ""

    def raw_usage(self, stream):
        return _verbatim(
            [line for event, line in json_events(stream) if _is_step_finish(event)]
        )

    def usage(self, stream):
        """The usage record of an opencode `run --format json` call.

        Source: every `step_finish` event's `part.tokens` and `part.cost`,
        summed — each step is one model request. opencode counts cached input
        apart from input (`input` is the fresh part) and reasoning apart from
        output, so output is `output + reasoning`, the convention's inclusive
        form. It names no provider (a gateway may route to any) and no
        response model, which stay blank.

        Implements: SR-222, LLR-268
        """
        steps = [
            _dig(event, "part") or {}
            for event, _ in json_events(stream)
            if _is_step_finish(event)
        ]
        tokens = [_dig(step, "tokens") or {} for step in steps]
        output = _sum([_dig(t, "output") for t in tokens])
        reasoning = _sum([_dig(t, "reasoning") for t in tokens])
        session = next(
            (e.get("sessionID") for e, _ in json_events(stream) if e.get("sessionID")),
            "",
        )
        return usage_record(
            self.cli,
            self.provider,
            fresh=_none(_sum([_dig(t, "input") for t in tokens])),
            cache_read=_none(_sum([_dig(t, "cache", "read") for t in tokens])),
            cache_write=_none(_sum([_dig(t, "cache", "write") for t in tokens])),
            output=_none(_sum([output, reasoning])),
            reasoning=_none(reasoning),
            conversation=session,
            cost=_none(_sum_cost([_dig(step, "cost") for step in steps])),
            scope="invocation" if steps else "",
            raw=self.raw_usage(stream),
        )

    def context(self, stream, env=None, session_id=""):
        """Occupancy of the session's final model request.

        Source field: the LAST `step_finish` event's `part.tokens`, summing
        `input + cache.read + cache.write` (opencode counts cached input apart
        from input). opencode reports no context window, so the percent stays
        blank rather than guessed.

        Implements: SR-222, LLR-267
        """
        sid, used = session_id, ""
        for event, _ in json_events(stream):
            sid = event.get("sessionID") or sid
            if not _is_step_finish(event):
                continue
            tokens = _dig(event, "part", "tokens")
            parts = (
                _count(_dig(tokens, "input")),
                _count(_dig(tokens, "cache", "read")),
                _count(_dig(tokens, "cache", "write")),
            )
            if any(p is not None for p in parts):
                used = sum(p or 0 for p in parts)
        return sid or "", used, "", ""


def _none(value):
    """`_sum`'s "" (nothing reported) as None, the record builder's absent."""
    return None if value == "" else value


def _sum_cost(values):
    """The sum of the numeric costs among `values`, or "" when there is none."""
    costs = [
        v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)
    ]
    return sum(costs) if costs else ""


def _without(argv, flag, value=False):
    """`argv` with every `flag` removed, and the token after it when the
    flag takes a value."""
    out, skip = [], False
    for tok in argv:
        if skip:
            skip = False
        elif tok == flag:
            skip = value
        else:
            out.append(tok)
    return out


def reported_error(stream):
    """Whether the runner's own result says the session failed (claude's
    `is_error`), whatever its exit code — an unusable retained session.

    Implements: SR-227, LLR-270
    """
    return _result_event(stream).get("is_error") is True


# The error class claude (2.1.289) tags its synthetic assistant event with when
# the API refuses the credential (HTTP 401 or 403). Other failures carry other
# classes: the OAuth-refresh failure of 2026-10-06 was tagged `server_error`.
AUTH_FAILED = "authentication_failed"


def auth_failed(stream):
    """Whether the runner says its credential was refused: an `assistant`
    event whose `error` is claude's `authentication_failed`. Such a call
    failed, but says nothing about the retained session it ran in.

    Implements: SR-227, LLR-270
    """
    return any(
        event.get("type") == "assistant" and event.get("error") == AUTH_FAILED
        for event, _ in json_events(stream)
    )


def _is_step_finish(event):
    return event.get("type") == "step_finish"


def _basename(executable):
    return os.path.basename(executable or "").lower()


# The adapters by executable-name prefix, in the one order they are tried.
_BY_PREFIX = (
    ("claude", ClaudeAdapter()),
    ("codex", CodexAdapter()),
    ("opencode", OpencodeAdapter()),
)
_PLAIN = PlainAdapter()


def adapter_for(argv):
    """The adapter for the CLI `argv` launches, else the plain adapter.

    Implements: SR-222, LLR-266
    """
    name = _basename(argv[0]) if argv else ""
    return next((a for prefix, a in _BY_PREFIX if name.startswith(prefix)), _PLAIN)


# The home variables of each CLI an account may name (WI-798, IF-245): the
# environment that moves the CLI's user layer, and with it its sign-in, into an
# account's home. opencode keeps its data and its config apart, so it takes two.
# A CLI outside this table cannot be named by an account.
# Implements: SR-222, LLR-266
HOME_VARIABLES = {
    "claude": ("CLAUDE_CONFIG_DIR",),
    "codex": ("CODEX_HOME",),
    "opencode": ("XDG_DATA_HOME", "OPENCODE_CONFIG"),
    "gemini": ("GEMINI_CLI_HOME",),
}

# The variable each CLI reads a long-lived token from in headless use, for an
# account that authenticates with one (`claude setup-token`, 2.1.289: "Use this
# token by setting: export CLAUDE_CODE_OAUTH_TOKEN=<token>"). Only these CLIs can
# carry a token account.
# Implements: SR-222, LLR-266
TOKEN_VARIABLES = {"claude": "CLAUDE_CODE_OAUTH_TOKEN"}


def cli_named(executable):
    """The CLI of `HOME_VARIABLES` an executable name launches, by the
    basename prefix `adapter_for` uses (case-insensitive), or "" for none.

    Implements: SR-222, LLR-266
    """
    name = _basename(executable)
    return next((cli for cli in HOME_VARIABLES if name.startswith(cli)), "")


def home_env(cli, home):
    """`{variable: value}` placing `cli`'s user layer in the account home
    `home`: the home itself for claude, codex and gemini; for opencode its data
    under `<home>/data` and its config at `<home>/opencode.json`. `{}` for a CLI
    outside `HOME_VARIABLES`.

    Implements: SR-222, LLR-266
    """
    if cli == "opencode":
        return {
            "XDG_DATA_HOME": str(Path(home) / "data"),
            "OPENCODE_CONFIG": str(Path(home) / "opencode.json"),
        }
    return {name: str(home) for name in HOME_VARIABLES.get(cli, ())}
