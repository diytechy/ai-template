"""The session service: act and record, and the usage record it writes.

Every model call the kit makes goes through `session_service`: `act` launches
it (through the launched CLI's adapter) and accounts it, `record` writes its
one session log and commits it. These tests drive both in memory with an
injected runner, over the recorded fixtures `tests/test_session_adapters.py`
describes (`tests/golden/sessions/`; all three are LIVE: the claude one
recorded 2026-09-28, the codex and opencode ones 2026-09-30, WI-541).
"""

import ast
import json
import re
from pathlib import Path

import pytest

from conftest import SCRIPTS, load_script

svc = load_script("session_service")
adapters = load_script("session_adapters")
common = load_script("agent_common")

GOLDEN = Path(__file__).parent / "golden" / "sessions"
PINNED = "e57c543b4889619eb2a05702471937db5119165d"


def _fixture(name):
    return (GOLDEN / name).read_text(encoding="utf-8")


def _runner(stream, code=0, timed_out=False, last_message=None):
    def run(argv, root, timeout, **kwargs):
        if last_message is not None and "--output-last-message" in argv:
            path = argv[argv.index("--output-last-message") + 1]
            Path(path).write_text(last_message, encoding="utf-8")
        return code, stream, timed_out

    return run


def _act(tmp_path, template, stream, **kw):
    runner = _runner(stream, last_message=kw.pop("last_message", None))
    call = svc.Call(
        root=tmp_path,
        role=kw.pop("role", "BUILD"),
        template=template,
        model="m",
        prompt="p",
        runner=runner,
        **kw,
    )
    return svc.act(call)


# --- the S8 usage record, one adapter per provider (TC-264) -------------------


def test_claude_usage_is_mapped_to_the_pinned_otel_names():
    usage = adapters.adapter_for(["claude"]).usage(_fixture("claude-stream-json.jsonl"))
    assert usage["semconv"].endswith("@" + PINNED)
    assert usage["cli"] == "claude"
    assert usage["gen_ai.provider.name"] == "anthropic"
    # Inclusive input: fresh 4 + cache read 48084 + cache write 48265.
    assert usage["gen_ai.usage.input_tokens"] == 4 + 48084 + 48265
    assert usage["gen_ai.usage.cache_read.input_tokens"] == 48084
    assert usage["gen_ai.usage.cache_write.input_tokens"] == 48265
    assert usage["gen_ai.usage.output_tokens"] == 129
    assert usage["fresh-input-tokens"] == 4
    assert usage["gen_ai.conversation.id"] == "81ebe617-b1cd-43d9-8930-c7adbf23e955"
    assert usage["cost-usd"] == pytest.approx(0.2049518)
    result_line = _fixture("claude-stream-json.jsonl").splitlines()[-1]
    assert usage["raw-usage"] == "[" + result_line + "]"  # the line as written
    (raw,) = json.loads(usage["raw-usage"])
    assert raw["usage"]["cache_read_input_tokens"] == 48084
    assert set(raw["modelUsage"]) == {"claude-haiku-4-5-20251001", "claude-sonnet-5"}


def test_claude_reported_model_survives_a_background_model_beside_it():
    # Defect C2: with two modelUsage entries the reported model went blank.
    usage = adapters.adapter_for(["claude"]).usage(_fixture("claude-stream-json.jsonl"))
    assert usage["gen_ai.response.model"] == "claude-sonnet-5"


def test_claude_reported_model_without_assistant_events_is_the_matching_entry():
    result = {
        "type": "result",
        "usage": {"input_tokens": 3, "output_tokens": 2},
        "modelUsage": {
            "claude-haiku-4-5": {"inputTokens": 900, "outputTokens": 9},
            "claude-opus-5": {"inputTokens": 3, "outputTokens": 2},
        },
    }
    usage = adapters.adapter_for(["claude"]).usage(json.dumps(result))
    assert usage["gen_ai.response.model"] == "claude-opus-5"


def test_claude_reasoning_tokens_are_read_from_the_field_the_cli_emits():
    # Defect C2: the old reader looked for `usage.reasoning_tokens`, which no
    # CLI emits; claude reports thinking under `output_tokens_details`.
    result = {
        "type": "result",
        "usage": {
            "input_tokens": 1,
            "output_tokens": 40,
            "output_tokens_details": {"thinking_tokens": 17},
        },
    }
    usage = adapters.adapter_for(["claude"]).usage(json.dumps(result))
    assert usage["gen_ai.usage.reasoning.output_tokens"] == 17


