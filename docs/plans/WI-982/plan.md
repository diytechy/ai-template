# WI-982 plan: both adjudication routes widen a sitting's hats by the authoring work item's tags

Planner: fresh session, 2026-11-04, at lane tip `de3838360`. Read in full: the spec `docs/work/active/wi-982/WI-982-minted-row-carries-authoring-tags.md` and its specref `docs/reviews/wi-976/004-ADJUDICATE-81e623b.md`. SR-161, LLR-360 and TC-399 were read as rows. Findings below were confirmed against the code at this tip.

## What the build changes, in one paragraph

The mint gains one cell and the hat composer reads it. `intake` works out the authoring tags once per mint and hands them to its two drafters, and `_draft_row` writes them. `hats.context_from_work_item` reads a non-empty cell in place of `Workstream` and `SafetyClass`. Nothing else changes: the routing `SafetyClass` stays `adjudication`, and `Workstream` stays `process`. `compose_lane.py` already hands the authoring row, so the in-lane route needs no edit, and its docstring's claim that it reads "the brief the merge's mint would hand a sitting" becomes true.

## Design decisions the rows depend on

1. **Names.** The column is `AuthoringTags`, after `Adopted`, in the existing `SafetyClass` / `safety_class` pattern. The frontmatter key is the spec's `authoring_tags`, a TOML array through `SPEC_LISTS` and `LIST_FIELDS`, as `adopted` and `adjudicates` are. The cell reads `;`-joined. I checked the join against the registry: none of the 18 workstreams or the 8 non-empty SafetyClass values on the 997 rows contains `;` or `,`, so `hats._as_tags` cannot split a value.

2. **One reader, used by the writer too.** The spec names `hats.context_from_work_item` as the only reader and says "a minted row that authors another passes its cell on". Both are satisfied if the mint takes each authoring row's tags from that same function: the function already answers "the tags this row widens by", cell first. `intake` therefore imports `hats`, and no second reading of the cell exists. The function already takes either spelling of a key, so it reads the lower-case frontmatter `_closed_spec` returns, once `authoring_tags` joins `AuthoringTags` in `_first`.

3. **The route test is `branch`, not `outcomes`.** `--with-terminal` and a bare sweep hand a full `outcomes` map, so `outcomes` alone would stamp every close on file. `_cmd_sweep` already passes `claim = args.branch if args.merged else ""`, the merge slot always passes its branch, and `--merged` refuses without one. So `branch` is non-empty exactly when a route names the authoring rows, which is the spec's closed list. The helper, in `intake.py`:

   ```python
   def _authoring_tags(root, outcomes, branch):
       if not branch:
           return []
       closed = [_closed_spec(root, wi, tuple(SWEEP_OUTCOMES)) for wi in sorted(outcomes or ())]
       tags = [t for hit in closed if hit for t in hats.context_from_work_item(hit[1]).get("tags", ())]
       return list(dict.fromkeys(tags))
   ```

   It needs the three `SWEEP_OUTCOMES` folders because `_closed_spec`'s default pair omits `complete/`, the usual close. Sorted ids make a union deterministic.

4. **Drafter signature.** `_amendment_drafts` and `_first_approval_drafts` take `authoring_tags=()`. The default keeps `scripts/coordinator/preview_mint.py` and the existing three-argument test calls as they are, and an empty value is the spec's own default case. `intake_after_merge` computes the tags once and passes them to both.

5. **`_DRAFT_KEYS` does not gain the key.** A `## Dispositions` block carrying `authoring_tags` keeps being refused as an unknown key, which is what keeps the two drafters the only writers.

6. **Bounds, stated so they are not silent.**
   - A row already minted keeps its cell. The exact-title dedup means a later `--merged` sweep over a range a branchless sweep already minted writes nothing, and rows standing at this landing widen by their own tags. No backfill is planned, because the spec promises only what these routes mint.
   - A merged spec that cannot be read already refuses the same all-or-nothing mint in `_merged_dispositions` (WI-969). A `partial/` or `cancelled/` spec that cannot be read contributes no tags, and `_authoring_tags` adds no refusal for it. A malformed closed spec on trunk needs the commit hook bypassed, so it sits outside PROCESS.md §6's review threat model.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. The spec's S5 answer holds, with one addition: the writer's new call into `hats` (step 4).

