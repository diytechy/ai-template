# P0b intermediate review — Opus 5, high

Provider session: 39ea9ea6-c455-4167-b327-46126fd59a82

# Adversarial review — P0b current-runner footing

Reviewed against the supplied diff only. No edits made.

---

## Blocking findings

**B1 — `plan_runner._dp_session`: session logs written into tracked `docs/iteration/`, never committed, no mkdir**

*Trigger:* any `--dual-plan` round (8+ sessions per round).
*Effect:* `agent_common.write_session_log(root / "docs" / "iteration", metrics, output)` writes into the **tracked** evidence directory that the worker path only ever writes *and then commits* (`commit_telemetry(root, tag+session, …, [log_path])` in `run_iteration`). The planner path has no such commit, so a round leaves N untracked `.log` files on trunk. `dispatch.run` reads `ac.working_tree_dirty(root)` at the top of **every** tick and returns `EXIT_PREFLIGHT` ("claims, resumes and merges all need a clean trunk"). A dual-plan round therefore wedges the next dispatcher launch, or its residue rides an unrelated later commit. Secondarily, `write_session_log` does `path.write_text(...)` with no `mkdir`; a root without `docs/iteration/` raises `FileNotFoundError` out of the round.
*Minimal remedy:* mirror the worker path — `mkdir(parents=True, exist_ok=True)` then `agent_common.commit_telemetry(root, <round tag>, "<role> <outcome>", [path])` immediately after the write. (Alternative smaller-but-weaker: write to the gitignored `out/run-logs/`, which loses the durable attribution the slice is for.)

**B2 — `agent_loop.session_meta`: an explicit `null` counter renders as `None`, not unknown**

*Trigger:* a provider result with `usage = {"input_tokens": 100, "output_tokens": null}` — the exact case the guard above it admits.
*Effect:* `usage.get("output_tokens", "?")` returns `None` (the key exists), so the existing `tokens` header column becomes `"100+None"`. This is neither raw nor the declared unknown token, and it contradicts the slice's own stated limitation. `agent_session._result_accounting.raw()` normalises the same field correctly to `""` — two readers of one payload, disagreeing.
*Minimal remedy:* in `session_meta`, `v = usage.get(k); "?" if v is None else v` for both counters (2 lines), or read the already-computed `invocation["input-tokens"]/["output-tokens"]` instead of re-deriving.

**B3 — `agent_session._result_accounting` computes `cost-usd`, `cache-read`, `cache-create`; `write_session_log`'s header tuple drops all three**

*Trigger:* a result carrying `total_cost_usd` and no token keys.
*Effect:* `usage-source=reported`, `usage-status=partial`, `raw-usage` unset (it is only written when token keys are present), and every visible column blank. The durable row asserts partial usage while recording nothing that could be partial — an uninterpretable record, and the one number the attribution slice exists to keep (cost) is computed then discarded.
*Minimal remedy:* add `"cost-usd"`, `"cache-read"`, `"cache-create"` to the header key tuple in `write_session_log` (+3 lines), or stop letting cost alone move `usage-source`/`usage-status`. The first is smaller and keeps the field honest.

**B4 — `agent_common.default_base` widened to return `None`; only one caller audited**

*Trigger:* `claim_base` returns `readable=False` (unreadable `git log`, or `_is_claim_move` returning `None`).
*Effect:* `default_base` now returns `None` on a path that previously required an unborn HEAD. The diff guards exactly one caller (`build_worker_assignment`). Per the module's own ratchet entry, `stale_terminal_assignment` resolves "the same range the loop's `default_base` already named"; a `None` base there yields a malformed `None..HEAD` range — an empty or garbage evidence read, which is the *same defect class* OI84 exists to repair, re-entered through the fix. `agent_loop` also re-exports the symbol.
*Minimal remedy:* either keep `default_base` total (merge-base fallback on `readable=False`) and have `build_worker_assignment` call `claim_base` directly for its fail-closed refusal; or enumerate and guard every caller in this commit. The first is smaller and preserves the pre-existing total contract.

**B5 — `wall-secs` silently changes from integer to float**

*Trigger:* every worker session.
*Effect:* `launch_session` now returns `metrics["wall-secs"]`, which `invoke_session` sets to a bare `time.monotonic()` delta; the deleted code was `int(round(time.time() - wall_start))`. The console line prints `wall=12.348739624023438s`, and the same float lands in the committed log header twice (via `session_meta` and again via `meta.update(invocation)`). Any existing reader that `int()`s the column breaks.
*Minimal remedy:* `metrics["wall-secs"] = int(round(time.monotonic() - started))` at both assignment sites in `invoke_session`. The new tests (`>= 0`) still pass.

**B6 — `_is_claim_move` is a third parser of `git diff --name-status` (Antidote)**

*Trigger:* structural.
*Effect:* `integrate._name_status` exists precisely because "two parsers that disagreed about the tab split or about backslashes would disagree about the facts those authorisations rest on." This commit adds a third, in a second module, with its own `partition("\t")`, its own `replace("\\","/")` and `startswith("A")` matching — and it now authorises the evidence base every completion, assignment and review consumer reads. The dependency direction is already proven by this same diff (`claim_subject` moved down; `integrate` re-exports).
*Minimal remedy:* move `_name_status` into `agent_common` beside `claim_subject`, have `integrate._name_status` delegate, and build `_is_claim_move` on it. This removes the duplication *and* takes ~10 lines off the +95.

