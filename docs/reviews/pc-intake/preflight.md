# PC intake and publication preflight

Baseline: `14ac5251bc5d1f6a39a1d2fc0867d8af3a5da7ac`.
The owner authorized continuing the [PC proposal](../../ai-template-redesign-2026-09-05-codex/PC-BATCH-CONTRACT.md),
with the coordinator paused and no control window, push or merge to main.

## Actual publication constraint

The [diagnostic output](preflight.txt) calls the existing read-only helpers on
the real baseline LLR census. It assumes evidence references validate, using a
local mock solely to isolate the scope condition; this creates no judgment,
Approval payload, primary selection or snapshot. Even with that assumption,
`_absorption_refusal` reports `approved-cell absorption LLR-140 has no accepted
scoped decision`. Adding that decision to WI-601 instead makes
`_decision_rows` report `decision LLR-140 is outside the turn scope`.

The actual approved-change LLR population is LLR-061/140/152/153/154/158/167/183/207.
WI-601 owns only LLR-061. The verifier requires all approved-change riders to
have an accepted decision in the same turn, while the scope parser prohibits
those other decisions. Separate completed judgments cannot satisfy these two
conditions simply by being cited in the absorption ledger. This is a
composition constraint, not permission to widen a scope or weaken either check.
The safe outcome remains no snapshot publication.
A zero-effect RETURN can still close a primary turn; the diagnostic proves
accepted re-anchoring is blocked, not that every terminal outcome is impossible.
Starting such a turn now would not satisfy PC's contract-acceptance prerequisite.

## Independent judgment and source corrections

The real [independent review](review-result.md) approved bounded reversible
intake only. [Metadata](review-meta.json) binds the frozen `review-prompt.txt`
and actual configured ANTHROPIC-FABLE session; its raw stream remains locally
under `out/run-logs/pc-continuation/`. This opinion approves neither a repair
implementation nor any registry cell.

Two reviewer assumptions were outside the supplied source and are corrected
here without altering its original response:

- The complete queued `adjudicates` census includes WI-605 as LLR-183's owner,
  as well as WI-601 for LLR-061 and WI-603 for LLR-167. LLR-152's cumulative
  owner is the future PC amendment WI. LLR-140/153/154/158/207 have no explicit
  queued owner in this baseline; that does not establish absence of historical
  judgments. The repair must distinguish missing evidence from valid evidence
  belonging to another scope and inventory the SR/TC populations as well.
- `intake._amendment_drafts` emits one amendment draft **per merge**, with all
  changed row IDs, rather than one draft per row. The PC authoring merge would
  therefore propose a scope overlapping WI-601. Reconcile that proposed scope
  through reviewed intake before selection; do not close, duplicate or silently
  transfer WI-601. The eventual PC amendment WI must exclude LLR-061 and carry
  the required hard predecessor on WI-601.

## Concrete intake

The canonical `intake.stage_mint` produced the new specs and watermark in a
pristine disposable checkout. Those exact outputs were copied to the primary
checkout under the existing dispatch and integration locks, after checking the
base, clean tree and absence of a pending primary writer. No coordinator or
primary engine ran. [The mint record](mint-result.json) names the actual files.

- [WI-608](../../work/queued/WI-608-apply-the-reviewed-pc-single-w.md): exclusive
  authoring of the exact reviewed PC patch; no approval or snapshot changes.
  Applying it increases drift and does not make WI-601 publishable.
- [WI-609](../../work/queued/WI-609-resolve-scoped-judgments-versu.md): a separate
  scoped resolution of the publication-composition conflict, including its
  governing contract impact and positive/negative acceptance cases. It must
  first establish whether a valid existing route was missed. It does not
  authorize unrelated runner changes inside PC or implement an unreviewed
  substitute approval path.

Existing adjudication owners remain queued and unchanged. Do not select a
primary approval turn over these carriers while this conflict remains. The
resolution must be independently reviewed and its necessary follow-ups
completed before selection; closing a design WI alone is not a working repair.
The tracked pause remains. No live registry, snapshot, code or test was edited.
