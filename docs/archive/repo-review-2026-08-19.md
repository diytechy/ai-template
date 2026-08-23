> **ARCHIVE** — design history as of 2026-08-19; not current guidance.

# Repository Review — 2026-08-19

Review target: `ai-template` at commit `2b867c0f` on branch
`requirements/ears-and-quality-characteristics`.

## Executive summary

This repository has unusually serious verification machinery for a reusable
project template: a 2,588-test suite, cross-platform CI, source-derived
traceability and architecture checks, explicit security/privacy gates,
full-SHA-pinned Actions, high measured coverage, and strong licensing. The
requirements spine is structurally coherent (`orphans=0`, no schema or
integrity errors), the full test suite passes, and the generated dashboard has
real keyboard, contrast, and responsive-design tests. These are material
strengths, not ceremonial process.

The central problem is that the machinery is no longer trustworthy as a whole.
The most severe defect is architectural: the shipped gate uses the least-mature
artifact as its global strictness selector. Adding one ordinary draft
requirement to a mature downstream project can therefore disable formatting,
lint, tests, and coverage in CI. Verification gets weaker when planning changes
are introduced. That is the opposite of a monotonic regression floor and
directly contradicts the project's promise of explicit gates "you can trust."
The root repository partly masks this with a separate pytest matrix, but its own
lint step is currently red and is not enforced at the current gate.

The implementation has also outgrown its claimed script-oriented architecture.
Seven major modules form a strongly connected component hidden behind deferred
imports. Seven scripts exceed 2,000 lines; `trace.analyze` alone is 514 lines at
cyclomatic complexity 50. The supposed independent-script directory is now a
59-module library graph held together by sibling `sys.path` injection, private
facade imports, mutable attribute bags, and known duplicated plumbing. Size and
complexity ratchets record the debt, but the size ratchet points to a completed
work item rather than a live owner.

The authored contract and the enforced contract have drifted in several places.
The shipped interface documentation teaches fields and values that the schema
rejects; the root README calls the mandatory depth-0 boundary frame optional;
and its commissioned-versus-shipped ledger overclaims the hat evidence record
while underclaiming the need-form checker. The strict architecture checker also
fails today on an undeclared `hats -> spine_carrier` seam. Meanwhile, normative
prose says every interface is backed by a contract/fixture test, yet 115 of 125
live interfaces have no TC citation and that condition can never fail a gate.

The project is recoverable without a rewrite. Its pure modules, test harness,
registry integrity, source-derived checks, and explicit debt records provide a
good base. The next program should first make quality gates monotonic, then
repair the current strict failures and adopter-facing documentation, then split
the cyclic orchestration graph behind typed, dependency-neutral contracts.
Adding more ratchets without paying down or assigning the current baselines
would only document deterioration more precisely.

### Overall assessment

- Fitness for stated goals: **partially fit, with a critical gate-design flaw**.
- Runtime/deployment security: **low exposed surface** (shipped Python is
  standard-library-only), but development dependency and privacy automation
  need work.
- Reliability: **strong test breadth, unreliable gate selection**.
- Maintainability: **poor in the central orchestration and trace subsystems**.
- Documentation/requirements: **strong structure, materially inconsistent
  adopter-facing semantics**.
- Accessibility: **better than typical and explicitly tested**, with a serious
  current dashboard information-density/layout defect.
- Internationalization: **explicitly a non-goal**, reasonably justified because
  machine tokens must remain locale-stable.
- Release readiness: **not ready** while the strict architecture check and lint
  are red and the gate can suppress regression checks.

## Scope and method

The review covered live code, tests, workflows, configuration, shipped
templates, root and kit documentation, requirements registries, generated user
surfaces, dependency metadata, and recent Git history. Logs and archive material
were excluded as requested. `docs/log.md`, `docs/log.d/**`, `docs/archive/**`,
iteration logs, and historical completed/cancelled records were not reviewed
except for narrow references needed to verify whether a finding already had an
owner. `OWNER_SCRATCHPAD.md` was deliberately not read. Generated historical
records were sampled rather than treated as normative prose.

The live-scope inventory contained approximately 1,119 tracked files after
those exclusions, including 183 Python files and 816 Markdown files. The shipped
`project-trajectory/scripts/` surface contains 59 Python modules.

Review techniques included:

- three independent specialist passes for architecture, executable/tests, and
  documentation/requirements;
- AST analysis for import strongly connected components, function lengths,
  complexity baselines, annotations, and module sizes;
- full and targeted pytest runs, Ruff lint/format checks, coverage inspection,
  shell and PowerShell parse checks, and dependency consistency checks;
- strict trace, trajectory, hats, vocabulary, need-form, privacy, documentation,
  reference, vendoring, and performance checks;
- rendering 30 dashboard screenshots across 390/1280/1680 px, light/dark
  themes, and the What/When/How/Process views;
- Git object-size, generated-file churn, and recent commit-subject review;
- current dependency/advisory lookup for the installed development toolchain.

### Verification snapshot

| Check | Result |
|---|---|
| Full pytest suite | **PASS** — 2,588 passed, 13 skipped in 628.85 s |
| Smoke suite on the default Windows environment | **FAIL** — UTF-8 decode failure in nested collection; 24 tests also environment-skipped because Git's POSIX shell was not on `PATH` |
| Smoke suite with Git shell on `PATH` and UTF-8 mode | **PASS** — 1,203 passed, 5 skipped in 62.34 s |
| Ruff format | **PASS** — all files in each invoked scope were formatted |
| Ruff lint | **FAIL** — 6 errors plus one malformed `noqa` warning |
| Coverage | **PASS** — 93% overall; all three committed module floors pass |
| `trace.py --strict` | **PASS** — 27 SN, 72 SR, 161 LLR, 157 TC; 0 orphans, 0 integrity findings |
| `check_trajectory.py --strict` | **FAIL** — undeclared cross-component `hats -> spine_carrier` import; many advisory gaps |
| Documentation links | **PASS with warnings** — 0 broken links; status size/staleness warnings |
| `hats.py audit --strict` | **PASS** — 27 needs, 16 hats, 0 unknown tag tokens |
| Need form / retired vocabulary | **PASS** |
| Configured secrets scan | **PASS** |
| `pip check` / `npm audit` | **PASS** / 0 npm vulnerabilities |
| Performance gate | **VACUOUS** — no live performance-budget registry to compare |

## Prioritized findings

## Critical

### C-01 — A normal draft requirement can disable established tests, lint, format, and coverage in shipped CI

**Location**

