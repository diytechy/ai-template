# Handoff 2026-10-04 (wave 11, coordinator): build the ruled frontier unattended

For the next session's **coordinator**. It runs **unattended**: the owner is away,
the frontier is built as far as it goes, and assumptions are recorded rather than
asked. It replaces
[handoff-2026-10-03-wave10-coordinator.md](handoff-2026-10-03-wave10-coordinator.md)
as the resume map.

- **The roles, tools and recipe** of the
  [wave-8 handoff](handoff-2026-10-03-wave8-coordinator.md) still hold, with the
  wave-10 handoff's in-lane cycle and corrections, plus the deltas below.
- **The tools** are in `C:/Projects/ai-template.wt/coordinator-tools/` (README
  there).
- **The last session's record** is
  [log.d/2026-10-04-wave10b-coordinator.md](log.d/2026-10-04-wave10b-coordinator.md).

## State at handoff (trunk `refactor_again`, clean, nothing pushed)

- **Ready frontier:**
  - **WI-790**: work items cite open items; the owner surface follows the queue;
    "Decisions to review"; the commit-time sync rule.
  - **WI-791**: OI-100. Amended needs reach the meaning-or-clarity adjudication,
    and CLARITY re-attests on a held rung.
  - **WI-788**: half 1, the design note, only.
