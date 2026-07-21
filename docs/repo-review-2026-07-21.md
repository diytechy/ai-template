# Deep repo review — 2026-07-21

Full-repository critical review (code quality, architecture, documentation &
requirements consistency, security & robustness, performance, testing,
dependencies/CI, standards, licensing). Method: nine parallel scoped deep-read
review passes (trace/check core; scaffolding + hooks; the trajectory dashboard
generator; the agent loop; dispatch/routing/dual-plan; tests + CI + dev
tooling; canonical process prose; shipped templates/registries/skills; this
repo's own spine), each verifying findings against file content, plus a
ground-truth full-suite run and cross-cutting license/secrets sweeps.
**Scope exclusions per the review request:** `docs/log.md`, `docs/archive/**`,
`docs/iteration/**`, `docs/reviews/**` (logs/history) were not reviewed;
`OWNER_SCRATCHPAD.md` is owner-only and was not read. `PROJECT_STATE.html` was
inspected only as generator output.

Ground truth at review time: branch `dualplan-routing-fix` @ `0b928ff`;
`python -m pytest -q -n auto` → **1255 passed, 4 skipped** (280.7 s under
heavy parallel load; see M-24); `ruff check .` clean; `trace.py` live-run
SN=25 SR=109 LLR=97 TC=100 with 0 orphan/integrity findings; derived gate G3
fresh.

---

## 1. Unfixed items and why

_Filled after the fix pass. Findings below are as-found on `0b928ff`; the fix
pass landed in the follow-up commit on this branch. Post-fix ground truth:
full suite **1291 passed / 4 skipped in 332.6 s**, smoke tier **1019 passed /
3 skipped in 239.7 s** (24-core box, quiet), `ruff` clean, `trace.py` 0
findings, derived gate G3 fresh, skills copies byte-identical, byte budgets
re-stamped (PROCESS.md 60,420 / PROCESS_OPTIONS.md 160,655 /
AGENTS.template.md 9,975 ≤ 10,000)._

**Fixed in this pass** (each with regression tests where behavior changed):
H-1 (both verdict parse-miss paths fail closed), H-2 (process-tree kill +
interrupt handler), H-4 (Model-cell slug refusal at registry load — the
unattended-path injection vector), H-5 (accreted bullet deleted; the
forward-only guard re-armed scoped to the hand region; docstring +
enforcement-audit row honest), H-6/H-7 (entry docs + PROCESS_OPTIONS
contradictions), H-8 (all 21 dead knowledge citations rewired/deleted;
INDEX + copies regenerated), H-11 (INTERFACES.template vocab/columns/example);
M-1, M-2, M-3, M-4 (core readers), M-6, M-14, M-15, M-16, M-17 (7 new
release-checklist tests), M-18 (timeout wired in all launcher slots), M-19
(transcript redaction), M-20, M-21, M-22, M-23, M-24 (timings re-stamped here,
in CLAUDE.md, stack.ini, and the session-protocol skill), M-27, M-28, M-30,
M-32, M-33, M-34 (arithmetic half), M-35 (9-row supersession sweep + OKF/
dashboard regenerated), M-36, M-37 (launcher headers + README routing row),
M-38, M-39, M-40, M-41, M-42; L-2, L-3, L-4, L-5, L-11..L-18, L-20..L-23,
L-25, L-26 (dialect aligned), L-27, L-28, L-29, L-31 (plus the same unquoted-
comma defect found and fixed in this repo's own `docs/agents.csv`), L-35,
L-37..L-43; L-1 partial (the false uniformity comment now states the real
per-script contract). The C901 ratchet BASELINE was re-stamped for nine
deliberate +1..+3 bumps (each a fail-closed guard above, reasons inline) and
one improvement (ratify_lines 28→27).

**Deferred, with reasons:**

- **H-3 (spine-class persistence)** — changes reservation-metadata semantics
  and integration gating; needs its own reviewed WI with recovery tests, not a
  drive-by (recommendation 2 stands).
- **H-9 (gen_trajectory decomposition)** and every render-surface fix —
  **M-8, M-9, M-11, M-13, L-6, L-7, L-10** — edits to `gen_trajectory.py`
  re-redden the WI-243 perceptual gate and this repo's own protocol files such
  work forward as render WIs with a bundled fresh critique (WI-257/258 are
  already queued; these belong with them). **M-12 and L-8/L-9**
  (check_trajectory's untracked-critique fail-open, rebase window, lexicographic
  critique pick) are checker-side kin deferred to the same WI so the gate
  family changes together, with tests.
- **H-10 (LICENSE)** — owner decision, correctly parked as OI-4/WI-097.
- **M-5 (two G3-SR definitions)** — a spec call between trace and derive_gate;
  decide in the derived-gate model, then pin in test_rule_sync.
- **M-7 (trace.py internal decomposition), M-25 (test-scaffold consolidation),
  M-26 (per-module LOC ratchet)** — refactor-sized; schedule as WIs.
- **M-29 (integrator verdict-gate semantics), M-31 (draw-weight scope),
  M-34's `next_primary` consumer, L-28's remaining design question (score
  gaming, M-* F9)** — design calls on review/routing policy; the mechanical
  halves are done, the policy halves need the owner's ruling.
- **M-10 (status-map machine-local refs)** — a design decision about what a
  byte-compared artifact may derive from.
- **L-19 (3.8 coverage CI leg)** — adds a CI matrix cell (cost); owner call,
  or record the gap in the enforcement audit.
- **L-24 (worktree pruning), L-30 (dual-plan prompts delivery), L-36
  (iteration-index sort), L-44 (run-state end-state), L-45 (`utcnow`
  deprecation sweep — delicate against the naive-UTC blackout contract)** —
  WI-sized follow-ups.
- **L-32 (blackout shipped active; privacy default), L-33 (IF-057
  ratification), L-34 (archive-anchored WI specs), git author-identity
  standardization** — owner decisions.
- **One deliberate WARN left standing:** `check_trajectory` now reports
  "WI-257 cites SR-052 amended after the WI row was last touched" — the
  amendment gate reacting to the M-35 citation sweep. The change is
  citation-only; WI-257's builder should glance and re-affirm the row, which
  is exactly what the gate is for.

---

## 2. Executive summary

**Overall: this is an unusually well-engineered repo whose remaining defects
cluster at the seams its own machines don't reach.** The registries and spine
are mechanically immaculate (zero orphan/integrity findings at G3, OKF bundle
byte-faithful, the review→WI→done loop verifiably closes); the test suite is
one of the strongest reviewed anywhere — meta-tests prove their own checks can
fail, asserts are behavioral, CI is SHA-pinned with least privilege; and the
scripts show deliberate, documented fail-closed engineering (pre-push hook,
durable git-ref state, deterministic generators, prompt-delivery-by-stdin).
Hard-won lessons are recorded in comments with WI provenance.

**The critical pattern, stated bluntly:** the kit preaches
single-source-of-truth and fail-closed gates, and its own weakest spots are
exactly (a) *prose that restates what code decides* — three entry-point
documents still teach models that were retired (hand-bumped `docs/gate`,
hand-edited `check.py`), `PROCESS_OPTIONS.md` contradicts itself outright
twice, 21 of 27 shipped skills cite knowledge files that don't exist, and
templates ship this repo's private WI numbers and project names downstream —
and (b) *gates that fail open in the unattended layer* — an unparseable
critique verdict is treated as APPROVED, spine trains silently lose their
serialization/ratification class on park/resume, the perceptual gate has an
untracked-file fail-open path, and a hung CLI wedges a lane forever by
default. None of these is Critical (no exploitable-at-default-path,
data-destroying, or silently-false-green-at-the-main-gate defect was found),
but the High cluster in the unattended layer deserves fixing before the next
long walk-away run, because each one contradicts the kit's own stated creed.

Strengths worth naming: EXAMPLE.md and ADOPTING.md are excellent adopter
documents; the WI-253/255/256 edge-routing code is clean, provably
terminating, and regression-pinned at unit and real-render level; the
coordinator lock, reservation refs, and publish-path dirt classification are
better than most production orchestrators; `requirements-dev.txt` and the
dashboard-shots Node tooling are model dependency hygiene.

Top items by leverage: H-1/H-2/H-3/H-4 (unattended-layer fail-opens),
H-5 (the forward-only status.md rule — currently both violated and
unenforceable), H-6/H-7 (entry-point prose teaching retired models),
H-8 (dead knowledge citations in 21 shipped skills), H-9 (the 4,357-line
`gen_trajectory.py` monolith), H-10 (no LICENSE — known, owner-parked),
H-11 (INTERFACES.template contradicting its own registry).

---

## 3. Prioritized findings

### Critical

None found. The closest candidates (H-1, H-3, H-4) require either a poisoned
repo file, a malformed-but-plausible LLM output, or a park/restart sequence to
bite, and all are contained inside the locally-run unattended layer rather
than exposed surface. This is a genuinely hardened codebase at the Critical
tier.

### High

#### H-1 · Critique gate fails open: unparseable verdict reads as APPROVED
- **Location:** `project-trajectory/scripts/agent_loop.py:2082` with `:1016-1030`
- **Evidence:**
  ```python
  merged = (v.verdict or "").upper()          # parse miss -> ""
  ...
  # record_critique_verdict: if merged == "CHANGES-REQUESTED": ... else:
  #     self.critique_rounds = 0; self.critique_scope = set(); return "approved"
  ```
- **Problem:** `score_reviews.parse_verdict` returns `verdict=None` when no
  line matches `VERDICT: APPROVE|CHANGES-REQUESTED`. A critic that writes real
  findings but garbles the machine line (`VERDICT: FAIL`, an em-dash, a fenced
  block — routine LLM failure modes) is silently treated as **approved**:
  scope reset, queue cleared, worker exits DONE. There is no downstream
  backstop for critique (the integrator's verdict count is satisfied by the
  REVIEW-A file alone).
- **Why it matters:** this gate was built after the owner's recorded WI-243
  lesson — "warns get IGNORED by autonomous agents; fail closed." It is the
  same defect class one layer down, in the exact subsystem that exists to be
  fail-closed. Verified by direct read of `record_critique_verdict`.
- **Fix:** treat an unparseable verdict exactly like a missing verdict file
  (cool + re-critique), and add the same guard to `record_review_verdict`
  (don't consume the phase on `verdict is None`). Add
  file-present/machine-line-absent tests for both paths.

#### H-2 · Session timeout/interrupt kills only the direct child; the agent process tree survives
- **Location:** `project-trajectory/scripts/agent_session.py:326-331`
- **Evidence:**
  ```python
  except subprocess.TimeoutExpired:
      proc.kill()
      proc.wait()
  ```
- **Problem:** `proc.kill()` terminates only the direct child. On Windows the
  direct child of a `.cmd` shim (npm-installed CLIs) is `cmd.exe`; the real
  node process survives. On POSIX there's no process group
  (`start_new_session`), so CLI-spawned children survive too. The coordinator
  then logs TIMEOUT and launches the *next* session in the same worktree while
  the orphan is still editing it — two concurrent writers in one checkout,
  the precise hazard `out/agent-loop.lock` exists to prevent (the lock guards
  coordinators, not sessions).
- **Why it matters:** "safe to walk away from" is the unattended layer's one
  job; a timeout that leaves a live writer behind is worse than no timeout.
- **Fix (stdlib, cross-platform):** POSIX — `Popen(..., start_new_session=True)`
  then `os.killpg(...)`; Windows — `taskkill /F /T /PID` (ships with the OS).
  No test covers tree survival today.

#### H-3 · Spine trains lose their `spine` class on park/reconcile — serialization AND ratification gate silently bypassed
- **Location:** `project-trajectory/scripts/agent_dispatch.py:2563`, `:2595`, `:2424`, `:2451`
- **Evidence:**
  ```python
  parked[tid] = {"state": state, "wis": wis, "base": info["base"]}   # spine dropped
  ...
  _spawn_worker(..., lane["wis"], lane["base"], spine=False)          # resume
  ```
- **Problem:** the `spine` bit exists only in the in-memory lane. It is
  dropped at park, absent from reservation metadata, and every resume path
  hardcodes `spine=False`. Consequences: (a) a spine worker that rate-limits
  resumes as a non-spine lane, so ordinary cars dispatch beside it — the
  "spine serializes whole-project" invariant (WI-204) is void after one rate
  limit; (b) the gate-ratification stop lives only in
  `_worker_exit_decision(code, spine, gate_policy)` — a crash-restarted
  dispatcher classifies a built spine train `ready-to-integrate` and
  integrates + publishes it with **no ratification ask** under
  `attended`/`single-ratify`. `tests/test_agent_loop_recovery.py` has zero
  spine coverage.
- **Why it matters:** the human-attestation gate on spine work is one of the
  kit's headline trust guarantees; it currently only holds on the happy path.
- **Fix:** persist `"cls"` in the `reserve_traincar` meta JSON
  (backward-compatible), restore it in `_reservation_trains` /
  `_reconcile_reserved_train` / resume paths, and gate reconciled-spine
  integration on the same ratify ask (absent `cls` → conservative spine
  default). Needs its own reviewed WI + recovery tests — not a drive-by.

#### H-4 · Windows `.cmd`-shim argv path re-parses repo-sourced text (BatBadBut class)
- **Location:** `project-trajectory/scripts/agent_session.py:269-271`, `:66-72`
- **Evidence:**
  ```python
  resolved = shutil.which(argv[0], ...)      # explicit .cmd runs fine (WI-120)
  ...
  argv.append(tok.replace("{model}", model).replace("{prompt}", prompt))
  ```
- **Problem:** when argv[0] is a `.cmd`/`.bat` shim, CreateProcess runs it via
  `cmd.exe /c`, which re-parses the command line: an embedded `"` toggles
  cmd's quote state and re-exposes `&`/`|` as live operators, and `%VAR%`
  expands. Substituted values are repo-influenced: `{model}` comes from
  `docs/agents.csv` (a tracked file worker sessions can edit); the shipped
  interactive template rides the vendored guardrails doc as `{prompt}` in
  argv. The kit already solved exactly this in `run_menu._win_quote`;
  `agent_session` never got the treatment.
- **Why it matters:** a poisoned model cell or guardrails doc becomes command
  execution on the operator's machine — a prompt-injection→command-injection
  bridge in the layer that runs unattended.
- **Fix:** validate every substituted `{model}` against a conservative slug
  charset (`[A-Za-z0-9._:-]+`), failing closed with a named reason (closes the
  unattended-path hole). For `{prompt}`-in-argv on shim CLIs, prefer refusing
  and requiring stdin delivery — that half is a compat decision (the shipped
  interactive template uses argv) and should be its own change.

#### H-5 · The forward-only status.md rule is currently violated AND structurally unenforceable
- **Location:** `project-trajectory/scripts/check_trajectory.py`
  (`status_forward_only_findings`); `docs/status.md:69-74`;
  `docs/enforcement-audit.md:26`
- **Evidence:** the guard's docstring: "when status.md carries the kit's
  generated-block marker … the token rule stands down … no status.md generator
  exists yet" — while `gen_trajectory.py --status` *is* that generator and
  this repo's `docs/status.md` carries `<!-- BEGIN GENERATED STATUS -->`. And
  the file itself: "**Standing floors just armed** (2026-07-20,
  WI-251/252/254 …)" — all three WIs are `done`.
- **Problem:** because the marker is present, the done-id rule stands down for
  the **whole file**, so the hand-authored half of the owner's flagship
  forward-only discipline is enforced by nothing; and it has already accreted
  a dated, backward-looking bullet naming three closed WIs.
  `enforcement-audit.md` still classifies the rule Primary=Harness, which is
  false for this repo's own instance.
- **Why it matters:** the repo's own thesis — "prose-only rules get skipped by
  autonomous agents" — is being re-proven on its own status file, on the
  owner's top-priority rule.
- **Fix:** delete the accreted bullet; scope the stand-down to the generated
  block only (hand-authored region stays policed); refresh the stale
  docstring; re-class the enforcement-audit row honestly. Test the scoped
  behavior.

#### H-6 · Entry-point docs teach the retired hand-set gate model and hand-edited check.py
- **Location:** `project-trajectory/KICKOFF_PROMPT.md:85-86` and `:81-84`;
  `project-trajectory/STATUS.template.md:30-31`;
  `project-trajectory/README.md` "How to use" step 3
- **Evidence:** KICKOFF: "closing a gate **bumps it in a reviewed commit**";
  STATUS.template: "_(mirror it in the one-line `docs/gate` file …)_"; kit
  README: "edit the step list `scripts/check.py`'s `steps()` returns". Against
  PROCESS.md §4: "`docs/gate` is generated by `scripts/derive_gate.py` …
  **never a manual bump**" and §7: "you wire these to your stack in one file,
  `docs/stack.ini` … keeping `check.py` take-wholesale on a re-sync."
- **Problem:** the two documents a newcomer reads first (and the template that
  scaffolds into every repo's daily-read status file) instruct exactly the
  hand-edits that `derive_gate.py --check` (a pre-commit floor step) rejects
  and that break the ADOPTING.md re-sync contract. Neither entry doc mentions
  `derive_gate.py` at all.
- **Why it matters:** an agent following KICKOFF will hand-edit `docs/gate`
  and fail its own hook; an adopter following the README will make `check.py`
  un-upgradeable. This inverts the SSOT promise precisely at the front door.
- **Fix:** three one-sentence rewrites (derived gate; stack.ini), mirrored in
  KICKOFF's harness bullet.

#### H-7 · PROCESS_OPTIONS.md contradicts itself on the dispatcher default, the reviewer dial, and status.md's role
- **Location:** `project-trajectory/PROCESS_OPTIONS.md` lines 2266-2269 vs
  2349-2351; 666-668 vs 689-690; 554-555 vs 874-877 (plus PROCESS.md §5/§6,
  AGENTS.template.md:63-64)
- **Evidence:** "**A plain launch is the dispatcher** … the legacy serial
  resume driver is retired" vs, ~80 lines later, "a repo that never opts in …
  keeps the legacy single-session resume loop, byte-for-byte unchanged."
  "the loop surfaces the dial in its banner but **never enforces it**" vs "when
  a repo opts into managed routing the loop ***enforces* it**." "status.md is a
  generated snapshot for humans, **never a session's input**" vs "leaves
  `status.md` holding only **the resume point** … the next fresh session's
  context reload."
- **Problem:** three direct self-contradictions in the canonical options doc,
  fossils of the WI-180/210 migrations. The code settles each (dispatcher is
  the default; managed mode schedules review rounds; the generated-snapshot
  model is partially landed), but a reader gets a coin-flip.
- **Why it matters:** this is the kit's own core sin per its own rules — one
  fact, two homes, drifted.
- **Fix:** delete/rewrite the stale sentences; scope the generated-status
  claims ("once the integrator generates status.md — not yet fully shipped");
  keep §-numbering untouched.

#### H-8 · 21 of 27 shipped skills cite knowledge files that do not exist anywhere
- **Location:** e.g. `project-trajectory/skills/ui-accessible-component/SKILL.md:19`
  (+20 more; verified by grep — 21 files)
- **Evidence:** `**Knowledge:** KNOWLEDGE-LIBRARY.md §A1`,
  `FIELD-KNOWLEDGE-GILBERT.md §G2`, `FIELD-KNOWLEDGE-NOTHOMEWRECKER.md §F1` —
  none of the three files exists in the repo.
- **Problem:** the knowledge library was split into `knowledge/*.md` and
  nobody updated the 14 consumers; the two FIELD-KNOWLEDGE files are private
  pilot notes that never shipped (7 citations). All 21 skills are
  `scope: kit`, so every adopter materializes instructions pointing agents at
  unfindable files.
- **Why it matters:** load-bearing citations that dead-end are exactly the
  drift this kit exists to prevent, shipped 21 times over.
- **Fix:** rewrite the 14 KNOWLEDGE-LIBRARY citations to
  `docs/knowledge/<pack>.md` (noting the pack ships only under the matching
  `--domain`), delete the 7 FIELD-KNOWLEDGE citations; regenerate INDEX.csv +
  per-agent copies.

#### H-9 · `gen_trajectory.py` is a 4,357-line module fusing five unrelated subsystems
- **Location:** `project-trajectory/scripts/gen_trajectory.py` (whole file;
  the `--status` git-projection subsystem is lines ~3616-4270)
- **Problem:** one namespace holds spine/CSV/OKF parsers, a Sugiyama layout
  engine, a Bézier obstacle router, six panel emitters, ~450 lines of CSS/JS
  string constants, and a git-ref-scanning status projector that shares
  nothing with rendering. Every edit to any subsystem shares one review
  surface and one perceptual-gate blast radius — the project's own
  "file MINORs forward" tax is partly a decomposition symptom.
- **Why it matters:** highest-churn file in the repo; the change surface, not
  today's correctness, is the risk. The complexity ratchet can't see this
  axis (it pins per-function C901 only — see M-26).
- **Fix (defer to a WI):** extract `--status`/`--pending` into a sibling
  `gen_status.py` (needs only the already-imported `check_trajectory`; add to
  bootstrap MAPPING; thin deprecation shim). Removes ~650 lines and takes the
  status projector out of the perceptual-gate blast radius. Do not split the
  emitters from the shell (shared DRILL assets).

#### H-10 · No LICENSE file (known, owner-parked as OI-4/WI-097)
- **Location:** repo root (verified: no LICENSE/COPYING/NOTICE anywhere in
  tracked tree)
- **Problem:** the kit's whole model is copy-in — the license travels with
  every scaffold — and there is none; default all-rights-reserved applies.
- **Why it matters:** every downstream adoption is legally ambiguous until
  ruled.
- **Fix:** **deferred by design** — `docs/open-items.md` OI-4 correctly parks
  this on the owner's public/private intent (MIT vs Apache-2.0 vs stay
  private). Flagged here for priority, not action.

#### H-11 · INTERFACES.template.md contradicts the registry it fronts; its worked example is malformed CSV
- **Location:** `project-trajectory/INTERFACES.template.md:40, 63-67`
- **Evidence:** doc vocabulary `Draft·Agreed·Implemented·Verified` vs the
  shipped registry's "Status is open-vocab (Draft|Proposed|Active|Stable|
  Deprecated)" (and specs templates mandating `Proposed`); doc lists 9
  columns vs the registry's 11; the example snippet has a 10-column header
  with 9-field rows.
- **Problem:** an adopter who seeds `interfaces.csv` from this doc's example
  fails their own pre-commit integrity floor on the first commit
  (`trace.py structure_findings` column-count rule).
- **Why it matters:** a template whose worked example fails the kit's own
  checker is the sharpest possible copy-readiness violation.
- **Fix:** regenerate the doc's table + snippet from the current registry
  template; align Status vocabulary with the open-vocab wording.

### Medium

#### M-1 · `Verification` cell compared unstripped at the three G3 decision points
- **Location:** `project-trajectory/scripts/trace.py:1440` (also 1428-1437)
- **Problem:** `llr_exempt()` strips its cell (a prior review fix, pinned by
  `test_rule_sync`), but `--require-verified` and the attested/mechanized
  split compare raw: `"Test "` (trailing space) passes `--strict-schema` (the
  enum check strips) yet is silently skipped by the G3 status criterion —
  a false PASS; `"Attest "` counts as *mechanized* in the trust report.
- **Fix:** strip once per row, use at all three points; add the padded case to
  the test battery.

#### M-2 · `gen_cases.py --format csv` emits a stale 9-column TC row (registry is 11 columns)
- **Location:** `project-trajectory/scripts/gen_cases.py:247-257`
- **Problem:** the "ready to paste" rows lack `Evidence`/`Phase`, so pasted
  raw they trip trace.py's always-on structure check; hand-realigned, the
  stamped `Automated=Yes` with empty Evidence trips `--strict-schema` at G3.
  The generator contradicts the checker; `test_gen_cases.py` never exercises
  `--format csv` (found independently by two review passes).
- **Fix:** emit the 11-column header/rows; add a one-line test pinning the
  emitted header to the template's header.

#### M-3 · `trace.py --strict` failures print only counts; the findings live in a gitignored report
- **Location:** `project-trajectory/scripts/trace.py:1886-1941` (`render_console`)
- **Problem:** gating findings (orphans/integrity/status/schema/placeholder)
  are never written to stdout — only counts plus a pointer to
  `docs/test/report.md`, which is gitignored. check.py's own creed: "We print
  the real command output; we do not summarize it away." Autonomous agents act
  on what's in their face (the owner's recorded lesson).
