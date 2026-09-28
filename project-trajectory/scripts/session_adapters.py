#!/usr/bin/env python3
"""One adapter per provider CLI: the only place a CLI's differences live.

The kit launches three agent CLIs (claude, codex, opencode) and each speaks
differently: which flag makes it emit structured output, where its final text
is, which events carry its token usage, and how full its context window is.
Scattered through role code those differences multiplied — the codex route
threw its usage away on every successful call, and the loop computed context
occupancy from cumulative counters. So each CLI gets ONE adapter here, and
every other module asks the adapter instead of knowing the CLI.

An adapter is chosen by the CLI actually launched (the argv's executable
name), not by the routed family: the flags and the output grammar belong to
the program, and a stand-in agent (a test double, an adopter's wrapper) that
is none of the three gets the plain adapter, which changes nothing.

Stdlib only, Python 3.11+, Windows/POSIX. A coordinator-layer module: the
session service (`session_service`) imports it, and it imports no kit sibling.

Contracts: IF-245 — the interface seam this module declares (process.md §8;
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
    emitted none (claude's usage rides its result event, so its raw usage is
    that event's `usage`, `modelUsage` and cost values, as emitted);
    `usage(stream)` returns the usage record, one dict with exactly the keys
    of `USAGE_KEYS` for every CLI: the OpenTelemetry GenAI usage names pinned
    by `OTEL_SEMCONV`, input counted inclusive of cached input, the derived
    `fresh-input-tokens`, `cost-usd`, `raw-usage`, `usage-scope`, and the
    `cli` and `semconv` columns, a count the CLI does not report being ""
    (never 0); `context(stream, env, session_id)` returns
    `(session_id, used, window, pct)`, the context occupancy of the session's
    LATEST model request, each field "" where the CLI does not report it.
"""

import json
import os
import tempfile
import uuid
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
    is there, so a stand-in agent is accounted exactly as before."""

    cli = ""

    def prepare(self, argv):
        return list(argv), None

    def final_text(self, stream, scratch, code):
        return stream

    provider = ""

    def raw_usage(self, stream):
        return ""

    def usage(self, stream):
        """A stand-in agent's result read the claude-shaped way, as the kit
        always read one; the provider stays unnamed."""
        return _claude_usage(self.cli, self.provider, stream)

    def context(self, stream, env=None, session_id=""):
        return "", "", "", ""

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
    `usage.output_tokens_details.thinking_tokens` (the old reader looked for a
    `reasoning_tokens` field no CLI emits). The response model is the model
    the session's last assistant event named, else the result's own `model`,
    else the one `modelUsage` entry whose counters match the result's usage —
    never blank merely because a background model's entry sits beside it.

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
        codex counts cached input INSIDE `input_tokens`, so its fresh part is
        `input_tokens - cached_input_tokens`; it reports no cache write and no
        response model, which stay blank. Its turn usage is cumulative over the
        thread, which is one call for a fresh session (scope `thread`).

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
        return usage_record(
            self.cli,
            self.provider,
            fresh=None if total is None else total - (cached or 0),
            cache_read=cached,
            cache_write=None,
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
        for this thread under the launch's `CODEX_HOME`, with
        `info.model_context_window` as the window. With no `CODEX_HOME` in the
        launch environment the rollout is not looked up in an ambient home,
        which could hold another route's thread: occupancy stays blank.

        Implements: SR-222, LLR-267
        """
        sid = session_id
        for event, _ in json_events(stream):
            if event.get("type") == "thread.started" and event.get("thread_id"):
                sid = event["thread_id"]
        home = (env or {}).get("CODEX_HOME")
        used, window = "", ""
        for event, _ in json_events(_codex_rollout(home, sid)):
            info = _dig(event, "payload", "info")
            if _dig(event, "payload", "type") != "token_count":
                continue
            value = _count(_dig(info, "last_token_usage", "input_tokens"))
            if value is not None:
                used = value
                window = _count(_dig(info, "model_context_window")) or window
        return sid, used, window, _pct(used, window)


def _codex_rollout(home, thread_id):
    """The newest rollout file's text for exactly `thread_id` under `home`,
    or "" — the id makes the lookup exact, so no other thread is read."""
    if not home or not thread_id:
        return ""
    try:
        pattern = "**/rollout-*-{}.jsonl".format(thread_id)
        found = list((Path(home) / "sessions").glob(pattern))
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
