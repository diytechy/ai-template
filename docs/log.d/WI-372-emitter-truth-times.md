## 2026-07-30 — WI-372: the `_every_emitter_document` truth-time contract

The WI-367 builder's finding, closed as the owner narrowed it (ruling same day,
[log.md](../log.md) Decisions): **documentation only**. The whole-document sweep
helper in `tests/test_gen_trajectory.py` hands its callers a list mixing two
different truth-times, and every caller had to work that out for itself — the
WI-367 sweep did, by hand, and paid for it with a local exclusion and a
paragraph of reasoning that lived only at its own call site.

**What shipped.** One docstring on `_every_emitter_document`, stating the
contract in the one place a caller reads before using it:

- **`shipped`** is the COMMITTED `PROJECT_STATE.html` — markup an OLDER renderer
  wrote. Generated artifacts belong to the trunk lane (concurrency-restructure
  §5.2; `check.py` skips the freshness gates on a work branch), so off trunk this
  document legitimately lags the code under test. Asserting over it is a
  **compatibility pin** — "the invariant holds for the markup already in a
  reader's hands" — never "this emitter satisfies it"; and it is simply *absent*
  in a checkout with no committed dashboard, so a caller that reads it must still
  be meaningful fresh-only.
- **Every other label** is FRESH: built into `tmp_path` and rendered by this
  run's `gen_trajectory.py`.
- **The trap that mixture sets**, and whose it is: a change that TIGHTENS an
  invariant reds through the stale shipped copy rather than through the emitter
  it changed — the failure names an older renderer's markup while the code under
  test is clean. A caller wanting the CURRENT emitter's answer filters at the
  call site and supplies a fixture for whatever shape the shipped copy used to
  contribute; `test_svg_viewbox_contains_every_routed_wire` is cited as the
  worked example (`lb != "shipped"` plus `WRAPAROUND_WIS`).
- **Which callers pin on purpose**, enumerated mechanically over the file rather
  than from memory: the fourteen sweeps that keep `shipped` are the U1–U4 /
  A1–A3 / T6 uniformity-and-accessibility checks and T8's through-box sweep,
  with the triage rule the finding was really about — **read the failing LABEL
  first**: `shipped` means regenerate the dashboard on trunk, any other label
  means the emitter really regressed.
  `test_a2_the_repos_own_shipped_dashboard_holds_the_invariant` is
  cross-referenced as the same pin made without the helper.

**What deliberately did not ship.** The shared fresh-emitting fixture of the
original medium-tier filing — rejected in the ruling as enforcement-layer growth
whose failure mode ("a future test author gets confused") does not justify a
medium build. So: no new fixture, no new test, no helper signature change, no
behaviour change at all. The evidence stays in
[WI-367-REVIEW-A](../reviews/WI-367-REVIEW-A.md) if it ever re-opens. The
per-caller exclusion pattern is untouched, which is the ruling's explicit ask.

**Deviations from spec.** None.

**Byte deltas on budgeted files.** None — `AGENTS.template.md`, `PROCESS.md` and
`PROCESS_OPTIONS.md` are untouched. The one file changed is
`tests/test_gen_trajectory.py` (+36 lines, all docstring); the module-size
ratchet reads kit scripts only, not `tests/`, and does not move.

**Bar.** Full unfiltered suite `python -m pytest -q -n auto`:
**1 failed, 1691 passed, 7 skipped in 629.93s**; smoke tier
`python -m pytest -q -n auto -m smoke`: **1 failed, 555 passed in 10.81s** — in
both, the sole failure is the standing WI-357 work-branch conditional
`test_check_lane.py::test_this_repo_is_not_a_work_branch`, red for the life of
any claimed branch and green on the composed trunk tree (the same shape WI-373's
close recorded). `check_docs.py --stale` OK — 324 doc(s), 928 intra-repo
link(s), 0 broken (the standing `status.md is 266 lines (budget 120)` WARN is
pre-existing; `status.md` is untouched here). `check_trajectory.py --strict` clean (371 work items, 355
done, graph acyclic; only the three pre-existing IF-seam WARNs).
`ruff format --check` + `ruff check` clean on the changed file.
