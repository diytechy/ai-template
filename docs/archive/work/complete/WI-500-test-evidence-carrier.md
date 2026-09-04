+++
id = "WI-500"
title = "The test-evidence carrier: the input that makes DevStg-Release reachable (owed by the ruled stage unification plan)"
specref = ""
workstream = "scripts"
sr_refs = ["SR-151", "SR-152"]
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

Full row, not a slice. `DevStg-Release` has exactly one producer and it is a
HARNESS VERDICT, never a cell.

- **The carrier.** `scripts/kitlib/evidence.py` (NEW) holds the
  `docs/test/evidence` record's format — key=value addressed by name, the
  `docs/stage` idiom, carrying `outcome`/`tier`/`command`/`revision`/`binding` —
  the whole-suite tier set, and the declared source surface (read from
  `docs/stack.ini` `[paths]`, never restated), with build residue excluded. It
  imports no sibling; `kitlib/stage.py` composes the folds, so the package stays
  free of a cycle, and its parse NEVER raises, because the file is a claim rather
  than derived state.
- **The binding, value-bound (the WI-492 precedent).** `stage.evidence_binding`
  folds the spine registries (minus the evidence file, which cannot contain its
  own digest) together with the declared source and test trees and
  `docs/stack.ini`. Both halves are load-bearing: without the spine half a test
  case authored after the run rides a green that never executed it; without the
  source half any code edit does.
- **The producer.** `scripts/record_test_evidence.py` (NEW) RUNS the declared bar
  through the documented harness entry point and writes only on exit 0. No flag
  records without running, there is no `outcome = fail` state, and a partial
  (`smoke`) tier is refused at the writer AND again at the reader. Built as a
  wrapper rather than a check step on a structural ground: a verdict about the
  whole run can only be written by something that outlives it.
- **The consumer.** `stage.evidence_verdict` → `derive_stage` (one read, handed to
  both folds through `frame`) → `spine_stage(..., evidence_passed=)`, the rung's
  one return.
- **Staleness is loud, in both directions.** The verdict answers False (the rung
  drops) AND `stage.fingerprint` folds the source surface whenever a record is
  present, so the committed `docs/stage` reads stale and `derive_stage --check`
  reds. That second half is NOT in the row's brief and is why the change is more
  than "an edit to one list": without it a recorded Release rides an unchanged
  evidence file over an edited tree, reachable and invisible.
- **The slice-3 pin retired DELIBERATELY**, as the act its own docstring named:
  `test_the_RELEASE_rung_has_EXACTLY_ONE_PRODUCER_and_it_is_the_EVIDENCE_VERDICT`
  keeps the two mutant-catching arms and adds a third — the one Release return
  must be guarded by the bare `evidence_passed` PARAMETER, so a guard computed
  from Status cells is unrepresentable. Driven against three mutants.
- **The orphan fold-in discharged.** `SR-151` and `SR-152` are decomposed:
  `LLR-190`/`TC-185`, `LLR-191`/`TC-186`, `LLR-192`/`TC-187` (watermarks LLR
  189→192, TC 184→187 via `trace.py --bump-ids`; snapshot refreshed with
  `refresh_refusal` clean).
- **Adopter surface.** `bootstrap.py` MAPPING, `test_bootstrap.py` lists, kit
  `README.md`, `docs/kernel-modules-allow`, PROCESS.md §4 + PROCESS_OPTIONS.md,
  and a RESYNC_PACK §3 entry `[since c3c9b36a]`. Scaffold-verified end to end on a
  real `bootstrap.py --dest` run, including the red path through the scaffold's
  own `check.py`.
- **THIS REPO HAS NO VALID RELEASE EVIDENCE AFTER THIS LANDS, AND THAT IS
  CORRECT.** No producer run was contrived to green the rung; `docs/stage` reads
  `DevStg-LLReqs` before and after, byte-identical in every derived field.

Log fragment: `docs/log.d/2026-08-22-wi500-test-evidence-carrier.md`. `specref`
cleared at close per the terminal-WI rule (R-F); the spec of record it named,
`docs/plans/2026-08-21-stage-unification-plan.md`, is still live for the rest of
the program and is cited in the Context below rather than archived.

## Context

The ruled plan (§5, sequencing note) names this as its own row: WI-498
made `DevStg-Release` evidence-gated with — deliberately — NO producer, so
the rung is unreachable until a test-evidence carrier exists. This row
builds the carrier: a durable, committed record that the declared test
suite ran and every test case passed, produced by the HARNESS (the OI-30
D2 rule survives: no Status cell, and no hand-written file, may ever be
the source of "the evidence passed").

Design constraints gathered by the program (read the plan + the design
record + the slice-3 fragment section before shaping):
- The evidence sources measured ABSENT today, all four: no TC outcome cell
  (by ruling — stays that way), docs/test reports gitignored,
  coverage.json opt-in and deleted per run, no junit/json-report anywhere.
  The carrier is NEW state, and its trust model is the design's heart:
  what makes a committed evidence file believable (producing command +
  revision binding, the declared-figure/fig: discipline, staleness =  <!-- fig-ok: prose about the convention -->
  unreachable again)?
- Once it exists it joins `kitlib/stage.DECLARED_INPUTS` (the one-list
  edit the input design promised) and `spine_stage`'s Release
  discriminator consumes it; the slice-3 structural pin (source contains
  no `return STAGE_RELEASE`) is then retired DELIBERATELY with the
  producer's arrival recorded.
- The evidence claim binds to the TREE it was measured on (the WI-492
  correction-record precedent: value-bound, not space-bound), or Release
  silently rides stale evidence — the failure class the whole unification
  exists to prevent.
- Adopter-facing throughout: RESYNC entry, scaffold verification, and the
  shipped ci lane is the natural producer (a harness driver writing the
  record on a green full run).

**Orphan fold-in (owner-directed 2026-08-22):** this row's build DISCHARGES
the decomposition debt on `SR-151` (hosted CI runs the declared bar per
trigger) and `SR-152` (the hosted CI verdict is the harness's own) — the
two orphaned SRs whose subject IS this carrier and its CI-lane producer.
Mint their LLR/TC rows as part of the design, so the carrier lands traced
rather than rowless.
