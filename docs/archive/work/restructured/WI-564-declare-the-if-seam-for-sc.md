+++
id = "WI-564"
title = "Declare the IF-### seam for schedule.py's lazy import of trace, clearing the strict ERROR WI-552 introduced"
workstream = "process"
specref = ""
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

Restructured into WI-582.

## Context

Drafted by WI-563 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

WI-552 arm 5 added `import trace as _trace` inside `schedule.load_oi_status`
(`project-trajectory/scripts/schedule.py:445`), creating a cross-component
import `scripts/schedule` (CMP-008) -> `scripts/trace` (CMP-006) with no
declared IF-### row. `check_trajectory.py --strict` errors on it (exit 1); the
same command at `b6e155d3^1` — trunk immediately before the WI-552 merge — is
ERROR-free, so the red is attributable to that work and not pre-existing.
IN SCOPE: choose ONE of the two exits the checker itself names — declare the
interface row in `docs/requirements/interfaces.toml` (the likely right answer:
the OI readiness gate really is a seam between the scheduler and the registry
reader, and a declared seam wants a covering TC per process.md §8) or retag the
component membership if the two modules genuinely belong to one component. Then
re-run `check_trajectory.py --strict` and show exit 0 on the ERROR line.
EXPLICITLY NOT IN SCOPE: the pre-existing WARN population (undeclared
connectivity, IF-without-TC, LLR CodeSymbol drift) — those long predate WI-552
and are their own burn-down; do not green them here. Also record, in this row's
Deliverable, the process finding this successor exists for: the WI-563
spot-check first passed the WI-552 close as clean because it declared a false
no-toolchain Bar and skipped the mandated `--strict` run. Setting
`[checks] components_check = false` is NOT an acceptable exit — that is
sanctioning the check to green a step.
