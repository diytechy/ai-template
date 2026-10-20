Reviewed: dd9b23f7272c83fbe748b81b815a72f148c6005d

### INDEPENDENT PLAN CRITIC — Plan decomposition — Round 2 — 2026-10-20

Fresh non-author session: this invocation of Codex as the independent critic, launched through the coordinator review route. No provider session id was supplied. Reviewed the committed artifact directly; no earlier verdict, decision record, implementer session notes, status, or project log was opened. Revision-history assertions embedded in the required plan/spec were not treated as review evidence.

Rubric: `docs/rubrics/plan-decomposition.md`, revision at dd9b23f7272c83fbe748b81b815a72f148c6005d, matching the supplied rubric; second and final critique in convergence stance.

Intent sources: the full `docs/work/active/wi-902/WI-902-disposition-adopts-existing-successor.md` at the reviewed commit; its specref `docs/plans/2026-10-11-review-churn/README.md#2-record-the-decision-at-its-event-checked-at-the-commit`; SR-148 and SR-220 in `docs/requirements/system-requirements.toml`, and their SN-006/SN-008/SN-010/SN-025/SN-027/SN-029 parent intent in `docs/requirements/stakeholder-needs.toml`. The supplied coverage report was used as the mechanical clause index.

Rubric derivation check: adequate for this plan judgment. DevStg-Tests and B2 independently require substantive coverage of the actual Done-when, including the validated event record and successor discharge, rather than merely counting cited TCs. DevStg-Reqs, DevStg-Impl, G4 and B1/B3/B4 cover solvability, seams and build order. No additional failure-class anchor is needed for the finding below.

Anchors judged: DevStg-Reqs, DevStg-Tests, DevStg-Impl, G4, B1, B2, B3, B4. P1-P9 identify concrete deliverables and checks. The declared multi-coverage splits are meaningful producer/consumer or build/adjudication seams; the excluded work-selection and absorption tests have reasons consistent with the stated unchanged behavior. P10-P12 carry iteration, checkpoint and landing in buildable order. DELTA: within is supported: the new cell and grammar value, new record-dependent outputs, validation owner and per-commit/staged consumers are carried without a new external boundary. Complete coverage fails at the specific supported close described below.

Transfer caveat: the debate/selection evidence behind this protocol comes from QA, math and code with objective verifiers; it does not benchmark plan artifacts. Applying it here is the rubric's best-supported extrapolation, not a proven instrument.

Findings:
- [MAJOR] DevStg-Tests / B2 -> P5, “What it judges” and “A residual stated, not built against,” plus the matching final risk: the proposed record check accepts a close only when `mechanical_close_attestation` accepts it, although that attestor deliberately refuses any close touching a path outside `docs/work/`. The supported close calls `spec_move.move_spec`, whose inbound-link traversal rewrites and stages Markdown links throughout the repository. Thus an otherwise valid adopting disposition with an inbound link in, for example, a plan or a log fragment produces a genuine machinery close that this new rider rejects at integration. This is a reachable D1 gap, not merely a request for broader peel coverage: the attestor previously declining to peel only required review, whereas P5 turns the same case into a record-admission refusal. P5's proposed “a person re-closes it” supplies no valid route, since hand closes are expressly rejected by P5 and forbidden by P7. -> Give record admission a close-verification rule that admits the machinery's supported exact inbound relinks while retaining record/request and parent-tree validation; it need not broaden review peeling. Add a real-close regression with an inbound link outside `docs/work/`, and demonstrate that its record passes the lane rider and squash hook while a hand-written record still fails. -> @WI-902-implementer

VERDICT: CHANGES-REQUESTED findings=1
