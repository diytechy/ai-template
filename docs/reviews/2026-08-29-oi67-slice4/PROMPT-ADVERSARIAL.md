ADVERSARIAL REVIEW of a completed build in the repo at c:\Projects\ai-template. Your job is to BREAK it, not to praise it. Assume the implementer was over-confident. Do NOT edit any repository file; run whatever you like read-only (the repo's Python is `.venv/Scripts/python.exe`, run from the repo root), and put every reproduction you attempt in your answer. A claim without a reproduction is worth less than a reproduced one.

WHAT WAS BUILT (work item WI-531, OI-67 slice 4, "the split"). The interface registry `docs/requirements/interfaces.toml` must now read ONE ROW = ONE OWNER, ONE DIRECTION, ONE KIND (the ruling: `docs/log.d/2026-08-29-oi67-ruled-a.md`; the plan of record: `docs/plans/2026-08-29-if-row-shape-plan.md` §1, §3 "Slice 4", §4 decisions 7 and 8). This slice:
- MINTED twenty rows, IF-145 .. IF-164, each split from a row that described two kinds (a request and its answer, a read and a write, a CLI and the file it writes) or from a bundled medium (docs/test/, docs/agents-enabled, docs/status.md, docs/log.d/ each get their own owner row). Every new row's `Contract IF-###:` body was written into its owner's header (a module docstring, a `#` header, a README's HTML comment).
- COLLAPSED two duplicate pairs: IF-127 into IF-075 (`trace.reattest_model`) and IF-116 into IF-101 (the watermark pair) — same owner surface, differing only in requestor.
- RE-MEASURED the far sides slice 3 found stale (IF-050, IF-053, IF-046, IF-090, IF-102, IF-037) and corrected three channels (IF-012 bytes->exit-code, IF-069 stdout->exit-code, IF-081 bytes->exit-code).
- Re-pointed the generated-document rows IF-019/IF-074/IF-140 from "the written artifact" to the reader class `external:downstream adopter` with a B-05 tie-back.
- Re-pointed TC-161's `verifies` from IF-127 to IF-075; pruned IF-075 and IF-116 from the seam-TC allowlist's seed (120 -> 118) and added twenty reasoned entries for the new rows; exempted `README.md` from `trunk_step.fragment_paths` so `docs/log.d/README.md` can be the directory's declaration home.
- Bumped the id watermark; regenerated the interface reference, CLI reference, component view, dashboard, status block, derived stage, open-items view and approval brief.

Read these:
- `docs/requirements/interfaces.toml` — every row; compare each `[interface.IF-1(4[5-9]|5[0-9]|6[0-4])]` block against the code its owner names.
- `docs/reviews/2026-08-29-oi67-slice4/slice4-worklist.json` and the three `slice4-report-*.json` — what was decided and what the workers measured.
- `docs/reviews/2026-08-29-oi67-slice4/slice4-fold.py` — the fold that wrote the registry.
- `docs/interface-reference.md` — the harvested bodies; `docs/if-tc-coverage-allow` (the additions past the seed); `tests/test_trajectory_arch.py` (`SEEDED_IF_TC_ALLOW`); `project-trajectory/scripts/trunk_step.py` (`fragment_paths`); `docs/test/test-cases.toml` (TC-161).
- `project-trajectory/scripts/trace.py` (`interface_findings`, `tieback_findings`, `if_carriage_advisories`), `project-trajectory/scripts/check_trajectory.py` (`_owner_exact_findings`, `_declared_seam_pairs`, `if_tc_coverage_findings`, `if_tc_allow_hygiene_findings`), `project-trajectory/scripts/gen_components.py` (`seam_placement`).
- `docs/log.d/2026-08-29-wi531-if-row-split.md` — what it claims it did.

FIND, in priority order:

1. **A ROW THAT LIES.** For each new or edited row: does the owner's code actually do what the body and the `data` cell state? Are the exit alphabets right (run the CLIs; read `main()`)? Is the far side the MEASURED set — grep the tree for every requestor/consumer named and for readers/callers NOT named? Is the channel right (the harness reads a return code, never stdout, for every checker step — check `check.py`)? A `requestors` row whose far side actually READS, or a `consumers` row whose far side actually WRITES, is a finding.

2. **A KIND STILL BUNDLED, OR A SPLIT THAT WENT TOO FAR.** Find a row that still describes two kinds (a request and its answer; a read and a write; a CLI and its file) that the slice did not split, and say which. Find a minted row that is NOT a distinct kind of its parent (a duplicate under another id). Judge the collapses: is IF-127 really the same surface as IF-075, IF-116 as IF-101?

3. **FALSE GREENS.** Run `.venv/Scripts/python.exe project-trajectory/scripts/trace.py --root . --strict` and `.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --root . --strict`. Then break things and see what stays green: change a new row's owner to a module that does not declare it; delete a new row's body from its header; make a new row name both `requestors` and `consumers`; point IF-164's owner at the wrong module. Does the seam-TC promotion still bite for a NEW uncited seam after the allowlist grew by twenty — plant IF-199 with no allow entry and check `--strict` reds. Does the pruned seed pin still catch a swap?

4. **THE README EXEMPTION.** `trunk_step.fragment_paths` now skips `README.md`. Try to make it skip something it should compile, or compile the README. Case-insensitivity on Windows (`readme.md`, `README.MD`)? A README committed as a fragment before this change?

5. **CITATION ROT.** IF-127 and IF-116 no longer exist. Grep the whole tree (docs, registries, tests, scripts, generated files) for the two ids and classify each hit: a record (log, review, archive — fine), a live cell that should have been re-pointed (a finding), a test pin, a generated file that should have been regenerated.

6. **THE RECORD vs THE TREE.** Every number in the log fragment (rows minted, rows collapsed, the registry's row count, the reference's summary line, the allowlist counts) — recompute it and report any that does not reproduce.

Report as a severity-ranked list: `[CRITICAL|MAJOR|MINOR]` — location — what is wrong — the reproduction you ran — the concrete change. End with one line: `VERDICT: APPROVE` or `VERDICT: CHANGES-REQUESTED findings=N`.
