# Queue drill hand-off (2026-11-21, wave A landed)

For the coordinator session that works the queue next, and for the operator.
Read this file first; it is the resume point. The longer history is
`docs/plans/2026-11-11-test-tiers/HANDOFF.md` §12.6, and nothing there needs
reading before starting.

**Where the drill stopped.** Wave A is built, reviewed and merged, and the
suite after it has run (§1). The drill stopped at §3's first stop: variant F
before WI-1015 builds. §3.1 holds the questions, each with a recommendation
and a blank for the operator's answer. A resuming session reads the answers,
applies them (§3.1 says what each answer sets in motion), and continues from
§4 with wave B.

**The job:** take each drillable work item through scope critique, build,
review and merge into `refactor_again`, running items in parallel worktrees
where they do not collide. Reviews: code by OpenAI Sol at low effort; prose
and documentation by Sol at low effort **and** Gemini Argon at low effort
(operator, 2026-11-21).

## 1. State at hand-off

- Trunk `refactor_again`, tree clean once this hand-off's own commit (the
  one after `361270a84`) lands. It is ahead of the remote; pushing is the
  operator's (`push = "operator"`).
- The baseline suite ran on `380764dd3`: `8255 passed, 31 skipped` in 34:56,
  no failure. Wave A merged: WI-1013 (`efafa872f`), WI-1014 (`2ea2fd150`)
  and WI-1017 (`fd3ece15d`), each followed by its regeneration; WI-1018 to
  WI-1020 were filed from WI-1017's evidence sample (`361270a84`). The suite
  after wave A ran on `361270a84`: `8264 passed, 31 skipped` in 26:12, no
  failure. The wave's worktrees and branches are removed.
- No worktree is open for this drill. No branch, act or snapshot is pending.
- The operator still owes, outside this drill: the OI-79 remote-ref delete
  and the push.

## 2. The queue

| Item | What | Wave | Notes |
|---|---|---|---|
| WI-1015 | The code is held to its interface and LLR rows | B | Critiqued (round 1, six findings, not yet dispositioned); waits on §3.1 Q1 to Q3; amends LLR-067 |
| WI-1016 | A repository can switch off the implementation layer | C | After WI-1015 (same checks); not yet critiqued, since its shape follows Q1; reverses SR-186, so its amendment is drafted for the operator |
| WI-1019 | An LLR states WI-1001's untagged-TC rule | B, beside WI-1015 | New from WI-1017's sample; not yet critiqued; touches LLR-366 or a new LLR under SR-157 and TC-428/429, no code |
| WI-1020 | The add-only amendment recipe names the re-cut | B, beside WI-1015 | New; one case behind it, so §3.1 Q6 asks whether to keep it; the coordinator-cycle recipe only |
| WI-1018 | Row text a lane leaves stale is filed, and the first set is brought up to the code | D, after WI-1015 | New; WI-1015 (or variant F) may clear B1, B7 and B9 of its set first |

Done in wave A: WI-1013, WI-1014 and WI-1017 (§10).

Not drillable: WI-827 (the operator's signature on SN-029's amendment),
WI-998 (waits for a decomposition round to supply its sample), WI-1012 (waits
on HomeHub's adoption), and the five Blocked rows the open items hold
(`docs/status.md` "Blocked").

**Why the waves.** WI-1015 and WI-1016 both rework `trace.py`, the
architecture checks and the interface registry, so they run one after the
other. WI-1019 (registry text) and WI-1020 (one recipe) share no file with
WI-1015 beyond the registries, where distinct rows merge, so they may run
beside it once critiqued. WI-1018 amends LLR text WI-1015 may clear, so it
waits. Wave A's merges showed the shared files: `RESYNC_PACK.md` (keep every
entry) and `byte-budget-guard`'s stamps (§9).

## 3. Stop and ask the operator

### 3.1 The questions this stop holds (answer in place)

Write each answer after its **Answer:** line. A question left blank takes
its recommendation only where it says so.

