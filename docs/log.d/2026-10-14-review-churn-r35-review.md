Deferred open items: OI-98 and OI-105 stay the owner's, each until its condition is met (the FileBackup re-sync; the FreeLLMAPI router).

## 2026-10-14: the review-churn plan's revision 35 review pair, and revision 36

A fresh session ran the plan's last plan-level review from
[review-handoff-r35.md](../plans/2026-10-11-review-churn/review-handoff-r35.md).
It took no lease, claimed and built nothing, and left `docs/work/pause`
unchanged. The only work-item edits are spec text in three queued rows,
following owner rulings.

- **Revision 35 review.** GPT-6 Astra (Codex 0.162.1) and Claude Fable 5.1 (a
  sub-agent), both at high, ran in parallel in detached worktrees at
  `4357b7d68` on `reviews/brief-r35.md`. They read what revisions 32–35
  changed and cross-checked the revision 35 rulings. Both left their worktree
  unchanged and returned REVISE (Astra 5 findings, Fable 12), and neither
  found a direction wrong. Judged by the handoff's three questions, the round
  came to 14 distinct points: 12 fixes and 2 owner calls. One finding was
  re-graded MINOR in part, three remedies were cut down, and two views were
  noted. The reviews are filed as `reviews/astra-high-r35.md` and
  `reviews/fable-high-r35.md`, and the dispositions are in `history.md`.
- **The brief's stale premise.** It said WI-858 was unbuilt, copying D-004's
  pre-landing wording; WI-858 landed on 2026-10-11 (`8b7e25e51`). Both
  reviewers read the built marker carrier instead, as the owner asked, and
  neither found a plausible break in normal use.
- **Revision 36** (`eb42a1c9a`) folded the fixes in:
  - B1 gives `coordinator_adjudicate.py` an act turn, because today it runs
    only a fresh judgement (a new verdict path, graded). The split covers
    both acting arms of the composer, the released re-attest and the held
    CLARITY re-attest.
  - B1's `spine-questions.md` rewrite keeps the traced `module` and
    `code_symbol` cells filled until item 5 removes them.
  - P2 settles where a call run on trunk (every scope critique) records its
    log. The plan's "one writer" is WI-800's store, not built yet, and
    serialized commits would still trip the other reviewer's change check.
  - The parent-LLR link names every walk from SR to LLR: the scoped test set,
    blast radius and component context, not only coverage and orphans.
  - G files with its own `needs`, B4 names its two cells, and stale "open"
    labels follow their rulings across the plan, the handoff and its session
    prompt.
  - WI-833, WI-850 and WI-851 drop the hand-merge path OI-113 (d) declined;
    OI-113's text and WI-893 now say WI-892 landed (`8d498e13f`).
- **The owner's two rulings** (revision 36), each walked with a real row:
  - Headless coordinator legs are marked **now**: the trailer instruction in
    B1's sitting briefs, a new queue row P9 (the marker in `overnight_legs.py`,
    the trailer on every headless commit, one lane-mode rule), and WI-851's
    marker arm narrowed instead of retired. The owner chose this over
    deferring the build or withdrawing the marking.
  - Interface consumers and requestors hand over **side by side**: each local
    side moves into code when a file of its component takes the interface,
    and a side code cannot reach, an `external:` party (69 of 243 IFs, IF-170
    among them), stays on the row. The owner first asked what they were
    missing; their own description of the flow was this option.
- `docs/status.md`'s resume line now points straight at the coordinator
  handoff, with no review pending.
- **Revision 37** (`0488eba14`), after the close-out, at the owner's
  questions: the program is ready with no further plan-level review, and it
  runs as separate lanes, not one branch, landing one mechanism change at a
  time. The owner's rulings:
  - three reviewers per round for this program only, as a trial: Sol medium,
    Fable medium, Opus high. Two stays the norm, and nothing is built for a
    third slot;
  - planners, builders and reviewers may spin up sub-agents within the
    spawning agent's bounds, and P2 records nested agents' usage;
  - a defect in a landed mechanism change is fixed forward, never by
    reverting the landing. The owner questioned the integrator's first
    wording ("revert, don't work around"), and the check confirmed it:
    `trace.py` refuses a lowered watermark mark, so a landing that minted ids
    cannot be reverted cleanly.

  The phase-0 baseline manifest, which nothing had scheduled, becomes the
  queue's row M.
- **Tests across parallel lanes** (owner, the same evening). The handoff
  gains four rules:
  - each test runner keeps its own `--basetemp`, a sub-agent included, since
    pytest deletes an existing basetemp when a run starts;
  - the landing's smoke-budget reading is taken quietly;
  - disk is the limit: 18.6 GB was free before a cleanup, and the 24
    logical CPUs are not the limit;
  - a red that passes when re-run quietly is filed as a defect.

  At the owner's request, the 44 worktrees of landed lanes were removed
  (branches kept), each checked first for a terminal spec and a clean status.
  `wi-880` is kept for the owner: it holds an uncommitted 4-line hook edit.
- **The coordinator's tools enter the repository** (owner, the same
  evening). On a second machine the coordinator found the recipes but not the
  Terra spine-author brief: the recipes ran ten tools from an untracked folder
  beside the checkout, a single unversioned copy.
  - The ten the procedure uses moved verbatim into `scripts/coordinator/`
    (`f8352b9eb`): this repo's own tooling, not shipped, since the kit is
    absorbing their jobs (WI-852's briefs, WI-801's `ask.py`, WI-812).
  - The next commit derives their paths from their own location
    (`layout.py`, `layout.sh`), and the recipes' `REPO`, `PY` and `TOOLS`
    from git, so no tool names a machine or a user. Verified on this machine
    by syntax checks, derived paths equal to the old literals, and a Terra
    brief whose only change is PowerShell's quoted call form.
  - Four retired files stay behind in the old folder, which is kept until the
    repo copy has run on a second machine. B1 takes the Terra brief's stale
    ruling-5 line.

The commit bar passed at `eb42a1c9a`: `2547 passed, 2 skipped` in the smoke
tier, `51.4s vs 60s budget -> within`.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce" rev=eb42a1c9a -->

Lesson for the procedure: a brief that cites a decision record's state
("nothing is built yet") inherits the record's date. Check the work item's
folder (`docs/archive/work/complete/`) before writing it into a brief.
