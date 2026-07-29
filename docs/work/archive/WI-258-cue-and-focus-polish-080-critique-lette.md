+++
id = "WI-258"
title = "Cue and focus polish (080-CRITIQUE letter-passing): mark the clip edge itself (gradient/shadow) so desktop truncation is discoverable at the point of cut, not only via the caption cue above the card; verify the keyboard-focus outline colour is distinct from the active-you-are-here legend accent (a captured tooling drill showed a near-match while the header reported 0 active - one-line source check). Render surface: bundle a fresh critique"
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "quick"
safety_class = "ordinary"
order = 255
+++

## Deliverable

Cue/focus polish (gen_trajectory.py): the clip edge is marked with an overflow-gated right-edge mask fade (.clipr toggled from the same scrollWidth>clientWidth signal as the WI-256 cue, cleared at scroll-end so the rightmost content reveals); the drill focus/highlight ring recolored from #b45309 (byte-identical to the active you-are-here accent) to var(--accent) (#4f46e5 light / #818cf8 dark), distinct in both themes. Byte-stable, 2 biting tests. Adversarial REVIEW-A APPROVE f=0.
