"""The Claude Code transcript reader in `session_adapters`: one session and
its sub-agents at any depth, each counted once per message id, with every
shape it does not know refused by file and field.

The reader runs over tmp copies of the cut fixtures in
`tests/golden/sessions/claude-transcripts/` (provenance:
`claude_transcript_fixtures`). Open tails, duplicated records, planted values
and malformed shapes are made in the copies, never in the committed
fixtures.
"""

import json
import shutil

import pytest
from conftest import load_script

import claude_transcript_fixtures as fx

adapters = load_script("session_adapters")

# The usage of each NESTED invocation: the sum over its unique message ids,
# each message's last record (fresh input, cache read, cache write, output),
# with the reasoning count where every counted stop record reports one.
NESTED_USAGE = {
    "": ((10, 300817, 48807, 2694), 349634, 811),
    fx.A23: ((10, 231724, 34351, 2701), 266085, 327),
    fx.A7B: ((8, 172821, 36977, 1303), 209806, 10),
    fx.AF7: ((14, 381334, 65887, 3349), 447235, ""),
}


def _read(home, session=fx.NESTED):
    return adapters.claude_session(home, session)


def _by_agent(read):
    return {inv.agent_id: inv for inv in read.invocations}


def _inv(home, agent, session=fx.NESTED):
    """The one invocation `agent` of `session`, asserted present."""
    found = _by_agent(_read(home, session))
    assert agent in found, sorted(found)
    return found[agent]


def _usage(inv):
    return adapters.transcript_usage(inv.messages)


def test_a_session_with_nested_agents_yields_four_invocations_with_their_identities(
    tmp_path,
):
    home = fx.home_copy(tmp_path)
    read = _read(home)
    identities = [
        (
            inv.session_id,
            inv.agent_id,
            inv.parent_agent_id,
            inv.depth,
            inv.agent_type,
            inv.request_model,
            _usage(inv)["gen_ai.response.model"],
            inv.messages[0].started_at,
            inv.messages[-1].ended_at,
        )
        for inv in read.invocations
    ]
    opus = "claude-opus-5-5"
    assert identities == [
        (
            fx.NESTED,
            "",
            "",
            0,
            "",
            "",
            opus,
            "2026-10-20T02:47:48.470Z",
            "2026-10-20T02:48:06.899Z",
        ),
        (
            fx.NESTED,
            fx.A23,
            "",
            1,
            "general-purpose",
            "opus",
            opus,
            "2026-10-20T07:58:49.804Z",
            "2026-10-20T07:59:18.271Z",
        ),
        (
            fx.NESTED,
            fx.A7B,
            fx.A23,
            2,
            "general-purpose",
            "",
            opus,
            "2026-10-20T07:59:19.580Z",
            "2026-10-20T07:59:33.864Z",
        ),
        (
            fx.NESTED,
            fx.AF7,
            fx.A23,
            2,
            "general-purpose",
            "",
            opus,
            "2026-10-20T09:05:45.737Z",
            "2026-10-20T09:06:32.027Z",
        ),
    ]
    assert all(inv.parent_resolved for inv in read.invocations)
    assert [inv.open_message for inv in read.invocations] == ["", "", "", ""]
    assert read.refusals == () and read.absent == ()


def test_each_invocation_usage_is_its_unique_message_sum(tmp_path):
    home = fx.home_copy(tmp_path)
    found = {
        agent: (fx.four(_usage(inv)), _usage(inv)["gen_ai.usage.input_tokens"])
        for agent, inv in _by_agent(_read(home)).items()
    }
    assert found == {
        a: (counts, total) for a, (counts, total, _) in NESTED_USAGE.items()
    }
    reasoning = {
        a: _usage(inv)["gen_ai.usage.reasoning.output_tokens"]
        for a, inv in _by_agent(_read(home)).items()
    }
    # AF7 counts a message with no stop record, so its reasoning is unknown.
    assert reasoning == {a: r for a, (_, _, r) in NESTED_USAGE.items()}
    assert [m.stopped for m in _inv(home, fx.AF7).messages].count(False) == 1
    # Adequacy witness: over the same fixture, counting every record, or each
    # message's first record, gives other totals than the literal ones above,
    # so a reader that did either would fail here.
    literal = [NESTED_USAGE[a][0] for a in ("", fx.A23, fx.A7B, fx.AF7)]
    paths = [fx.transcript(home, fx.NESTED, a) for a in ("", fx.A23, fx.A7B, fx.AF7)]
    assert [fx.message_sums(p, "last") for p in paths] == literal
    assert [fx.message_sums(p, "all") for p in paths] != literal
    assert [fx.message_sums(p, "first") for p in paths] != literal


