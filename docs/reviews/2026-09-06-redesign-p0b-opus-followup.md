# P0b follow-up review — Opus 5, high

Provider session: a702dc50-9e5e-4258-a5fd-01f095430bf9

Subject SHA256: `d4a8ae135e98761ea08f0600ee568a425b332bda0430f6c0e96d9c1e35f9360d`

# P0b follow-up adversarial review — Opus 5

Reviewed against the supplied source only. No edits.

## Verification of the prior findings

| # | Prior claim | Status in this source |
|---|---|---|
| B1 | planner logs never committed | **Fixed.** `_dp_session` now calls `commit_telemetry(root, invocation-id, "<phase> <outcome>", [log_path])` immediately after the write. The *mkdir* half of B1 was **false** — `write_session_log` already does `iter_dir.mkdir(parents=True, exist_ok=True)`. Scope is correctly narrow: only the invocation record, not the round's artifacts. |
| B2 | explicit `null` renders `None` | **Fixed.** `session_meta` gates on `is not None` and emits `"?"` per counter; `test_explicit_null_token_is_unknown_in_legacy_display` pins `100+?`. |
| B3 | cost/cache dropped from header | **Retracted — was false.** `write_session_log`'s key tuple lists `cost-usd`, `cache-read`, `cache-create` above the new keys. The added round-trip test is the right closure. |
| B4 | `None` base reaches another caller | **Retracted — was false.** `stale_terminal_assignment` reads `if not base: return True` *before* `train_evidence`; refusal is the documented direction. Widening `default_base` did not re-enter OI84. |
| B5 | float `wall-secs` | **Fixed.** Both assignment sites in `invoke_session` are `int(round(time.monotonic() - started))`; monotonic measurement kept, integer carrier preserved. |
| B6 | third name-status parser | **Fixed at the source.** `name_status` now lives in `agent_common` beside `claim_subject` and `_is_claim_move` consumes it. (Integrator delegation is asserted, not shown — see C2.) |
| B7 | bare `scripts/` smoke path | **Retracted — was false.** Meta-repo-owned `docs/stack.ini`; not templated, not scaffolded. |
| NB-1 | redundant drift guard | **Fixed.** `run_loop` is now a bare loop; the single check sits in `run_iteration` after `wait_out_blackout`, retargeted test present. |
| NB-5 | parentless claim fails closed | **Fixed.** `diff-tree --root` makes a root commit readable; a prose root commit yields `removed != wi_ids` → `False`, not `None`. |
| NB-6 | restart vs. finished-branch order | **Fixed.** The `EXIT_RESTART` arm precedes `finished_branches`, and `_advance` short-circuits to `preserved` once armed. |

## Remaining items

**R1 (condition, must discharge before the queue resumes) — planner logs are a second producer in the worker's tracked log stream.** B1's remedy is correct, but it makes `docs/iteration/` permanently carry rows named `<32-hex invocation-id>-<stamp>.log` with no train prefix, `phase` drawn from the step kind (`plan`/`critique`) rather than the loop's uppercase vocabulary, and `date` set to `metrics["started-at"]` (ISO-8601 `Z`) where every worker row is `%Y-%m-%d %H:%M`. Three consumers were not shown and must be driven once against a directory containing both shapes: `next_session_number` (worker numbering must not be perturbed by a non-train, non-numeric name), the integrator's index regeneration, and anything that `strptime`s `date`. Normalising `date` to the existing format is one line and removes a third of the exposure.

**R2 (small, real, shown) — the provenance line is now false on planner rows.** `write_session_log` hardcodes `# agent-loop session log — written by scripts/agent_loop.py` as line 1; `plan_runner` now emits that header. In the one artifact whose purpose is durable attribution, the attribution line is wrong. Generalise the wording or derive it from `meta["role"]`.

**C2 (verify) — `name_status`'s stated precondition at the integrator's call site.** The shared parser documents "no-renames" and takes `parts[-1]`. The integrator's previous parser took the first-tab *remainder*. On a rename record (`R100\told\tnew`) those differ — old path vs new path — and that feeds merge authorisation. Confirm `integrate`'s invocation passes `--no-renames`; if it does, this is closed and nothing else is owed.

**Non-blocking**

1. `commit_telemetry` is best-effort by design; under a hook veto the planner log stays untracked. On a lane branch that residue is swept, on trunk it re-wedges `dispatch`'s `working_tree_dirty` preflight. Acceptable under supervised execution; record it rather than mechanise it.
2. `session_meta` still re-derives `cost-usd`/`cache-read`/`cache-create` with `.get(..., "")`, so an explicit `null` renders `"None"` there. Only the unconditional `meta.update(invocation)` saves it. The B2 fix was applied to `tokens` alone; the other three are latent, not live.
3. NB-4 was accepted but only half-landed: the reconciling note is in `session_meta`, while `write_session_log`'s WI-535 header comment still attributes all four columns to `family_context_telemetry`. One comment.
4. A merge commit carrying the claim subject yields an empty `diff-tree` (no `-m`) → `False` → merge-base fallback. Degrades to prior behaviour; no action.
5. Quoted/non-ASCII paths remain unhandled in the shared parser (pre-existing, inherited by both callers). Failure direction is "not a claim" → fallback, not a false authorisation.

## Contract assessment

Unchanged from the prior review, and the source confirms the reasoning rather than merely restating it. `EXIT_RESTART` is returned by `_lane_close` **before** `close_partial`, and `_advance`'s `preserved` verb bypasses `_lane_close` entirely — so no disposition row is minted, no work outcome recorded, and SR-028's three mechanisms (`classify_outcome`, the zero-HEAD fail-closed guard, the all-ERROR rung) are untouched. Exit 11 parks; it does not decide. IF-015 `Drafted` with 11 as the declared carrier is sufficient; no SR/LLR/TC amendment is owed.

The one contract-adjacent change this round introduces is R1: SR-176/LLR-177's per-session log now has a second writer. That is a widening of an existing artifact's producer set, not a new schema, spool or aggregate — consistent with the stated constraints — but it should be stated in the record where the log's shape is owned, not left implicit in `plan_runner`.

Growth is now honest: `name_status` consolidation removed the duplication B6 named, `run_loop`'s guard is gone, and `session_meta`'s parse is a gated reuse of the same payload rather than a divergent one. Re-stamp the ratchet entries downward in the same commit if they were stamped against the pre-correction size.

**Verdict: APPROVE WITH CONDITIONS.** No blocking defect is demonstrable in the shown source; four of seven prior blockers were real and are correctly fixed, three were false and are correctly rejected with evidence. Discharge R1 (drive the mixed-shape log directory through numbering and index regeneration) and C2 (`--no-renames` at the integrator's call site) before resuming admission; R2 and the comment nits can ride the same commit. This remains an intermediate implementation milestone, not P0a completion, and the record says so.
