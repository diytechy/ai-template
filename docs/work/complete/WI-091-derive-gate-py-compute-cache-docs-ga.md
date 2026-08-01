+++
id = "WI-091"
title = "derive_gate.py - compute + cache docs/gate + --check"
workstream = "scripts"
needs = ["WI-089", "WI-090"]
order = 90
+++

## Deliverable

New scripts/derive_gate.py (stdlib, self-contained per F5 - small loaders duplicated from trace.py, never imports the joined-spine engine) computes the gate from artifact states (spec §3/§5): sr_gate (Draft->G0; ratified-undecomposed->G1; decomposed->G2; decomposed+Verified->G3; LLR-exempt methods need only a TC), maturity_gate for LLR/TC (Draft->G0 else never-caps: the SR's Verified status drives G2->G3, matching trace --require-verified which checks SRs not LLR/TC - so a downstream repo with `Implemented` LLRs still reaches G3), sn_gate (draft section->G0 else never-caps). Repo gate = min over all in-scope artifacts (no real SRs => G1, never a vacuous G3); a draft/reopen drops it (the new-phase signal, floored to G1 for the runnable value with the raw G0 recorded in the basis). Hybrid cache: writes docs/gate as a generated file (static header + a compared `# basis:` line + an informational git-derived compute stamp + the runnable value as the first non-comment line, so check.py resolve_gate reads it unchanged); --check recomputes + guards rot (a legacy no-basis hand-set gate compares value-only so the meta + fresh scaffolds stay green until WI-096 migrates); --print computes without writing. Bootstrap MAPPING ships it downstream. Meta dogfood: derive_gate --print reads G3 (SN=24 SR=48 LLR=49 TC=49 drafts=0), matching the declared docs/gate. check.py wiring is WI-092; the meta docs/gate migration + derive_gate's own SR/IF rows (the 1 interim connectivity warn) are WI-096. Tests: test_derive_gate.py (12: meta-smoke G3, every per-artifact rule, min-aggregation, draft SR/SN drop, undecomposed G1, decomposed-unverified G2, no-SR G1, write+--check roundtrip, drift detection, legacy value-only --check).
