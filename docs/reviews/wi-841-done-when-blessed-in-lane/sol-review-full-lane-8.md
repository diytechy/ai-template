159819d6 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/agent_loop.py:1833 — The loop admits a combined sitting but cannot accept its valid verdict. Confirmed: a claimed row declaring `Brief=combined` composes successfully with requested kinds `amendment;done-when`. After a successful call, bookkeeping instead validates against `("combined",)`, records `failed`, retains `adjudication_owed`, and blesses nothing. D-011’s premise at docs/decisions/wi-841.toml:78 that the loop “never draws” this class is not enforced. Preserve the composed request, or enforce the coordinator-only constraint before launch.

2. project-trajectory/RESYNC_PACK.md:7314 — The upgrade copy list omits `scripts/session_service.py`, which adds the required `call_succeeded` function. Confirmed in a scratch upgrade from `76b1d212`: applying every script/template change except that omitted file makes the updated coordinator fail with `AttributeError: module 'session_service' has no attribute 'call_succeeded'`. Both adjudication routes depend on this update.

**MINOR**

1. tests/test_snapshot_readers.py:776 — The purported all-return case does not create a RETURN verdict. `_split_act(approve=False)` still calls `_bind_branch` at line 750, which writes `[APPROVE] SN-091` and `OUTCOME: APPROVE`. The test confirms an amendment-only act merges beside an approval verdict; it leaves the claimed all-return scenario untested.

**Verified**

D-026 and D-027 close the seventh-pass failures: failed calls retain their obligation without reading their verdict, and accepted judgements over unrelated rows authorize no act. Reviewed the fixed range, full spec, decisions, amended cells, holds, parser, successor minting and carrier handling. R2 is satisfied; existing Status values are unchanged; all 65 changed-function back-links resolve. The RESYNC anchor is a trunk ancestor, and its compatibility wording is corrected. The prescribed checks produced **378 passed in 235.90 seconds** and a clean strict trajectory result with warnings. Two representative tests were red against the base. No worktree files were written.

**Commands**

Python runs disabled bytecode writes and used the requested Git ceiling. No full suite or smoke tier ran.

- `Get-Content`, `rg -n`, `Select-Object`, `Select-String` — inspected guides, spec, decisions, prior review, implementation, cells and tests.
- `git diff 76b1d212..159819d6`, scoped variants, `--stat`, `--name-only`, `--numstat`; `git diff 58c7c119..159819d6` — reviewed the lane and final fixes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final8 tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_agent_loop_worker.py tests/test_verdict_record.py` — **378 passed**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; warnings.
- `python.exe -B .../wi841-final8-audit.py` and inline TOML inspection — verified Status values, back-links, amended cells and byte stamps.
- `python.exe -B .../wi841-final8-probe.py` — confirmed combined dispatch and rejection; exit 0 after correcting the fixture’s import-alias target.
- `python.exe -B .../wi841-final8-resync.py` — confirmed the upgrade crash.
- `python.exe -B .../wi841-final-red.py` — two representative tests red against `76b1d212`.
- `git merge-base --is-ancestor dd595b62 76b1d212`; `git log -1 --format='%h %s' dd595b62` — verified RESYNC ancestry.
- `git diff --check 76b1d212..159819d6` — trailing whitespace in recorded telemetry.
- `git rev-parse HEAD`; `git diff --name-only 159819d6 HEAD`; `git status --short`; `git ls-files --eol` — concurrent changes confined to adjudication records; expected line endings.
- Scratch-only `Set-Content` and `apply_patch` — prepared audit and reproduction scripts under `review-tmp/2026-10-06-wave18/`.