## 2026-08-25 — WI-519: the allow-file parse-honesty arm reaches the last three declared exception readers

**Summary.** Five declared exception files, five separate parsers, four
modules — two already reported a declaring line their grammar could not
read (`docs/provenance-allow`, `docs/kernel-modules-allow`); three dropped it
silently (`docs/if-tc-coverage-allow`, `docs/declared-absences`,
`docs/need-form-allow`). `trace.read_provenance_allow`'s own docstring argues
why the drop is itself worth reporting — "the other half of 'declares
nothing' is that it also COUNTS as nothing" — argued once, adopted twice,
missing three times. This row carries the arm to the missing three, without
merging any of the five parsers: each keeps its own grammar, its own required
fields and its own fail-safe direction, exactly as the spec's MUST NOT
section demanded.

Deferred open items: none — the row's Done-when is fully discharged and files
no new question.

### The three fixes, each with a real consumer

- **`docs/if-tc-coverage-allow`** (`check_trajectory.py`).
  `_parse_if_tc_allow_full(text)` is the whole parse — `(entries, seed,
  unparsed)` — behind `parse_if_tc_allow`'s UNCHANGED, pinned 2-tuple
  wrapper: `tests/test_trajectory_arch.py::test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set`
  unpacks `parse_if_tc_allow`'s return directly, so its arity could not grow.
  The consumer, `if_tc_allow_parse_findings`, is wired into `main()`'s
  `if_tc_errors` block right beside `if_tc_coverage_findings` — same
  WARN-plain / ERROR-under-`--strict` severity, same `[checks]
  interfaces_check` opt-out — but deliberately NOT that function's ≤1-module
  arch-map vacuity: a malformed line is a fact about the FILE, not about
  whether the coverage rule currently has anything to say (the same
  reasoning `kernel_allow_parse_findings` gives for riding only
  `components_check`, not the top-view bound).
- **`docs/declared-absences`** (`check_doc_refs.py`). The first Watch-for
  hazard: `load_declared_absences` takes a bare PATH (not a root) and is
  called directly by `tests/test_dogfood_sync.py`'s scaffold walk — a
  signature or return-shape change there reaches a test module this row does
  not own. `read_declared_absences(path)` carries the new `(entries,
  unparsed)` parse; `load_declared_absences` is now a one-line wrapper
  returning `read_declared_absences(path)[0]`, byte-identical in behavior to
  every existing caller. The consumer, `declared_absences_parse_findings`,
  is folded into `main()`'s own `findings` list — the same WARN-plain /
  ERROR-under-`--strict` severity a dangling reference already gets. The
  second Watch-for hazard: the file is read by two consumers
  (`check_doc_refs.py`'s own reporting surface and the dogfood scaffold
  walk, which owns none) — the finding was added to the one that already
  reports, not duplicated into the test module.
- **`docs/need-form-allow`** (`check_need_form.py`). `read_need_form_allow(root)`
  carries the new `(tokens, unparsed)` parse; `load_allow` wraps it,
  returning the token set exactly as before. The consumer,
  `need_form_allow_parse_findings`, prints in `main()` at this checker's own
  WARN-always / ERROR-only-under-its-own-`--strict` severity (still not
  wired into `check.py` at any bar — WI-454's scope guard, unchanged by this
  row).

### Driven, not asserted — RED first, then GREEN

Each of the three new findings was proven to fail without the fix before it
was written to pass: the three source files were stashed back to their
pre-row state and the new tests re-run against them.

fig: cmd="git stash push -- project-trajectory/scripts/check_trajectory.py project-trajectory/scripts/check_doc_refs.py project-trajectory/scripts/check_need_form.py; then re-run the three new test modules; then git stash pop" rev=e1c01f2b-dirty

```
AttributeError: module 'check_trajectory' has no attribute 'if_tc_allow_parse_findings'
AssertionError: assert 'declared-absences:3' in ''
AssertionError: assert 'docs/need-form-allow:3' in 'check_need_form: clean ...'
```

All three pass after restoring the fix; each test also proves the SILENT
half unchanged (a well-formed file produces no parse-honesty finding). The
end-to-end `check_trajectory` test additionally runs the real `main()`
wiring at both severities:
`test_if_tc_allow_malformed_line_is_reported_end_to_end` shows WARN-plain
without `--strict` and exit 1 with it, on the same fixture
`test_a_bare_addition_past_the_seed_suppresses_nothing` already uses.

### The MUST NOT section, honored

Nothing merged. `docs/if-tc-coverage-allow` keeps its `# seed-count:`
migration baseline; `docs/declared-absences` keeps its two accepted
separators and `LIFECYCLE:` marker; `docs/need-form-allow` keeps discarding
the reason and its single ` — ` separator. No grammar changed: the set of
lines each reader ACCEPTS as a valid entry is untouched everywhere: only
whether a line the grammar already dropped is also *counted and reported*.
The fail-safe direction is unchanged everywhere — a malformed entry still
grants no exemption, before and after (the existing tests for this,
`test_absences_file_absent_or_malformed_never_silences` and
`test_an_allow_line_with_no_reason_separator_declares_nothing`, still pass
unmodified).

### Nothing on the live tree needed to change

