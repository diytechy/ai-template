## 2026-11-06 — Scoped spine rebuild route

Owner-requested retrospective from the FileBackup needs-to-Rust transition.
Prepared on `codex/simplify-spine-resync` at base `ee2b19b9e`, in an isolated
worktree. The active template checkout, coordinator pause, work-item queue,
policies and requirement approvals were not edited.

### Assessment and change

The resync skill was already a router. The pack's historical migration detail
is useful for a full upgrade, but its sole route implicitly coupled a semantic
spine rebuild to whole-kit adoption. The missing piece was scope selection and
a compact end-to-end rebuild sequence, not another migration engine.

[Pack §0](../../project-trajectory/RESYNC_PACK.md#0-choose-the-scope) now owns that
choice and the six-step rebuild recipe. The skill and adoption guide point to it;
the generated skill index and existing agent copies are synchronized. Full-kit
migration ordering and checker behavior are unchanged. No new registry tier,
automation mode, approval mechanism or runtime dependency was introduced.

The recipe keeps the practical lessons: audit reality without making code the
requirements authority; take a coherent, pinned subset of spine tooling; agree
needs, boundaries and assumptions before SRs; reconcile legacy obligations;
review real risks; allocate interfaces, design and tests; then reconnect code.
A partial resync records its own provenance and never advances the whole-kit
stamp. Existing enforced checks and declared approval authority remain binding.

Manual route review covered three requests: tooling-only upgrade selects §1;
stale-spine rebuild selects §0.1; a request for both tracks both outcomes.
This was a local document review, not an independent model evaluation or a new
downstream adoption trial.

### Validation

- Resync regression tests: **38 passed**. <!-- fig: command=C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest tests/test_resync_pack.py tests/test_check_resync.py -q --basetemp D:/review-tmp/2026-11-06-spine-resync/pytest; revision=ee2b19b9e plus this documentation patch -->
- Skill index/copy checks, anchored resync-entry check and `git diff --check` passed.
- The generic Codex skill validator rejects the kit's existing custom frontmatter
  fields; the kit's own skill validator accepts them. The schema was preserved.
- The declared `run_menu.py smoke` command completed its strict trace, trajectory,
  docs and resync-entry steps and exited zero, but its initial test run lacked
  Git's shell on PATH and therefore skipped shell-dependent cases. It also
  reported a CPU-budget warning; no thresholds were changed.
- Re-running the smoke tier with Git's shell available yielded **3388 passed,
  3 skipped, 1 failed** within its CPU/wall budgets. <!-- fig: command=C:/Projects/ai-template/.venv/Scripts/python.exe scripts/check_smoke_budget.py --mode warn; revision=ee2b19b9e plus this documentation patch -->
  The failure was invocation-induced: the session's `PYTEST_ADDOPTS` basetemp
  propagated into a nested collect-only process whose working directory was
  inside that basetemp. Pytest correctly refused it. Removing that environment
  override and passing `--basetemp` directly made
  `tests/test_smoke_budget.py::test_nested_collection_survives_a_non_utf8_console_byte`
  pass on its targeted rerun. No harness or product fix was needed. These are
  separate runs, not a claim of one uninterrupted fully green smoke execution.
- Final pre-commit rerun of the complete declared smoke bar passed with Git
  shell available and scratch on D:, without the inherited pytest option:
  **3389 passed, 3 skipped**, within CPU and wall budgets. <!-- fig: command=C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/run_menu.py smoke; revision=ee2b19b9e plus this documentation patch -->
  This supersedes the earlier partial-run limitation above; the earlier results
  remain as the invocation diagnosis.
- Validation logs remain in `D:/review-tmp/2026-11-06-spine-resync/` for review.

No budgeted master file changed. This is a documentation update; no downstream
registry conversion is required. Deferred open items: none — integration into
the active template branch is left to its ongoing work, not performed here.

The change remains isolated on `codex/simplify-spine-resync`; it has not been
merged into the active template branch or applied to another project.
