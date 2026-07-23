# Deep repository review — 2026-07-22

This is an as-found review of the live repository on branch
`dualplan-routing-fix` at commit `6a752b4`. It covers code quality,
architecture, requirements and prose, security, performance, tests,
dependencies, configuration, CI, Git practices, licensing, accessibility, and
internationalization readiness.

Per the request, historical/log material was excluded from the review corpus:
`docs/log.md`, `docs/archive/**`, `docs/iteration/**`, `docs/reviews/**`, and
the owner-only `OWNER_SCRATCHPAD.md` were not audited. Generated OKF pages were
checked through generator freshness rather than read one by one.
`PROJECT_STATE.html` was assessed through its generator and a fresh 36-image
width/theme/tab render matrix. Existing repository-review reports were used
only as a regression baseline; their conclusions were not copied forward
without re-verification.

Ground truth at review time:

- 728 tracked live-scope files; 58,445 Python lines across product scripts and
  tests, including 30,064 lines in the 34 shipped scripts.
- Full suite: **1,367 passed, 2 skipped in 275.66 s**.
- Smoke tier: **1,079 passed, 2 skipped in 221.43 s**.
- Ruff lint and format checks: clean. `compileall`: clean.
- Strict trace: **SN=25, SR=109, LLR=97, TC=100**, with zero orphan,
  integrity, schema, status, component, or interface findings.
- Latest coverage data: **92% overall**, but with materially weaker individual
  modules called out below.
- Duplicate detector: green with its allowlist; without that allowlist it
  reports **225 blocks across 101 allowlisted file pairs**.
- Secrets/privacy repository sweep: clean. No private-key material was found.
- Dashboard: 36/36 Playwright screenshots generated and representative light,
  dark, desktop, and 390 px images inspected. No clipping, contrast, or
  responsive-layout regression was visible.
- `npm audit --package-lock-only`: zero known vulnerabilities. Playwright
  1.61.1 is current. The compatible Ruff range already admits current
  0.15.22; pytest intentionally remains on the constrained 8.x line while a
  floating canary tests future majors.

---

## 1. Unfixed items and why

_To be filled after the remediation pass. Findings below describe the
repository as found at `6a752b4`._

**Fixed in this pass:** _(to be filled)_

**Deferred, with reasons:** _(to be filled)_

---

## 2. Executive summary

This repository is substantially better engineered than a typical template
kit. Its strongest feature is not any one script; it is the amount of
mechanized agreement between requirements, tests, generated views, and gates.
The trace spine is clean, generated artifacts are freshness-checked, the CI
workflow is SHA-pinned and least-privileged, tests are behavioral and
cross-platform, and the unattended coordinator contains unusually careful
failure and recovery handling. The recent dashboard work also holds up
visually across themes and widths.

The blunt assessment is that the repository's remaining risk is concentrated
where the machines are weakest:

1. A real Windows command-injection path remains in prompt delivery. The code
   says prompt substitution is safe because `shell=False`, but Windows can
   still route `.cmd`/`.bat` files through `cmd.exe` and reparse the substituted
   prompt.
2. The core is still too large and too cognitively expensive. Six production
   modules exceed 1,900 lines; 53 functions are deliberately grandfathered
   above the configured complexity limit. The ratchet prevents silent growth
   but does not make this code easy to reason about.
3. The project advertises a reusable copy-in kit without any license. That is
   a legal blocker, not cosmetic paperwork.
4. Several newer contracts are only partly implemented: the Python 3.11 floor
   is enforced by CI but not by the developer setup scripts; the dashboard
   loses `deferred`/`blocked` status information; and its visual tabs do not
   expose tab state to assistive technology.
5. Documentation currency slipped immediately after recent work. The status
   page still claims a 47-second smoke bar, teaches a noisier docs command, and
   puts completed work under “Next action.” The shipped README also describes
   only half of the six-state work-item lifecycle.

There are no Critical findings. The closest is H-1, but exploitation requires
a Windows batch-shim route plus attacker-influenced repository/prompt text in a
locally launched unattended session. That is serious and should be fixed
first, but it is not a remotely exposed default service.

---

