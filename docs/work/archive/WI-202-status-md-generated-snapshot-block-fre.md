+++
id = "WI-202"
title = "status.md generated-snapshot block + freshness gate - splice a BEGIN/END GENERATED block into docs/status.md carrying derived facts (spine+gate from trace.py/derive_gate.py; open-items projected from open-items.md) behind a new generator + its --check freshness step; the WI-200 mode-aware guard flips to freshness and the S-3 named-in-both presence lint retires"
workstream = "scripts"
needs = ["WI-200"]
buildtier = "medium"
order = 201
+++

## Deliverable

WI-202 (2026-07-17): gen_trajectory.py gains a --status mode that splices a <!-- BEGIN GENERATED STATUS --> block into docs/status.md carrying ONLY derived facts - the spine + derived gate (PROJECTED from docs/gate's freshness-guarded `# basis:` line, never recomputed) and the open-items one-liners (projected from open-items.md's ## OI-N sections). Its --status --check byte-compares like arch-map/trajectory-map, wired as the check.py `status-map` G3 step + the pre-commit --run-steps floor, so a registry/open-items/gate edit that stales the block blocks at commit. The WI-200 forward-only token guard stands down under the marker (already coded) and this freshness step is the successor invariant; check_docs S-3 OI-coherence goes mode-aware - it retires under the marker (a projected list cannot disagree with its source) while S-1/S-2 stay. Per-OI projection contract pinned in docs/specs/open-items-surface.md (explicit `- **One-line:**` field, else first Recommendation sentence; soft-wraps joined; volatile git-state never baked). meta status.md restructured behind the markers + One-line fields added to open-items.md. 9 gen_trajectory --status tests + 1 check_docs S-3-retires test. No new spine requirement (tooling + enforcement, the WI Non-goals); block-splice emit is the generated-block idiom (no new seam). Code map regenerated.
