+++
id = "WI-380"
title = "DESIGN DRAFT (docs/concurrency-v2.md §3) - do not claim until that doc is settled. Split ratified content from traced content in the post-attestation amendment detector. check_trajectory.staged_spine_findings currently compares EVERY column except Status, so Module, CodeSymbol, TestRefs, Component and Phase arm the re-attest warn exactly as if the requirement prose had changed. Owner ruling 2026-07-31: only what is RATIFIED matters - scope, defined by the prose and the relevant field attributes; traceability is TRACED, not ratified, and must not count as a spine touch. Driven cost of getting this wrong: WI-280's 19 LLR Module pointers followed code that moved, forcing 11 owning SRs to Modified, dropping the gate G3->G2, and buying a ratify brief plus four review rounds for a change that altered no requirement. Lands first regardless of how the rest of the design resolves: it is small, already ruled, and removes most of the pain WI-381/382 are designed around. Open: the exact per-registry cell split, including the arguable SN-Refs and Verifies cells."
workstream = "scripts"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "ordinary"
+++
