# Independent runtime review — 2026-09-07

Frozen manifest: `73382f84347c97c0f9203c9babd70391ded6c1669649333f866bbce095305288`.
Provider: Claude Code, `claude-opus-5`, high effort.
Session: `f06a6266-ae23-4c24-b289-878c7612fda9`.
Reported cost: USD 8.2929315, preparation only.
<!-- fig: derived="provider result total_cost_usd from out/run-logs/approval-runtime-opus.jsonl" rev=7ded8e5f+frozen-73382f84 -->

## VERDICT: CHANGES-REQUESTED (runtime repair)

The architecture is right and most of the hard parts are done well. Five defects block acceptance; two of them (F1, F2) defeat the repair's own stated guarantees, and four tests are red in the delivered tree.

No live spine approval performed. No edits, commits, pushes, coordinator launch or snapshot approval. Design judgments below approve no WI-605 cell.

---

## What holds up (verified, not assumed)

- **Branchless selection/resume binding is sound.** `primary_turn.validate_candidate` proves the record's unique creating commit via `log --diff-filter=A` + single-origin + `%P == base`, re-reads the record blob at both origin and candidate, requires live *and* approved registry blob maps equal at base **and** candidate, requires the spec definition outside `## Approval`/`## Dispositions` to be byte-equal to the proposal, and allows only `turn["spec"]` plus `verdict.is_record_path` paths to change. `_primary_identity` refuses a linked worktree and detached HEAD.
- **Every worktree approval/snapshot bypass I could find is closed.** `baseline_snapshot.copy_live` raises on `is_linked_worktree`; `staged_snapshot_findings` refuses linked-worktree snapshot staging; `merge_approval_refusal(root, base, head)` no longer takes an actor/scope argument and `adjudication_approval_refusal` is deleted; `integrate._claim_specs_refusal` refuses an adjudication claim branch and `_admit_parked` refuses an obsolete one. The `_primary_merge_snapshot_sync` exception is genuinely narrow — MERGE_HEAD must be an ancestor of the live primary HEAD, the index must equal MERGE_HEAD across the *whole* snapshot dir, paths must be in the merge delta and absent from the worker delta, and each source snapshot must be proven equal to live at its own writing commit; every unreadable question answers false.
- **RETURN/UNCERTAIN are genuinely zero-effect.** `_effects` returns empty `statuses`/`approves`, so `_apply_approval` no-ops and no snapshot is written, while close + successor mint still run.
- **Author/committer split preserves SR-140 without a cell change**; `_status_projection` refuses `human_approves_spine` registries and surfaces them rather than automating them.
- **Replay is exact on the real generators, not just fixtures.** I cloned HEAD twice (`--shared --no-checkout`, detached) into two *different-length paths* and ran `trunk_step.py --regen`: identical `write-tree` `29699e9c…`. The two date-bearing artifacts derive from the candidate commit (`derive_stage.py` uses `git log -1 --format=%cs`; `PROJECT_STATE.html` renders "as of commit \<sha\> · \<commit date\>"), not wall clock — so a replay tomorrow reproduces the same bytes. `trace.py`'s `date.today()` is on `--mint-approval-brief` only, which regen does not call.
- Import graph acyclic, all six new modules import standalone, `test_trajectory_arch.py` + complexity ratchets: **145 passed**.

---

## MAJOR

### M1 — The completion replay runs on every dispatcher tick; one published turn wedges the coordinator
`dispatch._admit` (called every loop iteration; idle sleep is `0.05 s`) → `primary_adjudication.pending` → `primary_publication.completed` → `publication_commit` → **`derive_tree`**, which does a full `git clone --shared`, `checkout --detach`, the whole projection including `trunk_step.py --regen`, `write-tree`, `commit-tree`, and a **`git fetch` of the carrier back into the primary object store**.

Measured on this repo at HEAD: clone+checkout **0.82 s**, regen **14.02 s** — ~15 s per tick, per completed turn. `turn.toml` records are immutable and never pruned, so cost is O(all completed adjudications) forever. Same path is on `integrate._slot` and `integrate._claim_refusal` via `writer_refusal`. If any publication took the product-bar arm, the replay additionally re-runs `check.py --jobs 0 --trunk-lane` (~11 min) on every tick.

Failure scenario: publish WI-601. From the next tick on, the idle coordinator spends 100 % of wall clock re-deriving a finished publication and appending a fresh dangling commit to `.git` every 15 s; a second completed turn doubles it. Nothing in the change bounds this.

Direction: `completed()` is the hot predicate and `publication_commit()` is the audit. Short-circuit `pending()` on a cheap immutable fact (the publication commit id / a reachable trailer match) and keep the exact byte replay for the verifier and for the one-time transition into `publish`.

