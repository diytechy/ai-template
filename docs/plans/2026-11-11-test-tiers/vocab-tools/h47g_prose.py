"""HANDOFF 4.5.5, 4.5.7 and 10.7 item 1 in the shipped prose and this
repository's own surfaces, by line (hline.py). Each "bar" read and given the
word its sense needs: a stage (4.5.5), a standard, minimum or threshold
(4.5.7), or the checks that run (the glossary's terms).

Kept: the retired axis named as retired (PROCESS.md 571, PROCESS_OPTIONS.md
215-227, gate-advance's "what used to be called a 'bar'"), the glossary's
"Formerly" lines, LOG.template's "stage/bar names" (a log keeps the words of
its day). Twins re-copied after: docs/gate-policy.md is checked against the
scaffold's text by test_gate_policy; docs/rubrics/ against the rubric
templates (trap 22).
"""

K = "project-trajectory/"
SK = K + "skills/"

LINES = [
    ("CLAUDE.md", 33, "the same bar:", "the same standard:"),
    ("CLAUDE.md", 61, "red tier FAILS the bar;", "red tier FAILS the checks;"),
    ("CLAUDE.md", 69, "runs the full bar declared", "runs the full checks declared"),
    (K + "AGENTS.template.md", 39, "before a bar.", "before a stage is accepted."),
    (K + "AGENTS.template.md", 46, "The check harness is the bar:", "The check harness is the standard:"),
    (K + "AGENTS.template.md", 153, "  bar. When reality", "  stage. When reality"),
    (K + "PROCESS.md", 29, "the bars **DevStg-Reqs", "the stages **DevStg-Reqs"),
    (K + "PROCESS.md", 137, "The full quality bar", "The full quality standard"),
    (K + "PROCESS.md", 196, "  bar. A regulated setting", "  minimum. A regulated setting"),
    (K + "PROCESS.md", 201, "  bar requires).", "  stage requires)."),
    (K + "PROCESS.md", 341, "the bar is", "the standard is"),
    (K + "PROCESS.md", 472, "harness is still the bar", "harness is still the standard"),
    (K + "PROCESS.md", 661, "lowest runnable bar;", "lowest runnable stage;"),
    (K + "PROCESS.md", 1025, "DevStg-Reqs/DevStg-Tests bar", "DevStg-Reqs/DevStg-Tests stages"),
    (K + "PROCESS.md", 1148, "bar the project has actually earned", "stage the project has actually earned"),
    (K + "PROCESS.md", 1153, "runs the full bar regardless.", "runs the full checks regardless."),
    (K + "PROCESS.md", 1154, "end-state DevStg-Impl bar", "end-state DevStg-Impl checks"),
    (K + "PROCESS_OPTIONS.md", 187, "runs the declared bar", "runs the declared checks"),
    (K + "PROCESS_OPTIONS.md", 432, "harness is the bar everywhere", "harness is the standard everywhere"),
    (K + "PROCESS_OPTIONS.md", 550, "every bar except", "every gate except"),
    (K + "PROCESS_OPTIONS.md", 1330, "toward a written bar.", "toward a written standard."),
    (K + "PROCESS_OPTIONS.md", 1599, "a bar checkable only by executing", "a standard checkable only by executing"),
    (K + "PROCESS_OPTIONS.md", 1618, "The bar is **honesty**", "The standard is **honesty**"),
    (K + "PROCESS_OPTIONS.md", 1647, "The bar is that a second person", "The standard is that a second person"),
    (K + "PROCESS_OPTIONS.md", 1656, "Two bars ride the marker.", "Two standards ride the marker."),
    (K + "PROCESS_OPTIONS.md", 1890, "are the bar;", "are the standard;"),
    (K + "PROCESS_OPTIONS.md", 2073, "the derived gate/bar pointers", "the derived stage pointers"),
    (K + "PROCESS_OPTIONS.md", 2898, "the **declared bar**", "the **declared checks**"),
    ("README.md", 75, "acceptance bars (DevStg-Reqs", "acceptance stages (DevStg-Reqs"),
    ("README.md", 76, "each gate's bar **fails, never", "each gate's checks **fail, never"),
    ("README.md", 142, "iterates toward the bar", "iterates toward the standard"),
    ("README.md", 175, "wired at all three bars", "wired at all three stages"),
    ("README.md", 449, "the smoke bar,", "the smoke tier,"),
    ("README.md", 515, "never because the bar came down", "never because the minimum came down"),
    (K + "README.md", 45, "rubric, the bar a component scope's", "rubric, the standard a component scope's"),
    (K + "README.md", 55, "RUNS the declared bar itself", "RUNS the declared checks itself"),
    (K + "README.md", 74, "runs at every bar with", "runs at every stage with"),
    (K + "README.md", 88, "the DECLARED bar run on the composed tree", "the DECLARED checks run on the composed tree"),
    (K + "README.md", 106, "N lanes' bars genuinely overlap", "N lanes' checks genuinely overlap"),
    (K + "README.md", 107, "reverting code the bar refuses", "reverting code the checks refuse"),
    (K + "README.md", 194, "clears the bars **DevStg-Reqs", "clears the stages **DevStg-Reqs"),
    (K + "README.md", 198, "as the bar.", "as the standard."),
    (K + "rubrics/README.template.md", 15, "toward a written bar", "toward a written standard"),
    (K + "rubrics/README.template.md", 41, "  bar, the TC names", "  standard, the TC names"),
    (K + "rubrics/README.template.md", 44, "the bar a", "the standard a"),
    (K + "rubrics/README.template.md", 63, "the same bar as", "the same standard as"),
    (K + "rubrics/architecture-decomposition.template.md", 22, "the bar that artifact", "the standard that artifact"),
    (SK + "README.md", 24, "are the bar (see", "are the standard (see"),
    (SK + "architecture-decomposition/SKILL.md", 10, "The bar is the rubric", "The standard is the rubric"),
    (SK + "gate-advance/SKILL.md", 183, "## What each bar takes", "## What each stage takes"),
    (SK + "gate-advance/SKILL.md", 228, "a bar closure is", "a stage's closure is"),
    (SK + "gate-advance/SKILL.md", 249, "a bar's readiness", "a stage's readiness"),
    (SK + "gate-advance/SKILL.md", 251, "A vouched bar can be", "A vouched stage can be"),
    (SK + "llm-vision-convergence-loop/SKILL.md", 12, "near the bar.", "near the threshold."),
    (SK + "render-compare-eval-loop/SKILL.md", 26, "the bar is met", "the standard is met"),
    (K + "prompts/dual-plan-planner.template.md", 81, "## Quality bar", "## Quality standard"),
    (K + "prompts/spine-questions.md", 82, "the quality bar written down", "the quality standard written down"),
    (K + "EXAMPLE.md", 247, "That is the bar each gate enforces.", "That is the standard each gate enforces."),
    (K + "EXTERNAL_SKILLS.md", 53, "offline/stdlib bar", "offline/stdlib rule"),
    (K + "KICKOFF_PROMPT.md", 238, "quality bar:", "quality standard:"),
    (K + "agent-hooks/README.md", 6, "so the bar holds", "so the standard holds"),
    ("docs/gate-policy.md", 62, "The harness is still the bar", "The harness is still the standard"),
    (".github/workflows/test.yml", 94, "No bar fails on the tier's seconds", "No run of the checks fails on the tier's seconds"),
    (".github/workflows/test.yml", 118, "the same bar", "the same checks"),
    (".github/workflows/test.yml", 133, "a code-quality bar", "a code-quality standard"),
    # 4.5.2's key, in the template registry's example row
    (K + "registries/work-items.template.csv", 2, "and Bar (optional DevStg-Reqs", "and ChecksStage (optional DevStg-Reqs"),
    (K + "registries/work-items.template.csv", 2, "bar declares verification strictness for this row's lane", "the stage this row's landing checks run at"),
]
