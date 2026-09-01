+++
id = "WI-555"
title = "Execute OI-71: convert the wi508 complete-close to a handback and close it partial through the kit's shape"
specref = ""
workstream = "process"
sr_refs = []
needs = ["WI-554"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

> **Record-only lane — verify on trunk, not on this branch's tree.** By OI-71's
> sanctioned manual special case, the wi508 mutations were performed directly on
> trunk, not carried in this claim branch's diff (which touches only this WI's
> spec, logs, and review records). This branch was cut at base `6d3d9db4`,
> before the conversion landed, so its tree still shows the pre-conversion state
> — that is expected, not a false close. The effects are committed on trunk
> `contract_split` at `551d1b2c` (commits `09f88ca2` partial → `979c3e5f` merge
> → `551d1b2c` WI-568 mint); the shipped admission path there returns
> `_claimed_specs(wi508)=[]`. Verification recipe and the REVIEW-A false-positive
> reconciliation: `docs/log.d/WI-555-wi508-partial-close.md` (rework section).

OI-71 (c) executed: the held wi508 lane's complete-close was CONVERTED to a
partial handback and closed through the kit's own path — nothing discarded.

1. Local `wi508-architectural-remap` created at the origin HELD ref (the ref
   "renamed back" to match the trunk claim); the spec restored from
   `archive/work/complete/` to `active/` (undo the self-close); then
   `handback.close_partial` wrote the immutable report
   `docs/handbacks/WI-508-wi508-architectural-remap.md` (outcome `partial`,
   reason, `commit_range ff29fef8..6ba27110`, `split_decided_by = "adjudicator"`)
   and moved the spec to the terminal `docs/work/partial/`. Verified drainable:
   the verdict gate stands down (no APPROVE owed), exactly as OI-71 predicted.
2. Merged via `integrate.py integrate` from the trunk root as a partial close
   (no verdict owed): trunk `6d3d9db4` → `551d1b2c`, `bar PASS (11 steps)`,
   `audit clean`. The six generated/record conflicts took trunk's side and were
   regenerated; the approval brief was regenerated with the WI-554-fixed renderer
   and is current on trunk.
3. Intake minted the disposition row **WI-568** from the report — it carries the
   keep/discard adjudication (under OI-70's bounds) that drafts the re-land
   successor. The last_approved REGENERATION condition is that successor's job.
4. Phantom head cleared: the wi508 claim left trunk's `active/`,
   `check_trajectory` is clean (the OI-70 hold-by-rename WARN is gone), scheduler
   and dispatcher agree (WI-508 reads `partial:terminal-stopped-early`). The
   SR-163 rows reached trunk with their honest branch status intact; the
   LLR-203/204-Approved-vs-Drafted question is flagged for WI-568 in the log.

Full execution record: `docs/log.d/WI-555-wi508-partial-close.md`.

## Context

Execution record and the exact conversion sequence live in the log fragment
`docs/log.d/WI-555-wi508-partial-close.md`.

`OI-71` RULED 2026-08-31: (c) — the lane closes `partial`, performed MANUALLY
as the special case its history makes it, and nothing is discarded. The branch
(`wi508-architectural-remap-HELD-for-owner-verdict`, pushed to origin
2026-08-31) closed itself COMPLETE on its own ref, so as it stands the
integrator reads `merged` and the verdict gate demands a fresh APPROVE; the
gate stands down for a handback BY DESIGN (only `merged` owes a verdict), so
the close must first be CONVERTED. The mechanics are on `OI-71`'s row and in
`docs/handoff-2026-08-31.md` §1; the six expected merge conflicts are all
generated or record files, with the precedented remedy on the branch itself
(`52faa5d8`: trunk's generated side; `log.md` spliced base + lane + trunk).
`needs = WI-554` because the successor regenerates the approval brief and
round 019's two trunk-side renderer defects would re-red it.

## Done-when

1. The ref renamed back to `wi508-architectural-remap` and the complete-close
   converted (the lane's close commit reverted, or the close re-performed
   into `partial/`) so the spec's directory reads handback, with the
   immutable report under `docs/handbacks/` naming outcome, reason, commit
   range and keep/discard.
2. The lane merges through `integrate.py integrate` as a partial close — no
   verdict owed — with conflicts resolved by the precedented remedy and
   `docs/ratify/CURRENT.md` regenerated on trunk after the merge.
3. The disposition row mints from the report; its adjudication (keep/discard,
   under `OI-70`'s bounds) drafts the successor that re-lands the reviewed
   spine content — the LIVE registry edits re-landed and
   `docs/archive/last_approved/` REGENERATED via `intake.py snapshot` at the
   successor's own approval commit, never copied from the branch's snapshot
   bytes (the ruling's degradation-risk condition).
4. The phantom head clears: `docs/work/active/wi508-architectural-remap/`
   leaves trunk's `active/`, scheduler and dispatcher agree, and the four
   Drafted spine rows reach trunk unflipped.
