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

- **What inclusion records: ANSWERED by the owner, 2026-10-04.** "Yes listed in
  agents.toml means to trust with standard repo content and agreed it should be
  plainly stated as such." So the shipped template, this repo's `docs/agents.toml`
  header and the row-admission wording state it plainly: a listed route is trusted
  with the repository's standard content, and its provider's terms are accepted by
  listing it. Adding a free or third-party route (FreeLLMAPI through OI-105,
  OpenCode's free models, a Claude Code row pointed at another provider) is
  therefore the owner's explicit act.
- **Secrets: still open.** The owner (2026-10-04): "Handling of secrets is perhaps a
  harder question, and how does that get validated (or restricted) is not
  something I'm privy to." Standard repo content excludes secrets, so the question
  is how to keep them from reaching any listed model, uniformly. Found on
  2026-10-04: this repo's checkouts hold no secret files (lane worktrees get only
  tracked files), and the secrets an agent could read are the CLI credential files
  in the user's home directory (`~/.claude/.credentials.json`, `~/.codex/auth.json`),
  outside every worktree. The coordinator laid out three layers for the owner to
  choose among: keep secrets out of where agents work (structure, checkable at
  launch), deny reads where a CLI supports it (restriction, per CLI and not
  uniform), and scan session transcripts and commits for secret classes
  (detection after the fact). None can prove a model never saw a secret.

It needs WI-815 (the routes row), and it is due before the first free or
third-party route is enabled.

## Done-when

- Settled at the time it is taken, against the two questions above, with the
  owner's answer recorded. Any guard it adds applies to every listed route, with
  no per-provider mode.
- Review bar: A. RESYNC_PACK: an entry if the template's wording or the launch
  changes.