- `docs/gate:3-16` explicitly defines strictness as the minimum across all
  in-scope artifacts and says one Drafted/Modified row drops a mature spine to
  what a fresh scaffold displays.
- `project-trajectory/scripts/check.py:572-576` schedules `format`, `lint`, and
  `tests+coverage` only for `BAR_RELEASE` (`DevStg-Impl`).
- `project-trajectory/ci/check.yml:66-89` runs pushes and pull requests through
  `check.py` at the currently derived gate.
- `.github/workflows/test.yml:118-123` claims the root gate enforces format,
  lint, tests+coverage, traceability, privacy, documentation, performance,
  flows, and architecture.

Relevant code:

```python
return [
    ("format", _requires(fmt_cmd), fmt_cmd, {BAR_RELEASE}, "product"),
    ("lint", _requires(lint_cmd), lint_cmd, {BAR_RELEASE}, "product"),
    ("tests+coverage", _requires(test_cmd), test_cmd, {BAR_RELEASE}, "product"),
]
```

**Problem**

Artifact maturity and regression assurance are represented by one reversible
global value. When a mature product adds a new draft need or requirement, the
minimum drops. In the shipped downstream workflow, that lower value removes all
product-code checks from both push and PR plans. The repository's own current
state demonstrates the practical effect: the full pytest matrix is green, Ruff
has six real findings, and the stage-aware gate does not care because it is at
`DevStg-Reqs`.

**Why it matters**

This is a silent-green failure in the system whose purpose is to prevent silent
green. New planning work is routine; it must not suspend regression detection
for already-built code. Downstream repositories use the shipped workflow and do
not have the root meta-repository's independent full-pytest matrix to soften the
damage. A breaking implementation change can be merged while CI truthfully
reports green under the wrong scope.

**Suggested improvement**

Separate two axes:

1. artifact-maturity checks selected by the current phase; and
2. a monotonic product regression floor that never falls after a project first
   configures or clears it.

Persist the highest cleared product bar, or infer the always-on floor from the
presence of configured product commands/code. Continue using the minimum
artifact state to select requirements-specific checks, but always run already
adopted format, lint, tests, coverage, secrets, and build checks. Add a shipped
CI regression fixture: start with a mature repository, add one Drafted row, and
assert that all established product checks remain in the plan. Correct the root
workflow comment so it describes actual enforcement.

## High

### H-01 — The advertised launcher selects unsupported Python and ignores a valid project environment

**Location**

- `README.md:38-43` requires Python 3.11+.
- `agent-resume.cmd:93-114` and
  `project-trajectory/scripts/agent-resume.template.cmd:73-91` accept any
  runnable `python` or `py -3`.
- `agent-resume.sh:86-95` and
  `project-trajectory/scripts/agent-resume.template.sh:68-74` do the same for
  `python3`/`python`.
- `tests/test_bootstrap.py:787-803` inspects launcher text and inert template
  slots, but does not execute interpreter selection against old/new candidates.

**Problem**

The launchers neither prefer `.venv` nor probe `sys.version_info`. On this
workspace, ambient `python` is 3.8.10 while `.venv` is 3.11.9. The advertised
entry point chooses the ambient interpreter and
`python project-trajectory/scripts/agent_loop.py --help` immediately fails with
`ModuleNotFoundError: tomllib`.

**Why it matters**

The one-command unattended coordinator is the product's front door. A common
multi-Python installation breaks it even though the repository has a valid
environment ready to use. Text-inspection tests create false confidence.

**Suggested improvement**

Prefer the repository's `.venv` interpreter. Probe every fallback candidate
with `sys.version_info >= (3, 11)` before selection, return a precise diagnostic
listing rejected candidates, and apply the same policy to `check.*` launchers.
Execute launcher tests with fake old/new interpreters and with a valid venv plus
an invalid ambient `python`.

### H-02 — Seven runtime modules form a dependency cycle hidden by deferred imports

**Location**

- `project-trajectory/scripts/dispatch.py:87-93` imports `handback`, `intake`,
  `integrate`, and `lane`.
- `project-trajectory/scripts/handback.py:55-75` imports `integrate` while its
  prose claims integration never imports back.
- `project-trajectory/scripts/integrate.py:2174-2197,2331-2340` lazily imports
  `handback` and `intake`.
- `project-trajectory/scripts/intake.py:1042-1054,1695-1702` lazily imports
  `dispatch`.
- `dispatch.py:746-770` imports `gen_trajectory`; that facade imports
  `traj_panels` at `gen_trajectory.py:117-121`; `traj_panels.py:8-21` imports
  `integrate`.

The AST import graph contains this strongly connected component:

```text
dispatch <-> handback <-> integrate <-> intake
    |                                  ^
    +-> gen_trajectory -> traj_panels -+
    +-> lane ---------------------------+
```

**Problem**

The coordinator, merge service, handback, intake, lane management, and dashboard
are not layered services. They are one cyclic subsystem. Lazy imports avoid
initialization crashes but do not remove coupling. The comments have already
drifted far enough to assert a dependency direction the code violates.

`dispatch._pending_cards` compounds the problem by calling private presentation
functions `_blocked_pending` and `_spine_pending`; IF-088 documents the bad
edge rather than removing it. `gen_open_items.py:33-41,64-69` likewise imports
the large facade for a state query.

**Why it matters**

Every lifecycle change has a large blast radius, import order becomes part of
behavior, isolated tests require broad monkeypatching, and the dashboard can
drag mutation coordinators into read-only rendering. Extending or substituting
one service is unnecessarily dangerous.

**Suggested improvement**

Extract dependency-neutral modules for work outcomes, terminal-state enums,
registry-gap parsing, and pending-action queries. Return typed values from those
modules. Make `dispatch` the top-level composer; keep `integrate`, `handback`,
`intake`, and `lane` one-way lower services; make views depend only on read
models. Add an import-layer/SCC test that includes imports inside function
bodies so deferred imports cannot hide regressions.

### H-03 — The current repository fails its own strict component-architecture check

**Location**

- `project-trajectory/scripts/hats.py:84-97,479-495` imports and consumes
  `spine_carrier`.
- `docs/requirements/low-level-requirements.toml:1683-1693` assigns the carrier
  to CMP-006; `:1708-1717` assigns hats to CMP-008.
- `docs/process.toml:142-143` enables the architecture checks.

Strict output:

```text
ERROR: cross-component import scripts/hats (CMP-008) ->
scripts/spine_carrier (CMP-006) has no declared IF-### seam
```

**Problem**

A live cross-component dependency has no declared interface. No queued/partial
work item or pending open item names this exact edge.

**Why it matters**

