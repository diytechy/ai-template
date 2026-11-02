# WI-987 plan, revision 2: the open-items page lists the stakeholder needs and stakeholders owing an act

Planned against lane `C:/Projects/ai-template.wt/wi-987` (branch `wi-987`, head `3f4b989df`). Read: the row `docs/work/active/wi-987/WI-987-open-items-renders-owing-needs.md` and its spec `docs/specs/WI-987.md`. The spec quotes no owner ruling or adjudicator draft beyond its scope-critique dispositions F1–F3, and the plan carries all three.

This revision answers the plan critique `docs/plans/WI-987/critique-1.md` (round 1, CHANGES-REQUESTED, findings=2). Both findings were checked against the code before any change; see "Critique dispositions" below.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. The answer is unchanged from revision 1; neither finding touches a state, a domain, an input or a boundary. Each step's result:

1. **Mode classes (A2).** None added. `gen_open_items.render` is a pure function of the committed tree with no state, and no flow in `docs/runtime-flows.md` covers it (Flows 1–8 are the coordinator, scaffold, secrets, station, blackout, judging and act, codex and usage flows). `docs/runtime-flows.md` is not edited: there is no new state and no new transition.
2. **Value domains (A3, A6).** Two values are added, both within scope:
   - IF-074 is the page's reported population. Section 2 now holds two kinds of entry: SR entries (`approve` or `reattest`, as before) and need or stakeholder rows. A need row carries the detector's `why`, one of `DRIFTED`, `Drafted, never approved` or `no Status cell, never approved`.
   - IF-126 is the data the page consumes from `baseline_snapshot`. It gains `needs_owing`, whose value is `[(id, why, cells, row)]`.
   - Both are recorded as each row's `data` cell (P4). IF-075, the SR-chain model `reattest_model`, keeps its domain and is not edited.
3. **Output-on-input dependencies (A4).** A new input is added. The table below is recorded here, as the skill allows when planning:

   | Page output | Inputs today | Input added |
   |---|---|---|
   | Section 2 cards | `trace.reattest_model` (IF-075) | `baseline_snapshot.needs_owing` (IF-126) |
   | Section 2 empty message | `reattest_model` | `needs_owing` |
   | Header counts (owing, drifted) | `reattest_model` | `needs_owing` |
   | Baseline list | `registry_stamps` (IF-126) | none |
   | Verdict audit list | `read_acts` | none |
   | Sections 1, 3, 4 | `pending.*` | none |

4. **Descent (A8).** No new boundary is crossed. The page (`scripts/gen_open_items`, CMP-009) already reads `scripts/baseline_snapshot` (CMP-006) over IF-126. The detector stays with CMP-006 and keeps its domain; CMP-009 adds one more read of it.
   - No component cut, no sub-component split, and no edit to `docs/requirements/components.toml`.
   - No new interface row, and no new detector rule.

The change is carried by P3, which adds the input, and P4, which edits the domains of IF-126 and IF-074.

## Critique dispositions

- **F1 (MAJOR), confirmed and adopted.** `trace.truncate_cell` clips at `CELL_TRUNCATE_LIMIT = 1500` (`trace.py:3513`), and revision 1's `_full_cells_html` kept it, so a first-approval need with a longer cell would render clipped while D1 asks for its cells in full. The bound is reachable by a supported workflow: the longest live need cell today is SN-029's `acceptance` at 1,025 characters, and the needs registry sets no length bound. The kit's own reasoning agrees: OI-71 defect 2 (the `_cell_diff_lines` docstring in `trace.py`) keeps the clip on context surfaces only, never on the text a signer rules on. A first-approval row is all ruled text: every cell of it is approved at once. The change:
  - P1's helper takes the values from its caller instead of clipping them. `_chain_row` passes its clipped values, so SR rendering is unchanged.
  - P3's first-approval need cards pass the raw stripped values.
  - T2 gains a cell longer than the limit and asserts that its end appears.
  - Found while checking, outside this row: the Markdown brief's own first-approval arm (`trace.need_brief_lines` through `_full_row_bullets`) clips the same way. The brief is not in this row's Done-when, and changing it is a separate behaviour change, so the plan does not touch it. It is surfaced in "Out of scope" for the coordinator to file if wanted.
