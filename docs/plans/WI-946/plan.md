# WI-946 implementation plan

The overnight launcher binds trunk once per run, keeps the primary checkout
on it, holds `archive/lanes` to a descent rule, and reads a lane's claim
through one checked reader that it shares with the merge slot.

- **Spec of record:** `docs/work/active/wi-946/WI-946-launcher-trunk-archive-claim.md`.
  It amends WI-917's `## Trust` (`docs/archive/work/complete/WI-917-headless-leg-marking.md#trust`).
- **Rulings:** `docs/decisions/coordinator-2026-10-18.toml` D-004 and D-005
  (C1 to C5), and `docs/decisions/wi-917.toml` D-003 (F1, F2, F3) and D-005.
- **The item's SR:** SR-209 (`docs/requirements/system-requirements.toml`),
  unchanged.
- **Its TCs** (`docs/test/test-cases.toml`):
  - TC-242 is amended (P8).
  - TC-321 also verifies SR-209. Its tests are untouched, and it runs in the
    phase-close full suite (P9).
- **Interfaces** (`docs/requirements/interfaces.toml`):
  - IF-065 (agent_common's shared coordinator primitives, Drafted) gains the
    reader in its data.
  - IF-179 (`trunk_name`) is crossed by a new non-kit caller, the launcher,
    with no data change. The launcher is not a kit component, so no registry
    row names it (as in WI-917).
- **Components** (`docs/requirements/components.toml`): `agent_common` and
  `integrate` are both CMP-008, so no component boundary is crossed.
- **Runtime flows** (`docs/runtime-flows.md`): no edit.
  - Flow 4 draws the merge slot's steps but not its provenance rungs. The new
    refusal is one more refusal from an existing rung ("nothing was merged"),
    so the flow's shape does not change.
  - Flow 6 (SR-209's act-turn provenance) is untouched.

## Architectural delta

DELTA: within

All four apply, and each is carried by a row of the table:

- **A new state:** the run's bound trunk, held for the run's lifetime (P4).
- **New domain values:**
  - two launcher stops, a checkout off the bound trunk (P4) and an archive
    that does not descend (P5);
  - a third answer from the claim reader, unreadable, which becomes a new
    slot refusal (P3).
- **An output depends on a new input.** The audit and `check-lane` take
  trunk's identity from the kit's `agent_common.trunk_name` (IF-179). The
  audit also reads the checkout's branch, compared with the bound name (P4).
- **A seam changes.** The claim reader moves into `agent_common`, so
  `integrate` reads it across IF-065, whose data then names it (P2, P3, P8).
  There is no sub-component split, and no refactor this item does not own.
  The extraction is its own behaviour-preserving commit (P2), as S1 orders.

## Decisions the spec leaves to the plan

1. **The reader's shape.** The new function is
   `agent_common.loop_claimed(root, branch, trunk_tip)`. It returns
   `(claimed, unreadable)`:
   - `(True, None)` for claimed;
   - `(False, None)` for unclaimed;
   - `(None, why)` for unreadable, where `why` names the read.

   This is the spec's "returns a refusal string" option, kept in a pair so
   that a boolean answer and a reason never share one value. `claim_base`'s
   `(value, readable)` pair was not chosen because it cannot name the read.
   - **What `why` holds.** It names the git command (`git log
     --first-parent --fixed-strings --grep=... <tip>`), and also:
     - for a failed read: the exit code and the first stderr line, formatted
       as the launcher's `read` formats them (`git ... failed (exit N): ...`);
     - for an unparseable record: the record's first 60 characters
       (`unparseable record ...`).

     So the launcher's existing claim-read cases, which assert `--grep` and
     `exit 128`, keep passing unchanged (D13).
   - **The read.** It uses `--format=%H%x00%B%x1e`, so every record must
     carry a full commit id. A record with no NUL, or whose id is not a sha,
     is unparseable (D18). This is the launcher copy's rule today.
   - **The reading is otherwise `_loop_claimed`'s, verbatim:**
     - the same suffix and `--grep`;
     - the newest match first;
     - `subject.startswith("claim: ") and subject.endswith(suffix)`;
     - claimed exactly when `provenance.parse_loop_trailer(message)` is not
       None.
   - **Where it lives.** Beside `claim_subject` and `claim_base`, with an
     `Implements: SR-209, LLR-248` line. It reads through the module's own
     `git()` (looked up at call time, so the tests can wrap it) and the
     module's existing `_kitprovenance` import.
2. **The trunk rule and the archive rule become one function** (spec
   deliverable 2, "the plan decides the form"; PROCESS.md §3, consolidate,
   don't duplicate). The new function is
   `judge_descent(repo, ref, pre, post, session, may_create)`, and it
   replaces both `judge_trunk` and `judge_archive`.
   - **Present before the leg** (both refs):
     - absent after, or not descending from the pre-leg tip (`merge-base
       --is-ancestor`, through the checked `read`): AuditStop naming the
       pre-leg tip;
     - otherwise its `--first-parent before..after` additions are judged.
       `unmoved` when the tip did not move.
   - **Absent before the leg:**
     - with `may_create=False` (trunk): AuditStop "does not resolve before
       the leg". `pre_leg` already refuses this case, so it is a backstop;
     - with `may_create=True` (`archive/lanes`): absent after reads `absent`;
       created, its commits are judged over `after --not <every pre-leg
       tip>`, as today.
   - **What it returns:** a summary string. Trunk's reads `N commit(s)`,
     whose wording is unchanged.
3. **Where the bind sits.** `prepare_run(repo)` gains the bind as its last
   step, after the CLI resolves:
   - `import agent_common`, then `name = agent_common.trunk_name(repo)`,
     called through the module attribute so the tests can count and replace
     it;
   - on `ValueError`: log `stop: trunk: <message>` and return None (exit 2);
   - otherwise log `run trunk <name>` and return `HEADS + name` with the
     tuple.

   `main` hands the bound ref to every `run_and_audit` call.
4. **The checkout check.** `checkout_refusal(repo, trunk_ref)` reads `git
   symbolic-ref -q HEAD` through `read` (answers 0 and 1). It raises
   AuditStop naming what it read, as follows:
   - exit 1: detached;
   - output not starting with `refs/heads/`: unparseable;
   - any other exit: a failed read, from `read` itself;
   - a branch other than the bound one: names that branch and the bound
     trunk.

   It is called in two places:
   - by `pre_leg(repo, trunk_ref)`, after the snapshot. That function first
     refuses a snapshot without `trunk_ref`, naming it, and returns the
     snapshot;
   - as the audit's last judgement, after the trunk, archive and lane
     judgements, so a refused commit is named first.
5. **The leg's log line.** `audit` returns `(summary, post)`. The line
   prints `pre[trunk_ref][:8] -> post[trunk_ref][:8]`. The
   `git(repo, "rev-parse", "HEAD")` call there goes.
6. **The in-process harness for the shared readers.** The `ol` fixture in
   `tests/test_overnight_legs.py` gains two patches:
   - `agent_common.trunk_name` returns `"main"`;
   - `agent_common.git` is routed through the active `FakeGit`, as an adapter
     from `(code, stdout, stderr)` to agent_common's `(code, out)` shape,
     with stderr appended on a non-zero exit as `git()` does.

   The claim site is still keyed on `--grep`, so `LANE_CASES` and the
   claim-read cases run unchanged through the shared reader.

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The plan gate: this plan, produced after the claim, is committed verbatim and passes `plan_coverage.py --item` and the independent critique before any build commit | D35 | intra-module: a plan document, no code seam | |
| P2 | Extraction, behaviour-preserving (its own commit, S1): `integrate._loop_claimed` moves to `agent_common.loop_claimed(root, branch, trunk_tip)` with its reading and its fail-open unchanged (returns a bool), `_loop_window` calls it with `_head(root)`; the RESYNC entry is written in this commit (the first to touch a kit-owned file) anchored `[since <lane base>]`, naming `agent_common.py` and `integrate.py` to overwrite and stating no migration; the ratchet's exact baselines for both modules re-stamped | D1; D23; D30; D31; D32; D33; D34; SR-209; TC-242 | IF-065 | P1 |
| P3 | The checked reader and both callers: `loop_claimed` returns `(claimed, unreadable)` per decision 1; `_loop_window` returns `(None, "cannot read <branch>'s claim to check its provenance; nothing was merged:\n<why>")` on unreadable; the launcher's `lane_claimed` is deleted and `lane_refusal` calls `agent_common.loop_claimed`, raising AuditStop(why) on unreadable; `integrate`'s `_loop_window` / `_loop_trailer_refusal` docstrings and `agent_common`'s reader docstring and `Contract IF-065:` text state the failure rule and name the reader; claim-reader tests in `tests/test_loop_provenance.py`; the in-process harness adapter (decision 6); ratchet re-stamped | D1; D13; D16; D17; D18; D19; D20; D21; D22; D23; D24; D34; SR-209; TC-242 | IF-065 | P2 |
| P4 | Trunk bound once, checkout held to it, `check-lane` on the kit reader (`scripts/coordinator/overnight_legs.py`, D-004 item 1, wi-917 D-003 F1, D-005 C2/C3): the bind in `prepare_run` (decision 3); the launcher's `trunk_name` deleted; `pre_leg(repo, trunk_ref)` and the audit's last judgement call `checkout_refusal` (decision 4); the audit, its lane-loop exclusion and the lane base read the bound ref; the log line (decision 5); `check_lane` reads `agent_common.trunk_name(repo)`, catching `ValueError` as "cannot judge", and verifies `refs/heads/<name>` as today; real-git and in-process tests | D1; D2; D3; D4; D5; D6; D7; D14; D15; SR-209 | IF-179 | P3 |
| P5 | `archive/lanes` descends (D-004 item 2, wi-917 D-005, D-005 C5): `judge_trunk` and `judge_archive` become `judge_descent` (decision 2); real-git and in-process tests, including the pins | D1; D2; D8; D9; D10; D11; D12; D15 | intra-module: `overnight_legs.py` only, no seam crossed | P4 |
| P6 | The launcher's docstring (deliverable 3, D-004 item 3, wi-917 D-003 F2): `**The bound.**` paragraph (what the two snapshots cannot see; a merge's non-first-parent commits judged by no rule; provenance only, not which branch a leg may move; `check-lane`'s pre-WI-925 escape) and the Stops paragraph naming the run-start trunk refusal (exit 2), the checkout stop, the bound-name stop, the archive descent stop and the unreadable-claim stop; the `check-lane` paragraph says it judges from the trunk the kit's reader names | D1; D24 | intra-module: docstring of `overnight_legs.py` | P5 |
| P7 | The `coordinator-cycle` skill §7 clause (deliverable 4, kit source `project-trajectory/skills/coordinator-cycle/SKILL.md`): the sentence "After each leg the launcher audits every ref the leg moved…" gains that the launcher judges every leg against the trunk it bound at run start and stops the run when a leg leaves the primary checkout on any other branch, a leg's work staying in lane worktrees; `bootstrap.py --dest . --sync` updates `.claude/skills/` and `.agents/skills/`; `check_docs.py --root . --strict-orphans` | D1; D25 | intra-module: skill text, no code seam | P4 |
| P8 | Spine, authored in the lane and judged at its checkpoint sitting, the act through WI-912's act turn: LLR-248 detail gains (capability voice) that a lane's claim record that cannot be read is a refusal, never a lane the loop did not claim, and its `code_symbol` names `loop_claimed`; TC-242 method gains the unreadable-claim case at the merge ladder (the loop lane is refused, naming the read, nothing merged) and its expected the same outcome; IF-065 data gains `loop_claimed` (Drafted, no act); SR-209 unchanged; derived registries regenerated by their generators, never hand-edited | D1; D26; D27; D28; D29; SR-209; TC-242 | IF-065 | P3 |
| P9 | The bar on the landing tip: `run_menu.py smoke` (both strict lints, docs staleness, `check_resync`, the smoke tier within 60 s); `check_trajectory.py --strict`; `trace.py --strict`; `check_docs.py --root . --strict-orphans`; the full unfiltered suite once at close (`pytest -q -n auto`), which runs TC-242's and TC-321's evidence and `test_overnight_legs_git` | D36; D37; D38; D39; SR-209; TC-242; TC-321 | intra-module: verification only, no seam | P5; P6; P7; P8 |

No `Excludes:` line is needed: every D# clause is covered by a row above.

## Step detail and the tests each adds

The modules: `GIT` is `tests/test_overnight_legs_git.py` (real git, already
in `tests/conftest.py` `SLOW_MODULES`, which stays as is for D15), `IN` is
`tests/test_overnight_legs.py` (in process, the smoke tier), and `PROV` is
`tests/test_loop_provenance.py`. "Fails before" names what the pre-change
code does. A pin is marked as one in its docstring or comment.

### P2: extraction (one commit, behaviour-preserving)

- **What moves.** The function moves verbatim into `agent_common`, with an
  explicit `trunk_tip` parameter in place of `_head(root)` inside it.
  `_loop_window` passes `_head(root)`. No test is added: the existing TC-242
  cases in PROV pass unchanged, which is the proof that behaviour is
  preserved.
- **RESYNC.** `project-trajectory/RESYNC_PACK.md` §3 gains one entry,
  written now because `check_resync` refuses this commit without it (WI-916).
  - **Title:** "The merge slot reads a lane's claim through one checked
    reader".
  - **What changed:** an unreadable claim log, or an unparseable record in
    it, is a refusal ("nothing was merged"), never a person's lane.
  - **Kit-owned files to overwrite:** `scripts/agent_common.py` and
    `scripts/integrate.py`.
  - **What to do:** overwrite. No migration: every lane whose claim log reads
    is read as before.
  - **Anchor:** the lane's trunk base, re-anchored at the landing's parent
    when the lane rebases before landing.

  The entry states the final behaviour that P3 delivers.
- **Ratchet.** `tests/test_module_size_ratchet.py` re-stamps both exact
  baselines with a dated reason: integrate down, agent_common up.

### P3: the checked reader, the slot and the launcher's claim read

**Code.**

- **The reader** returns its three answers per decision 1.
- **The slot.** `_loop_window` returns `(None, refusal)` when the reader
  answers unreadable. The format matches the existing unreadable-range
  refusal. `_loop_trailer_refusal` and `_held_status_refusal` need no change,
  since each already returns `_loop_window`'s refusal.
- **The launcher.** `lane_refusal` calls `agent_common.loop_claimed(repo,
  branch, trunk_tip)` and raises `AuditStop(why)` on unreadable. `audit`
  already stops on AuditStop, and `check_lane` already turns one into exit
  3, "cannot judge".

**Tests in PROV.** Each is built on `claim_repo` and the lane helpers. The
claim read alone is made to fail by wrapping `agent_common.git`: only a `log`
call whose argv carries both `--grep=` for `-> active/wi-401 (bookkeeping)`
and the reader's `%H%x00%B%x1e` format is answered `(128, "fatal: bad
object")`. So `claim_base`'s `%H%x09%s` read and every other call are left
alone. A lane whose only loop mark is its claim is used: a marked claim and
one unmarked commit, with no loop-writer commit in the range. Without the
claim, that lane reads as a person's.

- `test_an_unreadable_claim_log_is_refused_by_the_trailer_rung_naming_the_read`
  (D17)
  - **Asserts:** the refusal names `--grep` and "nothing was merged", and
    HEAD is unchanged.
  - **Fails before:** the rung returned None.
- `test_an_unreadable_claim_log_is_refused_by_the_held_status_rung` (D17)
  - **Asserts:** the same lane, and the same refusal from
    `_held_status_refusal`.
  - **Fails before:** it returned None, because `_loop_window` read a
    person's lane.
- `test_an_unparseable_claim_record_is_unreadable_never_unclaimed` (D18)
  - **Setup:** the wrapped claim read answers `(0, "no-sha-record\x1e")` and
    `(0, "<not a sha>\x00claim: ...\x1e")`.
  - **Asserts:** the reader answers `(None, why)` naming "unparseable"; both
    rungs refuse.
  - **Fails before:** the reader returned False, so the lane passed.
- **Pins on a readable log** (D19 to D22; marked as pins), parametrized
  `test_the_claim_reader_answers_as_before_on_a_readable_log`:
  - a marked newest claim: `(True, None)` (D20);
  - an unmarked newest claim, a malformed-trailer newest claim, an older
    marked claim under a newer unmarked one, and no claim: `(False, None)`
    (D21);
  - a marked claim of `wi-402` only, read for `wi-401`: `(False, None)`
    (D22).
- `test_the_slot_and_the_launcher_share_one_claim_reader` (D23)
  - **Asserts:** `not hasattr(integ, "_loop_claimed")`, and the launcher
    (`overnight_legs_fixtures.load_launcher()`) has no `lane_claimed`.
  - **Fails before:** both existed.

**IN** (D13, pins).

- `test_every_failed_audit_read_stops_the_run_naming_the_read[claim]` and
  `test_check_lane_refuses_when_a_read_fails` (the claim case) are
  unchanged. They now pass through the shared reader by way of the fixture
  adapter (decision 6). They are marked as pins in a comment: today's copy
  fails closed too.
- New `test_an_unparseable_claim_record_stops_the_audit`. The claim answers
  `ok("not-a-sha\x00claim\n\x1e\n")`, and the test asserts "unparseable".

### P4: the bind, the checkout, `check-lane`

**The stub.** `tests/overnight_legs_fixtures.py` gains stub actions and a
`TRUNK = "refs/heads/main"` constant:

- `checkout_elsewhere`: `git checkout -q -b elsewhere`;
- `main_unmarked`: `plumb(TRUNK, "unmarked trunk work")`;
- `archive_rewind`, `archive_reset_unrelated` and `archive_delete`, used
  in P5.

**GIT tests.**

- `test_a_leg_that_leaves_the_primary_checkout_off_trunk_stops_the_run` (D3)
  - **Plan:** `[["checkout_elsewhere", "handoff"], ["main_unmarked",
    "handoff"]]`.
  - **Asserts:** exit 3, one leg record, and the stop line names
    `elsewhere`.
  - **Fails before:** leg 2 ran from the handoff on `elsewhere`, and its
    audit judged `elsewhere` as trunk. The run ended with exit 0 and two
    records.
- `test_the_run_binds_trunk_once_and_logs_it` (D4)
  - **Setup:** wraps `agent_common.trunk_name` with a counter and runs two
    legs.
  - **Asserts:** count == 1; the run log holds `run trunk main`; `not
    hasattr(ol, "trunk_name")`.
  - **Fails before:** the kit reader was never called (count 0), and the
    launcher had its own `trunk_name`.
- `test_a_refusing_trunk_reader_stops_the_run_before_any_leg` (D5)
  - **Setup:** `agent_common.trunk_name` raises `ValueError("trunk
    undeclared: probe")`.
  - **Asserts:** exit 2, no leg record, and the message in the log.
  - **Fails before:** the launcher never called it, and the legs ran.
- `test_a_bound_name_no_local_branch_holds_stops_before_the_leg` (D6; a pin)
  - **Setup:** the reader returns `"HEAD"`.
  - **Asserts:** exit 3, no leg record, and the stop names `refs/heads/HEAD`.
- `test_check_lane_from_the_lanes_own_worktree_judges_from_the_kits_trunk`
  (D7)
  - **Setup:** `marked_lane(repo)`, then `git worktree add <tmp>/lane wi-1`;
    `check-lane wi-1 --repo <tmp>/lane`.
  - **Asserts:** exit 3, naming `lane work 2`.
  - **Fails before:** trunk was the worktree's HEAD, `wi-1`, an empty range,
    so it printed `passes (window 0)` with exit 0.
- `test_the_leg_log_line_names_the_bound_trunks_pre_and_post_leg_tips`
  (D14; a pin on real git)
  - **Asserts:** the `leg 1 exit 0; trunk X -> Y` line carries main's tips
    before and after leg 1.

**IN tests** (D15: each new rule pinned in the smoke tier).

- **The checkout.** `test_the_checkout_must_stay_on_the_bound_trunk` is
  parametrized over the `name` site:
  - `refs/heads/elsewhere`: names `elsewhere`;
  - `(1, "", "")`: detached;
  - `ok("garbage")`: unparseable;
  - FAILED: names `symbolic-ref`.

  It runs both through `pre_leg("repo", TRUNK)` and as the audit's last
  judgement. A refused trunk commit with an off-trunk HEAD names the commit,
  not the branch, which proves the order. Fails before: `pre_leg` took the
  checkout's branch as trunk, and the audit never compared it.
- **A name no branch holds.**
  `test_a_snapshot_without_the_bound_trunk_stops_before_the_leg` (a pin).
- **The bind.** `test_the_bind_reads_trunk_once_and_a_value_error_stops_the_run`
  - **Setup:** `prepare_run(repo)` with the counter or the raising reader.
  - **Asserts:** `run trunk main` is logged, or exit 2 with the message.
  - **Fails before:** `prepare_run` takes no repo and binds nothing.
- **`check-lane`'s reader.**
  `test_check_lane_cannot_judge_when_the_trunk_reader_refuses_or_names_no_branch`
  - **Setup:** a `ValueError`, and a name whose `rev-parse --verify` fails.
  - **Asserts:** exit 3, "cannot judge", and the reason.
  - **Fails before:** `check_lane` never called the kit reader.
- **The log line.** `test_the_leg_log_line_prints_the_bound_trunks_tips`
  - **Setup:** `run_and_audit` with `run_leg` stubbed to 0 over `FakeGit`.
  - **Asserts:** the line ends `A[:8] -> B[:8]`.
  - **Fails before:** it printed `rev-parse HEAD` from a real `git` on
    `"repo"`, which is empty.
- **Updated helper.** `audit_with` calls `ol.pre_leg("repo", TRUNK)` and
  `ol.audit(...)`, now unpacking `(summary, post)`. The existing `name` row
  of `test_every_failed_audit_read_stops_the_run_naming_the_read` keeps
  passing, because the checkout read is still `symbolic-ref`.

### P5: the archive's descent

**The stub actions.**

- `archive_rewind`: `update-ref ARCHIVE ARCHIVE~1`.
- `archive_reset_unrelated`: `update-ref ARCHIVE <a marked commit-tree whose
  parent is trunk's HEAD>`, so the archive does not descend from its old
  tip, and its one new commit is marked so that the code before the change
  passes it.
- `archive_delete`: `update-ref -d ARCHIVE`.

A setup helper `archive_two(repo)` writes two archive commits before the run.

**GIT tests.**

- `test_a_leg_that_rewinds_resets_or_deletes_archive_lanes_stops_the_run`
  (D8), parametrized over the three actions.
  - **Asserts:** exit 3, one record, and the stop line names the pre-leg
    archive tip's `[:10]`.
  - **Fails before:** each logged `0 commit(s)`, `1 commit(s)` or `deleted
    (logged, not judged)`, ran leg 2 and exited 0.
- **Pins:**
  - `test_a_marked_archive_commit_on_an_existing_archive_runs_the_next_leg`
    (D10): `archive_two` setup, plan `archive_marked`, exit 0, two records;
  - the existing `archive` case of
    `test_a_leg_that_adds_an_unmarked_foreign_or_rewinding_trunk_or_archive_commit_stops_the_run`,
    together with the existing all-marked case, which creates the archive
    (D11), marked as pins in comments.

**IN tests.**

- `test_the_archive_must_descend_from_its_pre_leg_tip`, parametrized:
  - an archive-descent answer of `(1, "", "")`: names `C[:10]`;
  - an archive absent from the post snapshot with `PRE` holding it: names
    `C[:10]`.

  Fails before: there was no descent read, and a deletion was logged.
- **The creation pin (D11).** The existing `archive-absent-before` case,
  marked as a pin.
- `test_a_failed_archive_descent_read_stops_the_run_naming_it` (D12; a pin
  per the spec's list)
  - **Setup:** the archive-descent site answers FAILED.
  - **Asserts:** it names `merge-base` and `exit 128`.
  - **Before the change:** the archive arm had no such read.
- **The FakeGit change.** `FakeGit.site` splits the `merge-base` site:
  - `archive-descent` when the args carry the archive's pre-leg tip `C`;
  - `descent` otherwise.

  The existing `descent` row (trunk's rewind) keeps naming `A[:10]`.

### P6 to P9

- **P6 (docstring).** No behaviour, so no test. The P4 and P5 tests are the
  stops' evidence, and the reviewer judges the text against the spec's
  `## Trust` bound and Stops list.
- **P7 (skill).**
  - The clause goes in the kit source only. Then sync, and confirm the three
    copies are byte-identical.
  - `test_the_block_opens_with_the_marker_check_and_the_skill_section_links_it`
    keeps passing, since §7's heading and link are unchanged.
  - `scope: this-repo`, so no RESYNC entry.
- **P8 (spine).**
  - **The edits.** The lane edits `docs/requirements/low-level-requirements.toml`
    (LLR-248), `docs/test/test-cases.toml` (TC-242) and
    `docs/requirements/interfaces.toml` (IF-065). The rows are byte-exact
    TOML, edited per cell.
  - **The checkpoint.** The sitting judges LLR-248 and TC-242. Its act is the
    adjudicator's, since the dial releases those rungs, taken through the act
    turn after the lanes ahead have landed.
  - **TC-242's evidence cell** is unchanged (`tests/test_loop_provenance.py`
    already).
  - **Flag for the coordinator.** LLR-248's `code_symbol` cell does not name
    `_loop_claimed` today
    (`_claim_locked/_mint/commit_telemetry/_loop_trailer_refusal/_commit_object/LOOP_WRITER_SUBJECTS/loop_writer_commit/loop_lane_window`).
    So "in place of the slot's copy" is in practice an addition of
    `loop_claimed`. The plan adds it and removes nothing. If WI-918 lands
    first and changes this cell, the rebase merges both.
- **P9 (the bar).** Its outputs are pasted, not claimed.

## Ordering and the WI-918 overlap

- **The commit order** is P2, then P3, then P4, then P5, then P6 and P7, then
  P8.
  - The extraction is alone in its commit (S1).
  - The launcher's commits follow the checked reader, so that `lane_claimed`
    is deleted once, onto a reader that already fails closed.
- **WI-918 runs in a parallel lane.** It touches the same areas:
  - `integrate._loop_window`'s neighbourhood;
  - LLR-248 and TC-242;
  - skill §7;
  - the launcher's `lane_refusal` window call.

  Whichever lands second rebases onto the first and re-sits the shared spine
  rows (spec S6). This row changes only the claim read inside `_loop_window`
  and `lane_refusal`, and leaves the window call (`loop_lane_window` and its
  inputs) to WI-918.
- **No migration is forced downstream.** The slot refuses only where git
  cannot read the claim log.
