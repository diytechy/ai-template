"""The HATS ROSTER (SN-036, ruled at OI-19 2026-08-13): the reader, the
applicability grammar, and the INJECTION into the decomposition brief.

Four things are checked, and the fourth is the one that makes the layer real:

1. READING — a well-formed roster parses in declared order; an ABSENT roster is
   silently empty (opt-out is a supported adopter act); a roster that EXISTS and
   is broken raises rather than reporting itself as empty.
2. THE GRAMMAR — `applies_when` is closed and evaluable, and its two honest
   edges hold: a mixed `or`/`and` expression is refused (no precedence to
   guess), and A FIELD THE CONTEXT DID NOT DECLARE SATISFIES NO CLAUSE, `!=`
   included.
3. SELECTION — the shipped six select the way their conditions say.
4. INJECTION — a brief composed from the REAL shipped planner template and the
   REAL shipped roster carries every applicable hat's question, and carries no
   inapplicable hat's question. That last clause is what stops the layer
   degrading into "the file exists": a roster nobody filtered would pass every
   test above.

The vacuous-guard rule applies here as everywhere: the malformed cases drive the
reader over trees built to break it, so the green above is demonstrated able to
fail before it is trusted to pass.
"""

from __future__ import annotations

import pytest

from conftest import ROOT, load_script

hats = load_script("hats")
plan_briefs = load_script("plan_briefs")

# The kit's own roster + the shipped template — the two files this WI authored.
LIVE_ROSTER = ROOT / "docs" / "requirements" / "hats.toml"
KIT_ROSTER = ROOT / "project-trajectory" / "registries" / "hats.template.toml"

WELL_FORMED = """
[hat.SECURITY]
applies_when = "always"
asks = "What secret does this touch?"
listens_for = "A secret spent with no requirement naming the authority."

[hat.CROSS-PLATFORM]
applies_when = 'tags contains "scripts"'
asks = "Which of Windows, macOS and Linux breaks this?"
listens_for = "A rule true only on the author's platform."
"""


def _write(tmp_path, text):
    (tmp_path / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "requirements" / "hats.toml").write_text(
        text, encoding="utf-8"
    )
    return tmp_path


# --- 1. reading ---------------------------------------------------------------
def test_a_well_formed_roster_parses_in_declared_order(tmp_path):
    roster = hats.load(_write(tmp_path, WELL_FORMED))
    assert [h["name"] for h in roster] == ["SECURITY", "CROSS-PLATFORM"]
    assert roster[0]["asks"].startswith("What secret")
    assert roster[0]["listens_for"].startswith("A secret spent")


def test_an_absent_roster_is_silently_empty(tmp_path):
    """Opt-out is deleting the file — never an error. An adopter who wants no
    hats must not have to keep an empty file around to say so."""
    assert hats.load(tmp_path) == []
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    assert hats.load(tmp_path) == []


@pytest.mark.parametrize(
    "text,expect",
    [
        ("[hat.A\nasks = 'x'\n", "does not parse as TOML"),
        ("[perspective.A]\napplies_when = 'always'\n", "unknown top-level table"),
        (
            '[hat.A]\napplies_when = "always"\nasks = "q"\n',
            "has no `listens_for`",
        ),
        (
            '[hat.A]\napplies_when = "always"\nlistens_for = "f"\n',
            "has no `asks`",
        ),
        (
            '[hat.A]\nasks = "q"\nlistens_for = "f"\n',
            "has no `applies_when`",
        ),
        (
            '[hat.A]\napplies_when = "always"\nasks = "q"\nlistens_for = "f"\n'
            'notes = "extra"\n',
            r"unknown key\(s\) notes",
        ),
        (
            '[hat.A]\napplies_when = "always"\nasks = "q"\nlistens_for = ""\n',
            "has no `listens_for`",
        ),
        (
            '[hat.A]\napplies_when = "colour == \'blue\'"\nasks = "q"\n'
            'listens_for = "f"\n',
            "unknown field",
        ),
        (
            '[hat.A]\napplies_when = "it feels relevant"\nasks = "q"\n'
            'listens_for = "f"\n',
            "not an evaluable clause",
        ),
    ],
)
def test_a_malformed_roster_refuses_loudly(tmp_path, text, expect):
    """Every arm names WHAT is wrong. A roster reported as empty because it was
    broken is a decomposition that silently faced no perspective at all."""
    with pytest.raises(hats.HatsError, match=expect):
        hats.load(_write(tmp_path, text))


