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
- **The two T6 exceptions review round 1 forced in**, both driven before being
  written: T6 is not a pin but **load-bearing** on the shipped document — its
  non-vacuity floor `nodes >= 50` reaches only **33** node pairs over the seven
  fresh fixtures, so following the contract's own filter remedy reds it on a
  floor unrelated to the emitter under change (replacement fixture first, filter
  second); and the LABEL triage covers only the per-document assertions, since
  T6's closing assertions run over a cross-document `text_fills` dict keyed by
  CSS selector and surface a disagreement as
  `('#dag .wi text', {'invariant', 'varying'})` — selector, never label.

**What deliberately did not ship.** The shared fresh-emitting fixture of the
original medium-tier filing — rejected in the ruling as enforcement-layer growth
whose failure mode ("a future test author gets confused") does not justify a
medium build. So: no new fixture, no new test, no helper signature change, no
behaviour change at all (proven by AST comparison with docstrings stripped, base
→ tip). The per-caller exclusion pattern is untouched, which is the ruling's
explicit ask.

**Two corrections to this WI's own record**, both found in review round 1 and
worth more than the fix they cost:

1. **The re-open pointer was wrong.** The filing and the ruling both say the
   shared-fixture evidence "stays in WI-367-REVIEW-A if it re-opens" — it never
   did. [WI-367-REVIEW-A](../reviews/WI-367-REVIEW-A.md) carries the port-fan
   7.90 px figure, the sw-0 / layer-count record figures and the `_path_xs` Q
   gap, and no version of it mentions `_every_emitter_document` (one commit,
   `c8750e7`). The builder's finding survives verbatim in the WI's own intake
   title, and the archived row now says so — the pointer resolved to a file that
   never held the evidence.
2. **The close commit's stated lane mechanism is false.** `059e7e5` says the
   emptied claim directory is "left on disk deliberately" because `check.py`
   keys on `docs/work/active/<branch>/` existing. It is not on disk (git prunes
   an emptied directory on checkout) and that is not what holds the lane:
   **WI-357 replaced that workaround with a git-history fallback**
   ([check.py:1095-1116](../../project-trajectory/scripts/check.py#L1095-L1116))
   — the base commit that cut the branch added the directory, and that add stays
   reachable, so `_work_branch` still answers `wi-372-emitter-truth-times` with
   nothing on disk and the §5.2 freshness skips still fire. The commit message
   recorded the *pre*-WI-357 workaround as if it were live; the true mechanism is
   here, in the surface that gets compiled into the log.

**Deviations from spec.** None.

**Review round record ([WI-372-REVIEW-A](../reviews/WI-372-REVIEW-A.md)).**
Round 1: CHANGES-REQUESTED, findings=4 (1 MAJOR, 3 MINOR). **All four confirmed
by independent reproduction before any fix, none refuted** — the finding
lifecycle applied to a documentation change, where "it reads plausibly" is
exactly the trap. The MAJOR is the one that matters: a docs-only WI can ship a
contract that is *wrong*, which is worse than no contract because a successor
trusts it — and the reviewer broke it by simply following its own prescribed
remedy (`lb != "shipped"`) at the one call site where that reds the test. Both
T6 exceptions are now in the docstring with their measurement dates. The two
record corrections above are the other findings; the fourth (the T6 label
triage) is folded into the same paragraph. The reviewer also proved the
zero-behaviour-change claim rather than accepting it, by comparing the module's
AST with all docstrings stripped across base → tip.

**Byte deltas on budgeted files.** None — `AGENTS.template.md`, `PROCESS.md` and
`PROCESS_OPTIONS.md` are untouched. The one file changed is
`tests/test_gen_trajectory.py` (+36 lines, all docstring); the module-size
ratchet reads kit scripts only, not `tests/`, and does not move.

**Bar** (measured after the round-1 fixes, on the tree this fragment ships with).
Full unfiltered suite `python -m pytest -q -n auto`:
**1 failed, 1691 passed, 7 skipped in 655.35s**; smoke tier
`python -m pytest -q -n auto -m smoke`: **1 failed, 555 passed in 11.70s** — in
both, the sole failure is the standing WI-357 work-branch conditional
`test_check_lane.py::test_this_repo_is_not_a_work_branch`, red for the life of
any claimed branch and green on the composed trunk tree (the same shape WI-373's
close recorded). `check_docs.py --stale` OK — 325 doc(s), 930 intra-repo
link(s), 0 broken (the standing `status.md is 266 lines (budget 120)` WARN is
pre-existing; `status.md` is untouched here). `check_trajectory.py --strict` clean (371 work items, 355
done, graph acyclic; only the three pre-existing IF-seam WARNs).
`ruff format --check` + `ruff check` clean on the changed file.

**A measurement lesson worth the line: don't run the suite on a tree you are
still editing.** The first post-fix full run reported **2 failed** — the standing
conditional plus `test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`
— and the second failure was an artifact of the run itself: the review file
existed as an unlinked orphan during the window in which this fragment had not
yet grown its link to it. Re-run on a quiescent tree, the same test passes in
1.17 s and the suite totals as above. This repo already has the sibling rule for
line endings ("measure on a tree whose line endings match the index, or the
measurement lies", status.md); the general form is that **a live working tree is
part of the measurement**, and an 11-minute run edited mid-flight has no single
tree to be true of.
