# Bar-vs-stage census — how often does the kit key behavior off a CLEARED bar rather than the CURRENT derived stage?

**Status:** measurement only. This document REPAIRS NOTHING and proposes nothing.
It answers one question the owner asked in the OI-51 exchange and stops there;
the ruling is the owner's.

**Scope swept:** `project-trajectory/scripts/` (all shipped scripts),
`project-trajectory/ci/`, `project-trajectory/agent-hooks/`,
`project-trajectory/skills/`, `docs/stack.ini`,
`project-trajectory/stack.ini.template`, `docs/process.toml`,
`project-trajectory/process.toml.template`, and `tests/` where a test pins one
semantics as the contract.

**As of:** branch `requirements/ears-and-quality-characteristics`, HEAD `83a92b99`,
clean tree, 2026-08-21.

---

## The owner's question

> "Bar indicates clearance of a stage, which is identical to just looking at the
> next higher stage. […] I would prefer this to just look for if we are in or
> above 'DevStg-Impl', then perform the checks. In this way it checks for 'When
> is it relevant for me to run these checks' rather than 'What previous step did
> I pass that implies these checks can be done'. In general, behavior should be
> tied to development stages, not bars or clears. Can you or a subagent break
> down how often we are checking for 'bars' or 'clear' vs just checking the
> current derived development stage?"

---

## The classification

- **(A) BAR / CLEARANCE semantics** — the site runs or allows something *because a
  bar was (or must next be) cleared*. It reads the runnable bar on `docs/gate`'s
  last line, an `ex-draft=`/`computed=`/`per-phase=` bar, a `gates=` step tag, a
  `--stage-cleared`/`--gate` argv value, or a WI's declared `bar:`.
- **(B) CURRENT-STAGE semantics** — the site runs or allows something *because the
  repo is IN (or at/above) stage X*. It reads the `stage=` basis field or a
  stage-rung predicate directly.
- **(C) MIXED or AMBIGUOUS** — the site reads one axis and presents or treats it as
  the other, or its vocabulary obscures which reading is meant. OI-51's root
  cause was exactly a C.

---

## TALLIES

| Class | Count | Share |
|---|---:|---:|
| **(A) bar / clearance** | **55** | 60% |
| **(B) current stage** | **27** | 30% |
| **(C) mixed / ambiguous** | **9** | 10% |
| **Total classified sites** | **91** | |

Plus 2 cross-axis **guards** (counted separately — they enforce vocabulary, they
do not consume state) and a set of **clean negatives** recorded at the end so
they are never miscounted as gate sites.

### Per-module counts

| Module | A | B | C | Note |
|---|---:|---:|---:|---|
| `derive_gate.py` | 7 | 4 | 2 | the producer of BOTH axes |
| `check.py` | 13 | 0 | 2 | **the entire harness selector is bar-keyed; it reads the stage nowhere** |
| `agent_common.py` | 0 | 6 | 0 | the ratification-dial layer — purely stage-keyed |
| `dispatch.py` | 0 | 3 | 0 | |
| `agent_loop.py` | 0 | 3 | 0 | |
| `agent_route.py` | 0 | 1 | 0 | |
| `plan_round.py` | 0 | 1 | 0 | |
| `intake.py` | 3 | 2 | 0 | split: WI `bar:` is A, adjudication authority is B |
| `integrate.py` | 4 | 0 | 0 | |
| `check_trajectory.py` | 3 | 0 | 0 | |
| `trace.py` | 2 | 0 | 0 | |
| dashboard / status surfaces | 3 | 1 | 2 | `traj_parse`, `traj_panels`, `traj_status` |
| `trunk_step.py`, `bootstrap.py`, `gen_release_checklist.py` | 3 | 1 | 0 | |
| `docs/stack.ini` + template | 4 | 0 | 0 | |
| `docs/process.toml` + template | 1 | 3 | 0 | |
| `project-trajectory/ci/` + `.github/workflows/` | 4 | 0 | 0 | |
| `project-trajectory/agent-hooks/` | 0 | 0 | 0 | **clean negative** |
| `tests/` (contract pins) | 5 | 1 | 3 | |
| `skills/` | 3 | 1 | 0 | |

**The headline shape:** the split is not random. It falls almost exactly along a
module boundary. **Everything that selects CHECKS is bar-keyed (A). Everything
that decides WHO RATIFIES is stage-keyed (B).** The owner's preferred rule is
therefore already implemented, correctly and in one home, on the ratification
half of the kit — and implemented nowhere on the harness half.

---

## THE DECISION-RELEVANT FACT: is "current derived stage" derivable to `DevStg-Impl`?

**Short answer: no — but not for the reason the bar cannot reach it, and the
distinction changes the ruling.**

There are two separate unreachabilities, on two axes, from two different causes.

### 1. The BAR cannot reach `DevStg-Impl` — the OI-30 D2 ceiling

