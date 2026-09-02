+++
id = "WI-569"
title = "WI-508 spine reseal: one clean reviewer round on current trunk, regenerate last_approved at the approval commit"
workstream = "process"
needs = ["OI-78", "WI-571", "WI-572"]
specref = ""
buildtier = "strong"
priority = 2
safety_class = "spine"
planmode = "single"
supersedes = "WI-508"
+++

## Deliverable

**A third act, taken knowingly.** The scope this row was narrowed to names two
arms: draw the round, and rule the two routed BLOCKERs. Amending two `Approved`
rows is a third, recorded here rather than left implicit because the drawn
round's subject was the rows as they stood BEFORE that amendment, so its new
text entered the lane unread by it. It is read now: the lane's own REVIEW-A
round 002 re-derived every corrected statement against the code, found each one
true, and found nothing true regressed. The structural backstop is the
amendment adjudication this row's merge mints over the amended rows, which
judges the new text on its own and owns the re-attestation that follows — no
`Status` moved on this lane and nothing under the snapshot was written, so that
judgement is unprejudiced.

**The round was drawn, and it did NOT confirm the rows.** The one clean
cross-family reviewer round the WI-508 lane never landed is
`docs/reviews/wi-569-wi-508-spine-reseal-one-clean/001-REVIEW-A-2f660cb7-spine-rows.md`,
drawn on current trunk `2f660cb7` on the cross-family strong route `OPENAI-SOL`
(gpt-5.6-sol, medium effort) against a hostile read-only brief that named the
four rows and the standing-claim rule and nothing about what had moved on trunk.
**`VERDICT: CHANGES-REQUESTED findings=2`** — two MAJORs, both against the
`Approved` LLR rows; scored `substance=0.667 precision=1.00 action=1.00`,
tripwires none.

- `TC-199` and `TC-200` **STAND, no finding.** All seven evidence node ids exist
  and pass, their `verifies` cells name the LLR arm rather than `SR-163`, their
  `expected` cells are still true, and TC-199's claim that two of its nodes are
  also TC-176's evidence checks out exactly. They stay `Drafted`, as ruled.
- `LLR-203` and `LLR-204` **DID NOT STAND.** Trunk moved under them: the
  file-to-requirement join, the independent shipped-tree universe, the
  mechanically parsed exclusion carrier and the four-class warn-to-gate checker
  are all delivered, and the two rows still asserted that none of them existed.
  Three of LLR-203's statements were false of the tree and one of LLR-204's was
  counterfactual; each was falsified by DRIVING, not by reading, and the round
  reached the same reading independently.

**What this lane did about it, and what it deliberately did not.** The false
sentences were corrected in the rows' own cells (`33aee707`). `Status` stayed
`Approved` on both — the approval act is the adjudicator's, and an amendment to
an approved row is expressly not one — so the amendment drifts the rows from
`last_approved` and returns them to the re-attestation brief. The DESIGN half of
the reviewer's remedy is NOT taken here: which row owns
`resolve_requirement_reference` / `mapping_purpose_findings` /
`MAPPING_FINDING_POLICY`, whether LLR-203's `CodeSymbol` widens, and where
TC-204's evidence binds are chain-reading calls a work lane does not hold the
chain for. That remainder is not left on no queue — the defect this row exists
to remedy: it is stated as the standing NOT-DISCHARGED gap in LLR-203's own
cell, and the amendment adjudication `intake` mints at this merge is confirmed
to list both rows.

**The two routed `5175065` BLOCKERs: ANNOTATED on trunk, no successor filed** —
the caveat arm of the choice, not the sterile-re-run arm. Both were re-verified
before ruling: the brief and the returns record are both first added by
`64e9bf2a`, so nothing immutably fixed the question before the answers existed;
and the instruction-context contamination is real, though the teams had already
disclosed it themselves at the line the finding anchors to. Standing caveats now
open both plan files, additively — the original text is unchanged, so the record
stays the record. A re-run was refused on three grounds: it cannot repair the
first defect at all (immutability is a property of the 2026-08-25 record, and a
fresh pre-committed brief would evidence a NEW exercise); no live requirement,
design or test row cites the exercise, so nothing on the spine waits on a better
number; and the alignment pass already declines to defer to either return.

