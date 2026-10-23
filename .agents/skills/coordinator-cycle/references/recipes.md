# Coordinator recipes

The exact commands and the traps behind each step of the coordinator cycle
([../SKILL.md](../SKILL.md)). Example paths assume the primary checkout
`C:/Projects/ai-template`, with lanes and scratch in its sibling folder
`C:/Projects/ai-template.wt/`. The coordinator tools are this repository's own
`scripts/coordinator/` (not shipped; their README documents part of them), and
they derive these paths from their own location.

Use **Git Bash** for the commands below. Run kit commands from the checkout
being operated on: trunk for claims/landings, the lane for authoring and
adjudication. Substitute placeholders, and set these in each shell. `REPO` is
the primary checkout from any lane, so nothing names a machine:

```bash
REPO=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
PY=$REPO/.venv/Scripts/python.exe
TOOLS=$REPO/scripts/coordinator
SCRIPTS=project-trajectory/scripts
```

Contents: 1 Invocations · 2 Claiming · 3 Landing · 4 Rebasing ·
5 Spine-cell edits · 6 Commits and hooks · 7 Environment and limits ·
8 Re-judge and consolidation recipes

## 1. Invocations

- **Builder:** the Agent tool with `subagent_type: "kit-builder"`, given the
  lane path and the build prompt. If the type is not listed, use
  `general-purpose` with `model: "opus"` and have it read
  `.claude/agents/kit-builder.md`.
  Override that file's old scratch recipe with the dated root in §7. Grant
  trace-cell upkeep only during iteration; require the spine change list,
  the coverage plan before fixes and the stop-and-file rule for consolidation
  outside the spec's surface in every build brief. Re-run the builder's
  claimed results before committing: one builder has reported a smoke result
  it never produced, and one read a check's exit code through `tail`
  (WI-921, 2026-10-15). Tell every builder that a comment it writes, code or
  test, never cites a review round or finding number: the convergence round
  reads the diff and must not see earlier findings (wi-911 D-014). In a headless leg (SKILL §7), tell every builder to run its
  commands in the foreground: one that backgrounded its pytest run returned
  "waiting" with no result (WI-902, 2026-10-11). Resume it with SendMessage;
  its report then arrives as a task notification while you keep working.
  Tell every builder never to run a full `check_complexity.py --restamp`
  (one rewrote four rows' line counts upward, WI-798) and to delete any
  `.ruff_cache` its ruff run leaves in the tree: one under
  `project-trajectory/scripts/` reddened `test_mapping_purpose` in the smoke
  tier (WI-798, 2026-10-11).
  Tell every builder never to fold parametrized cases into one looping
  test to stay under the smoke tier's `max-tests`: in-process growth
  re-stamps the ceiling instead (wi-927 D-002). Two lanes carrying the
  same re-stamp hunk, byte for byte, merge cleanly (2026-10-18b).
  A brief derived from another lane's by text substitution keeps that
  lane's spec filename: `ls` the spec path each derived brief names
  before its launch (one builder found the right spec on its own;
  2026-10-18a).
  A wording fix's brief names every site that states the text, found
  by grep: a builder held to the two sites a finding named left the
  spec's own copy of the same bound contradicting them, and flagged it
  (wi-946 D-010).
  Brief a hook's coverage as reading the command word the
  way the shell grammar does, from a list you give; a brief asking for every
  form that gets past the hook was cut off by a safety classifier (WI-834).
  A plan that orders its commits (a pin, then a structural move alone,
  then the rest) is built in stages: the builder stops after each, you
  verify and commit through `integrate.py attest` (§6), and SendMessage resumes the same builder (WI-911,
  2026-10-15). In a headless leg the resumed builder runs in the
  background and reports only while the leg's turn still runs: wait in
  the foreground on the file it writes last (its bar log, then its
  spine change list), never end the turn on it (wi-925 D-008).
  Ask it to create a `.done` file as its very last act and poll for that
  file in one foreground Python command (`time.sleep` in a loop; a bare
  `sleep` is blocked): three resumed stages were waited out that way
  (2026-10-22c). A sub-agent's write of a file named `report.md` was
  refused by the harness; ask for a `*-notes.md` or the reply inline.
  A stage that changes a shared signature before the stage
  that moves its callers has a red bar alone: commit the two stages
  together, never bridge them with a default (wi-918 D-001). A blank line ends a `Contract IF-NNN:` body for the
  interface reference, so text added to a contract continues the body
  without one (wi-922 D-003).
- **A Codex call (Sol or Terra)** runs through one entry point, from any
  directory:
  `"$PY" "$TOOLS/codex_call.py" <role> --root <dir> --prompt-file <prompt> --out <out> [--effort medium] [--wi WI-NNN] [--resume] [--route <entry>]`.
  The role is `REVIEW-A` (a Sol review), `CRITIQUE` (a Sol scope or plan
  critique) or `AUTHOR` (a Terra turn, which names its `--wi`). The role's
  enabled roster row (`OPENAI-SOL`, `OPENAI-TERRA`; `--route` names another
  enabled entry) gives the model and route; the launch is the entry
  point's own: workspace-write, unelevated, the review scratch root
  (`$REPO.wt/review-tmp`, derived from `--root`) writable, the effort, and
  the prompt on stdin. It writes the final text to `--out`, then prints the
  log's path and state and the exit code.
  - Inside the blackout window, a Sol or Terra call is refused before
    launch (exit 2), as every non-adjudication call is. Exit 2 also
    refuses an unknown role, an unreadable prompt, a route that cannot be
    used, commit hooks off, a bad resume carrier and an `AUTHOR` turn
    whose `--wi` the lane does not hold claimed; nothing is launched.
  - The change check reads `--root`'s HEAD and uncommitted paths (content
    and index state, so a staged or unstaged path counts) before and
    after the call. Exit 3 is an edit, its paths printed: for Sol any
    change but another call's session-log commit; for Terra only a HEAD
    move that such a commit does not account for (its uncommitted edits
    are its output). Nothing is reverted and the log is still recorded.
  - Exit 4 is a log left uncommitted, or a spool that could not be
    written, the log and the refusal named: commit the log before the next
    call in that lane. Exit 5 is a check that could not run (git could not
    answer): trust nothing the call wrote. Exit 1 is a failed call. After
    launch 5 outranks 3, 3 outranks 4, and 4 outranks 1.
  - In a claimed lane the call commits its own `call_` session log when
    it returns: a record-only commit that moves the lane's HEAD, so render
    a brief, filing or plan record that follows the call at the new tip
    (wi-960 D-009). A call outside a claimed lane (the primary checkout,
    the detached critique checkout) spools its log under the primary
    checkout's `out/sessions/spool/` and commits nothing; the spool's
    harvest is WI-800's.
- **Terra, first turn:**
  `"$PY" "$TOOLS/codex_call.py" AUTHOR --root <lane> --wi WI-NNN --prompt-file <prompt> --out <out>`.
  - Terra's first turn is the intent turn, TC rows included, before build
    round 1; a `single` row takes it after its pass record (SKILL §3,
    "Intent").
  - Terra's own pytest check has failed on a basetemp lock at every turn
    (wi-956 D-001, D-007): run its spine tests yourself with the bar, and
    normalize its CRLF writes to LF before the commit.
  - Fill `"$TOOLS/terra-spine-prompt.template.md"` with `mkprompt.py`, then add
    the intent or checkpoint instructions from the skill. Its default brief
    does not request a whole subtree or arms map. At the intent turn fill
    `CHANGES=none` and leave `TESTS=` empty: no build has run, so there is
    no change list and no lane test yet.
  - Commit a turn's log before the next turn: the call commits it in the
    lane, and after an exit 4 commit the named log yourself. The resumed
    turn reads its session id from that committed log: a lane resumed
    days later found a noted id only in `~/.codex/sessions/<date>/`, by
    its `cwd` and model (wi-798, 2026-10-20).
  - A single plan that orders its record step after its tests (WI-962's
    P5 after P1) still meets Terra first: the intent turn takes that
    step's registry rows, and the builder keeps its non-registry parts
    (flows, prose outside the registries, contract bodies) and the
    RESYNC entry (wi-962 D-001).
  - An intent row naming a module the build creates (a new IF row's
    owner) reds the bar before that module exists
    (`test_seam_resolution`; `check_trajectory --strict` also errors on
    an IF no TC cites): keep the set as a patch and let it ride the
    build commit that creates the module, recorded as a decision
    (wi-940 D-002).
  - `mkprompt.py` takes `LANE=<branch>` (`wi-912`), never the worktree
    path, which builds a broken `--basetemp` (`C:-Projects-...`).
