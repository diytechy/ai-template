"""Account tables, per-account homes and the one launch-environment rule (WI-798).

A second account of one CLI is an `[account.<ID>]` table in `docs/agents.toml`
and a qualified enable-list entry `ROUTE@ACCOUNT`, never a duplicated row. The
entry is the identity every consumer carries: its row, its account, the
account's home under the user configuration directory, its authentication
source and, for a retained call, the record whose identity includes the
account. These tests pin the Trust section's rulings consumer by consumer:
each one's absent, unreadable and malformed arms, the homes and precedence
shown by fixture CLIs that report the environment they were launched under
(one per IF-245 adapter), entry-keyed cooldowns, the record identity and its
one re-mint, the sign-in probe and the unverified printout.

No test reads a real credential or a real account home: the user
configuration directory is a temporary one (`tests/conftest.py` pins it for
every test, and these tests pin their own), every token is a canary file, and
the fixture CLIs are Python scripts on a temporary PATH.
"""

import json
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from conftest import hooked_checkout, load_script
from kitlib import provenance  # noqa: E402  (scripts/ is on the path)

route = load_script("agent_route")
svc = load_script("session_service")
keep = svc.session_keep
adapters = svc.session_adapters
coord = load_script("coordinator_adjudicate")
loop = load_script("agent_loop")
runner = load_script("plan_runner")

TEMPLATES = {
    "claude": "claude -p --model {model} --output-format stream-json --verbose",
    "codex": "codex exec --model {model}",
    "opencode": "opencode run --dir . -m {model} --auto",
    "gemini": "gemini --model {model}",
}

ROWS = "".join(
    '[agent.{c}-A]\nfamily = "F{c}"\nmodel = "m"\nversion = "1"\ntier = "strong"\n'
    'cmd_template = "{t}"\nenv = "ROUTE_ONLY=route-{c}"\nnotes = "row"\n\n'.format(
        c=cli.upper(), t=template
    )
    for cli, template in TEMPLATES.items()
)

ACCOUNTS = """
[account.WORK]
cli = "claude"
notes = "a second claude login, unverified"
env = "ACCOUNT_ONLY=work"

[account.HOME2]
cli = "claude"
notes = "a verified claude login"
verified = "2026-10-11 2.1.296"

[account.TOK]
cli = "claude"
notes = "a token account"
token_file_variable = "TEST_TOKEN_FILE_798"
"""
ACCOUNTS += "".join(
    '\n[account.{c}{n}]\ncli = "{cli}"\nnotes = "account {n}"\nenv = "ACCOUNT_ONLY={cli}-{n}"\n'.format(
        c=cli[:2].upper(), n=n, cli=cli
    )
    for cli in ("claude", "codex", "opencode", "gemini")
    for n in (1, 2)
)


@pytest.fixture
def config_dir(tmp_path, monkeypatch):
    """This test's own user configuration directory, where account homes live."""
    base = tmp_path / "user-config"
    monkeypatch.setenv("APPDATA" if os.name == "nt" else "XDG_CONFIG_HOME", str(base))
    return base


def _home(config_dir, account):
    return config_dir / "project-trajectory" / "accounts" / account


def _docs(root, agents=ROWS + ACCOUNTS, enabled=None):
    docs = Path(root) / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "agents.toml").write_text(agents, encoding="utf-8")
    if enabled is not None:
        (docs / "agents-enabled").write_text(
            "\n".join(enabled) + "\n", encoding="utf-8"
        )
    return docs


def _registry(tmp_path, agents=ROWS + ACCOUNTS):
    registry, errors = route.load_registry(_docs(tmp_path, agents) / "agents.toml")
    return registry, errors


# --- TC-361: the schema and the qualifier (the loader's arms) ----------------------


def test_account_tables_load_and_a_qualified_entry_carries_its_account(tmp_path):
    registry, errors = _registry(tmp_path)
    assert errors == []
    work = registry.accounts["WORK"]
    assert (work.cli, work.env, work.token_file_variable) == (
        "claude",
        "ACCOUNT_ONLY=work",
        "",
    )
    assert registry.accounts["TOK"].token_file_variable == "TEST_TOKEN_FILE_798"
    entries, errors = route.resolve_enabled(
        ["CLAUDE-A@WORK", "CLAUDE-A", "CLAUDE-A@HOME2"], registry
    )
    assert errors == []
    assert entries == ["CLAUDE-A@WORK", "CLAUDE-A", "CLAUDE-A@HOME2"]
    assert route.entry_route("CLAUDE-A@WORK") == "CLAUDE-A"
    assert route.entry_account("CLAUDE-A@WORK") == "WORK"
    assert route.account_of(registry, "CLAUDE-A@WORK") is work
    assert route.account_of(registry, "CLAUDE-A") is None  # the ambient login


@pytest.mark.parametrize(
    "table,why",
    [
        ('[account.BAD]\nnotes = "x"\n', "missing `cli`"),
        ('[account.BAD]\ncli = "cursor"\n', "outside"),
        ('[account.BAD]\ncli = "claude"\nhome = "x"\n', "unknown key"),
        ('[account.bad]\ncli = "claude"\n', "id outside"),
        ('[account.BAD]\ncli = "codex"\nenv = "CODEX_HOME=/x"\n', "home variable"),
        ('[account.BAD]\ncli = "claude"\nverified = "yes"\n', "verified"),
        (
            '[account.BAD]\ncli = "claude"\ntoken_file_variable = "a/b"\n',
            "variable name",
        ),
        (
            '[account.BAD]\ncli = "codex"\ntoken_file_variable = "T_798"\n',
            "no long-lived",
        ),
        ("[account.BAD]\ncli = 3\n", "non-string"),
    ],
)
def test_a_malformed_account_table_is_an_error_naming_it_and_is_dropped(
    tmp_path, table, why
):
    registry, errors = _registry(tmp_path, ROWS + table)
    named = [e for e in errors if "[account.BAD]" in e or "[account.bad]" in e]
    assert named and why in named[0], errors
    assert registry.accounts == {}
    assert set(registry) == {"CLAUDE-A", "CODEX-A", "OPENCODE-A", "GEMINI-A"}


def test_two_accounts_naming_one_token_variable_are_both_dropped(tmp_path):
    shared = (
        '[account.T1]\ncli = "claude"\ntoken_file_variable = "SAME_798"\n'
        '[account.T2]\ncli = "claude"\ntoken_file_variable = "SAME_798"\n'
    )
    registry, errors = _registry(tmp_path, ROWS + shared)
    assert len([e for e in errors if "SAME_798" in e]) == 2
    assert registry.accounts == {}


