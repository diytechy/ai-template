# Queue drill hand-off (2026-11-21, wave A landed)

For the coordinator session that works the queue next, and for the operator.
Read this file first; it is the resume point. The longer history is
`docs/plans/2026-11-11-test-tiers/HANDOFF.md` §12.6, and nothing there needs
reading before starting.

**Where the drill stands.** Waves A and B are merged. Variant F is filed
(WI-1021 to WI-1030) and critiqued by Sol and Argon, with every finding
applied. The drill is stopped at §3.3 N6: the operator sees F's cut (§3.4)
before any F builder starts. The suite after wave B runs during the stop.

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
- Wave B: WI-1019 merged (`da78f85ee`, regen `d19ab3efe`). Its worktree and
  branch are removed. No worktree is open for this drill; no branch or
  snapshot is pending.
- Acts owed, all to automated adjudication (§3.3 N4): wave A's three chains
  (§3.1 Q5) and LLR-395's first acceptance (SR-157's chain). WI-1038 then
  re-points TC-428 and TC-429, which drift.
- The operator still owes, outside this drill: the OI-79 remote-ref delete
  and the push.

## 2. The queue

| Item | What | Wave | Notes |
|---|---|---|---|
| WI-1038 | TC-428 and TC-429 verify LLR-395 once accepted | After LLR-395's acceptance | Filed from WI-1019's build; claimable only once adjudication accepts LLR-395 |
| WI-1021 to WI-1030 | Variant F's rows (F-1 to F-10, §3.3 N6, §3.4) | F, after the N6 stop | Filed and critiqued (round 1, Sol and Argon, all findings applied, `a57782d59`). Order by `needs`: 1021; 1022; 1023; then 1024 and 1027 (either order); 1025; then 1026, 1028 and 1030; then 1029. Built side by side where `needs` allows, landing one at a time (plan revision 37) |
| WI-1016 | A repository can switch off the implementation layer | After F | Re-critiqued once F lands; reverses SR-186, so its amendment is drafted for the operator |
| WI-1018 | Row text a lane leaves stale is filed, and the first set is brought up to the code | After F-8 | F-8's text migration takes B1, B7 and B9 and likely more; this row then fixes what is left |
| WI-1037 | The skill names roles, not models | Beside F-1 (§3.4 S3) | Built; review round 1: Argon APPROVE, Sol one MINOR (model labels lost on four observations), being fixed |
| WI-1040 to WI-1043 | WI-1036's findings: the last-act date and the test-first order read from the act ledger, an unanchored risk said so, two dead history helpers removed | Filed, not drilled | Owe a scope critique; WI-1041 amends LLR-239, WI-1042 amends LLR-257 |
| WI-1039 | The smoke tier back under its CPU budget | Beside F-1 | Filed 2026-11-21 (§3.4, the suite during F); owes its critique |
| WI-1031 to WI-1035 | The rest of phase 3 | Filed, not drilled | Owe a scope critique when they come up (§3.3 N2); WI-1035 carries §3.4 S4's answer |

Done in wave A: WI-1013, WI-1014 and WI-1017; in wave B: WI-1019; beside
F-1: WI-1036 (§10).
Closed by §3.3:
WI-1015 restructured into F's rows (N1), WI-1020 cancelled (N5).

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

**Answer:** Option (a), focus on transition to F first.

**Q2. If (b): how the overlap closes (item 2).**
- Re-tag: each of the 32 modules gets one component, by editing LLR
  `component` cells. Most are `Accepted`, so they drift and owe your
  re-accept; the choices carry into F's `Component:` headers later.
- Overlap as a crossing: the check treats a multi-component module's edges
  as crossings. No accepted row changes, but up to 63 edges each need a
  `call` row or a showing that they sit inside one component.

*Recommendation: re-tag.* F has already ruled one component per file, and
re-tagging answers the question F's migration will ask.

**Answer:** Not applicable, option (Q1(a) was selected)

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

**Answer:** What are the questions here?

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

**Answer:** Confirm

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

**Answer:** Leave all three to adjudication, for reference I have spot checked SR-233 and the spirit of the requirement is acceptable.

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

**Answer:** This probably needs more discussion.  The targetting LLM to run prose through and spine authoring would just be configurable, I wouldn't expect a skill to be touched.

**Q7. Argon.** Gemini Argon timed out at 900 seconds on every run of this
sitting that got as far as reviewing: the scope critiques of WI-1013 and
WI-1014, and the WI-1013 branch review. It had stalled twice the same way on
this hand-off's own review. The coordinator then stopped trying it, so every
wave-A critique and review was Sol alone. Keep trying it once per
item (a timeout costs 15 minutes, in the background), or drop it from the
drill until opencode-go works?

