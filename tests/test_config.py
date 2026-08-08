"""config.py — the single configuration authority (SR-137/SR-138, TC-150/TC-151).

The whole value of one authority is that it REFUSES what it does not understand,
so the refusals are tested as hard as the happy path: an unknown key, a wrong
type, an out-of-range value and an unsupported schema each have to name the
offending key, and one run has to report ALL of them rather than the first.

TC-150 permutations: well-formed | unknown-key | wrong-type | bad-schema-version
| absent-file.
TC-151 permutations: both-live | canonical-only | legacy-only.
"""

import tomllib

import pytest
from conftest import KIT, ROOT, load_script

CONFIG = load_script("config")
MIGRATE = load_script("config_migrate")

WELL_FORMED = """schema = 1

[attestation]
human_ratification_through = 2
final_full_spine_review = "always"

[automation]
lanes = 3
session_timeout_seconds = 600
blackout = "12:00-19:00"

[policy]
push = "agent"
privacy_check = true
secrets_scan = false
review_rounds = 2
guardrails = "all except fable"
subagent_gate = "ask"
live_status = true
status_lint = 0
trajectory_check = false
interfaces_check = false
components_check = false
okf_export = false

[outcomes]
complete_sampling_rate = 0.25
risk_safety_classes = ["spine", "gate"]

[admission]
max_batch_size = 4

[routing]
enabled = true

[[routes]]
id = "ANTHROPIC-OPUS-STRONG"
family = "ANTHROPIC"
model = "opus"
strength = 3
argv = ["claude", "-p", "--model", "{model}"]
env = { CLAUDE_CODE_EFFORT_LEVEL = "medium" }
capabilities = ["text", "review"]
notes = "install/sign-in hint"

[jobs.reviewer]
minimum_strength = 2
fallback = "same-or-higher"
prefer_cross_family = true
pool = [ { route = "ANTHROPIC-OPUS-STRONG", weight = 1 } ]

[prompts.reviewer]
template = "project-trajectory/prompts/reviewer.md"
required_slots = ["WI_ID", "SCOPE"]
allowed_sources = ["registry"]
prohibited_sources = ["self-assessment"]
output_schema = "review-v1"
"""


def write_config(root, text):
    """Put `text` at <root>/docs/config.toml and return root."""
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "config.toml").write_text(text, encoding="utf-8", newline="\n")
    return root


def keys(findings):
    return [f.key for f in findings]


# --- TC-150: well-formed ------------------------------------------------------
def test_well_formed_document_loads_to_a_typed_model(tmp_path):
    cfg, findings = CONFIG.load_config(write_config(tmp_path, WELL_FORMED))
    assert findings == []
    assert cfg.schema == 1
    assert cfg.policy.push == "agent"
    assert cfg.policy.privacy_check is True
    assert cfg.policy.review_rounds == 2
    assert cfg.attestation.human_ratification_through == 2
    assert cfg.automation.lanes == 3
    assert cfg.automation.blackout == "12:00-19:00"
    assert cfg.outcomes.complete_sampling_rate == 0.25
    assert cfg.outcomes.risk_safety_classes == ("spine", "gate")
    assert cfg.admission.max_batch_size == 4
    assert cfg.routing.enabled is True


def test_well_formed_routes_jobs_and_prompts_are_typed(tmp_path):
    cfg, findings = CONFIG.load_config(write_config(tmp_path, WELL_FORMED))
    assert findings == []
    (route,) = cfg.routes
    assert route.id == "ANTHROPIC-OPUS-STRONG"
    assert route.strength == 3
    assert route.argv == ("claude", "-p", "--model", "{model}")
    assert route.env == {"CLAUDE_CODE_EFFORT_LEVEL": "medium"}
    (entry,) = cfg.jobs["reviewer"].pool
    assert (entry.route, entry.weight) == ("ANTHROPIC-OPUS-STRONG", 1)
    assert cfg.prompts["reviewer"].output_schema == "review-v1"
    assert cfg.prompts["reviewer"].prohibited_sources == ("self-assessment",)


def test_typed_access_refuses_an_undeclared_attribute(tmp_path):
    # The point of the typed model: a typo raises HERE, naming the section,
    # rather than yielding None three modules away.
    cfg, _ = CONFIG.load_config(write_config(tmp_path, WELL_FORMED))
    with pytest.raises(AttributeError) as exc:
        cfg.policy.review_round
    assert "policy.review_round" in str(exc.value)
    with pytest.raises(AttributeError):
        cfg.policy.push = "human"


