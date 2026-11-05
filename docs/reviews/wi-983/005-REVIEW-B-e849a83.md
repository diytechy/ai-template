Reviewed: e849a83648a366ca690686d02b392468d06c39cd

Verified. Convergence stance, full lane e73e49cf8..e849a83. `git rev-parse HEAD` printed the reviewed commit. The worst classes this change admits, hunted first: a stopping line that a verdict reader takes as a ruling (silent wrong act); a line missing from a set the spec closes, or reaching a set it excludes; a no-hats round left with no placement; a shipped template losing the line unnoticed; an input of TC-211 moved so the observation of record goes stale. None held.

Behaviour, driven on real code in a scratch export of the tip. `adjudicate_brief.compose` on the shipped templates gave the line once for an amended need alone with no roster, and once in the perspectives part of a combined round, after the last section, with the placement sentence. A verdict carrying `- STOPPING BOUNDARY SR-001, LLR-001, TC-001 -> ...` parsed through `ksitting.parse`, `accepted` and `judged_rows` to the same machine lines, rulings and judged rows whether the line sat at the end, directly under the last heading, or inside the first section. `_ruled_row` matches only a line opening with a declared tag. `mkprompt.py` reads `round_questions`, so the spine author's prompt does not move. Both composing routes (`project-trajectory/scripts/agent_loop.py:406`, `scripts/coordinator/compose_lane.py:34`) call `adjudicate_brief.compose`, the only caller of `fill_hat_slot`. `gen_prompt_catalog.py --check` is fresh with no catalogue change, so the plan's "the digest moves" was wrong and the RESYNC entry is right to omit `CATALOG.md`.

Done-when map.
- D1, the line, for the closed set: `test_a_round_block_asks_a_stopping_boundary_line_beside_the_hat_outcome_lines`, `test_a_round_with_no_applicable_hat_still_carries_the_stopping_boundary_line`, `test_a_round_sitting_composed_alone_carries_the_stopping_boundary_line_once`, `test_a_combined_round_carries_the_stopping_boundary_line_once_after_its_last_section`, `test_a_combined_round_with_no_applicable_hat_is_told_where_to_write_the_line`, and for the default `test_a_non_round_carries_no_stopping_boundary_line`, `test_a_sitting_that_is_no_round_carries_no_stopping_boundary_line`, `test_an_override_without_the_hats_slot_composes_unchanged`, `test_a_malformed_roster_refuses_a_round_sitting_by_name`. COVERED.
- D2, shipped templates: `test_each_shipped_sitting_template_carries_the_stopping_boundary_line`. COVERED.
- D3, WI-998: `git merge-base --is-ancestor e72b1f700 2965e4762` exits 0, so it was filed before the claim; `needs = ["WI-983"]`; its Done-when runs in the spec's order; `docs/status.md` does not name it. COVERED by inspection.
- D4: one entry, `project-trajectory/RESYNC_PACK.md:10448`, and `check_resync` OK. Both strict lints are clean. The smoke tier was not run, as the round facts direct; every lint step of the bar was, so the tier's green is the launcher's to show.

Red-before. Pre-fix `plan_briefs.py` under the tip's tests: 13 failed, 8 passed over the 21 selected cases. The 13 are every new-behaviour test, and the 8 are the characterisations and the amended opt-out test, which pass on both sides as the plan says. Mutants, each red on the expected test: line appended ahead of the round test (4 red); line only with hats (4); line before the outcome instruction (1); round widened to `amended` (2); line in the section pointer (4); line moved into `round_questions` (6); no placement for a no-hats round (2); no placement for a hat round (3, through the assertion commit e19a5cd1b added); amendment template without `{hats}` (1); a verdict reader counting any `- ... -> ...` line as a ruling (3). That added assertion is the lane's one post-build test change, and the mutant confirms it. The one existing test amended, `test_an_absent_roster_yields_the_opt_out_line_in_a_round`, moves from `==` to `in` because the block now rightly holds more; its `- HAT` assertion stays.

Requirement/interface record. Changed side: LLR-360 (`sr_refs`, title, detail, rationale) and TC-399 (`verifies`, method, expected, evidence). Counterparts:
- SR-186: retained. Its requirement and acceptance already state the record duty and the line only asks, so its "no new machine gate" holds. Its rationale keeps mechanism-specific evidence with its current SR; no other SR owns this line, so LLR-360 and TC-399 add no conflict.
- SR-161: retained. Its perspective duty is unchanged, and the line is additive.
- TC-211: retained, and its fail stands. None of its declared inputs moved in this range (`docs/test/inspection-procedures.md`, SR-161, SR-186, `docs/requirements/hats.toml`, the two wi-976 records), and the trace report still lists SR-186 as demonstrated, not mechanized, so TC-399 masks nothing.
- IF-115, IF-113, IF-175, IF-287: retained. No signature or parsed shape changed. I read these rows' scope from the plan and the code's contract comments, and a grep of `docs/requirements/interfaces.toml` found no row stating the slot's values.
- Other rows: a grep sweep of the LLR, IF, assumption and TC registries for the perspective and stopping terms found no contradicting row.

Decomposition record. LLR-360 is the retained child under SR-186. Its independent decision is how a round's brief asks for the stopping reason, on which sittings, and where the verdict writes it. A separate LLR would repeat LLR-360's round classification, slot and code with no independent decision, so further splitting would only duplicate. TC-399 verifies that behaviour by unit test; TC-211 keeps the independent purpose of inspecting an actual record.

Rubric. K1: each amended LLR-360 and TC-399 clause matches the code. K2: no SN or SR cell changed. K3: `Implements:` tags name LLR-360, whose `module` and `code_symbol` cover both functions; all ten new `Evidence` names exist in the diff; no Status flipped; the spec grants the amendment.

Notes, no finding. At this tip LLR-360 differs from its `docs/archive/last_approved` anchor in four cells and that snapshot has no change in the range, so the amendment act is still owed; the sitting records sit outside this stance's reading scope, so I judged the text, not that route. TC-399's `Expected` does not repeat the non-round state its `Method` exercises; nothing it says is false. One disclosure: the stance bars `docs/reviews/`, while the round facts order the specref read. I read that one file, `docs/reviews/wi-976/021-ADJUDICATE-095bb79.md`, a ruling on another lane that the spec quotes verbatim, and no other record under `docs/reviews/` or `docs/decisions/`.

Commands
- `git rev-parse HEAD` -> e849a83648a366ca690686d02b392468d06c39cd
- `pytest -q -p no:cacheprovider -n 2 --basetemp .../gb/wi-983 tests/test_plan_briefs.py tests/test_adjudicate_brief.py tests/test_module_size_ratchet.py` -> 163 passed in 113.79s
- `project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (996 work item(s), 883 done (89%), 34 cancelled, graph acyclic). exit 0
- `project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=138 LLR=331 TC=363 orphans=0 integrity=0 ... interface-findings=0. exit 0
- `project-trajectory/scripts/trace.py --strict` -> same line, exit 0
- `project-trajectory/scripts/gen_prompt_catalog.py --check` -> fresh (14 prompts)
- `scripts/check_resync.py` -> OK, 3 shipped path(s) changed; entry anchored at e73e49cf83e79e58897edbb7f5519028a1f3863f
- `project-trajectory/scripts/check_docs.py --root . --stale` -> OK, 0 broken
- `pytest tests/test_prompts.py tests/test_hats.py` -> 181 passed in 5.71s
- pre-fix and mutant runs, in a scratch export of the tip, since removed -> as stated above. A first mutant batch failed on my own escaping (import errors or no-op edits) and was discarded and rerun.

VERDICT: APPROVE findings=0
