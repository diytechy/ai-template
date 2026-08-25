+++
id = "WI-519"
title = "Carry the allow-file parse-honesty arm to the three declared exception readers that drop a malformed line silently"
specref = "docs/plans/2026-08-25-remap-alignment.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by `WI-508`'s alignment pass (the architectural remapping program, slice
3) — the ONE divergence between the blind minimal map and the live layout that
survived having its original rationale read. The program is this row's origin,
not its gate: `WI-508` stays open for its own remaining slices and this row does
not wait on it. The two consolidation lanes the program's spec named as
destinations (`WI-448`, `WI-483`) are both closed-archived, so there is no
parent lane to feed; this row stands on its own in the queue.

### The measurement

Five declared exception files, five separate parsers across four modules:

| file | reader | reports a malformed declaring line? |
| --- | --- | --- |
| `docs/provenance-allow` | `trace.read_provenance_allow` | **yes** — returns `(entries, unparsed)` |
| `docs/kernel-modules-allow` | `check_trajectory._parse_kernel_allow` | **yes** — same shape, by explicit reference |
| `docs/if-tc-coverage-allow` | `check_trajectory.parse_if_tc_allow` | no |
| `docs/declared-absences` | `check_doc_refs.load_declared_absences` | no |
| `docs/need-form-allow` | `check_need_form.load_allow` | no |

Every one of the five drops a line the grammar cannot read — that half is
uniform and correct, and it is the fail-safe direction (a malformed entry grants
no exemption). What is NOT uniform is whether the drop is **reported**.

### Why this is a defect and not a preference — the repo already argued it

`read_provenance_allow`'s own docstring records the reasoning, after the
correction was made there:

> "Fail-soft in the LOUD direction ... a line with no separator, or with fewer
> than three key fields, declares NOTHING and is dropped here, so the worst a
> malformed entry can do is leave a finding reported — **and, since 2026-08-20,
> is REPORTED as dropped**, because the other half of 'declares nothing' is that
> it also COUNTS as nothing, and the arms that reason about how many exceptions
> stand were reading that silence as an empty surface."

`_parse_kernel_allow` then adopted it deliberately, naming the source: "the
whole parse, both halves, the `docs/provenance-allow` split". So the correction
is argued once, adopted twice, and **missing from three readers** — an author
who writes a malformed entry in any of those three gets silence, and any arm
counting how many exceptions stand reads that silence as an empty surface. It is
the same defect, in the same words, in three more places.

### WHAT THIS ROW MUST NOT DO — the flattening the rationale read prevented

**Do not merge the five parsers.** They differ, and every difference is a
recorded decision whose docstring argues it:

- `if-tc-coverage-allow` carries a `# seed-count:` migration baseline whose
  seeded entries share one reason stated in the header;
- `kernel-modules-allow` requires a per-entry reason and says so BY CONTRAST
  with the seed-count file — a reuse provision is "a deliberate recorded act
  every time, never a bare-baseline default";
- `provenance-allow` requires an open-item id as the FIRST TOKEN of the reason,
  a position rather than a mention, and that is a ruled required field;
- `declared-absences` accepts two separators and a `LIFECYCLE:` marker for paths
  whose presence is a legal state;
- `need-form-allow` keeps a token set and deliberately discards the reason.

A single reader would flatten five arguments to buy a few lines, and the
objective this program serves is *calls, not lines*. **Each file keeps its own
grammar, its own required fields and its own fail-safe direction.** What is
shared, and what this row extends, is the ARM: a declaring line the grammar
could not read is surfaced rather than swallowed.

### Done when

1. All five readers can report a dropped declaring line — the three that cannot
   gain the capability, in whatever shape suits each (the two that already have
   it return `(entries, unparsed)`; matching that is the obvious route but is
   not mandated, and neither reader's existing signature needs to change for
   its own callers if a sibling accessor is cleaner).
2. Each of the three has a **consumer** for the new signal: a finding, at the
   severity its own checker already uses. An unwired report is the original gap
   with a better name — the failure mode the spine-authoring rules call "the
   unwired marker" — so a reader that can report and a checker that never asks
   does not discharge this row.
3. Each new finding is DRIVEN by a test that fails without it: a malformed
   declaring line in a temp fixture is reported by name and line number, and a
   well-formed file stays silent. No arm is asserted.
4. The fail-safe direction is UNCHANGED everywhere: a malformed entry still
   grants no exemption. This row makes the drop audible; it must not make it
   forgiving.
5. Nothing is merged, no grammar is changed, and no existing allow file needs
   editing to stay valid — verified by running the full bar on the live tree,
   whose five allow files must all still parse to exactly what they parse to
   today.

### Watch for

- **`check_doc_refs.load_declared_absences` takes a PATH, not a root**, and is
  called from `tests/test_dogfood_sync.py` as well as from the checker — a
  signature change reaches a test module, so prefer an added accessor over a
  changed return.
- **`docs/declared-absences` is read by two consumers** (the doc-reference
  checker and the dogfood scaffold walk). The finding belongs to whichever one
  already owns a reporting surface; do not grow a second.
- The shipped-kit surface: three of the four modules ship, so a new finding
  class reaches adopters. If it does, it wants a `RESYNC_PACK.md` entry.
