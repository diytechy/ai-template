## 2026-10-20 — WI-798: account tables and per-account homes (headless leg 04)

### The lane, from its rebase to its landing

Claimed attended on 2026-10-11 and continued in headless leg 04 of loop
session `20261019T185432Z-8e4f05`. The lane was rebased 245 commits onto
trunk `9c4971543` (decisions D-010 to D-013 in `docs/decisions/wi-798.toml`:
the act turn runs under the declared account; session_keep defers its route
import so the guard's no-op hook stays cheap). Its count started at zero
under the review-churn shape: counted rounds 1 to 3 (reviews 005 to 010,
Codex Sol medium and a Claude Opus high stand-in), the cap's dispute sitting
011 (A009-F1 FIX: the OpenCode base kept the loop marker), the checkpoint
(Terra's reconcile; sittings 012, 013 and 014), the gate in convergence stance
(reviews 015 and 016, no BLOCKER or MAJOR), then one whole-set sitting, 017,
whose act re-attested 15 rows and approved LLR-336 and TC-361..366.

### Owner-dependent completion: the lane's evidence

- **The no-spend empty-home half of the Claude isolation check.** With real
  claude 2.1.296 on this workstation, `claude auth status` under an empty
  `CLAUDE_CONFIG_DIR` printed `"loggedIn": false` at exit 1, the kit's
  `signin_status` read that home and an absent home `missing`, and the
  ambient login read `signed-in` (reproduced independently by the gate's
  REVIEW-B, `docs/reviews/wi-798/016-REVIEW-B-f5b3240.md`; first observed
  2026-10-11, as `session_service._claude_signin`'s docstring records).
- **The adjudicator on its declared account.** `coordinator_adjudicate.py
  signin --retained`, run from the lane with the token variable set, read:

      signin [ADJUDICATOR] token: signed-in
      signin [ADJUDICATOR]: token_file_variable AGENT_CLAUDE_TOKEN_FILE

  and the lane's sittings 011 to 017 and the act turn launched on the
  qualified default entry `ANTHROPIC-OPUS-STRONG@ADJUDICATOR`, resuming one
  retained session across them.
- **The two-login half** is WI-908's, held by OI-114.

### Notes

- The smoke tier read over its 60 s budget throughout the leg on a loaded
  box (lane 67.6 to 139.5 s; trunk's own tip 170.1 s in one adjacent run);
  the landing reads beside its parent's (owner, 2026-10-17).
- A REVIEW-B probe in round 3 left a stray file (holding only a scratch
  path) in the primary checkout's root through a mis-aimed redirect from its
  default working directory; the coordinator removed it before the squash.
