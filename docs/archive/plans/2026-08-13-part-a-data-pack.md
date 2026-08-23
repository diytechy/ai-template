> **ARCHIVE** — design history as of 2026-08-23; not current guidance.

# WI-441 part A — the analysis data pack

**Status:** analysis input, **not a decision**. Produced for
[`OI-14`](../../requirements/open-items.toml) part A (ruled A3 + A6, 2026-08-13)
under [`WI-441`](../work/complete/WI-441-part-a-boundary-decomposition-partition-shortlist.md).
The coordinator ranks; the owner adopts. Nothing here selects a partition.

**Measured at revision `81a142c2`** (`WI-436: the OI-26 loose end records its
ruling`). Every figure below states the command or derivation that produced it,
per the declared-figure convention (`docs/process-options.md`, "Signed
measurements"). Appendix A carries the two derivation scripts verbatim so each
`cmd=` is genuinely re-runnable.

Method, as the ruling prescribes: N2/DSM-style decomposition from the system's
**declared inputs and outputs** (`docs/knowledge/system-decomposition-methods.md`),
with **one home per behaviour** as a hard constraint and **cut count** as the
tie-breaker. Candidates in §5 are derived from the boundary (§1) and the
functions (§2) — *not* by clustering the current tree, which the ruling
explicitly refutes (option A2).

---

## 0. The finding that governs the ranking

**No candidate partition satisfies the hard constraint, and none can.** The best
candidate still leaves **7 of 12** verified one-behaviour-many-homes violations
straddling a component boundary; today's shape leaves 10 of 12.

<!-- fig: cmd="python - < appendix-A-2 (score.py), rev=81a142c2" -->

This is not a defect in the candidates. **One home per behaviour is a property of
the CODE, not of the partition.** Twelve behaviours physically exist in 2–6
modules each; no assignment of 55 modules to components can put 6 copies of one
behaviour in one component unless those copies first collapse into one module.
Collapsing all twelve means **deleting 27 copies across 16 of the 55 modules**.

<!-- fig: cmd="python - < appendix-A-3 (collapse.py), rev=81a142c2" -->

That collapse collides head-on with the standing **F5 ruling** (owner,
2026-07-12; reaffirmed 2026-08-10 as repo-lock D-7, executed WI-426), which
*requires* each kit script to stay stdlib-only and independently copy-able and
which **rejected a shared `_kitcommon.py`**. F5's own live statement
(`tests/test_rule_sync.py` module docstring) draws the line the ruler needs:

> duplicated **PLUMBING** is accepted UNBOUNDED — no census, no allowlist, no
> count. […] duplicated **POLICY** requires a BEHAVIOURAL PIN IN THIS FILE.

So OI-14's "one home per behaviour" and F5's "duplicate plumbing freely" are
**both live owner rulings that contradict each other on exactly these twelve
behaviours**, unless "behaviour" is read as "policy". §4 therefore reports the
straddle count under both readings, and the ruler should say which one binds.
This is the single largest input to the ranking and it is prior to any
partition choice.

---

## 1. System boundary inventory

The kit-as-system. Direction is stated from the kit's point of view: **IN** =
the kit consumes, **OUT** = the kit provides. *Character* is the owner's ruled
discrete-vs-variable typing (OI-14 part B): **discrete** = a finite enumerable
alphabet (exit code, gate name, status enum, boolean dial); **variable** =
unbounded content (prose, file bytes, counts, durations).

### 1a. Crossings the registry already carries

Fifteen of the 113 live IF rows name an external counterpart.

<!-- fig: cmd="python - < appendix-A-1 (analyze.py) | jq .if_external_rows", rev=81a142c2 -->

| # | IF row | Dir | Counterpart (external actor) | What crosses | Character |
|---|--------|-----|------------------------------|--------------|-----------|
| X-01 | IF-013 | OUT | downstream adopter | `check.py` gate/tier harness verdict | discrete (exit code + step status) |
| X-02 | IF-014 | OUT | downstream adopter | `bootstrap.py` scaffold write + re-sync diff | variable (file bytes) |
| X-03 | IF-015 | OUT | downstream adopter | `agent_loop.py` unattended coordinator run | discrete (typed outcome) + variable (session log) |
| X-04 | IF-016 | OUT | downstream adopter | `check_vendored.py` drift verdict | discrete |
| X-05 | IF-017 | OUT | downstream adopter | `gen_cases.py` permutation expansion | variable (generated TC rows) |
| X-06 | IF-018 | OUT | downstream adopter | `gen_release_checklist.py` checklist | variable |
| X-07 | IF-020 | OUT | **agent CLI** | `subagent_gate.py` spawn allow/deny | discrete |
| X-08 | IF-030 | IN | docs | `check_docs.py` reads the doc tree | variable |
| X-09 | IF-032 | IN | **git** | `check_privacy.py` reads staged/outgoing content | variable |
| X-10 | IF-036 | IN | upstream docs | `check_vendored.py` reads the vendored source | variable |
| X-11 | IF-041 | IN | **agent CLI** | `agent_session.py` launches the CLI, reads its result | variable (stdout) + discrete (exit) |
| X-12 | IF-048 | OUT | **run.\* launchers** | `run_menu.py` capability menu | discrete (menu selection) |
| X-13 | IF-070 | IN | coverage.json | `check_coverage.py` reads the coverage report | variable (per-module percent) |
| X-14 | IF-080 | OUT | downstream adopter | `integrate.py` serialized merge queue | discrete (merge outcome) |
| X-15 | IF-081 | OUT | downstream adopter | `trunk_step.py` trunk step | discrete |

Note the asymmetry: **8 of 15** name the same coarse counterpart
`downstream adopter`, which is an actor, not a surface. The registry has no row
for the *human* on either side of it.

### 1b. Crossings the registry MISSES

Each of these is a real crossing of the kit's boundary with **no IF row today**.
Verified absent by literal search of `docs/requirements/interfaces.csv`:
`dev-setup` → 0 hits, `workflow`/`codex`/`OpenAI`/`onboard` → 1 hit
(`IF-064`, an unrelated `agent_session` row), `agent-resume` → 1 hit
(`IF-068`, the `[agent-loop]` ini section, not the launcher),
`PROJECT_STATE` → 1 hit (`IF-011`, the staleness contract to `check.py`, not
the owner-facing surface).

<!-- fig: cmd="grep -icF '<token>' docs/requirements/interfaces.csv", rev=81a142c2 -->

| # | Crossing | Dir | What crosses | Character | IF row today |
|---|----------|-----|--------------|-----------|--------------|
| M-01 | **contributor → `dev-setup.{sh,cmd,command}`** | IN | invocation; toolchain probe result | discrete (present/absent/version) | **none** |
| M-02 | **owner → `agent-resume.{sh,cmd,command}`** (root) | IN | one-command autonomous-run trigger | discrete (invoke) | **none** |
| M-03 | `run.*` launchers → contributor | OUT | the runnable capability list | discrete | IF-048 (menu side only) |
| M-04 | **CI runner → the harness** (`.github/workflows/{test,canary}.yml`, `project-trajectory/ci/check.yml`) | IN | push/PR/schedule trigger; OS × Python matrix | discrete | **none** |
| M-05 | **harness → CI runner** | OUT | job verdict, step log | discrete (exit) + variable (log) | **none** |
| M-06 | **`bootstrap.py` → adopting repo tree** (the MAPPING: templates → `docs/`) | OUT | scaffolded file set; kit-version stamp | variable (bytes) + discrete (stamp) | IF-014 (coarse; adopter, not tree) |
| M-07 | **shipped template set as a product artifact class** (OI-28 seed 2) | OUT | `*.template.*` + `registries/*` as traced product | variable | **none** (OI-28 asks for one SR anchor, `test_dogfood_sync` as verification) |
| M-08 | **owner ← `open-items.html`** | OUT | the decision-brief reference view | variable (prose) | IF-074 names the *file*, not the reader |
| M-09 | **owner ← `PROJECT_STATE.html`** | OUT | the trajectory dashboard | variable | **none** as an owner surface |
| M-10 | **owner ↔ `docs/status.md`** | IN/OUT | the resume-from-text SSOT; owner edits it | variable | IF-037 names the *file*, not the owner |
| M-11 | **owner → registries** (rulings, attestations, `Status` flips) | IN | ratification decisions | discrete (`Status` enum) | **none** |
| M-12 | **direct-session LLM agent → the repo** (OI-28 seed 1) | IN | instructions/prompt in | variable | **none** |
| M-13 | **direct-session LLM agent → artifact edits** (OI-28 seed 1) | OUT | edits landing through the **git-enforced hook floor** (`pre-commit`, `pre-push`, `commit-msg`); SR-019's rationale becomes the row's rationale | variable (diff) gated by discrete (hook exit) | **none** |
| M-14 | **OpenAI / critic CLI** (codex; `sol`/`terra` adversarial reviews) | IN/OUT | hostile-review brief out, findings in | variable | **none** (`docs/agents.csv` declares families via IF-045, but no external-provider row) |
| M-15 | **model provider API** (behind every agent CLI) | IN | rate limit, auth expiry, retired model — SN-020's failure modes | discrete (error class) | **none** |
| M-16 | **git as the mutation floor** (worktree, index, refs, hooks, remote) | IN/OUT | commits, merges, pushes, advisory locks | discrete (ref state) + variable (diff) | IF-032 only (`check_privacy` read side) |
| M-17 | **OS / filesystem / interpreter** (Windows + POSIX, Python ≥3.11) | IN | path semantics, encoding, kernel advisory lock, interpreter presence | discrete (platform, version) | **none** (SN-011/013, SR-034/035/114 depend on it) |
| M-18 | **pytest + coverage tooling** | IN | test results feeding the tier floors | discrete (pass/fail) + variable (percent) | IF-070 (coverage side only) |
| M-19 | **terminal / console** | OUT | every script's human-readable report | variable | **none** (the `_utf8_console` 32-copy behaviour serves exactly this crossing) |

### 1c. Completeness declaration

**The set X-01..X-15 + M-01..M-19 = 34 crossings is COMPLETE to my best
reading** of the registries, the launchers, the CI tree, the hook tree and the
OI-14/OI-28 rows.

Where I am **unsure**, stated rather than hidden:

1. **`downstream adopter` is one row-counterpart but at least three actors** —
   the adopting *repo tree* (M-06), the adopting *team* (M-01), and the adopting
   repo's *CI* (M-04). Whether that is one crossing or three is a modelling
   choice I did not make.
2. **Granularity of M-16 (git).** I counted git as one crossing. A case exists
   for splitting it into read (status/diff), write (commit/merge), and
   enforcement (hooks) — the hook floor is arguably a *different* boundary from
   the porcelain the coordinator shells out to.
3. **M-19 (terminal)** may be judged below the boundary — an output medium
   rather than an actor. I included it because it is the only crossing that
   explains a 32-copy behaviour.
4. **Skills fan-out** (`project-trajectory/skills` → `.claude/skills/` via
   `bootstrap.py --agents`) crosses into an *agent harness's* config namespace.
   IF-035 and IF-019 cover the index; the materialization into a third-party
   agent's directory layout is arguably its own crossing. I did not add it.
5. **`docs/knowledge/` packs** arm the containment rule (§3e) from *presence*.
   Whether a knowledge pack is an input crossing or an internal artifact is
   undecided here.
6. I did **not** audit `MULTI_REPO.md`'s cross-repo coordinator rung — it is a
   deferred design doc, so its crossings are not live.

---

## 2. Functional decomposition input

The system's obligations as **functions** — signal transformations between the
§1 crossings — with the SN/SR ids that feed each. Twenty top-level functions
over 37 SNs and 147 SRs.

<!-- fig: cmd="python - < appendix-A-1 (analyze.py) | jq '.sn_total, .sr_total'", rev=81a142c2 -->

| Fn | What the system must DO (signal transformation) | Feeding SN | Feeding SR |
|----|--------------------------------------------------|-----------|-----------|
| **Fn-01** | Turn a bare repo into a running gated process (templates IN → scaffolded tree OUT), idempotently and re-syncably | SN-001, SN-034, SN-038 | SR-009, SR-010, SR-011, SR-036, SR-111 |
| **Fn-02** | Read a declared stack/policy profile and refuse an ambiguous one (one dial, one home) | SN-003, SN-028 | SR-007, SR-008, SR-031, SR-137, SR-138 |
| **Fn-03** | Parse the requirement spine from one machine carrier (bytes IN → typed rows OUT) | SN-002 | SR-126, SR-129, SR-147 |
| **Fn-04** | Join SN→SR→LLR→TC and report orphans, id/structure integrity, schema and placeholder violations | SN-002, SN-022 | SR-001, SR-002, SR-003, SR-004, SR-005, SR-109, SR-127, SR-128 |
| **Fn-05** | Derive the gate/stage from artifact states (rows IN → gate OUT), never hand-set | SN-004 | SR-049, SR-139, SR-140 |
| **Fn-06** | Select and run the harness steps for that gate; never green over a skip | SN-004, SN-008, SN-014 | SR-006, SR-110, SR-133 |
| **Fn-07** | Lint document currency, navigability, refs, figures, flows | SN-010, SN-021 | SR-012, SR-013, SR-041, SR-136 |
| **Fn-08** | Lint code substance and budgets (stubs, perf, coverage, vendored drift) | SN-008, SN-021 | SR-014, SR-015, SR-016, SR-022, SR-110 |
| **Fn-09** | Enforce the always-on privacy/secrets floor at the git crossing | SN-009 | SR-017, SR-018, SR-019, SR-020, SR-021 |
| **Fn-10** | Generate derived views and refuse to let them silently rot (`--check`) | SN-010, SN-021, SN-023 | SR-023, SR-024, SR-025, SR-033, SR-042, SR-112, SR-122 |
| **Fn-11** | Render the trajectory/decomposition dashboard a human reads | SN-023 | SR-050, SR-052..SR-056, SR-070, SR-071, SR-072, SR-089..SR-092 |
| **Fn-12** | Declare architecture boundaries and interfaces; check that every crossing is covered | **SN-037, SN-040** | SR-073, SR-074, SR-075, SR-076, SR-077, SR-087, SR-088 |
| **Fn-13** | Compute the ready frontier over the WI DAG, deterministically and safety-classified | SN-027 | SR-057, SR-059, SR-060, SR-093, SR-094, SR-115, SR-116 |
| **Fn-14** | Run an unattended coordinator session: resume from text, never block, fail clearly | SN-006, SN-015..SN-020, SN-025, SN-029 | SR-026, SR-027, SR-028, SR-029, SR-030, SR-148 |
| **Fn-15** | Route a job to a model family/tier and escalate on a fixed ladder | SN-026 | SR-040, SR-079, SR-082, SR-083 |
| **Fn-16** | Score review substance; adjudicate subjective acceptance against a written rubric | SN-024 | SR-081, SR-084, SR-085, SR-086, SR-123, SR-145 |
| **Fn-17** | Decompose work by rival plans and compare their coverage | SN-036 | SR-078, SR-102..SR-108, SR-124, SR-125 |
| **Fn-18** | Serialize mutation of the integration branch (lease, merge, trunk step, recover) | SN-027 | SR-130, SR-131, SR-132, SR-134, SR-143, SR-144 |
| **Fn-19** | Present open decisions to the owner and record the ruling verbatim | SN-029 | SR-135, SR-141, SR-142, SR-146 |
| **Fn-20** | Report toolchain/portability fitness across OS and interpreter | SN-011, SN-013, SN-014 | SR-034, SR-035, SR-114 |

Two functions have **no module of their own today** and are the load-bearing
new ones for part A: **Fn-12** (SN-037 "a stakeholder can see where each
promised behavior enters or leaves the system" and SN-040 "a repeatable
explanation for why the system was divided into its chosen components") is
exactly what this pack is an input to, and **Fn-02**'s "one dial, one home"
obligation is discharged by three duplicated readers (§4, B7).

---

## 3. Current-state coupling data

### 3a. The import graph over `project-trajectory/scripts/`

**55 modules, 32 of them importing at least one sibling, 97 internal import
edges.** The AST-derived graph is **byte-identical to the generated map** in
`docs/architecture.md` — 0 differences — so the arch map is a trustworthy
source for this figure.

<!-- fig: cmd="python - < appendix-A-1 (analyze.py); python - < archdiff (see §3a note)", rev=81a142c2 -->

```
adjudicate_brief -> agent_common, dispatch, handback, prompts, spine_carrier
agent_common     -> agent_session
agent_loop       -> adjudicate_brief, agent_common, agent_route, agent_session,
                    dispatch, intake, plan_round, plan_runner, prompts,
                    score_reviews, spine_carrier
agent_route      -> spine_carrier
check_doc_refs   -> gen_arch_map, spine_carrier
check_docs       -> spine_carrier
check_figures    -> check_doc_refs
check_flows      -> spine_carrier
check_trajectory -> check_docs, spine_carrier
derive_gate      -> spine_carrier
dispatch         -> agent_common, gen_trajectory, handback, intake, integrate,
                    lane, schedule, trace
gen_okf          -> spine_carrier
gen_open_items   -> gen_trajectory, spine_carrier, trace
gen_prompt_catalog -> prompts
gen_release_checklist -> spine_carrier
gen_trajectory   -> check_trajectory, traj_graph, traj_panels, traj_parse,
                    traj_render, traj_status, traj_views
handback         -> agent_common, integrate, spec_move
intake           -> agent_common, check_trajectory, dispatch, schedule,
                    spine_carrier, trace, wi_convert
integrate        -> agent_common, handback, intake, schedule, score_reviews, spec_move
lane             -> agent_common, integrate
plan_artifacts   -> trace, wi_convert
plan_briefs      -> prompts, spine_carrier
plan_coverage    -> spine_carrier
plan_runner      -> agent_route, agent_session, plan_artifacts, plan_briefs,
                    plan_coverage_step, plan_round
spec_move        -> agent_common
trace            -> spine_carrier, trace_text
traj_panels      -> integrate, schedule, traj_graph, traj_parse, traj_render, traj_status
traj_parse       -> check_trajectory, schedule, spine_carrier
traj_render      -> traj_graph
traj_status      -> check_trajectory, traj_parse
traj_views       -> check_trajectory, traj_graph, traj_parse, traj_render
trunk_step       -> plan_artifacts, spine_carrier
```

**Fan-in (the shared-service signal).** A module imported by many others is a
shared service whether or not the architecture says so:

| Fan-in | Module | | Fan-in | Module |
|-------:|--------|-|-------:|--------|
| **17** | `spine_carrier` | | 4 | `traj_graph`, `traj_parse` |
| **8** | `agent_common` | | 3 | `dispatch`, `handback`, `agent_session`, `intake`, `traj_render` |
| 5 | `schedule`, `check_trajectory` | | 2 | 8 modules |
| 4 | `prompts`, `integrate`, `trace` | | 1 | 13 modules |

`spine_carrier` at 17 importers is the clearest shared-service signal in the
tree; `agent_common` at 8 is second. **Neither has its own component today** —
`spine_carrier` sits inside CMP-001 and `agent_common` is one of the five
double-tagged modules.

### 3b. LLR `Module` → `Component` tagging

**59 distinct `Module` values** across 149 live LLR rows (55 `.py` scripts + 2
hooks + 2 shell templates), all tagged, **zero untagged arch-map modules**.

<!-- fig: cmd="python - < appendix-A-1 (analyze.py) | jq '.module_count, .llr_total, .scripts_untagged'", rev=81a142c2 -->

> **Discrepancy, declared:** OI-14's decision cell states **70** distinct
> `LLR.Module` values (measured 2026-08-12). I reproduce **59** at `81a142c2`
> by splitting the `;`-joined cell and dropping `-000` rows — the same rule
> `check_trajectory.module_components` applies. I could not reproduce 70 by any
> reading. The 5-multi-tagged-module figure, the 149 LLR rows and the 147 SRs
> all reproduce exactly, so the 70 is likely a stale or differently-scoped
> count. **Do not carry 70 forward without re-deriving it.**

**Exactly 5 modules carry LLRs tagged into two components** — the same five
OI-14 names, no others:

| Module | Components | Why it is evidence |
|--------|-----------|--------------------|
| `bootstrap.py` | CMP-002 + CMP-005 | scaffolder *and* generator |
| `agent_common.py` | CMP-002 + CMP-004 | 8 importers; the de-facto kernel |
| `agent_session.py` | CMP-002 + CMP-004 | CLI launch *and* prompt assembly |
| `derive_gate.py` | CMP-001 + CMP-002 | spine reader *and* derived artifact |
| `handback.py` | CMP-003 + CMP-004 | report renderer *and* loop step |

**LLR rows per component:** CMP-004 = 51, CMP-002 = 49, CMP-001 = 31,
CMP-003 = 9, CMP-005 = 9.

### 3c. `SR.Area` values and their component spread

**31 non-empty `Area` values over 147 SRs; SR-049 carries no Area at all.**
Areas resolve to components through `LLR.sr_refs` → `LLR.component`.

<!-- fig: cmd="python - < appendix-A-1 (analyze.py) | jq '.areas, .area_to_cmp, .sr_no_area'", rev=81a142c2 -->

**Six Areas do not decompose into a single component** (five non-empty plus the
empty one), reproducing OI-14's "6 of 31":

| Area | SRs | Components spanned |
|------|----:|--------------------|
| `Process` | 10 | **4** — CMP-001, 002, 003, 004 |
| `Trajectory` | 27 | **4** — CMP-001, 002, 004, 005 |
| `Architecture connectivity` | 10 | 2 — CMP-001, 002 |
| `Unattended loop` | 13 | 2 — CMP-001, 004 |
| `Perf comparator + budgets` | 2 | 2 — CMP-001, 003 |
| *(empty — SR-049)* | 1 | 2 — CMP-001, 002 |

And one Area resolves to **no component at all**: `Portability` (3 SRs —
SR-034, SR-035, SR-114) has no LLR tagged into any component, because
portability is discharged by *every* module rather than one. That is a real
gap, not a tagging slip: Fn-20 has no home.

Full spread in §6.

### 3d. The current 5-component partition

`docs/requirements/components.csv`, with member modules per the LLR tagging
(`*` = double-tagged, counted in both):

| CMP | Name | Modules (from `LLR.Module` × `LLR.Component`) |
|-----|------|---------------------------------------------|
| **CMP-001** | Traceability core | `check`, `check_trajectory`, `derive_gate`\*, `plan_coverage`, `spine_carrier`, `trace`, `trace_text` — **7** |
| **CMP-002** | Generators | `agent_common`\*, `agent_session`\*, `bootstrap`\*, `derive_gate`\*, `gen_arch_map`, `gen_cases`, `gen_okf`, `gen_open_items`, `gen_prompt_catalog`, `gen_release_checklist`, `gen_skills_index`, `gen_trajectory`, `prompts`, `traj_graph`, `traj_panels`, `traj_parse`, `traj_render`, `traj_status`, `traj_views` — **19** |
| **CMP-003** | Quality checkers | `check_coverage`, `check_doc_refs`, `check_docs`, `check_figures`, `check_flows`, `check_perf`, `check_stubs`, `check_vendored`, `handback`\* — **9** |
| **CMP-004** | Unattended loop & floor | `adjudicate_brief`, `agent_common`\*, `agent_loop`, `agent_route`, `agent_session`\*, `check_privacy`, `dispatch`, `handback`\*, `intake`, `integrate`, `lane`, `plan_artifacts`, `plan_briefs`, `plan_coverage_step`, `plan_round`, `plan_runner`, `schedule`, `score_reviews`, `spec_move`, `subagent_gate`, `trunk_step`, + `hooks/pre-commit`, `hooks/pre-push` — **23** |
| **CMP-005** | Scaffold & onboarding | `bootstrap`\*, `migrate_carrier`, `run_menu`, `wi_convert`, + `dev-setup.template.sh`, `onboard.template.sh` — **6** |

### 3e. The enforcing check, and how much it actually polices

Reproduced exactly against `check_trajectory.cross_component_findings`:

<!-- fig: cmd="python - < appendix-A-2 census section (see §3e), rev=81a142c2" -->

| Measure | Value |
|---------|------:|
| internal import edges | **97** |
| classifiable (both endpoints component-tagged) | **97** |
| **suppressed because the two component sets OVERLAP** | **64** |
| …of which a **multi-tagged endpoint** caused the overlap | **17** |
| policed (component sets disjoint) | **33** |
| of those, covered by an IF row | **33** |
| **findings** | **0** |

Every figure OI-14 quotes reproduces. The fail-open is real and mechanical:
adding a component tag to a module can only *reduce* findings, and 17 edges are
silenced today by exactly that.

**The containment-rule guard, answered.** OI-14 asks whether the containment
rule covers the IF rows `cross_component_findings` is vacuous for. **It does
not — the two rules range over disjoint object classes.**

- **45 of 113** IF rows have at least one endpoint that carries no component
  tag, so `cross_component_findings` is vacuous for them; **68** are
  classifiable.
  <!-- fig: cmd="python - < appendix-A-2 vacuous section, rev=81a142c2" -->
  (OI-14 states 46/67 at 2026-08-12; I reproduce **45/68** at `81a142c2` using
  an exact replication of `_norm_module`. One row moved. Declared, not
  reconciled.)
- The untagged endpoints are **27 data-file/registry paths**, **14 external
  actors** (`downstream adopter` ×8, `agent CLI` ×2, `docs`, `git`,
  `upstream docs`, `run.* launchers`), and **4 directory paths**
  (`project-trajectory/scripts`, `.../skills`, `.../registries`,
  `docs/requirements`).
- `component_findings`' containment rule tests that every **arch-map module** is
  in some CMP. Its object is a *module*. A data file, a directory and an
  external actor are **never** arch-map modules, so containment cannot reach a
  single one of the 45.
- Containment is clean today (**0 uncontained modules**), which is exactly why
  reading its green as coverage of the 45 would be the fail-open OI-14 warns
  about.

**Verdict for the ruling: the 45 vacuous rows are covered by NOTHING.** They are
policed by neither rule.

---

## 4. Behaviour multi-home census

`tests/test_rule_sync.py` (907 lines) plus `tests/test_wi_loader_sync.py` are
the proxy census OI-14 names. I extended it by an AST census of duplicate
top-level symbol names across the 55 modules (**58 names defined in more than
one module**) and then **read each implementation**, because most are name
collisions rather than one behaviour.

<!-- fig: cmd="python - < appendix-A-2 (census.py), rev=81a142c2" -->

**Excluded after reading them** — same name, genuinely different behaviour:
`evaluate` (`check_coverage` per-module floor vs `check_perf` budget row vs
`schedule` WI readiness), `render_report` (four unrelated report bodies),
`_clip` (line-clip vs char-clip), `interface_findings` (different signatures,
different rules), plus `main`, `digest`, `emit`, `esc`, `load`, `preflight`,
`render`, `rel`. Counting these would have inflated every candidate's straddle
count. `_utf8_console` (**32 homes**) is excluded as declared F5 boilerplate
serving crossing M-19.

### The verified census — 12 behaviours, 39 (behaviour, home) pairs

| # | Behaviour | Homes | Pinned? | Candidate owner |
|---|-----------|-------|---------|-----------------|
| **B1** | `is_example` — is this a `-000` placeholder row | `derive_gate`, `gen_release_checklist`, `trace_text` (3) | yes | spine carrier / registry |
| **B2** | declared-line reader — first non-empty non-comment line of a one-word policy file | `agent_common`, `subagent_gate`, `bootstrap`, `check_privacy`, `check_trajectory` (5) | yes | policy/dial reader |
| **B3** | `value_to_cell` writer ↔ reader inverse | `migrate_carrier`, `spine_carrier` (2) | yes | registry carrier |
| **B4** | gate-policy predicates (`is_draft`/`is_verified`/`is_modified`/`llr_exempt`/`phase_num`) | `derive_gate`, `trace`, `trace_text` (3) | yes | gate derivation |
| **B5** | SN id scrapes (`sn_draft_ids`/`sn_all_ids`/`sn_cited_ids`) | `derive_gate`, `trace` (2) | yes | spine carrier |
| **B6** | SN row/field reader (`_sn_rows`/`sn_rows`/`_sn_prose`) | `traj_parse`, `gen_okf`, `trace` (3) | yes | spine carrier |
| **B7** | `[checks]` enablement reader (`docs/process.toml`) | `check_trajectory`, `gen_okf`, `subagent_gate` (3) | yes | policy/dial reader |
| **B8** | WI registry + spec-folder reader (`load_wis`, `parse_spec_*`, `read_spec_rows`, `spec_files`) | `agent_common`, `check_trajectory`, `schedule` (3) | yes (`test_wi_loader_sync`) | WI registry service |
| **B9** | spine-carrier column↔key vocabulary | `trace`, `check_trajectory`, `migrate_carrier` (3) | yes | registry carrier |
| **B10** | **ref splitting** (`refs`/`split_refs`/`_split_refs`) | `derive_gate`, `trace_text`, `check_trajectory`, `schedule`, `gen_okf`, `plan_coverage` (6) | **NO** | registry carrier |
| **B11** | plain `load_csv` | `derive_gate`, `gen_release_checklist`, `trace` (3) | **NO** | registry carrier |
| **B12** | `_norm_module` — module path → naming-neutral key | `check_trajectory`, `gen_arch_map`, `trace` (3) | **NO** | architecture service |

### New finding: B10 is a live, unpinned, DIVERGENT six-home behaviour

Five homes split on `[;,\s]+`; **`plan_coverage.split_refs` splits on `[;,]`
only** — it does not split on whitespace. Demonstrated:

```
'SR-001 SR-002'   5-home: ['SR-001','SR-002']   plan_coverage: ['SR-001 SR-002']   *** DIVERGES
'SR-001;SR-002'   5-home: ['SR-001','SR-002']   plan_coverage: ['SR-001','SR-002']  agree
'SR-001, SR-002'  5-home: ['SR-001','SR-002']   plan_coverage: ['SR-001','SR-002']  agree
'SR-001\tSR-002'  5-home: ['SR-001','SR-002']   plan_coverage: ['SR-001\tSR-002']   *** DIVERGES
```

<!-- fig: cmd="python -c \"import re; a=lambda c:[t for t in re.split(r'[;,\\s]+',(c or '').strip()) if t]; b=lambda c:[t.strip() for t in re.split(r'[;,]',c) if t.strip()]; print([(s,a(s),b(s)) for s in ['SR-001 SR-002','SR-001;SR-002']])\" rev=81a142c2" -->

This is the **same class** as the three OI-14 pins — one behaviour, several
homes, and they disagree — found by census rather than by a check, and **not
yet pinned by anything**. It matters beyond tidiness: OI-12's decision cell
records that whitespace-splitting `refs()` produced the "SN-001-and-SN-002
orphan bug", so the six homes disagree about a rule that has already caused a
real defect, and no test says which one is right. `plan_coverage` is also the
one home whose *component* differs (CMP-001 vs the others).

**B11 carries a smaller divergence of the same shape:** `derive_gate.load_csv`
and `trace.load_csv` pass `errors="replace"`; `gen_release_checklist.load_csv`
does not — so a non-UTF-8 byte in a registry is tolerated by two homes and
raises in the third. Also unpinned.

### The shared-service signal from the import graph

`spine_carrier` (fan-in **17**) and `agent_common` (fan-in **8**) are the two
modules a 10-plus-importer heuristic flags. Note the interaction with the
behaviour census: **`spine_carrier` is a home for B3, B9** and `agent_common`
is a home for **B2, B8**. The de-facto shared services are already the homes of
the contested behaviours — which is what makes "a shared service becomes its own
component" (OI-14's prescribed resolution) the structurally indicated move,
and simultaneously what makes it collide with F5 (§0).

---

## 5. Candidate partitions

Five candidates. **P1 is the honest floor** (closest to today's five that
assigns each module exactly one home). P2–P5 are derived from §1's boundary and
§2's functions, not from clustering the current tree.

Every candidate assigns **all 55 scripts to exactly one component** —
verified: `missing: [] dup: [] extra: []` for all five.

Metrics, all from one scorer over the §3a graph and the live IF registry:

- **cut count** = cross-component import edges (of 97).
- **IF rows owed** = distinct cross-component module pairs — the interface rows
  the partition forces into existence.
- **new IF rows** = of those, the ones with no covering row today.
- **boundaries** = distinct component pairs that touch.
- **rework** = modules leaving every current tag, after best-overlap matching
  each new component to the today-CMP it most overlaps (so a rename is not
  scored as a move).
- **straddle** = of the 12 verified behaviours, how many span >1 component.

<!-- fig: cmd="python - < appendix-A-2 (score.py), rev=81a142c2" -->

### Summary table

| | Cmps | Cut (edges) | IF rows owed | New IF rows | Boundaries | Straddle /12 | Modules moved | Multi-tags resolved |
|--|----:|------------:|-------------:|------------:|-----------:|-------------:|--------------:|--------------------:|
| **P1** minimal-change | 5 | **33** | 33 | **0** | 6 | 10 | **0** | 5 |
| **P2** shared-kernel | 6 | 48 | 48 | 11 | 10 | **11 (worst)** | 2 | 4 |
| **P3** actor-boundary | 5 | **30 (best)** | **30 (best)** | 1 | 8 | 10 | 8 | 5 |
| **P4** functional | 9 | 48 | 48 | **15 (worst)** | 12 | 9 | 5 | 5 |
| **P5** narrow-waist | 4 | 31 | 31 | **0** | **4 (best)** | **7 (best)** | 8 | 5 |

**No candidate reaches zero straddle** (§0). **No candidate meets Core's
narrow-waist target of ≤6 IF rows per component boundary** on more than two
components — see the per-component numbers below.

---

### P1 — minimal-change (the floor)

Today's five components, each of the five double-tagged modules resolved to one
home: `bootstrap`→CMP-005, `agent_common`→CMP-004, `agent_session`→CMP-004,
`derive_gate`→CMP-001, `handback`→CMP-004. Missions unchanged from
`components.csv`.

- **Cut 33 · IF rows owed 33 · new IF rows 0 · boundaries 6 · straddle 10/12**
- **Rework: zero modules move.** Only the five multi-tags narrow. This is the
  cheapest thing that satisfies one-module-one-component.
- **IF rows per component:** CMP-001 **23**, CMP-004 **19**, CMP-002 **17**,
  CMP-003 5, CMP-005 2 — three components far over the ≤6 waist.
- **Straddling behaviours:** B1, B2, B3, B6, B7, B8, B9, B10, B11, B12.
- **Honest reading:** it changes nothing except deleting the fail-open
  (17 suppressed edges become policed, because no endpoint is multi-tagged any
  more). It ratifies the accident A1 was refuted for. Its value in the ranking
  is as the zero-cost baseline every other candidate must beat by enough to
  justify its rework.

### P2 — shared-kernel extracted

Today's five, plus a sixth component owning the de-facto shared services.

| Component | Mission |
|-----------|---------|
| **K** Spine kernel | the shared service every other component reads: carrier, text rules, prompts, session-common |
| CMP-001..005 | unchanged missions, minus the four kernel modules |

Assignment: **K** = `spine_carrier`, `trace_text`, `prompts`, `agent_common`.

- **Cut 48 · IF rows owed 48 · new IF rows 11 · boundaries 10 · straddle 11/12 (worst)**
- **Rework:** 2 modules leave every current tag (`agent_common`, `prompts`);
  4 multi-tags narrow.
- **IF rows per component:** K **31**, CMP-004 **28**, CMP-001 15, CMP-002 15,
  CMP-003 5, CMP-005 2.
- **Straddling:** all but B5.
- **Honest reading: this candidate is a trap and should rank low.** Extracting
  the shared services *without collapsing the duplicated behaviours into them*
  makes everything worse: the cut jumps 33→48, the straddle jumps 10→11, and K
  becomes a 31-crossing hub. It is the measured proof that "extract a shared
  component" only pays if the copies are deleted at the same time — which is
  code work (§0), not partition work. Included precisely because it is the move
  a reader would reach for first.

### P3 — actor-boundary (derived from §1)

One component per **external actor class** from the boundary inventory.

| Component | Mission (one line) |
|-----------|--------------------|
| **A** Adopter surface | everything an adopting repo invokes or receives at set-up and conversion time |
| **B** Spine service | own the requirement spine: carry it, join it, derive the gate from it |
| **C** Verification harness | the surface CI and the git hooks call; every gate-time verdict |
| **D** Owner view surface | every artifact a human owner reads |
| **E** Agent autonomy surface | everything an LLM agent (coordinator or direct session) drives |

Assignment (55/55):
**A** = `bootstrap`, `migrate_carrier`, `wi_convert`, `run_menu`,
`gen_skills_index`, `gen_cases`, `gen_release_checklist` (7).
**B** = `spine_carrier`, `trace`, `trace_text`, `derive_gate`, `plan_coverage` (5).
**C** = `check`, `check_privacy`, `check_trajectory`, `gen_arch_map`,
`check_coverage`, `check_doc_refs`, `check_docs`, `check_figures`,
`check_flows`, `check_perf`, `check_stubs`, `check_vendored` (12).
**D** = `gen_trajectory`, `gen_open_items`, `gen_okf`, `gen_prompt_catalog`,
`traj_graph`, `traj_panels`, `traj_parse`, `traj_render`, `traj_status`,
`traj_views` (10).
**E** = `adjudicate_brief`, `agent_common`, `agent_loop`, `agent_route`,
`agent_session`, `plan_artifacts`, `plan_briefs`, `plan_coverage_step`,
`plan_round`, `plan_runner`, `dispatch`, `handback`, `intake`, `integrate`,
`lane`, `prompts`, `schedule`, `score_reviews`, `spec_move`, `subagent_gate`,
`trunk_step` (21).

- **Cut 30 (best) · IF rows owed 30 (best) · new IF rows 1 · boundaries 8 · straddle 10/12**
- **Rework: 8 modules move** — `check`, `check_privacy`, `check_trajectory`,
  `gen_arch_map`, `gen_cases`, `gen_release_checklist`, `gen_skills_index`,
  `prompts`; plus 5 multi-tags narrowed.
- **IF rows per component:** B **18**, E **17**, D **13**, C 9, **A 3** (only A
  meets the waist).
- **Straddling:** B1, B2, B3, B6, B7, B8, B9, B10, B11, B12.
- **Files that would split:** `check_trajectory` is the sharpest — it is a
  *validator* (belongs in C) that also owns the WI-registry reader B8 and the
  arch-map/component join, which serve B and D. Under a strict one-home reading
  it splits three ways.
- **New IF row needed:** 1 (the single cross pair with no covering row today).
- **Honest reading:** lowest cut of all five and near-zero new interface work,
  because actor boundaries happen to align with how the tree already
  communicates. It is derived from §1 rather than from the tree, which is what
  A3 asks for. Its weakness is that "owner view" and "agent surface" are
  *audience* distinctions, and Parnas asks what changes together — a dashboard
  and a decision-brief view may not.

### P4 — functional (derived from §2)

One component per signal transformation, at the granularity §2 names.

| Component | Mission |
|-----------|---------|
| **F1** Registry carrier | read and write the requirement registries in one carrier vocabulary |
| **F2** Spine conformance | join the spine, police its integrity, derive the gate and the architecture join |
| **F3** Gate harness | select and run the steps the derived gate requires |
| **F4** Artifact lints | every doc/code quality verdict at its declared gate |
| **F5** Safety floor | the always-on privacy and spawn-control floor |
| **F6** View generation | every generated, freshness-gated view |
| **F7** Work flow & integration | frontier, dispatch, lease, merge, trunk step |
| **F8** Agent session & planning | launch a model, assemble briefs, run rival-plan rounds |
| **F9** Scaffold | zero-to-running for an adopting repo |

Assignment (55/55): **F1** = `spine_carrier`, `trace_text`, `migrate_carrier`,
`wi_convert`. **F2** = `trace`, `check_trajectory`, `derive_gate`,
`plan_coverage`, `gen_arch_map`. **F3** = `check`, `check_coverage`.
**F4** = `check_docs`, `check_doc_refs`, `check_figures`, `check_flows`,
`check_perf`, `check_stubs`, `check_vendored`. **F5** = `check_privacy`,
`subagent_gate`. **F6** = the 7 `gen_*` (minus `gen_arch_map`) + the 6
`traj_*`. **F7** = `schedule`, `dispatch`, `lane`, `intake`, `integrate`,
`trunk_step`, `spec_move`, `handback`. **F8** = the 5 `agent_*`, the 5
`plan_*`, `prompts`, `score_reviews`. **F9** = `bootstrap`, `run_menu`.

- **Cut 48 · IF rows owed 48 · new IF rows 15 (worst) · boundaries 12 · straddle 9/12**
- **Rework: 5 modules move** — `check_coverage`, `gen_arch_map`,
  `migrate_carrier`, `prompts`, `wi_convert`; plus 5 multi-tags narrowed.
- **IF rows per component:** F7 **22**, F1 **20**, F8 **19**, F2 **16**,
  F6 **14**, F4 5, and **F3, F5, F9 at 0** — three components meet the waist by
  having no internal coupling at all.
- **Straddling:** B1, B2, B4, B6, B7, B8, B9, B10, B11.
- **Honest reading:** the finest-grained candidate and the most faithful to the
  ruled method — nine components for twenty functions, each traceable to §2. It
  buys the second-lowest straddle at the highest interface cost: **15 interface
  rows that do not exist today** must be written before the check is honest. Its
  distinguishing merit is that F3/F5/F9 are genuinely decoupled leaves, which is
  what a good partition looks like; its distinguishing cost is F7 at 22
  crossings, which says the work-flow cluster is not one component.

### P5 — narrow-waist (Core-style)

Four coarse components, placing boundaries where the fewest signals cross —
Core's rule (`docs/knowledge/system-decomposition-methods.md` via OI-14's
external-evidence section).

| Component | Mission |
|-----------|---------|
| **W1** Registry & conformance | the spine and everything that decides whether it holds |
| **W2** Gatekeeper | every verdict a hook, CI job or gate run consumes |
| **W3** Autonomy | the unattended coordinator end to end |
| **W4** Human & adopter surfaces | everything a person or an adopting repo reads or runs |

Assignment (55/55): **W1** = `spine_carrier`, `trace`, `trace_text`,
`derive_gate`, `check_trajectory`, `plan_coverage`, `migrate_carrier`,
`wi_convert`, `gen_arch_map` (9). **W2** = `check`, `check_privacy`,
`subagent_gate` + the 8 `check_*` lints (11). **W3** = the 5 `agent_*`, 5
`plan_*`, `dispatch`, `handback`, `intake`, `integrate`, `lane`, `prompts`,
`schedule`, `score_reviews`, `spec_move`, `trunk_step` (20). **W4** =
`bootstrap`, `run_menu`, the 7 `gen_*`, the 6 `traj_*` (15).

- **Cut 31 · IF rows owed 31 · new IF rows 0 · boundaries 4 (best) · straddle 7/12 (best)**
- **Rework: 8 modules move** — `check`, `check_privacy`, `gen_arch_map`,
  `migrate_carrier`, `prompts`, `run_menu`, `subagent_gate`, `wi_convert`; plus
  5 multi-tags narrowed.
- **IF rows per component:** W1 **26**, W3 **17**, W4 **14**, **W2 5** (meets
  the waist).
- **Straddling:** B1, B2, B6, B7, B8, B10, B11 — it is the only candidate that
  puts B3 (`value_to_cell`), B4 (gate policy), B9 (carrier vocabulary) and B12
  (`_norm_module`) each inside a single component.
- **Honest reading:** best on every structural measure that is not raw cut — 4
  boundaries, 0 new interface rows, and the lowest behaviour straddle — for the
  same 8-module rework as P3. Its cost is coarseness: W1 at 9 modules and 26
  crossings is a large component, and coarse components are the ones a later
  re-score most often splits. It is also the candidate whose shape most
  resembles Core's ratified answer, which the ruling names as the strongest
  external evidence available.

---

## 6. `SR.Area` verdict input

The decision: **does `Area` derive from `Component`, or does it retire?**

### What `Area` is today

- **31 distinct non-empty values** over 147 SRs; **SR-049 has none**.
- **Report-only by construction.** `trace.py` emits a per-Area count and, in its
  own words, "never a finding". It gates nothing, is validated against no
  vocabulary, and no other script reads it.
- Values range from a single SR (`Arch-map generation`, `Knowledge export`,
  `No-stub detector`, …) to 27 (`Trajectory`).

<!-- fig: cmd="python - < appendix-A-1 (analyze.py) | jq '.areas, .area_to_cmp'", rev=81a142c2 -->

### Does each Area map cleanly onto a candidate's components?

| Area | SRs | → today's CMPs | Clean under P1? | Clean under P5? |
|------|----:|----------------|:---:|:---:|
| Traceability | 8 | 001 | yes | yes |
| Off-spine registries | 1 | 001 | yes | yes |
| Gate harness | 2 | 001 | yes | yes |
| Declared stack profile | 2 | 001 | yes | yes |
| Arch-map generation | 1 | 002 | yes | yes |
| Knowledge export | 1 | 002 | yes | yes |
| Permutation case gen | 1 | 002 | yes | yes |
| Release checklist | 1 | 002 | yes | yes |
| Skills index + fan-out | 2 | 002 | yes | yes |
| Coverage floors | 1 | 003 | yes | yes |
| Doc currency | 2 | 003 | yes | yes |
| Doc navigability | 1 | 003 | yes | yes |
| No-stub detector | 1 | 003 | yes | yes |
| Runtime-flows check | 1 | 003 | yes | yes |
| Vendored-doc drift | 1 | 003 | yes | yes |
| Declared-policy readers | 1 | 004 | yes | yes |
| Dual-plan decomposition | 10 | 004 | yes | yes |
| Git hooks | 3 | 004 | yes | yes |
| Parallel dispatch | 25 | 004 | yes | yes |
| Parallel tracks | 2 | 004 | yes | yes |
| Secrets + privacy lint | 2 | 004 | yes | yes |
| Unattended coordinator | 4 | 004 | yes | yes |
| Conditional scaffold profiles | 1 | 005 | yes | yes |
| Onboarding + dev-setup | 3 | 005 | yes | yes |
| Scaffold generation | 4 | 005 | yes | yes |
| **Architecture connectivity** | 10 | 001, 002 | **no** | **no** |
| **Perf comparator + budgets** | 2 | 001, 003 | **no** | **no** |
| **Process** | 10 | 001, 002, 003, 004 | **no** | **no** |
| **Trajectory** | 27 | 001, 002, 004, 005 | **no** | **no** |
| **Unattended loop** | 13 | 001, 004 | **no** | **no** |
| **Portability** | 3 | *(none)* | **no** | **no** |
| *(empty, SR-049)* | 1 | 001, 002 | n/a | n/a |

**25 of 31 map cleanly onto exactly one of today's five components. Six do
not** — and five of those six are the *largest* Areas (`Trajectory` 27,
`Parallel dispatch` is clean at 25, `Unattended loop` 13, `Process` 10,
`Architecture connectivity` 10). `Portability` (3 SRs) maps to **no** component
at all.

### The input the verdict needs

- **If `Area` derives from `Component`:** 25 of 31 values become redundant
  labels for a component that already exists, and **6 values must be split or
  re-scoped**, affecting **65 of 147 SRs** (10+2+10+27+13+3). The five spanning
  Areas are not arbitrary — `Process`, `Trajectory` and `Unattended loop` span
  components because they are *cross-cutting concerns*, which is precisely the
  thing a component partition cannot express. Deriving Area from Component
  therefore **deletes information**, not just duplication.
- **If `Area` retires:** the loss is the cross-cutting view — the only column
  that groups SR-137..SR-146 (`Process`) as one concern, since they discharge
  into four different components. Nothing mechanical breaks: it gates nothing
  and only `trace.py`'s report reads it.
- **A third shape the measurement suggests, offered as data not recommendation:**
  the six spanning Areas behave like *aspects* rather than *domains*. If the
  ruling wants to keep a review-hat axis, the honest form is a small closed
  vocabulary of cross-cutting concerns validated by a schema tier — not 31
  free-text values validated by nothing. The measured fact that motivates this:
  25 of 31 values are *already* a component by another name, and the 6 that are
  not are the ones carrying 44% of the SRs.
- **Whatever is ruled, `Portability` needs an answer of its own.** Its 3 SRs
  reach no component because portability is discharged by every module. It is
  Fn-20 with no home, and it is a gap in the *component* model, not in `Area`.

---

## Appendix A — derivation scripts

The three scripts every marker above refers to. Each is stdlib-only and
runs against a checkout at `81a142c2`; set `ROOT` to the repo root.

### A-1 `analyze.py` — registries, areas, import graph

Parses `interfaces.csv`, `components.csv`, the three spine TOMLs, and walks the
AST of every `project-trajectory/scripts/*.py` collecting sibling imports.
Emits one JSON object with `if_total`, `if_external_rows`, `module_count`,
`multi_tagged_modules`, `cmp_to_mods`, `areas`, `area_to_cmp`, `sn_total`,
`sr_total`, `script_count`, `edge_count`, `edges`, `fan_in`,
`scripts_untagged`. Cross-checked against `docs/architecture.md`'s generated
`Imports (internal):` lines — **32 sources / 97 edges on both sides, 0
differences**.

```python
import ast, csv, collections, json, pathlib, tomllib
ROOT = pathlib.Path(".")                      # repo root
REQ, SCR = ROOT / "docs/requirements", ROOT / "project-trajectory/scripts"

rows = [r for r in csv.DictReader((REQ / "interfaces.csv").open(newline="", encoding="utf-8"))
        if r["IF-ID"] and not r["IF-ID"].endswith("-000")]
print("if_total", len(rows))
print("if_external_rows", sum(1 for r in rows if "/" not in r["Counterpart"].strip()))

llr = tomllib.loads((REQ / "low-level-requirements.toml").read_text(encoding="utf-8"))["design"]
mod_cmp = collections.defaultdict(set)
for lid, row in llr.items():
    if lid.endswith("-000"):
        continue
    for m in str(row.get("module", "")).split(";"):
        if m.strip():
            mod_cmp[m.strip()].add(str(row.get("component", "")).strip())
print("module_count", len(mod_cmp))
print("multi_tagged", {m: sorted(c) for m, c in mod_cmp.items() if len(c) > 1})

py = sorted(SCR.glob("*.py")); names = {p.stem for p in py}
edges = collections.defaultdict(set)
for p in py:
    for node in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            for a in node.names:
                b = a.name.split(".")[0]
                if b in names and b != p.stem:
                    edges[p.stem].add(b)
        elif isinstance(node, ast.ImportFrom) and node.module:
            b = node.module.split(".")[0]
            if b in names and b != p.stem:
                edges[p.stem].add(b)
print("script_count", len(py), "edge_count", sum(len(v) for v in edges.values()))
fan_in = collections.Counter(d for v in edges.values() for d in v)
print("fan_in", fan_in.most_common(5))
```

### A-2 `census.py` / edge accounting / vacuous rows

Three measurements sharing the membership map above.

```python
# duplicate top-level symbol names across the 55 modules
defs = collections.defaultdict(set)
for p in py:
    for node in ast.parse(p.read_text(encoding="utf-8")).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs[node.name].add(p.stem)
print("duplicate names", sum(1 for v in defs.values() if len(v) > 1))   # -> 58

# edge accounting, replicating check_trajectory.cross_component_findings
stem_cmp = collections.defaultdict(set)
for m, cs in mod_cmp.items():
    stem_cmp[pathlib.Path(m).stem] |= cs
covered = set()
for r in rows:
    a, b = pathlib.Path(r["ThisProject"].strip()).stem, pathlib.Path(r["Counterpart"].strip()).stem
    covered |= {(a, b), (b, a)}
E = [(s, d) for s, ds in edges.items() for d in ds]
cls = [e for e in E if stem_cmp.get(e[0]) and stem_cmp.get(e[1])]
ovl = [e for e in cls if stem_cmp[e[0]] & stem_cmp[e[1]]]
print(len(E), len(cls), len(ovl),
      len([e for e in ovl if len(stem_cmp[e[0]]) > 1 or len(stem_cmp[e[1]]) > 1]),
      len([e for e in cls if not (stem_cmp[e[0]] & stem_cmp[e[1]])]))
#   -> 97 97 64 17 33

# vacuous IF rows: exact replication of check_trajectory._norm_module
EXTS = (".py",".ts",".tsx",".js",".jsx",".go",".rs",".java",".kt",".rb",
        ".cs",".c",".h",".cpp",".hpp",".sh",".ps1",".sql")
def norm(p):
    p = (p or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/"):]
    for e in EXTS:
        if p.endswith(e):
            return p[:-len(e)]
    return p
mem = collections.defaultdict(set)
for m, cs in mod_cmp.items():
    mem[norm(m)] |= {c for c in cs if c.startswith("CMP-")}
vac = [r for r in rows
       if not (any(mem.get(norm(x)) for x in r["ThisProject"].split(";"))
               and any(mem.get(norm(x)) for x in r["Counterpart"].split(";")))]
print("vacuous", len(vac), "classifiable", len(rows) - len(vac))   # -> 45 68
```

### A-3 `score.py` / `collapse.py` — candidate scoring

`score.py` holds the five assignments of §5 verbatim as `{component: [modules]}`
dicts plus the twelve-behaviour census of §4, and for each candidate computes:
cross-component edges over `edges`; distinct cross-component module pairs; the
subset not in `covered`; distinct component pairs; per-component crossing counts
against the ≤6 waist; behaviours whose homes span >1 component; and rework by
best-overlap matching each new component to the today-CMP it most overlaps.
`collapse.py` sums `len(homes) - 1` over the census (**27 copies**) and takes
the union of homes (**16 modules**).

```python
for name, groups in CANDIDATES.items():
    assign = {m: c for c, ms in groups.items() for m in ms}
    assert set(assign) == names and sum(len(v) for v in groups.values()) == 55
    cross = [(s, d) for s, d in E if assign[s] != assign[d]]
    pairs = {tuple(sorted(e)) for e in cross}
    straddle = {b for b, homes in BEHAVIOURS.items() if len({assign[h] for h in homes}) > 1}
    print(name, len(cross), len(pairs),
          len([p for p in pairs if p not in covered]),
          len({tuple(sorted((assign[s], assign[d]))) for s, d in cross}),
          len(straddle))
```

---

## Appendix B — what this pack does NOT settle

1. **The partition.** Ranked inputs only; §0's constraint conflict is prior to
   any choice and is an owner question.
2. **Whether "behaviour" means "policy".** F5 vs OI-14 (§0). Every straddle
   number changes depending on the answer.
3. **Part B** — what an interface row must say. Out of scope for WI-441.
4. **Volatility.** Every metric here is coupling. The Parnas criterion — which
   modules will *change* together — is not measured and cannot be; the pack's
   own source knowledge pack says so, and it is the criterion that most often
   decides whether a partition survives.
5. **The 70-vs-59 `Module` count and the 46-vs-45 vacuous-row count.** Both
   declared as discrepancies against OI-14's 2026-08-12 figures rather than
   silently reconciled.