**NOT DONE, by ruling rather than by omission:** no `docs/archive/last_approved/`
write and no `Status` flip. The row was minted with a baseline-reseal arm that
two merged predecessors removed from any work lane before this one started —
`WI-571` scoped the snapshot to the act, and `WI-572` ruled the whole approval
act the adjudicator's, on trunk. Nothing on the spine needed re-sealing when
that was ruled: at the lane base `2f660cb7` all four rows WERE cell-for-cell
identical to the round-010-approved tree `b8d57e9f`, which is the one claim in
the row's premise that survived contact. They are no longer, and deliberately —
this lane's own `33aee707` corrected three false statements on `LLR-203`
(`title`, `detail`, `rationale`) and one on `LLR-204` (`detail`), so those two
rows now drift from `b8d57e9f` on exactly those cells, and the re-attestation is
owed by the amendment adjudication this merge mints rather than by a baseline
re-seal. `TC-199`/`TC-200` are still identical to `b8d57e9f` at the tip. Driven,
not read: loading `docs/requirements/low-level-requirements.toml` and
`docs/test/test-cases.toml` out of each of `b8d57e9f`, `2f660cb7` and `HEAD`
with `tomllib` and diffing the four rows cell by cell returns IDENTICAL for all
four at the base, and at the tip `LLR-203 -> ['detail', 'rationale', 'title']`,
`LLR-204 -> ['detail']`, `TC-199`/`TC-200 -> IDENTICAL`, with `status` unmoved
on all four (`Approved`/`Approved`/`Drafted`/`Drafted`).

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

**WI-572 UPDATE (triage, 2026-09-02) — read this before the baseline
bullets below, which it supersedes.** The owner ruled `OI-78` **STAND**
(2026-09-01) and ruled that the approval act — every `Status` flip and every
`docs/archive/last_approved/` write — is the adjudicator's alone, on trunk;
WI-572 (merged 2026-09-02) now REFUSES at the merge slot any work lane whose
delta writes the snapshot directory or flips a Status. So on THIS lane: do
NOT run `intake.py snapshot` in any form, with or without `--approves`, and
do not touch `docs/archive/last_approved/`. Nothing on the spine needs
re-sealing anyway — `LLR-203`/`LLR-204` are byte-identical in the snapshot
and `TC-199`/`TC-200` stay Drafted — and under STAND the off-spine baseline
stays as it is. This row's remaining scope is therefore: (1) the one clean
cross-family reviewer round on current trunk confirming the four rows stand
in their reviewed state (the round file IS the deliverable; record its
verdict in the Deliverable); (2) rule the two `5175065` BLOCKERs below, each
by annotating the plan file on trunk or filing a successor row, and say
which. Any future re-seal of an off-spine registry is an adjudication's act
on trunk, not this lane's. The bullets that follow are kept as the record of
what the row asked before these rulings.

**The baseline.** Apply the owner's ruling on the `open_item` above, and only
after it lands (the mint parks this row `waiting:open-item-pending`):
- ruling **"stand"** -> regenerate `docs/archive/last_approved/` with `python
  project-trajectory/scripts/intake.py --root . snapshot` in THIS row's own
  approval commit (never copied from the branch's snapshot bytes, per OI-71 (c)),
  and record in the Deliverable that the regeneration RE-SEALS the absorbed
  off-spine rows rather than re-reviewing them;
  - **WI-571 UPDATE (triage, 2026-09-01):** `intake.py snapshot` is now SCOPED
    to the act (`baseline_snapshot.copy_live`) — a refresh copies only the
    registries an approving `Status` MOVE happened in, plus every registry
    `--approves` names, and leaves every other registry's snapshot bytes
    UNTOUCHED. **This row's approval commit moves no `Status`:** `LLR-203`/
    `LLR-204` are ALREADY `Approved` on trunk (the `580df781` flips the WI-568
    adjudication KEEPS) and this successor only CONFIRMS them, and `TC-199`/
    `TC-200` stay `Drafted`. So a bare `intake.py snapshot` here copies ZERO
    registries — no flip authorises the spine copy, and the off-spine
    `interfaces.toml`/`external.toml`/`components.toml` bytes are untouched. The
    two consequences:
    - the off-spine census SURVIVES to its own review instead of being zeroed
      by a whole-tree copy (the WI-571 fix) — good, and the default a bare run
      now produces;
    - the four spine rows are NOT re-copied either, which is correct because
      they are already sealed byte-identical in `last_approved`, so nothing on
      the spine needs re-sealing. If the owner rules **"stand"** and this row is
      to DELIBERATELY re-seal any registry through a snapshot refresh, it must
      NAME it — `intake.py snapshot --approves "<registry>=<ref>"` — since a
      bare run authorises no copy. To re-seal the off-spine baseline under
      "stand": `intake.py snapshot --approves
      "interfaces.toml=<ref>;external.toml=<ref>;components.toml=<ref>"`;
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