The source-derived architecture map is a primary governance control. Shipping a
known-red strict check trains contributors to discount it and makes every other
architecture claim provisional.

**Suggested improvement**

Either declare a consuming IF owned by LLR-168 and cite the relevant contract
test, or correct the component assignments if the partition is wrong. Do not
allow the strict trajectory job to remain advisory after correction.

### H-04 — “Every interface has a contract test” is normative prose but not an enforceable property

**Location**

- `project-trajectory/PROCESS.md:1095-1110` and `README.md:197` say every
  interface is backed by an SR and contract/fixture test.
- `project-trajectory/PROCESS_OPTIONS.md:2177-2188` and
  `project-trajectory/scripts/check_trajectory.py:1014-1017` deliberately keep
  interface coverage warn-only at every gate.
- The current strict run reports **115 of 125** interface seams cited by no TC.

**Problem**

The normative assurance claim and the executable gate describe different
systems. `--strict` cannot turn this class into an error at any stage, and the
90%+ gap has not converged through warnings. No current work item owns the
115-seam backlog as a whole.

**Why it matters**

Interfaces are where this highly coupled system most needs focused tests. A
contract that is only prose is easy to break during the planned decomposition,
and reviewers are being told a stronger guarantee than the repository provides.

**Suggested improvement**

Choose honestly. Prefer promoting missing TC citations to errors from
`DevStg-Tests` onward, with a time-bounded migration allowlist. If that is not
the intended standard, rewrite “every interface” as explicit guidance and stop
presenting interface test coverage as gated architecture.

### H-05 — Core orchestration is far beyond maintainable review scale, and its debt owner is closed

**Location**

Seven scripts exceed 2,000 lines:

| Module | Lines |
|---|---:|
| `trace.py` | 4,438 |
| `check_trajectory.py` | 4,058 |
| `agent_loop.py` | 3,162 |
| `bootstrap.py` | 2,859 |
| `agent_common.py` | 2,608 |
| `integrate.py` | 2,541 |
| `check.py` | 2,096 |

The worst functions include `trace.analyze` (514 lines, complexity 50),
`check.steps` (494 lines), `agent_loop.main` (402 lines, complexity 27),
`plan_runner.run_dual_plan_round` (333 lines, complexity 31), and
`agent_loop.session_bookkeeping` (325 lines, complexity 31). The committed
complexity baseline contains 46 functions above 10 and 11 at 20 or higher.

`agent_loop.py:1832-1836` defines `LoopContext` as an empty class, then populates
roughly 38 mutable fields at `:3106-3143`. `trace.py:2963-2973` does the same
with empty `Registries` and `Findings` classes. `agent_common.py:2-20` combines
exit codes, Git state, config/policy reads, locking, work-registry parsing,
preflight, logs, and telemetry.

`tests/test_module_size_ratchet.py:1-24` directs active size debt to WI-280,
but `docs/work/complete/WI-280-bounded-core-decomposition-characteriz.md:11-17`
shows that completed item covered the dashboard and `bootstrap.main`, not the
remaining baseline.

**Problem**

These are not merely long files. Central functions combine parsing, policy,
classification, filesystem access, subprocess control, mutation, and rendering.
Dynamic attribute bags erase invariants at exactly the highest-risk seams.
Ratchets stop growth but neither improve the baseline nor assign it to live
work.

**Why it matters**

Reviewers cannot reliably reason about a 514-line decision engine with dozens of
implicit fields. Small changes have broad side effects, type/name mistakes fail
late, parallel contributors collide, and tests become the only documentation of
shape.

**Suggested improvement**

Open successor decomposition work by responsibility, not raw line count. Start
with pure finding producers around `trace.analyze`, typed immutable configuration
plus explicit mutable runtime state for `LoopContext`, and typed registry/result
objects. Split policy decisions from effects. Do not turn WI-448 into a larger
generic `common.py`; create small themed modules with clear ownership.

### H-06 — Shipped interface documentation teaches schema fields and values that strict validation rejects

**Location**

- Source/enforcement: `project-trajectory/registries/interfaces.template.toml:67-75,89`
  and `project-trajectory/scripts/trace.py:471-492` define
  `Status = Drafted|Approved` for IF/EXT/B/REL rows.
- `project-trajectory/PROCESS.md:1094-1100,1125-1126` calls the field
  `Approval` and uses `drafted|approved`.
- `project-trajectory/INTERFACES.template.md:22,31-48` specifies an
  `Approval` column with `draft|approved`.
- `project-trajectory/specs/README.template.md:27-38` and
  `project-trajectory/specs/WI-000.template.md:33-39` tell adopters to use
  `Status=Proposed`; dogfood copies repeat this under `docs/specs/`.
- `project-trajectory/KICKOFF_PROMPT.md:143-146`, `EXAMPLE.md:495-516`,
  `MULTI_REPO.md:163-168,277-281`, and
  `docs/registry-machinery-reference.md:653-655,716` retain `Stable` and/or
  `Approval` vocabulary.
- `README.md:201` describes CMP `State`, whereas the implemented model uses
  `Status`, `Standing`, and `SupersededBy`.

**Problem**

This is systemic schema drift across canonical, scaffolded, example, kickoff,
and reference surfaces. A reader who follows the documentation will create
invalid rows or make release decisions using fields that do not exist. The
drift survived the completed shipped-documentation sweep and passing sync tests.

**Why it matters**

This repository is a template: incorrect instructions multiply into every
downstream project. The contradiction also damages confidence in the claim that
human prose and machine enforcement describe the same playbook.

**Suggested improvement**

Run one reviewed vocabulary migration across every listed live surface. The
registry maturity field is `Status: Drafted|Approved`; reserve `Proposed` only
for plan-coverage notation. Generate schema reference tables from the TOML
templates/enforcement constants, or add a cross-document contract test that
uses one shared schema definition. Do not maintain this vocabulary manually in
ten places.

### H-07 — Documentation calls the required depth-0 boundary frame optional and omits it from the product map

**Location**

- `README.md:140-141,188-196` says only the four spine registries are required
  and describes off-spine registries as optional; the main diagram at
  `:147-173` omits EXT/B/REL.
- `project-trajectory/PROCESS.md:501-505,535-540` requires every project to
  enter `DevStg-Boundary` and produce `requirements/external.toml` before SRs
  form around crossings.
- `project-trajectory/registries/system-requirements.template.toml:18` requires
  SR `boundary_refs`.
- `project-trajectory/scripts/bootstrap.py:1647-1648` always installs the
  boundary frame.