### M2 — `copy_live`'s actual write set is wider than the absorption ledger's census
`_apply_approval` → `baseline_snapshot.copy_live(root, approves=plan["approves"])`. The write set is `_refresh_targets` → `_authorised_registries` = `approves` **∪ every registry with an approving `Status` transition ∪ every registry gaining a new row that already claims approval**. `primary_approval.absorption_census` censuses only `{registry for registry, _ in accepted}`. And `refresh_refusal` exempts a registry whose ledger has any flip (`e["absorbed"] and not e["flips"]`) and `refresh_ledger` skips new rows entirely (`if before is None: continue`).

Failure scenario: WI-604's turn scopes `LLR-210, TC-208`. `docs/requirements/interfaces.toml` (out of scope) already differs from its snapshot by (a) IF-200 whose Status crossed into Approved and (b) IF-100 whose approved `Contract` prose was amended. `_authorised_registries` adds interfaces.toml on the flip; `refresh_refusal` returns `""` because that entry has flips; `copy_live` copies the whole file; `absorption_census` never looks at it. The publication commits an approved-baseline change covering IF-100 and IF-200 with **no decision, no judgment ref and no ledger row** — precisely the "a whole-registry copier must not absorb pending, unapproved cells outside the accepted change" rule from WORK-FLOWS, and the rule LLR-158's amendment says the primary writer "must bind … complete absorb ledger". The even easier variant needs only a new already-Approved row in any out-of-scope registry.

This is also a regression against what was deleted: `adjudication_approval_refusal` enforced registry-set equality with explicit `WIDENED` / `WITHOUT ITS ANCHOR` arms. Nothing replaced that.

Direction: compute `baseline_snapshot._refresh_targets(...)` inside `approval_projection` and refuse unless it equals exactly the accepted-decision registry set (or run `absorption_census` over every registry the copy would write).

### M3 — `implementation_spine_refusal` refuses the trace-binding edits it claims to allow, and severs the amendment-routing arm
`_IMPLEMENTATION_TRACE_CELLS` permits LLR `{CodeSymbol, TestRefs}` and TC `{Evidence}`. `SPINE_TRACED_CELLS` rules LLR `{Module, CodeSymbol, TestRefs, Component, Phase, SR-Refs, Hat-Refs}` and TC `{Verifies, Evidence, Automated, Phase}` as traced. So an ordinary implementation WI that adds a source file and re-points its LLR `Module` cell is refused at merge — **the exact edit this change set makes to seven LLR rows** (`LLR-140`, `152`, `153`, `154`, `158`, `167`, `207` all gained `module = …;primary_*.py`). Row additions/removals in any of the four spine registries are also refused outright for non-`spine` branches (`before is None or after is None`).

Reproduced: `tests/test_integrate_station.py::test_the_merge_slot_mints_the_adjudication_row_at_intake` now fails with
`implementation work amended governing spine content outside an exclusive SafetyClass=spine authoring WI (docs/requirements/system-requirements.csv SR-001 (Requirement))`.
That test is the *preserved* WI-388 post-merge arm: an ordinary lane amends an Approved SR cell without a flip and the slot mints an amendment adjudication. Under the new rule that merge never lands, so `intake._routed_amendments` / `_amendment_drafts` / the amendment brief — whose prose this same change set rewrites — become unreachable from ordinary work. Either the rule over-reaches or the routing arm was silently retired; neither is stated.

### M4 — Four tests red in the delivered tree, all in Full/CI-tier modules the smoke bar does not see
| Test | Cause |
|---|---|
| `test_integrate_station.py::test_slot_acquisition_has_exactly_two_approved_call_sites` | The test was **rewritten by this change** (its comment names the primary turn) yet still asserts `"def _slot(root)" in src`; the signature is now `def _slot(root, *, primary_turn=False)`. |
| `test_integrate_station.py::test_the_merge_slot_mints_the_adjudication_row_at_intake` | M3. |
| `test_integrate_admission.py::test_the_branch_trees_copy_wins_under_the_invokers_layout` | `integrate._branch_tree_script = publication_verify.branch_tree_script` resolves against `publication_verify.SCRIPTS`, not the integrator's. |
| `test_integrate_admission.py::test_a_branch_tree_without_the_script_falls_back_to_the_invoker` | same. |

The `_branch_tree_script` extraction is behaviour-neutral **in this repo** (both `SCRIPTS` are `project-trajectory/scripts`), but for an adopter whose harness sits elsewhere (`kit/scripts`, the shape the test names) the branch tree's own copy no longer wins — that is the WI-368 defect returning, and its guard is now un-monkeypatchable. This is the kind of change CLAUDE.md asks to be flagged as forcing downstream migration.

