"""The coordinator's act turn, and the loop's trailer line on every prompt the
entry point launches (WI-912).

A sitting ends at its committed verdict; its act is a later adjudicator turn
taken from that verdict (revision 32 of the review-churn plan, Q1). The `act`
command composes the act brief from the verdict accepted at the lane's HEAD,
launches it on the retained session where the `[adjudicator]` dial retains the
verdict's class and on a fresh one otherwise, and succeeds only when nothing
the verdict authorizes is left owed and nothing was written under
`docs/reviews/`. Under the loop marker, every prompt the entry point launches
ends with the loop's `Loop-Session` instruction (Q4).

No test calls a real model: the launch is `session_service.run_session`,
replaced by a stub "adjudicator" that takes the act the delivered brief lists
the way a session would (the flips, then the copy, each part committed), or
stops short of it. Each fixture is a primary checkout with one lane worktree
holding a claim, a spine, its recorded copy and a committed verdict.
"""

import json
import re
import shlex
import subprocess

import pytest
from conftest import hooks_on, load_script, pin_autocrlf, set_process_key

import test_adjudicate_act as taa

cli = load_script("coordinator_adjudicate")
svc = cli.session_service
agent_brief = load_script("agent_brief")
baseline_snapshot = taa.baseline_snapshot
from kitlib import provenance as kprovenance  # noqa: E402
from kitlib import sitting as ksitting  # noqa: E402

