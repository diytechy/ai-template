+++
id = "WI-266"
title = "Status-map freshness gate purity (owner ruling 2026-07-21, repo-review-2026-07-21 M-10): exclude refs/llm/*-derived lines (open conflicts, reservations) from the --status --check byte-compare on every machine - the gate becomes a pure function of the committed tree - and label that section of the generated open-items.md as machine-local/advisory (as of the dispatch machine at generation time) so the exclusion is visible, not silent. Accepted trade recorded: those lines are guarded by frequent dispatch-loop regeneration + the label, not by a gate - the post-integration re-run of check.py deliberately skips them too (same exclusion everywhere, no split-brain)"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 263
+++

## Deliverable

Status-map freshness gate purity (gen_trajectory.py): the docs/open-items.md PENDING block is split into a committed-tree-pure gated region (blocked WI rows + run-state ask) and a machine-local advisory region (refs/llm conflicts/reservations/quarantine/stranded), separated by an always-present labeled boundary; a single _mask_machine_local() (anchored within PENDING_BEGIN..PENDING_END) drops the machine-local lines from the --status --check byte-compare on every machine, used by both the pre-commit gate and the post-integration re-run (no split-brain). Shipped OPEN_ITEMS.template.md placeholder updated to match. Tests bite. Adversarial REVIEW-A APPROVE f=1 (false-boundary fail-open, fixed).
