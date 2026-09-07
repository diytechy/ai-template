# 2026-09-07 — current-turn impact census judgment

Reviewed design proposal:
`docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`

Proposal SHA-256:
`e678a5d4628dd4d5bec383df01e20ad1a58eb83485f71fde24d0538bdd1d8821`

Reviewed authoring record:
`docs/reviews/2026-09-07-approval-contract-impact-current-turn-authoring.md`

Authoring SHA-256:
`f99a297abc1ef511514b239950ac928d27592f63d44134cae0d190fa4cc4d25d`

## Scope

This is a design judgment for the current-turn impact census
representational clarification only. It approves no live LLR/TC cell, WI-605
cell, runtime implementation, snapshot, Status change, Approval payload,
queued WI, or publication.

## Review

A candidate-wide census cannot require an Approval payload to contain the
blobs of the verdict, review, invocation, and iteration records created while
that same candidate is being produced. The proposed boundary excludes only
paths that satisfy both conditions: they are record paths under the existing
`kitlib.verdict.is_record_path` definition, and Git proves they were first
created after the immutable turn base. This resolves the cycle without adding
a new record class or a second identity mechanism.

The boundary preserves prior evidence. A record path present at or before the
turn base remains in the census, as does every non-record path in the candidate.
Those preexisting paths therefore retain exact ID/path coverage and candidate
blob binding. The separately reviewed selected-spec exception still uses the
initial `proposal_spec_blob`; it remains in the census because the selected
queued spec is not a record path, and primary definition validation plus final
Approval/Dispositions binding covers its changing sections.

The clarification does not alter the governing obligation to require exact
set equality for the applicable census, nor does it create a new workflow or
change any live registry wording. The post-base test is mechanically
verifiable from Git's path history and is narrower than excluding all record
paths, which would discard historical references.

## Disposition

**APPROVE — design clarification.** The implementation may exclude only
post-base newly created record paths proven by Git, while retaining preexisting
record paths and all non-record paths. It must preserve exact `(id, path)` set
checks and bind every retained pair to the candidate blob, with the selected
queued spec using its immutable proposal blob as the already reviewed
exception.

This is a design judgment only and grants no publication authority.
