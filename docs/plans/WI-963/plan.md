# WI-963 implementation plan, revision 2: the trunk mint skips amendments the merged range already settled

Spec: `docs/work/active/wi-963/WI-963-sweep-skips-settled-amendments.md`
(specref: `docs/plans/2026-10-03-s11-in-lane-adjudication.md#42-the-re-mint-trap`).
Item SR: SR-178. Planner: fresh session, read-only. Lane worktree:
`C:/Projects/ai-template.wt/wi-963` (base `7f8e57192`). This is the plan's one
revision, answering `docs/plans/WI-963/critique-1.md` (F1, F2); how each
finding was judged is under "The critique's findings, judged" below.

## The premise, confirmed on the kit's own history (read-only)

Over each of the two named landings, today's `intake._routed_amendments`
returns exactly the rows the redundant mint named. `acceptance_record.reattested_between`
names the same rows. Each row's whole cell set at the landing tree equals its
copy under `docs/archive/last_approved/` at that tree:

- `5245ac82cf9d2132f7c6c1940f9a1f3c49294ba3..08bbb71b60b060e0ceed4fa8baaac924b2be42c6`
  (WI-926, minted WI-952): SR-019, SR-020, LLR-019, LLR-020, LLR-140, LLR-300.
  All six were re-attested and none differs from its copy.
- `be80354d9297eac08952a9d3a1efeab0d31b28a5..ed84e25107cce3b18fb4977fd0afc7fe567f3bca`
  (WI-956, minted WI-959): LLR-207, TC-132 (approved `Expected`/`Method`,
  routed `Verifies`) and TC-205. All three were re-attested and none differs
  from its copy.

So the design in S11 §4.2 drops exactly those rows and nothing else. CI checks
out full history (`.github/workflows/test.yml`, `fetch-depth: 0`), so a
regression can replay both ranges from the object database. It does so the way
`tests/test_old_kit_resync.py` reaches its pinned commit: probe, and skip with
a named reason on a shallow clone.

## The critique's findings, judged

**F1 (review order): confirmed in part, refuted in part; covered by P6-P8.**

- *Confirmed:* revision 1's P6 was internally inconsistent. Its table row
  said "over the final tip", its detail said "before the act", and it also
  scheduled an authored edit (the RESYNC entry's final wording) after both
  reviews. An authored edit after the gate does land unreviewed. Revision 2
  splits P6 into three rows, and no authored text changes after the gate.
- *Refuted:* the claim that the A+B verdicts must be taken over the post-act
  tree. The review order this lane runs is the coordinator-cycle skill's
  (`.claude/skills/coordinator-cycle/SKILL.md` §3 "Checkpoint" step 4 and §4
  steps 1-2), not the S11 plan's §3 step 8 / §4.5. That plan was the
  2026-10-03 design proposal. This WI's specref cites only its §4.2 (the
  re-mint trap), and the cycle that was later built replaced its post-act
  review. In the cycle:
  1. The uncounted gate (REVIEW-A and REVIEW-B, convergence stance) reviews
     the checkpoint tip, code and rows together.
  2. The lane rebases. If the rebase changes code or authored rows, the
     affected checkpoint repeats and an uncounted convergence round reviews
     the rebased tip. When trunk moved only by commits the lane does not
     touch, the lane rebases before the gate, so the gate reviews the tip
     that lands (recipes §3, "Rebase, even when trunk moved only by the pause
     restore").
  3. The unchanged-rows check runs: each judged row at the verdict's commit
     is compared with the rebased tip.
  4. The act turn (`coordinator_adjudicate.py act`) commits Status flips and
     snapshot copies only, authorized by the accepted sitting verdict and
     bounded by it. The act composer refuses a judged row in a state no act
     explains. The merge slot's act rungs refuse an act outside the
     verdict's scope (`reattest_scope_refusal`, `held_reattest_refusal`,
     `lane_acted_set`).

  The act's content is therefore judged by the sitting and bounded
  mechanically, never authored after the reviews. A review round over the
  post-act tree is not a step of the cycle. Scheduling one here would run a
  lane outside the procedure every other lane follows.

**F2 (read failure of a present carrier): confirmed; covered by P2 and P3.**
The finding is right. `_ledger_acts` reads its ledger through `kitlib.git`
`git_out`, which returns None on any failure, and maps None to `[]` (absent).
A present ledger whose blob cannot be read would therefore read as no acts.
Revision 1's `_snapshot_copy_rows` named only absence and parse failure, so a
present copy whose blob cannot be read would fall to "absent, mint". Both
fail toward minting, never toward suppression. D4 nonetheless requires "a
ledger or snapshot copy that is present but cannot be read or parsed refuses
the mint by name", and the Trust ruling (D-020) says the same.

