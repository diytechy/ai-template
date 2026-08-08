"""config_migrate.py — the legacy converter (SR-140, TC-154).

TC-154 permutations: each-legacy-source | lossless-value | ambiguous-value |
read-only.

The load-bearing property is the one that is easiest to lose: a value the table
cannot map must be REPORTED, never guessed. The retired gate-authority enum is
the concrete case — `attended` maps to a boundary, `single-ratify` also encoded
a cadence and `autonomous` permitted no early human checkpoint, so neither is a
number. Those two are asserted absent from the emitted document, not merely
present in the report.

This module also carries the AGREEMENT bar for the cutover: the old declared-file
reader (`agent_common.read_declared`, the Python twin of the hooks' first-line
grep) and the new TOML read are driven over the same matrix and required to give
the same answer.
"""

import tomllib

import pytest
from conftest import ROOT, load_script

MIGRATE = load_script("config_migrate")
CONFIG = load_script("config")
COMMON = load_script("agent_common")


def legacy(root, rel, text):
    path = root.joinpath(*rel.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def converted(root):
    """Convert `root` and return `(parsed document, report)`."""
    document, report = MIGRATE.convert(root)
    return tomllib.loads(document), report


# The one-word value each retired source could carry, and what it becomes. Every
# LEGACY_MAP row with a canonical key must appear here (asserted below), so a
# newly retired source cannot be added to the table without a conversion test.
MATRIX = [
    ("docs/gate-policy", "attended", "attestation.human_ratification_through", 3),
    ("docs/push-policy", "agent", "policy.push", "agent"),
    ("docs/push-policy", "agent-iteration", "policy.push", "agent-iteration"),
    ("docs/review-policy", "2", "policy.review_rounds", 2),
    ("docs/review-policy", "0", "policy.review_rounds", 0),
    ("docs/privacy-check", "true", "policy.privacy_check", True),
    ("docs/privacy-check", "false", "policy.privacy_check", False),
    ("docs/secrets-scan", "off", "policy.secrets_scan", False),
    ("docs/secrets-scan", "on", "policy.secrets_scan", True),
    # The reviewer opt-down `pre-push` actually parses. It was missing from the
    # first draft of the retired-source list (which named a `docs/critique-policy`
    # this kit has never had), and driving the hooks found it. Note the idiom is
    # opt-DOWN: absence means the STRICT answer, so a deleted file can never
    # quietly soften the gate.
    ("docs/privacy-review", "warn-unwired", "policy.privacy_review", "warn-unwired"),
    ("docs/privacy-review", "require", "policy.privacy_review", "require"),
    (
        "docs/guardrails-policy",
        "all except fable",
        "policy.guardrails",
        "all except fable",
    ),
    ("docs/guardrails-policy", "off", "policy.guardrails", "off"),
    ("docs/blackout", "12:00-19:00", "automation.blackout", "12:00-19:00"),
    ("docs/live-status", "true", "policy.live_status", True),
    ("docs/live-status", "false", "policy.live_status", False),
    ("docs/subagent-gate", "deny", "policy.subagent_gate", "deny"),
    ("docs/subagent-gate", "ask", "policy.subagent_gate", "ask"),
    ("docs/status-lint", "off", "policy.status_lint", 0),
    ("docs/status-lint", "200", "policy.status_lint", 200),
    ("docs/trajectory-check", "off", "policy.trajectory_check", False),
    ("docs/interfaces-check", "off", "policy.interfaces_check", False),
    ("docs/components-check", "off", "policy.components_check", False),
    ("docs/okf-export", "off", "policy.okf_export", False),
]

AGENTS_CSV = (
    "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
    "# a comment row the registry allows\n"
    "ANTHROPIC-OPUS-STRONG,ANTHROPIC,opus,4.8,strong,"
    "claude -p --model {model} --verbose,CLAUDE_CODE_EFFORT_LEVEL=medium,hint\n"
    "OPENAI-SOL,OPENAI,gpt-5.6-sol,5.6,medium,codex exec --model {model},,another hint\n"
)


# --- TC-154: each-legacy-source + lossless-value ------------------------------
@pytest.mark.parametrize("source,raw,key,expected", MATRIX)
def test_each_legacy_source_converts_to_its_canonical_key(
    tmp_path, source, raw, key, expected
):
    legacy(tmp_path, source, "# explanatory header\n#\n{}\n".format(raw))
    document, report = converted(tmp_path)
    section, leaf = key.split(".", 1)
    assert document[section][leaf] == expected
    assert report == [], report


def test_the_matrix_covers_every_mappable_row_of_the_table():
    # Keeps the mapping honest as data: a newly retired source added to
    # LEGACY_MAP with no conversion test fails HERE.
    tabular = {
        row.source
        for row in MIGRATE.LEGACY_MAP
        if row.key is not None and row.reader == "line"
    }
    assert tabular == {source for source, _, _, _ in MATRIX}


def test_every_canonical_target_is_a_declared_key():
    declared = set(CONFIG.DEFAULTS) | {"routes"}
    for row in MIGRATE.LEGACY_MAP:
        if row.key is not None:
            assert row.key in declared, row.source


def test_the_converter_and_the_detector_watch_the_same_sources():
    # config.py declares the mixed-source watch list, config_migrate the
    # conversion table; the two are separate files by the F5 rule, so they are
    # pinned equal here rather than shared.
    mapped = {row.source for row in MIGRATE.LEGACY_MAP if row.key is not None}
    watched = {source.path for source in CONFIG.LEGACY_SOURCES.values()}
    assert mapped == watched


def test_a_converted_document_loads_clean(tmp_path):
    for source, raw, _, _ in MATRIX:
        legacy(tmp_path, source, raw + "\n")
    legacy(tmp_path, "docs/gate-policy", "attended\n")
    legacy(tmp_path, "docs/agents.csv", AGENTS_CSV)
    legacy(tmp_path, "docs/agents-enabled", "ANTHROPIC-OPUS-STRONG\nOPENAI-SOL\n")
    document, report = MIGRATE.convert(tmp_path)
    _, findings = CONFIG.validate(tomllib.loads(document))
    assert findings == [], CONFIG.refusal_lines(findings)


def test_an_empty_repo_converts_to_a_document_that_sets_nothing(tmp_path):
    document, report = converted(tmp_path)
    assert set(document) == {"schema"}
    assert report == []


# --- TC-154: ambiguous-value --------------------------------------------------
@pytest.mark.parametrize("value", ["single-ratify", "autonomous"])
def test_an_ambiguous_gate_authority_is_reported_and_left_unwritten(tmp_path, value):
    legacy(tmp_path, "docs/gate-policy", value + "\n")
    document, report = converted(tmp_path)
    assert "attestation" not in document, "a value with no lossless target was guessed"
    (item,) = report
    assert item.source == "docs/gate-policy"
    assert item.value == value
    assert item.targets, "an ambiguous value must carry its candidate targets"
    assert all("attestation." in t for t in item.targets)


def test_an_unrecognised_gate_authority_is_reported_with_no_candidates(tmp_path):
    legacy(tmp_path, "docs/gate-policy", "semi-attended\n")
    document, report = converted(tmp_path)
    assert "attestation" not in document
    (item,) = report
    assert item.targets == ()


def test_a_non_integer_where_an_integer_was_declared_is_reported(tmp_path):
    legacy(tmp_path, "docs/review-policy", "lots\n")
    document, report = converted(tmp_path)
    assert "policy" not in document
    assert report and report[0].source == "docs/review-policy"


def test_the_ambiguity_travels_with_the_file_not_just_the_terminal(tmp_path):
    # The open question is written into the emitted document as a comment: a
    # report that only ever existed in a terminal is a report nobody reads.
    legacy(tmp_path, "docs/gate-policy", "autonomous\n")
    document, _ = MIGRATE.convert(tmp_path)
    assert "NOT CONVERTED" in document
    assert "autonomous" in document
    assert "attestation.human_ratification_through = 0" in document


# --- TC-154: read-only --------------------------------------------------------
def snapshot(root):
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_the_read_only_run_modifies_nothing(tmp_path):
    for source, raw, _, _ in MATRIX:
        legacy(tmp_path, source, raw + "\n")
    legacy(tmp_path, "docs/agents.csv", AGENTS_CSV)
    before = snapshot(tmp_path)
    document, report = MIGRATE.convert(tmp_path)
    assert document
    assert snapshot(tmp_path) == before
    assert not (tmp_path / "docs" / "config.toml").exists()


def test_writing_is_opt_in_and_never_overwrites(tmp_path):
    legacy(tmp_path, "docs/push-policy", "agent\n")
    MIGRATE.convert(tmp_path, write=True)
    target = tmp_path / "docs" / "config.toml"
    assert target.exists()
    kept = target.read_bytes()
    # An adopter's edit must survive a second conversion (SR-141's property,
    # asserted at the converter too so no caller can lose it).
    target.write_text("schema = 1\n# hand-edited\n", encoding="utf-8", newline="\n")
    edited = target.read_bytes()
    MIGRATE.convert(tmp_path, write=True)
    assert target.read_bytes() == edited != kept


def test_written_documents_use_lf_endings(tmp_path):
    legacy(tmp_path, "docs/push-policy", "agent\n")
    MIGRATE.convert(tmp_path, write=True)
    assert b"\r\n" not in (tmp_path / "docs" / "config.toml").read_bytes()


# --- routes and the consent surface ------------------------------------------
def test_the_agents_registry_converts_to_routes(tmp_path):
    legacy(tmp_path, "docs/agents.csv", AGENTS_CSV)
    document, report = converted(tmp_path)
    strong, medium = document["routes"]
    assert strong["id"] == "ANTHROPIC-OPUS-STRONG"
    assert strong["family"] == "ANTHROPIC"
    assert strong["strength"] == 3
    assert strong["argv"] == ["claude", "-p", "--model", "{model}", "--verbose"]
    assert strong["env"] == {"CLAUDE_CODE_EFFORT_LEVEL": "medium"}
    assert medium["strength"] == 2
    assert medium["env"] == {}
    # The one thing the registry cannot supply is reported rather than invented.
    assert any(item.value == "capabilities" for item in report)
    assert all(route["capabilities"] == [] for route in document["routes"])


HOSTILE_CSV = (
    "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
    'EVIL-ROUTE,ANTHROPIC,"opus"" & calc.exe &",4.8,strong,claude -p {model},,\n'
    "BAD ID!,ANTHROPIC,opus,4.8,strong,claude -p {model},,\n"
    "DUPE,ANTHROPIC,opus,4.8,strong,claude -p {model},,\n"
    "DUPE,OPENAI,gpt,5.6,medium,codex exec,,\n"
    "AGENTS-EXAMPLE-000,EXAMPLE,example,0,quick,your-cli -p,,placeholder\n"
    "GOOD-ROUTE,ANTHROPIC,opus,4.8,strong,claude -p {model},,\n"
)


def test_a_row_the_registry_reader_refuses_is_not_converted(tmp_path):
    """Every row rung `agent_route.load_registry` applies to `docs/agents.csv`
    applies to the conversion of that same file.

    The load-bearing one is the model slug: `load_registry` refuses a Model cell
    with characters outside `[A-Za-z0-9._:/-]` because the cell rides `{model}`
    into a session argv (H-4). Mirroring only the tier rung turned the migration
    into a laundering path — a row the live reader refused arrived in the
    canonical document as an ordinary route, and nothing downstream re-checked
    it.
    """
    registry = load_script("agent_route")
    legacy(tmp_path, "docs/agents.csv", HOSTILE_CSV)
    _models, errors = registry.load_registry(tmp_path / "docs" / "agents.csv")
    assert len(errors) == 3, errors  # the shell-unsafe model, the id, the dupe

    text, report = MIGRATE.convert(tmp_path)
    document = tomllib.loads(text)
    ids = [route["id"] for route in document.get("routes", [])]
    assert ids == ["DUPE", "GOOD-ROUTE"], ids
    # The payload survives ONLY as a quoted report comment naming what was
    # refused; no declared value carries it.
    live = [
        line for line in text.splitlines() if line.strip() and not line.startswith("#")
    ]
    assert not [line for line in live if "calc.exe" in line], live
    reported = " | ".join(item.value + " " + item.why for item in report)
    for expected in ("EVIL-ROUTE", "BAD ID!", "DUPE"):
        assert expected in reported, expected
    # And the placeholder ships inert, exactly as it does through load_registry:
    # a `-000` example row must not become a live route in every adopter's config.
    assert "AGENTS-EXAMPLE-000" not in reported
    assert "AGENTS-EXAMPLE-000" not in ids

    # The whole point: what IS written still loads clean.
    _, findings = CONFIG.validate(tomllib.loads(text))
    assert findings == [], CONFIG.refusal_lines(findings)


def test_the_shipped_registry_template_converts_to_no_placeholder_route(tmp_path):
    legacy(
        tmp_path,
        "docs/agents.csv",
        (ROOT / "project-trajectory" / "agents.template.csv").read_text(
            encoding="utf-8"
        ),
    )
    document, _ = converted(tmp_path)
    assert all(not route["id"].endswith("-000") for route in document["routes"]), (
        document["routes"]
    )


def test_the_legacy_weak_tier_still_reads_as_quick(tmp_path):
    legacy(
        tmp_path,
        "docs/agents.csv",
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\nR,F,m,1,weak,cmd,,\n",
    )
    document, _ = converted(tmp_path)
    assert document["routes"][0]["strength"] == 1


def test_an_out_of_vocabulary_tier_is_reported_not_guessed(tmp_path):
    legacy(
        tmp_path,
        "docs/agents.csv",
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\nR,F,m,1,titanic,cmd,,\n",
    )
    document, report = converted(tmp_path)
    assert "routes" not in document
    assert any("titanic" in item.value for item in report)


def test_presence_of_the_enable_list_becomes_explicit_consent(tmp_path):
    legacy(tmp_path, "docs/agents.csv", AGENTS_CSV)
    legacy(
        tmp_path, "docs/agents-enabled", "# header\nANTHROPIC-OPUS-STRONG\nOPENAI-SOL\n"
    )
    document, _ = converted(tmp_path)
    assert document["routing"]["enabled"] is True
    assert CONFIG.DEFAULTS["routing.enabled"] is False, (
        "consent must be the explicit value, never the default"
    )


def test_the_per_phase_weight_grammar_is_preserved(tmp_path):
    legacy(
        tmp_path,
        "docs/agents-enabled",
        "ANTHROPIC-OPUS-STRONG BUILD=3 REVIEW=0\nOPENAI-SOL CRITIQUE=4\n",
    )
    document, _ = converted(tmp_path)
    jobs = document["jobs"]
    assert [(e["route"], e["weight"]) for e in jobs["implementer"]["pool"]] == [
        ("ANTHROPIC-OPUS-STRONG", 3),
        ("OPENAI-SOL", 1),
    ]
    assert [e["weight"] for e in jobs["reviewer"]["pool"]] == [0, 1]
    assert [e["weight"] for e in jobs["critic"]["pool"]] == [1, 4]
    # A job no phase named keeps the unannotated default weight everywhere.
    assert [e["weight"] for e in jobs["planner"]["pool"]] == [1, 1]
    assert set(jobs) == set(CONFIG.JOBS)


def test_a_phase_with_no_declared_job_is_reported_not_assigned(tmp_path):
    legacy(tmp_path, "docs/agents-enabled", "ANTHROPIC-OPUS-STRONG DESIGN-CHECK=5\n")
    document, report = converted(tmp_path)
    (item,) = [i for i in report if "DESIGN-CHECK" in i.value]
    assert item.targets == ("jobs.planner", "jobs.arbiter")
    assert all(
        e["weight"] == 1 for job in document["jobs"].values() for e in job["pool"]
    )


@pytest.mark.parametrize(
    "line", ["ID BUILD=-1", "ID BUILD=x", "ID NOPHASE=1", "BUILD=2"]
)
def test_a_malformed_enable_line_is_reported(tmp_path, line):
    legacy(tmp_path, "docs/agents-enabled", line + "\n")
    _, report = converted(tmp_path)
    assert report, line


def test_the_surviving_stack_ini_dials_are_reported(tmp_path):
    legacy(
        tmp_path,
        "docs/stack.ini",
        "[paths]\nsrc = src\n\n[agent-loop]\nmodel = opus\nlanes = 4\n",
    )
    document, report = converted(tmp_path)
    assert document["automation"]["lanes"] == 4
    assert any(item.value.startswith("model =") for item in report)


# --- values the retired readers themselves disagree about ---------------------
def test_a_malformed_blackout_window_is_reported_not_round_tripped(tmp_path):
    """`docs/blackout` holding an out-of-range window must not become a config
    value that reads as a window and behaves as OFF.

    Today `agent_loop` at least WARNS off the legacy file ("the blackout window
    is DISABLED this run"). A conversion that copied the string through would
    delete the only warning that exists and leave the schema — whose whole
    purpose is to end silent-off — endorsing it.
    """
    legacy(tmp_path, "docs/blackout", "25:00-99:99\n")
    document, report = converted(tmp_path)
    assert "automation" not in document, "a window no reader accepts was written"
    (item,) = report
    assert item.source == "docs/blackout"
    assert item.value == "25:00-99:99"
    assert item.targets == ("automation.blackout",)


@pytest.mark.parametrize("raw", ["TRUE", "True"])
def test_a_case_variant_privacy_check_is_reported_not_guessed(tmp_path, raw):
    """The one value the retired sources disagree with EACH OTHER about.

    The three git hooks test `[ "$p" = "true" ]` (exact), so the commit gates saw
    `TRUE` as off; `agent_loop`/`agent_common` fold case, so the loop's identity
    check saw it as on. Neither answer is the repo's policy, so the converter
    reports it. Folding silently (what it did) turns a privacy gate ON for a repo
    whose commit hooks never enforced it; matching the hooks silently turns it
    OFF for a loop that did.
    """
    legacy(tmp_path, "docs/privacy-check", raw + "\n")
    document, report = converted(tmp_path)
    assert "policy" not in document, "a disputed value was guessed"
    (item,) = report
    assert item.source == "docs/privacy-check"
    assert item.value == raw
    assert item.targets == (
        "policy.privacy_check = true",
        "policy.privacy_check = false",
    )


def test_the_exact_lowercase_privacy_check_still_converts(tmp_path):
    # The agreed values are unaffected: every reader reads `true` the same way.
    legacy(tmp_path, "docs/privacy-check", "true\n")
    document, report = converted(tmp_path)
    assert document["policy"]["privacy_check"] is True
    assert report == []


def test_live_status_still_folds_case_because_its_only_reader_does(tmp_path):
    # `agent_loop` reads it as `.lower() == "true"` and nothing else reads it, so
    # folding is faithful here — the split token is a fidelity rule, not a style.
    legacy(tmp_path, "docs/live-status", "TRUE\n")
    document, report = converted(tmp_path)
    assert document["policy"]["live_status"] is True
    assert report == []


# --- the retired source the contract names but this kit never carried ---------
def test_a_retired_source_with_no_canonical_key_is_reported(tmp_path):
    legacy(tmp_path, "docs/critique-policy", "strict\n")
    document, report = converted(tmp_path)
    assert set(document) == {"schema"}
    (item,) = report
    assert item.source == "docs/critique-policy"
    assert item.targets == ()


# --- the agreement bar for the cutover ---------------------------------------
@pytest.mark.parametrize("source,raw,key,expected", MATRIX)
def test_old_reader_and_new_authority_agree(tmp_path, source, raw, key, expected):
    """The OLD declared-file read and the NEW TOML read, over one matrix.

    `agent_common.read_declared` is the Python twin of the hooks' first-line
    grep and is what every current caller uses; after conversion the canonical
    key must carry the SAME decision, translated into its declared type. This is
    the property the P13 cutover will lean on.
    """
    legacy(tmp_path, source, "# header\n\n{}\n".format(raw))
    old = COMMON.read_declared(tmp_path.joinpath(*source.split("/")), None)
    assert old == raw, "the old reader must still see the value we converted"
    MIGRATE.convert(tmp_path, write=True)
    cfg, findings = CONFIG.load_config(tmp_path)
    assert findings == [], CONFIG.refusal_lines(findings)
    section, leaf = key.split(".", 1)
    assert getattr(getattr(cfg, section), leaf) == expected


def test_the_converters_declared_line_matches_the_old_reader(tmp_path):
    # `declared_line` is duplicated from agent_common per the F5 rule; pinned
    # equal here over the shapes a real declared file takes.
    cases = [
        "value\n",
        "# comment\nvalue\n",
        "\n\n   \n# c\n   value   \n",
        "# only comments\n",
        "",
    ]
    for n, text in enumerate(cases):
        path = legacy(tmp_path, "docs/probe-{}".format(n), text)
        assert MIGRATE.declared_line(path) == COMMON.read_declared(path, None), text
    assert MIGRATE.declared_line(tmp_path / "docs" / "absent") is None


def test_the_committed_config_agrees_with_the_converter_wherever_the_converter_speaks():
    """Every value the converter PRODUCES must match the committed file.

    This asserted byte-equality once, and that was wrong in a way worth
    recording: `docs/config.toml` is **adopter-owned**, and this repo is its own
    adopter. It legitimately carries content the converter cannot produce —
    `[prompts.*]`, which has no retired source at all, and each route's
    `capabilities`, which `docs/agents.csv` has no column for (the converter
    emits `[]` and reports the gap, exactly as SR-140 requires).

    Byte-equality therefore forbade the one thing SR-141 exists to protect: an
    adopter filling in what conversion could not. The property that actually
    matters is **agreement where the converter speaks** — which still catches a
    converter that drifts from the committed instance, and no longer punishes a
    file for being more complete than its source.
    """
    document, report = MIGRATE.convert(ROOT)
    produced = tomllib.loads(document)
    committed = tomllib.loads(
        (ROOT / "docs" / "config.toml").read_text(encoding="utf-8")
    )

    # Fields the converter is DOCUMENTED as unable to fill. Kept as a named set
    # rather than a loose comparison so adding a third one is a decision.
    UNFILLABLE = {"capabilities"}
    assert any("capabilit" in u.why for u in report), (
        "the converter no longer reports the capability gap; if it can now fill "
        "capabilities, drop it from UNFILLABLE and compare it too"
    )

    for key, value in produced.items():
        assert key in committed, "the committed config dropped {!r}".format(key)
        if key == "routes":
            for made, have in zip(value, committed[key]):
                for field, made_value in made.items():
                    if field in UNFILLABLE:
                        continue
                    assert have.get(field) == made_value, (
                        "route {} field {} drifted".format(made.get("id"), field)
                    )
            continue
        assert committed[key] == value, (
            "{} drifted from the converter; regenerate or reconcile".format(key)
        )
