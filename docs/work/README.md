<!--
Contracts: IF-023, IF-024, IF-054, IF-079, IF-159 — the interface seams this
directory declares (process.md §8; rows of record in
../requirements/interfaces.toml).

Contract IF-023: the work-item registry as the validated registry. One row is
    one Markdown spec file whose `+++` frontmatter carries `id`, `title`,
    `workstream`, `sr_refs`, `needs` and the optional scheduling keys, and whose
    `## Deliverable` body is the backward-only record; the filename repeats the
    id. STATUS IS THE DIRECTORY, so a spec under a directory outside the
    declared set RAISES rather than being skipped — inventing a folder takes
    rows out of the registry instead of adding a state to it. This directory
    holds the rows still in flight and `../archive/work/` the three terminal
    states; both are read as ONE registry, so a closed row is still a
    predecessor, a trace link and a counted row.
Contract IF-024: the same registry read as the roadmap DAG — each row's id,
    title and `needs` edges, with status taken from the directory — so a
    rendered roadmap shows what is queued, claimed, deferred and closed without
    a second statement of state anywhere.
Contract IF-054: the same registry read for READINESS. A row offers its status,
    its `needs` edges (an entry prefixed `~` is a SOFT edge and never blocks)
    and the optional `priority`, `exclusive`, `blockref`, `est_tokens` and
    `safety_class` keys. An absent optional key reads as its documented default,
    and the defaults are chosen to fail closed: an absent safety class is
    `unclassified` and is never scheduled, an absent priority is 0, an absent
    exclusive is empty. A hard edge is satisfied only by an integrated `done`
    predecessor — a cancelled one never satisfies it.
Contract IF-079: the registry as one of the two interchangeable FORMS. The
    frontmatter keys, the filename rule and the status-by-directory bijection
    are this format's definition, and the legacy row-per-line CSV is the other
    form, kept for migrating in and exporting out. The verify mode round-trips
    the whole registry through a temporary directory and compares cell-exact,
    writing to neither live home; byte identity is reported, never asserted.
Contract IF-159: the WRITE side of this directory, and the format's single
    writer — one registry row rendered as one spec file under the row's status
    directory, the filename repeating the id, UTF-8 with LF endings on every
    platform. The file is RE-READ and re-parsed before its path is returned: a
    spec whose frontmatter does not reconstruct its source row cell-exact, the
    order key included, raises instead of being left on disk. Bulk conversion
    and single-item filing both go through it, so no spec is produced by a path
    that skips that check. Moving a file between the status directories is a
    state change, not a write of this format.
-->

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
| `../archive/work/complete/WI-###-<slug>.md` | `done` — it shipped |
| `../archive/work/cancelled/WI-###-<slug>.md` | `cancelled` — it never will |
| `../archive/work/partial/WI-###-<slug>.md` | `partial` — a lane stopped early; the per-close report under `docs/handbacks/` is the event's identity, and continuing the work mints a successor |

`SPEC_STATUS_DIRS` in `scripts/kitlib/registry.py` is the authority this table
restates, and the readers **raise** on a directory outside that set rather than
skip it quietly — so inventing a folder here takes rows OUT of the registry
instead of adding a state to it.

## A terminal row STAYS in the registry — under the archive (WI-504)

`complete/`, `cancelled/` and `partial/` are the three terminal states, and a row
that reaches one stays in the registry permanently — but not in THIS directory.
`docs/work/` holds only rows still in flight; the terminal three live one
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
`docs/archive/work/` does not revive it — the three keep their own directories,
now beside each other one level further out.

What *does* archive is the other artifact: the narrative **spec-of-record** under
[`../specs/`](../specs/), which lives only while its WI is open and moves to
`docs/archive/specs/` at close (rule **R-F**). Two artifacts, two lifecycles —
the registry row is permanent, the spec-of-record is not.
