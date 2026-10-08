+++
id = "WI-846"
title = "The adjudicator's dedicated Claude home authenticates with a long-lived token, and an auth failure retires nothing"
workstream = "process"
sr_refs = ["SR-227"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Deliverable

A retained Claude adjudication (the loop's route, the coordinator's, or a keep-warm ping) authenticates its dedicated home with the owner's long-lived token, read at each launch from the file `AGENT_CLAUDE_TOKEN_FILE` names (OI-110 (b)) and passed as the launch's one environment credential; it is never stored, and every verbatim occurrence is kept out of argv, the captured stream, result, usage, session logs, retention records and commits (the D-004 bound; the CLI's own transcript is outside, D-002). An unset, missing, unreadable or empty token file, a competing credential name (case-insensitive on Windows) or `--bare` is refused before any lease; an authentication failure records the call, releases its lease under the store lock and leaves the session record unchanged. A retained launch is prepared once from the row its caller selected (`session_service.prepare_launch`, no registry re-read): one runner, substituted (`agent_session.substitute`) and resolved to an absolute path on the composed launch PATH, serves the version probe and the launch, and a runner that does not resolve is refused before any lease (D-008); the probe runs with the credential withheld. Rows: SR-227, LLR-270, LLR-305, TC-267, TC-268, TC-323 and TC-324 re-attested and TC-330 approved (verdicts 001 and 002, one combined sitting and its re-sit, the follow-ups answered in the lane); LLR-163's code_symbol traced. Codex 6.1 Sol: six narrow rounds, then the fresh full-lane review SOUND (`9bf77021`, at medium). Compromised-host findings dismissed under the owner's 2026-10-08 ruling (D-009). Decisions: `docs/decisions/wi-846.toml` (D-001..D-010).

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
  with the owner's long-lived token. The token is read at launch from a file
  outside the repository whose path a declared environment variable names
  (OI-110 ruled (b), 2026-10-08: nothing about the path is tracked, and an
  adopter sets its own), and passed to the CLI the way it documents for
  headless use. It is never written to a log, prompt, record or commit. An
  unset variable or a missing or unreadable token file is refused before
  launch, naming dev-setup; nothing falls back to OAuth.
- The sign-in probe reports `signed-in` only when the variable is set and
  the token file it names is present and readable (no model call); unset
  reads as not signed in. dev-setup offers the one-time `claude setup-token`
  step and tells the owner to set the variable. This is shared with WI-834's
  sign-in step (part C); whichever builds first owns it, and the other cites
  it.
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

## Adjudication follow-ups, answered in this lane

The checkpoint sitting (`docs/reviews/wi-846-adjudicator-home-long-lived-token/001-ADJUDICATE-6553682.md`) would bless TC-268, TC-323 and TC-324, did not bless SR-227, LLR-270, LLR-305 or TC-267, and returned TC-330, with three drafted follow-ups. Under the owner's ruling of 2026-10-06 (a return is answered in the lane, not minted), all three are answered here as row text, with no behaviour change:

- SR-227 states the ordinary dedicated-home refusal's closed conditions again, in both its Requirement and its AcceptanceCriteria: where no long-lived credential applies, a reading other than signed in refuses either retained route before any launch, home creation, lease or retention-state write, names the setup action, and neither signs in automatically nor falls back.
- LLR-270, LLR-305 and TC-267 state their rules in full, with no "as before": the lease, governing-input, drain, lineage, adapter, home, cap, bookkeeping and keep-warm rules; the documented probe pairs and the no-create home resolution; and the CODEX_HOME occupancy assertions. keep_abandon's tombstone protocol and its lock-exclusion and no-leftover-file assertions are restored to LLR-270 and TC-267; only new store-lock contention work is WI-858's (`docs/decisions/wi-846.toml` D-010).
- TC-330's Expected is bounded to the sinks the act redacts, excluding the dedicated home's own CLI transcript and escaped, encoded and line-split forms (D-002, D-004), and its Method names its tests; `test_the_token_is_read_at_launch_and_never_logged` asserts the canary's absence from the launch argv and the telemetry commit.

The re-sit judges SR-227, LLR-270, LLR-305 and TC-267 to TC-324 again, and TC-330 for first approval.
