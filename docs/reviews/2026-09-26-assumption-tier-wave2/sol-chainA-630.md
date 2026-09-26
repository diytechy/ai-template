5453f920 SOUND  
b501e5f4 NOT YET SOUND

### 5453f920

Context-only verdict: no defect found in the surfaces WI-630 consumes.

### b501e5f4

- **[major] IF-190’s single entry point is bypassed, and tests cannot detect lost checker composition.** IF-190 says one tier entry point owns finding classification (`docs/requirements/interfaces.toml:1838`), and its contract identifies `assumption_tier_findings` as that entry (`project-trajectory/scripts/assumption_rules.py:50-55`). Instead, `trace.analyze` imports and composes both reports separately (`project-trajectory/scripts/trace.py:223-225`, `5045-5055`). TC-214/TC-223 invoke the leaf functions directly (`tests/test_assumption_rules.py:430-432`, `596-597`), so deleting lines 5053-5055 would leave every new test green while the delivered harness stopped reporting both behaviors. Fix in **b501e5f4**: extend `assumption_tier_findings` with needs/stakeholders and compose both reports into its advisory result; make `trace.py` import only that entry point; add a composition test that fails if either advisory is absent from the entry-point result. Update IF-190’s body/data and re-stamp the reduced `trace.py` ratchet.

- **[minor] An undeclared surrogate produces misleading reach advisories in addition to its reference failure.** `_emulated` silently discards an unresolved `RealizedBy` id and returns an empty set (`project-trajectory/scripts/assumption_rules.py:548-560`); the caller nevertheless marks the assumption as fidelity and reports both its served need and landing as unreachable (`project-trajectory/scripts/assumption_rules.py:632-641`). Comparable undeclared crossings and needs are skipped. Fix in **b501e5f4**: do not run fidelity reach evaluation unless `RealizedBy` resolves to the valid surrogate shape; add the missing unresolved-surrogate reach test.

- **[minor] The negative fidelity test does not prove both clauses of LLR-227.** `test_a_fidelity_assumption_landing_elsewhere_is_reported` asserts only an advisory naming `B-01` (`tests/test_assumption_rules.py:550-557`). It still passes if the required per-served-need report naming `SN-001` disappears. Fix in **b501e5f4**: assert the exact two findings—one naming the unreached need and one naming the idle landing crossing.

### CROSS-CHAIN

No additional cross-chain defect. The major fix changes WI-629’s `assumption_tier_findings` entry point, so its earlier calls in `tests/test_assumption_rules.py` must be updated in **b501e5f4**; no registry, carrier, classifier, interface-ID, or watermark migration ripples beyond that.

The current repository data produces zero new reach advisories or mediation failures, as intended for its zero real assumptions, stakeholders, and operation crossings. `check_trajectory.py --strict` exited 0. The in-memory Smoke module passed: `66 passed in 0.17s`. The requested `-n 2` run and Full-tier scaffold tests could not initialize because the read-only sandbox provides no writable temporary directory.