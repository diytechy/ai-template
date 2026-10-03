# WI-763 adjudication: first approval of LLR-291 and TC-304 (WI-657)

Independent adjudicator (Claude Opus 5.5), 2026-10-03. Chains read: SR-006
(LLR-006/008/014/016/098/141, TC-006/008/014/016/101/134), SR-182 (LLR-195,
TC-190), SR-183 (LLR-206, TC-202/203). Checked against check.py
(changed_paths, _path_matches, resolve_plan, _invocation_plan),
kitlib/config.py (step_paths, step_threshold), docs/stack.ini (paths on
smoke, dupes-census, complexity, readability), the commented example in
project-trajectory/stack.ini.template, project-trajectory/hooks/pre-commit
(`check.py --path-triggered`) and tests/test_step_path_trigger.py (smoke tier,
not in SLOW_MODULES; 77 passed with the dupes-census and complexity modules).

- [APPROVE] LLR-291 -> a step's optional `paths` key is a comma/whitespace list of repo-relative, case-sensitive fnmatch patterns (`*` spans `/`); a step is selected at or above its from-stage OR on a matching changed path; staged paths first, a claimed lane's base-to-HEAD change when the index is empty; failed or empty reads are unknown and run every path-declaring step; deletions and both rename sides count; blank/absent paths stay rung-only; `--path-triggered` (the hook) runs only selected path-declaring steps except smoke, while ordinary gates keep smoke rung- or path-selected; each stack's declaration covers its sensor's baseline, script and config -> upward, SR-006 asks that the harness run the declared steps of the bar and a tier select exactly the declared subset; a step's declared trigger is part of its declaration and only ever adds a run, never skips a required one, so the bar is not weakened, and the owner's 2026-10-02 ruling places the rule here; sideways it is one decision (selection) not covered by LLR-006 (plan/missing tool) or LLR-141 (lane freshness skip); downward TC-304 drives every clause -> ready: each clause is a closed, observable obligation and matches the code read (fnmatchcase, --no-renames without a diff filter, None on b"" or failure, the smoke exclusion in _invocation_plan, the empty plan when no step declares paths).
- [APPROVE] TC-304 -> in memory: matching code/baseline/script/config change selects below the rung, an unrelated change does not, the rung selects with no change, unknown selects; blank and absent paths stay rung-only; mocked git reads cover no staged diff, failed reads, unresolvable lane base, base-to-tip change, deletion and both rename paths; the hook CLI through main runs only selected path-declaring steps except smoke while gates keep smoke; the live declaration covers all four sensors' inputs -> the evidence module has a test per clause (test_matching_change_below_rung ... test_hook_excludes_smoke_but_gate_keeps_it, test_repo_sensors_include_their_inputs), runs in the smoke tier as declared, and Verifies LLR-291 plus the selection sentences of LLR-195 and LLR-206 and IF-267 -> ready: method, expected and evidence agree with what the rows say, and nothing LLR-291 states goes unverified.

OUTCOME: APPROVE rows=2
