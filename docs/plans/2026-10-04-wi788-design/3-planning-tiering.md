# WI-788 design, chapter 3: planning and tiering

**Status:** design note for the owner's checkpoint. Drafted 2026-10-04 against lane
`wi-788` at `c3be7be0`. Nothing here is built. Code cites are `path:line` under
`project-trajectory/scripts/` unless another root is given. Lane state is
[chapter 1](1-state-evidence-recovery.md)'s, `ask` and sessions are
[chapter 2](2-sessions-routing-accounts.md)'s, and the lock, mint and landing are
[chapter 4](4-adjudication-mint-landing.md)'s. This chapter defines what `PLANNING`
produces, how it is judged, and how a plan changes the build's tier.

## 1. Decisions in brief

1. **Two products.** An *implementation plan* (`PLANNING.SINGLE`) leads to `BUILD`.
   A *decomposition* (`PLANNING.DUAL`) yields successor rows and a terminal parent,
   and its lane never builds (B7).
2. **No arbiter model call.** In a dual round, after cross-critique and revision,
   each drafter names the plan it would adopt. Agreement adopts the plan, and it always
   includes one drafter conceding to its rival. Disagreement becomes an owner item
   (option (a)). `ARBITRATION` is that selection plus a mechanical gate (B11).
3. **Plans are judged against checkable criteria.** `plan_coverage` extends from goal
   clauses to the item's Done-when items, open review findings, and the item's SR and
   TC rows. A plan the gate fails cannot be selected or built from.
4. **The dual pickup runs in the claimed lane.** Children are drafted with a
   provenance key and minted by chapter 4's one allocator. The round directory is
   named by its work item, so no `DP-NNN` allocator remains. A PAGE closes the
   parent `partial` and mints a successor decomposition row that carries the
   round's evidence and waits on an open item. The `--dual-plan` flag and the preflight refusal retire.
5. **A per-item planning step exists in two places:** by declaration
   (`planmode = "single"`), and on demand at the second consecutive CHANGES-REQUESTED,
   folded into the existing family swap. It never fires by BuildTier alone.
6. **OI-103 Q5 dial:** `[planning] build_below_planner = false` (shipped default false).
   It applies only to a declared plan made before the first build. It is the one
   sanctioned exception to "never downgrade a declared route".
7. **Replanning** is the on-demand step. It revises the existing plan once per item,
   and the gate must show the same Done-when covered (plan-drift guard).

## 2. Today, confirmed in code

- **The pickup regression is real.** The worker refuses a claimed dual row at
  preflight (`agent_loop.py:1317-1329`); `dispatch._lane_close` keeps an
  `EXIT_PREFLIGHT` lane claimed for the next cycle (`dispatch.py:630-637`), so it
  loops. The old `dual_plan_disposition`
  (`31ad569d^:project-trajectory/scripts/agent_dispatch.py:2465-2545`) closed the
  parent on SELECT and committed evidence on PAGE; nothing replaced it.
- **The trigger is live.** No live row is dual, but the disposition prompt tells an
  adjudicator when to set `planmode = "dual"`
  (`prompts/adjudicate-disposition.template.md:44`) and intake mints it
  (`intake.py:1395-1404`, `:2019`).
