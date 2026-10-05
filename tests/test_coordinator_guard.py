"""The coordinator context guard (WI-822): occupancy, the lease, the drain
latch, the claim boundary, the hooks and the relaunch, all in-process.

The built transcripts use the record shapes of a Claude Code 2.1.285
transcript (`CLAUDE_CODE_VERSION`, stamped into each record the way a real one
carries it): the assistant record and its `message.usage`, and the
`parentUuid` chain. The compaction case is also read from a RECORDED fixture,
`fixtures/coordinator_guard/compaction-manual-2.1.289.jsonl`: a real two-turn
Claude Code 2.1.289 session, a manual `/compact`, then one more turn,
sanitized (neutral paths and identity; attachment text over 2,000 characters
replaced by same-length filler) with every record shape, field and usage
number otherwise kept. Its boundary is `type: system`, `subtype:
compact_boundary`, `parentUuid: null`, and the messages it preserves are named
by uuid in `compactMetadata.preservedMessages`, not written again after it.
Subprocess routes (the CLI, a wrapper, the launchers, real git close-out) are
in test_coordinator_guard_e2e.py.
"""

import ast
import json
import threading
from pathlib import Path

import pytest

from conftest import ROOT, SCRIPTS, load_script

RECORDED = Path(__file__).parent / "fixtures" / "coordinator_guard"
REAL_COMPACTION = RECORDED / "compaction-manual-2.1.289.jsonl"

guard = load_script("coordinator_guard")
integ = load_script("integrate")

CLAUDE_CODE_VERSION = "2.1.285"
COORD = "c0c0c0c0-0000-4000-8000-000000000001"
OTHER = "0be70be7-0000-4000-8000-000000000002"
WINDOW = 1000


# --- transcript fixtures -------------------------------------------------------


class Transcript:
    """A version-stamped transcript builder: each record names its parent."""

    def __init__(self, path, session=COORD):
        self.path = Path(path)
        self.session = session
        self.records = []
        self.n = 0

    def _add(self, record, parent="last"):
        self.n += 1
        uid = "u-{:04d}".format(self.n)
        if parent == "last":
            parent = self.records[-1]["uuid"] if self.records else None
        base = {
            "parentUuid": parent,
            "isSidechain": False,
            "uuid": uid,
            "sessionId": self.session,
            "version": CLAUDE_CODE_VERSION,
        }
        base.update(record)
        self.records.append(base)
        self.write()
        return uid

    def user(self, parent="last"):
        return self._add({"type": "user", "message": {"role": "user"}}, parent)

    def reply(self, inp, read=0, create=0, parent="last", **extra):
        usage = {
            "input_tokens": inp,
            "cache_creation_input_tokens": create,
            "cache_read_input_tokens": read,
            "output_tokens": 5,
        }
        message = {"model": "claude-opus-5-5", "role": "assistant", "usage": usage}
        message.update(extra)
        return self._add({"type": "assistant", "message": message}, parent)

    def boundary(self):
        return self._add(
            {
                "type": "system",
                "subtype": "compact_boundary",
                "compactMetadata": {"trigger": "auto"},
            },
            parent=None,
        )

    def raw(self, record):
        self.records.append(record)
        self.write()

    def write(self, tail=""):
        text = "".join(json.dumps(r) + "\n" for r in self.records)
        self.path.write_text(text + tail, encoding="utf-8")


def make_root(tmp_path, pct=50, window=WINDOW):
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "process.toml").write_text(
        "[coordinator]\ncontext_guard_pct = {}\ncontext_window_tokens = {}\n".format(
            pct, window
        ),
        encoding="utf-8",
    )
    return root


@pytest.fixture
def root(tmp_path):
    return make_root(tmp_path)


@pytest.fixture
def tx(tmp_path):
    t = Transcript(tmp_path / "coord.jsonl")
    t.user()
    t.reply(100, read=50, create=50)  # 200 tokens = 20%
    return t


def held(root, tx):
    assert guard.take(root, COORD, str(tx.path)) is None
    return guard._load(guard.lease_dir(root))


def ev(event, session=COORD, transcript=None, **extra):
    payload = {
        "hook_event_name": event,
        "session_id": session,
        "transcript_path": str(transcript) if transcript else None,
        "cwd": ".",
    }
    payload.update(extra)
    return payload


def events(root):
    path = guard.lease_dir(root) / "events.jsonl"
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]


ENV = {guard.SESSION_ENV: COORD}


# --- occupancy -------------------------------------------------------------------


def test_occupancy_counts_input_cache_read_and_cache_creation(tx):
    reading = guard.read_occupancy(str(tx.path), WINDOW)
    assert (reading.tokens, reading.pct, reading.note) == (200, 20.0, "")


