+++
id = "WI-569"
title = "WI-508 spine reseal: one clean reviewer round on current trunk, regenerate last_approved at the approval commit"
workstream = "process"
needs = ["OI-78", "WI-571", "WI-572"]
specref = "docs/work/complete/WI-568-dispose-the-close-recorded-at.md"
buildtier = "strong"
priority = 2
safety_class = "spine"
planmode = "single"
supersedes = "WI-508"
+++

## Context

Drafted by WI-568 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

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
  - **WI-571 UPDATE (triage, 2026-09-01):** `intake.py snapshot` is now SCOPED
    to the act (`baseline_snapshot.copy_live`) — a plain run at this row's
    approval commit copies only the registries a `Status` flip authorises (the
    `LLR-203`/`LLR-204` spine rows) and leaves the off-spine `interfaces.toml`/
    `external.toml`/`components.toml` snapshot bytes UNTOUCHED. So a bare
    regeneration no longer re-seals the absorbed off-spine rows — the off-spine
    census SURVIVES to its own review instead of being zeroed. If the owner
    rules **"stand"** on the off-spine baseline, this row must name those
    registries explicitly to re-seal them: `intake.py snapshot --approves
    "interfaces.toml=<ref>;external.toml=<ref>;components.toml=<ref>"`. Absent
    that, "stand" on the spine and "leave the off-spine census standing" is the
    default a bare `intake.py snapshot` produces;
- ruling **"review-then-stand"** -> the owner reads the absorbed diff
  (`git diff 6d3d9db4 551d1b2c -- docs/archive/last_approved/docs/requirements/`)
  and amends any rejected row LIVE in the registry through the ordinary
  amendment path — the amended row then drifts from the snapshot and returns
  to the re-attestation brief for an explicit act — and only after that act
  does this row regenerate the snapshot as under "stand". A byte-level
  RESTORE of the `6d3d9db4` snapshot is NOT an option: the mirror invariant
  (`committed_snapshot_findings`) reds a snapshot file that is not a copy of
  its live counterpart at the commit that wrote it, permanently — the wi508
  lane's own decision 10 measured that red and reverted — and it would
  re-land external.toml's since-corrected header comment.

**OWNER BRIEF for the open item this row mints** (the mint carries only the
one-line question — `intake._mint_open_item` writes title/status/raised/
one_line/wi_refs and nothing else — so this is the brief; round 002 (Terra)
MAJOR; corrected at round 004):
- *Blast radius.* What moved into the approved baseline with the handback
  merge, all written on the branch by `580df781`/`4824c0ba`: interfaces.toml's
  132 changed / 30 added / 3 removed rows (rulings `OI-64`, `OI-65`, `OI-67`;
  rows `WI-522`, `WI-528`, `WI-530`, `WI-531`, `WI-533`, `WI-534`, `WI-553`),
  components.toml's one absorbed row (behind `WI-520`), and external.toml's
  header comment (a stale "dial of 4" claim replaced by the correct
  DevStg-Boundary wording — a correction, not a row). The re-attestation brief
  now reads "1 changed" for the off-spine registries where it read 132 before
  the merge. Nothing on the spine (LLR/TC) moves under either answer.
- *Options.* **STAND** — accept the bytes as the baseline; this row regenerates
  the snapshot with `intake.py snapshot` at its own approval commit, which
  re-seals the same content. **REVIEW-THEN-STAND** — the owner reads the diff
  above; any row they reject is amended live, which returns it to the brief
  through the ordinary path; the reseal follows that act. A byte-level RESTORE
  is unavailable by construction (the mirror invariant, above).
- *Recommendation.* **REVIEW-THEN-STAND.** STAND is within authority
  (`DevStg-Needs` leaves the Arch and Boundary rungs loop-approvable), but the
  132 rows entered the baseline as a side effect of a `partial` lane's
  handback merge, not as an approval act, and were never shown to anyone as a
  batch. Reading the diff once costs an hour; STAND without it accepts rows
  unseen.
- *Reversal cost.* STAND then review later: any row can still be amended live
  at any time and re-enters the brief — nothing is lost, only the batch view.
  REVIEW-THEN-STAND: the amendments are ordinary edits; the reseal is one
  `intake.py snapshot` commit.

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

Advisory registry joins (WI-388; never gating):

### Pending open items whose WI-Refs touch this row's kin (premise risk)
- OI-78 (pending): Does trunk's docs/archive/last_approved/ baseline for interfaces.toml, external.toml, and components.toml STAND as-is at the wi508 branch's 2026-08-30 bytes — …
