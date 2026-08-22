## 2026-08-22 — WI-501: the stale-Approved-cell repair batch, OI-53's ruling (b) executed

Deferred open items: none — SR-139's possibly-uncounted third/fourth dirty
cell is flagged for WI-499's worker to independently verify (see below),
not deferred as an owner decision; it is a scope note between two tracked
rows.

**Why.** The backlink-coverage campaign (WI-487/ROUND-OPUS) surfaced a dozen
Approved LLR rows whose `CodeSymbol` cell names a symbol that no longer
exists at the cited module — honest tag, stale row, and an Approved cell an
ordinary worker may not amend without a ruling. OI-53 ruled (b): a tracked
repair row under the ordinary review round, since only the `DevStg-Needs`
tier is human-held. The program close the same day re-scoped the
population by VALUE (grepping retired vocabulary across every registry
carrier) rather than by row name, landing at 22 rows / 37 cells, and
separately owed the SR that `derive_stage.phase_rule_findings` should have
pointed at instead of the mis-traced SR-139.

**What shipped.** Full per-row dossier — every repaired cell, its old and
new text, and the file:line evidence that warranted the fix — lives in
`docs/work/complete/WI-501-stale-approved-cell-repair.md`'s `## Deliverable`
(read there for the row-by-row table; not restated here). Summary:

- **CodeSymbol class: 12 rows addressed** (LLR-175, LLR-011, LLR-143,
  LLR-089, LLR-050, LLR-157, LLR-057, LLR-104, LLR-108, LLR-068, LLR-155,
  the LLR-172-adjacent note). 11 got a real edit; the LLR-172-adjacent note
  was verified clean (`component_findings` genuinely exists at
  `check_trajectory.py:1738`, matching a prior WI-484 log finding that this
  was already resolved) and left untouched. LLR-142's CodeSymbol (`regen`)
  was also verified clean — only its vocabulary-census `detail` cell needed
  repair, tracked in the next group. Each CodeSymbol repair either renamed
  to the real symbol the module carries today, or narrowed a multi-symbol
  cell to drop the dangling name(s) — never invented a symbol that isn't
  there (verified by direct grep/Read against the live module before
  writing each cell, the WI-482 precedent).
- **LLR-050: reworded, not formally retired.** No `Status = Retired`
  vocabulary exists in the schema, so the row stays `Approved` with its
  `title`/`code_symbol`/`detail` rewritten to record plainly that `compute`
  and the whole per-artifact gate/BAR mechanism it named were deleted
  wholesale by the ruled stage unification, that no successor occupies its
  identity, and that the SSOT argument it made is fully carried forward by
  LLR-185 (the declared-input carrier) and LLR-186 (the per-phase
  derivation). The original `rationale` is kept verbatim as historical
  record per the findings-are-claims discipline — its argument was never
  wrong, only the mechanism it was pinned to.
