49d5a9a6f83c53b2aaa0fc9f926021339fb4b368 NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/plan_coverage.py:456 — A cited fragment replaces the finding ID without checking that the ruling concerns the excluded finding. Confirmed reproduction: the review’s F1 concerns a launcher budget and F2 concerns wording; an accepted verdict dismisses only F1. `Excludes: F2 — dismissed: docs/reviews/wi-001/003-ADJUDICATE-abc1234.md#F1` passes with exit 0. An unrelated dismissal therefore clears an unresolved finding, contrary to Done-when and D-003. LLR-069’s “or cited ruling id” wording also permits this substitution without requiring correspondence.

- docs/requirements/system-requirements.toml:726 — SR-155 does not cover the shipped rework-dispatch rule. Its requirement and acceptance concern work marked for contested planning, rival decompositions and SELECT/PAGE outcomes. An ordinary reviewed build requiring rework falls outside that condition, although the new skill requires coverage before dispatch. Re-attesting LLR-069 and TC-069 leaves the new obligation without a covering SR; PROCESS.md’s requirement-gap route requires the parent obligation to be authored and judged.

## MINOR

- project-trajectory/scripts/plan_coverage.py:177 — The new docstring says the coordinator and loop “both call” the shared step; project-trajectory/RESYNC_PACK.md:7660 repeats that claim. Repository call-site inspection shows no loop replan invocation. The attended skill procedure exists, while loop integration remains WI-805’s future work. The shipped text incorrectly describes that future integration as present.

## Verified

The requested tests passed. WI-870’s strict verdict-word reader composes with finding extraction: `parse_verdict` retains finding lines independently of the verdict word. IF-046’s merged data cell accurately describes this split. New Implements tags match LLR-069’s module and symbols; amended approved rows have no Status flips and act 77 re-attests them. The RESYNC anchor is a trunk ancestor. Baseline checks confirmed verdict-shaped input previously exited 2 and an exclusion citing FIX previously passed. The worktree remained clean.

## Commands

- Requested pytest command, with the literal basetemp and `PYTHONDONTWRITEBYTECODE=1` — **69 passed in 4.30s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — **exit 0**, clean with advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi-853-review-repro.py` — unrelated dismissal **exit 0**; baseline verdict input **exit 2**; baseline FIX exclusion **exit 0**.
- `git diff 0b550da9..49d5a9a6f83c53b2aaa0fc9f926021339fb4b368` and scoped diffs/`--stat` — reviewed authored changes.
- `git diff --check 0b550da9..49d5a9a6f83c53b2aaa0fc9f926021339fb4b368` — clean.
- `git merge-base --is-ancestor c5076d62 0b550da9` — exit 0.
- `git show`, `git log --oneline`, `Get-Content` and `rg` — inspected baseline code, commits, rules, spec, proposal, reports, registries, sitting records and call sites.
- `git status --short` — clean before and after review.