# 097-REVIEW-A — WI-172 retrospective review of WI-169 + WI-170

Fresh-context retrospective review of commits `e544ae1` (WI-169) and `cef63a1`
(WI-170), required because both builds landed during review-exempt DESIGN-CHECK
sessions and therefore missed the declared `review-policy=1` round.

## WI-169 — process-loop racetrack scope

The change narrows the racetrack border and return-arrow selectors from the
shared `.loop` class to wrapper `div.loop`, preventing the nested `ol.loop`
from drawing duplicate tracks. The structural regression checks both the
positive wrapper selectors and absence of the broad selectors. Removing the
tautological degree attributes is paired with a TC-056 acceptance update that
states the observable shared-grid structure. Generated dashboard and status
bookkeeping are consistent with the implementation. No finding.

## WI-170 — requested-change scope carry-forward

The coordinator reads a durable `docs/rework-wi` override ahead of
`docs/next-wi` for prompt labeling and BuildTier lookup, writes it after a
CHANGES-REQUESTED review, and clears it only when the same scope approves. The
integration test exercises the failure mode end to end: the BUILD advances the
queue, review requests changes, the next run rebuilds the old scope, approval
clears the override, and the advanced queue remains intact. The opt-in process
text describes the same precedence and lifecycle; the watched byte baseline
was restamped consistently in all three skill copies. No finding.

## Review conclusion

Both diffs are scoped to their recorded WIs, preserve the absent-override path,
and carry tests at the behavior seams that motivated them. `git show --check`
is clean for both commits. No additional WI is required.

VERDICT: APPROVE findings=0
