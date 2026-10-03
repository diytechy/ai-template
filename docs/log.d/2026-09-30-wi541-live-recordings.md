## 2026-09-30 — WI-541: the live codex and opencode recordings

The owner authorized the live runs. One tool-using read of a one-line file, then
the answer, on each CLI on this box.

**Recorded, replacing the documented-shape fixtures** in `tests/golden/sessions/`:
`codex-exec-json.jsonl` (codex-cli 0.157.1; `codex exec --json --sandbox
read-only`, stdout verbatim), `codex-rollout.jsonl` (the same run's rollout,
trimmed to the identity fields, task events and token_count events; account ids,
injected instructions and rate limits dropped), and `opencode-run-json.jsonl`
(opencode 1.18.29, `opencode-go/kimi-k3`, working path rewritten). Their NOT
LIVE lines are gone; `tests/test_session_adapters.py`, `test_session_keep.py`
and `test_session_service.py` pin the recorded values, and TC-262, TC-264 and
TC-267's method cells say the fixtures are live. Smoke tier: 1903 passed, 3
skipped, 31.2 s against the 60 s budget.

**Window and occupancy.** Codex reports `model_context_window` 258,400 for its
default model on this box, and the last request's inclusive input was 15,224
(6%), read from the rollout as the adapter does. No configured fallback window
exists in the repo for codex to disagree with. opencode reports no window, so
none is guessed.

**opencode pathway on 1.18.29.** Piped-stdin delivery ran a live two-step
session; empty stdin still errors "You must provide a message or a command";
`--auto` is still a global flag; `--format json` emits step_start, tool_use,
step_finish and text events; auth works. Recorded in `docs/agents.toml`'s
OPENCODE family comment. No route disabled.

**Finding on the codex adapter (folded into WI-541, not patched into the
fixture).** codex 0.157.1 now reports `cache_write_input_tokens` (0 here) in
`turn.completed`; the adapter still records cache-write as "not reported".

**Not done.** The recording used `--sandbox read-only` and no model pin, because
the permission classifier refused the kit's own route flag
(`--dangerously-bypass-approvals-and-sandbox`). The compaction-ceiling run,
occupancy on a real multi-step adjudication, the cache TTLs and the 100k–700k
replay times remain open on WI-541.

**Addendum 2026-10-02.** The owner ran the kit's own route command (with the
bypass flag the classifier refused the agent) in a terminal: same event shapes,
final text PINEAPPLE, reasoning tokens 27, cache write 0; the adapter parses it.
The route-command item is closed. The compaction-ceiling run, real multi-step
occupancy, TTLs and replay times remain open.

**Addendum 2026-10-02 (measurements).** Codex honours
`-c model_auto_compact_token_limit` and compacted at the low limit (the exec stream
shows no compaction event; the rollout does; nothing in the scripts sets `compacted`).
At 212k tokens (82% of the 258,400 window) a resume replays in 6 to 7 s with the
cache and 10 to 11 s without it; the cache hit after ~6 idle minutes and missed
after ~13.5, so its TTL is between the two. The 100k to 700k wording is not reachable
on this model; the real multi-step adjudication occupancy remains open.
