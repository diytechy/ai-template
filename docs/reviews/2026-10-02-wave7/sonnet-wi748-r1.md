# Sonnet review — WI-748 (build/wi-748 at 72b035e5)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range `83db9d75..72b035e5`.

72b035e5 NOT YET SOUND

**BLOCKER:** none

**MAJOR**
1. The exec-total fallback compares per-turn SUMS, not per-request prompts, and can infer compaction falsely. `session_keep.py` `_observe_compaction` (~727-747) differences `turn.completed` running totals into `derived` and treats them as request prompts. The live fixtures show a turn is a sum of requests: `codex-rollout.jsonl` has two `token_count` requests in one turn (15154, 15224) and `codex-exec-json.jsonl` reports `input_tokens` 30378 = 15154 + 15224. With the rollout unreadable, a tool-using turn (3 requests, ~50k) followed by a plain turn (1 request, ~17k) differences to a drop and records `compacted=true` (inferred), which then sticks for the session. The tests feed single-request turns, so they hide it. Fix: infer only from rollout per-request prompts and keep exec totals as a baseline with no inference, or label the fallback turn-sum with a stronger condition.
2. The rollout path compares only the last two requests of the whole rollout (`pair[-1] < pair[-2]`, ~739). A compaction usually shows at the first request of a new call, below the previous call's last request; if that call makes further requests, the final two are both post-compaction and rising, and the drop is missed. `previous` is ignored whenever `prompts` is non-empty. Fix: scan consecutive pairs across the requests newer than the stored baseline, comparing the baseline to the first new request.

**MINOR**
1. `session_adapters.py` ~492-498 `fresh = input - cached - cache_write` assumes codex's `input_tokens` includes cache writes; the only live line has `cache_write_input_tokens: 0`, so there is no evidence either way; no clamp if it goes negative; LLR-268 and TC-264 assert the inclusive semantics as fact.
2. `session_service.py` act passes the raw `env` to `adapter.compaction` while `context()` gets `os.environ if env is None else env`; an ambient `CODEX_HOME` is ignored for an unretained call (harmless for retained calls).
3. `compaction()` re-reads the whole rollout on every retained codex call beside `context()`'s read (cost only).

**Held:** the cache-write field read (0 included; "" when absent), fixtures untouched, variants labelled; reset/new generation clears baselines; legacy record learns before inferring; non-codex returns `{}`; `reported` beats `inferred`; only LLR-268 detail and TC-264 method changed among approved cells; IF-266/LLR-290/TC-303 well-formed; log keys backward compatible; RESYNC entry; ratchet +2 honest.

**Commands:** `pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py`: `117 passed in 17.94s`; `check_trajectory.py --strict`: clean (748 WIs).

**Coordinator:** MAJOR 1's fixture evidence verified (rollout per-request 15154 and 15224; exec 30378 their sum). Sent to a fix round.
