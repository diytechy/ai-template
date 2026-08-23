> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# Deep repository review — 2026-07-17

Scope: the full active repository — portable kit scripts/templates, the
meta-repo's self-adopted requirements spine, tests, hooks, generated-artifact
contracts, dashboard rendering, CI, dependencies, configuration, security,
performance, legal posture, and recent Git history. Excluded as historical
working memory: `docs/log.md`, `docs/archive/**`, `docs/iteration/**`, and the
owner-only `OWNER_SCRATCHPAD.md`. Generated `docs/okf/**`, trace reports, and
`PROJECT_STATE.html` were checked through their generators and representative
rendered output rather than reviewed as independent sources of truth.

## 0. Unfixed items and why

The initial report was committed independently as `6ceb172`. The following
items remain after the fix pass because resolving them requires an owner policy
choice, reconstruction of historical intent, or a separately reviewed
high-risk refactor. They were not quietly converted into speculative changes.

| Item | Final state | Why it remains unfixed |
|---|---|---|
| H3 — coordinator complexity | Deferred to a dedicated decomposition campaign | Splitting the 698-line dispatcher and its state transitions is high-risk architectural work. It needs characterization tests, explicit module boundaries, and independent review; doing it inside a repository-wide cleanup would be reckless. |
| H4 — active WIs whose only specs are archive/log records | Deferred for owner triage | Moving or rewriting WI-060/061/062/063/082 requires deciding whether each old intention is still wanted. The active truth cannot be reconstructed confidently from explicitly ignorable history. |
| H5 — missing license | Needs owner/legal choice | Selecting a license changes downstream rights. No technically “safe default” can substitute for the owner’s distribution decision. |
| M5 — 50 orphan-document warnings after this report | Deferred to a documentation-policy WI | Most warnings are historical reviews or specs. Suppression, new entry roots, or moving them to archive each encode a different retention policy; bulk relinking would merely hide the design question. |
| M6 — weak per-module/transition coverage | Deferred to targeted test WIs | Raising meaningful coverage in `agent_loop`, `trace`, `bootstrap`, `check_docs`, and dashboard rendering requires behavior-specific tests, not low-value line chasing. |
| M7 — Python floor, dependency bands, and CI action generations | Needs compatibility policy | Raising Python above 3.8 or moving CI actions changes downstream runner support. The current bands resolve cleanly and no vulnerability was demonstrated, so this should be a deliberate compatibility release. |
| M8 — stale performance numbers and vacuous smoke timing | Needs a benchmark contract | Meaningful thresholds require named hardware/runner classes, warm/cold rules, and a variance policy. Replacing stale numbers with invented ones would be worse. |
| L1 — historical Git metadata/subjects | Left intact | Rewriting shared history to repair vague subjects or author metadata is destructive and disproportionate; enforce the convention prospectively. |
| L2 — dense/historical active prose | Deferred to scoped editorial work | Broad compression can accidentally weaken normative rules. The lifecycle paragraph touched by H2 was tightened, but a whole-guide rewrite needs separate semantic review. |
| L3 — internationalization policy | Needs product-scope decision | Localization is not currently a stated goal; adding machinery without a downstream requirement would be speculative. |

Confident fixes completed in this pass:

| Finding | Disposition |
|---|---|
| H1 | Added `PlanMode` to the shipped schema; made dual-plan filing header-aware; preserved blank `SafetyClass`/`PlanMode` unless explicitly declared; added modern- and legacy-schema regression tests. |
| H2 | Made `blocked` a first-class validator/process state and made a missing `BlockRef` a hard coherence error. |
| M1 | Fixed text `ready --explain` formatting and added an end-to-end regression test. |
| M2 | Replaced retired `next-wi` requirement text, repaired current lock-test citations, and attached the existing critique evidence to TC-053/054/055. |
| M3 | Added the pinned npm lockfile, so the documented `npm ci` recipe is executable. |
| M4 | Wrapped narrow tab navigation, captured the landing fold before any scroll-inducing click, and recorded the two rendered defects as WI-211/WI-212. |

