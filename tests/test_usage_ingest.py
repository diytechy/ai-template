"""The usage ingest (`usage_ingest.py`), in process, over roots outside any
checkout: each contribution is spooled under the root's own
`out/sessions/spool/`, so no case here needs git. The cases on real
repositories (a claimed lane, another worktree, the primary checkout) are in
`test_usage_ingest_git.py`; this module is that family's in-process pin.

The Claude home is a tmp copy of the cut fixtures
(`claude_transcript_fixtures`, whose docstring states their provenance),
named to the command by `CLAUDE_CONFIG_DIR`.
"""

import json
import re
import shutil
import uuid

import pytest
from conftest import load_script

import claude_transcript_fixtures as fx

ui = load_script("usage_ingest")
ac = load_script("agent_common")


AGENTS = ("", fx.A23, fx.A7B, fx.AF7)

# Per NESTED invocation: (role, spawn depth, parent, agent type, request
# model, message count, first and last message ids, started-at, ended-at,
# fresh, cache read, cache write, output, inclusive input, reasoning,
# usage-status)
EXPECTED = {
    "": (
        "COORDINATOR",
        "0",
        "",
        "",
        "",
        "5",
        "msg_011CgCj3Q3uj6XJhHCpboZ9B",
        "msg_011CgCj4nzLMqZqD4bySDZb7",
        "2026-10-20T02:47:48.470Z",
        "2026-10-20T02:48:06.899Z",
        (10, 300817, 48807, 2694),
        "349634",
        "811",
        "known",
    ),
    fx.A23: (
        "SUBAGENT",
        "1",
        "",
        "general-purpose",
        "opus",
        "5",
        "msg_011CgD8mDn8YpWkCdQhKKdqc",
        "msg_011CgD8nBT1xTuoWCqnyQJtZ",
        "2026-10-20T07:58:49.804Z",
        "2026-10-20T07:59:18.271Z",
        (10, 231724, 34351, 2701),
        "266085",
        "327",
        "known",
    ),
    fx.A7B: (
        "SUBAGENT",
        "2",
        fx.A23,
        "general-purpose",
        "",
        "4",
        "msg_011CgD8oSknh5DBc5nih8wKq",
        "msg_011CgD8pNkDf6cxpRQY3228r",
        "2026-10-20T07:59:19.580Z",
        "2026-10-20T07:59:33.864Z",
        (8, 172821, 36977, 1303),
        "209806",
        "10",
        "known",
    ),
    fx.AF7: (
        "SUBAGENT",
        "2",
        fx.A23,
        "general-purpose",
        "",
        "7",
        "msg_011CgDDsGTMcQPLq9VTdBZZr",
        fx.AF7_LAST,
        "2026-10-20T09:05:45.737Z",
        "2026-10-20T09:06:32.027Z",
        (14, 381334, 65887, 3349),
        "447235",
        "",
        "partial",
    ),
}