`derive_gate.py:364` sets `_RELEASE_CEILING = BAR_TESTS`, and `sr_bar`
(`derive_gate.py:390`) returns it at `:400` for any decomposed row whatever the
Status cell says. This is deliberate and ruled: a status cell must never claim
"the evidence passed". This is OI-51's stated mechanism.

### 2. The STAGE cannot reach `DevStg-Impl` either — rung 6 is VACANT under the closed Status enum

This is **not** the ceiling. `spine_stage` (`derive_gate.py:888`) is computed
independently of `sr_bar` and no ceiling is applied to it. The obstruction is a
different one, and it is arithmetic:

- `trace.py:431` closes the spine Status vocabulary:
  `STATUS_VALUES = frozenset({"Drafted", "Approved", "Founded"})`, and
  `trace.py:437` puts `Status` in `INTEGRITY_ENUM_COLS` — an **always-on**
  integrity error, not a `--strict-schema` one.
- `spine_stage`'s Tests→Impl→Release discriminator is `derive_gate.py:991`:
  `if not all(is_approved(r) or is_founded(r) for r in srs): return STAGE_IMPL`.
- An SR that survives the earlier Drafted rung (`derive_gate.py:965`) is by
  definition `Approved` or `Founded`. So the `STAGE_IMPL` branch **cannot be
  reached by any legal cell**, and a fully decomposed spine falls straight
  through to `STAGE_RELEASE`.

**A legal spine skips rung 6 entirely: `DevStg-Tests` (ord 5) → `DevStg-Release`
(ord 7).**

### The demonstration

Driven directly against `derive_gate`'s own functions over synthetic spines
(one SN, one SR decomposed by one LLR and verified by one TC, nothing Drafted;
no `external.toml`/`components.toml`, so the two inserted rungs are skipped by
their applies-when):

```
--- every LEGAL closed-enum spine, fully decomposed + TCs authored ---
SR Status = 'Drafted'  (legal)        stage=DevStg-Reqs     ord=2/8  computed=DevStg-Below  bar=DevStg-Reqs   stage_to_bar=DevStg-Reqs
SR Status = 'Approved' (legal)        stage=DevStg-Release  ord=7/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl
SR Status = 'Founded'  (legal)        stage=DevStg-Release  ord=7/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl

--- values OUTSIDE the closed enum (always-on integrity ERRORs) ---
SR Status = 'Implemented'             stage=DevStg-Impl     ord=6/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl
SR Status = 'Verified'                stage=DevStg-Impl     ord=6/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl
SR Status = 'Planned'                 stage=DevStg-Impl     ord=6/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl
SR Status = 'Bananas'                 stage=DevStg-Impl     ord=6/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl
SR Status = 'Approvd'                 stage=DevStg-Impl     ord=6/8  computed=DevStg-Tests  bar=DevStg-Tests  stage_to_bar=DevStg-Impl

--- the bar ceiling, directly ---
sr_bar(Approved, has_llr=True, has_tc=True) = DevStg-Tests
sr_bar(Founded,  has_llr=True, has_tc=True) = DevStg-Tests
_RELEASE_CEILING = DevStg-Tests
bar_label(DevStg-Tests) = DevStg-Tests (Release: pending harness driver)
```

The only inputs that reach `stage=DevStg-Impl` are Status cells outside the
closed enum — every one of which the always-on integrity floor reds
independently.

### This is already known and pinned — it is not a new discovery

`tests/test_ratification_level.py:359`
(`test_an_unverified_SR_over_AUTHORED_tests_is_the_IMPL_rung`) pins exactly this,
and its docstring at `:373–386` states it in the repo's own words:

> "D-9 STEP 5 MADE THIS RUNG UNREACHABLE-BY-CELL, AND THAT IS RECORDED HERE
> RATHER THAN PAPERED OVER. […] **This is the STAGE-axis twin of the hazard
> OI-30 D2 ruled a ceiling for on the BAR axis, and the ceiling covers only the
> bar**: a repo whose SRs are all ex-`Planned` now reads DevStg-Release where it
> used to read DevStg-Impl. NAMED FOR THE SITTING (log 2026-08-15m), not fixed
> here."

The assertions at `:399–402` pin `Approved`/`Founded` → `STAGE_RELEASE` and the
out-of-vocabulary `Modified` → `STAGE_IMPL`. My independent demonstration
reproduces both arms exactly.

### What this means for the owner's preferred shape

| Rule as written | Reachable today? | Why |
|---|---|---|
| "we are **IN** `DevStg-Impl`" (equality) | **NO** | rung 6 is vacant; only an integrity error puts a repo there |
| "we are **in or above** `DevStg-Impl`" (`stage_ord >= 6`) | **YES** | satisfied by `DevStg-Release` (ord 7), which a settled spine does reach |