pytestmark = pytest.mark.usefixtures("retained_runners")

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
""".replace("{template}", TEMPLATE)
VERDICT = taa.VERDICT
WI = "WI-9"
RETAIN = '["amendment", "first-approval", "combined"]'
SESSION = "20261017T000000Z-abc123"


def _git(where, *args):
    proc = subprocess.run(
        ["git", "-C", str(where), *args],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _commit(lane, message):
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "-m", message)


def _dial(lane, retained):
    """The `[adjudicator]` dial: retaining the actable classes, or off."""
    path = lane / "docs" / "process.toml"
    text = path.read_text(encoding="utf-8")
    pct = "50" if retained else "0"
    text = text.replace(
        "context_reset_pct = 0 ", "context_reset_pct = {} ".format(pct), 1
    )
    text = re.sub(r"(?m)^retain_for = .*$", "retain_for = " + RETAIN, text, count=1)
    path.write_text(text, encoding="utf-8")


def _lane(tmp_path, dial="DevStg-Needs", retained=True):
    """A primary checkout and a lane worktree on `wi-1` claiming WI-9, with
    the spine seeded and recorded, the route enabled and the dials set, all
    committed. Returns `(primary, lane)`."""
    primary, lane = tmp_path / "primary", tmp_path / "lane"
    primary.mkdir(parents=True)
    _git(primary, "init", "-q", "-b", "trunk")
    hooks_on(primary)  # every route refuses a checkout without hooks
    pin_autocrlf(primary)
    _git(primary, "config", "user.email", "loop@example.com")
    _git(primary, "config", "user.name", "Loop Test")
    taa._write(primary, ".gitignore", "out/\n")
    _commit(primary, "base")
    _git(primary, "worktree", "add", "-q", "-b", "wi-1", str(lane))
    taa._write(lane, "docs/work/active/wi-1/WI-9-test.md", "+++\nid = 'WI-9'\n+++\n")
    taa._write(lane, taa.SRS, taa.SPINE_SRS)
    taa._write(lane, taa.LLRS, taa.SPINE_LLRS)
    taa._write(lane, taa.TCS, taa.SPINE_TCS)
    taa._write(lane, "docs/agents.toml", AGENTS)
    taa._write(lane, "docs/agents-enabled", ROUTE + "\n")
    set_process_key(lane, "attestation", "human_approval_through", dial)
    _dial(lane, retained)
    baseline_snapshot.copy_live(lane, seed=True)
    _commit(lane, "claim and seed")
    return primary, lane


def _combined(tmp_path, **kw):
    """A lane owing a combined act: SR-001 amended (CLARITY) and LLR-002
    drafted (APPROVE)."""
    primary, lane = _lane(tmp_path, **kw)
    taa._replace(lane, taa.SRS, "add two numbers.", "add two integers.")
    taa._append(lane, taa.LLRS, taa.NEW_LLR)
    _commit(lane, "amend SR-001, draft LLR-002")
    taa._verdict(lane, taa.COMBINED, "combined", taa.COMBINED_KINDS)
    return primary, lane


def _first_approval(tmp_path):
    primary, lane = _lane(tmp_path)
    taa._draft(lane)
    taa._verdict(lane, taa.FIRST_APPROVAL_MIXED, "first-approval")
    return primary, lane


def _amendment(tmp_path, **kw):
    primary, lane = _lane(tmp_path, **kw)
    taa._amend(lane)
    taa._verdict(lane, taa.AMENDMENT_CLARITY, "amendment")
    return primary, lane


def _stream(sid="S"):
    usage = {"input_tokens": 1000, "output_tokens": 1}
    return "\n".join(
        [
            json.dumps(
                {"type": "assistant", "message": {"model": "m", "usage": usage}}
            ),
            json.dumps(
                {
                    "type": "result",
                    "is_error": False,
                    "result": "acted",
                    "session_id": sid,
                    "usage": usage,
                    "modelUsage": {"m": {"contextWindow": 1000000}},
                }
            ),
        ]
    )


# --- the stub adjudicator: it takes what the delivered brief lists ----------


def _commands(prompt):
    return [
        shlex.split(line.strip())
        for line in prompt.splitlines()
        if line.strip().startswith("python scripts/intake.py snapshot")
    ]


def _reattest(lane, prompt):
    for argv in _commands(prompt):
        if "--reattests" in argv:
            verdict = argv[argv.index("--verdict") + 1] if "--verdict" in argv else None
            ids = baseline_snapshot.parse_reattests(argv[argv.index("--reattests") + 1])
            baseline_snapshot.copy_live(lane, reattests=ids, verdict=verdict)
            _commit(lane, "re-attest\n\nWI: {}".format(WI))


def _flip(lane, prompt):
    match = re.search(r"exactly these rows: (.*)\.\n", prompt)
    for rid in re.findall(r"([A-Z]+-\d+) \(", match.group(1)) if match else ():
        rel = taa.LLRS if rid.startswith("LLR") else taa.TCS
        text = (lane / rel).read_text(encoding="utf-8")
        line = next(ln for ln in text.splitlines() if ln.startswith(rid + ","))
        taa._replace(lane, rel, line, line.replace(",Drafted,", ",Approved,"))
    return bool(match)


def _approve(lane, prompt):
    if not _flip(lane, prompt):
        return
    for argv in _commands(prompt):
        if "--approves" in argv:
            approves = baseline_snapshot.parse_approves(
                argv[argv.index("--approves") + 1]
            )
            baseline_snapshot.copy_live(lane, approves=approves)
    _commit(lane, "approve\n\nWI: {}".format(WI))


def full(lane, prompt):
    _reattest(lane, prompt)
    _approve(lane, prompt)


def skip_flip(lane, prompt):
    _reattest(lane, prompt)


def flip_uncommitted(lane, prompt):
    _flip(lane, prompt)


def full_and_edit_verdict(lane, prompt):
    full(lane, prompt)
    taa._append(lane, VERDICT, "\nan afterthought\n")
    _commit(lane, "edit the verdict\n\nWI: {}".format(WI))


def nothing(lane, prompt):
    pass


@pytest.fixture
def launched(monkeypatch, tmp_path):
    """The launch replaced by the stub adjudicator; `seen["act"]` is what it
    does with each delivered prompt, `seen["prompts"]` what it received."""
    seen = {"prompts": [], "act": full}
    token = tmp_path / "token" / "claude-token"
    token.parent.mkdir()
    token.write_text("canary-token", encoding="utf-8")
    monkeypatch.setenv(svc.TOKEN_VARIABLES["ANTHROPIC"][0], str(token))
    monkeypatch.delenv(kprovenance.LOOP_SESSION_ENV, raising=False)

    def run(argv, root, timeout, **kw):
        prompt = kw.get("stdin_input") or ""
        seen["prompts"].append(prompt)
        seen["act"](seen["lane"], prompt)
        return 0, _stream(), False

    monkeypatch.setattr(svc, "run_session", run)
    monkeypatch.setattr(svc, "cli_version", lambda *a, **k: "")
    monkeypatch.setattr(svc, "signin_status", lambda root, family: "signed-in")
    return seen


def _act(seen, lane, *extra, root=None):
    seen["lane"] = lane
    return cli.main(
        ["act", "--root", str(root or lane), "--verdict", VERDICT, "--wi", WI, *extra]
    )


def _snapshot_of(lane):
    """What a refused call must leave untouched: HEAD and the working tree."""
    return _git(lane, "rev-parse", "HEAD"), _git(
        lane, "status", "--porcelain", "--untracked-files=all"
    )


# --- the pre-launch refusals (the Trust section's inputs) -------------------


def _primary_root(tmp_path, primary, lane):
    return primary


def _unclaimed_root(tmp_path, primary, lane):
    other = tmp_path / "other"
    _git(primary, "worktree", "add", "-q", "-b", "other", str(other))
    return other


def _no_repo_root(tmp_path, primary, lane):
    bare = tmp_path / "bare"
    bare.mkdir()
    return bare


def _route_off(tmp_path, primary, lane):
    return ("--route", "ANTHROPIC-OFF")


def _verdict_absent(tmp_path, primary, lane):
    _git(lane, "rm", "-q", VERDICT, ksitting.requested_path(VERDICT))
    _commit(lane, "drop the verdict")


def _no_binding(tmp_path, primary, lane):
    _git(lane, "rm", "-q", ksitting.requested_path(VERDICT))
    _commit(lane, "drop the binding")


def _outcome(word):
    def state(tmp_path, primary, lane):
        text = ksitting.render_requested("amendment", ("amendment",), word)
        taa._write(lane, ksitting.requested_path(VERDICT), text)
        _commit(lane, "binding " + word)

    return state


def _malformed(tmp_path, primary, lane):
    taa._write(lane, VERDICT, "- [CLARITY] SR-001 Requirement -> a\n")
    _commit(lane, "a malformed verdict")


def _owes_no_act(tmp_path, primary, lane):
    taa._take_amendment_act(lane, ["SR-001"])


def _inconsistent(tmp_path, primary, lane):
    # A re-attest of a row below Approved: no act explains it. (A row absent
    # from the committed tree is a retirement, not an inconsistent state.)
    taa._draft(lane)
    taa._write(
        lane,
        VERDICT,
        "- [CLARITY] LLR-002 Detail -> a -> a -> same\n\nVERDICT: CLARITY rows=1\n",
    )
    _commit(lane, "a verdict re-attesting a Drafted row")


def _dirty(tmp_path, primary, lane):
    taa._write(lane, "stray.txt", "left over\n")


@pytest.mark.parametrize(
    "state, words",
    [
        (_primary_root, "primary checkout"),
        (_unclaimed_root, "holds no claim"),
        (_no_repo_root, "not the top of a git worktree"),
        (_route_off, "not named on docs/agents-enabled"),
        (_verdict_absent, "not committed"),
        (_no_binding, "no binding"),
        (_outcome("pending"), "pending"),
        (_outcome("failed"), "failed"),
        (_malformed, "not a valid"),
        (_owes_no_act, "owes no act"),
        (_inconsistent, "LLR-002"),
        (_dirty, "stray.txt"),
    ],
)
def test_the_act_command_refuses_each_trust_input_before_launch(
    tmp_path, launched, capsys, state, words
):
    primary, lane = _amendment(tmp_path)
    got = state(tmp_path, primary, lane)
    root = got if hasattr(got, "is_dir") else None
    extra = got if isinstance(got, tuple) else ()
    before = _snapshot_of(lane)
    assert _act(launched, lane, *extra, root=root) == 2
    out = capsys.readouterr().out
    assert "act: refused:" in out and words in out, out
    assert launched["prompts"] == []
    assert _snapshot_of(lane) == before


# --- the act turn -----------------------------------------------------------


def _head_rows(lane):
    return {
        rel: _git(lane, "show", "HEAD:" + rel)
        for rel in (taa.SRS, "docs/archive/last_approved/" + taa.SRS)
    }


def test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict(
    tmp_path, launched, capsys
):
    results = {}
    for name, retained in (("kept", True), ("fresh", False)):
        _primary, lane = _amendment(tmp_path / name, retained=retained)
        assert _act(launched, lane) == 0
        results[name] = (capsys.readouterr().out, _head_rows(lane))
    kept_prompt, fresh_prompt = launched["prompts"]
    assert kept_prompt == fresh_prompt
    assert "keep: minting a retained session" in results["kept"][0]
    assert "keep: none" in results["fresh"][0]
    assert results["kept"][1] == results["fresh"][1]
    copy = results["kept"][1]["docs/archive/last_approved/" + taa.SRS]
    assert "add two integers." in copy
    assert "act: complete" in results["kept"][0]


def test_a_combined_act_commits_its_amendment_act_before_its_first_approval_act(
    tmp_path, launched
):
    _primary, lane = _combined(tmp_path)
    assert _act(launched, lane) == 0
    subjects = _git(lane, "log", "--format=%s", "-4").splitlines()
    acts = [s for s in subjects if s in ("re-attest", "approve")]
    assert acts == ["approve", "re-attest"]  # newest first


def test_the_act_turn_reports_success_only_when_no_listed_act_is_left(
    tmp_path, launched, capsys
):
    _primary, lane = _combined(tmp_path)
    launched["act"] = skip_flip
    assert _act(launched, lane) == 1
    out = capsys.readouterr().out
    assert "act: owed after the call:" in out and "LLR-002" in out, out


def test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed(
    tmp_path, launched, capsys
):
    _primary, lane = _combined(tmp_path)
    launched["act"] = full_and_edit_verdict
    assert _act(launched, lane) == 1
    out = capsys.readouterr().out
    assert "act: wrote under docs/reviews:" in out and VERDICT in out, out


def test_an_act_interrupted_between_flip_and_snapshot_is_refused_dirty_then_rerun_in_full(
    tmp_path, launched, capsys
):
    _primary, lane = _first_approval(tmp_path)
    launched["act"] = flip_uncommitted
    assert _act(launched, lane) == 1
    assert _act(launched, lane) == 2
    out = capsys.readouterr().out
    assert taa.LLRS in out, out
    assert len(launched["prompts"]) == 1
    _git(lane, "checkout", "--", ".")
    launched["act"] = full
    assert _act(launched, lane) == 0
    assert launched["prompts"][1] == launched["prompts"][0]
    assert "LLR-002" in launched["prompts"][1]


def test_a_combined_act_interrupted_between_commits_reruns_with_only_its_first_approval_act(
    tmp_path, launched
):
    _primary, lane = _combined(tmp_path)
    launched["act"] = skip_flip
    assert _act(launched, lane) == 1
    launched["act"] = full
    assert _act(launched, lane) == 0
    first, second = launched["prompts"]
    assert ["--reattests" in argv for argv in _commands(first)] == [True, False]
    (only,) = _commands(second)
    assert "--approves" in only
    assert _amendment_part(second) == cli.adjudicate_act.NONE_OWED


def _amendment_part(prompt):
    """The rendered amendment act of a delivered act brief."""
    part = prompt.split("--- 1. THE AMENDMENT ACT (re-attestation) ---\n", 1)[1]
    return part.split("\n--- 2.", 1)[0]


def test_the_act_turn_writes_no_binding_and_reserves_no_path(tmp_path, launched):
    _primary, lane = _combined(tmp_path)
    before = _git(lane, "ls-files", "docs/reviews")
    binding = _git(lane, "show", "HEAD:" + ksitting.requested_path(VERDICT))
    assert _act(launched, lane) == 0
    assert _git(lane, "ls-files", "docs/reviews") == before
    assert _git(lane, "show", "HEAD:" + ksitting.requested_path(VERDICT)) == binding
    assert not _git(lane, "status", "--porcelain", "--untracked-files=all")


# --- the trailer line (Q4) --------------------------------------------------

BRIEF_TEXT = {
    "combined": "Judge each section.\n\nSITTING: JUDGED kinds=amendment\n",
    "dispute": "Rule each finding.\n\nDISPUTE: findings=F1\n",
}


def _launch(launched, lane, brief, n):
    """One launch of `brief` (an adjudication class, or `act`) from the lane;
    returns the brief the entry point composed or read."""
    if brief == "act":
        text, why = cli.adjudicate_act.compose_act(lane, VERDICT, WI)
        assert why is None, why
        _act(launched, lane)
        return text
    text = BRIEF_TEXT.get(brief, "Judge the rows.\n")
    path = lane.parent / "brief-{}.md".format(n)
    path.write_text(text, encoding="utf-8")
    launched["lane"] = lane
    cli.main(
        ["adjudicate", "--root", str(lane), "--brief-file", str(path), "--brief"]
        + [brief, "--wi", WI, "--verdict", str(lane / "docs/reviews/wi-1/x.md")]
    )
    return text


CLASSES = sorted(cli.adjudicate_brief.BRIEF_PROMPTS) + ["act"]


@pytest.mark.parametrize("brief", CLASSES)
def test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line(
    tmp_path, launched, monkeypatch, brief
):
    _primary, lane = _amendment(tmp_path)
    launched["act"] = nothing if brief != "act" else full
    monkeypatch.setenv(kprovenance.LOOP_SESSION_ENV, SESSION)
    note = agent_brief.loop_provenance_note()
    assert note and "Loop-Session: " + SESSION in note
    _launch(launched, lane, brief, 1)
    (prompt,) = launched["prompts"]
    assert prompt.endswith(note), prompt[-300:]


@pytest.mark.parametrize("brief", CLASSES)
def test_without_the_marker_no_prompt_carries_the_line(tmp_path, launched, brief):
    _primary, lane = _amendment(tmp_path)
    launched["act"] = nothing if brief != "act" else full
    composed = _launch(launched, lane, brief, 1)
    (prompt,) = launched["prompts"]
    assert prompt == composed
    assert "Loop-Session" not in prompt
