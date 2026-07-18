# 076-DESIGN-CHECK — tripwire page on the WI-161 review round (round 29)

The autonomous page-the-human path (PROCESS_OPTIONS.md "Unattended operation",
failure semantics): review round 29 (session 075, REVIEW-A of WI-161, built
session 074) fired a tripwire, `escalate` returned **page-human**, and
`docs/gate-policy: autonomous` routed the loop to a fresh **design-check
session** — a different provider at the strong tier — to rule grind-through vs.
genuine redesign. This session (Claude Fable, strong; the implementer was
gpt-5.6-sol / OPENAI) is that ruling.

## What fired, exactly (traced, not assumed)

- Scoreboard round 29: `verdict=APPROVE tier=strong margin=0 tripwire=1`
  ([scoreboard.txt](scoreboard.txt)).
- The only tripwire that can fire on a clean single-reviewer APPROVE with
  `findings=0` is **`implementer-touched-review-path`**
  (`score_reviews.fired_tripwires`): `finding-count-mismatch` needs a declared-N
  ≠ counted-N (075-REVIEW-A declares 0 and lists none), `near-duplicate-review`
  needs two verdicts (only REVIEW-A ran), and `mass-finding-rejection` needs
  rejected prior findings (there were none).
- The diff it checks is the **build's** commit range (`impl_range`, session 074
  = `9a39714..75cb46c`), which touched **`docs/agents-enabled`** — an exact
  member of `REVIEW_POLICY_PATHS` ("the implementer edited the referee").

## Ruling: **GRIND-THROUGH** (no redesign)

The tripwire fired true to its letter — the build diff did touch a
review-policy path — but the edit was not gaming; it was the *scoped work*:

1. **The owner ordered that exact edit.** WI-161's spec-of-record
   ([owner-intake-2026-07-14b.md#phase-preference](../specs/owner-intake-2026-07-14b.md))
   directs restoring `docs/agents-enabled` to Fable-first while the launchers'
   `AGENT_PREFER_MAP=BUILD=OPENAI-SOL` keeps Sol builds — the enable-list edit
   is a Done-when, not a smuggled referee change.
2. **An independent cross-family strong review approved it.** 075-REVIEW-A
   (Claude family, vs. the Sol implementer) ran the full `check.py` at G3
   (RESULT: PASS, 15/15 steps), the focused routing suite (55 passed), and
   traced all three selection branches — `VERDICT: APPROVE findings=0`.
3. **The mechanism worked as designed, end to end.** The tripwire is a
   non-scored hard stop that is "never absorbed silently"; autonomous mode
   answers it with exactly this cross-family strong ruling. Nothing about the
   design is indicted — the page is the design's cost for touching routing
   surfaces in-scope, paid once per such WI.

No assumption in the WI-161 implementation is disturbed; the artifact stands as
committed and reviewed. The loop returns to **BUILD** on the declared backlog
(`docs/next-wi` → WI-163).

## Follow-up filed (WI-167): a real coverage gap the trace exposed

`REVIEW_POLICY_PATHS` lists `scripts/score_reviews.py` and
`scripts/agent_route.py` — the *downstream scaffolded* layout. In this
meta-repo the kit scripts live at `project-trajectory/scripts/`, so the
prefix match misses them: session 074's diff **also touched
`project-trajectory/scripts/agent_route.py` (the routing referee itself) and
that did not fire** — only the `docs/agents-enabled` exact match did. An
implementer here could edit `score_reviews.py` (the scorer/tripwire source)
without tripping the wire. Fix sketch: extend the tuple with the
`project-trajectory/scripts/` variants (mechanical; keep the downstream
entries). Expected side effect, noted so no one is surprised: the fixing
commit itself touches the newly listed path, so its own review round will
fire the tripwire once and route one more design-check — by design.

RULING: GRIND-THROUGH — resume BUILD on WI-163; redesign not indicated.