A7B_SECOND = "msg_011CgD8ojPuptUi2S1joBiWn"
AF7_FOURTH = "msg_011CgDDtoVBbUDSj69WUpwBg"


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A tmp Claude home holding the fixture sessions, named to the command;
    no ambient session id."""
    home = fx.home_copy(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home))
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    return home


@pytest.fixture
def root(tmp_path):
    """A root outside any checkout: its contributions spool under it."""
    path = tmp_path / "root"
    path.mkdir()
    return path


def _ingest(root, session=fx.NESTED):
    return ui.main(["--session", session, "--root", str(root)])


def _spool(root):
    return ui.session_service.spool_dir(root)


def _logs(root):
    return sorted(_spool(root).glob("call_*.log"))


def _meta(path):
    meta, terminated = ac.log_meta_text(path.read_text(encoding="utf-8"))
    assert terminated, path
    return meta


def _metas(root):
    return [_meta(p) for p in _logs(root)]


def _of(root, agent):
    return [m for m in _metas(root) if m.get("agent-id") == agent]


def _lines(out, word):
    return [line for line in out.splitlines() if word in line]


def test_one_ingest_records_four_logs_with_the_usage_vocabulary(home, root, capsys):
    adapters = ui.session_adapters
    assert _ingest(root) == 0
    out = capsys.readouterr().out
    logs = _logs(root)
    assert len(logs) == 4
    assert len(_lines(out, "recorded")) == 4
    found = {}
    for path in logs:
        assert ui.session_service.is_call_log(path.name), path.name
        meta = _meta(path)
        agent = meta["agent-id"]
        inv = ui.invocation_id(fx.NESTED, agent)
        assert path.name == "call_{}-{}.log".format(
            inv, fx.local_stamp(meta["ended-at"])
        )
        assert meta["invocation-id"] == inv
        assert meta["session"] == "call_" + inv
        assert meta["contribution-key"] == "{}:{}:{}".format(
            inv, EXPECTED[agent][6], EXPECTED[agent][7]
        )
        assert meta["message-cursor"] == EXPECTED[agent][7]
        assert (meta["phase"], meta["outcome"]) == (meta["role"], "INGESTED")
        assert (meta["cli"], meta["semconv"], meta["gen_ai.provider.name"]) == (
            "claude",
            adapters.OTEL_SEMCONV,
            "anthropic",
        )
        assert (meta["usage-source"], meta["usage-scope"]) == (
            "transcript",
            "contribution",
        )
        assert meta["session-id"] == meta["gen_ai.conversation.id"] == fx.NESTED
        assert meta["model"] == meta["gen_ai.response.model"] == "claude-opus-5-5"
        assert meta["raw-usage"] == ""
        found[agent] = (
            meta["role"],
            meta["spawn-depth"],
            meta["parent-agent-id"],
            meta["agent-type"],
            meta["gen_ai.request.model"],
            meta["message-count"],
            EXPECTED[agent][6],
            meta["message-cursor"],
            meta["started-at"],
            meta["ended-at"],
            fx.header_four(meta),
            meta["gen_ai.usage.input_tokens"],
            meta["gen_ai.usage.reasoning.output_tokens"],
            meta["usage-status"],
        )
    assert found == EXPECTED


def test_the_invocation_id_is_derived_from_the_transcript_identity():
    ids = [ui.invocation_id(fx.NESTED, agent) for agent in AGENTS]
    assert all(re.fullmatch(r"[0-9a-f]{32}", i) for i in ids), ids
    assert len(set(ids)) == 4
    assert ids == [ui.invocation_id(fx.NESTED, agent) for agent in AGENTS]
    assert all(uuid.UUID(i).version == 5 for i in ids)
    assert ui.invocation_id(fx.CHAIN, "") not in ids


def test_ingesting_one_session_twice_records_nothing_the_second_time(
    home, root, capsys
):
    assert _ingest(root) == 0
    first = _logs(root)
    assert len(first) == 4
    capsys.readouterr()
    assert _ingest(root) == 0
    out = capsys.readouterr().out
    assert _logs(root) == first
    assert len(_lines(out, "unchanged")) == 4
    assert _lines(out, "recorded") == []


def test_appended_messages_are_recorded_alone_under_the_same_identity(
    home, root, capsys
):
    path = fx.transcript(home, fx.NESTED, fx.A7B)
    rest = fx.cut_after_message(path, A7B_SECOND)
    assert _ingest(root) == 0
    assert len(_logs(root)) == 4
    (before,) = _of(root, fx.A7B)
    assert before["message-count"] == "2"
    capsys.readouterr()
    fx.append_lines(path, rest)
    assert _ingest(root) == 0
    out = capsys.readouterr().out
    assert len(_logs(root)) == 5
    later = [
        m
        for m in _of(root, fx.A7B)
        if m["contribution-key"] != before["contribution-key"]
    ]
    assert len(later) == 1
    later = later[0]
    assert later["invocation-id"] == before["invocation-id"]
    assert later["message-count"] == "2"
    assert later["message-cursor"] == EXPECTED[fx.A7B][7]
    assert fx.header_four(later) == (4, 102148, 9554, 725)
    assert len(_lines(out, "recorded")) == 1
    assert len(_lines(out, "unchanged")) == 3


def test_initial_resumed_and_repeated_ingests_give_two_contributions_summing_to_the_whole(
    home, root
):
    path = fx.transcript(home, fx.NESTED, fx.AF7)
    rest = fx.cut_after_message(path, AF7_FOURTH)
    assert _ingest(root) == 0
    fx.append_lines(path, rest)
    assert _ingest(root) == 0
    assert _ingest(root) == 0
    logs = _of(root, fx.AF7)
    assert len(logs) == 2
    assert len({m["contribution-key"] for m in logs}) == 2
    assert len({m["invocation-id"] for m in logs}) == 1
    total = tuple(sum(c) for c in zip(*(fx.header_four(m) for m in logs)))
    assert total == fx.message_sums(path, "last") == (14, 381334, 65887, 3349)
    assert len(_logs(root)) == 5


def test_an_open_message_is_recorded_once_final_and_the_contributions_equal_the_completed_transcript(
    home, root, capsys
):
    path = fx.transcript(home, fx.NESTED, fx.A23)
    rest = fx.cut_after_first_record(path, fx.A23_THIRD)
    assert _ingest(root) == 0
    out = capsys.readouterr().out
    assert any("open " + fx.A23_THIRD in line for line in out.splitlines())
    (first,) = _of(root, fx.A23)
    assert first["message-count"] == "2"
    assert first["message-cursor"] == "msg_011CgD8mQLPEauvuYK5LWdDa"
    fx.append_lines(path, rest)
    assert _ingest(root) == 0
    logs = _of(root, fx.A23)
    assert len(logs) == 2
    (second,) = [m for m in logs if m["contribution-key"] != first["contribution-key"]]
    assert second["contribution-key"].split(":")[1] == fx.A23_THIRD
    # the once-open message counted at its final output (255), then two more
    assert fx.header_four(second) == (6, 161639, 6439, 2229)
    total = tuple(sum(c) for c in zip(*(fx.header_four(m) for m in logs)))
    assert total == fx.message_sums(path, "last")
    capsys.readouterr()
    assert _ingest(root) == 0
    assert len(_of(root, fx.A23)) == 2
    assert _lines(capsys.readouterr().out, "recorded") == []


def test_recorded_unchanged_and_open_lines_name_each_invocations_role_type_and_id(
    home, root, capsys
):
    """Each per-invocation line opens with that invocation's own role, agent
    type and agent id. Catches a line that drops the agent id or type, the
    session's prefix printed on a sub-agent's line, or an `open` or
    `unchanged` line printed bare or under another invocation's prefix."""
    fx.cut_after_first_record(fx.transcript(home, fx.NESTED, fx.A23), fx.A23_THIRD)
    session = "COORDINATOR - -: "
    agent = "SUBAGENT general-purpose {}: ".format(fx.A23)
    prefixes = {session} | {
        "SUBAGENT general-purpose {}: ".format(a) for a in AGENTS if a
    }
    assert _ingest(root) == 0
    first = capsys.readouterr().out.splitlines()
    assert _ingest(root) == 0
    second = capsys.readouterr().out.splitlines()
    for out in (first, second):
        assert all(line[: line.index(": ") + 2] in prefixes for line in out), out
        assert len([line for line in out if line.startswith(session)]) == 1, out
        assert agent + "open " + fx.A23_THIRD in out
        assert [line for line in out if fx.A23_THIRD in line] == [
            agent + "open " + fx.A23_THIRD
        ]
    assert [line for line in first if line.startswith(session + "recorded ")]
    assert [line for line in first if line.startswith(agent + "recorded 2 messages")]
    assert session + "unchanged" in second
    assert agent + "unchanged" in second