@pytest.mark.parametrize(
    "token",
    ["@WORK", "CLAUDE-A@", "CLAUDE-A@WORK@HOME2", "CLAUDE-A@NOPE", "CODEX-A@WORK"],
)
def test_a_malformed_qualifier_is_an_enable_list_error_never_the_unqualified_entry(
    tmp_path, token
):
    registry, _ = _registry(tmp_path)
    entries, errors = route.resolve_enabled([token], registry)
    assert entries == []  # never stripped to CLAUDE-A
    assert len(errors) == 1 and repr(token) in errors[0]


def test_route_and_account_environments_that_collide_are_refused(tmp_path):
    rows = ROWS + (
        '[agent.CLAUDE-HOME]\nfamily = "F"\nmodel = "m"\nversion = "1"\n'
        'tier = "strong"\ncmd_template = "claude -p"\nenv = "CLAUDE_CONFIG_DIR=/elsewhere"\n'
        '[agent.CLAUDE-KEY]\nfamily = "F"\nmodel = "m"\nversion = "1"\n'
        'tier = "strong"\ncmd_template = "claude -p"\nenv = "ACCOUNT_ONLY=route"\n'
    )
    registry, _ = _registry(tmp_path, rows + ACCOUNTS)
    entries, errors = route.resolve_enabled(
        ["CLAUDE-HOME@WORK", "CLAUDE-KEY@WORK", "CLAUDE-HOME", "CLAUDE-KEY"], registry
    )
    assert entries == ["CLAUDE-HOME", "CLAUDE-KEY"]  # unqualified: today's rule
    assert "CLAUDE_CONFIG_DIR" in errors[0] and "ACCOUNT_ONLY" in errors[1]


def test_an_unreadable_enable_list_is_an_error_and_an_absent_one_is_routing_off(
    tmp_path,
):
    docs = _docs(tmp_path)
    assert route.load_enabled_entries(docs / "agents-enabled") == ([], [])  # absent
    (docs / "agents-enabled").mkdir()  # exists, cannot be read as a file
    with pytest.raises(route.EnabledUnreadable):
        route.load_enabled_entries(docs / "agents-enabled")
    with pytest.raises(route.EnabledUnreadable):
        route.load_enabled(docs / "agents-enabled")


def test_keep_warm_is_off_on_an_unreadable_enable_list(tmp_path, capsys):
    docs = _docs(tmp_path)
    (docs / "agents-enabled").mkdir()
    on = keep.KeepConfig(context_reset_pct=50, keepwarm_minutes=50)
    assert svc.keep_warmer(tmp_path, on) is None  # no warmer, no thread
    err = capsys.readouterr().err
    assert err.startswith("keep-warm: off (") and "cannot be read" in err


def test_the_route_cli_exits_1_on_an_unreadable_enable_list(tmp_path, capsys):
    docs = _docs(tmp_path)
    (docs / "agents-enabled").mkdir()
    argv = ["--registry", str(docs / "agents.toml"), "--enabled"]
    assert route.main(argv + [str(docs / "agents-enabled"), "--list"]) == 1
    err = capsys.readouterr().err
    assert "agent_route: agents-enabled: " in err and "cannot be read" in err


def test_an_empty_registry_declares_nothing_and_an_unparseable_one_is_an_error(
    tmp_path,
):
    registry, errors = _registry(tmp_path, "")
    assert (dict(registry), registry.accounts, errors) == ({}, {}, [])
    registry, errors = _registry(tmp_path, "[account.X\ncli = 'claude'\n")
    assert registry.accounts == {} and errors and "does not parse" in errors[0]


# --- the loop launcher's arms --------------------------------------------------------


def test_the_loop_routes_on_an_unreadable_enable_list_and_fails_preflight(tmp_path):
    docs = _docs(tmp_path)
    (docs / "agents-enabled").mkdir()
    setup = loop.resolve_routing_setup(docs)
    assert setup.managed  # never routing off
    assert any("cannot be read" in e for e in setup.enable_errors)


def test_the_loop_fails_preflight_on_an_account_or_qualifier_error(tmp_path):
    agents = ROWS + ACCOUNTS + '[account.BAD]\ncli = "nope"\n'
    docs = _docs(tmp_path, agents, enabled=["CLAUDE-A@WORK", "CLAUDE-A@BAD"])
    setup = loop.resolve_routing_setup(docs)
    assert setup.managed and setup.enabled == ["CLAUDE-A@WORK"]
    assert any("[account.BAD]" in e for e in setup.reg_errors)
    assert any("'CLAUDE-A@BAD'" in e for e in setup.enable_errors)


def test_an_absent_registry_with_an_enable_list_fails_preflight(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "agents-enabled").write_text("CLAUDE-A@WORK\n", encoding="utf-8")
    setup = loop.resolve_routing_setup(docs)
    assert setup.managed and setup.enabled == [] and setup.enable_errors


def test_a_preference_may_name_a_qualified_entry():
    assert route.ENTRY_RE.match("CLAUDE-A@WORK")
    assert route.ENTRY_RE.match("CLAUDE-A")
    assert not route.ENTRY_RE.match("CLAUDE-A@WORK@X")
    assert not route.ENTRY_RE.match("CLAUDE-A@")


# --- TC-362: homes and the one launch-environment rule -------------------------------

FIXTURE_CLI = r"""
import json, os, sys
WATCHED = ("CLAUDE_CONFIG_DIR", "CODEX_HOME", "XDG_DATA_HOME", "OPENCODE_CONFIG",
           "GEMINI_CLI_HOME", "ROUTE_ONLY", "ACCOUNT_ONLY")
args = sys.argv[1:]
name = os.path.basename(sys.argv[0])
if args[:2] in (["auth", "status"], ["login", "status"]):
    home = os.environ.get("CLAUDE_CONFIG_DIR") or os.environ.get("CODEX_HOME") or ""
    signed = bool(home) and os.path.exists(os.path.join(home, "signed-in"))
    if args[0] == "auth":
        print(json.dumps({"loggedIn": signed}))
    else:
        sys.stderr.write("Logged in using ChatGPT\n" if signed else "Not logged in\n")
    sys.exit(0 if signed else 1)
sys.stdin.read()
seen = {k: os.environ[k] for k in WATCHED if k in os.environ}
seen["token"] = "CLAUDE_CODE_OAUTH_TOKEN" in os.environ
seen["canaries"] = sorted(k.upper() for k, v in os.environ.items()
                          if v.startswith("canary-ambient"))
seen["environ"] = dict(os.environ)
print("ENV " + json.dumps(seen, sort_keys=True))
"""


