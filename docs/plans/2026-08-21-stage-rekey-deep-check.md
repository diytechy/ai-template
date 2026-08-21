# Stage re-key deep check — the owner's three questions on OI-51 option (e)

**Status:** verified analysis only. This document REPAIRS NOTHING and recommends
nothing. It answers three questions the owner asked mid-ruling on OI-51 option
(e) and stops there; the ruling is the owner's.

**Foundation:** [`docs/plans/2026-08-21-bar-vs-stage-census.md`](2026-08-21-bar-vs-stage-census.md)
(yesterday's census). That census is not redone here. Where this document
*corrects* it, the correction is marked.

**As of:** branch `requirements/ears-and-quality-characteristics`, HEAD `b2cb0b1e`,
clean tree, 2026-08-21. `docs/gate` basis at that commit:

```
# basis: SN=27 SR=73 LLR=165 TC=161 drafted=9 uncovered=0 computed=DevStg-Below
  ex-draft=DevStg-Reqs phase=5 per-phase=1=DevStg-Tests;3=DevStg-Tests;4=DevStg-Reqs;5=DevStg-Below
  stage=DevStg-Reqs stage-ord=2 stage-of=8
DevStg-Reqs
```

**Method.** Every claim below is either a direct read at the cited `file:line`,
or a DRIVEN result — `derive_gate`'s and `agent_common`'s own functions called
over synthetic in-memory spines and temp scaffolds from throwaway scripts in the
session scratchpad. Nothing in the tree was modified; no test was edited. The
step table was MEASURED (`check.py --gate all --list`), not read off source
tuples. Driven blocks are labelled **D1**–**D10** and their raw output is
reproduced verbatim.

---

# Q1 — "What all does this expose?"

> "DevStg-Tests should jump to DevStg-Impl once everything is founded; release
> can only be verified if all test cases are passing."

Read as a proposal to **re-discriminate the top of the ladder**: all-Founded ⇒
the repo is IN `DevStg-Impl`; `DevStg-Release` requires **test evidence** (all
TCs passing), not status cells.

## Q1(a) — the discriminator change, and what evidence exists today

### The discriminator, as it stands

`derive_gate.spine_stage` (`derive_gate.py:888`) is a fall-through of rungs. The
two lines at the top of the ladder are:

- `derive_gate.py:991` — `if not all(is_approved(r) or is_founded(r) for r in srs): return STAGE_IMPL`
- `derive_gate.py:993` — `return STAGE_RELEASE`

`spine_stage`'s own docstring already flags this as an interim
(`derive_gate.py:932–936`):

> "CAVEAT ON THE Impl→Release DRIVER. DevStg-Impl ends when every SR reads
> `Approved`, which is a registry CELL, not a harness run. The intended signal is
> the harness (green tests at the declared tier and coverage); the cell is
> today's interim proxy for it, and repo-lock D-9's correction owes the swap to a
> later batch. Nothing here should be read as proof the tests passed."

**The owner's proposal is that swap.** Under it the two lines become roughly:

| | today | under the proposal |
|---|---|---|
| rung 6 `DevStg-Impl` entry | some SR not `Approved`/`Founded` | **every SR `Approved`/`Founded`** (all-Founded ⇒ IN Impl) |
| rung 7 `DevStg-Release` entry | every SR `Approved`/`Founded` | **test evidence: every TC passing** |

This is a **polarity inversion at rung 6**, not a tightening. Today rung 6 means
"the spine is NOT yet blessed"; under the proposal it means "the spine IS
blessed and the code is being made to pass". The proposal's reading is the one
the rung was originally inserted for (`tests/test_ratification_level.py:360–367`,
citing `docs/archive/plans/2026-08-11-stage-gate-semantics.md §3`), and it is the
reading that would **re-occupy the vacant rung** — see D1 and Q1(c).

### Is this the OI-30 D2 harness driver's stage-axis half?

**Yes — and that is the most decision-relevant fact in Q1.**

OI-30 D2's ceiling is stated at `derive_gate.py:334–364`, and its exit condition
is explicit at `:360–363`:

> "HOW IT LEAVES. Delete these three lines and the `_RELEASE_CEILING` flag when
> the harness driver lands."

The driver's job, as D2 defines it, is exactly what the owner asks for:
`derive_gate.py:51` — *"`DevStg-Impl` is unreachable-by-cell until the harness
driver computes it from test evidence"*; the human-facing note it leaves behind
is `_CEILING_NOTE = "(Release: pending harness driver)"` (`derive_gate.py:373`).

So the owner's proposal is **not a new subsystem**. It is the ruled long-term
path (OI-51 option (b), `open-items.toml:2046`), stated on the *stage* axis
instead of the *bar* axis. Both axes need the same missing input: a machine
reading of "did the tests pass".

### What evidence source exists today for "all test cases are passing"

**None. Verified across four independent places; every one is deliberately
empty.**

1. **The TC row schema has no outcome field, by ruling.** The closed TC key set
   is `spine_carrier.py:344–355`:
   `verifies, level, method, tier, parameters, expected, automated, evidence, status, phase`.
   Column side: `trace.py:365–374`. There is no `result`, `outcome`, `pass`,
   `last_run` or `verdict` key. `Status` is a closed authoring enum
   `{Drafted, Approved, Founded}` (`trace.py:431`), and the prohibition is
   written into the code at `trace.py:186–198`:

   > "`Verified` used to make TWO claims at once — the text is ratified AND the
   > evidence passed … D-9 deletes the pass claim from the vocabulary: `Approved`
   > says only that the text is blessed, and **whether the tests pass is the
   > harness's answer, not a cell's**."

   Restated at `trace.py:3009–3012` and `docs/registry-machinery-reference.md:194`.
   The `evidence` cell is a **locator**, validated for presence only
   (`trace.py:1667–1680`) — nothing reads it back.

2. **`docs/test/` holds no results artifact.** `git ls-files docs/test/` returns
   exactly one file, `docs/test/test-cases.toml`. `docs/test/report.md` and
   `report.html` are gitignored (`.gitignore:12–13`) and are *traceability*
   reports, not test-result reports — every TC line renders the authoring
   `Status` (`trace.py:3498`; e.g. `docs/test/report.md:174`
   `- TC-001 [Approved] — …`). No PASS/FAIL, no timestamp, no counts.

3. **`check.py`'s `tests+coverage` step leaves nothing durable.** Step at
   `check.py:605`; command built at `check.py:444–484`; default coverage args
   `check.py:180–182` are **term-only** (`--cov-report=term-missing`), so the
   shipped default emits no file at all. This repo's own profile adds
   `--cov-report=json` (`docs/stack.ini:471`), producing `coverage.json`
   (`check.py:211`) — which is (i) coverage percentages, never per-test
   pass/fail, (ii) gitignored (`.gitignore:6–8`), and (iii) **actively deleted
   before any run that would produce it**, `_clear_stale_coverage_report`
   (`check.py:2053–2071`, called at `:2292`). The reasoning is stated at
   `check.py:1116–1123`: *"Stale evidence reported as current is worse than no
   evidence."* There is **zero** junit/XML/`--json-report`/`--report-log`
   anywhere in the repo.

4. **No result parser exists.** The only report-parsing script is
   `check_coverage.py`, and it parses `summary.percent_covered` per source file
   (`check_coverage.py:19–24`) — coverage, not outcomes.

**What exists vs what would have to be built:**

| | exists today | would have to be built |
|---|---|---|
| a TC-level pass/fail record | — | a result field or a side-car results artifact, plus the ruling that lets a *derived* artifact carry it (a cell may not — `trace.py:186–198`) |
| a durable machine-readable run artifact | `coverage.json`, coverage-only, gitignored, deleted per run | a persisted, TC-joinable result file (junit/json) |
| a join from a run back to a TC id | — | the `evidence` locator would have to become a *read* key, not just a presence-checked string |
| a consumer that derives a rung from it | — | the harness driver itself (`derive_gate.py:360–363`) |
| the ceiling that stands in for it | `_RELEASE_CEILING` (`derive_gate.py:364`), `bar_label` note (`:376–388`) | deleted when the driver lands |
| tests pinning its absence | `tests/test_derive_gate.py:756` (*"DELETE THIS TEST DELIBERATELY, IN THE COMMIT THAT LANDS THE HARNESS DRIVER"*), `:796`, `:814`, `:829`; `tests/test_traj_status.py:88`; `tests/test_ratification_level.py:383`, `:395`; `tests/test_product_floor.py:189` | these red on the day it lands, by design |

There is also a **bootstrapping order problem** specific to the owner's phrasing.
"Release can only be verified if all test cases are passing" requires the test
suite to have RUN. But `tests+coverage` is tagged `{DevStg-Impl}` only
(`check.py:605`, measured below), and under a stage-keyed at-or-above rule its
threshold would be rung 6. So: the repo must reach rung 6 for the tests to run,
and the tests must pass for the repo to leave rung 6 — which is coherent
(6 → 7 is the transition the evidence gates), **provided rung 6 is reachable**.
Under the owner's re-discrimination it is (all-Founded ⇒ rung 6), which is
precisely what makes the proposal self-consistent where the current ladder is
not. That is the strongest structural point in favour of the owner's shape.

## Q1(b) — every consumer that behaves differently at ord 6 vs ord 7

### The 27 stage-keyed ratification sites: **not one distinguishes them**

All four production readers of the stage funnel through a single comparison:

- `agent_loop.py:2952` — `human_held = agent_common.human_holds(docs, agent_common.spine_stage_of(root))`
- `dispatch.py:1290` — `human_held = ac.human_holds(root / "docs", ac.spine_stage_of(root))`
- `intake.py:1443` — `human_held = ac.human_holds(root / "docs", ac.spine_stage_of(root))`
- `plan_round.py:319` — consumes `human_held` from the same source

and `human_holds` (`agent_common.py:649`) is a membership test against
`DIAL_HOLDS` (`agent_common.py:567`). **DRIVEN (D8):**

```
rung (ord)         lvl0  lvl1  lvl2  lvl3  lvl4
DevStg-Needs  (0)  -     HELD  HELD  HELD  HELD
DevStg-Boundary(1) -     HELD  HELD  HELD  HELD
DevStg-Reqs   (2)  -     -     HELD  HELD  HELD
DevStg-Arch   (3)  -     -     HELD  HELD  HELD
DevStg-LLReqs (4)  -     -     -     HELD  HELD
DevStg-Tests  (5)  -     -     -     -     HELD
DevStg-Impl   (6)  -     -     -     -     HELD
DevStg-Release(7)  -     -     -     -     HELD

human_holds differs between DevStg-Impl(6) and DevStg-Release(7) at levels:
  NONE - identical at every dial level
```

`DIAL_HOLDS` (`agent_common.py:567–587`) holds `{}` at 0, and rungs 6 and 7 fall
together into the `4: None` "holds everything" short-circuit
(`agent_common.py:583–586`). **No dial setting separates them.** Every
downstream behavior therefore also fails to separate them:

| Site | Decides | ord 6 vs ord 7 |
|---|---|---|
| `dispatch.py:309` `_kind_action` | `attestation`/`gate` kinds → `surface` vs `exclusive` | identical |
| `dispatch.py:370` `_admission` | surfaced vs dispatchable frontier | identical |
| `agent_loop.py:2324`/`:2378` | whether an escalation stops the run | identical |
| `agent_loop.py:3068` | dual-plan page outcome (`stop-needs-human`) | identical |
| `agent_route.py:955` `failure_action` | escalation mode | identical |
| `plan_round.py:315` `page_action` | PAGE disposition | identical |
| `intake.py:1402` `adjudication_action` | `recommend` vs `flip` | identical |

`human_approves` + `APPROVAL_RUNGS` (`agent_common.py:689`, `:613`) likewise.
**DRIVEN (D9):** `APPROVAL_RUNGS = {'external': 'DevStg-Boundary', 'interfaces':
'DevStg-Arch', 'components': 'DevStg-Arch'}` — **no registry is governed by a
rung at ord 6 or 7 at all.**

> **Verdict for Q1(b), ratification half: the re-discrimination is behaviourally
> INERT for all 27 stage-keyed sites.** Whether a settled spine reports rung 6 or
> rung 7 changes no dispatch, no admission, no escalation, no approval authority,
> at any dial setting. This is a genuinely reassuring result: the blast radius of
> the owner's Q1 proposal, on the layer that is already stage-keyed, is **zero**.

### Displays and dashboards — where it *does* change

| Site | What changes at ord 6 vs 7 | Evidence |
|---|---|---|
| `traj_status.py:389–405` `_stage_line` | the rendered sentence: "stage 6 of 8, **implementation in work**" vs "stage 7 of 8, **nothing in work; release checklist available**" | `derive_gate.STAGE_DESC` (`derive_gate.py:577–586`); live output at `docs/status.md:117` |
| `docs/status.md:117` | the tracked, committed rendering of that line | direct |
| `PROJECT_STATE.html` Process tab | renders the same block (`traj_status.py:387–388` claims the two "cannot disagree") | see incidental finding 2 |
| `derive_gate.py:1206`/`:1221` `compute()` | `stage` + `stage_ord` on the basis line | `basis_line` `:1341` |

This is the whole practical effect, and it is exactly the vocabulary complaint
recorded for the owner in OI-51's second exchange (`open-items.toml:2050`):
during implementation the ladder today reports `DevStg-Release` —
*"nothing in work; release checklist available"* (`derive_gate.py:585`) — which
is the wrong sentence for the longest stretch of a project. The owner's
re-discrimination fixes precisely that sentence, and **only** that sentence.

### The test pins that would move

| Pin | What it asserts | Under the proposal |
|---|---|---|
| `tests/test_ratification_level.py:359–408` `test_an_unverified_SR_over_AUTHORED_tests_is_the_IMPL_rung` | `Approved`/`Founded` → `STAGE_RELEASE` (`:398–399`); only out-of-vocabulary `Modified` → `STAGE_IMPL` (`:402`) | **inverts.** Its docstring (`:373–396`) already says it pins "the CURRENT truth, including the unreachability, so that landing the harness driver reddens this test rather than sliding past it" — i.e. this test is *designed* to fail on this change |
| `tests/test_ratification_level.py:340` | `Founded` → `STAGE_RELEASE` | inverts |
| `tests/test_ratification_level.py:353–356` `test_an_LLR_EXEMPT_requirement_needs_no_LLR` | `Analysis`-verified SR → `STAGE_RELEASE` | inverts |
| `tests/test_ratification_level.py:658–680` | `stage_to_bar`: rungs 6–7 → `DevStg-Impl` | unchanged (both rungs map to the same bar — `derive_gate.py:1007–1008`) |
| `tests/test_ratification_level.py:74–118` | which rungs `human_holds` holds per level | unchanged (D8) |

### Docs that teach the ladder

- `PROCESS.md:525–529` — the rendered ladder block, including
  `DevStg-Impl  implementation in work` and
  `DevStg-Release  nothing in work; release checklist available`
- `PROCESS.md:531–537` — "Read the marked rungs as events, in the tense that fits"
- `derive_gate.py:517–531` — the same ladder as a source comment
- `derive_gate.py:906–916` — `spine_stage`'s rung-by-rung docstring
- `derive_gate.py:932–936` — the CAVEAT that this change discharges
- `docs/registry-machinery-reference.md:644–650` — *"DevStg-Impl is a state the
  spine reaches and holds; DevStg-Release is an event performed per release …
  A repo can sit at DevStg-Impl indefinitely without ever performing one."*
  **This passage already describes the owner's model** and is, today, describing
  a rung no legal spine can occupy.
- `skills/gate-advance/SKILL.md:24–47` — "A stage is a state, a bar is an event"

## Q1(c) — has this repo (or any recorded figure) ever hit the vacant rung?

**No, and the history is unambiguous.** Every `stage=` value ever committed to
this repo's `docs/gate`, over the field's whole life (introduced `08c985cb`,
2026-08-13, *"WI-445: the gate vocabulary retires — the eight-rung stage ladder
lands"*):

```
$ git log -p --follow -- docs/gate | grep -oE "stage=DevStg-[A-Za-z]+" | sort | uniq -c
     79 stage=DevStg-Boundary
     12 stage=DevStg-Reqs
      4 stage=DevStg-Arch
      3 stage=DevStg-Needs
```

Four distinct values, none above ord 3. `DevStg-Tests`, `DevStg-Impl` and
`DevStg-Release` have **never** been written to this repo's gate cache.
`tests/test_ratification_level.py:385` says the same in prose: *"This repo is at
DevStg-Boundary, so nothing moved in practice."*

**Do any recorded figures CLAIM a repo was "in DevStg-Impl"?** Three, and all
three are bar readings dressed in stage-shaped prose — the C-class ambiguity the
owner's question is aimed at:

1. **`docs/requirements/open-items.toml:132`** — the Gilbert/Adamah adopter:
   *"`Core` … is a real MIXED software-plus-physical adopter of this kit (stamped
   `767487c 2026-07-06`, **at DevStg-Impl**, 37 SN / 31 SR / 63 LLR / 70 TC)"*.
   **This cannot be a stage reading:** the stamp is 2026-07-06 and the stage
   field did not exist until 2026-08-13 (`08c985cb`). It is a BAR reading of a
   hand-set gate — this repo's own gate file carried a literal `G3` on ten
   commits before the derived model (`git log -p --follow -- docs/gate`), and
   `G3 → DevStg-Impl` via `RETIRED_BAR_ALIASES` (`derive_gate.py:166`). So it is
   a *bar* recorded with the preposition "at", which reads as a stage.

2. **`README.md:74`** — *"Parallel-by-default execution (delivered — phase `v4`
   **at DevStg-Impl**…)"*. A per-phase BAR claim, same preposition.

