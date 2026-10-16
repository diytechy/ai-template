# WI-911 adjudication 010: amendment checkpoint at cdcd10ee2

I judged the ten amended rows on the text at `cdcd10ee2`, reading their chains in the live registries and checking the trace homes against the code. The SR, LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **Tests:** every `Evidence` test of TC-069, TC-332, TC-333 and TC-334 exists, and every test a Method names is in its Evidence.
- **Tiers:** TC-334 cites `tests/test_dispute.py`, which `tests/conftest.py` lists in `SLOW_MODULES`. The evidence of TC-069 and TC-332 is all fast.
- **Code:**
  - `kitlib/dispute.py` declares `RULINGS = ("FIX", "SUCCESSOR", "DISMISS", "ESCALATE")`, the order LLR-314 states.
  - `plan_coverage.py` resolves a rework exclusion through `RESOLVING = ("DISMISS", "SUCCESSOR")`, while the plan-cap path stays DISMISS-only, as LLR-069 states.
  - The dispute template rules out SUCCESSOR for "a fail-open path, data loss or a gap in the work item's Done-when".
- **Owner text:** commit `01614b9df` is the owner's text fix (D-016, D-017) behind the reachability, contrived-scenario and promise-bound clauses. I judge the resulting cells, not that ruling.

## amendment

- [MEANING] LLR-313 Detail -> attended review and critique rendering and filing, the single-plan briefs and the plan-critique rules -> it adds:
  - a review stance (ordinary by default with no stance line, or convergence with one fixed line after the range, refusing a narrow scope or an unknown stance);
  - distinct reading scopes (ordinary reads the decisions record and filed plan critiques, convergence excludes both and refuses a template lacking the exclusion exactly once);
  - the scope critique naming five declared registries and marking an absent one, from the set the single-plan brief shares;
  - plan-critique severity tied to normal-use reachability, and a confirming-round gate on BLOCKER or MAJOR;
  - a convergence-tagged finding counted as one finding.

  New behaviour and refusals. **Blessed.** Its parents SR-146 and SR-235 (attended briefs and records) call for the rendering arms. The additions name no implementation carrier. TC-333's new Expected clauses verify each arm.
- [MEANING] TC-333 Expected and Method -> verify the attended renders, filing, the plan briefs and the plan-critique cap -> it adds: five registries with only an absent one marked; matching ordinary and absent-stance output with no stance line; one convergence line; narrow convergence refused; distinct reading scopes; a tagged finding filed as one; no plan-cap pass record on SUCCESSOR; the plan-critique reachability gates -> new verification obligations. **Blessed.** It is closed over LLR-313's new arms, and every cited test exists.
- [MEANING] LLR-069 Detail -> an F# exclusion citing a dispute verdict resolves only on an accepted DISMISS of the same finding -> an accepted DISMISS **or SUCCESSOR** resolves it. The plan-cap condition stays DISMISS-only, and a refusal for another ruling names both resolving rulings -> the resolving set widened. **Blessed.** It matches `plan_coverage.RESOLVING` and SR-236's amended text, and it keeps the cap DISMISS-only.
- [MEANING] TC-069 Expected and Method -> verify exclusion resolution on an accepted DISMISS -> it adds: an accepted SUCCESSOR of the same finding resolves; one of another finding or round, or an unaccepted one, does not; refusals name both resolving rulings -> new cases. **Blessed.** These are the exact arms of LLR-069's change.
- [MEANING] SR-233 AcceptanceCriteria -> the review scope's normal-environment boundary, one definition, a recorded one-line dismissal, and briefs that cite it -> it adds: review directions tie every severity class to supported-route reachability; a contrived scenario is defined; a mislabelled BLOCKER or MAJOR is re-graded; a specification promise is bounded to supported routes; dispute directions weigh plausibility; an out-of-set input is classified by fail-closed or fail-open; the convergence review's confirmations, tags and reachability gate -> new acceptance conditions. **Blessed.**
  - Each clause makes concrete the Requirement's "limit findings to defects reachable in a normal working environment". The convergence clauses limit new findings by the same reachability test.
  - The clauses are stated as directions or ruling-party acts, the form the row's approved text already uses ("the party that rules ... records its dismissal"). LLR-311 decomposes them, and TC-332 checks the shipped directions.
  - Being in the SR registry, it is left unanchored behind SR-234 (aftermath).
- [MEANING] LLR-311 Detail -> the §6 threat-model paragraph and the briefs citing it -> it adds: the reachability-tied severity directions; the contrived-scenario definition, including the forbidden hand acts; the re-grade; the promise bound; the out-of-set classification; Done-when and regression review in every stance; the convergence-only reading and confirmation rules and BLOCKER or MAJOR tagging; dispute plausibility; no SUCCESSOR for a convergence-class finding -> new direction content. **Blessed.** It decomposes SR-233's amended AC clause by clause, names only the shipped doc section it cites, and TC-332 verifies each clause.
  - **Note for the SR-234 rework below:** its SUCCESSOR bound is a dispute-ruling constraint. If SR-234 comes to state that bound, LLR-311 should add SR-234 to its SR-Refs, so the bound decomposes from the row that owns rulings.
