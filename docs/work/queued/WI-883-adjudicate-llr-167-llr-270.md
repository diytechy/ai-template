+++
id = "WI-883"
title = "adjudicate: LLR-167, LLR-270, TC-161, TC-322 - approved/routed cell(s) amended on merged trunk c36cbc8..2b9817a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-167", "LLR-270", "TC-161", "TC-322"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-167 `Detail`: 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…' -> 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- TC-161 `Method`: 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…' -> 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…'
- TC-161 `Verifies`: 'LLR-167;IF-124;IF-075' -> 'SR-146;LLR-167;IF-124;IF-075'
- TC-322 `Method`: 'Run test_the_loop_composes_the_same_keep_request_as_before, test_switching_retained_classes_with_nothing_edited_keeps_t…' -> 'Run test_the_loop_composes_the_same_keep_request_as_before, test_switching_retained_classes_with_nothing_edited_keeps_t…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
