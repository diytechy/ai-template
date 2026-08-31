"""The adjudicator session-retention layer (WI-540).

Drives the pure mechanics of `adjudicator_session.py` and the `[adjudicator]`
config reader in `agent_common.py`: the dial-0 inert case, the per-family reset
clamp, the resume-argv adapter, the per-family occupancy readers, the store's
atomic round-trip, the drain/reset rule, the same-artifact guard and the
keep-warm decision — plus the structure parity between this repo's own
`docs/process.toml` and the shipped `process.toml.template`.

The layer ships INERT (`context_reset_pct = 0`), so the loop never exercises
these on the shipped dial; this suite is where they are exercised.
"""

import json
import tomllib
from pathlib import Path
from types import SimpleNamespace

from conftest import KIT, ROOT, load_script

adj = load_script("adjudicator_session")
ac = load_script("agent_common")
al = load_script("agent_loop")


# --- the config reader (agent_common.adjudicator_config) ----------------------
def _write_process_toml(tmp_path, body):
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "process.toml").write_text(body, encoding="utf-8")
    return docs


def test_dial_zero_is_inert(tmp_path):
    docs = _write_process_toml(tmp_path, "[adjudicator]\ncontext_reset_pct = 0\n")
    cfg = ac.adjudicator_config(docs)
    assert cfg.enabled is False
    assert cfg.context_reset_pct == 0


def test_absent_table_is_inert(tmp_path):
    docs = _write_process_toml(tmp_path, '[policies]\npush = "human"\n')
    assert ac.adjudicator_config(docs).enabled is False


def test_dial_on_parses_all_fields(tmp_path):
    docs = _write_process_toml(
        tmp_path,
        "[adjudicator]\n"
        "context_reset_pct = 55\n"
        'retain_for = ["disposition", "amendment"]\n'
        "keepwarm_minutes = 50\n"
        "reset_on_same_artifact = true\n",
    )
    cfg = ac.adjudicator_config(docs)
    assert cfg.enabled is True
    assert cfg.context_reset_pct == 55
    assert cfg.retain_for == ("disposition", "amendment")
    assert cfg.keepwarm_minutes == 50
    assert cfg.reset_on_same_artifact is True


def test_wrong_types_fail_closed_to_off(tmp_path):
    # A mistyped dial must read inert, never silently armed (fail-closed-to-OFF).
    docs = _write_process_toml(
        tmp_path,
        "[adjudicator]\n"
        'context_reset_pct = "55"\n'  # a string, not an int
        "keepwarm_minutes = -3\n"  # negative
        'reset_on_same_artifact = "yes"\n',  # a string, not a bool
    )
    cfg = ac.adjudicator_config(docs)
    assert cfg.enabled is False
    assert cfg.context_reset_pct == 0
    assert cfg.keepwarm_minutes == 0
    assert cfg.reset_on_same_artifact is False


def test_bool_pct_is_not_a_truthy_accident(tmp_path):
    # `True` is an int subclass in Python — it must not read as pct 1 / enabled.
    docs = _write_process_toml(tmp_path, "[adjudicator]\ncontext_reset_pct = true\n")
    assert ac.adjudicator_config(docs).enabled is False


def test_retain_for_defaults_when_not_a_list(tmp_path):
    docs = _write_process_toml(
        tmp_path, '[adjudicator]\ncontext_reset_pct = 40\nretain_for = "disposition"\n'
    )
    assert ac.adjudicator_config(docs).retain_for == ac.ADJUDICATOR_RETAIN_DEFAULT


# --- the per-family reset clamp (plan §2) -------------------------------------
def _cfg(pct):
    return ac.AdjudicatorConfig(
        enabled=pct > 0,
        context_reset_pct=pct,
        retain_for=(),
        keepwarm_minutes=0,
        reset_on_same_artifact=False,
    )


def test_codex_dial_clamps_to_85():
    assert adj.reset_pct_for_family(_cfg(90), "OPENAI") == (85, True)
    assert adj.reset_pct_for_family(_cfg(80), "OPENAI") == (80, False)


def test_anthropic_and_opencode_are_unclamped():
    assert adj.reset_pct_for_family(_cfg(95), "ANTHROPIC") == (95, False)
    assert adj.reset_pct_for_family(_cfg(95), "OPENCODE") == (95, False)


def test_inert_config_yields_zero_clamp():
    assert adj.reset_pct_for_family(_cfg(0), "OPENAI") == (0, False)


