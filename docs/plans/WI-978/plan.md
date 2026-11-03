# WI-978 implementation plan, revision 2: one mint across parallel lanes (the watermark carrier, the reserved-only landing, keep-or-mint)

Planner: a fresh session that did not write the spec and will not build it. This is the plan's one
allowed revision. I read the lane worktree `C:/Projects/ai-template.wt/wi-978` at tip `29d51a164`
(revision 1's plan at `e62eea418` plus its critique). Sources:

- the spec, `docs/work/active/wi-978/WI-978-watermark-carrier.md`, with its specref (review-churn
  plan item 16) and the OI-116 ruling it quotes;
- the code the spec's Trust table names: the `trace.py` watermark section; `integrate.py`'s
  `_merge_refusal`, `_merge_ready`, `integrate_one`, `_minted_id_refusal`, `_merge_trunk_in` and
  `refresh`; `check.py`'s `held-status` squash arm; `kitlib/git.py`'s `squash_commits`;
  `plan_gate.py`'s squash reader; `rejudge.py`'s archive extraction; the bootstrap manifest; the
  shipped pre-commit hook's `--run-steps` list; `scripts/check_resync.py` (in the commit bar);
- the rows SR-174, TC-147, TC-148, TC-158, IF-101, LLR-153 and LLR-154, plus CMP-006 and CMP-008,
  in `docs/requirements/system-requirements.toml`, `docs/test/test-cases.toml`,
  `docs/requirements/interfaces.toml` and `docs/requirements/components.toml`;
- runtime flow 4 in `docs/runtime-flows.md`;
- the coordinator text this row replaces or touches: SKILL §4 (the latch sentence and the
  "renumbered row counts as changed" rule), recipes §3 (the hand landing's squash bullet) and §4
  (the floor briefing and the rebase row), and `scripts/coordinator/terra-spine-prompt.template.md`
  with its slot pin in `tests/test_prompts.py`.

The ids drafted below follow today's marks (`LLR = 361`, `TC = 400`): the new rows are drafted as
LLR-362, LLR-363, TC-401 and TC-402. They do not exist yet, so the table's `Covers` cells name them
in prose only; the coverage gate accepts only existing `TC-###` ids there.

## The critique's findings, judged

Both findings are claims. I checked each against the spec and the code before changing anything.

- **F1 (the carrier fold on the hand-squash landing): confirmed.**
  - D12 says "the landing folds the carrier into trunk's watermark". Revision 1 folded only in the
    station refresh (P7). The hand landing (recipes §3) is `git merge --squash <lane>` on trunk,
    whose staged watermark is the lane's own copy, and P8 only judged it. A carrier moved after the
    lane's last fold therefore landed unfolded.
  - The same gap exists at the merge slot, which the critique did not name. The refresh is usually
    speculative, outside the slot (`refresh`'s docstring), and the slot's `--no-ff` merge lands the
    branch tip's tree as it is. A reservation between that refresh and the slot is not folded
    either.
  - Revised in P2, P7, P8, P11 and P12 (below). The slot treats a tip whose watermark lags the
    carrier as not merge-ready, and refreshes in the slot, so it folds. The squash's recipe folds
    in the staged squash, and the squash step refuses a staged watermark that lags the carrier.
    Each caller gets a test where the carrier moves after the lane's fold.
- **F2 (renumbering after the final act): confirmed.**
  - Revision 1's P13 sat and acted on the new rows. P15 then rebased, reserved, and allowed the
    same rows to be renumbered. SKILL §4 says "a renumbered row counts as changed; re-sit any
    changed row", and the act is the lane's last spine commit after the final rebase (SKILL §4
    steps 1 and 2). The order broke both rules.
  - Revised: the final rebase, the self-reservation and any renumbering now come first (P14). The
    checkpoint sitting and the act follow on the final numbering (P15). The landing (P16) depends
    on that act, and loops back to P14 if trunk moves before it.

A third defect, found while re-reading: revision 1 wrote the RESYNC entry late (P14). But
`check_resync.py` runs in the commit bar and refuses a commit touching a shipped path until an
entry exists. P2 is the first such commit. The entry is now placed in P2's commit, anchored at the
lane's base, and refined in P13 (recipes §3, "RESYNC").

## The architectural-delta answer

DELTA: within

The answer follows the `architecture-decomposition` skill, one step per clause. F1's fix adds one
input to an existing output (the slot's readiness), and that input is recorded below.

1. **Mode classes: it adds a state.**
   - The repository gains the carrier ref `refs/heads/id-carrier`. It has two mode classes:
     *absent*, and *present at tip T*.
   - Transitions:
     - absent to present happens at the first reservation, seeded from trunk's committed
       watermark;
     - T to T' happens at each later reservation, by compare-and-swap;
     - a lost swap or a refusal is no transition.
   - A lane's or landing's watermark relative to the carrier gains two classes: *holds the fold
     of T*, or *lags T* (a carrier mark above the file's, or a carrier record the file lacks).
   - The working watermark gains a mode the code must now handle: *clean*, or *conflicted*
     mid-merge or mid-rebase, with index stages 2 and 3.
   - These go into `docs/runtime-flows.md` (P12).
2. **Value domains: it adds values.**
   - The id-watermark file gains a line kind: `# reservation: <SPACE> <low>-<high> (<WI-NNN>)`.
   - The space domain splits into *carrier spaces* (every watermark space except WI, OI and DP,
     deny-by-default) and *trunk spaces*.
   - The count domain is the integers 1 to 50.
   - The landing's refusal domain gains the six-row landing table. At the squash caller it also
     gains "the staged watermark lags the carrier", which is how that caller enforces the fold
     (F1).
   - These domains are recorded as the form of IF-101 (`data`) in
     `docs/requirements/interfaces.toml` (P1).
3. **Dependency table: outputs gain new inputs.** The table is recorded here, as the skill allows
   when planning; new cells are in **bold**.

| Output | Inputs (existing; **new**) |
|---|---|
| hand-raise verdict (`--strict-integrity`, every commit) | marks, live maximum, committed marks, correction records; **reservation records in the commit's own file**; **committed reservation records, unioned across every parent** |
| `--bump-ids` / `--correct-mark` / the trunk mints' file | marks, live maximum, corrections; **records, carried verbatim** |
| reservation (carrier commit, range) | **carrier tip; trunk's committed watermark; trunk's claim; counts; the space list** |
| fold (working watermark) | **receiving file, clean or stages 2 and 3; carrier tip; receiving tree's live ids** |
| merge-slot readiness (merge now, or refresh in the slot) | ancestor relation, the tip's `Bar-Green:` attestation; **carrier tip against the tip's watermark (the fold lag)** |
| merge-slot landing verdict | landing tree, trunk, claim (R1); **carrier tip; live ids added landing-over-parent; landing and parent records** |
| squash pre-commit verdict | index, HEAD, the squashed lane commits; **the same new inputs as the slot's verdict; the fold lag of the staged watermark** |
| station refresh result | trunk, lane; **carrier tip; a conflict on the id watermark** |

4. **New boundaries, and the descent.**
   - The landing (`scripts/integrate`) and the squash step (`scripts/check`) become requestors of
     the watermark seam, so IF-101 gains them (P1). The carrier ref crosses to git, which the kit
     already uses.
   - Component descent: I compared three cuts.
     - (a) Everything in `trace.py`. Rejected: it is ratcheted, and the spec routes the new code
       elsewhere.
     - (b) One new stdlib module, `id_carrier.py`, in CMP-006, composed by `trace.py` the way it
       composes `retire.py`. **Kept.**
     - (c) The landing check inside `integrate.py`. Rejected: it has two callers, and
       `check.py` would then import the integrator.
   - Under (b), every outside caller enters through `trace.py`, IF-101's one owner. The
     trace-to-`id_carrier` edge stays inside CMP-006, so no new interface row and no
     `components.toml` change is needed. Placement is derived from the new LLR's `module` cell
     (revision 35).
   - The new module imports nothing from `trace.py`. Trace hands it the parsed marks and the
     live-id sweep, so no import cycle forms.
   - The fold lag is one pure predicate in the module, with two callers (the slot's readiness and
     the squash step). It is not a second definition of the fold: it asks whether folding the
     carrier into the file would change the file's marks or records.
   - No refactor this item does not own is needed. Moving `trace.py`'s existing watermark section
     into the module stays out of scope (spec S5).

## The table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The intent spine set, TC first: SR-174 amended (kept, widened; `sn_refs` gain SN-027), TC-158 amended, the carrier LLR and the landing LLR drafted (the landing LLR carries the fold at landing on both callers), with their two TCs, and IF-101's `data` and `requestors` updated; ids drafted under today's floor briefing | D1; D2; SR-174; TC-158 | IF-101 | |
| P2 | `id_carrier.py`: the record grammar, the carrier-space set, the count and work-item parsers, the pure fold, the pure fold-lag predicate, carrier read and write by plumbing with compare-and-swap, the pure landing judgement; shipped in the bootstrap manifest; the RESYNC entry first written in this commit (the first shipped-path commit), anchored at the lane's base | D4; D8; D12; D20; F1; SR-174 | IF-101 (composed by its owner `scripts/trace`); the trace-to-`id_carrier` call is intra-component (both CMP-006), so no interface row is demanded | P1 |
| P3 | Every watermark writer carries the records: `render_watermark`, `--bump-ids`, `--correct-mark`, and through them the intake, OI and plan-artifact mints; the three committed-baseline readers share one parent walk | D9; SR-174; TC-158; TC-147 | IF-101 | P2 |
| P4 | The hand-raise rule re-founded on the record: a rise covered by a well-formed record in the commit's own file passes, one above every record is refused, a committed record altered or deleted is refused across every parent (a union), a reservation line never reads as a correction | D9; SR-174; TC-158 | IF-101 | P3 |
| P5 | The verbs: `trace.py --reserve-ids WI-NNN SPACE=N[,SPACE=N...]` (the S3 table, compare-and-swap, first use seeds from trunk, floor = max(carrier, trunk committed) + 1, folds into the working file) and `trace.py --fold-ids`; WI, OI and DP refused as trunk-minted (OI-116 (a)) | D5; D6; D7; D8; D24; D25; SR-174; TC-158 | IF-101 | P4 |
| P6 | The landing check, one function: added = live in the landing tree and not in the parent, under the watermark's own sweep over each tree; judged against the carrier tip's records for the landing's work item; the six-row table; and `trace.landing_fold_lag` over a rev's watermark for both callers | D10; D11; D12; F1; SR-174 | IF-101 | P5 |
| P7 | Caller 1, the merge slot: the reserved-ids rung beside R1 in `_merge_refusal`; a tip whose watermark lags the carrier is not merge-ready, so the slot refreshes it in the slot (the pessimistic sequence), and the refresh folds; the refresh folds the carrier in and resolves a conflict on `docs/id-watermark` alone by the fold | D11; D12; F1; SR-174; TC-148 | IF-101 (`scripts/integrate` joins its requestors) | P6 |
| P8 | Caller 2, the hand squash: a `reserved-ids` step in `check.py` beside `held-status`, through `kitlib.git.squash_commits`, judging the six rows and refusing a staged watermark that lags the carrier (naming `--fold-ids`); added to the shipped hook's batched floor; the lanes-containing-tip read lifted into `kitlib.git` with the plan gate as its second caller | D11; D12; F1; SR-174 | IF-101 (`scripts/check` joins its requestors); IF-040; IF-134 | P6 |
| P9 | The act machinery untouched: no edit to the act ledger's writer, readers, numbering or latch; their tests pass unmodified | D13 | no interface: verification only, no code change | P7; P8 |
| P10 | Keep-or-mint text: PROCESS.md §4 beside the CLARITY and MEANING paragraph, stated once; `spine-questions.md` §0 cites it in one line; the `byte-budget-guard` delta and restamp | D14; D15; D16 | no interface: prose only | |
| P11 | The coordinator text: the spine-author prompt drafts from reserved ranges (`@RESERVED@`), with no `--bump-ids` and stop-and-report; recipes §4 "reserve before drafting" and the fold rebase row; recipes §3's squash bullet gains the fold in the staged squash; SKILL §4 latch sentence; shipped and dogfooded copies in sync | D12; D17; D18; F1 | no interface: procedure text and this repo's coordinator tooling under `scripts/coordinator/`, outside the component map | P5 |
| P12 | Runtime flows: flow 4 draws the refresh fold, the slot's fold-lag readiness and the reserved-ids rung; a new flow draws a reservation, its fold and its two landings, with the carrier's mode classes; the code headers' IF-101 and IF-145 contract text | D10; D12; F1; SR-174 | IF-101; IF-145 | P7; P8 |
| P13 | Shipping: the RESYNC entry, written in P2, refined to its final content (a forced change for an adopter running lanes; trunk-only repositories unaffected; no file migrates; `--bump-ids` no longer the lanes' minter; the new hook step, the squash fold, and the shipped module) | D19; D20 | no interface: docs | P8; P11 |
| P14 | Final rebase and own ids, before any sitting: rebase onto current trunk; reserve this row's own LLR and TC ids through the built verb; renumber the drafted rows if the ranges differ; commit the folded watermark | D21; F2; SR-174 | IF-101 | P9; P10; P11; P12; P13 |
| P15 | The checkpoint on the final numbering: Terra reconciles the set against the built code (evidence and `code_symbol` bind); one sitting judges every row; the act from its verdict on the released rungs is the lane's last spine commit; a later rebase re-runs the unchanged-rows check and re-sits a changed (or renumbered) row before the act is re-taken | D2; D3; F2; SR-174; TC-158; TC-147; TC-148 | IF-101 | P14 |
| P16 | The landing: only from P15's act at the final rebase (trunk moved since P14 sends the lane back to P14); every other open lane that adds carrier-space ids named; the squash folds the carrier in; generated pages regenerated on trunk; the commit bar green; both strict lints clean on the landing tip | D19; D21; D22; D23; F2; SR-174; TC-147; TC-148; TC-158 | no interface: verification and trunk regeneration | P15 |

Every TC that verifies SR-174 is named: TC-158 (amended, P1, P4, P5), TC-147 (the intake mint,
run in P3, P15 and P16) and TC-148 (the merge slot, run in P7, P15 and P16). The two new TCs are
drafted in P1 and bound in P15. No clause and no finding is excluded.

## The steps

Order in the lane follows the spec: the spine set first (P1), then deliverable 1 (P2 to P5), then
deliverable 2 (P6 to P8). P10 and P11 may go in any commit after the plan's pass record.

- Each build row ends at the commit bar (`run.cmd smoke`, or `run_menu.py smoke` from a shell).
- Before a row's code commits, its new tests are run against the row's parent commit, to confirm
  they fail as stated.
- Every new function stays inside its complexity baseline.
- Each growth in a ratcheted module (`trace.py` 3741, `integrate.py` 1743, `check.py` 1339) is a
  reviewed exact bump in `tests/test_module_size_ratchet.py`, with its reason.
- `id_carrier.py` stays under the 1000-line threshold.

### P1: The intent spine set (D1, D2)

The coordinator dispatches Terra's intent turn with `CHANGES=none` and `HATS` set to the SN ids
the set reaches: SN-025, plus SN-027, which SR-174's new `sn_refs` name. The brief's target
meaning is the spec's "The spine" section. This is the last brief under today's floor briefing
(spec: "This row's own new ids ... are minted before the carrier exists"):

- every open lane's ids are given as a floor;
- Terra runs `--bump-ids` once.

The rows:

- **SR-174, amended and kept.**
  - `requirement`: the delivered content allocates each identity it mints at most once. Work
    items are minted on the integration branch alone. The registry identities that parallel
    lanes author are drawn from one shared reservation record. No two concurrent actors receive
    the same identity, and an identity freed by a deletion is never re-issued.
  - `acceptance_criteria`: the current three clauses, plus three more:
    - reservations in sequence or at once, from any bases, receive disjoint ranges;
    - a landing that adds a registry identity outside its own work item's reservation is refused
      before it lands;
    - a mark rises only by allocation, by a ruled correction, or by a recorded reservation.
  - `sn_refs`: gain SN-027.
  - `rationale`: carries the keep-or-mint cross-reference the spec records. It names the users
    of SR-174 as rows only: LLR-153, LLR-154, TC-147, TC-148, TC-158, and the SR-170 and SR-173
    rationales.
  - No file or symbol is named in any SR cell.
- **LLR-362 (new), the carrier and its reservation record** (CMP-006).
  - Contract voice: the carrier holds the id watermark for the lane-minted spaces.
  - A reservation moves the carrier in one compare-and-swap, and appends one record per space:
    the space, an inclusive range, and the work item.
  - Only the reservation writes a record, and only the fold copies one.
  - Committed records are append-only across every parent.
  - Every writer of the watermark carries the records verbatim.
  - The watermark may be named, since it is a shipped boundary artifact.
- **LLR-363 (new), the landing admits only reserved identities.**
  - It states the spec's landing table.
  - It states the fold at landing: each landing lands a watermark that holds the fold of the
    carrier tip it read. The automated landing refreshes a lagging tip; the hand landing folds
    in the staged squash and is refused while its watermark lags. A refresh conflict is
    resolved by the same fold.
- **TC-158, amended.**
  - `method` and `expected` gain four cases:
    - a raise justified by a record;
    - a raise above every record, refused;
    - a committed record altered or deleted, refused;
    - a bump and a correction that keep the records.
  - `evidence` gains the P3 and P4 tests.
- **TC-401 (new; verifies SR-174, LLR-362, IF-101).** Sequential and concurrent reservations are
  disjoint (the folded sittings rule). Each refusal of the reserve table is driven with nothing
  written. The fold is checked on a clean file and on a conflicted one. Proposed tier: `Full`.
  The git-driven cases are slow; the in-process pins stay in smoke.
- **TC-402 (new; verifies SR-174, LLR-363, IF-101).** Each landing-table row is driven on both
  callers, including a stale-base lane's mint of another lane's reserved number. On each caller,
  a carrier moved after the lane's own fold is folded into the landed watermark. A refresh
  conflict is resolved by the fold. Proposed tier: `Full`.
- **IF-101.**
  - `data` gains: the reserve and fold calls, the record grammar, the carrier ref, the carrier
    and trunk space split, the landing check and the fold lag.
  - `requestors` gain `scripts/integrate` and `scripts/check`.
  - The owner stays `scripts/trace`. The status stays Drafted, so no sitting is owed.

"No cell names a code file, function or symbol" (D2) is read as revision 36 rules it:

- every authored cell is in contract voice;
- the traced `module` and `code_symbol` cells stay filled and binding until item 5's schema lane
  removes them, since `--strict-schema` requires both;
- at intent they name the symbols P2 to P8 will create, and they bind at P15.

Tests: none (spine only). `trace.py --strict` and `check_trajectory.py --strict` run clean.

### P2: `id_carrier.py` (D4, D8, D12; F1)

This is a new stdlib module in `project-trajectory/scripts/` that owns:

- `CARRIER_REF = "refs/heads/id-carrier"` and `TRUNK_SPACES = ("DP", "OI", "WI")`;
- `carrier_spaces(all_spaces)`: every space in trace's one list minus the trunk spaces, so a
  space added later joins by default;
- the record grammar:
  - `parse_reservations(text)` matches the whole stripped line, with `low <= high` and a carrier
    space;
  - a line that does not match is not a record;
  - number 0 is never an allocation;
- `parse_counts` and `check_work_item`, implementing the S3 argument table. They raise one
  `Refused` with a one-line message. The WI, OI and DP refusal says these are minted on trunk.
- the pure `fold(sides)`: for each space the maximum mark; the union of reservation and
  correction records, de-duplicated and sorted by space then low;
- the pure `fold_lag(carrier_text, file_text)`: the carrier marks above the file's and the
  carrier records the file lacks, empty when the file holds the carrier's fold or when there is
  no carrier. It is defined as "fold(carrier, file) differs from file in marks or records", so
  it cannot drift from the fold;
- the pure `plan_reservation(carrier_marks, trunk_marks, counts, wi)`: each range starts at
  max(carrier mark, trunk committed mark) + 1;
- carrier I/O through `kitlib.git`:
  - `carrier_tip`;
  - `carrier_text`;
  - `write_carrier`: `hash-object -w`, then `mktree` for a one-file tree holding
    `docs/id-watermark`, then `commit-tree` with no parent on first use, then
    `update-ref CARRIER_REF <new> <old>`;
  - on creation, `<old>` is the empty string, so the ref must not exist;
  - a failed swap raises `Refused("another reservation moved the carrier; re-run")`;
  - no worktree and no checkout are used, and the lock is git's ref lock (the `archive/lanes`
    precedent);
- the pure `landing_lines(added, carrier_records, wi_ids, landing_records, parent_records,
  carrier_present, claim_problem)`: the six-row table, each refusal naming the ids, the work item
  and the reserve verb.

It also ships: a manifest row in `kitlib/bootstrap_manifest.py`, and a line in `bootstrap.py`'s
shipped-script list. Without them, a scaffold's `trace.py` fails to import.

This commit is the lane's first that touches a shipped path, so it carries the `RESYNC_PACK.md`
entry, anchored `[since <lane base>]`; `check_resync.py` in the commit bar refuses the commit
without it. P13 refines the entry's text, and every rebase re-anchors it (recipes §3, "RESYNC").

Tests: `tests/test_id_carrier.py` (smoke, in process). Each fails before the change with
`ModuleNotFoundError`:

- the grammar admits exactly the well-formed line and rejects every malformed shape (no
  `low <= high`, a trunk space, a missing work item, trailing text);
- the carrier-space set is the space list minus WI, OI and DP, and a space added to the input
  joins;
- every count and work-item refusal of the S3 table, plus the admitted shapes;
- `fold` on two sides gives each space's maximum and the sorted union of records, with
  duplicates collapsed;
- `fold_lag` is empty for a file that holds the carrier's fold, and for no carrier; it names a
  carrier mark above the file's, and a carrier record the file lacks; it is empty for a file
  ahead of the carrier (the lane's own live ids above every record);
- `plan_reservation` starts above the larger of the two marks;
- `landing_lines` gives each of the six table rows, and a `-000` id is never judged.

The bootstrap end-to-end test in `tests/test_bootstrap.py` runs `trace.py` in a fresh scaffold.
Without the manifest row, it fails on the import.

### P3: Every writer carries the records (D9)

- `render_watermark(marks, basis, corrections, reservations)` renders a `# RESERVATIONS` block
  only when records exist, so a file with none renders byte-identical to today.
- `bump_watermark` and `correct_watermark` read the records and pass them through.
- The intake WI and OI mints and `plan_artifacts` reach the file only through `bump_watermark`,
  so they carry the records with no edit of their own.
- Consolidation (0→A→B):
  - `committed_watermark` and `committed_corrections` already repeat one walk over HEAD,
    MERGE_HEAD and the other parents, and P4 would add a third copy;
  - extract `_baseline_texts(root)`, which yields each baseline's watermark text, and call it
    from all three;
  - this offsets part of `trace.py`'s growth.

Tests, in `tests/test_id_watermark.py` (TC-158):

- `test_bump_ids_keeps_every_reservation_record`;
- `test_correct_mark_keeps_every_reservation_record`.

Each fails before the change because today's `render_watermark` drops the record line. Also run
`test_bump_watermark_preserves_a_recorded_correction` and TC-147's `tests/test_intake.py`
unchanged.

### P4: The hand-raise rule re-founded (D9)

- In `_mark_history_findings`, a rise above max(committed mark, live maximum) is justified up to
  the highest `high` that a well-formed record in the commit's own file names for that space. A
  fall is refused regardless. With no records, the rule is today's rule.
- A new committed-record check, beside the correction one, uses
  `id_carrier.record_history_findings(current, committed_union)`. Each record any baseline
  carries must be present unchanged. It is a union across parents, never longest-wins, so a
  merge cannot drop a side's records.
- `parse_corrections` is unchanged. The live-id finding's text points a lane at
  `--reserve-ids`, where today it says "the spine tiers have no minter".

Tests, in `tests/test_id_watermark.py`:

- `test_a_rise_covered_by_a_reservation_record_passes`. Fails before: today's rule refuses the
  raise as a hand-raise.
- `test_a_rise_above_every_record_is_refused`. Passes before, a guard that the widening stays
  bounded.
- `test_an_altered_committed_record_is_refused`. Fails before: no check exists.
- `test_a_deleted_committed_record_is_refused`. Fails before.
- `test_a_merge_dropping_one_parents_record_is_refused`: two parents, each with its own record,
  and the result keeps only one. Fails before.
- `test_a_reservation_line_never_reads_as_a_correction`. Pins today's behaviour.
- `test_a_malformed_reservation_line_justifies_nothing`. Passes before only because nothing
  justifies; kept as the pin.

All of these are driven through the CLI exit code, as
`test_the_rules_are_actually_WIRED_INTO_the_integrity_floor` does.

### P5: The verbs (D5, D6, D7, D8, D24, D25)

**`trace.py --reserve-ids WI-NNN SPACE=N[,SPACE=N...]`** (`nargs=2`). It is routed through one
helper in `_writer_mode`, so `main()` keeps its complexity ceiling. In order:

1. Parse both arguments through P2. A usage error exits 2 from argparse. Any other refusal exits
   1 with one line on stderr, and nothing is written.
2. Read the trunk claim through the kit's trunk reader (`agent_common.trunk_name`). The work item
   must have `docs/work/active/*/WI-NNN-*.md` at trunk's tip. If the trunk is undeclared, the
   refusal names the reader.
3. Read the carrier tip, or, absent, trunk's committed watermark.
4. Plan the ranges.
5. Write one carrier commit. Its file is `fold(carrier, trunk committed)` plus the raised marks
   and new records, so a trunk correction record is kept. The commit message goes through
   `kitlib.provenance.with_loop_trailer`, so a headless leg's carrier commit is marked.
6. Swap the ref.
7. Fold the new tip into the working `docs/id-watermark`, and leave that change for the caller to
   commit, as `retire.py` does. Print each range.

**`trace.py --fold-ids`.**

- It reads the receiving file: index stages 2 and 3 when the path is conflicted, else the file.
- It reads the carrier tip; when there is none, only the working sides are folded.
- It writes the fold, with the basis recomputed from the working tree's live ids.
- This verb repairs the failed-write shape "after the ref moves, before the fold". It is the
  rebase recipe's resolution and the hand landing's fold in the staged squash (P8, P11).

Tests:

- `tests/test_id_carrier.py`, in process:
  - each refusal of the S3 table, driven through the CLI: the carrier is unmoved, the working
    file byte-identical, exit 1 with one line, or exit 2 for argparse;
  - WI, OI and DP each refused with the trunk-minted message (OI-116 (a)).
  - Each fails before the change: `--reserve-ids` is an unknown argument (exit 2 for every case).
- `tests/test_id_carrier_git.py`: slow, added to `SLOW_MODULES`; the in-process module above is
  the family's smoke pin.
  - `test_first_reservation_seeds_the_carrier_from_trunk`: one orphan commit whose tree is the
    one file.
  - `test_a_lost_race_refuses_with_nothing_written`. Two worktrees of one repository. In
    worktree A, the in-process verb sees a stale tip (its tip read is patched to return the tip
    from before B's move), while B's verb runs as a subprocess and moves the carrier. Then:
    - A exits 1 with "another reservation moved the carrier; re-run";
    - the carrier stays at B's commit;
    - A's file is unchanged.
    The same is driven for two first-use creations.
  - `test_sequential_reservations_are_disjoint` and `test_stale_base_reservations_are_disjoint`.
    Two lanes cut from different trunk commits each reserve SR and TC. Their ranges are
    disjoint, and each starts one above the carrier's mark at its turn. This is the folded
    sittings rule.
  - `test_a_reservation_after_a_ruled_correction_starts_above_it`: trunk commits
    `--correct-mark` under a ruled open item. The next range starts at the corrected mark plus
    1, and the carrier file keeps the correction record.
  - `test_fold_ids_on_a_conflicted_watermark`: a real merge conflict on the file. The fold reads
    stages 2 and 3 plus the carrier, and writes max and union with no conflict markers and the
    basis from live ids.
  - Each fails before the change: the verbs do not exist (exit 2, or `ModuleNotFoundError`).
    This is the D7 test that fails on today's code: under today's procedure two stale-base lanes
    draw the same next number, and there is no verb to separate them.

### P6: The landing check (D10, D11, D12; F1)

`trace.landing_id_refusal(root, landing_rev, parent_rev, wi_ids)` is the one id judgement both
callers use. `trace.landing_fold_lag(root, rev)` is the one fold check both callers use: it reads
the rev's `docs/id-watermark` (a commit, or the index's tree) and the carrier tip, and returns
`id_carrier.fold_lag` over them.

- **"Live" at a tree.**
  - `trace.live_ids(root)` yields the `(space, number)` set from the existing sweep, and
    `live_max_ids` is derived from it, so there is one definition of live.
  - To sweep a git tree, `docs/requirements` and `docs/test` (the homes of every carrier space)
    are extracted at the rev into a temporary directory. The extractor is lifted from
    `rejudge.py` into `kitlib.git` as one stage with two callers. rejudge keeps its own error
    type at its call site, and its tests pass unchanged.
  - The index of a squash is named by `git write-tree`.
- **"Added"**: carrier-space ids live in the landing and not in the parent, excluding number 0.
- **The judgement.** It is `id_carrier.landing_lines`, over:
  - the carrier tip's records;
  - the landing and parent files' records;
  - the work items read from the claim.
  A malformed record line justifies nothing, so an id it would have covered is refused as
  outside every record.

Tests: `tests/test_id_landing.py` (slow; the in-process `landing_lines` and `fold_lag` pins are
in P2).

- `test_the_extracted_sweep_equals_the_working_sweep_for_every_carrier_space`, run on this
  repository. It pins that no carrier-space reader reads outside the two extracted directories:
  a reader added elsewhere later fails it.
- `test_a_minus_000_placeholder_is_never_added`.
- `test_landing_fold_lag_reads_a_commit_and_an_index_tree`: a carrier moved past a committed
  file and past a staged one is reported for each.

These fail before the change on the missing functions.

### P7: Caller 1, the merge slot (D11, D12; F1)

- **The id rung.** `_merge_refusal` gains a rung right after R1:
  `_reserved_id_refusal(root, branch, wi_ids)`, which calls
  `trace.landing_id_refusal(root, branch, _head(root), wi_ids)`. An empty claim is already
  refused by the ladder's first rung, so the "work item unreadable" row is driven on the rung
  function itself.
- **The fold at the slot (F1).**
  - The slot merges `--no-ff` only a tip trunk already descends into, so the landed tree is the
    tip's tree, which its refresh bar attested. The fold must therefore be in the tip.
  - In `integrate_one`, a tip that `_merge_ready` passes but whose watermark lags the carrier
    (`trace.landing_fold_lag(root, branch)` non-empty) is treated as not merge-ready, with that
    reason. It takes the existing pessimistic sequence: refresh inside the held slot, which folds
    (below), and is barred and attested as any refresh.
  - The readiness is combined in one small helper, `_landing_ready(root, branch)`, so
    `integrate_one` stays inside its complexity baseline. `_merge_ready` itself is unchanged.
    The post-refresh re-check stays `_merge_ready` alone, so the slot refreshes at most once.
  - The landing therefore holds the fold of the carrier tip the slot read. A reservation that
    races the in-slot refresh is a reservation after that read; the next landing or refresh
    folds it, and allocation is unaffected, since every reservation floors at the carrier's mark.
- **The refresh.**
  - In `_merge_trunk_in`, after `_resolve_generated_conflicts`, a remaining conflict that is
    exactly `docs/id-watermark` is resolved by `trace.fold_watermark(wt)` plus `git add`. That
    counts as auto-resolved. Any other remaining conflict still refuses, and the note names what
    was folded.
  - After a successful merge-in, while a carrier exists, `refresh` folds the carrier into the
    lane's file before the trunk step. The hand-raise rule judges the refresh commit as it judges
    any commit. With no carrier and no conflict nothing changes, so a trunk-only repository is
    unaffected.
- `Implements:` tags go on the new rung, the readiness helper and the fold call.

Tests: the landing rows at the slot, in `tests/test_id_landing.py` with the station fixtures from
`tests/test_integrate_station.py`. Each fails before the change: today's slot merges the lane.

1. A code-only lane with no carrier lands.
2. A lane whose added ids sit in its own record lands.
3. Three refused cases, each naming the ids, the work item and `--reserve-ids`:
   - an added id with no record;
   - **a stale-base lane that minted another lane's reserved number** (that work item's record);
   - a retired number re-used.
4. Ids added with no carrier ref: refused.
5. Claim unreadable: refused, naming the claim read.
6. The landing file carries a record that neither the carrier nor trunk holds: refused, naming
   the line.

Fold tests at the slot:

- `test_the_slot_folds_a_carrier_moved_after_the_lanes_refresh` (F1): lane A reserves, folds and
  refreshes; lane B then reserves; the slot runs on A. A is refreshed in the slot, and trunk's
  watermark after the merge holds B's record and B's raised mark beside A's. It fails before the
  readiness change: A merges with its stale file, and trunk lacks B's record.
- `test_a_code_only_lane_lands_with_the_carriers_fold`: a carrier exists and the lane adds no
  id; it lands with no reservation of its own, and the landed file holds the carrier's fold.

Refresh tests:

- `test_a_refresh_conflicting_only_on_the_watermark_is_resolved_by_the_fold`: both sides bumped,
  so the basis lines differ. Today it refuses with "merging trunk in CONFLICTS".
- `test_a_watermark_conflict_beside_another_conflict_still_refuses`: passes before.

Run TC-148 (`tests/test_integrate_station.py`, `tests/test_dispatch.py`) unchanged.

### P8: Caller 2, the hand squash (D11, D12; F1)

- A `reserved-ids` step in `check.py`'s step table, beside `held-status` (the `STAGE_NEEDS` rung,
  `process`). Its `--reserved-ids` mode follows `_held_status_mode`'s shape.
- It judges only while `kitlib.git.squash_commits` reports a squash in progress. Every other
  commit passes at once, so a non-squash commit costs one file read.
- The squash's work item: the claim folders at HEAD (`docs/work/active/<lane>/`) of every local
  branch containing the squashed tip. That read is lifted from `plan_gate._squash_lines` into
  `kitlib.git`, with the plan gate as its second caller. If no branch contains the tip, or no
  claimed spec is readable, the step refuses only when ids were added, naming the claim read.
- It calls `trace.landing_id_refusal(root, <write-tree of the index>, HEAD, wi_ids)`.
- **The fold at the squash (F1).** A pre-commit hook judges and never writes, so the fold is the
  landing actor's step and the hook enforces it:
  - recipes §3's squash bullet runs `"$PY" "$SCRIPTS/trace.py" --fold-ids` and
    `git add docs/id-watermark` in the staged squash, before the regeneration and the bar (P11);
  - the step refuses a squash whose staged watermark lags the carrier tip
    (`trace.landing_fold_lag` over the index's tree), naming each missing mark or record and the
    remedy, `trace.py --fold-ids` then `git add`;
  - the judged staged tree is therefore the folded one;
  - with no carrier the lag is empty, so a trunk-only repository is unaffected.
  - A reservation between the fold and the commit makes the hook refuse, and the coordinator
    re-runs the fold. The fold changes only `docs/id-watermark`, which the hook's own
    `--strict-integrity` floor judges.
- The step joins `--run-steps` in the shipped `project-trajectory/hooks/pre-commit`, with its
  comment line, and the dogfooded hook path picks it up.

Tests, in `tests/test_id_landing.py`, through a real `git merge --squash` and the step's CLI exit
code:

- the same six rows as P7. Each fails before the change: the step does not exist, and the squash
  commits;
- `test_a_hand_squash_folds_a_carrier_moved_after_the_lanes_fold` (F1): lane A reserves and
  folds; lane B reserves; trunk squashes A.
  - Committed unfolded, the step refuses, naming B's record and `--fold-ids`. Fails before: the
    squash commits with trunk's file lacking B's record.
  - After `--fold-ids` and `git add`, the commit passes through the hook, and trunk's committed
    watermark holds A's and B's records and the maximum marks.
- `test_a_code_only_squash_passes_with_no_reservation`: no carrier, and the step passes at once;
  with a carrier, it passes once the staged file holds the fold.

The hook-list pin test is updated. The plan gate's squash tests pass unchanged after the lift.

### P9: The act machinery untouched (D13)

- `git diff <lane base>..HEAD` shows no change to `baseline_snapshot.py`, `_record_act`, the act
  ledger readers, the act-numbering code or the latch text in SKILL §4. P11 removes only "and the
  id watermark" from that sentence, and the act clause stays.
- No change either to `tests/test_baseline_snapshot.py` or the act-ledger tests.
- Their tests pass at the commit bar.

Tests: none added. The evidence is the empty diff and those tests passing.

### P10: Keep-or-mint text (D14, D15, D16)

- One paragraph in `PROCESS.md` §4, directly after the paragraph defining the CLARITY
  re-attestation and the MEANING row. It is stated once:
  - a changed requirement leans toward a new id;
  - it keeps its id when the id's spirit is retained and keeping costs fewer changes overall;
  - keeping needs a cross-reference that checks every findable user of the id (the rows, the
    tests and code citing it, and known citers in other repositories) against the amended
    meaning;
  - a user the change breaks is updated, or the row mints instead.
- `spine-questions.md` §0 gains one bullet citing it, with no restatement.
- The `byte-budget-guard` skill reports PROCESS.md's delta and restamps its row in the shipped
  skill and its dogfooded copies.

Tests: none. The evidence is the byte report and `check_docs`.

### P11: The coordinator text (D12, D17, D18; F1)

- **`scripts/coordinator/terra-spine-prompt.template.md`.**
  - The `--bump-ids` clause leaves the "Edit ONLY" rule. The author never touches
    `docs/id-watermark`.
  - "New ids count up from the mark" becomes three statements:
    - draft new ids only from the reserved ranges this brief names, `@RESERVED@`, never from
      the watermark's mark;
    - an author who needs more ids than a range holds stops, and reports the count per space;
    - the coordinator then reserves again.
  - `mkprompt.py` already refuses an unfilled slot, so a brief cannot launch without its ranges.
    `RESERVED=none` states a turn that mints no id.
- **Recipes §4, in all three copies** (`project-trajectory/skills/coordinator-cycle/`, `.claude/`
  and `.agents/`).
  - The floor bullet becomes "Reserve before drafting":
    - before dispatching the spine author, reserve the draft's counts with
      `trace.py --reserve-ids WI-NNN SR=n,LLR=n,TC=n`;
    - commit the folded watermark;
    - name the ranges in `RESERVED=`.
  - The `docs/id-watermark` rebase row becomes `"$PY" "$SCRIPTS/trace.py" --fold-ids`, then
    `git add`.
  - The "Terra, first turn" bullet names `RESERVED`.
- **Recipes §3's squash bullet, in all three copies (F1).** After `git merge --squash <lane>`,
  run `--fold-ids` and `git add docs/id-watermark` before regenerating; the squash's hook
  refuses a staged watermark that lags the carrier, and a refusal there is answered by folding
  again.
- **SKILL §4, in all three copies.** "so its acts and the id watermark pull up" becomes "so its
  acts pull up".
- The `skills-sync` step holds the copies equal.

Tests: in `tests/test_prompts.py`.

- `test_the_terra_brief_has_an_intent_form_before_build_round_1`: the slot set gains `RESERVED`.
- A new clause pin for the reserved-range text and the absence of `--bump-ids`.
- A recipes pin for "Reserve before drafting", and one for the squash bullet's `--fold-ids`.

Each fails before the change on the template's or the recipe's text.

### P12: Runtime flows and contract text (D10, D12; F1)

- In `docs/runtime-flows.md`, flow 4 draws three things:
  - `Lane->>Lane`: the refresh folds the carrier in, and resolves a watermark conflict by the
    fold;
  - `Slot->>Slot`: the reserved-ids rung beside R1;
  - the slot's readiness: a tip whose watermark lags the carrier is refreshed in the slot.
- A new flow, "A reservation, its fold and its landing", draws:
  - the carrier's mode classes (absent, present at T) and the compare-and-swap transition;
  - the lost-swap refusal;
  - the fold into the lane;
  - the two landing callers, each folding: the slot through the in-slot refresh, the squash
    through `--fold-ids` with the hook's lag refusal.
- In the code headers, `trace.py`'s "Contract IF-101" paragraph gains the reserve and fold
  calls, the record grammar, the carrier ref, the landing check and the fold lag. "Contract
  IF-145" lists the two new writer arms.

Tests: none. The evidence is `check_flows` and the generated interface reference at P16.

### P13: Shipping (D19, D20)

The `RESYNC_PACK.md` entry written in P2 is refined to its final content. It states:

- the carrier exists from the first reservation;
- a lane that adds spine or off-spine registry ids reserves them first, or its landing is
  refused. This is a forced change for an adopter running lanes; a trunk-only repository is
  unaffected;
- a lane open at upgrade reserves and renumbers before it lands;
- the watermark gains a record line kind that every writer carries, and no existing file
  migrates;
- `--bump-ids` is no longer the lanes' spine minter;
- a landing lands the carrier's fold: the merge slot refreshes a lagging lane, and a hand
  squash runs `trace.py --fold-ids` in the staged squash, or its hook refuses;
- the new shipped module and the hook's new `reserved-ids` step are overwritten as kit-owned
  files.

The entry stays anchored at the lane's base and is re-anchored at each rebase (P14), and at the
landing's parent in the staged squash if the last rebase replayed cleanly over docs-only trunk
commits (recipes §3).

### P14: Final rebase and own ids, before any sitting (D21; F2)

This step moves ahead of the checkpoint so that the rows are sat on their final numbers (F2).

1. Rebase onto current trunk (recipes §3–§4). The `docs/id-watermark` conflict, if any, is
   resolved by the lane's own `--fold-ids`.
2. Reserve this row's own ids from the lane: `trace.py --reserve-ids WI-978 LLR=2,TC=2`. This
   first use creates the carrier from trunk's committed watermark.
3. If the ranges differ from the drafted LLR-362, LLR-363, TC-401 and TC-402, renumber the rows
   and every citer of them in the lane (the rows, the evidence cells, the tests and the
   `Implements:` tags).
4. Commit the folded watermark with the renumbering. The hand-raise rule passes it on the new
   record.
5. Re-run the commit bar and both strict lints.

The coordinator schedules no other landing between this step and P16, since this row lands
alone (revision 37). If one lands anyway, P16 sends the lane back here. The carrier keeps this
row's reservation through any later rebase, so a second pass re-reserves only if a landing made
under trunk's old code took one of the reserved numbers.

### P15: The checkpoint on the final numbering (D2, D3; F2)

1. Terra's checkpoint turn reconciles the set against the built code at P14's tip. Evidence
   cells name existing tests, and `code_symbol` cells name existing symbols
   (`check_doc_refs --strict`).
2. The closure check runs.
3. One sitting is held: SR-174 (an amendment), TC-158 (an amendment), the two new LLRs and two
   new TCs (first approval). IF-101 is Drafted, so it owes no sitting.
4. The acts are taken from the committed verdict by the adjudicator's act turn: the amendment
   act first, then the first-approval act. The SR, LLR and TC rungs are released, so no act is
   the owner's. The act is the lane's last spine commit (SKILL §4 step 2).
5. If trunk moves after the sitting, the lane rebases again before the act, or before landing if
   the act is already taken. The unchanged-rows check compares the rows at the verdict's commit
   with the rebased tip, and a renumbered row counts as changed. A changed row is re-sat with
   the whole set in one sitting, and the act is taken again from that verdict (SKILL §4;
   recipes §3, "a return in a sitting holds its whole registry").

### P16: The landing (D19, D21, D22, D23; F2)

1. **Entry condition (F2).** The landing starts only from P15's act at the lane's final rebase.
   If trunk has moved since P14, the lane goes back to P14, and then to P15's re-sitting rule.
   No row is renumbered after its act.
2. **The other lanes (D21).** The coordinator lists every other open lane: every claim folder
   under `docs/work/active/` on trunk. For each, it runs `trace.landing_id_refusal` read-only
   against that lane's tip over trunk. Each lane it would refuse is named in the landing's
   decisions record and in the handoff, as a lane that reserves and renumbers before its own
   landing.
3. **The landing.** It is a hand squash (recipes §3) or the merge slot.
   - On a squash, `--fold-ids` runs in the staged squash (P8, P11).
   - This row's own landing passes its own check: its added LLR and TC ids sit in WI-978's
     record, and the hook running the squash is the staged tree's.
4. On trunk, the declared `[generated]` pages are regenerated per the coordinator's landing
   list:
   - `docs/cli-reference.md` (`gen_arch_map.py --cli-doc`);
   - `docs/interface-reference.md`;
   - `prompts/CATALOG.md`;
   - `components.derived.toml` (`gen_arch_map --src`, for the new module);
   - the trunk step's document families.
5. The commit bar runs green on the staged squash.
6. `trace.py --strict` and `check_trajectory.py --strict` run clean on the landing tip.
7. The full bar declared for the stage runs at the lane refresh. The real output is pasted.

## Risks and surfaced findings (not built here)

- **The overnight audit reads `id-carrier` as a person's branch.**
  `scripts/coordinator/overnight_legs.py` judges trunk and `archive/lanes` by descent plus
  trailer, but every other moved branch only by the lane rule. A carrier moved in a headless leg
  therefore passes unjudged for provenance. P5 marks its commits, but nothing checks the mark.
  This is a candidate successor: judge the carrier as `archive/lanes` is judged. It is surfaced
  as a finding, not built.
- **The race window before this row lands.** Between P14's reservation and the landing, another
  lane landing carrier ids under trunk's old code would not be checked. Landing alone, with no
  landing between P14 and P16, closes it. If one slips in, P16's entry condition sends the lane
  back to P14; the next reservation's trunk floor still prevents a duplicate range.
- **A reservation racing a landing.** At the slot, a reservation during the in-slot refresh lands
  one fold behind, and the next landing folds it. At the squash, the hook refuses and the fold is
  re-run. Neither affects allocation, since every reservation floors at the carrier's mark.
- **Basis churn.** The fold recomputes the basis line. The refresh and the landings fold only
  while a carrier exists, so a trunk-only repository's file never churns from this row.
- **`trace.py` growth.** The estimate is +70 to +100 SLOC net of `_baseline_texts`: the
  composition, two writer arms, the rule widening and the fold-lag reader. Past about +120, more
  composition moves into `id_carrier.py` rather than taking a larger bump.
