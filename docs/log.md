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
[specs/capability-expansion.md](specs/capability-expansion.md), C1).

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