- `project-trajectory/PROCESS.md:25-32` and
  `project-trajectory/README.md:15-40` omit it from their minimum/full inventory.

**Problem**

The process and scaffolder treat the external frame as mandatory; the front
door tells adopters it is optional and visually erases it.

**Why it matters**

An adopter can reasonably skip the artifact required by the stage ladder and
write system requirements without identifying observable boundary crossings.
That undermines the repository's stated order: frame the system, then partition
and specify it.

**Suggested improvement**

Use three consistent categories everywhere: required spine; required depth-0
frame (off-spine but not optional); optional layers. Add EXT/B/REL to the root
diagram, minimum profile, and kit inventory. Keep interfaces optional only where
the project truly has no multi-component seam.

### H-08 — The root README's commissioned-versus-shipped ledger is false in both directions

**Location**

- `README.md:118-133` says the SN-036 machine-readable record shipped and says
  the SN-033 need-form checker remains owed.
- `project-trajectory/scripts/hats.py:12-18` explicitly says only hat injection
  exists; the per-decomposition evidence record is not built.
- `docs/status.md:86-88` lists that record as follow-up work.
- SN-036 acceptance at
  `docs/requirements/stakeholder-needs.toml:269-274` requires the record and a
  missing-perspective check.
- The need-form checker is delivered and wired at
  `project-trajectory/scripts/check.py:638-658`, documented at
  `project-trajectory/README.md:54`, and traced by SR-150 at
  `docs/requirements/system-requirements.toml:580-588`.

**Problem**

The front door overstates a major traceability promise and understates an
existing control.

**Why it matters**

Adopters and reviewers cannot tell what the kit actually guarantees. In a
requirements-centric project, a false delivery ledger is a product defect, not
a cosmetic README typo.

**Suggested improvement**

State that SN-036 roster/injection shipped while the evidence record and
missing-perspective gate remain owed; mark the SN-033 checker shipped and
warn-first. Prefer deriving this ledger from requirement states and cited
evidence rather than manually maintaining narrative counts.

### H-09 — Large-scale duplicated plumbing is accepted but no longer bounded

**Location**

- `tests/test_rule_sync.py:11-40` accepts duplicated plumbing and relies on
  behavior pins for known duplicated policy rather than maintaining a census.
- `docs/work/queued/WI-448-common-module-inversion.md:3` records an initial
  consolidation slice across roughly nine files that removes about 650 lines.
- Repeated declared-line readers exist at `agent_common.py:113`,
  `bootstrap.py:1065`, `check_privacy.py:161`, `check_trajectory.py:261`, and
  `subagent_gate.py:87`.
- Work-item loaders are duplicated at `schedule.py:477` and
  `check_trajectory.py:668`.

**Problem**

The original “independently copyable scripts” rationale has expanded into broad
duplication of registry, configuration, Git, and policy mechanics. Equality
tests can pin copies the maintainers already know about, but do not discover new
copies or semantically close implementations that drift differently.

**Why it matters**

Bug fixes and vocabulary migrations require multi-file sweeps, which is exactly
how the schema documentation and status vocabulary drift accumulated. The
queued work item itself confirms the duplication is substantial, not stylistic.

**Suggested improvement**

Prioritize WI-448, but organize the result as a small copied package with themed
modules (`registry`, `config`, `git`, `station`, `views`) rather than one more
generic common file. Keep directly executable CLI wrappers thin. Make bootstrap
copy the package atomically and test the complete dependency manifest in real
scaffolds.

## Medium

### M-01 — The default Windows smoke bar can crash while decoding its own nested pytest output

**Location**

`tests/test_smoke_budget.py:44-57` runs nested collection with:

```python
proc = subprocess.run(
    [sys.executable, "-m", "pytest", "--co", "-q", "-m", "smoke"],
    capture_output=True,
    encoding="utf-8",
)
return sum(1 for line in proc.stdout.splitlines() if "::" in line)
```

**Problem**

On the default Windows environment used for this review, a child emitted a
CP-1252 en dash in an environment-skip message. The UTF-8 reader thread raised
`UnicodeDecodeError`; `stdout` became `None`; the test then failed with
`AttributeError`. The run ended with 1 failed, 1,178 passed, 29 skipped. Adding
Git's POSIX-shell directory to `PATH` avoided the skip message and the full suite
passed, but that hides rather than fixes the decoder bug.

**Why it matters**

The documented per-commit bar fails on an ordinary Windows setup for reasons
unrelated to product behavior. Environment-dependent output must not be capable
of crashing the harness that reports the environment limitation.

**Suggested improvement**

Run the child in UTF-8 mode explicitly (`PYTHONUTF8=1`/`-X utf8`) or decode with
the child's actual encoding and a deliberate error policy. Add a regression
test whose nested collector emits a CP-1252-only byte. Keep the missing-shell
skip visible as a separate, actionable diagnostic.

### M-02 — The physical script topology no longer represents the linked implementation

**Location**

- `project-trajectory/scripts/` has 59 Python modules and no `__init__.py`.
- There are 33 sibling-directory `sys.path.insert` sites; representative ones
  are `agent_loop.py:145-165`, `check_trajectory.py:154-167`,
  `gen_trajectory.py:83-110`, and `plan_briefs.py:79-98`.
- `spine_carrier.py:29-45` concedes that “independently copyable” now means
  copyable with declared siblings.
- The executable import census found 173 internal-import occurrences across 36
  importing modules.

**Problem**

The directory presents independent scripts while behaving as a library graph.
Imports depend on path mutation, package boundaries cannot express the four
declared components, and private names are treated as cross-module APIs.

**Why it matters**

The topology makes cyclic dependencies and missing bootstrap dependencies easy
to introduce. Static analysis, IDE navigation, and normal Python import rules
are all weakened.

**Suggested improvement**

Preserve thin direct CLI wrappers, but move reusable code into a stdlib-only
package copied downstream as a unit. Use package-relative imports and public
entry points. Align subpackages with actual responsibilities/components, then
enforce allowed dependency directions.

### M-03 — One unbounded work-item title makes the rendered dashboard largely unusable

**Location**

- `project-trajectory/scripts/gen_trajectory.py:754-773` concatenates every
  active WI's entire title into `.sub.nowat` with no length or disclosure rule.
- `gen_trajectory.py:372-380` places Definition and Execution in equal-height
  grid cells.
- The active WI-455 title contains a long program narrative rather than a
  concise title.

**Problem**

Across the 390, 1280, and 1680 px screenshot matrix, the Execution card expands
to thousands of vertical pixels. Its Definition sibling becomes a matching
empty slab. On mobile, the orange active text dominates several screens before
the user reaches the navigation or project model. At desktop widths, half the
landing area is blank while the other half is an unreadable wall of prose.

