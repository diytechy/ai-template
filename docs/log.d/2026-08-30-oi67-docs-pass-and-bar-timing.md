## 2026-08-30 — docs: the OI-67 program's shipped and reference docs brought level with the tree, and the bar's wall time measured piece by piece

Deferred open items: none — a docs pass and a measurement; the one thing it
surfaces for work (the two five-minute graph tests) is named below for the
next session to file, not a ruling owed.

**Summary.** After the slice-6 round and the arms landed, six documents still
described the tier as it was before them; each now states the tree — and the
sweep found three more copies of one retired claim. Then, because the owner
saw "45 minutes" and asked what the bar really costs, the bar was measured
leg by leg on this box, with the full suite profiled per test in an isolated
worktree at HEAD.

**The docs, and the single-source discipline they follow.** Each rule is
STATED once and pointed at, never re-worded: the no-in-tree-endpoint rule
(decision 6.8) is stated in the registry header and the two template headers
(`interfaces.toml`, `registries/interfaces.template.toml`,
`INTERFACES.template.md`); `docs/registry-machinery-reference.md`'s IF row now
carries the presence-based retired-cell rule, that rule, and the definition
gate's four shapes with its severity ladder; `project-trajectory/RESYNC_PACK.md`
gains the entry adopters resync by (`[since 7fc42a5a]`: the refused header,
the retired column, the no-in-tree-endpoint refusal, the `csv_body` preamble
and its reach, the `gen_arch_map` multi-mode behaviour change, `schedule
--jobs`, the one `.gitignore` line to copy by hand); `project-trajectory/
MULTI_REPO.md` §3.3 agrees with the rewritten `EXAMPLE.md` §10 — a surface no
repo builds is an `external:`-owned row in the repo that USES it, its
definition our reading in the facing module's header — and the same retired
"coordinator-held row is the owner of record" claim was found and corrected in
`PROCESS.md` §8's purchased-part sentence, `PROCESS_OPTIONS.md`'s procurement
paragraph and `EXAMPLE.md`'s own `REPO-004` note; the plan of record's §0
closes the program; `tests/integrate_fixtures.py`'s docstring no longer
records a gitignore gap the template closed. `CLAUDE.md`'s "~6 min" for the
full suite — a 2026-08-02 number — reads "~10 min on a quiet box, 3–4× that
while other sessions load it".

**The bar, measured.** Three things get called "the bar" and they cost very
different amounts; the 45 minutes the owner saw was the third.

1. *The pre-commit hook's floor* (every commit, automatic): 17 steps,
   **47–58 s** on this box today across three commits — `trajectory-map`
   11–13 s, `open-items` 11–12 s, `trajectory` 8–10 s, `registry-integrity`
   5.5–7 s, `approval-fresh` 2–3 s, the other twelve under 2 s each.
2. *The commit bar the session-protocol names* (smoke tier + budget +
   `check_docs --stale`, before each commit): the smoke tier read **27 s** at
   the WI-496 re-tier on a quiet box and **70–180 s** today (1,378 passed, 6
   skipped; 1,384 collected) with other sessions holding 50–90 % of the CPU;
   `check_docs --stale` ~5 s. The tier's slowest test is 17 s
   (`test_id_watermark`'s live-marks guard); the next twenty-four are 5–9 s,
   most of them a scaffold bootstrap in `setup`. So a commit costs **one to
   four minutes** today, of which the hook is one.
3. *The full unfiltered suite* (a WI close, a phase close, a broad script
   change — NOT per commit): **~5 min on 2026-08-02** (296–341 s, four runs),
   **~10 min on a quiet box on 2026-08-29** (581 s and 591 s, 3,068–3,077
   tests, the smoke tier at 19–25 s beside them), and **28–45 min** whenever
   other sessions load the box (1,706–2,676 s, the smoke tier at 88–180 s
   beside them). Profiled per test in an isolated worktree at `b19d4bf7`:
   1,669.61 s wall (27:49) at ~60–80 % external load, and the forty slowest
   tests sum to **2,452 s of worker time** — `test_dispatch` 573 s (nine
   end-to-end lane runs at 60–90 s each, real git and hooks in subprocesses),
   `test_traj_graph` 484 s, `test_agent_loop_review` 312 s,
   `test_integrate_station` 260 s, `test_check_harness` 157 s,
   `test_integrate_unload` 147 s, `test_integrate_admission` 133 s. **The
   single slowest test is 304 s** —
   `test_traj_graph::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes`,
   the wire-through-box invariant checked over the REAL meta repo's Knowledge
   graph and When roadmap — with its sibling `test_fallback_dag_and_sw_graph…`
   at 129 s: one test bounds the whole suite's wall time from below at five
   minutes on any number of cores, and the pair is roughly half of the quiet
   ten. (The profile's one failure was the worktree's: `test_check_docs`'s
   meta-root orphan census found `docs/test/README.md` linking a
   `report.md` the fresh worktree had never generated; the same test passed
   in the main checkout's two full runs.)
<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -n auto --durations=40" rev=b19d4bf7 -->

**What that says.** The suite has doubled since August 2 (~5 → ~10 min quiet)
and the box's other sessions triple it on top; neither is a defect in the
bar's design, but the 304-second test is a hotspot worth a row of its own —
`_wire_through_box_violations` over a real-scale SVG looks quadratic in
elements — and the nine dispatch lanes are the second. Filed as topics for
the next session, not here.

**One incident, owned and repaired.** The profiling worktree borrowed the
main checkout's `.venv` through a directory junction; the junction's own
removal failed silently on a quoting error, and `git worktree remove
--force` then followed it and emptied `C:\Projectsi-template\.venv` —
no tracked file was touched (`git ls-files -d` reads 0). Rebuilt on the
spot from `requirements-dev.txt` (Python 3.11.9; ruff 0.15.22, pytest 9.1.1,
pytest-cov 7.1.0, pytest-xdist 3.8.0), verified by the hook's format step
over 224 files and the smoke tier above. The lesson is in the session
memory: never junction a shared venv into a throwaway worktree — point the
worktree's runs at the absolute interpreter path instead.

**Deviations from spec:** none — a docs pass the owner asked for, plus the
measurement they asked for with it.

**Byte deltas on budgeted files:** `PROCESS.md` +35 (87,836 → 87,871;
watched, flagged in the guard's table); `PROCESS_OPTIONS.md` +49
(179,209 → 179,258; watched, flagged); `CLAUDE.md` +59 (7,827 → 7,886; cap
8,500); the guard skill 4,795 → 4,938 (cap 5,000); `AGENTS.template.md`
untouched.

**pytest totals:** smoke tier under Git Bash `-m smoke --durations=25`:
**1378 passed, 6 skipped in 69.70 s**; the budget checker's own run **1378 passed, 6 skipped in 164.33 s → 165.1 s vs 60 s, OVER** on the loaded box (64 % external load at the sample), environmental, recorded, not waived; the byte-cap pins 3 passed;
`check_docs --stale`: 0 broken. No script changed, so the full suite is not
re-run here — its last run on this tree is the WI-534 close (3108 passed, 15
skipped) and the profile above (3107 passed, 1 worktree-only failure).
