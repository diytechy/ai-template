# Project Log — Append-only history (kit meta-repo self-adoption)

The durable record for the kit's **self-adoption** of its own gated process
(IMPROVEMENT_PLAN.md Thread 47; the process itself is
[PROCESS.md](../project-trajectory/PROCESS.md) §5): gate sign-offs, review
verdicts, ratified decisions, and session notes append here, **newest last**,
and are never rewritten. The working surface — what to do *next* — lives in
[status.md](status.md). This file is **evidence, never normative**: a rule
belongs in the process doc or a registry, not a log entry. The kit's *design
history* is the IMPROVEMENT_PLAN threads; this log is the gate-walk record of
applying that design to the kit itself.

---

## Gate Sign-offs

| Gate | Stakeholder | UX/Docs | System Eng | Test Eng | Human |
|---|---|---|---|---|---|
| G1 — Requirements/UX/Constraints | MET 2026-07-07 | MET 2026-07-07 | MET 2026-07-07 | n/a | ✅ Peter Johnson 2026-07-07 |
| G2 — Decomposition & Test Coverage | n/a | n/a | MET 2026-07-07 | MET 2026-07-07 | ✅ Peter Johnson 2026-07-07 |
| G3 — Implementation | n/a | n/a | MET 2026-07-07 | MET 2026-07-07 | ✅ Peter Johnson 2026-07-07 |

## Decisions log

_Ratified or executed decisions only — the call, the alternatives passed over,
why (one bullet each; cite ids)._

- **2026-07-07 — SR-011 split; SR-036 added (post-G2 spec review).** The G2
  review found SR-011 described the *ADOPTING.md §6 re-sync process* ("overwrite
  kit-owned, preserve project-owned") rather than what `bootstrap.py` mechanically
  does (idempotent skip-all-existing / `--force` overwrite-all, plus a
  `docs/kit-version` stamp; it has no kit-vs-project notion — `test_bootstrap.py::
  test_rerun_skips_existing_files`). Corrected SR-011 to the mechanical
  idempotency guarantee (Verification=Test, LLR-011 re-scoped to `write_kit_version`)
  and added **SR-036** for the deliberate, operator-driven re-sync integration
  (Verification=Inspection, LLR-exempt, TC-036 → ADOPTING.md §6 + the
  `downstream-resync` skill). Rejected: folding the process nuance into SR-011,
  which would conflate tool mechanism with human process and make the SR
  untestable. Spine now SN=22 SR=36 LLR=32 TC=36, orphans=0; the earlier G2
  DRIVER block's 35/35 counts predate this refinement. Surfaced by the Thread 47
  dogfood (a requirement that described the process, not the tool).

## Audit log

<!-- Append verdict blocks here per PROCESS.md §5. Newest at the bottom. -->

### DRIVER — G1 — Round 1 — 2026-07-07
Thread 47 (self-adoption) started. Phase 1 laid the layout: `docs/stack.ini`
(`src=project-trajectory/scripts`, `tests=tests`), `docs/gate` (G1), the
`docs/requirements/` + `docs/test/` registries, and this log. Phase 2 authored
the Stakeholder Needs (`docs/requirements/stakeholder-needs.md`, SN-001..) from
the README `PROJECT-VISION`. `SR→LLR→TC` decomposition (Thread 47 phases 3–5) is
the next session; `trace.py --strict` orphans are a G2 bar, not gated at G1.

### DRIVER — G2 — Round 1 — 2026-07-07 (session 2, phases 3–5)
Authored the `SR → LLR → TC` spine that decomposes the SNs and back-maps to the
existing suite: **35 SR** (`system-requirements.csv`, one cluster per shipped
script/hook/policy), **32 LLR** (`low-level-requirements.csv`, one design-tier
LLR per `Test`-verified SR — the `trace.py` orphan floor), **35 TC**
(`test-cases.csv`, one per SR, each citing the pytest node path in `Parameters`).
SR-033/034/035 are `Inspection`/`Analysis` (release-checklist has no dedicated
test yet; stdlib-only + stack-agnostic/portability are inspected, not executed) —
legitimately LLR-exempt, each still carrying a TC. Every SN-001..022 is cited by
≥1 SR. Authored [`docs/architecture.md`](architecture.md) with the **G2 Runtime
flows** (3 Mermaid sequence diagrams — coordinator, scaffold/re-sync, secrets
floor — citing 24 real SR/LLR ids) that `check_flows.py` requires at G2
(PROCESS.md §3); the *generated* module map stays deferred to phase 6.

**Mechanized verification (the G2 bar):**
- `trace.py --strict --no-placeholders --strict-schema` → `SN=22 SR=35 LLR=32
  TC=35 orphans=0 integrity=0 placeholders=0 schema-findings=0`.
- `check.py --gate G2` (wired from `docs/gate`) → **PASS** (traceability ·
  privacy · doc-navigability · design-flows).
- `pytest -q` → **358 passed, 2 skipped**.
- `check_docs.py --root . --stale` → OK, 12 docs, 60 links, 0 broken, 0 orphans.

`docs/gate` bumped G1 → **G2**. **Human ratification PENDING** (`docs/gate-policy`
= attended): the mechanical bar is met; the maintainer's attended approval of the
G1+G2 advance is still outstanding.

**Deviation from the session-2 brief.** The brief sequenced `docs/architecture.md`
entirely into phase 6, but the `design-flows` step is part of the **G2** harness
plan and `check_flows.py` hard-fails without a "Runtime flows" section — which
PROCESS.md §3 correctly places at G2 (flows are authored *with the LLRs*). So the
Runtime-flows section was pulled forward this session to keep the G2 gate honest;
only the generated module map (`gen_arch_map.py`, a G3 arch-map-freshness step)
remains deferred. **Kit-improvement finding filed** (IMPROVEMENT_PLAN.md Thread 47
phase-4 note): `test-cases.template.csv` has no test-evidence column, so the
concrete test is cited in `Parameters` as `node=…` — an `Evidence`/`Test` column
would be the cleaner model. Coverage `--tier full` stays deferred to phase 6
(subprocess-coverage instrumentation).

### REVIEW — G2 — Adversarial spine review — 2026-07-07
A fresh-context adversarial reviewer audited the spine + architecture flows + the
Thread 50 check before signoff. Mechanically clean (0/0/0/0) with all LLR symbols
resolving and full SN coverage, but it found honesty defects sitting on the
attestation surface, all fixed this round:
- **Fixed (major):** `architecture.md` Flow 2 still showed the corrected-away
  bootstrap "overwrite kit-owned / preserve project-owned" fiction — rewritten to
  skip-existing/`--force` + `docs/kit-version`, citing **SR-036**. SR-033 was
  labelled `Inspection` ("no automated test") though
  `test_check_perf.py::test_release_checklist_lists_perf_budgets` genuinely runs
  `gen_release_checklist.py` — reclassified to `Test` (+ **LLR-033**, TC-033 →
  the real node). SR-021 claimed `Verified` for the untested no-`python3` probe
  path — added `test_hook_skips_clearly_when_no_working_python3` (fake interpreters
  that exit nonzero, the Store-alias mode).
- **Fixed (minor):** SR-011 `--force` direction now tested
  (`test_force_overwrites_existing_files`); SR-006 / SR-035 / SR-017 acceptance
  criteria reworded to match what's actually tested (FAIL+`--lenient` SKIP, the
  macOS+3.8 matrix exclusion, the `docs/secrets-scan: off` opt-out); the Thread 50
  triangle tests deepened (multi-`SR-Refs` intersection + no-double-report).
  Stale `CLAUDE.md` CI line (Linux+Windows → +macOS) corrected.

Spine after fixes: **SN=22 SR=36 LLR=33 TC=36**, orphans=0; `check.py --gate G2`
→ **PASS**; `pytest -q` → **365 passed, 2 skipped**. **G2 human ratification
remains PENDING** — this review is evidence toward it, not the attestation itself.

### HUMAN RATIFICATION — G1 + G2 — 2026-07-07
Acceptor: **Peter Johnson** (owner; `docs/gate-policy` = `attended`). Ratifies the
closure of **G1** (Requirements/UX/Constraints) and **G2** (Decomposition & Test
Coverage) for the kit's self-adoption spine, on the mechanized bar plus the
adversarial review above.
- **Verification basis (trust footprint):** 36/36 SRs `Verified` — **33 Test**
  (runnable pytest), **2 Inspection** (SR-034 stdlib-only imports; SR-036 the
  ADOPTING.md §6 re-sync process), **1 Analysis** (SR-035 the CI portability
  matrix). **0 `Attest`** — nothing rests on a bare, unverifiable human judgment;
  the three non-Test SRs are re-inspectable/analyzable facts, not trust-only
  claims. (`trace.py`: mechanized=36, attested=0.)
- **Bar at ratification:** `trace.py --strict` orphans=0 integrity=0;
  `check.py --gate G2` → PASS; `pytest -q` → 365 passed, 2 skipped.

`docs/gate` remains **G2** (the active bar CI enforces); **G3** (implementation
back-links, coverage ≥ threshold, `--require-verified`) is the next milestone —
Thread 47 phases 6–7. No push (default `docs/push-policy` = human).

### DRIVER — G3 — Round 1 — 2026-07-07 (session 3, phases 6–7)
Walked the meta-repo to the **G3 (Implementation)** bar. Phase 6:
- **Subprocess coverage wired for real.** The suite runs the kit scripts as
  subprocesses (temp scaffold), which `--cov` missed in-process. `conftest.run_py`
  now starts coverage in each child (`COVERAGE_PROCESS_START` +
  `tests/_cov/sitecustomize.py`) and `.coveragerc`'s `[paths]` folds each
  temp-scaffold `*/scripts/` copy back onto the source tree. **Full-suite coverage
  ~82%**, so `docs/stack.ini`'s 80 is now a REAL enforced floor (was PROVISIONAL).
- **Generated arch-map** MODULE MAP block added to `docs/architecture.md`
  (`gen_arch_map --check` freshness, the G3 arch-map step). 3 drifted files
  `ruff format`ted.
- **check.py hardened** (`_step_env` strips ambient `COVERAGE_*`/`COV_CORE_*` so a
  project's own coverage run is authoritative, not corrupted by a parent coverage
  session) — a genuine robustness fix the dogfood surfaced.
- **CI** gains a `gate` job running `check.py` on the meta-repo (the phase-6
  "CI enforces the bar" item).
Phase 7: thread back-pointers were already seeded in SR `Rationale` (privacy ←
38/39/44/46, coordinator ← 33/45, tracks ← Parallel tracks, ERROR ← 45,
coherence ← 50).

**Mechanized verification (the G3 bar):** `check.py --gate G3` → **RESULT: PASS**
— all 9 steps green: format · lint · **tests+coverage (≥80%, ~82% measured)** ·
traceability (`--strict --no-placeholders --require-verified --strict-schema`:
orphans=0, status-findings=0) · privacy · doc-navigability · perf-budgets ·
design-flows · arch-map (`--check` fresh). `docs/gate` bumped G2 → **G3**.

**Human ratification PENDING** (`docs/gate-policy` = attended): the mechanized G3
bar is met; the maintainer's attested approval is outstanding. **Deviation:** the
coverage wiring was harder than the plan sketched — a trace-time `source` filter
in the child config silently produced empty data files; the fix was to let
children trace freely and remap paths at combine. **Byte-budgeted files:** none
touched. No push (`docs/push-policy` = human).

### REVIEW — G3 — Adversarial review + coverage-scoping correction — 2026-07-07
A fresh-context adversarial reviewer audited the phase-6/7 work before the G3
ratification. **No BLOCKERs — the gate reproduced green independently and was not
gamed (every measurement error found was pessimistic).** But it found the DRIVER
block's "~82%" was not the *product's* coverage, and fixed here:
- **Report was product+fixtures.** `.coveragerc` had no report scoping, so the
  agent-loop test fixtures (`fake_agent.py`, ~1061 stmts in temp dirs) folded into
  the TOTAL, understating the product. Added `[report] omit = */pytest-of-*/*`
  (runs AFTER the [paths] remap, so it drops the fixtures without touching the
  remapped script copies).
- **Uneven measurement.** `test_check_privacy.lint_env` and
  `test_pre_push_hook.run_hook` built their own subprocess env and bypassed the
  coverage wiring, so the whole privacy suite ran uninstrumented —
  `check_privacy.py` read a misleading 52%. Centralized the wiring as
  `conftest.augment_env` and routed both helpers through it; `check_privacy.py`
  now reads 91%.
- **Shipped hardening completeness.** Added `COVERAGE_RCFILE` to check.py's
  `_step_env` strip list (the only downstream-shipped fix).

**Corrected mechanized figure:** `check.py --gate G3` → **RESULT: PASS**;
`tests+coverage` → **366 passed, 2 skipped; product coverage 91%** (3273 stmts,
309 missed — the 14 kit scripts only), an 11-point margin over the 80 floor. This
supersedes the "~82%" in the DRIVER block above (that figure was product+fixtures,
measured unevenly). **Residual note:** the CI `gate` job's coverage path runs on
Linux only and the branch is unmerged, so it is unproven on CI — but the mechanism
is OS-agnostic and the margin is now wide. G3 human ratification still PENDING.

### REVIEW — G3 — Post-WI-1.41 coverage + arch-map regen — 2026-07-07
A second adversarial review (after WI-1.41) found `check.py --gate G3` actually
**FAILing**: WI-1.41 reworked `check_docs.check_inventory`'s docstring but did not
regenerate the code map, so the arch-map `--check` step (SN-021) reported
`docs/architecture.md` STALE. Regenerated (one line) and independently reproduced
**RESULT: PASS** (all 9 steps) from the committed state. The check_docs rework also
added one uncovered branch, so product coverage is now **3273 stmts / 310 missed
(90.53%)** — still 91%, still an 11-point margin over the 80 floor; this supersedes
the "309 missed" above by append (that figure was correct when measured, pre-WI-1.41).
Same review found the git-hook floor **dormant** here (no `.githooks/`,
`core.hooksPath` unset); WI-1.42 (interim) added a layout-adapted `.githooks/pre-commit`
and wired `core.hooksPath`, and `scripts/dev-setup.{sh,ps1}` now wire it on `--install`.
G3 human ratification still PENDING.

### RATIFICATION — G3 — Human sign-off (attended) — 2026-07-07
**Peter Johnson (owner/maintainer) ratifies G3.** `docs/gate-policy` = attended,
so the mechanized G3 bar requires a named human's sign-off; recorded here. This
resolves the sign-off outstanding since the DRIVER G3 walk (`docs/gate` was bumped
to **G3** during Thread 47; this is the deferred human ratification, not a bump).

**Basis of ratification (stated honestly):**
- **Mechanized bar reproduced independently.** `check.py --gate G3` → **RESULT:
  PASS** — all 9 steps (format · lint · tests+coverage · traceability · privacy ·
  doc-nav · perf · flows · arch-map), reproduced from committed HEAD (`pytest`:
  368 passed, 2 skipped; product coverage **90.53%** ≥ 80 floor; trace SN=22 SR=36
  LLR=33 TC=36, 0 orphans / integrity / schema / placeholder findings).
- **Four adversarial review passes, findings resolved** (see the REVIEW entries
  above): (1) a STALE arch-map that had G3 *actually FAILing* — regenerated;
  (2) the git-hook floor dormant — armed (`.githooks/pre-commit` + dev-setup
  wiring, WI-1.42 interim); (3) `.venv/` unignored — fixed; (4) came back clean
  save one LOW-severity doc-framing note.
- **Owner spot checks + the recorded review feedback** — ratified on that basis,
  **not** an exhaustive independent human re-derivation. The trust rests on the
  reproduced mechanized bar plus the review trail, sign-off by the named owner.

**Verification basis (attested vs mechanized — trace.py §4):** of 36 Verified SRs,
**36 mechanized, 0 attested** (33 Test · 1 Analysis · 2 Inspection — none rest on a
human `Attest`). The trust footprint is fully mechanical; nothing hidden behind an
attestation.

**Residual (disclosed, not blockers):** the CI `gate` job's coverage path is
Linux-only and this branch is unmerged (mechanism is OS-agnostic); the kit-level
onboarding-floor redesign stays tracked as **WI-1.42 (PROPOSED)**. No push
(`docs/push-policy` = human). **G3 is RATIFIED.**

---

## 2026-07-09 — SPINE CHANGE (WI-1.43 / WI-038 · THREAD_52_REVIEW F1): SR-037/038 added; G3 re-run PASS; re-attestation pending

**What changed (owner-authorized in-session, scope ruled by the owner):** the
trajectory layer's own code — the only untraced product scripts (F1, HIGH) — is now
on the spine. **SR-037** (work-item registry validation → `check_trajectory.py`,
LLR-034, TC-037 → `tests/test_trajectory.py`) and **SR-038** (offline project-state
view: single self-contained HTML, definition + execution completeness, the
SN→SR→LLR→TC hierarchy, the roadmap DAG, **usable on mobile viewports** →
`gen_trajectory.py`, LLR-035, TC-038 → `tests/test_gen_trajectory.py` + the new
`test_mobile_responsive_shell` mechanizing the mobile criterion). Future scope
(HOW view, root `PROJECT_STATE.html`, git-derived as-of) deliberately **not**
claimed — roadmapped as **WI-039**; Verified rows state only what is true today.
WI-038 (done) records the fix in the dogfood registry; the dashboard was
regenerated.

**Mechanized bar re-run (this session):** `check.py --gate G3` → **RESULT: PASS**
(11/11 steps incl. trajectory + trajectory-map); `pytest -q` **394 passed, 2
skipped**; trace **SN=22 SR=38 LLR=35 TC=38, 0 orphans / integrity / schema**.
Verification basis now: of 38 Verified SRs, **38 mechanized, 0 attested**
(35 Test · 1 Analysis · 2 Inspection).