def test_a_branched_transcript_reads_the_live_branch(tmp_path):
    t = Transcript(tmp_path / "b.jsonl")
    fork = t.user()
    t.reply(900)  # the abandoned branch, written first
    t.user(parent=fork)  # the rewind: a new branch from the fork point
    t.reply(300)
    assert guard.read_occupancy(str(t.path), WINDOW).tokens == 300


def test_a_sidechain_record_is_never_the_live_tip(tmp_path):
    t = Transcript(tmp_path / "s.jsonl")
    t.user()
    t.reply(300)
    t.raw(dict(t.records[-1], uuid="side", isSidechain=True, parentUuid="u-0001"))
    t.records[-1]["message"] = dict(
        t.records[-1]["message"], usage={"input_tokens": 999}
    )
    t.write()
    assert guard.read_occupancy(str(t.path), WINDOW).tokens == 300


def test_after_compaction_only_usage_after_the_last_boundary_counts(tmp_path):
    t = Transcript(tmp_path / "c.jsonl")
    t.user()
    t.reply(900)
    t.boundary()
    t.user()
    unknown = guard.read_occupancy(str(t.path), WINDOW)
    assert unknown.pct is None and "compaction" in unknown.note
    t.reply(120)
    assert guard.read_occupancy(str(t.path), WINDOW).tokens == 120


def _recorded():
    text = REAL_COMPACTION.read_text(encoding="utf-8")
    return [json.loads(x) for x in text.splitlines()]


def _recorded_prefix(tmp_path, upto):
    """The recorded transcript's first `upto` records, as a file."""
    lines = REAL_COMPACTION.read_text(encoding="utf-8").splitlines(keepends=True)
    path = tmp_path / "prefix-{}.jsonl".format(upto)
    path.write_text("".join(lines[:upto]), encoding="utf-8", newline="")
    return path


def test_the_recorded_compaction_fixture_is_claude_code_2_1_289():
    records = _recorded()
    assert {r["version"] for r in records if "version" in r} == {"2.1.289"}
    (boundary,) = [r for r in records if r.get("subtype") == "compact_boundary"]
    assert boundary["type"] == "system" and boundary["parentUuid"] is None
    assert boundary["compactMetadata"]["trigger"] == "manual"


def test_a_recorded_compaction_reads_the_reply_after_the_boundary():
    reading = guard.read_occupancy(str(REAL_COMPACTION), 200_000)
    assert reading.tokens == 10 + 30430 + 5723  # the post-compaction reply


def test_a_recorded_compaction_never_reads_a_preserved_messages_old_usage(tmp_path):
    """Until the first reply after the boundary, the messages the compaction
    preserved (named by uuid, not rewritten) keep their pre-compaction usage;
    the live branch stops at the boundary, so the reading is unknown rather
    than that stale number."""
    records = _recorded()
    at = next(
        i for i, r in enumerate(records) if r.get("subtype") == "compact_boundary"
    )
    reply = next(
        i for i, r in enumerate(records) if i > at and r.get("type") == "assistant"
    )
    kept = set(records[at]["compactMetadata"]["preservedMessages"]["uuids"])
    stale = [r for r in records if r.get("uuid") in kept and r["type"] == "assistant"]
    assert stale[-1]["message"]["usage"]["cache_read_input_tokens"] == 35551
    reading = guard.read_occupancy(str(_recorded_prefix(tmp_path, reply)), 200_000)
    assert reading.pct is None and "compaction" in reading.note
    before = guard.read_occupancy(str(_recorded_prefix(tmp_path, at)), 200_000)
    assert before.tokens == 10 + 35551 + 242


def test_after_a_resume_the_newest_usage_counts_whatever_session_wrote_it(tmp_path):
    t = Transcript(tmp_path / "r.jsonl", session="before-resume")
    t.user()
    t.reply(700)
    t.session = "after-resume"
    t.user()
    t.reply(450)
    assert guard.read_occupancy(str(t.path), WINDOW).tokens == 450


def test_malformed_and_partial_usage_is_skipped_to_the_newest_valid(tmp_path):
    t = Transcript(tmp_path / "m.jsonl")
    t.user()
    t.reply(400)
    t.reply("lots")  # a non-integer field
    t.reply(0)  # a zero total is no reading
    t.reply(50, model="<synthetic>")  # an error stand-in
    t.raw(
        {
            "type": "assistant",
            "uuid": "u-x",
            "parentUuid": t.records[-1]["uuid"],
            "message": {"usage": {"cache_read_input_tokens": 3}},
        }
    )  # no input_tokens
    t.write(tail='{"type": "assistant", "uuid": "u-partial", "mess')  # torn last line
    assert guard.read_occupancy(str(t.path), WINDOW).tokens == 400