# --- the session store (plan §3.1) --------------------------------------------
def test_store_round_trip_and_atomic_replace(tmp_path):
    record = adj.mint(
        "ANTHROPIC", "ANTHROPIC-OPUS-STRONG", "sid-1", "hash", "2026-01-01T00:00:00Z"
    )
    adj.save(tmp_path, record)
    loaded = adj.load(tmp_path, "ANTHROPIC", "ANTHROPIC-OPUS-STRONG")
    assert loaded["session_id"] == "sid-1"
    assert loaded["state"] == adj.STATE_ACTIVE
    assert loaded["generation"] == 1
    # No leftover temp file after an atomic replace.
    assert not list(adj.store_dir(tmp_path).glob("*.tmp"))


def test_corrupt_store_reads_as_no_session(tmp_path):
    adj.store_dir(tmp_path).mkdir(parents=True)
    adj.store_path(tmp_path, "ANTHROPIC", "route-a").write_text(
        "{not json", encoding="utf-8"
    )
    assert adj.load(tmp_path, "ANTHROPIC", "route-a") is None


def test_retire_keeps_the_file_and_generation(tmp_path):
    record = adj.mint("OPENAI", "r", "sid", "h", "t")
    record["generation"] = 3
    adj.save(tmp_path, record)
    adj.retire(tmp_path, record)
    loaded = adj.load(tmp_path, "OPENAI", "r")
    assert loaded["state"] == adj.STATE_RETIRED
    assert loaded["generation"] == 3  # kept so the next mint can increment it


def test_clear_unlinks(tmp_path):
    adj.save(tmp_path, adj.mint("OPENCODE", "r", "s", "h", "t"))
    adj.clear(tmp_path, "OPENCODE", "r")
    assert adj.load(tmp_path, "OPENCODE", "r") is None
    adj.clear(tmp_path, "OPENCODE", "r")  # absent file is a no-op


def test_store_is_keyed_by_family_and_route(tmp_path):
    first = adj.mint("OPENAI", "OPENAI-A", "sid-a", "h", "t")
    second = adj.mint("OPENAI", "OPENAI-B", "sid-b", "h", "t")
    adj.save(tmp_path, first)
    adj.save(tmp_path, second)

    assert adj.load(tmp_path, "OPENAI", "OPENAI-A")["session_id"] == "sid-a"
    assert adj.load(tmp_path, "OPENAI", "OPENAI-B")["session_id"] == "sid-b"
    assert adj.store_path(tmp_path, "OPENAI", "OPENAI-A") != adj.store_path(
        tmp_path, "OPENAI", "OPENAI-B"
    )


def test_load_family_enumerates_only_that_familys_valid_records(tmp_path):
    adj.save(tmp_path, adj.mint("ANTHROPIC", "ANTHROPIC-B", "sid-b", "h", "t"))
    adj.save(tmp_path, adj.mint("ANTHROPIC", "ANTHROPIC-A", "sid-a", "h", "t"))
    adj.save(tmp_path, adj.mint("OPENAI", "OPENAI-A", "sid-c", "h", "t"))
    # A corrupt file and a misplaced one (content's route id does not key the
    # file it sits in) are both skipped, never cross-read.
    adj.store_dir(tmp_path).mkdir(parents=True, exist_ok=True)
    adj.store_path(tmp_path, "ANTHROPIC", "corrupt").write_text(
        "{not json", encoding="utf-8"
    )
    misplaced = adj.mint("ANTHROPIC", "ANTHROPIC-REAL", "sid-m", "h", "t")
    adj.store_path(tmp_path, "ANTHROPIC", "ANTHROPIC-ALIAS").write_text(
        json.dumps(misplaced), encoding="utf-8"
    )

    records = adj.load_family(tmp_path, "ANTHROPIC")

    assert [r["route_id"] for r in records] == ["ANTHROPIC-A", "ANTHROPIC-B"]
    assert adj.load_family(tmp_path, "OPENCODE") == []


# --- the resume-argv adapter (plan §3.2) --------------------------------------
def test_anthropic_mint_appends_session_id_uuid():
    tmpl, mint_id = adj.resume_template(
        "ANTHROPIC", "claude -p --model {model} --verbose", None
    )
    tokens = json.loads(tmpl)
    assert tokens[-2] == "--session-id"
    assert tokens[-1] == mint_id and len(mint_id) == 36  # a uuid4
    assert "{model}" in tokens  # the placeholder survives for build_argv


