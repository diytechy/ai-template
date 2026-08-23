+++
id = "WI-419"
title = "Stakeholder-need cleanup (owner-directed, 2026-08-07): (1) SN-011 stated 'no pip installs', which had drifted from the standing owner ruling RULING-3 (2026-07-28, docs/dependencies.md) that the bar is 'no UNARGUED dependencies' - the absolute ban is itself a design constraint that can force a worse hand-rolled alternative than a well-chosen tool, so restate the need as stdlib-by-default plus ledger-argued dependencies, keeping shipped-tier checks stdlib-PREFERRED. (2) SN-025 read as a spec, not a need: one row carried the single-command autonomy claim AND the parallel-fan-out/serialized-integration claim, so 13 live SRs hung off a need whose headline no reader could hold. Split it - SN-025 keeps the single-command, no-human-curation autonomy need; a new SN-027 carries throughput (bounded parallel lanes) with mutation of the integration branch serialized and gated. (3) NO need existed for multi-family LLM configuration at all: SR-079/080/083/084 (pair-row routing, managed review scheduling, planner-pair selection, family-heterogeneous critique) are all Verified and all cited SN-006/SN-016/SN-024, none of which mention model families or capability levels - the docs/agents.csv (family x model x tier) registry, docs/agents-enabled consent surface and docs/review-policy dial were a whole configured subsystem with no stakeholder need behind them. Mint SN-026 and re-anchor those four rows onto it."
specref = ""
workstream = "requirements"
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

Landed on the trunk lane as one owner-directed amendment batch. **This opens an
attestation window: 20 SRs now read `Modified` and the derived gate dropped
G3 -> G2** (`docs/gate` basis: `SN=27 SR=136 LLR=137 TC=134 drafts=0
modified=20 uncovered=0 computed=G2 ex-draft=G2 per-phase=1=G2;2=G3;3=G3;4=G2`).
That drop is the machinery working as designed, not a regression: an SN has no
`Status` cell, so a changed ratified need rides its SR chain's `Modified`
(process.md section 4), and the window closes with one reviewed Status-change
sitting.

**Needs (`docs/requirements/stakeholder-needs.md`)**

- **SN-011 amended** — "clean Python 3.11+ with **no pip installs**" became
  "clean Python 3.11+ with **minimal, argued dependencies**": stdlib by default,
  a non-stdlib dependency admitted only through a reviewed `docs/dependencies.md`
  row. Acceptance intent now names the real enforcer
  (`tests/test_dependency_ledger.py` fails on an undeclared import) and preserves
  the `shipped`-tier stdlib-*preferred* bar, since a dependency there forces
  every adopter to install it. Closes a prose-vs-ruling drift that had stood
  since 2026-07-28.
- **SN-025 rewritten (narrowed)** — now only the single-command claim: one
  command from the repo root lets a configured agent implement toward the vision,
  fully autonomously where enabled, with no human curating what comes next.
- **SN-026 minted** — several LLM families configurable, selected **per job and
  per capability level**, with an automatic cross-family draw for work that
  benefits from an independent second opinion. Acceptance intent cites
  `docs/agents.csv`, `docs/agents-enabled` and the documented degraded
  same-family mode.
- **SN-027 minted** — throughput: ready work fans out across bounded parallel
  lanes while mutation of the integration branch stays serialized and gated
  behind one fail-closed integrator.

**Requirements (`docs/requirements/system-requirements.csv`) — 20 rows `Modified`**

- SN-011 chain: SR-034, SR-035, SR-114. SR-034 additionally **reworded** (title,
  requirement, rationale, acceptance) from "Scripts are stdlib-only" to the
  ledger model; the first draft carried two `shall`s and trace.py's requirement-form
  check caught it, so the shipped-tier clause moved into AcceptanceCriteria where
  it belongs.
- Re-anchored onto **SN-027**: SR-093, SR-094, SR-130, SR-131, SR-132, SR-133,
  SR-134, SR-135. SR-057 cites both (it derives the frontier *and* feeds the
  fan-out).
- Kept on **SN-025**: SR-057, SR-059, SR-060, SR-115, SR-116 — the
  no-hand-curated-pointer half.
- Re-anchored onto **SN-026**: SR-079, SR-080, SR-083, SR-084 (Rationale cells
  updated to match their new SN-Refs, so the two never disagree).
- Superseded rows still citing SN-025 were left untouched: they are historical
  and are not re-attested.

**README** — the SN-011 bullet no longer claims "no pip needed"; SN-025's bullet
became the one-command/no-pointer claim; the parallel bullet re-cites SN-027; the
heterogeneous-scheduling bullet now leads with SN-026 and names the per-job /
per-level selection. `check_docs` reports **0 README findings**, so the
Must/Should citation floor holds for all 27 needs.

**Generated artifacts** — regenerated in `REGEN_STEPS` dependency order via
`trunk_step.py --regen` (arch-map, okf, derived-gate, trajectory, status,
open-items); two new OKF concept files appeared for SN-026/SN-027.

## Evidence

- `trace.py --strict --strict-integrity`: `SN=27 SR=136 LLR=137 TC=134
  orphans=0 integrity=0 verified-mechanized=89 verified-demonstrated=27
  components=5 component-findings=0 interfaces=91 interface-findings=0
  form-findings=0` (exit 0).
  <!-- fig: python3 project-trajectory/scripts/trace.py --root . --strict --strict-integrity @ WI-419 -->
- `pytest -q -n auto -m smoke`: **667 passed, 2 skipped in 13.65s**.
  <!-- fig: python3 -m pytest -q -n auto -m smoke @ WI-419 -->
- Full unfiltered suite (this touches the spine, so the slice bar is the full
  one): **1966 passed, 5 skipped in 339.32s**.
  <!-- fig: python3 -m pytest -q -n auto @ WI-419 -->
- `check_trajectory.py --root . --strict`: exit 0.
  <!-- fig: python3 project-trajectory/scripts/check_trajectory.py --root . --strict @ WI-419 -->
- `check_docs.py` at the **declared commit bar** (`--ignore docs/test/report.md
  --ignore "docs/work/*" --stale`): **`OK — 376 doc(s), 1040 intra-repo link(s),
  0 broken`**, and **0 README findings**, so the Must/Should citation floor holds
  for all 27 needs.
  <!-- fig: python3 project-trajectory/scripts/check_docs.py --root . --ignore docs/test/report.md --ignore "docs/work/*" --stale @ WI-419 -->
  Run bare (without the declared ignores) it reports 4 broken links + 409 orphans;
  all four are in `docs/work/complete/` and are pre-existing — byte-identical on a
  stashed baseline of this branch — so they are not this WI's and were not fixed
  inline.

## Deviations from spec

- **TC-034's enforcer is now stricter than SR-034.** `tests/test_stdlib_only.py`
  asserts *pure* stdlib; the amended SR-034 permits ledger-declared imports.
  Nothing is red today (no `Kind=python` row exists yet), but the day one is
  admitted the test false-reds. Not retargeted here — that is a code change
  outside an SN-cleanup scope, and doing it silently would hide the choice.
  Filed as **WI-420**.
- Superseded SR rows citing SN-025 were not re-pointed (see above).
