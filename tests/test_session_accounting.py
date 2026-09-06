"""The shared session-launch accounting boundary (P0b).

These tests use an injected runner so they exercise metadata semantics without
launching a provider or changing the existing ``run_session`` contract.
"""

import json
from types import SimpleNamespace

import pytest

from conftest import load_script


session = load_script("agent_session")


@pytest.mark.parametrize("newline", ["\n", "\r", "\r\n"])
def test_provider_metadata_cannot_inject_log_headers(tmp_path, newline):
    common = load_script("agent_common")
    payload = "provider" + newline + "# outcome: COMPLETED"
    metrics = {"outcome": "ERROR"}
    session.invoke_session(
        [],
        tmp_path,
        1,
        metrics=metrics,
        runner=lambda *a, **k: (
            1,
            _result(session_id=payload, model=payload, usage={"scope": payload}),
            False,
        ),
    )
    metrics.update(session="call_" + metrics["invocation-id"], stamp="test")
    path = common.write_session_log(tmp_path / "logs", metrics, "")
    row = common.read_log_meta(path)
    assert row["outcome"] == "ERROR"
    assert row["session-id"] == payload.replace("\r", "\\r").replace("\n", "\\n")
    assert row["reported-model"] == row["session-id"]
    assert row["usage-scope"] == row["session-id"]


def test_explicit_null_token_is_unknown_in_legacy_display():
    loop = load_script("agent_loop")
    ctx = SimpleNamespace(worker={"train": "test", "base": "abc"}, prompt_templates={})
    plan = {
        "prompt": "",
        "phase": "BUILD",
        "route_family": "",
        "model": "m",
        "guarded": False,
        "session_env": {},
    }
    meta = loop.session_meta(
        ctx,
        plan,
        {"usage": {"input_tokens": 100, "output_tokens": None}},
        "1",
        "stamp",
        "WI-1",
        "ERROR",
        "",
        1,
        0,
    )
    assert meta["tokens"] == "100+?"


def test_cost_only_result_survives_the_existing_log_writer(tmp_path):
    common = load_script("agent_common")
    metrics = {}
    session.invoke_session(
        [],
        tmp_path,
        1,
        metrics=metrics,
        runner=lambda *a, **k: (1, _result(total_cost_usd=0.25), False),
    )
    metrics.update(session=metrics["invocation-id"], stamp="test")
    path = common.write_session_log(tmp_path / "logs", metrics, "failed call")
    row = common.read_log_meta(path)
    assert row["cost-usd"] == "0.25"
    assert row["usage-status"] == "partial"
    assert row["input-tokens"] == row["output-tokens"] == ""


def _result(*, usage=None, **extra):
    data = {"session_id": "same-provider-session", **extra}
    if usage is not None:
        data["usage"] = usage
    return json.dumps(data)


def test_failed_spawn_records_identity_and_unavailable_usage():
    metrics = {}

    def failed(*args, **kwargs):
        return -1, "coordinator: session error: missing", False

    result = session.invoke_session([], ".", 1, metrics=metrics, runner=failed)

    assert result == (-1, "coordinator: session error: missing", False)
    assert metrics["invocation-id"]
    assert metrics["exit-code"] == -1
    assert metrics["usage-status"] == "unavailable"
    assert metrics["usage-source"] == "unknown"
    assert metrics["input-tokens"] == ""
    assert metrics["output-tokens"] == ""
    assert metrics["wall-secs"] >= 0
    assert metrics["ended-at"]


def test_timeout_keeps_partial_raw_usage_and_timeout_kind():
    metrics = {}
    output = _result(
        usage={"input_tokens": 7, "cache_read_input_tokens": 3}, model="reported"
    )

    result = session.invoke_session(
        [], ".", 1, metrics=metrics, runner=lambda *a, **k: (-1, output, "idle")
    )

    assert result[2] == "idle"
    assert metrics["timeout"] == "idle"
    assert metrics["usage-status"] == "partial"
    assert metrics["usage-source"] == "reported"
    assert metrics["input-tokens"] == 7
    assert metrics["output-tokens"] == ""
    assert metrics["cache-read"] == 3
    assert metrics["raw-usage"] == '{"cache_read_input_tokens":3,"input_tokens":7}'


