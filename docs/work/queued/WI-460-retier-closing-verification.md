+++
id = "WI-460"
title = "The re-tier's closing verification, on the settled state: a SECOND top-down read of the 64-row layer against the six crossings (one has run in each direction and closed the orphan set; the ledger names a second read, now that the layer exists to be read, as the honest remaining check), and ADVERSARIAL ROUND 2 (round 1 is spent - it returned CHANGES-REQUESTED with 5 MAJOR findings, all confirmed and fixed, and the fixes postdate its verdict). Both run LAST, after the authoring calls and the crossing ruling, because a review round is spent by the next commit."
specref = "docs/plans/2026-08-15-retier-completion.md#3-blocker-class-b--the-verification-the-campaign-declared-it-owed"
workstream = "process"
sr_refs = []
needs = ["WI-458", "WI-459"]
supersedes = "WI-451"
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

The third and last of the three rows that finish the re-tier. Full statement:
[the completion analysis](../../plans/2026-08-15-retier-completion.md) §3.

**Blocked on `WI-458` and `WI-459`.** Both move rows. A review round is spent by
the next commit, so taking either review before the state settles wastes it —
which is exactly what happened to round 1.

## Why this row is not optional bookkeeping

Four defects in this campaign were found late, and **all four had the same
cause: a bar that was not being run.**

- **Act 4** — adversarial round 1 returned 5 MAJOR findings and named the
  smoke-only bar as their cause.
- **At the merge bar, `check_flows` refused**: the Runtime flows in
  `docs/architecture.md` cited **eight ids the campaign had demoted**
  (SR-029/057/060/093/115/124/131/132). Nothing earlier caught it — the flows
  are hand-authored prose that only `check_flows` reads, and the per-commit
  smoke tier does not run it.
- **At the same bar, `format` had been SKIPping on the entire lane**: the lane
  worktree had no `ruff`, so every commit on that branch was made without it,
  and two files carried unformatted code to the merge.
- **The first partial close this repo ever performed** turned the full suite red
  — `handback.close_partial` writes an immutable report to `docs/handbacks/`
  that nothing links to *by design*, and the contract shipped with no
  `orphans-allow` entry, in this repo and in the template every adopter
  scaffolds from.

**The lesson has been recorded three times and converted into a guard zero
times.** This row should either add that guard or state deliberately why none is
wanted — a lane bar that cannot silently SKIP a step is the obvious candidate,
since a SKIP is what hid two of the four.

## Done-when

- The second top-down read is run and its findings recorded, ranked, with each
  either fixed or dispositioned. A read that finds nothing is a valid result and
  should say so explicitly rather than going unreported.
- Adversarial round 2 runs on the settled tree, cross-family per the routing
  policy, and its verdict is recorded with each finding re-verified by the
  author before acceptance.
- The SKIP-hiding-a-defect pattern is closed by a guard, or its absence is a
  recorded decision naming who accepted the risk.
- The full suite (`pytest -q -n auto`, unfiltered) is green and pasted.
- `WI-451`'s close report is dispositioned via `WI-457`, and this row states
  whether the re-tier is now COMPLETE or what still stands.
