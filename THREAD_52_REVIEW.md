# Thread 52 — Adversarial Review Findings (to triage)

**Reviewer:** Claude (Opus 4.8), self-review · **Date:** 2026-07-08 ·
**Branch:** `MultiRepoSupport` (not pushed).

This is an adversarial review of everything Thread 52 (the trajectory / work-items
layer) landed, plus the SR-035 doc clarification. It is a **triage input**, not a
plan: it records what is wrong (or arguably wrong), the evidence, the concrete
failure, and — per the request — the **deeper, possibly-related changes** each
finding opens up, so a fresh session can drill in and decide how to handle them.
Nothing here has been fixed; every item is verified against the tree.

> How to read: F1 is the one that matters (a real hole the gate structurally
> cannot see). F2 is a one-line ergonomics bug. F3 is honest-but-loose data.
> F4–F5 are cheap hardening. F6–F8 are nits. Each finding ends with a
> **Deeper thread** — the larger question it exposes.

---

## Scope reviewed

- **Commit range:** `2e1351f..daee60c` on `MultiRepoSupport` (diff with
  `git log --oneline 2e1351f..daee60c` / `git diff 2e1351f..daee60c`).
- **The five commits:**
  - `07fd10f` — P1: `work-items.csv` registry + `check_trajectory.py` validator +
    the opt-out `trajectory` gate step.
  - `6fa3236` — P2: `gen_trajectory.py` → offline `docs/trajectory.html` (SVG
    icicle + plain-SVG layered DAG) + the `trajectory-map` freshness gate.
  - `49a5cf8` — P3: PROCESS_OPTIONS section + STATUS convention + README
    kit-contents (docs-only).
  - `fcd5ef5` — P4: the dogfood — the kit's own 37-WI `work-items.csv` +
    generated `docs/trajectory.html`.
  - `daee60c` — SR-035 macOS+3.8 rationale clarification (+ dashboard regen).
- **Key files:**
  [`project-trajectory/scripts/check_trajectory.py`](project-trajectory/scripts/check_trajectory.py),
  [`project-trajectory/scripts/gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py),
  [`project-trajectory/scripts/check.py`](project-trajectory/scripts/check.py) (the two new steps),
  [`project-trajectory/registries/work-items.template.csv`](project-trajectory/registries/work-items.template.csv),
  [`docs/requirements/work-items.csv`](docs/requirements/work-items.csv) (the dogfood data),
  [`docs/trajectory.html`](docs/trajectory.html) (generated),
  [`project-trajectory/PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) ("Trajectory / work-items layer"),
  [`tests/test_trajectory.py`](tests/test_trajectory.py),
  [`tests/test_gen_trajectory.py`](tests/test_gen_trajectory.py).

## Severity index

