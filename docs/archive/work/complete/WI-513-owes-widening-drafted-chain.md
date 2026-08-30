+++
id = "WI-513"
title = "Widen trace.reattest_model's owes() so a Drafted LLR/TC under an Approved SR reaches the owner brief (OI-61-sitting gap)"
specref = ""
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

`trace.reattest_model`'s `owes(sr)` widened past its SR-only test — the
2026-08-23 sitting's finding, executed under the owner's chosen path
("fix the surface first, approve from a corrected brief"). Record:
[../../../log.d/2026-08-24-owes-widening-and-b-brief.md](../../../log.md#2026-08-24--wi-513-widens--past-the-sr-only-test-and-oi-62-files-the-b-gono-go).

**The widening** (`project-trajectory/scripts/trace.py`). `owes()` used to
read `is_drafted(sr) or sr_chain_drifts(...)` — the SR row only, which is
exactly the discriminator that let nineteen `Drafted` LLR/TC rows sit under
`Approved`, undrifted SRs and never reach `open-items.html` or
`ratify/CURRENT.md`. It now also asks every row in the SR's chain:

```python
def owes(sr):
    if is_drafted(sr):
        return True
    chain = chain_of(sr.get("SR-ID", ""), srs, llrs_by_sr, tcs_by_ref)
    if any(is_drafted(row) for _kind, _rid, row in chain):
        return True
    return sr_chain_drifts(sr.get("SR-ID", ""), chain, snapshot)
```

Three more points kept honest so both renderers of the shared model
(`gen_open_items.py`'s HTML, `trace.py`'s markdown brief) stay coherent:

1. **The pill/kind answers for the whole chain.** `_entry_kind(sr_drafted,
   chain_has_drafted)` wears "approval owed" when the SR OR any chain row is
   `Drafted`, "re-attest owed" only for pure drift — before, a card could wear
   "re-attest owed" while the actual owed act was a first approval on a child.
2. **A `Drafted` row with no cell diff still renders**, rather than being
   silently dropped by the old `if cells:` gate. `intake.py snapshot` copies
   every registry wholesale, not only approved rows, so a `Drafted` row can
   sit in the snapshot byte-identical to its current text — never approved,
   yet producing an empty diff. Both renderers now show it (state/tag
   `"drafted"` / `"Drafted — never approved"`, or the markdown's dedicated
   section) with the reason.
3. **Every chain-row dict carries `drafted: bool`**, independent of `state`,
   so the reason a row owes — a first approval never given vs. drift vs. a
   chain amendment — is always sayable, not inferred from `state` alone.

**Driven by tests** (`tests/test_gen_open_items.py`,
`tests/test_trace_briefs.py`): a `Drafted` LLR under an `Approved`, undrifted
SR owes and surfaces; an `Approved` LLR under an `Approved` SR does not; a
`Drafted` row unchanged since the snapshot still owes; and a dynamic test runs
against THIS repo's own live spine (not a literal) asserting the widened
model's unique `drafted`-marked `(kind, id)` set equals the live
`is_drafted` count over `srs + llrs + tcs` — so it re-proves itself on every
future spine change rather than pinning today's count. Two pre-existing tests
whose fixtures/wording described the pre-widening gap
(`test_empty_attestation_state_names_only_what_it_checked`, 122-REVIEW-A) were
updated to describe the fix rather than left asserting behavior the widening
deliberately changed.

**Surfaces regenerated, no approval act taken.** `docs/open-items.html`:

- before: *"0 pending decision(s) · 1 spine row(s) owing a approval or a
  re-attest, across 1 chain row change(s); 1 row(s) drifted from the approved
  snapshot."*
- after: *"1 pending decision(s) · 10 spine row(s) owing a approval or a
  re-attest, across 20 chain row change(s); 10 row(s) drifted from the
  approved snapshot."*

10 SRs now own the 19 live `Drafted` rows plus 1 pre-existing genuine drift
(`SR-159` / `LLR-041`, unrelated to this widening) — 20 chain rows total,
matching `docs/stage`'s `drafted = 19` for the first time.
`docs/ratify/CURRENT.md` regenerated (`trace.py --approve modified`) against
the same model. Nothing was approved: the corrected brief is what the owner
approves FROM next.

Full figures, the per-SR/row breakdown, and gate output are in the log
fragment above.

## Context

The owner's chosen path, verbatim (2026-08-24, in-session): *"fix the surface
first, approve from a corrected brief."*

The 2026-08-23 sitting recorded in this row's original SpecRef
(`docs/log.d/2026-08-23-oi61-rule-and-spine-approval.md`) found a mechanism
gap and deliberately did not fix it — see "THE DISCREPANCY" in that fragment.
`trace.reattest_model`'s `owes(sr)` tested `is_drafted` on the SR row only:
`return is_drafted(sr) or sr_chain_drifts(...)`. A `Drafted` LLR or TC hanging
off an `Approved`, undrifted SR therefore reached no surface — `sr_chain_drifts`
cannot see it either, since `baseline_snapshot.is_drifted` reads False for a
row below approval ("it has made no claim to fall from") and False for a row
absent from the snapshot ("unanchored, not drifted"). Both individual rules
are correct; nothing then asked the `Drafted` question of a child. The
function's own docstring already stated the wider contract it did not
implement: *"A row now owes an act when it is `Drafted` (a first approval is
owed)"* — "a row", not "the SR row".

Effect measured at the sitting: nineteen `Drafted` LLR/TC rows
(`LLR-187/193/194/196/198/199/200/201/202`,
`TC-182/188/189/191/192/194/195/196/197/198`) were invisible to
`docs/open-items.html` and `docs/ratify/CURRENT.md` — the surfaces a human
approves from — while `docs/stage` and `docs/status.md`'s generated block
correctly counted them as `drafted`. Two surfaces agreeing with each other and
both disagreeing with the tree.

Widen `owes()` to ask every row in the SR's chain, not just the SR itself, and
keep the rendering honest about WHY a row owes (a first approval it never
received, vs. drift, vs. a chain amendment) — both `docs/open-items.html`
(`gen_open_items.py`) and the markdown brief (`trace.py --approve modified`)
read the same model and must stay coherent. Do not approve anything as part of
this row: the corrected brief is what the owner approves FROM, next.
