# Review handoff: put the review-churn plan through Codex Astra (medium), then Claude Fable 5.1 (medium)

A boot document for **one standalone session** whose only job is two
independent reviews of this plan, run in sequence, each followed by the
disposition of its findings. It is **not** the coordinator's handoff. It lives
in the plan's folder so that `coordinator-tools/overnight_legs.py` (which reads
the newest `docs/handoff-*.md`) and `docs/status.md`'s RESUME HERE never pick
it up. The coordinator's resume map remains
[`../../handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md).

## What is under review

- [`README.md`](README.md): the plan, revision 11.
  - Items 1–10 are ruled, in its "Owner rulings, 2026-10-11" section. The
    revision 6–7 clarifications not marked as rulings await the owner's
    confirm or overrule.
  - **Item 11 (what points where) is new and open:** code states its contract
    for each interface it serves, interfaces name the requirements they carry,
    and modules (files) declare their component. Its terms (contract, module)
    are the owner's. Nobody has reviewed it.
  - **Item 11 also carries two owner's queries** (revision 11), listed under
    its terms: (1) a contract is never mandated per function, and a function
    cites one only if it actually realizes that seam; (2) work items name
    the interfaces they serve, so the queue traces to the requirements
    mechanically.
- [`pointer-rules.md`](pointer-rules.md): the ruled pointer table, and the
  item 11 proposal as a second diagram.
- [`../../handoff-2026-10-11-attended-coordinator.md`](../../handoff-2026-10-11-attended-coordinator.md):
  the coordinator's boot document, which restates the rulings as working
  instructions.
- Earlier reviews and their dispositions are in [`reviews/`](reviews/):
  - Sonnet and Sol, of revision 2;
  - GPT-6 Astra (low effort), of revisions 3–5;
  - Claude Fable 5.1 (low effort), of revision 6.

  The plan's last section dispositions every finding. A review should not
  repeat them unless a fix is wrong.

## The brief (written once, adapted for stage 2)

Copy [`reviews/brief-r6.md`](reviews/brief-r6.md) into the review root as
`brief.md` and change it:

- **Scope.** Point it at the stage's worktree, the tip sha and the current
  revision. Say the earlier reviews include `fable.md`. Put the closest look
  on **item 11**, and on whatever revisions 7–10 changed: the convergence
  round's fresh-reviewer rule, tests naming their TC, the empty-pool refusal,
  and item 11's history, proposals and terms, and its two owner's queries.
- **Item 11's history.** Check its history table against the repository: the
  log.md entries, OI-14, OI-39/OI-42, OI-67, the 2026-09-20 assumption-tier
  plan, and the commits it cites.
- **Item 11 is in scope in full:** its history, terms, proposal table,
  nuances, the owner's two queries, and every one of its open calls. Each
  open call gets a grounded view the owner can rule on; leave none
  unaddressed.
- **Item 11's proposal.** Judge whether it holds together:
  - each module states the contract of every interface it serves;
  - IF → LLR/SR;
  - module → CMP;
  - the 55 LLRs in modules with no interface;
  - the interaction with item 5's removal of the LLR `module` cell and with
    SR-180.
- **The owner's two queries on item 11.** Judge each, grounded in the repo.
  - **Contracts only where served.** Confirm that nothing in the plan, the
    kit's checks or PROCESS.md would require a contract per function or per
    module. Find what today's "every shipped module carries an
    `Implements:` tag" rule becomes under item 11. Then say what, if
    anything, can mechanically refuse a contract cited by a symbol that
    doesn't realize the seam, and whether review alone is acceptable.
  - **Work items bound to served interfaces.** Read the WI schema (the
    `docs/work/` front matter, `work-items.template.csv`, PROCESS_OPTIONS.md's
    work-items layer) and the consolidation census in `check_trajectory.py`.
    Judge whether an `if_refs` cell should replace or sit beside
    `sr_refs`, how rows with no interface stand, and whether `needs`
    edges should be checked against, or derived from, the interfaces'
    provider and consumer order. Check what the requirement rows' parent
    links can and can't express today (`sn_refs`, `sr_refs`,
    `delivered_with`), and whether the queue should mirror that tree.
    PROCESS.md §5 recurses through sub-scope SRs per component ("the tier
    does not recurse, the activity does"; `DevStg-LLReqs` is terminal).
    Find how a sub-scope SR points to its parent obligation and component
    scope, or confirm that no cell does.
- **The decomposition alternatives (owner's request).** Item 11 records two
  readings: (a) SRs at every component scope decomposing to a terminal LLR,
  and (b) SRs only at the system boundary, with architecture decomposing
  them into LLRs recursively. The owner leans to (b) on churn grounds, but
  has not ruled. Give the strengths and weaknesses of each, judged on
  long-term design sustainability rather than on past rulings, with the
  concrete migration cost of (b) and its effect on physical projects.
- **Depth.** The reviewer may spawn its own sub-agents to drill into
  details (history, call sites, Gilbert), where its tooling allows. Their
  findings are folded into the one review file, and they modify nothing. Say how this sits with items 3 and 9.
- **Terminology cross-check (owner's request).** These terms were settled many
  sessions ago, and the kit must stay compatible with physical projects.
  - **Module:** item 11 says a module is one unit of realization represented
    by one file in git: a code file in software, a part's file where physical
    parts join, with "file" as a synonym. Find the earlier definitions and
    check this reading against them: the old `modules.csv` / `MOD-###`
    registry and its move to repos, PROCESS.md, PROCESS_OPTIONS.md, ADOPTING.md
    and the registry-machinery reference. Check it against Gilbert's PART and
    ASSET registries (read-only, at `C:/Projects/gilbert`, which mixes physical
    parts with software).
  - **Contract:** item 11 says a contract states the bounds of what crosses one
    interface (output range, stdout limits, CLI output pattern, refusal shape),
    not the business behaviour, which is the LLR's. Check that against PROCESS.md
    (the interface section, and "an interface says what crosses …"), and sample
    the existing `Contract IF-NNN:` bodies for ones that restate obligations
    instead.

## Stage 1: Codex Astra, medium effort

1. **Isolate.** Make a detached worktree at trunk's tip, plus a dated review
   root:
   `git worktree add --detach C:/Projects/ai-template.wt/review-churn-plan-astra-m <tip sha>`, and
   `C:/Projects/ai-template.wt/review-tmp/<date>-churn-plan-astra-m/`.
   Write the brief there.
2. **Run Astra at medium effort**, with the flags of
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
3. **Disposition**, as described below. Save the review as
   `reviews/astra-medium.md` and its brief as `reviews/brief-r10.md`. Commit,
   then remove the worktree.

## Stage 2: Claude Fable 5.1, medium effort

Run it only after stage 1 is committed, so it reviews the revised plan.

1. **Isolate** again at the new tip
   (`C:/Projects/ai-template.wt/review-churn-plan-fable-m`, and a new review
   root). Copy stage 1's brief and change it: the new sha and revision, and
   `astra-medium.md` among the earlier reviews whose findings were
   dispositioned.
2. **Spawn a sub-agent** with `model: fable` and `effort: medium`. Give it
   only this instruction: read `<review root>/brief.md` and carry it out
   exactly, write the review to `<review root>/fable-medium-review.md`,
   modify nothing in any repository or worktree, and return the review text.
   It writes nothing but its review file. It shares the plan author's model
   family but is a different model in a fresh context, as the low-effort
   Fable review was.
3. **Disposition.** Save the review as `reviews/fable-medium.md` and its brief
   as `reviews/brief-r11.md`. Commit, then remove the worktree.

## Disposition (both stages)

- **Findings are claims.** Confirm or refute each one against the repository
  before changing anything, and read a WI's original rationale before
  deleting anything.
- **Edit the plan's markdown** [`README.md`](README.md) directly, along with
  `pointer-rules.md` and the coordinator handoff, as the findings require.
- **Add a disposition table** to the plan's last section, in the shape of the
  earlier ones, titled "Review of revision N: \<model\>, medium effort".
  Advance the status line's revision number.
- **Owner decisions.** A finding that needs the owner's decision goes into
  item 11's open calls (or the relevant item's) and the coordinator handoff's
  "For the owner". Never decide it yourself.
