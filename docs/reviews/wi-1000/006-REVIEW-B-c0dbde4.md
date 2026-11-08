Reviewed: c0dbde48dcceb7ccc32bc799c1fbd9dbf8259dec

Verified. The checkout was the reviewed commit (`git rev-parse HEAD` printed c0dbde48dcceb7ccc32bc799c1fbd9dbf8259dec). The diff is three files: the new tests/test_language_neutral_scheme.py, the docstring tag and the `--strict-schema` flag in tests/test_profile.py, and TC-165's `evidence` cell. No shipped file changes, so no RESYNC entry is owed. The failure classes I hunted first were fail-open ones: a token the scan should report but does not, a surface or section silently skipped, an exemption wider than `<name>.py` / `scripts/<name>.py`, and a tag/evidence pairing the checker does not actually hold.

Done-when coverage:
(1) The module is tagged `Implements: TC-165`, declares both constants exactly as the spec lists them, and has one `scan`. `test_shipped_surface_scans_clean` passes on the real kit. I enumerated the exemptions independently: there are exactly 37, 29 of them in `registries/`, and every one names a real kit script, which matches the spec's measurement.
(2) Planted cases: `test_a_planted_token_is_reported_with_file_and_line` plants `pytest` and `src/app.py` into six surface classes, the two declared sections included, and asserts file and line. `scripts/trace.py` is exempt (`test_a_kit_script_name_is_not_reported`). `src/check.py` is reported (`test_a_py_path_beyond_the_exemption_is_reported`). A removed §2 heading fails (`test_a_removed_section_heading_fails`), and so does an empty glob.
(3) `test_every_profile_permutation_scaffolds_green` runs `trace.py --strict --strict-schema` over `any` and `node` and carries the node-level tag. `trace.exit_code` folds integrity into `--strict`, so the flag set is a superset of TC-165's `--strict-integrity --strict-schema`. `node` takes the same `NON_PYTHON_STACKS` branch in bootstrap.py as go, rust and powershell, and that branch touches no registry template.
(4) TC-165 evidence is equal to the tags. I confirmed the checker really holds them equal, not just that it reported clean: `gen_arch_map.read_test_tags` returns exactly the two parts for TC-165. Fed mutated evidence cells, `trajectory_arch._tag_evidence_findings` reports `tag without evidence` / `evidence without a tag` for each one.
(5) No shipped file changes.
(6) The A+B review bar is a process item and is not checkable from the diff.

The two sections are correctly bounded: PROCESS.md runs 18 lines and ends at `## 3.`; INTERFACES.template.md runs 22 lines and ends at `## Rules`. Neither contains a code fence.

Convergence (pre-fix code taken from `git log -p --format=%h` on the test file). I loaded the 000862e66 and addb2eebc versions of `_line_hits` and ran every current exemption and report case against them. 000862e66 fails the 4 wildcard/Windows-separator cases (`tests/*.py`, `tests/test_*.py`, `src\check.py`, `**/*.py`). addb2eebc fails the 8 extension-termination cases (emphasis, anchor, trailing `*`, curly apostrophe, em dash, `&`, query). The current version fails none. So each round's regression tests fail on their pre-fix code.

Rubric anchors: K1 holds (the TC-165 cell is true against the code); K2 does not apply (no SN/SR touched); K3 holds (the approved TC-165 changes only in the evidence cell the spec grants, and no Status flips). No new function repeats an existing kit helper. `kitlib/spine.MODULE_EXTS` serves a different purpose (module paths in requirement cells), and the spec rules that the token set lives once, in the test module.

Coverage-extension notes (no severity: these inputs are outside the spec's declared contract, which rules them out of the claim). `python3` is not reported, because a digit is a name character. A bare `` `.py` `` with no stem is not reported, because the rule needs a name character before the dot. Separately, `--strict-schema` sweeps only real rows (`schema_sweep(real)`), so on a fresh `-000`-only scaffold the schema tier passes by construction. That is SR-035's acceptance as worded, not a defect of this diff.

Commands:
- `git rev-parse HEAD` -> c0dbde48dcceb7ccc32bc799c1fbd9dbf8259dec
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r3-B/wi-1000 tests/test_language_neutral_scheme.py tests/test_profile.py` -> `60 passed in 94.55s (0:01:34)` (0 environment-gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (999 work item(s), 890 done (89%), 34 cancelled, graph acyclic).`
- probe (outside the lane): pre-fix `_line_hits` versions 000862e66 / addb2eebc / tip against every exemption and report case -> 4 / 8 / 0 failures
- probe (outside the lane): the tip test module with `re.IGNORECASE` removed from `_EXTENSION` only -> `37 passed in 3.33s`
- probe (outside the lane): `read_test_tags` and `_tag_evidence_findings` with mutated TC-165 evidence -> a mismatch finding for each mutation
- listed beside the set, not run: TC-035 `.github/workflows/test.yml`

- [MINOR] tests/test_language_neutral_scheme.py:98 -> the spec's "Matching is case-insensitive" is pinned for words (`test_the_vocabulary_is_read` expects `pytest` from `PYTEST`) but not for extensions. With `re.IGNORECASE` dropped from `_EXTENSION`, all 37 tests in the module still pass, so a plausible wrong implementation goes undetected and an upper-case `App.PY` or `main.JS` would scan clean -> add an upper-case case to `test_an_extension_ends_at_any_non_name_character` (e.g. `("See src/App.PY.", "src/App.PY")`) and an upper-case kit-script name (`TRACE.PY` is reported, since the stem comparison is case-sensitive) -> K1 -> @owner

VERDICT: APPROVE findings=1