3. **`docs/registry-machinery-reference.md:649`** — *"A repo can **sit at**
   DevStg-Impl indefinitely"*. Stage-shaped verb ("sit at" = a state) about a
   rung no legal spine can occupy. Correct as a *description of the intended
   model*, false as a description of today's mechanism.

> **Verdict for Q1(c):** the vacant rung has never been occupied here, and every
> written claim that a repo was "at DevStg-Impl" is a bar reading in stage
> grammar. That is not a documentation defect to fix in passing — it is direct
> evidence for the owner's underlying complaint that the shared token plus a
> loose preposition makes the two axes indistinguishable in prose.

---

# Q2 — "At or above will always be a valid method, but perhaps there is a corner case I'm missing."

Adversarial hunt. Five candidates were put to the code; **three are real, one is
real-but-narrower-than-feared, one is refuted**. Two further corner cases were
found that were not on the list, and both are real.

## Q2(i) — NON-MONOTONICITY: **REAL, and materially worse on the stage axis than on the bar axis**

The owner's premise is that the stage axis escapes the min-fold. It does not.
`spine_stage` is documented as *"the LOWEST unfinished rung"* (`derive_gate.py:899–904`)
— which is a min-fold over a finer ladder. The Drafted-row rungs are
`derive_gate.py:959` (SN), `:965` (SR), `:977` (LLR), `:981` (TC), plus the two
inserted rungs `:963` (boundary) and `:972` (arch).

