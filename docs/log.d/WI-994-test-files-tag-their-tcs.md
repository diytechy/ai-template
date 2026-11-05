## 2026-11-04 — WI-994: test files name their test cases on the `Implements:` line

Deferred open items: none.

`gen_arch_map.read_test_tags` reads the tags under the declared tests root and
`trajectory_arch.tc_tag_findings` carries its four refusals into
`check_trajectory`, a WARN and an ERROR under `--strict`.

- `gen_arch_map.py` is bumped +134 (1433 -> 1567 SLOC): the reader and its
  helpers. The spec fixes its home beside `declaration_sites`, because it shares
  the one grammar with `backlink_ids`; the plan's estimate was about 90.
- `gen_arch_map.py` is bumped +2 more (1567 -> 1569 SLOC): the wrap check also
  refuses a next line led by a comma or `and`, which takes one small pattern and
  the predicate's early return, and `backlink_ids` now calls the opening helper
  the tag reader calls, so the opening rule has one application.
- `check_trajectory.py` is bumped +2 (1656 -> 1658 SLOC): the binding line and
  the one term in the promotable loop. `trajectory_arch.py` stands at 971, under
  the 1000 threshold, and takes no baseline row.
- The code side reads as it did. Base `36ad6489f`'s `gen_arch_map.py`, taken by
  `git show` into the review scratch, and the lane's copy, both over the lane's
  `project-trajectory/scripts`, gave equal `scan_backlinks` and
  `implements_report` output.
- `gen_arch_map.py` is bumped +6 more (1569 -> 1575 SLOC): a `test*`-named def
  decorated as a pytest fixture is no read position, which takes `_is_test_def`
  and the decorator names it reads, and the malformed message gives Python
  advice apart from non-Python advice, because the reader refuses every Python
  comment tag as misplaced.

**Added wall time on the bar.** `check_trajectory.py --strict`, which the bar
runs once, takes about 2.5 s more with the check: a median of 80.59 s before
(min 78.98, max 81.29) and 83.10 s after (min 82.69, max 89.78), a difference of
3.71 s between the minimums. Each side ran three times, interleaved after one
warm-up run each, over the lane's tree, and all six timed runs exited 0 clean.
"Before" is base `36ad6489f`'s scripts and "after" is the lane's.
<!-- fig: cmd="python measure.py 3 (scratch timer: check_trajectory.py --root <lane> --strict, base scripts against lane scripts, interleaved)" rev=fbaefe99b + this change -->

The box was not quiet, so these are loaded figures, not the quiet figure the
plan asked for: total CPU read 18.6% to 25.9% across 24 logical processors,
sampled five times before and five times after, with 16 `python.exe` processes
running, other sessions' among them. Three runs a side on a loaded box is a
small sample, so read the difference as a few seconds and not as a precise
figure.

**The characterization pin's deliberate red.** On a scratch copy outside the
lane, `test_the_code_side_readers_keep_their_output_over_the_scripts_tree` passed
unchanged (`1 passed`). With `_DECL_OPENING` loosened to `^.*$` in that copy it
went red (`1 failed`), at its comparison with the frozen rule. The lane's rule
was never altered.

**Not in this row:** this repository's own test-file tags (WI-997), the derived
review test set and its refusals (WI-995), the strict-mark commit check and
`[bars] red_mark` (WI-996), and the generated evidence column (item 5). The
RESYNC entry states the same list.