### M5 — Publication is impossible without full route/session provenance, and the failure wedges the station with no in-band escape
`_machine_author` requires **all five** of `provider / roster-row / model / session-id / invocation-id` from **exactly one** ADJUDICATE log. `launch_session` sets `provider = plan["route_family"] or ""` and `roster-row = plan["route_id"] or ""` — both empty on the unmanaged-routing arm; `agent_session` leaves `session-id` empty for any provider that does not report one. `_effects` computes and requires the author **before** the RETURN branch, so even a RETURN cannot publish.

Failure scenario: a repo (or a route) without a routing registry admits a queued adjudication. `begin()` commits `turn.toml`. Every projection returns `no unique committed ADJUDICATE judgment and route/session identity bind this candidate`, so `worker_endstate` never reaches DONE, `primary_adjudication.run` returns `EXIT_PREFLIGHT`, and the dispatcher exits. `writer_refusal` now blocks every claim, merge and direct integration. Each relaunch burns a full adjudication session and exits again. The record is immutable by design, so recovery means hand-`git rm`-ing a committed `turn.toml` — undocumented and contrary to the contract. LLR-167 as amended explicitly says both routing arms take this path.

---

## MINOR

- **m1 — `primary_close._consolidation_close(root, root, "", …)`** passes an empty branch, so `_lane_verdict` globs `docs/reviews/*-ADJUDICATE-*.md` across the *whole primary checkout* and takes the lexicographic maximum. Verdict names are `<session>-ADJUDICATE-<sha7>.md`, so that sort is not chronological and the winner is an arbitrary historical verdict from an unrelated WI, which `_machine_line_refusal` then reconciles against this turn's `## Consolidation` record. On a branch the reader was scoped by `trunk...branch`; that scoping is gone. Spurious refusal, or a false pass on a coincidentally-compatible OUTCOME line.
- **m2 — `primary_publication.governing_identity` / `peel_target` are dead code.** The three production callers of `kverdict.governing_identity` (`agent_loop.py:3729`, `dispatch.py:158`, `integrate.py:1299,1391`) are all WI-branch-scoped and none passes `publication_peel`. `grep` finds no caller of the primary-aware wrapper and no test touching `publication_peel`/`peel_target`. Answering the architecture question directly: **no actual caller needs primary-aware identity today.** Either delete the wrapper and the injected parameter, or state which reader is owed the wiring.
- **m3 — `_impact_refusal` forces `history-unchanged` for everything under `docs/archive/`,** including `docs/archive/last_approved/…` — the snapshot files the same publication rewrites. A `meaning` decision must assert its own snapshot copy is historical and unchanged.
- **m4 — Crash window between install and commit.** `publish` does `read-tree --reset -u <tree>` then commits. A kill in that window leaves primary dirty with no publication; `primary_turn.validate`, `publish`'s clean check and the dispatch tick-top dirty check all then refuse, so resume needs a manual `git reset --hard`. LLR-207's appended "before the final commit the queued spec and pending record remain" is not true for that window. (Hook failure and post-commit are handled and tested — `test_real_return_publish_and_completion_replay` covers a `pre-commit` exit 1 with clean rollback.)
- **m5 — `SystemExit` escapes the refusal path.** `baseline_snapshot.copy_live` raises `SystemExit` on `refresh_refusal`; `derive_tree`, `publish` and `primary_adjudication.run` catch only `(KeyError, OSError, RuntimeError, ValueError, TypeError)`. An unauthorised-refresh refusal terminates the coordinator process instead of returning a refusal that retains the turn — and per M2 that is a reachable outcome.
- **m6 — `primary_turn._definition` splits on `^## ` with `re.M`, ignoring fenced blocks.** A `##`-prefixed comment inside the `## Approval` TOML fence re-partitions the definition and yields a false `judgment changed the proposal outside Approval/Dispositions`. Fail-closed, but a dead end for a payload the template itself invites the model to write.
- **m7 — Author derivation is brittle across rework rounds.** `_judgment_records` keeps only logs whose recorded candidate has the *same non-record tree identity* as the final candidate, and `_machine_author` requires exactly one. A rework round that lands the payload back on a previously-logged tree identity (a fix, a refusal, a revert to earlier bytes) leaves two qualifying logs and permanently refuses publication; the logs are committed and cannot be removed.
- **m8 — The product-bar arm is untested and fragile in the disposable clone.** `run_bar(Path(root), Path(root), tier)` is called with the scratch clone as both `wt` and `root`, so `ac.harness_python(scratch)` finds no `.venv` and silently falls back to `sys.executable`; `harness_floor_failures` is not consulted. Compounded by M1.
- **m9 — `## Approval` schema diverges from the reviewed contract.** The contract's `absorption.cells` is `{cell = "<before> -> <after>"}` and `[[decision]]` carries no `registry`; the implementation requires `registry` on `[[decision]]` and a nested `{cell = {before=…, after=…}}`. Code and prompt template agree with each other, so this is a contract-text divergence to reconcile, not a runtime bug.
- **m10 — `publication_verify.ADJUDICATION_SURFACES` is wider than LLR-152's amended allowlist** (`docs/work/`, `docs/archive/work/`, `docs/reviews/`, `docs/log.d/`, `docs/handbacks/` prefixes vs "the queued spec's reviewed `## Approval` bytes, in-scope registry cells, named snapshot files, that spec's move, parsed successors and id-watermark"). Not currently exploitable — the projection is derived — but the no-product-bar decision is not the narrow derivation the amendment describes.