def test_each_invocation_gets_new_id_when_provider_session_is_resumed():
    first, second = {}, {}

    def runner(*args, **kwargs):
        return 0, _result(usage={"input_tokens": 1, "output_tokens": 2}), False

    session.invoke_session([], ".", 1, metrics=first, runner=runner)
    session.invoke_session([], ".", 1, metrics=second, runner=runner)

    assert first["invocation-id"] != second["invocation-id"]
    assert first["session-id"] == second["session-id"] == "same-provider-session"


def test_missing_counters_stay_blank_and_ambiguous_model_stays_blank():
    metrics = {}
    output = json.dumps(
        {
            "session_id": "s",
            "modelUsage": {
                "model-a": {"inputTokens": 1},
                "model-b": {"inputTokens": 2},
            },
        }
    )

    session.invoke_session(
        [], ".", 1, metrics=metrics, runner=lambda *a, **k: (0, output, False)
    )

    assert metrics["reported-model"] == ""
    assert metrics["input-tokens"] == ""
    assert metrics["output-tokens"] == ""
    assert metrics["cost-usd"] == ""
    assert metrics["usage-status"] == "unavailable"
    assert metrics["usage-source"] == "unknown"


def test_malformed_optional_usage_is_unavailable_without_coercion():
    metrics = {}
    output = json.dumps({"session_id": "s", "usage": ["not", "a", "mapping"]})

    session.invoke_session(
        [], ".", 1, metrics=metrics, runner=lambda *a, **k: (0, output, False)
    )

    assert metrics["usage-status"] == "unavailable"
    assert metrics["usage-source"] == "unknown"
    assert metrics["input-tokens"] == ""


def test_runner_exception_is_recorded_then_reraised():
    metrics = {}

    def broken(*args, **kwargs):
        raise RuntimeError("runner broke")

    with pytest.raises(RuntimeError, match="runner broke"):
        session.invoke_session([], ".", 1, metrics=metrics, runner=broken)

    assert metrics["usage-status"] == "unavailable"
    assert metrics["error"] == "RuntimeError"
    assert metrics["wall-secs"] >= 0


def test_a_ctrl_c_in_an_attached_sitting_persists_a_complete_record(
    tmp_path, monkeypatch
):
    # KeyboardInterrupt is a BaseException: the pre-2026-09-06 boundary caught
    # Exception only, so the persisted `call_` log carried blank wall-secs,
    # ended-at and usage-status while the interrupt propagated.
    ac = load_script("agent_common")
    (tmp_path / "docs" / "iteration").mkdir(parents=True)
    committed = []
    monkeypatch.setattr(ac, "commit_telemetry", lambda *a, **k: committed.append(a))

    def interrupted(*args, **kwargs):
        raise KeyboardInterrupt

    metrics = {"requested-model": "m", "role": "INTERACTIVE"}
    with pytest.raises(KeyboardInterrupt):
        ac.invoke_and_persist(tmp_path, [], 1, metrics=metrics, runner=interrupted)

    assert metrics["outcome"] == "INTERRUPTED"
    assert metrics["usage-status"] == "unavailable"
    assert metrics["ended-at"] and metrics["wall-secs"] >= 0
    logs = list((tmp_path / "docs" / "iteration").glob("call_*.log"))
    assert len(logs) == 1 and committed, (logs, committed)
    header = logs[0].read_text(encoding="utf-8")
    assert "# outcome: INTERRUPTED" in header
    assert "# usage-status: unavailable" in header
    assert "# wall-secs: \n" not in header and "# ended-at: \n" not in header
