# Handoff 2026-10-03 (wave 7, coordinator) — Sol 6.1 builds, Sonnet 5.5 reviews; TC-055 passes

For the next session's **coordinator**: an Opus session that coordinates Codex Sol
builders, Sonnet reviewers and independent Opus adjudicators and judges, and lands
work on trunk. It replaces
[handoff-2026-09-29-wave6-coordinator.md](handoff-2026-09-29-wave6-coordinator.md)
as the resume map; that handoff's roles and hand-integration recipe still hold, with
the corrections below. This wave's record:
[log.d/2026-10-02-wave7-coordinator.md](log.d/2026-10-02-wave7-coordinator.md) (every
landing, review round and bar) and [reviews/2026-10-02-wave7/](reviews/2026-10-02-wave7/).

## State at handoff (trunk `refactor_again`, 46ececa8 plus this commit)

- **Open:** WI-747 (in flight, below), WI-667, WI-697, WI-541, WI-688, WI-684 (queued);
  WI-625 (deferred). WI-684 and WI-688 are **blocked mechanically** by pending OI-98
  and OI-99 (WI-746's gate: a pending open item's `wi_refs` holds the row).
- **Approval acts** run to seq 21 (`docs/archive/last_approved/acts.toml`).
- **TC-055 RECORDED pass** (WI-765), after two fails this wave; T8's box clearance
  and lane separation are now tests (TC-125, TC-305).
- **The complexity ratchet is green and now enforced by the pre-commit hook**
  (WI-657: complexity, dupes-census, readability run on every commit, ~4 s).
- Nothing pushed. Lane tips are in `archive/lanes` (re-created this wave; earlier
  tips were lost before it started).

## Resume first: WI-747 is mid-fix-round

`build/wi-747` (worktree `C:/Projects/ai-template.wt/wi-747`, tip dfe92989) was
reviewed NOT YET SOUND (scratchpad copy of the review is lost with the session; its
substance): the `stage-gate` re-judge trigger had no production caller (intake's CLI
accepts only `release`, `intake.py:3193`) while amended SR-215 claims it fires. A Sol
fix round was running at handoff to (1) add `stage-gate` as an intake rejudge CLI
checkpoint with a test and name the command in SR-215/LLR-293/PROCESS.md, (2) extract
`rejudge.checkpoint_for(case)` so `adjudicate_brief.rejudge_values` drops under the
complexity threshold, (3) re-check two flaky `tests/test_rejudge.py` cases.

1. `git -C C:/Projects/ai-template.wt/wi-747 status --short`: if the fix round left
   changes, verify them (the lane's uncommitted diff against dfe92989), commit on the
   lane, and send a Sonnet confirmation review; if it left nothing, re-run the round.
2. Land it: the lane predates WI-657, WI-758 and others, so expect conflicts in
   generated files, `docs/id-watermark`, the registries (append-only: keep both
   sides) and `RESYNC_PACK.md`; run `check_complexity --mode enforce` on the merged
   tree and stamp or reduce before committing (the hook refuses otherwise).
3. Its merge mints adjudications (SR-215/LLR-254 amendments; LLR-293/294, TC-306/307
   first approvals): one Opus sitting over both briefs, Sonnet cross-review.

## Then, in order

- **WI-667** (narrowed by the owner's signed ruling: assumption-only cases rendered in
  both briefs; the release-checklist assumptions section). Touches
  `adjudicate_brief.py`, so after WI-747.
- **WI-697** (TC-279's first judgement, against WI-747's new rubric).
- **WI-688** second to last (held by OI-99; the owner releases it by ruling OI-99). Its
  judge sitting is WI-541's multi-step occupancy run; WI-541 closes with it.
- **WI-625** (deferred) last.

## For the owner

- **OI-98 / WI-684:** the FileBackup re-sync (yours, from 2026-10-03). Rule OI-98 when
  done to release the row.
- **SR-006:** batch M's reviewer recommends a one-clause amendment (a step may also
  declare changed-path triggers selecting it below its rung); LLR-291 hangs on it.
  Requirement text is yours to approve.
- **Disk:** C: holds ~1.8 GB free, consumed by something outside these sessions. The
  full unfiltered suite has NOT run this wave (it died of a full disk); a phase-close
  green needs space freed first. Known slow-tier reds found and fixed this wave:
  WI-746's scaffold hook regression (WI-759), WI-722's `test_traj_graph` pin (WI-750).
- **Carried, unchanged:** the four need re-attestations (SN-003, SN-008, SN-009,
  SN-025), the pause, S11, merge-to-main and push, the `Bash(codex exec *)` allow rule
  (remove when the queue drains).
- **Noted, not filed:** the rubric's T8 still names the Knowledge graph (no lane test
  covers it; this repo emits no Knowledge tab); WI-657's test lacks comma-separated and
  wrong-case pattern cases; the legacy open-item reader in `needs` (TC-253) could be
  retired by an adjudicated amendment of TC-253, IF-176, LLR-058.

## Corrections to the recipe (learned this wave)

- **Sol 6.1 needs a new codex CLI.** The npm codex (0.157.1) and the desktop app's
  (0.155) are refused for `gpt-6.1-sol` ("not supported with a ChatGPT account").
  Launch the VS Code extension's bundled CLI by full path:
  `~/.vscode/extensions/openai.chatgpt-<newest>/bin/windows-x86_64/codex.exe exec -m gpt-6.1-sol -c model_reasoning_effort="medium" -c 'windows.sandbox="unelevated"' -s workspace-write -C <worktree> --add-dir C:/Projects/ai-template/.git --skip-git-repo-check -o <out> - < <prompt>`.
- **Sandbox `unelevated`, not `elevated`:** the elevated sandbox cannot read the
  user's Python install. Builders still cannot commit; the coordinator commits.
  Git Bash fails inside the sandbox, so the coordinator runs the hook test modules.
- **Usage limit:** the ChatGPT-plan Codex limit hit after ~14 Sol sessions in ~4.5 h;
  fill a Sol outage with Opus/Sonnet work.
- **Disk:** use ONE fixed `--basetemp "$TEMP/<lane>"` per lane (pytest wipes it per
  run); a new path per run filled the drive once (148 dirs).
- **Builders run the whole smoke tier at `-n 2`** before finishing; module-only runs
  missed smoke-only failures (WI-746). Smoke seconds beside other builders are
  contention.
- **Lanes regenerate generated files before committing** (the freshness steps do not
  skip an unclaimed lane). The commit message goes in a file: `git commit -F <file>`
  (`-F /dev/stdin` fails on Windows git).
- **Landing:** grep `status.md`'s hand-written prose for the landing WI id first (the
  forward-only check fails on a done id); run every `tests/test_traj_*.py` for a lane
  touching `rendering/`; never commit past a red smoke line, re-run first.
- **Parallel adjudications take the same act seq.** Land one, then retake the other's
  snapshot on the merged tree (`refresh_refusal` empty for the same arguments, reset
  `docs/archive/last_approved/` to trunk, re-run the exact command). An amendment act
  on a registry must land before a first-approval snapshot of the same registry.
- **TC-055 judging:** render with `scripts/dashboard-shots/shoot.mjs`, cut tiles of at
  most 1500 px with Playwright clips (no image library installed), and run three Opus
  judges, one per width, told that an anchor with only MINOR findings passes.
