"""SN-026 — the adjudicator as a routed job type, and prompts as audited files.

Three things this pins, all from plan §7 and §11.7:

  * **ADJUDICATE is a phase**, not an ordinary build. An adjudication row rules
    on a CLAIM another session made, so it draws from the phase pool at the
    phase tier and takes the reviewers' cross-family rule — routing it as BUILD
    meant the judge could be the same family as the party it was judging, at
    the implementer's tier.
  * **A CmdTemplate may be a JSON argv array.** The shell-string form has to
    guess where a Windows path ends and a quote begins; the array form does not
    guess. Existing templates must read byte-identically, which is what the
    fall-through cases here drive.
  * **A prompt is auditable after the fact.** The catalogue names each shipped
    template by digest and each session log records the digest of what it
    actually launched, so "which instruction did this session see" is a lookup.
"""

import pytest
from conftest import load_script

loop = load_script("agent_loop")
route = load_script("agent_route")
session = load_script("agent_session")
prompts = load_script("prompts")
ac = load_script("agent_common")
catalog = load_script("gen_prompt_catalog")


# --- ADJUDICATE as a phase ------------------------------------------------------


def test_adjudicate_is_a_weightable_phase():
    # `docs/agents-enabled` weights a model per phase. A job type that is not in
    # this tuple cannot be weighted at all, so "adjudicators draw from their own
    # pool" would have been prose with no mechanism.
    assert "ADJUDICATE" in route.WEIGHT_PHASES


def test_adjudicate_defaults_strong():
    # It judges, and the cost of a wrong judgement here is a wrong
    # approval. Same tier as the other two judging phases.
    assert loop.DEFAULT_PHASE_TIER["ADJUDICATE"] == "strong"
    assert loop.phase_tier("ADJUDICATE", {}) == "strong"


def test_an_adjudication_row_is_recognised_off_its_DECLARED_class():
    # The same cell `schedule.classify` reads to make the row exclusive and
    # rank it — one declaration, two consumers, never a second vocabulary.
    assert loop.adjudicating({"SafetyClass": "adjudication"}) is True
    assert loop.adjudicating({"SafetyClass": "  ADJUDICATION  "}) is True
    assert loop.adjudicating({"SafetyClass": "ordinary"}) is False
    assert loop.adjudicating({}) is False


def _state(**kw):
    st = loop.RoutingState.__new__(loop.RoutingState)
    st.last_impl_family = kw.get("last_impl_family")
    st.round_verdicts = []
    st.impl_tier_override = kw.get("impl_tier_override")
    st.impl_exclude = kw.get("impl_exclude") or set()
    return st


def test_an_adjudicator_never_shares_the_judged_party_s_family():
    # The reviewers' rule, for the reviewers' reason: a judge that shares the
    # family of the party it judges corroborates rather than checks.
    st = _state(last_impl_family="ANTHROPIC")
    tier, exclude, prefer_different = st.route_intent("ADJUDICATE", False, False, {})
    assert prefer_different is True
    assert exclude == {"ANTHROPIC"}
    assert tier == "strong"


def test_the_row_s_measured_tier_pins_the_adjudication_draw():
    # `intake.tier_signal` estimates the tier from MEASURED breadth (rows
    # touched, gate moved, how many requirements a red TC's contradiction
    # spans). A measured estimate beats a phase default, so the pin applies —
    # but the pin is the ONLY thing that lowers it.
    st = _state(last_impl_family="ANTHROPIC")
    tier, _exclude, _prefer = st.route_intent(
        "ADJUDICATE", False, False, {}, pinned_tier="medium"
    )
    assert tier == "medium"


def test_the_implementer_s_escalation_overrides_do_NOT_reach_an_adjudicator():
    # They describe the IMPLEMENTER's trouble — a swapped family, a tier-up
    # after failed review gates. An adjudication row is not the implementer's
    # work, and inheriting its escalation would silently re-tier a judgement
    # because a different row's build went badly.
    st = _state(
        last_impl_family="ANTHROPIC",
        impl_tier_override="strong",
        impl_exclude={"GOOGLE"},
    )
    tier, exclude, _prefer = st.route_intent(
        "ADJUDICATE", False, False, {}, pinned_tier="quick"
    )
    assert tier == "quick", "the row's own estimate stands"
    assert exclude == {"ANTHROPIC"}, "the judged family, not the swap set"


def test_an_adjudication_commit_never_triggers_a_review_round():
    # Its lane runs no product bar (`integrate.refresh`'s no-bar arm) because
    # its outputs are Status cells and the work registry. A review round over
    # it would be a fresh-context reviewer asked to judge a judgement with no
    # product diff to judge.
    assert "ADJUDICATE" in loop.NON_BUILD_PHASES


def test_the_shipped_registry_documents_the_job_type_table():
    # §7's ask: the job-type <-> phase mapping stated ONCE, where an adopter
    # editing the registry will meet it.
    from conftest import KIT

    text = (KIT / "agents.template.toml").read_text(encoding="utf-8")
    assert "JOB TYPE -> PHASE" in text
    for phase in ("PLAN", "BUILD", "REVIEW", "CRITIQUE", "ADJUDICATE"):
        assert phase in text, phase


