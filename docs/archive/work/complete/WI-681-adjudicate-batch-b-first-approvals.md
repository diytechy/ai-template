+++
id = "WI-681"
title = "adjudicate: SR-183, SR-184, SR-185, SR-186, SR-220, SR-221, LLR-205, LLR-206, LLR-210, LLR-259, LLR-260, LLR-261, LLR-262, LLR-263, TC-199, TC-200, TC-201, TC-202, TC-203, TC-204, TC-208, TC-209, TC-210, TC-211, TC-252, TC-253, TC-254, TC-255, TC-256, TC-257, TC-258, TC-259 - spine rows authored Drafted and never approved; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
sr_refs = ["SR-017", "SR-139", "SR-148", "SR-154", "SR-156", "SR-157", "SR-163", "SR-176", "SR-183", "SR-184", "SR-185", "SR-186", "SR-216", "SR-220", "SR-221"]
needs = ["WI-582", "WI-672", "WI-657", "WI-638", "WI-621"]
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["SR-183", "SR-184", "SR-185", "SR-186", "SR-220", "SR-221", "LLR-205", "LLR-206", "LLR-210", "LLR-259", "LLR-260", "LLR-261", "LLR-262", "LLR-263", "TC-199", "TC-200", "TC-201", "TC-202", "TC-203", "TC-204", "TC-208", "TC-209", "TC-210", "TC-211", "TC-252", "TC-253", "TC-254", "TC-255", "TC-256", "TC-257", "TC-258", "TC-259"]
priority = 2
+++

## Deliverable

Ruled by an independent adjudicator session (Fable) from the kit's
first-approval brief (every chain rendered in full), against the record at
1ea526ac, in the coordinator's spine-acts batch B:

    OUTCOME: RETURN rows=32

25 APPROVED and flipped in ONE act shared with WI-680 (acts.toml seq 4):
SR-183, SR-184, SR-185, SR-186, SR-221; LLR-210, LLR-259, LLR-260,
LLR-261, LLR-263; TC-199, TC-200, TC-202, TC-208, TC-209, TC-210, TC-211,
TC-252, TC-253, TC-254, TC-255, TC-256, TC-257, TC-258, TC-259.

7 RETURNED byte-exact. LLR-205 and LLR-206 have rationale sentences stating
their own status and signing authority, and history. TC-201 and TC-203 have
changelog prose in their method (wave-5 ruling 3). TC-204 is Smoke over a
slow-module pointer. SR-220 carries two `shall`s. LLR-262 has an open
"such as" list. SR-220's and LLR-262's form findings fire under `trace.py
--strict` only on an Approved row, and the adjudicator caught them by driving
the flipped tree before the act. The verdict is
`docs/reviews/wi-681-adjudicate-batch-b-first-approvals/001-ADJUDICATE-1ea526a.md`.

The `## Dispositions` draft below was NOT minted. Under the owner's
consolidate-before-filing direction, SR-220's fix is folded into WI-679,
which realises SR-220. The other six rows' fixes are folded into WI-616, the
open spine-text sweep whose rewrites route to a spine-acts batch, together
with the adjudicator's non-blocking findings on that surface.

