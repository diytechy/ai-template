+++
id = "WI-524"
title = "The ten passages with no legal home: delete the eight, correct IF-117 and IF-061 (OI-65 ruled (i))"
specref = ""
workstream = "requirements"
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

All ten rows edited; `contract` over the 135-row registry **40,472 → 40,137
characters (−335)**. No RESTATEMENT or REMAINDER clause was touched, every row
read `Drafted` before and after, and no kit-side file, script or test changed.

**The eight deletions.** `IF-080` loses `concurrency-restructure SS1.2/SS2.3`
(the naming half, "the local integration seam", survives it). `IF-088`,
`IF-089`, `IF-136` and `IF-137` lose their bare `docs/concurrency-v2.md §A…`
citations, and `IF-136` its inline `§A2`, each leaving the seam named in prose.
`IF-127` loses `Imported LAZILY.` — a duplicate, since the row's own `notes`
already says *"the lazy import keeps trace off the import path of the loop
modules that need only this module's other seams."*

Two of the eight resolved to nothing a reader could reach, and were replaced by
what they meant rather than merely cut. `IF-090`'s `enact ruled decision 2`
became *"flip a no-scope-moved spine row to Approved, or recommend only while
the tier is human-held"* — read off `intake.adjudication_action`'s own
docstring. `IF-094`'s `the ruled A1/A8 tables read as constants` became `read as
constants`.

**The two corrections.** Both re-verified against the tree before rewriting,
not against the old cell:

- `IF-117` carried three false claims. `docs/architecture.md` is **absent** —
  retired at WI-455 — so the present-tense *"the committed module map is a
  PUBLIC-API view"* described nothing; *"the sym: tier keeps reading the
  artifact"* is contradicted by `check_doc_refs.load_symbol_oracle`, which
  derives from `gen_arch_map.scan_inventory` and says in its own docstring that
  the committed block it used to parse is retired; and *"41 of this repo's 149
  live LLR rows"* is stale against a registry holding **187**. The cell now
  states the property without the retired artifact and without the stale count:
  the public-API selection drops `_`-prefixed names and module constants, which
  LLR rows name, so answering from it would report real code as missing.
- `IF-061` described a retired dual-write as live. `plan_artifacts._write_spec_rows`
  files into the spec folder and says so — *"the one registry home since the CSV
  retired (concurrency-restructure Phase 5, RULING-4)"* — and
  `docs/requirements/work-items.csv` is absent. The cell now reads
  `(docs/work/queued/ spec files, the one registry home)`.

`trace.py` exits 0, integrity 0. The IF advisory count is **43 before, 43
after**: the eight deletions were each too small to bring an over-ceiling row
under its 500-character ceiling, which is a fact about the ceiling arm, not
about the deletions.

## Context

`OI-65` part 2, ruled (i) on 2026-08-28. WI-522's cleanup could not move these
ten: `rationale`'s declared grammar refuses a citation and deletion was not then
ruled. What the ruling turned on is the split — eight are provenance or
duplication and go, two are rot and are corrected, because deleting a false
claim without writing the true one leaves the cell quieter rather than more
honest.

## Done when

- [x] The eight spans gone from their `contract` cells.
- [x] `IF-117` and `IF-061` state what is true of the tree now, verified against
      the code.
- [x] No RESTATEMENT or REMAINDER clause touched.
- [x] `trace.py` exits 0; advisory counts recorded before and after.
- [x] Commit bar green.