- **Blocked:** WI-684, on OI-98 (the owner's FileBackup re-sync). WI-625 is
  deferred.
- **No pending open item** except OI-98.
- **Approval acts** run to seq 28. The full unfiltered suite last ran at `d040ad75`.
- **The pause is tracked** (`docs/work/pause`).

## Order of work

1. **WI-791** (medium): the smallest, a clean warm-up of the cycle. It touches the
   amendment walk, intake, the amendment brief and PROCESS.md §4.
2. **WI-790** (medium, large): open-item edges in `needs`, the owner surface,
   "Decisions to review", the commit-time sync rule, and amendments A1 to A9 with
   OI-102's rulings.
   - Build it after WI-791, because both touch `intake.py`. One lane at a time.
3. **WI-788 half 1**: the design note, as four chapters (B12):
   1. state, evidence and recovery;
   2. sessions, routing and accounts (with U1, the usage ledger);
   3. planning and tiering;
   4. adjudication, mint and landing authority.

   It ends with one amend/preserve/retire matrix and one dependency graph of
   successor rows. It carries OI-101's and OI-103's rulings and the
   research-to-uncover list.
   - It is docs only, so it may be drafted alongside the builds.
   - Live probes are authorized for **OpenCode only**: FreeLLMAPI as a custom
     endpoint, `--session` resume.
   - CLI resume-by-id probes for claude and codex are local and cheap; run them.
   - Then a Codex 6.1 (`gpt-6.1-sol`, high) review of the note, and fixes.
   - **Then STOP at the checkpoint (the owner's ruling in the spec).** File one
     pending open item asking the owner to approve the note and its slice plan,
     holding WI-788, and do not file successor rows.

## Roles (owner, 2026-10-04; these supersede the wave-8 and wave-10 roles)

| Work | Who | How |
|---|---|---|
| Building and planning (code, tests, the WI-788 design note) | **Claude Opus** | the `kit-builder` agent, model opus, at medium effort; it leaves changes uncommitted, and the coordinator verifies and commits |
| **Spine authoring** (drafting or amending SN, SR, LLR, TC and IF rows, and the spec text the rows carry) | **GPT Terra at medium** (`gpt-5.6-terra`, the only Terra id the codex CLI knows) | `codex exec -m gpt-5.6-terra -c model_reasoning_effort="medium" -c 'windows.sandbox="unelevated"' -s workspace-write -C <lane>`, briefed with the rows to write and the spine-authoring skill's question list |
| **Code reviews** (every lane diff; the WI-788 note review) | **Codex 6.1** (`gpt-6.1-sol`) at high effort | `codex exec -m gpt-6.1-sol -c model_reasoning_effort="high"`, read-only, or `luna_review.sh` with the model switched; it replaces Luna as the lane reviewer |
| Adjudication (judging spine text, disputes, acts) | an **independent Claude Opus** session | never the session that authored what it judges; Terra authors and Opus judges, so they are different families |

Sol 6.1 capacity: on 2026-10-03 the ChatGPT-plan Codex limit was hit after about 14
Sol sessions in 4.5 hours. Keep reviews to one per lane round, and wait out a
limit rather than drop the review.

## Deltas since the wave-10 handoff

- **The `codex` on PATH is 0.160.0.** `codex exec -m gpt-6.1-sol` and
  `-m gpt-5.6-terra` work directly; the extension-binary workaround is no longer
  needed. `luna_review.sh` hardcodes `gpt-6-luna`, so pass the model by hand or
  use `codex exec`.
- **The native `claude` is 2.1.289.** The Opus rows are pinned to
  `claude-opus-5-5`.
- **Claude Code subagents** use a 1-hour prompt cache (user setting
  `subagentPromptCacheTtl`).
- **Owner rulings to apply** (all ruled; the decision references):
  - OI-100 to OI-103;
  - the S11 plan §6, ruled as recommended;
  - WI-788's risks 1 to 9, LS8 and LS9;
  - WI-790's three passes.
- **The owner's standing rules:**
  - Fix a single point of failure; never add a fallback, degenerate or legacy path.
  - Reviews and judgements stay independent of what they judge.
  - Enforce a coupling rule at the commit that makes the change (a commit against
    its parent).
  - Findings are claims: confirm or refute them first.
  - A builder acts only on verified evidence that no user setting or OS-level retry
    mitigates. Environment-caused failures are surfaced, not tooled around.
  - The adjudicator's call on a reviewer's request is final (OI-103 Q3).
- **Recording assumptions.** Every call the session makes on the owner's behalf,
  that no ruled open item or spec settles, goes into the delegated-decisions record
  (`docs/decisions/<branch>.toml`; template `project-trajectory/decisions.template.toml`):
  - each entry carries the four fields (`decided`, `alternative`, `reversal_cost`,
    `why_not_escalated`) and `review = ""`;
  - the riskiest entries are named in `high_risk`;
  - coordinator calls made on trunk go in `docs/decisions/coordinator-<date>.toml`.

  A decision that truly only the owner can make, and that blocks a row, is filed as
  a pending open item holding that row (`wi_refs`, until WI-790 lands; after it,
  the `needs` token and a placeholder). The session then moves on to the next row.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator for an UNATTENDED session: the owner is away
and will review afterwards. Build the ruled frontier as far as it goes,
recording assumptions instead of asking.

Read first, in order:
1. CLAUDE.md;
2. docs/status.md;
3. docs/handoff-2026-10-04-wave11-coordinator.md (the resume map, the order of
   work and the deltas);
4. docs/handoff-2026-10-03-wave10-coordinator.md and
   docs/handoff-2026-10-03-wave8-coordinator.md (the roles, the tools, the
   in-lane cycle and the corrections);
5. your memory index, especially the unattended-run traps.

Authorization (the owner's, for this session only):
- Claim WI-791, WI-790 and WI-788 through `integrate.py claim`, each with a
  scoped unpause: a reviewed commit deletes docs/work/pause, then the claim,
  then a byte-identical restore of the pause in the next commit. This does not
  spend the control ruling's pause deletion.
- Live probes on OpenCode only (FreeLLMAPI as a custom endpoint; session resume).
  Local CLI resume-by-id probes for claude and codex are fine.
- Roles (the owner's, 2026-10-04):
  - building and planning: Claude Opus (the kit-builder agent, model opus,
    medium);
  - spine authoring: GPT Terra at medium (gpt-5.6-terra) through the codex CLI;
  - code reviews: Codex 6.1 (gpt-6.1-sol, high) through the codex CLI (0.160
    on PATH), for every lane diff and for the WI-788 design-note review;
  - adjudication and disputes: an independent Claude Opus session that never
    authored what it judges.

Order: WI-791, then WI-790 (one lane at a time; both touch intake.py). Then
WI-788 half 1, the design note, which may be drafted alongside the builds
because it is docs only. Follow each spec's Done-when and owner-rulings sections
exactly. Where the spec says "STOP for the owner" (WI-788's checkpoint), stop
that row: file one pending open item asking for approval, holding the row, and
do not file its successor rows.

Per work item, the cycle from the handoffs:
1. Claim, with the lane at C:/Projects/ai-template.wt/wi-NNN.
2. A kit-builder agent (model opus, medium) builds and leaves the change
   uncommitted; you verify and commit it.
3. Any spine rows the work needs are drafted or amended by Terra (medium) in
   the lane, not by the builder.
4. A Codex 6.1 (gpt-6.1-sol, high) review of the lane diff.
5. Rework, with the builder skeptical of findings: it acts only on verified
   evidence that no setting or OS retry mitigates.
6. An independent Opus adjudicator resolves builder-reviewer disputes; its call
   is final.
7. Terra's spine rows go through the in-lane adjudication cycle (wave-10
   handoff), judged by an independent Opus adjudicator.
8. Land with a squash, archive the tip to archive/lanes, run the intake sweep,
   and close the redundant re-mint rows by citing the act.

The commit bar on every commit:
`python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce`,
plus `check_trajectory --strict` and `check_docs`. Paste real output. Run the
full unfiltered suite once at the end, in the background, from a detached
worktree with a fixed --basetemp.

Decisions:
- Use the ruled open items as your decision reference: OI-100 to OI-103 and
  earlier ruled rows in docs/requirements/open-items.toml, the rulings
  fragments in docs/log.d/, the S11 plan §6 (ruled), and the owner-rulings
  sections inside each WI spec.
- Apply the owner's standing rules: no fallback, degenerate or legacy paths
  (fix the single point of failure); independent reviews; coupling rules
  enforced at the commit; findings are claims.
- When a call is not settled by a spec or a ruled item, decide it the way the
  closest ruling and recommendation point, and record it in
  docs/decisions/<branch>.toml (decided, alternative, reversal_cost,
  why_not_escalated, review = ""; the riskiest go in high_risk). Coordinator
  calls on trunk go in docs/decisions/coordinator-<date>.toml.
- Only a decision that truly only the owner can make, and that blocks a row,
  becomes a pending open item holding that row. Then continue with the next row.

Never:
- push or merge to main;
- rule an open item, or sign a held rung or any act reserved to the owner;
- leave docs/work/pause deleted;
- read OWNER_SCRATCHPAD.md;
- change ~/.claude settings or install software beyond what the handoff names;
- self-review: if Codex is rate-limited, wait for its reset (schedule a
  wakeup); if it stays unavailable past 2 hours, use a fresh independent Opus
  reviewer and record the same-family relaxation in the decisions record.

Stop when no row on the frontier can move without the owner. Then:
- update docs/status.md (forward-only);
- write the next handoff;
- add a docs/log.d fragment;
- list in the handoff every decisions-record entry the owner should review,
  high-risk first.
```
