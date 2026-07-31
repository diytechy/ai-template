+++
id = "WI-385"
title = "DESIGN DRAFT (docs/concurrency-v2.md A5) - do not claim until that doc is settled. Re-evaluate the backlog after a re-attest: warn when a queued WI cites an SR that was amended after the WI was filed. A verdict goes stale when the tree moves under it and the kit mechanizes that (integrate._verdict_gate); a WI's PREMISE goes stale when a cited SR is amended under it and the kit does not check that at all - SR-Refs is only ever tested for existence. If re-attest means scope changed, every open WI citing an amended SR may now be mis-scoped, redundant or obsolete, and today it will be claimed and built as though nothing happened. Cheap to detect with machinery that already exists: ratify_check and _verdict_gate both do git-derived is-X-older-than-Y comparisons, so compare a WI spec's last commit against the last CONTENT change of each SR it cites. WARN, never gate - a scope change means a human should re-read the WI, and gating would strand the whole backlog on every ratification. Fires as the final step of the dispatcher flow, after the spine batch merges and the owner ratifies, before ordinary dispatch resumes. DEPENDS ON WI-380: until the ratified-vs-traced cell split lands, this would fire on every WI whose cited SR was touched by a Module-pointer re-home - constant noise on WIs whose premise never changed, which is how a warn gets switched off."
workstream = "scripts"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "ordinary"
+++
