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
| No live LLR grounds on a superseded SR (`SupersededBy` populated) | Harness | `trace.py --strict-integrity` (`sr_supersession_findings`; WI-364, owner-ruled error tier 2026-07-29 — TC citations stay legal, the TC-099/TC-133 evidence record) |
| Code map is generated, never hand-edited | Harness | `gen_arch_map.py --check` (pre-commit + G3) |
| Trajectory dashboard / OKF bundle stay fresh | Harness | `check.py --run-step trajectory-map / okf` (pre-commit + G3) |
| `status.md` stays forward-only (no closed-WI id accretes) | Harness | `check_trajectory` done-id rule (warn / ERROR `--strict`; WI-200 restored the WI-180-retired R-D, mode-aware — the generated splice block alone is exempt, its freshness being the `status-map` step's job; the hand-authored remainder stays policed, 2026-07-21) |
| Kit scripts are stdlib-only | Test | `tests/test_stdlib_only.py` (TC-034) |
| No secret committed or pushed | Harness | `check_privacy.py` floor + `hooks/pre-commit`, `hooks/pre-push` |
| Runtime flows diagrammed and current | Harness | `check_flows.py` (G2/G3) |
| No stub/placeholder at G3 | Harness | `check_stubs.py` (G3) |
| Docs stay navigable (links resolve; vision tag present) | Harness | `check_docs.py --stale` |
| `AGENTS.template.md` stays within its byte budget | Test | `test_bootstrap.py::test_agents_template_stays_within_size_budget` |
| Write the test first (failing-first TC) | Reviewer | G2 review (ordering can't be mechanized; the TC's existence is checked, its *timing* is judged) |
| Gates close only on the declared authority | Harness + Prose | `check.py --gate` runs the bar; the human attestation in `docs/log.md` is Prose |
| A post-attestation spine amendment owes a re-attest (WI-316) | Harness + Prose | Was Prose-only (`RE-ATTESTATION PENDING` commit-message flags — durable nowhere, derived by nothing). Now: `Status=Modified` pulls the derived gate to G2 (`derive_gate`), projects a pending-owner-actions line (`gen_trajectory --status`), counts on the basis line (`modified=N`), and the `--staged` amend-without-flip warn polices the write side (`check_trajectory`). Honest residue: *setting* the marker is still discipline — the staged warn is warn-tier and a determined omission survives it; the flip back (`Modified`→`Verified`/`Planned`) is the human judgment itself, recorded in `log.md` Decisions (Prose, correctly — that judgment is the thing being trusted) |
| Specs act on declared `IF-###` seams (cite resolvable IFs; Proposed carries a rationale) | Harness + Reviewer | `check_trajectory` spec-interface check (warn / ERROR `--strict`, vacuous-until-armed); near-dup honesty is Reviewer (finding 4) |
| Spec-lifecycle close side: done WI clears `SpecRef`; a live spec has an open citer (archive at close) | Harness + Reviewer | `check_trajectory` R-F (WI-251; warn / ERROR `--strict`) mechanizes the pointers; whether durable spec content was **absorbed** into a spine/architecture home before archiving is Reviewer-tier (the honest gap — the sweep's per-spec dispositions live in `log.md`) |

## Working-agreement rules (AGENTS.template.md)

| Rule | Primary | Backup / note |
|---|---|---|
| One fact, one home — no copy-paste logic | Harness | `check_dupes.py` (opt-in `[step:dupes]`); Reviewer for semantic dups |
| A census class states a rationale a reader can CHECK against its blocks (no catch-all bucket under any label) | Reviewer | Was a mechanized majority rule in `tests/test_dupes_census_audit.py`; 129-REVIEW-A **drove and bypassed** it (even split + keyword-stuffed row, WI-350), and the Phase 5 dispatcher deletion false-positived it in the opposite direction (an honest shrink concentrated the survivors). Per the 2026-07-28 audit ruling the property is not fully mechanizable — the checkable halves (per-section counts, distribution-table consistency, charged-class-names-open-WI-and-modules) stay tests; whether a class's rationale actually fits its blocks is the reviewer's read |
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
| Every environment-gated skip routes through the declared gate (WI-326) | **Harness + Reviewer (bounded gap)** | `tests/test_env_gates.py` bans, over the AST, a `skipif` condition that probes a gated tool, a function that both probes and skips, and a module that probes with `which` and skips while importing neither declared helper. What it CANNOT see, and does not claim to: a **cross-module** probe (module A decides, module B skips); a probe that shells out (`subprocess.run(["git", ...])`) rather than using `which`; and a probe whose result is frozen into a module constant at import time. Those are semantic. The first two AST rules were **driven and bypassed** by 130-REVIEW-A (helper indirection plus the tool name passed through a variable), which is why the module rule exists and why the residue is written down here instead of implied by a guard that would be advertising a property it lacks |
| A signed measurement is reproducible, or marked historical (WI-342) | **Reviewer (honest gap)** | process-options.md "Signed measurements". Nothing can tell a live measurement from a recollection, so no harness or test can hold this; the reviewer asking "re-derive that number" is the whole enforcer, and it works — 127-REVIEW-A and 128-REVIEW-A between them refuted or marked UNVERIFIABLE eight signed figures. The mechanizable half is the *habit*: commit the command and manifest before the fix destroys the input |
| A review finding is confirmed (reproduced) or refuted before code changes; a re-review round verifies fixes, never hunts fresh findings in them (WI-373) | Reviewer + Prose | process-options.md "The LLM-gate verdict protocol" (the finding lifecycle). Symmetric to the signed-measurements row: nothing mechanical can tell a reproduction from a recollection, so the round record holding the confirm/refute evidence is the enforcer; `score_reviews.py`'s confirmed-finding rate is the advisory backstop *on paper* — its scoreboard has been dark since 2026-07-15, and feed-or-delete is an open owner call (2026-07-28 audit rec #8). The evidence: rounds 127→131 ran ~70% non-product findings, and the self-aimed rounds converged to zero while manufacturing work |
| Undoing takes the same evidence as doing — read the record behind landed work before reverting it (WI-373) | Prose | working agreement; Reviewer backs it (a revert citing no record is a finding). Origin: parked work scrubbed by sessions that never read the record justifying it (owner directive 2026-07-30) |
| A wrong design escalates as a written case to its owner, never patched around or parked — no sunk-cost keeping (WI-373) | Prose | working agreement; judgment, not mechanizable. The ConcurrencyTrainRewrite restructure is the worked precedent that deliberate costly rework is the sanctioned move |

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
3. **The judgment rules are honestly Prose.** The "how to think" rules
   (ask-one-question, distrust-certainty, no-sunk-cost, name-the-contradiction,
   right-size — and, since WI-373, confirm-or-refute, reversal-evidence, and
   no-sunk-cost-keeping) have no mechanical enforcer and are not expected to —
   they are reserved for the always-loaded guide by design, and the reviewer
   charter is their only backup. Recorded as a **stated reason**, per the
   audit's bar.
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
