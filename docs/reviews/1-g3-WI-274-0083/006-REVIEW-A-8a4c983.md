# 006-REVIEW-A — WI-274 fix single-home launcher migration (8a4c983)

Independent review of commit `8a4c983` (base `747f152`), the fix for the
004-REVIEW-A MAJOR. Scope: the diff (docs/specs/WI-274.md, the two
`agent-resume.template.{sh,cmd}` comments, `stack.ini.template`, and the new
`tests/test_bootstrap.py` regression) against the WI-274 spec + IF-068.

Verified by driving the REAL shipped paths, not by reading:

- New test `test_scaffolded_launcher_single_home_migration_lets_config_jobs_win`
  passes (`1 passed in 3.97s`).
- Drove `resolve_coordinator_dials` against a `[agent-loop] jobs = 1` stack.ini:
  `AGENT_JOBS` **absent** → `'1'` (config wins); env `AGENT_JOBS=2` (the
  un-migrated self-defaulting line) → `'2'` (config LOSES) — reproduces the
  004-REVIEW defect and confirms the documented edit fixes it. The exact edits
  (`unset AGENT_JOBS` + drop from the POSIX export list; `set "AGENT_JOBS="` on
  CMD) are stated identically across the two launchers, the stack.ini.template,
  and the spec, and anchor to the real launcher lines (sh:58/73, cmd:58).
- The `stack.ini.template` reformat (inline `# comment` → own-line comment) is a
  *necessary* correctness fix, not cosmetic: I drove `read_agent_loop_config` and
  the OLD inline form parses `jobs` = `'2                 # dispatcher worker
  ceiling (int, 1 = serial, or auto)'` (configparser has no inline_comment_prefixes),
  while the new own-line form yields clean `'2'`. The regression is coupled to
  this reformat and would fail against the old inline block.
- `trace.py` clean (orphans=0, integrity=0, interface-findings=0);
  `test_dogfood_sync.py` + `test_agent_loop.py` green (140 passed, 1 skipped).

The diff itself is correct and complete; both findings below are MINOR and
non-blocking.

- [MINOR] docs/status.md:56 -> `check.py --tier smoke` is NOT fully green: steps `trajectory` and `test_trajectory.py::test_forward_only_unit_over_the_real_meta_repo` fail because a `done` WI-275 token still lives in status.md and `docs/specs/WI-275.md` is unarchived (SpecRef still set) -> this is PRE-EXISTING at base `747f152` and untouched by this diff (no WI-274 commit edits status.md/work-items.csv/WI-275); recording it so the APPROVE is not misread as fully-green — scrub the WI-275 tokens from status.md and archive its spec as WI-275 close-out, do NOT block WI-274 on it -> @owner
- [MINOR] tests/test_bootstrap.py:502 -> for clarity: the regression proves the real resolver returns the declared `jobs` when `AGENT_JOBS` is absent (`monkeypatch.delenv`) and that the documented sed edits anchor to real launcher text, but it never executes the migrated launcher, so the edit→absent-env link rests on `unset`/`set ""` shell semantics rather than a driven check -> optionally exec the migrated `agent-resume.sh` under `sh` and assert `AGENT_JOBS` is unset in its exported env (POSIX-only; CMD stays reasoned, unrunnable on Linux/macOS CI) -> @owner
VERDICT: APPROVE findings=2
