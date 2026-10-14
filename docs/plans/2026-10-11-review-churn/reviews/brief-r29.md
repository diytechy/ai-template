<!-- The brief for the revision 29 review pair (GPT-6 Astra and Claude Fable 5.1, both at medium effort), run from review-handoff-r29.md. Render one copy per reviewer, replacing {TIP} with the reviewed commit, {WT} with that reviewer's detached worktree, {OUT} with its review file and {ROOT} with the review root. Neither reviewer sees the other's review. -->

# Independent review: the whole review-churn plan, revision 29

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at `{OUT}`.

## Where things are

- **Repository (read-only):** `{WT}`, a detached worktree at commit `{TIP}`. It shares the main repository's refs, so `git -C {WT} show contract_split:<path>` works. Python 3.11+ with `tomllib`: the primary checkout's `.venv` interpreter, by absolute path (the worktree has no `.venv` of its own). Scratch scripts may go in `{ROOT}/scratch/`.
- **What changed since the last review** (revision 22, reviewed at `3be48cfaa` by GPT-6 Astra and Claude Fable 5.1, both at medium): `git -C {WT} log --oneline 3be48cfaa..{TIP} -- docs/plans docs/handoff-2026-10-11-attended-coordinator.md docs/status.md` and `git -C {WT} diff 3be48cfaa..{TIP} -- docs/plans/2026-10-11-review-churn`. Revision 23 dispositioned the revision 22 reviews; revisions 24–27 and 29 record the owner's rulings on items 14–16; revision 28 consolidated the plan, moving its revision log and every review's dispositions verbatim into `history.md`.

## What is under review: the whole plan

`docs/plans/2026-10-11-review-churn/README.md`, revision 29, all of it. Read it whole before judging any part. Its Status states what is ruled, open and proposed; the rulings section governs where an item's text differs. In particular:

- **Items 1–10 are ruled.** Challenge a ruling only where the plan's later text contradicts it, applies it wrongly, or where a later revision undermines it.
- **Item 11, variant F**, the owner's position (decisions 1 and 2; F-calls 1, 2, 8 and 9 answered; F-calls 3–7 open). **Item 12** is open. **Item 13** is answered, with the authority vocabulary rewrite and the coordinator role's side open. **Decision 4** is ruled. These were reviewed at revision 22; their dispositions are in `history.md`. Don't repeat a dispositioned finding unless its fix is wrong or a later revision broke it.
- **Item 14** (revisions 21–25): retire the perspective-record sidecar WI-688 built, apply the owner's 2026-09-06 SN-036 ruling's four row acts, wire the hat questions into the briefs for the SN → SR step only, delete the existing sidecar, and drop SAFETY from this repo's roster. Item 12's audit also rechecks the hats (revision 24).
- **Item 15** (revision 25, new): one work item per lane. It retires the managed loop's spine batch and ports `contract_split`'s drafted rows.
- **Item 16** (revisions 25–29, new): a watermark carrier lane that every mint draws from (spine ids, WI ids, act seqs) under a short lock, merged with each landing, with a landing check that refuses unreserved marks; the owner's keep-or-mint rule for ids; and the owner's note that the adjudicator need not wait on landing order, which the plan records for a closer look (the whole-file snapshot question).
- **Background for items 14–16:** `docs/plans/2026-10-13-contract-split-divergence.md` (closed; its §5 records the owner's answers) and `git -C {WT} show contract_split:<path>` for the branch it describes.
- **Companion files, for consistency:** `history.md`, `pointer-rules.md`, `docs/handoff-2026-10-11-attended-coordinator.md` ("For the owner"), `docs/status.md`'s resume line, `item-11-llr-fitness-report.md` and `item-11-value-domain-research.md`.

## The owner's lens

Long-term design sustainability. Keep behavioural expectations divorced from implementation. Keep the spine's authored links few: every link must earn its upkeep by the orientation it gives a reader (human or LLM) or the check it enables. Prefer derived over authored, and one home per relation. Duplication, exact or in intent, is the curse of maintainability. Review sessions are the scarce resource; deterministic checks are cheap. **Do not over-engineer:** a finding whose remedy is new machinery against a speculative corner case will be dismissed.

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
- **One work item per lane** (revision 25). **Snapshots are permitted in a lane when ruled in that lane** (revision 25, overruling the stranded 2026-09-07 statement). **Keep or mint an id** (revision 26): lean toward a new id; keep one whose spirit is retained when that costs fewer changes overall.

## Severity, as the owner calibrates it

- **Dismiss a finding that needs a compromised or contrived host, or a contrived, improbable scenario.** The plan does not design against those; at most, note one in a sentence under "Views", never as a finding.
- **BLOCKER** only where a ruling-dependent instruction is wrong or unsafe, an owner rule is broken, or a direction is wrong.
- **MAJOR** only where an inconsistency, contradiction or factual error would actually mislead the owner's ruling or the next session's build.
- **MINOR** for precision and wording; mark wording ambiguities `for clarity`.

Severity tracks plausibility and impact, not ingenuity. A plan at this stage needs findings that would change what gets built.

## What to do: two phases, in order

### Phase 1: challenge

Is each new direction right? Judge, on the owner's lens: item 14 as it now stands (the SN → SR scope, the wiring, SAFETY); item 15; item 16's carrier lane against any simpler design you can name; the keep-or-mint rule; and the adjudicator without the landing latch. Ground every claim in a file, a row id or a command you ran. If a direction is wrong, say so plainly and say what should replace it.

### Phase 2: stress-test

Find where the plan breaks down and where contradictions surface. Spend most of the effort on what no review has seen:

- **Item 16's carrier:** reserve-at-draft against how lanes mint today (`trace.py --bump-ids`, `docs/id-watermark` and its integrity rule), the max-per-space merge at landing, the landing check that refuses unreserved marks, WI ids moving off trunk, and act seqs against `docs/archive/last_approved/acts.toml`.
- **Item 16's adjudicator note:** is the plan's reading right that the landing latch also guards the whole-file snapshot copies (`intake.py snapshot`, `acceptance_record.staged_snapshot_findings`)? Is anything else it guards missing?
- **Item 15:** the port list against `contract_split`'s rows (`git -C {WT} diff 607cf609 contract_split -- docs/requirements docs/test`), what in `dispatch.py`, `integrate.py`, `agent_loop.py` and `handback.py` the batch retirement touches, and its interaction with item 16's exclusivity question.
- **Item 14:** the decomposition-round bound (SN → SR) against the two sitting templates and the composer, and the retirement list's completeness.
- **The consolidation:** does the Status match the items and the rulings? Did anything a later reader needs leave with the history? Do the summary table, phase 0 and `docs/status.md` agree?
- **The rest of the plan, briefly:** anything a revision 23–29 change broke.

Say which phase each finding comes from.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [phase 1|phase 2] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

Then, under **"Views for the owner"**, one short grounded paragraph each on:
- item 14 as it now stands;
- item 15;
- item 16: the carrier, the keep-or-mint rule, and the adjudicator without the latch;
- the consolidation, and anything else the owner should weigh.

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
