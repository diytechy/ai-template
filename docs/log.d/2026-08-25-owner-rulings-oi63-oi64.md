## 2026-08-25 — the owner rules OI-63 (d) and directs OI-64 to the interface tier

Both statements were made in session, in one message, and are recorded
verbatim on their rows. This fragment is the ruling record the rows'
`ruling_ref` / recommendation cells cite.

## OI-63 — RULED: option (d), the non-crossing cleanup first

The owner: *"OI-63: recommendation is okay at least to move information to
rationale to clean up the contract text itself before further shuffle. But
note that C says '(the far side is often a file or an external party with no
module to hold a header)' but that indicates the file is itself the
interface, and can still be defined / set by the owning header contract, so
long as others refer back to it, and an external party should just be a
boundary line interface."*

What is ruled: the non-crossing (M/X) content leaves `contract` for the
row's `rationale` field, BEFORE any placement shuffle; the placement
question is re-asked on the cleaned cells. Execution row: **WI-522**
(filed this sitting). The (c) correction — a file far side IS the interface
and its format is the producing side's contract to define; an external far
side resolves to the boundary tier — is recorded on the row for the re-ask,
which materially weakens the old objection that Consumes rows have no
header home.

## OI-64 — OWNER DIRECTION recorded, row stays pending

The owner: *"yes this is also my concern. Technically a 'contract' is a
requirement, but specifically an interface type. Interfaces can be numerous,
so I don't think it needs to be elevated to an LLR, and interfaces already
trace back to their LLRs, but either way the method should be consistent.
Either the interface contract (whereever it lives) defines the interface
expectations, or the LLR does."*

What the direction changes: the finding/severity/exit contract, if stated,
is stated at the INTERFACE tier — not minted as a new SR, not elevated to an
LLR — and the kit-wide method rule is one definer per interface expectation:
the interface contract or the LLR, never both. The measure-vs-state choice
((c) before (a)/(b), or decline) remains the owner's; the row stays
`pending` with the direction folded into its recommendation cell.

The one-definer rule is cross-cutting: OI-63's re-ask must honour it, and
it is the same single-source principle the kit preaches
(decompose-don't-paraphrase), now stated by the owner for the interface
tier specifically.

## The bar at this commit, measured honestly

Registry/docs-only diff (two OI cells, one queued WI spec, the watermark,
this fragment, regenerated surfaces): `check_trajectory --strict` clean
(519 WIs), `check_docs --stale` 0 broken, smoke **1363 passed, 6 skipped**
— green on results. The seconds half read **101.7s / 102.1s** on two
consecutive enforced runs against the 60s budget, on a box measured at
**74% CPU under an interactive non-repo load** (a game client at 93
CPU-minutes, 7.3 GB resident) — the same tier at the same HEAD measured
**22.9s** in the WI-521 sitting on a quiet box. The budget is NOT
re-stamped and no module is re-tiered off a loaded-box reading, per the
standing rule and the WI-518/WI-521 precedent: one box is one data point,
and timing a tier under someone's game measures the game.
