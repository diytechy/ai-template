# Deep repository review — 2026-07-12 (second pass, "b")

Scope: the full repository — kit scripts, templates, process docs, the meta-repo's
own spine, tests, hooks, CI, and configuration. Excluded per instruction:
`docs/log.md`, `docs/archive/**` (including the earlier same-day review), and
`OWNER_SCRATCHPAD.md` (owner-only by standing rule).

Evidence run for this review (real output, this machine, 2026-07-12):

- `python -m pytest -q -n auto` → **665 passed, 3 skipped in 109.37s** (skips are
  platform-conditional POSIX/exec-bit tests — legitimate).
- `python project-trajectory/scripts/check.py --jobs 0` (the repo's own derived-G3
  gate) → **RESULT: FAIL (1 step)**: 13 of 14 steps PASS (format, lint,
  derived-gate, traceability, privacy, doc-navigability, perf-budgets,
  design-flows, trajectory, arch-map, trajectory-map, okf, skills-sync);
  `tests+coverage` FAILED with a pytest-cov `INTERNALERROR` during the
  session-end coverage combine (`FileNotFoundError: .coverage.DESKTOP-OFFICE.
  82712.972655`) **after all 665 tests had passed**. See finding M9 — a flaky
  race in the parallel-coverage plumbing, not a product/test failure.
- Retry of the step alone (`check.py --run-step tests+coverage`) → **PASS**
  (665 passed, coverage 81.83% ≥ 80%), but with five xdist workers crashed and
  recovered at startup and 812 uncombined `.coverage.*` files left behind —
  full diagnosis in M9. Net: the gate is **green on substance, flaky on
  coverage plumbing** on this machine's (older, unpinned) toolchain.

Where a finding overlaps the backlog already ruled by the owner (WI-078…WI-082 in
`docs/requirements/work-items.csv` / `docs/status.md`), the WI id is cited — those
findings are *re-confirmed*, not newly discovered.

---

## 0. Unfixed items and why (filled after the first report write)

This was a **review-only pass: no fixes were applied to the tree.** Every finding
below is therefore "unfixed"; the ones with a decided disposition are:

| Item | State | Why it is unfixed |
|---|---|---|
| H1 `agent_loop.py:main()` decomposition | Deferred (WI-080) | Owner-ruled 2026-07-12: approved as its own behavior-preserving `main-decomposition` campaign, sequenced after the owner sitting. Highest value, highest risk — not a drive-by fix. |
| H2 `trace.py:main()` decomposition | Deferred (WI-081) | Owner-ruled follow-on to WI-080; the most-copied artifact, so churn ships widest — batched deliberately. |
| M-class cross-script duplication census | Deferred (WI-078) | Owner-ruled: keep independently-copyable scripts, gate *new* duplication via `check_dupes.py` allowlist; only the `stack.ini` step + populated allowlist remain. |
| Archive-provenance comments shipped downstream | Deferred (WI-079) | Owner-ruled: strip `(REVIEW_*/THREAD_*)` suffixes at scaffold time; lowest-value of the batch, accept-and-document is the fallback. |
| `bootstrap.py:main()` decomposition | Deferred indefinitely (WI-082) | Owner-ruled: honest sequential scaffolding, mildest of the three god-mains. |
| H3 missing LICENSE | **Filed as WI-097** — needs the owner | A legal call (which license, whether the repo/kit is meant to be public), not an agent's. Raised here as the one genuinely new High item. |
| M9 flaky coverage-combine race at the gate | **Filed as WI-105** (hard-edged behind WI-104's toolchain pinning) | Surfaced *by this review's own gate run* (the `tests+coverage` step INTERNALERROR'd after 665/665 tests passed). Not fixed in-pass because the right remedy (children's data dir vs combine tolerance vs erase-on-start) deserves a deliberate pick, and the review charter was look-don't-touch. Recommended as the first fix (§3.1b). |
| Everything else (Medium/Low below) | **Filed as WI-098…WI-106** (same day, owner-directed) | Awaiting the owner's triage/sequencing per the repo's change-intake discipline (process.md §5). |

**Update (2026-07-12, same day):** on the owner's direction, every High/Medium
finding now has a registry home — `Campaign=deep-review-2026-07-12b` in
[work-items.csv](../../work/), named in
[status.md](../../status.md):

- **H3 → WI-097** (LICENSE; owner ruling). **H4 → WI-098** (thin provenance in
  masters; `~WI-079` soft edge) — H4's strip-at-scaffold half stays on the
  already-ruled **WI-079**; H1/H2 stay on **WI-080/WI-081** (no duplicates).
- **M1 → WI-099** · **M2 → WI-100** · **M3 → WI-101** · **M4+L7 → WI-102** ·
  **M5 → WI-103** · **M6 → WI-104** · **M9+L1 → WI-105** (after WI-104) ·
  **M7+L2+L4 → WI-106**. **M8 and L3 fold into WI-081/WI-080** (recorded on
  their status.md bullets).
- **Not filed:** L5 (accept, or it needs a commit-msg check to be a backed
  rule), L6 (owner taste ruling on a deliberate template design), L8 (N/A).

**Second update (2026-07-12, owner-directed):** two follow-ups from the same
sitting:

- **WI-106's scope grew** to include **L9** (below): the agent-resume
  launchers' baked-in prompt still scopes sessions to the archived
  `IMPROVEMENT_PLAN.md` — retire those references to the live surfaces.
- **WI-107 filed** (owner-directed enablement, *not* a review finding):
  unattended operation wired for real — fill the launchers'
  `AGENT_MODEL_MAP`/`AGENT_CMD_MAP`, seed `docs/agents.csv` +
  `docs/agents-enabled` + `docs/run-phase` + `docs/guardrails-policy`, and move
  `docs/gate-policy` from `attended` to **`single-ratify`** (one human
  attestation per phase batch) with its deviation register, each in a reviewed
  commit. Spec: [specs/WI-107.md](../specs/WI-107.2026-07-20.md). `status.md`'s Next action
  now brings WI-107 in first, soft-edged after WI-106 (both edit the launcher
  twins).

---

## 1. Executive summary

**This is an unusually disciplined repository.** The kit preaches
single-source-of-truth, generated-never-hand-maintained artifacts, fail-loud
automation, and honest gates — and, rarely for a methodology repo, it actually
practices nearly all of it on itself: a 665-test end-to-end suite that bootstraps
real scaffolds and runs the real commands (measured ~91% product coverage with an
enforced 80% floor, including subprocess coverage — a detail most projects get
wrong), a 3-OS × 2-Python CI matrix plus a self-applied gate job, a derived (not
hand-set) gate marker, freshness-gated generated views, an enforcement audit that
names its own gaps, and WI-tagged commit discipline with spec-of-record links.
The security posture is sound: argv-based subprocess use throughout (the one
`shell=True` in `run_menu.py` executes only the user's own declared commands and
says so), HTML output is escaped everywhere, secrets/privacy scanning is honest
about being a lint and points to real tools, and the unattended-agent layer makes
its consent model explicit instead of hiding it.

**The most critical issues are concentration, not correctness.** The three
biggest scripts hide their logic inside enormous `main()` functions —
`agent_loop.py:main()` is ~1,015 lines carrying a dozen mutable loop-state
variables and an inline escalation state machine; `trace.py:main()` is ~690 lines
mixing loading, validation, rendering, and exit-code policy — which directly
contradicts the kit's own shipped rule ("entry points orchestrate, they don't
compute; small functions") and blocks unit testing of exactly the logic that most
deserves it. Second, the repo's distinctive comment style has tipped past its own
"comment the surprising" bar into narrating process history: shipped scripts cite
archived meta-repo documents (`REVIEW_GRIND_A A5`, `THREAD_52_REVIEW F5`,
IMPROVEMENT_PLAN threads, owner-ruling dates) that mean nothing in a downstream
copy and will rot. Third — the one high-severity item not already on the backlog —
**there is no LICENSE file** in a repository whose entire purpose is to be copied
into other repositories. Finally, the opt-in surface has grown large:
`PROCESS_OPTIONS.md` (125 KB) is now more than twice the size of the load-bearing
core it optionalizes, and the off-spine registry vocabulary (IF/PB/PART/ASSET/
CMP/REPO/WI) is a lot of concept for a newcomer, even inert.

Nothing found rises to "broken" in the product itself: all 665 tests pass, the
traceability spine reports zero orphans, and no security vulnerability of
consequence exists in the scripts. But this review's own gate run surfaced one
live infrastructure defect worth naming up front: the `tests+coverage` step
**failed nondeterministically** with a pytest-cov coverage-combine race, and on
retry passed while crashing five workers, losing ~9 points of measured
coverage (81.83% vs the documented ~90.8%), and leaving 812 uncombined
`.coverage.*` files behind (M9) — a flaky gate and a degraded metric at the
repo's own G3 bar, in a repo whose core promise is that the gate never lies.
The root enabler is the unpinned dev toolchain (M6): this box runs pytest-cov
4.1.0 where CI runs 7.x.

---

## 2. Prioritized findings

Severity reflects impact on the repo's own stated goals (maintainable,
trustworthy, copy-ready kit) — not runtime danger, since almost nothing here
faces untrusted input.

