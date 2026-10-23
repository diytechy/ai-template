# WI-961 checkpoint sitting at ed7a157

## first-approval

This re-sits the whole set at ed7a157b2. Sitting 007 approved nineteen of these rows and returned LLR-355 and TC-389. Since 007's commit (932d2f055), only two registry cells have changed: LLR-355's Detail and TC-389's Evidence. One test was added for TC-389. No code changed.

Checks I ran at this tip:
- `trace.py --strict` exits 0.
- The perspective record still passes `hats.py record ... --check --strict`.
- The new test and the shape-refusal test both pass.

Twenty rows are ready. LLR-355 goes back once more, for a claim its new sentence makes that the code does not keep.

- [APPROVE] SR-244 -> the obligation: record once each transcript-bearing session completion ingests, nested agents included, with identity and transcript usage. Record no message twice, duplicate no service record, grant no gate authority, include no transcript text, refuse an unknown shape, and direct completion to ingest the current session and a prior tail -> what its chain shows: unchanged since sitting 007 approved it. The derivation is recorded through PERFORMANCE and fed back to SN-026, and every acceptance clause measures a Requirement obligation -> why it is ready: on 007's reasons. LLR-355's return does not touch any clause of this row.
- [APPROVE] LLR-347 -> the obligation: usage from assistant messages, once per id at its last record, with the stated finality rules, the one open last message, partial marking and the reasoning rule -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-348 -> the obligation: one invocation per transcript, with its identities and a deterministic 32-hex id, role and phase COORDINATOR or SUBAGENT -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-349 -> the obligation: the contribution's count, cursor, immutable key, endpoint timestamps and rising name stamp -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-350 -> the obligation: exactly-once over same-invocation logs in every record directory, with refusals that name the log -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-351 -> the obligation: a service-recorded session's main transcript is skipped, its sub-agents follow the declared coverage constant, own contributions are not service records, and an unreadable governing record refuses -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-352 -> the obligation: the closed transcript shape, any positive non-boolean depth, unresolved parents named, and a per-transcript refusal naming the file and field -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-353 -> the obligation: the ambient home and never an account home, an explicit session before the ambient one, exit 2 with neither, two locations refused, and an absent main transcript named with its sub-agents still read -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-354 -> the obligation: the contribution's enumerated fields, and a fixed summary body without transcript text or raw usage -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [RETURN] LLR-355 -> the obligation, at this tip: the command takes an optional session and root. It emits recorded, unchanged, open, skipped, refused, absent or unresolved-parent outcomes, "each line naming the invocation's role, agent type and agent id, in the stdout form IF-306 declares", and exits 0, 1 or 2 -> what its chain shows: sitting 007's finding is answered for the lines it named. The row now states the identifying details and cites IF-306, and the new test pins them on recorded, unchanged and open lines. But the sentence now covers every listed outcome, and one of them does not keep it. A transcript the reader refuses for its shape is printed as `refused <file>: <field>`, with no role, agent type or agent id. That is the command's line for reader refusals, and IF-306's own contract docstring gives it in that form. The existing shape-refusal case passes on exactly that line. A test written from this row, asserting the prefix on every line, would fail on any shape refusal. The other refusals do carry the prefix: header, cursor and governing-record refusals, and the absent line (`COORDINATOR - -:`) -> why it is not ready: approving it would bless a universal claim the code contradicts for one of its own named outcomes. My own 007 disposition suggested the over-broad phrase ("each line names the invocation's role, agent type and agent id"), and the lane followed it. The fault is in that wording, and the narrower statement below is what the code does.
- [APPROVE] LLR-356 -> the obligation: completion ingests its current session before its handoff, names its own session, re-ingests a replaced handoff's named session, and records only the newly final range -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] TC-386 -> unchanged since 007; identities, deterministic ids and the non-synthetic model, held by three existing cases -> ready on 007's reasons.
- [APPROVE] TC-387 -> unchanged since 007; the once-per-message sum, the vocabulary, partial state and role values -> ready on 007's reasons.
- [APPROVE] TC-388 -> unchanged since 007; the finality arms, each held -> ready on 007's reasons.
- [APPROVE] TC-389 -> the obligation: contribution shape and ordering, exactly-once over every record directory, refusals naming the log, the own-contribution rule, and recorded, unchanged and open outcomes identifying each invocation, exit zero and the later range -> what its chain shows: sitting 007's finding is answered. Evidence gains `test_recorded_unchanged_and_open_lines_name_each_invocations_role_type_and_id`, which runs two ingests over a nested fixture with an open message. It asserts that every line opens with its own invocation's prefix, that the session prefix appears once, that the open message sits under its own agent, and that recorded and unchanged lines carry the prefix. The case exists and passes -> why it is ready: every Expected clause is now held by a listed case. Its clause covers only recorded, unchanged and open lines, so LLR-355's remaining finding does not touch it.
- [APPROVE] TC-390 -> unchanged since 007; the skip under both coverage states, and the governing-record refusal -> ready on 007's reasons.
- [APPROVE] TC-391 -> unchanged since 007; shape refusals named by file and field with exit 1, nesting and parents observable, two locations refused -> ready on 007's reasons. Its "named" clause is the reader refusal's real form, which LLR-355's rework should match.
- [APPROVE] TC-392 -> unchanged since 007; a fixed summary body with no transcript text -> ready on 007's reasons.
- [APPROVE] TC-393 -> unchanged since 007; no round, build, draw or resume carrier, verifying SR-244 directly -> ready on 007's reasons.
- [APPROVE] TC-394 -> unchanged since 007; home, precedence, exit 2, absent main transcript and the exit-1 cases -> ready on 007's reasons.
- [APPROVE] TC-395 -> unchanged since 007; the synchronized guidance's ingest order and session naming -> ready on 007's reasons.

OUTCOME: RETURN rows=21

## Returns answered in the lane

```toml
title = "WI-961 spine rework: LLR-355's outcome-line sentence scoped to what each kind of line names; re-sit it"
workstream = "process"
sr_refs = ["SR-244"]
needs = ["WI-961"]
safety_class = "ordinary"
buildtier = "quick"
```

This is spine text only, and no code change is called for.
1. **LLR-355:** scope the identifying sentence to the lines that carry it, for example: each invocation's line names its role, agent type and agent id, while a transcript refused for its shape is named by its file and field, in the stdout form IF-306 declares. The alternative, giving shape-refusal lines the prefix too, is a code change and a test change, and is the lane's call.
2. **IF-306** carries no approval status, but its `data` cell says the same thing ("refused ... readings with role, agent type, agent id"). Align it in the same commit so the row and its interface agree.

Then re-sit LLR-355 for first approval. The twenty rows approved here keep their rulings, because none of these changes touches their text.

SITTING: JUDGED kinds=first-approval
