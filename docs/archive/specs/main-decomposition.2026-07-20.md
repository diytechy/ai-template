# Implementation plan — main-decomposition (WI-080 → WI-081)

> **ARCHIVED 2026-07-20 — WI-251 spec-lifecycle sweep.** Spec-of-record for **WI-080, WI-081** (all `done`; deliverables in `docs/requirements/work-items.csv`, session records in `docs/log.md`). Absorb-verified before archiving: every durable decision has a live spine/architecture/process home (dispositions in the log, 2026-07-20 entry).

**Status: DETAILED PLAN, pending the owner's go.** Prepared 2026-07-16 at the
owner's request; this supersedes the one-line shapes recorded at the 2026-07-12
ruling ([log.md](../../log.md) "Rulings", H1/M1/M5) and folds in the
2026-07-12b review findings that were parked on these WIs (L3 → WI-080,
M8 → WI-081; [repo-review-2026-07-12b.md](../history/repo-review-2026-07-12b.md)).
Starting a slice means flipping the WI's `Status` from `deferred` to `queued`
in [work-items.csv](../../work/).

**Branch:** `derived-gate-model` (the current working branch).

---

## 1. Tier ruling (why the routes below are what they are)

Per the session-protocol triage rule — `strong` only for design-shaping or
spine-touching work; `medium` by default — the effort splits:

- **WI-080 (`agent_loop.py`) — `BuildTier=strong`.** Genuinely design-shaping:
  the slice work *chooses the seam architecture* (which state becomes an
  object, which closure becomes a function, what the unit-test surface is) for
  the most intricate logic in the kit, in a file the v4 effort just reworked
  (5,283 lines today; `main()` grew from ~1,015 lines at review time to
  ~1,657). The refactor must thread between the legacy serial loop and the new
  worker/dispatcher paths (`--wi`/`--train`, managed routing, reviewer
  dispatch) without behavior drift the coarse end-to-end net could miss. This
  is the walk-away automation downstream repos are asked to trust — the
  highest-risk item in the backlog per status.md.
- **WI-081 (`trace.py`) — `BuildTier=medium`.** Does **not** need strong. The
  target shape is already fixed (this spec + the review: `analyze()` /
  `render_report()` / docstring shrink), making the build largely mechanical
  extraction under a byte-identical golden-output net. This matches the owner
  dial "strong plans, medium builds" (WI-121): the strong-tier design work is
  this spec. The most-copied-artifact caveat is honored by the golden net
  (§4), not by tier.

Net effect: strong-tier budget is spent where the design risk is (WI-080), not
on the wider-shipping but more mechanical half (WI-081).

## 2. Ground rules (both WIs)

- **Behavior-preserving.** No flag, output, exit-code, or file-format change.
  Every slice ends at the commit bar (smoke suite + `check_docs.py --stale`);
  each WI closes with the full unfiltered suite; the phase closes with
  `check.py --gate G3`.
- **Test-seams-first.** A slice that extracts a unit lands the unit tests for
  it in the same commit — the extraction *creates* the seams; the tests are
  the point, not an afterthought.
- **Stdlib-only, Python 3.8+** (plain classes, no dataclass field tricks that
  need 3.10, no third-party test helpers).
- **Serial execution.** Both WIs touch the same workstream and WI-081 is soft
  `~WI-080`. Run attended or at `--jobs 1`; the meta-repo's SafetyClass audit
  (the `--jobs 1` hold) is **not** part of this effort.
- **Existing end-to-end tests are the golden net** — they must pass unmodified
  unless a test names an internal symbol that moved (mechanical rename only,
  called out in the log).

## 3. WI-080 — decompose `agent_loop.py:main()` (~1,657 lines → orchestration)

Five slices, each a logical commit (`WI-080: <slice>`).

- **A — Golden net + state inventory (no production change).** Enumerate the
  mutable loop-state locals (~15: `stall`, `errors`, `cooldowns`,
  `review_queue`, `round_verdicts`, `rounds`, `last_impl_family`,
  `last_impl_tier`, `impl_range`, `swapped`, `at_top_tier`,
  `impl_tier_override`, `impl_exclude`, `critique_queue`, `critique_scope`,
  `critique_rounds`, …) and map each to the transitions that mutate it. Where
  the existing fake-agent subprocess tests leave a transition unpinned
  (win-stay/lose-shift, tier-up-never-down, cooldown decay, stall counting,
  critique entry/exit, each `WAITING/DONE/BLOCKED/NEEDS-HUMAN` outcome), add
  the missing end-to-end case. Deliverable: the inventory in the slice log
  entry + the strengthened net.
