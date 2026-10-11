# WI-887 dispute 011 — finding DC

Ruled at ff9b7fac3, lane range b3ef42844..1e11dd4de, within the bound set by
PROCESS.md §6 "Review threat model".

## DC — a malformed nested lease reads as no lease, and the held session is resumed

**Observed.** I wrote a full scoped OPENAI review record under its own `_record_name`, with `lease = {"holder": H, "until": now + 3600}`.

| holder `H` | `_read_record` | `_lease_held` | `retire_stale_lease` |
|---|---|---|---|
| `[]` | admits it | `''`: no holder | `False`: not retired |
| `None` | admits it | `''` | `False` |
| `0` | admits it | `''` | `False` |
| `"other-holder"` (well formed) | admits it | `"other-holder"`: held | `False` |

In `keep_for` (~906–917) an empty `busy` goes straight to `_hold`. `_hold` overwrites the lease with the caller's own and, the record being active, resumes its session.

So a live lease whose holder is not a string is read as no lease at all. The call takes over a transcript the lease says another call holds. That is the two-calls-on-one-session corruption the lease exists to prevent (LLR-270: "let no two calls use one retained session at once"). It fails toward resuming, the opposite of the lane's fail-closed contract. A well-formed holder in the same position correctly makes the call wait, then run unretained.

**Correction of dispute 008.** 008 said nested lease values "are already guarded at their consumers and need no change". That is half right. `_lease_held` and `retire_stale_lease` check that the lease is a dict and that `until` is a number, but not the type of `holder`: `lease.get("holder") or ""` turns any falsy non-string into "no holder". 008's statement is wrong for `holder`, and this finding is the gap it left. It is not refuted by 008.

**Scope.** The coordinator's out-of-scope argument is the one 008 weighed and rejected for DA, and nothing distinguishes this case:

- Both reproductions need a mistyped value in the kit's own runtime store, not a compromised host, binary or tool.
- The lane itself made "malformed record means no session" a SUPPORTED behaviour, in its Trust ruling, SR-239 and LLR-270 ("all consumed fields typed").
- `holder` and `until` are consumed fields.

Ruling DA in scope and DC out of scope would split one boundary at a line nothing in §6 draws.

**Worth the cost.** The cost is small, and the defect is worse than DA's: a crash there, a silent shared transcript here.

**Remedy.** `_variant`'s declaration types the lease's inner fields as its writers produce them: `holder` a non-empty str and `until` an int or float. A lease that fails that is no record, so the call mints. Add the service-level regression the reviewer names: a live record whose lease holder is mistyped yields a fresh session, not `--resume`.

So the declaration leaves no consumed nested value untyped, it also types `judged`'s items as str, since its consumers test work-item ids for membership in it. With that, every top-level and nested field any consumer reads is declared once at the reader, and the class this lane has reviewed four times is closed. Re-attest LLR-270 and TC-351 through a sitting if their text changes.

RULING: DC FIX _read_record admits a lease whose holder is not a string (observed with [], None and 0 under a live until), and _lease_held reads that falsy holder as no holder, so keep_for takes over and resumes a transcript the lease says is held, contrary to the lane's fail-closed contract and LLR-270's one-call-per-session rule; dispute 008's statement that nested lease values need no change was wrong for holder; type the lease's holder (non-empty str) and until (number), and judged's items, in _variant's one declaration, with a service-level fresh-session regression