The sticky header (`gen_trajectory.py:354-358`) also overlays content during
long-page scrolling/full-page capture, and fixed graph label sizes
(`--nlabel:10px`, `--nsub:8.5px` at `:316-321`) are difficult to read in the
dense DAG views.

**Why it matters**

The dashboard is the primary state summary. A single malformed or overlong data
cell can destroy its hierarchy, responsive behavior, and scanning utility.
This is both robustness and accessibility: users with magnification or narrow
screens pay the worst cost.

**Suggested improvement**

Enforce a concise WI title at registry validation, with long rationale in the
deliverable/body. Defensively truncate the hero title behind the same native
`details/summary` disclosure already used for “Next work.” Set grid items to
start rather than stretch, constrain the active summary's measure, and retest
keyboard focus/zoom at 200% and 400%. Reconsider 8.5 px graph sublabels or offer
a textual table as a co-equal view.

### M-04 — Living specifications are too dense to review reliably and carry migration history in normative cells

**Location**

- `project-trajectory/PROCESS_OPTIONS.md` is 2,563 lines / about 25,612 words.
- `project-trajectory/README.md` is about 8,464 words in 170 lines, including a
  roughly 2,060-character table row at line 94.
- `docs/requirements/system-requirements.toml:559-561` gives SR-148 a
  1,067-character requirement, 2,798-character rationale, and 1,763-character
  acceptance cell.
- SR-140's rationale at `system-requirements.toml:468-472` is roughly 4,944
  characters of prior-design and adversarial-review chronology.

**Problem**

Standing rules, rejected alternatives, migration history, review argument, and
implementation detail are packed into giant cells and table rows. This violates
the repository's own cell-hygiene principle that rationales carry the durable
reason rather than a change log.

**Why it matters**

These formats are poor diff and review surfaces. Important contradictions hide
inside walls of text, always-loaded agent context grows, and one edit creates a
large conflict domain. The stale schema words surviving a dedicated docs sweep
are evidence of the practical limit.

**Suggested improvement**

Move chronology to decision/log/archive evidence and keep normative cells to the
standing rule, durable reason, and concise acceptance predicates. Split
independently failing acceptance conditions into lower-tier rows. Replace mega
tables with terse indexes linking focused sections. Retain explicit waivers,
but do not let a waiver become a home for multi-page prose.

### M-05 — The module-size safeguard is itself a 1,746-line, duplicate-key-prone monolith

**Location**

- `tests/test_module_size_ratchet.py` is 1,746 lines and about 169 KB for one
  test.
- The baseline declares `"bootstrap.py"` twice at lines 1275 and 1283.
- Python silently keeps the latter value, so pytest passes; Ruff reports F601.

**Problem**

The control intended to prevent architecture drift silently overwrites one of
its own entries. Extensive historical commentary has turned a small baseline
into one of the repository's hardest files to review.

**Why it matters**

A safeguard that cannot detect duplicate keys is not self-defending. Its size
also raises the likelihood of merge mistakes and obscures the current bound.

**Suggested improvement**

Move the compact current baseline into duplicate-rejecting TOML or generate it
from a small declarative source. Keep only present rationale adjacent; Git and
WI records already preserve historical deltas. Add a test that parses the
baseline through a duplicate-detecting loader.

### M-06 — Several test modules are too large for effective navigation and parallel ownership

**Location**

- `tests/test_integrate.py`: 3,495 lines / 130 tests.
- `tests/test_trace.py`: 1,826 lines / 80 tests.
- `tests/test_agent_loop.py`: 1,567 lines / 63 tests.
- `tests/test_trajectory_arch.py`: 1,412 lines / 64 tests.
- `tests/conftest.py`: 988 lines.

**Problem**

Individual tests are generally bounded and well named, but subsystem-level files
have become test monoliths. There is no equivalent organizational sensor for
test-file growth.

**Why it matters**

Large files slow discovery, produce conflict hotspots, and blur behavioral
ownership even when each test is good.

**Suggested improvement**

Split by stable behavior rather than arbitrary size: claim/refresh/integration/
unload; trace loading/analysis/rendering; loop routing/session/bookkeeping; and
architecture inventory/contracts/rendering. Keep shared fixtures narrowly
scoped rather than expanding `conftest.py` further.

### M-07 — Current lint is red, including a defect inside an architecture control

**Location**

Ruff reports:

- `project-trajectory/scripts/trace.py:4040` — three unused tuple names;
- `tests/test_hats.py:174` — E731 lambda assignment;
- `tests/test_module_size_ratchet.py:1283` — duplicate dict key;
- `tests/test_trace_rules.py:11` — unused import;
- `tests/test_stage_ladder.py:41` — malformed `noqa` warning.

**Problem**

The default lint step is not green. Most findings are small, but the duplicate
key is semantic and is invisible to pytest. The current gate treats lint as
advisory because of C-01.

**Why it matters**

The repository's standards are demonstrably not enforced at the stage where it
does most requirements work. This normalizes red quality signals.

**Suggested improvement**

Fix the six findings immediately, then make lint part of the monotonic regression
floor. Keep the weekly canary for future tool compatibility, but do not rely on
it for current-branch hygiene.

### M-08 — Live requirement-to-code anchors contain stale and pseudo-symbol references

**Location**

`check_doc_refs.py` identifies live registry anchors that do not resolve:

- LLR-015 at `docs/requirements/low-level-requirements.toml:156-164` cites
  nonexistent `trace.py::budget_findings`.
- LLR-087 at `:863+` cites removed `gen_trajectory::_drill_svg` and
  `_drill_edges`.
- LLR-088 at `:874+` cites removed `_descend` and `_breadcrumb` names.
- LLR-112 at `:1095+` uses descriptive prose (`emitted querySelectorAll
  wiring; tabindex + native-link emission`) as though it were a code symbol.
- Draft LLR-172 at `:1753+` cites not-yet-built `component_findings`.

**Problem**

The repository's primary spine is structurally joined, but some precise
implementation anchors are stale or never were valid symbols. The checker also
produces enough record/log noise that these live errors are easy to miss.

**Why it matters**

Reviewers following a supposedly exact `CodeSymbol` link cannot find the
implementation. During refactoring, false anchors make coverage look stronger
than it is.

**Suggested improvement**

Repair the four standing anchors and mark future symbols explicitly as planned
rather than resolvable. Route the checker to live normative registries by
default, with separate opt-in historical scans, and promote live CodeSymbol
resolution at the appropriate gate after the known OI-42 audit work lands.

