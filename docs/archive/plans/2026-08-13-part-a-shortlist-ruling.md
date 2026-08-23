> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# Part A — the ranked shortlist and the provisional ruling (WI-441)

Coordinator record, 2026-08-13, under the owner's confirmed execution mode for
the absence: the top candidate is **provisionally adopted warn-first** (safe:
`LLR.Component` is a traced cell, so no re-attest window opens), and this
document is the package the owner ratifies — or overturns — at return. The
measured inputs live in [2026-08-13-part-a-data-pack.md](2026-08-13-part-a-data-pack.md)
(every figure reproducible; derivation scripts in its Appendix A). The ruling
being executed is OI-14 (A3 + A6), 2026-08-13.

## The ranking

| Rank | Candidate | Why it places here |
|---|---|---|
| **1 — ADOPTED (provisional)** | **P5 narrow-waist** (4 components: W1 Registry & conformance · W2 Gatekeeper · W3 Autonomy · W4 Human & adopter surfaces) | Best on the PRIMARY constraint: lowest behaviour straddle (7/12) and the only candidate that single-homes B3 (`value_to_cell`), B4 (gate policy), B9 (carrier vocabulary) and B12 (`_norm_module`). Best boundary count (4) at a cut (31) statistically tied with the best (30). Zero new interface rows owed. Same 8-module rework as the runner-up. It is also the shape closest to the Core adopter's ratified answer — the strongest external evidence the OI-14 brief names. |
| 2 — runner-up | P3 actor-boundary (5 components) | Lowest raw cut (30) and near-zero new interface work — but its components are AUDIENCE distinctions, and Parnas asks what CHANGES together; a dashboard and a decision brief may not. Straddles 10/12. If the owner overturns P5, this is the candidate to reach for. |
| 3 | P4 functional (9 components) | Most faithful to the pure method; second-best straddle (9/12) — but 15 interface rows that do not exist today must be written before its checks are honest, and its F7 work-flow cluster at 22 crossings says that grouping is not one component. The right shape for a LATER depth-1 recursion, not for depth 0. |
| 4 | P1 minimal-change (today's 5, multi-tags narrowed) | The honest floor: zero modules move, and it deletes the fail-open (no endpoint stays multi-tagged). But it ratifies the accident A1 was refuted for and straddles 10/12. Its value was making every other candidate justify its rework — P5 beats it on every structural measure for 8 moved modules. |
| 5 | P2 shared-kernel | The measured TRAP, ranked last on purpose: extracting the shared services without deleting the duplicated copies makes everything worse (cut 33→48, straddle 10→11, a 31-crossing hub). Kept in the record because it is the move a reader reaches for first. |

## What P5's adoption means concretely (the rework list, sized)

- **8 modules re-home:** `check`, `check_privacy`, `gen_arch_map`,
  `migrate_carrier`, `prompts`, `run_menu`, `subagent_gate`, `wi_convert`;
  the 5 multi-tagged modules (`bootstrap`, `agent_common`, `agent_session`,
  `derive_gate`, `handback`) each narrow to ONE component.
- **New component identities are minted, not re-pointed:** CMP-006 (W1),
  CMP-007 (W2), CMP-008 (W3), CMP-009 (W4); CMP-001..005 retire under D-4
  (ids never re-meaning). All 149 `LLR.Component` cells re-tag — traced cells,
  no re-attest.
- **31 cross-component seams owed an IF row — all 31 exist today.** Zero new
  rows for the internal cut; the 19 MISSING rows are boundary crossings
  (section 1b of the data pack) and land as Draft rows with WI-442/443.
- **W1 is deliberately coarse** (9 modules, 26 crossings). That is not a
  defect to fix now: under the OI-21 ladder, architecture RECURSES — W1 is the
  first candidate for a depth-1 partition at the scheduled RE-SCORE, which the
  A3 ruling already carries as its loop. P4's F1/F2 split is the natural seed
  for that recursion.

## The constraint finding the owner must see (it reshapes nothing, but it is
## the deepest fact the derivation produced)

**One-home-per-behaviour is unsatisfiable by ANY partition of today's tree**:
the 12 duplicated behaviours live as 39 (behaviour, home) pairs across 16
modules, so the copies — not the boundaries — are the violation. The partition
ADOPTS the owning home; the D-8 common-module program (WI-448, inversion
confirmed 2026-08-13) is what DELETES the copies. The pack flagged an apparent
contradiction with the D-7-era F5 ruling ("duplicated plumbing accepted
unbounded; shared `_kitcommon` rejected"): resolved by recency — D-8
(2026-08-12, step 2 inverted 2026-08-13) supersedes that acceptance, and P2's
measurement is the proof the two must land together (extraction without
deletion makes every number worse).

Two NEW unpinned divergent behaviours surfaced by the census — **B10**
(`plan_coverage.split_refs` splits on `[;,]` while five sibling homes split on
`[;,\s]+`, demonstrably diverging on whitespace input, same class as the
SN-001/SN-002 orphan bug) and **B11** (`load_csv` `errors=` divergence) — are
WI-448 intake, and B10 wants a `test_rule_sync` pin NOW rather than at the
program (it is live and divergent, not live and pinned).

## `SR.Area` — the explicit verdict (provisional)

**Neither pure option survives the measurement.** 25 of 31 values are a
component by another name (derivable → redundant); the 6 spanning values carry
65 of 147 SRs and are ASPECTS — cross-cutting concerns a partition structurally
cannot express — so "derive from Component" deletes information and "retire
outright" deletes the only grouping of SR-137..146. The provisional verdict,
for the owner to ratify:

- `Area` as a 31-value free-text authored column **retires**;
- the six spanning values convert to a small **closed aspect vocabulary**
  (`process`, `trajectory`, `unattended-loop`, `connectivity`, `perf`,
  `portability`), validated by the Part B schema tier — an aspect is a REVIEW
  grouping, not an ownership claim, which is also cleanly compatible with the
  OI-19 hats axis;
- the 25 derivable values are dropped at conversion (the component already
  carries the fact);
- **Portability's homelessness is not a defect**: its 3 SRs are depth-0
  system-level obligations discharged by every module — under the OI-21 ladder
  the system IS the depth-0 component, and that is their honest home.

## Two vacuous-zero corrections Part B inherits (measured here, fixed there)

- The containment rule does **NOT** cover the 45 IF rows
  `cross_component_findings` is vacuous for — their untagged endpoints are
  data files, external actors and directories, never arch-map modules, so
  **they are policed by nothing today**. The OI-14 brief's hope that
  containment covered them is refuted; the Part B schema tier is where that
  coverage lands.
- Two figures in the OI-14 brief did not reproduce and are corrected by the
  pack: `LLR.Module` distinct values 59 (brief said 70), vacuous IF rows 45/68
  (brief said 46/67). Every load-bearing figure (149 LLRs, 5 multi-tags,
  97/64/17/33 edge accounting) reproduced exactly.

## What ratification at the owner's return looks like

Accept or overturn: (1) P5 as the depth-0 partition; (2) the CMP-006..009
mint and CMP-001..005 retirement; (3) the Area→aspect conversion; (4) the
boundary inventory (34 crossings, its completeness declaration, and the two
OI-28 seeds inside it). Everything is warn-first until then; overturning
re-tags traced cells and re-derives generated surfaces, nothing else.
