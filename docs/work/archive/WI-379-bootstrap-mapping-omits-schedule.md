+++
id = "WI-379"
title = "bootstrap.py's MAPPING omits scripts/schedule.py, so the integration seam is BROKEN ON EVERY FRESH SCAFFOLD. Four shipped modules import it - integrate.py:257 and drive.py:47 UNGUARDED, agent_loop.py and traj_parse.py guarded - and a MAPPING audit confirms it is the only such omission (gen_skills_index is deliberately kit-only). PROVEN 2026-07-31, not inferred: bootstrapped a scaffold with bootstrap.py --dest, added one queued spec, ran `integrate.py claim` and got `ModuleNotFoundError: No module named 'schedule'` from _claim_refusal's frontier check. So a newly scaffolded repo cannot claim work, and a plain agent-resume launch (the WI-374 drive loop) cannot run either - the two headline capabilities of the whole integration seam. Invisible upstream because the kit's own scripts/ dir holds every file, and invisible to the gilbert re-sync because that repo already carried schedule.py from an older kit; only a fresh-scaffold probe reaches it. Fix: the MAPPING row + tests/test_bootstrap.py scaffold file list + the project-trajectory/README.md kit-contents row. ALSO fix the CLASS, not just the instance: add a test that every module a MAPPED script imports as a sibling is itself MAPPED (an ast walk over the shipped set against the MAPPING, the audit this was found with) - the same defect can recur with any future sibling extraction, and WI-280 alone added six."
workstream = "scripts"
buildtier = "quick"
priority = 1
safety_class = "ordinary"
+++

## Deliverable

scripts/schedule.py now ships. The MAPPING row states its reason at the row (it is a sibling import of the integration seam, not a nicety), with the tests/test_bootstrap.py scaffold file-list entry and the project-trajectory/README.md kit-contents row beside it.

Proven end to end rather than argued: the same fresh-scaffold probe that raised `ModuleNotFoundError: No module named 'schedule'` from integrate.py's claim refusal ladder now answers `integrate: claimed WI-001 on probe`. An AST audit of every MAPPED script's sibling imports established that schedule was the ONLY omission (43 mapped, 46 on disk; the remainder are bootstrap itself and the deliberately kit-only gen_skills_index), so this is a complete fix rather than the first of a series.

The class fix is the durable half: test_every_sibling_imported_module_is_shipped_by_mapping walks the AST of every shipped script and asserts each kit-module it imports is itself mapped. It is mutation-proven against the pre-fix bootstrap.py taken from git history - not a hand-edited stand-in - where it reports exactly {'schedule': ['agent_loop.py', 'drive.py', 'integrate.py', 'traj_parse.py']}. WI-280 alone added six sibling modules this session, so the next extraction that forgets its MAPPING row fails in this suite instead of in an adopter's repo.

Found by the gilbert migration, and findable no other way: the kit's own scripts/ dir holds every file so nothing here fails, and an already-adopted repo carries schedule.py from an older kit so no re-sync fails either - only a fresh scaffold reaches it.
