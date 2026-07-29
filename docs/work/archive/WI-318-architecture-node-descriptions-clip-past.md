+++
id = "WI-318"
title = "Architecture node descriptions clip past their box on every width (T4, 121-CRITIQUE MAJOR) - in the What/Architecture decomposition each visible SN block draws its description as a single unwrapped line that begins outside the left edge of the node and runs past the right edge, so the text is unreadable AS a label and also breaks the box it belongs to. Reported at 390px (390px-light-arch-full.png, SN-001..SN-009) and still present at desktop width (1680px-light-arch-full.png, 1680px-dark-arch-full.png), so this is not a narrow-viewport reflow issue that WI-307's scale-to-fit covers - the string is simply longer than any box it is drawn in. Fix by WRAPPING within the node, sizing the node to its content, or emitting a deliberately budgeted summary that fits (the _drill_block_label wrap idiom WI-246 built for CMP blocks is the existing shape). Bind by widening the T4 label-legibility owner rather than filing a new anchor: no character of a node label may render outside its own rect, checked against the emitted geometry, not by eye. RE-AFFIRMED against the amended SR-054 (2026-07-26, WI-321's prompt): the amendment removed the row's restatement of which critique anchors are live, moving that to the rubric alone. The requirement text this finding is judged against is unchanged, and the rubric still carries the anchor, so the finding stands as scoped."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "medium"
priority = 1
safety_class = "ordinary"
order = 315
+++

## Deliverable

The shared drill label emitter FITS a sub-label to the column it is drawn in (_fit_lines: a second line broken on a word, then an ellipsis; three text lines the ceiling, the grid the id/name wrap idiom already proved fits row_h) - so the 15 arch-root SN blocks whose whole need ran outside their box now read inside it, and a sub that already fits renders byte-identically. Bound as the T4 GEOMETRIC FLOOR in LLR-119/TC-124: every label line of every drill block measured against its own rect on both axes, swept over the emitted document, proven to bite on the pre-fix emitter. T4 stays a live critique anchor for its truncated-WITHOUT-AFFORDANCE clause; the rubric now says which half is a test.