def test_two_contributions_whose_last_messages_share_a_second_both_survive(home, root):
    path = fx.transcript(home, fx.NESTED, fx.A7B)
    rest = fx.cut_after_message(path, A7B_SECOND)
    first_end = fx.last_timestamp(path)
    assert first_end == "2026-10-20T07:59:25.246Z"
    assert _ingest(root) == 0
    fx.append_lines(path, fx.restamp(rest, first_end[:19]))
    second_end = fx.last_timestamp(path)
    assert second_end[:19] == first_end[:19] and second_end != first_end
    assert _ingest(root) == 0
    names = sorted(p.name for p in _logs(root) if _meta(p)["agent-id"] == fx.A7B)
    assert len(names) == 2
    stamps = sorted(n[-19:-4] for n in names)
    assert stamps == [
        fx.local_stamp(first_end),
        fx.next_second(fx.local_stamp(first_end)),
    ]
    ends = sorted(m["ended-at"] for m in _of(root, fx.A7B))
    assert ends == sorted([first_end, second_end])
    assert all(m["message-cursor"] for m in _of(root, fx.A7B))
    assert _ingest(root) == 0
    assert len(_of(root, fx.A7B)) == 2


def test_a_run_killed_after_some_logs_then_rerun_records_each_invocation_once(
    home, root, monkeypatch
):
    real = ui.session_service.record
    calls = []

    def record(*args, **kwargs):
        calls.append(1)
        if len(calls) == 3:
            raise KeyboardInterrupt
        return real(*args, **kwargs)

    monkeypatch.setattr(ui.session_service, "record", record)
    with pytest.raises(KeyboardInterrupt):
        _ingest(root)
    assert len(_logs(root)) == 2
    assert _ingest(root) == 0
    metas = _metas(root)
    assert len(metas) == 4
    assert len({m["invocation-id"] for m in metas}) == 4
    assert {m["agent-id"]: m["message-count"] for m in metas} == {
        a: EXPECTED[a][5] for a in AGENTS
    }


