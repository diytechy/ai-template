+++
id = "WI-565"
title = "Rule and apply the intake._SPEC_NEEDS_RE no-DOTALL residual, and clear the two cosmetic WI-552 leftovers"
workstream = "process"
needs = ["OI-77"]
specref = "docs/archive/work/complete/WI-563-spot-check-the-clean-close-of.md"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++

## Context

Drafted by WI-563 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Gated on the owner's ruling by construction: the `open_item` cell above makes
`intake._inject_open_item` mint a `pending` OI at this row's merge and land its
id in THIS row's `needs`, so the successor parks
`waiting:open-item-pending` until the ruling lands (OI-73 exit (B) — there is no
standalone OI exit; the OI is always a dependency of a queued successor).
Riding along, because they are one small pass over the same two files and were
also left on no queue by the first spot-check pass: (i) `intake._OI_ID_RE`
(intake.py:304) is dead — `next_oi_id` reads the watermark and
`trace.live_max_ids`, nothing uses the regex; delete it or use it. (ii)
`check_trajectory.validate`'s docstring disagrees with the shipped
`known_ois=None` coercion at check_trajectory.py:812 (`known_ois = known_ois if
known_ois is not None else frozenset()`); fix the docstring to state what the
code does. Both are cosmetic and neither needs the ruling — but do them in the
same commit range so the residual list from the WI-552 review closes out whole.

Advisory registry joins (WI-388; never gating):

### Pending open items whose WI-Refs touch this row's kin (premise risk)
- OI-77 (pending): intake._SPEC_NEEDS_RE (intake.py:1344) has no re.DOTALL, so _replace_inbound_edges silently skips a dependent whose `needs` is a MULTI-LINE TOML list: WI-552 a…
