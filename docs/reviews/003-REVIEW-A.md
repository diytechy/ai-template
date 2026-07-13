# 003 — REVIEW-A (independent)

Work under review: iteration 001 BUILD, commits `6ae82d9..28dc890` — the phase-v2
pre-dev batch **WI-116** (`[v2]-[g1]` draft + ratify SR-050/SR-051 Draft→Planned),
**WI-117** (`[v2]-[g2]` decompose to LLR-051/052 + TC-051/052, v2→G2) and its
follow-up, and **WI-118** (test-suite hermeticity: scrub inherited `AGENT_*`
routing env). Requirement surface: `docs/specs/WI-085.md`, `docs/specs/WI-087.md`,
`docs/specs/derived-gate-model.md`, and the SN/SR/LLR/TC + work-items registries.
(Iteration 002 REVIEW-A `gpt-5.6-terra` errored; this is the retry.)

## Harness (run and observed, not trusted)

- `trace.py --root .` → `SN=24 SR=51 LLR=52 TC=52 orphans=0 integrity=0 components=5
  component-findings=0 interfaces=51 interface-findings=0`.
- `check.py` (derived gate **G2**) → `RESULT: PASS` (all 6 steps green).
- `derive_gate.py --check --root .` → `docs/gate up to date (G2)`, exit 0; `--print`
  → `per-phase=(default)=G3;v2=G2`.
- `gen_okf.py --check --root .` → `OKF bundle up to date (241 files)` (the SN-010.md /
  SN-021.md OKF changes are legitimate child-ref regenerations).
- `python -m pytest -q -n auto` → **671 passed, 3 skipped**.
- WI-118 verified load-bearing: with ambient `AGENT_TIER_MAP=BUILD=strong` /
  `AGENT_CMD` / `AGENT_MODEL_MAP` exported, `tests/test_agent_loop.py` → 41 passed
  (the conftest scrub neutralizes the contamination the WI describes).
- Investigated the `docs/gate` `as-of 55eb4b5` vs `LLR=52` mismatch: benign — the
  as-of is `git rev-parse HEAD` at cache-write (one commit behind the commit that
  carries the staged spine change), and `--check` compares only the basis counts +
  gate value, not the as-of. Not a defect.

## Findings

- [MINOR] docs/requirements/system-requirements.csv:52 (SR-051, for clarity) -> SR-051 triggers the containerized How-SW view on ">3 top-level components", a different trigger than the *Verified* SR-048/TC-049 which containerize "whenever CMP rows contain modules" (vacuous ≤10 modules); for a repo with ≤3 components but >10 CMP-contained modules the two disagree (SR-048 → containerized, SR-051 → flat), so implementing SR-051 as worded at WI-087 could regress Verified TC-049 — LLR-052's "TOP_VIEW_MAX unchanged" preserves the item cap but not the containerize trigger -> add a composition clause to SR-051 (mirror in LLR-052/TC-052) stating that CMP-containment containerization still governs when components ≤3 (TC-049 holds) and the ">3" rule only adds the start-collapsed component tier above it -> @owner

VERDICT: APPROVE findings=1