- **Stale-vocabulary census: 14 rows edited, 7 verified clean and left
  untouched** (LLR-155 vocabulary — its only defect was the CodeSymbol
  anchor, fixed above; LLR-156, LLR-186; IF-081 and PB-004, both already
  repaired inline at the WI-498 close per that close's own notes). Every
  edited cell replaced retired `docs/gate`/`derive_gate`/`derived-gate`/
  the 0-4 numeric ordinal/`arch-map`/BAR-axis vocabulary with the current
  `docs/stage`/`derive_stage.py`/`DevStg-*` rung vocabulary, verified
  against the live scripts and tests rather than assumed — including
  TC-051's two dangling pytest ids, corrected to the real current names
  (`test_process_current_stage_highlight_follows_docs_stage`,
  `test_process_tab_omitted_and_byte_identical_without_stage`, both
  confirmed present in `tests/test_traj_panels.py`).
- **SR-139 / WI-499 split, recorded explicitly.** SR-139 got 2 cells
  repaired (`requirement`, `acceptance_criteria`) for the retired 0-4
  ordinal / harness-gate mapping only. The word "ratification"/"ratify" —
  in SR-139 and everywhere else this batch touched — is untouched
  deliberately: that rename is WI-499's scope, not this row's. WI-501's own
  Context named "four dirty cells" for SR-139; only two are independently
  substantiated by this session and by ROUND-OPUS.md itself. Flagged for
  WI-499's worker to re-verify rather than assumed settled.
- **W-15 — SR-181 minted.** "A spine edit that lowers the effective stage
  surfaces as a phase change" (`sn_refs = SN-004, SN-008`; `phase = 5`;
  `aspect = "process"`), `status = "Approved"` — machine-approvable, the
  same mint-status precedent WI-483 used for LLR-188/LLR-189 the same day,
  verified against the machinery (`intake.py snapshot --approves` ran
  clean) rather than merely asserted. `derive_stage.phase_rule_findings`'s
  docstring re-pointed from the mis-traced `Implements: SR-139` to
  `Implements: SR-181`, with a short citation-frame-free note recording the
  correction (the full account lives here and in the Deliverable table, not
  in the docstring — `trace.py`'s spine stand-alone rule).
- **Snapshot reconciliation, same commit.** `intake.py snapshot --approves
  "OI-53 (b), 2026-08-22 -- docs/log.d/2026-08-22-oi53-54-rule.md"` mirrored
  all 7 spine-tier registries into `docs/archive/last_approved/` after the
  edits landed — no fabricated warrant; the ruling itself is the citation,
  the same shape WI-494 used for OI-48.

**A real miss caught by `trace.py --strict --strict-integrity`, fixed
in-session.** The first pass of new prose (SR-181's rationale, LLR-050's
title/detail/rationale, LLR-147's detail, LLR-157's detail, TC-170's
method) cited `WI-498`/`WI-501`/`OI-53`/`OI-51`/`WI-455`/dates directly —
6 new `WARNING (advisory)` + 6 new `FINDING (spine stand-alone)` lines, the
same class WI-494 hit. Reworded to timeless prose with zero citation
tokens; a second run showed zero surviving citation-frame findings.

**Gates**, real output, Windows, `.venv` Python 3.11.9, `-n auto`:

- `check_doc_refs.py --root . --strict`: dangling references **197 -> 196**
  (LLR-050's `compute` WARN — the only CodeSymbol defect this population
  actually gated on — cleared; zero new dangling introduced)
  <!-- fig: cmd="python project-trajectory/scripts/check_doc_refs.py --root . --strict" rev=8848f6fb -->.
- `check_trajectory.py --root . --strict`: **identical** before/after — 105
  WARN/FINDING lines both sides, exit 0 both sides. HOLD
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=8848f6fb -->.
- `trace.py --root . --strict --strict-integrity`: `integrity=0` unchanged
  before/after (the SR-181 approval-record/integrity findings the mint
  produced cleared once the snapshot absorbed it). The only surviving diff
  against the pre-session baseline is expected: `orphans` 13 -> 15 (SR-181
  freshly minted, no LLR/TC child yet — the same shape every other pending
  SR in this registry already carries) and the hat-coverage denominator
  244 -> 245 (one more requirement row to attribute).
- `check.py --run-steps okf,trajectory-map,status-map,open-items,trajectory,`
  `registry-integrity,derived-stage,skills-sync,skills-index,prompt-catalog,`
  `ratify-fresh,staged-divergence`: all 12 steps PASS after one
  `trunk_step.py --regen` (derived-stage/trajectory/status/open-items) and
  `git add -A` (staged-divergence needs the regenerated bytes staged).
- `python -m pytest -q -n auto -m smoke`: **1368 passed, 5 skipped in
  61.95s** <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=8848f6fb -->
  — a hair over the WI-281 60s budget; the standing rule is one machine is
  one data point (CLAUDE.md's own measured range on this box spans
  54.9-64.0s across three prior warm runs), not something this registry-only
  change moved.
- `python project-trajectory/scripts/check_docs.py --root . --stale`: OK —
  1008 doc(s), 1345 intra-repo link(s), 0 broken (1 pre-existing orphan
  warning; the rest are non-blocking staleness hints, expected after a
  registry-wide edit) <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root . --stale" rev=8848f6fb -->.

Registry-only change (plus a docstring comment in `derive_stage.py`), so
the full unfiltered suite is not owed by CLAUDE.md's own rule — no
executable code changed, only a docstring/comment edit.
