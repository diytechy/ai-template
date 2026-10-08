# Coordinator recipes

The exact commands and the traps behind each step of the coordinator cycle
([../SKILL.md](../SKILL.md)). Paths assume the primary checkout
`C:/Projects/ai-template`, lanes under `C:/Projects/ai-template.wt/wi-NNN`,
and the coordinator tools in `C:/Projects/ai-template.wt/coordinator-tools/`
(untracked; its README documents only part of it).

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
8 Re-judge recipes

## 1. Invocations

- **Builder:** the Agent tool with `subagent_type: "kit-builder"`, given the
  lane path and the build prompt. If the type is not listed, use
  `general-purpose` with `model: "opus"` and have it read
  `.claude/agents/kit-builder.md`.
  Override that file's old scratch recipe with the dated root in §7. Grant
  trace-cell upkeep only during iteration; require the spine change list,
  the sweep table before fixes and the stop-and-file rule for consolidation
  outside the spec's surface in every build brief.
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
- **Sol:** `bash "$TOOLS/sol_review.sh" <lane> <prompt> <out> [effort]`
  (default high).
  - Fill `"$TOOLS/sol-review-prompt.template.md"` with
    `"$PY" "$TOOLS/mkprompt.py" <template> <out> KEY=VALUE ...`
    (slots WI, SHA, BASE, LANE, SPEC, NOTES, TESTS; an unfilled slot is
    refused).
  - Override its old `-n 2` and flat scratch path with `-n 0` and the dated
    root in §7. For narrow rounds, override "The requirement text itself"
    with the iterate-phase scope in the skill; retain the spec and Drafted
    intent as code obligations. At the full-lane gate, judge code and rows,
    allowing adjudicator Status flips backed by their verdicts and acts.
    Omit builder self-assessments from NOTES; carry findings and sweep evidence.
  - Add the kit reviewer template's failure-class and antidote questions,
    plus the prior sweep table and an unlisted-site probe per class. The local
    template lacks them. Rendering through `prompts.py` and wiring
    `plan_coverage.py --findings` are follow-up work, not live gates.
  - Exit 3 means the reviewer changed the lane; inspect before trusting.
  - The local read-only sandbox probe could not run Python; the launcher
    therefore uses workspace-write and checks HEAD/status afterwards.
  - Start each codex call as its own background command. One started in a
    detached subshell sends no notification.
- **Scope critique:** fill `project-trajectory/prompts/critique.template.md`
  with a written scope rubric, the spec/reading recipe and anchor intent in `{brief}`, and
  the assigned record path in `{verdict}`. Include the skill's two scope/trust
  questions. This template expects a rubric and artifact recipe; a bare spec
  is insufficient. Use a fresh Sol session and record the answer before claim.
- **Closure checks,** from the lane root:
  `"$PY" "$SCRIPTS/trace.py" --strict-integrity` and
  `"$PY" "$SCRIPTS/check_trajectory.py" --strict`.
  These operate on the whole repo; neither accepts a row-set filter. Check
  the set's parents, TC links, interface citations and arms map separately.
- **Adjudication,** from the lane root:
  1. Compose the brief:
     `"$PY" "$TOOLS/compose_lane.py" WI-NNN <brief> "<ids>" "<srs>" <verdict> <out>`.
     The classes are `amendment`, `first-approval`, `done-when`, `combined`,
     `disposition`, `consolidate`, `red-tc` and `rejudge`.
     For `combined`, `<ids>` is **kind-prefixed**, for example
     `"amendment:LLR-123;first-approval:SR-234;first-approval:LLR-345;first-approval:TC-456;done-when:WI-NNN"`.
     Include only kinds actually owed (`amendment`, `first-approval`,
     `done-when`); `<srs>` is the semicolon-joined SR scope. Single-kind briefs
     use bare ids. An empty section refuses the entire composition. Include
     affected chain rows in the appropriate scope and supply the arms map
     as an additional input; the composer does not generate it.
  2. Name the verdict `docs/reviews/<wi-slug>/NNN-ADJUDICATE-<lane sha7>.md`.
  3. Check sign-in: `"$PY" "$SCRIPTS/coordinator_adjudicate.py" signin`.
     Read `signed-in`, `missing` or `unknown`; `signin` itself always exits 0.
     Leave the verdict path absent: `adjudicate` reserves it exclusively.
  4. Run in the background, because a call can outlast the 10-minute tool cap:
     `"$PY" -u "$SCRIPTS/coordinator_adjudicate.py" adjudicate --brief-file <brief> --brief <class> --wi WI-NNN --verdict <path>`
  5. Read the exit code:
     - 0: a valid verdict (returns can still require rework);
     - 1: the call failed or the verdict is bad;
     - 2: refused before launch (for example, run from the primary checkout);
     - 7: the home is not signed in.
  6. After each call, read `C:/Projects/ai-template/out/adjudicator/*.json`
     (`state`, `pct`, `reset_reason`); the store is under the primary checkout.
  7. The adjudicator commits its verdict and its act. The entry point commits
     the telemetry.
  - Check the current handoff for sign-in state. Wave 18 reports headless OAuth
    refresh failures pending WI-846; the owner runs `/login` at expiry.
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
there by title. If `claim` did not cut the lane, cut it with
`git worktree add C:/Projects/ai-template.wt/wi-NNN wi-NNN` and merge trunk in,
before any spine row is committed.

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
  - A baseline row that went down is deleted alone from the tab-separated
    `docs/complexity-baseline`. Never run a full `--restamp`.
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
- **Squash** on trunk with `git merge --squash <lane>`, one per lane.
  If the lane recorded an owner overrule in
  `docs/decisions`, land two commits: the squash up to the commit before the
  close, then the close. Ruling-sync needs an open item citing the overrule.