- **F2 (MINOR), confirmed and adopted.** P4 edits the `gen_open_items.py` module docstring and the `Contract IF-074:` body, both above the `newline=chr(10)` site that P5 re-pins. With only P3 as a predecessor, P5 could pin the line before P4 moves it. P5 now names P4 as a predecessor.

## Build table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Share the cell markup inside gen_open_items, values supplied by the caller | D1; F1; SR-178 | intra-module: gen_open_items.py only, no seam crossed | |
| P2 | Write the failing tests | D1; D2; D4; F1; SR-178; TC-269 | IF-074; IF-126 | P1 |
| P3 | Section 2 reads needs_owing, first-approval cells unclipped | D1; D2; F1; SR-178 | IF-126; IF-075; IF-074 | P2 |
| P4 | Contract text for IF-126 and IF-074 | D3; SR-178 | IF-126; IF-074; IF-075 | P3 |
| P5 | Pins and TC-269 evidence | D2; D4; F2; SR-178; TC-269 | no interface: test pins and one traced registry cell | P3; P4 |
| P6 | Regenerate the page and check SN-028 and SN-036 | D5; SR-178 | IF-074 | P4; P5 |
| P7 | RESYNC entry, log fragment, bar and strict lints | D6; SR-178; TC-269; TC-271; TC-278 | IF-074; IF-126 | P6 |

Excludes: TC-153 — it verifies the drift comparison in `baseline_snapshot` and `check_trajectory.split_changed_cells`, which this item does not change.
Excludes: TC-331; TC-398 — they verify the merge-slot approval rung and the act turn's held-text identity check. Neither reads `gen_open_items` or `needs_owing`, and nothing here touches their code.

**Why some clauses span several rows.**
- D1: P1 is a refactor that changes no behaviour, P2 adds the tests that pin D1, and P3 delivers D1.
- D2: P2 adds the count test, P3 changes the code, and P5 extends the existing empty-message test.
- D4: P2 writes the test and P5 records it as TC-269 evidence.
- F1: P1 shapes the helper so the caller owns clipping, P2 adds the long-cell assertion, and P3 passes unclipped values.

No scope is duplicated.

## Steps

### P1: share the cell markup (`project-trajectory/scripts/gen_open_items.py`)

Refactor only, with byte-identical output. Two helpers are extracted so the need cards in P3 reuse the SR cards' markup instead of copying it (deep-module-design; this also saves module SLOC):
- `_cell_diff_html(cells)`: the loop in `_changed_cell_lines` that renders each `(name, before, after)` as the `cellname` heading with its `% of the words changed` pill and `word_diff`. The before and after are rendered whole, as today.
- `_full_cells_html(pairs)`: the loop in `_chain_row` that renders each `(key, value)` as a `cellname` heading over a `diff` block. It escapes the value and skips an empty one, but **does not clip** (F1). Clipping is the caller's choice, not a mode flag of the helper:
  - `_chain_row` calls it with `((k, tr.truncate_cell(v.strip())) for k, v in full.items())`, so the SR cards render exactly as today.
  - P3's need cards call it with the stripped values unclipped.

`_changed_cell_lines` and `_chain_row` call these helpers.

Check: before any other edit, `python project-trajectory/scripts/gen_open_items.py --check` exits 0 on the lane, so the page is unchanged. `pytest tests/test_gen_open_items.py -q` stays green, which pins the SR cards' clipped rendering. No test is added because P1 changes no behaviour.

### P2: write the failing tests first

All three tests go in `tests/test_snapshot_readers.py`, after `test_a_drifted_approved_stakeholder_is_reported_and_briefed`, on the `scaffold` fixture. They render in-process with `load_script("gen_open_items").render(root)`, the same way `test_the_owners_brief_and_open_items_name_each_registrys_own_copy` does. That module is in `SLOW_MODULES`, so the smoke tier's `max-tests` ratchet does not move.

