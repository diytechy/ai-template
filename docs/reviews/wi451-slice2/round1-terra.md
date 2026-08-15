# Adversarial review round 1 — WI-451 slice 2

**Reviewer:** OPENAI-TERRA (`gpt-5.6-terra` via `codex exec`), fresh context, did
not author the change. **Rubric:** [code-review-adversarial.md](../../rubrics/code-review-adversarial.md).
**Diff under review:** `ad0d0456..e6cdc8fd` (acts 1–3 + the status update).
**Round taken:** 2026-08-14.

## Verdict as returned

```
- [MAJOR] docs/architecture.md:44 -> the committed architecture maps now say `no source scanned`; the declared `--src project-trajectory/scripts --check` command exits 1, and five full-suite graph/component tests fail -> regenerate the maps from the declared source root -> @owner
- [MAJOR] docs/requirements/low-level-requirements.toml:1751 -> new Draft LLR-171 is phase 5 under phase-1 SR-035, making derive_gate and its independent phase derivation disagree; the full suite fails -> align the child/parent phase contract and its test -> @owner
- [MAJOR] tests/test_trajectory_staged.py:557 -> the suite still requires the deleted SR-tier `SupersededBy` ratified-cell entry, so the retired-supersession change leaves a full-suite failure -> retire or update this stale assertion while retaining CMP `SupersededBy` coverage -> @owner
- [MAJOR] docs/plans/2026-08-14-wi451-slice2-ledger.md:124 -> signed Act-3 counts are false: the act changes 66 LLR detail cells, re-points 78 demotion TCs, rewrites 42 matching `expected` cells, and flips 58 re-parented LLRs Verified→Modified—not 69/68/32/69 -> correct the ledger and its log-fragment claims from the actual TOML diff -> @owner
- [MAJOR] docs/requirements/low-level-requirements.toml:637 -> the rider claims SR-060's dead `docs/next-wi` clause was struck, but its successor still states `never status.md/next-wi` -> remove the retired-pointer clause or retract the execution claim -> @owner
VERDICT: CHANGES-REQUESTED findings=5
```

## Author disposition — all five CONFIRMED and FIXED

Every finding was re-verified by the author before fixing (rubric R5), and none
was refuted. The round earned its keep decisively: **four of the five were
invisible to the commit bar the author actually ran.**

| # | Finding | Re-verification | Fix |
|---|---|---|---|
| F1 | arch-map destroyed | CONFIRMED, and worse than reported: `git diff` showed **1,413 lines deleted** from the generated module map. The author had run `gen_arch_map.py` with DEFAULT args, which scans a non-existent `src/` and emits an empty map with a warning the author did not read. | Regenerated with the declared `--src project-trajectory/scripts`; diff vs base is now 21 legitimate lines. `--check` green. |
| F2 | LLR-171 phase 5 under phase-1 SR-035 | CONFIRMED. | LLR-171 + TC-165 → phase 1. **Root cause ran deeper than the finding** — see below. |
| F3 | stale `SupersededBy` ratified-cell assertion | CONFIRMED at `tests/test_trajectory_staged.py:557`. | Assertion inverted to pin the column's ABSENCE from both halves (so a silent re-classification still reds); the WI-388 comment records the retirement; CMP coverage untouched. |
| F4 | signed counts false | CONFIRMED — and this is the repo's most-guarded defect class ("Signed measurements"). The author had reported the MANIFESTS' INTENT rather than measuring the applied diff. Re-derived: 83 re-grounded / **68** detail addenda / **58** flips / **78** TC re-points / **42** expected rewrites. (Terra's own detail-cell figure of 66 was itself slightly off; the author's re-derivation is carried with its producing command.) | Ledger + fragment corrected, now carrying a `fig:` marker with the reproducing command. |
| F5 | SR-060 rider claimed but not executed | CONFIRMED — LLR-061 still read `never status.md/next-wi`. Verified `docs/next-wi` does not exist and no script reads it. | The dead half struck (`never the generated status surface`); the LIVE `status.md` prohibition kept. |

### What F2 actually uncovered (bigger than the finding)

Aligning one row exposed the systemic version: the demotions re-parented
long-standing **phase-1** children onto newly minted **phase-5** parents,
taking child/parent phase mismatches from **19 (base) to 144**. The new
parents' phase was the author's own unexamined default — they govern work that
shipped in phase 1, not new phase-5 work. Fixed by giving each new parent the
phase in which the bulk of its decomposed work was delivered (SR-154/157/158/159
→ 1, SR-153/155/156 → 4; the six SN-coverage mints and the CI pair keep 5, having
no children and being genuinely new work). Mismatches now **38** — still above
base, and named as owed rather than declared clean.

### The process failure this round exposes, stated plainly

The author ran only the **smoke** tier and treated it as sufficient. The
protocol requires the **full unfiltered suite** before claiming a slice done;
the full suite is exactly what surfaced F1/F2/F3. Smoke was green through all
of them. Recorded so the next session does not repeat it.

**After fixes:** `pytest -q -n auto` → **2489 passed, 11 skipped**;
`trace.py --strict` → `orphans=0 integrity=0`; `check_trajectory --strict`
clean with the dangling-WI WARN class cleared.

### Round accounting

These fixes POSTDATE the verdict, so under the merge-queue rule the APPROVE is
spent and **another round is owed before this lane merges** — that is the gate
working, not a defect. The lane is deliberately left OPEN at a slice boundary,
so that round belongs to the session that closes it.

One honesty note: the author began fixing the dangling-WI-refs issue (found by
this same round's `check_trajectory` output) while the reviewer was still
running, so the reviewer observed a briefly-dirty tree. Perturbing a review's
subject mid-round is a mistake; recorded rather than hidden.
