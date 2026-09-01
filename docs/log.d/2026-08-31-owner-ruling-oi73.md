## 2026-08-31 — the owner rules OI-73 ((a), the full posture: typed OI edges in `needs`; a successor at every partial close; inbound edges replaced at the mint)

Deferred open items: none — the one row raised on 2026-08-31 after the
OI-70/71/72 sitting is ruled by this entry, and no other row is pending.

The ruling was made in session, the owner's words recorded verbatim; the row's
`one_line` and `decision` cells carry the ruling at their head (the OI-67
convention). The ruling is on [../open-items.html](../open-items.html); the
evidence base is the same-day survey of the hand-back mechanization recorded
in the row's `decision` cell (the two measured gaps: the unordered mixed
outcome, and the silent dependent-of-`partial` strand repaired by hand at
`b708a604`).

### OI-73 — RULED: (a), the full posture

The owner, raising the item (on whether a partial close's dependents should
re-point): *"Any WIs that required the WI as a dependency would just get
replaced to the followup WI, but this means any partial WI MUST followup with
at least a WI, and that WI MIGHT have a dependancy on a new OI if it requires
human input if the adjudicator could not find an alternative."* And ruling it:
*"Agreed with recommendation, please update the frontier and current WI scope
as needed."*

What is ruled. **Option (a).** Four arms, one mechanism:

- **Typed OI edges.** An `OI-###` id becomes a valid HARD token in a WI's
  `needs` list, satisfied when the row leaves `pending`; validated for
  existence through the spine carrier and the id-watermark's OI space; read by
  both loaders, the validator and the scheduler (a new waiting reason). The
  grammar widens tolerantly — bare WI ids keep meaning what they mean, no
  downstream flag day.
- **The mandatory successor.** Every `PARTIAL` or `CANCELLED` disposition must
  queue at least one successor WI. OI-70's exit-(B)-alone case is retired: the
  refusal invariant tightens from "names neither a queued successor nor a
  minted OI id" to "queues no successor" — an OI alone no longer discharges
  the close.
- **The OI as a dependency, not an exit.** Where the answer is human-owed and
  the adjudicator found no alternative route, the close still mints the OI —
  and the successor carries it in `needs`, so the ruling gates the successor's
  readiness instead of relying on adjudicator restraint.
- **Replacement, not report.** The mint REPLACES the superseded row's inbound
  hard `needs` edges with the successor — the WI-541 strand class becomes
  unrepresentable rather than merely visible. `dead_dependency_findings`
  extends to `partial` predecessors as the validator net for anything minted
  outside this path.

What it commissions: no new row — WI-552 already owns the adjudication-row
close and is re-scoped in this commit to carry the four arms (its Done-when 2–4
amended, the typed-edge mechanism and the validator net added), per the
ruling's own sequencing: rule first, amend the row before it is worked. The
row sits on the ready frontier; nothing else moves.
