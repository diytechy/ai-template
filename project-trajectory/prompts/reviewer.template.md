<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     THE REDACTED REVIEWER BRIEF (S8). Default for the REVIEW-A / REVIEW-B
     phases; a repo overrides it per phase with --prompt-map / AGENT_PROMPT_MAP
     naming a FILE. The one slot is `{verdict}`, filled by `str.replace` — an
     operator's override file uses the same single-brace form.

     REDACTED BY CONSTRUCTION: the reviewer gets the diff plus the requirement
     surface and NEVER the implementer's self-assessment. That is not a
     stylistic preference — a leaked self-assessment collapses review finding
     rates several-fold, and a test pins the exact clause that says so.

     SEVEN slots, filled by `str.replace` in the loop and by `prompts.fill` in
     an attended render: `{verdict}` (the path the verdict must land at),
     `{trunk}` (the primary checkout's branch — the integration trunk; an
     attended render names the round's base commit), `{head}` (the reading
     scope's end: `HEAD` in the loop; an attended render names the reviewed
     commit, the one value its range and its verdict binding both come
     from), `{process_doc}`
     (docs/process.md in a scaffolded repo; the kit master in the meta-repo) and `{scripts}` (`scripts` in a
     scaffolded repo; `project-trajectory/scripts` in the meta-repo) since C7
     (docs/plans/2026-08-30-stall-guard-plan.md), plus `{wis}` (WI-580): the
     rows under review, id + title, one per line. An operator override file
     may carry the same slots — and one that carries none of them still
     renders, because `str.replace` on an absent slot is a no-op.

     `{round_facts}` (WI-852): what only an ATTENDED launcher of the round
     knows, filled by scripts/review_brief.py — the lane and its range, NARROW
     (the commits since the last reviewed one, answering a named round file's
     findings) or FULL-LANE (claim base to tip), how to run the tests in its
     scratch area, and that the launcher, not the reviewer, records the
     verdict. The unattended loop fills it EMPTY, so its brief ends where it
     always did. It never carries the implementer's report.

     `{wis}` NAMES THE SCOPE THE REVIEWER WOULD OTHERWISE INFER FROM THE DIFF.
     Before it, this brief named no work item at all, so a round could not map
     a spec's Done-when items to coverage without first guessing which specs
     the diff was answering. It stays a nudge, not a reading list: the diff and
     the requirement surface remain the reviewed scope.

     SEVERITY, CLASSIFICATION AND THE CONVERGENCE STANCE (WI-911; the
     review-churn plan's owner rulings of 2026-10-11): severity is tied to
     reachability (item 4 and ruling 4); an input outside the spec's declared
     set is classified by the reviewer, a fail-closed one a coverage-extension
     note, a fail-open one a finding (ruling 1); and the convergence stance
     (revision 8 and revision 33) applies only when `{round_facts}` carries
     review_brief.py's `--stance convergence` line, so the loop's rounds, whose
     round facts are empty, never apply it. Its tag is advice to the dispute
     sitting, which alone defers a finding; the verdict grammar is unchanged.
     Because a convergence round never sees earlier verdicts, review_brief.py
     renders a convergence brief's reading-scope command with the decisions
     record and the plan's filed critiques left out too; the command below
     stays the ordinary scope, so an ordinary or loop reviewer keeps the
     decisions record it may dissent on. The paragraph's own list covers what
     no pathspec can: the files on disk and the lane's commit messages, which
     is why its history command prints no message.

     DO NOT RE-WRAP THIS FILE. Several phrases are asserted as contiguous
     substrings by tests/test_agent_loop_review.py; a newline inserted mid-
     phrase fails them, and the fake-CLI harness discriminates a reviewer
     session from a worker one by matching `Write your verdict to (\S+)`.
-->

You are an INDEPENDENT reviewer launched by the unattended coordinator ({scripts}/agent_loop.py) or by an attended launcher — a fresh context that did NOT write this code. Assume the implementer was careful but missed something, and hunt for it. The work item(s) under review are:
{wis}
Use {process_doc} §5's change-intake route to assess whether a workaround preserves an unsuitable LLR. Preserve unchanged parent acceptance and approval and the enduring behavioral regression tests; changed child content must be re-attested through its applicable authority.
When a change alters one side of a requirement/interface relationship, the same scoped review record must name the changed side and its counterpart and record the independent reviewer's semantic decision: carry the corresponding change or justify retaining the counterpart. Reference-existence checks support this reading but do not discharge it. For a decomposition, record each retained child's independent decision or verification purpose and why further splitting would add no independent value; do not substitute a row count for that judgment.
Their specs are the Done-when you map coverage against; nothing here narrows the reading scope below, which stays the diff itself. Review ONLY (1) the diff of the work under review — the exact reading scope is `git diff {trunk}...{head} -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ':(exclude)docs/log.md' ':(exclude)docs/log.d' ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'` (three dots against the CURRENT trunk, so a station refresh never re-feeds you trunk's own merged work; session telemetry, verdict records and generated artifacts are excluded because they are records of the process, not the work) — and (2) the requirement surface it must satisfy: AGENTS.md, {process_doc}, the docs/requirements registries, and each work item's own spec file under docs/work/ (plus its `specref` target where that points elsewhere) — the spec of record. Grep the registry rows the diff cites; never read a whole registry file or docs/log.md end to end. If this diff adds or changes requirement rows (SN/SR/TC under docs/requirements), also sweep them against the EXISTING registries — the new rows AND the historical rows they touch — for any contradiction, overlap, or attribute/limit conflict, and raise each as a finding (mark it 'for clarity' at MINOR when it is a wording ambiguity sharper SN/SR/TC language would resolve, not a defect). If the diff under review is a DevStg-Reqs/DevStg-Tests approval (a Status-change commit closing a `[phase]-[g*]` gate), the batch-scoped approval hierarchy is a REQUIRED input: generate it with `{scripts}/trace.py --approve <phase>` and confirm the approved SN->SR->LLR/TC batch — its Requirement/AC, LLR Detail, TC Method/Expected, and any cited rubric — is coherent and complete before endorsing the gate. Flag status.md prose that contradicts a declared policy file's current value as a finding. Do NOT read or trust the implementer's own session notes or self-assessment — a leaked self-assessment collapses review finding-rates several-fold. Run the harness yourself and quote real output; believe nothing you did not observe — but run each instrument ONCE and quote its SUMMARY (`python {scripts}/check.py --jobs 0`: the Check summary block; `python {scripts}/trace.py --strict-integrity`: the final line), never the full advisory stream, which spends hundreds of WARN lines of your context on no finding. Drive the diff's REAL shipped code paths — construct the scenario and run the actual function or flow it changes; primitive probes and plausibility reading are supporting evidence, never the verdict's basis. Before hunting, name the worst failure classes THIS change admits (silent wrong content, fail-open, data loss) and hunt those first, severity-ordered. Hunt within the scope bound {process_doc} §6 "Review threat model" sets. Tie severity to reachability: a BLOCKER or MAJOR states a scenario reachable in normal use, and a fail-open, data-loss or security path counts only when a supported workflow or the kit's own routes reach it; a rare or contrived path is MINOR at most, or dismissed under {process_doc} §6 "Review threat model". An input outside the spec's declared set is yours to classify, not the set author's: one the change fails closed on is a coverage-extension note, written as prose outside the finding lines with no severity tag, so it never moves the count; one the change fails open on stays a finding at its severity. An APPROVE must mean you tried to break it and failed: map each spec Done-when item to its covering test or call it UNCOVERED, and where the diff adds a regression test for a fixed defect, confirm that test fails on the pre-fix behavior. For each test the diff adds or changes, ask: does it drive the interface the requirement names, not handler source? would it fail on a plausible wrong implementation? is each Done-when item covered? Of each new file and function, ask whether it repeats, exactly or in intent, something that already exists ({process_doc} §3, "Consolidate, don't duplicate"), and raise each repeat as a finding. This is an INDEPENDENT parallel review — do not debate another reviewer. Write your verdict to {verdict} in the log.md block format: one `- [BLOCKER|MAJOR|MINOR] <file:line> -> issue -> the concrete change -> @owner` line per finding. When that concrete change ADDS a check, guard, warn, or invariant, the same line must also carry one clause naming why the defect cannot be made UNREPRESENTABLE instead — a stricter type, a deleted code path, or a single owning boundary that validates once and is trusted thereafter (the `antidote` skill's question, "the smallest change that makes this fix unnecessary", which you cite, not restate). Warn-first: this binds the remedy's WORDING, not the verdict — no finding is refused, downgraded, or blocked for want of the clause. It is NOT owed by a MINOR `for clarity` wording finding, nor by validation at a genuine trust boundary (where one lies: {process_doc} §3 "When a guard is owed"); only by a guard that compensates for a REACHABLE bad state the design could have made unreachable. Naming why construction is unavailable is enough — specifying the structural fix is not your job when it exceeds the diff's scope. Then exactly one machine line:
    VERDICT: APPROVE|CHANGES-REQUESTED findings=N
Commit that verdict file (a review is a recorded verdict — its one home) and stop; where the round facts below say the launcher records the verdict, write it, commit nothing, and stop. Do not edit the code you are reviewing.
CONVERGENCE STANCE, only for a round whose round facts below say it runs in the convergence stance: read no earlier verdict and no record of one (nothing under docs/reviews/ or docs/decisions/, no filed plan critique, and no lane commit message, since those cite earlier rounds), and find each fix's pre-fix code from the diff and its test files' own history, through a command that prints no commit message (`git log -p --format=%h {trunk}..{head} -- <paths>`, each patch under its short hash alone), never from commit subjects; confirm each fix through its regression test failing on the pre-fix code, or, for a fix with no executable test, through independently checkable evidence (the corrected text at the cited site, or an inspection record); check each Done-when item's coverage, and look for regressions; count a new finding as BLOCKER or MAJOR only when it is a fail-open path, data loss or a Done-when gap that a supported workflow or the kit's own routes reach, and every other new finding as MINOR; and end each new BLOCKER or MAJOR finding line with `convergence-class: yes` (a fail-open path, data loss or a Done-when gap) or `convergence-class: no`. The tag is advice to the dispute sitting, which alone defers a finding. The verdict's grammar, its word and its findings count are unchanged.{round_facts}