- **B — Session-construction seams.** Extract the nested closures
  `session_model` / `session_template` / `session_prompt`
  (agent_loop.py:4080–4258) into module-level pure functions taking explicit
  state. Fold-in **L3**: rename `parse_model_map` → `parse_map` (it parses
  model/cmd/prompt/tier maps alike). Unit tests pin prompt/template/model
  selection per phase+tier without a coordinator run.
- **C — `RoutingState` / `EscalationState`.** Move the slice-A state inventory
  into one (or two) plain classes with **pure transition methods** — inputs:
  the prior state + a session outcome; output: the next state + the routing
  decision. Covers the S8 managed-routing/reviewer-dispatch block (~4259) and
  the WI-068 critique-loop block (~4298). Unit tests pin single transitions
  directly — the review's core complaint ("no test can pin a single
  transition … without staging a whole coordinator run") is retired here.
- **D — Outcome classification + worker end-state.** Extract the outcome
  dispatch (`WAITING`/`DONE`/`BLOCKED`/`NEEDS-HUMAN`/stall-limit,
  ~5174–5250) and the worker-mode `worker_endstate`/`worker_exit` closures
  (~4320–4368) into module functions that **return actions** instead of
  mutating loop locals.
- **E — `run_one_session()` step.** Compose B–D into an iteration-step
  function; `main()` shrinks to argument parsing, mode selection
  (dispatch/worker/legacy), and the loop-over-steps — target ≤ ~150
  orchestration lines, honoring the kit's own "entry points orchestrate, they
  don't compute" rule. Close WI-080: full suite, log entry, registry row.

## 4. WI-081 — decompose `trace.py:main()` (~790 lines) + docstring

Four slices.

- **A — Golden-output net (no production change).** Snapshot-style tests
  capturing the full report text and exit code over the existing fixture
  scaffolds (clean, orphaned, draft-exempt, off-spine-registry cases),
  so B–D can assert byte-identical output.
- **B — `analyze(docs, flags) -> Findings`.** Extract the orphan analysis +
  integrity passes (spine + PB/REPO/PART/ASSET/CMP/IF, ~1307–1470) into a
  pure function returning a findings structure; `main()` keeps loading and
  flag wiring.
- **C — `render_report(findings) -> str` + exit policy.** Extract the ~240
  lines of report list-building, the console summary, and the exit-code
  policy. Fold-in **M8**: pre-index the `refs()` joins (id → rows maps built
  once) to kill the O(SR×LLR + SR×TC + LLR×TC) rescans — output must stay
  byte-identical under the slice-A net (ordering preserved).
- **D — Docstring shrink.** Cut the 239-line module docstring to contract +
  usage + a pointer to `process.md` §4 (decompose-don't-paraphrase applied to
  itself; target ≲ 60 lines). Check `docs/dupes-allow` (line ~116 references
  this effort) and `check_docs.py` for anything anchored to the old text.
  Close WI-081: full suite, log entry, registry row; then phase close —
  `check.py --gate G3` + `pytest -q -n auto` pasted in the log.

## 5. Done-when

- `agent_loop.py:main()` and `trace.py:main()` are orchestration-only; the
  routing/escalation state machine and the trace analyze/render split are
  unit-addressable with direct transition/golden tests.
- Zero behavior change: full suite green throughout; golden nets unmodified
  (mechanical renames excepted and logged).
- `check.py --gate G3` passes at phase close; `gen_trajectory.py` regenerated.
- Registry: WI-080/WI-081 `done` with deliverables; log entries per slice
  batch; status.md Next action no longer names this effort.

## 6. Risks / watch-fors

- **Hidden coupling between loop locals.** The ~15 locals mutate across
  branches; slice C must move them *together* (one state object), not
  piecemeal — a half-moved state is the drift vector. Slice A's inventory is
  the guard.
- **Worker vs legacy mode divergence.** The v4 worker paths short-circuit
  parts of the loop; extraction must keep both paths byte-identical (the
  fault-injection tests from Slice G of v4 are part of the net).
- **`trace.py` output ordering.** M8's pre-indexing must not reorder findings;
  the golden net asserts full-text equality, not set equality.
- **Scope creep.** `bootstrap.py` (WI-082) stays deferred indefinitely — do
  not fold it in.
