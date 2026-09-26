+++
id = "WI-648"
title = "adjudicate: LLR-140, LLR-143, LLR-151, TC-132, TC-144, TC-145 - approved cells amended by WI-612's bookkeeping helper; judge whether scope moved"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-156"]
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
priority = 2
+++

## Context

WI-612 replaced the claim's clean-trunk refusal and the dispatcher's
dirty-trunk stop with one shared bookkeeping helper that refuses by name a
dirty path the step must write, and ignores the owner's scratchpad. Six
approved rows stated the old behaviour, and the build amended their attesting
cells in the same change (status left `Approved`, nothing re-anchored):

- LLR-140 `detail`, LLR-143 `detail`, LLR-151 `detail` (plus traced `module`
  and `code_symbol`)
- TC-132 `method`, TC-144 `method`, TC-145 `method` (plus traced `verifies`)

Each row now differs from its copy in `docs/archive/last_approved/`. The
design-row and test-case tiers are released to the adjudicator
(`human_approval_through = "DevStg-Needs"`), so a MEANING verdict is
re-attested by the adjudicator, re-anchoring only these rows.

## Done-when

- Each amended row is ruled MEANING or CLARITY, with the verdict recorded
  where the amendment brief puts it.
- A MEANING row whose new text is blessable is re-anchored in its own commit,
  naming exactly these rows; one that is not gets its corrective work drafted
  in `## Dispositions`.
