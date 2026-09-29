"""The session service's keep operation: adjudicator session retention.

Retention rides the service's act and record steps: resuming by id, reading
occupancy, draining and resetting, and the keep-warm ping are all ordinary
calls through `session_service`, and the layer is INERT at the shipped
`[adjudicator] context_reset_pct = 0`. The rules and the store are
`session_keep`'s. Driven in memory with an injected launch over the recorded
fixtures in `tests/golden/sessions/` (the claude one LIVE; the codex and
opencode ones NOT LIVE, built from documented event shapes and owed a live
recording by a person). The store lives under a temporary repository root.
"""

import json
import threading
import tomllib
from pathlib import Path

import pytest

from conftest import ROOT, load_script

svc = load_script("session_service")
keep = load_script("session_keep")
adapters = load_script("session_adapters")
common = load_script("agent_common")

GOLDEN = Path(__file__).parent / "golden" / "sessions"
TEMPLATES = {
    "ANTHROPIC": "claude -p --model {model} --output-format stream-json --verbose",
    "OPENAI": "codex exec --model {model}",
    "OPENCODE": "opencode run --dir . -m {model} --auto",
}
STREAMS = {
    "ANTHROPIC": "claude-stream-json.jsonl",
    "OPENAI": "codex-exec-json.jsonl",
    "OPENCODE": "opencode-run-json.jsonl",
}
ON = keep.KeepConfig(context_reset_pct=50, keepwarm_minutes=50)


def _fixture(name):
    return (GOLDEN / name).read_text(encoding="utf-8")


def _launch(stream, code=0, timed_out=False, seen=None, envs=None):
    def run(argv, root, timeout, **kwargs):
        if seen is not None:
            seen.append(list(argv))
        if envs is not None:
            envs.append(kwargs.get("env"))
        if "--output-last-message" in argv:
            path = argv[argv.index("--output-last-message") + 1]
            Path(path).write_text("VERDICT", encoding="utf-8")
        return code, stream, timed_out

    return run


def _call(tmp_path, family, kept, runner, role="ADJUDICATE"):
    return svc.Call(
        root=tmp_path,
        role=role,
        template=TEMPLATES[family],
        model="m",
        prompt="judge",
        provider=family,
        route_id=family + "-ROUTE",
        keep=kept,
        runner=runner,
    )


def _keep(tmp_path, cfg, family="ANTHROPIC", wi="WI-1", brief="disposition", **kw):
    kw.setdefault("lease_wait", 0)
    return keep.keep_for(
        tmp_path,
        cfg,
        role="ADJUDICATE",
        brief=brief,
        family=family,
        route_id=family + "-ROUTE",
        wi=wi,
        **kw,
    )


# --- dial 0: the layer is inert (TC-266) ----------------------------------------


def test_the_shipped_dial_is_off_in_both_policy_files_with_one_structure():
    live = tomllib.loads((ROOT / "docs" / "process.toml").read_text(encoding="utf-8"))
    kit = (ROOT / "project-trajectory" / "process.toml.template").read_text(
        encoding="utf-8"
    )
    template = tomllib.loads(kit)
    assert live["adjudicator"]["context_reset_pct"] == 0
    assert template["adjudicator"]["context_reset_pct"] == 0
    assert set(live["adjudicator"]) == set(template["adjudicator"])
    assert keep.keep_config(ROOT) == keep.KeepConfig()
    assert not keep.keep_config(ROOT).enabled


def test_at_dial_zero_an_adjudication_launches_exactly_as_a_fresh_session(
    tmp_path, monkeypatch
):
    ran = []
    monkeypatch.setattr(svc, "cli_version", lambda *a, **k: ran.append(a) or "")
    kept = svc.plan_keep(
        tmp_path,
        keep.KeepConfig(),
        template=TEMPLATES["ANTHROPIC"],
        role="ADJUDICATE",
        brief="disposition",
        family="ANTHROPIC",
        route_id="ANTHROPIC-ROUTE",
        wi="WI-1",
    )
    assert kept is None and ran == []  # nothing minted, no version read
    stream = _fixture(STREAMS["ANTHROPIC"])
    retained, fresh, envs = [], [], []
    svc.act(
        _call(tmp_path, "ANTHROPIC", kept, _launch(stream, seen=retained, envs=envs))
    )
    svc.act(_call(tmp_path, "ANTHROPIC", None, _launch(stream, seen=fresh, envs=envs)))
    assert retained == fresh
    assert envs == [None, None]  # the ambient environment, exactly
    assert "--session-id" not in retained[0] and "--resume" not in retained[0]
    assert not keep.store_dir(tmp_path).exists()


