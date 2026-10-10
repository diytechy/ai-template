"""The blackout window pauses lanes on both routes (WI-834 part B).

One window function (`agent_policy.blackout_at`) is the only reader of
`[policies] blackout`; the claim, the session service's launch boundary, the
coordinator guard's hooks and the retained adjudicator's retirement all ask
it. Driven in-process with the window's clock replaced (`agent_policy._utcnow`)
over a temporary repository; the subprocess and launcher routes are in
test_run_devsetup.py.
"""

import datetime
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from conftest import load_script

guard = load_script("coordinator_guard")
integ = load_script("integrate")
svc = load_script("session_service")
keep = load_script("session_keep")
loop = load_script("agent_loop")
coadj = load_script("coordinator_adjudicate")
# The modules the scripts above imported: the one clock every caller reads.
POLICY = sys.modules["agent_policy"]
DISPUTE = sys.modules["kitlib.dispute"]  # the one dispute-verdict parser

WINDOW = "12:00-19:00"
MON = datetime.datetime(2026, 7, 13)  # a Monday
INSIDE = MON.replace(hour=14)
END = MON.replace(hour=19)
AFTER = MON.replace(hour=20)
COORD = "c0c0c0c0-0000-4000-8000-0000000000b1"
HANDOFF = "# Handoff\n\n## Session prompt\n\n```text\nYou are the coordinator.\n```\n"
AGENTS = (
    '[agent.ANTHROPIC-ROUTE]\nfamily = "ANTHROPIC"\nmodel = "m"\nversion = "1"\n'
    'tier = "strong"\ncmd_template = "claude -p --model {model}"\nenv = ""\n'
    'notes = "test row"\n\n'
    '[agent.OPENAI-ROUTE]\nfamily = "OPENAI"\nmodel = "m"\nversion = "1"\n'
    'tier = "strong"\ncmd_template = "codex exec --model {model}"\nenv = ""\n'
    'notes = "test row"\n'
)


def write_policy(root, blackout=WINDOW, guard_pct=0, reset_pct=0):
    docs = Path(root) / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "process.toml").write_text(
        '[policies]\nblackout = "{}"\n\n[adjudicator]\ncontext_reset_pct = {}\n'
        "keepwarm_minutes = 50\n\n[coordinator]\ncontext_guard_pct = {}\n"
        "context_window_tokens = 1000\n".format(blackout, reset_pct, guard_pct),
        encoding="utf-8",
    )


@pytest.fixture
def clock(monkeypatch):
    """Set the window's clock: `clock(dt)`."""
    state = {"now": INSIDE}
    monkeypatch.setattr(POLICY, "_utcnow", lambda: state["now"])

    def set_now(now):
        state["now"] = now

    return set_now


@pytest.fixture
def root(tmp_path, clock):
    root = tmp_path / "repo"
    write_policy(root)
    (root / "docs" / "agents.toml").write_text(AGENTS, encoding="utf-8")
    return root


def at(docs, t):
    return POLICY.blackout_at(Path(docs), t)


# --- the one window function -------------------------------------------------------


def test_the_end_minute_is_exclusive_and_the_last_end_inclusive(root):
    docs = root / "docs"
    assert at(docs, MON.replace(hour=11, minute=59)).inside is False
    inside = at(docs, MON.replace(hour=12))
    assert inside.end == END and inside.wake_seconds == 7 * 3600
    last_minute = at(docs, MON.replace(hour=18, minute=59, second=30))
    assert last_minute.end == END and last_minute.wake_seconds == 30
    at_end = at(docs, END)
    assert at_end.inside is False and at_end.last_end == END  # inclusive
    assert at(docs, END - datetime.timedelta(seconds=1)).last_end == END.replace(
        day=10
    )  # the Friday before: Monday's has not ended yet


def test_a_friday_night_window_runs_into_saturday(tmp_path):
    write_policy(tmp_path, blackout="22:00-06:00")
    fri = datetime.datetime(2026, 7, 17)  # a Friday
    sat_two = fri + datetime.timedelta(days=1, hours=2)
    reading = at(tmp_path / "docs", sat_two)
    assert reading.inside and reading.end == fri + datetime.timedelta(days=1, hours=6)


def test_a_sunday_night_window_does_not_exist(tmp_path):
    write_policy(tmp_path, blackout="22:00-06:00")
    sun_late = datetime.datetime(2026, 7, 19, 23)  # a Sunday
    mon_two = datetime.datetime(2026, 7, 20, 2)
    assert at(tmp_path / "docs", sun_late).inside is False
    reading = at(tmp_path / "docs", mon_two)
    assert reading.inside is False
    assert reading.last_end == datetime.datetime(2026, 7, 18, 6)  # Saturday 06:00


def test_a_weekend_daytime_is_clear_and_remembers_fridays_end(root):
    sat_noon = datetime.datetime(2026, 7, 18, 14)
    reading = at(root / "docs", sat_noon)
    assert reading.inside is False
    assert reading.last_end == datetime.datetime(2026, 7, 17, 19)


@pytest.mark.parametrize("value", ["", "12:00-12:00", "garbage", "24:00-19:00"])
def test_a_disabled_window_answers_neither_question(tmp_path, value):
    write_policy(tmp_path, blackout=value)
    reading = at(tmp_path / "docs", INSIDE)
    assert (reading.inside, reading.last_end, reading.window) == (False, None, value)


def test_a_changed_value_applies_from_the_next_call(root):
    assert at(root / "docs", INSIDE).inside
    write_policy(root, blackout="")
    assert not at(root / "docs", INSIDE).inside
    write_policy(root, blackout="13:00-15:00")
    assert at(root / "docs", INSIDE).end == MON.replace(hour=15)


