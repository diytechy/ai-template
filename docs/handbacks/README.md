# Per-close reports — the close event's own document

One immutable file per lane close that is not a clean merge (SR-144;
[handback-contract.md](../archive/history/handback-contract.md)). `handback.close_partial`
writes one here and moves the claimed spec to `docs/archive/work/partial/`
(WI-504, OI-55 ruled (a) — the terminal directories relocated under the
archive 2026-08-22; this report's own home, `docs/handbacks/`, did not move);
the integrator merges the branch like any other; `intake._close_drafts` mints
the disposition row that judges it.

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

**First exercised 2026-08-15**, by the WI-451 re-tier campaign closing `partial`
on an owner ruling that a partially completed re-tier is within the design
expectation. That first run found a real gap and it is recorded rather than
quietly patched: the contract shipped with **no `docs/orphans-allow` entry**, so
the very first report written made `check_docs` fail the full suite with "orphan
doc (no path from an entry root)". A report is deliberately linked from nowhere
— its path is the event's identity, and the disposition row is what makes it
reachable as work — so the allow entry, not a navigation link, was always the
right home. Both this repo's `docs/orphans-allow` and the shipped
`orphans-allow.template` now carry it; adopters upgrading past this point get it
via `RESYNC_PACK.md`.

---

## The other half: `docs/archive/work/partial/`

The spec itself moves to [`docs/archive/work/partial/`](../archive/work/partial/),
which is **TERMINAL**. Nothing re-claims a row from there, so nothing strands — that is
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
