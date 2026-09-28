+++
id = "WI-681"
title = "adjudicate: SR-183, SR-184, SR-185, SR-186, SR-220, SR-221, LLR-205, LLR-206, LLR-210, LLR-259, LLR-260, LLR-261, LLR-262, LLR-263, TC-199, TC-200, TC-201, TC-202, TC-203, TC-204, TC-208, TC-209, TC-210, TC-211, TC-252, TC-253, TC-254, TC-255, TC-256, TC-257, TC-258, TC-259 - spine rows authored Drafted and never approved; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-017", "SR-139", "SR-148", "SR-154", "SR-156", "SR-157", "SR-163", "SR-176", "SR-183", "SR-184", "SR-185", "SR-186", "SR-216", "SR-220", "SR-221"]
needs = ["WI-582", "WI-672", "WI-657", "WI-638", "WI-621"]
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["SR-183", "SR-184", "SR-185", "SR-186", "SR-220", "SR-221", "LLR-205", "LLR-206", "LLR-210", "LLR-259", "LLR-260", "LLR-261", "LLR-262", "LLR-263", "TC-199", "TC-200", "TC-201", "TC-202", "TC-203", "TC-204", "TC-208", "TC-209", "TC-210", "TC-211", "TC-252", "TC-253", "TC-254", "TC-255", "TC-256", "TC-257", "TC-258", "TC-259"]
priority = 2
+++

## Context

Spine-acts batch B, first-approval half (the fourth coordinator's handoff,
`docs/handoff-2026-09-27-wave4-coordinator.md`, first job 2). These spine rows
are BELOW approval and no act has blessed them. The approval dial reads
`human_approval_through = "DevStg-Boundary"`, which releases every spine tier
to an adjudication session: `trace.py --approve modified` renders every chain
below inside its "Waiting for automated adjudication" block, and no chain on a
held rung owes an act. So the scope is the whole Drafted population, not only
the fourth wave's.

By the item that authored each row:

- WI-582 (the spine authoring sweep and WI-604's RETURN): SR-220 (a labelled
  derived requirement under SN-025), LLR-210 (re-pointed to SR-220), TC-208
  (split: Smoke) and TC-254 (Full), LLR-259, TC-252, TC-253.
- WI-672: SR-221 (a labelled derived requirement under SN-012), LLR-260,
  LLR-263, TC-255, TC-258.
- WI-657: LLR-261, TC-256.
- WI-621: LLR-262, TC-257, TC-259.
- The 2026-09-25 assumption-tier sitting (77612fb2), collateral that arrived
  Drafted: SR-184, SR-185, SR-186 and their cases TC-209, TC-210, TC-211 (the
  three cases gained `inputs` and `max_age` at WI-638, wave-4 ruling 2).
- Older rows never taken to an act: SR-183, LLR-206, TC-202, TC-203 (WI-537,
  the complexity census); LLR-205, TC-201 (WI-520, the credential-class
  vocabulary); TC-199, TC-200 (WI-508); TC-204 (WI-543).

Filled by the coordinator in this row's filing commit, before any judgement:
TC-256 and TC-258 were authored with no `status` cell, which hid them from the
re-attestation brief, and they and LLR-261 and LLR-263 had no `phase`. Each now
reads `status = "Drafted"` and `phase = 6` (their parents' phase). The checker
gap is folded into WI-651.

SR-220 and SR-221 are labelled derived requirements: judge the derivation
(the spine-authoring skill's rule (c)) as well as the text. The owner may
prefer widening the need instead (SN-025's acceptance, the loop keeps its own
queue free of duplicated work; SN-012's, a builder reaches the tests for a
change); say which you would recommend and why.

Recorded, and not this row's: CMP-006 `Notes` drift, and the Drafted IF rows
(IF-176 to IF-178, IF-228 to IF-233, IF-239, IF-240, IF-242), which follow their
own route.

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN (the parent
SR, the sibling LLRs, the test cases) and either APPROVE (move the row's
`Status` to `Approved`) or RETURN with findings, drafting the follow-up in a
`## Dispositions` section of THIS spec. The approval act is ONE snapshot shared
with WI-680: `intake.py snapshot --reattests <WI-680's blessed rows> --approves
"<registry>=WI-681;..."`, naming only the registries holding an approved row.

## Done-when

- A verdict is committed under `docs/reviews/` at the path the brief names,
  with one `APPROVE` or `RETURN` line for each row in scope and exactly one
  `OUTCOME: APPROVE|RETURN rows=32` line, in a commit carrying this row's `WI:`
  trailer.
- Each approved row's `Status` moves from `Drafted` to `Approved` with no other
  registry cell changed, in the one act shared with WI-680.
- Each returned row keeps every cell byte-exact, and this spec's
  `## Dispositions` section drafts its follow-up.
