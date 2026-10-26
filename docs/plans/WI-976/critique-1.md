Reviewed: 90d29557a5986007c16d1a3b2b687bb9dafa0a19

## 2026-10-25 — WI-976 single-plan critique, round 1

Reviewer/session: Codex, this fresh independent non-author critic session, invoked for pcrit1 by the coordinator. This session produced neither the plan nor the work-item spec. No provider session id was supplied. Recording route: the assigned verdict file only; no commit, as the invocation explicitly directs.

Artifact: docs/plans/WI-976/plan.md, read with git show at the Reviewed commit. Intent sources: the complete docs/work/active/wi-976/WI-976-retire-perspective-sidecar.md and its specref, docs/plans/2026-10-11-review-churn/README.md item 14, at that commit; SN-036 and SR-161 at the specified contract_split tip 961f9e47; SR-186's unchanged independent-purpose obligation as carried by the spec and TC-211 procedure. The supplied coverage report is the coverage input. No implementer session notes, docs/status.md, docs/log.md, or neighboring plan critiques were read.

Rubric: docs/rubrics/plan-decomposition.md at 90d29557a5986007c16d1a3b2b687bb9dafa0a19, blob 4f183eb6aa17a459c9b0741391791d03a8f76293 (last changed by 247dc36c46a6536f3586cc241b231151b5692a93).

Rubric derivation: independently compared the anchors with the supplied intent before scoring. DevStg-Tests and B2 test whether retirement, computed questions, recorded outcomes, inspection evidence and the owner-held act are actually delivered; DevStg-Reqs tests executable steps; DevStg-Impl/B3 test the split; G4/B4 test the required record/text/build/sitting/act/inspection order; B1 and the single-plan DELTA question test the changed input and existing seams. These cover the supplied intent without substituting a permissive TC for it; no missing anchor is proposed.

Transfer caveat: the debate/selection evidence comes from QA, math and code with objective verifiers. It has not benchmarked plan artifacts, and reconciliation evaluated for plan quality remains an open research gap. This rubric is an extrapolation, not a proven instrument.

Anchors judged: DevStg-Reqs, DevStg-Tests, DevStg-Impl, G4, B1, B2, B3, B4. The 12 steps have concrete deliverables; the retirement, roster/test split, optional slots, combined composition, outcome-parser invariance, owner act and downstream notice have substantive planned work. TC-198's exclusion is honest because its staging arm remains unchanged. The repeated coverage has identifiable intent/test/build/inspection seams. DELTA: within is supported: the plan identifies the new roster/parent input, places the call inside CMP-008, carries the flow change and IF-133 deletion, and preserves the existing composition/refusal contract. The finding below concerns the planned evidence after a supported re-sit, despite nominal 35/35 clause coverage.

- [MAJOR] DevStg-Tests -> docs/plans/WI-976/plan.md P9 step 6, consumed by P11: the unconditional instruction to move TC-211's inputs to the re-sit's B and V loses the required decomposition-round sample on a normal supported RETURN. For example, the combined checkpoint accepts the SN/SR amendments but returns the new LLR or TC; P9 correctly re-sits that row alone, but P5 explicitly gives an LLR/TC-only sitting NOT_A_ROUND, with no hat questions or outcomes. Replacing the sample with that brief/verdict makes P11's question/outcome inspection unable to satisfy D26/D27 and SR-161, costing another review round. -> Keep the actual decomposition-round brief/verdict as the sample and include any narrow follow-up reviews needed to establish the completed chain; replace the sample only with a sitting that itself meets the decomposition-round and per-hat evidence conditions. Make P9's re-sit instruction and P11's input selection agree. -> @planner

VERDICT: CHANGES-REQUESTED findings=1
