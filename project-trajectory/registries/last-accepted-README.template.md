# `last_accepted` — what the spine looked like when an operator last blessed it

**This file is prose. Nothing parses it.** Every machine fact about the
snapshot comes from the copied registry files beside it, from the act ledger
`acts.toml` beside them, or from `git log` over this directory. That is
deliberate: a stamp file that grew fields would quietly become a record every
reader depends on without a declared format, so the one typed record of the
acceptance acts lives in its own file.

## What is in here

Copies of the requirement spine and the registries that carry operator-only
acceptance cells. Each row here is, byte for byte, its live text at the act that
last wrote it: the first signing copies the files whole, and each later act
writes the rows it names (and the rows that follow live) row by row:

```
docs/requirements/stakeholder-needs.toml
docs/requirements/system-requirements.toml
docs/requirements/low-level-requirements.toml
docs/test/test-cases.toml
docs/requirements/interfaces.toml
docs/requirements/external.toml
docs/requirements/components.toml
```

Beside them, `acts.toml` holds one entry per acceptance act that copied a
registry, the first signing included: its number, its day, the rows it carried
into acceptance, the rows it re-accepted, the registries it copied
(`copied`) and the rows it left at their recorded text, owed (`kept`). An entry
written before `copied` or `kept` existed keeps its shape; its copy set is
unknown, and nothing infers one. An accepted risk is anchored to the latest act
naming its assumption there.

Repo-relative paths are preserved under this root, so `git diff` and an
ordinary text editor are all you need to read it. **If this directory contains
only this README, that is correct and not a gap** — it means this project has
not accepted anything yet.

## Why a copy rather than a hash

Every "has this accepted row changed?" question is answered by diffing the live
registry against its copy here. A copy is inspectable, needs no generator, and —
because each row is copied WHOLE — it keeps each row's own `Status` cell. That last
part is what lets the checks catch the failure that matters: a live row claiming
acceptance whose copy here reads *below* acceptance is an acceptance that was written
without copying the text it blessed.

## The one rule

> In any commit that writes a registry's copy in this directory, that copy must
> be the copy the commit's act writes: the previous copy with exactly the rows
> the act names taken from the live registry in that same commit, every other
> row placed by the row rule.

This README and `acts.toml` have no live counterpart and are exempt from the
copy comparison by name; neither may be deleted while the rest of the record
stands. A record written before its first row-by-row act (no `acts.toml` entry
carrying `kept`) is judged as it was written: each copy byte-identical to its
live counterpart in its commit.

`check_trajectory.staged_snapshot_findings` enforces it at the commit, and
`committed_snapshot_findings` on the committed history. A legitimate act
satisfies it always; a hand edit, a copy-then-amend-live, an unnamed row's drift
carried in, a named row copied with an edit and a row dropped that no act
retired all fail it. **So the only way to write text into this directory is to write it into
the live registry first** — an acceptance, in a reviewed commit.

## How it is written

Never by hand. One writer only: `scripts/intake.py snapshot`, run in the
reviewed commit of an acceptance act and committed together with it. It writes
only the registries the act authorises, and in them only the rows the act names
from live, with the rows that follow live (a row claiming no acceptance, or one
whose accepted text and adjudicated links are unchanged). Any other drifted row
keeps its text here, and the command prints it as LEFT OWED:

- **A first acceptance** — move the row's `Status` to `Accepted`, run
  `intake.py snapshot`, and commit both together. (`--accepts <REGISTRY=REF>`
  names a registry the act blesses by an acceptance ref instead.)
- **A re-acceptance** — an amended row still reads `Accepted`, so no flip
  carries it. Read its changed cells, then run
  `intake.py snapshot --reaccepts <ROW-ID>[,<ROW-ID>...]`, naming exactly the
  rows you read. A drifted row that is not yours to bless stays out of the
  list, and keeps its recorded text until its own act.

The FIRST snapshot needs `intake.py snapshot --seed`, which is the only way this
directory is created. Run it once, in the reviewed commit that first blesses the
spine, **after** every pending row has been ruled — seeding it earlier records a
blessing of text nobody read.

This is one generation: a row here is replaced when an act names it, and the
record is never migrated in place; git holds the history.
