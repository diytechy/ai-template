<!-- The brief both revision 19 reviewers receive, identical except for each one's own detached worktree at 39c1fcfd0 (<WT>) and review file (<OUT>). They run one after the other (GPT-6 Astra at high effort, then Claude Fable 5.1 at medium), and neither sees the other's review. -->

# Independent review: the whole review-churn plan, revision 19

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at `<OUT>`.

## Where things are

- **Repository (read-only):** `<WT>`, a detached worktree at commit `39c1fcfd0`. Python 3.11 with `tomllib`: `C:/Projects/ai-template/.venv/Scripts/python.exe`, or `python` on PATH. Scratch scripts may go in `C:/Projects/ai-template.wt/review-tmp/2026-10-13-churn-plan-r19/scratch/`.
- **What changed since the last review** (revision 17, reviewed at `29a613d93` by GPT-6 Astra at high effort and Claude Fable 5.1 at medium): `git -C <WT> log --oneline 29a613d93..39c1fcfd0` and `git -C <WT> diff 29a613d93..39c1fcfd0 -- docs/plans/2026-10-11-review-churn docs/handoff-2026-10-11-attended-coordinator.md`. Revision 18 dispositioned those two reviews and recorded owner decisions 1, 2 and 4; revision 19 recorded decision 3.

## What is under review: the whole plan

`docs/plans/2026-10-11-review-churn/README.md`, revision 19, all of it. Read it whole before judging any part. Its state:

- **Items 1–10 are ruled.** The "Owner rulings, 2026-10-11" section governs where older item text differs. Challenge a ruling only where the plan's later text contradicts it, applies it wrongly, or where a revision 18–19 change undermines it.
- **Item 11, variant F**, the owner's position, with these owner answers: F-call 1 (i) and **decision 1** (an IF's owner is a local component id or an `external:` party; the optional IF `component` cells that hold placement today are migrated); F-call 2 (no stub for every file; the builder mints files and must not duplicate); F-call 8 (an LLR need not name an IF; placement is derived); F-call 9 with **decision 2** (an interface states only its form, in one line that is the `data` cell until the build and the contract body's first line after; an LLR or SR states the behaviour and its full dimensional scope; every IF is pointed at by at least one LLR or SR, replacing OI-43's direct IF → TC rule). F-calls 3 (restated per TC and LLR pair) to 7 remain open.
- **Item 12** (architectural decomposition). Open, except that **decision 4** moved its architectural-delta question to the scope critique.
- **Item 13** (review only a green tip). Answered: the gate sits at the start of review; about three red rounds, then a partial close; TC rows before the build, failing test code as the build's first deliverable; a scoped test set; an advisory mutation trial. **Decision 3** (revision 19): `[policies] dependency_admission = "owner-or-delegate" | "independent"`, with the owner's definition of a delegate.
- **Decision 4:** the plan comes after the claim, in the lane; the scope critique, before the claim, asks the questions that reshape the queue.
- **Companion files, for consistency:** `pointer-rules.md`, `docs/handoff-2026-10-11-attended-coordinator.md` ("For the owner"), `item-11-llr-fitness-report.md`, `item-11-value-domain-research.md`, `review-handoff-astra-fable.md`.
- **Earlier reviews and dispositions** are in `reviews/` and the plan's last section, including `astra-high-r17.md` and `fable-medium-r17.md`. Don't repeat a dispositioned finding unless its fix is wrong or a later revision broke it.

## The owner's lens

Long-term design sustainability. Keep behavioural expectations divorced from implementation. Keep the spine's authored links few: every link must earn its upkeep by the orientation it gives a reader (human or LLM) or the check it enables. Prefer derived over authored, and one home per relation. Duplication, exact or in intent, is the curse of maintainability. Review sessions are the scarce resource; deterministic checks are cheap.

## The owner's standing rules (check the plan against them)

