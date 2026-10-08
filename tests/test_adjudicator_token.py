"""The retained Claude home's long-lived token, and an auth failure that keeps the session.

WI-846. The retained adjudicator's dedicated Claude home authenticates with
the owner's long-lived token (`claude setup-token`). The token FILE's path is
read at each retained launch from a declared environment variable (OI-110
(b), 2026-10-08: nothing about the path is tracked), and the token reaches
the CLI only through the variable the CLI reads it from. An unset variable, or
a missing, unreadable or empty token file, is refused before launch naming
dev-setup; nothing falls back to OAuth. An authentication failure on a
launched call records the call failed and leaves the session's record as it
was.

No test reads a real token file: every token here is a canary in a temporary
file, and `tests/conftest.py` removes the declared variable from every test's
environment. The canary is asserted absent from every log, record, argv and
printed line the code writes.
"""

import json
import os
import sys

import pytest

import test_coordinator_adjudicate as coord
import test_session_keep as sk

CANARY = "sk-ant-oat01-CANARY-846-never-logged"  # a fake token shaped like a real one; privacy-ok
TOKEN_FILE = "AGENT_CLAUDE_TOKEN_FILE"


# Every retained launch here prepares with a resolvable runner (WI-846).
pytestmark = pytest.mark.usefixtures("retained_runners")


def _token_file(tmp_path, monkeypatch, text=CANARY):
    path = tmp_path / "outside" / "claude-token"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    monkeypatch.setenv(TOKEN_FILE, str(path))
    return path


def _auth_failed_stream(sid="S"):
    """The shape claude 2.1.289 writes when the API refuses the credential:
    a synthetic assistant event tagged `authentication_failed`, then an error
    result (the recorded 2026-10-06 incident's shape, with its tag)."""
    return "\n".join(
        [
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"model": "<synthetic>", "content": []},
                    "session_id": sid,
                    "error": "authentication_failed",
                    "is_api_error_message": True,
                }
            ),
            json.dumps(
                {
                    "type": "result",
                    "is_error": True,
                    "result": "Failed to authenticate.",
                    "session_id": sid,
                    "usage": {"input_tokens": 0, "output_tokens": 0},
                }
            ),
        ]
    )


def _files_text(*roots):
    """Every file's bytes under `roots`, decoded loosely, for a canary scan."""
    texts = []
    for root in roots:
        for path in root.rglob("*"):
            if path.is_file() and "outside" not in path.parts:
                texts.append(path.read_bytes().decode("utf-8", "replace"))
    return "\n".join(texts)


# --- the token at launch -----------------------------------------------------------


def test_the_token_is_read_at_launch_and_never_logged(tmp_path, monkeypatch, capsys):
    seen = {"argv": [], "env": []}

    def run(argv, root, timeout, **kw):
        seen["argv"].append(list(argv))
        seen["env"].append(kw.get("env"))
        coord.VERDICT["path"].write_text(
            "VERDICT: MEANING rows=SR-1\n", encoding="utf-8"
        )
        return 0, coord._claude_stream(10), False

    monkeypatch.setattr(coord.svc, "run_session", run)
    monkeypatch.setattr(coord.svc, "cli_version", lambda *a, **k: "")
    commits = []
    monkeypatch.setattr(
        coord.svc.agent_common, "commit_telemetry", lambda *a, **k: commits.append(a)
    )
    root = coord._repo(tmp_path / "repo")
    _token_file(tmp_path, monkeypatch)
    assert coord._adjudicate(root) == 0
    assert coord._adjudicate(root) == 0  # the resume reads the token again
    assert [env["CLAUDE_CODE_OAUTH_TOKEN"] for env in seen["env"]] == [CANARY] * 2
    assert all(CANARY not in " ".join(argv) for argv in seen["argv"])
    printed = capsys.readouterr()
    assert CANARY not in printed.out + printed.err
    assert CANARY not in repr(commits)
    assert CANARY not in _files_text(tmp_path / "repo")  # logs, records, home
    assert coord._state(root)["state"] == "active"


