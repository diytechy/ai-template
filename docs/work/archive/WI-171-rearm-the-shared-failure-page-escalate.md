+++
id = "WI-171"
title = "Rearm the shared-failure page - escalate's top-tier-fail tally spans the whole coordinator run so after two strong-tier CHANGES-REQUESTED rounds every later review round (even a clean APPROVE) pages and schedules a design-check forever; reset the tally when the page dispatches so only NEW top-tier fails re-page"
workstream = "unattended"
needs = ["WI-059"]
buildtier = "medium"
order = 170
+++

## Deliverable

escalate() gained a fails_since index (default 0 keeps the whole-run count for un-updated callers); top_tier_fails now sums strong-tier CHANGES-REQUESTED only over rounds[fails_since:]. The coordinator advances page_fails_since=len(rounds) on EVERY page dispatch (agent_loop.py, before the mode branch), so an already-paged (autonomous: already-ruled) top-tier fail can no longer re-page every subsequent round - only NEW strong-tier fails recorded after the last dispatch reach the shared-failure regime; the last-round tripwire and two-round contradiction windows are untouched. Regression test (two fails page -> boundary advanced -> a later APPROVE does not page -> two FRESH fails re-page) in test_agent_route.py; arch-map re-harvested the new signature. Takes effect on the next coordinator restart (routing referees import at process start), per the 094 fast-path note.
