+++
id = "WI-267"
title = "Retired WI status (owner ruling 2026-07-21, repo-review-2026-07-21 L-34): add a terminal retired Status to the work-item vocabulary (queued/deferred/done/retired) - a wont-build row that stays in the registry forever with the reason in Deliverable; NOT overloading done. Audit every Status consumer before flipping any row: check_trajectory (counts, DAG, spec-lifecycle R-F done => empty SpecRef must decide how retired interacts), gen_trajectory dashboard buckets/legend, agent_loop/agent_dispatch queued-WI selection, derive_gate if it reads WI status, and the shipped templates/PROCESS_OPTIONS wording (downstream vocabulary change - migration note). Driving case: triage the five archive-anchored deferred rows WI-060/061/062/063/082 (re-spec against a live home or retire with reason) - per-row disposition needs the owner at WI build time"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 264
+++

## Deliverable

Terminal retired work-item Status + full consumer audit (L-34): adds a sixth Status (queued|active|done|deferred|blocked|retired) - a won't-build row with its reason in Deliverable, TERMINAL not a done-overload. R-A/R-F extended (retired = non-empty Deliverable + empty SpecRef); a retired predecessor does NOT satisfy a hard dependency (conservative - surfaced via a new dead-dep finding, warn/ERROR --strict); separate dashboard bucket (#78716c/glyph/legend) + counts never folded into done; consumers audited across check_trajectory/schedule/agent_dispatch/gen_trajectory + the agent_common preflight guard (derive_gate/agent_loop confirmed no-change); PROCESS_OPTIONS + work-items.template vocabulary updated (byte +352, baseline re-stamped). 14 tests (12 bite). The five archive-anchored deferred rows WI-060/061/062/063/082 remain deferred pending the owner's per-row triage. Adversarial REVIEW-A APPROVE f=2 (missed agent_common consumer + count test - both fixed).