1. **Mode classes (A2): none added.** The mint and the composer stay stateless functions of their inputs. Flow 6 in `docs/runtime-flows.md` reads "a decomposition round's judging brief reads the applicable hats' questions", which stays true, and no flow names a row's tags, so no flow is edited.

2. **Value domains (A3, A6): one added, carried by P1.** The new domain crosses IF-092 and rides the IF-023 carrier. Its cases are disjoint and cover every mint:

   | Case | Holds when | Reader's result |
   |---|---|---|
   | empty | no route named an authoring row, or the named rows carry no tags | the row's `Workstream` and `SafetyClass`, as today |
   | tags | a route named rows carrying tags: their values, deduplicated, `;`-joined | those tags, in place of the two cells |

   By route:

   | Route | Source | Cell |
   |---|---|---|
   | merge slot | the closed rows its `outcomes` name | their tags |
   | `sweep --merged ... --branch` | the named rows | their union |
   | range sweep with no `--merged`, with or without `--with-terminal` or `--branch` | none | empty |
   | bare sweep | none, and it reads HEAD..HEAD | mints neither row kind |

   IF-092's `data` cell records this in P1, inside §8's 160-character limit. IF-023 states no key list ("one Markdown spec per row"), so its text does not change.

3. **Output against input (A4): one new cell, and one new output.** Recorded here, as the skill allows when planning:

   | Output | Inputs today | Input added |
   |---|---|---|
   | a minted row's hat block (`plan_briefs.sitting_hat_block`) | the row's `Workstream` and `SafetyClass`, the parent needs, the roster | `AuthoringTags`, in place of the two cells when non-empty |
   | a minted row's `AuthoringTags` (new) | none | `outcomes`, `branch`, each closed row's tags |
   | routing, `Brief`, `Adjudicates`, `SR-Refs` | unchanged | none |

4. **Boundaries (A6, A8): no new boundary interface.** `intake` calling `hats` is a new import edge, and it is not a new component crossing. `docs/requirements/components.derived.toml` places both modules in CMP-006 and in CMP-008, and PROCESS_OPTIONS.md's rule ("A cross-component edge needs a declared seam") covers only edges between different components. `plan_briefs` calls `hats` under the same terms, with no row. The rank table in `tests/test_import_layers.py` is unaffected: `hats` is outside the lifecycle band and imports only `kitlib`, so no cycle can form. Requirement descent adds nothing, since LLR-360's Detail already reads "widens each need by the authoring work item's declared tags". The component scope stays whole.

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The spine set: the IF-092 `data` edit, TC-399's `Verifies` and `Evidence`, LLR-360's `Module` and `CodeSymbol`; LLR-360's Detail confirmed and left standing | D3; SR-161; TC-399 | IF-092; IF-023 | |
| P2 | The tests alone, under strict xfail marks with the characterisations beside them; no shipped file | D2; D4; SR-161; TC-399 | intra-module: test code only, no seam crossed | P1 |
| P3 | The column in its schema copies and the shipped template, with IF-092's contract body | D1; SR-161 | IF-092; IF-023; IF-078 | P2 |
| P4 | The reader: `context_from_work_item` takes a non-empty cell in place of the two cells | D3; SR-161; TC-399 | intra-module: one function of `hats`; its caller `plan_briefs` keeps its call | P3 |
| P5 | The writer: `_authoring_tags`, the two drafters, `_draft_row`, and the `intake.py` size stamp in the same row | D1; D2; D4; SR-161; TC-399 | IF-090; IF-092 | P4 |
| P6 | The adopter and reference records: the RESYNC_PACK entry and the machinery reference | D1; SR-161 | no interface: documents only | P5 |
| P7 | TC-399's `Method` and `Expected` text, written after the code settles, and the lane's one combined sitting | D3; SR-161; TC-399 | no interface: row text only | P6 |
| P8 | The commit bar and both strict lints on the landing tip | D5; SR-161; TC-399 | no interface: runs the bar | P7 |