def test_no_valid_usage_reads_unknown_never_zero(tmp_path):
    t = Transcript(tmp_path / "n.jsonl")
    t.user()
    t.reply(0)
    reading = guard.read_occupancy(str(t.path), WINDOW)
    assert reading.pct is None and reading.tokens is None and not reading.known
    assert guard.read_occupancy(None, WINDOW).pct is None
    assert guard.read_occupancy(str(tmp_path / "absent.jsonl"), WINDOW).pct is None


def test_admission_compares_unrounded_occupancy(tmp_path):
    root = make_root(tmp_path, pct=50, window=1_000_000)
    t = Transcript(tmp_path / "edge.jsonl")
    t.user()
    t.reply(499_600)  # 49.96%: displays as 50.0, must not latch
    assert guard.take(root, COORD, str(t.path)) is None
    assert guard.claim_refusal(root, env=ENV) is None
    assert guard.read_occupancy(str(t.path), 1_000_000).pct < 50
    t.reply(500_000)
    assert "drain mode is latched" in guard.claim_refusal(root, env=ENV)


def test_a_mismatched_window_is_flagged_with_its_percent(tmp_path):
    t = Transcript(tmp_path / "w.jsonl")
    t.user()
    t.reply(1500)
    reading = guard.read_occupancy(str(t.path), WINDOW)
    assert reading.pct == 150.0 and "window mismatch" in reading.note


def test_the_reader_reads_the_tail_and_widens_only_to_resolve(tmp_path, monkeypatch):
    t = Transcript(tmp_path / "big.jsonl")
    t.user()
    t.reply(333)
    for _ in range(200):
        t.user()  # a long run of records without usage
    sizes = []
    real = guard._tail_records
    monkeypatch.setattr(
        guard, "_tail_records", lambda p, n: sizes.append(n) or real(p, n)
    )
    assert guard.read_occupancy(str(t.path), WINDOW, tail_bytes=512).tokens == 333
    assert sizes[0] == 512 and len(sizes) > 1
    sizes.clear()
    t.reply(10)
    guard.read_occupancy(str(t.path), WINDOW, tail_bytes=512)
    assert sizes == [512]


# --- dials -----------------------------------------------------------------------


def test_the_dials_are_declared_here_and_in_the_template():
    import tomllib

    live = tomllib.loads((ROOT / "docs" / "process.toml").read_text("utf-8"))
    tmpl = tomllib.loads(
        (ROOT / "project-trajectory" / "process.toml.template").read_text("utf-8")
    )
    assert live["coordinator"] == {
        "context_guard_pct": 50,
        "context_window_tokens": 1000000,
    }
    assert tmpl["coordinator"]["context_guard_pct"] == 0
    assert guard.guard_config(ROOT) == guard.GuardConfig(50, 1000000)


def test_a_malformed_threshold_leaves_the_guard_off(tmp_path):
    root = tmp_path / "r"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "process.toml").write_text(
        '[coordinator]\ncontext_guard_pct = "half"\ncontext_window_tokens = -1\n',
        encoding="utf-8",
    )
    assert guard.guard_config(root) == guard.GuardConfig(0, guard.DEFAULT_WINDOW)


def test_off_means_off_claims_pass_and_hooks_do_nothing(tmp_path, tx):
    root = make_root(tmp_path, pct=0)
    assert guard.claim_refusal(root, env={}) is None
    for name in sorted(guard.MONITORED | {"SessionStart", "PreCompact", "SessionEnd"}):
        assert (
            guard.hook(ev(name, transcript=tx.path, reason="logout"), root, env={})
            is None
        )
    assert not (root / "out").exists()


# --- identity and the lease -----------------------------------------------------


def test_a_subagent_and_another_sessions_hook_calls_are_no_ops(root, tx):
    held(root, tx)
    tx.reply(900)  # over the threshold
    sub = ev("PostToolUse", transcript=tx.path, agent_id="a1", agent_type="Explore")
    other = ev("PostToolUse", session=OTHER, transcript=tx.path)
    foreign_tx = ev("PostToolUse", transcript=tx.path.with_name("sub.jsonl"))
    for payload in (sub, other, foreign_tx):
        assert guard.hook(payload, root, env={}) is None
    assert not guard._load(guard.lease_dir(root)).get("draining")
    respelled = ev(
        "PostToolUse", transcript=str(tx.path.parent / "x" / ".." / tx.path.name)
    )
    assert guard.hook(respelled, root, env={}) is not None  # one file, spelled apart


