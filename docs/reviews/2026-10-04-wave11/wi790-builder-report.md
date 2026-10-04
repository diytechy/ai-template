# WI-790 builder report (Claude Opus kit-builder, 2026-10-04) — the spine change list

The builder edited no spine registry. Every item below is a CLAIM to confirm against the code (lane commit 10497d7c).

## `Implements:` tags added
SR-148/LLR-288 on the schedule functions; SR-148 only on the new kitlib/spine, check_trajectory, acceptance_record, check and integrate functions (they wait for new LLRs); SR-174/LLR-153 on the two intake functions; SR-168/LLR-198 on `pending.open_item_queue`; SR-225/LLR-283 on `pending.decisions_to_review`, the gen_open_items decision functions and the new kitlib.decisions symbols; SR-049/LLR-118 on the three new gen_open_items card functions; SR-054/LLR-115 on the Next-work helpers; SR-010/LLR-010 on `bootstrap.file_stack_placeholder`; SR-189/LLR-215 on `kitlib/spine.HISTORICAL_KEYS`.

## Existing rows
- **IF-073** — now `data = "status: pending | ruled; wi_refs: work items waiting on this ruling"`. Must say: status pending or ruled; no work-item pointer; `wi_refs` is historical metadata no reader uses. State the rule (with IF-054): every pending item is filed with a queued row citing it, and ruling updates citing rows in the same commit (Done-when with criteria citing the item, a real specref, other fields where they change, the confirmation criterion). Drop `scripts/schedule` from `consumers` (the scheduler reads statuses through trace (IF-176) and titles through IF-265).
- **IF-074** — now `data = "docs/open-items.html ... pending decisions, approval and re-attest chains, verdict-named re-attestation audit, pending owner actions"`. Must add: only cited pending items appear, beside their citing rows; the integrity notice for uncited items; "Decisions to review" last.
- **IF-054** — now `data = "status; work-item needs edges (a ~ prefix is soft); IF-073 owner gates; absent safety class = unclassified"`. Must say: `needs` carries work-item edges and `OI-###` edges; a pending item blocks the row; the placeholder minimum; the same-commit ruling rule.
- **IF-176** — still true; optionally drop the "legacy" framing in TC-253's context.
- **IF-264** — now `data = "work rows and IF-073 gates -> readiness records carrying gating ids and titles"`, rationale "...without changing the work-item format." Must say: work rows' `needs` OI edges become blocked records naming each unmet item. The rationale is now untrue (the format is the edge).
- **IF-265** — still true; its rationale ("scheduling gates") could say "the titles of cited items".
- **IF-164** — now `data = "docs/status.md ... derived stage, spine counts, the ready frontier"`. Must add: the open items a queued row cites (and which rows they hold), uncited items, the Decisions-to-review count, and the Blocked list.
- **LLR-058** — now "The ready set contains exactly the WIs whose hard predecessors are done...". Must add: an `OI-###` edge is met when the item leaves pending; otherwise the row is blocked, the item named.
- **LLR-288** — now "Load IF-073 gates into internal scheduler data. ... A ruled gate releases the row without editing it." Must say: gates come from the row's `needs` OI tokens; blocked rows name each item; a row with both edge kinds keeps its waiting reasons; ruling releases readiness. Add `_open_item_holds/_held_disposition` to `code_symbol`.
- **LLR-289** — RETIRE: `open_item_wi_ref_findings` is deleted; `wi_refs` is no longer resolved.
- **TC-253** — approved, its evidence still passes; optionally drop "legacy".
- **TC-301** — now method "...hold a queued row through a pending open item's wi_refs...ruling...spec unchanged...". Must say: hold through `needs = ["OI-98"]`. Evidence remains `tests/test_open_item_readiness.py`.
- **TC-302** — RETIRE with LLR-289 (its evidence functions are gone, except `test_only_queued_rows_are_held_and_a_drained_frontier_still_lists_gates`).
- **LLR-118** — now "renders (a) every pending row of docs/requirements/open-items.toml as a decision brief". Must say: only rows a queued item cites, plus the integrity notice and "Decisions to review". Add `_brief_cards/_brief_card/_uncited_notice` to `code_symbol`.
- **TC-123** — now "assert a pending registry row renders as a brief and a RULED row does not". Must add: uncited items are a notice, not a card. Evidence `tests/test_open_item_queue.py`.
- **LLR-153** — now "context_block renders the pure registry joins (... pending OIs ...)". Must say: pending OIs the row's kin cite in `needs`; the disposition mint writes the OI id into the successor's `needs` and supplies the registry specref. Add `_inject_open_item/_pending_oi_lines` to `code_symbol`.
- **TC-147** — must add: a handback `[open_item]` yields a queued, blocked successor citing the item, and the context block ignores `wi_refs` (evidence in `tests/test_intake.py`).
- **LLR-010** — now "Writes the mapped kit files ... runs green out of the box." Must add: a non-Python profile's OI-3 is filed with its queued placeholder WI-001 and both watermarks are raised. Add `file_stack_placeholder`.
- **TC-010** — must add that a node scaffold is green under `check_trajectory --strict`; evidence `tests/test_profile.py::test_the_scaffolded_oi3_is_filed_with_its_queued_placeholder`.
- **IF-255** — `data` must add the optional `reviewed` key; its `notes` "no reader judges a review cell" is now untrue.
- **IF-256** — `data` must add `reviewed_state(value)` and `review_queue(text)`.
- **SR-225** acceptance — must add that an unrecognized `reviewed` value is reported as a format finding, and that the owner surface lists entries not marked reviewed (R2: no script names in the SR cell).
- **LLR-283** — must add the `reviewed` vocabulary, the finding, and `review_queue`. Add `REVIEWED_KEY/REVIEWED_TRUE/REVIEWED_FALSE/reviewed_state/review_queue` to `code_symbol`.
- **TC-293** — must add the reviewed-key cases. Evidence `tests/test_decisions_to_review.py`.
- **WI-205's backlog-staleness rows** (ids not located by the builder) — must add that a registry `specref` is clocked per cited item; evidence `tests/test_ruling_sync.py::test_a_registry_specref_is_clocked_per_cited_item`.
- **What pins the disposition brief's open-item clause** — `tests/test_prompts.py::test_disposition_brief_makes_the_successor_the_open_items_placeholder`, renamed from `..._through_open_item_wi_refs`; any TC citing the old name must be updated.
- **What pins the snapshot's lists** — `tests/test_open_item_queue.py::test_the_status_snapshot_lists_the_same_projection`.
- **LLR-198** — add `open_item_queue/decisions_to_review` to `code_symbol`. **LLR-115** — add the Next-work helpers (`_blocked_item`, `_waiting_item`, `_next_work_item`, `_next_work_none`). **LLR-215** — add `HISTORICAL_KEYS`.

