<!-- The brief for the revision 22 review pair (GPT-6 Astra and Claude Fable 5.1, both at medium effort), run 2026-10-13 in place of the revision 20 pair in review-handoff-r20.md, which never ran. Render one copy per reviewer, replacing {TIP} with the reviewed commit, {WT} with that reviewer's detached worktree, {OUT} with its review file and {ROOT} with the review root. Neither reviewer sees the other's review. -->

# Independent review: the whole review-churn plan, revision 22

You are an INDEPENDENT reviewer, a different model and a fresh context from the plan's author. You did not write this. Assume the author was careful but wrong somewhere, and find where. Do not edit, create or commit any file in the repository or any worktree. Never read `OWNER_SCRATCHPAD.md`. Write only your review file, at `{OUT}`.

## Where things are

- **Repository (read-only):** `{WT}`, a detached worktree at commit `{TIP}`. It shares the main repository's refs, so `git -C {WT} show contract_split:<path>` works. Python 3.11+ with `tomllib`: the primary checkout's `.venv/bin/python`, by absolute path (the worktree has no `.venv` of its own). Scratch scripts may go in `{ROOT}/scratch/`.
- **What changed since the last review** (revision 19, reviewed at `39c1fcfd0` by GPT-6 Astra at high effort and Claude Fable 5.1 at medium): `git -C {WT} log --oneline 39c1fcfd0..{TIP} -- docs/plans docs/handoff-2026-10-11-attended-coordinator.md` and `git -C {WT} diff 39c1fcfd0..{TIP} -- docs/plans/2026-10-11-review-churn docs/handoff-2026-10-11-attended-coordinator.md`. Revision 20 dispositioned the revision 19 reviews and recorded the owner's answers; its own review pair never ran, so revision 20's changes are reviewed here for the first time. Revisions 21 and 22 added item 14.

## What is under review: the whole plan

`docs/plans/2026-10-11-review-churn/README.md`, revision 22, all of it. Read it whole before judging any part. Its state:

- **Items 1–10 are ruled.** The "Owner rulings, 2026-10-11" section governs where older item text differs. Challenge a ruling only where the plan's later text contradicts it, applies it wrongly, or where a later revision undermines it.
- **Item 11, variant F**, the owner's position, with these owner answers:
  - **Decision 1:** an IF's owner is a local component id or an `external:` party; the optional IF `component` cells that hold placement today are migrated; far-side bodies of external rows are checked against a local endpoint; one body per IF over a stated scan surface.
  - **Decision 2, as revised in revision 20:** an interface states only its form, and the LLR or SR that constrains it defines the behaviour with respect to that form, over its full dimensional scope. The IF `data` cell holds the whole form, with no one-line limit, until the build; then the code body opens with exactly that text. A `call` interface crossing a component boundary gets a typed form with no symbol names; one inside a component is optional. An SR gains the same optional `constrains` cell as an LLR, and a derived check requires every IF to reach an executable TC through such a link. The LLR's dimensions cell is the one home of an input space.
  - F-calls 1, 2, 8 and 9 are answered; F-calls 3 (per TC and LLR pair) to 7 remain open.
  - **Proposed:** a derived component context in the build brief, from the owner's question.
- **Item 12** (architectural decomposition). Open; decision 4 moved its architectural-delta question to the scope critique, with new anchors and inputs.
- **Item 13** (review only a green tip). Answered: the gate at the start of review; about three red rounds, then a partial close, now priced; TC rows before the build; the red-before proven by strict expected-failure marks (revision 20), not an evidence record; a scoped test set; an advisory mutation trial. **Decision 3:** `[policies] dependency_admission = "owner-or-delegate" | "independent"`. In revision 20 the owner settled that owner and delegate are one role, "owner-or-delegate", distinct from an autonomous run the kit's machinery starts; the plan proposes the vocabulary rewrite that follows, and asks which side the coordinator role is on.
- **Decision 4:** the plan comes after the claim, in the lane; the scope critique, before the claim, asks the questions that reshape the queue.
- **Item 14** (new in revisions 21–22, owner-directed, both calls answered). The owner's 2026-09-06 SN-036 ruling (perspective coverage is a recorded hat-by-hat review, not a machine-readable record plus a check) landed only on the unmerged `contract_split` branch, and this branch then built the withdrawn design (WI-688: `hats.py record`, LLR-297, TC-312, one sidecar file). Item 14 retires that build, applies the ruling's four row acts in `contract_split`'s wording, wires the hat questions into the coordinator's sitting and spine-author briefs, and deletes the existing sidecar. Background, for checking its claims: `docs/plans/2026-10-13-contract-split-divergence.md` §4 ("Group 3 since the split"), and the ruling's text in `git -C {WT} show contract_split:docs/log.md` (search "SN-036 / SR-161 owner ruling").
- **Companion files, for consistency:** `pointer-rules.md`, `docs/handoff-2026-10-11-attended-coordinator.md` ("For the owner"), `item-11-llr-fitness-report.md`, `item-11-value-domain-research.md`, and the divergence report above.
- **Earlier reviews and dispositions** are in `reviews/` and the plan's last sections, including `astra-high-r19.md` and `fable-medium-r19.md`. Don't repeat a dispositioned finding unless its fix is wrong or a later revision broke it.

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
- **The adjudicator's scope is the spine and behaviour**, not whether something may be installed.
- **Owner-or-delegate is one role.** A delegate is an LLM agent the human has explicitly permitted to act in their stead, with whatever permission the human granted; the kit cannot tell it from the owner and does not try. What the kit can tell is an autonomous run, which its machinery starts and marks.
- **A guard where construction suffices is ceremony** (the 2026-09-06 ruling item 14 applies): before proposing a record, cell or check, ask whether a review pass or a construction already does the job.

