## 2026-08-02 — WI-402: Phase is numeric-only, and the next phase is a derived call

**Summary.** Owner rulings 2026-08-01 (dispatcher-flow review). Two halves.
(1) `trace.phase_ratified_findings` (`--strict-schema`, G3 where the tier
already bites) tightens from digit-parses to **full-cell bare integer** on
every ratified SR/LLR/TC once any spine row is phased. Numeric-only is a
correctness rule, not a style: the `--phase`/`--ratify` scope filters
(`in_phase`/`_scope_srs`) and check_trajectory's phase-drop detector join the
cell **literally** (`per-phase=` basis labels against `[phase]-[gN]` title
anchors), so a prefixed `P1`/`v2` cell did not fail them — it went *silently
vacuous*, disarming a warn without telling anyone, worse than a crash.
(2) `derive_gate.py --next-phase` prints max(Phase over non-draft spine
rows) + 1 — the basis line's `phase=N` derivation exposed as an output mode
(docs/gate never written), printed bare so the intake mint helper (WI-388,
future) can shell out and `int()` it. On this repo it prints 5
<!-- fig: cmd="python project-trajectory/scripts/derive_gate.py --next-phase --root ." rev=e0623526 -->.

**Spec re-validation (the standing SpecRef WARN, first act).** The spec was
re-read against the WI-401-amended `registry-machinery-reference.md` before
building: no conflict — WI-401's additions (`sn_cited_ids`, `uncovered=`, the
gate-rung/orphan-listing seam) live in §2.1/§6/§8; this WI's edits land
*beside* them in §3.3, the §3 column table, §12.7 and §13, with §3.3
cross-referencing the §8.3 basis line it already documents. Both docs' edits
compose; nothing WI-401 wrote was overwritten.

**Deliverables.**

- **The rule** (`project-trajectory/scripts/trace.py`): once armed
  (digit-parse arming — a `v2` cell arms it too), a ratified row's stripped
  `Phase` must `re.fullmatch("[0-9]+")`; the finding names the cell and the
  literal joins a prefix disarms. A legacy `vN` registry now arms the rule
  AND fails it, per cell — the deliberately retired pre-WI-402 guarantee.
  `phase_num` and its F5 copies stay digit-extract (grandfathering: legacy
  labels still filter and derive); legacy `[v3]`-style title anchors under
  `docs/work/complete/` are history, never rewritten.
- **The helper** (`project-trajectory/scripts/derive_gate.py`): `--next-phase`
  is an output mode over the existing derivation (no second parse, no
  docs/gate write); a Draft row's phase is not yet scope and never bumps the
  answer; an unphased spine is the implicit foundation (1), so it prints 2 —
  printing 1 would collapse new scope into the foundation the blank rows
  occupy (spec was silent here; pinned by test).
- **The ruled boundary, recorded where the derivation is documented:** a phase
  increments when re-opened scope is *confirmed* — an adjudication verdict
  that scope moved, or a new draft-SN batch ratified into scope — **never on
  the raw derived-gate drop**; a spurious `Modified` window must not burn a
  phase number (the 19-traced-cells counterexample). Recorded in
  `registry-machinery-reference.md` §3.3, PROCESS.md §4 (it speaks of phases;
  §-numbering untouched), process-options "Phased delivery", and both
  scripts' comments.
- **The v2-blessing sweep:** every live "a downstream `v2` still parses"
  updated — the SR template's Phase comment, the reference doc (§3 table,
  §3.3, §12.7, §13 example now `--phase 2` + the `--next-phase` line),
  PROCESS.md §4, process-options, EXAMPLE.md — and the ADOPTING.md §6 resync
  ledger carries the migration note: a `vN` registry arms-and-now-fails, strip
  prefixes (`v2` → `2`) on resync; `Phase` is a *traced* cell, so the edit
  opens no re-attest window.

**Judgment calls / deviations.** (1) Registration shape: LLR-003 `Detail` and
TC-003 `Method` asserted "a downstream vN parses and passes" — false once this
landed — so both cells were amended to the built truth in the work commit (the
WI-392 REVIEW-A-rework precedent: amend the cell, the review adjudicates; no
`Modified` flip — the requirement itself did not move, and opening a spurious
window is this WI's own counterexample). The new behavior rides new rows per
the WI-393/401 precedent: LLR-148 + TC-142 under SR-049 (CMP-001, Phase 4).
(2) The provenance rule convicted WI ids in the first draft of the amended
cells; reworded — a spine row states the system, not its history. (3)
EXAMPLE.md also blessed `vN` (the spec named the template comments + reference
doc); updated for truth in the same sweep.

**Bookkeeping, reasons in place:** trace.py size baseline 2909 → 2919 (+10:
the docstring now records the literal-join rationale and the grandfathering
stance — the reason a successor must not "simplify" the rule back to the
parse). Skills-sync caught the third tracked byte-budget-guard copy
(`.agents/`); refreshed via `bootstrap.py --sync`. No rule-sync change —
`phase_num` is untouched on both sides; no new duplicated predicate.

**Byte deltas:** AGENTS.template.md 9,991 (untouched); PROCESS.md 64,319 →
64,460
<!-- fig: cmd="wc -c project-trajectory/PROCESS.md" rev=e0623526 -->
(+141: the §4 note's numeric-only tightening + the boundary sentence + the
`--next-phase` pointer); PROCESS_OPTIONS.md 168,222 → 169,010
<!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md" rev=e0623526 -->
(+788: the numeric-only paragraph with its literal-join rationale replacing
the free-form-string blessing, the boundary paragraph, the helper). Both
baselines re-stamped in every tracked byte-budget-guard skill copy in the
work commit.

**Watched, measured on the work commit e0623526 (clean tree):** red first — 4
failed on the claim tree (the retired vN-passes assertion, the prefixed-P1
scaffold, both `--next-phase` fixtures: unrecognized argument), then green.
Smoke tier 616 passed / 6 skipped in 10.41s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=e0623526 -->;
full suite 1870 passed / 10 skipped in 0:04:49
<!-- fig: cmd="python -m pytest -q -n auto" rev=e0623526 -->;
the trace G3 bar (`--strict --no-placeholders --require-verified
--strict-schema`) rc=0; `check_trajectory` / `check_doc_refs` /
`check_figures` all rc=0 under `--strict`; `derive_gate --check` rc=0 on the
regenerated cache (basis now LLR=131 TC=128); `check_docs --stale` stays at
the pre-existing trunk red of 4 broken links (the same WI-070/WI-173/WI-288
record lines, none added by this branch).
