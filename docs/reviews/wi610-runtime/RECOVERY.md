# Pending primary-turn evidence recovery

The actual REVIEW-A session requested changes. The session engine wrote its
original invocation log, but its telemetry commit failed because the generated
verdict rollup was stale. This supervised record commit preserves the original
log and scoreboard bytes and regenerates the rollup through its owning writer.
No historical metadata or candidate binding is restamped. No approval trailer
is invented; the logged round files retain their own provenance and verdict.

The review's two MAJOR findings remain outstanding. The generic tripwire also
flagged the machine-written selection under docs/reviews/primary/: the reviewed
range starts at the pre-selection base, while impl_changed_paths excludes only
this train's review directory and iteration records. The exact flagged selection
was committed by primary_adjudication.begin before the author session. This is
a reader attribution defect, not evidence that a foreign review was edited.
The flag and actual scoreboard remain intact. The loop-held escalation calls
for a strong design check; that check must assess the required rework before
continuing. No source-code change or check suppression occurs in this recovery.

The turn remains selected, with its proposed zero-acceptance RETURN unpublished.
The tracked pause is unchanged. No control window, push or main merge.
