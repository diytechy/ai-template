## 2026-08-29 — WI-532: the interface row shape ships to adopters (OI-67 slice 5)

Deferred open items: none — the shape is ruled; this slice states it where
adopters read it and gives them the converter.

**Summary.** Taken out of plan order, straight after slice 1: a `PROCESS.md`
§8 that described five cells the code no longer reads is the WI-527 4b defect
(shipped documentation the shipped grammar ignores) at the kit's core, and
every day between the two slices was a day the kit shipped it. §8 is rewritten
for the one-owner row — `Owner` the providing thing, the far side naming the
direction, `Channel` and `Data` the typed statement, the definition beside the
code, **mint header-first** for parallel work (plan decision 9), the reason
cells' argument-never-citation rule — in fewer bytes than the paragraphs it
replaces. `PROCESS_OPTIONS.md`'s intra-repo section, `INTERFACES.template.md`'s
rules and worked snippet (both repos' rows of one cross-repo seam, the owner
on one side and `external:` on the other), the registry-machinery reference
row and the two enforcement-audit rows follow it.

**The converter.** `migrate_carrier.py --if-shape` rewrites an old-shape
registry IN PLACE — comments, order and every other cell kept: `owner` from
the stated `provider`, else the owner design row's single `module` (short
spelling); the four retired cells dropped; `channel` SEEDED from the owner's
kind; `consumers` kept as `consumers`. It is a converter that REPORTS every
judgement it did not make rather than guessing: each dropped `req_refs` value
beside its row, each seeded channel, and each owner it could not derive (an
`SR-###` owner with no provider — the published-medium shape) left AS IS for
the adopter to name, where `trace.py --strict` names it until they do.
`--check` reports without writing; a second pass rewrites nothing; the kit's
own registry reads as already converted (the dogfood test). Four tests.

**The RESYNC entry** (`[since 088a6cca]`, the commit the shape landed in)
carries the kit-owned file list, the two commands, the search recipe for rows
the converter could not finish, what replaces the `req_refs` grep, the
version-bump instruction (do not), and the header-first rule.

**Byte deltas on budgeted files** (`wc -c`, before → after):
`project-trajectory/PROCESS.md` 88,018 → 87,651 (**−367**; the row was
stamped 86,676 — WI-527's +1,342 had gone unflagged and is absorbed in this
stamp); `project-trajectory/PROCESS_OPTIONS.md` 178,760 → 179,209
(**+449**: the seam model paragraph and the risk paragraph);
`project-trajectory/skills/byte-budget-guard/SKILL.md` 4,906 → the re-stamped
size recorded on its own row (cap 5,000), three copies identical.

**Deviations from spec:** none. Not done, stated: `ADOPTING.md`, `EXAMPLE.md`
and `MULTI_REPO.md` name no retired cell and needed no edit.

**pytest totals:** full suite `python -m pytest -q -n auto`: 3071 passed, 15 skipped, 1 failed in 638.98s — the one failure was the C901 census on the converter's new `_convert_if_block` (13, over the ceiling), decomposed into `_fold_owner` / `_rewrite_if_lines` and re-verified by `test_migrate_carrier.py` (36 passed) and both ratchets; smoke tier: 1366 passed, 6 skipped in 92.47s (0:01:32); smoke wall-clock budget: 23.5s vs 60s budget -> within. `check.py` harness: PASS; `check_docs --stale`: 0 broken.
