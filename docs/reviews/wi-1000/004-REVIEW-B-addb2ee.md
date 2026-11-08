Reviewed: addb2eebca8f2ccf8c49120b183f0bf2c38dc57f

Verified. The checkout is the reviewed commit (`git rev-parse HEAD` = addb2eeb...). The reading-scope diff touches four files: `tests/test_language_neutral_scheme.py` (new), `tests/test_profile.py`, the TC-165 `evidence` cell in `docs/test/test-cases.toml`, and `docs/decisions/wi-1000.toml`. No shipped `project-trajectory/` file changes, so no RESYNC entry is owed (Done-when 5).

The failure class that matters most here is fail-open: the scan reporting clean on a surface that carries a token, or quietly skipping a file or section. I checked for it in these ways:
- The surface globs all 15 `registries/*.template.{toml,csv}` files. It adds `work/WI-000.template.md` and `id-watermark.template`. It reads `trace.WATERMARK_SPACES` and the two declared sections. The PROCESS.md section runs from line 97 to line 114. The INTERFACES.template.md section runs from line 26 to line 47. Neither section has a fenced `## ` line that would cut it short.
- An empty glob or a missing heading fails the scan instead of being skipped (`_section` and `_surface_files` assert).
- Planted cases cover every surface class, including a declared section. Line numbers count from the file, not from the section.
- Both constants match the spec's lists exactly.
- The word matcher backtracks correctly through prefix pairs such as ruby/rubygems and java/javascript.
- The `.py` exemption fires only on bare `<name>.py` or `scripts/<name>.py` where the kit script exists. `src/check.py`, `project-trajectory/scripts/trace.py`, `nope.py`, `tests/*.py` and `src\check.py` are all reported.

I loaded the pre-fix module (000862e66) next to the tip and drove `_line_hits` directly. The round-1 regression cases `tests/*.py`, `tests/test_*.py` and `src\check.py` return `[]` before the fix and are reported after it. They are real red-before tests.

Done-when map:
1. Module, constants, scan, shipped surface clean: `test_shipped_surface_scans_clean` and `test_the_vocabulary_is_read`.
2. Planted cases:
   - `pytest` and `src/app.py` reported with file and line: `test_a_planted_token_is_reported_with_file_and_line`, 6 surfaces x 2 tokens.
   - `scripts/trace.py` not reported: `test_a_kit_script_name_is_not_reported`.
   - `src/check.py` reported: `test_a_py_path_beyond_the_exemption_is_reported`.
   - A removed §2 heading fails: `test_a_removed_section_heading_fails`.
3. Scaffold half: `test_every_profile_permutation_scaffolds_green` (stacks `any` and `node`) now runs `trace.py --strict --strict-schema` and carries the node-level `Implements: TC-165` tag. `trace.py`'s `exit_code` shows that `--strict` includes integrity findings, so this is at least as strict as TC-165's `--strict-integrity --strict-schema`.
4. TC-165 `evidence` holds exactly the specified string. `check_trajectory --strict` is clean, and its `tc_tag_findings` holds tags equal to Evidence parts under `--strict`.
5. No shipped file changed: confirmed.

Rubric `docs/rubrics/kit-change-review.md`:
- K1/K2: the diff adds or amends no SN/SR/LLR text. The one TC cell changed is `evidence`, at the tier where a carrier may be named.
- K3: the only approved-row change is the `evidence` cell the spec grants. No Status flipped. The `Implements: TC-165` tags are test-file tags.

Requirement-row sweep: the diff adds no requirement row. TC-165 still verifies SR-035 and LLR-171, and their texts agree with the test's claim.

Consolidation: the scan has no existing counterpart in `tests/` or the kit. Other test modules have `_section` helpers, but they return flattened text with no line numbers, so they cannot serve here. That is not a repeat.

Commands:
- `git rev-parse HEAD` -> addb2eebca8f2ccf8c49120b183f0bf2c38dc57f
- `$env:GIT_CEILING_DIRECTORIES=...; python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-11-08-leg39/r2-B/wi-1000 tests/test_language_neutral_scheme.py tests/test_profile.py` -> `47 passed in 67.36s (0:01:07)` (0 environment-gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (999 work item(s), 890 done (89%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=334 TC=380 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md` exit 0. It was invoked twice: once filtered for TC-165/evidence lines (none), once for the final line. It writes only the gitignored report, and `git status` in the lane is clean.
- Probe: `python -I` over `probe/probe.py` loads the pre-fix (000862e66) and tip modules and drives `_line_hits` and `scan` on the cases below. Both versions scan the shipped surface as `[]`.

- [MINOR] tests/test_language_neutral_scheme.py:96 -> (B1, confirmed by running `_line_hits`) The round-1 fix replaced the boundary-anchored extension regex with "read the whole separator-delimited token, then require it to END in the extension" (lines 96-103, 143-145). That regressed the spec's closed matching rule, "a name character before the dot and none after it": an extension followed by a non-name character outside the `_TOKEN` separator set is no longer reported. Probed on the tip, these return `[]`, while the pre-fix code reports them: `see [app](src/app.py#L3) here` (the markdown `path#Lnn` link form, which this repo's own prose uses), `src/app.py*`, `app.py’s` (curly apostrophe), `app.py—then` (em dash), `app.py&x`, `https://x/y.py?raw=1`. Nothing on today's surface carries such a form, so this is a latent fail-open of the guard, not a present miss. No test covers it -> Judge the extension the way the spec states it: match `[name*?]\.(ext)(?![A-Za-z0-9_])` anywhere inside the token, and test the exemption on the token's prefix up to that match, so separator and wildcard handling stay whole. Add one planted case (e.g. `src/app.py#L3`) to `test_a_py_path_beyond_the_exemption_is_reported`. This corrects a matcher, not a guard, so no unrepresentability clause is owed -> @owner

VERDICT: APPROVE findings=1
