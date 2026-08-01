+++
id = "WI-096"
title = "Migration + dogfood the meta spine"
workstream = "scripts"
needs = ["WI-095"]
order = 95
+++

## Deliverable

Phase close (spec §10.8/§11): the meta's own docs/gate MIGRATED to the derived form - `derive_gate.py` regenerated it (header + `# basis: SN=24 SR=49 LLR=50 TC=50 drafts=0 computed=G3 per-phase=(default)=G3` + a git-derived compute stamp + the value G3), replacing the hand-set G3 comment block. The DOGFOOD is proven: the meta's derived gate reads G3, matching its declared gate byte-for-byte on the value line (resolve_gate reads G3 unchanged); derive_gate --check now full-basis-compares (was value-only) and passes 'up to date (G3)'. ADOPTING §5 (first green run - run derive_gate.py to compute docs/gate; the gate is derived not bumped) + §6 (re-sync ships derive_gate.py + the derived-gate step; run it once to migrate a legacy hand-set gate; value-only until then) updated; derive_gate.py added to the overwrite-freely script list. Retired the last hand-set-gate references in shipped surfaces: ci/check.yml, bootstrap.py (the docs/gate MAPPING comment + the LLM-GATE deviation-register text), check.py --gate help. The design spec's §11 Done-when marked LANDED. End-to-end dogfood test: test_requirement_first_lifecycle_end_to_end (draft SR in the live spine -> gate drops to G1 -> ratify+decompose -> G2 -> verify -> G3, trace clean throughout). RE-ATTESTATION: the effort added SR-049 (WI-092), a new Verified Test SR, so the meta's G3 rides a PENDING owner re-attestation (still all-mechanized: 46 Test / 2 Analysis / 1 Inspection / 0 Attest). No new spine rows in this WI. Full gate bar run at phase close.