Final verification after remediation:

- Full G3 gate: **PASS**, all 16 steps; **1,009 passed, 34 skipped**;
  aggregate coverage **90.75%** (85% floor).
- Strict traceability: **25 SN / 66 SR / 76 LLR / 76 TC**, with zero orphan,
  integrity, status, placeholder, schema, component, or interface findings.
- Trajectory: **212 WIs / 200 done**, graph acyclic, strict mode clean.
- Focused changed-surface suite: **217 passed**; Ruff format and lint clean.
- Documentation: **0 broken links**; 50 orphan warnings remain and are listed
  above under M5.
- Render tooling: clean `npm ci` succeeded with **0 vulnerabilities** reported;
  all **36** declared screenshots regenerated; representative 390 px light/dark
  fold and full-page images visually inspected.
- Byte deltas: `AGENTS.template.md` **9,978 → 9,978** (unchanged, 22 B
  headroom); `PROCESS.md` **60,169 → 60,169** (unchanged);
  `PROCESS_OPTIONS.md` **155,819 → 155,536** (**−283 B**).

## 1. Executive summary

This repository has an unusually strong verification culture, but its current
green gate overstates the coherence of the product it is checking. The full G3
gate passed: **1,005 tests passed, 34 skipped, aggregate coverage 90.74%, strict
traceability reported 25 SN / 66 SR / 76 LLR / 76 TC with zero orphans and zero
schema findings, and format/lint/duplicate/privacy/freshness checks all passed**.
The suite is broad, cross-platform, and heavily end-to-end. The architecture and
process are documented far beyond the norm for a template repository.

The most serious defects are contract gaps that the existing checks do not see:

1. The shipped work-item schema omits the `PlanMode` column required to trigger
   the newly verified dual-plan behavior. The dual-plan filer also appends a
   fixed nine-field row to whatever schema it finds, so a successful round can
   publish structurally short CSV rows and omit the safety classification the
   dispatcher requires. Its tests use a legacy nine-column fixture, masking the
   current-schema failure.
2. The template and scheduler support `Status=blocked`, while the authoritative
   trajectory validator and process prose reject it as unknown. A documented,
   runtime-used lifecycle state therefore fails the strict gate.
3. The coordinator remains heavily concentrated after its completed
   “main decomposition” campaign: `agent_loop.py` is over 6,000 physical lines,
   `dispatch_run()` is 698 lines with Ruff cyclomatic complexity 84, and several
   other coordinator functions remain 175–355 lines. The complexity was partly
   moved, not eliminated, and no complexity budget prevents recurrence.
4. Active deferred work still points into `docs/archive/**` and `docs/log.md` as
   its only `SpecRef`. Those areas are declared non-working surfaces and were
   explicitly meant to be ignorable, yet future work cannot be resumed without
   them.
5. There is still no LICENSE in a repository whose documented purpose is to be
   copied into other repositories. This is a real distribution defect, not
   paperwork.

The dashboard is visually solid on desktop in both themes, but the 390 px layout
clips its tab navigation off-screen. The render-critique tool itself is not
reproducible as documented (`npm ci` fails because there is no lockfile), and its
narrow “fold” capture is invalid because clicking the below-fold tab scrolls the
page before the screenshot.

The subsequent fix pass resolved the schema/lifecycle/CLI/evidence/render-tool
defects above. The remaining release-level concerns are the coordinator's
concentration of risk, archive-dependent active work, and the absent license;
all three require deliberate follow-on work rather than opportunistic edits.

The correct posture is not a rewrite. Fix the schema/validator/CLI correctness
defects immediately; repair evidence and stale requirements; make the render
tool reproducible; then run a separately scoped decomposition campaign around
the dispatcher state machine. Do not infer a `SafetyClass`, choose a license, or
rewrite repository history without an owner decision.

## 2. Evidence and method

Primary local evidence (2026-07-17, Windows, Python 3.8.10):

