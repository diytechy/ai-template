Reviewed: b700adb1f37f38c05a50ff443a85c800a89a16ec

### CRITIC — WI-987 plan — Round 1 — 2026-11-01

Fresh non-author session: Codex independent plan critic, invoked for coordinator leg 28, pcrit987. This session did not produce the plan. No provider session id was supplied. Read the actual Markdown artifact from the pinned commit; no image or description proxy was needed. No implementer session notes, status, log or neighboring plan critiques were read.

Rubric: docs/rubrics/plan-decomposition.md at b700adb1f37f38c05a50ff443a85c800a89a16ec, including its G5 reference to docs/rubrics/architecture-decomposition.md at that revision. Intent sources: docs/work/active/wi-987/WI-987-open-items-renders-owing-needs.md in full, its specref docs/specs/WI-987.md in full, docs/requirements/system-requirements.toml#SR-178 and its parent docs/requirements/stakeholder-needs.toml#SN-029, all at the reviewed revision; supplied D1–D6 coverage report.

Rubric derivation check: DevStg-Tests and B2 require substantive coverage of D1–D6, including SR-178's status-independent need-drift reporting and the scoped first-approval population; G5 tests the new detector dependency and interface population against A2/A3/A4/A6. These anchors independently reach the supplied intent rather than inheriting a permissive TC's expectations. No missing rubric anchor is needed.

Anchors judged: DevStg-Reqs, DevStg-Tests, DevStg-Impl, G4, G5, B1, B2, B3, B4. The rows have identifiable deliverables; the declared test/code/evidence splits explain the multi-coverage without duplicated implementation. The TC exclusions respect the unchanged detector and act boundaries. DELTA: within is supported: P3 adds the needs_owing input and P4 amends IF-126 and IF-074, while IF-075 and the detector remain unchanged. No new mode class or component boundary is required. The findings below concern honest D1 coverage and one missing artifact dependency.

Transfer caveat: the protocol's debate/selection evidence comes from QA, math and code with objective verifiers; plan quality and two-planner reconciliation remain unbenchmarked. This rubric is a supported extrapolation, not a proven instrument.

- [MAJOR] DevStg-Tests / B2 -> P1's `_full_cells_html(full)` explicitly retains `esc(tr.truncate_cell(...))`, and P3 uses that helper for first-approval need and stakeholder cards while claiming D1's cells-in-full coverage. At this revision `trace.truncate_cell` clips values at 1,500 characters. A supported first-approval workflow authoring a valid need or stakeholder with a longer prose cell therefore produces a clipped card rather than the full cells D1 requires; the registry has no corresponding 1,500-character authoring bound. P2's short fixtures do not expose that mismatch. -> Specify untruncated escaped cell text for the new first-approval cards, preserving existing SR rendering if necessary, and make T2 include a cell longer than the clipping limit with an assertion that its end appears. -> @implementer
- [MINOR] G4 / B4 -> The build table gives P5 only P3 as predecessor, although P5 explicitly consumes the final line position after P1, P3 and P4. P4 edits the gen_open_items module docstring above the `newline=chr(10)` site, so following the declared DAG can re-pin in P5 before P4 and invalidate that pin again in an otherwise supported build order. -> Add P4 to P5's predecessors (or move the final line re-pin into a step that depends on P4). -> @planner

VERDICT: CHANGES-REQUESTED findings=2
