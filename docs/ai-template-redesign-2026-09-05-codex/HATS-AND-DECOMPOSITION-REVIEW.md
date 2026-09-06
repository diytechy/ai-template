# Vision, hats and SN-to-SR review

**Reviewed:** 2026-09-05, source `0402dc8f`, after committing the expanded
plan at the owner's request. This is a source-based review, not a new blind
derivation, an independent model verdict, or a live registry amendment.

**Verdict:** retain the objective proposal, add one upgrading-adopter lens,
and repair how existing perspectives reach and constrain decomposition.
The current SRs do **not** completely decompose every SN. Most capabilities
have recognizable coverage, but valid references hide several missing clauses.
Some other obligations are fully stated at SR and remain implementation debt;
those two cases need different treatment.

## 1. Vision and hat recommendation

The [live vision](../../README.md#vision) remains the purpose authority.
The proposed [O1–O6 anchors](VISION-OBJECTIVES.md) unpack it usefully. O5/O6
also expose commitments from the existing needs rather than merely reformatting
the opening paragraph; that scope clarification still deserves review.
Neither a new objective nor another approval stage is needed for the findings
below. In particular, O6 already names adoption and upgrade, and O1/O6 already
provide the purpose for measuring operating cost.

**Add `UPGRADING-ADOPTER`, subject to the normal roster review.** Proposed
question: “For a project already using this kit, which existing customizations,
policy meanings, accepted evidence and unfinished work must survive this
change, and how does that project complete or reverse the upgrade?”

Its distinct failure class is an upgrade that preserves file bytes but changes
their meaning, breaks supported callers, loses accepted evidence or strands
unfinished work. FIRST-RUN-ADOPTER asks about a stranger starting successfully;
MAINTAINER asks whether rationale survives; INTEGRITY-RECOVERABILITY asks about
interruption. None explicitly asks about a successful, intentional migration
of an existing adoption. SR-036 already supplies a starting contract, so this
lens should refine that family instead of creating an upgrade framework.

Recommend `always` for this meta-repo, with “no compatibility impact” a valid
answer. A new tag that nobody supplies would repeat the routing failure below.
Adopters retain the existing ability to narrow or remove seeded hats. A smaller
alternative is renaming/extending FIRST-RUN-ADOPTER to cover the whole adopter
lifecycle; do that only if the two distinct questions remain explicit.

| Existing hat | Objective connection | Recommendation after reading its actual charter |
|---|---|---|
| SECURITY | O3/O4 | Keep. Make authorization of an action explicit even when it neither spends a secret nor destroys data; current-policy approval fits this lens. |
| FIRST-RUN-ADOPTER | O6 | Keep the novice setup question; distinguish it from upgrade compatibility. |
| UNATTENDED-OPS | O5 | Keep. Reach every applicable unattended decomposition and record unavailable-provider, retry and stop behavior. |
| CROSS-PLATFORM | O6 | Keep. Supported-platform evidence is already stated by SR-114/SR-160. |
| MAINTAINER | O1/O2 | Keep. Ask whether rationale is still true after carrier changes, not only whether rationale exists. |
| TEST-ENGINEER | O3 | Broaden the question from only a mechanical check to suitable test, analysis, critique or attestation evidence and its demonstrated limits. Mechanical checks remain preferred where they actually verify the claim. |
| UX-DESIGNER | O5 | Keep. Apply the decision-first question to text/CLI owner surfaces as well as HTML. |
| UX-ENGINEER | O5 | Keep. Source inspection is insufficient for a claim about rendered usability. This review makes no rendering verdict. |
| SAFETY | O3 | Keep available as an opt-in downstream lens. No current need activates it; that alone warrants neither invented hazards nor extra SRs. The existing owner roster question remains unresolved. |
| LEGAL | O6/O3 | Keep. Repair routing to provider-consent work; the licence/contract question is distinct from credential detection. This review makes no legal-compliance judgment. |
| DATA-PROTECTION | O3 | Keep. Repair provider-work routing and preserve the deliberate limits recorded by SR-175/SR-176. |
| ACCESSIBILITY | O5 | Keep the owner-ruled unconditional question; verify nonvisual operation where a surface is involved. |
| PERFORMANCE | O1/O6 | Extend “speed or size” to provider spend, token usage and operator time, including completeness and measurement conditions. A separate cost/metrics hat would duplicate this purpose. |
| CONSISTENCY | O2/O4/O5 | Extend beyond vocabulary and rendering to agreement of meaning across related requirements, interfaces and policy readers when one side changes. |
| INTEGRITY-RECOVERABILITY | O3/O4 | Keep. Covers atomic writes, claims and interruption in attended as well as unattended use. |
| PRODUCT-FITNESS | O1/O5/O6 | Keep. Objective-to-need relevance and evidence that a stakeholder recognizes the result belong here; filled links do not establish either. |

Do not add separate AI, prompt, metrics, architecture or governance hats merely
because those topics occur in the redesign. A charter earns a separate name
only when its failure question cannot be assigned clearly to an existing lens.

## 2. Findings, ordered for implementation planning

### H1 — Applicable hats are not reliably carried into the real decomposition

**High; SN-036/SR-161, with SN-026 a concrete example.** The
[roster](../requirements/hats.toml) gates LEGAL on `legal` and DATA-PROTECTION
on `personal-data`. SN-026 supplies only `unattended` and `loop`, yet SR-175
expressly derives its inclusion/consent obligation from both hats, plus
SECURITY. A need-only derivation does not receive those two governing lenses.

There is a second break: [plan_runner._hat_slots](../../project-trajectory/scripts/plan_runner.py)
calls `hat_context_for_work_item(row)`. That context uses only Workstream and
SafetyClass. `hat_context_for_need` exists, but no shipped runner call merges
the referenced need's context into this brief. The need audit is therefore
not a proof about what the actual planner receives.

Reproduction: `_hat_slots(root, {Workstream: scripts, SafetyClass: normal,
SpecRef: docs/requirements/stakeholder-needs.toml#SN-026}, '{{HAT_QUESTIONS}}')`
omits LEGAL, DATA-PROTECTION and UNATTENDED-OPS. The synthetic row is a bounded
composer probe, not a claimed reproduction of a specific historical run.
No provider was invoked. Separately composing the need context with proposed
`legal`/`personal-data` tags selects all three.

**Smallest correction:** resolve the decomposition's actual scope through the
existing parsed references, combine relevant declared need/WI context once,
and use that shared result in the brief and audit. Do not scan every need or
infer tags from arbitrary prose. Reconcile SN-026's missing subject tags as
part of that work. Test the resulting brief, including a multi-parent scope
and a legacy prompt override. Record an override that omits hats explicitly;
the current warning is not evidence that its decomposition faced the roster.

### H2 — SN-024's rubric contract disappears at the SR tier

**High; TEST-ENGINEER, PRODUCT-FITNESS.** SN-024 requires a written rubric
derived from SN/SR intent, numbered rubric anchors in verdicts and independent
critique. SR-154 covers independence, routing and bounded rework; SR-155
covers competing plans. Neither states the rubric derivation or anchor-citation
obligations. No SR requirement or acceptance cell contains `rubric` at this
revision. SR-052/053/054's historical titles and rationales are not that contract.

There is also a scope narrowing: SR-154 begins when *unattended* work reaches
integration, while SN-024's subjective acceptance promise is not limited to
unattended integration. LLR-048 carries some rubric/intent briefing behavior;
that is evidence to preserve, not a substitute for the missing SR obligation.

**Smallest correction:** put the rubric/intent/verdict obligation in the
independent-acceptance contract, applicable whenever Critique acceptance is
required, and leave scheduling/routing in its own appropriate scope. Reuse
existing critique records and numbered findings. Counterexamples: a reviewer
approves against only the builder's TC; a verdict cites no criterion; an
attended critique evades the contract by never entering the loop.

### H3 — SN-037's coordinated requirement/interface change has no SR

**High; CONSISTENCY, MAINTAINER, TEST-ENGINEER.** SR-162 covers reference
resolution, boundary coverage and signal types. Its own rationale expressly
states that no SR carries SN-037's final clause: a one-sided requirement/interface
change must include or justify its counterpart. LLR-187 also records this as
unimplemented. This is an acknowledged missing obligation, not a newly inferred
desire for more architecture checking.

**Smallest correction:** add the missing change-review obligation with a
changed-side/affected-counterpart review record. A review or attestation can
judge semantic adequacy; do not pretend a reference-existence test can. No new
interface registry or SYSTEMS-ENGINEER hat is necessary to state this promise.
Counterexample: an SR changes signal meaning while its IF references still
resolve and its interface text remains unchanged.

### H4 — SN-007's whole-suite landing promise is not carried by its children

**Medium; TEST-ENGINEER, CONSISTENCY, PERFORMANCE.** SN-007 requires a green
whole suite before each change lands. Its children cover scaffold execution,
resync, version stamping, package structure and sensors. SR-010 says the suite
exercises every script, but not that the whole suite must pass before landing.
SR-151/152 carry declared CI moments under other needs; their selectable bars
do not resolve the discrepancy with SN-007's unconditional wording.

**Smallest correction:** explicitly reconcile the parent promise with the
declared per-commit/slice/release cadence, then state the agreed landing
obligation once and link its enforcers. Preserve current authority until that
amendment. Do not turn this into an unconditional all-green implementation-test
bar at DevStg-Tests. The owner's timing exception for the preceding documentation
commit is a recorded exception, not a general amendment of this need.

### H5 — SN-012's proportionality clause lacks an SR home

**Medium; PRODUCT-FITNESS, MAINTAINER, PERFORMANCE.** Optional scaffold
profiles and vacuous optional checks have SR coverage. The separate acceptance
clause governing LLR/TC granularity does not: none of SN-012's citing SRs states
how decomposition stays proportionate. Documentation can state the doctrine
while the declared SN-to-SR breakdown still omits it.

**Smallest correction:** state a reviewable proportionality obligation that
permits stopping decomposition when a child adds no independent decision or
verification value. Use review/attestation where appropriate. Do not invent
row-count caps, deletion quotas or a mandatory new ratchet. Counterexample:
every optional feature is absent, but one small edit still requires numerous
paraphrasing LLR/TC rows; the existing optional-profile SRs all pass.

### H6 — Correctly stated SRs still lack complete downstream evidence

**Material limitation, not an SN-to-SR decomposition defect.** These rows
should not be reminted merely because their children expose unfinished work:

| Need/SR | What remains according to its existing design/rationale |
|---|---|
| SN-036 / SR-161 | LLR-183's Hat-Refs records row attribution, not per-decomposition applicability or explicit no-finding. LLR-202's amendment warning does not fill that gap. |
| SN-037 / SR-162 | LLR-187 says joined-seam signal compatibility is not implemented; reference resolution alone does not discharge it. The missing SR change-review clause is separately H3. |
| SN-038 / SR-163 | LLR-203/204 distinguish inventory and reverse references from complete shipped-file-to-SR-to-SN coverage; unfilled references and consumer ownership remain debt. |
| SN-039 / SR-164 | LLR-194 says the SN scope field and its schema checking are not implemented. The general schema mechanism is not a scope-specific acceptance result. |
| SN-040 / SR-165 | LLR-172 records the absent component derivation-record fields. Naming a scoring/ranking checker does not establish that an actual partition record exists. |
| SN-026 / SR-175 | Its declared inclusion surface and planted-credential dispatch acceptance are recorded build gaps. Existing prompt conventions are narrower evidence. |
| SN-009 / SR-176 | Its rationale distinguishes credential redaction from the still-owed PII/identity classes. Protecting Git publication and filtering a provider brief are different boundaries. |
| SN-027 / SR-177 | LLR-196 supplies session telemetry; per-run fan-out aggregation is still owed. Neither implies the redesign's complete per-invocation token accounting. |

Extend the existing decomposition artifact with perspective results: source
revision, roster/context identity, each applicability result, and produced SR
references or explicit no-finding. Reuse existing review records, not a second
authority database. Keep substantive adequacy with independent review and
coverage advisories under their existing policy. Do not require one new SR
per hat, or treat an empty Hat-Refs cell as proof of neglect.

### H7 — Some parent/child text preserves obsolete or conflicting assumptions

**Medium; CONSISTENCY/MAINTAINER.** Three concrete reconciliation cases:

- SN-006's acceptance resumes from the tracked status surface; SR-026
  explicitly excludes generated status as a session input, and SN-025 selects
  from tracked WI/Git state. Preserve recovery intent while amending the obsolete
  carrier wording; do not reintroduce a status-prose reader to satisfy it.
- SR-178 repeatedly says stakeholder needs have no status cell. The current
  SN carrier has `status`. Keep the substantive protection against normative
  drift regardless of status movement, but retire the inaccurate premise.
- SN-009's unqualified protection wording and always-on acceptance must be
  read alongside SR-017's explicit `secrets_scan = false` exception and the
  documented bypassability of local hooks in SR-019. Clarify the promised
  default and limits in the normative contract; do not claim a hosted check
  prevents an earlier disclosure. This review does not change those dials.

SN-006's deliberate fail-open *supervision* and SN-029's conservative approval
authority also need an explicit boundary in the replacement. A metrics or
supervision fault cannot silently relax approval authority. This is preservation
of distinct existing contracts, not a recommendation to make every fault fatal.

## 3. Sweep across every current SN

This table summarizes the semantic sweep. “Covered” means no additional
SN-to-SR clause gap was identified here; it is not a test result or certification
of all reachable behavior. The perspectives column names the most consequential
lenses for the finding, not a quota or a replacement for the full roster.

| SN | Principal SR homes inspected | Perspectives and result |
|---|---|---|
| 001 | 010/011/032/036/046/111/113/166 | Adopter, security, consistency: install/preserve/setup covered; upgrading-adopter lens should challenge semantic compatibility. |
| 002 | 015/024/129/147/155/157/159/180 | Test, maintainer: joins and migration evidence covered; zero orphans does not prove clause completeness. Reassess solution-specific mechanisms during P9. |
| 003 | 007/009/035/114/180 | Adopter, platform: declarative stack swap and non-Python support covered. |
| 004 | 006/031/033/049/149/151/181 | Test, authority, consistency: stage/bar coverage present; preserve failing-first definition work when resolving H4. |
| 005 | 019/020/031/146/151/152 | Security, consistency: local/reference-CI pairing and declared moments covered, with expressly limited control over adopter-edited CI. |
| 006 | 026/027/028/040/043/148/154/155/171/172 | Operations, recovery, security: substantial coverage; resolve status-source drift and supervision/authority boundary (H7). |
| 007 | 010/011/036/111/166/182/183 | Test, consistency, performance: missing landing obligation/cadence reconciliation (H4). |
| 008 | 006/049/148/152/156/158/167/170/173/174/181 | Test, integrity: honest outcomes and required-bar behavior covered through explicit selection/skip semantics; reports must preserve those limits. |
| 009 | 017/018/019/020/176 | Security, data protection: publication/redaction contracts present; exception wording and remaining redaction debt need treatment (H6/H7). |
| 010 | 022/070/148/149/158/168/170/173 | Consistency, usability: navigation, singleton vision and freshness covered. Objective references would be a reviewed extension. |
| 011 | 034/035/114 | Adopter, platform, legal: dependency admission and supported-platform evidence covered. |
| 012 | 009/043/070/112/129/147/157/159/167/183 | Product, performance, maintainer: optionality covered; decomposition proportionality missing (H5). |
| 023 | 052/053/054/159/168/169 | UX, accessibility, consistency: progress and connection views have substantial distinct coverage. No new UX hat identified. |
| 024 | 052/053/054/154/155 | Test, product: independent critique exists, but rubric provenance, anchors and general applicability need SR coverage (H2). |
| 025 | 148/156/157/170/171/172/174 | Operations, recovery: selection, ordering and bounded failure behavior covered. Sole-scheduler changes still require the plan's enabling amendment. |
| 026 | 154/155/175 | Operations, security, data protection, legal: routing covered; applicable lenses fail to reach the need/brief, and inclusion implementation is incomplete (H1/H6). |
| 027 | 144/148/156/170/177 | Operations, recovery, performance: bounded parallel lifecycle covered; utilisation evidence unfinished. Do not add an unapproved speedup promise. |
| 028 | 137/138, with 031's shared reader invariant | Consistency, security, adopter: declaration/refusal/migration covered. Need-only tags omit FIRST-RUN-ADOPTER despite the explicit migration subject; assess in H1's context reconciliation. |
| 029 | 049/139/140/148/178/179 | Security, integrity, test: authority/evidence obligations covered broadly; H7's stale carrier premise and the plan's snapshot-absorption concern remain. |
| 033 | 150 | Product: declared syntax check covered. A cell free of internal identifiers can still be incomprehensible; independent stakeholder-language review remains necessary. |
| 034 | 160 | Adopter, platform, accessibility: launcher actions/platforms covered; accessibility is a relevant question, not automatically another launcher SR. |
| 035 | 046 | Consistency, platform, UX: single capability inventory and action dispatch covered. |
| 036 | 161 | Test, all applicable lenses: SR text faithfully carries the need; injection and per-decomposition record incomplete (H1/H6). |
| 037 | 162 | Consistency, test: missing coordinated-change obligation (H3), plus signal-check implementation debt. |
| 038 | 163, with 166's materialization contract | Maintainer, adopter: purpose obligation stated; inventory mapping/completeness evidence unfinished (H6). |
| 039 | 164 | Consistency, adopter: scope obligation stated; schema/values/checking unfinished (H6). |
| 040 | 165 | Maintainer, product, test: partition alternatives/objective/ranking/human choice stated; record implementation unfinished (H6). |

## 4. Consequences for the redesign plan

1. **P0a/P1:** reconcile H1–H7 alongside the existing promise map. Review the
   proposed new hat and charter refinements before using them to derive new
   obligations. Vision objectives explain purpose; they do not replace hats.
2. **P1A:** land the missing/changed assurance obligations before enabling
   affected behavior. Retain existing SRs where the real gap is implementation.
   The interface-change and proportionality reviews can use ordinary reviewed
   artifacts; no requirement to mechanize their semantic judgment is implied.
3. **P2/P7:** compose scope/context once, carry applicable hat questions into
   actual briefs, and extend existing decomposition/review records. Verify
   considered-with-no-finding separately from not-applicable and not-recorded.
4. **P5/P10:** make the upgrading-adopter counterexample part of the real
   migration trial: upgrade a populated adoption, preserve accepted evidence
   and queued/unfinished work, exercise changed meanings and rehearse rollback.
5. **Metrics:** the new invocation contract is more specific than existing
   SR-177. Give it explicit normative coverage under the relevant existing
   need(s) and the reviewed PERFORMANCE lens; do not claim lane utilisation
   already commissions every token/cost field. Missing metrics stay visible
   without becoming an accidental new approval gate.

## 5. Evidence and limits

Read the live vision, all 27 SN need/acceptance cells, all 76 SR
requirement/acceptance cells, all 16 hat charters, relevant rationales and the
targeted LLR/TC/source seams above. The earlier
[derivation alignment](../plans/2026-08-16-derivation-alignment.md) was used
as historical corroboration after checking current text; it is not a fresh
independent derivation in this sitting.

`.venv/bin/python project-trajectory/scripts/hats.py --root . audit --strict`
passes: 10 hats always apply, 6 are conditional, no unknown need-tag tokens.
Conditional reach is adopter 10, unattended 5, platform 10, safety 0, legal 1,
data protection 2. Eleven needs activate no conditional hat but still receive
the ten unconditional questions. These counts measure routing, not adequacy.

A TOML join confirmed every current SN has at least one citing SR and every
SR parent ID resolves. Reading the normative cells, with a keyword search as
corroboration, found no SR-level rubric requirement or granularity/proportionality
clause. The `_hat_slots` probe in H1 checked actual brief composition without
any provider call or registry edit.

No live hats, needs, requirements, approval snapshots, queue rows or process
dials were changed. The preceding commit's hook checks passed; its smoke timing
exception remains scoped to that commit. This review does not claim new runtime
test coverage, complete implementation of the promised perspective record,
or a new independent adequacy verdict.
