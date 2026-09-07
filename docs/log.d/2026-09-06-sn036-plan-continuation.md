## 2026-09-06 — Perspective-review amendment and redesign continuation

The owner accepted OI-86/OI-87's recommendations and authorized continued
redesign execution with Sol, Terra and Luna implementation agents and Claude
Opus 5 CLI adversarial review. The [ruling record](2026-09-06-oi86-oi87-owner-ruling.md)
settles those cards; the LLR-041 residue was already approved and snapshot-aligned
at `13593db9`, so no duplicate adjudication was minted.

Applied the [SN-036 owner ruling](2026-09-06-sn036-owner-ruling.md): SN-036's
acceptance now uses the hat-by-hat review record, SR-161 uses the existing
brief/review mechanism with Inspection verification, LLR-183 retains row-level
Hat-Refs provenance, and SR-186/TC-211 inspect the real review record. TC-211
now directly cites SR-161 as well as SR-186. No new coverage carrier, cell,
checker, or backfill was introduced. The SR-161 rationale cites the ruling as
it expressly required; the existing citation-frame advisory is accepted for
this scoped owner-directed citation.

The needs-only snapshot command was
`intake.py snapshot --approves docs/requirements/stakeholder-needs.toml=docs/log.d/2026-09-06-sn036-owner-ruling.md`.
The live/snapshot needs delta before the copy contained only SN-036 acceptance;
its need and why are unchanged. The other registry snapshots were untouched.

Queued the amendment adjudication and its dependent first-approval batch through
the existing spec writer and watermark allocator. Their specs keep older
snapshot drift explicit and preserve the existing adjudications. In particular,
TC-178's mechanical Hat-Refs evidence is supplementary; it cannot substitute for
TC-211's Inspection. Authoring and actual Inspection results do not approve
the Drafted SR/TC rows. Those acts remain with the queued adjudicators.

The [first Opus review](../reviews/2026-09-06-sn036-decomposition-structured-opus.md)
requested changes; the [fresh closure review](../reviews/2026-09-06-sn036-closure-structured-opus.md)
approved after correcting SR-186's duplicated clause, TC-178's Expected claim,
and the historical result's tense. [Dispositions](../reviews/2026-09-06-sn036-review-dispositions.md)
retain the advisories and correct the reviewers' inaccurate rubric-digest
abbreviations without altering their original verdicts. The actual full digest
and launcher-bound prompt identities remain available.

The [fresh TC-211 Inspection](../reviews/2026-09-06-sn036-inspection-structured-opus.md)
reports PASS for the actual review record and the two abnormal cases. Its
separate record findings prompted the source-manifest corrigendum, one current
preflight observation, and completion of the test-registry absorption ledger.
The original reviewer bodies and earlier incomplete execution remain intact.
The [final bounded record review](../reviews/2026-09-06-sn036-records-final-structured-opus.md)
returns APPROVE after those corrections; its two procedure wording nits are
applied without changing the method or result.

Validation on the stable authored tree:

- Smoke: **1680 passed, 4 skipped in 58.17s**.
- Enforcing smoke run: **1680 passed, 4 skipped in 59.69s**; measured wall time
  **60.0s versus the declared 90s budget**, within.
- Strict trace: **orphans=0, integrity=0, placeholders=0, schema-findings=0**;
  strict trajectory: clean, acyclic. Docs/stale: zero broken links; existing
  warnings/hints remain visible. Generated surfaces refreshed through
  `trunk_step.py --regen`.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=a6b54584+oi86-sn036-final; out/run-logs/oi86-smoke-stable.txt -->
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=a6b54584+oi86-sn036-final; out/run-logs/oi86-commit-smoke-budget.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/trace.py --strict --no-placeholders --strict-schema" rev=a6b54584+oi86-sn036-final; out/run-logs/oi86-trace-final.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=a6b54584+oi86-sn036-final; out/run-logs/oi86-docs-final.txt -->

Failed-first evidence: an early trace read overlapped the OI file's authoring
write and refused invalid TOML; the stable file parsed and strict trace passed.
An intermediate smoke run copied the new documentation WI before its opening
frontmatter fence was corrected, producing one failed case and four setup
errors. Its fixture starts with `id =` while the finished spec starts `+++`;
all writers finished before the stable rerun above. No check, threshold, test
or parser was changed to clear either result.
No byte-capped or byte-watched guide changed (budgeted-file delta: zero).
This is a mid-phase documentation/registry slice; it does not claim a new
unfiltered suite, phase close, live control observation or replacement decision.
The tracked pause and policy dials remain unchanged, and nothing was pushed.

Deferred open items: none — the two owner cards are ruled; the control's exact
reviewed pause deletion remains the separately recorded owner launch act in
[CONTROL-DECISION.md](../ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06).