def test_a_repeated_record_adds_nothing(tmp_path):
    home = fx.home_copy(tmp_path)
    path = fx.transcript(home, fx.NESTED, fx.A23)
    lines = fx.read_lines(path)
    out = []
    for line in lines:
        rec = json.loads(line)
        if rec.get("type") == "assistant" and rec["message"]["stop_reason"]:
            # an earlier, partial record of the same message, then the
            # record itself twice, verbatim
            partial = json.loads(line)
            partial["message"]["stop_reason"] = None
            partial["message"]["usage"]["output_tokens"] = 1
            out += [json.dumps(partial) + "\n", line, line]
        else:
            out.append(line)
    fx.write_lines(path, out)
    inv = _inv(home, fx.A23)
    assert fx.four(_usage(inv)) == NESTED_USAGE[fx.A23][0]
    assert len(inv.messages) == 5


def test_the_parents_tool_result_summary_is_never_read(tmp_path):
    home = fx.home_copy(tmp_path)
    path = fx.transcript(home, fx.CHAIN)
    summaries = [r for r in fx.records(path) if "toolUseResult" in r]
    assert summaries and summaries[0]["toolUseResult"]["usage"]["output_tokens"] == 187
    planted = []
    for rec in fx.records(path):
        if "toolUseResult" in rec:
            for key in fx.COUNTS:
                rec["toolUseResult"]["usage"][key] = 10**9
        planted.append(json.dumps(rec) + "\n")
    planted.insert(
        3,
        json.dumps(
            {
                "type": "attachment",
                "sessionId": fx.CHAIN,
                "timestamp": "2026-10-22T22:59:50.000Z",
                "attachment": {"usage": {k: 10**9 for k in fx.COUNTS}},
            }
        )
        + "\n",
    )
    fx.write_lines(path, planted)
    main = _inv(home, "", fx.CHAIN)
    assert fx.four(_usage(main)) == (4, 47798, 11300, 380)


MAIN_LAST = "msg_011CgCj4nzLMqZqD4bySDZb7"  # NESTED's own last message
MAIN_FOURTH = "msg_011CgCj4aj8xjqzuHALLTaYy"


def _edit_records_of(path, message_id, edit):
    """Apply `edit` to every assistant record of `message_id` at `path`."""
    out = []
    for rec in fx.records(path):
        if rec.get("type") == "assistant" and rec["message"]["id"] == message_id:
            edit(rec)
        out.append(json.dumps(rec) + "\n")
    fx.write_lines(path, out)


def test_the_response_model_is_the_last_counted_model_not_named_synthetic(tmp_path):
    # Adequacy witness: the session's last message is renamed `<synthetic>`
    # and the one before it given a model of its own, so a reader that took
    # the last message's model regardless (`<synthetic>`) or the first
    # message's (the opus model) would fail here.
    home = fx.home_copy(tmp_path)
    path = fx.transcript(home, fx.NESTED)
    _edit_records_of(path, MAIN_FOURTH, lambda r: r["message"].update(model="m-own"))
    _edit_records_of(
        path, MAIN_LAST, lambda r: r["message"].update(model="<synthetic>")
    )
    main = _inv(home, "")
    assert [m.model for m in main.messages][-2:] == ["m-own", "<synthetic>"]
    assert main.messages[0].model == "claude-opus-5-5"
    assert _usage(main)["gen_ai.response.model"] == "m-own"


