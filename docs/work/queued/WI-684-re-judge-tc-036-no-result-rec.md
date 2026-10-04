+++
id = "WI-684"
title = "re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093"
workstream = "process"
sr_refs = ["SR-036"]
needs = ["OI-98"]
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-036"]
+++

## Context

The merge checkpoint at 77fb093 found observation test case TC-036 due for re-judging.

- What changed: no result has been recorded for it.
- Method: Inspect a re-sync done per ADOPTING.md section 6 against the docs/kit-version diff — kit-owned taken wholesale, generated docs regenerated, filled-in files preserved. Process doc + downstream-resync skill; no automated test.
- Expected: Satisfies SR-036 AcceptanceCriteria
- Declared inputs: project-trajectory/ADOPTING.md; project-trajectory/skills/downstream-resync/SKILL.md; SR-036
- Result lifetime: 90 days
- Latest result: none
- Inputs digest at 77fb093: sha256:2f2f30dfba872273c9250558dcde22783dad0a144e4d94e761ca0124f200e336

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-036 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-036 -> project-trajectory/ADOPTING.md
Judged 2026-09-28 (`docs/reviews/wi-684-re-judge-tc-036-no-result-rec/001-ADJUDICATE-fe96ec6.md`, confirmed by Codex Sol): `OUTCOME: NEEDS-JUDGEMENT result=-`. No re-sync of an existing adoption exists to inspect: this repository is the kit, and no stamped adoption's re-sync is on record. The owed act is a person's re-sync of a stamped adoption, per ADOPTING.md §6 and RESYNC_PACK.md, with its per-file decisions, regenerated docs, the target kit's checker run and the re-stamp; an inspector then records TC-036's result. This row stays open so that the merge checkpoint does not re-mint it; it suppresses a second draft only while a row for the case is open (wave-5 ruling 31). Folded (the adjudicator's finding, upheld by Sol): TC-036's `inputs` omit `project-trajectory/RESYNC_PACK.md`, where the procedure lives, so a change to the pack would not stale a recorded result. Amend the cell (approved, so it goes to adjudication) before the result is recorded.


## Owner direction 2026-09-30

For now the stamped adoption to re-sync is `C:\Projects\FileBackup` (kit stamp
`9b697cc 2026-07-02` in its `docs/kit-version`), performed as a scratch trial
and not committed to that repo's trunk. The per-file decisions, regenerated
docs, target-kit checker run and re-stamp are recorded here, and an inspector
then records TC-036's result. The `RESYNC_PACK.md` input amendment above is
still owed first.
