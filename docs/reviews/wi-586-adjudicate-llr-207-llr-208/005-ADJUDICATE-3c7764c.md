# WI-586 — ADJUDICATE first approval — commit 3c7764c

Four rows awaiting a FIRST approval: `LLR-207`, `LLR-208`, `TC-205`, `TC-206`.
The question judged is the only one this act answers — is each row's TEXT ready
to be blessed as it stands. Basis: the live registries against
`docs/archive/last_approved` (copied 2026-08-30, commit `4824c0ba`).

This is the THIRD adjudication of these four rows (`001`, `003`, and this one).
Before judging I established the fact that governs how much weight the earlier
verdicts may carry: **this lane has committed nothing to either registry.**
`git log` over `docs/requirements/low-level-requirements.toml` and
`docs/test/test-cases.toml` shows their newest commits are `WI-579`'s, all
ancestors of this lane's start; the lane's own eight commits touch only
`docs/iteration/`, `docs/reviews/` and its spec. All four rows are therefore
byte-identical to the text `001` and `003` judged, and all four are still
`Status = "Drafted"` (read through `tomllib`, not grep).

That makes inheriting the earlier findings the easy error, so I re-drove every
load-bearing one myself rather than reading them for plausibility. Everything
below is what I ran at this commit. Mutations were applied to a copy-backed
file and reverted, with `git diff --quiet` asserted clean after each.

Baseline first: `tests/test_verdict_record.py tests/test_score_reviews.py`
→ **72 passed**.

- **Finding 1 (`governing_identity` / `HEAD`)** — CONFIRMED, driven.
  `refresh_attestation(root, 'wi-585-adjudicate-llr-045-llr-140', 'c16246e0')`
  → `('e2b3cf8af0a1…', 'bar PASS (12 steps, tier all)')` and
  `governing_identity(...)` → `ce5e2550be0a…`; with `'HEAD'` → `None` and
  `2c9a184049f8…`. Two identities across exactly one refresh commit.
  `kitlib/verdict.py:738-740` forbids the token by name — "`branch` must
  therefore be the lane's BRANCH NAME and not `HEAD`".
- **Finding 2 (`governing_rev` termination)** — CONFIRMED, driven and read.
  `governing_rev(root, <branch>, '0e6bad3b')` → `d202c9f3cd66…` with
  `refresh_attestation` `None` — no peel occurred, so the walk did not
  terminate on one. The loop `continue`s on a peel (`verdict.py:467`) and
  `break`s where identity differs from the parent's (`:473`, commented "this
  commit changed the work, so it is where the walk ends").
- **Finding 3 (multi-log rule undetected)** — CONFIRMED by mutation. Relaxed
  `verdict.py:608` from `len(ph) == 1` to a last-wins `sorted(ph)[-1]`:
  **72 passed**. A stated fail-closed rule with no detector.
- **Finding 4 (trailer-carrier check undetected)** — CONFIRMED by mutation.
  Deleted the `governing_identity(root, branch, sha) != tree` guard
  (`verdict.py:802-803`, "the words rode onto a tree they do not describe"):
  **72 passed**. The row's own anti-forgery claim is unexercised.
- **Finding 5 (`TC-205` evidence misses the reset peel)** — CONFIRMED. Parsed
  `TC-205.evidence`: the only modules cited are `tests/test_verdict_record.py`
  and `tests/test_integrate_admission.py`. `test_integrate_station.py`, where
  `work_tip` and `refresh_attestation`'s refusal arms are driven, is cited by
  `TC-132` for `LLR-140` — not here.
- **Finding 6 (`TC-205.method` misstates its own driving)** — CONFIRMED by
  reading `tests/test_verdict_record.py:81-90`. The `Method` says "a changed
  work blob and a changed `docs/work/` spec each fold DIFFERENT"; the second
  assertion compares against `_listing("src/widget.py")`, which DROPS the spec
  entry rather than changing it.
- **The `LLR-208`/`TC-206` gap** — CONFIRMED by mutation, and this is the one
  the first adjudication missed. Deleted the `verdict-rollup` row from
  `trunk_step.REGEN_STEPS` entirely: `TC-206`'s four cited evidence nodes →
  **4 passed** (unchanged from baseline), and the whole of
  `tests/test_trunk_step.py` → **16 passed**. The wiring is real
  (`trunk_step.py:589`, `check.py:1176`/`:1556`, `docs/stack.ini:988`), but
  nothing `TC-206` cites detects its removal.

## The rows

- [RETURN] LLR-207 -> obligation: state ONE definition of a governing verdict — the record-path tree identity, the rev it is measured at, the logged-session evidence join, the declared phase span and the cycle count — so the merge slot's "may this lane merge" and the loop's "which phase is still owed" cannot answer differently -> chain: parent `SR-156` is the right home (its seam's verdict rung is the already-Approved `LLR-140`, and this row is that rung's shared definition, declared as the `IF-175` seam); sideways it does not overlap `LLR-140`, `LLR-145`, `LLR-150` or `LLR-151`; downward its sole `TestRefs` is `TC-205` -> NOT READY on five counts, each re-driven above. Findings 1 and 2 are false statements of a delivered contract: a row whose one job is to name the identity both readers key on must not name `HEAD`, the value the module bans by name and which I measured producing a second identity, and must not state a termination condition the loop does not have. Findings 3, 4 and 5 are stated obligations no cited test discharges — two of them proven undetected by mutations that left the suite fully green. Either class alone returns the row. The DESIGN is not returned: the identity fold, the two-shape peel, the logged-session join and the cross-check-not-accept reading of the trailer are correct as built, and I would bless them stated accurately.

