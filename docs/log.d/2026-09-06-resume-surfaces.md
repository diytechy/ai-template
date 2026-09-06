## 2026-09-06 — Refresh the redesign resume surfaces

Starting revision: `ae610215`, branch `contract_split`, clean working tree.
The owner requested updated surface documentation and a fresh-session handoff.

Deferred open items: none.

Added [the September 6 handoff](../handoff-2026-09-06.md) with committed scope,
remaining SR-161/TC-211 work, separate artifact adjudications, the settled
Short-control ruling and its still-unmet launch prerequisites. It links the
existing execution, review, validation and migration records rather than
replacing their authority. The status board, documentation map and plan entry
now lead to it; older handoff/sitting instructions are marked historical.

The root README now points to derived stage/component views, reflects the live
approval and blackout dials, and describes invocation accounting and the
attended/unattended Critique distinction. The kit contents table names the
renderer package, shared snapshot and supported facade. No runtime, registry,
snapshot, queue, pause or policy change; no capped/watched document edited.
Regeneration refreshed dashboard/stage metadata and the approval brief's
snapshot provenance without changing artifact states.
No push. The existing broad implementation result remains the Full evidence.

Terra independently checked completion/authority claims, the SR-161 gap and
fresh-builder rework semantics against current source and records. Its proposed
wording change to the generated status banner was declined: “rendering” there
means the derived text view, not an import of the HTML renderer package, so no
source-code change is needed.

Validation:

```text
.venv/bin/python -m pytest -q -n auto -m smoke
1680 passed, 4 skipped in 62.51s (0:01:02)

.venv/bin/python scripts/check_smoke_budget.py --mode enforce
1680 passed, 4 skipped in 60.86s (0:01:00)
smoke wall-clock budget: 61.1s vs 60s budget -> OVER
```

The enforcer exited 1 on timing alone; the owner's standing local commit
exception applies. No test membership or ceiling changed.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=ae610215+resume-docs; out/run-logs/resume-surfaces-smoke.txt -->
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=ae610215+resume-docs; out/run-logs/resume-surfaces-smoke-budget.txt -->

`check_docs.py --root . --stale` passes with no broken links and the existing
`docs/test/report.md` orphan warning. `check_trajectory.py --root . --strict`
passes with the standing queue title/shared-spec warnings. `trunk_step.py
--root . --regen` and `git diff --check` pass. An additional
`check_figures.py --root . --strict` sweep exits 1 on pre-existing malformed
provenance markers in untouched September 5 logs; this change adds no findings.
Those historical markers are left for their own correction. Installed commit
hooks remain enabled.
