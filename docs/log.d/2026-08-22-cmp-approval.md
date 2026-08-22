## 2026-08-22 — The component registry approves; the ladder lifts to LLReqs

Deferred open items: none — an approval act executing the owner's written
ruling ("looks good, approve", the four CMP rows shown in full first).

The four `Drafted` component rows — the last unapproved registry —
flipped `Drafted → Approved` in one act (status cells only, no text
moved), the approval baseline re-seeded through `intake.py snapshot`
(7 files; the integrity check's approval-record arm REFUSED the bare flip
first and named exactly the four rows, then read clean after the seed —
the machinery confirming scope, as at both prior approval acts).

**The stage moved `DevStg-Arch → DevStg-LLReqs`, not Impl** — and that is
the derivation being honest: the frame is settled (boundary + components
approved), but the nine undecomposed SRs (the declared orphans debt, 15
orphan findings on the trace surface) hold the repo at the low-level-
requirements rung. The earlier expectation that approval would read Impl
was wrong about the spine's coverage, not about the mechanism. At the new
rung **no additional check newly selects** (the LLReqs plan is the same
ten-step floor; the Impl product checks stay above), so the gate reads
fully green: `check.py --jobs 0` RESULT PASS after the seed.

One test-data consequence, fixed in the same commit:
`test_baseline_snapshot._approved_offspine` seeded its CMP fixture by
flipping a live `Drafted` row that no longer exists — its own
anti-vacuity guard fired, and the helper now flips only where a
non-claiming row remains (the closing `assert claiming` keeps the teeth;
docstring records the 2026-08-22 premise change).

Commit bar: smoke 1344 passed / 29 skipped in 73.21 s (posix-gated
shell); test_baseline_snapshot 41 passed; check_docs --stale 0 broken;
check_trajectory --strict exit 0; registry-integrity PASS post-seed.
