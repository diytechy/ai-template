<!-- The brief both revision 15 reviewers received, identical except that {WT} was each one's own detached worktree at 7bfe0c06b. They ran in parallel, neither seeing the other. -->

# Independent review: the review-churn plan, revision 15 (variant F, items 12 and 13)

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at the path the launch instructions give.

## Where things are

- **Repository (read-only):** `{WT}`, a detached worktree at commit `7bfe0c06b`. Python 3.11 with `tomllib`: `{WT}/.venv/Scripts/python.exe`, or `python` on PATH. Scratch scripts may go in `C:/Projects/ai-template.wt/review-tmp/2026-10-13-churn-plan-r15/`.
- **What changed since the last full-plan review** (revision 12, reviewed by Claude Fable 5.1 at `32868aa01`): `git -C {WT} log --oneline 32868aa01..7bfe0c06b` and `git -C {WT} diff eae8e1cbe..7bfe0c06b -- docs/plans/2026-10-11-review-churn docs/handoff-2026-10-11-attended-coordinator.md`. Revision 13's dispositions predate `eae8e1cbe`.

## What is under review

- `docs/plans/2026-10-11-review-churn/README.md`, the plan, revision 15. Items 1–10 are ruled (its "Owner rulings, 2026-10-11" section governs where older item text differs). Under review:
  - **Item 11's variant F,** read through the table "Where every item 11 call stands after variant F" and the F section ("Variant F: the owner's refinement of E": points 1–8, its E-versus-F table, F-calls 1–7). **F is the owner's position, deliberately left unruled so you test it.**
  - **Item 12** (architectural decomposition at three moments).
  - **Item 13** (review only a green tip; test cases reviewed in stages).
  - **The revision 15 changes elsewhere:** item 5's per-module `Implements:` floor withdrawn; item 7's reviewer-family rule loosened; `reviewer_families`.
- The reports behind them: `item-11-llr-fitness-report.md` (two analysts on the 302 LLRs; it recommends variant E, which F refines) and `item-11-value-domain-research.md` (the sources for F point 8).
- `pointer-rules.md` and `docs/handoff-2026-10-11-attended-coordinator.md` ("For the owner"), for consistency.
- Earlier reviews and their dispositions are in `reviews/` (Sonnet, Sol, Astra, Fable, `astra-low-r11.md`, `fable-medium-r12.md`, `astra-medium-item11.md`, `fable-medium-item11.md`) and the plan's last section. Don't repeat a dispositioned finding unless its fix is wrong.

## The owner's lens

Long-term design sustainability. Keep behavioural expectations divorced from implementation. Keep the spine's authored links few: every link must earn its upkeep by the orientation it gives a reader (human or LLM) or the check it enables. Prefer derived over authored, and one home per relation.

## The owner's standing rules (check the plan against them)

- **Enforce at the commit, not through history.** A coupling rule is a commit-time check of a commit against its parent, never git-history archaeology or a marker convention.
- **Fix single points of failure; never add fallback, degenerate or legacy paths.** Reviews and judgements are independent of what they judge.
- **Findings are claims:** confirm or refute before acting. Deleting something requires first reading the WI's original rationale.
- **Decisions are confirmed or overruled**, never "approved".
- **Review threat model:** a finding that needs a compromised or contrived host is dismissed.
- **Requirement rows never name implementation carriers** (code files, functions, symbols). Shipped boundary files may be named at LLR/TC only. SN/SR name no files.
- **One configuration file in TOML;** `docs/work/pause` is the only presence-file exception.
- **The kit's scripts stay stdlib-preferred and cross-platform. Edit conservatively,** and flag anything that forces adopters to migrate.

## What to do: two phases, in order (the owner's stance)

### Phase 1: challenge

Is variant F the right direction? Judge it against E, the original proposal (A), the other analysed variants (B–D) and anything better you can name, on the owner's lens. Do the same, more briefly, for items 12 and 13: are they the right response to the problem each states? Ground every claim in a file, a row id or a command you ran. If F is wrong in direction, say so plainly and say what should replace it.

### Phase 2: stress-test (if F, item 12 or item 13 holds, or needs only minor changes)

Go further: find where each breaks down and where contradictions surface. Check at least:
- **F against the rulings.** Ruling 5 (F retires LLR → CMP, which amends "LLRs keep naming their component by id"), ruling 1 (F point 8 extends its allow-set to interfaces), OI-48 (no seams minted for helpers), OI-112 (F claims to answer it), and OI-67 and the 2026-09-20 `realizes` rejection (F claims they stand).
- **Decomposition (b) with `part_of`.** The ladder text ("TERMINAL", "the tier does not recurse"), SR → LLR coverage and orphan rules, the new question of whether a deeper LLR points to its SR, a parent LLR, or derives its parent from the component tree, and the effect on Gilbert (read-only at `C:/Projects/gilbert`).
- **Derivations F relies on.** IF level as the lowest common ancestor, file → component from headers created at design time, blast radius IF → TC → LLR. Do they hold on the kit's real registries: shared kernels, external owners, multi-module LLRs, file-channel handoffs?
- **Thin interfaces.** Under ruling 5, how are IF consumer and requestor roles held, and does F's "approve just in time, class compatibility only" leave any check that OI-67's "verified by nothing" objection would reopen?
- **Item 12.** Does the skill-plus-prompt route actually reach a Codex planner (read `prompts/dual-plan-planner.template.md`, `plan_briefs.py`)? Does the critique cadence (depth 0, the whole tree before build, every second depth) fit the ladder's approval points?
- **Item 13.** Does the green gate reuse one record (the merge slot's `Bar-Green`) without creating a second home for "green"? Does TC-first in lanes contradict the coordinator cycle's current order or item 9's pre-claim flow? Does the gate work in the unattended loop as well as the attended coordinator?
- **Internal consistency.** Do the README, its status table, `pointer-rules.md` and the coordinator handoff agree? Are the counts and citations right?

Say which phase each finding comes from.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [phase 1|phase 2] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

- BLOCKER: a ruling-dependent instruction is wrong or unsafe, breaks an owner rule, or F's direction is wrong.
- MAJOR: an inconsistency, contradiction or factual error that would mislead the owner's ruling or the next session.
- MINOR: precision or wording. Mark wording ambiguities `for clarity`.

Then, under **"Views for the owner"**, one short grounded paragraph each on:
- F-calls 1–7;
- the rows still open in item 11's status table (WI `if_refs`, decomposition (a)/(b) and the parent-LLR question, the module term, IF consumer/requestor roles, interactive dashboard evidence, the IF `data` cells);
- item 13's three calls.

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
