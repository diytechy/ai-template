# Independent review: the review-churn plan, revision 11 (item 11 and revisions 7–11)

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write your review where the launch instructions say.

## What is under review

The worktree `C:/Projects/ai-template.wt/review-churn-plan-astra-m`, a detached checkout at commit be2d10c3d (plan revision 11). Read these in full:

- `docs/plans/2026-10-11-review-churn/README.md`, the plan. Its **"Owner rulings, 2026-10-11"** section is what the owner decided for items 1–10; where older item text differs, that section governs. The "Revision 6–8 clarifications" box mixes owner rulings (revision 8) with proposals awaiting the owner's confirm or overrule.
- `docs/plans/2026-10-11-review-churn/pointer-rules.md`: the ruled pointer table, and the item 11 proposal as a second diagram.
- `docs/handoff-2026-10-11-attended-coordinator.md`: the coordinator's boot document, which restates the rulings as working instructions.
- `docs/plans/2026-10-11-review-churn/reviews/`: the earlier independent reviews and their briefs: Sonnet and Sol of revision 2 (`sonnet.md`, `sol.md`), GPT-6 Astra at low effort of revisions 3–5 (`astra.md`), and Claude Fable 5.1 at low effort of revision 6 (`fable.md`). The plan's last section dispositions every one of their findings. Don't repeat a dispositioned finding unless its fix is wrong or incomplete; say which.

**Give the closest look to item 11** (what points where), which nobody has reviewed, and to whatever revisions 7–10 changed: the convergence round's fresh-reviewer rule (no prior verdicts; regression tests confirm fixes), test files naming their TC, the empty-pool refusal, and item 11's history, proposals and terms, and the owner's two queries on it (revision 11).

## The owner's standing rules (check the plan against them)

- **Enforce at the commit, not through history.** A coupling rule is a commit-time check of a commit against its parent, never git-history archaeology or a marker convention.
- **Fix single points of failure; never add fallback, degenerate or legacy paths.** Reviews and judgements are independent of what they judge.
- **Findings are claims:** confirm or refute before acting. Deleting something requires first reading the WI's original rationale.
- **Decisions are confirmed or overruled**, never "approved".
- **Scope is settled where a row is born** (scope critique); there is no lane-size tripwire.
- **Review threat model:** a finding that needs a compromised or contrived host is dismissed.
- **Requirement rows never name implementation carriers** (code files, functions, symbols). Shipped boundary files may be named at LLR/TC only. SN/SR name no files.
- **One configuration file in TOML;** `docs/work/pause` is the only presence-file exception.
- **Re-sync is applied by an LLM** and needs no new mechanization.
- **The kit's scripts stay stdlib-preferred and cross-platform. Edit conservatively,** and flag anything that forces adopters to migrate.

## What to do

### 1. Item 11's history, checked against the repository

Check each row of item 11's "How the links got their shape" table: the `docs/log.md` entries (search by date, e.g. 2026-07-09, 2026-07-14, 2026-08-12, 2026-08-13, 2026-08-15, 2026-08-29, 2026-09-20), OI-14, OI-20, OI-21, OI-39/OI-42, OI-48, OI-67 (open-issue records under `docs/`; search for them), the 2026-09-20 assumption-tier plan (search `docs/` and `docs/archive/`), WI-057, WI-441, WI-445, WI-527, and any commits cited. Say which rows are accurate, which misquote or misdate, and anything material the table omits. Check the "Where things stand today" counts too (`Implements:` lines, functions, LLRs covered, `Contract IF-NNN` citations, files carrying each, the 55 LLRs in modules owning no IF, 95 of 316 TCs listing an IF).

### 2. Item 11's proposal: does it hold together?

Item 11 is in scope **in full**: its history, terms, proposal table, nuances, the owner's two queries, and **every one of its open calls**. For each open call, give a grounded view the owner can rule on; leave none unaddressed. Judge in particular:

