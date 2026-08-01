+++
id = "WI-273"
title = "Dashboard semantic tabs — expose selected tab/panel state and keyboard navigation through the ARIA tabs pattern"
workstream = "dashboard"
sr_refs = ["SR-052"]
needs = ["~WI-272"]
buildtier = "medium"
safety_class = "ordinary"
order = 270
+++

## Deliverable

Dashboard tabs are a real WAI-ARIA tablist (role=tab/tabpanel, aria-selected/aria-controls, roving tabindex, arrow/Home/End controller) — integrated 2026-07-25 by merging stage/WI-273 after the owner attested its SR-084 dispatch. The code was proven sound before the merge: REVIEW-A (OPENAI-TERRA, non-Anthropic) drove a live keyboard probe through click / Left-Right wraparound / Up-Down / Home-End / Space / Enter with exactly one selected tab, one visible panel and one tabindex=0 at every transition. Its CRITIQUE's two CHANGES-REQUESTED findings (A2, A4-boundaries) were pre-existing whole-document items this train never touched, and both were separately ruled and closed (A2 -> LLR-101/TC-104; A4-boundaries retired as not-a-defect 2026-07-24). Two mechanical merge conflicts resolved by the documented conventions: PROJECT_STATE.html regenerated from the integrated tree, and the module-size ratchet re-stamped to the ACTUAL integrated count (4791) keeping both rationale chains — the WI-289 re-stamp-off-own-base class, hit twice here (train stamped 4573, compose 4660).