## 3. Prioritized findings

### Critical

None found.

### High

#### H-1 · Windows batch-shim prompt delivery permits command injection

- **Location:** `project-trajectory/scripts/agent_session.py:51-73`;
  `project-trajectory/agents.template.csv:5-9`
- **Relevant code:**

  ```python
  for tok in split_cmd(template):
      if "{prompt}" in tok:
          saw_prompt = True
      argv.append(tok.replace("{model}", model).replace("{prompt}", prompt))
  return (argv, None) if saw_prompt else (argv, prompt)
  ```

  ```csv
  GOOGLE-GEMINI-3-PRO,...,gemini -p {prompt} --output-format json,...
  AGENTS-EXAMPLE-000,...,your-cli -p {prompt},...
  ```

- **Problem:** The comment “never through a shell” is false on Windows for
  batch files. `run_session()` deliberately resolves npm-style commands to
  `.cmd` shims. A prompt token containing `&`, `|`, `%NAME%`, quotes, or other
  `cmd.exe` syntax can therefore be reparsed as shell input even though Python
  was called with `shell=False`. Repository text is incorporated into prompts,
  so a malicious or merely unlucky prompt can cross this boundary.
- **Why it matters:** This is command execution inside the developer's
  checkout with the agent process's privileges. It undermines the otherwise
  careful model-slug validation and stdin transport work.
- **Suggested improvement:** Fail closed when `{prompt}` is used with an
  executable that explicitly is, or resolves on Windows to, `.cmd`/`.bat`.
  Require stdin prompt delivery or a native executable. Apply the check in
  preflight and again after environment-specific PATH resolution at launch.
  Add regressions for explicit and PATH-resolved batch shims and update the
  template guidance.
