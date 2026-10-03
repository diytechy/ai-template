+++
id = "WI-748"
title = "Codex adapter: read cache-write tokens, and infer compaction from a prompt-size drop between turns"
workstream = "process"
specref = ""
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

The codex adapter's two gaps from WI-541's live runs, closed:

- **Cache writes:** the usage record reads `cache_write_input_tokens` (and
  `reasoning_output_tokens`) when reported and leaves them empty when absent. Fresh
  input subtracts cached and cache-write tokens, clamped at zero; that codex's
  `input_tokens` includes cache writes is taken from the usage shape and is not yet
  verified live (the only live line reports 0), and the rows say so.
- **Compaction:** a retained session's row records `compacted` with
  `compaction-source` `reported` (the rollout's `compacted` entry) or `inferred` (a
  drop across any consecutive pair of NEW rollout per-request prompts, from the
  stored baseline, with a cursor so old requests are not rechecked). Exec
  `turn.completed` totals are per-turn sums of requests (15154 + 15224 = 30378 in the
  live fixtures), so they never drive an inference; a kit reset clears the
  comparison.
- **Rows:** TC-264 method and LLR-268 detail amended in place (Approved, for this
  merge's adjudication); IF-266, LLR-290, TC-303 added Drafted. A RESYNC entry; the
  session log gains `compacted` and `compaction-source`.
- **Reviews:** Sonnet 5.5, NOT YET SOUND at 72b035e5 (per-turn sums read as request
  prompts; only the last pair compared), SOUND at 630150c3
  (`docs/reviews/2026-10-02-wave7/sonnet-wi748-r1.md`, `-r2.md`).

## Context

Filed 2026-10-02 at the owner's direction, from WI-541's live runs on
codex-cli 0.157.1 (`docs/work/queued/WI-541-verify-retention-layer.md`):

- Cache READS are parsed correctly (`cached_input_tokens`). Cache WRITES are not:
  0.157.1 reports `cache_write_input_tokens`, and `CodexAdapter`'s usage builder
  hard-codes `cache_write=None` (`session_adapters.py`, the codex usage arm), so
  TC-264's usage formula reads "not reported" for codex.
- No code under `project-trajectory/scripts/` sets `compacted`. The `exec --json`
  stream carries no compaction event; the rollout file records a `compacted` entry
  with `replacement_history`. The observed run's request prompts went 15,489,
  20,422, 35,911, then 15,717 after the provider compacted, with no reset by the
  kit. The stream's `turn.completed` usage is a running total, so per-turn prompt
  size must be differenced, and a compaction inside one turn shows only at the next
  turn.

## Done-when

- The codex usage record carries `cache_write_input_tokens` when the CLI reports
  it, and stays empty when it does not, with a test over a recorded line of each.
- A retained session's row records `compacted = true` when the rollout carries a
  `compacted` entry, or, without one, when the latest request's prompt falls below
  the previous request's prompt with no reset by the kit in between. Each is
  tested, and the inference is labelled as inferred, not reported.
- A shape the fixtures lack is recorded live, not hand-written (WI-541's rule).
- The commit bar passes.

Noted 2026-10-02 by WI-749's adjudication: TC-264's (approved) clause says codex's
"unreported cache write" stays empty, true of the adapter today. Reading the field
changes what that clause must say: amend TC-264 in this lane (status left Approved,
for the merge's adjudication).