- **Provenance and commits.** Each saved review opens with a one-line
  provenance comment, as the earlier ones do. Commit only the plan folder and
  the coordinator handoff, with the repo's commit style and attribution, and
  let the pre-commit hook run.
- **The rendered pages (optional).** The plan's page is the private artifact
  `https://claude.ai/artifact/BCXC6juE1Ab47fNrc3xJSY` and the diagram is
  `https://claude.ai/artifact/VYzwf3J1WYcFJpvZCjRdt5`. To update either, read
  it with the Artifact tool's `read` action and republish to its `url`. The
  markdown in this folder is the record; the pages are views.

## Session prompt (paste to start the review session)

```text
You are running ONE review session for the ai-template review-churn plan,
attended by the owner: two independent reviews in sequence, Codex gpt-6-astra
at medium effort, then Claude Fable 5.1 at medium effort, each followed by the
disposition of its findings. You are not the coordinator: take no lease,
claim nothing, touch no lane, and leave docs/work/pause and docs/status.md
alone.

1. Read CLAUDE.md. Then read
   docs/plans/2026-10-11-review-churn/review-handoff-astra-fable.md (this
   procedure) in full, the plan README.md's "Owner rulings" section and
   item 11, and your memory index.
2. Write the brief as the handoff says, including the terminology
   cross-check of "module" and "contract", the owner's two queries on
   item 11, and the two decomposition alternatives.
3. Stage 1: run Astra (medium) in a detached worktree in the background. When
   it finishes, confirm or refute every finding against the repository. Then
   update the plan, pointer-rules.md and the coordinator handoff, record the
   review and its disposition table, and commit.
4. Stage 2: at the new tip, run Fable 5.1 (medium) as a sub-agent
   (model: fable, effort: medium) that reads only the brief. Disposition it
   the same way, and commit.
5. Anything that needs the owner's decision: ask the owner, or record it as
   an open call. Never decide it yourself. Never push. Report each verdict,
   what changed, and the open calls.

Never: read OWNER_SCRATCHPAD.md; push or merge; bypass a commit hook; let a
reviewer sub-agent see anything but its brief.
```