def test_a_silent_live_holder_keeps_the_lease_however_long_it_is_quiet(root, tx):
    lease = held(root, tx)
    lease["taken_at"] = "2000-01-01T00:00:00Z"  # silent for decades
    guard._save(guard.lease_dir(root), lease)
    refusal = guard.take(root, OTHER)
    assert COORD in refusal and "release" in refusal
    assert guard._load(guard.lease_dir(root))["holder"] == COORD


def test_a_non_holders_claim_refuses_naming_the_holder_and_the_release(root, tx):
    held(root, tx)
    refusal = guard.claim_refusal(root, env={guard.SESSION_ENV: OTHER})
    assert COORD in refusal and "coordinator_guard.py release" in refusal
    assert "unknown" in guard.claim_refusal(root, env={})


def test_with_no_lease_held_a_claim_refuses_naming_the_take(root):
    refusal = guard.claim_refusal(root, env=ENV)
    assert "no coordinator lease" in refusal and "coordinator_guard.py take" in refusal


def test_the_holders_claim_below_threshold_passes(root, tx):
    held(root, tx)
    assert guard.claim_refusal(root, env=ENV) is None


def test_the_owners_release_frees_the_lease_and_is_recorded(root, tx):
    held(root, tx)
    assert guard.release(root, "") is not None
    assert guard.release(root, "the session crashed before SessionEnd") is None
    assert guard._load(guard.lease_dir(root)) == {}
    last = events(root)[-1]
    assert last["event"] == "release" and last["was"] == COORD
    assert guard.take(root, OTHER) is None


def test_the_relaunched_successor_takes_the_lease_at_session_start(root, tx):
    lease = held(root, tx)
    lease.update(draining=True, successor_token="tok")
    guard._save(guard.lease_dir(root), lease)
    wrong = guard.hook(
        ev("SessionStart", session=OTHER), root, env={guard.TAKE_ENV: "nope"}
    )
    assert wrong is None and guard._load(guard.lease_dir(root))["holder"] == COORD
    out = guard.hook(
        ev("SessionStart", session=OTHER, transcript="next.jsonl", source="startup"),
        root,
        env={guard.TAKE_ENV: "tok"},
    )
    assert "coordinator lease" in out["hookSpecificOutput"]["additionalContext"]
    lease = guard._load(guard.lease_dir(root))
    assert (lease["holder"], lease["draining"], lease["successor_token"]) == (
        OTHER,
        False,
        None,
    )
    assert [e["event"] for e in events(root)][-2:] == ["take-refused", "take-successor"]


# --- the drain latch ---------------------------------------------------------------


def test_the_latch_holds_after_a_compaction_drops_the_reading(root, tx):
    held(root, tx)
    tx.reply(600)
    assert "drain mode is latched" in guard.claim_refusal(root, env=ENV)
    tx.boundary()
    tx.user()
    tx.reply(50)  # 5% after the compaction
    assert guard.read_occupancy(str(tx.path), WINDOW).pct == 5.0
    assert "drain mode is latched" in guard.claim_refusal(root, env=ENV)


def test_the_latch_survives_a_resumed_session_and_is_restated(root, tx):
    held(root, tx)
    tx.reply(600)
    guard.hook(ev("PreToolUse", transcript=tx.path), root, env={})
    tx.session = "resumed"
    tx.reply(10)
    out = guard.hook(
        ev("SessionStart", transcript=tx.path, source="resume"), root, env={}
    )
    assert "drain mode is latched" in out["hookSpecificOutput"]["additionalContext"]
    assert guard._load(guard.lease_dir(root))["draining"] is True
    assert guard.claim_refusal(root, env=ENV) is not None


def test_only_the_owners_recorded_clear_or_the_successor_unlatches(root, tx):
    held(root, tx)
    tx.reply(600)
    guard.claim_refusal(root, env=ENV)
    assert guard.take(root, COORD) is None  # a re-take is not a clear
    assert guard._load(guard.lease_dir(root))["draining"] is True
    assert guard.clear(root, "") is not None
    assert guard.clear(root, "measured wrong window") is None
    assert guard._load(guard.lease_dir(root))["draining"] is False
    assert events(root)[-1]["event"] == "clear"