@pytest.fixture
def fixture_clis(tmp_path, monkeypatch):
    """One fixture CLI per IF-245 adapter (claude, codex, opencode, gemini) on
    a PATH of its own, each reporting the environment it was launched under,
    and answering its status command from a `signed-in` marker in its home."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    script = bindir / "envcli.py"
    script.write_text(FIXTURE_CLI, encoding="utf-8")
    for cli in TEMPLATES:
        if os.name == "nt":
            (bindir / (cli + ".cmd")).write_text(
                '@echo off\r\n"{}" "{}" %*\r\n'.format(sys.executable, script),
                encoding="ascii",
            )
        else:
            shim = bindir / cli
            shim.write_text(
                '#!/bin/sh\nexec "{}" "{}" "$@"\n'.format(sys.executable, script),
                encoding="ascii",
            )
            shim.chmod(0o755)
    monkeypatch.setenv("PATH", str(bindir) + os.pathsep + os.environ["PATH"])
    return bindir


def _launched_env(root, registry, entry):
    """What a fixture CLI reports when the entry is launched unretained
    through the session service under the one rule. `root` is made a
    checkout with its commit hooks on: the service refuses a launch anywhere
    else (WI-926)."""
    hooked_checkout(root)
    row = registry[route.entry_route(entry)]
    outcome = svc.act(
        svc.Call(
            root=root,
            role="BUILD",
            template=row.cmd_template,
            model=row.model,
            prompt="go",
            env=svc.entry_env(root, registry, entry),
            timeout=60,
        )
    )
    line = next(x for x in outcome.stream.splitlines() if x.startswith("ENV "))
    return json.loads(line[4:])


@pytest.mark.parametrize("cli", sorted(TEMPLATES))
def test_two_accounts_of_one_cli_launch_under_two_homes(
    tmp_path, config_dir, fixture_clis, cli
):
    registry, errors = _registry(tmp_path)
    assert errors == []
    prefix = cli[:2].upper()
    seen = {}
    for n in (1, 2):
        account = "{}{}".format(prefix, n)
        _home(config_dir, account).mkdir(parents=True)  # the person provisioned it
        seen[n] = _launched_env(
            tmp_path, registry, "{}-A@{}".format(cli.upper(), account)
        )
        home = _home(config_dir, account)
        expected = {k: v for k, v in adapters.home_env(cli, home).items()}
        assert {k: seen[n][k] for k in expected} == expected
        assert seen[n]["ROUTE_ONLY"] == "route-" + cli.upper()  # never overridden
        assert seen[n]["ACCOUNT_ONLY"] == "{}-{}".format(cli, n)
        assert seen[n]["token"] is False
    homes = [v for v in adapters.HOME_VARIABLES[cli]]
    assert all(seen[1][v] != seen[2][v] for v in homes)


def test_an_ambient_entry_has_no_kit_held_home(
    tmp_path, config_dir, fixture_clis, monkeypatch
):
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    registry, _ = _registry(tmp_path)
    seen = _launched_env(tmp_path, registry, "CLAUDE-A")
    assert "CLAUDE_CONFIG_DIR" not in seen and seen["ROUTE_ONLY"] == "route-CLAUDE"
    assert not (config_dir / "project-trajectory").exists()  # nothing created


def _spaced_claude(fixture_clis):
    """The fixture claude CLI at a path holding a space."""
    shim = "claude.cmd" if os.name == "nt" else "claude"
    spaced = fixture_clis.parent / "my tools"
    spaced.mkdir(exist_ok=True)
    (spaced / shim).write_bytes((fixture_clis / shim).read_bytes())
    (spaced / shim).chmod(0o755)
    return (spaced / shim).as_posix()


@pytest.mark.parametrize("form", ["json-array", "quoted-path"])
def test_a_qualified_entry_launches_on_every_template_form_the_launcher_reads(
    tmp_path, config_dir, fixture_clis, form
):
    """The CLI a route launches is read by the launcher's own template parse,
    so a qualified entry is recognised on a JSON-array template and on a
    quoted executable path with a space, as its ambient entry is."""
    template = {
        "json-array": '["claude", "-p", "--model", "{model}"]',
        "quoted-path": '"{}" -p --model {{model}}'.format(_spaced_claude(fixture_clis)),
    }[form]
    row = (
        '[agent.CLAUDE-J]\nfamily = "F"\nmodel = "m"\nversion = "1"\n'
        'tier = "strong"\ncmd_template = \'{}\'\nenv = "ROUTE_ONLY=j"\n\n'
    ).format(template)
    registry, errors = _registry(tmp_path, ROWS + row + ACCOUNTS)
    assert errors == [] and route.route_cli(registry["CLAUDE-J"]) == "claude"
    entries, errors = route.resolve_enabled(["CLAUDE-J@WORK"], registry)
    assert (entries, errors) == (["CLAUDE-J@WORK"], [])
    home = _home(config_dir, "WORK")
    home.mkdir(parents=True)
    seen = _launched_env(tmp_path, registry, "CLAUDE-J@WORK")
    assert seen["CLAUDE_CONFIG_DIR"] == str(home) and seen["ACCOUNT_ONLY"] == "work"


def test_a_template_the_launcher_refuses_names_no_cli(tmp_path):
    row = SimpleNamespace(
        id="CLAUDE-J", cmd_template='["claude", 3]', model="m", env=""
    )
    assert route.route_runner(row.cmd_template, row.model) == ""
    assert route.route_cli(row) == ""
    account = SimpleNamespace(cli="claude", env="")
    assert "launches no known CLI" in route.qualifier_problem(row, account, "WORK")


def test_the_launch_rule_refuses_a_route_env_that_names_the_home_or_a_shared_key(
    tmp_path, config_dir
):
    registry, _ = _registry(tmp_path)
    row = SimpleNamespace(**vars_of(registry["CLAUDE-A"]))
    for env in ("CLAUDE_CONFIG_DIR=/x", "ACCOUNT_ONLY=route"):
        row.env = env
        with pytest.raises(svc.SigninRefused, match="neither side silently"):
            svc.launch_env(tmp_path, row, registry.accounts["WORK"])


def vars_of(row):
    return {k: getattr(row, k) for k in row.__slots__}


def test_a_login_account_with_no_home_is_refused_naming_its_provisioning(
    tmp_path, config_dir
):
    registry, _ = _registry(tmp_path)
    with pytest.raises(svc.SigninRefused) as refused:
        svc.entry_env(tmp_path, registry, "CODEX-A@CO1")
    hint = svc.provision_command(registry.accounts["CO1"])
    assert hint == 'with CODEX_HOME set to "{}", run `codex login`'.format(
        _home(config_dir, "CO1")
    )
    assert "Sign it in there yourself: {}.".format(hint) in str(refused.value)
    assert not _home(config_dir, "CO1").exists()  # never created by the kit


# A shell assignment (`NAME=value`): the hint names its variables in prose
# instead, so no reader is handed a form its shell does not run.
ASSIGNMENT = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*=")


@pytest.mark.parametrize(
    "cli,expected",
    [
        ("claude", 'with CLAUDE_CONFIG_DIR set to "{h}", run `claude auth login`'),
        (
            "opencode",
            'with XDG_DATA_HOME set to "{d}" and OPENCODE_CONFIG set to "{c}", '
            "run `opencode auth login`",
        ),
    ],
)
def test_the_provisioning_hint_names_each_variable_in_prose_with_its_value_quoted(
    tmp_path, monkeypatch, cli, expected
):
    base = tmp_path / "user config"  # a home holding a space
    monkeypatch.setenv("APPDATA" if os.name == "nt" else "XDG_CONFIG_HOME", str(base))
    hint = svc.provision_command(SimpleNamespace(id="A1", cli=cli))
    home = keep.account_home("A1")
    assert " " in str(home) and not ASSIGNMENT.search(hint)
    assert hint == expected.format(h=home, d=home / "data", c=home / "opencode.json")


def test_a_token_account_home_is_created_empty_and_carries_the_token(
    tmp_path, config_dir, monkeypatch
):
    token = tmp_path / "outside" / "token"
    token.parent.mkdir()
    token.write_text("canary-798\n", encoding="utf-8")
    monkeypatch.setenv("TEST_TOKEN_FILE_798", str(token))
    registry, _ = _registry(tmp_path)
    env = svc.entry_env(tmp_path, registry, "CLAUDE-A@TOK")
    home = _home(config_dir, "TOK")
    assert home.is_dir() and list(home.iterdir()) == []
    assert env["CLAUDE_CONFIG_DIR"] == str(home)
    assert env["CLAUDE_CODE_OAUTH_TOKEN"] == "canary-798"


def test_a_token_account_whose_token_cannot_be_read_is_refused_before_its_home(
    tmp_path, config_dir
):
    registry, _ = _registry(tmp_path)
    with pytest.raises(svc.SigninRefused) as refused:
        svc.entry_env(tmp_path, registry, "CLAUDE-A@TOK")
    assert "TEST_TOKEN_FILE_798" in str(refused.value) and "dev-setup" in str(
        refused.value
    )
    assert not _home(config_dir, "TOK").exists()


def test_an_unresolvable_user_config_dir_refuses_every_qualified_launch(
    tmp_path, monkeypatch
):
    registry, _ = _registry(tmp_path)
    monkeypatch.setattr(keep, "user_config_dir", lambda environ=None: None)
    with pytest.raises(svc.SigninRefused, match="cannot be resolved"):
        svc.entry_env(tmp_path, registry, "CLAUDE-A@WORK")
    assert svc.entry_env(tmp_path, registry, "CLAUDE-A")["ROUTE_ONLY"]  # ambient


def test_the_user_config_dir_follows_the_platform_rule():
    if os.name == "nt":
        assert keep.user_config_dir({"APPDATA": r"C:\Users\x\AppData\Roaming"}) == Path(
            r"C:\Users\x\AppData\Roaming"
        )
        assert keep.user_config_dir({}) is None
        assert keep.user_config_dir({"APPDATA": "relative"}) is None
    else:
        assert keep.user_config_dir({"XDG_CONFIG_HOME": "/cfg"}) == Path("/cfg")
        assert keep.user_config_dir({"XDG_CONFIG_HOME": "rel"}).name == ".config"
    home = keep.account_home("WORK", {"APPDATA": "C:\\cfg", "XDG_CONFIG_HOME": "/cfg"})
    assert home.parts[-3:] == ("project-trajectory", "accounts", "WORK")


def test_a_probe_on_an_account_that_cannot_launch_fails_with_the_refusal(
    tmp_path, config_dir
):
    registry, _ = _registry(tmp_path)
    ok, transcript = loop.probe_route(
        registry["CODEX-A"], tmp_path, account=registry.accounts["CO1"]
    )
    assert not ok and "codex login" in transcript


# --- TC-363: entry-keyed cooldowns and the planner's entries -------------------------


def test_two_accounts_on_one_route_cool_and_select_independently(tmp_path):
    registry, _ = _registry(tmp_path)
    enabled = ["CLAUDE-A@WORK", "CLAUDE-A@HOME2"]
    cooldowns = {}
    assert (
        route.select(enabled, registry, "strong", 0.0, cooldowns)[0] == "CLAUDE-A@WORK"
    )
    route.cool(cooldowns, "CLAUDE-A@WORK", 0.0, 60)
    chosen, reason = route.select(enabled, registry, "strong", 1.0, cooldowns)
    assert chosen == "CLAUDE-A@HOME2" and "CLAUDE-A@HOME2" in reason
    assert "cooling" in route.pool_context(enabled, registry, cooldowns, 1.0)


def test_the_dual_plan_fallback_carries_the_failed_entry_and_refuses_errors(
    tmp_path, config_dir
):
    rows = ROWS + (
        '[agent.OTHER-A]\nfamily = "OTHER"\nmodel = "m"\nversion = "1"\n'
        'tier = "strong"\ncmd_template = "claude -p"\nnotes = "row"\n'
    )
    for name in ("CL1", "CL2"):
        _home(config_dir, name).mkdir(parents=True)
    _docs(
        tmp_path, rows + ACCOUNTS, enabled=["CLAUDE-A@CL1", "OTHER-A", "CLAUDE-A@CL2"]
    )
    registry, _ = route.load_registry(tmp_path / "docs" / "agents.toml")
    pair, routes, why = runner._dp_fallback(tmp_path, registry, "CLAUDE-A@CL1")
    assert why == "" and [s.entry for s in pair.sessions] == ["OTHER-A", "OTHER-A"]
    assert [r[4] for r in routes] == ["OTHER-A", "OTHER-A"]
    _docs(tmp_path, rows + ACCOUNTS, enabled=["CLAUDE-A@CL1", "NO-SUCH-ROW"])
    _, routes, why = runner._dp_fallback(tmp_path, registry, "CLAUDE-A@CL1")
    assert routes == [] and "NO-SUCH-ROW" in why  # refused, never discarded
    (tmp_path / "docs" / "agents-enabled").unlink()
    (tmp_path / "docs" / "agents-enabled").mkdir()
    _, routes, why = runner._dp_fallback(tmp_path, registry, "CLAUDE-A@CL1")
    assert routes == [] and "cannot be read" in why


def test_the_dual_plan_routes_page_on_an_unreadable_enable_list(tmp_path):
    docs = _docs(tmp_path)
    (docs / "agents-enabled").mkdir()
    routes, registry, note = runner._dp_routes(tmp_path, "strong")
    assert routes is None and registry is not None and "cannot be read" in note


def test_the_dual_plan_hats_launch_under_their_accounts(tmp_path, config_dir):
    for name in ("CL1", "CO1"):
        _home(config_dir, name).mkdir(parents=True)
    _docs(tmp_path, enabled=["CLAUDE-A@CL1", "CODEX-A@CO1"])
    routes, _registry_, _note = runner._dp_routes(tmp_path, "strong")
    by_entry = {r[4]: r[3] for r in routes}
    assert by_entry["CLAUDE-A@CL1"]["CLAUDE_CONFIG_DIR"] == str(
        _home(config_dir, "CL1")
    )
    assert by_entry["CODEX-A@CO1"]["CODEX_HOME"] == str(_home(config_dir, "CO1"))


# --- TC-364: the retained record's identity ------------------------------------------


def _prepared(home=None):
    return SimpleNamespace(home=home or {}, family="FCLAUDE")


def _keep_for(root, account="", **kw):
    return keep.keep_for(
        root,
        keep.KeepConfig(context_reset_pct=50),
        role="ADJUDICATE",
        brief="disposition",
        family="FCLAUDE",
        route_id="CLAUDE-A",
        wi="WI-1",
        lease_wait=0,
        prepared=_prepared(),
        account=account,
        **kw,
    )


def _full_record(root, account, session="S1"):
    record = {
        "family": "FCLAUDE",
        "route_id": "CLAUDE-A",
        "session_id": session,
        "generation": 1,
        "governing_hash": keep.governing_hash(root),
        "cli_version": "",
        "judged": [],
        "state": "active",
        "reset_reason": "",
    }
    if account is not None:
        record["account"] = account
    return record


def test_a_record_written_before_accounts_is_not_its_own_and_mints_once(tmp_path):
    legacy = _full_record(tmp_path, None)
    path = keep.store_dir(tmp_path) / keep._record_name("FCLAUDE", "CLAUDE-A")
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(legacy), encoding="utf-8")
    assert keep.store_load(tmp_path, "FCLAUDE", "CLAUDE-A") is None  # lacks account
    kept = _keep_for(tmp_path)
    assert kept.session_id == "" and kept.account == ""  # the one re-mint
    written = keep.store_load(tmp_path, "FCLAUDE", "CLAUDE-A")
    assert written["account"] == "" and written["lease"]["holder"] == kept.holder


def test_another_accounts_record_is_never_resumed(tmp_path):
    with keep.store_lock(tmp_path):
        keep.store_save(tmp_path, _full_record(tmp_path, "WORK"))
    assert keep.store_load(tmp_path, "FCLAUDE", "CLAUDE-A", account="WORK")
    assert keep.store_load(tmp_path, "FCLAUDE", "CLAUDE-A", account="HOME2") is None
    assert keep.store_load(tmp_path, "FCLAUDE", "CLAUDE-A") is None
    assert _keep_for(tmp_path, "HOME2").session_id == ""  # mints its own
    resumed = _keep_for(tmp_path, "WORK")
    assert resumed.session_id == "S1" and resumed.account == "WORK"


def test_a_marker_names_its_account_and_another_accounts_read_ignores_it(tmp_path):
    with keep.store_lock(tmp_path):
        keep.store_save(tmp_path, _full_record(tmp_path, "WORK"))
    kept = _keep_for(tmp_path, "WORK")
    keep.publish_marker(tmp_path, keep.keep_marker(kept, keep.RELEASE))
    work = keep._pending(tmp_path, ("FCLAUDE", "CLAUDE-A", "", "WORK"))
    other = keep._pending(tmp_path, ("FCLAUDE", "CLAUDE-A", "", "HOME2"))
    assert len(work.markers) == 1 and work.markers[0][1]["account"] == "WORK"
    assert other.markers == []


def test_a_scoped_records_pin_is_its_qualified_entry(tmp_path):
    record = {**_full_record(tmp_path, "WORK"), "scope": "lane@base:REVIEW-A:iteration"}
    with keep.store_lock(tmp_path):
        keep.store_save(tmp_path, record)
    assert keep.scoped_route(tmp_path, record["scope"]) == "CLAUDE-A@WORK"


# --- keep-warm: only enabled entries whose account resolves -------------------------


def test_keep_warm_pings_only_enabled_entries_whose_account_resolves(tmp_path):
    registry, _ = _registry(tmp_path)
    routes = svc._warm_routes(
        registry, ["CLAUDE-A@WORK", "CLAUDE-A", "CODEX-A@CO1", "CLAUDE-A@GONE"]
    )
    assert routes == {("CLAUDE-A", "WORK"), ("CLAUDE-A", "")}  # codex: never one turn
    warmer = svc.KeepWarmer(tmp_path, keep.KeepConfig(), registry, entries=[])
    assert warmer.routes == set()
    prepared, why = warmer._prepare("CLAUDE-A", "GONE")
    assert prepared is None and "GONE" in why  # never the ambient login


# --- TC-365: the adjudicator's entry and the sign-in probe ---------------------------


def test_the_adjudicator_refuses_a_registry_error_an_undeclared_account_or_an_unreadable_list(
    tmp_path,
):
    _docs(tmp_path, enabled=["CLAUDE-A@TOK", "CLAUDE-A"])
    registry, why = coord.resolve_route(tmp_path, "CLAUDE-A@TOK")
    assert why is None and route.account_of(registry, "CLAUDE-A@TOK").id == "TOK"
    assert "not declared" in coord.resolve_route(tmp_path, "CLAUDE-A@NOPE")[1]
    assert "not named" in coord.resolve_route(tmp_path, "CLAUDE-A@WORK")[1]
    _docs(tmp_path, ROWS + ACCOUNTS + '[account.BAD]\ncli = "x"\n')
    assert "[account.BAD]" in coord.resolve_route(tmp_path, "CLAUDE-A@TOK")[1]
    _docs(tmp_path)
    (tmp_path / "docs" / "agents-enabled").unlink()
    (tmp_path / "docs" / "agents-enabled").mkdir()
    assert "cannot be read" in coord.resolve_route(tmp_path, "CLAUDE-A@TOK")[1]


def registry_of(root):
    return route.load_registry(Path(root) / "docs" / "agents.toml")[0]


def _signin(root, entry, capsys):
    assert coord.main(["signin", "--root", str(root), "--route", entry]) == 0
    return capsys.readouterr().out.splitlines()


def test_the_signin_probe_reads_a_token_account_from_its_file_only(
    tmp_path, config_dir, monkeypatch, capsys
):
    _docs(tmp_path, enabled=["CLAUDE-A@TOK"])
    lines = _signin(tmp_path, "CLAUDE-A@TOK", capsys)
    assert lines == [
        "signin [TOK] token: missing",
        "signin [TOK]: token_file_variable TEST_TOKEN_FILE_798",
    ]
    token = tmp_path / "outside" / "token"
    token.parent.mkdir()
    token.write_text("canary-798", encoding="utf-8")
    monkeypatch.setenv("TEST_TOKEN_FILE_798", str(token))
    lines = _signin(tmp_path, "CLAUDE-A@TOK", capsys)
    assert lines[0] == "signin [TOK] token: signed-in"
    assert "canary-798" not in "\n".join(lines) and str(token) not in "\n".join(lines)
    assert not _home(config_dir, "TOK").exists()  # the probe creates nothing


def test_the_signin_probe_reads_a_login_account_from_its_own_home(
    tmp_path, config_dir, fixture_clis, capsys
):
    _docs(tmp_path, enabled=["CLAUDE-A@WORK", "CLAUDE-A@HOME2", "CODEX-A@CO1"])
    lines = _signin(tmp_path, "CLAUDE-A@WORK", capsys)
    assert lines[0] == "signin [WORK] login: missing (unverified)"
    assert "provision it yourself" in lines[1] and "claude auth login" in lines[1]
    assert "UNVERIFIED" in lines[2]
    home = _home(config_dir, "WORK")
    home.mkdir(parents=True)
    assert _signin(tmp_path, "CLAUDE-A@WORK", capsys)[0] == (
        "signin [WORK] login: missing (unverified)"  # the fixture's own answer
    )
    (home / "signed-in").write_text("", encoding="utf-8")
    assert _signin(tmp_path, "CLAUDE-A@WORK", capsys)[0] == (
        "signin [WORK] login: signed-in (unverified)"
    )
    # a sign-in in another account's home never establishes this one
    _home(config_dir, "HOME2").mkdir(parents=True)
    assert _signin(tmp_path, "CLAUDE-A@HOME2", capsys) == [
        "signin [HOME2] login: missing",
        "signin [HOME2]: provision it yourself: "
        + svc.provision_command(registry_of(tmp_path).accounts["HOME2"]),
    ]
    _home(config_dir, "CO1").mkdir(parents=True)
    assert _signin(tmp_path, "CODEX-A@CO1", capsys)[0] == "signin [CO1] login: missing"


def test_the_signin_probe_names_an_ambient_or_unresolved_entry(tmp_path, capsys):
    _docs(tmp_path, enabled=["CLAUDE-A"])
    assert _signin(tmp_path, "CLAUDE-A", capsys) == ["signin [-] ambient: ambient"]
    lines = _signin(tmp_path, "CLAUDE-A@WORK", capsys)
    assert lines[0].startswith("signin [-] unresolved: unknown (")


@pytest.mark.parametrize(
    "code,text,expected",
    [
        (0, '{"loggedIn": true, "authMethod": "claude.ai"}\n', "signed-in"),
        (1, '{"loggedIn": false, "authMethod": "none"}\n', "missing"),
        (0, '{"loggedIn": false}\n', "unknown"),
        (1, '{"loggedIn": true}\n', "unknown"),
        (0, "not json\n", "unknown"),
        (0, '[{"loggedIn": true}]\n', "unknown"),
        (2, '{"loggedIn": false}\n', "unknown"),
    ],
)
def test_the_claude_status_reader_takes_only_its_documented_pairs(code, text, expected):
    assert svc._claude_signin(code, text) == expected


def test_a_retained_login_account_not_signed_in_is_refused_with_its_provisioning(
    tmp_path, config_dir, fixture_clis
):
    registry, _ = _registry(tmp_path)
    _home(config_dir, "WORK").mkdir(parents=True)
    prepared = svc.prepare_launch(
        tmp_path, registry["CLAUDE-A"], registry.accounts["WORK"]
    )
    with pytest.raises(svc.SigninRefused) as refused:
        svc.require_signin(tmp_path, prepared)
    hint = svc.provision_command(registry.accounts["WORK"])
    assert "`claude auth login`" in hint and hint in str(refused.value)
    (_home(config_dir, "WORK") / "signed-in").write_text("", encoding="utf-8")
    assert svc.require_signin(tmp_path, prepared) is None


# --- TC-366: an unverified Claude login is printed, never refused --------------------


def test_preflight_prints_each_enabled_unverified_account_only(tmp_path):
    registry, _ = _registry(tmp_path)
    lines = route.unverified_lines(
        registry,
        ["CLAUDE-A@WORK", "CLAUDE-A@HOME2", "CLAUDE-A@TOK", "CLAUDE-A", "CODEX-A@CO1"],
    )
    assert len(lines) == 1 and lines[0].startswith(
        "CLAUDE-A@WORK: account WORK is UNVERIFIED"
    )
    assert registry.accounts["WORK"].unverified
    assert not registry.accounts["TOK"].unverified  # outside the isolation question


def test_the_loop_preflight_prints_the_unverified_account_and_passes_it(
    tmp_path, capsys, monkeypatch
):
    docs = _docs(tmp_path, enabled=["CLAUDE-A@WORK"])
    setup = loop.resolve_routing_setup(docs)
    monkeypatch.setattr(loop, "preflight", lambda root, template, args: [])
    monkeypatch.setattr(loop.prompts, "preflight", lambda: [])
    monkeypatch.setattr(loop, "launcher_exe", lambda tmpl: ("claude", True))
    failures, _templates = loop.map_preflight(
        tmp_path,
        "",
        None,
        {},
        {},
        {},
        {},
        True,
        setup.registry,
        setup.enabled,
        setup.reg_errors,
        setup.enable_errors,
    )
    assert failures == []  # printed, never refused
    assert "account WORK is UNVERIFIED" in capsys.readouterr().err


# --- TC-362 (round 3): the selected account's authentication mode owns the env -------

# The ambient sources each CLI ranks above a login in its own home, written
# out from the sources session_service.COMPETING_CREDENTIALS cites (not read
# from it): Claude's authentication precedence and profile/federation table;
# the WI-788 design's per-CLI table for codex; Gemini CLI's
# getAuthTypeFromEnv (packages/core/src/core/contentGenerator.ts) and its
# Vertex credentials. opencode has no list: its credential sources are
# open-ended, so a qualified opencode launch starts from a declared base
# instead (the opencode tests below).
AMBIENT_SOURCES = {
    "claude": (
        "CLAUDE_CODE_USE_BEDROCK",
        "CLAUDE_CODE_USE_VERTEX",
        "CLAUDE_CODE_USE_FOUNDRY",
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_API_KEY",
        "CLAUDE_CODE_OAUTH_TOKEN",
        "ANTHROPIC_PROFILE",
        "ANTHROPIC_FEDERATION_RULE_ID",
    ),
    "codex": ("CODEX_API_KEY", "OPENAI_API_KEY"),
    "gemini": (
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_GEMINI_BASE_URL",
        "GEMINI_API_KEY",
        "CLOUD_SHELL",
        "GEMINI_CLI_USE_COMPUTE_ADC",
        "GOOGLE_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
    ),
}
EVERY_SOURCE = sorted({n for names in AMBIENT_SOURCES.values() for n in names})


def _canaries(monkeypatch, names=EVERY_SOURCE):
    for name in names:
        monkeypatch.setenv(name, "canary-ambient-" + name)


def _carried(env):
    return sorted(
        k.upper() for k, v in (env or {}).items() if k.upper() in EVERY_SOURCE
    )


@pytest.mark.parametrize("cli", sorted(AMBIENT_SOURCES))
def test_a_qualified_login_launch_withholds_every_ambient_credential_its_cli_ranks_above_the_home(
    tmp_path, config_dir, fixture_clis, monkeypatch, cli
):
    _canaries(monkeypatch)
    registry, errors = _registry(tmp_path)
    assert errors == []
    account = registry.accounts[cli[:2].upper() + "1"]
    row = registry[cli.upper() + "-A"]
    entry = "{}@{}".format(row.id, account.id)
    _home(config_dir, account.id).mkdir(parents=True)
    ranked = set(AMBIENT_SOURCES[cli])
    prepared = svc.prepare_launch(tmp_path, row, account)
    seen_run = []
    svc.signin_status(
        tmp_path,
        account,
        row=row,
        run=lambda argv, env: seen_run.append(env) or (1, ""),
    )
    for env in [
        svc.entry_env(tmp_path, registry, entry),
        svc.compose_env(os.environ, prepared),
        svc.probe_env(prepared),
        *seen_run,
    ]:
        assert ranked.isdisjoint(_carried(env)), _carried(env)
    launched = _launched_env(tmp_path, registry, entry)["canaries"]
    assert ranked.isdisjoint(launched), launched
    # every other CLI's sources are not this account's to withhold
    assert set(launched) == set(EVERY_SOURCE) - ranked
    assert set(svc.COMPETING_CREDENTIALS[cli]) == ranked  # the one table


def test_a_token_account_launch_carries_only_its_own_token(
    tmp_path, config_dir, monkeypatch
):
    _canaries(monkeypatch, AMBIENT_SOURCES["claude"])
    token = tmp_path / "outside" / "token"
    token.parent.mkdir()
    token.write_text("file-token-798\n", encoding="utf-8")
    monkeypatch.setenv("TEST_TOKEN_FILE_798", str(token))
    registry, _ = _registry(tmp_path)
    env = svc.entry_env(tmp_path, registry, "CLAUDE-A@TOK")
    assert _carried(env) == ["CLAUDE_CODE_OAUTH_TOKEN"]
    assert env["CLAUDE_CODE_OAUTH_TOKEN"] == "file-token-798"


def test_an_ambient_entry_keeps_the_ambient_environment(tmp_path, monkeypatch):
    _canaries(monkeypatch)
    registry, _ = _registry(tmp_path)
    bare = SimpleNamespace(**vars_of(registry["CLAUDE-A"]))
    bare.env = ""
    assert svc.launch_env(tmp_path, bare, None) is None  # inherit exactly
    env = svc.entry_env(tmp_path, registry, "CLAUDE-A")
    assert _carried(env) == EVERY_SOURCE  # every canary kept
    bare.env = "ANTHROPIC_API_KEY=route-declared"  # the route's own choice
    assert svc.launch_env(tmp_path, bare, None)["ANTHROPIC_API_KEY"] == (
        "route-declared"
    )


# An opencode provider's key is any catalog provider's variable, or its SDK's
# own default, and OPENCODE_AUTH_CONTENT stands in for the home's auth.json:
# the canaries are one of each kind. The proxy is a transport variable the
# declared base keeps.
OPENCODE_AMBIENT = ("XAI_API_KEY", "OPENCODE_AUTH_CONTENT", "SOME_PROVIDER_API_KEY")
PROXY = "http://proxy.invalid:3128"


def _opencode_ambient(monkeypatch):
    for name in OPENCODE_AMBIENT:
        monkeypatch.setenv(name, "canary-ambient-" + name)
    monkeypatch.setenv("HTTPS_PROXY", PROXY)


def _folded(env):
    return {route.env_name_key(k): v for k, v in (env or {}).items()}


def test_a_qualified_opencode_launch_starts_from_the_declared_base(
    tmp_path, config_dir, fixture_clis, monkeypatch
):
    _opencode_ambient(monkeypatch)
    registry, errors = _registry(tmp_path)
    assert errors == []
    account, row = registry.accounts["OP1"], registry["OPENCODE-A"]
    _home(config_dir, "OP1").mkdir(parents=True)
    prepared = svc.prepare_launch(tmp_path, row, account)
    seen_run = []
    svc.signin_status(
        tmp_path,
        account,
        row=row,
        run=lambda argv, env: seen_run.append(env) or (1, ""),
    )
    for env in [
        svc.entry_env(tmp_path, registry, "OPENCODE-A@OP1"),
        svc.compose_env(os.environ, prepared),
        svc.probe_env(prepared),
        *seen_run,
    ]:
        folded = _folded(env)
        assert not {route.env_name_key(n) for n in OPENCODE_AMBIENT} & set(folded)
        assert folded[route.env_name_key("PATH")] == os.environ["PATH"]
        assert folded[route.env_name_key("HTTPS_PROXY")] == PROXY
    launched = _launched_env(tmp_path, registry, "OPENCODE-A@OP1")
    assert launched["canaries"] == []
    assert launched["ROUTE_ONLY"] == "route-OPENCODE"  # the route's declared pairs
    assert launched["ACCOUNT_ONLY"] == "opencode-1"  # the account's
    assert launched["XDG_DATA_HOME"] == str(_home(config_dir, "OP1") / "data")


def test_a_qualified_opencode_launch_keeps_the_kit_owned_names(
    tmp_path, config_dir, fixture_clis, monkeypatch
):
    """The loop marks its own process, and every session it launches inherits
    the mark, whatever the account's declared base keeps: a commit the child
    makes is read as the loop's by the floors that rely on it."""
    _opencode_ambient(monkeypatch)
    marker = provenance.mark_loop_process()
    registry, errors = _registry(tmp_path)
    assert errors == []
    _home(config_dir, "OP1").mkdir(parents=True)
    launched = _launched_env(tmp_path, registry, "OPENCODE-A@OP1")
    assert launched["environ"].get(provenance.LOOP_SESSION_ENV) == marker
    for name in svc.KIT_INHERITED:
        assert launched["environ"].get(name) == os.environ[name]
    assert launched["canaries"] == []  # the credentials stay withheld


