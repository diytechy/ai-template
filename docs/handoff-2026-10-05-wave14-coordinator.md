# Handoff 2026-10-05 (wave 14, coordinator): two lanes in adjudication, the guard first

For the next session's **coordinator**. It replaces
[handoff-2026-10-04-wave13-coordinator.md](handoff-2026-10-04-wave13-coordinator.md)
as the resume map. The wave-13 handoff's "How the program runs" and the wave-11
handoff's roles, tools and "never" list still hold, with the corrections below.
This session's record is
[log.d/2026-10-04-wave14-coordinator.md](log.d/2026-10-04-wave14-coordinator.md).

> **Superseded as the resume map by
> [handoff-2026-10-05-wave15-coordinator.md](handoff-2026-10-05-wave15-coordinator.md).**

The session stopped at about 41% of its context, by the rule the guard it was
building will enforce. It claimed nothing after its one batch: both remaining
lanes needed several more Codex rounds, and Codex was rate-limited until
2026-10-05 02:34.

## State (trunk `refactor_again`, nothing pushed)

- **Landed:**
  - **WI-796:** TC-055 RECORDED pass. Two of six Codex Luna judges returned
    CHANGES-REQUESTED, and an independent Opus adjudicator refuted both against
    the render.
  - **WI-797:** the kit glossary, `project-trajectory/GLOSSARY.md`.
  - **WI-803:** the plan gate (act seq 32). An independent adjudicator ruled the
    builder-reviewer dispute: an unexplained DUAL gap fails too.
  - **WI-824:** closed. It was the WI-803 sweep's re-mint, closed citing act 32.
- **Filed:** WI-823, TC-055's rubric bindings and the full shot matrix (the
  re-judge's follow-ups).
- **Claimed (one scoped unpause, `d15f33f8` to `8b1103b5`):**
  - **WI-822** and **WI-806** are built and in adjudication (below).
  - **WI-818** and **WI-821** are claimed, with no lane worktree cut yet. Cut
    each from trunk (`git worktree add C:/Projects/ai-template.wt/wi-NNN wi-NNN`,
    then merge trunk in) when you start it.
- **Approval acts run to seq 32.** `docs/work/pause` is tracked and
  byte-identical to its 2026-09-04 declaration.
- **The full unfiltered suite** at `78681d97` (detached worktree, fixed basetemp):
  1 failed, 5061 passed and 17 skipped, in 613.8 s.
  - The failure is environmental and passes in isolation (2 passed):
    `test_conftest_isolation.py::test_a_module_importing_kitlib_collects_on_its_own`.
  - It reads the child run's last line as its summary, but conftest's
    "already inside another job object" notice printed after it; the child run
    itself passed (4 passed).
  - This is an unfiled follow-up: the test should find the summary line, not
    take the last line.

## The two lanes in flight

### WI-822, the coordinator context guard (land it first)

The lane is `C:/Projects/ai-template.wt/wi-822`, HEAD `3547242e`, with GPT
Terra's round-3 row edits **uncommitted** in the worktree (also saved as
`C:/Projects/ai-template.wt/review-tmp/wave14/wi822-terra-r3-partial.patch`).

- **Done:**
  - **Sol round 1** (6 MAJOR, 4 MINOR) and **round 2** (2 MAJOR, 2 MINOR): all
    fixed. The round-2 fixes (`b08a1925`) and the adjudication-round tests
    (`3547242e`) have **not been reviewed by Sol yet**.
  - **The real compaction fixture:** a Claude Code 2.1.289 transcript from a
    local probe (coordinator record D-012). It shows that preserved messages are
    named by uuid and never rewritten after the boundary.
  - **The in-lane adjudicator's verdicts** (`docs/reviews/wi-822-context-guard/`
    001 and 002 at `c1fd783`) returned all eight new rows (SR-229, SR-230,
    LLR-300, LLR-301, TC-315 to TC-318) with byte-exact fixes. They rule LLR-140
    MEANING with Fix A and LLR-270 MEANING.
  - **Terra's round 3** applied those fixes and minted IF-277 to IF-280, then
    stopped at the Codex limit **without reporting**. The coordinator renamed
    IF-280's external party to `external:agent CLI`.
