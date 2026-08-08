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
| No *unargued* dependency: every non-stdlib import in a kit script is a reviewed ledger row | Test | `tests/test_dependency_ledger.py` (TC-034; WI-420 re-pointed it here from the retired `test_stdlib_only.py`, which asserted the pre-RULING-3 absolute "stdlib-only" and had become stricter than SR-034 permits) |
| An **adopter-facing** dependency (reached by a `layer="process"` check) is `Tier=shipped` **and** owner-ruled | Test | `tests/test_shipped_tier.py` (TC-149; WI-420 — derives the adopter-facing set from `check.py`'s own layer tags and walks transitive sibling imports) |
| No secret committed or pushed | Harness | `check_privacy.py` floor + `hooks/pre-commit`, `hooks/pre-push` |
| Runtime flows diagrammed and current | Harness | `check_flows.py` (G2/G3) |
| No stub/placeholder at G3 | Harness | `check_stubs.py` (G3) |
| Docs stay navigable (links resolve; vision tag present) | Harness | `check_docs.py --stale` |
| `AGENTS.template.md` stays within its byte budget | Test | `test_bootstrap.py::test_agents_template_stays_within_size_budget` |
| Write the test first (failing-first TC) | Reviewer | G2 review (ordering can't be mechanized; the TC's existence is checked, its *timing* is judged) |
| Gates close only on the declared authority | Harness + Prose | `check.py --gate` runs the bar. The human attestation was Prose alone (a paragraph in `docs/log.md`); since the attestation ledger it is also an **append-only event** carrying the artifact id, the normative digest and the decision word (`attest.py`), so "which text was approved, by whom, when" is now machine-readable and re-derivable. The *judgment* stays Prose — correctly, since that judgment is the thing being trusted |
| A post-attestation spine amendment owes a re-attest (WI-316) | Harness + Prose | Was Prose-only (`RE-ATTESTATION PENDING` commit-message flags — durable nowhere, derived by nothing). Then: `Status=Modified` pulls the derived gate to G2 (`derive_gate`), projects a pending-owner-actions line (`gen_trajectory --status`), counts on the basis line (`modified=N`), and the `--staged` amend-without-flip warn polices the write side (`check_trajectory`). **The residue that row recorded — "setting the marker is still discipline, and a determined omission survives the warn" — is now largely closed, and by a different mechanism:** `attest.detect_candidates` compares the row's **current normative digest** against its accepted anchor, so an amendment is detected whether or not anyone set a marker, whether or not it was staged in one diff, and whether or not the Status moved (the two structural blind spots of the staged check, `docs/registry-machinery-reference.md` §8.6). What remains Prose is only the verdict itself — `clarity` vs `meaning` is a reading of intent — and that verdict is now a recorded event rather than a recollection |
| Specs act on declared `IF-###` seams (cite resolvable IFs; Proposed carries a rationale) | Harness + Reviewer | `check_trajectory` spec-interface check (warn / ERROR `--strict`, vacuous-until-armed); near-dup honesty is Reviewer (finding 4) |
| Spec-lifecycle close side: done WI clears `SpecRef`; a live spec has an open citer (archive at close) | Harness + Reviewer | `check_trajectory` R-F (WI-251; warn / ERROR `--strict`) mechanizes the pointers; whether durable spec content was **absorbed** into a spine/architecture home before archiving is Reviewer-tier (the honest gap — the sweep's per-spec dispositions live in `log.md`) |
| A spine row's Evidence-class citation (TC `Evidence`; LLR `Module`/`CodeSymbol`/`TestRefs`) names a FILE that exists | Harness + **Prose (accepted gap: the `::node` selector)** | Was nothing — an invented citation passed every strict gate at rc=0 while its row read `Automated=Yes, Status=Verified` (WI-394's driven evidence). Now: `check_doc_refs.py`'s registry tier (WI-394, owner ruling R2 2026-08-01, option (c)) checks the FILE half of each citation exists — warn-first, gating at the `[step:doc-refs]` `--strict` G3 step, the WI-062 precedent. The `::node` test-id selector (and `CodeSymbol`'s symbol names) are ruled **prose by that same ruling**: a renamed-but-still-present test node is deliberately NOT detected — accepted for false-positive control (the original `::` guard's real question), recorded here so it is never implied as covered |

### The mechanized-loop rungs (2026-08-08)

Added when the loop's judgement machinery landed. Each row states the rule the
program committed to and the file that bites tomorrow; where the strongest
honest enforcer is still a human, the row says so rather than implying a guard.

| Rule | Primary | Enforcer file |
|---|---|---|
| Behavior is declared **once**, in one validated file — no key has two homes | Harness | `config.py`'s strict loader (unknown key / wrong type / out-of-range / absent-or-unsupported `schema` are each a **finding**, all printed before one refusal) plus `mixed_source_findings`, which refuses the dangerous middle state where a retired declared-policy file and its canonical key are both present rather than picking a silent precedence (SR-137/SR-138) |
| A dial cannot exist in code and be missing from the adopter's form | Test | `config.toml.template` is **generated** from the same declared `SCHEMA` table the validator walks, and pinned byte-equal — so the two cannot drift apart at all, rather than being compared after the fact |
| A shell hook that cannot read the policy **fails closed** | Test | `config_query.py` refuses loudly on a missing or below-floor interpreter; `tests/test_config_hooks.py` drives the refusal rather than grepping the source for a version string (the earlier test did exactly that, and a verifier deleted the floor check without reddening it) |
| "Approved" means *this text*, not a Status word | Harness | `attest.py`: a content digest over the declared normative cells, canonicalised so a re-wrap is not an amendment, anchored in an append-only ledger whose `parent` must equal the current head. `detect_candidates` asks the **tree**, so it has neither blind spot of the staged check (§8.6 of `registry-machinery-reference.md`) |
| A migration is never counted as a human approval | Harness | `attest.py --seed` writes the distinct decision word **`baseline`**, and `is_accepting` reads the word and nothing else. Driven: without it, a `--seed` run over this repo would have recorded 523 machine anchors indistinguishable from 523 ratifications, and a chain could read `[ratified/seed, meaning/<human>, ratified/seed]` — a machine erasing a human refusal |
| The workflow axis and the harness axis are never inferred from each other | Harness | `derive_gate.STAGE_GATE` is the one declared join, and `verification_gate_for` **refuses** an out-of-range stage by name instead of clamping (clamping is how an off-by-one silently runs the wrong step tier and calls it a gate) |
| A cached stage never claims a green it did not watch | Harness + Prose | `spine_stage` derives the **attestation half** of stage 4 only; `check.py` owns the harness half; the resume planner joins them. Nothing caches the join. The honest residue is that the split is a convention between three components — the enforcement is that neither component has the other's inputs, so neither *can* claim it |
| A branch may not narrow its own scope | Harness | `outcome.scope_digest` freezes the obligation cells and body sections at claim (deliberately excluding `## Deliverable`, which an honest close writes), recorded by `integrate.py` and compared at the merge. Driven hole, closed after the fact: the digest did not originally cover the admission declaration cells, so the blast radius a conflict verdict is *computed from* could be edited without moving it |
| A stopped attempt classifies every change group before it lands | Harness | `outcome.classify_groups` requires `keep`/`discard`/`quarantine` per group; an unlabelled group is a refusal, because "we did not decide" is exactly the state the 2026-08-03 incident (`08e6c08a`) merged |
| An attempted work item is never revived — remaining scope is a new row with lineage | Harness | `adjudicate.draft_successor` mints a `draft/` candidate carrying `supersedes` + `source_event`; `admit.py` refuses a candidate that supersedes itself, a non-work-item, or a row in a state that cannot be superseded — and the successor still faces the ordinary admission transaction |
| One transaction owns every move into `queued/` | Harness | `admit.admit` — validate, **move**, then record (a crash between the last two leaves a loud, re-runnable half-state; record-then-move would leave an append-only ledger asserting an admission that never happened) |
| A queued row's conflict ruling is present **and current** | Harness | `check_trajectory.admission_verdict_findings`' three rungs (absent / stale scope / stale spine), with a newest `conflict` counting as absent. Adoption is presence-gated on the ledger, and a legacy queue migrates by a `pre-transaction` **baseline event per row** rather than an id exemption — so the debt stays current instead of being exempted forever (SR-158) |
| A red declared bar mints **exactly one** remediation | Harness | `outcome.failure_event`'s id is the content digest of (tree, failing step, normalised fingerprint), so however many cycles observe one defect there is one event and one draft |
| Every operational prompt is a reviewed asset with a declared contract | Harness | `prompt_render.render` refuses an unknown, extra, missing or still-unrendered slot **before launch**; `prompt_render.py check` compares the declared slot list against the one **derived from the template** and refuses on a mismatch (a hand-written slot list is only a second place to be wrong) |
| A judge's brief never carries the judged party's self-assessment | Harness + Reviewer | `prompt_render.check_sources` against a **closed** source vocabulary, with `worker-rationale` prohibited in every judging brief (SR-156). Mechanical for *presence*; whether a brief's prose is actually adversarial enough stays Reviewer — no string-presence test can prove prose is semantically good |
| The resume precedence is deterministic and testable | Test | `resume_plan.plan(snapshot)` is a pure function of one frozen record, so "a lower rung is never selected while a higher rung has work" is arithmetic over fixtures. It was previously asserted in prose and **driven nowhere**, because every rung was entangled with the read that fed it and proving the ordering meant standing up a live station with real git, subprocesses and a clock |
| A new rung never reds a repo that has not adopted the thing it checks | Test | The presence-as-consent shape, now used by three rungs (the admissions ledger, the attestation ledger, and `resume_plan`'s ledger-reading rungs). Driven: P8's freshness rung red **seven** fixture modules on its first run, every one of them a tree that had never run an admission |

**Where this program RETIRED a rule rather than enforcing it better.** Two are
worth recording, because a retired rule that keeps a row would be an audit
claiming coverage of something nobody does any more:

- **The handback contract** (`hand_back`: commit as-is, move each claimed spec
  back to `queued/` carrying a `## Handback` section and a self-`blockref`) is
  retired by decision D-4. It never had a row here, and it must not gain one: a
  branch rewriting its own obligation is the *defect*, and the replacement —
  the `partial/` terminal plus an immutable outcome event — is covered by the
  scope-freeze and classify-groups rows above. The `quarantine` arm survives,
  generalized into the classification. The general `blockref` mechanism is
  untouched and is not part of the retirement.
- **Routing off a prose substring** (`NEEDS-HUMAN` matched inside a free-form
  reason string to select a strong tier) is retired by decision D-6: the tier
  decision keys off the **worker exit-code class**, and the reason string it
  read is deleted with the mutating handback. This is the "answered by
  deletion" case — there is nothing left to enforce, which is a stronger result
  than a guard would have been. The **label** rename (`NEEDS-HUMAN` →
  `NEEDS-JUDGEMENT`) is prose only: **exit code 7 does not move**, and the
  open-items *bucket* of the old name keeps its spelling, because there an
  owner call genuinely is the point.

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
| A signed measurement is reproducible, or marked historical (WI-342) | **Reviewer (truth) + Harness (presence of provenance, WI-392)** | process-options.md "Signed measurements". Nothing can tell a live measurement from a recollection, so the **truth** of a figure stays Reviewer — asking "re-derive that number" works: 127-REVIEW-A and 128-REVIEW-A between them refuted or marked UNVERIFIABLE eight signed figures, and three false figures on 2026-08-01 each cost a review round. The mechanizable half is now mechanized: a figure declared under the opt-in marker (`fig: cmd="…" rev=…`, or a derivation for a figure computed from declared figures) must carry the command that produced it and the revision it was driven at — `check_figures.py`, warn-first, gating at the `[step:figures]` `--strict` G3 step. Presence, never truth; an unmarked figure is out of scope by design ("declared figures carry provenance", never "all figures do"). **Rung 2 — re-derivation by running the recorded command — is a declared absence, deliberately NOT built** (WI-392; drain plan 2026-08-01 row 6): recorded commands are an execution surface needing an allow-list, most figures are legitimately historical (valid only at the recorded revision, which may be unreachable), and some are expensive (tests+coverage 634 s) or non-deterministic — recorded here so it is never implied as covered |
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
   `check_dupes`' token windows work on code, not contract prose. Backed by the
   plan/spec critique-rubric anchor
   [`docs/rubrics/spec-interface-hygiene.md`](rubrics/spec-interface-hygiene.md)
   **B1** ("proposes a near-duplicate of `IF-###` instead of consuming or
   amending it"), which WI-190's plan rubric imports. Recorded as a **stated
   reason**: Reviewer is the strongest honest enforcer for contract-prose
   semantics.
