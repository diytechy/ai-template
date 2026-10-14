## 2026-10-14: coordinator (attended): the review-churn plan's revision 29 review pair, revisions 30 and 31, and the revision 31 review brief

Deferred open items: none ruled. OI-98, OI-105, OI-112, OI-113 and OI-114
stay the owner's.

This attended session took the lease and resumed from
[handoff-2026-10-11-attended-coordinator.md](../handoff-2026-10-11-attended-coordinator.md),
which stays the resume map. The owner chose to run the plan's optional
revision 29 review before filing batch 1, so nothing was claimed or built, and
`docs/work/pause` is unchanged.

- **Revision 29 review.** GPT-6 Astra (Codex) and Claude Fable 5.1 (a
  sub-agent), both at medium, ran in parallel in detached worktrees at
  `4c5287d2d` on `reviews/brief-r29.md`; both left their worktree unchanged
  and returned REVISE (Astra 5 findings, Fable 10). All 11 distinct findings
  held against the repository; none was dismissed. Reviews filed as
  `reviews/astra-medium-r29.md` and `reviews/fable-medium-r29.md`.
- **Revision 30** (`9c2c79a81`) folded them in. Item 16's carrier would have
  broken the watermark's hand-raise rule, `--bump-ids` (no count) and the act
  ledger's file-order rule; it now records each reservation (WI, space,
  range), checks a lane's new ids against it at landing, and writes the
  ledger union in seq order. Item 15's port gained LLR-061 and TC-061. The
  local `contract_split` branch stops at the ancestor `607cf609`, so the plan
  and the divergence report now name `961f9e47`. The latch's guards were
  corrected (disjoint snapshot copies merge cleanly, reproduced on WI-860 and
  WI-866; the sitting's basis added).
- **Revision 31** (`eae598aff`) records the owner's answers: verdicts move
  between lanes while acts keep landing order; the reservation record is
  confirmed; F-call 4 is answered by keep-or-mint, which now needs a
  cross-reference to the id's other users; the local `contract_split` branch
  is dead.
- **Revision 31 brief** (`3939b5180`): `reviews/brief-r31.md` and
  `review-handoff-r31.md`, for one more pair (Astra and Fable, both high) in
  a fresh session before any build. The brief ties severity to rework and adds
  a pre-mortem, a build-readiness walk and an ordering check of the
  coordinator handoff's queue against the plan's phase 1; the handoff makes
  the judging session test each finding for truth, reasonable occurrence and
  worth before acting.

Lesson for the procedure: `docs/open-items.html` can go stale with no source
change (its baseline line moved), and the pre-commit hook then refuses a
docs-only commit; regenerate it with `gen_open_items.py` and include it.