### CRITICAL

**None.** No correctness, security, or data-loss defect was found; the test and
gate evidence is green.

### HIGH

**H1. `agent_loop.py:main()` is a ~1,015-line god function.**
*(Known: WI-080, owner-ruled, deferred.)*
- **Location:** [agent_loop.py:1112](../../../project-trajectory/scripts/agent_loop.py#L1112)
  to end of file (2,126); the iteration loop body alone is ~500 lines, with
  nested closures (`session_model`, `session_template`, `session_prompt`) and
  ~15 mutable loop-state locals (`stall`, `errors`, `cooldowns`, `review_queue`,
  `round_verdicts`, `rounds`, `last_impl_family`, `last_impl_tier`, `impl_range`,
  `swapped`, `at_top_tier`, `impl_tier_override`, `impl_exclude`,
  `critique_queue`, `critique_scope`, `critique_rounds`, …).
- **Problem:** the scheduling/escalation state machine — the most intricate logic
  in the kit — is not addressable as a unit. The suite exercises it only through
  subprocess runs against a fake agent (good, but coarse); no test can pin a
  single transition of the win-stay/lose-shift policy without staging a whole
  coordinator run.
- **Why it matters:** this file ships to every downstream repo and is the
  walk-away automation people are asked to *trust*. It also flatly violates the
  kit's own AGENTS.template.md rules ("one responsibility per function", "entry
  points orchestrate, they don't compute") — the kit's credibility rests on
  dogfooding.
- **Suggestion:** the already-approved WI-080 shape is right: extract a
  `SessionOutcome` classifier, a `RoutingState`/`EscalationState` object with
  pure transition methods, and a `run_one_session()` step, behavior-preserving,
  test-seams-first. Treat the existing end-to-end tests as the golden net.

**H2. `trace.py:main()` is ~690 lines; the module docstring is 213 lines.**
*(Known: WI-081, deferred.)*
- **Location:** [trace.py:891](../../../project-trajectory/scripts/trace.py#L891)–1580;
  docstring [trace.py:2-213](../../../project-trajectory/scripts/trace.py#L2-L213).
- **Problem:** loading, orphan analysis, integrity checks, report assembly
  (~240 lines of list-building), console summary, and exit-code policy are one
  block. The docstring restates orphan/draft/schema semantics that are normatively
  stated in `process.md` §4 and the derived-gate spec — the kit's own
  "decompose-don't-paraphrase; state it once and link" rule applied to itself
  would cut it by more than half.
- **Why it matters:** `trace.py` is the single most-copied artifact in the kit;
  every downstream repo inherits its readability. Two parallel statements of the
  draft-exemption rules (docstring + PROCESS) *will* drift.
- **Suggestion:** extract `analyze(docs, flags) -> Findings` and
  `render_report(findings) -> str` (WI-081 already names `render_report`); shrink
  the docstring to contract + usage + a pointer to process.md §4.

**H3. No LICENSE file — in a repo built to be copied.** *(New.)*
- **Location:** repository root (absent). `git ls-files` shows no
  LICENSE/COPYING/NOTICE; the README never states terms. Meanwhile
  `registries/assets.template.csv` and PROCESS_OPTIONS demand license provenance
  for every downstream *asset* — the kit holds adopters to a bar it doesn't meet.
- **Why it matters:** without a license, default copyright applies: an adopter
  copying `project-trajectory/` into their repo (the documented quick-start!) has
  no legal right to do so, and anything scaffolded inherits the ambiguity. The
  sibling guardrails repo is already public on GitHub; if this kit ever is, the
  gap becomes immediately real.
- **Suggestion:** owner decision required. MIT/Apache-2.0 at root (Apache-2.0 if
  patent grant matters), plus one line in README, and have `bootstrap.py` note in
  the scaffold which license the copied scripts carry.

**H4. Shipped code narrates meta-repo history instead of stating constraints.**
*(Partially known: WI-079 covers stripping citations at scaffold; the style issue
is broader.)*
- **Location:** pervasive. Examples:
  [check.py:225](../../../project-trajectory/scripts/check.py#L225) ("kept a small
  duplicated helper per the F5 rule (REVIEW_GRIND_FULL C2)"),
  [agent_loop.py:1383](../../../project-trajectory/scripts/agent_loop.py#L1383)
  ("REVIEW_GRIND_A A5"), [conftest.py:30](../../../tests/conftest.py#L30)
  ("THREAD_52_REVIEW.md F5"), trace.py's "(IMPROVEMENT_PLAN.md Thread 50)",
  "owner-ruled 2026-07-09" in a schema check, `hooks/pre-commit`'s
  "(IMPROVEMENT_PLAN.md WI-1.42)" — plus module docstrings that double as design
  history (bootstrap.py's is ~300 lines).
- **Problem:** these are review-provenance notes, not constraints the next reader
  needs. The cited documents live in `docs/archive/` — which this repo itself
  classifies as "context, not a working surface" — and don't ship downstream at
  all, so a downstream reader gets dangling references. The kit's own guide says
  "comment the surprising, not the obvious" and "a comment is a promise — keep it
  true"; a comment pointing at an archived thread is a promise that rots by
  construction.
- **Why it matters:** cognitive load and trust. The information density is so
  high that the *load-bearing* invariants (e.g. "splitting first keeps a Windows
  interpreter path intact") drown among provenance trivia. It also inflates every
  file: `trace.py` is 1,584 lines of which well under half is executable logic.
- **Suggestion:** land WI-079 (strip at scaffold) as the floor. Better: adopt a
  one-line convention — keep the *rule*, drop the *citation* — in the masters
  themselves, and let `docs/log.md`/git blame carry provenance (that is exactly
  what the process says logs are for).

### MEDIUM

**M1. Hand-synchronized rule duplication between `trace.py` and `derive_gate.py`.**
- **Location:** `LLR_EXEMPT` at
  [derive_gate.py:78](../../../project-trajectory/scripts/derive_gate.py#L78) vs the
  inline tuple at [trace.py:1024](../../../project-trajectory/scripts/trace.py#L1024);
  `is_draft`, `sn_draft_ids`, `refs`, `load_csv` duplicated wholesale ("kept in
  sync with trace.py's orphan rule" — a comment, not a check).
- **Problem:** the *gate semantics themselves* (which Verification methods are
  LLR-exempt; what "draft" means) now live in two files whose agreement is
  promised in prose. The F5 copy-ability rule justifies duplicating *plumbing*;
  duplicating *policy* is a different, riskier thing — if one file adds a method
  to the exempt set and the other doesn't, the derived gate and the orphan report
  disagree about the same repo.
- **Why it matters:** disagreement here is a false green or false red at a gate —
  the exact failure class the kit exists to prevent.
- **Suggestion:** cheapest honest fix: a meta-repo test asserting
  `derive_gate.LLR_EXEMPT == the trace.py set` and `is_draft` equivalence (import
  both modules; the suite already does in-process imports). That keeps scripts
  copy-able while mechanizing the "kept in sync" promise. Fold into WI-078's
  census.

**M2. `check.py` resolves `docs/gate` and `docs/stack.ini` relative to CWD while
everything else takes `--root`.**
- **Location:** [check.py:133](../../../project-trajectory/scripts/check.py#L133)
  (`PROFILE_FILE = Path("docs/stack.ini")`),
  [check.py:606](../../../project-trajectory/scripts/check.py#L606) (`GATE_FILE`), and the
  literal `"docs/architecture.md"` in the arch-map step — vs `--root/--docs` on
  trace.py, derive_gate.py, check_docs.py, check_trajectory.py.
- **Problem:** run `check.py` from anywhere but the repo root and it silently
  sees *no profile and no gate file* — which means built-in commands and gate
  `all`. The failure mode is not an error but a *different, stricter-or-weaker
  plan*, which is the kind of silent divergence the kit hates. Hooks and CI
  happen to run at root, so it works today by convention only.
- **Suggestion:** either add the same `--root` flag (defaulting to `.`), or
  fail loudly when `docs/` is absent from CWD ("check.py must run at the repo
  root — no docs/ found here").

**M3. Status-vocabulary case handling is inconsistent.**
- **Location:** `is_draft()` lowercases
  ([trace.py:250](../../../project-trajectory/scripts/trace.py#L250),
  [derive_gate.py:110](../../../project-trajectory/scripts/derive_gate.py#L110)); the
  Verified checks compare exact-case (`r.get("Status") == "Verified"`,
  [trace.py:1163](../../../project-trajectory/scripts/trace.py#L1163),
  [derive_gate.py:141](../../../project-trajectory/scripts/derive_gate.py#L141)).
- **Problem:** `status=draft` and `Status=Draft` both count as draft, but
  `verified` (lowercase) silently counts as *not* verified. The failure direction
  is safe (a gate under-reports, never over-reports), but the asymmetry is
  undocumented and surprising in an open-vocabulary column: an adopter typing
  `verified` gets a G3 status finding whose cause ("capital V") nothing explains.
- **Suggestion:** pick one rule — either case-insensitive for the two magic
  values (`Draft`, `Verified`) or exact-case for both — state it once in
  process.md §4, and make the status finding name near-miss casing
  (`Status='verified' — did you mean 'Verified'?`).

**M4. `gen_trajectory.py` redefines the same `_esc` HTML-escape closure six times
in one file.**
- **Location:** [gen_trajectory.py:275, 525, 664, 772, 1017, 1707](../../../project-trajectory/scripts/gen_trajectory.py#L275)
  — each panel builder declares its own identical
  `def _esc(s): return html.escape(str(s), quote=True)`.
- **Problem:** the F5 rule justifies duplication *across* scripts, not *within*
  one module. This is plain copy-paste in a single 1,989-line file — the exact
  thing "one fact, one home — in code too" forbids.
- **Suggestion:** one module-level `_esc`. Two-minute fix; also a smell that the
  panel builders grew by accretion (`sw_containment` is ~240 lines) — a candidate
  for the same decomposition treatment as WI-080/081 when the file next churns.

**M5. `PROCESS_OPTIONS.md` (125 KB) has outgrown the core it optionalizes.**
- **Location:** [PROCESS_OPTIONS.md](../../../project-trajectory/PROCESS_OPTIONS.md)
  (125,618 B, 24 top-level layers) vs [PROCESS.md](../../../project-trajectory/PROCESS.md)
  (59,638 B, byte-budget-watched).
- **Problem:** the byte-budget discipline guards PROCESS.md and
  AGENTS.template.md, but the growth simply moved next door: the "opt-in" doc is
  now 2× the core, and an adopter deciding *whether* a layer applies must read a
  book. Some layers (Unattended operation, ~320 lines; Trajectory layer) are
  full specifications, not options-notes. The off-spine registry vocabulary
  (IF/PB/PART/ASSET/CMP/REPO/WI) compounds this — seven id namespaces before a
  newcomer writes their first SR, even if all are inert.
- **Why it matters:** the kit's proportionality doctrine ("cost nothing when
  unused") is honored in *runtime* cost but not in *reading* cost; the reading
  cost is what makes adopters bounce.
- **Suggestion:** give PROCESS_OPTIONS a byte budget and an *applies-when* index
  table at the top (one line per layer: trigger → cost → files touched) so the
  common path is "scan one table, read one section". Consider splitting the two
  spec-sized layers (Unattended, Trajectory) into their own reference docs, the
  MULTI_REPO.md pattern.

**M6. Dev-dependency versions are unpinned, and the suite has already been
broken once by a floating dep.**
- **Location:** CI installs `ruff pytest pytest-cov pytest-xdist` (latest) in
  [test.yml:39](../../../.github/workflows/test.yml#L39); no requirements/constraints
  file exists. [tests/conftest.py:42-46](../../../tests/conftest.py#L42-L46) documents the
  pytest-cov 7.0 breakage ("silently unwired every child … the coverage floor
  read a fraction of reality") that had to be worked around after the fact.
- **Problem:** the kit *runtime* being dependency-free is a genuine strength, but
  the meta-repo's own verification chain floats on unpinned tools; the next
  ruff format-rule change turns the `format` gate red (or a coverage-tool change
  silently weakens the floor again) unrelated to any commit. **Observed
  consequence during this review:** the local box runs pytest-cov 4.1.0 /
  pytest 7.4.3 while CI installs pytest-cov 7.x / pytest 8.x — two materially
  different coverage machineries answering to the same declared command, and
  the old-local combo is where the M9 races and the 81.83%-vs-90.8% coverage
  loss live.
- **Suggestion:** a small `requirements-dev.txt` with `~=` pins (or at least
  major-version caps) used by CI and dev-setup; a scheduled CI job can float
  latest to catch upcoming breakage without gating merges on it.

**M7. Stale hand-maintained counts in the shipped pre-commit hook.**
- **Location:** [hooks/pre-commit:84-86](../../../project-trajectory/hooks/pre-commit#L84)
  says "ONE interpreter spawn running **six** independent checks … where this
  hook once chained six separate calls"; the command on
  [line 134](../../../project-trajectory/hooks/pre-commit#L134) runs **seven** steps
  (arch-map, okf, trajectory-map, trajectory, registry-integrity, derived-gate,
  skills-sync).
- **Why it matters:** trivial in isolation, but it is precisely the
  hand-maintained-number drift the kit's whole generated-artifact discipline
  exists to prevent — in the kit's own most-copied hook.
- **Suggestion:** drop the number ("running the independent floor checks
  concurrently"); numbers in prose age, adjectives don't.

**M8. Quadratic joins in `trace.py`'s report rendering.**
- **Location:** the SR→LLR/TC matrix loop
  ([trace.py:1352-1356](../../../project-trajectory/scripts/trace.py#L1352)) and
  `build_forest`'s `sr_node`/`llr_node`
  ([trace.py:679-730](../../../project-trajectory/scripts/trace.py#L679)) rescan every
  LLR/TC row per SR, re-splitting `refs()` (a regex) on the same cells each
  time — O(SR×LLR + SR×TC + LLR×TC) with per-visit regex parsing.
- **Why it matters:** invisible at this repo's scale (≈50 rows each) and merely
  warm at hundreds; at the "scales to any project size" claim the outline view
  makes, a few thousand rows per tier turns the pre-commit-adjacent trace run
  into tens of millions of regex splits.
- **Suggestion:** build parent→children index dicts once (the code already does
  exactly this in `_per_phase` in derive_gate.py — copy the idiom). Fold into
  WI-081.

**M9. The `tests+coverage` gate step fails nondeterministically: a
coverage-combine race under `-n auto` + subprocess coverage.** *(New — observed
live during this review.)*
- **Location:** the measured parallel path: `docs/stack.ini` `[product] test =
  {py} -m pytest -q -n auto` + `[coverage] args = --cov=…`, with
  [tests/conftest.py `augment_env`](../../../tests/conftest.py#L62) sharing pytest-cov's
  datafile with every spawned child and [.coveragerc](../../../.coveragerc)
  `parallel = true`.
- **Observed (run 1 — the full gate, `check.py --jobs 0`):** **all 665 tests
  passed**, then pytest-cov's `engine.finish() → cov.stop() →
  combine_parallel_data()` raised `FileNotFoundError:
  .coverage.DESKTOP-OFFICE.82712.972655` — INTERNALERROR, step exit 3, **gate
  RESULT: FAIL**. The aborted combine left its workers' data files behind: root
  `.coverage.*` debris grew from ~40 (pre-existing) to 77 files.
- **Observed (run 2 — the step alone, `check.py --run-step tests+coverage`):**
  the step **PASSED** (exit 0, 665 passed, coverage 81.83% ≥ 80%), but on the
  way: **five xdist workers crashed at startup** (`[gw1/gw3/gw9/gw10/gw13] node
  down`) inside `pytest_cov.engine.DistMaster.start() → cov.erase()` with
  Windows `PermissionError [WinError 32]` deleting `.coverage.*` files "being
  used by another process" — i.e. **worker processes misidentifying as the
  coverage master during initial conftest load and concurrently erasing the
  shared data-file glob**. xdist replaced the nodes and recovered. After this
  *passing* run, **812** `.coverage.*` files remained at root — hundreds of
  subprocess children's data files never combined.
- **The coverage number itself is degraded on this toolchain:** run 2 measured
  **81.83%** against the documented ~**90.8%** (`docs/stack.ini` [coverage]
  comment) — the uncombined children *are* the missing ~9 points. The enforced
  80% floor held by 1.83 points of plumbing luck; one slightly worse race and
  the gate turns red on coverage while the true product coverage is unchanged.
- **Toolchain on this box vs CI:** Python 3.8.10, pytest 7.4.3, **pytest-cov
  4.1.0**, xdist 3.6.1, coverage 7.3.2 — while CI installs *latest* (pytest-cov
  7.x; [tests/conftest.py](../../../tests/conftest.py#L42) explicitly handles the
  pytest-cov 7 contract). So the local box and CI run materially different
  coverage plumbing; the race classes above belong to the old-local combo, and
  CI (2-core runners → few workers) under-observes them anyway. This is the
  concrete cost of M6 (unpinned dev deps): the same command means different
  machinery per machine.
- **Why it matters:** a nondeterministic red at the gate — and a coverage
  metric that swings ~9 points by plumbing loss — is corrosive in exactly the
  way this repo's philosophy warns about: it trains contributors to re-run
  until green, one habit away from ignoring a *true* red.
- **Suggestion:** (1) pin the dev toolchain (see M6) so every machine runs the
  pytest-cov ≥ 7 path the conftest already supports; (2) point subprocess
  children at a dedicated coverage data *directory* distinct from the xdist
  workers' base so worker erase/combine and child writes never share a glob;
  (3) add a stale-`.coverage.*` sweep to dev-setup / a pre-test step so an
  aborted run can't contaminate the next measurement; (4) once stable, alert
  when measured coverage deviates far from the recorded ~90.8% — a silent drop
  to 82% is itself a signal the wiring broke.

### LOW

**L1. `.coverage.*` debris accumulates at the repo root** (77 files at review
end — see M9, which supersedes this as the root cause; kept here for the
housekeeping angle). Gitignored, so harmless to git, but interrupted runs never
get `coverage erase`'d and the leftovers join later combines.

**L2. `PREDICATE_MARKERS` substring matching is looser than it looks.**
[trace.py:389-414](../../../project-trajectory/scripts/trace.py#L389): `"per "` matches
"proper ", "wrapper ", "developer "; `"within "` similar — so a comparative AC
containing any such word is silently considered "pinned" (advisory false
negative). Warn-only by design, so impact is only lint quality; word-boundary
regexes would tighten it if the advisory ever earns promotion.

**L3. `parse_model_map` parses four different map kinds** (model/cmd/prompt/tier)
under a model-specific name ([agent_loop.py:559](../../../project-trajectory/scripts/agent_loop.py#L559));
already noted in the prior pass — rename to `parse_map` when WI-080 lands.

**L4. Duplicated-malformed ids report "malformed" twice, never "duplicated".**
[trace.py:449-463](../../../project-trajectory/scripts/trace.py#L449): a malformed id is
added to `seen`, so its second occurrence re-reports malformed rather than
duplicated. Cosmetic — both are integrity failures either way.

**L5. Commit-subject lengths run long** (up to 134 chars in the last 200
commits). The bodies and WI-tagging are exemplary; subjects >72 chars just
truncate in tooling. Convention note, not a defect.

**L6. Template CSVs embed multi-kilobyte manuals inside `-000` placeholder
cells** (the WI-000 `Deliverable` cell is ~1.4 KB of prose;
[work-items.template.csv](../../../project-trajectory/registries/work-items.template.csv)).
Clever — the doc is exactly where the confused editor is looking — but a CSV cell
is a hostile reading surface (spreadsheet views, diff wrapping), and the same
rules are stated in PROCESS_OPTIONS, which is the kind of restatement the kit
polices elsewhere. Consider one-line cells pointing at the section id.

**L7. Accessibility of generated HTML views is minimal.** The dashboard
(`PROJECT_STATE.html`) is SVG-heavy with no ARIA labels/titles on nodes;
`report.html` is `<details>`-based (keyboard-fine) but unlabeled. Low relevance
for a dev-facing artifact; worth a `<title>` per SVG node (also gives hover
tooltips — a UX win, not just a11y).

**L8. i18n/localization: N/A by design** (developer tooling, English prose).
No blocker; noted for completeness.

**L9. The agent-resume launchers' baked-in prompt scopes sessions to an
archived surface.** *(Post-filing addendum, found while answering the owner's
model-config question; owner-directed into WI-106.)*
- **Location:** the `AGENT_PROMPT` slot in [agent-resume.cmd](../../../agent-resume.cmd)
  and [agent-resume.sh](../../../agent-resume.sh): "Work only scope recorded in
  IMPROVEMENT_PLAN.md — a thread or a WI-1.x entry … update … the plan's WI
  log."
- **Problem:** `IMPROVEMENT_PLAN.md` was archived (`docs/archive/` — "context,
  not a working surface"); the live scope surfaces are `work-items.csv` +
  `status.md` + `log.md`. An unattended session booted today is pointed at
  frozen history for its scope control — the exact drift class H4 describes,
  in the file that *launches* the walk-away runs.
- **Suggestion:** rewrite the two prompt strings (the launchers are declared
  twins — keep them in sync) to scope work to `docs/requirements/work-items.csv`
  per the session-protocol skill, and log to `docs/log.md`. Two-string edit;
  folded into WI-106.

### POSITIVE / GOOD PRACTICES (keep these)

1. **The test suite is the real thing.** End-to-end against freshly bootstrapped
   scaffolds, subprocess coverage correctly wired (including the pytest-cov 7
   migration), xdist-parallel, platform-conditional skips instead of silent
   passes, and a positive-control test for the stdlib-only rule. 665 tests,
   ~91% measured product coverage against an enforced 80% floor.
2. **CI is honest and layered:** 3-OS × {3.8, latest} matrix for portability,
   plus a separate job that runs the repo's *own* gate (`check.py --jobs 0`) — CI
   enforces the same bar a contributor runs locally.
3. **Fail-loud engineering throughout:** missing tool ≠ pass
   (`SKIP(missing)` fails outside `--lenient`); malformed `stack.ini` kills the
   run with the reason; step-name shadowing is rejected; `--check` freshness
   gates byte-compare every generated artifact (arch-map, OKF, dashboard, gate
   marker, skills fan-out).
4. **The derived gate model** (`derive_gate.py`) is the SSOT idea applied to the
   process's own state, and the script itself is the best-factored code in the
   repo — small pure functions, clean aggregation, testable. Use it as the house
   style for the WI-080/081 refactors.
5. **Cross-platform care beyond the norm:** PATHEXT-aware executable resolution
   with the resolved path exec'd (the WinError 2 class), cp1252 console
   reconfigure, case-sensitive-FS awareness (`scripts/` vs `Scripts/`), venv
   probing that *runs* the candidate python (the Windows Store alias trap),
   POSIX-sh-only hooks that work under Git for Windows.
6. **Security/consent posture:** argv-only subprocess calls (the single
   documented `shell=True` runs the user's own declared `[run]` commands);
   `html.escape` at every HTML sink; an always-on secrets floor that is honest
   about being a lint and names gitleaks/trufflehog rather than pretending;
   the unattended layer's permission-bypass consent stated in the banner every
   run; push-policy defaulting to human.
7. **The enforcement audit** (`docs/enforcement-audit.md`) — mapping each rule to
   its strongest enforcer and *recording the gaps* (the unenforced `Implements:`
   convention, the honestly-Prose judgment rules) — is a practice most teams
   should steal.
8. **Working-surface discipline:** forward-only status.md, backward-only WI
   deliverables, machine-checked coherence (R-A…R-E), WI-tagged commits with
   spec links, campaign batching for owner attestation. The repo's own history is
   navigable in a way very few are.
9. **Copy-ready templates:** inert `-000` rows that parse but never gate, so a
   fresh scaffold is green by construction and `--no-placeholders` flips the bar
   at G2. Elegant.

---

## 3. Overall recommendations & suggested next steps

The repo does not need a course correction; it needs to spend its own discipline
on itself in three places. In priority order:

1. **Resolve the license gap (H3) — one owner decision, minutes of work.** It is
   the only finding that makes the kit's core promise ("copy this into your
   repo") legally unsound. Do it before any further public exposure.

1b. **Fix the flaky coverage-combine race (M9) next session.** It is the only
   finding that makes the repo's own gate lie (a nondeterministic red), it was
   reproduced live during this review, and it self-amplifies via debris. Small
   blast radius: `.coveragerc` / `tests/conftest.augment_env` / dev-setup only —
   no kit-shipped file changes.
2. **Execute the already-approved `main-decomposition` campaign (WI-080 →
   WI-081), and use `derive_gate.py` as the target idiom.** Sequence:
   test-seams-first, behavior-preserving, one script per WI, with the existing
   end-to-end suite as the golden net. Fold M8 (index-dict joins), L3 (the
   `parse_map` rename), and M4 (the six `_esc` clones) into the same passes —
   they are free riders on files already churning.
3. **Mechanize the two "kept in sync by comment" promises (M1).** One small
   meta-repo test pinning `derive_gate` ↔ `trace` rule-set equality closes the
   only path found to a silent gate/trace disagreement. Cheap, high leverage.
4. **Land WI-078 (dupes gate + census) and WI-079 (strip provenance at
   scaffold)** as ruled — then go one step further than WI-079: thin the
   provenance narration in the *masters* (H4). The history belongs to log.md and
   git blame; the code should carry constraints only.
5. **Put PROCESS_OPTIONS.md on the same byte-budget regime as PROCESS.md (M5)**,
   add the applies-when index table, and consider promoting the two spec-sized
   layers to standalone reference docs. The adopter's first hour is the kit's
   real gate.
6. **Small hygiene batch (can ride any session):** M2 (`--root` or loud failure
   in check.py), M3 (status-casing rule stated once + near-miss hint), M7 (drop
   the "six" count), M6 (`requirements-dev.txt` with pins + a floating canary CI
   job), L1 (coverage debris).

**What to explicitly not do:** don't introduce a shared helper module across the
kit scripts (the owner's ruling to keep scripts independently copy-able is
correct — the drop-in property is worth more than DRY plumbing), and don't try to
mechanize the judgment-layer rules the enforcement audit honestly classifies as
Prose. The kit's restraint there is a feature.

---

*Review executed by Claude (Fable 5), 2026-07-12, on branch `derived-gate-model`
at `95a3b0d`. Excluded surfaces per instruction: `docs/log.md`,
`docs/archive/**`, `OWNER_SCRATCHPAD.md`.*