### M-09 — The architecture declaration parser creates false “undeclared interface” warnings

**Location**

- `project-trajectory/scripts/gen_arch_map.py:233-246` harvests IF identifiers
  only from the exact line containing `Contracts`.
- `project-trajectory/scripts/dispatch.py:72-77` places `Contracts:` on one line
  and IF-088/IF-089 on continuation lines.

**Problem**

The strict run says IF-088 and IF-089 are undeclared even though the docstring
visibly declares them. The grammar is implicit and line-fragile.

**Why it matters**

False warnings dilute real architecture errors such as H-03 and encourage
contributors to ignore the report.

**Suggested improvement**

Define and parse an indented continuation grammar, or enforce all identifiers on
the marker line with a lint rule. Add a multiline regression test and fail on
ambiguous declarations.

### M-10 — A structurally dead “red TC” feature remains shipped with a stale adjudication prompt

**Location**

- `project-trajectory/scripts/dispatch.py:846-872` explains that
  `_TC_NOT_RED = {approved, drafted, modified}` covers the entire conforming TC
  status vocabulary, so `red_tc_census` is unreachable for valid rows.
- `tests/test_adjudicate_brief.py:211-225` uses an invalid `Implemented` status
  to keep the path testable.
- `project-trajectory/prompts/adjudicate-red-tc.template.md:3-33` still defines
  red as status not `Verified`, a retired state.

**Problem**

The code openly retains a dead feature pending an owner ruling, and its tests
prove behavior only by constructing schema-invalid input. The live prompt still
describes the superseded state model.

**Why it matters**

This is “clever” residue: substantial census/mint/prompt machinery appears live,
but conforming repositories cannot reach it. Future maintainers must reason
about a branch that should not exist, and a schema regression could accidentally
reanimate it.

**Suggested improvement**

Resolve the recorded decision promptly. Delete the feature and invalid-fixture
tests, or re-arm it using actual executable test evidence rather than a status
that no longer exists. Do not retain unreachable production paths as decision
placeholders.

### M-11 — The constrained pytest range selects a known vulnerable version and excludes the fix

**Location**

- `requirements-dev.txt:22-25` declares `pytest~=8.3`; the reviewed virtual
  environment resolved pytest 8.4.2.