def test_an_unqualified_opencode_entry_keeps_the_ambient_environment(
    tmp_path, monkeypatch
):
    _opencode_ambient(monkeypatch)
    registry, _ = _registry(tmp_path)
    folded = _folded(svc.entry_env(tmp_path, registry, "OPENCODE-A"))
    for name in OPENCODE_AMBIENT:
        assert folded[route.env_name_key(name)] == "canary-ambient-" + name
    assert folded[route.env_name_key("HTTPS_PROXY")] == PROXY


@pytest.mark.parametrize("side", ["route", "account"])
def test_a_key_declared_for_a_qualified_opencode_launch_is_carried(
    tmp_path, config_dir, monkeypatch, side
):
    _opencode_ambient(monkeypatch)
    keyed = '\n[account.OPKEY]\ncli = "opencode"\nnotes = "k"\n'
    if side == "account":
        keyed += 'env = "XAI_API_KEY=declared-xai"\n'
    registry, errors = _registry(tmp_path, ROWS + ACCOUNTS + keyed)
    assert errors == []
    row = SimpleNamespace(**vars_of(registry["OPENCODE-A"]))
    if side == "route":
        row.env = "XAI_API_KEY=declared-xai"
    _home(config_dir, "OPKEY").mkdir(parents=True)
    folded = _folded(svc.launch_env(tmp_path, row, registry.accounts["OPKEY"]))
    assert folded[route.env_name_key("XAI_API_KEY")] == "declared-xai"
    assert route.env_name_key("OPENCODE_AUTH_CONTENT") not in folded


