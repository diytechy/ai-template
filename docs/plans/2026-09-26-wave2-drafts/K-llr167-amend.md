+++
id = "WI-@K@"
title = "Amend LLR-167 to the hold its code and test pin, and correct the routing prose that lags"
workstream = "requirements"
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-146"]
needs = ["WI-645", "WI-646"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

Found by WI-645's build, which re-drafted TC-161 to what its tests drive:

- LLR-167's approved `detail` says "A refusal falls back to the worker
  assignment and PRINTS why." The code holds instead:
  `agent_loop.route_session` returns `EXIT_NEEDS_HUMAN`, `session_body` says a
  declared brief that cannot be composed is a hold, not a fallback, and
  `test_an_unfillable_declared_brief_HOLDS_rather_than_dispatching_a_builder`
  pins it. The sentence survived the WI-603 amendment and its verdict. TC-161
  now says "held", so the two rows disagree until LLR-167 is amended.
- The same `detail` names `dispatch.red_tc_census` and `dispatch.parse_red_tc`;
  the code calls `census.red_tc_census` and `census.parse_red_tc`.
- Stale prose (non-spine): the comment above `adjudicate_brief._ASSEMBLERS`
  ("a key absent here is documented in this module's header"); `compose`'s
  "has no evidence assembler" branch, unreachable now that the routed set
  equals the shipped set; `agent_loop.session_body`'s paragraph saying an
  adjudication row whose evidence could not be assembled builds from the
  worker assignment; `tests/test_agent_loop_worker.py`'s module docstring
  (legacy `--track` "still runs", and SR-060 where TC-061 verifies SR-026);
  and `test_the_review_scorer_cannot_serve_this_grammar`'s count of "four"
  grammars where there are five.
- LLR-167's four original `code_symbol` entries carry no `Implements:`
  back-link.

IN SCOPE: draft the LLR-167 `detail` amendment (hold, not fall back; the
census module); correct the stale prose and
decide whether the unreachable branch goes; add the missing back-links.
No behavior change. File one amendment adjudication covering TC-061 and
TC-161 (WI-645's and WI-646's re-drafts, and TC-161's move to the Full
tier) with LLR-167 (WI-646's sentence and this item's), so a single re-anchor
re-attests all of them.

## Done-when

- LLR-167's `detail` matches the code at the landing commit, and no approval record is refreshed by this item.
- The stale prose above is corrected, and `ruff check` is clean on the files
  touched.
- The joint adjudication is filed, and the commit bar passes.
