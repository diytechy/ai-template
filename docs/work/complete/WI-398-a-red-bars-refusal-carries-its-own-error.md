+++
id = "WI-398"
title = "A RED BAR'S REFUSAL MUST CARRY THE FAILING STEP'S OWN OUTPUT - today it structurally cannot. MECHANISM: agent_common._failure_tail anchors on the LAST '  FAIL  <step>' line and walks back to the nearest '=== <step> :' banner, but check.py re-prints every step's status in its closing summary block at ANY --jobs value, so the anchor always lands in the summary copy and the extracted window is always summary lines - the per-step error text can never reach integrate's refusal message, at any parallelism, by construction. DRIVEN COST (2026-08-01, handoff-2026-08-01.md §6): the wi-387 refresh red cost THREE lost diagnoses of one failure - two integrate refusals and a re-run, each losing the error text - before a hand-rebuilt tree recovered it; compounding, the refresh's undo resets the lane on refusal, so the failing tree itself was gone each time the message was finally read. THE FIX IS NARROWING, NOT MACHINERY: anchor on the FIRST FAIL after the last banner (or have check.py re-emit the failing step's captured output once, after the summary - builder judges which is smaller), and on a refresh refusal keep the bar's full output at a path the refusal message NAMES, so the evidence survives the undo. DONE-WHEN, driven not asserted: a constructed red bar's refusal message contains the failing step's own output rather than summary lines, proven by a test that REDS under the current anchor and greens under the fix (the mutation-twin discipline); and a refused refresh leaves the full bar log at the path its message names, proven end-to-end. SCOPE GUARD: one anchor fix and one retained file - do not grow a log-management layer, and do not touch what a PASSING bar prints."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**The anchor fix** — `agent_common._failure_tail` no longer anchors on the LAST
`  FAIL  <step>` line (which `check.py`'s closing summary re-prints at any
`--jobs`, so the window was structurally always summary rows). The FIRST FAIL
line names the failing step, and the extracted window is that step's OWN
`=== <step> : ` banner down to the next banner or the summary rule
(`_own_step_window`, found by name via startswith — step names carry regex
metacharacters). The `--jobs 1` shape, where statuses print only in the
summary, appends the anchoring FAIL row so the refusal still names the step and
exit; no banner → the WI-240 fallback window; no FAIL marker → the bounded
tail. `check.py`'s own printing is untouched — the spec's alternative (re-emit
the failing step's output after the summary) was judged larger: it changes what
every bar prints, while the anchor fix changes nothing a PASSING bar does and
every `_failure_tail` consumer inherits it.

**The retained evidence** — every refresh refusal that reaches `undo` keeps its
FULL output at `out/run-logs/refresh-refused-<branch>.log` in the root checkout
(`integrate._keep_refused_output`): outside the lane worktree, so neither the
undo's `reset --hard` nor `_shed_residue` can sweep it, and the refusal message
names the path. One file per branch, overwritten by the next refusal —
deliberately NO rotation, indexing or pruning (the scope guard), fail-soft, and
the home is gitignored here and in the shipped scaffold so the kept log can
never dirty a trunk the claim rung would then refuse.

**Done-when, driven 2026-08-01:** the two new `_failure_tail` fixtures (the
`--jobs 0` and `--jobs 1` shapes) and the end-to-end
`test_a_red_refusal_carries_the_steps_own_output_and_names_the_kept_log` (a
real red refresh whose stub bar prints the real banner/status/summary shape)
all REDDED under the old anchor — the watched red measured the window as
`=== trajectory` banner + `Check summary` rows, zero bytes of the failing
step's output — and green under the fix, the kept log asserted to hold the
whole output and survive the undo. On the build commit b121aba8 (clean tree):
`tests/test_agent_common_harness.py` 17 passed in 0.02s
<!-- fig: cmd="python -m pytest -q -p no:xdist tests/test_agent_common_harness.py" rev=b121aba8 -->;
integrate + handback + drive 137 passed in 26.68s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_integrate.py tests/test_handback.py tests/test_drive.py" rev=b121aba8 -->;
smoke tier 615 passed / 6 skipped in 10.98s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b121aba8 -->;
`check_trajectory` / `check_doc_refs` / `check_figures` rc=0 under `--strict`.
Size ratchet re-stamped (agent_common.py 1741 → 1784, integrate.py 1946 → 1977,
reasons in the baseline comments); no new LLR/TC rows owed — both surfaces are
internals of SR-132/LLR-140's registered rows (the WI-374/WI-387 precedent
files rows only for new modules).
