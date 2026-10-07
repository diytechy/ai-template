c1d8dc61 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/acceptance_record.py:1073 — A rejected combined sitting can still authorize another section’s act. Confirmed with a bound `amendment;done-when` verdict containing a CLARITY ruling for SR-001 but no Done-when machine line. Sitting validation rejects it, yet the integrator’s approval-act rung accepts its held-rung re-attestation. This reader consumes raw row tags without checking the whole sitting, violating SR-232’s refusal without another kind acting.

2. project-trajectory/scripts/kitlib/done_when.py:341 — Failed-call verdicts still release holds. Through the actual coordinator entry point with an injected model call, a session committed a matching BLESSED verdict and then failed or timed out. The coordinator returned 1 and explicitly declined to read its verdict, but committed its binding at project-trajectory/scripts/coordinator_adjudicate.py:314. Dispatch, staged close and merge subsequently released, and intake minted nothing. Coverage preserves the requested kinds but loses the failed-call outcome.

3. project-trajectory/scripts/kitlib/sitting.py:223 — A valid disposition verdict can crash the covering reader. Confirmed with `OUTCOME: COMPLETE successors=0`, its coordinator-style `brief = disposition` binding, and a fenced Done-when example. Disposition validation accepts the file, but coverage passes `disposition` into this parser, which indexes a grammar table lacking that class and raises `KeyError`. An unrelated valid adjudication therefore crashes the changed lane’s dispatch check.

**MINOR**

none

**Verified**

The two final2 parser findings are closed, and TC-257 now correctly says “no goalposts adjudication.” All **323 prescribed tests passed in 151.35 seconds**; strict trajectory checking passed with warnings. Changed SR cells satisfy R2, existing Status values are unchanged, and 51 changed-function back-links resolve. The RESYNC anchor is a trunk ancestor, byte stamps match, and two representative tests were red against the base. I changed no worktree files; concurrent changes were adjudication records and snapshots only.

**Commands**

Python runs disabled bytecode writes and used the requested Git ceiling. No full suite or smoke tier ran.

- `Get-Content`, `Select-Object`, `rg -n`, and `rg --files` — read the guide, full spec, D-001..D-021, adjudications, prior review, amended cells, implementation and tests.
- `git diff 76b1d212..c1d8dc61`, with scoped, `--stat`, `--name-status`, and `--unified=0` variants — reviewed the fixed lane range.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final3 tests/test_done_when_blessing.py tests/test_adjudicate_brief.py tests/test_intake.py tests/test_coordinator_adjudicate.py tests/test_snapshot_readers.py` — **323 passed**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; repeated after concurrent adjudication commits.
- `python.exe -B …/wi841-final3-probe.py` and inline `python.exe -B -` probes — confirmed all three MAJORs, including the integrator’s approval-act rung.
- `python.exe -B …/wi841-final3-audit.py` — checked changed cells, Status values, back-links, byte deltas and concurrent scope.
- `python.exe -B …/wi841-final-red.py` — two representative tests red against `76b1d212`.
- `git merge-base --is-ancestor dd595b62 76b1d212`; `git log -1 --format='%h %s' dd595b62` — verified the RESYNC anchor.
- `git diff --check 76b1d212..c1d8dc61` — trailing whitespace in recorded telemetry.
- `git status --short`, `git rev-parse HEAD`, revision diffs, and `git ls-files --eol` — checked concurrent scope and measured-document line endings.
- Scratch-only `apply_patch` and fixture writes — confined to the authorized scratch area.