@pytest.mark.parametrize("side", ["route", "account"])
def test_a_login_account_whose_route_or_account_declares_a_competing_source_is_refused(
    tmp_path, config_dir, side
):
    keyed = '\n[account.KEYED]\ncli = "claude"\nnotes = "k"\n'
    if side == "account":
        keyed += 'env = "Anthropic_Api_Key=declared"\n'
    registry, errors = _registry(tmp_path, ROWS + ACCOUNTS + keyed)
    assert errors == []
    row = SimpleNamespace(**vars_of(registry["CLAUDE-A"]))
    if side == "route":
        row.env = "ANTHROPIC_API_KEY=declared"
    account = registry.accounts["KEYED"]
    _home(config_dir, "KEYED").mkdir(parents=True)
    with pytest.raises(svc.SigninRefused) as refused:
        svc.launch_env(tmp_path, row, account)
    assert "anthropic_api_key" in str(refused.value).lower()
    assert "login in its own home" in str(refused.value)
    ran = []
    status = svc.signin_status(
        tmp_path,
        account,
        row=row,
        run=lambda argv, env: ran.append(argv) or (0, '{"loggedIn": true}'),
    )
    assert (status, ran) == ("unknown", [])  # refused: never probed, never ready


def test_a_gemini_login_account_whose_route_declares_a_vertex_source_is_refused(
    tmp_path, config_dir
):
    registry, errors = _registry(tmp_path)
    assert errors == []
    row = SimpleNamespace(**vars_of(registry["GEMINI-A"]))
    row.env = "GOOGLE_GENAI_USE_VERTEXAI=true"
    account = registry.accounts["GE1"]
    _home(config_dir, "GE1").mkdir(parents=True)
    with pytest.raises(svc.SigninRefused) as refused:
        svc.launch_env(tmp_path, row, account)
    assert "GOOGLE_GENAI_USE_VERTEXAI" in str(refused.value)
    assert "login in its own home" in str(refused.value)