def test_anthropic_resume_appends_resume_id():
    tmpl, mint_id = adj.resume_template(
        "ANTHROPIC", "claude -p --model {model}", {"session_id": "abc"}
    )
    assert json.loads(tmpl)[-2:] == ["--resume", "abc"]
    assert mint_id == ""


def test_codex_mint_adds_json():
    tmpl, mint_id = adj.resume_template("OPENAI", "codex exec --model {model}", None)
    assert "--json" in json.loads(tmpl)
    assert mint_id == ""


def test_codex_resume_inserts_resume_and_strips_c_and_ephemeral():
    tmpl, _ = adj.resume_template(
        "OPENAI",
        "codex exec -C /some/dir --ephemeral --model {model}",
        {"session_id": "t1"},
    )
    tokens = json.loads(tmpl)
    assert tokens[:4] == ["codex", "exec", "resume", "t1"]
    assert "-C" not in tokens and "/some/dir" not in tokens
    assert "--ephemeral" not in tokens
    assert "--json" in tokens


def test_opencode_mint_and_resume():
    mint_tmpl, _ = adj.resume_template(
        "OPENCODE", "opencode run --dir . -m {model} --auto", None
    )
    assert json.loads(mint_tmpl)[-2:] == ["--format", "json"]
    resume_tmpl, _ = adj.resume_template(
        "OPENCODE", "opencode run --dir . -m {model} --auto", {"session_id": "s9"}
    )
    tokens = json.loads(resume_tmpl)
    assert "--format" in tokens and tokens[-2:] == ["--session", "s9"]


def test_unknown_family_passthrough():
    tmpl, mint_id = adj.resume_template("GEMINI", "gemini -p {model}", None)
    assert tmpl == "gemini -p {model}" and mint_id == ""


# --- dedicated homes (plan §4; OI-69 (e1)) ------------------------------------
def test_dedicated_home_env_per_family(tmp_path):
    assert "CLAUDE_CONFIG_DIR" in adj.dedicated_home_env("ANTHROPIC", {}, tmp_path)
    assert "CODEX_HOME" in adj.dedicated_home_env("OPENAI", {}, tmp_path)
    assert "OPENCODE_CONFIG" in adj.dedicated_home_env("OPENCODE", {}, tmp_path)
    assert adj.dedicated_home_env("GEMINI", {}, tmp_path) == {}


# --- occupancy readers (plan §3.3) --------------------------------------------
def test_anthropic_occupancy_sums_four_counters():
    usage = {
        "input_tokens": 10,
        "output_tokens": 5,
        "cache_read_input_tokens": 3,
        "cache_creation_input_tokens": 2,
    }
    assert adj.anthropic_occupancy(usage) == 20
    assert adj.anthropic_occupancy({}) == 0


def test_codex_occupancy_reads_last_event():
    events = [
        {
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {
                    "last_token_usage": {"total_tokens": 100},
                    "model_context_window": 200_000,
                },
            },
        },
        {
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {
                    "last_token_usage": {"total_tokens": 250},
                    "model_context_window": 300_000,
                },
            },
        },
        {"unrelated": True},
    ]
    assert adj.codex_occupancy(events) == 250
    assert adj.codex_window(events) == 300_000
    assert adj.codex_occupancy([]) == 0


def test_opencode_occupancy_reads_last_step_finish():
    events = [
        {"type": "step_finish", "part": {"tokens": {"total": 40}}},
        {"type": "text"},
        {"type": "step_finish", "part": {"tokens": {"total": 77}}},
    ]
    assert adj.opencode_occupancy(events) == 77


def test_pct_of_never_guesses_on_a_missing_window():
    assert adj.pct_of(500_000, 1_000_000) == 50
    assert adj.pct_of(500_000, 0) == ""
    assert adj.pct_of(500_000, "") == ""


