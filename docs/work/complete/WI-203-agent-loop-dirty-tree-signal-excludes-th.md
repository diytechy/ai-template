+++
id = "WI-203"
title = "agent_loop dirty-tree signal excludes the owner-only scratchpad - a perpetually-edited tracked OWNER_SCRATCHPAD.md keeps working_tree_dirty non-empty so the WI-076 reconcile note fires on every resume (and can read a done tree as not-done); exempt the FB3 owner-only path (shared with check_docs) at both the note trigger and the done guard so the interrupted-residue signal only fires on genuine residue"
workstream = "unattended"
needs = ["WI-076"]
buildtier = "quick"
order = 202
+++

## Deliverable

WI-203 (2026-07-17): agent_loop.substantive_working_tree_dirty(root) drops the FB3 owner-only path (OWNER_ONLY_PATHS=OWNER_SCRATCHPAD.md, mirrored from check_docs.SCRATCHPAD - NOT imported, to avoid a CMP-004->CMP-001 edge + IF seam for one fixed filename) from the dirty-tree signal at BOTH callers: the WI-076 resume-note trigger (start_dirty) and the worker done-detection guard (worker_endstate). A tree whose only change is the perpetually-edited scratchpad now reads clean, so the interrupted-residue note fires only on genuine residue and an owner-only-dirty tree is not read as not-done; the raw working_tree_dirty primitive stays honest. 3 tests (substantive-drop unit + resume-note-injects-nothing + done-stays-done, contrasting the still-deferring scratch.txt case). No spine change (coordinator behavior refinement, the WI-076 precedent), intra-module, no new seam. Code map regenerated.
