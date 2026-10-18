+++
id = "WI-942"
title = "The merge slot reads an acted row's registry from its id, so a retirement alone in its registry is no longer refused as a widened copy"
workstream = "process"
sr_refs = ["SR-207", "SR-178"]
specref = "docs/decisions/wi-912.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = []
+++

## Context

Filed on trunk from WI-912's lane (wi-912 D-009, D-013 F5; status.md's
unfiled follow-ups, "from the adjudication split's lane"). D-008 accepted,
on the owner's ruling, that a checkpoint retiring an Approved row takes its
act: the coordinator-cycle skill's checkpoint step "Carry retired rows into
scope explicitly" relies on it, and plan item 14 retires LLR-297 and TC-312.
WI-912's derivation now lists a retirement (a re-attest of a ruled row
absent at the head) in `--reattests` while the recorded copy still holds the
row. D-009's builder then found the merge slot refuses one shape of it, a
refusal that predates WI-912: "a retirement whose registry carries no other
act in the branch: the acted-set reader finds a row's registry at the branch
head, where a retired row is absent, so its copy reads as widened". D-009
left it as residue for this row, "to land before the first lane whose
sitting retires a row alone in its registry", and ruled out pre-checking the
slot's rules in the derivation ("that would state them in a second home").
D-009's second case, a retirement on a held rung, is the held rung's rule,
not a gap. It stays refused.

