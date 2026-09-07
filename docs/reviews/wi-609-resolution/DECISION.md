# WI-609 — proposed one-time ownership transfer

**Proposed decision:** authorize a reviewed, supervised transfer of the queued
amendment scopes in WI-601, WI-603 and WI-605 into one new combined adjudication
WI for the affected registry snapshot set, after exact PC source authoring.
This is a queue-ownership decision, not approval of any requirement or code.
No transfer, new primary selection or snapshot write has occurred.
The decision is recorded as OI-88; WI-609 has a hard dependency on that answer.

## Why this is the smaller route

The [independent design review](review-result.md) returned the proposed
judgment-only publication mechanism. It would add a protocol intent, reusable
foreign-judgment validation, a collection hold and a bootstrap exception. The
[rejected design](rejected-judgment-only-design.txt) is retained as review input,
not as a second implementation plan. The review instead identified a combined
scope under the existing publisher as the smaller way to drain the current
backlog without weakening scope or absorption checks.

[The exact proposed scope](combined-scope.json) is derived from the corrected
PC candidate's actual whole-file census. It includes every changed Approved row
that those three files would absorb. Drafted riders are listed separately and
remain Drafted. This replaces the earlier PC proposal's dependency on an
independent WI-601 close with one owner for the complete atomic approval set;
it must therefore be explicitly approved as an ownership transfer.

The [isolated executable check](combined-scope-check.txt) calls the real scope
parser and absorption verifier on that candidate. Assuming accepted judgments
and valid evidence solely for diagnostic isolation, both constraints pass for
the combined scope. They fail for the current WI-601-only scope. This proves
scope consistency, not semantic approval, impact coverage, valid provenance or
publication readiness. The real judgments remain to be performed.

## Exact effect of the proposed authorization

1. Retain the paused coordinator and no-control-window/no-push/no-main-merge
   constraints. Do not modify any currently bound primary turn; none is pending.
2. Complete the exact PC authoring under WI-608, with no approval or snapshot
   changes. Recompute the census at its actual committed candidate. If it differs
   materially from the proposed scope, return the changed transfer for review.
3. Independently review the complete transfer and lineage before its queue
   mutation. Use canonical intake/spec-move helpers for the new owner and
   restructured historical specs; preserve original scopes, proposals, real
   review evidence, stopped WI-605 incident records and successor lineage.
   Do not claim the old owners accepted their rows or mark them complete.
4. The new adjudication owns the exact combined Approved-change set in
   `combined-scope.json`, with WI-608 as its hard predecessor. No new WI ID is
   reserved here. Replace obsolete dependent edges through the existing
   lineage-repointing path; review every affected edge and prohibit self-edges.
   The previous not-yet-minted PC amendment WI is unnecessary: its intended
   scope is included in this one owner. Existing first-approval ownership of
   Drafted rows is unchanged.
5. Only after that transfer and authoring are complete may the new exclusive
   primary adjudicator judge each row's cumulative approved-to-candidate text,
   parents, siblings, tests and every meaning-changing use. Require a complete
   real absorption ledger and ordinary independent review/provenance. A missing
   or rejected judgment still refuses the whole copy. No manual snapshot copy,
   synthetic approval, weakened check or new publication mechanism is authorized.
6. After successful live contract acceptance, continue PC implementation under
   its existing scope and test obligations. This decision does not authorize a
   new control window. Any recurrence prevention that changes runner scheduling
   requires its own scoped review; no new merge-time hold is smuggled in here.

## Why approval is requested now

The current [WI-609 scope](../../work/queued/WI-609-resolve-scoped-judgments-versu.md)
explicitly says “Preserve WI-601, WI-603 and WI-605 ownership”. The accepted PC
proposal also requires the separate WI-601 judgment and predecessor. The normal
automatic consolidation census refuses while queued adjudications exist
(`consolidate._pending_refusal`), so simply launching that census is not a
supported way around this constraint. This proposal asks for a one-time
supervised ownership change with independent review, not deletion of that guard.

The original answer that no input was needed was too broad: diagnosis and
preparation required none, but this chosen resolution changes the recorded
ownership boundary. The alternative is a larger protocol change that also
needs a bootstrap decision. The recommended transfer keeps existing approval
semantics and all publisher checks intact. The unrelated oldest-supported-kit
question for legacy expiry does not block this decision.

## Evidence and present state

The existing primary approval/publication tests passed unchanged. Actual output
is recorded in the session log. Reviewer metadata and frozen prompt are preserved
beside the verbatim review; the review is not a machine approval artifact.
Production code, SR/LLR/TC registries, snapshots, existing amendment ownership
and the tracked pause are unchanged. Only the owner question and WI-609's
dependency on it were added to the live registries. WI-609 remains queued; no false claim or completion
is recorded while work is performed as supervised proposal preparation.
