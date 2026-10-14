<!-- The brief for the revision 31 review pair (GPT-6 Astra and Claude Fable 5.1, both at high effort), run from review-handoff-r31.md. Render one copy per reviewer, replacing {TIP} with the reviewed commit, {WT} with that reviewer's detached worktree, {OUT} with its review file and {ROOT} with the review root. Neither reviewer sees the other's review. -->

# Independent review: the whole review-churn plan, revision 31, before the build

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. This is the last review before the plan's first lanes are built, so the question is no longer only "is this right?" but "what here will make a lane redo work?" Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at `{OUT}`.

## Where things are

- **Repository (read-only):** `{WT}`, a detached worktree at commit `{TIP}`. It shares the main repository's refs. Python 3.11+ with `tomllib`: the primary checkout's `.venv` interpreter, by absolute path (the worktree has no `.venv` of its own). Scratch scripts may go in `{ROOT}/scratch/`.
- **`contract_split`** means its tip `961f9e47`, which `origin/contract_split` holds: `git -C {WT} show 961f9e47:<path>`. The local `contract_split` branch stops at the common ancestor `607cf609` and is dead (owner); never read it.
- **What changed since the last review** (revision 29, reviewed at `4c5287d2d`): `git -C {WT} log --oneline 4c5287d2d..{TIP}` and `git -C {WT} diff 4c5287d2d..{TIP} -- docs/plans/2026-10-11-review-churn`. Revision 30 dispositioned the revision 29 reviews (`history.md`, "Review of revision 29"); revision 31 records the owner's answers to revision 30's calls (the rulings section).

## What is under review: the whole plan

`docs/plans/2026-10-11-review-churn/README.md`, revision 31, all of it. Read it whole before judging any part. Its Status states what is ruled, open and proposed; the rulings section governs where an item's text differs.

- **Ruled:** items 1–10, decision 4, and items 14, 15 and 16, including revision 31's answers (verdicts move between lanes while acts keep landing order; the reservation record; keep-or-mint with its cross-reference). Challenge a ruling only where the plan's own text contradicts it, applies it wrongly, or would make a lane redo work.
- **The owner's position:** item 11's variant F and item 13. **Open:** item 11's F-calls 3 and 5–7, item 12, and the rest of phase 0. Don't design the open calls; do say where an open call blocks a phase-1 lane that the plan schedules as if it didn't.
- **Already dispositioned:** the revision 22 and revision 29 rounds, in `history.md`. Don't repeat a dispositioned finding unless its fix is wrong, incomplete, or broken by a later revision.
- **Companion files, for consistency:** `history.md`, `pointer-rules.md`, `docs/handoff-2026-10-11-attended-coordinator.md` (its queue table and "For the owner"), `docs/status.md`'s resume line, and `docs/plans/2026-10-13-contract-split-divergence.md`.

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

## What to do: four phases, in order

Say which phase each finding comes from.

### Phase 1: challenge

Is each direction still right after revisions 30 and 31? Judge briefly, on the owner's lens: item 16 as now ruled (the reservation record, verdicts moving while acts keep landing order), the keep-or-mint cross-reference, and anything earlier that a revision 30–31 change undermines. If a direction is wrong, say so plainly and say what should replace it.

### Phase 2: pre-mortem

Assume the plan is built in its phase order, starting with the handoff's queue, and some lane has to be reopened or reworked because of something the plan said or left out. **Name the three most likely causes**, most likely first. For each, give the item, the lane step where it surfaces, and the evidence that makes it likely: a file, a row id, or a command you ran. Unlikely causes don't count; this is a ranking of plausible ones.

### Phase 3: build-readiness walk

For each item scheduled in phase 1 of the Sequence (and B1, G and B2–B4 in the handoff's queue), play the first lane's builder or spine author at its first step. What would they have to ask, guess or discover before they could start? Then **verify every claim of compatibility with what exists**: wherever the plan says an existing mechanism "stays", "holds", "is kept", "becomes" something, or "needs no change", open the code or the row and check. Revision 30's findings were all of this kind (the watermark's hand-raise rule, `--bump-ids` taking no count, the act ledger's file-order rule, a stale branch ref), so expect more where no review has looked yet. Report only what would cost rework; a question a builder answers in a minute from the code is not a finding.

### Phase 4: ordering across items

The handoff's queue (B1, G, B2–B4, then WI-798, then leg 03's queue) was written at revision 13, before items 14–16 existed. Check it against the plan's phase 1 as it now stands: does any queued row depend on something scheduled later, do two rows edit the same surface in an order that forces one to redo the other, and is anything in phase 1 missing from the queue that a queued row needs? Check the dependencies the plan states (item 13 after item 6; item 16 after item 15; item 14 before the FileBackup re-sync and before item 5's migration; item 10 before the FileBackup re-sync; WI-897 last) against each other and against the queue. Then briefly: do the Status, the summary table, phase 0 and `docs/status.md` agree?

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [phase 1|2|3|4] <file:line or section> -> what is wrong (claim checked / evidence found) -> rework it would cause -> the concrete change

Then, under **"Pre-mortem"**, your three ranked causes, one short grounded paragraph each (each may also appear as a finding above).

Then, under **"Views for the owner"**, one short grounded paragraph each on:
- item 16 as now ruled;
- the handoff's queue against the plan's phase 1;
- anything else the owner should weigh before the build.

Then a short paragraph naming what you verified and found correct, including the compatibility claims you checked that hold.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
