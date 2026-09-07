# Trace binding review — 2026-09-07

This is an implementation binding review, not a new semantic approval.  It
records the live registry anchor repair for LLR-140, LLR-152, LLR-153,
LLR-154, LLR-158, LLR-167 and LLR-207 after the branchless primary
adjudication split.

## Reviewed bytes

- Live registry: `docs/requirements/low-level-requirements.toml`
- SHA-256 at review: `4b2e08394d1773ea83cc4d8d729fd6247673af48aaaf2d399da20be7269b21f3`
- The reviewed edit changes only `module` and `code_symbol` in the seven
  named rows.  Detail, Status, SR refs, TC refs and all other row fields are
  outside this binding review.

## Binding dispositions

| Row | Live implementation anchors | Disposition |
| --- | --- | --- |
| LLR-140 | `integrate.py` claim/queue/integration/audit; `primary_adjudication.py` pending/begin/run/completion_refusal; `primary_publication.py` derive_tree/publish/publication_commit | Accepted as the split ownership of ordinary integration and the in-process primary carrier. |
| LLR-152 | `schedule.py` safety-kind constants; `primary_adjudication.py` begin/run; `primary_publication.py` derive_tree/publish | Accepted; the scheduling kind remains in schedule and its primary execution/projection anchors are live. |
| LLR-153 | `intake.py` mint/context helpers; `primary_approval.py` approval_projection/absorption_census/impact_census; `primary_publication.py` derive_tree/publish | Accepted; deleted `flip_verified` is removed and projection ownership is bound to the live approval/publication code. |
| LLR-154 | `integrate.py` merge/bar hooks; `primary_adjudication.py` run; `primary_publication.py` publish/publication_commit; `primary_close.py` stage_primary_adjudication | Accepted; branchless publication and close transformation have concrete anchors. |
| LLR-158 | `acceptance_record.py` staged-cell readers; `primary_approval.py` approval_projection/absorption_census/impact_census | Accepted; the approval comparison and impact census are anchored to their live carrier. |
| LLR-167 | `adjudicate_brief.py` compose/compose_primary/assembler values; `primary_adjudication.py` begin/run; `primary_turn.py` record_path/validate/validate_candidate; `kitlib/adjudication.py` verdict_text_refusal | Accepted; blank and specialized brief paths, turn validation, and refusal parsing resolve to actual callables. |
| LLR-207 | `kitlib/verdict.py` record/identity/round readers; `primary_turn.py` record/validation; `primary_approval.py` projection/censuses; `primary_publication.py` derive/publish/carrier; `primary_close.py` stage_primary_adjudication; `publication_verify.py` lower-bar helpers and adjudication surfaces | Accepted as implementation bindings. Deleted `mechanical_close_attestation` is removed; primary publication is represented as a verified carrier rather than a disposable verdict commit. |

The moved lower-bar helpers are owned by `publication_verify.py`:
`run`, `branch_tree_script`, `passed_steps`, `run_bar`, `generated_table`,
`generated_paths`, and `ADJUDICATION_SURFACES`. `primary_close.py` owns
`stage_primary_adjudication`; `handback.py` remains a compatibility re-export
surface. These are implementation facts and do not amend the governing
meaning of any row.

## Checks and limits

`./.venv/bin/python project-trajectory/scripts/trace.py --strict-integrity`
completed with `integrity=0`, `orphans=0`, and `component-findings=0`; the
existing advisory findings remain advisory. The focused trace and primary
runtime suites completed with 81 passed tests. This review does not approve a
WI, a registry cell value, a snapshot, or a semantic contract change; it only
records that the seven live Module/CodeSymbol carriers resolve to the current
implementation ownership.

## IF-123 physical endpoint repair

The strict trajectory scan found three new CMP-008 callers importing the
CMP-006 `baseline_snapshot` provider. The existing IF-123 contract already
covers the provider's whole read side and `copy_live` write side, so its
`requestors` list was extended to include the three actual callers. No IF
meaning, owner, status, identifier, or component was changed.

- `primary_adjudication` reads `SNAPSHOT_DIR` and uses the snapshot registry
  blob carrier while creating and validating a bound turn.
- `primary_turn` reads `SNAPSHOTTED`, `NEEDS_REL`, `SNAPSHOT_DIR`, and the
  approved snapshot blob set while constructing and validating immutable turn
  bindings.
- `primary_publication` calls `copy_live` for the approved projection and
  reads `SNAPSHOT_DIR` when deriving the allowed publication paths.

The resulting IF-123 requestors are `scripts/intake`,
`scripts/primary_adjudication`, `scripts/primary_publication`, and
`scripts/primary_turn`. The live interface file SHA-256 after this physical
endpoint update is
`81029c59e4eb6ae3044701c70725b9cbee76ed95a51fc217514d0298a838ae1e`.

`check_trajectory.py --root . --strict` now exits cleanly. It reports only
the repository's pre-existing warnings and no strict trajectory errors.