def test_a_missing_or_malformed_table_reads_as_the_off_dial(tmp_path):
    (tmp_path / "docs").mkdir()
    assert keep.keep_config(tmp_path) == keep.KeepConfig()
    (tmp_path / "docs" / "process.toml").write_text(
        '[adjudicator]\ncontext_reset_pct = "lots"\n', encoding="utf-8"
    )
    assert not keep.keep_config(tmp_path).enabled


def test_only_a_retained_adjudication_class_is_kept(tmp_path):
    assert _keep(tmp_path, ON, brief="first-approval") is None
    assert not keep.applies(ON, "REVIEW-A", "disposition", "R")
    assert _keep(tmp_path, ON) is not None


def test_the_dispatcher_keeps_nothing_warm_at_dial_zero(tmp_path):
    assert svc.keep_warmer(tmp_path, keep.KeepConfig()) is None
    assert svc.keep_warmer(tmp_path, keep.KeepConfig(context_reset_pct=50)) is None
    assert not keep.store_dir(tmp_path).exists()


def _loop_ctx(root):
    from types import SimpleNamespace

    return SimpleNamespace(
        root=root, prompt_templates={}, args=SimpleNamespace(session_timeout=60)
    )


PLAN = {
    "phase": "ADJUDICATE",
    "brief": "disposition",
    "route_family": "ANTHROPIC",
    "route_id": "ANTHROPIC-ROUTE",
    "tmpl": TEMPLATES["ANTHROPIC"],
    "session_env": None,
}


def test_the_loop_retains_nothing_at_the_shipped_dial(tmp_path):
    al = load_script("agent_loop")
    assert al.adjudication_keep(_loop_ctx(tmp_path), PLAN, "WI-1") is None
    assert al.adjudication_keep(_loop_ctx(ROOT), PLAN, "WI-1") is None


# --- dial on: resume and occupancy per provider (TC-267) -----------------------


@pytest.mark.parametrize(
    "family,session_id,used",
    [
        ("ANTHROPIC", None, 48267),
        ("OPENAI", "0199a213-81c0-7800-8aa1-bbab2a035a53", ""),
        ("OPENCODE", "ses_6a1f0c2e5ffeQk2VbQ9rX1a7Lm", 9990),
    ],
)
def test_a_first_adjudication_mints_and_the_next_resumes(
    tmp_path, family, session_id, used
):
    seen = []
    stream = _fixture(STREAMS[family])
    first = svc.act(
        _call(tmp_path, family, _keep(tmp_path, ON, family), _launch(stream, seen=seen))
    )
    record = keep.store_load(tmp_path, family, family + "-ROUTE")
    assert record["state"] == "active" and record["generation"] == 1
    if family == "ANTHROPIC":
        # claude takes a pre-minted id; the others report theirs.
        minted = seen[0][seen[0].index("--session-id") + 1]
        assert record["session_id"] == minted
    else:
        assert record["session_id"] == session_id
    assert record["occupancy"] == used
    assert first.metrics["session-gen"] == 1
    assert record["judged"] == ["WI-1"]
    assert "lease" not in record  # released when the call was bookkept

    svc.act(
        _call(tmp_path, family, _keep(tmp_path, ON, family), _launch(stream, seen=seen))
    )
    resumed = seen[1]
    sid = record["session_id"]
    if family == "ANTHROPIC":
        assert resumed[resumed.index("--resume") + 1] == sid
    elif family == "OPENAI":
        at = resumed.index("exec")
        assert resumed[at + 1 : at + 3] == ["resume", sid]
    else:
        assert resumed[resumed.index("--session") + 1] == sid


def test_codex_resume_drops_a_working_directory_and_ephemeral_flag():
    argv = adapters.adapter_for(["codex"]).resume(
        ["codex", "exec", "-C", "/elsewhere", "--ephemeral", "--json"], "T1"
    )
    assert argv[:4] == ["codex", "exec", "resume", "T1"]
    assert "-C" not in argv and "--ephemeral" not in argv


