## 2026-08-31 — WI-543: SR-163's owner — the tolerant reference cell, the four-class checker warn-first, the direct TC (OI-72)

Re-scoped row per `OI-72`'s ruling (log.md 2026-08-31). SR-163's verification is
mechanism-first: ship the tolerant `MAPPING` reference cell, a checker that runs
the four finding classes over the real inventory, and a direct TC on SR-163 that
proves the checker catches each class on a scaffold — with the reference
burn-down begun, not finished.

### Build

1. **Tolerant cell** — `bootstrap.py::MAPPING` rows may carry a requirement
   reference as an optional third element; `bootstrap.mapping_entries()`
   normalizes every row to `(src, dst, ref|None)` so a bare pair keeps working
   and is by definition an unmapped-entry warning. All consumers (the copy pass,
   the dogfood walk, the kit-path invariant, the resync/profile tests) unpack
   pairs and triples.
2. **The checker** — in `gen_arch_map.py` (LLR-204's module, the purpose-
   reference home), the forward direction beside the backlink machinery:
   `mapping_purpose_findings(entries, present, sr_by_id, sn_ids,
   declared_absences)` returns the four classes; `resolve_requirement_reference`
   is the SR → live-stakeholder-need join stated once; `load_spine_index` loads
   the repo's SR/SN registries; `mapping_purpose_report` computes the pass.
   `MAPPING_FINDING_POLICY` is the one home for warn-vs-gate: `unmapped_file` and
   `unresolved_reference` WARN, `missing_file` and `stale_entry` GATE (they are
   already delivered/zero via the dogfood+bootstrap checks). The stale arm
   honors the `LIFECYCLE:` marker, the same rule the dogfood walk applies. The
   flip of a warn class to gate at count zero is a later reviewed commit.
