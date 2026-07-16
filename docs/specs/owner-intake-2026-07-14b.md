# Owner intake — 2026-07-14 (batch b, 4 items)

**Status: triaged same day.** The owner's second 2026-07-14 batch (handed after
the phase-v3 g2-close sitting), flagged "possible duplicates" — so dedupe first,
per the [2026-07-14 intake](owner-intake-2026-07-14.md) pattern. Item 1 was an
executable directive (ruled inline, incl. the one side-effect question the owner
answered "flip now + knob WI"); items 2–4 are answered below and filed as WIs.

| # (owner item) | Already covered? | Disposition |
|---|---|---|
| 1 (OpenAI CLI → provider CLI; builder = Codex Sol) | Not covered — routing rows ride opencode | **WI-160** executed in-session ([openai-cli](#openai-cli)); the per-phase preference gap → **WI-161** ([phase-preference](#phase-preference)) |
| 2 (parallel work-items) | **Partially** — parallel tracks exist (WI-025: per-track lock, `--track` lanes); nothing *dispatches* independent WIs onto them | Answer below; auto-dispatch design → **WI-162** ([parallel-dispatch](#parallel-dispatch)) |
| 3 (critique budget: infinite / block dial) | **Partially** — `AGENT_CRITIQUE_MAX` exists (global); exhaustion already blocks-or-moves-on keyed to `docs/gate-policy` | Answer below; per-WI dial → **WI-163** ([critique-budget](#critique-budget)); the optimization-methodology research → **WI-164** ([optimization-research](#optimization-research)), joins the ratified research effort |
| 4 (Process tab loops render straight, want circular) | Not covered — SR-055's *prose* says "circular working loops"; the shipped TC-056 checks stages/links/determinism, not layout shape | **WI-165** ([process-loops](#process-loops)) |

## openai-cli

**WI-160 (executed in-session — owner directive).** The three OPENAI rows in
`docs/agents.csv` swap `opencode run --model openai/{model}` for the provider's
own CLI: `codex exec --model {model} --dangerously-bypass-approvals-and-sandbox`
(the non-interactive form; the bypass flag is this repo's explicit unattended
consent, the same posture as claude's `--dangerously-skip-permissions` — see the
launcher CONSENT banner). Driver: opencode sessions sometimes do not respond;
the owner wants to compare the native interface. **Builder preference = Codex
Sol "for now":** `AGENT_TIER_MAP=BUILD=strong` in both launchers + `OPENAI-SOL`
moved to the head of `docs/agents-enabled`.

- **Side effect (owner-ruled at intake: "flip now + knob WI"):** the routing
  engine has one preference order per tier, so Sol leading strong also makes it
  the first PLAN/DESIGN-CHECK draw — amending the WI-113 "Fable leads strong"
  lineup *for now*. CRITIQUE keeps drawing Fable whenever the implementer is
  OpenAI (heterogeneity excludes the implementer's family). **WI-161** restores
  per-phase preference properly.
- **Not installed yet:** `codex` is not on PATH at triage time. Self-healing by
  design — a session that fails to start puts the model on cooldown and
  selection falls back (BUILD → Fable at strong), no silent weaker tier. To get
  Sol builds: `npm i -g @openai/codex` (or brew) + `codex login`.
- **Supersedes (recorded, not deleted):** the WI-121 BUILD-medium relax (builds
  now route strong while this directive stands) and WI-110's OpenAI-side note
  (reasoning effort was "opencode `--variant`"; codex exposes it as
  `-c model_reasoning_effort=<level>` — left unwired, same no-telemetry-parity
  reason as WI-110).

## dev-setup-windows

**WI-160 follow-up (same directive, owner follow-up question "will dev-setup
also install the OpenAI CLI?").** Two gaps closed in the meta repo at the
follow-up: (1) `scripts/dev-setup.{sh,ps1}` still checked/offered **opencode**
after the codex swap — both twins now report/offer the **codex CLI**
(`npm install -g @openai/codex`, `codex login`); pinned test strings updated
(`test_onboard_devsetup.py`). (2) **No Windows double-click rung existed**
(`dev-setup.command` is macOS-only; double-clicking a `.ps1` opens an editor) —
new `scripts/dev-setup.cmd` shim runs `-Check` then offers `-Install`, logic
staying in the `.ps1` (the WI-051 `.command` pattern, Windows twin).

**WI-166 (queued, scripts).** Ship the rung downstream: a
`dev-setup.template.cmd` twin of `dev-setup.template.command` — scaffold-surface
work (bootstrap `MAPPING` + `test_bootstrap` file lists + README kit-contents +
a syntactic-validity test, per the session-protocol scaffold rule). Done-when: a
fresh scaffold ships the `.cmd` rung; double-click on Windows reports then
offers install; tests cover presence + shape; README row updated.

## phase-preference

**WI-161 (queued, unattended).** A per-phase model *preference* knob so "builder
prefers X" stops implying "every strong phase prefers X":
`AGENT_PREFER_MAP=BUILD=OPENAI-SOL,...` (launcher env, same shape as
`AGENT_TIER_MAP`) consulted by selection *within* the resolved tier before the
enable-list order; unknown/cooling ids fall through to today's order —
never-breaking, absent = today's behavior byte-for-byte. Done-when: map parsed +
validated at preflight; selection honors it within-tier only (never a tier
change); tests (preferred picked, cooling falls through, reviewer heterogeneity
still wins over preference); PROCESS_OPTIONS routing paragraph + launcher slot
comments; on landing, the owner may restore Fable-led PLAN by reverting the
enable-list order while keeping `BUILD=OPENAI-SOL`.

## parallel-dispatch

**WI-162 (queued, unattended — design spec first, WI-088 pattern).** Owner: "if
a work item's dependencies are all complete and there is no risk of overlap with
another work-item already being actively worked on, the work item should start
getting processed. Parallelization should be emphasized." **Answer to "is there
a setting preventing that?": no blocker — a missing dispatcher.** The machinery
exists (WI-025: `--track` lanes, per-track lock, per-lane `run-state`/`next-wi`),
but the shipped operating mode is one coordinator lane working one
`docs/next-wi` pin serially; nothing *assigns* independent actionable WIs to
parallel lanes. (Some of today's serialism is deliberate: effort coherence —
the v3 slices are a G2→G3 series; the research effort is owner-sequenced.)
The design WI specs: an actionability scan (all hard predecessors `done`) ×
an **overlap guard** (never two lanes on one WI; heuristics: shared `Workstream` /
same `Workstream` / shared SpecRef surface / spine-touching WIs stay serial —
exact rule is the spec's core question) × lane lifecycle (spawn up to
`docs/parallel` N lanes, per-lane next-wi, telemetry merge) × review-round
semantics per lane. Deliverable: ratifiable spec; implementation WIs file on
ratification. BuildTier=strong.

## critique-budget

**WI-163 (queued, unattended).** Answers first: **yes, the max is global today**
— `AGENT_CRITIQUE_MAX` (env, default 3), counted per run in-memory, one knob for
every critique scope. **And yes, a block provision already exists:** exhaustion
routes through `failure_action(docs/gate-policy)` — `attended` writes
`NEEDS-HUMAN` (hard block); `single-ratify` pauses *that WI* and surfaces it for
the batched sitting while the loop keeps running non-dependent work (exactly the
"default move on, block for human review where it matters" the owner describes —
it is how WI-144/OI-12 played out). What's missing is the **per-case dial**:
- a per-WI budget override — registry `CritiqueBudget` column or a
  `docs/critique-budget` map (design call in the WI): an integer, or **`inf`
  = iterate until APPROVE** (the acceptance-criteria-met loop; guarded by the
  existing per-session cost caps + the blackout/pause files so "infinite" can't
  run away unattended);
- a per-WI exhaustion disposition — `move-on` (default, today's single-ratify
  shape) vs `block` (force NEEDS-HUMAN even under single-ratify/autonomous).
Done-when: dial parsed (absent = today, never-breaking); `inf` honored with the
runaway guards named; `block` forces the page across gate-policies; tests for
all three shapes; PROCESS_OPTIONS paragraph.

## optimization-research

**WI-164 (queued, research track — `Workstream=research`, `BuildTier=strong`,
joins the ratified OI-9 effort behind WI-152/WI-154).** The owner's ask: a
principled approach to *iterative optimization problems* so the template stops
treating every refinement loop as "re-prompt the LLM and hope": how to lay out a
solution space, select samples, cross-pollinate candidates (population/beam
methods), when to stop — and, critically, **when the agent should construct a
conventional optimization/minimization loop over explicit variables (objective
function + optimizer as code) instead of iterating on the LLM itself**. Named
questions (the row's Done-when, per the research-WI shape): (1) a
decision rubric LLM-iteration vs. constructed-optimizer vs. hybrid; (2)
solution-space layout + sampling patterns usable at WI scale; (3) how
critique-loop budgets (WI-163's dial) map onto convergence criteria; (4) what of
this belongs in PROCESS_OPTIONS vs. a knowledge pack. Deliverable: a
`docs/knowledge/` pack + a PROCESS_OPTIONS guidance input — never code. Grounded
second-opinion review per the research charter.

## process-loops

**WI-165 (queued, dashboard — SR-055; hard predecessor WI-144, same emitter
file).** The Process tab renders loops A (intake) and B (human-decision) as
**straight stage rows today; the owner wants true circular loops** —
ring/racetrack layouts whose return edges close visibly, **intersecting at the
shared `LLM_Agent` node** (already rendered once per SR-055; the loops must
visually share it, the junction being the owner's stated intent). SR-055's prose
already says "two circular working loops," so this is render fidelity, not a new
requirement — no spine change; TC-056 gains a layout assertion (each loop's edge
cycle closes; the shared node appears once with degree ≥ 2 into each loop) via
change-intake if the build hardens it. Constraints unchanged: data-derived,
self-contained, byte-deterministic, data-less repos render byte-identically,
`--check` trips.
