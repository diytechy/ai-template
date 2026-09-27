+++
id = "WI-664"
title = "Amend LLR-167, LLR-140, LLR-154 and TC-144 to the code as built, correct the routing prose that lags, and file the wave's joint amendment adjudication"
workstream = "requirements"
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-146", "SR-156", "SR-026"]
needs = ["WI-645", "WI-646", "WI-647", "WI-653", "WI-654"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

Absorbs the former draft H (backlog audit: both amend approved design rows to
the code and both owe an amendment adjudication, and under row-level refusal
an unjudged amendment blocks every other act that copies its registry, so they
are judged together).

**LLR-167 and its routing prose** (found by WI-645's build):

- LLR-167's approved `detail` says "A refusal falls back to the worker
  assignment and PRINTS why." The code holds instead:
  `agent_loop.route_session` returns `EXIT_NEEDS_HUMAN`, `session_body` says a
  declared brief that cannot be composed is a hold, not a fallback, and
  `test_an_unfillable_declared_brief_HOLDS_rather_than_dispatching_a_builder`
  pins it. TC-161 now says "held", so the two rows disagree until LLR-167 is
  amended.
- The same `detail` names `dispatch.red_tc_census` and `dispatch.parse_red_tc`;
  the code calls `census.red_tc_census` and `census.parse_red_tc`.
- Stale prose (non-spine): the comment above `adjudicate_brief._ASSEMBLERS`;
  `compose`'s unreachable "has no evidence assembler" branch;
  `agent_loop.session_body`'s paragraph saying an adjudication row whose
  evidence could not be assembled builds from the worker assignment;
  `tests/test_agent_loop_worker.py`'s module docstring (legacy `--track`
  "still runs", and SR-060 where TC-061 verifies SR-026); and
  `test_the_review_scorer_cannot_serve_this_grammar`'s count of "four"
  grammars where there are five.
- LLR-167's four original `code_symbol` entries carry no `Implements:`
  back-link.

**LLR-140, LLR-154 and TC-144** (found adjudicating the bookkeeping helper's
amendments, and by the codex review of that verdict, which judged LLR-140
blessed although two of its clauses are false):

- LLR-140's refusal ladder lists a "non-ordinary safety_class" rung the claim
  no longer has (`integrate._claim_refusal` runs SpecRef and status-prose
  refusals instead) and omits the rungs added since; its "commits only the
  paths the claim wrote" is stronger than the helper, which commits every
  changed path inside its declared scope (WI-647 narrows that window to what
  IF-186's contract then states; say exactly that).
- LLR-154 says the mint commits "the declared generated set"; the mint commits
  through the bookkeeping helper, which stages only the step's scope.
- TC-144 (verifies SR-156, LLR-150) carries a clause about the dispatcher
  reading past a dirty owner scratchpad, behavior LLR-143 owns under SR-026
  (`tests/test_dispatch.py::test_a_dirty_owner_scratchpad_does_not_stop_the_drive`).

IN SCOPE: draft the LLR-167, LLR-140 and LLR-154 `detail` amendments and move
TC-144's scratchpad clause to a test case of LLR-143's chain (amend both
methods), each to the code at the landing commit; correct the stale prose and
decide whether the unreachable branch goes; add the missing back-links. No
behavior change. Then file ONE amendment adjudication, by an independent
session, covering every approved row the second build wave amended (TC-061,
TC-161, TC-222, LLR-167, LLR-246, LLR-248, LLR-257, SR-209 and the bookkeeping
isolation test case, as each lands) together with this item's rows, so one
`intake.py snapshot --reattests` re-anchors them all.

Added 2026-09-26 at the owner's rulings: the joint adjudication also covers
the amendments WI-653 (LLR-216, OI-93 — the ruling delegates it to the next
amendment adjudication) and WI-654 (SR-211, its design row and test case,
OI-94) draft, which is why this item now needs them. WI-650's SR-217 chain
builds on LLR-257's adjudicated text and so follows the adjudication. WI-643 (the C1 sitting commit) needs this item; add the adjudication item
this item files to WI-643's `needs` in the same change, so the sitting waits
for the verdict and its re-anchor.

## Done-when

- LLR-167, LLR-140 and LLR-154's `detail` match the code at the landing
  commit, TC-144 states only SR-156/LLR-150 behavior, and the scratchpad
  clause is in a test case of LLR-143's chain.
- The stale prose is corrected, and `ruff check` is clean on the files touched.
- The joint adjudication is filed naming every amended row; no approval record
  is refreshed by this item, and the commit bar passes.
