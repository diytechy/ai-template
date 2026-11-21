## 2026-11-21 — WI-1017: an LLR yields to a sustainable design; PROCESS.md §5 says it once and the readers point at it

Deferred open items: none — the causes outside the guidance are work rows
filed on trunk at the landing (WI-1018 to WI-1020) or the review-churn plan's
phase 3, which the queue-drill hand-off puts to the operator.

Review: Sol (`gpt-6.1-sol`, low) reviewed the whole branch alone; Gemini
Argon was not run, since it timed out at 900 seconds on every run in this
sitting and is skipped (operator, 2026-11-21). CHANGES-REQUESTED, two
findings, both fixed:

- [MAJOR] The causes outside the guidance were named and not filed: rows 1
  to 3 are filed on trunk at the landing as WI-1018 to WI-1020, row 4 is
  covered by the review-churn plan's phase 3, put to the operator, and the
  Deliverable and this fragment say so (`1af9e6326`).
- [MINOR] Three readers restated §5's prohibition on bending the design:
  every reader keeps its own instruction and the §5 pointer only, and the
  pin now fails a reader that shares a five-word run with the statement,
  speaks of bending the design, or lists the re-cut's verbs; red on the
  prior text for five readers, green after (`41fce6e27`). After the fixes:
  the eight modules they reach, `308 passed, 1 skipped in 280.27s`;
  `test_plan_filing`, `32 passed in 40.57s`.

Built on the maintenance branch `maint/wi-1017` from `0d67302bd`, with the
commit hooks on. The record of the sample, case by case, is in the row's
Deliverable (`../archive/work/complete/WI-1017-llrs-yield-to-design.md`).

- **The sample, first** (`3d6ad6fe1`, with the plan). Every entry naming an
  LLR in the decisions records of the thirteen most recent lanes (92 of 145),
  the thirteen maintenance rows since, the review verdicts of wi-960 to
  wi-1002, the latest handbacks, the retirement records and WI-1015's
  measurement. No lane changed a behaviour to fit an LLR's text, and many
  reshaped rows with their design; but when the design changed shape the row
  set did not (WI-1007's five-module split minted no design row and bounded
  its cut by the rows that existed; no retirement was a re-cut; 48 of 345
  LLRs list more than ten symbols), and row text was left trailing the code
  at the end of a lane (eight entries, mostly by the post-gate MINOR rule).
- **The guidance** (`d1d221c82`). PROCESS.md §5's design-replacement bullet
  states once that an LLR records the current design, not a commitment: the
  rows are split, merged, moved or retired (`retire.py`) under their tier's
  authority when a sustainable design needs it, the parent keeps its
  acceptance, moving code that keeps every row true moves trace cells only,
  and keeping an unsuitable row to avoid an act is a finding. The chart gains
  the re-cut. The spine-authoring skill ("keep IDs where meaning remains" and
  what to do where it does not), its in-lane reference, the spine questions'
  §3, the worker and reviewer briefs, the builder agent and the kit-change
  and scope-critique rubrics point at it. The builder agent and K3 tag new
  code with the LLR whose stated behavior it implements, not the one whose
  module is the file.
- **Causes outside the guidance, not built:** work ids are minted on trunk,
  so the coordinator files rows 1 to 3 there at the landing, from the
  Deliverable's descriptions: WI-1018 (row text a lane leaves stale is filed;
  seven rows listed as its first set), WI-1019 (WI-1001's rule has no LLR)
  and WI-1020 (accepted rows amended only by addition; one case, the
  operator may cancel it). Row 4, the containment rule, is covered by the
  review-churn plan's phase 3 (variant F), whose rows are the operator's
  call, put to them in `../plans/2026-11-21-queue-drill/HANDOFF.md` §3.
- **Decisions:** `docs/decisions/maint-wi-1017.toml` D-001 (the
  coordinator's procedure is outside this row's homes), D-002 (no spine row
  minted; the pin rides `tests/test_prompts.py`'s file-level tag).
- **Nearest existing homes:** the pin sits beside
  `test_both_builder_briefs_search_before_minting_a_file_or_function` in
  `tests/test_prompts.py`; the statement replaces §5's existing
  design-replacement bullet rather than adding a section.
- **Tests:** the pin red on the base text, green after. The modules the
  change reaches (19, listed in the Deliverable): `658 passed, 1 skipped in
  404.37s (0:06:44)`; `test_bootstrap.py -k "byte_caps or size_budget or
  baselines"`: `3 passed in 11.78s`. `check_trajectory.py --strict` clean,
  `trace.py --strict` `orphans=0 integrity=0`. The unfiltered suite was not
  run (the coordinator runs it per wave).
- **Byte deltas:** `PROCESS.md` 100,990 -> 101,691 (+701, watched,
  re-stamped); `byte-budget-guard/SKILL.md` 4,613 -> 4,610 (cap 5,000);
  `spine-authoring/SKILL.md` 19,630 -> 19,744; `in-lane.md` 5,135 -> 5,212;
  `spine-questions.md` 21,623 -> 21,532; `reviewer.template.md`
  12,058 -> 11,900; `worker.template.md` 8,901 -> 8,885. `AGENTS.template.md`,
  `CLAUDE.md` and `PROCESS_OPTIONS.md` untouched.
- **RESYNC:** one entry `[since 0d67302bd]`; nothing forced.