def test_the_window_function_is_the_only_reader_of_the_dial():
    """No kit script names the dial's key or legacy file but the policy
    module that defines the window function (the migration tables excepted:
    bootstrap's converter and the key table are not readers)."""
    scripts = Path(guard.__file__).parent
    readers = []
    for path in sorted(scripts.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if "declared_policy(" in text and '"blackout"' in text:
            readers.append(path.stem)
    assert readers == ["agent_policy"]


# --- claims: every route, the dispatcher's included --------------------------------


def test_a_claim_inside_the_window_is_refused_with_the_guard_off(root, clock):
    refusal = guard.claim_refusal(root, env={})
    assert "blackout window 12:00-19:00 UTC is open until 2026-07-13 19:00" in refusal
    clock(AFTER)
    assert guard.claim_refusal(root, env={}) is None  # guard off: unchanged


def test_the_dispatchers_claim_is_refused_inside_the_window(root, monkeypatch, capsys):
    def boom(*a, **k):
        raise AssertionError("the dispatcher's route consulted the context guard")

    monkeypatch.setattr(integ.coordinator_guard, "claim_refusal", boom)
    code = integ.claim(root, ["WI-001"], "wi-001", dispatch_lock_held=True)
    assert code != 0
    assert "no work item is claimed inside it" in capsys.readouterr().err


def test_the_dispatchers_context_guard_exemption_is_unchanged(tmp_path, clock):
    root = tmp_path / "repo"
    write_policy(root, guard_pct=50)  # on, and no lease is held
    clock(AFTER)
    assert "no coordinator lease is held" in guard.claim_refusal(root, env={})
    assert guard.window_refusal(root) is None  # the dispatcher's whole check


def test_the_dispatcher_holds_its_claim_and_waits_out_an_idle_window(root, monkeypatch):
    dispatch = load_script("dispatch")
    waits, said = [], []
    monkeypatch.setattr(dispatch.ac, "blackout_wait", lambda *a: waits.append(a[:3]))
    monkeypatch.setattr(dispatch, "_say", lambda msg, err=False: said.append(msg))
    state = {}
    assert dispatch._blackout_hold(root, True, state) is True  # lanes live
    assert dispatch._blackout_hold(root, True, state) is True
    assert len(said) == 1 and waits == []  # said once, nothing waited
    assert dispatch._blackout_hold(root, False, state) is True  # idle station
    assert waits == [(5 * 3600, WINDOW, END)]


# --- the session service's launch boundary ------------------------------------------


def _ran():
    calls = []

    def run(argv, root, timeout, **kw):
        calls.append(argv)
        return 0, '{"type":"result","result":"ok"}', False

    return calls, run


def active_claim(root, wi="WI-7"):
    spec = root / "docs" / "work" / "active" / wi.lower() / "{}-x.md".format(wi)
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(
        '+++\nid = "{}"\ntitle = "x"\nworkstream = "process"\nsr_refs = ["SR-1"]\n'
        'buildtier = "medium"\nsafety_class = "ordinary"\npriority = 1\n+++\n\n'
        "## Context\n\nx\n".format(wi),
        encoding="utf-8",
    )


def call(root, role, run, wi=""):
    return svc.Call(
        root=root, role=role, template="claude -p", model="m", runner=run, wi=wi
    )


@pytest.mark.parametrize("role", ["BUILD", "REVIEW", "PROBE", "KEEP-WARM", "PLAN"])
def test_a_non_adjudication_launch_is_refused_inside_the_window(root, role):
    active_claim(root)
    calls, run = _ran()
    with pytest.raises(svc.BlackoutRefused, match="open until 2026-07-13 19:00"):
        svc.act(call(root, role, run, wi="WI-7"))
    assert calls == []


def test_an_adjudication_without_an_active_claim_is_refused(root):
    calls, run = _ran()
    with pytest.raises(svc.BlackoutRefused):
        svc.act(call(root, "ADJUDICATE", run, wi="WI-7"))  # no claim at all
    active_claim(root)
    with pytest.raises(svc.BlackoutRefused):
        svc.act(call(root, "ADJUDICATE", run))  # no work item named
    assert calls == []


def test_a_wrap_up_adjudication_of_an_active_claim_launches(root):
    active_claim(root)
    calls, run = _ran()
    svc.act(call(root, "ADJUDICATE", run, wi="WI-7"))
    assert len(calls) == 1


def test_a_refused_call_records_nothing(root, monkeypatch):
    written = []
    monkeypatch.setattr(svc, "record", lambda *a, **k: written.append(a))
    calls, run = _ran()
    with pytest.raises(svc.BlackoutRefused):
        svc.call(call(root, "BUILD", run))
    assert calls == [] and written == []


def test_the_loop_waits_out_a_refused_launch_and_resumes_after_it(root, clock):
    """The loop's route: a lane claimed before the window starts no session
    inside it; the refusal is waited out and the launch resumes."""
    calls, run = _ran()
    waited = []

    def sleep(seconds):
        waited.append(seconds)
        clock(AFTER)

    outcome = svc.through_blackout(
        lambda: svc.act(call(root, "BUILD", run)), emit=lambda line: None, sleep=sleep
    )
    assert outcome.code == 0 and len(calls) == 1
    assert sum(waited) == 5 * 3600


def test_the_loops_pre_session_wait_asks_the_window_function(root, monkeypatch):
    waits = []
    monkeypatch.setattr(loop, "blackout_wait", lambda *a: waits.append(a[:3]))
    loop.wait_out_blackout(root / "docs")
    assert waits == [(5 * 3600, WINDOW, END)]


def test_the_coordinators_adjudication_reports_a_refusal(root, monkeypatch, capsys):
    """The coordinator's route: a refused launch is reported, its verdict
    reservation released, and nothing waits."""
    released = []
    monkeypatch.setattr(coadj, "_inputs", lambda r, a: (_Row(), "brief", None))
    monkeypatch.setattr(coadj, "_release", released.append)
    monkeypatch.setattr(svc, "adjudication_keep", lambda request: None)
    args = _Args(root)
    assert coadj.adjudicate(args) == coadj.agent_common.EXIT_PREFLIGHT
    assert released == [args.verdict]
    assert "blackout window" in capsys.readouterr().out


class _Row:
    id = "ANTHROPIC-ROUTE"
    family = "ANTHROPIC"
    model = "m"
    tier = "strong"
    cmd_template = "claude -p"
    env = ""


class _Args:
    def __init__(self, root):
        self.root = str(root)
        self.brief = "disposition"
        self.wi = "WI-404"  # no active claim
        self.verdict = str(Path(root) / "verdict.md")
        self.timeout = 60


@pytest.fixture
def waited(clock, monkeypatch):
    """The loop's wait on the controlled clock: what `through_blackout` sleeps
    advances the window's clock from INSIDE, so the window ends when the wait
    does. Returns the seconds slept."""
    slept = []

    def sleep(seconds):
        slept.append(seconds)
        clock(INSIDE + datetime.timedelta(seconds=sum(slept)))

    quiet = (lambda line: None, sleep)
    monkeypatch.setattr(loop.session_service.through_blackout, "__defaults__", quiet)
    return slept


@pytest.fixture
def runner(monkeypatch):
    """The outermost external model runner, the one substitute on the loop's
    routes: it records the window's clock at each launch it is handed."""
    launched = []

    def run(argv, root, timeout, **kw):
        launched.append(POLICY._utcnow())
        return 0, '{"type":"result","result":"OK"}', False

    monkeypatch.setattr(loop.session_service, "run_session", run)
    monkeypatch.setattr(loop.session_service, "run_attached", run)
    return launched


def test_each_loop_route_waits_out_a_refused_launch_and_retries(
    root, clock, waited, runner
):
    """The loop's three launch routes, each driven whole through a refusal: a
    worker session, the interactive sitting and a recovery probe each wait
    the window out to its end and then launch once."""
    ctx = SimpleNamespace(
        root=root,
        args=SimpleNamespace(
            no_session_echo=True, session_timeout=60, session_idle_timeout=0
        ),
        worker={"train": "t", "base": "b"},
        use_live=False,
        status_path=root / "docs" / "status.md",
        registry={},
        prompt_templates={},
    )
    plan = {"phase": "BUILD", "tmpl": "claude -p", "model": "m", "prompt": "go"}
    plan.update(
        route_family="ANTHROPIC", route_tier="strong", route_id="", session_env=None
    )
    interactive = SimpleNamespace(interactive_cmd="claude -p", model="m")
    routes = [
        ("launch_session", lambda: loop.launch_session(ctx, plan, "WI-7").code, 0),
        (
            "run_interactive",
            lambda: loop.run_interactive(interactive, root, {}, {}, "", "none", []),
            0,
        ),
        ("probe_route", lambda: loop.probe_route(_Row(), root)[0], True),
    ]
    for name, launch, answer in routes:
        clock(INSIDE)
        waited.clear()
        runner.clear()
        assert (launch(), sum(waited), runner) == (answer, 5 * 3600, [END]), name


def test_a_refused_retained_call_releases_its_lease(root, clock, retained):
    """A retained call the window refuses releases its lease and keeps its
    session's record, then raises: the retry after the window plans afresh."""
    cfg, prepared = retained
    seed(root, MON.replace(hour=11))
    kept = first_keep(root, cfg, prepared)  # inside: the lease is taken
    assert kept.session_id == "S1" and "lease" in state(root)
    calls, run = _ran()
    refused = svc.Call(
        root=root, role="ADJUDICATE", runner=run, wi="WI-7", keep=kept
    )  # no active claim: not a wrap-up
    with pytest.raises(svc.BlackoutRefused):
        svc.act(refused)
    assert calls == []
    after = state(root)
    assert "lease" not in after and after["session_id"] == "S1"


# --- the hooks: guard off, a window open -----------------------------------------


def ev(event, session=COORD, **extra):
    payload = {"hook_event_name": event, "session_id": session, "cwd": "."}
    payload.update(extra)
    return payload


def denial(out):
    spec = (out or {}).get("hookSpecificOutput") or {}
    return spec.get("permissionDecision") == "deny"


def bash(command, tool="Bash"):
    return ev("PreToolUse", tool_name=tool, tool_input={"command": command})


DENIED = [
    ev("PreToolUse", tool_name="Agent", tool_input={"prompt": "x"}),
    ev("PreToolUse", tool_name="SendMessage", tool_input={"to": "a1"}),
    bash("claude -p 'judge'"),
    bash("codex exec --model m"),
    bash("timeout 600 codex exec -"),
    bash("timeout -k 5 600 claude -p x"),
    bash("env -u BAR FOO=1 claude -p x"),
    bash("FOO=bar BAZ=1 codex exec"),
    bash("git status && claude -p x"),
    bash("false || codex exec"),
    bash("cd lane; claude -p x"),
    bash("cat brief.md | codex exec -"),
    bash('/usr/local/bin/claude -p "x"'),
    bash('& "C:\\Tools\\codex.exe" exec --model m', tool="PowerShell"),
]
ALLOWED = [
    bash("git status && python -m pytest -q"),
    bash("echo claude codex"),
    bash("grep -n claude docs/agents.toml"),
    bash("python scripts/coordinator_adjudicate.py adjudicate --wi WI-7"),
    ev("PreToolUse", tool_name="Read", tool_input={"file_path": "x"}),
]


@pytest.mark.parametrize("payload", DENIED)
def test_the_hooks_deny_each_launch_form_with_the_guard_off(root, payload):
    out = guard.hook(payload, root, env={})
    assert denial(out)
    assert "19:00 UTC" in out["hookSpecificOutput"]["permissionDecisionReason"]


@pytest.mark.parametrize("payload", ALLOWED)
def test_the_hooks_allow_everything_else(root, payload):
    assert not denial(guard.hook(payload, root, env={}))


# The command line is read with its shell's quoting (REVIEW-A F1): a quoted
# assignment value is one word, env's split string is itself a command line, a
# substitution's command runs, and a quoted operator, a comment or a
# here-document body is not a command boundary. One test per direction, each
# naming every case it gets wrong (the smoke tier's membership budget).
QUOTED_DENIED = [
    ('FOO="two words" claude -p x', "Bash"),
    ("env -S 'claude -p x'", "Bash"),
    ("env --split-string='FOO=1 codex exec -'", "Bash"),
    ("env -i -S'claude -p' x", "Bash"),
    ("timeout --signal=KILL 600 'codex' exec", "Bash"),
    ("echo ';' && claude -p x", "Bash"),
    ("out=$(claude -p q)", "Bash"),
    ('echo "$(codex exec -)"', "Bash"),
    ("if true; then claude -p x; fi", "Bash"),
    ("python -m pytest 2>&1 | codex exec -", "Bash"),
    ("cat > notes.md <<'EOF'\nit's a note; codex later\nEOF\nclaude -p x", "Bash"),
    ("$env:FOO = 'a b'; claude -p x", "PowerShell"),
    ('& "C:\\Program Files\\codex.exe" exec', "PowerShell"),
    ("cat <<EOF\n$(\nclaude -p x\n)\nEOF", "Bash"),
    ("cat <<-EOF\n\t$(claude -p x)\n\tEOF", "Bash"),
    ("cat <<EOF\n`claude -p x`\nEOF", "Bash"),
    ('x="$(cat <<EOF\n$(claude -p x)\nEOF\n)"', "Bash"),
    ('Write-Output @"\n$(\nclaude -p x\n)\n"@', "PowerShell"),
    # A PowerShell assignment runs its right-hand command (round 016 F1,
    # dispute 017 ruled FIX): the ruling's table, plus `??=` and the operator
    # written against its target.
    ("$response = claude -p x", "PowerShell"),
    ("[string]$r = claude -p x", "PowerShell"),
    ("$a, $b = claude -p x", "PowerShell"),
    ("$r += claude -p x", "PowerShell"),
    ("$env:X = claude -p x", "PowerShell"),
    ("$r ??= codex exec -", "PowerShell"),
    ("$r=claude -p x", "PowerShell"),
    # Any assignment target, recognised by its operator (round 018 F1): the
    # review's three forms and further probes, a chained assignment included.
    ("$result.Answer = claude -p x", "PowerShell"),
    ("$answers[0] = claude -p x", "PowerShell"),
    ("[string[]]$answers = claude -p x", "PowerShell"),
    ("$a.b[1].c = codex exec -", "PowerShell"),
    ("[System.Collections.Generic.List[string]]$l = claude -p x", "PowerShell"),
    ("$h['k=v'] = claude -p x", "PowerShell"),
    ("$r =claude -p x", "PowerShell"),
    ("$a = $b = claude -p x", "PowerShell"),
    # An unquoted operator after a quoted piece of the same word (round 020
    # observation O1): quotedness is known per character, not per word.
    ("$h['answer']=claude -p x", "PowerShell"),
    ("$o.'Answer'=claude -p x", "PowerShell"),
    ('$o."A"=claude -p x', "PowerShell"),
    # PowerShell's dot invocation operator, like `&` (round 024 F1, dispute
    # 025 ruled FIX): direct, quoted name, captured.
    (". claude -p x", "PowerShell"),
    (". 'claude' -p x", "PowerShell"),
    ("$r = . claude -p x", "PowerShell"),
    # A Bash grammar word's own options are grammar too (round 028 F1, D-025,
    # under sitting 025's line): the timed or coprocess command is the word.
    ("time -p claude -p x", "Bash"),
    ("time -p codex exec -", "Bash"),
    ("time -- claude -p x", "Bash"),
    ("time -p -- claude -p x", "Bash"),
    ("coproc claude -p x", "Bash"),
    ("coproc NAME { claude -p x; }", "Bash"),
    # coproc takes its NAME before any compound command (round 030 F1,
    # dispute 031 ruled FIX, D-026).
    ("coproc WORK while claude -p x; do :; done", "Bash"),
    ("coproc WORK if codex exec -; then :; fi", "Bash"),
]
QUOTED_ALLOWED = [
    ("echo 'pause; claude notes'", "Bash"),
    ('echo "a && claude -p x | codex"', "Bash"),
    ("git commit -m 'stop; codex exec after the window'", "Bash"),
    ('FOO="two words" python -m pytest', "Bash"),
    ("echo hi # ; claude -p x", "Bash"),
    ("cat > handoff.md <<'EOF'\nNext: claude -p review; don't launch\nEOF", "Bash"),
    ("git commit -m \"$(cat <<'EOF'\nPause; claude resumes (later)\nEOF\n)\"", "Bash"),
    ("Write-Output 'it''s; claude'", "PowerShell"),
    ('Write-Output "x`"; claude"', "PowerShell"),
    ("git commit -m @'\nPause; claude's turn is over\n'@", "PowerShell"),
    ('cat <<"EOF"\n$(claude -p x)\nEOF', "Bash"),
    ("cat <<\\EOF\n$(claude -p x)\nEOF", "Bash"),
    ("cat <<-'EOF'\n\t$(claude -p x)\n\tEOF", "Bash"),
    ("Write-Output @'\n$(claude -p x)\n'@", "PowerShell"),
    # A quoted or variable right-hand side is a value, not a command (D-020).
    ("$r = 'claude -p x'", "PowerShell"),
    ('$r = "claude -p x"', "PowerShell"),
    ("$r='claude -p x'", "PowerShell"),
    ("$r = $other", "PowerShell"),
    ('$result.Answer = "claude -p x"', "PowerShell"),
    ("$answers[0] = 'claude -p x'", "PowerShell"),
    ("echo a = claude", "PowerShell"),
    ("$x -match 'a=claude'", "PowerShell"),
    (". ./setup.ps1", "PowerShell"),  # a dot-sourced script is not read into
    ("time -p echo ok", "Bash"),
    ("coproc NAME { echo ok; }", "Bash"),
    ("coproc CLAUDE while true; do echo ok; break; done", "Bash"),
    ("function f { claude; }", "Bash"),  # a definition runs nothing
]
UNREADABLE = [
    ("echo 'unbalanced; claude -p x", "Bash"),
    ('echo "$(claude -p x"', "Bash"),
    ("Write-Output 'unbalanced", "PowerShell"),
]


def _decisions(root, cases):
    return [
        (command, (guard.hook(bash(command, tool=tool), root, env={}) or {}))
        for command, tool in cases
    ]


def test_a_quoted_launch_form_is_denied(root):
    wrong = [c for c, out in _decisions(root, QUOTED_DENIED) if not denial(out)]
    assert wrong == []


def test_a_quoted_operator_is_not_a_command_boundary(root):
    wrong = [c for c, out in _decisions(root, QUOTED_ALLOWED) if denial(out)]
    assert wrong == []


def test_an_unreadable_command_line_is_denied_inside_the_window(root, clock):
    """A line the hook cannot read is refused, naming why, rather than read as
    no launch (decision D-010); outside the window it is not read at all."""
    for command, out in _decisions(root, UNREADABLE):
        reason = out.get("hookSpecificOutput", {}).get("permissionDecisionReason", "")
        assert denial(out) and "cannot read" in reason, command
    clock(AFTER)
    assert all(not out for _command, out in _decisions(root, UNREADABLE))


def test_the_one_reading_keeps_quoted_text_in_its_word():
    """`kitlib.shell_line.segments`, the hook's one reading of a command
    line: quotes stay inside their word, operators split only unquoted, and
    a substitution's command line is read as a further command."""
    segments = sys.modules["kitlib.shell_line"].segments
    assert segments('FOO="two words" claude -p x') == [
        ["FOO=two words", "claude", "-p", "x"]
    ]
    assert segments("echo 'a; b' && c 2>&1 > out") == [["echo", "a; b"], ["c"]]
    assert segments("x=$(claude -p q)") == [["x=$(claude -p q)"], ["claude", "-p", "q"]]
    assert segments("cat <<EOF\n'; x\nEOF\nnext") == [["cat"], ["next"]]
    assert segments("cat <<EOF\n'$(claude -p q)'\nEOF") == [
        ["cat"],
        ["claude", "-p", "q"],
    ]
    assert segments("Write-Output 'it''s'", "powershell") == [["Write-Output", "it's"]]


def test_a_json_array_template_names_its_cli(root):
    """The CLI names are read by the kit's one template reader, so the
    declared JSON-array form names its executable too."""
    (root / "docs" / "agents.toml").write_text(
        AGENTS.replace(
            'cmd_template = "codex exec --model {model}"',
            """cmd_template = '["C:/Tools/gpt runner.exe", "exec"]'""",
        ),
        encoding="utf-8",
    )
    assert guard.model_clis(root) == {"claude", "gpt runner"}


def test_a_subagents_call_is_never_denied(root):
    assert not denial(guard.hook({**bash("claude -p x"), "agent_id": "a1"}, root, {}))


def test_the_cli_names_come_from_the_route_registry(root):
    assert guard.model_clis(root) == {"claude", "codex"}
    (root / "docs" / "agents.toml").write_text(
        AGENTS.replace("codex exec", "gpt-runner exec"), encoding="utf-8"
    )
    assert guard.model_clis(root) == {"claude", "gpt-runner"}
    assert denial(guard.hook(bash("gpt-runner exec"), root, env={}))


def test_outside_the_window_with_the_guard_off_the_hooks_do_nothing(root, clock):
    clock(AFTER)
    for payload in DENIED + [ev("SessionStart"), ev("Stop")]:
        assert guard.hook(payload, root, env={}) is None


def test_session_start_and_the_monitored_events_tell_the_close_down(root):
    start = guard.hook(ev("SessionStart"), root, env={})
    text = start["hookSpecificOutput"]["additionalContext"]
    assert "BLACKOUT WINDOW" in text and "next obligation" in text
    assert "pause point" in text and "end the session" in text
    assert "no relaunch is requested" in text
    told = [
        guard.hook(ev("Stop"), root, env={}) for _ in range(guard.REMINDER_EVERY + 1)
    ]
    assert [t is not None for t in told] == (
        [True] + [False] * (guard.REMINDER_EVERY - 1) + [True]
    )


def test_the_window_check_subcommand_exits_nonzero_inside(root, clock, capsys):
    assert guard.main(["--root", str(root), "window-check"]) == 1
    assert "blackout window" in capsys.readouterr().err
    clock(AFTER)
    assert guard.main(["--root", str(root), "window-check"]) == 0


# --- the relaunch: neither written nor launched inside the window -----------------


def _held(root, tmp_path):
    transcript = tmp_path / "coord.jsonl"
    transcript.write_text("", encoding="utf-8")
    assert guard.take(root, COORD, str(transcript)) is None
    handoff = tmp_path / "handoff.md"
    handoff.write_text(HANDOFF, encoding="utf-8")
    return handoff


def test_no_relaunch_is_written_inside_the_window(tmp_path, clock):
    root = tmp_path / "repo"
    write_policy(root, guard_pct=50)
    handoff = _held(root, tmp_path)
    refusal = guard.request_relaunch(root, handoff, COORD)
    assert "no relaunch is requested inside it" in refusal
    assert not (guard.lease_dir(root) / "relaunch.json").exists()


@pytest.mark.parametrize("guard_pct", [0, 50])
def test_a_pending_relaunch_at_session_end_inside_the_window_is_cancelled(
    tmp_path, clock, guard_pct
):
    root = tmp_path / "repo"
    write_policy(root, guard_pct=50)
    handoff = _held(root, tmp_path)
    clock(AFTER)
    assert guard.request_relaunch(root, handoff, COORD) is None
    write_policy(root, guard_pct=guard_pct)
    clock(INSIDE)
    launched = []
    out = guard.hook(
        ev("SessionEnd", reason="prompt_input_exit"),
        root,
        env={},
        launch=lambda *a: launched.append(a),
    )
    directory = guard.lease_dir(root)
    assert out is None and launched == []
    assert not (directory / "relaunch.json").exists()
    assert len(list(directory.glob("relaunch.*.cancelled"))) == 1
    events = [
        json.loads(x)
        for x in (directory / "events.jsonl").read_text("utf-8").splitlines()
    ]
    assert events[-1]["event"] == "relaunch-cancelled"
    assert events[-1]["reason"] == "blackout"


def test_reopening_the_same_session_with_both_drains_needs_the_owners_clear(
    tmp_path, clock
):
    """The context latch tripped inside the window (round 035 F2): it is
    recorded, but a new latch and the latched holder's resumed start each get
    the one blackout close-down, never the relaunch request the window
    refuses; after the window the latch still needs the owner's clear."""
    root = tmp_path / "repo"
    write_policy(root, guard_pct=50)
    _held(root, tmp_path)
    usage = {"input_tokens": 600, "cache_creation_input_tokens": 0}
    usage.update(cache_read_input_tokens=0, output_tokens=5)
    record = {"parentUuid": None, "isSidechain": False, "uuid": "u-1"}
    record.update(sessionId=COORD, type="assistant")
    record["message"] = {"role": "assistant", "model": "m", "usage": usage}
    transcript = tmp_path / "coord.jsonl"
    transcript.write_text(json.dumps(record) + "\n", encoding="utf-8")  # 60%
    directory = guard.lease_dir(root)
    for event in ("PostToolUse", "SessionStart"):  # a new latch, then a resume
        payload = ev(event, transcript_path=str(transcript), tool_name="Read")
        said = guard.hook(payload, root, env={})["hookSpecificOutput"]
        text = said["additionalContext"]
        assert "request the relaunch" not in text, (event, text)
        assert "BLACKOUT WINDOW" in text and "no relaunch is" in text, (event, text)
        assert guard._load(directory).get("draining"), event
    transcript.write_text("", encoding="utf-8")  # the reopened session's fresh context
    env = {guard.SESSION_ENV: COORD}
    assert "blackout window" in guard.claim_refusal(root, env=env)
    clock(AFTER)  # the blackout drain ends with the clock ...
    assert "drain mode is latched" in guard.claim_refusal(root, env=env)
    assert guard.clear(root, "owner: resume after the window") is None
    assert guard.claim_refusal(root, env=env) is None  # ... the latch by the clear


# --- the pause point ------------------------------------------------------------------


@pytest.mark.parametrize("role", ["REVIEW", "BUILD", "CRITIQUE"])
def test_a_review_next_or_rework_launch_is_refused_for_an_active_claim(root, role):
    """A review, build or critique launch for a work item whose claim is
    active is refused inside the window: an active claim admits only a
    wrap-up adjudication."""
    active_claim(root)
    calls, run = _ran()
    with pytest.raises(svc.BlackoutRefused):
        svc.act(call(root, role, run, wi="WI-7"))
    assert calls == []


def _git(where, *args):
    proc = subprocess.run(
        ["git", "-C", str(where), "-c", "user.name=t", "-c", "user.email=t@t"]
        + ["-c", "core.hooksPath=no-hooks", "-c", "core.autocrlf=false", *args],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


@pytest.fixture
def paused_lane(tmp_path, clock):
    """A primary checkout whose trunk holds WI-7's active claim, and the
    lane worktree claimed before the window, whose last finished step (a
    review round asking for rework) is committed: its pause point."""
    primary, lane = tmp_path / "primary", tmp_path / "lane"
    primary.mkdir()
    _git(primary, "init", "-b", "trunk")
    active_claim(primary)
    _git(primary, "add", "docs")
    _git(primary, "commit", "-m", "claim: WI-7")
    _git(primary, "worktree", "add", "-b", "wi-7", str(lane))
    review = lane / "docs" / "reviews" / "wi-7" / "001-REVIEW-A-abc1234.md"
    review.parent.mkdir(parents=True)
    review.write_text(
        "- [MAJOR] x.py:1 -> a defect -> fix it -> @builder\n\n"
        "VERDICT: CHANGES-REQUESTED findings=1\n",
        encoding="utf-8",
    )
    _git(lane, "add", "docs")
    _git(lane, "commit", "-m", "WI-7: review round 1")
    write_policy(lane)  # retention off: the wrap-up rule needs no keep
    (lane / "docs" / "agents.toml").write_text(AGENTS, encoding="utf-8")
    (lane / "docs" / "agents-enabled").write_text("ANTHROPIC-ROUTE\n", "utf-8")
    return lane


def test_a_wrap_up_verdict_asking_for_rework_leaves_the_rework_waiting(
    paused_lane, clock, monkeypatch, capsys
):
    """On the coordinator's route inside the window: the lane's committed
    review round is its pause point; the wrap-up dispute adjudication of its
    active claim is admitted and rules the finding FIX; the rework that
    ruling asks for (the builder's subagent, a model CLI, the service's
    BUILD and REVIEW launches) is refused until the window ends, then
    admitted. Writing the handoff that names the obligation is the
    coordinator's prose, not code: the close-down instruction asking for it
    is pinned in test_session_start_and_the_monitored_events_tell_the_close_down."""
    lane = paused_lane
    assert _git(lane, "status", "--porcelain", "--", "docs/reviews") == ""
    service = coadj.session_service
    verdict = lane / "docs" / "reviews" / "wi-7" / "002-ADJUDICATE-abc1234.md"
    launched = []

    def run(argv, root_, timeout, **kw):
        launched.append(argv)
        verdict.write_text("RULING: F1 FIX the defect holds\n", encoding="utf-8")
        return 0, '{"type":"result","is_error":false,"result":"ok"}', False

    monkeypatch.setattr(service, "run_session", run)
    monkeypatch.setattr(service, "cli_version", lambda *a, **k: "")
    monkeypatch.setattr(service.agent_common, "commit_telemetry", lambda *a, **k: None)
    brief = lane / "brief.md"
    brief.write_text("Rule it.\n\nDISPUTE: findings=F1\n", encoding="utf-8")
    argv = ["adjudicate", "--root", str(lane), "--route", "ANTHROPIC-ROUTE"]
    argv += ["--brief-file", str(brief), "--brief", "dispute", "--wi", "WI-7"]
    assert coadj.main(argv + ["--verdict", str(verdict)]) == 0, capsys.readouterr()
    assert len(launched) == 1
    rulings, why = DISPUTE.parse(verdict.read_text(encoding="utf-8"), ["F1"])
    assert why is None and rulings["F1"][0] == "FIX"  # the rework is owed

    assert denial(guard.hook(ev("PreToolUse", tool_name="Agent"), lane, env={}))
    assert denial(guard.hook(bash("codex exec --model m -"), lane, env={}))
    calls, run_next = _ran()
    for role in ("BUILD", "REVIEW"):
        with pytest.raises(service.BlackoutRefused):
            service.act(call(lane, role, run_next, wi="WI-7"))
    assert calls == []
    clock(AFTER)
    service.act(call(lane, "BUILD", run_next, wi="WI-7"))
    assert len(calls) == 1


# --- retention across the window ---------------------------------------------------


@pytest.fixture
def retained(root, retained_runners, monkeypatch, tmp_path):
    token = tmp_path / "token"
    token.write_text("canary-token", encoding="utf-8")
    monkeypatch.setenv(svc.TOKEN_VARIABLES["ANTHROPIC"][0], str(token))
    write_policy(root, reset_pct=50)
    cfg = keep.keep_config(root)
    rows = svc.agent_route.load_registry(root / "docs" / "agents.toml")[0]
    prepared = svc.prepare_launch(root, rows["ANTHROPIC-ROUTE"])
    return cfg, prepared


def epoch(dt):
    return dt.replace(tzinfo=datetime.timezone.utc).timestamp()


def seed(root, last_used, state="active", **extra):
    record = {
        "family": "ANTHROPIC",
        "route_id": "ANTHROPIC-ROUTE",
        "session_id": "S1",
        "generation": 1,
        "state": state,
        "reset_reason": "",
        "judged": ["WI-9"],
    }
    if last_used is not None:
        record["last_used_epoch"] = epoch(last_used)
    record.update(extra)
    with keep.store_lock(root):
        keep.store_save(root, record)


def first_keep(root, cfg, prepared, rows=None):
    return keep.keep_for(
        root,
        cfg,
        role="ADJUDICATE",
        brief="disposition",
        family="ANTHROPIC",
        route_id="ANTHROPIC-ROUTE",
        wi="WI-7",
        rows=rows,
        lease_wait=0,
        prepared=prepared,
    )


def state(root):
    return keep.store_load(root, "ANTHROPIC", "ANTHROPIC-ROUTE")


@pytest.mark.parametrize(
    "last_used, retired",
    [
        (MON.replace(hour=18, minute=30), True),  # the wrap-up ended inside
        (END, False),  # exactly at its end
        (MON.replace(hour=19, minute=5), False),  # after it
        (None, True),  # no last-use time
    ],
)
def test_the_first_keep_call_after_a_window_retires_by_the_predicate(
    root, clock, retained, last_used, retired
):
    cfg, prepared = retained
    seed(root, last_used)
    clock(AFTER)
    kept = first_keep(root, cfg, prepared)
    assert (kept.session_id == "") is retired
    assert (state(root)["reset_reason"] == "blackout") is retired


def test_a_draining_sessions_chain_does_not_survive_the_window(root, clock, retained):
    cfg, prepared = retained
    seed(root, MON.replace(hour=11), state="draining", reset_reason="crest")
    rows = {"WI-9": {"Status": "active", "SafetyClass": "", "Predecessors": ""}}
    clock(AFTER)
    kept = first_keep(root, cfg, prepared, rows=rows)
    assert kept.session_id == "" and state(root)["reset_reason"] == "blackout"


def test_a_wrap_up_inside_the_window_resumes_the_retained_session(
    root, clock, retained
):
    cfg, prepared = retained
    seed(root, MON.replace(hour=11))  # used before this window, after Friday's
    kept = first_keep(root, cfg, prepared)  # inside: the wrap-up
    assert kept.session_id == "S1"


def test_no_keep_warm_ping_fires_inside_the_window(root, clock, retained):
    cfg, prepared = retained
    seed(root, MON.replace(hour=11))
    ping, reason = keep.take_warm_lease(
        root,
        cfg,
        now=epoch(INSIDE),
        work_pending=True,
        holder="keep-warm:x",
        prepare=lambda route_id: (prepared, ""),
    )
    assert (ping, reason) == (None, None)
    assert "lease" not in state(root)


def _wrap_up_across_the_end(root, cfg, prepared, clock, mp):
    """A wrap-up admitted at 18:59 whose call is still running at 19:01, when
    the dispatcher's real keep-warm tick runs; it is bookkept at 19:03. The
    window's clock and the store's clock are one. Returns the tick's lines and
    the record the tick left."""
    now = {}

    def set_now(dt):
        now["t"] = dt
        clock(dt)

    fake = SimpleNamespace(time=lambda: epoch(now["t"]), monotonic=lambda: 0.0)
    for module in (keep, svc.session_keep):  # the test's copy and the service's
        mp.setattr(module, "time", fake)
    mp.setattr(svc, "_now", lambda: now["t"].strftime("%Y-%m-%dT%H:%M:%SZ"))
    set_now(MON.replace(hour=18, minute=59))
    active_claim(root)
    rows = svc.agent_route.load_registry(root / "docs" / "agents.toml")[0]
    warmer = svc.KeepWarmer(
        root, cfg, rows, runner=None, clock=fake.time, dirty=lambda: False
    )
    seen = {}

    def run(argv, root_, timeout, **kw):
        set_now(MON.replace(hour=19, minute=1))  # the call is still running
        seen["lines"] = warmer.tick(work_pending=True)
        seen["record"] = state(root)
        set_now(MON.replace(hour=19, minute=3))  # and completes
        return 0, '{"type":"result","result":"ok","session_id":"S1"}', False

    kept = first_keep(root, cfg, prepared)
    assert kept.session_id == "S1"
    svc.act(svc.Call(root=root, role="ADJUDICATE", runner=run, wi="WI-7", keep=kept))
    assert warmer.thread is None  # no ping started
    set_now(MON.replace(hour=19, minute=10))
    return seen["lines"], seen["record"]


def test_a_keep_warm_tick_first_after_the_window_retires_and_never_refreshes(
    root, clock, retained
):
    cfg, prepared = retained
    seed(root, MON.replace(hour=11))
    # A tick meeting a session another call's live lease holds leaves it to
    # that call: the call's own last use (19:03) decides at the next keep.
    with pytest.MonkeyPatch.context() as mp:
        lines, during = _wrap_up_across_the_end(root, cfg, prepared, clock, mp)
        assert len(lines) == 1 and "the session is leased to" in lines[0]
        assert during["state"] == "active" and during["reset_reason"] == ""
        assert first_keep(root, cfg, prepared).session_id == "S1"
    clock(INSIDE)  # an unleased stale record, on the real store clock
    seed(root, MON.replace(hour=11))
    before = state(root)["last_used_epoch"]
    clock(AFTER)
    ping, reason = keep.take_warm_lease(
        root,
        cfg,
        now=epoch(AFTER),
        work_pending=True,
        holder="keep-warm:x",
        prepare=lambda route_id: (prepared, ""),
    )
    assert ping is None and reason is None
    after = state(root)
    assert after["state"] == "retired" and after["reset_reason"] == "blackout"
    assert after["last_used_epoch"] == before


# --- dev-setup's sign-in reading (part C, in-process) --------------------------------


def test_the_sign_in_reading_is_off_while_retention_is_off(root, capsys):
    args = coadj._parser().parse_args(["signin", "--root", str(root), "--retained"])
    assert coadj.signin(args) == 0
    assert capsys.readouterr().out.strip() == "signin [ANTHROPIC]: off"


def test_the_sign_in_reading_names_signed_in_and_missing(root, monkeypatch, capsys):
    write_policy(root, reset_pct=55)
    variable = svc.TOKEN_VARIABLES["ANTHROPIC"][0]
    monkeypatch.delenv(variable, raising=False)
    args = coadj._parser().parse_args(["signin", "--root", str(root), "--retained"])
    coadj.signin(args)
    assert capsys.readouterr().out.strip() == "signin [ANTHROPIC]: missing"
    token = root / "token"
    token.write_text("t", encoding="utf-8")
    monkeypatch.setenv(variable, str(token))
    coadj.signin(args)
    assert capsys.readouterr().out.strip() == "signin [ANTHROPIC]: signed-in"


# --- the hooks opt-in (part D, in-process) --------------------------------------------


GUARD_GROUP = {
    "hooks": [
        {
            "type": "command",
            "command": 'python "${CLAUDE_PROJECT_DIR}/scripts/coordinator_guard.py" hook',
        }
    ]
}


def example(tmp_path):
    path = tmp_path / "settings.json.example"
    path.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {"matcher": "Task|Agent", "hooks": [{"command": "gate"}]},
                        GUARD_GROUP,
                    ],
                    "SessionEnd": [GUARD_GROUP],
                }
            }
        ),
        encoding="utf-8",
    )
    return path