def test_a_torn_earlier_log_refuses_that_invocation_naming_it(home, root, capsys):
    path = fx.transcript(home, fx.NESTED, fx.A7B)
    rest = fx.cut_after_message(path, A7B_SECOND)
    assert _ingest(root) == 0
    assert len(_of(root, fx.A7B)) == 1
    (torn,) = [p for p in _logs(root) if _meta(p)["agent-id"] == fx.A7B]
    text = torn.read_text(encoding="utf-8")
    torn.write_text(text[: text.index("\n# ---") + 1], encoding="utf-8")
    fx.append_lines(path, rest)
    capsys.readouterr()
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    assert any(torn.name in line for line in _lines(out, "refused"))
    assert len(_logs(root)) == 4
    assert len(_lines(out, "unchanged")) == 3


def test_a_cursor_missing_from_the_transcript_refuses(home, root, capsys):
    assert _ingest(root) == 0
    assert len(_of(root, fx.A7B)) == 1
    (log,) = [p for p in _logs(root) if _meta(p)["agent-id"] == fx.A7B]
    fx.cut_after_message(fx.transcript(home, fx.NESTED, fx.A7B), A7B_SECOND)
    capsys.readouterr()
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    assert any(log.name in line for line in _lines(out, "refused"))
    assert len(_logs(root)) == 4


def test_an_unknown_shape_exits_nonzero_and_records_nothing_for_that_transcript(
    home, root, capsys
):
    path = fx.transcript(home, fx.NESTED, fx.A7B)
    recs = fx.records(path)
    for rec in recs:
        if rec.get("type") == "assistant":
            rec["message"]["usage"]["output_tokens"] = "12"
            break
    fx.write_lines(path, [json.dumps(r) + "\n" for r in recs])
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    assert sorted(m["agent-id"] for m in _metas(root)) == sorted(["", fx.A23, fx.AF7])
    refused = _lines(out, "refused")
    assert len(refused) == 1
    assert path.name in refused[0] and "output_tokens" in refused[0]


SERVICE_ARMS = [
    # (the planted log's usage source, the declared result coverage, the
    # agents recorded, how many transcripts are skipped)
    ("reported", False, ["", fx.A23, fx.A7B, fx.AF7][1:], 1),
    ("reported", True, [], 4),
    ("transcript", False, ["", fx.A23, fx.A7B, fx.AF7], 0),
]


@pytest.mark.parametrize(
    "source, covers, recorded, skipped",
    SERVICE_ARMS,
    ids=["main-skipped", "all-skipped", "transcript-source-skips-nothing"],
)
def test_a_service_recorded_session_skips_its_main_transcript(
    home, root, capsys, monkeypatch, source, covers, recorded, skipped
):
    monkeypatch.setattr(ui.session_adapters, "CLAUDE_RESULT_COUNTS_SUBAGENTS", covers)
    planted = ac.write_session_log(
        _spool(root),
        {
            "session": "call_" + uuid.uuid4().hex,
            "stamp": "20261020-000000",
            "role": "ADJUDICATE",
            "phase": "ADJUDICATE",
            "session-id": fx.NESTED,
            "usage-source": source,
        },
        "",
    )
    status = _ingest(root)
    out = capsys.readouterr().out
    written = [m for p, m in zip(_logs(root), _metas(root)) if p != planted]
    assert sorted(m["agent-id"] for m in written) == sorted(recorded)
    lines = _lines(out, "skipped")
    assert len(lines) == skipped
    assert all(planted.name in line for line in lines)
    assert len(_lines(out, "recorded")) == len(recorded)
    assert status == 0


