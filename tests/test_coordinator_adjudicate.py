"""The coordinator's adjudication route and the retained launch's sign-in rule.

The coordinator adjudicates through the same keep operation and the same
`out/adjudicator/` record as the loop (WI-835): one entry point composes the
shared adjudication request, the session service plans the keep, launches,
records the session log, and the entry point prints the verdict. A retained
launch whose dedicated CLI home is not signed in is refused before launch on
either route, naming dev-setup; nothing signs in automatically and nothing
falls back to a fresh session or the default home.

No test calls a real model or a real CLI login: the launch is
`session_service.run_session`, replaced in the module the entry point
imported, and the sign-in probe's status command is an injected runner. The
entry point runs only from a lane (a linked worktree on a branch holding a
claim), so its fixture is a temporary primary checkout with one lane worktree;
the store lives under that primary checkout.
"""

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from conftest import ROOT, load_script

cli = load_script("coordinator_adjudicate")
svc = cli.session_service


# Every retained launch here prepares with a resolvable runner (WI-846).
pytestmark = pytest.mark.usefixtures("retained_runners")
keep = svc.session_keep

ROUTE = "ANTHROPIC-OPUS-STRONG"
TEMPLATE = "claude -p --model {model} --output-format stream-json --verbose"
AGENTS = """[agent.ANTHROPIC-OPUS-STRONG]
family = "ANTHROPIC"
model = "claude-opus-5-5"
version = "5.5"
tier = "strong"
cmd_template = "{template}"
env = ""
notes = "test row"

[agent.ANTHROPIC-OFF]
family = "ANTHROPIC"
model = "claude-opus-5-5"
version = "5.5"
tier = "medium"
cmd_template = "{template}"
env = ""
notes = "a row the enable-list does not name"
"""


def _claude_stream(pct, window=1000000, sid="S"):
    used = pct * window // 100
    usage = {"input_tokens": used, "output_tokens": 1}
    return "\n".join(
        [
            json.dumps(
                {"type": "assistant", "message": {"model": "m", "usage": usage}}
            ),
            json.dumps(
                {
                    "type": "result",
                    "is_error": False,
                    "result": "judged",
                    "session_id": sid,
                    "usage": usage,
                    "modelUsage": {"m": {"contextWindow": window}},
                }
            ),
        ]
    )


def _git(where, *args):
    proc = subprocess.run(
        ["git", "-C", str(where), "-c", "user.name=t", "-c", "user.email=t@t"]
        + ["-c", "core.hooksPath=no-hooks", "-c", "core.autocrlf=false", *args],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def _lane(base, branch="wi-1"):
    """A primary checkout at `base/primary` and a linked worktree at
    `base/lane` on `branch`, whose committed tree claims WI-9 (the lane's
    own row, outside the chains the tests judge) under
    `docs/work/active/<branch>/`. Returns `(primary, lane)`."""
    primary, lane = base / "primary", base / "lane"
    primary.mkdir(parents=True)
    _git(primary, "init", "-b", "trunk")
    (primary / "README").write_text("x\n", encoding="utf-8")
    _git(primary, "add", "README")
    _git(primary, "commit", "-m", "base")
    _git(primary, "worktree", "add", "-b", branch, str(lane))
    claim = lane / "docs" / "work" / "active" / branch
    claim.mkdir(parents=True)
    (claim / "WI-9-test.md").write_text("+++\nid = 'WI-9'\n+++\n", encoding="utf-8")
    _git(lane, "add", "docs")
    _git(lane, "commit", "-m", "claim")
    return primary, lane


def _repo(tmp_path, dial=50, where="lane"):
    primary, lane = _lane(tmp_path)
    return _inputs(lane if where == "lane" else primary, dial)


def _inputs(tmp_path, dial=50):
    """Valid launch inputs under `tmp_path`: the policy, a registry with the
    route enabled, and a brief."""
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "process.toml").write_text(
        "[adjudicator]\ncontext_reset_pct = {}\n".format(dial), encoding="utf-8"
    )
    (docs / "agents.toml").write_text(
        AGENTS.replace("{template}", TEMPLATE), encoding="utf-8"
    )
    (docs / "agents-enabled").write_text(ROUTE + "\n", encoding="utf-8")
    (tmp_path / "brief.md").write_text("judge the amendment", encoding="utf-8")
    return tmp_path


