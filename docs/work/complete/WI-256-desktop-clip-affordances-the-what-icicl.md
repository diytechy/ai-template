+++
id = "WI-256"
title = "Desktop clip affordances: the What-icicle (fixed 848px) clips at 1280/1680 - clientWidth 742 vs scrollWidth 867, the TC lane header lands past the visible edge and the scroll hint renders only at 390 (extend the WI-219 scroll-cue idiom to desktop); wide drill layers silently clip at the card edge at 1280 (When-unphased cuts the Docs block mid-label with its right port invisible, How-CMP-004 cuts its rightmost column); polish: two steep When wires terminate on a block edge near a corner instead of the port circle. Render surface: bundle a fresh critique (079-CRITIQUE follow-ups)"
workstream = "dashboard"
sr_refs = ["SR-053", "SR-054"]
buildtier = "quick"
safety_class = "ordinary"
order = 253
+++

## Deliverable

Overflow-driven scroll cues: a .cued class toggled from actual overflow (scrollWidth>clientWidth+1) on every .view/.tablescroll, re-synced on resize/tab switch/ResizeObserver and on drill descend via __syncCues; the revealed cue spans a full-width grid row so the layout never shifts; no-JS media fallback kept; no WI-219 clone (check_dupes clean). Icicle TC lane and the wide drill layers (When-unphased, How-CMP-004) now announced at 1280/1680 both themes. Wire terminals snap to port-circle centers while the first/last control keeps the fanned height (unfanned wires byte-identical; through-box scan 0 across all 5 panels - the snap tightened the endpoint exclusion, detours-off still detects 536). Opus build cd444aa; 111-REVIEW-A APPROVE (mechanism driven correct + race-free for static shots); 080-CRITIQUE APPROVE f=0 - cues and port terminals verified in pixels (6x crops cross-checked against emitted SVG coordinates).
