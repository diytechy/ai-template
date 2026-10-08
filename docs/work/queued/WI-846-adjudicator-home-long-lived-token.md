+++
id = "WI-846"
title = "The adjudicator's dedicated Claude home authenticates with a long-lived token, and an auth failure retires nothing"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/log.d/2026-10-06-wave18-coordinator.md"
needs = ["OI-110"]
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Context

Filed by the wave-18 coordinator on 2026-10-07 at the owner's ruling. The
retained adjudicator runs headless `claude -p` under its own
`CLAUDE_CONFIG_DIR` (`out/adjudicator/home/anthropic`). Its OAuth sign-in
failed to refresh twice: at about 21:17 on 2026-10-06, and again at 13:37 on
2026-10-07 after a clean `/login`. Each failure was
`Failed to refresh OAuth token` and left `.oauth_refresh.lock` behind, with
no other process using that home. Each time the owner had to sign in by hand,
which defeats an unattended loop. Three gaps showed:

- the sign-in probe reads `signed-in` for a home whose token cannot refresh;
- the first failed call retired the retained session as unusable;
- how the home was provisioned is not recorded.

The owner ran `claude setup-token` (a long-lived token for headless use) and
holds the token in a file outside the repository. The coordinator has its path
and must never read the file's contents into a log, prompt or commit.

## Done-when

- A retained Claude launch on either route authenticates the dedicated home
  with the owner's long-lived token. The token is read at launch from a
  declared location outside the repository (a dial naming the file; never its
  value) and passed to the CLI the way it documents for headless use. It is
  never written to a log, prompt, record or commit. A missing or unreadable
  token file is refused before launch, naming dev-setup; nothing falls back to
  OAuth.
- The sign-in probe reports `signed-in` only when the configured token is
  present and readable (no model call), and dev-setup offers the one-time
  `claude setup-token` step. This is shared with WI-834's sign-in step (part
  C); whichever builds first owns it, and the other cites it.
- An authentication failure on a launched call records the call failed and
  leaves the retained session's record as it was; it never retires the
  session as unusable.
- Tests: the token path is read, the token is never logged (a canary value
  absent from every log and record), a missing token refuses, and an
  auth-failure call keeps the session.
- SR-227's approved clause "retire it at once when a call on it fails" is
  amended to exclude an authentication failure, and its rows pass in-lane
  adjudication.
- The sign-in guidance in the coordinator's procedure skill (`session-protocol`
  today, `coordinator-cycle` once it lands) describes the token step, not an
  interactive sign-in.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
