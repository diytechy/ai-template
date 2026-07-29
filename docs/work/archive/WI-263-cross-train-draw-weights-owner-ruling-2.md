+++
id = "WI-263"
title = "Cross-train draw weights (owner ruling 2026-07-21, repo-review-2026-07-21 M-31): the per-phase draw ordinal counts prior same-phase sessions ACROSS trains (drop the train prefix from the count key), so each train draws its own reviewers and the long-run frequency of provider selection converges to the declared weights - the advertised weight 4 draws ~4x as often becomes true across trains, not only within multi-round trains. Two-train share test required (the existing 18-rounds-single-train test is exactly the case that hides the reset); keep the draw deterministic given the session history. BUILD DOUBLE-CHECK (code-verified 2026-07-21): phase_draw_ordinal (agent_common.py:868) globs the LOCAL iter_dir - a fresh train worktree has NO sibling-train logs, so merely relaxing the regex train-prefix (the existing train=None branch) still counts 0 and the fix is a silent no-op. The count MUST read from a durable cross-train aggregate (the committed docs/iteration logs in the main repo / shared iter_dir), not the train-local worktree dir; the two-train test must exercise real cross-worktree state, not one dir with mixed prefixes"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 260
+++

## Deliverable

Cross-train draw weights (agent_common.py + agent_loop.py): phase_draw_ordinal(iter_dirs, phase) now counts same-phase sessions across the durable PRIMARY-worktree committed docs/iteration aggregate (primary_worktree_root + draw_iter_dirs) unioned with the worker-local dir, de-duped by filename, so the declared provider weights converge ACROSS trains (not only within a multi-round train) and a fresh worktree is no longer a silent 0. Real cross-worktree two-train test bites. Adversarial REVIEW-A APPROVE f=1 (docstring-accuracy MINOR, fixed).
