# WI-887 dispute 008 — findings DA, DB

Ruled at 5dc2d4144, lane range b3ef42844..27831e0f7, within the bound set by
PROCESS.md §6 "Review threat model".

## DA — the store admits a full record whose optional compaction fields are mistyped

Observed, not taken on either account. I wrote a scoped OPENAI review record
to a file under its own `_record_name`. It carried every identity, retirement
and session field, plus `"rollout_requests": "oops"`.

- `_read_record` returned it, and `_variant` classified it `full`.
- `_observe_compaction` over that record then raised `TypeError: slice indices must be integers or None`, at `prompts[(cursor or 0):]`.
- That call sits inside `keep_bookkeep` (session_keep.py ~1033), which `session_service.act` calls (~440) with no handler, so the review call itself raises after its launch.

The lease half of the reviewer's remedy does not hold. Every consumer of the nested lease values (`_lease_held`, `retire_stale_lease`, and the holder check in `keep_bookkeep`) already tests `isinstance(lease, dict)` and the type of `until` before using them.

**Scope.** §6 excludes reproductions that need the host compromised or contrived: a hostile binary, a tampered OS or tool, an environment changed mid-call. A mistyped field in the kit's own runtime store is none of those. More decisively, this lane made malformed-record fail-closed a SUPPORTED behaviour three times over:

- its Trust ruling: "an absent, unreadable or malformed record ... is no record, so the call mints";
- SR-239, approved: "read an absent, unreadable, malformed, misfiled or differently keyed retained record as no session and start fresh";
- LLR-270, re-attested at act 108: `_read_record` "accepts only writer-produced ... variants with all consumed fields typed".

`rollout_requests`, `request_prompt` and `compaction_source` are consumed fields, read by `_observe_compaction`. So the code fails the very text this lane approved. That is a regression of stated behaviour, which is in scope.

The compaction fields do predate the lane (`_observe_compaction` read `rollout_requests` at the base). But the reader that claims to close the boundary is this lane's, so the gap between that claim and the code is this lane's too.

**Worth the cost.** The fix is small and ends the class instead of chasing it. This is the third round on one boundary (round 001 F2, round 002 F1, now DA), each found one field at a time. The remedy is therefore not "type `rollout_requests`". It is to complete `_variant`'s declaration with every OPTIONAL top-level field any consumer reads, each with its type, checked when present:

- the compaction cursor and baselines (`rollout_requests`, `request_prompt` allowing null, `input_total`, `compaction_source`, `compacted`);
- the occupancy and use fields (`occupancy`, `window`, `pct`, `last_used`, `last_used_epoch`), as their writers produce them (the `""` placeholders included).

Add the resumed-review regression the reviewer names: one parametrised case per declared optional field, each mistyped, that the draw mints fresh instead of raising. A fourth review round then has no undeclared field left to find. Nested lease values need no change.

## DB — approved SR-239 carries two `shall`s

The reviewer's broad reading is not upheld. On that reading, SR-239 must be split into six rows (identity, fallback, warm suppression, final mode, template invalidation, audit) or waived. Sittings 005 and 006 judged the row as one decision, reviewer-session retention, enumerated as clauses the way the approved SR-227 enumerates its own. Nothing at this range changes that judgement.

The narrow fact under the finding is real, though, and it is mechanical:

- `trace.py --strict` at this range exits 1 with `FINDING (requirement form): SR SR-239 Requirement carries 2 'shall'`.
- That command is the traceability step `check.py` runs.
- `trace_text`'s shall-count check skips Drafted rows, which is why the finding appeared only once sitting 006 flipped SR-239 to Approved.
- The check reads no `recorded waiver:` marker, so the waiver route the reviewer offers would not clear it.

The second `shall` exists because sitting 005 told the author to move the fail-closed reading out as an `If ... then` clause, which here means a second obligation sentence. Sitting 006 then approved the row without re-running the gate. Both were this adjudicator's errors.

**The defect:** an approved row now fails the singular-requirement gate (PROCESS §3, "Singular: exactly one `shall`"), which `trace.py --strict` enforces.

**The remedy** is to restore one `shall` per row, without restating the retention obligation as six rows. Either:

- move the fail-closed reading into its own sibling SR in the `If ... then` pattern, citing SR-239 (the cleaner EARS shape); or
- word it as a response clause of SR-239's single `shall`, with its condition kept reachable.

Either way, the changed or new rows go back through an adjudication sitting, MEANING or first approval as applicable. They must not be edited in place under the existing approval.

Separately, and outside both findings: `trace.py --strict` here also reports `LLR LLR-292 Detail uses 'minimal'`. That finding predates the lane; LLR-292 is unchanged in b3ef42844..HEAD. And a process gap worth its own work item: the in-lane closure check before a sitting should run the requirement-form check on Drafted rows, so that a gate that fires only on Approved rows is seen before approval, not after it.

RULING: DA FIX _read_record admits a full record whose optional consumed fields are mistyped (rollout_requests "oops" reproduced: classified full, then _observe_compaction raises TypeError uncaught through keep_bookkeep and session_service.act), contrary to this lane's approved SR-239/LLR-270 fail-closed contract; complete _variant's declaration with every optional field any consumer reads (compaction cursor/baselines, occupancy and use fields) plus a parametrised resumed-review regression; nested lease values are already guarded at their consumers and need no change
RULING: DB FIX approved SR-239 carries two shall sentences and so fails trace.py --strict's singular-requirement gate (exit 1; the check skips Drafted rows and reads no waiver), a defect introduced by sitting 005's If-then direction and missed by sitting 006's approval; restore one shall per row (a sibling If-then SR for the fail-closed reading, or a response clause under SR-239's one shall) and re-sit the changed rows, without the six-way split the reviewer proposes
