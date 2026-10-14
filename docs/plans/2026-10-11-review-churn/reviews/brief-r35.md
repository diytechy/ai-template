<!-- The brief for the revision 35 review pair (GPT-6 Astra and Claude Fable 5.1, both at medium effort), run from review-handoff-r35.md. It reviews only what revisions 32–35 changed, and cross-checks revision 35's rulings for conflicts. Render one copy per reviewer, replacing {TIP} with the reviewed commit, {WT} with that reviewer's detached worktree, {OUT} with its review file and {ROOT} with the review root. Neither reviewer sees the other's review. -->

# Independent review: what revisions 32–35 of the review-churn plan changed, before the build

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. The whole plan was reviewed at revision 31 by two reviewers at high effort; revisions 32–35 folded in their findings and the owner's answers, and **that new text has not been reviewed**. Revision 35 is large: the owner ruled every call the plan still had open, walking them one at a time, so nothing in the plan is open any more. Your job is that delta: is each change correct against the code, complete, and consistent with the rest of the plan and the coordinator's queue, and do revision 35's rulings conflict with each other, with earlier rulings, or with text that still says otherwise? Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at `{OUT}`.

## Where things are

- **Repository (read-only):** `{WT}`, a detached worktree at commit `{TIP}`. It shares the main repository's refs. Python 3.11+ with `tomllib`: the primary checkout's `.venv` interpreter, by absolute path (the worktree has no `.venv` of its own). Scratch scripts may go in `{ROOT}/scratch/`.
- **`contract_split`** means its tip `961f9e47`, which `origin/contract_split` holds. The local `contract_split` branch is dead (owner); never read it.
- **The delta under review:** `git -C {WT} log --oneline 4a25720e2..{TIP}` and `git -C {WT} diff 4a25720e2..{TIP} -- docs/plans/2026-10-11-review-churn docs/handoff-2026-10-11-attended-coordinator.md docs/status.md`. Revision 32 dispositioned the revision 31 reviews (`history.md`, "Review of revision 31", which says what was taken, cut down and dismissed, and why); revision 33 records the owner's answers to revision 32's two calls; revision 34 sequences WI-902's reshape; revision 35 records the owner's rulings on every remaining call (the rulings section's "Owner rulings, 2026-10-14 (revision 35)"), rules OI-112 in `docs/requirements/open-items.toml`, cancels WI-871, and updates `pointer-rules.md`. Include `docs/requirements/open-items.toml` and `docs/archive/work/cancelled/WI-871-interfaces-as-spine-io.md` in the diff you read.

## What is under review: the delta, read in place

Read the plan's Status and rulings section first, then each section the diff touches **whole**, in its current form: items 2, 6, 8, 12 and 13 where changed, item 11's status table and variant F entire, item 16 entire, the Sequence table, `pointer-rules.md` entire, and the coordinator handoff's "The queue" section entire (its table is what the next coordinator session works from). Text the delta did not touch is out of scope, unless a change breaks it or contradicts it.

- **Ruled:** everything the rulings section lists, through revision 35. Challenge a ruling only where the plan's text applies it wrongly, where it conflicts with another ruling, or where building it as written would make a lane redo work. Don't re-argue a ruling's direction; the owner chose it. Where you believe one is unsound, say so once under "Views for the owner", with evidence.
- **Already dispositioned:** the revision 31 round. Don't repeat a finding it dispositioned, including the ones it dismissed or cut down, unless the fix it chose is wrong, incomplete, or contradicted elsewhere.

## The owner's lens

Long-term design sustainability. Keep behavioural expectations divorced from implementation. Keep the spine's authored links few: every link must earn its upkeep by the orientation it gives a reader (human or LLM) or the check it enables. Prefer derived over authored, and one home per relation. Duplication, exact or in intent, is the curse of maintainability. Review sessions are the scarce resource; deterministic checks are cheap. **Do not over-engineer:** a finding whose remedy is new machinery against a speculative corner case will be dismissed. The owner wants holes found before the build, not a longer list.

## The owner's standing rules (check the plan against them)

- **Enforce at the commit, not through history.** A coupling rule is a commit-time check of a commit against its parent, never git-history archaeology or a marker convention.
- **Fix single points of failure; never add fallback, degenerate or legacy paths.** Reviews and judgements are independent of what they judge.
- **Findings are claims:** confirm or refute before acting. Deleting something requires first reading the WI's original rationale.
- **Decisions are confirmed or overruled**, never "approved".
- **Requirements never reference code.** No implementation carrier (code file, function, symbol) in any requirement row. Shipped boundary files may be named at LLR/TC only; SN/SR name no files; IF and CMP rows name no code or files. Code points up to requirements; tests may name modules.
- **One configuration file in TOML** (`docs/process.toml`); `docs/work/pause` is the only presence-file exception.
- **The kit's scripts stay stdlib-preferred and cross-platform;** a dependency enters only through a reviewed row in `docs/dependencies.md`. **Edit conservatively,** and flag anything that forces adopters to migrate.
- **Owner-or-delegate is one role**, distinct from an autonomous run, which the kit's machinery starts and marks.
- **A guard where construction suffices is ceremony** (the 2026-09-06 ruling item 14 applies).
- **One work item per lane.** **Snapshots are permitted in a lane when ruled in that lane.** **Keep or mint an id:** lean toward a new id; keep one whose spirit is retained when that costs fewer changes overall, after checking the id's other users against the amended meaning.

## Severity, tied to rework

Every finding names its **rework scenario**: which lane or item, at which step, would build the wrong thing or have to redo work, and why. A finding with no such scenario is a view, not a finding.

- **Dismiss a finding that needs a compromised or contrived host, or a contrived, improbable scenario.** The plan does not design against those; at most, note one in a sentence under "Views", never as a finding.
- **BLOCKER** only where following the plan as written would build something wrong or unsafe, break an owner rule, or rest on a wrong direction.
- **MAJOR** only where an inconsistency, missing step, false claim about existing code, or ordering error would actually cost a lane rework or mislead an owner ruling.
- **MINOR** for precision and wording; mark wording ambiguities `for clarity`.

Severity tracks plausibility and rework cost, not ingenuity.


## What to check

Say which check each finding comes from.

### Check 1: does each new claim hold against the code?

Every sentence the delta adds that says how existing code behaves, or that an existing mechanism "is", "can", "stays" or "needs no change", is a claim: open the code and confirm or refute it. Revision 32's findings were all of this kind. At least these:

- **Item 16's verdict/act split.** The plan says an early sitting ends at its committed verdict and "the act is a later turn of the same retained adjudicator, after the rebase". Can it be, today? Read `coordinator_adjudicate.py`, the session-keep rules it uses, `adjudicate_brief.compose` and the sitting templates it fills (first-approval, amendment, combined), including the held-rung arms (`intake.adjudication_action`). Name what B1 must change for the split to work, and whether any of it is more than template text and the composer's wording.
- **Item 8's change check between `act` and `record`.** Can the coordinator's wrappers (`coordinator-tools/sol_review.sh`, `terra_author.sh`, outside this repository at `C:/Projects/ai-template.wt/coordinator-tools/`) use that seam, and does committing two parallel reviewers' logs one after the other fit `agent_common.commit_telemetry`?
- **Revision 33's narrowed carrier.** With act seqs and WI ids off the carrier, is item 16 internally consistent (steps 1–3, the landing, the measure, the latch's guards)? Does anything else in the plan, the handoff or the code still rely on the carrier for an act seq or a WI id?
- **The reservation record as a header line** of `docs/id-watermark`, copied into the lane and unioned at landing: does that fit `trace.py`'s watermark reader and its correction-record checks?