**B7 — `[step:smoke]` names a bare `scripts/` path**

*Trigger:* the step running in a scaffolded adopter.
*Effect:* `command = {py} scripts/check_smoke_budget.py` violates the kit-path invariant recorded at WI-509 ("a bare `scripts/bootstrap.py` path an adopter's own repo never has"); the kit lives at `project-trajectory/scripts/`. A repo that does pick this step up reds on a missing file.
*Minimal remedy:* spell the kit-relative path (or whichever placeholder the sibling steps use — `[step:coverage]`'s `{src}` shows substitution exists) and drive it once from a scaffolded destination root before this ships.

---

## Non-blocking findings

1. **Redundant drift guard (Antidote).** `run_loop` calls `moved_scripts_stop()` immediately before `run_iteration`, which calls it again after `wait_out_blackout`. The second strictly subsumes the first; the only thing pinning the first is `test_worker_loop_stops_before_starting_another_session`, which patches out `run_iteration`. Delete the `run_loop` guard (−4 SLOC, one fewer full-tree hash per session) and retarget that test at `run_iteration`.
2. **Fingerprint cost and import-time I/O.** `LAUNCHED_SCRIPTS_FINGERPRINT` is computed at *import* of `agent_common`, so every short-lived sibling CLI and every `load_script("agent_common")` in the suite pays a recursive read+SHA of all `*.py` under `scripts/`. `dispatch._poll` then re-hashes at least once per 0.5s tick plus once per lane event. Lazy-prime on first call (3 lines) if this shows up in gate timing.
3. **`route_tier` lookup.** `registry[route_id].tier if route_id else ""` is an unguarded subscript where the sibling `route_family` is derived defensively; a truthy `route_id` absent from `registry` is a `KeyError` inside routing. Prefer `.get`.
4. **`session-id` semantics change.** `meta.update(invocation)` overwrites the WI-535 column, which `family_context_telemetry` deliberately blanks for non-ANTHROPIC families. `session-id` now populates for every family while `context-*` stays blank, so the header's own documented per-family rule is no longer true of that one field. Reconcile the comment or the write.
5. **`_is_claim_move` root-commit case.** `git diff <sha>^1 <sha>` fails on a parentless commit, which returns `None`, which fails the *whole* assignment closed — on the strength of an unrelated commit whose subject merely matched. Treat "no parent" as "not a claim move" and continue.
6. **`_lane_close` ordering.** The finished-branch guard precedes the new `EXIT_RESTART` arm, so a worker that finishes and *then* trips drift falls through to refresh+integrate. In practice `_arm_code_restart` fires first on the same tick (both read `_SCRIPTS_DIR`), so this is ordering hygiene, not a live hole.
7. **Exit 11 has no shown consumer outside `dispatch`.** IF-015 and the module docstring are amended; `docs/cli-reference.md`'s exit alphabet is not, and no launcher arm is in scope. Given "no hotreload/reexec", an unattended run now stops after any merge touching `scripts/*.py` unless the launcher relaunches on 11. Record this explicitly.
8. **Smoke step overlap.** If `[step:tests]`/`[step:coverage]` already run at or before `DevStg-Tests`, a smoke subset at the same stage is a second red path over a strict subset. Confirm the two `from-stage` values before keeping it. Also note `docs/stack.ini` is adopter-owned and never re-synced, so this step reaches new scaffolds only.

---

## Contract assessment

**No amendment is required; the carrier is already documented.** SR-028's three mechanisms all survive intact and unmodified: typed session outcomes still come from `classify_outcome` (untouched), the zero-HEAD guard still fails closed in `build_worker_assignment` (widened in its trigger set, not weakened in direction), and the all-ERROR→unavailable-agent rung still runs through `stall_stop`/`stall_verdict`. `EXIT_RESTART` never enters any of them: it is not in `END_STATES`, not in `dispatch._WORKER_OUTCOMES`, and never reaches `classify_outcome`. It is a process-lifecycle carrier that parks rather than decides — the same posture as `EXIT_PREFLIGHT` and `EXIT_REVIEW_OWED`, both of which coexist with SR-028 today. Approved LLR-028 sites three mechanisms; three remain.

IF-015 is `Drafted`, and the exit alphabet **is** the declared carrier, so amending it to v4 with `9 · 11` (10 retired) is the correct and sufficient act. What remains is documentation completeness — `docs/cli-reference.md`'s exit table, and the launcher's exit-11 arm — which is a preference for further documentation, not a contradiction with an existing promise. Do not open an SR amendment for this.

**Growth.** The +95/+36/−1 is mostly justified at existing boundaries: the 18 header keys are a flat table with one home, `claim_base`/`scripts_fingerprint` are irreducible new questions, and the −1 in `integrate` is a genuine de-duplication. Roughly 15–25 lines are not: `_is_claim_move`'s porcelain parse (B6), the redundant `run_loop` guard (NB-1), and `session_meta`'s third parse of the same result payload (B2). Take those out and the ratchet entries should be re-stamped downward in the same commit, per that file's own rule.

**Verdict: CHANGES-REQUESTED.** Seven blocking findings, all small and local; the OI84 and OI83 mechanisms themselves are sound and correctly sited. B1 is the one that bites an operator on the next run. This is neither full P0a nor control-window completion, and the record correctly says so.