So the owner's preferred shape **dissolves OI-51's unreachability — but only in
its at-or-above form, and only by stepping over a rung nothing can legally
occupy.** Two consequences follow, and both are facts rather than
recommendations:

1. **The at-or-above phrasing is load-bearing, not stylistic.** The owner's own
   words are "in or above", so the shape as stated works. An implementation that
   compared for equality would inherit the unreachability from a second,
   independent cause and OI-51 would recur with a different explanation.
2. **The state the owner describes has no rung reporting it.** The owner's OI-51
   framing was: "once the test registries are Founded the spine is broken down,
   DevStg goes to implementation, and these checks should run in parallel." On
   today's ladder a `Founded` spine reports `DevStg-Release` —
   *"nothing in work; release checklist available"* (`derive_gate.py:585`) —
   during exactly the period implementation is in work. The at-or-above test
   still fires, so the checks would run; but the reported stage during that
   period is not `DevStg-Impl`.

**Asymmetry summary:** the OI-30 D2 ceiling ceilings the **bar** and nothing
else. The **stage** is not ceilinged — it is *vacated at one rung* by the D-9
step-5 vocabulary fold. A stage-keyed re-key inherits a different, narrower
problem than the one it dissolves.

---

## THE CENSUS TABLE

### `project-trajectory/scripts/derive_gate.py` — the producer of both axes

| Site | Decides | Reads | Class | Under an at-or-above stage rule |
|---|---|---|---|---|
| `:390` `sr_bar` | each SR's bar contribution; ceilinged at `BAR_TESTS` (`:400`) | SR rows | **A** | unchanged — it produces the bar, which remains the ratification record |
| `:404` `maturity_bar` | LLR/TC bar contribution | rows | **A** | unchanged |
| `:473` `sn_bar` | SN bar contribution (WI-401 coverage rung) | rows | **A** | unchanged |
| `:1043` `_raw_level` | the min-fold → raw bar | rows | **A** | unchanged |
| `:1230` `compute()["gate"]` | floors raw to `DevStg-Reqs`, the runnable value | raw | **A** | unchanged |
| `:1234` `_per_phase` | per-phase bar (unfloored) | rows | **A** | unchanged |
| `:376` `bar_label` | appends the ceiling note for humans | bar name | **A** *(display)* | unchanged |
| `:810` `boundary_incomplete` | rung 1 — is the boundary inventory in work? | `external.toml` | **B** | unchanged — already the target shape |
| `:856` `arch_incomplete` | rung 3 — is the partition in work? | `components.toml` | **B** | unchanged |
| `:888` `spine_stage` | **THE current stage** | rows | **B** | becomes the primary selector input for the whole kit |
| `:1206` `compute()["stage"/"stage_ord"]` | publishes stage + derived ordinal | `spine_stage` | **B** | unchanged |
| `:1000` `STAGE_BAR` / `:1012` `stage_to_bar` | maps a stage to the next bar to clear | stage | **C** | **the axis-crossing site.** Its own docstring (`:1029–1033`) says nothing derives the bar from the stage in production — it is a reader's reconciliation only |
| `:1286` `basis_line` / `:1390` `render_cache` / `:1396` | the CARRIER — writes the bar as the machine value and the stage as a comment field | both | **C** | **structural obstacle: see below** |

**The carrier asymmetry (`docs/gate`).** The file is headed `# DERIVED BAR`
(`derive_gate.py:1360`), its **machine-readable last line is the bar**
(`:1396`), and the **stage exists only as a substring of the `# basis:` comment**
(`:1341`). Every bar consumer reads a whole line; the one stage consumer
regex-scrapes a comment (`agent_common.py:783`). A stage-keyed re-key must
either promote the stage to a machine line or make comment-scraping the norm.

### `project-trajectory/scripts/check.py` — the harness selector (bar-keyed throughout; reads the stage NOWHERE)

