"""The per-provider session adapters: capture and occupancy.

Each provider CLI has one adapter, and the adapter is the only place its
differences live: the flags that make it emit structured output, how the final
text is read back, which events carry its usage, and how full its context is.
These tests drive each adapter over a recorded fixture of that CLI's output in
`tests/golden/sessions/`, in memory (an injected runner, no subprocess).

Fixture provenance, stated because the two kinds differ:

- `claude-stream-json.jsonl` is LIVE: one `claude -p --output-format
  stream-json --verbose` run recorded 2026-09-28 on CLI 2.1.266, a two-call
  session (a Read tool call, then the answer). Trimmed only by dropping the
  rate-limit event, narrowing the init event to its identity fields and
  rewriting the working path.
- `codex-exec-json.jsonl`, `codex-rollout.jsonl` and `opencode-run-json.jsonl`
  are LIVE, recorded 2026-09-30 (WI-541) on codex-cli 0.157.1 and opencode
  1.18.29: one tool-using read of a one-line file, then the answer. The codex
  exec stream is the stdout verbatim (`codex exec --json --sandbox read-only`,
  no model pinned). The rollout is the same run's file under `~/.codex/
  sessions`, trimmed to the session_meta identity fields, the task events and
  the two token_count events (the account ids, injected instructions and rate
  limits are dropped). The opencode run is `opencode run --format json` on
  `opencode-go/kimi-k3`, working path rewritten to a neutral `work` directory.
"""

import json
from pathlib import Path

import pytest

from conftest import load_script

adapters = load_script("session_adapters")
service = load_script("session_service")
session = load_script("agent_session")

GOLDEN = Path(__file__).parent / "golden" / "sessions"


def _fixture(name):
    return (GOLDEN / name).read_text(encoding="utf-8")


def _invoke(argv, runner):
    """One call through the service's act step with `runner` as its launch:
    `(code, text, timed_out, metrics)`."""
    out = service.act(
        service.Call(root=".", role="BUILD", template=json.dumps(argv), runner=runner)
    )
    return out.code, out.text, out.timed_out, out.metrics


def _runner(stream, last_message=None):
    """A runner standing in for `run_session`: it writes the codex
    last-message file when the argv names one, and returns the fixture."""
    seen = {}

    def run(argv, root, timeout, **kwargs):
        seen["argv"] = list(argv)
        if last_message is not None and "--output-last-message" in argv:
            path = argv[argv.index("--output-last-message") + 1]
            Path(path).write_text(last_message, encoding="utf-8")
        return 0, stream, False

    return run, seen


# --- adapter selection --------------------------------------------------------


def test_the_adapter_is_chosen_by_the_cli_actually_launched():
    assert adapters.adapter_for(["claude", "-p"]).cli == "claude"
    assert adapters.adapter_for(["/opt/bin/CODEX.CMD", "exec"]).cli == "codex"
    assert adapters.adapter_for(["opencode", "run"]).cli == "opencode"
    assert adapters.adapter_for(["python", "fake_agent.py"]).cli == ""
    assert adapters.adapter_for([]).cli == ""


# --- codex: `exec --json` beside `-o` (WI-606) --------------------------------


def test_codex_route_runs_exec_json_beside_the_last_message_file():
    argv, scratch = adapters.adapter_for(["codex", "exec", "--model", "m"]).prepare(
        ["codex", "exec", "--model", "m"]
    )
    try:
        assert "--json" in argv
        assert argv[argv.index("--output-last-message") + 1] == scratch
    finally:
        Path(scratch).unlink()


def test_codex_json_flag_is_not_doubled_when_the_template_carries_it():
    argv, scratch = adapters.adapter_for(["codex"]).prepare(["codex", "exec", "--json"])
    Path(scratch).unlink()
    assert argv.count("--json") == 1


def test_a_successful_codex_call_keeps_its_usage_and_its_final_text():
    stream = _fixture("codex-exec-json.jsonl")
    runner, seen = _runner(stream, last_message="  PINEAPPLE  ")
    code, text, timed_out, metrics = _invoke(["codex", "exec"], runner)
    assert (code, timed_out) == (0, False)
    assert "--json" in seen["argv"]
    # The final text still comes from `-o`, never from the event stream.
    assert text == "PINEAPPLE"
    # The usage event survives, verbatim: the exact line the CLI wrote.
    usage_line = next(ln for ln in stream.splitlines() if '"turn.completed"' in ln)
    assert json.loads(metrics["raw-usage"]) == [json.loads(usage_line)]
    assert usage_line in metrics["raw-usage"]


# --- opencode: `run --format json` (WI-606) -----------------------------------


def test_opencode_route_runs_format_json():
    argv, scratch = adapters.adapter_for(["opencode"]).prepare(
        ["opencode", "run", "--dir", ".", "-m", "x", "--auto"]
    )
    assert scratch is None
    assert argv[argv.index("--format") + 1] == "json"


