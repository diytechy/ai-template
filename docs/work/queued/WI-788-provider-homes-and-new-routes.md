+++
id = "WI-788"
title = "Per-route provider homes for multiple accounts, and new routes: SuperGrok, Google's CLI, FreeAI through opencode"
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

## Deliverable
