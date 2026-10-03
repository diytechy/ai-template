# Arbitration — wave 8

## 1. SR-215's re-attested rationale (act seq 23), 2026-10-03

**Dispute.** The adjudicator blessed SR-215's amended `rationale`. It noted that the
cell omits that a release or stage-gate trigger also makes a case due, and found
"nothing it says is false". Codex Luna's cross-review ruled that re-attestation
"not earned as written" (MAJOR): the sentence "a judgement can stand … until a
qualifying change meets the floor or its result expires" names an incomplete set
of ends.

**Arbiter:** an independent Claude Opus 5.5 that directed none of the work.

**Ruling: B — the re-attestation is not earned.** A `release` or `stage-gate`
trigger makes a case due at the matching checkpoint once the floor is met, with
no input change (`observation_cadence.py:141`, returning `checkpoint == trigger
and since != self.revision`). `rejudge._judge` then files it as a trigger, even
when the result has not expired. So the rationale is wrong for two of the four
trigger kinds:

- "a declared trigger narrows which changes make it due" is false for them;
- the list of ends leaves out the matching checkpoint.

The cell was rewritten precisely to stop overclaiming a bound, so "nothing it says
is false" is not the bar.

**Consequence.** The coordinator retook act seq 23 without SR-215 in `--reattests`.
`1345a7c8` was discarded before landing and is kept reachable in `archive/lanes`.
The retaken act is `b74f6a81`. WI-776's drafted successor carries this exact
replacement for the rationale's sentence:

> The closed-work floor and the declared trigger are cost limits the owner
> directed (the PERFORMANCE lens): no change or checkpoint makes an accepted
> judgement due again within the configured number of closed work items of its
> latest record, and a declared trigger replaces input changes with the change or
> checkpoint it names, so a judgement can stand on changes it never judged until a
> qualifying change or checkpoint meets the floor or its result expires.
