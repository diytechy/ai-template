# WI-953 disposition: the partial close of WI-902 (lane wi-902)

Judged from the lane's report, WI-902's spec, and the commit facts. I checked the facts myself over `41375927dc..144fbd662a`.

**1. The claimed outcome is right: PARTIAL.** WI-902 asks for the record-at-close rebuild: ten deliverables across the close, the record's cell, a per-commit check, the sweep, the parser, a shared module, the prompt, the recipes, a RESYNC entry and the mint's lineage corrections, with their spine sittings. The range holds nine commits, and every changed path is under `docs/`:
- the single plan and its one revision;
- critiques 1 and 2;
- the plan cap's dispute findings and its FIX verdict (016);
- two telemetry commits;
- decision D-011.

No code, test or spine row changed, so no Done-when item was delivered. The lane stopped where the coordinator cycle says a single plan stops: at its cap, with a FIX that only the owner may take. Its records are real inputs to the continuation, so the close is neither complete nor a cancellation: the owner has since ruled that the work proceeds.

**2. The keep/discard split is honest.** The keep list names all nine commits in the range, and the discard list is empty. Nothing in the range is left on trunk unaccounted for, and nothing the report calls kept is outside it. Every kept commit is a record (plan, critique, findings, verdict, decision, telemetry). None touches code or a registry, so none can break the declared bar. The lane decided the split itself, which a partial close may do.

**3. The successor is drafted.** One successor, in this row's own `## Dispositions` section, carries `supersedes = "WI-902"`. It keeps WI-902's scope unchanged by pointing its `specref` at the closed spec, and follows the owner's route (coordinator-2026-10-20 D-008):
- a third plan revision that carries sitting 016's FIX: record admission admits the close's exact inbound relinks through `spec_move.exact_relink`, with the record/request, parent-tree and close-shape validation and the peel unchanged, and the real-close regression added;
- one confirming critique in convergence stance;
- then the build.

It stays `planmode = "single"` and `buildtier = "medium"`. What is left is the row's whole build at the size its filing estimated, and the plan fork is already decided, so it is not a dual-plan design question.

**4. Nothing is human-owed now.** The owner has already ruled the route, so the successor carries no `[open_item]` gate. It is ordinary queued work whose first step is the plan revision.

No findings: the claim, the split and the remaining scope all hold as the lane reported them.

OUTCOME: PARTIAL successors=1
