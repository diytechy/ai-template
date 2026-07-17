"""plan_briefs.py — the redacted dual-plan brief assembler (WI-195).

The P2 done-condition: an assembled planner/critic/arbiter brief carries only
allowlisted material (the SR surface + IF registry excerpt from the two
registries, plus the caller-passed goal/coverage/plan/rubric strings) and NEVER
status.md / log.md content — redaction BY CONSTRUCTION. Also covers the strict
slot-fill errors, dispatcher-block stripping, the prompt-map override winning
over the kit template, and hat-key vocabulary stability.
"""

import csv

import pytest
from conftest import SCRIPTS, load_script, run_py

pb = load_script("plan_briefs")

# A string planted in status.md/log.md — the leak the redaction boundary must
# never let through into any assembled brief.
SENTINEL = "TOPSECRET-SELF-ASSESSMENT-LEAK-42"

SR_TITLE = "Redacted brief assembler"
SR_REQ = "The system shall assemble briefs from an allowlist only."
IF_CONTRACT = "plan_briefs Consumes system-requirements.csv and interfaces.csv"


def _write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def _fixture_repo(root):
    """A repo whose status.md/log.md hold the SENTINEL and whose registries hold
    known SR-061 / IF-059 rows (plus inert `-000` example rows that must be
    dropped from the surface)."""
    docs = root / "docs"
    req = docs / "requirements"
    req.mkdir(parents=True)
    (docs / "status.md").write_text(
        "# status\ncurrent focus: " + SENTINEL + "\n", encoding="utf-8"
    )
    (docs / "log.md").write_text(
        "## session\nself-assessment: " + SENTINEL + "\n", encoding="utf-8"
    )
    _write_csv(
        req / "system-requirements.csv",
        [
            "SR-ID",
            "Title",
            "SN-Refs",
            "Requirement",
            "Rationale",
            "AcceptanceCriteria",
            "Permutations",
            "Priority",
            "Verification",
            "Status",
            "Phase",
            "Area",
        ],
        [
            [
                "SR-061",
                SR_TITLE,
                "SN-001",
                SR_REQ,
                "rationale",
                "ac",
                "",
                "M",
                "Test",
                "Verified",
                "4",
                "Dual-plan",
            ],
            [
                "SR-000",
                "example placeholder",
                "SN-000",
                "ignored stub",
                "",
                "",
                "",
                "M",
                "Test",
                "Proposed",
                "",
                "",
            ],
        ],
    )
    _write_csv(
        req / "interfaces.csv",
        [
            "IF-ID",
            "Direction",
            "ThisProject",
            "Counterpart",
            "Contract",
            "SR-Refs",
            "Version",
            "Stability",
            "Status",
            "Component",
            "Notes",
        ],
        [
            [
                "IF-059",
                "Consumes",
                "scripts/plan_briefs",
                "docs/requirements/interfaces.csv",
                IF_CONTRACT,
                "SR-061",
                "v1",
                "Experimental",
                "Proposed",
                "CMP-004",
                "note",
            ],
            [
                "IF-000",
                "Provides",
                "scripts/example",
                "scripts/other",
                "example stub",
                "SR-000",
                "v1",
                "Experimental",
                "Proposed",
                "",
                "",
            ],
        ],
    )
    return root


# --- the goal/coverage/plan/rubric strings a real caller passes in (all sourced
# from allowlisted material; none carry the sentinel) --------------------------
GOAL = "C1: assemble redacted briefs; the surface must expose SR-061 and IF-059."
RUBRIC = "G1: solvability. G2: completeness."
COVERAGE = "coverage: SR-061 covered by P2; IF-059 resolves; neither: (none)."
PLAN_A = "| Plan-WI | Title |\n|---|---|\n| P2 | brief assembler (SR-061) |"
PLAN_B = "| Plan-WI | Title |\n|---|---|\n| P2 | assembler covering SR-061 |"


def _slots_for(hat, surface):
    """The exact slot set each stripped kit template needs (strict fill: an
    unknown or missing key would raise)."""
    if hat == pb.HAT_PLANNER:
        return {
            "GOAL_BRIEF": GOAL,
            "SR_SURFACE": surface["SR_SURFACE"],
            "IF_REGISTRY": surface["IF_REGISTRY"],
            "OWN_PLAN": "",
            "CRITIQUE": "",
        }
    if hat == pb.HAT_CRITIC:
        return {
            "GOAL_BRIEF": GOAL,
            "SR_SURFACE": surface["SR_SURFACE"],
            "IF_REGISTRY": surface["IF_REGISTRY"],
            "RUBRIC": RUBRIC,
            "COVERAGE_REPORT": COVERAGE,
            "PLAN": PLAN_A,
        }
    return {
        "OWNER_PROMPT": GOAL,
        "GOAL_BRIEF": GOAL,
        "RUBRIC": RUBRIC,
        "COVERAGE_REPORT": COVERAGE,
        "PLAN_A": PLAN_A,
        "PLAN_B": PLAN_B,
    }


# --- build_surface: the allowlist boundary ------------------------------------
def test_build_surface_reads_only_the_two_registries(tmp_path):
    root = _fixture_repo(tmp_path)
    surface = pb.build_surface(root)
    assert set(surface) == {"SR_SURFACE", "IF_REGISTRY"}
    # Registry material is present...
    assert "SR-061" in surface["SR_SURFACE"]
    assert SR_TITLE in surface["SR_SURFACE"]
    assert SR_REQ in surface["SR_SURFACE"]
    assert "IF-059" in surface["IF_REGISTRY"]
    assert IF_CONTRACT in surface["IF_REGISTRY"]
    # ...the inert -000 example rows are dropped...
    assert "SR-000" not in surface["SR_SURFACE"]
    assert "IF-000" not in surface["IF_REGISTRY"]
    # ...and status.md / log.md content is unreachable by construction.
    assert SENTINEL not in surface["SR_SURFACE"]
    assert SENTINEL not in surface["IF_REGISTRY"]


