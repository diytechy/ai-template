## 2026-10-15 (f) — attended coordinator: the hook-floor row through its checkpoint; the store-lock row claimed, planned and built

The ninth attended coordinator session under the review-churn program
(handoff-2026-10-15e-attended-coordinator). It took the hook-floor row from
its open round-2 finding through its last counted round and its checkpoint,
fixed the process-text row's last shipped-text MINORs, and claimed the
store-lock row and took it through its plan gate and first build round.

- **WI-921 (the hook floor):** the builder confirmed 004 F1 (an amend is
  judged against HEAD, not its real parent) in both shapes, found no amend
  signal at pre-commit, and costed the exact boundary, git's
  reference-transaction hook (about 300 lines, a new shipped hook, a git
  2.28 floor, side effects under `--no-verify`). The finding is fail-open,
  so neither the coordinator nor a sitting could defer it; the owner ruled
  it a successor row (D-014), and the spec's Trust section states the
  residue. Round 3, the last counted, in convergence stance: no
  round-costing code finding (D-016); Opus's merge-commit route joined the
  residue. The lane rebased onto trunk's tip. The checkpoint: Terra's
  reconcile returned SR-156 to its approved text; sitting 010 was composed
  single-kind by the coordinator and came back with a section the one
  verdict parser refuses, after its act was committed, so it was discarded
  and archived and the lane rewound (D-018); the returns were reworked, and
  combined sitting 011 blessed all five rows, with its act re-attesting
  LLR-019, LLR-307, LLR-309, TC-019 and TC-325.
- **WI-911 (B1's text):** the text fix after round 3 (`d9376ea14`, D-014):
  the convergence command prints no commit message, and the lane's shipped
  comments cite no review records. The triage was narrowed to the two
  findings' own remedies, so WI ids and dated rulings stay.
- **WI-923 (the store lock):** claimed under one scoped unpause
  (`c11eb456b`, `7848b6c62`, `4c216fd2f`). A fresh Opus planner's plan
  passed the coverage gate; Sol's critique had one MINOR, so the pass record
  followed (`61c6d2afa`). Build round 1 (`a62cdb456`): an access-denied lock
  create reads as held, is retried, and past the wait is refused as busy
  naming the cause; three red-first tests failed on trunk's code with the
  crash, and the builder's stress run saw 143 escapes on trunk's code and
  none on the change.
- **The trial,** WI-921 round 3: round-costing 0 each; MINORs Sol 0,
  Fable 3, Opus 4.
- **Lessons folded into the recipes:** a checkpoint sitting is always
  combined; read a finding's own remedy before a broader disposition; a
  fail-open finding whose fix is a new boundary goes to the owner, and a
  successor ruling lives in the Trust section; builders' comments never cite
  review rounds; name a lane's unapproved sentences to Terra, and define a
  sibling row's borrowed term.
