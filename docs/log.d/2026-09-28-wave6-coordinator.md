## 2026-09-28 — The sixth coordinator session: owner rulings, WI-721 and WI-720, Sol builders under Sonnet review

Resumed from [the wave-5 handoff](../handoff-2026-09-28-wave5-coordinator.md).
The owner first ruled OI-95 to OI-97
([2026-09-28-owner-rulings-oi95-oi96.md](2026-09-28-owner-rulings-oi95-oi96.md),
[2026-09-28-owner-ruling-oi97.md](2026-09-28-owner-ruling-oi97.md)). Reviews
for this session are in [../reviews/2026-09-28-wave6/](../reviews/2026-09-28-wave6/).

### The builder launch, tested

The handoff's roles make Codex Sol the builder, launched through `codex
exec`. The first launch was refused by the coordinator's permission
classifier ("Create Unsafe Agents"). The owner allowed a temporary
`Bash(codex exec *)` rule in `.claude/settings.local.json`, to be removed
when the queue drains, and the launch then ran.

Both builders built and tested in their worktrees, but neither could
commit. Codex's `workspace-write` sandbox keeps `.git` read-only, and
`--add-dir` naming the primary `.git` did not change that (`Permission
denied` on `.git/worktrees/wi-NNN/index.lock`). The coordinator commits
each builder's change on its lane branch, and the commit says so. The
sandbox was not widened.

The `sonnet` alias resolves to Sonnet 5 here, the newest Sonnet available,
not the 5.5 the handoff names.

### WI-720 lands: SR-222's and SR-227's chains restated as standing prose

- **Build:** one Sol build, committed as 9a7c063d.
- **Review:** one Sonnet round, SOUND
  ([sonnet-wi720.md](../reviews/2026-09-28-wave6/sonnet-wi720.md)). Its one
  minor finding (SR-227's rationale also lost the cache comparison) is
  accepted as still true.
- **What landed:** thirteen registry cells on nine Drafted rows, the IF-245
  docstring sentence, and TC-268's evidence pinned to the skip line.
- **Next:** the sweep mints the rows' first approval.
- **Trunk before this squash:** 4dd6827d.
- **Bar:** smoke `1890 passed, 3 skipped`. Its seconds read 64.7 s and
  65.4 s, over the 60 s budget. A control at the parent commit 4dd6827d,
  in a throwaway worktree, read 91.1 s, so the box was loaded (desktop
  apps, a game) and this cells-only lane is not a regression; the budget is
  not re-stamped. check_trajectory --strict, trace --strict-integrity,
  gen_open_items, gen_trajectory, derive_stage and check_docs are clean.

### WI-725 lands: the spot check of WI-720's close, CONFIRMED

An independent Opus spot-checker judged WI-720's close at bbe00d8a:
CONFIRMED
([record](../reviews/wi-725-spot-check-the-clean-close-of/001-SPOTCHECK-bbe00d8a.md)).

- **Folded into WI-724's Context:** three observations on the rows WI-724
  adjudicates, plus a docstring note. These are LLR-266's remaining history
  phrases and a false "already carried" claim, TC-264's Method overclaiming
  the pinned revision, and SR-222's "where the runner reports one".
- **Corrected:** the cell count in WI-720's Deliverable and above.
- **Not filed:** no new row.
- **Bar:** smoke `1890 passed, 3 skipped`. Its seconds read 329.0 s, with
  WI-723's builder and a Sonnet confirmation running tests beside it. That
  is contention, not this documentation-only lane. The spine and doc checks
  are clean.

### WI-723 lands: the joint-delivery class (OI-97 (a))

- **Build and review:** one Sol build and one Sol fix round, with two
  Sonnet rounds.
  - [Round 1](../reviews/2026-09-28-wave6/sonnet-wi723-r1.md): NOT YET
    SOUND. SR-024's sibling was not argued from its rationale.
    `assumption_rules.py` had reached exactly 1000 SLOC by cutting the
    explanations out of its advisory text, and it computed undeclared ids
    in two places.
  - [Round 2](../reviews/2026-09-28-wave6/sonnet-wi723-r2.md): SOUND at
    35444157. The builder accepted every finding, so no arbitration.
- **What landed:** `delivered_with` and the joint class, with SR-193's chain
  amended in place.
  - Seven rows are joint: SR-015, SR-033, SR-111, SR-174, SR-177, SR-223 and
    SR-225.
  - SR-024 and SR-129 stay unclassified, because no rationale sentence
    carries a sibling.
  - The ratchet is re-stamped at 1028 with its reason.
- **Owed:** the amendments and the nine rows' re-opened attestations go to
  the next spine-acts batch.
- **Trunk before this squash:** e86cae4f.
- **Bar:** smoke `1898 passed, 3 skipped` (eight new tests). Its seconds
  read 136.5 s against 60 s, with WI-721's full unfiltered suite running
  `-n auto` on the same box, so this is contention and not re-stamped.
  check_trajectory --strict, trace --strict-integrity, gen_open_items,
  gen_trajectory, derive_stage, check_docs, and the live approval brief
  (`trace.py --approve modified`) are current.
