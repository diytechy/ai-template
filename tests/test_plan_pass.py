"""The single plan's records and briefs, in process (WI-913).

The smoke tier's pin for the plan gate's script family: the pass record's
grammar (`kitlib.plan_pass`), the plan's typed `DELTA:` line, the planner's
brief (`review_brief.py plan`) rendered strictly in both modes over a
temporary spec, and the shipped template's delta question. The git-driven
arms of the gate and the filing step are in `test_plan_gate.py` and
`test_plan_filing.py`, in `tests/conftest.py`'s `SLOW_MODULES`.
"""

import re

import pytest
from conftest import KIT, load_script

rb = load_script("review_brief")
pr = load_script("prompts")
from kitlib import plan_pass as pp  # noqa: E402  (scripts/ put on the path above)

WI = "WI-950"
FIELDS = {
    "wi": WI,
    "plan": "sha256:" + "a" * 64,
    "done_when": "sha256:" + "b" * 16,
    "critique": "docs/plans/WI-950/critique-1.md",
    "critique_digest": "sha256:" + "c" * 64,
    "reviewed": "d" * 40,
    "delta": "none",
    "dispute": "",
    "dispute_digest": "",
}
SPEC = """+++
id = "WI-950"
title = "A row that plans first"
sr_refs = ["SR-001"]
planmode = "single"
+++

## Done-when

- The gate holds the build.
- The record releases it.
"""
# Review-churn plan item 12, entry point 2: the delta question in its own words.
DELTA_QUESTION = (
    "does the WI add a state, add a value to a domain, make an output depend "
    "on a new input, or cross a new boundary?"
)


def test_a_record_renders_and_reads_back_through_one_grammar():
    text = pp.render(FIELDS)
    data, why = pp.parse(text)
    assert why is None and data == FIELDS


@pytest.mark.parametrize(
    "change",
    [
        {"plan": "sha256:short"},
        {"done_when": "sha256:" + "b" * 64},
        {"reviewed": "abc"},
        {"delta": "beyond"},
        {"wi": "WI-x"},
        {"critique": "docs/plans/WI-951/critique-1.md"},
        {"critique": "docs/plans/WI-950/critique-3.md.bak"},
        {"dispute": "docs/reviews/x/001-ADJUDICATE-abc1234.md"},
    ],
)
def test_a_record_outside_its_grammar_is_malformed_and_never_written(change):
    data, why = pp.parse(pp.render(FIELDS).replace("\n", "\n", 1) + "")
    assert why is None and data
    fields = {**FIELDS, **change}
    body = "".join('{} = "{}"\n'.format(k, fields[k]) for k in pp.FIELDS)
    data, why = pp.parse(body)
    assert data is None and why
    with pytest.raises(ValueError):
        pp.render(fields)