def test_codex_usage_is_mapped_inclusive_with_fresh_input_derived():
    usage = adapters.adapter_for(["codex"]).usage(_fixture("codex-exec-json.jsonl"))
    assert usage["semconv"].endswith("@" + PINNED)
    assert usage["cli"] == "codex"
    assert usage["gen_ai.provider.name"] == "openai"
    assert usage["gen_ai.usage.input_tokens"] == 30378  # codex counts cache inside
    assert usage["gen_ai.usage.cache_read.input_tokens"] == 27392
    assert usage["gen_ai.usage.cache_write.input_tokens"] == 0
    assert usage["gen_ai.usage.output_tokens"] == 47
    assert usage["gen_ai.usage.reasoning.output_tokens"] == 0
    assert usage["fresh-input-tokens"] == 30378 - 27392
    assert usage["gen_ai.conversation.id"] == "01a0f5b5-ff52-73c1-b233-c11dd3defd4d"


def test_codex_provider_name_stays_at_its_default_when_reconfigured():
    adapter = adapters.adapter_for(
        ["codex", "exec", "-c", 'model_provider="third-party"']
    )
    usage = adapter.usage(_fixture("codex-exec-json.jsonl"))
    assert usage["gen_ai.provider.name"] == "openai"


def test_opencode_usage_is_summed_over_its_steps_and_made_inclusive():
    usage = adapters.adapter_for(["opencode"]).usage(
        _fixture("opencode-run-json.jsonl")
    )
    assert usage["semconv"].endswith("@" + PINNED)
    assert usage["cli"] == "opencode"
    assert usage["gen_ai.provider.name"] == ""
    assert usage["gen_ai.usage.input_tokens"] == (10483 + 0 + 0) + (3107 + 7680 + 0)
    assert usage["gen_ai.usage.cache_read.input_tokens"] == 7680
    assert usage["gen_ai.usage.cache_write.input_tokens"] == 0
    # Reasoning is included in output, as the convention asks.
    assert usage["gen_ai.usage.output_tokens"] == (99 + 86) + (14 + 39)
    assert usage["gen_ai.usage.reasoning.output_tokens"] == 86 + 39
    assert usage["fresh-input-tokens"] == 10483 + 3107
    assert usage["gen_ai.conversation.id"] == "ses_f0a498817ffe2U5tfcBE7s7Q2I"


def test_every_provider_row_carries_the_same_columns():
    rows = [
        adapters.adapter_for([cli]).usage(_fixture(name))
        for cli, name in (
            ("claude", "claude-stream-json.jsonl"),
            ("codex", "codex-exec-json.jsonl"),
            ("opencode", "opencode-run-json.jsonl"),
            ("python", "claude-stream-json.jsonl"),
        )
    ]
    assert rows[-1]["gen_ai.provider.name"] == ""
    assert all(set(row) == set(adapters.USAGE_KEYS) for row in rows)


def test_gemini_usage_is_recorded_with_unread_values_empty():
    result = json.dumps(
        {
            "session_id": "example-session",
            "response": "done",
            "stats": {"models": {}, "tools": {}, "files": {}},
        }
    )
    usage = adapters.adapter_for(["gemini", "--output-format", "json"]).usage(result)
    empty_keys = (
        "cli",
        "gen_ai.provider.name",
        "raw-usage",
        *adapters.USAGE_COUNT_KEYS,
        "fresh-input-tokens",
    )
    assert all(usage[key] == "" for key in empty_keys)
    assert set(usage) == set(adapters.USAGE_KEYS)


# --- act: one path launches every call (TC-265) --------------------------------


def test_act_launches_through_the_adapter_and_accounts_the_call(tmp_path):
    out = _act(
        tmp_path,
        "codex exec --model {model}",
        _fixture("codex-exec-json.jsonl"),
        provider="OPENAI",
        tier="strong",
        route_id="OPENAI-SOL",
        source_event="managed",
        last_message="PINEAPPLE",
    )
    assert (out.code, out.text, out.timed_out) == (0, "PINEAPPLE", False)
    assert '"turn.completed"' in out.stream  # the raw stream is kept whole
    m = out.metrics
    assert m["invocation-id"] and m["started-at"] and m["ended-at"]
    assert m["role"] == "BUILD" and m["provider"] == "OPENAI"
    assert m["roster-row"] == "OPENAI-SOL" and m["tier"] == "strong"
    assert m["gen_ai.request.model"] == "m"
    assert m["gen_ai.usage.input_tokens"] == 30378
    assert m["usage-status"] == "known"


