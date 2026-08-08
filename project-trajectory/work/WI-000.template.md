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
gates on it, so a fresh scaffold stays vacuously clean. It is inert where it
matters: every loader skips a `-000` id (the same rule that makes the `-000`
row in each registry template inert), so a fresh scaffold's registry reads
empty and nothing gates on this exemplar. That inertness is also why this
example may carry a filled `Deliverable` while sitting in `queued/`, which the
rule below forbids for real work. (Since concurrency-restructure Phase 5 this
folder is the ONE registry home — the CSV form survives only as
`wi_convert.py`'s migration/interchange format.)

**Status is the DIRECTORY, never a field.** One home per fact: the mutable
state is the file's location, the immutable-ish metadata is the frontmatter, and
the narrative is the body.

| Location | Status |
|---|---|
| `docs/work/draft/WI-###-<slug>.md` | `draft` — written down, not claimable |
| `docs/work/queued/WI-###-<slug>.md` | `queued` — filed, unclaimed |
| `docs/work/active/<branch>/WI-###-<slug>.md` | `active` — claimed by that branch |
| `docs/work/deferred/WI-###-<slug>.md` | `deferred` — parked with its reason |
| `docs/work/complete/WI-###-<slug>.md` | `done` — it shipped |
| `docs/work/cancelled/WI-###-<slug>.md` | `cancelled` — it never will |
| `docs/work/partial/WI-###-<slug>.md` | `partial` — it was attempted and stopped short |

Three consequences worth stating, because they are the reason for the shape:

- **`blocked` has no directory.** A blocked item is `queued/` plus a `blockref`
  frontmatter key naming the reason, so a second encoding of "not now" would be
  a second home for one fact. The scheduler derives `blocked` from the key's
  **presence** — it never consults the state of what the key names, so ruling
  an open item or closing a blocking WI does not, by itself, return the row to
  the frontier. **What releases a park is one act: editing the row — deleting
  the `blockref` — in a reviewed commit.** There is no second, automatic route:
  a lane that cannot finish does not write a `blockref` back onto its own spec,
  so no park is ever minted by the loop (see the terminals below). The general
  `blockref` is untouched by that — it stays the one home for "not now, because
  of *that*", and an ordinary blocked row still reads exactly as it always did.
- **A terminal is a move, never a deletion — and each terminal gets its OWN
  directory.** There are three: `complete/` shipped it, `cancelled/` never
  will, `partial/` was attempted and stopped short. Each record stays in the
  registry forever with its reason in this body. They are three folders rather
  than one, because a folder holding two states needs an attribute to tell them
  apart and a validator to keep folder and attribute honest — the shape this
  format deliberately does not have. Neither a `cancelled` nor a `partial`
  predecessor satisfies a successor's hard dependency (neither delivered the
  scope, and neither ever will under that id), so a work item hard-blocked on
  one stays visibly waiting. **An attempted item is never revived in place:**
  the remaining scope of a `partial` is a NEWLY minted work item carrying
  `supersedes` lineage and its own queue-admission verdict. Which is also why
  the attempt's own verdict is not a field here — it is an immutable outcome
  event recorded outside `docs/work/`, so the branch that made the attempt
  cannot restate its own obligation and then report against the restatement.
- **`draft` is the absence of a decision**, where `deferred` is a decision:
  `deferred` says *not now*, `draft` says *still being figured out*. Both are
  never-ready to the scheduler and differ only in what they say. `draft/` is a
  DECLARED status directory rather than a scratch folder for one hard reason:
  specs outside the declared set are skipped by every reader, so they never
  enter the registry — the duplicate-id guard and the dashboard both go blind to
  an id a draft is holding. (The id mint itself reads FILENAMES and is safe
  either way; the declaration is what makes the reservation checked rather than
  incidental.)

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
- `supersedes` / `source_event` — the **lineage** a successor carries: the id(s)
  whose remaining scope it picks up, and the outcome event that produced it. A
  successor to a `partial` attempt states both; ordinary work omits them. They
  are the reason an attempt never needs reviving — the history is a link, not a
  rewritten row.
- `order` — a migration artifact written by `wi_convert.py` to reproduce a CSV
  whose row order the ids do not describe. A hand-filed spec omits it and sorts
  after the numbered ones, by id.

**This body is backward-only (rule R-A).** `## Deliverable` stays EMPTY while
the work is open and is filled when the item reaches ANY terminal — what
shipped, why it never will, or what a stopped attempt actually landed — the
`specref` above is the forward-looking half. A spec whose body is neither empty
nor exactly one `## Deliverable` section is a malformation the readers name by
filename; the long record lives in the body precisely because body text needs no
escaping, so headings, quotes, backticks and blank lines survive verbatim.

**The registry is authoritative; `docs/status.md` is a generated snapshot.**
Execution's *how* atop the spine's *what* — a view, never a source of truth.