# --- TC-150: absent-file ------------------------------------------------------
def test_absent_file_yields_the_declared_defaults(tmp_path):
    cfg, findings = CONFIG.load_config(tmp_path)
    assert findings == [], "an absent config is not a finding — it is the default"
    assert cfg.policy.push == CONFIG.DEFAULTS["policy.push"]
    assert cfg.policy.review_rounds == 1
    assert cfg.routes == ()
    assert cfg.jobs == {}


def test_an_absent_key_resolves_exactly_like_an_absent_file(tmp_path):
    # LLR-156's whole claim, made mechanical.
    empty, _ = CONFIG.load_config(tmp_path)
    partial, findings = CONFIG.load_config(
        write_config(tmp_path, 'schema = 1\n\n[policy]\npush = "agent"\n')
    )
    assert findings == []
    for path, default in CONFIG.DEFAULTS.items():
        if path == "policy.push":
            continue
        assert partial.get(path) == default == empty.get(path), path


# --- TC-150: unknown-key ------------------------------------------------------
def test_unknown_key_is_refused_by_name(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(tmp_path, "schema = 1\n\n[policy]\nprivacy_chek = true\n")
    )
    assert keys(findings) == ["policy.privacy_chek"]


def test_unknown_section_is_refused_by_name(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(tmp_path, "schema = 1\n\n[polciy]\npush = 'agent'\n")
    )
    assert keys(findings) == ["polciy"]


def test_unknown_route_field_and_job_name_are_refused(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(
            tmp_path,
            'schema = 1\n\n[[routes]]\nid = "R"\nfamily = "F"\nmodel = "m"\n'
            'tier = "strong"\n\n[jobs.reviewr]\nminimum_strength = 2\n',
        )
    )
    assert "routes[0].tier" in keys(findings)
    assert "jobs.reviewr" in keys(findings)


def test_every_problem_is_reported_not_just_the_first(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(
            tmp_path,
            "schema = 1\n\n[policy]\nbogus_one = 1\nbogus_two = 2\n"
            'review_rounds = "1"\n\n[bogus_section]\nx = 1\n',
        )
    )
    assert set(keys(findings)) == {
        "policy.bogus_one",
        "policy.bogus_two",
        "policy.review_rounds",
        "bogus_section",
    }


# --- TC-150: wrong-type -------------------------------------------------------
@pytest.mark.parametrize(
    "body,key",
    [
        ('[policy]\nreview_rounds = "1"\n', "policy.review_rounds"),
        ("[policy]\npush = 3\n", "policy.push"),
        ("[policy]\nprivacy_check = 1\n", "policy.privacy_check"),
        ("[automation]\nlanes = true\n", "automation.lanes"),
        (
            "[automation]\nsession_timeout_seconds = 1.5\n",
            "automation.session_timeout_seconds",
        ),
        ('[outcomes]\nrisk_safety_classes = "spine"\n', "outcomes.risk_safety_classes"),
        ("[outcomes]\nrisk_safety_classes = [1, 2]\n", "outcomes.risk_safety_classes"),
        ("[routing]\nenabled = 1\n", "routing.enabled"),
    ],
)
def test_wrong_typed_value_is_refused_by_name(tmp_path, body, key):
    _, findings = CONFIG.load_config(write_config(tmp_path, "schema = 1\n\n" + body))
    assert keys(findings) == [key]


def test_a_boolean_is_never_accepted_as_an_integer(tmp_path):
    # `True` IS an int in Python, so an isinstance check would let this through
    # and `lanes = true` would silently mean one lane.
    cfg, findings = CONFIG.load_config(
        write_config(tmp_path, "schema = 1\n\n[automation]\nlanes = true\n")
    )
    assert keys(findings) == ["automation.lanes"]
    assert cfg.automation.lanes == CONFIG.DEFAULTS["automation.lanes"]


