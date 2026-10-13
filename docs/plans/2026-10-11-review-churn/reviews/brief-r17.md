<!-- The brief both revision 17 reviewers receive, identical except that <WT> is each one's own detached worktree at 29a613d93 and <OUT> its own review file. They run one after the other (GPT-6 Astra at high effort, then Claude Fable 5.1 at medium), and neither sees the other's review. -->

# Independent review: the whole review-churn plan, revision 17

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at `<OUT>`.

## Where things are

- **Repository (read-only):** `<WT>`, a detached worktree at commit `29a613d93`. Python 3.11 with `tomllib`: `C:/Projects/ai-template/.venv/Scripts/python.exe`, or `python` on PATH. Scratch scripts may go in `C:/Projects/ai-template.wt/review-tmp/2026-10-13-churn-plan-r17/scratch/`.
- **What changed since the last review** (revision 15, reviewed at `7bfe0c06b` by GPT-6 Astra and Claude Fable 5.1 at medium effort): `git -C <WT> log --oneline 7bfe0c06b..29a613d93` and `git -C <WT> diff 7bfe0c06b..29a613d93 -- docs/plans/2026-10-11-review-churn docs/handoff-2026-10-11-attended-coordinator.md`. Revision 16 dispositioned those two reviews; revision 17 records the owner's answers from a 2026-10-13 session.

## What is under review: the whole plan

`docs/plans/2026-10-11-review-churn/README.md`, revision 17, all of it. Read it whole before judging any part. Its state:

- **Items 1–10 are ruled.** The "Owner rulings, 2026-10-11" section governs where older item text differs. Challenge a ruling only where the plan's later text contradicts it, applies it wrongly, or where a revision 16–17 change undermines it.
- **Item 11, variant F.** The owner's refinement of the analysts' variant E. In revision 17 the owner answered F-calls 1 (option (i): the IF's owner is the producing component's id), 2 (not every file is stubbed; the builder may mint files but must not duplicate), 8 (an LLR need not name an interface; its placement is derived through the interface its verifying test drives) and 9 (the contract's one home is the code body, held in the IF row's `data` cell until the build writes the body: "one home at a time"). F-calls 3–7 and several status-table rows remain open.
- **Item 12** (architectural decomposition at three moments). Open.
- **Item 13** (review only a green tip; tests reviewed in stages). In revision 17 the owner chose to gate the *start* of review, set a red-bar cap of about three rounds then the adjudicator, confirmed TC rows before the build with test code as the build's first deliverable, confirmed an advisory mutation trial, and scoped the gate's tests to those under the WI's SRs. Revision 17 also adds a **proposed** in-lane dependency policy (`[policies] dependency_admission = "human" | "independent"`, a new admission hat, an eight-step verification order, when it runs, and what a hand-back means under the existing partial close), for the owner to confirm.
- **Companion files, for consistency:** `pointer-rules.md`, `docs/handoff-2026-10-11-attended-coordinator.md` ("For the owner"), `item-11-llr-fitness-report.md`, `item-11-value-domain-research.md`.
- **Earlier reviews and dispositions** are in `reviews/` and the plan's last section, including `astra-medium-r15.md` and `fable-medium-r15.md`. Don't repeat a dispositioned finding unless its fix is wrong or revision 17 broke it.

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
- **The adjudicator's scope is the spine and behaviour** (owner, 2026-10-13), not whether something may be installed.

## What to do: two phases, in order

### Phase 1: challenge

Is each open direction right? Judge variant F as now answered (against E and anything better you can name), item 12, item 13 as now shaped, and the proposed dependency policy, on the owner's lens. Ground every claim in a file, a row id or a command you ran. If a direction is wrong, say so plainly and say what should replace it.

### Phase 2: stress-test the whole plan

Find where it breaks down and where contradictions surface, across all thirteen items, not only the revision 17 text. Check at least:

- **Revision 17's F answers against each other and the rulings.**
  - "One home at a time" (F-call 9): is it one home, or two with a hand-over? Does the commit check that decides the home exist or need building? Does the approval snapshot (`baseline_snapshot.py`) really catch a change made in the move? What happens to an external-owned IF, whose body is stated by the far-side module (`trajectory_arch.contract_body_findings`, shape (2))?
  - F-call 1 (i): the amendment of OI-67 (a)'s header text; the check "the file holding the body declares the owning component" before any file carries a `Component:` header; the 31 file- or directory-owned rows; whether making the optional IF `component` cell the owner changes its existing meaning.
  - F-call 8: placement derived through a TC's named interface; F-call 3's rule turned into a "must" for that case; the residues; multi-placement.
  - Ruling 5, OI-48, OI-67, OI-112 and the 2026-09-20 `realizes` rejection, as F now stands.
- **Item 13 as now shaped.** One tree-bound bar attestation shared by review dispatch and landing, without a second home for "green". The red cap's `on_limit = "adjudicate"` reuse of item 4's shape, and the adjudicator's scope rule. The red-before record bound to the parent's tree, and "the red must reach the test's assertion": is that checkable? The scoped test set derived from the spine (SR → LLR → TC → tagged test files), its dependence on tagging, and whether keeping the smoke tier contradicts the owner's "not all". The TC-first split against the coordinator cycle and item 9. Do the cited studies say what the plan says they say?
- **The dependency policy.** Does `dependency_admission` fit `[policies]` and the `push` precedent? Is "two places it can start" a second path under the no-fallback rule? A network-reading identity script in the kit's scripts against stdlib-preferred and cross-platform. The lane-local environment, given lanes run on the main checkout's `.venv`. The coupling to `decision_recording`. The hand-back: `handback.py`'s partial close, `adjudicate-disposition.template.md`'s `[open_item]` card, and whether the card's recommendation breaks the adjudicator's scope rule.
- **The dashboard stamp** from observation records, against byte-deterministic generation.
- **The rest of the plan.** Items 1–10's text against their rulings; the sequence and phases table; the session budget; the measures; whether revision 17's additions changed costs or ordering the "Sequence" section doesn't reflect.
- **Internal consistency.** Do the README's summary table, the item 11 status table, the F section and its table, item 13, `pointer-rules.md` and the coordinator handoff agree after revision 17? Are counts and citations right?

Say which phase each finding comes from.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [phase 1|phase 2] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

- BLOCKER: a ruling-dependent instruction is wrong or unsafe, breaks an owner rule, or a direction is wrong.
- MAJOR: an inconsistency, contradiction or factual error that would mislead the owner's ruling or the next session.
- MINOR: precision or wording. Mark wording ambiguities `for clarity`.

Then, under **"Views for the owner"**, one short grounded paragraph each on:
- the F-calls still open (3–7) and whether revision 17's answers to 1, 2, 8 and 9 hold;
- item 12;
- item 13 as now shaped;
- the proposed dependency policy.

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
