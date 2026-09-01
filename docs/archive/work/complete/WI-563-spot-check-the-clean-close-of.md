+++
id = "WI-563"
title = "spot-check the clean close of WI-552 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

Spot-check of the GREEN close of WI-552 (the adjudicator's two exits, OI-70 as
refined by OI-73). One question asked: does what shipped answer what the row
asked for? **Verdict: yes — the close stands, no successor.**

Each of the seven Done-when arms was located in the merged tree and matched the
ask: arm 1 mechanical close (`handback.close_adjudication` +
`dispatch._close_done_adjudication`); arm 2 OI-mint
(`intake._mint_open_item`/`_inject_open_item`); arm 3 refusal invariant at both
close and merge, extended to the cancelled arm; arm 4 inbound-edge replacement
(`intake._replace_inbound_edges`); arm 5 typed OI edges
(`kitlib.spine.split_pred_edges`, `waiting:open-item-pending`,
`validate(..., known_ois)`); arm 6 `dead_dependency_findings` extended to
`partial`; arm 7 the widened brief + PROCESS_OPTIONS prose. Each arm carries a
covering test, and REVIEW-A APPROVEd after driving all seven.

One residual surfaced, latent and already on the REVIEW-A record (not a
reversal): `intake._SPEC_NEEDS_RE` (intake.py:1344) lacks `re.DOTALL`, so
`_replace_inbound_edges` silently skips a dependent whose `needs` is written as
a MULTI-LINE TOML list — arm 4's "becomes unrepresentable" guarantee holds only
under the single-line-`needs` invariant. It does not bite today: the machine
writers emit single-line `needs` and a tree-wide scan finds no multi-line
`needs` list. It was caught as REVIEW-A round-2 MINOR and shipped routed
`@owner`; it does not warrant a spine mint from this branch. Two further
round-4 APPROVE MINORs (dead `intake._OI_ID_RE`; `validate` docstring vs
`known_ois=None` coercion) are cosmetic and confirmed present. Evidence in the
log fragment `docs/log.d/WI-563-spot-check-the-clean-close-of.md`.

No spine rows minted or re-statused (adjudication row, no SR-Refs), so no
approval-brief regeneration. Read-only audit: no product code changed.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-552-adjudicator-two-exit-close.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.