def test_a_hat_naming_no_failure_class_is_refused_as_ceremony(tmp_path):
    """The `listens_for` requirement is the guardrail OI-19 asked for, applied
    to the roster itself: if you cannot say what goes wrong when nobody wears
    the hat, the row does not load."""
    text = '[hat.VIBES]\napplies_when = "always"\nasks = "Is it good?"\n'
    with pytest.raises(hats.HatsError, match="a hat naming no failure is ceremony"):
        hats.load(_write(tmp_path, text))


# --- 2. the applies_when grammar ----------------------------------------------
def test_mixed_or_and_is_refused_rather_than_given_a_precedence():
    with pytest.raises(hats.HatsError, match="mixes `or` and `and`"):
        hats.parse_condition('scope == "a" or kind == "b" and scope == "c"')


@pytest.mark.parametrize(
    "expr,match",
    [
        ('tags == "scripts"', "takes `contains` only"),
        ('scope contains "template"', "takes == / != only"),
    ],
)
def test_an_operator_a_field_does_not_admit_is_refused(expr, match):
    with pytest.raises(hats.HatsError, match=match):
        hats.parse_condition(expr)


def test_always_holds_for_the_empty_context():
    assert hats.evaluate(hats.parse_condition("always"), {}) is True


@pytest.mark.parametrize("expr", ['scope == "template"', 'scope != "template"'])
def test_an_undeclared_field_satisfies_no_clause(expr):
    """The fail-CLOSED rule, and the `!=` half is the load-bearing one: reading
    an absent fact as "not equal, therefore true" would fire a scope-keyed hat
    on every decomposition in a project that never records scope."""
    assert hats.evaluate(hats.parse_condition(expr), {}) is False
    assert hats.evaluate(hats.parse_condition(expr), {"kind": "core"}) is False


def test_and_needs_every_clause_while_or_needs_one():
    ctx = {"scope": "template", "kind": "core"}
    assert hats.evaluate(
        hats.parse_condition('scope == "template" and kind == "core"'), ctx
    )
    assert not hats.evaluate(
        hats.parse_condition('scope == "template" and kind == "draft"'), ctx
    )
    assert hats.evaluate(hats.parse_condition('scope == "nope" or kind == "core"'), ctx)


# --- 3. selection -------------------------------------------------------------
def test_selection_filters_on_the_declared_condition(tmp_path):
    roster = hats.load(_write(tmp_path, WELL_FORMED))
    names = lambda ctx: [h["name"] for h in hats.applicable(roster, ctx)]
    assert names({}) == ["SECURITY"]
    assert names({"tags": ["scripts"]}) == ["SECURITY", "CROSS-PLATFORM"]
    assert names({"tags": ["docs"]}) == ["SECURITY"]


def test_the_shipped_roster_selects_the_three_always_on_hats_at_minimum():
    """The kit's own roster, read from disk. The three `always` hats are the
    floor every decomposition faces; the other three are conditional, which is
    the whole point of `applies_when`."""
    roster = hats.load(ROOT)
    assert [h["name"] for h in roster] == [
        "SECURITY",
        "FIRST-RUN-ADOPTER",
        "UNATTENDED-OPS",
        "CROSS-PLATFORM",
        "MAINTAINER",
        "TEST-ENGINEER",
    ]
    minimum = [h["name"] for h in hats.applicable(roster, {})]
    assert minimum == ["SECURITY", "MAINTAINER", "TEST-ENGINEER"]
    unattended = [h["name"] for h in hats.applicable(roster, {"tags": ["unattended"]})]
    assert "UNATTENDED-OPS" in unattended
    assert "CROSS-PLATFORM" not in unattended


def test_the_work_item_context_is_the_two_typed_classification_cells():
    ctx = hats.context_from_work_item(
        {"Workstream": "unattended", "SafetyClass": "spine", "Title": "ignored"}
    )
    assert ctx == {"tags": ["unattended", "spine"]}
    # A work item declares neither scope nor kind, so neither is invented.
    assert "scope" not in ctx and "kind" not in ctx


def test_the_need_context_reads_only_typed_cells():
    assert hats.context_from_need({"kind": "core", "scope": "template"}) == {
        "kind": "core",
        "scope": "template",
    }
    # A need row without a scope FIELD (today's registry) declares no scope —
    # it is not inferred from prose (SN-039 is what makes it a field).
    assert hats.context_from_need({"kind": "draft"}) == {"kind": "draft"}


