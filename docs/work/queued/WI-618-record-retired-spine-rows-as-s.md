+++
id = "WI-618"
title = "Record retired spine rows as structured fragments in docs/log.d/retired/, amending D-4 (S4)"
workstream = "scripts"
specref = "docs/repo-lock.md#d-4--supersession-is-deletion-and-ids-are-never-reused"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Context

Ruled by the owner 2026-09-23 on a condition: fragments are for lookup, not
browsing, stated in PROCESS.md and not in AGENTS (sister plan S4, §1.4). The home
was revised 2026-09-24 to `docs/log.d/retired/`, because `trunk_step.py` folds
and deletes every top-level `docs/log.d/*.md` and its glob does not recurse.

D-4 says a superseded row is deleted and its history lives in git and the log;
a structured record is a third home, so this is an amendment. The shape: id,
date, successor if any, reason, written in the same commit as the deletion. No
self-referential hash: the dashboard resolves the deleting commit from git at
render time and shows *unknown* in a shallow or squashed clone. Append-only by
check, warn-first: a fragment edited after it lands, and a spent id with no
fragment from the day the rule starts.

## Done-when

- D-4 in `docs/repo-lock.md` names the retirement fragments as the structured
  home.
- A deletion writes its fragment under `docs/log.d/retired/` in the same
  commit, and a test drives `trunk_step.py --compile-log` over one and shows it
  stays.
- The two warn-first checks and the dashboard renderer exist; the template
  gains the `orphans-allow` line and `RESYNC_PACK.md` an entry.
- PROCESS.md says the fragments are for lookup, not browsing.