@pytest.mark.parametrize(
    "body,key",
    [
        (
            "[attestation]\nhuman_ratification_through = 9\n",
            "attestation.human_ratification_through",
        ),
        (
            "[attestation]\nhuman_ratification_through = -1\n",
            "attestation.human_ratification_through",
        ),
        (
            '[attestation]\nfinal_full_spine_review = "sometimes"\n',
            "attestation.final_full_spine_review",
        ),
        ("[policy]\nreview_rounds = 3\n", "policy.review_rounds"),
        ('[policy]\npush = "nobody"\n', "policy.push"),
        ('[policy]\nsubagent_gate = "maybe"\n', "policy.subagent_gate"),
        ("[policy]\nstatus_lint = -5\n", "policy.status_lint"),
        ("[automation]\nlanes = 0\n", "automation.lanes"),
        ('[automation]\nblackout = "12-19"\n', "automation.blackout"),
        (
            "[outcomes]\ncomplete_sampling_rate = 1.5\n",
            "outcomes.complete_sampling_rate",
        ),
        ("[admission]\nmax_batch_size = -1\n", "admission.max_batch_size"),
    ],
)
def test_out_of_range_value_is_refused_by_name(tmp_path, body, key):
    _, findings = CONFIG.load_config(write_config(tmp_path, "schema = 1\n\n" + body))
    assert keys(findings) == [key]


# --- the closed vocabularies are actually CHECKED -----------------------------
# A vocabulary the validator never applies is a vocabulary in name only: the
# typo it was closed to catch sails through, and the refusal that eventually
# lands names a pool or a work item instead of the misspelled word.
@pytest.mark.parametrize(
    "body,key,typo",
    [
        (
            '[[routes]]\nid = "R"\nfamily = "F"\nmodel = "m"\n'
            'capabilities = ["text", "reveiw"]\n',
            "routes[0].capabilities",
            "reveiw",
        ),
        (
            '[outcomes]\nrisk_safety_classes = ["spine", "protexted"]\n',
            "outcomes.risk_safety_classes",
            "protexted",
        ),
    ],
)
def test_a_typo_in_a_closed_array_vocabulary_is_refused_by_name(
    tmp_path, body, key, typo
):
    _, findings = CONFIG.load_config(write_config(tmp_path, "schema = 1\n\n" + body))
    assert keys(findings) == [key]
    assert typo in findings[0].reason, findings[0].reason


@pytest.mark.parametrize(
    "body",
    [
        '[[routes]]\nid = "R"\nfamily = "F"\nmodel = "m"\ncapabilities = ["Review"]\n',
        '[outcomes]\nrisk_safety_classes = ["Spine", " gate "]\n',
    ],
)
def test_a_case_variant_of_a_declared_token_still_loads(tmp_path, body):
    # The consumers fold and strip before comparing (agent_route's capability
    # filter, intake's safety-class check), so the validator must too — a token
    # must not be legal to one and a typo to the other.
    _, findings = CONFIG.load_config(write_config(tmp_path, "schema = 1\n\n" + body))
    assert findings == [], CONFIG.refusal_lines(findings)


def test_the_safety_class_vocabulary_is_the_schedulers():
    # config.SAFETY_CLASSES is an F5 copy, not an import (the git hooks load this
    # module and must not pay for the dispatcher). Pinned equal here so the copy
    # cannot drift into accepting a class the classifier refuses.
    schedule = load_script("schedule")
    assert CONFIG.SAFETY_CLASSES == schedule.SAFETY_CLASSES


def test_the_capability_vocabulary_covers_every_declared_job():
    # One token per role, or a job could never be served by any legal route.
    route = load_script("agent_route")
    assert set(route.JOB_CAPABILITY.values()) <= set(CONFIG.CAPABILITIES)


# --- the route row rungs are the registry's, restated as schema ---------------
def test_the_route_patterns_are_the_agents_csv_readers_rules():
    # `docs/agents.csv` and `docs/config.toml` are the same routing facts before
    # and after the migration, so the canonical document must face the same bar.
    route = load_script("agent_route")
    assert route.ID_RE.pattern.strip("^$") == CONFIG.ROUTE_ID_PATTERN
    assert route.MODEL_SLUG_RE.pattern.strip("^$") == CONFIG.MODEL_SLUG_PATTERN


