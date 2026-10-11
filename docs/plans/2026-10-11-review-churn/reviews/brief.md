# Independent review: the review-churn plan

You are an INDEPENDENT reviewer from a different model than the plan's author. You did not write this plan. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository. Never read `OWNER_SCRATCHPAD.md`. Write your review where the launch instructions say. If you have no file to write to, return it as your final message.

## What is under review

`docs/plans/2026-10-11-review-churn/README.md` in the repository at `C:/Projects/ai-template.wt/review-churn-plan`, a detached worktree at commit 85a37767a. Read it in full.

The plan explains why this repo's coordinator legs take 4–6+ hours each while the work-item queue does not shrink. It proposes nine changes for the owner to confirm or overrule:
1. closed coverage;
2. record-at-event, with a WI-902 reshape;
3. a size basis for splits;
4. full-lane review rounds;
5. requirements never reference code (the owner already ruled the core rule; the mechanics are proposals);
6. lint before review;
7. a third-family second reviewer;
8. usage recording for every model call;
9. a reviewed plan before the build.

It also answers two owner questions: how narrow and full reviews differ, and whether splitting work items pays.

## Evidence you can check

- `docs/reviews/<wi>/`: review rounds (`NNN-REVIEW-A-<sha>[-narrow].md`), dispute files and adjudications. Lanes still in flight hold theirs under `C:/Projects/ai-template.wt/wi-902/docs/reviews/wi-902/` and `C:/Projects/ai-template.wt/wi-798/docs/reviews/wi-798/`.
- `docs/log.d/`, `docs/handoff-*.md`, `docs/decisions/`, `docs/work/`.
- `.claude/skills/coordinator-cycle/` (SKILL.md and references/recipes.md).
- `project-trajectory/` (PROCESS.md, PROCESS_OPTIONS.md, `scripts/`, `prompts/`, `hooks/pre-commit`), `docs/process.toml`, `docs/rubrics/`.
- The size-versus-rounds data behind the plan's splitting answer: `C:/Projects/ai-template.wt/review-tmp/2026-10-11-churn-plan/rows.json`, with the scripts that produced it (`wi_stats.py`, `analyze.py`) beside it.
- The plan's usage figures for leg 3 come from Claude Code transcripts at `C:/Users/Peter/.claude/projects/c--Projects-ai-template/4a3bd3cb-802b-4914-bf20-2ea3b5f2ad23.jsonl` and its `subagents/` folder. Those may lie outside what you can read; if so, say the figure is unchecked.

## Owner rules the plan must respect

The plan claims to respect these. Check whether it actually does.

- **Enforce at the commit, not through history.** A coupling rule is a commit-time check of a commit against its parent, never git-history archaeology or a marker convention.
- **Fix single points of failure; never add fallback, degenerate or legacy paths.** Reviews and judgements are always independent of what they judge.
- **Findings are claims:** confirm or refute before acting. Deleting something requires first reading the WI's original rationale. Costly rework is preferred to moth-balling.
- **Decisions are confirmed or overruled**, never "approved".
- **Scope is settled where a row is born**, by a scope critique, and there is **no lane-size tripwire** (owner ruling 2 of 2026-10-07).
- **Review threat model:** a finding that needs a compromised or contrived host is dismissed.
- **Requirement rows (SN/SR/LLR) never reference code** (owner, 2026-10-11). Code points up through `Implements:` tags; tests may name modules.
- **The kit's own scripts stay stdlib-only and cross-platform. Edit conservatively,** and flag anything that forces downstream adopters to migrate.

## What to do

1. **Verify the factual claims.** Check every number, count, file:line citation and statement about how the code or process behaves against the repository. Examples: round counts per WI; "18 of 43 late findings"; "the last 40 session logs are all ADJUDICATE"; "dispatch.py never picks dual rows up"; "the narrow brief fills `{trunk}` with the round's base"; the hook's `|| true`; the bucket medians. Report each claim that is wrong, unsupported or overstated, with the evidence you found. Sample where the space is large, and say what you sampled.
2. **Judge each proposal.** Would it actually reduce review churn or leg time? Does it conflict with an owner rule above, or with the kit's principles in `CLAUDE.md`? Is there a simpler change that does the same job? Does it create a new churn source, a second path or a fallback?
3. **Check the two answers.** Is the narrow-versus-full analysis right? Does the splitting conclusion follow from the data, given its confounders?
4. **Look for what is missing:** a churn cause the plan doesn't name, an interaction between items, or an ordering problem in the sequence.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] <plan section or file:line> -> what is wrong (claim checked / evidence found) -> the concrete change to the plan

- BLOCKER: a claim the plan's argument rests on is false, or a proposal breaks an owner rule.
- MAJOR: a proposal wouldn't work as described, or a significant claim is unsupported.
- MINOR: precision or wording.

Mark a finding `for clarity` when it is a wording ambiguity, not an error.

After the findings, write a short paragraph naming which claims you verified and found correct, so the owner knows what was checked and what wasn't.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