**Q1. Variant F, before WI-1015 builds.** The review-churn plan's pointer
rules (`docs/plans/2026-10-11-review-churn/pointer-rules.md`; page
https://claude.ai/artifact/VYzwf3J1WYcFJpvZCjRdt5) are ruled in full and not
built: LLRs lose `module`, `code_symbol` and their component cell, an
interface's owner becomes a component id, code files declare `Component:`,
consumers and requestors hand over to role-typed citations in code, and an
interface's test coverage comes through the LLR or SR that `constrains` it
(OI-43's direct IF→TC check stays until that link is populated). Its build
is the plan's phase 3, a multi-lane program (item 5's schema removal, item
11's migration, item 12's checks) with no rows filed.

WI-1015's critique (`docs/reviews/2026-11-21-scope-critiques/WI-1015.md`,
Sol, six MAJORs) asks for this choice first (its S5/S6 finding). Each
Done-when item against F:

| WI-1015 item | Under F |
|---|---|
| 1. A cross-component import is covered only by a `call` row owned by the imported module naming the importer as a requestor | The rule survives; its cells move (owner a component id, the requestor a citation in code), so F's migration rebinds the check |
| 2. Overlap: 32 modules in several components silence the rule on 63 edges | Dissolves: a `Component:` header gives each file one component |
| 3. Each declared requestor imports the owner | Retired as stated: requestors become role-typed citations in code, and F's hand-over checks a citation against the row, not that the citing file imports the owner. Holding imports to citations under F would be new work there |
| 4. Each `name(args)` in a `data` cell matches the owner's code | Retired as stated: F's call form is "typed, no symbol names", and F's hand-over compares the row's form with the code's `Contract IF-NNN:` body exactly, which replaces it |
| 5. Each LLR CodeSymbol resolves in its Module | Retired with the cells |
| 6. Each interface row is verified by a TC or names its covering parent in `verified_by` (125 uncovered) | Survives as a goal; F's `constrains` link replaces `verified_by` as the carrier |

- (a) File the phase-3 rows and build F first, then WI-1015 and WI-1016 on
  it. WI-1015's loopholes stay open until then.
- (b) Build WI-1015 narrowed to what survives F, items 1, 2 and 6, and drop
  items 3, 4 and 5; WI-1016 builds on today's shape. Item 4 is dropped by
  default, since F retires symbol-named forms; say "(b) with item 4" to
  keep a check on today's nine stale signatures until F lands.

*Recommendation: (b), without item 4.* The cover loophole is open today,
F's build has no rows yet, and items 1, 2 and 6 state rules F keeps, so only
their cell bindings move in F's migration.

**Answer:**

**Q2. If (b): how the overlap closes (item 2).**
- Re-tag: each of the 32 modules gets one component, by editing LLR
  `component` cells. Most are `Accepted`, so they drift and owe your
  re-accept; the choices carry into F's `Component:` headers later.
- Overlap as a crossing: the check treats a multi-component module's edges
  as crossings. No accepted row changes, but up to 63 edges each need a
  `call` row or a showing that they sit inside one component.

*Recommendation: re-tag.* F has already ruled one component per file, and
re-tagging answers the question F's migration will ask.

**Answer:**

**Q3. WI-1015's other findings.** The coordinator's proposed dispositions,
applied on resume unless overruled here:
- S1 (landable deliverables bundled): under (b), WI-1015 keeps the
  cross-component rule (items 1 and 2, and 4 if Q1 keeps it), cover first; item 6
  splits into its own row, filed on trunk, since it is independent, touches
  125 rows, and its carrier is the cell F replaces. Under (a), the rows
  follow F's.
- S2 (`## Trust` owed): rejected. The checks are trace findings over the
  registries and the code, warn-first then failing `--strict` like their
  siblings; no file gains authority over a hold, an act or a gate, and no
  sibling check carries a Trust section.
- S3 (no closed grammar for signatures and CodeSymbol cells): under (b)
  without item 4 it falls away with items 4 and 5. With item 4 kept, it is
  adopted: the plan names the accepted signature forms, and anything else is
  a finding (deny by default), bounded to rows a supported route writes.
  Under (a), F's typed forms carry their own grammar.
- S4: `planmode = "single"`.

**Answer:**

**Q4. WI-1013's reconciliation: confirm or overrule.** Review found that
PROCESS.md §6 and the `coordinator-cycle` skill still sent the conduct of a
run to the decisions record: dismissals, dispute rulings, failed
commit-check rounds, a same-family reviewer substitution. The coordinator
ruled it in scope, since no code reads those entries and no cited ruling
names the record as their carrier. Dismissals, re-grades, dispute rulings
and the convergence map now go in the commit message answering the review
(not the log fragment, which the convergence reviewer reads, so it would see
earlier verdicts); reviewer substitutions, failed commit-check rounds and a
lane keeping an older order go in the commits and the log fragment. A ruling
that selects a design no spine row states still goes in the record. To match, SR-233's acceptance criteria, LLR-311 and TC-332
lost the clause "and in the delegated-decisions record too, when the run
keeps one" (text only; all stay `Accepted` and drift). Overruling means
reverting those lines and the three amendments.