- **WI-858's Trust ruling** (`docs/decisions/coordinator-2026-10-11.toml` D-004; WI-858's spec under `docs/work/`), confirmed by the owner with a request that this review look at it: a lockless marker carrier for the session store, published first and applied under a short lock, folded by one pure function. Nothing is built yet. Could it break in normal use (a lost or double-applied marker, a record retired or kept wrongly, a reader that disagrees with the locked applier)? Read `session_keep`'s store and lock code to judge it.

A question a builder answers in a minute from the code is not a finding. Report only what would cost rework.

### Check 2: the queue

The handoff's queue table now runs: a "pre" trunk fix, B1, G, B2–B4, WI-798, P1–P8, then leg 03's rows. For each row, play its spine author or builder at the first step. Does any row depend on something scheduled after it? Do two rows edit the same surface in an order that forces one to redo the other? Is anything in the plan's phase 1 still missing? Check the stated constraints against each other and against the plan: WI-902 (B4) after B1 and G and before items 15 and 16 (P4, P5); item 13's gate (P1) after item 6 (B2); item 16 after item 15; item 14 (P3) before item 5's migration and the FileBackup re-sync; item 12's text (P6) after its W3 dry run and F-call 6's ruling; WI-897 last.

### Check 3: revision 35's rulings, cross-checked

For each revision 35 ruling: does any text in the plan, `pointer-rules.md`, the coordinator handoff or `docs/status.md` still say otherwise; does it conflict with another ruling, old or new; and would building it as written leave a lane without something it needs? At least these:

- **The parent-LLR link** (F-call 5): only a top-level LLR carries `sr_refs`, a child's SR derived up the chain, a parent discharged by its children plus an integration TC. Check it against PROCESS.md §4's ladder ("TERMINAL", "the tier does not recurse"), SR → LLR coverage and the orphan rules (`trace.py`), F's placement and scope rules (an LLR's scope is its IF owner's component), F-call 8 (an LLR need not name an IF), keep-or-mint, and the plan text that still describes flat LLRs.
- **Consumers and requestors handed over like the form,** while the owner stays authored (F-call 1 (i)): is the asymmetry coherent? What does the role-typed citation do to the uniqueness rule (exactly one in-tree file states `Contract IF-NNN:`) and to F-call 1's over-claim check?
- **F-call 3's repeat check in `trace.py --strict`,** not the hook: does anything still call it a commit check?
- **"Module" retired as a spine term:** where do the kit's shipped docs and schemas still give it a spine meaning that items 5 and 11 don't already remove?
- **"human-or-delegate" replacing "owner-or-delegate",** and the key rename to `human_or_delegate_approval_through` in item 10's migration: is the vocabulary consistent across the plan's items 10 and 13?
- **Headless coordinator legs marked as autonomous runs:** what does that change for `overnight_legs.py` and for the acts a headless leg may take?
- **OI-112 ruled and WI-871 cancelled** in one commit: does the ruling-sync rule hold, and does anything else still cite WI-871 or a pending OI-112?
- **The Architect role owning `runtime-flows.md`**, and item 12's cadence (the every-two-levels critique always runs).

### Check 4: consistency

Do the plan's Status, summary table, rulings section, item texts and Sequence agree with each other and with the handoff's queue and "For the owner" block and `docs/status.md`'s resume line, after revisions 32–35?

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [check 1|2|3|4] <file:line or section> -> what is wrong (claim checked / evidence found) -> rework it would cause -> the concrete change

Then, under **"Views for the owner"**, at most three short grounded paragraphs: anything the owner should weigh before the first lane is filed.

Then a short paragraph naming what you verified and found correct, including the claims from check 1 that hold.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
