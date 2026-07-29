+++
id = "WI-000"
title = "EXAMPLE work item (permanent exemplar — keep)"
workstream = "example"
sr_refs = []
needs = []
buildtier = "medium"
priority = 0
+++

## Deliverable

**What this file is.** One work item is one Markdown spec file under
`docs/work/`, and this `-000` example is the format's documentation. Copy it to
`docs/work/queued/WI-<n>-<slug>.md` to file real work; keep this one — nothing
gates on it, so a fresh scaffold stays vacuously clean. It is inert in the two
ways that matter: every loader skips a `-000` id (the same rule that makes the
`-000` row in each registry template inert), and it does not decide which
registry home is authoritative, so scaffolding it never demotes a project's
`docs/requirements/work-items.csv`. That inertness is also why this example may
carry a filled `Deliverable` while sitting in `queued/`, which the rule below
forbids for real work.

**Status is the DIRECTORY, never a field.** One home per fact: the mutable
state is the file's location, the immutable-ish metadata is the frontmatter, and
the narrative is the body.

| Location | Status |
|---|---|
| `docs/work/queued/WI-###-<slug>.md` | `queued` — filed, unclaimed |
| `docs/work/active/<branch>/WI-###-<slug>.md` | `active` — claimed by that branch |
| `docs/work/deferred/WI-###-<slug>.md` | `deferred` — parked with its reason |
| `docs/work/archive/WI-###-<slug>.md` | `done` |
| `docs/work/archive/…` + `disposition = "retired"` | `retired` |

Two consequences worth stating, because they are the reason for the shape:

- **`blocked` has no directory.** A blocked item is `queued/` plus a `blockref`
  frontmatter key naming the reason; readiness is the scheduler's to derive, so
  a second encoding of "not now" would be a second home for one fact.
- **`retired` is a move, never a deletion.** It shares `archive/` with `done`
  and is told apart by `disposition = "retired"`, with the reason in this body:
  a terminal won't-build record that stays in the registry forever. A retired
  predecessor does **not** satisfy a successor's hard dependency (it never
  integrates), so a work item hard-blocked on one stays visibly waiting.

**The filename** is `<id>-<slug>.md`, the slug a short kebab-case of the title.
The id in the frontmatter and the id in the filename are compared on every read
— two homes for one fact, so they are checked rather than trusted apart.

**Frontmatter keys.** All optional except `id` and `title`; an absent key and an
empty one mean the same thing, so empty keys are omitted rather than written as
a wall of `= ""`.

- `workstream` — the mutable grouping category this work advances.
- `sr_refs` — the requirement id(s) it delivers (`["SR-012", "SR-013"]`).
- `needs` — the predecessor id(s): the DAG edges. A bare id is a **hard** edge
  (it blocks; the graph must stay acyclic); a `~`-prefixed id is a **soft** edge
  (advisory ordering — it must resolve, never blocks, and renders dashed). The
  `~` is meaning, not decoration, and is carried verbatim.
- `specref` — the forward bridge (rule R-E): a `docs/specs/WI-###.md` file or a
  `doc#anchor` that resolves while the item is open, and clears at close.
- `buildtier` — an optional routing hint for the unattended coordinator:
  `strong|medium|quick` (legacy `weak` reads as `quick`). It is the STARTING
  tier for this item's build sessions and never caps escalation; absent means
  the phase default.
- `critique_budget` / `critique_exhaustion` — optional critique-loop controls: a
  positive integer or `inf`, and `move-on` or `block`. Absent keeps the global
  default plus `move-on`.
- `priority` (integer, default 0), `exclusive` (semantic mutex keys),
  `blockref`, `est_tokens`, `safety_class`
  (`ordinary|spine|gate|attestation|protected|high-risk`) and `planmode`
  (`dual` opts into dual-plan decomposition) are the scheduler's optional
  inputs. `safety_class` **fails closed**: absent reads as `unclassified` and is
  never scheduled, so a repo enables parallelism only after its own audit.
- `order` — a migration artifact written by `wi_convert.py` to reproduce a CSV
  whose row order the ids do not describe. A hand-filed spec omits it and sorts
  after the numbered ones, by id.

**This body is backward-only (rule R-A).** `## Deliverable` stays EMPTY while
the work is open and is filled with what actually shipped when it closes — the
`specref` above is the forward-looking half. A spec whose body is neither empty
nor exactly one `## Deliverable` section is a malformation the readers name by
filename; the long record lives in the body precisely because body text needs no
escaping, so headings, quotes, backticks and blank lines survive verbatim.

**The registry is authoritative; `docs/status.md` is a generated snapshot.**
Execution's *how* atop the spine's *what* — a view, never a source of truth.
