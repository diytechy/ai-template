## 2026-09-04 — Two review-churn defects: MINOR-only refusals, and a rework that moved nothing

Both were measured on the 2026-09-03/04 supervised run and are recorded in
[the handoff's churn section](../handoff-2026-09-04.md) (§4). Together they cost
six review rounds and four rework sessions in one day, none of which changed
what ships.

### 1. A CHANGES-REQUESTED whose findings are all `[MINOR]` routes as an APPROVE

Four rounds refused a lane over a single `[MINOR]` finding each — WI-586 rounds
006 and 010, WI-590 round 013. Each refusal bought a rework session AND another
round (an agent session plus a full harness re-run) to land a wording nit the
reviewer had not called a defect. A MINOR is by construction the severity a
reviewer assigns when the remedy is not worth blocking on; spending the block on
it inverts the scale the brief asks reviewers to use.

`kitlib.verdict.effective_verdict(word, findings)` is the one home for the rule:
`CHANGES-REQUESTED` + at least one finding + every finding `[MINOR]` reads as
`APPROVE`; every other word is returned untouched. **The round file is never
rewritten** — the reviewer's own `VERDICT:` line stays exactly as written and
the findings stay carried. What changes is what the READERS do with it, and both
readers had to change together, since a lane the loop routed as APPROVE would
otherwise still be refused at the merge slot:

- routing — `score_reviews.merged_routing_verdict` reads `merge_verdict`'s
  output through the rule and prints `review round: CHANGES-REQUESTED with
  MINOR-only findings routed as APPROVE (N findings carried)` when the reading
  changes the outcome. The ROUND is the unit, not the reviewer, because the
  merge has already collapsed them: an APPROVE beside a MINOR-only refusal is a
  round nobody found a defect in, while a MAJOR anywhere keeps the refusal.
- the gate — `kitlib.verdict.round_entries`, which feeds
  `integrate._round_refusal`, parses each round file and yields the effective
  word, so the slot re-derives the same verdict from the same rule.

**A CHANGES-REQUESTED with NO findings stays a refusal.** A reviewer that blocks
without naming anything is a different defect, and `all()` over an empty sequence
would have promoted it silently; the emptiness is tested first and on purpose.

`prompts/reviewer.template.md` is unchanged: no sentence there says a finding of
any severity forces a refusal, so nothing in it contradicts the new reading.

Tests: `test_effective_verdict_reads_the_findings_not_only_the_word`
(7 cases incl. the mixed-severity and zero-finding negatives),
`test_a_minor_only_refusal_clears_the_gate_and_the_file_is_untouched`,
`test_a_minor_beside_a_major_still_refuses`,
`test_a_refusal_naming_no_finding_at_all_still_refuses`
(tests/test_verdict_record.py);
`test_merged_routing_verdict_promotes_a_minor_only_round_and_says_so`
(tests/test_score_reviews.py);
`test_a_minor_only_refusal_routes_as_an_approve`,
`test_a_minor_beside_a_major_still_requests_changes`,
`test_a_refusal_with_no_findings_still_requests_changes`
(tests/test_agent_loop_review.py, the shipped loop end to end).

### 2. No round is drawn on a tree a verdict has already named

A rework session that DECLINED a finding committed only its answer under
`docs/reviews/` — a record path `kitlib.verdict` is built to ignore — so
`governing_identity` did not move. The loop armed another round, the reviewer
approved the very tree the previous round had refused, and
`integrate._round_refusal` read the pair as a reroll-until-green and refused the
lane. Two reviewer sessions and a merge attempt bought nothing, and no console
line said why.

`kitlib.verdict.tree_already_judged(root, branch, base, parse)` asks the merge
slot's own question — does a logged round already name this governing tree — and
`agent_loop.schedule_review_round` now asks it BEFORE drawing a round instead of
after wasting one. When the answer is yes it prints the cause and escalates
through the existing ladder (`agent_route.failure_action` → `page_consequence` →
`apply_page_consequence`): a human-held run stops with a banner, a loop-held one
degrades to DESIGN-CHECK, whose own commit re-arms the round if it moved the
tree (the owner's 2026-09-03 ruling leaves that degrade uncapped and it is left
alone). Unreadable git answers "not shown to be unchanged" and the round is
drawn, so a repo these readers cannot see into never wedges its first build.

Tests: `test_a_record_only_rework_draws_no_round_and_pages` and
`test_a_rework_that_moves_the_spec_draws_its_round`
(tests/test_verdict_record.py) — the two answers driven through the shipped
`build_bookkeeping` arm on a real lane.

### The size budget, paid outward

Both features landed **net negative** on `agent_loop.py` (2575 → 2572 SLOC,
re-stamped downward) rather than taking a baseline bump. The routed verdict went
to `score_reviews`, the tree question and its operator sentence to
`kitlib.verdict` (both far under the module threshold), and three duplicates
inside the arms being touched became one each: `page_human` (the page prologue
the review-escalation and critique-budget paths held in duplicate),
`committed_build_rounds` (the three-call sequence the BUILD and DESIGN-CHECK
arms held in duplicate), and `absorb_review_verdict`'s twin failure arms — one
consequence, two messages, now one arm and a `why` string. Every console line
those consolidations emit is byte-identical to what it replaced.

`schedule_review_round`, `schedule_adjudication_round` and `build_bookkeeping`
now return an exit code (or None) so the page can end the run; nothing else
about their contracts moved.

Deferred open items: none — both defects are closed at their root with the
routing and gate arms driven from the shipped paths, and the reviewer brief
needed no edit because nothing in it contradicted the new reading.