def test_no_transcript_text_reaches_any_written_log(home, root):
    plant = "PLANTED-TRANSCRIPT-TEXT-5c1e9a"

    def rewrite(path, edit):
        recs = fx.records(path)
        for rec in recs:
            edit(rec)
        fx.write_lines(path, [json.dumps(r) + "\n" for r in recs])

    def user_text(rec):
        if rec.get("type") == "user":
            rec["message"] = {"role": "user", "content": plant}

    def assistant_text(rec):
        if rec.get("type") == "assistant":
            rec["message"]["content"] += [
                {"type": "text", "text": plant},
                {"type": "thinking", "thinking": plant},
                {"type": "tool_use", "name": "Bash", "input": {"command": plant}},
            ]

    def blob_text(rec):
        if rec.get("type") == "api-request-blob":
            rec["message"] = {
                "role": "user",
                "content": [{"type": "text", "text": plant}],
            }

    rewrite(fx.transcript(home, fx.NESTED), user_text)
    rewrite(fx.transcript(home, fx.NESTED, fx.A23), assistant_text)
    rewrite(fx.transcript(home, fx.NESTED, fx.A7B), blob_text)
    meta = fx.meta(home, fx.NESTED, fx.AF7)
    data = json.loads(meta.read_text(encoding="utf-8"))
    data["description"] = plant
    meta.write_text(json.dumps(data), encoding="utf-8")
    planted_in = [
        p.name
        for p in fx.session_dir(home).rglob("*")
        if p.is_file() and plant in p.read_text(encoding="utf-8")
    ]
    assert len(planted_in) == 4
    assert _ingest(root) == 0
    logs = _logs(root)
    assert len(logs) == 4
    assert [p.read_text(encoding="utf-8").count(plant) for p in logs] == [0, 0, 0, 0]


def test_no_session_is_a_usage_error(home, root, capsys):
    assert ui.main(["--root", str(root)]) == 2
    assert _logs(root) == []


def test_an_absent_transcript_is_named(home, root, capsys):
    absent = "00000000-0000-4000-8000-000000000000"
    assert _ingest(root, absent) == 1
    out = capsys.readouterr().out
    assert any(absent in line for line in _lines(out, "absent"))
    assert _logs(root) == []


def test_a_finished_agents_hand_back_is_recorded_once(home, root, capsys):
    # The unmodified CHAIN fixture: every agent's last message is a hand-back
    # with no stop record, and each agent finished. Each is recorded at the
    # last-record sum over every unique message id, and nothing stays open.
    assert _ingest(root, fx.CHAIN) == 0
    out = capsys.readouterr().out
    assert _lines(out, "open ") == []
    metas = {m["agent-id"]: m for m in _metas(root)}
    assert sorted(metas) == sorted(["", fx.C1, fx.C2, fx.C3])
    for agent, meta in metas.items():
        path = fx.transcript(home, fx.CHAIN, agent)
        assert fx.header_four(meta) == fx.message_sums(path), agent
        assert meta["usage-status"] == ("known" if not agent else "partial"), agent
    assert _ingest(root, fx.CHAIN) == 0
    assert len(_lines(capsys.readouterr().out, "unchanged")) == 4
    assert len(_logs(root)) == 4


# --- prior logs and their headers --------------------------------------------


def _log_of(root, agent):
    (path,) = [p for p in _logs(root) if _meta(p)["agent-id"] == agent]
    return path


def test_an_unreadable_header_refuses_that_invocation_naming_it(home, root, capsys):
    # A directory under a log's name holds the invocation's one prior
    # contribution, and it cannot be opened. Adequacy witness: an ingest that
    # skipped an unreadable log as no record would record A7B again from its
    # first message, and one that let the error escape would record nothing.
    inv = ui.invocation_id(fx.NESTED, fx.A7B)
    unreadable = _spool(root) / "call_{}-20261020-000000.log".format(inv)
    unreadable.mkdir(parents=True)
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    refused = _lines(out, "refused")
    assert len(refused) == 1
    assert unreadable.name in refused[0] and "cannot be read" in refused[0]
    assert fx.A7B in refused[0]
    written = [_meta(p)["agent-id"] for p in _logs(root) if p != unreadable]
    assert sorted(written) == sorted(["", fx.A23, fx.AF7])


