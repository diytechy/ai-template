+++
id = "WI-383"
title = "DESIGN DRAFT (docs/concurrency-v2.md §1 and §4) - do not claim until that doc is settled. Fix the driver/dispatcher vocabulary in the process text and rule on the vestigial grouping plumbing. Driver = sequencing WITHIN one lane (drive.py, exists); dispatcher = allocation ACROSS lanes (does not exist, deleted with the v4 dispatcher at Phase 5). The 2026-07-31 session's confusion came from collapsing the two, and the owner's mental model was still the retired jobs=1 worker ceiling. Separately: session grouping is half-alive and misleading - schedule.py still classifies for optimistic multi-WI packing, agent_loop --wi still accepts 'WI-201;WI-204', and the section 7 continuation guard still ends an assignment early, but NOTHING packs. Capability that looks present and is not is the worst of the three states: either wire it or formally mark it dormant. Open: whether driver and dispatcher stay separate modules, and whether session grouping is wanted at all once drain grouping (WI-382) exists."
workstream = "process"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "ordinary"
+++
