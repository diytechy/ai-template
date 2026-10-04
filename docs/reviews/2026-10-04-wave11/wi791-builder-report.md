# WI-791 builder report (Claude Opus kit-builder, 2026-10-04)

## Changes
- acceptance_record.py: AMENDMENT_CSVS = APPROVAL_ACT_CSVS (SR, LLR, TC, SN, DA, SUR); staged_spine_amendments walks it; the pre-commit amend-without-flip warning (staged_spine_findings) reads the same walk (now warns on approved needs/assumptions/surrogates; Hat-Refs arm silent there). SPINE_CSVS unchanged (first-approval mint, check_test_first, retired flip untouched). _amended_cells extracted (complexity 20 -> 9). Gap 2: held_reattest_refusal (+ verdict_rulings, _ruled_row, _held_row, _held_act_lines, _wrote_ledger) wired into merge_approval_refusal: refuses at the merge slot any row an adjudication re-attests on a rung trunk's dial holds unless the act's ledger entry names a verdict file with a `- [CLARITY] <id>` line. String parsing (module may not import re). IF-091 header text updated.
- baseline_snapshot.py: optional ledger `verdict` field (_record_act writes when given; parse_acts returns when present; _named_rows_problems split from _entry_problems); copy_live(..., verdict=None); _refuse_verdict refuses a verdict with no --reattests or naming no file; act_summary prints it; tier_owing (needs_owing delegates); copy_live 26 -> 14 via _seed_targets/_copy_registry. IF-123/IF-220 header text.
- intake.py: adjudication_action(human_held, verdict="") three arms: released -> flip; held + CLARITY -> reattest; held otherwise -> recommend. `snapshot --verdict PATH`. Amendment row Context states new aftermath.
- adjudicate_brief.py: amendment brief renders drifted SN/DA/SUR rows (_unchained_amended_rows); _REGISTRY_OF gains SN/DA/SUR; _aftermath takes held-rung arm from intake.adjudication_action (deferred import); released wording: CLARITY rows in --reattests (gap 0).
- prompts/adjudicate-amendment.template.md: aftermath rewritten (CLARITY re-anchored via --reattests, + --verdict on held rung; MEANING blessed on released, recommended on held; never approve a first draft on held; gap 3 sibling hold reported).
- gen_open_items.py: verdict_reattest_block/_ledger_entries: audit list at end of section 2 listing every act-ledger entry naming a verdict, newest first, "None recorded." otherwise. IF-074 text.
- PROCESS.md §4: one stated case (+429 bytes, 94,780 -> 95,209); byte-budget skill row re-stamped in 3 copies (4,450 -> 4,451 of 5,000 cap).
- RESYNC_PACK.md entry [since 484b411c].
- docs/decisions/wi-791.toml D-001..D-007; high_risk D-003 (merge-slot refusal binds an attended session in an adjudication lane).
- Tests in test_intake, test_trajectory_staged, test_acceptance_record, test_baseline_snapshot, test_adjudicate_brief, test_snapshot_readers, test_gen_open_items_render. TC-271/TC-278 scope fixtures release the dial. Re-stamps: import-layers deferred window 30 -> 31; module-size intake.py 1658 -> 1672; generated-newlines pin 1392 -> 1443.

## Red/green
Red: 11 failed + 20 passed (new tests); merge-slot tests 5 failed. Green: 43 passed; affected modules 471 passed; smoke 1975 passed, 2 skipped, 1 failed (prompts/CATALOG.md stale, generated).

## Spine change list (builder edited no registry) — CLAIMS for Terra to confirm
- LLR-158 (SR-178): code_symbol += AMENDMENT_CSVS, _amended_cells; detail: walk universe AMENDMENT_CSVS = approval-act set; pre-commit warning reads same walk.
- LLR-278 (SR-178): code_symbol += verdict_rulings, held_reattest_refusal, _wrote_ledger; detail: merge_approval_refusal then calls held_reattest_refusal (held-rung re-attested rows need the act entry to name a verdict file whose `- [CLARITY] <id>` line rules it; dial read at the merge base; a row ruled both ways reads MEANING; refusal names each row).
- LLR-245 (SR-207): code_symbol += _refuse_verdict; detail: --verdict refused without --reattests or when no file; ledger records it.
- LLR-271 (SR-178): code_symbol += tier_owing.
- LLR-167 (SR-146): code_symbol += _unchained_amended_rows; detail: brief renders drifted need/assumption/surrogate rows; aftermath takes held-rung arm from intake.adjudication_action.
- LLR-118 (SR-049): code_symbol += verdict_reattest_block; detail: section-2 audit list.
- LLR-153 (SR-174): code_symbol lacks adjudication_action; detail: walk covers need/assumption/surrogate tiers; adjudication_action's three arms; snapshot --verdict.
- SR-178 acceptance: amended approved need/assumption/surrogate routed to the same judgement; on a held rung a CLARITY ruling may re-anchor only through an act recording its ruling, visible to the owner (R2: no script names).
- SR-207 acceptance: the act may record the ruling that justified a re-attestation.
- SR-140: optional note.
- Possibly a NEW SR for ruled decision 2's held arm as OI-100 amends it (capability voice).
- TC-147 (LLR-153), TC-278 (LLR-278), TC-153 (LLR-158), TC-240 (LLR-245), TC-161 (LLR-167), TC-123 (LLR-118): extend methods/evidence with the new tests (names in the report).
- IF-091, IF-220, IF-123, IF-074 (Drafted): update.
- WI sr_refs: SR-178, SR-207 (+ new SR); specref: system-requirements.toml#SR-178 or new SR.

## Departures
- OI-100 blast radius said "the brief and the mint are unchanged"; the brief had to change (a need-scoped amendment row refused to compose). D-005.
- Legacy .md needs carrier gets no need-amendment mint (same limit as APPROVAL_ACT_CSVS).