Excludes: TC-178 — it verifies LLR-183's Hat-Refs resolution and effective-set mechanics, and this row touches neither Hat-Refs nor the roster.
Excludes: TC-198 — it verifies LLR-202's staged Hat-Refs amendment guard, which this row does not touch.
Excludes: TC-211 — a Release-tier Inspection of a completed decomposition record, run at release; this row changes which hats a brief lists, not the record or the inspection.

**Why clauses are cited twice.** D2 and D4 sit on P2 (the failing test) and P5 (the behaviour that turns it green). D1 sits on P3, P5 and P6, because the column, the write and the adopter record are separate deliverables of it. D3 sits on P1 (LLR-360 confirmed and its trace cells), P4 (the reader) and P7 (TC-399's text). These are real seams, not overlapping scope.

**Commit boundaries.** P1 is one commit and P2 is one commit, touching no shipped file. P3 to P6 are one code commit, for two reasons: strict xfail marks turn red on the first XPASS, so they all come off together, and the commit bar refuses a shipped-file change without a RESYNC entry anchored at the trunk base. No row repairs an earlier row. P7 follows review.

### P1: the spine set

Authored before the build, as `spine-authoring/references/in-lane.md` orders. No new id is reserved.

- **IF-092 `data`:** replace the stale "19-column" count and state the cell, for example `wi_convert.COLUMNS with AuthoringTags (authoring tags, ;-joined, or empty) and write_spec_file; ConvertError is the mint's refusal input`. The `version` stays `v1`, as WI-969's `data` edits left theirs.
- **TC-399 `Verifies`:** add IF-092, because an altered interface row needs a citing TC and today none cites it. `Verifies` routes to adjudication, so this joins P7's sitting.
- **TC-399 `Evidence`:** name every test in P2.
- **LLR-360 `Module` and `CodeSymbol`:** add `project-trajectory/scripts/hats.py` and `project-trajectory/scripts/intake.py`, and the symbols `context_from_work_item` and `_authoring_tags`. Both cells are traced, so no re-attestation arms. The CodeSymbol crosscheck is warn-only, so naming a symbol P5 creates does not red this commit.
- **LLR-360 `Detail`:** confirmed to read "widens each need by the authoring work item's declared tags" at this tip. No edit, which is D3's second half.

SR-161 itself is unchanged. It requires every applicable perspective's question in the brief, and this row makes the applicable set the same on both routes.

### P2: the tests

Each new test's docstring carries `Implements: TC-399` on its own line. New behaviour takes `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`, so the red must reach the test's own assertion. Two consequences for the builder: read the cell with `row.get("AuthoringTags")`, never a subscript, and drive the mint through `intake_after_merge` or the sweep, never the drafters' new parameter, which would raise `TypeError` before the change.

| Test | Class | Fails before the change on |
|---|---|---|
| `tests/test_wi_convert.py::test_the_authoring_tags_cell_round_trips_through_the_spec_form` | new | the writer drops the cell and neither reader returns it, so the read-back is empty (IF-092's citing test) |
| `tests/test_hats.py::test_a_non_empty_authoring_cell_supplies_the_tags_in_place_of_the_row_cells`, over the column and frontmatter spellings | new | the context is `["process", "adjudication"]`, not the cell's tags |
| `tests/test_plan_briefs.py::test_the_authoring_cell_widens_each_need_and_sibling_needs_never_merge` | new | a `process` / `adjudication` row carrying cell `b` over SN-4 and SN-5 omits `both question?` (D3) |
| `tests/test_intake.py::test_the_slot_mint_carries_the_closed_lanes_tags_on_both_row_kinds`, parametrized over first-approval and amendment | new | the cell is empty; it also pins `SafetyClass == "adjudication"` and `Workstream == "process"` (D1) |
| `tests/test_intake.py::test_a_merged_sweep_unions_the_named_rows_tags` | new | the cell is empty; expected is the deduplicated union in sorted-id order (D1) |
| `tests/test_intake.py::test_a_minted_author_passes_its_cell_on` | new | the cell is empty; a closed adjudication row carrying `authoring_tags` must pass it on, not `process;adjudication` |
| `tests/test_intake.py::test_a_real_mint_and_the_lane_row_compose_one_hat_set` | new | the two blocks differ (D4, below) |
| `tests/test_hats.py::test_an_empty_authoring_cell_reads_the_two_row_cells` | characterisation | passes before. Witness: an implementation that stops at a present-but-empty cell returns no tags |
| `tests/test_intake.py::test_a_range_sweep_with_no_merged_leaves_the_cell_empty_and_widens_by_its_own_tags`, over a plain range, `--with-terminal` and `--branch` alone | characterisation | passes before, by design (D2). Witness: an implementation keyed on `outcomes` rather than `branch` stamps every close on the `--with-terminal` case. It also asserts the row's own `process` hat is in its block |
| `tests/test_intake.py::test_a_bare_sweep_mints_neither_row_kind` | characterisation | passes before. Witness: a bare sweep that widened its range past HEAD..HEAD mints a row (spec's fourth provenance case) |
| `tests/test_intake.py::test_a_dispositions_block_may_not_declare_authoring_tags` | characterisation | passes before. Witness: adding the key to `_DRAFT_KEYS` admits a third writer |

**The D4 test.** It writes `docs/requirements/hats.toml` and a need, closes one lane row (`workstream = "unattended"`, `safety_class = "ordinary"`) and lands one Drafted SR. It takes the minted shape from `queued_rows` after a real `intake_after_merge`, and the in-lane shape as `compose_lane.py` builds it: the lane's row with `Brief`, `Adjudicates` and `SR-Refs` overridden. It calls `plan_briefs.sitting_hat_block` on each and asserts the blocks are equal, the `unattended` hat is in and the `process` hat is out. That last assertion is what catches reading the cell beside the two cells instead of in their place, the failure the spec warns about. Its roster mirrors the ruling's SR-161 line: UNATTENDED-OPS in, FIRST-RUN-ADOPTER out.

**Which tier runs what.** `test_intake` and `test_wi_convert` are in `SLOW_MODULES`, so the smoke tier skips them. Each build round runs them by name through `integrate.py attest --tests`. The `test_hats` and `test_plan_briefs` tests are the smoke tier's in-process pin of the reader. `hand_lane_repo` needs a small keyword to give its closed rows tags. That is test fixture work, and `write_spec` already forwards `workstream`, `safety_class` and list keys.

### P3: the column

- Add `"AuthoringTags"` after `"Adopted"` to `wi_convert.COLUMNS`, `kitlib.registry.WI_COLUMNS` and `plan_artifacts.WI_HEADER`.
- Add `("AuthoringTags", "authoring_tags")` to `wi_convert.LIST_FIELDS` and `kitlib.registry.SPEC_LISTS`.
- Append the column to `project-trajectory/registries/work-items.template.csv`, with an empty trailing cell on its WI-000 row, and to `WI_HEADER_LINE` in `tests/test_plan_artifacts.py`.
- State in the column's comment that this cell is not the routing `SafetyClass`.
- In `wi_convert.py`'s `Contract IF-092` body, replace "19-column" as P1 did in the row.

`test_columns_are_pinned_to_the_shipped_registry_header` and `test_wi_header_matches_the_shipped_template` hold the copies together.

### P4: the reader

In `hats.context_from_work_item`, read `_as_tags(_first(row, "AuthoringTags", "authoring_tags"))`. If that is non-empty, return it as the tags; otherwise run today's loop. Update the docstring and add `Implements: SR-161, LLR-360`. `plan_briefs` is unchanged, and `_hat_parent_context` widens each need by the context it is given, so the cell reaches every parent need with no further edit.

This reader also serves `plan_runner`'s planner brief, through `hat_surface_for_work_item`. A row with an empty cell composes as today there, so no ordinary planner brief moves.

### P5: the writer

- `import hats`, with the siblings.
- Add `_authoring_tags` (decision 3), carrying `Implements: SR-161, LLR-360`.
- In `intake_after_merge`, compute it once and pass it to both drafters.
- Each drafter adds `"authoring_tags": list(authoring_tags)` to its draft.
- `_draft_row` gains `row["AuthoringTags"] = ";".join(draft.get("authoring_tags") or [])`.

**The size stamp is in this row.** `intake.py` measures exactly its baseline of 1872 SLOC today, and `test_module_sizes_exactly_match_the_committed_baseline` runs in the smoke tier. This row adds about 13 SLOC. Stamp the measured value in `tests/test_module_size_ratchet.py`, naming WI-982 and the reason. This is the reviewed upward bump the file's docstring allows: the addition is the provenance rule itself, and `hats` already holds the reading half, so there is nothing to split off. A review round or rebase that moves the count re-stamps in that commit.

The other changed modules stay under the 1000 SLOC threshold: `hats.py` 511, `wi_convert.py` 408, `plan_artifacts.py` 172, `kitlib/registry.py` 266. No touched function sits in `docs/complexity-baseline` except `_close_drafts`, which is not edited.

### P6: the records

- **`project-trajectory/RESYNC_PACK.md`:** a new §3 entry, anchored `[since <sha>]` at the lane's trunk base as read at build time. What changed: the mint's new cell, and that a minted row's hat block now follows the authoring item. **No forced migration**: an absent key reads as an empty cell and rows already minted keep today's widening. Only a repo still carrying the retired legacy CSV adds `AuthoringTags` after `Adopted`. Kit-owned files to overwrite: `scripts/intake.py`, `scripts/hats.py`, `scripts/wi_convert.py`, `scripts/plan_artifacts.py`, `scripts/kitlib/registry.py`, `registries/work-items.template.csv`.
- **`docs/registry-machinery-reference.md`:** a short section after "The `Digests` cell" stating the domain, the provenance table, and why it is a real column.

### P7: TC-399's text

Written once the code stops moving, then judged with TC-399's `Verifies` change in the lane's one combined sitting (`in-lane.md`). No text is added to LLR-360 or SR-161.

- **`Method`:** after "work-item tags widen one need without merging siblings", add: "the authoring work item's tags widen them on both routes: a minted row's authoring cell supplies its tags in place of its own, the minted and in-lane rows for one system requirement compose one hat set, and a row whose cell is empty widens by its own tags".
- **`Expected`:** add that the two routes put one hat set for one system requirement.

### P8: the bar

On the landing tip, run `run.cmd smoke` (`run_menu.py smoke` from a shell). It runs `trace.py --strict`, `check_trajectory.py --strict`, the docs staleness and RESYNC entry checks, and the smoke tier. Also run the P2 tests in `test_intake` and `test_wi_convert` by name, since smoke skips them. The generated views (`docs/interface-reference.md`, `docs/requirements/components.derived.toml`, the arch map) follow the coordinator's landing recipe, `coordinator-cycle` recipes §3, and are not hand-edited. The lane keeps its module-size stamp through that restore.

## Downstream effect

No forced migration. Adopters take the new cell on their next resync, the spec-folder registry needs no edit, and `docs/process.toml` is untouched. The one visible change: minted first-approval and amendment rows' hat blocks follow the authoring lane, so `process`-keyed hats such as FIRST-RUN-ADOPTER can drop off a minted sitting whose lane is not `process`-tagged. That is the ruling's intent, and the RESYNC entry says so.

## Findings outside this row, not fixed here

- `hats` owns no IF row, though `plan_briefs` calls it and now `intake` will. PROCESS.md §8 reads as wanting a row for a surface between a repo's own modules, while the mechanized rule covers only cross-component edges. This is a pre-existing gap, and closing it would add a boundary the spec rules out.
- "19-column" and "19-key" remain as stale prose in `wi_convert.py`'s CSV reader and writer docstrings and in `kitlib/registry.py`'s `parse_spec_row` docstring. The count has been 22 since `Adopted`. They carry no contract, so they are left alone.
