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
- **Secrets: ANSWERED by the owner, 2026-10-04.** Option (b) for every listed
  route: structure plus detection. "b, with a provisions for an a like method when
  set in agents.toml", then, of the per-route forms offered: "Both 2 or 1 will work.
  I lean toward #1." So:
  - **every launch (structure):** a model is never launched in a worktree holding a
    file of a known secret class (the `kitlib` secret-class vocabulary
    `check_privacy` already uses); the launch is refused by name;
  - **every session (detection):** session transcripts are scanned for the same
    secret classes, and a hit is reported to the owner the way a commit-scan hit is;
  - **per route, opt-in (#1):** a route row may set `deny_reads = [...]` (paths, e.g.
    the home-folder CLI credential files), and its launch then passes them to its
    CLI's own read-deny where that CLI supports one; a route whose CLI has no
    read-deny refuses a non-empty `deny_reads` at preflight rather than silently
    ignoring it. #2 (a per-route list of extra paths that must be absent before
    launch) is acceptable to the owner too, if #1 proves impractical.
  It is one launch path with declared values, never a second mode.

It needs WI-815 (the routes row), and it is due before the first free or
third-party route is enabled.

## Done-when

- The shipped template, this repo's `docs/agents.toml` header and the
  row-admission wording state that a listed route is trusted with the repository's
  standard content, and that listing it accepts its provider's terms.
- A launch in a worktree holding a file of a known secret class is refused, naming
  the file and its class; tested per class, and for a clean worktree.
- Session transcripts are scanned for the same classes, and a hit reaches the
  owner's surface; tested on a fixture transcript.
- A route's `deny_reads` reaches its CLI's read-deny where supported (tested per
  supporting CLI), and a non-empty `deny_reads` on a CLI with none is refused at
  preflight.
- SR and LLR rows for the three behaviours pass adjudication.
- Review bar: A. RESYNC_PACK: an entry if the template's wording or the launch
  changes.