@pytest.mark.parametrize(
    "event",
    ["PreToolUse", "PostToolUse", "PostToolUseFailure", "UserPromptSubmit", "Stop"],
)
def test_the_instruction_comes_once_at_the_latch_then_bounded_reminders(
    root, tx, event, monkeypatch
):
    monkeypatch.setattr(guard, "REMINDER_EVERY", 3)
    held(root, tx)
    assert guard.hook(ev(event, transcript=tx.path), root, env={}) is None  # 20%
    tx.reply(500)
    first = guard.hook(ev(event, transcript=tx.path), root, env={})
    assert first["hookSpecificOutput"]["hookEventName"] == event
    assert first["hookSpecificOutput"]["additionalContext"].startswith(
        "COORDINATOR CONTEXT GUARD: this session's context reached 50.0%"
    )
    outs = [guard.hook(ev(event, transcript=tx.path), root, env={}) for _ in range(9)]
    said = [o["hookSpecificOutput"]["additionalContext"] for o in outs if o]
    assert [bool(o) for o in outs] == [False, False, True] * 3
    assert all(s.startswith("COORDINATOR CONTEXT GUARD reminder") for s in said)
    assert [e["event"] for e in events(root)].count("latch") == 1


# --- the claim boundary --------------------------------------------------------------


def _crossing(root, tx):
    """Round 2's sequence: the last measured reply is below the threshold,
    the next reply crosses it, and its first tool call is a claim."""
    held(root, tx)
    assert guard.hook(ev("PostToolUse", transcript=tx.path), root, env={}) is None
    tx.reply(480, read=40)  # 52%: the crossing reply, not yet measured


def test_the_crossing_replys_claim_refuses_via_the_pre_tool_use_reading(
    root, tx, monkeypatch, capsys
):
    _crossing(root, tx)
    out = guard.hook(
        ev("PreToolUse", transcript=tx.path, tool_name="Bash"), root, env={}
    )
    assert "drain mode is latched" in out["hookSpecificOutput"]["additionalContext"]
    assert (
        "permissionDecision" not in out["hookSpecificOutput"]
    )  # never a spelling rule
    monkeypatch.setenv(guard.SESSION_ENV, COORD)
    capsys.readouterr()
    assert integ.claim(root, ["WI-001"], "wi-001") == 1
    assert "coordinator guard: drain mode is latched" in capsys.readouterr().err


def test_the_crossing_replys_claim_refuses_with_no_hook_run(
    root, tx, monkeypatch, capsys
):
    _crossing(root, tx)
    monkeypatch.setenv(guard.SESSION_ENV, COORD)
    assert integ.claim(root, ["WI-001"], "wi-001") == 1
    assert "drain mode is latched" in capsys.readouterr().err
    assert guard._load(guard.lease_dir(root))["latched_pct"] == 52.0


def test_the_live_dispatchers_claim_route_is_untouched(root, tx, monkeypatch, capsys):
    held(root, tx)
    tx.reply(900)

    def boom(*a, **k):
        raise AssertionError("the dispatcher's route consulted the guard")

    monkeypatch.setattr(integ.coordinator_guard, "claim_refusal", boom)
    integ.claim(root, ["WI-001"], "wi-001", dispatch_lock_held=True)
    assert "coordinator guard" not in capsys.readouterr().err


def _guard_calls(fn):
    """True when function `fn` calls `coordinator_guard.claim_refusal`."""
    return any(
        isinstance(node, ast.Attribute)
        and node.attr == "claim_refusal"
        and getattr(node.value, "id", "") == "coordinator_guard"
        for node in ast.walk(fn)
    )


def test_only_the_claim_consults_the_guard_so_close_out_passes():
    """Landing, archive, sweep, the scoped-unpause restore and verification
    worktrees never reach the guard: no kit script but `integrate.claim`
    calls it, and the PreToolUse hook never denies a call."""
    sources = {p.stem: p.read_text(encoding="utf-8") for p in SCRIPTS.rglob("*.py")}
    callers = [
        (stem, fn.name)
        for stem, text in sorted(sources.items())
        if stem != "coordinator_guard" and "claim_refusal" in text
        for fn in ast.walk(ast.parse(text))
        if isinstance(fn, ast.FunctionDef) and _guard_calls(fn)
    ]
    assert callers == [("integrate", "claim")]


def test_a_draining_pre_tool_use_never_denies_a_close_out_command(root, tx):
    held(root, tx)
    tx.reply(900)
    for command in (
        "git worktree add --detach ../verify HEAD",
        "git worktree remove ../verify",
        "git merge --squash wi-001",
        "python project-trajectory/scripts/intake.py sweep",
        "git checkout HEAD~1 -- docs/work/pause",
    ):
        payload = ev(
            "PreToolUse",
            transcript=tx.path,
            tool_name="Bash",
            tool_input={"command": command},
        )
        out = guard.hook(payload, root, env={}) or {"hookSpecificOutput": {}}
        assert "permissionDecision" not in out["hookSpecificOutput"]


# --- compaction telemetry ---------------------------------------------------------------


