+++
id = "WI-553"
title = "The hold ban mechanized: claim-ref check, blocked_pending retired, fragment declaration cross-checked (OI-70)"
specref = "docs/requirements/open-items.toml#OI-70"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

`OI-70`'s ruling bans the hold-by-rename outright — a lane must close or it
gets lost, as the wi508 lane nearly was — and the owner endorsed the
mechanization: a claim directory must have a matching branch ref. That
mismatch (spec in `active/`, no ref) is the rename-hold's exact signature and
the same scheduler/dispatcher disagreement `docs/handoff-2026-08-31.md` §2
names as the phantom head. Two dead surfaces ride with the ruling:
`pending.blocked_pending` reads `queued/` rows carrying a `blockref` and
NOTHING produces one any more (`LLR-161` removed the producers), and
`gen_open_items.py --check` verifies a fragment DECLARES its deferred open
items without checking the declaration is true.

## Done-when

1. A check (harness-run, warn-or-gate per the declared policy) reports every
   `docs/work/active/<branch>/` claim directory with no matching branch ref —
   driven on a scaffold both ways (matching ref: silent; renamed ref: named).
2. `pending.blocked_pending` and the `blockref` vocabulary are retired or
   re-pointed — the owner surface keeps no source with zero producers; the
   `-000` example row and any doc teaching `blockref` follow in the same
   slice.
3. The fragment deferred-open-items declaration is cross-checked against the
   registry (a fragment claiming `none` while it should have deferred a row
   is contradicted), not merely presence-checked.
4. The ban is stated where supervisors read: the session-protocol skill and
   the handback/ADJUDICATE docs name the sanctioned stop (the partial close;
   nothing else) and cite `OI-70` as the ruling of record.
