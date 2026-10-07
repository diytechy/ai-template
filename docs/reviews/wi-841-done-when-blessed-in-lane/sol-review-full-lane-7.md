58c7c119 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/kitlib/sitting.py:478 — Accepted evidence for unrelated rows authorizes a rejected sitting’s unnamed act. Confirmed on a released rung: a failed combined sitting approves SR-002 and re-attests SR-001 without naming a verdict. It is initially refused, but adding an accepted sitting judging SR-003 and SR-004 makes `merge_approval_refusal` return `None`. Coverage unions kind names without tying the act to the judgement covering its rows. The amended kind-only rules in docs/requirements/low-level-requirements.toml:2855 and docs/requirements/low-level-requirements.toml:3284 permit this failure and do not preserve SR-232’s requested scope.

2. project-trajectory/scripts/agent_loop.py:1827 — A failed adjudication call can clear its obligation and finish `DONE`. Confirmed with `call_ok=False` after the session commits a syntactically valid Done-when verdict and WI trailer: bookkeeping reads the verdict, clears `adjudication_owed`, records the binding as `failed`, and `worker_endstate` returns `(0, "DONE", ...)`. The required re-sit is lost. This also contradicts LLR-310’s statement at docs/requirements/low-level-requirements.toml:3284 that a failed call’s verdict is not read. Completion must use the same acceptance result the route records.

**MINOR**

1. project-trajectory/RESYNC_PACK.md:7305 — “Inert until a lane edits its Done-when” is false under D-025. Confirmed with an unchanged claimed Done-when and a pre-upgrade unnamed amendment act on a released rung: the Done-when predicate releases, but merge refuses because the branch has no accepted binding. The compatibility statement must acknowledge this upgrade effect.

**Verified**

Both sixth-pass findings are closed: the isolated unnamed rejected act is refused, and the first-approval test explicitly approves SR-002 and asserts its ledger entry. Reviewed the fixed range, spec, D-001–D-025, amended cells, parser, holds, successor minting and carrier handling. R2 is satisfied; existing Status values are unchanged; all 63 changed-function back-links resolve. The RESYNC anchor is a trunk ancestor. All **294 prescribed tests passed in 162.95 seconds**; strict trajectory checking passed with warnings. Two representative tests were red against the base. No worktree files were written.

**Commands**

Python runs disabled bytecode writes and used the requested Git ceiling. No full suite or smoke tier ran.

- `Get-Content`, `Select-Object`, `Where-Object`, `Select-String`, `rg` — inspected rules, full spec, decisions, earlier review, changed cells, implementation and tests.
- Scoped `git diff 76b1d212..58c7c119`, `--stat`, `--name-only` and `--numstat` variants — reviewed the fixed lane changes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final7 tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_agent_loop_worker.py` — **294 passed**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; warnings.
- `python.exe -B C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final7-probe.py` — confirmed findings and sixth-pass fixes; final exit 0 after correcting the initial spy target.
- `python.exe -B C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final7-audit.py` — checked Status values, changed cells, back-links and byte deltas.
- `python.exe -B C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final-red.py` — two representative tests red against `76b1d212`.
- `git merge-base --is-ancestor dd595b62 76b1d212`; `git log -1 --format='%h %s' dd595b62` — verified RESYNC anchor.
- `git diff --check 76b1d212..58c7c119` — trailing whitespace in recorded telemetry.
- `git ls-files --eol`, `git status --short`, `git rev-parse HEAD`, `git diff --name-only 58c7c119 HEAD` — expected line endings; concurrent changes confined to adjudication records and snapshots.
- Scratch-only `apply_patch` and `Set-Content` — prepared reproduction and audit scripts.