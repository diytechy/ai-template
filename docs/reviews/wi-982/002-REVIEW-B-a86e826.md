Reviewed: a86e826877d289bdd698e88b59b4b97cb8eecd43

### REVIEW-B — WI-982 — full lane de3838360..a86e82687 — 2026-11-04

**Failure classes hunted first, severity-ordered.** (1) Silent wrong content: a minted sitting composing a different hat set from the in-lane route, or a cell that is written and never read, or read beside the routing cells. (2) Fail-open by route: a branchless or `--with-terminal` sweep stamping every close on file into the cell. (3) Schema regression: a new column moving a row hash, tripping a key lint, or being dropped by a writer, or an `intake -> hats` import breaking a scaffold or the layer order. None was reproduced.

**Verified.** `git rev-parse HEAD` printed the reviewed commit. Everything beyond the two declared commands ran in a scratch copy of the tree under my writable area.

- Real routes driven. `intake.intake_after_merge` over both row kinds gave `AuthoringTags = unattended;ordinary`, with `SafetyClass = adjudication` and `Workstream = process` kept. `adjudicate_brief.compose` on the minted row and on the row shape `scripts/coordinator/compose_lane.py` builds both returned a body: lane question present, `process` adopter question absent, on each.
- A close under `docs/archive/work/complete/` with a real `kitlib.station.Outcome.MERGED` value stamps the cell, and a `partial/` close stamps the amendment row.
- Sweeps. `--before/--after` with no `--merged`, with `--with-terminal`, and with `--branch` alone leave the cell empty. The `--merged` union is deduplicated and in sorted-id order, and an unnamed close adds nothing.
- A branchless sweep followed by `--merged` over the same range prints "nothing to mint" and leaves the cell empty, which is the bound the machinery reference states.
- Callers. `intake_after_merge` has two callers, and the route test is sound: `integrate.py:3550` always passes its branch, and `_cmd_sweep` passes `claim` only under `--merged`, whose outcomes branch runs before `--with-terminal`.
- Brief kinds. Only the first-approval and amendment templates declare `{hats}`, and only the two edited drafters mint those briefs.
- The combined sitting is per row, so `sitting_tail` loses no second lane's tags. `compose_lane.py`, `mkprompt.py` and `agent_loop.py:406` all hand a full registry row.
- Schema. `consolidate.queue_digest` hashes four named fields, so the column moves no digest. `check_trajectory`'s row walk is cell-generic. Registry population: 997 rows, every one with a Workstream, none whose values contain `;` or `,` in the tags used.
- Scaffold. A bootstrapped scaffold imports `intake`, ships `scripts/hats.py` (`bootstrap_manifest.py:571`), writes a row carrying the cell through `wi_convert.write_spec_file`, reads it back, and `check_trajectory --strict` stays clean. `bootstrap_manifest.py:259` confirms the template CSV is deliberately not delivered, so D-003's overwrite-list correction is right.
- The WI-000 template row is 21 cells against a 23-cell header, 20 against 22 before: short as found, as D-002 states.

**Red-before and adequacy.** With the five shipped scripts restored to de3838360 and the lane's tests kept, the selection went 19 passed to 9 failed, 10 passed: exactly the new-behaviour tests. The 10 that passed are the characterisations, as the plan classes them, and each was killed by a mutant:

| Mutant | Tests failed |
|---|---|
| cell read beside the two cells, not in their place | 4 |
| route keyed on `outcomes`, not `branch` | 1 (`with-terminal`) |
| `_closed_spec` default pair, omitting `complete/` | 5 |
| ids unsorted | 1 |
| no pass-on of a minted author's cell | 1 |
| amendment drafter drops the tags | 1 |
| no dedup | 1 |
| reader stops at a present-but-empty cell | 6 |

The `_DRAFT_KEYS` and bare-sweep characterisations were not mutated; their witnesses were read, not run.

**Done-when map.**
- D1, the cell on both row kinds by a naming route: `test_the_slot_mint_carries_the_closed_lanes_tags_on_both_row_kinds`, `test_a_merged_sweep_unions_the_named_rows_tags`, `test_a_minted_author_passes_its_cell_on`, `test_the_authoring_tags_cell_round_trips_through_the_spec_form`.
- D2, the branchless case: `test_a_range_sweep_with_no_merged_leaves_the_cell_empty_and_widens_by_its_own_tags` (three ids), `test_a_bare_sweep_mints_neither_row_kind`.
- D3, both routes widen by the authoring tags: `test_a_non_empty_authoring_cell_supplies_the_tags_in_place_of_the_row_cells`, `test_an_empty_authoring_cell_reads_the_two_row_cells`, `test_the_authoring_cell_widens_each_need_and_sibling_needs_never_merge`. LLR-360's Detail already reads "widens each need by the authoring work item's declared tags" and is unchanged, as the spec records.
- D4, one hat set: `test_a_real_mint_and_the_lane_row_compose_one_hat_set`. It builds the in-lane shape by hand rather than calling `compose_lane.py`; my `compose` run above covers that shape through the real composer.
- D5: partly observed. `check_trajectory --strict` exits 0 and `trace.py --strict-integrity` exits 0. The commit bar and `trace.py --strict` were NOT run here, because the round facts forbid the smoke tier; this item stays with the landing tip.

