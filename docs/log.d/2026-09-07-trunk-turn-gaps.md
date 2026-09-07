## 2026-09-07 — Four mechanical gaps in the trunk-turn decision

Reviewed `9988c611` before implementation starts. Its two substantive additions
are sound and one corrects me: the stable-ID rule (an existing ID denotes a
stable meaning, so "reapproval" asks whether meaning held, and an actual change
owes impact review of every use) and the ruling that adjudication runs as an
exclusive coordinator turn in the primary checkout on the integration branch.

**Codex's correction to my earlier row is right.** I described the snapshot as
bounded by the `Adjudicates` cell. That is the first-approval arm only. In
`acceptance_record.merge_approval_refusal`, an adjudication branch whose
`first_approval_scope` is None and whose `approval_delta[0]` (the Status flips)
is empty falls through to `return delta[2]`, the read refusal alone — so an
AMENDMENT adjudication may write any snapshot file with no scope check at all.
That is the WI-605 path exactly, and it is a wider hole than I stated.

Four gaps found, recorded in the plan; no code, registry, queue or pause change.

1. **The trunk turn is a second writer on the merge slot's branch.**
   `integrate._slot` takes `out/integrate.lock` and its docstring states the
   assumption the move breaks: the slot is "held for well under a second."
   An adjudication turn is a provider session lasting minutes. Holding the
   slot for it queues every merge behind an LLM call; not holding it puts two
   processes on one working tree with nothing detecting the interleave, which
   is worse than today's merge conflict because Git catches that one.
   `integrate()` also refuses on a dirty trunk before taking the lock, so a
   mid-turn trunk makes the queue refuse itself. This is the owner's stated
   concurrency concern landing on the new design; it needs a decision and an
   honest throughput statement, not an assertion that ownership prevents
   interleaving.
2. **The adjudication close is branch-keyed.**
   `dispatch._close_done_adjudication(root, branch)` and
   `handback.close_adjudication(root, branch)` both key on a branch. A turn
   with no branch has no key, and that path exists because the dispatcher once
   resumed a finished adjudication row forever (OI-70 decision 21, the C6
   loop). Rehome it or the loop returns.
3. **No bar attests a trunk-side approval commit.** A lane branch carries
   `Bar-Green:` verified at the merge slot; a direct trunk commit has only the
   installed hooks, and the refresh/bar/merge sequence never runs.
4. **Six rows are shaped for worktree dispatch.** `WI-605` active (step 5
   covers it) plus `WI-601`, `WI-602`, `WI-603`, `WI-604` and `WI-606` queued
   as `safety_class = "adjudication"`, with `WI-606` depending on `WI-605`.
   Removing adjudication worktree dispatch changes how all six run. Added as
   resolution step 6, sequenced before step 3's removal.

Deferred open items: none.
