# Coordinator tools (this repository's own tooling, not shipped)

Built from wave 8 (2026-10-03) in an untracked folder beside the checkout and
moved into the repository on 2026-10-14. They derive the checkout, its sibling
`<checkout>.wt` folder (lanes, `review-tmp`, `overnight-logs`) and the venv
Python from their own location (`layout.py`), so no tool names a
machine or a user. The coordinator recipes set `TOOLS` and `PY` the same way.

Run from the repo root with the repo venv.

- `compose_lane.py WI-NNN <brief> "<ID;ID;...>" "<SR;SR>" <verdict-path> <out.md>`,
  run from the lane root: composes an in-lane adjudication brief through the
  kit's `adjudicate_brief.compose`. Verdict paths are repo-relative, e.g.
  `docs/reviews/wi-NNN-<slug>/001-ADJUDICATE-<sha7>.md`.
- `toml_merge3.py <branch> <registry paths...> [--out-dir DIR]`: a table-wise
  three-way merge of `[kind.ID]` registry blocks, from the merge base. Run it
  after `git merge --squash <branch>` hits conflicts in a registry. It refuses
  on a true per-table conflict.

## A Codex call through the session service (WI-960)

`codex_call.py` runs every Sol and Terra call (the coordinator recipes, §1,
"A Codex call"). It replaced the shell launchers, so the call is recorded
through the kit's session service like the adjudicator's.

    "$PY" "$TOOLS/codex_call.py" <role> --root <dir> --prompt-file <prompt> --out <out> \
      [--effort medium] [--wi WI-NNN] [--resume] [--route <entry>] [--timeout 7200]

- The role is `REVIEW-A` or `CRITIQUE` (Sol, the enabled `OPENAI-SOL` row) or
  `AUTHOR` (Terra, the enabled `OPENAI-TERRA` row, naming its `--wi`).
  `--route` names another enabled entry (the recipes' Luna substitution, §7).
- The launch template is the script's own: `codex exec` under the
  workspace-write sandbox, unelevated on Windows, with the primary checkout's
  `<checkout>.wt/review-tmp` its one extra writable root, so a reviewer can
  run pytest with a literal `--basetemp` there. The prompt goes on stdin; the
  final text goes to `--out`.
- `--resume` (an `AUTHOR` turn only) continues the thread of the lane's newest
  Terra log committed at HEAD, and refuses before launch when that log is
  missing, damaged, foreign, or older than an uncommitted one.
- The change check reads `--root`'s HEAD and uncommitted paths before and
  after the call. Another call's commit that only adds standard-call session
  logs is not an edit.
- The log commits in a claimed lane. Outside one (the primary checkout, a
  detached checkout, an unclaimed branch) it spools under the primary
  checkout's `out/sessions/spool/` and nothing is committed.

Exit codes: 0 a call recorded with no edit; 1 a failed call; 2 refused before
launch (an argument, the route, the prompt, the blackout window, commit hooks
off, the resume carrier); 3 an edit, its paths printed; 4 a log left
uncommitted or a spool that could not be written, the log named; 5 a change
check that could not run. After launch the precedence is 5, 3, 4, 1, 0.
`mkprompt.py` still fills the Terra spine-author brief,
`terra-spine-prompt.template.md`: an unfilled slot is refused, and
`@LANE_SLUG@`, `@WTROOT@` and `@PY@` are derived. Review briefs are rendered
with the kit's `review_brief.py review` (the recipes give the command).

## Adjudicate through the retained session (WI-835, 2026-10-06)

The coordinator never starts a subagent to adjudicate. It runs the kit's entry
point FROM THE LANE WORKTREE (a primary checkout or an unclaimed worktree is
refused with exit 2), so the call goes through the loop's keep operation and
`out/adjudicator/` record, and one retained session judges the whole chain.

1. Compose the brief with `compose_lane.py` (above): `amendment` for approved
   rows whose text drifted from `docs/archive/last_approved/`, `first-approval`
   for Drafted rows. Number the verdict `NNN-ADJUDICATE-<lane sha7>.md` under
   `docs/reviews/<wi-slug>/`.
2. Confirm the adjudicator's declared account is signed in: the command
   prints `signin [ADJUDICATOR] token: <status>`, and only `signed-in` is
   ready:

       .venv/Scripts/python.exe project-trajectory/scripts/coordinator_adjudicate.py signin

3. Launch it with `run_in_background: true` (a call can outlast the 10-minute tool cap):

       "$PY" -u project-trajectory/scripts/coordinator_adjudicate.py adjudicate \
         --brief-file <brief.md> --brief <class> --wi WI-NNN \
         --verdict docs/reviews/<wi-slug>/NNN-ADJUDICATE-<sha7>.md

   Expect `keep: minting…` on a route's first call and `keep: resuming <id>`
   after. Exit 0 means a valid verdict, 1 a failed call or missing/invalid
   verdict, 2 a refusal before launch, and 7 an ADJUDICATOR account that is
   not signed in (set its token up through dev-setup; nothing falls back).
4. The adjudicator commits the verdict (trailer `WI: WI-NNN`) and its own
   re-attest or approve act. The entry point commits the telemetry log. A
   returned row's follow-up arrives as a `## Dispositions` block in the spec.
   If it is answered in-lane, replace the section under another heading, since
   intake refuses a `## Dispositions` heading with no toml block.
5. Read the store record (`out/adjudicator/*.json` in the primary checkout)
   after each call: `state`, `pct` and `reset_reason` show whether the session
   is active, draining or retired.
