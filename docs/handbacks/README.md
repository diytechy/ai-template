# Per-close reports — the close event's own document

One immutable file per lane close that is not a clean merge (SN-031;
[handback-contract.md](../handback-contract.md)). `handback.close_partial`
writes one here and moves the claimed spec to `docs/work/partial/`; the
integrator merges the branch like any other; `intake._close_drafts` mints the
disposition row that judges it.

**The file IS the event's identity.** That is the whole design, and it is what
dissolved a defect class rather than mitigating it: five successive dedup
mechanisms had tried to answer *"is a judgement still owed for THIS close?"* by
reconstructing the event from a mutable proxy — a merge sha in a title, the
spec's last-touch commit, a digest of a note, a title token, a relationship
field — and every one leaked, silently, as an owed judgement that never
happened. A document that never moves cannot leak that way: the disposition's
title keys on this path and nothing else, so a re-sweep dedupes exactly and a
genuinely second close is a second document.

So: **never edit a report, and never delete one.** `close_partial` refuses to
overwrite an existing report rather than rewriting the record of the first
close, and restores every report it wrote if any part of the close refuses —
a half-close is not a state this ritual permits.

Naming: `WI-nnn-<branch>.md`. Contents: the claimed outcome, the reason, the
commit range, the keep/discard split (or an explicit deferral to the
adjudicator — silence about it is what merged rejected code onto trunk on
2026-08-03), and the review tier the close suggests for its own judgement.

This directory is empty in the kit's own repo, which is the honest state: no
lane here has closed early since the contract shipped.

---

## The other half: `docs/work/partial/`

The spec itself moves to [`docs/work/partial/`](../work/partial/), which is
**TERMINAL**. Nothing re-claims a row from there, so nothing strands — that is
what it buys over the retired shape, which put the spec back in `queued/` behind
a `blockref` and left an owed judgement hanging on a mutable marker. Continuing
the work means the adjudicator DRAFTS A SUCCESSOR carrying `supersedes =
"WI-nnn"`, so the thread survives the id change while the closed row's scope
stays exactly what it was.

The moved spec's definition is **byte-identical** to what it was before the
close. Only its location changed, and what the report here says about delivery.
"Scope definitions never change; only whether they were delivered" is the rule,
and it is why R-A's terminal-Deliverable requirement EXEMPTS `partial`: the
record of what happened lives in the report, and demanding a Deliverable cell as
well would demand a second, weaker copy of it — one that is unsatisfiable by
construction, since the whole point is that the definition did not move.
