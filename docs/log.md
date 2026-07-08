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
