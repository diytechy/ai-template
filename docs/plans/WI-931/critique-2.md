Reviewed: 7a4e14ce85bd2d2ef5a1b3de84ec0cb9c1e7d3de

## WI-931 — independent plan critique 2

Fresh non-author session: this invocation of Codex as the independent plan critic; it did not produce the plan. Coordinator-assigned sitting/review record: `2026-10-17-coord/wi-931/plan/crit2/WI-931-plan-critique-2.md`. No provider session id was supplied. Second and final critique, convergence stance. The launcher records this verdict; no staging or commit was performed.

Rubric: `docs/rubrics/plan-decomposition.md` at `7a4e14ce85bd2d2ef5a1b3de84ec0cb9c1e7d3de`, matching the supplied rubric. Intent sources at that revision: the full `docs/work/active/wi-931/WI-931-session-kill-guards-removed.md`; its specref `docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`; SN-006 in `docs/requirements/stakeholder-needs.toml`; SR-238 and the retained SR-026 in `docs/requirements/system-requirements.toml`. IF-064 was checked in `docs/requirements/interfaces.toml`. Artifact produced for inspection by `git show 7a4e14ce85bd2d2ef5a1b3de84ec0cb9c1e7d3de:docs/plans/WI-931/plan.md`; the full text was inspected directly, without a proxy. The supplied coverage arithmetic was accepted. No excluded critique, decision, review, session log or status file was opened; the plan's own claims about earlier review or owner rulings were not treated as independent authority.

Rubric derivation check: SN-006 requires bounded unattended operation and clear failure reporting; SR-238 makes ending the supervised process tree before continuation the relevant outcome. The WI explicitly narrows the two timing windows while retaining the ordinary kill and stop-on-unended-tree behavior. DevStg-Tests and B2 independently require honest coverage of these obligations through the WI's Done-when, rather than merely accepting permissive tests. DevStg-Reqs, DevStg-Impl, G4 and B1–B4 assess whether that coverage can actually be built. The rubric is adequate for this plan review; no missing numbered anchor is required.

Anchor coverage and judgment:

- DevStg-Reqs: P0–P8 identify concrete deliverables and checkable completion conditions. The code removals, handler census, spine amendments and evidence work are bounded steps.
- DevStg-Tests: D1–D16 have substantive coverage. P0 and P7 require Windows and Linux evidence at base and tip; P8 compares the four records, expected platform skips and unchanged kept bodies, and prevents completion on mismatch. P3 supplies D2's red/green assertion; P4 supplies D13's census and re-check; P5 requires the checkpoint acts; P6 supplies the resync entry; P7 requires the smoke bar and REVIEW-A. This judges the proposed evidence route, not whether future runs have already passed.
- DevStg-Impl: the plan explicitly separates repeated coverage into symbol/test removal versus spine prose, before versus after execution versus completion comparison, and assertion implementation versus platform verification. These are distinct artifacts rather than duplicate implementations.
- G4 and B4: build order preserves the spec's late-spawn/PID-check-first sequence on shared code and registry cells. The census consumes P3's changed exception path; spine review consumes the removals and census; final evidence consumes the completed implementation and amendments; P8 consumes both evidence legs. No missing dependency prevents the stated order from being built.
- B1: the plan uses existing IF-064 and private intra-module behavior; it proposes no duplicate seam. Retaining IF-064 is justified by its unchanged named surface while the exception contract receives explicit census and adopter guidance.
- B2: the cited clauses correspond to deliverables, checks or recorded acts. The table's apparent multi-coverage is explained in the plan, and no hollow citation leaves a Done-when obligation unserved.
- B3: P8 has an independently checkable deliverable: reconciliation of the four evidence records with the landing tree and kept test bodies. It adds a completion decision beyond P0/P7's executions. The other rows likewise own distinct outputs.

Architectural delta: `DELTA: none` is correct under the specified four triggers. Removing a job state and restoring an existing error's OSError inheritance adds no state, domain value, input dependency or boundary. The changed behavior on the existing error seam is nevertheless carried by P3's assertion, P4's handler census and P6's adopter guidance.

Transfer caveat: the protocol's debate/selection evidence comes from QA, math and code with objective verifiers; plan-artifact quality and two-planner reconciliation remain an open research gap. This rubric is an extrapolation, not a proven instrument.

VERDICT: APPROVE findings=0
