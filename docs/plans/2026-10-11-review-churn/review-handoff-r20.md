# Review handoff: revision 20, GPT-6 Astra (high), then Claude Fable 5.1 (medium)

> **Historical (2026-10-13): this round never ran.** The owner ran a review of
> revision 22 instead (GPT-6 Astra and Claude Fable 5.1, both at medium), on
> [`reviews/brief-r22.md`](reviews/brief-r22.md); its dispositions are the
> plan's "Review of revision 22" section.

A boot document for **one fresh session** whose job is one more pair of
independent reviews of this plan, then judging every finding and reporting
to the owner. It is not the coordinator's handoff
([`docs/handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md)).
It replaces [`review-handoff-astra-fable.md`](review-handoff-astra-fable.md),
now historical.

**The owner's hope for this round:** the BLOCKERs empty, and the MAJORs too,
where they are validly labelled MAJOR.

## State

- **Trunk:** `refactor_again`, nothing pushed (push is the owner's). The
  reviewed commit is trunk's tip when this session starts: record
  `git rev-parse --short HEAD` as `<TIP>`.
- **The plan:** [`README.md`](README.md), revision 20. Items 1–10 are ruled.
  Item 11's variant F, item 12 and item 13 carry the owner's answers from
  2026-10-13 (decisions 1–4 and the revision 20 answers); its status paragraph
  says which. Earlier rounds and their dispositions are the plan's last
  sections, and the reviews are in [`reviews/`](reviews/).
- **The brief:** [`reviews/brief-r20.md`](reviews/brief-r20.md), ready to
  render. It carries the owner's severity calibration (below).
- **The readable view:** the published "Spine Pointer Rules" page and its
  source, [`pointer-rules.md`](pointer-rules.md). Reviewers read the file.

## The owner's severity calibration

Stated in the brief, and the bar you judge by:

- **Contrived or improbable scenarios are not designed against.** A finding
  that depends on one is dismissed, whoever raised it. Astra tends to raise
  them; judge by plausibility and impact, not ingenuity.
- **BLOCKER:** a ruling-dependent instruction is wrong or unsafe, an owner
  rule is broken, or a direction is wrong.
- **MAJOR:** an inconsistency, contradiction or factual error that would
  actually mislead the owner's ruling or the next session's build.
- **MINOR:** precision and wording.

Re-grade a finding when its label doesn't match these definitions, and say
so in the report.

## Procedure

1. **Isolate.** Two detached worktrees at `<TIP>` and a dated review root.
   If a path exists, add `-2`, then `-3`; never reuse or delete one.

   ```bash
   git worktree add --detach C:/Projects/ai-template.wt/churn-r20-astra-h <TIP>
   git worktree add --detach C:/Projects/ai-template.wt/churn-r20-fable-m <TIP>
   mkdir -p C:/Projects/ai-template.wt/review-tmp/<date>-churn-plan-r20/scratch
   ```

2. **Render two briefs** from `reviews/brief-r20.md` into the review root,
   replacing `{TIP}`, `{WT}` (each reviewer's own worktree) and `{OUT}` (each
   one's review file, `astra-high-review.md` and `fable-medium-review.md` in
   the review root). Check that no `{`-placeholder is left.

3. **Run Astra at high effort, in the background,** and wait for the
   notification. **`-o` points at a different file from `{OUT}`**: it writes
   Codex's final message, and at the same path it overwrites the review (the
   revision 17 trap).

   ```bash
   R=C:/Projects/ai-template.wt/review-tmp/<date>-churn-plan-r20
   WT=C:/Projects/ai-template.wt/churn-r20-astra-h
   codex exec -m gpt-6-astra -c model_reasoning_effort="high" \
     -c 'windows.sandbox="unelevated"' -s workspace-write \
     --add-dir C:/Projects/ai-template.wt/review-tmp \
     -C "$WT" --skip-git-repo-check \
     -o "$R/astra-high-final-message.md" - < "$R/brief-astra.md" \
     > "$R/astra-high-review.md.log" 2>&1
   ```

   This machine's Codex (0.162.1) knows `gpt-6-astra`. A high run took about
   ten minutes on revision 19; Fable at medium took about ten more. Afterwards check `git -C "$WT" rev-parse HEAD`
   and `git -C "$WT" status --porcelain`; if either changed, inspect before
   trusting the review. If Codex refuses on a usage limit, stop and tell the
   owner; don't substitute a model unasked.

4. **Then run Fable at medium effort,** as a sub-agent (`model: fable`,
   `effort: medium`, `subagent_type: general-purpose`, in the background).
   Give it only this: read `<review root>/brief-fable.md` and carry it out
   exactly; write the review to `<review root>/fable-medium-review.md`; modify
   nothing in any repository or worktree except that file and scratch under
   `<review root>/scratch/`; read no other file in the review root; never read
   `OWNER_SCRATCHPAD.md`; return the review text. It reviews the same `<TIP>`
   and never sees Astra's review.

5. **Judge every finding.** Findings are claims: confirm or refute each
   against the repository with a command or a read, never from the review's
   say-so. Watch for a reviewer inheriting a false premise from the plan (in
   revision 19, Fable repeated the plan's wrong "12 kitlib kernel IFs").
   Dismiss contrived scenarios. Re-grade labels per the calibration. Merge
   duplicates across the two reviews. Separate:
   - **owner calls:** anything that needs a ruling, with a recommendation;
   - **mechanical fixes:** stale text, counts, citations, consistency.

6. **Report to the owner, and don't revise the plan until they have seen it.**
   Give both verdicts and counts; how many findings held, were refuted or were
   re-graded, and why; the owner calls with recommendations; the mechanical
   fixes in one list; anything new you found while checking.

7. **Clean up.** Remove both worktrees once you've checked they're unchanged.
   Keep the review root.

8. **After the owner answers:** fold the answers and the fixes into revision
   21, add a disposition section ("Review of revision 20: …") in the shape of
   the earlier ones, file the reviews as `reviews/astra-high-r20.md` and
   `reviews/fable-medium-r20.md` with the brief as `reviews/brief-r20.md`
   (already filed), bring `pointer-rules.md` and the coordinator handoff's
   "For the owner" block up to date, and commit in the repo's style. Republish
   the "Spine Pointer Rules" page only if the owner asks.

## Session prompt (paste to start the session)

```text
Work in C:/Projects/ai-template on branch refactor_again. Read
docs/plans/2026-10-11-review-churn/review-handoff-r20.md and follow it: run
the revision 20 review pair (GPT-6 Astra at high effort through Codex, then
Claude Fable 5.1 at medium as a sub-agent, each in its own read-only worktree
at trunk's tip, on reviews/brief-r20.md), judge every finding against the
repository using the owner's severity calibration in the handoff, and report
to me before changing the plan. Never read OWNER_SCRATCHPAD.md. Don't push.
```
