# Review handoff: revision 29, GPT-6 Astra and Claude Fable 5.1 (both medium)

A boot document for **one fresh session** whose job is one pair of independent
reviews of this plan, then judging every finding and folding in what holds.
It is not the coordinator's handoff
([`docs/handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md)).
It replaces [`review-handoff-r20.md`](review-handoff-r20.md), now historical.

**Why this round:** the last full review ran on revision 22. Since then the
owner added items 15 and 16, reshaped item 14 and the carrier design, and the
plan was consolidated (revision 28). No review has seen items 15 and 16, the
keep-or-mint rule, the adjudicator note, or the consolidated Status.

## State

- **Trunk:** `refactor_again`, nothing pushed (push is the owner's). The
  reviewed commit is trunk's tip when this session starts: record
  `git rev-parse --short=9 HEAD` as `<TIP>`.
- **The plan:** [`README.md`](README.md), revision 29. Its Status says what is
  ruled, open and proposed; the rulings section governs. The revision log and
  every earlier review's dispositions are in [`history.md`](history.md), and
  the reviews are in [`reviews/`](reviews/).
- **The brief:** [`reviews/brief-r29.md`](reviews/brief-r29.md), ready to
  render. It carries the owner's severity calibration.
- **Background for items 14–16:**
  [`../2026-10-13-contract-split-divergence.md`](../2026-10-13-contract-split-divergence.md),
  closed; its §5 records the owner's answers.

## The owner's calibration

Stated in the brief, and the bar you judge by:

- **Only valid, realistic findings are taken** (owner, 2026-10-13): "we do not
  need to over-engineer a solution here to speculative corner-cases". Astra
  tends to raise them. Split a mixed finding into the part that holds and the
  part dismissed as a corner case, and record why the remedy would over-build.
- **BLOCKER:** a ruling-dependent instruction is wrong or unsafe, an owner rule
  is broken, or a direction is wrong.
- **MAJOR:** an inconsistency, contradiction or factual error that would
  actually mislead the owner's ruling or the next session's build.
- **MINOR:** precision and wording.

Re-grade a finding when its label doesn't match these definitions, and say so.

## Procedure

1. **Isolate.** Two detached worktrees at `<TIP>` and a dated review root, all
   under this session's scratch directory. If a path exists, add `-2`; never
   reuse or delete one.

   ```bash
   S=<this session's scratch directory>
   git worktree add --detach "$S/wt-churn-r29-astra" <TIP>
   git worktree add --detach "$S/wt-churn-r29-fable" <TIP>
   mkdir -p "$S/<date>-churn-plan-r29/scratch"
   ```

2. **Render two briefs** from `reviews/brief-r29.md` into the review root,
   replacing `{TIP}`, `{WT}` (each reviewer's own worktree), `{OUT}` (each
   one's review file, `astra-medium-review.md` and `fable-medium-review.md` in
   the review root) and `{ROOT}`. Check that no `{`-placeholder is left.

3. **Run both reviewers in parallel, in the background.** Each took about ten
   minutes on revision 22.
   - **Astra through Codex**, at medium. `-o` must point at a different file
     from `{OUT}`: it writes Codex's final message, and at the same path it
     overwrites the review. On Windows add `-c 'windows.sandbox="unelevated"'`.

     ```bash
     R="$S/<date>-churn-plan-r29"; WT="$S/wt-churn-r29-astra"
     codex exec -m gpt-6-astra -c model_reasoning_effort="medium" \
       -s workspace-write --add-dir "$R" -C "$WT" --skip-git-repo-check \
       --color never -o "$R/astra-medium-final-message.md" - < "$R/brief-astra.md" \
       > "$R/astra-medium-review.md.log" 2>&1
     ```

   - **Fable as a sub-agent** (`model: fable`, `effort: medium`,
     `subagent_type: general-purpose`, in the background). Give it only this:
     read `<review root>/brief-fable.md` and carry it out exactly; write the
     review to `<review root>/fable-medium-review.md`; modify nothing in any
     repository or worktree except that file and scratch under
     `<review root>/scratch/`; read no other file in the review root; never
     read `OWNER_SCRATCHPAD.md`; return the review text.

   Afterwards check each worktree's `rev-parse HEAD` and
   `status --porcelain`; if either changed, inspect before trusting the
   review. If Codex refuses on a usage limit, stop and tell the owner; don't
   substitute a model unasked.

4. **Judge every finding.** Findings are claims: confirm or refute each
   against the repository with a command or a read, never from the review's
   say-so. Watch for a reviewer inheriting a false premise from the plan.
   Apply the calibration, merge duplicates across the two reviews, and
   separate:
   - **owner calls:** anything that needs a ruling, with a recommendation;
   - **fixes:** stale text, counts, citations, consistency, and corrections a
     confirmed finding makes plainly necessary.

5. **Fold in the fixes; bring the owner calls to the owner.** Never decide a
   ruling for the owner. Record the round as revision 30:
   - add "Review of revision 29: …" to [`history.md`](history.md)'s
     dispositions, in the shape of the earlier ones, and a one-line entry to
     its list of later revisions;
   - update the plan's Status (the last review, what is open) and anything
     the fixes touch;
   - file the reviews as `reviews/astra-medium-r29.md` and
     `reviews/fable-medium-r29.md`, each with a one-line provenance header, as
     the revision 22 pair were;
   - bring `pointer-rules.md` and the coordinator handoff's "For the owner"
     block up to date if they are affected. Republish the "Spine Pointer
     Rules" page only if the owner asks.

6. **Commit** in the repo's style after the commit bar
   (`python -m pytest -q -n auto -m smoke` and
   `python scripts/check_smoke_budget.py --mode enforce`). Don't push.

7. **Clean up.** Remove both worktrees once you've checked they're unchanged.
   Keep the review root.

## Session prompt (paste to start the session)

```text
Work in the ai-template repository on branch refactor_again. Read
docs/plans/2026-10-11-review-churn/review-handoff-r29.md and follow it: run
the revision 29 review pair (GPT-6 Astra through Codex and Claude Fable 5.1
as a sub-agent, both at medium, in parallel, each in its own read-only
worktree at trunk's tip, on reviews/brief-r29.md), judge every finding against
the repository, take only valid and realistic findings, fold the fixes in as
revision 30, and bring anything that needs a ruling to me. Never read
OWNER_SCRATCHPAD.md. Don't push.
```
