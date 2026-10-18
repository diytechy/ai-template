## 2026-10-18 — WI-915: the build, stage 2 (P2 to P9): `docs/stack.ini` is read through one reader

### What the stage built

`kitlib/config.py` gains `STACK_INI`, `StackIniError` and
`read_stack_ini(path, *, fold_keys=True)`, the one `ConfigParser`
construction under `project-trajectory/scripts` and `scripts`. The 13 sites
read through it, each keeping its name, key case, defaults and failure rule;
the restating parse comments point at the reader. The characterization
test's 17 ruled cells lost their expected-failure marks, and
`tests/test_stack_profile.py` gained the reader's unit tests and a one-home
pin. `tests/test_flag_axis.py` imports `configparser` itself.

### Red before green

The builder (Claude Opus, medium, the `kit-builder` agent), with the one
fixed basetemp, `-p no:cacheprovider` and
`GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`:

- Red, the committed stage-1 tree, `tests/test_stack_profile.py -k
  "keeps_its_outcome or marks_exactly" --runxfail`: `17 failed, 101 passed`,
  exactly the 17 ruled cells.
- Red, the new reader tests over the unchanged `kitlib/config.py`: `7 failed,
  100 passed, 17 xfailed` (`AttributeError`: no `read_stack_ini`; the
  one-home pin listing the 12 other files; a cell still marked).
- Green, the 21 affected modules with `--runxfail` after the change:
  `759 passed, 4 skipped`.

### Ratchet re-stamps

Measured with `check_complexity.module_sloc`, the ratchet's own census, after
the edits and before the bar:

- `trace.py`: 3776 -> 3775. `_cmd_tests_for` reads its test root through the
  reader, and the module's `configparser` import goes.
- `check.py`: 1307 -> 1298. `load_profile` and `_generated_census` read
  through the reader and map its one error onto their own outcomes, and the
  module's `configparser` import goes.
- `integrate.py`: 1551 -> 1548. `_generated_table` reads the `[generated]`
  keys through the reader, as written.
- `agent_common.py`: 1053, unchanged, so no re-stamp.
- `[dupes-census]`: 2/2/32 before and after, so no re-stamp.

### The commit bar

`run_menu.py smoke`, twice on the finished tree: both runs `2695 passed,
2 skipped`, `check_trajectory: clean`, `Traceability: ... orphans=0
integrity=0`. The first run's smoke tier took 80.9 s against the 60 s budget
(exit 1); the second, with the box quieter, 59.1 s, within (exit 0). The
tier's membership is unchanged by this stage.