**DRIVEN (D2/D3) — a settled 3-SR spine, then one Drafted row added:**

```
settled spine (3 SR / 3 LLR / 3 TC, all Approved)   stage=DevStg-Release  ord=7/8  raw-bar=DevStg-Tests  ex-draft=DevStg-Tests
  + ONE Drafted SR-004 (ordinary new requirement)   stage=DevStg-Reqs     ord=2/8  raw-bar=DevStg-Below  ex-draft=DevStg-Tests
  + ONE Drafted LLR-004                             stage=DevStg-LLReqs   ord=4/8  raw-bar=DevStg-Below  ex-draft=DevStg-Tests
  + ONE Drafted TC-004                              stage=DevStg-Tests    ord=5/8  raw-bar=DevStg-Below  ex-draft=DevStg-Tests
  + ONE Drafted SN-002 (a new need)                 stage=DevStg-Needs    ord=0/8  raw-bar=DevStg-Below  ex-draft=DevStg-Tests
  + ONE ratified-but-UNCITED SN-002                 stage=DevStg-Needs    ord=0/8  raw-bar=DevStg-Below  ex-draft=DevStg-Below
  + a Drafted CMP row (have_cmps=True)              stage=DevStg-Arch     ord=3/8
  + a Drafted boundary crossing (have_bifs=True)    stage=DevStg-Boundary ord=1/8
```

And the selection consequence, driving an at-or-above rule with
`tests+coverage`'s threshold at ord 6:

```
  settled spine      stage=DevStg-Release  ord=7  -> tests+coverage RUNS
  +1 Drafted SR      stage=DevStg-Reqs     ord=2  -> tests+coverage DOES NOT RUN  <-- REGRESSION
  +1 Drafted LLR     stage=DevStg-LLReqs   ord=4  -> tests+coverage DOES NOT RUN  <-- REGRESSION
  +1 Drafted TC      stage=DevStg-Tests    ord=5  -> tests+coverage DOES NOT RUN  <-- REGRESSION
  +1 Drafted SN      stage=DevStg-Needs    ord=0  -> tests+coverage DOES NOT RUN  <-- REGRESSION
```

