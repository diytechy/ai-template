+++
id = "WI-506"
title = "Session continuity: the template review, the resume-pack ritual, and the investigated context-restart trigger (OI-57 ruled (b), 2026-08-22)"
specref = ""
workstream = "process"
sr_refs = ["SR-177"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

**The review** (twelve templates read against this week's actual grinds,
docs/log.d/2026-08-23-wi506-session-continuity.md §Review): the split is by
design, not drift — adjudicator briefs (`adjudicate-*`) hand a narrow,
single-verdict evidentiary snapshot with the judged party's own
self-assessment structurally excluded, while the worker brief hands a
cumulative, self-referential lane-state picture (predecessor deliverables,
registry context joins, the branch's own diff, any rework finding) recomputed
FRESH at every launch. The real drift found: `worker.template.md` gave the
session no instruction about WHEN to make that state resumable — and
`docs/log.d/2026-08-21-wi498-stage-unification.md` records the cost: two
sittings interrupted before committing left ~121 modified/renamed files and a
section already claiming LANDED with no gates block, requiring a whole third
"recovery" sitting to reconcile.

**The resume-pack ritual** (SR-060/WI-181's worker brief, `prompts/worker.template.md`):
gains one Rules bullet — the standing-state discipline — instructing the
worker to start its log.d fragment and land the spec's own
Context/Deliverable edits BEFORE heavy verification, refining both as the
session continues rather than writing them once at the end. No loop-side
change is needed: `agent_loop.worker_prompt`'s `diff_block` already
recomputes the branch's own accepted-not-yet-reviewed commits fresh at every
launch (confirmed by the existing `test_worker_resume_with_complete_evidence_spends_no_session`),
so a session killed mid-verification already hands the next launch its own
diff — the only real gap was behavioral, not mechanical, and is now closed by
prose pinned by `tests/test_prompts.py::test_the_worker_brief_carries_the_standing_state_ritual`.

**The trigger, investigated** (OI-57 (c)): no provider this kit routes
through exposes a LIVE, mid-session context-percentage a running session
could read and act on. ANTHROPIC (`claude -p --output-format stream-json`)
is the only family whose CLI reports token/cache usage at all
(`agent_loop.py`'s `usage = data.get("usage")` block, ~L2621), but that
report arrives only in the final `type: result` event AFTER the process has
already exited — too late to inform a still-running session's own decision.
OPENAI (`codex exec`, captured via `-o/--output-last-message`) and OPENCODE
(`opencode run`, plain stdout) report no token/usage accounting at all, even
post-hoc. Verdict: (c)'s proactive trigger is not implementable on real
context accounting today, on any routed provider — ruling (b) without (c) is
confirmed rather than assumed, and no heuristic was built.

**Fold-in A** — `LLR-196` + `TC-191` mint `Drafted` against `SR-177`: the
per-session telemetry columns (`wall-secs`/`api-secs`/`turns`/`tokens`/
`cache-read`/`cache-create`, `agent_common.regenerate_index`/`per_turn_pace`/
`per_turn_context`) are real, shipped and tested, but nothing GROUPS them by
run or lane — the utilisation report itself (lanes configured vs occupied,
work items per wall-hour) remains the stated, undischarged build gap, per the
row's own honest-debt framing (the `LLR-193`/`LLR-194` pattern).

**Fold-in B** — `TC-192` mints `Drafted`, verifying `SR-146` + `LLR-164`
(the generated prompt catalogue + freshness gate). Investigation found
`LLR-164`'s existing `test_refs = "TC-157"` cell was WRONG — `TC-157`
verifies `SR-146`/`LLR-162`/`LLR-163`, never `LLR-164` — which is why the row
showed as orphaned despite a filled cell; `test_refs` is corrected to
`TC-192`, the real citation.

Watermarks `LLR` 195 -> 196, `TC` 190 -> 192, via `trace.py --bump-ids`.
Orphans: before **7**, after **4** (`SR-163`, `SR-181` remain, owned by other
queued rows). `integrity=0` throughout. Gates and full pytest totals are in
the log fragment.

## Context

Executes OI-57 (b), with (c)'s trigger investigated in the same row:

1. **The review**: the twelve templates under project-trajectory/prompts/
   read side by side for the owner's split question — what the ADJUDICATOR
   is told versus what the WORKER is told about the same lane state —
   against the sessions the recent grinds actually ran; drift between what
   templates promise and what workers do filed as findings.
2. **The resume-pack ritual**: the worker template gains a standing-state
   contract — the fragment section + lane-spec Context written BEFORE
   heavy verification, so an interruption at any point leaves a resumable
   record (the pattern all seven of this week's successful interruption
   recoveries used) — and the loop relaunches a died session from that
   record.
3. **The trigger, investigated not assumed**: adopt a proactive ~66%-
   context restart ONLY where a provider exposes real context accounting;
   never the guesswork heuristic alone. Record per-provider findings
   either way.

Adopter-facing template changes carry RESYNC entries; the prompt catalog
regenerates.

**Orphan fold-in (owner-directed 2026-08-22):** this row's telemetry
investigation DISCHARGES the decomposition debt on `SR-177` (fan-out
utilisation reported from the run's own telemetry — mint its LLR/TC while
in that surface), and the template review mints the missing TC for
`LLR-164` (the generated prompt catalogue + freshness gate), which this
row regenerates anyway.
