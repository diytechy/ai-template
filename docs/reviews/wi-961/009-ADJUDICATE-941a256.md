# WI-961 checkpoint sitting at 941a256

## first-approval

This re-sits the whole set at 941a256e7. Sitting 008 approved twenty of these rows and returned LLR-355. Since 008's commit (afb72e490), these are the only changes:
- LLR-355's Detail;
- IF-306's `data` cell;
- the IF-306 contract text in the command's module docstring (no executable line changed);
- one decision record.

No other row's text has moved.

Checks I ran at this tip:
- `trace.py --strict` exits 0.
- The perspective record passes `hats.py record ... --check --strict`.
- The 66 cases in `tests/test_usage_ingest.py` and `tests/test_claude_transcripts.py` pass.
- The command has four places that print a line. Three carry the invocation prefix: the absent line, the skip and governing-record refusal lines, and the per-invocation outcome lines. The fourth, the reader's shape refusal, prints `refused <file>: <field>`, which is the form the row now states.

All twenty-one rows are ready.

- [APPROVE] SR-244 -> the obligation: record once each transcript-bearing session that completion ingests, nested agents included, with identity and transcript usage. Record no message twice, duplicate no service record, grant no gate authority, include no transcript text, refuse an unknown shape, and direct completion to ingest the current session and a named prior tail -> what its chain shows: unchanged since sittings 007 and 008. The derivation is recorded through PERFORMANCE and fed back to SN-026, and every acceptance clause measures a Requirement obligation -> why it is ready: on 007's reasons.
- [APPROVE] LLR-347 -> the obligation: usage from assistant messages, once per id at its last record, under the stated finality rules, with one open last message, partial marking and the reasoning rule -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-348 -> the obligation: one invocation per transcript, with its identities, a deterministic 32-hex id, and COORDINATOR or SUBAGENT role and phase -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-349 -> the obligation: a contribution's count, cursor, immutable key, endpoint timestamps and rising name stamp -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-350 -> the obligation: exactly-once over same-invocation logs in every record directory, with refusals that name the log -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-351 -> the obligation: a service-recorded main transcript is skipped, sub-agents follow the declared coverage constant, the session's own contributions are not service records, and an unreadable governing record refuses -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-352 -> the obligation: a closed transcript shape, any positive non-boolean depth, unresolved parents named, and refusal per transcript naming the file and field -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-353 -> the obligation: the ambient home and never an account home, an explicit session before the ambient one, exit 2 with neither, two locations refused naming both, and an absent main transcript named while its sub-agents are still read -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-354 -> the obligation: the contribution's enumerated fields and a fixed summary body, without transcript text or raw usage -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] LLR-355 -> the obligation:
  - the command takes an optional session and root;
  - it emits recorded, unchanged, open, skipped, refused, absent or unresolved-parent outcomes, each invocation's line naming its role, agent type and agent id, while a transcript refused for its shape is named by its file and field, in IF-306's stdout form;
  - it exits 0 with no refusal, absence or refused commit, 1 with any of them, and 2 with no session.

  -> what its chain shows: sitting 008's finding is answered. The sentence now claims the prefix only on invocation lines, and gives the shape refusal its real form. That matches every place the command prints a line: the shape refusal is unprefixed, and the absent, skip, governing-refusal and outcome lines are prefixed. IF-306's `data` cell and the module's contract text now say the same, so the row, its interface and the code agree. Downward:
  - TC-389's new case pins the prefix on recorded, unchanged and open lines;
  - TC-391 holds the shape refusal by file and field, and the unresolved-parent line;
  - TC-390 holds the skipped line;
  - TC-394 holds the absent line and every exit code.

  -> why it is ready: a closed contract over its outcome kinds and exit codes, citing its interface by id, with no `shall` and no symbol in its text.
- [APPROVE] LLR-356 -> the obligation: completion ingests its current session before its handoff, names its own session, re-ingests a replaced handoff's named session, and records only the newly final range -> what its chain shows: unchanged since 007 -> why it is ready: on 007's reasons.
- [APPROVE] TC-386 -> unchanged since 007: identities, deterministic ids and the non-synthetic model -> ready on 007's reasons.
- [APPROVE] TC-387 -> unchanged since 007: the once-per-message sum, the vocabulary, partial state and the role values -> ready on 007's reasons.
- [APPROVE] TC-388 -> unchanged since 007: the finality arms -> ready on 007's reasons.
- [APPROVE] TC-389 -> unchanged since 008 approved it: every Expected clause, including the identifying prefix on recorded, unchanged and open lines, is held by a listed case -> ready on 008's reasons. The narrowed LLR-355 sentence leaves its clause exact.
- [APPROVE] TC-390 -> unchanged since 007: the skip under both coverage states, and the governing-record refusal -> ready on 007's reasons.
- [APPROVE] TC-391 -> unchanged since 007: shape refusals named by file and field with exit 1, nesting and parents observable, two locations refused -> ready on 007's reasons, and its "named" clause now matches LLR-355's stated form.
- [APPROVE] TC-392 -> unchanged since 007: a fixed summary body with no transcript text -> ready on 007's reasons.
- [APPROVE] TC-393 -> unchanged since 007: no round, build, draw or resume carrier, verifying SR-244 directly -> ready on 007's reasons.
- [APPROVE] TC-394 -> unchanged since 007: home, precedence, exit 2, absent main transcript, and the exit-1 cases -> ready on 007's reasons.
- [APPROVE] TC-395 -> unchanged since 007: the synchronized guidance's ingest order and session naming -> ready on 007's reasons.

OUTCOME: APPROVE rows=21

SITTING: JUDGED kinds=first-approval
