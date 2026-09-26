# Builder brief — the assumption tier's build

**Status: WORKING BRIEF**, the one text every builder session of the
[assumption tier's build](../handoff-2026-09-26.md) is handed, with its work
item, its worktree and its pre-assigned interface ids. It records the
conventions the first builds surfaced, so each builder does not rediscover
them. The integrator's procedure around it is in the handoff.

You build ONE work item of this kit, test-first, in your own git worktree.
The repository is a meta-project: a requirement-traced process kit
(`project-trajectory/`) whose own scripts are **stdlib-only Python 3.11+ on
Windows and POSIX**. Read `CLAUDE.md` first. Do only your work item's scope.

## Your spec of record

- Your work item: `docs/work/queued/WI-<n>-*.md` (its Context and Done-when).
- The APPROVED spine rows it names, which are the contract: the SRs
  (`docs/requirements/system-requirements.toml`), design rows
  (`docs/requirements/low-level-requirements.toml`: `module`, `code_symbol`,
  `detail`) and test cases (`docs/test/test-cases.toml`: `method`, `tier`,
  `evidence`). Read them in full before anything else.
- Decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md` §4 and §6
  (D-numbers). D21: pure rules live beside the checker (`frame_rules.py` for
  frame and need-tier rules, `assumption_rules.py` for assumption-tier rules),
  never in `trace.py`, which grows by composition lines only. D31: each Smoke
  test case sits in a fast in-memory module, each Full one in a module
  registered as slow.

## Test-first, and prove it

1. Write every test case's test at its `evidence` path, one test per clause of
   its `method`. A `tier = "Smoke"` case goes in an in-memory module (no
   scaffold, no subprocess, no git); a `tier = "Full"` case goes in a module you
   add to `tests/conftest.py`'s `SLOW_MODULES` (with a one-line reason
   comment), because the per-commit tier selects by module.
2. Run them and RECORD the red result (the pytest summary line) BEFORE writing
   the implementation. A test that passes before the code exists must be one
   that asserts a vacuous case; say which.
3. Implement until green. Run only your own test modules and the modules your
   change directly affects (e.g. `tests/test_trace.py`,
   `tests/test_dogfood_sync.py`, `tests/test_rule_sync.py`,
   `tests/test_bootstrap.py`, `tests/test_module_size_ratchet.py`,
   `tests/test_complexity_ratchet.py`, `tests/test_resync_pack.py`) with
   `python -m pytest -q -n 4 <modules>`. Do NOT run the whole suite or the
   whole smoke tier: other builders share this 8-core machine, and the
   integrator runs the full bar on the merged result.

## Conventions the checks enforce (each one bit the first build)

- **`Implements:` back-links.** Every symbol a design row's `code_symbol`
  names carries `Implements: SR-###, LLR-###` in its docstring; a module-level
  constant gets a `# Implements: ...` comment on the line directly above it.
  Every `code_symbol` must exist in its `module`.
- **New seams need an interface row.** A new module another module imports, a
  new file a module writes or reads, a new CLI: add a Drafted row to
  `docs/requirements/interfaces.toml` using ONLY the IF ids pre-assigned to you
  (below), with `owner`, `requestors` or `consumers`, `channel`, `data`,
  `version = "v1"`, `status = "Drafted"`, `component`, and `rationale`/`notes`
  written as the argument with no work-item id, date or ruling citation in
  them. Put a `Contracts: IF-###` marker and a `Contract IF-###:` body in the
  owning module's header (see `project-trajectory/scripts/frame_rules.py` and
  `trace_text.py`). `check_trajectory.py --strict` ERRORS on a seam no test case
  cites: add the IF id to the `verifies` list of the test case that exercises
  it (`verifies` is a traced pointer cell, so it re-opens no attestation).
  Then run `python project-trajectory/scripts/trace.py --bump-ids`.
- **Never edit an approved row's attesting cells** (requirement, rationale,
  acceptance_criteria, need, why, acceptance, detail, method, expected, level,
  tier, status). Traced pointer cells (`verifies`, `module`, `code_symbol`,
  `test_refs`, `sr_refs`) may move when the build needs it; report each one.
  If an approved row is wrong or impossible as written, STOP that part and
  report it: the fix is an amendment and an adjudication, not an edit.
- **Shipping.** A new kit script or registry template goes in
  `bootstrap.MAPPING` (`project-trajectory/scripts/bootstrap.py`), in
  `tests/test_bootstrap.py`'s file list, and in `project-trajectory/README.md`'s
  kit-contents table. A registry schema change keeps the dogfood three-leg rule
  (`tests/test_dogfood_sync.py`: template keys == the schema in
  `kitlib/spine.py`; live keys are a subset of it) and the carrier's column maps
  a bijection (`spine_carrier.OFFSPINE_COLUMN`/`SPINE_COLUMN` against
  `migrate_carrier.KEY`, pinned by `tests/test_rule_sync.py`). This repository's
  `docs/process.toml` `[checks]` keys must EQUAL the template's
  (`tests/test_rule_sync.py`), and `docs/stack.ini` must declare every template
  section.
- **Adopter note.** A schema, template, CLI or step change gets an entry in
  `project-trajectory/RESYNC_PACK.md`, inserted directly before
  `## 5. Promotion: when this pack stops being prose`, titled
  `### <what changed> [since <the short SHA of your worktree's base commit>]`,
  opening with `*(Anchored at the preceding commit: the change lands in the
  commit after it.)*`, then **What changed.** and **What to do.** paragraphs.
- **Size and complexity ratchets.** `tests/test_module_size_ratchet.py` pins
  exact code-line counts per large module; `tests/test_complexity_ratchet.py`
  pins function complexity. Prefer decomposition into a sibling module. Where
  growth is the composition the design prescribes, re-stamp the entry and
  prepend a reason in the established style (`+N (old -> new) <date>,
  WI-<n>: <why>. Reviewed bump, reason in
  docs/log.d/2026-09-25-assumption-tier-build.md. Earlier: ...`).
- **Style.** `ruff format` and `ruff check` clean on every file you touch.
  Match the surrounding code's comment density and voice: docstrings explain
  WHY. No new dependency.
- **Do not touch** `docs/status.md`, `docs/log.md`, `docs/log.d/`, the work
  item spec, or generated artifacts (`PROJECT_STATE.html`, `docs/stage`,
  `docs/open-items.html`, `docs/ratify/CURRENT.md`, `docs/interface-reference.md`,
  `docs/cli-reference.md`, `docs/requirements/components.derived.toml`,
  `docs/test/report.md`). Freshness failures on those in your worktree are the
  integrator's to clear. Never run `intake.py` mint/sweep/snapshot or
  `integrate.py claim`, never approve a spine row, never push.

## Before you finish

Run in your worktree: your modules plus the affected ones (above),
`python project-trajectory/scripts/trace.py --strict-integrity`, and
`python project-trajectory/scripts/check_trajectory.py --strict`. Then COMMIT
your change on your worktree's branch in one commit, subject
`WI-<n>: <imperative summary>`, body explaining the why, ending with the
trailer `WI: WI-<n>` and
`Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.

## Your final message (the integrator reads only this)

- The worktree path and branch name, and the commit SHA.
- Files changed, one line each.
- The red run (per test module: the pytest summary line before the code) and
  the green run after, with counts.
- Every traced cell you moved on an approved row; every IF id you used.
- Deviations from the spec, anything you could not do, anything in an approved
  row you believe is wrong, and any finding outside your scope. Be exact and
  never claim a result you did not see.