- **Terra, resumed:**
  `"$PY" "$TOOLS/codex_call.py" AUTHOR --resume --root <lane> --wi WI-NNN --prompt-file <prompt> --out <out>`.
  It continues the thread of the lane's newest Terra log committed at
  HEAD (bound to one of the lane's work items and the Terra route). A
  missing, damaged, foreign or conflicting log, or an uncommitted newer
  one, refuses the turn before launch, naming the log and the cause; it
  never starts a fresh thread in its place. Commit the named log, or run
  a first turn without `--resume`.
- **A review round: render, launch, file** (SKILL Roles and §3; rulings 4
  and 7, revision 37). Never write a review brief by hand. Every round is
  full-lane, from the lane's trunk base to its tip, and runs REVIEW-A and
  REVIEW-B in parallel, each from its own render with its own scratch
  directory (so its own verdict path and `--basetemp`).
  1. Render from the lane root, once per reviewer:
     `"$PY" "$SCRIPTS/review_brief.py" review --wi WI-NNN --base <trunk base> --sha <tip> --scope full --tests <files> --scratch <dated root>/<reviewer> --rubric docs/rubrics/kit-change-review.md --out <brief>`.
     `--tests` takes the files as separate arguments; one quoted string
     renders as a single bogus path in the brief's pytest line.
     `--tests` is the list the tip was attested with: the render refuses a
     tip with no verified `review` attestation for that list, looking
     beneath it only through record-only commits (round files, log
     fragments, empty commits), and names the `integrate.py attest` command
     to run. A spine-checkpoint commit and a decisions-record commit change
     non-record paths, so attest them (stage them into the next attest, or
     make an empty attestation commit) before the round.
     A red the tip already shows (a known failing test) is fixed in a build
     stage before the round, so the round reviews a green tip (item 13;
     wi-926 D-007).
     Counted rounds 1 and 2 pass no `--stance` (the ordinary default). The
     third counted round, the last the cap allows (ruling 4), the gate over
     the checkpoint tip, a round over a rebase that changed code or rows, and
     a review after a fix round the cap's sitting orders each add
     `--stance convergence`, and each renders only after the convergence map
     (SKILL §3) is recorded in the lane's decisions. The brief names the
     verdict path under the scratch directory.
  2. Append nothing the template states: its reviewer brief carries the
     threat model (PROCESS.md §6), severity by reachability, the out-of-set
     classification and, under `--stance convergence`, the convergence
     stance with its reading exclusion. Never add a builder self-assessment
     or the builder's coverage plan: a judge's brief carries no claim of the
     judged party. A handoff's builder notes "for the reviewers" stay out
     too: raise them at triage if the round does not (the reviewer found
     both on its own, wi-928 D-002).
  3. Launch REVIEW-A with `"$PY" "$TOOLS/codex_call.py" REVIEW-A --root <lane> --prompt-file <brief> --out <out> [--effort medium]`
     (default medium). In a headless leg, launch REVIEW-B before REVIEW-A:
     the harness runs the two launches one after the other, and REVIEW-A's
     call commits its session log in the lane when it returns, moving HEAD
     past the sha REVIEW-B's brief pins (wi-960 D-009). Exit 3 means the reviewer changed the lane; inspect
     before trusting. Edit nothing in a lane while its reviewer runs: the
     check counts your own edit too (WI-911, 2026-10-15). The launch uses workspace-write, because a read-only
     sandbox could not run Python, and its change check reads HEAD and
     status before and after; the call's log commits in the lane.
     Launch the Claude REVIEW-B as a sub-agent given only its brief's path
     plus the lane worktree and the interpreter, which the brief does not
     name, and ask for a two-line reply (the verdict path and its VERDICT
     line). Pass the Agent tool's `model: "opus"` and `effort: "high"`: a
     prompt saying "work at high effort" does not set it (2026-10-16c).
     Record the stand-in in the lane's decisions. Create each reviewer's
     scratch directory before the launch: Sol's first pytest run failed on
     a missing basetemp parent (2026-10-18c). A Claude reviewer that
     backgrounds its own pytest can lose the completion notice and stop
     with no verdict: look for its process (its scratch path in the
     command line), then resume that reviewer with SendMessage, never a
     fresh one (WI-921's gate, 2026-10-15g). A Sol launch whose sandboxed
     shell never returns runs no command and writes no verdict (its
     output says the review was blocked): probe the same entry point with a
     one-command prompt (`git rev-parse HEAD`), then relaunch fresh on
     the same brief, and file nothing from the failed one (wi-946
     D-012).
  4. File each: `"$PY" "$SCRIPTS/review_brief.py" file --review <verdict path> --sha <tip> --scope full --phase REVIEW-A`
     (or `--phase REVIEW-B`) writes `docs/reviews/<lane>/NNN-<phase>-<sha7>.md`.
     It refuses a review not opening `Reviewed: <full sha>`, or without
     exactly one `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<n>` line
     whose count matches its findings. It picks `NNN` itself: read the filed
     name before a commit subject or brief cites the round. A verdict
     quoting a fixture's markdown link files a broken link, which
     `check_docs` reds in the bar: make that link a code span in the
     scratch verdict (backticks only), delete the filed copy and
     re-file (wi-925 D-011). Each round file
     gets its own coverage plan (`plan_coverage.py --findings` takes one).
  - A round finding that the lane's amended rows carry no sitting or act
    yet names no code defect: its remedy is the checkpoint sitting, the
    cycle's next step. Re-grade it in the lane's decisions; it costs no
    fix round, and the convergence map points it at the sitting's verdict
    and act (wi-931 D-006, D-008). So is a gate finding that an accepted
    sitting's act is still owed: the act turn follows the gate (wi-942
    D-005).
  - With Codex capacity short, run two lanes' REVIEW-A sessions one at a
    time, so a usage limit takes out at most one review.
- **Scope critique:** render
  `"$PY" "$SCRIPTS/review_brief.py" critique --wi WI-NNN --rubric docs/rubrics/scope-critique.md --scratch <dated root> --out <brief>`,
  add the skill's two scope and trust questions, and send it to a fresh Sol
  session:
  `"$PY" "$TOOLS/codex_call.py" CRITIQUE --root "$REPO.wt/trunk-tmp" --prompt-file <brief> --out <out>`.
  Record the answer before the claim. In an attended session, put
  the spec's filing calls to the owner first and record them under
  `## Calls ruled at filing`, so the critique judges the ruled spec (WI-921
  to WI-923, 2026-10-15). `review_brief.py critique`
  names the same verdict path every round (`WI-NNN-scope-critique.md`): move
  the previous round's file aside before rendering the next. Ask in the same brief for a ruling per
  consumer and for every carrier's failure contract (producer, write route,
  failed-write shape): asked piecemeal, they cost WI-882, WI-884 and WI-887
  three rounds each (2026-10-10).
  Run each critique from a detached scratch checkout at the committed tip
  (`git -C "$REPO.wt/trunk-tmp" checkout --detach <tip>`): the change check
  compares the checkout's HEAD and status before and after, so the
  coordinator's own uncommitted trunk edits would read as the critic's.
  Several critiques may run at once from that one checkout, each with its own
  scratch directory (2026-10-14). A detached checkout is outside a claimed
  lane, so each critique's log spools under the primary checkout's
  `out/sessions/spool/` and nothing is committed there.
  The rendered brief tells a critic in coordinator use to commit its
  verdict: append a line naming the verdict path and saying to commit
  nothing and change no file in the checkout. Confirming rounds can run
  there beside a lane's reviews (2026-10-17b).
  A confirming round runs in convergence stance (owner, 2026-10-14). The
  rubric's verdict section states that stance, so append one line to its
  brief: that it is a confirming round of round N, checking the adopted
  dispositions the spec records. A disposition that adds a carrier with authority gives the
  next round new S2 surface: prefer removing the authority over guarding it
  (WI-911, rounds 2 to 4).
- **Filing a row by hand:** bump the mark (`trace.py --bump-ids`) in the
  commit that adds the row. A row whose spec is its own evidence gets a spec
  of record in `docs/specs/WI-NNN.md`, the text moved there, never a
  `specref` that merely resolves (coordinator-2026-10-14 D-001); R-F archives
  it at close. Delegate drafting to planner sub-agents writing into scratch,
  and read their Done-when, Trust and Scope answers before filing. Ask a
  Trust drafter to read the code and report any consumer that fails open:
  WI-921's found the very step it arms failing open (2026-10-15). Once the
  owner rules a draft's calls, resume the same drafter with the decision ids
  to fold them into a final copy: it keeps its reading (2026-10-15i).
  Drafts have come back CRLF: normalize to LF as you place them. A claimed
  row's revised copy is critiqued from its own detached worktree
  (`git worktree add --detach`) with the copy placed uncommitted, never in
  the shared critique checkout (WI-922, 2026-10-16).