## Severity, as the owner calibrates it

- **Dismiss a finding that needs a compromised or contrived host, or a contrived, improbable scenario** (for example, a stub written to raise `AssertionError` so an assertion-free test "fails"). The plan does not design against those; at most, note one in a sentence under "Views", never as a finding.
- **BLOCKER** only where a ruling-dependent instruction is wrong or unsafe, an owner rule is broken, or a direction is wrong.
- **MAJOR** only where an inconsistency, contradiction or factual error would actually mislead the owner's ruling or the next session's build.
- **MINOR** for precision and wording; mark wording ambiguities `for clarity`.

Severity tracks plausibility and impact, not ingenuity. A plan at this stage needs findings that would change what gets built.

## What to do: two phases, in order

### Phase 1: challenge

Is each direction right? Judge, on the owner's lens: variant F as now answered (against E and anything better you can name); decision 2 as revised; the strict expected-failure marks; the owner-or-delegate role against the autonomous run; decision 4; item 12; item 13 as now shaped; the proposed component context; item 14. Ground every claim in a file, a row id or a command you ran. If a direction is wrong, say so plainly and say what should replace it.

### Phase 2: stress-test the whole plan

Find where it breaks down and where contradictions surface, across all fourteen items. Check at least:

- **The whole-form `data` cell and the hand-over:** registries with long form cells, artifact-class wording for `file` forms (no paths), the exact compare, and the approval snapshot.
- **The `call` classification and the typed form**, on real `call` rows that cross a component boundary.
- **The SR `constrains` cell and the derived executable-test check:** external-owned rows, shared crossings, the migration manifest, and keeping OI-43's check until the new link exists.
- **The strict expected-failure marks:** is the stack-neutral contract buildable, does the parent's tree-bound bar attestation really prove the red, and is the commit check static and light enough for ruling 6's commit-bar command?
- **Owner-or-delegate and the autonomous run:** the existing enforcers (`kitlib/provenance.py`'s marker, `check.py`'s `held-status` step, the merge slot), the vocabulary rewrite's renames and their adopter migration, and the coordinator-role question.
- **The scope critique's new anchors and inputs**, and the re-critique of queued rows as each is claimed.
- **The derived component context:** is it derivable from what the plan keeps, and does it avoid a third home?
- **Item 14:** do its row acts match the ruling and `contract_split`'s rows (`git -C {WT} diff 607cf609 contract_split -- docs/requirements docs/test`)? Is its retirement list complete (every live reference to `hats.py record`, `.perspectives.toml`, LLR-297 and TC-312)? Does the wiring keep one home for applicability? Is its sequencing against item 5 and the FileBackup re-sync right, and does it conflict with item 12's "hats don't fit" reasoning?
- **Internal consistency:** the README's summary table, item 11's status table, the F section and its table, items 12–14, the dispositions, `pointer-rules.md` and the coordinator handoff after revision 22; counts and citations.

Say which phase each finding comes from.

## Output

One line per finding, most severe first:

    - [BLOCKER|MAJOR|MINOR] [phase 1|phase 2] <file:line or section> -> what is wrong (claim checked / evidence found) -> the concrete change

Then, under **"Views for the owner"**, one short grounded paragraph each on:
- variant F as answered, and F-calls 3–7;
- decision 2 as revised, and the component context;
- decisions 3 and 4, and the owner-or-delegate role;
- items 12 and 13, including the strict marks;
- item 14.

Then a short paragraph naming what you verified and found correct.

End with exactly one line:

    VERDICT: SOUND|REVISE findings=N