def test_the_main_sum_equals_the_clis_own_result(tmp_path):
    home = fx.home_copy(tmp_path)
    session, usage = fx.result_usage()
    assert session == fx.CHAIN
    line = json.dumps({"type": "result", "session_id": session, "usage": usage})
    reported = adapters.adapter_for(["claude"]).usage(line)
    main = _inv(home, "", fx.CHAIN)
    keys = (
        "gen_ai.usage.input_tokens",
        "gen_ai.usage.cache_read.input_tokens",
        "gen_ai.usage.cache_write.input_tokens",
        "gen_ai.usage.output_tokens",
    )
    assert [_usage(main)[k] for k in keys] == [reported[k] for k in keys]


def test_an_open_last_message_is_named_and_not_counted(tmp_path):
    home = fx.home_copy(tmp_path)
    path = fx.transcript(home, fx.NESTED, fx.AF7)
    removed = fx.cut_after_first_record(path, fx.AF7_LAST)
    inv = _inv(home, fx.AF7)
    assert inv.open_message == fx.AF7_LAST
    assert fx.AF7_LAST not in [m.id for m in inv.messages]
    # the full sum less the last message's final counts (2, 79233, 9565, 1526)
    assert fx.four(_usage(inv)) == (12, 302101, 56322, 1823)
    fx.append_lines(path, removed)
    inv = _inv(home, fx.AF7)
    assert inv.open_message == ""
    assert [m.id for m in inv.messages].count(fx.AF7_LAST) == 1
    assert inv.messages[-1].output == 1526
    assert fx.four(_usage(inv)) == NESTED_USAGE[fx.AF7][0]


def test_a_message_without_a_stop_record_is_final_once_a_later_message_follows(
    tmp_path,
):
    home = fx.home_copy(tmp_path)
    inv = _inv(home, fx.AF7)
    held = [m for m in inv.messages if m.id == fx.AF7_NO_STOP]
    assert len(held) == 1
    assert (held[0].output, held[0].stopped) == (16, False)
    assert [m.stopped for m in inv.messages].count(False) == 1
    assert inv.open_message == ""
    # The same message as the transcript's last is open, and not counted.
    fx.cut_after_message(fx.transcript(home, fx.NESTED, fx.AF7), fx.AF7_NO_STOP)
    inv = _inv(home, fx.AF7)
    assert inv.open_message == fx.AF7_NO_STOP
    assert fx.AF7_NO_STOP not in [m.id for m in inv.messages]
    assert len(inv.messages) == 4


def test_a_finished_agents_unstopped_hand_back_is_counted_at_its_last_record(
    tmp_path,
):
    # The unmodified CHAIN fixture: each agent's hand-back has no stop record
    # and no later message, but its parent's tool result for the agent's call
    # follows it, so the agent finished and the message is final.
    home = fx.home_copy(tmp_path)
    read = _read(home, fx.CHAIN)
    found = {
        inv.agent_id: (inv.open_message, fx.four(_usage(inv)), inv.messages[-1].id)
        for inv in read.invocations
    }
    assert found == {
        agent: ("", fx.message_sums(fx.transcript(home, fx.CHAIN, agent)), last)
        for agent, last in (
            ("", "msg_011CgJ77b5PVsdCCRk72wpqd"),
            (fx.C1, fx.C1_LAST),
            (fx.C2, fx.C2_LAST),
            (fx.C3, fx.C3_LAST),
        )
    }
    # Adequacy witness: those sums hold each hand-back's counts, so a reader
    # that left the hand-backs open would fall short of them.
    assert fx.four(_usage(_by_agent(read)[fx.C3])) == (6, 20258, 20684, 379)


