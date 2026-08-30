## 2026-08-30 — sitting: the three stranded claims become parked lanes again, and the two owner-owed rows carry the owner's delegation for an unattended run

Deferred open items: none — the owner delegated in session; nothing is owed a
ruling.

**Summary.** The owner will be away while a fresh session drives the
mechanized loop, and asked what the open rows would wait on them for and
whether the rows or the prompt needed changing to run unattended. Two things
did.

**Three claims were stranded.** `docs/work/active/` held the claim
directories for `WI-484`, `WI-508` and `WI-521`, but none of the three branch
refs existed any more — the slices were built by hand on the trunk checkout
and the lane branches were never re-cut. The dispatcher resumes a parked lane
only when the claim directory AND the ref exist (`dispatch._parked_branches`),
and the scheduler lists an `active` row as ready, so the loop would have
neither resumed nor claimed them — the "spec in `active/<branch>/` with no
branch to build it" case the integrator's own docstring names as the hand
repair. The three refs are re-cut at trunk HEAD; the dispatcher now reads all
three as parked (`WI-484` and `WI-508` exclusive on the spine class, `WI-521`
parallel), verified by driving `_parked_branches` and `_branch_exclusive`
directly.

**Two rows deferred to the owner, and the dial does not.** `WI-508`'s Context
said its four `Drafted` rows "await blessing — no session may flip them", and
`WI-484`'s said the `hats.toml` `knowledge` values are "owner text, not an
agent's act" and its 17 duplicated approved `Rationale` cells are
"owner-adjacent, not taken". `docs/process.toml` holds only `DevStg-Needs`
human-held, so LLR/TC approval and SR/LLR amendment proceed under ordinary
review; the roster's own header asks the owner to cut at RETURN, not before an
agent drafts. The owner delegated both in session (*"I thought the hats.toml
would just repoint to what was there or draft out according knowledge"*): each
row's Context gains a **Delegated for the unattended run** section — the lane
approves the four rows through the ordinary flow and closes `WI-508` (its
other item, `OI-64`, was ruled 2026-08-28); the `WI-484` lane drafts the
`knowledge` values (re-point to `docs/knowledge/` packs, draft only where none
carries the perspective, mark drafts) and may trim the duplicated prose under
review — and both list what they did under a heading the owner can find.

**What the run may still stop for, on record:** the loop's own fail-closed
exits — no routable model of a tier, an adjudication row with no usable
brief, a worker page with a `stop` consequence, a dual-plan page — and the
supervisor session holds the owner's delegation to dispose those with the
best decision available, recording each in a decisions-for-review file; the
genuine stops are the approval dial, the `[policies]` block, a destructive or
irreversible act, and any push to a remote.

**Deviations from spec:** none — bookkeeping and two Context amendments the
owner asked for.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** smoke tier under Git Bash **1378 passed, 6 skipped in 29.58 s** — the budget read **30.0 s vs 60 s → within** on a quiet box (the WI-496 re-tier's own reading, 27 s, is now reproduced within a few seconds); `check_trajectory --strict`: exit 0;
`check_docs --stale`: 0 broken; every generated document current.