# --- 4. the injection ---------------------------------------------------------
def _planner_template():
    return plan_briefs.strip_dispatcher_block(
        plan_briefs.load_template(plan_briefs.HAT_PLANNER)
    )


def _compose(root, context):
    template = _planner_template()
    slots = dict(
        plan_briefs.hat_surface(root, context),
        GOAL_BRIEF="C1: do the thing",
        SR_SURFACE="- SR-001 - a requirement",
        IF_REGISTRY="| IF-ID |\n|---|",
        OWN_PLAN="(none)",
        CRITIQUE="(none)",
    )
    return plan_briefs.assemble(plan_briefs.HAT_PLANNER, slots, template)


def test_the_shipped_planner_template_declares_the_slot():
    assert plan_briefs.declares_slot(
        _planner_template(), plan_briefs.HAT_QUESTIONS_SLOT
    )


def test_a_composed_brief_carries_every_applicable_hats_question_and_no_other():
    """THE POINT OF THE WHOLE LAYER. Composed from the real shipped template and
    the kit's real roster: a decomposition session cannot avoid a perspective
    that applies, and is not taxed with one that does not."""
    roster = hats.load(ROOT)
    context = {"tags": ["unattended"]}
    applicable = hats.applicable(roster, context)
    brief = _compose(ROOT, context)

    for question in hats.questions(applicable):
        assert question in brief, question
    for hat in roster:
        if hat in applicable:
            continue
        assert hat["asks"] not in brief, hat["name"]
    # CROSS-PLATFORM is the inapplicable one this context is chosen to exclude —
    # asserted by NAME so the test cannot pass vacuously if the roster is edited
    # to make every hat always-on.
    assert "CROSS-PLATFORM" not in [h["name"] for h in applicable]
    assert "{{" not in brief  # a strict fill left no hole


def test_an_absent_roster_composes_a_brief_with_a_stated_no_hats_line(tmp_path):
    """Opt-out reaches the brief as a STATEMENT, not as an empty section: the
    reader can tell "nothing was declared" from "the slot did not get filled"."""
    brief = _compose(tmp_path, {})
    assert hats.NO_HATS in brief
    assert "{{" not in brief


def test_a_malformed_roster_refuses_at_composition(tmp_path):
    _write(tmp_path, "[hat.A]\nasks = 'q'\n")
    with pytest.raises(plan_briefs.HatsError):
        plan_briefs.hat_surface(tmp_path, {})


def test_an_override_template_without_the_slot_is_not_handed_it():
    """The backwards-compatibility guard. `assemble` rejects a slot key the
    template does not declare, so an operator override authored before this
    slot existed would stop composing entirely if the runner filled it
    unconditionally."""
    older = "Plan {{GOAL_BRIEF}} against {{SR_SURFACE}} and {{IF_REGISTRY}}."
    assert not plan_briefs.declares_slot(older, plan_briefs.HAT_QUESTIONS_SLOT)
    with pytest.raises(ValueError, match=plan_briefs.HAT_QUESTIONS_SLOT):
        plan_briefs.assemble(
            plan_briefs.HAT_PLANNER,
            {
                "GOAL_BRIEF": "g",
                "SR_SURFACE": "s",
                "IF_REGISTRY": "i",
                plan_briefs.HAT_QUESTIONS_SLOT: "h",
            },
            older,
        )


# --- the dogfood rule: structure must not drift, values may -------------------
def test_the_kit_template_and_the_live_roster_share_a_STRUCTURE():
    """CLAUDE.md's dogfood rule applied to the roster. The two files are allowed
    to diverge in VALUES — the live one is owner text marked for edit, and an
    adopter is *expected* to rewrite theirs — so this pins the SHAPE: both parse
    under the same reader, both declare the same three required keys per hat,
    and neither ships a hat whose condition the grammar cannot evaluate."""
    live = hats.load(ROOT)
    kit = hats.load(ROOT, rel=str(KIT_ROSTER.relative_to(ROOT)))
    assert live and kit
    for roster in (live, kit):
        for hat in roster:
            assert set(hat) == {
                "name",
                "applies_when",
                "asks",
                "listens_for",
                "condition",
            }
    # And the shipped form is not a blank one: a roster template with no hats
    # would be a form with nothing behind it (the reason it ships CONTENT).
    assert len(kit) >= 3
