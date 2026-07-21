# 109-REVIEW-A — WI-251/252/253/254 (spec-lifecycle close side + R-F + cadence exclusion + coverage sweep)

Independent adversarial review (REVIEW-A) of `bb361fa..e6184cb` on
`dualplan-routing-fix` (11 commits). Reviewer did not write the code and read
no builder self-assessment; judged the artifacts and drove the shipped paths.
Rubric: `docs/rubrics/code-review-adversarial.md`.

## Scope / subject frame (R1)

- **WI-251** — the spec-of-record *close* half R-E never enforced. Parts: (a) the
  `WI-000.template.md` delete-banner contradiction fixed + specs/rubrics scaffold
  boilerplate dogfooded + `.githooks/commit-msg` wrapper; (b) rule **R-F**
  (`spec_lifecycle_findings`) riding the warn-plain / error-under-`--strict` tier
  + SR-109/LLR-097/TC-100 + 4 tests; (c) `test_dogfood_sync` MAPPING walk vs a
  declared-omissions list; (d) the sweep — 61 specs archived, 137 done-row
  SpecRefs cleared; (e) PROCESS_OPTIONS / specs-README / enforcement-audit prose.
- **WI-252** — plan/build cadence ⇄ trajectory layer mutual exclusion + a
  `PLAN.template.md` header note.
- **WI-253** — FILED ONLY (spec + queued row + rubric anchor T8).
- **WI-254** — `.githooks/pre-commit` sweeps `.coverage` residue.

Worst failure classes hunted first (R3): R-F fail-open at the gate; the sweep
silently orphaning durable content; the WI-254 `rm` deleting a tracked/staged
file; a lying archive banner; a dead (non-biting) test; byte-stamp drift.

## What I verified (driven, not assessed — R2)

**1. R-F clean; only pre-existing strict error.**
```
$ python project-trajectory/scripts/check_trajectory.py --root .
check_trajectory: WARN - perceptual-stale SR-052;SR-053;SR-054 ... (render surface changed)
check_trajectory: clean (252 work item(s), 237 done (94%), graph acyclic).   EXIT=0
$ python project-trajectory/scripts/check_trajectory.py --root . --strict
check_trajectory: ERROR - perceptual-stale SR-052;SR-053;SR-054 ...
check_trajectory: 1 error(s) in docs/requirements/work-items.csv.            EXIT=1
```
The sole `--strict` error is the pre-existing WI-243 perceptual-stale re-fire; no
R-F finding on the live registry.

**2. Scratch R-F violation fires (drove `spec_lifecycle_findings` directly).**
A done WI with a SpecRef → fires ("still set"); an uncited live spec → fires
("no open WI"); `README.md`/`WI-000.md` → excluded; a `deferred` WI's cited spec
→ no fire (shared-doc lives while any open citer remains). All four branches
behave as specified.

**3. Tests bite.** `pytest -q tests/test_trajectory.py tests/test_dogfood_sync.py`
→ **126 passed**. The 4 R-F tests assert the literal `R-F WI-001` / spec-path
strings that only exist when `spec_lifecycle_findings` returns findings — they go
red on revert. The MAPPING walk ships an explicit bite-proof
(`test_bite_scaffold_walk_catches_an_undeclared_absence`) and an honesty half
(`test_scaffold_omissions_list_is_current`) that fails if a declared omission
materializes.

**4. Links resolve after the move.**
`check_docs.py` → `204 doc(s), 638 intra-repo link(s), 0 broken`. The archive
census glob was added to `docs/orphans-allow`.

**5. Banners match the registry (spot-checked ≥5).** WI-230/159/243 → each
`done`; `main-decomposition` → WI-080/081 both `done`; `parallel-wi-dispatch` →
WI-176…186 all `done`. Attribution and the "all `done`" claim are accurate.

