# OI-130 re-score: the depth-0 component partition on today's tree

An attended analysis session on 2026-11-08 (saved 2026-11-11), at the owner's
request. It measured what decision 10 of 2026-08-13 deferred and nobody ran
afterwards: P5 was to be approved "after WI-448 and the re-tier, on re-derived
numbers". WI-448 closed on 2026-08-23. This is measurement only. No code,
registry row or open item changed. Trunk `refactor_again` at `0fe7277b2`.

The answer to OI-130's question is in [Scores](#scores). What it means for
WI-999 is in [What this changes](#what-this-changes), and the handoff that
carries it is
[handoff-2026-11-11a-attended-oi130-rescore.md](../../handoff-2026-11-11a-attended-oi130-rescore.md).

## Why OI-130 needed re-measuring

- OI-14 (2026-08-13) ruled two things. One home per behaviour is a hard
  constraint. Cut count (import edges crossing a component boundary) is the
  tie-breaker.
- WI-441's data pack found the constraint unsatisfiable by any partition: 12
  behaviours lived as 39 copies in 16 modules, so the copies were the
  violation, not the boundaries
  ([data pack §0](../../archive/plans/2026-08-13-part-a-data-pack.md)). The
  shortlist used **straddle** as its working stand-in for the constraint: how
  many of the 12 behaviours have copies in more than one component.
- Ranked by straddle with cut as tie-breaker, the August numbers give P5, P4,
  P3, P1, P2. The recorded order is P5, P3, P4, P1, P2. The one swap was a
  stated judgement: P4 needed 15 interface rows that did not exist. Neither of
  OI-130's two Q2 options, cut alone or straddle alone, describes that rule.
- All of it was measured on a 55-module tree. Today there are 130 modules, and
  `kitlib/` exists.

## Method

- **Inventory and edges.** 130 modules under `project-trajectory/scripts/`.
  555 internal import edges, with `kitlib.x`, `rendering.x` and relative
  imports resolved. The live seam check resolves only bare stems (see
  [Defects](#defects-in-the-live-partition)).
- **Shared kernel.** The 7 modules in `docs/kernel-modules-allow` are a shared
  layer K in every candidate. An edge into K is not a cut, which is the live
  rule. A copy in K beside a copy elsewhere is a straddle, because the outside
  copy should import K.
- **Candidates.** P5\* is the live tags resolved to one home per module. P3\*
  and P4\* apply August's rules to the 75 modules added since. The placements
  are in `score.py`. P1 is not re-scored: the retired CMP-001..005 define no
  home for the new modules. P2 is not re-scored either, because its shared
  kernel is now in every candidate as K.
- **Behaviour census.** `census.py` finds 92 function names defined in more
  than one module. Three independent readers (Claude Opus sub-agents) read
  every definition and classified each group. Their tables are in
  [classifications.md](classifications.md). B1–B12 of 2026-08-13 were traced
  again by behaviour, not by name. The rolling review's confirmed §13.B policy
  duplicates were added where its text names the modules (see
  [the rolling review](#the-rolling-review-branch)).
- **Census totals.** 19 POLICY behaviours ([policy.json](policy.json)) and 18
  PLUMBING behaviours ([plumbing.json](plumbing.json)) have more than one
  independent home. A copy that delegates to a shared home is not counted.
  Inline `endswith("-000")` checks are not counted.

## Scores

| Candidate | Cut | Boundaries | Policy straddle /19 | Plumbing straddle /18 |
|---|---:|---:|---:|---:|
| **P5\* narrow-waist (W1–W4)** | **140** | **6** | **12** | **10** |
| P3\* actor (A–E) | 152 | 9 | 15 | 11 |
| P4\* functional (F1–F9) | 235 | 22 | 14 | 15 |

**P5 ranks first under every objective:**

- straddle first, then cut (OI-14, with the constraint read as "fewest
  violations"): P5, P4, P3;
- cut alone: P5, P3, P4;
- boundary count: P5, P3, P4.

Selecting P5 needs no human override.

**Bias.** P5\* inherits the live placement, and the new modules' placements in
P3\* and P4\* are judgement. P4's gap is structural: it has 22 boundaries. P3's
gap (152 against 140) is small enough that other placements could narrow it.

## One home per behaviour: still a code obligation

No partition satisfies the constraint. Under P5, 12 policy behaviours still
straddle a boundary, and 7 more have copies inside one component. **11 of the
19 policy duplicates disagree on some input.** The readers ran most of these,
and their tables say which:

- **B3 `value_to_cell`:** `None` becomes `''` in migrate_carrier and `'None'`
  in spine_carrier. The pin has no None case.
- **B5 SN-id universe:** on a TOML needs file, `check_docs` and `check_flows`
  scrape ids from comments and descriptions, and `check_flows` also counts
  SN-000. The `need_ids` pin returns early on TOML, so it checks nothing.
- **B8b spec parse:** `wi_convert.parse_spec` and
  `kitlib.registry.parse_spec_row` disagree on `title = 5`, on an id that does
  not match its filename, and on `["a;b"]`.
- **B10 ref split:** `adjudicate_brief`, `consolidate` and `intake` split on
  `;` only. As a result, `consolidate.py:451` misses OI edges that
  `split_pred_edges` finds. This is the defect class of August's B10.
- **B12 module key:** `migrate_carrier._short_module` differs from
  `kitlib.spine.norm_module` on `__init__.py` and on non-`.py` paths.
- **Queued-spec lookup:** given two matching specs, `handback` takes the first,
  `integrate` refuses, and `consolidate` takes the first.
- **Id number from an id:** `kitlib.spine` and `kitlib.decisions` take the
  digits after the last dash. `wi_convert` and `kitlib.registry` take the first
  run of digits.
- **Rolling review §13.13, §13.14, §13.16 and §13.22:** spec precedence, the
  generator freshness arm, the declared-file grammar and the command
  tokenizer.

## Defects in the live partition

These are separate from the ranking.

1. **Membership drift.** 29 of 130 modules carry two or three component tags.
   August's adoption of P5 had resolved its 5 multi-tags to 0. A module's
   membership is the union of the tags on every LLR that names it. As a
   result, 194 cross-component edges reach only the warn-only advisory.
2. **The seam check cannot see dotted or relative imports.**
   - `trajectory_arch._classifiable_edges` matches an import by its bare stem,
     so `kitlib.spine` never matches `spine`. Every import into `kitlib/*` or
     `rendering/*` is skipped.
   - 10 cross-component edges have no interface row, and nothing reports them.
     Three examples: `check_perf` to `kitlib/spine`, `check_privacy` to
     `kitlib/secret_classes`, and `rejudge` to `kitlib/observation`.
   - CMP-006's note says the edges into `kitlib/station` and `kitlib/verdict`
     are "policed as an interface row", but this check cannot see them.
3. **The module → component join exists twice:**
   `gen_components.module_components` and `trajectory_arch.module_components`.
   A test covers only the second.

## The rolling review branch

`origin/rolling_review` (`04488d5cd`, 14 commits off `e73e49cf83`, unmerged)
holds the 2026-11-05 maintenance review in
`docs/reviews/rolling-review-2026-11-05/README.md`. Its findings bear on this
work in three ways.

- **It confirms this re-score independently.**
  - The duplication: §2.1 (`load_wis`), §2.2 (git runners) and the §13.B list.
  - The multi-tag drift: §13.42 counts 34 of 162 files, all files included.
  - The component rows list their modules instead of naming what each hides:
    §13.32, the rubric's own B3 tell, and §3.2.
- **It questions WI-999's premise.** §13.32 finds SR-165 is one of four
  incompatible specifications of a "stopping record". The others are
  PROCESS_OPTIONS' (d2), spine-questions §3 and rubric A8. The review proposes
  two optional CMP keys, `hides` and `stops`, in place of SR-165 and LLR-172.
  Its own verifier notes that SR-165 is Approved under SN-040, so the change is
  an amendment act. The verifier prefers a cheaper route: move SR-165 under the
  dual-plan layer.
- **It points at owner rulings that already moved this ground**
  ([review-churn plan](../2026-10-11-review-churn/README.md)):
  - variant F (item 11, revision 35) declares membership on the realization
    and retires LLR → CMP, which removes the multi-tag cause. Its migration
    sits in phase 3, which is structural and runs last;
  - item 12 ruled a decomposition critique at depth 0 that gates the first LLR
    sitting there. It also ruled an Architect role owning `components.toml`,
    and `run.cmd audit` with an `arch` part, the ruled home for the
    measurement done here by hand;
  - the [W3 dry run](../2026-10-11-review-churn/w3-dry-run/README.md)
    (2026-10-25) already found W3 the under-decomposed component.
- **What the review does not have:** the seam check's blindness to dotted
  imports, and most of the divergences listed above. Those are the
  `;`-only splitters, the SN-id universe on TOML, `value_to_cell` on None, the
  queued-spec lookup, the spec-parser split, the duplicated component join and
  `traj_status._clip_title`.

## What this changes

- **OI-130's Q1.** The evidence now supports approving P5 as the depth-0
  partition on today's numbers. That is option (b), a fresh ruling the record
  can cite, and it settles whether the 2026-08-22 approval closed decision 10.
- **OI-130's Q2.** No longer a choice between objectives that rank
  differently. The honest record is OI-14 with its constraint measured as
  straddle and cut as the tie-breaker. P5 ranks first without an override.
- **WI-999.** Whether to build SR-165's record as written, or settle its shape
  first against rolling review §13.32 and item 12, is the owner's call. The
  analysis recommends settling the shape first.
- **Unfiled rows.** The seam check's import resolution, the diverged policy
  duplicates, and the duplicated component join are each a row to file.
  Nothing has been filed.

## Re-running

From the repo root, writing the outputs to a scratch folder, not here:

```bash
python docs/plans/2026-11-11-oi130-rescore/live.py <scratch>/live.json
python docs/plans/2026-11-11-oi130-rescore/census.py
python docs/plans/2026-11-11-oi130-rescore/score.py <scratch>/live.json docs/plans/2026-11-11-oi130-rescore/policy.json
python docs/plans/2026-11-11-oi130-rescore/score.py <scratch>/live.json docs/plans/2026-11-11-oi130-rescore/plumbing.json
```

`score.py` writes `scores.json` beside `live.json`. The census JSON files are
hand-built from the readers' classifications. A copy that is later folded into
its home drops out of them by editing, not by re-running.
