## 2026-09-05 — Cross-check Fable's simplifications and define adopter revalidation

Reviewed the changes in `9f938edd` against `360a075a` and recorded the
[dispositions](../ai-template-redesign-2026-09-05-codex/FABLE-3-CROSSCHECK-DISPOSITIONS.md).
Kept prose-only objective anchors, a minimum metrics writer, the combined
adopter charter and targeted repair when control evidence is insufficient.
Qualified smoke as a baseline rather than full regression coverage, retained
the minimum semantics needed for comparable usage, and reconciled stale agenda
and measurement-window instructions.

Added the owner's [adopter revalidation workflow](../ai-template-redesign-2026-09-05-codex/ADOPTER-REVALIDATION.md):
review each project's hats against its own vision, derive missing hats where
needed, propose genuinely missing SNs and rederive affected SRs. Distinguish
new stakeholder outcomes, hat-derived constraints and implementation debt.
Linked the workflow into P0/P1 and P10 without editing live registries or
commissioning a new schema.

Validation at `9f938edd` plus this documentation diff:

- `.venv/bin/python scripts/check_smoke_budget.py --mode enforce` ran the
  declared `.venv/bin/python -m pytest -q -n auto -m smoke` command:
  `1638 passed, 4 skipped in 59.14s`; enforced wall time
  `59.4s vs 60s budget -> within`, exit 0. <!-- fig: command on preceding lines; 9f938edd + this docs diff -->
- `.venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale`
  passed with no broken links; the unrelated existing report orphan and
  historical staleness hints remain warnings.
- An in-memory `[step:smoke]` profile parsed through `check.extra_steps` as
  a product step from DevStg-Tests. The live profile was not edited.
- The named integration test modules are in SLOW_MODULES. This verifies the
  smoke-coverage limitation, not a planted runtime regression.
- Historical Fable reviews/metadata and the prior hats sweep match their
  source-commit bytes. `git diff --check` passed.

Scope/deviation: owner-requested plan review and extension only; no model
invocation, runtime implementation, live vision/hat/SN/SR edit, queue change,
unpause or policy alteration. Budgeted-document byte delta: zero. No full-suite
or station-prototype result is claimed.

Deferred open items: none new — implementation choices remain in the plan's
existing review agenda; no new operational hold or owner ruling was created.
