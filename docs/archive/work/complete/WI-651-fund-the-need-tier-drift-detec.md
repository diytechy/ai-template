+++
id = "WI-651"
title = "Snapshot and carrier: the need and stakeholder tiers in the drift comparison, each registry's own anchor copy on the owner's surfaces, an amendment act held to its scope, and the needs carrier chosen from the file"
workstream = "scripts"
specref = ""
sr_refs = ["SR-178"]
needs = ["WI-633", "WI-638", "WI-646", "WI-660"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
supersedes = "WI-666;WI-671"
+++

## Deliverable

Built by one builder over five commits and four Codex Sol rounds (wave-5
arbitration rulings 17, 19 to 22, 24 and 25), SOUND at f88e92e6.

- **WI-671, the needs carrier.** Every caller of `needs_from_text` passes
  the carrier. An unparseable `.toml` needs file refuses by name.
  `spine_carrier.load_need_tier` is the one need-tier loader for both need
  carriers, Markdown included.
- **WI-666, each registry's own copy, and the re-attest scope.** The owner's
  brief and the open-items view name, per registry, the commit that last
  wrote its copy. At merge, `acceptance_record.reattest_scope_refusal` refuses
  by name a re-attested row outside the claimed amendment rows'
  `Adjudicates`. A batch-B-shaped mixed act (one row approved, another
  re-attested, each claimed by its own row) merges.
- **WI-651's own scope: the need tier is funded (OI-91 (a)).** The needs
  file's needs and stakeholders are in `SNAPSHOT_TIERS`. A drifted approved
  need or stakeholder is shown with its cells before and after in the
  brief's owner section, never in the adjudicator block. An act copying the
  needs registry is refused until `--reattests SN-###` (or `STK-##`) names it,
  and the act ledger records need and stakeholder approvals.
  `unanchored_findings` covers the need tiers.
- **The fold: a missing cell is an integrity finding.**
  `kitlib.spine.missing_cell_findings` reports a spine row with no `status`
  (SN, SR, LLR, TC) or no `phase` once phased (SR, LLR, TC), naming the row
  and cell, and the approval brief lists a status-less row. The tests
  would have caught TC-256 and TC-258 as they stood before 1ea526ac.
- **Amended in place, status left Approved:** SR-178 (requirement,
  rationale, acceptance: needs no longer "carry no status cell"), LLR-245,
  TC-240, LLR-173, TC-167 and LLR-158. **New Drafted rows:** LLR-271 to
  LLR-273, LLR-277, LLR-278, TC-269 to TC-272 and TC-278. IF-112 and IF-126
  are cited now and pruned from `docs/if-tc-coverage-allow`, with its seed
  pin.

The whole-ledger arm of `refresh_refusal`, where an act that copies nothing
is still refused over drift, pre-dates this row and is deliberate under
LLR-245. It now also sees the need tiers (ruling 25). For the owner: with
this landed, WI-616's amendments to SN-003, SN-008, SN-009 and SN-025
surface on your brief, and any act copying the needs registry is refused
until you re-attest them.

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-666 (Name each registry's own anchor copy on the owner's surfaces, and hold an amendment act to its scope at merge), WI-671 (Choose the needs carrier from the file in needs_from_text too, failing closed on an unparseable TOML needs file). All three change how the approval snapshot and its readers see the registries (`baseline_snapshot`, `spine_carrier`, the owner's brief): WI-651 adds tiers to the comparison, WI-666 names each registry's copy and holds an amendment act to its scope, and WI-671 fixes the needs readers the snapshot's need tier will rely on. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

Order: WI-671's carrier fix first (the need tier this row adds reads needs through it), then WI-666, then this row's own scope. OI-91's sequencing after the assumption build still holds, so this row waits on WI-638.

OI-91 ruled 2026-09-26: fund the detector. Approved SR-178 reports a recorded artifact whose text moved from its acceptance copy, "stakeholder needs included"; `baseline_snapshot.SNAPSHOT_TIERS` excludes the need tier, and the re-attestation brief (`trace.py --approve modified`) renders no need section, so OI-85 and OI-86 were each found by hand. OI-85's ruling deferred exactly this pass; the parked note is in `baseline_snapshot.py`'s approval predicate docstring.

IN SCOPE: add the need tier to the snapshot comparison (row-level refusal then covers it too, spine map D18), render a need section in the re-attestation brief with the word-level diff the other tiers get, and route a drifted approved need through the same `intake.py snapshot --reattests` re-anchor. The owner's note from OI-86 applies: a need whose meaning did not change is re-anchored through the amendment adjudication, not re-signed by the owner. Sequenced after the assumption tier's build (OI-91's recommendation).

Extended 2026-09-27 (arbitration ruling 15(i) of `docs/reviews/2026-09-26-wave3/ARBITRATION.md`): the stakeholder tier (`STK-ID` in the needs file) is absent from `SNAPSHOT_TIERS` too, so the C1 sitting's approval of STK-01..STK-04 is recorded only in the snapshot stamp's ref text and not in `docs/archive/last_approved/acts.toml`'s row list (IF-220). Add the stakeholder tier with the need tier, with a regression showing an approved STK row recorded by the act ledger.

Folded 2026-09-27 (the fifth coordinator session, batch B's filing): a spine row with NO `status` cell is invisible to the snapshot's readers. WI-657 authored TC-256 and WI-672 authored TC-258 with neither `status` nor `phase` (and LLR-261 and LLR-263 with no `phase`); `trace.py --strict-integrity` reported 0 integrity findings, and `trace.py --approve modified` rendered neither case, so the two rows owed a first approval no brief showed. The coordinator filled the cells by hand in the batch-B filing commit. What is left is the checker: TC-003 says an empty field is flagged, and an absent key is not.

## Done-when

- A drifted approved need is reported by the snapshot comparison and appears in `trace.py --approve modified`'s brief with its diff; a test drives both on a scaffold.
- `intake.py snapshot` refuses an unnamed drifted need as it does the other tiers, and `--reattests SN-###` re-anchors it.
- A spine row missing its `status` cell, or its `phase` cell once the spine is phased, is an integrity finding naming the row and the cell, and `trace.py --approve modified` cannot silently omit it; a test drives both on a scaffold.
- The commit bar passes.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-666 (Done-when, verbatim)

- The owner's brief and the open-items view name, per registry, the commit
  that last wrote its copy.
- An amendment act re-attesting a row outside its row's `Adjudicates` scope is
  refused at merge, by name.
- The commit bar passes.

### From WI-671 (Done-when, verbatim)

- No caller of `needs_from_text` leaves the carrier to a text guess, and an
  unparseable `.toml` needs file refuses naming the file.
- The tests above were red first and pass; the commit bar passes.
