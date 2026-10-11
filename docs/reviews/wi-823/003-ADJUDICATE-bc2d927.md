# ADJUDICATE — WI-823 @ bc2d927: dispute W823F1

Scope bound: PROCESS.md §6 "Review threat model" (normal working environment,
supported configurations, regressions of supported behaviour). This finding
needs no contrived host, so the bound does not exclude it; it is ruled on the
code.

**W823F1** (K4, RESYNC_PACK entry owed for
`project-trajectory/skills/render-dashboard-critique/SKILL.md`). Rubric K4
(`docs/rubrics/kit-change-review.md`) binds "a change to a **shipped** file".
Whether this file ships is a fact of the code at this range, and I checked it:
- the skill's frontmatter declares `scope: this-repo`;
- `bootstrap.py` `select_skills` (line 534 onward) skips every skill whose scope
  is not `kit` ("`this-repo` skills maintain *this* template and are meaningless
  in an adopted product repo");
- `delivery_inventory` (around line 1897–1903) excludes the whole directory of a
  non-`kit` skill with the reason "scope: this-repo skill; never materialized
  downstream", and RESYNC_PACK.md (around line 7705) already records that
  exclusion;
- `ADOPTING.md` (lines 20–29) says the adopter's repo "never receives a copy" of
  the kit checkout, so the file cannot reach them as part of a vendored kit tree
  either.

An adopter therefore never holds this file, and a RESYNC entry would tell them to
re-sync something they do not have. Being under `project-trajectory/skills/`
puts the file in the shipped tree's directory, but the scope declaration keeps it
out of what is delivered. The other files the lane changes are outside the kit,
at the repo root: `scripts/dashboard-shots/*`, `docs/rubrics/*`, the registries
and the dogfooded `.claude/` and `.agents/` skill copies. So K4 is owed nowhere in
this range.

RULING: W823F1 DISMISS refuted the skill is `scope: this-repo`, which bootstrap.py `select_skills` and `delivery_inventory` exclude from downstream delivery, and adopters never receive the kit tree (ADOPTING.md), so it is not a shipped file and K4 owes no RESYNC_PACK entry
