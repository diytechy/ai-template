+++
id = "WI-741"
title = "adjudicate: LLR-270 - approved/routed cell(s) amended on merged trunk 4cbb73c..3ecef62 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-270"]
+++

## Deliverable

`VERDICT: MEANING rows=1`, from spine-acts batch K, act seq 13. An
independent Opus adjudicator ruled it. The verdict is
[001-ADJUDICATE-768b209.md](../../../reviews/wi-741-adjudicate-llr-270-approved/001-ADJUDICATE-768b209.md).

- **LLR-270 re-attested:** keep-warm pings only a route whose runner's
  adapter bounds one turn.
- **The review's inferred-capability major** makes no stated claim untrue.
  By `one_turn`'s own contract, overriding it declares a bound.
- **One successor drafted below**, for a defect in WI-740's code that the
  WI-743 spot check found independently. `KeepWarmer` builds every row's
  argv at construction, so on Windows a refused `{prompt}` row behind a
  `.cmd` shim stops the dispatcher before its first poll when the dial is
  on. The fix leaves that row out of the eligible routes and adds one test.
  No row text changes.
- **Cross-review:** Sonnet found the act SOUND
  ([sonnet-batch-k.md](../../../reviews/2026-09-28-wave6/sonnet-batch-k.md)).

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-741-adjudicate-llr-270-approved/001-ADJUDICATE-768b209.md`,
under `VERDICT: MEANING rows=1`. LLR-270's new text is the text I would bless,
so it is re-attested in batch K's act, and nothing is returned. The one draft
below fixes a code defect that WI-740 introduced under the approved text, so no
requirement text changes.

```toml
title = "Build the keep-warmer even when one routing row's argv cannot be built: KeepWarmer builds every row's argv at construction, so a row the prompt-transport check refuses raises and stops the dispatcher before its first poll with the dial on"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 3
specref = ""
sr_refs = ["SR-227"]
```

THE DEFECT, reproduced at 768b209.

- WI-740 made `KeepWarmer.__init__` call `agent_session.build_argv` for
  EVERY row of the routing registry, of every family, to classify its adapter.
- `build_argv` raises `ValueError` for a row it refuses. One case is a
  `{prompt}`-in-argv row behind a Windows `.cmd`/`.bat` shim. The kit's own
  template row `gemini -p {prompt}` is such a row wherever `gemini` is an npm
  `.cmd` shim.
- So with `[adjudicator]` `context_reset_pct` and `keepwarm_minutes` both on,
  `session_service.keep_warmer` raises. `dispatch.run` then stops before its
  first poll, where before only that route's own launch was refused.
- This breaks LLR-270's approved "built by keep_warmer when keepwarm_minutes
  is also on, ticked once per dispatcher poll by run".
- Nothing changes at the shipped dial 0, where `keep_warmer` returns before it
  builds anything.

IN SCOPE, exactly the following:

1. **Code.** In `KeepWarmer.__init__`, a row whose argv `build_argv` refuses
   with `ValueError` is left out of the eligible routes, so it is never
   pinged. The warmer is still built, and every other row is classified
   exactly as today. Change nothing else:
   - do not move or weaken the prompt-transport check;
   - do not change `bounds_one_turn`;
   - leave every route's retention, resume, drain and retirement untouched.
2. **One test, in `tests/test_session_keep.py`.**
   - Build a `KeepWarmer` over a registry holding a claude row and a row whose
     argv build is refused. Force the refusal on every platform, for example
     by monkeypatching the prompt-transport check, because CI runs POSIX.
   - Assert the warmer is built, the refused row is not in its routes, and
     the claude row still is.
3. **The rows: none change.** LLR-270's text already states the obligation,
   and TC-268's method already covers the warmer being built from the routing
   registry.

OUT OF SCOPE, and a lane touching any of it is refused at review:

- `bounds_one_turn`'s method-identity inference. WI-741 ruled it honest, and
  a declared attribute is its own intake if one is ever wanted.
- Any cell of any row, LLR-270 and TC-268 included.
- The prompt-transport rule itself.
- The session-adapter interface row's method list.
