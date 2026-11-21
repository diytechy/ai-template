+++
id = "WI-1033"
title = "Model routes and routing consent move into docs/process.toml, and coordinator tools read each role's model from them"
workstream = "process"
sr_refs = ["SR-040", "SR-154", "SR-148"]
needs = ["WI-1032"]
specref = "docs/plans/2026-10-11-review-churn/README.md#10-one-configuration-file-in-toml"
buildtier = "strong"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed on trunk on 2026-11-21 so the review-churn plan's phase 3 is not lost
(queue-drill hand-off §3.3 N2). This is item 10's step 5, ruled 2026-10-11.
Its rulings-section clarifications include revision 8's "no consent means
no managed loop" and `agents-enabled` as an ordered route array.

Today:

- `docs/agents.toml` (147 lines; template 86) holds one `[agent.<ID>]`
  table per model and route pair, plus `[account.<ID>]` tables, as
  IF-045's contract.
- `docs/agents-enabled` is an ordered pool of route ids, with optional
  per-phase weights and an `@ACCOUNT` suffix, validated by `agent_route.py`.
  An absent or empty pool silently falls back to the single-model
  `[agent-loop]` path.
- `[agent-loop]` (`model`, `model-map`) lands in `process.toml` with WI-1032.
- This repo's coordinator tools hard-code each role's model.
  `scripts/coordinator/codex_call.py` maps `REVIEW-A` and `CRITIQUE` to
  `OPENAI-SOL` and `AUTHOR` to `OPENAI-TERRA` in `ROLE_ROUTES`, and only a
  per-call `--route` overrides it. The ruling says these tools read their
  models from the routes. It meets the operator's expectation of 2026-11-21
  that the authoring model "would just be configurable".
- 11 scripts read `agents-enabled` and 11 read `agents.toml`.

Settled here:

- **Routes become `process.toml` tables** under the schema of WI-1031. Their
  triple-quoted notes strings stay, since the shape rule is gone.
- **Consent becomes a setting** that keeps its meaning exactly: an ordered
  TOML array of tables, each an `id` with optional per-phase weights and an
  account. It is validated as `agent_route.py` validates today.
- **No consent, no managed loop.** `[agent-loop]` retires into the routes,
  and with it the fallback. The loop refuses to launch with an empty or
  absent pool, naming the setting. A one-model setup is a pool of one
  route. The template ships the pool empty.
- **The coordinator's role defaults come from the routes:** a setting maps
  each coordinator role to a route id, and `codex_call.py` reads it. `--route`
  stays as the per-call override.
- Adopters migrate by this row's own RESYNC entry, applied by an LLM; no
  new migrator.

## Done-when

- [ ] `agents.toml`'s tables and `agents-enabled`'s pool live in
      `process.toml` and its template, under WI-1031's schema. Both old
      files are deleted and refused by name when present.
- [ ] Every reader of either file reads the new home. `agent_route.py`'s
      validation and IF-045's contract hold for the new carrier: the
      interface row moves to it, and the row stays `Drafted`.
- [ ] `[agent-loop]` is gone. The loop refuses an empty or absent pool by
      the setting's name, and a test shows it.
- [ ] `codex_call.py` takes each role's default route from the setting, and
      a test changes the setting and sees the route follow.
- [ ] `RESYNC_PACK.md` carries this row's entry.
