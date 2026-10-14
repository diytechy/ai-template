# Coordinator tools (outside the repo; wave 8, 2026-10-03)

Run from the repo root with the repo venv.

- `compose.py WI-NNN <verdict-path> <out.md> [WI-MMM <verdict> <out> ...]`:
  composes each adjudication row's kit brief through
  `adjudicate_brief.compose`. Verdict paths are repo-relative, e.g.
  `docs/reviews/wi-NNN-<slug>/001-ADJUDICATE-<trunk sha7>.md`.
- `toml_merge3.py <branch> <registry paths...> [--out-dir DIR]`: a table-wise
  three-way merge of `[kind.ID]` registry blocks, from the merge base. Run it
  after `git merge --squash <branch>` hits conflicts in a registry. It refuses
  on a true per-table conflict.

## Codex Luna review through the CLI (owner, 2026-10-03)

1. Fill the reviewer prompt. Slots: WI, SHA, BASE, LANE, SPEC, NOTES and TESTS;
   LANE_SLUG is derived. An unfilled slot is refused.

       .venv/Scripts/python.exe C:/Projects/ai-template.wt/coordinator-tools/mkprompt.py \
         C:/Projects/ai-template.wt/coordinator-tools/review-prompt.template.md <scratch>/review-wi-NNN.md \
         WI=WI-NNN SHA=<lane tip> BASE=<trunk at cut> LANE=build/wi-NNN \
         SPEC=docs/work/queued/WI-NNN-<slug>.md NOTES="<paths to builder report / prior reviews>" \
         TESTS="tests/test_a.py tests/test_b.py"

2. Launch it, from the Bash tool with `run_in_background: true`. The effort
   defaults to high.

       bash C:/Projects/ai-template.wt/coordinator-tools/luna_review.sh \
         C:/Projects/ai-template.wt/wi-NNN <scratch>/review-wi-NNN.md <scratch>/luna-wi-NNN.md

   The review goes to `<out>`, the CLI transcript to `<out>.log`, and the first
   line is echoed (`<sha> SOUND` or `<sha> NOT YET SOUND`).
   - Exit 3 means the reviewer changed the lane. Inspect `git status` in the lane
     before trusting the review.
   - The allow rule for this exact command is in `.claude/settings.local.json`.

Why the flags are what they are: see the header of `luna_review.sh`. In short,
`-s read-only` cannot run Python. `workspace-write` plus `--add-dir review-tmp`,
with a literal `--basetemp` under it, runs the tests. Probed end to end on
2026-10-03: `tests/test_rule_sync.py` gave 42 passed, and the lane was unchanged.

## Adjudicate through the retained session (WI-835, 2026-10-06)

The coordinator never starts a subagent to adjudicate. It runs the kit's entry
point FROM THE LANE WORKTREE (a primary checkout or an unclaimed worktree is
refused with exit 2), so the call goes through the loop's keep operation and
`out/adjudicator/` record, and one retained session judges the whole chain.

1. Compose the brief with `compose_lane.py` (above): `amendment` for approved
   rows whose text drifted from `docs/archive/last_approved/`, `first-approval`
   for Drafted rows. Number the verdict `NNN-ADJUDICATE-<lane sha7>.md` under
   `docs/reviews/<wi-slug>/`.
2. Confirm the dedicated home is signed in:

       .venv/Scripts/python.exe project-trajectory/scripts/coordinator_adjudicate.py signin

3. Launch it with `run_in_background: true` (a call can outlast the 10-minute tool cap):

       C:/Projects/ai-template/.venv/Scripts/python.exe -u \
         project-trajectory/scripts/coordinator_adjudicate.py adjudicate \
         --brief-file <brief.md> --brief <class> --wi WI-NNN \
         --verdict docs/reviews/<wi-slug>/NNN-ADJUDICATE-<sha7>.md

   Expect `keep: minting…` on a route's first call and `keep: resuming <id>`
   after. Exit 0 means a valid verdict, 1 a failed call or missing/invalid
   verdict, 2 a refusal before launch, and 7 a home that is not signed in
   (sign in through dev-setup; nothing falls back).
4. The adjudicator commits the verdict (trailer `WI: WI-NNN`) and its own
   re-attest or approve act. The entry point commits the telemetry log. A
   returned row's follow-up arrives as a `## Dispositions` block in the spec.
   If it is answered in-lane, replace the section under another heading, since
   intake refuses a `## Dispositions` heading with no toml block.
5. Read the store record (`C:/Projects/ai-template/out/adjudicator/*.json`)
   after each call: `state`, `pct` and `reset_reason` show whether the session
   is active, draining or retired.
