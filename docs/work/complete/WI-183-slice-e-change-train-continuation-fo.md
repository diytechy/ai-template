+++
id = "WI-183"
title = "Slice E - change-train continuation + fork/join"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["WI-182"]
buildtier = "strong"
order = 182
+++

## Deliverable

Slice E (2026-07-16): the traincar execution model over C's worker + D's dispatcher. ONE review cycle per traincar - the worker schedules the policy-required round only after the LAST assigned WI commits, over the combined base..HEAD train diff (verdict named on the train head; intermediate constituents accepted-on-train, never per-WI reviewed; no constituent done until integration - the registry stays untouched on-branch). §7 continuation re-check before each successor: a POSITIVE classifier conflict (spine/gate/attestation/protected/high-risk/critique/checkpoint) ends the train early with new EXIT_TRAIN_END=10 (missing classification is not a newly-visible conflict - the dispatcher fails closed at packing; explicit assignments are dispatcher-authorized). Dispatcher: on a blocked or early-end exit, train_branch_evidence splits built/blocked/unstarted and release_reservations deletes the UNSTARTED refs in one update-ref --stdin transaction (built + blocked keep theirs as integrator evidence); the rescan is the traincar-DAG recompute; released dependents re-enter only when the durable disposition advances. Fork = packer never chains past multiple successors, children take separate lanes after (Slice-F-simulated) parent integration; join dispatches only when all parents done, its reservation base = the combined integration HEAD (asserted from the reservation metadata commit). Cap 4 bounds packing (5-chain -> 4-car + tail). tests/test_agent_loop_train.py (6 fixtures). SR-062/LLR-063/TC-063 Verified (autonomous single-agent adversarial review).
