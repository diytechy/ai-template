# WI-568 adjudication — WI-508 architectural-remap close

The lane's `partial` claim stands. The architectural derivation, alignment
survey, and consolidation filings survive, while the final record honestly
leaves `TC-199`/`TC-200` Drafted and still owes a clean review on current trunk
plus an authoritative disposition of the approval baseline. The one successor
is drafted in this session's own spec under `## Dispositions`; it carries
`supersedes = "WI-508"`, `buildtier = "strong"`, and `planmode = "single"`.

## Findings

- [MINOR] the claimed outcome is correctly PARTIAL -> the range delivered the blind derivation, alignment survey, and consolidation rows, but its final reviewed state deliberately leaves `TC-199`/`TC-200` Drafted and does not land the fresh current-tree reviewer round named by the handback -> retain the partial close and carry only the remaining reseal work into the drafted successor -> @owner
- [BLOCKER] the report's `keep_commits = []` / `discard_commits = []` is a missing keep/discard split -> a partial close cannot leave the already-landed range unjudged, especially where `580df781` contains both the surviving `LLR-203`/`LLR-204` approvals and snapshot movement while later commits correct the TC over-claim -> record KEEP all commits in `ff29fef8f9..6ba2711078`, including the explicit LLR approvals and the later TC corrections, DISCARD none; any owner-directed baseline restoration is a successor correction rather than rejected code silently left on trunk -> @owner
- [MAJOR] a successor is mandatory and exactly one is drafted in WI-568's own `## Dispositions` section -> the terminal WI-508 row cannot be revived, while a clean current-tree review of `LLR-203`/`LLR-204` and Drafted `TC-199`/`TC-200`, the approval-baseline disposition, and the two preserved blind-derivation caveats remain executable work -> mint that `supersedes = "WI-508"` successor at this adjudication's close with `buildtier = "strong"` and `planmode = "single"` -> @owner
- [MAJOR] the off-spine `docs/archive/last_approved/` baseline disposition is human-owed -> the range moved the snapshot while the handback requires regeneration at the successor's own approval act, and deciding whether the absorbed baseline stands or is restored changes what the approval surface asks a human to attest -> mint the successor's `open_item` as a pending typed dependency and keep the successor waiting until the owner rules STAND or RESTORE; then execute the corresponding branch already stated in the disposition scope -> @owner

OUTCOME: PARTIAL successors=1
