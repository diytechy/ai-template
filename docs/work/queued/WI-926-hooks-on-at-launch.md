+++
id = "WI-926"
title = "Every agent route refuses to start in a checkout whose commit hooks are not on, checked once at the one entry every route passes through"
workstream = "process"
sr_refs = ["SR-113", "SR-019"]
specref = "docs/specs/WI-926.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = []
+++

## Context

**Placeholder** (owner, 2026-10-15, the attended checkpoint session):
filed to hold the owner's direction; it owes its scope critique,
dispositions and a confirming round before any claim, and its calls are
not yet ruled.

The kit's commit hooks are opt-in per checkout: only `setup.*`,
`dev-setup.*` and bootstrap set `core.hooksPath`, and no route checks it
when it starts. In a fresh clone, or on a machine where setup was skipped,
every commit runs with no hook at all, and nobody typed a bypass. Today the
landing's walk of each lane commit (the owner's 2026-10-03 rule: commit
against its parent at pre-commit, and per lane commit at merge) is the
backstop for that gap, and WI-922 was filed to close the corners of the walk
itself, where a commit that escaped its hook meets a landing the walk cannot
place.

The owner's direction: protect against the hookless checkout by
construction, not by more corners in the walk. The agent guide makes hooks
part of starting work, and one mechanical check at the top of the function
every route passes through refuses to start when the hooks are not on.
This row is a candidate replacement for WI-922's scope, weighed in the
re-scope walk the owner ordered (coordinator-2026-10-15 D-010).

## Deliverables (sketch, for the scope critique)

1. **The check, in one home:** one shipped function that answers whether
   this checkout's hooks are on: `core.hooksPath` resolves to the kit's
   hooks directory and the hooks there are present and executable. Deny by
   default: an unset, unresolvable or foreign hooks path, or a missing hook,
   is "not on", named in the refusal with the setup command that fixes it.
2. **Called first by every agent route:** the managed loop's launch, the
   integrator's claim and merge slot, the coordinator's lease, and the
   kit's bookkeeping commits, each through the one entry they already share
   or one introduced for the purpose (the critique names it), so no route
   can start without passing the check.
3. **The agent guide:** `AGENTS.template.md` states that hooks are on
   before any work (the setup step that turns them on) and that a commit
   never bypasses them; this repository's own guide says the same.
4. **The deliberate as-is writers stay:** `handback.close_partial`'s
   `--no-verify` close commit and the plumbing bookkeeping commits are
   judged by the landing walk as today; the check guards the checkout they
   run in, not their commit.

## Done-when (sketch, for the scope critique)

- Each agent route, started in a fixture checkout with no hooks path, a
  foreign hooks path, or a missing hook, refuses before any work and names
  the setup command; started in a checkout with the hooks on, it runs. Each
  case fails before the change.
- One function holds the check; a test pins that every route's entry calls
  it (a census, like the commit floor's).
- The agent guide and the template carry the hooks-on line.
- `RESYNC_PACK.md` carries the entry; an adopter's forced change, if any,
  is named.
- The bar is green on the landing tip.

## Calls for the owner (open)

- Which entry is "the top function every route will touch", or whether
  each route calls the check itself.
- Whether WI-922 is cancelled, narrowed, or kept beside this row (the
  D-010 walk).
- Whether a human committing by hand outside any agent route is in scope
  (the check guards agent routes; the hook itself still runs only where it
  is installed).