**This is C-01 exactly, reproduced on the new axis.** C-01 (repo review
2026-08-19; `check.py:1238–1245`) is: *"ONE ordinary draft requirement drops a
mature project's bar to what a fresh scaffold displays … `tests+coverage` stops
running at all."* WI-473 fixed it on the bar axis with `product_floor`
(`check.py:1233`), built on the `ex-draft=` counterfactual
(`derive_gate.py:1188–1194`).

**The stage axis has no such counterfactual.** `basis_line`
(`derive_gate.py:1338–1355`) emits exactly one `stage=` field, computed from the
live rows at `:1206`. There is no `stage-ex-draft=`. `product_floor`
(`check.py:1283`) reads `_EX_DRAFT_RE` and nothing else. So an at-or-above rule
keyed on the LIVE stage **re-opens C-01 with the WI-473 fix still in place and
unable to help** — note in D2 that `ex-draft` holds firm at `DevStg-Tests` in
every draft row, while the stage collapses.

**Two ways it is strictly worse than the bar axis:**

1. **The stage has no floor.** `compute()` floors the runnable bar:
   `"gate": BAR_NAMES[max(BAR_REQS, raw)]` (`derive_gate.py:1230`). The stage is
   published raw (`:1220`). **DRIVEN (D2):** one Drafted SN takes the stage to
   **ord 0**, three rungs below where the bar's floor pins the strictness. A
   `{DevStg-Reqs}`-tagged step (threshold ord 2) would stop running — something
   the bar axis structurally cannot do.
2. **The collapse is deeper.** The bar drops from `DevStg-Tests` to the floor
   `DevStg-Reqs` — one runnable rung. The stage drops from ord 7 to ord 0–5
   depending on *which tier* the draft lands in, i.e. the depth of the drop is
   controlled by an unrelated property of the drafted row.

**The fix, stated (not recommended):** an `ex-draft` analogue for the stage —
`spine_stage` re-run over the non-draft subset, emitted as a second basis field,
and a `stage_floor` in `check.py` mirroring `product_floor`. This is
**pre-authorized by the ruled model**, twice and in the owner's own doctrine:

- `PROCESS.md:571–574` — *"The ladder is therefore not monotonic … If a monotonic
  reading is wanted it is a second, derived high-water number shown **beside** the
  honest one, never instead."*
- `derive_gate.py:548–551` — the same sentence in the source.
- `check.py:1253–1260` — WI-473's own justification for choosing `ex-draft` over
  a stored high-water, citing that exact `PROCESS.md` sentence.

So the corner case is real, it is the *known* one, and its remedy already has a
ruled shape. What does not exist is the field.

## Q2(ii) — CHECKS THAT SHOULD STOP: **REAL but narrow — exactly ONE step, and it is duplicative rather than wrong**

The census correctly quotes `check.py:1306–1310`: *"Selection is MEMBERSHIP at
the floor, not 'any bar at or below it', because that is how the gate itself
selects (`registry-integrity` is tagged `{DevStg-Reqs}` and genuinely does not
run at DevStg-Impl)."*

**MEASURED** (`check.py --gate all --list`, 26 steps). The only step whose tag
set is not upward-closed is `registry-integrity`:

| Tag set | Steps | Upward-closed? |
|---|---|---|
| `{DevStg-Reqs}` only | `registry-integrity` | **NO** — the only one |
| `{DevStg-Tests, DevStg-Impl}` | `traceability`, `design-flows`, `trajectory`, `backlink-coverage`, `ratify-fresh` | yes |
| `{DevStg-Impl}` only | `format`, `lint`, `tests+coverage`, `doc-refs`, `figures`, `module-coverage`, `perf-budgets`, `trajectory-map`, `status-map`, `open-items`, `okf`, `skills-sync` | yes |
| all three | `derived-gate`, `vocabulary`, `need-form`, `privacy`, `doc-navigability`, `skills-index`, `prompt-catalog`, `staged-divergence` | yes |

**So the entire membership→threshold semantics change has a delta of one step.**
Under at-or-above, `registry-integrity` would newly run at `DevStg-Tests`+.

**Is that wrong?** No — it is redundant. `registry-integrity` is
`trace.py --strict-integrity` (`check.py:631`); `traceability`, which runs at
`DevStg-Tests`/`DevStg-Impl`, is `trace.py --strict …` (`check.py:488–506`). The
exit-code contract at `trace.py:5022` is explicit:

> "1 under `--strict` if any orphan/status/**integrity**/placeholder/schema/off-spine
> finding exists; 1 under `--strict-integrity` if any integrity finding exists"

`--strict` **subsumes** `--strict-integrity` (`trace.py:5039` vs `:5025`). So the
`{DevStg-Reqs}`-only tag is not a semantic exclusion, it is a *de-duplication*:
at higher bars the stricter step already covers the floor.

**Cost, MEASURED:** `python project-trajectory/scripts/trace.py --strict-integrity`
= **1.51 s wall** on this box. Both invocations write the same artifact and are
already serialized on one lane (`check.py:1992–2002`, `"registry-integrity":
"trace-report"`), so the price is one extra serialized 1.5 s engine run per
invocation — real but small.

> **Refined verdict:** the census's framing ("registry-integrity … genuinely does
> not run at DevStg-Impl … is the live row that would change meaning") is
> accurate about the mechanism but overstates the stakes. Nothing becomes wrong
> or meaningless; one 1.5 s check becomes redundant. **The membership→threshold
> change is much cheaper than the census implies.**

**Conversely, must anything run ONLY in a window?** Yes — `window_open`
(`check.py:1198`) is the one true window predicate: it decides *whether the
advisory tier exists at all* (`advisory_plan`, `check.py:1429` —
`if gate == "all" or not window_open(): return []`). It reads `drafted=`,
`modified=`, `ex-draft=` vs `computed=` (`check.py:1205–1230`) — all **bar**
counterfactuals. Note the honest reading recorded in the census as C-2: the
question `window_open` actually asks is *"is this repo mid-redrafting?"*, which
the stage answers directly (a Drafted row drops the stage — D2). A stage re-key
would want this re-expressed, and if it is, it collides head-on with Q2(i): the
same drop that *opens the window* is the drop that *removes the checks*. The two
readings must not be built from the same unqualified value.

## Q2(iii) — THE FOUR CLEARANCE-NEEDING BEHAVIORS: **all four confirmed bar-keyed; the mixed system is coherent EXCEPT for one shared-token hazard**