@pytest.mark.parametrize("problem", ["unset", "missing", "unreadable", "empty"])
def test_a_token_that_cannot_be_read_refuses_before_launch(
    tmp_path, monkeypatch, capsys, problem
):
    launched = []
    monkeypatch.setattr(coord.svc, "run_session", lambda *a, **k: launched.append(a))
    monkeypatch.setattr(coord.svc, "cli_version", lambda *a, **k: "")
    root = coord._repo(tmp_path / "repo")
    if problem == "missing":
        monkeypatch.setenv(TOKEN_FILE, str(tmp_path / "no-such-token"))
    elif problem == "unreadable":
        monkeypatch.setenv(TOKEN_FILE, str(tmp_path))  # a directory
    elif problem == "empty":
        _token_file(tmp_path, monkeypatch, text="  ")
    assert coord._adjudicate(root) == coord.svc.agent_common.EXIT_NEEDS_HUMAN
    out = capsys.readouterr().out
    assert "dev-setup" in out and "setup-token" in out and TOKEN_FILE in out
    assert str(tmp_path) not in out  # the variable is named, never its path
    assert launched == []
    assert not (coord.keep.store_dir(root) / "home").exists()
    assert coord._state(root) is None  # no lease taken, nothing recorded


def test_the_claude_probe_reads_the_token_file_and_runs_nothing(tmp_path, monkeypatch):
    ran = []

    def probe(root):
        return coord.svc.signin_status(
            root, "ANTHROPIC", run=lambda argv, env: ran.append(argv)
        )

    assert probe(tmp_path) == "missing"  # unset reads as not signed in
    monkeypatch.setenv(TOKEN_FILE, str(tmp_path / "absent"))
    assert probe(tmp_path) == "missing"
    _token_file(tmp_path, monkeypatch)
    assert probe(tmp_path) == "signed-in"  # no home needed: the token is all
    assert ran == []  # no status command, no model call
    assert not coord.keep.store_dir(tmp_path).exists()  # nothing created


