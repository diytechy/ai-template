# P0a scenarios and historical train census

**Evidence revision:** `83f2c7aa990a757729e7847816d40a8cdc2afcc7` (`base83f2c7aa`). **Prepared:** 2026-09-06. This is read-only decision material. It does not authorize a pilot, unpause the loop, call a paid provider, alter a queue, or adopt one-WI cardinality.

## Reproducible scenario set

These scenarios use existing fake-provider or Real-Git fixtures. A passing test proves only its named observable. It does not prove operational cost, cross-platform behavior beyond the platform running it, or equivalence of a proposed replacement. P1/P5 must replay the applicable scenarios against both implementations before deleting the current path.

| Scenario | Existing reproduction | Required observable and durable evidence | Governed obligations | Known gap before replacement use |
|---|---|---|---|---|
| Ordinary work | `.venv/bin/python -m pytest -q tests/test_agent_loop_worker.py::test_worker_builds_assignment_and_exits_done tests/test_integrate_station.py::test_claim_build_and_integrate_end_to_end` | One ready row is claimed on a branch; a fake worker commits its WI trailer; refresh/check/attestation precede serialized integration; the terminal spec and Git history reconstruct the result. | SN-004/005/006/008/025/027; SR-026/028/049/148/151/152/156/170/174 | Does not measure queue wait, a real provider, or a populated non-Python adopter. |
| Spine amendment | `.venv/bin/python -m pytest -q tests/test_intake.py::test_a_approved_cell_diff_mints_one_adjudication_row tests/test_derive_stage.py::test_ONE_drafted_row_does_not_drop_the_effective_stage` | An approved-cell change creates one owed adjudication record; status/stage is derived from registry state and does not silently claim a lower or higher bar from one draft. | SN-002/004/008/029; SR-049/139/140/157/178/179/181 | Does not settle replacement for the snapshot-copy carrier; P1A still owes clause-level authority/freshness amendments. |
| Adjudication | `.venv/bin/python -m pytest -q tests/test_intake.py::test_under_attended_adjudication_recommends_and_never_flips tests/test_integrate_station.py::test_an_adjudication_lane_runs_no_bar` | Under human-held authority the tool recommends without changing Status; a pure adjudication lane follows its declared no-product-bar path; verdict and any later act remain separate records. | SN-004/008/024/029; SR-139/140/154/157 | Does not prove reviewer independence or a real decision’s semantic quality. |
| Consolidation | `.venv/bin/python -m pytest -q tests/test_consolidate_close.py::test_a_consolidate_verdict_absorbs_its_cluster_end_to_end` | One reviewed consolidation verdict absorbs exactly its declared cluster, preserves quoted Done-when text, rewrites dependencies, mints at most one successor, and leaves no half-applied queue mutation. | SN-008/012/025/029; SR-148/157/173/174 | This demonstrates the current mechanism, not that consolidation improves throughput or should survive P0c. |
| Human stop and handback | `.venv/bin/python -m pytest -q tests/test_dispatch.py::test_a_needs_human_worker_hands_back_and_the_run_keeps_going` | Typed NEEDS-HUMAN closes the affected lane through a terminal partial record while unrelated ready work may continue; no branch is hidden by renaming. | SN-006/008/029; SR-028/144/148/156 | The fixture does not judge whether the human stop was necessary or measure operator minutes. |
| Partial close | `.venv/bin/python -m pytest -q tests/test_handback.py::test_the_partial_close_lands_terminal_with_its_report_and_finishes_the_branch tests/test_handback.py::test_a_partial_close_is_CLEAN_under_the_real_trajectory_check` | The immutable report identifies keep/discard material, the spec lands in terminal `partial/`, and the real trajectory validator accepts the resulting lifecycle. | SN-006/008/027/029; SR-144/156/157/174 | Does not cover every sole-copy artifact or the open WI-581 quarantine/cleanup obligations. |
| Interrupted review | `.venv/bin/python -m pytest -q tests/test_dispatch.py::test_a_review_owed_worker_stays_parked_and_the_next_cycle_resumes_it tests/test_agent_loop_worker.py::test_worker_review_evidence_names_exact_reviewed_commit` | A worker owing review remains recoverable and is resumed before a fresh claim; review evidence names the exact reviewed tree. | SN-006/008/026/029; SR-028/154/156 | Does not yet inject process death between verdict-file write, telemetry commit, refresh, and promotion; P5 needs those crash points. |
| Adopter upgrade, including non-Python owner content | `.venv/bin/python -m pytest -q tests/test_old_kit_resync.py::test_old_kit_scaffold_syncs_forward_to_a_green_harness tests/test_old_kit_resync.py::test_node_adopter_upgrade_preserves_populated_owner_content` | A pinned old-kit scaffold moves forward, preserves populated Node/user-owned content, retains its adoption anchor, and runs the resulting declared harness. | SN-001/003/007/011/038/039; SR-007/010/011/034/035/036/111/114/129/163/164/166 | This is one historical range and one Node fixture. It does not establish all supported versions, Windows behavior, reverse migration, or post-cutover rollback. |

