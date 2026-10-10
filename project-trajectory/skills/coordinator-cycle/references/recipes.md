# Coordinator recipes

The exact commands and the traps behind each step of the coordinator cycle
([../SKILL.md](../SKILL.md)). Paths assume the primary checkout
`C:/Projects/ai-template`, lanes under `C:/Projects/ai-template.wt/wi-NNN`,
and the coordinator tools in `C:/Projects/ai-template.wt/coordinator-tools/`
(this repo's working setup, outside the repository; its README documents only
part of it).

Use **Git Bash** for the commands below. Run kit commands from the checkout
being operated on: trunk for claims/landings, the lane for authoring and
adjudication. Substitute placeholders, and set these in each shell:

```bash
PY=C:/Projects/ai-template/.venv/Scripts/python.exe
TOOLS=C:/Projects/ai-template.wt/coordinator-tools
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
  it never produced. Brief a hook's coverage as reading the command word the
  way the shell grammar does, from a list you give; a brief asking for every
  form that gets past the hook was cut off by a safety classifier (WI-834).
- **Terra, first turn:**
  `bash "$TOOLS/terra_author.sh" <lane> <prompt> <out> [effort]`.
  - Fill `"$TOOLS/terra-spine-prompt.template.md"` with `mkprompt.py`, then add
    the intent or checkpoint instructions from the skill. Its default brief
    does not request a whole subtree or arms map.
  - The script runs `codex exec -m gpt-5.6-terra` at medium with the
    unelevated sandbox, workspace-write,
    `--add-dir C:/Projects/ai-template.wt/review-tmp` and
    `--skip-git-repo-check`. It exits 3 if HEAD moved.
  - Note the `session id:` line in its log.
- **Terra, resumed.** Run this from the lane directory; `resume` takes no `-s`
  or `-C`:
  `codex exec resume <session id> -m gpt-5.6-terra -c model_reasoning_effort="medium" -c 'windows.sandbox="unelevated"' -c 'sandbox_mode="workspace-write"' -c 'sandbox_workspace_write.writable_roots=["C:/Projects/ai-template.wt/review-tmp"]' --skip-git-repo-check -o <out> - < <prompt>`
  Keep the quoting exactly as shown.
- **Sol review: render, launch, file.** Never write a review brief by hand.
  1. Render from the lane root:
     `"$PY" "$SCRIPTS/review_brief.py" review --wi WI-NNN --base <sha> --sha <tip> --scope narrow|full --tests <files> --scratch <dated root> --rubric docs/rubrics/kit-change-review.md --out <brief>`.
     A narrow round adds `--findings <the round file it answers>`; the
     full-lane gate names none and runs from the lane's trunk base. The brief
     names the verdict path under the scratch root.
  2. Append to the brief only what the template cannot know: for a narrow
     round, that row wording is deferred to the checkpoint; the prior coverage
     plan, with an unlisted-site probe per class. The template already cites
     the review threat model (PROCESS.md §6). Never add a builder
     self-assessment: a judge's brief carries no claim of the judged party.
  3. Launch `bash "$TOOLS/sol_review.sh" <lane> <brief> <out> [effort]`
     (default medium). Exit 3 means the reviewer changed the lane; inspect
     before trusting. The launcher uses workspace-write, because a read-only
     sandbox could not run Python, and checks HEAD and status afterwards.
  4. File it: `"$PY" "$SCRIPTS/review_brief.py" file --review <verdict path> --sha <tip> --scope narrow|full`
     writes `docs/reviews/<lane>/NNN-REVIEW-A-<sha7>[-narrow].md`. It refuses
     a review not opening `Reviewed: <full sha>`, or without exactly one
     `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<n>` line whose count
     matches its findings. It picks `NNN` itself: read the filed name before
     a commit subject or brief cites the round.
  - With Codex capacity short, run two lanes' Sol reviews one at a time, so a
    usage limit takes out at most one review.
- **Scope critique:** render
  `"$PY" "$SCRIPTS/review_brief.py" critique --wi WI-NNN --rubric docs/rubrics/scope-critique.md --scratch <dated root> --out <brief>`,
  add the skill's two scope and trust questions, and send it to a fresh Sol
  session. Record the answer before the claim.
- **Coverage plan (rework):** from the lane root,
  `"$PY" "$SCRIPTS/plan_coverage.py" --item <spec> --findings <round file> <plan>`.
  Dispatch the fix only on exit 0. A finding a dispute sitting dismissed is
  excluded citing that verdict:
  `Excludes: F2 — dismissed: docs/reviews/<lane>/NNN-ADJUDICATE-<sha7>.md#<its id there>`.
  The gate refuses a cite that is not an accepted DISMISS of that finding, or
  whose findings file beside the verdict records another finding under that
  id. Until WI-878 binds the findings file into the sitting, keep finding ids
  unique within a lane: a second dispute reusing ids refuses a valid
  dismissal.
