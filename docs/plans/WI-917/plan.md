# WI-917 implementation plan: a headless coordinator leg is a marked autonomous run

Spec: `docs/work/active/wi-917/WI-917-headless-leg-marking.md`. Its spec of
record is `docs/plans/2026-10-11-review-churn/README.md`, "Owner rulings,
2026-10-11": revision 35's "The coordinator role" and revision 36's "Headless
coordinator legs are marked now", plus the owner's two rulings of 2026-10-14
quoted in the spec (P9 pulled forward; P9 split, WI-918 taking the merge
slot's reading of the re-claim). Where this plan and a ruling differ, the
ruling governs.

Read for this plan: the spec in full; the rulings section of the plan of
record; `docs/decisions/coordinator-2026-10-14.toml` D-015 (the lane-mode
reading) and D-016 (design calls Q1, Q2, Q4, Q5);
`scripts/coordinator/overnight_legs.py` and `layout.py`;
`kitlib/provenance.py` (IF-194); `agent_brief.loop_provenance_note` (IF-260);
`coordinator_guard.session_prompt`; `agent_session`'s IF-041 and IF-064
contracts; the merge slot's `_loop_claimed`, `_loop_window` and
`_loop_trailer_refusal` in `integrate.py`; `bootstrap.select_skills` and
`delivery_inventory`; the `coordinator-cycle` SKILL.md and
`references/recipes.md`; SR-209 and SR-208 in
`docs/requirements/system-requirements.toml`; TC-241, TC-242 and TC-321 in
`docs/test/test-cases.toml`; IF-194, IF-197, IF-260 and IF-041 in
`docs/requirements/interfaces.toml`; CMP-006 to CMP-009 in
`docs/requirements/components.toml`; Flows 1 and 6 of `docs/runtime-flows.md`;
`tests/conftest.py` (`SLOW_MODULES`, the loop-marker fixture) and
`docs/stack.ini` `[smoke-budget]`. WI-912 landed at `5604f0fd9` (the
adjudicator's trailer line this row relies on) and WI-914 at `4fe9114a1` (the
LLR-292 fix D21 names), so both are in the lane's base.

## The architectural-delta answer

Yes, and within scope. No preparatory refactor is needed. The WI adds:

- **A state:** a run of headless legs is an autonomous run, marked with one
  loop session, where legs ran unmarked. P3 carries it.
- **Values in domains:** the headless block, a new part of every leg prompt
  (P2); the launcher's new stops, exit 2 for an unusable block, note or agent
  CLI and exit 3 for an audit refusal, and its new `check-lane` command (P3,
  P4); and the re-claim subject `reclaim: <branch> (attended)`, a lane-commit
  subject nothing reads until WI-918 (P5).
- **Outputs on new inputs:** each leg's prompt depends on the block and the
  run's session (P3). Whether the next leg starts depends on the audit of the
  refs the leg moved and the commits it added (P4). Whether a leg lands a lane
  depends on `check-lane` (P4, P5).
- **A boundary with a new producer:** IF-194's marker crossing, an environment
  variable a run sets once and its children inherit, now also starts in this
  repo's launcher. The launcher's existing crossing to the agent CLI moves its
  prompt to stdin, the route IF-041 declares for every kit launch (decision 4).
  Both crossings keep their form. The launcher is this repo's tooling, not a
  kit component, so no IF, CMP or runtime-flow row changes (the spec's
  architectural-delta answer; D13). Its git reads are its own and cross no kit
  seam.

Rows P2 to P5 carry the change: the block, the marker and the composition,
the audit and the command, and the procedure text with the re-claim subject.

DELTA: within

## Design decisions this plan fixes

The builder may refine wording. The following are the plan's reading of the
spec, and a critic who disagrees should say so before the build.

1. **One session per run** (D-016 Q1). The launcher calls
   `provenance.mark_loop_process()` once, before the first leg, after the
   block is read. It logs `run session <s> (inherited)` or `(new)`, by
   comparing the marker before and after the call. Kit modules are imported as
   today, from the checkout `--repo` names.
2. **The block is read once per run**, from beside the launcher
   (`Path(__file__).with_name("headless-leg.md")`, a module constant the tests
   replace), as strict UTF-8. Reading it once means a leg that commits an edit
   to the block cannot change a later leg's mode text. The order before any
   leg is: read the block (absent, unreadable or empty after stripping: exit 2,
   naming the path and the reason); mark; compose the note (empty: exit 2,
   naming it); resolve the agent CLI (none: exit 2). `--dry-run` runs the same
   refusals, logs the run session and the composed prompt's size, and returns
   0 before any leg.
3. **The composition** is one function: the handoff's session prompt
   (`coordinator_guard.session_prompt`, unchanged), a blank line, the block
   stripped of surrounding whitespace, then `agent_brief.loop_provenance_note()`
   verbatim, which opens with its own blank line. The session prompt is read
   per leg from the newest handoff, as today. The block and the note are fixed
   for the run.
4. **The launch resolves `claude` with `shutil.which` and pipes the prompt on
   stdin** (UTF-8, `input=`), never in argv. The rest of the argv is unchanged
   and no `env=` is passed, so the leg inherits the marked environment. Why:
   the Done-when puts a stub `claude` on `PATH`, and on Windows a bare name
   reaches only an `.exe` through CreateProcess, while a which-resolved batch
   shim with a multi-line prompt in argv would cross cmd.exe, which re-parses
   it. Piping on stdin is the route IF-041 and IF-064 state for every shipped
   launch template ("the prompt is piped to the child's stdin"). The launcher
   has run by bare name, which CreateProcess resolves only to an `.exe`, so the
   owner's install keeps working. The coordinator records this call in the
   lane's decisions.
5. **The audit's binding** (the spec's Trust section). Immediately before each
   leg the launcher reads trunk's name (`git symbolic-ref -q HEAD` in the
   checkout; a detached HEAD cannot be judged) and snapshots `refs/heads/*`
   (`git for-each-ref --format=%(objectname) %(refname) refs/heads/`). It reads
   the snapshot again immediately after the leg exits, before any other step.
   It then judges, in this order, stopping at the first refusal:
   - **trunk:** the pre-leg trunk ref must still resolve and descend from its
     pre-leg tip (`git merge-base --is-ancestor <pre> <post>`: exit 1 is a
     rewind, any other non-zero exit a failed read). Every commit on its
     first-parent line from `<pre>` to `<post>`
     (`git log --first-parent --format=%H%x00%B%x1e <pre>..<post>`) is judged
     with `provenance.loop_trailer_refusal(message, session)`;
   - **`archive/lanes`:** the same rule over its first-parent line from its
     pre-leg tip to its post-leg tip. When it is absent before the leg, its
     first-parent commits not reachable from any pre-leg tip are judged; when
     the leg deleted it, that is logged. Descent is not required, since the
     spec requires it of trunk alone;
   - **every other branch the leg created or moved:** the lane rule
     (decision 6), over its range from the post-leg trunk tip;
   - **a branch the leg deleted:** logged, not judged.
   A refusal stops the run with exit 3 and a log line naming the commit (its
   sha's first ten hex digits, as the slot names one, and its subject), the
   pre-leg tip trunk no longer descends from, or the read that failed. The
   launcher never repairs, skips or re-orders a commit. Each leg's audit logs
   one summary line: the commits judged on trunk and `archive/lanes`, each lane
   judged with its window size, and each deleted branch. The next attended
   session reads that line (B4).
6. **The lane rule is the merge slot's, with checked reads.** For a branch and
   a trunk tip:
   - its commits are
     `git log --reverse --topo-order --format=%H%x00%B%x1e <trunk>..<branch>`;
   - it is claimed when the newest commit on trunk's first-parent line whose
     subject is `claim: ... -> active/<branch> (bookkeeping)` carries a
     well-formed trailer (`provenance.parse_loop_trailer`), which is
     `integrate._loop_claimed`'s reading;
   - its window is `provenance.loop_lane_window(commits, claimed, branch)`;
   - each windowed commit is judged with `provenance.loop_trailer_refusal(message)`,
     with no session, so any well-formed session passes, as at the slot. A
     `None` window, a person's lane, passes.
   The audit and `check-lane` call this one function. The launcher does not
   call `integrate`'s private functions, because `_loop_claimed` reads a failed
   git read as "not claimed", which the Trust section forbids here (see Risks).
7. **Every git read goes through one checked runner.** A non-zero exit is a
   failed read, except for the two reads where exit 1 is an answer
   (`merge-base --is-ancestor` and `symbolic-ref -q`). Output the launcher
   cannot parse is a failed read too: a snapshot line that is not one full hex
   sha and one `refs/heads/` name, or a log record without a full hex sha
   before its NUL. A failed read is never an empty range or an empty snapshot.
   The runner is a module-level callable the in-process tests replace with a
   fake. The launcher's existing `git()` helper stays for `newest_handoff`,
   whose failed read already stops the run (no handoff found).
8. **`check-lane`:** `overnight_legs.py check-lane <branch> [--repo R]`.
   `--repo` defaults to the primary checkout, as for the run. It binds to the
   branch's tip when it runs, with trunk the branch the checkout's HEAD names.
   It exits 0, or 3, printing the first refused commit or the failed read; an
   unresolvable branch is a failed read. It runs decision 6 and sets no
   marker. The run's own invocation, `overnight_legs.py [--repo] [--max-legs]
   [--model] [--dry-run]`, is unchanged.
9. **The order after a leg:** the post-leg snapshot and the audit come first,
   so a refused commit is named whatever else the leg did. The existing stops
   follow: a non-zero leg exit, a held lease, no new handoff. All of them stop
   with exit 3.
10. **No `Implements:` tags** in the launcher or the block. Both sit outside the
    traced source surface (`docs/stack.ini` `[paths] src`), and the Done-when
    rules out trace rows. The docstring, the block and the skill section each
    cite the rulings they carry, which is D1.

## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The plan gate: this plan, produced after the claim, is committed verbatim as docs/plans/WI-917/plan.md, passes `plan_coverage.py --item` and an independent critique from another model family, and a pass record binds it before any build | D17 | no interface (a process step; intra-module escape) | |
| P2 | The headless block `scripts/coordinator/headless-leg.md`: fixed ASCII text that opens with the marker check, then states the mode, points to the skill's headless-leg section and gives the close-out rule, ending with its ruling citation; it restates nothing of the session prompt | D1; D5; SR-209 | IF-041 (the block rides each leg's prompt to the agent CLI; the launcher is outside the kit, so no row changes) | P1 |
| P3 | The launcher marks its run and composes each leg's prompt: the block read once (exit 2 when absent, unreadable or empty), `mark_loop_process()` once with the session logged, the note (exit 2 when empty), the prompt as session prompt then block then note, and `claude` resolved with `shutil.which` with the prompt piped on stdin; the docstring states the marker, the composition and the new stops; tests for the marker and the prompt | D1; D2; D3; D4; D5; D6; SR-209; SR-208 | IF-194 (mark_loop_process and LOOP_SESSION_ENV: the marker's crossing, with a new producer outside the kit); IF-260 (loop_provenance_note); IF-041 (the prompt on stdin to a which-resolved agent CLI) | P2 |
| P4 | The after-leg audit and `check-lane`: ref snapshots around each leg; trunk and `archive/lanes` first-parent commits judged against the run's session; trunk descent; every other created or moved branch judged by the slot's lane rule; every git read checked (exit 3 naming the commit or the read); `check-lane <branch>` runs the same lane rule; the docstring states the stop and the command; tests for the audit, the command and the failed reads | D1; D2; D7; D8; D9; D10; D11; SR-209; TC-242 | IF-194 (loop_trailer_refusal, parse_loop_trailer and loop_lane_window, with loop_writer_commit through it: the merge slot's rule, called as it stands) | P3 |
| P5 | The coordinator-cycle skill's headless-leg section (SKILL.md section 7): the trailer on every commit, foreground only, owner-held steps, the lane-mode rule, the re-claim step and a leg's landing; pointers from recipes section 1 (adjudication steps 4 and 7), section 3 (squash, messages, archive) and section 7 (Background or foreground); the per-agent copies synced; a cross-reference pin | D1; D12; SR-209; SR-208 | no interface (procedure text and its per-agent copies; intra-module escape) | P2; P4 |
| P6 | No shipped file changes: on the lane tip, the diff touches only this repo's tooling, tests and the `scope: this-repo` skill; `select_skills` never selects that skill and `delivery_inventory` excludes its whole directory; `scripts/coordinator/` and `tests/` sit outside the kit; no TC must cite the new test modules; RESYNC_PACK.md and the registries are untouched | D13; D14; D15; D16 | no interface (a read-only verification; intra-module escape) | P2; P3; P4; P5 |
| P7 | The landing bar on the landing tip: `run_menu.py smoke` within the 60 s budget, `check_trajectory.py --strict` clean, `trace.py --strict` with no finding beyond LLR-292's, `check_docs.py --root . --strict-orphans`, the complexity census and the per-agent skill check; the full suite once at close, which runs TC-241, TC-242 and TC-321 unchanged | D12; D18; D19; D20; D21; SR-208; SR-209; TC-241; TC-242; TC-321 | no interface (a verification step; intra-module escape) | P6 |

No clause is excluded: every D# clause is covered by a row above, both item
SRs are cited, and each TC verifying them (TC-241, TC-242, TC-321) is named.

## Build order and commits

Three build stages on one builder, each stopping for the coordinator to
verify and commit before SendMessage releases the next (recipes section 1):

- stage 1, P2 and P3 together, because the launcher refuses to run without
  the block;
- stage 2, P4;
- stage 3, P5 with its sync.

P6 and P7 are the coordinator's checks on the lane tip and the landing tip.
Every stage commit passes the commit bar (`run_menu.py smoke`) and runs the
slow module `tests/test_overnight_legs_git.py` explicitly, since the smoke
tier does not.

Every test below is written before its code and run red against the lane's
base launcher, in a detached scratch worktree at the base commit with the new
test files copied in, never by stashing. The red output goes in the lane
report. "Fails before" says why each one is red on today's code.

## Steps in detail

### P1: the plan gate (D17)

The coordinator commits this plan verbatim. `plan_coverage.py --item` judges
it, then a fresh critic from another model family (`review_brief.py critique
--plan`). The pass record under `docs/plans/WI-917/` binds the plan and the
Done-when before the first build commit. The claim (`c4a4d7f01`) precedes this
plan. Nothing is built in this row.

### P2: the headless block (deliverable 2; D1, D5)

`scripts/coordinator/headless-leg.md`, ASCII, LF, fixed text. In order:

1. **The marker check, as the block's first line** (D5: "the block (which
   opens with the marker check)"): before step 1, run `echo "$KIT_LOOP_SESSION"`;
   it must print the session that the LOOP PROVENANCE line at the end of this
   prompt names. If it does not, write nothing and end the reply.
2. **The mode:** this session is one headless leg: one turn, ending the reply
   ends the leg, and nobody answers. Where the prompt above says otherwise
   (attended, asking the owner, background tasks or notifications), this block
   governs.
3. **The procedure:** follow the `coordinator-cycle` skill's headless-leg
   section (SKILL.md section 7, "Headless legs").
4. **Close-out:** the new handoff's session prompt block is the prompt above
   this block, copied verbatim, never this block or the provenance line. Add
   the `Overnight: stop` line only when the queue is done or no row can move
   without the owner.
5. **Its ruling, last**, so the first line stays the check: review-churn plan
   revisions 35 ("The coordinator role") and 36 ("Headless coordinator legs
   are marked now"); coordinator-2026-10-14 D-016 (Q2).

No line of the block begins with `Overnight:` or `Resume-not-before:`, the
launcher's two handoff keys, so a block pasted into a handoff by mistake
cannot stop or delay a run. The block restates nothing of the session prompt
(D-016 Q2: nothing is copied, so nothing can drift).

Tests: the block's opening line is asserted by P3's D5 test and by P5's
cross-reference pin. Neither exists before; both fail on the absent file.

### P3: the marker and the prompt (deliverable 1; D1 to D6)

`scripts/coordinator/overnight_legs.py` implements decisions 1 to 4. The
module docstring gains:

- the marker: one session per run, inherited by every leg and every process a
  leg starts, a well-formed inherited marker kept and a malformed one replaced,
  as `mark_loop_process` states;
- the composition;
- the new exit-2 stops beside the existing ones: an unusable block, an empty
  note and an unresolvable `claude`;
- the rulings: revisions 35 and 36, the owner's 2026-10-14 split ruling, and
  D-015 and D-016.

The marker is what arms the commit-msg floor (SR-209), and the held-status
step and the loop writers' refusal arm (SR-208), for every commit a leg makes.

Test modules (both new, neither cited by a TC, D16):

- `tests/test_overnight_legs.py`: in-process only, with no git and no
  process spawned; it stays in the smoke tier as the family's pin.
- `tests/test_overnight_legs_git.py`: a real git repository per case and stub
  legs; it joins `tests/conftest.py` `SLOW_MODULES` with its reason ("a tmp git
  repo per case and stub `claude` legs; its in-process pin is
  test_overnight_legs"), as WI-869 drew the line.
- `tests/overnight_legs_fixtures.py`: the stub program and the repo builder.
  The stub is a Python program behind a `claude` shim on `PATH`: a `#!/bin/sh`
  script on POSIX and a `claude.cmd` on Windows, each exec'ing
  `sys.executable` on the stub. Each leg appends one JSON record (the marker it
  saw, the prompt it got, its argv) and then performs the case's scripted git
  actions. It reads the prompt from argv when the launcher passes it there
  (the pre-change shape), else from stdin, so the red run fails on its
  assertion and never waits on a terminal. Finding no marker, it writes nothing
  and exits 0, as the block tells a real leg.

The tests run `main()` in-process with `LOGDIR` on `tmp_path`, `lease_holder`
returning None, `sys.path` restored, and the kit modules from the suite's own
path, since a tmp repo carries no kit. Git identity and `core.autocrlf` come
from `integrate_fixtures.git_repo`.

Smoke, in `tests/test_overnight_legs.py`:

- `test_the_prompt_is_the_session_prompt_then_the_block_then_the_provenance_line`
  (D5 pin): the composer's output is the session prompt, then the stripped
  block, then the note verbatim, in that order. Fails before: no composer
  exists.
- `test_a_missing_unreadable_or_empty_block_refuses_the_run_before_any_leg`
  (D6), parametrized: absent, a directory in its place, non-UTF-8 bytes,
  empty, whitespace only. Each gives exit 2, a log line naming the block path
  and the reason, and no stub record. Fails before: no block is read, and on a
  tmp checkout the run stops for "no handoff found", whose line names no
  block.
- `test_an_empty_provenance_note_refuses_the_run_before_any_leg` (D6): with
  `loop_provenance_note` replaced by one returning `""`, the run exits 2 naming
  the note. Fails before: no note is read.
- `test_the_run_marks_itself_once_keeping_a_well_formed_inherited_marker`
  (D4 pin): a `--dry-run` over a tmp handoff (`newest_handoff` replaced),
  parametrized over no marker, a well-formed one and a malformed one. After the
  run the marker is well-formed; it equals the inherited one only when that was
  well-formed; and the log names it. Fails before: the dry run sets no marker.

Slow, in `tests/test_overnight_legs_git.py`, each with two legs at
`--max-legs 2`, every leg committing a new marked handoff:

- `test_two_legs_see_one_well_formed_marker_the_same_in_both` (D3). Fails
  before: the launcher sets no marker, so leg 1 finds none and writes nothing,
  and the run stops after one leg with no marker recorded.
- `test_an_inherited_well_formed_marker_is_kept_and_a_malformed_one_is_replaced`
  (D4), parametrized. Both legs see the expected session, and each leg's prompt
  ends with the provenance line naming it. Fails before: no provenance line is
  composed, and a malformed marker reaches the legs unchanged.
- `test_each_leg_gets_the_session_prompt_then_the_block_then_the_provenance_line`
  (D5). Each record is the session prompt of the handoff that leg started from
  (`coordinator_guard.session_prompt`), then the block file's text, whose first
  line holds `echo "$KIT_LOOP_SESSION"`, then the note naming the run's
  session. Fails before: the prompt is the session prompt alone, and on
  Windows the bare-name launch does not find the `.cmd` stub.

### P4: the audit and `check-lane` (deliverable 1, Trust; D1, D2, D7 to D11)

`overnight_legs.py` implements decisions 5 to 9: the snapshot, the audit,
the lane rule, the checked runner and the `check-lane` subcommand. The
docstring's stop list gains the audit (exit 3, naming the commit or the read)
and names `check-lane` and its exits. The module stays one consumer, as the
Trust section names it. Each function stays small (`deep-module-design`):
snapshot, trunk judgement, archive judgement, lane rule, audit, check-lane.
The file is outside the module-size and complexity ratchets, but the test
modules are inside the complexity census and stay under its threshold.

Smoke, in `tests/test_overnight_legs.py`, driving the audit and `check-lane`
through a fake runner:

- `test_every_failed_audit_read_stops_the_run_naming_the_read` (D10),
  parametrized over each read site: trunk's name, the ref snapshot, trunk's
  descent (exit 128, against exit 1 meaning a rewind), the trunk range, the
  archive range, a lane range and a lane's claim lookup. Each is a stop naming
  the read. Fails before: no audit exists.
- `test_a_failed_range_read_is_never_an_empty_range` (D10). A lane range read
  that exits 128 with empty output is a stop; the same empty output with exit 0
  passes. Fails before: no audit exists, and the launcher's only git helper
  returns stdout whatever the exit.
- `test_unparseable_read_output_stops_the_run` (D10; the Trust section's
  "output it cannot parse"): a snapshot line without a full sha, and a log
  record without one. Fails before: no audit exists.
- `test_check_lane_refuses_when_a_read_fails` (D10): an unresolvable branch, a
  failed range read and a failed claim lookup each exit 3 naming the read.
  Fails before: no `check-lane` exists.
- `test_the_trunk_rule_refuses_an_unmarked_or_foreign_commit_and_a_rewind`
  (D7 pin), over fake reads, `archive/lanes` absent before the leg included.
  Fails before: no audit exists.
- `test_the_lane_rule_is_the_merge_slots` (D8, D9 pin), parametrized:
  - a claimed lane holding an unmarked commit is refused, naming it;
  - a lane marked by a `telemetry: session` loop-writer commit is judged from
    that commit on;
  - commits naming another well-formed session pass;
  - a person's lane passes.
  Fails before: no lane rule exists in the launcher.

Slow, in `tests/test_overnight_legs_git.py`:

- `test_a_leg_that_adds_an_unmarked_foreign_or_rewinding_trunk_or_archive_commit_stops_the_run`
  (D7), parametrized:
  - an unmarked trunk commit;
  - a trunk commit naming another session;
  - an unmarked `archive/lanes` commit, made with `git commit-tree` as the
    recipe makes it;
  - trunk reset behind its pre-leg tip, with a marked handoff on top.
  Each exits 3, its log names the commit (for the rewind, the pre-leg tip),
  and leg 2 never runs. Fails before: no audit, so leg 2 runs and the run ends
  0.
- `test_a_leg_that_adds_an_unmarked_commit_to_a_lane_it_marked_stops_the_run_naming_it`
  (D8), parametrized over the mark and the follow-up:
  - the mark: the leg's own marked claim on trunk, or a marked `telemetry:
    session` commit the leg adds to a lane claimed unmarked before the run;
  - the follow-up after the unmarked commit: a marked lane commit, or a marked
    squash onto trunk (`git merge --squash`, then a marked commit).
  Each exits 3, naming the unmarked lane commit. Fails before: no audit.
- `test_check_lane_refuses_a_marked_lane_holding_an_unmarked_commit_before_the_squash`
  (D8): the same lane state before any squash; `check-lane` exits 3 naming the
  unmarked commit. Fails before: `check-lane` is no command, and argparse
  exits 2.
- `test_a_lane_whose_replayed_commits_carry_another_runs_session_passes` (D9).
  The lane is claimed and built by an earlier run, with another well-formed
  session on its claim and commits. Leg 1 advances trunk and replays the lane
  onto it: same messages, new parents. The run goes on to leg 2, and
  `check-lane` exits 0. A second parameter, a person's lane (unmarked claim, no
  loop-writer commit), also passes `check-lane`, as at the slot. Fails before:
  `check-lane` is no command.
- `test_a_git_read_that_fails_after_a_leg_stops_the_run_and_check_lane_refuses`
  (D10, real git). The leg removes the loose object of a lane commit below the
  lane's tip, made writable first on Windows. The tip stays readable, so the
  ref still lists, and the range read fails. The run exits 3 naming that read,
  and `check-lane` exits 3. Fails before: no audit, so the run goes on.
- `test_a_leg_whose_commits_all_carry_the_runs_trailer_runs_the_next_leg`
  (D11). Leg 1 adds a marked handoff, a marked claim with marked lane commits,
  and a marked archive commit. Leg 2 runs, and the run exits 0 at
  `--max-legs 2`. Fails before: no marker, so leg 1 writes nothing and the run
  stops with exit 3 for no new handoff.

TC-242's module (`tests/test_loop_provenance.py`) is run unchanged beside
these. It is the slot's rule the audit shares, and nothing in `provenance.py`
changes.

### P5: the skill's headless-leg section (deliverable 3; D1, D12)

`project-trajectory/skills/coordinator-cycle/SKILL.md` gains `## 7. Headless
legs` after section 6, keeping sections 1 to 6 numbered as the recipes cite
them. It is the procedure's one home, and it cites revisions 35 and 36, the
owner's 2026-10-14 split ruling, D-015 (the lane-mode reading) and D-016. It
links the block (`../../../scripts/coordinator/headless-leg.md`, which
resolves from every per-agent copy too) and states:

- **What a headless leg is:** an autonomous run. The launcher marks it, one
  session per run, and every leg's prompt ends with the block and the
  provenance line.
- **The trailer on every commit:**
  - every message ends with the provenance line inside its final trailer
    block: the landing's message file and an amended message included (the
    last trailer wins), and the `archive/lanes` `commit-tree -F` message, the
    one plumbing commit the coordinator writes;
  - the kit's writers add the trailer themselves, and the adjudicator gets it
    from WI-912's line;
  - a step the marker refuses is never re-run unmarked or past a hook.
- **Foreground only:**
  - every command runs in the foreground with an explicit timeout up to the
    launcher's cap;
  - every Agent call passes `run_in_background: false`;
  - every builder, reviewer and planner is told to run its commands in the
    foreground.
- **Owner-held steps:**
  - the enumerated set: an act the marker refuses (a status move on a held
    rung), an ESCALATE ruling, an open item's ruling, a Done-when item that
    needs an owner act or credential, and a push or a merge to main. Any other
    step the session prompt's Never list or section 5 reserves to the owner is
    treated the same way;
  - the handling: bring the lane to a safe committed point; record the step and
    its evidence in the lane's decisions record and under the new handoff's
    "For the owner"; turn an owner-only decision into a pending open item the
    row's `needs` cites (section 5, unchanged); move to the next row;
  - close out with the `Overnight: stop` line when no row can move without
    the owner, and answer a Codex limit with a `Resume-not-before:` line, as
    the launcher reads it.
- **The lane-mode rule**, stated once (D-015). A lane a headless leg marked,
  by its claim or by a commit one of the loop's own writers made in its range
  under the marker (a sitting's telemetry commit included), lands headless.
  Otherwise the attended coordinator re-claims it before its own first commit
  there, its sittings' verdict and act commits included.
- **The re-claim step**, the subject's one home until WI-918 moves it into
  `provenance.py`:
  - the attended, unmarked coordinator writes an empty commit in the lane with
    the subject `reclaim: <branch> (attended)` and no trailer;
  - a missed re-claim is placed before the first attended commit: create the
    re-claim commit on the last headless commit with `git commit-tree`, then
    replay the attended commits onto it with `git rebase --onto`. A replay
    keeps each message and never reaches the floor;
  - until WI-918 lands nothing reads that commit, and nothing needs to, since
    coordinator landings are hand squashes that never run the slot's trailer
    rung.
- **A leg's landing:** a leg squashes a lane only after
  `"$PY" "$TOOLS/overnight_legs.py" check-lane <lane>` exits 0. Until WI-918
  lands, a leg leaves a lane holding a re-claim to the attended session.

`references/recipes.md` points to section 7 rather than restating it:

- section 1, Adjudication step 4 ("a headless leg: foreground") and step 7 (a
  headless leg's adjudicator commits carry the trailer), plus the Builder
  bullet's existing headless sentence, which keeps its evidence;
- section 3: the squash bullet (`check-lane` first in a headless leg), the
  messages bullet and the archive bullet (the `-F` message ends with the
  trailer in a headless leg);
- section 7, "Background or foreground".

Every clause `tests/test_prompts.py` pins in SKILL.md stays verbatim.

Sync: `python project-trajectory/scripts/bootstrap.py --dest . --sync`
refreshes every per-agent copy (`.claude/skills/coordinator-cycle/` and
`.agents/skills/coordinator-cycle/`), in the same commit, as the
`skills-sync` step requires. `bootstrap.py --check-agents` confirms byte
identity (D12). `check_docs.py --root . --strict-orphans` is run and passes
with the new block (D12). Its scan covers root-level and `docs/` markdown,
and the gitignored `docs/test/report.md` it reports is local, not a finding.
The skill's frontmatter is unchanged, so `skills/INDEX.csv` does not move.

Smoke test, in `tests/test_overnight_legs.py`:
`test_the_block_opens_with_the_marker_check_and_the_skill_section_links_it`.
The block's first non-blank line carries `echo "$KIT_LOOP_SESSION"`; it names
the skill section; that section links the block's path; and the recipes'
section 1, 3 and 7 pointers name the section. It holds the block, the skill
and the recipes to one another. Fails before: no block and no section exist.

### P6: no shipped file changes (D13 to D16)

The coordinator runs these read-only checks on the lane tip, each with
`python -B`, and records the outputs in the lane report:

- `git diff --name-only <trunk base>...<tip>` lists only:
  - `scripts/coordinator/` (the launcher and the block);
  - `tests/` (the two modules, the fixtures, and the `SLOW_MODULES` line);
  - `project-trajectory/skills/coordinator-cycle/` and its two per-agent
    copies;
  - `docs/stack.ini`, only if the membership ceiling is re-stamped (P7);
  - the lane's own records (`docs/plans/WI-917/`, `docs/reviews/wi-917/`,
    `docs/decisions/wi-917.toml`, the WI spec).
- **D14:** `bootstrap.select_skills(stack, domain, binary_assets)` over every
  declared stack and domain value never returns `coordinator-cycle`. The
  exclusions `bootstrap.delivery_inventory()` returns map both
  `skills/coordinator-cycle/SKILL.md` and
  `skills/coordinator-cycle/references/recipes.md` to "scope: this-repo
  skill; never materialized downstream".
- **D15:** neither `scripts/coordinator/` nor `tests/` lies under
  `bootstrap.KIT` (`project-trajectory/`).
- **D13:** `git diff --stat <trunk base>...<tip> -- project-trajectory/RESYNC_PACK.md docs/requirements docs/test docs/runtime-flows.md`
  is empty, so there is no RESYNC entry, no trace row and no flow change.
- **D16:** no TC's evidence names the new test modules, and the strict lints
  and the smoke tier pass anyway. A recount of the test modules no TC cites
  (49 of 232 at filing) gives that count plus the new modules.

### P7: the landing bar (D12, D18 to D21)

On the landing tip, the staged squash, before the landing commit:

- `run_menu.py smoke`: both strict lints, the docs staleness check, then the
  smoke tier timed against its 60 s budget (D19). Its reading is taken beside
  its parent's in one window, as the recipes' load rule asks. If the new smoke
  pins take the tier past `max-tests` (2715), the ceiling is re-stamped in the
  commit that crossed it, with its reason, fig line and decision (recipes
  section 6).
- `check_trajectory.py --strict`: clean (D20).
- `trace.py --strict`: no finding beyond LLR-292's (D21). WI-914 landed
  first, so none is expected.
- `check_docs.py --root . --strict-orphans` (D12), `check_complexity.py
  --mode enforce` (the tests census) and `bootstrap.py --check-agents`.
- `ruff format --check` and `ruff check` over the new test files, the declared
  `[product]` lint, with any `.ruff_cache` left in the tree removed.
- The full unfiltered suite once at close, batched under the tool's cap or
  backgrounded. It runs the slow module and the TCs verifying the item's SRs,
  all unchanged:
  - TC-241 (SR-208): the held-status step and the loop writers refuse a held
    change under the marker, the arm this row's marker sets for every leg;
  - TC-242 (SR-209): the trailer helpers, the commit-msg floor and the slot's
    lane rule the audit shares;
  - TC-321 (SR-209): the adjudicator's launched prompts carry the provenance
    line under the marker, which is how a marked leg's sittings commit.

Outputs are pasted as produced, never claimed.

## Not in this plan

- **The first headless run** is the owner's call to start, by dropping the
  `Overnight: stop` line, so it is no Done-when item (B4). The next attended
  session reads that run's launcher log and handoff and records the result as
  a decision.
- **Landing alone.** This row is a mechanism change: it lands alone, after the
  cycle has run once through WI-912's act turn. Whether WI-916 waits for the
  first headless run is the coordinator's call at the landing.
- **WI-918** reads the re-claim at the merge slot; **WI-851** narrows its
  marker arm. Neither is an edge here.

## Risks and what the critic should check

- **Decision 4 changes how the prompt reaches `claude`.** The spec composes
  the prompt but does not say how it travels. The plan moves it to stdin
  because the Done-when's stub on `PATH` must launch on Windows, and IF-041
  already makes stdin the kit's route. On a batch-shim install the `--settings`
  JSON would still cross cmd.exe; that hazard predates this row, and the owner's
  launches have reached an `.exe`.
- **Refs moved by another process during a leg** are judged as the leg's.
  That is fail-closed: an overnight run assumes nobody else commits in the
  repository while it runs.
- **A true merge onto trunk of a lane the same leg then deletes:** its
  non-first-parent commits are judged by no rule, since the Trust section
  binds trunk to its first-parent line and logs a deleted branch. Coordinator
  landings are squashes (recipes section 3), so the procedure never takes that
  route. The plan follows the Trust section's binding rather than widening it.
- **Surfaced, not fixed here (shipped code, D13):**
  - `integrate._loop_claimed` reads a failed `git log` as "not claimed", so at
    the slot a failed claim read can turn a loop-claimed lane with no
    loop-writer commit into a person's lane, which the trailer rung does not
    judge. The launcher reads the claim through its checked runner instead
    (decision 6). The coordinator may file this as its own row.
  - The claim-subject reading now has two homes, the slot and the launcher,
    until a kit row gives the slot a checked reader both can call.
- **`provenance.py`'s docstring** names the dispatcher and the loop's main
  entry as the marker's setters. This repo's launcher becomes a third,
  outside the kit. It sets the marker in its own Python process, never in a
  person's shell, so TC-242's "launcher scripts never set it" pin, which covers
  the shipped launchers, still holds. No shipped text changes (D13).