| # | Site | Stays bar-keyed? | Verified how |
|---|---|---|---|
| 1 | `check_trajectory.py:1886` `phase_findings` — the phase-drop high-water | **YES, unavoidably** | Two independent reasons. (a) It compares against a level a **closed phase anchor recorded in a WI title**, and `_ANCHOR_LEVEL` (`check_trajectory.py:1802`) still accepts the retired `g1`/`g2` spellings "forever" — those are historical records that cannot be re-spelled as stages. (b) **There is no per-phase stage to compare.** DRIVEN (D6): `spine_stage`'s signature is `(srs, llrs, tcs, sn_ids, sn_draft, bifs, cmps, have_bifs, have_cmps)` — **no phase parameter**; `_per_phase(srs, sr_g, llrs, tcs)` folds `maturity_bar`/`sr_bar`, i.e. **bars only**. A per-phase stage does not exist and would have to be built. |
| 2 | `intake.py:480` `_gate_moved` + `:242` `tier_signal` | **YES** — inherently a two-point delta across git trees, never an at-or-above test | direct read. **But it is currently BROKEN — see incidental finding 1.** |
| 3 | `dispatch.py:309` `_kind_action` for `attestation`/`gate` WI kinds | **the RECORDING does; the SELECTION already does not** | The census's nuance is correct and D8 sharpens it: `_kind_action` is *already* stage-keyed via `human_holds`, and D8 shows that comparison cannot distinguish rung 6 from rung 7 at any dial. So the act's *selection* is stage-keyed and unaffected; only the *record* of the clearance is a bar. |
| 4 | `derive_gate.py:390` `sr_bar` + the OI-30 D2 ceiling | **YES** | `_RELEASE_CEILING = BAR_TESTS` (`:364`), returned at `:400`. It constrains what may be CLAIMED, not what may be RUN. A stage-keyed selector does not touch it. |

**Is the mixed system coherent?** Structurally yes — the kit already runs mixed
(55 bar sites + 27 stage sites + 9 mixed), and the two axes are computed
independently from the same rows (`derive_gate.py:1143` vs `:1206`), with the
reconciliation declared once and called by nothing in production
(`stage_to_bar`, `derive_gate.py:1012`, whose docstring at `:1028–1033` says so).

**But there is one mechanical incoherence, and it is a live footgun.**
**DRIVEN (D5):**

```
  stage_ord('DevStg-Below') RAISES
  bar_ord  ('DevStg-Below') RAISES
  stage_ord('DevStg-Impl' ) = 6      bar_ord('DevStg-Impl') = 2
  stage_ord('DevStg-Reqs' ) = 2      bar_ord('DevStg-Reqs') = 0
```

`DevStg-Reqs`, `DevStg-Tests` and `DevStg-Impl` are members of **both closed
vocabularies** (`BAR_ORDER`, `derive_gate.py:159`; `STAGE_ORDER`, `:564`) with
**different ordinals**. Both `bar_ord` and `stage_ord` raise loudly on an unknown
label — the guard both docstrings advertise (`:186–188`, `:592–601`) — but
**neither can raise on a value from the other ladder**, because the value is
legal on both. `stage_ord("DevStg-Impl")` returns 6 whether the caller meant the
top stage or the top bar. `tests/test_stage_ladder.py:68–105` bans *lexical*
comparison; nothing guards *cross-ladder* comparison, because nothing can.

In a system where selection is stage-keyed and four behaviours stay bar-keyed,
values of both kinds flow through the same functions carrying the same spellings
and no type. Today this is contained because `check.py` reads the stage nowhere
(census, `check.py` row) — a re-key removes that containment. **This is the
concrete mechanism by which a mixed system becomes incoherent, and it is not
detectable by any guard the kit currently has.**

## Q2(iv) — MULTI-PHASE: **REAL, and the sharpest gap — "the current stage" is not defined per phase**

This repo's live basis line reads
`per-phase=1=DevStg-Tests;3=DevStg-Tests;4=DevStg-Reqs;5=DevStg-Below phase=5`
alongside a single `stage=DevStg-Reqs`.

**DRIVEN (D6)** — a repo with phase 1 settled and phase 5 drafting:

```
  per-phase BARS: {'1': 'DevStg-Tests', '5': 'DevStg-Below'}
  repo-wide STAGE: DevStg-Reqs
```

Three separate facts follow:

1. **There is no per-phase stage.** `spine_stage` takes no phase filter (D6);
   `_per_phase` (`derive_gate.py:1234`) folds bars. To key selection on
   "the current phase's stage", the per-phase stage would have to be **built** —
   `spine_stage` re-run per phase subset, with the SN/boundary/arch rungs
   somehow apportioned (the SN coverage rung `:967` and the two inserted rungs
   `:963`/`:972` are repo-global — they have no phase).
2. **The single global stage is already a MIN over phases in effect.** Reading
   "the lowest unfinished rung" over the union of all phases' rows gives the
   least-mature phase's answer. **So yes — MIN over phases is the bar problem
   again**, and the owner's intuition that the stage escapes the min-fold does
   not hold. The global stage `DevStg-Reqs` in D6 is driven entirely by phase 5's
   draft; phase 1's maturity is invisible on the stage axis, whereas it *is*
   visible on the bar axis (`1=DevStg-Tests`).
3. **The `DevStg-Below` sentinel has no stage counterpart.** The per-phase line
   carries `5=DevStg-Below` today. `stage_ord("DevStg-Below")` **RAISES** (D5).
   `check.py` handles this on the bar axis with a separate degrading table
   `_window_ord` (`check.py:1090`; 4 values incl. `DevStg-Below`, degrades to
   `-1`) precisely because the sentinel appears in per-phase values. A per-phase *stage* line would need the same escape hatch, and the
   stage ladder deliberately has none (`PROCESS.md:583–585`: *"There is no
   `DevStg-Below` you sit at"*).

**Which phase's stage would at-or-above read?** There is no answer in the code
today. The three candidates each fail differently: the *global* stage is the min
(problem 2); the *derived current phase* (`derive_gate.py:1202–1204`,
`max` over non-draft phase numbers) is the newest phase, which is the one most
likely to be drafting and therefore lowest; a *per-phase* stage does not exist.

> **Verdict for Q2(iv): this is the corner case the owner was reaching for.** It
> is not that at-or-above is invalid — it is that "the current stage" is
> underdetermined in a phased repo, and every available reading reproduces the
> min-fold the re-key was meant to escape.

## Q2(v) — further corner cases found

### (v-a) SCAFFOLD-FRESH REPOS: **REAL — two opposite failure modes depending on whether `derive_gate.py` has run**

`gate.template` (scaffolded to `docs/gate` by `bootstrap.py:1555`) is a bare
one-line file:

```
DevStg-Reqs
```

No `# basis:` line, no `stage=` field. So for a freshly bootstrapped repo:

- **Before the first `derive_gate.py` run:** `resolve_gate` (`check.py:1472`)
  reads `DevStg-Reqs` and works. A stage-keyed `resolve_gate` would find **no
  stage at all** — `spine_stage_of` returns `None` (`agent_common.py:784`,
  DRIVEN in D10). `resolve_gate`'s absent-file fallback is `"all"`
  (`check.py:1500`), so the plausible behaviours are (i) hard-exit
  (`check.py:1493–1498` is the existing unknown-value path) or (ii) fall through
  to `all` — running the full strict plan, including `--require-verified` and
  `--strict-schema` (`check.py:495–506`), against an empty scaffold. Both are
  bad; today neither happens.
- **After `derive_gate.py` runs.** **DRIVEN (D4):**

```
  no SN, no SR (bootstrap.py output)   stage=DevStg-Needs  ord=0/8  raw-bar=DevStg-Reqs
  one ratified SN, no SR               stage=DevStg-Needs  ord=0/8  raw-bar=DevStg-Reqs
  one Drafted SN, no SR                stage=DevStg-Needs  ord=0/8  raw-bar=DevStg-Reqs
```

  The stage is **ord 0**. Under at-or-above with `registry-integrity` at
  threshold ord 2, a fresh scaffold would run **nothing at all** — losing the one
  always-on integrity floor it has today. The bar's `max(BAR_REQS, raw)` floor
  (`derive_gate.py:1230`) is exactly what prevents this now, and
  `derive_gate.py:64–66` states that intent: *"A repo with no real SRs yet (a
  fresh scaffold) derives `DevStg-Reqs` … never a vacuous `DevStg-Impl`."*
  The stage axis has the opposite vacuity guard (`spine_stage:959`/`:961` return
  `STAGE_NEEDS`, documented at `:951–953`) and **no floor**.

  `ci/check.yml:70–73` states the scaffold promise explicitly: *"a freshly-scaffolded
  DevStg-Reqs repo is green"*. Under at-or-above it would be green **because
  nothing ran**, which is the silent green SN-008 forbids.