**G3 re-attestation:** ✅ **re-attested 2026-07-09 — Peter Johnson (owner)**, given
in-session in direct response to the re-attestation request ("Looks good, you can
implement"), over the SR-037/038 spine change with the mechanized bar re-run above
(G3 PASS 11/11; SN=22 SR=38 LLR=35 TC=38, 0 orphans; 38/38 SRs mechanized).

## 2026-07-10 — SPINE CHANGE (the WI-1.48…1.52 grind batch): SR-039…042 added; SR-038/LLR-035/TC-038 extended; G3 re-run; RE-ATTESTATION PENDING

**What changed (owner-authorized in-session: "grind through all the queued WI, I
will review at a later point" — R4 registry-change path, review deferred by the
owner's own instruction):** four new SRs for four new product capabilities, each
with its LLR + TC, plus one Verified SR's text extended to newly-true claims:

- **SR-039** duplicate-code lint → `check_dupes.py`, LLR-036, TC-039 (WI-1.48).
- **SR-040** per-phase routing + review dial → `agent_loop.py`
  (`session_template`/`status_size_warning`), LLR-037, TC-040 (WI-1.49).
- **SR-041** doc reference validation → `check_doc_refs.py`, LLR-038, TC-041
  (WI-1.50).
- **SR-042** OKF knowledge-bundle export → `gen_okf.py`, LLR-039, TC-042
  (WI-1.51).
- **SR-038 extended** (WI-1.52): the root `PROJECT_STATE.html`, the How-SW
  module-map view, the optional CMP table, the git-derived as-of stamp
  (excluded from the `--check` compare) — superseding WI-1.43's "not claimed"
  scope note; LLR-035 + TC-038 texts updated to match.

Also in the batch, non-spine: the TC `Evidence` column (WI-1.47, ruled earlier
the same day) predates this entry's grind but rides the same re-attestation.

**Mechanized bar re-run (this session):** `check.py --gate G3` → **RESULT: PASS
(12/12** — the `okf` step joined the gate this batch; the first run caught a real
format FAIL on 6 not-yet-ruff-clean new files, fixed and re-run**)**;
`pytest -q` **445 passed, 2 skipped**; trace **SN=22 SR=42 LLR=39 TC=42,
0 orphans / integrity / schema**. Verification basis: of 42 Verified SRs,
**42 mechanized, 0 attested** (39 Test · 1 Analysis · 2 Inspection).

**G3 re-attestation:** ⏳ **PENDING the owner** — required (not merely
recommended): a Verified SR's text changed (SR-038) and four SRs were added to
the ratified spine. The ask is recorded as the `Needs <human>` item in
`docs/status.md`; three adversarial review reports (diff method/risk, diff
process/trace, full-repo) are queued as review input for the same sitting.

**Addendum (same day, review triage — WI-1.53):** three fresh-context adversarial
reviews of this batch (`REVIEW_GRIND_A/B/FULL`; 20 findings, no HIGH) landed fully
triaged before re-attestation. Spine-relevant: **B1** re-routed SR-039/041/042
`SN-Refs` to the needs their text states (SR-041→SN-010; SR-039/042 +SN-012) —
SN coverage only widened, trace stays 0 orphans. So the pending re-attestation
now covers a **reviewed, corrected** spine, not the as-first-written one.

## 2026-07-10 — SPINE CHANGE (ClaudeGuardChecks integration, Phases 1–4): SR-043 added; SR-034 Inspection→Analysis; G3 re-run PASS; RE-ATTESTATION still PENDING

Owner-directed batch (review deferred) integrating the reviewed findings from
the ClaudeGuardChecks reference checkout. Spec of record, copied in-repo so a
fresh checkout resolves it: [`docs/archive/INTEGRATION_PLAN.md`](archive/INTEGRATION_PLAN.md)
(no file links point outside this repo). Records live here + in `work-items.csv`
(WI-045…049), **not** in `IMPROVEMENT_PLAN.md`, which this session archives (below).

- **Phase 1 (docs, b443c9d)** — three sharp working-agreement framings distilled
  into `AGENTS.template.md` (the contradiction is the deliverable; scope is a
  promise; every line is a liability), byte-neutral (9976→9978). No spine change.
- **Phase 2 (docs, 379ed76)** — named `TheColliny/FableClaudeMDForOpus` as the
  reference vendorable upstream for the guardrails layer (worked `UPSTREAM` pin).
  The upstream's own content enrichment is **deferred** pending the owner's
  target-repo ruling (it edits a published external repo). No spine change.
- **Phase 3 (e6afac7)** — the **enforcement-audit** discipline (PROCESS_OPTIONS +
  `docs/enforcement-audit.md` dogfood) and **SR-034/TC-034 promoted
  Inspection→Analysis**, mechanized by `tests/test_stdlib_only.py`. Reviewer
  charter gained the claims-verification line. Finding filed: the `Implements:`
  back-link convention is unenforced (Prose gap; not built).
- **Phase 4 (73b5bd0)** — **SR-043**, a Claude `PreToolUse` subagent-spawn gate
  for unattended runs (`scripts/subagent_gate.py`; deny-by-default, launcher-held
  override, fail-open) — the one code adoption, adapted from stop-subagent-fanout
  (MIT). Materialized Claude-only; the agent-neutral floor is untouched.

**Mechanized bar (this session):** `check.py --gate G3` → **RESULT: PASS
(12/12)** (`tests+coverage` 610.9 s, the 80 % coverage floor enforced);
`pytest -q` **470 passed, 2 skipped**; trace **SN=22 SR=43 LLR=40 TC=43,
0 orphans / integrity / schema**. Verification basis: of 43 Verified SRs,
**43 mechanized, 0 attested** (40 Test · 2 Analysis · 1 Inspection) — SR-034
moved Inspection→Analysis and SR-043 is a new Test; the sole remaining
Inspection is SR-036 (deliberate re-sync process).

**G3 re-attestation:** ⏳ **still PENDING the owner** — this batch *widens* the
already-pending re-attestation: a Verified SR's text changed (SR-034) and a new
SR joined the spine (SR-043). Recorded as the `Needs <human>` item in
`docs/status.md`. Deviation recorded: SR-043 was written script-then-test (not
strict failing-first) on an existing G3 repo; TC-043 exercises real code plus a
positive control.

**`IMPROVEMENT_PLAN.md` archived (this session, owner-directed).** The kit's
design-history file moved to `docs/archive/` — its deferred backlog was already
mirrored in `status.md`, so no open work was lost. Go-forward records now split
per the ratified SSOT direction: **next → `status.md`**, **work items →
`work-items.csv`**, **session/gate record → this log**; the `session-protocol`
skill's authority (both tracked copies) was re-pointed to those live homes, and
`status.md`/`CLAUDE.md`/`docs/archive/README.md` updated. Four root-relative
`trace.py#L…` links inside the plan were re-based `../../` for its new depth
(`check_docs --stale` → 0 broken). **Surfaced for review:** this crosses from
"move the file" into enacting part of the working-surface SSOT restructure; the
fuller restructure (relocating the backlog, a `SpecRef` column, mechanizing the
status↔registry SSOT rules) remains a separate, unstarted effort. Residual, not
touched: shipped/meta files still cite `IMPROVEMENT_PLAN.md WI-1.42 / Thread 50`
as design provenance (`trace.py`, `dev-setup.*`, `skills/README.md`, two test
comments) — valid pointers into the archive, left for a later pass.

## 2026-07-10 — README registry map · change-intake flow · fresh-Mac toolchain honesty (WI-050…052; NO spine change)

**Owner-directed session** (no pre-scoped plan): answer the standing questions
about the registries (why `CMP-###` exists; whether `IF-###` acts on
components), give the registry/artifact model one discoverable home, then
verify the double-click onboarding rung on a genuinely fresh Mac — which
surfaced four real defects, each fixed failing-first where testable.

- **WI-050 (b4fbc4d)** — root README: "The registries & trace artifacts — one
  map" (Mermaid spine + off-spine chart; per-tier purpose rows; the CMP
  rationale + derived-interface rule stated with links instead of re-derivation
  from the archive); script table deduped to prose (SN-001/009/010 rehomed —
  the kit README is the one per-script home). PROCESS.md §5: **"Change intake —
  routing a problem to the spine"** — the defect-routing Mermaid flow the owner
  asked for (coverage gap vs requirement gap → IF/CMP/PART scoping → WI →
  gates), previously alive only in archived AXES §4 prose.
- **WI-051 (d9d434e)** — dev-setup honesty on a fresh Mac: `real()` CLT-
  placeholder probe (meta + template), pytest-cov in the install/report set,
  venv-first probing, and the new `dev-setup.template.command` double-click
  rung (bootstrap-scaffolded, exec bit, uname-guarded) — verified live on the
  owner's machine (dialog → CLT install → honest all-[ok] report). SR-032's
  text already covers it: **no re-attestation impact**.
- **WI-052 (6004004)** — pytest-cov 7 removed the `COV_CORE_*` env contract;
  the subprocess-coverage wiring keyed on it and silently unwired every child
  (floor read **29%** vs 80). `coverage.Coverage.current()` detection restores
  **91%**; also heals the ubuntu CI `check` job on fresh installs.

**Byte deltas:** `AGENTS.template.md` 9,978 → 9,978 (untouched);
`PROCESS.md` 56,375 → **57,966** (**+1,591, flagged**: the change-intake
subsection — owner-requested core, not an opt-in layer; baseline re-stamped in
all three `byte-budget-guard` copies, kept byte-identical).

**Mechanized bar (this session):** `check.py --gate G3` → **RESULT: PASS
(12/12)**, coverage **91%** vs the 80 floor; `pytest -q` **476 passed,
1 skipped** (the new coverage-wiring test skips outside a measured run; 477
pass under `--cov`); `check_docs --stale` **0 broken**.

**No SR/LLR/TC text touched** — this batch adds nothing to the pending G3
re-attestation. Residual noted for the restructure effort: the root README's
"Why this produces sustainable code" and Quick-start still paraphrase the kit
README's "core ideas" / "How to use" (stable prose, left deliberately; the
load-bearing per-script duplication is what WI-050 removed).

## 2026-07-10 — SPINE CHANGE (working-surface SSOT campaign S1+S2, WI-053/WI-054): SR-037 text extended; RE-ATTESTATION still PENDING

**Campaign** (spec:
[archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md),
fully ruled): mechanize the status.md↔work-items.csv single-source-of-truth so
the model holds without discipline (S1), then bring the kit's own working
surface into that shape (S2). Two commits on `MultiRepoSupport`.

