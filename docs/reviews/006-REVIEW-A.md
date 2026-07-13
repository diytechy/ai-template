# REVIEW-A — session 006 (independent) — WI-085 close (Process reference tab / SR-050)

Scope: `481e374..a411062` on `derived-gate-model` — the BUILD that shipped the
Process tab in `PROJECT_STATE.html` (`gen_trajectory.process_panel`), plus the
bookkeeping commit `b609a0d` (iteration logs 001–003 + index + scoreboard, no
product surface). Reviewed the diff against AGENTS/PROCESS, the spine registries,
and the spec-of-record `docs/archive/specs/WI-085.2026-07-12.md`.

## Harness — run independently, real output

- `python project-trajectory/scripts/check.py --gate G3 --phase v1 --jobs 0`
  → **RESULT: PASS** — 14/14 steps green; `678 passed, 3 skipped` in 160.75s;
  coverage **91.11%** (floor 80). derived-gate, traceability, trajectory-map,
  arch-map, okf, skills-sync all PASS.
- `python project-trajectory/scripts/trace.py --root .`
  → `SN=24 SR=51 LLR=52 TC=52 orphans=0 integrity=0 components=5
  component-findings=0 interfaces=52 interface-findings=0` — IF-052 coheres.
- `python project-trajectory/scripts/derive_gate.py --check` → up to date (G2),
  exit 0 — the state changes (SR-050→Verified, LLR-051→Implemented, TC-051→
  Verified) do not move the computed gate (v2 floor held by SR-051 Planned).
- `pytest tests/test_gen_trajectory.py -k process` → 8 passed. All 7 node paths
  pinned in TC-051 exist and assert real behavior (three-panel live-data join,
  gate-flip highlight, link-out preference, campaign-stats join, gate-less
  byte-identical round-trip, `--check` trips on a gate flip, meta smoke proving
  every link-out resolves). The Verified TC is honest.

The work is well-decomposed, deterministic, and genuinely tested; no correctness
defect found. Three non-blocking MINOR items follow (two clarity, one hygiene).

## Findings

- [MINOR] docs/requirements/system-requirements.csv:51 -> SR-050's Requirement prose promises panel 1 shows "each stage linked to its process-doc section", but the delivered render (gen_trajectory.py:2033-2036) emits a single caption-level link to `process.md` naming §3/§4 in prose — the stage `<li>` chips carry no per-stage anchors. The testable AcceptanceCriteria only asks that "process-doc links resolve" (met), so the Verified status is honest; the prose overstates the render. -> Either soften SR-050's clause to "the panel links to the process-doc sections (§3 tiers, §4 gates)" or add per-stage section anchors; this scope trim was not noted in the commit's Deviation line. -> @owner
- [MINOR] docs/requirements/low-level-requirements.csv:52 -> LLR-051 is left at Status=Implemented while all 50 other closed LLRs — including same-batch LLR-050 — read Verified, and its TC-051 and SR-050 are both Verified. maturity_gate() treats any non-Draft LLR as G3, so this is cosmetic to the derived gate, but it reads as an odd-one-out "not fully done" row to any human scanning the registry. -> Set LLR-051 Status=Verified for registry-convention consistency (or state why this batch's LLR terminal state is Implemented). -> @owner
- [MINOR] project-trajectory/scripts/gen_trajectory.py:2027 -> The panel shows a single "Current gate: <b>G2</b>" read from the first non-comment line of docs/gate, but the derived model is per-phase (`per-phase=(default)=G3;v2=G2`). On this very meta-repo the default phase is G3, so the dashboard tells a viewer "G2" while the main body is at G3 — the runnable floor, honestly labeled, but the per-phase reality is not surfaced. SR-050 only specced a single docs/gate highlight, so the impl is faithful to the SR; this is a spec-level clarity gap. -> Consider surfacing the per-phase breakdown (or a "runnable floor" qualifier) in the gnow banner, or note in SR-050 that the highlight is the floor gate only. -> @owner

VERDICT: APPROVE findings=3
