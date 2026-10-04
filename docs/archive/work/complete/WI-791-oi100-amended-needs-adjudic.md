+++
id = "WI-791"
title = "Route amended needs to the meaning-or-clarity adjudication; CLARITY re-attests on a held rung"
workstream = "process"
specref = ""
sr_refs = ["SR-178", "SR-207", "SR-228"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

OI-100 (ruled (a), 2026-10-03), built on lane `wi-791` and landed by squash; the lane tip is kept in `archive/lanes`.

- **Gap 1.** The amendment walk reads `acceptance_record.AMENDMENT_CSVS`, an alias of the approval-act set (SR, LLR, TC, SN, DA, SUR), so an amended approved need, assumption or surrogate mints one `amendment` adjudication row. The pre-commit amend-without-flip warn takes the same scope (decision D-002). The amendment brief renders those tiers' rows (D-005; without it a need-scoped row refused to compose, a departure from OI-100's "the brief is unchanged").
- **Gap 2.** `intake.adjudication_action` gains the held-rung CLARITY arm (`reattest`). An act may name its verdict (`snapshot --verdict`, an optional ledger field, recorded repo-relative). The merge slot refuses a held-rung re-attestation whose verdict does not rule the row CLARITY, reads the dial at trunk's tip, and refuses a row below approval (D-003, D-008, D-010). PROCESS.md §4 states the one case. No script approves (OI-45 stands).
- **Gaps 0 and 3.** The brief tells a CLARITY verdict to name its rows in `--reattests`; one MEANING row still holds its CLARITY siblings, and the brief says so.
- **Audit.** `open-items.html` section 2 lists every verdict-carrying act, newest first (D-004).
- **Spine.** GPT Terra authored the rows; new SR-228 (held-rung CLARITY re-attestation). An independent Opus adjudicator sat in the lane over three fix rounds (verdicts 001-005 under `docs/reviews/wi-791-oi100-amended-needs-adjudic/`) and took act seq 29: SR-228 approved; SR-178, LLR-118, LLR-153, LLR-158, LLR-167, LLR-245, LLR-271, LLR-278, TC-123, TC-147, TC-153, TC-161, TC-240 and TC-278 re-attested.
- **Reviews.** Codex 6.1 Sol: round 1 at `523d576a` (3 MAJOR, 2 MINOR; all confirmed and fixed); the final review of the post-act tree at `38709c82` (no BLOCKER or MAJOR; two MINORs, verdict-path canonicalization and a DA/SUR test assertion, fixed in 2eaa8ebd and re-checked SOUND).
- **RESYNC_PACK** entry `[since 2aad71a3]`; no migration.
- **Decisions record:** `docs/decisions/wi-791.toml`, D-001 to D-010 (D-003 high risk).
- **Follow-up (not filed; for WI-788's in-lane sitting):** an in-lane (S11) act never reaches the merge slot's `held_reattest_refusal`, which runs only for lanes whose every spec is an adjudication spec; on a held rung an in-lane re-attestation would not meet SR-228's refusal.

## Context

Filed by hand by the coordinator on 2026-10-03, when the owner ruled **OI-100**
option (a): "Agreed with recommendation." OI-100's `decision`, `blast_radius`,
`options` and `recommendation` cells in `docs/requirements/open-items.toml` are this
row's spec of record. The ruling's record is
`docs/log.d/2026-10-03-owner-rulings-oi100-oi102.md`.

It extends the existing mechanism and builds nothing parallel: WI-388's amendment
trigger and its one-question brief (MEANING or CLARITY). No script approves anything;
OI-45 stands.

## Done-when

- **Gap 0.** The shipped amendment brief's aftermath
  (`prompts/adjudicate-amendment.template.md`) says that a CLARITY verdict names its
  rows in the act's `--reattests` where the dial releases the rung, so the anchor
  copy stops drifting. Coordinators already do this.
- **Gap 1.** The amendment walk (`acceptance_record.SPINE_CSVS`, read by
  `intake._amendment_drafts`) also covers the need, assumption and surrogate tiers.
  The pre-commit warning's scope is decided in the same change and stated. A test
  shows that an amended approved need mints one `amendment` adjudication row.
- **Gap 2.** On a held rung, an independent adjudicator session re-attests a row it
  rules CLARITY, as a judgement act recorded in the act ledger with its verdict. It
  recommends a MEANING row to the owner, and it never approves a first draft on a
  held rung. This amends ruled decision 2's held-rung arm
  (`intake.adjudication_action`), the brief's held-rung aftermath and PROCESS.md §4,
  with one stated case and tests.
- **Gap 3** stays as it is: one MEANING row still holds its CLARITY siblings in the
  same registry until the owner signs, and the coordinator puts them in the same
  sitting. The brief says so.
- Every held-rung CLARITY re-attestation stays listed on the owner's surface for audit
  after the fact.
- The spine rows that pin the amendment trigger, ruled decision 2 and the brief are
  identified and amended through in-lane adjudication. This row's `sr_refs` and
  `specref` are set to them, replacing the open-items reference.
- A RESYNC_PACK entry: adopters who hold the needs rung will see need amendments
  minted as adjudication rows. No migration is forced.
- The commit bar passes.