def test_a_failed_spawn_is_accounted_with_unavailable_usage(tmp_path):
    call = svc.Call(
        root=tmp_path,
        role="PROBE",
        template="agent",
        runner=lambda *a, **k: (-1, "coordinator: session error: missing", False),
    )
    out = svc.act(call)
    assert out.code == -1
    assert out.metrics["usage-status"] == "unavailable"
    assert out.metrics["gen_ai.usage.input_tokens"] == ""
    assert out.metrics["wall-secs"] >= 0


def test_a_timeout_keeps_partial_usage_and_its_kind(tmp_path):
    stream = json.dumps({"type": "result", "usage": {"input_tokens": 7}})
    call = svc.Call(
        root=tmp_path,
        role="BUILD",
        template="agent",
        runner=lambda *a, **k: (-1, stream, "idle"),
    )
    out = svc.act(call)
    assert out.metrics["timeout"] == "idle"
    assert out.metrics["usage-status"] == "partial"
    assert out.metrics["gen_ai.usage.input_tokens"] == 7


def test_each_call_gets_a_new_invocation_id(tmp_path):
    stream = json.dumps({"type": "result", "session_id": "same"})
    first = _act(tmp_path, "agent", stream).metrics
    second = _act(tmp_path, "agent", stream).metrics
    assert first["invocation-id"] != second["invocation-id"]
    assert first["session-id"] == second["session-id"] == "same"


def test_a_runner_exception_is_accounted_then_reraised(tmp_path):
    metrics = {}

    def broken(*a, **k):
        raise RuntimeError("runner broke")

    call = svc.Call(root=tmp_path, role="BUILD", template="agent", runner=broken)
    with pytest.raises(RuntimeError, match="runner broke"):
        svc.act(call, metrics)
    assert metrics["error"] == "RuntimeError"
    assert metrics["usage-status"] == "unavailable"


# --- record: one writer (TC-265) ------------------------------------------------


def test_call_records_one_log_with_the_usage_record_and_the_raw_stream(
    tmp_path, monkeypatch
):
    committed = []
    monkeypatch.setattr(svc.agent_common, "commit_telemetry", _capture(committed))
    stream = _fixture("claude-stream-json.jsonl")
    call = svc.Call(
        root=tmp_path,
        role="PROBE",
        template="claude -p --model {model}",
        model="sonnet",
        prompt="Reply OK",
        source_event="recovery-probe",
        runner=_runner(stream),
    )
    out = svc.call(call)
    logs = list((tmp_path / "docs" / "iteration").glob("call_*.log"))
    assert len(logs) == 1 and len(committed) == 1
    row = common.read_log_meta(logs[0])
    assert row["outcome"] == "COMPLETED" and row["phase"] == "PROBE"
    assert row["cli"] == "claude"
    assert row["semconv"].endswith(PINNED)
    assert row["gen_ai.usage.input_tokens"] == str(4 + 48084 + 48265)
    assert row["gen_ai.response.model"] == "claude-sonnet-5"
    assert row["context-used"] == "48267" and int(row["context-pct"]) <= 100
    assert row["invocation-id"] == out.metrics["invocation-id"]
    # The transcript is the raw stream, not a reduced result.
    assert '"type":"assistant"' in logs[0].read_text(encoding="utf-8")


def test_a_ctrl_c_in_an_attached_sitting_persists_a_complete_record(
    tmp_path, monkeypatch
):
    committed = []
    monkeypatch.setattr(svc.agent_common, "commit_telemetry", _capture(committed))

    def interrupted(*a, **k):
        raise KeyboardInterrupt

    call = svc.Call(
        root=tmp_path,
        role="INTERACTIVE",
        template="agent",
        model="m",
        attached=True,
        runner=interrupted,
    )
    with pytest.raises(KeyboardInterrupt):
        svc.call(call)
    logs = list((tmp_path / "docs" / "iteration").glob("call_*.log"))
    assert len(logs) == 1 and committed
    header = logs[0].read_text(encoding="utf-8")
    assert "# outcome: INTERRUPTED" in header
    assert "# usage-status: unavailable" in header
    assert "# wall-secs: \n" not in header and "# ended-at: \n" not in header