# --- the governing-inputs hash (plan §3.4 rule 2) -----------------------------
def test_governing_hash_changes_with_a_governing_file(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("one", encoding="utf-8")
    first = adj.governing_hash(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("two", encoding="utf-8")
    assert adj.governing_hash(tmp_path) != first
    # Deterministic for an unchanged tree.
    assert adj.governing_hash(tmp_path) == adj.governing_hash(tmp_path)


def test_governing_hash_changes_with_the_loaded_adjudication_template(tmp_path):
    template = tmp_path / "prompts" / "adjudicate-disposition.md"
    template.parent.mkdir()
    template.write_text("judge one", encoding="utf-8")
    first = adj.governing_hash(tmp_path, (template,))
    template.write_text("judge two", encoding="utf-8")
    assert adj.governing_hash(tmp_path, (template,)) != first


def test_preflight_surfaces_the_loaded_adjudication_template_to_the_hash(tmp_path):
    # The production half of the same rule: the loop's preflight is what hands
    # `adjudicator_prompt_paths` to the launch, so the path it surfaces for a
    # brief's prompt must be the file actually loaded — an operator override,
    # not silently the shipped kit file — and the hash over those surfaced
    # paths must move when the judging instruction does.
    ab = load_script("adjudicate_brief")
    override = tmp_path / "custom-disposition.md"
    override.write_text("judge one", encoding="utf-8")
    prompt_map = {"ADJUDICATE-DISPOSITION": str(override)}

    def adjudication_hash():
        _, _, paths = al.map_preflight(
            tmp_path,
            "",
            SimpleNamespace(),
            {},
            prompt_map,
            {},
            {},
            False,
            {},
            [],
            [],
            [],
        )
        assert Path(paths["ADJUDICATE-DISPOSITION"]) == override
        return adj.governing_hash(
            tmp_path, tuple(paths[key] for key in ab.BRIEF_PROMPTS.values())
        )

    first = adjudication_hash()
    override.write_text("judge two", encoding="utf-8")
    assert adjudication_hash() != first


# --- the drain / reset rule (plan §3.4) ---------------------------------------
def _active(**over):
    record = adj.mint("ANTHROPIC", "r", "s", "h0", "t")
    record.update(over)
    return record


def test_drain_on_crest():
    assert adj.drain_reason(_active(), 60, 55, "h0", "") == "crest 60% >= 55%"


def test_reset_pct_zero_never_crests():
    assert adj.drain_reason(_active(), 99, 0, "h0", "") is None


def test_drain_on_governing_change_and_version_drift():
    assert "governing" in adj.drain_reason(_active(), 10, 55, "h1", "")
    assert "version" in adj.drain_reason(
        _active(cli_version="1.0"), 10, 55, "h0", "2.0"
    )


def test_already_draining_returns_no_new_reason():
    assert (
        adj.drain_reason(_active(state=adj.STATE_DRAINING), 99, 55, "hX", "9") is None
    )


def test_retire_now_on_unusable_and_same_artifact():
    assert adj.retire_now_reason(True, True, False, (), []) == "session unusable"
    assert adj.retire_now_reason(False, False, False, (), []) == "session unusable"
    assert (
        adj.retire_now_reason(False, True, True, ["WI-1"], ["WI-1"])
        == "same-artifact guard"
    )
    assert adj.retire_now_reason(False, True, True, ["WI-2"], ["WI-1"]) is None
    assert adj.retire_now_reason(False, True, False, ["WI-1"], ["WI-1"]) is None


def test_is_clear_point():
    assert adj.is_clear_point([]) is True
    assert adj.is_clear_point(["WI-1"]) is False


# --- keep-warm (plan §3.5; OI-69 (c2)) ----------------------------------------
def _warm_cfg(minutes):
    return ac.AdjudicatorConfig(
        enabled=minutes > 0,
        context_reset_pct=55,
        retain_for=(),
        keepwarm_minutes=minutes,
        reset_on_same_artifact=False,
    )


def test_keepwarm_due_gating():
    record = _active()
    cfg = _warm_cfg(50)
    now = 100_000
    # Due: active, anthropic, work pending, elapsed >= 50 min.
    assert adj.keepwarm_due(record, cfg, "ANTHROPIC", now, now - 3000, True) is True
    # Not yet elapsed.
    assert adj.keepwarm_due(record, cfg, "ANTHROPIC", now, now - 100, True) is False
    # No work pending.
    assert adj.keepwarm_due(record, cfg, "ANTHROPIC", now, now - 3000, False) is False
    # Non-anthropic never pings.
    assert adj.keepwarm_due(record, cfg, "OPENAI", now, now - 3000, True) is False
    # Dial off.
    assert (
        adj.keepwarm_due(record, _warm_cfg(0), "ANTHROPIC", now, now - 3000, True)
        is False
    )
    # A draining session is not kept warm.
    assert (
        adj.keepwarm_due(
            _active(state=adj.STATE_DRAINING), cfg, "ANTHROPIC", now, now - 3000, True
        )
        is False
    )


# --- the loop-side launch hook (agent_loop.adjudicator_launch) ----------------
def test_launch_is_a_strict_no_op_when_dial_off(tmp_path):
    docs = _write_process_toml(tmp_path, "[adjudicator]\ncontext_reset_pct = 0\n")
    env_in = {"X": "1"}
    tmpl, env, meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "ANTHROPIC",
        "disposition",
        "WI-1",
        "claude -p --model {model}",
        env_in,
        route_id="ANTHROPIC-A",
    )
    assert tmpl == "claude -p --model {model}"
    assert env is env_in  # unchanged object — byte-for-byte today's launch
    assert meta is None


def test_launch_mints_when_on_for_a_retained_class(tmp_path):
    docs = _write_process_toml(
        tmp_path,
        '[adjudicator]\ncontext_reset_pct = 55\nretain_for = ["disposition"]\n',
    )
    tmpl, env, meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "ANTHROPIC",
        "disposition",
        "WI-1",
        "claude -p --model {model}",
        None,
        route_id="ANTHROPIC-A",
    )
    assert meta is not None and meta["family"] == "ANTHROPIC" and meta["wi"] == "WI-1"
    assert "--session-id" in json.loads(tmpl)
    assert meta["mint_id"] and meta["session_id"] == meta["mint_id"]
    assert "CLAUDE_CONFIG_DIR" in env
    # A non-retained brief class stays a no-op even with the dial on.
    _, _, none = al.adjudicator_launch(
        tmp_path,
        docs,
        "ANTHROPIC",
        "red-tc",
        "WI-1",
        "claude -p",
        None,
        route_id="ANTHROPIC-A",
    )
    assert none is None


