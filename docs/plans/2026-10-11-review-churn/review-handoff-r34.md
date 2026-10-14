# Review handoff: revision 34, the delta since revision 31 (GPT-6 Astra and Claude Fable 5.1, both medium)

A boot document for **one fresh session**. Its job is one pair of independent
reviews of what revisions 32–34 changed, then judging every finding and
folding in only what holds. It is not the coordinator's handoff
([`docs/handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md)).
It replaces [`review-handoff-r31.md`](review-handoff-r31.md), which ran and is
now historical.

**Why this round, and why it is narrow.** The revision 31 pair, both at high
effort, reviewed the whole plan and found no direction wrong. Every finding
was about build scope, ordering, or a claim about existing code that didn't
hold. Revisions 32–34 folded those in. The new text includes the queue's rows
P1–P8, item 16's verdict/act split in the shipped sitting briefs, item 8's
change check, and the narrowed carrier, and none of it has been checked
against the code. A whole-plan review at high effort again would mostly re-read
reviewed text, and every queued row still gets its own scope critique before
it is claimed. So this round reads only the delta, at medium effort (the
integrator's recommendation, 2026-10-14; the owner may raise it). It is meant
to be the last plan-level review: after it, the coordinator's queue starts.

## State

- **Trunk:** `refactor_again`, nothing pushed (push is the owner's). The
  reviewed commit is trunk's tip when this session starts: record
  `git rev-parse --short=9 HEAD` as `<TIP>`. The delta's base is `4a25720e2`,
  the commit the revision 31 pair reviewed.
- **The plan:** [`README.md`](README.md), revision 34. Its Status says what is
  ruled, open and proposed; the rulings section governs. The revision log and
  every earlier review's dispositions are in [`history.md`](history.md), the
  revision 31 round last.
- **The brief:** [`reviews/brief-r34.md`](reviews/brief-r34.md), ready to
  render. It asks for three checks: each new claim against the code, the
  queue's order, and consistency across the surfaces.
- **`contract_split`** means `961f9e47` (`origin/contract_split`). The local
  branch is dead; don't read or touch it.

## The caution this session owes

The owner wants holes found, not a longer list, and asked that this session
**be cautious about applying feedback before validating that it truly needs
addressing and could reasonably occur.** So:

- **Only valid, realistic findings are taken** (owner, 2026-10-13): "we do not
  need to over-engineer a solution here to speculative corner-cases".
- **A finding must survive three questions**, each answered with a command or
  a read, never from the review's say-so:
  1. **Is it true?** Confirm the claim against the repository. Watch for a
     reviewer inheriting a false premise from the plan, or misreading code.
  2. **Would it reasonably occur?** It needs a path in normal use: the lanes
     the queue schedules, the tools as they run today. A scenario that needs a
     contrived sequence, a tampered host or an improbable coincidence is
     dismissed in one recorded line.
  3. **Is the fix worth its cost?** A remedy that adds machinery, a new
     record, a new check or a new ceremony against a rare case is dismissed or
     cut down to the part that holds, with the reason recorded. Prefer a
     sentence of plan text over a mechanism, and an existing mechanism over a
     new one.
- **Split mixed findings:** take the part that holds, dismiss the rest, and say
  why the remedy would over-build.
- **Grades:** BLOCKER, building the plan as written would produce something
  wrong or unsafe, break an owner rule, or rest on a wrong direction; MAJOR, it
  would actually cost a lane rework or mislead an owner ruling; MINOR,
  precision and wording. Re-grade a finding whose label doesn't match, and say
  so.
- **Never decide a ruling for the owner.** A finding that would change a ruled
  item, or needs a design choice, goes to the owner with a recommendation.
- **A clean round is a fine outcome.** If both reviewers find nothing that
  holds, record that and stop; don't go looking for changes to make.

## Procedure

1. **Isolate.** Two detached worktrees at `<TIP>` and a dated review root, all
   under this session's scratch directory. If a path exists, add `-2`; never
   reuse or delete one.

   ```bash
   S=<this session's scratch directory>
   git worktree add --detach "$S/wt-churn-r34-astra" <TIP>
   git worktree add --detach "$S/wt-churn-r34-fable" <TIP>
   mkdir -p "$S/<date>-churn-plan-r34/scratch"
   ```

2. **Render two briefs** from `reviews/brief-r34.md` into the review root,
   replacing `{TIP}`, `{WT}` (each reviewer's own worktree), `{OUT}` (each
   one's review file, `astra-medium-review.md` and `fable-medium-review.md` in
   the review root) and `{ROOT}`. Check that no `{`-placeholder is left.

3. **Run both reviewers in parallel, in the background.** At high effort on the
   whole plan, revision 31 took about 10 minutes (Astra) and 14 (Fable); this
   round is smaller.
   - **Astra through Codex**, at medium. `-o` must point at a different file
     from `{OUT}`: it writes Codex's final message, and at the same path it
     overwrites the review. On Windows add `-c 'windows.sandbox="unelevated"'`.

     ```bash
     R="$S/<date>-churn-plan-r34"; WT="$S/wt-churn-r34-astra"
     codex exec -m gpt-6-astra -c model_reasoning_effort="medium" \
       -c 'windows.sandbox="unelevated"' \
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

4. **Judge every finding** by the three questions above. Merge duplicates
   across the two reviews, and separate:
   - **owner calls:** anything that needs a ruling or changes a ruled item,
     with a recommendation;
   - **fixes:** stale text, false claims about existing code, ordering
     corrections, and what a confirmed finding makes plainly necessary;
   - **dismissed:** with a one-line reason each (untrue, unreasonable, or
     over-built).

5. **Fold in the fixes; bring the owner calls to the owner.** Record the round
   as revision 35:
   - add "Review of revision 34: …" to [`history.md`](history.md)'s
     dispositions, in the shape of the revision 31 one, and a one-line entry
     to its list of later revisions;
   - update the plan's Status (the last review, what is open) and anything
     the fixes touch;
   - where a finding changes the coordinator handoff's queue table, change it
     there, since that table is what the next coordinator session works from;
   - file the reviews as `reviews/astra-medium-r34.md` and
     `reviews/fable-medium-r34.md`, each with a one-line provenance header, as
     the revision 31 pair were;
   - bring `pointer-rules.md`, `docs/status.md`'s resume line and the
     coordinator handoff's "For the owner" block up to date if they are
     affected. With this round done, status.md's resume line points straight
     at the coordinator handoff, with no further review pending.

6. **Commit** in the repo's style after the commit bar
   (`python -m pytest -q -n auto -m smoke`,
   `python scripts/check_smoke_budget.py --mode enforce` and
   `python project-trajectory/scripts/check_docs.py --root . --stale`). If the
   hook reports `docs/open-items.html` stale, regenerate it
   (`python project-trajectory/scripts/gen_open_items.py`) and include it.
   Python's `write_text` on Windows writes CRLF; write files with
   `newline="\n"` or as bytes. Don't push.

7. **Close out.** Remove both worktrees once you've checked they're unchanged,
   and keep the review root. Write a log fragment,
   `docs/log.d/<date>-review-churn-r34-review.md`, in the shape of
   `2026-10-14-review-churn-r31-review.md`, naming deferred open items. Then
   commit.

## Session prompt (paste to start the session)

```text
Work in the ai-template repository on branch refactor_again. Read
docs/plans/2026-10-11-review-churn/review-handoff-r34.md and follow it: run
the revision 34 review pair (GPT-6 Astra through Codex and Claude Fable 5.1
as a sub-agent, both at MEDIUM effort, in parallel, each in its own
read-only worktree at trunk's tip, on reviews/brief-r34.md), which reviews
only what revisions 32-34 changed. Judge every finding against the
repository by the handoff's three questions (is it true, would it
reasonably occur, is the fix worth its cost) before acting on any of it;
take only valid and realistic findings, fold the fixes in as revision 35,
bring anything that needs a ruling to me, and close out the session. Never
read OWNER_SCRATCHPAD.md. Don't push.
```
