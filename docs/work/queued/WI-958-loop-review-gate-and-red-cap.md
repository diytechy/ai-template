+++
id = "WI-958"
title = "The loop draws a review only on a tip attested green, and a lane whose build stays red for the declared number of rounds closes partial through the existing red arm"
workstream = "process"
sr_refs = ["SR-154", "SR-144", "SR-172"]
specref = "docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages"
buildtier = "high"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-956", "~WI-957"]
+++

## Context

Review-churn item 13, the loop's half of the gate and the red-round cap
(precondition 3, revisions 17, 18 and 20).

**The loop.** It queues a review as soon as a build is committed
(`agent_loop.py:schedule_review_round`: "accepted-on-train (locally green
and committed)"), after a narrow approve (`complete_review_round`) and on
resume (`review_owed_by_evidence`). Every review session is drawn at one
point, `st.pick_phase()` in the session body. Nothing reads a bar result.

**The cap.** "A red bar returns to the builder without a review, inside the
builder's own bound." The owner set the bound at about three red rounds
(revision 17). At the bound the lane closes partial through `handback.py`'s
existing red arm, never a new stop (revision 18; OI-70: partial is the only
stop). The setting is a build-round count, not a review setting:
`[build] red_rounds_max = 3`. The red adjudication judges behaviour and
scope only; it never waives a failing bar (Astra, revision 18).

**Why the gate and the cap are one row.** A red build still commits, so the
stall guard never trips (`note_session`: a commit resets the stall). A loop
gate without a bound would rebuild forever on a red tip, downstream too.

**Without P8**, the loop names no tests: its review bar is the commit bar
alone (`tests=none`) until P8 derives the set.

**Anchor.** SN-004 and SN-008 (approved). SR-154 (the loop obtains review
verdicts), SR-144 (the partial close and its report), SR-172 (a stall is its
own outcome; the cap gets its own too). The loop's LLR joins WI-957's derived
SR; a derived SR for the cap ("a lane whose build stays red for the declared
count closes partial") is drafted TC-first in the lane.

## Deliverables

1. **The loop attests at the event.** After a committed BUILD session the
   loop runs WI-956's producer on the lane (an empty attestation commit,
   `bar=review`). Green: the round is scheduled as today. Red: no round; the
   bar's failure tail reaches the next build session the way a round's
   findings do.
2. **The draw verifies.** At the review draw, the tip (or the commits
   beneath it whose non-record identity equals their parent's) must carry a
   verified `review` attestation. If none (a crash between build and attest,
   or a resumed round), the loop runs the producer once there; red counts as
   a red round. One choke point covers fresh, post-narrow and resumed
   rounds, and adjudication-triggered rounds (`schedule_adjudication_round`).
3. **The count, recorded at the event.** Each red result is written into
   the committed session log of the build whose tip it refused. The count is
   consecutive red rounds since the lane's last green attestation, read from
   the lane's committed logs, so a resumed run keeps it.
4. **The cap.** `[build] red_rounds_max` in `process.toml.template` and
   `docs/process.toml`, read by one reader in `kitlib/config.py`. At the cap
   the worker ends with a new exit code of its own; `dispatch.py` adds it to
   its worker outcomes and closes the lane partial through
   `handback.close_partial` with typed fields (the reason naming the count
   and the last bar summary, `split_decided_by = "adjudicator"`); the drain's
   red refresh then quarantines it as today.
5. **The coordinator's cap text** in `coordinator-cycle` SKILL §3 (both
   copies byte-identical): count each red `attest` as a red round in the
   lane's decisions record; at `[build] red_rounds_max` consecutive red
   rounds, close the lane partial (recipes §8, "Close a lane partial").
6. **Records.** The exit-code interface row and IF-037's `[build]` mention;
   one RESYNC entry (a new setting with its shipped value; the loop's new
   exit code).

## Trust

`[build] red_rounds_max` gains authority over an act (the partial close).
Written under [PROCESS.md §3, "When a guard is owed"](../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).
The attestation's Trust is WI-956's.

- **Producer:** the owner or an agent, by hand, in a reviewed commit; the
  template ships `3`.
- **Consumers:** the new reader in `kitlib/config.py`; its caller in
  `agent_loop.py`; the coordinator through the skill text.
  `tests/test_dogfood_sync.py` pins the section in both files.
- **Ruling:** absent file, table or key reads the shipped `3`. A present
  value that is not an int, is a bool, or is below 1 is refused at the
  loop's preflight, naming the line, before any session. Never read as off:
  off would be unbounded, the fail-open side. Binds to the working tree's
  `docs/process.toml` at the run's start.
- **The count's record:** a hand-edited session log is outside the promise
  (PROCESS.md §6). A log that cannot be read counts toward the cap, never
  away from it.

## Done-when

Each named test fails on the code before the change.
- **No review on red.** A stand-in build whose bar fails: the loop draws no
  review, records a red round, and dispatches a build carrying the bar's
  failure tail.
- **Review on green.** The same build with a passing bar: one attestation
  commit, then the review draw as today.
- **Resumed and post-narrow rounds** are drawn only on a verified
  attestation; a resumed round on an unattested tip runs the producer once.
- **The count survives a resume**, and a green attestation resets it.
- **The cap.** At `red_rounds_max` consecutive reds the worker exits with
  the new code, the dispatcher closes the lane partial with the typed
  fields, and the drain quarantines it. One red fewer: no close.
- **The key.** Absent reads 3; `0`, `-1`, `true`, `"3"` and `3.0` are each
  refused at preflight, naming the line, with no session started.
- The skill states the coordinator's cap citing the key; both copies
  byte-identical.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` clean; the derived rows are judged at
  the lane's sitting; the RESYNC entry anchors at the landing's parent.

## Scope answers

- **S1.** One deliverable: the loop's gate, its count and its cap are
  broken alone (see Context). Last of P1's four rows.
- **S2.** `## Trust`.
- **S3.** Closed: the key's values above; a bar result is exit 0 (green)
  or anything else (red, a bar that could not run included, its cause
  named in the close report).
- **S4.** `single`: Trust, input space, three families (`agent_loop.py`,
  `dispatch.py`, `kitlib/config.py`).
- **S5.** A new state (a red round), a new exit-code value, a new dial, a
  new input to the review draw. No component change.
- **S6.** `WI-956` (hard). `~WI-957` (the same §3 text). **Add P4 (item 15,
  one WI per lane) as a hard edge when it is filed:** it retires the train
  scope inside `schedule_review_round`, which this row gates, and both land
  before the loop is unpaused.
- **B3.** The count reads records written at each event.
- **B4.** No owner act. The loop is paused (`docs/work/pause`), so this
  lane's evidence is tests; the first live use is the owner's first run
  after the unpause.