def test_a_successful_opencode_call_keeps_its_usage_and_its_final_text():
    stream = _fixture("opencode-run-json.jsonl")
    runner, seen = _runner(stream)
    code, text, _, metrics = _invoke(["opencode", "run"], runner)
    assert code == 0 and text == "PINEAPPLE"
    assert seen["argv"][-2:] == ["--format", "json"]
    finishes = [ln for ln in stream.splitlines() if '"step_finish"' in ln]
    assert len(finishes) == 2
    assert json.loads(metrics["raw-usage"]) == [json.loads(ln) for ln in finishes]


def test_opencode_output_with_no_json_event_passes_through_as_text():
    runner, _ = _runner("Error: no provider configured\n")
    _, text, _, metrics = _invoke(["opencode", "run"], runner)
    assert text == "Error: no provider configured\n"
    assert metrics.get("raw-usage", "") == ""


# --- occupancy: the latest request's prompt, never the cumulative (WI-605) ----


def test_claude_occupancy_is_the_final_calls_prompt_not_the_cumulative_usage():
    stream = _fixture("claude-stream-json.jsonl")
    result = session.parse_json_result(stream)
    usage = result["usage"]
    cumulative = sum(
        usage[k]
        for k in (
            "input_tokens",
            "cache_read_input_tokens",
            "cache_creation_input_tokens",
            "output_tokens",
        )
    )
    session_id, used, window, pct = adapters.adapter_for(["claude"]).context(stream)
    # The final model call: input 2 + cache read 48084 + cache write 181.
    assert used == 2 + 48084 + 181
    assert cumulative != used  # the recorded stream is one where they differ
    assert window == 1000000
    assert pct == round(used * 100 / window)
    assert session_id == "81ebe617-b1cd-43d9-8930-c7adbf23e955"


def test_claude_occupancy_docstring_names_its_source_field():
    doc = adapters.ClaudeAdapter.context.__doc__
    assert "message.usage" in doc and "assistant" in doc


def test_claude_occupancy_through_the_invocation_boundary_stays_under_the_window():
    runner, _ = _runner(_fixture("claude-stream-json.jsonl"))
    metrics = _invoke(["claude", "-p"], runner)[3]
    assert metrics["context-used"] == 48267
    assert metrics["context-window"] == 1000000
    assert 0 <= metrics["context-pct"] <= 100


def test_opencode_occupancy_is_the_last_steps_prompt_and_no_window_is_guessed():
    _, used, window, pct = adapters.adapter_for(["opencode"]).context(
        _fixture("opencode-run-json.jsonl")
    )
    assert used == 3107 + 7680
    assert window == "" and pct == ""


def test_codex_exec_usage_is_cumulative_so_no_occupancy_is_read_from_it(tmp_path):
    session_id, used, window, pct = adapters.adapter_for(["codex"]).context(
        _fixture("codex-exec-json.jsonl"), env={"CODEX_HOME": str(tmp_path)}
    )
    assert session_id == "01a0f5b5-ff52-73c1-b233-c11dd3defd4d"
    assert (used, window, pct) == ("", "", "")


def test_codex_occupancy_reads_the_last_request_from_its_rollout(tmp_path):
    thread = "01a0f5b5-ff52-73c1-b233-c11dd3defd4d"
    day = tmp_path / "sessions" / "2026" / "09" / "30"
    day.mkdir(parents=True)
    (day / "rollout-2026-09-30T23-25-40-{}.jsonl".format(thread)).write_text(
        _fixture("codex-rollout.jsonl"), encoding="utf-8"
    )
    _, used, window, pct = adapters.adapter_for(["codex"]).context(
        _fixture("codex-exec-json.jsonl"), env={"CODEX_HOME": str(tmp_path)}
    )
    assert used == 15224  # the last request's inclusive input, not 30378
    assert window == 258400
    assert pct == round(15224 * 100 / 258400)


THREAD = "01a0f5b5-ff52-73c1-b233-c11dd3defd4d"


def _put_rollout(home, text):
    """Write `text` as THREAD's rollout under the codex home `home`."""
    day = Path(home) / "sessions" / "2026" / "09" / "30"
    day.mkdir(parents=True, exist_ok=True)
    name = "rollout-2026-09-30T23-25-40-{}.jsonl".format(THREAD)
    (day / name).write_text(text, encoding="utf-8")


@pytest.fixture
def default_home(tmp_path, monkeypatch):
    """codex's default home, `<user home>/.codex`, with the user home
    redirected into the test's own directory and no CODEX_HOME set: the
    owner's real home is never read."""
    user = tmp_path / "user"
    user.mkdir()
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setenv("HOME", str(user))
    monkeypatch.setenv("USERPROFILE", str(user))
    return user / ".codex"


def test_codex_occupancy_falls_back_to_codexs_default_home(default_home):
    _put_rollout(default_home, _fixture("codex-rollout.jsonl"))
    adapter = adapters.adapter_for(["codex"])
    stream = _fixture("codex-exec-json.jsonl")
    _, used, window, pct = adapter.context(stream, env={})
    assert (used, window) == (15224, 258400)
    assert pct == round(15224 * 100 / 258400)
    # The compaction observations read the same rollout through the same home.
    assert adapter.compaction(stream, {}, THREAD)["prompts"][-1] == 15224


