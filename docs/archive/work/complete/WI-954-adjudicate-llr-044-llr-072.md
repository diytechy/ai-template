+++
id = "WI-954"
title = "adjudicate: LLR-044, LLR-072, LLR-266, LLR-267, LLR-268, LLR-270, LLR-305, LLR-306, LLR-321, TC-267, TC-321, TC-323, TC-324, TC-330, TC-344 - approved/routed cell(s) amended on merged trunk 9c49715..2c8ff80 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-044", "LLR-072", "LLR-266", "LLR-267", "LLR-268", "LLR-270", "LLR-305", "LLR-306", "LLR-321", "TC-267", "TC-321", "TC-323", "TC-324", "TC-330", "TC-344"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-798's in-lane sitting
`docs/reviews/wi-798/017-ADJUDICATE-00a353f.md` blessed all fifteen rows as
MEANING+BLESS, and the lane's act turn took act seqs 141 and 142. At the
landing 2c8ff804e the low-level and test registries are byte-equal to their
approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-044 `Detail`: 'Parses pair rows and enable tokens; resolves versions; merges Env; selects by tier, family, cooldown, and order with le…' -> 'Parses pair rows and enable tokens; resolves versions; merges Env; selects by tier, family, cooldown, and order with le…'
- LLR-072 `Detail`: 'Selects two fresh planner sessions across families where possible and applies the bounded nonresponse fallback with rea…' -> 'Selects two fresh planner sessions across families where possible and applies the bounded nonresponse fallback with rea…'
- LLR-266 `Detail`: 'adapter_for(argv) picks the adapter by the basename prefix of the executable argv launches (claude, codex, opencode, ca…' -> 'adapter_for(argv) picks the adapter by the basename prefix of the executable argv launches (claude, codex, opencode, ca…'
- LLR-267 `Detail`: "context(stream, env, session_id) returns (session_id, used, window, pct) for the session's final model request, each fi…" -> "context(stream, env, session_id) returns (session_id, used, window, pct) for the session's final model request, each fi…"
- LLR-268 `Detail`: 'usage(stream) returns one dict with exactly the USAGE_KEYS columns for every runner: cli, semconv (OTEL_SEMCONV, open-t…' -> 'usage(stream) returns one dict with exactly the USAGE_KEYS columns for every runner: cli, semconv (OTEL_SEMCONV, open-t…'
- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- LLR-270 `Rationale`: 'Retention is one more thing a call does, not a second launch path, so resume, occupancy, reset and keep-warm all go thr…' -> 'Retention is one more thing a call does, not a second launch path, so resume, occupancy, reset and keep-warm all go thr…'
- LLR-305 `Detail`: 'REQUEST. AdjudicationRequest carries root, brief, the selected route row, work item, role, prompt-template overrides an…' -> 'REQUEST. AdjudicationRequest carries root, brief, the selected route row, work item, role, prompt-template overrides an…'
- LLR-305 `Rationale`: 'A coordinator route that retained independently would duplicate the request composition, state path and dedicated-home …' -> 'A coordinator route that retained independently would duplicate the request composition, state path and account-home po…'
- LLR-305 `Title`: 'Coordinator adjudication shares the keep request and refuses an unsigned retained home' -> 'Coordinator adjudication shares the keep request and refuses an unsigned account'
- LLR-306 `Detail`: 'ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and otherwise refuses before launch through IF-284…' -> 'ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and otherwise refuses before launch through IF-284…'
- LLR-321 `Detail`: 'The workstation report omits the retained-adjudicator sign-in item while retention is off; otherwise it reports signed-…' -> 'The workstation report omits the retained-adjudicator sign-in item while retention is off; otherwise it reports signed-…'
- TC-267 `Method`: 'With the dial on, over the recorded fixtures (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert…' -> 'With the dial on, over the recorded fixtures (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert…'
- TC-330 `Expected`: 'Satisfies LLR-305 (parent SR-227): verbatim credential occurrences are absent from argv, the captured stream, result, u…' -> 'Satisfies LLR-305 (parent SR-227): verbatim credential occurrences are absent from argv, the captured stream, result, u…'
- TC-321 `Expected`: 'Only a claimed lane worktree launches and writes one attributed session log per call; a second coordinator-route adjudi…' -> 'Only a claimed lane worktree launches and writes one attributed session log per call; a second coordinator-route adjudi…'
- TC-323 `Expected`: 'The dedicated-home sign-in probe has the three declared readings without making a model call or creating an absent home.' -> 'The account-home sign-in probe has the three declared readings without making a model call or creating an absent home.'
- TC-323 `Method`: 'Run test_the_probe_reports_signed_in_missing_or_unknown, test_a_probe_that_fails_or_times_out_reports_unknown, test_the…' -> 'Run test_the_probe_reports_signed_in_missing_or_unknown, test_a_probe_that_fails_or_times_out_reports_unknown, test_the…'
- TC-324 `Expected`: 'Only a retained launch for a family with a dedicated home requires a readable sign-in; missing or unknown refuses befor…' -> 'A retained token account requires its own readable token file and a retained login account requires its own documented …'
- TC-324 `Method`: 'Run test_the_coordinator_route_refuses_a_retained_launch_not_signed_in, test_the_loop_route_refuses_a_retained_launch_n…' -> 'Run test_the_coordinator_route_refuses_a_retained_launch_not_signed_in, test_the_loop_route_refuses_a_retained_launch_n…'
- TC-344 `Expected`: 'The sign-in item is off when retention is off, otherwise reports signed-in, missing, or unknown accurately while the re…' -> 'The sign-in item is off when retention is off; otherwise it reports a readable token or documented account-home login a…'
- TC-344 `Method`: 'Run workstation reporting with retention off, and with readable, missing, and unreadable retained sign-in inputs on bot…' -> 'Run workstation reporting with retention off; a token account with readable, missing, and unreadable inputs; a login ac…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