- **Single plan** (a claimed row whose claim copy declares
  `planmode = "single"`; SKILL §3 "Plan"), from the lane root. Each record
  commits alone: the hook's plan-gate step refuses a pass record committed
  with the critique it cites.
  1. Brief: `"$PY" "$SCRIPTS/review_brief.py" plan --wi WI-NNN --scratch <dated root> --out <brief>`;
     launch a fresh Opus sub-agent (Agent tool, `model: "opus"`) given only
     the brief's path. It writes `<dated root>/WI-NNN-plan.md`; copy it
     verbatim to `docs/plans/WI-NNN/plan.md` and commit it alone.
  2. Gate: `"$PY" "$SCRIPTS/plan_coverage.py" --item <spec> docs/plans/WI-NNN/plan.md`;
     only exit 0 goes on. A `DELTA: beyond` plan closes the lane partial.
  3. Critique:
     `"$PY" "$SCRIPTS/review_brief.py" critique --plan --wi WI-NNN --sha <plan commit> --rubric docs/rubrics/plan-decomposition.md --scratch <dated root> --out <brief>`
     (it runs the coverage step itself and refuses a failing plan), then
     `"$PY" "$TOOLS/codex_call.py" CRITIQUE --root <lane> --prompt-file <brief> --out <out>`. Each round has its
     own verdict path, `WI-NNN-plan-critique-<n>.md`. Append one line to
     every critique brief naming that path and saying to commit nothing,
     run no `plan-file` and change no file in the checkout: with it, eleven
     plan critiques left their lanes untouched (2026-10-18a). Several
     lanes' plans, critiques and records run in parallel, each from its
     own lane, its records committed alone behind its own bar.
  4. File: `"$PY" "$SCRIPTS/review_brief.py" plan-file --wi WI-NNN --critique <verdict> --sha <plan commit>`
     writes `docs/plans/WI-NNN/critique-<n>.md`; commit it alone. The
     critic may file it first: Sol ran `plan-file` in the lane and tried to
     commit (WI-911, 2026-10-15; the entry point exits 3). Move its copy
     aside, file the verdict yourself, and compare the two. Never rebase
     the lane between a critique's verdict and its filing: filing needs
     the reviewed commit to be an ancestor of HEAD, so a rebase orphans it
     and the filing refuses. Reset to the pre-rebase tip, file, then
     rebase (wi-931 D-001, 2026-10-16d).
  5. Pass: `"$PY" "$SCRIPTS/review_brief.py" plan-file --wi WI-NNN --pass`
     writes `docs/plans/WI-NNN/pass.toml` (refused, writing nothing, unless
     the critique reads as an APPROVE); commit it alone. A CHANGES-REQUESTED
     whose findings are all MINOR reads as one (`plan_gate`, through
     `kitlib.verdict.effective_verdict`): the pass follows, the plan
     unedited (wi-918 D-001).
  6. The one revision: `review_brief.py plan --revise` (its brief carries the
     committed plan and the critique's findings as claims), commit the
     revised plan, gate it with
     `plan_coverage.py --item <spec> --findings docs/plans/WI-NNN/critique-1.md docs/plans/WI-NNN/plan.md`,
     then steps 3 to 5 again: the second critique's brief is in convergence
     stance and carries no first verdict, and its render refuses a revision
     that does not answer the first critique's findings. Its render names no
     reading exclusion, though the lane holds `critique-1.md` and a decisions
     record that summarizes it: append one by hand (those files and
     `docs/reviews/`), and tell the critic never to file or commit (wi-911
     D-003).
  7. At the cap: never number the findings by hand. A finding's `F#` is its
     position among ALL the critique's findings (a MAJOR after a MINOR is
     F2). Write a positions file, one `F#: <position>` line per BLOCKER and
     MAJOR finding, then
     `"$PY" "$SCRIPTS/review_brief.py" plan-file --wi WI-NNN --dispute-findings docs/reviews/<lane>/NNN-DISPUTE-findings.toml --positions <file>`
     writes the dispute findings file (below) with those ids and each
     finding verbatim; a refusal names the ids it expects. The positions
     are the coordinator's (`held_by = "coordinator"`): when nothing is
     contested, say so, and that the cap routes it, taking no side. The
     text after the colon is that statement, filed verbatim as the
     finding's `position`; a bare number there files as the position
     (wi-902, 2026-10-20).
     Two lanes' sittings have run in parallel (2026-10-18b). Sit it; commit;
     then `plan-file --wi WI-NNN --pass --dispute <verdict path>`. Anything
     but an accepted DISMISS of every one is the owner's: close the lane
     partial.
  An edited plan or Done-when unbinds the record: remove it, and a fresh
  critique (the cap still counts) must pass the changed plan.
  So a checkpoint item a handoff or spine change list calls a Done-when
  amendment, on a `single` row whose pass record stands, goes to the
  Trust section instead: once the Done-when digest moves, the plan gate
  refuses every later commit outside the record homes, the reconcile's
  registry edits, the act and a rebase's RESYNC re-anchor included
  (wi-927 D-010).
  A row claimed `single` whose lane already holds build commits before its
  pass record fails the landing walk at each of them: rebase those commits
  onto the plan, critique and pass commits, or re-cut the lane and run the
  plan step first.
  A disposition-minted successor whose spec names its predecessor's spec
  of record in `specref` but declares no Done-when of its own is refused
  by the plan render: carry the spec of record's sections into the row's
  spec byte for byte, and a `combined` sitting of kind
  `done-when:WI-NNN` blesses them before the plan (wi-969 D-001). A plan
  revision the owner routes to such a successor renders as a fresh
  `plan --wi`, with the predecessor's plan and critiques appended as
  claims and the ruling as binding; its critique then renders as round 1
  in the ordinary stance, so append the convergence line by hand (wi-969,
  2026-10-22).
- **Coverage plan (rework):** from the lane root,
  `"$PY" "$SCRIPTS/plan_coverage.py" --item <spec> --findings <round file> <plan>`.
  Dispatch the fix only on exit 0. A finding a dispute sitting dismissed, or
  ruled SUCCESSOR, is excluded citing that verdict:
  `Excludes: F2 — dismissed: docs/reviews/<lane>/NNN-ADJUDICATE-<sha7>.md#<its id there>`, or
  `Excludes: F2 — successor: docs/reviews/<lane>/NNN-ADJUDICATE-<sha7>.md#<its id there>`.
  The gate refuses a cite that is not an accepted DISMISS or SUCCESSOR of
  that finding, or whose findings file beside the verdict records another
  finding under that id. The plan cap takes only a DISMISS. Until WI-878 binds the findings file into the sitting, keep finding ids
  unique within a lane: a second dispute reusing ids refuses a valid
  dismissal.
  A dispute FIX's remedy is checked on the coordinator's own landing
  shape: the remedy WI-963's sitting named (compare with the copy the
  re-attesting act's commit wrote) closed its finding only on an
  unsquashed range, while every hand landing is a squash; ask the
  builder to drive the fix over a squashed range too (wi-963 D-011).
  Before writing a disposition broader than a finding, read the finding's
  own remedy: a triage that forbade WI ids in shipped comments contradicted
  both reviewers' remedies and a pinned convention (wi-911 D-014). A
  fail-open or Done-when-gap finding the builder accepts, whose only fix is
  a new boundary beyond the spec's surface, goes to the owner as a choice
  (a successor, the build, or a sitting): neither you nor a sitting may
  defer it. A successor ruling is stated in the spec's Trust section, never
  its Done-when, so the pass record stays bound (wi-921 D-014).
  Run a fix round in two stages on one builder. Stage 1 confirms each
  finding on the real path and writes the coverage plans (one per round
  file), changing nothing in the lane; you re-run each gate, rule the
  plan's stop points (a site of the class outside the spec's surface is
  reported, not built), then SendMessage releases the fix (WI-921 and
  WI-911, 2026-10-15). Brief the builder to confirm a route it names by
  reading the function behind it: one cited `handback.py`'s `--no-verify`
  commit as a return-to-queue route, which `close_partial` owns and
  `spec_move.py`'s stale docstring still describes (wi-921 D-013).
  In a headless leg, where a resumed builder reports only in the
  background, one fresh builder may run both stages in one dispatch: it
  gates every plan to exit 0 before changing anything, and you re-run
  each gate before the commit (wi-955 D-003, wi-956 D-003). Never number
  a round file's findings in the brief: tell the builder to read the
  gate's positional ids from the file (a hand count ran one high, wi-956
  D-003).
- **Closure checks,** from the lane root, both strict lints:
  `"$PY" "$SCRIPTS/trace.py" --strict` and
  `"$PY" "$SCRIPTS/check_trajectory.py" --strict`.
  These operate on the whole repo; neither accepts a row-set filter. Check
  the set's parents, TC links, interface citations and arms map separately.
- **Adjudication,** from the lane root:
  1. Compose the brief:
     `"$PY" "$TOOLS/compose_lane.py" WI-NNN <brief> "<ids>" "<srs>" <verdict> <out>`.
     The classes are `amendment`, `first-approval`, `done-when`, `combined`,
     `disposition`, `consolidate`, `red-tc`, `rejudge` and `dispute` (below).
     For `combined`, `<ids>` is **kind-prefixed**, for example
     `"amendment:LLR-123;first-approval:SR-234;first-approval:LLR-345;first-approval:TC-456;done-when:WI-NNN"`.
     Include only kinds actually owed (`amendment`, `first-approval`,
     `done-when`); `<srs>` is the semicolon-joined SR scope. A checkpoint is
     always `combined`, even when only amendments are owed, and so is a
     returned row's re-sit (`first-approval:TC-370` alone, wi-926 D-012): sitting 010,
     composed as the single-kind `amendment` class, came back with a
     `## amendment` section the one verdict parser refuses for a single-kind
     brief, after its act was committed, and was discarded (wi-921 D-018).
     Single-kind briefs use bare ids. An empty section refuses the entire composition.
     A `disposition` row that carries an `## Owner route` section (WI-953,
     coordinator-2026-10-20 D-013): the composer reads only the closed spec,
     its report and the commit facts, never the disposition row's own body,
     so append that section verbatim to the composed brief, chained on the
     composer with `&&` (the WI-894 trap in step 3), and check the brief
     carries it before the launch. Include
     affected chain rows in the appropriate scope and supply the arms map
     as an additional input; the composer does not generate it.
  2. Name the verdict `docs/reviews/<wi-slug>/NNN-ADJUDICATE-<lane sha7>.md`.
  3. Check sign-in. The adjudicator runs on the declared ADJUDICATOR account,
     which authenticates with the owner's long-lived token, read at each
     launch from the file the `AGENT_CLAUDE_TOKEN_FILE` environment variable
     names. Set that variable
     to the path in the launching shell; never read the file, and never put
     the token in a brief, log or commit. It is the launch's one environment
     credential: an ambient `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` or
     cloud-provider switch is left out, and a route declaring one (or
     `--bare`) is refused. Settings-file credentials (`apiKeyHelper`, a
     settings `env` block, a managed gateway) are not checked: keep them out
     of this repo. Then run
     `"$PY" "$SCRIPTS/coordinator_adjudicate.py" signin` and read its
     `signin [ADJUDICATOR] token: <status>` line: `signed-in`, `missing` or
     `unknown`; `signin` itself always exits 0.
     Leave the verdict path absent: `adjudicate` reserves it exclusively.
     Check the composer's output before appending to the brief: a
     `compose_lane: REFUSED` line leaves no brief, and an append then makes
     a brief of the append alone, which the sitting will judge (WI-894,
     2026-10-10). Chain the append and the launch on the composer with `&&`.
  4. Run it in the background (a headless leg: foreground, SKILL §7), because a
     call can outlast the 10-minute tool cap:
     `"$PY" -u "$SCRIPTS/coordinator_adjudicate.py" adjudicate --brief-file <brief> --brief <class> --wi WI-NNN --verdict <path>`
  5. Read the exit code:
     - 0: a valid verdict (returns can still require rework);
     - 1: the call failed or the verdict is bad;
     - 2: refused before launch (for example, run from the primary checkout);
     - 7: the token is unset or unreadable, or the route declares a competing
       credential. The remedy for an account that is not signed in is
       dev-setup's one-time `claude setup-token` step (`scripts/dev-setup.*`) and the
       variable above, never an interactive sign-in.
  6. After each call, read `$REPO/out/adjudicator/*.json`
     (`state`, `pct`, `reset_reason`) for telemetry only, never to decide a
     hold, act or gate; the store is under the primary checkout. A `*.mark`
     file beside a record (same stem) means its state is pending until the
     next locked read; an absent or unreadable record means no retained
     session is known, and a malformed one is no record. Never edit or
     delete a record or a marker.
  7. The adjudicator commits its verdict, and the sitting ends there. The
     entry point records the outcome beside it and commits the telemetry. The
     verdict's act is a later act turn, after the rebase (§3). In a headless
     leg these commits carry the run's trailer: the adjudicator's from its
     brief's provenance line, the telemetry from the kit's writer (SKILL §7).
