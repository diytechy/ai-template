+++
id = "WI-788"
title = "Session families with reset terms, a glossary, per-route provider homes, and new routes"
workstream = "process"
specref = "docs/agents.toml"
sr_refs = ["SR-222"]
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
2. **Build what the owner approves.**
   - Route rows in `docs/agents.toml`, and in the shipped template where adopters need
     them.
   - The Google adapter, and any opencode provider handling.
   - The per-route home wiring this repo uses for its own accounts.
   - Spine rows through in-lane adjudication.
   - Tests against recorded fixtures. A live recording only where the owner authorizes
     the run.
   - A RESYNC_PACK entry.

   Nothing forces an adopter to install a new CLI.

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

- `docs/glossary.md`, referenced from PROCESS.md, with one term per concept:
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

## Deliverable
