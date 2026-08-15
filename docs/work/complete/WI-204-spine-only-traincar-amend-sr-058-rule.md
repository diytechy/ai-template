+++
id = "WI-204"
title = "Spine-only traincar - amend SR-058 rule 1 so mid-run spine-serial WIs (spine/gate/attestation) pack together into ONE serial spine-only traincar (never with ordinary/protected/high-risk/critique/checkpoint work; whole-project drain + one-active-spine-train invariants unchanged), closing the N-sequential-single-trains residual to match the stage-2 gate pass batching; precedes the dispatcher-migration set so repos migrate onto the amended rule"
workstream = "unattended"
sr_refs = ["SR-153", "SR-156"]
buildtier = "strong"
order = 203
+++

## Deliverable

WI-204 (2026-07-17): SR-058 amended (Requirement+AC+Rationale - spine packs only with spine; owner rulings: attestation rows join the batch, drafted/reviewed/attested together; pause-free under autonomous). agent_loop.pack_traincars gains the spine-only batch: every READY spine-serial WI (mutually independent by construction) seeds ONE spine-only traincar, a fixed-point closure absorbs queued spine-serial WIs whose every hard pred is done-or-aboard (topological append order), chunked at the cap; protected/single-wi/ordinary packing unchanged, empty-spine frontier byte-identical. The worker §7 continuation re-check permits a HOMOGENEOUS spine-only train (fail-closed on any missing sched row) and still refuses heterogeneous groupings. Dispatch drain + one-active-spine-train invariants untouched. Spec text synced: parallel-wi-dispatch.md §4 rule 1 + §7; PROCESS_OPTIONS dispatcher paragraph (rides the WI-206 commit); agent_loop docstring; TC-059 Method/Evidence extended. Tests: 4 packing units (one-car batch incl. attestation, hard-edge order, cap chunking, never-another-class) + 2 end-to-end dispatch pins (batch rides ONE train + zero ratification pause under autonomous; attended still exits with the whole batch as one ratification scope). Re-validated against the amended spec per the WI-205 staleness warn.
