# WI-834 checkpoint sitting 011 (a56d9769)

## amendment

Both rows move only their Tier, from Smoke to Full. What a TC verifies is
unchanged; when its verification is owed moves.
- **Smoke:** the case is part of the per-commit bar, `pytest -m smoke` under
  the 60 s budget.
- **Full:** it runs in the unfiltered suite at phase close and in the merge
  slot's full bar.

An implementation that met the old rows (evidence green at every commit) also
meets the new ones. But a lane could now pass every commit bar while these
cases are broken, which the old text forbade. That is a change in an acceptance
condition, so the rows change MEANING.

I would bless both. Every evidence item in both rows is in
`tests/test_run_devsetup.py`, and `tests/conftest.py:105` lists that module in
`SLOW_MODULES`. So the Smoke tier claimed a per-commit verification the suite
never performs, which is exactly the case `tests/test_evidence_join.py`
reports. I ran that check: `16 passed`. Full is the true statement of when this
evidence runs. The in-process pins in `tests/test_blackout_window.py` still
cover the cheap readiness cases at the commit bar.

- [MEANING] TC-342 Tier -> the bare-run, direct and list readiness cases are owed at every commit's smoke bar -> owed at the full-suite bar (phase close and merge) -> the same verification, owed at a different bar; a lane may now pass its commit bar with these cases red, so the acceptance timing changed; blessed, because the old tier was false (its only evidence module is in SLOW_MODULES and never runs at the smoke bar), so the new text states what the suite actually does
- [MEANING] TC-343 Tier -> the dev-setup readiness-operation cases are owed at every commit's smoke bar -> owed at the full-suite bar -> the same change of verification bar, for the same reason; blessed (all five evidence tests are in the slow `tests/test_run_devsetup.py`)

VERDICT: MEANING rows=2

The act re-attests TC-342 and TC-343.

SITTING: JUDGED kinds=amendment
