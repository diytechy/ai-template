## 2026-08-23 — WI-448 slice 4: the residual duplicate groups, and the census reaches zero

Deferred open items: none — this slice took no owner decision. Two questions it
could have raised are settled inside it: every home is an EXISTING themed module
(no new `MAPPING` row, so the downstream risk surface the WI names is untouched),
and the one behaviour that could not enter `kitlib` took `spine_carrier` under
the precedent slice 3 already set for `sn_draft_ids`.

**Summary.** Item 4 of WI-448's STILL OWED list. All six groups the standing
census reported at HEAD are gone, plus four copies the census could not see,
and the `[dupes-census]` baseline re-stamps to **0 / 0 / 0** — empty for the
first time since OI-58 armed it. No new `kitlib` module was created: every
behaviour joined a theme the package already declares, which is the
smallest-total-code answer D-8 asks for and the answer slice 2 gave for the
console guard. CLI behaviour is byte-identical — every former name is
re-exported from its original module under the spelling it always had, so no
call site in any consumer moved. Six `tests/test_rule_sync.py` equality pins
retire; four replacements land (two identity pins, two by-value batteries).

### The census-to-item-4 mapping

Item 4 named a population. The census at HEAD reported six groups. They are not
the same list, and reconciling them is the first thing this slice did:

| item 4 named | census at HEAD (`77d67c38`) | reading |
| --- | --- | --- |
| `is_example`, "the 3-home behaviour whose copies disagreed, one crashing on `None`" | **not reported** | Slice 3 folded two of the three into `kitlib.spine`; the third (`gen_release_checklist`) survived, but at 2 lines it is UNDER the census's 4-line body floor. Real duplicate, invisible instrument. Consolidated anyway. |
| `_process_check` x2 | group `7c17bf05` (22 lines) | as named |
| `_norm_module` x2 | group `2e5beefa` (14 lines) | as named — but there were FOUR homes, see below |
| `sn_rows` x2 | group `ab9af0a1` (9 lines) | as named |
| `_split_tokens` / `split_refs` x2 | group `c0ea3338` (10 lines) | as named — but there were SIX homes, same floor effect |
| `wi_convert`'s `spec_paths` / `work_dir_for` | group `e8a90d94` (5 lines, `work_dir_for` only) | `spec_paths` diverged in SHAPE from `kitlib.registry.spec_files` (one function vs a helper plus a `sorted`), so the AST hash missed it. Same behaviour; consolidated. |
| — | group `13e012ea` (16 lines): `kitlib/evidence.field_block` vs `kitlib/stage.field_block` | NOT in item 4 and NOT in the population that list was derived from: both modules landed after it was written (WI-500 / WI-498 slice 1). Taken here because it is the same slice's work. |

### Per-group disposition

Copies were diffed before anything moved.

| behaviour | homes before | home now | disagreement found |
| --- | --- | --- | --- |
| `_process_check` | `check_trajectory.py`, `gen_okf.py` | `kitlib.config.process_check` | none in the CODE — see the finding below, which is about the STATED reason |
| the multi-ref cell split | `check_trajectory._split_refs`, `gen_okf.split_refs`, `plan_coverage.split_refs`, `plan_artifacts._split_tokens`, `schedule._split_refs`, `kitlib.spine.refs` | `kitlib.spine.refs` (already there) | none NOW; `plan_coverage`'s copy had split on `[;,]` alone until a pin repaired it (B10, part-A census 2026-08-13) |
| `is_example` | `gen_release_checklist.py`, `kitlib.spine` | `kitlib.spine.is_example` | none now; the `None`-crashing copy was repaired at the 2026-08-12 census and the guard is in the shared home |
| the module-path key (`norm_module` + `MODULE_EXTS`) | `check_trajectory.py`, `gen_arch_map.py`, `trace_text.py` (and `trace.py` by alias) | `kitlib.spine.norm_module` / `.MODULE_EXTS` | none in behaviour; a FALSE SYNC CLAIM and a census blind spot, both below |
| the root-relative need rows | `traj_parse._sn_rows`, `gen_okf.sn_rows` | `spine_carrier.needs_for_root` | none; both were one-line delegations composing the same relpath |
| the `k = v` block renderer | `kitlib/evidence.field_block`, `kitlib/stage.field_block` | `kitlib.evidence.render_fields`, called by both | none in the shared part; the two bodies were byte-identical while binding DIFFERENT `FIELDS` and `_fmt`, so the shared rule is the line join and the differing halves are now ARGUMENTS |
| the spec-folder read side | `wi_convert.work_dir_for` / `.spec_paths`, `kitlib.registry.spec_work_dir` / `.spec_files` | `kitlib.registry` | none |

