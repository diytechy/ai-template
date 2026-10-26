Reviewed: 14f786d1a5291ae5bca2739ae0b798d1656bd5e0

Verified: Hunted silent omission or over-inclusion of hats first, then fail-open composition and loss of retirement evidence. Exercised the shipped composer against the live lane and fixture repositories, the real author-prompt CLI, verdict parsing, and the removed command. No actionable defect was confirmed. The changed spine is coherent with the owner ruling and rubric K1–K3/B1; this verdict judges the scoped diff and does not certify the later owner act or TC-211 observation.

Commands:
- `git rev-parse HEAD` -> `14f786d1a5291ae5bca2739ae0b798d1656bd5e0`.
- `git status --short` (initial and subsequent checks) -> no tracked changes.
- `git diff aa36a5b6e2bc47fe9960bbc4a0727c04c9571f36...14f786d1a5291ae5bca2739ae0b798d1656bd5e0 -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ':(exclude)docs/decisions' ':(exclude)docs/plans/*/critique-*' ':(exclude)docs/log.md' ':(exclude)docs/log.d' ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'` (stat and scoped path reads) -> 49 files; retirement, shared composition, prompt integration, requirement/procedure changes and shipment wiring reviewed.
- Scoped `Get-Content`, `rg`, and `git show` reads -> read the guide, process, WI spec, specref item 14 and its quoted owner ruling at 961f9e47; swept cited and related registry rows; checked status against declared policy; inspected the removed tests and producer. No contradictory historical requirement found. Live-sidecar search returned no surviving sidecar producer or instruction outside the expressly allowed RESYNC notices; generic unrelated `record_findings` symbols were discounted.
- `git log -p --format=%h aa36a5b6..14f786d -- project-trajectory/scripts/plan_briefs.py scripts/coordinator/mkprompt.py project-trajectory/scripts/amendment_brief.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_plan_briefs.py` -> inspected fix history under hashes only, without commit messages.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt/review-tmp/2026-10-25c-leg21` and `PYTHONDONTWRITEBYTECODE=1`: `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-25c-leg21/reva/wi-976 tests/test_plan_briefs.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_hats.py tests/test_dogfood_sync.py tests/test_spine_carrier.py tests/test_trace.py tests/test_trace_hats.py tests/test_coordinator_adjudicate.py tests/test_import_layers.py tests/test_integrate_admission.py tests/test_bootstrap.py tests/test_brief_egress_conventions.py tests/test_baseline_snapshot.py tests/test_module_size_ratchet.py` -> `792 passed, 2 skipped in 700.64s (0:11:40)`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (973 work item(s), 863 done (89%), 34 cancelled, graph acyclic).` Advisory output omitted.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 drafts=2 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md`.
- Scratch `probe.py` -> current retirement, mixed amendment parents, combined parents and author/sitting agreement all PASS. Substituting the actual pre-fix amendment module from 7d9f4143d^ makes the removed-TC regression fail at its assertion. Substituting the actual pre-fix composer/applicability modules from 49a47d3b5^ makes both mixed-parent regression tests fail at their question assertions. An initial scratch reporting error on an empty assertion message was corrected before completing these probes.
- Scratch `author-red.py` -> the current extra-parent regression fails against the actual pre-fix mkprompt.py from 49a47d3b5^: the author prompt incorrectly contains the unrelated need-b question. The prescribed suite passes its current implementation. The author/sitting agreement characterization also passes with the older writer when no unrelated parent is present, as expected.
- Scratch `live-flow.py` -> `live-lane combined compose: PASS; one perspectives block; all computed questions; LLR-297 and TC-312 removal evidence; 10 bound identities`; `live-lane slot-free combined override: PASS; no injected tail`; `retired record CLI: exit 2 (invalid choice)`. The first scratch assertion used a mistaken literal removal marker; correcting it to the product's declared marker produced these results.
- Read-only Python registry/byte inspection -> SR-161's children are LLR-183, LLR-202 and LLR-360; PROCESS.md 98,185 -> 97,962 bytes (-223), byte-budget skill 4,519 -> 4,523 (+4), matching their stamps.

Done-when coverage (items numbered in the spec's order):
1. Ruling-fragment commit precedence: UNCOVERED; current process records are excluded from this review.
2. SN-036/SR-161/LLR-183/TC-178/TC-211 meaning: verified by scoped row comparison with the quoted ruling and procedure; actual completed-sample judgment is item 22.
3. LLR-297/TC-312 retirement: deletions and live-lane removal briefing verified; retirement-record/sitting authority UNCOVERED in the excluded records.
4. New LLR/TC: LLR-360 and TC-399 present and coherent; executable coverage passed; authority remains a later act (both are Drafted).
5. IF-133: `load` removed; retained reader operations still belong to the roster reader.
6. Inspection procedure and historical INCOMPLETE: corrected text verified, with history retained.
7. Rubric R1/B1: outcomes replace producer evidence; R2/R3/B2 retain independent child purposes.
8. Record command, module tests and exclusive symbols/imports: removed; actual CLI refuses the command.
9. Redesign sidecar and pointer: deleted in the diff.
10. Process, c3, roster headers and three recipe copies: corrected text and dogfood/prompt tests.
11. SAFETY: live/template pins and applicability tests passed; live roster removes it, template retains it.
12. Live references: scoped search and CLI-reference diff; excluded generated owner views were not independently re-rendered.
13. Round eligibility: first-approval SR, amended SN, SR-only amendment and LLR/TC-only tests drive compose; other template classes remain slot-free.
14. Applicability: parent-specific, WI-widened and sibling-conjunction cases; mixed-parent red-before probes and live composition.
15. Optional slots: template pins, real override composition and malformed-roster override test.
16. Combined questions once: real combined compose and union tests; the sample verdict's authored outcomes are UNCOVERED (item 21).
17. Absent/malformed roster: opt-out and refusal tests, including compose's named refusal.
18. Hat outcome parsing: amendment, first-approval and combined verdicts preserve parsed rulings and authorized rows.
19. Spine-author prompt: actual mkprompt subprocess tests, exact-parent test, author/sitting agreement, dispatch/recipe pins.
20. Tests/prompt pins: prescribed test run passed; new behavior tests drive the named interfaces. Existing characterization tests remain meaningful; deleted tests solely exercised the withdrawn sidecar. Structural import, catalogue and shipment pins support the behavioral tests.
21. Committed checkpoint brief and per-hat verdict outcomes: UNCOVERED because those records are excluded from the reading scope; composing the equivalent live-lane population succeeded.
22. Fresh post-act TC-211 inspection/observation: UNCOVERED; the procedure currently records historical results, not this required new observation.
23. Owner's SN-036 act: UNCOVERED; not inferred from unchanged Approved status or a test pass.
24. Headless stop/other acts/handoff: UNCOVERED in excluded process records; the spec expressly reserves the owner act.
25. No landing before owner act/return handling: the lane remains active; actual authority/landing evidence UNCOVERED. This review grants no substitute authority.
26. RESYNC: retirement failure, inert notes, optional overrides and stale preserved header all stated; new amendment module included in overwrite/shipment wiring.
27. Generated pages/catalogue/budget: catalogue and bootstrap/dogfood pins passed; byte deltas independently match; excluded generated views UNCOVERED.
28. Bar/lints: prescribed review bar passed and both lints above are clean; full/smoke suites deliberately not run under the launcher's instructions.

Semantic counterpart decisions:
- Carry SN-036's changed acceptance through SR-161, LLR-183 and TC-211. Carry TC-178's narrower expected result; retain its provenance mechanics and SR-186's independent-purpose obligation. SR-165's distinct component-derivation obligation stays; removing its obsolete SR-161 analogy changes no acceptance.
- Retain LLR-183/TC-178 for name resolution, provenance and effective sets; retain LLR-202/TC-198 for staged provenance rereading; add LLR-360/TC-399 for round eligibility and sitting presentation. Each child has its own decision/verification purpose. Further splitting would subdivide those integrated purposes without adding an independent obligation or observation. Retain LLR-168/TC-162 for roster parsing and planner injection.
- Carry removal briefing through LLR-167 and TC-161; retain SR-146/SR-178's scope, anchor and authority constraints. The extracted amendment module owns that evidence arm rather than duplicating it. Retain LLR-271's comparison purpose, LLR-273's per-registry provenance and LLR-359's text identity; the new helper shares the existing removal definition, while moved symbols retain one implementation.
- Carry IF-133's removed operation and the changed IF-161/075/090/113/114/124/129/287 endpoints to the extraction. Retain IF-115's all-or-nothing public composition behavior: the additional optional internal composition context does not weaken that contract. Retain IF-124/IF-123's snapshot-evidence relationship: the new removal read uses the same recorded anchor and its function documents the returned removal/unknown populations; it neither writes nor approves the snapshot.
- This is PROCESS.md section 5's ruled obligation/design replacement, not a workaround retaining LLR-297. It removes the withdrawn sidecar design and keeps enduring provenance and authority behavior. Changed approved content still requires its applicable re-attestation; no status flip in this diff substitutes for it.

No finding lines.
VERDICT: APPROVE findings=0
