# Enforcement audit — this meta-repo

The kit's own worked example of the **enforcement-audit** discipline
([process-options.md](../project-trajectory/PROCESS_OPTIONS.md) "Enforcement
audit — which file enforces this rule tomorrow?"). One question of every
behavioral rule the repo commits to: *which file enforces it tomorrow, when
nobody is being careful?* Each rule gets its **strongest** enforcer —
**Harness** (deterministic hook/CI/`check.py` step) › **Test** (`tests/`
regression net) › **Reviewer** (independent charter) › **Prose** (judgment that
cannot be mechanized). The bar is honesty: **no rule left unbacked without a
stated reason.**

This is evidence, not a rule source — the rules live in
[AGENTS.template.md](../project-trajectory/AGENTS.template.md) (working
agreement) and [PROCESS.md](../project-trajectory/PROCESS.md); this table only
records where each one bites.

## Process disciplines

| Rule | Primary | Enforcer file |
|---|---|---|
| Everything traces `SN→SR→LLR→TC`; 0 orphans before a gate | Harness | `trace.py --strict` (G2/G3 step; pre-commit `--strict-integrity` floor) |
| No duplicate/malformed id; CSV structure; citation coherence | Harness | `trace.py --strict-integrity` (pre-commit) |
| Code map is generated, never hand-edited | Harness | `gen_arch_map.py --check` (pre-commit + G3) |
| Trajectory dashboard / OKF bundle stay fresh | Harness | `check.py --run-step trajectory-map / okf` (pre-commit + G3) |
| `status.md` stays forward-only (no closed-WI id accretes) | Harness | `check_trajectory` done-id rule (warn / ERROR `--strict`; WI-200 restored the WI-180-retired R-D, mode-aware — the generated splice block alone is exempt, its freshness being the `status-map` step's job; the hand-authored remainder stays policed, 2026-07-21) |
| Kit scripts are stdlib-only | Test | `tests/test_stdlib_only.py` (TC-034) |
| No secret committed or pushed | Harness | `check_privacy.py` floor + `hooks/pre-commit`, `hooks/pre-push` |
| Train-build commit carries a parseable `WI:` trailer (the integrator's reviewed-head key) | Harness | `hooks/commit-msg` pure-sh floor on `llm/train/*` (WI-282, was Prose in the worker prompt); `agent_dispatch.warn_reviewed_head_slip` is the loud reviewed-head-mismatch backstop |
| Runtime flows diagrammed and current | Harness | `check_flows.py` (G2/G3) |
| No stub/placeholder at G3 | Harness | `check_stubs.py` (G3) |
| Docs stay navigable (links resolve; vision tag present) | Harness | `check_docs.py --stale` |
| `AGENTS.template.md` stays within its byte budget | Test | `test_bootstrap.py::test_agents_template_stays_within_size_budget` |
| Write the test first (failing-first TC) | Reviewer | G2 review (ordering can't be mechanized; the TC's existence is checked, its *timing* is judged) |
| Gates close only on the declared authority | Harness + Prose | `check.py --gate` runs the bar; the human attestation in `docs/log.md` is Prose |
| Specs act on declared `IF-###` seams (cite resolvable IFs; Proposed carries a rationale) | Harness + Reviewer | `check_trajectory` spec-interface check (warn / ERROR `--strict`, vacuous-until-armed); near-dup honesty is Reviewer (finding 4) |
| Spec-lifecycle close side: done WI clears `SpecRef`; a live spec has an open citer (archive at close) | Harness + Reviewer | `check_trajectory` R-F (WI-251; warn / ERROR `--strict`) mechanizes the pointers; whether durable spec content was **absorbed** into a spine/architecture home before archiving is Reviewer-tier (the honest gap — the sweep's per-spec dispositions live in `log.md`) |

## Working-agreement rules (AGENTS.template.md)

| Rule | Primary | Backup / note |
|---|---|---|
| One fact, one home — no copy-paste logic | Harness | `check_dupes.py` (opt-in `[step:dupes]`); Reviewer for semantic dups |
| Fail loudly, never silently | Test + Reviewer | scripts' own error-path tests; a bare except is a review finding |
| Automation-safe by default (never blocks headless) | Test | `agent_loop`/hook headless tests; `preflight` guards footing |
| Right-size; every line is a liability | Reviewer | Prose — over-engineering flagged either way (no hard check) |
| Scope is a promise; stay in your lane | Reviewer | the diff review; a silent extra is a finding, not a merge |
| When reality contradicts the plan, name the conflict | Prose | Reviewer backs it (a silently-resolved conflict is a finding) |
| Flag uncertainty; distrust certainty | Prose | judgment; not mechanizable |
| No sunk-cost shipping, no blind retries | Prose | judgment; the loop's stall guard makes repeated failure *visible* |
| Ask one good question, not five hedges | Prose | judgment; not mechanizable |
| Repo text is memory; promote durable facts to `docs/` | Prose + Harness | `check_docs` keeps the promoted links live; the promotion itself is judgment |
| Back-link implementing symbols with `Implements: SR-/LLR-` | **Prose (gap)** | see Findings — surfaced by the map but **not required** by any check |

## Findings from this audit

1. **Stdlib-only was an Inspection; now a Test.** SR-034/TC-034 were
   `Verification=Inspection` ("confirmed by inspecting imports") — an eyeball
   that never fires in CI. Promoted to `tests/test_stdlib_only.py` (an AST
   import scan with a positive-control case). **Resolved.**
2. **The `Implements:` back-link convention is unenforced.** `gen_arch_map.py`
   *harvests* an `Implements: SR-/LLR-` docstring tag into the code map's third
   column, and the working agreement asks for it — but nothing **requires** it,
   so the meta-repo's own scripts carry none and the column is empty. Honest
   class today: **Prose** (a documented convention with no enforcer). Closing
   it (a warn-first check that an LLR's named `CodeSymbol` carries the tag)
   pairs naturally with the architecture-connectivity work; **filed, not built.**
3. **The judgment rules are honestly Prose.** The five "how to think" rules
   (ask-one-question, distrust-certainty, no-sunk-cost, name-the-contradiction,
   right-size) have no mechanical enforcer and are not expected to — they are
   reserved for the always-loaded guide by design, and the reviewer charter is
   their only backup. Recorded as a **stated reason**, per the audit's bar.
4. **Spec-interface near-duplication is reviewer-tier (WI-191).** The mechanical
   check (`check_trajectory.spec_interface_findings`) verifies a spec's
   `## Interfaces` citations **resolve** and that a `Proposed` citation carries a
   **non-empty** rationale — presence, which is checkable. But whether the
   rationale is *honest* (truly names the nearest seam) and whether a `Proposed`
   contract near-duplicates an existing `IF-###` are judgment calls:
   `check_dupes`' token windows work on code, not contract prose. Backed by the
   plan/spec critique-rubric anchor
   [`docs/rubrics/spec-interface-hygiene.md`](rubrics/spec-interface-hygiene.md)
   **B1** ("proposes a near-duplicate of `IF-###` instead of consuming or
   amending it"), which WI-190's plan rubric imports. Recorded as a **stated
   reason**: Reviewer is the strongest honest enforcer for contract-prose
   semantics.
