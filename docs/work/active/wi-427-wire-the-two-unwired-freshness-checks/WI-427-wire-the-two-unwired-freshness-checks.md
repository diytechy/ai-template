+++
id = "WI-427"
title = "SN-010 says every generated artifact carries a --check freshness contract; two committed, DECLARED-generated artifacts have a working --check that runs NOWHERE, so the need is currently false. (1) project-trajectory/prompts/CATALOG.md, declared generated at docs/stack.ini [generated] as `promptcatalog`: gen_prompt_catalog.py --check works, and zero references to it exist in check.py, the pre-commit hook, .github/workflows or ci/check.yml. (2) project-trajectory/skills/INDEX.csv, declared as `skillsindex`: gen_skills_index.py --check (index-vs-SKILL.md staleness) is wired nowhere, and only the DIFFERENT --check-agents mode (per-agent copy drift) runs, as the skills-sync step - so a stale INDEX.csv passes every gate. Wire both into check.py's built-in step table and the hook's --run-steps list following the arch-map/okf/derived-gate/ratify-fresh idiom, deciding each step's GATE SET on what the artifact means rather than by copying the most common value, and deciding fold-vs-separate for the skills index on the two modes' actual properties. MAKE THEM NON-VACUOUS: plant a defect in a temp tree and prove each step REDS, with a test per step - a freshness step that cannot fail is the SN-008 green-hides-a-skipped-check failure and would be worse than the gap. ALSO verify the census claim that these are the only two gaps, reporting the full [generated]-vs-wiring table."
workstream = "scripts"
specref = "docs/requirements/stakeholder-needs.toml"
buildtier = "medium"
safety_class = "ordinary"
+++

## Context

**SN-010 is a ratified core stakeholder need**, and it is stated universally:
*every* generated artifact carries a `--check` freshness contract. A universal
claim is false the moment one instance fails it. Two do.

**This row makes the need TRUE; it does not edit the need.** SN-010's own prose
is sitting territory (the 2026-08-10 prose-rewrite plan) and is out of scope
here, as are `docs/repo-lock.md`, `docs/plans/*`, and any registry row's text.

**Why this is worse than an ordinary gap.** Both artifacts are declared in
`docs/stack.ini`'s `[generated]` section — the §5.2 declaration of *what the
repo owns as derived*. A declaration with no enforcer is the shape SN-008
forbids from the other direction: the tree asserts a contract that nothing
holds it to, so a reader (human or agent) reasonably concludes the artifact is
gated when it is not. `CATALOG.md`'s whole purpose is to answer *"which prompt
template did that session use"* from a session log's `prompt-sha` — a lying
catalogue is worse than no catalogue, as its own module docstring says.
`INDEX.csv` is what an agent reads to decide whether a skill applies.

**The three decisions this row owns**, to be argued from the precedents rather
than assumed: each step's gate set (the existing spread is real —
`derived-gate` at `{G1,G2,G3}`, `ratify-fresh` at `{G2,G3}`, the doc-freshness
family at `{G3}`); whether the INDEX staleness check folds into the existing
`skills-sync` step or becomes its own; and whether the shipped reference CI
(`project-trajectory/ci/check.yml`) needs any change — it invokes `check.py` as
a single entry point, which must be *verified* rather than assumed.

**Non-vacuity is the acceptance bar, not a nicety.** Wiring a check that cannot
fail converts a visible gap into an invisible one. Each new step must be shown
red against a planted defect, in a temp tree, with the proof kept as a test.
