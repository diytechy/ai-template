## 2026-08-01 — WI-398: a red bar's refusal carries the failing step's own output

**Summary.** A red bar's refusal message structurally could not carry the
failing step's own output: `agent_common._failure_tail` anchored on the LAST
`  FAIL  <step>` line, and `check.py`'s closing summary block re-prints every
step's status at any `--jobs`, so the anchor always landed in the summary copy,
the nearest banner above it was the LAST step's, and the extracted window was
summary rows — never the error text. Driven cost (handoff-2026-08-01 §6): the
WI-387 refresh red was diagnosed and lost THREE times, compounded by the
refresh's undo resetting the very tree that held the evidence. Both halves
fixed: the anchor now extracts the failing step's own window, and a refused
refresh retains its full output at a path the refusal message names.

**Deliverables.**

- **The anchor** (`agent_common._failure_tail` + the extracted
  `_own_step_window`): the FIRST `  FAIL  <step>` line names the failing step,
  and the window is that step's OWN `=== <step> : ` banner down to the next
  banner or the summary rule — found by NAME (startswith, not an interpolated
  regex: step names carry regex metacharacters, `tests+coverage`), so the
  `--jobs 1` shape, where statuses print only in the summary, still reaches the
  step's streamed output, with the anchoring FAIL row appended so the refusal
  names the step and exit. No banner names the step → the WI-240 fallback
  window anchored on the first FAIL; no FAIL marker → the bounded tail;
  `check.py`'s own printing is untouched (the spec offered re-emitting the
  failing step's output after the summary as the alternative — the anchor fix
  was judged smaller: zero output-shape change, and every `_failure_tail`
  consumer — `integrate.py`, `handback.py`, `agent_common`'s commit journal —
  inherits it).
- **The retained evidence** (`integrate._keep_refused_output`): every refresh
  refusal that reaches `undo` writes its FULL output to
  `out/run-logs/refresh-refused-<branch>.log` in the ROOT checkout — outside
  the lane worktree, so neither the `reset --hard` nor `_shed_residue` can
  sweep it — and the refusal message names the path. One file per branch,
  overwritten by the branch's next refusal; deliberately NO rotation, indexing
  or pruning (the spec's scope guard), and fail-soft (a log that cannot be
  written must not mask the refusal it documents; empty output keeps nothing).
  The home is already gitignored here (`out/`) and in the shipped scaffold
  (`gitignore.template`'s `out/run-logs/`), so the kept log can never dirty a
  trunk the claim rung would then refuse.
- **Driven, red-then-green (the mutation-twin discipline):** two new
  `_failure_tail` fixtures — the `--jobs 0` shape `_run_bar` produces and the
  `--jobs 1` summary-only shape — plus the end-to-end
  `test_a_red_refusal_carries_the_steps_own_output_and_names_the_kept_log`
  (a real red refresh over the enriched `STUB_CHECK_RED`, which now prints the
  real banner/inline-status/summary shape). All three FAILED under the old
  anchor — the watched red measured the exact defect: the extracted window was
  `=== trajectory` banner + `Check summary` rows, zero bytes of the failing
  step's output — and pass under the fix, with the kept log asserted to hold
  the whole output, survive the undo, and leave both trees clean.

**Deviations and judgments.**

1. **Registration: no new LLR/TC rows owed.** Both surfaces are internals of
   already-registered rows — `integrate.py` under SR-132/LLR-140 with TC-132's
   suite-level coverage, `_failure_tail` a private helper exercised by that
   suite and `tests/test_agent_common_harness.py`. The WI-374/WI-387 precedent
   files rows for NEW modules; no module was added.
2. **Size ratchet re-stamped upward, reasons in the baseline comments:**
   `agent_common.py` 1741 → 1784 (the anchor rewrite + the docstring history
   that keeps a successor from "simplifying" back to last-FAIL; the C901
   ratchet's preferred extraction, `_own_step_window`, taken rather than a
   complexity bump), `integrate.py` 1946 → 1977 (`_keep_refused_output` and
   its no-log-management statement).
3. **The kept log covers every `undo` path, not only the red bar** — a
   conflicting trunk merge and a failed trunk step lose their evidence to the
   same reset. One mechanism, one file; narrowing it to the bar branch would
   have been more code, not less.

**Watched, measured on the build commit b121aba8 (clean tree):**
`tests/test_agent_common_harness.py` 17 passed in 0.02s
<!-- fig: cmd="python -m pytest -q -p no:xdist tests/test_agent_common_harness.py" rev=b121aba8 -->;
the three consumer suites (integrate + handback + drive) 137 passed in 26.68s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_integrate.py tests/test_handback.py tests/test_drive.py" rev=b121aba8 -->;
smoke tier 615 passed / 6 skipped in 10.98s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b121aba8 -->
(the watched red first: 3 failed on the pre-fix tree — the two anchor fixtures
and the e2e kept-log test — historical, that tree is gone);
`check_trajectory` / `check_doc_refs` / `check_figures` all rc=0 under
`--strict`.
