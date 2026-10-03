# WI-782 adjudication: twenty approved rows amended by WI-771 (dropping the assumption evidence ladder)

Independent adjudicator: Claude Opus 5.5. I directed none of WI-771, WI-778 or WI-781.

**What I read.**
- The before/after cells the brief showed for all twenty rows.
- The owner's signed ruling of 2026-10-02, items 1 to 9, in WI-667. An assumption has status, standing and a falsifier, and no evidence level. Falsification is the one evidence-shaped signal, and a person or an adjudication sets standing. The accepted-risk reopen triggers stay.
- SN-043's current need and acceptance.
- PROCESS.md §3: the EARS openings and the decidable lint, the comparative and absolute rules, and ruling R2.
- The code behind the rows: `assumption_rules.py` (`falsification_worklist`, `accepted_risk_state`, `_UNBOUND_CELLS`, `release_gate_findings`, `assumption_chain`), `check_assumption_gate.py` and `traj_parse.need_assumptions`.
- The evidence behind the six TC rows: `tests/test_evidence_partition.py`, `tests/test_assumption_rules.py`, `tests/test_accepted_risk.py`, `tests/test_trace_briefs.py`, `tests/test_assumption_gate.py` and `tests/test_traj_views.py`.

**What I ran.**
- `trace.py --strict` on `d040ad75`. It exits 1 on LLR-292's pre-existing `minimal` finding alone. None of the twenty rows carries a form finding.
- A mutation probe: add `"Standing"` to `assumption_rules._UNBOUND_CELLS`. With that change a risk accepted while an assumption stood active still reads covered after it is recorded falsified. `tests/test_accepted_risk.py`, `test_assumption_gate.py`, `test_assumption_rules.py`, `test_observation_record.py`, `test_observation_writer.py` and `test_assumptions_registry.py` still PASS: 298 passed. The probe was reverted.
- A reverted trial of the fix required below:
  - The new test cases pass: `tests/test_assumption_gate.py` 16 passed.
  - The same probe now fails two of them.
  - With both replacement cells in place, `trace.py --strict` output is line-for-line unchanged: LLR-292's finding only.

## Per row

- [CLARITY] SR-191 Rationale -> "evidence about it is counted apart from evidence about the system's behavior" -> "the test cases that can show it false are counted apart" -> a rationale only. The obligation, a row of its own for each relied-on assumption, is unchanged. It is the same split, now named for what the cases can do.
- [CLARITY] SR-192 Rationale -> stand-in evidence "beside sparse evidence that the stand-in still matches" -> "beside the sparse samples whose failure shows the stand-in no longer matches" -> a rationale only. The surrogate row and its fidelity assumption are obliged exactly as before.
- [CLARITY] SR-197 Requirement, AcceptanceCriteria, Coincident, Rationale, Title -> accept a case that "evidences" assumptions in its own field, and count "assumption evidence" apart -> accept a case naming the assumptions "its failure shows false", and count those cases apart -> the same field, the same orphan, undeclared-reference and phase rules, and the same counted-apart set. Only the name of what the field means moved, and it moved to the ruling's.
- [CLARITY] TC-227 Expected -> "assumption evidence is counted apart from requirement evidence" -> "the test cases that can falsify an assumption are counted apart" -> the same clause of SR-197 and the same partition asserted.
- [CLARITY] SR-198 Requirement, AcceptanceCriteria, Rationale:
  - The obligation before: report or refuse an observation case's inputs, lifetime and sampling policy, the policy being required of a case that "evidences an assumption".
  - After: the same declarations, the policy required of a case that "can falsify an assumption".
  - The case set is the same: those naming an assumption. The floors, refusals and re-opening are identical. The rationale now says why a sampling model matters for recognising a failed sample.