def test_pre_compact_records_trigger_occupancy_and_guard_state(root, tx):
    held(root, tx)
    guard.hook(ev("PreCompact", transcript=tx.path, trigger="auto"), root, env={})
    entry = guard._load(guard.lease_dir(root))["compactions"][-1]
    assert entry["trigger"] == "auto" and entry["occupancy"]["tokens"] == 200
    assert (entry["draining"], entry["relaunch_requested"]) == (False, False)
    assert entry["class"] == "missed-threshold"
    assert events(root)[-1]["event"] == "compaction"


@pytest.mark.parametrize(
    "entry, expected",
    [
        ({"trigger": "auto", "draining": False}, "missed-threshold"),
        ({"trigger": "manual", "draining": False}, "manual"),
        ({"trigger": "auto", "draining": True}, "during-drain"),
        ({"trigger": "manual", "draining": True}, "during-drain"),
    ],
)
def test_the_handoff_classifies_each_compaction(entry, expected):
    assert guard.classify_compaction(entry, guard.GuardConfig(50)) == expected


# --- the relaunch -------------------------------------------------------------------------


HANDOFF = "# Handoff\n\n## Session prompt (paste to start the next session)\n\n```text\nYou are the coordinator.\nRead docs/status.md.\n```\n"


def _ready(root, tx, tmp_path):
    held(root, tx)
    handoff = tmp_path / "handoff.md"
    handoff.write_text(HANDOFF, encoding="utf-8")
    assert guard.request_relaunch(root, handoff, COORD) is None
    return handoff


class Launches:
    def __init__(self, fail=False):
        self.calls = []
        self.fail = fail

    def __call__(self, repo_root, prompt_file, token):
        if self.fail:
            raise OSError("no console")
        self.calls.append(
            (repo_root, Path(prompt_file).read_text(encoding="utf-8"), token)
        )


def test_the_session_prompt_is_the_fenced_block_under_its_heading(tmp_path):
    path = tmp_path / "h.md"
    path.write_text(HANDOFF, encoding="utf-8")
    assert (
        guard.session_prompt(path) == "You are the coordinator.\nRead docs/status.md."
    )
    path.write_text("# Handoff\n\n```text\nnot a prompt\n```\n", encoding="utf-8")
    assert guard.session_prompt(path) is None


def test_a_heading_inside_the_prompt_fence_is_prompt_text(tmp_path):
    path = tmp_path / "h.md"
    path.write_text(
        "# Handoff\n\n```sh\n# Session prompt (a comment, not a heading)\n```\n\n"
        "## Session prompt\n\n```text\n# Coordinator role\nRead docs/status.md.\n"
        "## Order\nBuild first.\n```\n",
        encoding="utf-8",
    )
    assert guard.session_prompt(path) == (
        "# Coordinator role\nRead docs/status.md.\n## Order\nBuild first."
    )


def test_only_the_holder_requests_a_relaunch_naming_a_real_handoff(root, tx, tmp_path):
    held(root, tx)
    handoff = tmp_path / "h.md"
    handoff.write_text(HANDOFF, encoding="utf-8")
    assert "only the lease holder" in guard.request_relaunch(root, handoff, OTHER)
    assert "no session prompt" in guard.request_relaunch(root, tmp_path / "x.md", COORD)
    assert guard.request_relaunch(root, handoff, COORD) is None
    request = json.loads((guard.lease_dir(root) / "relaunch.json").read_text("utf-8"))
    assert set(request) == {"session_id", "repo_root", "handoff", "created"}


@pytest.mark.parametrize("reason", ["clear", "resume", "", None])
def test_clear_and_resume_never_launch(root, tx, tmp_path, reason):
    _ready(root, tx, tmp_path)
    launch = Launches()
    guard.hook(ev("SessionEnd", reason=reason), root, env={}, launch=launch)
    assert launch.calls == [] and (guard.lease_dir(root) / "relaunch.json").exists()


@pytest.mark.parametrize("reason", sorted(guard.EXIT_REASONS))
def test_an_exit_launches_once_in_the_declared_root_with_the_prompt(
    root, tx, tmp_path, reason
):
    _ready(root, tx, tmp_path)
    launch = Launches()
    assert (
        guard.session_end(root, ev("SessionEnd", reason=reason), launch=launch) is True
    )
    assert (
        guard.session_end(root, ev("SessionEnd", reason=reason), launch=launch) is False
    )
    ((where, prompt, token),) = launch.calls
    assert where == Path(root).resolve()
    assert prompt == "You are the coordinator.\nRead docs/status.md."
    assert guard._load(guard.lease_dir(root))["successor_token"] == token


def test_a_non_holders_or_subagents_end_never_launches(root, tx, tmp_path):
    _ready(root, tx, tmp_path)
    launch = Launches()
    guard.session_end(
        root, ev("SessionEnd", session=OTHER, reason="logout"), launch=launch
    )
    guard.session_end(
        root, ev("SessionEnd", reason="logout", agent_id="a1"), launch=launch
    )
    assert launch.calls == []


