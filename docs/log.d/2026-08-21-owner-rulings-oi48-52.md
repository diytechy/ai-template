## 2026-08-21 — Four of the six queued briefs rule in one owner message; the floor question is answered but deliberately not yet ruled

Deferred open items: none still owed — SUPERSEDED 2026-08-22: everything
this file ever declared is ruled. It originally declared the floor
question (51 in the OI space — answered across four exchanges below, then
ruled the same day as the stage unification program) and the stale-cell
batch (53 — ruled (b)+(d) on 2026-08-22, execution rows queued); both ids
sit off the declaration line per the parser's live-state reading, and the
per-exchange record below stands as history.

The owner ruled four pending briefs in one message (2026-08-21); each row
flipped `pending -> ruled` with the ruling recorded at the top of its
recommendation cell and its executing WI queued in the same commit.

| OI | Ruling | Execution |
|---|---|---|
| OI-48 | **(d) EXEMPT A DECLARED KERNEL FROM THE SEAM RULE — generalised to a reuse provision, per the owner's own follow-through question.** The owner asked whether the same multiple-seams-into-multiple-components shape recurs for other REUSED modules, and the answer is yes — that is what a shared library IS — so the declared surface is a LIST of kernel modules with a per-entry recorded reason, never a `kitlib` hardcode: any future shared module whose consumers span components takes the same declared path, each addition a deliberate recorded act rather than a heuristic's guess. The multi-membership advisory stays live so candidates keep surfacing; the seam rule stays live for every edge NOT into a declared kernel. One owning component per (d)'s own text — the recorded closest-fit analysis points at `CMP-006` (the registry reader is the package's bulk); the execution row measures and records the tag with reasoning, and reconciles `LLR-182`'s single-tag choice with the ruled ownership. | WI-494 |
| OI-49 | **(b) RATIFY WITH A NAMED EXCEPTION LIST, as recommended.** The bulk of the LIVE cells (not the superseded 2026-08-15 list) is accepted; the exception reads are the two unargued picks (`IF-013`→SR-006, `IF-044`→SR-154), the five-row loaders-vs-decision split (IF-056/082/084 vs IF-071/085), `IF-131`'s single-constituent bundle, and the still-provisional depth bound of 2. The execution row prepares the dossier with a recommendation per read; the ratifying Status-change commit stays the owner's. | WI-495 |
| OI-50 | **(a) NO CROSSING — locked in as a RULING, no longer the standing silence.** The owner's phrasing: the system just PROVIDES that capability. Fetching a vendored upstream source is the system consuming a tool, not exchanging obligations with a party; the frame stays literally four; `IF-036`'s recorded no-tie-back reason is now an answer, not an open question. Zero cell edits owed, exactly as the row's blast radius stated. (c) stays declined for the recorded reason — the network reach must remain visible in the registry. | — (record-only) |
| OI-52 | **(a) ENFORCE LOCALLY — with a tuning mandate that reorders the recommendation.** The owner: the smoke bar should be TUNED so it passes within 60 s on EVERY dev machine (a faster box might pass in 30 s) — the point of the budget is that smoke stays quick. So the 60 s is a worst-machine ceiling, not a this-box target; the enabling work is the re-tier the brief priced as (c), and enforcement lands AFTER the tier fits again, or every honest commit on this box reds on day one. The recommendation's (b) (redefine as CI-only) is REJECTED: the bar means the seconds, locally. Budget VALUE unmoved, per both reviewers' shared constraint. | WI-496 |

**OI-51 — ANSWERED, NOT RULED.** The owner asked: once the test registries
are all `Founded` the spine is broken down and implementation begins, and
DevStg goes to implementation, which should allow these checks in parallel —
why would that require the test suite to run? The answer dissolves the
confusion: **nothing requires the suite to pass to ENTER implementation —
the defect is the inverse.** The three checks are TAGGED to run only at the
`DevStg-Impl` bar, and OI-30 D2 deliberately made that bar unreachable from
status cells alone (a Status cell must never be able to claim "the evidence
passed"; only the future harness driver, computing the bar FROM test
results, may). So during exactly the phase the owner describes — spine
Founded, implementation underway, derived bar at `DevStg-Tests` — the
selector never schedules format/lint/tests on a push or PR. The owner's
described end state ("the checks run in parallel once the breakdown is
done") IS option (a): re-tag the three to `{DevStg-Tests, DevStg-Impl}` so
they RUN from decomposition onward, while the pass/fail EVIDENCE claim
stays where D2 put it. (a) awaits the owner's word now that the mechanism
is stated; the row stays pending.

Bookkeeping in the same commit: watermark `WI` 493 → 496 via
`trace.py --bump-ids`; open-items.html, the dashboard and the status block
regenerated; `docs/status.md`'s hand prose re-pointed (the wi448/wi483
ruling-owed sentences now cite the ruling; the close-leaves-for-the-owner
sentence narrows to what is actually still open). Commit bar figures in the
close record below.

