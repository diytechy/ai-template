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

### WI-721 lands: the slow-tier reds cleared, and the full unfiltered suite green

- **Build and review:** one Sol build and one Sol fix round, with two
  Sonnet rounds.
  - [Round 1](../reviews/2026-09-28-wave6/sonnet-wi721-r1.md): SOUND, with
    one major. Approved LLR-286 still said "TOML registry", narrower than
    the fixed reader.
  - The fix round amended that one cell in place under the coordinator's
    grant, listed the new test in TC-299's evidence, and aligned IF-102's
    docstring.
  - [Round 2](../reviews/2026-09-28-wave6/sonnet-wi721-r2.md): SOUND at
    d7c43118.
- **What landed:** `retire.live_ids` reads through `spine_carrier`, so the
  three trace goldens pass with no golden regenerated. The skills-index test
  pins STALE again.
- **The full unfiltered suite:** `4816 passed, 15 skipped, 18 warnings in
  4998.50s (1:23:18)`, run with `--durations=30`.
  - It ran on e86cae4f plus this lane, in a throwaway worktree, with the
    WI-723 builder and reviewers sharing the box.
  - The durations are pasted in WI-721's Deliverable.
  - Two tests dominate the critical path:
    `test_traj_graph.py::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes`
    at 1160.6 s, and its fallback-graph sibling at 392.7 s.
  - Both route over graphs built from the live registries, and the router
    has not changed since 2026-09-06. So the jump from about 10 minutes
    follows the spine's growth.
  - Alone, on a mostly quiet box, the first takes **790.5 s** of call time
    (`1 passed in 965.37s`). No parallelism can finish the suite faster.
  - Filed as **WI-727**: profile the router, fix the cost or bound the test
    at a real scale, and re-measure.
- **Owed:** LLR-286's amendment goes to the next spine-acts batch.
- **Trunk before this squash:** 5124c932. The full-suite run did not
  include WI-723, which landed first; the next phase-close run covers both.
- **Bar:** smoke `1898 passed, 3 skipped`, 54.6 s against 60 s, within
  budget on a quiet box. check_trajectory --strict, trace
  --strict-integrity, gen_open_items, gen_trajectory, derive_stage,
  check_docs and the live approval brief are current.

### Spine-acts batch G (WI-724, WI-726, WI-728): eight SRs re-attested, nine rows returned, the LLR and TC anchoring held

- **The sitting:** one independent Opus adjudicator, which directed none of
  the amendments, sat once over three kit-composed briefs and took one act
  (seq 9). Every routed pointer cell was ruled. A flip showed no
  requirement-form finding.
- **Re-attested and anchored:** SR-015, SR-033, SR-111, SR-174, SR-177,
  SR-193, SR-223 and SR-225. These are the seven `delivered_with` rows and
  SR-193, each judged against OI-97.
- **Returned:**
  - SR-222 ("where the runner reports one");
  - SR-227 (its shall has no mint case or held-session case);
  - LLR-266 (history, and a false "already carried");
  - LLR-268 (the provider name's source is decomposed nowhere);
  - TC-264 (the revision is asserted for claude only);
  - LLR-223 and TC-220. `assumption_rules._classify` classifies a row whose
    only sibling shares no need as `joint`, contrary to SR-193. That is a
    defect WI-723 landed and its two review rounds missed.
- **Held:** LLR-267, LLR-269, LLR-270 and TC-262 are approved in the verdict
  but still Drafted. LLR-222, TC-222 and LLR-286 are blessed but not
  anchored. The snapshot refuses the LLR and TC registries while the returned
  LLR-223 and TC-220 drift, which is the brief's own stop case. Both the
  adjudicator and the cross-review confirmed it with
  `baseline_snapshot.refresh_refusal`.
- **Follow-up:** one consolidated Dispositions draft in WI-724. The sweep at
  this merge mints it, carrying the owed first approvals and
  re-attestations.
- **Cross-review:** Sonnet found the act SOUND, with one minor
  ([sonnet-batch-g.md](../reviews/2026-09-28-wave6/sonnet-batch-g.md)). It
  reproduced every return against the code.
- **Trunk before this squash:** f1733daa.
- **Bar:** smoke `1898 passed, 3 skipped`. Its seconds read 63.0 s
  against 60 s, with WI-545's builder and a Sonnet review running tests
  beside it. That is contention on a lane that changes only records, and
  the budget is not re-stamped. check_trajectory --strict, trace
  --strict-integrity, gen_open_items, gen_trajectory, derive_stage,
  check_docs and the live approval brief are current.

### WI-729 lands: batch G's returns answered

- **Build and review:** one Sol build, and one Sonnet round, SOUND with no
  findings ([sonnet-wi729.md](../reviews/2026-09-28-wave6/sonnet-wi729.md)).
- **What landed:** eleven items across SR-222, SR-227, LLR-266, LLR-268,
  TC-264, LLR-223 and TC-220, plus the three optional rationale and title
  items. Among them is the classifier fix: joint needs a sibling that shares
  a need.
- **Next:** the sweep mints the adjudication. The coordinator adds the
  batch-G carry-over to it: first approvals LLR-267, LLR-269, LLR-270 and
  TC-262, and re-attestations LLR-222, TC-222 and LLR-286.
- **Trunk before this squash:** a20b496a.
- **Bar:** smoke `1899 passed, 3 skipped`, 49.2 s against 60 s, within
  budget. check_trajectory --strict, trace --strict-integrity,
  gen_open_items, gen_trajectory, derive_stage, check_docs and the live
  approval brief are current.
