# Development tracks — parallel lanes

*Applies only under the parallel-tracks layer (process-options.md "Parallel
tracks"); a single-lane repo deletes this folder.* This repo runs **several
large deliverables in parallel**. Each is a **track**: an independent lane of
work with its own coordination files, so two drivers (human or agent) never
thrash the same blackboard.

## What a track binds together

| Binding | What it is | Collision it prevents |
| --- | --- | --- |
| **Worktree** | `git worktree add ../<repo>-<track> llm/<track>` | two drivers in one checkout (filesystem) |
| **Branch** | `llm/<track>` iteration branch | interleaved history; gives the stall guard a private HEAD |
| **Lane dir** | `docs/tracks/<track>/` | two drivers editing one status.md / plan.md / run-state |

## The lane directory

Each `docs/tracks/<track>/` holds this track's copies of the coordination files
that are otherwise repo-singular at `docs/`:

```
docs/tracks/<track>/
  status.md          # this track's Current State — its resume surface
  plan.md            # this track's PLAN/BUILD block list (if it uses the cadence)
  run-state          # coordinator contract: RUNNING | DONE | BLOCKED | NEEDS-HUMAN
  run-phase          # coordinator model-tier key (PLAN | BUILD | …); optional
  log.md             # this track's append-only session evidence
  iteration/         # this track's session logs + generated iteration_index.md
```

`scripts/agent_loop.py --track <name>` (or `AGENT_TRACK=<name>`) resolves **all**
of these under the lane; without `--track` the coordinator uses `docs/` exactly
as before. The lane is chosen by **invocation**, never a tracked pointer file.
The coordinator creates a lane on first use; a dormant track can be just a lane
directory + a "blocked on `IF-…`" note, no worktree, costing nothing.

## What stays repo-singular (integrator-owned, never in a lane)

The requirement registries (`docs/requirements/*` — one `SN→SR→LLR→TC` spine,
0 orphans across the whole repo), `docs/gate` + `gate-policy` + `push-policy` +
`privacy-check` + `guardrails-policy`, the **root** `docs/status.md` (the
cross-track dispatcher), the **root** `docs/log.md` (gate sign-offs), `AGENTS.md`,
and the generated code map. A track **proposes** changes to these (off-spine
scope drafts, findings, `IF-###` seam rows); the **integrator** (a sync session,
human or an agent leg run without `--track`) lands them and is the only writer of
the root dispatcher. See [id-blocks.md](../requirements/id-blocks.md) for the
per-track ID reservations that keep parallel drafts from minting colliding ids.

## Active tracks

_(One row per lane — edit for yours.)_

| Track | Lane | State |
| --- | --- | --- |
| `<track-a>` | `<track-a>/status.md` | active |
| `<track-b>` | `<track-b>/status.md` | dormant — blocked on `IF-…` |

The root [../status.md](../status.md) dispatcher is the one-screen roll-up of
these lanes plus the cross-track items.