SR-220 and SR-221 are labelled derived requirements. The adjudicator's advice
for the owner: widen SN-025's acceptance to state SR-220's obligation ("the
loop keeps its own queue free of duplicated work"), and keep SR-221 derived
rather than widening SN-012.

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

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-681-adjudicate-batch-b-first-approvals/001-ADJUDICATE-1ea526a.md`,
governing line `OUTCOME: RETURN rows=32`: 25 rows approved and flipped in
the act shared with WI-680 (d7558774), seven returned with every cell
byte-exact (LLR-205, LLR-206, TC-201, TC-203, TC-204, SR-220, LLR-262). One
draft covers the seven, since each fix is a sentence, a phrase or a cell and
they share a surface (the spine) and a next step (one first-approval
adjudication). The coordinator folds it into WI-616 rather than minting it
(wave-5 ruling 2).

```toml
title = "LLR-205/LLR-206/TC-201/TC-203/TC-204/SR-220/LLR-262 return: two design rows and two test methods carry changelog and status prose, one Smoke case cites a slow module, one requirement carries two shalls and one design detail an open such-as list"
workstream = "process"
safety_class = "spine"
buildtier = "quick"
priority = 3
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-017", "SR-176", "SR-183", "SR-163", "SR-220", "SR-154", "SR-156"]
bar = "DevStg-Tests"
```

VERDICT THIS CONTINUES: the file above. Every clause of the seven rows was
driven on the tree at 1ea526ac: `tests/test_kitlib_secret_classes.py`,
`tests/test_check_complexity.py`, `tests/test_consolidate.py`,
`tests/test_review_scope.py`, `tests/test_done_when.py` and
`tests/test_mapping_purpose.py` are green in the fast batch (391 passed,
1 skipped by design); `tests/test_check_complexity_cli.py`,
`tests/test_consolidate_close.py` and the named
`tests/test_mapping_purpose_cli.py`, `test_verdict_record.py`,
`test_agent_loop_review.py`, `test_agent_loop_critique.py`,
`test_integrate.py` and `test_intake.py` tests in the slow batch (86
passed); every code symbol the three design rows name exists in the module
each names. The returns are about what the cells CLAIM and how they are
SHAPED, not what the code does: two of them (items 4 and 5) are
requirement-form FINDINGS `trace.py` raises on an Approved row and gates
under `--strict`, driven on the flipped tree before the act.

IN SCOPE — seven rows, then a first-approval adjudication of the seven.

1. `LLR-205.rationale` and `LLR-205.detail` (wave-5 ruling 2, the whole
   fix): (a) delete the last sentence of the rationale, "Landing Drafted
   because SR-017 and SR-176 are both Approved and this row must not be read
   as amending either row's own attestation; approving it is the owner's
   act." A reason cell states what is true now, never its own status or the
   authority that will sign it (spine-authoring skill, cell hygiene); once
   the row is `Approved` under the `DevStg-Boundary` dial both halves are
   false. (b) In the same rationale, drop "a live, dated finding" and the
   dated plan citation "(docs/plans/2026-08-25-remap-alignment.md S8)":
   state the divergence as the standing reason (two consumers compiled
   their pattern sets apart and disagreed on four of five samples, never
   pinned equal) and send the citation to the log. (c) In the detail, drop
   the pre-table narration ("Before this table, the two consumers had
   compiled their pattern sets independently: driven against five samples,
   four disagreed ... missed by omission rather than by name") and keep
   what stands: the table, the two derivations by comprehension, the
   unchanged code symbols of LLR-017 and LLR-177, no exhaustiveness claim,
   and the three deliberately looser redactor thresholds with their reason.
   Nothing of the argument is lost: the durable half (the row amends
   neither parent's attestation) is already what `sr_refs` plus a Drafted
   status say structurally, and the divergence the table closed is the
   rationale's reason without its date. `module`, `code_symbol`,
   `component` and `sr_refs` stand as adjudicated.
2. `LLR-206.rationale`: delete the last sentence, "Landing Drafted because
   its parent SR-183 is itself Drafted and approving this design is the
   owner's act." Same rule, same reason; SR-183 is approved in this act, so
   the sentence's premise is also gone. Every other cell stands.
3. `TC-204.tier` reads `Smoke` while one of its eleven evidence pointers,
   `tests/test_mapping_purpose_cli.py::test_cli_mapping_purpose_gates_when_real_shipped_row_is_removed`,
   is in `tests/conftest.py` `SLOW_MODULES`, so the Method's "real-row
   end-to-end bite" does not run in the per-commit tier the cell claims
   (WI-604's TC-208 return, the same fact). Two remedies, the lane's choice:
   (a) split, the precedent WI-604 set for TC-208/TC-254: TC-204 keeps the
   ten in-process `tests/test_mapping_purpose.py` pointers at `Smoke` and
   its Method drops the end-to-end sentence, and a new `Full` case verifying
   SR-163 carries the CLI pointer with that sentence as its Method; or
   (b) re-tier TC-204 to `Full` and leave its evidence and Method as they
   are. (a) keeps the four-class checker in the commit bar; (b) is one cell.
   Under either, `Automated`, `Level`, `Expected` and `Verifies` stand.
4. `SR-220.requirement` carries two `shall`s: "shall hand that set to a
   single judgement, ... and shall enact the judgement's outcome ...". One
   row states one obligation (PROCESS.md §3). Drop the second `shall` so the
   sentence reads "... shall hand that set to a single judgement, at most
   once ..., and enact the judgement's outcome as a recorded restructuring,
   ...", or split the enactment into a row of its own under SN-025 with its
   own case. The derivation label, `Hat-Refs`, the rationale and the
   acceptance stand as adjudicated; LLR-210, TC-208 and TC-254 are approved
   in this act and need no change.
5. `LLR-262.detail` reads "a capitalised completion word such as LANDED or
   DONE"; "such as" is an open-ended clause the form rule refuses on an
   Approved row. Enumerate the closed set `kitlib/done_when.py`'s
   `_EVIDENCE_TOKEN_RE` holds (LANDED, DONE, MET, VERIFIED, SHIPPED,
   PASSED, FIXED, COVERED), or name it as that grammar's closed list. TC-257
   and TC-259 are approved in this act and need no change. The row's width
   (five modules, twenty-three symbols) is a non-blocking finding in the
   verdict; a split by carrier may ride this lane or not.

6. `TC-201.method` and `TC-203.method` (wave-5 ruling 3, returned with
   LLR-205 and LLR-206 for the same class of defect): rewrite each Method as
   a standing test contract with no changelog prose. TC-201: drop "now
   catches on both sides (was floor-catch/redactor-miss)", "stay
   floor-miss/redactor-catch" and "every pattern each module compiled
   BEFORE this table existed"; state the three arms as they stand: a
   five-sample decision table in which the PEM private-key class is caught
   by both the floor and the redactor while a Bearer token, a short GitHub
   token and a short API key are caught by the redactor alone, the three
   asymmetries `SECRET_CLASSES` declares per class; one canonical positive
   sample per declared class reaching each consumer through its
   comprehension over the table; and a frozen, independent pattern record
   compared by matching behaviour over threshold-straddling probes, so no
   class is caught less than that record catches. TC-203: drop the closing
   "Re-tiered into conftest.SLOW_MODULES because each case pays interpreter
   startup — the in-process metric is TC-202's" and state where it stands:
   the module runs at the full tier, each case paying interpreter startup;
   the in-process metric is TC-202's. `Evidence`, `Tier`, `Level`,
   `Automated`, `Expected` and `Verifies` of both cases stand as
   adjudicated; the arms are real and both modules are green.

All seven rows stay `Drafted` through this lane (an authoring lane never
approves; the merge refuses a lane that flips). Their first approval is the
next spine-acts batch's, from the first-approval brief.

NOT IN SCOPE, surfaced in the verdict's non-blocking findings: TC-201's
Full tier over a fast module (LLR-260's advisory class, never false), the
same plan-citation shape in SR-176's approved rationale (an approved row
with the defect is a reason to fix that row too, not a precedent for
approving a new one), and SR-163's undecomposed checker
(`gen_arch_map.mapping_purpose_findings`, `bootstrap.delivery_inventory`),
which LLR-203 and LLR-204 record as not theirs.
