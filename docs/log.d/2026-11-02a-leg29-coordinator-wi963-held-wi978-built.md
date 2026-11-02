## 2026-11-02 — headless leg 29: WI-963 held on OI-119; WI-978 built through its rounds

Loop session `20261102T035202Z-8dc8b4`, leg 29 (coordinator session
`9c217bef-0ddc-40a3-81e0-8fff79680181`). The leg rebased queue row 1 and
filed its hold for the owner. It then claimed row 2 under one scoped
unpause and ran it from the plan through its last review round. It closed
out at 35% occupancy, before row 2's final rebase and self-reservation.
Its decisions are coordinator-2026-11-01 D-008 and D-009, wi-963 D-012 and
wi-978 D-001 to D-012.

- **The settled-amendment filter (WI-963):**
  - It rebased onto `35226d1af` across twenty commits; its six affected
    modules pass and `check-lane` passes.
  - OI-115's Done-when item, now under every lane commit, unbinds the
    single plan's pass record (the digest moved). The plan gate refuses its
    landing and any build commit, and the plan cap is spent.
  - OI-119 is filed with its placeholder WI-989; the recommendation is the
    item in the Trust section.
- **The watermark carrier (WI-978):**
  - Plan: a fresh planner, critique 1 with two MAJORs, one revision, then
    critique 2 APPROVE.
  - Terra's intent set, then a build in four attested stages: tests first,
    deliverable 1, deliverable 2, the text.
  - Round 1 had three MAJORs, all fixed.
  - Round 2 had two MAJORs: one fixed, one re-graded to the plan's
    self-reservation step.
  - Round 3 (convergence) had one MAJOR. Sitting 008 ruled it FIX, and the
    fix was built.
  - The uncounted convergence review after that fix had one MAJOR, which
    sitting 012 ruled DISMISS refuted.
  - No BLOCKER or MAJOR is open.
- **Bars:**
  - trunk smoke at the OI-119 filing: 3301 passed, CPU 489.0 s;
  - at the unpause and the restore: 599.4 s and 616.6 s, over the 540 s
    budget, reported only;
  - every WI-978 stage and fix passed `integrate.py attest`'s review bar;
  - the strict lints were clean;
  - no trunk code changed, so no full suite ran.
- **Recipe lesson:** an owner ruling that adds a Done-when item to a
  claimed single-plan row unbinds its pass record once the lane rebases, so
  such an item goes in the Trust section at the ruling.
