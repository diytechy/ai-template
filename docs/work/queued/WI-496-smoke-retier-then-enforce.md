+++
id = "WI-496"
title = "Re-tier smoke to fit its 60 s ceiling everywhere, then enforce the seconds at the commit bar (OI-52 ruled (a), 2026-08-21)"
specref = "docs/requirements/open-items.toml#OI-52"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-52's ruling (a) ENFORCE LOCALLY, with the owner's tuning
mandate: the 60 s budget is a WORST-MACHINE ceiling, not a this-box target
— the tier should pass within 60 s on every dev machine (a fast box might
pass in 30 s), because the point of smoke is that it executes quickly. The
budget VALUE does not move in either direction.

Ordering is load-bearing — the re-tier lands FIRST:

1. **Re-tier.** The tier grew from ~900 tests to ~1,300 in a month and
   runs at 0.9–1.1x budget on this box (the 2026-08-21 re-measurement in
   `scripts/check_smoke_budget.py` is the current basis). Move the
   subprocess/scaffold-heavy modules that crept back into
   `tests/conftest.py` `SLOW_MODULES`, per the original tiering doctrine
   (the hook/gate/scaffold runs exercise them anyway). Target: restore
   real headroom on this box (the slowest known dev machine) — the tier
   passes comfortably under 60 s warm, measured over ≥3 runs, stamped
   with the fig: convention. Re-stamp the membership ratchet and the
   seconds stamp deliberately with reasons.
2. **Enforce.** Only after (1) lands green: the commit bar names the
   seconds — wire `check_smoke_budget.py --mode enforce` beside the
   pytest smoke command (session-protocol skill §3, CLAUDE.md's bar
   sentence, and the pre-commit surface if the hook runs smoke), so a
   breach fails the bar where it is introduced instead of being reported
   green. Keep CI's enforce lane as-is.
3. **Words.** The session-protocol skill and CLAUDE.md state what the bar
   now promises (results AND seconds, enforced), replacing the current
   wording that lets a worker read "passed" over a failed budget — the
   defect OI-52 was minted for.

Known risk, stated by the ruling: a wall-clock assert on a loaded box reds
an honest commit — that is why the re-tier precedes enforcement and why
headroom (not budget-fitting) is the target. If after re-tiering the tier
still cannot clear 60 s with margin on this box, STOP and hand the finding
back to the owner rather than moving the budget or softening the mode.
