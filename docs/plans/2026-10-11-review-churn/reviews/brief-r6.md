# Independent review: the review-churn plan, revision 6 (the rulings and the Astra revisions)

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository. Never read `OWNER_SCRATCHPAD.md`. Write your review where the launch instructions say.

## What is under review

The worktree `C:/Projects/ai-template.wt/review-churn-plan-r6`, a detached checkout at commit 17e87484a. Read these in full:

- `docs/plans/2026-10-11-review-churn/README.md`, the plan. Its **"Owner rulings, 2026-10-11"** section is what the owner decided. The rest is reasoning from revisions 2–4, some of it written before the rulings.
- `docs/plans/2026-10-11-review-churn/pointer-rules.md`: what each spine artifact may point to or name under the rulings.
- `docs/handoff-2026-10-11-attended-coordinator.md`: the handoff the next coordinator session starts from. It restates the rulings as working instructions and sets a first batch.
- `docs/plans/2026-10-11-review-churn/reviews/`: the earlier independent reviews (Sonnet and Sol of revision 2; GPT-6 Astra of revisions 3–5, in `astra.md`) and their briefs. The plan's last section dispositions every one of their findings. Don't repeat a dispositioned finding unless its fix is wrong or incomplete; say which.

Revision 6 (the Astra fixes, and the "Revision 6 clarifications" box in the rulings section, which are proposals awaiting the owner's confirm or overrule) has not been reviewed by anyone. Give it the closest look: check each Astra fix actually landed consistently across the plan, pointer-rules.md and the handoff, and whether a fix introduced a new inconsistency or gap.

## The owner's standing rules (check the plan and handoff against them)

- **Enforce at the commit, not through history.** A coupling rule is a commit-time check of a commit against its parent, never git-history archaeology or a marker convention.
- **Fix single points of failure; never add fallback, degenerate or legacy paths.** Reviews and judgements are independent of what they judge.
- **Findings are claims:** confirm or refute before acting. Deleting something requires first reading the WI's original rationale.
- **Decisions are confirmed or overruled**, never "approved".
- **Scope is settled where a row is born** (scope critique); there is no lane-size tripwire.
- **Review threat model:** a finding that needs a compromised or contrived host is dismissed.
- **Requirement rows never name implementation carriers** (code files, functions, symbols). Shipped boundary files may be named at LLR/TC only. SN/SR name no files.
- **One configuration file in TOML;** `docs/work/pause` is the only presence-file exception.
- **Re-sync is applied by an LLM** and needs no new mechanization.
- **The kit's scripts stay stdlib-only and cross-platform. Edit conservatively,** and flag anything that forces adopters to migrate.

## What to do

1. **Internal consistency.** Where does a ruling contradict the plan's older item text, the pointer rules or the handoff in a way a reader could follow wrongly? Look especially at: item 4's settings versus the handoff's "How to run reviews now"; item 5's refined reference rule versus the pointer table and item 5's layer-2 check; item 6 (after the build, not in the hook) versus older text; item 9 (dispositions; dual kept) versus older text; item 10 versus the rest.
2. **Factual claims new in revisions 3–5.** Check them against the repository. Examples:
   - that all three git hooks refuse without Python 3.11+ (`project-trajectory/hooks/`, `kit-python.sh`);
   - the 14 `stack.ini` parse sites;
   - `stack.ini`'s 1,277 lines and 70 settings;
   - no adopter on disk has taken the process.toml migration (C:/Projects/gilbert, Finance-Auditor, NotHomeWrecker, FileBackup; read-only);
   - CMP rows having no module field;
   - the 316 `Contract IF-NNN` citations;
   - `trace.py --strict` exiting 1 on LLR-292;
   - the reference-census counts (about 18 SN/SR rows to reword);
   - the handoff's lane facts (tips, sessions, watermarks) against `docs/handoff-2026-10-11-leg03-coordinator.md` and git.
3. **The rulings' design.** Within each ruling, is there a hole the owner would want flagged? For example:
   - does the review cap with an adjudicated exit let a real defect land unrecorded?
   - does the convergence round conflict with "reviews independent"?
   - does folding `agents-enabled` into a key lose the consent semantics?
   - does dropping the shell grep reopen M-42's fail-closed requirement anywhere, such as the missing-scripts-directory case?
   - does "boundary files at LLR/TC only" clash with how the shipped-file inventory is derived?
4. **The handoff as a boot document.** Could a fresh coordinator follow it correctly? Is anything missing, ambiguous or unsafe: claim procedure, the review shape done by hand, the Sonnet stand-in's brief and isolation, order, close-out?

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

- BLOCKER: a ruling-dependent instruction is wrong or unsafe, or breaks an owner rule.
- MAJOR: an inconsistency or factual error that would mislead the next session.
- MINOR: precision or wording.

Mark wording ambiguities `for clarity`.

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
