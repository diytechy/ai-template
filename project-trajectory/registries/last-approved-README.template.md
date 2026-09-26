# `last_approved` — what the spine looked like when a human last blessed it

**This file is prose. Nothing parses it.** Every machine fact about the
snapshot comes from the copied registry files beside it, from the act ledger
`acts.toml` beside them, or from `git log` over this directory. That is
deliberate: a stamp file that grew fields would quietly become a record every
reader depends on without a declared format, so the one typed record of the
approval acts lives in its own file.

## What is in here

Byte-for-byte copies of the requirement spine and the registries that carry
human-only approval cells, at the commit where an approval was last written:

```
docs/requirements/stakeholder-needs.toml
docs/requirements/system-requirements.toml
docs/requirements/low-level-requirements.toml
docs/test/test-cases.toml
docs/requirements/interfaces.toml
docs/requirements/external.toml
docs/requirements/components.toml
```

Beside them, `acts.toml` holds one entry per approval act that copied a
registry, the first signing included: its number, its day, the rows it carried
into approval and the rows it re-attested. An accepted risk is anchored to the
latest act naming its assumption there.

Repo-relative paths are preserved under this root, so `git diff` and an
ordinary text editor are all you need to read it. **If this directory contains
only this README, that is correct and not a gap** — it means this project has
not approved anything yet.

## Why a copy rather than a hash

Every "has this approved row changed?" question is answered by diffing the live
registry against its copy here. A copy is inspectable, needs no generator, and —
because it is a WHOLE FILE — it keeps each row's own `Status` cell. That last
part is what lets the checks catch the failure that matters: a live row claiming
approval whose copy here reads *below* approval is an approval that was written
without copying the text it blessed.

## The one rule

> In any commit that touches a file in this directory, that file must be
> byte-identical to its live counterpart in that same commit.

This README and `acts.toml` have no live counterpart and are exempt by name.

`check_trajectory.staged_snapshot_findings` enforces it. A legitimate copy
satisfies it always; a hand edit, a partial copy, and a copy-then-amend-live all
fail it. **So the only way to write text into this directory is to write it into
the live registry first** — an approval, in a reviewed commit.

## How it is written

Never by hand, and never by the unattended loop. Two callers only:

- `scripts/intake.py snapshot` — the human path. At an approval sitting: edit
  the `Status` cells, run it, and commit both together.
- the mechanical flip inside `intake.py adjudicate`, which copies in the same act
  as the status write.

The FIRST snapshot needs `intake.py snapshot --seed`, which is the only way this
directory is created. Run it once, in the reviewed commit that first blesses the
spine, **after** every pending row has been ruled — seeding it earlier records a
blessing of text nobody read.

This is one generation. It is replaced wholesale at each approval and never
migrated in place; git holds the history.
