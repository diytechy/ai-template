ADVERSARIAL REVIEW of a completed build in the repo at c:\Projects\ai-template. Your job is to BREAK it, not to praise it. Assume the implementer was over-confident.

WHAT WAS BUILT (work item WI-527, ruled as open item OI-66 option (a)). A module may now state the contract for each interface seam it declares, beside the code, and a committed freshness-gated document harvests them.

Read these:
- `project-trajectory/scripts/gen_arch_map.py` — `_MARKER_RE`, `_marker_ids`, `_marker_text`, `module_contracts`, `contracts_grammar_findings`, `module_contract_bodies`, `scan_contracts`, `build_contract_reference`, `_contracts_doc_exit`
- `project-trajectory/scripts/check.py` — `staged_divergence` (the tracked-but-absent arm) and the `interface-reference` step
- `project-trajectory/scripts/check_trajectory.py` — `_contracts_grammar_findings`
- `project-trajectory/scripts/trunk_step.py` — the `interface-reference` regen step
- `tests/test_gen_arch_map.py` — the tests at the end of the file
- `docs/interface-reference.md`, `docs/stack.ini` `[generated]`, `project-trajectory/hooks/pre-commit`
- `project-trajectory/PROCESS.md` section 8, `project-trajectory/RESYNC_PACK.md` (the newest entry), `project-trajectory/registries/interfaces.template.toml`
- `docs/decisions-for-review-2026-08-29.md` — the decisions the implementer took alone
- `docs/log.d/2026-08-29-wi527-contract-header.md` — what it claims it did

FIND, in priority order:

1. **CORRECTNESS BUGS.** Construct inputs that make the parser wrong: a docstring that declares a seam the harvester misses, or harvests one it should not; a contract body that is silently lost, merged, truncated, or mis-attributed; a way to corrupt the generated Markdown. Actually try them against the code and report what you ran. A claim without a reproduction is worth less.

2. **FALSE GREENS.** Any path where the gate passes while the thing it guards is wrong or absent. The implementer added a tracked-but-absent arm to `staged_divergence` — try to defeat it. Try to make the interface reference stale while `--check` stays green. Consider: prefix rows, symlinks, case-insensitive filesystems, a repo where git is unavailable, `[arch-map] mode = files`, a scan root that is a file.

3. **ADOPTER BREAKAGE.** The `Contracts:` marker grammar was tightened on a SHIPPED kit. Find a legitimate declaration form, plausible in a real downstream repo, that used to work and now silently declares nothing AND is not caught by `contracts_grammar_findings`. That combination is the failure that matters.

4. **CLAIMS THAT DO NOT HOLD.** The log fragment and the decisions document make specific factual claims (counts, "0 findings on this tree", "proved to fire", "closed for the whole kit", "no adopter loses a declaration in silence"). Check them. Say which are overstated.

5. **WHAT THE TESTS DO NOT COVER.** Name the untested path most likely to bite.

Rules: verify before asserting; run the code. Rank by severity with a concrete reproduction for each. If something is fine, say so briefly rather than padding. Do not edit any file.