The scenario commands are selected nodes, so they can run without live agents. Their results should be recorded per revision when used as a replacement gate; merely importing their subject modules establishes no behavior.

The 14 selected nodes above were run together in this sitting against the shared workspace based on `83f2c7aa` after the authorized P0b footing edits: `14 passed in 18.31s`. This confirms that the named current fixtures execute and pass in that workspace. It is not a clean-tree rerun at the historical evidence revision, a full-suite result, or a replacement-equivalence result.

## WI-589 batch lane: record-derived census

The representative lane was claimed at `794de60d` as the ordered assignment `WI-589;WI-584;WI-587;WI-588`. The four completed specs and four legacy rollups remain in Git. The lane’s 11 tracked session logs are under `docs/iteration/wi-589-two-verified-defects-around-th-*`; the one mechanized review file is `docs/reviews/wi-589-two-verified-defects-around-th/011-REVIEW-A-6f27419.md`.

Reproduce the history and session figures with:

```sh
git log --all --reverse --format='%h%x09%s' \
  --ancestry-path 794de60d^..c5c4a8b3
.venv/bin/python - <<'PY'
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, 'project-trajectory/scripts')
import agent_common
logs = sorted(Path('docs/iteration').glob(
    'wi-589-two-verified-defects-around-th-*.log'))
meta = [agent_common.read_log_meta(p) for p in logs]
print('sessions', len(meta))
print('phase', Counter(m.get('phase') for m in meta))
print('outcome', Counter(m.get('outcome') for m in meta))
print('wall-secs', sum(int(m.get('wall-secs') or 0) for m in meta))
known = [m for m in meta if m.get('cost-usd')]
print('known-cost', len(known), sum(float(m['cost-usd']) for m in known))
print('known-token-rows', [m['tokens'] for m in meta if m.get('tokens')])
PY
```

At the evidence revision, the observable record is:

| Item | Observed record |
|---|---|
| Assignment size | 4 WIs on one exclusive spine lane |
| Sessions | 11 total: 10 BUILD, 1 REVIEW-A |
| Outcomes | 8 COMMITTED, 2 NO-COMMIT, 1 TIMEOUT |
| Per-WI build sessions | WI-589: 1; WI-584: 1; WI-587: 7; WI-588: 1 |
| Logged wall time | 15,815 seconds (4 h 23 m 35 s), including the 5,114-second timeout |
| Usage coverage | Tokens and cost present in only 3 of 11 logs: `132+44130`, `61+19029`, `122+32881`; known cost $13.2394445. The other eight invocations are unknown and no total-spend estimate is made. |
| Claim/review/integration | 1 batch claim; 1 mechanized cross-family review over combined tree `6f274193`; 1 eventual station integration at `c5c4a8b3` after refresh/repair work |
| Row evidence | Four distinct completion trailers: WI-584 `9c8b3ce2`, WI-587 `91642f95`, WI-588 `6f274193`, WI-589 `836ccd94` |
| Supervisor/recovery record | Tracked pause after the batch condition; a timeout; partial-close commit `b0be72c7`; supervisor-recorded verdict `4366b19b`; close of stranded WI-589 after the reviewed tree; legacy rollups; a further pause; hand refresh; four batch-lane machinery fixes at `f4ca1bd5`; then refresh and integration |
| Post-merge assurance | Separate follow-up/adjudication/spot-check work was minted. WI-590 treated LLR-207/TC-205 separately from LLR-208/TC-206; WI-591 spot-checked WI-584; WI-592 spot-checked WI-588. These are distinct acceptance purposes, not a continuation of one shared deliverable. |

The record does not support a clean “one batch saved three reviews” claim. It shows one mechanized review, but also a supervisor-drawn/recorded verdict path, legacy rollups per row, recovery commits, and later per-purpose adjudication and spot checks. It also does not show that every later turn was caused by cardinality: the full-suite red and some approval work had independent causes.

## Shared acceptance versus separate deliverables