**Rubric anchors.** K1: the one gap is the finding below. K2: no SN or SR cell changed. K3: the two new `Implements: SR-161, LLR-360` tags sit on `context_from_work_item` in `hats.py` and `_authoring_tags` in `intake.py`, both now in LLR-360's `module` and `code_symbol`. Every Status is unchanged; the approved rows changed only in trace cells (LLR-360) and `verifies`/`evidence` (TC-399), as the plan's P1 sets out, and each of the 11 evidence names resolves to a test. B1: the finding was confirmed by reading the rows. PROCESS.md §3: `_authoring_tags` reuses `_closed_spec` and `hats.context_from_work_item`, and repeats nothing.

**Counterpart record (R1, R2).** This is a semantic reading, not reference existence.
- IF-092 `data` changed. Its code counterpart, the `Contract IF-092` body at `project-trajectory/scripts/wi_convert.py:90`, carries the same change. IF-023 is retained: its "one Markdown spec per row" names no key list, so the cell rides it with no change of meaning. TC-399 `verifies` carries the citation, but its `method` and `expected` do not yet carry the behaviour: see the finding.
- LLR-360 `module` and `code_symbol` changed. SR-161 is retained, because it requires every applicable perspective's question and this change only makes the applicable set agree across routes. LLR-360's `detail` is retained, because the code now makes the clause true.
- PROCESS.md §5 change intake: no workaround preserves an unsuitable LLR. Parent acceptance, approval and the enduring regression tests stand.
- The diff adds no SN, SR or TC row and no decomposition, so there is no new-row sweep and no retained-child record to make.

**Coverage-extension note (no severity, not counted).** An authoring row that declares neither Workstream nor SafetyClass falls outside the spec's declared cases. The cell is empty, so the minted row widens by `process` and `adjudication` while the in-lane route widens by nothing, and the two blocks differ; I reproduced this. It errs toward an extra question, never a lost one, and all 997 rows on file carry a Workstream, though no validator requires one. The plan's domain table records it.

**Observations outside the reading scope (not findings).** `docs/requirements/hats.toml:44-45`, owner text, still says the composer's tags are "a work item's Workstream and SafetyClass". The header comment of the two sitting templates still says "the work item's tags". Both now read slightly short of the behaviour, and the owner may wish to touch the first at the roster's review.

**Lane side effect, disclosed.** The instruments the brief orders wrote only ignored files in the lane: `trace.py --strict-integrity` rewrote `docs/test/report.md` (gitignored, written by its normal run), and the pytest run may have left ignored bytecode. `git status --short` is empty, and no tracked file changed.

**Commands.**
- `git rev-parse HEAD` -> `a86e826877d289bdd698e88b59b4b97cb8eecd43`
- the brief's pytest line (7 modules, `-n 2`, literal `--basetemp`) -> `305 passed, 4 skipped in 157.27s (0:02:37)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (996 work item(s), 882 done (89%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=331 TC=363 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md` exit 0
- scratch `mutate.py` (pre-fix tree and eight mutants over the new tests) -> base `19 passed`, pre-fix `9 failed, 10 passed`, every mutant red as tabled above
- scratch `tests/test_zz_review.py` (real compose on both routes, archive close, partial close, untagged lane, branchless then `--merged`) -> `3 passed` and `2 passed`, the printed values as stated above
- scratch `pytest tests/test_import_layers.py` -> `7 passed in 4.73s`
- scratch `bootstrap.py --dest`, then `scripts/check_trajectory.py --strict` with a cell-carrying row -> `check_trajectory: clean (1 work item(s), 0 done (0%), graph acyclic).`

**Findings.**

- [MINOR] docs/test/test-cases.toml:4047 -> K1: at the reviewed commit TC-399's amended `verifies` cites IF-092 and its `evidence` names the eleven new tests, but `method` (4049) and `expected` (4051) state nothing of the authoring cell, the two routes' one hat set, or the empty-cell default, so the row's text does not describe the verification its citation claims, and the counterpart change to IF-092 is only half carried; the plan schedules this as P7, after review, so it is owed rather than overlooked -> write the plan's P7 `method` and `expected` text into TC-399 and judge it in the lane's one combined sitting before the landing -> @owner

VERDICT: CHANGES-REQUESTED findings=1
