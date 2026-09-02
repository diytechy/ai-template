# The work-item registry (`docs/work/`)

One work item is one Markdown spec file in this folder, and **status is the
DIRECTORY** — never a frontmatter field — so moving the file is how state
changes and there is exactly one home for the fact. The spec format itself
(frontmatter keys, the backward-only `## Deliverable` body, the filename rule)
is documented in the [WI-000 exemplar](queued/WI-000-example.md) beside this file.

| Location | Status |
|---|---|
| `draft/WI-###-<slug>.md` | `draft` — written down, not claimable |
| `queued/WI-###-<slug>.md` | `queued` — filed, unclaimed |
| `active/<branch>/WI-###-<slug>.md` | `active` — claimed by that branch |
| `deferred/WI-###-<slug>.md` | `deferred` — a decision to park; not now |
| `../archive/work/complete/WI-###-<slug>.md` | `done` — it shipped |
| `../archive/work/cancelled/WI-###-<slug>.md` | `cancelled` — it never will |
| `../archive/work/partial/WI-###-<slug>.md` | `partial` — a lane stopped early; the per-close report under `docs/handbacks/` is the event's identity, and continuing the work mints a successor |
| `../archive/work/restructured/WI-###-<slug>.md` | `restructured` — a consolidation ABSORBED it into a successor; its scope text stays byte-identical and its Deliverable is the one line `Restructured into WI-<successor>.` |

`SPEC_STATUS_DIRS` in `scripts/kitlib/registry.py` is the authority this table
restates, and the readers **raise** on a directory outside that set rather than
skip it quietly — so inventing a folder here takes rows OUT of the registry
instead of adding a state to it.

## A terminal row STAYS in the registry — under the archive (WI-504)

`complete/`, `cancelled/`, `partial/` and `restructured/` are the four terminal
states, and a row
that reaches one stays in the registry permanently — but not in THIS directory.
`docs/work/` holds only rows still in flight; the terminal four live one
directory deeper, under `docs/archive/work/`, so an agent listing the active
workspace meets only the frontier instead of wading through hundreds of closed
rows to find it (OI-55, ruled 2026-08-22). Nothing is deleted and nothing stops
being **live data**: `kitlib.registry.read_spec_rows` reads `docs/work/` and
`docs/archive/work/` as ONE registry (`spec_roots`), so a closed row is still a
predecessor successors' `needs` edges resolve against, a `sr_refs` trace link,
and a row the dashboard counts — status is still the directory, only its parent
changed. `docs/work/archive/` itself must still never exist: that was the
PRE-WI-384 shape, one folder holding two terminal states behind a `disposition`
attribute; splitting it into `complete/` and `cancelled/` is precisely what
deleted that attribute and its validator, and moving the split three under
`docs/archive/work/` does not revive it — each keeps its own directory,
now beside the others one level further out.

`restructured/` is the fourth word and the newest (the 2026-09-02
backlog-restructure plan §1.6). It exists because the other three cannot carry
an ABSORBED row: `cancelled` says the scope was refuted — and says it loudly,
since `intake.context_block` briefs every later row on the same SRs with the
cancelled precedent "do not re-propose the refuted", which would tell an
absorbed row's own successor not to build it — while `partial` says a lane
stopped early and owes a per-close report and a disposition, neither of which a
consolidation produces. A restructured row was carried onward: same scope text,
one-line Deliverable naming the successor, and its inbound hard edges re-pointed
to that successor at the close (an edge still naming it is reported as a dead
one, never silently satisfied).

What *does* archive is the other artifact: the narrative **spec-of-record** under
[`../specs/`](../specs/), which lives only while its WI is open and moves to
`docs/archive/specs/` at close (rule **R-F**). Two artifacts, two lifecycles —
the registry row is permanent, the spec-of-record is not.