# --- TC-361 (round 3): a hand-authored name compares as the platform resolves it -----


@pytest.mark.parametrize("aid", ["WORK.", "A.B", "CON", "NUL", "COM1", "LPT9", "AUX"])
def test_an_account_id_a_platform_would_alias_is_a_registry_error(tmp_path, aid):
    table = '[account."{}"]\ncli = "claude"\nnotes = "x"\n'.format(aid)
    registry, errors = _registry(tmp_path, ROWS + table)
    named = [e for e in errors if "[account.{}]".format(aid) in e]
    assert named and "id outside" in named[0], errors
    assert registry.accounts == {}
    entries, errors = route.resolve_enabled(["CLAUDE-A@" + aid], registry)
    assert entries == [] and len(errors) == 1 and "not declared" in errors[0]


def test_two_ids_that_alias_one_windows_directory_cannot_both_load(tmp_path):
    tables = '[account.WORK]\ncli = "claude"\n\n[account."WORK."]\ncli = "claude"\n'
    registry, errors = _registry(tmp_path, ROWS + tables)
    assert list(registry.accounts) == ["WORK"]
    assert len(errors) == 1 and "[account.WORK.]" in errors[0]


def test_token_locators_the_platform_resolves_as_one_name_drop_both_accounts(tmp_path):
    tables = (
        '[account.T1]\ncli = "claude"\ntoken_file_variable = "X_TOKEN_FILE_798"\n'
        '[account.T2]\ncli = "claude"\ntoken_file_variable = "x_token_file_798"\n'
    )
    registry, errors = _registry(tmp_path, ROWS + tables)
    if os.name == "nt":  # one variable as Windows resolves it
        assert registry.accounts == {}
        assert len(errors) == 2
        assert "[account.T1]" in errors[0] and "X_TOKEN_FILE_798" in errors[0]
        assert "[account.T2]" in errors[1] and "x_token_file_798" in errors[1]
    else:  # two distinct variables on POSIX
        assert sorted(registry.accounts) == ["T1", "T2"] and errors == []