| WI | Deliverable and authority | Can ship independently? | Shared acceptance finding |
|---|---|---|---|
| WI-584 | Rules and implements snapshot refusal scope. It changes approval-act behavior but no spine cell. | Yes. Its ruling and tests do not require the verdict-row corrections or review-span cleanup. | No joint atomicity requirement with the other three is recorded. |
| WI-587 | Corrects LLR-207/TC-205 text and adds two verdict-record detectors; leaves those rows Drafted for later adjudication. | Yes, though LLR-207 and TC-205 belong together as requirement/test halves of one gap. | Shares provenance with WI-588’s RETURN, but later WI-590 accepted/returned the pairs separately. That is evidence against four-row joint acceptance. |
| WI-588 | Corrects LLR-208/TC-206 around trunk regeneration/exclusive writer and leaves approval to a later act. | Yes. Later adjudication approved this pair while returning LLR-207/TC-205. | No joint acceptance atomicity with WI-587 was required in practice. |
| WI-589 | Removes a duplicate review-phase definition and declares the missing IF-175 requestor. | Yes. It is related to the verdict surface but is a separate implementation/interface defect. | The row’s spec close after round 011 changed the non-record tree and triggered the legacy rollup path; sharing a lane created coupling without a shared approval clause. |

Round 011 was one acceptance decision over the combined implementation tree. It does not turn the four specs into one deliverable. The specs have separate Done-when scopes, completion trailers, later assurance paths, and in WI-587/WI-588’s case demonstrably separable adjudication outcomes.

## Cardinality alternatives and turn accounting

Counts below use observable process turns: claim/admission, BUILD sessions, review sessions, integration, and post-merge intake. They do not equate a Git bookkeeping commit with a model turn. Counterfactual counts are minimum structural counts, not measured duration or spend.

| Shape | Claim/admission | BUILD | Review | Integration | Post-merge intake | Evidence-based assessment |
|---|---:|---:|---:|---:|---:|---|
| Actual four-WI batch | 1 | 10 | 1 mechanized | 1 eventual | 1 batch merge intake | 14 nominal turns before counting supervisor recovery. The history adds pause/resume, partial close, verdict recording/rollups, repair and refresh work. |
| One consolidated WI containing all four | 1 | Unknown; 10 only if observed effort transferred unchanged | 1 minimum | 1 | 1 | Operationally compact, but incoherent: it joins an unrelated snapshot ruling, two separately adjudicable row/test pairs, and a review-span/interface defect. No record supports one acceptance authority for that union. |
| Four separate exclusive WIs | 4 | At least the observed 10 only as a comparison floor, not a prediction | 4 minimum under one-round policy | 4 | 4 | 26 nominal turns at the observed build count. It adds 3 reviews, 3 integrations, 3 intake turns and 3 claims, while removing batch-only shared close/recovery coupling. Actual duration is unknown because this alternative was not run. |
| Three WIs, combining WI-587+WI-588 | 3 | Unknown | 3 minimum | 3 | 3 | 22 nominal turns at the same comparison floor. Their common RETURN provenance makes this the strongest consolidation candidate, but WI-590’s split outcome shows they did not require atomic acceptance; separate exclusive WIs remain the safer proposal. |

**Proposed classification:** preserve exclusive serialization for each spine-affecting WI, but do not treat exclusivity as joint approval. For this historical set, four separate WIs best match the recorded deliverables. A future consolidation should combine only clauses that one reviewer can accept or return as one coherent result. This is a proposal for the P0c cardinality decision; current approved batch behavior remains governing until that decision and its amendments land.

## Evidence still required

1. Re-run the selected scenario set at each named replacement candidate and at its clean comparison revision. This sitting’s shared-workspace result does not establish old/new equivalence.
2. Add P5 crash injections between verdict write, telemetry persistence, refresh attestation, promotion, intake and cleanup. Current interrupted-review tests do not cover every boundary.
3. Establish supported upgrade start/end versions and run the non-Python fixture on the supported OS matrix. One Node fixture and one local platform are insufficient.
4. Measure real operator interventions with reason codes. Git commits reveal intervention events but not elapsed human effort.
5. Fill provider usage coverage before cost comparisons. Eight of the eleven historical train sessions have no token/cost accounting.
6. Predeclare matched workload and thresholds before any control window. This historical train is a cautionary case, not a statistically valid retain/replace baseline.
7. Decide the snapshot carrier, batch cardinality and interface-contract amendments through their normal authority. No classification or counterfactual above changes an Approved row.