| Site | Decides | Reads | Class | Under an at-or-above stage rule |
|---|---|---|---|---|
| `:1484` `resolve_gate` | which step plan runs; hard-exits on an unknown value (`:1493`); `all` when the file is absent (`:1500`) | `docs/gate` last line (**bar**) | **A** | would read `stage=` instead |
| `:1349` `resolve_plan` | **the primary step-selection decision**: `gate in s[3]` — set MEMBERSHIP | resolved bar | **A** | membership → threshold; see the note below |
| `:603–605` `format`, `lint`, `tests+coverage` tagged `{BAR_RELEASE}` | **OI-51's exact site** — the three product checks | tag | **A** | would become `>= DevStg-Impl`, which an at-or-above rule reaches |
| `:634`–`:966` the other 23 built-in step tags | step inclusion (see the full listing below) | tags | **A** | each tag set becomes a threshold rung |
| `:374–387` `extra_steps` `gates=` loader; `fallback=BAR_RELEASE` (`:375`) | adopter-declared step inclusion; **the default for an undeclared step is `DevStg-Impl`** | `docs/stack.ini` | **A** | the declared vocabulary moves to stage rungs |
| `:495–506` `if gate in (BAR_RELEASE, "all")` | appends `--require-verified`, `--strict-schema`, `--phase` to the trace command | resolved bar | **A** | threshold on the stage |
| `:551–554` `if gate in (BAR_TESTS, BAR_RELEASE)` | promotes trajectory/vocab/backlink checks WARN→ERROR | resolved bar | **A** | threshold on the stage |
| `:1277` `product_floor` | the WI-473 monotonic product floor | `ex-draft=` (**a bar counterfactual**) | **A** | needs a stage counterfactual, which `basis_line` does not emit today |
| `:1314` `floor_plan` | restores product steps the derived bar dropped | `ex-draft` vs gate | **A** | as above |
| `:1429`/`:1439` `advisory_plan` | the advisory tier at higher bars | resolved bar | **A** | threshold on the stage |
| `:1017` `bar_ord` / `:984` `BAR_ORDER` | the only legal bar ordering | — | **A** | `stage_ord` already exists as the analogue |
| `:1038`/`:2200` `_resolve_bar_alias` | translates retired `G*`/`DevBar-*` and warns | argv | **A** | a third alias generation would be owed |
| `:1509` `_step_gate` | a DEFAULTED gate resolves to `all`, never `docs/gate` — keeps the pre-commit floor warn-first | argv | **A** | unchanged in spirit |
| `:2092` `--stage-cleared` / `--gate` flag | the override | argv | **C** | **see C-1 below** |
| `:1198` `window_open` | **whether the advisory tier exists at all** | `drafted=`, `modified=`, `ex-draft=` vs `computed=` | **C** | **see C-2 below** |

**Built-in step tags, as `check.py --gate all --list` reports them** (measured,
not read off the source):

| Bar tag | Steps |
|---|---|
| `{DevStg-Impl}` only | `format`, `lint`, `tests+coverage`, `doc-refs`, `figures`, `module-coverage`, `perf-budgets`, `trajectory-map`, `status-map`, `open-items`, `okf`, `skills-sync` |
| `{DevStg-Tests, DevStg-Impl}` | `traceability`, `design-flows`, `trajectory`, `backlink-coverage`, `ratify-fresh` |
| `{DevStg-Reqs}` only | `registry-integrity` |
| all three | `derived-gate`, `vocabulary`, `need-form`, `privacy`, `doc-navigability`, `skills-index`, `prompt-catalog`, `staged-divergence` |

**Selection is MEMBERSHIP, not a threshold — and that is stated deliberately.**
`check.py:1310` records it: *"Selection is MEMBERSHIP at the floor, not 'any bar
at or below it', because that is how the gate itself selects (`registry-integrity`
is tagged `{DevStg-Reqs}` and genuinely does not run at DevStg-Impl)."* So the
owner's "at or above" rule is **not a relabel of the current mechanism** — it
changes step selection from set membership to an ordering test, and
`registry-integrity` is the live row that would change meaning.

### `project-trajectory/scripts/agent_common.py` — the ratification dial (stage-keyed throughout)

| Site | Decides | Reads | Class | Under an at-or-above stage rule |
|---|---|---|---|---|
| `:760` `spine_stage_of` | **THE stage reader for the whole loop** — regex-scrapes `stage=(DevStg-[A-Za-z]+)` out of the `# basis:` comment (`:783`); `None` on a pre-OI-21 cache | basis comment | **B** | **already the target shape**; would gain many more callers |
| `:649` `human_holds` | whether work at the current rung is the human's to ratify; unknown rung → held (`:654`) | stage + dial | **B** | unchanged |
| `:567` `DIAL_HOLDS` | level → held-rung sets; `4: None` = holds everything | — | **B** | unchanged |
| `:689` `human_approves` + `:613` `APPROVAL_RUNGS` | whether a machine may move an off-spine `status` cell; unmapped → held (`:690`) | stage rung + dial | **B** | unchanged — OI-30 D3 already ruled this derives from the stage ladder |
| `:503` `ratification_level` | the 0–4 int dial | `docs/process.toml` | **B** | WI-493 (deferred) re-keys this to `DevStg-*` strings |
| `:554` `LADDER_RUNGS` | the recognized-rung vocabulary | — | **B** | unchanged |

### The loop layer — every site already stage-keyed

| Site | Decides | Class |
|---|---|---|
| `dispatch.py:1290` | `human_held` computed once per run from `human_holds(spine_stage_of())` | **B** |
| `dispatch.py:309` `_kind_action` | `attestation`/`gate` kinds → `surface` when human-held, else `exclusive` | **B** |
| `dispatch.py:370` `_admission` | partitions the frontier into surfaced vs dispatchable | **B** |
| `agent_loop.py:2952` | `human_held` for the session | **B** |
| `agent_loop.py:2324`/`:2378` | whether an escalation stops the run | **B** |
| `agent_loop.py:3068` | the dual-plan page outcome (`stop-needs-human`) | **B** |
| `agent_route.py:955` `failure_action` | the escalation mode | **B** |
| `plan_round.py:315` `page_action` | the PAGE disposition; `None` → held (`:326`) | **B** |
| `intake.py:1443` | `human_held` for the flip path | **B** |
| `intake.py:1402` `adjudication_action` | `recommend` vs `flip` — whether adjudication may move a spine Status | **B** |