- each module stating the contract of every interface it serves;
- the IF → LLR/SR pointer (and whether it re-creates the "two homes" objection of 2026-09-20 or OI-67's "verified by nothing" objection);
- module (file) → CMP declared in the file header, IF → CMP derived;
- the 55 LLRs in modules with no interface (add `call`-channel seams, reframe, or retire);
- the interaction with item 5's removal of the LLR `module` / `code_symbol` cells, and with SR-180 / LLR-180 / TC-175 (the "symbol resolves" discharge gate) — what re-founds the LLR floor;
- whether IF rows should gain an approval status once they carry requirement weight.

### 3. The owner's two queries on item 11

**Query 1 — contracts only where served.**

- Confirm that nothing in the plan, the kit's checks (`project-trajectory/scripts/`) or `project-trajectory/PROCESS.md` would require a contract per function or per module. Search the checks that read `Contracts:` / `Contract IF-NNN` lines.
- Find today's "every shipped module carries an `Implements:` tag" rule (where it is stated and which check enforces it) and say what it becomes under item 11.
- Say what, if anything, can mechanically refuse a contract cited by a symbol that doesn't realize the seam (the candidates in the plan: the contract's TCs exercising the citing symbol; the citing file declaring the IF's owning component or a declared consumer; review alone). Is review alone acceptable, given item 1's preference for closed rules?

**Query 2 — work items bound to the interfaces they serve.**

- Read the WI schema: the `docs/work/` spec front matter, `project-trajectory/registries/work-items.template.csv` (or wherever the template lives), `project-trajectory/PROCESS_OPTIONS.md`'s work-items layer, and the consolidation census in `check_trajectory.py`.
- Judge whether an `if_refs` cell should replace or sit beside `sr_refs`; how rows with no interface (process, adjudication, doc rows) stand; and whether `needs` edges should be checked against, or derived from, the interfaces' provider and consumer order.
- Check what the requirement rows' parent links can and can't express today (`sn_refs`, `sr_refs`, `delivered_with`), and whether the queue should mirror that tree.
- PROCESS.md §5 recurses through sub-scope SRs per component ("the tier does not recurse, the activity does"; `DevStg-LLReqs` is terminal). Find how a sub-scope SR points to its parent obligation and its component scope, or confirm that no cell does (look at the SR schema in `kitlib/spine.py`, the SR registry header, and the ladder text).

### 4. The two decomposition alternatives (owner's request)

Item 11 records two readings: **(a)** SRs at every component scope, decomposing to a terminal LLR (the 2026-08-12 ladder as written), and **(b)** SRs only at the system boundary, with architecture decomposing them into LLRs **recursively** (an LLR may decompose an LLR). The owner leans to (b) on churn grounds but has not ruled. Give the strengths and weaknesses of each, judged on **long-term design sustainability**, not on what past rulings committed to. Give the **concrete migration cost of (b)**: a parent-LLR pointer, the ladder's "TERMINAL" and "the tier does not recurse" text, the `DevStg-Reqs`/`DevStg-Arch` recursion, SR → LLR coverage and orphan rules (`trace.py`), the CMP tree, adopters' schemas, and its **effect on physical projects** (Gilbert, read-only at `C:/Projects/gilbert`, which mixes physical parts with software). Say what item 11's discharge rule (an LLR is discharged when a code-cited interface carries it) and the 2026-08-13 form rule ("a single shall … applied to interfaces going to the respective component level") imply for each reading. Give a recommendation the owner can confirm or overrule, with its reasons.

### 5. Terminology cross-check (owner's request)

These terms were settled many sessions ago, and the kit must stay compatible with physical projects.

- **Module.** Item 11 says a module is one unit of realization represented by one file in git: a code file in software, a part's file where physical parts join, with "file" as a synonym. Find the earlier definitions and check this reading against them: the old `modules.csv` / `MOD-###` registry and its move to repos (search `docs/log.md`, `docs/archive/`, git history of `project-trajectory/registries/`), `PROCESS.md`, `PROCESS_OPTIONS.md`, `ADOPTING.md`, and `docs/registry-machinery-reference.md`. Check it against Gilbert's PART and ASSET registries (read-only, `C:/Projects/gilbert`). Does a physical part have "one file in git"? Does a PART row play the role a module plays in software, or a component's?
- **Contract.** Item 11 says a contract states the bounds of what crosses one interface (output range, stdout limits, CLI output pattern, refusal shape), not the business behaviour, which is the LLR's. Check that against PROCESS.md (the interface section, and "an interface says what crosses …"). Sample at least fifteen existing `Contract IF-NNN:` bodies in `project-trajectory/scripts/` and count how many restate obligations instead of bounds; name examples.

### 6. Depth, and how it sits with items 3 and 9

You may spawn your own sub-agents to drill into details (history, call sites, Gilbert), where your tooling allows. Fold their findings into your one review file; they modify nothing. Also judge item 11 query 2's last bullet: does an interface make the natural split unit for item 3 (S1, independent deliverables), and does item 9's S4 criterion ("two or more IF seams") become countable?

### 7. Internal consistency

Where does revision 7–11 text contradict older item text, pointer-rules.md (both diagrams) or the coordinator handoff in a way a reader could follow wrongly? For example: the session budget (the clarifications say at most eight sessions; check "Sequence and how we'll know" and item 4's prose), the revision count in the status line and the revision history paragraph, and whether the handoff's "For the owner" lists item 11's open calls.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

- BLOCKER: a ruling-dependent instruction is wrong or unsafe, or breaks an owner rule.
- MAJOR: an inconsistency or factual error that would mislead the next session or the owner's ruling.
- MINOR: precision or wording.

Mark wording ambiguities `for clarity`.

Then, under the heading **"Item 11: views for the owner"**, one short grounded paragraph per open call of item 11 (eight calls), per owner's query (two), and on the decomposition alternatives (with your recommendation), and on the terminology cross-check (module, contract).

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