**Follow-up, same day — the second OI-51 exchange and the bar-vs-stage
census.** The owner diagnosed the OI-51 confusion as the bar vocabulary
itself and stated the general preference: behavior ties to development
STAGES ("in or above DevStg-Impl → run the checks" — the question being
"when is it relevant for me to run these checks", not "what previous step
did I pass"), never to bars or clears — then asked for a census of which
semantics the kit actually checks. Taken the same day
([plans/2026-08-21-bar-vs-stage-census.md](../plans/2026-08-21-bar-vs-stage-census.md)):
**91 sites — 55 bar/clearance, 27 current-stage, 9 mixed**, split cleanly
on a module boundary (check SELECTION is 100% bar-keyed; ratification
AUTHORITY is 100% stage-keyed already). The decision-critical fact: the
stage axis carries no OI-30 D2 ceiling, but **rung 6 is VACANT** — the
closed Status enum makes `spine_stage`'s Impl discriminator unreachable,
so a legal spine jumps `DevStg-Tests` → `DevStg-Release` (already pinned,
named-for-the-sitting, at `test_ratification_level.py:359`). The owner's
shape therefore works in its AT-OR-ABOVE form only; an equality test on
`DevStg-Impl` inherits unreachability from a second, independent cause.
Recorded on the row as option (e) with the census's FOR/AGAINST (step
tags are set MEMBERSHIP today, so at-or-above is a semantics change per
step; four behaviors genuinely need clearance semantics; the stage rides
`docs/gate` only as a comment substring one consumer regex-scrapes — the
carrier seam any re-key crosses first). The row stays PENDING — the
census is the owner's asked-for input, not the ruling.

**Second follow-up, same day — the ladder re-discrimination question and
the at-or-above deep check.** The owner proposed re-discriminating the
ladder itself (all-Founded → IN `DevStg-Impl`; `DevStg-Release` requires
all test cases PASSING) and asked for an adversarial corner-case check of
at-or-above, plus why `docs/gate`'s headline value cannot simply be the
current stage. The deep-check
([plans/2026-08-21-stage-rekey-deep-check.md](../plans/2026-08-21-stage-rekey-deep-check.md)),
driven not assumed: the re-discrimination is the OI-30 D2 harness
driver's stage-axis half and is behaviourally INERT for all 27
stage-keyed ratification sites (rungs 6/7 identical at every dial level)
— but NO test-evidence source exists today at four independent points, so
the evidence source is the real build. At-or-above is valid as an
operator with NINE real corner cases in what it would read — worst: one
Drafted row drops the raw stage ord 7 → as low as 0 with no floor and no
ex-draft analogue (C-01 reproduced on the stage axis, the WI-473 floor
unable to help), and no per-phase stage exists at all — so (e) needs a
DESIGNED effective-stage derivation, not the raw field. `docs/gate`'s
line: eight readers take it as the bar and `check.py` hard-exits on
non-bar values, so the meaning cannot silently flip; three honest carrier
options are priced in the doc. One census correction (the hyphenated-label
claim inverted: truncation to a DIFFERENT VALID RUNG, the unsafe
direction) and one incidental LIVE DEFECT found and queued
(`intake._gate_moved` reads the static header comment and has been
always-False since the derived-gate migration — one of the four
clearance-needing behaviors is not running at all; watermark `WI`
496 → 497 in this commit).

**Third follow-up, same day — the compute-vs-read schedule map.** The
owner asked when the gate is computed versus read, and whether the
readers are scheduled properly. Mapped and demonstrated
([plans/2026-08-21-gate-schedule-map.md](../plans/2026-08-21-gate-schedule-map.md)):
`docs/gate` is a COMMITTED CACHE of a pure function of the live
registries — one writer (`derive_gate.py`, production-called only by
`trunk_step.regen` on the trunk lane), freshness enforced by a `--check`
that RECOMPUTES from the live registries and byte-compares value + basis
lines at all three bars, so no green run or commit lands stale ON THE
TRUNK. Reader tally: 2 protected, 6 windowed-but-self-correcting, 1
broken (the WI-queued `_gate_moved`), 1 dead (`read_declared`, documented
as the gate's reader, called on it nowhere). Two real windows ranked
above the rest: (W-1) a CLAIMED WORK BRANCH switches the freshness step
off by design (`_TRUNK_FRESHNESS_STEPS`), which FALSIFIES
`spine_stage_of`'s written trust invariant ("either current or the step
is already red" — in that lane it cannot be red); (W-2) `agent_loop` and
`dispatch` hoist the stage ONCE PER RUN while the run's own merges
regenerate the gate beneath them (`tracked_pause` is re-read every tick;
the stage is not). De-escalation, measured: at this repo's dial 4 every
rung is human-held, so no stage value changes any decision here today —
both windows are latent, live only for adopters at dials 1–3, erring
toward MORE human involvement. The W-1 invariant mismatch (re-document
vs arm branch-lane freshness) is put to the owner in the same reply; it
is the one place a written guarantee and the mechanism disagree.

**Fourth follow-up, same day — OI-51 RULES as the stage unification
program.** The exchange chain (Impl-vs-Release measured behaviourally
empty; the four "clearance" behaviors reduced to events-over-history plus
one derivation rule; the enum inventory: 648 occurrences / 64 files, four
code definition homes held equal by pins) closed with the owner agreeing
the redesign and supplying the mechanism chain-of-thought: `docs/stage`
carrying stage + phase + an input fingerprint, one self-healing common
reader, and the phase-decrease rule with exactly the `LLReqs → Arch`
decomposition-cycle exemption. Recorded as the design record + plan
([plans/2026-08-21-stage-unification-design-record.md](../plans/2026-08-21-stage-unification-design-record.md),
[plans/2026-08-21-stage-unification-plan.md](../plans/2026-08-21-stage-unification-plan.md));
the owner answered the plan's four open questions (phase stays DERIVED
with the decrease rule as an authoring-time check — verified: `phase` is
a spine-only column, all 73 SRs carry it; both stage and phase recorded
in `docs/stage`, the consistency principle; NO interim (a) — meta repo;
branch trust confirmed on the serial-spine argument) and the plan went
v1 FINAL. **OI-51 flipped `pending → ruled`** with `ruling_ref` the plan
itself; execution row **WI-498** minted (program lane, slices 0–5;
WI-497 folds at slice 4, the deferred WI-493 at slice 5); watermark `WI`
497 → 498. The 2026-08-20 program-grind fragment's two OI-51 deferral
declarations superseded in place at the same commit.
