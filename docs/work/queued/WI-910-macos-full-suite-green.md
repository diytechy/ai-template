+++
id = "WI-910"
title = "The full suite is green on macOS: the run.command fixture runs an executable run.sh, and the dispatch lane-worktree flake is explained"
workstream = "process"
sr_refs = ["SR-046", "SR-032"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 2
needs = ["WI-909"]
+++

## Context

Filed by hand on 2026-10-13 at the owner's direction: "drill through to see
if there is anything else related to Mac failures, and make a single WI to
cover that scope". WI-909 fixed the first Mac failure (the hooks' probe did not
parse under bash 3.2). This row holds what the drill found after it.

**How the drill was run.** The full unfiltered suite ran on the owner's Mac
(macOS, Darwin 25.6, `/bin/sh` is bash 3.2.57) at `492de194`, with
`python -m pytest -q -n auto -rfE -p no:cacheprovider`: 3 failed, 5819 passed,
59 skipped in 1210 s. A static sweep of every tracked shell file for GNU-only
flags (`sed -i` without a suffix, `readlink -f`, `date -d`, `timeout`,
`grep -P`, `stat -c`) and bash-4 syntax (`declare -A`, `mapfile`, `${x,,}`)
found nothing. The kit's Python calls no GNU-only tool. The only
platform-conditional skips are two Windows-only job-object tests in
`tests/test_cpu_cap.py`, so the 59 skips do not hide a Mac gap.

**Finding 1: the `run.command` fixture copies a non-executable `run.sh`
(2 failures, deterministic).**
`tests/test_run_devsetup.py::test_a_bare_run_calls_the_check_once_from_the_root_before_the_menu[run.command]`
and `::test_a_bare_run_hands_the_check_the_interpreter_its_menu_runs_on[run.command]`
fail with `run.sh: Permission denied` (exit 126). `_launcher_root` copies
`run.template.sh` with `shutil.copyfile`, which drops mode bits, and the
template is tracked `100644`. `run.command` then runs `exec ./run.sh`. The
`run.sh` cases pass because they invoke `sh run.sh` directly. This is not
Mac-specific: the same fixture fails on any POSIX where the exec bit is
honored, Linux included. It passes only where Git Bash ignores exec bits,
which suggests the machine running the suite since WI-834 (2026-10-09, when
the `run.command` case was added) is Windows. Adopters are not affected:
`bootstrap.py` sets the exec bit on every scaffolded `.sh`/`.command`
(line ~2533), and this repo's own `run.sh` is tracked `100755`.

**Finding 2: one intermittent dispatch failure under full-suite load (seen
once, not reproduced).**
`tests/test_dispatch.py::test_a_finished_branch_that_owes_nothing_goes_straight_to_the_slot`
failed once in the full run with `<tmp>-drive/wi-777 exists but does not hold
wi-777 - refusing to clobber it` (`integrate.lane_worktree`). It passed alone,
and passed in three parallel runs of the whole module (36/36 each). One
suspect, not yet driven: `agent_common.worktree_records` returns `[]` when
`git worktree list --porcelain` exits nonzero, and `lane_worktree` reads that
as "nothing holds the branch". An existing lane directory then refuses as a
clobber, where the real cause was git failing to answer. Nothing shows this
is Mac-specific; it was only first seen here.

**Why these went unseen.** Both failing modules sit in the slow tier
(`tests/conftest.py` `SLOW_MODULES`), so the per-commit smoke bar never runs
them. The suite's recent full runs were on a machine where finding 1 cannot
fail. CI's macOS and Linux jobs should show finding 1; their state on this
branch was not checked (no `gh` on the Mac).

## Done-when

- The `run.command` cases pass on macOS and Linux: the fixture gives the
  copied launchers their exec bit, as bootstrap does. Whether to also track
  `run.template.sh`/`.command` as `100755` is decided and recorded either way.
- Finding 2 is either reproduced and fixed at its cause, or recorded as not
  reproducible with the attempts named. If the suspect holds, git's failure
  surfaces as the refusal's reason instead of reading as "no holder".
- The full unfiltered suite is green on the Mac, with the command, revision
  and result recorded. The CI macOS and Linux jobs' state on the branch tip is
  checked and recorded.
- The finding that the suite's recent full runs could not see a POSIX-only
  failure is carried to the owner as a question: whether the full suite should
  also run on a POSIX box before phase close, beyond CI.