def test_launch_never_resumes_another_route_of_the_same_family(tmp_path):
    docs = _write_process_toml(
        tmp_path,
        '[adjudicator]\ncontext_reset_pct = 55\nretain_for = ["disposition"]\n',
    )
    adj.save(
        tmp_path,
        adj.mint("OPENAI", "OPENAI-A", "old-route-session", "h", "t"),
    )

    tmpl, _, meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "OPENAI",
        "disposition",
        "WI-2",
        "codex exec --model {model}",
        None,
        route_id="OPENAI-B",
    )

    tokens = json.loads(tmpl)
    assert "old-route-session" not in tokens
    assert tokens[:2] == ["codex", "exec"] and "resume" not in tokens
    assert meta["route_id"] == "OPENAI-B" and meta["resumed"] is False


def _retention_docs(tmp_path):
    return _write_process_toml(
        tmp_path,
        '[adjudicator]\ncontext_reset_pct = 55\nretain_for = ["disposition"]\n',
    )


def _ctx(tmp_path, docs):
    return SimpleNamespace(root=tmp_path, docs=docs)


def test_openai_bookkeeping_captures_thread_and_rollout_then_resumes(tmp_path):
    docs = _retention_docs(tmp_path)
    tmpl, env, meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "OPENAI",
        "disposition",
        "WI-1",
        "codex exec --model {model}",
        None,
        route_id="OPENAI-A",
    )
    assert "--json" in json.loads(tmpl)
    session_id = "019c-session-a"
    rollout = (
        Path(env["CODEX_HOME"])
        / "sessions"
        / "2026"
        / "08"
        / "31"
        / ("rollout-now-{}.jsonl".format(session_id))
    )
    rollout.parent.mkdir(parents=True)
    rollout.write_text(
        json.dumps(
            {
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {"total_tokens": 45_000},
                        "model_context_window": 200_000,
                    },
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    output = json.dumps({"type": "thread.started", "thread_id": session_id})

    telemetry = al.adjudicator_bookkeeping(
        _ctx(tmp_path, docs),
        {"adjudicator": meta, "session_env": env},
        al.parse_json_result(output),
        False,
        1_000,
        output,
    )

    record = adj.load(tmp_path, "OPENAI", "OPENAI-A")
    assert record["session_id"] == session_id
    assert (record["occupancy"], record["window"], record["pct"]) == (
        45_000,
        200_000,
        22,
    )
    assert telemetry["session-id"] == session_id
    resumed, _, resumed_meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "OPENAI",
        "disposition",
        "WI-2",
        "codex exec --model {model}",
        None,
        route_id="OPENAI-A",
    )
    assert json.loads(resumed)[:4] == ["codex", "exec", "resume", session_id]
    assert resumed_meta["resumed"] is True


def test_opencode_bookkeeping_captures_stream_session_then_resumes(tmp_path):
    docs = _retention_docs(tmp_path)
    _, _, meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "OPENCODE",
        "disposition",
        "WI-1",
        "opencode run -m {model}",
        None,
        route_id="OPENCODE-A",
    )
    events = [
        {"type": "step_start", "sessionID": "ses-a"},
        {
            "type": "step_finish",
            "sessionID": "ses-a",
            "part": {"tokens": {"total": 77_000}},
        },
    ]
    output = "\n".join(json.dumps(event) for event in events)

    al.adjudicator_bookkeeping(
        _ctx(tmp_path, docs),
        {"adjudicator": meta},
        events[-1],
        False,
        1_000,
        output,
    )

    record = adj.load(tmp_path, "OPENCODE", "OPENCODE-A")
    assert record["session_id"] == "ses-a" and record["occupancy"] == 77_000
    resumed, _, resumed_meta = al.adjudicator_launch(
        tmp_path,
        docs,
        "OPENCODE",
        "disposition",
        "WI-2",
        "opencode run -m {model}",
        None,
        route_id="OPENCODE-A",
    )
    assert json.loads(resumed)[-2:] == ["--session", "ses-a"]
    assert resumed_meta["resumed"] is True