def test_provider_metadata_cannot_inject_log_headers(tmp_path, monkeypatch):
    monkeypatch.setattr(svc.agent_common, "commit_telemetry", _capture([]))
    payload = "provider\n# outcome: COMPLETED"
    stream = json.dumps({"type": "result", "session_id": payload, "model": payload})
    call = svc.Call(
        root=tmp_path, role="BUILD", template="agent", runner=_runner(stream, code=1)
    )
    svc.call(call)
    (log,) = (tmp_path / "docs" / "iteration").glob("call_*.log")
    row = common.read_log_meta(log)
    assert row["outcome"] == "ERROR"
    assert row["session-id"] == payload.replace("\n", "\\n")


def test_the_worker_record_takes_the_callers_row_and_the_raw_stream_file(
    tmp_path, monkeypatch
):
    committed = []
    monkeypatch.setattr(svc.agent_common, "commit_telemetry", _capture(committed))
    out = _act(tmp_path, "agent", json.dumps({"type": "result", "result": "ok"}))
    meta = {"session": "007", "stamp": "s", "outcome": "COMPLETED", "phase": "BUILD"}
    path = svc.record(
        out,
        meta,
        iter_dir=tmp_path / "logs",
        raw_dir=tmp_path / "raw",
        raw_name="007-s.log",
        label="BUILD COMPLETED",
        session="t007",
    )
    assert path.parent == tmp_path / "logs"
    assert (tmp_path / "raw" / "007-s.log").read_text(encoding="utf-8") == out.stream
    row = common.read_log_meta(path)
    assert row["session"] == "007" and row["invocation-id"]
    assert committed[0][1:3] == ("t007", "BUILD COMPLETED")


def _capture(sink):
    def commit(root, session, label, paths, trailer=None):
        sink.append((root, session, label, paths))

    return commit


# --- the one path, pinned structurally (Done-when: no role or provider keeps
# its own launch or logging path) ----------------------------------------------
#
# Two guards over every kit script's syntax tree. A DIRECT PROVIDER LAUNCH is
# a process launch (subprocess or os) whose argv names a provider runner, or
# one made in a function that builds an argv from a command template; only the
# service and its launch layer may make one. A SESSION-LOG WRITER is a call to
# the log writer, the log's header literal, or a write in a function that
# names the iteration directory; only the service calls the writer and only
# the shared primitives define it. Each guard is shown to bite on a planted
# mutation.

PROVIDERS = ("claude", "codex", "opencode")
LAUNCHERS = {
    "run",
    "Popen",
    "call",
    "check_call",
    "check_output",
    "system",
    "popen",
    "execvp",
    "spawnv",
}
LAUNCH_HOMES = {"session_service.py", "agent_session.py"}
WRITER_CALLERS = {"session_service.py"}
WRITER_HOMES = {"agent_common.py"}


def _callee(node):
    func = node.func
    return func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")


def _is_launch(node):
    """A process launch: `subprocess.X(...)` or `os.X(...)` for a launching
    X, or a bare `Popen`/`check_output`/`check_call` imported by name."""
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id in ("subprocess", "os") and func.attr in LAUNCHERS
    return getattr(func, "id", "") in ("Popen", "check_output", "check_call")


def _names_provider(node):
    """Whether an argv expression names a provider runner as its program."""
    if isinstance(node, ast.BinOp):
        return _names_provider(node.left)
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts:
        return _names_provider(node.elts[0])
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        words = node.value.strip().split()
        program = Path(words[0]).name.lower() if words else ""
        return program.startswith(PROVIDERS)
    if isinstance(node, ast.JoinedStr):
        return any(_names_provider(part) for part in node.values)
    return False


def _owned(scope):
    """The nodes `scope` owns: its subtree without nested function bodies."""
    stack = list(ast.iter_child_nodes(scope))
    while stack:
        node = stack.pop()
        yield node
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stack.extend(ast.iter_child_nodes(node))