def test_a_retained_codex_route_runs_under_its_dedicated_home_and_reads_occupancy(
    tmp_path,
):
    """The route-level path: a retained codex adjudication launches with the
    dedicated CODEX_HOME the owner ruled for retention, and its occupancy is
    read from the rollout under that home."""
    thread = "0199a213-81c0-7800-8aa1-bbab2a035a53"
    kept = _keep(tmp_path, ON, "OPENAI")
    home = Path(kept.home_env["CODEX_HOME"])
    assert home.is_dir() and home.parent.parent == keep.store_dir(tmp_path)
    day = home / "sessions" / "2026" / "09" / "28"
    day.mkdir(parents=True)
    (day / "rollout-2026-09-28T05-10-01-{}.jsonl".format(thread)).write_text(
        _fixture("codex-rollout.jsonl"), encoding="utf-8"
    )
    envs = []
    out = svc.act(
        _call(
            tmp_path,
            "OPENAI",
            kept,
            _launch(_fixture(STREAMS["OPENAI"]), envs=envs),
        )
    )
    assert envs[0]["CODEX_HOME"] == str(home)
    assert out.metrics["context-used"] == 12463
    assert keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")["pct"] == 5


def test_an_unretained_codex_call_reads_occupancy_under_the_inherited_home(
    tmp_path, monkeypatch
):
    thread = "0199a213-81c0-7800-8aa1-bbab2a035a53"
    day = tmp_path / "home" / "sessions" / "2026"
    day.mkdir(parents=True)
    (day / "rollout-x-{}.jsonl".format(thread)).write_text(
        _fixture("codex-rollout.jsonl"), encoding="utf-8"
    )
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "home"))
    out = svc.act(_call(tmp_path, "OPENAI", None, _launch(_fixture(STREAMS["OPENAI"]))))
    assert out.metrics["context-used"] == 12463  # env=None inherits CODEX_HOME


# --- dial on: the reset rules (TC-267) ------------------------------------------


def _claude_stream(pct, window=1000000, is_error=False, sid="S"):
    used = pct * window // 100
    return "\n".join(
        [
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "model": "m",
                        "usage": {"input_tokens": used, "output_tokens": 1},
                    },
                }
            ),
            json.dumps(
                {
                    "type": "result",
                    "is_error": is_error,
                    "session_id": sid,
                    "usage": {"input_tokens": used, "output_tokens": 1},
                    "modelUsage": {"m": {"contextWindow": window}},
                }
            ),
        ]
    )


def _adjudicate(tmp_path, cfg, stream, wi="WI-1", code=0, timed_out=False, **kw):
    return svc.act(
        _call(
            tmp_path,
            "ANTHROPIC",
            _keep(tmp_path, cfg, wi=wi, **kw),
            _launch(stream, code=code, timed_out=timed_out),
        )
    )


def _state(tmp_path):
    return keep.store_load(tmp_path, "ANTHROPIC", "ANTHROPIC-ROUTE")


def _rows(**statuses):
    """Work-item rows: `WI_n="status[:adjudication][:pred=WI-m]"`."""
    rows = {}
    for key, spec in statuses.items():
        parts = spec.split(":")
        row = {"Status": parts[0], "SafetyClass": "", "Predecessors": ""}
        for part in parts[1:]:
            if part == "adjudication":
                row["SafetyClass"] = "adjudication"
            elif part.startswith("pred="):
                row["Predecessors"] = part[5:]
        rows[key.replace("_", "-")] = row
    return rows


def test_a_session_under_the_dial_stays_active(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(20))
    assert _state(tmp_path)["state"] == "active"
    assert _state(tmp_path)["pct"] == 20


def test_cresting_the_dial_drains_and_does_not_retire(tmp_path):
    out = _adjudicate(tmp_path, ON, _claude_stream(60))
    assert _state(tmp_path)["state"] == "draining"
    assert out.metrics["reset-reason"] == "crest 60% >= 50%"


def test_a_draining_session_resumes_while_its_chain_has_a_queued_adjudication(
    tmp_path,
):
    _adjudicate(tmp_path, ON, _claude_stream(60), wi="WI-1")
    minted = _state(tmp_path)["session_id"]
    rows = _rows(WI_1="done", WI_2="queued:adjudication:pred=WI-1", WI_9="queued")
    kept = _keep(tmp_path, ON, wi="WI-9", rows=rows)
    assert kept.session_id == minted  # WI-2 continues its chain: not clear
    assert _state(tmp_path)["state"] == "draining"