def test_loaded_adjudication_prompt_change_retires_at_clear_point(tmp_path):
    docs = _retention_docs(tmp_path)
    prompt = tmp_path / "prompts" / "adjudicate-disposition.md"
    prompt.parent.mkdir()
    prompt.write_text("judge one", encoding="utf-8")
    _, _, first = al.adjudicator_launch(
        tmp_path,
        docs,
        "ANTHROPIC",
        "disposition",
        "WI-1",
        "claude -p --model {model}",
        None,
        route_id="ANTHROPIC-A",
        template_paths=(prompt,),
    )
    al.adjudicator_bookkeeping(
        _ctx(tmp_path, docs),
        {"adjudicator": first},
        {"session_id": first["session_id"]},
        False,
        1_000,
        "",
    )
    prompt.write_text("judge two", encoding="utf-8")

    tmpl, _, second = al.adjudicator_launch(
        tmp_path,
        docs,
        "ANTHROPIC",
        "disposition",
        "WI-2",
        "claude -p --model {model}",
        None,
        route_id="ANTHROPIC-A",
        template_paths=(prompt,),
    )

    assert first["governing_hash"] != second["governing_hash"]
    assert "--resume" not in json.loads(tmpl)
    assert second["resumed"] is False


def test_resume_record_same_artifact_guard_retires(tmp_path):
    cfg = ac.AdjudicatorConfig(True, 55, ("disposition",), 0, True)  # guard on
    record = adj.mint("ANTHROPIC", "r", "sid", "h", "t")
    record["judged"] = ["WI-1"]
    adj.save(tmp_path, record)
    # The row about to be judged was already judged -> retire, mint fresh.
    assert (
        al._adjudicator_resume_record(tmp_path, cfg, "ANTHROPIC", "WI-1", route_id="r")
        is None
    )
    assert adj.load(tmp_path, "ANTHROPIC", "r")["state"] == adj.STATE_RETIRED


def test_resume_record_draining_continuation_vs_clear_point(tmp_path):
    cfg = ac.AdjudicatorConfig(True, 55, ("disposition",), 0, False)
    record = adj.mint("ANTHROPIC", "r", "sid", "h", "t")
    record["state"] = adj.STATE_DRAINING
    record["judged"] = ["WI-1"]
    adj.save(tmp_path, record)
    # A row continuing the session's chain keeps it resumed mid-drain.
    assert (
        al._adjudicator_resume_record(tmp_path, cfg, "ANTHROPIC", "WI-1", route_id="r")
        is not None
    )
    # A row that does not continue is a clear point -> retire.
    assert (
        al._adjudicator_resume_record(tmp_path, cfg, "ANTHROPIC", "WI-9", route_id="r")
        is None
    )
    assert adj.load(tmp_path, "ANTHROPIC", "r")["state"] == adj.STATE_RETIRED


# --- structure parity: this repo's process.toml vs the shipped template --------
def test_adjudicator_table_parity_between_instance_and_template():
    live = tomllib.loads(
        (ROOT / "docs" / "process.toml").read_text(encoding="utf-8-sig")
    )
    template = tomllib.loads(
        (KIT / "process.toml.template").read_text(encoding="utf-8-sig")
    )
    assert "adjudicator" in live and "adjudicator" in template
    # VALUES may diverge; the KEY SET (structure) must not.
    assert set(live["adjudicator"]) == set(template["adjudicator"])
    # And both ship the dial OFF.
    assert live["adjudicator"]["context_reset_pct"] == 0
    assert template["adjudicator"]["context_reset_pct"] == 0
