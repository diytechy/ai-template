## 2026-08-28 — the owner rules OI-64 (b) and OI-65 (b')/(i)/(iv)

Both rows were rewritten for legibility earlier this sitting (`d0f16357`) after
a cross-family review round; the owner then ruled the recommendations as they
stood. This fragment is the ruling record their `ruling_ref` cells cite.

Deferred open items: OI-66 — the go/no-go on the header build's price, filed
this sitting as the carrier (b') owes.

### OI-64 — RULED: option (b), state the contract, sweep nothing

The owner: *"I'm good with the recommendations on the OIs as well."*

What is ruled: the finding/severity/exit protocol is **stated once at the
interface tier**, and no existing row is edited. The ten restating rows keep
their own wording; new rows cite the contract instead of restating it. Option
(a)'s sweep stays available and unruled — it cannot be executed today anyway,
because an SR row has no field for citing an interface.

**The guard carried from the row:** the contract does NOT carry *every degrade
is named, never silent*. `SR-181`'s acceptance permits a silent degrade
(*"degrades silently (reports nothing) when no prior committed state is
available to compare against"*) while `SN-008` forbids one, so a contract
carrying that clause would land red on an `Approved` row on the day it is
stated. The clause is left out and the contradiction is recorded, unfixed.

**The shape question, raised and then answered on the evidence.** It first read
as a blocker: an interface row carries one `provider` (29 rows) or one
`component` (55 rows), and this contract has fourteen providers whose ten
restating rows split **five and five** across `CMP-006` and `CMP-007`, with
`SR-181` in neither. That was the wrong axis. The protocol is not a
module-to-module seam — it is what the delivered harness presents at its
**package boundary**, and all ten restating rows cite **`B-05` unanimously**.
Twenty-eight interface rows already carry `interface_to_external = "B-05"`, so
the row takes an established shape rather than a new one. The owner's own
direction anticipated this in saying an external far side is a boundary-line
interface. Executed as **`IF-144`** (`WI-526`); no further ruling was needed.

### OI-65 — RULED: (b') placement, (i) the ten passages, (iv) the lint

The owner: same message, and the follow-up *"I assume you will surface the
'cost' of transfer to the module header as a new oi?"* — which is what (b')
owes and is now `OI-66`.

**(b') placement.** The component-side contract header is committed to **in
principle**; no cell moves and no code changes until the build is priced and
the owner accepts the price. Execution row: **WI-525** (the pricing study),
whose output is ruled at **OI-66**. If the price is beyond appetite the row
returns to (a), keep-in-cell — that fallback is part of what is ruled, not a
later re-opening.

The pricing must include the **harvester fix**, not only the new artifact and
its gate: `gen_arch_map.module_contracts` already reads `handback.py` as
declaring `IF-080` although that docstring says *"No `Contracts:` line,
deliberately"*. A negated declaration is read as a declaration, so the header
mechanism cannot be costed as though the existing harvester works.

**(i) the ten passages.** The eight provenance and duplicate spans are deleted;
`IF-117` and `IF-061` are **corrected to what is true now** rather than deleted
into silence. All ten rows read `Drafted`, so no re-attestation is owed.
Execution row: **WI-524**.

**(iv) the lint.** `rationale` joins `IF_REASON_CELLS`, and `_WI_TOKEN_RE` stops
being case-sensitive. Driven before the ruling, not estimated: the widened arm
finds **0 findings** across the current 37 `rationale` cells, and the case fix
finds exactly **3** — `wI-280` on `IF-082`, `IF-083`, `IF-084`. Execution row:
**WI-523**.