- [CLARITY] SR-199 Coincident -> the record answers "whether a current result evidences it" -> it is "the record a failing observation is read from" -> the argument cell only, re-pointed at SN-043's amended need. What is recorded is unchanged: outcome, observer, expiry and judged digest.
- [CLARITY] SR-201 Requirement, AcceptanceCriteria -> report on a falsified assumption, or on a failing result "evidencing it", listing the cases "evidencing it" -> the same triggers and report, the cases named as those "that can show it false" -> the same cases (those naming it in `Assumption-Refs`), the same trigger and the same advisory-until-gated rule.
- [CLARITY] LLR-238 Detail -> the worklist takes an assumption whose latest record "for any evidencing case" failed -> "for any case that can falsify it" -> the same set of cases. It matches `falsification_worklist` as built.
- [CLARITY] TC-233 Method -> "two evidencing cases" -> "two cases that can falsify it" -> the same fixture and the same assertions.
- [MEANING] SR-202 Requirement, AcceptanceCriteria:
  - Before: unproven until the risk is accepted again "or current evidence arrives". Covered only "with no current evidence". A current passing result restores coverage.
  - After: covered whatever the results. A passing result "restores nothing". Only a reviewed re-acceptance restores coverage.
  - An implementation correct under the old text, restoring coverage on a passing result, fails the new text. I would bless it: it is ruling items 2 and 6 exactly.
- [MEANING] TC-234 Expected, Method -> a reviewed re-acceptance "or a current passing result" restores coverage -> a re-acceptance restores it and "a passing result does not" -> the restoration check is inverted. `_restorations` asserts the inverted check (passing observation -> still `unproven`). I would bless it.
- [MEANING] SR-203 Requirement, AcceptanceCriteria, Coincident, Rationale -> the brief shows each assumption's "evidencing test cases with its current evidence level" -> it shows "the test cases that can show it false … with no evidence level" -> a brief correct under the old text, which printed a level, fails the new one. I would bless it: `trace.py` renders "**Can be falsified by.**" and no level.
- [MEANING] LLR-240 Detail -> `assumption_chain` gathers "its evidencing cases with the current evidence level" -> the cases naming it in `Assumption-Refs` "with no evidence level" -> the level was dropped from the chain. It matches `assumption_chain`, which reads no result. I would bless it.
- [MEANING] TC-235 Expected, Method -> assert each assumption's "evidence level" in order -> assert "Can be falsified by", with no evidence level and no "Evidenced by" line -> the asserted content is inverted. `test_an_assumption_leads_with_its_citing_requirements_and_needs` and `test_no_assumption_shows_an_evidence_level` assert it. I would bless it.
- [MEANING] SR-206 Requirement, AcceptanceCriteria, Coincident, Rationale, Title:
  - Before: release fails each relied-on assumption lacking a current passing result of its declared kind (sampled only under a declared model) and lacking an unreopened accepted risk.
  - After: release fails each relied-on assumption recorded falsified and not covered by an unreopened accepted risk. An active one passes whatever its results.
  - The gate is replaced. I would bless it: ruling item 1, with R2 held and the EARS Optional-feature opening.
- [MEANING] LLR-243 Detail -> `release_gate_findings(das, srs, levels, risks, tcs)` fails on a missing monitored or sampled level -> `release_gate_findings(das, srs, risks)` fails a falsified assumption not covered, and Standing is a bound cell of the accepted risk -> the rule is replaced. NOT BLESSED as it stands; see the return below.
- [MEANING] TC-238 Expected, Method, and the routed pointer `Verifies` (+IF-216) -> monitored, automated or sampled-under-model evidence passes -> an active assumption passes whatever its results; a falsified one passes only under an unreopened risk -> the asserted gate is replaced. NOT BLESSED as it stands; see the return below. IF-216 is a sound addition: TC-238's Method asserts the `observation_evidence_findings` composition that IF-216 declares.
- [MEANING] SR-218 Requirement, AcceptanceCriteria, Coincident, Rationale, Title -> the per-need view shows each assumption's "validity and evidence level", and marks one "relied on with no current evidence" -> it shows status, validity, falsifier and the cases that can show it false, marks only a falsified one, and shows no level -> a view correct under the old text fails the new one. I would bless it, against SN-043's amended acceptance ("its approval status and whether it has been shown false").
- [MEANING] LLR-258 Detail -> `need_assumptions` carries "its evidence level from assumption_rules.evidence_level", and an unevidenced premise is labelled -> it carries status, standing, falsifier and the cases naming it, with no level -> the derived fields changed. It matches `traj_parse.need_assumptions`. I would bless it.
- [MEANING] TC-251 Expected, Method -> assert the evidence level, and a label for "one with no current evidence" -> assert status, standing, falsifier and falsifying cases, with no evidence level or label -> the assertions are inverted. `test_each_need_s_detail_lists_its_assumptions_with_their_standing` asserts them. I would bless it.