@pytest.mark.parametrize(
    "route_body,key",
    [
        ('id = "BAD ID!"\nfamily = "F"\nmodel = "m"\n', "routes[0].id"),
        ('id = "lower"\nfamily = "F"\nmodel = "m"\n', "routes[0].id"),
        # The H-4 shape: a quote re-arms `&` as a live operator when a Windows
        # .cmd shim re-parses the argv this slug is substituted into.
        (
            'id = "EVIL"\nfamily = "F"\nmodel = \'opus" & calc.exe &\'\n',
            "routes[0].model",
        ),
        ('id = "R"\nfamily = "F"\nmodel = "opus prompt"\n', "routes[0].model"),
    ],
)
def test_a_route_id_or_model_the_registry_would_refuse_is_refused_here(
    tmp_path, route_body, key
):
    _, findings = CONFIG.load_config(
        write_config(tmp_path, "schema = 1\n\n[[routes]]\n" + route_body)
    )
    assert keys(findings) == [key]


def test_a_legal_router_style_model_slug_still_loads(tmp_path):
    # `org/model` and `us.anthropic....` are legal slugs; the pattern must not
    # narrow the registry's own vocabulary while closing the injection hole.
    _, findings = CONFIG.load_config(
        write_config(
            tmp_path,
            'schema = 1\n\n[[routes]]\nid = "OPENCODE-KIMI"\nfamily = "OPENCODE"\n'
            'model = "opencode-go/kimi-k3"\n',
        )
    )
    assert findings == [], CONFIG.refusal_lines(findings)


def test_duplicate_route_ids_are_refused_rather_than_shadowed(tmp_path):
    # Every consumer keys routes by id, so a second declaration makes the first
    # unreachable — and the no-capable-route refusal then quotes capabilities the
    # adopter can see their file does not give that route.
    cfg, findings = CONFIG.load_config(
        write_config(
            tmp_path,
            'schema = 1\n\n[[routes]]\nid = "A"\nfamily = "F1"\nmodel = "m1"\n'
            'capabilities = ["review"]\n\n'
            '[[routes]]\nid = "A"\nfamily = "F2"\nmodel = "m2"\n'
            'capabilities = ["text"]\n',
        )
    )
    assert keys(findings) == ["routes[1].id"]
    assert "duplicates routes[0].id" in findings[0].reason
    assert "'A'" in findings[0].reason


def test_distinct_route_ids_are_not_reported_as_duplicates(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(
            tmp_path,
            'schema = 1\n\n[[routes]]\nid = "A"\nfamily = "F"\nmodel = "m"\n\n'
            '[[routes]]\nid = "B"\nfamily = "F"\nmodel = "m"\n',
        )
    )
    assert findings == [], CONFIG.refusal_lines(findings)


# --- the blackout window is validated as a TIME, not as a shape ---------------
@pytest.mark.parametrize("window", ["25:00-99:99", "24:00-01:00", "12:60-13:00"])
def test_an_out_of_range_blackout_window_is_refused(tmp_path, window):
    # The shape-only pattern accepted these, and the only reader
    # (`agent_common.parse_blackout`) then returns None — which DISABLES the
    # window. A typo that reads as "no blackout" is the exact silent-off defect
    # this module exists to end.
    _, findings = CONFIG.load_config(
        write_config(
            tmp_path, 'schema = 1\n\n[automation]\nblackout = "{}"\n'.format(window)
        )
    )
    assert keys(findings) == ["automation.blackout"]


@pytest.mark.parametrize("window", ["", "00:00-23:59", "22:30-06:00", "12:00-19:00"])
def test_every_accepted_blackout_window_parses_for_its_only_reader(tmp_path, window):
    # The agreement that makes the refusal above honest: what the schema accepts,
    # the live parser must understand.
    common = load_script("agent_common")
    _, findings = CONFIG.load_config(
        write_config(
            tmp_path, 'schema = 1\n\n[automation]\nblackout = "{}"\n'.format(window)
        )
    )
    assert findings == [], CONFIG.refusal_lines(findings)
    if window:
        assert common.parse_blackout(window) is not None, window


def test_a_rate_may_be_written_as_an_integer(tmp_path):
    # TOML `0` and `0.0` are different types but the same honest answer.
    cfg, findings = CONFIG.load_config(
        write_config(tmp_path, "schema = 1\n\n[outcomes]\ncomplete_sampling_rate = 1\n")
    )
    assert findings == []
    assert cfg.outcomes.complete_sampling_rate == 1.0
    assert isinstance(cfg.outcomes.complete_sampling_rate, float)


