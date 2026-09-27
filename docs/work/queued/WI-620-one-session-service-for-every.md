+++
id = "WI-620"
title = "One session service for every model call (act, keep, record) writing the OTel usage schema, with its occupancy fix, lossless codex/opencode capture, and adjudicator retention as its keep operation"
workstream = "unattended"
needs = ["WI-579", "WI-580"]
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#31-a-common-session-service-note-1"
buildtier = "strong"
priority = 3
safety_class = "ordinary"
supersedes = "WI-605;WI-606;WI-551"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-605 (Compute context occupancy from the latest request's prompt, not the session's cumulative usage (review pack C1)), WI-606 (Record codex and opencode token usage losslessly: JSON output on both routes, raw usage kept verbatim (review pack C2)), WI-551 (Retain adjudicator sessions through the session service's keep operation, inert at dial 0). WI-605 and WI-606 were this row's declared first steps (its soft edges), and WI-551 was already rewritten as this service's keep operation. One service, one lane. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

Order: WI-606 (capture raw usage) and WI-605 (occupancy) first, then the service, then WI-551's keep operation on it. It is large: it may land as several commits on one branch, one review chain. WI-541 verifies the result on this box afterwards.

Ruled by the owner: S7 (2026-09-23, option (a): "refactor as much as possible
to reduce individual or custom code components") and S8 (2026-09-24), sister
plan §3.1 and §3.2.

- **act:** a role differs only in data (brief, route, tier, tool set), never in
  its own launch code.
- **keep:** resume by id, keep warm, reset. WI-551 lands through this
  operation, so its keep-warm ping is an ordinary recorded call.
- **record:** one writer replaces the loop's in-line logging and
  `invoke_and_persist`. It writes S8's schema: OTel GenAI usage names pinned to
  a commit, inclusive input, fresh input derived, raw usage verbatim, provider
  and CLI columns, billed tokens apart from context occupancy; exporters are
  optional.
- **provider differences** live in one adapter per provider (argument
  building, output and usage parsing). Claude's two parse defects
  (`reasoning-tokens`, `reported-model`; review pack C2) are fixed in its
  adapter.

WI-606 first captures raw codex and opencode usage; WI-605 fixes occupancy.
The loop's C901 pin (`tests/test_complexity_ratchet.py`) still applies:
decompose, don't re-stamp. It is large; slice it at claim if needed.

## Done-when

- Every model call goes through the service; no role or provider keeps its own
  launch or logging path (grep evidence of the removed paths, and the SLOC
  removed).
- The record step writes the S8 schema for Claude, codex and opencode, pinned
  to a named OTel commit, with raw usage verbatim; a fixture test per provider.
- Claude's `reasoning-tokens` and `reported-model` defects are fixed in its
  adapter.
- The service exposes the keep operation WI-551 lands through.
- The C901 pin and the module-size ratchet hold without re-stamping.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-605 (Done-when, verbatim)

- Occupancy is computed from the final model call's prompt tokens (its
  input plus cache read plus cache write), not the result's cumulative
  counters, and the docstring names the source field.
- A test pins it with a recorded multi-call stream where the cumulative and
  last-request values differ.
- No newly written session log reports occupancy above 100%; the fix's log
  fragment names the first session recorded under the corrected meaning.

### From WI-606 (Done-when, verbatim)

- The codex route runs `exec --json` beside `-o`: a successful session's final
  text still comes from `-o`, and its raw usage events are kept verbatim in the
  session's raw record.
- The opencode route runs `run --format json`, and its raw usage events are
  kept verbatim the same way.
- Each route is pinned by a test over a recorded fixture of that CLI's output,
  showing the usage survives a successful call.
- Today's parsed columns are unchanged: no new field mapping is added.
- The opencode pathway checks are re-run on the installed version over the
  changed route, their output quoted in the log fragment, and
  `docs/agents.toml` records the version actually tested; a failing check
  disables the route or is filed, and the version is not bumped over it.

### From WI-551 (Done-when, verbatim)

- Adjudicator retention runs through the session service's keep operation:
  resume, occupancy, drain and reset, and keep-warm each go through the
  service's act and record steps, and no role or provider code launches or logs
  a retained session on its own (grep evidence).
- With `context_reset_pct = 0`, a test shows the layer inert: no session id
  minted, no resume argument, and the launch identical to a fresh session's.
- With the dial on, tests pin the reset rules (drain at the dial, retire at a
  clear point, retire at once on an errored session) and each provider's resume
  and occupancy parsing from recorded fixtures.
- A keep-warm ping appears in the session log like any other call.
- The `[adjudicator]` table ships at 0 in both `docs/process.toml` and the
  template, with matching structure, and the commit bar passes.