## New rows needed
- **The sync ERROR (an LLR + a TC).** Modules `acceptance_record.py`, `check.py`, `integrate.py`; symbols `ruling_sync_lines/_sync_lines/_ruled_items/_citing_rows/_sync_gap/_tree_specs/staged_ruling_sync_lines/commit_ruling_sync_lines`, check's `_ruling_sync_refusal/_ruling_sync_mode`, and integrate's `_ruling_sync_refusal`. TC evidence: the six case tests in `tests/test_ruling_sync.py`.
- **The uncited-pending ERROR and the specref state check (an LLR + a TC).** Modules `check_trajectory.py` and `kitlib/spine.py`; symbols `uncited_open_item_findings/open_item_specref_findings` and `open_item_queue/_pending_items/_held_rows`. TC evidence: `tests/test_open_item_readiness.py::test_an_uncited_pending_item_is_an_error_even_with_no_work_items`, `::test_a_ruled_items_row_may_not_keep_the_registry_as_its_specref`, `::test_a_placeholder_row_passes_every_check_and_is_blocked`, and `tests/test_open_item_queue.py`.
- **Possibly an IF row** for `pending`'s carrier read: to avoid an undeclared crossing (pending -> spine_carrier) the builder routed it through `traj_parse.ct.spine_carrier`; a declared seam would be cleaner.
- **This WI's `sr_refs` and `specref`:** suggested `sr_refs = ["SR-148", "SR-225", "SR-049", "SR-010"]` and `specref = "docs/requirements/interfaces.toml#IF-073"`.

## Builder's open points
- The carrier route for `pending.py` (above).
- TC-302 and LLR-289 still cite a deleted symbol and deleted tests; `check_trajectory --strict` and `trace.py --strict` did not flag either.
- The new git-backed tests add about 6.5 s serial to the smoke tier (18.6 s at -n auto).
