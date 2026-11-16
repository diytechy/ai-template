## 2026-11-16 — OI-130 ruled (attended, maintenance branch)

- **OI-130 Q1 (b):** the operator accepts P5 as the depth-0 component
  partition, on the re-score of 2026-11-11
  ([record](../plans/2026-11-11-oi130-rescore/README.md)). The operator: "I
  have not looked in some time, but given the evidence is for P5 I approve."
  This closes decision 10 of 2026-08-13, which had deferred the approval to
  re-derived numbers that nobody then derived.
- **Q2:** the record declares OI-14's objective as ruled, "minimize cut", with
  the one-home-per-behaviour constraint violated by every candidate. On
  today's scores (P5 140, P3 152, P4 235) P5 ranks first, so the record
  carries no override. Neither of the item's filed options said this; both
  were written against August's numbers.
- **The record's shape:** SR-165 as written, and WI-999 builds it. The
  operator: "If any optionality, build as opt-out configurable (on by
  default), but I believe without it tracability becomes incomplete." The
  existing `[checks] components_check` dial is that switch; no setting is
  added.
- **Why it stayed open:** the question changed three times before it could be
  answered: a deferral in August, an approval of the component rows whose
  scope the log left unclear, an item filed on August's numbers, and then a
  re-score that made the filed options moot.
- WI-999 drops its `needs` on the item and its Done-when names the record's
  cells. WI-1001 still follows WI-999.
