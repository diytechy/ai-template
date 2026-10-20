# WI-926 — adjudication of the plan-cap dispute (F1)

Adjudicator: an independent Claude Opus 5.5 session launched by the
coordinator. It did not write the plan, either critique or the findings file.
Range judged: `c58293d5443a881585864be3491f6e0cd0c749c0..1bf2896b4206d67f126f46cbc359d13e74674274`.
The plan at the range tip is byte-identical to the Reviewed revision
`94805b4c4` (`git diff 94805b4c 1bf2896b4 -- docs/plans/WI-926/plan.md` is
empty). Scope bound: `project-trajectory/PROCESS.md` §6 "Review threat model",
read before ruling.

## F1 — no plan step registers `kitlib/commit_hooks.py` in the bootstrap MAPPING

**The premise holds.** `project-trajectory/scripts/kitlib/bootstrap_manifest.py`
lists each `scripts/kitlib/*.py` module as its own MAPPING row (lines 329–417),
and bootstrap copies those rows; it does not discover modules. The plan's P3
creates `kitlib/commit_hooks.py` and no step adds its row. P12 names the module
as a shipped file only in the RESYNC entry.

**The failure scenario does not.** The finding says a fresh scaffold would get
the changed routes without their new dependency, and that only P13's full
suite would surface the gap. Neither part holds on this range. SR-163's
delivery census walks every physical file under the kit and requires each one
to be classified (MAPPING row, reasoned exclusion, conditional or generated
copy). Its tests live in `tests/test_mapping_purpose.py`, which is **not** in
`tests/conftest.py`'s `SLOW_MODULES` (only `test_mapping_purpose_cli` is), so
they run in the smoke tier, the per-commit bar the plan's P13 binds on every
slice (`run.cmd smoke`).

I reproduced it rather than reasoning about it. I placed a stub
`project-trajectory/scripts/kitlib/commit_hooks.py` with no MAPPING row and
ran `pytest tests/test_mapping_purpose.py -k "delivery_census or gate_class"`.
Two tests failed, and both named `scripts/kitlib/commit_hooks.py`:
`test_delivery_census_classifies_every_physical_package_source` and
`test_real_mapping_has_no_gate_class_findings`. Then I removed the stub, and the
tree was clean again. So P3's own commit, the first one that adds the module,
fails the bar the plan already requires, and the failure names the missing
row. The omission cannot reach a commit, a landing or an adopter's scaffold
through any supported workflow. That puts its consequence outside the
reachability the threat model requires. Severity tracks plausibility and
impact, and a gap the kit's own per-commit gate mechanically closes is not
a MAJOR coverage defect in the plan.

The rest of the requested fix is either already covered or not owed:

- `test_the_common_package_ships_complete` and the scaffold refusal and passing
  paths run in P13's full unfiltered suite, which the plan already names.
- The fifteen-name kitlib list in `tests/test_bootstrap.py` is a declared
  spot-check ("asserts the set EXACTLY ... these fifteen rows are the
  spot-check"), not an inventory that must grow with each new module.

Naming the MAPPING row in P3 would be harmless, but the plan is not deficient
without it.

RULING: F1 DISMISS refuted the unregistered module cannot reach a scaffold: SR-163's delivery census (tests/test_mapping_purpose.py, smoke tier, not in SLOW_MODULES) fails P3's own commit bar naming scripts/kitlib/commit_hooks.py, reproduced by stubbing the file with no MAPPING row (2 failures), so the per-commit gate the plan already binds forces the row and no supported workflow ships the gap