*Recommendation: confirm.*

**Answer:**

**Q5. The acts owed (none taken).** The drift and drafts wave A left,
`docs/ratify/CURRENT.md` (text committed before any act):
- SR-168: LLR-393, LLR-394, TC-455 and TC-456 `Drafted` (WI-1014), and
  IF-325 `Drafted`, off-spine;
- SR-225: LLR-283 and TC-293 amended (WI-1013);
- SR-233: SR-233, LLR-311 and TC-332 amended (WI-1013, Q4).

The dial (`operator_accepts_through`) releases all three chains to
automated adjudication, so the brief lists none under your own acts. SR-233
is an accepted SR whose acceptance criteria changed to follow your
2026-11-20 rule. Do you want to take SR-233's chain yourself, or leave all
three to an adjudication sitting?

**Answer:**

**Q6. WI-1020: keep or cancel?** The coordinator's recipe "Brief Terra to
amend an accepted row by addition" only ever appends text to an accepted
row, which guards against losing an obligation but makes rows grow. WI-1020
would have that recipe name PROCESS.md §5's re-cut (retire the row and mint
its replacements, under acceptance) as the alternative when the row no
longer fits the design, keeping addition for a row that still fits. One case
stands behind it, out of WI-1017's sample of 92 decisions entries and 136
review verdicts: a review finding (wi-977, 008 F6) that LLR-149 repeats a
sentence after add-only amendments.

*Recommendation: keep it at P4.* It changes one recipe's text, and §5 now
states the re-cut it would point at.

**Answer:**

**Q7. Argon.** Gemini Argon timed out at 900 seconds on every run of this
sitting that got as far as reviewing: the scope critiques of WI-1013 and
WI-1014, and the WI-1013 branch review. It had stalled twice the same way on
this hand-off's own review. The coordinator then stopped trying it, so every
wave-A critique and review was Sol alone. Keep trying it once per
item (a timeout costs 15 minutes, in the background), or drop it from the
drill until opencode-go works?

**Answer:**

### 3.2 Standing stop rules

- **Variant F, before WI-1015 builds:** §3.1 Q1.
- **Any acceptance.** New rows are `Drafted`; an amended `Accepted` row keeps
  its status and shows as drift. Never flip a status to `Accepted`, never run
  `intake.py snapshot`. At the end, list what owes an act (`docs/open-items.html`
  §2) for the operator. An amendment's text is committed before its act
  (the `text-then-act` hook check).
- **A finding that would reverse an operator ruling.** Rulings are in each
  spec's Context ("operator, 2026-11-2x"), HANDOFF §12.2 of the test-tiers
  plan, and the review-churn plan.
- **Anything irreversible or outward:** a push, deleting a ref, a release.

## 4. One work item, start to finish

Run the commands from the repository root with
`.venv/Scripts/python.exe` (the system Python is 3.8; the kit needs 3.11).
`<scratch>` is the session's scratchpad.

1. **Scope critique, on trunk, before any build.** Render the brief:
   `review_brief.py critique --wi WI-NNNN --rubric docs/rubrics/scope-critique.md --scratch <scratch> --out <scratch>/crit-NNNN.txt`.
   A scope critique judges prose, so both reviewers read it (§6). Save both
   verdicts, as returned, in `docs/reviews/2026-11-2X-scope-critiques/WI-NNNN.md`
   (the pattern of `docs/reviews/2026-11-19-scope-critiques/`). Apply the
   findings to the spec on trunk: settle open choices, add `planmode`, split
   where the critique shows independent deliverables (a split mints its new
   WI id on trunk; `trace.py --bump-ids`). Commit with hooks. Once a wave's
   critiques are all in, update §2's waves and §8's id ranges for any split
   rows on trunk before launching a builder.
