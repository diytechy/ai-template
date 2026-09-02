## 2026-09-02 — WI-572 independent review

- [MAJOR] project-trajectory/scripts/acceptance_record.py:595 -> an `Approved` → `Drafted` status-only withdrawal is deliberately omitted from `staged_drafted_rows`, so `intake_after_merge` mints no first-approval adjudication even though `trace.reattest_model` reports the row as awaiting `approve`; the released row is silently stranded with no actor able to perform its required re-approval -> classify every transition into `Drafted` in the shared two-tree reader and feed it to the first-approval trigger (while retaining the existing no-refusal rule for de-approval) -> @owner

VERDICT: CHANGES-REQUESTED findings=1