def test_build_surface_missing_registries_are_empty_not_a_crash(tmp_path):
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    surface = pb.build_surface(tmp_path)
    assert surface["SR_SURFACE"] == ""
    # The IF excerpt keeps its header row even when there are no data rows.
    assert "IF-ID" in surface["IF_REGISTRY"]


# --- the P2 done-condition: every brief carries registry material, no sentinel -
@pytest.mark.parametrize("hat", [pb.HAT_PLANNER, pb.HAT_CRITIC, pb.HAT_ARBITER])
def test_assembled_brief_has_registry_material_never_sentinel(tmp_path, hat):
    root = _fixture_repo(tmp_path)
    surface = pb.build_surface(root)
    template = pb.strip_dispatcher_block(pb.load_template(hat))
    brief = pb.assemble(hat, _slots_for(hat, surface), template)

    # Registry material reached the brief (the SR/IF surface for the planner and
    # critic; the SR-061-bearing goal brief + coverage for the arbiter).
    assert "SR-061" in brief
    # The self-assessment leak never did — the whole point of the module.
    assert SENTINEL not in brief
    # No placeholder survives a strict fill.
    assert "{{" not in brief


def test_planner_and_critic_embed_the_if_registry(tmp_path):
    root = _fixture_repo(tmp_path)
    surface = pb.build_surface(root)
    for hat in (pb.HAT_PLANNER, pb.HAT_CRITIC):
        template = pb.strip_dispatcher_block(pb.load_template(hat))
        brief = pb.assemble(hat, _slots_for(hat, surface), template)
        assert "IF-059" in brief
        assert SR_TITLE in brief


# --- strict slot fill ---------------------------------------------------------
def test_unfilled_placeholder_raises_and_names_it():
    template = "A {{ALPHA}} and a {{BETA}}."
    with pytest.raises(ValueError, match="BETA"):
        pb.assemble(pb.HAT_PLANNER, {"ALPHA": "x"}, template)


def test_unknown_slot_key_raises_and_names_it():
    template = "Only {{ALPHA}} here."
    with pytest.raises(ValueError, match="GHOST"):
        pb.assemble(pb.HAT_PLANNER, {"ALPHA": "x", "GHOST": "y"}, template)


def test_assemble_fills_every_placeholder():
    template = "{{ALPHA}}-{{BETA}}"
    assert pb.assemble(pb.HAT_CRITIC, {"ALPHA": "1", "BETA": "2"}, template) == "1-2"


def test_slot_value_containing_brace_pair_is_passed_through():
    # A slot value that itself looks like a placeholder is content, not a hole.
    out = pb.assemble(pb.HAT_PLANNER, {"ALPHA": "literal {{X}} text"}, "{{ALPHA}}")
    assert out == "literal {{X}} text"


# --- dispatcher-block stripping -----------------------------------------------
def test_strip_dispatcher_block_removes_leading_comment():
    raw = pb.load_template(pb.HAT_PLANNER)
    assert "DISPATCHER NOTES" in raw
    body = pb.strip_dispatcher_block(raw)
    assert "DISPATCHER NOTES" not in body
    assert body.startswith("You are an independent planner")


def test_strip_dispatcher_block_noop_without_leading_comment():
    assert pb.strip_dispatcher_block("plain body, no comment") == (
        "plain body, no comment"
    )


# --- prompt-map override vs kit template --------------------------------------
def test_prompt_map_override_wins_over_kit_template(tmp_path):
    override = tmp_path / "my-planner.md"
    override.write_text("CUSTOM OPERATOR TEMPLATE {{GOAL_BRIEF}}", encoding="utf-8")
    got = pb.load_template(pb.HAT_PLANNER, override=str(override))
    assert got == "CUSTOM OPERATOR TEMPLATE {{GOAL_BRIEF}}"
    # With no override the shipped kit template loads instead.
    assert "DISPATCHER NOTES" in pb.load_template(pb.HAT_PLANNER)


def test_load_template_rejects_unknown_hat():
    with pytest.raises(KeyError, match="unknown hat"):
        pb.load_template("DUALPLAN-BOGUS")


# --- hat key vocabulary stability ---------------------------------------------
def test_hat_keys_vocabulary_is_stable():
    assert set(pb.HAT_KEYS) == {
        "DUALPLAN-PLANNER",
        "DUALPLAN-CRITIC",
        "DUALPLAN-ARBITER",
    }
    assert pb.HAT_KEYS["DUALPLAN-PLANNER"] == "dual-plan-planner.template.md"
    assert pb.HAT_KEYS["DUALPLAN-CRITIC"] == "dual-plan-critic.template.md"
    assert pb.HAT_KEYS["DUALPLAN-ARBITER"] == "dual-plan-arbiter.template.md"
    # Every mapped template is a real shipped kit file.
    for fname in pb.HAT_KEYS.values():
        assert (pb.PROMPTS / fname).exists()


# --- CLI (documentation aid) --------------------------------------------------
def test_cli_surface_prints_registry_material_not_sentinel(tmp_path):
    _fixture_repo(tmp_path)
    proc = run_py(
        [SCRIPTS / "plan_briefs.py", "--root", tmp_path, "surface"], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-061" in proc.stdout
    assert "IF-059" in proc.stdout
    assert SENTINEL not in proc.stdout