### (v-b) THE STAGE READER'S REGEX SILENTLY TRUNCATES: **REAL — and this CORRECTS the census**

The census (C-5) states: *"`agent_common.py:783` requires `stage=DevStg-<Alpha>`
— a label with a digit or hyphen reads `None`, which holds everything."*
The digit half is right; **the hyphen half is wrong, and in the unsafe
direction.** The regex is
`r"#\s*basis:.*\bstage=(DevStg-[A-Za-z]+)\b"` (`agent_common.py:783`).
**DRIVEN (D10):**

```
  cache carries DevStg-Impl-2            -> 'DevStg-Impl'      <-- TRUNCATED to a DIFFERENT VALID RUNG (in LADDER_RUNGS: True)
  cache carries DevStg-Release-Candidate -> 'DevStg-Release'   <-- TRUNCATED to a DIFFERENT VALID RUNG (in LADDER_RUNGS: True)
  cache carries DevStg-Reqs-v2           -> 'DevStg-Reqs'      <-- TRUNCATED to a DIFFERENT VALID RUNG (in LADDER_RUNGS: True)
  cache carries DevStg-Impl2             -> None               (fail-honest, holds everything)
  cache carries DevStg-                  -> None               (fail-honest, holds everything)
  cache carries DevStg-Below             -> 'DevStg-Below'     (not in LADDER_RUNGS -> human_holds holds, fail-honest)
```

A hyphenated label matches the `\b` at the hyphen and returns a **prefix that is
a legal rung**, passing `LADDER_RUNGS` membership and driving `human_holds` to a
confident, wrong answer — the opposite of the fail-honest direction the
docstring claims (`agent_common.py:769–776`). Today this is latent (no rung is
hyphenated past its first segment). It becomes live the moment anyone inserts a
rung with a compound label — which the ladder's own design explicitly provides
for (`PROCESS.md:576–582`: *"inserting a rung self-corrects every ordinal"*).
**A re-key runs the whole kit's selection through this seam**, which is the
census's own point about the carrier, sharpened.

### (v-c) ADOPTER MIGRATION AND CI: **REAL, and larger than the bar-axis alternative**

- `ci/check.yml:79`/`:83` pass **no `--gate`**, so adopters inherit whatever
  `resolve_gate` resolves; only `ci/check.yml:89` names `--gate all`.
  `.github/workflows/test.yml:162` likewise. So CI needs no edit — but its
  behaviour changes silently for every adopter on re-sync, which is the worst
  shape for a migration.
- The `--stage-cleared`/`--gate` flag (`check.py:2092`) and the `gates=`
  declaration (`check.py:374–387`, contract at `stack.ini.template:181–188`) are
  an **adopter-authored vocabulary**. Re-keying them means a third alias
  generation after `G*` and `DevBar-*` (`derive_gate.py:164–177`) — and the
  aliases cannot be mechanical, because `DevStg-Impl` is legal in *both*
  vocabularies with different meaning (Q2(iii)). An adopter's
  `gates = DevStg-Impl` would silently mean ord 2 → ord 6.
- The WI `bar:` frontmatter (`intake.py:97`, `:113`, `:968`; `integrate.py:1446`,
  `:1467`, `:1608`) is written into **tracked WI spec files**. `wi_convert.py:160`
  and the equality pin `tests/test_stage_ladder.py:124–139` hold four tables in
  step; a re-key touches all of them plus every historical WI row.
- By contrast, OI-51 option (a) is *"one line per step"* (`open-items.toml:2045`)
  and withdrawable by the same one-line edit (`:2058`).

### (v-d) REFUTED: "the ex-draft basis can be reused for the stage"

`product_floor` (`check.py:1283–1290`) reads `_EX_DRAFT_RE` and validates the
value against `BAR_ORDER` (`:1288`), returning `None` for anything else. The
`ex-draft=` field carries a **bar** (`derive_gate.py:1349`,
`ed=BAR_NAMES[result["ex_draft"]]`). Feeding it to `stage_ord` would type-check
(both ladders share three spellings — D5) and return a wrong ordinal. So the
existing counterfactual is **not** reusable on the stage axis; a new derived
field is required. Refuted as a shortcut.

---

# Q3 — "docs/gate still reads DevStg-Reqs — why can't this just be changed to the current/active development stage?"

## Who reads what, and what the value MEANS to each

`docs/gate` carries **two payloads**: the machine-readable last line (a BAR) and
the `# basis:` comment (which carries the stage as a substring). The header
states the contract at `docs/gate:5–6` — *"The value on the last line is the bar
that must next be CLEARED — and therefore the STRICTNESS SELECTOR check.py runs
at"* — and at `:26`: *"check.py / CI read the first non-comment line below,
exactly as before."*

### Readers of the LAST LINE (the bar)

| Reader | file:line | What the value MEANS to it | If the line's meaning flips to the stage |
|---|---|---|---|
| `check.py` `resolve_gate` | `check.py:1472–1500` | **the strictness selector.** Validated against `GATES = BAR_ORDER + ["all"]` (`check.py:985`) and **hard-exits** on anything else (`:1493–1498`) | breaks immediately: `DevStg-Needs`, `DevStg-Boundary`, `DevStg-Arch`, `DevStg-LLReqs`, `DevStg-Release` are all outside `GATES` → `sys.exit`. **Five of the eight rungs would hard-exit `check.py` on day one.** |
| `derive_gate.py` `parse_cache` | `derive_gate.py:1400–1411` | the cached value `--check` compares for rot | needs re-pointing |
| `traj_parse.py` `_gate_value` | `traj_parse.py:449–462` | the Process tab's existence condition (`None` ⇒ omit the tab) | display re-key |
| `intake.py` `_gate_moved` | `intake.py:480–487` | "did the derived value move across the merge?" → mints a `strong` adjudication row (`:242`) | **currently broken — see incidental finding 1** |
| `agent_common.read_declared` | `agent_common.py:129–138` | the generic one-word declared-policy reader; documented as *"still the reader for `docs/gate` (a generated cache with a one-value last line)"* | generic; follows |
| CI (adopter) | `ci/check.yml:79`, `:83` | passes **no `--gate`** — inherits `resolve_gate` | inherits silently |
| CI (kit) | `.github/workflows/test.yml:162` | same | inherits silently |
| pre-commit hook | `project-trajectory/hooks/pre-commit:269` | passes **no `--gate`** → `_step_gate` (`check.py:1503–1509`) resolves to `"all"`, deliberately, to keep the floor warn-first | unaffected |

