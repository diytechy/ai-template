+++
id = "WI-656"
title = "Checker findings that lie: interface-owner reachability, unbound design-row modules, section-anchored shared specs, and the generated-artifact list"
workstream = "scripts"
specref = "project-trajectory/scripts/coherence.py"
buildtier = "medium"
safety_class = "ordinary"
needs = ["WI-662"]
priority = 4
supersedes = "WI-670;WI-626;WI-658"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-670 (Count design rows that list a module none of their symbols binds in), WI-626 (Make the shared-spec warning compare section anchors, so distinct sections of one plan are distinct specs), WI-658 (Make the shipped stack profile's generated-artifact list match what the regeneration writes). Each is a false or missing advisory from `trace`, `check_trajectory` or the generated set: WI-656 and WI-670 both read a design row's `Module` cell (split `;`-joined cells once, then count what binds), WI-626 is the queue-conflict advisory, and WI-658 is the declared generated list the lane-close readers trust. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

**WI-670's precondition is ruled** (coordinator, ruling 1 of `docs/reviews/2026-09-27-wave4/ARBITRATION.md`, open to the owner's overturn): a design row's `module` cell lists the modules holding the row's `code_symbol` entries, so LLR-180 is amended as WI-670 describes. LLR-160 (WI-626) and LLR-180 are amended in place, status left `Approved`, and judged in the spine-acts batch; this lane files no adjudication. Build WI-656's `;`-split first: WI-670's count reads the same cells.

`trace.py` warns when an interface row's owner is named by no design row's
`Module` and declares no `Implements:` line. Two defects make that advisory
fire on owners that are traced:

- `coherence.llr_module_ids` takes each `Module` cell whole, so a cell listing
  several modules joined by `;` contributes one unusable key instead of one per
  module.
- `trace._implementing_modules` joins the profile's source root to paths that
  already start from it, producing `scripts/scripts/<mod>` keys that match no
  owner.

At b14d1808, IF-186 (`scripts/bookkeeping`) and IF-187
(`scripts/check_readability`) both get the advisory although design rows name
their modules inside `;`-joined `Module` cells.

IN SCOPE: split `;`-joined `Module` cells wherever the owner join reads them,
fix the doubled source prefix, and test both with an owner reached each way.
NOT IN SCOPE: changing what counts as reaching the spine.

Land with or after draft I (WI-662): once `;`-joined cells are split, a design row
that lists `bootstrap.py` without naming anything in it would count as
reaching the owner `scripts/bootstrap` (`interfaces.toml` ~353).

## Done-when

- A test with an owner named only inside a `;`-joined `Module` cell, and one
  reached only through an `Implements:` header, gets no advisory; an owner
  reached neither way still does.
- `trace.py` at the landing commit prints no reachability advisory for
  IF-186 or IF-187.
- The commit bar passes.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-670 (Done-when, verbatim)

- The ruling on the `module` cell's meaning is recorded.
- LLR-180's amendment is adjudicated, its test case gains one clause per new
  behaviour, and the count reports LLR-235-shaped rows a `main` coincidence
  used to hide.
- The commit bar passes.

### From WI-626 (Done-when, verbatim)

- The shared-SpecRef signal pairs two open items only when their files match
  and either their anchors are equal or one of them has none; the other two
  signals are unchanged.
- LLR-160's detail is amended to state the rule, in the same lane, Status
  untouched, for the adjudicator's re-attestation.
- Tests: different anchors in one file do not pair; the same anchor pairs; an
  anchor-less reference pairs with an anchored one in the same file; two
  anchor-less references to one file pair.
- The strict check's warning count on this repo, before and after, is quoted.

### From WI-658 (Done-when, verbatim)

- A test fails when a regeneration step writes a path the generated set
  omits, or the reverse.
- `integrate._abandoned_claim` and `audit` read the one home.
- A resync-pack entry names what an adopter must do, and the commit bar passes.
