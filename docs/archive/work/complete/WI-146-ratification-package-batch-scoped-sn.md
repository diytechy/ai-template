+++
id = "WI-146"
title = "Ratification package - batch-scoped SN->SR->LLR/TC tree + brief link check"
workstream = "scripts"
needs = ["~WI-130", "~WI-093", "WI-145"]
order = 145
+++

## Deliverable

Owner-intake 2026-07-14 #hierarchy-view. (a) trace.py --ratify SCOPE (a phase tag or SR-id list) emits the batch-scoped SN->SR->LLR/TC hierarchy WITH prose (SR Requirement/AC, LLR Detail+Module/Component, TC Method/Expected, any docs/rubrics/*.md cited) to stdout or --out FILE, reusing the loaded/filtered working sets - a generator mode that runs no checks (exit 0). (b) check_trajectory.ratify_brief_findings: warn-first (never a gate fail) lint that an `## OI-N` open-items.md section whose decision names a `[phase]-[g1|g2]` anchor + ratification language links the view (a `trace.py --ratify` cmd token or a ratif/hierarch link) - vacuous without such a brief; silent on the live repo (the only [v3]-[g2] token is intro prose, outside any OI section). (c) gate-advance SKILL 'Carry the hierarchy view' step + the redacted REVIEWER_PROMPT names the view a REQUIRED input for a G1/G2 ratification diff. (d) gate-advance G2->G3 recipe line: a [g2] batch also authors/updates the IF-### rows its LLRs imply (PROCESS.md 8). Skills re-synced byte-identical (.claude/.agents). Tests: 3 in test_trace.py (SR-list prose, phase+rubric+empty, --out) + 4 in test_trajectory.py (unlinked warns, cmd/link silent, vacuous). No spine change.