def _scopes(tree):
    """The module and each function, each yielding the nodes it owns."""
    yield tree
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def _argv_source(value):
    """Whether an assigned value is a provider argv: a literal naming a
    provider runner, or a command template's argv (`build_argv`/`split_cmd`)."""
    if isinstance(value, ast.Call):
        return _callee(value) in ("build_argv", "split_cmd")
    return _names_provider(value)


def _built_names(nodes):
    """Names bound to a provider argv in one scope: the target (or a tuple
    target's first name) of an assignment `_argv_source` recognises, so an
    argv held in a variable before its launch is still seen."""
    names = set()
    for node in nodes:
        if not (isinstance(node, ast.Assign) and _argv_source(node.value)):
            continue
        for target in node.targets:
            first = target.elts[0] if isinstance(target, ast.Tuple) else target
            if isinstance(first, ast.Name):
                names.add(first.id)
    return names


def _names_built(node, built):
    """Whether an argv expression is (or starts with) a template-built argv."""
    if isinstance(node, ast.BinOp):
        return _names_built(node.left, built)
    return isinstance(node, ast.Name) and node.id in built


def _launch_argv(call):
    """The argv expression a launch call runs, or None."""
    if call.args:
        return call.args[0]
    return next((k.value for k in call.keywords if k.arg == "args"), None)


def direct_provider_launches(source):
    """Line numbers of the direct provider launches in `source`."""
    hits = set()
    for scope in _scopes(ast.parse(source)):
        nodes = list(_owned(scope))
        built = _built_names(nodes)
        for c in (n for n in nodes if isinstance(n, ast.Call) and _is_launch(n)):
            argv = _launch_argv(c)
            if argv is None:
                continue
            if _names_provider(argv) or _names_built(argv, built):
                hits.add(c.lineno)
    return sorted(hits)


def _writes(scope):
    for c in (n for n in _owned(scope) if isinstance(n, ast.Call)):
        if _callee(c) in ("write_text", "write_bytes", "write"):
            yield c
        elif _callee(c) == "open" and any(
            isinstance(a, ast.Constant) and str(a.value)[:1] in ("w", "a")
            for a in c.args[1:2]
        ):
            yield c


def _code_constants(scope):
    """The string constants a scope's code holds, its docstrings excluded."""
    nodes = list(_owned(scope))
    docs = {
        id(n.value)
        for n in nodes
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
    }
    return [
        n
        for n in nodes
        if isinstance(n, ast.Constant)
        and isinstance(n.value, str)
        and id(n) not in docs
    ]


def _names_iteration(node):
    """Whether a string constant names the iteration directory, alone or as
    one part of a path written in either separator."""
    return "iteration" in re.split(r"[\\/]", node.value)


def session_log_writers(source):
    """`(writer_calls, header_literals, iteration_writes)` line numbers."""
    tree = ast.parse(source)
    calls = [
        n.lineno
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and _callee(n) == "write_session_log"
    ]
    headers = [
        n.lineno
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant)
        and isinstance(n.value, str)
        and "agent session log" in n.value
    ]
    writes = set()
    for scope in _scopes(tree):
        if scope is tree:
            continue
        names_dir = any(_names_iteration(n) for n in _code_constants(scope))
        if names_dir:
            writes.update(c.lineno for c in _writes(scope))
    return calls, headers, sorted(writes)


def _kit_sources():
    for path in sorted(SCRIPTS.rglob("*.py")):
        yield path.name, path.read_text(encoding="utf-8")


def test_only_the_service_launches_a_provider_runner():
    offenders = {
        name: lines
        for name, text in _kit_sources()
        if name not in LAUNCH_HOMES and (lines := direct_provider_launches(text))
    }
    assert offenders == {}


def test_only_the_service_writes_a_session_log():
    offenders = {}
    for name, text in _kit_sources():
        calls, headers, writes = session_log_writers(text)
        if calls and name not in WRITER_CALLERS:
            offenders[name] = ("writer call", calls)
        if (headers or writes) and name not in WRITER_HOMES:
            offenders[name] = ("second writer", headers + writes)
    assert offenders == {}


