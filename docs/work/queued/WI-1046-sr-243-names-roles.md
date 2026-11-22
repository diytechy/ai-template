+++
id = "WI-1046"
title = "SR-243 names the author, critic and REVIEW-A roles, not the models that fill them"
workstream = "docs"
sr_refs = ["SR-243"]
needs = ["WI-1044"]
specref = "docs/archive/work/complete/WI-1037-skill-names-roles-not-models.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-21 from WI-1044's build. SR-243 (Accepted) still
names models where it means roles: its requirement says the coordinator call
capability shall "provide the sole Sol or Terra launch route", and its
acceptance criteria say published guidance "names the coordinator-call route
as the only Sol or Terra launch path". The operator's rule behind WI-1037:
which model fills a role is a setting (`codex_call.py`'s role routes over
the enabled roster).

WI-1044 brings TC-385, which verifies SR-243, to the skill's own phrase,
"author, critic and REVIEW-A". It left SR-243 alone, since amending an
accepted SR was outside its critiqued scope. This row takes the SR to the
same words. The amended text drifts for automated adjudication.

## Done-when

- [ ] SR-243's requirement and acceptance criteria name the coordinator-call
      route as the only launch route for the author, critic and REVIEW-A
      calls, in TC-385's words after WI-1044 (text only; its status
      unchanged). No other cell changes.
- [ ] The Deliverable lists SR-243's drift as the act owed for automated
      adjudication.
