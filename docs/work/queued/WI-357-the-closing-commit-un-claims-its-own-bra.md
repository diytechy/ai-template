+++
id = "WI-357"
title = "The closing commit un-claims its own branch: §2.3 step 3 (move active/<branch>/ -> archive/) removes the directory §5.2's lane signal keys on (check.py _claimed_work_branch reads docs/work/active/<branch>/ ON DISK), so the trunk-freshness steps re-arm inside the very commit that closes the WI and demand generated artifacts the branch is forbidden to commit. Hit three times in the Phase 4 acceptance (both workers + the wi-346 reviewer); the working workaround - leave the emptied claim dir on disk untracked - depends on nobody running rmdir. The signal needs a source that survives the close: the branch's own history (its base commit claimed it), not the working tree."
workstream = "scripts"
specref = "docs/log.md"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
+++
