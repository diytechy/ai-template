# WI-405 — REVIEW-A (2026-08-02)

Verdict: APPROVE — the review's core was re-litigating the DECLINE, and I did
not take the builder's word for it: I hacked a last-match-before-FAIL variant
of `_own_step_window` into a scratch harness and drove BOTH anchors over the
quoted-mock-banner shape, its symmetric twin (a failing step whose banner a
LATER passing step quotes, at inline-status and `--jobs 1` shapes), shape 1,
and shape 3. The trade is real, no variant dominates, and shape 1 is provably
out of reach of any banner preference. One record-only nuance below.

Reviewed independently against the spec
(`docs/work/complete/WI-405-anchor-trusts-bar-shaped-embedded-text.md`: the
documented-limit clause + a JUDGED outermost-banner preference, the WI-398
REVIEW-A finding 1 shapes as pins). Diff = `28860c87` (work) + `3611f4d2`
(close) on `wi-405-anchor-trusts-bar-shaped-embedded-text` vs
`ConcurrencyTrainRewrite`. `docs/log.d/` was not read. All commands run under
`/Users/diytechy/Documents/ai-template/.venv/bin/python` from the worktree.

## Findings

1. **NOTE — the decline's "merely mirrors the hole" phrasing under-reports
   the variant it declines: last-match-before-FAIL would also accidentally
   repair shape 3.** Driven on the pinned shape-3 fixture, the variant
   anchors on the NESTED `=== format : stub ruff format --check ===` line
   (the last marker match before the nested `  FAIL  format` row) and the
   window then runs to the summary rule, so it carries
   `FAILED tests/test_integrate.py::test_red_bar - AssertionError: OUTER
   REAL` and the outer `  FAIL  tests+coverage` row — the real error the
   current anchor loses — albeit opened under the quoted stub banner's label.
   So the honest score is: variant fixes shapes 2 and 3, breaks the `--jobs 1`
   symmetric twin, cannot touch shape 1; current handles both twins, pins
   shapes 1–3 as limits. **This does not change the verdict**: no dominance
   (each anchor breaks a shape the other handles — verified, see "None
   against"), the shape-3 gain is an accident of the missing-next-banner
   window shape rather than a designed attribution, and the Deliverable's
   two load-bearing decline claims (the twin break, shape 1's unreachability)
   are both TRUE as stated. Record-only, for whoever next re-grades this
   limit. -> @owner

## None against — what I tried and could not break

- **The decline core, re-derived by construction.** Scratch driver: the
  worktree's `agent_common` loaded by path, plus a variant
  `_own_step_window` choosing the LAST `=== <step> : ` match at an index
  before the first FAIL line (first match anywhere as fallback), all else
  identical. Six bars: the pinned shape 2 (inline statuses) and a `--jobs 1`
  form of it; the SYMMETRIC TWIN — real `tests+coverage` red FIRST, a later
  passing `docs` step quoting `=== tests+coverage : stub pytest -q ===` —
  at inline and `--jobs 1` shapes; pinned shapes 1 and 3. Results:
  first-match (current) is CORRECT on both twins and WRONG on shapes 1/2/3
  (exactly the pinned limits); last-match-before-FAIL is CORRECT on shape 2
  (both forms) and WRONG on the `--jobs 1` twin — its window becomes the
  quoting step's `=== tests+coverage : stub pytest -q ===` / `fixture tail`,
  zero bytes of `REAL ERROR`. The trade is real: at `--jobs 1` the first
  FAIL row sits in the summary, below every section, so "before FAIL"
  excludes nothing and last-match lands on the quote. Each anchor breaks a
  shape the other handles; neither dominates; the parser-free space has no
  free fix here.
- **Shape 1 is unreachable by ANY banner preference — verified, not just
  argued.** Both anchors produce the byte-identical window on shape 1
  (`all good` / quoted `  FAIL  tests+coverage` / `  PASS  tests+coverage`):
  the hijack happens at FAIL-line selection (`_FAILTAIL_FAIL_RE` picks the
  quoted row as first FAIL, and its step name resolves to the passing step's
  real banner), before any banner choice is consulted. The only lever there
  is last-FAIL — which is precisely the WI-240 anchor WI-398 reverted
  because the closing summary re-prints every status.
- **A true outermost preference needs a parser — the spec's "ONLY if it
  stays inside the existing shape" condition fails.** "Outermost" means "not
  inside another step's section", which requires knowing section boundaries,
  which requires knowing which banners are real — circular without
  structural parsing, which the inherited WI-398 scope guard forbids. The
  judged decline is inside the spec's own fallback ("pin whichever behavior
  is chosen — documented limit or outermost-banner preference").
- **The three pins, re-run and re-derived.** Module run:
  `python -m pytest -q -p no:xdist tests/test_agent_common_harness.py` →
  **20 passed in 0.02s** (17 + the 3 new; Deliverable fig agrees exactly).
  I drove `_failure_tail` directly on each fixture and the pinned assertions
  match the actual windows byte-for-byte: shape 1 = the passing quoter's
  section (`all good`, `  PASS  tests+coverage`; no `F401`, no
  `  FAIL  lint`); shape 2 = quoted stub banner + `fixture tail`, no
  `REAL ERROR`, with the appended anchoring row naming `tests+coverage`
  (the pin asserts exactly that nuance); shape 3 = `146 files already
  formatted` + the nested `  FAIL  format` row, no `OUTER REAL`, no
  `tests+coverage` token anywhere in the tail. The pins assert the WRONG
  window's content positively, so a future anchor change reds them rather
  than passing vacuously. The section comment is honest twice over: "pinned
  AS THE KNOWN LIMIT, not as designed behavior" and "if one reds, the anchor
  changed and the docstring's limit clause is stale". All 20 run under
  `-m smoke`, so the pins sit in the per-commit tier.
- **Fixture fidelity to the reviewer's recipes.** Each pinned bar carries the
  REVIEW-A finding 1 ingredients (`all good`/F401-lint for shape 1;
  `=== tests+coverage : stub pytest -q ===`/`fixture tail`/`REAL ERROR` for
  shape 2; `146 files already formatted`/nested `  FAIL  format` inside a red
  `tests+coverage` for shape 3), built from check.py's real printing shapes
  (banner, 2-space status rows, `"=" * 56` rule, summary block).
- **Zero code tokens, proven not eyeballed.** Both revisions of
  `agent_common.py` parsed to AST with every docstring nulled:
  dumps identical (`28860c87^` vs `28860c87`). The +10/−2 hunk is entirely
  inside `_own_step_window`'s docstring; the clause is accurate — both
  anchors ARE pure line-shape trust (`^\s*FAIL\s` for the FAIL line,
  `lstrip().startswith("=== <step> : ")` for the banner), and the named
  backstop `out/run-logs/refresh-refused-<branch>.log` is the kept-log home
  WI-398 shipped and its review verified.
- **Ratchet exact.** Census by the ratchet's own metric
  (`len(text.splitlines())`): `agent_common.py` = **1792**, equal to the
  re-stamped baseline; `test_module_size_ratchet` module green; the baseline
  comment carries the +8 delta, the WI-405 reason, the 2026-08-02 date, and
  keeps the WI-280 re-stamp-down pointer.
- **The record, re-run rather than read.** In the worktree at `3611f4d2`:
  smoke tier **625 passed, 2 skipped in 10.17s** (Deliverable's fig at
  `28860c87` says 621/6 — same universe of 627, the environment-dependent
  skips pass on this machine, the same delta WI-398 REVIEW-A recorded). The
  full-suite fig (**1880 passed / 10 skipped in 0:04:39** at `28860c87`) is
  the BUILDER'S, attributed not re-verified: my own full re-run was still in
  flight at finalize time, and the refresh bar re-runs the full tier
  mechanically before any merge — every other figure in this review is
  reviewer-produced. `check_trajectory --root . --strict`
  rc=0 — **the same 11 WARNs trunk prints, diffed line-for-line, none about
  WI-405**; `check_doc_refs --root . --strict` rc=0; `check_figures --root .
  --strict` rc=0, **39 declared figure(s), every one carrying its command and
  revision** — WI-405's harness-module fig re-run with exact agreement, its
  smoke fig re-run with the environment-consistent totals above; `ruff format
  --check` 152 files already formatted; `ruff check` All checks passed.
- **R-A / R-F.** The close move cleared
  `specref = "docs/reviews/WI-398-REVIEW-A.md"` from the frontmatter (present
  at `3611f4d2^`, absent in the complete spec); the Deliverable is dated
  2026-08-02 and every number in it re-verified or reconciled above, save the
  full-suite fig attributed as noted. The
  `WI-405` token at `docs/status.md:173` sits inside the GENERATED frontier
  block (exempt from forward-only; drops at the merge regen).
- **Scope and delta.** The whole branch delta vs merge-base is six paths: the
  docstring, the two test files, the active→complete spec move, and the
  unread `docs/log.d/` fragment — the `docs/work/` delta is exactly the
  WI-405 move, nothing else. Matches the spec's "agent_common.py
  docstring/one clause + tests; nothing else".
- **Registration judgment — sound.** No new LLR/TC rows: WI-405 adds no
  module and no public surface (a docstring clause + tests inside the
  already-cited harness suite); this extends the WI-398 registration
  judgment its review already graded defensible (`_failure_tail` row-less
  since WI-240; LLR-143/144/145 precedent is for NEW modules).

**THIS IS AN APPROVE:** the declined alternative was rebuilt and driven, not
believed — the symmetric twin breaks it exactly as claimed, shape 1 sits
below any banner preference, and no parser-free variant dominates; the three
pins assert the true current windows, in the smoke tier, with honest
stale-clause comments; the shipped change is provably zero code tokens; and
the record re-ran green (the builder's full-suite fig attributed, pending the
refresh bar). The one finding is a completeness note on the decline's prose,
not on its verdict.

VERDICT: APPROVE findings=1
