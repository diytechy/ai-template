+++
id = "WI-545"
title = "The decomposition debt owner (cont.): three wide modules, check_trajectory's remaining fusion, and M-06's last two test monoliths"
workstream = "process"
specref = "docs/plans/2026-08-25-remap-alignment.md"
buildtier = "strong"
priority = 2
safety_class = "ordinary"
supersedes = "WI-521"
needs = ["WI-552", "WI-553"]
+++

## Context

Drafted by WI-542 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

`needs` added 2026-08-31: this row decomposes `agent_loop.py`, `integrate.py`
and `dispatch.py` — the modules the OI-70 repair rows (`WI-552`, `WI-553`)
change. Sequencing it behind them avoids two ratchet re-stamps and a merge
conflict (`docs/handoff-2026-08-31.md` §2).
