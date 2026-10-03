+++
id = "WI-541"
title = "Verify the retention layer on this box before the dial is turned: windows, compaction ceiling, occupancy, TTLs, replay"
specref = "docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists"
workstream = "process"
sr_refs = []
needs = ["WI-620"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

`needs` re-pointed 2026-08-31: this row waited on `WI-540`, which closed
`partial` (terminal), stranding it — the gap `docs/handoff-2026-08-31.md` §2
names. `WI-551` supersedes `WI-540` and builds the retention layer this row
verifies (as the session service's keep operation, after WI-620), so the edge
follows the successor. (`WI-552` makes this strand
class visible at mint time.)

**Folded 2026-09-28 from WI-719** (the sampled spot check of WI-620's close,
wave-5 ruling 57). WI-620 closed with four clause parts openly owed, and
they are recorded here because this row's live runs on this box produce
them:
- WI-606's recorded-fixture clause, and its opencode pathway re-check;
- WI-551's recorded-fixture clause;
- the log-fragment half of WI-605's third clause.

The permission classifier refused the builders' live codex and opencode
runs, so those runs need the owner, or a session they authorize. The
verdict is
`docs/reviews/wi-719-spot-check-the-clean-close-of/001-SPOTCHECK-d7e1be0e.md`.

## Done-when

- The context window each routed family reports on this machine is recorded
  beside the configured fallback, and a mismatch is logged rather than guessed.
- A retained session driven toward the compaction ceiling (the auto-compact
  window set low) is observed and recorded: the kit's reset fires before the
  provider compacts, or the compaction is logged on the session's row.
- Occupancy on a real multi-step, tool-using adjudication is checked against
  the latest request's prompt size, the rule the reset trusts, and any
  disagreement is recorded. The log fragment names the first session log
  written under the corrected occupancy meaning (the latest request's prompt
  over the window), and its `context-pct` reads at or under 100 (WI-605's
  third clause, second half).
- The first live `codex exec --json` and `opencode run --format json`
  sessions on this box are recorded into `tests/golden/sessions/`, in place
  of the documented-shape fixtures (`codex-exec-json.jsonl`,
  `codex-rollout.jsonl`, `opencode-run-json.jsonl`). Their NOT LIVE first
  lines are removed, `tests/test_session_adapters.py`'s provenance note and
  TC-262/263/264/267's method cells say so, and the adapter tests stay green
  over the recordings. A shape the installed CLI emits differently from the
  documented one is a finding on the adapter, filed, not patched into the
  fixture. This carries WI-606's third clause ("a test over a recorded
  fixture of that CLI's output") and WI-551's third ("each provider's resume
  and occupancy parsing from recorded fixtures"); `codex-rollout.jsonl`
  serves both.
- The opencode pathway checks (stdin prompt delivery, the global `--auto`
  flag, final-text-only stdout under `--format json`, auth) are re-run on
  the installed opencode over the changed route, with their output quoted
  in the log fragment. `docs/agents.toml`'s OPENCODE family and row notes
  record the version actually tested. A failing check disables the route
  or is filed, and the version is not bumped over it (WI-606's last clause,
  carried verbatim).
- The codex and opencode cache TTLs and the resume replay time at 100k–700k
  tokens are measured.
- Each reading is in the log fragment with its producing command under `fig:`,
  and the retention dial in `docs/process.toml` is left at 0: turning it on is
  the owner's act.

## Owner direction 2026-09-30

The owner authorizes the live codex and opencode runs on this box ("You can
perform the test"). This clears the gate the permission classifier left on the
runs; the row is claimable by a session that performs them. The retention dial
stays at 0 (its turning on is still the owner's act).

## Progress 2026-09-30

Done (log fragment `docs/log.d/2026-09-30-wi541-live-recordings.md`): the live
codex and opencode recordings replace the three fixtures; the adapter tests, TC-262,
TC-264 and TC-267's method cells say so; the opencode pathway re-check on 1.18.29
is recorded in `docs/agents.toml`; the codex window (258,400) and the last-request
occupancy are recorded.

Still owed, and this row stays open for them:
- the compaction-ceiling run (auto-compact window set low), occupancy on a real
  multi-step adjudication, the cache TTLs, and replay time at 100k–700k tokens;
- a recording of the kit's own route command: the classifier refused
  `--dangerously-bypass-approvals-and-sandbox`, so the fixture came from
  `--sandbox read-only` with no model pinned;
- a finding on the codex adapter: 0.157.1 reports `cache_write_input_tokens`, which
  the adapter records as "not reported" (the TC-264 usage formula's codex arm).

### The kit's own route command, run by the owner 2026-10-02

The classifier refused the agent's run of
`codex exec -c model_reasoning_effort=medium --model gpt-5.6-terra
--dangerously-bypass-approvals-and-sandbox --json`, so the owner ran it in a terminal on
codex-cli 0.157.1 (same read-a-file prompt). Result: the same event shapes as the
`--sandbox read-only` fixture (thread.started, turn.started, command_execution
started and completed, agent_message PINEAPPLE, turn.completed), final text
PINEAPPLE, usage input 27,152, cached 24,064, output 101, `reasoning_output_tokens`
27 (nonzero this time), `cache_write_input_tokens` 0. Fed through the adapter in
memory: usage and thread id parse correctly, reasoning 27, cache write still ""
(the finding above), no occupancy from the exec stream. No new fixture was needed;
this closes the "route command" item. Not committed as a fixture.

### Compaction ceiling, observed 2026-10-02

`codex exec --json --sandbox read-only -c model_reasoning_effort=low -c
model_auto_compact_token_limit=20000`, six sequential file reads, one session. The
override IS honoured on codex-cli 0.157.1, so the ceiling is reachable for about 50k
tokens, not near the 258,400 window. Observed: request prompts grew 15,489 ->
20,422 -> 35,911; the provider compacted (a `compacted` entry with a
`replacement_history` in the rollout) and the next request's prompt fell to 15,717.
Findings, not patched:
- the `exec --json` stdout stream carries NO compaction event (event types seen:
  thread.started, turn.started, item.started/completed, turn.completed); only the
  rollout file records it, so the plan's "`codex thread/compacted` event on the stream"
  source for `compacted = true` does not exist for `exec`;
- no code under `project-trajectory/scripts/` sets `compacted` at all (grep finds none),
  so the plan's "compaction is logged on the session's row" is unbuilt for every route;
- the kit's reset fires before the provider compacts only if its dial is below the
  provider's limit; with the default codex limit unmeasured here, that stays an
  assumption until a run without the override approaches it.
Still owed: real multi-step adjudication occupancy, cache TTLs, replay time. Those
two measurements need large contexts; a scaled measurement (20k to 100k) with an
extrapolation is possible but would not meet the 100k-700k wording without the
owner's ruling.

### Large-context replay, measured 2026-10-02 (codex-cli 0.157.1, default model, `--sandbox read-only`, low effort)

A 418 KB random-word prompt tokenized to 212,530 input tokens (82% of the 258,400
window), because random words tokenize badly; the window caps one session below the
row's 100k-700k wording, so 700k is unreachable on this model. First request: 10 s wall.
An immediate `codex exec resume` of the same thread: 6 s wall; the second request's
input was 212,548 tokens of which 212,352 were cached (cumulative `turn.completed`
usage 425,078 input, 224,768 cached, which is why the exec stream's usage is a running
total). Cache TTL probes (resume after 6 and then 10 further idle minutes) were started
in the background; results go in the log fragment if they land. Not done: occupancy on a
real multi-step adjudication brief through the kit's own session path.

### Cache TTL probes, measured 2026-10-02 (same ~212k-token codex thread)

Each probe is one `codex exec resume` replaying the whole thread; the usage figures
are cumulative, so each is the difference from the previous `turn.completed`.
- After ~6 min idle (20:40:29 to 20:46:41): 7 s wall; 214,127 input tokens, 212,352 of
  them cached: a cache HIT.
- After ~13.5 min idle (20:46:48 to about 21:00:19; the owner's machine slept, which
  paused the script's own timer, so the real gap is taken from the output files'
  timestamps): 11 s wall; 214,146 input tokens, 0 cached: a cache MISS, and the
  replay cost a full re-read.
So codex's prompt-cache TTL on this box lies between 6 and about 13.5 minutes
(consistent with a roughly 10-minute window, but not pinned to it). A keep-warm ping
must therefore fire inside 6 minutes to be safe; a 10-minute cadence is unproven.
Replay time at 212k tokens: 6 to 7 s cached, 10 to 11 s uncached. One sample each, one
model, one box. 700k is unreachable (window 258,400); occupancy on a real multi-step
adjudication through the kit's own session path is still owed.
