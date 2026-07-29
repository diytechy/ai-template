+++
id = "WI-103"
title = "PROCESS_OPTIONS byte budget + applies-when index table (M5)"
workstream = "docs"
order = 102
+++

## Deliverable

WI-103 (2026-07-14, OI-6 ruling log.md 2026-07-13): the review's M5 - PROCESS_OPTIONS.md (now 131 KB, 2x the core it optionalizes) grew unbudgeted while PROCESS.md/AGENTS.template.md are guarded, so the bloat just moved next door; and an adopter deciding WHETHER a layer applies had to read a book. Two deliverables per the owner ruling (byte budget + index; doc SPLIT deferred until size forces it). (1) Added an **Applies-when index** section at the top of PROCESS_OPTIONS.md - a 22-row table (one per `##` layer, document order): Layer | Applies when (skip the section if not) | What it adds (files/machinery). Turns the common path into `scan one table, read one section`. (2) Registered PROCESS_OPTIONS.md as a **byte-watched** doc (the PROCESS.md model, not a hard test - a 131 KB doc holding all opt-in layers would fight legitimate additions): added it to the byte-budget-guard skill's Budgets table with baseline **134,965** (2026-07-14), reworded the intro + expansion-homes note, extended the wc command; propagated to the 2 agent copies via `bootstrap.py --dest . --sync` and regenerated skills/INDEX.csv (description changed). A short **Byte budget** note in the doc itself points at the skill + records the deferred split. **Byte delta (flagged):** PROCESS_OPTIONS.md 130,964 -> 134,965 (+4,001 = the index table; this edit establishes the watched baseline). AGENTS.template.md untouched (hard 10,000 budget intact); PROCESS.md 59,827 unchanged. Commit bar: smoke 563 passed/2 skipped, check_docs --stale exit 0, skills-sync (--check-agents) OK 10/10. No SN/SR/LLR/TC (G3).
