+++
id = "WI-439"
title = "OI-27's three do-not-wait defects, taken ahead of the re-sync pack: (1) the tarball adopter path stamps an anchorless `unknown (kit not a git checkout)` silently at exit 0 — add the loud warning the -dirty path already has; (2) the downstream-resync skill's hand-maintained WI-381 recipe duplicates ADOPTING section 6 and has drifted — point, do not restate (through the materializer, never three hand edits); (3) zero tests re-sync from an old kit state — build the first old-kit test: scaffold at an older kit commit, sync forward, harness green. That third test is what makes any re-sync method's claims evidence rather than prose, and it is owed under every option OI-27 weighed."
specref = "docs/requirements/open-items.toml"
workstream = "lock-program"
sr_refs = ["SR-036", "SR-111"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++