## Headless session prompt (scheduled, unattended)

For a run started by Task Scheduler through
`C:/Projects/ai-template.wt/coordinator-tools/scheduled_review.py`, which
reads the fenced block below. A `claude -p` session exits when its turn ends
and kills its background tasks, and nobody is there to answer. So everything
runs in the foreground, and owner questions become open calls.

```text
You are running ONE UNATTENDED review session for the ai-template
review-churn plan (headless; the owner is asleep and cannot answer): two
independent reviews in sequence, Codex gpt-6-astra at medium effort, then
Claude Fable 5.1 at medium effort, each followed by the disposition of its
findings. You are not the coordinator: take no lease, claim nothing, touch no
lane, and leave docs/work/pause and docs/status.md alone.

HEADLESS RULES: this session ends when your turn ends and kills anything in
the background. Never use run_in_background, Monitor or notifications. Run
the Codex command in the FOREGROUND with the Bash tool's timeout at 10800000
ms (3 hours). Spawn the Fable reviewer with run_in_background: false. Never ask a
question: record anything needing the owner as an open call. These rules
OVERRIDE the procedure wherever it says to run in the background, wait for a
notification or ask the owner. Skip the optional rendered-page update
entirely: publish or republish no artifact.

FAILURE RULES: on any failure, clean up, write the summary (step 6), and
stop; never improvise around a failure.
- A worktree path that already exists: use the same path with a -2 suffix
  (then -3), never reuse or delete an existing one. Remove every worktree
  you created on every exit path, success or failure.
- Codex exits non-zero, hits the 3-hour timeout, reports a usage limit, or
  leaves its review file missing or empty: the stage failed.
- The Fable sub-agent errors or returns no review file: the stage failed.
- A commit hook refuses: fix the cause only if it lies in the files you
  edited, and commit again. Never bypass a hook. If you cannot fix it, leave
  the change uncommitted, name it in the summary, and stop.

1. Read CLAUDE.md. Then read
   docs/plans/2026-10-11-review-churn/review-handoff-astra-fable.md (this
   procedure) in full, the plan README.md's "Owner rulings" section and
   item 11, and your memory index.
2. Write the brief as the handoff says, including the terminology
   cross-check of "module" and "contract", the owner's two queries on
   item 11, and the two decomposition alternatives.
3. Stage 1: run Astra (medium) in a detached worktree, in the foreground. If
   Codex refuses on a usage limit, stop. Write the reason to the summary file
   (step 6), remove the worktree and commit nothing. Otherwise confirm or
   refute every finding against the repository. Then update the plan,
   pointer-rules.md and the coordinator handoff, record the review and its
   disposition table, and commit.
4. Stage 2: at the new tip, run Fable 5.1 (medium) as a sub-agent
   (model: fable, effort: medium, foreground) that reads only the brief.
   Disposition it the same way, and commit.
5. Never decide an owner call yourself; record it as an open call and in the
   coordinator handoff's "For the owner". Never push.
6. Finally write C:/Projects/ai-template.wt/review-tmp/<date>-churn-plan-summary.md:
   each verdict, what changed (commit ids), the open calls, and anything that
   failed. Your last message repeats it.

Never: read OWNER_SCRATCHPAD.md; push or merge; bypass a commit hook; let a
reviewer sub-agent see anything but its brief.
```