- **T1 `test_a_drifted_need_has_its_card_on_the_open_items_page`** (D4, D1 drift arm).
  - Setup: `_append(root, NEEDS_REL, _NEED)`, then `SNAP.copy_live(root, seed=True)`, then rewrite `need =` to add ", at once" (the fixture edit that `test_a_drifted_approved_need_is_reported_and_briefed_with_its_diff` already uses).
  - Asserts: `id="SN-001-attest"` is in the page. The card's pill is `DRIFTED`, it has a `Need` cellname, and its diff contains `<ins>` around "at once" and the unchanged before-text. The page does not contain "no SR owes an approval or a re-attest".
  - Fails today: the card id is absent and section 2 prints the empty message.
- **T2 `test_a_first_approval_need_and_stakeholder_show_their_cells_in_full`** (D1 first-approval arm, F1).
  - Setup: append need `SN-002` with `status = "Drafted"` and a `why` cell longer than the clipping limit: `"x " * (trace.CELL_TRUNCATE_LIMIT // 2 + 50)` followed by the sentinel `"END-OF-WHY"`. Append stakeholder `STK-01` with a name and description but no `status` line. Render with no seed; the detector reports first-approval rows with or without a record.
  - Asserts: card `SN-002-attest` has the pill `Drafted, never approved` and its `Need` text in full. Its `Why` cell ends with `END-OF-WHY`, and the card does not contain "more chars — read the registry row" (the clip marker). Card `STK-01-attest` has the pill `no Status cell, never approved` and its `Name` and `Description` in full. Neither card has a `<del>` or `<ins>`.
  - Fails today: neither card exists. It also fails on a renderer that routes these cells through `truncate_cell`, which is the F1 defect.
- **T3 `test_the_open_items_counts_include_the_needs_that_owe`** (D2 counts).
  - Setup: the same as T1.
  - Asserts: the header reads `1 stakeholder need(s) or stakeholder(s)` and its drifted count includes the need (`1 row(s) drifted`, assuming the scaffold has no owing SR; the builder confirms that against the scaffold and asserts the computed number).
  - Fails today: the header has no needs count and reports `0 row(s) drifted`.

Run `pytest tests/test_snapshot_readers.py -k "open_items_page or in_full or counts_include" -q` and record that all three fail before P3.

### P3: section 2 reads `needs_owing` (`gen_open_items.py`)

**`render`**
- Add `owing = baseline_snapshot.needs_owing(root)`. This is the one detector `trace.need_brief_lines` reads; the page applies no second filter and does no reclassification.
- Compose section 2 as `(_attestation_cards(model, srs_by_id) + _need_cards(owing)) or _NOTHING_OWED`. The empty message is printed only when both are empty.

**`_attestation_cards`**
- Lose its `if not model` branch. With an empty model it now returns `""` naturally.
- Its message text moves to `_NOTHING_OWED` (a constant or a small function).

**`_NOTHING_OWED`** (D2)
- Keep the existing wording. Existing tests pin "no SR owes an approval or a re-attest", `<strong>SR</strong>`, "snapshot-drift" and "reaches this view DIRECTLY".
- Add the needs clause, which says what was checked: "and no stakeholder need or stakeholder in `<code>docs/requirements/stakeholder-needs.toml</code>` is `Drafted`, lacks a `Status` cell, or has drifted from its recorded copy (`<code>baseline_snapshot.needs_owing</code>`)". The path comes from `baseline_snapshot.NEED_TIERS[0][0]`, not a literal.