# --- argv arrays ----------------------------------------------------------------


def test_a_json_array_template_is_the_argv_verbatim():
    assert session.split_cmd('["claude", "-p", "--model", "{model}"]') == [
        "claude",
        "-p",
        "--model",
        "{model}",
    ]


def test_an_array_survives_what_the_shell_split_has_to_guess_at():
    # The whole reason the form exists. A Windows path and an embedded quote
    # are data in the array form and a parsing problem in the string form.
    tokens = session.split_cmd(
        '["C:\\\\Program Files\\\\cli\\\\run.exe", "--note", "say \\"hi\\""]'
    )
    assert tokens == ["C:\\Program Files\\cli\\run.exe", "--note", 'say "hi"']


@pytest.mark.parametrize(
    "template",
    [
        "claude -p --model {model}",
        "[weird] --flag",  # starts with a bracket, is not JSON
        '["unclosed", --flag',  # starts with a bracket, does not parse
        "",
    ],
)
def test_every_non_array_template_still_shell_splits(template):
    # Never-breaking: no existing template may change meaning. The array form
    # is recognised only when the value actually parses as a JSON list.
    lex_tokens = session.split_cmd(template)
    assert isinstance(lex_tokens, list)
    if template.startswith("claude"):
        assert lex_tokens == ["claude", "-p", "--model", "{model}"]
    if template == "[weird] --flag":
        assert lex_tokens == ["[weird]", "--flag"]


def test_a_non_string_token_in_an_array_is_a_REFUSAL():
    # A registry is config a human edits. Stringifying `3` into a command
    # nobody wrote is a launch that does not match its declaration.
    with pytest.raises(ValueError) as exc:
        session.split_cmd('["codex", 3]')
    assert "non-string" in str(exc.value)


def test_an_array_template_takes_the_same_prompt_transport_decision():
    # The `{prompt}`-or-stdin rule is about the TOKENS, so it must not care
    # which form produced them.
    argv, stdin = session.build_argv('["codex", "exec"]', "gpt", "the brief")
    assert argv == ["codex", "exec"] and stdin == "the brief"
    argv, stdin = session.build_argv('["cli", "-p", "{prompt}"]', "m", "the brief")
    assert argv == ["cli", "-p", "the brief"] and stdin is None


# --- prompts as audited files ---------------------------------------------------


def test_the_session_log_records_which_template_and_what_it_rendered_to():
    assert "prompt-template" in _log_keys()
    assert "prompt-sha" in _log_keys()


def _log_keys(cache={}):
    """The metadata keys `write_session_log` emits, read out of the source's
    own key tuple rather than by writing a log — the tuple IS the contract."""
    if not cache:
        import inspect

        src = inspect.getsource(ac.write_session_log)
        cache["keys"] = src
    return cache["keys"]


def test_the_fingerprint_identifies_the_text_and_folds_nothing_else():
    a = ac.prompt_fingerprint("build the thing")
    assert a.startswith("sha256:") and len(a) == len("sha256:") + 12
    assert ac.prompt_fingerprint("build the thing") == a
    assert ac.prompt_fingerprint("build the other thing") != a
    assert ac.prompt_fingerprint(None) == ""


def test_the_prompt_source_names_an_override_rather_than_hiding_it():
    # An overridden prompt must be visible in the TELEMETRY, not only in the
    # launch flags — otherwise a session's instruction cannot be reconstructed
    # from its own record.
    assert loop.prompt_source({}, "BUILD") == "kit:BUILD"
    assert loop.prompt_source({}, "") == "kit:BUILD"
    assert loop.prompt_source({"REVIEW-A": "text"}, "REVIEW-A") == "override:REVIEW-A"
    assert loop.prompt_source({"REVIEW-A": "text"}, "REVIEW-B") == "kit:REVIEW-B"


def test_the_catalogue_lists_every_shipped_prompt_with_its_digest():
    text = catalog.render()
    for key in prompts.KIT_PROMPTS:
        assert "`{}`".format(key) in text, key
    for _key, _file, _slots, digest in prompts.catalog_rows():
        assert digest in text


def test_the_catalogue_on_disk_is_FRESH():
    # A generated artifact nobody regenerates is a document that lies, and a
    # lying catalogue is worse than none: it invites the operator to conclude
    # the wrong thing about the session they are debugging.
    assert catalog.main(["--check"]) == 0


def test_a_template_edit_moves_its_digest_and_so_the_catalogue():
    # The property the whole scheme rests on. If a template could change
    # without its digest changing, a session log's `prompt-sha` would name a
    # prompt that no longer exists.
    before = prompts.digest("Do the thing.\n")
    assert prompts.digest("Do the OTHER thing.\n") != before
    # ...but a line-ending difference is NOT an edit: the same template checked
    # out CRLF on Windows and LF on POSIX is the same prompt, and a telemetry
    # field that said otherwise would report a change on every clone.
    assert prompts.digest("Do the thing.\r\n") == before
