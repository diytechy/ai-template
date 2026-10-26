Reviewed: 14f786d1a5291ae5bca2739ae0b798d1656bd5e0

**Verified.** This was a full-lane review in the convergence stance. I read the scoped diff `aa36a5b6e...14f786d1a`, the WI-976 spec, PROCESS.md section 1, the cited SN/SR/LLR/TC/IF rows and the kit-change rubric. I read nothing under `docs/reviews/` or `docs/decisions/` and no lane commit message.

Worst failure classes I hunted first:
1. Silent wrong content: the wrong hats, or the wrong round/no-round decision.
2. Fail-open: a malformed roster that composes anyway, or a slot-less override that breaks.
3. Hat outcome lines changing what a verdict rules.
4. Silent behaviour change hidden in the `adjudicate_brief` -> `amendment_brief` split.

What I checked and found right:
- **The real code paths.** I ran `scripts/coordinator/compose_lane.py` on this lane:
  - An amendment scoped `SN-036;SR-161;LLR-297` composes with the 13 applicable hats' questions and the one-outcome-per-hat instruction. It briefs LLR-297 as "(removed from the live registry)" with a JUDGED-TEXT line.
  - An SR-only amendment (`SR-161`) gets the stated no-decomposition-round line.
  - `mkprompt.py ... HATS=SN-036` puts the same questions, without the verdict instruction, into the spine-author prompt.
- **The module split.** I compared every function AST-by-AST between the old `adjudicate_brief.py` and the new `amendment_brief.py` / `adjudicate_brief.py`. It is a pure move except for three things: `_cell_block` was extracted, `HAT_PARENTS` reporting was added, and removed-row briefing plus the unknown-token refusal were added.
- **Parsing.** `ksitting.parse` / `accepted` / `judged_rows` are unchanged by `- HAT` lines (`test_hat_outcome_lines_change_no_ruling`). No verdict reader matches anything but its tagged `- [..]` lines.
- **Fix regression tests fail on the pre-fix code.** I extracted each fix commit's parent tree with `git archive` and overlaid that commit's tests:
  - 49a47d3b5: 7 of 7 fail with real assertions (`need-b question?` absent or present).
  - 7d9f4143d: 6 of 6 fail ("none of the 1 row(s) ... (TC-002) still carries approved text ...").
  - e12f69aa1 changed docstrings and recipe text only. Its recipe pin fails on the pre-fix tree (3 failed), and its new consistency test passes there, as expected for a fix with no code change.
- **Done-when map.**
  - Ruling fragment `docs/log.d/2026-10-25-wi976-sn036-ruling.md` landed at 36fc6d6f7, before the first registry commit 4fc5d55f4.
  - SN-036, SR-161, LLR-183, TC-178 and TC-211 match the proposed text. SR-161 verification is Inspection. TC-178's expected is split. TC-211 verifies SR-161 and SR-186, and its inputs name the 016 sitting brief and verdict (both files exist) and no sidecar.
  - LLR-297 and TC-312 are gone, and both have records under `docs/log.d/retired/`.
  - LLR-360 and TC-399 are new. IF-133 no longer lists `load`, and `hats.py` no longer calls it.
  - The inspection procedure and its "Missing perspective outcome" input are in. The rubric's R1/B1 are rewritten.
  - The `record` command and `tests/test_hats_record.py` are gone, with no live reference left (grep over every live root in the spec).
  - The sidecar and its pointer paragraph are gone. PROCESS.md section 1, (c3), both roster headers and all three recipe copies are rewritten.
  - SAFETY: the live roster has 15 hats and the template 16; the name pins are split (`TEMPLATE_NAMES`).
  - The hat block's states are covered by TC-399's 19 cases plus the mkprompt tests (none, empty, missing, need-scoped). The RESYNC entry is present, and the catalogue and byte stamp are refreshed.
  - Pending by the spec's own order, so not findings: SN-036's owner act, the lane's other acts, and TC-211's fresh re-judge. The convergence stance also keeps me from reading the 016 verdict, so its hat outcomes are left to that inspection.
