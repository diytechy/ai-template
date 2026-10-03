+++
id = "WI-748"
title = "Codex adapter: read cache-write tokens, and infer compaction from a prompt-size drop between turns"
workstream = "process"
specref = "project-trajectory/scripts/session_adapters.py"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

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
