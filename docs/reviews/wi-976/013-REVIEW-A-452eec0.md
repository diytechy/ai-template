Reviewed: 452eec010d33a712de5f7beba5330968d8cc6a89

Verified: Independent convergence review of the prescribed full-lane diff, WI-976's complete spec, its item-14 specref and quoted owner ruling, PROCESS sections 3/5/6, the kit-change rubric, and the cited registry rows and their existing counterparts. Hunted silent omitted/extra hat questions first, fail-open composition second, and retirement/data-loss regressions third. The specified test selection passed (452 passed, 2 skipped); trajectory and strict integrity checks passed. Actual compose and mkprompt flows preserve separate parent contexts, include amended SRs' parents in mixed rounds, reject malformed rosters where the optional slot is used, and keep outcome lines outside the ruling grammar. No new reachable defect was found. The worktree remains clean. This verdict does not attest the owner-held act or the subsequent TC-211 execution.

Commands:
- `git rev-parse HEAD` -> `452eec010d33a712de5f7beba5330968d8cc6a89` before running checks.
- `Get-Content CLAUDE.md`, `.agents/skills/antidote/SKILL.md`, `.agents/skills/coordinator-cycle/SKILL.md`, WI-976's spec, and `docs/rubrics/kit-change-review.md`; targeted `Get-Content`/`Select-Object` reads of PROCESS, item 14, the changed scripts/tests, and the authored implementation plan -> governing rules and changed behavior inspected. No earlier verdict file, decisions file, filed critique, lane commit subject, or implementer session note was opened.
- `git diff aa36a5b6e2bc47fe9960bbc4a0727c04c9571f36...452eec010d33a712de5f7beba5330968d8cc6a89 -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ':(exclude)docs/decisions' ':(exclude)docs/plans/*/critique-*' ':(exclude)docs/log.md' ':(exclude)docs/log.d' ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'` (stat and path-grouped patches) -> 42 changed files; code, tests, requirements, instructions, shipping notice and generated changes inspected.
- Targeted `rg -n` searches in the existing SN/SR/LLR/TC/IF registries for the changed IDs, perspective obligations and retained counterparts -> no conflicting obligation, new overlapping capability, or changed limit found. `rg` retirement sweep across the declared live surfaces, excluding RESYNC's retirement notices -> no remaining sidecar path, record command, retired row citation or command-only symbol; the loose `hats record` pattern also matched unrelated English in trace's docstring.
- `git show f6c7360f:docs/log.d/2026-09-06-sn036-owner-ruling.md` -> independently read the quoted ruling, its four acts and prohibition on the sidecar/check.
- `git log -p --format=%h aa36a5b6e2bc47fe9960bbc4a0727c04c9571f36..452eec010d33a712de5f7beba5330968d8cc6a89 -- project-trajectory/scripts/plan_briefs.py project-trajectory/scripts/adjudicate_brief.py scripts/coordinator/mkprompt.py tests/test_adjudicate_brief.py tests/test_prompts.py`; `git log --format=%h` over the changed implementation paths -> pre-fix implementations located without commit messages.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt/review-tmp/2026-10-25b-leg20` and `PYTHONDONTWRITEBYTECODE=1`: `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-25b-leg20/g1a/wi-976 tests/test_plan_briefs.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_hats.py tests/test_dogfood_sync.py tests/test_spine_carrier.py tests/test_trace.py tests/test_trace_hats.py` -> `452 passed, 2 skipped in 397.59s (0:06:37)`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (973 work item(s), 863 done (89%), 34 cancelled, graph acyclic).` Exit 0; advisory warnings are not reproduced here.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/trace.py --strict-integrity` (last line selected) -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 drafts=2 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md` Exit 0; no resulting worktree change.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-25b-leg20/g1a/reproduce.py` -> current mixed-amendment and combined-round tests PASS; both EXPECTED FAIL against `49a47d3b5^`; author-parent selection and empty-HATS tests PASS currently and EXPECTED FAIL with pre-fix mkprompt; original base compose omits the new test's `need-b question?`; combined templates both overridden without the slot compose over a malformed roster. One intermediate invocation stopped with FileExistsError because its scratch fixture already existed; a fresh scratch directory resolved that setup error. Production harnesses were each run once.
- `git log --format=%h --reverse aa36a5b6..452eec0 -- docs/log.d/2026-10-25-wi976-sn036-ruling.md docs/requirements/stakeholder-needs.toml`, `git diff-tree --no-commit-id --name-only -r` for those commits -> ruling fragment at `36fc6d6f7`, row changes later at `4fc5d55f4`.
- `git ls-tree -r --name-only 452eec0 -- docs/log.d/retired/LLR-297.md docs/log.d/retired/TC-312.md` -> both retirement records exist; their excluded contents and sitting authorization were not reviewed.
- Python byte comparison of `git show aa36a5b6:project-trajectory/PROCESS.md` with the tip -> `PROCESS bytes: base=98185 tip=97962 delta=-223`, matching all three updated stamps.
- `git diff --name-only aa36a5b6...452eec0 -- docs/status.md docs/process.toml` -> neither changed. `git status --porcelain` -> empty at completion.

Requirement/counterpart semantic decisions:
- Changed SN-036 acceptance -> carry the corresponding SR-161 change. Preserve SN-036's need/why; the owner ruling explicitly changes the coverage mechanism. This is a requirement amendment followed by design replacement under PROCESS section 5, not a workaround preserving unsuitable LLR-297.
- Changed SR-161 -> carry LLR-183's revised review-path clause, retire LLR-297/TC-312, add LLR-360/TC-399, and split TC-178's mechanical evidence from TC-211's adequacy inspection. Retain LLR-202/TC-198: they reconsider row attribution after an amendment and do not produce or validate a decomposition sidecar.
- Retained children under SR-161 have distinct purposes: LLR-183 resolves row attribution and derives effective hats; LLR-202 handles stale attribution at an approved-row amendment; LLR-360 assembles the sitting's applicable questions and outcome instruction. Further splitting these by branch or template would repeat their owning algorithm rather than add an independent decision. TC-178 verifies provenance mechanics, TC-198 verifies the staged attribution arm, TC-399 drives sitting composition and ruling parsing, and TC-211 inspects actual outcomes and child value. None substitutes a row count for adequacy.
- Changed TC-211 -> retain SR-186 unchanged: its independent-child-purpose and stopping-decision acceptance still applies, alongside SR-161's newly inspected hat outcomes. The revised procedure/rubric retains the paraphrasing-child abnormal case and adds the missing-outcome case.
- Changed IF-133 data -> carry hats.py's deletion of its sole `load` consumer; retain load_needs/resolve/stem/folded/NEED_CARRIERS for roster audit. Retain IF-115's compose text-or-reason contract and IF-113's strict template-fill contract: the new block uses their existing all-or-nothing refusal boundary.
- Changed SR-165 rationale -> retain its requirement/acceptance, LLR-172 and TC-166. Removing the obsolete analogy to SR-161 does not change component partition completeness, ranking recomputation or override behavior.
- Authority: unchanged parent acceptance/approval (including SR-186) and enduring Hat-Refs tests remain intact. Changed approved text and new Drafted children still require the applicable recorded acts; this code review grants no re-attestation.

Done-when coverage (numbers follow the 28 checkboxes in spec order):
1. Ruling committed first: verified by message-free commit/path history; ruling content cross-checked with the quoted original.
2. Amended row meanings and TC split: inspected against spec/ruling and existing counterparts; applicable re-attestation not verified here.
3. Retired LLR-297/TC-312: deletions and retirement-record existence verified; sitting/record contents UNCOVERED by this round's exclusions.
4. New LLR and TC: LLR-360/TC-399 inspected; automated states exercised. First-approval act UNCOVERED.
5. IF-133 loses load: inspected alongside deleted consumer.
6. Procedure and historical INCOMPLETE: inspected; missing-outcome abnormal input included.
7. Rubric R1/B1: inspected; requires actual review outcomes.
8. Record command/module/symbol retirement: diff and live sweep; remaining roster tests pass.
9. Sidecar and pointer removal: diff verified.
10. Instruction retirement: PROCESS, c3, both roster headers and all three recipe copies inspected; dogfood/prompt tests pass.
11. SAFETY divergence: live/template pins and applicability tests pass; ruling citation/count inspected.
12. Live-surface retirement: targeted sweep and generated diffs inspected; RESYNC retirement notices are intentional.
13. Round classification: first-approved SR, amended SN, SR-only amendment and LLR/TC-only first approval compose tests pass; other brief slot pins pass.
14. Parent applicability: judged-parent replacement, amended SR parents, sibling separation and WI tag-widening tests pass; two pre-fix regressions independently reproduced.
15. Optional slots/overrides: real compose tests pass, including independent combined no-slot overrides over malformed roster.
16. Combined questions once: real combined compose tests pass; actual checkpoint verdict outcomes UNCOVERED because earlier verdicts cannot be read in convergence stance.
17. Absent/malformed roster: round and compose tests pass; no-round path does not read malformed roster.
18. Outcome parsing: amendment, first-approval and combined verdict tests preserve parsed rulings and actable rows.
19. Author prompt: actual mkprompt CLI tests pass for computed parents, no-round, missing/empty slot, and equality with sitting questions; dispatch/recipe pins pass. The final recipe correction is independently visible in the changed text.
20. State tests and pins: specified test selection passed; tests exercise compose/mkprompt/parser interfaces and discriminate plausible missing-parent, extra-parent, duplicate-block and permissive-empty implementations. Static pins support the runtime tests.
21. Committed checkpoint brief/verdict sample: UNCOVERED; those process records are excluded and earlier verdicts forbidden for this review.
22. Fresh post-act TC-211 execution: UNCOVERED; the changed procedure reports the historical pass, not a new execution. This remains a required later step after the acts.
23. Owner SN-036 re-attestation: UNCOVERED; reserved to the owner and not granted by this verdict.
24. Headless stop/handoff/other acts: UNCOVERED; excluded process records were not inspected.
25. No landing before owner act and return handling: future workflow obligation; UNCOVERED, with the spec's hold preserved.
26. RESYNC: retirement, failing old caller, inert notes, optional override and stale preserved header all documented.
27. Generated pages/catalogue/restamp: changed generated surfaces and catalogue inspected; prompt/dogfood tests pass; independently measured PROCESS delta -223. Excluded views and implementer skill-report records UNCOVERED.
28. Bar/strict lints: launcher-substituted test command and both strict checks pass on the exact reviewed tip. Full smoke/full suite intentionally not run under this round's instructions; future landing-tip attestation UNCOVERED.

The UNCOVERED authority and post-act items are not evidence of a code defect and must not be treated as completed by this approval. No out-of-spec fail-closed input was counted as a finding.

Findings: none.
VERDICT: APPROVE findings=0