def test_a_draining_session_resumes_while_a_lane_is_out_on_its_chain(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(60), wi="WI-1")
    rows = _rows(WI_1="done", WI_3="active:pred=WI-1", WI_9="queued")
    assert _keep(tmp_path, ON, wi="WI-9", rows=rows).session_id != ""


def test_a_draining_session_resumes_for_an_item_that_continues_its_chain(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(60), wi="WI-1")
    rows = _rows(WI_1="done", WI_4="queued:adjudication:pred=WI-1")
    assert _keep(tmp_path, ON, wi="WI-4", rows=rows).session_id != ""


def test_a_draining_session_retires_at_a_clear_point(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(60), wi="WI-1")
    rows = _rows(WI_1="done", WI_2="done:pred=WI-1", WI_9="queued")
    kept = _keep(tmp_path, ON, wi="WI-9", rows=rows)
    assert kept.session_id == ""  # the next launch is fresh
    assert _state(tmp_path)["state"] == "retired"
    seen = []
    svc.act(_call(tmp_path, "ANTHROPIC", kept, _launch(_claude_stream(5), seen=seen)))
    assert "--session-id" in seen[0]
    assert _state(tmp_path)["generation"] == 2


@pytest.mark.parametrize(
    "stream_kw,code,timed_out",
    [({"is_error": True}, 0, False), ({}, 1, False), ({}, -1, "idle")],
)
def test_an_errored_session_retires_at_once(tmp_path, stream_kw, code, timed_out):
    out = _adjudicate(
        tmp_path, ON, _claude_stream(10, **stream_kw), code=code, timed_out=timed_out
    )
    assert _state(tmp_path)["state"] == "retired"
    assert out.metrics["reset-reason"] == "session unusable"


