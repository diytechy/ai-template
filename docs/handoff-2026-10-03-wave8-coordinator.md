# Handoff 2026-10-03 (wave 8, coordinator): Claude Opus builds, Codex Luna reviews

For the next session's **coordinator**: an Opus session that dispatches builders,
reviewers, independent adjudicators and judges, and lands their work on trunk. This
handoff replaces
[handoff-2026-10-03-wave7-coordinator.md](handoff-2026-10-03-wave7-coordinator.md)
as the resume map. That handoff's hand-integration recipe still holds, with the
corrections below.

This wave's record:
- the log fragment
  [log.d/2026-10-03-wave8-coordinator.md](log.d/2026-10-03-wave8-coordinator.md), with
  every landing, sitting and bar;
- [reviews/2026-10-03-wave8/](reviews/2026-10-03-wave8/).

## New roles (owner direction, 2026-10-03)

- **Builder: Claude Opus, medium effort.**
  - Dispatch it with the Agent tool, `model: "opus"`, working in a pre-cut lane
    worktree.
  - The Agent tool takes no effort parameter. An agent definition's frontmatter
    sets it (`.claude/agents/<name>.md`). Confirm the frontmatter key with the
    `claude-code-guide` agent before creating a `kit-builder` definition with
    `model: opus` and medium effort. None exists yet.
  - An Opus builder is not sandboxed. It can run the hook test modules, sync the
    `.agents` skill mirror and run the whole smoke tier, which Sol could not.
  - Keep the rule that the builder leaves its change uncommitted. The coordinator
    then:
    1. verifies it;
    2. regenerates the generated files with `trunk_step.py --regen`;
    3. commits it on the lane.
- **Reviewer: Codex Luna (`gpt-6-luna`), high effort, through the codex CLI.**
  The set-up lives outside the repo in `C:/Projects/ai-template.wt/coordinator-tools/`
  (its README has the exact commands):
  - `review-prompt.template.md` is the reviewer brief.
  - `mkprompt.py` fills its slots and refuses to write the prompt while any slot
    is unfilled.
  - `luna_review.sh <worktree> <prompt> <out> [effort]` launches the newest VS
    Code extension codex.exe with
    `exec -m gpt-6-luna -c model_reasoning_effort="high" -c 'windows.sandbox="unelevated"' -s workspace-write --add-dir C:/Projects/ai-template.wt/review-tmp`.
    - It writes the review to `<out>` and the transcript to `<out>.log`.
    - It exits 3 if the reviewer changed the lane.
  - Run the launcher with `run_in_background`. Its allow rule is in
    `.claude/settings.local.json`.
  - Probed end to end on 2026-10-03:
    - `-s read-only` cannot run Python at all ("no usable temporary directory").
    - `workspace-write` with the added scratch root and a LITERAL `--basetemp`
      under it ran `tests/test_rule_sync.py`: 42 passed, lane unchanged.
    - The sandbox shell is PowerShell, so `$TEMP` is empty there.
  - There is no 6.1 Luna; the models cache lists `gpt-6-luna` and `gpt-5.6-luna`.
  - Builder and reviewer are now cross-family (Claude builds, Codex reviews).
  - Luna also takes the cross-reviews of adjudication acts, which Sonnet did this
    wave.
- **Unchanged:**
  - An independent Opus agent adjudicates, arbitrates and judges. It is a fresh
    session that directed none of the work.
  - TC-055's judges must differ in family from whoever wrote the rendering code
    under judgement.
  - The `Bash(codex exec *)` allow rule stays; the reviews now use it. Remove it
    when the queue drains.

## State at handoff (trunk `refactor_again`)

- **Landed this wave:**
  - WI-747: rubric-first observation judgement on a closed-work cadence.
  - WI-667: assumption-only cases in both briefs, and the release checklist's
    assumptions section.
  - WI-770 and WI-774: the returned rows reworked.
  - Spine-acts batch N (returned) and batch O (act seq 22: 11 re-attested,
    7 approved, 4 returned).
  - WI-771 filed.
- Nothing is pushed. Lane tips are in `archive/lanes`. Approval acts run to
  seq 22.
- **Coordinator tools** are kept outside the repo in
  `C:/Projects/ai-template.wt/coordinator-tools/` (see the README there):
  - `compose.py` composes adjudication briefs;
  - `toml_merge3.py` merges registries table by table.

## Resume here, in order

1. **One combined sitting over WI-775 and WI-776.** WI-774's merge minted both.
   - WI-775 is the amendment of SR-215 (rationale) and TC-055 (expected). WI-776
     is the first approval of LLR-296, TC-306, TC-309 and TC-310.
   - Use one act, with one combined ref per registry (`WI-775+WI-776`).
   - The first-approval copy of the test-case registry is refused while TC-055
     has drifted unattested, so the two must act together.