@pytest.mark.parametrize("key", ["message-cursor", "contribution-key"])
def test_a_header_without_its_cursor_or_key_refuses_that_invocation(
    home, root, capsys, key
):
    # Adequacy witness: an ingest that read a missing cursor as no prior
    # record would write a second A7B log of the same messages, and one that
    # checked only the cursor would report the keyless log unchanged.
    assert _ingest(root) == 0
    log = _log_of(root, fx.A7B)
    text = log.read_text(encoding="utf-8")
    stripped = re.sub(r"(?m)^# {}:.*\n".format(re.escape(key)), "", text)
    assert stripped != text
    log.write_text(stripped, encoding="utf-8")
    capsys.readouterr()
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    refused = _lines(out, "refused")
    assert len(refused) == 1
    assert log.name in refused[0] and key in refused[0]
    assert len(_lines(out, "unchanged")) == 3
    assert len(_logs(root)) == 4


def test_a_log_in_the_roots_own_record_directory_counts_and_a_name_held_twice_is_read_once(
    home, root, capsys
):
    # Adequacy witness: an ingest that read only the spool would record all
    # four invocations again once their logs sit in the root's own record
    # directory, and one that kept every path rather than every name would
    # list each of the four twice.
    assert _ingest(root) == 0
    own = root / "docs" / "iteration"
    own.mkdir(parents=True)
    names = []
    for path in _logs(root):
        path.replace(own / path.name)
        names.append(path.name)
    capsys.readouterr()
    assert _ingest(root) == 0
    assert len(_lines(capsys.readouterr().out, "unchanged")) == 4
    assert _logs(root) == []
    for name in names:
        (_spool(root) / name).write_bytes((own / name).read_bytes())
    logs = ui.recorded_logs(root)
    assert sorted(logs) == sorted(names)
    assert _ingest(root) == 0
    assert len(_lines(capsys.readouterr().out, "unchanged")) == 4
    assert sorted(p.name for p in _logs(root)) == sorted(names)


# --- the service-recorded decision -------------------------------------------


@pytest.mark.parametrize(
    "covers, refused, recorded",
    [(False, [""], [fx.A23, fx.A7B, fx.AF7]), (True, list(AGENTS), [])],
    ids=["main-governed", "all-governed"],
)
def test_an_unreadable_service_record_refuses_every_transcript_it_governs(
    home, root, capsys, monkeypatch, covers, refused, recorded
):
    # A log not named for one of the session's own invocations, cut short
    # before its header ends, could be the service's record of the session.
    # Adequacy witness: an ingest that passed over it would record the
    # session's own transcript (and, when the result covers them, its
    # sub-agents), counting usage the service may already hold.
    monkeypatch.setattr(ui.session_adapters, "CLAUDE_RESULT_COUNTS_SUBAGENTS", covers)
    planted = ac.write_session_log(
        _spool(root),
        {
            "session": "call_" + uuid.uuid4().hex,
            "stamp": "20261020-000000",
            "role": "ADJUDICATE",
            "phase": "ADJUDICATE",
            "session-id": fx.NESTED,
            "usage-source": "reported",
        },
        "",
    )
    text = planted.read_text(encoding="utf-8")
    planted.write_text(text[: text.index("\n# ---") + 1], encoding="utf-8")
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    lines = _lines(out, "refused")
    assert len(lines) == len(refused)
    assert all(planted.name in line for line in lines)
    assert sorted(line.split()[0] for line in lines) == sorted(
        "COORDINATOR" if not agent else "SUBAGENT" for agent in refused
    )
    written = [_meta(p)["agent-id"] for p in _logs(root) if p != planted]
    assert sorted(written) == sorted(recorded)
    assert len(_lines(out, "recorded")) == len(recorded)


# --- the command's selection, body and readings ------------------------------


