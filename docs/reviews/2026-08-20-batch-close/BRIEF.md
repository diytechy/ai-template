# Adversarial review brief — the 2026-08-20 batch

You are an ADVERSARIAL reviewer of one day's work in c:\Projects\ai-template
(a meta-repo whose product is the process kit under project-trajectory/).
Your job is to find what is WRONG, OVERCLAIMED, or SILENTLY BROKEN — not to
summarize. Every finding needs file:line evidence and a concrete failure
scenario; rank by severity. The repo's dominant historical defect class is
FLUENT FALSE SIGNED CLAIMS and GUARDS THAT CANNOT FAIL — hunt those first.

THE RANGE: git commits 28466711..HEAD on this branch (~24 commits, one
day): (1) a repository-review triage that minted WIs and OIs; (2) five
owner rulings executed; (3) THE SPINE SIGNING — 243 status flips + the 11
frame rows + the first baseline seed (docs/archive/last_approved/), sitting
3 closed; (4) D-9 steps 7+8 — the Modified status retired, the enum closed
at {Drafted, Approved, Founded}, two snapshot rules armed as integrity
ERRORs; (5) sixteen work items ground in series (WI-474..482, 485, 486,
489, 465, 466, 452, 470, 477, 479 — seams, launchers, lint, goldens,
pytest 9, perf budgets, the OI-41 deferral arms, the Implements harvester +
coverage scanner, the derived-label migration, the docs-contract sweep, the
dashboard title defense); (6) the per-WI record in
docs/log.d/2026-08-20-frontier-grind.md and the day's Decisions entries in
docs/log.md.

PRIORITY TARGETS (where wrongness costs most):
1. THE SIGNING ITSELF: were the flips complete and honest (grep for any
   surviving Drafted/Modified in the four spine files + external.toml)?
   Does the seeded snapshot ACTUALLY match live byte-for-byte? Was anything
   blessed that changed after the seed in the same commit? Is the Sittings
   row / Decisions record accurate about what was signed?
2. STEP 7/8: is `Modified` really gone from every live predicate/reader
   (not just the ones the worker listed)? Do the newly-armed integrity
   rules actually FAIL when violated (plant a violation mentally — trace
   the code path)? Did any read-side tolerance get deleted that a
   downstream repo mid-migration still needs?
3. THE GRIND CLOSES: pick at least four WI Deliverable claims at random
   and verify them against the tree — do the tests they cite exist and
   assert what the claim says? Any claim of "verified/green/measured"
   without the artifact to back it?
4. THE NEW MECHANISMS: the OI-41 arms (can the vacuity check be silenced
   without retiring an entry? can ARM 1's grammar be satisfied
   vacuously?), the backlink scanner (does its 1/161 number reproduce?),
   the title advisory, the status-vocabulary contract test (does it
   actually red on a planted retired word?).
5. CROSS-CUTTING: the day introduced ~30 new tests — any that cannot fail?
   Ratchet re-stamps — any that quietly RAISED a bound without reason? The
   orchestrator's own recorded mistakes (the golden gap, the R-D token,
   the R-F specrefs, piped exit codes) — is each fix real and is the
   class closed or just the instance?
DELIBERATELY OUT OF SCOPE: the 19 orphans (declared decomposition debt),
the unwired perf-metrics emitter, the remaining queued programs
(WI-448/455/469/473/483/484/487/488/390/467), docs/log.md history, and
OWNER_SCRATCHPAD.md (never read it).

Also read docs/log.d/2026-08-20-frontier-grind.md's "Adjacent findings"
section — CONFIRM or REFUTE each banked finding while you are in there.

FORMAT: numbered findings, each with severity (CRITICAL/MAJOR/MINOR),
file:line evidence, the failure scenario, and a one-line suggested fix.
End with: the three claims you tried hardest to refute and could not.
