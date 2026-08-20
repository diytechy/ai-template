+++
id = "WI-488"
title = "Promote interface contract-test coverage to an ERROR from DevStg-Tests onward, with a migration allowlist seeded at the measured 115 and a declared burn-down expectation (OI-43 ruled (a), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-43"
workstream = "process"
sr_refs = []
needs = ["~WI-469", "~WI-455"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-43's ruling — (a) as recommended. The measured population:
`check_trajectory.py --strict` reports 115 of 125 IF seams cited by no TC
(verified 2026-08-19); the coverage class is deliberately warn-only at every
bar today (`PROCESS_OPTIONS.md` ~:2177-2188, `check_trajectory.py`
~:1014-1017) — this row is the ruled reversal of that posture at one bar.

- **The promotion:** a seam with no citing TC becomes an ERROR when the
  cleared bar is DevStg-Tests or above; below that bar the class stays
  warn-only. This repo is at DevStg-Reqs today, so the promotion bites
  nobody here until the bar rises — which is the point of adopting it now.
- **The allowlist:** seeded with the current 115 seams, each entry a declared
  exemption with the standing never-green-by-list-edit rule in force —
  adding an entry to clear a NEW seam's finding is accepting what it
  measures, and the list carries a declared burn-down expectation rather
  than living as a permanent exemption surface.
- **The prose stays:** `PROCESS.md`'s and `README.md`'s "every interface is
  backed by a contract/fixture test" claim is NOT softened — the promotion
  is what makes it true. (WI-477's docs sweep deliberately does not touch
  this claim.)
- **Sequencing (the soft edges):** the wi455 lane holds the 49
  provenance-held Contract cells and WI-469 re-authors the 27 file-as-
  endpoint Consumes rows — tests written against cells about to be
  re-authored pin the wrong thing, so this lands BEHIND both. Downstream:
  the promotion ships to every adopter at the same bar — RESYNC entry owed.
