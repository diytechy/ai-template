## 2026-10-14: the review-churn plan's revision 31 review pair, revisions 32–34, and the revision 34 review brief

Deferred open items: none ruled. OI-98, OI-105, OI-112, OI-113 and OI-114
stay the owner's.

A fresh session ran the plan's last whole-plan review from
[review-handoff-r31.md](../plans/2026-10-11-review-churn/review-handoff-r31.md).
It took no lease, claimed and built nothing, and left `docs/work/pause`
unchanged.

- **Revision 31 review.** GPT-6 Astra (Codex 0.162.1) and Claude Fable 5.1 (a
  sub-agent), both at high, ran in parallel in detached worktrees at
  `4a25720e2` on `reviews/brief-r31.md`. Both left their worktree unchanged
  and returned REVISE (Astra 3 findings, Fable 9), and neither found a
  direction wrong. Judged by the handoff's three questions, the round came to
  14 distinct points: 10 fixes (two findings re-graded MINOR), 2 owner calls,
  and 2 views dismissed or noted. Three remedies were cut down. The reviews
  are filed as `reviews/astra-high-r31.md` and `reviews/fable-high-r31.md`,
  and the dispositions are in `history.md`.
- **Revision 32** (`cf6a72f19`) folded the fixes in:
  - The shipped sitting briefs put the act in the judging turn, so B1 now
    carries the verdict/act split, not only `coordinator-cycle` §4's text.
  - Item 8's wrappers would refuse the session service's own log commit, so
    the change check now runs between the service's `act` and `record`.
  - The coordinator handoff's queue, written at revision 13, gained a "pre"
    trunk fix and rows P1–P8 for phase 1. B1 asks the architectural-delta
    question without citing item 12's rubric, which doesn't exist yet.
  - B4 settles WI-902's lane acts 113–117 before it rebases onto B2's act.
  - `check_trajectory.py --strict` is red on trunk on WI-910's empty
    `specref`, not only `trace.py --strict` on LLR-292. The fix is left to
    the coordinator as the queue's "pre" row.
- **Revision 33** (`5b2ffc150`) records the owner's answers. Item 16's carrier
  carries spine ids only, since acts keep landing order and only trunk mints
  a WI id. A fix with no executable test is confirmed by independently
  checkable evidence, which the coordinator maps before the convergence
  round.
- **Revision 34** (`445104bfe`), at the owner's question: the plan's Sequence
  had left WI-902's reshape in phase 2, after the items that share its files.
  It is now in phase 1, after B1 and G and before items 15 and 16.
- **Revision 34 brief:** `reviews/brief-r34.md` and `review-handoff-r34.md`,
  for one narrow pair (Astra and Fable, both medium) that reads only what
  revisions 32–34 changed. The integrator recommended against another
  whole-plan review at high effort, since every queued row still gets its own
  scope critique; the delta's claims about existing code are unchecked.

Every commit passed the commit bar, for example at `445104bfe`:
`2547 passed, 2 skipped` in the smoke tier, `34.5s vs 60s budget -> within`.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce" rev=445104bfe -->

Lesson for the procedure: Python's `Path.write_text` on Windows writes CRLF.
Git normalized the committed blob, but the working copy showed a CRLF
warning; write with `newline="\n"` or as bytes. The r34 handoff says so.