- **Closure checks,** from the lane root:
  `"$PY" "$SCRIPTS/trace.py" --strict-integrity` and
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
     `done-when`); `<srs>` is the semicolon-joined SR scope. Single-kind briefs
     use bare ids. An empty section refuses the entire composition. Include
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
  4. Run it in the background (a headless leg: foreground, §7), because a
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
  6. After each call, read `C:/Projects/ai-template/out/adjudicator/*.json`
     (`state`, `pct`, `reset_reason`); the store is under the primary checkout.
  7. The adjudicator commits its verdict and its act. The entry point commits
     the telemetry.
- **Dispute sitting,** from the lane root:
  1. Write the findings file beside the verdict it will get,
     `docs/reviews/<lane>/NNN-DISPUTE-findings.toml`, in the shape
     `project-trajectory/scripts/kitlib/dispute.py` declares: `range =
     "<base>..<head>"`, then one `[[finding]]` table per finding with exactly
     `id`, `held_by` (`builder` or `coordinator`), `finding` (the reviewer's
     text verbatim) and `position` (the holder's position verbatim). Keep the
     file after the sitting: the coverage gate reads it.
  2. Compose: `"$PY" "$TOOLS/compose_lane.py" WI-NNN dispute "<findings path>" "" <verdict> <brief>`
     (a row whose `Brief` is `dispute` and whose `Adjudicates` names the
     findings file, through `adjudicate_brief.compose`).
  3. Run `adjudicate --brief dispute` as above. The verdict rules each
     finding once: `RULING: <id> FIX|DISMISS <class>|ESCALATE <why>`, the
     dismissal classes being `out-of-scope`, `refuted` and `not-worth-cost`.
  4. Record each ruling in the response to the review and in the lane's
     `docs/decisions/<branch>.toml`. An ESCALATE goes to the owner.
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
   for each row. Branch names are single-segment.
5. Restore the pause byte-identical in the next commit, again with the
   regenerated `docs/open-items.html`, even if a claim failed.

The pause gates claims only; acts, landings and sweeps run under it. `claim`
refuses a row whose id appears in `status.md`'s hand text, so describe rows
there by subject; reword an offending line in its own trunk commit before the
claim. A branch cut at the claim lacks the restored pause: while it has no
commit of its own, move it to trunk's tip
(`git branch -f wi-NNN <trunk tip>`), then add its worktree with
`git worktree add C:/Projects/ai-template.wt/wi-NNN wi-NNN`.

## 3. Landing

- **Restore trunk-only views before the final gate.** These are
  `PROJECT_STATE.html`, the generated part of `docs/status.md`, `docs/stage`,
  `docs/open-items.html`, `docs/requirements/components.derived.toml`,
  `docs/cli-reference.md` and `docs/interface-reference.md`. Preserve authored
  status text. The hand path regenerates views during iteration; restoring
  them keeps the final range to authored work. Normal claimed work branches
  skip these freshness gates in `check.py`; this is a hand-path convention,
  not a requirement imposed by every lane commit's hook. Keep the lane's
  module-size stamp (`linecounts` in `tests/test_module_size_ratchet.py`).
- **Rebase, even when trunk moved only by the pause restore.** Text-then-act
  exempts a squash only of a tip that contains HEAD. Conflicts: §4.
- **Complexity on the merged tree:**
  - Run `"$PY" "$SCRIPTS/check_complexity.py" --mode enforce`.
  - A module pushed past 1000 SLOC is decomposed, never bumped.
  - A baseline row that went down is deleted or lowered alone, in the lane
    commit that moved it (the hook refuses a stale row), in the tab-separated
    `docs/complexity-baseline`. Never run a full `--restamp`: it rewrites every
    row's line count and writes any row that grew.
- **The adjudicator's act** (last spine commit; session telemetry may follow):
  1. Stash the act files.
  2. Commit the verdicts.
  3. Pop the stash.
  4. Commit the act: Status flips and the snapshot only.

  Name CLARITY rows and retired rows in `--reattests`. For held-rung CLARITY
  re-attests, pass `--verdict <path>` naming the ruling. Take one act per kind
  of judgement, in the combined brief's order: the amendment act
  (`--reattests`) first, then the first-approval act (`--approves`). A
  first-approval copy is refused while an approved row in its registry still
  drifts unattested, and the amendment act clears that drift first. The old
  single act covering both kinds is retired, because the spine is decomposed
  one way in every mode (owner, 2026-10-07). This order is not yet proven on a
  same-registry checkpoint, so record the first one. `--approves` splits on
  `;`, so never put one in a ref. A traced-only change owes no sitting.
  If the squash touches
  its snapshot, re-anchor it with
  `"$PY" "$SCRIPTS/intake.py" snapshot --approves "<registry>=<ref>"`.
- **Squash** on trunk with `git merge --squash <lane>`, one per lane. Cite
  the lane's SOUND full-lane review in the command's description: the
  auto-mode classifier has refused an uncited squash as an unreviewed merge.
  If the lane recorded an owner overrule in
  `docs/decisions`, land two commits: the squash up to the commit before the
  close, then the close. Ruling-sync needs an open item citing the overrule.
- **Regenerate** with `"$PY" "$SCRIPTS/trunk_step.py" --regen`. By hand, the traps are:
  - pass `--src project-trajectory/scripts` to both `gen_arch_map.py` forms (a
    bare `--contracts-doc` wipes the interface reference);
  - regenerate `docs/ratify/CURRENT.md` with
    `"$PY" "$SCRIPTS/trace.py" --approve modified --out docs/ratify/CURRENT.md`.
- **Run `"$PY" "$SCRIPTS/check_trajectory.py" --strict` before the landing
  commit.** The hook runs the non-strict form, so R-F (a closed row's
  `specref`) passes it. A lane that adds a doc also runs
  `"$PY" "$SCRIPTS/check_docs.py" --root . --strict-orphans`: the orphan check
  runs only in the full suite.
- **Close the row:**
  - `## Deliverable` comes before `## Context`, because the parser clips
    everything after Context (the hook refuses a missing one, R-A);
  - `specref = ""` on the closed row only: an open row's specref must resolve
    (R-E), and never to a log fragment, which compiles away;
  - `"$PY" "$SCRIPTS/spec_move.py" <src> docs/archive/work/complete/<name>.md`, never
    `--archive`;
  - scrub the id from `status.md`'s hand text in the same commit;
  - keep hand-filed slugs to the handoff's 37-character ceiling; the kit's
    spec writer uses a 30-character title prefix (`wi_convert.SLUG_CHARS`).
- **RESYNC:** anchor the entry at the landing's parent, never at a lane-only
  sha. Fold a fix round's entry into its parent entry, and flag forced
  migrations.
- **Archive the tips** to `archive/lanes`, adding the pre-rebase tip the
  verdicts cite (and any discarded act) as extra parents. Archive commits
  carry the empty tree, `4b825dc642cb6eb9a060e54bf8d69288fbee4904`. Read the
  old tip with `git rev-parse archive/lanes`. Create the archive
  commit with `git commit-tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904 -p <old-archive-tip> -p <rebased-tip> -p <pre-rebase-tip> -F <archive-message>`;
  add a `-p <discarded-act>` for each discarded act. Record its output id,
  then run `git update-ref refs/heads/archive/lanes <new-archive-commit> <old-archive-tip>`.
  Verify the parents with `git show -s --format=%P archive/lanes` before
  treating the lane as archived.
- **Sweep:** `"$PY" "$SCRIPTS/intake.py" sweep --merged "WI-a;WI-b" --branch <lane> --before <trunk before> --after <landing>`.
  `--merged` names every row the landing closed, or other rows' Dispositions
  are skipped silently. The sweep mints first, and its re-mint takes the next
  WI id: file hand rows after it, or cite them by subject until filed.
- **The re-mint:** close it citing the act once `cmp` shows the registries
  equal their anchors. Two minted rows are real work and stay open: an
  observation re-judge whose trigger fired, and a goalposts row.
- **Review rollup:** restore `docs/reviews/rollup/` to its trunk version before
  committing the lane. `trunk_step.py --regen` writes it on trunk at landing,
  from the round files the lane brought in.
- **Messages:** write each to a file and use `git commit -F <file>`. Never
  reuse a message file across a lane act and a trunk landing.

## 4. Rebasing

In a rebase, "ours" is the tree already replayed onto trunk; "theirs" is the
lane commit being replayed.

| File | Take |
|---|---|
| Generated views | `git checkout --ours`, continue, regenerate once at the end |
| Registries | resolve per table using this replay's base/ours/theirs (`git show :1:<path>`, `:2:<path>`, `:3:<path>`); keep independent changes from both sides and judge same-row conflicts; never take the whole file `--ours` |
| `docs/id-watermark` | `--ours`, then `"$PY" "$SCRIPTS/trace.py" --bump-ids`; preserve any higher mark for retired lane ids |
| RESYNC_PACK | both sides' entries, trunk's first; when the replayed commit rewrites the lane's own earlier entry, keep its rewrite and drop the entry it replaces |
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

- Write UTF-8 only, with LF line endings. Terra has left CRLF and cp1252
  dashes; normalize before any snapshot.
- Re-read every whole cell a splice touches. Spliced sentences have come back
  without a verb.
- If `apply_patch` cannot match a long one-line cell, use a guarded Python replace:
  - read and write with `newline=""`;
  - assert each old value occurs once;
  - check with `tomllib` that list cells stay lists.
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

## 6. Commits and hooks

- Run the smoke tier on every commit, docs-only ones included. The commit
  hook does not run it: run `python -m pytest -q -n auto -m smoke` and
  `python scripts/check_smoke_budget.py --mode enforce` yourself, before a
  landing commit rather than after it.
- A commit sometimes exits 1 with every hook step passing. Read the hook
  output and retry with `-F`; never skip the hook.
- On trunk (or `check.py --trunk-lane`), `approval-fresh` refuses a stale
  `docs/ratify/CURRENT.md`. Regenerate it and read what it lists before an act.
- Where freshness is gated, `interface-reference` refuses a stale view after
  a declared header or contract changes; regenerate it.
- `skills-sync` drift: run `"$PY" "$SCRIPTS/bootstrap.py" --dest . --sync`
  in every lane commit that touches a kit skill.
- Redirect each commit's output to a file: the pre-commit hook prints about
  80 KB.
- The secrets floor refuses a fake token shaped like a real one in a test;
  mark that line `privacy-ok`.
- `gen_verdict_rollup.py` refuses on a work branch; a lane that changes how
  rounds read leaves its rollups to the trunk landing.
- `git add -A <paths>` aborts entirely if one path is missing. `2>/dev/null`
  hides that, and `staged-divergence` then fails. `components.derived.toml`
  lives under `docs/requirements/`.
- Specref anchors take plain headings (no backticks or apostrophes), one
  anchor per row.

## 7. Environment and limits

- **Codex usage limit:** wait for the reset the CLI error names. Retain Terra
  and keep review rounds narrow; observed session counts are not a quota.
  Every Codex call runs through the `codex` CLI on `PATH`; the owner switches
  accounts with `codex logout` and `codex login`.
- **Background or foreground.** In an attended session, start each Codex call
  as its own background command; one started in a detached subshell sends no
  notification. A headless leg (`claude -p`, the overnight launcher
  `"$TOOLS/overnight_legs.py"`) kills its background tasks when it exits, so
  it runs everything in the foreground under the raised shell cap.
- Set `export MSYS_NO_PATHCONV=1`; Git Bash rewrites leading-slash arguments.
- **Scratch:** one dated root, `C:/Projects/ai-template.wt/review-tmp/<date>-<session>/`, with one literal
  `--basetemp` per kind of run (`$TEMP` is empty in the Codex shell). Delete
  the root once results are recorded.
- **Full suite:** past runs used about 4 GB of basetemp. Check `(Get-PSDrive C).Free`
  in PowerShell first,
  run from a detached worktree in the background, and delete the basetemp
  after recording.
- **A smoke budget breach under load:** time the parent commit in the same
  window before charging the breach to the change; record both readings in
  the commit message and re-measure quiet before landing.
- The guard's relaunch has had no live verification. Check the current
  handoff and supervise its first unverified use.

## 8. Re-judge and consolidation recipes

- **Re-sit a closed consolidation by rewinding its lane.** The entry point
  refuses a sitting on a row no longer under `active/`. Reset the lane to
  before the close (archive the discarded commits), re-sit, then re-run
  `handback.close_adjudication` (it takes `Path(root).resolve()`, not a
  string).
- **A trunk edit to a queued row moves the consolidation digest,** and the
  close refuses as stale. Never re-stamp `digests` by hand; a narrow sitting
  judges the move and re-stamps it.
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
