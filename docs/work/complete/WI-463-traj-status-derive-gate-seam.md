+++
id = "WI-463"
title = "Declare the traj_status->derive_gate seam: check_trajectory reports 'cross-component import scripts/traj_status (CMP-009) -> scripts/derive_gate (CMP-006) has no declared IF-### seam' — a WARN at the defaulted floor and the ONE ERROR at --strict on a clean tree (measured 2026-08-15, pre-dating the sweep, log 2026-08-15n), so check_trajectory --strict cannot read clean until it lands. Scope: mint the one IF row with owner/req_refs per the 2026-08-15e conventions, or retag the membership if the import is genuinely intra-component — decide from the code, don't default. Distinct from WI-390's inherited-drift clause (which names the arch-map no-IF warns and the undeclared registry rows, not this edge) and from the wi455 lane's B-06/B-07 mints (external crossings; this is an internal seam)."
workstream = "process"
sr_refs = ["SR-159"]
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

**Real seam, declared — `IF-130`.** `traj_status._stage_line` calls
`derive_gate.bar_label(gate)`, the ONE rendering home for the OI-30 D2
release-ceiling note, precisely so the status snapshot and every other
surface render the withheld top bar identically. Both component tags are
correct (`components.toml`: CMP-006 lists derive_gate, CMP-009 lists the
traj_* modules), so retagging was ruled out from the code. Row minted
`Consumes` (a Q2 coverage declaration), `signal = discrete` (closed-set bar
name in, name or name+fixed-suffix out), `owner = SR-049` — derive_gate's
own SR; no LLR names `bar_label` (LLR-050 pins `compute`, LLR-139 pins
`_pause_pending`), so ownership falls to the SR per the R4 fallback —
`req_refs = [SR-049, SR-159]`, mirroring sibling IF-084's shape.
`check_trajectory --strict`'s one clean-tree ERROR is GONE; the expected
follow-on WARN (no `Contracts:` docstring line declares IF-130) is the
standing class the wi455 lane owns. Watermark IF 129→130. PROVISIONAL,
overturnable at the sitting like every drafted row.

## Context

Recorded at the 2026-08-15 sitting sweep (log `2026-08-15n`) after the
stash-test proved it fires identically on the clean tree at HEAD — it is
inherited, not the sweep's. The bar note in `docs/status.md` says to run
`check_trajectory.py --strict` unfiltered before claiming anything done;
this edge is currently the one ERROR standing between a clean tree and that
command reading clean, which makes every future session re-derive the same
"is this mine?" answer this row now records once.

`traj_status` (CMP-009, the trajectory/status projection family) imports
`derive_gate` (CMP-006, the gate derivation family). If the read is the
status snapshot asking the derived gate for the current bar/stage, that is a
real seam and the IF row should say so (direction, endpoints, `owner` +
`req_refs` per the `2026-08-15e` conventions — SR-159's family owns the
connectivity rule, but the row's own owner is whoever owns the contract).
If instead the import is a leftover that should move or the membership tag
is wrong, retag — but decide from the code, not from which fix is cheaper.
