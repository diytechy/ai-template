+++
id = "WI-379"
title = "bootstrap.py's MAPPING omits scripts/schedule.py, so the integration seam is BROKEN ON EVERY FRESH SCAFFOLD. Four shipped modules import it - integrate.py:257 and drive.py:47 UNGUARDED, agent_loop.py and traj_parse.py guarded - and a MAPPING audit confirms it is the only such omission (gen_skills_index is deliberately kit-only). PROVEN 2026-07-31, not inferred: bootstrapped a scaffold with bootstrap.py --dest, added one queued spec, ran `integrate.py claim` and got `ModuleNotFoundError: No module named 'schedule'` from _claim_refusal's frontier check. So a newly scaffolded repo cannot claim work, and a plain agent-resume launch (the WI-374 drive loop) cannot run either - the two headline capabilities of the whole integration seam. Invisible upstream because the kit's own scripts/ dir holds every file, and invisible to the gilbert re-sync because that repo already carried schedule.py from an older kit; only a fresh-scaffold probe reaches it. Fix: the MAPPING row + tests/test_bootstrap.py scaffold file list + the project-trajectory/README.md kit-contents row. ALSO fix the CLASS, not just the instance: add a test that every module a MAPPED script imports as a sibling is itself MAPPED (an ast walk over the shipped set against the MAPPING, the audit this was found with) - the same defect can recur with any future sibling extraction, and WI-280 alone added six."
workstream = "scripts"
specref = "project-trajectory/README.md"
buildtier = "quick"
priority = 1
safety_class = "ordinary"
+++
