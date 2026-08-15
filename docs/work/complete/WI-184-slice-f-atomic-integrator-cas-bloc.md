+++
id = "WI-184"
title = "Slice F - atomic integrator + CAS + blocked-disposition"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["WI-180", "WI-182"]
buildtier = "strong"
order = 183
+++

## Deliverable

Slice F (2026-07-16): the atomic serialized integrator wired into the dispatch loop. One logical writer against refs/heads/llm/integration (CAS-only, never checked out in the primary worktree); per-train staging branches llm/integrate/<tid> in their own worktrees compose from the CURRENT integration HEAD; reservation scope + EXACT-HEAD review verdicts verified (train_verdicts parses reviews/<train>/NNN-<PHASE>-<sha7>.md off the branch; a stale-named verdict = rework, proven); clean 3-way apply = fast path no re-review, ANY textual conflict parks needs-re-review (never a silent pick, proven with a shared-path collision); WI rows -> done with derived Deliverables (surgical row rewrite, no registry reflow) + log evidence + generated status snapshot (marker-gated: hand-authored status untouched until migration - SR-059's generation half now exists) + iteration-index regen on the composed tree; combined bar = declared stack.ini test command, ALWAYS runs, red bar blocks with the ref untouched (proven); ONE integration commit with Integrated-WI/Train-Head trailers; stale CAS fails harmlessly and recomposes. Blocked disposition: smaller transaction (only its WI blocked + BlockRef + trailers + CAS, reservation released only after; proven only-its-WI). Publication: durable refs/llm/publish-intent (target+old+ref JSON commit) before the dev-ref CAS; verified reset-sync (index+tracked tree exactly at expected-old; untracked untouched); dirty checkout defers untouched + reported; crash-between-CAS-and-sync recovers idempotently (proven); intent deleted only after sync. Integration ref = authoritative frontier source (registry_rows_at) + new-train base; multi-wave runs complete in one launch (fork/join E tests now end-to-end). Deviations: partial-train re-review after mid-train blocker -> G/H; conflict RESOLUTION loop (vs parking) -> later rung; full/gate-bar differentiation at closes -> H. tests/test_agent_loop_integrate.py (9 fixtures) + D/E suites upgraded to integrated semantics (48 green). SR-063/LLR-064/TC-064 Verified (autonomous single-agent adversarial review).