- **Dispute sitting,** from the lane root:
  1. Write the findings file beside the verdict it will get,
     `docs/reviews/<lane>/NNN-DISPUTE-findings.toml`, in the shape
     `project-trajectory/scripts/kitlib/dispute.py` declares: `range =
     "<base>..<head>"`, then one `[[finding]]` table per finding with exactly
     `id`, `held_by` (`builder` or `coordinator`), `finding` (the reviewer's
     text verbatim) and `position` (the holder's position verbatim). Never
     name a finding `G` plus a digit: `check_vocab` reads it as a retired gate
     tag wherever the id is quoted in an authored file (a decisions record),
     and the smoke tier goes red. Keep the
     file after the sitting: the coverage gate reads it.
  2. Compose: `"$PY" "$TOOLS/compose_lane.py" WI-NNN dispute "<findings path>" "" <verdict> <brief>`
     (a row whose `Brief` is `dispute` and whose `Adjudicates` names the
     findings file, through `adjudicate_brief.compose`).
  3. Run `adjudicate --brief dispute` as above. The verdict rules each
     finding once: `RULING: <id> FIX|SUCCESSOR|DISMISS <class>|ESCALATE <why>`,
     the dismissal classes being `out-of-scope`, `refuted` and
     `not-worth-cost`. A SUCCESSOR's reason says what its row must do; the
     brief never offers it for a convergence-class finding.
  4. Record each ruling in the response to the review and in the lane's
     `docs/decisions/<branch>.toml`. An ESCALATE goes to the owner. A
     SUCCESSOR is filed on trunk at the landing (§3).
- **Preview spine mints,** from the lane root:
  `"$PY" "$TOOLS/preview_mint.py" <before> [<after>]`.
  `<before>` is the lane/trunk merge base; `<after>` defaults to HEAD. This
  previews amendments and first approvals only, not every sweep outcome.

## 2. Claiming

1. `"$PY" "$SCRIPTS/coordinator_guard.py" take --transcript <path>`.
   If a stale holder blocks it, the owner releases it.
2. Commit the deletion of `docs/work/pause`, carrying the regenerated
   `docs/open-items.html`. Run `trunk_step.py --regen` first: right after
   a landing the deletion commit was refused for a stale status block and
   `docs/ratify/CURRENT.md` (2026-10-21d). It counts as reviewed when it passes the commit bar
   and cites the owner's authorization.
3. Confirm HEAD moved. `claim` reads the **working-tree** pause.
4. Run `"$PY" "$SCRIPTS/integrate.py" claim --wi WI-NNN --branch wi-NNN`
   for each row. Branch names are single-segment. A claim that exits 127
   with an empty log never launched (two of four did, 2026-10-17e):
   retry it, and read `git log` for its claim commit.
5. Restore the pause byte-identical in the next commit, again with the
   regenerated `docs/open-items.html`, even if a claim failed.

The claims may go in while another lane's act turn runs in its own
worktree, so the new lanes' planners start sooner; that lane then rebases
once more over the docs-only commits before it lands (2026-10-18f).

A claim moves the row's spec from `queued/` to `active/<branch>/`, so any
other row whose `specref` names that queued path stops resolving (R-E) the
moment the claim lands (WI-887 on WI-884, 2026-10-10). Point a split's
`specref` at its stable home (the decision record that split it), never at
another row's spec. Run `check_trajectory.py --strict` after the claims and
gate the restore commit on its summary line, not only on the smoke tier's.

A batch claimed under one scoped unpause carries only soft edges
(`~WI-NNN`) between its rows: a hard edge blocks a claim until its
predecessor is done. The landing order and each row's Done-when holds (the
plan gate before a `single` build) carry the sequence (2026-10-14).

The pause gates claims only; acts, landings and sweeps run under it. `claim`
refuses a row whose id appears in `status.md`'s hand text, so describe rows
there by subject; reword an offending line in its own trunk commit before the
claim. A branch cut at the claim lacks the restored pause: while it has no
commit of its own, move it to trunk's tip
(`git branch -f wi-NNN <trunk tip>`), then add its worktree with
`git worktree add "$REPO.wt/wi-NNN" wi-NNN`.

## 3. Landing

- **Restore trunk-only views before the final gate.** These are
  `PROJECT_STATE.html`, the generated part of `docs/status.md`, `docs/stage`,
  `docs/open-items.html`, `docs/requirements/components.derived.toml`,
  `docs/cli-reference.md` and `docs/interface-reference.md`. Preserve authored
  status text. The hand path regenerates views during iteration; restoring
  them keeps the final range to authored work. Normal claimed work branches
  skip these freshness gates in `check.py`; this is a hand-path convention,
  not a requirement imposed by every lane commit's hook. Keep the lane's
  module-size stamp (`linecounts` in `tests/test_module_size_ratchet.py`),
  and any view the lane's Done-when names: WI-922 kept the interface
  reference its Done-when required fresh (wi-922 D-006).
- **Rebase, even when trunk moved only by the pause restore.** Text-then-act
  exempts a squash only of a tip that contains HEAD. Conflicts: §4. When
  trunk moved only by commits the lane does not touch, rebase before the
  gate: the gate then reviews the tip that lands, and no post-rebase round
  is owed (WI-922, 2026-10-16c).
- **Complexity on the merged tree:**
  - Run `"$PY" "$SCRIPTS/check_complexity.py" --mode enforce`.
  - A module pushed past 1000 SLOC is decomposed, never bumped.
  - A baseline row that went down is deleted or lowered alone, in the lane
    commit that moved it (the hook refuses a stale row), in the tab-separated
    `docs/complexity-baseline`. Never run a full `--restamp`: it rewrites every
    row's line count and writes any row that grew.
