+++
id = "WI-067"
title = "run capability menu - stack.ini [run] + run_menu.py"
workstream = "scripts"
sr_refs = ["SR-046"]
needs = ["WI-010"]
order = 65
+++

## Deliverable

stack.ini gains a [run] section (declared once) read by a new stdlib scripts/run_menu.py - numbered menu / direct launch with exit passthrough / --list agent surface; the run.* launchers become thin delegates and the duplicated RUN_CMD is retired. New SR-046 (+LLR-047/TC-047) formalizes the launcher surface.