# --- TC-361 (round 3): account fields are type-checked before any lookup -------------


@pytest.mark.parametrize(
    "cells,key",
    [
        ("cli = []", "cli"),
        ("cli = {}", "cli"),
        ('cli = "claude"\ntoken_file_variable = 7', "token_file_variable"),
        ('cli = "claude"\nverified = true', "verified"),
        ("cli = 7", "cli"),
        ('cli = "claude"\nnotes = []', "notes"),
        ('cli = "claude"\nenv = {a = 1}', "env"),
    ],
)
def test_a_non_string_account_field_is_the_named_table_error(tmp_path, cells, key):
    table = "[account.BAD]\n{}\n".format(cells)
    registry, errors = _registry(tmp_path, ROWS + table)
    assert registry.accounts == {}
    assert len(errors) == 1 and "[account.BAD]" in errors[0], errors
    assert "non-string" in errors[0] and key in errors[0]
    docs = _docs(tmp_path, ROWS + table, enabled=["CLAUDE-A"])
    setup = loop.resolve_routing_setup(docs)  # never raises
    assert any("[account.BAD]" in e for e in setup.reg_errors)


@pytest.mark.parametrize("side", ["route", "account"])
def test_a_qualified_opencode_entry_declaring_its_auth_content_is_refused(
    tmp_path, config_dir, side
):
    keyed = '\n[account.OPAUTH]\ncli = "opencode"\nnotes = "k"\n'
    if side == "account":
        keyed += 'env = "Opencode_Auth_Content={}"\n'
    registry, errors = _registry(tmp_path, ROWS + ACCOUNTS + keyed)
    assert errors == []
    row = SimpleNamespace(**vars_of(registry["OPENCODE-A"]))
    if side == "route":
        row.env = "OPENCODE_AUTH_CONTENT={}"
    _home(config_dir, "OPAUTH").mkdir(parents=True)
    with pytest.raises(svc.SigninRefused) as refused:
        svc.launch_env(tmp_path, row, registry.accounts["OPAUTH"])
    assert "opencode_auth_content" in str(refused.value).lower()
    assert "login in its own home" in str(refused.value)
