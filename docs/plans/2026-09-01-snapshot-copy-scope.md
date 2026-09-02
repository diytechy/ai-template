# The snapshot copies only what the act authorises: `copy_live` scoped to the flipped registry and the named `--approves` refs

**Status:** plan of record for the row minted against it. Authored 2026-09-01
(evening supervised session) from the owner's question on `OI-78` — "I would
never expect a work lane to modify the content of the last-approved
directory" — and a read-only investigation of the mechanism (an independent
Opus pass; commands quoted in the 2026-09-01 log addendum that files this).

## 1. The problem, measured

`baseline_snapshot.copy_live` iterates every registry in `SNAPSHOTTED` — all
seven — unconditionally (`for rel in SNAPSHOTTED: … shutil.copyfile(live,
dest)`, baseline_snapshot.py:679-696). `intake._apply_flips` is a dead arm
(OI-45 ruled (b): the action writes nothing), so `intake.py snapshot` is the
one door, and every invocation re-baselines the WHOLE tree regardless of
which registry the approval act touched. A `Status` flip on two LLR rows
therefore drags interfaces.toml, external.toml and components.toml along,
and any trunk-side off-spine drift present in the live files at that moment
is re-sealed as a side effect.

The guard did not refuse because it had nothing to refuse: `refresh_refusal`
blocks only rows whose SNAPSHOT copy claims approval and whose approved cells
moved; every interfaces.toml row is Drafted on both sides (snapshot 135 rows,
live 163, all Drafted), so by its own doctrine "copying it re-blesses
nothing". True of approval; false of the CENSUS — the only rendering of
off-spine change is computed against the snapshot, so the whole-tree copy
silently zeroed it (132 changed / 30 added / 3 removed → 1 / 0 / 1 at the
wi508 branch's `580df781`). `docs/ratify/CURRENT.md` already says this:
"`intake.py snapshot` copies them WHOLESALE alongside any spine approval."

Not a one-off: `git log -- docs/archive/last_approved` shows 9 of the 21
snapshot commits before `580df781` (ac121647, 4fd20f89, 13593db9, 2b7be11a,
69e4a854, ad2222df, 8848f6fb, 46616726, 34a42f7e) wrote off-spine files while
only spine `Status` moved. The wi508 handback merge and its refresh carried
the branch bytes and nothing more (`git diff 4824c0ba..551d1b2c --
docs/archive/last_approved/` is empty); OI-71's disposition is not causal.

A secondary widening: `refresh_refusal` short-circuits `if approves: return
""` (:536) — one `--approves` ref mutes the gate for all seven files rather
than the registry it names.

## 2. What this is NOT

- Not a ruling on `OI-78`: the rows already absorbed at `580df781` stay
  absorbed until the owner rules; this plan stops the NEXT act from
  absorbing more. A byte-level restore stays unavailable (the mirror
  invariant).
- Not a change to the mirror invariant (`committed_snapshot_findings`) or to
  the seed path (`--seed` still copies everything once, on the owner's
  signing commit).
- Not a move of the snapshot write to the serial trunk lane. That is a
  legitimate alternative the owner may prefer (a lane never writes
  `docs/archive/last_approved/`; the approval act is replayed at the merge
  slot); it is recorded here as the alternative, not chosen, because it
  changes where approvals happen rather than what one approval copies, and
  the smaller change closes the class on its own. Re-open it if the owner
  rules the other way.

## 3. Done-when

1. `copy_live` copies ONLY the registries the act authorises: the registry
   whose `Status` flipped in the same act, plus every registry a
   `--approves` ref names — never the rest. The remaining registries' snapshot
   copies are left byte-identical to what they were (so the mirror invariant
   stays satisfied at the writing commit: an untouched file is not "written").
   The seed path is unchanged.
2. `--approves` becomes a NAMED list: a ref mutes `refresh_refusal` only for
   the registry it names; the other six keep their gate.
3. `intake.py snapshot`'s prose stamp records the registries the act copied
   and why (flip / named ref), so the next reader of `docs/archive/last_approved/README.md`
   sees the act's scope, not a whole-tree claim.
4. Tests in `tests/test_baseline_snapshot.py` (existing style): a spine flip
   with off-spine drift present leaves the off-spine snapshot bytes untouched
   and the census intact; a named `--approves` ref copies exactly its
   registry; the seed still copies all; the mirror invariant stays green
   across the act.
5. The queued reseal row's "stand" branch is re-read against the new scope:
   after this lands, that row's regeneration re-seals the four spine rows and
   nothing else, so the off-spine census survives to its own review. Its
   spec text is updated by this row (a queued spec's `## Context`/scope is
   triage, not a spine act) and the change is stated in the fragment.
6. Fragment with a file-level `Deferred open items:` line and `fig:`
   provenance on the 9-of-21 history figure (`git log --format=… --
   docs/archive/last_approved` at `6000ec9c`).

## 4. Evidence trail

The 2026-09-01 log addendum that files this row; `docs/reviews/WI-568-REVIEW-A.md`
rounds 4–5 and `docs/reviews/wi-555-wi508-partial-close/005-REVIEW-A-5c8a007-supervisor.md`
MAJOR 1; `docs/ratify/CURRENT.md`'s own wholesale-copy sentence; OI-45 (b);
baseline_snapshot.py `copy_live` / `refresh_refusal` / `_record_approval`.