## Returned for a fix in this lane (owner direction S11, 2026-10-03)

Two rows are not blessed: LLR-243 and TC-238. The other eighteen I would re-attest as they stand. No `## Dispositions` row is drafted and no act is taken: the fix is applied in this lane, and I re-judge only these two rows before taking the one combined act.

**Finding 1 (LLR-243 and TC-238): the new release gate's load-bearing clause is unverified.**
- LLR-243 now states: "Standing is among the cells an accepted risk is bound to, so a risk accepted while the assumption stood active reopens once it is recorded falsified".
- That clause stops a risk accepted on an active premise from silently waving through its later falsification. Under SR-206's new gate, it is the only thing between a falsified relied-on assumption and a green release.
- No test pins it. Every accepted risk in TC-238's fixtures was accepted while its assumption already stood falsified. TC-234 reopens only on the `Assumption` cell, a need, or a late failure.
- The probe above, adding `Standing` to `_UNBOUND_CELLS`, survives the whole assumption suite.

**Finding 2 (LLR-243): the Detail contradicts itself on what the gate reads.**
- It says "no result, inputs digest or suite record is read", then that the step reads "the observation records".
- An observation record is a result. Its one use, a failing sample reopening a risk, is the SR-202 trigger that TC-238 itself asserts.
- A builder taking the first sentence literally drops the records and loses that trigger. The relative clause "cited by at least one requirement whose standing reads falsified" also attaches standing to the requirement.

**Fix 1: replace LLR-243 `detail` with exactly this text (one line in the TOML string):**

```
release_gate_findings(das, srs, risks) fails each assumption that at least one requirement cites and whose standing reads falsified, unless its accepted risk reads covered by accepted_risk_state; each failure names the assumption, the requirements relying on it and either that it records no accepted risk or the triggers that reopened its risk. An active assumption passes whatever results it has or lacks. The rule itself reads no result, inputs digest or suite record: an observation record reaches it only through an accepted risk's reading. Standing is among the cells an accepted risk is bound to, so a risk accepted while the assumption stood active reopens once it is recorded falsified, and covers it only when accepted again. check.py gains a built-in step `assumption-evidence` at the DevStg-Release threshold, gated by the same setting; the step reads the observation records and each accepted risk's approval act to compute those readings. The stage's single release producer, the harness evidence verdict, is left untouched.
```

**Fix 2: replace TC-238 `method` with exactly this text (one line in the TOML string):**

```
The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow, and its rule called on in-memory rows. A relied-on assumption whose standing is active passes with no result at all, and also beside a failing observation no person has acted on. A falsified one with no accepted risk fails; one whose accepted risk, accepted while it stood falsified, still stands passes; one whose risk has reopened, by an edit to its text, by a failing sample recorded after the act, or by its being recorded falsified after an act that accepted the risk while it stood active, fails naming the trigger. Each failure names the assumption, the requirements relying on it and that it is falsified. The risk is read through the observation rules' accepted_risk_state, the reading the checker's reopened-risk advisory composes, and that composition (observation_evidence_findings) reports no assumption for lacking a result and reports a failing record as the one signal. With the setting off the same cases are advisories. A project declaring no frame is judged the same way. The step lists at the DevStg-Release threshold, and the approval-level pin on the single release producer still holds.
```

No other cell of either row changes. Every other row's `Status` stays `Approved`.