- **Enforce at the commit, not through history.** A coupling rule is a commit-time check of a commit against its parent, never git-history archaeology or a marker convention.
- **Fix single points of failure; never add fallback, degenerate or legacy paths.** Reviews and judgements are independent of what they judge.
- **Findings are claims:** confirm or refute before acting. Deleting something requires first reading the WI's original rationale.
- **Decisions are confirmed or overruled**, never "approved".
- **Review threat model:** a finding that needs a compromised or contrived host is dismissed. Agent-written repository content stays in scope.
- **Requirements never reference code.** No implementation carrier (code file, function, symbol) in any requirement row. Shipped boundary files may be named at LLR/TC only; SN/SR name no files. Code points up to requirements; tests may name modules.
- **One configuration file in TOML** (`docs/process.toml`); `docs/work/pause` is the only presence-file exception.
- **The kit's scripts stay stdlib-preferred and cross-platform;** a dependency enters only through a reviewed row in `docs/dependencies.md`. **Edit conservatively,** and flag anything that forces adopters to migrate.
- **The adjudicator's scope is the spine and behaviour**, not whether something may be installed.
- **A delegate** is an LLM agent the human has explicitly permitted to act in their stead; it can do everything the owner can (owner, 2026-10-13).

## What to do: two phases, in order

### Phase 1: challenge

Is each direction right? Judge, on the owner's lens: variant F as now answered (against E and anything better you can name); decision 2's split of form from behaviour; decision 3's policy and delegate definition; decision 4's division between the scope critique and the in-lane plan; item 12; item 13 as now shaped. Ground every claim in a file, a row id or a command you ran. If a direction is wrong, say so plainly and say what should replace it.

### Phase 2: stress-test the whole plan

Find where it breaks down and where contradictions surface, across all thirteen items, not only the revision 18–19 text. Check at least:

- **Decision 2 on the kit's real registries.** Apply the plan's "form is what both sides must agree on to connect; behaviour is what must be true of what flows through" test to real IF rows, including file, `stdout`, `call` and schema-pointer rows (IF-047's review verdicts, IF-011's exit code, and others you pick). Does every form fit one line of at most 160 characters, and where a form line is a schema pointer, where does the schema live, given one home per fact and ruling 5? Does "every IF is pointed at by at least one LLR or SR" hold for external crossings, declared-kernel IFs (OI-48) and `call` rows, and does replacing OI-43's direct rule lose a check that rule gave? The LLR dimensions cell against the SR `permutations` cell and ruling 1.
- **Decision 1's migration** (the component cells that hold placement, external-owned rows, the uniqueness rule) and the effective-contract reader with its transition check.
- **Decision 3.** The delegate definition against PROCESS.md §4 ("an attended session on the owner's explicit delegation"; "a mechanically triggered session … never approves on a held rung") and its enforcers (the `Loop-Session` trailer, `check.py`'s `held-status` step, the merge slot). The owner-or-delegate default, the card assembled outside the adjudicator, the decision bound to the resolved lock, the identity script as coordinator tooling, and the lane-local environment.
- **Decision 4.** Can the scope critique carry the queue-shaping questions (its rubric, anchors S1–S4)? Item 12's moved entry point, WI-805's in-lane plan and re-plan, and the "work branch never mints a WI id" rule.
- **Item 13.** The red cap as a partial close (its cost per occurrence), the red-before evidence contract (is it buildable on every supported OS and stack?), the scoped set's refusal rule, and tags moved to phase 1.
- **The rest of the plan.** Items 1–10's text against their rulings; the Sequence phases and their order now that revision 18 added builds; the session budget; the measures.
- **Internal consistency.** Do the README's summary table, item 11's status table, the F section and its table, items 12 and 13, `pointer-rules.md` and the coordinator handoff agree after revision 19? Are the counts and citations right?

Say which phase each finding comes from.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [phase 1|phase 2] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

- BLOCKER: a ruling-dependent instruction is wrong or unsafe, breaks an owner rule, or a direction is wrong.
- MAJOR: an inconsistency, contradiction or factual error that would mislead the owner's ruling or the next session.
- MINOR: precision or wording. Mark wording ambiguities `for clarity`.

Then, under **"Views for the owner"**, one short grounded paragraph each on:
- variant F as answered, and F-calls 3–7;
- decision 2;
- decisions 3 and 4;
- items 12 and 13.

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