- **Decomposition under SR-161.** LLR-183 keeps the row-level Hat-Refs attribution decision. LLR-360 owns the sitting-composition behaviour over a closed input space, which TC-399 covers as one unit case family. TC-211 inspects the SR-level acceptance. Splitting LLR-360 further, for example into a combined-sitting row or an author-prompt row, would repeat one composer's decision with no new verification purpose.
- **Counterpart reading.** IF-129, IF-090, IF-075, IF-113, IF-114, IF-124, IF-161 and IF-287 had their requestors updated to match the real imports. I confirmed `adjudicate_brief` no longer imports `acceptance_record` or `intake`, and `amendment_brief` does.

**Commands**
- `git rev-parse HEAD` -> `14f786d1a5291ae5bca2739ae0b798d1656bd5e0`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../revb/wi-976 <the 15 listed modules>` -> `791 passed, 3 skipped in 1010.60s (0:16:50)` (1 posix-shell gate unsatisfied)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (973 work item(s), 863 done (89%), 34 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.`
- `python scripts/coordinator/compose_lane.py WI-976 amendment "SN-036;SR-161;LLR-297" ...` -> composed, 37810 chars, hat block and removal shown; `... amendment "SR-161" ...` -> composed with the no-round line
- `python scripts/coordinator/mkprompt.py scripts/coordinator/terra-spine-prompt.template.md <scratch> ... HATS=SN-036` -> `mkprompt: wrote ...`, 13 hats' questions under `## Perspectives`
- pre-fix red runs (scratch trees from `git archive <fix>^` plus the fix's tests): 49a47d3b5 -> `7 failed`; e12f69aa1 -> `3 failed, 1 passed`; 7d9f4143d -> `6 failed`
- AST function compare of the old `adjudicate_brief.py` against the new `amendment_brief.py` / `adjudicate_brief.py` (scratch script) -> only the changes listed above
- LLR module/code_symbol scan for modules that hold none of their row's symbols -> `adjudicate_brief LLR-273`

- [MINOR] project-trajectory/RESYNC_PACK.md:9868 -> This entry's "Kit-owned files — overwrite" list omits `scripts/kitlib/bootstrap_manifest.py`. This lane changed that file (the new `amendment_brief.py` MAPPING row), and the file is shipped: its own MAPPING maps it, and earlier entries such as line 9587 list it whenever it changes. An adopter following the list keeps a stale manifest that does not know the new module. -> Add `scripts/kitlib/bootstrap_manifest.py` to that list. -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:2873 -> K3: this lane edited LLR-273's `module` cell and kept `project-trajectory/scripts/adjudicate_brief.py` in it, but none of LLR-273's code symbols (`registry_stamps/_baseline_lines/_spine_stamps/_copy_stamp_lines`) is left in that file. `_copy_stamp_lines` moved to `amendment_brief.py`, and the composer now only calls it. The traced cell therefore names a module that implements nothing of the row. -> Drop `adjudicate_brief.py` from LLR-273's `module` cell. -> @owner
- [MINOR] docs/requirements/system-requirements.toml:868 -> K3: Approved SR-165's `Rationale`, an approved cell, is amended: "the SR-161 form applied to the partition instead of the perspective set" is removed. The `docs/archive/last_approved` copy still holds the old text. The spec of record's spine change set (deliverable 2 and the Done-when "The spine") names SN-036, SR-161, LLR-183, TC-178, TC-211, LLR-297, TC-312, the new rows and IF-133, and never SR-165. The edit is the right counterpart change, since SR-161 no longer has that form, but no spec grant covers it. -> Name SR-165's rationale amendment in the spec's spine change set (or its Done-when), so the act that re-attests it is one the spec of record authorizes. -> @owner
- [MINOR] project-trajectory/scripts/adjudicate_brief.py:652 -> Consolidate (PROCESS.md section 3, deep-module design): the split leaves the composer reaching into the new module's private names, `amendment_brief._loop_approves` (652), `_REGISTRY_OF` (678, 912, 927) and `_copy_stamp_lines` (896). It also homes `adjudicates` and `tier_questions`, which every arm calls (consolidate, rejudge, done-when, combined scopes, first approval), in the module named for the amendment arm. The module boundary does not match the ownership, so the next arm added must import the amendment arm's internals too. -> Move the arm-shared helpers (`adjudicates`, `tier_questions`, `_REGISTRY_OF`, `_loop_approves`, `_copy_stamp_lines`) to one shared home under public names, or keep them in the composer and let `amendment_brief` import them one way. -> @owner

VERDICT: CHANGES-REQUESTED findings=4
