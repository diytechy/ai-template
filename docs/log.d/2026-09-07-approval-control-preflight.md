## 2026-09-07 — Repaired control preflight and authorized launch baseline

The repair landed locally as `0f106ce9c1e13a5f86b744311d649a4f69df32f2`
with hooks enabled. The committed read-only preflight resolves the existing
launcher, exact queued amendment scope and normal first admission of WI-605.
No premature turn record or claim was created. The preserved branch/worktree
and forensic patch still match the handoff. The
[fresh preflight](../ai-template-redesign-2026-09-05-codex/CONTROL-APPROVAL-PREFLIGHT.md)
records source/test evidence, route limits, exclusions, carried accounting and
the publication recovery limit. The source-anchored
[resync entry](../../project-trajectory/RESYNC_PACK.md) explains the coherent
adopter update and explicit interrupted-adjudication migration.

This commit removes the tracked pause under the owner's existing instruction.
The coordinator stays stopped until the hooks-enabled launch commit exists and
its clean SHA is captured under out/run-logs/control-retry-approval. There are
no control observations, provider requests or additional completions in this
preparation act. Postcommit normal regeneration changed only four provenance
lines; no live Status or snapshot registry byte changed.

Launch commit bar: smoke 1694 passed, 4 skipped in 49.86 seconds;
enforcing smoke 1694 passed, 4 skipped in 50.62 seconds, 50.8-second wall
against 90 seconds. Docs: 1496 documents, 2394 links, zero broken and one
pre-existing orphan warning.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=0f106ce9+launch-preflight; out/run-logs/approval-launch-smoke.txt -->
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=0f106ce9+launch-preflight; out/run-logs/approval-launch-smoke-budget.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=0f106ce9+launch-preflight; out/run-logs/approval-launch-docs.txt -->

The first launch commit hook refused a stale generated open-items page after
the new log fragment was added. Regenerating that page incorporates the new
fragment's `none` declaration; no code or policy changed. The hook rejection
is retained in out/run-logs/approval-launch-commit.txt.

Deferred open items: none — this is the already-authorized supervised retry.