- **Owed, in order:**
  1. **Finish Terra's round 3** (resume session `01a10a29-2a58-7352-b6fd-c9516ecfd580`
     from the lane). Five problems remain:
     - check_trajectory: IF-277 to IF-280 have no citing TC;
     - check_trajectory: IF-277's `external:` owner needs its reading stated in
       the far-side module's header;
     - trace integrity: TC-317 cites LLR-140 beside SR-229 (add SR-156, or
       re-pair);
     - the builder owes the `Contracts:` lines for IF-277 to IF-280;
     - the frame test's untied pin (`tests/test_frame_context.py:128`) must
       gain the new `external:` rows that carry "No tie-back" notes. This
       changes no frame crossing.
  2. **Sol round 3** over `b08a1925..` (code) and the rows.
  3. **The adjudicator re-judges** the landed text: resume it, or start a fresh
     Opus session with the two verdicts. Its recommended act is
     `intake.py snapshot --approves "low-level-requirements.toml=WI-822;system-requirements.toml=WI-822;test-cases.toml=WI-822" --reattests LLR-140,LLR-270`
     plus the eight flips.
  4. **Rebase the lane onto trunk before the act** (see the corrections), take
     the act as the lane's last commit, land by squash, archive, sweep, and close
     any re-mint citing the act.
