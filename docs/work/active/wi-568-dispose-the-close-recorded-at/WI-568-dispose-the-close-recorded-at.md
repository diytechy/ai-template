+++
id = "WI-568"
title = "dispose: the close recorded at docs/handbacks/WI-508-wi508-architectural-remap.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = "docs/work/partial/WI-508-architectural-remap-program.md"
buildtier = "strong"
safety_class = "adjudication"
brief = "disposition"
+++

## Context

The closed spec is `docs/work/partial/WI-508-architectural-remap-program.md`.

Its per-close report is `docs/handbacks/WI-508-wi508-architectural-remap.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

**Named for this adjudication (WI-555 round 005, 2026-09-01):**

- The `580df781` keep/discard explicitly includes the LLR-203 / LLR-204 `Drafted` -> `Approved` flips: stand or revert. They were `Drafted` on trunk at `6d3d9db4` and are `Approved` at `551d1b2c`; the flip is loop-permitted under `human_approval_through = "DevStg-Needs"`, so the question is disposition, not authority.
- It explicitly includes the `docs/archive/last_approved/` baseline move for the off-spine registries: the merge `979c3e5f` carried the branch's snapshot bytes (`580df781` / `4824c0ba`) onto trunk, shifting the baseline off the pre-merge anchor `6d3d9db4:docs/archive/last_approved` (last written at `13593db9`) and collapsing `docs/ratify/CURRENT.md`'s off-spine census from "132 changed, 30 added, 3 removed" across nine rulings to "1 changed, 0 added, 1 removed (WI-553)". Restore trunk's baseline to the `6d3d9db4` bytes for `interfaces.toml` / `external.toml` / `components.toml`, or let the absorption stand — owner-owed; mint an OI through this row's `open_item` cell if the adjudicator judges it needs the owner.
- The handback report's `## Delivered` sentence "the four Drafted slice-1 spine rows" is inaccurate: the true split is 2 `Approved` (LLR-203, LLR-204) / 2 `Drafted` (TC-199, TC-200). Read the archived spec at `docs/work/partial/WI-508-architectural-remap-program.md` and the WI-555 log entries in `docs/log.d/WI-555-wi508-partial-close.md` as the corrected record; the report is immutable and stays as the claim it was.

## Dispositions

```toml
title = "WI-508 spine reseal: one clean reviewer round on current trunk, regenerate last_approved at the approval commit"
workstream = "process"
safety_class = "spine"
priority = 2
supersedes = "WI-508"
planmode = "single"
buildtier = "strong"
open_item = "Does trunk's docs/archive/last_approved/ baseline for interfaces.toml, external.toml, and components.toml STAND at the wi508 branch's 2026-08-30 bytes — absorbing interfaces.toml's 132 changed / 30 added / 3 removed rows (OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553) and components.toml's 1 changed row (WI-520), while external.toml had no row-level census — or is it RESTORED to the pre-merge 6d3d9db4 bytes so those rows return to the re-attestation brief for explicit approval?"
```

IN SCOPE — four rows and one baseline question.

**The rows.** `LLR-203`, `LLR-204` (`Approved` on trunk) and `TC-199`, `TC-200`
(`Drafted` on trunk, `verifies = ["LLR-203"]` / `["LLR-204"]`, `Expected` scoped
to the LLR arm). Draw the ONE clean cross-family reviewer round the WI-508 lane
never landed — the "fresh reviewer round on a refreshed tree" its own handback
report lists under *Not delivered* — on CURRENT trunk, confirming the four rows
stand in their reviewed state. **The `580df781` `Drafted` -> `Approved` flips of
`LLR-203`/`LLR-204` are KEPT by the WI-568 adjudication**: that is a named keep
decision, not a defaulted one — the flip was loop-permitted under
`human_approval_through = "DevStg-Needs"` and the rows are byte-identical to the
round-010-approved tree (`b8d57e9f`), so the successor CONFIRMS them and does not
re-litigate the flip. `TC-199`/`TC-200` STAY `Drafted`; do not approve them here
(their `verifies` drift is normal on an unapproved row).

**The baseline.** Apply the owner's ruling on the `open_item` above, and only
after it lands (the mint parks this row `waiting:open-item-pending`):
- ruling **"stand"** -> regenerate `docs/archive/last_approved/` with `python
  project-trajectory/scripts/intake.py --root . snapshot` in THIS row's own
  approval commit (never copied from the branch's snapshot bytes, per OI-71 (c)),
  and record in the Deliverable that the regeneration RE-SEALS the absorbed
  off-spine rows rather than re-reviewing them;
- ruling **"restore"** -> re-copy the `6d3d9db4` off-spine snapshot files
  (`interfaces.toml`, `external.toml`, `components.toml`) under
  `docs/archive/last_approved/` in a reviewed commit, then regenerate
  `docs/ratify/CURRENT.md` and let the re-attestation brief re-list the rows for
  an explicit act.

**Inherited ruling.** This row inherits `OI-72`'s `SR-163` ruling (owned and
discharged by the re-scoped `WI-543`); do not re-open the `SR-163` shape.

**Routed here rather than dropped** — the two `BLOCKER`s of
`docs/reviews/wi508-architectural-remap/010-REVIEW-A-5175065.md`, which the
WI-508 close left on no queue and which target files that are on trunk:
1. `docs/plans/2026-08-25-blind-minimal-map-brief.md:3` — the anti-post-hoc
   condition is uncovered: brief and both agent returns first appear together in
   `64e9bf2a`, so nothing immutably fixes the question before the answers exist.
2. `docs/plans/2026-08-25-blind-minimal-map-derivation.md:29` — both "blind" teams
   received this repo's instruction context (Team B a memory index), breaking the
   brief's closed five-file input set.
Do NOT re-run the blind exercise here. Rule each: either annotate the two plan
files on trunk with the defect as a standing caveat, or file a successor row for
a sterile re-run — and say which, in the Deliverable.

EXPLICITLY NOT IN SCOPE: any revert of the `ff29fef8f9..6ba2711078` range (WI-568
ruled KEEP-all); re-opening `WI-508` (closed, superseded); the `5175065` Team-A
census MINOR and the wider off-spine WARN population.
