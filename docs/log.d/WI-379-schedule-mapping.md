## 2026-07-31 — WI-379: a fresh scaffold could not claim work

**One line:** `bootstrap.py`'s MAPPING omitted `scripts/schedule.py`, which
`integrate.py` and `drive.py` import **unguarded**, so every newly
bootstrapped repo raised `ModuleNotFoundError` the first time it tried to
claim a work item — the integration seam and the walk-away loop, both dead
on arrival.

**How it was found — and why nothing else could have found it.** The gilbert
re-sync surfaced it. The bug is invisible three ways over: the kit's own
`scripts/` directory holds every file, so nothing here fails; an
already-adopted repo carries `schedule.py` from an older kit, so no re-sync
fails (gilbert's did not); and the two importers are the *newest* surfaces,
so no historical run covered them. Only a **fresh scaffold probe** reaches
it, and this session ran one.

**Driven, not inferred.** Bootstrapped a scaffold with `bootstrap.py --dest`,
dropped in one queued spec, ran `integrate.py claim`:

```
File ".../scripts/integrate.py", line 257, in _claim_refusal
    import schedule  # sibling; deferred so the cheap refusals above stay cheap
ModuleNotFoundError: No module named 'schedule'
```

After the fix, the identical probe answers
`integrate: claimed WI-001 on probe (trunk commit + branch cut)`.

**Scope, established by audit rather than assumed.** An AST sweep of every
MAPPED script's sibling imports against the MAPPING found `schedule` to be
the **only** omission. Counted by parsing the MAPPING literal itself:
**43 mapped before this fix, 44 after**, against **46** kit scripts on disk —
and the two that remain unmapped are `bootstrap` itself and
`gen_skills_index`, kit-only by design (it generates the kit's own
`INDEX.csv` from a neutral `skills/` source a scaffold never receives, and
`check.py` already branches to a vacuous no-op downstream). 44 + 2 = 46.

**Deliverables.** The MAPPING row (with the reason stated at the row, so the
next reader knows it is load-bearing rather than a nicety), the
`tests/test_bootstrap.py` scaffold file-list entry, and the
`project-trajectory/README.md` kit-contents row.

**The class fix, which is the durable part.**
`test_every_sibling_imported_module_is_shipped_by_mapping` parses the MAPPING literal via ast (not a whole-file regex, which would also match script names in prose and mark an unmapped module as mapped) and walks the AST of
every shipped script and asserts each kit-module it imports is itself
mapped. **Mutation-proven**: run against the pre-fix `bootstrap.py` (taken
from git history, not a hand-edit) it reports exactly
`{'schedule': ['agent_loop.py', 'drive.py', 'integrate.py', 'traj_parse.py']}`.
This matters more than the one-line fix: WI-280 alone added six sibling
modules this session, and the next extraction that forgets its MAPPING row
now fails here instead of in an adopter's repo.

**Downstream note:** an adopting repo that already carries `schedule.py`
needs no action; a repo scaffolded from a kit between the drive-loop
landing and this fix should copy `scripts/schedule.py` across.

**Ratchet re-stamp:** `bootstrap.py` 2224 -> 2232 (+8) — the MAPPING row plus the comment stating why it is load-bearing. Required registration, the same shape as the trunk_step/integrate/drive rows, not monolith growth.

**Bars:** the new test and the scaffold file-list test pass; `ruff check`
and `ruff format` clean; commit bar green except the standing work-branch
red.