**Answer:** Instead of passing via std-in (my interpretation), can we save it to a file and just ask opencode-go argon to reference that file as a prompt?  Would that help?

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

### 3.3 The second round, raised by Q1(a) (answered 2026-11-21)

The coordinator's clarifications: Q3 lapses under (a) (WI-1015 is re-cut
onto F, and F's rows get their own critiques). Q6's row changes the method
of one recipe line, not the model; the model is already a roster setting
(`codex_call.py AUTHOR` reads `OPENAI-TERRA`, `--route` picks another), but
the coordinator-cycle skill names "Terra" where it means the author role.
Q7: the prompts went in as one command-line argument, not stdin; a prompt
file read by reference was never tried, and works (§6).

- **N1. WI-1015 under (a).** Items 3 to 5 retire with F's cells, item 2
  dissolves with the `Component:` headers, item 6 is F's every-IF-reached
  rule and item 1 belongs with F's `call`-row work. *Answer:* fold items 1
  and 6 into those F rows; WI-1015 is restructured into them.
- **N2. F only, or all of phase 3?** *Answer (operator):* "There is no reason
  the resync needs to be in a single entry. You can focus on building F only,
  but do the other items still have work items in the queue so they aren't
  lost?" They had none: item 10 steps 3 to 6, item 4's `[review]` section
  and item 2's history-reader audit are filed as WI-1031 to WI-1036, not
  drilled. The authority vocabulary's renames are not filed: the 2026-11
  vocabulary work already renamed those settings (`operator_accepts_through`,
  `push = "operator"`), superseding the plan's spelling. F ships its own
  RESYNC entry.
- **N3. One component per file.** 34 files have LLRs tagged in more than one
  component today. *Answer (operator):* "I would still expect a file is
  generally ascribed to a single component except for cases like reuse /
  configuration." The nuance: the overlap comes from tagging each LLR, not
  the file; most files have a clear majority (`trace.py` 25 to 1), and under
  F a minority LLR is placed through the interface it constrains. Reuse
  keeps one owner: a shared-kernel file (`docs/kernel-modules-allow`) is
  owned by CMP-006 and imported across components without a seam.
  Configuration keeps one owner: other components read it through a `file`
  interface. The real calls are the near-even splits (`check.py`,
  `acceptance_record.py`, and five files at 1 to 1); a file doing two
  components' work is evidence about the partition (OI-14), filed, not split
  inline. F-1 proposes the table, review checks it, and the operator rules
  before F-1 merges.
- **N4. The acts F creates.** *Answer:* as recommended: the batch act
  ("trace cells removed, requirement text unchanged") is the operator's
  ruling, recorded once; every other act goes to adjudication, and the drill
  lists what is owed. A sitting after F-8's text migration.
- **N5. WI-1020.** *Answer:* cancel it; F-8 states its own amendment rule
  (it rewrites accepted text in place to remove code names, which the
  add-only recipe forbids); file a row for the skill to name the author role,
  not a model (WI-1037).
- **N6. One stop after filing.** *Answer:* yes. F's rows are filed and
  critiqued on trunk, then the drill stops for the operator to see the cut.
- **N7. WI-1018 after F-8, WI-1016 after F.** Left blank; the recommendation
  stands.

### 3.4 The F stop (N6): the cut, for the operator (answer in place)

Each row's spec is in `docs/work/queued/`, and its critique with the
coordinator's dispositions is in `docs/reviews/2026-11-21-scope-critiques/`.

