# The work-item registry (`docs/work/`)

One work item is one Markdown spec file in this folder, and **status is the
DIRECTORY** — never a frontmatter field — so moving the file is how state
changes and there is exactly one home for the fact. The spec format itself
(frontmatter keys, the backward-only `## Deliverable` body, the filename rule)
is documented in the [WI-000 exemplar](queued/WI-000-example.md) beside this file.

| Location | Status |
|---|---|
| `draft/WI-###-<slug>.md` | `draft` — written down, not claimable |
| `queued/WI-###-<slug>.md` | `queued` — filed, unclaimed (`blockref` set = parked) |
| `active/<branch>/WI-###-<slug>.md` | `active` — claimed by that branch |
| `deferred/WI-###-<slug>.md` | `deferred` — a decision to park; not now |
| `complete/WI-###-<slug>.md` | `done` — it shipped |
| `cancelled/WI-###-<slug>.md` | `cancelled` — it never will |
| `partial/WI-###-<slug>.md` | `partial` — a lane stopped early; the per-close report under `docs/handbacks/` is the event's identity, and continuing the work mints a successor |

`SPEC_STATUS_DIRS` in `scripts/agent_common.py` is the authority this table
restates, and the readers **raise** on a directory outside that set rather than
skip it quietly — so inventing a folder here takes rows OUT of the registry
instead of adding a state to it.

## A terminal row STAYS here — there is no archive

`complete/`, `cancelled/` and `partial/` are the three terminal states, and a row
that reaches one stays in the registry permanently. Nothing is moved out, nothing
is deleted: every reader rglobs the whole of `docs/work/`, and a closed row is
still **live data** — a predecessor that successors' `needs` edges resolve
against, a `sr_refs` trace link, and a row the dashboard counts. Moving closed
rows to an archive would silently break those edges rather than tidy anything, so
**`docs/work/archive/` must never exist**. It did once, holding two terminal
states behind a `disposition` attribute; splitting it into `complete/` and
`cancelled/` is precisely what deleted that attribute and its validator.

What *does* archive is the other artifact: the narrative **spec-of-record** under
[`../specs/`](../specs/), which lives only while its WI is open and moves to
`docs/archive/specs/` at close (rule **R-F**). Two artifacts, two lifecycles —
the registry row is permanent, the spec-of-record is not.
