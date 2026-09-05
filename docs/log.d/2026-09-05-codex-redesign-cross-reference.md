## 2026-09-05 — Codex redesign cross-reference

Owner-directed documentation work on `redesign-codex-crossref-2026-09-05`, in the isolated `ai-template-wt-codex-crossref` worktree, based on `32a08c24`. Compared the current Claude plan and its review dispositions with the Codex proposal. The [comparison and disposition record](../ai-template-redesign-2026-09-05-codex/CROSS-REFERENCE-CLAUDE.md) identifies accepted elements, retained differences, source corrections, and the resulting implementation order.

Amended the Codex proposal to make replacement conditional on measurement, add common parsing/prompt boundaries and an early adopter oracle, compare the smaller integration alternative, improve owner resumption and LLR replacement, and stage renderer test selection. No kit implementation, registry, authority, test membership, or live-loop changes. Claude's source documents and historical Fable artifacts are unchanged. The primary checkout remains clean on `contract_split` at the original revision.

Validation: smoke `1638 passed, 4 skipped in 79.95s`; documentation check passed with zero broken links and non-fatal orphan/staleness warnings; strict trajectory check passed with non-fatal warnings; `git diff --check` passed. The separate enforced run also passed tests (`1638 passed, 4 skipped in 73.59s`) but failed the wall-clock bar: `73.8s vs 60s budget -> OVER` (exit 1). Changes remain uncommitted in the isolated worktree because the required commit bar did not pass; no budget or test-tier changes were made to fit this run. No full-suite or implementation acceptance claim.

Deferred open items: none created by this documentation task. Proposed implementation and unresolved choices remain in the linked review plan, not an active implementation commitment.

### Owner-requested integration

After the timing failure and uncommitted status were disclosed, the owner explicitly requested merging this workstream into `contract_split`. Proceeding with that documentation-only integration under the owner instruction; the timing bar remains failed, not waived globally or restamped. Revalidation through `python scripts/check_smoke_budget.py --mode enforce` ran the declared smoke command: `1638 passed, 4 skipped in 71.27s`; enforced wall time `71.5s vs 60s budget -> OVER`, exit 1. Documentation links and `check_trajectory.py --strict` passed with non-fatal warnings. Normal Git hooks remain enabled. No full-suite claim. <!-- fig: check_smoke_budget.py --mode enforce; workstream based on 32a08c24 with the documentation diff recorded by this commit -->

Target had independently advanced to `2e37c9e2` with Claude’s reciprocal comparison. Preserve those changes and this comparison’s original source revision; do not reinterpret the original findings as a review of that newer Claude revision.
