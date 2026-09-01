# WI-567 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-567-construction-first-remedies-t/`, time-ordered, governing
line last. One mechanized round exists (the loop scheduled it after the
committing BUILD, review-policy 1, cross-family draw); the verdict gate
requires this per-WI rollup and nothing in the kit writes it yet (the
verdict-carrier repair is queued), so it is compiled by hand.

### Supervisor note — NOT a round, does not govern

Recorded so the merge carries it, per the standing "compile, do not
rubber-stamp" brief. An independent read of the lane diff against the plan's
five Done-when arms (a read-only Opus pass drawn by the supervisor, not a
recorded round) agrees arms 1–4 are delivered and that the adjudicator
briefs were correctly left unwidened with per-template reasons. It found
three convention misses no instrument reds, all in the record layer:

- the fragment's driven figure (1 structural remedy in 13 rounds) carries no
  `fig:` provenance marker (the declared-figure convention, WI-392;
  `check_figures.py` is opt-in by marker, so it stays green);
- the fragment declares no `Deferred open items:` line (`gen_open_items.py
  --check` passes because its file-level rule fires only on multi-section
  fragments);
- the new test pins the two exemptions but not the warn-first sentence
  ("no finding is refused, downgraded, or blocked"), the plan §2 property
  most likely to be edited into a gate.

None alters the round's verdict. They are carried to the session record for
a later row, not reworked here: a post-APPROVE code commit would cost another
round for a record-layer nit, and the doctrine this very row wires argues
against a guard-shaped fix for a convention miss.

### REVIEW-A — Round 2 — OPENAI-TERRA (medium, `-c model_reasoning_effort=medium`) — tip dfbfe08

The reviewer established the governing plan and exact diff, exercised the
changed paths, and recorded: prompt-loader behaviour verified; the added
`tests/test_prompts.py` regression body FAILS against the pre-change
`contract_split` prompt loader and PASSES on the lane tip, so it detects the
changed behaviour; harness summary `RESULT: PASS`; strict integrity
`integrity=0`; `gen_prompt_catalog.py --check` fresh. No findings raised.
(Full text: `002-REVIEW-A-dfbfe08.md` — the machine line only; the reasoning
above is the reviewer's committed final message as the session log records
it. Advisory scoreboard: `scoreboard.txt`, margin 0, tripwires none.)

VERDICT: APPROVE findings=0