# --- TC-150: bad-schema-version ----------------------------------------------
def test_unsupported_schema_version_is_refused(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(tmp_path, 'schema = 99\n\n[policy]\npush = "agent"\n')
    )
    assert keys(findings) == ["schema"]
    assert "99" in findings[0].reason


def test_a_document_with_no_schema_declaration_is_refused(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(tmp_path, '[policy]\npush = "agent"\n')
    )
    assert keys(findings) == ["schema"]


def test_malformed_toml_is_refused_naming_the_file(tmp_path):
    _, findings = CONFIG.load_config(write_config(tmp_path, "schema = 1\n[policy\n"))
    assert keys(findings) == [CONFIG.CONFIG_REL]


def test_a_byte_order_mark_does_not_rename_the_first_key(tmp_path):
    root = write_config(tmp_path, WELL_FORMED)
    path = root / "docs" / "config.toml"
    path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())
    cfg, findings = CONFIG.load_config(root)
    assert findings == []
    assert cfg.schema == 1


def test_refusal_lines_carry_the_kit_refusal_shape(tmp_path):
    _, findings = CONFIG.load_config(
        write_config(tmp_path, "schema = 1\n\n[policy]\nnope = 1\n")
    )
    (line,) = CONFIG.refusal_lines(findings)
    assert line.startswith("config: REFUSED - policy.nope (")
    assert line.endswith(")")