- **The act turn** (last spine commit; session telemetry may follow), from
  the lane root, after the rebase:
  1. Before the rebase, note the commit that added the verdict. After it,
     compare each judged row at that commit (`git show <verdict
     commit>:<registry>`) with the same row at the rebased tip. A changed or
     renumbered row is re-sat; never act on it.
  2. Run it in the background, as the sitting ran:
     `"$PY" -u "$SCRIPTS/coordinator_adjudicate.py" act --verdict <path> --wi WI-NNN`.
     It composes the act brief from the verdict and its binding as committed
     at HEAD and launches it on the retained session where the dial retains
     the verdict's class, else fresh. It writes no verdict and no binding.
  3. Read the exit code:
     - 0: every act the verdict authorizes is committed;
     - 1: the call failed, an act is still owed (printed), or the call wrote
       under `docs/reviews/`;
     - 2: refused before launch: not a lane, uncommitted changes (named), a
       verdict not accepted at HEAD, one that owes no act (a re-run after a
       completed act), or a judged row in a state no act explains (named);
     - 7: as for `adjudicate`.
  4. An act that stopped between its flip and its snapshot leaves the flip
     uncommitted, and the next `act` refuses the lane as dirty. Discard the
     named paths (`git checkout -- <paths>`), record that as a decision, and
     re-run: it lists the whole act again. A combined act stopped between its
     two commits re-runs with only its first-approval act.
  5. A lane in flight when WI-912 landed: a verdict sat before it whose act is
     still owed carries no bless marks, so re-sit it, recorded as a decision.
     An act a lane already took from such a verdict on a MEANING row is not
     authorized either: the merge slot refuses it, so re-sit the row before
     the landing.

  The act brief lists its own `--reattests` and `--approves` rows: CLARITY
  rows, a MEANING row the verdict marks `[MEANING+BLESS]` on a released rung,
  and APPROVE rows on a released rung; on a held rung a CLARITY re-attest
  names the verdict with `--verdict`. A row the verdict rules CLARITY that
  the lane deleted (a retired row) is listed in `--reattests` until its
  recorded copy drops it; on a held rung it owes no act (removing a held row
  is the owner's). A first approval of a row absent at HEAD is refused as
  inconsistent.
  The act turn takes one act per kind of judgement, in the combined brief's
  order: the amendment act
  (`--reattests`) first, then the first-approval act (`--approves`). A
  first-approval copy is refused while an approved row in its registry still
  drifts unattested, and the amendment act clears that drift first. The old
  single act covering both kinds is retired, because the spine is decomposed
  one way in every mode (owner, 2026-10-07). This order is not yet proven on a
  same-registry checkpoint, so record the first one. `--approves` splits on
  `;`, so never put one in a ref. A traced-only change owes no sitting.
  A traced cell changed after the act (a `code_symbol` a later fix adds)
  leaves the registry off its anchor: re-anchor it in the LANE, as its last
  spine commit, with
  `"$PY" "$SCRIPTS/intake.py" snapshot --approves "<registry>=<ref>"`
  (no `--reattests`; the ref names the sitting that last anchored it).
  Taken on trunk inside the squash, text-then-act refuses it (WI-887,
  2026-10-11). Adding an IF to an approved TC's `Verifies` (the strict gate refuses
  an IF row no TC cites) is traced-only too: the composer refuses an
  amendment sitting for it, and the re-anchor is the step (WI-902's archived lane tip `d3d301216`). The bar command on the staged squash (below) catches
  this drift; the lane hook does not.
- **A return in a sitting holds its whole registry.** A row the sitting
  would bless is not anchored while another row in the same registry is
  returned; rework the returns and re-sit them all together. Move each
  answered verdict's `## Dispositions` under another heading in the lane,
  or the landing sweep mints the rework rows. The rename may precede the act:
  the binding records the brief, kinds and outcome, not the verdict's digest
  (wi-918, 2026-10-18g).
  Re-sitting only the returned rows leaves the set judged across several
  verdicts, none of which authorizes the whole act: once the re-sits
  bless everything, one combined sitting over the whole set at the gated
  tip authorizes the act turn (wi-798 D-023). So re-sit the whole set at
  once when the returns are answered: one sitting, one verdict for the act
  (wi-958 D-014).
- **Run the commit bar in the lane after the act turn,** before the
  squash. An act that approves a row arms checks a Drafted row escapes:
  an approved Smoke TC whose evidence sits in a `SLOW_MODULES` module reds
  `test_every_approved_smoke_case_has_evidence_in_the_smoke_tier`. Fix it
  in the lane (move the case to a fast module, a traced-only change) and
  re-anchor there, never on trunk (wi-958 D-019).
- **Squash** on trunk with `git merge --squash <lane>`, one per lane.
  Run `git status` in the primary checkout first: a Claude reviewer's
  probe once left a stray file at its root through a redirect from its
  default working directory (wi-798, 2026-10-20). In a
  headless leg, first run `"$PY" "$TOOLS/overnight_legs.py" check-lane <lane>`
  and squash only on exit 0 (SKILL §7). Never
  `git stash` between the squash and its commit: the stash's reset deletes
  `.git/SQUASH_MSG`, and `text-then-act` then refuses the landing as an
  unsquashed act. Recover by `git reset --hard HEAD` and redoing the squash,
  never by forging the file. Cite
  the lane's SOUND full-lane review in the command's description: the
  auto-mode classifier has refused an uncited squash as an unreviewed merge.
  The squash's hook judges text-then-act, held-status and ruling-sync, but
  never the merge slot's approval-act floor, so on this path the act
  turn's verdict-derived command is the only guard until the one-landing
  row moves coordinator landings onto the slot (coordinator-2026-10-17
  D-009).
  If the lane recorded an owner overrule in
  `docs/decisions`, land two commits: the squash up to the commit before the
  close, then the close. The hook judges the first commit's Done-when change
  against its parent, so that commit carries the lane's covering verdict or
  owner ruling in its own tree, or the hook refuses it naming the digest; the
  close then compares against the blessed copy. Never amend either commit to
  change a Done-when or drop a blessing: an amend is judged against the
  commit it replaces, not its real parent (WI-921's stated residue).
  Ruling-sync needs an open item citing the overrule.
- **Regenerate** with `"$PY" "$SCRIPTS/trunk_step.py" --regen`. By hand, the traps are:
  - pass `--src project-trajectory/scripts` to both `gen_arch_map.py` forms (a
    bare `--contracts-doc` wipes the interface reference);
  - regenerate `docs/ratify/CURRENT.md` with
    `"$PY" "$SCRIPTS/trace.py" --approve modified --out docs/ratify/CURRENT.md`.
- **Run the commit bar, `"$PY" "$SCRIPTS/run_menu.py" smoke`, on the staged
  squash before the landing commit** (ruling 6). Its strict lints catch what the hook's
  non-strict forms pass: R-F (a closed row's `specref`) and a traced cell off
  its anchor. A lane that adds a doc also runs
  `"$PY" "$SCRIPTS/check_docs.py" --root . --strict-orphans`: the orphan check
  runs only in the full suite.
  In a working checkout it also reports the gitignored `docs/test/report.md`
  (written by `trace.py`) as an orphan; that one is local, not a finding.
- **Close the row:**
  - `## Deliverable` comes before `## Context`, because the parser clips
    everything after Context (the hook refuses a missing one, R-A);
  - `specref = ""` on the closed row only: an open row's specref must resolve
    (R-E), and never to a log fragment, which compiles away;
  - `"$PY" "$SCRIPTS/spec_move.py" <src> docs/archive/work/complete/<name>.md`, never
    `--archive`;
  - a spec of record (`specref` naming `docs/specs/WI-NNN.md`) that no
    open row cites moves with `spec_move.py --archive docs/specs/WI-NNN.md`
    in the same close, or R-F refuses it (WI-923, 2026-10-16); the move
    relinks every spec that links it, another open lane's spec of
    record included, so expect that lane's rebase to meet the relink
    (WI-926's, at WI-927's close, 2026-10-18e);
  - scrub the id from `status.md`'s hand text in the same commit;
  - keep hand-filed slugs to the handoff's 37-character ceiling; the kit's
    spec writer uses a 30-character title prefix (`wi_convert.SLUG_CHARS`).
- **RESYNC:** anchor the entry at the landing's parent, never at a lane-only
  sha. Fold a fix round's entry into its parent entry, and flag forced
  migrations.
  The bar's `check_resync` refuses every commit of a lane rebased past
  WI-916 until its entry exists, so a plan step that writes the entry
  later moves into the first commit after the rebase (wi-927 D-005).
  So does a lane's first commit that touches a shipped path, a test
  stage's stubs included: place the entry there, anchored at the lane's
  base, and let the plan's record step refine it (wi-958 D-004).
  A last rebase onto a trunk that moved only by docs commits replays
  cleanly and leaves the entry at the old base: re-anchor it in the
  staged squash on trunk, at the landing's parent (WI-927, 2026-10-18e).
- **Archive the tips** to `archive/lanes`, adding the pre-rebase tip the
  verdicts cite (and any discarded act) as extra parents. Archive commits
  carry the empty tree, `4b825dc642cb6eb9a060e54bf8d69288fbee4904`. Read the
  old tip with `git rev-parse archive/lanes`. Create the archive
  commit with `git commit-tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904 -p <old-archive-tip> -p <rebased-tip> -p <pre-rebase-tip> -F <archive-message>`;
  add a `-p <discarded-act>` for each discarded act. Record its output id,
  then run `git update-ref refs/heads/archive/lanes <new-archive-commit> <old-archive-tip>`.
  Verify the parents with `git show -s --format=%P archive/lanes` before
  treating the lane as archived. In a headless leg the `-F` message ends with
  the run's provenance line as its trailer (SKILL §7).
- **Sweep:** `"$PY" "$SCRIPTS/intake.py" sweep --merged "WI-a;WI-b" --branch <lane> --before <trunk before> --after <landing>`.
  `--merged` names every row the landing closed, or other rows' Dispositions
  are skipped silently. The sweep mints first, and its re-mint takes the next
  WI id: file hand rows after it, or cite them by subject until filed.
- **Successor rows:** for each SUCCESSOR ruling of an accepted dispute
  verdict (its `.requested` binding reads `outcome = accepted`), file one row
  on trunk after the landing, its scope the ruling's reason, citing the
  verdict by the name read from disk. A verdict not accepted files nothing,
  and its finding holds the landing. Bump the mark as for any hand-filed row
  (§1, "Filing a row by hand").
- **A gate MINOR** whose fix would move the tip off the gated one, or
  whose wording lives in homes outside the lane, is a follow-up in
  status.md's unfiled list, never a fix after the gate (wi-935 D-005).
- **The re-mint:** close it citing the act once `cmp` shows the registries
  equal their anchors. Compare each file under `docs/archive/last_approved/`
  with its live path (the test registry is `docs/test/test-cases.toml`): a
  `cmp` against a missing path reads as a difference (2026-10-16). A close
  committed after the gate, as WI-911's was, lands only when
  `git diff --stat <gate tip> HEAD` shows no code and no authored spine row. Two minted rows are real work and stay open: an
  observation re-judge whose trigger fired, and a goalposts row.
- **Review rollup:** restore `docs/reviews/rollup/` to its trunk version before
  committing the lane. `trunk_step.py --regen` writes it on trunk at landing,
  from the round files the lane brought in.
- **Messages:** cite every review and verdict file by the name read from
  disk (`ls docs/reviews/<lane>/`), never by the sha you composed it at:
  the entry point names a verdict after the lane tip at launch, and an amend
  to correct a landing's message is refused by the open-items freshness
  check. Write each to a file and use `git commit -F <file>`. Never
  reuse a message file across a lane act and a trunk landing. In a headless
  leg each message file ends with the run's provenance line inside its final
  trailer block (SKILL §7).

## 4. Rebasing

In a rebase, "ours" is the tree already replayed onto trunk; "theirs" is the
lane commit being replayed.

| File | Take |
|---|---|
| Generated views | `git checkout --ours`, continue, regenerate once at the end |
| Registries | resolve per table using this replay's base/ours/theirs (`git show :1:<path>`, `:2:<path>`, `:3:<path>`); keep independent changes from both sides and judge same-row conflicts; never take the whole file `--ours` |
| `docs/id-watermark` | `--ours`, then `"$PY" "$SCRIPTS/trace.py" --bump-ids`; preserve any higher mark for retired lane ids |
| RESYNC_PACK | both sides' entries, trunk's first; when the replayed commit rewrites the lane's own earlier entry, keep its rewrite and drop the entry it replaces; then re-anchor the lane's own entry at its new base, since the bar's `check_resync` step refuses an entry anchored elsewhere (WI-916, 2026-10-18b) |
| Byte-budget skill rows | each side's own row |
| `stack.ini`, size-ratchet notes | both sides' notes |
| Smoke-ceiling restamp | trunk's note plus the lane's count; restamp only past the ceiling |
| Module-size ratchet | per hunk: trunk's note plus the lane's count, the lane's reason kept; never `--ours` the whole file, which also drops the lane's stamps outside the conflict (2026-10-19b) |

- **At a trunk squash,** use `"$PY" "$TOOLS/toml_merge3.py" <branch> <registries...>`
  for registry conflicts; compare parsed tables even after a clean line-merge.
  It merges merge-base/HEAD/branch, not a rebase replay's three stages. It
  refuses a per-table conflict, but can already have written other files:
  inspect its output before staging.
- Never merge-refresh a lane with committed spine rows after trunk took an
  act: registry-integrity refuses the snapshot copies.
- Deleting a landed lane's branch raises hold-by-rename errors in other
  lanes; a rebase clears them.
- Ids collide across unlanded lanes. Brief each lane's Terra with every open
  lane's ids as a floor, or renumber in the later lane before committing.
  A floor spends the skipped ids on the lane: once it lands, `trace.py
  --strict` lists them as spent with no retirement record until their own
  lanes land. Record the floor in the lane's decisions; never retire them
  (WI-913 D-004).
- A lane whose spine set amends rows another open lane is amending, or
  whose code edits the same functions, waits for that lane's landing and
  rebases onto it before its spine turn and first round. Its text then
  amends what the sitting approved, and the round reviews the tip that
  lands (wi-946 D-006). Conflicts across several replayed commits can go to
  a kit-builder briefed to keep both sides' behaviour and stop on any
  semantic choice; read the resolved functions and re-run the bar yourself
  (wi-946 D-007).
- A long-stale lane continued by rebase (WI-798, 245 commits): a clean
  auto-merge can drop the lane's behaviour where trunk moved a call into a
  new shared helper (git kept the lane's computed account environment, and
  trunk's helper ignored it). After the replay, read each function both
  sides touched for a value computed and never used, and run the lane's
  tests against trunk's new commands. A trunk command the lane's design
  must govern (the act turn under the account) is a semantic call,
  recorded as a decision (wi-798 D-010).
- Show that a rebase changed no lane code or row by comparing
  `git diff <old base> <old tip> | git patch-id --stable` with the same
  over the new base and tip: equal ids owe no post-rebase round, and the
  judged rows still get their unchanged-rows check (wi-927 D-013).
- Acts collide too: check `acts.toml` after every rebase for duplicate act
  seqs (the skill's §4 latches sittings to avoid them).
- A registry cell's line can carry leading whitespace (` detail = "...`):
  match a cell on its `key = ` line after stripping, or a guarded replace
  edits the next row's cell. Chain a merge script to its `git add` with
  `&&`: a failed guard followed by `;` stages the conflict markers, and
  `rebase --continue` commits them.
- Validate a union of appended TOML rows per cell: the result equals ours
  plus theirs-minus-base, read from the three index stages. A line union has
  dropped shared tail cells; restore any missing cell from trunk's stage.
  A keep-both script resolving two new rows' hunk never dedupes a line
  across the sides: identical cells (`tier = "Full"`) belong to both rows,
  and a dedupe meant for import lists dropped three of TC-370's (wi-926
  D-006). Run `ruff format` on each resolved Python file: a joined import
  line reds the hook's format step.
- After a rebase, run trunk's and the lane's changed test modules on the
  rebased lane: the smoke tier skips the slow ones, where trunk's new
  tests meet the lane's new refusals. A failure the pre-rebase tip shares is the lane's,
  for its next build round (wi-926 D-005).
- Launch no review until the rebase has finished. A rebase stopped on
  generated-file conflicts leaves the lane mid-rebase: take `--ours`,
  regenerate, continue, then render the brief at the real tip.
- A rebase changes every commit's `work=`, so no attestation survives it:
  attest the rebased tip (`integrate.py attest` with nothing staged makes
  an empty attestation commit) before its round.

## 5. Spine-cell edits (brief Terra with these)

- Delete the lane's `<lane>-terra` basetemp before each Terra turn: an
  interrupted run left it locked, and Terra's pytest could not start
  (WinError 183; WI-922, 2026-10-16c). Re-run its checks yourself.
- Write UTF-8 only, with LF line endings. Terra has left CRLF and cp1252
  dashes; normalize before any snapshot. On 2026-10-10 every Terra turn
  rewrote whole registries CRLF: count `
` in each touched file and
  normalize before every commit.
  Count CR bytes with Python (`open(p, "rb").read().count(b"
")`): in Git
  Bash `grep -c $'
'` loses the pattern and counts every line, which read
  as a CRLF rewrite on 2026-10-10 (c) when the files were LF.
- Re-read every whole cell a splice touches. Spliced sentences have come back
  without a verb, and a deletion the spec dictates has left a list without
  its "and"; repair it in the same retained session and record it (wi-930
  D-002). To compare a Terra copy with a spec block, strip the spec's `> `
  blockquote markers first (WI-928, 2026-10-16d).
- If `apply_patch` cannot match a long one-line cell, use a guarded Python replace:
  - read and write with `newline=""`, through `open()`: Python 3.11's
    `Path.read_text` takes no `newline` argument (2026-10-15h);
  - assert each old value occurs once;
  - check with `tomllib` that list cells stay lists.
- A script that checks registry cells must assert it read rows. The
  registries are tables keyed by id (`[requirement.SR-234]`), not arrays of
  tables: a post-rebase per-cell check that iterated arrays read nothing and
  passed vacuously before it was fixed (2026-10-15h).
- A single-quoted TOML literal cannot hold an apostrophe. Rewrite the line as
  a JSON-escaped basic string, then assert with `tomllib` that the cell equals
  the verdict and no other cell moved.
- A TC citing an LLR also cites that LLR's SR, or `registry-integrity`
  refuses the commit.
- Keep an IF Data cell short, with the definition in the owner's contract
  body. `trace.py`'s 160-character data rule is a warn-first advisory that
  14 rows exceed: never fold names into brace or other shorthand to fit it,
  which hides them from a search (wi-918 D-008).
- A TC states only what the rows it verifies state. A method sentence on
  this repository's unshipped tooling (the overnight launcher) was returned
  at the sitting: its evidence absent, and no verified row stating it. A
  Done-when item about such tooling stays pinned by its own test and
  recorded in the lane's log (wi-918 sitting 003).
- Reuse the declared external parties (`external:agent CLI`). An `external:`
  IF row tied to no frame crossing joins the frame test's untied pin with a
  "No tie-back" reason.
- A row split leaves `Implements:` tags on the old id; retag them in a
  coordinator commit.
- Terra has dropped an existing `code_symbol` entry as "nonexistent". Grep
  every symbol it removes before committing.
- On a large change set (WI-834: about 30 cells) one Terra turn applies three
  to five cells, then ends saying the rest "did not apply". Resume the same
  session per batch, naming the remaining cells, one cell per script; match a
  long cell on its `key = ` line inside the row's table block. Verify the
  change-list path in the prompt before launching: a stale path wastes a turn.
- An IF row's `channel` is a closed set (`kitlib.spine.IF_CHANNELS`); a value
  outside it passes the commit hook and reddens the smoke tier
  (`test_seam_resolution`). An invocation with an exit code is `cli`.
- The local Codex sandbox has failed shallow-clone tests and `git worktree add`,
  and hit Windows locks at `-n 2`. Ask for `-n 0`; confirm those failures with
  decisive tests outside that sandbox before treating them as code defects.
- Name the sentences a lane added and no sitting approved: Terra may
  rewrite those. Told only to amend by addition, it appended a corrective
  sentence after a lane-added one it contradicted, which the coordinator
  removed before the sitting (WI-921 LLR-309, 2026-10-15). A term one row
  defines is defined again, or cited by name, in a sibling row that uses
  it: the sitting returned LLR-309 for an "elsewhere" only LLR-307 defines.
- Brief Terra to amend an approved row by addition: keep the approved cell
  verbatim, function names included (item 5's schema lane migrates them),
  and append the new text in contract voice. Told only to restate the
  builder's function names, it rewrote LLR-313's whole Detail and TC-333's
  Expected and dropped approved obligations (WI-913, 2026-10-14).
- Check that every spine item the Done-when names moved its cell at
  intent, by diffing the cell against the lane's trunk base: an intent
  turn reported SR-019's acceptance amended and never applied it, which
  round 1 caught as a MAJOR (wi-926 D-009).
- Check an intent or reconcile set mechanically before committing it: in
  each changed cell of an approved row the approved text must occur
  verbatim (old within new, read with `tomllib`; judge a tier or list
  cell by hand). Compare with the row at the lane's trunk base,
  sentence by sentence, not with HEAD: a lane-added sentence may be
  rewritten, an approved one may not (wi-925 D-009). Terra follows a
  plan's literal text: it dropped from an IF data cell a function the
  owner still serves to a requestor, and restated in an approved row a
  sentence its new row already states. Check each changed IF data
  cell against its requestors' calls, and each new sentence for a
  second home (wi-925 D-006). Terra reworded two approved phrases in SR-233 while
  reporting every approved text kept: restore the approved bytes by a
  guarded replace, keep its addition, and record it (wi-911 D-007,
  2026-10-15).
- An interface row names no file in any cell; a "No tie-back" note belongs
  only to a row with an `external:` party. Until item 11's migration, its
  `owner`, `consumers` and `requestors` hold `scripts/<module>` ids (IF-286's
  form): brief that form, or Terra strips the prefix (wi-926 D-003). Terra's
  template edits registries only, so an intent turn whose plan edits
  `docs/runtime-flows.md` says so in its addendum, and a new IF's
  `Contract IF-NNN:` body is added in the code by the builder or you before
  the commit (wi-926 D-002).
- Before composing a sitting, match each TC `expected` clause to a
  sentence of an LLR or SR in the set. A reconcile dropped two obligations
  the tests carried (a tick does not unbind a record; the second critique
  never meets the first verdict), which a sitting returns as a TC
  expecting what no requirement states (WI-913, 2026-10-15). Check it
  at intent too: a spec-dictated replacement of a sentence whose
  semicolon joined a second clause dropped an obligation the new TC
  text still expected (wi-931 D-004, 2026-10-17).
- An acceptance clause must be stated by its requirement: sitting 010
  returned SR-154 for a clause no requirement sentence made. Run
  `trace.py --strict` on a return's rework before its re-sit: the
  disposition's "shall refuse" gave SR-154 a second `shall`, which the
  one-`shall` form rule reports (WI-913, 2026-10-15).
- A TC's `tier` is the cheapest tier at which every cited arm runs
  (TC-205's rule): a TC citing any test in `SLOW_MODULES` is `Full`.
  Check each new TC against `conftest.SLOW_MODULES` before its sitting
  (wi-960 D-013).
- After every Terra turn, diff the registries row by row against the
  last commit and compare the changed rows with the set the turn was
  given: a checkpoint turn narrowed two approved evidence cells outside
  the set from a module to named nodes, which the approved-sentence
  check passes, and its report named one under another id. Restore any
  row outside the set by a guarded replace (wi-960 D-012).
- A lane that drafts a derived SR owes its perspective record
  (`hats.py record <plan dir>/plan.perspectives.toml --row <ids>`,
  passing `--check --strict`) until plan item 14 retires the sidecar:
  brief it into Terra's checkpoint turn, or the first-approval sitting
  returns the derived SR for it (wi-957, wi-958, wi-960 sitting 005).
- Draw the arms map before composing the sitting: a sub-agent given the
  rows and told to change nothing maps each LLR arm and SR acceptance
  clause to the TC clause and the test that verify it, and lists the gaps.
  At a tip two counted rounds had approved it found 25: arms no test
  exercised (a builder stage pins them with characterization tests, no
  code change) and arms no citing TC stated (Terra's next turn). Resume
  the same sub-agent to re-draw it after the fixes, and append the map to
  the brief (wi-961 D-011 to D-013).
- After a Terra turn rewrites TC rows, check each LLR's `test_refs`
  against the TCs whose `verifies` cite it, and each clause it dropped
  against the evidence that still tests it: an arms turn listed a TC in
  an LLR's `test_refs` without the forward link, and dropped a clause
  whose test stayed in the evidence (wi-961 D-012, D-013).
- A sitting's suggested wording is a claim too: check a sentence it
  proposes against every outcome the sentence covers before applying it.
  Sitting 008 returned the universal sentence sitting 007's own
  disposition suggested, which one listed outcome did not keep (wi-961
  D-015).

## 6. Commits and hooks

- A commit made by hand in a lane worktree runs the hook under the
  ambient interpreter, which has no ruff, so its format step prints "A
  DECLARED CHECK DID NOT RUN": commit every Python change through
  `integrate.py attest` (below), which runs under the primary checkout's
  interpreter; a records-only commit may go by hand (2026-10-22c).
- Run the commit bar on every commit, docs-only ones included. A lane
  commit runs it through `"$PY" "$SCRIPTS/integrate.py" attest --branch
  <lane> --bar review --tests <files> --message-file <msg>` from the
  primary checkout, which runs `[bars] review` and the named tests, refuses
  red, and commits the staged work with the attestation the review render
  requires (SKILL §3, Iterate step 1). A trunk commit runs the one
  declared command by hand, `run.cmd smoke` (`"$PY" "$SCRIPTS/run_menu.py" smoke` from
  a shell), whose steps are `docs/stack.ini` `[run] smoke`. Read the summary
  lines for `failed` and for each lint's findings before committing; a chain
  gated only on the command's exit code inside `$(...)` committed a red tier
  (2026-10-10). The commit hook does not run it: run it yourself, before a
  landing commit rather than after it.
- `integrate.py attest` runs `[bars] review`, the smoke action with its
  budget step in warn mode, so it refuses only a red bar, never the
  tier's seconds. Run it from the primary checkout, `"$PY"
  "$SCRIPTS/integrate.py" --root "$REPO" attest --branch <lane> --bar
  review --tests <files> --message-file <file>`: it finds the lane by
  branch and runs the bar there under the primary checkout's
  interpreter. Run from the lane with the default root, its harness floor
  reads the lane's own root, finds no `.venv` and refuses (wi-957 D-007).
- The declared bar runs the tier once: the lints run first, then the
  budget step's run, which exits with the tier's own code on a red tier
  and prints its CPU-seconds and wall time, with a WARN line for a limit
  over. No bar fails on seconds: `run.cmd audit` (`[run] audit`, the same
  step in enforce mode) judges them and the tier's count against
  `max-tests`, by hand and at phase close, and a breach there is filed
  as a re-tier row, never charged to the lane that ran it. A hand wrapper
  passes the step's exit code through, so a chained `&& git commit` never
  records a red tier.
- A build whose in-process tests take the smoke tier past `max-tests`
  re-stamps the ceiling in that commit, with its reason, fig line and a
  decision, not at the landing: a red bar is not left standing (wi-911
  D-005).
- A commit sometimes exits 1 with every hook step passing. Read the hook
  output and retry with `-F`; never skip the hook.
- On trunk (or `check.py --trunk-lane`), `approval-fresh` refuses a stale
  `docs/ratify/CURRENT.md`. Regenerate it and read what it lists before an act.
- Where freshness is gated, `interface-reference` refuses a stale view after
  a declared header or contract changes; regenerate it.
- On trunk, `open-items` can refuse a docs-only commit with no source change:
  the page's baseline line goes stale on its own (2026-10-14). Regenerate it
  (`gen_open_items.py`) and include it; the long list of deferral warnings
  above the refusal is standing noise from old fragments.
- A lane commit that edits a prompt template carries the regenerated
  `project-trajectory/prompts/CATALOG.md`: the hook's `prompt-catalog`
  step refuses a stale catalogue on a lane commit and `staged-divergence`
  an unstaged regeneration, whatever a plan says about regenerating it
  only at the landing (wi-912 D-003).
- A build stage that adds a module owes its component before its
  commit: `check_trajectory.py --strict` errors until an LLR names the
  module's CMP (wi-912 D-003). The intent set, committed before build
  round 1, already names it.
- `skills-sync` drift: run `"$PY" "$SCRIPTS/bootstrap.py" --dest . --sync`
  in every lane commit that touches a kit skill.
- Redirect each commit's output to a file: the pre-commit hook prints about
  80 KB.
- The secrets floor refuses a fake token shaped like a real one in a test;
  mark that line `privacy-ok`.
- `gen_verdict_rollup.py` refuses on a work branch; a lane that changes how
  rounds read leaves its rollups to the trunk landing.
- `test_the_live_repos_own_mark_covers_its_live_ids` reads the working
  tree: an uncommitted row numbered above the mark reds the smoke tier. Set
  unrelated uncommitted rows aside before running the bar for a commit
  (2026-10-14).
- `git add -A <paths>` aborts entirely if one path is missing. `2>/dev/null`
  hides that, and `staged-divergence` then fails. `components.derived.toml`
  lives under `docs/requirements/`.
- `ruling-sync` refuses an overrule (`owner = "overruled"`) unless the same
  commit amends a queued or active row citing the decision as
  `docs/decisions/<file>.toml#D-NNN`, in that form; a prose citation does
  not count. Regenerate the views after the commit's last edit: that
  citation can stale `docs/open-items.html` again (2026-10-14).
- Specref anchors take plain headings (no backticks or apostrophes), one
  anchor per row.
- A new built-in check step runs at commit only from the shipped hook's
  `--run-steps` floor or a path trigger; registering it in `check.py` runs
  it nowhere. Ask a builder adding a step for a test that drives the
  hook's own step list (WI-913 round 2; WI-841's `done-when-blessed` has
  the same gap).

## 7. Environment and limits

- **A lane that changes the reviewer template** is reviewed under
  trunk's: render its briefs with the primary checkout's
  `review_brief.py review --root <lane>` (prompts resolve beside the
  script; wi-911 D-008, 2026-10-15). Since WI-911 landed (2026-10-16) the
  template and the rubric carry what the interim addenda did; append none.
- **Model not offered on the signed-in account:** `400 ... not supported
  when using Codex with a ChatGPT account` from a current CLI (2026-10-10:
  0.162.x refused `gpt-6.1-sol`) means the account, not the CLI version.
  Read the offered models from `~/.codex/models_cache.json` (`models[].slug`,
  read as UTF-8), then probe with a one-word `CRITIQUE` call from the
  detached checkout
  (`"$PY" "$TOOLS/codex_call.py" CRITIQUE --root "$REPO.wt/trunk-tmp" --prompt-file <one-word prompt> --out <out>`;
  its log spools): the cache listed it and it worked again on 2026-10-10
  at 22:40 local (leg 02). While it is not offered, review through the
  same entry point with `--route <the enabled Luna row>` at
  `--effort high` (coordinator-2026-10-10 D-017, pending the owner); the
  model is that row's. Record the substitution in every lane's decisions
  record.
- **Codex usage limit:** wait for the reset the CLI error names. Retain
  Terra; observed session counts are not a quota.
  Every Codex call runs through the `codex` CLI on `PATH`; the owner switches
  accounts with `codex logout` and `codex login`.
- **Background or foreground.** In an attended session, start each Codex call
  as its own background command; one started in a detached subshell sends no
  notification. A headless leg (`claude -p`, the overnight launcher
  `"$TOOLS/overnight_legs.py"`) kills its background tasks when it exits, so
  it runs everything in the foreground under the raised shell cap. The
  headless procedure is SKILL §7.
  Give every bar, attest and full-suite run the whole raised cap
  (3600000 ms): on a box other sessions loaded an attest's bar ran 30
  minutes and the full suite 54, and a 30-minute timeout moved the attest
  to the background, where a leg loses it (2026-10-22).
  Launch each background call as its own command: in `A=… && (x) & (y) &`
  only the first subshell sees `A`.
- The agent harness sets `NoDefaultCurrentDirectoryInExePath=1`, so a Windows
  probe run inside it never sees the command processor's working-directory
  lookup; unset it when that lookup is the subject (dispute 005, WI-880).
- Set `export MSYS_NO_PATHCONV=1`; Git Bash rewrites leading-slash arguments.
  With it set, write every path as `C:/...`, never `/c/...`: `git -C /c/...`
  fails, and a Windows Python writes `/c/x` to `C:\c\x` (a critique
  brief landed in a stray `C:\c\` folder on 2026-10-14).
- A long heredoc that mixes backticks, quotes, `$` or backslashes has
  failed in the agent's shell (a parse error, or an escape the shell
  rewrote), a Python script or plain TOML alike (a decisions append quoting
  `$a = $b`, 2026-10-15i). Write the text or the edit script to the scratch
  root with the file tool and append or run it from there (2026-10-14).
  A step after a failed `&&` chain on its own line still runs: a spec
  placement whose guard failed was followed by an edit to the decisions
  record's `high_risk` line (2026-10-20d). Chain every dependent step
  with `&&` on one line, and check a guard's exit before the next step.
  The shell has also rewritten `\n` and `\1` inside heredoc Python, in a
  builder's test strings and in a coordinator's log edit (WI-912,
  2026-10-17): tell every builder the same.
  A command that reads stdin (a stray `cat`, a script waiting on input)
  never returns in a headless leg and is moved to the background at the
  tool cap: give kit commands `< /dev/null` (2026-10-21a), except one
  fed by a heredoc: `python - <<'EOF' ... < /dev/null` replaces the
  heredoc, so Python prints its interactive banner and runs nothing
  (2026-10-22b). A file read whose path is an empty `$(ls <glob>)`
  hangs the same way: `sed -n 1,9p $F` with
  `F` empty reads stdin (2026-10-21c); check the path first. A message
  composed with `sed` over a wrapped line rewrites the wrong text: write
  commit messages with the file tool (2026-10-21a).
- **The first bar in a freshly added worktree reads cold:** with no
  bytecode cache it read 64.9 to 68.7 s where the same tree, warm, read
  52 to 54 s (2026-10-21a, five readings). A parent timed in a new scratch
  worktree is that cold reading: run its bar twice and take the second,
  or record the first as cold, never charge the gap to the change.
- **The bar runs no hook step:** `skills-sync` (and every other pre-commit
  step) runs only at the commit, so a green bar can meet a refused commit;
  read the hook log, fix, and commit again (2026-10-21a).
- **Scratch:** one dated root, `$REPO.wt/review-tmp/<date>-<session>/`, with one literal
  `--basetemp` per kind of run (`$TEMP` is empty in the Codex shell). Delete
  the root once results are recorded.
- **Full suite:** past runs used about 4 GB of basetemp. Check `(Get-PSDrive C).Free`
  in PowerShell first,
  run from a detached worktree in the background, and delete the basetemp
  after recording.
  Off a claimed branch the suite asserts the trunk-only `docs/stage` in
  full (`test_this_repo_s_committed_stage_is_current`), so a lane whose
  close moved the derived stage reads that one red in a detached
  worktree: re-derive there (`derive_stage.py`) and re-run the test
  before treating it as a defect (wi-921 D-020).
- **Test jobs while the owner's applications load the box:** when the
  owner asks, run every local test job (bars, the full suite, Codex
  launches, the Claude reviewers' pytest) at below-normal priority
  through a stdlib wrapper
  (`subprocess.call(cmd, creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)`;
  Windows children inherit the class), naming Git Bash by its full path
  (`C:/Program Files/Git/usr/bin/bash.exe`), since Windows resolves a
  bare `bash` by its own search order (2026-10-15g). The wrapper resolves
  its program with `shutil.which`: a bare `codex` (an npm `.cmd` shim) is
  not found by `CreateProcess` (2026-10-16d). No bar fails on the smoke
  tier's seconds, so a slow reading under load holds nothing: the
  audit (`run.cmd audit`) judges them, by hand and at phase close.
- A bar that stops mid-tier with no summary line was terminated, not
  failed: a test error still prints a summary, and pytest locks a live
  run's default basetemp, so concurrent runs do not prune each other
  (checked on pytest 9.1.1). A lane and parent pair died that way beside
  two builders on 2026-10-18d, cause unknown. Write every bar to a fresh
  log path so the dead run's output survives, re-run it, and file a
  defect row with the kept log if it recurs.
- Never grep the whole scratch root: its basetemps hold gigabytes, and
  a recursive search there outran the tool's two-minute cap
  (2026-10-17). Never grep `tests/test_module_size_ratchet.py` with a
  pattern its notes may hold: each stamp's history is one line tens of
  kilobytes long, and one hit spent about ten thousand tokens of
  context (2026-10-18a).
- **POSIX evidence on this workstation** (owner, wi-931 D-002): WSL's
  Ubuntu distro (Python 3.12, pytest 7.4, no xdist; nothing installed).
  Name it, `wsl.exe -d Ubuntu`: the default distro here is
  `podman-machine-default`, which has no git. Run the same modules at
  the lane's base in the same clone, so a red the base shares is not
  charged to the lane (two `run.command` cases, 2026-10-18c).
  To confirm that a fix's regression test fails on the pre-fix code on
  POSIX, check out the pre-fix scripts over today's tests in the WSL
  clone (`git checkout <pre-fix> -- project-trajectory scripts`), run the
  test, then restore (`git checkout FETCH_HEAD -- .`); a test that passes
  on both is a pin, not the convergence map's evidence (wi-927 D-011).
  Clone into WSL's own filesystem (`git clone /mnt/c/Projects/ai-template
  ~/<lane>-posix`, about a minute), check out detached, run serially. From
  Git Bash, prefix a `wsl.exe` call that passes a `/mnt/c/...` path with
  `MSYS_NO_PATHCONV=1`, or the path is rewritten.
  A record that names its checkout's HEAD (a plan's platform legs) can
  run from a detached scratch worktree at the recorded sha, which leaves
  the lane worktree free for a sitting whose commits would move its HEAD
  mid-run (wi-931 D-007).
- **Context:** the boot reading took about a quarter of the window on
  2026-10-14. Delegate long reads to sub-agents and read only their
  summaries and the sections you judge.
- The guard's relaunch has had no live verification. Check the current
  handoff and supervise its first unverified use.
- Unset `MSYS_NO_PATHCONV` in a shell that runs pytest: exported, it
  breaks the shallow-clone tests' `git clone` of a file URI ("'/C:/...'
  does not appear to be a git repository"; WI-913, 2026-10-15).

## 8. Re-judge and consolidation recipes

- **A disposition row's lane** (WI-953): compose and sit it from the lane
  (recipes §1, Adjudication), then close it with
  `handback.close_adjudication(Path(".").resolve(), "<branch>")` from the
  lane root. It moves the row to `docs/work/complete/` with its Deliverable
  and `specref = ""` and commits with the run's trailer; land the lane
  as any other, and the sweep (`--merged` naming the row) mints each
  drafted successor.
- **A disposition whose successor was filed by hand** (WI-894, WI-969):
  the filed row's `supersedes` names the closed row, and the verdict adopts
  it (`adopts = "WI-NNN"` in its `## Dispositions`) rather than drafting a
  duplicate. An adopting disposition closes through
  `handback.close_adjudication`, which writes the `adopted` record, and
  lands inside the squash, never by a hand close, which the
  adoption-record step refuses. An inbound link elsewhere in the repository
  needs no workaround: the close's exact relink is admitted. A verdict that
  neither drafts nor adopts is still refused at the close and at the
  landing's sweep (OI-73). Since WI-901 (2026-10-11) a close whose commit
  range is empty composes its disposition brief.
- **Close a lane partial for an owner decision** (OI-70: never park it
  claimed). Save any uncommitted build outside the repository and revert the
  lane first: `handback.close_partial` commits residue as-is with the hook
  skipped. Call it as `handback.close_partial(Path(root).resolve(), branch,
  reason, fields)` (a `str` root raises), from the primary checkout; then
  land the lane, re-home every open row that hard-depends on the closed one
  (`check_trajectory` names them as dead-dep), and sweep, which mints the
  disposition row. `fields` names every lane commit in `keep_commits` or
  `discard_commits` (`git rev-list --reverse <base>..<lane>`). When no row
  carries the closed row's scope yet, the landing softens each such edge
  to `~WI-NNN`, recorded as a decision, and the successor takes the hard
  edge once minted (coordinator-2026-10-19 D-004).
- **Re-cut a lane instead of a long rebase** (coordinator-2026-10-14
  D-010): archive the old tip whole to `archive/lanes` first, then
  `git -C <lane worktree> reset --hard <trunk tip>` on a clean worktree.
  `check-lane` reads the empty range as a person's lane, and the overnight
  launcher's audit passes the moved ref (wi-902, 2026-10-20).
- **Re-sit a closed consolidation by rewinding its lane.** The entry point
  refuses a sitting on a row no longer under `active/`. Reset the lane to
  before the close (archive the discarded commits), re-sit, then re-run
  `handback.close_adjudication` (it takes `Path(root).resolve()`, not a
  string).
- **A trunk edit to a queued row moves the consolidation digest,** and the
  close refuses as stale. Never re-stamp `digests` by hand; a sitting scoped
  to that move alone judges it and re-stamps it.
- **A hand-chosen consolidation cluster:** mint the `consolidate` row with
  `adjudicates` and `digests` (`consolidate.digests`); the composer needs
  every row queued and some mechanical overlap among them.

- **TC-055 (dashboard render):**
  - render with `scripts/dashboard-shots/shoot.mjs`;
  - cut tiles of at most 1500 px with Playwright clips;
  - run the judges per width, at about 5k tokens a tile with
    `codex exec -i <png>`, splitting a 120-tile width by theme;
  - an anchor with only MINOR findings passes;
  - the judges' model family differs from the rendering author's.
- **TC-279:** the part population is `gen_arch_map.declaration_sites`, never a
  hand-written scan. Record the first result only after the case is approved.
