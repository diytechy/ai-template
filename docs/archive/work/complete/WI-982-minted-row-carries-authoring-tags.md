+++
id = "WI-982"
title = "Both adjudication routes widen a sitting's hats by the authoring work item's tags: the minted first-approval and amendment rows carry the merged lane's tags"
workstream = "process"
sr_refs = ["SR-161"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

Both adjudication routes now widen a sitting's hats by the authoring work
item's tags. The mint writes a new `AuthoringTags` cell on the first-approval
and amendment rows a naming route mints, deduplicated across the authors it
names, and passes on a minted author's own record. The hat composer reads a
non-empty cell in place of the row's `Workstream` and `SafetyClass`, and an
empty cell reads those two as before. A range sweep with no `--merged` leaves
the cell empty. The routing `SafetyClass` stays `adjudication`. LLR-360 states
the rule by addition and TC-399 verifies it, both re-attested at act seq 172
under `docs/reviews/wi-982/004-ADJUDICATE-f8f3572.md`.

## Context

Filed by hand by headless leg 23 (2026-10-26) at WI-976's landing, from
the SUCCESSOR ruling of WI-976's dispute sitting 004
(`docs/reviews/wi-976/004-ADJUDICATE-81e623b.md`, RB1-F1, accepted; its
duplicate RB3-F1 was dismissed by sitting 010, and the post-rebase round's
REVIEW-B re-raised the same class, `docs/decisions/wi-976.toml` D-028).

What is true: a decomposition round's hats are widened by the tags of the
row the sitting composer is handed. The coordinator's in-lane route hands
it the authoring lane's own row. The unattended route hands it the
merge-minted adjudication row, whose Workstream is always `process` and
whose SafetyClass is `adjudication` (it routes the row), so the authoring
work item's tags are lost and the hat set differs by route. The defect is
in the minted row's provenance, outside WI-976's declared surface.

The ruling, verbatim: "make both routes widen a sitting's parent needs by
the authoring work item's declared tags: carry the merged lane's
Workstream and SafetyClass (in a cell other than the routing SafetyClass)
or a link to it onto every minted first-approval and amendment row,
resolve the branchless sweep, state in LLR-360 that the authoring work
item's tags widen, and add a test that composes the minted row shape and
the in-lane shape for one SR and asserts one hat set".

Its scope critique runs before its claim (the `coordinator-cycle` skill,
section 1).

**Deliverables and order (S1).** Two deliverables, kept together in one
landing on purpose: the mint writing the provenance cell and the composer
reading it, with the paired-shape test. A cell nothing reads changes no
hat, and a reader with no writer reads nothing, so neither lands first.
The ruling's LLR-360 item needs no work: that row already reads "widens
each need by the authoring work item's declared tags", and this row leaves
the clause standing.

**Architectural delta (S5).** No new mode class and no new boundary. The
row adds one cell, `authoring_tags`, to the work-item row
(`wi_convert.COLUMNS`, the schema IF-092 names, in the IF-023 carrier). Its
value domain: the authoring work items' Workstream and SafetyClass values,
deduplicated and `;`-joined, or empty when no authoring item is known. The
ruling's alternative, a link, is not taken: the mint already holds the
rows, so it writes the fact once and a later composition reads that record
instead of looking a row up (rubric B3). `intake`'s two drafters are the
only writers. `hats.context_from_work_item` is the only reader: a non-empty
cell supplies the row's tags in place of its Workstream and SafetyClass,
never beside them, since beside them a minted row would keep `process` and
its FIRST-RUN-ADOPTER hat and the sets would still differ. An empty cell
reads those two cells, as every row does today, so the in-lane route
changes nothing. The output that moves is the hat set, which now depends
on the authoring tags on both routes. The routing SafetyClass stays
`adjudication`.

**Provenance cases (S3).** The cell's source is closed, by the route that
mints:

- The merge slot: the lane's closed row, the one its outcomes name.
- `sweep --merged ... --branch`: the named rows, their tags unioned when
  there are several.
- A range sweep with no `--merged`, with or without `--with-terminal`: the
  branchless case. It knows no authoring item (`--branch` alone only labels
  the commit, and `--with-terminal` holds every close on file), so the
  default applies: the cell stays empty and the row widens by its own tags,
  as a minted row does today. A person who knows the lane gets its tags by
  naming its rows with `--merged`.
- A bare sweep: it reads HEAD..HEAD, so it mints neither row kind.

An authoring row's tags are the ones it widens by itself, so a minted row
that authors another passes its cell on. No route infers a lane from
history. The promise reaches what these routes mint (PROCESS.md §6,
"Review threat model"); a hand-edited cell is outside it.

## Done-when

- [x] Every first-approval and amendment row minted by a route that names
      an authoring work item carries that item's Workstream and
      SafetyClass in `authoring_tags`, a cell other than the routing
      SafetyClass.
- [x] The branchless sweep's case is resolved as "Provenance cases" states:
      a range sweep with no `--merged` leaves the cell empty, its row
      widens by its own tags, and a test pins it.
- [x] Both routes widen a sitting's parent needs by the authoring work
      item's declared tags wherever that item is named, and LLR-360 states
      that it is the authoring work item's tags that widen.
- [x] A test composes the minted row shape and the in-lane shape for one
      SR and asserts one hat set.
- [x] The commit bar is green, and both strict lints are clean on the
      landing tip.

## Critique dispositions

Round 1 (fresh Sol, 2026-11-04): CHANGES-REQUESTED, one MAJOR and three
MINORs.

- **S1, adopted.** The Context now reads "Two deliverables, kept together
  in one landing on purpose", and records that LLR-360 "already reads".
- **S3, adopted.** The unresolved bullet is replaced. "Provenance cases"
  reads "The cell's source is closed, by the route that mints", its
  branchless default reads "the cell stays empty and the row widens by its
  own tags", and its bound reads "The promise reaches what these routes
  mint". The first and third Done-when bullets are narrowed to match.
- **S4, adopted.** The frontmatter reads `planmode = "single"`: the row
  touches the mint and the hat composer, and promises behaviour over the
  mint's routes.
- **S5, adopted.** The delta reads "No new mode class and no new boundary",
  names the carrier's domain ("deduplicated and `;`-joined, or empty when
  no authoring item is known"), its writers and its one reader, and states
  that the hat set "now depends on the authoring tags on both routes".
