# Handoff 2026-09-28 (wave 5, coordinator) — batch B, the consolidation machinery, and the remaining groups landed

For the next session's **coordinator**: an Opus session that coordinates
builders, arbitrates, and lands work on trunk. It replaces
[handoff-2026-09-27-wave4-coordinator.md](handoff-2026-09-27-wave4-coordinator.md)
as the resume map. That handoff's loop, integration recipe and traps still
hold, and the corrections below are folded in. Its **roles do not**: the
owner re-assigned builders, reviewers and arbitration for the next session,
as stated in "Roles for the next session" below. This session's record:

- the log fragment [log.d/2026-09-27-wave5-coordinator.md](log.d/2026-09-27-wave5-coordinator.md):
  every landing, its bar, and the open count at each step;
- the arbitration file [reviews/2026-09-27-wave5/ARBITRATION.md](reviews/2026-09-27-wave5/ARBITRATION.md),
  rulings 1 to 59, with every Codex Sol review file beside it.

## What happened

**Open count: 13 at the start, 11 at the end** (10 queued, 1 deferred;
WI-721 was filed at the close). Every job the wave-4
handoff listed has landed:
- spine-acts batch B, as one sitting and one act;
- WI-679, the consolidation run end to end through the kit's own census,
  judgement and close;
- every remaining group: WI-616, WI-657 part 4, WI-651, WI-655, WI-615,
  WI-557, WI-618 and WI-620;
- five spine-acts batches (B to F), each an independent Fable sitting and
  one snapshot act.

Each group went through Codex Sol rounds and arbitration.

| commit | item | what it carried |
|---|---|---|
| 464dc7ac | batch B (WI-680, WI-681) | 25 approved, 30 re-attested, 7 returned |
| 77fb0936 | WI-679 | consolidation through the kit's census, judgement and close; `intake.py sweep --merged` gives a hand merge the merge slot's mints |
| 0ded5c77 | WI-689 | WI-679 run on the live queue (queue-with-edge: WI-655 needs WI-616) |
| da7ad245 | WI-616 | absolutes: the check to SN/SR/LLR, the OI-37 sweep, batch B's returns |
| e520b6e6 | WI-657 part 4 | WI-624's duplicated-stage research: adopt nothing, a warn-only near-miss report offered |
| fe96ec69 | WI-651 (+666, 671) | the need and stakeholder tiers under the snapshot; an act held to its scope |
| bcf1e9a8 | WI-655 | C2: assumption and surrogate rows, every SR's `da_refs` or `coincident`, the `boundary_refs` re-point |
| d79e039f, 47f8b573, 32687d47 | re-judges | TC-209, TC-210 pass; TC-055 cross-family on native tiles |
| 4ecdc998 | WI-615 | the doctrine sitting, seven of eight parts; OI-95 for the eighth |
| 500be4c9 | WI-701 | TC-055's T5 contrast fixed with one token; T4 measured at 390 px |
| 655c60ab | WI-557 | the delegated-decisions record under `decision_recording` |
| eecd656d | batch C | 31 approved, 9 re-attested (LLR and TC only) |
| 5934f4c3 | WI-707 | batch C's returns; OI-97 for joint delivery |
| e7fe487d | batch D | the SR tier's C2 cells anchored: 13 approved, 76 re-attested |
| cfef8d1d | WI-618 | retired spine rows as structured fragments (`retire.py`) |
| 6763d08d | batch E | LLR-286, TC-299, TC-296 approved; SR-226's chain returned |
| 3bb6186c | WI-715 | SR-226's chain made approvable |
| b90e84b6 | WI-620 (+605, 606, 551) | one session service for every model call; retention shipped at 0 |
| e827e697 | WI-719 | the spot check of WI-620's close: four owed clause parts folded into WI-541 |
| 2d264589 | batch F (WI-716, 717, 718) | 7 approved, LLR-177 and TC-172 re-attested, 10 returned into WI-720 |

Nothing is in flight. Every lane launched this session has landed, and no
worktree remains. Trunk is `refactor_again` at bc3310f3, and nothing is
pushed.

**No `build/*` branch remains.** A squash leaves a lane's own commits only
on its branch, and the review files and ARBITRATION.md cite those shas
(706cadc7, d6ee9cd3, and others). So at the owner's direction, all 60 lane
tips were folded into one side branch, `archive/lanes`, and then deleted.
Each tip is one `-p` parent of a commit whose tree is empty, and each was
verified reachable before its branch went. Every cited sha stays
reachable, and survives a push, without touching main's history. See "Hand
integration" below.