**New `_need_cards(owing)`**
- Docstring cites `Implements: SR-178`, an SR-only tag. LLR-271's Module cell does not name this file, so an LLR tag would raise the CodeSymbol cross-check warning. SR-only tags already exist (`check_test_first.py:612`, `derive_stage.py:499`).
- It returns `""` for an empty list. Otherwise it returns one sub-heading, "Stakeholder needs and stakeholders owing an act" (the brief's heading), then one short paragraph with the brief's guidance (re-anchor with `intake.py snapshot --reattests <ROW-ID>`; a `Drafted` or Status-less row owes its first approval), then one card per detector row, in the detector's order:
  - The card is `<article class="card" id="{rid}-attest">`, headed by the id and a pill showing the detector's `why` verbatim through `esc`.
  - The pill class is plain when `cells` is non-empty and ` approve` when it is empty. The wording differs between the two kinds, so `test_a3_kind_pills_are_never_distinguished_by_colour_alone` still holds.
  - When `cells` is non-empty (drift), the body is `_cell_diff_html(cells)` plus `_context_block(row, skip={moved cell names}, heading="the rest of this row — unchanged since the snapshot")`. The moved cells render whole; the unchanged rest is context and keeps `_context_block`'s existing clip, as the SR cards' context does.
  - When `cells` is empty (first approval, or any other `why` the detector returns), the body is `_full_cells_html((k, (v or "").strip()) for k, v in row.items())`: the row shown as the detector returns it, every cell unclipped (F1), because every cell of a first-approval row is under approval.
- Keep it within C901 10: one loop and one branch.

**Counts**
- Add `"needs": len(owing)`.
- `drifted` becomes the SR count it is today plus `sum(1 for o in owing if o[2])`.
- The header sentence becomes "{attest} SR chain(s) and {needs} stakeholder need(s) or stakeholder(s) owing an approval or a re-attest, across {rows} chain row change(s); {drifted} row(s) drifted…". This also fixes "a approval".
- Its authority clause names `baseline_snapshot.needs_owing` beside `trace.reattest_model` as "the same code behind `trace.py --approve`".

**Budget**
- `gen_open_items.py` is at 933 SLOC (`check_complexity.module_sloc`) against THRESHOLD 1000 in `tests/test_module_size_ratchet.py`, and has no baseline entry. P1 and P3 together must add fewer than 67 SLOC. Docstrings do not count. The F1 change moves the clip from the helper to its one SR caller and adds no line.
- If the change would cross 1000, decompose instead. Do not add a baseline entry.

Afterwards T1–T3 pass, and `pytest tests/test_gen_open_items.py tests/test_open_item_queue.py -q` stays green. Those fixtures write a `# SN` markdown needs file with no rows, so `needs_owing` returns `[]`.

### P4: contract text (D3)

**`docs/requirements/interfaces.toml`**
- IF-126 `data`: change "registry_stamps and SNAPSHOT_DIR" to "registry_stamps, needs_owing and SNAPSHOT_DIR". Its `notes` may add "needs_owing: the stakeholder needs and stakeholders owing an act, read for section 2".
- IF-074 `data`: change "…approval/re-attest chains, verdict audit…" to "…approval/re-attest chains and the stakeholder needs and stakeholders owing an approval or a re-attest, verdict audit…".
- Both rows are `status = "Drafted"`, so the edits raise no drift and no re-attestation.
- IF-075 is not touched, and neither is any other row.

**Module docstrings, kept in step**
- `baseline_snapshot.py`, the `Contract IF-126:` body (line 147): name `needs_owing(root)` and its `(id, why, cells, row)` rows.
- `gen_open_items.py`:
  - the module docstring's "WHAT IT RENDERS" item 2, which gains the needs rows, a first-approval one with its cells unclipped;
  - the ANTI-DUPLICATION paragraph, which says the module imports `baseline_snapshot.needs_owing` as the brief does;
  - the `Contract IF-074:` body, which names the needs population and `needs_owing` among its sources.

No test is added: these are text edits, and `trace.py --strict` in P7 checks the rows.

### P5: pins and evidence (after P3 and P4, F2)

P5 runs only once P3 and P4 have both landed in the working tree, because P4's docstring edits sit above the line it pins.

- **`tests/test_generated_newlines.py::test_the_one_non_literal_site_in_the_kit_is_lf`.** It pins `("gen_open_items.py", 1580)`. Re-pin it to the measured new line of `newline=chr(10)` after P1, P3 and P4, and add the history clause "1580 -> N when WI-987 added `_need_cards`, the shared cell helpers and the needs clauses above this site". Before the re-pin this test fails on the moved line.
- **`tests/test_gen_open_items.py::test_empty_attestation_state_names_only_what_it_checked`** (D2). Extend it to assert the needs clause: "stakeholder need", `docs/requirements/stakeholder-needs.toml` and `needs_owing`. It fails on today's message.
- **`docs/test/test-cases.toml` TC-269 `evidence`.** Append T1, T2 and T3 by node id. `Evidence` is a traced cell (`acceptance_record.SPINE_TRACED_CELLS`), so the change arms no re-attest on the approved TC-269.
  - Not edited: `Method` and `Expected` (approved cells; editing them would raise drift), and `Verifies`. Adding IF-074 to `Verifies` would force a pruning of `SEEDED_IF_TC_ALLOW` in `tests/test_trajectory_arch.py`.

### P6: regenerate and check (D5)

- Run `python project-trajectory/scripts/gen_open_items.py` in the lane, and commit `docs/open-items.html` with the code (lane commits carry it, as `dc7e2a5cf` did).
- Check: the set of need and stakeholder card ids in the page equals the ids `baseline_snapshot.needs_owing('.')` returns.
  - On `3f4b989df` that set is {SN-028 (DRIFTED: Acceptance, Why), SN-036 (DRIFTED: Acceptance)}.
  - Each card shows its moved cells before and after.
  - The section no longer prints the empty message.
- If WI-985 (SN-028's re-attestation act) lands on trunk before this lane does, SN-028 correctly drops off. D5 is read as "shows while its act is owed", so the check is against the detector on the landing tip.
- `--check` must exit 0 afterwards.

### P7: shipping entry, log, bar (D6)

- **`project-trajectory/RESYNC_PACK.md` §3.** `gen_open_items.py` and `baseline_snapshot.py` ship, so `scripts/check_resync.py` requires an added entry, `### The open-items page lists the stakeholder needs and stakeholders owing an act [since <trunk base sha>]`. It says that section 2 now reads `baseline_snapshot.needs_owing`, what each card shows (a first-approval card's cells unclipped), the widened empty message and the counts, and that an adopter's page gains need cards on regeneration.
- **Log fragment.** `docs/log.d/WI-987-<slug>.md` per session-protocol, including its `Deferred open items:` line, which names the brief's clipped first-approval arm (see "Out of scope") if the coordinator has not filed it.
- **Bar.** `run.cmd smoke`: both strict lints, then `check_docs --stale`, `check_resync` and the smoke tier.
- **Strict lints, run separately and quoted.** `trace.py --strict` and `check_trajectory.py --strict`.
- **Targeted slow modules.** `pytest tests/test_snapshot_readers.py tests/test_gen_open_items.py tests/test_open_item_queue.py tests/test_generated_newlines.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py -q`.
  - This runs the tests of TC-269 (T1–T3 included), TC-271 (`test_the_owners_brief_and_open_items_name_each_registrys_own_copy`, which renders the same page) and TC-278.

## Out of scope (kept from the spec's boundaries)

- Assumption and surrogate tiers.
- `pending.py`'s own owing reading, and `PROJECT_STATE.html`.
- Any change to the detector.
- **The Markdown brief's first-approval arm.** `trace.need_brief_lines` renders a first-approval need through `_full_row_bullets`, which clips at 1,500 characters. After this row the page shows such a cell whole and the brief shows it clipped with its explicit marker. Both name the same rows as owing, so the page and the brief do not disagree on what owes; they differ only in how much of an over-limit cell each prints. Changing the brief is a behaviour change outside this row's Done-when; it is a separate finding for the coordinator to file as a successor.
- LLR-118's `Detail` (an Approved cell) is not amended, though it lists the page's sections without the needs.
  - Amending it would raise drift and owe an owner re-attestation outside this row's Done-when.
  - The precedent is WI-651, which put the page's SR-178 behaviour under TC-271 with no edit to LLR-118.
  - The coordinator may file the wording as a successor if wanted.

## Risks

- **SLOC headroom of 67** (P3 budget).
- **The 1580 line pin** (P5, now after P4).
- **Trunk movement on SN-028** (P6).
- **A snapshot that will not parse.** `needs_owing` raises on it, the same as `reattest_model` already does. That is outside D1's coverage bound.

### Critical Files for Implementation
- C:/Projects/ai-template.wt/wi-987/project-trajectory/scripts/gen_open_items.py
- C:/Projects/ai-template.wt/wi-987/project-trajectory/scripts/baseline_snapshot.py
- C:/Projects/ai-template.wt/wi-987/docs/requirements/interfaces.toml
- C:/Projects/ai-template.wt/wi-987/tests/test_snapshot_readers.py
- C:/Projects/ai-template.wt/wi-987/tests/test_generated_newlines.py