def test_an_agent_with_no_evidence_of_finishing_keeps_its_last_message_open(
    tmp_path,
):
    home = fx.home_copy(tmp_path)
    parent = fx.transcript(home, fx.CHAIN, fx.C2)
    lines = fx.read_lines(parent)
    at = fx.tool_result_line(parent, fx.C3_TOOL_USE)
    # Evidence older than the message is no evidence: an agent resumed after
    # a finish is writing again.
    early = json.loads(lines[at])
    early["timestamp"] = "2026-10-22T23:00:03.000Z"
    fx.write_lines(parent, lines[:at] + [json.dumps(early) + "\n"] + lines[at + 1 :])
    assert _inv(home, fx.C3, fx.CHAIN).open_message == fx.C3_LAST
    # No evidence at all: still open, and not counted.
    fx.write_lines(parent, lines[:at] + lines[at + 1 :])
    inv = _inv(home, fx.C3, fx.CHAIN)
    assert inv.open_message == fx.C3_LAST
    assert fx.four(_usage(inv)) == (2, 0, 20258, 376)
    # The other agents keep their own evidence.
    assert _inv(home, fx.C2, fx.CHAIN).open_message == ""


def test_a_background_agents_task_notice_makes_its_last_message_final(tmp_path):
    home = fx.home_copy(tmp_path)
    path = fx.transcript(home, fx.NESTED, fx.AF7)
    fx.cut_after_message(path, fx.AF7_NO_STOP)
    assert _inv(home, fx.AF7).open_message == fx.AF7_NO_STOP
    fx.append_lines(
        fx.transcript(home, fx.NESTED),
        [fx.task_notice(fx.NESTED, fx.AF7, "2026-10-20T09:06:10.000Z")],
    )
    inv = _inv(home, fx.AF7)
    assert inv.open_message == ""
    assert inv.messages[-1].id == fx.AF7_NO_STOP
    assert fx.four(_usage(inv)) == fx.message_sums(path)


def test_no_finish_notice_finishes_the_sessions_own_last_message(tmp_path):
    # The session's own last message loses its stop reason, and the session's
    # transcript then holds, after it, a task notice naming the session's own
    # id, a task notice naming a sub-agent, and a tool result. The sub-agent's
    # notice finishes the sub-agent (it is timely and well formed), but the
    # session's own message stays open and uncounted. Adequacy witness: a
    # reader that let any timely notice finish any transcript's last message,
    # or gave the session's own transcript a finish key (its session id, or a
    # call's tool result), would count it here.
    home = fx.home_copy(tmp_path)
    main = fx.transcript(home, fx.NESTED)
    _edit_records_of(main, MAIN_LAST, lambda r: r["message"].update(stop_reason=None))
    fx.cut_after_message(fx.transcript(home, fx.NESTED, fx.AF7), fx.AF7_NO_STOP)
    later = "2026-10-20T10:00:00.000Z"
    result = {
        "type": "user",
        "sessionId": fx.NESTED,
        "timestamp": later,
        "message": {
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": "toolu_0own"}],
        },
    }
    fx.append_lines(
        main,
        [
            fx.task_notice(fx.NESTED, fx.NESTED, later),
            fx.task_notice(fx.NESTED, fx.AF7, later),
            json.dumps(result) + "\n",
        ],
    )
    found = _by_agent(_read(home))
    assert found[fx.AF7].open_message == ""
    assert found[fx.AF7].messages[-1].id == fx.AF7_NO_STOP
    own = found[""]
    assert own.open_message == MAIN_LAST
    assert MAIN_LAST not in [m.id for m in own.messages]
    assert len(own.messages) == 4


# --- the closed shape -----------------------------------------------------------


def _edit_assistant(home, agent, edit):
    """Apply `edit` to the first assistant record of a NESTED transcript."""
    path = fx.transcript(home, fx.NESTED, agent)
    out, done = [], False
    for rec in fx.records(path):
        if rec.get("type") == "assistant" and not done:
            edit(rec)
            done = True
        out.append(json.dumps(rec) + "\n")
    fx.write_lines(path, out)