def test_codex_default_home_follows_the_launch_home_on_posix(
    default_home, tmp_path, monkeypatch
):
    # codex's POSIX default is "${CODEX_HOME:-$HOME/.codex}" in the launch
    # environment, so a route overriding HOME has codex write there, not under
    # the service process's home (which here holds nothing).
    monkeypatch.setattr(adapters, "LAUNCH_HOME_VARIABLE", "HOME", raising=False)
    launch = tmp_path / "launch-user"
    _put_rollout(launch / ".codex", _fixture("codex-rollout.jsonl"))
    adapter = adapters.adapter_for(["codex"])
    stream = _fixture("codex-exec-json.jsonl")
    _, used, window, _ = adapter.context(stream, env={"HOME": str(launch)})
    assert (used, window) == (15224, 258400)
    prompts = adapter.compaction(stream, {"HOME": str(launch)}, THREAD)["prompts"]
    assert prompts[-1] == 15224


def test_codex_default_home_ignores_a_launch_home_override_on_windows(
    default_home, tmp_path, monkeypatch
):
    # On Windows codex takes its default from the OS profile and ignores a
    # launch's HOME and USERPROFILE, so the adapter does too.
    monkeypatch.setattr(adapters, "LAUNCH_HOME_VARIABLE", None, raising=False)
    _put_rollout(default_home, _fixture("codex-rollout.jsonl"))
    launch = {"HOME": str(tmp_path / "x"), "USERPROFILE": str(tmp_path / "x")}
    _, used, _, _ = adapters.adapter_for(["codex"]).context(
        _fixture("codex-exec-json.jsonl"), env=launch
    )
    assert used == 15224


def test_an_explicit_codex_home_wins_over_the_default(default_home, tmp_path):
    _put_rollout(default_home, _fixture("codex-rollout.jsonl"))
    explicit = tmp_path / "explicit"
    _put_rollout(explicit, _fixture("codex-rollout.jsonl").replace("15224", "20000"))
    _, used, _, _ = adapters.adapter_for(["codex"]).context(
        _fixture("codex-exec-json.jsonl"), env={"CODEX_HOME": str(explicit)}
    )
    assert used == 20000


def test_codex_occupancy_stays_blank_without_this_threads_rollout(default_home):
    # Another thread's rollout sits in the home; this thread has none.
    day = default_home / "sessions" / "2026" / "09" / "30"
    day.mkdir(parents=True)
    (day / "rollout-2026-09-30T23-25-40-another-thread.jsonl").write_text(
        _fixture("codex-rollout.jsonl"), encoding="utf-8"
    )
    _, used, window, pct = adapters.adapter_for(["codex"]).context(
        _fixture("codex-exec-json.jsonl"), env={}
    )
    assert (used, window, pct) == ("", "", "")


def test_an_unknown_cli_reports_no_occupancy():
    assert adapters.adapter_for(["python"]).context('{"type":"result"}') == (
        "",
        "",
        "",
        "",
    )


# --- raw usage is the runner's own line, byte for byte (TC-262) ---------------
#
# Each case writes the usage-bearing line in a shape a re-serialisation would
# change: odd whitespace, keys out of order, a field the adapter never reads.
# The raw-usage column must hold that line exactly, beside (not rebuilt from)
# the parsed values.

MUTATED = {
    "claude": (
        '{ "session_id" : "s1",  "usage": {"output_tokens": 2, "input_tokens": 3,'
        ' "future_field": {"x": 1}}, "type":"result", "total_cost_usd": 0.5 }'
    ),
    "codex": (
        '{"usage": {"output_tokens": 2,   "input_tokens": 3, "cached_input_tokens": 1,'
        ' "new_counter": 9}, "type" : "turn.completed"}'
    ),
    "opencode": (
        '{"part":{"tokens":{"output":2,"input":3,"cache":{"write":0,"read":1}},'
        '"extra":true,"type":"step-finish"},  "type":"step_finish","sessionID":"x"}'
    ),
}


@pytest.mark.parametrize("cli", sorted(MUTATED))
def test_raw_usage_keeps_the_usage_line_byte_for_byte(cli):
    line = MUTATED[cli]
    stream = "banner line\n" + line + "\n"
    raw = adapters.adapter_for([cli]).raw_usage(stream)
    assert raw == "[" + line + "]"


@pytest.mark.parametrize("cli", sorted(MUTATED))
def test_the_usage_record_carries_the_verbatim_line_beside_the_parsed_counts(cli):
    line = MUTATED[cli]
    usage = adapters.adapter_for([cli]).usage(line + "\n")
    assert usage["raw-usage"] == "[" + line + "]"
    assert usage["gen_ai.usage.output_tokens"] == 2


def test_a_usage_line_with_surrounding_whitespace_is_kept_as_written():
    line = "   " + MUTATED["codex"] + "\t"
    raw = adapters.adapter_for(["codex"]).raw_usage(line + "\n")
    assert raw == "[" + line + "]"
    assert json.loads(raw)[0]["usage"]["new_counter"] == 9
