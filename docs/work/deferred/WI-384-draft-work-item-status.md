+++
id = "WI-384"
title = "DESIGN DRAFT (docs/concurrency-v2.md §5) - do not claim until that doc is settled. Add a draft/ status directory for work items that are written down but not yet claimable. Today the vocabulary is queued|active|deferred|archive, so a design still under discussion has nowhere honest to live: deferred means parked-with-a-reason, which reads as a decision rather than as thinking in progress (these very rows are in deferred/ for exactly that lack). Real schema change, which is why it is a WI and not a casual edit: SPEC_STATUS_DIRS is duplicated across the three F5 readers (schedule.py, check_trajectory.py, agent_common.py) plus wi_convert.py and their tests, and the driver/scheduler must treat draft as never-ready. Open: whether the write-it-down-before-it-is-claimable need is recurring enough to earn the change - this session suggests it is, but one session is one data point."
workstream = "process"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "ordinary"
+++
