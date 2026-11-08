Reviewed: addb2eebca8f2ccf8c49120b183f0bf2c38dc57f

Verified: Reviewed the exact scoped full-lane diff, CLAUDE.md/AGENTS.md, PROCESS.md's change-intake and threat-model rules, the kit-change rubric, WI-1000 in full, LLR-171, SR-035, their SN parents, TC-165, IF-039 and the cited OI-127/OI-129 rulings. Prioritized fail-open token detection, silent coverage omissions and regression of the scaffold checks; this test-only change introduces no data-loss path. The prescribed tests and integrity instruments pass, but the actual shipped-surface test also passes on a copied template containing an explicitly forbidden source filename in ordinary Markdown emphasis.

Commands:
- `git rev-parse HEAD` -> `addb2eebca8f2ccf8c49120b183f0bf2c38dc57f`.
- `git diff b683375adf386c2c959abc1f806dad58973b6b2f...addb2eebca8f2ccf8c49120b183f0bf2c38dc57f -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ':(exclude)docs/log.md' ':(exclude)docs/log.d' ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'` -> four changed files; no shipped files or requirement-text/status changes.
- `Get-Content` / targeted `rg -n` reads of the requirement surface, changed tests and related existing helpers -> approved parent acceptance preserved; TC-165's only amendment is its evidence pointer; no conflicting historical requirement found for that pointer change, and no duplicated token scanner found.
- `git log -p --format=%h b683375adf386c2c959abc1f806dad58973b6b2f..addb2eebca8f2ccf8c49120b183f0bf2c38dc57f -- tests/test_language_neutral_scheme.py tests/test_profile.py` -> initial implementation 000862e66 and revised scanner addb2eebc, without commit messages.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt/review-tmp/2026-11-08-leg39` and bytecode writes disabled: `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-11-08-leg39/r2-A/wi-1000 tests/test_language_neutral_scheme.py tests/test_profile.py` -> `47 passed in 90.58s (0:01:30)`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (999 work item(s), 890 done (89%), 34 cancelled, graph acyclic).` Exit 0; advisory warnings were emitted.
- `trace.py --strict-integrity`, invoked once through `runpy` with only the report write redirected to this review directory to honor the no-worktree-writes constraint -> `Traceability: SN=31 SR=138 LLR=334 TC=380 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=258 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md`. Exit 0.
- Inline Python invoking the actual `scan` on copied surfaces -> emphasized `**src/app.py**`, italic `*src/app.py*` and anchored `src/app.py#L12` each returned `[]`; plain `src/app.py` returned its file, line 33 and token. A separate call to `test_shipped_surface_scans_clean` with its KIT set to a copied surface returned PASS with `detail = "See **src/app.py** for implementation."` planted at registries/system-requirements.template.toml:33.
- Inline Python loading `git show 000862e66:tests/test_language_neutral_scheme.py` in memory and invoking the current path regression assertions -> `tests/*.py`, `tests/test_*.py` and `src\check.py` each FAIL on the earlier scanner and PASS on the current scanner.
- `git status --short` -> empty; no worktree changes.

TC-035: .github/workflows/test.yml is listed beside the executed set and was not run.

Done-when coverage:
- New in-process module, constants, scan function, TC-165 tag and clean shipped surface: present; test_shipped_surface_scans_clean passes. Matching adequacy is incomplete as F1 demonstrates.
- Required planted pytest/app.py cases, script exemption, src/check.py rejection and removed heading: covered by test_a_planted_token_is_reported_with_file_and_line, test_a_kit_script_name_is_not_reported, test_a_py_path_beyond_the_exemption_is_reported and test_a_removed_section_heading_fails. Additional cases cover each surface class, vocabulary, empty glob, wildcards and Windows paths. These invoke the scan interface rather than inspecting handler source.
- Profile strict/schema invocation and node-level TC-165 tag: present and exercised across the eight profile permutations.
- Exact TC-165 evidence and equality of tags/evidence: correct; strict trajectory check passes.
- No shipped changes / no RESYNC entry: confirmed by the diff.
- A+B review: this is the independent A record; the other review is launcher-owned and was not used as evidence.

Semantic counterpart decision: TC-165 evidence is the changed side; its verifying method and SR-035/LLR-171 are the counterparts. Retain those approved obligations and acceptance unchanged: this is delivery of the missing verification, not replacement of an unsuitable design. No changed child normative content requires re-attestation and no decomposition is introduced. The regression below belongs in the existing scan boundary, preserving the parent obligation.

Findings:
- [MAJOR] tests/test_language_neutral_scheme.py:101 -> F1 (K1, B1): whole-token extension matching silently accepts a declared source extension when ordinary Markdown emphasis follows it. Planting `detail = "See **src/app.py** for implementation."` in a scanned template makes both `scan` return `[]` and `test_shipped_surface_scans_clean` PASS; plain `src/app.py` is correctly reported. Hand-authored registry prose supports Markdown, so a normal template edit can defeat TC-165's token-scan claim without changing the token or surface -> recognize the filename suffix before closing emphasis at the owning scan boundary and add an emphasized-path planted regression; this validates hand-authored file bytes at a genuine trust boundary (PROCESS.md section 3), consistent with antidote's "What is the smallest change that makes this fix unnecessary?" -> @Test Engineer
VERDICT: CHANGES-REQUESTED findings=1