- `python project-trajectory/scripts/check.py --jobs 0` — **PASS**, all 16
  steps; **1,005 passed, 34 skipped, 13 warnings in 293.38 s**; total gate
  elapsed for tests/coverage 333.6 s; **90.74%** coverage.
- `trace.py --strict --no-placeholders --require-verified --strict-schema` via
  the gate — **orphans=0, integrity=0, status-findings=0, placeholders=0,
  schema-findings=0, interface-findings=0**.
- `check_docs.py --stale` via the gate — **0 broken links**, but **48 orphan
  document warnings** and many staleness hints.
- Additional Ruff review rules not in the project gate:
  `C901,PLR0911,PLR0912,PLR0913,PLR0915` — **142 findings**; the largest is
  `dispatch_run()` at complexity 84 / 313 statements.
- AST span census over all product/test Python — largest functions:
  `dispatch_run` 698 lines, `bootstrap.main` 381, `trace.analyze` 360,
  `agent_loop.run_iteration` 355, `agent_loop.main` 326,
  `run_dual_plan_round` 304, and `session_bookkeeping` 298.
- Render matrix: all 36 declared Playwright screenshots (390/1280/1680 px ×
  light/dark × five tabs, plus landing captures) were generated and visually
  inspected. The documented `npm ci` prerequisite first failed with `EUSAGE`
  because no lockfile exists.
- Security review: existing repo privacy sweep passed; additional Ruff `S`
  rules and targeted searches found no committed credentials, unsafe
  deserialization, dynamic `eval`/`exec`, or accidental shell construction.
  The one `shell=True` call is the explicitly documented execution boundary for
  the user's own `[run]` command.
- Git review: 68 of the last 100 subjects use the declared `WI-NNN:` style;
  there are also vague subjects such as `Misc scratch` and `Additional notes`,
  and many recent commits have the author rendered as `/`.

Current dependency facts were checked against primary sources. The compatible
release bands resolve to current patch/minor releases, but Python 3.8 is EOL,
pytest's current major requires Python 3.10+, pytest-xdist's current line
requires Python 3.9+, and GitHub's official examples have moved to checkout and
setup-python v6:

- [Python version status](https://devguide.python.org/versions/)
- [pytest on PyPI](https://pypi.org/project/pytest/)
- [pytest-cov on PyPI](https://pypi.org/project/pytest-cov/)
- [pytest-xdist on PyPI](https://pypi.org/project/pytest-xdist/)
- [Ruff on PyPI](https://pypi.org/project/ruff/)
- [actions/setup-python](https://github.com/actions/setup-python)
- [actions/checkout](https://github.com/actions/checkout)

## 3. Prioritized findings

### Critical

None found. There is no demonstrated remote-code-execution, secret exposure,
data-loss path, or currently failing production gate. The high findings below
are nevertheless release-blocking for a kit that claims its generated scaffold
is copy-ready and internally traced.

### High

#### H1. The verified dual-plan feature cannot be declared from the shipped schema and can corrupt the registry shape

**Location**

- `project-trajectory/registries/work-items.template.csv:1-2` — the header ends
  in `...,EstTokens,SafetyClass`; there is no `PlanMode` column, although the
  example prose and SR-066 require a row to declare `PlanMode=dual`.
- `project-trajectory/scripts/plan_artifacts.py:43-55`:

  ```python
  WI_HEADER = [
      "WI-ID", "Title", "Workstream", "SR-Refs", "Predecessors",
      "Status", "Deliverable", "SpecRef", "BuildTier",
  ]
  ```

- `project-trajectory/scripts/plan_artifacts.py:183-211` appends lists in that
  fixed nine-column order, regardless of the destination header.
- `tests/test_plan_artifacts.py:26-28` deliberately supplies the same legacy
  nine-column header, so the test cannot expose drift against the modern
  template (16 columns) or this meta-repo (10 columns).
- `docs/requirements/system-requirements.csv`, SR-066, and
  `project-trajectory/PROCESS_OPTIONS.md` “Dual-plan decomposition” require the
  missing trigger.

**Problem**

The product contract and the file users copy disagree. An adopter cannot use
the feature without inventing a schema extension. Worse, the selected-plan
filer writes fewer fields than a current registry header, which makes the CSV
structure invalid under `trace.structure_findings`. It also leaves
`SafetyClass` absent, so the dispatcher fails the new children closed. The
docstring's claim that the result passes `check_trajectory.py` is only true for
the outdated fixture schema and ignores the strict trace structure sweep.

**Why it matters**

This is a false green in the newest high-risk orchestration path. A successful
unattended planning round can publish a registry that immediately breaks the
next G3 gate and disables parallel scheduling until a human repairs the rows.

**Suggested improvement**

Add `PlanMode` as an optional, documented template column. Make the filer read
the destination's actual header and append named values in that exact order,
filling unknown/optional fields with blanks. Test against the full modern
template header and run `trace.structure_findings` after filing. Continue to
leave `SafetyClass` blank unless a reviewed plan supplies it—the dispatcher is
correct to quarantine rather than infer safety.

#### H2. `blocked` is simultaneously documented, scheduled, and rejected

**Location**

- `project-trajectory/registries/work-items.template.csv:2` documents
  `Status = queued|active|done|deferred|blocked` and `BlockRef`.
- `project-trajectory/scripts/schedule.py:370-395` explicitly renders blocked
  items and their reason codes.
- `project-trajectory/scripts/check_trajectory.py:153-154`:

  ```python
  OPEN_STATUSES = ("queued", "active", "deferred")
  KNOWN_STATUSES = ("queued", "active", "done", "deferred")
  ```

- `tests/test_trajectory.py:345-352` asserts that `blocked` is unknown.
- `project-trajectory/PROCESS_OPTIONS.md:1433-1436` omits `blocked` from the
  normative lifecycle vocabulary.

**Problem**

The scheduler/runtime migration added a first-class state without updating the
authoritative validator or lifecycle prose. Under `--strict`, a row that follows
the shipped template is rejected; it also escapes the open-WI `SpecRef` check.

**Why it matters**

Downstream users receive contradictory instructions, and the strict gate
penalizes the safer choice of recording a blocker. This is precisely the kind of
cross-file semantic drift the kit claims to eliminate.

**Suggested improvement**

Add `blocked` to `KNOWN_STATUSES` and `OPEN_STATUSES`; require a resolvable
`SpecRef` plus `BlockRef` for blocked rows; update the one normative vocabulary
and tests. Keep deferred distinct: deferred is deliberately not next, while
blocked is live work waiting on a named dependency.

#### H3. The coordinator remains a concentration-of-risk despite the completed decomposition campaign

**Location**

- `project-trajectory/scripts/agent_loop.py` — over 6,000 physical lines.
- `dispatch_run()` at line 3827 — 698 lines, Ruff complexity **84**, 72
  branches, 313 statements.
- `run_iteration()` at line 5514 — 355 lines, complexity 23.
- `session_bookkeeping()` at line 5214 — 298 lines, complexity 29.
- `main()` at line 5871 — 326 lines, complexity 24.
- `run_dual_plan_round()` at line 1176 — 304 lines, complexity 29.
- `bootstrap.main()` at line 1468 — 381 lines, complexity 41 (already deferred
  as WI-082).
- `trace.analyze()` at line 1141 — 360 lines, complexity 50; `render_report()`
  is 281 lines.

**Problem**

WI-080 successfully extracted several seams, but the new dispatcher grew into a
larger state-machine monolith. Nested closures mutate `active`, `parked`,
`retry_at`, `quarantined_wis`, and `needs_human_ask` across reconciliation,
reservation, worker lifecycle, integration, publication, and end-state logic.
The gate runs only Ruff's default rule set, so this regression is invisible.

**Why it matters**

This is the repository's highest-consequence code: it owns Git refs,
worktrees, process spawning, recovery, and publication. Large stateful functions
make transition coverage hard to reason about even when end-to-end coverage is
high. A minor edit can change several lifecycle phases at once.

**Suggested improvement**

Run a separately scoped, behavior-preserving dispatcher decomposition: explicit
`DispatchState` data, pure reconciliation/frontier/end-state reducers, a worker
supervisor object that owns handles, and one integration transaction service.
Add complexity reporting in CI with a deliberately grandfathered baseline so
new regressions fail without forcing an unsafe one-shot rewrite.

#### H4. Active work depends on archive/log material that is declared ignorable

**Location**

`docs/requirements/work-items.csv` deferred rows:

- WI-060 and WI-061 point only into `docs/archive/IMPROVEMENT_PLAN.md`.
- WI-062 and WI-063 point only into `docs/log.md`.
- WI-082 points only into `docs/archive/repo-review-2026-07-12.md`.
- `docs/status.md:12,52` claims every deferred item and its reason live in the
  registry, but the registry has no reason field; those reasons are external.

**Problem**

The repository guide calls the archive “context, not a working surface,” and
the review scope explicitly permits logs/archive to be ignored. Yet five live
deferred items cannot be understood or resumed from active documents alone.

**Why it matters**

This breaks resumability and the stated forward-only design. It also means a
cleanup that correctly archives or prunes history can silently destroy the only
specification of future work.

**Suggested improvement**

Create concise live specs for each still-real deferred WI, including the defer
reason and un-defer trigger, then repoint `SpecRef`. If an item is no longer
valuable, close/remove it rather than retaining a load-bearing archive link.
Do not reconstruct intent automatically from historical prose.

#### H5. No license grants the copying the README instructs users to perform

**Location**

Repository root: no `LICENSE`, `COPYING`, or `NOTICE`; README has no licensing
statement. Tracked WI-097/OI-4 already records the missing owner decision.

**Problem**

Default copyright applies. The documented quick start tells users to copy the
kit into other repositories without granting permission to do so.

**Why it matters**

This undercuts the repository's core purpose and creates legal ambiguity for
every adopter. The kit requires asset-license provenance downstream while not
providing its own.

**Suggested improvement**

Owner decision: declare public/private intent and choose a license (MIT for
simplicity or Apache-2.0 if the patent grant matters), add the file and README
statement, and define whether scaffolded copies retain a notice.

### Medium

#### M1. The documented `schedule.py ready --explain` text path crashes

**Location** — `project-trajectory/scripts/schedule.py:456-460`:

```python
"... {reasons}".format(reasons=";".join(r["reasons"]), **r)
```

**Problem** — `r` already contains a `reasons` key. Passing it again as a named
argument raises `TypeError: str.format() got multiple values for keyword
argument 'reasons'`. Tests cover JSON explain output, not text explain output.

**Why it matters** — This is the documented human diagnostics command for the
new dispatcher. It fails precisely when an operator needs to understand why a
WI is excluded.

**Suggested improvement** — Copy the record and replace its `reasons` value, or
format the joined value positionally. Add an end-to-end text-mode test.

#### M2. Verified requirements and test evidence contain stale or missing truth

**Location**

- `docs/requirements/system-requirements.csv`, SR-055, still requires an
  intake loop containing `docs/next-wi`, although SR-059 requires every live
  dependency on that file to be removed.
- `docs/requirements/low-level-requirements.csv`, LLR-056, and
  `docs/test/test-cases.csv`, TC-056, repeat the retired stage.
- `docs/requirements/stakeholder-needs.md:50-51` cites the deleted
  `tests/test_agent_loop_tracks.py` for SN-017/SN-018.
- TC-053/054/055 are `Verified`, `Automated=No`, but have empty `Evidence`; the
  actual approval exists at `docs/reviews/074-CRITIQUE.md`.

**Problem**

The strict spine validates IDs, schemas, and coverage, not semantic
contradiction or evidence path completeness. “Verified” therefore includes
rows that name retired behavior and manual tests with no recorded evidence.

**Why it matters**

These are the repository's source-of-truth artifacts. If they drift, generated
dashboards and trace reports faithfully amplify the wrong statement.

**Suggested improvement**

Amend the SR/LLR/TC text to the registry-derived resume loop, update test
citations to current files/test nodes, and populate critique evidence paths.
Add a strict-schema rule: a Verified, non-automated TC must have non-empty,
resolvable Evidence.

#### M3. The dashboard render-critique tool is not reproducible as documented

**Location** — `scripts/dashboard-shots/README.md` and skill step 1 require
`npm ci`; `scripts/dashboard-shots/package.json` pins Playwright 1.61.1, but no
`package-lock.json` is tracked.

**Problem** — `npm ci` fails immediately with npm `EUSAGE`. The exact transitive
dependency graph is not locked despite the tool's stated goal of comparable,
pinned renders.

**Why it matters** — The only perceptual verification recipe cannot be
bootstrapped by following its own instructions, and future screenshots may use
different transitive packages.

**Suggested improvement** — Commit a lockfile generated from the exact direct
pin; add a lightweight CI or dev-setup check that `npm ci --ignore-scripts`
can resolve the locked package metadata.

#### M4. Narrow dashboard navigation is clipped, and the narrow fold recipe captures the wrong viewport

**Location**

- Rendered evidence:
  `scripts/dashboard-shots/shots/390px-{light,dark}-arch-fold.png` and all
  390 px full shots.
- `project-trajectory/scripts/gen_trajectory.py:1608-1613`: `nav.tabs` is a
  flex row with neither wrapping nor horizontal overflow behavior.
- `scripts/dashboard-shots/shoot.mjs:91-104`: the runner clicks each tab before
  taking both full and fold screenshots.

**Problem**

At 390 px, the Knowledge/Process tabs extend beyond the viewport and are
cropped. Separately, clicking the landing tab forces Playwright to scroll the
below-fold navigation into view; the alleged fold image begins around the
execution card and omits the actual landing content.

**Why it matters**

Keyboard/mobile users cannot reliably discover all tabs, and the artifact used
to approve mobile first-impression quality is invalid. The prior manual critique
could not have relied on this recipe for the narrow fold claim.

**Suggested improvement**

File and execute separate WIs: make tabs wrap or become an explicitly labeled,
keyboard-operable horizontal scroller; and capture the landing fold before any
click (or activate tabs via DOM state without scrolling). Re-run the full matrix.

#### M5. Documentation warnings have become normalized noise

**Location** — G3 `check_docs.py --stale` reported 48 orphan warnings, including
`docs/iteration_index.md`, `docs/plans/README.md`, approximately 40 review
artifacts, completed specs, and design notes.

**Problem**

The gate is technically green while emitting a screenful of warnings. Many are
historical review/session artifacts that belong under an explicit ignored or
archived policy; others are genuinely unlinked active docs.

**Why it matters**

High-volume accepted warnings train contributors to ignore the checker and hide
new navigability defects. This contradicts the “fails loudly” philosophy even
if warnings are intentionally non-gating.

**Suggested improvement**

Classify the corpus: move true history under the ignored archive/log boundary,
add explicit index links for active plans/specs, and baseline only the residue
that cannot yet move. Make new orphan warnings fail relative to that baseline.

#### M6. Aggregate coverage hides weak modules and transition gaps

**Location** — full coverage report:

- `subagent_gate.py`: 42%
- `gen_cases.py`: 61%
- `plan_coverage_step.py`: 65%
- `gen_release_checklist.py`: 74%
- `agent_loop.py`: 86% despite owning the most complex state transitions

**Problem**

The 85% aggregate floor allows a small, well-covered renderer to offset weak
coverage in permission gating, release logic, and adapters. Some low numbers are
coverage-plumbing artifacts (subprocess tests are present), but the gate cannot
distinguish that from genuinely untested code.

**Why it matters**

Module-local regressions can land while the total remains comfortably above
85%. Complexity plus an aggregate-only target is especially risky in the
coordinator.

**Suggested improvement**

Add per-module floors or a diff-coverage rule for security/orchestration modules;
wire subprocess coverage uniformly for direct hook subprocess tests; add direct
transition tests around the largest uncovered dispatcher branches.

#### M7. Support/dependency policy is deliberate but aging

**Location**

- `requirements-dev.txt` uses compatible bands and currently resolves cleanly.
- `.github/workflows/{test,canary}.yml` still use `actions/checkout@v4` and
  `actions/setup-python@v5`, while official current majors are v6.
- The advertised floor is Python 3.8+, which reached EOL on 2024-10-07.
- Actions are referenced by mutable major tags, not immutable commit SHAs.

**Problem**

No vulnerable package was identified in the four dev-only dependencies, and the
bands sensibly preserve Python 3.8 compatibility. However, the repo is spending
substantial CI effort on an EOL interpreter and carries older action runtimes.
Major tags also leave a broader supply-chain trust surface than SHA pins.

**Why it matters**

The minimum version constrains modern idioms and complicates dependency pins;
older action majors eventually lose runtime support. Mutable tags are a common
CI supply-chain weakness.

**Suggested improvement**

Upgrade official actions after checking hosted-runner requirements, preferably
pinning reviewed SHAs with Dependabot/Renovate updates. Make the Python floor an
explicit next-major decision; Python 3.10 is the clean contemporary floor, while
3.9 is the smallest move that unlocks current pytest-xdist/pytest-cov lines.

#### M8. Performance claims and performance enforcement are stale or vacuous

**Location**

- `CLAUDE.md:47-48`, `docs/status.md:36`, and three session-protocol skill
  copies claim roughly 47 s / 531 smoke cases and 66 s / 684 full cases.
- Current full evidence is 1,005 passed / 34 skipped in 293 s on this machine;
  tests+coverage took 333.6 s and doc navigation alone took 63.2 s.
- `check_perf.py` reports “no performance budgets to compare.”

**Problem**

Volatile benchmark numbers are repeated across working instructions and are no
longer credible. The repository has a performance-budget framework but does not
use it for its own dominant developer costs.

**Why it matters**

Contributors plan commit cadence around timings that are off by several times,
and suite growth has no regression sensor. CI repeats the full suite across five
OS/Python cells and again in the gate job.

**Suggested improvement**

Remove hardware-specific timings/counts from normative instructions or label a
dated benchmark in one place. Add coarse, non-flaky budgets for collection/test
wall time and `check_docs` I/O, and avoid running an identical unmeasured full
suite twice on the same Linux/current-Python combination.

### Low

#### L1. Git discipline is mostly strong but not consistently applied

**Location** — recent history includes `Misc scratch`, `Additional notes`,
`Status hygiene: ...`, and commit authors rendered as `/`; 68/100 subjects use
the declared WI prefix.

**Problem** — The repository's normal WI commits are excellent, but vague
scratch commits weaken bisectability and contradict the contributor guide.

**Suggested improvement** — Require informative imperative subjects for every
commit, even off-WI hygiene, and repair the local commit identity for future
work. Do not rewrite published history merely for cosmetics.

#### L2. Prose is precise but over-dense and too historical in active surfaces

**Location** — `PROCESS_OPTIONS.md` is about 155 KB / 2,093 nonblank lines;
several module docstrings and requirement rows embed WI numbers, owner rulings,
and migration history alongside current behavior. SR-066 alone is a large
multi-paragraph contract compressed into one CSV cell.

**Problem** — The material is accurate in spirit but cognitively expensive.
History and current contract are often interleaved, making it difficult for an
adopter to determine which clause is normative now.

**Suggested improvement** — Keep present-tense contracts in active artifacts;
move rationale/history to logs or linked design records. Split overgrown SRs by
independently verifiable responsibility rather than adding more semicolon
clauses.

#### L3. Internationalization is intentionally absent but should be stated

**Location** — CLI messages, generated HTML, templates, and docs are English
only; the dashboard correctly declares `<html lang="en">`.

**Problem** — This is reasonable for a developer kit, but there is no explicit
non-goal or localization boundary. User-provided Unicode is handled well.

**Suggested improvement** — State that localization is currently out of scope;
continue keeping machine tokens separate from human-facing strings so future
translation remains possible.

### Positive / good practices

1. **Verification is real and broad.** The suite bootstraps actual downstream
   scaffolds, runs scripts as subprocesses, exercises hooks, Git worktrees,
   recovery, rendering, and cross-platform behavior. The full gate was green,
   not inferred.
2. **Traceability mechanics are excellent.** Zero-orphan strict joins,
   placeholder rejection, interface/component checks, derived gates, generated
   status/dashboard/OKF freshness, and an explicit acceptance vocabulary are
   unusually mature.
3. **Security boundaries are mostly honest.** There were no secrets in the
   active tree. Subprocesses generally use argv arrays, HTML is escaped, policy
   files make consent explicit, privacy/secrets checks are integrated with
   hooks, and `shell=True` is clearly disclosed as executing the user's own
   command rather than misrepresented as safe parsing.
4. **Portability is treated as a product feature.** Stdlib-only shipped scripts,
   Python 3.8 syntax discipline, Windows/POSIX launchers, and a Linux/Windows/
   macOS matrix directly support the repository's stated goal.
5. **Generated views usually have one source of truth.** The architecture map,
   trace report, dashboard, OKF bundle, status block, and gate marker are derived
   and freshness-checked rather than hand-maintained copies.
6. **Desktop dashboard quality is good.** Light/dark themes are coherent,
   typography and contrast are strong, status uses text as well as color, graph
   panels provide detail context, and keyboard affordances are present in the
   generated markup.
7. **Dependency scope is lean.** Shipped scripts have no third-party runtime
   dependencies; the four Python packages are meta-repo test tools, and the one
   Playwright dependency is isolated to an optional render harness.
8. **Failure handling is conservative.** The dispatcher uses durable Git state,
   reservations, CAS, quarantines, explicit end-state codes, bounded polling,
   and fail-closed scheduling for unclassified work.

## 4. Overall recommendations and next steps

Recommended order:

1. **Restore correctness of the work-item contract.** Add `PlanMode`, make child
   filing header-aware, cover the modern schema, accept/validate `blocked`, and
   fix `ready --explain` text output.
2. **Repair trace truth.** Amend SR-055/LLR-056/TC-056, current test citations,
   and manual critique evidence; add the non-automated Evidence gate.
3. **Make perceptual QA reproducible.** Commit the Playwright lockfile, correct
   the fold capture, file the mobile-nav defect as its own WI, and rerun/read the
   complete matrix before closing it.
4. **Reduce warning noise.** Move true review/session history to an ignored
   archive class and index genuinely active specs. Gate on new warnings relative
   to a reviewed baseline.
5. **Start a dispatcher-specific decomposition campaign.** Golden transition
   tests first, then state/reducer/supervisor extraction in small commits. Add a
   complexity baseline so the problem cannot immediately regrow.
6. **Resolve owner decisions.** License/public intent; live specs or retirement
   for archive-backed WIs; Python minimum; action SHA policy. These are not safe
   drive-by choices.
7. **Control developer cost.** Remove stale timing promises, establish a dated
   benchmark and coarse budgets, and deduplicate the current-Python Linux full
   suite between the matrix and gate job where evidence is equivalent.

Fitness against the project vision: the kit is demonstrably test-first and
mechanically traced, but it is not yet fully “maintainable and trustworthy” at
its newest orchestration layer. The gate is good at structural integrity and
regression execution; it needs stronger semantic-contract, schema-evolution,
complexity, and evidence-completeness checks to justify the confidence its green
badge currently communicates.