### `intake.py` / `integrate.py` — the WI `bar:` frontmatter (bar-keyed)

| Site | Decides | Class |
|---|---|---|
| `intake.py:97` `WI_BARS`, `:113` `normalize_bar`, `:968` mint refusal | a WI may declare the bar its refresh runs at | **A** |
| `intake.py:480` `_gate_moved` | compares `docs/gate`'s first line across two git trees | **A** |
| `intake.py:242` `tier_signal` | a moved bar mints a `strong` adjudication row | **A** |
| `integrate.py:1446` `_BAR_GATES`, `:1467` `_normalize_bar` | the lane's bar vocabulary | **A** |
| `integrate.py:1588` `_lane_bar_directives` | refuses a refresh on an unknown declared bar | **A** |
| `integrate.py:1608` | `strictest = max(bars, key=_BAR_GATES.index)` — the bar a lane's refresh runs at | **A** |
| `integrate.py:1412` `_run_bar` | `if gate: argv += ["--gate", gate]` — where a WI's declared bar reaches `check.py` | **A** |

### `check_trajectory.py` / `trace.py`

| Site | Decides | Class |
|---|---|---|
| `check_trajectory.py:1823` `read_derived_phases` | parses `per-phase=` bars; unknown values silently dropped (`:1836`) → detector goes vacuous | **A** |
| `check_trajectory.py:1886` `phase_findings` | **the phase-drop warn** — compares the current per-phase bar against the level a CLOSED phase anchor recorded | **A** |
| `check_trajectory.py:1802` `_ANCHOR_LEVEL` | accepts the retired `g1`/`g2` anchor spellings in WI titles forever | **A** |
| `trace.py:4181`/`:4220` `--require-verified` | the `DevStg-Impl` approval criterion; joins the exit code at `:5025` | **A** |
| `trace.py:5140` `--no-placeholders` | leftover `-000` rows, "use from DevStg-Tests on" | **A** |

### Dashboard and status surfaces

| Site | Decides | Reads | Class |
|---|---|---|---|
| `traj_parse.py:450` `_gate_value` | the bar for the Process tab | bar | **A** *(display)* |
| `traj_panels.py:885` `process_panel` | **whether the Process tab exists at all** | bar | **A** *(display)* |
| `traj_status.py:389–405` `_stage_line` | renders **"In stage: X (stage N of 8, …) · next to clear: Y"** | **both** | **A + B** *(display; counted once in each)* |
| `traj_panels.py:918` | `now = gate in span.split("→")` — marks which lifecycle tier is "now" | bar | **C** — **see C-3** |
| `traj_panels.py:1043` | renders `"Next stage to clear: <gate>"` **raw**, bypassing `bar_label` | bar | **C** — **see C-5** |

`traj_status.py:389` is the one surface in the kit that gets the vocabulary
exactly right, and it is where `docs/status.md:117` comes from.

### Configuration

| Site | Declares | Class |
|---|---|---|
| `docs/stack.ini:487` `[step:doc-refs]` | `gates = DevStg-Impl` | **A** |
| `docs/stack.ini:503` `[step:figures]` | `gates = DevStg-Impl` | **A** |
| `docs/stack.ini:532` `[step:module-coverage]` | `gates = DevStg-Impl` | **A** |
| `stack.ini.template:181–188` | the `gates=` contract and its **default of `DevStg-Impl`**; ships **no `[step:*]` section at all** | **A** |
| `process.toml.template:250–254` | `backlink-coverage` exists from `DevStg-Tests` on | **A** |
| `docs/process.toml:69` | `human_ratification_through = 4`; the comment at `:50–52` states the semantics as *"compares the IN-PROCESS stage of a row against this number"* | **B** |
| `process.toml.template:95` | the shipped default | **B** |
| `docs/process.toml:70–82` | the `APPROVAL_RUNGS` derivation (OI-30 D3), explicitly "A COMMENT, NOT A KEY" | **B** |

### CI

| Site | Decides | Class |
|---|---|---|
| `ci/check.yml:79` push → `check.py --tier smoke`, **no `--gate`** | selects by the derived bar — **OI-51's live adopter path** | **A** |
| `ci/check.yml:83` pull_request → `--tier full`, **no `--gate`** | selects by the derived bar — **OI-51's live adopter path** | **A** |
| `ci/check.yml:89` tag → `--gate all --tier release` | the one path that forces every step | **A** |
| `.github/workflows/test.yml:162` | this repo's own gate job, no `--gate` | **A** |

