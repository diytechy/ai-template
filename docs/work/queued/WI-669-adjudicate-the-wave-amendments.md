+++
id = "WI-669"
title = "adjudicate: LLR-140, LLR-143, LLR-154, LLR-167, LLR-216, LLR-224, LLR-246, LLR-248, LLR-250, LLR-257, SR-209, SR-211, TC-061, TC-135, TC-137, TC-144, TC-145, TC-161, TC-164, TC-170, TC-178, TC-192, TC-206, TC-222, TC-244 - approved cells amended by the second build wave; judge whether scope moved"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-026", "SR-144", "SR-146", "SR-148", "SR-156", "SR-174", "SR-189", "SR-190", "SR-193", "SR-194", "SR-197", "SR-198", "SR-208", "SR-209", "SR-211", "SR-214", "SR-217"]
needs = ["WI-664", "WI-652"]
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-140", "LLR-143", "LLR-154", "LLR-167", "LLR-216", "LLR-224", "LLR-246", "LLR-248", "LLR-250", "LLR-257", "SR-209", "SR-211", "TC-061", "TC-135", "TC-137", "TC-144", "TC-145", "TC-161", "TC-164", "TC-170", "TC-178", "TC-192", "TC-206", "TC-222", "TC-244"]
priority = 2
+++

## Context

The second build wave amended approved spine rows in place to the code each
item built, status left `Approved` and nothing re-anchored, so each row now
differs from its copy in `docs/archive/last_approved/`. Under row-level
refusal an unjudged amendment blocks every other act that copies its
registry, so the amendments are judged together here and one
`intake.py snapshot --reattests` re-anchors the rows a MEANING verdict
blesses.

The amended attesting cells, by the item that amended them:

- TC-061 `method` (WI-645)
- TC-161 `method` (WI-645, WI-646) and `tier` (WI-645)
- LLR-167 `detail` (WI-646, WI-664)
- TC-222 `tier` (WI-629)
- LLR-257 `detail` (WI-640)
- SR-209 `acceptance_criteria`, LLR-246 `detail`, LLR-248 `detail` (WI-636)
- TC-145 `method` (WI-647)
- LLR-140 `detail`, LLR-143 `detail`, LLR-154 `detail`, TC-144 `method`,
  TC-137 `method` (WI-664; TC-144's clause on the dispatcher reading past a
  dirty owner scratchpad moved to TC-137, LLR-143's test case; LLR-143 and
  TC-137 were then checked clause by clause against `dispatch.py` and
  `tests/test_dispatch.py`, which corrected the no-branch-ref residue,
  NEEDS-HUMAN handback, pause, refresh-bar and lanes clauses)
- LLR-216 `detail` (WI-653)
- SR-211 `acceptance_criteria`, LLR-250 `detail`, TC-244 `method` and
  `expected`, LLR-224 `detail` (WI-654)

- TC-135, TC-164, TC-170, TC-178, TC-192 and TC-206 `tier`, Smoke -> Full
  (WI-652, the smoke re-tier ruled OI-92 (b); arbitration ruling 4(ii): each
  case's method has a clause that inherently drives git, a subprocess or a
  scaffold, so its evidence cannot all run in the per-commit tier; traced
  `evidence` pointers of TC-135, TC-170, TC-178 and TC-206 moved to the split
  fast or slow modules)

Traced pointer cells moved on the same rows, which re-open no attestation but
appear in the brief: LLR-167 `code_symbol`; LLR-246 and LLR-248 `module` and
`code_symbol`; TC-145 and TC-222 `evidence`; TC-244 `verifies`.

Checked against `python project-trajectory/scripts/trace.py --approve
modified` at WI-664's build (base e1325e24 plus WI-664's amendments): every
row above differs from its approved copy, and no other row differs in an
attesting cell. Seven further approved rows differ from their copies in the
traced `verifies` cell alone, each gaining an interface id, and are not
listed above: TC-226, TC-227 and TC-228 (WI-631), TC-241 and TC-242 (WI-636),
TC-246 (WI-637), TC-250 (WI-640). The brief's off-spine census also reports
the interfaces and components registries changed since the snapshot; it has
no per-row rendering.

The approval dial reads `human_approval_through = "DevStg-Needs"`; what a
MEANING verdict owes next on each tier is derived from it, and the amendment
brief states it.

## Done-when

- Each amended row is ruled MEANING or CLARITY, with the verdict recorded
  where the amendment brief puts it.
- A MEANING row whose new text is blessable is re-anchored in its own commit,
  naming exactly these rows; one that is not gets its corrective work drafted
  in `## Dispositions`.