def test_a_keep_warm_ping_passes_the_token_or_skips_and_keeps_the_session(
    tmp_path, monkeypatch
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    sk._adjudicate(tmp_path, sk.ON, sk._claude_stream(10))
    minted = sk._state(tmp_path)["session_id"]
    monkeypatch.delenv(TOKEN_FILE, raising=False)
    envs = []
    warmer = sk._warmer(tmp_path, sk._launch(sk._claude_stream(11), envs=envs))
    lines = warmer.tick(work_pending=True)
    assert len(lines) == 1 and "keep-warm: skipped" in lines[0]
    assert "dev-setup" in lines[0] and warmer.thread is None and envs == []
    record = sk._state(tmp_path)
    assert record["session_id"] == minted and record["state"] == "active"
    assert "lease" not in record  # released, nothing retired
    _token_file(tmp_path, monkeypatch)
    warmer.last_said = None
    assert warmer.tick(work_pending=True) == []
    warmer.thread.join(10)
    assert envs[0]["CLAUDE_CODE_OAUTH_TOKEN"] == CANARY


# --- an authentication failure keeps the session -------------------------------------


def test_an_auth_failure_records_the_call_failed_and_keeps_the_session(
    tmp_path, monkeypatch
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    sk._adjudicate(tmp_path, sk.ON, sk._claude_stream(10))
    before = sk._state(tmp_path)
    outcome = sk._adjudicate(
        tmp_path, sk.ON, _auth_failed_stream(before["session_id"]), wi="WI-2", code=1
    )
    assert not sk.svc.call_succeeded(outcome)  # recorded failed
    assert outcome.metrics["reset-reason"] == ""
    assert outcome.metrics["session-gen"] == before["generation"]
    assert sk._state(tmp_path) == before  # as it was: no retire, no WI-2
    assert sk._keep(tmp_path, sk.ON, wi="WI-3").session_id == before["session_id"]


def test_an_auth_failure_on_a_first_mint_leaves_no_record(tmp_path, monkeypatch):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    outcome = sk._adjudicate(tmp_path, sk.ON, _auth_failed_stream(), code=1)
    assert not sk.svc.call_succeeded(outcome)
    assert sk._state(tmp_path) is None  # the lease-only record is gone


def test_another_failure_still_retires_the_session(tmp_path, monkeypatch):
    """Only the CLI's `authentication_failed` tag keeps the session: the
    2026-10-06 OAuth-refresh failure was tagged `server_error`, and that, like
    any other failure, still retires it."""
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    sk._adjudicate(tmp_path, sk.ON, sk._claude_stream(10))
    stream = _auth_failed_stream().replace("authentication_failed", "server_error")
    sk._adjudicate(tmp_path, sk.ON, stream, code=1)
    assert sk._state(tmp_path)["state"] == "retired"
    assert sk.adapters.auth_failed(_auth_failed_stream())
    assert not sk.adapters.auth_failed(stream)


# --- round 2 (Sol r1): the token is the launch's one credential --------------------

# A canary with no credential shape, so only exact-value redaction removes it.
PLAIN = "plain-canary-846-no-known-shape"
COMPETING = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)


def _plan(tmp_path, monkeypatch, template=None, env=None):
    """Plan a retained keep; the route's row is `_registry`'s unless the test
    wrote its own."""
    if not (tmp_path / "docs" / "agents.toml").exists():
        _registry(tmp_path)
    monkeypatch.setattr(sk.svc, "cli_version", lambda *a, **k: "")
    return sk.svc.plan_keep(
        tmp_path,
        sk.ON,
        route=sk._route(tmp_path),
        role="ADJUDICATE",
        brief="disposition",
        wi="WI-1",
        lease_wait=0,
    )


def test_competing_ambient_credentials_never_reach_the_retained_launch(
    tmp_path, monkeypatch
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    for name in COMPETING:
        monkeypatch.setenv(name, "ambient-" + name)
    envs = []
    kept = _plan(tmp_path, monkeypatch)
    sk.svc.act(
        sk._call(
            tmp_path, "ANTHROPIC", kept, sk._launch(sk._claude_stream(10), envs=envs)
        )
    )
    assert envs[0]["CLAUDE_CODE_OAUTH_TOKEN"] == PLAIN
    assert not set(COMPETING) & set(envs[0])


@pytest.mark.parametrize(
    "declared", ["ANTHROPIC_API_KEY", "CLAUDE_CODE_USE_VERTEX", "--bare"]
)
def test_a_route_declaring_a_competing_credential_is_refused_before_launch(
    tmp_path, monkeypatch, declared
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    if declared == "--bare":  # the route's own registry row carries it
        _registry(tmp_path, template=sk.TEMPLATES["ANTHROPIC"] + " --bare")
    else:
        _registry(tmp_path, env=declared + "=declared-by-the-route")
    with pytest.raises(sk.svc.SigninRefused) as refused:
        _plan(tmp_path, monkeypatch)
    assert declared in str(refused.value) and "dev-setup" in str(refused.value)
    assert sk._state(tmp_path) is None  # no lease, nothing recorded


def test_an_echoed_token_is_redacted_from_every_sink(tmp_path, monkeypatch):
    monkeypatch.setattr(sk.svc.agent_common, "commit_telemetry", lambda *a, **k: None)
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    kept = _plan(tmp_path, monkeypatch)
    echoed = sk._claude_stream(10).replace(
        '"is_error": false', '"is_error": false, "result": "echo {}"'.format(PLAIN)
    )
    shown = []

    def run(argv, root, timeout, **kw):
        kw["on_line"]("live line echoing " + kw["env"]["CLAUDE_CODE_OAUTH_TOKEN"])
        return 0, echoed + "\nstderr: " + kw["env"]["CLAUDE_CODE_OAUTH_TOKEN"], False

    call = sk._call(tmp_path, "ANTHROPIC", kept, run)
    call.on_line = shown.append
    outcome = sk.svc.act(call)
    log = sk.svc.record(
        outcome,
        {"session": "s", "stamp": "x", "phase": "ADJUDICATE", "outcome": "COMPLETED"},
        raw_dir=tmp_path / "out" / "run-logs",
        raw_name="raw.log",
    )
    assert PLAIN in echoed  # the launch really echoed it
    assert shown and all(PLAIN not in line for line in shown)
    assert PLAIN not in outcome.text + outcome.stream + repr(outcome.metrics)
    assert PLAIN not in (tmp_path / "out" / "run-logs" / "raw.log").read_text(
        encoding="utf-8"
    )
    assert PLAIN not in log.read_text(encoding="utf-8")
    assert PLAIN not in _files_text(tmp_path)  # the record and the store too


# --- round 3 (Sol r2): one prepared launch, one name rule, one marker view --------

ROW = """[agent.ANTHROPIC-ROUTE]
family = "ANTHROPIC"
model = "m"
version = "1"
tier = "strong"
cmd_template = "{template}"
env = "{env}"
notes = "test row"
"""


def _registry(tmp_path, env="", template=None):
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "agents.toml").write_text(
        ROW.replace("{template}", template or sk.TEMPLATES["ANTHROPIC"]).replace(
            "{env}", env
        ),
        encoding="utf-8",
    )


def test_the_name_key_folds_case_on_windows_semantics_only(tmp_path, monkeypatch):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    _registry(tmp_path, env="Anthropic_Api_Key=declared")
    monkeypatch.setattr(sk.svc, "_CASE_INSENSITIVE", False)
    assert sk.svc._name_key("Anthropic_Api_Key") == "Anthropic_Api_Key"
    monkeypatch.setattr(sk.svc, "_CASE_INSENSITIVE", True)
    assert sk.svc._name_key("Anthropic_Api_Key") == "ANTHROPIC_API_KEY"
    with pytest.raises(sk.svc.SigninRefused) as refused:
        _plan(tmp_path, monkeypatch)
    assert "Anthropic_Api_Key" in str(refused.value)
    assert sk._state(tmp_path) is None
    prepared = sk.svc.Prepared(
        family="ANTHROPIC",
        template="t",
        model="m",
        tier="",
        executable="",
        declared={},
        credential={"T": "x"},
        home={},
    )
    composed = sk.svc.compose_env(
        {"anthropic_api_key": "ambient", "Path": "p"}, prepared
    )
    assert composed == {"Path": "p", "T": "x"}  # dropped by its folded name


def test_a_route_declaring_the_ambient_value_is_still_refused(tmp_path, monkeypatch):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "shared-config-value")
    _registry(tmp_path, env="ANTHROPIC_API_KEY=shared-config-value")
    with pytest.raises(sk.svc.SigninRefused) as refused:
        _plan(tmp_path, monkeypatch)
    assert "ANTHROPIC_API_KEY" in str(refused.value)
    assert sk._state(tmp_path) is None


def test_keep_warm_with_a_bare_route_is_refused_before_any_lease(tmp_path, monkeypatch):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    sk._adjudicate(tmp_path, sk.ON, sk._claude_stream(10))
    _registry(tmp_path, template=sk.TEMPLATES["ANTHROPIC"] + " --bare")
    seen = []
    warmer = sk.svc.KeepWarmer(
        tmp_path,
        sk.ON,
        {
            "ANTHROPIC-ROUTE": sk._Row(
                "ANTHROPIC", sk.TEMPLATES["ANTHROPIC"] + " --bare"
            )
        },
        runner=sk._launch(sk._claude_stream(11), seen=seen),
        clock=lambda: 10**10,
        dirty=lambda: False,
    )
    lines = warmer.tick(work_pending=True)
    assert len(lines) == 1 and "--bare" in lines[0] and "skipped" in lines[0]
    assert warmer.thread is None and seen == []
    record = sk._state(tmp_path)
    assert "lease" not in record and record["state"] == "active"
    marker = sk.keep._tombstone_path(tmp_path, "ANTHROPIC", "ANTHROPIC-ROUTE")
    assert not marker.exists()  # nothing to release: no lease was taken


# --- round 4 (Sol r3): one route snapshot through preparation and launch ---------


def test_a_keep_warm_ping_launches_one_route_snapshot(tmp_path, monkeypatch):
    """The warmer selected its routes from the row as it stood; the row on
    disk then changed its model and its declared endpoint. The ping launches
    the row the warmer SELECTED, whole: its model with its endpoint, never a
    mix with the changed row."""
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    _registry(tmp_path, env="ANTHROPIC_BASE_URL=https://old.invalid")
    sk._adjudicate(tmp_path, sk.ON, sk._claude_stream(10))
    seen, envs = [], []
    selected = sk.svc.agent_route.load_registry(tmp_path / "docs" / "agents.toml")[0]
    warmer = sk.svc.KeepWarmer(
        tmp_path,
        sk.ON,
        selected,
        runner=sk._launch(sk._claude_stream(11), seen=seen, envs=envs),
        clock=lambda: 10**10,
        dirty=lambda: False,
    )
    row = (
        ROW.replace("{template}", sk.TEMPLATES["ANTHROPIC"])
        .replace("{env}", "ANTHROPIC_BASE_URL=https://new.invalid")
        .replace('model = "m"', 'model = "new-model"')
    )
    (tmp_path / "docs" / "agents.toml").write_text(row, encoding="utf-8")
    assert warmer.tick(work_pending=True) == []
    warmer.thread.join(10)
    argv = seen[0]
    assert argv[argv.index("--model") + 1] == "m"
    assert envs[0]["ANTHROPIC_BASE_URL"] == "https://old.invalid"


def test_a_retained_call_launches_its_prepared_route_not_the_callers(
    tmp_path, monkeypatch
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    _registry(tmp_path)
    kept = sk._keep(tmp_path, sk.ON)
    seen = []
    call = sk._call(
        tmp_path, "ANTHROPIC", kept, sk._launch(sk._claude_stream(10), seen=seen)
    )
    call.template = "claude -p --model {model} --stale-template"
    call.model = "stale-model"
    outcome = sk.svc.act(call)
    assert "--stale-template" not in seen[0]
    assert seen[0][seen[0].index("--model") + 1] == "m"
    assert outcome.metrics["gen_ai.request.model"] == "m"


# --- round 5 (Sol r4): the SELECTED row is the one snapshot -----------------------


def _selected(tmp_path, monkeypatch, row_text):
    """A loop context whose registry is the snapshot the loop selected from
    (`row_text`), on a root with the retention dial on and a token."""
    from types import SimpleNamespace

    _token_file(tmp_path, monkeypatch, text=PLAIN)
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "process.toml").write_text(
        "[adjudicator]\ncontext_reset_pct = 50\n", encoding="utf-8"
    )
    (docs / "agents.toml").write_text(row_text, encoding="utf-8")
    registry = sk.svc.agent_route.load_registry(docs / "agents.toml")[0]
    ctx = SimpleNamespace(
        root=tmp_path,
        prompt_templates={},
        args=SimpleNamespace(session_timeout=60),
        registry=registry,
    )
    plan = {
        "phase": "ADJUDICATE",
        "brief": "disposition",
        "route_family": "ANTHROPIC",
        "route_id": "ANTHROPIC-ROUTE",
        "tmpl": sk.TEMPLATES["ANTHROPIC"],
        "session_env": None,
    }
    return ctx, plan


def _row_text(model="m", env="", family="ANTHROPIC"):
    return (
        ROW.replace("{template}", sk.TEMPLATES["ANTHROPIC"])
        .replace("{env}", env)
        .replace('model = "m"', 'model = "{}"'.format(model))
        .replace('family = "ANTHROPIC"', 'family = "{}"'.format(family))
    )


def test_a_row_changed_after_selection_launches_the_selected_row(tmp_path, monkeypatch):
    al = load_agent_loop()
    monkeypatch.setattr(al.session_service, "cli_version", lambda *a, **k: "")
    ctx, plan = _selected(tmp_path, monkeypatch, _row_text(model="selected"))
    (tmp_path / "docs" / "agents.toml").write_text(
        _row_text(model="changed", env="ANTHROPIC_BASE_URL=https://changed.invalid"),
        encoding="utf-8",
    )
    kept = al.adjudication_keep(ctx, plan, "WI-1")
    seen, envs = [], []
    call = al.session_service.Call(
        root=tmp_path,
        role="ADJUDICATE",
        template=plan["tmpl"],
        model="selected",
        prompt="judge",
        provider="ANTHROPIC",
        route_id="ANTHROPIC-ROUTE",
        keep=kept,
        runner=sk._launch(sk._claude_stream(10), seen=seen, envs=envs),
    )
    al.session_service.act(call)
    assert seen[0][seen[0].index("--model") + 1] == "selected"
    assert "ANTHROPIC_BASE_URL" not in (envs[0] or {})


def test_the_version_probe_runs_under_the_prepared_environment(tmp_path, monkeypatch):
    al = load_agent_loop()
    probed = []
    monkeypatch.setattr(
        al.session_service,
        "cli_version",
        lambda prepared: probed.append(al.session_service.probe_env(prepared)) or "",
    )
    ctx, plan = _selected(
        tmp_path, monkeypatch, _row_text(env="ANTHROPIC_BASE_URL=https://row.invalid")
    )
    monkeypatch.setenv("ANTHROPIC_API_KEY", "ambient-key")
    plan["session_env"] = {"CALLER_ONLY": "1"}
    al.adjudication_keep(ctx, plan, "WI-1")
    env = probed[0]
    assert "CLAUDE_CODE_OAUTH_TOKEN" not in env  # the launch's credential only
    assert env["ANTHROPIC_BASE_URL"] == "https://row.invalid"
    assert "ANTHROPIC_API_KEY" not in env and "CALLER_ONLY" not in env


def test_keep_warm_never_warms_a_record_of_another_family(tmp_path, monkeypatch):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    sk._adjudicate(tmp_path, sk.ON, sk._claude_stream(10))  # an ANTHROPIC session
    _registry(tmp_path)
    (tmp_path / "docs" / "agents.toml").write_text(
        _row_text(family="OPENAI"), encoding="utf-8"
    )
    row = sk._Row("ANTHROPIC")
    row.family = "OPENAI"  # the route now names another family, same runner
    seen = []
    warmer = sk.svc.KeepWarmer(
        tmp_path,
        sk.ON,
        {"ANTHROPIC-ROUTE": row},
        runner=sk._launch(sk._claude_stream(11), seen=seen),
        clock=lambda: 10**10,
        dirty=lambda: False,
    )
    lines = warmer.tick(work_pending=True)
    assert len(lines) == 1 and "skipped" in lines[0] and "OPENAI" in lines[0]
    assert seen == [] and warmer.thread is None
    assert "lease" not in sk._state(tmp_path)  # skipped before any lease


# --- round 6 (Sol r5): the probe and the launch share one prepared executable -----


def _shim(directory, version, stream="", echo_variable=""):
    """A real `claude` runner in `directory`: `--version` prints `version`
    (then the value of `echo_variable`, when named), anything else prints a
    RUNNER marker and `stream`, so a test sees which runner each call ran."""
    directory.mkdir(parents=True, exist_ok=True)
    data = directory / "stream.jsonl"
    data.write_text("RUNNER-" + version + "\n" + stream + "\n", encoding="utf-8")
    if sys.platform == "win32":
        shim = directory / "claude.cmd"
        echoed = " %{}%".format(echo_variable) if echo_variable else ""
        shim.write_text(
            '@echo off\r\nif "%~1"=="--version" goto version\r\n'
            'type "{}"\r\nexit /b 0\r\n:version\r\necho {}{}\r\nexit /b 0\r\n'.format(
                data, version, echoed
            ),
            encoding="ascii",
        )
    else:
        shim = directory / "claude"
        echoed = ' "${}"'.format(echo_variable) if echo_variable else ""
        shim.write_text(
            '#!/bin/sh\nif [ "$1" = "--version" ]; then echo {}{}; exit 0; fi\n'
            'cat "{}"\n'.format(version, echoed, data),
            encoding="ascii",
        )
        shim.chmod(0o755)
    return shim


def _row_with_path(tmp_path, path):
    """The selected row declares its own PATH."""
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "agents.toml").write_text(
        _row_text().replace('env = ""', "env = " + json.dumps("PATH=" + path)),
        encoding="utf-8",
    )