2. **Build, in a worktree.**
   `git worktree add D:/ai-template-wt-wiNNNN -b maint/wi-NNNN refactor_again`.
   Worktrees go on D:, never under `C:\Projects` (VS Code's file watcher
   storms on bulk writes there), and never while a suite runs. The hook
   looks for `.venv/Scripts/python.exe` in the worktree and otherwise falls
   to the system 3.8 and refuses, so link trunk's venv in (it is ignored):
   `New-Item -ItemType Junction -Path D:\ai-template-wt-wiNNNN\.venv -Target C:\Projects\ai-template\.venv`.
   The builder is
   a fresh sub-agent given §5's rules, the spec path, its id ranges (§8) and
   the worktree path. With `planmode = "single"` it writes
   `docs/plans/WI-NNNN/plan.md` first.
3. **Close out on the branch, before the review,** so the review reads the
   closing prose too. The spec gets its `## Deliverable`, moves with
   `spec_move.py --root . docs/work/queued/WI-NNNN-<slug>.md docs/archive/work/complete/WI-NNNN-<slug>.md`,
   and the log fragment `docs/log.d/WI-NNNN-<slug>.md` opens with `## `.
4. **Review the branch** (the coordinator, never the builder).
   `review_brief.py review` refuses a maintenance branch, since it wants a
   lane claim under `docs/work/active/<branch>/`, so wave A built the brief
   by hand: a preamble (the reviewer's identity, read-only, answer from the
   diff, about 15 tool calls; for Sol the repository path and `git show
   <tip>:<path>`), the checks the kit's reviewer brief asks for (Done-when
   coverage, correctness confirmed by reading, failure classes and
   red-before tests, requirement rows against K1 to K3, one home per rule,
   the closing prose true to the diff, severity by reachability, one line
   per finding and the `VERDICT:` line), `docs/rubrics/kit-change-review.md`,
   the spec at the tip, and `git diff <merge-base> <tip>` with the generated
   files of §7.2 excluded. A narrow round prepends the round's findings and
   the coordinator's rulings to the same brief over the fix range. Code changes (scripts, tests) go to Sol. Prose and documentation changes
   (docs, skills, prompts, templates, registry text, RESYNC entries) go to Sol
   and Argon. A branch with both: Sol reads the whole diff, Argon the prose
   part. Fix findings on the branch, then record the reviewers, findings and
   fixes in the Deliverable and the log fragment. That record needs no
   further review; any other change made after the review gets a narrow
   re-review (`--scope narrow --findings <round file>`) before the merge.
5. **Merge** (§7), one branch at a time, never while the suite runs.
6. **After each wave:** the unfiltered suite, fixes for anything red, a
   progress line in §10, and the merged worktrees removed. Unlink the venv
   junction first, `cmd /c rmdir D:\ai-template-wt-wiNNNN\.venv` (that
   removes the link only), or the recursive delete can follow it into
   trunk's venv; then `git worktree remove D:/ai-template-wt-wiNNNN` and
   `git branch -d maint/wi-NNNN`.

## 5. Builder rules (paste into each builder's brief)

1. Work only in your worktree, on `maint/wi-NNNN`. Never touch trunk or
   another worktree. Never push. Commit with hooks on; never `--no-verify`.
2. Read your spec and its `specref`, `CLAUDE.md` and the `session-protocol`
   skill. Build test-first: a failing test, then the code.
3. Mint ids only from the ranges in your brief, then run `trace.py --bump-ids`
   on your branch so no live id sits above its mark. Never use `--reserve-ids`.
   Need an id outside your ranges: stop and ask.
4. New spine rows are `Drafted`. Amending an `Accepted` row changes its text
   only. Never flip a status to `Accepted`, never run `intake.py snapshot`.
5. Run every test module that imports a module you changed (grep the
   importers; `trace.py --tests-for <module>` lists the spine-linked ones),
   not just the tests you edited, plus the whole-tree tests your change can
   reach (`test_import_layers`, `test_module_size_ratchet`, `test_dogfood_sync`).
   Quote the real summary lines.
6. Before a commit that changes what a generated view reads, run
   `trunk_step.py --root . --regen` so the hook's freshness steps pass.
7. A work-item title stays under 120 characters; a spec filename stem under 38.
8. Write scripts and multi-line files with the Write tool; Bash heredocs
   mangle tabs and CRLF.
9. If `$PYTEST_DEBUG_TEMPROOT` is set in your shell, run pytest under
   `env -u PYTEST_DEBUG_TEMPROOT`.
