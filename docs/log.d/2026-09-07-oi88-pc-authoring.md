## 2026-09-07 — OI-88 approved; exact PC source authoring

The owner answered “Yes that's fine” to the [one-time transfer proposal](../reviews/wi-609-resolution/DECISION.md). Recorded OI-88 as ruled; its approval concerns ownership only. The coordinator and tracked pause remain in place; no control window, push, main merge or primary selection occurred.

Applied the exact corrected [PC patch](../ai-template-redesign-2026-09-05-codex/PC-BATCH-AMENDMENTS.patch) after verifying its recorded SHA-256 and clean application. The resulting live SR/LLR/TC files are byte-identical to the proposal's registry candidate `9fa3e1bbf188d50d762ca4ee6d6af14ad06f8618`. Status, parents and approval snapshots are unchanged; no code or test deletion. This is supervised source authoring under the existing station locks, without an ordinary claim while paused. The authoring WI remains queued until its ownership deliverable is reconciled through the approved reviewed transfer. The ruling supersedes the earlier separate-owner dependency; historical proposal/review evidence is retained.

Strict trace passed with no orphan or integrity findings; its existing advisories remain. fig: `.venv/bin/python project-trajectory/scripts/trace.py --root . --strict` on `b9852757` plus the exact reviewed patch, output `out/run-logs/pc-transfer/authoring-trace.txt`.

Deferred open items: none — OI-88 is ruled; actual transfer review and semantic adjudication remain work, not outstanding owner approval. The separate legacy upgrade-window boundary remains undeclared and no legacy removal occurred.

Validation: smoke **1695 passed, 4 skipped in 49.70s** (49.94s measured wall; enforced within the 90s budget). fig: `.venv/bin/python -m pytest -q -n auto -m smoke` and `scripts/check_smoke_budget.py --mode enforce --elapsed 49.93877849995624` on `b9852757` plus this source/ruling changeset; output `out/run-logs/pc-transfer/authoring-smoke.txt`.