# --- TC-151: mixed sources ----------------------------------------------------
def legacy(root, rel, text):
    path = root.joinpath(*rel.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_both_live_refuses_and_lists_the_conflicting_pair(tmp_path):
    write_config(tmp_path, 'schema = 1\n\n[policy]\npush = "agent"\n')
    legacy(tmp_path, "docs/push-policy", "# header\nhuman\n")
    findings = CONFIG.mixed_source_findings(tmp_path)
    assert keys(findings) == ["policy.push"]
    assert "docs/push-policy" in findings[0].reason


def test_both_live_lists_every_conflicting_pair_not_just_one(tmp_path):
    write_config(
        tmp_path,
        'schema = 1\n\n[policy]\npush = "agent"\nreview_rounds = 2\n'
        "privacy_check = true\n",
    )
    for rel, text in (
        ("docs/push-policy", "human\n"),
        ("docs/review-policy", "1\n"),
        ("docs/privacy-check", "false\n"),
    ):
        legacy(tmp_path, rel, text)
    assert set(keys(CONFIG.mixed_source_findings(tmp_path))) == {
        "policy.push",
        "policy.review_rounds",
        "policy.privacy_check",
    }


def test_canonical_only_passes(tmp_path):
    write_config(tmp_path, 'schema = 1\n\n[policy]\npush = "agent"\n')
    assert CONFIG.mixed_source_findings(tmp_path) == []


def test_legacy_only_passes(tmp_path):
    (tmp_path / "docs").mkdir()
    legacy(tmp_path, "docs/push-policy", "human\n")
    assert CONFIG.mixed_source_findings(tmp_path) == []


def test_a_key_left_at_its_default_never_conflicts(tmp_path):
    # An unset key is not a second source of truth, so a surviving legacy file
    # beside it is a single source, not a divergence.
    write_config(tmp_path, "schema = 1\n\n[policy]\nreview_rounds = 2\n")
    legacy(tmp_path, "docs/push-policy", "human\n")
    assert CONFIG.mixed_source_findings(tmp_path) == []


def test_routes_conflict_with_the_surviving_agents_registry(tmp_path):
    write_config(
        tmp_path,
        'schema = 1\n\n[[routes]]\nid = "R"\nfamily = "F"\nmodel = "m"\n',
    )
    legacy(tmp_path, "docs/agents.csv", "Id,Family,Model,Version,Tier\n")
    assert keys(CONFIG.mixed_source_findings(tmp_path)) == ["routes"]


def test_stack_ini_conflicts_only_when_the_section_declares_the_dial(tmp_path):
    # docs/stack.ini SURVIVES the migration, so its presence proves nothing —
    # only the [agent-loop] section actually declaring `lanes` is a live pair.
    write_config(tmp_path, "schema = 1\n\n[automation]\nlanes = 2\n")
    legacy(
        tmp_path, "docs/stack.ini", "[paths]\nsrc = src\n\n[agent-loop]\nmodel = opus\n"
    )
    assert CONFIG.mixed_source_findings(tmp_path) == []
    legacy(
        tmp_path,
        "docs/stack.ini",
        "[paths]\nsrc = src\n\n[agent-loop]\nmodel = opus\nlanes = 4\n",
    )
    assert keys(CONFIG.mixed_source_findings(tmp_path)) == ["automation.lanes"]


def test_a_malformed_config_sets_no_keys_so_nothing_conflicts(tmp_path):
    write_config(tmp_path, "schema = 1\n[policy\n")
    legacy(tmp_path, "docs/push-policy", "human\n")
    assert CONFIG.mixed_source_findings(tmp_path) == []


def test_the_harness_paths_have_no_canonical_mirror_at_all(tmp_path):
    # The P13 cutover DELETED `[harness] src`/`tests` rather than landing the
    # parity test the contracts doc said it owed one of. Nothing ever read them,
    # the mirror of docs/stack.ini [paths] was never proved, and this repo's own
    # instance had already diverged. So there is no pair to watch and no section
    # to declare — docs/stack.ini is simply the one home of the toolchain.
    assert "harness.src" not in CONFIG.LEGACY_SOURCES
    assert "harness.tests" not in CONFIG.LEGACY_SOURCES
    assert "harness" not in CONFIG.SECTIONS
    assert not any(k.path.startswith("harness.") for k in CONFIG.SCHEMA)


# --- the schema table is the one table ---------------------------------------
def test_defaults_are_the_projection_of_the_schema():
    assert CONFIG.DEFAULTS == {k.path: k.default for k in CONFIG.SCHEMA}
    assert len(CONFIG.DEFAULTS) == len(CONFIG.SCHEMA), "duplicate dotted path"


def test_every_declared_default_survives_its_own_validator():
    # A default that its own schema row would refuse is a trap: the absent-file
    # path would hand a caller a value the file path rejects.
    cfg, findings = CONFIG.validate({"schema": CONFIG.SCHEMA_VERSION})
    assert findings == []
    for spec in CONFIG.SCHEMA:
        section, leaf = spec.path.split(".", 1)
        assert getattr(getattr(cfg, section), leaf) == CONFIG.DEFAULTS[spec.path]


def test_every_schema_row_documents_itself():
    undocumented = [k.path for k in CONFIG.SCHEMA if not k.doc.strip()]
    assert not undocumented, "a dial with no doc string is invisible to an adopter"


def test_every_legacy_source_names_a_declared_key():
    declared = set(CONFIG.DEFAULTS) | {"routes"}
    assert set(CONFIG.LEGACY_SOURCES) <= declared


# --- the shipped blank form is GENERATED from the schema ----------------------
def test_shipped_template_is_the_rendered_schema():
    shipped = (KIT / "config.toml.template").read_text(encoding="utf-8")
    assert shipped == MIGRATE.render_template(), (
        "regenerate: python scripts/config_migrate.py --template"
    )


def test_shipped_template_has_lf_endings():
    assert b"\r\n" not in (KIT / "config.toml.template").read_bytes()


def test_shipped_template_declares_the_schema_and_sets_nothing_else():
    # Every dial is commented out on purpose: bootstrap still scaffolds the
    # retired one-word files, so a template that SET keys would make every fresh
    # repo mixed-source on day one.
    document = tomllib.loads((KIT / "config.toml.template").read_text(encoding="utf-8"))
    assert document.pop("schema") == CONFIG.SCHEMA_VERSION
    assert all(v == {} for v in document.values()), document


def test_shipped_template_shows_every_dial_with_its_default():
    text = (KIT / "config.toml.template").read_text(encoding="utf-8")
    for spec in CONFIG.SCHEMA:
        leaf = spec.path.split(".", 1)[1]
        assert "# {} = ".format(leaf) in text, spec.path


# --- agreement with the normative contract ------------------------------------
def _contract_document():
    """The first fenced ```toml block of the contracts doc's §1 — the normative
    sample document this schema must be able to hold."""
    text = (ROOT / "docs" / "mechanized-loop-contracts.md").read_text(encoding="utf-8")
    body = text.split("```toml", 1)[1].split("```", 1)[0]
    return tomllib.loads(body)


# Sections the contract SAMPLE still shows that the schema no longer declares.
#
# EMPTY, and the emptying is the point. It held exactly one entry — `harness` —
# by the contracts doc's own ruling: §1 said P13 owed either a parity test for
# `[harness]` or its deletion, and had to say WHICH. It deleted; the cutover
# slice does not edit the two mechanized-loop documents, so the doc amendment was
# owed and this tuple was the mechanical record of that debt rather than a quiet
# tolerance. The amendment landed, the guard below said so in as many words, and
# the tuple is now empty.
#
# Leave it here. A future retirement gets one line and a reason, and the guard
# tells whoever lands the doc half that they may remove it — which is the only
# way a "we'll fix the doc later" stays visible instead of becoming folklore.
SAMPLE_SECTIONS_RETIRED_SINCE = ()


def test_every_key_of_the_contract_sample_is_declared():
    document = _contract_document()
    assert "schema" in document
    for name, value in document.items():
        if name == "schema" or name in SAMPLE_SECTIONS_RETIRED_SINCE:
            continue
        if name == "routes":
            declared = {f.path for f in CONFIG.ROUTE_FIELDS}
            for route in value:
                assert set(route) <= declared, set(route) - declared
            continue
        if name in ("jobs", "prompts"):
            fields = CONFIG.JOB_FIELDS if name == "jobs" else CONFIG.PROMPT_FIELDS
            declared = {f.path for f in fields}
            names = CONFIG.JOBS if name == "jobs" else CONFIG.PROMPTS
            for entry_name, entry in value.items():
                assert entry_name in names
                assert set(entry) <= declared, set(entry) - declared
            continue
        for leaf in value:
            assert "{}.{}".format(name, leaf) in CONFIG.DEFAULTS


def test_the_contract_sample_document_validates_clean():
    document = _contract_document()
    for retired in SAMPLE_SECTIONS_RETIRED_SINCE:
        assert document.pop(retired, None) is not None, (
            "the contracts sample no longer shows [{}] — the doc amendment "
            "landed, so drop it from SAMPLE_SECTIONS_RETIRED_SINCE".format(retired)
        )
    _, findings = CONFIG.validate(document)
    assert findings == [], CONFIG.refusal_lines(findings)


def test_the_declared_job_and_prompt_vocabularies_match_the_contract():
    # contracts §1: "Declared jobs: planner, critic, arbiter, implementer,
    # reviewer, adjudicator" plus the four adjudicator templates.
    assert set(CONFIG.JOBS) == {
        "planner",
        "critic",
        "arbiter",
        "implementer",
        "reviewer",
        "adjudicator",
    }
    # The prompt vocabulary is the jobs plus one PURPOSE-SPECIFIC brief per
    # extra reviewed template the kit ships: the four adjudicator briefs, and
    # `dual-plan-critic` for the second of the two critic templates. Contracts §1
    # still says "the six jobs plus the four adjudicator templates" and owes this
    # name — it was written before the second critic template was counted, and
    # with ten names one of the two shipped critic prompts was undeclared,
    # unrenderable and invisible to `prompt_render check`.
    assert set(CONFIG.PROMPTS) == set(CONFIG.JOBS) | {
        "dual-plan-critic",
        "adjudicate-amendment",
        "adjudicate-disposition",
        "adjudicate-conflict",
        "adjudicate-red-test",
    }


def test_every_shipped_prompt_template_is_declared_by_this_repos_config():
    """No orphan templates: a reviewed prompt this config never names cannot be
    rendered by any code path — `declarations()` iterates the CLOSED vocabulary,
    and `render` takes a job name, never a file. `critique.md` was exactly that:
    shipped to every adopter by bootstrap, and unreachable."""
    cfg, findings = CONFIG.load_config(ROOT)
    assert findings == [], CONFIG.refusal_lines(findings)
    declared = {entry.template for entry in cfg.prompts.values()}
    shipped = {
        "project-trajectory/prompts/" + p.name
        for p in sorted((KIT / "prompts").glob("*.md"))
        if p.name != "README.md"
    }
    assert shipped - declared == set(), "undeclared prompt template(s)"


def test_this_repos_own_config_validates_clean():
    cfg, findings = CONFIG.load_config(ROOT)
    assert findings == [], CONFIG.refusal_lines(findings)
    assert cfg.routing.enabled is True
    assert len(cfg.routes) >= 1
