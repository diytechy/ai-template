+++
id = "WI-616"
title = "Absolutes: extend the check to needs, SRs and LLRs, then run the OI-37 sweep with it and route the rewrites for approval (S1)"
workstream = "scripts"
specref = ""
buildtier = "strong"
priority = 3
safety_class = "ordinary"
needs = []
supersedes = "WI-617"
+++

## Deliverable

Built by one builder in three Codex Sol rounds (wave-5 arbitration rulings
11 to 18, and 23), SOUND at 3f9bd487.

- **The check.** `project-trajectory/scripts/absolute_terms.py` (new, a pure
  sibling of trace_text) scans needs, SRs and LLRs, never TCs. It is
  warn-first (never the exit code, pinned in the never-gates regression) and
  has one waiver grammar, `recorded waiver:`. Its tokenization and
  suppression predicate are documented where the check lives: clauses end at
  a semicolon, colon, parenthesis or sentence stop, and a comma cuts a clause
  into segments. Tests cover a closed-domain absolute (suppressed), an
  open-world one (warned) and a waived one. The spine-authoring skill gains
  the closed-domain question (§2(d2)), kit master and this repo's copy
  byte-identical. Live console: 278 absolute-term advisories (SN 30, SR 98,
  LLR 150), so precision on the requirement tier is low.
- **The sweep** is recorded in `docs/plans/2026-09-28-absolutes-sweep.md`.
  Of 48 need absolutes: 33 closed, 4 not a promise over a domain, 3 bounded
  by rewrite (SN-003, SN-008, SN-009), 3 mechanisms moved down a tier
  (SN-025; SR-148 carries them), 5 premises. Of 166 requirement absolutes:
  160 closed, 4 not a promise, 2 premises. No SR cell needed bounding. The
  premises are listed for C2 (WI-655), not written into it.
- **Amended in place, status left Approved:** SN-003, SN-008, SN-009 and
  SN-025 (needs, for the owner's brief); LLR-203 (SR-163's mechanisms are now
  owned by LLR-275 and LLR-276); LLR-233 (a registry row id is a legal
  declared input).
- **Batch B's returns**, re-authored and still Drafted: LLR-205, LLR-206,
  LLR-262, TC-201, TC-203 and TC-204 (split: the CLI bite moves to a new Full
  TC-274).
- **Ride-alongs.** SR-163's checker has design rows (LLR-275, LLR-276). The
  SR-184 Critique-advisory false positive is fixed: an Inspection row is
  exempt only when its requirement's subject, the text before `shall`, names
  a Critique record. New Drafted rows: LLR-274 to LLR-276, TC-273 to TC-276,
  IF-252.

Not this row's, recorded for others. PROCESS.md §4 still states the
absolutes rule for acceptance criteria only; that is folded into WI-615.
Needs are not in the drift comparison until WI-651 lands, so the four SN
amendments surface on the owner's brief then.

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-617 (Run the OI-37 absolutes sweep over the needs, then the SRs, and route the rewrites for approval (S1)). The sweep's input is the check's output; the 2026-09-26 handoff already sequenced them check-then-sweep. One lane, check first. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

The sweep's rewrites are Drafted amendments: needs go to the owner's brief, SRs to the spine-acts batch. Open-world absolutes that are really assumptions are listed for C2 (WI-655), not written into it.

Ruled by the owner 2026-09-23 (sister plan S1, §1.1).

Today `trace_text.ac_advisories` (`:269-289`) scans only SR acceptance cells,
its term list (`:146-156`) holds only comparatives, and it only warns, while 23
of 27 needs and 66 of 79 SRs carry an absolute. The ruled matrix: needs scan
`need` and `acceptance`, waiver in `why`; SRs scan `requirement` and
`acceptance_criteria`, waiver in `rationale`; LLRs scan `detail`, waiver in
`rationale`; TCs are not scanned. The waiver reuses `recorded waiver:
<reason>`. The suppression predicate is defined before shipping: an absolute is
satisfied when it names its domain from a closed list (a registry, an id space,
a declared set), with the tokenization documented; whether a named domain is
really closed stays a review question in the spine-authoring skill. The OI-37
sweep is its own item.

Folded 2026-09-27 (spine-acts batch B's close, the fifth coordinator session): WI-681's
first-approval adjudication RETURNED six rows on this row's surface (spine text, routed to a
spine-acts batch), and its `## Dispositions` draft was folded here instead of minted. The fixes are
stated in that draft ([`docs/archive/work/complete/WI-681-adjudicate-batch-b-first-approvals.md`](WI-681-adjudicate-batch-b-first-approvals.md),
items 1, 2, 3 and 5), its verdict (`docs/reviews/wi-681-adjudicate-batch-b-first-approvals/001-ADJUDICATE-1ea526a.md`) and wave-5 arbitration rulings 2 and 3
(`docs/reviews/2026-09-27-wave5/ARBITRATION.md`). LLR-205's rationale ends in a sentence stating its
own status and the authority that will sign it, calls itself "a live, dated finding" and cites a dated
plan, and its detail narrates the state before the table: rewrite both to the standing divergence and
design reason, with no dates, plan provenance or status. LLR-206's rationale ends in the same status
sentence, to be deleted. TC-201's method narrates what "now" catches against what "was" and a record
"BEFORE this table existed", and TC-203's opens "Re-tiered into": rewrite both as standing test
contracts. TC-204 reads `Smoke` while one of its eleven pointers is in a `SLOW_MODULES` module (split
as WI-604 split TC-208, or re-tier to `Full`). LLR-262's detail leaves its completion-word list open
with "such as", to be closed to `kitlib/done_when.py`'s set (a split by carrier may ride it). The rows
are Drafted, so these are authoring edits, not amendments; their first approval joins the next batch.
The adjudicator's non-blocking findings on the same surface ride along: no SR-198 or LLR-233 cell says
a registry id is a legal declared input, though TC-036, TC-055 and TC-209 to TC-211 declare them;
SR-163's checker (`gen_arch_map.mapping_purpose_findings`, `bootstrap.delivery_inventory`) has no
design row; and trace.py's Critique-instrument advisory fires on SR-184, whose subject is Critique
records while its method is Inspection (a lexical false positive, the same kind of lexical check this
row extends).

## Done-when

- The check scans the matrix's cells, warn-first, and never TCs.
- A waiver uses `recorded waiver:` in the tier's reason cell; there is no second
  grammar.
- The suppression predicate and tokenization are documented where the check
  lives, with tests for a closed-domain absolute (suppressed), an open-world
  one (warned) and a waived one.
- The spine-authoring skill carries the closed-domain question, kit master and
  this repo's copy in sync.
- LLR-205, LLR-206, TC-201, TC-203, TC-204 and LLR-262 carry the fixes above, stay Drafted, and are listed for the next spine-acts batch's first approval; the registry-id input rule is stated in the row that owns declared inputs (an amendment, for that batch); SR-163's checker has a Drafted design row; and the SR-184 advisory no longer fires on a row whose method is Inspection, with a test.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-617 (Done-when, verbatim)

- Every absolute the check reports in a need is classified with a one-line
  reason, and then every one in an SR.
- Rewrites land as amendments for the approval route (needs to the owner's
  brief, SRs to the adjudicator); none is approved in the lane.
- Open-world absolutes that are really assumptions are listed for the
  assumption tier's C2, not written into it.