10. Never read `OPERATOR_SCRATCHPAD.md`.
11. Record a design call in `docs/decisions/maint-wi-NNNN.toml`
    (`project-trajectory/decisions.template.toml`) only when no spine row
    states what you chose and it is not about conducting the run: a reading
    of scope, or a design choice no LLR or interface states (the operator's
    rule behind WI-1013). Most branches need few or none.
12. Stop and report, rather than guess, when a call is the operator's, when
    the spec leaves something unsettled, or when a red is outside your scope.
13. End with: your commits, the tests you ran and their summaries, and
    anything left.

## 6. Reviewers

- **Sol (code, and prose alongside Argon):** from `<scratch>`, not the repo:
  `codex exec -c model_reasoning_effort=low --model gpt-6.1-sol --skip-git-repo-check -o <scratch>/sol-NNNN.md - < <scratch>/rev-NNNN.txt`.
  Several Sol runs may go at once.
- **Argon (prose):** from `<scratch>`:
  `timeout 900 opencode run -m opencode-go/gemini-4-argon --variant low -- "$(cat <scratch>/part.txt)"`.
  Put the text inline, under about 31,000 characters (split a longer diff
  into parts): Windows' 32,767-character command line refuses a longer
  argument at once ("Argument list too long"). Argon run from `<scratch>`
  cannot read the repository (opencode refuses each outside read and returns
  nothing), so inline the spec, its specref and the registry rows too. Never
  attach with `-f`: it has stalled for 20 minutes. One opencode run at a
  time: two at once fail with "database is locked". **If Argon times out,
  skip it** (operator, 2026-11-21): it stalled twice on this hand-off's own
  review, inline, at 13 KB. Note in the review record that Sol reviewed
  alone; do not retry it in a loop.
- Tell each reviewer to answer from the brief and diff, and to cap its tool
  calls; a reviewer handed the whole repository reads for half an hour.

## 7. Merging and the suite

1. On trunk with a clean tree: `git merge --no-ff --no-commit maint/wi-NNNN`.
2. Conflicts: in a registry, rows with distinct new ids are all kept; an
   existing row both sides edited is reconciled cell by cell, keeping its
   status, and two edits that disagree in meaning go to the operator.
   `docs/id-watermark` takes theirs, then `trace.py --bump-ids`. A generated
   file (`PROJECT_STATE.html`, `docs/open-items.html`, `docs/status.md`'s
   generated block, `docs/stage`, `docs/ratify/CURRENT.md`,
   `docs/interface-reference.md`, `docs/cli-reference.md`,
   `docs/requirements/components.derived.toml`) takes trunk's.
3. Whether or not anything conflicted, run `trunk_step.py --root . --regen`,
   then commit with hooks: `Merge maint/wi-NNNN: <what it delivers> (WI-NNNN)`.
4. Then regenerate once more, since the views stamp the merge commit, and
   commit `regen: the generated views over the WI-NNNN merge` if anything
   moved. The same holds after any act commit.
5. A commit runs the hook's 29 steps and takes 2 to 3 minutes. One past 10
   minutes is stalled: look for a process waiting on input.
6. The unfiltered suite:
   `env -u PYTEST_DEBUG_TEMPROOT .venv/Scripts/python.exe -m pytest -q -n auto`,
   35 to 60 minutes, on a clean trunk. Run it in the background. Until it
   finishes, make no trunk commit, merge or regeneration and create no
   worktree; builders already in their D: worktrees keep working. Record the
   commit it ran on and its summary line in §10. Fix or triage every failure
   before the next wave starts; the baseline run's failures are fixed before
   wave A.

## 8. Ids for wave B

Marks at hand-off (`docs/id-watermark`): SR 247, LLR 394, TC 456, IF 325,
DA 28, SUR 4, CMP 9, WI 1020. Wave A minted LLR-393, LLR-394, TC-455, TC-456
and IF-325 (WI-1014); the rest of its ranges went unused and are free.

If WI-1019 or WI-1020 runs beside WI-1015, each branch mints only from its
own ranges; proposed:

| Branch | LLR | TC | IF |
|---|---|---|---|
| WI-1015 | 395–399 | 457–464 | 326–330 |
| WI-1019 | 400 | 465–466 | none |
| WI-1020 | none | none | none |