- [RETURN] TC-205 -> obligation: drive the verdict record's two halves — the identity and the evidence — each beside its opposite, so the gate's demand and the loop's owed set are shown to come from one reader -> chain: `Verifies SR-156;LLR-207;IF-175` satisfies the triangle and `Tier: Smoke` is defensible for the `test_verdict_record` nodes -> NOT READY, and it moves with its parent: findings 3, 4 and 5 are gaps in exactly this row's `Method` and `Evidence`, so blessing this text would record `LLR-207` as verified while its multi-log ambiguity rule and its trailer-carrier refusal are provably undetected and its reset-peel contract is cited nowhere. Finding 6 is this row's alone — a `Method` is a claim about what was driven, and this one describes an assertion the test does not make.

- [RETURN] LLR-208 -> obligation: the per-review-scope rollup is GENERATED — one file per review scope, scope set taken from the round-file name parser's own `train` field rather than the directory layout, the generator owning that directory on both the check and the write arm, the collision refused rather than last-write-resolved, declared/regenerated/freshness-gated at the seam, stood down on a work branch, and stating no governing verdict -> chain: parent `SR-170` holds the exclusive-writer contract and this is a third such surface beside `LLR-137` and `LLR-060`/`LLR-124`, no overlap, one decision; downward `TC-206` -> NOT READY on one count, and it is the count that matters most for THIS parent. The clause that makes the artifact a serial-actor surface at all — "regenerated by the trunk step" — is the row's load-bearing tie to `SR-170`, and I deleted that regeneration row outright while every test `TC-206` cites stayed green. The rest of the cell binds: I read `gen_verdict_rollup.py` and the reserved flat stem, the both-arm collision refusal, the normalized comparison, the `_extra` report-and-prune pair and the "**The merge gate does not read this file.**" header are all real. One unpinned load-bearing clause is still a returned row.

- [RETURN] TC-206 -> obligation: drive the rollup as derived state — regeneration, all three `--check` answers, the extra arm proven CLEARABLE by the remedy its own failure message names, the flat pre-train layout, the collision refusal, the prune and the honesty sentence, with the declaration side held by the wiring guard -> chain: `Verifies SR-170;LLR-208`, all four evidence nodes exist and pass, and all three modules sit outside `conftest.py`'s `SLOW_MODULES` so `Tier: Smoke` is exact -> NOT READY, and it moves with its parent for the same single reason. Its `Expected` asserts the rollup "is written by a regenerator the serial merge step runs"; that sentence can become false — I made it false — with all four cited nodes green. Every other arm of this row's `Method` is genuinely driven, so this is one missing detector rather than a broad coverage failure.

## What this returns, and what it does not

All four rows go back, on two independent grounds: `LLR-207`/`TC-205` for two
contradicted contracts and three undetected obligations, `LLR-208`/`TC-206` for
one unpinned trunk-regeneration clause. Both `## Dispositions` drafts in this
row's spec state the repairs; `intake.parse_dispositions` was driven on the
edited spec and returns `refusal=None` with **2 drafts**.

Because every row is returned, no `Status` was flipped, `intake.py snapshot`
was not run in any form, and nothing under `docs/archive/last_approved/` moved.
The snapshot blocker `001` recorded (`WI-584`) is therefore not reached by this
act and is neither resolved nor worsened by it.

## The outstanding CHANGES-REQUESTED was applied

`004-REVIEW-A-3c7764c.md` returned three findings against the disposition
drafts, unaddressed until now. All three are fixed in this commit, each
verified first:

- BLOCKER — the first draft asserted "`LLR-208` and `TC-206` were APPROVED by
  that act", which no adjudication ever did. Replaced with the true reason they
  are out of that draft's scope (they were RETURNED and are the SECOND draft's
  business), and the `VERDICT THIS CONTINUES:` pointer re-aimed from the
  superseded `001` at this verdict, the latest governing one.
- MAJOR — both drafts declared `bar = "DevStg-Reqs"` while their deliverable is
  new pytest regressions. Verified the distinction rather than taking it:
  `check.py --stage DevStg-Reqs --list` yields **12** steps and
  `--stage DevStg-Tests --list` yields **14**, the two added being
  `design-flows` and `trajectory`; `kitlib/ladder.py:79` defines `DevStg-Tests`
  as "the test set for those obligations in work". Both drafts now declare
  `bar = "DevStg-Tests"`, re-parsed clean.
- MINOR — finding 1's reproduction never named the branch, so a builder
  following it literally would reproduce the wrong half of the contrast. It now
  names `wi-585-adjudicate-llr-045-llr-140` as the refresh's own subject.

## One process observation, recorded rather than acted on

These four rows have now been adjudicated three times against byte-identical
text, because an adjudication lane may flip a `Status` but may not edit the
cells its findings name — so the repair can only travel through the disposition
drafts at merge. That is the design working, not a fault, but the loop has
spent three rounds re-deriving one answer. The drafts are now correct and
parse; the next useful act on these rows is the merge that mints them, not a
fourth reread. This is an observation for the coordinator and falsifies no cell
in this batch.

OUTCOME: RETURN rows=4
