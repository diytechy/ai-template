# Failed uncommitted selection and derived-view refresh

The exclusive WI-619 selection attempt at source commit 35020525 failed its real
pre-commit hook before any model invocation. The exact machinery-authored selection
is preserved in attempted-turn.toml; it never had a committed origin and is not a
completed or accepted primary turn. Actual runner output, result and hook output
are preserved unchanged. The queued WI and its scope are unchanged.

The hook refused stale docs/ratify/CURRENT.md and docs/open-items.html. Source
commit 35020525 added Drafted IF-180; the generated brief's last-Status-change
provenance therefore advances to that commit and the interface census can cite
its WI-612 source-authoring record. This is not approval of IF-180 or any existing
row: existing Status cells and accepted snapshots did not change. No semantic
adjudication occurred in this failed attempt.

Under the existing dispatch/integration locks the supervisor preserved and removed
only the uncommitted selection, regenerated the declared views using trunk_step,
and passed the commit checks. The next selection must bind the resulting commit,
not reuse the abandoned turn's old base. No source, requirement, approval payload,
accepted snapshot, ordinary claim, coordinator/control window, push or main merge.

The full regeneration also refreshed the as-of provenance in docs/stage and
PROJECT_STATE.html. The next hook correctly refused those two derived files
while they were unstaged; that actual refusal is preserved. Their data/fingerprint
and phase values did not change. All four declared generated outputs are now
staged together, with no check bypass.
