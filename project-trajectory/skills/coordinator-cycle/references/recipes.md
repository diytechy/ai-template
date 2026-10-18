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
  Brief a hook's coverage as reading the command word the
  way the shell grammar does, from a list you give; a brief asking for every
  form that gets past the hook was cut off by a safety classifier (WI-834).
  A plan that orders its commits (a pin, then a structural move alone,
  then the rest) is built in stages: the builder stops after each, you
  verify and commit, and SendMessage resumes the same builder (WI-911,
  2026-10-15). A blank line ends a `Contract IF-NNN:` body for the
  interface reference, so text added to a contract continues the body
  without one (wi-922 D-003).
- **Terra, first turn:**
  `bash "$TOOLS/terra_author.sh" <lane> <prompt> <out> [effort]`.
  - Fill `"$TOOLS/terra-spine-prompt.template.md"` with `mkprompt.py`, then add
    the intent or checkpoint instructions from the skill. Its default brief
    does not request a whole subtree or arms map.
  - The script runs `codex exec -m gpt-5.6-terra` at medium with the
    unelevated sandbox, workspace-write,
    `--add-dir` on the review scratch root (`$REPO.wt/review-tmp`) and
    `--skip-git-repo-check`. It exits 3 if HEAD moved.
  - Note the `session id:` line in its log.
  - `mkprompt.py` takes `LANE=<branch>` (`wi-912`), never the worktree
    path, which builds a broken `--basetemp` (`C:-Projects-...`).
  - Launched through `lowprio.py` with Git's `usr/bin/bash.exe`, the
    script's bash exited 127 after about ten minutes while `codex exec`
    ran on, orphaned, and wrote its `-o` report when it finished: wait on
    the codex process (`tasklist`), never relaunch. A resumed turn ran
    cleanly with `lowprio.py` launching the vendored `codex.exe` directly
    (under the npm `@openai/codex` package's `vendor/` folder), which keeps
    the `-c` quoting intact (WI-912, 2026-10-17).
- **Terra, resumed.** Run this from the lane directory; `resume` takes no `-s`
  or `-C`:
  `codex exec resume <session id> -m gpt-5.6-terra -c model_reasoning_effort="medium" -c 'windows.sandbox="unelevated"' -c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.writable_roots=["C:/Projects/ai-template.wt/review-tmp"]' --skip-git-repo-check -o <out> - < <prompt>`
  Keep the quoting exactly as shown. The writable root is the review scratch
  root, `$REPO.wt/review-tmp`: on a checkout elsewhere, write that path in
  place of the literal, inside the same quotes.
- **A review round: render, launch, file** (SKILL Roles and §3; rulings 4
  and 7, revision 37). Never write a review brief by hand. Every round is
  full-lane, from the lane's trunk base to its tip, and runs REVIEW-A and
  REVIEW-B in parallel, each from its own render with its own scratch
  directory (so its own verdict path and `--basetemp`).
  1. Render from the lane root, once per reviewer:
     `"$PY" "$SCRIPTS/review_brief.py" review --wi WI-NNN --base <trunk base> --sha <tip> --scope full --tests <files> --scratch <dated root>/<reviewer> --rubric docs/rubrics/kit-change-review.md --out <brief>`.
     `--tests` takes the files as separate arguments; one quoted string
     renders as a single bogus path in the brief's pytest line.
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
  3. Launch REVIEW-A with `bash "$TOOLS/sol_review.sh" <lane> <brief> <out> [effort]`
     (default medium). Exit 3 means the reviewer changed the lane; inspect
     before trusting. Edit nothing in a lane while its reviewer runs: the
     check counts your own edit too (WI-911, 2026-10-15). The launcher uses workspace-write, because a read-only
     sandbox could not run Python, and checks HEAD and status afterwards.
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
     fresh one (WI-921's gate, 2026-10-15g).
  4. File each: `"$PY" "$SCRIPTS/review_brief.py" file --review <verdict path> --sha <tip> --scope full --phase REVIEW-A`
     (or `--phase REVIEW-B`) writes `docs/reviews/<lane>/NNN-<phase>-<sha7>.md`.
     It refuses a review not opening `Reviewed: <full sha>`, or without
     exactly one `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<n>` line
     whose count matches its findings. It picks `NNN` itself: read the filed
     name before a commit subject or brief cites the round. Each round file
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
  session. Record the answer before the claim. In an attended session, put
  the spec's filing calls to the owner first and record them under
  `## Calls ruled at filing`, so the critique judges the ruled spec (WI-921
  to WI-923, 2026-10-15). `review_brief.py critique`
  names the same verdict path every round (`WI-NNN-scope-critique.md`): move
  the previous round's file aside before rendering the next. Ask in the same brief for a ruling per
  consumer and for every carrier's failure contract (producer, write route,
  failed-write shape): asked piecemeal, they cost WI-882, WI-884 and WI-887
  three rounds each (2026-10-10).
  Run each critique from a detached scratch checkout at the committed tip
  (`git -C "$REPO.wt/trunk-tmp" checkout --detach <tip>`): the launcher
  compares the checkout's HEAD and status before and after, so the
  coordinator's own uncommitted trunk edits would read as the critic's.
  Several critiques may run at once from that one checkout, each with its own
  scratch directory (2026-10-14).
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
     `bash "$TOOLS/sol_review.sh" <lane> <brief> <out>`. Each round has its
     own verdict path, `WI-NNN-plan-critique-<n>.md`. Append one line to
     every critique brief naming that path and saying to commit nothing,
     run no `plan-file` and change no file in the checkout: with it, eleven
     plan critiques left their lanes untouched (2026-10-18a). Several
     lanes' plans, critiques and records run in parallel, each from its
     own lane, its records committed alone behind its own bar.
  4. File: `"$PY" "$SCRIPTS/review_brief.py" plan-file --wi WI-NNN --critique <verdict> --sha <plan commit>`
     writes `docs/plans/WI-NNN/critique-<n>.md`; commit it alone. The
     critic may file it first: Sol ran `plan-file` in the lane and tried to
     commit (WI-911, 2026-10-15; the launcher exits 3). Move its copy
     aside, file the verdict yourself, and compare the two. Never rebase
     the lane between a critique's verdict and its filing: filing needs
     the reviewed commit to be an ancestor of HEAD, so a rebase orphans it
     and the filing refuses. Reset to the pre-rebase tip, file, then
     rebase (wi-931 D-001, 2026-10-16d).
  5. Pass: `"$PY" "$SCRIPTS/review_brief.py" plan-file --wi WI-NNN --pass`
     writes `docs/plans/WI-NNN/pass.toml` (refused, writing nothing, unless
     the critique reads as an APPROVE); commit it alone.
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
     contested, say so, and that the cap routes it, taking no side.
     Two lanes' sittings have run in parallel (2026-10-18b). Sit it; commit;
     then `plan-file --wi WI-NNN --pass --dispute <verdict path>`. Anything
     but an accepted DISMISS of every one is the owner's: close the lane
     partial.
  An edited plan or Done-when unbinds the record: remove it, and a fresh
  critique (the cap still counts) must pass the changed plan.
  A row claimed `single` whose lane already holds build commits before its
  pass record fails the landing walk at each of them: rebase those commits
  onto the plan, critique and pass commits, or re-cut the lane and run the
  plan step first.
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
     always `combined`, even when only amendments are owed: sitting 010,
     composed as the single-kind `amendment` class, came back with a
     `## amendment` section the one verdict parser refuses for a single-kind
     brief, after its act was committed, and was discarded (wi-921 D-018).
     Single-kind briefs use bare ids. An empty section refuses the entire composition. Include
     affected chain rows in the appropriate scope and supply the arms map
     as an additional input; the composer does not generate it.
  2. Name the verdict `docs/reviews/<wi-slug>/NNN-ADJUDICATE-<lane sha7>.md`.
  3. Check sign-in. The retained Claude home authenticates with the owner's
     long-lived token, read at each launch from the file the
     `AGENT_CLAUDE_TOKEN_FILE` environment variable names. Set that variable
     to the path in the launching shell; never read the file, and never put
     the token in a brief, log or commit. It is the launch's one environment
     credential: an ambient `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` or
     cloud-provider switch is left out, and a route declaring one (or
     `--bare`) is refused. Settings-file credentials (`apiKeyHelper`, a
     settings `env` block, a managed gateway) are not checked: keep them out
     of this repo. Then run
     `"$PY" "$SCRIPTS/coordinator_adjudicate.py" signin` and read
     `signed-in`, `missing` or `unknown`; `signin` itself always exits 0.
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
       credential. The remedy for a home that is not signed in is dev-setup's
       one-time `claude setup-token` step (`scripts/dev-setup.*`) and the
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
   `docs/open-items.html`. It counts as reviewed when it passes the commit bar
   and cites the owner's authorization.
3. Confirm HEAD moved. `claim` reads the **working-tree** pause.
4. Run `"$PY" "$SCRIPTS/integrate.py" claim --wi WI-NNN --branch wi-NNN`
   for each row. Branch names are single-segment. A claim that exits 127
   with an empty log never launched (two of four did, 2026-10-17e):
   retry it, and read `git log` for its claim commit.
5. Restore the pause byte-identical in the next commit, again with the
   regenerated `docs/open-items.html`, even if a claim failed.

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
  amendment sitting for it, and the re-anchor is the step (WI-902, act 117). The bar command on the staged squash (below) catches
  this drift; the lane hook does not.
- **A return in a sitting holds its whole registry.** A row the sitting
  would bless is not anchored while another row in the same registry is
  returned; rework the returns and re-sit them all together. Move each
  answered verdict's `## Dispositions` under another heading in the lane,
  or the landing sweep mints the rework rows.
- **Squash** on trunk with `git merge --squash <lane>`, one per lane. In a
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
    in the same close, or R-F refuses it (WI-923, 2026-10-16);
  - scrub the id from `status.md`'s hand text in the same commit;
  - keep hand-filed slugs to the handoff's 37-character ceiling; the kit's
    spec writer uses a 30-character title prefix (`wi_convert.SLUG_CHARS`).
- **RESYNC:** anchor the entry at the landing's parent, never at a lane-only
  sha. Fold a fix round's entry into its parent entry, and flag forced
  migrations.
  The bar's `check_resync` refuses every commit of a lane rebased past
  WI-916 until its entry exists, so a plan step that writes the entry
  later moves into the first commit after the rebase (wi-927 D-005).
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
- Launch no review until the rebase has finished. A rebase stopped on
  generated-file conflicts leaves the lane mid-rebase: take `--ours`,
  regenerate, continue, then render the brief at the real tip.

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
- Keep an IF Data cell to 160 characters, with the definition in the owner's
  contract body.
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
- Check an intent or reconcile set mechanically before committing it: in
  each changed cell of an approved row the approved text must occur
  verbatim (old within new, read with `tomllib`; judge a tier or list
  cell by hand). Terra reworded two approved phrases in SR-233 while
  reporting every approved text kept: restore the approved bytes by a
  guarded replace, keep its addition, and record it (wi-911 D-007,
  2026-10-15).
- An interface row names no file in any cell; a "No tie-back" note belongs
  only to a row with an `external:` party.
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

## 6. Commits and hooks

- Run the commit bar on every commit, docs-only ones included: the one
  declared command, `run.cmd smoke` (`"$PY" "$SCRIPTS/run_menu.py" smoke` from
  a shell), whose steps are `docs/stack.ini` `[run] smoke`. Read the summary
  lines for `failed` and for each lint's findings before committing; a chain
  gated only on the command's exit code inside `$(...)` committed a red tier
  (2026-10-10). The commit hook does not run it: run it yourself, before a
  landing commit rather than after it.
- The declared bar runs the tier once: the lints run first, then the
  budget step's timed run, which exits with the tier's own code on a red
  tier and 1 on a breach. `--elapsed <s>` serves only a hand wrapper that
  still runs every `[run] smoke` step and times its own tier run. A
  wrapper must exit nonzero
  on a red tier or a breach: one that exited 0 let a chained `&& git
  commit` record a 66.2 s reading unmentioned (WI-921's pass record,
  its message amended, 2026-10-15).
- Time a breach's parent in a detached scratch worktree at the lane's
  HEAD (`git worktree add --detach <scratch>/parent-wt HEAD`, removed
  after), never by stashing an uncommitted build, and record both
  readings. Three reviewers running their suites in parallel took a
  parent to 86 s (2026-10-15): re-measure quiet before the landing.
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
  module's CMP, so Terra's intent rows for that stage ride the stage's
  commit, and the rest of the set follows the round (wi-912 D-003).
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
  read as UTF-8), then probe with a one-word `codex exec -m gpt-6.1-sol`
  call: the cache listed it and it worked again on 2026-10-10 at 22:40
  local (leg 02). While it is not offered, review with `gpt-6-luna` at high
  through `"$TOOLS/luna_review.sh"` (coordinator-2026-10-10 D-017, pending
  the owner) and record the substitution in every lane's decisions record.
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
  The shell has also rewritten `\n` and `\1` inside heredoc Python, in a
  builder's test strings and in a coordinator's log edit (WI-912,
  2026-10-17): tell every builder the same.
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
- **A smoke budget breach under load:** time the parent commit in the same
  window before charging the breach to the change; record both readings in
  the commit message and re-measure quiet before landing. When the
  owner's own applications load the box and the owner asks, run every
  local test job (bars, the full suite, Codex launches, the Claude
  reviewers' pytest) at below-normal priority through a stdlib wrapper
  (`subprocess.call(cmd, creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)`;
  Windows children inherit the class), naming Git Bash by its full path
  (`C:/Program Files/Git/usr/bin/bash.exe`), since Windows resolves a
  bare `bash` by its own search order (2026-10-15g). The wrapper resolves
  its program with `shutil.which`: a bare `codex` (an npm `.cmd` shim) is
  not found by `CreateProcess` (2026-10-16d). A landing no longer waits
  for a quiet box (owner, coordinator-2026-10-17 D-005): take the staged
  squash's reading beside its parent's in one window and record both in
  the landing commit. A breach close to the parent's reading on the same
  tier is load and holds nothing; one well above it, or a tier that
  grew, is the change's (WI-912's stage 2 read 26 s over its parent until
  its new module moved to `SLOW_MODULES`, wi-912 D-004). Your own parallel `-n auto`
  jobs (a builder's module runs, the full suite) push a lane bar to
  78 to 82 s: take lane bars between them, or re-take one quiet before
  its commit (2026-10-17).
  The owner kept D-012's rule under far heavier load (readings of 140 to
  1832 s, 2026-10-17b): take a commit's reading and its parent's side by
  side, the parent in a detached scratch worktree at the lane's HEAD, so
  the pair shares one window. A commit that changes only records
  (decisions, review files, a queued or closed spec, generated views)
  records its own reading and cites the session's latest same-window
  pairs instead; a commit that changes code or tests, or grows the tier,
  and every landing, still takes its own pair (coordinator-2026-10-17
  D-011, 2026-10-17e).
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

- **A disposition whose successor was filed by hand** (WI-894): the verdict
  drafts none, so `handback.close_adjudication` refuses (`owes_successor`)
  and the landing's sweep refuses the empty `## Dispositions` (OI-73).
  Until WI-902 lands, close the row by hand into `docs/work/complete/`
  citing the verdict, give the existing successor `supersedes`, and record
  the sweep's refusal; it mints nothing else. Since WI-901 (2026-10-11) a
  close whose commit range is empty composes its disposition brief.
- **Close a lane partial for an owner decision** (OI-70: never park it
  claimed). Save any uncommitted build outside the repository and revert the
  lane first: `handback.close_partial` commits residue as-is with the hook
  skipped. Call it as `handback.close_partial(Path(root).resolve(), branch,
  reason, fields)` (a `str` root raises), from the primary checkout; then
  land the lane, re-home every open row that hard-depends on the closed one
  (`check_trajectory` names them as dead-dep), and sweep, which mints the
  disposition row.
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