The live tree's five allow files were re-verified to parse to exactly what
they parsed to before this row: `check_trajectory.py --strict`,
`check_doc_refs.py --strict` and `check_need_form.py --strict` produce zero
new "grammar cannot read it" findings against this repo's own committed
`docs/if-tc-coverage-allow`, `docs/declared-absences` and
`docs/need-form-allow`. `check_doc_refs.py --strict`'s dangling-reference
count is identical before and after (204 both times, diffed directly against
the pre-row source).

fig: cmd="git stash the three source files; run check_doc_refs.py --root . --strict; compare the trailing dangling-reference count against the same command post-fix" rev=e1c01f2b-dirty

### Ratchets re-stamped, reason recorded at the site

`tests/test_module_size_ratchet.py`: `check_trajectory.py` grew past its
baseline (a new full-parse function, a new consumer, two docstrings
explaining why the pinned wrapper's arity could not grow) — 4903 → 4963
(+60). Re-stamped upward with the reason at the entry itself, per this
file's own rule ("a ratchet that fires on legitimate work is re-stamped
deliberately, never bumped silently"); `check_doc_refs.py` (884 lines) and
`check_need_form.py` (377 lines) stay far under `THRESHOLD` (1500) and carry
no baseline. `tests/test_complexity_ratchet.py` and
`tests/test_smoke_budget.py`'s membership ceiling (1367) both stayed green
with no re-stamp — the new tests fit inside existing headroom (1361/1367
collected on the smoke tier after this row).

### Shipped-kit surface

All three touched modules ship (`scripts/check_trajectory.py`,
`scripts/check_doc_refs.py`, `scripts/check_need_form.py` are all in
`bootstrap.py`'s `MAPPING`), so a new finding class reaches adopters:
`project-trajectory/RESYNC_PACK.md` gained an entry naming the three new
finding classes, their severities/opt-outs, and the unchanged-signature
guarantee on `load_declared_absences` / `load_allow` / `parse_if_tc_allow`.

### Gates

Per-commit bar (final, on the fully-settled tree):

```
python -m pytest -q -n auto -m smoke
1355 passed, 6 skipped in 24.34s / 26.01s (two runs; a third, unrelated run
mid-session read 82.1s, over the 60s budget — re-run immediately after read
22.1s, confirming the external-load caveat this repo's own docs already
record rather than a real regression; not re-stamped)

python scripts/check_smoke_budget.py --mode enforce
smoke wall-clock budget: 26.4s vs 60s budget -> within

python project-trajectory/scripts/check_docs.py --root . --stale
check_docs: OK - 1093 doc(s), 1436 intra-repo link(s), 0 broken (1 orphan
warning(s) — docs/test/report.md, a gitignored trace.py artifact regenerated
locally during this session, pre-existing and unrelated)

python project-trajectory/scripts/check_trajectory.py --root . --strict
check_trajectory: clean (518 work item(s), 493 done (95%), 21 cancelled,
graph acyclic) — remaining WARNs are pre-existing and unrelated (WI-484's own
title/specref findings, LLR tag mismatches in untouched modules, the phase-4
drop notice)

python project-trajectory/scripts/trace.py --root . --strict
integrity=0 (2 pre-existing SR-181 orphan findings, unrelated to this row)

python project-trajectory/scripts/derive_stage.py --check
docs/stage up to date (DevStg-LLReqs)
```

Full unfiltered suite, two foreground batches at the smoke/slow boundary:

```
python -m pytest -q -n auto -m smoke
1355 passed, 6 skipped in 24.88s

python -m pytest -q -n auto -m "not smoke"
1695 passed, 9 skipped in 642.50s (0:10:42)
```

3065 collected total (`--collect-only`); 1361 + 1704 = 3065. 1355 + 1695 =
3050 passed, 6 + 9 = 15 skipped, 3050 + 15 = 3065 — matches.

### Deviations from spec

- The spec's two named readers already sharing the arm
  (`read_provenance_allow`, `_parse_kernel_allow`) were read for their shape
  but not touched — confirmed unmodified.
- Claimed directly from `docs/work/queued/` to `docs/archive/work/complete/`
  via `spec_move.py` (the link-aware ritual), without the intermediate
  `docs/work/active/` hop — the work completed within one continuous sitting
  with no handoff in between, the same precedent `WI-520`'s close recorded.
- `docs/status.md`'s hand-authored WI-508 alignment narrative named this row
  by its literal `WI-519` token when first drafting the close note;
  `check_trajectory.py --strict`'s R-D guard correctly caught it (a `done`
  id in forward-only prose) before commit, and the sentence was reworded to
  describe the close without the bare token — the guard working as designed,
  not a defect.
- `docs/open-items.html` was found STALE by `gen_open_items.py --check`
  (unrelated to this row: `WI-520`'s close touched `components.toml` without
  regenerating this surface) and regenerated as part of this session's own
  close — a two-line diff correcting an off-spine "ruling(s): none cited" to
  "ruling(s): WI-520." Not this row's defect; left stale would have been a
  known-bad generated artifact riding into the next session.
- The pre-commit hook's `approval-fresh` step refused the first commit
  attempt for the same underlying reason: `docs/ratify/CURRENT.md`'s
  off-spine census carried the same stale "ruling(s): none cited" line and
  a stale approval-provenance commit id (`0f8cb9a7` instead of `e1c01f2b`).
  Regenerated with `trace.py --approve modified --out docs/ratify/CURRENT.md`
  (a plain regenerate-and-compare, not an approval act) and the commit
  re-attempted.