def test_a_raising_retained_launch_retires_the_session(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    kept = _keep(tmp_path, ON)
    assert kept.session_id

    def broken(*a, **k):
        raise RuntimeError("launch broke")

    with pytest.raises(RuntimeError):
        svc.act(_call(tmp_path, "ANTHROPIC", kept, broken))
    assert _state(tmp_path)["state"] == "retired"
    assert _state(tmp_path)["reset_reason"] == "session unusable"
    assert "lease" not in _state(tmp_path)


def test_changed_governing_inputs_drain_the_session(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    (tmp_path / "CLAUDE.md").write_text("a new rule", encoding="utf-8")
    _keep(tmp_path, ON, wi="WI-1")
    assert _state(tmp_path)["state"] == "draining"
    assert _state(tmp_path)["reset_reason"] == "governing-inputs changed"


def test_a_changed_loaded_skill_drains_the_session(tmp_path):
    skill = tmp_path / ".claude" / "skills" / "review" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("v1", encoding="utf-8")
    _adjudicate(tmp_path, ON, _claude_stream(10))
    skill.write_text("v2", encoding="utf-8")
    _keep(tmp_path, ON, wi="WI-1")
    assert _state(tmp_path)["reset_reason"] == "governing-inputs changed"


def test_cli_version_drift_drains_the_session(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(10), cli_version="2.1.266")
    assert _state(tmp_path)["cli_version"] == "2.1.266"
    _keep(tmp_path, ON, wi="WI-1", cli_version="2.1.300")
    assert _state(tmp_path)["state"] == "draining"
    assert _state(tmp_path)["reset_reason"] == "cli version 2.1.266 -> 2.1.300"


def test_the_runner_version_is_read_for_a_retained_launch(tmp_path, monkeypatch):
    from types import SimpleNamespace

    calls = []

    def fake_run(argv, **kw):
        calls.append(argv)
        return SimpleNamespace(returncode=0, stdout="2.1.266 (Claude Code)\n")

    monkeypatch.setattr(svc.subprocess, "run", fake_run)
    kept = svc.plan_keep(
        tmp_path,
        ON,
        template=TEMPLATES["ANTHROPIC"],
        role="ADJUDICATE",
        brief="disposition",
        family="ANTHROPIC",
        route_id="ANTHROPIC-ROUTE",
        wi="WI-1",
        lease_wait=0,
    )
    assert calls and calls[0][-1] == "--version"
    assert kept.cli_version == "2.1.266 (Claude Code)"


def test_the_same_artifact_guard_retires_before_rejudging(tmp_path):
    cfg = keep.KeepConfig(context_reset_pct=50, reset_on_same_artifact=True)
    _adjudicate(tmp_path, cfg, _claude_stream(10), wi="WI-1")
    kept = _keep(tmp_path, cfg, wi="WI-1")
    assert kept.session_id == ""
    assert _state(tmp_path)["state"] == "retired"


def test_the_codex_dial_is_clamped_to_its_own_compaction_limit():
    cfg = keep.KeepConfig(context_reset_pct=95)
    assert keep.reset_pct(cfg, "OPENAI") == 85
    assert keep.reset_pct(cfg, "ANTHROPIC") == 95


def test_the_loop_folds_the_adjudication_template_into_the_governing_inputs(
    tmp_path, monkeypatch
):
    al = load_script("agent_loop")
    monkeypatch.setattr(svc, "cli_version", lambda *a, **k: "")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "process.toml").write_text(
        "[adjudicator]\ncontext_reset_pct = 50\n", encoding="utf-8"
    )
    kit = al.adjudication_keep(_loop_ctx(tmp_path), PLAN, "WI-1")
    keep.keep_abandon(tmp_path, kit, "test")  # release the lease it took
    ctx = _loop_ctx(tmp_path)
    ctx.prompt_templates = {"ADJUDICATE-DISPOSITION": "an override brief"}
    override = al.adjudication_keep(ctx, PLAN, "WI-1")
    assert kit is not None and override is not None
    assert kit.governing != override.governing
    assert kit.governing != keep.governing_hash(tmp_path)


# --- the store: its lock, its lease (TC-267) --------------------------------------


def test_records_are_written_through_their_own_temporary_file(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    names = sorted(p.name for p in keep.store_dir(tmp_path).iterdir())
    assert not any(n.endswith(".tmp") for n in names)
    assert ".lock" not in names  # released after each write


def test_the_store_lock_excludes_a_second_holder(tmp_path):
    with keep.store_lock(tmp_path):
        with pytest.raises(keep.StoreBusy):
            with keep.store_lock(tmp_path, wait=0.1):
                pass
    with keep.store_lock(tmp_path, wait=0.1):
        pass  # free again once released


def test_an_adjudication_waits_out_a_keep_warm_lease_then_runs_unretained(
    tmp_path, capsys
):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    ping, reason = keep.take_warm_lease(
        tmp_path, ON, now=10**10, work_pending=True, holder="keep-warm:x"
    )
    assert ping is not None and reason is None
    assert _keep(tmp_path, ON, lease_wait=0) is None  # never races the ping
    assert "held by keep-warm:x" in capsys.readouterr().err


# --- keep-warm (TC-268) -------------------------------------------------------------


class _Row:
    def __init__(self, family, cmd_template=None):
        self.id = family + "-ROUTE"
        self.family = family
        self.model = "m"
        self.tier = "strong"
        self.cmd_template = cmd_template or TEMPLATES[family]
        self.env = ""


def test_keep_warm_is_due_only_for_an_active_anthropic_session_with_work():
    record = {"state": "active", "family": "ANTHROPIC", "last_used_epoch": 0}
    assert keep.keepwarm_due(record, ON, now=3001, work_pending=True)
    assert not keep.keepwarm_due(record, ON, now=2999, work_pending=True)
    assert not keep.keepwarm_due(record, ON, now=3001, work_pending=False)
    assert not keep.keepwarm_due({**record, "state": "draining"}, ON, 3001, True)
    assert not keep.keepwarm_due({**record, "family": "OPENAI"}, ON, 3001, True)
    assert not keep.keepwarm_due(record, keep.KeepConfig(), 3001, True)


def test_keep_warm_skips_a_session_an_adjudication_holds(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    assert _keep(tmp_path, ON) is not None  # an adjudication takes the lease
    ping, reason = keep.take_warm_lease(
        tmp_path, ON, now=10**10, work_pending=True, holder="keep-warm:x"
    )
    assert ping is None and reason.startswith("the session is leased to adjudicate:")


def test_keep_warm_pings_only_a_route_whose_adapter_bounds_one_turn(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    seen = []
    opencode = svc.KeepWarmer(
        tmp_path,
        ON,
        {"ANTHROPIC-ROUTE": _Row("ANTHROPIC", "opencode run -m anthropic/model")},
        runner=_launch(_claude_stream(11), seen=seen),
        clock=lambda: 10**10,
        dirty=lambda: False,
    )

    assert opencode.tick(work_pending=True) == []
    assert opencode.thread is None
    assert "lease" not in _state(tmp_path)
    assert seen == []

    claude = _warmer(tmp_path, _launch(_claude_stream(11), seen=seen))
    assert claude.tick(work_pending=True) == []
    claude.thread.join(10)
    assert seen
    argv = seen[0]
    assert argv[argv.index("--max-turns") + 1] == "1"


def _warmer(tmp_path, runner, dirty=lambda: False):
    return svc.KeepWarmer(
        tmp_path,
        ON,
        {"ANTHROPIC-ROUTE": _Row("ANTHROPIC")},
        runner=runner,
        clock=lambda: 10**10,
        dirty=dirty,
    )


def test_a_keep_warm_ping_is_one_bounded_turn_off_the_tick_and_recorded_on_it(
    tmp_path, monkeypatch
):
    """The enabled dispatcher path: the tick returns at once while the ping
    runs on its own thread, a second tick skips with its reason, and the
    session log is written and committed on the tick's thread afterwards."""
    committed = []
    monkeypatch.setattr(
        svc.agent_common,
        "commit_telemetry",
        lambda *a, **k: committed.append(threading.current_thread().name),
    )
    _adjudicate(tmp_path, ON, _claude_stream(10))
    minted = _state(tmp_path)["session_id"]
    release, seen = threading.Event(), []

    def slow(argv, root, timeout, **kw):
        seen.append(list(argv))
        release.wait(10)
        return 0, _claude_stream(11, sid=minted), False

    warmer = _warmer(tmp_path, slow)
    assert warmer.tick(work_pending=True) == []  # started, not waited on
    assert warmer.thread is not None and warmer.thread.is_alive()
    assert _state(tmp_path)["lease"]["holder"].startswith("keep-warm:")
    lines = warmer.tick(work_pending=True)
    assert lines == ["keep-warm: skipped (a ping is in flight)"]
    assert committed == []  # nothing recorded while the ping runs
    release.set()
    warmer.thread.join(10)
    warmer.tick(work_pending=False)  # records; with no work, starts no ping
    assert committed == [threading.current_thread().name]  # the tick's thread
    assert warmer.thread is None
    argv = seen[0]
    assert argv[argv.index("--resume") + 1] == minted
    assert argv[argv.index("--max-turns") + 1] == "1"
    (log,) = (tmp_path / "docs" / "iteration").glob("call_*.log")
    row = common.read_log_meta(log)
    assert row["role"] == "KEEP-WARM" and row["source-event"] == "keep-warm"
    assert row["outcome"] == "COMPLETED" and row["context-pct"] == "11"
    assert _state(tmp_path)["pct"] == 11 and "lease" not in _state(tmp_path)


def test_a_finished_ping_waits_for_a_clean_trunk_to_be_recorded(tmp_path, monkeypatch):
    committed = []
    monkeypatch.setattr(
        svc.agent_common, "commit_telemetry", lambda *a, **k: committed.append(1)
    )
    _adjudicate(tmp_path, ON, _claude_stream(10))
    dirty = [True]
    warmer = _warmer(tmp_path, _launch(_claude_stream(11)), dirty=lambda: dirty[0])
    warmer.tick(work_pending=True)
    warmer.thread.join(10)
    assert warmer.tick(work_pending=True) == [
        "keep-warm: session log held (the trunk is dirty)"
    ]
    assert committed == []
    dirty[0] = False
    warmer.tick(work_pending=False)
    assert committed == [1]


def test_keep_warm_skips_with_its_reason_when_an_adjudication_holds_the_lease(
    tmp_path,
):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    assert _keep(tmp_path, ON) is not None
    warmer = _warmer(tmp_path, _launch(_claude_stream(11)))
    (line,) = warmer.tick(work_pending=True)
    assert line.startswith("keep-warm: skipped (the session is leased to adjudicate:")
    assert warmer.thread is None
    assert warmer.tick(work_pending=True) == []  # said once


def test_the_run_end_records_a_ping_still_in_flight(tmp_path, monkeypatch):
    committed = []
    monkeypatch.setattr(
        svc.agent_common, "commit_telemetry", lambda *a, **k: committed.append(1)
    )
    _adjudicate(tmp_path, ON, _claude_stream(10))
    warmer = _warmer(tmp_path, _launch(_claude_stream(11)))
    warmer.tick(work_pending=True)
    warmer.finish()
    assert committed == [1]


def test_the_dispatcher_builds_its_warmer_from_the_routing_registry(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "agents.toml").write_text(
        '[agent.ANTHROPIC-ROUTE]\nfamily = "ANTHROPIC"\nmodel = "m"\n'
        'version = "1"\ntier = "strong"\n'
        'cmd_template = "claude -p --model {model}"\n'
        'env = "CLAUDE_CODE_EFFORT_LEVEL=high"\nnotes = ""\n',
        encoding="utf-8",
    )
    warmer = svc.keep_warmer(tmp_path, ON)
    row = warmer.registry["ANTHROPIC-ROUTE"]
    assert row.cmd_template == "claude -p --model {model}"
    assert svc._row_env(row)["CLAUDE_CODE_EFFORT_LEVEL"] == "high"


# --- round 3: lineage, shutdown, tombstone, the real dirty read -------------------


def test_a_re_adjudication_naming_only_the_worker_keeps_the_chain_open(tmp_path):
    """adjudication WI-1 -> worker WI-2 (pred WI-1) -> re-adjudication WI-3
    (pred WI-2 only): WI-3 still belongs to WI-1's chain through the worker,
    so a draining session is not at a clear point while WI-3 is queued."""
    _adjudicate(tmp_path, ON, _claude_stream(60), wi="WI-1")
    rows = _rows(
        WI_1="done",
        WI_2="done:pred=WI-1",
        WI_3="queued:adjudication:pred=WI-2",
        WI_9="queued",
    )
    assert keep.chain_pending(rows, ["WI-1"], "WI-9") == ["WI-3"]
    assert _keep(tmp_path, ON, wi="WI-9", rows=rows).session_id != ""
    assert _state(tmp_path)["state"] == "draining"


def test_the_lineage_is_followed_through_supersession_and_survives_a_cycle():
    rows = _rows(WI_1="done", WI_2="done", WI_3="active", WI_4="done:pred=WI-3")
    rows["WI-2"]["Supersedes"] = "WI-1"
    rows["WI-3"]["Predecessors"] = "WI-2;WI-4"  # a cycle back through WI-4
    assert keep.chain_pending(rows, ["WI-1"], "WI-9") == ["WI-3"]


def test_launching_the_re_adjudication_itself_continues_the_chain(tmp_path):
    _adjudicate(tmp_path, ON, _claude_stream(60), wi="WI-1")
    rows = _rows(
        WI_1="done", WI_2="done:pred=WI-1", WI_3="queued:adjudication:pred=WI-2"
    )
    assert not keep.is_clear_point(rows, ["WI-1"], "WI-3")
    assert _keep(tmp_path, ON, wi="WI-3", rows=rows).session_id != ""


def test_the_run_end_records_a_finished_ping_only_over_a_clean_trunk(
    tmp_path, monkeypatch, capsys
):
    committed = []
    monkeypatch.setattr(
        svc.agent_common, "commit_telemetry", lambda *a, **k: committed.append(1)
    )
    _adjudicate(tmp_path, ON, _claude_stream(10))
    warmer = _warmer(tmp_path, _launch(_claude_stream(11)), dirty=lambda: True)
    warmer.tick(work_pending=True)
    lines = warmer.finish()
    assert committed == []  # never beside a dirty trunk, not even at exit
    assert lines == ["keep-warm: session log not recorded (the trunk is dirty)"]
    assert "the trunk is dirty" in capsys.readouterr().err
    assert not (tmp_path / "docs" / "iteration").exists()


def test_a_raising_launch_under_a_held_store_lock_still_retires_its_session(
    tmp_path,
):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    kept = _keep(tmp_path, ON)
    sid = kept.session_id
    assert sid

    def broken(*a, **k):
        raise RuntimeError("launch broke")

    with keep.store_lock(tmp_path):  # another holder keeps the lock throughout
        with pytest.raises(RuntimeError):
            svc.act(_call(tmp_path, "ANTHROPIC", kept, broken))
        assert _state(tmp_path)["state"] == "active"  # the record was unreachable
    # The tombstone it left is honoured by the next launch and by keep-warm.
    assert keep.due_routes(tmp_path, ON, 10**10, True) == []
    nxt = _keep(tmp_path, ON)
    assert nxt.session_id == ""  # the next launch mints
    assert _state(tmp_path)["state"] == "retired"
    assert _state(tmp_path)["reset_reason"] == "session unusable"
    assert not list(keep.store_dir(tmp_path).glob("*.retire"))


def test_the_warmer_reads_the_trunk_through_the_shared_dirty_check(tmp_path):
    import subprocess

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    _adjudicate(tmp_path, ON, _claude_stream(10))
    (tmp_path / "work.py").write_text("x = 1\n", encoding="utf-8")  # substantive
    warmer = svc.KeepWarmer(
        tmp_path,
        ON,
        {"ANTHROPIC-ROUTE": _Row("ANTHROPIC")},
        runner=_launch(_claude_stream(11)),
        clock=lambda: 10**10,
    )
    warmer.tick(work_pending=True)
    warmer.thread.join(10)
    assert warmer.tick(work_pending=False) == [
        "keep-warm: session log held (the trunk is dirty)"
    ]


def test_an_expired_unreleased_lease_retires_the_session_rather_than_reusing_it(
    tmp_path, monkeypatch
):
    """The interleaving: an adjudication holds the session and is still
    running when its lease expires (a retained launch has no wall of its own
    beyond the lease). The next keep_for must not resume that session: an
    expired lease that was never released means its holder is still running
    or crashed, so the session is retired and the launch mints fresh."""
    _adjudicate(tmp_path, ON, _claude_stream(10))
    held = _keep(tmp_path, ON, lease_seconds=5)  # the long-running holder
    assert held.session_id
    later = keep.time.time() + 60
    monkeypatch.setattr(keep.time, "time", lambda: later)  # its lease expired
    nxt = _keep(tmp_path, ON)
    assert nxt is not None and nxt.session_id == ""  # never the held session
    assert _state(tmp_path)["state"] == "retired"
    assert _state(tmp_path)["reset_reason"] == "lease expired unreleased"
    assert _state(tmp_path)["lease"]["holder"] == nxt.holder


def _split_clock(monkeypatch, start):
    """A clock whose every read advances one second: two reads in one
    decision straddle a lease that ends half a second after the first."""
    reads = iter(range(10**6))
    monkeypatch.setattr(keep.time, "time", lambda: start + next(reads))
    monkeypatch.setattr(keep.time, "sleep", lambda s: None)


def _lease_to_other(tmp_path, until):
    with keep.store_lock(tmp_path):
        record = keep.store_load(tmp_path, "ANTHROPIC", "ANTHROPIC-ROUTE")
        record["lease"] = {"holder": "adjudicate:other", "until": until}
        keep.store_save(tmp_path, record)
    return record["session_id"]


def test_keep_for_reads_one_clock_per_decision_and_never_resumes_a_stale_lease(
    tmp_path, monkeypatch
):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    start = keep.time.time()
    held = _lease_to_other(tmp_path, start + 0.5)
    _split_clock(monkeypatch, start)
    nxt = _keep(tmp_path, ON, lease_wait=30)
    assert nxt is not None and nxt.session_id == ""  # minted, never `held`
    assert nxt.session_id != held
    assert _state(tmp_path)["state"] == "retired"
    assert _state(tmp_path)["reset_reason"] == "lease expired unreleased"


def test_take_warm_lease_reads_one_clock_per_decision(tmp_path, monkeypatch):
    _adjudicate(tmp_path, ON, _claude_stream(10))
    start = keep.time.time()
    _lease_to_other(tmp_path, start + 0.5)
    _split_clock(monkeypatch, start)
    ping, reason = keep.take_warm_lease(
        tmp_path, ON, now=10**10, work_pending=True, holder="keep-warm:x"
    )
    assert ping is None  # the session is never leased to the ping
    assert _state(tmp_path)["lease"]["holder"] != "keep-warm:x"
