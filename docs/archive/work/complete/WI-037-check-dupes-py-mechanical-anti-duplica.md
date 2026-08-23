+++
id = "WI-037"
title = "check_dupes.py - mechanical anti-duplication"
workstream = "scripts"
sr_refs = []
needs = ["WI-008"]
order = 36
+++

## Deliverable

Thread 53 RULED (owner 2026-07-10, recommended defaults) + landed (WI-1.48): opt-in [step:dupes] profile step, --min-tokens default 30, docs/dupes-allow pair allowlist (POSIX-normalized); adapted from gilbert; SR-039/LLR-036/TC-039; kit's own dupes recorded for owner triage, not self-allowlisted.

**2026-08-11 (WI-426, repo-lock D-7):** the duplication census was torn down by owner ruling — `check_dupes.py`, its census file and the spine chain SR-039 → LLR-036 → TC-039 are DELETED (D-4: supersession is deletion, ids are never reused). This row's `sr_refs` is cleared because it is a machine-read join field and the row it named no longer exists; the prose above keeps its citations, which are accurate history. The forwarding pointer for the retired ids is the `docs/log.md` Decisions entry of 2026-08-11.
