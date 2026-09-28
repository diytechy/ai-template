# ADJUDICATE — WI-689 — queue overlap at e26e22aa

Independent adjudication of the seven-row cluster the consolidation census
minted at e26e22aa (digests `af589a4f5319|edd7832b0dd6`, unchanged at the
time of judging): WI-615, WI-616, WI-620, WI-651, WI-655, WI-657 and WI-667.
The one question: do any of these contradict the spine they cite, overlap so
that two lanes would fight, or ask for something already answered, and if so
are they one work item wearing several ids.

Brief: the kit's consolidate brief rendered for this row
(`adjudicate_brief.compose`: the seven specs in full, the fourteen other open
rows, SR-178, SR-197, LLR-158, LLR-225, LLR-229, LLR-230 and LLR-231, the ten
mechanical pre-filter lines, and the earlier-consolidation record). Every
earlier absorption in that record is marked `(by hand)`, so no judgement
stands behind any host here and nothing below overturns one. Disclosure: I
read WI-617's archived spec under `docs/archive/work/restructured/` for how
its sweep lands, the SR registry and its shipped template for the row shape
the two spine-editing rows would both write, `trace_text.ac_advisories`,
`baseline_snapshot.SNAPSHOT_TIERS`, `census.py`, the reviewer prompt, the
spine-authoring skill, PROCESS.md and `docs/requirements/assumptions.toml` to
test each row's scope against trunk for "already answered", and wave-4
arbitration ruling 13 for WI-657's remaining scope. HEAD stayed at e26e22aa
throughout; the worktree was clean before this file was written.

Shape 1, contradiction with the spine: none. SR-178 asks for exactly the
need-tier drift report WI-651 builds; SR-197 and LLR-229 to LLR-231 admit the
assumption-evidence census WI-667 routes; LLR-158 already places the needs
file inside APPROVAL_ACT_CSVS, so WI-651 widening the comparison tiers to
needs and stakeholders lands on the side LLR-158 already declares.

Shape 3, already answered: none. On trunk the reviewer prompt still names
`docs/specs`, PROCESS.md carries neither glossary line nor the fan-out or
guard-owed rules, `AGENTS.template.md` has no partial-search bullet and no
`subagent-brief` skill ships (WI-615's parts stand); `ac_advisories` still
scans SR acceptance only (WI-616 stands); `SNAPSHOT_TIERS` is still the three
spine registries (WI-651 stands); `assumptions.toml` holds no row (WI-655
stands); `gap_census` still carries the requirement half only (WI-667
stands). WI-657's parts 1 to 3 are on trunk by its own lane under ruling 13,
which its Context records; the research write-up under `docs/plans/` is not,
so the row is in progress, not a duplicate.

Shape 2, scope overlap, judged pair by pair on intent:

- [MAJOR] WI-655 -> WI-616 -> both rows write the same approved SR rows in one sitting from two directions, and one is the other's declared input. WI-616's sweep (WI-617's quoted Done-when) rewrites `requirement` and `acceptance_criteria` on the SRs that carry an absolute (66 of 79 at filing), staged as Drafted amendments for the spine-acts batch, and its third clause says the open-world absolutes that are really assumptions are "listed for the assumption tier's C2, not written into it". WI-655 IS C2: it writes those DA rows from the needs the sweep is about to rewrite, gives every SR `da_refs` or `coincident` and re-points every SR's `boundary_refs`, in the same rows. Claimed on the same day, the second to merge rebases its amendment set over the other's across most of the SR registry and the batch adjudicates one row's text twice from two lanes; built in the wrong order, the sweep's list arrives after C2 has closed and needs a C2-bis no plan step names. Each is still its own decision: a lexical check plus a wording sweep is not the assumption tier, and merging them would make a lane too big to build or review -> add the hard edge `WI-655 needs WI-616`; nothing else changes on either row. The cost is real and stated: C2, the condition of OI-94's ruling, waits behind a strong-tier row. The sister plan's S1 (ruled 2026-09-23) already sequences the sweep's output into C2, so the edge writes down an order the rows already assume rather than inventing one.
- [MINOR] WI-615 -> WI-655 -> the shared spec of record (the assumption-tier plan §11) is two of that plan's packages, T (terminology and the doctrine sitting) and C2 (the assumption rows). One edits prose in byte-capped docs, prompts, skills and dashboard labels; the other writes registry rows. No shared artifact, no shared decision -> queue as they stand.
- [MINOR] WI-615 -> WI-657 -> the `gen_skills_index.py` hint is stale. WI-657's parts 1 to 3 landed under wave-4 ruling 13, including WI-539's PROCESS.md and PROCESS_OPTIONS.md edits and the `INDEX.csv` regeneration; what remains is WI-624's write-up under `docs/plans/`, which touches no doctrine and no script. WI-615's WI-536 part changes `gen_skills_index.py --check`; WI-657 no longer does -> queue; no edge. WI-657's Context still says "do not run the two lanes at once" about WI-539 and WI-615; that sentence describes work already merged and can be struck when the row closes.
- [MINOR] WI-616 -> WI-620 -> one commissioning plan, two sections (§1.1 absolutes, §3.1 session service), two modules (`trace_text` and the loop's launch and logging path). Nothing shared -> queue.
- [MINOR] WI-616 -> WI-651 -> both edit `trace.py`, in different functions: WI-616 the lexical Critique-instrument advisory (SR-184's false positive) beside `ac_advisories`; WI-651 the `--approve modified` brief's need section and the missing-`status`/`phase` integrity finding. WI-651's spine touch is code and tests only, and its rows would carry `status` either way. Ordinary same-file merge, not a shared decision -> queue.
- [MINOR] WI-616 -> WI-667 -> `trace.py` again, different seams: WI-667 wires `gap_census` and `intake._census_drafts` once an owner ruling re-arms the red-TC rung; WI-616 never touches the census -> queue. Separate finding on WI-667 alone: its IN SCOPE opens "once the rung's re-arming is ruled", and no `needs` target or open-item row carries that ruling, so the row is claimable while unbuildable; the coordinator should point its `needs` at the judgement item once one is filed. Not a contradiction and not an overlap, so no outcome here rests on it.
- [MINOR] WI-651 -> WI-655 -> WI-651 changes what the snapshot compares (need and stakeholder tiers) and how `needs_from_text` chooses its carrier; WI-655 writes assumption and surrogate rows and SR pointer cells. The assumption registry is outside `SNAPSHOT_TIERS` today and WI-651 does not add it. WI-651 already waits on WI-638 -> queue.
- [MINOR] WI-651 -> WI-667 -> `acceptance_record.py` and `trace.py`: WI-651's absent-key integrity finding (TC-003 flags an empty field, not a missing key) against WI-667's `_TC_NOT_RED` routing. Different constants, different decisions, and WI-667 is gated on an owner ruling besides -> queue.
- [MINOR] WI-655 -> WI-667 -> WI-655 writes the assumption rows; WI-667 decides how a red assumption-evidence TC is routed once the rung is armed. A dependency in subject, not in artifact: WI-667 reads rows through `assumption_evidence_rows` whatever WI-655 writes -> queue.
- [MINOR] WI-620 -> every other row -> the session service, its adapters and the OTel record touch no registry, no doctrine doc and no trace or census module the others edit. Its inbound edges (WI-541, WI-545) are already declared -> queue.

OUTCOME: QUEUE-WITH-EDGE needs=WI-655 absorbs=-