The owning read boundary already exists: `kitlib.git.git_show` (WI-818). It
returns None only when the tree does not list the path. It raises
`UnreadableBlob` when the tree lists the path but its blob cannot be read (a
partial clone offline, a damaged object store), or when git cannot list the
tree at all. The ruling and overrule syncs already read through it
(`acceptance_record._show`). Revision 2 reads both new carriers through it and
adds the two read-failure tests (P2 tests 6b and 7b). The existing
`_ledger_acts` contract is preserved byte-for-byte for its unchanged readers
(see P3).

## The architectural-delta question

The WI does two of the four things.

- **It makes an output depend on a new input.** Which amendment rows the trunk
  mint files now depends on the act ledger (`docs/archive/last_approved/acts.toml`,
  IF-220) and on the snapshot's registry copies at the range's `after` tree. Today
  it reads only the two live trees.
- **It adds a value to a domain.** The amendment arm's outcome today is "drafts"
  only (`_amendment_drafts` returns a list). It gains a **refusal**: a present
  ledger or snapshot copy that cannot be read, or that does not parse,
  refuses the mint by name. That refusal joins the all-or-nothing refusal set
  `intake_after_merge` already has for its other arms (`_done_when_drafts`,
  `_disposition_drafts`, `_rejudge_drafts`). The ledger read's own result
  domain gains one distinguished value, "present but unreadable", at the new
  tri-state reader (P3). The old two-valued reader `_ledger_acts` keeps its
  result domain for its existing callers.

It adds **no new state**: it writes no file, marker or store, and it reads
only what the act turn and the owner's signing acts already commit. It
**crosses no new boundary**:

- `intake` already calls `acceptance_record` across IF-091, and that row's
  data cell widens to name the new call.
- `acceptance_record` already reads the act ledger (IF-220) and the snapshot
  copies (`staged_snapshot_findings`, the mirror rules).
- It already reads blobs through `kitlib.git.git_show` (the ruling sync's
  `_show`).

The one gap found is not this WI's to fix. No IF row declares the snapshot
copies' file shape as a seam: IF-220 covers only the ledger "beside the
snapshot copies". This WI reads those copies through the same module that
reads them today, so it adds no crossing. The undeclared seam is surfaced as
a separate finding (below), not fixed inline.

Every change sits in modules this item owns (`intake.py`,
`acceptance_record.py`) and on rows it amends in place (IF-091, LLR-153,
LLR-158, plus a new LLR and TC under SR-178). No refactor outside the lane is
needed. The table rows below make the change explicitly.