## Scope items checked and found faithful

- **No-product-bar scope**: preserved and correctly rehomed onto the projection (`_outside_adjudication_scope` → `run_bar` only on escape), with the verification receipt recorded in the commit message and re-checked in `publication_commit`. Modulo m10.
- **WI-605 migration**: same WI, same spec, `active/ → queued/`, `adjudicates = ["SR-161","LLR-183","TC-178"]` added, one copy only, no accepted cells, preserved branch/patches explicitly labelled incident evidence. The supervisor clarification narrows rather than widens scope. Deviation to note: the contract's "one reviewed trunk commit … creates its immutable `turn.toml`" is not implemented (no `docs/reviews/primary/`); the record is minted at `begin()`. I think that is the *better* choice — a pre-minted base would be invalidated by every subsequent repair commit — but the contract's migration verifier is therefore unimplemented and should be re-worded rather than silently dropped.
- **WI-601/603/604/606 scopes**: exact scopes preserved; only the outcome prose retargets the copier→publisher, plus `adjudicates` keys added to 601/603. WI-606 keeps its dependency on WI-605 and its explicit six-row limit. Nothing approves a disputed cell.
- **Absorption/Drafted riders**: `absorption_census` classifies correctly and `_absorption_refusal` blocks the whole file on any `UNJUDGED` or any `approved-change` outside `accepted` — so WI-605 will RETURN, which is the right answer.
- **Engine reuse / telemetry / rework / restart**: `session_body` forks to `compose_primary` on `worker["primary_turn"]`; `session_binding` writes `primary-turn` / `judgment` / `candidate` into the session log and `write_session_log` allow-lists them; `commit_telemetry` commits the log immediately, and `docs/iteration/` is a `RECORD_PREFIX`, so the telemetry commit does not stale the tree identity the judgment names. `completion_refusal` feeds the projection refusal back as rework rather than closing. `main(args, primary_turn=…)` correctly skips the coordinator lock (already held by the dispatcher).

---

## Tests actually run (`.venv/bin/python`, this frozen snapshot)

| Command | Result |
|---|---|
| `pytest -q tests/test_primary_{adjudication,approval,publication,session}.py tests/test_implementation_spine_boundary.py tests/test_kitlib_git.py` | **55 passed, 41.33 s** |
| `pytest -q` over the 10 modified test modules | **4 failed, 431 passed, 326.55 s** (M4) |
| `pytest -q -n auto -m smoke` | **3 failed, 1690 passed, 4 skipped, 91.69 s** |
| `pytest -q tests/test_trajectory_arch.py tests/test_complexity_ratchet.py tests/test_check_complexity.py` | **145 passed, 24.25 s** |
| Two-path `--shared` clone + `trunk_step.py --regen` × 2 | identical `write-tree 29699e9c…`; clone 0.82 s, regen 14.02 s |

The three smoke failures are **not** repair defects and I discount them: `test_dogfood_sync::test_scaffold_mapping_covered_or_declared` and `test_mapping_purpose::test_real_mapping_has_no_gate_class_findings` both fail only on `OWNER_SCRATCHPAD.md` being absent — an intentional property of this review snapshot — and `test_module_size_ratchet` is the acknowledged stale re-stamp (`agent_common 1456→1459, agent_loop 2707→2731, bootstrap 1665→1677, intake 1452→1455`, `integrate 1416→1358`), which confirms the claimed net monolith reduction. Note the wall reading: **91.69 s against the declared 90 s ceiling** on a loaded box — one data point, and the budget is not moved to fit it, but the enforced measurement is still owed.

## Limits of this review

Read-only, frozen snapshot, no OWNER_SCRATCHPAD.md. I did **not** run the full unfiltered suite, `check_smoke_budget.py --mode enforce`, the docs/byte-budget checks, or any real provider route. M1's per-tick cost is derived from the code path plus a measured 14.8 s replay on this repo, not from an instrumented live coordinator run. M2 and M5 are reasoned from the code with the reachability argument given; I did not build a fixture to execute them. I did not review the PROCESS.md / PROCESS_OPTIONS.md / skill prose deltas beyond confirming they match the runtime, and I made no judgment on the disputed WI-605 governing cells.
