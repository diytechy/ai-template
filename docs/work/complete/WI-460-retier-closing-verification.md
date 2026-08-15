+++
id = "WI-460"
title = "The re-tier's closing verification, on the settled state: a SECOND top-down read of the 64-row layer against the six crossings (one has run in each direction and closed the orphan set; the ledger names a second read, now that the layer exists to be read, as the honest remaining check), and ADVERSARIAL ROUND 2 (round 1 is spent - it returned CHANGES-REQUESTED with 5 MAJOR findings, all confirmed and fixed, and the fixes postdate its verdict). Both run LAST, after the authoring calls and the crossing ruling, because a review round is spent by the next commit."
workstream = "process"
sr_refs = []
needs = ["WI-458", "WI-459"]
supersedes = "WI-451"
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Closed DONE 2026-08-15. **The re-tier's verification is COMPLETE; what stands
between here and done is the sitting itself.** Three things shipped. (1) The
SECOND top-down read of the settled layer ran — 59 rows against the six locked
crossings, six findings, two fixed mechanically and four recorded for the
sitting (log `2026-08-15i`). (2) **Adversarial round 2** ran cross-family on the
settled tree — GPT-5.6 Sol via `codex`, read-only sandbox — and returned
**CHANGES-REQUESTED with 7 MAJOR findings**, each re-verified by the author
before acceptance: **five confirmed and fixed** (`SR-140` re-based off the
abolished on-row anchor onto the ruled snapshot contract; `SR-148` regains
`SR-059`'s dropped migrated-repo deletion half; `IF-004`/`IF-031` owners → the
row that actually owns the comparator; `SR-163`/`SR-166`'s conflicting manifest
clauses resolved; `unanchored_findings` wired), **one confirmed in half and
fixed in that half** (`_claims_approval` is tier-aware; the SN exclusion is
design §B7), **one dispositioned as a recorded decision** (F4 — the wave is a
full re-read, not a diff). Verdict on the record at
[`docs/reviews/wi451-retier/ROUND-2-SOL.md`](../../reviews/wi451-retier/ROUND-2-SOL.md);
per-finding reasoning in log `2026-08-15j`. Wiring F2's fix found one further
defect the round had not seen — the vacuum was keyed on a directory
`bootstrap.py` scaffolds README-only, which would have reported eight missing
tiers in **every fresh adopter repo on day one**. (3) The **SKIP-hiding-a-defect
pattern is closed by a guard** (`6d341ea2`), not recorded a fourth time. Full
suite green (2533 passed, 10 skipped). All of it PROVISIONAL under the
2026-08-15 charge-through; **no Status, `approval` or attestation cell moved in
any direction.**

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

## Close

**CLOSED 2026-08-15** (log `2026-08-15j`). *Every call in this row is
provisional under the owner's 2026-08-15 charge-through and overturnable at the
review sitting; no Status, `approval` or attestation cell moved in any
direction.*

### The second top-down read (Done-when 1) — log `2026-08-15i`

Fifty-nine rows read top-down against the six locked crossings, **after**
`WI-458`'s merges/demotions/mints, the crossing confirmations, the interface
owner/`req_refs` rework and the M3 coverage extensions. **Six findings on 59
rows**, against the first read's base rate of five on 64 — two fixed
mechanically, four recorded for the sitting. A read that found nothing would
have been a valid result; this one did not, and said so.

### Adversarial round 2 (Done-when 2) — log `2026-08-15j`

**CHANGES-REQUESTED, 7 MAJOR.** Cross-family per the routing policy: **GPT-5.6
Sol via `codex`, read-only sandbox**, on the settled tree. The verdict is on the
record verbatim at
[`docs/reviews/wi451-retier/ROUND-2-SOL.md`](../../reviews/wi451-retier/ROUND-2-SOL.md).
Every finding was **re-verified by the author before acceptance**, as this row
required:

- **5 confirmed and fixed** — F1 (`SR-140` still required the on-row anchor its
  own mechanism abolished, while `LLR-173` claimed to implement it), F5
  (`SR-059`'s migrated-repo deletion half dropped in the merge), F6
  (`IF-004`/`IF-031` owners routed to rows that cannot answer for the contract),
  F7 (`SR-163`/`SR-166` prescribing conflicting outcomes for one observable),
  and F2's wiring half.
- **1 half-confirmed and fixed** — F3: the tier-awareness half is real and
  fixed; the SN half is BY DESIGN (§B7 — needs carry no maturity cell).
- **1 dispositioned** — F4: no per-row before/after evidence for this sitting,
  accepted as a **recorded decision**. The wave is a full re-read by ruling
  `2026-08-14e` / sitting-3 §2.1, and the git-walk baselines it asks to restore
  are meaningless for rows the re-tier restructured.
- F2's ERROR-arming deferral is likewise **by design** (§B4/§B6, migration
  step 7).

Wiring F2's fix immediately found a defect the round had not seen: the vacuum
was keyed on the snapshot DIRECTORY, which `bootstrap.py` scaffolds
README-only — so the rule reported all eight tiers missing in every fresh
adopter repo on day one. Fixed and pinned.

### The SKIP guard (Done-when 3)

**Closed by a guard, not by a recorded acceptance of the risk** — log
`2026-08-15i`, commit `6d341ea2`: a SKIPped step the repo itself declared
cannot pass unnoticed. The lesson that had been recorded three times and
converted into a guard zero times is now converted.

### Done-when 4-5

The full unfiltered suite is green and pasted in the session record. `WI-451`'s
close report is dispositioned via `WI-457` (log `2026-08-15f`).

### The closing statement

**The re-tier's VERIFICATION is COMPLETE.** Both reads have run, the adversarial
round is spent on a settled tree, every finding is fixed or dispositioned with
its reason recorded, and the silent-SKIP class is guarded.

**What stands between here and done is the sitting itself** — `OI-30`'s three
calls and the ratification wave, in the sequence set out in
[`docs/plans/2026-08-15-review-package.md`](../../plans/2026-08-15-review-package.md)
§5. Nothing further is queued behind this row.