def test_the_home_is_the_config_variable_else_the_default_never_an_account_home(
    tmp_path, root, capsys, monkeypatch
):
    # The session sits in an account home under the user config directory,
    # and in a home the config variable names; the user's own `~/.claude`
    # starts empty. Adequacy witness: a selection that ignored the variable,
    # fell back to an account home, or read the default from anywhere but
    # the user's home would record or name another home than the one below.
    keep = load_script("session_keep")
    user = tmp_path / "user"
    config = tmp_path / "config"
    for name in ("HOME", "USERPROFILE"):
        monkeypatch.setenv(name, str(user))
    for name in ("APPDATA", "XDG_CONFIG_HOME"):
        monkeypatch.setenv(name, str(config))
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    account = keep.account_home("CLAUDE-ACCT")
    assert account is not None and str(account).startswith(str(config))
    shutil.copytree(fx.FIXTURES / "projects", account / "projects")
    declared = fx.home_copy(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(declared))
    assert ui.session_adapters.claude_home(ui.os.environ) == declared
    assert _ingest(root) == 0
    assert len(_logs(root)) == 4
    capsys.readouterr()
    monkeypatch.delenv("CLAUDE_CONFIG_DIR")
    default = user / ".claude"
    assert ui.session_adapters.claude_home(ui.os.environ) == default
    other = tmp_path / "other-root"
    other.mkdir()
    assert _ingest(other, fx.CHAIN) == 1
    absent = _lines(capsys.readouterr().out, "absent")
    assert len(absent) == 1 and str(default / "projects") in absent[0]
    assert _logs(other) == []
    shutil.copytree(fx.FIXTURES / "projects", default / "projects")
    assert _ingest(other, fx.CHAIN) == 0
    assert len(_logs(other)) == 4


def test_the_ambient_session_id_is_ingested_when_none_is_named(
    home, root, capsys, monkeypatch
):
    # Adequacy witness: a command that ignored the ambient id would exit 2
    # with nothing recorded, and one that let it override `--session` would
    # record the CHAIN session in the second root.
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", fx.CHAIN)
    assert ui.main(["--root", str(root)]) == 0
    assert {m["session-id"] for m in _metas(root)} == {fx.CHAIN}
    assert len(_logs(root)) == 4
    named = root.parent / "named-root"
    named.mkdir()
    assert _ingest(named) == 0
    assert {m["session-id"] for m in _metas(named)} == {fx.NESTED}


def test_an_absent_main_transcript_is_named_and_its_sub_agents_are_recorded(
    home, root, capsys
):
    # Adequacy witness: a command that refused the whole session for its
    # missing main transcript would record no sub-agent, and one that passed
    # over the absence would exit 0 without naming it.
    main = fx.transcript(home, fx.NESTED)
    main.unlink()
    assert _ingest(root) == 1
    out = capsys.readouterr().out
    absent = _lines(out, "absent")
    assert len(absent) == 1 and main.name in absent[0]
    assert sorted(m["agent-id"] for m in _metas(root)) == sorted(AGENTS[1:])
    assert len(_lines(out, "recorded")) == 3


def test_each_log_body_is_the_fixed_summary_of_counts_ids_and_timestamps(home, root):
    # Adequacy witness: the body must equal these lines exactly, so a body
    # holding transcript text, a raw usage object or any further line, or
    # one whose counts, ids or timestamps were not the contribution's, fails.
    assert _ingest(root) == 0
    bodies = {}
    for path in _logs(root):
        text = path.read_text(encoding="utf-8")
        bodies[_meta(path)["agent-id"]] = text.split("\n# ---\n", 1)[1].splitlines()
    for agent, row in EXPECTED.items():
        fresh, cache_read, cache_write, output = row[10]
        assert bodies[agent] == [
            "usage ingest of one transcript contribution",
            "role: " + row[0],
            "messages counted: {} ({} without a stop record)".format(
                row[5], 1 if agent == fx.AF7 else 0
            ),
            "first message: {} at {}".format(row[6], row[8]),
            "last message: {} at {}".format(row[7], row[9]),
            "fresh input: {}".format(fresh),
            "cache read: {}".format(cache_read),
            "cache write: {}".format(cache_write),
            "output: {}".format(output),
            "open message: none",
        ], agent


def test_an_unresolved_parent_is_named_on_its_agents_lines(home, root, capsys):
    # Adequacy witness: a command that dropped the reader's unresolved mark
    # would print no such line, and one that refused the orphaned agents
    # would record neither and exit 1.
    fx.transcript(home, fx.NESTED, fx.A23).unlink()
    fx.meta(home, fx.NESTED, fx.A23).unlink()
    assert _ingest(root) == 0
    out = capsys.readouterr().out
    lines = _lines(out, "parent unresolved")
    assert sorted(line.split()[2] for line in lines) == sorted(
        [fx.A7B + ":", fx.AF7 + ":"]
    )
    assert all(line.endswith("parent unresolved " + fx.A23) for line in lines)
    assert sorted(m["agent-id"] for m in _metas(root)) == sorted(["", fx.A7B, fx.AF7])