@pytest.mark.parametrize(
    "planted",
    [
        'import subprocess\nsubprocess.run(["claude", "-p", "hi"])\n',
        'import subprocess\np = subprocess.Popen(["codex", "exec"] + extra)\n',
        "import os\nos.system('opencode run --auto')\n",
        "from subprocess import Popen\ndef go(t):\n"
        "    argv, _ = build_argv(t, 'm', 'p')\n    return Popen(argv)\n",
        'import subprocess\nsubprocess.check_output(args=[f"{home}/bin/claude"])\n',
        # A literal provider argv held in a variable first.
        'import subprocess\nargv = ["claude", "-p"]\nsubprocess.run(argv)\n',
        "import subprocess\ndef go():\n"
        "    cmd = ('codex', 'exec')\n    return subprocess.Popen(cmd + ('x',))\n",
    ],
)
def test_the_launch_guard_bites_on_a_direct_provider_launch(planted):
    assert direct_provider_launches(planted)


def test_the_launch_guard_passes_a_non_provider_launch():
    assert not direct_provider_launches(
        'import subprocess\nsubprocess.run(["git", "status"])\n'
    )


@pytest.mark.parametrize(
    "planted,which",
    [
        (
            "from agent_common import write_session_log\n"
            "write_session_log(d, meta, text)\n",
            0,
        ),
        ('HEADER = "# agent session log - my own writer"\n', 1),
        (
            "def keep_log(root, text):\n"
            "    (root / 'docs' / 'iteration' / 'x.log').write_text(text)\n",
            2,
        ),
        (
            "def keep_log(root, text):\n"
            "    with open(root / 'iteration' / 'x.log', 'a') as f:\n"
            "        f.write(text)\n",
            2,
        ),
        # An iteration-directory path built from parts in one literal.
        (
            "from pathlib import Path\ndef keep_log(text):\n"
            "    Path('docs/iteration/x.log').write_text(text)\n",
            2,
        ),
        (
            "def keep_log(root, text):\n"
            "    (root / 'docs\\\\iteration\\\\x.log').write_bytes(text)\n",
            2,
        ),
    ],
)
def test_the_writer_guard_bites_on_a_second_session_log_writer(planted, which):
    assert session_log_writers(planted)[which]


def test_the_retired_launch_and_logging_paths_are_gone():
    for name in (
        "invoke_and_persist",
        "invoke_session",
        "_run_attached_session",
        "family_context_telemetry",
        "_result_accounting",
        "write_raw_stream",
    ):
        users = {
            path
            for path, text in _kit_sources()
            if any(
                getattr(n, "id", getattr(n, "attr", None)) == name
                for n in ast.walk(ast.parse(text))
            )
        }
        assert users == set(), name


def test_a_credential_in_a_raw_usage_line_is_redacted_in_the_log_header(
    tmp_path, monkeypatch
):
    # The claude usage line is its result event, which carries the result
    # text; the header is committed history, so it passes the same redaction
    # seam the transcript does.
    monkeypatch.setattr(svc.agent_common, "commit_telemetry", _capture([]))
    key = "sk-ant-api03-" + "A" * 30
    stream = json.dumps(
        {"type": "result", "result": "leaked " + key, "usage": {"input_tokens": 1}}
    )
    call = svc.Call(
        root=tmp_path,
        role="BUILD",
        template="claude -p",
        runner=_runner(stream),
    )
    svc.call(call)
    (log,) = (tmp_path / "docs" / "iteration").glob("call_*.log")
    text = log.read_text(encoding="utf-8")
    assert key not in text
    header = text.split("# ---")[0]
    assert "[REDACTED]" in header and "# raw-usage: [" in header


@pytest.mark.parametrize("write", [None, 117, 4000])
def test_codex_cache_write_present_or_absent_inline_recording_variant(write):
    # Inline variants of the live line; the recording has only a reported zero.
    event = json.loads(_fixture("codex-exec-json.jsonl").splitlines()[-1])
    event["usage"].pop("cache_write_input_tokens")
    if write is not None:
        event["usage"]["cache_write_input_tokens"] = write
    usage = adapters.CodexAdapter().usage(json.dumps(event))
    assert usage["gen_ai.usage.cache_write.input_tokens"] == (
        "" if write is None else write
    )
    assert usage["gen_ai.usage.input_tokens"] == max(30378, 27392 + (write or 0))
    assert usage["fresh-input-tokens"] == max(0, 30378 - 27392 - (write or 0))