def _first_record(home, agent, edit):
    path = fx.transcript(home, fx.NESTED, agent)
    recs = fx.records(path)
    edit(recs[0])
    fx.write_lines(path, [json.dumps(r) + "\n" for r in recs])


def _torn(home, agent):
    path = fx.transcript(home, fx.NESTED, agent)
    lines = fx.read_lines(path)
    lines.insert(5, lines[5][: len(lines[5]) // 2] + "\n")
    fx.write_lines(path, lines)


def _edit_meta(home, agent, edit):
    path = fx.meta(home, fx.NESTED, agent)
    data = json.loads(path.read_text(encoding="utf-8"))
    edit(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def _drop(key):
    def edit(node):
        node.pop(key)

    return edit


def _drop_message(key):
    def edit(rec):
        rec["message"].pop(key)

    return edit


def _set(key, value):
    def edit(node):
        node[key] = value

    return edit


def _string_count(rec):
    rec["message"]["usage"]["output_tokens"] = "12"


def _no_meta(home):
    fx.meta(home, fx.NESTED, fx.A7B).unlink()


def _no_transcript(home):
    fx.transcript(home, fx.NESTED, fx.A7B).unlink()


def _workflows(home):
    flow = fx.session_dir(home) / fx.NESTED / "subagents" / "workflows" / "wf_1"
    flow.mkdir(parents=True)
    shutil.copy(fx.transcript(home, fx.NESTED, fx.A7B), flow / "agent-a1.jsonl")


# (id, the change, the agent whose transcript it refuses ("" the session's
# own, None no transcript), a token of the file named, the field named)
SHAPES = [
    (
        "unknown-type",
        lambda h: _first_record(h, fx.A7B, _set("type", "telepathy")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "type",
    ),
    (
        "missing-type",
        lambda h: _first_record(h, fx.A7B, _drop("type")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "type",
    ),
    ("torn-line", lambda h: _torn(h, fx.A7B), fx.A7B, fx.A7B + ".jsonl", "line"),
    (
        "no-message-id",
        lambda h: _edit_assistant(h, fx.A7B, _drop_message("id")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "message.id",
    ),
    (
        "no-message-model",
        lambda h: _edit_assistant(h, fx.A7B, _drop_message("model")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "message.model",
    ),
    (
        "no-timestamp",
        lambda h: _edit_assistant(h, fx.A7B, _drop("timestamp")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "timestamp",
    ),
    (
        "no-stop-reason-key",
        lambda h: _edit_assistant(h, fx.A7B, _drop_message("stop_reason")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "message.stop_reason",
    ),
    (
        "no-usage",
        lambda h: _edit_assistant(h, fx.A7B, _drop_message("usage")),
        fx.A7B,
        fx.A7B + ".jsonl",
        "message.usage",
    ),
    (
        "string-count",
        lambda h: _edit_assistant(h, fx.A7B, _string_count),
        fx.A7B,
        fx.A7B + ".jsonl",
        "output_tokens",
    ),
    (
        "other-session",
        lambda h: _edit_assistant(h, fx.A7B, _set("sessionId", fx.CHAIN)),
        fx.A7B,
        fx.A7B + ".jsonl",
        "sessionId",
    ),
    (
        "other-agent",
        lambda h: _edit_assistant(h, fx.A7B, _set("agentId", fx.AF7)),
        fx.A7B,
        fx.A7B + ".jsonl",
        "agentId",
    ),
    (
        "main-sidechain",
        lambda h: _edit_assistant(h, "", _set("isSidechain", True)),
        "",
        fx.NESTED + ".jsonl",
        "isSidechain",
    ),
    (
        "meta-no-depth",
        lambda h: _edit_meta(h, fx.A7B, _drop("spawnDepth")),
        fx.A7B,
        fx.A7B + ".meta.json",
        "spawnDepth",
    ),
    (
        "meta-bool-depth",
        lambda h: _edit_meta(h, fx.A7B, _set("spawnDepth", True)),
        fx.A7B,
        fx.A7B + ".meta.json",
        "spawnDepth",
    ),
    # A depth below 1 is refused: a reader that checked only the type would
    # keep these agents.
    (
        "meta-zero-depth",
        lambda h: _edit_meta(h, fx.A7B, _set("spawnDepth", 0)),
        fx.A7B,
        fx.A7B + ".meta.json",
        "spawnDepth",
    ),
    (
        "meta-negative-depth",
        lambda h: _edit_meta(h, fx.A7B, _set("spawnDepth", -1)),
        fx.A7B,
        fx.A7B + ".meta.json",
        "spawnDepth",
    ),
    (
        "meta-no-type",
        lambda h: _edit_meta(h, fx.A7B, _drop("agentType")),
        fx.A7B,
        fx.A7B + ".meta.json",
        "agentType",
    ),
    (
        "meta-no-parent",
        lambda h: _edit_meta(h, fx.A7B, _drop("parentAgentId")),
        fx.A7B,
        fx.A7B + ".meta.json",
        "parentAgentId",
    ),
    ("no-meta", _no_meta, fx.A7B, fx.A7B + ".meta.json", "meta"),
    # A meta whose transcript is missing is refused naming the transcript: a
    # reader that skipped the unpaired meta silently would name nothing.
    ("no-transcript", _no_transcript, fx.A7B, fx.A7B + ".jsonl", "transcript"),
    ("workflows", _workflows, None, "workflows", ""),
]


@pytest.mark.parametrize(
    "change, refused, file_token, field",
    [s[1:] for s in SHAPES],
    ids=[s[0] for s in SHAPES],
)
def test_an_unknown_shape_is_refused_naming_file_and_field(
    tmp_path, change, refused, file_token, field
):
    home = fx.home_copy(tmp_path)
    change(home)
    read = _read(home)
    assert len(read.refusals) == 1
    refusal = read.refusals[0]
    assert isinstance(refusal, adapters.TranscriptRefused)
    assert file_token in refusal.path
    assert field in refusal.field and refusal.field
    kept = [inv.agent_id for inv in read.invocations]
    every = ["", fx.A23, fx.A7B, fx.AF7]
    assert kept == [a for a in every if a != refused]


def test_a_depth_two_agent_whose_parent_is_absent_is_kept_and_named_unresolved(
    tmp_path,
):
    home = fx.home_copy(tmp_path)
    fx.transcript(home, fx.NESTED, fx.A23).unlink()
    fx.meta(home, fx.NESTED, fx.A23).unlink()
    read = _read(home)
    found = [
        (inv.agent_id, inv.parent_agent_id, inv.parent_resolved)
        for inv in read.invocations
    ]
    assert found == [
        ("", "", True),
        (fx.A7B, fx.A23, False),
        (fx.AF7, fx.A23, False),
    ]
    # its usage is real and kept
    assert fx.four(_usage(_by_agent(read)[fx.A7B])) == NESTED_USAGE[fx.A7B][0]
    assert read.refusals == ()


def test_any_spawn_depth_is_accepted_and_recorded(tmp_path):
    home = fx.home_copy(tmp_path)
    read = _read(home, fx.CHAIN)
    found = [
        (inv.agent_id, inv.depth, inv.parent_agent_id, inv.parent_resolved)
        for inv in read.invocations
    ]
    assert found == [
        ("", 0, "", True),
        (fx.C1, 1, "", True),
        (fx.C2, 2, fx.C1, True),
        (fx.C3, 3, fx.C2, True),
    ]


def test_a_session_held_in_two_project_directories_is_refused_naming_both(tmp_path):
    home = fx.home_copy(tmp_path)
    first = fx.transcript(home, fx.CHAIN)
    other = home / "projects" / "elsewhere"
    other.mkdir()
    second = other / first.name
    shutil.copy(first, second)
    read = _read(home, fx.CHAIN)
    assert read.invocations == ()
    assert len(read.refusals) == 1
    named = str(read.refusals[0]).replace("\\", "/")
    assert "projects/" + fx.SLUG in named and "projects/elsewhere" in named
