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
| G1 — Requirements/UX/Constraints | MET 2026-07-07 | MET 2026-07-07 | MET 2026-07-07 | n/a | PENDING (attended) |
| G2 — Decomposition & Test Coverage | n/a | n/a | MET 2026-07-07 | MET 2026-07-07 | PENDING (attended) |
| G3 — Implementation | n/a | n/a | PENDING | PENDING | PENDING |

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
