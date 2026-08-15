## 2026-08-14 — WI-451 slice 2, act 3: the 73 demotions land, and the spine closes (orphans=0)

The layer-by-layer method's second constructive step (`2026-08-14g`): with the
SR layer decided, each demoted row landed under the parent whose obligation it
decomposes. **SR 137 → 64**; the fan-out matched the design's sn_refs-derived
map exactly (SR-157×15 · SR-070×15 · SR-155×10 · SR-154×6 · SR-153×5 ·
SR-156×5 · SR-159×5 · SR-158×4 · SR-006×3 · SR-026/030/112/144/148×1 = 73).
Per-row dispositions, riders and the shed-clause map:
[plans/2026-08-14-wi451-slice2-ledger.md](../plans/2026-08-14-wi451-slice2-ledger.md).

**The finding worth recording as a deliverable (13s): ZERO new LLRs were
needed.** All 73 obligations fit an existing component-level carrier — 83 LLRs
re-grounded, 68 taking a `detail` addendum folding the tokens the LLR did not
already state, and not one row left homeless. That is the census's central
claim — *these rows were always LLRs wearing SR ids* — confirmed mechanically
rather than asserted. Had the mis-tiering been about substance rather than
altitude, the demotions would have had nowhere to land.

- **`orphans=0 integrity=0`** — SN=27 · SR=64 · LLR=153 · TC=148. The spine is
  fully joined in both directions for the first time in the campaign. The
  bottom-up sweep the method asks for found nothing dangling because the
  top-down pass closed it; the one orphan act 2 left behind (SR-035's
  Analysis→Test flip) is discharged by minting **LLR-171 + TC-165** (watermark
  TC 164 → 165).
- **78 TCs re-pointed**, and 42 `expected` cells that read *"Satisfies SR-NNN
  AcceptanceCriteria"* rewritten to name the parent plus the LLR that now
  carries the acceptance — a dangling "satisfies" pointer is precisely the
  silent-rot class this campaign exists to remove.
- **Form findings 9 → 2**: exactly the two recorded 13v waivers (SR-140,
  SR-147). Every other multi-shall row dissolved on landing at its own tier —
  the form rule's own prediction, observed.
- **Boundary-Refs: 0 uncovered of 64** (149 of 149 at slice start), so
  sitting-3 decision 8's deferral condition — *"until slice 2 populates
  Boundary-Refs"* — is MET on the SR side.
- **Riders:** SR-126's carve-out narrowed to the ten declared port scripts
  (13u); SR-060's dead `next-wi` clause struck (§6 item 7); four MW
  scrub-or-keep calls made on mechanical evidence, each recorded (SR-067 and
  SR-042 KEPT — their legacy sentinels are still read by live code; SR-131's
  pause window CLOSED); D8 dependencies stated rather than silently retired;
  B03 render rows reframed as REL-002 adopted-toolkit outputs with every
  obligation kept.
- **Status movement:** 58 re-parented `Verified` LLRs flip `Modified`
  (the sanctioned amend-and-flip; `modified` 65 → 102). Nothing self-ratifies
  — `human_ratification_through = 4`, and the whole layer awaits the owner's
  sitting.
- **One test followed the registry:** `test_dogfood_sync`'s planted-defect
  fixture keyed on `[requirement.SR-001]`, a row that no longer exists —
  re-pointed to SR-006. That it was the ONLY casualty across 73 deletions is
  itself evidence the demote set was internal-facing.

Deviation from the design doc, recorded: the design anticipated new LLR mints
where an obligation fit no existing carrier; none were required. The demotions
were applied from three cluster manifests (harness 27 · generators 16 · loop
30), each authored against the WI-444 token bar and machine-checked for
coverage before application.