DELTA: within

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Spine intent, TC-first: draft the filter's LLR (a new `Drafted` LLR under SR-178, or LLR-153's detail if the in-lane adjudicator rules it no separate obligation), amend LLR-153's trigger-(a) clause to point at it, amend LLR-158's detail with the shared-walk restatement, and draft one TC verifying SR-178, the LLR and IF-091 that names every test P2 adds (the read-failure arms included), before any code | D7; D8; D11; F2; SR-178; TC-147; TC-153 | no interface: registry rows only, no code seam crossed |  |
| P2 | The tests, red: a new `tests/test_intake_settled.py` with one test per arm (settled skips at both routes, amended-after-act mints, no-act mints, absent ledger, consulted-only-with-records, malformed ledger refuses, unreadable ledger blob refuses, malformed copy refuses, unreadable copy blob refuses, missing copy mints, the one-cell restore mints, the two real landings replayed) | D1; D2; D3; D4; D5; D6; D11; F2; SR-178 | IF-091; IF-220 | P1 |
| P3 | The filter: `acceptance_record._ledger_read` (the tri-state ledger read through `kitlib.git.git_show`: absent, acts, or a named read/parse failure), `_ledger_acts` re-expressed over it with its contract unchanged, `_snapshot_copy_rows` (the same tri-state over a copy) and `settled_amendments`; `intake._routed_amendments` drops the settled records and returns `(records, refusal)`, `_amendment_drafts` passes the refusal on, `intake_after_merge` refuses on it like its other arms; the five test call sites take the tuple; the IF-091 data cell and the module's `Contract IF-091` docstring name the new call; the `intake.py` module-size ratchet re-stamp; the RESYNC_PACK entry drafted (the commit bar's `check_resync.py` requires it from the first shipped-file commit) | D1; D2; D3; D4; D5; D6; D10; F2; SR-178; TC-147; TC-278; TC-331 | IF-091; IF-220 | P2 |
| P4 | The shared-walk restatement in code and the flow: the comment above `AMENDMENT_CSVS` says the warn and the mint read one walk and the mint additionally drops rows the merged range re-attested (the warn is unchanged; it fires before any act); `docs/runtime-flows.md` Flow 4's intake return line says the same | D8; SR-178; TC-153 | no interface: a comment and a flow-diagram label, no code seam crossed | P3 |
| P5 | The workaround's removal, once P3's regressions pass: the coordinator-cycle skill §4 step 3 and recipes §3 drop "close the re-mint citing the act" and the re-mint wording around the sweep; the `.claude/` and `.agents/` copies kept byte-identical; the RESYNC entry's wording finalised here, the last authored text before the reviews | D9; D10; F1 | no interface: skill and pack prose only, no code seam crossed | P3 |
| P6 | Counted rounds and the checkpoint: counted full-lane rounds (REVIEW-A and an independent REVIEW-B, at most three) over the lane until one has no BLOCKER or MAJOR; Terra's reconcile of the set; the closure check; one combined in-lane sitting judging P1's rows (first approval of the new LLR and TC, the LLR-153 and LLR-158 amendments), its verdict committed | D7; D12; F1; SR-178; TC-147; TC-153; TC-278; TC-331 | no interface: review and sitting records only, no code seam crossed | P4; P5 |
| P7 | The gate over the checkpoint tip: rebase first when trunk moved only by commits the lane does not touch; then the uncounted REVIEW-A and independent REVIEW-B in convergence stance (after the convergence map) over the checkpoint tip, code and rows together; this tip carries every authored change the landing carries | D12; F1; SR-178 | no interface: review records only, no code seam crossed | P6 |
| P8 | The act and the landing: rebase (if not already done at P7; a rebase that changes code or authored rows repeats the affected checkpoint and runs an uncounted convergence round over the rebased tip); the unchanged-rows check; the act turn (Status flips and snapshot copies only, authorized by P6's accepted verdict, re-attesting LLR-153 and LLR-158 and first-approving the new rows); the squash with the RESYNC anchor re-stamped at the landing's parent (an anchor only, no wording); the commit bar, `check_trajectory.py --strict` and `trace.py --strict` green; the full suite once; the sweep, which mints no re-mint for this lane's own settled rows | D1; D7; D10; F1; SR-178; TC-147; TC-153; TC-269; TC-271; TC-278; TC-331 | no interface: landing bookkeeping, no code seam crossed | P7 |

The Done-when, Trust section and specref are not amended by this revision, so
the pass record's Done-when binding is unaffected.

## Step detail

### P1: spine intent (TC-first)

**Where the rule lives: a recommendation, not a fixed choice.** LLR-153's
`sr_refs` are SR-174 and SR-228, not SR-178. The filter is anchored at SR-178
("text that has moved away from its acceptance record is reported": a row
re-attested in the range has not moved away, so routing it again reports
nothing). If the rule were stated only in LLR-153's detail, an SR-178
obligation would sit under a row that does not trace to SR-178. The fix would
then be adding SR-178 to LLR-153's `sr_refs`, a routed traced re-point of an
Approved row. So the plan **recommends a new `Drafted` LLR under SR-178** and
puts that choice to the in-lane adjudicator (D7 allows either).

- **New LLR-NNN** (`docs/requirements/low-level-requirements.toml`; next free
  id at authoring; `sr_refs = ["SR-178"]`; `module` =
  `project-trajectory/scripts/intake.py;project-trajectory/scripts/acceptance_record.py`;
  `code_symbol` = `_routed_amendments/settled_amendments/_snapshot_copy_rows/_ledger_read`;
  `component = "CMP-008"`, the intake mint's component in
  `docs/requirements/components.toml`, where IF-091 also sits). Its `detail`
  states:
  - The rule: the trunk mint drops an amendment record when an act-ledger
    entry the range added (a `seq` the `before` ledger does not hold) lists
    the row in `reattested`, AND the row's approved and routed traced cells
    at `after` equal the row's copy in the snapshot at `after`. The
    comparison uses the whole row through `split_changed_cells`, not the net
    diff's cells.
  - The fail directions:
    - An absent ledger (the tree does not list it) is no acts.
    - The filter is consulted only when the walk returned records.
    - A ledger or snapshot copy that the tree lists but whose blob cannot be
      read refuses the mint by name. So does one that does not parse. A
      failed read is never read as absent.
    - A missing copy, or a copy without the row, is minted.
  - The two routes: the merge slot's post-merge arm and `intake.py sweep`
    reach it through `intake_after_merge`, so there is one filter.
  - What a refusal says: the mint was refused and the merge stands; recovery
    is a reviewed fix (or a fetch, for an unreadable blob), then `intake.py
    sweep --before --after`.
  - The bound (D11): inputs the act turn and signing acts produce; hand edits,
    alias spellings and sub-second windows are outside it.
- **LLR-153** (Approved, so it is amended and then re-attested at the act).
  Trigger (a)'s clause "-> one adjudication row listing each changed
  row/cell/before-after" gains "minus the rows the merged range already
  settled (LLR-NNN)". `code_symbol` is unchanged. If the adjudicator instead
  rules the rule into LLR-153, the LLR-NNN content moves into this detail,
  SR-178 joins `sr_refs` (a routed re-point, judged at the same sitting) and
  the TC below verifies LLR-153.
- **LLR-158** (Approved, amended then re-attested; D8). The sentence "the
  amend-without-flip warn and the intake amendment mint, which both consume
  that walk" gains: the mint then drops the rows the merged range
  re-attested (LLR-NNN), and the warn reads the unfiltered walk because it
  fires before any act.
- **New TC-NNN** (`docs/test/test-cases.toml`, `Drafted`; `verifies =
  ["SR-178", "LLR-NNN", "IF-091"]`; tier Smoke, or Full if P2's module moves
  to `SLOW_MODULES`). Its `method` names each arm, the two read-failure arms
  included. Its `evidence` names each P2 test. It is one TC with every arm a
  named test, following TC-278's shape; the adjudicator may split it.
- **TC-147** (verifies LLR-153) and **TC-153** (verifies LLR-158): their
  methods stay true ("an approved SR amendment mints ONE adjudication row";
  the walk's universe pinned). They are not amended; they are run at P3 and
  P8.
- SR-178 is unchanged.
- Tests added: none. This row writes the rows P2's tests answer to. The rows
  stay `Drafted`, or amended with Status unchanged, until P6's sitting.

### P2: the tests, red (`tests/test_intake_settled.py`, new)

The tests are committed alone, before the code. Each test that fails today
carries `@pytest.mark.xfail(strict=True, raises=(AssertionError,
pytest.fail.Exception))`, and the P3 code commit removes the marks. Each
*guard* test is an unmarked characterization, and its docstring states the
wrong implementation it would catch (the cycle's evidence classes, SKILL §3
"Intent").

The fixtures are built **through the real producer**: commits of
`baseline_snapshot.copy_live(root, reattests=[...])`, the function
`intake.py snapshot --reattests` and the act turn reach, using
`tests/baseline_snapshot_fixtures.py` where it fits. This keeps every ledger,
copy and range one a supported workflow produces (D11). The out-of-bound
shapes (a hand-edited ledger, an alias spelling, a sub-second window) are not
tested, by the bound. Only the refusal arms use hand-broken carriers:

- two malformed files;
- two dropped blobs, by the `_drop_blob` recipe of `tests/test_ruling_sync.py`.
  It deletes the loose object, so the tree still lists the path. That is the
  partial-clone and damaged-store shape `kitlib.git.UnreadableBlob` names.

The builder may lift `_drop_blob` into a shared test helper if it serves both
modules.

1. `test_a_row_reattested_in_range_and_equal_to_its_copy_mints_nothing` (D1).
   Setup: an Approved SR is seeded with its copy (ledger seq 1); the range
   amends it and commits the act re-attesting it (seq 2).
   Asserts: `intake_after_merge` mints nothing and returns no refusal. The
   sweep, run as a subprocess (`intake.py sweep --before --after`), prints
   "nothing to mint." and writes no mint commit.
   `acceptance_record.staged_spine_amendments(root, before, after)` still
   returns the record, which proves the walk (and so the warn) is unfiltered.
   Fails today because one `adjudicate:` row is minted on both routes.
2. `test_a_row_amended_again_after_its_act_still_mints` (D2, *guard*).
   Setup: as 1, then one more commit in the range amends the same approved
   cell. Asserts: one row naming the SR.
   Pins a filter that tests only the ledger and skips the snapshot comparison.
3. `test_an_amendment_with_no_act_in_range_still_mints` (D3, *guard*).
   Setup: a ledger is present with an older act only, and the range amends an
   Approved row. Asserts: exactly today's draft (same title and adjudicates).
   Pins a filter that reads the whole ledger rather than the added entries.
4. `test_an_absent_ledger_filters_nothing` (D4, *guard*).
   Setup: no `acts.toml` at either revision. Asserts: the amendment mints as
   today, with no refusal. Pins an absent ledger read as a refusal. It also
   pins the tri-state reader treating "the tree does not list it" as absent.
   This case is the contrast that test 6b's refusal is measured against.
5. `test_the_filter_is_not_consulted_without_amendment_records` (D4, *guard*).
   Setup, case (a): a malformed `acts.toml` at `after`. Case (b): an
   `acts.toml` whose blob at `after` is dropped. In both cases the range
   amends no approved row. Asserts: no refusal in either case, and the other
   arms still run. Pins a filter consulted unconditionally.
6. `test_a_malformed_ledger_refuses_the_mint_by_name` (D4).
   Setup: an amended re-attested row, with `acts.toml` unparseable at `after`.
   Asserts:
   - `intake_after_merge` returns `([], refusal)`;
   - the refusal names `docs/archive/last_approved/acts.toml` and the
     revision, and says the mint was refused, not that nothing merged;
   - the sweep exits nonzero with no mint commit.
   Fails today because a row is minted.
6b. `test_an_unreadable_ledger_blob_refuses_the_mint_by_name` (D4, F2).
   Setup: as 1, then the loose object of `acts.toml` at `after` is dropped.
   A second case drops it at `before` instead; that blob differs from the
   `after` one because seq 2 was appended. Asserts, for each case:
   - `intake_after_merge` returns `([], refusal)`;
   - the refusal names the ledger path and the revision, and says its
     contents cannot be read (as distinct from "does not parse");
   - the sweep exits nonzero with no mint commit.
   Fails today because a row is minted.
   It also pins the ledger read: if `_ledger_read` reused `git_out`, the
   dropped blob would read as an absent ledger, and test 4's minting outcome
   would follow.
7. `test_a_malformed_snapshot_copy_refuses_the_mint_by_name` (D4).
   Setup: as 1, but the registry's copy at `after` does not parse.
   Asserts: the refusal names the copy's path. Fails today because a row is
   minted.
7b. `test_an_unreadable_snapshot_copy_blob_refuses_the_mint_by_name` (D4, F2).
   Setup: as 1, then the loose object of the registry's copy at `after` is
   dropped. **Fixture trap:** the copy of a settled registry can be
   byte-identical to the live registry file. They would then share one blob,
   and dropping it would also break the live read. That empties the walk, the
   filter would not be consulted, and the test would pass vacuously. So the
   fixture's range ends with a commit that adds a `Drafted` row to the live
   registry after the act. The live blob then differs from the copy's blob,
   and the settled row is still settled. The test asserts the two blob shas
   differ before dropping one. Asserts:
   - `intake_after_merge` returns `([], refusal)`;
   - the refusal names the copy's path and says its contents cannot be read;
   - no row is minted.
   Fails today because a row is minted.
8. `test_a_reattested_row_missing_from_its_copy_still_mints` (D4).
   Setup: the ledger re-attests the row, but the copy lacks it. A second case
   removes the copy file from the tree (absent, not unreadable).
   Asserts: one row in each case.
   *Guard*: pins a missing copy read as settled, and pins an absent copy read
   as a refusal.
9. `test_a_cell_restored_after_the_act_still_mints` (D5).
   Setup: the range moves cells X and Y; the act copies the row; X is then
   restored to its pre-range text. The net diff shows Y only, which equals
   the copy, but X differs from the copy. Asserts: one row.
   *Guard*: pins a filter that compares only the net diff's cells.
10. `test_the_two_real_redundant_landings_mint_nothing` (D6).
    Setup: against the kit's own repo at the pinned full SHAs above,
    read-only (`git show` only, so no file is written). If a commit is
    absent, it skips with a named reason, as `_old_kit_unavailable` does.
    Asserts the premise first: `staged_spine_amendments` returns the six rows
    and the three rows. Then it asserts `_routed_amendments` returns
    `([], None)` and `_amendment_drafts` mints nothing for both ranges.
    Fails today because it returns 6 and 3 records. "A fixture amended after
    its act still mints" is test 2, cited beside it in the TC.

Smoke budget: test 10 reads two large trees, and tests 1, 6 and 6b spawn the
sweep subprocess. The builder measures the module with
`scripts/check_smoke_budget.py`. If it would breach the 60 s bar, the module
joins `tests/conftest.py` `SLOW_MODULES`, and test 1's in-process half stays
in `tests/test_intake.py` as the smoke pin, which keeps the per-family pin
rule.

### P3: the filter (`acceptance_record.py` 916 SLOC, `intake.py` 1719 SLOC = its ratchet ceiling)

The decision lives in `acceptance_record`. That module reads the ledger and
the copies today, already reads blobs through `kitlib.git.git_show` (`_show`),
and has about 80 SLOC of headroom under the 1000 threshold. That keeps
`intake.py`'s growth to a few lines. The filter's one caller is
`_routed_amendments`, which is the spec's "a helper it alone calls".

- **`_ledger_read(root, rev) -> (acts | None, failure | None)`**: the one
  ledger reader, through `_show` (`kitlib.git.git_show`). It has four
  outcomes:
  - `([], None)` when the tree does not list the ledger (absent);
  - `(acts, None)` when it parses;
  - `(None, "cannot be read")` when `UnreadableBlob` is raised;
  - `(None, "does not parse")` on a `TOMLDecodeError` or a non-list `act`.

  Read failure and parse failure are told apart at this one boundary, so
  the refusal names which happened (F2).
- **`_ledger_acts(root, rev)` keeps its contract byte-for-byte** for its
  unchanged readers (`reattested_between`, `_added_acts`, `lane_acted_set`,
  `reattest_scope_refusal`, `held_reattest_refusal`). Those are the merge
  rung's act reads, which the Trust section lists as unchanged under their
  established contracts. It becomes a two-line mapping over `_ledger_read`:
  - "cannot be read" maps to `[]`, which is today's `git_out` collapse;
  - "does not parse" maps to `None`.

  Making those rungs refuse a read failure too would change the merge
  rung's behaviour, which this WI does not own. It is surfaced below as a
  successor candidate. `reattested_between` keeps its exact refusal wording
  ("... nothing was merged"), which TC-278's tests pin. This is a 0->A->B
  extraction (one reader, two contracts over it), not a second ledger
  reader.
- **`_reattested_added(root, base, head) -> (ids, refusal_parts)`**: the
  filter's view of the ledger. It reads `_ledger_read` at both revisions:
  - a failure at either side is returned with its path, revision and kind;
  - otherwise it returns the re-attested ids of the entries whose `seq` the
    `base` side does not hold, the same rule as `_added_acts`, sharing its
    seq comparison.
- **`_snapshot_copy_rows(root, rev, rel_path, id_col) -> (rows | None, failure | None)`**:
  it reads `SNAPSHOT_DIR/<carrier>` through `_tier_carriers` in preference
  order, via `_show`. It has four outcomes:
  - no carrier listed: `(None, None)` (absent, so the row mints);
  - `UnreadableBlob`: `(None, "<path> cannot be read")`;
  - text that does not parse (`tier_rows_from_text` returns None):
    `(None, "<path> does not parse")`;
  - otherwise `(rows, None)`.

  It exists because `_spine_rows_at` collapses absence, read failure and
  parse failure all to `{}` (the spec's Trust section). `_spine_rows_at`
  itself is unchanged.
- **`settled_amendments(root, base, head, records, routed_cells) -> (settled, refusal)`**:
  1. With no records, it returns `(frozenset(), None)` without reading
     anything (D4).
  2. It reads `_reattested_added`. A read or parse failure is a refusal.
  3. For each record whose id is re-attested, it resolves `(csv_path, id_col)`
     by `_tier_of(rid)`. This is not by stem: assumptions.toml holds two tiers.
  4. It reads the live rows at `head` (`_spine_rows_at`) and the copy rows
     (`_snapshot_copy_rows`), once per registry. A copy failure is a refusal.
     A live read that yields no row for a record id leaves the row unsettled,
     so it mints: the record was itself read from that tree, so this collapse
     can only fail toward minting.
  5. The row is settled only when the copy holds it and
     `split_changed_cells(csv_path, id_col, copy_row, live_row)` shows no
     approved cell and no cell of `routed_cells` for that registry stem.
  `routed_cells` is passed in, so `intake.ROUTED_TRACED_CELLS` stays the one
  home of the routing rule.
- **`intake._routed_amendments`** returns `(records minus settled, refusal)`.
  **`_amendment_drafts`** returns `(drafts, refusal)`. **`intake_after_merge`**
  returns `([], refusal)` on it, before any other arm, like
  `_done_when_drafts`. The refusal is worded once in intake, because intake
  knows its routes: "the amendment mint was refused: <carrier> <cannot be
  read | does not parse> at <rev>; the merge stands - fetch or fix it in a
  reviewed commit, then `intake.py sweep --before <b> --after <a>`". At the
  sweep, `_cmd_sweep` already ends on the refusal through `_cli_result`.
- **Call sites that take the tuple:** `tests/test_intake.py` (two),
  `tests/test_adjudicate_brief.py` (one), and
  `tests/test_stage_event_detectors_driven.py` (two).
  `tests/test_traj_panels.py` only checks `callable`. TC-147's suite runs
  green on them.
- **IF-091** (`docs/requirements/interfaces.toml`, Drafted): the data cell
  gains "; settled_amendments(root, base, head, records, routed_cells) ->
  (settled ids, refusal) for the trunk mint, over the act ledger (IF-220) and
  the snapshot copies, refusing a present carrier that cannot be read or
  does not parse". The module docstring's `Contract IF-091` block gains the
  matching paragraph.
- **The ratchet:** `tests/test_module_size_ratchet.py` gets a reviewed
  upward re-stamp of `intake.py` by the measured delta, with the reason (the
  amendment arm's refusal). `acceptance_record.py` must stay under 1000
  SLOC. Crossing it would admit a new member to the watch set, so if that
  happens the builder stops and reports (SKILL §3 "Iterate" step 8).
- **RESYNC_PACK draft:** the `### <title> [since <lane base>]` entry is
  written now, because the smoke bar's `scripts/check_resync.py` refuses any
  shipped-file change without it. Its wording is finalised at P5 and its
  anchor re-stamped at P8.
- Tests: P2's twelve tests pass, and their xfail marks are removed. TC-147's,
  TC-278's and TC-331's suites (`tests/test_intake.py`,
  `tests/test_snapshot_readers.py`, `tests/test_integrate_admission.py`) run
  unchanged and green. Those suites pin `_ledger_acts`' preserved contract
  through `reattested_between` and the merge rungs.

### P4: the shared-walk restatement (D8)

- The comment block above `AMENDMENT_CSVS` ("THE PRE-COMMIT WARN'S SCOPE IS
  THIS SET TOO ...") gains one sentence. The mint additionally drops the rows
  the merged range re-attested (`settled_amendments`, LLR-NNN). The warn
  reads the unfiltered walk because it fires before any act.
  `staged_spine_findings` is unchanged; test 1's unfiltered-walk assertion is
  its pin.
- `docs/runtime-flows.md` Flow 4: the line `Intake-->>Slot: rows the merge
  forces, as ONE bookkeeping commit on trunk (LLR-153)` gains "minus
  amendments the range already settled (LLR-NNN)". `check_flows` runs in the
  bar.
- Tests added: none. TC-153's suite runs unchanged.

### P5: the workaround's removal (D9) and the RESYNC wording (D10), after P3 is green

- `project-trajectory/skills/coordinator-cycle/SKILL.md` §4 step 3: "sweep,
  and close the re-mint citing the act" becomes "sweep". Any row the sweep
  still mints is real work.
- `references/recipes.md` §3:
  - The **Sweep** bullet's "its re-mint takes the next WI id" becomes "a
    row it mints takes the next WI id".
  - The **The re-mint** bullet is deleted.
  - Its last sentence ("Two minted rows are real work and stay open: ...")
    is reworded as the general rule: every minted row stays open.
  - The post-gate-close clause about WI-911 goes with the deleted bullet.
- The `.claude/skills/` and `.agents/skills/` copies are rewritten
  byte-identical (`tests/test_skills_sync.py`).
- The builder greps `tests/` for "close the re-mint" first. Any test that
  pins the old wording moves in this row.
- **The RESYNC entry, final wording (F1: no authored text after the
  reviews).** The title is "The trunk mint skips amendments a lane already
  settled".
  - What changed: an adopter's trunk mint stops filing amendment rows for
    rows its lanes re-attested and left equal to their copies. A ledger or
    copy that cannot be read, or does not parse, now refuses the mint by
    name, and recovery is `intake.py sweep --before --after`.
  - What to do: nothing; no data migrates.
  - Kit-owned files to overwrite: `scripts/intake.py` and
    `scripts/acceptance_record.py`, plus the coordinator-cycle skill files
    if the delivery inventory ships them (the builder checks).

  From here on, only the `[since <sha>]` anchor and its "(Anchored at ...)"
  line may change (P8).

### P6: counted rounds and the checkpoint (D7, D12)

- **Counted rounds** (SKILL §3 "Iterate"; D12's A+B bar): REVIEW-A and an
  independent REVIEW-B, each from `review_brief.py review --scope full` over
  the lane's trunk base to its tip. The third counted round, if reached,
  renders `--stance convergence`. Each BLOCKER or MAJOR gets a coverage plan,
  then a fix. Rounds stop at the first one with no BLOCKER or MAJOR, or at
  the cap's dispute sitting.
- **The checkpoint:**
  1. Terra reconciles P1's set against the settled code, the arms map
     included.
  2. The closure check runs.
  3. One combined sitting judges the set: first approval of LLR-NNN and
     TC-NNN; LLR-153 and LLR-158 as amendments; the LLR-or-LLR-153 choice
     put to it (D7).
  4. Returns are routed and the returned rows re-sat.
  5. The accepted verdict is committed.
- Before the gate, restore the trunk-only generated views on the lane
  (recipes §3). The lane keeps its module-size stamp.

### P7: the gate over the checkpoint tip (D12)

- If trunk has moved only by commits the lane does not touch, rebase first,
  so the gate reviews the tip that lands and no post-rebase round is owed.
- Record the convergence map in the lane's decisions record. Then run the
  uncounted REVIEW-A and an independent REVIEW-B with `review_brief.py
  review --scope full --stance convergence`, over the checkpoint tip: code,
  rows, P4's comment and flow line, P5's skill text and P5's final RESYNC
  wording. Any BLOCKER or MAJOR goes to the dispute sitting. A fix round it
  orders is followed by one more checkpoint (P6) and gate before landing.
- This is the last review. Every authored change the landing carries is in
  the tip it reviews. After it come only:
  - the act, whose content P6's verdict judged and the act rungs bound;
  - the RESYNC anchor re-stamp, a sha and its anchor line;
  - the squash's regenerated views.

### P8: the act and the landing (D1, D7, D10)

1. **Rebase** onto current trunk, if P7 did not already. If the rebase
   changes code or authored rows, repeat the affected checkpoint and run an
   uncounted convergence round over the rebased tip before going on.
2. **The unchanged-rows check:** each row P6's verdict judged, at the
   verdict's commit, is compared with the rebased tip. A changed or
   renumbered row is re-sat, never acted on.
3. **The act turn:** `coordinator_adjudicate.py act --verdict <path> --wi
   WI-963`. It is the lane's last spine commit: Status flips and snapshot
   copies only. The amendment act re-attests LLR-153 and LLR-158 first,
   then the first-approval act approves LLR-NNN and TC-NNN, as the verdict
   authorizes.
4. **The squash:** regenerate, re-anchor the RESYNC entry at the landing's
   parent (anchor only), and run the commit bar on the staged squash. Then
   run `check_trajectory.py --strict` and `trace.py --strict`, and the full
   suite once at phase close. TC-269's and TC-271's suites run unchanged
   there, since they verify SR-178 arms this item does not touch: the needs
   file's drift report and brief (LLR-271), and the copy stamp (LLR-273).
5. **The sweep:** close the row, archive the tips, sweep. This is the first
   landing under the filter, so the sweep should mint no row for LLR-153 or
   LLR-158. Any row it mints is recorded and examined as real work, which is
   D1's live confirmation on the lane itself.

## Surfaced, not fixed here

- **No IF row declares the snapshot copies as a file seam.** IF-220 covers
  only the ledger. `acceptance_record` (the mirror rules, and now
  `settled_amendments`) and `baseline_snapshot`'s readers read
  `docs/archive/last_approved/<live path>` copies under no declared contract.
  This is a candidate successor row for the coordinator, outside this WI's
  scope.
- **The merge rung's act reads still collapse an unreadable ledger blob into
  absence.** `_ledger_acts` keeps its `git_out` contract for
  `reattested_between`, `_added_acts`, `lane_acted_set` and the two
  re-attest refusals (F2's preservation; the Trust section's unchanged
  readers). With the tri-state reader in place, moving them to refuse a read
  failure is a small, separate change of their contract. It is a candidate
  successor row, not this WI's.
- **The spec orders RESYNC last, but the commit bar needs it first.**
  "RESYNC entry, last" (Deliverables piece 4) cannot be literal, because the
  smoke bar's `check_resync.py` refuses a shipped-file change that has no
  entry. The plan drafts the entry at P3, finalises its wording at P5 (before
  the reviews), and re-anchors it at P8, at the trunk commit that carries the
  filter. The described behaviour is still true only once the filter lands.
