+++
wi = "WI-451"
branch = "wi451-sr-retier-campaign"
claimed_outcome = "partial"
reason = "Closed PARTIAL on an owner ruling in session, 2026-08-15: a partially completed re-tier is within the design expectation, and modifying attested rows is the point of the exercise rather than an obstacle to it. The SR layer was rebuilt against the locked six-crossing frame and the spine closes clean; what remains is judgement, not mechanism."
commit_range = "8d2dfc6a9b..d2226ccf79"
suggested_tier = "medium"
keep_commits = ["d2226ccf7986a2926897da66f88aadf90b0f3fac", "75c096de5e42f1ee5b18cdd965655d9a3e58fafb", "f49b713995374182e65a9004d7ecb356ede07332", "9861e9572a913e45fd7f83466c347cd35829564a", "4ae9f351268280f875234ba69b1c11fdf35cddac", "e6cdc8fd67ff3604b7e733fda531ffcef48d9ed8", "0d5a9432f839f6f962b0acabd8cf0dd9ff262d95", "a787e74b56f68f80e56c7734300d11a14adfe934", "fd26a96698712d193405d5f2ce3a43f047e0ab02", "ad0d045682de64ee27d061bb3fc7c7133ff1d25a", "5a214b2b9dc5a31b9657012719fa1b99849b8243"]
discard_commits = []
split_decided_by = "lane"
+++

## What happened

Lane `wi451-sr-retier-campaign` closed `WI-451` as **partial**: Closed PARTIAL on an owner ruling in session, 2026-08-15: a partially completed re-tier is within the design expectation, and modifying attested rows is the point of the exercise rather than an obstacle to it. The SR layer was rebuilt against the locked six-crossing frame and the spine closes clean; what remains is judgement, not mechanism.

The work so far is in trunk, not on a branch — the lane merges like any
other. Read it with `git log --oneline 8d2dfc6a9b..d2226ccf79` / `git diff 8d2dfc6a9b..d2226ccf79`.

## Delivered

The system-requirements tier went **149 -> 64 rows** across seven acts:

1. **26 supersession tombstones deleted** per D-4 (`2026-08-14b`), with the
   `SupersededBy` column, their validator, 2 test cases and 6 pinning tests.
   One log entry carries the forwarding map.
2. **The SR layer decided and reattached** - 34 held, 14 re-stated, SR-141
   merged into SR-148, 15 minted (SR-151...SR-165), `Boundary-Refs` populated
   on all 64.
3. **73 rows demoted to the design tier**, and the finding worth keeping is
   that **zero new design rows were needed** - every obligation fit an
   existing carrier, which confirms the census's "these were always LLRs"
   claim mechanically rather than by assertion.
4. **Adversarial round 1** returned CHANGES-REQUESTED with 5 MAJOR findings;
   all were confirmed and all fixed. Its named cause - a smoke-only bar - is
   recorded with it.
5. **`Area` retired for the closed `Aspect` vocabulary** (owner ruling
   `2026-08-14h`), derivable values dropped rather than remapped: 21 of 64
   rows carry an aspect, 42 carry none by design. Adopters carry a
   RESYNC_PACK entry.
6. **A re-iteration pass** closed two owed calls (SR-043's MW clause KEPT on
   driven evidence; the child/parent phase spread RECORDED AS INTENDED with
   the analysis), finished the Aspect conversion in the shipped docs, and ran
   an independent top-down read.
7. **The top-down read's mechanical half closed** - 19 cells across 12 rows.

Measured at close: `SN=27 SR=64 LLR=153 TC=148`, `orphans=0 integrity=0
component-findings=0 interface-findings=0 form-findings=2` (two recorded
waivers, SR-140 and SR-147). The lane also re-pointed **62 of 115 interface
rows' `sr_refs`**, so the IF registry already tracks the new SR layer with
zero dangling pointers.

## Not delivered

**Five findings from the top-down read remain UNRULED.** None is mechanical;
each needs an owner call on its substance. Full detail in the lane ledger at
`docs/plans/2026-08-14-wi451-slice2-ledger.md` lines 330-334.

| # | Finding | Interface rows it would move |
|---|---|---|
| H1 | The frame's own named B-05 observable - "the package exists, is complete and consumable", the MAPPING manifest - has NO row. 15 were minted and the one the frame spelled out was not. | none |
| H4 | SR-148 / SR-153 / SR-059 all state (SN-025, loop work-selection) - the same class as the SR-141 merge already performed. | **6** (IF-053/054/071/085/088/089, via SR-153) |
| H5 | SR-031 and SR-137 both claim the tomllib-vs-sh observable and have already DIVERGED - only SR-031 names the fail-OPEN decoy. | **2** (IF-032, IF-037) |
| M1 | Four rows escaped demotion against the campaign's own criterion - SR-008, SR-021, SR-030, SR-133 (SR-133's rationale literally reads "Decomposed from SR-006"). **SR-008 and SR-133 are `Verified`**; the owner ruled 2026-08-15 that overriding a historical attest is fine where it improves the design, so this is no longer an obstacle - but the demotion calls themselves are still owed. | **3** (IF-013, IF-022 via SR-008; IF-015 via SR-030) |
| M3 | Three needs have zero textual coverage despite `orphans=0` - SN-026's consent surface, SN-037's discrete/variable signal typing, SN-029's delegated-approval record. | none |

**Two crossing attributions were revised in act 7 and are flagged for
overrule** - nothing mechanical can catch a wrong answer here, because the
checker verifies that a crossing RESOLVES, never that it is the right one:
`SR-137` `["B-01","B-02"]` -> `["B-01","B-04"]`, and `SR-139` `["B-02"]` ->
`["B-02","B-05"]`.

**Also outstanding:**

- **SR-165 needs a design row and a test case** before it can leave `Draft`;
  its verification flipped Inspection -> Test in act 7, deliberately.
- **The second top-down read** the method names - one has run in each
  direction and closed the orphan set; a second read of the 64-row layer
  against the six crossings, now that the layer exists to read, was named in
  the ledger as the honest remaining check.
- **Adversarial round 2** is owed on the settled state. Round 1 is spent
  because the fixes postdate its verdict, and the campaign's own sequencing
  note says a round is spent by the next commit - so it belongs AFTER this
  merge, not before it.
- **Sequencing that a successor must not get wrong:** rule the five findings
  BEFORE any interface-registry work. The re-tier moves IF rows (11 more, per
  the table above); the ruled interface model moves no SR ids at all, since
  its owner cell lands on the IF row. Reversed, those 11 rows are re-pointed
  twice.

## Keep / discard

- **keep**: d2226ccf7986a2926897da66f88aadf90b0f3fac, 75c096de5e42f1ee5b18cdd965655d9a3e58fafb, f49b713995374182e65a9004d7ecb356ede07332, 9861e9572a913e45fd7f83466c347cd35829564a, 4ae9f351268280f875234ba69b1c11fdf35cddac, e6cdc8fd67ff3604b7e733fda531ffcef48d9ed8, 0d5a9432f839f6f962b0acabd8cf0dd9ff262d95, a787e74b56f68f80e56c7734300d11a14adfe934, fd26a96698712d193405d5f2ce3a43f047e0ab02, ad0d045682de64ee27d061bb3fc7c7133ff1d25a, 5a214b2b9dc5a31b9657012719fa1b99849b8243
- **discard**: (none)
- **decided by**: lane