### `project-trajectory/agent-hooks/` — a clean negative

No hook reads gate or stage state. `claude.settings.json:9` invokes
`subagent_gate.py`, which reads the `[checks] subagent_gate` **spawn dial** and
no bar or stage (confirmed: `subagent_gate.py` contains zero `DevStg-` or
`docs/gate` references). The `Stop` hook runs the always-on integrity floor
ungated. Recorded so the word "gate" here is never miscounted.

### Tests that pin one semantics as the contract

| Site | Pins | Class |
|---|---|---|
| `tests/test_ratification_level.py:359–404` | **the vacant rung 6** — `Approved`/`Founded` → `STAGE_RELEASE`, only out-of-vocabulary reaches `STAGE_IMPL` | **C** |
| `tests/test_ratification_level.py:658–680` | `stage_to_bar` = the next bar you must clear; rungs 0–2→Reqs, 3–5→Tests, 6–7→Impl | **C** |
| `tests/test_dispatch.py:663–694` | **a WI must pin its own `bar: DevStg-Impl`** because a fully-approved scaffold no longer derives it | **C** |
| `tests/test_ratification_level.py:74–118` | per level, exactly which rungs `human_holds` holds; top two rungs held by level 4 alone | **B** |
| `tests/test_derive_gate.py:753–788` | the OI-30 D2 ceiling; no SR row of any live shape reaches `BAR_RELEASE` | **A** |
| `tests/test_product_floor.py:184–232` | the floor is dormant for the built-ins and says so; fails the day either half moves | **A** |
| `tests/test_check_harness.py:514–557` | the default gate comes from `docs/gate`; explicit `--gate` wins; a retired `G2` in the file is REFUSED | **A** |
| `tests/test_stack_profile.py:206–260` | `gates=` membership; the default bar is `["DevStg-Impl"]`; sorting by `bar_ord`, never lexically | **A** |
| `tests/test_pre_commit_hook.py:175–207` | a defaulted gate keeps the trajectory floor warn-first | **A** |

**Guards** (enforce vocabulary; consume no state, so counted separately):
`tests/test_stage_ladder.py:68–105` bans lexical ordering of any ladder value in
every kit script — and `:87` proves the grep bites. `tests/test_stage_ladder.py:111–139`
pins `check.BAR_ORDER`, `derive_gate.BAR_ORDER`, `intake.WI_BARS` and
`integrate._BAR_GATES` equal.

### Skills

| Site | Frames behavior as | Class |
|---|---|---|
| `skills/gate-advance/SKILL.md:11`, `:56–66`, `:133–158` | clearing a bar; `docs/gate`'s first line is the bar to next clear; "what each bar takes" | **A** |
| `skills/gate-advance/SKILL.md:24–47` | the eight-rung ladder; **"A stage is a state, a bar is an event"**; the ladder is not monotonic | **B** |
| `skills/registry-hygiene/SKILL.md:20`, `:27`, `:30`, `:36`, `:42` | strictness per bar (`DevStg-Tests+`, `DevStg-Impl`) | **A** |
| `skills/session-protocol/SKILL.md:96` | the "gate bar" is `check.py --gate <gate>` | **A** |

---

## The most interesting C-class sites

**C-1 — `check.py:2092`, the `--stage-cleared` flag's tense.** The flag was
renamed from `--gate` by owner ruling 2026-08-18 so the token would say which
reading it means. Its help text (`:2099`) says *"the stage being CLEARED, not the
one in work"* — present progressive, i.e. the stage you are **trying** to clear
and have **not** cleared. But the flag *name* reads as a past participle: "stage
cleared". `docs/gate`'s own header calls the same value *"the bar that must next
be CLEARED"*. So the value is a **future** clearance and the name reads as a
**past** one. This is the vocabulary trap the owner's question is pointing at,
surviving inside the very rename that was meant to remove it.

**C-2 — `check.py:1198` `window_open`, a draft count standing in for the stage.**
Decides whether the advisory tier exists at all, by comparing `ex-draft=` against
`computed=` and counting `drafted=`/`modified=`. The question it is really
asking is *"is this repo mid-redrafting?"* — which is precisely what the stage
axis answers directly (a Drafted row drops `stage` to `DevStg-Reqs`). It answers
it instead with a bar counterfactual plus a row count. Twelve gate steps stop
running silently when this detector goes blind — the measured 2026-07-26/27
precedent named in `derive_gate.py:1319–1327`.

**C-3 — `traj_panels.py:918`, a next-to-clear bar rendered as "now".**
`now = gate in span.split("→")` marks a lifecycle tier as the current one using
the **bar**, whose documented meaning is what must *next* be cleared. This is the
owner's complaint made literal on the dashboard: the value that says "where you
are going" is used to paint "where you are". `traj_status.py:389` does the same
job correctly by reading `stage=`, so the two surfaces answer the same question
from different axes.

