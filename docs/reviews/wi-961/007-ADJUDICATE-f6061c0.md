# WI-961 checkpoint sitting at f6061c0

## first-approval

Twenty-one lane-added rows await a first approval: SR-244, LLR-347 to LLR-356, and TC-386 to TC-395. I read them at f6061c086 against:
- SN-026, SR-222, and the spec's Trust section and Done-when;
- the lane's decisions (D-002's probes settle the three unverified facts, and D-003 records the bounds);
- the arms map, and the code in `usage_ingest.py` and `session_adapters.py`;
- the tests, and interface rows IF-305 to IF-307.

Checks I ran:
- `hats.py record docs/plans/WI-961/plan.perspectives.toml --check --strict` reports no findings. PERFORMANCE produced SR-244, which matches its `Hat-Refs`, and every other applicable hat carries a no-finding.
- `trace.py --strict` and `check_trajectory.py --strict` exit 0. The only SR-244 advisories (no Form, unclassified) are ones nearly every SR in the registry carries.
- No log in this lane's records, trunk's records or the primary spool has an unterminated header, so LLR-351's unreadable-record refusal blocks nothing on this box today.

Nineteen rows are ready. Two go back together, LLR-355 and TC-389, for one finding: what the command's recorded, unchanged and open lines must identify is left to an unnamed definition, and no test pins it.

- [APPROVE] SR-244 -> the obligation: record once each transcript-bearing session that coordination completion ingests, every nested agent included, with its identity and transcript-derived usage. Record no already-recorded message, duplicate no service record, give the record no gate authority, include no transcript text, refuse an unknown source shape, and direct completion to ingest the current session and a named prior-session tail -> what its chain shows:
  - It is honestly labelled DERIVED under SN-026, through PERFORMANCE: the cost reading is incomplete when nested work is omitted, or inflated when a read repeats. The Rationale argues that lens, cites the recorded probes (D-002) and feeds back to the need.
  - The fan-out re-stamp names ten decisions a reader can argue with, one per LLR.
  - Each acceptance clause measures an obligation the Requirement states. The guidance arm sits in the Requirement ("direct completion to ingest"). "Marks source-stated partial counts" is the fit criterion of transcript-derived usage, where the source itself says a count is incomplete, and is not a new obligation.
  - The no-gate-authority clause has no LLR. TC-393 verifies it directly, which is an honest state for a property the record's role, phase and outcome values together produce.

  -> why it is ready: one capability with its scope bounded to what completion ingests. It names no file, and its absolutes stay within the transcripts it reads.
- [APPROVE] LLR-347 -> the obligation:
  - usage only from assistant message usage, in first-appearance order, at each message id's last record;
  - finality by a stop reason, a later assistant message, or a timely finish notice for a sub-agent, never for the session's own transcript;
  - only the last message may stay open, named, uncounted and uncrossed;
  - an unstopped final message counted as partial, and reasoning empty unless every message reports it;
  - the sum, the last non-synthetic model, and the cli and provider.

  -> what its chain shows: it matches `transcript_usage` and the finality code, and TC-386, TC-387, TC-388 and TC-389 hold each arm -> why it is ready: a closed, refactor-proof contract with no `shall` and no symbol in its text. The arms map's note, that no fixture isolates first-appearance order, is test depth rather than a text defect.
