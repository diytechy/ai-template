Reviewed: fd5acbf580483cfad2b7253a638259677332b885

Verified. This is a full-lane review in the convergence stance, over the diff 8c03d504f...fd5acbf with the brief's excludes, read against the WI-969 spec (its carried WI-902 spec of record), PROCESS.md and the registry rows the diff cites. I read no verdict, decision, critique or lane commit message.

Failure classes hunted first:
- A record landing without the close (fail-open). The staged hook form, the slot rider and the squash walk all refuse every non-close record change, removal or request rewrite. Moving a requesting spec into complete/ without a record is refused. A merge is judged by what neither parent carried. A close-shaped commit is validated in its parent tree, so an `M` edit to the adopted row in the same commit cannot launder it.
- Silent wrong lineage. The sweep re-points only from a record equal to the request, with the disposed id read from the title token, and it never reads the adopted row's state or git history.
- Silently dropped drafts (data loss). Fences are now paired at column zero before any block is read.

Pre-fix evidence (convergence): I exported the base tree 8c03d504f (git archive, under my area), dropped in the lane's tests/test_intake.py, tests/test_handback.py and tests/test_disposition_adoption.py, and ran the regression tests. They fail on pre-fix code for the right reasons:
- An unclosed draft after a valid one: the close succeeds (`['WI-401'] is None`) and the sweep mints nothing.
- An unreadable merged spec: the sweep returns no refusal.
- A title collision on another lineage: no refusal.
- A drafts-only or mixed replay: the late dependent keeps WI-005.

The commit-check tests cover a new module, so they cannot be red against a pre-fix file.

Done-when map:
- Close accepts and records, plus each refusal (missing, complete, cancelled, not-utf8, unparseable, other-lineage, no-supersedes, untokened title, repeated, consolidation, draft beside an adoption): tests/test_handback.py adoption block and tests/test_consolidate_close.py::test_a_consolidation_verdict_that_adopts_refuses_the_close.
- Commit check, passes and every listed refusal: tests/test_adoption_record.py (real repos, lanes, squashes, shallow parent).
- Sweep (full successor set with drafts, a late dependent, after the successor completes, a shallow clone, the four request/record mismatches, an unreadable spec): tests/test_intake.py.
- Parser, review 015's reproduction at the close and at the sweep, for an adoption and for a draft: covered.
- Trunk census: test_every_dispositions_section_in_the_repository_passes_the_fence_grammar. My own parser probe over every docs/work and docs/archive/work spec found no fence refusal, only three pre-existing archived open_item-shape refusals.
- RESYNC entry: one entry, anchored at trunk 8c03d504f, naming the three tightenings, no forced migration.
- Recipes §3 and §8 updated and synced.
- `adopts` is not in `_DRAFT_KEYS`.
- Back-links (K3): every new Implements tag names an LLR whose module holds the file and whose code_symbol lists the function.

UNCOVERED at this tip, process-owed rather than a code defect: the spine-adjudication item. LLR-335, LLR-345, TC-360, TC-383, IF-294, IF-303 and IF-304 are Drafted. SR-148, LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254 carry amended text under Approved, with re-sit evidence outside this reading scope. The sitting and act must discharge both before the landing.

trace.py rewrote docs/test/report.md; the worktree stayed clean (git status empty).

Commands:
- `git rev-parse HEAD` -> fd5acbf580483cfad2b7253a638259677332b885
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../g1b/wi-969 tests/test_disposition_adoption.py tests/test_adoption_record.py tests/test_intake.py tests/test_handback.py` -> 261 passed in 304.90s (0:05:04)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (966 work item(s), 850 done (88%), 34 cancelled, graph acyclic). exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=134 LLR=312 TC=338 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2. exit 0
- `python project-trajectory/scripts/trace.py --strict` -> the same Traceability line, exit 0
- pre-fix probe: the lane's new regression tests run on the exported 8c03d504f tree (`-k "unclosed or indented or replay or title_match or unreadable_merged or full_successor_set or nothing_left"`) -> 17 failed, 1 passed (draft-path failures as stated above)
- probe/census.py: `intake.parse_disposition_section` over every tracked docs/work and docs/archive/work spec containing "\n## Dispositions" -> no fence refusal; 3 archived open_item-shape refusals, pre-existing
- probe/broken.py (a real git repo) -> `commit_adoption_record_lines` on a commit that only writes a queued spec with a cp1252 title byte (no record or request anywhere) -> `WI-010: 'utf-8' codec can't decode byte 0xe9 ...; only `handback.close_adjudication` writes the record; close the row through it`. The same happens for invalid TOML front matter. The fixing commit after it -> []

Findings:

- [MINOR] project-trajectory/scripts/adoption_record.py:305 -> `_spec_refusal` reads the head copy of every touched spec strictly before it asks whether a record question is live (moved, changed or recorded). A lane commit that only writes an unreadable or unparseable spec, with no record or request in any tree, is therefore refused by the slot rider. That covers an as-is residue commit later fixed, which `_commit_residue_as_is` makes with `--no-verify` by design. Because the walk judges history, the refusal is permanent, and line 250 attaches REMEDY ("close the row through handback.close_adjudication"), which names the wrong cure. Confirmed by running (B1), probe/broken.py. -> Read the head copy through `_base_spec`'s tolerant reading unless the spec moves into complete/ or a parent recorded: an unparseable spec carries no record that any consumer trusts, since the sweep refuses it. At minimum, report a read failure without REMEDY. (The remedy removes strictness and adds no guard.) -> @owner
- [MINOR] project-trajectory/scripts/adoption_record.py:397 -> `staged_adoption_record_lines` and `_squash_walk` repeat in intent `text_then_act.staged_text_then_act_lines` and `_squash_lines`. Both resolve HEAD, MERGE_HEAD and the SQUASH_MSG tip, run the is-ancestor test and walk rev-list HEAD..tip. The second copy also walks commits outside the one `lane_commit_walk`. Its stated reason, an import cycle, exists only because text_then_act imports adoption_record to register the rider (PROCESS.md §3, consolidate, don't duplicate). -> Extract the shared stage (the staged commit's bases plus the squash's lane commits) into one home beside `_commit_parents`, parameterized by the per-commit rule and each rule's own exemption predicate. Compose `LANE_COMMIT_RIDERS` where the slot consumes it, so neither rule module imports the other. -> @owner
- [MINOR] docs/test/test-cases.toml:1463 -> for clarity (K1): TC-147 (line 1463) and TC-156 (line 1562) Expected cite "LLR-335's single-lineage operation", but neither verifies LLR-335. TC-147, TC-156 and TC-254 (line 2647) now verify SR-148, yet their Expected still names only SR-174, SR-144 and SR-220. -> Name the SR-148 clause each one discharges, and either add LLR-335 to the verifies of a TC that cites it or drop the citation. -> @owner
- [MINOR] tests/test_disposition_adoption.py:266 -> the Done-when census picks files by the exact heading `^## Dispositions\s*$`. The production parser reads the first "\n## Dispositions" prefix, so the close, the sweep and the commit check would parse a section under a decorated heading (for example "## Dispositions (round 2)") that the census never judges. My parser-level probe shows the claim holds today, but the instrument is narrower than the Done-when it pins. -> Select census files with the parser's own partition, `"\n## Dispositions" in text`, so the census and the parser agree on which sections exist. -> @owner

VERDICT: APPROVE findings=4
