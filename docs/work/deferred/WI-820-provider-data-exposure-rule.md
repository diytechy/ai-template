+++
id = "WI-820"
title = "What listing a route in agents.toml means for the repository's content: provider terms and secret-bearing files"
workstream = "process"
specref = "docs/plans/2026-10-04-lanes-evaluation.md#taken-deferred-route-listing-and-the-repository-content"
needs = ["WI-815"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

DEFERRED by the owner's direction (2026-10-04: "Add 3 as WI but also deferred"),
from the evaluation of `thebpandey/lanes`
([plans/2026-10-04-lanes-evaluation.md](../../plans/2026-10-04-lanes-evaluation.md)).
There, `model-relay` refuses to run a third-party model in the main checkout or in
a worktree holding `.env`-style files.

The owner rejected a trust tier: "if a model should not be trusted it should not
be in agents.toml". Trust is binary, by inclusion in `docs/agents.toml`, so this
row adds no trust level and no per-route exemption. What is left to decide:

- **What inclusion records.** Does listing a route state that its provider's terms
  (retention, training on input) are acceptable for this repository's content? If
  so, the shipped template and the row-admission wording say so, and enabling a
  free or third-party route (FreeLLMAPI through OI-105, OpenCode's free models) is
  the owner's explicit act.
- **Secret-bearing files.** Whether any model launch needs a guard against
  secret-bearing files in the worktree. If one is needed, it applies to every
  provider alike, since inclusion is the trust decision.

It needs WI-815 (the routes row), and it is due before the first free or
third-party route is enabled.

## Done-when

- Settled at the time it is taken, against the two questions above, with the
  owner's answer recorded. Any guard it adds applies to every listed route, with
  no per-provider mode.
- Review bar: A. RESYNC_PACK: an entry if the template's wording or the launch
  changes.
