+++
id = "WI-357"
title = "The closing commit un-claims its own branch: §2.3 step 3 (move active/<branch>/ -> archive/) removes the directory §5.2's lane signal keys on (check.py _claimed_work_branch reads docs/work/active/<branch>/ ON DISK), so the trunk-freshness steps re-arm inside the very commit that closes the WI and demand generated artifacts the branch is forbidden to commit. Hit three times in the Phase 4 acceptance (both workers + the wi-346 reviewer); the working workaround - leave the emptied claim dir on disk untracked - depends on nobody running rmdir. The signal needs a source that survives the close: the branch's own history (its base commit claimed it), not the working tree."
workstream = "scripts"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-29 (the grind session; adversarially reviewed). The lane signal is two-stage in check.py `_claimed_work_branch`: the on-disk claim dir (fast path), else the branch's own committed history (`git log -1 -- docs/work/active/<branch>`), so the closing commit and its successors keep the freshness skip. Fail direction: no git / failing git / empty answer read as the TRUNK lane, because a false positive would disable the freshness gates where nothing else catches drift. Review-confirmed residual, accepted and recorded in the code comment: any branch name that ever appeared under docs/work/active/ reads claimed forever (relaxes a branch, never the trunk); trunk cost ~0.05 ms/commit, once per process. Tests: tests/test_check_lane.py (staged close, post-close commit, trunk with other branches' claims), non-vacuous against the pre-fix signal. Registry: SR-133/LLR-141/TC-134 state the obligation.
