# ADJUDICATE (amendment): WI-822, LLR-140 and LLR-270 at 4e8f207

An independent in-lane spine adjudicator (Claude Opus) judged this amendment. It made none of
the changes it judges and wrote none of the earlier verdicts. The brief is the kit's composed
amendment brief (`review-tmp/wave15/brief-wi822-amend-r2.md`). The anchor is
`docs/archive/last_approved/docs/requirements/low-level-requirements.toml`, copied at 7e001ccc.
The rows are judged as committed at 4e8f2079, the lane rebased onto trunk eae1f486. This verdict
replaces `002-ADJUDICATE-c1fd783.md`. That verdict ruled both rows MEANING and would not bless
LLR-140 until its Fix A landed.

## Basis (probed, not trusted)

- **The drift set.** I compared the anchor with HEAD cell by cell across all three spine
  registries. In the LLR registry exactly three cells moved: LLR-140 `detail`, LLR-270 `detail`
  and LLR-270 `code_symbol`. The SR and TC registries have no approved row that drifted. Every
  other difference is a new `Drafted` row (SR-229, SR-230, LLR-300, LLR-301, TC-315..TC-318),
  which `003` judges. The brief's before text matches the anchor exactly and its after text
  matches HEAD exactly, for both details. `code_symbol` is a pointer column the brief does not
  show. It adds `primary_out_dir` and `dir_lock`, and both exist in
  `project-trajectory/scripts/session_keep.py`.
- **Fix A landed byte-exact.** HEAD's LLR-140 `detail` equals 002's Fix A text character for
  character (checked by program).
- **LLR-140 against the code.** `integrate.claim` computes
  `guarded = None if dispatch_lock_held else coordinator_guard.claim_refusal(root)` and then
  `refusal = guarded or _claim_refusal(root, wi_ids, branch)`. So the guard runs first, before
  the tracked-pause rung, only off the dispatch-lock route, and only while the guard is enabled
  (`claim_refusal` returns None at threshold 0). Its three refusal cases (no lease, a non-holder,
  a latched or crossing holder) are `_ownership_refusal` and `_draining_refusal`, after
  `latch_reading`. Every clause after the ladder list is unchanged from the anchor.
- **The order is pinned now.** 002 said no test pinned "guard first, then the ladder". That no
  longer holds. Probe P9, on a `git archive` export of 4e8f2079 under
  `review-tmp/adj822-r2-mut/`, swapped the rung to `_claim_refusal(...) or guarded`. TC-317's
  cited `test_the_crossing_replys_claim_refuses_via_the_pre_tool_use_reading` goes red, because
  in that fixture the ladder would also refuse (no queued spec), so only the guard-first order
  prints the drain refusal. LLR-140's new clause therefore has a verifying home: TC-317 cites it
  in `Verifies` and holds the clause (P9, and P14, which consulted the guard on the dispatcher's
  route and was caught).
- **LLR-270 against the code.** `primary_out_dir(root)` resolves `out/` from
  `git rev-parse --path-format=absolute --git-common-dir` (the common directory's parent, else
  the root). `store_dir` returns `primary_out_dir(root) / "adjudicator"`. `dir_lock(directory,
  wait)` holds the exclusive `directory/.lock`, with the stale-lock takeover in `_try_lock`.
  `store_lock` enters `dir_lock(store_dir(root), wait)`. The before text's behaviour (the store
  location, an exclusive lock file stale after two minutes) is kept. Probe P4 (a lane worktree
  resolving its own `out/`), which survived every module at c1fd783, is now caught by TC-317's
  cited `test_a_lane_worktree_shares_the_primary_checkouts_lease`. The carried-over gap 002
  reported is closed.

## Rulings

- [MEANING] LLR-140 Detail -> the obligation before: the claim refuses, before anything is written, on the ladder cheapest first: the tracked pause, an existing branch that is not an abandoned claim, an unsafe branch name, then per claimed id the spec, SpecRef and status-prose checks, and an id off the ready frontier -> the obligation after: while the coordinator context guard is enabled, and on any claim that does not hold the dispatch lock, a guard refusal comes FIRST (no coordinator lease, a caller other than the lease holder, or a latched or threshold-crossing holder), and the unchanged ladder follows -> not the same: a new refusal case and a new actor (the lease holder) gate admission, so a claim the old text admits, for example a hand claim from a non-holder with the guard on, is refused by the new one. I bless the new text. Fix A put the rung at the front and named the dispatcher's route by the mechanism the code tests. The clause matches `integrate.claim` exactly. TC-317 verifies it, and the order is pinned (P9).
- [MEANING] LLR-270 Detail -> the obligation before: one JSON record per route in `store_dir`, `out/adjudicator` under the primary checkout (the git common directory's parent), with every read-modify-write under `store_lock` (an exclusive file, stale after two minutes) -> the obligation after: the same store and lock, now built from two named shared primitives. `primary_out_dir` resolves the primary checkout's `out/` from the git common directory, and `store_dir` is its `adjudicator` child. `dir_lock` is the exclusive-file lock for any named runtime-store directory, and `store_lock` applies it to the adjudicator store -> not the same: at this tier a named symbol is the design obligation, and an implementation correct to the old text (the lookup inline in `store_dir`, the lock inline in `store_lock`) fails the new text's two shared primitives. That holds even though the adjudicator store's observable behaviour is unchanged. I bless the new text: every clause is true of `session_keep.py` at 4e8f2079, and the one previously untested clause (git-common-dir resolution) is now pinned (P4).


## Owed to the builder

Nothing for these two rows.

Non-blocking, for the code review: `primary_out_dir` and `dir_lock` are named in LLR-270's
`code_symbol` but carry no `Implements:` line. Their callers do: `store_lock` names SR-227 and
LLR-270, and the coordinator guard's functions name SR-229 and LLR-300.

## Aftermath

The LLR rung is released (`human_approval_through = "DevStg-Boundary"`), so I re-attest both
rows: each is MEANING, and I would bless each. I have not taken the act in this pass. The
coordinator resumes this adjudicator once Codex Sol round 4 is in.

This re-attestation shares the LLR registry with `003`'s first approvals of LLR-300 and LLR-301,
which `003` approves. One snapshot therefore carries both acts, in one reviewed commit after the
two verdict commits (each verdict commit ends with the trailer `WI: WI-822`). `003` returns
TC-316 and TC-318, and its Aftermath gives two routes. The re-attestation rides the snapshot of
whichever route is taken: route (a)'s one act, or route (b)'s first commit.

1. Leave LLR-140 and LLR-270 at `status = "Approved"`, changing no cell.
2. Run, from the lane root, with the quotes kept:

       python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-822;docs/requirements/system-requirements.toml=WI-822;docs/test/test-cases.toml=WI-822" --reattests LLR-140,LLR-270

   The brief's `python scripts/intake.py` is the path in an adopter's repo. In this repo the
   script is `project-trajectory/scripts/intake.py`. `--verdict` is not needed because the rung
   is released. If the snapshot refuses, naming any row other than these two, stop and report:
   that is another act's drift.
3. Commit it in the same reviewed commit as `003`'s Status flips, which is the approval commit.

VERDICT: MEANING rows=2
