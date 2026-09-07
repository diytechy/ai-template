# Independent runtime follow-up — 2026-09-07

Frozen manifest: `26afd9f9e1fa1eff02216bf771972fc30dc5b21d14236ea97823cc617447d2ae`.
Provider: Claude Code, `claude-opus-5`, high effort.
Resumed provider session: `f06a6266-ae23-4c24-b289-878c7612fda9`.
Reported result cost: USD 6.043847499999999, preparation only.
<!-- fig: derived="provider result total_cost_usd from out/run-logs/approval-runtime-followup-opus.jsonl" rev=7ded8e5f+frozen-26afd9f9 -->

## VERDICT: APPROVE (runtime repair) — with stated operational limits

All five majors and all ten minors are resolved in this snapshot. I verified each against the actual new code rather than the disposition text, and re-ran the two modules that were red last round. Nothing I found blocks the supervised retry. This approves no live Status/snapshot cell and no disputed WI-605 judgment.

I could not locate a manifest file inside the snapshot to check `26afd9f9…` against, and I did not read the parent checkout. Everything below is read from this tree and `git diff HEAD` against base `7ded8e5f`. The contract file hashes to `b2c434dd…` as stated.

---

## M1–M5

**M1 — resolved, sufficient.** `_VERIFIED_PUBLICATIONS` is keyed `(resolved root, publication rev, json.dumps(turn, sort_keys=True))` and checked before the expensive path; only successful full proofs are inserted, at the very end of `publication_commit` after tree, parent, receipt, author and close-home all verify. A mutated `turn.toml` re-serializes to a different key and re-verifies. Negative results are never cached. Regression is real and precise (`test_real_return_publish_and_completion_replay`: `calls == []` on a repeat, `calls == [candidate]` on a mutated `primary_root`, and a forged same-trailer commit still resolves to the true rev with one derive). Fresh process audits once — correct.

**M2 — resolved at the right layer.** `_exact_refresh_rels` refuses `seed`, resolves both sets and requires `exact_rels == set(approves)`; `_refresh_targets` returns exactly that set and additionally refuses when no standing record exists; `refresh_refusal` takes the same set as its scope. `_apply_approval` passes `exact_rels=approves`. The widening paths I demonstrated — an out-of-scope registry pulled in by an approving `Status` transition, or by a new row arriving already Approved, both of which `refresh_ledger` and `refresh_refusal` let through — are now structurally unreachable, because `_authorised_registries` is bypassed entirely on this call. Legacy manual callers keep `exact_rels=None` and their existing behaviour. `plan["approves"]` is built only from accepted decisions, so the copied set and `absorption_census`'s registry set are now provably identical.

**M3 — accepted as the owner's boundary, not a defect.** Handoff execution step 2 is explicit that implementation needing governing spine changes hands back to separate exclusive authoring, and `implementation_spine_refusal` is that rule. The route survives: `test_the_merge_slot_mints_the_adjudication_row_at_intake` now runs `claim_repo(..., safety="spine")` and passes, so the post-merge amendment mint is still proven end to end. `test_implementation_spine_boundary.py` pins both sides (ordinary lane refused on LLR `Detail` / TC `Method`; permitted on `CodeSymbol`/`TestRefs`/`Evidence`). I withdraw the finding.

**M4 — resolved.** `tests/test_integrate_station.py tests/test_integrate_admission.py` → **83 passed in 102.05 s**. The `_slot` signature assertion, the amendment-mint fixture and both `_branch_tree_script` patch points are repaired. The downstream-layout half of my concern is answered: `bootstrap.MAPPING` ships `publication_verify.py` beside `integrate.py` (lines 2126–2131), so their physical script directory is identical in every supported scaffold and the resolution order cannot diverge.

**M5 — resolved for this launch; one residual, non-reachable here.** `_machine_author` now requires only `model` and `invocation-id`; `provider`/`roster-row`/`session-id` contribute to the digest when present and are not fabricated when absent. I verified both arms as asked:
- Unmanaged: `session_model(model_map, args.model)` returns `model_map.get("", default_model)`; this repo's `model-map` has no `""` key, so it falls through to `[agent-loop] model = opus` — non-empty.
- Managed: every enabled roster row in `docs/agents.toml` carries a non-empty `model` and a `{model}` template.
- `invocation-id` is coordinator-generated unconditionally in `agent_session.invoke_session` (`uuid.uuid4().hex`), before the runner is called and even on `BaseException`.

The optional-identity handling is correct: absence degrades the digest's discriminating power but `invocation-id` is per-invocation, so replay stays exact and distinct turns stay distinct.

---

## m1–m10

Verified fixed in source: **m1** (`stage_primary_adjudication(..., judgment_path=plan["judgment"])`; `_machine_line_refusal` refuses a primary consolidation with no bound path, and the whole-repo `docs/reviews` glob is now unreachable from it) · **m2** (`_peel_target(root, branch, rev)` — parameter and wrapper deleted; ordinary lanes keep only the verified refresh peel) · **m3** (`_impact_path_class` gives snapshot paths their own class; `_impact_disposition_refusal` requires `amend`/`regenerate`) · **m5** (`SystemExit` caught at the `copy_live` boundary and returned as a refusal, with the candidate-date binding restored in `finally`) · **m6** (`_definition` walks `check_docs.blank_fenced`, so a `##` TOML comment inside a fence cannot become a heading) · **m7** (`_latest_judgment` ranks by the commit that added each log via `rev-list candidate`, takes the strict latest, and refuses on a same-commit tie — the rework-round deadlock is gone) · **m8** (`_project(..., harness_root)` passes the primary checkout to `run_bar`, so the candidate-local `check.py` runs under the real harness interpreter) · **m9** (schema/launch clarification authored and reviewed; contract SHA matches).

