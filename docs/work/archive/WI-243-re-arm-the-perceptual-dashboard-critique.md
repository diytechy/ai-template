+++
id = "WI-243"
title = "Re-arm the perceptual dashboard critique - re-fire the SR-052/053/054 critique on render-surface diffs + feed the critic rendered pixels (2026-07-20 quality-gap review)"
workstream = "quality"
sr_refs = ["SR-047", "SR-054"]
buildtier = "strong"
safety_class = "high-risk"
order = 240
+++

## Deliverable

Perceptual critique RE-ARMED + FAIL-CLOSED (owner ruling 2026-07-20). Two parts: (1) the 3 Verification=Critique TCs (TC-053/054/055) name shoot.mjs PNG matrix as the artifact recipe so the critic judges pixels not ~790KB markup; (2) critique_staleness_findings in check_trajectory.py compares git commit-time of the render surface (__file__-co-located gen_trajectory.py + meta-only shoot.mjs) vs the latest docs/reviews/*-CRITIQUE.md - when the surface is newer, a finding routed through main s strict-promotable loop (run-state precedent): WARN at the commit bar, ERROR under --strict (check.py adds --strict at G2/G3, NOT the pre-commit floor) so a stale render surface CANNOT reach a green G3 gate (agent-proof) while a plain commit stays warn-first; main C901 21 held. Downstream-safe: vacuous without a Verification=Critique SR (none ship, grep-verified), render surface = kit script + meta-only shoot.mjs, opt-out via docs/trajectory-check - so fail-closed is a this-repo gate decision not a downstream migration. PROVEN END-TO-END: warn fired -> owner-directed render critique (075 confirmed the Knowledge tab hard-to-read + WI-159 deferred) -> WI-159 built+DONE (tab fixed) -> 076 re-judged -> warn cleared; lands green now (--strict exit 0), reddens on the NEXT render change. REVIEW-A: CHANGES-REQUESTED f=5 (MAJOR=the owner gate-strength ruling + 4 MINOR consumed 446d5ca); fail-closed REVIEW-A APPROVE f=1 (1 MINOR = a PRE-EXISTING no-work-items early-return fail-open boundary shared by ALL trajectory findings, degenerate/out-of-scope, ACCEPTED - fixing only perceptual would be inconsistent). Builds c900cf1 + 446d5ca + f26efbf; full suite 1235p/4s, check_trajectory --strict exit 0 @ G3.