**C-4 — `tests/test_dispatch.py:663–694`, a WI hardcoding a bar the repo cannot
derive.** The fixture is `scaffold_with_queued_wi(tmp_path, bar="DevStg-Impl")`
*precisely because* a fully-approved scaffold no longer derives `DevStg-Impl`
under the ceiling, and `tests+coverage` is `DevStg-Impl`-only. This is OI-51's
defect already being routed around in the test suite by declaring the clearance
that cannot be derived — the workaround, pinned.

**C-5 — `derive_gate.py:1286`/`:1396` vs `agent_common.py:783`, the carrier
asymmetry.** `docs/gate`'s machine line is the bar; the stage is a substring of a
comment. Every bar consumer reads a line; the sole stage consumer regex-scrapes a
comment, and `agent_common.py:783` requires `stage=DevStg-<Alpha>` — a label with
a digit or hyphen reads `None`, which holds everything. Any stage-keyed re-key
runs through this seam.

*(Runner-up: `derive_gate.py:1012` `stage_to_bar` — the declared axis-crossing
table, pinned by a test, called by nothing in production. It is the reconciliation
a stage-keyed re-key would either delete or promote.)*

---

## What a stage-keyed re-key would touch

Factual list only. No recommendation; the ruling is the owner's.

### Sites that would change (bar → current-stage, at-or-above)

**The harness selector — the whole of it.**
`check.py:1484` (`resolve_gate`), `:1349` (the primary selection),
`:495–506` and `:551–554` (the two strictness promotions), `:1277`/`:1314`
(the product floor), `:1429`/`:1439` (the advisory tier), `:1017`/`:984`
(the ordering vocabulary), `:1509` (`_step_gate`).