| ID | Sev | One-liner |
|---|---|---|
| **F1** | **HIGH** | The trajectory layer's own code is untraced in the self-adopted spine — and the gate can't see it. |
| **F2** | MEDIUM | `trajectory.html` staleness is caught only in CI, not at commit (hook gap). |
| **F3** | MEDIUM | The dogfood DAG encodes narrative/ordering, not true dependencies. |
| **F4** | LOW | Unbounded recursion in the layout/validation crashes on pathological input. |
| **F5** | LOW | `gen_trajectory`'s sibling import is a latent trap for the next test author. |
| **F6** | nit | PROCESS_OPTIONS "Referenced from §7" is aspirational (§7 doesn't name it). |
| **F7** | nit | STATUS template calls the layer "off"; it is opt-**out** (on-but-vacuous). |
| **F8** | nit | Registry is validated twice at G3 (`trajectory` + `trajectory-map`). |

---

## F1 — HIGH · The trajectory layer's own code is untraced in the self-adopted spine

> **RESOLVED 2026-07-09 (WI-1.43 / WI-038):** SR-037/038 + LLR-034/035 + TC-037/038
> landed, owner-scoped — SR-038 written at need level (single offline HTML,
> definition + execution completeness, the SN→SR→LLR→TC hierarchy, the roadmap DAG,
> mobile viewports — the mobile criterion mechanized by a new
> `test_mobile_responsive_shell`); the HOW-view / root `PROJECT_STATE.html`
> evolution is deliberately *not* claimed — roadmapped as WI-039.
> `check.py --gate G3` re-run → PASS; **owner re-attestation pending in
> `docs/log.md`**. The "deeper thread" below (a mechanical untraced-code check)
> stays open — Thread 49-adjacent, sequenced with the AXES schema bundle.

**What.** The meta-repo's premise (Thread 47) is *"the kit traced with its own
process, its product being `project-trajectory/scripts` + `tests/`."* Every other
product script has a full `SN→SR→LLR→TC` chain — `LLR-001..033` each map an
`SR → CodeSymbol → TC`. **`check_trajectory.py` and `gen_trajectory.py` are the
only product scripts with no SR, no LLR, and no TC.** Thread 52 added ~600 lines of
new product code (and its dogfood registry) but never extended the spine to cover
it.

**Evidence (reproduce):**
```
grep -niE "trajectory|work-item" docs/requirements/low-level-requirements.csv   # -> nothing
grep -niE "trajectory|work-item" docs/test/test-cases.csv                       # -> nothing
grep -niE "trajectory|work.item" docs/requirements/system-requirements.csv      # -> only the SR-035 edit
grep -cE "check_trajectory|gen_trajectory" docs/architecture.md                 # -> 3 (arch-map DOES list them)
```
`SN=22 SR=36 LLR=33 TC=36` — unchanged by Thread 52. The **arch-map** (structural
symbol map) includes the new scripts, which masks the gap visually; **arch-map is
not traceability.**

**Why the gate stays green.** `trace.py` enforces *"no orphans among declared
rows"* — every declared LLR/TC must link up — **not** *"every source symbol is
declared."* So untraced code creates no orphan and trips nothing. The ≥80%
coverage gate *does* cover the new scripts (they're tested at ~98%), so they are
**tested but not traced** — which hides the hole even more.

**Failure scenario.** The owner (or an auditor) treats the meta-repo as the proof
that the kit dogfoods its own traceability. They inspect and find the kit's
*newest* feature — the one whose whole job is to visualize the spine — is the only
part of the product not on the spine. The claim and the reality diverge, silently.

**Deeper thread (the real question).** F1 in the meta-repo is a symptom of a
**kit-wide capability gap**: *the kit has no mechanical check that product code is
traced at all* — only that declared rows are self-consistent. Any downstream
adopter can add untraced modules and sail through G3. Worth deciding:
- Should there be a new **"symbol-coverage" / "untraced-code" check** (every public
  symbol in `src`, or every module, must be cited by some LLR `CodeSymbol`)? This
  is a real new kit feature, warn-first probably, and it is **adjacent to Thread 49**
  (doc-currency hardening: symbol-reference validation) — consider folding them.
- Adding `SR-037`/`SR-038` (+ LLRs + TCs) to the meta-repo **touches the
  G3-ratified spine.** New `Verification=Test` SRs must be `Verified` (their TCs
  are the existing `test_trajectory.py` / `test_gen_trajectory.py`), and the owner
  may want to re-attest G3 rather than let an agent silently mutate a ratified
  spine. So the fix is not "add two rows" — it is a spine change with a
  ratification question attached.

**Suggested fix (local).** Add `SR-037` (WI-registry validation — `check_trajectory.py`)
and `SR-038` (offline trajectory dashboard — `gen_trajectory.py`), each with an
LLR pointing at the real symbol(s) and a TC pointing at the existing tests; mark
`Verified`; re-run `check.py --gate G3`; record the spine change + (owner)
re-attestation in `docs/log.md`. Then reconcile with the "Deeper thread" above.

---

## F2 — MEDIUM · Dashboard staleness is caught only in CI, not at commit

> **RESOLVED 2026-07-09 (WI-1.45 / WI-040):** the shipped `hooks/pre-commit` now
> runs `check.py --run-step trajectory-map` as step 1b, delegated exactly like
> arch-map — vacuous for a non-adopter (absent/placeholder registry passes,
> `docs/trajectory-check: off` silences), and measured at ~0.2 s per commit on
> the meta-repo's real 39-WI registry (the "acceptable latency?" question:
> yes). The deeper hook-vs-CI question is answered and **stated once, in the
> hook's step-1b comment**: a generated artifact's freshness check joins the
> floor when regeneration is one stdlib command and the step is vacuous for a
> repo that never adopted the layer; checks needing the product toolchain or
> gate context (tests, perf, flows) stay in check.py / CI. Cross-cutting
> question 2 below is thereby settled. The shipped [`hooks/pre-commit`](project-trajectory/hooks/pre-commit)
runs `check.py --run-step arch-map` (code-map freshness), `trace.py
--strict-integrity`, and the privacy scan — but **not** `trajectory-map`. The
`trajectory.html` freshness gate lives only in `check.py --gate G3` (CI).

**Evidence:** `grep -nE "run-step|arch-map|trajectory" project-trajectory/hooks/pre-commit`
shows `--run-step arch-map` on line 97 and no `trajectory` anywhere.

**Why it bites.** The icicle reads **all four spine registries** (`stakeholder-needs.md`,
`system-requirements.csv`, `low-level-requirements.csv`, `test-cases.csv`) **plus
the README `PROJECT-VISION:` tag**. So editing *any* requirement row or the README
vision staleness the 114 KB dashboard. A contributor fixing an SR typo commits
clean locally and only discovers the stale dashboard when CI goes red — a much
slower loop than the code map, which the hook catches before the commit exists.
**This actually happened in this session:** the SR-035 edit (`daee60c`) staled
`trajectory.html`; nothing local flagged it — it was regenerated only because the
reviewer remembered.

Note the coupling is **broader** than arch-map: arch-map tracks source only;
`trajectory-map` tracks four registries + README, so it goes stale far more often
during ordinary requirements work.

**Deeper thread.** This is a **shipped-hook change that affects every adopter.**
Questions to settle:
- Should `check.py --run-step trajectory-map` be added to `hooks/pre-commit`
  (mirroring the arch-map step)? It is vacuous/fast for non-adopters, but for an
  adopter it regenerates a large HTML in memory on **every** commit — acceptable
  latency? (Probably yes; measure.)
- Or keep freshness CI-only (like some choose for expensive checks) and instead
  make the local **failure message** actionable, and/or teach `dev-setup` /
  session-protocol to regen after registry edits.
- General principle to state once: **which generated-artifact freshness checks
  belong in the pre-commit hook vs CI-only, and why.** (arch-map is in the hook;
  perf/flows/trajectory are not — the rule is currently implicit.)

**Suggested fix (local).** Add a `trajectory-map` step to the shipped pre-commit
hook, guarded like arch-map (missing-tool → skip). One line + a comment.

---

## F3 — MEDIUM · The dogfood DAG encodes narrative, not true dependencies

**What.** Several predecessor edges in [`docs/requirements/work-items.csv`](docs/requirements/work-items.csv)
are "reads well left-to-right," not "blocks build." SR-refs on meta-work are
representative-not-exhaustive.

**Evidence (a concrete false edge):**
```
grep -E "^WI-013|^WI-014" docs/requirements/work-items.csv | cut -d',' -f1,2,5
# WI-013 check_docs.py ...           (pred WI-008)
# WI-014 check_flows.py ... pred ->  WI-013
```
`check_flows.py` does **not** depend on `check_docs.py` — they are independent
validators. Likewise `WI-028` (self-adoption spine) lists `SR-Refs=SR-001;SR-010`
though that work realized **all 36** SRs; the two ids are illustrative.

**Why it matters.** The generated dashboard presents these edges with the
authority of real data. A reader (or a future automated consumer) trusting the DAG
would infer dependencies that do not exist. It is flagged as a "first honest pass"
in the plan/status, but the artifact itself carries no such disclaimer.

**Deeper thread.**
- **Data pass:** prune edges to true build-blockers; make meta-work SR-refs honest
  (empty, or the actual set). The owner explicitly wanted to review the 37-WI
  mapping — this is where.
- **Schema question for the layer:** should `work-items.csv` distinguish a **hard
  predecessor** (blocks) from a **soft/ordering** hint? gilbert's original may
  have a convention; check `c:\Projects\gilbert`. If yes, it is a small schema +
  `check_trajectory` + `gen_trajectory` change (a new column or an edge-style),
  and it is **downstream-migrating** — decide before more adopters use the CSV.
- **Granularity question:** 37 WIs across 4 tracks is one defensible cut; the user
  may want finer (split the `WI-1.x` batch into its own lane) or coarser. Cheap
  CSV edit + regen either way.

---

## F4 — LOW · Unbounded recursion on pathological input

**What.** `gen_trajectory._dag_ranks.r` (rank), `arch_icicle.wt/collect/draw`, and
`check_trajectory.validate.visit` (cycle DFS) all recurse over the graph/tree with
no depth guard or iterative fallback.

**Evidence:** `grep -nE "def visit|def r\(|def draw|def wt|def collect|setrecursionlimit"`
over both scripts — the recursive defs are present, no `setrecursionlimit`.

**Failure scenario.** A registry with a dependency chain (or an `SN→…→TC` spine)
deeper than Python's ~1000-frame limit raises a raw `RecursionError` traceback
instead of a clean, kit-style message. Realistic registries are shallow (the kit's
is 10 ranks), so low — but the kit otherwise prides itself on failing *clearly*,
and this is an uncaught crash mode on adversarial input.

**Deeper thread.** The `arch_icicle` recursion is **ported ~verbatim from gilbert**,
so any hardening (iterative reformulation, or a friendly depth guard) touches the
ported code and should be considered for gilbert too. Low priority; bundle with
any future `gen_trajectory` refactor rather than as its own change.

---

## F5 — LOW · Sibling import is a latent trap for the next test author

> **RULED 2026-07-09 (owner): option (a) — keep the import.** The kit's de facto
> rule, scoped from its own precedents: *duplicate small, stable helpers*
> (bootstrap's inlined helper; WI-1.42's 3-line git-config wiring;
> `check_trajectory`'s own `_first_declared_line` copy) — *import a large,
> evolving core, guarded* (the ~200-line validation surface here, which WI-1.44's
> soft-edge change already evolved once; inlining would have made that a
> two-place edit with split-brain risk). Also consistent with the deferred
> shared-graph-engine extraction (AXES Q8), which depends on sibling imports.
> Scope: guarded import in `gen_trajectory`, a `conftest.load_script` shim, an
> in-process `load_script("gen_trajectory")` regression test (the trap becomes
> the test), the convention stated once as the guarded import's comment.
> Queued as part of the F4–F8 closure WI (status.md).

**What.** [`gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py) does
`import check_trajectory as ct` — the **first** kit script to import a sibling. It
resolves only because the script's own directory is `sys.path[0]` when run as a
script/subprocess.

**Failure scenario.** A future unit test that follows the established
`conftest.load_script("gen_trajectory")` pattern (used across the suite) would hit
`ImportError: No module named 'check_trajectory'`, because `load_script`
(`importlib.util.spec_from_file_location`) does **not** put `scripts/` on
`sys.path`. Today's tests use subprocess (`run_py`), so it is green; the trap is
for whoever writes the next in-process test.

**Deeper thread — a kit-architecture decision.** The kit's established convention
is **standalone scripts** — `bootstrap.py` deliberately *inlines* a shared helper
"so bootstrap stays a single stdlib file" rather than importing. `gen_trajectory`
broke that convention to keep the WI validation **single-sourced** in
`check_trajectory` (SSOT). Both principles are kit values and they collide here.
Decide the rule once:
- (a) **Keep the import** (SSOT wins for the ~80 lines of graph validation) + add a
  guarded `sys.path` insert at the top of `gen_trajectory` + a `load_script` shim,
  and document "sibling imports are allowed for scripts that always ship together";
  or
- (b) **Inline** the validation into `gen_trajectory` (standalone wins) and accept
  the duplication + a "keep in sync" note (the bootstrap precedent).
This is a genuine judgment call worth an owner ruling, because it sets precedent
for future multi-script features.

---

## F6 — nit · PROCESS_OPTIONS "Referenced from §7" is aspirational

> **RULED 2026-07-09 (owner): soften the phrasing** to the "Parallel tracks"
> style ("Builds on PROCESS.md §7 …") — PROCESS.md stays byte-flat. Queued with
> the F4–F8 closure WI.

The new PROCESS_OPTIONS section opens `*Referenced from PROCESS.md §7 (the harness
contract + the offline-render principle).*` — but §7 does **not** name the
trajectory layer (unlike "Skills layer," which §7's boundary-notes list *does*
name). It was left that way to keep `PROCESS.md` byte-flat. Either add a one-line
§7 boundary note (costs `PROCESS.md` bytes — check `byte-budget-guard`) or soften
the phrasing to the "Parallel tracks" style (*"Builds on PROCESS.md §7 …"*), which
does not claim §7 points back.

## F7 — nit · STATUS template wording: "off" vs opt-out

[`STATUS.template.md`](project-trajectory/STATUS.template.md)'s "Work items?"
bullet says *"off unless you adopted the trajectory layer."* The layer is
**opt-out** (on-by-default but vacuous), not "off" — every other description in the
kit is careful about that distinction. Reword to "*ignore unless you are tracking
work items*" or similar.

## F8 — nit · Registry validated twice at G3

> **RULED 2026-07-09 (owner): accepted as-is** — the duplication is cheap and
> the G2-validation / G3-freshness gate split stays as designed; do not collapse
> the steps. Closed by ruling, no code change.

At G3 both `trajectory` (runs `check_trajectory.py`) and `trajectory-map` (runs
`gen_trajectory.py --check`, which re-validates before rendering to protect the
layout from a cycle) validate the same registry. Cheap (a small CSV), but
duplicated. Acceptable as-is; noted for completeness. If ever a concern, the split
was chosen so validation gates from G2 while freshness gates from G3 — do not
collapse them without re-deciding those gate assignments.

---

## Cross-cutting "deeper" questions (span multiple findings)

1. **Should the kit mechanically enforce that product code is traced?** (F1, and it
   generalizes beyond the meta-repo.) Today nothing does. A symbol/module-coverage
   check would be a new, warn-first kit capability — evaluate alongside **Thread 49**
   (symbol-reference validation) and note it is downstream-migrating.
2. **Which freshness checks belong in the pre-commit hook vs CI-only?** (F2.) State
   the rule once; it drives whether `trajectory-map` (and `perf`, `flows`) join the
   shipped hook.
3. **What is the kit's rule for cross-script imports vs inlining?** (F5.) `gen_trajectory`
   set an unruled precedent; the SSOT-vs-standalone tension needs one decision.
4. **Does `work-items.csv` need hard-vs-soft edge semantics?** (F3.) A schema
   question that, if answered "yes," is a downstream-migrating change to the
   template + both scripts — decide before adoption spreads.
5. **Editing a G3-ratified spine.** (F1.) Adding SRs to the meta-repo's ratified
   spine raises a process question the owner should answer: does an agent-authored
   spine addition need human re-attestation, or is "add + Verified + record in
   log.md" sufficient under the current gate policy?

## Suggested triage / sequencing (for the new session to weigh)

- **Fix now, focused commit:** F1 (add SR-037/038 + LLRs + TCs; re-run G3; record) +
  F2 (one-line hook step) + F6/F7 (wording). These close the real self-adoption
  hole and the feedback-loop gap. F1 needs the owner's call on re-attestation first.
- **Data pass, separate commit:** F3 (prune false edges / honest SR-refs; optionally
  refine granularity), regenerating `docs/trajectory.html`.
- **Backlog / bundle later:** F4, F5, F8 — cheap hardening + one architecture
  ruling; no urgency.
- **New thread candidates:** cross-cutting #1 (traced-code check, with Thread 49)
  and #3 (import convention) are plan-level, not quick fixes.
