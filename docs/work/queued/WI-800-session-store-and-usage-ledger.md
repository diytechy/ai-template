+++
id = "WI-800"
title = "One session store with durable invocations, the usage ledger and the spool"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-session-store"
sr_refs = ["SR-222", "SR-227"]
needs = ["WI-798", "WI-799", "OI-109", "WI-851", "WI-847"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-session-store (ch.2 §4, §6, §9). One
untracked store, `out/sessions/store.toml`, absorbs today's per-route JSON under
`out/adjudicator/` (risk 1): slots keyed by family and scope, cooldowns keyed by
`route@account`, and durable invocation records (D-013). U1's usage ledger,
`docs/usage-ledger.csv`, replaces `docs/iteration_index.md` and its uncalled
`regenerate_index` (D-012); `trunk_step` appends it at the final regeneration. Usage
is attributed per invocation, with thread-scope rows taken as end minus a stored
baseline and kill recovery counting only entries after a launch cursor (D-028).
Keep-warm pings, probes and a discarded lane's logs go to the spool
`out/sessions/spool/` instead of trunk (OI-103 Q1; ch.4 §3). It needs the provider
for `harvest` at discard (ch.1 §5, "The U1 hook").

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- A mid-call kill is recovered into a `KILLED` log, from per-CLI fixtures, counting
  only usage after the invocation's cursor.
- A resumed `thread`-scope session's row is end minus baseline, and the claude
  resumed-call fixture pins its scope.
- `trunk_step`'s ledger append is idempotent.
- Spooled logs land exactly once; a spooled entry is deleted only once trunk's tree
  holds its log.
- The backfill covers every existing log (keyed `log:<name>` where a log predates
  `invocation-id`).
- Keep-warm commits nothing to trunk.
- `docs/iteration_index.md` and `regenerate_index` are retired.
- Each spine row the README matrix gives this row (SR-222 and LLR-269, shared with
  WI-801 and WI-804; SR-227, LLR-270, TC-266/267/268/303, IF-247/248, IF-081/155,
  shared with WI-802; LLR-137 shared with WI-807; LLR-246 shared with WI-807 and
  WI-810; a new LLR for the ledger with a TC verifying each arm it states) is
  amended or added and passes adjudication of that row, on whichever adjudication
  path is the one path when this row lands.
- Its LLR-246 amendment follows WI-851's state rule; it adds no per-writer
  held-status arm.
- OI-109 ruled 2026-10-07 (a): under the station authority, the lane-side trunk
  step produces the tree that lands, so the verdict rollup it writes is trunk's.
  The rollup step stays in the one trunk step; a lane outside the authority never
  commits a rollup.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus per-CLI kill fixtures and usage baselines.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; it deletes `out/adjudicator/`
  and resets the store (a dropped session costs one reload).