def test_a_partial_or_extra_keyed_record_is_malformed():
    whole = pp.render(FIELDS)
    assert pp.parse(whole[: len(whole) // 2])[0] is None
    assert pp.parse(whole + 'extra = "x"\n')[0] is None
    assert pp.parse("not = toml = at all")[0] is None


@pytest.mark.parametrize(
    "text, value",
    [
        ("x\nDELTA: none\n", "none"),
        ("DELTA:   within  \n", "within"),
        ("DELTA: beyond\n", "beyond"),
        ("no line\n", None),
        ("DELTA: none\nDELTA: within\n", None),
        ("DELTA: sideways\n", None),
    ],
)
def test_the_delta_line_is_one_typed_line_from_a_closed_set(text, value):
    found, why = pp.delta(text)
    assert found == value
    assert (why is None) == (value is not None)


def test_a_critique_round_is_read_only_under_its_own_plan_home():
    assert pp.critique_round(WI, "docs/plans/WI-950/critique-2.md") == 2
    assert pp.critique_round(WI, "docs/plans/WI-951/critique-2.md") is None
    assert pp.critique_round(WI, "docs/plans/WI-950/plan.md") is None


def test_a_critique_round_past_the_cap_is_no_critique():
    # Fable REVIEW-B F2 (round 1): the grammar admitted critique-3..9.
    beyond = "docs/plans/WI-950/critique-{}.md".format(pp.MAX_CRITIQUES + 1)
    assert pp.critique_round(WI, beyond) is None
    _data, why = pp.parse(pp.render(FIELDS).replace(FIELDS["critique"], beyond))
    assert why and "not a filed critique" in why


@pytest.mark.parametrize("raw", ["false", "0", "[]", "{}", "true"])
def test_a_non_string_planmode_is_outside_the_set_and_named(raw):
    # Sol REVIEW-A F1 (round 1): a raw TOML false, 0, [] or {} read as absent.
    text = SPEC.replace('planmode = "single"', "planmode = " + raw)
    mode, why = pp.planmode(text, "spec.md")
    assert mode is None
    assert "not a string" in why and "outside the set" in why
    assert pp.planmode(SPEC.replace('planmode = "single"\n', ""), "s") == ("", None)


def _lane(tmp_path, plan=None, critique=None):
    spec = tmp_path / "docs" / "work" / "active" / "wi-950" / "WI-950-plan-first.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC, encoding="utf-8")
    home = tmp_path / "docs" / "plans" / WI
    if plan is not None:
        home.mkdir(parents=True, exist_ok=True)
        (home / "plan.md").write_text(plan, encoding="utf-8")
    if critique is not None:
        (home / "critique-1.md").write_text(critique, encoding="utf-8")
    return tmp_path


CRITIQUE = (
    "Reviewed: " + "d" * 40 + "\n\n"
    "- [MAJOR] docs/plans/WI-950/plan.md:3 -> P2 has no test -> add one -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)


def test_the_planner_brief_carries_the_clauses_the_contract_and_the_delta_question(
    tmp_path,
):
    root = _lane(tmp_path)
    text = rb.render_plan(root, WI, "scratch/WI-950-plan.md")
    assert "- D1: The gate holds the build." in text
    assert "- D2: The record releases it." in text
    assert "`scratch/WI-950-plan.md`" in text
    assert "Plan-WI" in text and "Excludes:" in text
    assert DELTA_QUESTION in " ".join(text.split())
    assert "DELTA: none" in text and "DELTA: beyond" in text
    assert "SR-001" in text
    assert "REVISION MODE" not in text


def test_the_revision_brief_asks_the_delta_question_again_and_labels_its_inputs(
    tmp_path,
):
    root = _lane(tmp_path, plan="| Plan-WI |\nDELTA: none\n", critique=CRITIQUE)
    text = rb.render_plan(root, WI, "scratch/WI-950-plan-r2.md", revise=True)
    flat = " ".join(text.split())
    assert DELTA_QUESTION in flat
    assert "REVISION MODE" in text and "claims under judgement" in flat
    assert "F1: [MAJOR] docs/plans/WI-950/plan.md:3 -> P2 has no test" in text
    assert "| Plan-WI |" in text


@pytest.mark.parametrize("missing", ["spec", "plan", "critique"])
def test_the_planner_brief_refuses_a_missing_input(tmp_path, missing):
    if missing == "spec":
        root = tmp_path
    elif missing == "plan":
        root = _lane(tmp_path)
    else:
        root = _lane(tmp_path, plan="| Plan-WI |\n")
    with pytest.raises(rb.BriefError):
        rb.render_plan(root, WI, "p.md", revise=missing != "spec")


def test_the_planner_brief_refuses_an_unfilled_slot(tmp_path, monkeypatch):
    root = _lane(tmp_path)
    real = pr.load
    monkeypatch.setattr(
        rb.prompts,
        "load",
        lambda key, *a: real(key, *a) + ("{unfilled}" if key == pr.PLAN_SINGLE else ""),
    )
    with pytest.raises(rb.prompts.PromptError):
        rb.render_plan(root, WI, "p.md")


def test_the_command_writes_nothing_when_the_brief_refuses(tmp_path):
    out = tmp_path / "out" / "brief.md"
    argv = ["plan", "--root", str(tmp_path), "--wi", WI]
    assert rb.main(argv + ["--scratch", str(tmp_path), "--out", str(out)]) == 2
    assert not out.exists()


def test_the_shipped_planner_template_names_no_skill_and_no_row_of_this_repo():
    text = pr.load(pr.PLAN_SINGLE)
    raw = (KIT / "prompts" / "plan-single.template.md").read_text(encoding="utf-8")
    assert "skill" not in raw.lower()
    assert DELTA_QUESTION in " ".join(text.split())
    assert not re.search(r"\b(?:WI|SR|LLR|TC|IF|OI)-\d+\b", raw)


def test_the_planner_template_is_in_the_generated_catalogue():
    catalog = (KIT / "prompts" / "CATALOG.md").read_text(encoding="utf-8")
    assert "`PLAN-SINGLE`" in catalog and "plan-single.template.md" in catalog