@pytest.fixture
def launched(monkeypatch, tmp_path):
    """The launch and the telemetry commit replaced: each launch writes a
    valid amendment verdict and returns the queued stream (10% by default).
    The retained Claude home's long-lived token is a canary file outside the
    repository (WI-846; tests/test_adjudicator_token.py tests it)."""
    seen = {"argv": [], "env": [], "streams": []}
    token = tmp_path / "token" / "claude-token"
    token.parent.mkdir()
    token.write_text("canary-token", encoding="utf-8")
    monkeypatch.setenv(svc.TOKEN_VARIABLES["ANTHROPIC"][0], str(token))

    def run(argv, root, timeout, **kw):
        seen["argv"].append(list(argv))
        seen["env"].append(kw.get("env"))
        VERDICT["path"].write_text("VERDICT: MEANING rows=SR-1\n", encoding="utf-8")
        stream = seen["streams"].pop(0) if seen["streams"] else _claude_stream(10)
        return 0, stream, False

    monkeypatch.setattr(svc, "run_session", run)
    monkeypatch.setattr(svc, "cli_version", lambda *a, **k: "")
    monkeypatch.setattr(svc.agent_common, "commit_telemetry", lambda *a, **k: None)
    return seen


def _signed_in(monkeypatch, status="signed-in"):
    calls = []
    monkeypatch.setattr(
        svc, "signin_status", lambda root, family: calls.append(family) or status
    )
    return calls


# The verdict path of the call in flight: each call names a fresh one, as the
# entry point requires, and the injected launch writes there.
VERDICT = {"path": None, "n": 0}


def _verdict(root):
    VERDICT["n"] += 1
    VERDICT["path"] = Path(root) / "verdict-{}.md".format(VERDICT["n"])
    return VERDICT["path"]


def _adjudicate(root, wi="WI-1", *extra, brief="amendment"):
    verdict = _verdict(root)
    return cli.main(
        [
            "adjudicate",
            "--root",
            str(root),
            "--brief-file",
            str(root / "brief.md"),
            "--brief",
            brief,
            "--wi",
            wi,
            "--verdict",
            str(verdict),
            *extra,
        ]
    )


def _state(root):
    return keep.store_load(root, "ANTHROPIC", ROUTE)


# --- the coordinator route (TC-321) ---------------------------------------------