**The original rationale, read before drafting.** WI-849 introduced
`lane_acted_set` as "THE ONE DERIVATION OF A LANE'S ACTED SET" (Sol r3), so
the scope, backing and copy checks judge one set. It resolved each acted
row's registry with `_registries_holding`, a search of the head's live
rows. It replaced `_reattested_registries`, which searched the head the
same way. Neither records a reason for reading presence rather than the id.
At the time no route produced a re-attested row that the head lacks. The
snapshot writer always placed a re-attested id by its prefix
(`baseline_snapshot._reattested_registry`: "By prefix rather than by
searching the live rows").

**The code path today, checked on trunk `cd6ba3160`.**
`acceptance_record.merge_approval_refusal` → `lane_acted_set` →
`_registries_holding(root, head, ledger | reattested)` returns no registry
for a row absent at the head, so `acted["reattest"]` maps the retired id to
`None`. `_copy_lines` then drops `None` registries from the authorized set
(`if reg`), and the registry copy the writer took for the retirement reads
as `snapshot WIDENED ... without an approved row`. It reads that way unless
another acted row in the same registry authorizes it. The writer and the
floor answer "which registry did this act move?" two ways. The writer reads
the id, and the floor reads presence at the head.

**Probe** (`C:/Projects/ai-template.wt/review-tmp/2026-10-17e/drafts/probe/probe_floor.py`,
output `probe_floor.out`; trunk's own test helpers, the real snapshot
writer, a released rung):
1. An Approved TC row is deleted and ruled CLARITY by an accepted amendment
   verdict.
2. The act derivation lists `{'reattests': ['TC-001'], 'retires': ['TC-001']}`.
3. `intake.py snapshot --reattests TC-001` copies the test-case registry.
4. The acted set reads `{'reattest': {'TC-001': None}}`.
5. The floor refuses the act, "snapshot WIDENED to docs/test/test-cases.csv",
   for a lane scoped to the amendment and for an unscoped lane alike.

With each acted row's registry read from its id's tier (patched in memory),
the acted set names the test-case registry and the floor admits the act.
WI-912's own round-2 probe saw the same refusal, and saw that the same
retirement beside a first approval in that registry merges.

**Where it bites.** It bites only a landing through the merge slot
(`integrate.py integrate`). The coordinator's `git merge --squash` landing
runs no approval-act reader until WI-808 lands (the residue in `## Trust`,
Ruling). Item 14's row is
not filed yet. Its sitting retires LLR-297 and TC-312 beside amendments to
LLR-183, TC-211 and TC-178, so each registry may already carry another act.
It retires a row alone only if one of those amendments takes no act in the
branch.

**The anchor.** SR-207 (Approved) is the anchor: an act re-attesting a row
"clears the refusal", and "the rule holds for every tier whose rows are
compared". LLR-245, under SR-207, counts a recorded row that the live
registry no longer carries as drift and clears it only when `--reattests`
names it. So the writer half of SR-207 already treats a retirement as an act
in its registry. The floor half refuses that same act.

The row amended is LLR-278 ("An adjudication re-attestation constrained at
merge"). It hangs from SR-178 and SR-228 and holds the WIDENED rule. Its
upward read does not change, since its copy-authorization clause already
answers SR-178. No SR changes.

## Deliverables

1. **The acted set reads each row's registry from its id**
   (`project-trajectory/scripts/acceptance_record.py`). In `lane_acted_set`,
   a row the act ledger names is placed in the registry its id's tier names
   in the approval walk. That covers a ledger-only approval and every
   re-attestation. The reader is `_tier_of`, which `held_reattest_refusal`
   already uses for the same ids. It is never the registry that holds the
   row at the head. A live flip keeps the registry the two-tree walk
   reports. `_registries_holding` is deleted.
   - A retired row named in an act's re-attestations therefore authorizes
     its own registry's copy.
   - An id of a tier the walk does not cover (`APPROVAL_ACT_CSVS`: SR, LLR,
     TC, SN, DA, SUR) still names no registry, so its copy stays WIDENED,
     as today.
   - `lane_acted_set`'s docstring drops "with the registry that holds it".
2. **Doc text.**
   - The `coordinator-cycle` skill's `references/recipes.md` §3 "The act
     turn" drops "and the merge slot still refuses a retirement whose
     registry carries no other act in the branch (a residue left to a
     follow-up row)". The kit source is
     `project-trajectory/skills/coordinator-cycle/`, and its copies in
     `.claude/skills/` and `.agents/skills/` stay byte-identical
     (`bootstrap.py --dest . --sync`).
   - `PROCESS_OPTIONS.md` is unchanged: "a copy of a registry no act moved
     is refused (WIDENED)" already reads right once a retirement counts as
     an act in its registry.
3. **Spine rows** (Terra authors; judged at the lane's checkpoint sitting).
   - **LLR-278** (Approved), **amended**. "a snapshot is WIDENED only when
     the complete acted set holds no approved or re-attested row in that
     registry identity:" becomes "a snapshot is WIDENED only when the
     complete acted set holds no approved or re-attested row in that
     registry identity, a row the act ledger names being placed in the
     registry its id's tier names whether or not the row remains in the
     live registry at the head, so a retirement authorizes its own
     registry's copy:". Its `code_symbol`
     drops `_registries_holding`, which is traced upkeep.
   - **TC-278** (Approved), **amended**.
     - Method gains: "On a RELEASED rung, an act whose only re-attestation
       retires an Approved row the lane deleted, ruled by an accepted
       amendment verdict inside the amendment scope, merges with that
       registry's copy as its only copy. The same retirement on a held rung
       is refused by row."
     - Expected gains: "a retired row's re-attestation authorizes its own
       registry's copy, whether or not another act moved that registry".
     - Evidence: the new tests.
   - **Unchanged:** SR-207, SR-178, SR-228, LLR-245 and TC-240 (the
     writer's half, already right); LLR-338 and TC-368 (the derivation
     already lists a retirement); SR-226 and LLR-286 (the retirement
     record).
4. **`RESYNC_PACK.md` entry**, anchored at the landing's parent. The
   kit-owned file is `scripts/acceptance_record.py`. The entry says the
   merge slot now admits a retirement whose registry carries no other act
   in the branch. Nothing migrates, and no setting changes.

## Trust

The act ledger and the snapshot copies already hold authority over the merge
gate (LLR-278's WIDENED and WITHOUT ITS ANCHOR checks). This row changes how
the gate reads one part of that input: a re-attested id that the head no
longer holds now authorizes its registry's copy. Written before the claim,
under
[`PROCESS.md` §3, "When a guard is owed"](../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer.** The act's snapshot write: `intake.py snapshot --reattests
  <ids>`, the command the act turn lists for a retirement
  (`adjudicate_act._amendment_text`), or a hand run of it.
  - **What it writes.** `baseline_snapshot.copy_live` copies every registry
    holding a named row, placed by the id's prefix. It appends one `[[act]]`
    entry, whose `reattested` holds the named ids, to
    `docs/archive/last_approved/acts.toml`, and the act commits both.
  - **What it refuses before moving any byte:** an id naming neither a live
    row nor a recorded one, a ledger that does not parse, and drift it
    would absorb into a registry it copies (SR-207).
  - **What a failed write looks like:** no copy and no entry (refused); a
    write left uncommitted, which is not on the branch the floor reads; or
    a ledger that does not parse at the head.
- **Consumers** (grep over `project-trajectory/scripts` and `tests` for
  `lane_acted_set`, `_registries_holding` and `acted[`):
  - `acceptance_record.py`:
    - `merge_approval_refusal`, the one caller of `lane_acted_set`;
    - `reattest_scope_refusal` and `backed_act_refusal`, which read the
      ids;
    - `adjudication_approval_refusal` → `_copy_lines`, which reads the
      registries for WIDENED and WITHOUT ITS ANCHOR.
  - `integrate.py`: `_approval_act_refusal` → `_merge_refusal` →
    `integrate_one`, the merge slot.
  - `tests/test_snapshot_readers.py`, which reads `lane_acted_set` directly.
  - **Not a consumer: the hand landing**, as in WI-943 (residue below). A
    `git merge --squash` landing's hook reads no acted set.
- **Ruling.**
  - **Unchanged refusals.** An unreadable snapshot delta is refused by
    `approval_delta`. A ledger that does not parse at the base or the head
    is refused, naming it (`reattested_between`).
  - **An absent ledger** (`docs/archive/last_approved/acts.toml`) reads as
    no entries, as does one git cannot show; only a ledger that does not
    parse is refused. Absent at the base (a base before the first snapshot
    act, or a record older than the ledger), it is an empty prior act set,
    so every entry at the head counts as this branch's and is judged for
    scope, backing and copy. Absent at the head while the base holds it (the
    branch deleted it), the branch adds no act: a registry copy beside the
    deletion is refused, and the deletion alone is refused on an unscoped
    lane but admitted on a scope-bound one, because the copy check skips the
    record's own files (the ledger and its README). That admission fails
    open, before and after this row; no kit route deletes the ledger. Absent
    at both, the ledger is not read and the branch adds no act.
  - **A changed copy no ledger entry authorizes** is judged by the copy
    check alone. Only a live flip into approval (or a row born approved) in
    that registry, itself backed by an accepted verdict, authorizes it;
    otherwise it is WIDENED on a scope-bound lane and refused as an act no
    accepted verdict backs on an unscoped lane. This row places only the ids
    that added entries name, so none of these cases changes.
  - **An id of a tier the approval walk does not cover** (a non-string or
    misspelt id included) names no registry, so its copy is refused as
    WIDENED.
  - **An id absent at the head** names its tier's registry: this is the
    change.
  - **The other checks still apply to a retirement:**
    - its scope, on a scope-bound lane (`reattest_scope_refusal`);
    - its backing, an accepted verdict in the branch that rules it
      (`uncovered_refusal`);
    - on a held rung, refusal by row ("below approval (or absent) at the
      act", SR-228 and D-009).
  - **What the authority binds to:** the ledger entries the head adds over
    the base (by `seq`), the copies in the base-to-head delta, and each
    id's tier.
  - **Tighter, not looser.** A ledger-only approval of a row absent at the
    head now owes its registry's copy (WITHOUT ITS ANCHOR) where today it
    owes none.
  - **No consumer fails open on a retirement.** Today's defect fails closed.
  - **Residue** (docs/decisions/coordinator-2026-10-17.toml#D-009): the
    coordinator's squash landing runs no approval-act reader until WI-808
    lands. WI-808 moves those landings onto the operation the loop uses,
    which runs `merge_approval_refusal`; this row corrects the rule that
    path will enforce. This row stays ahead of item 14's retirement lane
    regardless.

## Done-when

Each new test fails on the code before the change; the pins pass before and
after.
- **A retirement alone in its registry merges.** On a released rung, a
  lane scoped to an amendment deletes an Approved requirement row. An
  accepted amendment verdict rules it CLARITY, and the act
  `snapshot --reattests <id>` copies that registry alone.
  `merge_approval_refusal` admits it. It fails before: "snapshot WIDENED to
  <registry> without an approved row", as the probe shows.
- **The acted set names the retired row's registry.** It fails before (the
  probe reads `None`).
- **Pins:**
  - the same lone retirement on a held rung is refused by row;
  - a retirement outside the amendment scope is refused OUTSIDE;
  - a retirement that no accepted verdict rules is refused;
  - `test_a_combined_act_copying_a_registry_neither_section_moved_is_widened`
    passes unchanged.
- **`_registries_holding` is gone** from `acceptance_record.py`.
- **The recipes sentence is gone**, and the skill copies are
  byte-identical.
- **The spine.** LLR-278 and TC-278 carry the amended text, judged at the
  lane's checkpoint sitting, and TC-278's evidence names the new tests.
- **`RESYNC_PACK.md`** carries the entry.
- **On the landing tip**, the commit bar is green (smoke tier and budget
  enforce), and `check_trajectory.py --strict` and `trace.py --strict` are
  clean.

## Scope answers

- **S1.** One landable unit: a reader change, its tests, one recipes
  sentence, two row amendments and a RESYNC entry. WI-943, the MEANING-bless
  row filed beside it, is separate. It lands after this one, because both amend
  LLR-278, TC-278 and the same recipes paragraph, and this one carries the
  deadline.
- **S2.** Yes: the act ledger's re-attested ids gain authority over a copy
  the gate refused before. See `## Trust`.
- **S3.** Closed, deny by default. The input is each acted id.
  - An id of the approval walk's tiers (SR, LLR, TC, SN, DA, SUR) names that
    tier's registry, present at the head or not.
  - Any other id names none, so its copy stays WIDENED.
  - The bound covers ledgers the snapshot writer wrote. A hand-edited ledger
    is outside it (PROCESS.md §6).
  - **Stated residue, unchanged from today:**
    - A lone retirement of a stakeholder (STK) row stays refused. The writer
      copies the needs file for it, but the floor's walk does not cover the
      STK tier, which sits on a rung this repository holds.
    - An off-spine row's copy stays outside this rung
      (`OUTSIDE_THE_APPROVAL_ACT`).
- **S4.** `single`, because the row has a Trust section. A cheap test
  specifies the diff, but S4's criteria make a Trust row `single`, as
  WI-929's round 1 held. The construction is fixed above, so the plan step
  only checks it.
- **S5, architectural delta.** No new state, no new domain value, no new
  boundary. The gate's output stops depending on one input (the head's live
  rows) for a registry's identity. **Found, not fixed:** three readers turn
  a row id's prefix into a registry, over two tier sets:
  `baseline_snapshot._reattested_registry` and `adjudicate_act._tier` over
  `SNAPSHOT_TIERS`, and `acceptance_record._tier_of` over
  `APPROVAL_ACT_CSVS`. This row uses the floor's own reader and keeps its
  universe. Whether to consolidate the three is the coordinator's to file;
  this row does not need it.
- **S6.** No edges and nothing third-party.
  - WI-943 carries `~WI-942`.
  - When item 14's row (the sidecar retirement) is filed, its `needs`
    carries `~WI-942`. A hard edge would block its batch claim, and
    the order matters only for a slot landing.
  - Later rows, not edges: WI-851 amends LLR-278's held clause and TC-278.
- **B1.** The probe is evidence, and the item-14 reading is placement. No
  hidden work.
- **B2.** No split is minted on a work branch.
- **B3.** The floor reads the act ledger the act wrote in its own commit,
  and each id's tier. It stops reading current state (the head's live rows)
  to decide which registry an act moved.
- **B4.** No owner act or credential. LLR-278 and TC-278 sit on released
  rungs.

## Calls ruled at filing

- **The hand-landing gap** (owner, docs/decisions/coordinator-2026-10-17.toml#D-009):
  WI-808 owns it, and no hook-step row is filed. It is stated once, as
  residue in `## Trust`, Ruling; this row stays ahead of item 14's
  retirement lane regardless.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-17; CHANGES-REQUESTED, one finding):

- **S2, MINOR: adopted.** The Trust section's Ruling now reads: "**An absent
  ledger** (`docs/archive/last_approved/acts.toml`) reads as no entries, as
  does one git cannot show; only a ledger that does not parse is refused.
  Absent at the base (a base before the first snapshot act, or a record
  older than the ledger), it is an empty prior act set, so every entry at
  the head counts as this branch's and is judged for scope, backing and
  copy. Absent at the head while the base holds it (the branch deleted it),
  the branch adds no act: a registry copy beside the deletion is refused,
  and the deletion alone is refused on an unscoped lane but admitted on a
  scope-bound one, because the copy check skips the record's own files (the
  ledger and its README). That admission fails open, before and after this
  row; no kit route deletes the ledger. Absent at both, the ledger is not
  read and the branch adds no act." and "**A changed copy no ledger entry
  authorizes** is judged by the copy check alone. Only a live flip into
  approval (or a row born approved) in that registry, itself backed by an
  accepted verdict, authorizes it; otherwise it is WIDENED on a scope-bound
  lane and refused as an act no accepted verdict backs on an unscoped lane.
  This row places only the ids that added entries name, so none of these
  cases changes."