- **After it lands:**
  - This repo's dial (`[coordinator] context_guard_pct = 50`) makes every hand
    claim need the coordinator lease. Run `python
    project-trajectory/scripts/coordinator_guard.py take` from the coordinator
    session before claiming.
  - The tracked `.claude/settings.json` hooks take effect for sessions started
    after the landing.
  - The relaunch has never run live. Do one supervised relaunch before relying
    on it (the builder's D-009/D-011).
- **Shipping** (lane decisions D-002, to record at landing): the module ships
  dormant at threshold 0. The hook registration and launchers stay this repo's
  until a live relaunch is verified.

### WI-806, spine text before the act

The lane is `C:/Projects/ai-template.wt/wi-806`, rebased onto `cde27048`. HEAD is
`61f14843`: the builder's round 1, written after the reviews below. It fixes Sol's
BLOCKER (cell values are judged against every parent) and both MINORs, narrows the
MAJOR (the squash exemption now needs the staged tree to equal git's merge of the
tip, git 2.38+), and adds the adjudicator's two tests and tag. The builder
**disputes** one remaining case (a direct commit byte-identical to an abandoned
squash's merge result stays exempt), recorded in D-004, for the adjudicator. Terra
owes LLR-302's code_symbol (`_commit_parents`, `_squash_lines`) and its squash
sentence (and TC-173's (f)). `acceptance_record.py` sits at exactly 1000 lines.

- **Reviews at `78d90c70`:**
  - **Codex Sol (REVIEW-A):** one BLOCKER (intersecting change labels across
    parents hides newly authored text in a merge or squash), one MAJOR (a stale
    `SQUASH_MSG` exempts a direct trunk commit) and two MINOR. The builder has
    been sent all of them, after the adjudicator's two tests.
  - **Codex Luna (REVIEW-B):**
    - MAJOR: IF-129 not amended. **The coordinator refutes it with evidence:** the
      retired phrase is in no IF-129 cell or contract, before or after the lane.
      It lived only in the warning text, which the build changed.
    - MINOR: all parents, not the first parent. This is the builder's deliberate
      design: a first-parent rule would refuse every refresh merge carrying
      trunk's separate text and act commits.

    The adjudicator rules both points; its call is final.
- **The in-lane adjudicator's verdicts** (001 and 002 at `78d90c7`) return
  LLR-302, LLR-173, TC-173 and LLR-245 with byte-exact fixes, and owe two tests
  (an unreadable parent; an unreadable diff) plus a tag on `_commit_parents`.
- **SN-029** (owner-held) becomes untrue when this lands: its acceptance and why
  cells call amend-and-flip "the sanctioned path". At the landing, file a
  pending open item with its placeholder row, using the adjudicator's
  recommended text (delete the clause; see verdict 001).
- **Owed, in order:**
  1. (Done: the builder's round is committed at `61f14843`.)
  2. Terra applies the adjudicator's fixes and LLR-173's qualification (Sol
     MINOR).
  3. Sol round 2.
  4. The adjudicator re-judges.
  5. Rebase onto trunk after WI-822 lands, take the act, and land.

## Corrections learned this session

- **The pause deletion carries the regenerated `docs/open-items.html`.** The owner
  page renders the pause, so the hook refuses the deletion alone as stale; the
  restore is the same.
- **A lane's first commit attempt sometimes exits 1 with every hook step
  passing** (twice this session). A retry passed both times; the cause was not
  found. Read the hook output before retrying, and never skip the hook.
- **Deleting a landed lane's branch** makes every other lane's tree report a
  "hold-by-rename" ERROR, since it still holds the landed claim folder. Refreshing
  or rebasing the lane onto trunk clears it.
- **Never refresh a lane by merge once its spine rows are committed and trunk has
  taken an act since.** The merge commit writes trunk's snapshot copies, which
  differ from the lane's live registries, and registry-integrity refuses it. Rebase
  the lane's own commits onto trunk instead: no lane commit writes the snapshot.
  In a rebase, "ours" is trunk.
- **Acts serialize.** A lane takes its act on top of trunk's latest act, so rebase
  before the act, and land lanes with acts one at a time.
- **An `external:` IF row tied to no frame crossing** joins the frame test's
  untied pin, with a "No tie-back ..." reason on the row. That is not a frame
  change. Reuse the declared external parties (`external:agent CLI` for Claude
  Code); Terra twice drafted a new one.
- **Smoke-ceiling restamps conflict** across lanes. At each refresh, keep trunk's
  note and add the lane's count beside it; restamp only when the count passes the
  ceiling.
- **Git Bash rewrites a leading-slash argument** (`/compact` became a path). Set
  `MSYS_NO_PATHCONV=1`.
- **A reviewer started in a detached subshell sends no notification.** Run each
  codex call as its own background command.
- **Codex capacity:** about 24 Codex sessions (Sol, Luna, Terra) over about 5
  hours hit the ChatGPT-plan limit. Six of those were Luna image judges with
  about 40 tiles each.
- **A sweep still mints a redundant re-mint row** after a lane's act. Close it
  citing the act once `cmp` shows the registries equal their anchors.

## Decisions to review (confirm or overrule; high risk first)

- **High risk:**
  - `docs/decisions/wi-796.toml` D-001: TC-055 recorded PASS over two judges'
    CHANGES-REQUESTED, both refuted by the adjudicator.
  - `docs/decisions/wi-803.toml` D-001: the byte-identity reading of "DUAL
    fixtures stay byte-identical" under the adjudicator's ruling (a).
  - `docs/decisions/wi-822.toml` D-001 (on lane `wi-822`): the live dispatcher's
    claim route is outside the guard.
  - `docs/decisions/wi-822.toml` D-003 (on lane `wi-822`): the caller's identity
    is read from `CLAUDE_CODE_SESSION_ID`.
  - `docs/decisions/wi-806.toml` D-004 (on lane `wi-806`): the squash exemption,
    to be reworked for Sol's MAJOR.
- **The rest:**
  - `docs/decisions/coordinator-2026-10-04.toml` D-009 to D-013: the batch claim;
    the pause view; Luna as judge; the compaction probe; reusing
    `external:agent CLI`.
  - `docs/decisions/wi-796.toml` D-002.
  - `docs/decisions/wi-797.toml` D-001 to D-006.
  - `docs/decisions/wi-803.toml` D-002 to D-007.
  - The lane records of WI-822 (D-002, D-004 to D-013) and WI-806.

## Open for the owner (not blocking)

- **Push** `refactor_again` and `archive/lanes`.
- **OI-98** and **OI-105**, and the decisions above.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-05-wave14-coordinator.md (the resume map:
the two lanes in flight and their owed steps, and the corrections); the
wave-13 handoff's "How the program runs" and the wave-11 handoff for the roles,
the coordinator tools and the "never" list; the design note
docs/plans/2026-10-04-wi788-design/README.md, its section "The owner's
checkpoint ruling" first; your memory index.

Finish WI-822 (the coordinator context guard) first, then WI-806, each by the
owed steps in the handoff: Terra completes the rows, Codex 6.1 Sol reviews
(high), the independent in-lane adjudicator re-judges and takes the act after
the lane is rebased onto trunk, then land by squash, archive the tip, sweep
with --before/--after, and read the watermark. After WI-822 lands, take the
coordinator lease (coordinator_guard.py take) before any claim. Then build
the claimed WI-818 and WI-821, and the rest of the lane-lifecycle program in
`needs` order, claiming each new batch under ONE scoped unpause.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve.
Stop for the owner only where a row needs a signature (SN-029 at WI-806's
landing, WI-814's new need, a frame change): file a pending open item with its
placeholder row, and continue. Push and merge to main stay the owner's. Never
read OWNER_SCRATCHPAD.md.

At 50% context, stop claiming and close out: update docs/status.md
(forward-only), write the next handoff and a log fragment, and run the full
unfiltered suite once from a detached worktree with a fixed --basetemp.
```