def test_a_second_coordinator_adjudication_resumes_the_first(
    tmp_path, monkeypatch, launched, capsys
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    assert _adjudicate(root) == 0
    assert _adjudicate(root, "WI-1") == 0
    first, second = launched["argv"]
    minted = first[first.index("--session-id") + 1]
    assert second[second.index("--resume") + 1] == minted
    record = _state(root)
    assert record["session_id"] == minted and record["generation"] == 1
    assert record["judged"] == ["WI-1"] and "lease" not in record
    # the retained launch runs under the dedicated home, in the primary store
    home = keep.store_dir(root) / "home" / "anthropic"
    assert launched["env"][0]["CLAUDE_CONFIG_DIR"] == str(home)
    out = capsys.readouterr().out
    assert "VERDICT: MEANING rows=SR-1" in out


def test_the_coordinator_route_writes_one_session_log_per_call(
    tmp_path, monkeypatch, launched
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    _adjudicate(root)
    logs = sorted((root / "docs" / "iteration").glob("*.log"))
    assert len(logs) == 1
    text = logs[0].read_text(encoding="utf-8")
    assert "# phase: ADJUDICATE" in text and "# wi: WI-1" in text
    assert "# session-gen: 1" in text


def test_a_session_at_the_dial_drains_and_retires_at_the_next_clear_point(
    tmp_path, monkeypatch, launched
):
    root = _repo(tmp_path, dial=50)
    _signed_in(monkeypatch)
    launched["streams"] += [_claude_stream(60), _claude_stream(10)]
    _adjudicate(root, "WI-1")
    assert _state(root)["state"] == "draining"
    # WI-1 continues the chain the draining session judged: it is resumed
    _adjudicate(root, "WI-1")
    assert "--resume" in launched["argv"][1]
    # WI-2 belongs to no chain it judged and nothing of its own is pending:
    # the clear point, so it retires and the launch mints generation 2
    _adjudicate(root, "WI-2")
    assert "--session-id" in launched["argv"][2]
    assert _state(root)["generation"] == 2 and _state(root)["state"] == "active"


def test_an_unknown_route_or_one_off_the_enable_list_is_refused(
    tmp_path, monkeypatch, launched, capsys
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    assert _adjudicate(root, "WI-1", "--route", "NO-SUCH-ROW") == 2
    assert _adjudicate(root, "WI-1", "--route", "ANTHROPIC-OFF") == 2
    assert launched["argv"] == []
    assert "agents-enabled" in capsys.readouterr().out


def test_a_missing_or_malformed_verdict_is_reported_and_fails(
    tmp_path, monkeypatch, launched, capsys
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)

    def run(argv, root_, timeout, **kw):
        VERDICT["path"].write_text("no machine line\n", encoding="utf-8")
        return 0, _claude_stream(10), False

    monkeypatch.setattr(svc, "run_session", run)
    assert _adjudicate(root) == 1
    assert "carries no `VERDICT:` machine line" in capsys.readouterr().out


# --- the loop's route composes the same request (TC-322) -------------------------


# The row the loop selected for PLAN's route (the loop's own registry).
LOOP_ROW = SimpleNamespace(
    id="ANTHROPIC-ROUTE",
    family="ANTHROPIC",
    model="claude-opus-5-5",
    tier="strong",
    cmd_template=TEMPLATE,
    env="X=1",
)


def _loop_ctx(root, templates=None, timeout=60):
    """A loop context whose registry, the snapshot the loop selects from,
    holds the repository's rows (when the root has them) and LOOP_ROW."""
    agents = Path(root) / "docs" / "agents.toml"
    registry = cli.agent_route.load_registry(agents)[0] if agents.exists() else {}
    return SimpleNamespace(
        root=root,
        prompt_templates=templates or {},
        args=SimpleNamespace(session_timeout=timeout),
        registry={**registry, LOOP_ROW.id: LOOP_ROW},
    )


PLAN = {
    "phase": "ADJUDICATE",
    "brief": "disposition",
    "route_family": "ANTHROPIC",
    "route_id": "ANTHROPIC-ROUTE",
    "tmpl": TEMPLATE,
    "session_env": {"X": "1"},
}


@pytest.mark.parametrize(
    "templates,timeout",
    [({}, 60), ({"ADJUDICATE-DISPOSITION": "an override"}, None)],
)
def test_the_loop_composes_the_same_keep_request_as_before(
    tmp_path, monkeypatch, templates, timeout
):
    """The pre-extraction composition, written out: the loop's request is
    unchanged by moving it into the shared step, except the template identity,
    which since round 4 covers every class the dial retains (the shipped
    default: amendment, disposition, red-tc), each by its override text when
    one is loaded, else its shipped path."""
    al = load_script("agent_loop")
    prompts = load_script("prompts")
    seen = []
    monkeypatch.setattr(
        al.session_service, "plan_keep", lambda root, cfg, **kw: seen.append(kw)
    )
    al.adjudication_keep(_loop_ctx(tmp_path, templates, timeout), PLAN, "WI-7")
    override = templates.get("ADJUDICATE-DISPOSITION")
    shipped = ["ADJUDICATE-AMENDMENT", "ADJUDICATE-DISPOSITION", "ADJUDICATE-RED-TC"]
    assert seen == [
        {
            "route": LOOP_ROW,  # the row the loop selected, carried whole
            "role": "ADJUDICATE",
            "brief": "disposition",
            "wi": "WI-7",
            "rows": {},
            "template_paths": [
                prompts.template_path(key)
                for key in shipped
                if not (override and key == "ADJUDICATE-DISPOSITION")
            ],
            "template_texts": [override] if override else [],
            "lease_seconds": (timeout or 7200) + 300,
        }
    ]


def test_the_identity_covers_each_class_and_nothing_for_a_class_without_a_template():
    """Pins the no-template clause: a brief class with no template adds
    neither a path nor a text; each other class adds its override text when
    one is wired, else its shipped path."""
    ab = cli.adjudicate_brief
    assert ab.governing_templates(["no-such-class"]) == ([], [])
    assert ab.governing_templates([]) == ([], [])
    paths, texts = ab.governing_templates(
        ["red-tc", "no-such-class", "amendment"],
        {"ADJUDICATE-RED-TC": "an override"},
    )
    assert paths == [ab.prompts.template_path("ADJUDICATE-AMENDMENT")]
    assert texts == ["an override"]


# --- the sign-in probe (TC-323) ----------------------------------------------------


def _home(root, family):
    home = keep.store_dir(root) / "home" / family.lower()
    home.mkdir(parents=True)
    return home


@pytest.mark.parametrize(
    "family,code,text,expected",
    [
        ("OPENAI", 0, "Logged in using ChatGPT\n", "signed-in"),
        (
            "OPENAI",
            1,
            "WARNING: proceeding, even though we could not create PATH aliases:"
            " x\nNot logged in\n",
            "missing",
        ),
        ("OPENAI", 2, "error: unrecognized subcommand 'status'\n", "unknown"),
    ],
)
def test_the_probe_reports_signed_in_missing_or_unknown(
    tmp_path, family, code, text, expected
):
    home = _home(tmp_path, family)
    seen = []

    def run(argv, env):
        seen.append((argv, env))
        return code, text

    assert svc.signin_status(tmp_path, family, run=run) == expected
    argv, env = seen[0]
    assert argv[:2] == ["codex", "login"]  # Claude's home reads its token file
    assert argv[-1] == "status"
    variable = keep.HOME_VARIABLES[family]
    assert env[variable] == str(home)


@pytest.mark.parametrize("error", [OSError, TimeoutError, ValueError])
def test_a_probe_that_fails_or_times_out_reports_unknown(tmp_path, error):
    _home(tmp_path, "OPENAI")

    def run(argv, env):
        raise error("boom")

    assert svc.signin_status(tmp_path, "OPENAI", run=run) == "unknown"


def test_the_probe_resolves_the_home_without_creating_it(tmp_path):
    ran = []
    status = svc.signin_status(
        tmp_path, "ANTHROPIC", run=lambda argv, env: ran.append(argv)
    )
    assert status == "missing" and ran == []
    assert not keep.store_dir(tmp_path).exists()
    variable, home = keep.dedicated_home(tmp_path, "OPENAI")
    assert variable == "CODEX_HOME" and not home.exists()
    assert keep.dedicated_home(tmp_path, "OPENCODE") is None


def test_the_signin_command_prints_the_probe_result(tmp_path, monkeypatch, capsys):
    _signed_in(monkeypatch, "missing")
    code = cli.main(["signin", "--root", str(tmp_path), "--family", "OPENAI"])
    out = capsys.readouterr().out
    assert code == 0 and "OPENAI" in out and "missing" in out


# --- the refusal (TC-324) ------------------------------------------------------------


@pytest.mark.parametrize("status", ["missing", "unknown"])
def test_the_coordinator_route_refuses_a_retained_launch_not_signed_in(
    tmp_path, monkeypatch, launched, capsys, status
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch, status)
    assert _adjudicate(root) == svc.agent_common.EXIT_NEEDS_HUMAN
    out = capsys.readouterr().out
    assert "dev-setup" in out and status in out
    assert launched["argv"] == []  # no launch, fresh or otherwise
    assert not (keep.store_dir(root) / "home").exists()  # no home created
    assert _state(root) is None  # no lease taken, nothing recorded


@pytest.mark.parametrize("status", ["missing", "unknown"])
def test_the_loop_route_refuses_a_retained_launch_not_signed_in(
    tmp_path, monkeypatch, capsys, status
):
    al = load_script("agent_loop")
    root = _repo(tmp_path)
    monkeypatch.setattr(al.session_service, "cli_version", lambda *a, **k: "")
    monkeypatch.setattr(
        al.session_service, "signin_status", lambda root, family: status
    )
    ran = []
    monkeypatch.setattr(al.session_service, "act", lambda *a, **k: ran.append(a))
    ctx = _loop_ctx(root)
    ctx.status_path = root / "docs" / "status.md"
    ctx.worker = {"train": "t"}
    ctx.use_live = False
    ctx.args.no_session_echo = True
    plan = dict(PLAN, route_id=ROUTE, session_env=None)
    assert al.launch_session(ctx, plan, "WI-1") == al.EXIT_NEEDS_HUMAN
    assert ran == []
    out = capsys.readouterr().out
    assert "NEEDS-HUMAN" in out and "dev-setup" in out


def test_an_unretained_call_is_never_probed(tmp_path, monkeypatch, launched):
    """The probe guards only a launch whose keep carries a dedicated home: at
    the off dial, or for a brief class the dial does not retain, nothing is
    probed and the call launches fresh as before."""
    calls = _signed_in(monkeypatch, "missing")
    root = _repo(tmp_path, dial=0)
    assert _adjudicate(root) == 0
    root2 = _repo(tmp_path / "two")
    # the stub's verdict line is an amendment's, not a first approval's: 1
    assert _adjudicate(root2, brief="first-approval") == 1
    assert calls == []
    assert all("--session-id" not in a for a in launched["argv"])


def test_the_shipped_entry_point_defaults_to_the_strong_anthropic_route():
    assert cli.DEFAULT_ROUTE == ROUTE
    registry = cli.agent_route.load_registry(ROOT / "docs" / "agents.toml")[0]
    assert registry[ROUTE].family == "ANTHROPIC" and registry[ROUTE].tier == "strong"


# --- round 2 (Sol r1): the probe recognises only documented answers (TC-323) ----


@pytest.mark.parametrize(
    "family,code,text",
    [
        ("OPENAI", 0, "Logged in? No credentials found"),
        ("OPENAI", 2, "Not logged in"),
        ("OPENAI", 1, "Logged in using ChatGPT"),
        ("OPENAI", 0, "Logged in using ChatGPT\nNot logged in"),
        ("OPENAI", 0, "Logged in using ChatGPT\nfatal: status unavailable"),
        ("OPENAI", 1, "Not logged in\nfatal: status unavailable"),
        ("OPENAI", 0, "Logged in using ChatGPT\nLogged in using ChatGPT"),
        ("OPENAI", 0, "  Logged in using ChatGPT"),
        ("OPENAI", 0, "WARNING: other\nLogged in using ChatGPT"),
    ],
)
def test_an_undocumented_probe_answer_is_unknown(tmp_path, family, code, text):
    _home(tmp_path, family)
    assert svc.signin_status(tmp_path, family, run=lambda a, e: (code, text)) == (
        "unknown"
    )


# --- round 2 (Sol r1): the entry point runs only from a lane (TC-324) -----------


def test_a_primary_checkout_root_is_refused_before_launch(
    tmp_path, monkeypatch, launched, capsys
):
    """A run from the primary checkout would commit its session log onto
    trunk, which the integrator's audit refuses: it is refused before launch
    and writes nothing."""
    primary = _repo(tmp_path, where="primary")
    calls = _signed_in(monkeypatch)
    head = _git(primary, "rev-parse", "HEAD")
    assert _adjudicate(primary) == 2
    assert "primary checkout" in capsys.readouterr().out
    assert launched["argv"] == [] and calls == []
    assert _git(primary, "rev-parse", "HEAD") == head
    assert not (primary / "docs" / "iteration").exists()
    assert not keep.store_dir(primary).exists()


def test_a_worktree_whose_branch_holds_no_claim_is_refused(
    tmp_path, monkeypatch, launched, capsys
):
    root = _repo(tmp_path)
    _git(root, "checkout", "-q", "-b", "not-a-lane")
    _signed_in(monkeypatch)
    assert _adjudicate(root) == 2
    assert "no claim" in capsys.readouterr().out
    assert launched["argv"] == []


def test_a_root_outside_any_repository_is_refused(
    tmp_path, monkeypatch, launched, capsys
):
    """Otherwise valid inputs (policy, enabled route, brief): only the lane
    check can refuse, so removing it turns this red."""
    root = _inputs(tmp_path / "plain")
    _signed_in(monkeypatch)
    assert _adjudicate(root) == 2
    assert "is not the top of a git worktree" in capsys.readouterr().out
    assert launched["argv"] == []


# --- round 2 (Sol r1): a stale verdict never reads as success (TC-321) ----------


def test_a_failed_call_reusing_a_verdict_path_does_not_return_success(
    tmp_path, monkeypatch, launched, capsys
):
    """Sol's sequence: a successful run, then a failing call naming the same
    verdict path. The path already holds a verdict, so the second call is
    refused before launch; a failing call on a fresh path fails too."""
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    assert _adjudicate(root) == 0
    used = VERDICT["path"]
    monkeypatch.setattr(svc, "run_session", lambda *a, **k: (1, "failed", False))
    argv = [
        "adjudicate",
        "--root",
        str(root),
        "--brief-file",
        str(root / "brief.md"),
        "--brief",
        "amendment",
        "--wi",
        "WI-1",
        "--verdict",
        str(used),
    ]
    assert cli.main(argv) == 2
    assert "already exists" in capsys.readouterr().out
    assert _adjudicate(root) == 1


@pytest.mark.parametrize("code,timed_out", [(1, False), (0, "wall"), (0, "idle")])
def test_a_nonzero_exit_or_a_timeout_fails_whatever_file_exists(
    tmp_path, monkeypatch, launched, capsys, code, timed_out
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)

    def run(argv, root_, timeout, **kw):
        VERDICT["path"].write_text("VERDICT: MEANING rows=SR-1\n", encoding="utf-8")
        return code, _claude_stream(10), timed_out

    monkeypatch.setattr(svc, "run_session", run)
    assert _adjudicate(root) == 1
    assert "verdict valid" not in capsys.readouterr().out


# --- round 2 (Sol r1): an undecodable brief is the input refusal (TC-321) -------


def test_an_undecodable_brief_is_refused_with_the_usage_exit(
    tmp_path, monkeypatch, launched, capsys
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    (root / "brief.md").write_bytes(b"judge \xff this")
    assert _adjudicate(root) == 2
    assert "brief file cannot be read" in capsys.readouterr().out
    assert launched["argv"] == []


# --- round 3 (Sol r2): the verdict path is owned exclusively (TC-321) -----------


def _argv(root, verdict):
    return [
        "adjudicate",
        "--root",
        str(root),
        "--brief-file",
        str(root / "brief.md"),
        "--brief",
        "amendment",
        "--wi",
        "WI-1",
        "--verdict",
        str(verdict),
    ]


def test_two_calls_naming_one_verdict_path_never_share_its_verdict(
    tmp_path, monkeypatch, launched, capsys
):
    """Sol's sequence, with retention on: call A passes its input check;
    call B, naming the same absent path, starts while A runs; A's session
    exits 0 without writing a verdict. B is refused at the reservation and
    never launches, and A reads its own empty reservation as no verdict."""
    root = _repo(tmp_path, dial=50)
    _signed_in(monkeypatch)
    verdict = root / "shared-verdict.md"
    seen = {}

    def run_a(argv, root_, timeout, **kw):
        if "b" in seen:  # B's session (only if B was let through): it writes
            verdict.write_text("VERDICT: MEANING rows=SR-1\n", encoding="utf-8")
            return 0, _claude_stream(10), False
        seen["b"] = None
        seen["b"] = cli.main(_argv(root, verdict))  # B, while A runs
        return 0, _claude_stream(10), False  # A writes nothing

    monkeypatch.setattr(svc, "run_session", run_a)
    assert cli.main(_argv(root, verdict)) == 1
    assert seen["b"] == 2
    out = capsys.readouterr().out
    assert "reserved" in out and "verdict valid" not in out
    assert verdict.read_bytes() == b""  # A's reservation, left for inspection


def test_a_call_whose_session_writes_into_its_reservation_succeeds(
    tmp_path, monkeypatch, launched
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    verdict = root / "own-verdict.md"

    def run(argv, root_, timeout, **kw):
        assert verdict.read_bytes() == b""  # reserved before the launch
        verdict.write_text("VERDICT: MEANING rows=SR-1\n", encoding="utf-8")
        return 0, _claude_stream(10), False

    monkeypatch.setattr(svc, "run_session", run)
    assert cli.main(_argv(root, verdict)) == 0


def test_a_call_refused_before_launch_releases_its_reservation(
    tmp_path, monkeypatch, launched
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch, "missing")
    verdict = root / "refused-verdict.md"
    assert cli.main(_argv(root, verdict)) == svc.agent_common.EXIT_NEEDS_HUMAN
    assert not verdict.exists() and launched["argv"] == []


def test_a_verdict_path_that_cannot_be_reserved_is_refused(
    tmp_path, monkeypatch, launched, capsys
):
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    (root / "a-file").write_text("x", encoding="utf-8")
    assert cli.main(_argv(root, root / "a-file" / "v.md")) == 2
    assert "cannot be reserved" in capsys.readouterr().out
    assert launched["argv"] == []


# --- round 4: the first live run (TC-321, TC-266) --------------------------------


def test_a_verdict_path_under_a_missing_directory_is_reserved_and_launches(
    tmp_path, monkeypatch, launched
):
    """A work item's first adjudication names a review directory that does
    not exist yet: the reservation creates it, and the call launches."""
    root = _repo(tmp_path)
    _signed_in(monkeypatch)
    verdict = root / "docs" / "reviews" / "wi-1-new" / "001-ADJUDICATE.md"
    VERDICT["path"] = verdict
    assert cli.main(_argv(root, verdict)) == 0
    assert len(launched["argv"]) == 1
    assert verdict.read_text(encoding="utf-8").startswith("VERDICT: MEANING")


RETAINED = '["disposition", "amendment", "red-tc", "first-approval"]'


def _retaining(tmp_path):
    """A lane whose dial retains four brief classes, as this repo's does."""
    root = _repo(tmp_path)
    (root / "docs" / "process.toml").write_text(
        "[adjudicator]\ncontext_reset_pct = 50\nretain_for = {}\n".format(RETAINED),
        encoding="utf-8",
    )
    return root


def test_switching_retained_classes_with_nothing_edited_keeps_the_session(
    tmp_path, monkeypatch, launched
):
    root = _retaining(tmp_path)
    _signed_in(monkeypatch)
    _adjudicate(root, "WI-1", brief="amendment")
    _adjudicate(root, "WI-1", brief="first-approval")
    assert "--resume" in launched["argv"][1]
    record = _state(root)
    assert record["state"] == "active" and record["reset_reason"] == ""


def test_editing_another_retained_class_template_drains_the_session(
    tmp_path, monkeypatch, launched
):
    """The governing identity covers every retained class's template, so an
    edit to one the call does not use still drains the session."""
    root = _retaining(tmp_path)
    _signed_in(monkeypatch)
    prompts = cli.adjudicate_brief.prompts
    copied = tmp_path / "prompts"
    copied.mkdir()
    for name in prompts.KIT_PROMPTS.values():
        source = prompts.PROMPTS / name
        if source.is_file():
            (copied / name).write_bytes(source.read_bytes())
    monkeypatch.setattr(prompts, "PROMPTS", copied)
    _adjudicate(root, "WI-1", brief="amendment")
    red_tc = copied / prompts.KIT_PROMPTS[prompts.ADJUDICATE_RED_TC]
    red_tc.write_text(red_tc.read_text(encoding="utf-8") + "\nA new rule.\n")
    _adjudicate(root, "WI-1", brief="amendment")
    record = _state(root)
    assert record["state"] == "draining"
    assert record["reset_reason"] == "governing-inputs changed"


def test_an_operator_override_still_drains_the_session(tmp_path, monkeypatch, launched):
    """The coordinator's call mints under the shipped templates; the loop's
    next call of the same class under an operator override drains it."""
    al = load_script("agent_loop")
    root = _retaining(tmp_path)
    _signed_in(monkeypatch)
    _adjudicate(root, "WI-1", brief="amendment")
    assert _state(root)["state"] == "active"
    ctx = _loop_ctx(root, {"ADJUDICATE-AMENDMENT": "an override brief"})
    plan = dict(PLAN, brief="amendment", route_id=ROUTE, session_env=None)
    assert al.adjudication_keep(ctx, plan, "WI-1") is not None
    record = _state(root)
    assert record["state"] == "draining"
    assert record["reset_reason"] == "governing-inputs changed"


def test_a_family_with_no_dedicated_home_passes_require_signin_unprobed(
    tmp_path, monkeypatch
):
    """Pins existing behaviour: opencode has no dedicated home, so nothing
    is probed and nothing is refused."""
    calls = _signed_in(monkeypatch, "missing")
    assert "OPENCODE" not in keep.HOME_VARIABLES
    assert svc.require_signin(tmp_path, "OPENCODE") is None
    assert calls == []
