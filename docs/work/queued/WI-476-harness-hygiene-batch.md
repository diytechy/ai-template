+++
id = "WI-476"
title = "Harness-hygiene batch: the six live Ruff findings, a duplicate-key-proof size-ratchet baseline, the smoke tier's nested UTF-8 decode crash, and one load-bearing assert (repo review 2026-08-19 M-07, M-05, M-01, L-02)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Four confirmed, mechanical defects batched (the WI-106 micro-fix-batch
precedent). All verified on this tree 2026-08-19; `ruff check .` reports
exactly 6 errors.

1. **M-07 — lint is red.** The six: unused tuple names in `trace.py` (~:4040),
   an E731 lambda in `tests/test_hats.py`, the F601 duplicate dict key in
   `tests/test_module_size_ratchet.py`, an unused import in
   `tests/test_trace_rules.py`, and a malformed `noqa` in
   `tests/test_stage_ladder.py`. Fix all six; none is a suppression case.
2. **M-05 — the ratchet baseline cannot see its own duplicate keys.**
   `test_module_size_ratchet.py` declares `"bootstrap.py"` at BOTH line 1275
   (2808) and line 1283 (2859); Python silently keeps the latter, so pytest
   passes while one bound is dead — the F601 above is the only thing that
   noticed. Restructure the baseline so a duplicate key is a hard error (a
   duplicate-rejecting loader — TOML, or a checked dict build), keep only
   PRESENT rationale beside entries (history lives in git/WI records — the
   commentary is why this one test is 1,746 lines), and add a test that parses
   the baseline through the duplicate-detecting path. Standing rule applies:
   reconciling the two `bootstrap.py` values is a re-stamp with the reason
   logged, never a quiet pick.
3. **M-01 — the smoke bar can crash decoding its own child.**
   `tests/test_smoke_budget.py` runs nested pytest collection with
   `encoding="utf-8"` and no error policy; on a stock Windows box a child
   emitting a CP-1252 en dash (the missing-POSIX-shell skip message) kills the
   reader thread, `stdout` becomes `None`, and the budget test dies on
   `AttributeError` — the documented per-commit bar failing for
   environment-cosmetic reasons. Run the child in UTF-8 mode explicitly
   (`PYTHONUTF8=1` / `-X utf8`) or decode with a deliberate error policy, and
   add a regression test whose nested collector emits a CP-1252-only byte.
   Keep the missing-shell skip visible as its own diagnostic.
4. **L-02 — a production invariant rides on `assert`.**
   `gen_trajectory.py:812` asserts a panel ends in `</section>` then slices;
   `python -O` removes the assert and keeps the slice. Replace with an
   explicit conditional raising a descriptive error.
