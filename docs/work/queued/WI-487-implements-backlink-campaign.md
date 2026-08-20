+++
id = "WI-487"
title = "The back-link campaign: write the Implements: tags across the declared source surface with a code-review pass, raise the coverage dial to a bar the tree clears, and answer decay (OI-42 ruled, 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-42"
workstream = "process"
sr_refs = []
needs = ["WI-486"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes the campaign half of OI-42's ruling, under the owner direction that
coverage is low BECAUSE THE TAGS ARE MISSING, so the remedy is to write them
— not to lower the bar. Hard-blocked on WI-486: the tightened harvester and
the report-only scanner are this campaign's instrument and progress bar.

- **The population:** 781 public symbols measured 2026-08-18 (the row's own
  AST method); reverse coverage starts at 1 of 161 live LLRs. Target: 50%,
  recorded on the ruling. Each tag lands with a CODE-REVIEW pass so it names
  the requirement the symbol genuinely fulfils — a wrong back-link is worse
  than none, because the column reads as evidence.
- **The dial rises AFTER the tags land:** the scanner's threshold moves from
  `0`/off to a value the tree already clears — the number goes up because
  the tags landed, never because the bar came down.
- **The decay answer is owed at close, not skipped:** the row's measured
  hazard is decay, not initial effort (WI-425's own hand repair went stale in
  three days; `adjudicate_brief.py` was born citing retired ids). At close,
  RE-CONSIDER option (c) — the OFT-style revisioned marker, the one surveyed
  mechanism that converts silent decay into loud failure — and record the
  recommendation either way; the ruling reversed the premise that refused it.
- **Rides along:** `dispatch.py:310`'s dangling SR-141 citation (merged into
  SR-148) — the one non-historical dangling id the row's census found.

Tags are source comments/docstrings — no spine cell moves; `ordinary` class.
Priority 2: deliberately after WI-486 lands and the scanner's first honest
number is on record.
