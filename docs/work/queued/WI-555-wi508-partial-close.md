+++
id = "WI-555"
title = "Execute OI-71: convert the wi508 complete-close to a handback and close it partial through the kit's shape"
specref = "docs/requirements/open-items.toml#OI-71"
workstream = "process"
sr_refs = []
needs = ["WI-554"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

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
