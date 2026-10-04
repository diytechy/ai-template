+++
id = "WI-788"
title = "Session families with reset terms, a glossary, per-route provider homes, and new routes"
workstream = "process"
specref = "docs/agents.toml"
sr_refs = ["SR-222", "SR-227", "SR-154", "SR-155"]
needs = ["WI-787"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the wave-9 coordinator on 2026-10-03, at the owner's direction.
The owner's words:

> "there is likely a reason to set this dynamically in case multiple codex account
> are being used. In fact this might be an issue with claude as well where a similar
> instance might need to be able to be passed accordingly. This probably needs to be
> another WI both to address openai, add in untested support for supergrok (or if
> there is a free plan I can prepare for that formally here), add in support for
> google cli (which I have note checked yet), and add in support for FreeAI through
> opencode (Which needs some method of connfiguraiton / routing, of which I'm not sure
> of the best way to setup)."

What exists today (checked 2026-10-03):

- **Per-route homes are already ruled and already expressible.**
  - OI-69 (e1), ruled 2026-08-30: "dedicated config homes for the orchestrator's
    CLIs".
  - A route row's `env` cell is merged over the launch environment, and
    `agent_loop.py` names exactly this use: "a router (ANTHROPIC_BASE_URL), a second
    account (CLAUDE_CONFIG_DIR / CODEX_HOME), or an API key (GEMINI_API_KEY) is
    selected declaratively".
  - No row in this repo's `docs/agents.toml` sets a home. The ANTHROPIC rows set only
    `CLAUDE_CODE_EFFORT_LEVEL`; the OPENAI rows set nothing.
  - Whether every adapter reads the home it was launched under is unverified, except
    codex: WI-787 adds the default-home fallback, and an explicit `CODEX_HOME` is
    already read.
- **Adapters:** `session_adapters.py` has Plain, Claude, Codex and Opencode adapters.
  There is no Google adapter.
- **Routes:**
  - Grok is reachable today only through opencode (`OPENCODE-GROK`,
    `opencode-go/grok-4.6`).
  - No `gemini` or `grok` CLI is installed on this box. `opencode` is.
  - FreeAI has no route.
- **Unknown, to be researched rather than assumed:**
  - whether SuperGrok ships its own CLI;
  - whether xAI or FreeAI offer a free plan;
  - which Google CLI and auth path fit a headless route;
  - how opencode selects a FreeAI provider.

## Done-when

Two halves. The second is built only after the owner reviews the first.

1. **Research and design note (owner checkpoint).** Write a short note under
   `docs/plans/`, citing sources and probes, that settles:
   - per provider (OpenAI/codex, Anthropic/claude, xAI/SuperGrok, Google, FreeAI
     through opencode): the headless CLI and its version, the auth and account model,
     the config-home variable that isolates an account, whether a free plan exists and
     its limits, and the stream format the adapter must parse for usage, occupancy and
     session id;
   - how one route selects one account: the `env` cell, a per-account row, or
     something else, and how a second account of the same provider is declared without
     duplicating rows;
   - opencode provider configuration for FreeAI: where its config lives, how a route
     names the provider and model, and how that config is kept per-route and out of the
     tracked tree when it holds secrets;
   - for each new route, tested vs untested. The owner asked for SuperGrok support
     even if untested; an untested route must be visibly so in `docs/agents.toml` and
     never enabled by default;
   - spine impact: which SRs and LLRs cover routes and adapters, and what is amended or
     added.

   STOP at the note. The owner rules before any build.

   OI-101 (ruled 2026-10-03) settles what was unknown. The note must also:
   - state the spine-authoring approval act as the adjudicator's final pass, valid
     only if that pass changes nothing; any change goes back to the adjudication
     reviewer, and the cycle is bounded at 3 rounds (OI-101 Q1);
   - apply risk 6 on lane and trunk: no commit changes spine text together with a
     snapshot update, which retires "amend-plus-flip is approval" everywhere
     (OI-101 Q2);
   - route Grok and FreeAI through OpenCode, and add no separate xAI or SuperGrok CLI
     route (OI-101 Q3). "FreeAI" is **FreeLLMAPI** (owner, 2026-10-03: "really just
     FreeLLMAPI, and it can be accessed like Grok through OpenCode CLI as an
     endpoint"). It is not OpenCode's own free `opencode/*-free` models, as the OI-101
     record first read it. The note settles:
     - how OpenCode declares FreeLLMAPI as a custom endpoint provider;
     - how a route row names that provider and model;
     - how the endpoint's URL and key stay per route and out of the tracked tree;
     - whether OpenCode's free models are worth a separate untested row;
   - live-probe OpenCode only (authorized). Google's CLI is researched from its
     documentation and its route is marked untested (OI-101 Q4);
   - put the glossary in a kit-shipped `project-trajectory/GLOSSARY.md`, linked from
     PROCESS.md (OI-101 Q5);
   - build on the S11 plan's §6 as ruled, not as open questions (OI-101 Q6).
   - end with a **slice plan**: the build divided into successor rows, each with its own
     lane, Done-when, review and test bar, ordered by `needs` edges (see "Scope widened
     2026-10-04");
   - cover every later section of this spec: each "Scope widened" section, each set of
     owner directions and rulings, LS1 to LS10, U1, and amendments B1 to B12. It is
     written as B12's four chapters, with the amend/preserve/retire matrix and the
     dependency graph. These sections sit outside this Done-when heading only
     because they accreted later; they bind it (B12);
   - wait on OI-103 (Q1 to Q6). Each ruling is written into this spec, citing
     OI-103, before the note is drafted.
2. **Build what the owner approves, as successor rows.** At the checkpoint the
   coordinator files the slice plan's rows on trunk, and WI-788 closes on the approved
   note. The rows together deliver:
   - Route rows in `docs/agents.toml`, and in the shipped template where adopters need
     them.
   - The Google adapter, and any opencode provider handling.
   - The per-route home wiring this repo uses for its own accounts.
   - Spine rows through in-lane adjudication.
   - Tests against recorded fixtures. A live recording only where the owner authorizes
     the run.
   - A RESYNC_PACK entry.

   Nothing forces an adopter to install a new CLI.

## Scope widened 2026-10-04 (owner): plan kinds, the dual-plan regression, and a slice plan

The owner asked whether the plan / dual-plan method had been removed, and what
research says about planning before the build. The coordinator recommended designing
the plan kinds inside this item, because they overlap the single labelled entry
point, and building through successor slices. The owner: "That sounds fine, though
it sounds like your preliminary research shapes it well, but if you think there is
more to uncover feel free to salt that into the plan as you see appropriate."

What was found (record:
[plans/2026-10-04-planning-before-build-research.md](../../plans/2026-10-04-planning-before-build-research.md)):
- **Dual-plan decomposition** (SN-024, SR-155) is an opt-in decomposition layer:
  rival breakdowns of a goal, cross-critique, two swapped arbiter runs, then the
  winner's rows are filed. It is not a per-item plan-before-build step. The builder
  plans inside its own session.
- **Its automatic start was lost, not ruled away.**
  - WI-199 and WI-209 (2026-07-17) made the dispatcher run the round for a
    `planmode = "dual"` row.
  - The old dispatcher's deletion (`31ad569d`, concurrency-restructure Phase 5,
    2026-07-29) took that start with it, and `dispatch.py` never re-implemented it.
  - Today a dual row is claimed, refused at preflight
    (`agent_loop.py:1317-1329`), parked and resumed in a loop: WI-209's "quiet park"
    is back.
  - No live row is marked dual. Under the no-fallback rule (risk 7), restoring the
    pickup is the fix, and no interim guard is added.
- **The preliminary research:**
  - A plan helps on non-trivial, multi-file or ambiguous work.
  - A bad plan is worse than none.
  - Planning only on demand is far cheaper than planning every time.
  - Same-model debate adds cost for little gain, and different families are what
    help.
  - Dual plans plus an arbiter have no direct coding evidence. An arbiter must be
    grounded in executable or testable criteria.

**The owner's evidence on the arbiter (2026-10-04):** "even before this the arbiter
never was actually needed, the cross-critique always resulted in both drafters
selecting the same plan at the end." The owner also recalls earlier notes on how the
arbiter could judge the plan itself. The coordinator did not find them in this repo;
they may live downstream. What this repo records:
- one round, DP-001 (2026-07-16,
  [verdict](../../archive/plans/DP-001-dual-plan-loop-wiring/verdict.md));
- each cross-critique raised one finding;
- both position-swapped arbiter runs selected the same plan (`plan-B-rev`), with
  nothing ported.

So the arbiter added no information there. The record does not capture the drafters
choosing for themselves.

Added to half 1 (the design note):
- **Is the arbiter a standing step?** On the owner's evidence it may not be. Options
  for the note to weigh:
  - (a) after cross-critique and revision, each drafter selects; agreement adopts the
    plan, and disagreement goes to the owner;
  - (b) as (a), but disagreement goes to an arbiter;
  - (c) one plan judged by an independent session, so that the arbiter's role
    becomes judging a single plan against testable criteria, with the competing
    pair kept for high-risk decisions.

  Under risk 7, whichever is chosen is the one path, not a fallback.
- **Plan kinds through the one entry point:** plan, plan-critique and arbitrate, with
  their families, independence (planners cross-family; the arbiter never a planner's
  session) and reset terms. `plan_runner`'s own route drawing stops being a bypass.
- **Restore the dual-plan pickup:** the dispatcher admits a `planmode = "dual"` row
  and runs the round instead of letting the worker refuse it (WI-209's behaviour on
  today's dispatcher), with tests for admit, round, filed children and page.
- **Decide whether a per-item planning step exists**, and when:
  - never;
  - by declaration (for example `planmode = "single"` or by BuildTier);
  - on demand after a failed attempt (for example on the first REVIEW-A
    CHANGES-REQUESTED, ahead of the existing swap, tier-up, page ladder).

  State each option's cost.

To uncover before the note recommends (the research left these open):
- **This repo's own baseline**, measured from what is already recorded, before any
  planning step is proposed:
  - review rounds per row;
  - CHANGES-REQUESTED rates by BuildTier;
  - handback and partial-close rates;
  - tokens per row (session logs' `gen_ai.usage.*`, review scoreboards, handback
    reports).

  A planning step must name the metric it is expected to move.
- **How often drafters converge:** count, across every recorded round (this repo's
  DP-001, and downstream repos' rounds where their records are available), how
  often both drafters would select the same revised plan and how often an arbiter
  changed the outcome. This tests the owner's observation before the arbiter is
  dropped or kept.
- **The cost of the dual-plan round on a real decomposition:** sessions, tokens and
  wall time from its session logs. Re-read WI-199's and WI-209's records and any
  `docs/plans/DP-*` artifacts for evidence of what it produced.
- **What the arbiter checks against:** whether the existing coverage pre-pass (a
  script) can be extended so that the arbiter judges executable criteria, such as
  Done-when coverage and the TC/SR coverage diff, rather than prose persuasiveness.
- **Replanning:** whether a review's findings should reopen the plan rather than only
  the build, against plan drift.
- **Read the component's knowledge packs first:** `docs/knowledge/agent-routing`,
  `docs/knowledge/effort-tiering` and `docs/knowledge/prompt-image-token-efficiency`
  (CMP-008). They carry the routing, tier and token evidence already collected.
- **Verify the research's weakest links** before relying on them: read the 2026
  SWE-agent planning paper (arXiv 2604.12147) in full, not just its abstract, and
  check the AdaCoder cost figures.

The slice plan (half 1's last output; the note may reorder it, and slice 2 is the
dependency the others share):
1. The glossary and PROCESS.md wording (docs only; it settles the vocabulary).
2. The labelled entry point and the one session store, carrying today's kinds.
3. Plan kinds through the entry point: the restored dual-plan pickup, and any
   per-item planning step the note recommends.
4. Provider routes and homes: FreeLLMAPI and Grok through OpenCode, Google untested,
   per-route homes.
5. The spine-authoring flow and the lane-and-trunk text-then-act commit split.
6. The RESYNC entry, which is the migration.

## Scope widened 2026-10-03 (owner): session families, reset terms, a glossary, and spine authoring

The owner's words, in order:

> "I do not want to maintain an adjudicator vs a retained adjudicator. There might
> just need to be a glossary.md referenced by process.md. Adjudication must be
> performed by an adjudicator, which is a session that is retained by default until
> reset conditions are met at which point it should be reinitialized (The reset terms
> must be defined, which may include resetting every time - resulting in equivalent
> behavior today), similar sessions I would expect to hold similar retention
> structures ([plan and build],[review and judge]). I would expect a similar call
> method ... another function either continues a session (retained), or determines
> it's reset condition is met and initializes a new session with the appropriate
> model along with the expected prompt."

> "judgements and reviews should always be independent. The other item I missed is
> probably related to spine authoring and author reviews ... Perhaps in those cases
> the adjudicator should draft the authoring, and the author review can update the
> same spine text, followed by one more pass from the adjudicator. That way the
> adjudicator maintains the full scope spine / vision, but a dedicated retained
> reviewer is able to run / act as a second check. This probably just needs to be the
> adjudication reviewer."

How it compares with the code (checked 2026-10-03):

- **Already built.**
  - One call path for every role (`session_service.call`; S7).
  - A resume-or-mint decision (`plan_keep` -> `session_keep.keep_for`, per-route lease).
  - Declared drain and retire rules (`drain_reason`, `_before_launch`): crest of
    occupancy over the dial, a governing-template change or a CLI version change; an
    optional same-artifact guard; retire at a clear point when no open chain remains.
  - Keep-warm.
  - `context_reset_pct = 0` is exactly "reset every time".
- **The gaps.**
  - Retention ships OFF.
  - It covers only `role == "ADJUDICATE"` for `retain_for` briefs (`disposition`,
    `amendment`, `red-tc`).
  - It is keyed per route, while model choice happens before the service, in
    `agent_loop`'s router.
  - It has no notion of a session family.
  - The coordinator's independent adjudicator (Agent-tool subagents) bypasses the
    service entirely: no routing, no session log, no retention.
- **Rulings this touches; the design note must state each change explicitly.**
  - S10 (DECIDED 2026-09-23): "the adjudicator's lands; builder retention a separate
    ruled experiment; reviewers never". A retained adjudication reviewer narrows
    "reviewers never". The coordinator's reading of "independent": it never reviews
    its own work, and it is always a different session, and preferably family, from
    the adjudicator it checks.
  - OI-69: turning the dial on is the owner's act. "Retained by default" turns it.
  - The amendment brief: a judge never amends the row it judges. Under the proposed
    spine-authoring flow, the adjudicator drafts, the adjudication reviewer edits, and
    the adjudicator makes a final pass. The design must say which act carries
    approval, and why the reviewer's independent edit keeps it from being
    self-approval.

Added to Done-when half 1 (the design note, owner checkpoint):

- `project-trajectory/GLOSSARY.md` (kit-shipped; OI-101 Q5), referenced from PROCESS.md, with one term per concept:
  - adjudicator (a role performed by a session, retained under declared reset terms);
  - session family;
  - reset terms;
  - adjudication reviewer;
  - reviewer;
  - judge (an observation re-judge);
  - arbiter;
  - independent adjudicator (the coordinator's hand role).

  It retires the "adjudicator vs retained adjudicator" split.
- Session families and their declared reset terms: [plan and build], [adjudicate],
  [adjudication review], [review], [judge]. Each says whether it is retained, its
  reset terms ("every call" is one valid setting), and its independence rule (a
  review or judgement never runs in a session that authored what it judges).
- The one call method: continue a retained session, or, when its reset terms are met,
  initialize a new one with the routed model and the expected prompt. Where today's
  router-before-service split needs to move, say so.
- The spine-authoring flow above, as an option with its approval act stated, against
  today's builder-authors / adjudicator-approves split and the S11 in-lane plan.
- The proposed defaults, each named as a change to a ruling where it is one.

## Owner direction on the gaps (2026-10-03, second pass)

1. **Retention defaults.** "This repo retention does not matter because the
   adjudicator typically runs in the visual code or other development session
   environment, but downstream adopters (resync note) should turn on retained
   adjudication. Retained builders can likely stay off but the capability should be
   built but defaults to always reset."
   - So the shipped template defaults to retained adjudication, and the RESYNC_PACK
     entry tells adopters.
   - Builder retention is built, with "reset every call" as its shipped default.
   - This repo's own dial may stay as it is.
2. **Why only some adjudication kinds?** Checked: it is drift, not a decision.
   `retain_for = ["disposition", "amendment", "red-tc"]` was written on 2026-08-30
   (OI-69 filing, `232018f2`), when those were the adjudication kinds. The
   `first-approval` brief came on 2026-09-01 (WI-572), `consolidate` on 2026-09-04,
   and `rejudge` later. None was ever added. The design states the rule per brief
   kind; any exclusion keeps a reason.
3. **One labelled entry point** (owner, gaps 3 and 4): "Each LLM call should not have
   to know it's family ... a single function that labels what is getting asked
   (builder / reviewer / judgement / authoring / authoring review / perhaps multiple).
   Then that function can do the reset determination, can lock the adjudicator (if
   it's in use from another lane), and can route to other models depending on
   availability and desired usage ratio of models."

   Today these parts exist but are spread across modules:
   - **The label:** `agent_loop` `pick_phase` (BUILD, REVIEW-A/B, CRITIQUE,
     DESIGN-CHECK, ADJUDICATE).
   - **Tier:** `agent_brief.phase_tier` plus the row's BuildTier pin.
   - **Family exclusion:** `agent_loop` `route_intent`, keyed on the loop's memory of
     the last implementer family.
   - **Model choice:** `agent_route.select`: tier, heterogeneity, cooldown for
     availability, per-phase weights in `docs/agents-enabled` for the usage ratio,
     and prefer-map.
   - **The prompt:** `agent_brief.compose_session_prompt` and
     `agent_loop.session_body`.
   - **Reset and lock:** `session_service.plan_keep` -> `session_keep.keep_for`, with
     a per-route lease.
   - **Launch and record:** `session_service.act`, `.record` and `.call`.
   - **Composition:** `agent_loop` composes these steps itself (around
     `agent_loop.py:2580-2850`).
   - **Bypasses:** `plan_runner` calls the service with a fixed template; the
     coordinator's hand path bypasses everything.

   The design proposes the single labelled entry: `ask(kind, ...)` or similar, with
   kinds such as build, review, judge, author and author-review. It owns the label to
   tier, family-exclusion, availability and ratio routing, reset or continue, and
   lock. A caller then never names a family, model or route.
   - The family exclusion must come from the work being judged (for example the
     lane's commit authorship or recorded session logs), not from loop memory: the
     2026-10-03 WI-688 judge drew the builder's family because the build ran outside
     the loop.
   - It also states how the coordinator's hand sittings can call the same entry, so
     the independent adjudicator stops being a bypass.

## Owner rulings on the design risks (2026-10-03)

The coordinator raised nine risks of one labelled entry point. The owner answered
each, and the design note follows these answers.

1. **One session store absorbs session_keep's.** One file records each retained
   session's id per role and per route, for example the main adjudicator, and each
   builder session with its route such as `agent.ANTHROPIC-OPUS-STRONG`.
   - Coordinator notes: today's store is one JSON per route under the untracked
     `out/adjudicator/`, behind a store lock. Session ids are machine-local, so the
     file belongs untracked, not at the tracked root, or clones and lanes would carry
     stale ids and conflict.
   - TOML is readable through stdlib, and the kit has its own writer.
2. **Builder family comes from what is already recorded; nothing new is built.**
   Each kit session log already commits `role`, `provider`, `roster-row` and the
   `commits` range (e.g. `docs/iteration/wi-688-001-*.log`).
   - The change: read the lane's BUILD-role logs over `base..HEAD` instead of
     `route_intent`'s in-memory `last_impl_family`.
   - What the logs cannot cover is work run outside the service: the hand path,
     closed by 8.
3. **Retention has priority over the usage ratio.** A retained session keeps its
   route until reset, and the ratio applies at (re)initialization. The documented
   assumption: the ratios are made up over time.
4. **A family that reports no occupancy declares fallback reset terms.**
   - Claude does report occupancy: its stream-json `result.modelUsage.<model>.contextWindow`
     plus the last request's usage. The live fixture
     `tests/golden/sessions/claude-stream-json.jsonl` (claude-code 2.1.266) gives
     48,267 / 1,000,000 = 5% through `ClaudeAdapter.context`.
   - Codex reports it since WI-787.
   - opencode reports no window.
5. **Lock fallback.** A caller waits about 20 minutes for the retained adjudicator's
   lease (today `lease_wait = 120` s), then runs a fresh session that does NOT replace
   the retained one. `keep_for` already returns None rather than re-minting.
6. **Mechanize the self-approval guard.** In a lane, no commit may carry a spine-text
   change together with a snapshot update. So text is committed, and reviewed, before
   any act re-anchors it.
   - This replaces the current allowance "amend-plus-flip is approval" in the snapshot
     refusal's own message. The owner notes that allowance may need removing on trunk
     too.
7. **No fallback modes for a single point of failure.** A single point of failure is
   fixed, not wrapped in extra code paths. The design must not add a degenerate or
   legacy mode for robustness. "Reset every call" is a value of the one path, not a
   second path.
   - The owner asked whether this pattern exists elsewhere. The note lists known dual
     paths as consolidation candidates: the legacy one-word config fallback, CSV and
     TOML carrier dual support, the legacy open-item reader in `needs` (TC-253), and
     any second recording wrapper. Each is retired or justified.
8. **The coordinator calls the same function.** No subagent bypass. The note
   settles the communication path:
   - the prompt on stdin, which the kit already uses (immune to command-line caps and
     Windows shim re-parsing), or a prompt file the call names;
   - results as files in the lane plus the captured final message (codex `-o`, claude
     stream-json);
   - continuity through each CLI's own resume form instead of the Agent tool's.

   Known constraint: the permission classifier once refused codex's
   `--dangerously-bypass-approvals-and-sandbox` for an agent run (WI-541 notes); it
   ran under bypass mode on 2026-10-03.
9. **The RESYNC entry is the migration.** It moves the appropriate configs; no
   transition wrapper is kept.

## Scope widened 2026-10-04 (owner): the delegated-decisions record on every path

The owner asked whether a ledger of decisions made autonomously by an LLM was ever
built, and agreed to put its enforcement here and its review surface in WI-790 ("Yes,
...").

What exists (checked 2026-10-04):
- **The ruling:** OI-74 and OI-75, ruled 2026-08-31. The dial is
  `[attestation] decision_recording` (off / record / escalate-first); the shipped
  template is off, and this repo records.
- **The build:** WI-557 (2026-09-28; SR-225, LLR-282 to LLR-284, TC-292 to TC-294,
  IF-255 and IF-256, `kitlib/decisions.py`). One TOML file per run at
  `docs/decisions/<branch>.toml`. Each `[decision.D-NNN]` entry carries `decided`,
  `alternative`, `reversal_cost`, `why_not_escalated` and a free-text `review` cell.
- **How it is used:**
  - Two real records exist: `build-wi-557.toml` (5 entries) and `wi-688.toml`
    (1 entry). About 83 work items have landed since the ledger went live.
  - Only the loop's merge slot (`integrate.py`, around :2803) refuses a close that
    owes a record. The coordinator's hand path lands lanes by squash outside the slot,
    so nothing demanded a record there.
  - No owner surface shows the entries. The module says "a collator, if one is ever
    built" and "nothing reads [the review cell]".

Added to half 1 (the design note), as part of risk 8 and the slice plan's slice 2:
- **The one entry point hands every delegated session the record note**
  (`kitlib.decisions.session_note`), whether a loop session or a coordinator's
  sitting, so writing the record never depends on which path launched the session.
- **Every landing checks the record**, through one function, whichever path lands the
  lane: the loop's merge slot, or the coordinator's landing, which risk 8 moves onto
  the same entry and landing code. This fixes the single point of failure: the check
  lives where every landing passes, not in one of two paths (risk 7).
- **Measure the gap first:** list the delegated lanes landed since 2026-09-28 that owe
  a record under `decision_recording = "record"` and carry none. State whether any is
  backfilled or accepted as history.
- WI-790 builds the owner's "Decisions to review" section and the `reviewed` key.
  This row only guarantees that the records exist.

## Scope widened 2026-10-04 (owner): one lane-state provider and the lane's states

The owner, verbatim:

> "Now the final -potentially largest- design shift I want you to make. Right now
> there are multiple kit scripts interacting with each-other to coordinate a lane's
> state. I would like to distill that into a single lane state provider, and at the
> same time adjust how this state get's set through. If WI-788 is being scoped as a
> complex design breakdown, perhaps this belongs there as well.
>
> What I want: A single method that sets the current state of a lane / work-tree,
> with an Enum output list:
>
> 1. Planning (This can get skipped depending on the WI expectations): Single; Dual
>    (Draft, Cross-critique, Arbitration)
> 2. Build. Note: If detailed planning occurred and limited to one file or a few
>    functions, drop down to a medium tier builder if plan developed by a strong tier.
> 3. Review and rework. Important: This may have already been noted, but a builder
>    should be just as skeptical of a reviewers feedback as a review is of the
>    builder's work. Unless the project clearly specifies it, the builder should not
>    overdesign for corner cases. It should be able to assume inputs from other
>    functions / sources in the design system are constructed for validity, and if
>    there is a chance of rare corner case, the cheapest action is usually a retry
>    (like for example, to fetch a file read), rather than a complex guard that
>    creates more complexity and more maintenance. Again, that note might have
>    already been sufficiently emphasized.
> 4. In lane-adjudication. Lock adjudicator and prevent other lanes from merging.
>    Refresh the lane (Note this needs to happen before the adjudicator pulls in the
>    respective info craft WI and OI because the watermark must be up-to-date, and we
>    should not run tests on old checkouts.) Resolve any reviewer / builder
>    disagreements. Perform judgements. Take hand-back items and mint OIs and
>    decision entries (make sure prompting text here is adequate to encourage the
>    adjudicator to consume items accordingly.) At this moment when WI minting is
>    being considered consolidation is also being considered. Define merge action
> 5. Merge (mechanical)
> 6. Archive (mechanical)"

**Where lane state lives today** (from the 2026-10-03 code walk behind
`docs/iteration/wi-lifecycle.html`): it is spread across several carriers and modules
that read one another.
- **The spec's folder:** `queued/`, then `active/<branch>/`, then a terminal folder.
  The claim moves it, and the builder or `handback.py` moves it on.
- **Commit trailers:** `WI:`, `Blocked-WI:`/`BlockRef:`, `Review-Verdict:`,
  `Bar-Green:` and `Loop-Session:`.
- **Session logs** under `docs/iteration/`, and verdict files under `docs/reviews/`.
- **Machine-local markers and locks:** `out/review-owed`, `out/integrate.lock` (the
  merge slot) and `out/agent-loop.lock`.
- **Worker exit codes**, which `dispatch._advance` interprets: done, decided, review
  owed, park.
- **The dispatcher's per-tick lane table**, with its park and resume.
- **The scripts that coordinate it:**
  - `dispatch.py` (admission, advance, closes);
  - `lane.py` (spawn worker or refresh);
  - `integrate.py` (claim, refresh, merge slot, unload);
  - `agent_loop.py` (end state, review rounds, `resume_owed_round`);
  - `handback.py` (closes);
  - `intake.py` (the post-merge mint);
  - `schedule.py` (readiness).

**The state set** the provider owns is the owner's list, as one enum:
- `PLANNING`: `SINGLE`, or `DUAL` with `DRAFT`, `CROSS_CRITIQUE` and `ARBITRATION`. It
  is skippable per the row's expectations. `ARBITRATION` follows whichever arbiter
  option the note picks.
- `BUILD`.
- `REVIEW_REWORK`.
- `ADJUDICATION`: `LOCK`, `REFRESH`, `RESOLVE`, `JUDGE`, `MINT`, `MERGE_ACTION`.
- `MERGE` (mechanical).
- `ARCHIVE` (mechanical).

Added to half 1 (the design note). Each item comes with a recommendation the owner
rules on at the checkpoint:

- **LS1, the one setter.** `set_lane_state(lane, State, evidence)`, or similar, is the
  only way a lane's state changes. Every module above calls it instead of moving a
  folder, writing a marker or reading another module's exit code.
  - The kit derives its other states from committed evidence (`docs/stage`, review
    owed; "the evidence decides, alone"). So the note settles whether the state is
    stored or derived.
  - **Coordinator's recommendation:** one committed lane-state record that only the
    provider writes. Each transition is admitted only when its evidence is present
    (for example `BUILD` to `REVIEW_REWORK` needs the `WI:` trailer, and `MERGE`
    needs `Bar-Green` and the act). The record is never a second truth beside the
    evidence, and the markers it replaces are retired, not kept beside it (risk 7).
  - The note inventories every carrier above, and says for each whether it stays as
    evidence, folds into the record, or retires.
- **LS2, other states.** Parked (rate limit, review owed with no reviewer), handed back
  or partial, and claimed exist today. The note says whether each is a state, a
  substate, or an evidence condition the provider reports.
- **LS3, the build tier.** If a strong-tier plan limits the build to one file or a few
  functions, `BUILD` routes a medium-tier builder.
  - This deliberately overrides the row's BuildTier pin and the coordinator's standing
    rule against downgrading a declared route, for this case only. The owner directs
    it.
  - The trigger must be mechanical: the plan declares its scope (files and functions
    touched), and the provider reads it.
  - The escalation ladder (swap family, then tier up, then page) still applies after a
    failed round.
- **LS4, adjudication under one lock.** `LOCK` takes the adjudicator's lease and holds
  the merge slot, so no other lane merges while this lane is adjudicated.
  - `REFRESH` runs inside the lock and before the adjudicator reads any work-item or
    open-item state: trunk is merged in, the views regenerated and the declared bar
    run. The watermark is then current, and no test runs on a stale checkout.
  - The cost: merges serialize for the length of a sitting. The lease wait from risk
    5 (about 20 minutes) bounds other callers, and the note states the expected hold
    time.
- **LS5, resolve.** A builder may dispute a review finding with evidence. Disputes left
  unresolved after rework go to the adjudicator in `RESOLVE`. This replaces the hand
  path's separate arbiter for builder-reviewer disagreements.
- **LS6, mint.** In `MINT` the adjudicator consumes every handback item and every
  disposition. Each one becomes one of:
  - an open item with its placeholder work item (WI-790);
  - a decision entry (WI-790's "Decisions to review");
  - a successor work item;
  - a recorded no-action, with its reason.

  Consolidation is weighed at the same moment, so a new row is checked against open
  rows before it is minted (the consolidate brief folds in here). The brief makes
  consumption checkable: a list of every item with its disposition, so an item left
  undisposed is a refusal, not a silent drop. This is the "adequate prompting" the
  owner asked for.
- **LS7, merge action.** `MERGE_ACTION` is the adjudicator's declared outcome, for
  example merge, merge partial, return for another round, or cancel. `MERGE` and
  `ARCHIVE` carry it out mechanically. The note defines the set.
- **LS8, rulings this changes.** Each is stated as a change:
  - R1 (2026-08-01, "a work branch never mints a work-item id") and the merge slot's
    mint refusal. Under LS4 a locked, refreshed lane mints at trunk's current
    watermark. The proposed amendment: only a lane in `ADJUDICATION.MINT` under the
    lock mints.
  - The merge slot's refusal of an approval act from a work lane
    (`integrate.py:1154`). Acts move into the lane under the lock, which the S11 plan
    Q1 (ruled) already allows.
  - The S11 plan's act-freshness rung ("admitted only if no other act reached trunk
    since"). The lock replaces it.
  - Intake's post-merge mint arms (amendment, first-approval, dispose, Done-when
    changed, successors, rejudge). The note says which move into `MINT` and which
    stay mechanical after the merge.
  - The BuildTier pin, as LS3 overrides it.
- **LS9, builder and reviewer stance** (the owner's note).
  - What is already stated: `AGENTS.template.md` says "distrust certainty, yours or a
    reviewer's: a finding is a claim" and "right-size the solution", and PROCESS.md
    §3 owes a guard only at a trust boundary.
  - Two places pull the other way:
    - the rework brief says "REWORK FINDING (address this before anything else)"
      (`agent_brief.py:312`), which asks for compliance;
    - `AGENTS.template.md`'s "never retry past a failure whose cause you haven't
      found" reads against "the cheapest action is usually a retry".
  - The note proposes wording for each:
    - the rework brief asks the builder to confirm or refute each finding with
      evidence, and to record disputes for `RESOLVE`;
    - the reviewer brief gains the reciprocal: do not demand guards for inputs the
      design already constructs as valid;
    - the retry rule distinguishes a known transient class, which is retried (for
      example a file read failing on a Windows lock), from an unexplained failure,
      which is not.

**The slice plan changes:** the lane-state provider is the backbone the other slices
move onto.
1. The glossary and PROCESS.md wording (the states named once).
2. The labelled entry point and the one session store.
3. **The lane-state provider (LS1, LS2), with today's flow moved onto it unchanged in
   behaviour.**
4. Planning states through the entry point: the restored dual-plan pickup, LS3, and
   any per-item planning step.
5. **In-lane adjudication (LS4 to LS8):** lock, refresh, resolve, judge, mint with
   consolidation, merge action.
6. Provider routes and homes.
7. The spine-authoring flow, the text-then-act commit split, and LS9's prompt
   changes.
8. The RESYNC entry.

The row's title no longer describes its scope. The checkpoint may retitle it, and
because a title edit renames the file, it is a deliberate commit of its own.

## Owner rulings on LS8 and LS9, and the resume questions (2026-10-04)

**LS8, confirmed.** The owner: "Yes my minting and approval refusal were to ensure
there were not concurrency issues with the development branch, but with the
adjudicator locked that will not occur."
- R1's mint refusal and the merge slot's refusal of approval acts in a work lane
  existed only to prevent concurrency hazards on the development branch.
- Under LS4's lock they are amended to "only a lane in `ADJUDICATION` under the lock
  mints or takes an act", not kept beside the lock.

**LS9, refined.** The owner:

> "A past failure should still be identified, but that doesn't mean it must be acted
> on, it depends on the complexity of the work-around and the likelihood of
> occurrence. For instance, a virus scanner may try to scan new test files and block
> deletion / modification of test files. This shouldn't require the tooling to
> change, it should just surface an open item to the user or similar noting what
> caused an issue and the recommended action (in this case adding a test directory
> to an ignored virus scanning path) is. ... the rework brief can still encourage the
> builder of course, but the builder likewise can note it should only act on
> verified evidence and on a claim that cannot be mitigated through a setting change
> from the user or just from a simple retry of the action if it is due to OS
> interactions."

So the note's LS9 wording becomes:
- **Identify every failure; act only when it pays.** A failure is always identified
  and recorded. Whether the code changes depends on the work-around's complexity
  against the failure's likelihood.
- **The builder acts on a finding only when both hold:** it is verified by evidence,
  and it cannot be mitigated by a setting the user changes, or by a simple retry
  when the cause is an OS interaction (a file lock, a virus scanner holding a new
  test file).
- **An environment-caused failure changes no tooling.** It is surfaced to the owner
  with its cause and the recommended action, for example "add the test directory to
  the virus scanner's excluded paths".
  - **Where that surfaces is for the note to settle:** an open item, which under
    WI-790 needs a placeholder row, for example one confirming that the setting was
    changed; or an entry in WI-790's "Decisions to review".
  - **Coordinator's recommendation:** the decision entry for advice the owner may
    simply take, and an open item only when work is blocked until the owner acts.
- **The rework brief** still asks the builder to address findings, now on these
  terms. The reviewer brief gains the reciprocal: a finding that a setting or a
  retry mitigates is advice, not a defect.

**LS10, resume (from the owner's frontier questions).** The note settles how a lane
resumes, at two levels:
- **State.** The provider reads the committed lane-state record and checks it against
  the evidence.
  - The record is written in the same commit as the evidence that admits the
    transition, so an interruption cannot leave the two disagreeing.
  - On resume the provider re-admits whatever transition the evidence already
    supports.
  - The note also decides what happens to uncommitted work found in the worktree:
    keep it and resume the session in place, or reset to the last commit (today's
    refresh resets).
- **Session.** An interrupted session resumes through its CLI's own resume form,
  using the session id recorded in the session log (`session-id`) and in the
  retention store, instead of starting fresh.
  - **Today:** session logs are committed on the lane (a `telemetry:` commit) and
    reach trunk at the merge. Resumable ids live in one untracked store,
    `out/adjudicator/`, under the primary checkout, which every lane worktree shares
    (`session_keep.store_dir`).
  - **To verify by probe:**
    - whether each CLI resumes by id from a different working directory;
    - codex keeps sessions in its home, so it is expected to resume from anywhere;
    - Claude Code is believed to file conversations per project directory, so a
      retained adjudicator that moves between lane worktrees may need a fixed
      working directory, such as the primary checkout or a dedicated adjudicator
      worktree;
    - OpenCode resumes with `--session` from its own data directory.
  - The coordinator's subagent resume (SendMessage) has no store and no log, and
    risk 8 retires it.

## Owner direction 2026-10-04: a rolling usage ledger on trunk

The owner: "the generated usage should roll into WI-788, with the intent a rolling
token usage with relevant columns is continuously appended at trunk with its own
items and those of its work-tree lanes. Obviously we won't be able to record
everything for this project because of how the session in Claude Code runs external
to those mechanisms, but it is something we'll see in the first down-stream adopter
checks."

- **U1, the ledger.** One append-only usage ledger on trunk, generated from the
  session logs. It holds a row per session for trunk's own sessions and every lane's.
  - **Columns:** date, work item, lane, role or kind, route, provider, CLI, model,
    the `gen_ai.usage.*` counts, fresh input, cost where known, wall seconds, outcome
    and session id.
  - **Recommended mechanism:** lanes keep writing their session logs. `trunk_step`,
    which already compiles `log.d` into `log.md` at every refresh and bookkeeping
    commit, appends the rows it has not yet seen. The file is then generated,
    append-only and conflict-free, the same pattern as the log.
  - **A discarded lane's usage** is harvested into the ledger before its work is
    dropped (see OI-103 Q6).
  - **A hard kill that wrote no session log:** the note designs how to recover its
    usage, from the CLI's own record by session id or from a launch noted before the
    session starts.
  - **Placement:** U1 joins the session-store slice.
  - **What it cannot cover here:** this repo's coordinator sessions (Claude Code
    hand sittings and shell-launched reviews) run outside the service and stay
    unrecorded until risk 8 moves them onto the entry point. The first downstream
    adopter shows the full picture.

## Amendments from the Sol review (2026-10-04)

Codex Sol (gpt-6.1-sol, high effort, read-only, at `b61f450f`) reviewed the widened
spec and rated it NOT-READY for design as written. Its brief and review are in
`docs/reviews/2026-10-04-wi788-widened/`, which also carry its full inventory of
carriers, modules, spine rows, docs and prompts. The coordinator confirmed findings 2,
3, 6 and 9 in the code. The amendments below bind the design note and supersede
earlier text where they differ. The decisions only the owner can make are in OI-103.

- **B1 State: derived evidence, recorded decisions** (supersedes LS1's
  recommendation and LS10's "same commit" promise).
  - The provider derives a lane's current state from committed evidence and live
    ownership (leases, locks, running processes).
  - Committed records carry decisions (a merge intent, a merge action, a dispute's
    resolution), never claims that a process or lock is still live.
  - The note specifies recovery at every effect boundary: lease taken, process
    launched, trunk advanced, worktree removed. Today's claim already orders its
    effects so that an interruption is recoverable (`bookkeeping.py:68-80`).
- **B2 Tree identity.** The merge reproduces the refreshed lane tree byte for byte, and
  `Bar-Green` attests that exact tree (`integrate.py:9-14`, `kitlib/verdict.py`). So
  `MERGE` is derived from git ancestry and `ARCHIVE` from refs and worktree inventory,
  never written into the merged tree. A merge intent is committed before the final
  bar. The note states where each record lives and which checkout writes it.
- **B3 Lock coverage.** Locking the merge slot does not stop every writer that can
  stale a sitting. Claims (under the dispatch lock), intake CLI mints, plan
  artifacts' id allocation and keep-warm records all commit to trunk outside
  `out/integrate.lock`.
  - The adjudication authority must cover every writer that affects the sitting's
    tree, queue or watermark (OI-103 Q1), and be held through trunk advancement, not
    just `MERGE_ACTION`.
  - Only once that coverage holds does the lock replace S11's freshness check.
- **B4 Lock mechanics.** Risk 5's 20-minute figure bounds a wait to acquire, not how
  long a sitting holds. The note specifies:
  - one canonical lock location, an acquisition order, ownership transfer,
    cancellation and expiry;
  - waiting outside the merge slot and the dispatcher's tick, with non-blocking
    scheduling;
  - that risk 5's fresh session still takes the station authority;
  - no "run unguarded on an unsupported filesystem" behaviour for this authority
    (`agent_common.py:946-957`).
- **B5 Final evidence after adjudication.** `JUDGE` and `MINT` write to the tree after
  `REFRESH`. So the final independent review (S11 Q4, ruled always owed), the
  regeneration and the `Bar-Green` bar run on the final staged tree, after every
  substantive adjudication write. Nothing tracked changes the tree after that before
  the merge. The note defines the back edge on rejection, and when the lock is
  released.
- **B6 The lock is not authorization.** `merge_approval_refusal` also requires
  first-approval and amendment scopes from claimed adjudication rows
  (`acceptance_record.py:805-824`; LLR-278, TC-278). These are replaced by an
  independently recorded, previewed lane scope. Actor independence, held-rung
  authority, named rows, snapshot coverage and out-of-scope refusals are kept.
- **B7 Planning has two products.**
  - An implementation plan for the assigned item, which leads to `BUILD`.
  - A decomposition (dual-plan), which yields successor rows and a terminal parent.
  - The selected plan's child allocation moves onto the one serialized allocator,
    because `plan_artifacts` allocates ids directly today. Parent closure, PAGE
    recovery and duplicate suppression are defined before automatic admission is
    restored.
- **B8 LS3 needs a typed scope declaration.** Today's plan tables carry `Plan-WI`,
  title, covers, interfaces and predecessors, but no implementation scope and no
  planner tier. The note adds a typed scope (files and functions), the planning
  tier, the accepted plan's identity and a threshold (OI-103 Q5). Work that exceeds
  the declared scope returns to the row's tier, and escalation still overrides.
- **B9 Conditional resume** (supersedes LS10's unconditional session resume). A lane
  resumes from evidence. Its session resumes only when its id and ownership are valid
  under the reset terms. Today a launch exception abandons the retained session
  (`session_service.py:238-243`), and an expired lease blocks reuse. The note designs
  durable invocation and session discovery, and promises no finished-session log
  after a hard interruption.
- **B10 Attribution for every authoring kind.** Commit ranges are recorded for every
  authoring kind through the entry point (build, adjudicator edits, author review),
  and family exclusion comes from all authors of the judged scope, not BUILD logs
  alone. OI-101 Q1's non-mutating final pass is recorded as the spine-authoring
  exception to the blanket rule that "a review never runs in a session that authored
  what it judges".
- **B11 Precedence, where earlier text conflicts.**
  - **Retention:** the second-pass defaults win (the shipped adjudicator is retained,
    the builder resets every call, this repo's dial may stay as it is).
  - **Spine authoring:** OI-101 Q1 wins over "as an option".
  - **Risk 6:** it applies on lane and trunk (OI-101 Q2).
  - **Routes:** Grok and FreeLLMAPI go through OpenCode, and Google is documentation
    only (OI-101 Q3 and Q4). This supersedes the original per-provider research list
    where they differ.
  - **`ARBITRATION`** means selection under the chosen protocol. It does not mandate
    an arbiter model call.
  - **Calls and effects:** `ask` owns model and session calls, and the lane provider
    owns lifecycle effects. Attended and loop paths share one landing operation.
  - **The successor rows** deliver the whole widened scope, not just the original
    half-2 bullets.
  - **S11:** S11's freshness check is replaced only with complete writer exclusion
    (B3). Its ruled exhaustion behaviour, 3 returns then land, is restated or amended
    by OI-103 Q2.
  - **LS9:** its refined wording supersedes the earlier LS9 proposal.
- **B12 One dependency graph, a design split into chapters, and Done-when coverage.**
  - **The design** is split into four linked chapters under one owner checkpoint:
    1. state, evidence and recovery;
    2. sessions, routing and accounts (including U1);
    3. planning and tiering;
    4. adjudication, mint and landing authority.

    It closes with one amend/preserve/retire matrix (rows, contracts, docs, prompts;
    the review lists them) and one dependency graph. That graph replaces both
    numbered slice lists above, and successors are named by identifier, not ordinal.
  - **The build order:** shared contracts, then the session and account foundation
    with the provider moved onto today's flow unchanged in behaviour, then planning,
    then adjudication with the text-then-act split and final evidence, then the
    remaining routes. The provider slice is representation only, with no new locking,
    minting authority or archive ordering. Homes come early, because retained homes
    override route environments today.
  - **Migration:** each successor that ships carries its own RESYNC entry, so
    migration does not wait for the end.
  - **Dependencies:** WI-790 (open-item placeholders, the commit-time sync rule,
    "Decisions to review") and WI-791 (OI-100: need, assumption and surrogate
    routing; held-rung CLARITY acts) are contracts LS6 consumes, not redesigns.

## Deliverable