def _plan_real(tmp_path, wi="WI-1"):
    """Plan a retained keep with the REAL version probe."""
    return sk.svc.plan_keep(
        tmp_path,
        sk.ON,
        route=sk._route(tmp_path),
        role="ADJUDICATE",
        brief="disposition",
        wi=wi,
        lease_wait=0,
    )


def test_the_probe_and_the_launch_run_the_one_prepared_executable(
    tmp_path, monkeypatch
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    ambient = os.environ.get("PATH", "")
    _shim(tmp_path / "old", "old")
    new = _shim(tmp_path / "new", "new", sk._claude_stream(10, sid="PATH-S"))
    _shim(tmp_path / "other", "other")
    monkeypatch.setenv("PATH", str(tmp_path / "old") + os.pathsep + ambient)
    _row_with_path(tmp_path, str(tmp_path / "new") + os.pathsep + ambient)
    kept = _plan_real(tmp_path)
    assert kept.cli_version == "new"  # the selected row's runner, not ambient's
    assert os.path.normcase(kept.prepared.executable) == os.path.normcase(str(new))
    outcome = sk.svc.act(sk._call(tmp_path, "ANTHROPIC", kept, sk.svc.run_session))
    assert "RUNNER-new" in outcome.stream and "RUNNER-old" not in outcome.stream
    assert sk._state(tmp_path)["cli_version"] == "new"
    minted = sk._state(tmp_path)["session_id"]
    # Changing only the ambient PATH changes neither call's runner.
    monkeypatch.setenv("PATH", str(tmp_path / "other") + os.pathsep + ambient)
    nxt = _plan_real(tmp_path, wi="WI-2")
    assert nxt.cli_version == "new" and nxt.session_id == minted != ""
    assert sk._state(tmp_path)["state"] == "active"
    sk.keep.keep_release(tmp_path, nxt)


def test_the_version_probe_never_receives_the_credential(tmp_path, monkeypatch):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "ambient-" + PLAIN)
    ambient = os.environ.get("PATH", "")
    _shim(tmp_path / "echo", "v1", echo_variable="CLAUDE_CODE_OAUTH_TOKEN")
    _row_with_path(tmp_path, str(tmp_path / "echo") + os.pathsep + ambient)
    real_run, probed = sk.svc.subprocess.run, []

    def spy(argv, **kw):
        if argv[-1] == "--version":
            probed.append(kw["env"])
        return real_run(argv, **kw)

    monkeypatch.setattr(sk.svc.subprocess, "run", spy)
    kept = _plan_real(tmp_path)
    monkeypatch.setattr(sk.svc.subprocess, "run", real_run)
    assert len(probed) == 1 and probed[0] is not None
    keys = {sk.svc._name_key(k) for k in probed[0]}
    assert sk.svc._name_key("CLAUDE_CODE_OAUTH_TOKEN") not in keys
    assert kept.cli_version.startswith("v1") and PLAIN not in kept.cli_version
    envs = []
    sk.svc.act(
        sk._call(
            tmp_path, "ANTHROPIC", kept, sk._launch(sk._claude_stream(10), envs=envs)
        )
    )
    assert envs[0]["CLAUDE_CODE_OAUTH_TOKEN"] == PLAIN  # the launch still has it
    assert PLAIN not in sk._state(tmp_path)["cli_version"]
    assert PLAIN not in _files_text(tmp_path)


