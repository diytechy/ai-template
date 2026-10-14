# docs/plans/ — live plan documents

**Open for owner ruling:**
[`2026-09-20-validation-gap-and-the-assumption-tier.md`](2026-09-20-validation-gap-and-the-assumption-tier.md)
— proposes recording the domain assumptions that carry interface facts up to
the human outcomes needs are written about, as rows the requirements cite, and
redrawing the depth-0 view as two frames (the kit in operation, and the system
that delivers it). Revised after an adversarial review; carries its own impact
survey, staging and a rendered mockup ([`mockups/`](mockups/)).
Its sister, [`2026-09-23-owner-notes-spine-sessions-and-tests.md`](2026-09-23-owner-notes-spine-sessions-and-tests.md)
— the owner's 2026-09-23 notes on spine authoring, sessions and test strategy,
each set against what the repo already does, with fifteen questions.
Their first sitting's decision surface is
[`2026-09-25-c1-sitting-package.md`](2026-09-25-c1-sitting-package.md): the
frame rows, the reversed rulings, the stakeholder rows and the two headline
needs the owner signs at C1, and how the sitting is run. The spine derived from
the plan while the owner is away, with every assumption and decision taken on
the way, is recorded in
[`2026-09-25-assumption-tier-spine-map.md`](2026-09-25-assumption-tier-spine-map.md).

Also open for owner ruling:
[`2026-09-28-duplicated-stage-detection.md`](2026-09-28-duplicated-stage-detection.md)
— WI-624's research result (S14): call-sequence and near-miss detection
measured against this repository's past consolidations, with the ground truth,
each method's recall and noise, and a recommendation. It adopts nothing; its
producing script sits beside it.

Also open for owner ruling:
[`2026-10-07-wi841-retro/`](2026-10-07-wi841-retro/README.md)
— the WI-841 retrospective: why the lane took as long as it did. It holds the
proposal (rows P1–P8 and the guards on spine approval), its reconciliation
with the queue (§8, with five owner questions), and the reviewed drafts of the
`coordinator-cycle` and `spine-authoring` skill changes. The owner's rulings
from it are in the 2026-10-07 log fragment.

Answered by the owner on 2026-10-13 and 2026-10-14:
[`2026-10-13-contract-split-divergence.md`](2026-10-13-contract-split-divergence.md)
— what the `contract_split` branch holds that this branch never received
(110 commits from 2026-09-06 to 09-07): the primary-adjudication code, four
colliding spine IDs, and 40 amended requirement rows, including a 2026-09-06
SN-036 ruling missing here, whose withdrawn design this branch has since built
(WI-688). Its read-only census script sits beside it.

Ruled by the owner on 2026-10-11, being built:
[`2026-10-11-review-churn/`](2026-10-11-review-churn/README.md)
— why coordinator legs take so long: where review-round churn comes from
(2026-10-09 → 10-11), whether splitting work items pays, and six changes to cut
it (closed coverage, record-at-event, a size basis for splits, full-lane
rounds, lint before review), plus a third-family second reviewer, usage
recording for every model call, a reviewed plan before the build, and one
TOML configuration file. Its "Owner rulings" section records every call;
item 11 (what points where) is open, and a separate review handoff in the
folder boots independent Codex Astra and Claude Fable reviews.

The live planning surface. **Start at
[`2026-08-15-review-package.md`](2026-08-15-review-package.md)** — the one
document the pending review sitting runs from; the 2026-08-15 plan set
(re-tier completion, interface rework, D-9 migration, snapshot design) records
the charge-through it packages, and the 2026-08-16 set (re-tier v2's cursor, the
tiering research memo, the blind-derivation inputs and their alignment map)
records the work that followed — each stamped with its own execution state. The
two sitting documents remain the ruling record —

- [`2026-08-13-sitting-2-boundary-and-context.md`](2026-08-13-sitting-2-boundary-and-context.md)
  — rules the depth-0 boundary, the operational context, the port list, the
  partition, the hats roster, and the tabled structural calls; carries the
  downhill impacts on the queued WIs and the housekeeping ledger.
- [`2026-08-13-sitting-3-spine-verification.md`](2026-08-13-sitting-3-spine-verification.md)
  — verifies the adapted spine after sitting 2's rulings execute; owns the
  re-attest window close, the LLR/TC draft ratifications, and the D-9
  status-ladder decision.

Everything older — the sitting pack, the boundary draft, the measured data
packs, the prose-rewrite plan and its ledgers, and the closed `DP-001` dual-plan
round — is archived with per-file dispositions at
[`../archive/plans/`](../archive/plans/README.md); sitting 2 §7 is the audit of
what was carried forward versus pointed at.

Dual-plan decomposition rounds land here as one directory per round,
`DP-NNN-<slug>/`, holding the round's tracked artifacts: the goal brief
(numbered `C#` clauses), both plans and their revisions, the cross-critiques,
the computed `coverage*.md` reports, and `verdict.md` (the arbiter's
select-and-port ruling). The protocol, its safeguards, and the hard caps are
defined once in the process-options master ("Dual-plan decomposition"); the
verdict is summarized in [log.md](../log.md) and the selected plan's rows are
filed as real WIs in [docs/work/](../work/). A closed round archives to
`../archive/plans/` intact, as a unit.
