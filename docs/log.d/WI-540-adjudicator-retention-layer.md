## 2026-08-31 — WI-540: the adjudicator session-retention layer, shipped inert at dial 0

Plan §5 step 3 of the adjudicator session-retention plan
(`docs/plans/2026-08-29-adjudicator-session-retention-plan.md`). The layer that
turns WI-535's telemetry into an opt-in retained session: a session store, a
per-family resume-argv adapter, occupancy readers, the drain/reset rule and the
keep-warm tick — all guarded behind `[adjudicator] context_reset_pct`, shipped
at `0` (inert: today's one-shot behaviour byte-for-byte). Turning the dial on
and verifying it on-box is WI-541 (plan §5 step 4).

Owner rulings honoured (OI-69, `docs/log.d/2026-08-30-owner-rulings-oi68-oi69.md`):
(a1) no-daemon — a retained transcript a bounded process replays, not an actor;
(b1) `reset_on_same_artifact = false` default; (c2) keep-warm pings THROUGH the
blackout (Anthropic only) — the plan's own §2/§3.5 "skipped inside the blackout"
text is superseded by this ruling and the code follows the ruling; (d1) dial in
`docs/process.toml [adjudicator]`; (e1) dedicated CLI homes once the dial is on.

Deviations from spec: keep-warm pings through the blackout per OI-69 (c2),
against the plan §2/§3.5 wording (Sol #17); recorded above and in the spec
Context.

### REVIEW-A rework (round 002, CHANGES-REQUESTED findings=6)

Session 003 died mid-rework on a provider usage limit; this session reconciled
its uncommitted residue (the fix shape was already in the tree), completed and
verified it. What the rework changes, finding by finding:

1. MAJOR (store keyed by family only) — the store is now keyed by
   `(family, route_id)`: the route id is hashed into the filename and checked
   verbatim after parsing, so neither a misplaced file nor a stale family-only
   record crosses a route boundary; `load_family` enumerates one family's valid
   records for the dispatcher's keep-warm; `adjudicator_launch` refuses a
   missing route id. Driven: a stored `OPENAI-A` session is never resumed for
   `OPENAI-B` (`test_launch_never_resumes_another_route_of_the_same_family`).
2. MAJOR (governing hash omitted the judging templates) — `map_preflight` now
   returns the actual file each loaded prompt came from (override-aware);
   `resolve_session_setup` carries the four `adjudicate-*` paths on
   `LoopContext.adjudicator_prompt_paths`; `route_session` passes them to
   `adjudicator_launch`, whose `governing_hash` folds them in; a changed
   judging instruction drains the session and retires it at the next clear
   point. Driven at both ends:
   `test_governing_hash_changes_with_the_loaded_adjudication_template`,
   `test_preflight_surfaces_the_loaded_adjudication_template_to_the_hash`,
   `test_loaded_adjudication_prompt_change_retires_at_clear_point`.
3. MAJOR (OPENAI/OPENCODE never read their telemetry) —
   `adjudicator_session.context_telemetry` selects the reader by family:
   OPENAI joins the emitted `thread.started.thread_id` to the exact
   `rollout-*-<id>.jsonl` under the launch environment's `CODEX_HOME` (no
   `--last`, no ambient home — either could select another route's
   transcript); OPENCODE reads its own `--format json` stream.
   `adjudicator_bookkeeping` persists the captured id, so a later launch
   resumes instead of minting; `session_meta` merges the retained columns
   blank-by-blank over WI-535's one-shot tuple. Driven:
   `test_openai_bookkeeping_captures_thread_and_rollout_then_resumes`,
   `test_opencode_bookkeeping_captures_stream_session_then_resumes`.
4. MINOR (IF-174 Rationale cited history) — the cell now states only the
   standing reason; provenance lives here.
5. MINOR (IF-174 Data over ceiling, named a runtime path) — the cell is now a
   typed pointer to the owner contract ("AdjudicatorSession record schema and
   callable API declared by Contract IF-174 in scripts/adjudicator_session",
   99 chars vs the 160 ceiling).
6. MINOR (no contract on the owner) — `adjudicator_session.py`'s header now
   carries `Contracts: IF-174` and the `Contract IF-174:` body (record schema,
   compound identity, atomic writes, per-family readers, lifecycle purity).

Adjacent consequences of the compound key: the dispatch keep-warm tick
enumerates `load_family("ANTHROPIC")` instead of reading one family file;
LLR-163/TC-157 re-pointed at the adapter seam (`resume_template` joins
`split_cmd`/`build_argv`; TC-157 verifies IF-174's surface);
`IF-064`'s row names `scripts/adjudicator_session` a requestor of `split_cmd`.
Ratchets re-stamped DELIBERATELY: module-size DOWN (agent_loop 2640 -> 2622,
agent_common 1300 -> 1299 — the bookkeeping body moved into
`adjudicator_session.bookkeep`, one home); the complexity baseline's
`route_session` entry dropped (the launch call now sits under the census
floor). Smoke-budget membership: 1478 collected vs the 1482 ceiling — inside
the stamped headroom, no re-stamp owed.
# fig: cmd="python -m pytest -q -n auto -m smoke --collect-only" rev=6210a254-dirty

Deferred open items: none.