## Your first jobs, in order

1. **WI-721: the full unfiltered suite is red.** At bc3310f3 it read 5
   failed, 4810 passed, 15 skipped, in 1:51:23 (details below). One failure
   was this handoff not yet linked, and that is cleared. The other four are
   real and landed unseen, because each lane ran only its named slow
   modules. WI-721 carries them, plus the wall time to measure. Build it
   first, and run the full suite again at its close.
2. **Put the owner's items below to the owner.** Several of them gate
   queued rows.
   WI-713 waits on OI-96. WI-697 waits on WI-667. WI-667 needs its
   red-TC rung re-armed.
3. **WI-720 first**: a quick spine lane over fourteen cells of WI-620's
   returned rows, SR-222's and SR-227's chains. It is mostly receipts and
   history in standing cells, plus LLR-268's raw-usage description (and the
   same sentence in `session_adapters.py`'s IF-245 docstring) and TC-268's
   second-tick assertion. Its merge mints the first approval, which goes to
   the next spine-acts batch. Until then, `trace` advises that LLR-267 and
   LLR-269 read Drafted under Approved cases.
4. **Then the queue**, one builder each, at most four at once. Triage
   before building.
   - **WI-541** verifies the retention layer on this box. It now also
     carries WI-620's four owed clause parts, folded in by WI-719: the live
     codex and opencode fixture recordings, the opencode pathway re-check,
     and the first corrected-occupancy log. It needs live model runs, which
     the permission classifier refused this session (see "For the owner"),
     so do not start it without the owner.
   - **WI-545** is the decomposition debt; WI-620 unblocked it. Its Context
     holds the live duplicates WI-624's research sampled.
   - **WI-657** stays open for the narrowed rung question (the owner's).
   - **WI-684 and WI-688** hold owed acts: TC-036 owes a person's re-sync of
     a stamped adoption, and TC-211 owes the SR-161 record producer. Closing
     them re-mints them at every merge, so leave them open until the act is
     done.
   - **WI-625** is deferred, and last.

## For the owner

- **Three open items, each with a recommendation:**
  - **OI-95:** where the `Review-Verdict` trailer rides; recommendation (a).
  - **OI-96:** the dashboard's shrink floor at 390 px; recommendation (a), a
    rendered-pixel minimum. WI-713 (TC-055's re-judge) waits on it.
  - **OI-97:** a joint-delivery classification class; recommendation (a).
- **Live model runs, owed to a person.** The permission classifier refused
  the builders' live codex and opencode runs, and nothing worked around it.
  Two jobs are owed:
  - record `tests/golden/sessions/codex-exec-json.jsonl` and
    `opencode-run-json.jsonl` live, since both are built from documented
    shapes;
  - re-run the opencode pathway checks on the installed 1.18.29 over the
    changed route (`run --format json`): stdin delivery and empty-stdin
    refusal, `--auto`, and a one-word ping to Kimi and to Grok. Then update
    `docs/agents.toml` from 1.17.18.

  WI-606's last two Done-when lines stay unmet until then. WI-541 needs the
  same kind of runs.
- **The needs are yours:**
  - re-attest SN-003, SN-008, SN-009 and SN-025, which WI-616 amended and
    WI-651 put under the drift comparison: `intake.py snapshot --reattests
    SN-003,SN-008,SN-009,SN-025` in your own reviewed commit;
  - tag SN-005 `process` so SR-224 can be approved;
  - consider widening SN-025's acceptance instead of keeping SR-220 derived.
    The adjudicators recommend it; SR-223 stays derived.
- **WI-657's rung, narrowed.** Batch C's approvals took the derived stage
  to DevStg-Impl (eecd656d). So `complexity` (green, 203 rows) and
  `dupes-census` (warn-only, 5/5/52 against a 0/0/0 stamp; the five
  groups are named in WI-545) now select at their ruled rung. What is left
  is yours: should a step also select below its rung when the derived stage
  falls back?
- **The pause** (`docs/work/pause`, since 2026-09-04) still holds the loop.
  Unpausing is your reviewed deletion. The first session log after it is
  the first under WI-605's corrected occupancy.
- **Kit gaps recorded in the log, not filed:**
  - the amendment brief omits routed pointer cells, so an adjudicator must
    read them itself;
  - an amendment and its act that share a squash mint a redundant row
    (WI-706, WI-710);
  - a first-approval brief cannot show a form finding that fires only on
    Approved rows;
  - observation inputs are too coarse: a traced cell or any section edit
    stales a record, and the re-judge brief lists every input, not the
    changed ones;
  - the absolutes check keeps reporting the absolutes the sweep judged
    closed.
- **S11 for the loop.** Hand integration now follows your direction
  (below). The loop's `integrate.py` still merges `--no-ff` under
  RULING-6, and its `audit` flags every squash commit. Moving the loop to
  squash-plus-archive is S11's plan and a RULING-6 amendment, designed with
  S9's reviewer-commit check.
- **Four non-lane branches** are yours to decide on: `MultiRepoSupport`,
  `contract_split`, `template-review-fixes` and `wi-657-pre-rebase`.
- Unchanged: merge-to-main and push (`push = "human"`).

## Roles for the next session (owner direction, 2026-09-28)

These replace the wave-4 handoff's "Builders", "Adjudications" and "Sol
reviews" bullets, and its rule that the coordinator arbitrates alone.

- **Builders are Codex Sol, launched through the CLI**, not Claude
  subagents.
  - Each builder works in its own worktree, cut from a named trunk commit
    (`git worktree add -b build/wi-NNN <path> <sha>`).
  - Launch it backgrounded, with the prompt on stdin as a UTF-8 file:
    `codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" -c 'windows.sandbox="elevated"' -s workspace-write -C <worktree> --add-dir C:/Projects/ai-template/.git --skip-git-repo-check -o <out> - < <prompt>`
  - The prompt carries what the builder note carried:
    - [the builder brief](plans/2026-09-26-assumption-tier-builder-brief.md);
    - the item (a consolidated host reads its absorbed specs under
      `docs/archive/work/restructured/`);
    - the worktree, the pre-assigned ids, `-n 2`, and any amendment grant;
    - "commit on build/wi-NNN only; never push, never merge, never touch
      the primary checkout".
  - `--add-dir` names the primary's `.git`, because a linked worktree keeps
    its git metadata there, outside the worktree. Without it the sandbox may
    refuse the builder's commits.
  - **This launch is untested.** Confirm the first builder can commit. If
    the sandbox or the permission classifier refuses, surface it to the
    owner. Never escalate to `--dangerously-bypass-approvals-and-sandbox` on
    your own.
  - A fix round is a fresh `codex exec` carrying the ruling and the prior
    sha, or `codex exec resume <session id>` (the id is in the `-o` run's
    log).
  - At most four builders at once, fix rounds included.
- **The reviewer is Claude Sonnet 5.5**, an Agent-tool subagent
  (`model: "sonnet"`; confirm the alias resolves to 5.5).
  - It is read-only: it is told to modify nothing, and it reviews the lane's
    commit range against its spec.
  - Its output contract is unchanged: one verdict line
    (`<sha> SOUND|NOT YET SOUND`), then blocker/major/minor findings with
    file:line evidence.
  - Every fix round gets a confirmation. Copy each review beside
    ARBITRATION.md, for example `sonnet-wi720.md`.
  - Sol building and Sonnet reviewing keeps every lane's review
    cross-family.
- **Arbitration goes to an independent Opus agent** (`model: "opus"`),
  never Fable, and is no longer ruled by the coordinator alone.
  - When a builder and the reviewer disagree, or you doubt a finding, brief
    a fresh Opus agent that directed none of the work. Give it the
    governing texts, the finding and both positions.
  - It rules. You record the ruling, with its reasoning, in the wave's
    ARBITRATION.md.
  - A finding the builder accepts needs no arbitration.
- **Spine adjudications and spot checks also go to an independent Opus
  agent**, in place of Fable.
  - It must have directed none of the amendments.
  - It works from `adjudicate_brief.compose`, rules each row and routed
    cell, and takes the one act.
  - The Sonnet reviewer then cross-reviews every act. That review is now
    same-family, where Codex Sol's was not.
  - Where a check must be cross-family, the judge's family must differ
    from the family that wrote the code under judgement. For TC-055's
    critique: a Claude judge for rendering code Sol wrote, a non-Claude
    judge for code Claude wrote.

## Hand integration: one commit per item, lane tips archived (owner direction, 2026-09-28)

Main's history stays legible: **one commit per work item**, or per batch of
items landed together, as the S11 direction reads. The lane's round commits
are kept, off main, in `archive/lanes`.

1. Squash-merge (`git merge --squash build/wi-NNN`) and integrate as the
   wave-4 recipe says, with the corrections below.
2. Commit it. The message names the item, the final reviewed sha, the
   review rounds and the bar that ran.
3. Archive the lane tip. This touches neither the working tree nor main:

       git update-ref refs/heads/archive/lanes $(git commit-tree archive/lanes^{tree} -p archive/lanes -p build/wi-NNN -m "archive: build/wi-NNN at <sha8>")

4. Check `git merge-base --is-ancestor build/wi-NNN archive/lanes`, then
   `git worktree remove <path>` and `git branch -D build/wi-NNN`.
5. Run the sweep (`intake.py sweep --merged ...`).

Reviews and ARBITRATION.md keep citing round shas, which stay reachable
through the archive. The findings and their fixes are also recorded in
prose in the log, so the trail does not depend on any sha. `integrate.py
audit` flags these squash commits until S11's ruling. Expect that, and
don't "fix" it with a `--no-ff` merge.

## Corrections to the role and the loop

- **A hand squash-merge is followed by `intake.py sweep --merged WI-NNN
  --before <trunk before> --after <the squash> --branch build/wi-NNN`.**
  WI-679 built it: it replays the merge slot's mints. Without the range it
  refuses.
- **Registries merge table by table, not by line.** Git aligns identical
  `status`/`phase` tails across rows two lanes added, and keeping both hunks
  can strip a row's tail. The scratchpad's `toml_merge3.py <branch> <paths>`
  merges `[table.ID]` blocks from the merge base. Rebuild it if the
  scratchpad is gone; its docstring is the spec.
- **Run the whole smoke tier at the merge.** Builders are told not to on a
  shared box, so a lane can carry a smoke red: WI-620's IF-247 named its
  own owner as consumer, and `test_seam_resolution` caught it only at the
  merge's bar.
- **An adjudication brief is not the whole scope.** Tell every adjudicator
  to read and rule the routed pointer cells (`SN-Refs`, `Boundary-Refs`,
  `SR-Refs`, `Verifies`) itself, and to flip and run `trace.py --strict` to
  see form findings. Batch D was reverted once for this (ruling 51).
- **Observation re-judges churn** when a lane touches their inputs before
  they land. Judge them on the latest trunk and land them promptly. A
  critique of a tall screenshot uses native-resolution tiles, never one
  downsampled image, and TC-055 needs a cross-family judge (see "Roles").
- **A coordinator's note to an adjudicator points at the brief; it never
  restates the brief's aftermath.** Ruling 58: the note for batch F had
  CLARITY and MEANING backwards. In the kit's amendment brief, CLARITY owes
  nothing, and MEANING on a released rung is re-attested by the
  adjudicator. A cross-review of every act caught a real finding in
  batches D, E and F (Codex Sol's then; the Sonnet reviewer's now), so keep
  it.
- **Smoke seconds on a loaded box are not a breach to re-stamp.** A control
  run at the parent commit tells load from regression.
- **The smoke tier grew with WI-620:** 1893 collected under the 1955
  ceiling. It read 41.7 s on a quiet box at 2d264589, against 26–35 s at
  1799 tests before, so the 60 s budget has less headroom than it did.
  Watch it; don't move the budget.

## The full unfiltered suite

Run once this session, quietly, at bc3310f3 (`python -m pytest -q -n auto
-p no:cacheprovider`):

    FAILED tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans
    FAILED tests/test_generated_freshness_wiring.py::test_skills_index_step_reds_when_a_skill_is_added
    FAILED tests/test_trace_golden.py::test_golden_clean_spine - AssertionError: ...
    FAILED tests/test_trace_golden.py::test_golden_offspine_rich_spine - Assertio...
    FAILED tests/test_trace_golden.py::test_golden_orphaned_spine - AssertionErro...
    5 failed, 4810 passed, 15 skipped, 18 warnings in 6683.90s (1:51:23)

- **`test_check_docs`:** the orphan was this handoff before `docs/status.md`
  linked it, and the close-out commit clears it.
- **`test_trace_golden` (3):** `retire.live_ids` reads only TOML, so
  WI-618's retirement advisory calls every live row of a CSV-registry
  scaffold spent-without-record.
- **`test_skills_index`:** the planted skill's description trips the newer
  100-character floor before STALE.

All four real failures are WI-721's. So is the wall time, which was about
10 minutes before.

**Lesson:** lanes run their named slow modules, not the slow tier, so a red
in a slow module another lane's change reaches lands unseen until the full
suite runs. Run the full suite at every phase close, as the rule already
says, and consider running it after any lane that changes a shared reader.
