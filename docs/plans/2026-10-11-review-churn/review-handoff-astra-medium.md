# Review handoff: put the review-churn plan through a Codex Astra (medium) review

A boot document for **one standalone session** whose only job is an
independent review of this plan, followed by the disposition of the findings
the owner asked for. It is **not** the coordinator's handoff. It lives in the
plan's folder so that `coordinator-tools/overnight_legs.py` (which reads the
newest `docs/handoff-*.md`) and `docs/status.md`'s RESUME HERE never pick it
up. The coordinator's resume map remains
[`../../handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md).

## What is under review

- [`README.md`](README.md): the plan, revision 9.
  - Items 1–10 are ruled, in its "Owner rulings, 2026-10-11" section. The
    revision 6–7 clarifications not marked as rulings await the owner's
    confirm or overrule.
  - **Item 11 (what points where) is new and open:** code cites only
    interfaces, interfaces name the requirements they carry, and files
    declare their component. Nobody has reviewed it.
- [`pointer-rules.md`](pointer-rules.md): the ruled pointer table, and the
  item 11 proposal as a second diagram.
- [`../../handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md):
  the coordinator's boot document, which restates the rulings as working
  instructions.
- Earlier reviews and their dispositions are in [`reviews/`](reviews/):
  - Sonnet and Sol, of revision 2;
  - GPT-6 Astra (low effort), of revisions 3–5;
  - Claude Fable 5.1 (low effort), of revision 6.

  The plan's last section dispositions every finding. The review should not
  repeat them unless a fix is wrong.

## How to run it

1. **Isolate.** Make a detached worktree at trunk's tip, and a dated review
   root:
   `git worktree add --detach C:/Projects/ai-template.wt/review-churn-plan-astra-m <tip sha>`, plus
   `C:/Projects/ai-template.wt/review-tmp/<date>-churn-plan-astra-m/`.
2. **Brief.** Copy [`reviews/brief-r6.md`](reviews/brief-r6.md) into the
   review root as `brief.md`, then change it:
   - point it at the new worktree, the tip sha and revision 9;
   - say the earlier reviews include `fable.md`, and that the closest look goes
     to **item 11** and to anything revisions 7–9 changed (the convergence
     round's fresh-reviewer rule, tests naming their TC, the empty-pool
     refusal, item 11's history and proposals);
   - add to "What to do": check item 11's history table against the
     repository (log.md entries, OI-14, OI-39/OI-42, OI-67, the 2026-09-20
     assumption-tier plan, the commits it cites). Then judge whether its
     proposal holds together:
     - code → IF only;
     - IF → LLR/SR;
     - file → CMP;
     - the 55 LLRs in modules with no interface;
     - the interaction with item 5's removal of the LLR `module` cell and with
       SR-180.
3. **Run Astra at medium effort**, with the same flags as
   `coordinator-tools/sol_review.sh` and the model swapped. Record the
   worktree's `git rev-parse HEAD` and `git status --porcelain` before and
   after; if either changed, inspect the change before trusting the review.

   ```text
   codex exec -m gpt-6-astra -c model_reasoning_effort="medium" \
     -c 'windows.sandbox="unelevated"' -s workspace-write \
     --add-dir C:/Projects/ai-template.wt/review-tmp \
     -C C:/Projects/ai-template.wt/review-churn-plan-astra-m --skip-git-repo-check \
     -o <review root>/astra-medium-review.md - < <review root>/brief.md \
     > <review root>/astra-medium-review.md.log 2>&1
   ```

   This machine's Codex knows `gpt-6-astra`; `gpt-6.1-astra` is refused for
   this account. A medium run can take tens of minutes: run it in the
   background and wait for the notification.
4. **Disposition.** Findings are claims: confirm or refute each against the
   repository before changing anything, and read a WI's original rationale
   before deleting anything.
   - Edit the plan's markdown [`README.md`](README.md) directly, along with
     `pointer-rules.md` and the coordinator handoff, as the findings require.
   - Add a "Review of revision 9: GPT-6 Astra, medium effort" disposition
     table to the plan's last section, in the shape of the earlier ones.
   - Mark the plan's status line as the next revision.
   - A finding that needs an owner decision goes into the plan's open calls
     and the coordinator handoff's "For the owner". Never decide it yourself.
5. **Record and commit.** Save the review verbatim as
   `reviews/astra-medium.md`, with a one-line provenance comment as the
   earlier ones have, and its brief as `reviews/brief-r9.md`. Commit only the
   plan folder and the coordinator handoff, with the repo's commit style and
   attribution, and let the pre-commit hook run. Remove the worktree.
6. **The rendered page (optional).** The plan's page is the private artifact
   `https://claude.ai/artifact/BCXC6juE1Ab47fNrc3xJSY` and the diagram is
   `https://claude.ai/artifact/VYzwf3J1WYcFJpvZCjRdt5`. To update either,
   read it with the Artifact tool's `read` action and republish to its `url`.
   The markdown in this folder is the record; the pages are views.

## Session prompt (paste to start the review session)

```text
You are running ONE independent-review session for the ai-template
review-churn plan, attended by the owner. You are not the coordinator: take
no lease, claim nothing, touch no lane, leave docs/work/pause and
docs/status.md alone.

1. Read CLAUDE.md, then docs/plans/2026-10-11-review-churn/review-handoff-astra-medium.md
   (this procedure) in full, then the plan's README.md "Owner rulings" section
   and item 11, and your memory index.
2. Follow the handoff's "How to run it" steps 1-5 exactly: isolate in a
   detached worktree, adapt the brief, run Codex gpt-6-astra at medium effort
   in the background, then confirm or refute every finding against the
   repository before changing the plan, pointer-rules.md or the coordinator
   handoff.
3. Anything that needs the owner's decision: ask the owner, or record it as
   an open call. Never decide it yourself.
4. Commit only the plan folder and the coordinator handoff; never push.
   Report the verdict, what changed, and the open calls.

Never: read OWNER_SCRATCHPAD.md; push or merge; bypass a commit hook; review
or disposition through a sub-agent that also wrote the plan.
```
