"""The session service's keep operation: adjudicator session retention.

Retention rides the service's act and record steps: resuming by id, reading
occupancy, draining and resetting, and the keep-warm ping are all ordinary
calls through `session_service`, and the layer is INERT at the shipped
`[adjudicator] context_reset_pct = 0`. The rules and the store are
`session_keep`'s. Driven in memory with an injected launch over the recorded
fixtures in `tests/golden/sessions/` (all three LIVE: the claude one
recorded 2026-09-28, the codex and opencode ones 2026-09-30, WI-541). The store lives under a temporary repository root.
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


def test_the_shipped_dial_is_off_and_this_repo_shares_its_structure():
    """The template ships the dial off; this repo's VALUE may diverge (it is
    on at 55 since WI-835, owner ruling (b)) while its keys stay the same."""
    live = tomllib.loads((ROOT / "docs" / "process.toml").read_text(encoding="utf-8"))
    kit = (ROOT / "project-trajectory" / "process.toml.template").read_text(
        encoding="utf-8"
    )
    template = tomllib.loads(kit)
    assert template["adjudicator"]["context_reset_pct"] == 0
    assert live["adjudicator"]["context_reset_pct"] == 55
    assert set(live["adjudicator"]) == set(template["adjudicator"])
    # And retains first approvals too (owner, 2026-10-05,
    # docs/decisions/wi-835.toml#D-007); the template's list is unchanged.
    assert keep.keep_config(ROOT) == keep.KeepConfig(
        context_reset_pct=55,
        retain_for=("disposition", "amendment", "red-tc", "first-approval"),
    )


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


# --- dial on: resume and occupancy per provider (TC-267) -----------------------


@pytest.mark.parametrize(
    "family,session_id,used",
    [
        ("ANTHROPIC", None, 48267),
        ("OPENAI", "01a0f5b5-ff52-73c1-b233-c11dd3defd4d", ""),
        ("OPENCODE", "ses_f0a498817ffe2U5tfcBE7s7Q2I", 10787),
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
    thread = "01a0f5b5-ff52-73c1-b233-c11dd3defd4d"
    kept = _keep(tmp_path, ON, "OPENAI")
    home = Path(kept.home_env["CODEX_HOME"])
    assert home.is_dir() and home.parent.parent == keep.store_dir(tmp_path)
    day = home / "sessions" / "2026" / "09" / "30"
    day.mkdir(parents=True)
    (day / "rollout-2026-09-30T23-25-40-{}.jsonl".format(thread)).write_text(
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
    assert out.metrics["context-used"] == 15224
    assert keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")["pct"] == 6


def test_an_unretained_codex_call_reads_occupancy_under_the_inherited_home(
    tmp_path, monkeypatch
):
    thread = "01a0f5b5-ff52-73c1-b233-c11dd3defd4d"
    day = tmp_path / "home" / "sessions" / "2026"
    day.mkdir(parents=True)
    (day / "rollout-x-{}.jsonl".format(thread)).write_text(
        _fixture("codex-rollout.jsonl"), encoding="utf-8"
    )
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "home"))
    out = svc.act(_call(tmp_path, "OPENAI", None, _launch(_fixture(STREAMS["OPENAI"]))))
    assert out.metrics["context-used"] == 15224  # env=None inherits CODEX_HOME


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
    monkeypatch.setattr(svc, "signin_status", lambda root, family: "signed-in")
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
    monkeypatch.setattr(
        al.session_service, "signin_status", lambda root, family: "signed-in"
    )
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


# --- a route's first mint takes the lease (TC-329) --------------------------------


def _first_calls(tmp_path, count=2):
    """`count` first calls on one route, released together, each meeting
    the store with no record; the keeps they got, in finishing order."""
    gate, kept = threading.Barrier(count), []

    def first():
        gate.wait()
        kept.append(_keep(tmp_path, ON, lease_wait=0))

    threads = [threading.Thread(target=first) for _ in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(30)
    return kept


def test_two_concurrent_first_calls_mint_one_session_and_run_one_unretained(
    tmp_path, capsys
):
    kept = _first_calls(tmp_path)
    minting = [k for k in kept if k is not None]
    assert len(kept) == 2 and len(minting) == 1  # one mints, one is refused
    assert minting[0].session_id == ""
    lease_only = _state(tmp_path)
    assert lease_only["lease"]["holder"] == minting[0].holder
    assert "session_id" not in lease_only and "state" not in lease_only
    assert "runs unretained" in capsys.readouterr().err
    seen = []
    svc.act(_call(tmp_path, "ANTHROPIC", None, _launch(_claude_stream(10))))
    svc.act(
        _call(tmp_path, "ANTHROPIC", minting[0], _launch(_claude_stream(10), seen=seen))
    )
    record = _state(tmp_path)
    minted = seen[0][seen[0].index("--session-id") + 1]
    assert record["session_id"] == minted and record["generation"] == 1
    assert record["state"] == "active" and "lease" not in record


def test_a_crashed_first_calls_lease_expires_and_is_retired(tmp_path, monkeypatch):
    crashed = _keep(tmp_path, ON, lease_seconds=5)  # minted, never bookkept
    assert crashed is not None and crashed.session_id == ""
    assert _keep(tmp_path, ON) is None  # its lease holds while it is live
    later = keep.time.time() + 60
    monkeypatch.setattr(keep.time, "time", lambda: later)  # the lease expired
    nxt = _keep(tmp_path, ON)
    assert nxt is not None and nxt.session_id == ""  # the next call mints
    assert _state(tmp_path)["state"] == "retired"
    assert _state(tmp_path)["reset_reason"] == "lease expired unreleased"
    assert _state(tmp_path)["lease"]["holder"] == nxt.holder
    # The overrunning first call finishing late lands on nothing of its own.
    late = svc.act(_call(tmp_path, "ANTHROPIC", crashed, _launch(_claude_stream(10))))
    assert late.metrics["reset-reason"] == "store moved on"
    assert _state(tmp_path)["lease"]["holder"] == nxt.holder


def test_a_late_first_mint_never_replaces_the_session_that_took_its_lease_over(
    tmp_path, monkeypatch
):
    crashed = _keep(tmp_path, ON, lease_seconds=5)  # minted, never bookkept
    later = keep.time.time() + 60
    monkeypatch.setattr(keep.time, "time", lambda: later)  # the lease expired
    svc.act(
        _call(tmp_path, "ANTHROPIC", _keep(tmp_path, ON), _launch(_claude_stream(10)))
    )
    replacement = _state(tmp_path)
    assert replacement["state"] == "active" and "lease" not in replacement
    # The overrunning first call finishes after the replacement released.
    late = svc.act(_call(tmp_path, "ANTHROPIC", crashed, _launch(_claude_stream(10))))
    assert late.metrics["reset-reason"] == "store moved on"
    assert _state(tmp_path) == replacement  # generation 1, its session kept


def test_a_first_mint_that_raises_removes_its_lease_only_record(tmp_path):
    kept = _keep(tmp_path, ON)
    assert _state(tmp_path)["lease"]["holder"] == kept.holder

    def broken(*a, **k):
        raise RuntimeError("launch broke")

    with pytest.raises(RuntimeError):
        svc.act(_call(tmp_path, "ANTHROPIC", kept, broken))
    assert _state(tmp_path) is None
    assert not list(keep.store_dir(tmp_path).glob("*.json"))
    assert not list(keep.store_dir(tmp_path).glob("*.retire"))
    assert _keep(tmp_path, ON) is not None  # the route is free again


def test_at_dial_zero_a_first_call_writes_no_lease(tmp_path):
    assert _keep(tmp_path, keep.KeepConfig()) is None
    assert not keep.store_dir(tmp_path).exists()


# --- keep-warm (TC-268) -------------------------------------------------------------


class _Row:
    def __init__(self, family, cmd_template=None):
        self.id = family + "-ROUTE"
        self.family = family
        self.model = "m"
        self.tier = "strong"
        self.cmd_template = cmd_template or TEMPLATES[family]
        self.env = ""


def test_keep_warmer_excludes_a_route_whose_argv_is_refused(tmp_path, monkeypatch):
    def refuse_prompt_transport(argv, stdin_input):
        if argv[0] == "gemini":
            raise ValueError("prompt-in-argv refused")

    monkeypatch.setattr(
        svc.agent_session, "_validate_prompt_transport", refuse_prompt_transport
    )
    warmer = svc.KeepWarmer(
        tmp_path,
        ON,
        {
            "GEMINI-ROUTE": _Row("GEMINI", "gemini -p {prompt}"),
            "ANTHROPIC-ROUTE": _Row("ANTHROPIC"),
        },
    )
    assert isinstance(warmer, svc.KeepWarmer)
    assert "GEMINI-ROUTE" not in warmer.routes
    assert "ANTHROPIC-ROUTE" in warmer.routes


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
    assert svc.route_env(row)["CLAUDE_CODE_EFFORT_LEVEL"] == "high"


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


# TC-303: inline variants of recorded events, not additional live recordings.
def _codex_total(total, thread=None):
    events = [json.loads(ln) for ln in _fixture("codex-exec-json.jsonl").splitlines()]
    events[-1]["usage"]["input_tokens"] = total
    if thread:
        events[0]["thread_id"] = thread
    return "\n".join(json.dumps(e) for e in events)


def _codex_turn(root, total, cfg=ON, thread=None):
    retained = _keep(root, cfg, family="OPENAI")
    return svc.act(
        _call(root, "OPENAI", retained, _launch(_codex_total(total, thread)))
    )


def test_codex_rollout_prompt_drop_labels_inference(tmp_path, monkeypatch):
    prompts = []
    for total, prompt in ((15489, 15489), (35911, 20422), (71822, 35911)):
        prompts.append(prompt)
        _codex_rollout(tmp_path, prompts)
        out = _codex_turn(tmp_path, total)
        assert out.metrics["compacted"] is False
    _codex_rollout(tmp_path, prompts + [15717])
    out = _codex_turn(tmp_path, 87539)
    assert out.metrics["compacted"] is True
    assert out.metrics["compaction-source"] == "inferred"
    record = keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")
    assert record["compacted"] is True
    assert record["request_prompt"] == 15717
    monkeypatch.setattr(common, "commit_telemetry", lambda *a, **k: None)
    path = svc.record(out, {"session": "compaction", "stamp": "now"})
    text = path.read_text(encoding="utf-8")
    assert "compacted: True" in text
    assert "compaction-source: inferred" in text


def test_codex_reported_rollout_compaction_takes_precedence(tmp_path):
    retained = _keep(tmp_path, ON, family="OPENAI")
    home = Path(retained.home_env["CODEX_HOME"])
    thread = json.loads(_fixture("codex-exec-json.jsonl").splitlines()[0])["thread_id"]
    rollout = _fixture("codex-rollout.jsonl")
    # The fixture lacks compacted: inline envelope variant with the observed
    # WI-541 compacted/replacement_history shape; not a live recording.
    entry = json.loads(rollout.splitlines()[0])
    entry.update(type="compacted", payload={"replacement_history": []})
    day = home / "sessions"
    day.mkdir(parents=True, exist_ok=True)
    (day / f"rollout-test-{thread}.jsonl").write_text(
        rollout + json.dumps(entry) + "\n", encoding="utf-8"
    )
    out = svc.act(_call(tmp_path, "OPENAI", retained, _launch(_codex_total(30378))))
    assert out.metrics["compacted"] is True
    assert out.metrics["compaction-source"] == "reported"
    assert (
        keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")["compaction_source"]
        == "reported"
    )


def test_codex_inferred_compaction_holds_on_later_rising_requests(tmp_path):
    _codex_rollout(tmp_path, [35911])
    _codex_turn(tmp_path, 35911)
    _codex_rollout(tmp_path, [35911, 15717])
    out = _codex_turn(tmp_path, 51628)
    assert out.metrics["compaction-source"] == "inferred"
    _codex_rollout(tmp_path, [35911, 15717, 18000])
    out = _codex_turn(tmp_path, 69628)
    assert out.metrics["compacted"] is True
    assert out.metrics["compaction-source"] == "inferred"


def test_codex_reported_replaces_inferred_and_holds_on_new_drop(tmp_path):
    _codex_rollout(tmp_path, [35911])
    _codex_turn(tmp_path, 35911)
    _codex_rollout(tmp_path, [35911, 15717])
    out = _codex_turn(tmp_path, 51628)
    assert out.metrics["compaction-source"] == "inferred"
    _codex_rollout(tmp_path, [35911, 15717])
    retained = _keep(tmp_path, ON, family="OPENAI")
    home = Path(retained.home_env["CODEX_HOME"]) / "sessions"
    thread = json.loads(_fixture("codex-exec-json.jsonl").splitlines()[0])["thread_id"]
    rollout = home / f"rollout-test-{thread}.jsonl"
    entry = json.loads(_fixture("codex-rollout.jsonl").splitlines()[0])
    entry.update(type="compacted", payload={"replacement_history": []})
    rollout.write_text(
        rollout.read_text(encoding="utf-8") + "\n" + json.dumps(entry) + "\n",
        encoding="utf-8",
    )
    out = svc.act(_call(tmp_path, "OPENAI", retained, _launch(_codex_total(51628))))
    assert out.metrics["compacted"] is True
    assert out.metrics["compaction-source"] == "reported"
    record = keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")
    assert record["compaction_source"] == "reported"
    assert record["rollout_requests"] == 2
    assert record["request_prompt"] == 15717
    # Rewrite without the old compacted entry: only the stored source can win
    # over this new drop beyond the cursor, not a re-read reported observation.
    _codex_rollout(tmp_path, [35911, 15717, 10000])
    out = _codex_turn(tmp_path, 61628)
    assert out.metrics["compacted"] is True
    assert out.metrics["compaction-source"] == "reported"
    record = keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")
    assert record["compaction_source"] == "reported"
    assert record["rollout_requests"] == 3
    assert record["request_prompt"] == 10000


def test_codex_kit_reset_discards_prompt_comparison(tmp_path):
    cfg = keep.KeepConfig(context_reset_pct=50, reset_on_same_artifact=True)
    _codex_rollout(tmp_path, [35911])
    _codex_turn(tmp_path, 35911, cfg)
    out = _codex_turn(tmp_path, 15717, cfg, thread="new-thread")
    assert out.metrics["session-gen"] == 2
    assert out.metrics["compacted"] is False
    assert out.metrics["compaction-source"] == ""


def test_codex_equal_prompt_is_not_compaction(tmp_path):
    _codex_rollout(tmp_path, [10000])
    _codex_turn(tmp_path, 10000)
    _codex_rollout(tmp_path, [10000, 10000])
    out = _codex_turn(tmp_path, 20000)
    assert out.metrics["compacted"] is False


def test_codex_rollout_request_drop_is_inferred_without_reported_entry(tmp_path):
    retained = _keep(tmp_path, ON, family="OPENAI")
    home = Path(retained.home_env["CODEX_HOME"]) / "sessions"
    home.mkdir(parents=True, exist_ok=True)
    events = [json.loads(ln) for ln in _fixture("codex-rollout.jsonl").splitlines()]
    requests = [e for e in events if e.get("payload", {}).get("type") == "token_count"]
    # Inline count variants: the recorded prompts grow rather than compact.
    requests[0]["payload"]["info"]["last_token_usage"]["input_tokens"] = 35911
    requests[-1]["payload"]["info"]["last_token_usage"]["input_tokens"] = 15717
    thread = json.loads(_fixture("codex-exec-json.jsonl").splitlines()[0])["thread_id"]
    (home / f"rollout-test-{thread}.jsonl").write_text(
        "\n".join(json.dumps(e) for e in events), encoding="utf-8"
    )
    out = svc.act(_call(tmp_path, "OPENAI", retained, _launch(_codex_total(87539))))
    assert out.metrics["compaction-source"] == "inferred"
    assert out.metrics["compacted"] is True


def test_codex_legacy_record_learns_running_total_before_inference(tmp_path):
    _codex_turn(tmp_path, 35911)
    record = keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")
    record.pop("input_total")
    record.pop("request_prompt")
    keep.store_save(tmp_path, record)
    out = _codex_turn(tmp_path, 51628)
    assert out.metrics["compacted"] is False
    assert keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")["request_prompt"] is None
    out = _codex_turn(tmp_path, 67345)
    assert out.metrics["compacted"] is False


def test_codex_unrelated_rollout_cannot_report_compaction(tmp_path):
    retained = _keep(tmp_path, ON, family="OPENAI")
    day = Path(retained.home_env["CODEX_HOME"]) / "sessions"
    day.mkdir(parents=True, exist_ok=True)
    entry = json.loads(_fixture("codex-rollout.jsonl").splitlines()[0])
    entry.update(type="compacted", payload={"replacement_history": []})
    (day / "rollout-test-other-thread.jsonl").write_text(
        json.dumps(entry), encoding="utf-8"
    )
    out = svc.act(_call(tmp_path, "OPENAI", retained, _launch(_codex_total(30378))))
    assert out.metrics["compacted"] is False


def test_codex_multiple_exec_totals_without_rollout_cannot_infer(tmp_path):
    retained = _keep(tmp_path, ON, family="OPENAI")
    stream = "\n".join(_codex_total(total) for total in (15489, 35911, 71822, 87539))
    out = svc.act(_call(tmp_path, "OPENAI", retained, _launch(stream)))
    assert out.metrics["compaction-source"] == ""


def _codex_rollout(root, prompts):
    # Inline token_count variants of the live rollout, in request order.
    retained = _keep(root, ON, family="OPENAI")
    home = Path(retained.home_env["CODEX_HOME"]) / "sessions"
    with keep.store_lock(root):
        record = keep.store_load(root, "OPENAI", "OPENAI-ROUTE")
        if record:
            record.pop("lease", None)
            keep.store_save(root, record)
    home.mkdir(parents=True, exist_ok=True)
    event = next(
        json.loads(line)
        for line in _fixture("codex-rollout.jsonl").splitlines()
        if json.loads(line).get("payload", {}).get("type") == "token_count"
    )
    thread = json.loads(_fixture("codex-exec-json.jsonl").splitlines()[0])["thread_id"]
    lines = []
    for prompt in prompts:
        event["payload"]["info"]["last_token_usage"]["input_tokens"] = prompt
        lines.append(json.dumps(event))
    (home / f"rollout-test-{thread}.jsonl").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def test_codex_multi_request_exec_turn_then_smaller_turn_cannot_infer(tmp_path):
    _codex_turn(tmp_path, 15154 + 15224)
    out = _codex_turn(tmp_path, 15154 + 15224 + 15717)
    assert out.metrics["compacted"] is False
    assert out.metrics["compaction-source"] == ""


@pytest.mark.parametrize("new", [[15717, 18200], [36000, 38000, 40000]])
def test_codex_scans_every_new_rollout_request_from_stored_baseline(tmp_path, new):
    _codex_rollout(tmp_path, [35911])
    _codex_turn(tmp_path, 35911)
    _codex_rollout(tmp_path, [35911] + new)
    out = _codex_turn(tmp_path, 35911 + sum(new))
    assert out.metrics["compacted"] is (new[0] < 35911)
    assert out.metrics["compaction-source"] == ("inferred" if new[0] < 35911 else "")
    assert (
        keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")["request_prompt"] == new[-1]
    )


def test_codex_legacy_rollout_learns_baseline_without_rechecking_old_drop(tmp_path):
    _codex_turn(tmp_path, 35911)
    _codex_rollout(tmp_path, [35911, 15717])
    out = _codex_turn(tmp_path, 51628)
    assert out.metrics["compacted"] is False
    record = keep.store_load(tmp_path, "OPENAI", "OPENAI-ROUTE")
    assert record["request_prompt"] == 15717
    assert record["rollout_requests"] == 2
    _codex_rollout(tmp_path, [35911, 15717, 18200, 20000])
    out = _codex_turn(tmp_path, 89828)
    assert out.metrics["compacted"] is False


def test_codex_context_and_compaction_receive_same_ambient_environment(
    tmp_path, monkeypatch
):
    seen = []
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "ambient"))
    monkeypatch.setattr(svc, "_launch_env", lambda call: None)
    monkeypatch.setattr(
        svc.session_adapters.CodexAdapter,
        "context",
        lambda self, stream, env, sid: seen.append(env) or (sid, "", "", ""),
    )
    monkeypatch.setattr(
        svc.session_adapters.CodexAdapter,
        "compaction",
        lambda self, stream, env, sid: seen.append(env) or {},
    )
    _codex_turn(tmp_path, 30378)
    assert seen[0] is seen[1]
    assert seen[1]["CODEX_HOME"] == str(tmp_path / "ambient")
