# ADJUDICATE — WI-697 round 2 — TC-279 (DA-011) at f2bc66c1

This is the second sitting on TC-279, the observation of DA-011: the sampled
new-reader inspection. Round 1 ([001](001-ADJUDICATE-f2bc66c.md)) recorded
nothing, because its frame left out about a fifth of the back-linked parts.
The adjudicator for round 2 is an independent Claude Opus 5.5 session. It
directed none of the draw and none of the readers, and had read none of the
sampled parts before this sitting.

What the judgement used:

- the declared inputs: the rubric `docs/rubrics/sampled-new-reader.md` (R1,
  R2, B1, B2) and DA-011;
- the procedure in `docs/test/inspection-procedures.md#sampled-new-reader-inspection`;
- TC-279's cells: sample size 5, the acceptance rule and the Expected;
- the coordinator's round-2 draw scripts, both outputs, and the five reader
  statements;
- each part's code and its linked SR and LLR rows, read by this adjudicator
  at `f2bc66c1`.

Each statement is recorded beside its rows in
[SAMPLE-r2-f2bc66c.md](SAMPLE-r2-f2bc66c.md).

- [BLOCKER] The draw: population, randomness, and the coordinator's after-the-fact live-id restriction -> **Population: honoured.** It is every (file, enclosing symbol) pair that `gen_arch_map.declaration_sites` reports under `docs/stack.ini` `[paths]` `src` and `tests`, the surface `[readability]` measures: 516 parts, including module headers, module-level blocks and comment-linked functions. **Randomness: honoured.** The seed is `int(f2bc66c1…, 16)`, fixed by rule, and I reproduced both draws exactly. **Restriction: the sample stands, but not on the stated ground.** The unrestricted pick 3, `tests/test_trajectory_arch.py:1494 <module header>`, is a line inside the `MOD_A_SRC` fixture string. It names LLR-900 and LLR-901, which do not exist, and is the only site in that file. It is a frame blank, not "a part … with its own back-link". I checked the mechanics: that key sorts last (index 515), and the unrestricted stream's sixth draw is `_render_drill`. So the restricted sample equals the unrestricted stream with the blank skipped, which is exactly what a pre-stated rule "skip a drawn key that is not a part, take the next seeded draw" yields. The coordinator had no discretion over the replacement. I do NOT adopt the live-id criterion as the population definition. It is a proxy that keeps other fixture-string hits naming live ids: `tests/test_gen_arch_map.py`'s `<module header>` (line 580, inside `PROSE_MOD`) and `test_reverse_coverage_reads_non_python_source_but_not_unlisted_types` (lines 687 and 690). None was drawn, and all five sampled parts carry a genuine `Implements:` line of their own, so the skip rule gives this sample whatever else the frame holds. Not B2.
- [MINOR] R1: random parts, fresh non-author readers, reader kind and statements recorded beside the linked rows -> **Holds.** Each reader is a fresh Claude Sonnet 5.5 session, told that it did not author its part, that read only the part and the rows its `Implements:` names and did not ask the author. The record is now `SAMPLE-r2-f2bc66c.md` plus the result section. **Registry files rather than "through the generated views": does not break R1.** R1's text does not name the views. The views are generated from these same registry cells, so the readers read the same records in their source form, which gives a reader no more help, so the deviation cannot have produced the pass. It is a deviation from the procedure's letter and is recorded as one.
- [MINOR] Part 1, `gen_arch_map.MAPPING_FINDING_POLICY` (SR-163, LLR-276) -> **Agrees.** The class-to-severity mapping is exactly the code's. "Fails only on a gate-class finding" is `mapping_purpose_report`'s `ok`. The purpose is LLR-276's one-table rationale and its no-flag-day burn-down. The open notes, OI-72 and whether overrides exist, concern references outside the part. The one consumer call, line 2267, passes the default policy.
- [MINOR] Part 2, `session_service.KeepWarmer` (SR-227, LLR-270) -> **Agrees.** The route filter (`bounds_one_turn`), the tick order, the daemon thread through `act`, `_once`, recording only over a clean trunk, and `finish` dropping the logs over a dirty trunk all match the code and LLR-270's keep-warm clause. The purpose matches SR-227's "one bounded turn that never blocks the scheduler". The reader read the in-flight `due_routes` call as read-only, and that is correct.
- [MINOR] Part 3, `consolidate.close_refusal` (SR-220, LLR-210) -> **Agrees.** The four rungs and then `reabsorption_refusal`, the six refusals and "specific cause before generic drift so the message names the row" are all the code's own. The purpose is SR-220's refuse-by-name, one-successor and no-re-absorption rules, and LLR-210's `close_refusal` clause. One soft slip: the reader called `rows` and `where` "unused-looking", but they are forwarded to every rung. It was offered as an uncertainty, not as part of the account, and does not touch behaviour or purpose. The reader's note that LLR-210 does not spell out the scope and digest rungs is accurate and is no contradiction.
- [MINOR] Part 4, `gen_release_checklist._rejudge_checklist_line` (SR-215, LLR-255) -> **Agrees.** Exact. The Required checkbox names the release command and the `due_cases(root, "HEAD", checkpoint="release")` count, and on `RejudgeError` it says why rather than showing zero. The purpose is LLR-255's person's-act checklist item, read through rejudge's pure decision because the checklist may not import intake.
- [MINOR] Part 5, `traj_render._render_drill` (SR-054, LLR-100) -> **Agrees.** The layer divs with non-root layers hidden, `nav.crumbs` with a per-root aria-label, `data-root-crumb`, the trace bar for `when`/`sw` only, and `DRILL_SCRIPT` are all as described. The purpose is LLR-100's never-without-a-way-back breadcrumb. The reader could not say WHY only `when` and `sw` get the trace bar. That reason is in neither the part nor its linked rows. `DRILL_STYLE`'s trace rules cite LLR-285, which is about contrast, and I found no SR or LLR naming the focused trace. Ruled not B1: the reader stated that branch's behaviour correctly and the part's purpose in agreement with its rows. It is surfaced below as finding 1.
- [MINOR] B1, a reader who cannot explain the part, or who contradicts its rows -> **Does not hold.** All five readers stated what their part does and why it exists, without asking the author, in agreement with the linked rows. Every "could not explain" note concerns code outside the part, an external reference (an OI, a plan section, a WI), or the reason for one sub-branch that the records do not carry (part 5). None is a failure to explain the part's behaviour or purpose, and none contradicts a row. R2 holds.
- [MINOR] B2, an author-selected sample or a claim about unsampled parts -> **Does not hold.** No author chose a part. The after-the-fact restriction changed one pick, and it changed it to exactly what a pre-stated skip-blank rule yields (ruling above). This verdict makes no claim about unsampled parts. **The pass establishes nothing beyond these five parts.** It bounds discovery and does not show that DA-011 holds for parts the sample did not reach. It also does not settle round 1's part 3, `sn_all_ids`, which a person may still overrule to `fail` on that sample.

