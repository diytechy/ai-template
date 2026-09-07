# Obligation allocation and proof

This map implements the existing RETURN judgment's design decisions. It does not
accept the cells or replace the fresh full-scope impact/absorption judgment.

| Obligation | Normative home | Actual verification / limit |
| --- | --- | --- |
| Intake triggers, high-water allocation including deletion non-reuse, context joins, approval-level arms | LLR-153 / TC-147 | Existing `tests/test_intake.py` and TC-158 allocation proofs retained. |
| Exact accepted scoped Status/snapshot effects, byte-equal live snapshot and complete absorbed-cell ledger | LLR-153 / TC-147 | `test_primary_approval.py` scope/unjudged, absorption and impact cases; `test_real_first_approval_snapshot_and_successor_are_one_commit`. |
| Exact queued-to-complete transformation, cleared SpecRef, fixed Deliverable before Context and derived link rebasing | LLR-153 / TC-147 | `test_real_primary_close_moves_exact_queued_spec`; complete-byte replay and malformed carrier refusals. |
| Successor specs, watermark, declared generated records, atomic transaction, crash and idempotent replay | LLR-153 / TC-147 | Existing real publication/replay fixtures plus `test_abrupt_publication_process_exit_preserves_one_completion`; process-loss boundaries on this box, explicit residue reconciliation before retry. |
| Held-slot lifetime, competing writer exclusion, scoped directives, pending precedence | LLR-154 / TC-148 | Existing primary-adjudication/station fixtures plus `test_primary_engine_holds_writer_exclusion_through_publication`; callbacks exercise actual engine/locks at admission, judgment, review and install. |
| Raw identity including undecodable paths; governing traversal; refresh-only reset peel | LLR-207 / TC-205 | Existing verdict-record and integration-station cases retained. Publication maps identity read-only and never becomes reset-disposable. |
| Exact verified primary-carrier recognition, wrong-turn/candidate/tree/receipt/author refusal | LLR-207 / TC-205, IF-180 | Shared completion proof; real-publication tests plus adversarial carriers and primary-session before/after identity assertion. Unknown/missing proof maps nothing. |
| Logged review joins, phase/count policy, trailer grammar and interpretation | LLR-207 / TC-205, IF-175 | Existing verdict-record suite retained; historical closed-lane fixtures remain labelled as such. |
| Primary dial, committing ADJUDICATE scheduling and shared queued/terminal input | LLR-207 / TC-205 | `test_pending_primary_review_dial_schedules_and_gates_real_publication`, complete never/when-minting/always × ordinary/spine/derived-dual matrix; independent fixture rounds serve owed phases. |

## Retained LLR-167 shape

LLR-167 is one validity decision over the primary brief assembled for the bound turn.
Splitting its independent refusal criteria into extra rows would repeat that same
validity contract rather than introduce independent authorities. TC-161 keeps distinct
verification purposes: selection/proposal binding (`test_primary_brief_refuses_an_unbound_turn_before_composing`);
strict field filling and failed versus blank assembly (unfillable/unknown/missing-data
cases); route bindings and shipped routing (`test_every_shipped_brief_is_routed_and_the_retired_one_is_gone`);
ordinary worker separation and generic primary assignment (`test_primary_blank_brief_renders_generic_schema_and_approval_carrier`);
report/census/cluster freshness (typed report, clean census and consolidation-digest
cases); and committed output correspondence (typed verdict and specialized-session
scope/rework cases). The existing real-CLI fixture tests remain fixture tests.
TC-161 now names the shipped all-routed contract and IF-075's reattestation seam.

## Retained counterparts

The reasons below carry the current RETURN's explicit decisions; fresh adjudication
must still accept meaning-changing uses by their own authority.

- SR-026 with LLR-061/TC-061: retain headless assignment and committed evidence
  reconciliation. Judge exact singleton and trailer-AND-spec-move completion together.
- SR-174 with LLR-153/TC-147 and LLR-154/TC-148: retain at-most-once allocation,
  deletion non-reuse and the high-water mark. IF-090 remains intake; IF-091 remains
  amendment-reader/admission, neither implicitly becomes a publication interface.
- SR-178 with LLR-158/TC-153: retain status-independent normative drift, including needs.
- LLR-159 with TC-154: retain stable partition and human holds.
- IF-075/IF-124 with TC-161: retain valid empty reattestation model and missing-anchor
  refusal, with no invented approved baseline.
- IF-175 Notes: separate authoring prerequisite; shared readers/bindings, phase span
  and distinct read-only/reset traversal remain; Drafted status and owner remain.
- IF-180: separately declared exact-publication query, Drafted with separate first
  approval. No IF status or approval snapshot is accepted by this source packet.

The retired two-row mechanical-close test remains absent. Nothing in this map claims
it passed or authorizes deletion of batch tests. The complete PC-BATCH-USES retirement
obligations, immutable history and all original absorption obligations remain owed.

TC-161 is Full: its cited test_adjudicate_brief module is explicitly in the
existing SLOW_MODULES set. This corrects a stale registry tier without changing
test membership. The stable full run preceded this declaration-only correction;
derived-state and final commit checks are rerun afterward.