@pytest.mark.parametrize("declared", [False, True])
def test_a_runner_not_on_the_launch_path_is_refused_before_any_lease(
    tmp_path, monkeypatch, declared
):
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    template = sk.TEMPLATES["ANTHROPIC"].replace("claude", "no-such-runner-846", 1)
    _registry(tmp_path, template=template)
    if declared:  # the row declares a PATH that does not hold it
        _row_with_path(tmp_path, str(tmp_path / "empty"))
        (tmp_path / "docs" / "agents.toml").write_text(
            (tmp_path / "docs" / "agents.toml")
            .read_text(encoding="utf-8")
            .replace(sk.TEMPLATES["ANTHROPIC"], template),
            encoding="utf-8",
        )
    with pytest.raises(sk.svc.SigninRefused) as refused:
        _plan_real(tmp_path)
    message = str(refused.value)
    assert "no-such-runner-846" in message
    assert ("declared PATH" if declared else "ambient PATH") in message
    assert sk._state(tmp_path) is None  # no lease, nothing recorded


def test_the_runner_resolves_after_the_template_substitution(tmp_path, monkeypatch):
    """Sol r6 MAJOR 3: a `{model}` in the runner's own token is substituted
    exactly as the launch argv substitutes it before the runner resolves."""
    _token_file(tmp_path, monkeypatch, text=PLAIN)
    runner = _shim(tmp_path / "runners" / "m", "v1")
    template = sk.TEMPLATES["ANTHROPIC"].replace(
        "claude", (tmp_path / "runners").as_posix() + "/{model}/" + runner.name, 1
    )
    _registry(tmp_path, template=template)
    prepared = sk.svc.prepare_launch(tmp_path, sk._route(tmp_path))
    assert os.path.normcase(prepared.executable) == os.path.normcase(str(runner))


def load_agent_loop():
    from conftest import load_script

    return load_script("agent_loop")
