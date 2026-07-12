# Deep repository review — 2026-07-12

Owner-directed full-repo review (scope: everything except `docs/log.md`,
`docs/archive/`, and the generated artifacts they describe). Reviewer: Claude
(Fable 5), one sitting, with the real harness run for every claim. Baseline at
review start: clean tree on `MultiRepoSupport`, `python -m pytest -q` →
**633 passed, 3 skipped in 338 s** (serial), `ruff check` + `ruff format
--check` clean, `check_dupes.py` run manually (not wired) → 110 findings.

Review depth, stated honestly: the five largest scripts (`agent_loop.py`,
`gen_trajectory.py`, `trace.py`, `check.py`, `check_trajectory.py`) and the
hooks/CI/test infrastructure were read line-by-line; `bootstrap.py`,
`check_docs.py`, `gen_arch_map.py`, `gen_okf.py` and the small scripts were
read at docstring/structure level plus targeted spot-checks; templates, README,
and the skills were read in full; `PROCESS.md`/`PROCESS_OPTIONS.md` were
sampled, not re-reviewed (they carry their own review history).

---

## 1. Unfixed items and why

_This file is committed twice: first as the review itself (where a **FIXED**
tag records the session's confident-fix plan), then finalized alongside the fix
commit once the harness is green. Everything below tagged **DEFERRED** stays
unfixed for the stated reason._

- **H1 / M1 / M5 — the monolithic `main()`s** (`agent_loop.py` ~1,015 lines,
  `trace.py` ~640, `bootstrap.py` ~390). Deferred: a correct decomposition is a
  multi-session refactor of the three most load-bearing scripts, with churn
  risk far above this session's mandate. The suite exercises them via
  subprocess, so a mechanical split has no test seam to lean on until the split
  itself creates one. Needs its own WI + plan.
- **M2 — `check_dupes.py` is not wired for the meta-repo.** Deferred: wiring
  `[step:dupes]` today means allowlisting ~40 file-pairs of *ruled* F5
  duplication (see M6), which converts a deliberate policy into permanent
  allowlist noise. The owner should first rule on M6 (the F5 census); the
  enforcement audit already records this enforcer as opt-in, so the gap is
  honest, just not closed.
- **M6 — the F5 duplication policy has no upper bound.** Deferred — owner
  ruling. `_utf8_console` now exists in ~22 copies; the policy that sanctions
  small-helper duplication (so each script stays independently copy-able) is
  sound, but nothing bounds it or records the census. Options: (a) accept and
  record the census in `docs/enforcement-audit.md`; (b) wire `[step:dupes]`
  with a `docs/dupes-allow` naming each ruled pair; (c) allow one shared
  `_kitcommon.py` for the strictly-identical helpers and amend F5.
- **M7 — code comments anchored to archived review docs.** Deferred — policy
  question. `THREAD_52_REVIEW.md F4`, `REVIEW_GRIND_FULL C6` etc. resolve
  inside this repo (`docs/archive/`), but every scaffold copies the scripts
  *without* the archive, so downstream readers inherit dangling pointers.
  Fixing means either stripping the anchors (loses provenance the meta-repo
  values) or expanding each into a self-contained why (bytes). Owner call.
- **L1 — `Links.rtf` at the repo root.** Deferred — owner content. An RTF is
  opaque to diff review and the root is supposed to stay live-only; suggest
  converting to a markdown reference memory/doc or archiving. Not touched
  because it is owner-authored material.
- **L3 — `parse_model_map` naming.** Deferred: the function now parses four
  different `KEY=value` maps (model/cmd/prompt/tier); renaming to `parse_map`
  is trivial but pure churn against a stable, tested surface. Fold into the H1
  refactor when it happens.
- **L4 — quadratic registry joins** in `trace.py` (`build_forest`, the
  SR→LLR/TC matrix loops) and `gen_trajectory.py`. Deferred: at the current
  scale (≤49 rows/tier) the cost is microseconds; a thousand-row adopter would
  want the `refs()` results precomputed into index dicts. Not worth touching
  until a real adopter hits it — recorded here so it is findable.

---

## 2. Executive summary

**This repository is in unusually good shape.** No critical findings. The
things most reviews flag — missing tests, drifting docs, secrets, silent
failure paths, platform assumptions — are not just absent, they are actively
mechanized against: 633 tests with ~91 % measured coverage *including
subprocess coverage*, freshness-gated generated artifacts, an honest
attested-vs-mechanized split, encoding guards on every console writer, and a
CI matrix that actually runs the 3.8 floor on two OSes. The repo eats its own
dog food and the dog food is real.

The critique, bluntly, is concentrated in four places:

1. **Function-scale discipline does not match file-scale discipline.** The kit
   preaches decomposition, yet its three flagship scripts have `main()`
   functions of ~1,015 / ~640 / ~390 lines. They work, they are tested — but
   only end-to-end; the cognitive load of the `agent_loop` session loop
   (managed routing + reviews + critique + stall/limit handling interleaved in
   one 500-line `for` body) is exactly what the working agreement tells
   downstream authors not to write.
2. **The dedup story has a blind spot the repo itself ships a detector for.**
   `check_dupes.py` run on `project-trajectory/scripts` yields 110 findings.
   Most are the *ruled* F5 small-helper duplication (fine, but unbounded and
   uncensused — 22 copies of `_utf8_console`); three were genuine intra-file
   copy-paste in `gen_trajectory.py` (~100 significant tokens × 3, the layered
   graph layouter) — fixed this session.
3. **Iteration speed still had low-hanging fruit.** The commit-bar guidance
   told every session to run the suite *serially* (`pytest -q`, 338 s) while
   `docs/stack.ini` already declares `-n auto` (~70 s) — a 4.7× loss on every
   commit, many times per unattended session. The gate's process steps and the
   pre-commit hook chain were strictly serial. Fixed this session (see §5).
4. **Small correctness debris:** a duplicate `id="dag"` in the generated
   dashboard (invalid HTML that works by accident), a dead `.gitattributes`
   pattern claiming protection it doesn't provide, and a template
   `.gitattributes` missing the `commit-msg` hook it ships. Fixed.

---

## 3. Findings by severity

### Critical

None. Stated plainly rather than padded: no data-loss path, no false-green
path, no injection or secrets exposure, no gate that silently skips was found.

### High

**H1 — `agent_loop.py:main()` is ~1,015 lines; the session loop body alone is
~500.** *(Code quality / SRP / testability — DEFERRED, needs its own WI.)*
`project-trajectory/scripts/agent_loop.py:1106-2116`. One function owns:
argument parsing, preflight, lane resolution, lock acquisition, the
interactive path, banner printing, and then a per-iteration body interleaving
managed routing, reviewer dispatch, verdict merging/escalation, the critique
loop, rate-limit backoff, stall/error accounting, and six exit paths, with
~15 pieces of loop-carried mutable state (`stall`, `errors`, `review_queue`,
`round_verdicts`, `rounds`, `last_impl_family`, `impl_range`, `swapped`,
`at_top_tier`, `impl_tier_override`, `impl_exclude`, `critique_*`…).

*Why it matters:* this is the script that runs unattended with a
permission-bypass flag — the one you most want reviewable at a glance. Every
new phase (S8 routing, WI-068 critique) was bolted into the same loop; the
next one raises the interleaving cost again. The tests are strong but almost
entirely subprocess-level, so no unit seam exists for the state machine.
*Suggested shape:* a `SessionOutcome` dataclass + extracting `route_session()`,
`handle_review_round()`, `handle_critique()`, `handle_rate_limit()` as pure-ish
functions over an explicit `LoopState` — behavior-preserving, test seams first.
`trace.py:main()` (M1) and `bootstrap.py:main()` (M5) are the same disease,
milder.

**H2 — The commit bar told sessions to run the suite serially.** *(Iteration
speed — FIXED.)* `project-trajectory/skills/session-protocol/SKILL.md` (+ its
`.claude`/`.agents` fan-out copies) and `CLAUDE.md` said `python -m pytest -q`;
`docs/stack.ini` already declares and WI-075 already verified `-n auto`
(338 s → ~70 s, zero flakes, coverage intact). Since the protocol requires the
bar before *every* commit, every session paid ~4.7× on every commit. Fixed by
updating the commit-bar text everywhere to `python -m pytest -q -n auto`.

**H3 — `gen_trajectory.py` triplicated the layered-layout block.** *(Real
duplication, intra-file, outside the F5 rule — FIXED.)* The rank → order →
barycentre-sweep → coordinate block appeared three times (`_dag_layout`
~458-501, `sw_graph` ~633-661, `know_graph` ~1691-1719; `check_dupes` measures
~97-109 identical significant tokens per pair). A bug fixed in one copy (e.g.
the `_dag_ranks` cycle guard) silently misses the others' call sites' layout
constants. Fixed by extracting one `_layered_layout()` helper (node order +
pred/succ maps + geometry constants in, positions/width/height out) used by
all three; output is byte-identical (`gen_trajectory.py --check` green without
regeneration).

**H4 — The gate's process steps and the pre-commit hook ran strictly
serially.** *(Iteration speed — FIXED; measurements in §5.)* `check.py`
executed its plan one subprocess at a time; the hook spawned ~10 sequential
interpreter chains per commit (`check.py --run-step X` × 6, `trace.py`,
`check_privacy.py` × 2, `check_trajectory.py`). All the process-layer steps
are read-only or write disjoint gitignored artifacts, so they are
parallel-safe. Fixed with a `--jobs N` mode on `check.py` (default 1 —
downstream behavior byte-identical), a `--run-steps a,b,…` batch mode that
runs named steps concurrently with buffered, non-interleaved output, and a
hook rewritten to one batched call — which also *improves* failure reporting:
the old `set -e` chain stopped at the first stale artifact; the batch reports
every stale artifact at once.

### Medium

**M1 — `trace.py:main()` ~640 lines.** *(DEFERRED — see H1.)* The join logic,
finding collection, report rendering (~250 lines of list-building), and exit
policy are one function. Rendering belongs in a `render_report(findings…)`
function; the finding passes are already mostly free functions — the fix is
mechanical but broad, and this file is the kit's most-copied artifact, so it
deserves its own reviewed WI rather than a drive-by.

**M2 — The kit ships a duplicate-code detector it does not run on itself.**
*(Consistency / dogfooding — DEFERRED, owner ruling; see §1.)* `docs/stack.ini`
has no `[step:dupes]`; running the detector manually yields 110 findings.
`docs/enforcement-audit.md:39` honestly records the enforcer as opt-in, but
the flagship dogfooding repo opting out of its own dedup gate is a visible
inconsistency with the "one fact, one home — in code too" agreement.

**M3 — Duplicate `id="dag"` in the generated dashboard.** *(Correctness /
standards — FIXED.)* `gen_trajectory.py` emitted both
`<section id="dag" class="panel">` and, inside it, `<div id="dag"
class="view">` — invalid HTML (duplicate IDs); `getElementById('dag')`
resolved to the section only by document-order accident, and the tab-switching
code iterates panels by id. Renamed the inner view to `id="dag-view"` (tests
that used the old string as a split anchor updated; dashboard regenerated).

**M4 — `.gitattributes` dead pattern; template missing a shipped hook.**
*(Config correctness — FIXED.)* The meta-repo's `.gitattributes` pinned
`hooks/pre-commit text eol=lf` — a slash-containing pattern is root-anchored,
and no root `hooks/` exists, so it matched *nothing* (the hooks actually live
at `.githooks/` and `project-trajectory/hooks/`; only the `* text=auto eol=lf`
catch-all saved them). The shipped `gitattributes.template` pinned
`.githooks/pre-commit` and `.githooks/pre-push` but not `.githooks/commit-msg`,
which bootstrap also scaffolds (`bootstrap.py` MAPPING lines 1137-1139). Both
corrected.

**M5 — `bootstrap.py:main()` ~390 lines.** *(DEFERRED — see H1.)* Milder: much
of it is honest sequential scaffolding, but the interactive-prompt flow, the
MAPPING walk, and the post-scaffold seeding would each stand alone.

**M6 — The F5 small-helper duplication policy is unbounded and uncensused.**
*(Design tension — DEFERRED, owner ruling; options in §1.)* The rule ("a small
stable helper is duplicated rather than imported, so each script ships
standalone") is repeatedly and correctly cited — but it now covers ~22 copies
of `_utf8_console`, 3-4 copies each of `_norm_module`/`_MODULE_EXTS`,
`refs`/`_split_refs`, the declared-policy reader, and the `_sn_rows` parser
pair whose comment admits the two copies *did* drift once (phantom SN-000
icicle root, REVIEW_GRIND_FULL C6). The policy's cost curve is bending up;
it deserves an explicit bound or census rather than accretion.

**M7 — Script comments cite archive-only documents.** *(Docs / portability —
DEFERRED, policy question; see §1.)* Scaffolds copy the scripts but not
`docs/archive/`, so `(THREAD_52_REVIEW.md F4)`-style anchors dangle for every
downstream reader. Note this borders the working agreement's own rule that a
comment should state the constraint, not its provenance.

### Low

**L1 — `Links.rtf` at the repo root.** Opaque binary-ish format on a root the
docs say stays live-only; not diff-reviewable, invisible to `check_docs`.
Owner content — surface only.

**L2 — `AGENTS.template.md` is at 9,978 of its 10,000-byte hard budget.**
22 bytes of headroom means the next durable working-agreement rule forces a
compensating cut. Not actionable now; worth knowing before the next edit
(WI-072 already dodged one edit for exactly this reason).

**L3 — `parse_model_map` parses four kinds of maps.** Naming debt; fold into
H1. *(DEFERRED.)*

**L4 — Quadratic joins in `trace.py`/`gen_trajectory.py`.** Fine at current
scale; recorded for the thousand-row adopter. *(DEFERRED.)*

**L5 — `check_docs.py --stale` is the slowest light step (~1.6 s).** One
`git log` over history builds the commit lookup — already the right design;
noted only so nobody "optimizes" it into many git calls.

### Positive practices worth naming (so they survive refactors)

- **Determinism by construction** everywhere a `--check` byte-compare exists
  (sorted inputs, no clocks, git-derived as-of stamp excluded via `ASOF_RE`,
  `newline="\n"` writes for cross-OS byte-stability).
- **Never a false green:** missing tool ⇒ FAIL not SKIP (outside `--lenient`);
  resolved-executable exec on Windows (PATHEXT); malformed profile fails loud;
  `--run-step` lenient only where a not-yet-set-up repo must still commit.
- **Vacuous-by-default optional layers** (absent/placeholder registries pass
  free; one-word opt-outs), consistently applied across trajectory / OKF /
  interfaces / components / critique.
- **Subprocess coverage wiring** (`tests/conftest.py` + `.coveragerc` [paths]
  fold-back) — the 91 % is real, not parent-process-only; and the pytest-cov 7
  `COV_CORE_DATAFILE` removal was caught and handled.
- **The Windows/POSIX lock split** in `agent_loop.py` (mandatory CRT lock byte
  at offset 2^40 so diagnostics stay readable; unsupported-filesystem errnos
  degrade open with a warning, everything else fails closed) is textbook.
- **Honest security posture:** hooks self-describe as supervision-not-security;
  the subagent gate fails open *with a paper trail*; redaction-by-construction
  reviewer/critic prompts; the attested-vs-mechanized trust split is always
  reported. No secrets, no injection paths found (`run_menu`'s `shell=True` is
  a documented same-user trust boundary; session prompts are argv-substituted,
  never shell-interpolated).
- **CI actually tests the claims:** 3.8 floor on Linux+Windows, macOS current,
  and a gate job running the repo's own `check.py` on real data.

---

## 4. Scope areas with no findings

- **Security & robustness:** beyond the positives above — input validation on
  every declared file (`errors="replace"` reads, loud failures on malformed
  profiles/ids), no `eval`/`pickle`/network use anywhere in the kit scripts.
- **Dependencies:** the kit is genuinely stdlib-only (a test enforces it);
  test tooling (ruff/pytest/pytest-cov/pytest-xdist) is current and minimal;
  CI actions are v4/v5 current majors.
- **Licensing:** the one vendored adaptation (`subagent_gate.py`) credits its
  MIT source. No license file exists at the repo root — flag only if the repo
  is ever published; add MIT/Apache-2.0 before publishing.
- **Git practice:** commit history is exemplary — one WI per commit,
  imperative subjects, bodies explaining why and deviations.
- **i18n/accessibility:** not applicable for the kit itself; the generated
  dashboard uses `role="img"` on its SVGs and honors `prefers-color-scheme` —
  above the bar for an internal artifact.

---

## 5. Iteration speed — measurements and changes

Measured this session (Windows, warm cache):

| Surface | Before | After / notes |
|---|---|---|
| Commit bar test run (`pytest -q` serial, as the protocol instructed) | 338 s | ~70 s with `-n auto` (already verified by WI-075) — **protocol text fixed** (H2) |
| Pre-commit hook (10 sequential interpreter chains) | ~3.3 s | one batched `check.py --run-steps …` call, steps in parallel (H4) |
| `check.py` gate run, non-test process steps | ~8-10 s serial (each step 0.1-1.6 s + spawn) | bounded by the slowest step with `--jobs 0` (H4) |
| Full `--gate G3` bar | dominated by tests+coverage (~157 s parallel) | light steps now overlap it under `--jobs` |

Changes shipped (details in the fix commit):

1. **`check.py --jobs N`** — runs the gate plan's steps concurrently
   (`0` = auto). Output is captured per step and printed whole on completion,
   so nothing interleaves; the summary and exit semantics are unchanged.
   Default stays `--jobs 1`: a downstream re-sync sees byte-identical behavior
   until it opts in. All plan steps were audited for parallel safety: the only
   writers are `trace.py` (gitignored `docs/test/report.{md,html}`) and the
   test step (coverage files) — disjoint targets; everything else is
   read-only `--check`/lint.
2. **`check.py --run-steps a,b,…`** — the batch form of `--run-step`: resolves
   each named step from the full plan, runs them in parallel (lenient, like
   `--run-step`), prints one result line per step, exits 1 if any FAIL.
3. **Hook rewrite** — `project-trajectory/hooks/pre-commit` now makes one
   batched call for the six independent freshness/integrity steps
   (`arch-map,okf,trajectory-map,trajectory,registry-integrity,skills-sync`)
   instead of six chains; privacy (staged-scoped), the `--staged` ratchet, and
   format keep their own calls (different arguments / conditionality). The old
   "ORDER MATTERS" first-failure comment is superseded: the batch reports
   *all* stale artifacts in one pass, which names the root cause better than
   stopping at the first.
4. **Session-protocol commit bar** updated to `-n auto` (H2) — the single
   biggest per-commit win (~270 s per commit under unattended operation).
5. **The regen sequence itself** ("regenerate arch-map / okf / dashboard and
   re-verify") stays sequential *between* regen tiers by data dependency
   (dashboard consumes the okf bundle and architecture.md), but arch-map ∥ okf
   can regen concurrently and all `--check` verifications now can run as one
   parallel batch: `check.py --run-steps arch-map,okf,trajectory-map`. The
   dual-interpreter dashboard determinism check remains a manual meta-repo
   practice; both interpreter runs can simply be launched concurrently.

---

## 6. Recommendations / next steps (priority order)

1. **Ratify the deferred rulings** (M2/M6/M7, L1): the F5 census-or-bound
   decision unblocks the dupes-gate decision; the archive-anchor policy is a
   one-paragraph ruling.
2. **Plan the `agent_loop.py` decomposition (H1)** as its own campaign:
   extract the session-loop state machine behind unit-testable seams before
   the next scheduling feature lands — each new phase raises the cost.
3. **Then `trace.py` (M1) and `bootstrap.py` (M5)** — same shape, less urgent.
4. **Adopt `--jobs 0` where the meta-repo runs its own gate** (CI gate job now
   does; sessions can) and watch for any output-ordering surprise downstream
   before recommending it in the shipped docs.
5. **Before any public release:** add a LICENSE, and revisit L2's byte budget
   before the next AGENTS.template.md edit.
