+++
id = "WI-680"
title = "adjudicate: SR-151, SR-152, SR-157, SR-175, SR-198, SR-212, LLR-051, LLR-056, LLR-057, LLR-124, LLR-139, LLR-160, LLR-180, LLR-233, LLR-244, LLR-254, TC-036, TC-055, TC-067, TC-068, TC-077, TC-086, TC-100, TC-175, TC-189, TC-198, TC-228, TC-239, TC-247 - approved cells amended by the fourth build wave (WI-582, WI-656, WI-672, WI-638); judge whether scope moved"
workstream = "process"
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-036", "SR-054", "SR-151", "SR-152", "SR-157", "SR-159", "SR-161", "SR-164", "SR-168", "SR-170", "SR-175", "SR-180", "SR-198", "SR-212", "SR-215"]
needs = ["WI-582", "WI-656", "WI-672", "WI-638"]
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-151", "SR-152", "SR-157", "SR-175", "SR-198", "SR-212", "LLR-051", "LLR-056", "LLR-057", "LLR-124", "LLR-139", "LLR-160", "LLR-180", "LLR-233", "LLR-244", "LLR-254", "TC-036", "TC-055", "TC-067", "TC-068", "TC-077", "TC-086", "TC-100", "TC-175", "TC-189", "TC-198", "TC-228", "TC-239", "TC-247"]
priority = 2
+++

## Context

Spine-acts batch B, amendment half (the fourth coordinator's handoff,
`docs/handoff-2026-09-27-wave4-coordinator.md`, first job 2). The fourth build
wave amended approved spine rows in place to the code each item built, status
left `Approved` and nothing re-anchored, so each row now differs from its copy
in `docs/archive/last_approved/`. Under row-level refusal an unjudged amendment
blocks every other act that copies its registry, so the amendments are judged
together here, in the same adjudicator session as WI-681 (the batch's
first-approval half: a different verdict grammar, so a separate row), and ONE
`intake.py snapshot` act re-anchors the rows a MEANING verdict blesses together
with WI-681's approvals. Precedent: WI-669 and batch A (bc6a245f).

The amended attesting cells, by the item that amended them:

- WI-582 (the spine authoring sweep, the redrawn C1 frame): SR-151, SR-152,
  SR-157, SR-175 `rationale`; LLR-051, LLR-056, LLR-057, LLR-124, LLR-139
  `detail`.
- WI-656 (checker findings that lie; wave-4 ruling 1 on the `module` cell):
  LLR-160, LLR-180 `detail`; TC-175 `method`.
- WI-672 (the tier rule; wave-4 rulings 5, 9 and 14): TC-067, TC-068, TC-077,
  TC-086, TC-100, TC-189, TC-198 `tier`, Smoke -> Full; TC-068 `expected`
  (the retired "unjustified seam" arm dropped, under the coordinator's grant).
- WI-638 (the assumption build; OI-88 (c); wave-4 rulings 2, 7 and 11):
  SR-198 `requirement` and `acceptance_criteria`; SR-212 `title`,
  `requirement`, `acceptance_criteria` and `rationale` (the Boundary arm over
  crossings, interface-form requirements only); LLR-233, LLR-244, LLR-254
  `detail`; TC-228, TC-239 `method` and `expected`; TC-247 `method`; TC-036,
  TC-055 `inputs` and `max_age` declared.

Traced pointer cells moved on the same rows, which re-open no attestation but
appear in the brief: LLR-244 `module` and `code_symbol`; LLR-254
`code_symbol`; TC-068 and TC-175 `evidence`; TC-239 and TC-247 `verifies`.

Checked against the registries and `docs/archive/last_approved/` at the filing
commit: every row above differs from its approved copy in an attesting cell,
and no other approved spine row does. Seven more approved rows differ in traced
cells only and are not listed: LLR-242 and LLR-243 (`module`, `code_symbol`),
TC-075, TC-153 and TC-196 (`evidence`), TC-237 and TC-248 (`verifies`). The
copy carries them.

The approval dial reads `human_approval_through = "DevStg-Boundary"`; what a
MEANING verdict owes next on each tier is derived from it, and the amendment
brief states it.

## Done-when

- Each amended row is ruled MEANING or CLARITY, with the verdict recorded
  where the amendment brief puts it.
- A MEANING row whose new text is blessable is re-anchored in ONE act shared
  with WI-681, whose `--reattests` names exactly the blessed rows; one that is
  not gets its corrective work drafted in `## Dispositions`.
