+++
id = "WI-832"
title = "A decisions record has an identity no other run can share"
workstream = "process"
specref = "docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md"
needs = ["OI-107"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the wave-16 coordinator on 2026-10-05, as the queued placeholder
that puts OI-107 on the owner's surface: an open item is filed together with the
queued row that cites it. The independent adjudicator's finding F1 at WI-818
(`docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md`) found that a run's
decisions record is named by a lossy, reusable branch name.

OI-107 was ruled on 2026-10-07: (b) now, with a decision watermark as the
owner's cleaner, deferred option. Its Done-when follows.

## Done-when

- OI-107 ruled 2026-10-07 (b): a run's decisions record is named by the work
  item it records, never by its branch name, so two runs never share a record.
- A decision not tied to a work item (a coordinator's call on trunk) takes the
  next number above the highest existing non-work-item decision. Trunk is
  serial, so taking the highest is safe there.
- Existing records move once. A RESYNC entry carries the migration (forced for
  adopters with slash-named branches), and every citation of a moved record
  (`docs/decisions/<run>.toml#D-NNN`) in work items and logs is rewritten in the
  same commit.
- Deferred, not this row: a decision watermark, one decision id space in
  `docs/id-watermark`, so a decision id is unique across every record.
- SR-225's rows state the naming and pass in-lane adjudication.