- [GHSA-6w46-j5rx-g56g](https://github.com/advisories/GHSA-6w46-j5rx-g56g)
  affects pytest versions below 9.0.3. It concerns insecure predictable
  `/tmp/pytest-of-{user}` handling on Unix and is rated moderate (CVSS 6.8).
- No Dependabot, Renovate, pip-audit, OSV, or equivalent Python SCA workflow is
  configured.

**Problem**

The compatible-release constraint intentionally blocks the only patched major
line. The weekly floating-latest compatibility canary is not a vulnerability
scanner and does not create an update path.

**Why it matters**

The issue is development-only and requires local multi-user Unix preconditions,
so it is not a critical production exposure. It still affects CI/developer
machinery and demonstrates that dependency constraints can retain a known
vulnerability indefinitely.

**Suggested improvement**

Qualify pytest 9.0.3+ and move the constrained range after compatibility tests.
Add scheduled Python SCA plus automated update proposals. Keep the deliberate
stdlib-only shipped runtime, full-SHA Action pins, and isolated npm tooling.

### M-12 — Privacy scanning is disabled while personal author identity metadata exists in history

**Location**

- `docs/process.toml:114-121` sets `privacy_check = false`; the secrets floor is
  separately enabled.
- Git history contains substantial author metadata using personal email-provider
  domains in addition to no-reply and example identities.

**Problem**

The repository has made a configured choice not to scan for privacy/identity
leaks, but the irreversible Git surface already contains potentially personal
metadata. This may be intentional; it is not documented as a publication
decision.

**Why it matters**

If public distribution is intended and the identities are not meant to be
public, later remediation requires a disruptive history rewrite that changes
commit IDs and downstream references.

**Suggested improvement**

Make and record an explicit owner decision before wider publication. If the
metadata is unintended, coordinate a one-time history rewrite, update downstream
references, and then enable privacy checking. Do not copy the identities or
their counts into more artifacts while deciding.

### M-13 — The subagent supervision gate calls itself deny-by-default but deliberately fails open

**Location**

- `project-trajectory/scripts/subagent_gate.py:2` says “deny-by-default.”
- `:13-20` says absent/off allows and the kit ships off.
- `:57-85` maps unreadable or malformed TOML to undeclared policy.
- `:188-201` deliberately allows on that path; tests pin the behavior.

**Problem**

The headline safety description contradicts the executable consent behavior.
Even after an operator chooses to configure supervision, corrupting the policy
can turn it off.

**Why it matters**

This mechanism is correctly scoped as supervision rather than a sandbox, but
operators still need its failure posture described accurately. False
deny-by-default language encourages reliance the code does not provide.

**Suggested improvement**

Either rename it “opt-in, fail-open supervision,” or treat malformed configured
policy as `ask`/deny while keeping clearly out-of-scope payload errors fail-open
if availability is the priority. Test corruption separately from intentional
absence.

### M-14 — Tracked generated HTML creates large, frequent history churn

**Location**

- `PROJECT_STATE.html` is about 1.9 MB and has changed in roughly 791 commits.
- `docs/open-items.html` is about 846 KB and has changed in roughly 122 commits.
- The local object database reports about 137 MB loose plus 60 MB packed objects.
- `project-trajectory/scripts/gen_trajectory.py` embeds an as-of commit stamp,
  so regeneration changes the dashboard even when its substantive model is
  unchanged.

**Problem**

Large derived artifacts are committed repeatedly, often for provenance-only or
small source changes. Git delta compression mitigates some storage, so not all
object size is attributable to these files, but the churn is objectively one of
the dominant history surfaces.

**Why it matters**

Generated diffs crowd review, increase clone/fetch/storage costs, produce merge
conflicts, and can hide meaningful generated changes in megabyte-scale output.

**Suggested improvement**

Decide which generated views must be versioned. For reproducible views, consider
publishing CI artifacts/site output and keeping only source plus a checksum or
compact summary in Git. If committed HTML remains a requirement, remove
provenance-only churn where possible, split stable assets/data, and add a
generated-size/change budget.

### M-15 — The forward-only status surface exceeds its own context budget

**Location**

- `docs/status.md:3-10` defines the file as a lean forward-only resume surface.
- The file is 166 lines against a declared 120-line budget; `check_docs --stale`
  warns.
- Countersign/history and standing doctrine remain at `:46-54,130-155` even
  though other homes exist for both.

**Problem**

An always-loaded context file contains more historical/standing prose than its
own design allows, and the warning has become accepted background noise.

**Why it matters**

Every agent/human resume pays this context and scanning cost. Ignoring the
budget weakens the repository's “no silent green” culture even though the
finding is low-risk by itself.

**Suggested improvement**

Reduce the file below 120 lines by moving durable doctrine to the contributor/
process guide and resolved countersign detail to decision/log evidence. Keep
only next acts, generated state, and scope.

### M-16 — Live performance assurance is mostly absent

**Location**

- `project-trajectory/scripts/check_perf.py --tier all` reports
  `OK - no performance budgets to compare`.
- There is no live `docs/requirements/performance-budgets.csv`; only the shipped
  PB-000 template exists.
- The smoke wall-clock budget is a useful exception. The full suite took
  628.85 seconds on this Windows host.

**Problem**

The repository has a performance-check framework but no measurements/budgets for
trace analysis, bootstrap, dashboard generation, gate runtime, memory, or Git
I/O. The green performance result is vacuous.

**Why it matters**

Hook- and agent-critical tools run frequently, central modules scan large
registries, and the test suite already takes more than ten minutes locally.
Regressions can grow unnoticed until developer workflow becomes unusable.

**Suggested improvement**

Create a small live budget registry for the few commands that dominate feedback
latency. Measure representative fixture sizes, record machine-independent size/
operation metrics where possible, and reserve noisy wall-clock checks for CI
with generous thresholds.

### M-17 — Git test repositories are not hermetic on Windows

**Location**

`docs/work/queued/WI-465-autocrlf-fixture-pin-sweep.md:3` records 28 `git init`
fixture sites that inherit global `core.autocrlf` and five near-verbatim
`git_repo` helpers.

**Problem**

Fixture repositories can normalize bytes differently according to the
developer's global Git configuration. One assertion can fail while another
becomes vacuous. The debt is already known but remains queued.

**Why it matters**

The suite's strongest value is its real temporary Git repositories. If those
repos are not deterministic, cross-platform confidence is weaker than the green
matrix suggests.

**Suggested improvement**

Complete WI-465 using one shared repository builder that writes the
production-faithful `.gitattributes`/local config before commits. Migrate every
fixture without weakening byte-sensitive assertions.

## Low

### L-01 — Several live comments and skills describe superseded behavior

**Location**

- `project-trajectory/scripts/check_trajectory.py:56-62` says
  `status_forward_only_findings` is not implemented and no status generator
  exists; the function is implemented at `:2416+` and the docstring itself
  describes the later hybrid generated-block behavior.
- `project-trajectory/skills/registry-hygiene/SKILL.md:30` says the
  `DevStg-Impl` trace adds “+ Verified,” while the current model folds Verified
  into Approved. The command's legacy `--require-verified` name remains valid,
  but the prose is wrong.
- `project-trajectory/scripts/handback.py:55-74` claims integration never
  imports handback; it does at `integrate.py:2186`.

**Problem / why it matters**

These comments sit close to operational code and are likely to be trusted more
than historical prose. They send maintainers toward the wrong model and reveal
that vocabulary checks do not cover ordinary status language.

**Suggested improvement**

Correct the statements now. Extend rule-sync/vocabulary tests to a small set of
current operational phrases without attempting to police all historical text.

### L-02 — A production invariant relies on removable `assert`

**Location**

`project-trajectory/scripts/gen_trajectory.py:812` asserts that a panel ends in
`</section>` and then slices the string.

**Problem / why it matters**

`python -O` removes the assertion while leaving the unsafe slice. This is a
small but avoidable example of optimization-dependent behavior.

**Suggested improvement**

Use an explicit conditional and raise a descriptive exception/refusal.

### L-03 — Commit-subject practice does not match the shipped session protocol

**Location**

`project-trajectory/skills/session-protocol/SKILL.md:129` prescribes
`WI-<n>: <imperative subject>`. Only 38 of the last 200 subjects match a
`WI-###:` prefix; some older examples are opaque (“Spine note tweak”, “Prep
notes #2”, “Added scratch notes”), while many recent commits use descriptive
category prefixes instead.

**Problem / why it matters**

The recent categorical subjects are often good, but the repository has two
competing conventions. Automation and readers cannot rely on either.

**Suggested improvement**

Choose one documented convention. A practical form is
`WI-### <category>: imperative summary`, with a documented exception for owner
sittings/merge commits. Enforce only if tooling genuinely consumes the form.

### L-04 — The development toolchain is constrained but not reproducibly locked

**Location**

`requirements-dev.txt` intentionally uses compatible-release ranges and states
that it is not a byte-reproducible lock. CI installs those ranges directly.

**Problem / why it matters**

Patch/minor releases can change the exact verification environment between two
runs. The canary handles future compatibility, but no exact resolved set is
available for reproducing a historical failure.

**Suggested improvement**

Keep human-maintained compatible constraints, but generate a hash-pinned CI lock
for supported Python versions and update it automatically after the canary/SCA
passes.

## Positive / good practices

### P-01 — Test breadth and real-repository behavior are strong

The full suite passed 2,588 tests with 13 intentional/environment skips.
Coverage is 93% overall and all committed per-module floors pass. Tests create
real temporary repositories, exercise process-tree termination, and cover
platform-specific paths. Individual tests are usually bounded and named by
behavior even where their containing files are too large.

### P-02 — Cross-platform and supply-chain CI defaults are unusually good

`.github/workflows/test.yml:47-87` covers Linux, Windows, macOS, Python 3.11,
and current Python. Actions are pinned to full commit SHAs and workflows use
`permissions: contents: read`. Concurrency cancellation and timeouts are
explicit. The shipped runtime remains standard-library-only. Shell syntax
checks passed for all eight `.sh` files and PowerShell parsing passed for all
five `.ps1` files.

### P-03 — Registry structural integrity is excellent

Strict tracing reports 27 SN, 72 SR, 161 LLR, and 157 TC with zero orphans and
zero integrity/schema errors. All 72 SRs contain exactly one `shall`. The hats
audit finds 27 needs, 16 hats, and no unknown tag token. Need-form and retired-
vocabulary checks are clean. This is a strong base even though content remains
provisional and some exact code anchors drifted.

### P-04 — Several extracted modules demonstrate the architecture the rest should adopt

- `project-trajectory/scripts/plan_round.py:2-29` is a small typed, pure state
  machine with no filesystem/Git/session effects.
- `spine_carrier.py:17-50` centralizes failure-prone registry vocabulary while
  keeping I/O ownership explicit.
- `traj_graph.py:1-39` is a clean pure layout layer with immutable geometry and
  iterative deep-graph handling.
- `docs/runtime-flows.md:3-34` clearly separates command tools from the station
  and combines authored behavior with source-derived structure.

These are credible templates for decomposition: pure decisions, explicit data,
and effects at the edge.

### P-05 — Security-sensitive subprocess and secret handling are generally disciplined

Configured repository/range secret scans are clean. Most subprocesses use argv
execution rather than a shell. `run_menu.py:193` is the sole deliberate
`shell=True` boundary found; it is limited to trusted configured recipes and has
detailed quoting tests. `pip check` is clean and the isolated dashboard-shot
npm project reports zero vulnerabilities.

### P-06 — Licensing and downstream attribution are strong

The root and portable kit carry Apache-2.0 license texts, a detailed NOTICE and
scope explanation, and tests that pin root/portable equality. Bootstrap writes
the full kit license and attribution into scaffolds. No obvious licensing or
vendoring compliance defect was found; the vendored checker reports no manifest
because there is no vendored payload.

### P-07 — Accessibility is treated as a requirement, not a slogan

SR-052 (`docs/requirements/system-requirements.toml:306-313`) traces to an
accessibility rubric and keyboard/ARIA/contrast tests. The dashboard provides
keyboard tab control, native disclosure widgets, light/dark themes, and
responsive layouts. The M-03 data-density failure is serious precisely because
the underlying accessibility practice is otherwise good.

### P-08 — Internationalization scope is explicit and defensible

`docs/requirements/stakeholder-needs.toml:81-89` records i18n as a non-goal and
explains why stable machine-readable identifiers and tokens must not vary by
locale. For a developer-process kit rather than an end-user application, this
is an acceptable scope decision. Human-facing prose could still be externalized
later without localizing the protocol vocabulary.

### P-09 — Documentation navigation and derived checks catch real defects

The live documentation scan found no broken links, and source-derived
architecture checking exposed H-03 rather than letting it remain invisible.
The repository records known debt through ratchets and queued work rather than
pretending the baseline is ideal. That candor should be retained while assigning
real owners and deadlines.

## Known and explicitly deferred risk

The following conditions are important context but should not be misrepresented
as newly discovered defects:

- The spine is intentionally provisional: `docs/gate` reports 74 Drafted and
  151 Modified artifacts, and the dashboard shows only 2 of 72 SRs Approved.
  `docs/status.md` explicitly says the current corpus is not signed/seeded.
- WI-448 already owns the first shared-helper consolidation slice; WI-465 owns
  the Git fixture normalization sweep.
- The missing SN-036 per-decomposition hat record is declared in the hats
  registry/status. H-08 is about the README falsely claiming it shipped.
- The SAFETY hat currently reaches zero needs, but the hat registry explicitly
  records that inclusion as an owner decision.
- Interface/provenance hygiene is known and large: 49 held contract-provenance
  citations, argumentative/overlong contracts, and 47 of 125 endpoints that do
  not resolve to architecture modules. WI-469/WI-455 own much of that rewrite.
- B-01/B-02 have no realizing IF rows under an explicit ruling.
- OI-42 owns broader `Implements:` enforcement drift; WI-464 owns the planned
  retiering work; WI-390 owns part of the concurrency-v2 contract drift.
- The dead red-TC feature is acknowledged in source/status. M-10 rates the cost
  of continuing to ship it rather than presenting it as an undiscovered issue.

These declarations are useful, but “known” is not the same as “controlled.”
Anything without a live owner, deadline, or gating consequence remains an
accepted risk.

## Overall recommendations and next steps

### 1. Stop the false-green paths first

1. Redesign gate selection so established product checks are monotonic and
   always run in downstream CI.
2. Declare/correct the `hats -> spine_carrier` seam and require the strict
   architecture job to pass.
3. Fix current Ruff findings, especially the duplicate ratchet key.
4. Repair launcher interpreter selection and the Windows nested-output decoder.
5. Upgrade pytest to a patched release and add scheduled SCA.

These are small-to-medium changes with disproportionate trust impact. Do them
before another large requirements migration.

### 2. Restore one authoritative contract

Run a single coordinated schema/documentation correction covering interface
`Status`, boundary-frame mandatory status, CMP vocabulary, the shipped promise
ledger, the registry-hygiene skill, stale prompts, and exact CodeSymbol anchors.
Where possible, generate tables and validation prose from the same constants or
templates used by enforcement. Add adopter-level tests that follow the written
instructions to create real valid rows.

### 3. Break the cyclic core behind typed contracts

Treat the seven-module SCC as one refactoring program:

1. characterize import directions and behavior;
2. extract pure read models and lifecycle result types;
3. move view dependencies onto read-only models;
4. make dispatch the outer composer;
5. package shared implementation while retaining thin CLI wrappers;
6. split `trace.analyze`, `check.steps`, and loop state by policy/effect boundary;
7. install an SCC/layer test.

Use dataclasses/`TypedDict` first at the `Registries`, `Findings`, `LoopContext`,
pending-action, and work-outcome seams. Do not attempt a repository-wide typing
conversion before these high-value boundaries.

### 4. Turn advisory assurance into an honest staged plan

Decide whether IF contract-test coverage is mandatory. If yes, create a bounded
migration allowlist and promote it at `DevStg-Tests`; if no, soften the claim.
Separate live code-symbol validation from historical-record noise. Finish the
Git fixture normalization. Add a few real performance budgets for commands on
the commit/agent feedback path.

### 5. Reduce context and generated-history cost

Shorten status to its declared budget, move decision chronology out of
normative cells, split mega tables and test modules by behavior, and decide
whether megabyte-scale derived HTML belongs in Git. Put hard limits on titles
that become UI labels and make the dashboard defensively render arbitrary
registry text.

### 6. Make publication/governance decisions explicit

Resolve the personal-author-metadata/privacy posture before wider publication,
standardize the commit-subject convention, and keep the existing strong Apache
license/NOTICE and SHA-pinned CI practices.

## Final verdict

The repository is ambitious, thoughtful, and much better tested than most
templates. It is also carrying enough cyclic coupling, duplicated mechanics,
normative prose drift, and advisory-only enforcement that its core promise is
currently overstated. The full suite being green is valuable evidence about the
tested configuration; it is not evidence that downstream gates will keep
running those tests. Fix that first. Then use the repository's strongest ideas
— pure bounded modules, executable traceability, real temp-repo tests, and
explicit contracts — to replace the central monolith/cycle rather than adding
more prose around it.
