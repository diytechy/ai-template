+++
id = "WI-373"
title = "Skepticism in the review protocol runs one direction: the reviewer charter treats the implementation report as claims to re-run, but nothing charters a finding's OWNER to confirm-or-refute before acting - the measured failure mode of the review-round era (127-131: ~70% of findings were claims/hollow-guards/bookkeeping; re-review rounds aimed 100% at prior fixes and converged to zero real findings while manufacturing work), and the same one-way trust let parked work be scrubbed by sessions that never read the record justifying it, with no sanctioned shape for costly-but-right rework (owner directive 2026-07-30). Documentation-only, three homes stated once each: PROCESS_OPTIONS.md verdict protocol gains the finding lifecycle (a finding names a falsifiable failure scenario; its owner CONFIRMS by reproducing or REFUTES it before changing code, refutation a legitimate recorded outcome feeding the reviewer's confirmed-finding rate; a re-review round verifies fixes landed, never hunts fresh findings in them - fresh hunts aim at product surfaces); AGENTS.template.md working agreement gains the reversal-evidence bar (deleting/reverting takes the same evidence as creating - read the record that justified the thing first) and the symmetric sunk-cost failure (sunk-cost KEEPING/moth-balling: a wrong design escalates as a written case to a design-change item, never parks unrecorded, never silently reverts), paid inside the 10,000-byte budget; docs/enforcement-audit.md records the honest tiers. NO new checks or scripts (the 2026-07-28 audit's enforcement-layer-growth warning applies); score_reviews feed-or-delete stays an owner call, out of scope."
workstream = "process"
specref = ""
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-30. PROCESS_OPTIONS' LLM-gate verdict protocol carries the
finding lifecycle — a finding names a falsifiable failure scenario; its
owner confirms it by reproducing that scenario or refutes it before code
changes, a refutation recorded in the round record and charged to the
reviewer's confirmed-finding rate, never the owner's standing; a re-review
round verifies fixes landed, never hunts fresh findings in them; the
mid-build design-escalation case (what was found / why the shape can't
reach the requirement / both paths' costs) closes the paragraph, and the
reviewer-independence bullet routes per-WI rounds through the lifecycle.
AGENTS.template's working agreement carries the three clauses austerely —
finding-is-a-claim as a *pointer* to the lifecycle (round-1 finding 3: the
first cut restated it — one fact, one home), undo-takes-evidence in the
repo-text-is-memory bullet, wrong-design-escalates in the (now
"shipping, keeping, or blind retries") sunk-cost bullet — paid inside the
10,000-byte budget (9,975 → 9,991, size test green) per the file's own
Customizing rule. Enforcement audit: three new Working-agreement rows
(Reviewer+Prose / Prose / Prose), finding 3 amended, and the
score_reviews backstop row states the scoreboard has been dark since
2026-07-15 (round-1 finding 5). PROCESS_OPTIONS 161,117 → 162,601
(+1,484 flagged; baseline re-stamped in all three skill copies). Round 1
also caught a `git add -A` sweeping an uncommitted OWNER_SCRATCHPAD.md
hunk into the build commit — recut excluding it, the owner's edits left
on disk unread (finding 2). All five round-1 findings CONFIRMED on
reproduction, none refuted — the lifecycle's first dogfooding, recorded
in the log entry.
