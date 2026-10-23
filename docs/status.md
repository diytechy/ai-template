<!--
Contracts: IF-163 — the interface seam this file declares (process.md §8; row of
record in requirements/interfaces.toml).

Contract IF-163: the forward-only blackboard's HAND-AUTHORED bytes — everything
    outside the GENERATED STATUS marker pair — read as data by the kit's checks
    and by a resuming session; the block between the markers is its writer's
    own row. Markdown with `##` sections: `## Current State` is the section a
    stopping coordinator excerpts into its exit banner (the generated block
    rides inside that excerpt as the writer's bytes). Only what must happen
    NEXT belongs here — what already happened lives in log.md — so a work-item
    id recorded closed must not appear in the hand-authored prose, and a claim
    naming one there is refused; inside the generated block that rule stands
    down, because the generated frontier legitimately names queued ids.
-->

# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself. **Forward-only**, held to
the declared S-1 budget (`docs/status-lint`; raised 2026-08-31 to carry the
supervisor prompt at the owner's request). Backward-looking homes:
[log.md](log.md) (sessions, verdicts, **Decisions**), [open-items.html](open-items.html)
(the generated **Open items** owner surface), [docs/work/](work/) (the WI registry —
status = directory; terminal rows under [archive/work/](archive/work/)),
[archive/](archive/README.md), and the folder map [docs/README.md](README.md).

- **RESUME HERE:** start with the coordinator's
  [handoff-2026-10-22d-leg14-coordinator.md](handoff-2026-10-22d-leg14-coordinator.md),
  run in **headless legs** under the overnight launcher (the handoff
  carries no stop line). The owner ruled the review-churn program
  ([plans/2026-10-11-review-churn/](plans/2026-10-11-review-churn/README.md):
  every call is ruled; read its Status, then its rulings). The batch's
  process-text, strict-lints and plan-gate landing-shapes rows have
  landed, and the reviewer trial has ended: each round runs two reviewers,
  Sol and Opus. The adjudication split has landed: a checkpoint sitting
  now ends at its committed verdict, and its act is a later turn
  (`coordinator_adjudicate.py act`), and the machine-line reader row has
  landed through it. No bar fails on the
  smoke tier's seconds: the bars report its CPU-seconds and wall, and
  `run.cmd audit` judges them and its count (owner, 2026-10-20).
  The re-sync entry check is in the commit bar: a lane rebased onto a
  newer trunk re-anchors its own RESYNC entry at its new base.
  The headless coordinator's marking row has landed, and the guard-hooks
  row has landed, and so have the bless-mark row, the re-claim reader
  row, the launcher's follow-ups row, the trunk-by-name row (the trunk
  is now the branch `docs/process.toml` declares) and the hooks-on row
  (every agent route refuses a checkout whose commit hooks are not on),
  and the guard hook's per-call cost row (its PreToolUse group runs only
  for the launch and shell tools). The two merge-slot rows are claimed; their
  coordinator-landing gap is the one-landing row's
  (owner, 2026-10-17). The
  disposition-adoption row's successor has landed on the owner's route: a
  disposition can adopt an already-filed successor, recorded at the close
  and judged by one commit check that admits the close's exact relinks
  (the hook's `adoption-record` step). The trunk mint's settled-amendment filter
  (the first new build, owner, 2026-10-20) passed its checkpoint and
  holds at its gate for the owner (OI-115: its ruled fix needs the act
  ledger to record what each act copied), and the lane
  lifecycle design's in-lane mint and station authority rows are
  cancelled, its config-retirement row folded into item 10's program. The
  account-homes row has landed: the adjudicator runs on its declared
  token account through a qualified entry. The review gate's queue row is
  filed as four rows: its text row (test cases before the code in a lane)
  and its attestation row (one tree-bound bar attestation, and the
  `attest` verb) have landed, and so has the coordinator's review refusal:
  a review brief renders only over the tip's attested review bar
  (`attest` runs from the primary checkout and finds the lane by branch).
  The loop's refusal (with its red-round cap) has landed: a loop review is
  drawn only over an attested tip, and `[build] red_rounds_max` closes a
  lane red that long partial.
  The lane lifecycle design's remaining rows are deferred until the owner
  reviews their re-scopes, and the queue table is an explicit list. Item 8's usage
  record is filed as two rows (the coordinator's Sol and Terra calls
  through the session service, then the Claude sub-agent usage ingest);
  the first has landed: every Sol and Terra call goes through one
  coordinator entry point on the session service, and a call outside a
  claimed lane spools its log and commits nothing; the second has landed
  too: each close-out records its session and every sub-agent, at any
  depth, from their transcripts. Item 10 step 2's row (the
  hooks' one policy read) has landed, and its shape-rule retirement row
  is filed.
  The coordinator's procedure lives in the `coordinator-cycle` skill, its
  headless legs in its section 7. The owner directed (2026-10-18,
  coordinator-2026-10-18 D-004, D-006) that the queue turn toward headless
  runs: its two gate rows, the re-claim reader row and the launcher's
  follow-ups row, have landed, so the handoff carries no stop line, the owner
  starts the overnight launcher (`scripts/coordinator/overnight_legs.py`),
  and the rest of the queue runs in headless legs, continuing the lanes
  claimed attended with no re-claim.
  Delegated decisions take the owner's verdict as `owner = "confirmed"` or
  `"overruled"`; entries not yet seen, high-risk first, render under "Decisions
  to review" in [open-items.html](open-items.html), and an overrule must change
  open work citing it in the same commit.
  Approval acts run to seq 152 on trunk. The context guard's hooks are machine-local
  (installed through dev-setup's consented offer, or at a lease take run at a terminal; this
  workstation is on), and the guard is live where they are: take the coordinator
  lease (`coordinator_guard.py take`) before any claim, and hand it back
  (`coordinator_guard.py handback --handoff <path>`) as the close-out's last act.
  Every adjudication sitting now authenticates with the owner's long-lived token:
  set `AGENT_CLAUDE_TOKEN_FILE` to its path before `coordinator_adjudicate.py`.
  0. **The handoff's queue table in order:** the program's first batch,
     then the lane in flight (claimed, on its branch; the handoff names its
     returns), then the phase-1 rows.
     Review rule (owner, 2026-10-11, superseding 2026-10-07): no narrow rounds.
     Each round runs two full-lane reviewers in parallel (Codex Sol and
     Claude Opus; the three-reviewer trial ended 2026-10-16), at most three rounds, with a dispute sitting at the cap; the
     handoff states the rest. Review threat model (owner,
     2026-10-08, PROCESS.md §6): a finding that needs a compromised or
     contrived host is dismissed in one recorded line; a contested or
     third-round finding goes to the coordinator's `dispute` sitting
     (`coordinator_adjudicate.py adjudicate --brief dispute`), whose ruling is
     final.
  1. **Build the S788-* successor rows** of the approved design note
     ([plans/2026-10-04-wi788-design/README.md](plans/2026-10-04-wi788-design/README.md),
     its ruling section first; it overrides the chapters), in their `needs`
     order with the wave-11 cycle, claiming each batch under one scoped unpause.
     The generated ready frontier below lists the rows that can start; the
     handoff names them. The owner directed (2026-10-04) that this campaign
     runs by coordinator session, not the unattended loop. OI-105 (the
     FreeLLMAPI endpoint and pinned models) waits for the owner's router; it
     holds only the FreeLLMAPI row of S788-routes.
  2. OI-98: the owner re-syncs `C:\Projects\FileBackup` (stamp `9b697cc`) as a
     scratch trial, after TC-036's inputs gain `RESYNC_PACK.md`, then rules it.

  `docs/work/pause` is still tracked (since 2026-09-04): the unattended
  dispatcher claims nothing until a reviewed commit deletes it, so work is
  taken by a coordinator session, not the loop. Owner direction 2026-10-04: a coordinator
  session claims its whole batch of rows under ONE scoped unpause (a reviewed
  deletion commit, the claims, then a byte-identical restore), not one per row;
  the control ruling's pause deletion is not spent. The roles (owner, 2026-10-04): Claude Opus builds and plans at medium
  effort and the coordinator commits for it; GPT Terra (`gpt-5.6-terra`,
  medium) authors spine rows; Codex 6.1 (`gpt-6.1-sol`, high) reviews code
  through the CLI; and an independent Opus agent adjudicates and resolves
  disputes. File new work as a row; an open item is filed together with the queued
  placeholder row whose `needs` cites it, and the commit that rules it updates
  that row's Done-when (OI-102). The reviewers' `codex exec` launch
  runs under a temporary `Bash(codex exec *)` allow rule in
  `.claude/settings.local.json` (owner, 2026-09-28): remove it when the
  queue drains. Recheck Git and the generated frontier before choosing
  work; earlier handoffs are historical context.
- **Assumption tier — C1 and C2 have landed and are approved:** the
  redrawn frame, checkpoint re-judging of observation tests, the assumption
  gate's four steps (behind `[checks] assumption_gate = false`), and C2's
  assumption and surrogate rows with every SR's bridging. The owner signed
  the assumption ruling on 2026-10-02: an assumption carries status and standing
  only, falsification is the one signal, and there is no evidence ladder, so
  C3 shrinks to the falsification route and C5 loses its evidence arm. OI-97's joint-delivery class has
  landed and is anchored.
- **Sister plan — one plan still owed:** every question in the
  [notes on spine, sessions and tests](plans/2026-09-23-owner-notes-spine-sessions-and-tests.md)
  §5 is ruled except S11. The owner said yes to adjudication inside the lane
  (2026-10-03): a return is fixed in the lane, not minted as a follow-up row.
  Its plan, with S9's reviewer-commit check, is
  [plans/2026-10-03-s11-in-lane-adjudication.md](plans/2026-10-03-s11-in-lane-adjudication.md).
  Its §6 questions are ruled as recommended (owner, 2026-10-03, recorded with
  OI-101 Q6). Hand integration already follows it (owner direction 2026-09-28): one
  squash commit per item, with lane tips kept reachable in `archive/lanes`. S7's session service has landed, writing S8's adopted OTel schema, with
  retention shipped off; its live verification closed 2026-10-03 (a real adjudication peaked at 44% of the codex window), and the dial stays off. S6 is designed
  with the assumption tier before its C3. S14's flag-axis count and
  duplicate-detection research have both landed.
- **Control launch:** retain the tracked `docs/work/pause` while preparing
  route-complete spending bounds, including in-flight drain, against the
  [settled control ruling](ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06).
  Revalidate the [preflight](ai-template-redesign-2026-09-05-codex/CONTROL-PREFLIGHT.md)
  at the proposed frozen launch commit, then obtain the ruling's owner-reviewed
  pause deletion. Replacement packages follow the control's evidence decision.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). The held wi508
  branch is on origin; the queued wi508-partial-close row is the only
  sanctioned act on it (`OI-71`).
- **Standing constraints:** the depth-0 frame is **LOCKED and APPROVED** (4
  entities · 4 crossings · 3 relationships, watermark-held); `OI-61` (c) stays deferred
  on its condition (a demonstrated residual drift class), not owner-owed.
- **Unfiled follow-ups** (topics, no ids): from the disposition-adoption
  successor's gate (wi-969 D-027): the mint's LLR lacks the adoption SR in
  its SR refs; the close's LLR and the disposition prompt still say
  continuing partial work mints a successor, unqualified beside adoption;
  three TCs' expected text should name the adoption SR clause each
  discharges, one citing the record LLR without a verifies link; the
  Dispositions census selects files by the exact heading where the parser
  reads the first prefix; the record step refuses a commit that only
  writes an unreadable spec with no record question live. From the CPU-time budget
  row's gate (wi-940 D-011): its archived spec's two delta sentences say
  TC-026 verifies IF-302 where TC-374 does, the root conftest comment and
  pytest.ini still state a 60 s wall bound, the shipped job module's
  docstring names this repository's own step by path, and its deliverable
  3 says max-tests is unchanged where the lane re-stamped it (wording);
  from the settled-amendment filter's lane (wi-963 D-007, D-010): a ledger
  malformed at a range's before revision leaves no sweep that recovers
  the range, and two ledger readers repeat one seq rule (with OI-115);
  from WI-968's drafter: the bookkeeping and lane harness reads have no
  floor of their own and fall back to the ambient interpreter when a
  pinned repository has no .venv; the wave-11 log's follow-ups (the claim
  reads the working-tree pause; an in-lane act never meets the held-rung
  re-attestation refusal; a refresh merge must carry a citer's update for a
  trunk ruling); the wave-9 log's session-close list (removed approved rows mint no adjudication; six batch-R row-text residues); the stage-ladder program's deferred
  codex round; the SN-036 coverage record (re-derive — basis reads
  `uncovered=0`); the archived [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md)
  findings; the [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md)
  residues (§7 items 2/4/5 need a destination); whether the `ruling-sync`
  and `held-status` hook riders share the hand-merge shapes the plan gate's
  contract now states as residue (text-then-act's is accepted by its
  approved requirement; owner, 2026-10-15); from the process-text row's
  last gate (wi-911 D-020): PROCESS.md §3 still places a concrete filename
  in an SR's acceptance as carrier evidence, against ruling 5's text in
  `spine-questions.md` (to plan item 5's schema lane), and SR-233's
  acceptance states convergence duties its requirement does not (wording,
  at its next sitting); from the landing-shapes row's first round (wi-922
  D-005): LLR-337's rationale reads wider than the residue the plan gate's
  contract states (wording, at its next sitting); from the bar row's gate
  (wi-935 D-005): CLAUDE.md, the session-protocol skill and the budget
  script's docstring date OI-52 ruling (a) 2026-08-23, its wiring date,
  where the record reads 2026-08-21 (wording, in all three together);
  from the session-kill row's gate (wi-931 D-009): SR-238's acceptance
  clause on a process that joins the session job late in the kill has no
  verifying TC clause (wording, at its next sitting: keep it in the
  rationale's residue, or name its verification in TC-026); from the
  adjudication split's lane (wi-912 D-013): the intake module's minted
  first-approval and amendment rows'
  Context still tells the judging session to act in-turn (to the row that
  builds the loop route's act turn); the judging composer's first-approval
  comments still describe the removed `--approves` slot; LLR-167's detail
  still says its tiers come from that walk, and an "it" in its addition
  lacks a referent, and SR-231's new act-turn sentences sit outside its one
  `shall` (wording, at their next sitting); from the merge-slot rows'
  drafting (their specs' S5 and Trust): the held-rung act rule has two
  homes, three readers map a row id to its registry over two tier sets,
  and an act ledger deleted alone is admitted on a scope-bound lane, which
  no kit route reaches; from the re-sync
  check's gate (wi-916 D-008): the enforcement audit's row and the
  check's docstrings say a retitled entry counts zero, where one keeping
  its old anchor is refused by the anchor rule, and a lost landed heading
  that cancels a valid added entry is refused with the plain no-entry
  reason, naming neither (wording, and a clearer message); from the guard-hooks row's
  fix round (wi-927 D-007): a shipped coordinator-hook example holding JSON
  null reads none, which its Trust section does not rule; from the same
  lane's POSIX run: two `run.command` cases in the dev-setup tests fail on
  POSIX at trunk itself (a bare run's check order and interpreter); from
  the guard-hooks row's gate (wi-927 D-012): a take run from a lane
  worktree reads the hooks under that worktree, not the primary checkout's
  where the lease lives, so it refuses naming the lane's file; TC-345's
  `verifies` cites SR-237, which none of its cases exercises; LLR-322's and
  TC-345's "all missing guard events" understates the absent reading, which
  also covers events present and empty (wording); and the take's hooks
  refusal is stated in both LLR-300 and LLR-322 (cross-refer at the next
  amendment of either); from
  the trunk-by-name row's build: a spec move rewrites the moved spec's own relative links, so a
  row whose Done-when holds one reads as changed at its own close; and the
  dispatcher may keep looping on a worker that refuses at preflight;
  from the guard-hooks row's second fix (wi-927 D-009): bootstrap's setup
  prompt reads a NUL stdin as a terminal on Windows (harmless: it takes the
  default); nothing checks an LLR's code_symbol entries back against the
  tags, and trace.py does not compare a TC's `verifies` with an LLR's
  `test_refs` (so `--strict` missed a back-link gap); the occupied fix text
  also prints for an unparseable settings file or a broken shipped example;
  a crashed hooks reader's `[missing]` line carries only its traceback;
  from the trunk-by-name row's gate (wi-925 D-011): TC-369's expected joins
  an existing policy file's preservation to the no-repository and detached
  defaults, where the scaffold leaves an existing file's trunk alone and
  prints no note, and TC-206's method still explains its single-checkout
  fixtures as their own trunk (wording, at each row's next sitting);
  LLR-307's bound and the shipped hook's heading call all seven fail-open
  items routes outside the supported ones, where three are shapes inside
  them (wording, in both homes together); from its fix round (wi-925
  D-008): with the trunk undeclared, the readability report skips a
  measure the profile declares gating (LLR-256's exit contract), and the
  plan record repeats a schema comment's corrected reason;
  from the hooks-on row's gate (wi-926 D-014): IF-194's notes and IF-197's
  rationale still say the commit-msg hook reads the loop marker to fail
  closed, where it now reads none and refuses every commit without the kit
  scripts (wording, at each row's next touch); the row's archived
  Done-when says a missing or non-executable hook's refusal names the setup
  command, where the code and the approved SR-240, LLR-340 and TC-370 name
  the repair for that cause; TC-370's evidence omits four existing check
  cases (the `.git/hooks` path, an empty hooks path, a directory that is
  not a work tree, a linked worktree on the main worktree's absolute
  `.githooks`; traced-only, at its next touch); and LLR-140's and
  LLR-300's test_refs do not list TC-370, which now verifies both;
  from the bless-mark row's gate (wi-943 D-007): the act module's
  docstring still calls the merge slot's checks unchanged, where they now
  read the same judged-rows reader (wording); TC-278's method claims the
  two-way-tagged refusal through a named verdict as well as through the
  backing check, and its evidence covers only the backing check (add a
  named-verdict case to the two-ways test, or narrow the sentence);
  from the re-claim reader row's gate (wi-918 D-008): the lane window's
  state advances in log order, not along ancestry, so in a loop lane
  holding a lane-local side line merged back in, an unmarked side commit
  that does not descend from the re-claim is exempted (no kit route
  merges such a line; derive each record's state from its parents');
  SR-209's rationale still says the floor judges every commit of a loop
  lane and gives no reason for the re-claim exception (wording, at its
  next amendment); IF-194's data spells three names in brace notation,
  so a search for them misses the row, and nothing forced it: the
  160-character data rule is a warn-first advisory (spell them out at
  the row's next touch);
  from the launcher's follow-ups row's gate (wi-946 D-012): LLR-246, the
  held-status rung's row, does not state that the rung refuses a lane
  whose claim cannot be read, which it inherits through the slot's
  window read (wording, at its next amendment: add the sentence or
  cross-refer LLR-248); and from its sitting: TC-242's method says "a
  loop lane whose claim record cannot be read", where an unread claim
  cannot show the lane is the loop's (wording, "a lane", at its next
  sitting);
  from the guard hook cost row's gate (wi-897 D-007): IF-261 (the policy
  file's readers) still names only `scripts/agent_common` as requestor,
  while `session_keep` and `coordinator_guard` now read it directly, and
  `agent_policy`'s contract text still says `agent_common` re-exports it
  (add the two requestors at the row's next touch); and the traced-only
  re-anchor recipe names the sitting that last anchored each registry as
  the refresh's ref, where the snapshot README's rule reads as asking for
  the lane's own WI or no entry (wording, in the recipe or the README);
  from the account-homes row's gate (wi-798 D-024): IF-246 and IF-282
  list a `route_runner(entry)` the session service does not define, and
  IF-044 omits the route module's `route_runner(template, model)`; IF-248's
  notes still say the keep module creates account homes; the row's
  Implements tags name SR-222 beside LLR-336, which traces to SR-154 and
  SR-227 only; LLR-305's compose_env sentence reads unconditional, where
  the withholding applies under a declared account; `docs/process.toml`'s
  adjudicator comment says the loop draws the unqualified route, where a
  heterogeneity-filtered draw or a win-stay pin picks the weight-0
  adjudicator entry when the ambient Opus route cools (wording, at each
  row's next touch); and SR-227 still binds its credential clause to a
  family with a dedicated home (the owner's wording, at its next
  amendment);
  from the attestation row's rounds and gate (wi-956 D-002, D-004, D-006,
  D-010): `attest`'s review-bar step puts the interpreter's directory first
  on PATH with only the Windows half of the run menu's interpreter rule
  (one home for that rule, moved into kitlib, which both read); the named
  tests step appends pytest's `--basetemp` to whatever `[product] test`
  declares, so a non-pytest adopter's `attest --tests` is red (the
  spec's own mandate; the owner's call: a declared placeholder, or a
  pytest-only note in the template); LLR-247's traced `code_symbol` gained
  `append_trailer` without the spec naming that amendment (wording);
  `handback.py`'s lane resolution repeats the primary-checkout refusal
  `_lane_off_trunk` now owns; and several `git status --porcelain` reads
  (`integrate.py` `_worktree_dirt`, two in `agent_common.py`, one in
  `bootstrap.py`) do not pin `--untracked-files`, so a user's
  `status.showUntrackedFiles = no` hides untracked files from them;
  from the hooks' one-read row's sitting and gate (wi-962 D-006, D-007):
  LLR-021 lists the five hook answers in prose where LLR-031 defers to
  IF-298, and LLR-031's kept opening sentence still names the hooks
  (wording, at each row's next sitting); TC-021's evidence omits the
  pre-push case for a scripts directory found nowhere, and TC-031's method
  says every hook drives the adversarial table, where pre-push drives it
  and all three drive the refusals; SR-031's rationale still speaks of two
  readings pinned equal; the RESYNC entry omits that a
  `privacy_check = false` the parser places outside `[policies]` now
  reads ON at pre-push; Flow 3 draws the scripts-directory refusal after
  the probe's call, where the probe refuses before it; and one loader for
  the policy file would serve `check_privacy`, three `kitlib.config`
  reads and `agent_policy.read_toml`, which repeat its read-parse-catch
  (a consolidation row);
  from the coordinator review refusal's gate (wi-957 D-014): SR-241's
  acceptance states no search depth, while LLR-341 and TC-371 refuse
  when no record lies among the first 64 commits examined (wording, at
  SR-241's next amendment: state the bound or cite LLR-341); and
  `test_a_search_past_the_walk_bound_refuses` stacks two commits past
  the 63, so the record is the 66th examined and a 65-commit walk still
  passes (stack one, and TC-371's method reads "63 and then 64");
  from the red-round cap row's rounds and gate (wi-958 D-012, D-017): a
  rebase re-counts reds a verified green had reset, since the reset reads
  sha ancestry and a rebased attestation stops verifying (fails closed;
  date each red by the commit that added its log); `handback.BOOKKEEPING`
  repeats `kverdict.RECORD_PREFIXES` by hand (derive it); an undeclared
  `[bars] review` is found only after each build and spends the cap
  (refuse it at both preflights beside the cap's read); `kitlib.config`'s
  key locator repeats `agent_policy`'s section walk and
  `bootstrap._locate_process_key` (one locator); SR-154's escalation
  clause and SR-242's cap overlap for a red rebuild run, and the row's
  archived spec Anchor and SR-241's rationale still name SR-241 as the
  loop LLR's parent, where LLR-344 is derived under SR-154 (wording, at
  each row's next amendment);
  from the Sol and Terra route row's rounds and gate (wi-960 D-006,
  D-009, D-011, D-016): the shipped gitignore template still leaves the
  adjudicator store, the coordinator lease and the review-owed marker
  under `out/` unignored, while an older RESYNC entry says a stock
  scaffold ignores all of `out/`; the coordinator entry point's
  working-tree snapshot and range walk repeat `bookkeeping`'s and
  `retire`'s blob readers and `text_then_act`'s and `kitlib.verdict`'s
  walks, and the service's trunk-side claim read copies
  `integrate.claimed_ids_on_branch` through two private names (one
  public reader taking a ref); `record` reads `commit_telemetry`'s
  nothing-committed result as committed; the change check records HEAD's
  commit, not its symbolic ref, so a call that leaves the lane on another
  branch at the same commit reads clean; `session_service.lane_branch`
  shares its name with `agent_loop.lane_branch`; a plan critique run in a
  lane now leaves a telemetry commit between the plan records, which the
  recipes do not mention; LLR-269 keeps its keep-only session-mode
  sentence, LLR-346 says the call launches under the route's sandbox and
  effort where the entry point declares its own template, and SR-243
  names the roster's Sol and Terra rows (wording, at each row's next
  sitting); and the RESYNC entry should say that a `--wi` worker on the
  primary checkout, even on its claimed branch, now spools its BUILD,
  ATTEST and REVIEW logs, so the loop's committed-evidence readers see
  none (whether a `--wi` preflight refuses the primary checkout is the
  owner's call);
  from the sub-agent usage ingest's gate (wi-961 D-017): the adapter's
  `_is_count` repeats `_count`'s non-boolean-integer rule, and `_thinking`
  re-spells `_count` (delete `_is_count`); the reader accepts any string
  timestamp, and one `transcript_time` cannot parse crashes the command
  at its stamp step naming no file, against LLR-352's per-file refusal
  (validate it in the reader's shape check); `recorded_logs` counts an
  untracked log in a lane worktree's iteration directory as recorded, so
  after a refused lane commit a rerun reads unchanged (only with `--root`
  on a lane; the published route spools); `usage_ingest._header` repeats
  `codex_call._classify`'s cut-short-header refusal over the same log
  grammar (one strict header read beside `log_meta_text`); and SR-244's
  'record once each session' reads against a resumed session's several
  contributions, which its acceptance resolves (wording, at its next
  amendment);
  from the parent-first row's Trust draft (coordinator-2026-10-22 D-002):
  `acceptance_record._spine_rows_at` and `rows_at` read an unparseable
  registry or a failed `git show` as an absent one, so on such a tree the
  staged approval-act, amendment and drafted-row readers and
  `check_test_first._members` pass; `registry-integrity` backstops it on
  disk, leaving a direct trunk commit whose index alone holds the broken
  registry (its own row); and the Approved-or-Founded pair is restated in
  six modules (one home in `kitlib.spine`);
  **owner intake 2026-09-22:** the self-test
  suite should fail fast when its dev toolchain is missing, and name the run
  menu's setup action as the fix. Today a missing pytest-xdist dies on
  `unrecognized arguments: -n`. This depends on the root launchers SN-034/SN-035
  require, which do not exist yet, and needs stepping through as a requirement
  before it is built.
- **Conventions:** [specs/README.md](specs/README.md) · [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-Impl** (stage 7 of 8, implementation in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-Impl;6=DevStg-Impl`, derived current **phase=6**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=31 SR=136 LLR=323 TC=350** (21 drafts) · 254 seams · 4 components.
- **Open items** _(the pending rows of [requirements/open-items.toml](requirements/open-items.toml) a queued work item cites; each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-98** — The owner must perform the re-sync from 2026-10-03 and rule this item to release WI-684. _(holds WI-684)_
  - **OI-105** — When the owner's FreeLLMAPI router is running, name its endpoint and the models to pin, and confirm it holds a one-model chain per pinned id, so the FreeLLMAPI route row can ship and take its one live call. _(holds WI-795)_
  - **OI-115** — Choose how WI-963 closes its gate's ruled FIX, whose only sound remedy needs the act ledger to record the registries each act copied (outside the row's surface); recommendation (a), a preparatory row for the ledger's producer, landed first. _(holds WI-967)_
- **Decisions to review:** 824 — [open-items.html](open-items.html#decisions-to-review)
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-920** — re-judge TC-055: declared trigger fired [sha256:5bdf43dafa30] at merge b803dd0
  - **WI-971** `P6` — The adoption-record step reads lane commits and work specs through the shared walk and li…
  - **WI-851** `P5` — Held-rung spine rows are protected by state: the registry, the snapshot and the dial
  - **WI-850** `P5` — A spine row is approved only after the rows it hangs from are
  - **WI-966** `P5` — The policy file's one-key-per-line shape rule retires: the hooks read it through one pars…
  - **WI-878** `P4` — A dispute sitting's binding records the findings file it ruled, and the coverage gate rea…
  - **WI-856** `P3` — A queue-with-edge verdict edges a waiter filed without a needs line
  - **WI-827** `P3` — Owner signs SN-029's amendment after text-before-act
  - **WI-908** `P3` — Owner-assisted Claude login-isolation check: two account homes on Windows show two logins
  - **WI-910** `P2` — The full suite is green on macOS: the run.command fixture runs an executable run.sh, and…
- **Blocked** _(held by a pending open item its `needs` cites):_
  - **WI-684** — re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093 — [OI-98 — Owner re-sync from 2026-10-03](open-items.html#OI-98)
  - **WI-795** — Owner provisioning: the FreeLLMAPI endpoint and pinned models — [OI-105 — FreeLLMAPI provisioning: the endpoint and the pinned models](open-items.html#OI-105)
  - **WI-967** — OI-115's ruling: route WI-963's settlement fix — [OI-115 — WI-963: settlement the act ledger cannot prove on a squashed landing](open-items.html#OI-115)
<!-- END GENERATED STATUS -->

- **Bar (per commit)** and the **standing rules** (claim refusal on prose ids,
  never sanction a check to green a step, line-ending hygiene, claiming through
  the integrator): the `session-protocol` skill §2–§3. Run
  `check_trajectory.py --strict` unfiltered before claiming anything done;
  route a critique dispatch by PROVIDER, probing first.
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working rules
  [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · lock items
  [repo-lock.md](repo-lock.md) · external (not this repo's work): guardrails
  content in `TheColliny/FableClaudeMDForOpus`.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the `PROJECT-VISION:`
  tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only, Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the kit's
  "product" is `project-trajectory/` + `tests/`; an actions-menu launcher is in
  scope, a `run.*` product launcher is not. No scaffolded `docs/process.md` (the
  masters live in `project-trajectory/`).