**6. Losslessness (sampled 3 design-notes-shaped docs — the orphan-risk class).**
`parallel-dispatch-design-notes` is explicitly non-normative decision history;
`derived-gate-model` is RATIFIED and fully realized in `derive_gate.py` + the
SR/LLR spine; `open-items-surface` maps to live `check_docs.py` lints + the
two-file split. No durable content left without a home. `log.md` (2026-07-20
"WI-251d") carries per-spec dispositions; four independent verifiers reported
61/61 absorbed — consistent with the sample.

**7. R-F blast radius.** `check.py` appends `--strict` to the trajectory step
**only** at `gate in ("G2","G3")`; `all` (the pre-commit floor) is deliberately
excluded. So an adopter with accumulated done+SpecRef rows warns at every commit
and reddens only at their next G2/G3 gate; opt-out is `docs/trajectory-check`.
Claim holds in code.

**8. Byte stamps match.** `wc -c` → PROCESS_OPTIONS.md **159,787**, PROCESS.md
**60,169**; the byte-budget-guard SKILL.md baseline stamps read 159,787 /
60,169 in all three copies (`project-trajectory/`, `.claude/`, `.agents/`).

**9. WI-254 hook is safe.** `rm -f "$ROOT"/.coverage "$ROOT"/.coverage.*` —
non-recursive, exact top-level names; both patterns are gitignored
(`.gitignore` lines 6–7). The one tracked `.coverage*` file, `.coveragerc`, is
**not** matched by the `.coverage.*` glob (no dot after `coverage`). It touches
only the working tree (never the index), so it cannot drop a staged blob from a
commit. The shipped kit hooks (`project-trajectory/hooks/*`) are untouched in the
range; `.githooks/commit-msg` is a wrapper delegating via `KIT_SCRIPTS_DIR`, not
a copy.

**10. commit-msg hook fires.** Drove it: a clean message → `check_privacy: clean`
(exit 0); a message carrying `AKIA…` → `1 finding(s) … [secrets floor]` (exit 1).
The always-on message-side secrets floor works.

**11. Registry + spine coherence.** WI-251/252/253/254 all `queued`, empty
Deliverable, SpecRef resolving to `docs/specs/WI-25x.md`. `trace.py --strict`:
`SN=25 SR=109 LLR=97 TC=100 orphans=0 integrity=0`. TC-100 cites all four R-F
tests. Sweep totals confirmed: **61** archived, **0** done rows still carrying a
SpecRef, **11** legit live specs (boilerplate + open/deferred citers + this
session's queued WIs). Dogfooded copies are byte-identical to their templates
(specs README/WI-000, rubrics README/rubric-000). WI-252's mutual-exclusion note
is reciprocal on both sides + the PLAN.template.md header; WI-253's T8 anchor is
well-formed and the intro `T1…T7` was correctly bumped to `T1…T8`.

**12. Full suite (close bar): `pytest -q -n auto` → 1242 passed, 4 skipped.**

## Findings

- [MINOR] docs/status.md:1 -> the forward-only lean surface is over its 120-line
  budget (`check_docs` WARN: 131 lines) and this session pushed it further
  (126 → 131) by adding the WI-251 block without trimming the now-historical
  dashboard-quality workstream prose it sits under -> trim the closed-workstream
  narrative to `log.md` (or record a `docs/status-lint` override) so the snapshot
  stays lean -> @owner
- [MINOR] tests/test_dogfood_sync.py:357 -> the dogfooded specs/rubrics
  boilerplate is gated for **existence** by the MAPPING walk but not for
  **structure**, unlike the registry-header/launcher drift checks; the spec's own
  "STRUCTURE must not drift" intent is only partially realized. The four copies
  are byte-identical to their templates today (verified), and they carry no
  instance-specific VALUES, so a cheap byte/structure pin would fully close the
  gap and catch a silent future edit -> add a template-equality assertion for the
  four copied convention docs (they legitimately have no VALUES to diverge on) ->
  @owner

Both are low-stakes; every worst-class hunt (R3) — R-F gate fail-open, sweep
content loss, the `rm` deleting tracked/staged files, a lying banner, a dead
test — was driven and survived, and every WI-251 Done-when item maps to a driven
observation above (R4).

- VERDICT: APPROVE findings=2
