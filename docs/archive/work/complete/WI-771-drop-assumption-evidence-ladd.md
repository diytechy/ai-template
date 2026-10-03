+++
id = "WI-771"
title = "Drop the assumption evidence ladder: an assumption carries status, standing and a falsifier only"
workstream = "process"
specref = ""
sr_refs = ["SR-200"]
needs = ["WI-770", "WI-775", "WI-776"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

The evidence ladder is gone. An assumption carries status, standing and a
falsifier only (the owner's signed 2026-10-02 ruling, items 1 and 4).

- **Code.**
  - The ladder and everything computing it are deleted.
  - Briefs and the per-need view show status, standing, falsifier and "Can be
    falsified by".
  - The release gate reads standing: a falsified relied-on assumption blocks
    unless an unreopened accepted risk covers it. The reopen triggers are
    unchanged.
  - The step keeps its `assumption-evidence` name, to avoid a contract change.
  - `assumption_refs` and the sampling declarations stay as the falsification
    pointer.
- **Rows retired:** SR-200, LLR-237 and TC-232, with successors SR-201, LLR-238
  and TC-233. Their records are in `docs/log.d/retired/`.
- **Rows amended:**
  - SR-198, SR-199, SR-202, SR-203, SR-206 and SR-218;
  - LLR-240, LLR-243 and LLR-258;
  - TC-235, TC-238 (now also verifying IF-216) and TC-251;
  - TC-234, under a coordinator grant extension.
  - Fix round 1 moved SR-191, SR-192, SR-197, SR-198, SR-201, LLR-238, TC-227 and
    TC-233 to falsification wording: a test case never "evidences" an assumption.
- **Follow-up, not done:** LLR-231 and TC-227's `method` keep the "assumption
  evidence" group name. It is tied to the `assumption_evidence_rows` symbol and a
  rendered label, so renaming it is a contract change.
- **Reviews:** Codex Luna (high) found it NOT YET SOUND at 94ccce56 (SR-198's
  "evidences an assumption") and SOUND at ec3a99ac.

## Context

The owner's signed ruling of 2026-10-02 (recorded in WI-667, "Owner ruling
2026-10-02", items 1 and 4) drops the `assumed | specified | monitored | sampled`
evidence ladder. An assumption carries `status`, `standing` and its `falsifier`
only. Falsification is the one evidence-shaped signal, and a person or
adjudication sets `standing`. Item 4 owes the amendments of the rows built for
the evidence model through the artifact adjudication route.

WI-667 built the ruling's narrowed scope: the composer arms, the release
checklist's assumptions section, and the SN-043, SR-033 and plan C3/C5 edits.
Its Sonnet review (`docs/reviews/2026-10-03-wave8/sonnet-wi667.md`) found the
ladder still alive and outside that grant:

- **Rendered:** the shared assumption renderer prints `_Evidence level now: ..._`
  and `Evidenced by.` in the approval and re-judge briefs. The WI-697 brief
  shows "specified" for DA-011.
- **Computed or gated in code:** `assumption_rules.py`,
  `check_assumption_gate.py`, `trace.py`, `rendering/traj_views.py`,
  `traj_parse.py` and `kitlib/spine.py`.
- **Required by approved rows:** a 2026-10-03 census matched SR-198, SR-199,
  SR-200, SR-202, SR-203, SR-206, SR-218, LLR-232, LLR-237, LLR-240, LLR-243,
  LLR-258, TC-228, TC-232, TC-235, TC-238 and TC-251. Several `coincident` cells
  cite SN-043's removed sentence, "whether a current result evidences it". The
  census was a text match: confirm each row before amending it.

Order: build only after WI-770's combined adjudication sitting has acted. Its
amendments drift the same SR, LLR and TC registries, and an act copying a
registry is refused while any approved row in it has drifted unattested.

## Done-when

- No brief, view or report renders an assumption evidence level. An assumption
  shows its status, standing and falsifier, and the observation cases that can
  falsify it, under a name that does not claim evidence (not "Evidenced by").
- The assumption gate (`[checks] assumption_gate`) no longer requires current
  evidence for an assumption. Its release half reads standing: a falsified
  assumption, unless covered by an accepted risk, blocks. The accepted-risk
  reopen triggers stay (ruling item 2).
- Every approved row that states the ladder is amended or retired through the
  artifact adjudication route, each confirmed against the text first. Ruling R2
  holds.
- A RESYNC_PACK entry tells adopters what changes for their assumption rows and
  gate.
- The commit bar passes.