| Row | What | Needs |
|---|---|---|
| WI-1021 (F-1) | `Component:` headers; membership read from them; the one-component table held for the operator's ruling before merge (N3) | — |
| WI-1022 (F-2) | Interface owner and sides become component ids or `external:` parties; one body per interface; the cover rule on components (WI-1015 item 1); `call` rows classified, internal ones retired | 1021 |
| WI-1023 (F-3) | LLR `module`, `code_symbol` and `component` removed; undeclared keys refused; the `Implements:` index; derived placement; SR-180's chain retired with successors; the migrator; the batch act held for the operator (N4) | 1021, 1022 |
| WI-1024 (F-4) | `constrains`, `dimensions` and `out_of_domain` cells; every interface reaches an executable test (WI-1015 item 6); OI-43's check retired | 1023 |
| WI-1027 (F-7) | The parent-LLR link and one tree walk for every SR-to-LLR reader | 1023 |
| WI-1025 (F-5) | One home per contract: the effective-contract reader, the hand-over check, bodies cut to their form | 1024 |
| WI-1026 (F-6) | `Consumes:` and `Requests:` tags in code; sides hand over side by side | 1025 |
| WI-1028 (F-8) | No code in requirement text: the commit check, the `boundary` class, rows rewritten in place (WI-1018's cases) | 1023, 1025 |
| WI-1030 (F-10) | Item 12's builds: checks A and C, `run.cmd audit`'s `arch` and `hats` parts | 1021, 1024, 1025 |
| WI-1029 (F-9) | The build brief's derived component context | 1024, 1025, 1027 |

**S1. Approve the cut and its order?** *Recommendation:* approve. F lands
one row at a time; F-1 starts alone, since every other row needs it.

**Answer:** Approve

**S2. WI-1023 mints one SR.** The plan retires SR-180's chain and states its
discharge rule again under new ids, so F-3 needs one SR beside its LLRs and
TCs, against §8's "no SR expected". *Recommendation:* allow one SR in
WI-1023's range.

**Answer:** Yes that's fine

**S3. Work beside F-1.** Only WI-1021 can build at first. WI-1036 (audit
the scripts that read git history; research, no code) and WI-1037 (the
skill names roles, not models; text) share no file with F-1. *Recommendation:*
critique both and build them beside F-1.

**Answer:** Yes that's fine

**S4. WI-1035's two questions, for when it comes up (not blocking).** This
repo has `review_rounds = 1` while the coordinator runs two reviewers; the
draft keeps 1 as `full_reviewers` and leaves a change to you. And WI-802, a
draft row, also proposes a `[review]` section for a different purpose; the
spec says whichever lands second renames.

**Answer:** I don't have a strong opinion on either of the questions implied here, is there any historical evidence pushing one way or the other?

*The coordinator's finding (2026-11-21), applied to WI-1035:* the history
settles both. (a) The operator ruled `full_reviewers = 2` (review-churn
plan, item 4, confirmed in revision 35), and this drill already runs two
reviewers; `review_rounds = 1` predates that ruling and only the managed
loop reads it. This repo takes 2; an adopter keeps its own value. (b) WI-802
configures its session family under `[sessions.review]`, a different table
from `[review]`, so no rename is owed.

**The suite during F (operator, 2026-11-21).** The operator asked why the
suite runs so long at each landing; it runs once per batch (the 2026-11-19
option 3), measured 26 to 35 minutes, while the per-commit bar is the smoke
tier. Agreed for F: each landing runs the smoke tier on the merged trunk;
the unfiltered suite runs after WI-1023 (F-3, the widest change) and when F
closes, or sooner when a smoke red points wider. The smoke tier has grown
past its CPU budget (WI-1019's run: 1,014.6 CPU seconds against 540; 351 s
wall against about 55 s when stamped), so a re-tier row is filed: WI-1039.

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
6. **After each wave:** the unfiltered suite (during F, only at the
   checkpoints §3.4 names; each other landing runs the smoke tier,
   `.venv/Scripts/python.exe project-trajectory/scripts/run_menu.py smoke`,
   on the merged trunk), fixes for anything red, a
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
- **Argon (prose), by file reference (operator's idea, 2026-11-21):** write
  one self-contained bundle into `<scratch>`: a first line saying it cannot
  read the repository and must make no tool call but reading this file, then
  the brief, the spec, its specref and the registry rows it names, or the
  diff. Run from `<scratch>`:
  `timeout 900 opencode run -m opencode-go/gemini-4-argon --variant low -- "Read the file bundle-NNNN.md in the current directory and carry out the review it contains. It is self-contained: make no tool call other than reading that one file. Give your verdict as your final message."`.
  WI-1019's scope critique (a 23 KB bundle) returned in 37 seconds. No
  31,000-character cap applies: only the one-line prompt is on the command
  line. Argon run from `<scratch>` cannot read the repository (opencode
  refuses each outside read), and briefs that told it to may be what stalled
  the earlier runs. Never attach with `-f`: it has stalled for 20 minutes.
  One opencode run at a time: two at once fail with "database is locked".
  **If Argon times out, skip it** (operator, 2026-11-21); note in the review
  record that Sol reviewed alone, and do not retry it in a loop.
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
   measured 26 to 35 minutes, on a clean trunk. Run it in the background. Until it
   finishes, make no trunk commit, merge or regeneration and create no
   worktree; builders already in their D: worktrees keep working. Record the
   commit it ran on and its summary line in §10. Fix or triage every failure
   before the next wave starts; the baseline run's failures are fixed before
   wave A.

## 8. Ids for wave B

Marks at hand-off (`docs/id-watermark`): SR 247, LLR 394, TC 456, IF 325,
DA 28, SUR 4, CMP 9, WI 1020. Wave A minted LLR-393, LLR-394, TC-455, TC-456
and IF-325 (WI-1014); the rest of its ranges went unused and are free.

WI ids filed on trunk by §3.3: WI-1021 to WI-1030 (F-1 to F-10),
WI-1031 to WI-1037 (the rest of phase 3, and the author-role row) and
WI-1038 (WI-1019's follow-up). F-3 (WI-1023) mints a successor SR for
SR-180's discharge rule, so its launch range includes one SR.

| Branch | LLR | TC | IF |
|---|---|---|---|
| WI-1019 | 395 | 457–458 | none |
| WI-1021 (F-1) | 396–400 | 457–464 | 326–328 |
| WI-1036, WI-1037 | none | none | none |

WI-1019 used LLR-395 only; its TC range went unused and passes to WI-1021.
The other F rows' ranges are set as each launches; WI-1023's includes one
SR (§3.4 S2). No other SR, DA or SUR is expected; a builder that needs one
stops and asks.

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
- 2026-11-21: the operator answered §3.1 (Q1 (a): F first) and the second
  round it raised (§3.3). Argon by file reference tested: a trivial prompt in
  11 s, a 26 KB file in 18 s, WI-1019's scope critique in 37 s
  (CHANGES-REQUESTED, two findings). §2, §6 and §8 updated to match.
  `9b8ad0e04`.
- 2026-11-21: WI-1019's critique by Sol and Argon recorded and applied (the
  critics split; the coordinator took Argon's new row over amending
  LLR-366), `d849667f1`. Its builder stopped at the parent-first rule (an
  accepted TC may not verify a drafted LLR); ruled: land LLR-395 and its code
  tag, file the re-point as WI-1038.
- 2026-11-21: filed WI-1021 to WI-1038 (F-1 to F-10 drafted by one session,
  the rest by another, both into the scratchpad first); WI-1015
  restructured into WI-1022 and WI-1024; WI-1020 cancelled; WI-1016 now
  needs WI-1021 and WI-1023, WI-1018 needs WI-1028. `41a2daeeb` (the first
  try was refused: a restructured row's Deliverable is one fixed line, and
  its successors name it in `supersedes`).
- 2026-11-21: F's scope critiques, round 1. Sol: two APPROVE, 14 findings
  over eight rows. Argon by file reference: ten CHANGES-REQUESTED, 35
  findings, every run 41 to 113 seconds. 49 distinct findings: 47 adopted,
  2 in part, none rejected, no split. `a57782d59`.
- 2026-11-21: WI-1019 built (`maint/wi-1019`): LLR-395 and its code tag, a
  RESYNC entry for the tagged shipped file; smoke `3698 passed, 3 skipped`.
  Review round 1: Sol and Argon both APPROVE, no findings (an Argon run
  started from the repository root by a coordinator slip was stopped before
  it wrote anything, and rerun from the scratchpad). Merged `da78f85ee`,
  regen `d19ab3efe`; worktree and branch removed. Stopped at §3.4 for the
  operator; the suite after wave B runs during the stop.
- 2026-11-21: the operator answered §3.4 (S1 approve, S2 one SR for
  WI-1023, S3 WI-1036 and WI-1037 beside F-1; S4 settled from the history)
  and agreed the suite schedule for F; WI-1039 filed for the smoke tier's
  budget breach. Suite after wave B on `224ff2c68`: `8264 passed, 31
  skipped` in 32:59, no failure. WI-1036 and WI-1037 critiqued (Sol
  approved both; Argon approved WI-1037 and raised two findings on WI-1036,
  both applied).
- 2026-11-21: F-1 (WI-1021), WI-1036 and WI-1037 building in D: worktrees.
  WI-1039 critiqued by Sol alone (two findings, applied; Argon timed out),
  `d1c56e986`. WI-1036 built (69 history calls in 25 files, 4 recompute a
  past decision); review: Sol APPROVE, Argon timed out inside opencode's
  start-up (its log stops at `init`, before any model call); merged
  `a0ca15d3f`. Its findings filed as WI-1040 to WI-1043; the coordinator
  ruled the two `check_test_first` calls one row and the two re-run checks
  class (b).