**Every step tag — 26 built-ins plus the adopter contract.**
`check.py:603–605` (OI-51's three), `:634`–`:966` (the other 23),
`:374–387` (the `gates=` loader and its `DevStg-Impl` default),
`docs/stack.ini:487`, `:503`, `:532`, and `stack.ini.template:181–188`.
Note that selection is **membership** today (`check.py:1310`), so this is a
semantics change and not a relabel — `registry-integrity`, tagged `{DevStg-Reqs}`
and deliberately not running at `DevStg-Impl`, is the row that changes meaning.

**The WI `bar:` frontmatter and the lane refresh.**
`intake.py:97`/`:113`/`:968`/`:1156`, `integrate.py:1446`/`:1467`/`:1588`/`:1608`/`:1412`,
`wi_convert.py:160`. Pinned equal by `tests/test_stage_ladder.py:124–139`.

**The carrier.** `derive_gate.py:1286`/`:1390`/`:1396` — the stage would need to
become a machine-readable value rather than a comment field, and
`agent_common.py:783`'s regex scrape would be replaced. `derive_gate.py:1000`/`:1012`
(`STAGE_BAR`/`stage_to_bar`) is either deleted or promoted from reconciliation to
production path.

**Display.** `traj_panels.py:918` and `:1043`, `traj_parse.py:450`,
`traj_status.py:389–405`.

**CI inherits automatically.** `ci/check.yml:79`/`:83` and
`.github/workflows/test.yml:162` pass no `--gate` at all, so they follow whatever
`resolve_gate` resolves. Only `ci/check.yml:89` (`--gate all`) names a value.

**Tests that would need re-pinning.** `tests/test_check_harness.py:514–557`,
`tests/test_stack_profile.py:206–260`, `tests/test_pre_commit_hook.py:175–207`,
`tests/test_product_floor.py:184–232`, `tests/test_dispatch.py:663–694`,
plus the two guards at `tests/test_stage_ladder.py:68–105` and `:111–139`.

**Docs and skills.** `skills/gate-advance/SKILL.md` (`:11`, `:51`, `:56–66`,
`:133–158`), `skills/registry-hygiene/SKILL.md` (`:20`, `:27`, `:30`, `:36`, `:42`),
`skills/session-protocol/SKILL.md:96`, `PROCESS.md:532`, `ADOPTING.md:104`.
A RESYNC_PACK entry would be owed for every adopter.

### Sites already stage-keyed — no change

All **27 B-class sites**. The whole ratification-authority layer already does
exactly what the owner describes, and it was ruled that way twice:

- `agent_common.py:649` `human_holds` — the one comparison, stated once, reading
  `spine_stage`'s answer. Its docstring records that the retired form was
  `stage < level` over two integer ladders and that OI-21 replaced it with a
  declared lookup.
- `agent_common.py:689` `human_approves` + `:613` `APPROVAL_RUNGS` — **OI-30 D3
  is the precedent for the owner's whole preference.** The owner's words there:
  *"I thought this would follow the dev-stage directly? Why build a new enum?"*
  A proposed declared list was overturned for a derived stage-rung lookup.
- `derive_gate.py:810`/`:856` — the two inserted rungs read registry state
  directly, with an applies-when.
- `dispatch.py:1290`/`:309`/`:370`, `agent_loop.py:2952`/`:2324`/`:3068`,
  `agent_route.py:955`, `plan_round.py:315`, `intake.py:1443`/`:1402`.
- `docs/process.toml:69` and its comment at `:50–52`, which already states the
  semantics in the owner's own terms: *"compares the IN-PROCESS stage of a row
  against this number."*
- `WI-493` (deferred, `docs/work/deferred/WI-493-dial-rekeys-to-stage-strings.md`)
  re-keys the dial's **vocabulary** from the 0–4 ordinal to `DevStg-*` strings.
  Same family, already directed by the owner, explicitly deferred until woken.
  It changes the dial's spelling, not its axis — that axis is already the stage.

### Behavior that genuinely needs clearance semantics

Four sites, each with its reason:

1. **`check_trajectory.py:1886` `phase_findings` — the phase-drop detector.**
   It compares the current per-phase level against **the level a CLOSED phase
   anchor recorded**. That is irreducibly a comparison against a *past*
   clearance: the finding is "this phase has fallen below what it once reached".
   A current-state read cannot express it — there is no current value that
   remembers a previous one. This is the one detector that needs a high-water
   record.

2. **`intake.py:480` `_gate_moved` + `:242` `tier_signal`.** Asks whether the
   derived value **moved between two git trees**, and mints a `strong`
   adjudication row when it did. Inherently a delta across time, not a state
   read. It would work equally well on the stage axis — but it stays a
   two-point comparison either way, never an at-or-above test.

3. **The ratification acts themselves — `dispatch.py:309` `_kind_action` for the
   `attestation` and `gate` WI kinds.** Clearing a bar is an **event that moves
   the stage**; it cannot be selected purely by the stage it produces, or the
   rule is circular. Note the honest nuance: this site is *already stage-keyed*
   — `human_holds` decides who performs the act from the current rung. So what
   needs clearance semantics is the act's **recording**, not its **selection**.
   `PROCESS.md`'s ruled model already draws exactly this line:
   *"a stage is a state, a bar is an event"* (`skills/gate-advance/SKILL.md:24–26`).

4. **`derive_gate.py:390` `sr_bar` and the OI-30 D2 ceiling.** The bar remains
   the record of what a human has certified, and the ceiling remains the guard
   rail that a Status cell may not claim the evidence passed. Nothing in a
   stage-keyed selector touches this; the ceiling constrains what may be
   *claimed*, not what may be *run*. That separation is precisely what OI-51's
   recommendation calls "moving a different axis".

Everything else in the A column is a **selector**, and a selector is exactly
what the owner's rule addresses.

---

## Incidental findings (out of census scope; recorded, not acted on)

Surfaced by the sweep, unrelated to the ruling, each a claim to confirm before
anyone acts on it:

1. **`tests/test_ratification_level.py:779` names a template path that does not
   exist** — `project-trajectory/process.template.toml`, where the real file is
   `project-trajectory/process.toml.template`. With the `path.exists()` guard at
   `:781`, the template half of the `human_approval_registries` pin silently
   never runs.
2. **`traj_panels.py:1043` renders the raw bar** while `traj_status.py:389` goes
   through `derive_gate.bar_label`. `_stage_line`'s docstring claims this surface
   and `PROJECT_STATE.html` "cannot disagree" — but the dashboard's Process tab
   does not call `bar_label`, so the OI-30 D2 ceiling note appears in
   `docs/status.md` and not on the dashboard.
3. **`.github/workflows/test.yml:132–133`** states the ceiling in prose that no
   test pins. If the ceiling lifts, five tests go red and this comment goes stale
   silently.
4. **Three bar-ordinal tables with different domains** — `check.BAR_ORDER` (3,
   raises), `check._window_ord` (4 incl. `DevStg-Below`, degrades to `-1`),
   `check_trajectory._BAR_LEVEL` (4, silently drops unknowns). A new bar name
   would be silently dropped by `check_trajectory.py:1836` and read as the floor
   by `check.py:1101`.
5. **Five independent retired-literal tables** — `derive_gate.py:164`,
   `check.py:1005`, `intake.py:98`, `integrate.py:1451`,
   `check_trajectory.py:1802`. Only the first two are pinned equal to each other.

---

## Method note

The stage-reachability result was produced by driving `derive_gate`'s own
functions (`spine_stage`, `_raw_level`, `sr_bar`, `stage_ord`, `stage_to_bar`)
over synthetic in-memory spines from a throwaway script in the session
scratchpad — never in the repo, and nothing in the tree was modified. The step
table was measured by running `python project-trajectory/scripts/check.py
--gate all --list` rather than parsing the source tuples. Everything else is a
direct read at the cited `file:line`.
