+++
id = "WI-092"
title = "check.py consumes the derived gate"
workstream = "scripts"
sr_refs = ["SR-049"]
needs = ["WI-091"]
order = 91
+++

## Deliverable

check.py now consumes the DERIVED gate (spec §5/§10.4). resolve_gate() reads docs/gate's first non-comment line unchanged - the value is simply derived by derive_gate.py now, sitting on that same line with the `# basis:` derivation in comments above - so no read change was needed; its docstring records the shift. New `derived-gate` process step (`derive_gate.py --check`) at every gate G1/G2/G3 guards the cache against rot (the arch-map/OKF/dashboard freshness idiom applied to the gate marker), and joins the pre-commit hook's batched freshness floor (--run-steps ...,derived-gate,...); a legacy hand-set gate (no basis line) is compared value-only, so the meta + fresh scaffolds stay green until WI-096 migrates. conftest.make_minimal_project regenerates docs/gate via derive_gate (a full G3 chain advances the derived gate off the scaffolded G1). SPINE (pulled forward from WI-096 to keep the meta green: adding derive_gate.py as a traced product script needs its spine rows or the meta's own uncontained-module + connectivity invariants go red): +SR-049 (derived gate from artifact states, SN-004;SN-008, Test/Verified) + LLR-050 (Component CMP-001) + TC-050 (tests/test_derive_gate.py) + IF-050 (Provides->check: the docs/gate marker) + IF-051 (Consumes<-system-requirements.csv: the states) + the Contracts docstring; derive_gate now contained + a declared endpoint (trace 0 findings, check_trajectory 0 warns). Meta spine SN=24 SR=49 LLR=50 TC=50, 51 IF seams, 24 modules->5 components 0 uncontained. Rides the effort re-attestation. Tests: test_check_harness.py (derived-gate wired at every gate + run + drift), updated batch test.