- **Approved rows describe deleted code.** LLR-096 ("Commits SELECT or PAGE as one
  docs-only disposition") and TC-098 ("Run dispatcher SELECT…") have had no
  implementation since `31ad569d`; TC-098's evidence lists only flag-path tests.
- **`plan_runner` bypasses routing.** It draws its own pair (`plan_runner.py:102-154`),
  reroutes on nonresponse (`:392-430`), runs the arbiter pair on the ambient template
  (`:495-520`), and hard-codes the planner tier `"strong"` (`:317`).
- **The round writes outside any lane:** a `DP` id and watermark bump
  (`plan_artifacts.py:228-261`), WI ids from `max(live, mark)+1` with every child
  `medium` (`:277-352`, `:116`), and a direct `docs/log.md` append (`:355-371`), which
  this repo now compiles from `docs/log.d/`. All are trunk writers under OI-103 Q1.
- **Round state is not persisted**, though `plan_round` is built for it
  (`plan_round.py:27-29`; the runner holds it in memory, `plan_runner.py:340`).

## 3. Evidence

### 3.1 This repo's baseline (loop lanes only; commands in §9)

| measure | value |
|---|---|
| loop lanes with REVIEW-A verdict files | 48 (2026-07: 16, 08: 11, 09: 21) |
| REVIEW-A rounds per lane | mean 3.38, median 3; 12 lanes approved first time |
| first-round CHANGES-REQUESTED | 34 of 48 (71%) |
| lanes with two CR in a row before any APPROVE (the swap trigger) | 20 of 48 (42%) |
| lanes with three CR in a row | 10 of 48 (21%) |
| first CR, then APPROVE at round 2 | 13 of 34 |
| by BuildTier: strong | 17 lanes, first CR 76%, CR rounds 71%, **5.06 rounds/lane** |
| by BuildTier: medium | 28 lanes, first CR 68%, CR rounds 55%, **2.46 rounds/lane** |
| partial closes (= handback reports) | 5 of 783 terminal rows; all 5 strong (5 of 147 strong, 3.4%); 0 medium or quick |
| tokens per session (uncached input + output; 221 logs) | BUILD median 50.5k; REVIEW-A 35.5k; ADJUDICATE 23.4k |
| wall per session (median) | BUILD 1,066 s; REVIEW-A 622 s |
| tokens per row (77 rows with logged tokens) | median 83k across a median of 3 sessions, 2,318 s |
| logs carrying `gen_ai.usage.*` | 1 of 484 (`wi-688-001`); older logs carry only `tokens: in+out` |

**Limits.**
- The hand path (most work since 2026-09-24) writes no session logs and no loop
  verdict files, so it is absent here. Risk 8 closes that gap.
- `tokens:` counts Claude's uncached input only (`agent_loop.py:2682-2688`), so it
  under-counts cost.
- Three bands are thin: quick (2 lanes), medium/strong (1 lane), and the
  partial-close count.

### 3.2 Every recorded dual-plan round

This repo holds one round (DP-001, hand-run). The downstream repo `gilbert` sits on
this box (`C:/Projects/gilbert`, read-only) and holds seven (DP-001…007,
2026-07-18). That makes eight in all. No other downstream records are available here.

| round | critiques (A / B) | revised | coverage diff after revision | arbiter runs agree | ports | selected plan's family = arbiter's family |
|---|---|---|---|---|---|---|
| kit DP-001 | CR 1 / CR 1 | both | empty (7/7 each) | yes | 0 | yes (fable plan; opus arbiter) |
| g DP-001 | CR 2 / CR 3 | both | A 10/17, B 12/17 | yes | 0 | yes |
| g DP-002 | CR 4 / CR 3 | both | empty | yes (manual completion) | 0 | yes |
| g DP-003 | CR 4 / CR 1 | both | empty | yes (manual arbiters) | 0 | UNVERIFIED (planners fell back to Sol mid-round) |
| g DP-004 | CR 4 / APPROVE 1 | A | empty | yes | 0 | yes |
| g DP-005 | CR 3 / APPROVE 0 | A | empty | yes | 0 | yes |
| g DP-006 | CR 2 / CR 1 | both | empty | yes | 0 | yes |
| g DP-007 | CR 4 / CR 4 | both | empty | yes | 0 | yes |

Gilbert's planner A was ANTHROPIC-FABLE: `planner_pair` routes hat A first, and the
route note reads "ANTHROPIC-FABLE [ANTHROPIC] + OPENAI-SOL". Its arbiter rode the
ambient `AGENT_MODEL=claude-fable-5` (`gilbert/agent-resume.cmd:30`).

**What the record shows.** The arbiter pair agreed in 16 of 16 runs and ported
nothing in 8 of 8 rounds: the losing plan never contributed content. The arbiter
always picked its own family's plan (at least 7 of 8), so the record cannot separate
"better plan" from self-preference. Cross-critique did the work: 15 of 16 critiques
asked for changes, and 13 of 16 plans were revised.

**What it cannot show.** The owner's observation, that the drafters themselves
converged, is untestable here: no round asks a drafter to choose, and a critic sees
only the plan it critiques (`plan_runner.py:462-473`). The owner's earlier notes on an
arbiter judging the plan itself were not found in this repo, `gilbert`,
`gilbert-guidance` or `ai-template-plans`.

**Cost of a real round.** 8 to 11 sessions (each verdict's `budget:` line), 2 of the
happy path's 8 being arbiter runs. Wall time 27, 31 and 39 minutes (gaps between
gilbert's serial select commits, DP-004…007). Tokens, OpenAI half only, matched by
timestamp from codex rollouts: DP-005 2 Sol sessions 48.6k, DP-006 3 sessions 105k,
DP-007 3 sessions 154k (cached input included). The Claude half is unrecorded: the
plan sessions wrote no session log and the transcripts are gone. This repo's DP-001
ran by hand, without logs.

### 3.3 The research's weakest links, re-read (2026-10-04)

- **arXiv 2604.12147** v3 (ASE '26), read in full at https://arxiv.org/html/2604.12147.
  **It holds more narrowly than the research note says.** Its "plan" is SWE-agent's
  *generic* system-prompt workflow (navigate, reproduce, patch, validate), and its
  "subpar plan" is that workflow minus one phase (Finding 8), on GPT-5 mini,
  DeepSeek-V3/R1 and Devstral-small. It does not test planner-authored plans. What
  transfers: an incomplete plan hurts more than none, so gate plans on coverage
  (§4.5); and **periodic plan reminders raise success** (RQ5.2), so re-show the plan
  in each rework brief.
- **AdaCoder**, arXiv 2504.04220v1, at https://arxiv.org/html/2504.04220 (abstract,
  §III-E, §IV, §V-C and §VI read). **The figures hold as stated, on a narrow base:**
  27.69% average relative Pass@1 over MapCoder, 12.13× fewer tokens (26.81× vs 2.21×
  over Direct) and 15.88× shorter inference, on function-level HumanEval/MBPP with
  timing on open-source models only. Its planning trigger is a failed *execution* of
  sample tests. The kit's analogue is a failed review, which §4.7 keys on.

## 4. Design

### 4.1 Two products (B7)

| | implementation plan | decomposition |
|---|---|---|
| state | `PLANNING.SINGLE` | `PLANNING.DUAL` |
| declared by | `planmode = "single"`, or the on-demand trigger (§4.7) | `planmode = "dual"` (filing or a disposition draft) |
| artifact | `docs/plans/<WI>/plan.md` in the lane | `docs/plans/<WI>/round-<n>/` in the lane |
| next state | `BUILD` | no build: parent closes `complete`, children are drafted for `MINT` |
| ids | none | child ids from chapter 4's allocator at `ADJUDICATION.MINT` |

The plan file and round directory are named by the work item, so they are unique by
construction. This retires the `DP` watermark allocation, one trunk writer fewer for
B3. Existing `docs/archive/plans/DP-*` stay as history. `<n>` counts rounds within
the item; a PAGE's re-run happens under its successor's id (§4.6 item 5), so in
practice an item holds one round.

### 4.2 `PLANNING` for chapter 1's provider

The provider derives the substate from committed lane evidence. Nothing new is
stored. The round's persisted state is `round-<n>/state.json`, which the runner now
writes after every `plan_round.record`.

| substate | evidence |
|---|---|
| skipped | `planmode` empty or absent, and no on-demand trigger |
| `SINGLE` | `planmode = "single"` and no `plan.md` passing the gate with an accepted critique; **or** an on-demand trigger and no revised plan for that round |
| `DUAL.DRAFT` | `state.json` stage `plan` or `coverage1` |
| `DUAL.CROSS_CRITIQUE` | stage `critique`, `revise` or `coverage2` |
| `DUAL.ARBITRATION` | stage `select`. The outcome is `verdict.md`: `SELECTED` or `PAGE`. |

`plan_round`'s `arbiter` stage becomes `select` (§4.4). A resumed lane continues the
round from `state.json`, so sessions already spent are not re-run (B9).

### 4.3 Plan kinds through `ask`

Chapter 3 needs two kinds of [chapter 2's](2-sessions-routing-accounts.md) `ask`:

| kind | family | tier | independence | reset terms |
|---|---|---|---|---|
| `plan`: draft, repair, revise, select | [plan and build] | declared tier map; default `strong` | the two drafters are of **different families**, excluded by the round's recorded evidence (each drafter's attributed roster row), never by loop memory | the family's terms: shipped "every call", which is valid because each prompt is self-contained (own plan, rival, critique, coverage). If the family is retained, each drafter holds its own slot (`plan-and-build/<lane>/A` and `/B`), reset at round end. |
| `plan-critique` | [review] | the review tier | family ≠ the family of the plan's drafter; never a drafter's session | every call (S10's "reviewers never" retention stands) |

- **No `arbitrate` kind** is needed under §4.4. `ask` owns availability, the ratio and
  the pair constraint. `plan_runner` stops calling `agent_route.planner_pair`,
  `planner_fallback` and the ambient template; it calls `ask` and records results.
- **Two families are required.** When `ask` cannot draw two, the lane parks for
  availability (the review-owed park class). It does not run a same-family pair.
  This **changes PROCESS_OPTIONS' "family diversity best-effort"** for dual rounds
  under risk 7: no degraded mode.

### 4.4 Is the arbiter a standing step? No: option (a)

> **Amended by the owner's checkpoint ruling** ([README A3](README.md#the-owners-checkpoint-ruling-2026-10-04)): a disagreement's open item offers running an independent third agent of the owner's choosing.

| option | sessions after revision | what decides | cost, from §3.2 |
|---|---|---|---|
| (a) drafters select; disagreement to the owner | 2 short calls (continuations when retained) | adoption needs the rival author's concession | cheapest. The concession is a non-author's vote, so the self-preference confound in §3.2 disappears. |
| (b) as (a); disagreement to an arbiter | 2, plus 2 on disagreement | as (a), plus an arbiter that picked its own family 7+ of 8 times | adds a fresh full-context pair. No third family exists on this box. |
| (c) one plan, independent judge; pair kept for high risk | 1 plan + 1 judge | the judge, against the gate | right for implementation plans (§4.7). Dual rounds are the declared high-risk case, so a dual round still needs a selection rule: (a) or (b). |

**Recommendation: (a) for `DUAL`; (c)'s shape for `SINGLE`.** In `select`, each
drafter sees both revised plans, the coverage report and both critiques, and answers
`SELECT own|rival`; the adopted plan must also pass the gate (§4.5). If both choose
their own, the round PAGEs into an open item with its WI-790 placeholder (OI-103 Q2):
the owner picks from the evidence or orders a re-run. Every select is recorded, so
the first restored rounds measure drafter convergence; if disagreement proves
frequent, the owner may later rule (b) as the one path.

**A stated exception** to "a judgement never runs in a session that authored what it
judges", beside OI-101 Q1's: the deciding vote is the *losing* author's, cast against
its own interest; the winner's self-vote carries no weight alone (owner question 1).

### 4.5 What selection checks against: the gate

Today `plan_coverage.py` reads `C#` goal clauses and a `Plan-WI` table. It resolves
SR and IF references, finds cycles, and reports "coverage gaps as payload, never
findings". The extension makes the gate a script verdict:

- **Clauses.**
  - A `SINGLE` plan's clauses are the claimed item's Done-when items
    (`kitlib.done_when.items`, `D1…Dn`), plus open review finding ids (`F1…`) on a
    replan.
  - A `DUAL` plan's clauses are its goal's `C#` clauses.
- **Coverage is a finding.** A clause is either covered by a row, or named under
  `Excludes: <clause> — <reason>`. An unexplained gap fails the gate.
  - Gilbert DP-001's plan declared exclusions with reasons, and the arbiter accepted
    them (§3.2). The grammar makes that mechanical.
- **SR/TC diff.**
  - For `SINGLE`: every `sr_refs` entry of the item is cited by a row, and every TC
    that verifies those SRs is named by a row (to run or amend) or excluded with a
    reason.
  - For `DUAL`: today's pairwise coverage diff, unchanged.
- **Reference resolution**, as today: SR, LLR, TC and IF ids resolve; a `Proposed:`
  seam carries its rationale; a named file exists or is marked `new`.

The gate is what the drafters, the plan-critic and `BUILD` all read. The build's own
review is the execution-grounded judge (§3.3).

### 4.6 Restoring the dual pickup

The fix under risk 7; no interim guard.

1. **Admit.** The dispatcher admits a dual row like any row. Dual stays the
   exclusive `high-risk` kind (`schedule.py:359-381`): gilbert's owner asked for a
   cross-lane audit because concurrent rounds "couldn't see each other".
2. **Round.** The lane's worker enters `PLANNING.DUAL` instead of refusing.
   `run_dual_plan_round` runs in the lane worktree through `ask`, writing
   `round-<n>/` and `state.json`; its summary is a `docs/log.d/` fragment.
3. **Children, on SELECT.** The selected rows become successor drafts in the lane,
   in the format intake reads, each with `source = "<WI>/round-<n>:<Plan-WI>"`, a
   tier (the plan's `Tier` column, else the parent's BuildTier) and `needs` from
   plan-local edges plus the parent. The parent closes `complete` in the same lane.
   At `ADJUDICATION.MINT`, chapter 4's allocator mints all children or none.
4. **Duplicates.** A terminal parent is never re-admitted; `MINT` refuses a `source`
   an existing spec already carries (this also covers a resumed partial mint).
5. **PAGE.** A terminal parent can never be resumed (`handback.close_partial`
   moves it to terminal `partial/`, `handback.py:449`; the schedule never puts a
   `partial` row back on the frontier and requires a successor,
   `schedule.py:680-690`). So a PAGE:
   - commits the round's evidence in the lane, and the sitting's `MERGE_ACTION`
     is `merge-partial`: the parent closes `partial`, with its report;
   - at `MINT`, mints two things from the consumption list: the **open item**
     (its WI-790 placeholder) stating the disagreement, and the mandatory
     **successor** (OI-73): a decomposition row with `planmode = "dual"`, the
     parent's goal and Done-when, `source = "<parent>/round-<n>:PAGE"`, its
     `needs` citing the open item (so readiness holds it until the owner rules)
     and the parent;
   - the successor's lane reads the parent's `docs/plans/<parent>/round-<n>/`.
     The owner's ruling on the open item becomes its Done-when line (WI-790's
     rule): "adopt plan X from `<parent>/round-<n>`" makes its round a SELECT
     from that evidence with no new drafting, filing X's rows as on SELECT;
     "re-run" makes it run its own `docs/plans/<successor>/round-1/`.

   This replaces gilbert's ad-hoc "manual completion".
6. **Retired:** the preflight refusal; the `--dual-plan` flag and `_dual_plan_entry`
   (`agent_loop.py:3678-3734`, `:3920`), an off-lane trunk writer; the `DP` and WI
   allocation in `plan_artifacts`; `append_log_summary`.
7. **Tests:** admit (claimed, enters `PLANNING.DUAL`, no loop); round (recorded
   fixtures reach SELECT); children (provenance, all-or-none mint); duplicate (a
   repeated `source` is refused); page (the parent closes `partial`; the minted successor carries the round and waits on the open item);
   resume (continues from `state.json`).

### 4.7 A per-item planning step

| option | cost | metric it should move | verdict |
|---|---|---|---|
| never | 0 | none | rejected: strong rows average 5.06 rounds and own every partial close |
| by declaration, `planmode = "single"` | plan + gate + one cross-family `plan-critique` (+1 revision): ≈ 2-3 sessions, ≈ 85-150k tokens, 20-40 min, before any build | first-round CR rate (76% strong) and rounds per lane (5.06 strong) for declared rows | **adopt**: declared at filing or by the disposition draft, beside `buildtier` |
| by BuildTier (every strong row) | the above on ≈ 19% of rows (147 of 783) | the same | rejected: blunt, and no evidence that a missing plan is the cause |
| on demand at first CR | 1 plan session (≈ 50k) on 71% of lanes | rounds after a first CR | rejected: 13 of 34 first-CR lanes approved at round 2 without help |
| **on demand at second consecutive CR**, with the family swap | 1 plan session on 42% of lanes, and no added round: the swapped family plans, then builds | share of lanes reaching a third consecutive CR (**21%**); rounds in CC-prefixed lanes | **adopt** |

- **The ladder becomes:** CR → rework; CR CR → **replan + swap**; CR → tier-up;
  (Amended, [README A1](README.md#the-owners-checkpoint-ruling-2026-10-04): the swap prefers
  another eligible family; where one family alone may build, it draws a fresh session of it.)
  CR → page.
  - The replan is a `plan` call by the incoming family. Its clauses are the Done-when
    items plus the open findings, and the gate must pass before the build session.
  - No plan-critique is drawn: the next review judges.
  - This **amends LLR-081's ladder** (swap now carries a replan). It does not change
    the escalation constants.
- **The plan is re-shown in every rework brief.** This is the reminder effect
  (§3.3), at no session cost.

### 4.8 OI-103 Q5: build one tier below the planner

- **Where:** a new `[planning]` table, `build_below_planner = false`, in
  `docs/process.toml` and `process.toml.template`.
- **Recorded:** `plan.md` frontmatter carries `plan_id` (blob id at acceptance),
  `planner_tier`, `planner_route` and `session_id`, written by the caller from
  `ask`'s result, never by the model.
- **How BUILD reads it:** the pin is read today in `agent_brief.row_routing`
  (`agent_brief.py:423-443`) and folded in by `route_intent`
  (`agent_loop.py:544-548`); under chapter 2 it moves into `ask`'s tier rule for
  `build`. With the dial on and an accepted *declared* plan in the lane, the pin is
  one step below `planner_tier` (never below quick), and the log records
  `tier-reason: build-below-planner plan=<plan_id>`.
- **Never applies** to an on-demand replan (it follows failure) or to decomposition
  children (tier declared per row). **Escalation still wins**: the override applies
  after the pin, as today.
- **The one sanctioned exception** to "never silently downgrade the route"
  (`docs/knowledge/effort-tiering.md`) and the standing "never downgrade a declared
  route". It stays visible: an explicit dial and a recorded reason per session.
- **Replaces** LS3's scope threshold and B8's typed scope (OI-103 Q5).

### 4.9 Replanning against plan drift

- **Do findings reopen the plan? Yes, but only through §4.7's trigger:** two
  consecutive CR mean the approach is in question, not the edit.
- **Bound:** one replan per item. The next failure goes to tier-up, then page.
- **Drift guard:** the Done-when is fixed at claim (`kitlib/done_when.py`). The
  replanned plan must still cover every Done-when item, so a plan cannot narrow the
  item. A replan that drops one fails the gate.
- **Replan input:** a replan revises the existing plan, given the plan and the
  findings. It does not start blank, which keeps the reviewed rationale.

### 4.10 Rulings this changes

- **PROCESS_OPTIONS "Dual-plan decomposition"**, steps 5 and 7 and the `--dual-plan`
  paragraph:
  - the arbiter pair becomes drafter selection;
  - a degraded same-family pair becomes a park;
  - "the manual protocol remains the fallback" retires (risk 7);
  - the round runs only inside a claimed lane.
- **SR-155** ("arbitrated by fresh sessions", "refused on the direct build path") is
  amended. Its "never falling back to a single uncontested plan silently" stands.
- **"A review or judgement never runs in a session that authored what it judges"**
  gains a second recorded exception (§4.4).
- **"Never downgrade a declared route"** gains its one sanctioned exception (§4.8).
- **LLR-081's escalation ladder** gains the replan at swap (§4.7).

## 5. Matrix rows

| item | kind | action | why | successor |
|---|---|---|---|---|
| SR-155 | row | amend | selection by drafters under the gate; runs in the lane; PAGE becomes an open item | S788-dual-pickup |
| SN-024, SN-026 | row | preserve | rubric-judged by a non-author; families differ | — |
| SR-154 | row | amend (AC) | per-item planning, replan at swap, the Q5 dial | S788-single-plan |
| LLR-069 / TC-069 | row | amend | the gate's clauses, exclusions, SR/TC diff | S788-plan-gate |
| LLR-070 / TC (its) | row | amend | `arbiter` stage becomes `select`; persisted state | S788-plan-kinds |
| LLR-071 | row | amend | add the select brief; arbiter brief retires | S788-plan-kinds |
| LLR-072 | row | retire | the planner pair moves into `ask` (chapter 2) | S788-plan-kinds |
| LLR-073 | row | preserve | the coverage-step adapter | — |
| LLR-074 / TC-074 | row | amend | no DP or WI allocation, no `log.md` append; drafts with `source` | S788-dual-pickup |
| LLR-076 / TC-076 | row | amend | the runner draws no routes; calls `ask` | S788-plan-kinds |
| LLR-095 / TC-097 | row | amend | the preflight refusal is replaced by `PLANNING.DUAL`; `classify` kept | S788-dual-pickup |
| LLR-096 / TC-098 | row | amend (today unimplemented) | lane disposition: parent closure plus drafts for MINT | S788-dual-pickup |
| LLR-132 | row | amend | PAGE becomes an open item with a placeholder (OI-103 Q2) | S788-dual-pickup |
| LLR-081 / TC-084 | row | amend | replan folded into swap | S788-single-plan |
| new LLR under SR-154 | row | add | the build-below-planner tier rule (`ask`'s build tier) | S788-single-plan |
| SR-222 / LLR-269 | row | amend | `_dp_session` goes through `ask` | S788-plan-kinds |
| IF-057, IF-060 | contract | amend | the gate's input grammar and exit meaning | S788-plan-gate |
| IF-242 | contract | amend | `plan_coverage` joins `kitlib.done_when`'s requestors (the gate's `D#` clauses) | S788-plan-gate |
| IF-058 | contract | amend | `STEP_SELECT`; `SELECTED` needs a concession | S788-plan-kinds |
| IF-061 | contract | amend | the write side without allocators | S788-dual-pickup |
| IF-066 | contract | amend | no `template` or `model` args: `ask` routes | S788-plan-kinds |
| `PROCESS_OPTIONS.md:1365-1460` | doc | amend | §4.10 | S788-dual-pickup |
| `docs/knowledge/effort-tiering.md`, `co-planning.md` | doc | amend | the exception; the 8-round record | S788-single-plan |
| `prompts/dual-plan-arbiter.template.md` | prompt | retire | no arbiter call | S788-plan-kinds |
| `prompts/dual-plan-planner.template.md` | prompt | amend | select mode; `Excludes:`; `Tier` column | S788-plan-kinds |
| new `prompts/plan-single.template.md` | prompt | add | the implementation-plan brief, Done-when clauses | S788-single-plan |
| `prompts/adjudicate-disposition.template.md:44` | prompt | amend | name `planmode = "single"` beside `"dual"` | S788-single-plan |
| `agent_brief.py` rework brief | prompt | amend | re-show the accepted plan | S788-single-plan |
| `plan_runner.py`, `plan_round.py`, `plan_artifacts.py`, `plan_coverage.py`, `plan_briefs.py` | module | amend | §4.3-§4.6 | as above |
| `agent_route.planner_pair` / `planner_fallback` | module | retire (into `ask`) | bypass | S788-plan-kinds |
| `agent_loop._dual_plan_entry`, `--dual-plan`, preflight refusal | module | retire | off-lane trunk writer; refusal loop | S788-dual-pickup |
| `docs/id-watermark` `DP` key | carrier | preserve (frozen) | no new DP ids; history keeps its mark | S788-dual-pickup |
| `docs/process.toml` / template `[planning]` | carrier | add | the Q5 dial | S788-single-plan |
| `work/WI-000.template.md` `planmode` | doc | amend | `"" \| single \| dual` | S788-single-plan |

## 6. Proposed successor rows

Other chapters' rows are named by their final ids: S788-ask (chapter 2),
S788-lane-state-provider (chapter 1) and S788-mint (chapter 4). The full graph is the
[README's](README.md#the-dependency-graph-of-successor-rows).

| id | title and scope | Done-when sketch | needs | tier | bar | RESYNC |
|---|---|---|---|---|---|---|
| S788-plan-gate | The plan gate becomes checkable: `D#`/`F#` clauses, `Excludes:` grammar, SR/TC diff for SINGLE, optional `Tier` column | a SINGLE plan missing a Done-when item exits 1 naming it; an excluded clause with a reason passes; the diff names an uncovered SR and an unnamed TC; existing DUAL fixtures byte-identical; LLR-069, TC-069, IF-057, IF-060 amended | none | medium | module tests + smoke | yes (planner grammar) |
| S788-plan-kinds | `plan` and `plan-critique` through `ask`; runner loses route drawing and the ambient template; `STEP_SELECT` with the concession rule; `state.json` persisted; arbiter prompt retires | a fixture round makes no direct `session_service.call` or `planner_pair` call; a one-family pair parks; agreement adopts, mutual self-select PAGEs; an interrupted round resumes without re-spending; LLR-070/071/072/076, IF-058/066 amended | S788-ask, S788-plan-gate | strong | affected modules + smoke | yes (arbiter template retires) |
| S788-dual-pickup | Restore the dual pickup in a lane: `PLANNING.DUAL`, round dirs by WI, provenance-keyed child drafts for MINT, parent closure, PAGE as a `partial` close with a minted successor and open item; `--dual-plan`, the preflight refusal and off-lane writers retire | the §4.6 item 7 tests; as the last trunk-writer move (B3), a census test that no tool writer remains outside the landing (chapter 4 §3); SR-155, LLR-074/095/096/132, TC-074/097/098, IF-061 amended; PROCESS_OPTIONS reworded | S788-plan-kinds, S788-lane-state-provider, S788-mint, WI-790 | strong | affected modules + smoke | yes (`--dual-plan` launchers stop; a dual row is claimed like any row) |
| S788-single-plan | `planmode = "single"` (plan, gate, critique, ≤1 revision); replan folded into the swap; the `[planning]` dial; plan re-shown in rework briefs | a single row builds only after a gated, critiqued plan; CR CR yields one replan by the swapped family and a third CR tiers up; dial on: strong-planned row builds medium with `tier-reason`, dial off: unchanged; escalation still tiers up; SR-154, LLR-081 amended, new LLR + TC added | S788-plan-kinds, S788-lane-state-provider | strong | affected modules + smoke | yes (new dial, default false; new prompt) |

Order: plan-gate → plan-kinds → {dual-pickup, single-plan}. **The dual regression stays
latent until S788-dual-pickup**: restoring it earlier would allocate ids off the one
allocator, which breaks OI-103 Q1.

## 7. Questions for the owner

Consolidated in the [README](README.md#questions-for-the-owner-at-the-checkpoint):
question 1 is Q-5 and question 3 is Q-6. Question 2 is decided there under risk 7
(park), as a stated change the owner may reverse.

1. **Dual selection: (a), (b) or (c)?**
   - **Recommend (a):** the drafters select, and a mutual self-select goes to the owner
     as an open item. Also record that a losing author's concession is a second
     exception to the independence rule.
   - Why: in 8 rounds the two arbiter runs always agreed and ported nothing, and the
     arbiter picked its own family's plan in at least 7 (DP-003 unverified). Whether
     arbitration ever changed a selection is unknown: no drafter was asked.
2. **Dual rounds with only one family available: park, or run a same-family pair?**
   **Recommend park** (risk 7: no degraded mode). Every recorded round had two families
   at the start, and DP-003 degraded mid-round.
3. **Per-item planning: declaration plus on-demand at the second consecutive CR (as
   recommended), or also at the first CR?**
   **Recommend as recommended**, and re-measure the 21% three-CR share after 20 lanes.

## 8. Calls no spec or ruling settles

| decided | alternative | reversal cost | why not escalated |
|---|---|---|---|
| round directories named by WI (`docs/plans/<WI>/round-<n>`) | keep DP allocation, moved to MINT | low: a path convention | removes a trunk writer outright |
| replan at the *second* CR, folded into the swap | at the first CR | low: one ladder constant | measured: 13 of 34 first-CR lanes approved unaided |
| the dial skips on-demand replans and decomposition children | apply everywhere | low | "planned items" read as items with a declared accepted plan |
| child tier is the plan's `Tier` column, else the parent's BuildTier | today's hard-coded `medium` | low | the hard-coded value lowers tier without a dial |
| dual stays `high-risk` and exclusive | drop exclusivity now that rounds run in lanes | low | gilbert's owner asked for cross-round visibility |
| no plan-critique on an on-demand replan | critique it too | low: one session | the next review judges |

## 9. Research record

Read-only, from `C:/Projects/ai-template.wt/wi-788` unless named; every command exit 0.

- **Baseline:** `C:/Projects/ai-template/.venv/Scripts/python.exe <scratchpad>/ch3_baseline.py .`
  (spec frontmatter, `docs/reviews/*/*-REVIEW-A-*.md` verdicts, `docs/iteration/*.log`
  headers). Decisive: `REVIEW-A rounds per lane: n=48 mean=3.38 median=3.0`;
  `strong lanes=17 firstCR=13 (76%) … mean-rounds=5.06`; `medium lanes=28 firstCR=19
  (68%) … mean-rounds=2.46`; `BUILD n=136 median-tokens=50541`;
  `with gen_ai.usage.input_tokens: 1`.
- **Verdict sequences:** a per-lane `grep -o "VERDICT: …"` fold through
  `sort | uniq -c`: `11 A`, `9 CA`, `6 CCA`, `4 CCCA`, … Lanes by month from
  `git log --diff-filter=A` per review folder.
- **Partials:** `grep -h "^buildtier" docs/archive/work/partial/WI-*.md` → 5× strong;
  `complete/` by tier: strong 142, medium 340, quick 105.
- **WI-199's record** (`docs/archive/work/complete/WI-199-*.md`, read in the fix
  round): the round's runner drew planners through `planner_pair`, with "ambient
  template both hats = the recorded routing-off degraded mode", and mapped PAGE
  per gate policy (attended: a NEEDS-HUMAN stop). It records no session, token or
  wall-time figures, so it adds nothing to §3.2's cost evidence; the degraded
  mode it names is the one §4.3 retires.
- **Rounds:** `docs/archive/plans/DP-001-*`; in `C:/Projects/gilbert`,
  `find . -type d -name "DP-*"` (7), `grep` of critique, coverage and verdict lines,
  `git log` of the `dual-plan select` commits (10:34, 11:01, 11:33, 12:12 −0500,
  2026-07-18), `agent-resume.cmd:24-31`.
- **OpenAI half of round cost:** `<scratchpad>/ch3_codex_dp.py` over
  `~/.codex/sessions/2026/07/{17,18}`, cwd gilbert. `ls ~/.claude/projects/c--Projects-gilbert`
  shows only 2026-09-19/20 files, so the Claude half is not recoverable.
- **Code read:** `plan_runner.py`, `plan_artifacts.py`, `plan_round.py:1-140`,
  `agent_loop.py:495-552,1295-1340,2676-2692,3270-3290,3678-3740`,
  `dispatch.py:577-850`, `schedule.py:340-440`, `agent_route.py:864-960,1090-1150`,
  `agent_brief.py:423-443`, `intake.py:55-70,436-452,1395-1404`, `git show 31ad569d`,
  `31ad569d^:…/agent_dispatch.py:2465-2545`.
- **Rows, specs, log:** SR-155, SN-024, LLR-044/045/069-076/081/095/096/132,
  TC-097/098, IF-057/058/060/061 from the lane's TOML; WI-209's archived spec;
  `docs/log.md:13266-13330`.
- **Papers:** `curl -sL` (HTTP 200), 2026-10-04, converted to text.
- **Knowledge packs:** `agent-routing.md`, `effort-tiering.md`,
  `prompt-image-token-efficiency.md` (no bearing beyond token accounting),
  `co-planning.md`.

**UNVERIFIED:**
- DP-003's selected-plan family;
- the session-to-round mapping for Sol tokens;
- which LLR, if any, owns `agent_brief.row_routing` (no LLR lists it in `code_symbol`);
- the AdaCoder Pass@1 base set's per-model rows were not recomputed;
- the owner's earlier arbiter notes, which were not found.