def test_two_concurrent_end_handlers_launch_once(root, tx, tmp_path):
    _ready(root, tx, tmp_path)
    launch = Launches()
    barrier = threading.Barrier(2)

    def end():
        barrier.wait()
        guard.session_end(root, ev("SessionEnd", reason="logout"), launch=launch)

    threads = [threading.Thread(target=end) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(launch.calls) == 1


def test_a_failed_launch_restores_the_request(root, tx, tmp_path, capsys):
    _ready(root, tx, tmp_path)
    assert (
        guard.session_end(
            root, ev("SessionEnd", reason="logout"), launch=Launches(fail=True)
        )
        is False
    )
    assert (guard.lease_dir(root) / "relaunch.json").exists()
    assert guard._load(guard.lease_dir(root))["successor_token"] is None
    assert "request restored" in capsys.readouterr().err
    assert events(root)[-1]["event"] == "launch-failed"
    launch = Launches()
    assert (
        guard.session_end(root, ev("SessionEnd", reason="logout"), launch=launch)
        is True
    )


def _assert_restored(root):
    directory = guard.lease_dir(root)
    assert (directory / "relaunch.json").exists()
    assert not list(directory.glob("relaunch.*.consumed"))
    assert not list(directory.glob("relaunch-prompt.*.txt"))
    assert guard._load(directory)["successor_token"] is None
    assert events(root)[-1]["event"] == "launch-failed"


def test_a_failed_prompt_write_restores_the_request(root, tx, tmp_path, monkeypatch):
    _ready(root, tx, tmp_path)
    real = Path.write_text

    def disk_full(self, *a, **k):
        if self.name.startswith("relaunch-prompt."):
            raise OSError(28, "No space left on device")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "write_text", disk_full)
    launch = Launches()
    end = ev("SessionEnd", reason="logout")
    assert guard.session_end(root, end, launch=launch) is False
    monkeypatch.undo()
    assert launch.calls == []
    _assert_restored(root)


class Process:
    """A started launcher: `code` is its exit within the grace, or None
    while it is still running."""

    def __init__(self, code):
        self.code = code

    def wait(self, timeout=None):
        if self.code is None:
            raise guard.subprocess.TimeoutExpired("launcher", timeout)
        return self.code


def _real_launch(code):
    def launch(repo_root, prompt_file, token):
        guard.launch_detached(
            repo_root,
            prompt_file,
            token,
            popen=lambda argv, **kw: Process(code),
            os_name="nt",
            grace=0,
        )

    return launch


def test_a_launcher_that_exits_non_zero_restores_the_request(root, tx, tmp_path):
    _ready(root, tx, tmp_path)
    (root / "scripts").mkdir()
    (root / "scripts" / "coordinator-relaunch.cmd").write_text("", encoding="utf-8")
    end = ev("SessionEnd", reason="logout")
    assert guard.session_end(root, end, launch=_real_launch(42)) is False
    _assert_restored(root)
    assert guard.session_end(root, end, launch=_real_launch(None)) is True
    assert events(root)[-1]["event"] == "launched"


@pytest.mark.parametrize(
    "field, value",
    [
        ("session_id", OTHER),
        ("repo_root", "/elsewhere"),
        ("handoff", "/no/such/handoff.md"),
    ],
)
def test_a_foreign_request_is_refused_and_reported(
    root, tx, tmp_path, capsys, field, value
):
    _ready(root, tx, tmp_path)
    path = guard.lease_dir(root) / "relaunch.json"
    request = json.loads(path.read_text("utf-8"))
    request[field] = value
    path.write_text(json.dumps(request), encoding="utf-8")
    launch = Launches()
    assert (
        guard.session_end(root, ev("SessionEnd", reason="logout"), launch=launch)
        is False
    )
    assert launch.calls == []
    assert "relaunch refused" in capsys.readouterr().err
    assert events(root)[-1]["event"] == "relaunch-refused"
    assert list(guard.lease_dir(root).glob("relaunch.*.refused"))


def test_a_windows_root_with_spaces_keeps_every_part_quoted(tmp_path):
    root = tmp_path / "root with spaces"
    _, line, _ = guard.launch_command(root, root / "out" / "p.txt", "tok", "nt")
    launcher = root / "scripts" / "coordinator-relaunch.cmd"
    assert " " in str(launcher)
    assert line == 'cmd /d /s /c ""{}" "{}" "{}" "tok""'.format(
        launcher, root, root / "out" / "p.txt"
    )


