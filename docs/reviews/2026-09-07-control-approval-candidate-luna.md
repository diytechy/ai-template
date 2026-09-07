# Control approval candidate audit — 2026-09-07

## Scope and disposition

This is a bounded, read-only audit of the stopped `contract_split` control
window. I did not read `OWNER_SCRATCHPAD.md`, change source or tests, request a
new control window, or treat this record as an approval. **Disposition:
RETURN / cannot advance.** The first primary telemetry record carries an
abbreviated candidate that the approval verifier must reject.

## Exact evidence

The inspected telemetry is
`docs/iteration/contract_split-001-20260907-040924.log`. Its binding fields
are:

```text
# base: b830f202c551
# phase: ADJUDICATE
# primary-turn: WI-605-b830f202c551c7c11d1a63ea4baff84a7ff6e596
# judgment: docs/reviews/contract_split/001-ADJUDICATE-65eda1b.md
# candidate: fa90a5b7
# commits: 65eda1bf..fa90a5b7
```

The candidate recorded in the session metadata is eight hex characters.
Resolving that ref gives the full commit
`fa90a5b73ead04ee8dfbf151a53eeca5cddf1c86`. The verifier's
`primary_approval._HEX40` contract requires exactly forty lowercase hex
characters, and `_judgment_record` rejects a metadata candidate that does not
match it. Therefore this telemetry cannot establish the candidate/judgment
binding needed for a read-only projection. The subsequent ADJUDICATE attempt
was a correct refusal to advance, rather than evidence of approval.

The exact runtime caller is:

* `project-trajectory/scripts/agent_loop.py:4049` calls
  `primary_adjudication.session_binding(root, worker, plan, after)` after the
  session metadata is assembled and before `write_session_log` at line 4050.
* `project-trajectory/scripts/primary_adjudication.py:135-143` returns
  `candidate: candidate` for an ADJUDICATE primary turn. In this invocation
  that argument was the shortened `after` value `fa90a5b7`.

Thus the defect is in the real session metadata path: the caller emits the
short commit-range result without normalizing or rejecting it before binding
the session record. The approval verifier correctly remains strict.

## Testing gap

The existing approval fixtures exercise the parser and projection with
synthetic metadata containing full commit IDs; they do not exercise a real
`agent_loop` session through `session_commit_range` (the `after` value),
`session_binding`, and `write_session_log`, followed by the verifier's
forty-hex candidate check. That missing integration case allowed the first
telemetry file to contain `fa90a5b7` while the underlying commit was valid.
This finding is evidence for a future test/implementation handback only; no
source or test change is made in this audit.

## Launch-to-stop effects

I compared launch base
`b830f202c551c7c11d1a63ea4baff84a7ff6e596` with stop `HEAD`
`79115aab19d4bdb023a14f19f4b7d852cd8db56b`. The changed paths were limited
to the session log, the judgment review artifact, the primary-turn metadata,
and the queued WI-605 document. Path-scoped checks showed no changes to the
SN/SR/LLR/TC registry Status cells, `docs/archive/last_approved` snapshots,
terminal/complete work records, or the ID watermark/mint paths.

The queued WI-605 document and review/telemetry artifacts are evidence of the
stopped attempt. They do not publish a Status transition, snapshot, terminal
close, or minted identity. No such effect is accepted by this record.

