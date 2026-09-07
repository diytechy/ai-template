# Supervisor disposition — retire the stopped primary selection

Resume item 1: retire `WI-605-b830f202c551c7c11d1a63ea4baff84a7ff6e596`;
do not resume or publish its candidate. The owner authorized this choice in
the [post-stop resume prompt](../handoff-2026-09-07.md#resume-prompt-2026-09-07-after-the-stop).
The invocation's abbreviated candidate cannot bind its judgment, and subsequent
supervisor commits changed the candidate surface. Repairing code cannot make
that historical invocation valid.

The selection's exact bytes now live in the
[retired evidence home](retired-primary/WI-605-b830f202c551c7c11d1a63ea4baff84a7ff6e596/turn.toml),
outside `primary_publication.pending`'s active `docs/reviews/primary/*/turn.toml`
scan. This is an explicit supervisor retirement, not a completed publication
or an automated recovery route. The original path remains in Git at selection
commit `65eda1bff8ec37a2594f2d205e12569df350663d`.

The queued proposal is restored byte-for-byte to blob
`9e5967174d0e38727273e1d31a34c7bf4c8d167d` from the turn's launch base.
Its unaccepted Approval and Dispositions remain preserved at carrier commit
`fa90a5b73ead04ee8dfbf151a53eeca5cddf1c86`; neither draft is minted. The
[judgment](contract_split/001-ADJUDICATE-65eda1b.md) and
[actual invocation log](../iteration/contract_split-001-20260907-040924.log)
stay at their original paths and bytes. Their findings remain unaccepted.
The [observations](../ai-template-redesign-2026-09-05-codex/CONTROL-APPROVAL-OBSERVATIONS.md)
retain the stopped HEAD, transcript evidence and legacy lane identities.

WI-605 stays queued with its original scope; its dependent WI-606 stays queued.
Later judgment needs a fresh selection at its then-current base and separate
execution authority. No governing cell, snapshot, policy, legacy branch or
forensic patch changes. The tracked pause remains and the coordinator stays
stopped. The remaining resume items precede package PC.

Source review: `pending` reads only the active selection home, and
`writer_refusal` delegates to it. Moving the record therefore releases the
durable writer boundary without weakening either validator or forging a
publication. Verified the archived selection's Git blob equals its original,
the restored spec equals the bound proposal blob, and both `pending` and
`writer_refusal` return `None`. This is a supervisor source review, not an
independent adjudication of the preserved findings.