- [MEANING] TC-332 Expected and Method -> verify the §6 paragraph's phrases, the citing briefs, and that no prompt copies the boundary examples -> it adds checks that the shipped directions dismiss contrived scenarios, gate every class on reachability, re-grade, bound the promise, weigh plausibility, and carry the classification, convergence and SUCCESSOR-bound clauses -> new verification obligations. **Blessed.** Its two named tests exist, and it is closed over LLR-311's arms.
- [MEANING] SR-234 Requirement and AcceptanceCriteria -> a contested or third-round finding is preserved and ruled exactly once as a fix, a reasoned dismissal or an escalation -> "a successor row" joins the ruling set; the AC adds that a SUCCESSOR has a reason, an unknown ruling names the set, and "the dispute sitting never selects SUCCESSOR for a fail-open, data-loss, or Done-when-gap finding" -> a new ruling and a new constraint. **Not blessed,** for one clause. The SUCCESSOR addition to the ruling set and its reason rule are sound.
  - **The Requirement does not state the bound.** "the dispute sitting never selects SUCCESSOR for a fail-open, data-loss, or Done-when-gap finding" restricts which verdicts are acceptable. The Requirement admits a successor row with no restriction.
  - **No child under SR-234 decomposes or verifies it.** LLR-314 (the parser) accepts SUCCESSOR for any finding. TC-334 does not check the bound. The only checks are LLR-311's direction clause and TC-332's text assertion, both under SR-233.
  - **It reads as a guarantee about a judge's output** ("never selects"), but only shipped directions back it.

  This is the protection against deferring the very class of finding the convergence work exists to keep in the lane, so its record must say honestly what holds it.
- [MEANING] LLR-314 Detail -> the parser accepts only FIX, DISMISS or ESCALATE rulings with reasons, DISMISS taking a declared class -> it adds SUCCESSOR as a fourth ruling (a reason, no class), with an unknown-ruling refusal naming FIX, SUCCESSOR, DISMISS and ESCALATE in that order -> a widened ruling set. **Blessed.** It matches `kitlib/dispute.RULINGS`, and the addition names no implementation carrier. It stays correct whichever way SR-234's bound is homed, because the bound is not a parser rule today.
- [MEANING] TC-334 Expected, Method and Tier -> verify the dispute brief, findings refusals, verdict parsing and the entry point, at Smoke -> it adds: a reasoned SUCCESSOR accepted and bound at the entry point, and a reasonless SUCCESSOR or an unknown ruling refused; the tier moves to Full -> new cases, and a tier claim under which evidence could leave the commit floor. **Blessed.** The new tests (`test_a_successor_ruling_is_accepted_and_parsed`, `test_an_unknown_ruling_is_refused_naming_the_four_rulings`, `test_a_dispute_verdict_ruling_a_finding_successor_is_valid_and_bound`) exist. `Full` is honest, because `test_dispute` is slow-only.
- [MEANING] SR-236 Requirement and AcceptanceCriteria -> a dispute-ruling exclusion resolves a finding only on an accepted dismissal of that same finding -> an accepted dismissal **or successor ruling** of that same finding resolves it, and a ruling of another finding or round, or any other ruling, is refused -> the resolving set widened. **Blessed.** It follows from SUCCESSOR being a ruling that moves a finding out of the lane, and LLR-069 and TC-069 decompose and verify it. Left unanchored behind SR-234 (aftermath).

VERDICT: MEANING rows=10

**Aftermath:**
- **Re-attested by this session:** the eight blessed LLR and TC rows, in their own act commit: `python project-trajectory/scripts/intake.py snapshot --reattests LLR-069,LLR-311,LLR-313,LLR-314,TC-069,TC-332,TC-333,TC-334`.
- **Blessed but left unanchored:** SR-233 and SR-236. SR-234's drift holds the SR registry, and the copy takes it whole.
- **Not blessed:** SR-234.

**Advisory:** no spine row obliges the successor row a SUCCESSOR ruling promises. The spec's Trust section puts its filing in the coordinator's landing procedure. If that obligation should be attested rather than procedural, it needs a home.

## Dispositions answered in the lane (decisions D-018; re-sat at sitting 011)

```toml
title = "WI-911 spine rework: SR-234 states its SUCCESSOR bound where a child can verify it (answer checkpoint 010)"
workstream = "process"
sr_refs = ["SR-234", "SR-233"]
needs = ["WI-911"]
safety_class = "ordinary"
buildtier = "medium"
```

Spine text only; no code change is called for.

1. Move the SUCCESSOR bound from SR-234's AcceptanceCriteria into its Requirement, stated as what the delivered adjudication content does. For example, its directions rule out a successor row for a fail-open, data-loss or Done-when-gap finding. In the AC, keep the observable condition: the shipped dispute directions carry that bound.
2. Give the bound a verifying child under SR-234: add SR-234 to LLR-311's SR-Refs, or state it in LLR-314. Have TC-334 assert the dispute directions' bound, or cite TC-332's check.
3. Re-sit SR-234 together with SR-233 and SR-236, which this sitting blesses as they stand. They are unanchored only because SR-234 holds the SR registry.

SITTING: JUDGED kinds=amendment