**Outcome.** R1 and R2 hold, and neither B anchor holds. `pass` is recorded
with `record_observation.py --tc TC-279`, by "Claude Opus 5.5 adjudicator,
WI-697 round 2; readers: 5 fresh Claude Sonnet 5.5 sessions". The result
section in `docs/test/inspection-procedures.md` is updated, keeping its
heading and anchor and noting round 1. The test-case registry is untouched.

## Non-blocking findings (surfaced, not acted on)

1. **`_render_drill`'s trace-bar branch has no recorded reason.** It is the
   focused trace on the `when` and `sw` drills only. The part links SR-054 and
   LLR-100, the breadcrumb, and no spine row I found names which drills get a
   focused trace or why. This is a small live instance of DA-011's Obstacle:
   a reason that lives outside the part's records. The fix is a back-link to
   the row that owns the focused trace, or a row for it if none exists. It is
   not a sample failure: the reader explained the part.
2. **The harvest counts fixture strings in `tests/` as back-links.**
   `declaration_sites` scans lines, so `Implements:` text inside a test's
   string literal becomes a site keyed to its enclosing symbol, or to
   `<module header>` at module level. That made the round-2 frame carry at
   least three non-parts: the one dropped, and the two kept in
   `tests/test_gen_arch_map.py`. The procedure should name the skip rule for a
   drawn non-part before the draw. Better, the enumeration should exclude a
   site inside a string literal that is not the enclosing symbol's own
   docstring, so that no restriction has to be stated after the fact. Whether
   other consumers of `declaration_sites` over `tests/` see the same noise was
   not checked.
3. **Round 1's finding 2 still stands.** This result lives in a file that
   TC-209, TC-210 and TC-211 declare as an input. TC-279's own declared
   inputs (the rubric and DA-011) are not touched by this edit.

OUTCOME: RECORDED result=pass
