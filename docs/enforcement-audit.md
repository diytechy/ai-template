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
| Everything traces `SN→SR→LLR→TC`; 0 orphans before a gate | Harness | `trace.py --strict` (DevBar-Tests/DevBar-Release step; pre-commit `--strict-integrity` floor) |
| No duplicate/malformed id; CSV structure; citation coherence | Harness | `trace.py --strict-integrity` (pre-commit) |
| Code map is generated, never hand-edited | Harness | `gen_arch_map.py --check` (pre-commit + DevBar-Release) |
| Trajectory dashboard / OKF bundle stay fresh | Harness | `check.py --run-step trajectory-map / okf` (pre-commit + DevBar-Release) |
| `status.md` stays forward-only (no closed-WI id accretes) | Harness | `check_trajectory` done-id rule (warn / ERROR `--strict`; WI-200 restored the WI-180-retired R-D, mode-aware — the generated splice block alone is exempt, its freshness being the `status-map` step's job; the hand-authored remainder stays policed, 2026-07-21) |
| No *unargued* dependency: every non-stdlib import in a kit script is a reviewed ledger row | Test | `tests/test_dependency_ledger.py` (TC-034; WI-420 re-pointed it here from the retired `test_stdlib_only.py`, which asserted the pre-RULING-3 absolute "stdlib-only" and had become stricter than SR-034 permits) |
| An **adopter-facing** dependency (reached by a `layer="process"` check) is `Tier=shipped` **and** owner-ruled | Test | `tests/test_shipped_tier.py` (TC-149; WI-420 — derives the adopter-facing set from `check.py`'s own layer tags and walks transitive sibling imports) |
| No secret committed or pushed | Harness | `check_privacy.py` floor + `hooks/pre-commit`, `hooks/pre-push` |
| Runtime flows diagrammed and current | Harness | `check_flows.py` (DevBar-Tests/DevBar-Release) |
| No stub/placeholder at DevBar-Release | Harness | `check_stubs.py` (DevBar-Release) |
| Docs stay navigable (links resolve; vision tag present) | Harness | `check_docs.py --stale` |
| `AGENTS.template.md` stays within its byte budget | Test | `test_bootstrap.py::test_agents_template_stays_within_size_budget` |
| Write the test first (failing-first TC) | Reviewer | DevBar-Tests review (ordering can't be mechanized; the TC's existence is checked, its *timing* is judged) |
| Gates close only on the declared authority | Harness + Prose | `check.py --gate` runs the bar; the human attestation in `docs/log.md` is Prose |
| A post-attestation spine amendment owes a re-attest (WI-316) | Harness + Prose | Was Prose-only (`RE-ATTESTATION PENDING` commit-message flags — durable nowhere, derived by nothing). Now: `Status=Modified` pulls the derived gate to DevBar-Tests (`derive_gate`), projects a pending-owner-actions line (`gen_trajectory --status`), counts on the basis line (`modified=N`), and the `--staged` amend-without-flip warn polices the write side (`check_trajectory`). Honest residue: *setting* the marker is still discipline — the staged warn is warn-tier and a determined omission survives it; the flip back (`Modified`→`Verified`/`Planned`) is the human judgment itself, recorded in `log.md` Decisions (Prose, correctly — that judgment is the thing being trusted) |
| Specs act on declared `IF-###` seams (cite resolvable IFs; Proposed carries a rationale) | Harness + Reviewer | `check_trajectory` spec-interface check (warn / ERROR `--strict`, vacuous-until-armed); near-dup honesty is Reviewer (finding 4) |
| Spec-lifecycle close side: done WI clears `SpecRef`; a live spec has an open citer (archive at close) | Harness + Reviewer | `check_trajectory` R-F (WI-251; warn / ERROR `--strict`) mechanizes the pointers; whether durable spec content was **absorbed** into a spine/architecture home before archiving is Reviewer-tier (the honest gap — the sweep's per-spec dispositions live in `log.md`) |
| One decision per row / one home per method (re-tier v2 R1, log `2026-08-15p`) | Harness (advisory) + Reviewer | `trace_text.sr_fanout_advisories` (warn-only, never the exit code): an SR whose direct-LLR fan-out exceeds the declared bound (default 7) warns unless its `rationale` carries a `fan-out re-stamp` with its reason — a DETECTOR for merged rows, deliberately not a cap. Whether a split is by observable class, and whether two rows share one interface identity, stays the consistency review's |
| A requirement cell never names a concrete artifact (re-tier v2 R2, supersedes 2.7(a)) | Harness (advisory) + Reviewer | `trace_text.sr_artifact_advisories` (warn-only, never the exit code): a `*.py` token in an SR `requirement` cell warns unless the `rationale` carries a stated 13v reason; >1 SR naming one artifact warns naming the rows. Presence only — capability/artifact-class VOICE is judgment, the review's |
| `this_project` stays derivable as owner→LLR→`module` until wi455 drops the cell (re-tier v2 R4, log `2026-08-15p`) | Harness (advisory) | `trace_text.if_this_project_advisories` (warn-only, never the exit code): an LLR-owned IF row whose owner-side endpoint (`this_project` for Provides, `counterpart` for Consumes) is module-shaped but disagrees with the owner LLR's `module` warns naming both cells — a redundant cell can be deleted, a disagreeing one cannot. Non-module endpoints are out of scope by design (wi455's counterpart-transform); SR-owned rows are silent until re-pointed |
| A row states ONE verification method — its prose does not claim an instrument its `Verification` field contradicts | Harness (advisory) | Was **nothing**: the enum and the prose describe the same thing and no check compared them, so SR-052/SR-053 flipped `Critique`→`Test` on 2026-07-26 and went on demanding an APPROVE verdict from rubrics whose headers read RETIRED — three weeks, several reviews and a full re-tier pass at rc=0. Now `trace_text.verification_coherence_advisories` (warn-only, never the exit code; log `2026-08-16p`) over `Rationale` + `AcceptanceCriteria`. Two measured narrowings, both recorded in the docstring: `Requirement` is excluded (it fired on SR-040, where `CRITIQUE` names a routed session phase, not a verdict), and the rubric token is the bare word rather than a path (the path form missed all three real cases). One direction only — a `Critique` row naming no instrument is not reported, since its TC may legitimately hold the naming. Honest residue: detection is the token AS WRITTEN, so a cell describing a critique without the vocabulary passes |
| A retired perceptual gate's residue is not implied to be live coverage | **Prose (accepted gap, owner ruling `2026-08-16p`)** | RULING-5 retired SR-054's perceptual gate and named the residue "the periodic advisory critique", but `perceptual-stale` selects on `Verification=Critique` SRs — an empty set since the flip — so nothing re-fired it across 80 render-surface commits. Re-arming on TC `level="Critique"` was refused: an LLM critic on an any-change trigger would re-fire on nearly every spine change, and the loop was not working well before. The clause therefore rests on a **one-time recorded judgement**, stated as such in SR-054 and at `LLR-055`/`TC-055` rather than implied as standing coverage. `perceptual-stale` is untouched and stays correct for a downstream repo that declares a Critique SR |
| A spine row's Evidence-class citation (TC `Evidence`; LLR `Module`/`CodeSymbol`/`TestRefs`) names a FILE that exists | Harness + **Prose (accepted gap: the `::node` selector)** | Was nothing — an invented citation passed every strict gate at rc=0 while its row read `Automated=Yes, Status=Verified` (WI-394's driven evidence). Now: `check_doc_refs.py`'s registry tier (WI-394, owner ruling R2 2026-08-01, option (c)) checks the FILE half of each citation exists — warn-first, gating at the `[step:doc-refs]` `--strict` DevBar-Release step, the WI-062 precedent. The `::node` test-id selector (and `CodeSymbol`'s symbol names) are ruled **prose by that same ruling**: a renamed-but-still-present test node is deliberately NOT detected — accepted for false-positive control (the original `::` guard's real question), recorded here so it is never implied as covered |

## Working-agreement rules (AGENTS.template.md)

| Rule | Primary | Backup / note |
|---|---|---|
| One fact, one home — no copy-paste logic | **Test (policy only) + Reviewer** | **Downgraded 2026-08-11 by owner ruling (repo-lock D-7, executed WI-426): the mechanical duplication census is GONE** — `check_dupes.py`, `docs/dupes-allow` and the `[step:dupes]` step are deleted, on the evidence that it caught once at the one-time triage and never since, went silent exactly when a copy DIVERGED (the dangerous case), and spent 93% of its census lines registering accepted idioms. What replaces it is narrower and honest: duplicated **policy** must carry a behavioural pin in [`tests/test_rule_sync.py`](../tests/test_rule_sync.py) (its docstring is now the F5 rule's live home) or [`tests/test_wi_loader_sync.py`](../tests/test_wi_loader_sync.py); duplicated **plumbing** is accepted **unbounded**, which the ledger showed was its de-facto state anyway. Reviewer remains the only enforcer for semantic dups |
| ~~A census class states a rationale a reader can CHECK against its blocks~~ | **n/a — the subject is gone** | **RETIRED 2026-08-11 with the census itself (D-7/WI-426).** Kept as a line rather than deleted because the reasoning is reusable the next time someone proposes a classified allowlist. It was a mechanized majority rule in `tests/test_dupes_census_audit.py`; 129-REVIEW-A **drove and bypassed** it (even split + keyword-stuffed row, WI-350), and the Phase 5 dispatcher deletion false-positived it in the opposite direction (an honest shrink concentrated the survivors). Per the 2026-07-28 audit ruling the property is not fully mechanizable — the checkable halves (per-section counts, distribution-table consistency, charged-class-names-open-WI-and-modules) stay tests; whether a class's rationale actually fits its blocks is the reviewer's read |
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
| A signed measurement is reproducible, or marked historical (WI-342) | **Reviewer (truth) + Harness (presence of provenance, WI-392)** | process-options.md "Signed measurements". Nothing can tell a live measurement from a recollection, so the **truth** of a figure stays Reviewer — asking "re-derive that number" works: 127-REVIEW-A and 128-REVIEW-A between them refuted or marked UNVERIFIABLE eight signed figures, and three false figures on 2026-08-01 each cost a review round. The mechanizable half is now mechanized: a figure declared under the opt-in marker (`fig: cmd="…" rev=…`, or a derivation for a figure computed from declared figures) must carry the command that produced it and the revision it was driven at — `check_figures.py`, warn-first, gating at the `[step:figures]` `--strict` DevBar-Release step. Presence, never truth; an unmarked figure is out of scope by design ("declared figures carry provenance", never "all figures do"). **Rung 2 — re-derivation by running the recorded command — is a declared absence, deliberately NOT built** (WI-392; drain plan 2026-08-01 row 6): recorded commands are an execution surface needing an allow-list, most figures are legitimately historical (valid only at the recorded revision, which may be unreachable), and some are expensive (tests+coverage 634 s) or non-deterministic — recorded here so it is never implied as covered |
| A review finding is confirmed (reproduced) or refuted before code changes; a re-review round verifies fixes, never hunts fresh findings in them (WI-373) | Reviewer + Prose | process-options.md "The LLM-gate verdict protocol" (the finding lifecycle). Symmetric to the signed-measurements row: nothing mechanical can tell a reproduction from a recollection, so the round record holding the confirm/refute evidence is the enforcer; `score_reviews.py`'s confirmed-finding rate is the advisory backstop *on paper* — its scoreboard has been dark since 2026-07-15, and feed-or-delete is an open owner call (2026-07-28 audit rec #8). The evidence: rounds 127→131 ran ~70% non-product findings, and the self-aimed rounds converged to zero while manufacturing work |
| Undoing takes the same evidence as doing — read the record behind landed work before reverting it (WI-373) | Prose | working agreement; Reviewer backs it (a revert citing no record is a finding). Origin: parked work scrubbed by sessions that never read the record justifying it (owner directive 2026-07-30) |
| A wrong design escalates as a written case to its owner, never patched around or parked — no sunk-cost keeping (WI-373) | Prose | working agreement; judgment, not mechanizable. The ConcurrencyTrainRewrite restructure is the worked precedent that deliberate costly rework is the sanctioned move |

## Findings from this audit

1. **Stdlib-only was an Inspection; then a Test; now the right two tests.**
   SR-034/TC-034 were `Verification=Inspection` ("confirmed by inspecting
   imports") — an eyeball that never fires in CI. Promoted to an AST import scan
   with a positive-control case. **Resolved** — but WI-419 then widened SN-011
   from "no pip installs" to the RULING-3 bar ("no *unargued* dependencies"),
   which left that test asserting **stricter than its own requirement**, and a
   second scan (`test_dependency_ledger.py`) already made the identical
   assertion with the ledger term included. WI-420 deleted the duplicate and
   spent it on the clause that had **no enforcer at all**: the `Tier` column was
   never read, so nothing distinguished a `coordinator` dependency (this repo
   installs it) from a `shipped` one (**every adopter** is forced to install
   it). `tests/test_shipped_tier.py` now derives the adopter-facing check set
   from `check.py`'s own `layer="process"` tags — not a hand-copied list — and
   holds its transitive import closure to `Tier=shipped` + a recorded ruling.
   **Resolved, and the honest gap it exposed is now closed rather than
   recorded.**
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
   token-window duplicate detection works on code, not contract prose (and the
   kit no longer ships any — D-7/WI-426). Backed by the
   plan/spec critique-rubric anchor
   [`docs/rubrics/spec-interface-hygiene.md`](rubrics/spec-interface-hygiene.md)
   **B1** ("proposes a near-duplicate of `IF-###` instead of consuming or
   amending it"), which WI-190's plan rubric imports. Recorded as a **stated
   reason**: Reviewer is the strongest honest enforcer for contract-prose
   semantics.