**`kitlib/registry.py`'s WI-504 both-roots union is NOT touched.** `spec_roots`
and `read_spec_rows` are READER concerns; `wi_convert` is the WRITER, and a
writer files into the active workspace, never into the archive. It re-exports
the two single-root primitives and nothing else.

### Three findings

**1. A copy's stated reason for existing did not describe the copy.**
`check_trajectory._process_check`'s docstring argued that `kitlib` owned the
declared-LINE rule but not "this module's `[checks]` POLICY — which key, which
fail-direction, which residual", and that "folding the policy in would put one
checker's decision in a library every checker imports". Only the key is the
caller's, and it is a **parameter**. The fail-direction (present-but-unparseable
reads ON, loudly) and the residual (undeclared -> `None`, fall through to the
legacy one-word dial) were hardcoded identically in both bodies. Nothing
module-specific was ever encoded, so the equality pin was holding one decision
equal to itself with a copy in between. This is the declared-line shape again: a
prose justification that reads convincingly and is false about the code beneath
it. `subagent_gate.read_process_policy` is genuinely different (a WORD-valued
dial with an `UNPARSEABLE` sentinel so `decide()` fails closed) and stays its own
reader — that is what the retired docstring's argument would have looked like if
it had been true.

**2. A sync claim naming a home that does not exist.**
`check_trajectory._MODULE_EXTS` carried "Kept in sync with `trace.py._MODULE_EXTS`".
`trace.py` has never held that name — it takes the tuple from `trace_text.py`,
which WI-464 made its home. The comment named nobody, so the promise could not be
broken and could not be kept. Its real second copy was `gen_arch_map.py`'s, which
the comment did not mention.

**3. The census is blind to a copy that renames the constant it reads.**
`norm_module` had four homes and scored as ONE group of two, because
`trace_text.py` spelled the tuple `MODULE_EXTS` where the other two spelled it
`_MODULE_EXTS`, and `check_dupes_census.measure` hashes the body AST including
the loaded NAME. The fourth copy only became visible once the shared home settled
on one spelling — mid-slice the census went 6 -> 1 and the surviving group was
`kitlib.spine.norm_module` against `trace_text.norm_module`, a copy that had been
invisible the whole time. Renaming a local is not drift, but it hides a copy from
the instrument, which is the same structural blindness class as slice 3's
`set`-vs-`tuple` case. Recorded in `docs/stack.ini`'s re-stamp and in
`tests/test_rule_sync.py`; not fixed here, because widening the hash to ignore
loaded names would group functions that genuinely read different tables.

### Pins retired, and what replaced them

Six equality tests in `tests/test_rule_sync.py` are deleted with the reasoning
recorded in their place, per slice 3's pattern:

* `test_the_three_local_checks_readers_agree_by_value` and
  `test_an_absent_process_toml_is_undeclared_in_all_three_copies` (the CT/OKF
  limbs) — the two readers are one object.
* `test_is_example_agrees_across_all_three_copies_including_none` — the third
  home is a re-export.
* `test_ref_splitting_agrees_across_plan_coverage_and_check_trajectory` — all
  six homes are one object.
* the `rows == OKF.sn_rows(tmp_path)` limb of
  `test_sn_field_mapping_agrees_across_all_three_readers` — one object compared
  to itself.

Replacements, and the split is the same one slice 3 drew:

* **IDENTITY (the deletions' warrant):** `test_the_cell_shape_rules_are_one_home`
  asserts every re-exported name **is** the `kitlib.spine` object (`is`, not
  `==`), across `is_example`, all five external ref-split names, all three
  `norm_module` names and all three `MODULE_EXTS` names, plus the `trace.py`
  link at the end of the `trace_text` chain. `test_the_checks_reader_is_one_home`
  does the same for `kitlib.config.process_check`. The two need-row wrappers are
  pinned identical to **each module's own** `spine_carrier` instance, because
  `load_script` builds a fresh module object per call and a cross-instance `is`
  would fail for a reason about the fixture.
* **BY VALUE (the half that was never about sameness):**
  `test_the_placeholder_test_and_the_ref_split_answer_by_value` keeps the `None`
  case (one home used to crash on it) and every whitespace shape B10's drifted
  copy got wrong; `test_the_module_key_answers_by_value` is NEW — the module key
  had four homes and no pin at all — and drives the three spellings that must
  collapse, a Windows-authored cell, `__init__` stripping, every declared
  extension, and a `.md` path that must NOT be stripped;
  `test_the_checks_reader_answers_by_value` keeps the file-shape table and adds
  the one thing the retired pin never checked: a key the section does not carry
  reads UNDECLARED rather than the other key's value, which is the
  parameterization the copies' docstrings mistook for policy.

### Measurements

Census, before and after, one command both revisions:

<!-- fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev="77d67c38 (before) and this commit's tree (after)" -->

    before  6 group(s) / 6 redundant copy/copies / 76 redundant line(s)
    after   0 group(s) / 0 redundant copy/copies / 0 redundant line(s)

`docs/stack.ini` `[dupes-census]` is re-stamped down to `0 / 0 / 0` with that
reason, and its `fig:` marker now names `check_dupes_census.py` instead of the
retired `python -c` one-liner — WI-507 made that walk a named script, which is
the 0->A->B rule the census itself measures, applied to the census's own
provenance line. **Zero is a reading, not a floor:** the check stays armed and
warn-first (D-7), so a future duplicate re-appears as a WARN against `0/0/0`.

Module-size ratchet: **one** entry fires, re-stamped down in this commit —
`check_trajectory.py` 4791 -> 4765 (three helper bodies became one-line
re-exports and the now-unused `tomllib` import went with them). No other module
crossed its baseline or the 1500-line threshold.

Byte-budgeted files: untouched.

### Gates

    python -m pytest -q -n auto -m smoke
    1283 passed, 5 skipped in 23.11s   (re-run after the last docstring edit)

    python -m pytest -q -n auto --basetemp=D:/pytest-tmp-w448b   (full, unfiltered)
    2937 passed, 14 skipped in 1090.41s (0:18:10)

The full run was started once the code was final. Three edits landed after it
began — two docstring blocks (`kitlib/__init__.py`'s roster, `kitlib.spine`'s
`norm_module`) and the `RESYNC_PACK.md` entry — none of them executable. They
are covered by the smoke re-run above plus `tests/test_resync_pack.py`,
`tests/test_old_kit_resync.py`, `tests/test_generated_newlines.py` and
`tests/test_kit_path_invariant.py` (31 passed), which are the tests that read
those three files. Stated rather than implied, because "the full suite covered
this tree" would not have been true of them.

`check_smoke_budget.py --mode enforce` (20.6 s vs the 60 s budget),
`check_docs.py --root . --stale` and `check_trajectory.py --strict` all clean.
`ruff check` clean over `project-trajectory/scripts/` and the edited test. A real scaffold was bootstrapped and
the consolidated scripts were run inside it, per the standing lesson — no
`MAPPING` change was needed, because every home is a module already in it.

### Adopter-facing

`RESYNC_PACK.md` §3 takes an entry `[since 77d67c38]`. It is the first one in
the `kitlib` series that adds NO module — nine files before, nine after — so its
action line is "you need do nothing but keep copying the package whole", and the
body lists every re-exported name for a downstream that carries its own copy of
one. The kit README, `bootstrap.MAPPING`, `tests/test_bootstrap.py`'s file list
and the package roster's module count are all unchanged for the same reason; the
roster's per-theme descriptions grew, and it now records why no module was added.

### Deviations from the brief

* **Item 2 (`STACK_OI3_ROW`) did NOT ride.** The brief's condition was that the
  open-items key vocabulary land naturally in this movement, and it did not:
  every home this slice touched is a *cell-shape* or *declared-policy-file*
  theme, and nothing here goes near the open-items registry's keys. Taking it
  would have meant inventing a theme to carry one constant. It stays owed, and
  the stale premise comment on
  `test_rule_sync.test_bootstraps_scaffolded_brief_uses_the_converters_own_keys`
  stays with it, since the spec ties the correction to the duplicate's removal.
* **One group beyond item 4's list was taken** (`field_block`), because the
  census names it and it post-dates the list.
* **Four copies beyond the census were taken** (`is_example`'s third home, four
  more ref splitters, two more `norm_module` homes, `wi_convert.spec_paths`),
  because diffing the copies found them and leaving a known copy standing to
  keep a number tidy is the inverse of this row's point.
* **One near-copy was left standing and is recorded rather than fixed:**
  `gen_release_checklist.load_csv` is `kitlib.spine.load_csv` without
  `errors="replace"`. Adopting the shared home would CHANGE decode behaviour on
  a mis-encoded registry (crash -> replacement character), which is a behaviour
  decision, not a consolidation, and this slice's rule was byte-identical CLI.
  Left for whoever takes item 2.
