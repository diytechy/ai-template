# WI-835 — amendment adjudication at a10adc3 (meaning vs clarity)

Judged against the anchor in `docs/archive/last_approved` (copied 2026-10-05,
a8458c22), on the cells shown only.

- [MEANING] SR-227 Requirement + AcceptanceCriteria -> the loop's own retained-class adjudication resumes/mints/waits/drains/retires one session per route, writes the store whole by one writer, and keeps keep-warm to one bounded turn; at dial 0 nothing is minted, resumed, written or pinged -> the same, now for adjudications started by the coordinator as well as the loop, with both routes composing one retention request, a second coordinator-route call resuming its first call's session, a dedicated-home sign-in reading (signed in / missing / unknown, no home created, no model call) that refuses either retained route before any launch, home creation, lease or store write and names the setup action, no sign-in probe at dial 0, and a coordinator adjudication running only from a claimed lane worktree and reading success only from a verdict written by a call that finished within its deadline -> not the same: a correct implementation of the old text (loop-only retention, no sign-in check) fails the new one on the coordinator route, the refusal, and the lane/verdict conditions; the Title and Rationale cells follow that change and add no further obligation.
- [MEANING] LLR-270 Detail -> plan_keep, for a covered call, goes straight to keep_for (lease, then dedicated home created under the store) -> plan_keep first asks LLR-305's sign-in refusal, so a refused call takes no lease and creates no home -> not the same: a new precondition and a new ordering sit in front of the lease and the home creation, and a build that leases or creates the home before any sign-in check (correct under the old text) fails the new one.
- [MEANING] TC-266 Method + Expected -> both the shipped template and this repo's policy file declare context_reset_pct = 0, and the retention plan is None in a bare repository AND in this one -> the template declares 0, this repo declares 55, both carry the same keys, and the None plan is asserted only in a bare repository -> not the same: the acceptance condition changed (this repo is now asserted to be on at 55, and the "inert in this repository" check is dropped), so a test correct under the old text fails the new one.

Re-attestation, on the RELEASED rung: I would bless LLR-270 and TC-266 as
amended. LLR-270's added ordering follows from the parent's new refusal and
its child LLR-305. TC-266's 55 matches the owner's recorded dial in
`docs/process.toml` (WI-835, owner ruling (b), 2026-10-05).

I would NOT bless SR-227 as amended. Its AcceptanceCriteria now carry two
conditions the Requirement cell never obliges: "a coordinator adjudication
runs only from a claimed lane worktree" and "reads success only from a
verdict written by a call that completed within its deadline". The
Requirement is also scoped "where the retention dial is above zero", and
these two conditions concern coordinator adjudication whatever the dial
reads. LLR-305's own rationale grounds them in telemetry landing on trunk
and in stale evidence, not in retention. A reader deriving only from the
Requirement would not build them, and an acceptance cell that outruns its
requirement is the silent widening the approval exists to catch. The
corrective work is drafted under `## Dispositions` in the WI-835 spec.

VERDICT: MEANING rows=3