# The guard group as the opt-in installs it: run by the interpreter the
# opt-in itself runs on, never a bare `python` (round 016 F2, decision D-019).
BOUND_GROUP = {
    "hooks": [
        {
            "type": "command",
            "command": '"{}" "${{CLAUDE_PROJECT_DIR}}/scripts/coordinator_guard.py" hook'.format(
                Path(sys.executable).as_posix()
            ),
        }
    ]
}


def test_the_hook_opt_in_merges_and_keeps_existing_hooks(tmp_path):
    """The opt-in writes the machine-local settings file, binding each guard
    hook to this interpreter; it keeps the hooks already there, a re-run
    changes nothing, and the committed project settings are left alone. It
    owns the guard's commands, not whole groups (round 018 F2): a user
    command beside a guard command in one group keeps its place and its
    group's matcher, and only the guard's command moves to the bound group."""
    root = tmp_path / "repo"
    local = root / ".claude" / "settings.local.json"
    local.parent.mkdir(parents=True)
    # The example's own bare-`python` guard command is the guard's; a user
    # command that merely names the guard's file is not (round 020 O2).
    stale = dict(GUARD_GROUP["hooks"][0])
    user = {"type": "command", "command": "echo user-audit-notification"}
    lint = {
        "type": "command",
        "command": "ruff check project-trajectory/scripts/coordinator_guard.py",
    }
    mixed = {"matcher": "Bash", "hooks": [stale, user, lint]}
    mine = {
        "hooks": {"PreToolUse": [{"hooks": [{"command": "mine"}]}, mixed]},
        "x": 1,
    }
    local.write_text(json.dumps(mine), encoding="utf-8")
    shared = root / ".claude" / "settings.json"
    shared.write_text('{"hooks": {}}', encoding="utf-8")
    source = example(tmp_path)
    assert guard.hooks_state(root, source) == "off"
    guard.enable_hooks(root, source)
    guard.enable_hooks(root, source)  # idempotent
    merged = json.loads(local.read_text(encoding="utf-8"))
    assert merged["x"] == 1
    assert merged["hooks"]["PreToolUse"] == [
        mine["hooks"]["PreToolUse"][0],
        {"matcher": "Bash", "hooks": [user, lint]},
        BOUND_GROUP,
    ]
    assert merged["hooks"]["SessionEnd"] == [BOUND_GROUP]
    assert guard.hooks_state(root, source) == "on"
    assert shared.read_text(encoding="utf-8") == '{"hooks": {}}'


def test_the_hook_opt_in_with_no_guard_hooks_changes_nothing(tmp_path, capsys):
    root = tmp_path / "repo"
    root.mkdir()
    source = tmp_path / "plain.example"
    source.write_text('{"hooks": {"Stop": [{"hooks": [{"command": "x"}]}]}}', "utf-8")
    assert (
        guard.main(["--root", str(root), "hooks", "--example", str(source), "--enable"])
        == 0
    )
    assert capsys.readouterr().out.strip() == "none"
    assert not (root / ".claude").exists()