### Readers of the `# basis:` COMMENT

| Reader | file:line | Reads | Note |
|---|---|---|---|
| `agent_common.spine_stage_of` | `agent_common.py:760–784` | `stage=` via regex at `:783` | **the current hack** — the only stage consumer, and it regex-scrapes a comment. Truncation bug: Q2(v-b) |
| `check.py` `window_open` | `check.py:1198–1230` via `_BASIS_RE` (`:1074`) | `drafted=`, `modified=` | bar counterfactuals |
| `check.py` `product_floor` | `check.py:1283` via `_EX_DRAFT_RE` | `ex-draft=` | bar |
| `check_trajectory.read_derived_phases` | `check_trajectory.py:1823` | `per-phase=` | bars; unknown values silently dropped (`:1836`) |
| `traj_status._stage_line` | `traj_status.py:389–405` | `stage=`, `stage-ord=`, `stage-of=` + the bar | the one surface that gets the vocabulary right |
| `derive_gate.py --check` | `basis_line` `:1286`, compared whole | the entire line | any new field is a cache-format change (`:1296–1299`) |

## The three honest options, and what each costs

### Option A — FLIP THE LINE (the last line becomes the stage)

- **Cost, immediate and hard:** `check.py:1493–1498` hard-exits on any value
  outside `GATES` (`check.py:985` = the three runnable bars + `all`). Five of the
  eight rungs are outside it. Every one of the eight last-line readers above must
  be re-keyed **in the same commit**, or an adopter's `check.py` exits on
  checkout.
- **Cost, semantics:** step selection changes from set membership to an ordering
  test for all 26 built-in steps plus the adopter `gates=` contract
  (`check.py:374–387`, `stack.ini.template:181–188`) — though the *behavioural*
  delta is one step (Q2(ii)).
- **Cost, migration:** a third alias generation that cannot be mechanical,
  because `DevStg-Reqs`/`Tests`/`Impl` are legal in both vocabularies with
  different ordinals (Q2(iii)). A `RESYNC_PACK.md` entry is owed; the existing
  entries for this file (`RESYNC_PACK.md:495`, `:646`, `:1064`, `:2185`) show the
  shape — `:1064` already carries a **"This OVERRIDES §1's preserve-classes
  rule"** regenerate-don't-preserve directive for `docs/gate`.
- **Cost, correctness:** inherits Q2(i) (no stage counterfactual → C-01 reopens),
  Q2(iv) (undefined per phase), Q2(v-a) (scaffold seam), Q2(v-b) (truncating
  regex).
- **What it buys:** one axis, one value, the owner's question asked directly.

### Option B — CARRY BOTH MACHINE-READABLY (second line, or `key=value`)

- The stage stops being a comment substring; `agent_common.py:783`'s regex-scrape
  is retired.
- **Cost:** every reader that takes "the first non-comment line" as the value
  must learn a second line or a key. That idiom is duplicated per the F5 rule
  across `check.py:1490`, `derive_gate.py:1409`, `traj_parse.py:459`,
  `agent_common.py:129–138` (which is itself the ONE home since WI-448, with four
  former copies pinned equal). A second bare line is the cheapest form but is
  positional and silent on mis-order; `key=value` is safer and touches every
  reader.
- **Cost:** `basis_line` is compared **whole** by `--check`
  (`derive_gate.py:1296–1299`), so this is a cache-format change every adopter
  passes through by regenerating once — the ordinary regenerate step, and the
  precedent is stated (`:1301–1308`, field-compatible-not-value-compatible).
- **What it buys:** both axes are first-class; the four clearance-needing
  behaviours (Q2(iii)) keep the bar they genuinely need; the shared-token hazard
  is *reduced* by giving each axis its own key, though not eliminated.

### Option C — KEEP THE BAR LINE; PROMOTE THE STAGE TO A FIRST-CLASS MACHINE FIELD

Mechanically a subset of B: the last line is untouched (zero reader churn, zero
adopter migration on that line), and `stage=` moves from "substring of a comment
that happens to be greppable" to a declared field with its own parser and its own
test pin — plus, if Q2(i) is to be answered, a `stage-ex-draft=` companion.

- **Cost:** the smallest of the three. One producer change (`basis_line`
  `derive_gate.py:1338–1355`), one consumer change (`agent_common.py:783`), one
  round-trip pin (the precedent exists: `tests/test_derive_gate.py`'s
  `check._BASIS_RE.search(derive_gate.basis_line(result))`, cited at
  `derive_gate.py:1325–1327`).
- **Cost:** it does **not** answer the owner's Q3 as asked — `docs/gate`'s
  headline value still reads `DevStg-Reqs`, the bar. The stage becomes reliable,
  not prominent. Any selection re-key is then a separate, later act.
- **What it buys:** it de-risks whichever way the ruling goes, because *every*
  stage-keyed path (including a future option-A flip) runs through the carrier
  seam the census named as the first obstacle.

## Is any option strictly dominated?

**Yes — exactly one, and only in the narrow technical sense.**

**Option A is not dominated** (it is the only one that answers the question as
asked; it costs the most).
**Option C is not dominated by B** (it is strictly cheaper and strictly less
capable — a real trade).
**"Do nothing" IS dominated by C**: leaving `stage=` as a comment substring
retains the truncation bug (Q2(v-b)) and the sole-consumer regex-scrape at
`agent_common.py:783`, at no saving relative to C, whose cost is one producer
field and one parser. Every other pair is a genuine trade-off.

**One fact bearing directly on the owner's premise.** The question assumes the
line "still reads `DevStg-Reqs`" *because nobody changed it*. It reads
`DevStg-Reqs` because it is **derived and floored**: `compute()` returns
`BAR_NAMES[max(BAR_REQS, raw)]` (`derive_gate.py:1230`) over a `computed=DevStg-Below`
raw value, driven by this repo's nine Drafted rows and its declared undecomposed-SR
debt. And the `# basis:` line's `stage=DevStg-Reqs` **coincidentally reads the
same token by a completely different route** — `spine_stage`'s Drafted-SR rung
(`derive_gate.py:965`) — at ord 2 of 8 rather than bar-ord 0 of 3. The two
`DevStg-Reqs` on this repo's gate file today are the same spelling of two
different facts. That coincidence is, in miniature, the whole of OI-51.

---

# Closing summary