2. **WI-697, TC-279's first judgement.**
   - Lane `build/wi-697` (worktree `C:/Projects/ai-template.wt/wi-697`) is at
     `53912f68`. That commit holds round 1's verdict, `NEEDS-JUDGEMENT result=-`,
     because the coordinator's draw missed about 93 of 516 back-linked parts.
   - Round 2's draw and five fresh-reader statements are ready in
     `C:/Projects/ai-template.wt/wi-697-notes/round2/`:
     - `draw-r2b.txt` and `draw_parts_v3.py`: the population is
       `gen_arch_map.declaration_sites`' distinct (file, enclosing symbol) pairs
       under `docs/stack.ini`'s src and tests roots, restricted to sites naming a
       live spine id. The seed is trunk HEAD `f2bc66c1`.
     - `draw-r2.txt`: the unrestricted draw, which surfaced a test-fixture string
       naming the non-existent LLR-900/901. Show both draws to the judge, who
       rules whether the restriction stands.
   - Send round 2 to the same or a fresh independent Opus judge, with the brief
     at `wi-697-notes/brief-wi697.md`.
   - It writes a second verdict on the lane, updates
     `inspection-procedures.md#sampled-new-reader-inspection-result`, and records
     with `record_observation.py --tc TC-279`.
   - That result section is a declared input of TC-209, TC-210 and TC-211, so
     editing it makes their records stale. Their records were already stale
     after WI-747.
3. **WI-777: TC-055 re-judge.** Its declared `component:CMP-009` trigger fired at
   WI-774's merge, so the cadence works. Judge it after WI-775 settles TC-055's
   text. The TC-055 judging recipe is in the wave-7 handoff.
4. **WI-771: drop the assumption evidence ladder.** It is strong tier and needs
   WI-770 (done).
   - Build it only after item 1's act lands. Its amendments drift the same
     registries.
   - The 17-row census in its Context is a text match, so confirm each row.
   - `inspection-procedures.md`'s "evidences DA-011" is ladder wording too.
5. **WI-688** second to last (held by OI-99). Its sitting is WI-541's occupancy
   run, and WI-541 closes with it. **WI-625** (deferred) goes last.

## For the owner

- **OI-98 / WI-684:** the FileBackup re-sync is yours. Rule OI-98 when you are done.
- **Need re-attestations:** SN-003, SN-008, SN-009 and SN-025 are carried over.
  SN-043 is new: WI-667 changed its premises from "checked" to "shown false".
- **SR-006:** batch M's one-clause amendment recommendation is unchanged.
- **Disk:** C: holds about 1.5 GB free. The full unfiltered suite has not run this
  wave or the last, and a phase-close green needs space freed first.
- **Carried:** the pause, S11, merge-to-main and push, and the allow rule.

## Corrections to the recipe (learned this wave)

- **Code review does not catch requirement-text defects.** Two Sonnet reviews of
  WI-747 checked the code against SR-215's text. Neither saw that the text inverted
  PROCESS.md's no-result rule. The spine adjudicator caught it.
  - Tell code reviewers to read every amended requirement cell against PROCESS.md
    too.
  - Remember ruling R2: a requirement cell names no command or script. A fix
    prompt that asked SR-215 to name one had to be undone.
- **Snapshot coupling.** An act copying a registry is refused while any APPROVED
  row in it has drifted and is not re-attested; Drafted rows never block.
  - Sit an amendment and the first approvals of the same registries together, as
    one act with `--approves "<reg>=WI-A+WI-B;..." --reattests ...`. The ref is
    free text.
  - Order lanes so that no new amendment lands between a merge and its sitting.
  - Carry rows that no mint routes (blessed but un-anchored rows, or a row given
    no text change) into the sitting's `adjudicates` list, with a Context note.
    The brief renders `adjudicates` intersected with the drifted model, or with
    the live Drafted rows for a first approval.
- **`intake.py sweep --merged` must name every row a landing closed,**
  `;`-joined. With one id, the other rows' Dispositions are silently skipped:
  batch O's successor was missed once.
- **Dispositions headings.**
  - A `## Dispositions` heading with no toml block is a refusal. A RETURN that
    points at another row's draft uses `## Follow-up for the returned rows`.
  - Only partial and cancelled closes owe a successor.
- **Closing a row:** a done row needs a `## Deliverable` section (R-A) and
  `specref = ""` (R-F). Then run `spec_move.py <spec> docs/archive/work/complete/`.
  Keep a hand-filed slug at 37 characters or fewer.
- **Generated files:**
  - Use `trunk_step.py --regen`.
  - A bare `gen_arch_map.py --contracts-doc` without `--src
    project-trajectory/scripts` wipes the interface reference.
  - When the hook names a complexity row that went DOWN, delete only that row.
    A full `--restamp` rewrites the SLOC column of unrelated rows.
- **RESYNC anchors:**
  - Re-anchor a lane's entry at trunk's parent when it lands.
  - Never anchor at a lane-only sha.
  - Fold a fix round's entry into its parent entry.
- **TC-279 draws:**
  - The part population is the kit's own harvest (`declaration_sites`), never a
    hand-written docstring scan.
  - The first result is recorded only after the case is approved.
- **`trace.py --strict` exits 1 on trunk**, from LLR-292's "no claim is made that
  crossing count is minimal". That is a disclaimer the vagueness lint misreads.
  The commit bar does not run it, but adjudicators do: tell them it is
  pre-existing, or file a lint fix.
- **Verify before a round trip.** A finding's load-bearing claim can often be
  confirmed on a scratch copy faster than another review round. This wave the
  IF-200 seam fix was confirmed that way (`check_trajectory --strict` exit 0 with
  the edit, ERROR without it). Say so in the log.