- **External confirmation:** Python's official subprocess documentation states
  that Windows batch files may be launched in a system shell regardless of
  the arguments passed to `subprocess`, with no escaping added by Python:
  [Python subprocess security considerations](https://docs.python.org/3/library/subprocess.html#security-considerations).

#### H-2 · Core module and function complexity remains beyond maintainable review scale

- **Location:** `project-trajectory/scripts/gen_trajectory.py` (4,511 lines),
  `agent_dispatch.py` (3,452), `agent_loop.py` (3,034), `trace.py` (2,206),
  `check_trajectory.py` (1,926), `bootstrap.py` (1,916);
  `tests/test_complexity_ratchet.py:37-111`
- **Relevant code/config:**

  ```python
  ("agent_dispatch.py", "dispatch_run"): 40,
  ("agent_loop.py", "session_bookkeeping"): 31,
  ("bootstrap.py", "main"): 41,
  ("plan_runner.py", "run_dual_plan_round"): 30,
  ("trace.py", "analyze"): 53,
  ("gen_trajectory.py", "sw_containment"): 28,
  ```

  Measured function sizes include `dispatch_run` at 398 lines,
  `agent_loop.main` at 393, `trace.analyze` at 383, `bootstrap.main` at 378,
  and `run_iteration` at 358.
- **Problem:** Fifty-three functions exceed the configured complexity ceiling
  of 10. The coordinator split improved file boundaries, but the central
  orchestration still passes large dictionary-shaped state through long
  procedures that mix decision logic, Git effects, process launching, artifact
  writes, and error disposition. `gen_trajectory.py` combines parsing,
  layout algorithms, HTML/CSS/JS templating, accessibility behavior, status
  generation, and CLI concerns in one file.
- **Why it matters:** These are the repository's highest-risk paths. A reviewer
  cannot hold all branches and invariants in working memory, and narrow edits
  routinely require complexity-baseline exceptions. The code can be green and
  still be difficult to change safely.
- **Suggested improvement:** Treat decomposition as architecture work, not a
  formatting exercise. Characterize state transitions first, introduce typed
  value objects for session/train/route state, isolate pure decisions from Git
  and subprocess effects, and split the dashboard into parsing, graph/layout,
  view-model, and rendering modules. Add a per-module size ratchet alongside
  the existing per-function complexity ratchet.

#### H-3 · The reusable kit has no license

- **Location:** repository root and `project-trajectory/`; no `LICENSE`,
  `COPYING`, or root legal notice exists. The decision is acknowledged in
  `docs/open-items.md` under OI-4 and deferred as WI-097.
- **Problem:** The README tells adopters to copy this kit into other
  repositories, but the repository grants no explicit right to copy, modify,
  or redistribute it.
- **Why it matters:** Default copyright is not an open-source license. External
  adoption is legally ambiguous, and every copied scaffold inherits that
  ambiguity. This is especially inconsistent in a kit that requires adopters
  to track asset licenses and attribution carefully.
- **Suggested improvement:** The owner must decide whether the repository is
  private, source-available, or open source. Then add the chosen license,
  copyright/notice text, README terms, and any required third-party notices.
  Do not guess MIT versus Apache-2.0 in an engineering cleanup.

### Medium

#### M-1 · The declared Python 3.11 floor is not enforced by developer setup

- **Location:** `scripts/dev-setup.sh:73-84`,
  `scripts/dev-setup.ps1:37-60`,
  `project-trajectory/scripts/dev-setup.template.sh:149-151`, and the
  PowerShell template equivalent.
- **Relevant code:**

  ```sh
  if [ -x .venv/bin/python ]; then PY=.venv/bin/python
  elif real python3; then PY=python3
  elif real python; then PY=python
  fi
  report "runtime (python3)" "$([ -n "$PY" ] && echo 1 || echo 0)" \
    "install Python 3.11+"
  ```

- **Problem:** Any runnable Python is reported as `[ok]`. The live workspace
  demonstrates the defect: `.venv/bin/python` is 3.9.6, yet `dev-setup`
  accepts it and the full suite runs. `requirements-dev.txt` contains prose
  about the 3.11 floor but no enforceable interpreter constraint.
- **Why it matters:** Local verification can occur on an unsupported runtime,
  hiding 3.11-only failures until CI. The setup command explicitly promises to
  provision the supported environment and currently does not.
- **Suggested improvement:** Probe `sys.version_info >= (3, 11)` for every
  venv/ambient candidate, report older interpreters as missing/unsupported,
  refuse `--install` through an old interpreter, and regression-test both
  sides of the boundary in the shell and PowerShell templates.

#### M-2 · The dashboard silently rewrites `deferred` and `blocked` work items as `queued`

- **Location:** `project-trajectory/scripts/gen_trajectory.py:489-504`,
  `:702-743`, `_wi_st()` near `:1214`; generated `PROJECT_STATE.html`
  currently serializes WI-271 as `"status": "queued"` although the registry
  says `deferred`.
- **Relevant code:**

  ```python
  STATUS_FILL = {
      "done": "#047857",
      "active": "#b45309",
      "queued": "#94a3b8",
      "retired": "#78716c",
  }
  st = w["status"] if w["status"] in STATUS_FILL else "queued"
  details[w["id"]] = {"status": st, ...}
  ```

- **Problem:** The six-state source vocabulary is reduced to four states.
  This is not only a shared visual bucket: tooltips and the detail JSON report
  the wrong status. `deferred` means deliberately parked and `blocked` carries
  a named impediment; neither is equivalent to queued work.
- **Why it matters:** The dashboard is the repository's advertised unified
  state surface. Mislabeling parked work as ordinary queue work causes bad
  prioritization and contradicts the registry SSOT model.
- **Suggested improvement:** Preserve all six source statuses in details,
  labels, accessible names, and legend. If visual grouping is retained, name it
  explicitly and keep the actual status as a second field. Because this is a
  render-surface change, file it as its own dashboard WI and repeat the full
  width/theme/tab critique matrix.

#### M-3 · Dashboard tabs have visual state but no tab semantics

- **Location:** `project-trajectory/scripts/gen_trajectory.py:2252-2280` and
  `:2418-2423`
- **Relevant code:**

  ```html
  <nav class="tabs">
    <button class="active" data-tab="arch">What (SR breakdown)</button>
    ...
  </nav>
  ```

  ```javascript
  b.onclick = () => {
    for (const x of document.querySelectorAll('nav.tabs button'))
      x.classList.toggle('active', x===b);
    for (const p of document.querySelectorAll('.panel'))
      p.classList.toggle('active', p.id===b.dataset.tab);
  };
  ```

- **Problem:** There is no `role="tablist"`, `role="tab"`,
  `aria-selected`, `aria-controls`, `role="tabpanel"`, `aria-labelledby`,
  roving tabindex, or arrow-key behavior. Native buttons are reachable, but a
  screen reader is not told which view is selected or how buttons and panels
  relate.
- **Why it matters:** The active view is core state, not decoration. Visual-only
  selection excludes assistive-technology users and weakens the otherwise good
  keyboard/accessibility work in the graphs.
- **Suggested improvement:** Implement the ARIA tabs pattern, synchronize
  selected/hidden/focus state, and add keyboard regressions for arrows,
  Home/End, Enter/Space, and panel visibility. File and validate it as its own
  render WI.

#### M-4 · The global coverage floor hides weak high-risk modules

- **Location:** `docs/stack.ini:45-51` (`threshold = 85`); latest coverage
  report.
- **Evidence:** Overall coverage is 92%, but
  `subagent_gate.py` is 40%, `plan_coverage_step.py` 65%,
  `agent_session.py` 74%, `plan_runner.py` 79%, and `run_menu.py` 79%.
- **Problem:** One aggregate threshold permits heavily tested generators and
  trace code to subsidize thin coverage in process-launch, policy-gate, and
  planning adapters. The headline percentage overstates confidence in those
  modules.
- **Why it matters:** `agent_session.py` contains the process and security
  boundary implicated by H-1. `subagent_gate.py` is itself a safety control.
  Branches missed there are not interchangeable with lines covered elsewhere.
- **Suggested improvement:** Add per-module minimums for security/process
  boundaries, initially at honest current baselines, then raise them with
  focused behavioral tests. Keep the global floor as a backstop rather than the
  only measure.

#### M-5 · Duplicate-code enforcement is too coarse to detect growth inside 101 trusted pairs

- **Location:** `docs/dupes-allow`; `project-trajectory/scripts/check_dupes.py`
- **Relevant policy text:**

  ```text
  Paths are allowed by line-number-free "a.py == b.py" file pairs.
  New copy-paste between two files ALREADY listed here is not caught.
  ```

- **Problem:** The allowlist currently hides 225 detected blocks across 101
  file pairs. Much of it is a deliberate “standalone script” policy, but the
  pair-level exemption means any future duplicate block between an already
  listed pair passes automatically. It is a widening trust hole, not a fixed
  census.
- **Why it matters:** The repository's F5 duplication exception is large enough
  that accidental clones can disappear inside it. It also makes the green
  duplicate check easy to misread as “no duplication.”
- **Suggested improvement:** Key exemptions by normalized token fingerprint
  plus file pair, or keep a count/hash baseline per pair. Continue permitting
  small standalone loaders where justified, but make new blocks require a
  deliberate baseline change.

#### M-6 · Live operational documentation contradicts current behavior

- **Location:** `docs/status.md:37-43`; `docs/status.md` “Next action”;
  `docs/stack.ini:18-23`; `project-trajectory/README.md:36`;
  `tests/test_complexity_ratchet.py:18,56,104`.
- **Evidence:**

  ```markdown
  smoke ... (~47 s)
  check_docs.py --root . --stale
  ```

  Current smoke is 221.43 s. The direct docs command also omits the
  `--ignore docs/test/report.md` used by the real harness and can warn on its
  generated trace report. “Next action” contains completed dual-plan and
  Python-floor work. The shipped README says only
  `queued→active→done`, omitting `deferred`, `blocked`, and `retired`. The
  complexity test says WI-226 “is paying” the debt although WI-226 is done and
  major debt remains.
- **Problem:** These are entry-point instructions and current-state claims, not
  harmless history. They disagree with the code and registry.
- **Why it matters:** Agents and contributors budget incorrectly, run a noisier
  command than CI, and learn an incomplete lifecycle. This repository's product
  is partly its process documentation; stale process prose is a product defect.
- **Suggested improvement:** Restamp counts/timings from this review, use the
  exact harness docs command, make “Next action” genuinely forward-looking,
  document the six-state lifecycle, and relabel WI-226 as historical rather
  than an active debt owner.

#### M-7 · The active branch is 845 commits ahead of `main`, and branch pushes receive no CI

- **Location:** Git graph; `.github/workflows/test.yml:6-9`;
  `docs/status.md` merge note.
- **Relevant workflow:**

  ```yaml
  on:
    push:
      branches: [main]
    pull_request:
  ```

- **Problem:** `dualplan-routing-fix` is published to its remote but is 845
  commits ahead of `main`. A push to this branch does not trigger CI unless a
  pull request exists. The status page explicitly leaves merge-to-main as an
  owner decision.
- **Why it matters:** An enormous integration delta is difficult to review,
  bisect, or merge, and the remote branch can look healthy without a hosted CI
  result. Local gates are strong but are not an independent environment.
- **Suggested improvement:** Decide the integration strategy immediately:
  open/maintain a PR so branch updates run CI, or enable CI on protected
  development branches. Merge in reviewed slices rather than letting the delta
  grow. Do not rewrite the 845-commit history casually.

### Low

#### L-1 · Test organization mirrors the production monoliths

- **Location:** `tests/test_gen_trajectory.py` (2,261 lines),
  `test_agent_loop.py` (2,047), `test_trajectory.py` (1,940),
  `test_agent_loop_integrate.py` (1,939), and `test_trace.py` (1,295).
- **Problem/impact:** Coverage is extensive, but navigating these files and
  understanding fixture ownership is unnecessarily expensive. Splitting tests
  before production seams stabilize could duplicate fixtures, so this should
  follow H-2's architectural boundaries.
- **Suggested improvement:** Split by stable behavior boundary
  (parsing/decision/effect/recovery/rendering), with shared fixture modules only
  where they express a genuine test API.

#### L-2 · The generated dashboard is a heavy single artifact

- **Location:** `PROJECT_STATE.html` (1,145,810 bytes);
  `project-trajectory/scripts/gen_trajectory.py`.
- **Problem/impact:** A one-file offline dashboard is a deliberate and useful
  deployment choice, but every small view change regenerates a megabyte-scale
  diff and forces full perceptual revalidation. Embedded HTML/CSS/JS inside a
  Python `String.Template` also reduces editor and static-analysis help.
- **Suggested improvement:** Preserve the single-file output contract while
  generating it from separately testable source fragments/modules. Add a size
  budget or warning so accidental growth is visible.

#### L-3 · Historical Git metadata is inconsistent

- **Location:** repository history.
- **Problem/impact:** Four author identities occur in the history, and even the
  most recent 100 commits contain vague subjects such as “Latest,” “Tweak
  notes,” and “Various notes.” Recent WI-oriented commits are much better, so
  this is mostly historical review/bisect friction.
- **Suggested improvement:** Keep the repo-local canonical identity and current
  WI/outcome subject convention. Do not rewrite published history solely for
  cosmetic consistency.

#### L-4 · Internationalization is not designed in

- **Location:** dashboard and CLI strings throughout
  `gen_trajectory.py`, `agent_loop.py`, and related scripts; dashboard root
  declares `lang="en"`.
- **Problem/impact:** All labels, prompts, policy tokens, and parsers are
  English-only. This is acceptable for the stated developer-process-kit goal,
  but localization later would be expensive because strings and parsing rules
  are embedded in code.
- **Suggested improvement:** Record English-only as an explicit non-goal. If
  localization becomes a requirement, separate display strings from stable
  machine tokens before translating anything.

### Positive / good practices

#### P-1 · Requirements and traceability are genuinely mechanized

The SN→SR→LLR→TC spine is clean at strict G3, status is derived rather than
hand-set, generated artifacts are freshness-gated, and off-spine interfaces,
components, assets, and work items have integrity checks. Requirements are not
merely decorative documents.

#### P-2 · Testing is broad, behavioral, and failure-oriented

The 1,367-test suite covers unit, integration, linked-worktree, recovery,
cross-platform launcher, generator, hook, and dashboard behavior. Many tests
prove checks can fail rather than only exercising happy paths. Xdist,
timeouts, smoke/full tiers, and the complexity ratchet are thoughtful.

#### P-3 · Security and robustness posture is strong outside H-1

No `eval`, `exec`, or accidental `os.system` use was found. The only
`shell=True` boundary runs the user's own declared run recipe and is explicitly
documented. Model slugs and registries are validated, secrets scanning is
always present, privacy review is opt-in but fail-closed when enabled,
subprocesses have timeouts and process-tree cleanup, and generated/registry
writes generally fail closed.

#### P-4 · Dependency and CI hygiene is excellent

Shipped scripts remain standard-library-only. Meta dependencies are limited to
four constrained test tools, with a floating canary for future-major
compatibility. Actions are pinned to full SHAs, permissions are read-only,
jobs have timeouts, and redundant runs are cancelled. The current package
checks found no npm vulnerability; Playwright 1.61.1 is current
([npm package](https://www.npmjs.com/package/playwright)), Ruff's current patch
is 0.15.22 ([PyPI](https://pypi.org/project/ruff/)), and pytest 9.1.1 is
available but intentionally outside the stable 8.x constraint
([PyPI](https://pypi.org/project/pytest/)).

#### P-5 · Documentation architecture is unusually deliberate

`README.md`, `ADOPTING.md`, `PROCESS.md`, and the applies-when index in
`PROCESS_OPTIONS.md` give adopters clear entry points. Owner-only notes,
historical evidence, generated artifacts, current status, requirements, and
open decisions have distinct homes. The exclusions in this review are
therefore practical rather than hiding required operational facts.

#### P-6 · Dashboard rendering is currently visually sound

The fresh 36-shot matrix showed readable light/dark themes, correct mobile
reflow, explicit horizontal-overflow cues, legible graph labels, and no
confirmed clipping or sticky-header defect. SVGs have titles, focusable graph
items, redundant non-color status glyphs, reduced-motion handling, and named
scroll regions. M-2/M-3 are semantic/data issues, not a claim that the visual
design is poor.

#### P-7 · Naming, portability, and deterministic generation are consistent

File/function naming is mostly descriptive, CLI exit behavior is documented,
UTF-8 and newline handling are explicit, and generators avoid clocks in
byte-compared output. Python code favors straightforward standard-library
idioms over clever metaprogramming. The main maintainability problem is scale,
not obscurity.

#### P-8 · Performance choices fit the product

No obvious unbounded production hot loop or memory leak was found. Graph
layout/routing is deterministic and bounded for the repository's data sizes,
subprocess output is streamed, logs are size-bounded, and Git operations are
generally scoped. The four-to-five-minute full suite is expensive but justified
by real worktree/process integration and is separated from the cheaper commit
bar.

---

## 4. Overall recommendations and next steps

1. **Close the security boundary first:** block prompt-in-argv for Windows
   batch shims and require stdin/native executables.
2. **Make the Python floor real locally:** version-check all dev-setup
   candidates and refuse unsupported environments.
3. **Correct current-state prose immediately:** timings, exact commands,
   six-state lifecycle, forward-only status, and the stale WI-226 ownership
   language are cheap, high-confidence fixes.
4. **Handle dashboard defects through the repository's own quality process:**
   one WI for status fidelity and one for semantic tabs, each with tests and a
   fresh 36-shot critique.
5. **Start a bounded decomposition program:** typed orchestration state, pure
   decision modules, isolated effects, and a modular dashboard generator.
   Do not “solve” this by moving 300-line functions unchanged.
6. **Add module-level quality floors:** coverage minimums for security/process
   boundaries, a module-size ratchet, and fingerprinted duplicate exemptions.
7. **Resolve the license and integration decisions:** both are owner calls,
   but continuing to postpone them materially reduces the kit's fitness for
   its stated reusable purpose.

The repository is fit for careful internal use today, but it is not yet honest
to call the copy-in distribution story complete while H-1 and H-3 remain, and
the central orchestration is still expensive enough to review that future
correctness depends too heavily on an unusually large test suite catching what
humans cannot readily reason through.
