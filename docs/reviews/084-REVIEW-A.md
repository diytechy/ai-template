# 084-REVIEW-A — WI-165 (Process tab — render loops A/B as shared circular loops)

Independent review of commit `a0a0361` (WI-165: render shared circular process
loops), built session 083. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-14b.md#process-loops`), the WI-165 registry row
(SR-055, predecessor WI-144), SR-055 / LLR-056 (`docs/requirements/`), and the
changed TC-056 (`docs/test/test-cases.csv` + the generated `docs/okf/.../TC-056.md`).
This is a BUILD commit (spine stays G3), not a G1/G2 Status-change ratification,
so no `--ratify` hierarchy applies. TC-056 changed, so the registry-sweep step
applies (below).

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check.py` → all steps PASS: `format`
  (72 files already formatted), `lint` (all checks passed), `tests+coverage`
  **780 passed, 3 skipped, coverage 91.60%** (178.7s).
- `python project-trajectory/scripts/trace.py` → `SN=24 SR=56 LLR=57 TC=57
  orphans=0 integrity=0 components=5 component-findings=0 interfaces=52
  interface-findings=0`.
- Process-loop cases: `pytest -k "process_loop or process_tab_renders"` → 6 passed.
- Policy sweep: `docs/gate-policy` = `autonomous`, derived `docs/gate` = `G3`,
  `docs/push-policy` = `human` — all consistent with `status.md`/`next-wi` prose
  (WI-165 dropped as done, `next-wi` → WI-167). No status/policy contradiction.

## Registry sweep (TC-056 changed)

TC-056's new Expected — "explicit closed cycles", "degree ≥ 2 into each loop",
"outbound and return-side placement" — is coherent with SR-055's AC (shared
LLM_Agent once; links resolve; gate-ratification in loop B; data-less identical;
deterministic; `--check` trips) and LLR-056's stage lists, and matches the
spec's stated TC hardening ("each loop's edge cycle closes; the shared node
appears once with degree ≥ 2 into each loop"). Stage lists in `_loop_panel`
(A = 5 stages, B = 4 stages) match the TC row and the CSS `nth-child` grid
placement. No contradiction with the historical rows it touches.

## Assessment

The mechanical contract holds: the panel is data-derived, self-contained, links
resolve, the data-less render is byte-identical, generation is deterministic and
`--check` trips — the whole G3 suite is green. The layout logic (two 2-row grid
"racetracks", loop-B corner overrides, the responsive ≤760px reflow) is sound in
isolation.

But the render fidelity that is the entire point of this WI has a cascade defect
the string-only tests can't see. The `loop` class is applied to **two** nested
elements — the wrapper `<div class="loop loop-a">` *and* the inner
`<ol class="pflow loop">` (confirmed in the generated HTML). The new box rule
`#process .loop{...border:2px solid var(--accent);border-radius:999px;padding:...
;min-height:10.5rem;position:relative}` (line 2729) and the return-arrow
`#process .loop::after{...}` (line 2733) both use the **bare** `.loop` selector,
so they match the inner `<ol>` as well as the wrapper. `#process ol.pflow.loop`
(line 2739) only overrides `display/grid/margin/align-items` — it does **not**
reset `border`, `border-radius`, `padding`, `min-height`, or `position`, so the
`<ol>` keeps them. Net: each loop renders as a **nested double racetrack** (two
concentric accent-colored pills, the inner one inset by the wrapper's padding)
with **two** return arrowheads. The same bug repeats in the `@media(max-width:760px)`
block (lines 2754 and 2759), so both the default and mobile layouts are affected.
That is not "true circular loops" — it directly undercuts the WI's Done-when.
The fix is to scope the box + `::after` rules to the wrapper only (e.g. `div.loop`
/ `div.loop::after`, or the div-only `.loop-a,.loop-b` classes); the grid rule
already correctly targets `ol.pflow.loop`, and `.loop .loopname` still resolves.

A secondary, lower-severity point: TC-056 now advertises "degree ≥ 2 into each
loop" as a verified property, but the only mechanization is the test asserting
the literal `data-loop-a-degree="2"` / `data-loop-b-degree="2"` strings that this
same commit hardcodes into `_loop_panel` — a self-referential check that gives no
regression protection for the actual junction connectivity.

## Findings

- [MAJOR] project-trajectory/scripts/gen_trajectory.py:2729 -> the bare `#process .loop{...border-radius:999px;border;padding;min-height;position}` box rule and the `#process .loop::after` arrowhead (lines 2729/2733, and again in the ≤760px media query at 2754/2759) match BOTH the wrapper `<div class="loop loop-x">` and the inner `<ol class="pflow loop">` (both carry class `loop`); `#process ol.pflow.loop` never resets those props, so each loop renders as a nested double pill with two return arrowheads instead of one racetrack — defeating the WI's "true circular loops" render intent (string-only tests don't catch it) -> scope the four box/`::after` rules to the wrapper element (`#process div.loop{` / `#process div.loop::after{`, both the main-block and media-query occurrences), leaving `#process ol.pflow.loop` for the grid; then eyeball the regenerated `PROJECT_STATE.html` Process tab -> @owner
- [MINOR] docs/test/test-cases.csv:57 (TC-056) -> the Expected claims "LLM_Agent renders once with degree >= 2 into each loop" as verified, but `test_process_loops_share_one_llm_agent_entry` only asserts the hardcoded `data-loop-*-degree="2"` attributes the same commit emits — a tautological assertion that can't detect a layout that fails to connect the shared node twice -> either soften the TC wording to "declares its per-loop degree via a data attribute" (for clarity), or assert the junction connectivity structurally (e.g. count the return arrowheads / entry-adjacency) rather than the self-emitted constant -> @owner

VERDICT: CHANGES-REQUESTED findings=2
