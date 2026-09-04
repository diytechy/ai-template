+++
id = "WI-596"
title = "The anchoring copy's absorb ledger: the first-approval brief and the approval act's record name every drifted Approved row a whole-file snapshot re-blesses"
workstream = "process"
specref = "docs/reviews/wi-590-adjudicate-llr-207-llr-208/008-REVIEW-A-9671078.md"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

Drafted by WI-590 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

REWORK OF ROUND 008's MAJOR, drafted by the supervising session (2026-09-04)
after two adjudication sessions declined it as `@owner`. The finding stands
and is driven: at this lane's merge base `baseline_snapshot.refresh_ledger`
lists 10 LLR rows (LLR-045, LLR-058, LLR-136, LLR-140, LLR-144, LLR-158,
LLR-197, LLR-198, LLR-203, LLR-204) and 4 TC rows (TC-082, TC-138, TC-147,
TC-194) whose Approved text had moved under the snapshot, and the act at
`a1d80c6f` (`--approves` naming the LLR and TC registries for LLR-208 and
TC-206) copied both files whole, so all 14 now read as blessed with nothing
naming them. WHAT THE LEDGER SAYS ABOUT THEM, so the debt does not vanish
with the copy: 13 of the 14 were judged before this lane — LLR-045, LLR-140
and TC-082 by WI-585 (MEANING; the re-anchor was the act its verdict
prescribed and the unscoped refusal blocked until WI-584 landed); LLR-058,
LLR-144, LLR-198, TC-138, TC-147 and TC-194 by WI-566 (MEANING); LLR-136
and LLR-158 by WI-573; LLR-158, LLR-203 and LLR-204 by WI-578 (MEANING, same
blocked re-anchor). The one UNJUDGED row is LLR-197, reworded on the trunk at
`14beba0a` outside any lane; its amendment adjudication is WI-593, minted at
`09193fea`. The copy therefore absorbed thirteen judged rows and one that now
has its judge queued.

IN SCOPE for the successor, the structural half round 008 asked for:
`project-trajectory/prompts/adjudicate-first-approval.template.md` step 2
tells the adjudicator only that returned rows "stay Drafted inside it" and is
silent on pre-existing drift — render the absorb ledger in the brief the way
`{approves_rows}` is rendered (one line per drifted row with its registry,
cell and the verdict that judged it, or "UNJUDGED"), and have the act's own
record (`acceptance_record` / the ADJUDICATE round file's governing section)
enumerate the absorbed set so the ledger survives the copy in a file the
rollup and intake read. A row the ledger marks UNJUDGED and no verdict names
holds the flip until an act names it. No change to the whole-file snapshot
granularity: `unanchored_findings` is decidable only because the copy is a
whole file, as round 008 itself states.

ROUND 005's MAJOR (LLR-208's exclusive-writer clause contradicted by the
generator writing `docs/reviews/rollup/` on a claimed branch) is closed on the
TRUNK, not by a draft: `gen_verdict_rollup.py` now refuses a direct write on
any branch other than the trunk and the trunk step passes `--trunk-step`
(`tests/test_verdict_record.py::test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`),
landed on the trunk at `7ea3cce7` — it reaches this lane through the
station's refresh, the one merge the verdict gate peels, so it is not
hand-merged here. The registry debt that fix leaves (LLR-208 and TC-206 no
longer describing their module in full) is the amendment half of the spine
successor this same verdict drafts — "LLR-207/TC-205 return and LLR-208/TC-206
amendment" — which needs no ordering against any other row: WI-594 was
narrowed on the trunk to LLR-209 and TC-207.