3. **The direct TC on SR-163** — TC-204 (`tests/test_mapping_purpose.py`, Smoke
   tier so it runs on every commit bar): plants one defect of each class on a
   synthetic scaffold plus a clean control and asserts each is reported; drives
   the checker over the real `bootstrap.MAPPING` + this repo's real spine and
   asserts NO gate-class finding survives (the standing every-file-maps
   evidence) and every filled reference resolves. Registered Drafted (SR-163 is
   Approved; approving TC-204 is the owner's act).
4. **Burn-down begun** — 20 references filled to unambiguous EXISTING SRs
   (`SR-049` derived stage, `SR-137` one policy home, `SR-146` prompts ×9,
   `SR-147` spine registries ×3, `SR-159` interfaces ×2, `SR-015` perf budgets,
   `SR-151` hosted CI, `SR-161` hats). No new SR needed yet — no filled file
   lacked a justifying requirement.

**Baseline (recorded for the burn-down):** of 147 MAPPING rows, 20 carry a
resolved reference and **127 remain bare (unmapped_file WARN)**; 0 unresolved, 0
missing, 0 stale over the real inventory. The 127 is the count the burn-down
retires against; gating flips only at zero, per the ruling.

### Design notes

- No new LLR: the ruling keeps the wi508 rows (LLR-203/204, TC-199/200) as they
  are and makes TC-204 a DIRECT test on SR-163. The checker's functions carry no
  `Implements:` tag / LLR — back-link coverage is warn-only, and the mechanism
  is verified by its direct TC.
- No new `stack.ini` step: `bootstrap.py` is excluded from its own MAPPING and
  never ships downstream, so a harness step over `bootstrap.MAPPING` would be
  dead in every adopter. The kit self-check home is the test, which runs the
  checker over the real inventory on every suite run — the "on every run"
  evidence the ruling asks for. An adopter with their own inventory can call the
  `gen_arch_map` functions directly.

### Close

- **Harness re-stamps (reviewed baseline edits naming this WI):** the checker's
  new behavior grew two ratcheted modules past baseline — `bootstrap.py` +29
  SLOC (1571 → 1600, the tolerant cell) and `gen_arch_map.py` +79 SLOC (1262 →
  1341, the four-class checker) — both re-stamped UP in `tests/test_module_size_ratchet.py`
  as reviewed bumps, not monolith drift (the placement is LLR-204's module by
  the ruling; decomposition remains WI-521's program). TC-204's 17 in-process
  smoke tests pushed the smoke tier to 1450 collected, so `docs/stack.ini`
  `[smoke-budget] max-tests` re-stamped 1440 → 1458 (+8 headroom, the standing
  small-slack posture); the seconds budget is NOT touched (smoke wall 21.8 s vs
  60 s).
- **Approval brief regenerated** (`trace.py --approve modified`): TC-204 (the
  one spine row this WI minted, Drafted) now appears in `docs/ratify/CURRENT.md`
  as ADDED-since-snapshot / never-approved — approving it is the owner's act.
- **Verification:** commit bar green — smoke 1442 passed / 8 skipped / 23.6 s,
  budget within (60 s). Full unfiltered suite: **3199 passed, 24 skipped, 1
  failed** in 586 s. The one failure is
  `tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`: this
  WI's `8978b265` added TC-204 to `docs/test/test-cases.toml` (a declared
  stage-derivation input), staling the committed `docs/stage` fingerprint. That
  is an EXPECTED work-branch condition, not a regression — `docs/stage` is a
  trunk-lane-regenerated generated artifact (the `derived-stage` pre-commit step
  SKIPS on a work branch precisely because "generated freshness is the trunk
  lane's, §5.2", and `git log -- docs/stage` shows it moves only on
  claim/mint/refresh trunk commits, never on a worker WI commit). The branch
  rules forbid a worker from regenerating it; the trunk lane re-derives it at
  merge and the test goes green on trunk. Latent gap surfaced (NOT fixed here,
  out of SR-163 scope): the dogfood test mirrors the commit-bar `--check` claim
  but, unlike that check step, is not work-branch-aware, so it reds on ANY work
  branch that touches a stage-derivation input — a candidate OI for a
  work-branch skip mirroring the step.

### 2026-09-01 — REVIEW-A rework: wire the checker to a delivered path (MAJOR)

REVIEW-A (`docs/reviews/wi-543-sr163-verification-tc/005-REVIEW-A-47579c8.md`)
returned CHANGES-REQUESTED with one MAJOR: `mapping_purpose_findings` /
`mapping_purpose_report` were defined in `gen_arch_map.py` but reached only from
`tests/test_mapping_purpose.py` — no delivered CLI, bootstrap flow, or `check.py`
step called them, so a real unmapped/unresolved/missing/stale inventory entry
produced no SR-163 report or gate. The mechanism was verified but not *wired*.

Fix (mechanism-first, one delivered home, no new LLR/TC — the same posture the
ruling took):

- **`mapping_purpose_over_repo(root)`** — the ONE delivered function that
  assembles every environment fact the pure checker needs from the real repo:
  `bootstrap.mapping_entries()` (the inventory), `load_spine_index` (SR/SN), and
  `check_doc_refs.load_declared_absences` (the ledger), plus the kit-served
  `present()` predicate. The `bootstrap`/`check_doc_refs` imports are deferred to
  call time via `_import_sibling` (the `spine_carrier` idiom) so a plain
  `gen_arch_map` invocation never pays to import `bootstrap`.
- **`--mapping-purpose`** — a warn-first REPORT MODE on `main`, the
  `--backlink-coverage` sibling (`_mapping_purpose_exit`, added to the composing
  `modes` tuple so it runs beside the other report modes and the verdict is the
  worst). Exits 1 only on a gate-class finding; unmapped/unresolved rows are
  reported but never gate — the burn-down stays visible without a flag day.
  Verified over the real repo: 127 unmapped WARN, 0 gate-class, exit 0.
- **TC-204 now drives the delivered path.** `_real_mapping_findings` collapsed
  onto `mapping_purpose_over_repo` (was a hand-assembled copy of the same logic),
  so the standing evidence and the shipped command grade the inventory through
  identical code. Added `tests/test_mapping_purpose_cli.py` — two end-to-end
  subprocess drives of `gen_arch_map.py --mapping-purpose` (green over the real
  repo; gate-class `missing_file` fires and exits 1 when `--root` points at a
  tree missing every destination). Kept SEPARATE and re-tiered into
  `conftest.SLOW_MODULES` (the `test_check_complexity_cli` precedent): each case
  pays interpreter startup, so the commit bar drops it and close/CI runs it — the
  in-process unit module stays in smoke unchanged, so `max-tests` stays 1458.
- **Ratchet re-stamp:** `gen_arch_map.py` +53 SLOC (1341 → 1394) — the delivered
  path and CLI wiring — re-stamped UP as a reviewed bump in
  `tests/test_module_size_ratchet.py`. Not decomposed: it is the report-mode
  sibling of `_backlink_exit`, same file, same `main` dispatch.
- **`docs/cli-reference.md` left stale on purpose:** the new flag changes
  `gen_arch_map`'s argparse surface, but the `cli` artifact is a trunk-owned
  generated block (its freshness step SKIPS on a work branch, and it rides
  `trunk_step.py --regen`). A worker must not commit it; the trunk regenerates it
  at merge.

Verification (rework): commit bar green — smoke 1442 passed / 8 skipped / 23.0 s,
budget within (60 s). Full unfiltered suite re-run recorded at close below.

### 2026-09-01 — REVIEW-A round-2 rework: enumerate the delivered universe (MAJOR)

REVIEW-A (`docs/reviews/wi-543-sr163-verification-tc/007-REVIEW-A-35c7146.md`)
returned CHANGES-REQUESTED with one MAJOR: the newly delivered
`mapping_purpose_over_repo` still supplied the checker only
`bootstrap.mapping_entries()`. The declaration therefore also defined the
universe being checked; deleting the real `process.toml.template →
docs/process.toml` row made that shipped source invisible and left the report
green.

Root-cause correction selected before implementation: the bootstrap boundary
will expose an independent delivered-package census. Every physical kit source
must be classified exactly once as a `MAPPING` source or a reasoned exclusion;
generator-derived scaffold outputs will name the mapped generator row whose
reference they inherit. `mapping_purpose_over_repo` will diff that universe
against the live manifest before grading destinations/references, and an
end-to-end TC-204 regression will remove the real process-policy row and require
the shipped command to report and gate the omission.