**Fix 3: the test assertion, in `tests/test_assumption_gate.py` (TC-238's evidence).**
- Tests affected: `test_the_release_step_fails_each_falsified_assumption_no_standing_risk_covers` and `test_the_release_step_is_advisory_with_the_gate_off`, through their shared fixture.
- The change:
  - Add DA-007, which is active with an accepted risk in the acceptance act, and SR-007, which cites it.
  - After the act, flip DA-007's `standing` to `falsified`.
  - Expect one FAIL (gate on), or one ADVISORY (gate off), naming DA-007, "falsified", "reopened" and "Standing changed since the act".
- The existing `len(lines) == len(RELEASE_FAILURES)` check then also pins that DA-007 fails exactly once.
- Exactly this diff:

```diff
@@ -527,7 +527,8 @@ def test_the_arms_list_at_their_rungs_and_the_stage_fold_takes_no_interface(
 # no accepted risk; DA-004 falsified under a risk accepted in the act that
 # still stands; DA-005 falsified under a risk reopened by an edit to its text
 # after that act; DA-006 falsified under a risk reopened by a failing sample
-# recorded after it.
+# recorded after it; DA-007 active when its risk was accepted, then recorded
+# falsified after the act, which reopens that risk (Standing is a bound cell).
 
 RELEASE_DAS = (
     _assumption("DA-001")
@@ -536,10 +537,11 @@ RELEASE_DAS = (
     + _assumption("DA-004", standing="falsified", accepted_risk="Ship it anyway.")
     + _assumption("DA-005", standing="falsified", accepted_risk="Ship it anyway.")
     + _assumption("DA-006", standing="falsified", accepted_risk="Ship it anyway.")
+    + _assumption("DA-007", accepted_risk="Ship it anyway.")
 )
 
 RELEASE_SRS = "".join(
-    _requirement("SR-00{}".format(i), da=["DA-00{}".format(i)]) for i in range(1, 7)
+    _requirement("SR-00{}".format(i), da=["DA-00{}".format(i)]) for i in range(1, 8)
 )
 
 
@@ -577,6 +579,7 @@ RELEASE_FAILURES = {
     "DA-003": ("falsified", "no accepted risk"),
     "DA-005": ("falsified", "reopened"),
     "DA-006": ("falsified", "reopened", "failed after the act"),
+    "DA-007": ("falsified", "reopened", "Standing changed since the act"),
 }
 
 
@@ -642,6 +645,16 @@ def _release_repo(scaffold, gate):
         encoding="utf-8",
         newline="\n",
     )
+    text = da.read_text(encoding="utf-8")
+    marker = "[assumption.DA-007]\n"
+    head, tail = text.split(marker)
+    da.write_text(
+        head
+        + marker
+        + tail.replace('standing = "active"', 'standing = "falsified"', 1),
+        encoding="utf-8",
+        newline="\n",
+    )
     for tid in ("TC-002", "TC-006"):
         _observe(root, tid, outcome="fail")
     return root
```

- **Probe it must make fail:** in `project-trajectory/scripts/assumption_rules.py`, change `_UNBOUND_CELLS = frozenset({"DA-ID", "Status", "AcceptedRisk"})` to also hold `"Standing"`. Both tests above must FAIL. Revert the probe after.
- **Bar for the fix commit:**
  - `tests/test_assumption_gate.py` and `tests/test_assumption_rules.py` pass.
  - `trace.py --strict` shows only LLR-292's pre-existing finding.
  - The smoke commit bar passes.
- No production code changes: the code already binds `Standing`. Only the row text and the test move.

## Out of scope, noted, not withholding

- **SR-202 still says "unproven".** Its cells and `RISK_UNPROVEN` keep that word for a reopened risk. Under the ruling no assumption is ever proven, so the word reads like a residue of the evidence ladder. The SR defines the term (covered versus unproven), so the obligation is closed. A rename would be a later amendment.
- **TC-227 `method` still says the census and report "count assumption evidence".** WI-771 already logged this follow-up, and it is tied to the `assumption_evidence_rows` symbol.
- **SR-191 versus SR-206 on projects with no frame.** SR-191's rationale says the tier "applies only where a frame is declared". SR-206's gate, and TC-238 explicitly, judge a project with no frame too. The behaviour predates WI-771. The two rows should say which one governs.
- **IF-216 `requestors` omits `scripts/check_assumption_gate`.** That script calls `accepted_risk_state`, one of the calls IF-216 declares.

First sitting's machine line, superseded by the re-judgement below: VERDICT MEANING rows=20.

## Re-judgement after fix round 1 (fea1b8f3), 2026-10-03

Re-judged on the lane at `fea1b8f3`: LLR-243 and TC-238 only. The other eighteen rows' rulings above stand unchanged.

**What I checked myself.**
- **The cell text:**
  - I parsed the registries at `fea1b8f3` against `d040ad75`.
  - LLR-243 `detail` and TC-238 `method` are byte-identical to Fix 1 and Fix 2 in this file.
  - No other cell of any LLR or TC row moved, and no `Status` moved.
- **The test change:** the `+`/`-` lines of `tests/test_assumption_gate.py` between `d040ad75` and `fea1b8f3` equal Fix 3's diff exactly.
- **The suites:** `tests/test_assumption_gate.py`, `tests/test_assumption_rules.py` and `tests/test_accepted_risk.py` gave 195 passed.
- **The probe:**
  - I added `"Standing"` to `_UNBOUND_CELLS`.
  - `test_the_release_step_fails_each_falsified_assumption_no_standing_risk_covers` and `test_the_release_step_is_advisory_with_the_gate_off` FAILED, each on DA-007 with no finding naming "Standing changed since the act".
  - I reverted the probe, and the tree is clean.
- **The lint:** `trace.py --strict` reports only LLR-292's pre-existing `minimal` finding, and nothing on LLR-243 or TC-238.

- [MEANING] LLR-243 Detail -> before: `release_gate_findings(das, srs, levels, risks, tcs)` fails a relied-on assumption lacking a monitored or sampled level and an unreopened risk -> after (fix round 1):
  - It fails each relied-on assumption whose standing reads falsified unless its accepted risk reads covered.
  - Each failure names the assumption, the requirements relying on it and why.
  - The rule reads no result itself. Records reach it only through a risk's reading, which the step computes.
  - Standing is a bound cell, so a risk accepted while the assumption was active reopens when it is falsified.
  -> the gate is replaced, so this is meaning. The Detail is now closed and consistent, and matches `release_gate_findings`, `_UNBOUND_CELLS` and `check_assumption_gate._evidence_findings`. BLESSED.
- [MEANING] TC-238 Expected, Method, Verifies (+IF-216) -> before: monitored, automated, or sampled-under-model evidence passes -> after (fix round 1):
  - An active assumption passes whatever its results.
  - A falsified one passes only under an unreopened risk.
  - A risk reopened by a text edit, a late failing sample, or a falsification after an act that accepted it while active fails, naming the trigger.
  -> the asserted gate is replaced, so this is meaning. The newly stated case is now asserted (DA-007), and the probe shows it bites. BLESSED.

All twenty rows are now blessed, and the re-attestation is taken in the one combined act with WI-783.

The re-judgement's machine line, superseded below: VERDICT MEANING rows=20.

## The three retirements (carried in 2026-10-03)

The coordinator carried these three rows into this sitting at `01230d18`. Intake's amendment walk iterates only rows still present in the live registry, so a removal never mints. I judged each as a removal: is retiring it right, and does its successor carry whatever of its obligation survives? I read:
- the last approved text of each row in `docs/archive/last_approved`;
- the retirement records in `docs/log.d/retired/`;
- the owner's 2026-10-02 ruling, items 1, 2 and 6;
- the successors' live text.

`git grep` finds no live registry cell, script or test citing any of the three. The only remaining mentions are history: plans, ratify records, the RESYNC entry, the handoff, the retired-rows table and WI graph on the generated dashboard, and this row's spec. `check_trajectory` notes the two WIs (WI-632 and WI-771).

- [MEANING] SR-200 (removed) -> before: the harness derives an assumption's evidence level (assumed, specified, monitored or sampled) from current results alone, and reports an approved, active assumption reading assumed or specified -> after: no such obligation; the row is retired, and SR-201 reports falsification -> ruling item 1 drops the ladder and any rule needing current evidence, so nothing of SR-200's obligation survives to be carried. Its one surviving principle, that a result never sets standing, is SR-201's acceptance: "a failing observation result is reported as falsification evidence without changing the assumption's validity cell". The re-judge freshness it shared (expiry or a changed judged state) is SR-215's own obligation. Retirement BLESSED.
- [MEANING] LLR-237 (removed) -> before: `evidence_level`, `result_current` and `tier_covers` derive the level, and an approved-but-unevidenced advisory is raised -> after: none of these exist (`test_no_evidence_level_is_declared_or_computed` pins their absence), and LLR-238's worklist carries the falsification signal -> follows SR-200's retirement. Its "never sets the standing cell" lives on in LLR-238 ("never writes the standing cell"). Retirement BLESSED.
- [MEANING] TC-232 (removed) -> before: table-driven assertions of the four levels, the tier contract and the unevidenced advisory -> after: none; TC-233 verifies SR-201 and LLR-238, including the standing cell left unchanged -> a case for a retired obligation has nothing left to verify. TC-233 covers what survives. IF-216, which it also verified, is now verified by TC-238. Retirement BLESSED.

All twenty-three rows are blessed. They are re-attested in the one combined act with WI-783.

VERDICT: MEANING rows=23