- **WI-053 (S1) — mechanize the SSOT.** `SpecRef` column on the work-items
  template + the meta CSV (a legacy CSV without it reads empty — never-breaking);
  `deferred` first-class status. `check_trajectory.py` cross-reads
  `work-items.csv` + `docs/status.md` (utf-8/replace): **R-A** (Deliverable
  non-empty iff `done`) is a hard ERROR at every run — the pre-commit floor,
  because a commit is the agent handoff point; **R-B…R-E** (open WIs named in
  status.md, no done id there, every open WI's `SpecRef` resolves) warn plain and
  gate under `--strict` at G2+. `--staged` adds the warn-first no-validation-delta
  check. `pre-commit` gains the trajectory floor (`check.py --run-step
  trajectory`) + the staged step; `check.py` wires `--strict` into the trajectory
  step at G2/G3 (deliberately **excluding `all`** so the hook's `--run-step`
  path, resolved at gate=all, stays warn-first). `bootstrap` scaffolds
  `docs/specs/` (a README + a `WI-000.md` Done-when example). PROCESS_OPTIONS
  gains the SSOT model + the campaign ruling; the kit README + `check_trajectory`
  Contents rows updated. **Spine:** `SR-037` Requirement/Rationale/Acceptance
  extended to cover the status coherence + SpecRef rules, with `LLR-034`/`TC-037`
  kept coherent (TC Evidence still `tests/test_trajectory.py`). *(commit d4a849b)*
- **WI-054 (S2) — meta-repo compliance.** Closed the stale-active **WI-033**
  (the dogfood registry + dashboard it described shipped with WI-030…032 long
  ago — leaving it `active` with a filled Deliverable is exactly the R-A
  incoherence S1 adds; **the fix rode the WI-053 commit** because R-A now fails
  the commit and the registry had to be coherent to land the code). Backfilled a
  resolvable `SpecRef` (this spec's real `#anchor` slugs) on every open campaign
  WI (WI-055…WI-059); moved the status.md "Deferred (backlog)" bullets into
  first-class `deferred` rows **WI-060…WI-064** with archive/log SpecRefs; rewrote
  status.md to the forward-only shape — **no `done` WI id token, no session-local
  codename** (the S4 rule written clean now: e.g. "F3" → "WI-DAG edge data-pass";
  "the grind"/"Phases 1–5" → plain descriptions). Dropped the "Recently landed"
  narrative (log.md holds history). Regenerated `PROJECT_STATE.html` + `docs/okf`.

**Deviations from spec.** (1) WI-033's close rode the WI-053 commit rather than
WI-054's, because R-A makes an incoherent registry un-committable — noted in that
commit body. (2) The no-validation-delta warn is implemented as a real,
git-backed `--staged` mode (warn-only, silent no-op outside a git checkout) wired
as a dedicated pre-commit line; it does not run at gate time (no staging there).
Nothing deferred — the warn fires and is tested. (3) `check_doc_refs` was left
untouched: R-E resolves the SpecRef path part inside `check_trajectory`, and
deeper anchor validation rides the existing (opt-in, unwired-in-meta) path tier —
no minimal addition was needed.

**Byte deltas:** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (57,966) — neither byte-budgeted file was edited. PROCESS_OPTIONS.md
(not budgeted) grew by the SSOT-model subsection.

**Mechanized bar:** `check_trajectory.py --root . --strict` **clean** (64 work
items, 54 done); `pytest -q` **490 passed, 3 skipped**; `check_docs --stale`
**0 broken**; `check.py --gate G3` **PASS (12/12)**.

**RE-ATTESTATION (pending, mandatory).** `SR-037` is a Verification=Test,
Status=Verified requirement whose **text changed** this session; its extension
**rides the already-pending G3 re-attestation** (alongside the SR-034 text change
and the added SR-039…043 / extended SR-038). No new SR was added; the owner
one-liner remains outstanding.

## 2026-07-10 — DOCS (working-surface SSOT campaign S4, WI-055): codename-discipline rule

**Campaign slice** (spec:
[archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md),
S4). Docs only — the writing/review rule that keeps session-local labels off the
durable surfaces. One commit on `MultiRepoSupport`.

- **WI-055 (S4) — codename discipline.** Stated the rule **once** in
  PROCESS_OPTIONS "Trajectory / work-items" (a new *Codename discipline (durable
  references)* paragraph beside the SSOT material S1 added): every durable
  reference in a registry or spec is a `WI-`/`SR-`/`LLR-`/`TC-` id or an in-repo
  path, never a session-local codename — codenames (finding labels, phase
  nicknames, "the grind"-style shorthand) may live in a `log.md` session entry
  but not in `work-items.csv`, the SR/LLR/TC registries, or `docs/specs/` (a
  codename resolves only by spelunking archived docs; an id/path resolves
  mechanically). Added the matching one-line item to the **reviewer-B
  (process/trace) charter** in the reviewer-dial section: a session-local
  codename in a durable cell is a finding. The **mechanical lint stays
  deferred** — a naive `[A-Z]\d+` shape would false-positive on `G3`/`SR-###`,
  so it remains a writing rule + review item until a real pattern earns a narrow
  lint (stated in one sentence where the rule lives). Marked spec S4 ✅ DONE;
  closed WI-055 to `done` (Deliverable filled, `SpecRef` cleared per the S1
  model); dropped WI-055 from status.md and advanced **Next action → WI-056**
  (no `done` id left on the working surface — R-D). Regenerated
  `PROJECT_STATE.html`; `docs/okf` unchanged (the bundle carries the spine +
  process guides, not WI rows).

**No spine change — docs only, no re-attestation impact.** No SN/SR/LLR/TC text
touched; this slice adds nothing to the pending G3 re-attestation.

**Byte deltas:** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (57,966) — neither byte-budgeted file was edited. `PROCESS_OPTIONS.md`
(not budgeted) grew by the codename-discipline paragraph + the reviewer-B line.

**Mechanized bar:** `check_trajectory.py --root . --strict` **clean** (64 work
items, 55 done); `gen_trajectory.py --check` + `gen_okf.py --check` **up to
date**; `check_docs.py --root . --stale` **0 broken**; `pytest -q` **490 passed,
3 skipped**.

## 2026-07-11 — SPINE CHANGE (working-surface campaign S5, WI-056): SN-023 + SR-044 added; architecture-connectivity mechanized; RE-ATTESTATION PENDING

**Campaign slice** (spec:
[archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md),
S5). The architecture view now shows how modules connect, from declared `IF-###`
seams — the seam the AXES ratification sanctioned. One session on
`MultiRepoSupport`; the spine cut rides the pending G3 re-attestation.

- **WI-056 (S5) — architecture-connectivity mechanize.**
  - **`trace.py` reads the IF tier** (closing the SR-002-era gap where it never
    did): `IF-###` id shape/duplication joins the always-on integrity floor;
    each real row's `SR-Refs` must resolve to a real SR (empty or unknown = a
    `--strict` finding, the PB back-link idiom, so every seam links the spine and
    stays transitively TC-covered); and a best-effort `ThisProject`↔`LLR.Module`
    endpoint check is a **warn-only advisory** (the LLR-Module set is a partial,
    differently-named inventory — `scripts/check` vs
    `project-trajectory/scripts/check.py` — so both sides are normalized and the
    authoritative coverage lives in `check_trajectory`). Absent `interfaces.csv`
    / a leftover `IF-000` = vacuous.
  - **`check_trajectory.py` runs the connectivity coverage** at the same
    `trajectory` step (hook + gate), **all warn-first — never an exit-code
    change, even under `--strict`**. Ruled **opt-out, default-on**: the coverage
    warn fires even with an empty/absent `interfaces.csv`, so a multi-module
    arch-map with no seams reads **"connectivity undeclared"** instead of passing
    vacuously; silenced only by the one word `off` in `docs/interfaces-check`
    (the `trajectory-check` idiom — no file scaffolded, absence reads on) or a
    ≤1-module inventory. Per-module warns: a module that is not an IF endpoint;
    a covered module missing the Provides or Consumes direction (the **honesty
    valve** — begin that module's IF-row `Notes` with `source`/`sink` to
    suppress it); an `Active` seam cited by no TC; a `Contracts: IF-###`
    docstring id absent from the registry (and the reverse, once the convention
    is in use). The arch-map is the oracle (`arch_inventory` parses
    `architecture.md`'s generated block for module names + harvested `Contracts`
    lines), the same view `check_doc_refs` uses for its symbol oracle.
  - **`gen_trajectory.py` — the How-SW panel becomes a real graph** when seams
    exist: module / file / external-actor nodes, IF-labeled directed edges,
    **reusing the WI-DAG layouter** (`_dag_ranks` longest-path + barycentre
    sweeps), byte-deterministic, with the symbol table kept beneath it. No IF
    rows → the panel stays today's bare module table (the graph is *earned* by
    declaring seams; the no-seam render is byte-identical to before).
  - **`gen_arch_map.py`** merges module↔module `IF-###` seams into the Mermaid
    dependency diagram as distinctly-styled dotted, labeled edges, and harvests a
    `Contracts: IF-###` module-docstring line exactly like the existing
    `Implements:` harvest (emitted as a `Contracts (interfaces):` map line — the
    oracle above).
  - **Template + docs.** `interfaces.template.csv` gains a `Notes` column
    (legacy rows read it empty — never-breaking) and its explainer row is
    rewritten to the model (ThisProject module → Counterpart module/file/external
    actor; the source/sink valve). `bootstrap.py` interface paragraph updated
    (trace now reads the tier; the opt-out/default-on posture, no file to
    scaffold). PROCESS_OPTIONS gains **"Intra-repo interfaces & the architecture
    graph"** (building on §8: the model, the opt-out, the honesty valve, the
    graph, the ~30-row maintenance-surface risk). ADOPTING §6 gains a re-sync
    recipe. **PROCESS.md §8** widened from "Cross-project interfaces (only when
    projects interlink)" to **"Interface seams — cross-project and intra-repo"**.
  - **Spine (one new SR, ruled).** No existing SN stated the single-dashboard
    intent (SR-038's parents SN-010/SN-021 are about doc-navigability/freshness),
    so minted **SN-023** ("progress **and** how the parts connect from one
    dashboard-like file", Priority S, cited in the root README per the SN
    need-coverage gate). Hung the new **SR-044** (declared-interface
    connectivity: trace integrity + coverage warns + graph render) from
    SN-023;SN-002. Decomposed into **LLR-041** (trace IF integrity) + **LLR-042**
    (connectivity views/warns/graph) and **TC-044** (`Automated=Yes`). SR-005 and
    SR-038 text were **left unchanged** — the ruling chose one new SR over
    extending them, and coherence did not demand it.

- **Judgment calls.** (1) **No `docs/interfaces-check` file scaffolded** — the
  `trajectory-check`/`okf-export` precedent is absence-reads-on, so "bootstrap
  ships it" is satisfied by the reader, not a MAPPING entry (scaffold surface
  unchanged → no `test_bootstrap` / kit-README file-list churn). (2) **Empty
  registry emits one aggregate warn** ("the N-module architecture declares no
  interfaces"), not N per-module warns — the per-module warns start once some
  seams exist. (3) **Source/sink marker = the first word of `Notes`** (not any
  occurrence), so "the source of truth is X" is not a false marker; keyed to
  `ThisProject`. (4) **Two LLRs** (trace-integrity vs views) rather than one, the
  honest two-subsystem decomposition; one TC covers both. (5) The trace endpoint
  join stays a **warn-only advisory** because two module-naming conventions
  coexist and the LLR-Module inventory is partial.

**Byte deltas:** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**57,966 → 58,297 (+331 B, flagged)** — the §8 widening (cross-project → seam
registry, cross-project **and** intra-repo). Baseline re-stamped to 58,297 in the
`byte-budget-guard` skill (source + `.claude` + `.agents` copies).
`PROCESS_OPTIONS.md` / `ADOPTING.md` (not budgeted) grew by the new section +
recipe.

**Re-attestation rider.** New spine rows **SN-023 + SR-044 + LLR-041/042 +
TC-044** join the pending re-attestation batch (`SR-034`/`SR-037`/`SR-038`
/`SR-039…043` from the prior slices). No existing Verified-SR *text* changed in
this slice (SR-044 is new; SR-005/SR-038 untouched), so the re-attestation adds a
new SN→SR chain rather than re-opening one.

**Meta dogfood — the WI-057 driver.** The meta repo now emits exactly **one**
`connectivity undeclared` warn at the hook and G3: *"the 20-module architecture
declares no interfaces"* (20 arch-map modules, zero IF rows). Expected and
non-blocking — WI-057 authors the `IF-###` rows that resolve it (the real
`check.py` hub, hooks/agent_loop feeding it, `stack.ini` + registries as
shared-contract nodes).

**Mechanized bar:** `pytest -q` **506 passed, 3 skipped**;
`check_docs.py --root . --stale` **0 broken**; `check_trajectory --strict`
clean (64 WIs, 56 done); `gen_trajectory --check` + `gen_okf --check` + arch-map
**up to date**; `check.py --gate G3` **12/12 PASS** (first run caught an
unformatted diff → `ruff format` → re-run). Spine **SN=23 SR=44 LLR=42 TC=44,
0 orphans**.

## 2026-07-11 — WI-057 (S6): the kit's own interface registry — the connectivity dogfood

**Session.** Authored `docs/requirements/interfaces.csv` — **43 `IF-###` seams**
describing the kit's real architecture — plus a `Contracts: IF-###` line in the
module docstring of every one of the 20 scripts. This closes the S5 driver: the
meta repo's lone *"connectivity undeclared"* warn. **Data + docstrings only — no
kit-script behavior changed.**

**The 43 rows (species).**
- **20 Provides-CLI rows**, one per arch-map script — the downstream
  compatibility surface, now formal. The 12 gate-step scripts (`trace`,
  `check_docs`, `check_flows`, `check_perf`, `check_privacy`, `check_stubs`,
  `check_dupes`, `check_doc_refs`, `check_trajectory`, `gen_arch_map`,
  `gen_trajectory`, `gen_okf`) `Provides → scripts/check`, so the How-SW graph
  shows the real **`check.py` hub** (12 arrows in); the other 8 provide to the
  downstream adopter / `git` / the `agent CLI` / an output file.
- **19 file-mediated Consumes rows** over the shared-contract hubs
  (`docs/stack.ini`, `docs/architecture.md`, `docs/requirements/work-items.csv`,
  the spine registries, `docs/status.md`, the source tree, the policy files) —
  each row gives its module its consumes-credit.
- **4 subprocess/external seams**: `pre-commit → check` (freshness floor),
  `pre-commit → trace` (`--strict-integrity`), `pre-push → check_privacy`
  (`--range`), `agent_loop → agent CLI` (headless session driver).
- `scripts/gen_cases` carries the **`source` Notes valve** (it consumes only its
  `--spec` argv and produces cases) — the one honest source in the set.

**End state — zero connectivity warns.** Every one of the 20 arch-map modules is
now a declared IF endpoint with **both** a Provides and a Consumes seam (or the
source valve). `check_trajectory --strict` → **clean, 0 warns** (inventory
coverage + docstring-citation + seam-TC all satisfied); `trace --strict` →
**interfaces=43 interface-findings=0, 0 endpoint advisories**. Regenerated
`docs/architecture.md` (20 `Contracts (interfaces):` lines harvested into the
MODULE MAP), root `PROJECT_STATE.html` (the **How-SW panel now renders the
43-edge module/file/external graph**), and `docs/okf` (which now emits an
`IF-###` concept per seam; bundle 155 → **207 files**).

**Judgment calls.**
1. **43 rows, above the ~30-35 guide.** Full 20-module *bidirectional* coverage
   is the honest floor — every module needs a Provides **and** a Consumes credit,
   ~2 rows/module. Every row is a real seam (no boilerplate); the count is
   coverage, not padding.
2. **`ThisProject` is always a script (or a hook in the LLR `Module` set),** so
   the `trace` endpoint advisory (ThisProject-vs-LLR-Module) never fires — 0
   advisories — and every `ThisProject` normalizes into the arch-map inventory.
3. **All seams `Status=Stable`.** These are shipped, pinned contracts (the
   never-break-downstream surface), not in-development seams — `Stable` is the
   accurate label. It also makes the **Active-seam-TC citation rule vacuous** (no
   `Active` row), so it warns on nothing.

**Remaining-warn honesty — a surfaced S5 tension (not silenced).** The
Active-seam-TC rule is *not exercised* by the meta dogfood, and there is a
concrete reason beyond "these are stable": `check_trajectory`'s seam-TC scan
reads the TC **`Verifies`** column for `IF-###` tokens (per
`tests/test_trajectory.py::test_seam_tc_citation_warn`), but `trace.py`'s TC
orphan check flags **any** `Verifies` token that is not an `SN/SR/LLR/TC` id as
*"references unknown"*. So marking a seam `Active` and citing it the documented
way (`Verifies=SR-044;IF-009`) would **pass** `check_trajectory` yet **fail**
`trace --strict` — the two S5 checks are in tension for an Active seam. Surfaced
as a finding, **not fixed inline** (this WI is data + docstrings, "no kit-script
behavior changes"; and the working agreement is to surface a smell, not fix it
in an unrelated change). Because the kit's seams are genuinely `Stable`, the
tension is moot here. **Recommended follow-up** (a new WI or an S5 rider): teach
`trace.py` to treat an `IF-###` token in a TC `Verifies` cell as an off-spine
seam citation resolved against the IF registry, not a spine orphan — then an
adopter can mark a seam `Active` and cite it without tripping the integrity
floor.

**`Implements:` tags — skipped (deliverable #3 was optional).** Seeding
`Implements: SR-/LLR-` on the `CodeSymbol` functions would touch ~40 functions
across all 20 files with per-symbol accuracy risk and no mechanical oracle —
broad for a data-authoring WI. Deferred to a focused pass; the arch-map
`Implements` column stays empty except `subagent_gate`'s existing tags.

**Byte deltas.** `AGENTS.template.md` **untouched (9,978)**; `PROCESS.md`
**untouched (58,297)**. No byte-budgeted file changed.

**Spine note.** No new SN/SR/LLR/TC rows; the interface layer's spine cut landed
in S5 (SN-023 + SR-044 + LLR-041/042 + TC-044). WI-057 is **data + docstrings
only — nothing new rides the pending re-attestation beyond S5's chain.**

**Mechanized bar.** `pytest -q` **506 passed, 3 skipped**;
`check_docs.py --root . --stale` **0 broken**; `check_trajectory --strict` clean
(64 WIs, 57 done, graph acyclic); `gen_arch_map --check` + `gen_trajectory
--check` + `gen_okf --check` **up to date**; `check.py --gate G3` **12/12 PASS**.
Spine **SN=23 SR=44 LLR=42 TC=44, 0 orphans**; **interfaces=43,
interface-findings=0, 0 connectivity warns**.

## 2026-07-11 — SPINE CHANGE (working-surface campaign S7, WI-058): SR-025 extended to the checked per-agent skill fan-out; RE-ATTESTATION PENDING

**Session.** Closed the campaign's cross-agent slice: the per-agent skill copies
are now a **checked, one-command-refreshable fan-out** of the one neutral
`project-trajectory/skills/` source, so `.claude`/`.agents`/`.gemini` can't
silently drift. Fixes the write-once `materialize_agent_layer` defect and the
live three-way `session-protocol` drift. **Independent of the SSOT/arch halves;
rides the same pending re-attestation** (the campaign ruling).

**What shipped.**
- **`.agents/skills/` is a first-class bootstrap target.** New `codex` entry in
  `bootstrap.AGENTS` (`skills_dir=".agents/skills"`, no hook config —
  `hooks_src`/`hooks_dst` are now optional); `--agents codex` materializes the
  matched **kit-scope** skills into `.agents/skills/` byte-identical to source
  (this-repo skills still excluded, same rule as claude/gemini). `both` keeps its
  historical claude+gemini meaning.
- **Refresh, not write-once.** `bootstrap.py --sync` (new
  `sync_agent_skills`) force-overwrites **only** each existing
  `<agent>/skills/<name>/` subtree from source, byte-exact (read/write bytes so
  CRLF can't false-refresh). A focused early-exit mode — it does **not** run the
  full scaffold, so refreshing the meta repo's own copies doesn't re-stamp
  kit-version or re-run generators. Every other scaffolded file stays write-once
  (never clobbers project content); a file outside a skill subtree is never
  touched.
- **Drift gate.** `gen_skills_index.py --check-agents` (new `check_agent_sync`)
  byte-compares every per-agent copy to source. Wired as the **`skills-sync`
  check.py step (G3)** + a **pre-commit floor step (1f)**, the arch-map/OKF
  freshness idiom. **Severity: hard-fail** (a drifted copy fails with a
  one-command fix — reconciling the spec's "warn-first" prose with its binding
  Done-when "an out-of-sync copy fails the check"; the Done-when wins, and
  hard-fail matches the established freshness gates). **Vacuous** when there is no
  neutral source or no per-agent dir.
- **Docs.** PROCESS_OPTIONS "Skills layer" + `skills/README.md` gained the
  checked-fan-out subsection and the **tenability constraint** (verbatim fan-out
  holds only while frontmatter stays agent-neutral; the day a skill needs an
  agent-specific field, materialization gains a per-agent transform and tracking
  flips to gitignore + regenerate-on-setup — the recorded revisit trigger).
  ADOPTING §6 gained the `re-sync check.py+hook together` caveat (mirrors `okf`).

**Judgment calls.**
1. **Drift-check home = extend `gen_skills_index.py` (kept KIT-only), not a new
   script.** It already owns the skills layer + a `--check`. It needs the neutral
   `skills/` source, which only the kit repo hosts — a scaffold has no source to
   drift from — so it is **not** scaffolded downstream. To keep the shipped hook's
   `--run-step skills-sync` honest without a `check: no step named` break, the
   check.py step's command is **real when `gen_skills_index.py` sits beside
   check.py (this kit), else a vacuous `python -c pass` no-op** (downstream). This
   is more conservative than scaffolding a permanently-dead generator + gate step
   into every downstream repo, and honest: downstream there is genuinely nothing
   to check. Never-breaking; no scaffold-surface change.
2. **Missing-skill decision: a source skill absent from a per-agent dir does NOT
   warn.** Subset materialization is legitimate (a scope-matched downstream
   carries only some skills), so the check compares only skills that a per-agent
   dir already holds. An **orphan** (a copy whose skill no longer exists in
   source) is surfaced as a non-failing WARN, not a hard fail — `--sync` can't fix
   it (the fix is a manual removal).
3. **Meta drift resolved by advancing the SOURCE, not reverting `.claude`.** The
   three-way `session-protocol` drift was: source lagged on the check_docs command
   (`--root .`), while `.claude` had already hand-gained the correct `--stale`
   (the meta repo's actual standing gate) and `.agents` sat on the pre-archive
   body. Fix: advance `project-trajectory/skills/session-protocol/SKILL.md` to
   `--stale` (the true gate) — which made `.claude` **already byte-identical** (its
   only diff) — then `--sync` refreshed `.agents/session-protocol`. All 10
   per-agent copies now byte-identical to source; committed (the tracked+drift
   ruling).

**Deviations.** (a) The drift check hard-fails where the S7 prose said
"warn-first" — reconciled per the binding Done-when (call #above). (b) Advanced
the source skill body (`--stale`) rather than reverting `.claude` — a one-word
SSOT correction to the true gate, documented above. No other deviations.

**Byte deltas.** `AGENTS.template.md` **untouched (9,978)**; `PROCESS.md`
**untouched (58,297)**. No byte-budgeted file changed (the S7 docs landed in
PROCESS_OPTIONS / skills-README / ADOPTING).

**Spine.** **SR-025 text extended** (Verified) to cover the checked per-agent
fan-out (same "generated, not hand-maintained" property; SN-Refs unchanged);
**+LLR-043** (`gen_skills_index.check_agent_sync` drift check) **+TC-045**
(`tests/test_skills_sync.py`). This is a **Verified-SR text change + 2 new
spine rows → rides the pending G3 re-attestation** (with SR-037/SR-038/
SR-039…044/SN-023, one owner sitting — the campaign ruling).

**Mechanized bar.** `pytest -q` **519 passed, 3 skipped** (+13: 12 skills-sync +
1 hook-step); `check_docs.py --root . --stale` **0 broken**; `trace --strict
--require-verified --strict-schema` **SN=23 SR=44 LLR=43 TC=45 orphans=0
integrity=0 schema=0 interfaces=43 interface-findings=0**; `check_trajectory
--strict` clean (64 WIs, 58 done); `gen_arch_map`/`gen_trajectory`/`gen_okf`
`--check` **up to date**; `check.py --gate G3` **13/13 PASS** (the new
`skills-sync` step). Spine **SN=23 SR=44 LLR=43 TC=45, 0 orphans**.

## 2026-07-11 — WI-059 (S8): heterogeneous implementer/reviewer scheduling — the campaign's last slice

**Summary.** Landed S8, the final slice of the working-surface +
architecture-connectivity campaign
([archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md#s8--heterogeneous-implementerreviewer-scheduling--done-2026-07-11)):
the unattended coordinator now schedules separate implementer and reviewer
sessions across tiers **and providers**, with next-round routing a **declared,
legible** policy informed by a mechanical (advisory) review-substance scorer.
Everything stays stdlib, consent-explicit (no silent model swap), and
**never-breaking** — the whole layer is gated on the presence of the
`docs/agents-enabled` enable-list, so an absent enable-list reproduces today's
single `AGENT_CMD`/`AGENT_MODEL` behavior byte-for-byte (the 38 legacy
`agent_loop` tests are unchanged and green).

**Deliverables (per the S8 Done-when — all ticked).**
1. **Loop-side reviewer dispatch + `--prompt-map` (test-first).** In managed mode
   a committing non-review session schedules `REVIEW-A` (and `REVIEW-B` under
   `docs/review-policy: 2`) before the next build — `review-policy 0|1|2` is now
   **loop-enforced**, not just surfaced. Reviewer verdicts are **repo files**
   (`docs/reviews/NNN-<phase>.md`, log.md block + one machine line
   `VERDICT: APPROVE|CHANGES-REQUESTED findings=N`), merged **mechanically, no
   debate**. `--prompt-map`/`AGENT_PROMPT_MAP` = per-phase prompt-template FILES
   (parse_model_map reuse; each preflighted). The reviewer prompt is **redacted
   by construction** — diff + requirements, never the implementer's
   self-assessment (a test asserts the driver resume prompt never reaches a
   reviewer).
2. **`docs/agents.csv` registry + enable-list routing** (`scripts/agent_route.py`,
   new). One row per usable model, `[PROVIDER]-[MODEL_NAME]-[VERSION]` id (a join
   key, **never parsed**; `Provider`/`Model`/`Version`/`Tier`/`CmdTemplate` are
   the columns). Selection = enable-list preference order + phase tier + reviewer
   heterogeneity (two providers, ≥1 differing — *preferred*; **degraded
   same-provider legal**) + per-model **cooldown** (the rate-limit backoff
   generalized) + **tier-up-never-down**; every selection logged before launch.
   No vendored catalog (pointer to models.dev / LiteLLM).
3. **The substance scorer** (`scripts/score_reviews.py`, new): anchored precision,
   actionability, cross-reviewer corroboration (cross-family weighted up),
   optional confirmed-finding rate; **length never scores positively**. Severity
   hygiene + four **tripwires** (finding-count/cap gaming, near-duplicate review
   text, an implementer diff touching a review/policy path, mass finding-rejection)
   are **non-scored gates**. Scoreboard = one decayed-tally text file
   (`docs/reviews/scoreboard.txt`); **advisory** — the declared policy picks.
   **Fixed escalation** (win-stay/lose-shift): margin ≥ 2, implementer-provider
   swap after 2 failed gates, tier rise only after the swap fails, **page-human**
   on the shared-failure regime / contradictory verdicts / any tripwire, with
   **`docs/gate-policy`-keyed failure semantics** (attended stops NEEDS-HUMAN;
   single-ratify surfaces + continues; autonomous schedules a strong-tier
   different-provider design-check).
4. **Docs.** PROCESS_OPTIONS "Unattended operation" gained the
   routing/escalation subsection; the "reviewer tier never delegated down"
   wording **narrowed to gate-closure** reviews (iteration reviewers are
   cheap-but-heterogeneous); the root README unattended bullet gained the
   one-sentence iteration-review summary pointing at the detail.
5. **Spine.** New **SR-045** under `SN-006`/`SN-016` + **LLR-044/045/046**
   (router / loop dispatch / scorer) + **TC-046** + **IF-044…047** (the two new
   scripts' Provides-CLI + Consumes seams; `Contracts:` docstrings harvested into
   the arch map). Rides the pending G3 re-attestation.

**Judgment calls.**
- **Verdict-file home = `docs/reviews/`** (`NNN-<phase>.md` per round, alongside
  the advisory `scoreboard.txt`) — a repo-text-as-memory surface, the loop reads
  it back at the round boundary.
- **Scoreboard format** = a small line-oriented text file: `provider <P>
  substance=<f> rounds=<n>` (decayed, DECAY=0.7) + `round <n> verdict=… tier=…
  margin=… primary=… tripwire=… contradiction=…` (the history the escalation
  policy reads). Documented in `score_reviews.py` + PROCESS_OPTIONS.
- **Prompt-template shape** = an **embedded default** `REVIEWER_PROMPT` constant
  in `agent_loop.py` (no new scaffold file), overridable per phase with a
  `--prompt-map` FILE; `{verdict}` is slotted with the verdict path.
- **Constants + knobs** = per-repo-overridable env defaults `AGENT_ROUTE_MARGIN`
  (2), `AGENT_ROUTE_SWAP_AFTER` (2), `AGENT_ROUTE_PAGE_TOP_TIER_FAILS` (2),
  `AGENT_COOLDOWN_SECONDS` (900), `AGENT_TIER_MAP` (phase→tier; iteration
  reviewers default to a cheaper tier) — calibration values, not spine facts.
- **`docs/agents.csv` is scaffolded** (via `agents.template.csv`, example rows
  for the verified `claude -p` / `codex exec` / `gemini -p` shapes) — present but
  **inert**; **`docs/agents-enabled` is NOT scaffolded** (the consent surface +
  on-switch; absence = routing off = today's behavior).

**Deviations.** None from the S8 rulings. Confirmed-finding rate is scored only
when a follow-up diff is supplied (the loop passes none inline, so it is left
out of substance rather than faked to 0) — per the spec. The spec's
"cheap in-kit A/B" is FUTURE work, not built (scoreboard stays advisory).

**Byte deltas.** `AGENTS.template.md` **untouched (9,978)**; `PROCESS.md`
**untouched (58,297)** — the §5 change-intake flow is **linked, not edited**.

**Mechanized bar.** `pytest -q` **561 passed, 3 skipped** (+3 over the 558
pre-WI-059 total: the S8 route/scorer/loop suites are
`tests/test_agent_route.py` + `tests/test_score_reviews.py` +
`tests/test_agent_loop_review.py`); `check_docs.py --root . --stale` **0
broken**; `trace.py --strict --require-verified --strict-schema` **SN=23 SR=45
LLR=46 TC=46 orphans=0 integrity=0 status-findings=0 placeholders=0
schema-findings=0 interfaces=47 interface-findings=0**; `check_trajectory
--strict` clean; `gen_arch_map`/`gen_trajectory`/`gen_okf` `--check` **up to
date**; `check.py --gate G3` **13/13 PASS**. Spine now **SN=23 SR=45 LLR=46
TC=46, 0 orphans**.

**Re-attestation rider.** The new **SR-045** (Verification=Test, Verified) joins
the pending G3 re-attestation — one owner sitting now covers SR-034/SR-037/
SR-038/SR-039…044/SR-025 **and SR-045** + the new `SN`-hung SR. The campaign is
complete; the coordinating session handles the spec archival + final status.

## 2026-07-11 — Campaign close (coordinating session): spec archived; WI-065 filed; NO spine change

**Session.** The working-surface + architecture-connectivity campaign is
closed. The campaign spec moved
`docs/specs/` → [archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](archive/specs/working-surface-and-architecture-restructure.2026-07-11.md)
per the S0 #2 ruling — close date appended, an ARCHIVED banner naming the
attributed WIs (WI-053…WI-059) — with every in-repo citation re-pointed (this
log ×4, `status.md`, `AGENT_ROUTING_RESEARCH.md`, the SR-045 Rationale cell)
and `docs/archive/README.md` gaining a `specs/` inventory row.

**WI-065 filed (deferred).** The WI-057 session surfaced a real tension it
correctly did not fix inline: `check_trajectory`'s seam-TC-citation scan reads
the TC `Verifies` column for `IF-###` tokens, but `trace.py`'s orphan check
flags unknown `Verifies` tokens — so an `Active` seam cited the documented way
fails `trace --strict`. Now a first-class `deferred` row with a live per-WI
spec ([specs/WI-065.md](specs/WI-065.md), Done-when checklist included —
dogfooding the S0 #5 convention), parked until a seam actually needs `Active`
status (all 47 current seams are `Stable`).

**status.md** counts refreshed (13-step G3; SN=23 SR=45 LLR=46 TC=46; 47
seams); the campaign block now points at the archived spec; next action = the
owner sitting (re-attestation over the campaign's accumulated spine changes,
push ruling, sibling-repo target, batch review).

**No SR/LLR/TC text touched** — registry data (one deferred row) + docs moves
only; nothing new rides the re-attestation beyond what the campaign entries
recorded.

## 2026-07-11 — WI-066: OKF self-identification banner + doc-graph exclusion

**Session.** A one-WI session resolving the **2026-07-11 OKF audit** (owner
ruling recorded in
[archive/specs/WI-066.2026-07-11.md](archive/specs/WI-066.2026-07-11.md)):
~210 of the 218 generated `docs/okf/` files carried no in-body signal that they
are generated reference copies — only the subtle `resource:` frontmatter line —
and `check_docs.py` counted the whole bundle in its doc graph, so 218 of its 219
orphan warnings were okf files, drowning the one real orphan.

**Deliverables.**
1. **`gen_okf.py` banner.** A new `banner(source)` helper emits one
   source-slotted blockquote — `> **GENERATED — a reference copy, not the source
   of truth.** Derived from <source> by scripts/gen_okf.py; edit the
   registry/doc, then rerun it (docs/okf-export: off silences the layer).` —
   immediately after the frontmatter of every concept file, tier index, root
   index and process guide, and first in the frontmatter-less `UPSTREAM.md`.
   Concept files slot their exact `resource:` string, tier indexes their
   registry, process guides their summarized source doc; the root index and
   `UPSTREAM.md` **absorbed** their pre-existing routing sentences so the message
   is stated once per file. No clock — `--check` stays byte-stable.
2. **`check_docs.py` exclusion.** `collect_docs` drops `docs/okf/` from doc
   discovery (doc count, link graph, orphan detection) via the
   gen_arch_map/gen_trajectory/check_doc_refs "never lint generated output"
   idiom, using an `OKF_DIR = "docs/okf"` constant matching gen_okf's `OUT_DIR`.
   Links **into** the bundle still resolve (the files stay on disk as targets).
3. **Regenerated** the 218-file meta bundle, `docs/architecture.md` (the new
   `banner()` public function added one MODULE MAP row), and root
   `PROJECT_STATE.html`.

**Owner-ruling provenance.** The 2026-07-11 OKF audit + ruling — (a) banner,
(b) exclusion, and *nothing else* (no default flip, no `.ignore`, no `rg`
change) — is archived in the per-WI spec above.

**Orphan delta.** `check_docs --root . --stale` orphan warnings **219 → 1** (the
pre-existing `docs/test/report.md`, deliberately out of scope); doc count
243 → 25 (the bundle no longer counted).

**Spine.** **No SR/LLR/TC text changed.** The banner is presentation within
SR-042's "one typed markdown concept per real row" (files stay frontmatter-typed,
graph links resolve, regeneration byte-identical); the exclusion is scan-scope
within SR-012's broken-link / vision claim (links into the bundle still resolve).
Verified neither AcceptanceCriteria contradicts. Nothing new rides the pending
G3 re-attestation.

**Byte deltas.** No budgeted file touched — `AGENTS.template.md` and `PROCESS.md`
are **untouched**; the change is scripts + generated output + the meta
registry/spec/log.

**Mechanized bar.** `pytest -q` **564 passed, 3 skipped** (+3 over the 561
pre-WI-066 total: the banner test in `tests/test_gen_okf.py` +
`test_okf_bundle_dropped_from_doc_scan` / `test_okf_bundle_adds_zero_scanned_docs`
in `tests/test_check_docs.py`); `check_docs.py --root . --stale` **0 broken**
(1 orphan warn); `gen_okf` / `gen_arch_map` / `gen_trajectory` `--check` **up to
date**; `check.py --gate G3` **13/13 PASS**. Spine unchanged at **SN=23 SR=45
LLR=46 TC=46, 0 orphans**.

## 2026-07-11 — WI-067 (capability-expansion C1): the run capability menu — SPINE CHANGE (SR-046 added); RE-ATTESTATION PENDING

**What shipped.** The root `run.*` launchers stop hard-wiring one duplicated
`RUN_CMD` and become **thin delegates** to a new stdlib
**`scripts/run_menu.py`**, which reads a **`[run]` section** in `docs/stack.ini`
(one `<name> = <command>` line per capability + optional `<name>.desc`) and
presents the major capabilities an evaluator runs — no args = a numbered
interactive menu, `run_menu.py <name>` = direct launch with exit-code
passthrough, `--list` = a stable `name<TAB>desc` machine listing (the agent
surface). An absent/empty `[run]` section prints the same "no launch command
wired yet" guidance and exits 1. The launch command now lives in exactly one
place (spec:
[archive/specs/capability-expansion.2026-07-11.md](archive/specs/capability-expansion.2026-07-11.md), C1).

**Deliverables.**
- `scripts/run_menu.py` (new, stdlib): a configparser `[run]` reader
  (`interpolation=None`, case-preserving `optionxform`, declaration order kept;
  a `.desc` attaches to its command, an orphan/empty command dropped); menu /
  direct / `--list`; the `_utf8_console` guard like the sibling scripts.
- `stack.ini.template` gains a commented `[run]` example block (serve/iso); the
  meta repo's own `docs/stack.ini` gets **no** `[run]` section — the "no `run.*`
  product launchers" self-application non-goal stands.
- `run.template.{sh,cmd,command}` rewritten as delegates to
  `python scripts/run_menu.py "$@"` (reusing the agent-resume launchers'
  python-probe idiom); `.command` still hops to `run.sh`. The `RUN_CMD`
  duplication is retired; the "pure library → delete them" guidance kept.
- Spine: **SR-046** (Run capability menu) under **SN-001** + **LLR-047**
  (`run_menu.py`) + **TC-047** (Automated=Yes, Evidence `tests/test_run_menu.py`).
- Off-spine: the meta's own connectivity dogfood — **IF-048** (Provides →
  `run.* launchers`) + **IF-049** (Consumes ← `docs/stack.ini`) declare
  run_menu's seams + a `Contracts:` docstring line, so the new module stays a
  first-class arch-map endpoint (zero connectivity warns, like every sibling
  script).
- Docs: PROCESS.md §7 rung prose (the launcher now presents declared
  capabilities), PROCESS_OPTIONS.md §7 boundary-notes bullet (the menu
  mechanics, single-sourced there), the kit README per-script table
  (`run_menu.py` row + the `run.template` row), ADOPTING §6 migration note
  (existing `RUN_CMD` launchers keep working — re-sync never clobbers; new
  scaffolds get delegates), bootstrap `MAPPING` + docstring, root README
  launcher line.
- Tests: `tests/test_run_menu.py` (11 cases: `--list` stable format, direct
  launch + arg passthrough, exit-code passthrough, menu from piped stdin, no
  hang on closed stdin, quit, absent/empty `[run]` guidance, `--list` empty,
  shell-quoting sanity); `test_bootstrap.py` updated (scaffold ships
  `scripts/run_menu.py`; launchers delegate with no `RUN_CMD`).

**Judgment calls.**
- **`shell=True`** in `run_menu.launch`: the value is the user's own declared
  shell line from their own `docs/stack.ini` (the same trust boundary as the
  `RUN_CMD` it replaced — the user edits their own file), and a capability is
  deliberately a full shell command (pipes, `&&`, redirects) so a project script
  owns multi-step launches. Reasoning recorded in the module docstring + at the
  call site.
- **`--list` format = `name<TAB>desc`**, one capability per line, declaration
  order, desc empty (trailing tab) when none. An empty `[run]` under `--list`
  prints nothing + exit 0 (a machine surface reads zero lines, not guidance
  prose on stdout); the launch/menu paths keep guidance + exit 1.
- **SR-046 hung from SN-001** (not a new SN): the launcher surface is part of
  what the kit scaffolds to make an adopted product runnable — the evaluator's-
  rungs / onboarding family SR-032 sits in. One new SR, per the C1 ruling.

**Byte deltas.** `AGENTS.template.md` **9978 → 9978** (untouched). `PROCESS.md`
**58,297 → 58,380 (+83 B)**, flagged: the §7 evaluator's-rungs sentence now
names the `docs/stack.ini [run]` capability set — the minimal factual add for the
new surface; the menu mechanics live in PROCESS_OPTIONS §7, not the budgeted
core. Baseline re-stamped to **58,380 (WI-067)** in the `byte-budget-guard` skill
(all 3 tracked copies, byte-identical).

**Mechanized bar.** `pytest -q` **575 passed, 3 skipped** (+11 over WI-066's 564:
the 11 `tests/test_run_menu.py` cases); `check_docs.py --root . --stale` **0
broken** (1 orphan warn); `gen_arch_map` / `gen_okf` / `gen_trajectory` `--check`
**up to date**; `check.py --gate G3` **13/13 PASS**. Spine now **SN=23 SR=46
LLR=47 TC=47, 0 orphans**; 49 declared interface seams.

**Re-attestation rider.** New **SR-046** (Verification=Test, Verified) joins the
mechanized spine under SN-001 → it rides the **one pending G3 re-attestation**
with the rest of the accumulated changes (status.md Needs-\<human> #1).
*Mandatory*: a new test-verifiable SR joined the spine.

## 2026-07-11 — WI-068 (capability-expansion C2): the `Critique` verification value + the subjective-quality critique loop — SPINE CHANGE (SN-024 + SR-047 added); RE-ATTESTATION PENDING

**What shipped.** Subjective/perceptual acceptance — "a realistic-looking
render", an artifact comparison with no crisp measurable interface — becomes a
first-class, mechanizable thing: **`Critique`** joins the Verification vocabulary
(owner ruling #4 — LLM-provisioned feedback that runs autonomously, deliberately
separated from human `Attest`), and the S8 coordinator gains a **CRITIQUE
run-phase** that gives another agent a *different hat* to judge a code-produced
artifact against a **written rubric**, driving bounded rework. Spec:
[archive/specs/capability-expansion.2026-07-11.md](archive/specs/capability-expansion.2026-07-11.md) C2 (now ✅ DONE).

**Deliverables.**
- **`Critique` in the Verification vocabulary** — `trace.py` `ENUM_FIELDS`
  (accepts `Critique`, still rejects unknowns) + the `registry-hygiene` skill
  (all 3 tracked copies) + PROCESS.md §4. **LLR-exemption decision:** a `Critique`
  SR is **NOT** LLR-exempt (unlike `Analysis`/`Inspection`/`Attest`) — its artifact
  is *produced by code* (a render/generation pipeline) and only its acceptance is
  perceptual, so it keeps its LLR like `Demonstration`/`Manual`; a genuinely
  code-less subjective requirement is an `Attest`, not a `Critique`. Stated once in
  PROCESS.md §4 and the trace.py orphan-rule docstring; mechanized by
  `test_trace.py::test_critique_verification_value`.
- **The rubric convention — `docs/rubrics/`** (scaffolded via bootstrap): a README
  (a rubric is derived from the SN/SR intent, **not** the possibly-lax TC; that
  inversion is what catches a lax TC) + an inert `rubric-000.md` showing the shape
  — an intent statement + **numbered good (`G#`) / bad (`B#`) anchors** (definite,
  citable, TC-style) — plus the **accumulation rule** (a critique finding naming a
  new failure mode is added as a new `B#` at rework, so later rounds judge against
  the accumulated reference; verdicts cite anchor ids). `MAPPING` + `test_bootstrap`
  lists + kit README + bootstrap docstring updated.
- **The CRITIQUE run-phase in `agent_loop` managed mode.** A committing build
  whose **commit-subject WI ids** (`build_scope_srs`, joined through
  `work-items.csv`) deliver a `Critique` SR (read off `system-requirements.csv`)
  schedules a **fresh, provider-heterogeneous CRITIQUE session before the next
  build** — strong tier by default, `agent_route.select` preferring a different
  provider from the implementer. The prompt is an embedded `CRITIQUE_PROMPT`
  (overridable via the existing `--prompt-map` under the `CRITIQUE` key) slotting a
  **redacted `critique_brief`**: the rubric text + the SN/SR intent + the TC
  `Parameters` artifact recipe, and **never** the implementer's self-assessment.
  Verdict = `docs/reviews/NNN-CRITIQUE.md` (the S8 `VERDICT: …` machine line +
  anchor-citing findings + optional `[TC-HARDEN]` proposals). Iteration:
  CHANGES-REQUESTED → rework BUILD → re-CRITIQUE, bounded by **`AGENT_CRITIQUE_MAX`**
  (default 3, env-overridable) → then `agent_route.failure_action(gate-policy)` pages
  the human (attended → NEEDS-HUMAN). **Absent the enable-list or any `Critique` SR,
  byte-for-byte today's behavior.**
- **The lax-TC ratchet** (`check_trajectory --staged`, warn-first): a WI closing on
  a `Critique` SR while the latest `docs/reviews/*-CRITIQUE.md` verdict is
  CHANGES-REQUESTED, without the staged change touching the TC registry, the tests
  dir, **or** a `docs/rubrics/` file → warn (harden the TC or add an anchor — the fix
  must land in the chain, not just the artifact).
- Spine: **SN-024** (subjective acceptance adjudicated by an independent critical
  eye against a written rubric, never the authoring session) + **SR-047**
  (Verification=Test, Verified) under SN-024/SN-006 + **LLR-048** + **TC-048**
  (Automated=Yes, Evidence = real pytest nodes).
- Docs: PROCESS_OPTIONS "Critique verification & the critique loop" subsection (the
  model stated once — rubric anchors, redaction, budget, the arbiter split: the
  critic gates iteration / the human owns acceptance via `Attest` at gate closure /
  autonomous per gate-policy; the multimodal caveat — image-capable CLIs read
  artifact paths natively, capability noted per-model in the registry `Notes`,
  degraded = text-proxy critique). PROCESS.md §4: the minimal vocabulary addition
  only. Root README: an SN-024 need bullet.

**Judgment calls.**
- **LLR-exemption:** decided NOT-exempt (reasoning above) — the sound default the
  spec itself flagged; a Critique SR without implementing code should be an
  `Attest`.
- **Trigger mechanics:** the honest "which WI did this build touch" signal is the
  **`WI-<n>:` commit-subject convention** (which the loop already relies on) joined
  through `work-items.csv` `SR-Refs`. **Recorded gap:** absent WI-tagged commits or
  a `work-items.csv`, the critique layer is vacuous (a downstream repo not using the
  trajectory layer gets no critique) — the closest honest version; a per-WI marker
  in the verdict file was not added.
- **Ratchet shape:** the verdict file is not WI-tagged, so the ratchet reads the
  **latest** `*-CRITIQUE.md` overall as the honest proxy for "the in-scope critique"
  (the loop critiques one scope at a time, so the newest verdict is the live one).
  Recorded as a gap in the code comment.
- **Critique tier = strong by default** (perceptual judgment + multimodal support
  are exactly where model capability matters; tier-up-never-down).
- **Budget counting:** a *new* scope resets `AGENT_CRITIQUE_MAX`; a rework of the
  *same* scope preserves the count so the budget actually bounds the loop (a
  re-scheduled critique after a rework build does not reset it).

**Byte deltas.** `AGENTS.template.md` **9978 → 9978** (untouched). `PROCESS.md`
**58,380 → 58,853 (+473 B)**, flagged: the §4 vocabulary gains the `Critique`
definition + the non-LLR-exempt clause (the minimal factual add; the full model
lives in PROCESS_OPTIONS, not the budgeted core). Baseline re-stamped to **58,853
(WI-068)** in the `byte-budget-guard` skill (all 3 tracked copies, byte-identical).

**Mechanized bar.** `pytest -q` **584 passed, 3 skipped** (+9 over WI-067's 575:
6 `test_agent_loop_critique.py` + 1 `test_trace.py` critique vocab/exemption + 2
`test_trajectory.py` ratchet); `check_docs.py --root . --stale` **0 broken** (1
orphan warn = the pre-existing `docs/test/report.md`); `gen_arch_map` / `gen_okf` /
`gen_trajectory` `--check` **up to date**; `check.py --gate G3` **13/13 PASS**.
Spine now **SN=24 SR=47 LLR=48 TC=48, 0 orphans**; 49 declared interface seams.

**Re-attestation rider.** New **SN-024** (a new stakeholder need) + **SR-047**
(Verification=Test, Verified) join the mechanized spine → they ride the **one
pending G3 re-attestation** with the rest of the accumulated changes (status.md
Needs-\<human> #1). *Mandatory*: a new SN and a new test-verifiable SR joined the
spine.

## 2026-07-11 — WI-069 (capability-expansion C3): the pair-row agent registry — SPINE CHANGE (SR-045 text extended); RE-ATTESTATION PENDING

**What shipped.** The **pair-row registry** ("pairs now, factor later"), the C3
slice. `docs/agents.csv` becomes `Id,Family,Model,Version,Tier,CmdTemplate,Env,
Notes` — **one row = one (model × route) pair**, the table itself the allow
matrix. The semantic cleanup is **identity vs access**: `Family`/`Model`/
`Version` = identity (Family = who trained it, the heterogeneity + scorer
corroboration key; Model = the line identity incl. `-pro`/`-flash`; Version = the
*comparable* token only), `CmdTemplate`/`Env` = access. `Provider` is **retired**
— a legacy `Provider` column with no `Family` reads Provider as Family
(never-breaking). Absent the new columns/tokens, every existing behavior is
byte-identical.

**Deliverables.**
- **`agent_route.py`:** `Family` column (legacy `Provider` fallback) + `Env`
  parsed by new `parse_env` (`KEY=value;KEY2=value2`, lenient). New
  `resolve_token`/`resolve_enabled`: a version-less enable-list token resolves to
  the newest pair in its `Family-Model` line — **exact-id first**, else the
  column-keyed `Family-Model` match (intra-line only, the `-PRO` correction),
  newest by **dotted-numeric tuple → maturity rank → date stamp**, `preview`/
  `exp` skipped unless named/only, **equal-key route pairs by registry row
  order**. `load_tag_rank`/`parse_tag_rank` hold the `ga>preview>beta>exp`
  vocabulary (per-registry override: a `# tag-rank:` comment line in `agents.csv`
  or the `AGENT_TAG_RANK` env knob). `select()`'s prefer-different/exclude keyed
  on **Family** (`exclude_families`).
- **`agent_loop.py`:** `run_session` gains an `env` param; a selected pair row's
  `Env` is merged `{**os.environ, **row_env}` and passed **only when the row
  declares Env** (else `session_env` stays `None` = today's exact call). All
  phases (BUILD/REVIEW-A/REVIEW-B/CRITIQUE) inherit it through the shared launch
  path. The enable-list is resolved up front (`managed = bool(raw_enabled)` so an
  unresolvable token fails preflight, never silently drops to legacy); the
  implementer/reviewer exclude sets and the scoreboard key re-keyed to Family.
- **`score_reviews.py`:** corroboration documented + re-keyed on **Family**
  (legacy Provider = the fallback); the CLI gains `--family` (preferred over the
  retained legacy `--provider`).
- **`agents.template.csv`:** new header + compliant rows (Gemini `Model=gemini-3-
  pro`, `Version=3`; a `# tag-rank:` directive; commented `-ACCT2` second-account
  + router pair examples with their `Env`); the registry explainer rewritten.
- **Docs:** PROCESS_OPTIONS routing subsection rewritten once (pair-row
  semantics, identity-vs-access, version-less resolution, account/router rows,
  the recorded revisit trigger, and the two research safety notes — pin LiteLLM
  off the malicious PyPI builds `1.82.7`/`1.82.8`; Gemini OAuth multi-account
  refresh race → API keys or serialize). `project-trajectory/README.md`
  kit-contents entry updated; the `IF-044`/`IF-045` seam descriptions refreshed
  to the pair-row scheme (accuracy, not a status change). **No PROCESS.md
  change.**
- **Spine:** `SR-045` Requirement + AcceptanceCriteria extended (pair-row
  identity/access, Family-keyed heterogeneity, version-less newest resolution,
  per-pair `Env`); `LLR-044`/`LLR-045` text extended. No new SN/SR.
- **Tests:** `test_agent_route.py` +11 (Family fallback / Env parse, resolver
  ordering incl. numeric-beats-date + preview-skip + tag-rank override +
  multi-route registry order, exact-id precedence, unresolvable token, `-ACCT2`
  independent cooldown, router-not-diverse-from-native, CLI version-less
  resolution); `test_agent_loop_env.py` +2 (Env merge into the launch; empty Env
  = ambient, no injected var). The existing legacy `Provider`-header registry
  tests prove byte-identical selection.

**Judgment calls.**
- **Column contract (ruling 8).** Model carries the full line identity
  (`gemini-3-pro`, `gpt-5.2`, `opus`); Version is the extracted comparable token
  (`3`, `5.2`, `4.8`). Where the line name already embeds the number
  (`gemini-3-pro`), version-less resolution within `(Family, Model)` degenerates
  to maturity/date tiebreaking — correct per the `-PRO` correction (a newer
  generation is a *new line*, a new enable-list entry, never a silent version
  bump). The clean iterating case is `opus` (Model has no number, Version
  iterates 4.8→4.9→…).
- **Tag-rank override home.** A `# tag-rank: ga>preview>beta>exp` comment line in
  `agents.csv` (parsed by `load_tag_rank`), overridable by `AGENT_TAG_RANK`; the
  default equals the built-in `DEFAULT_TAG_RANK`. The **skip set** stays fixed at
  `{preview, exp}`; the override tunes the *tiebreak* rank only. Documented in
  the template + PROCESS_OPTIONS.
- **Registry-row-order tiebreak (vs the spec block's "enable-list order").** A
  version-less token is *one* enable-list entry, so enable-list order can't
  order the several *registry* rows it matches — **registry row order decides**
  (implemented, documented). `select()`'s enable-list-order preference is a
  separate, unchanged layer (ordering the resolved pool).
- **Env merge semantics.** `subprocess.run(..., env={**os.environ, **row_env})`
  **only when the row declares Env** (row wins on a key collision); an empty Env
  passes `env=None` — byte-identical to today's call (verified by
  `test_empty_env_inherits_the_ambient_environment`). The interactive leg is
  unchanged (it never routes through the registry, so it carries no pair `Env`).
- **score_reviews scope.** The module already spoke "cross-family"; the honest
  re-key lives at the loop call site (it now passes `route_family`). Kept the
  function param name `providers` (API/scoreboard-format stability) and added the
  self-describing `--family` CLI alias rather than churn the on-disk format.

**Byte deltas.** `AGENTS.template.md` **9978 → 9978** and `PROCESS.md` **58,853 →
58,853** — **both untouched** (verified: `git diff --stat` empty). The routing
expansion landed in `PROCESS_OPTIONS.md`, not the budgeted core.

**Mechanized bar.** `pytest -q` **597 passed, 3 skipped** (+13 over WI-068's 584:
11 `test_agent_route.py` + 2 `test_agent_loop_env.py`); `check_docs.py --root .
--stale` **0 broken** (1 pre-existing orphan warn; only `hint`-level staleness on
an archived doc); `check_trajectory --strict` **clean**; `gen_arch_map`
(`--src project-trajectory/scripts`, the new public functions) / `gen_okf` (SR-045
+ LLR-044/045 concepts) / `gen_trajectory` regenerated; `check.py --gate G3`
**13/13 PASS**. Spine unchanged in shape (**SN=24 SR=47 LLR=48 TC=48, 0
orphans**); SR-045/LLR-044/LLR-045 text extended.

**Re-attestation rider.** `SR-045` is a **Verified** SR whose **Requirement +
AcceptanceCriteria text changed** (pair-row identity/access split, Family-keyed
heterogeneity, version-less newest resolution, per-pair `Env`) → it rides the
**one pending G3 re-attestation** with the rest of the accumulated spine changes
(status.md Needs-\<human> #1). *Mandatory*: a Verified SR's text changed.

## 2026-07-11 — WI-070 (capability-expansion C4): the OKF knowledge tab — the dashboard becomes the bundle's first real consumer — SPINE CHANGE (SR-038 + SR-042 text extended); RE-ATTESTATION PENDING

**What shipped.** The **C4** slice and the capability-expansion campaign's last:
`PROJECT_STATE.html` gains a **Knowledge tab** that consumes the committed
`docs/okf/` OKF bundle, making the dashboard the bundle's **first real
consumer** — the gap the 2026-07-11 OKF audit named. Layered deterministic
render, no vendored JS graph lib (the CDN-bound Google visualizer and every
vendored option were disqualified by the research pass; rulings 14–16).

**Deliverables.**
- **`gen_trajectory.py` OKF loader** (`_okf_frontmatter`/`_okf_nodes`) —
  DUPLICATED per the F5 small-loader rule, **not** a `gen_okf` import (the
  sanctioned sibling import stays reserved for the large `check_trajectory`
  graph core). Walks `docs/okf/<tier>/*.md`, parses the JSON-scalar frontmatter
  (`type`/`title`/`description`/`resource`) + the `- Label: [id](href)` link
  lists into typed nodes + tier-oriented spine edges. Skips `index.md`/
  `UPSTREAM.md`; never reads the GENERATED banner (a `>` blockquote, never a
  `- ` list line) as content; a malformed file is skipped with a stderr warn.
- **The Knowledge tab** (`know_graph`/`_know_panel`) — the concept graph laid out
  server-side by the WI-DAG layouter (`_dag_ranks` longest-path + `_reorder`
  barycentre, the `sw_graph` pattern), nodes fill-keyed by OKF `type`;
  hover-highlight + click-to-detail reusing the vanilla-JS idiom. Middle-path
  embedding (ruling #15): the detail panel embeds each concept's `description`
  and **links out** to `docs/okf/<tier>/<id>.md` for the full body (a relative
  link — the bundle sits beside the artifact).
- **Vacuity + byte-identity** — the tab, its scoped `<style>`, its embedded data
  and its interaction JS are **all inside the conditional panel**, so with no
  bundle the panel is not appended and the artifact is byte-for-byte what it was
  before this view existed. `HTML_TEMPLATE` is untouched → no `--check`
  exclusion added (the as-of stamp stays the only excluded line).
- **Pre-commit hook reordered** — `okf` freshness now runs at **step 1b**,
  before the dashboard's `trajectory-map` at **1c**, because the dashboard now
  consumes the bundle; with `set -e` the hook reports the root cause (a stale
  bundle) first. Documented once in the hook comment + ADOPTING §6.
- **Docs** — PROCESS_OPTIONS "Trajectory / work-items" gains a Knowledge-tab
  paragraph (consumes the bundle, middle-path embedding, omitted without one,
  regen order arch-map → okf → trajectory); the kit `README` gen_trajectory /
  gen_okf rows and the root `README` generated-views rows updated. **No
  PROCESS.md change.**
- **Spine** — `SR-038` Requirement + AcceptanceCriteria (the knowledge-tab
  clause, rendered-with-a-bundle / omitted-without), `SR-042` Rationale (the
  consumer note — resolves the audit's no-consumer finding), `LLR-035`
  (CodeSymbol `know_graph`, Detail) and `TC-038` (Method) extended. No new SN/SR.
- **Tests** — `test_gen_trajectory.py` +6: renders-from-bundle (typed nodes,
  spine edges, embedded description, link-out target exists), omitted +
  byte-identical without a bundle (round-trip), byte-deterministic double-gen,
  `--check` stable through regen, malformed-concept-skipped-with-warn, and a
  meta-bundle smoke test over the real `docs/okf/` (~219 concepts, link-outs
  resolve). The banner-never-rendered + mobile-shell assertions ride the
  renders-from-bundle test.

**Judgment calls.**
- **Loader tolerances.** A file with no opening/closing `---` fence, or with a
  fence but no `type`, is treated as malformed → skipped with a stderr warn
  (`skipping malformed OKF concept …`), never a crash; `index.md`/`UPSTREAM.md`
  are skipped by name (not concepts); edges are parsed **only** from `- ` list
  lines and only kept when the target id is a known node, so the GENERATED
  banner blockquote and the process-guide `[docs/…](…)` source link contribute
  no spurious edges.
- **Edge orientation.** Links are oriented **upstream → downstream by tier**
  (`OKF_TIER_ORDER`), so the concept graph is a DAG the layouter can rank
  (SN→SR→LLR→TC) regardless of which file declared the link; interfaces and
  process guides carry no spine links in the bundle, so they render as isolated
  rank-0 nodes — an honest picture of what the bundle actually links.
- **Hook order (the judged reorder).** okf-before-dashboard is correct because
  the dashboard reads the bundle: reporting a stale dashboard first would send
  the author to regenerate it over a still-stale bundle. One-line move + comment.
- **Size.** The middle path embeds each concept's description; on the 219-concept
  meta bundle that is +180 KB (below the embed-all-bodies ~+250 KB alternative,
  above link-only). A downstream repo with fewer concepts pays proportionally
  less; a bundle-less repo pays nothing (byte-identical).

**Byte deltas.** `AGENTS.template.md` **9978 → 9978** and `PROCESS.md` **58,853 →
58,853** — **both untouched** (the budgeted core). `PROJECT_STATE.html`
**214,667 → 394,909 B** (+180,242, the embedded 219-concept bundle). The OKF
bundle stayed 227 files (4 concept files re-emitted for the SR-038/SR-042/
LLR-035/TC-038 text; no add/prune).

**Mechanized bar.** `pytest -q` **603 passed, 3 skipped** (+6 over WI-069's 597);
`check_docs.py --root . --stale` **0 broken** (1 pre-existing orphan warn; only
`hint`-level staleness on archived docs); `check_trajectory --strict` clean;
arch-map / okf / trajectory regenerated **in order** (arch-map → okf →
trajectory); `check.py --gate G3` **13/13 PASS**. Spine unchanged in shape
(**SN=24 SR=47 LLR=48 TC=48, 0 orphans**); SR-038/SR-042/LLR-035/TC-038 text
extended.

**Re-attestation rider.** `SR-038` (Requirement + AcceptanceCriteria) and
`SR-042` (Rationale) are **Verified** SRs whose **text changed** → they ride the
**one pending G3 re-attestation** with the rest of the accumulated spine changes
(status.md Needs-\<human> #1). *Mandatory*: a Verified SR's text changed.

**Campaign close.** With C4 landed, all four capability-expansion slices are
done (C1 run menu · C2 critique loop · C3 pair-row registry · C4 OKF knowledge
tab). The spec is **not** archived here — the coordinating session closes the
campaign (spec archival + WI reconciliation belong to that close, per the S8
campaign-close precedent).

## 2026-07-11 — Campaign close (coordinating session): capability-expansion spec archived; NO spine change

**Session.** The capability-expansion campaign is closed — all four slices
landed (the run capability menu, the `Critique` verification value + critique
loop, the pair-row agent registry, the OKF knowledge tab). The spec moved
`docs/specs/` → [archive/specs/capability-expansion.2026-07-11.md](archive/specs/capability-expansion.2026-07-11.md)
per the spec lifecycle (close date appended, an ARCHIVED banner naming the
attributed WIs WI-067…WI-070), with every in-repo citation re-pointed (this
log ×2, `status.md`) and its one internal relative link re-based for the new
depth; `docs/archive/README.md`'s `specs/` row extended. `status.md` returns
to an empty in-flight lane; next action = the owner sitting.

Also recorded here: the WI-070 close-out commit was performed by this
coordinating session after the implementing session's final gate run was
interrupted — the full bar was re-run from scratch first (pytest 603/3,
`check_docs` 0 broken, G3 13/13 PASS) so the commit rode a verified green,
not an assumed one.

**No SR/LLR/TC text touched** — docs moves + working-surface tidy only;
the re-attestation list is unchanged from the WI-070 entry above.

## 2026-07-11 — WI-071: campaign gate cadence documented + campaign vocabulary in the README (docs only)

**Session.** FB1 (gate cadence) + FB2 (campaign language) of the owner-feedback
batch (spec: [archive/specs/owner-feedback-2026-07-11.md](archive/specs/owner-feedback-2026-07-11.md);
FB1/FB2 marked ✅ DONE). This slice **dogfoods FB1's own ruling** — it ends at
the **commit bar**, not the full gate; the coordinating close runs
`check.py --gate G3` once for the whole batch.

**Deliverables.**
- **The cadence, stated once** — `PROCESS_OPTIONS.md` "Campaign ruling" paragraph
  extended with the gate cadence: mid-campaign WI slices end at the commit bar
  (hook floor + the project's test command + `check_docs --stale`); the full
  `check.py --gate <gate>` runs **once at campaign close** and CI runs it on every
  push regardless; test-impact selection ("only relevant tests") is **rejected**
  in favor of the declared `stack.ini [tiers]` **smoke** tier for slow suites.
  This is the one home for the rule.
- **session-protocol skill** — "End green (gates)" now distinguishes the **commit
  bar** from the **gate bar** (gate advancement / campaign close / CI), pointing
  at PROCESS_OPTIONS "Campaign ruling". Edited the **neutral source**
  (`project-trajectory/skills/session-protocol/SKILL.md`), then
  `bootstrap.py --dest . --sync` refreshed both fan-out copies (`.claude/`,
  `.agents/`) — verified **byte-identical** (SHA-256 match ×3; the skills-sync
  gate stays green).
- **Root README** — one sentence added to the registry map adopting the
  **campaign** vocabulary (batch spine-touching work → one owner sitting
  re-attests it all, the gate cadence riding the same convention), linking the
  PROCESS_OPTIONS home; no mechanics duplicated.
- **Kit README** — the existing one-off "shared campaign doc" mention (line ~36,
  spec-of-record file layout) checked and left as-is: consistent with the
  documented cadence, no contradiction.

**Docs only — no spine change, no re-attestation impact.** No SR/LLR/TC row
touched; the pending G3 re-attestation list is unchanged.

**Byte deltas (budgeted files).** `AGENTS.template.md` and `PROCESS.md`
**untouched** (0 delta) — the cadence expansion landed in `PROCESS_OPTIONS.md`
(not budgeted), per the push-expansion rule.

**Mechanized bar (commit bar).** `pytest -q` → **572 passed, 34 skipped**
(0 failures; same 606 total as the WI-070 entry's 603/3 — the elevated skip
count is environmental, optional-tool-gated tests, and no test logic changed
this session). `check_docs.py --root . --stale` → **0 broken** (1 pre-existing
`docs/test/report.md` orphan warn + hint-level staleness on archived docs only).
`gen_trajectory.py` regenerated `PROJECT_STATE.html` after the WI-071 registry
close; `gen_okf --check` up to date (227 files). The full `check.py --gate G3`
is **deferred to the campaign close** per the cadence just documented.

## 2026-07-11 — WI-072: OWNER_SCRATCHPAD.md + check_docs scan-scope (archive, scratchpad) — docs/scripts only, NO spine change

**Session.** FB3 (owner scratchpad) + FB4 (archive scan-scope) of the
owner-feedback batch (spec:
[archive/specs/owner-feedback-2026-07-11.md](archive/specs/owner-feedback-2026-07-11.md);
FB3/FB4 marked ✅ DONE). Per FB1's ruling this slice ends at the **commit bar**,
not the full gate; the coordinating close runs `check.py --gate G3` once.

**Deliverables.**
1. **The owner scratchpad (FB3).** Root `OWNER_SCRATCHPAD.md` (meta) +
   `project-trajectory/OWNER_SCRATCHPAD.template.md`, **byte-identical (651 B
   each)**, scaffolded to a downstream root via a new `bootstrap.py` MAPPING
   entry (beside the README front door). The file opens with a loud header block —
   *for the human owner only; LLM agents must not read, index, summarize, cite,
   or act on it; nothing here is a requirement, ruling, or working surface (those
   are `docs/status.md`, the registries, `docs/log.md`); notes may be stale,
   contradictory, augmented, or half-formed; the always-on secrets floor still
   scans it, so it is not a secrets-safe zone* — then an empty notes area (an `---`
   and a placeholder comment).
2. **check_docs exempts the scratchpad entirely (FB3).** `collect_docs` drops
   root `OWNER_SCRATCHPAD.md` from doc discovery via the **WI-066 okf-exclusion
   idiom** (`SCRATCHPAD` constant beside `OKF_DIR`): its links, orphanhood, and
   staleness never gate — free-form owner notes must never block a commit — but it
   still resolves as a link *target* and the secrets floor still scans it.
3. **check_docs archive scan-scope (FB4).** `docs/archive/` files **KEEP
   broken-link validation** (a dead link in the design history still misleads a
   reader) but are **DROPPED from orphan warnings and stale-mtime hints** (a frozen
   doc's orphanhood/staleness is noise by definition). Implemented narrowly: an
   `ARCHIVE_DIR` constant + one `_in_archive()` helper, filtered in `find_orphans`
   and `find_stale`; the rationale stated once at the constant.
4. **Agent-side ignore.** The meta `CLAUDE.md` (not budgeted) gained a one-liner
   callout ("`OWNER_SCRATCHPAD.md` is owner-only — never read, cite, or act on
   it"). A reinforcement note also landed in `PROCESS_OPTIONS.md` §7 (the
   memory/scratch discussion — the owner scratchpad framed as the human
   counterpart to agent scratch) and a **kit README Contents row**. The file's
   own loud header is the primary defense.

**AGENTS.template.md decision.** **Untouched — 9,978 → 9,978 bytes (22 B headroom
preserved).** The file offered only 22 B of headroom; a meaningful "don't read
the scratchpad" line (~50–70 B) would have required manufacturing an equal
tightening in the crisp, universally-inherited working agreement purely to fund a
niche, file-specific instruction — no clean net-≤22-B fold exists without diluting
a durable rule (the WI-045 fold worked because it folded genuinely-redundant
framings; there is none to fold here). Per the spec's stated fallback, the line
went to `PROCESS_OPTIONS.md` (scaffolds to `docs/process-options.md`, so downstream
agents still get it) + the meta `CLAUDE.md`, and the file's own header remains the
primary defense.

**Spine (SR-012) decision — NO text change.** SR-012's claim (check_docs fails on
a broken intra-repo link / missing PROJECT-VISION tag, checks freshness under
`--stale`) is unchanged and untouched. Both new behaviors are **scan-scope within
that existing claim** — exactly the **WI-066 precedent** (the okf exclusion was
recorded as "scan-scope within SR-012", no spine edit): the scratchpad exemption
and the archive orphan/stale drop change *which files* the orphan/staleness
heuristics survey, not what a broken link or a missing vision tag means. Verified
SR-012's AcceptanceCriteria is not contradicted (broken links still fail, incl. in
the archive). Nothing new rides the pending G3 re-attestation.

**Meta run (before → after).** `check_docs --root . --stale`: **stale hints
27 → 0** — every one of the 27 pre-existing hints was on an archived doc
(`AGENT_ROLES.md`, `AXES_AND_WORKSTREAMS.md`, `IMPROVEMENT_PLAN.md`,
`THREAD_52_REVIEW.md`), so all vanish; **orphan warnings 1 → 1** (the pre-existing
`docs/test/report.md`, deliberately out of scope — not an archive doc); 27 docs,
182 links, 0 broken. `PROJECT_STATE.html` regenerated after the WI-072 registry
close; `gen_okf`/`gen_arch_map` `--check` up to date.

**Byte deltas (budgeted files).** `AGENTS.template.md` **untouched (9,978)**;
`PROCESS.md` **untouched**. The FB3 reinforcement expanded `PROCESS_OPTIONS.md`
(not budgeted), per the push-expansion rule.

**Mechanized bar (commit bar).** `pytest -q` → **609 passed, 3 skipped**
(0 failures; +6 over the 603 real-pass baseline — 5 new `test_check_docs.py`
tests [scratchpad-exempt, archive-broken-link-fails, archive-not-orphan-but-live-is,
`find_stale`-skips-archive unit, archive-stale-suppressed end-to-end] + 1
`test_bootstrap.py` [scaffolds-owner-scratchpad, byte-identity to template]).
`check_docs.py --root . --stale` → **0 broken** (1 out-of-scope orphan warn, 0
stale hints). Spine unchanged at **SN=24 SR=47 LLR=48 TC=48, 0 orphans** (49
interface seams). The full `check.py --gate G3` is **deferred to the campaign
close** per FB1's cadence.

## 2026-07-11 — WI-073 (owner-feedback FB5): How-SW top view ≤10 items via CMP containerization + the right-sizing rule — SPINE CHANGE (SR-048 added; SR-038 clarified); RE-ATTESTATION PENDING

**Owner directive (FB5).** In the software-architecture diagram on
`PROJECT_STATE.html` the first view must show **at most 10 items**; software items
that belong to a component are **containerized** into it (a component may contain
components), and exceeding the bound is a **failure** that drives right-sizing of
the component designations. Spec: `docs/specs/owner-feedback-2026-07-11.md#fb5`.

**What shipped.**
- **`check_trajectory.py` — the right-sizing rule.** New `component_top_view()` is
  the **one home** for the AXES membership join: `arch_inventory` modules ×
  `load_cmps` CMP rows × `module_components` (the `Component` tag on an LLR joins
  `LLR.Module → CMP-###`); `_cmp_roots` resolves `PartOf` up to the top-level
  root(s), cycle-guarded. `component_findings()` bounds the top view at
  `TOP_VIEW_MAX = 10` (top-level components that contain a module + uncontained
  modules) — **WARN plain, ERROR under `--strict` (G2+)**, printed before the WI
  vacuity return so a big arch-map with no CMPs trips even with no work items.
  Opt-out `docs/components-check` (the `interfaces-check` reader; **no scaffolded
  file, absence = on** — confirmed matching the interfaces-check precedent);
  **vacuous** at ≤10 modules or with no arch-map inventory (the bound, not the
  registry, is the rule).
- **`gen_trajectory.py` — the containerized render.** `sw_containment()` imports
  the same `ct.component_top_view` derivation (so the render and the rule can
  never disagree on the count) and renders the How-SW panel as a native
  **`<details>` tree** (no JS → deterministic, offline, byte-stable through
  `--check`): top-level components + uncontained modules as the first view, each
  component expanding to its member modules, nested child components, and the
  seams internal to it. IF seams crossing a component boundary **aggregate to one
  deduplicated component-to-component edge** at the top level (the module-level
  ids listed on the one edge); intra/boundary seams live in the expansion. When no
  CMP contains a module the panel keeps today's flat graph/table **byte-identical**
  (proven by a round-trip test). `build_html` routes `Category=software` CMPs to
  the containerized How-SW view and non-software CMPs to the How-physical table, so
  a domain-neutral CMP lands in the tab matching its category.
- **Meta dogfood.** Authored `docs/requirements/components.csv` — **5 right-sized
  software components**: `CMP-001` Traceability core (trace/check/check_trajectory,
  3 modules), `CMP-002` Generators (gen_arch_map/gen_trajectory/gen_okf/
  gen_release_checklist/gen_skills_index/gen_cases, 6), `CMP-003` Quality checkers
  (check_docs/check_doc_refs/check_dupes/check_flows/check_perf/check_stubs/
  check_vendored, 7), `CMP-004` Unattended loop & floor (agent_loop/agent_route/
  score_reviews/subagent_gate/check_privacy, 5), `CMP-005` Scaffold & onboarding
  (bootstrap/run_menu, 2). Added the `Component` column + a tag to **all 48 meta
  LLR rows** (hooks → CMP-004, onboard → CMP-005 for completeness even though they
  are not arch-map modules). **Result: the meta How-SW top view drops from 23
  modules to 5 components, 0 uncontained** (`trace components=5
  component-findings=0`; `check_trajectory --strict` green with the new rule).

**Component cut — why this cut.** Grouped by role along the real architecture (the
same shape `architecture.md` already narrates: checkers/generators, the floor, the
declared config): the join+harness core; the `--check`-gated generators; the
quality lints; the autonomous coordinator + its safety floor; and the
zero-to-running scaffold surface. Kept flat (5 top-level, no nesting in the meta
data — nesting is exercised by tests) because the real architecture has no deep
subsystem tree; every arch-map module lands in exactly one component, so nothing is
uncontained.

**Judgment calls.**
- **Edge aggregation** is at the *top-level root*: an IF between two modules in
  different top-level components → one deduped root→root edge; same-root → intra
  (shown in the expansion); a file/external counterpart → a boundary seam of the
  module's component. Aggregation dedups on `(rootA, rootB)` with the contributing
  IF ids collected — one edge per crossing pair (regression test: IF-001 + IF-002
  both crossing CMP-001→CMP-002 render as ONE edge naming both).
- **Expansion mechanism** = native HTML `<details>` (the spec sanctioned a
  `<details>`-style approach): zero JS, so it stays deterministic and byte-stable
  through `--check` without touching the existing vanilla-JS icicle/DAG/Knowledge
  interaction code. Nested components render as nested `<details>` inside the
  parent.
- **`SR-038` decision — minimal clarify, not silent, not over-touch.** The new
  render introduces one genuine contradiction with SR-038's text ("the component
  table when CMP rows exist" is now false for a software-only CMP set, which routes
  to the containerized How-SW view). Made the **minimal** edit: "the software
  module-map view … (containerized into its components when a CMP layer contains
  modules, else the flat module map), the **non-software** component table when
  non-software CMP rows exist". Left the rest of SR-038 alone (its acceptance
  criteria never named the CMP table and its testable claims still hold). Rides the
  pending re-attestation (SR-038 was already pending from WI-070).
- **`Category` routing of `_cmp_panel`.** Filtering the How-physical table to
  non-software CMPs is a behavior change to `build_html`, but it is the honest cut
  (CMP is domain-neutral) and non-breaking: no test asserted software CMPs in the
  physical table, and a physical-CMP or no-CMP repo is unaffected.

**Spine.** +`SR-048` under `SN-023`/`SN-012` (the architecture view stays legible —
the top view is bounded at 10 via declared composition, and exceeding it is a
finding that drives component right-sizing) + `LLR-049` (check_trajectory,
`Component=CMP-001`) + `TC-049` (Automated=Yes; Evidence = test_trajectory.py +
test_gen_trajectory.py). `SR-038` text minimally clarified. Spine now **SN=24
SR=48 LLR=49 TC=49, 0 orphans, 0 integrity, 0 schema, 0 status findings**;
`components=5`, `interfaces=49`. **Rides the one pending G3 re-attestation**
(SR-038 text changed + SR-048/LLR-049/TC-049 joined the spine).

**Docs.** `PROCESS_OPTIONS.md` "Component layer" gained "The How-SW top view is
bounded" (the ≤10 rule + the containerized render + the `docs/components-check`
switch + the `Category` routing), stated once. `components.template.csv`'s CMP-000
explainer gained the top-view note pointing at that section. `AGENTS.template.md`
and `PROCESS.md` **untouched** (not in scope — verified below).

**Regenerated (view artifacts).** `gen_arch_map` (the new public functions in
check_trajectory/gen_trajectory entered the module map) → `gen_okf` (spine change;
230 files) → `PROJECT_STATE.html` (the containerized How-SW panel; the WI-073
close). All three `--check` up to date; `trace --strict-integrity` 0.

**Byte deltas (budgeted files).** `AGENTS.template.md` **untouched (9,978)**;
`PROCESS.md` **untouched**. The rule + render narrative expanded
`PROCESS_OPTIONS.md` (not budgeted) per the push-expansion rule.

**Mechanized bar (commit bar).** `pytest -q` → **622 passed, 3 skipped**
(0 failures; +13 over the 609 baseline — 7 new `test_trajectory.py` [over-bound
warn/strict, declaring-components-clears, nested-counts-at-root, uncontained-count,
off-switch, ≤10 vacuous, absent-inventory vacuous] + 6 new `test_gen_trajectory.py`
[containerizes, boundary-dedupe, no-CMP flat byte-identical, deterministic+--check,
nested renders inside parent, meta smoke]). `check_docs.py --root . --stale` →
**0 broken** (1 pre-existing out-of-scope orphan warn). The full `check.py --gate
G3` is **deferred to the coordinating close** per FB1's cadence.

## 2026-07-11 — Batch close (coordinating session): owner-feedback spec archived; the batch's ONE full gate

**Session.** The owner-feedback batch is closed — FB1/FB2 (WI-071), FB3/FB4
(WI-072), FB5 (WI-073) all landed at the commit bar per the cadence FB1
itself documented. The spec moved
`docs/specs/` → [archive/specs/owner-feedback-2026-07-11.md](archive/specs/owner-feedback-2026-07-11.md)
(the basename already carries the close date — drafted and closed the same
day — so no second suffix; the ARCHIVED banner names WI-071…WI-073), with
every citation re-pointed (this log ×2, `status.md`) and the archive README
`specs/` row extended. `status.md` returns to an empty in-flight lane.

**The one full gate** (the new cadence's close obligation) runs in this
session over the whole batch — result recorded in this entry's commit and
the coordinating summary.

**No SR/LLR/TC text touched by the close** — the batch's spine changes
(SR-048/LLR-049/TC-049, the SR-038 clarification) are recorded in the WI-073
entry above and ride the one pending re-attestation.

**Correction (same session, honest record).** The close entry above was
committed while the batch's full gate had actually returned **FAIL** — the
`format` step: WI-073 left `gen_trajectory.py` un-ruff-formatted, and the
commit floor never caught it because the hook's Python lacks ruff (the hook
SKIPs format; the gate's declared `{py}` toolchain runs it — the gap is
precisely why the cadence keeps ONE full gate at batch close). Fixed with the
gate's own interpreter (`ruff format`, 1 file), lint clean, and the full bar
re-run from scratch: `pytest -q` **622 passed / 3 skipped**, `check_docs`
**0 broken**, `check.py --gate G3` **RESULT: PASS (13/13)**. The FB1 cadence
worked as designed — the close gate caught what the commit bar structurally
cannot.

## 2026-07-11 — WI-074 (campaign-binning batch, slice 1): the `Campaign` column + the When-view binned by it

**Session.** WI-074 (P1 of the campaign-binning · parallel-tests ·
resume-hardening batch) landed at the **commit bar** — the batch's one full
`check.py --gate G3` runs at the coordinating close, not here. Owner-directed:
give a WI's campaign membership a **queryable, durable home** (after `SpecRef`
clears at close it lived only in the archived spec banner + log narrative) and
**bin the roadmap DAG** like the software architecture (the FB5 symmetry —
WHEN-axis binning = campaign, HOW-axis binning = CMP).

**Deliverables.**
- **`Campaign` column** on `work-items.template.csv` (with an explainer in the
  inert `WI-000` row) + the meta registry. `check_trajectory.load_wis` reads it
  as a `campaign` field — a mutable grouping tag in the **`Workstream`
  precedent**, NOT id-checked (no vocabulary rule); empty = standalone; a legacy
  CSV without the column reads `""` (never-breaking). No validation was added.
- **When-view binning** — new `gen_trajectory.campaign_containment(wis)` mirrors
  `sw_containment` (the FB5 idiom): work items sharing a `Campaign` tag collapse
  into a native `<details>` container (member table: WI/Title/Status/Delivers/
  After), campaign-crossing predecessor edges **aggregate to one deduplicated
  container-to-container edge** (contributing WI edges listed), and campaign-less
  WIs render **flat** below the containers. It returns `None` when no WI carries a
  campaign, so `$dag_svg` falls back to today's flat SVG DAG and a campaign-less
  registry renders **byte-identically**. **Deliberately no right-sizing bound**
  (the FB5 asymmetry): a campaign is bounded by construction (one re-attestation
  sitting each), so binning is presentation only — no new gate.
- **Meta backfill (honest).** WI-053…059 → `working-surface-restructure-2026-07-11`
  (7), WI-067…070 → `capability-expansion-2026-07-11` (4), WI-071…073 →
  `owner-feedback-2026-07-11` (3), WI-074…076 → `campaign-binning-batch-2026-07-11`
  (3). All other rows stay empty — no retroactive invention. The meta When-view
  now renders **4 campaign containers + 59 standalone WIs** (was a 76-node flat
  SVG DAG).
- **Docs.** One sentence in the PROCESS_OPTIONS "Campaign ruling" paragraph (the
  column exists, the DAG bins by it, no right-sizing bound) + the template
  explainer row.

**Spine decision — NO spine change.** Verified against SR-037/SR-038: SR-037
enumerates *checks*, not columns, and the `Campaign` tag adds no check (the
`Workstream` precedent, also read-not-validated and unmentioned there). The
binned render sits inside SR-038's existing **"prospective roadmap DAG"** claim;
its AcceptanceCriteria ("the roadmap DAG render from the registries") stays
literally true and TC-038 (which only asserts "Satisfies SR-038
AcceptanceCriteria") is not invalidated — no assertion requires the DAG be SVG.
The asymmetry with SR-038's How-SW containerization clause is principled: that
clause exists because WI-073 minted the SR-048 right-sizing *rule* (a mechanized
gate); campaigns deliberately mint no SR and no right-sizing rule, so
presentation-only binning needs no requirement clause. **This does NOT ride the
pending re-attestation.**

**Byte deltas.** Byte-budgeted files (`AGENTS.template.md`, `PROCESS.md`)
**untouched** (verified — empty diff). `PROJECT_STATE.html` 393,503 → 385,720 B
(**−7,783**; the compact `<details>` tree replaced the 76-node SVG DAG).
`docs/architecture.md` +1 line (the new `campaign_containment` public symbol);
`docs/okf` bundle unchanged (it doesn't read `work-items.csv`; `--check` clean).

**Gates (commit bar).** `pytest -q` **629 passed / 3 skipped** (+7 over the 622
baseline: 6 new `test_gen_trajectory.py` [containerize, flat-outside-container,
no-campaign byte-identical, boundary-dedupe, deterministic+--check, meta smoke] +
1 `test_trajectory.py` [Campaign never-breaking]). `check_docs.py --root .
--stale` → **0 broken** (1 pre-existing out-of-scope orphan warn).
`gen_arch_map --check`, `gen_okf --check`, `gen_trajectory --check` all clean.
`ruff format`/`ruff check` (the gate interpreter) clean. The full `check.py
--gate G3` is **deferred to the coordinating close** per the batch cadence.

## 2026-07-11 — WI-075 (campaign-binning batch, slice 2): pytest-xdist parallel execution — verified, no spine change

**Session.** WI-075 (P2 of the campaign-binning batch) landed at the **commit
bar** — the batch's one full `check.py --gate G3` runs at the coordinating
close, not here. Owner-directed: the fully-serial suite (~377 s, no hotspot —
time is spread across hundreds of ~0.5 s subprocess/scaffold tests) is
embarrassingly parallel (every test isolated in `tmp_path`), so wire
**pytest-xdist `-n auto`** and **verify, don't assume** the three risks the
owner named.

**Deliverables.**
- **Wiring.** `docs/stack.ini` `[product] test` gains `-n auto` (the `smoke`
  tier line + the `[coverage]` args untouched — check.py still appends them).
  `scripts/dev-setup.{sh,ps1}` gain a **pytest-xdist** check row + the
  `--install` set (`dev-setup.command` delegates to `.sh`, so it inherits both).
  pytest-xdist is **dev tooling**, not a kit script — the stdlib-only rule
  governs `project-trajectory/scripts/`, not the test tooling (the
  pytest/pytest-cov precedent).
- **Template posture.** The shipped `stack.ini.template` keeps the plain
  `test = {py} -m pytest -q` with a **commented** `-n auto` opt-in line + one
  explainer sentence: a downstream suite may not be xdist-safe, so opting in is a
  knowing act. configparser ignores the comment, so the template plan stays
  byte-identical to check.py's built-ins (`test_reference_profile_matches_builtin_plan_every_tier`
  still passes).
- **Docs.** A new **"Parallel test execution"** paragraph in the PROCESS_OPTIONS
  "Trajectory / work-items layer" (beside the Campaign ruling): parallelism is a
  stack.ini concern; the FB1 **test-impact-selection rejection stands** (the
  sanctioned levers are the smoke tier per commit + parallel execution at the
  gate); the **session-scoped shared-scaffold fixture is the recorded fallback
  lever — filed, not built**. No README kit-contents row: the scaffold **surface**
  is unchanged (only `stack.ini.template`'s content).

**Verify, don't assume — the three owner items, on 24 workers (`-n auto` on a
24-core box).**
- **(a) Subprocess coverage under xdist HOLDS.** Full coverage command
  (`pytest -q -n auto --cov=project-trajectory/scripts --cov-report=term-missing
  --cov-fail-under=80`) → **combined total 90.8%** (serial baseline ~91% —
  **unchanged**), exit 0, "Required test coverage of 80% reached." The
  `conftest.augment_env` wiring works **per-worker**: each xdist worker runs under
  pytest-cov (`COV_CORE_DATAFILE` set per worker; here pytest-cov 4.1.0), so the
  subprocesses each worker spawns start coverage against that worker's datafile,
  and `.coveragerc parallel=true` + the session-end combine folds it all back.
  No silent unwiring. Coverage **step time 726 s → 157 s** (~4.6×).
- **(b) Meta-tree readers are concurrency-safe.** Surveyed every test that reads
  the real repo (not `tmp_path`): `check_privacy --repo`, `gen_skills_index
  --check` (returns before its write), `dev-setup --check` (installs nothing),
  and `gen_trajectory` graph reads (`know_graph`/`component_top_view`/
  `sw_containment`/`load_wis`) — **all read-only**. No test calls `os.chdir`;
  subprocess `cwd=` is per-call, and env vars + cwd are per-worker-process, so
  the only cross-worker hazard (a shared non-`tmp_path` write) does not occur.
  No markers/serialization needed.
- **(c) Windows spawn overhead is fine.** Plain suite **377 s → 71.0 s / 61.4 s**
  across the two required runs (~5.5×).

**Flake honesty — two clean parallel runs.** Both plain runs `629 passed / 3
skipped` with **zero flakes**; the coverage run `629 passed / 3 skipped`; the
commit-bar run `630 passed / 3 skipped` (+1 = the new stack-profile guard).
`pytest.ini` declares no `addopts`/`--reruns`, and pytest-rerunfailures is not
configured, so a flake would have surfaced honestly. None did.

**CI decision (`.github/workflows/test.yml`).** Both jobs parallelize. The
**gate** job runs check.py, which reads the meta `docs/stack.ini` and so inherits
`-n auto` automatically — pytest-xdist is therefore **required** there (check.py
SKIP-guards only `-m <module>`/`--cov` deps, not the `-n` flag, so a missing
xdist would **fail** the tests+coverage step, not skip). Added it to the gate
job's install. The **matrix `test`** job runs `pytest -q` directly; parallelized
it too (`-n auto` + the dep) so all three OSes exercise the same parallel path
developers and the gate run — the minimal coherent choice (a serial matrix would
never test cross-OS xdist-safety and would leave CI's slowest job un-sped).

**Spine decision — NO spine change.** Dev tooling + a change to the declared
stack test command; no requirement is added or altered. Verified **SR-034**
(Analysis) and **SR-035** (cross-OS CI) are not contradicted: their stdlib-only
claims are about the **kit scripts** (`project-trajectory/scripts/`), not the
test tooling, and SR-035's "CI inherits the stack.ini command" is exactly what
now parallelizes. **Does NOT ride the pending re-attestation.**

**Byte deltas.** Byte-budgeted files (`AGENTS.template.md`, `PROCESS.md`)
**untouched** (verified — not in the diff). `PROJECT_STATE.html` 385,720 →
385,716 B (**−4**; the WI-075 node flips queued→done). `PROCESS_OPTIONS.md`
+16 lines (the parallel-execution paragraph). No `docs/okf` / arch-map churn
(neither reads `work-items.csv`; `--check` clean).

**Gates (commit bar).** `pytest -q -n auto` **630 passed / 3 skipped** in 65.8 s.
`check_docs.py --root . --stale` → **0 broken** (1 pre-existing out-of-scope
orphan warn + pre-existing README stale hints, all warn-only). `ruff format` /
`ruff check` (the gate interpreter, `C:/Python38`) clean. The full `check.py
--gate G3` is **deferred to the coordinating close** per the batch cadence.
**Next up: WI-076** (dirty-tree resume hardening — the batch's last slice).

## 2026-07-11 — WI-076 (campaign-binning batch, slice 3): dirty-tree resume hardening — detect + surface + stale-lock recheck — no spine change

**Session.** WI-076 (P3, the batch's **last** slice) landed at the **commit
bar** — the batch's one full `check.py --gate G3` runs at the coordinating
close, not here. Owner question: an interrupted agent session can leave
working-tree residue; on resume, will the next session notice and recover?
Answer (recorded in the spec): the *logical* layer is interruption-safe (progress
= commits; an uncommitted interruption leaves the WI open + named in status.md +
blocked from a confused mixed commit by the hook floor), but **noticing was not
mechanized** — the preflight checked command/CLI/git/privacy/locks, not tree
cleanliness. This slice mechanizes the noticing (the **thin slice** — detect +
surface, never auto-stash; full stash/rollback stays deferred as **WI-060**).

**Deliverables.**
- **Detect + surface at the loop (`agent_loop.py`).** New `working_tree_dirty(root)`
  helper — `git status --porcelain` through the encoding-safe `git()` reader
  (text, `errors=replace`, like the siblings), returning the porcelain lines
  (one per uncommitted path; a rename is a single `R  old -> new` entry, an
  untracked file a single `?? path` entry). New module constant
  `RESUME_RECONCILE_NOTE` (the injected text, kept in **ONE place**). At loop
  start the coordinator (a) logs one stderr line — `working tree carries N
  uncommitted path(s) — likely an interrupted session` — and (b) prepends the
  reconcile note (+ `--- ` separator) to the **first** session's composed prompt,
  routed through the existing `session_prompt()` composition point (`resume_reconcile`
  closure var) so guardrails-core / track-preamble / reviewer-body composition is
  unchanged. **Surface only — never stash, clean, or block.**
- **Protocol text.** The `session-protocol` skill (neutral source
  `project-trajectory/skills/session-protocol/SKILL.md`) gains a "**Check `git
  status` first**" bullet in §1 Read-before-doing (reconcile residue against the
  open WI's spec/Done-when before new work). `bootstrap.py --dest . --sync`
  fanned it out **byte-identical** to `.claude/skills/` + `.agents/skills/`
  (skills-sync gate green). `PROCESS_OPTIONS.md` "Unattended operation" gains one
  sentence (the loop surfaces a dirty tree into the first session's prompt;
  stash/rollback deliberately not automated — the judgment belongs to the session).

**Scope choice — ONCE at loop start, NOT per-iteration (the honest call).** The
spec floated "at loop start *and* each session launch." Chose **once-at-start**,
after reasoning it out: the coordinator writes its own **tracked** bookkeeping
between sessions — `docs/iteration/NNN-<stamp>.log` + the regenerated
`iteration_index.md` (only `out/` is gitignored) — *after* each session, to be
committed by the *next* session. So in a healthy run the tree is legitimately
non-empty before every iteration ≥ 2 (a one-session-lagging log + index), and a
per-iteration check would **false-positive every pass** on the loop's own
artifacts — worse, it would tell the session to "reconcile interrupted-session
residue" about the coordinator's own logs. The only point where the tree purely
reflects the **outside world** is *before iteration 1* — a fresh coordinator
resuming a repo someone left dirty, which is exactly the interruption-recovery
signal WI-076 targets (a killed session ⇒ a fresh `agent-resume.*` ⇒ a fresh
`main()` ⇒ loop start). The snapshot is taken **before `acquire_lock`** so the
coordinator's own `out/agent-loop.lock` never counts as residue (in a scaffold
`out/` is gitignored so it would not anyway; taking it first is correct
regardless of a repo's `.gitignore` hygiene — and it is what makes the
clean-tree test byte-exact).

**Stale-lock recheck — SAFE, no fix needed (verify + report).** Read the WI-025
lane-lock code: the per-worktree lock is a **kernel advisory lock** (`fcntl.flock`
on POSIX, `msvcrt.locking` on Windows) held on an open descriptor for the
process's lifetime. The OS releases it automatically on process exit **including
a crash or SIGKILL**, so a killed holder **cannot wedge** the next run — there is
no stale-pid file to reason about and no PID-reuse hazard (the pid/host/stamp in
the file are human-readable diagnostics only, never the liveness signal). The
killed-holder case is **already covered** by `test_lock_auto_released_when_holder_dies`
(a subprocess probe acquires the lock then `os._exit(0)` — no release/atexit,
modelling a crash — after which the parent acquires cleanly). Per the spec's
"add the missing test only if cheap," none was added (it already exists);
recorded here.

**Spine decision — NO spine change.** The reconcile injection is **prompt
composition inside the existing session contract** — no new coordinator
capability, no new requirement. Verified the adjacent SRs honestly:
**SR-026/027/028** (the unattended-loop / run-state / resume claims) are not
extended — surfacing a pre-existing tree state to the session it already launches
adds no promise they must now cover. **Does NOT ride the pending re-attestation.**

**Tests (+3, `tests/test_agent_loop.py`).** `test_dirty_tree_at_start_injects_reconcile_and_logs`
(dirty tree ⇒ the stderr log line + the reconcile note in the composed prompt;
surface-only — the residue is neither committed nor cleaned by the loop);
`test_clean_tree_prompt_is_byte_identical` (clean tree ⇒ prompt is byte-for-byte
`DEFAULT_PROMPT`, no dirty line logged); `test_working_tree_dirty_counts_renames_and_untracked`
(porcelain parse: a rename is one entry not two, an untracked one entry, clean is
empty). The existing skills-sync test covers the byte-identical fan-out (green).

**Byte deltas.** Byte-budgeted files (`AGENTS.template.md`, `PROCESS.md`)
**untouched** (verified — not in the diff). `agent_loop.py` +67/−4 lines.
`PROCESS_OPTIONS.md` +4/−1 lines. `PROJECT_STATE.html` 385,716 → 385,712 B
(**−4**; the WI-076 node flips queued→done). No `docs/okf` / arch-map churn.

**Gates (commit bar).** `pytest -q -n auto` **602 passed / 34 skipped** in 52.4 s
(**0 failed**; the 34 skips are all the pre-push/pre-commit **hook shell tests**
— `needs a POSIX shell and git on PATH` — an environmental platform gate under
this PowerShell-invoked run, unrelated to WI-076; the 3 new tests all pass).
`check_docs.py --root . --stale` → **0 broken** (the same pre-existing orphan +
README stale hints, warn-only). `ruff format` / `ruff check` (the gate
interpreter, `C:/Python38`) clean. The full `check.py --gate G3` is **deferred to
the coordinating close** per the batch cadence — **all three batch slices
(WI-074/075/076) are now done at the commit bar, awaiting that close.**

## 2026-07-11 — Batch close (coordinating session): campaign-binning batch spec archived; the batch's ONE full gate

**Session.** The campaign-binning · parallel-tests · resume-hardening batch
is closed — all three slices landed at the commit bar per the campaign
cadence. The spec moved `docs/specs/` →
[archive/specs/campaign-binning-parallel-tests-resume-hardening.2026-07-11.md](archive/specs/campaign-binning-parallel-tests-resume-hardening.2026-07-11.md)
(close date appended, ARCHIVED banner naming WI-074…WI-076); status.md
citations re-pointed, the archive README `specs/` row extended, the done-WI
id tokens scrubbed from the working surface (R-D), and the in-flight lane
returned to empty. The batch's one full gate runs in this close — its result
rides this entry's commit.

**No SR/LLR/TC text touched by the batch or the close** — all three slices
verified no-spine-change honestly (recorded in their entries above); nothing
new rides the pending re-attestation.

## 2026-07-12 — WI-077: owner-directed deep review + confident fixes + parallel harness steps (deep-review-2026-07-12)

**Session.** Owner-directed full-repo review (logs/archive out of scope), the
report committed first ([archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md),
commit `9cba199`), then the confident fixes in this entry's commit. **No
critical findings**; four owner rulings queued in status.md Open items #6 (F5
duplication census/bound · wiring `[step:dupes]` · the archive-anchor comment
policy · the `agent_loop`/`trace`/`bootstrap` `main()` decomposition campaign).

**Fixes (the review's H2/H3/H4/M3/M4).**
- **H4 — parallel harness steps.** `check.py --jobs N` (0 = auto) runs the gate
  plan's steps concurrently in *lanes* (`registry-integrity` + `traceability`
  share one — both trace.py runs rewrite `docs/test/report.md`; every other
  step is read-only or writes a disjoint artifact), each step's output captured
  and printed whole (never interleaved); the sequential `--jobs 1` default
  keeps downstream behavior byte-identical. `--run-steps A,B,…` is the batch
  form of `--run-step` (lenient, parallel, reports **every** failure).
  `hooks/pre-commit`'s six chained `--run-step`/script calls collapsed to one
  batched call — faster on every commit, and a commit with several stale
  artifacts now names them **all in one pass** (supersedes the `set -e`
  okf-before-dashboard first-failure ordering). CI's gate job runs `--jobs 0`.
- **H2 — commit-bar speed.** The session-protocol skill (source + both fan-out
  copies, byte-identical, `--check-agents` green) and `CLAUDE.md` now state
  `python -m pytest -q -n auto` — the declared stack.ini command (~70 s vs
  ~340 s serial; the largest per-commit win available).
- **H3 — gen_trajectory dedup.** The rank→order→barycentre→coordinates block
  the WI-DAG / How-SW / Knowledge views each carried (~100 significant tokens
  × 3 per `check_dupes.py`) extracted into one `_layered_layout()`; verified
  **byte-identical** (`gen_trajectory.py --check` green *before* any regen).
- **M3 — valid HTML.** The dashboard's inner When-view `<div id="dag">`
  duplicated its section's id; renamed `dag-view` (zero behavior change —
  `getElementById('dag')` already resolved the section by document order).
- **M4 — .gitattributes.** The meta root-anchored `hooks/pre-commit` pattern
  matched **nothing** (hooks live at `.githooks/` + `project-trajectory/hooks/`;
  only the `*` catch-all saved them) — replaced with the real paths;
  `gitattributes.template` gains the shipped-but-unlisted `.githooks/commit-msg`.

**Spine decision — NO spine change.** `--jobs`/`--run-steps` preserve SR-006's
claim exactly (the active gate's required steps run; a missing tool fails,
never silently passes) — concurrency is execution mechanics, not requirement
surface (the WI-075 dev-tooling precedent). Verified SR-007/SR-008 untouched
(profile reading/validation unchanged). **Nothing rides the pending
re-attestation.**

**Tests (+4, `tests/test_check_harness.py`).** Batch green on a clean scaffold;
batch reports **every** failure (stale arch-map + duplicated SR id in one run);
unknown step name fails loudly; `--jobs 0` plan matches the sequential plan's
step set and still fails on a failing test (never a false green). Hook +
gen_trajectory test anchors updated to the batched call / `dag-view`.

**Byte deltas.** Byte-budgeted files (`AGENTS.template.md` 9,978 B,
`PROCESS.md` 58,853 B) **untouched**. `check.py` +171/−36 lines;
`gen_trajectory.py` −44 net (the dedup); `hooks/pre-commit` −34 net.
`PROJECT_STATE.html` regenerated (WI-077 node + arch-map symbol updates).

## 2026-07-12 — Follow-up: deep-review report archived; the remaining owner items moved inline to status.md

**Session (owner-directed follow-up).** The review report moved
`docs/` → [archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md)
with the ARCHIVED banner (the spec-lifecycle idiom); the archive README gained
its row. status.md Open items #6 now names **every** owner item inline — the
four rulings plus `Links.rtf` and the `AGENTS.template.md` 22-byte-headroom
note — so nothing awaits a decision outside the working surface. Citations
re-pointed (this log's WI entry link + the WI registry Deliverable path); no
code, spine, or template change.

## 2026-07-12 — Owner rulings on the deep-review deferred items (WI-078…082 filed; Links.rtf archived)

**Session (owner-directed).** The owner ruled the four deep-review deferred
items ([archive/repo-review-2026-07-12.md](archive/repo-review-2026-07-12.md)
§1/§3) and directed `Links.rtf` to the archive. The rulings are now first-class
backlog rows (the WI-054 idiom — `deferred` WIs, not prose bullets), so
status.md Open items no longer carries a pending-decision block for the review.

**Rulings.**
- **F5 census/bound + `[step:dupes]` (M6/M2) → WI-078.** Option (b): wire the
  detector over a `docs/dupes-allow` allowlist that **is** the census; reject
  the shared `_kitcommon.py` (it would break the per-script copy-readiness the
  kit sells, forcing downstream migration). `check_dupes.py` already carries the
  allowlist machinery (`--allowlist`, `read_allowlist`, line-number-free
  matching) — only the `stack.ini` step and the populated allowlist remain.
- **Archive-anchor comments (M7) → WI-079.** Strip the trailing
  `(REVIEW_*/THREAD_*)` provenance suffixes in `bootstrap.py`'s copy path —
  provenance stays in the meta-repo, downstream gets the copy-ready comment (the
  suffix is redundant there since it can't resolve without `docs/archive/`).
  Accept-and-document is the recorded fallback if the transform isn't cheap.
- **`main()` decomposition (H1/M1/M5) → WI-080/081/082, campaign
  `main-decomposition`.** Approved: `agent_loop.py` first (WI-080),
  test-seams-first and behavior-preserving — the extraction *creates* the unit
  seams the ~500-line loop lacks today; `trace.py` follow-on (WI-081, soft
  `~WI-080`, `render_report` extraction, `parse_map` rename folds in);
  `bootstrap.py` left deferred **indefinitely** (WI-082, mild). Highest
  value/risk of the batch, sequenced after the owner sitting.
- **`Links.rtf` (L1) → archived.** `git mv Links.rtf docs/archive/`; the archive
  README gains a provenance-only row (not opened or converted — owner content).
  The root is live-only again.
- **AGENTS.template.md 22-byte headroom (L2).** No ruling — a mechanized
  tripwire (`byte-budget-guard`); dropped from the working surface.

**No spine change; nothing rides the pending G3 re-attestation** — backlog
filings + one archive move.

**Checks.** `check_trajectory.py --root . --strict` → clean (82 WIs, 71 done,
graph acyclic); `gen_trajectory.py --check` → up to date after regen (the When
view gains WI-078…082 + the `main-decomposition` container); `check_docs.py
--root . --stale` → OK, 0 broken links (the docs/test/report.md orphan +
README script-freshness hints are pre-existing). `pytest -q` → **639 passed,
1 skipped in 86.75s** (serial — this venv has no pytest-xdist; the declared
`-n auto` command applies wherever xdist is installed).

**Committed** as `74787c2` (single commit, owner-approved right after this
entry was written).

## 2026-07-12 — Reconcile the stale "Needs \<human>" items 3–5 (edge sweep · sibling-repo already-ruled · guardrails review)

**Session (owner-directed).** The owner asked to verify items 3–5 of status.md
"Needs \<human>" (suspecting drift), rule item 3, and run the item-5 review.
Findings confirmed the drift: item 4's ruling was already made and item 5 was
~90% covered by the 2026-07-12 deep review.

**Item 3 — WI-DAG soft-edge sweep (owner ruled "move with your recommendation").**
The hard/soft edge *policy* already ships
([process-options](../project-trajectory/PROCESS_OPTIONS.md) "Trajectory /
work-items", ~L1070: hard = real technical blocker; soft = advisory ordering),
so this was purely the deferred data pass (the "full 39-edge pass" from
THREAD_52_REVIEW F3, now 77 edges). Applied the test to the multi-predecessor
rows and demoted four edges to soft (`~`):
- **WI-032 ← ~WI-003** (trajectory-P3-docs ← byte-budget-discipline) — a
  standing constraint, not a build input. *High confidence.*
- **WI-074 ← ~WI-073** (campaign-column ← How-SW-containment) — reuses the
  `sw_containment` render *pattern*; independent code. *Owner's call, my lean.*
- **WI-047 ← ~WI-028** (enforcement-audit ← self-adoption-spine) — the real
  driver is the stdlib mechanization (WI-020, kept hard); the spine is context.
  *Owner's call, my lean.*
- **WI-048 ← ~WI-025** (subagent-gate ← parallel-tracks) — the gate rides the
  coordinator (WI-024, kept hard), not the parallel-lane model. *Owner's call.*
Instructive non-demotion: **WI-043**'s five-predecessor review-triage fan-in
*looks* narrative but stays **hard** — a review genuinely cannot complete before
the reviewed work exists (it *is* a real blocker). Single-predecessor chain
edges left hard (a full 77-edge audit is inert — every WI is done, so hard/soft
only affects dashboard rendering, never readiness). Soft edges now: 6
(`~WI-003/013/025/028/073/080`).

**Item 4 — sibling-repo ruling was already made.** INTEGRATION_PLAN.md header
(L6–8) records the enrichment as "owner-ruled to be done in
`TheColliny/FableClaudeMDForOpus`"; the ai-template side is done (WI-046). Only
external execution remains — reframed in status.md from a paused "Needs
\<human>" decision to an **External follow-up** pointer (tracked upstream, pulled
via `check_vendored.py`).

**Item 5 — focused PROCESS_OPTIONS review: clean, no findings.** The three
guardrails paragraphs the deep review only *sampled* — Tier-conditional
guardrails (L722), Enforcement audit (L807), Per-phase effort (L410) — read in
full: accurate, honest, internally consistent, and consistent with item 4 (the
vendoring section correctly lists no `JUDGMENT.md` in the upstream, matching the
still-pending Phase 2). The deep-review coverage + this pass close the batch
review.

**status.md reconciled.** "Needs \<human>" shrinks 5→2 (only G3 re-attestation +
the push ruling genuinely remain); the External-follow-up pointer added; Next
action trimmed. Forward-only preserved — the resolutions live here, not there.

**No spine change; nothing rides the pending G3 re-attestation.** Data + docs +
one dashboard regen.

**Checks.** `check_trajectory.py --root . --strict` → clean (82 WIs, 6 soft
edges, acyclic); `gen_trajectory.py --check` → up to date after regen;
`check_docs.py --root . --stale` → OK, 0 broken links; `pytest -q` → **639
passed, 1 skipped in 89.65s** (serial; no xdist in this venv).

## 2026-07-12 — WI-083: efficiency-package pointer (RDXmin) + adoption/re-sync emphasis

**Session (owner-directed).** After assessing `JayPokale/RDXmin` (a
token-efficiency agent tool), the owner directed a "see also" pointer emphasized
at adoption + re-sync. RDXmin's two mechanisms — a YAGNI output-ladder ruleset
and a `PostToolUse` scrub/elide/dedup tool-output compressor — are already
covered philosophically (the working agreement + the vendored guardrails
`EFFICIENCY` playbook) or out of kit scope (a runtime cost tool), so nothing was
imported; instead one pointer naming it as a separately-vendorable efficiency
package.

**Deliverable.** PROCESS_OPTIONS "Tier-conditional guardrails" gains a "related
opt-in — efficiency packages" note (RDXmin the worked example, orthogonal to the
guardrails core); ADOPTING §5 (first green run) + §6 (re-sync) gain "weigh the
opt-in layers" callouts pointing at it. Single-sourced (content in
PROCESS_OPTIONS; ADOPTING points) — no duplication. No spine change; nothing
rides the pending G3 re-attestation.

**Checks.** `check_trajectory --strict` clean (83 WIs, 72 done); `gen_okf
--check` up to date (the note is deep in PROCESS_OPTIONS, not its first-heading
summary, so the OKF process-guide is unchanged); `gen_trajectory --check` fresh
after regen; `check_docs --stale` OK, 0 broken links; `pytest -q` → **639
passed, 1 skipped in 89.10s**.

**Byte deltas.** Byte-budgeted files (`AGENTS.template.md`, `PROCESS.md`)
untouched — the additions land in the unbudgeted `PROCESS_OPTIONS.md` +
`ADOPTING.md`.

## 2026-07-12 — WI-084 (reviewer requirement-consistency sweep) + WI-085 (process-view spec filed)

**Session (owner-directed).** From the Ask-2 options menu the owner chose
**Option A only**, extended to cross-check historical items; and directed the
Ask-3 process view into a work item.

**WI-084 — Option A (done).** The embedded `REVIEWER_PROMPT` (`agent_loop.py`,
the SR-045 reviewer surface) gains a directed requirement-consistency sweep:
when a diff adds/changes SN/SR/TC rows, the reviewer cross-checks them against
the existing registries — the new rows **and** the historical rows they touch —
for contradiction / overlap / attribute-limit conflict, raising each as a finding
(MINOR "for clarity" where sharper SN/SR/TC wording would resolve an ambiguity,
per the owner's future-clarity goal). Operationalizes PROCESS.md §3's existing
statement that "§6 [the reviewer] is well-suited to a first-pass contradiction
sweep" within the existing reviewer capability — **no new SR, no PROCESS/SR text
change** (byte-budgeted files untouched); the critique prompt is untouched
(consistency is a review, not an artifact-quality, concern). Test:
`test_agent_loop_review.py::test_reviewer_prompt_carries_requirement_consistency_sweep`.

**WI-085 — process-view spec filed (deferred).** `docs/specs/WI-085.md` captures
the Ask-3 plan + owner rulings: a new Process tab in `PROJECT_STATE.html`
(artifact lifecycle × gates · the resume loop · slices→campaigns→gates); needs a
**new SR** (rides the re-attestation); generated if tenable, else a static
diagram whose **Critique** TC has an agent verify the diagram matches the real
process; bounded in-view duplication accepted where no single other doc states
the relationship. Predecessors WI-039/WI-070; campaign `process-view`.

**Checks.** ruff format+lint clean on the changed script/test; `check_trajectory
--strict` clean (85 WIs, 73 done); `gen_trajectory --check` fresh after regen;
`check_docs --stale` OK, 0 broken links (30 docs incl. the new spec); `pytest -q`
→ **640 passed, 1 skipped in 92.15s**.

## 2026-07-12 — GATE: G3 re-attestation (owner sign-off; bar green, spine all-mechanized)

**Gate action (`docs/gate-policy` = attended — the human owner is the acceptor).**
The owner re-attests **G3** over the accumulated spine changes that were awaiting
sign-off (status.md item 1): `SR-034` (Inspection→Analysis); added
`SR-039…043`; extended `SR-038` (OKF Knowledge-tab consumer + the How-SW
containment clarification) + `SR-042` Rationale consumer note; `SR-037` text
(SSOT coherence + SpecRef); `SN-023` + `SR-044` (declared-interface
connectivity); `SR-025` text (checked per-agent skill fan-out; +LLR-043/TC-045);
`SR-045` (S8 heterogeneous implementer/reviewer scheduling; +LLR-044/045/046 +
TC-046 + IF-044…047, extended by the pair-row registry slice); `SR-046` (run
capability menu; +LLR-047/TC-047); `SN-024` + `SR-047` (Critique verification /
critique loop; +LLR-048/TC-048); `SR-048` (How-SW top-view bound + containerized
render; +LLR-049/TC-049).

**Mechanized bar — RESULT: PASS.** `check.py --gate G3 --jobs 0`, all 13 steps:
format · lint · **tests+coverage 90.62 % (≥ 80), 641 passed** · traceability ·
privacy · doc-navigability · perf-budgets · design-flows · trajectory · arch-map
· trajectory-map · okf · skills-sync. `docs/gate` stays **G3** (a
re-attestation, not an advance).

**Verification basis (the trust footprint).** Of 48 `Verified` SRs, **48
mechanized** (Test/Demonstration/Manual/Analysis/Inspection) and **0 attested**
(`Attest`) — the spine rests entirely on runnable checks; nothing rides an
unverifiable human judgment (`docs/test/report.md` "Verification basis").

**Sign-off (§4 consistency review — the human half).** Owner **Peter Johnson**
attests the accumulated SR text changes and new SN/SRs are consistent with the
`PROJECT-VISION:` and with one another; the pending re-attestation is **closed**.
Housekeeping: the 5 stale "Rides the pending G3 re-attestation" notes
(`SR-037/045/046/047/048` Rationale) cleared; `docs/okf` + `PROJECT_STATE.html`
regenerated to match.

**Phased re-entry — opening the next increment.** New scope re-enters as a new
phase: the attested baseline is the implicit **v1** (blank `Phase` tag), new SRs
get `Phase=v2`, and `docs/gate` is **held at G3** — the recipe now spelled out in
PROCESS_OPTIONS "Phased delivery" (WI-086). status.md "Next action" routes a
resume session to draft the new requirement artifacts and **page the owner for
the G1 sign-off** before implementing (WI-085 first).

## 2026-07-12 — WI-087 filed (phase-aware hierarchical When/How views); gate-fallback design clarified

**Session (owner-directed).** Two owner topics.

**WI-087 (queued, phase v2).** Filed `docs/specs/WI-087.md` for tiered,
count-thresholded, click-to-explode ("Simulink-style") When and How views: When
tiers **phase → workstream → WI** (each collapsing above > 3), How tiers
**component → module** (> 3), parent edges inherited/aggregated from children
(the WI-073/WI-074 idiom generalized), and the delivery `Phase` surfaced on the
When view. Builds on campaign binning (WI-074) + component containment (WI-073).
Needs a new SR + owner G1 sign-off; the grouping composition (Phase vs Campaign
vs Workstream) and phase encoding are the open G1 questions. status.md's phase-v2
drafting now batches WI-085 + WI-087 for one owner sign-off.

**Gate-fallback question (design discussion, no change).** Clarified that "keep
confirmed items while new content reopens some" is achieved by **phasing +
per-item Status/`Attest`**, not by regressing `docs/gate` (the marker is CI's
enforcement bar; regressing it *un-enforces* the confirmed items — the opposite
of preserving them). Reopening a confirmed item a later phase affects = phase-tag
it (Verified-deferred while reworked), its prior `Attest` staying in the log as
history. Offered a complementary process note (the reopen-a-confirmed-item case)
+ a possible per-item attest-maturity enhancement, pending owner direction.

**Checks.** `check_trajectory --strict` clean (87 WIs); `gen_trajectory --check`
fresh after regen; `check_docs --stale` OK, 0 broken links.

## 2026-07-12 — WI-088: derived-gate-model DESIGN spec drafted (branch `derived-gate-model`)

**Session (owner-directed; branch `derived-gate-model`).** The owner directed a
**replacement** of the monolithic declared gate with a **derived** one, and a
design spec for it.

**Design.** `docs/specs/derived-gate-model.md`: the repo (and each phase) gate is
**derived** from artifact states, not the hand-set `docs/gate` line. Owner
constraints honored — (1) **hybrid**: a fast check script computes the gate and
caches it to `docs/gate` with a compute date (known on checkout; `--check` guards
rot); (2) **no new column**: reuse the open-vocab `Status` (prepend `Draft`:
Draft→Planned→Verified), ratification date git-derived; (3) SN maturity needs a
home (§4 open decision — section-as-state recommended). **Parallel** requirement
structuring per phase (G0→G2 as a batch, surfacing conflicts) then **series** dev
(G2→G3 per WI); phase **derived** from gate trajectory (backward movement revs
it); the pre-dev batch is a first-class `[phase]-[g*]` work item; ratification
becomes a Status-change-in-a-reviewed-commit (composes with
attended/single-ratify/autonomous). The **draft-exemption** from `trace.py`'s
orphan rule is the biggest change — and it retires the `-000`/off-spine
workaround. §10 breaks the campaign into 8 implementation WIs, filed **only after
the design is ratified**.

**Status.** WI-088 queued (campaign `derived-gate`), SpecRef the design doc;
awaiting owner ratification of the DESIGN at G1 before implementation. No code or
spine change yet — design + registration only.

**Checks.** `check_trajectory --strict` clean (88 WIs); `gen_trajectory --check`
fresh after regen; `check_docs --stale` OK, 0 broken links.

## 2026-07-12 — WI-088 RATIFIED: derived-gate design signed off; WI-089…096 filed

**Session (owner-directed; branch `derived-gate-model`).** The owner ratified the
derived-gate design — **this commit is the sign-off**, dogfooding the model's own
"ratification = a reviewed commit" rule. Final direction: the phase **anchoring**
method (the derived-gate *drop* is the detector; the committed `[phase]-[g*]` WI
is the anchor of identity + membership — pure git-history derivation is
rebase-sensitive and carries no membership).

**Recorded.** `docs/specs/derived-gate-model.md` → **RATIFIED** (its Ratification
section holds the four G1 decisions). WI-088 (design) closed **done**; the §10
implementation campaign filed as **WI-089…096** (campaign `derived-gate`, SpecRef
the design doc): WI-089 (queued) artifact-state model + `Draft`-exemption in
`trace.py` (the foundation); WI-090 SN maturity · WI-091 `derive_gate.py` ·
WI-092 check.py integration · WI-093 phase + `[phase]-[g*]` · WI-094 ratification
workflow · WI-095 process-doc rewrite · WI-096 migration + dogfood (deferred
behind WI-089). The campaign builds under today's monolithic gate; once it lands,
phase v3+ runs on the derived gate. No code change yet — ratification + registry.

**Checks.** `check_trajectory --strict` clean (96 WIs); `gen_trajectory --check`
fresh after regen; `check_docs --stale` OK, 0 broken links.

## 2026-07-12 — WI-089 (derived-gate campaign): the Draft artifact state + decomposition exemption

**Session (branch `derived-gate-model`).** First build slice of the derived-gate
campaign (spec §10.1) — the foundation the rest of the campaign needs. `trace.py`
gains a first-class `Draft` artifact state so a requirement can be **drafted in
the live spine before it is decomposed**, retiring the `-000`/off-spine
workaround.

**What changed (code + tests only — no spine/process change yet).**
- **`trace.py`** — new `is_draft(row)` keys on the open-vocab `Status` value
  `Draft`. The orphan pass exempts Draft rows from the **child-completeness**
  rules *only*: a Draft SR needs no LLR/TC, a Draft LLR needs no TC. Everything
  else still bites — a Draft SR still links an SN (parent linkage), ids stay
  unique/well-formed (integrity floor), and a Draft SR is skipped by
  `--require-verified` (it is pre-ratification, below G1, so it makes no Verified
  claim). Draft rows are surfaced **auditable**, not silent: a metrics-table
  count, a `## Draft artifacts (decomposition-exempt)` report section listing
  them, and a `drafts=N` stdout token. The module docstring's Orphan-rules block
  documents the exemption and points at the design spec.
- **Fixture migration.** Three existing test fixtures used `Status=Draft`
  *casually* to mean "an in-progress orphan" — which the new semantics would make
  green. Migrated so they still exercise what they test: `ORPHAN_SR` SR-002
  Draft→**Planned** (a genuine ratified orphan), `PHASED_SRS` SR-002
  Draft→**Implemented** (so `--require-verified` phase scoping is the axis under
  test). No behavior lost.
- **New tests** (`tests/test_trace.py`): a Draft SR exempt from decomposition
  (and flagged again once ratified to Planned); a Draft LLR exempt from the no-TC
  rule; a Draft SR exempt from `--require-verified`; a Draft SR still orphaning on
  a missing SN link and still failing the integrity floor on a malformed id.

**Judgment call — the exemption is scoped to child-completeness, not
parent-linkage.** The spec (§3) calls this "exempt from the *child-completeness*
rule." So a Draft SR must still link its SN (drafted alongside it in the
`[phase]-[g1]` batch); only the requirement to *have children yet* is lifted.
Draft SN maturity (section-as-state) is WI-090's job — `trace.py`'s SN scrape is
unchanged here, so a Draft SN's id still resolves an SR's SN-Ref.

**No re-attestation impact.** No SR/SN/LLR/TC rows added or changed; this is a
`trace.py` behavior addition (like adding a check), under today's monolithic
gate. The campaign's spine reconciliation is WI-096.

**Byte deltas.** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (58,297). No byte-budgeted file changed.

**Checks.** `pytest -q -n auto` **642 passed, 3 skipped**; `check_docs.py --root
. --stale` OK, 0 broken; trace self-run clean. Full `check.py --gate G3` runs at
campaign close (the campaign gate cadence, PROCESS_OPTIONS "Campaign ruling").

## 2026-07-12 — WI-090 (derived-gate campaign): SN maturity via section-as-state

**Session (branch `derived-gate-model`).** Second build slice (spec §10.2, the §4a
decision): stakeholder needs get a maturity state without a new column —
**section-as-state**. A stakeholder-needs.md heading whose text contains `draft`
(e.g. `## Draft needs (unratified)`) marks the SNs under it **Draft** (unratified,
G0); SNs under any other heading are **Ratified** (G1). Ratifying = moving a
need's row up into *Core needs* / *Edge-case expectations* in a reviewed commit
(git-derived date). The SN analogue of the `Status=Draft` bit on SR/LLR/TC rows.

**What changed (code + template + tests — no spine change).**
- **`trace.py`** — `sn_draft_ids(text)` line-scans headings and returns the SN
  ids under any `draft` heading (`-000` excluded). Draft SNs are exempt from the
  `SN with no SR` orphan rule, join the `drafts=N` count + the `## Draft
  artifacts` report section, and render with the draft class in the outline/DAG
  (`build_forest`/`mermaid_graph` gained a default-empty `sn_draft` param — a
  legacy caller is byte-identical).
- **`check_docs.py`** — `_registry_needs` exempts draft-section SNs from the
  Must/Should README-coverage floor (existence still holds), so a *drafted* Must
  need doesn't force a README bullet before it is ratified.
- **`stakeholder-needs.template.md`** — a "Maturity is section-as-state" note + a
  `## Draft needs (unratified)` section. A fresh scaffold stays vacuous (no SN ids
  under the draft heading).

**Judgment call — heading-text match on the single word "draft".** The rule is
deliberately loose (any heading containing "draft", case-insensitive) so
`## Draft needs`, `## Draft (unratified)`, `## DRAFT items` all work, and the
top-level `# Stakeholder Needs` / `## Core needs` / `## Edge-case expectations`
headings never match. Body prose containing "draft" is not a heading, so it never
flips the section state.

**No re-attestation impact.** No SR/SN/LLR/TC rows added or changed (the meta's
own needs are all ratified — no draft section); this is reader + template
behavior under today's monolithic gate.

**Byte deltas.** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (58,297). No byte-budgeted file changed.

**Checks.** `pytest -q -n auto` **646 passed, 3 skipped**; `check_docs.py --root
. --stale` OK, 0 broken; trace self-run clean.

## 2026-07-12 — WI-091 (derived-gate campaign): derive_gate.py — the hybrid, cached derived gate

**Session (branch `derived-gate-model`).** The campaign core (spec §5): a new
`scripts/derive_gate.py` computes the active gate from the spine's own maturity
states instead of a hand-set marker. **The repo is at gate G iff every in-scope
SN/SR/LLR/TC meets G's bar.** Stdlib, self-contained (small loaders duplicated
from trace.py per the F5 rule — it never imports the joined-spine engine).

**Per-artifact gate (§3), with one reconciliation to trace's actual bar.**
- **SR** — Draft→G0; ratified-but-undecomposed→G1; decomposed (its LLR — unless
  LLR-exempt Analysis/Inspection/Attest — plus a TC)→G2; decomposed +
  Status=Verified→G3.
- **LLR/TC** — Draft→G0 (the new-phase signal). **Reconciliation:** once present,
  an LLR/TC's own Status does *not* independently gate — the SR's Verified status
  drives G2→G3, matching `trace.py --require-verified` (which checks SRs, not
  LLR/TC status). The spec §3 sketch had "LLR present⇒G2, Verified⇒G3"; taken
  literally that caps any repo whose LLRs read `Implemented` (the kit's own
  minimal-project fixture, and typical downstream) at G2 even though trace calls
  it G3. So a present LLR/TC contributes G3 and never caps; its *existence* is
  what makes its SR decomposed (decided in sr_gate). This keeps derived == trace's
  G3 for **any** G3 repo, not just the meta.
- **SN** — Draft (section-as-state)→G0; ratified never caps (contributes G3).

**Aggregation.** Repo gate = min over all in-scope artifacts; a repo with no real
SRs is G1 (never a vacuous G3). A draft/reopen drops the min to G0 → the runnable
value floors to G1 with the raw G0 recorded in the basis (the new-phase-pending
signal; the phase detector + `[phase]-[g*]` archetype are WI-093). Per-phase
breakdown reported.

**Hybrid cache.** Writes `docs/gate` as a generated file: a static header, a
compared `# basis:` line (counts + raw level + per-phase), an informational
git-derived compute stamp (never compared — the arch-map/trajectory as-of idiom),
then the runnable value as the first non-comment line — so `check.py`'s
`resolve_gate()` reads it unchanged. `--check` recomputes and guards rot; a
**legacy** hand-set gate (no `# basis:` line) is compared value-only, so the meta
and fresh scaffolds stay green until the one-time migration (WI-096). `--print`
computes without writing. `bootstrap.py` MAPPING ships it downstream.

**Meta dogfood (proven early).** `derive_gate.py --print` on the meta reads **G3**
(SN=24 SR=48 LLR=49 TC=49 drafts=0), byte-matching today's declared `docs/gate`.
The meta's `docs/gate` is NOT migrated yet (that's WI-096); it stays the legacy
hand-set `G3`, which `--check` accepts value-only.

**Interim connectivity warn (resolved in WI-096).** derive_gate.py is a new
arch-map module with no IF-### row yet (its SR + interface rows are the WI-096
spine reconciliation), so `check_trajectory` emits **one warn-only** "connectivity
undeclared: module 'scripts/derive_gate'…". Never fails the exit code (interface
coverage is warn-first at every gate); `check_trajectory --strict` stays clean.

**No re-attestation impact.** No SR/SN/LLR/TC rows added or changed; a new script
+ tests under today's monolithic gate. check.py wiring is WI-092.

**Byte deltas.** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (58,297). No byte-budgeted file changed.

**Checks.** `pytest -q -n auto` **658 passed, 3 skipped**; `check_docs.py --root
. --stale` OK, 0 broken; `check_trajectory --strict` clean (1 warn-only
connectivity note); arch-map + dashboard regenerated fresh.

## 2026-07-12 — SPINE CHANGE (WI-092, derived-gate campaign): check.py consumes the derived gate; SR-049 added; RE-ATTESTATION rides the campaign

**Session (branch `derived-gate-model`).** `check.py` now consumes the derived
gate (spec §5/§10.4), and — to keep the meta's own dogfood green — `derive_gate.py`
is traced into the meta spine.

**check.py integration (the light part).** `resolve_gate()` reads `docs/gate`'s
first non-comment line **unchanged** — the value is simply *derived* by
`derive_gate.py` now (it sits on that same line, with the `# basis:` derivation in
comments above), so no read change was needed; the docstring records the shift. A
new **`derived-gate`** process step (`derive_gate.py --check`) runs at **every gate
G1/G2/G3** (the gate value is check.py's own input, so its cache must be fresh
whenever check.py runs) and joins the **pre-commit** batched freshness floor
(`--run-steps …,derived-gate,…`; the shipped `project-trajectory/hooks/pre-commit`,
which the meta's thin `.githooks/pre-commit` wrapper delegates to). A **legacy**
hand-set gate (no `# basis:` line) is compared value-only, so the meta + fresh
scaffolds stay green until WI-096 migrates. `conftest.make_minimal_project`
regenerates `docs/gate` via derive_gate (a full G3 chain advances the derived gate
off the scaffolded G1).

**Spine change (deviation — pulled forward from WI-096).** Adding `derive_gate.py`
as a *traced product script* means the meta's own invariants (every arch-map
module contained in a component; every module a declared IF endpoint — WI-073 /
WI-057) go **red** the moment the module enters the arch-map, and one of them
(`component_top_view` uncontained == []) is a hard **test** (`test_gen_trajectory
::test_meta_component_top_view_smoke`), not just a warn. So the meta-spine tracing
of derive_gate could not wait for WI-096 without leaving the meta's own suite red
for four commits. Traced now:
- **SR-049** (derived gate from artifact states; SN-004 mechanical-gate + SN-008
  honest-gate; Test/Verified) + **LLR-050** (Module `…/derive_gate.py`, Component
  **CMP-001** Traceability core, alongside trace/check/check_trajectory) + **TC-050**
  (`tests/test_derive_gate.py`).
- **IF-050** Provides `derive_gate → check` (the `docs/gate` marker) + **IF-051**
  Consumes `derive_gate ← system-requirements.csv` (the states) + the `Contracts:
  IF-050, IF-051` docstring line. derive_gate is now contained **and** a declared
  endpoint: `trace --strict …` → interfaces=51 interface-findings=0, 0 orphans; the
  interim connectivity warn is gone.

What stays for **WI-096**: regenerate the meta's own `docs/gate` to the derived
form (basis line), prove derived == declared G3 byte-for-byte, and the ADOPTING
migration recipe.

**RE-ATTESTATION.** SR-049 is a new Verified Test SR on the ratified spine, so it
**rides a pending G3 re-attestation** at campaign close (still all-mechanized: 46
Test · 2 Analysis · 1 Inspection · 0 Attest). Recorded as the campaign's
re-attestation rider in `docs/status.md`.

**Meta spine:** SN=24 **SR=49 LLR=50 TC=50**, 0 orphans / integrity / schema /
status findings; **51** IF seams, interface-findings=0; 24 modules → 5 components,
0 uncontained.

**Byte deltas.** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (58,297). No byte-budgeted file changed.

**Checks.** `pytest -q -n auto` **659 passed, 3 skipped**; `check_docs.py --root .
--stale` OK, 0 broken; `check_trajectory --strict` clean (0 connectivity warns);
`derive_gate --check` value-OK (G3, legacy — WI-096 migrates); arch-map + OKF +
dashboard regenerated fresh.

## 2026-07-12 — WI-093 (derived-gate campaign): the [phase]-[g*] archetype + phase-drop detector

**Session (branch `derived-gate-model`).** `check_trajectory.py` learns the phase
archetype (spec §7/§9.3). No spine change — validator + reader behavior only.

- **Archetype.** A phase's pre-dev batch is a first-class WI whose **Title**
  carries a `[<phase>]-[g<N>]` tag (`[v2]-[g1]` = requirement structuring,
  `[v2]-[g2]` = decomposition + TCs). `phase_anchors()` parses them from Titles
  and warns on a **duplicate** `(phase, gate)` and on a `-g2` anchor that omits its
  `-g1` as a predecessor. The WI id stays `WI-###`; the archetype is a Title
  marker, so nothing in the id scheme changes.
- **Phase-drop detector (§9.3).** `read_derived_phases()` parses the per-phase
  levels from `docs/gate`'s `# basis:` line — the **hybrid cache** (no recompute;
  a shared format contract with `derive_gate.basis_line`). For each phase with a
  **done** `[phase]-[gN]` anchor (its recorded closed level), if the current
  derived level fell **below** N — new or reopened content entered — it warns to
  **open a new phase-gate WI**. The committed anchor is where phase identity +
  membership live (a git-history walk is rebase-sensitive and carries no
  membership, §9.3).
- **All WARN-FIRST** — never an exit-code change at any gate (the
  connectivity-coverage precedent). **Vacuous** on a single-phase repo with no
  anchors (the meta) or a legacy `docs/gate` with no basis line. So the meta's own
  `check_trajectory --strict` stays clean, 0 new warns.
- **`derive_gate._per_phase` now reports the RAW per-phase min** (unfloored, can
  read `G0`), so a phase's drop below G1 is visible in the cached basis for the
  detector to read. The runnable repo value stays floored to G1 (unchanged).

**No re-attestation impact.** No SN/SR/LLR/TC rows added or changed.

**Byte deltas.** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (58,297). No byte-budgeted file changed.

**Checks.** `pytest -q -n auto` **664 passed, 3 skipped**; `check_docs.py --root .
--stale` OK, 0 broken; `check_trajectory --strict` clean (0 phase/connectivity
warns on the meta); arch-map + dashboard regenerated fresh.

## 2026-07-12 — WI-094 (derived-gate campaign): ratification = a reviewed Status-change commit

**Session (branch `derived-gate-model`).** Docs/skill only (spec §6/§10.6). The
human no longer bumps a gate line — they **ratify a batch of artifacts in a
reviewed commit**, and the gate derives from it.

- **`gate-advance` skill** — the "active-gate mechanism" section rewritten:
  `docs/gate` is **generated** by `derive_gate.py` (computed from artifact
  states), regenerated after a ratification, freshness-guarded by the
  `derived-gate` step. A new **"Ratification = a reviewed Status-change commit"**
  section: mark a batch ratified (`Draft`→`Planned` on the SR, or move an SN out
  of the `## Draft needs` section) and that commit *is* the sign-off; it composes
  with the gate-authority levels (`attended` = each batch; `single-ratify` = once
  at the phase `[g2]` close; `autonomous` = a fresh-context reviewer's verdict),
  and an agent may make the ratifying commit governed by the level. "Sync before
  you bump" → "Sync before you **ratify**".
- **`gate-policy.template` + the meta `docs/gate-policy`** — comment rewritten:
  gates are derived, the level governs **who makes the ratifying commit**, and the
  policy value itself stays hand-set (`docs/gate` is generated, never hand-edited).
- **Skill fan-out** — the source skill edit was re-synced byte-identical to
  `.claude`/`.agents` (`bootstrap.py --sync`, 2 files refreshed) and
  `skills/INDEX.csv` regenerated (the frontmatter description changed).
  `gen_skills_index --check-agents` clean (10 copies match).

**No spine change, no re-attestation impact.** No SN/SR/LLR/TC rows touched.

**Byte deltas.** `AGENTS.template.md` **untouched** (9,978); `PROCESS.md`
**untouched** (58,297). No byte-budgeted file changed (PROCESS.md §4/§7 rewrite is
WI-095).

**Checks.** `pytest -q -n auto` **664 passed, 3 skipped**; `check_docs.py --root .
--stale` OK, 0 broken; `gen_skills_index --check-agents` clean.
