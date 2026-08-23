+++
id = "WI-286"
title = "Worker/integrator worktrees run the ambient interpreter not the venv - the dispatcher's train worktrees have no .venv and resolve whatever Python is on PATH (run 20260723T0202 inherited 3.8, below the 3.11 floor), so a floor-violating idiom passes locally and the pinned dev tools may be absent; point worktree sessions at a >=3.11 pinned interpreter (share the root .venv by absolute path) + preflight the floor. Sibling of WI-274; compounds WI-285"
workstream = "scripts"
needs = ["~WI-274"]
buildtier = "medium"
safety_class = "ordinary"
order = 283
+++

## Deliverable

Integrated from train p0-g3-WI-286-9253 @ d4c3833: build: WI-286 rework — fail closed on a missing root .venv (REVIEW-A MAJOR)