def test_a_failed_token_save_restores_the_request(root, tx, tmp_path, monkeypatch):
    _ready(root, tx, tmp_path)
    real = guard._save

    def disk_full(directory, lease):
        if lease.get("successor_token"):
            raise OSError(28, "No space left on device")
        return real(directory, lease)

    monkeypatch.setattr(guard, "_save", disk_full)
    launch = Launches()
    end = ev("SessionEnd", reason="logout")
    assert guard.session_end(root, end, launch=launch) is False
    monkeypatch.undo()
    assert launch.calls == []
    _assert_restored(root)


@pytest.mark.parametrize(
    "os_name, shell, launcher",
    [
        ("nt", "cmd", "coordinator-relaunch.cmd"),
        ("posix", "sh", "coordinator-relaunch.sh"),
    ],
)
def test_the_launcher_runs_detached_in_the_repo_root(
    tmp_path, os_name, shell, launcher
):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / launcher).write_text("", encoding="utf-8")
    seen = []
    guard.launch_detached(
        tmp_path,
        tmp_path / "p.txt",
        "tok",
        popen=lambda argv, **kw: seen.append((argv, kw)) or Process(None),
        os_name=os_name,
        grace=0,
    )
    ((argv, kw),) = seen
    if os_name == "nt":
        assert argv == 'cmd /d /s /c ""{}" "{}" "{}" "tok""'.format(
            tmp_path / "scripts" / launcher, tmp_path, tmp_path / "p.txt"
        )
    else:
        assert argv == [
            shell,
            str(tmp_path / "scripts" / launcher),
            str(tmp_path),
            str(tmp_path / "p.txt"),
            "tok",
        ]
    assert kw["cwd"] == str(tmp_path)
    handles = {"stdin", "stdout", "stderr"}
    if os_name == "nt":  # the new console's own handles stay the successor's
        assert kw["creationflags"] and not handles & set(kw)
    else:
        assert kw["start_new_session"] and handles <= set(kw)
    for code, launched in ((0, True), (42, False)):
        try:
            guard.launch_detached(
                tmp_path,
                tmp_path / "p.txt",
                "t",
                popen=lambda argv, **kw: Process(code),
                os_name=os_name,
                grace=0,
            )
            assert launched
        except OSError as exc:
            assert not launched and "exited 42" in str(exc)
    with pytest.raises(OSError):
        guard.launch_detached(
            tmp_path / "none", tmp_path / "p.txt", "t", popen=None, os_name=os_name
        )


def test_exec_claude_passes_the_prompt_as_one_argument(tmp_path):
    prompt = tmp_path / "p.txt"
    prompt.write_text('line one "quoted" & more\nline two %PATH%', encoding="utf-8")
    seen = []
    guard.exec_claude(prompt, run=lambda argv: seen.append(argv) or 0)
    assert seen == [["claude", 'line one "quoted" & more\nline two %PATH%']]


# --- registration and the dry run -------------------------------------------------------


def test_the_hooks_are_registered_in_the_tracked_project_settings():
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text("utf-8"))
    wanted = {
        "PreToolUse",
        "PostToolUse",
        "PostToolUseFailure",
        "UserPromptSubmit",
        "Stop",
        "SessionStart",
        "SessionEnd",
        "PreCompact",
    }
    assert set(settings["hooks"]) == wanted
    for name in wanted:
        (group,) = settings["hooks"][name]
        (entry,) = group["hooks"]
        assert entry["type"] == "command"
        assert entry["command"].endswith(
            'project-trajectory/scripts/coordinator_guard.py" hook'
        )


def test_end_to_end_dry_run(root, tx, tmp_path, monkeypatch):
    """Over the threshold: the latch, the instruction and a refused claim;
    then a stubbed exit launches exactly once, and the successor takes over."""
    held(root, tx)
    tx.reply(700)
    out = guard.hook(ev("PreToolUse", transcript=tx.path), root, env={})
    assert "Close out now" in out["hookSpecificOutput"]["additionalContext"]
    monkeypatch.setenv(guard.SESSION_ENV, COORD)
    assert integ.claim(root, ["WI-001"], "wi-001") == 1
    handoff = tmp_path / "handoff.md"
    handoff.write_text(HANDOFF, encoding="utf-8")
    assert guard.request_relaunch(root, handoff, COORD) is None
    launch = Launches()
    for _ in range(2):
        guard.hook(
            ev("SessionEnd", reason="prompt_input_exit"), root, env={}, launch=launch
        )
    assert len(launch.calls) == 1
    token = launch.calls[0][2]
    guard.hook(
        ev("SessionStart", session=OTHER, transcript="n.jsonl"),
        root,
        env={guard.TAKE_ENV: token},
    )
    assert guard._load(guard.lease_dir(root))["holder"] == OTHER
