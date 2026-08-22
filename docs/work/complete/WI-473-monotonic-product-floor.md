+++
id = "WI-473"
title = "Gate scheduling loses every established product check when one draft row lands: design and build a monotonic product-regression floor beside the derived-bar selector (repo review 2026-08-19 C-01)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

**Shipped in full at slice 1 (2026-08-20), then deliberately superseded and
deleted by the WI-498 stage unification (2026-08-21, the OI-51 ruling) —
closed COMPLETE per the owner's disposition (2026-08-21, "no preference,
move to complete"): completion records work done, not perpetual existence.**

What this row delivered, and why it counts even though the code is gone:
`product_floor()`/`floor_plan()`/`floor_notice()` in `check.py` with five
guards including the review-specified regression fixture (all green at
c23eb907/b9538b26); the corrected `.github/workflows/test.yml` enforcement
claim (which SURVIVES); the design record
`docs/plans/2026-08-20-product-regression-floor.md` (survives as history);
and — the load-bearing part — **building it refuted C-01's framing**: the
floor's construction surfaced that `DevStg-Impl` was unreachable from the
derived selector at all, which became OI-51, whose four-exchange ruling
became the stage unification program that made the floor unnecessary (the
effective stage carries the draft-exclusion by design, and C-01 is pinned
fixed at the SELECTION level by `tests/test_selection_at_or_above.py`,
this row's tests' named successor).

The four items the slice left owed, each dispositioned by the program:
(1) OI-51 — RULED, as the unification rather than the interim re-tag;
(2) the SR-006/LLR-060 amendment — folds into the stale-Approved-rows
batch beside OI-53 (the prose describes superseded machinery);
(3) TC coverage — superseded with the mechanism (the successor test file
carries the obligation);
(4) the rehearsal — delivered by WI-498 slice 2's C-01-at-selection
acceptance run on a real scaffold.

## Context

The 2026-08-19 repository review's one Critical finding, confirmed against the
tree before this row was minted. The mechanism, verified: `docs/gate`'s header
states the derived bar is "the MIN over every in-scope SN/SR/LLR/TC's own bar
... a Drafted or Modified row DROPS it", and `check.py` schedules `format`,
`lint`, and `tests+coverage` only at `BAR_RELEASE` (`check.py:574-576`), while
the shipped downstream workflow (`project-trajectory/ci/check.yml`) runs pushes
and PRs at the currently derived bar. So a mature downstream project that adds
ONE ordinary draft requirement silently drops formatting, lint, tests, and
coverage from its CI — verification gets weaker exactly when planning work is
introduced. Two aggravations, both already on record here: (1) OI-30 D2 ruled
`sr_bar` ceilings at `DevStg-Tests`, so `BAR_RELEASE` — and with it every
product check — is currently unreachable-by-cell until the harness driver
lands; (2) `.github/workflows/test.yml` claims the root gate enforces
format/lint/tests+coverage, which is true only because this meta-repo runs a
separate full-pytest matrix that downstream adopters do not get.

The direction (the review's, adopted here as the starting design, not the
ruling): separate two axes. Artifact-maturity checks stay selected by the
derived bar exactly as today; a PRODUCT REGRESSION FLOOR — format, lint,
tests+coverage, and the other already-adopted product checks — never falls
once a project has configured or first cleared it (persist the highest cleared
product bar, or infer the floor from the presence of configured product
commands). Add the shipped CI regression fixture the review specifies: start a
mature scaffold, add one Drafted row, assert every established product check
remains in the plan. Correct the root workflow comment to describe actual
enforcement.

Why `safety_class = "spine"` and `buildtier = "strong"`: the derived-gate
model is design-shaped by SR/LLR rows (several LLRs name
`derive_gate.py` as their module) and stated normatively in `PROCESS.md` §4,
so the fix amends design rows and byte-budgeted prose, not just `check.py`.
The first slice is a written design proposal for the owner — the monotonic
floor changes what a downstream green MEANS, which is not a builder's call.
Sequencing note: independent of the sitting's status-vocabulary step 7 (the
enum retirement changes row STATES, not the min-selector shape), but any SR
amendment lands through the same amendment discipline as every other
spine-class row.

## Slice 1 landed 2026-08-20 — what shipped, and the four items still owed

The row stays QUEUED, not complete: the mechanism is built and proven, and the
ruling that makes it reach the three checks the finding is about is the owner's.
Design record: [../../plans/2026-08-20-product-regression-floor.md](../../plans/2026-08-20-product-regression-floor.md).

**Shipped.** `check.py` gains `product_floor()` (reads `ex-draft=` off the
`# basis:` line), `floor_plan()` (the product-layer steps the dropped bar would
have lost, built from the FLOOR bar's own table) and `floor_notice()` (the
disclosure, on `--list` and the run summary); `tests/test_product_floor.py`
carries five guards including the review's asked-for regression fixture, driven
through the real `derive_gate` on a mature scaffold; `PROCESS_OPTIONS.md` states
the rule; `RESYNC_PACK.md` §3 carries the adopter entry; the root
`.github/workflows/test.yml` enforcement claim is corrected.

**The design decision taken:** the floor is `max(derived bar, ex-draft)` —
DERIVED, not a stored high-water mark — which is the shape `PROCESS.md` §4
pre-authorizes ("a second, derived high-water number shown BESIDE the honest
one, never instead"). It is monotonic against DRAFTING and is not claimed to be
monotonic against anything else; a lowering therefore requires a reviewed
human-held spine act and is visible as a changed `ex-draft=`.

**Owed, in the order they unblock each other:**

1. **`OI-51` — the binding constraint, and it is not the one C-01 names.**
   Measured while building: OI-30 D2 ceilings `derive_gate.sr_bar` at
   `DevStg-Tests`, and `ex-draft` is a MIN that includes it, so neither the bar
   nor the floor can reach `DevStg-Impl` — where `format`/`lint`/`tests+coverage`
   are tagged. Those three therefore gate on **no adopter's push or pull
   request**, draft or no draft; only the tag path forces `--gate all`. The floor
   is DORMANT for them until this is ruled (recommendation: re-tag to
   `{DevStg-Tests, DevStg-Impl}` as the interim, harness driver as the terminus).
   `test_the_floor_is_dormant_for_the_BUILT_IN_product_steps_and_says_so` fails
   the day either half moves, so arming is an act rather than a drift.
2. **The spine amendment, deferred as the sitting's act.** `SR-006` is the
   requirement home ("shall run the required steps of *the gate that must next be
   passed*") and `LLR-060` its design row. Both are **Approved**, and the floor
   makes `SR-006`'s shall incomplete rather than wrong; amending an Approved cell
   overrides attestation (the `SR-158` precedent, which left `LLR-014`/`TC-014`
   re-points owed for exactly this reason). No spine row was minted or amended
   here. Until it is taken, the built behaviour is ahead of its requirement.
3. **No TC covers the floor**, following from 2 — the guards exist in `tests/`
   but nothing in the trace registry claims them, so the coverage join does not
   see this work.
4. **The rehearsal this repo cannot give itself.** Its own `ex-draft` reads
   `DevStg-Reqs` (nine Approved SRs undecomposed — the declared orphans debt), so
   no floor engages here and the change is unobservable from the meta-repo's own
   CI. The scaffold fixture is the cheapest place to add a rehearsal if `OI-51`
   is ruled (a).