| # | Corner case | Real or refuted | What handles it today | What would have to handle it |
|---|---|---|---|---|
| **Q2(i)** | Stage NON-MONOTONICITY — one Drafted row drops ord 7 → 0–5, removing at-or-above-selected checks | **REAL** (D2/D3) | nothing — `ex-draft` is bar-only (`derive_gate.py:1349`) and `product_floor` validates against `BAR_ORDER` (`check.py:1288`) | a stage counterfactual field + a `stage_floor` mirroring `product_floor`. Pre-authorized: `PROCESS.md:571–574` |
| **Q2(i-b)** | The stage has **no floor** — ord 0 is reachable, below every runnable bar's rung | **REAL** (D2/D4) | the bar's `max(BAR_REQS, raw)` floor (`derive_gate.py:1230`), which the stage axis lacks (`:1220`) | a stage floor, or a threshold vocabulary that starts at ord 0 |
| **Q2(ii)** | Membership → threshold changes step meaning | **REAL but narrow** | `check.py:1306–1310` chose membership deliberately | delta is **one** step (`registry-integrity`), and it is duplicative not wrong — `--strict` subsumes `--strict-integrity` (`trace.py:5022`). MEASURED cost 1.51 s |
| **Q2(ii-b)** | `window_open` must stay a window | **REAL** | `check.py:1198–1230`, bar counterfactuals | on a stage re-key, the same drop that opens the window removes the checks — the two readings must not share one unqualified value |
| **Q2(iii)** | The four clearance-needing behaviours | **all four CONFIRMED bar-keyed** | phase-drop `check_trajectory.py:1886`; `_gate_moved` `intake.py:480`; the ratification *record*; `sr_bar`'s ceiling `derive_gate.py:390`/`:364` | mixed system is coherent, with one exception below |
| **Q2(iii-b)** | Shared-token hazard — `DevStg-{Reqs,Tests,Impl}` legal on BOTH ladders with different ordinals | **REAL** (D5: `stage_ord`=6 vs `bar_ord`=2 for `DevStg-Impl`) | nothing — both `bar_ord` and `stage_ord` raise on unknowns but **cannot** raise on a value from the other ladder; `tests/test_stage_ladder.py:68–105` bans only *lexical* comparison | a type/prefix distinction, or a guard that cannot exist while the spellings coincide |
| **Q2(iv)** | MULTI-PHASE — which phase's stage does at-or-above read? | **REAL — the sharpest gap** | nothing. **No per-phase stage exists** (D6: `spine_stage` takes no phase arg; `_per_phase` folds bars) | build a per-phase stage; the global stage is *already* the min over phases (D6), i.e. the bar problem again |
| **Q2(iv-b)** | `DevStg-Below` under stage ordering | **REAL** (D5: `stage_ord` RAISES) | the bar axis has a degrading `_window_ord`; the stage ladder deliberately has no sentinel (`PROCESS.md:583–585`) | a per-phase stage line would need an escape hatch the ladder refuses |
| **Q2(v-a)** | Scaffold-fresh repos | **REAL, two opposite modes** | `gate.template` = bare `DevStg-Reqs`, no basis line; the bar floor keeps a fresh repo at `DevStg-Reqs` | pre-derive: no stage to read → hard-exit or full-strict-on-empty. Post-derive: ord 0 → **nothing runs**, breaking `ci/check.yml:70–73`'s green-scaffold promise |
| **Q2(v-b)** | `spine_stage_of` regex silently truncates a hyphenated label to a **different valid rung** | **REAL — and CORRECTS the census's C-5** (D10) | nothing; latent only because no rung is compound today | `agent_common.py:783`'s `\b` must not match at a hyphen; digit case correctly reads `None` |
| **Q2(v-c)** | Adopter migration / CI | **REAL, larger than option (a)** | CI passes no `--gate` (`ci/check.yml:79`,`:83`) so it changes silently | a third alias generation that cannot be mechanical (shared spellings); WI `bar:` in tracked spec files; 4 tables pinned equal (`tests/test_stage_ladder.py:124–139`) |
| **Q2(v-d)** | Reuse `ex-draft=` as the stage counterfactual | **REFUTED** | `ex-draft` carries a BAR (`derive_gate.py:1349`), validated against `BAR_ORDER` (`check.py:1288`) | a new derived field; there is no shortcut |
| **Q1(b)** | Does anything behave differently at ord 6 vs ord 7? | **REFUTED for all 27 stage-keyed sites** (D8/D9) | `DIAL_HOLDS` (`agent_common.py:567`) puts both rungs in the `4: None` catch-all; `APPROVAL_RUNGS` names neither | the change is **display-only** on the ratification half — blast radius zero |
| **Q1(c)** | Has this repo ever been at rung 6? | **REFUTED — never** | 4 distinct `stage=` values ever committed, max ord 3 | three docs *claim* "at DevStg-Impl" (`open-items.toml:132`, `README.md:74`, `docs/registry-machinery-reference.md:649`) — all bar readings in stage grammar |

## Incidental findings (out of scope; recorded, not acted on)

Each is a claim to confirm before anyone acts on it.

1. **`intake.py:480` `_gate_moved` reads the WRONG LINE and is therefore always
   `False`.** It takes `out.splitlines()[0].strip()` — the **first** line of
   `docs/gate`, which since the derived-gate model is the static header comment
   `# DERIVED BAR — generated by scripts/derive_gate.py (do not hand-edit).`
   (`derive_gate.py:1360`), not the first *non-comment* line every other reader
   takes (`check.py:1490`, `derive_gate.py:1409`, `traj_parse.py:459`).
   **Verified:** the header is byte-identical at `08c985cb` and at `HEAD`.
   Consequence: `tier_signal` (`intake.py:242`) can never mint its `strong`
   adjudication row for a moved gate. This worked before `docs/gate` gained a
   header (a legacy hand-set gate's line 0 *was* the value) and broke silently
   at the migration. Directly relevant to Q2(iii)#2 — one of the four
   clearance-needing behaviours is currently not running.

2. **`traj_panels.py:1043` renders the raw bar** while `traj_status.py:389–405`
   goes through `derive_gate.bar_label`. `_stage_line`'s docstring
   (`traj_status.py:387–388`) claims this surface and `PROJECT_STATE.html`
   "cannot disagree", but the dashboard's Process tab does not call `bar_label`,
   so the OI-30 D2 ceiling note appears in `docs/status.md` and not on the
   dashboard. (Carried forward from the census, unchanged.)

3. **The census's C-5 hyphen claim is wrong** — see Q2(v-b). Recorded here so the
   census is not cited for it.

## Method note

`derive_gate`'s and `agent_common`'s own functions were driven over synthetic
in-memory spines and temp scaffolds from throwaway scripts in the session
scratchpad — never in the repo. The step table was measured with
`python project-trajectory/scripts/check.py --gate all --list`. The
`trace.py --strict-integrity` timing is a single warm run on this box
(`real 0m1.514s`) and is a price indication, not a budget. Git history was read
with `git log -p --follow -- docs/gate`. Nothing in the tree was modified and
nothing was committed.
