# WI-902 plan, revision 2: the close validates an adoption once and records it; the commit check judges the record; the sweep trusts it

## Revision 2: what changed, and why

This is the plan's one allowed revision, answering critique 1
(`docs/plans/WI-902/critique-1.md`, one MAJOR finding, F1).

**F1 is confirmed.** Revision 1 put the combined sitting (old P10) before
the counted review rounds (old P11, whose predecessor was P10). The
coordinator-cycle skill orders them the other way. §3 "Iterate" runs code-only
counted rounds; §3 "Checkpoint" starts "when a counted round has no BLOCKER
or MAJOR", reconciles the spine against the settled code, sits once, and
then runs the uncounted gate ("A counted round always precedes the
checkpoint, and the gate follows it"). §4 then takes the act only after the
rebase and the unchanged-rows check. Revision 1 also put the act in the
checkpoint row, ahead of the rebase §4 requires first. Read in that order, a
round's fix would land after its rows were judged, which costs another
reconciliation and sitting.

**The fix: the old P10 and P11 become three rows, in the skill's order.**
- **P10, iterate.** The bar on the lane tip, then the counted full rounds
  with their coverage plans, disputes and convergence map, until a round has
  no BLOCKER or MAJOR.
- **P11, checkpoint and gate.** Terra reconciles P8's intent set against
  P10's settled code. Then the closure check, the one combined sitting, the
  restore of the trunk-only views, and the uncounted gate in convergence
  stance.
- **P12, land.** The rebase, a repeat checkpoint and convergence round only
  if the rebase changed code or rows, the unchanged-rows check, the act
  turn, D17's proof, the full suite, the squash landing and the bar on the
  landing tip.

P8 is now intent only: authored once, `Drafted`, and not sat. Its
reconciliation and pre-sitting checks move to P11. The predecessor cells,
the clause cross-index and the detailed sections are changed to match.
Rows P0 to P7 and P9 are unchanged in substance; only their cross-references
to P10 and P11 are re-pointed.

The lane tip is now `bd6d7debd`. It differs from `41375927d`, where the code
below was read, only by `docs/plans/WI-902/` (the plan and its critique), so
every code reading below stands. WI-911 is in `complete/`, so the
skill shape D18 names is the one on the lane today.

Planner (revision 1): fresh session, 2026-10-20. Spec, read in full:
`docs/work/active/wi-902/WI-902-disposition-adopts-existing-successor.md`.
Its specref is the review-churn plan's item 2
(`docs/plans/2026-10-11-review-churn/README.md#2-record-the-decision-at-its-event-checked-at-the-commit`).
The rulings it relies on, also read: the lane record
(`docs/plans/2026-10-11-review-churn/wi-902-lane-record.md`), with the five
calls it cites in `docs/decisions/coordinator-2026-10-14.toml` (D-009 to
D-013) and D-014 (deliverable 10 kept in the row); review 015
(`git show d3d301216:docs/reviews/wi-902/015-REVIEW-A-97ea2e4.md`); and the
record-at-event rule, now `project-trajectory/PROCESS.md` §3, "Record a
decision where it is made".

**Code read at the lane tip `41375927d`** (the re-cut lane, equal to trunk):
- `intake.py`: `parse_dispositions`, `_TOML_FENCE_RE`, `_DRAFT_KEYS`,
  `_successor_drafts`, `_disposition_drafts`, `_apply_supersedes`, `_mint`,
  `_write_mint`, `_mint_message` and `intake_after_merge`;
- `handback.py`: `_loop_commit`, `_adjudication_close_text`,
  `_consolidation_close`, `_archive_one_adjudication_row` and
  `close_adjudication`;
- `text_then_act.py` in full;
- `integrate.py`: `_text_then_act_refusal` and `_each_lane_commit`;
- `check.py`: the step table and `_text_then_act_refusal`;
- `plan_gate.py`: its rider, `landing_refusal` and `_squash_lines`;
- `acceptance_record._commit_parents`;
- `kitlib/verdict.mechanical_close_attestation`;
- `kitlib/registry.py`: `WI_COLUMNS`, `SPEC_SCALARS`, `SPEC_LISTS`,
  `adjudicates_tokens` and `parse_spec_row`;
- the column lists in `wi_convert.py` and `plan_artifacts.py`;
- `consolidate._section_blocks`;
- `agent_loop.dispositions_drafted`;
- `agent_policy.adjudication_review_owed`;
- the shipped `hooks/pre-commit` step list.

`intake.py` and `text_then_act.py` are byte-identical to the old lane's base
`ccd66391`. `handback.py` has moved only in `_lane_verdict` and
`_machine_line_refusal` (WI-925's undeclared-trunk refusal), so the lane's
handback edits port without conflict.

**The old lane, read at `d3d301216`:**
- `git diff ccd66391 d3d301216` over `intake.py`, `handback.py`,
  `kitlib/adoption.py`, `kitlib/bootstrap_manifest.py`, the prompt,
  `RESYNC_PACK.md` and the five test modules;
- LLR-335, TC-360 and IF-294 as the lane wrote them;
- `docs/decisions/wi-902.toml`.

**Tests read:**
- `tests/conftest.py` (`SLOW_MODULES`, `hooks_on`);
- `tests/test_text_then_act.py`, for its test names and the remedy pin.

**Rows of record:**
- the item's SRs, SR-148 and SR-220, in
  `docs/requirements/system-requirements.toml`;
- the TCs that verify them, in `docs/test/test-cases.toml`: TC-058,
  TC-059, TC-060, TC-091, TC-097, TC-143, TC-146, TC-154, TC-183, TC-208,
  TC-254, TC-260, TC-313, TC-314 and TC-331. A row names each, or an
  `Excludes:` line at the end gives the reason it is left out. TC-147 and
  TC-156 do not verify either SR on trunk today, but the Done-when re-sits
  them, so rows name them too;
- LLR-153, LLR-161, LLR-181, LLR-298, LLR-302, LLR-312 and LLR-337, in
  `docs/requirements/low-level-requirements.toml`;
- in `docs/requirements/interfaces.toml`: IF-040, IF-047, IF-078, IF-079,
  IF-090, IF-092, IF-102, IF-123, IF-134, IF-137, IF-159, IF-161, IF-173,
  IF-175, IF-186, IF-244 and IF-295 (plan_gate's exit-code row, the
  precedent for the new one);
- CMP-006, CMP-007 and CMP-008, in `docs/requirements/components.toml`;
- `docs/runtime-flows.md`, Flow 4.

**Runtime flows: no edit.** Flow 4 draws the merge slot and its post-merge
intake arm, but none of the close, the per-commit rungs or the hook steps.
This row changes only those, so Flow 4 stays true as drawn.

**Ids not yet in the registries.** LLR-335, TC-360 and IF-294 have no row on
trunk: the re-cut dropped them, and D-011 keeps their ids. The coverage gate
validates cited ids against the lane's registries, so this plan names those
three in prose and in titles only, never in a `Covers` or `Interfaces`
cell. The new rows' ids are not minted until P8 either.

## Architectural delta

The row does three of the four things.

**It adds a value to a domain.**
- The work-item row gains a declared `Adopted` column (front-matter key
  `adopted`), beside `Adjudicates` and `Digests` (D-012).
- The `## Dispositions` grammar gains a second block shape, the adoption
  block `adopts = "WI-NNN"`.
- The section grammar tightens: fences must pair.

**Outputs depend on a new input.**
- The close's output, the closed spec, now carries the record, and the
  record depends on the request and on the lane HEAD's registry.
- The sweep's re-point now depends on the record.
- A per-commit verdict depends on the record and the request, at the commit
  and at its parent.

**It crosses no new system boundary.**
- The commit check reads git trees, as `text_then_act` and `plan_gate`
  already do.
- The close already runs git in the lane worktree.
- The old lane's git-history read (`rev-list --first-parent`, the shallow
  boundary test) is not ported, so one input is removed.

**It adds new internal seams, and the plan's rows carry them.**
- The new module `scripts/adoption_record.py` (P4, P5). It holds the git
  side of the record: the tree reader at a revision, validation at a
  revision, the per-commit rule, and its staged form.
- `kitlib/adoption.py` (P1, P3). It is pure, and owns the request grammar,
  the disposed-id reader, the validation rule, the record's strict reader
  and the record-change judgement.
- Two interface rows for `adoption_record.py`: a call row to `handback` and
  `text_then_act`, and an exit-code row to `scripts/check`, mirroring
  IF-295. IF-294 is re-added with its Contract rebuilt. All of these are
  minted and amended in P8.

There is no state machine to extend. The record is data on a terminal row,
written once.

DELTA: within

## Steps, in build order

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Port the old lane's record into the re-cut lane: reviews 001 to 015, adjudications 004/006/007/009/011/013 with their request and dispute files, the six adjudicator call logs, and `docs/decisions/wi-902.toml` with each entry marked kept, re-made or withdrawn per the lane record's part (b); add the lane decisions the rebuild owes (round count restarts at zero at review 016; the reviewer shape the coordinator-cycle skill carries; acts 113 to 117 not ported) | D17; D18; SR-148 | IF-047 (the review verdict files are ported byte for byte; no seam change) | |
| P1 | One complete-section parser with fence pairing, and the pure adoption module ported from d3d301216 (block parser, disposed-id reader, validation rule over a supplied listing; `work_specs` not ported), its bootstrap MAPPING row, and the repository-wide grammar census | D3; D11; D12; D20; D1; SR-148 | IF-090; Proposed: the pure kitlib adoption call seam, re-added under the lane record's kept id; nearest existing IF-090 (intake's call surface) falls short because the new owner is a kitlib module shared by the close, the sweep and the commit check, not intake | P0 |
| P2 | The mint's lineage corrections (deliverable 10, the lane's D-003 and D-004), ported: a replay keeps an already-minted draft in the successor set, and a title match on another lineage refuses before any write | D3; D10; D22; SR-148; TC-147 | IF-244; IF-186; IF-090 | P0 |
| P3 | The record's cell: the declared `Adopted` column in the registry reader, the converter and the plan-artifact column list, documented in the WI-000 template; its one strict reader and the pure record-change judgement in the adoption module | D3; D1; SR-148 | IF-092; IF-078; IF-079; IF-159 | P1 |
| P4 | The close validates once, in the lane HEAD's tree, and writes the record in the rewrite that clears `specref`; the consolidation arm refuses an adoption before its first write; the new `adoption_record.py` holds the tree reader and validation at a revision | D1; D2; D3; D4; D11; SR-148; SR-220; TC-254; TC-156; TC-331 | IF-137; IF-173; Proposed: the adoption-record module's call seam (validation at a revision for handback, the per-commit rule for text_then_act); nearest existing IF-175 (kitlib/verdict's record readers) falls short because it reads verdict records and owns no git tree reads of work specs | P1; P3 |
| P5 | The commit check: one rule judging a commit against its parents, riding `LANE_COMMIT_RIDERS` at the merge slot, and a staged form run by the pre-commit hook's new `adoption-record` step (with its own squash-landing walk); the record never borrows text-then-act's remedy; the peel's stated premise names the record | D3; D5; D6; D7; D8; D9; SR-148; TC-313; TC-173 | IF-040; IF-134; IF-175; IF-173; Proposed: the adoption-record exit-code seam to scripts/check, the same shape as IF-295 (plan_gate), which falls short only because its owner is plan_gate | P4 |
| P6 | The sweep trusts the record: it compares the request with the record, re-points from the record beside the drafts, and refuses an unreadable merged spec; none of the old lane's history readers is ported | D1; D2; D3; D10; D11; D21; SR-148; TC-147 | IF-244; IF-090 | P2; P3; P4 |
| P7 | The consumer text: the disposition prompt teaches the adoption form and the lane-tree rule, and the prompt catalog is regenerated; recipes §8 says an adopting disposition closes through `handback.close_adjudication` and lands inside the squash, and §3's citation of act 117 is replaced; the skill copies are synced | D1; D2; SR-148 | no interface (prompt and skill prose; the catalog and the skill copies are regenerated by their own steps) | P4; P6 |
| P8 | The spine at intent, authored once after the first build round and not sat: SR-148's acceptance re-stated; LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254 amended where the rebuilt code needs it; LLR-335 and TC-360 re-added Drafted in record-at-close text; the commit check's new LLR and TC minted Drafted; IF-294 re-added as rebuilt; the two new adoption-record interface rows minted; Implements tags and Contract headers retagged (D-005 re-made); existing statuses unchanged | D13; D14; D15; D16; SR-148; SR-220; TC-147; TC-156; TC-254 | IF-102; IF-161 | P1; P2; P3; P4; P5; P6; P7 |
| P9 | The RESYNC_PACK.md entry: one entry anchored at the trunk commit the lane is rebased on, naming the three tightenings, the kit-owned files and no forced migration | D19; D20; D21; D22; SR-148 | IF-244; IF-134 (adopter-facing prose naming the sweep's new refusals and the hook's new step) | P5; P6; P7 |
| P10 | Iterate, before any sitting: the bar on the lane tip after each build round, then the counted full review rounds in the skill's shape from review 016 (count from zero, at most three, the third in convergence stance after its convergence map), each with its coverage plan, threat-model triage and dispute sittings, until one round has no BLOCKER or MAJOR; code fixes only, row-text proposals go to the spine change list | D18; D23; F1; SR-148; SR-220; TC-147; TC-156; TC-254; TC-313; TC-173; TC-331 | no seam crossed beyond P1 to P7's (fix rounds stay inside the rows' declared interfaces; a fix that needs a new one stops the round, skill §3 Iterate step 8) | P8; P9 |
| P11 | The checkpoint, after the settled rounds, then the gate: Terra reconciles P8's intent set and the spine change list against P10's settled code; the closure check and both strict lints; one combined sitting (SR-148 and the six re-sat rows, first approval of LLR-335, TC-360 and the check's rows, the interface rows stated); returns routed and re-sat; the trunk-only views restored; then the uncounted gate in convergence stance over the checkpoint tip | D13; D14; D15; D16; D18; F1; SR-148; SR-220; TC-147; TC-156; TC-254 | IF-123 | P10 |
| P12 | Land, after the gate: rebase onto trunk and re-anchor the RESYNC entry; a repeat checkpoint and an uncounted convergence round only if the rebase changed code or authored rows; the unchanged-rows check; the act turn above trunk's ledger top; the five old act commits proven absent; the full suite once; the squash landing (whose own hook runs the new step); the bar again on the landing tip | D17; D19; D23; F1; SR-148; SR-220; TC-147; TC-156; TC-254; TC-313; TC-173; TC-331 | IF-123; IF-134 (the landing commit meets the hook) | P11 |

Excludes: TC-058; TC-059; TC-060; TC-091; TC-097; TC-143; TC-146; TC-154; TC-183 — they verify SR-148's work-selection order (the frontier and its ordering, the safety classifier, the generated status surface, the structural safety cross-check, the dual-plan class, the admission table, the adjudication kind's rank slot, admission order with the red-TC census, the gap census); none of that code (`schedule`, `dispatch` admission, `census`, the status generators) changes here, and SR-148's amended acceptance adds only a third way an unresolved handback is resolved, which TC-147 and TC-360 carry. The full suite at P12 still runs them.

Excludes: TC-314 — pending open-item citation integrity (LLR-299) reads `needs` tokens that cite open items; the adoption carries none, and the re-point P2 and P6 extend rewrites only work-item edges, which TC-147 covers.

Excludes: TC-208; TC-260 — the consolidation census and its command (LLR-210, LLR-264) read only `consolidate._enacted_supersedes`, which this row leaves unchanged because an adoption carries no `supersedes`. P1's `test_an_adoption_never_counts_as_an_absorption` pins that. The one consolidation behaviour this row adds, the close refusing an adoption, is TC-254's.

### Clauses covered by more than one row

Each row does a separate part.

- **D1:** the parser (P1), the cell (P3), the close (P4), the sweep (P6) and
  the prompt (P7).
- **D2:** the close's discharge rule (P4), the sweep's OI-73 guard (P6) and
  the prompt's wording (P7). See "D2" below.
- **D3:** every row that adds a test (P1 to P6).
- **D10:** the mint's replay correction (P2) and the sweep's recorded
  re-point (P6).
- **D11:** the parser (P1), the close (P4) and the sweep (P6).
- **D13 to D16:** the rows authored at intent (P8), and reconciled and sat
  at the checkpoint (P11).
- **D17:** the decision recorded at the port (P0), and the ancestry proof
  at the act and again on the landing tip (P12).
- **D18:** the lane decision (P0), the counted rounds run in that shape
  (P10), and the gate in that shape (P11).
- **D19:** the entry written (P9), and re-anchored after the rebase (P12).
- **D20, D21 and D22:** built in P1, P6 and P2, and named in P9.
- **D23:** the bar on the lane tip at every round (P10), and on the landing
  tip (P12).
- **F1:** the order is iterate (P10), then checkpoint and gate (P11), then
  land (P12); each row's predecessor is the one before it.

### Every commit meets the smoke bar

Every row ends at the per-commit bar (`run_menu.py smoke` within 60 s).

- A row that grows a ratcheted module re-stamps it in its own commit, in
  `tests/test_module_size_ratchet.py` or `docs/complexity-baseline`, with a
  reason line.
- Git-repo tests go in modules listed in `tests/conftest.py`
  `SLOW_MODULES`: `test_handback`, `test_intake`, `test_consolidate_close`,
  `test_verdict_record`, `test_text_then_act`, `test_wi_convert`, and the
  new `test_adoption_record`, which P5 adds to the set.
- Each family keeps an in-process pin in the smoke module
  `tests/test_disposition_adoption.py`.

## P0: port the lane's record (D17, D18)

**What is ported, unchanged.** These are the lane's record, and land with
it (lane record, "Mechanics"):
- `docs/reviews/wi-902/` 001 to 015;
- the six adjudications 004, 006, 007, 009, 011 and 013, each with its
  `.requested` file;
- the three `NNN-DISPUTE-findings.toml` files;
- the six `docs/iteration/call_*-20261011-*.log` files.

Each is copied with `git show d3d301216:<path>` and committed alone, as
record.

**`docs/decisions/wi-902.toml`.** It is copied from `d3d301216` with each
entry's status written into it, following the lane record's part (b):
- D-001 is withdrawn, under plan ruling 2.
- D-002 is re-made; P11 finalises its stamp at the reconciliation.
- D-003 and D-004 are kept.
- D-005 is re-made; P8 retags.
- D-006: F1 is withdrawn (ruling 2 supersedes ruling 009's mechanism),
  and F2 is kept.
- D-007: F1 is withdrawn, and F2 is kept and moved to the close.
- D-008 is kept, amended in P8.
- D-009 is withdrawn, with act 117.
- D-010 is kept, folded into P1.

Kept and re-made entries stay open for the owner to confirm or overrule, as
the lane record lists them.

**The new decisions:**
- **D18.** A lane in flight when the review shape landed "starts its count
  at zero at its next review, recorded as a decision" (coordinator-cycle
  SKILL §3, "Rounds, the cap and the convergence round"). The decision says
  that count starts at zero at review 016. It also names the reviewers,
  and the model behind each REVIEW file, by the skill's current roles.
- **D17.** Acts 113 to 117 (`a2a95f847`, `7c4544ef3`, `acab09035`,
  `a588ae83f` and `97ea2e47d`) are not ported, and no seq between 113 and
  117 is taken by this lane (D-009, D-010).

**Not ported:**
- the act commits;
- their `docs/archive/last_approved/` copies, their `acts.toml` rows and
  their README lines;
- the lane's own spec edit (the amended trunk spec governs);
- the lane's `docs/id-watermark` and `docs/complexity-baseline` edits.
  Both are regenerated where the rebuild needs them.

**No test.** This is record, not behaviour. The proof for D17 is P12's
ancestry check.

## P1: one complete-section parser and the pure adoption module (D11, D12, D20)

**`project-trajectory/scripts/kitlib/adoption.py` (new).** Ported from
`d3d301216`:
- `KEY`, `OPEN_STATES`, `parse_block`, `disposed_id`, `row_refusal` and
  `_hits`.

Not ported:
- `work_specs` (the close no longer reads trunk's working tree);
- the docstring's landing-tree paragraph.

The module stays pure: no git, no writes.

The repeated-id rule ("an id that another block already adopts") is
enforced where the section is assembled. `_hits` keeps its open-state
filter.

Its `bootstrap_manifest.MAPPING` row is ported, re-worded so that its
readers are `intake.py`, `handback.py` and `adoption_record.py`.

**`intake.py`:**
- `parse_disposition_section(text, where)` is the one parser, returning
  `(drafts, adoptions, refusal)`.
- `_section_block` is ported.
- `parse_dispositions` stays a wrapper that returns drafts only. Its
  callers (`agent_loop.dispositions_drafted`, `integrate._verdict_owed`,
  `handback`, `_successor_drafts`) keep their shape.

**What is new: fence pairing**, the S3 grammar. Within the section:
- every line that begins with three backticks must be either an opening
  `` ```toml `` or a bare closing `` ``` ``;
- the fences must alternate, open then close, starting with an open;
- the count must be even.

Anything else refuses the whole section, naming the line, before any block
is read. Only then are the blocks harvested, from the paired fences, so the
complete-fence regex can no longer skip an unclosed block.

The prose between blocks (each draft's `scope`) is cut at the same pairs as
today.

`consolidate._section_blocks` stays as it is. The Trust section rules the
historical absorption reader unchanged and skips a bad block, and no
consolidation verdict carries an adoption (P4 refuses one).

**Tests, in `tests/test_disposition_adoption.py`** (new, smoke, pure). Each
says what it fails on at trunk.

- Ported from `d3d301216`. Each is red at trunk: the module and the
  adoption shape are absent there, so `adopts` is refused as an unknown
  draft key.
  - `test_an_adoption_block_is_parsed_apart_from_the_drafts`;
  - `test_a_malformed_adoption_block_is_a_parse_refusal` (another key
    beside `adopts`, and a value that is not one id);
  - `test_the_disposed_row_is_read_from_either_minted_title_form`;
  - `test_acceptance_is_read_against_the_registry_with_distinct_refusals`.
    It is re-fixtured over a supplied listing, without `work_specs`, and
    covers missing, closed, unreadable (non-UTF-8 bytes, front matter that
    does not parse) and non-superseding rows;
  - `test_an_adoption_never_counts_as_an_absorption`.
- `test_a_repeated_adoption_is_a_parse_refusal`: two blocks adopt the same
  id. Red: trunk refuses the unknown key, not the repeat, and the test
  asserts the repeat's reason.
- `test_a_valid_block_then_an_unclosed_one_is_refused`, parametrised over an
  adoption pair and a draft pair. This is review 015's reproduction at the
  parser. Red: for drafts, trunk's
  `_TOML_FENCE_RE.findall` returns the first draft with no refusal, so the
  second is lost silently. The adoption variant fails on the unknown key.
- `test_a_fence_that_is_not_toml_or_a_bare_close_is_refused` (for
  example, `` ```text `` inside the section). Red: trunk ignores it.
- `test_every_dispositions_section_in_the_repository_passes_the_fence_grammar`
  (D12). It walks the files `git ls-files` lists under `docs/work/`,
  `docs/archive/work/` and `docs/reviews/` that carry a `## Dispositions`
  section, and asserts that the fence-pairing step refuses none.
  - For specs, it also asserts that the new parser returns the same drafts
    trunk's parser returned, compared through a frozen copy of trunk's
    regex in the test.
  - This is a census, not a red-first test. To show the instrument is live,
    the same test feeds it one planted unpaired copy and asserts a refusal.
  - A probe at planning time found 66 such files on trunk, all paired.
  - Verdict files are checked for fence pairing only, because a verdict's
    `## Dispositions` may hold prose and no block.

## P2: the mint's lineage corrections (D10, D22)

**Ported from `d3d301216`** (D-003, D-004; D-014 keeps them in the row):
- `_standing_successors`, `_title_identity_refusal` and `_repoint_owed`;
- `_apply_supersedes`, now returning its edits;
- `_supersede_source_refusal(..., adopted=())`, `_mint(..., adopted=())`,
  `_write_mint(..., adopted=())` and `_mint_message(..., adopted=())`.

The `adopted` parameter defaults to empty, so P2 lands before the record
exists. P6 then fills it.

**Tests, in `tests/test_intake.py`** (slow):
- `test_a_replay_re_points_a_late_dependent_to_the_full_successor_set`.
  It is ported in a drafts-only form first, and P6 adds the adoption form.
  Red: trunk's dedup drops the already-minted draft before the lineage is
  built, so a dependent filed after the first sweep stays on the closed
  row.
- `test_a_title_match_off_the_drafts_lineage_refuses_the_mint`. It asserts
  exit 1, the rows named, and nothing written. Red: trunk swallows the draft
  and returns `([], None)`.
- `test_a_drafts_title_match_on_its_own_lineage_stays_standing`. Red: the
  partition does not exist at trunk.
- `test_a_replay_with_nothing_left_to_re_point_commits_nothing`. This is a
  pin of `_repoint_owed`. It may pass at trunk for drafts, and it is kept
  because P6's adoption-only replays depend on it.

## P3: the record's cell (D1)

**The column:**
- `kitlib/registry.py`: an `Adopted` entry in `WI_COLUMNS`, with a comment
  in the voice of `Adjudicates` and `Digests` (the drop-at-the-one-moment
  reason), and `("Adopted", "adopted")` in `SPEC_LISTS`. The generic list
  join carries it through as data.
- `wi_convert.py`: the same entries in its `COLUMNS` and key map.
- `plan_artifacts.py`: its column list gains `Adopted`.
- `project-trajectory/work/WI-000.template.md`: a paragraph documenting the
  key. Only the close writes it, as a non-empty TOML list of WI ids, and a
  row that adopts nothing carries no key.

**The registry readers grant the cell nothing.** `parse_spec_row` does not
validate it, so a malformed record does not break every registry read. The
three consumers that act on it refuse it through the one strict reader.

**The strict reader:** `kitlib/adoption.record_ids(data, where)` returns
`(ids, refusal)`:
- an absent key answers `None`;
- it accepts only a non-empty list of distinct, well-formed WI ids;
- it refuses a bare string, an empty list, a table, a non-string element, a
  repeated id and a malformed id.

**The record-change judgement:** a pure function in `kitlib/adoption.py`
that P5 wraps. It takes the record each parent holds for a spec, the
commit's record and request, whether the spec moved into `complete/`,
whether the commit is the machinery's close, and the validation result. It
returns the S3 commit-check case: pass, or a named refusal.

Putting it here lets the whole S3 table be pinned in the smoke tier, with
git kept out.

**Tests:**
- `test_disposition_adoption.py` (smoke):
  - `test_the_record_reader_accepts_only_a_list_of_distinct_ids`: every
    shape above. Red: the reader is absent.
  - `test_an_adopted_cell_survives_the_spec_row_reader`:
    `parse_spec_row` returns `Adopted == "WI-1;WI-2"`. Red: trunk drops
    the key, and the column is absent.
  - `test_the_record_change_table`: one case per S3 commit-check row.
    The close's own commit with record equal to request and validation
    passing passes. Anything carried unchanged passes. A merge's value
    held by any parent passes. Refused: a record added, changed or
    removed outside the close; a record that differs from the request; a
    record that fails validation; a requesting spec moved into
    `complete/` with no record. Red: the function is absent.
- `test_wi_convert.py` (slow):
  `test_an_adopted_cell_round_trips_through_the_converter`. The spec
  written by `write_spec_file` reads back cell-exact. Red: the column is
  absent.

## P4: the close validates once and writes the record (D1, D2, D4, D11)

**`adoption_record.py` (new, CMP-008, beside `plan_gate.py`).**
- `tree_specs(root, rev)` and `_tree_text(root, rev, path)` are ported from
  the lane's `intake._tree_specs` and `_tree_text`. They keep strict UTF-8
  and LF normalisation (D-007 F2 kept, moved).
- `validate_at(root, rev, title, owes, adoptions)` returns
  `(record, refusal)`:
  - the disposed id comes from the title (`kitlib/adoption.disposed_id`);
  - each id passes `row_refusal` over `tree_specs(root, rev)`;
  - the record is the request's ids in block order.
- A tree git cannot list is a refusal, never a fallback.

The module's MAPPING row joins the bootstrap manifest.

**`handback._archive_one_adjudication_row`:**
- It reads `parse_disposition_section` once.
- `owes_successor` is discharged by drafts or adoptions.
- `_consolidation_close(..., adoptions)` refuses an adoption before its
  first write (ported).
- Then `adoption_record.validate_at(wt, "HEAD", ...)` runs, before any
  move. The lane's HEAD is the tree the closing commit is made on, and so
  that commit's parent.
- `_adjudication_close_text(text, deliverable, adopted)` writes
  `adopted = [...]` into the front matter in the same rewrite that clears
  `specref`. The line sits where `wi_convert.write_spec_file` would
  serialise the key, so a converter round trip of the closed spec is
  byte-stable.
- On any refusal, nothing moves and no record is written, and the
  refusal names the reason. Validation runs before the first move of each
  row.
- `close_adjudication`'s existing loop over a multi-row lane is unchanged.
  Its behaviour when a later row refuses after an earlier row moved
  predates this row, so the tests here are single-row. If the builder sees
  that gap, it is surfaced as a finding, not fixed inline.

The old lane's `intake.adoption_lineage` is not ported, nor its read of
trunk's working tree (`root`). The close reads the lane's tree.

**Tests, in `tests/test_handback.py`** (slow). Their fixtures file the
successor on trunk before the lane is cut, as WI-893 was filed before
WI-894's lane (lane record, "Survives").

The trunk baseline every adoption test fails against: trunk refuses an
`adopts` block as an unknown draft key, or as "drafted NO successor".

- `test_an_adoption_of_a_superseding_row_closes_and_writes_the_record`:
  - the spec is in `complete/`;
  - its front matter holds `adopted = ["WI-…"]`;
  - `specref` is cleared;
  - the close's commit carries the machinery's subject.
- `test_an_adoption_that_is_not_accepted_refuses_the_close`, parametrised
  over four adopted rows: missing, closed (in `complete/` and in
  `cancelled/`), unreadable (committed non-UTF-8 bytes, and front matter
  that does not parse, which gives the distinct "cannot read" reason),
  and non-superseding. Each case asserts that the lane worktree's
  `git status --porcelain` is empty, HEAD is unchanged, the spec is still
  in `active/<branch>/`, and no file contains `adopted =`.
- `test_an_adoption_without_a_disposition_event_token_refuses`, with the
  same write-nothing asserts.
- `test_a_repeated_adoption_refuses_the_close`, with the same asserts.
- `test_a_drafted_successor_beside_an_adoption_still_mints`:
  - the close writes the record;
  - the merge sweep mints the draft (a new id);
  - a dependent of the closed row ends on both successors.

  This one needs P6. It is written here and goes green at P6. The P4
  commit carries the test xfail-strict with P6 named, and P6 removes the
  marker; or the builder moves the test into P6's commit.
- `test_a_valid_block_then_an_unclosed_one_refuses_the_close`, parametrised
  over adoption and draft (D11 at the close). Red: for drafts, trunk
  closes and the second draft is lost; for adoptions, the unknown-key
  refusal is a different reason, and the test asserts the fence reason.

Then:
- `tests/test_consolidate_close.py` (slow):
  `test_a_consolidation_verdict_that_adopts_refuses_the_close` (ported),
  asserting the lane tree is byte-identical. Red: trunk refuses on the
  unknown key, not by this reason.
- Kept green as regressions: TC-156's handback suite and TC-331's
  `test_an_unreadable_claim_is_never_closed_early`.

## P5: the commit check (D5 to D9)

**The rule:** `adoption_record.commit_adoption_record_lines(root, rev)`.

**Parents.** It reads the commit's parents with
`acceptance_record._commit_parents`, the one parent reader of the per-commit
rules. A parent the repository cannot read, including one behind a shallow
boundary, is a line naming it, never a root (TC-313's precedent).

**What it reads.** It runs one
`git diff --name-only --no-renames <parent> <rev> -- docs/work
docs/archive/work` per parent. If no spec path is touched, it returns `[]`
with no further read, so a lane's ordinary commits cost one git call each.

**What it judges.** For each touched spec, keyed by the WI id in its file
name, across both spec roots and every state folder, it reads:
- the record at the commit and at each parent, with `record_ids`;
- the request at the commit, read only when the record changed or the spec
  moved into a `complete/` folder.

It then applies P3's judgement. "The machinery's close" is
`kitlib.verdict.mechanical_close_attestation(root, rev) is not None`, with
the WI id among its closed ids. This is the shape the peel already
verifies: one parent, paired moves out of one `active/<branch>/` into
`complete/`, and the composed subject. The peel and the check therefore
agree on which commit is the close.

For the close, validation is `validate_at(root, parent, title, ...)`. It is
the same function P4 ran, in the same tree.

**A merge** is judged by what neither parent carried. Merges and the
moves after a landing (`complete/` to the archive's `complete/`) carry
the record unchanged, and pass.

**A residual stated, not built against.** A close whose `spec_move` relink
reaches outside `docs/work/` is not peeled today, and the check also reads
it as not the machinery's close, so it is refused. That is fail-closed and
consistent with the peel: a person re-closes it. The prompt (P7) and the
recipes need no workaround for it.

**Where the rule runs:**
1. **The merge slot.** The rule is appended to
   `text_then_act.LANE_COMMIT_RIDERS`, as Deliverable 3 and the Trust
   section direct, so `integrate._each_lane_commit` judges every lane
   commit with it.
   - The slot's rung currently appends `TEXT_THEN_ACT_REMEDY` to whatever
     line any rider returns. That rung's composition changes so the remedy
     is added to text-then-act lines only. The record rule's lines carry
     their own remedy: "only `handback.close_adjudication` writes the
     record; close the row through it".
   - The rung's label, "text and act", becomes the walk's.
2. **The pre-commit hook.** It runs as a new `adoption-record` step:
   - a row in `check.py`'s step table, with
     `[sys.executable, adoption_record.py]` as its command (IF-295's
     shape, `plan_gate`'s precedent);
   - the step name in the shipped `hooks/pre-commit` `--run-steps` list;
   - a comment block beside `text-then-act`'s in that hook.

   `adoption_record.main` judges the index against HEAD, and against
   MERGE_HEAD while a merge is in progress. Outside a squash landing, any
   staged record change, or any requesting spec moved into `complete/`, is
   refused. The close commits with `--no-verify`, so it never meets this
   step in that position.

**The squash landing in the hook.** The record step owns its squash
handling, rather than standing down on `text_then_act._squash_lines`.
That function's exemption is keyed to the approval-act registries, so a
squash whose spine matches the tip while its index carries a hand-edited
record would go unjudged.

When git's `SQUASH_MSG` names a tip that contains HEAD:
- a staged record equal to that tip's own record for the spec is exempt;
- the commits from HEAD to the tip are walked with this rule
  (`text_then_act.lane_commit_walk(root, commits, (rule,))`);
- any other staged record change is judged as above.

`text_then_act._squash_lines` then walks only text-then-act's own rule. Its
lines then never carry a record refusal under the wrong remedy, and its
tests stay green unchanged. The record is still judged on every squashed
commit, by its own step. This is recorded as a new lane decision, with
WI-913's `plan_gate` (its own rider, slot rung and squash walk) named as
the alternative. That alternative was passed over because the spec and
Trust name `LANE_COMMIT_RIDERS` for the slot.

**The peel's premise.** The docstring of
`kitlib.verdict.mechanical_close_attestation` now names the record ("the
record it adds is the request's validated result, which the adoption-record
rule verifies"). What it verifies is unchanged.

**Tests, in `tests/test_adoption_record.py`** (new, real git, added to
`SLOW_MODULES`). Every refusal test is red at trunk, because no such rule
exists and the commit is accepted.

- **D5:**
  - `test_the_closes_own_commit_passes`, made by the real
    `handback.close_adjudication`;
  - `test_a_later_commit_carrying_the_record_unchanged_passes`: the move to
    `docs/archive/work/complete/`, and an unrelated edit to the closed
    spec's body.
- **D6:**
  - `test_a_record_written_in_a_lane_commit_is_refused_at_the_slot`,
    through `integrate._each_lane_commit` with `LANE_COMMIT_RIDERS`;
  - `test_a_hand_close_writing_a_record_is_refused`: the right move under
    a hand subject;
  - `test_a_record_staged_on_trunk_is_refused_by_the_hook_step`, through
    `adoption_record.main` and through `check.py --run-steps
    adoption-record`.
- **D7:**
  - `test_a_close_shaped_commit_whose_record_differs_from_the_request_is_refused`;
  - `test_a_close_shaped_commit_whose_adoption_fails_in_the_parent_tree_is_refused`:
    the adopted row was closed in the parent. The commit carries the
    composed subject and paired moves, built by hand so the peel's shape
    holds.
- **D8:** `test_a_record_changed_later_is_refused` and
  `test_a_record_removed_later_is_refused`.
- **D9:**
  `test_a_requesting_spec_moved_into_complete_without_a_record_is_refused`,
  at the slot and at the hook step.
- **Merges, parents and squashes:**
  - `test_a_refresh_merge_carrying_trunks_record_passes`: what neither
    parent carried;
  - `test_a_parent_behind_a_shallow_boundary_is_refused_by_name`;
  - `test_a_rebased_lanes_squash_landing_is_admitted`;
  - `test_a_squash_whose_index_edits_the_tips_record_is_refused`.
- **Wiring:**
  - `test_the_pre_commit_hook_runs_the_adoption_record_step`. Red: the
    step is absent;
  - `test_the_record_rule_rides_the_lane_commit_walk`.
    `LANE_COMMIT_RIDERS` contains it. Red: absent;
  - `test_a_record_refusal_at_the_slot_does_not_carry_the_text_then_act_remedy`.
    Red: today's composition appends the remedy to every rider line.

**Regressions.** TC-173's `tests/test_text_then_act.py` and TC-313's
`tests/test_ruling_sync.py` stay green unchanged. They pin the shared walk,
the parent reader and text-then-act's squash path.

## P6: the sweep trusts the record (D1, D2, D10, D11, D21)

**`intake._merged_dispositions(root, hit, relpath)`.** It returns
`(meta, drafts, lineage, refusal)`, ported without its history arm.

It refuses, with nothing minted:
- a merged spec it cannot read, or whose front matter does not parse (the
  old lane's refusal, kept; trunk skips such a spec);
- the four bad request and record pairs: a request with no record, a record
  with no request, the two differing, and a malformed record (through
  `record_ids`).

With no adoption, the OI-73 empty-section guard keeps its text and adds
"or adopted".

The lineage is `[(adopted, [disposed])]`, built from the record, with
`disposed` read from the title by `disposed_id`. An untokened title is a
refusal, never a guess. Nothing is validated, and no git or adopted-row
state is read.

**`_disposition_drafts`** returns `(drafts, lineage, refusal)`, and
`intake_after_merge` passes the lineage to `_mint` (P2's parameter).

**Not ported:**
- `_landing_commit`, `_UNLANDED`, `import retire`, `import functools`,
  `from kitlib import git as kgit`;
- `adoption_lineage`;
- intake's `_tree_specs` and `_tree_text`, which moved to P4.

**`_successor_drafts`** reads through the same parser, so an unpaired fence
in a SUCCESSOR Done-when verdict's section is refused there too.

**Tests, in `tests/test_intake.py`** (slow). Fixtures produce the record
through the real close (P4) where the case allows. Refusal cases write the
spec by hand on a fixture branch; the fixtures' hooks are stubs
(`hooks_on`).

The trunk baseline for the adoption tests is a refusal: trunk rejects
`adopts` as an unknown draft key.

- `test_a_recorded_adoption_re_points_a_dependents_needs`, minting nothing.
- `test_drafts_and_adoptions_together_hold_the_full_successor_set`.
- `test_a_replay_re_points_a_late_dependent_to_the_full_successor_set`,
  the adoption form beside P2's drafts form.
- `test_a_consumed_adoption_replays_after_its_successor_completes`
  (ported).
- `test_a_shallow_clone_sweeps_a_recorded_adoption`. It runs
  `git clone --depth 1 file://…` of the landed fixture, then
  `intake.py sweep --merged WI-…` in the clone, and asserts the re-point.
  This shows the sweep reads no history. Run it with `MSYS_NO_PATHCONV`
  unset (recipes §7's note).
- `test_the_sweep_refuses_a_request_and_record_mismatch`, parametrised
  over request with no record, record with no request, the two differing,
  and a malformed record. It asserts exit 1, nothing minted, no
  bookkeeping commit, and an unchanged dependent.
  - Request with no record: trunk refuses on the key, and the test
    asserts the record reason.
  - Record with no request: trunk ignores the unknown front-matter key,
    and the draft-less section passes or refuses for the wrong reason.
  - The other two: trunk has no record reader.
- `test_an_unreadable_merged_adjudication_spec_refuses_the_sweep`
  (ported). Red: trunk `continue`s past it and returns `([], None)`.
- `test_a_valid_block_then_an_unclosed_one_refuses_the_sweep`,
  parametrised over adoption and draft. Red, for drafts: trunk mints the
  first and drops the second.
- `test_a_successor_done_when_verdict_with_an_unclosed_block_is_refused`.
  Red: trunk's `findall` drops it.

Then:
- `tests/test_verdict_record.py` (slow):
  `test_the_scheduler_and_the_gate_read_an_adoption_by_its_shape` (ported).
  A well-formed adoption owes no review round, and a malformed section
  still fails toward review. Red: trunk's unknown-key refusal reads as
  review owed.
- Rewritten, not ported: the lane's
  `test_the_sweep_accepts_an_adoption_only_of_a_superseding_row` becomes
  the record-trusting case above. The five history-read regressions the
  lane record lists are not ported.

## P7: the consumer text (D1, D2)

**`prompts/adjudicate-disposition.template.md`.** Item 3 gains the adoption
form, re-worded from `d3d301216`:
- when a row superseding the closed one is already open, adopt it with a
  block holding exactly `adopts = "WI-…"`;
- an adoption mints nothing and is the same successor exit, not a third
  one.

The lane's sentence "the close and the merge accept it only while…" is
replaced. The close accepts an adoption only if that row is open and
supersedes the closed row in the lane's tree when the row closes, and it
records the adoption there.

The machine-line paragraph says `successors=` counts drafts and adoptions
together, and that a disposition which neither drafted nor adopted is
refused.

The catalog (`prompts/CATALOG.md`) is regenerated; the `prompt-catalog`
step checks it.

**`project-trajectory/skills/coordinator-cycle/references/recipes.md`,
synced to `.claude/skills/` and `.agents/skills/`** (`skills-sync` checks
the copies).
- **§8.** The "Until WI-902 lands" hand-close recipe is replaced: an
  adopting disposition closes through `handback.close_adjudication` and
  lands inside the squash, never by a hand close, which the adoption-record
  step refuses.
- **§3.** "(WI-902, act 117)" becomes a citation of the archived lane tip
  `d3d301216`, with no act number (D-009's withdrawal).

This is this repo's tooling, so it gets no RESYNC entry.

**D2.** The scope of OI-73's "no third exit" is kept. The prompt, the
OI-73 guard's message at the close and the sweep, and LLR-335's text (P8)
all state an adoption as the successor exit. The guard still refuses a
section that neither drafts nor adopts, and an open item alone still does
not discharge it.

**No new tests.** The `prompt-catalog` and `skills-sync` steps are the
checks. P6's empty-section regressions pin D2's refusal half at the sweep:
the existing trunk tests of the empty `## Dispositions` refusal are kept
green unchanged. P4's tests pin it at the close.

## P8: the spine at intent (D13 to D16)

This follows the coordinator-cycle skill §3, "Intent". The builder builds
P1 to P7 as the first round. Then Terra authors the whole change set once,
from SR-148 down, with the arms map. New rows are `Drafted`, and existing
statuses are unchanged. The coordinator verifies and commits the set with
no sitting. These rows give the P10 reviewers the obligations the code must
meet. The set is reconciled and sat only at P11, after P10's rounds settle
the code.

**Rows to be re-sat at P11, with text expected to stand.** Each is checked against
the rebuilt code:
- **SR-148.** The acceptance gains "or names an already-open item that
  supersedes it as its successor" (the lane's text, act 113's content).
- **LLR-153 and TC-147.** These are the mint's arms: an adopts-only block
  allocates no id, title identity and lineage are resolved together, and
  replays use the full successor set. Both gain SR-148. TC-147's Evidence is
  re-pointed at P2's and P6's tests by name.
- **LLR-161 and TC-156:** "drafts a successor, or adopts an already-filed
  one".
- **LLR-312 and TC-254:** a consolidation verdict that adopts refuses
  before its first write. TC-254's Evidence gains P4's consolidation test.

**LLR-335, re-added Drafted.** Its text is record-at-close, in contract
voice. Its detail names no function, under ruling 5. Its `module` and
`code_symbol` cells stay filled until plan item 5's schema lane.

It states:
- the request grammar;
- the disposed row read from the title's one event token;
- the open-state and `supersedes` rule;
- validation once, in the tree the closing commit is made on, with the
  record written in that commit;
- the sweep trusting the record and refusing the four bad pairs, a
  malformed record and an unreadable merged spec;
- fence pairing;
- the narrowed no-cell-change clause (D-006 F2).

The landing-tree, shallow-boundary and replay clauses are gone.

**TC-360, re-added Drafted.** It verifies SR-148 and LLR-335, and the
re-added seam row. Its Evidence names P1's, P3's, P4's and P6's tests.

**New LLR and TC under SR-148 for the commit check.** They take the next
free ids from `docs/id-watermark` at the spine step (today LLR-341 and
TC-371), or the floor the coordinator briefs, above WI-798's LLR-336 and
TC-361 to TC-366.
- The LLR has LLR-298's per-commit shape. It states:
  - the close's own commit, a carried record and a merge's
    neither-parent rule;
  - refusal of every other record change, and of a requesting spec moved
    into `complete/` without a record;
  - a parent that cannot be read, reported by name;
  - the slot walk and the staged step with its squash handling.
- The TC names P5's tests. Tier: `Full`. Its smoke pin is P3's
  `test_the_record_change_table`.

**Interface rows.** None of them carries an approval status.
- **IF-294, re-added** (D-008 kept, amended):
  - owner: `scripts/kitlib/adoption`;
  - requestors: `scripts/intake`, `scripts/handback` and
    `scripts/adoption_record`;
  - its Contract header in `kitlib/adoption.py` loses `work_specs` and
    gains `record_ids` and the record-change judgement.
- **Two new rows** for `scripts/adoption_record`:
  - a call row with requestors `scripts/handback` and
    `scripts/text_then_act`;
  - an exit-code row with consumer `scripts/check`, in IF-295's shape.

  Each has a Contract header in the module, and is CMP-008.

**Code tags (D-005, re-made).** Each `Implements:` line names every row its
function serves, per sitting 007's advisory 1:
- the shared parser serves SR-148, LLR-153 and LLR-335;
- `_archive_one_adjudication_row` serves SR-220, SR-148, LLR-312 and
  LLR-335;
- the rider serves SR-148 and the check's new LLR;
- `lane_commit_walk` and `_each_lane_commit` add that LLR to their lines.

CMP-008's notes name `adoption_record` if the `component-view` step asks.

**Generated references.** The derived references the hook checks
(`interface-reference`, `component-view`, `cli-reference`) are regenerated
in the lane. The trunk-only views are restored at P11, before the gate
(recipes §3).

**Size stamps.** Each row that grows a ratcheted module stamps it in its own
commit. D-002 is re-made at P11, with the settled `intake.py` stamp and its
reason. The lane's history readers do not return, so the rise is smaller
than 1854. D-002's alternative, decomposing the Dispositions parsing out of
`intake.py`, is weighed again and recorded as declined here: the
downstream rows the spec names (the batch's P4 and P5) edit `intake.py`'s
mint next. It stays for the owner.

**Check at intent:** `trace.py --strict` and `check_trajectory.py --strict`
with the commit bar, so the Drafted set is structurally whole before the
P10 reviewers read it. The closure check runs at P11.

## P9: the RESYNC_PACK.md entry (D19 to D22)

**One new entry under §3**, "A disposition can adopt an already-filed
successor", anchored `[since <sha>]` at the trunk commit the lane is
based on when P9 is written, so the P10 reviewers read it. P12 re-anchors
it at the trunk commit the landing is rebased on. The lane's entry is never
ported, so this one replaces it.

**"What changed"** states:
- the adoption block;
- the close's single validation and its `adopted` record;
- the hook's new `adoption-record` step and the slot rule (only the close
  writes the record);
- the sweep's trust of the record.

**It names the three tightenings:**
- **D20.** An unpaired fence in a `## Dispositions` section is refused, for
  drafts too, where a trailing unclosed block was silently dropped.
- **D21.** An unreadable merged spec, or one whose front matter does not
  parse, refuses the sweep (exit 1, the merge stands), where it was skipped.
- **D22.** A drafted title held by a row on another lineage, or by two
  rows, refuses the mint before any write, where the draft was swallowed.

**Kit-owned files to overwrite:**
- `scripts/intake.py`, `scripts/handback.py`, `scripts/text_then_act.py`,
  `scripts/integrate.py`, `scripts/check.py`;
- `scripts/adoption_record.py` (new);
- `scripts/kitlib/adoption.py` (new), `scripts/kitlib/registry.py`,
  `scripts/kitlib/verdict.py`, `scripts/kitlib/bootstrap_manifest.py`;
- `scripts/wi_convert.py`, `scripts/plan_artifacts.py`;
- `hooks/pre-commit`;
- `prompts/adjudicate-disposition.template.md`, `prompts/CATALOG.md`;
- `work/WI-000.template.md`.

**"What to do":** no registry or setting migration. Before the first sweep
after upgrading, check:
- that no merged `complete/` spec has unparseable front matter;
- that no pending `## Dispositions` section has an unpaired fence;
- that no pending drafted title is already a row's title under another
  `supersedes`.

The sweep now stops on each, naming the file or rows.

**Check:** reviewers verify the anchor with `git merge-base --is-ancestor`,
as review 015 did.

## P10: iterate, in counted rounds, before any sitting (D18, D23, F1)

This is coordinator-cycle skill §3, "Iterate" and "Rounds, the cap and the
convergence round". It runs after P8's intent set and P9's entry are
committed, and before anything is sat.

**Each round:**
1. Confirm the round's commit landed (`git log -1` moved).
2. **The bar on the lane tip:**
   - `run.cmd smoke` (`run_menu.py smoke`), with its wall time under 60 s;
   - `check_trajectory.py --strict` clean;
   - `trace.py --strict` with no finding beyond LLR-292's.
3. The full-lane reviewers, in the skill's shape under Roles, each from its
   own brief rendered by `review_brief.py review --scope full` from the
   lane's trunk base to its tip, and filed with `review_brief.py file`.
   The first counted round is review 016, and its count is zero before it
   (P0's decision, D18).
4. Triage under the review threat model, a `Plan-WI` coverage plan per round
   file through `plan_coverage.py --findings`, findings confirmed or refuted
   on the real code path, and a dispute sitting for a contested finding.
5. Fixes are code and trace fields only (`Implements:`, the LLR module and
   symbols, TC Evidence). Proposed row text goes to the lane's spine change
   list, for P11.

**The cap.** At most three counted rounds. The third renders `--stance
convergence`, after the convergence map is recorded in the lane's
decisions. At the cap, every open BLOCKER or MAJOR goes to one dispute
sitting. P10 ends at the first counted round with no BLOCKER or MAJOR. P11
starts only then.

**The Done-when hold.** No Done-when change is planned. If one arises, a
verdict bound to its exact text, or an owner ruling, comes before the next
build round.

**No new tests.** P10 adds the regression test each accepted finding's fix
needs, red before the fix, through the coverage plan.

## P11: the checkpoint, then the gate (D13 to D16, D18, F1)

This is coordinator-cycle skill §3, "Checkpoint". It starts when a counted
P10 round has no BLOCKER or MAJOR.

**1. Reconcile.** Terra, resumed, reconciles P8's whole set against the
settled code: the spine change list P10 accumulated, plus the arms map.
This includes D-002's final `intake.py` stamp and TC Evidence names that a
fix round renamed. The coordinator verifies, regenerates and commits it
before the sitting. The turn is omitted only if no round proposed row text
and no code moved since P8, recorded with the mechanical check the skill
names.

**2. The closure check** passes (`spine-authoring`,
`references/in-lane.md`), and `trace.py --strict` and
`check_trajectory.py --strict` are clean.

**3. One combined sitting**, composed by `coordinator_adjudicate.py
adjudicate --brief combined`, top-down. It covers:
- SR-148's amendment;
- the re-sit of LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254;
- the first approval of LLR-335, TC-360 and the commit check's LLR and TC;
- the interface rows, stated in their final form (they carry no status).

The sitting ends at its committed verdict. Its act is P12's. Returns are
routed per the skill (text to Terra, code to the builder). The returned
rows, and any chain or row they change, are re-sat.

**4. Restore** the trunk-only generated views on the lane (recipes §3).
The module-size stamp stays.

**5. The gate.** The full-lane reviewers run uncounted over the checkpoint
tip, from the lane's trunk base, with `review_brief.py review --scope full
--stance convergence`, after the convergence map. They review code and rows
together. An open BLOCKER or MAJOR goes to the dispute sitting. A fix round
it orders is followed by one more checkpoint (steps 1 to 4) before P12.

## P12: land (D17, D19, D23, F1)

This is coordinator-cycle skill §4, after P11's gate.

**1. Rebase** onto current trunk (recipes §3 and §4). P9's entry is
re-anchored `[since <sha>]` at the trunk commit the lane now sits on. If the
rebase changed code or authored rows, P11's affected checkpoint steps are
repeated and an uncounted convergence round runs over the rebased tip.

**2. The unchanged-rows check.** The rows the P11 verdict judged, read at
the verdict's own commit, are compared with the rebased tip. A changed or
renumbered row is re-sat.

**3. The act turn**, `coordinator_adjudicate.py act --verdict <path> --wi
WI-902`, takes its acts at one above trunk's ledger top at that time. It is
the lane's last spine commit.

**4. D17's proof.** For each of `a2a95f847`, `7c4544ef3`, `acab09035`,
`a588ae83f` and `97ea2e47d`, `git merge-base --is-ancestor <sha> <lane
tip>` exits 1. Also, `docs/archive/last_approved/acts.toml` on the lane
adds only rows above trunk's top, each citing this lane's own verdicts.

**5. The full suite once**, alone on the box: `python -m pytest -q -n
auto`. Its real output is pasted into the log.

**6. The squash landing.** The squash's own commit meets the hook, so the
new `adoption-record` step judges the squash by its tip's commits. Then the
row is closed, the tips archived, and the sweep run (recipes §3).

**7. The bar on the landing tip** (D23): the smoke tier within 60 s, read
quiet; `check_trajectory.py --strict` clean; `trace.py --strict` with no
finding beyond LLR-292's. D17's ancestry check is re-run there.

The landing lands alone (spec S1, "Landing"; skill §4, a lane that changes
the machinery the cycle runs on). It changes the close, the sweep and a
hook step.

## Risks the builder should know

- **The squash condition (P5).** The text-then-act squash exemption is keyed
  to the approval-act registries. The record step must not stand down on it.
  P5's last squash test is the pin.
- **The peel/check agreement (P5).** Both read
  `mechanical_close_attestation`. If the builder finds a legitimate
  adopting close whose relink leaves `docs/work/`, that is the residual
  stated in P5, and it is reported, not widened.
- **Smoke budget.** All new git tests are in slow modules. The smoke pins are
  pure, so the 60 s tier should not move. Measure it at each commit.
- **Shallow-clone tests on Windows.** Run them with `MSYS_NO_PATHCONV` unset
  (recipes §7). A sandboxed `sh.exe` failing CreateFileMapping is a
  launcher limit, not a finding (review 015's note).
