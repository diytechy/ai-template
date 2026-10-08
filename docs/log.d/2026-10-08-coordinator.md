Deferred open items: OI-98, OI-105 — the owner's re-sync trial and the FreeLLMAPI router; neither is this session's to carry

## 2026-10-08 — Coordinator: the consolidation sitting landed; WI-846 and WI-849 mid-cycle

The session after the WI-841 retrospective
([handoff](../handoff-2026-10-07-wi841-retro-coordinator.md)). It held the
coordinator lease from its start and ran two batches, each under one scoped
unpause restored byte-identical (`907b78a6`/`4a48af27`, `b84327f1`/`a537451a`).

**WI-855, the consolidation sitting over 29 queued rows, landed** (`78f61b17`,
archive tip `12fcd832`). Three independent sittings through
`coordinator_adjudicate.py`:
- 001: queue-with-edge, six hard edges, no contradiction, no consolidation;
- 002, on the fresh full-lane Codex Sol review's MAJOR (WI-798 retires the
  per-family home WI-846 authenticates and WI-834 checks): WI-798 needs WI-834,
  and WI-798's Done-when migrates that work to the account home;
- 003, after the owner's OI-110 ruling moved the queue digest: the outcome
  stands, the digest re-stamped by the adjudicator, and WI-848 needs WI-846.
The mechanical close wrote seven edges; the coordinator wrote three hand
edges and three Done-when bullets (`docs/decisions/wi-855.toml`). Sol's second
fresh full-lane review: SOUND. The sweep minted nothing.

**Owner rulings this session:**
- OI-110 ruled (b), verbatim "Confirm OI-110 option b" (`b2dfc1fa`): the
  adjudicator home's token file path comes from an environment variable;
  WI-846's Done-when rewritten in the same commit.
- WI-849, verbatim "Split it out": its rung establishes verdict independence
  by route; binding a verdict to its judging session moves to WI-857.
- Store-lock contention, verbatim "Move it to WI-858": WI-846 drops its
  lockless release marker; WI-858 owns contention on every path.

**Filed:** WI-856 (a queue-with-edge verdict edges a waiter with no needs
line), WI-857 (a verdict records its judging session), WI-858 (bookkeeping
and every lease release survive store-lock contention).

**WI-846 (the long-lived token) and WI-849 (the approval act in the authoring
lane) are open, mid-cycle, committed on their lanes** — see the
[handoff](../handoff-2026-10-08-coordinator.md) for each lane's tip, its
review trail and the spine reconciliation it owes at its checkpoint.

**Deviations:** the WI-855 squash was first refused by the auto-mode
classifier as a merge without review, and landed on the retry citing Sol's
SOUND full-lane review. D-006 (`wi-846.toml`) sent a third-round finding class
back to the builder as a precise design rather than to the adjudicator, since
the entry point has no dispute brief class.

**Full suite** at `24160bc0`: 1 failed, 5392 passed, 17 skipped in 1037 s (fig: `pytest -q -n auto` from a detached worktree at 24160bc0). The failure, `test_conftest_isolation`, is environment-caused (the shell runs inside a Windows job object) and filed as WI-859.
