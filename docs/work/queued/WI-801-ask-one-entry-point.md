+++
id = "WI-801"
title = "One labelled entry point for model calls, with the per-kind routing table"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-ask"
sr_refs = ["SR-154", "SR-222"]
needs = ["WI-800"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-ask (ch.2 §3, §9). `ask(kind, ...)` and
`ask.py` become the only way to launch a model call, for the loop and the
coordinator alike (risk 8). Today's phases move on unchanged except for
author-derived exclusion (risk 2, B10; D-022, D-031), the decisions note handed by
`ask` on every path (D-014), and README A1, which this row builds: the per-kind
table `[routing.kind.<kind>]` in the one dial home (`families` weights, a family
absent or at 0 not eligible; `tier`, moved out of `agent_brief.DEFAULT_PHASE_TIER`),
ordering steps 1-4 and 6, every family exclusion as a ranked preference (D-035), the
swap rule, and family weights as literal shares (D-036). Step 5 (account by pace) is WI-814's; until then the account is drawn
by today's enable-list order. SR-154's "wherever one is configured" becomes
"configured for that kind" (README changes 28-29). An unlogged commit is attributed
by its `Co-Authored-By:` trailer (README Q-10 (a), D-001). One live `ask.py` call is
authorized (OI-104 Q-3).

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- Only `ask` launches or draws a route; the loop-memory family fields
  (`last_impl_family`, `last_build_family`) are deleted.
- `ask` deletes WI-835's entry point and moves its callers and tests to the
  adjudicate kind.
- A WI-688-shaped test passes: a build run outside the loop excludes its family
  from the judge.
- An `ask.py` call writes a log and carries the note; S9's reader covers CRITIQUE
  and plan-critique, and every kind outside it (judge included) receives the note.
- Each kind's judged scope and exclusions match ch.2 §3 step 2's table as amended
  by A1, and an excluded retained session yields a fresh, non-replacing call.
- A1 fixtures: a kind with one eligible family (a fresh same-family session,
  logged, no decisions entry); a judging kind after a swap; the shipped template's
  all-families table (equal weights draw equal shares; 2:1 draws two to one over a
  run of draws); `plan-critique` of
  each drafter's plan in a dual round; a weight of 0 never drawn.
- A preference the eligible set could have met but availability prevented is logged
  and becomes a "Decisions to review" entry (A1).
- This repo's dial home carries A1's per-kind values (build, plan, adjudicate,
  author ANTHROPIC; review, judge, author-review, plan-critique, final review
  OPENAI; plan-dual both; D-032, D-033).
- One live `ask.py` call has run (Q-3).
- Each spine row the README matrix gives this row (SR-154's first amendment:
  exclusion from all authors and "configured for that kind"; SR-222 and LLR-269,
  shared; LLR-044, LLR-081, TC-046, TC-084, IF-246; a new LLR and IF for `ask`) is
  amended or added and passes adjudication of that row, on whichever adjudication
  path is the one path when this row lands. The `session-protocol` skill and the S11
  hand recipe direct the coordinator to `ask.py`.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus judged-scope tests and the one live `ask.py` call.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit, adding the per-kind table to
  the dial home and stating the adopter-visible change (D-036): two families
  eligible for one kind at equal weights now alternate; unequal weights, or 0 to
  make a family ineligible, restore a lead.