- **Regenerate** with `"$PY" "$SCRIPTS/trunk_step.py" --regen`. By hand, the traps are:
  - pass `--src project-trajectory/scripts` to both `gen_arch_map.py` forms (a
    bare `--contracts-doc` wipes the interface reference);
  - regenerate `docs/ratify/CURRENT.md` with
    `"$PY" "$SCRIPTS/trace.py" --approve modified --out docs/ratify/CURRENT.md`.
- **Close the row:**
  - `## Deliverable` comes before `## Context`, because the parser clips
    everything after Context;
  - `specref = ""`;
  - `"$PY" "$SCRIPTS/spec_move.py" <src> docs/archive/work/complete/<name>.md`, never
    `--archive`;
  - scrub the id from `status.md`'s hand text in the same commit;
  - keep hand-filed slugs to the handoff's 37-character ceiling; the kit's
    spec writer uses a 30-character title prefix (`wi_convert.SLUG_CHARS`).
- **RESYNC:** anchor the entry at the landing's parent, never at a lane-only
  sha. Fold a fix round's entry into its parent entry, and flag forced
  migrations.
- **Archive the tips** to `archive/lanes`, adding the pre-rebase tip the
  verdicts cite (and any discarded act) as extra parents.
  Read the old tip and archive tree with
  `git rev-parse archive/lanes "archive/lanes^{tree}"`. Create the archive
  commit with `git commit-tree <archive-tree> -p <old-archive-tip> -p <rebased-tip> -p <pre-rebase-tip> -F <archive-message>`;
  add a `-p <discarded-act>` for each discarded act. Record its output id,
  then run `git update-ref refs/heads/archive/lanes <new-archive-commit> <old-archive-tip>`.
  Verify the parents with `git show -s --format=%P archive/lanes` before
  treating the lane as archived.
- **Sweep:** `"$PY" "$SCRIPTS/intake.py" sweep --merged "WI-a;WI-b" --branch <lane> --before <trunk before> --after <landing>`.
  `--merged` names every row the landing closed, or other rows' Dispositions
  are skipped silently. The sweep mints first, so allocate ids only after it.
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
| RESYNC_PACK | both sides' entries, trunk's first |
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
- Ids collide across unlanded lanes. Brief Terra with every open lane's ids,
  or renumber before the act.

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
- The local Codex sandbox has failed shallow-clone tests and `git worktree add`,
  and hit Windows locks at `-n 2`. Ask for `-n 0`; confirm those failures with
  decisive tests outside that sandbox before treating them as code defects.

## 6. Commits and hooks

- Run the smoke tier on every commit, docs-only ones included.
- A commit sometimes exits 1 with every hook step passing. Read the hook
  output and retry with `-F`; never skip the hook.
- On trunk (or `check.py --trunk-lane`), `approval-fresh` refuses a stale
  `docs/ratify/CURRENT.md`. Regenerate it and read what it lists before an act.
- Where freshness is gated, `interface-reference` refuses a stale view after
  a declared header or contract changes; regenerate it.
- `skills-sync` drift: run `"$PY" "$SCRIPTS/bootstrap.py" --dest . --sync`.
- `git add -A <paths>` aborts entirely if one path is missing. `2>/dev/null`
  hides that, and `staged-divergence` then fails. `components.derived.toml`
  lives under `docs/requirements/`.
- Specref anchors take plain headings (no backticks or apostrophes), one
  anchor per row.

## 7. Environment and limits

- **Codex usage limit:** wait for the reset the CLI error names. Retain Terra
  and keep review rounds narrow; observed session counts are not a quota.
- Set `export MSYS_NO_PATHCONV=1`; Git Bash rewrites leading-slash arguments.
- **Scratch:** one dated root, `C:/Projects/ai-template.wt/review-tmp/<date>-<session>/`, with one literal
  `--basetemp` per kind of run (`$TEMP` is empty in the Codex shell). Delete
  the root once results are recorded.
- **Full suite:** past runs used about 4 GB of basetemp. Check `(Get-PSDrive C).Free`
  in PowerShell first,
  run from a detached worktree in the background, and delete the basetemp
  after recording.
- Wave 18 carries no live guard-relaunch verification. Check the current
  handoff and supervise the first unverified use.

## 8. Re-judge recipes

- **TC-055 (dashboard render):**
  - render with `scripts/dashboard-shots/shoot.mjs`;
  - cut tiles of at most 1500 px with Playwright clips;
  - run the judges per width, at about 5k tokens a tile with
    `codex exec -i <png>`, splitting a 120-tile width by theme;
  - an anchor with only MINOR findings passes;
  - the judges' model family differs from the rendering author's.
- **TC-279:** the part population is `gen_arch_map.declaration_sites`, never a
  hand-written scan. Record the first result only after the case is approved.
