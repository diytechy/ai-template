+++
id = "WI-473"
title = "Gate scheduling loses every established product check when one draft row lands: design and build a monotonic product-regression floor beside the derived-bar selector (repo review 2026-08-19 C-01)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

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
