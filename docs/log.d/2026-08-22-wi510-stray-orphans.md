## 2026-08-22 — WI-510 closes: the two stray orphan SRs are decomposed

Deferred open items: none — a scoped decomposition executing the orphan-vs-
frontier mapping's own assignment for the two strays no queued row owned.

**Summary.** `SR-160` (front-door launchers) and `SR-164` (declared SN
scope) each mint one LLR/TC pair, both `Drafted` per the row's own Context.
Investigation found the two obligations in very different states of
delivery, and both mints record that difference on the row rather than
paper over it.

### Deliverables

- **`LLR-193`** — *Root launcher interpreter selection: the loop-resume
  half's probe-then-floor, the front door's own robustness.* Module
  `agent-resume.sh`, symbol `pick_py` (mirrored by `agent-resume.cmd`'s
  `:pickpy`, inherited by `agent-resume.command`'s delegation), component
  `CMP-009`, `Drafted`. Realizes the built half of `SR-160`: the two-stage
  probe (runnable, then `sys.version_info >= 3.11`) across both `.venv`
  layouts then PATH `python3`/`python`, refusing by naming every rejected
  candidate rather than crashing cryptically inside the engine. **NOT
  DISCHARGED, stated on the row:** SN-034 names TWO universal contributor
  actions and only the loop-resume one has a root launcher — the
  environment-preparation half's scripts (`onboard.sh`, `dev-setup.sh`)
  materialize under `scripts/`, not the repository root SR-160's acceptance
  names (README.md's own "Still owed" ledger already says so). No LLR
  citation was minted for that half: there is no module to point at.
- **`TC-188`** — Integration / Full, `Drafted`, verifying `SR-160` +
  `LLR-193`. Evidence is 11 EXISTING `[live]`-parametrized node ids in
  `tests/test_launcher_interpreter.py` (venv preference, refusal naming
  rejected candidates, PATH-python success, stale-venv fallback, the same
  four for `agent-resume.cmd`, plus the `.command` inheritance pair) — the
  module WI-475 built specifically to run a launcher rather than grep its
  text.
- **`LLR-194`** — *The scope obligation's seam: the schema tier's
  required-field and closed-vocabulary check, not yet extended to SN.*
  Module `project-trajectory/scripts/trace.py`, symbols
  `schema_findings`/`REQUIRED_FIELDS`/`ENUM_FIELDS`, component `CMP-006`,
  `Drafted`. Investigation found `SR-164` entirely unbuilt: no field,
  checker branch or test anywhere in the shipped scripts reads a
  stakeholder-need `scope` value (the `**Scope: ...**` prose prefix is
  pure convention), and `SN` has no entry in `trace.py`'s schema tables at
  all. The row cites the real, already-delivered GENERIC mechanism SN-039's
  own acceptance text names as scope's future home ("the field enters the
  registry schema in the scheduled schema batch") rather than a fabricated
  scope-specific checker, and states plainly that SN's own entry does not
  exist yet.
- **`TC-189`** — Unit / Smoke, `Drafted`, verifying `SR-164` + `LLR-194`.
  Evidence is 2 EXISTING node ids
  (`tests/test_trace.py::test_missing_required_if_field_is_a_warn`,
  `::test_out_of_vocabulary_aspect_is_a_schema_finding`) exercising the
  same generic mechanism's two behaviours — missing-field warn, and
  out-of-vocabulary schema finding naming the row/value/allowed-set — over
  the one table (`IF`) that carries them today, honestly framed as
  verifying the seam rather than scope itself.
- Watermarks `LLR` 192 -> 194, `TC` 187 -> 189, via `trace.py --bump-ids`.
  Surfaces regenerated: report, open-items, `docs/stage` (unmoved —
  `drafted` 2 -> 6, rung stays `DevStg-LLReqs`, drafts excluded from the
  effective stage), `PROJECT_STATE.html`, `docs/status.md`'s generated
  block (WI-510 drops out of the ready frontier automatically).
- `docs/status.md`'s hand-authored orphan-debt sentence corrected: "five
  undecomposed SRs" -> "three" (the two strays no longer count), and "the
  two strays have their own decomposition row" replaced with "the two
  strays are decomposed" — forward-only, no closed WI id named (the R-D
  guard).

### The SR-160 testable-vs-inspection decision

Not reclassified. The Context offered re-classing `Verification` to
Analysis/Inspection only if the obligation were genuinely inspection-only;
investigation found real, already-passing tests driving the loop-resume
launcher (WI-475's `test_launcher_interpreter.py`), so the default
expectation — decompose into LLR/TC — applies. The row is DECOMPOSED, not
FULLY DISCHARGED: the environment-preparation half of SN-034 has no built
launcher to cite, and that gap is recorded on `LLR-193` as a stated
residual rather than silenced by a reclass or a fabricated citation.

### Orphan count

<!-- fig: cmd="python project-trajectory/scripts/trace.py" rev=25428fee -->

Before: **orphans=11** (`SR-160`, `SR-163`, `SR-164`, `SR-177`, `SR-181`
each missing LLR+TC, plus `LLR-164` missing TC — 5 SRs x2 + 1 = 11
findings). After: **orphans=7** (`SR-163`, `SR-177`, `SR-181` + `LLR-164`
remain — 3 SRs x2 + 1 = 7; owned by other queued rows per the orphan-vs-
frontier mapping, out of this row's scope). `integrity=0` throughout.

### Gates

- Smoke: `python -m pytest -q -n auto -m smoke` — 1397 passed, 5 skipped,
  70.92 s. Over the 60 s budget on this run; no test in the tier was added
  or slowed by this registry-only change (no code touched), so this reads
  as the box's own measured variance the budget's header already documents
  (54.9/64.0/55.7 s across three prior warm runs) rather than a regression
  to chase here.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=25428fee -->
- `python project-trajectory/scripts/check_docs.py --root . --stale` — 0
  broken references (pre-existing staleness hints unrelated to this row).
- `python project-trajectory/scripts/check_trajectory.py --strict` — clean
  (507 work items, pre-existing warnings unrelated to this row).
- `python project-trajectory/scripts/trace.py --strict` — integrity 0,
  orphans 7 (down from 11), drafts 6, interface-findings 0. Exits 1 under
  `--strict` on the three remaining orphan rows this row does not own —
  unchanged failure class from before this commit.
- Registry-only work (spine TOML + status.md + WI spec move): no full
  unfiltered suite owed per session-protocol.