- [APPROVE] LLR-348 -> the obligation: one invocation per session or sub-agent transcript, keeping its identities, depth, agent type, model and timestamps, under a deterministic 32-hex id from the session and agent identities, with COORDINATOR or SUBAGENT as role and phase -> what its chain shows: the code derives the id from a fixed namespace, and TC-386 and TC-387 hold each clause -> why it is ready: one decision (identity), and observable.
- [APPROVE] LLR-349 -> the obligation: a contribution's count, cursor, immutable key from its invocation and its first and last ids, verbatim endpoint timestamps, and a name stamp that rises one second past any existing same-invocation stamp -> what its chain shows: `contribution_row` and `name_stamp` match, and TC-389 states the clause -> why it is ready: one decision (the contribution's shape and ordering).
- [APPROVE] LLR-350 -> the obligation: read same-invocation logs by name from the spool, the root and every worktree, de-duplicated. Record only final messages after the furthest cursor, report unchanged when there are none, and refuse the invocation, naming the log, on an unreadable or unterminated header, a missing cursor or key, or an absent cursor -> what its chain shows: this is the spec's Trust ruling, "the command refuses, rather than re-count or skip", and it matches `prior_contributions` and `new_messages`. f6061c0 brings TC-389 into line with the naming arm -> why it is ready: closed and fail-closed. Sitting 002 already ruled the torn-write window out of the promise.
- [APPROVE] LLR-351 -> the obligation: a non-transcript record of the session skips its main transcript and names the skip. Its sub-agents are skipped only when the declared result-coverage constant says so. The session's own contributions are not service records. An unreadable governing record refuses what the decision governs -> what its chain shows: D-002's probe B sets the constant false, and the code treats every unreadable non-own log as possibly this session's service record, as plan decision 6 rules. TC-390 and TC-389 hold each arm -> why it is ready: one decision (no double count), stated as observable outcomes. D-003's background-agent under-count is a recorded bound, not a defect of this row.
- [APPROVE] LLR-352 -> the obligation: only declared record types and the required typed fields are accepted, each bound to its session and transcript. Every positive non-boolean depth is accepted. An unresolved parent is kept and named. Any one malformed or missing record, meta, pairing or entry refuses its transcript, naming the file and field, and leaves the others recordable -> what its chain shows: the spec's S3 closed shape; TC-391 holds each arm through the parametrized shapes -> why it is ready: a closed domain, fail-closed per transcript.
- [APPROVE] LLR-353 -> the obligation: the ambient home from the environment or its default, never an account home (LLR-336's bound). An explicit session takes precedence over the ambient one, and the command refuses with exit 2 when neither exists. Two matching locations are refused, naming both. An absent main transcript is named, and its sub-agents are still read -> what its chain shows: f6061c0's precedence sentence matches `main`, and TC-394 and TC-391 now state every arm -> why it is ready: one decision (what is read).
- [APPROVE] LLR-354 -> the obligation: the contribution's enumerated header fields, a fixed body of counts, ids and timestamps, never transcript text or raw usage, and empty fields left empty -> what its chain shows: `contribution_row` and `summary` match. TC-387, TC-392 and TC-393 hold it, and the planted-text test checks the whole log -> why it is ready: one decision (the record's content), and observable.
- [RETURN] LLR-355 -> the obligation: the command's arguments, its per-invocation outcome kinds "with the defined identifying details", and its exit codes 0, 1 and 2 -> what its chain shows: the exit-code arms are exact and held. The outcome arm defers to a definition the row never names. IF-306 holds it ("role, agent type, agent id, and declared outcome details"), but this row does not cite IF-306 or state the details, so a reader cannot restate from the row what a recorded, unchanged or open line must identify. Reading downward, that arm is held only on refused and parent-unresolved lines; no test asserts the identifying prefix on recorded, unchanged or open lines -> why it is not ready: an outcome left to an unnamed definer is an open obligation, and the gap is both in the text and in the evidence beneath it. State the identifying details, or cite IF-306 by id, and pin them with TC-389 (below).
- [APPROVE] LLR-356 -> the obligation: completion ingests its current session before writing its handoff; each handoff names its own session; a replaced handoff's named session is ingested again; and that later read records only the newly final range -> what its chain shows: the shipped `coordinator-cycle` §6 and §7 carry exactly this, in all three copies. TC-395 reads the guidance and TC-389 holds the tail arm -> why it is ready: it names only the shipped skill as its trace home, and it is one decision (when ingest runs).
- [APPROVE] TC-386 -> the obligation: identities, depth, parent, model, timestamps and deterministic distinct invocation ids over a nested fixture, plus the synthetic-model case -> why it is ready: an observable Expected, and three existing cases.
- [APPROVE] TC-387 -> the obligation: the once-per-message sum in first-appearance order, the reasoning rule, the written vocabulary, partial state, empty fields and raw usage, and the role values -> why it is ready: each clause matches LLR-347, LLR-348 and LLR-354, with five existing cases.
- [APPROVE] TC-388 -> the obligation: open, later-message, timely or stale notice, and session-notice finality, each counted once and marked partial where unstopped -> why it is ready: it matches LLR-347's finality clauses arm for arm, with seven existing cases.
- [RETURN] TC-389 -> the obligation: contribution shape and ordering, exactly-once over the spool, the root and other worktrees, the header and cursor refusals naming the log, the own-contribution rule, outcomes that "identify each invocation", exit zero, and the later read of the prior range -> what its chain shows: thirteen existing cases hold every clause but one. "Recorded, unchanged, and open outcomes identify each invocation" is claimed by Expected, and none of its evidence asserts it. The cases count recorded and unchanged lines, and match an open message's id, but never check the role, agent type and agent id on those lines -> why it is not ready: Expected claims a clause its Evidence does not hold, and LLR-355's rework moves that clause. It goes back with LLR-355.
- [APPROVE] TC-390 -> the obligation: the main-transcript skip under both coverage states, and the refusal by an unreadable governing record -> why it is ready: two existing parametrized cases hold LLR-351's arms, and its LLR-355 citation stands on the skipped and refused outcomes.
- [APPROVE] TC-391 -> the obligation: unknown or missing shapes refused with exit 1 while others stay recordable, nesting and unresolved parents observable, and two locations refused naming both -> why it is ready: f6061c0 restores the two-locations clause, and eight existing cases hold it.
- [APPROVE] TC-392 -> the obligation: a fixed summary body with no transcript text or raw usage, with text planted in every supported location -> why it is ready: an observable negative condition, two existing cases.
- [APPROVE] TC-393 -> the obligation: an ingested log in a lane is no round, build, draw or resume carrier -> what its chain shows: the case drives `logged_rounds`, `last_build_family`, `phase_draw_ordinal` and `read_carrier` beside a real AUTHOR log -> why it is ready: it verifies SR-244's no-gate-authority clause directly, which is honest where no LLR decomposes it, and Full is honest for a git fixture.
- [APPROVE] TC-394 -> the obligation: the home selection, explicit-over-ambient precedence, exit 2, absent-main naming with sub-agents recorded, and absence or a refused commit exiting 1 -> why it is ready: each clause matches LLR-353 and LLR-355, with six existing cases, and it is tiered Full for its git case.
- [APPROVE] TC-395 -> the obligation: the synchronized guidance ingests the current session before each handoff, names its own session and ingests the replaced handoff's session -> why it is ready: a text pin with two existing cases, Smoke being honest for it.

OUTCOME: RETURN rows=21

## Returns answered in the lane

```toml
title = "WI-961 spine rework: LLR-355's identifying details on each outcome line, with TC-389's evidence for them; re-sit both"
workstream = "process"
sr_refs = ["SR-244"]
needs = ["WI-961"]
safety_class = "ordinary"
buildtier = "quick"
```

This is spine text, plus one pinned test.
1. **LLR-355:** replace "with the defined identifying details" with the details themselves (each line names the invocation's role, agent type and agent id), or cite IF-306 by id. Either way, the row should state what a builder must emit.
2. **TC-389:** add, or extend, a case that asserts the role, agent type and agent id on recorded, unchanged and open lines, and list it in Evidence, so the clause "Recorded, unchanged, and open outcomes identify each invocation" is held by its evidence.

Then re-sit LLR-355 and TC-389 for first approval. The nineteen rows approved here keep their rulings, because none of these changes touches their text.

SITTING: JUDGED kinds=first-approval