- **Fix:** on nonzero exit, print the first N findings per class with a
  "+K more in report.md" tail.

#### M-4 · Inconsistent decode-error policy: content readers crash raw on non-UTF-8; BOM gaps
- **Location:** `trace.py:1196`, `:594`; `derive_gate.py:205`;
  `check_docs.py:213/468/493/540`; `check_doc_refs.py:131/147`;
  `check.py:200`; also `gen_okf.py:511`, `gen_arch_map.py` scan paths,
  `gen_trajectory.py:175/430/2391/4240/4330`
- **Problem:** the kit has a stated policy ("degrade a stray byte, don't crash
  (C8)") applied to policy files and git output, but every *content* reader
  (stakeholder-needs.md, markdown docs, stack.ini) reads strict UTF-8: one
  cp1252 curly-quote turns the gate chain into a traceback with no
  file-naming finding. A BOM'd stakeholder-needs.md silently defeats the
  first-heading draft rule. Windows-first hazard in a Windows-first kit.
- **Fix:** standardize `encoding="utf-8-sig", errors="replace"` for prose
  reads; wrap `load_csv` decode errors into an integrity finding naming the
  file.

#### M-5 · Two definitions of "G3-ready SR": derive_gate demands Verified for every SR; trace's `--require-verified` only for `Verification=Test`
- **Location:** `derive_gate.py:160-171` vs `trace.py:1440`
- **Problem:** a decomposed SR with `Verification=Demonstration,
  Status=Implemented` can never derive G3, yet `check.py --gate G3` (explicit
  override, or gate-file-absent `all`) reports PASS — the two scripts disagree
  about the gate the kit exists to make honest. `test_rule_sync` pins four
  smaller policy pairs but not this one.
- **Fix:** **spec call** — decide in the derived-gate model doc (widen trace's
  criterion or narrow sr_gate's), then pin the pair in `test_rule_sync`.
  Deferred to owner/WI; not a drive-by.

#### M-6 · `derive_gate._per_phase` drops LLR/TC rows that don't cite an SR id directly
- **Location:** `derive_gate.py:273-282`
- **Problem:** a TC whose `Verifies` cites only its LLR (legal, common) is
  bucketed under the LLR id, which the per-SR lookup never reads: a Draft TC
  in that shape drops the repo's raw min to G0 while the per-phase entries
  stay G2/G3 — the phase-drop detector then points at nothing.
- **Fix:** resolve TC refs through the LLR→SR map before bucketing; fixture
  test.

#### M-7 · trace.py structure: 2,077-line module, ~360-line `analyze()`, attribute-bag classes
- **Location:** `trace.py:1215-1575`, `:1127-1136`
- **Problem:** `Registries`/`Findings` are empty classes populated by external
  attribute assignment — a typo'd attribute silently creates a new one. Every
  new registry adds parallel edits at four sites.
- **Fix (defer):** within the single-file convention: per-tier analyze
  functions + dataclasses/`__slots__`. Refactor WI, not a patch.

#### M-8 · Dashboard JSON guard stops `</` but not `<!--` — adopter text can kill all dashboard JS
- **Location:** `gen_trajectory.py:3585-3587` (and 3 inline `dj` sites)
- **Problem:** per HTML5 script-data states, `<!--` + a later `<script` puts
  the parser in double-escaped state; the block's real `</script>` no longer
  closes it. Registry text containing `see <!-- old` plus any later `<script`
  breaks every tab's interactivity. Not injection, but data-driven page-wide
  breakage; no test covers hostile text through the embedded JSON.
- **Fix:** `json.dumps(...).replace("<", "\\u003c")` in `j()` and the inline
  sites (supersedes the `</` replace); add the seam test. **Render-surface
  change — must ride a render WI with regenerated artifact + fresh critique
  per the WI-243 protocol.**

#### M-9 · CMP `PartOf` cycle crashes the renderer (checker passes); two-parent CMPs emit duplicate layers
- **Location:** `gen_trajectory.py:1045-1061` (`emit_cmp_layer`)
- **Problem:** `subtree_modules` and `ct._cmp_roots` are cycle-guarded; the
  layer-emission recursion is not — `A PartOf B, B PartOf A` recurses to
  RecursionError. trace.py validates only that `PartOf` names known ids, not
  acyclicity: checker green, renderer traceback.
- **Fix:** `{cid: lid}` memo in `emit_cmp_layer` (fixes both); acyclicity
  ERROR beside the PartOf-resolution check. Render-surface (same protocol
  note as M-8).

#### M-10 · `--status --check` byte-compares a projection of machine-local, unpushed git state
- **Location:** `gen_trajectory.py:4036-4059` + `check.py:585-590`
- **Problem:** `refs/llm/*` (conflicts, reservations) don't transport with
  clone/push, so the committed `open-items.md` projection generated on the
  dispatch machine reads STALE in any other clone (CI, second machine) —
  a freshness gate that isn't a pure function of the committed tree.
- **Fix:** **design decision** — exclude ref-derived lines from the compare,
  degrade to WARN when the namespace is absent, or document the gate as
  dispatch-machine-authoritative. Deferred.

#### M-11 · `_splice_status` lacks its sibling's hardening: CRLF whole-file churn; inverted markers corrupt silently
- **Location:** `gen_trajectory.py:4213-4229`, `:4240-4267`
- **Problem:** `_splice_pending` preserves dominant EOL and fails closed on
  duplicated/inverted markers (tested); `_splice_status` predates that — a
  CRLF checkout's hand-authored status.md gets rewritten wholesale as LF, and
  an inverted marker pair produces garbled text.
- **Fix:** port the pending splicer's logic (arguably one parameterized
  function). Render-surface protocol applies.

#### M-12 · The fail-closed perceptual gate is fail-open when the newest critique file is untracked
- **Location:** `check_trajectory.py:1631-1643`, `:1679-1681`
- **Problem:** the newest `*-CRITIQUE.md` is selected from the filesystem but
  timed from git; an uncommitted file has no commit time → finding suppressed
  even under `--strict`. An agent that writes the verdict before committing
  (or abandons it) gets a green gate from a gate the owner ruled fail-closed;
  the ratchet reads the same untracked file.
- **Fix:** when selected evidence has no commit time, fall back to the newest
  *committed* critique or emit the finding (evidence not durable ⇒ stale).

#### M-13 · The flat WI DAG (layout + O(E·V) obstacle routing + SVG assembly) is computed then discarded whenever the tiered view renders
- **Location:** `gen_trajectory.py:3545-3550`
- **Problem:** for >3 workstreams (this repo: 5, 256 WIs) the full `dag_svg`
  pipeline runs solely to be thrown away — only the details dict survives.
  Most expensive pass in the generator, dead work exactly at scale.
- **Fix:** extract the details-dict loop; call `dag_svg` only when needed.
  Render-surface protocol applies.

#### M-14 · `bootstrap.py --sync` cannot fix deleted-source drift; the gate's own remediation hint is wrong
- **Location:** `bootstrap.py:506-517`; `gen_skills_index.py:96-103, 232-235`
- **Problem:** `sync_agent_skills` copies but never deletes; when a kit skill
  removes a file, `--check-agents` (pre-commit floor) goes red with "file set
  differs" and prescribes `--sync`, which cannot fix it — every commit blocks
  until someone manually deletes the stray. No deleted-source test exists.
- **Fix:** delete dest files absent from source (subtree is kit-owned by
  contract); add the test.

#### M-15 · Bootstrap text writes produce CRLF on Windows — including the seeded `agent-resume.sh`
- **Location:** `bootstrap.py:569`, `:1724-1727`, plus every `write_text` site
- **Problem:** the `.py` branch avoids `write_text` for exactly this reason
  (its own comment); the seeding rewrite then converts `agent-resume.sh` to
  CRLF — "a CRLF shebang breaks `#!/bin/sh`" per the kit's own
  gitattributes.template. All `.md`/policy scaffolds are platform-dependent
  bytes.
- **Fix:** route every text write through one `open(w, encoding="utf-8",
  newline="\n")` helper (the pattern gen_arch_map/gen_okf already use); add a
  `b"\r" not in seeded` assertion.

#### M-16 · Windows launchers trust the Microsoft-Store `python` alias — the trap the kit's own hooks document and avoid
- **Location:** `run.template.cmd:14-15`; `agent-resume.template.cmd:62-63`
  (and this repo's `agent-resume.cmd:81-82`); `setup.ps1:9-13`;
  `dev-setup.template.ps1:65,100`
- **Problem:** `where python` / `Get-Command python` succeed on the Store
  app-execution stub (exit 9009 nag on run); `dev-setup.ps1` even reports
  `[ok] runtime` for it. The hooks probe by *running* the candidate — the
  four evaluator-facing files never got the same treatment (found by two
  passes independently).
- **Fix:** probe `python -c ""` exit status before trusting; mirror the hook
  pattern in the PowerShell loops.

#### M-17 · `gen_release_checklist.py` is effectively untested
- **Location:** only functional exercise: `tests/test_check_perf.py:244-253`
- **Problem:** the script that produces the G-Release human sign-off record
  has one incidental happy-path invocation. Untested: the `--phase` scope
  filter (incl. the foundation-phase `min()` rule), LLR-parent phase
  resolution, blank-`Automated`-counts-as-manual, `--version` routing — the
  exact invocation the shipped reference CI runs on every release tag. A
  phase-filter regression would silently *drop human verification items from
  the release checklist* (found by two passes independently).
- **Fix:** add `tests/test_gen_release_checklist.py` covering phase filter,
  TC-cites-LLR-only, blank Automated, `--version` path.

#### M-18 · Default walk-away config has no session timeout and no dispatcher watchdog
- **Location:** `agent_loop.py:1363-1368`; both launchers (no
  `--session-timeout` in any slot); `agent_dispatch.py:2490-2491`
- **Problem:** default `0` → `proc.wait(timeout=None)`; a hung CLI blocks a
  worker forever (stall guard/blackout/pause can't fire inside `wait()`), and
  the dispatcher has no wall-clock watchdog — a permanently occupied lane in
  the flagship unattended mode. The docstring's promise only holds if the
  operator opts in; the shipped launchers don't.
- **Fix:** wire a generous timeout into the launcher slots (and consider a
  non-zero code default); land together with H-2 (a timeout that leaks the
  tree makes things worse).

#### M-19 · Session transcripts are auto-committed to tracked history with no secret redaction
- **Location:** `agent_common.py:649-691`, `:780-817`
- **Problem:** head+tail of every session's raw output — including CLI auth
  errors that echo keys — is committed into `docs/iteration/*.log`
  permanently; nothing scans content (privacy layer checks author identity
  only). `push-policy: human` is the only barrier before publication.
- **Fix:** stdlib redaction pass over well-known token shapes (`sk-…`,
  `ghp_…`, `AKIA…`, `Bearer …`) in `bounded_transcript`/`write_session_log`,
  with an honest imperfection note.

#### M-20 · Malformed declared policies fail open silently (blackout disables; review-policy downgrades to 1)
- **Location:** `agent_common.py:154-166`; `agent_loop.py:2810-2814`, `:2232-2233`
- **Problem:** a typo'd `docs/blackout` silently disables a policy the
  scaffold ships enabled; a typo'd `docs/review-policy` silently halves review
  coverage — inconsistent with the kit's own posture for `agents-enabled`
  ("the consent surface — never silently ignored"). A test currently locks in
  the silence.
- **Fix:** startup stderr warnings for both malformations (behavior can stay
  fail-open for compat; the *silence* is the defect); update the pinning
  test.

#### M-21 · `subagent-gate.log` is written into tracked `docs/` and gitignored nowhere
- **Location:** `subagent_gate.py:111-120`, `:139-140`
- **Problem:** every spawn decision (including allow-when-off) appends to
  `docs/subagent-gate.log`; untracked dirt blocks `worker_endstate` DONE
  ("a dirty tree is not done"), burns budget, and eventually gets committed
  as junk.
- **Fix:** write to `out/subagent-gate.log` (already ignored; paper trail
  intact).

#### M-22 · A pre-existing file at the predictable verdict path is accepted as the reviewer's verdict
- **Location:** `agent_loop.py:1941-1947`, `:1985-1997`
- **Problem:** verdict paths are fully predictable (`NNN-REVIEW-A-<sha7>.md`
  where sha7 is the implementer's own HEAD); an implementer that plants an
  *uncommitted* APPROVE there gets it counted whenever the review session
  errors — and the inline "caught upstream (SR-096)" comment overstates: the
  integrator verifies name/head match, not provenance. (The sha-in-filename
  design genuinely defeats *committed* pre-planting.)
- **Fix:** unlink any pre-existing file at `verdict_path` before launching a
  review/critique session; soften the comment.

#### M-23 · Two divergent CSV readers split the system's view of a BOM'd registry — and can silently vacate the critique layer
- **Location:** `agent_common.py:476-483` vs `schedule.py:99-103`
- **Problem:** `_read_csv_rows` reads `utf-8` + `splitlines()` (header becomes
  `﻿WI-ID`, quoted multi-line cells break); `schedule.load_rows` uses
  `utf-8-sig`. One worker holds both views: the dispatcher assigns from one,
  preflight refuses from the other. Same reader feeds `load_critique_srs` — a
  BOM'd system-requirements.csv silently disables the entire critique gate.
- **Fix:** `open(newline="", encoding="utf-8-sig")` + DictReader on the file
  handle; BOM regression test.

#### M-24 · Documented suite-runtime claims (~47 s smoke / ~66 s full) are badly stale
- **Location:** `CLAUDE.md` ("Self-test before claiming done");
  `docs/stack.ini:17-19` comment
- **Problem:** the full suite measured 280.7 s on a 24-core box during this
  review (shared with review load — the true number is lower, but not 66 s;
  two prior reviews already flagged these numbers and the suite has grown 25%
  since). These figures budget every agent's self-test decision; an agent
  budgeting 47 s and paying minutes starts "optimizing" (skipping) the bar.
- **Fix:** re-measure on a quiet box and re-stamp with a date + machine class,
  or drop absolutes for "measure locally."

#### M-25 · ~60-100 lines of scaffold copy-pasted across 11 agent_loop test files — unpoliced by the repo's own dupes gate
- **Location:** `tests/test_agent_loop_dispatch.py:36-98` and 10 siblings
- **Problem:** `_git` defined identically 11×, the WI CSV `HEADER` 5×,
  `_make_repo` 6×, and the fake-agent trailer parser in 6+ module-level FAKE
  strings; the G3 dupes gate scopes `--src` to `project-trajectory/scripts`
  only, so tests are a blind spot. A trailer-protocol change means editing 6+
  embedded fakes in lockstep.
- **Fix (schedule, don't drive-by):** `tests/_loop_helpers.py` with the shared
  scaffold + one parameterized fake-agent template (~10 files touched).

#### M-26 · The complexity ratchet is blind to the growth axis that motivated it
- **Location:** `tests/test_complexity_ratchet.py:35-94`
- **Problem:** exact bidirectional C901 pinning is genuinely good, but
  per-module LOC is unmeasured: you can grow a file by thousands of lines
  (how gen_trajectory.py got to 4,357) while the ratchet stays green; and a
  BASELINE edit in the same commit as the growth is prose-policed only.
- **Fix (defer to WI-226 workstream):** companion per-module LOC baseline in
  the same exact-match style; reviewer rubric explicitly diffs BASELINE
  edits.

#### M-27 · CI has no `timeout-minutes` and no `concurrency` anywhere; the shipped reference CI exports the same omission
- **Location:** `.github/workflows/test.yml`, `canary.yml`;
  `project-trajectory/ci/check.yml`
- **Problem:** this suite spawns coordinator loops and pollers with real
  timeouts (60 s rendezvous, 300 s dispatch); a wedge burns GitHub's
  360-minute default × 5 matrix cells, and stacked pushes queue redundant
  runs.
- **Fix:** `timeout-minutes` per job + a `concurrency` block keyed on ref;
  mirror into the shipped check.yml.

#### M-28 · Dispatcher integrator: unguarded `ValueError` from `_rewrite_wi_rows` crash-loops on the integrate/dual paths
- **Location:** `agent_dispatch.py:1558`, `:1746-1758` (guarded correctly at
  `:1681-1684`)
- **Problem:** the blocked path got the WI-238 try/except; integrate and dual
  didn't. A headerless registry kills the dispatcher *after* the staging
  merge, stranding the worktree with reservations held; relaunch reconciles
  the same train → same crash, until a human intervenes.
- **Fix:** wrap both sites in the same `→ "error", _reset_failed_disposition`
  idiom; tests for each path.

#### M-29 · Integrator verdict gate counts CRITIQUE approvals and ignores exact-head CHANGES-REQUESTED
- **Location:** `agent_dispatch.py:1519-1528`, `:785`
- **Problem:** `review-policy 2` is satisfied by REVIEW-A APPROVE + CRITIQUE
  APPROVE while a REVIEW-B CHANGES-REQUESTED at the same head never blocks —
  weaker than the in-train rule (`score_reviews.merge_verdict`: any
  CHANGES-REQUESTED blocks) the integrator supposedly independently verifies
  (SR-096).
- **Fix:** **design call** — count only REVIEW-[AB] phases toward the dial and
  define a deterministic latest-file-per-phase rule for CHANGES-REQUESTED;
  needs its own reviewed WI + tests.

#### M-30 · Dual-plan routing silently degrades to the ambient template when agents.csv is missing/malformed but the enable-list exists
- **Location:** `plan_runner.py:90-93`
- **Problem:** the documented consent posture is "unresolvable ids PAGE
  loudly"; an enable-list with a broken registry instead collapses both hats
  (and critic legs) onto one template with no page and no family diversity —
  while BUILD workers fail preflight loudly on the identical condition.
  `_errors` is discarded even when non-empty.
- **Fix:** PAGE when `enabled` is non-empty but registry is empty/erroring —
  mirroring the resolve-errors branch below it; test.

#### M-31 · Per-phase draw weights (WI-236) are largely inert across trains
- **Location:** `agent_common.py:834-854`; `agents-enabled` comment
- **Problem:** the draw ordinal counts prior same-phase sessions *on this
  train only* and every train is freshly minted — so every train's first
  REVIEW-A draw is slot 0, deterministically; the advertised "weight 4 draws
  ~4× as often" materializes only within multi-round trains. The supporting
  test runs 18 rounds on a single train — exactly the case that hides the
  reset.
- **Fix:** **design call** — cross-train ordinal (drop the train prefix) or
  document weights as within-train only; two-train share test either way.

#### M-32 · Stale (manually deleted) train worktree crashes the dispatcher in a relaunch loop
- **Location:** `agent_dispatch.py:463-465`, `:2499-2505`
- **Problem:** `git worktree list` keeps listing removed directories until
  prune; `lease_worktree` returns the path unchecked and `Popen(cwd=…)`
  raises uncaught. A user tidying `../<repo>-trains/` bricks unattended
  operation (the kit never prunes worktrees — see L-24).
- **Fix:** `is_dir()` check + `git worktree prune` fallback in
  `lease_worktree`; `except OSError → quarantine` around the spawn.

#### M-33 · `plan_artifacts` reads the WI registry BOM-blind — duplicate/empty WI-IDs can enter the serialized integration commit
- **Location:** `plan_artifacts.py:133`, `:145`
- **Problem:** every sibling reader uses `utf-8-sig` for exactly this; here a
  BOM makes `_existing_wi_nums` find zero ids (children mint from WI-001,
  colliding) and `_registry_header` feeds `﻿WI-ID` to DictWriter
  (`extrasaction="ignore"` drops the real id → empty id cells appended).
- **Fix:** `utf-8-sig` at both opens + strip BOM from the returned header.

#### M-34 · Escalation "win-stay" half is doubly dead: margin threshold unreachable; `next_primary` never consumed
- **Location:** `agent_route.py:122`, `:807`; `agent_loop.py:1976, 2030-2031`
- **Problem:** recorded margins are bounded by 1.0; the default threshold is 2
  and env overrides parse with `int()` — so `next_primary` is always None
  under any sane config, and no caller reads it anyway. The documented
  win-stay/lose-shift policy is prose-only; its test fabricates `margin: 3`,
  a value the pipeline cannot produce.
- **Fix:** float default (e.g. 0.15) + `float()` env parse + a
  reachable-margin test now; wiring-or-deleting `next_primary` is a design
  call for a WI.

#### M-35 · WI-229's attested migration left ~10 active spine rows citing superseded SR ids as live authorities
- **Location:** `docs/requirements/system-requirements.csv` (SR-026, SR-042,
  SR-052/053/054 rationale); `low-level-requirements.csv`
  (LLR-053/054/055/057); `docs/test/test-cases.csv` (TC-053/054/055)
- **Problem:** the owner-attested plan required active semantic back-links be
  moved to the narrow replacement ids; these Verified rows still lean on the
  composite ids (`SR-047 loop`, `SR-051's tiering`, `SR-057/SR-064`).
  Traceability survives via the stubs, but the migration's own bar wasn't
  fully executed.
- **Fix:** sweep the cited rows to SR-084..086 / SR-089..092 / SR-099..101 as
  applicable; regenerate OKF + dashboard.

#### M-36 · gate-policy.md asserts the gate "reads G2 today" while `docs/gate` says G3
- **Location:** `docs/gate-policy.md:26-27` vs `docs/gate:11-13`
- **Problem:** the deviation register embedded a point-in-time fact
  (2026-07-15) that the derived cache has contradicted twice since.
- **Fix:** dateless rewording ("the level never moves the derived gate").

#### M-37 · Both launcher headers claim "every docs/agents.csv row is Family=ANTHROPIC" — three families are enabled
- **Location:** `agent-resume.cmd:55-56`; `agent-resume.sh:54-55`
- **Problem:** the consent-editing surface asserts a provider topology false
  since WI-160 and doubly false since the OPENCODE enablement; a human
  reasoning from it concludes cross-provider dispatch is unwired. (Root
  README's "tree-checked" table has the same staleness: claims 6 rows /
  2 families; reality is 8 / 3.)
- **Fix:** update both headers + the README table row.

#### M-38 · R-A…R-F documented three ways; entry docs and PROCESS_OPTIONS both wrong
- **Location:** kit `README.md` rows 36/61; `PROCESS_OPTIONS.md:1516-1518`;
  truth in `check_trajectory.py:1037-1215`
- **Problem:** the kit README documents retired R-B/R-C as live and omits R-F;
  PROCESS_OPTIONS says R-D is retired without noting WI-200 restored its
  done-id half (so its claim is false — the checker flags exactly that).
- **Fix:** correct both prose homes to the code's rule set.

#### M-39 · PROCESS.md §4 gate bullets contradict the same section's method definitions (and trace.py)
- **Location:** `PROCESS.md` §4 G2 bullet vs methods paragraph vs G3 bullet;
  `KICKOFF_PROMPT.md:126-133` inherits it
- **Problem:** G2 bullet says "(or Analysis/Inspection)" where code exempts
  `Analysis/Inspection/Attest`; the G3 bullet lists three of the six non-Test
  methods. A human applying the bullets literally demands an LLR for an
  Attest SR (EXAMPLE.md correctly says the opposite).
- **Fix:** align both bullets with `LLR_EXEMPT` and the full method list;
  mirror in KICKOFF.

#### M-40 · Shipped templates leak meta-repo archaeology: WI ids, archived spec paths, private project names
- **Location:** `registries/work-items.template.csv:2`;
  `PLAN.template.md:4`; `OPEN_ITEMS.template.md:36`; `stack.ini.template:76`;
  `gitattributes.template:24`; `gate-advance/SKILL.md:26`;
  `stakeholder-needs.template.md:72`; `knowledge/*.md` + 
  `gaussian-splat-scene/SKILL.md:10` (gilbert / NotHomeWrecker / Craft)
- **Problem:** templates scaffold verbatim into adopters' `docs/`, citing this
  repo's WI-180/191/210/234/235/251/252 (which will eventually collide with
  the adopter's *own* WI numbers), two spec paths that resolve nowhere
  downstream (`docs/specs/parallel-wi-dispatch.md`,
  `docs/specs/derived-gate-model.md` — archived even here), a "§4a" that
  exists in no shipped doc, and three of the owner's private project names
  presented as directives ("gilbert's kinematics should be written in…").
  Same class: PROCESS_OPTIONS/ADOPTING cite "§14" of an unshipped plan.
- **Fix:** strip WI/Thread ids and private names from shipped surfaces;
  repoint dead spec paths at the surviving PROCESS/PROCESS_OPTIONS sections
  (the derived-gate section's "in the kit's meta-repo, not shipped" phrasing
  is the model).

#### M-41 · `check_perf`: a malformed metric value silently degrades a `Gate=fail` budget to SKIP (exit 0)
- **Location:** `check_perf.py:96-101`, `:184-186`, `:345-358`
- **Problem:** a missing metrics file is loud, but a present file whose
  hard-gated row turns non-numeric (`"480ms"`) drops that row to SKIP inside
  a green run — a hard gate that quietly stops measuring.
- **Fix:** malformed value on a `Gate=fail` row → FAIL (absent stays SKIP);
  per-row WARN line for gated SKIPs.

#### M-42 · Kit pre-commit/commit-msg fail OPEN without Python — even when `docs/privacy-check` is `true`
- **Location:** `project-trajectory/hooks/pre-commit:53-56, 79-82`;
  `hooks/commit-msg:33-36, 57-60`
- **Problem:** exit-0 skip on a Python-less box also skips the secrets floor
  and the declared privacy checks; the pre-push hook fails CLOSED for the
  same policy and already parses policy files in pure sh — the pattern
  exists, unapplied.
- **Fix:** when Python is unfindable and `docs/privacy-check` reads true,
  fail closed (sh-parse); keep the skip otherwise, note the trade in the
  existing comment.

### Low

Compact format — location · problem → fix.

- **L-1** `trace.py:2019-2028` vs `check_docs.py:796-798` · `--docs` is a
  *path* in trace/check_perf but a *subdirectory name* in check_docs, while
  trace's comment claims uniformity → make check_docs accept a path
  (join-under-root when relative) and fix the comment.
- **L-2** `trace.py:967, 971` · ratify view sorts SRs by `id_key(r["SR-ID"])`
  — a semantic misuse producing lexicographic order (SR-9 after SR-10) →
  numeric sort key.
- **L-3** `trace.py:912-948` · `ratify_lines` re-introduces the quadratic
  refs() joins WI-081 removed from the report path → reuse `_bucket_by_ref`.
- **L-4** `trace.py:1197` · SN tier has no duplicate-id detection; a
  draft+ratified duplicate silently exempts a ratified need → scan table rows
  for repeats and draft/non-draft doubles as integrity findings.
- **L-5** `trace.py:395-398` · a data row with content but a blank id is
  invisible to the entire integrity floor → flag "row with no {label}-ID".
- **L-6** `gen_trajectory.py:3028, 2947-2949` · client-side `esc()` doesn't
  escape quotes yet feeds an attribute context (OKF hrefs) → build anchors
  via `createElement`/`setAttribute`. (Render surface.)
- **L-7** `gen_trajectory.py:1306-1351` etc. · DRILL_SCRIPT/STYLE emitted ×3,
  four JS `esc()` copies, `_gate_value` re-implements the imported sibling's
  helper, two `_git` wrappers with different contracts → hoist/emit-once.
  (Render surface.)
- **L-8** `check_trajectory.py:1682-1687` · committer-time gates: rebase/
  amend/cherry-pick re-stamps evidence commits and can silently *clear* a
  stale perceptual gate; same-second commits invisible to strict `>` →
  document the window; consider ancestry checks.
- **L-9** `check_trajectory.py:1642` · "highest-numbered" critique pick is
  actually lexicographic (`sorted(glob)[-1]`) — breaks at 4 digits or an
  unpadded name → numeric key.
- **L-10** `gen_trajectory.py` seam-test gaps: no `</script>`/`<!--`-in-title
  test, no `_splice_status` inversion/CRLF tests, no CMP-cycle render test,
  `_detour_d` least-obstructed fallback unexercised → add with the M-8/M-9/
  M-11 fixes.
- **L-11** `bootstrap.py:465-472` vs `knowledge/README.template.md:30-32` ·
  appended index rows misfile `domain:` under the `Components` column and
  stamp a frozen `2026-07-09` date → emit header-shaped cells, drop the
  hardcoded date.
- **L-12** `gen_arch_map.reference.ps1:68,323-338` · `Write-Error` under
  `$ErrorActionPreference='Stop'` dies at the first stale doc; the
  accumulate-and-exit path is dead code (the kit documents this exact trap in
  dev-setup.template.ps1) → `[Console]::Error.WriteLine` + keep accumulation.
- **L-13** `onboard.template.cmd:42,84,92-96`; `agent-resume.template.cmd:54-58` ·
  UTF-8 em-dashes in `echo` lines render as mojibake under cp437/cp850 —
  in consent banners, against dev-setup.cmd's own ASCII rule → ASCII-ify;
  extend the ASCII test.
- **L-14** `hooks/pre-push:145,207` · the LLM reviewer runs inside the
  `while read` over the hook's stdin; a stdin-reading reviewer eats the
  remaining ref lines on a multi-ref push → `< /dev/null` both invocations;
  two-ref test.
- **L-15** `.githooks/pre-commit:18` · unconditional `.coverage*` sweep can
  race a live coverage run mid-write (the exact WinError-32 class WI-104
  closed) → age-guard the sweep.
- **L-16** `tests/test_bootstrap.py:119-122` · the action-pin test bans `@vN`
  but not `@main`/unknown refs, and deleting an action vacates its check →
  assert every `uses:` ref matches `@[0-9a-f]{40}`.
- **L-17** `tests/test_agent_loop.py:361-373` · the only wall-clock-relative
  test (+2/+3 min blackout window) can wedge the loop under a >2-min
  scheduler stall; `datetime.utcnow()` deprecation noise → widen to +30/+31,
  timezone-aware now.
- **L-18** `pytest.ini` ×2 · intentional pairing (meta opt-out tiering vs
  shipped opt-in) undocumented at the point of confusion; template lacks the
  `slow` marker a cargo-culted conftest would need → one header sentence
  each.
- **L-19** `test.yml:48,62` + `requirements-dev.txt:26` · the
  subprocess-coverage wiring guard skips in all 5 matrix cells (coverage runs
  only in the gate job), so the pytest-cov 5.x/Python 3.8 leg is
  CI-unverified → one cheap 3.8 coverage cell, or record the gap in
  enforcement-audit.
- **L-20** `agent_loop.py:2680-2690` · guardrails-inert warning computed from
  env maps, not the registry rows that actually run under managed routing →
  build the model set from enabled registry rows.
- **L-21** `agent_loop.py:1046-1060` · plain-text rate-limit sniffing scans
  the whole transcript; "the token limit resets at 9:00" in echoed content
  misclassifies a failed session as WAITING → scan only the last N lines.
- **L-22** `agent-resume.command:7-10` · exports `AGENT_JOBS=2` that
  `agent-resume.sh` unconditionally reassigns — a dead knob inviting silent
  misconfiguration → drop it or honor inheritance (documented).
- **L-23** `schedule.py:251-288` · `depth`/`reach` are recursive despite the
  "iterative" docstring — RecursionError on ~1000-deep hard chains → explicit
  stack; fix the docstring.
- **L-24** `agent_dispatch.py` · train/integrate worktrees under
  `../<repo>-trains/` are never pruned — unbounded disk accretion and the raw
  material for M-32 → prune on successful publish (WI).
- **L-25** `agent_dispatch.py:978-1010,1425-1431,2750-2756`;
  `plan_coverage_step.py:112-117` · subprocess text-mode without
  `encoding=`/`errors=` → locale-codec (cp1252) strict decodes inside the
  integrator; one bad byte = uncaught crash → `encoding="utf-8",
  errors="replace"` (matching the kit's own `git()` wrapper).
- **L-26** `agent_dispatch.py:791-796` vs `score_reviews.py:57-60` vs
  `plan_runner.py:66-69` · three verdict-line dialects; the integrator's is
  last-match, case-sensitive, quote-blind — prose quoting `VERDICT: APPROVE`
  flips a CHANGES-REQUESTED file fail-open → one shared parser.
- **L-27** `score_reviews.py:518-527` · two `--verdict` + one `--family` →
  IndexError; unlabeled `--record` pollutes the scoreboard under `?0`/`?1`
  keys → pad providers; skip placeholder keys.
- **L-28** `plan_runner.py:236-239,311`; `plan_coverage_step.py:121` · the
  "mechanical repair" prompt hands each planner the full coverage report incl.
  the rival's coverage diff (weakens two-planner independence at the cheapest
  gaming point); an exit-2 rerun can serve a stale report file → filter to
  the implicated plan's FAIL lines; ignore `out_path` on exit 2.
- **L-29** `plan_artifacts.py:232-252` · duplicate plan-local ids collapse to
  one minted id written twice; unknown predecessor tokens pass through
  verbatim → reject both (the caller has a PAGE channel).
- **L-30** `plan_briefs.py:66-67,122` · dual-plan prompt templates ship but
  bootstrap has no `prompts/` MAPPING entry and no doc names the expected
  downstream path — the opt-in is folklore (graceful PAGE when missing) →
  one sentence in PROCESS_OPTIONS/ADOPTING now; a `--dual-plan` copy step as
  a WI.
- **L-31** `agents.template.csv:7,9` · unquoted commas in Notes cells (9
  fields vs 8-column header; DictReader silently truncates) — a bad exemplar
  in the template that teaches CSV hygiene → quote the two cells.
- **L-32** `privacy-check.template:19`; `blackout.template:14` · the one
  fail-open shipped default (privacy off — documented, defensible) and a
  blackout that ships *active* 12:00-19:00 UTC (a fresh adopter gets sessions
  silently deferred with the reason buried in a dotfile) → owner call;
  consider shipping blackout disabled.
- **L-33** `docs/requirements/interfaces.csv` IF-057 · still
  Proposed/Experimental though shipped and consumed since WI-190/199 (its
  WI-201 siblings were ratified) → ratify or record why not (owner).
- **L-34** `docs/requirements/work-items.csv` WI-060/061/062/063/082 · live
  backlog rows whose only spec anchors are archive/log material the repo
  declares non-working → owner triage (re-spec or retire).
- **L-35** `docs/requirements/low-level-requirements.csv` LLR-050 · TestRefs
  reads `(see TC)` with no id (siblings say `(see TC-050)`) → fix the cell.
- **L-36** `docs/iteration_index.md:110-146` · lane-prefixed log names broke
  the lexicographic sort — dates interleave and "#" repeats → sort by date in
  the regenerator (WI).
- **L-37** `byte-budget-guard/SKILL.md:25-26,62-63` · the example report
  contradicts the skill's own baseline table (56,230/134,965 vs 60,169/
  159,787); AGENTS.template.md sits at 9,978/10,000 — **22 bytes of
  headroom** → refresh the example; treat the headroom as a live constraint
  on any AGENTS.template edit.
- **L-38** `PROCESS.md`/`PROCESS_OPTIONS.md` internal links are authored for
  the scaffolded `docs/` home (`process-options.md`, `rubrics/README.md`) and
  are dead at the shipped location, outside `check_docs.py`'s net → one
  header line ("links resolve at the scaffolded location"), or bootstrap-time
  rewriting (WI).
- **L-39** `KICKOFF_PROMPT.md:78-80` · restricts interfaces to cross-repo
  only, contradicting §8's intra-repo seams (adopters then hit connectivity
  warns they were told not to expect) → add "or module-to-module seams".
- **L-40** `PROCESS_OPTIONS.md:16` rows 39-40 · the applies-when index claims
  document order; two rows are swapped → swap back. Also `:1440` "uniquely …
  opt-out" is contradicted by three other opt-out layers in the same file →
  delete "uniquely". Also §4's `COVERAGE_THRESHOLD … record here` vs §7's
  stack.ini declared-home → point §4 at stack.ini.
- **L-41** `scripts/dev-setup.ps1:62-66` vs `dev-setup.sh:95` · the ps1
  variant (Windows — the platform that uses it) lacks the dashboard-shots
  report line the sh variant has → add the Report line.
- **L-42** `shoot.mjs:56` · the python-candidate picker returns non-venv
  candidates without existence checks (ternary makes the fallback dead) →
  restructure the loop.
- **L-43** `check.sh:8` · probes only `.venv/bin/python` (POSIX layout);
  Git-Bash-on-Windows users silently skip their venv (`hooks/pre-commit`
  probes both layouts) → probe `Scripts/` too.
- **L-44** `docs/status.md:75-78` + memory-file claims vs `docs/run-state`
  reading `RUNNING` with no dispatcher alive · residue self-heals on next
  reconcile; a truthful end-state on stop would be cleaner → WI-sized.
- **L-45** Five `datetime.utcnow()` sites in kit scripts (3.12 deprecation
  debt, flagged by a prior review, no WI filed) → mechanical sweep to
  timezone-aware now with naive-preserving conversion.

### Positive / good practices

- **P-1** The test suite is exceptional: meta-tests prove their own checks can
  fail (dogfood-sync mutates scratch copies; stdlib-only has a synthetic
  offender; smoke-tier guards its own partition), asserts pin real messages
  not exit codes, golden files are platform-normalized with a deliberate
  regeneration ritual, and the subprocess-coverage plumbing solves a genuinely
  hard problem cleanly.
- **P-2** CI/dependency hygiene: all three workflows SHA-pin actions with
  least-privilege permissions and a test enforcing the pins; the 3.8 floor is
  actually tested on Linux+Windows with a written macOS exclusion;
  `requirements-dev.txt` is a model constraint file with a scheduled
  non-gating canary; dashboard-shots pins playwright exactly with a 3-package
  lockfile.
- **P-3** Fail-closed engineering where it counts: the pre-push hook (BLOCK
  overrides zero exit; typo'd policy reads as the stricter posture — all
  tested), gen_okf/arch-map staleness gates, write-once scaffolding with
  tested idempotency, `check.py`'s missing-tool ≠ pass.
- **P-4** The unattended layer's core designs are better than most production
  orchestrators: kernel-lock coordinator guard (ENOLCK degrade tested),
  stdin prompt delivery (kills the 8191-char cap and the argv injection
  surface in one move), sha-named verdict files defeating committed
  pre-planting, all-or-none `update-ref --stdin` reservation transactions,
  derived dirt-disjointness on the publish path.
- **P-5** Determinism discipline in the generators: no clocks, sorted
  everything, `--check` idempotence gates, byte-stability argued in comments
  and pinned by tests; the WI-253/255/256 obstacle-routing work is clean,
  provably terminating, and regression-pinned against the real repo's render.
- **P-6** The spine practices what it preaches: zero mechanical findings at
  G3, OKF bundle byte-faithful to the CSVs, honest allowlist censuses
  (dupes/orphans record *why*), the WI-229 attested migration preserved ids
  and recorded the owner hard-stop, and every consumable prior-review finding
  verifiably became a done WI.
- **P-7** Prose accuracy at the flag level is essentially perfect — every
  script flag cited across PROCESS/OPTIONS/ADOPTING exists (verified
  exhaustively) — and EXAMPLE.md/ADOPTING.md are genuinely excellent adopter
  documents (the standards crosswalk and vacuous-pass warnings especially).
- **P-8** Accessibility of the generated dashboard is far above typical:
  status glyphs alongside fills, focusable blocks, labelled scroll regions,
  WCAG-contrast and palette-bijection *tests*.

---

## 4. Overall recommendations and next steps

1. **Before the next long unattended run**, land the fail-closed cluster:
   H-1 (critique parse-miss), H-2 (process-tree kill), H-4's `{model}`
   validation, M-18 (session timeout wiring), M-20 (policy malformation
   warnings), M-22 (verdict-path unlink), M-23/M-33 (BOM readers). These are
   mechanical, stdlib, and directly protect the walk-away guarantee.
2. **File H-3 (spine-class persistence) as its own reviewed WI** — it changes
   reservation metadata semantics and integration gating; it needs recovery
   tests, not a drive-by fix.
3. **Restore truth at the entry points** (H-6, H-7, M-38, M-39, M-40): these
   are one-sentence-scale edits with outsized trust impact; then consider a
   small link-and-id lint over shipped templates so the prose layer gets what
   the CSVs already have (the review's clearest systemic lesson: every model
   migration left one or two prose surfaces behind).
4. **Re-arm the forward-only guard scoped to the hand-authored region of
   status.md** (H-5) after deleting the accreted bullet — this is the owner's
   own top-priority discipline currently running on honor.
5. **Schedule the two decompositions** as WIs: extract `--status` from
   gen_trajectory.py (H-9; also shrinks the perceptual-gate blast radius),
   and split agent_dispatch.py's refs/integrator/publisher seams (the seams
   are already visible). Pair with a per-module LOC ratchet (M-26) so the
   next monolith can't grow silently.
6. **Render-surface fixes (M-8, M-9, M-11, M-12, M-13, L-6, L-7, L-10) should
   ride the already-queued render WIs** (WI-257/258 or a follow-on), each
   with the regenerated artifact + bundled fresh critique the WI-243 protocol
   requires — not a review commit.
7. **Close the test blind spots**: gen_release_checklist tests (M-17), the
   loop-scaffold helper consolidation (M-25), BOM/verdict-parse-miss/spine-
   recovery regression tests, and CI timeouts (M-27).
8. **Owner decisions to rule** (parked, correctly, in open-items): the
   license (H-10 / OI-4), the G3-SR definition split (M-5), the integrator
   verdict-gate semantics (M-29), draw-weight scope (M-31), blackout shipped
   default (L-32), IF-057 ratification (L-33), archive-anchored WI specs
   (L-34), and git author-identity standardization going forward.
9. **Keep doing what works**: the meta-test discipline, scar-tissue comments
   with WI provenance, allowlist censuses, and the review→WI→done loop are
   the reasons this repo's defect density is as low as it is. The kit's one
   systemic gap is that nothing lints its *prose and citations* the way
   trace.py lints its registries — build that, and the drift class that
   dominates this report's High tier disappears.