**m10** — retained per the owner's requirement. Accepted.

**m4 — disposition is faithful; I accept it as an operational limit.** LLR-207's appended clause is a statement about *committed* state, and it holds exactly: before the commit, HEAD is still `cand` and carries the queued spec and the pending record; the index/worktree are not committed durability. The contract's enumerated kill points (after `turn.toml`, after a verdict, after one of two review phases, after the final commit) do not include the `read-tree`→`commit` staging window, so nothing in the judged contract demands automatic recovery there. Refusing a dirty resume is the same rule `_claim_refusal`, `integrate()` and the dispatch tick-top already apply. Nothing requires automatic recovery.

---

## Nonblocking follow-ups

1. **The dirty-residue stop message is generic, and its first suggestion is destructive in this exact case.** `dispatch.py:1448` says *"commit or stash it, then relaunch."* Stashing is correct. **Committing is not**: the residue moves the queued spec to `docs/archive/work/complete/` and rewrites live registry Status cells, so on relaunch `primary_turn.validate_candidate` refuses permanently — `registry_blobs changed during judgment` (`primary_turn.py:128`) and `_validate_proposal`'s queued-spec requirement — leaving the turn pending forever while `writer_refusal` blocks every claim, merge and `_slot`. Recovery then needs a branch rewrite. Smallest correct boundary, and not automatic recovery: when the tree is dirty *and* `primary_publication.pending(root)` returns a turn, name the turn and print the reconcile instruction (derive the projection at HEAD, compare against the residue, then `git reset --hard <candidate>`), and do not offer "commit". ~5 lines in `dispatch.run` reusing an existing call. **Operational limit if left as-is: the supervisor must never commit or stash-drop primary residue while a `turn.toml` is pending.**

2. **`_effects` still derives the author before the RETURN branch,** so any future configuration where `model` or `invocation-id` is empty makes even a RETURN unpublishable and wedges every primary writer. Not reachable in this repo (verified above), but the precondition *"every ADJUDICATE-eligible route carries a non-empty model"* is undocumented and unenforced at preflight.

3. **M1's residual per-tick cost.** `publication_commit` still runs a full-history `git log --fixed-strings --grep` on every call — **0.24 s** measured over this repo's 3558 commits — once per completed turn record per `_admit` tick (idle sleep 0.05 s). Fine now; it grows linearly with completed adjudications. Separately, negative results are deliberately uncached, so a commit carrying a valid-looking `Primary-Publication-Turn:` trailer that fails verification costs one full ~15 s `derive_tree` per tick for as long as it is reachable.

4. **`Module` has no test on either side of the spine boundary.** The disposition rules it governing, which is the cell this repo's own workflow touches on every new-file WI — the change set itself re-points it on seven LLR rows. Worth pinning with a case, and worth entering as an accepted process cost: every ordinary implementation WI that adds a file now needs a paired exclusive spine WI to record its `Module`.

5. **Coverage moved, not lost, but thinned.** Three lane-level no-bar tests in `test_integrate_station.py` were replaced by unit assertions on `_outside_adjudication_scope` plus a direct `run_bar` call. The end-to-end no-bar decision is covered in `test_primary_publication.py` instead; noting the shift so it is a choice rather than a drift.

---

## Launch readiness

No launch-blocking defect remains. Two checks I ran that bear on the launch itself:

- **`schedule.py ready`** confirms the supervisor's claim without any preselection API: `WI-582` (`safety_class = "spine"`, rank 0, exclusive) is the first admission and takes an ordinary lane; `WI-605` (rank 1, `down=1 path=1`) is the first *primary* selection, reached through `_admit_frontier`'s existing `kinds.get(payload[0]) == "adjudication"` arm.
- **Post-publication freshness does not red.** `gen_trajectory.ASOF_RE` has always excluded the as-of stamp from the `--check` compare (`gen_trajectory.py:1065–1067`), and `derive_stage --check` compares `kitstage.field_block`, which excludes the rendered `# computed … (as-of …)` header. `docs/stage`'s fingerprint does move on a publication — and `trunk_step --regen` regenerates it *inside* the projection, so the publication commit lands fresh. The disposition's claim is accurate.

## Tests actually run this round

| Command | Result |
|---|---|
| `pytest -q tests/test_integrate_station.py tests/test_integrate_admission.py -p no:randomly` | **83 passed, 102.05 s** |
| `pytest -q tests/test_module_size_ratchet.py -p no:randomly` | **3 passed, 1.15 s** (honest restamp confirmed) |
| `schedule.py --root . ready` | frontier ordering above |
| `time git log --fixed-strings --grep=<token>` | 0.24 s over 3558 commits |
| `shasum -a 256` on `APPROVAL-REPAIR-CONTRACT.md` | `b2c434dd…` — matches |

Per instruction I did **not** run the full unfiltered suite, the smoke tier, or `check_smoke_budget.py`, and did not re-run the architecture, complexity, import, baseline, primary-approval/brief/session or primary-publication modules — I relied on your stated focused results for those and verified each fix by source reading. The 90 s enforcement measurement on a quiet box remains owed. My earlier three smoke failures were, as you say, the private-file omission and a then-stale ratchet; the ratchet is green here and I did not re-measure the tier.