A row split from WI-1015 on trunk (§3.1 Q3) takes the next WI and its
ranges are set when it is filed. No SR, DA or SUR is expected; a builder
that needs one stops and asks. Wave C runs alone and mints from trunk's
marks at its start.

## 9. Gotchas

- `docs/status.md`'s hand-written prose must name no retired stage tag and no
  work-item id a later claim needs (`integrate._status_prose_refusal`); point
  at files instead.
- An accepted row's amendment lands in a commit before its act, never in the
  same one (`text-then-act`).
- After an act commit or a merge commit, regenerate before the next commit.
- `check_trajectory` warns, harmlessly, that a CMP-008 knowledge pack is never
  cited by a new spec; it warns hard on a title over 120 characters.
- A sub-agent's list of tests can miss whole-tree tests; check them yourself
  before merging.
- Claims through the kit's lanes refuse without a coordinator lease; this
  drill uses maintenance branches merged by hand, as the last three batches did.
- Two branches that each re-stamp a watched document's size in
  `byte-budget-guard` (three byte-equal copies: `project-trajectory/skills/`,
  `.claude/skills/`, `.agents/skills/`) conflict at the merge. Stamp the
  merged file's real size, note each branch's delta, and re-measure the
  skill's own row, which counts its own bytes (wave A: PROCESS.md 101,623).
- The generated views stamp the commit they were made at, so after any
  commit they read one commit behind. That is the steady state: regenerate
  and commit after a merge or an act, not after every commit.
- A builder's close-out commit can draw the hook warning that its change
  set "touches neither test-cases nor tests/"; it reads only that commit.

## 10. Progress log

Append one line per step taken: the item, what happened, the commit.

- 2026-11-21: hand-off written; queue as in §2. Reviewed by Sol (low): five
  findings, all applied (regenerate on every merge, close out before the
  review, reconcile shared rows cell by cell, waves and ids for split rows,
  trunk frozen while the suite runs). Argon timed out twice and was skipped.
- 2026-11-21: baseline suite on `380764dd3`: `8255 passed, 31 skipped` in
  34:56; nothing to fix before wave A.
- 2026-11-21: scope critiques of WI-1013, 1014, 1015 and 1017, round 1, by
  Sol (low) alone (Argon timed out on the first two; its runs on the rest
  were stopped): all CHANGES-REQUESTED. Wave A's dispositions adopted
  (`planmode = "single"` on all three; WI-1013's delta settles LLR-283, not
  SR-225; WI-1014 kept whole, map first; WI-1017's guidance lands whatever
  its sample finds). WI-1015's six wait on §3.1. `0d67302bd`. No confirming
  round, as in the last batches.
- 2026-11-21: WI-1013 built (`maint/wi-1013`). Review round 1 (Sol): a
  MAJOR (PROCESS.md §6 and the coordinator-cycle skill still routed conduct
  to the record; fixed in the row, §3.1 Q4) and a MINOR (TC-293's wording);
  round 2 narrow: APPROVE. Merged `efafa872f`, regen `8e25a9982`.
- 2026-11-21: WI-1014 built (`maint/wi-1014`). Review round 1 (Sol): two
  MINORs (the README's `coincident` alternative, TC-455 restating LLR-393),
  plus the README's interface-backing claim the builder noticed; round 2
  narrow: APPROVE. Merged `2ea2fd150` (RESYNC kept both entries), regen
  `c0fb22838`.
- 2026-11-21: WI-1017 built (`maint/wi-1017`); its sample found no
  behaviour bent to a row's text, but rows not re-cut when the design
  changed shape. Review round 1 (Sol): a MAJOR (the causes outside the
  guidance were named, not filed) and a MINOR (readers restating §5); round
  2 narrow: APPROVE. Merged `fd3ece15d` (byte-budget-guard's PROCESS.md
  stamp set to the merged size). WI-1018 to WI-1020 filed, views
  regenerated: `361270a84`.
- 2026-11-21: suite after wave A on `361270a84`: `8264 passed, 31 skipped` in 26:12, no failure. Wave A's
  worktrees and branches removed. Stopped at §3.1 for the operator. This
  hand-off reviewed by Sol (low) alone: five findings, all applied (F
  retires items 3 and 4 rather than moving them, item 4's default stated,
  Q6 made self-contained, Q4's destinations exact, §1's clean-tree claim
  qualified).
