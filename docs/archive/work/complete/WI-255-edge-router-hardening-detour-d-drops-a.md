+++
id = "WI-255"
title = "Edge-router hardening: _detour_d drops a box overlapping the port-stub corridor (within the 18px stub) from the lane search, silently keeping the through-box direct cubic - fail-open that holds on current data only (16px column gaps already exist); re-verify the full routed polyline clears all obstacles. Also anchor a detoured sw_graph edge label to its routed lane instead of the straight-chord midpoint (label floats off the wire, T4 downstream). Render surface: build re-fires the WI-243 gate - bundle a fresh critique (110-REVIEW-A MINORs 1+3)"
workstream = "dashboard"
sr_refs = ["SR-052", "SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 252
+++

## Deliverable

Full routed-polyline obstacle re-verification: _clear_lane_y generalized to _lane_candidates (nearest-midline first, first fully-clear lane wins, deterministic least-obstructed fallback when none clears - terminates, 200 dict-order shuffles = 1 output) with _detour_points/_detour_str sharing one curve between hit-test and emitted d; the 110-REVIEW-A stub-corridor scenario now detours (reconstructed pre-fix code = through-box, so the new bite-proof goes red on revert). Detoured sw_graph labels anchored to the routed lane midpoint via _routed_label_xy (driven: 26/65 real detoured swedges label-on-lane; straight labels chord-midpoint byte-identical). Meta render byte-identical except the as-of stamp (111-REVIEW-A cross-commit diff = exactly 1 line). Opus build 3e0fc24; 111-REVIEW-A APPROVE f=2 both MINOR (outboard-stub span residual - 13/3000 synthetic, 0 on every real panel; dense-overlap perf - no live impact on tiered geometry; both filed as WI-257); 080-CRITIQUE APPROVE f=0.
