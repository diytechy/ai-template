# DP-001 verdict — arbiter select-and-port (2026-07-16)

**VERDICT: SELECT plan-B-rev ports=0** — the two position-swapped arbiter runs
**agree** (the swap rule passes), each selecting the same underlying plan under
opposite labels. `RESIDUAL GAPS: none` in both runs.

## Round record

| Hat | Session (family/model/effort) | Artifact |
|---|---|---|
| Planner A | OPENAI / gpt-5.6-sol (codex exec, fresh, isolated cwd) | [plan-A.md](plan-A.md) |
| Planner B | ANTHROPIC / claude-fable-5, high (claude -p, fresh, isolated cwd) | [plan-B.md](plan-B.md) |
| Coverage r1 | `plan_coverage.py` (mechanical) | [coverage-r1.md](coverage-r1.md) — both 7/7, diff empty |
| Critic of A | ANTHROPIC / opus, xhigh | [critique-of-A.md](critique-of-A.md) — 1 finding [G1] |
| Critic of B | OPENAI / gpt-5.6-terra | [critique-of-B.md](critique-of-B.md) — 1 finding [B2] |
| Revision A | OPENAI / gpt-5.6-sol | [plan-A-rev.md](plan-A-rev.md) — split P3→P3+P4 |
| Revision B | ANTHROPIC / claude-fable-5, high | [plan-B-rev.md](plan-B-rev.md) — P3 runtime-nonresponse fallback |
| Coverage r2 | `plan_coverage.py` (mechanical) | [coverage-r2.md](coverage-r2.md) — both 7/7, refs resolve |
| Arbiter ×2 | ANTHROPIC / opus, xhigh (fresh each; anonymized, coin-flipped labels, positions swapped) | [verdict-run1.md](verdict-run1.md) · [verdict-run2.md](verdict-run2.md) |

Hard caps honored: one cross-critique round, one revision each, no further
rounds; the arbiter judged artifacts only (plans + coverage reports + rubric +
owner prompt).

## De-anonymization

Run 1 labels: A = plan-B-rev (fable), B = plan-A-rev (sol) → `SELECT A`.
Run 2 labels: A = plan-A-rev (sol), B = plan-B-rev (fable) → `SELECT B`.
Both select **plan-B-rev** (the ANTHROPIC planner's revision).

## Deciding anchors (consistent across both runs)

- **G4/B4:** plan-B-rev's DAG is edge-free where possible (P2/P3/P5
  standalone) with one defended artifact edge (P4→P1, typed outcome
  constants) and a single P6 integration fan-in; plan-A-rev carries a
  near-linear P1→…→P6 chain both runs read as partly sequencing habit.
- **G1:** plan-B-rev's rows carry their own testable done-conditions (pure
  state machine unit-tested against injected step results; fixture-branch
  tests per row). (Run 1 scored this even, run 2 scored it for the same plan;
  neither scored it against.)
- Anchors G2/G3/B1/B2/B3 were even or marginal in both runs — the coverage
  pre-pass had already equalized coverage (7/7 both), which is what it is for.

## Ports

None. The losing plan covers no clause the selected plan misses
(coverage diff empty both rounds), so there are no coverage-closing deltas to
port; per the layer, ports exist only to close coverage gaps.

## Recorded degradations & caveats (honest, per the layer)

- **No third family available** on this host (`gemini` absent; two families
  enabled: ANTHROPIC, OPENAI). The arbiter ran on ANTHROPIC/opus — a
  different *model* from planner B's fable session but the **same family**:
  the recorded, mitigated degraded case (provenance-anonymized inputs,
  coin-flipped labels, position-swap ×2 with the agreement rule). The
  self-preference caveat stands: an ANTHROPIC arbiter selected the
  ANTHROPIC-authored plan. Counterweights on the record: the cross-family
  critic (terra) found only one finding in that plan; both swapped runs cite
  concrete row-level anchor reasons (the edge-free DAG, the in-row
  done-conditions) that a reader can verify against the artifacts.
- **Transfer caveat** (rubric + knowledge pack): this protocol is the
  best-supported extrapolation from QA/math/code evidence — plan-artifact
  selection is unbenchmarked. DP-001 is a single sample, not validation.
- **Acceptance:** closed under `docs/gate-policy: autonomous` on recorded
  verdicts (this file); the owner's `Attest` remains open to re-open the
  selection at the next sitting.

## Disposition

The selected plan's six rows are filed as queued WIs **WI-194…WI-199**
(workstream `unattended`, predecessor edges as in the plan: WI-197→WI-194,
WI-199→all five; WI-194/WI-199 `strong`, the rest `medium`), SpecRef →
[plan-B-rev.md](plan-B-rev.md) + this verdict.
