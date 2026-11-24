# Queue drill hand-off (2026-11-21, variant F building)

For the coordinator session that works the queue next, and for the operator.
Read this file first; it is the resume point. The longer history is
`docs/plans/2026-11-11-test-tiers/HANDOFF.md` §12.6, and nothing there needs
reading before starting.

**Where the drill stands.** Waves A and B are merged, and WI-1036 and
WI-1037 beside F-1. Variant F is filed (WI-1021 to WI-1030), critiqued, and
its cut approved (§3.4). F-1 (WI-1021), F-2 (WI-1022), F-3 (WI-1023) and
F-7 (WI-1027) are merged, and so are F-4's slices 1 to 3 (WI-1024), with
the rows beside them (WI-1045, WI-1070 to WI-1073 in the seventh session).
Nine adjudication sittings have run; the ninth (WI-1074) blessed 49 of 50
amendments and accepted all 10 new rows. Owed now: F-4's slice 3 (48 rows,
its sittings C1 and C2) and WI-1072's LLR-359 and TC-398. **Start at §0.**

## 0. Resume here (2026-11-24, end of the seventh session)

Trunk `refactor_again` is clean at this hand-off's commit. One drill
worktree is open, `D:/ai-template-wt-wi1024` (F-4, `maint/wi-1024` at
`a76ffcd3c`, clean, merged into trunk, nothing unmerged); no builder is
running. **First run `git log --oneline -3` and `git status --short` in it.**

1. **The tenth sitting.** File it first: every spine row owed on trunk.
   That is F-4's slice 3 (`docs/plans/WI-1024/slice-3.md` §5: C1, 23 rows,
   LLR-014 among them answering the ninth sitting; C2, 25 rows) and
   WI-1072's LLR-359 and TC-398 (amendments). All are amendments; no new
   `Drafted` row is owed but LLR-421, LLR-422, TC-531 and TC-532, held for
   slice 5. Dry compose the 50 tokens (`sit/mkspec.py`, then
   `sit/prepare_sit.py` with an existing WI id, see §9) and split into C1
   and C2 only if over about 400K characters; the ninth sitting's 60 rows
   came to 344K. Then as WI-1074 ran (§3.7): file with `--bump-ids`, bind,
   Neon high, write, record, act (test the first snapshot read-only, run
   `trace.py --strict` after any flips), close. WI-1072's composition check
   now refuses any brief carrying an identity line its composer did not
   write; a real dry compose passed it (`0de9125ad`).
2. **WI-1075** (IF-144's checker protocol, a census test): critiqued and
   its dispositions applied at this hand-off's commit (`planmode =
   "single"`, parent SR-006, the discovery rule and bound stated). Build
   it (plan first) before F-4's slice 5. Ranges at launch: LLR from 516, TC
   from 613.
3. **F-4's slice 4** (CMP-006's population, about 98 interfaces, likely two
   sittings D1 and D2): brief it from `brief-1024-s3.md`, fast-forwarding
   the branch to trunk first (`git -C D:/ai-template-wt-wi1024 merge
   --ff-only refactor_again`). Carry from slice 3's §6: LLR-288 may become
   IF-054's and IF-073's row; IF-271 to IF-275 stay reached through their
   naming cases (IF-274's unstated parse failure goes to LLR-300's next
   amendment; IF-272 and IF-273 wait for LLR-270's next amendment, IF-247
   and IF-248 stay on LLR-290); TC-301's repeated IF-264 is slice 5's.
   Then slice 5 (the strictness) once slice 4's sittings and WI-1075 land.
4. **The smoke tier's membership** is at 4,017 of `max-tests = 4060`
   (`docs/stack.ini`); slice 4 or WI-1075 may cross it. Re-stamp with the
   reason and about 4% headroom (§9), not current+1.
5. **Then:** WI-1039 on a quiet box; F-5 (WI-1025) after F-4 closes. Brief
   every builder from the scratchpad's briefs (`brief-1070.md` for a
   planned row, `brief-1024-s3.md` for a slice) or `common-rules.md`.
6. **For the operator:**
   - A push: trunk is ahead of the remote by 133 commits, from
     `80d64a5f3`.
   - Scratch folders to delete by hand: `D:/rt*` (`D:/rt1024`, `D:/rt1072`,
     `D:/rtm` among them) and `D:/review-tmp/2026-11-23-wi1060`,
     `D:/review-tmp/2026-11-24-wi1070`.

Not filed, noted for WI-1018's list or a later row:
- IF-231's notes still describe the reach as through the owner's design
  rows only.
- LLR-338's accepted Detail still says "APPROVE".
- The commit hook does not run `check_docs`.
- No standing report shows verdicts with waiting flips.
- A first-acceptance act does not check that the row's text is the text
  its verdict judged (§9).
- LLR-369 (the vocabulary migrator's design row) states one obligation per
  migrator step, a decomposition WI-1065 left out of scope; the eighth
  sitting blessed it as is, so re-cut it only if a later sitting returns it.
- A merge of trunk into a branch is refused by the staged mirror check
  when trunk took an act and the branch amends rows (§9).
- The commit hook let through a closed row with its `specref` still set
  (WI-1066, `86fde801e`) and two titles over 120 characters; only
  `check_trajectory --strict` reports them, so run it before each filing
  or closing commit.
- A first-acceptance act can arm a requirement-form finding the `Drafted`
  status exempted (LLR-484's "such as", `855b4388f`), and the commit hook
  does not run `trace.py --strict`, so trunk's smoke went red unseen. Run
  `trace.py --strict` after the flips, before the act's commit (§9).
- LLR-300 stays one row of several obligations (WI-1071's D8); re-cut it
  only if a sitting returns it.
- `acceptance_record.verdict_rulings` has no caller and keeps an edge into
  the verdict library that falsifies a sentence of CMP-006's accepted
  notes; `landing_rules.ARCHIVE_WORK_DIR` is unused (WI-1045's D10).
- TC-369's text lists its tests by name and does not mention slice 3's new
  fallback test (its evidence does); the lane's base is an abbreviated
  commit id in the no-merge-base fallback but a full one otherwise
  (slice 3's §6 item 16).
- `tests/test_migrate_vocabulary_record.py` has an unused import (ruff
  F401), outside the smoke lint.

Scratch tools, in the seventh session's scratchpad
(`C:/Users/Peter/AppData/Local/Temp/claude/9919beaa12ed540b/3f3a88bd-e950-46b6-8d3e-0f9f3ffb7f42/scratchpad`,
which may be cleared; it holds copies of the sixth session's tools too):
- `resolve.py <file> ours|theirs|both ...` resolves conflict hunks in
  order; `showhunks.py <file> [width]` prints them with long lines cut;
  `check3way.py <base> <ours> <theirs> <registry>...` checks a merged TOML
  registry cell by cell against both sides (run it on every registry merge).
- `build_review.py` builds the review briefs (`--part code|docs`,
  `--replace path=summary`, `--round N --findings`, `--checks`,
  `--keep-plan <path>`); `rows_accepted.py <repo> <rev> <bundle> ID...`
  appends each amended row's last accepted text to a Hydrogen bundle, and
  `rows_ifs.py` the interfaces the named design rows constrain. `checks-NNNN.md`
  are the per-row extra checks; `rev/findings-*.md` the round findings.
- `mkbundle.py` and `crit3/write_crit.py` build the critique bundles and
  records (`crit2/pre.txt` is Sol's launcher preamble).
- `common-rules.md` holds the row rules, the close-out and §5's builder
  rules; `brief-1070.md`, `brief-1071.md`, `brief-1045.md`,
  `brief-1073.md` and `brief-1024-s2.md`, `brief-1024-s3.md` are this
  session's build briefs.
- Under `sit/`: `scope.py` (drifted and Drafted rows; it lists accepted-cell
  drift only, so add link-only rows from the slice records), `mkspec.py
  <out> amendment:ID,... first-acceptance:ID,...`, `prepare_sit.py <spec>
  [--bind]` (a dry compose needs an existing WI id in the spec),
  `preface-1074-src.md`, `record_sit.py <spec> <verdict> write|record|act
  [ids]`, `flip.py`, `close_1074.py`, `deliverable-1074.md`.

Each is small enough to rebuild from §4, §6 and §3.7 if lost.

**The job:** take each drillable work item through scope critique, build,
review and merge into `refactor_again`, running items in parallel worktrees
where they do not collide. Reviews: code by OpenAI Sol at low effort; prose
and documentation by Sol at low effort **and** Gemini Hydrogen through the
Antigravity CLI (`agy`), which replaced Gemini Argon through opencode-go;
adjudication sittings by Gemini Neon through `agy` (operator, 2026-11-21;
§6).

## 1. State at hand-off

- Trunk `refactor_again` at this hand-off's latest commit (§10's last
  line), tree clean. It is ahead of the remote; pushing is the operator's
  (`push = "operator"`).
- Merged: wave A, WI-1013 (`efafa872f`), WI-1014 (`2ea2fd150`) and WI-1017
  (`fd3ece15d`); wave B, WI-1019 (`da78f85ee`); beside F-1, WI-1036
  (`a0ca15d3f`) and WI-1037 (`b62079378`); F-1, WI-1021 (`147fed185`, regen
  `ed671a026`); beside F-2, WI-1044 (`e17c677f9`), WI-1043 (`7371f0cf6`),
  WI-1041 (`8b50e28c1`), WI-1046 (`e29eb9d30`) and WI-1040 (`2a57861ec`);
  F-2, WI-1022 (`b2b0d9476`, regen `24656b1de`); after F-2, WI-1042
  (`abb00a88d`) and WI-1048 (`0f670626a`, regen `22a9a9369`); F-3, WI-1023
  (`4335c1a4d`, regen `d31ddce0c`); after F-3, WI-1050 (`9ce559b84`,
  regen `867d6361e`); WI-1038
  cancelled, superseded by WI-1048. On trunk, not merged branches: OI-79
  closed (`6eff30f85`); WI-1049, the second sitting (filed `d5cb62675`,
  verdict `7598caf5e`, revert `0333b64f0`, acts `4e3e28a2f` and
  `55e40f407`); WI-1047 cancelled, superseded by WI-1049; WI-1055, the
  third sitting (filed `982063eef`, verdict `0c5440672`, revert
  `7b342d8b9`, acts `b86518820` and `fe8db46b2`); WI-1050 to WI-1054 and
  WI-1056 filed. Open drill worktree: F-3's (§0). Suites:
  after wave A on `361270a84`, `8264 passed, 31 skipped`; after wave B on
  `224ff2c68`, `8264 passed, 31 skipped`; smoke after WI-1048 on
  `73aa095ce`, `3717 passed, 3 skipped`; after F-3 on `dc907c4c6`,
  `8282 passed, 31 skipped` (32:10). The next unfiltered suite runs when F
  closes (§3.4), or sooner when a smoke red points wider.
- Third session (2026-11-22 to 23): WI-1056 (`db6f47649`), WI-1051
  (`fb782bbc5`), WI-1052 (`4e2ad727a`), WI-1053 (`4cb091e79`) and WI-1054
  (`b486b1ea1`) merged. The smoke membership was re-stamped 3740 -> 3890
  (`ff5b15e4a`). WI-1057, the fourth sitting: filed `ca5a7d9dc`, verdict
  `c8d0a4453`, acts `e9f6362cc` and `072f93670`, closed `a6d447b76`. Smoke
  on trunk after WI-1056: `3749 passed, 3 skipped`. No drill worktree is
  open.
- Acts owed: none on the spine since the sixth sitting's act
  (`43f711b6d`). `docs/ratify/CURRENT.md` reads that no spine row differs
  from its recorded copy and none awaits a first acceptance. IF-312 and
  CMP-006 still drift in their off-spine registries, and IF-296 and IF-308
  are `Drafted` interface rows (no sitting has been shown an off-spine
  row).
- The operator pushed trunk through `80d64a5f3` (2026-11-23); later pushes
  stay the operator's. OI-79 is closed
  (operator, 2026-11-22): its remote-ref delete is done (`git ls-remote
  origin`: no `wi508-architectural-remap-HELD-for-owner-verdict` branch; the
  tag `wi508-record-2026-08-30` at `fa3c99c4` is there), and its row's
  `follow_up` cell records it.

## 2. The queue

| Item | What | Wave | Notes |
|---|---|---|---|
| Tenth sitting | F-4's slice 3 (C1, C2) and WI-1072's LLR-359, TC-398 | Next (§0 step 1) | 50 amendments; split only above about 400K |
| WI-1075 | IF-144's checker protocol: a census test, parent SR-006 | Critiqued, ready to build (§0 step 2) | Before F-4's slice 5 |
| WI-1024 slices 4 and 5 | CMP-006's population, then the strictness | Slice 4 may build (§0 step 3) | Slices 1 to 3 merged (`6ed2cfc28`, `88e589103`, `eb96d6298`) |
| WI-1045 | `acceptance_record.py`'s landing rules move to a CMP-008 module (F-1's table, §3.5 R2) | Merged `3bd545635` | Critiqued (Sol and Hydrogen, all findings applied): the order settled after F-3, the cover held to F-2's rule, IF-308's callers named |
| WI-1039 | The smoke tier back under its CPU budget | Beside F-1 | Filed 2026-11-21 (§3.4, the suite during F); critiqued by Sol alone, findings applied (`d1c56e986`); not built |
| WI-1031 to WI-1035 | The rest of phase 3 | Filed, not drilled | Owe a scope critique when they come up (§3.3 N2); WI-1035 carries §3.4 S4's answer |

Done in wave A: WI-1013, WI-1014 and WI-1017; in wave B: WI-1019; beside
F-1: WI-1036 and WI-1037; beside F-2: WI-1044, WI-1043, WI-1041, WI-1046
and WI-1040; after F-2: WI-1042 and WI-1048, and the second sitting
WI-1049; F-3 (WI-1023); after F-3: WI-1050 and the third sitting WI-1055; then WI-1056, WI-1051
to WI-1054 and the fourth sitting WI-1057; in the fourth session WI-1058,
WI-1059, WI-1062 and the sittings WI-1061 and WI-1063 (§10). In the sixth and seventh: WI-1064 to WI-1071 and the sittings WI-1066, WI-1068 and WI-1074. Cancelled: WI-1038, superseded by WI-1048's TC-475; WI-1047,
superseded by WI-1049.
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

### 3.5 F-1's one-component table, for the operator's ruling (§3.3 N3)

WI-1021 is built on `maint/wi-1021` (`fa057410d`) and waits for this ruling
before its review and merge. The table, with each file's LLR tags and the
reason for each pick: `docs/plans/WI-1021/component-table.md` on that
branch (`git show maint/wi-1021:docs/plans/WI-1021/component-table.md`).

**R1. The eight near-even files** (the leading component holds under two
thirds of the tags): `acceptance_record` CMP-006, `check` CMP-007,
`gen_open_items` CMP-009, `census` CMP-008, `check_doc_refs` CMP-007,
`held_status` CMP-006, `id_carrier` CMP-006, `kitlib/authority` CMP-006.
Each pick follows the file's stated job; the picks create three new
crossings, each now covered by an interface row. *Recommendation:* accept.

**Answer:** Accept, as recommended (operator, 2026-11-21, given in the
coordinator's session; recorded by the coordinator).

**R2. Two files doing two components' work.** `acceptance_record.py` holds
the spine's two-tree comparison (CMP-006) and five coordinator landing rules
on top of it (CMP-008). `check_doc_refs.py` holds a prose lint (CMP-007) and
the symbol-binding oracle that discharges a design row (CMP-006), which
WI-1023 retires. *Recommendation:* file a row to move `acceptance_record`'s
landing rules into a CMP-008 module behind an interface; no row for
`check_doc_refs` until WI-1023 lands, since the oracle's spine role goes
with it.

**Answer:** As recommended (operator, 2026-11-21). Filed as WI-1045;
`check_doc_refs` is looked at again when WI-1023 lands.

**R3. Three picks against the tag majority.** `hooks/pre-commit` CMP-007
(CMP-007's row names it and its interface carries CMP-007; its CMP-008 tags
are lane rules it runs as steps); `kitlib/config` and `kitlib/git` CMP-006
(the shared-kernel rule). *Recommendation:* accept.

**Answer:** Accept, as recommended (operator, 2026-11-21).

**R4. 22 in-scope files no LLR names.** Launchers and setup scripts CMP-009
(`check.{ps1,sh}` CMP-007); registries CMP-006; configuration files to the
component that mainly reads them (`process.toml`, `agents.toml`,
`agents-enabled`, `status.md` CMP-008; `stack.ini`, `coverage-floors`,
`declared-absences`, `pre-push` CMP-007; `runtime-flows.md` CMP-009).
*Recommendation:* accept.

**Answer:** Accept, as recommended (operator, 2026-11-21). The ruling is
recorded in WI-1021's Context on its branch.

### 3.6 Raised by a review of this hand-off (answer in place)

The operator brought a Gemini review of this hand-off and the F rows
(2026-11-21). The coordinator checked each point against the code; the
stale sections it found are fixed in place (§10). Three are the operator's
to decide. None blocks F-1 or F-2.

**G1. An adjudication sitting before F-3's batch act.** N4 schedules one
sitting, after F-8's text migration. But an acceptance act is refused while
any row of a registry it copies has accepted text drifted from its recorded
copy, unless the act itself blesses that row (`baseline_snapshot`, SR-207).
F-3's batch act copies the design and test-case registries, which already
carry drift (LLR-283, LLR-311, TC-293 and TC-332 from wave A, §3.1 Q5), and
F-1 and F-2 add more (F-1: LLR-373, LLR-067, LLR-199 and four TCs). Naming
those rows in the act's `--reaccepts` would bless text no sitting has read,
so the batch act cannot run until a sitting clears the drift.
*Recommendation:* one automated adjudication sitting after F-2 merges and
before F-3's batch act, beside the one after F-8. It also clears
`docs/ratify/CURRENT.md` and lets WI-1038 start.

**Answer:** Yes, run through antigravity cli (agy) model neon high.

**G2. F-4 (WI-1024): how strict are `dimensions` and `out_of_domain`?** The
review-churn plan's revision 20 made an LLR's `dimensions` cell the one
home of a behaviour's input set. Requiring both cells on every LLR that
`constrains` an interface came later, from Sol's scope critique of WI-1024,
which the coordinator adopted. The `gen_cases` grammar has ranges, sets and
booleans only; the plan counted 68 of 243 interface `data` cells as
alphabet-shaped, and most `file`, `stdout`, `bytes` and `git` interfaces
carry a schema or a document. About 197 interfaces need a constraining LLR.
- (a) As filed: both cells required; a missing one fails `--strict`.
- (b) Warn-first: a missing cell is reported but does not fail `--strict`;
  strictness is decided once population shows how many interfaces the
  grammar fits.

*Recommendation: (b).* It keeps the revision 20 ruling and defers only the
critique's addition until there is evidence.

**Answer:** b, this was already noted before though to go with route b and not follow the original filing, was this lost somewhere along the way?

*Coordinator (2026-11-21):* the operator had agreed to warn-first in the
coordinator's session, and the coordinator filed it here as a question
instead of recording it as a ruling; no earlier file held it. Applied:
WI-1024's Context records the ruling, and its Done-when makes a missing
companion cell a warning, with the Deliverable counting the cells by
interface channel for the later strictness call.

**G3. F-6 (WI-1026): role tags, or imports?** Revision 35 ruled that an
interface's consumers and requestors are generated from code once code
exists; revision 36, that each side hands over on its own. WI-1026 reads
them from `Consumes:` and `Requests:` header tags. No record weighs
inferring them from imports instead, and with WI-1015's item 3 retired
(§3.1 Q1) nothing checks that a `Requests:` tag matches an import. Of the
222 live interfaces with a local consumer or requestor, 133 are `call` rows,
which imports show; the other 89 are file reads, exit codes, CLI calls,
stdout and the environment, which imports do not show. An import also names
a file, not which of its interfaces, since a contract body sits in the
owner's module docstring.
- (a) As filed: tags for every channel.
- (b) Hybrid: cross-component `call` requestors read from imports and
  `Component:` headers; tags only for the other channels.
- (c) Tags as filed, plus a check that a `Requests:` tag's file imports the
  owner.

*Recommendation:* decide before WI-1026 is claimed, once F-2 shows how many
`call` rows survive as crossings. WI-1026 is late in F's order and nothing
before it depends on it.

**Answer:** Agreed, will wait.

### 3.7 The adjudication sitting (§3.6's first question): how it runs

The operator ruled the sitting: after F-2 merges, before F-3's batch act,
on Gemini Neon through `agy` at high effort. The kit has no supported way
to launch that model there. `coordinator_adjudicate.py` needs a claimed lane
and an adjudicator route enabled in `docs/agents.toml` and
`docs/agents-enabled`, and neither file has an `agy` or Gemini entry. Adding
one is a consent change, which is the operator's. So the coordinator runs
the kit's own pieces by hand on trunk, and only the launch differs:

1. File an adjudication row (`safety_class = "adjudication"`,
   `brief = "combined"`, `adjudicates` naming each drifted row as
   `amendment:` and each Drafted SR, LLR or TC as `first-acceptance:`),
   with `trace.py --bump-ids`, as WI-681 did.
2. Compose the brief with `scripts/coordinator/compose_lane.py` (it calls
   `adjudicate_brief.compose`), and bind the request with
   `adjudicate_brief.bind_pending(..., exclusive=True)`, as the entry point
   does.
3. Run Neon on one self-contained bundle, by file reference from the
   scratchpad, in plan mode: one session, never fanned out (PROCESS.md
   §6). Its reply is the verdict file, kept as returned; `verdict_refusal`
   must pass, and the binding records the outcome.
4. Take the act `adjudicate_act.compose_act` derives from the verdict: the
   re-acceptances in one commit (`intake.py snapshot --reaccepts`), then the
   first acceptances' flips with `--accepts` in the next. Only CLARITY and
   `MEANING+BLESS` amendments and ACCEPT rows are taken; MEANING and RETURN
   rows stay owed, and their follow-up is filed.

What it cannot accept: the first-acceptance brief covers SR, LLR and TC rows
only, so Drafted interface rows (IF-325, IF-326, and any F-2 adds) stay
Drafted. Drafted rows do not block F-3's batch act; drifted ones do. The
commits record the launch by hand and the hand-written binding.

To overrule: say so here before the sitting. The alternative is to register
an `agy` route and run the sitting from a claimed lane.

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
   and Hydrogen. A branch with both: Sol reads the whole diff, Hydrogen the
   prose part. Fix findings on the branch, then record the reviewers, findings and
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
- **Hydrogen (prose), through the Antigravity CLI (operator, 2026-11-21:
  "For prose please use antigravity (cli "agy") hydrogen"; it replaces
  Argon).** Effort low, as the prose route has run; the operator named no
  effort. Write one self-contained bundle into `<scratch>`: a first line
  saying it cannot read the repository and must make no tool call but
  reading this file, then the brief, the spec, its specref and the registry
  rows it names, or the diff. Run from `<scratch>`:
  `timeout 900 agy -p "Read the file bundle-NNNN.md in the current directory and carry out the review it contains. It is self-contained: make no tool call other than reading that one file. Give your verdict as your final message." --model gemini-4-hydrogen-low --mode plan --print-timeout 880s > hyd-NNNN.md`.
  `--mode plan` keeps it from editing; a file-reference ping returned in 8
  seconds. Run one at a time until two at once are shown to work.
  **If Hydrogen times out, skip it** (the operator's rule for Argon,
  2026-11-21); note in the review record that Sol reviewed alone, and do not
  retry it in a loop.
- **Argon (retired from the drill, 2026-11-21).** It ran through
  `opencode run -m opencode-go/gemini-4-argon --variant low` by the same file
  reference; it stalled at opencode's start-up on several runs, and the
  operator moved prose to Hydrogen.
- **Neon (adjudication sittings, operator, 2026-11-21, §3.6 G1):** the
  Antigravity CLI at high effort, `--model gemini-4-neon-high`.
- Tell each reviewer to answer from the brief and diff, and to cap its tool
  calls; a reviewer handed the whole repository reads for half an hour.

## 7. Merging and the suite

1. On trunk with a clean tree: `git merge --no-ff --no-commit maint/wi-NNNN`.
2. Conflicts: in a registry, rows with distinct new ids are all kept; an
   existing row both sides edited is reconciled cell by cell, keeping its
   status, and two edits that disagree in meaning go to the operator.
   `docs/id-watermark` takes, in each id space, the higher of the two marks
   (taking either side whole can lower a mark the other raised), then
   `trace.py --bump-ids`. A generated
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

## 8. Ids

Marks on trunk (`docs/id-watermark`): SR 247, LLR 395, TC 456, IF 325,
DA 28, SUR 4, CMP 9, WI 1045. Wave A minted LLR-393, LLR-394, TC-455, TC-456
and IF-325 (WI-1014); the rest of its ranges went unused and are free.
`maint/wi-1021` minted LLR-396, LLR-397, TC-457 to TC-461 and IF-326; its
marks rise to those on its merge (§7.2).

WI ids filed on trunk: WI-1021 to WI-1030 (F-1 to F-10), WI-1031 to
WI-1037 (the rest of phase 3, and the author-role row), WI-1038 (WI-1019's
follow-up), WI-1039 (the smoke tier), WI-1040 to WI-1044 (WI-1036's and
WI-1037's findings), WI-1045 (F-1's table, §3.5 R2) and WI-1046 (WI-1044's
finding: SR-243's model names). F-3 (WI-1023) mints
a successor SR for SR-180's discharge rule, so its launch range includes
one SR.

| Branch | LLR | TC | IF |
|---|---|---|---|
| WI-1019 | 395 | 457–458 | none |
| WI-1021 (F-1) | 396–400 | 457–464 | 326–328 |
| WI-1036, WI-1037 | none | none | none |
| WI-1022 (F-2) | 398–405 (used 398) | 462–475 (used 462–467) | 327–340 (none) |
| WI-1042 | 399–402 (none) | 468–473 (used 468–471) | none |
| WI-1048 | none | 474–479 (used 474–475) | none |
| WI-1023 (F-3) | 403–412, and SR-248 (used 403–407, SR-248) | 480–495 (used 480–484) | 327–330 (none) |

Marks on trunk at `22a9a9369`: SR 247, LLR 398, TC 475, IF 326, WI 1048.
WI-1049 to WI-1054 filed on trunk 2026-11-22. Marks on trunk at
`dc907c4c6`, after F-3's merge: SR 248, LLR 407, TC 484, IF 326, WI 1054.
WI-1050 mints no ids; the leftovers get their ranges at launch.
Third session ranges: WI-1056 SR 249 to 252, LLR 408 to 412, TC 485 to 495
(used SR-249 to SR-251, LLR-408, TC-485); WI-1051 to WI-1054 LLR 413 to
420 (none used) and TC 496 to 511 (used TC-500, TC-501, TC-504, TC-508).
Marks on trunk at `a6d447b76`: SR 251, LLR 408, TC 508, IF 326, WI 1059;
WI-1060 filed after. Fourth session: WI-1061 to WI-1063 filed on trunk;
WI-1058, WI-1059 and WI-1062 minted no ids. WI-1060's ranges are LLR 412
to 416 and TC 519 to 526 (its plan mints none). Marks on trunk after
WI-1063: SR 251, LLR 408, TC 508, IF 326, WI 1063. At the end of the
fourth session trunk's marks are SR 251, LLR 408, TC 508, IF 326, WI 1065;
the open branches have minted F-4 LLR 417 to 424 (421 and 422 held for
slice 5) and TC 527 to 534, and F-7 LLR 480 to 483 and TC 560 to 568. Each
merge takes the higher mark per space.
Fifth session: both merged; trunk's marks are SR 251, LLR 483, TC 568,
IF 326, WI 1069 (WI-1066 to WI-1069 filed). Ranges at launch: WI-1069 LLR
484 to 489 and TC 571 to 580; WI-1067 TC 569 to 570 (none expected). Next
free: LLR 490, TC 581.
Sixth session: WI-1069 used LLR-484 and TC-571; trunk's marks are SR 251,
LLR 484, TC 571, IF 326, WI 1071 (WI-1070 and WI-1071 filed). Ranges for
the next launches: WI-1070 LLR 485 to 489 and TC 572 to 580; WI-1071 LLR
490 to 492 and TC 581 to 585 (it expects none; a re-cut needs them);
F-4's slice 2 from LLR 493 and TC 586.
Seventh session: WI-1070 and WI-1071 minted none; F-4's slice 2 used
LLR-493 to LLR-495 and TC-586 to TC-588; WI-1072 to WI-1074 filed. Trunk's
marks: SR 251, LLR 495, TC 588, IF 326, WI 1074. Ranges at launch: F-4's
slice 3 LLR 496 to 510 and TC 589 to 605; WI-1045 IF 327 to 336, LLR 511
to 515 and TC 606 to 612; WI-1073 none. Next free: LLR 516, TC 613, IF 337.
End of the seventh session: slice 3, WI-1045, WI-1072 and WI-1073 minted
no ids; WI-1075 filed. Trunk's marks: SR 251, LLR 495, TC 588, IF 326, WI
1075. Next free: LLR 496, TC 589, IF 327.

WI-1019 used LLR-395 only; its TC range went unused and passes to WI-1021,
which used LLR-396 and LLR-397, TC-457 to TC-461 and IF-326; the rest of its
ranges are free once it merges.
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
- **D3 (operator, 2026-11-11; test-tiers HANDOFF §5):** no core reader for
  an earlier spelling; formats in git history are cut cleanly. The record
  before the 2026-11-16 vocabulary move (`2bee2b551`: `last_approved/`, the
  `approved`/`reattested` keys, `status = "Approved"`) is never read; an
  acceptance it carries reads as at or before the move's trunk commit
  (LLR-257). Check D3 before adopting any finding that reads history
  across that move: WI-1042's critique did, and its builder had to stop.
- **A keep-both join of a registry conflict can drop lines.** When two
  sides append rows that end alike (`status = "Drafted"`, `phase = 6`), git
  folds those lines into the shared tail after the conflict, so joining
  ours, then theirs, then the tail leaves the first block's last row short.
  Run `trace.py --strict` before committing such a merge, and diff each
  side's rows against the merged file.
- This hand-off's question labels (G1 to G3) spell retired stage tags. Cite
  them in a spec or any other live file as "§3.6, its second question", never
  as `G2`: `check_vocab --strict` refuses the tag, the commit hook runs it
  warn-only, and the smoke tier's `test_stage_ladder` fails on it
  (`1b15d07fb` did this; fixed in the commit after `1b22c9355`).
- **Closing a hand-run adjudication row** (WI-1049): in `complete/`, a
  `## Dispositions` section must carry ` ```toml ` draft or adoption blocks
  (the hook's `adoption-record` step; only `handback.close_adjudication`
  writes it, on a lane). A sitting run on trunk whose follow-up is already
  filed records its verdict and rulings under another heading; a draft
  block there would mint a duplicate at the next sweep.
- **A derived act can list a flip the hook refuses** (WI-1057). When a
  sitting accepts a child and returns its parent, `compose_act` still
  lists the child's flip, and the hook's parent-first step refuses the
  commit. Take the act without the child (less than listed, nothing more);
  its flip stays owed under that verdict until the parent is accepted.
  WI-1059 fixes the derivation.
- **The smoke tier's membership budget** (`docs/stack.ini` `[smoke-budget]`
  `max-tests`) fails the smoke tier when in-process tests outgrow it.
  Re-stamp it with the reason and about 4% headroom over the measured
  count, never at current+1 (`ff5b15e4a`).
- **A builder's worktree can show reds that trunk does not.** WI-1056's
  builder met 45 failures in five intake and snapshot modules, on its
  branch and with its changes stashed alike. The same modules passed on
  trunk before and after its merge (`235 passed`; `308 passed, 1
  skipped`). Re-run a builder's "fails on the base too" on trunk before
  believing it.
- **A single-kind sitting's preface differs from a combined one's**
  (WI-1061). A combined verdict opens each part with its `## <kind>`
  heading and ends with a `SITTING:` line. A single-kind verdict carries
  neither: row lines, the hat and stopping-boundary lines, one `OUTCOME:`
  line. `verdict_refusal` refuses the wrong shape. The preface must ask
  for the brief's own format. A first-acceptance row's `adjudicates`
  takes bare ids (`"SR-251"`); the `first-acceptance:` and `amendment:`
  prefixes belong to combined rows. Amendment tokens for IF-312 and
  CMP-006 alone leave the amendment section empty, since the brief shows
  no off-spine row, so the compose refuses.
- **A later RETURN voids an earlier ACCEPT of the same text** (WI-1061).
  A first-acceptance act does not check that the row's text is still the
  text the verdict judged (Flow 6: the coordinator confirms that by hand).
  So an old verdict's ACCEPT can still derive a flip after a later sitting
  returned the row, or after its text changed. Take a flip only from the
  latest verdict that judged the row's current text.
- **Merging trunk into a branch can be refused by the staged mirror
  check** (seen at WI-1060, and with the old code as with the new). When
  trunk took an act and the branch amends rows, trunk's copies enter the
  index unequal to a live file carrying the branch's amendments. Merge
  trunk-first instead: cut a temporary branch from trunk, merge the work
  branch into it, run the suite there, and fast-forward trunk to the tested
  commit (WI-1060's route: `0794b602e`, `39f7b87a4`).
- **An act commit carries the regenerated views:** the hook's
  `acceptance-fresh` and `open-items` steps refuse a snapshot commit whose
  `docs/ratify/CURRENT.md` and `docs/open-items.html` predate the copy. Run
  `trunk_step.py --root . --regen` after `intake.py snapshot` and stage
  both in the act's commit.

- **Never write into trunk's tree while a background commit runs there.**
  A `git add -A` in a running command sweeps in whatever is written before
  it runs: at WI-1068's act a new spec was staged into the act's commit;
  the coordinator stopped the commit (no lock left), unstaged the spec,
  moved it out, regenerated and recommitted. Stage named paths, or wait.
- **A first-acceptance act can turn trunk's `trace.py --strict` red.** The
  requirement-form findings (vague words, "such as") exempt a `Drafted`
  row, and the commit hook does not run `trace.py --strict`, so the
  eighth sitting's flip of LLR-484 left trunk's smoke red until the
  seventh session amended it (`855b4388f`). Run `trace.py --strict` after
  the flips and before the act's commit; a form finding then is an
  amendment owed to the next sitting.
- **A sitting's dry compose needs an existing work-item id.**
  `compose_lane.py` refuses a spec whose id names no row; dry-compose under
  a closed sitting's id before filing the new one.
- **A backgrounded `codex` inside a subshell is not waited for.** Run two
  Sol critiques as two background commands, not `( ... &)` and `wait` in
  one; the second's output file reads empty while it still runs.

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
- 2026-11-21: WI-1037 built; review round 1: Argon APPROVE, Sol one MINOR
  (seven observations had lost their model labels), fixed; round 2 narrow:
  Sol APPROVE, Argon timed out in start-up again. Merged `b62079378`; its
  leftovers filed as WI-1044. All three Argon timeouts froze at opencode's
  `init`, each launched in the same second as a Sol run; Argon now starts
  after Sol, staggered.
- 2026-11-21: smoke on the merged trunk `78ea4e843`: `3699 passed, 3
  skipped` in 87 s, CPU 547.7 s against 540 with one builder beside it (the
  1,014.6 s of WI-1019's run was mostly load). WI-1021 (F-1) built on
  `maint/wi-1021` (`fa057410d`): 167 files declare a component, membership
  read from the headers, the multi-membership advisory retired, IF-326 and
  three requestor additions cover the new crossings; smoke `3713 passed, 3
  skipped`. Stopped at §3.5 for the operator's ruling on its table.
- 2026-11-21: the operator ruled §3.5 (R1 to R4 as recommended); WI-1045
  filed for R2. The operator brought a Gemini review of this hand-off; the
  coordinator checked it and brought the opening, §1, §2 (WI-1044's broken
  row, WI-1039's critique), §7.2's watermark rule and §8 current, updated
  `docs/status.md`'s resume point, and raised G1 to G3 (§3.6; G1 confirmed
  in `baseline_snapshot`). On `maint/wi-1021` (`2e22775b6`): the ruling in
  the spec's Context, and the declaration's batch and PowerShell carriers
  narrowed to Done-when 1's (`::` and `<# #>` were read too), red first,
  `667 passed, 1 skipped` over every importer of `gen_arch_map`.
- 2026-11-21: WI-1021 (F-1) reviewed. Round 1: Argon APPROVE; Sol three
  MINORs, two adopted (an undeclared Python module took a same-stem shell
  file's component on its import edges; LLR-067's `code_symbol` lacked
  `_classifiable_edges`), one dismissed (a parenthesized module docstring:
  no file uses one, and the reader fails closed); fixes `d0b624208`,
  `2207 passed, 2 skipped` over the importers. Round 2 narrow: Sol APPROVE.
  Merged `147fed185` (the watermark took the higher mark per space; the
  generated files trunk's, regenerated), regen `ed671a026`. Smoke on
  `ed671a026`: `3714 passed, 3 skipped` in 172 s, CPU 738.0 s against 540
  (over, report-only; WI-1039's). Worktree and branch removed.
- 2026-11-21: the operator answered §3.6: G1 yes, the sitting before
  F-3's batch act run through the Antigravity CLI (`agy`) on Neon at high
  effort; G2 (b), applied to WI-1024 (Context and Done-when); G3, decided
  before WI-1026 is claimed.
- 2026-11-21: resumed. F-2 (WI-1022) building on `maint/wi-1022` in
  `D:/ai-template-wt-wi1022` from `1b15d07fb` (ranges LLR 398–405, TC
  462–475, IF 327–340). The operator moved prose review from Argon to Gemini
  Hydrogen through `agy`, and confirmed Neon through `agy` for adjudication
  (§6, the opening). WI-1039 waits for a quiet box: its readings need no
  other test run beside them. Scope critiques of WI-1040 to WI-1045, round
  1: Sol and Hydrogen (low) both APPROVE WI-1044; Hydrogen APPROVE WI-1043;
  the rest CHANGES-REQUESTED, 19 findings in all (Hydrogen 15 to 25 s per
  run). All adopted: `planmode` set on five rows, coverage bounds on WI-1040
  and WI-1041, WI-1042's pre-ledger, pairing and completeness rules settled
  with a Trust section and `needs` WI-1022, WI-1045 ordered after F-3 with
  its cover held to F-2's rule. `1b22c9355`. WI-1043 and WI-1044 building
  beside F-2.
- 2026-11-21: WI-1043's builder stopped: `traj_parse._git` is called by one
  test and re-exported by `gen_trajectory`. Ruled: test-only use is not a
  caller, and the grep covers code, not records; recorded on the branch as
  its D-001. WI-1044's builder stopped at a smoke red outside its scope:
  `1b15d07fb` wrote the retired tag `G2` into WI-1024's spec. Fixed on
  trunk (§9); WI-1044's SR-243 finding filed as WI-1046. `dd8f79e6c`.
- 2026-11-21: WI-1044 built (`maint/wi-1044`); review round 1: Sol and
  Hydrogen both APPROVE, no findings. Merged `e17c677f9`, regen
  `ca7039691`; smoke on `ca7039691`: `3714 passed, 3 skipped` in 114 s, CPU
  648.1 s against 540 (report-only). TC-385's drift owed to adjudication.
- 2026-11-21: WI-1043 built (`maint/wi-1043`; D-001, test-only use is not a
  caller). Review round 1: Hydrogen APPROVE; Sol one MINOR, confirmed and
  adopted (the remaining `_asof` checks returned before `_run_captured`, so
  the retained off-git coverage was not there); fixed `b47cae466`. Round 2
  narrow: Sol APPROVE. Merged `7371f0cf6`, regen `b3363670a`; smoke on
  `b3363670a`: `3714 passed, 3 skipped` in 121 s, CPU 647.1 s. Hydrogen's
  branch reviews ran in under a minute each. WI-1040 and WI-1041 building
  beside F-2.
- 2026-11-21: WI-1046 critiqued (Sol and Hydrogen both APPROVE, spec
  unchanged), `660805e62`. WI-1041 built (`maint/wi-1041`): a risk no act
  names reads unanchored, `_risk_first_written` deleted, LLR-239 amended.
  Review round 1, with SR-202's "a recorded accepted risk is read as
  covered" put to both by name: Sol and Hydrogen APPROVE (Hydrogen: within
  SR-202, "recorded" read as recorded by an act; no assumption here records
  a risk, so nothing reads differently in this repository). Merged
  `8b50e28c1` (RESYNC kept WI-1043's entry and this one), regen
  `7048e6a6f`; smoke `3714 passed, 3 skipped` in 210 s, CPU 704.7 s.
  WI-1046 built: SR-243's two cells name the roles in TC-385's words; review
  round 1: Sol and Hydrogen APPROVE. Merged `e29eb9d30`, regen `2b15d64e5`;
  smoke `3714 passed, 3 skipped` in 162 s, CPU 662.0 s. Acts owed to
  adjudication since this resume: TC-385, LLR-239, SR-243. Noted, not filed:
  the advisory and the release gate say "has reopened" for every unproven
  risk, which reads oddly for one no act ever accepted (WI-1041's builder).
  WI-1040 built; its branch is merging trunk to resolve WI-1041's conflict
  in `baseline_snapshot.py` before its review. Its builder found that the
  ledger walk it now shares with the accepted-risk reader follows the
  ledger's current path only; WI-1042, which must read across the
  2026-11-16 move anyway, takes that fix. `80cf46475`.
- 2026-11-22: WI-1040's branch merged trunk (`8539c3124`): its shared
  `_ledger_commits` walk keeps WI-1041's no-fallback end. Review round 1
  over `7048e6a6f..d6ccdb587`: Hydrogen APPROVE; Sol one MINOR, confirmed
  by execution and adopted (an undecodable ledger raised through
  `last_act`, against the branch's D-001); fixed `5dc1c9174` inside
  `last_act` only. Round 2 narrow: Sol APPROVE. Merged `2a57861ec`, regen
  `aab4808c3`; smoke `3714 passed, 3 skipped` in 130 s, CPU 652.6 s. On this
  repository the heading moved from naming a build commit that accepted
  nothing to the ledger's seq 185. WI-1042's spec amended: the cross-move
  reading lands in `_ledger_commits`, with a Done-when for all three
  readers. Left for the operator: `D:/rt1040`, a builder's scratch folder
  (logs and pytest temp, every link inside it), which the harness would not
  let the coordinator delete. Every branch beside F-2 has landed; F-2 is in
  its builder's full-suite run. `daa6bbe57`.
- 2026-11-22: F-2 (WI-1022) built and closed out on `maint/wi-1022`
  (`0b9921e98` plan, `d8ac920b8` build, `b2c4c2725` close): 240 interface
  rows with component or declared-party endpoints, 30 `call` rows retired,
  the one-body rule and the stricter cover (115 crossing edges, all
  covered). The builder's full suite ran under heavy load: 77 failures, all
  rerun green or fixed, or trunk's vocabulary red. Review round 1 split
  Sol in two (code; registries and documents; the brief was 500 KB whole)
  and gave the interface registry as a per-row summary in place of its
  204 KB diff. Hydrogen APPROVE (the five recorded deviations judged
  justified); Sol four MINORs, all adopted (two contract bodies that escape
  the uniqueness scan, LLR-244's missing symbol, the RESYNC entry's
  external-owner wording); fixes in progress. §3.7 records how the
  adjudication sitting runs. `b8dff9239`.
- 2026-11-22: F-2 round 1's fixes `edcd89c3f`; round 2 narrow: Hydrogen
  APPROVE, Sol two MINORs the fix introduced (an unparseable listed header
  raised through `interface_findings`; LLR-398's missing symbol), adopted,
  fixed `7a94e148f`; round 3 narrow: Sol and Hydrogen APPROVE. Merged
  `b2b0d9476`: the watermark took LLR 398 and TC 467 from the branch and WI
  1046 from trunk; `RESYNC_PACK.md` kept every entry; `trace.py`'s size
  baseline re-stamped to the merged 3780 (F-2 -55, WI-1040 -9). Before the
  commit, `check_resync` refused F-2's entry as anchored at the branch base
  rather than trunk's tip, which is how it reads any uncommitted merge (the
  hook does not run it); after the commit it reads OK. trace `--strict`:
  interface-findings 0. Regen `24656b1de`; smoke `3717 passed, 3 skipped` in
  106 s, CPU 648.3 s. Worktree and branch removed; no drill worktree open.
  `6915cde7d`.
- 2026-11-22: WI-1042 launched; its builder stopped before building, rightly:
  the spec's cross-move reading (added by the coordinator from the critique
  and WI-1040's finding) is a reader of an earlier spelling, which the
  operator's D3 forbids (§9). Ruled option 2: the vocabulary move is the
  record's cut, every acceptance it carries reads at or before its trunk
  commit (LLR-257's existing rule), and `_ledger_commits` keeps the current
  path, so WI-1040's finding was D3 working, not a defect. Spec amended on
  the branch.
- 2026-11-22: the adjudication sitting (§3.7). WI-1047 filed `3cd25133c`;
  brief composed by `adjudicate_brief.compose` (359K characters), verdict
  path reserved and request bound by the entry point's own functions;
  Gemini Neon (high) through `agy`, plan mode, one session, 494 s. Verdict
  `42df09628` (`verdict_refusal` None), recorded `902d218e9`: 19
  MEANING+BLESS and 1 CLARITY; LLR-080 and LLR-373 MEANING, not blessed (TC-081
  stale against LLR-080; LLR-373 contradicts LLR-199 and TC-435); 13 ACCEPT;
  6 RETURN (code names in LLR-393, LLR-394, TC-455, TC-456; TC-463 leaves
  five LLR-398 clauses unverified; LLR-395 has no TC, the parent-first
  circle with WI-1038). The derived act's first snapshot refused (SR-207),
  and nothing was taken. WI-1048 filed `3002931c7` to answer the verdict,
  critiqued (Sol three findings, Hydrogen APPROVE, all adopted)
  `2474d7b4f`. F-3 (WI-1023) and WI-1048 launched; WI-1042 rebuilding
  under the D3 ruling. Kit leftovers noted for filing: the act template
  names `scripts/intake.py` (the adopter's path); the first-acceptance
  template says "`APPROVE`" where its grammar reads ACCEPT.
- 2026-11-22: WI-1042 merged `abb00a88d` (review: Hydrogen APPROVE, Sol two
  MINORs fixed, round 2 both APPROVE; the watermark took TC 471), regen
  `b78624a23`; smoke `3717 passed, 3 skipped`. WI-1048 built: LLR-373's title,
  Detail and rationale and TC-081 follow the code, LLR-393, LLR-394, TC-455
  and TC-456 name no carrier, and TC-474 and TC-475 cover LLR-398 and
  LLR-395. Its review was briefed to judge each row as the next sitting
  will: Hydrogen APPROVE, Sol one MINOR (a docstring), fixed `9ae7df40c`;
  round 2 both APPROVE. Merged `0f670626a`: `test-cases.toml` kept both
  sides' new rows. The conflict had factored TC-471's last two lines (status,
  phase) into the shared tail, so a keep-both join dropped them; trace
  `--strict` caught it (integrity 2) and they were restored to trunk's
  bytes. Check every keep-both registry join this way (§9). WI-1038
  cancelled in the same merge. Regen `22a9a9369`. F-3's builder stopped on
  the API usage limit with its build uncommitted; resumed, told to merge
  trunk before its close-out. §0 written as the resume point.
  `73aa095ce`; smoke on it `3717 passed, 3 skipped` in 107 s, CPU 638.2 s.
- 2026-11-22: resumed. The operator confirmed OI-79 complete; its row gains a
  `follow_up` cell citing the delete and the tag (`gen_open_items
  --ruled-cover`: 0 findings, as before, now without leaning on WI-1006's
  text). F-3's builder had finished: build `19749ec70`, trunk merged
  `8e7d43c6f`, close-out `bcbc00bd6`, tree clean.
  `6eff30f85`.
- 2026-11-22: the second adjudication sitting. WI-1049 filed `d5cb62675`
  (57 tokens over 14 chains; WI-1047 cancelled, superseded); brief 398K
  characters, composed, reserved and bound as WI-1047's; Neon (high)
  through `agy`, plan mode, one session, 488 s. Verdict `7598caf5e`
  (`verdict_refusal` None), recorded `468c91fd9`: 23 MEANING+BLESS, LLR-244
  and LLR-257 MEANING not blessed (each amendment added code names), 22
  ACCEPT, TC-457, TC-468 and TC-475 RETURN. The derived act's first
  snapshot, tested read-only through `refresh_refusal`, refused over the
  two. The operator ruled: revert the two and act now. Their `detail` went
  back to the accepted text and WI-1050 was filed to re-land them,
  `0333b64f0`; re-acceptance `4e3e28a2f`, first acceptance `55e40f407`
  (each act commit needs the regenerated views, or the hook's freshness
  steps refuse it). `compose_act`: no act owed. `CURRENT.md` waits on three
  chains, from fourteen; trace drafts 25 to 3.
- 2026-11-22: F-3 (WI-1023) review round 1 over `73aa095ce..bcbc00bd6`, the
  design registry given as a TOML-verified diff without the three cells.
  Sol (low) in two halves, code 94 s and docs 54 s: the migrator turns CRLF
  into LF against LLR-407's "every other byte" (raised MAJOR by both halves,
  regraded MINOR: adopters carry the kit's `eol=lf` `.gitattributes`);
  multi-line literal strings (`'''`) are not handled (fails closed);
  SR-248 and LLR-403 omit the `Drafted` exemption of the no-test rule;
  LLR-263's rationale still names the Module cell. Hydrogen (low, 45 s)
  APPROVE. The coordinator added two from the second sitting's rule:
  LLR-244's and LLR-263's rewrites add parameter names to call
  signatures. All six adopted; a builder is answering them on the branch.
  WI-1051 to WI-1054 filed for this drill's kit leftovers. WI-1049 closed.
  `e93ae3fbe`.
- 2026-11-22: WI-1050 to WI-1054 critiqued (Sol and Hydrogen, all ten
  CHANGES-REQUESTED, every finding adopted): WI-1050 needs WI-1023 and
  settles TC-475 (narrowed; TC-428 and TC-429 point at LLR-395); WI-1052
  words three reading states; WI-1053's fork settled from
  `stack.ini.template` (the check reports itself dormant in files mode);
  `planmode = "none"` on all five. `a8e55cb1e`. F-3's round 1 answered by
  a builder (`4c105adf0`; red first for the CRLF and literal-string cases;
  567 passed over 18 modules); round 2 narrow, Sol and Hydrogen APPROVE;
  record `08ea43f55`. Merged `4335c1a4d`: statuses trunk's, LLR-244 the
  branch's text, LLR-257 trunk's reverted text, the three cells off every
  row (355 design rows and 422 test cases verified with tomllib against
  the expectation); the watermark LLR 407, SR 248, TC 484 from the branch,
  WI 1054 from trunk. Regen `d31ddce0c` (WI-1018 now names SR-221's stale
  wording). Smoke first stopped at `check_docs` on a link in F-3's spec one
  parent too deep, which the hook does not check; fixed `dc907c4c6`; smoke
  `3723 passed, 3 skipped` in 108 s, CPU 638.1 s. Unfiltered suite on
  `dc907c4c6`: `8282 passed, 31 skipped` in 32:10, no failure. Worktree and
  branch removed. The operator ruled F-3's batch act ("trace cells removed,
  requirement text unchanged"), to ride the third sitting's act.
- 2026-11-22: WI-1050 built (`maint/wi-1050`; LLR-257 re-amended with no
  code name at all, TC-457's unreadable-file test shown red against three
  deliberate breakages, TC-475 narrowed, TC-428 and TC-429 pointed at
  LLR-395). Review round 1: Hydrogen APPROVE; Sol one MAJOR dismissed (a
  generated evidence cell names its test by definition) and one NIT fixed.
  Merged `9ce559b84`, regen `867d6361e`; smoke `3724 passed, 3 skipped`.
- 2026-11-22: the third adjudication sitting. WI-1055 filed `982063eef`
  (38 tokens over 15 chains, the cell-only rows left to the batch ruling;
  brief 275K characters); Neon 444 s. Verdict `0c5440672`, recorded
  `8e08b3029`: 14 MEANING+BLESS, 1 CLARITY, 5 MEANING not blessed (LLR-244,
  SR-212, TC-239, LLR-263, TC-258), 5 ACCEPT, 9 RETURN (SR-248's chain).
  The act's first snapshot refused over the five; the operator ruled
  revert and act, as at WI-1049. Revert and WI-1056 filed `7b342d8b9`;
  re-acceptance `b86518820` (the copy drops the retired cells: the batch
  ruling), first acceptance `fe8db46b2`; `compose_act`: no act owed.
  `CURRENT.md` waits on four chains. WI-1055 closed.
- 2026-11-22 (third session): WI-1056 critiqued (Sol CHANGES-REQUESTED
  findings=3, Hydrogen CHANGES-REQUESTED findings=2; every finding
  adopted). The Done-when now says the tests are the row's and nothing is
  deferred. The Context says why the chains stay one row.
  `planmode = "single"` (Sol's choice over Hydrogen's `none`): the plan
  settles SR-248's split and LLR-406's SR. Record in
  `docs/reviews/2026-11-22-scope-critiques/WI-1056.md`.
- 2026-11-22 (third session): WI-1056's plan (`9548c30c1` on its branch)
  approved with two corrections. SR-221's and LLR-263's titles say "file",
  since a re-acceptance is per row. LLR-405 cites LLR-204's grammar rather
  than restating it. SR-248 splits into SR-248 (discharge), SR-249
  (placement) and SR-250 (the back-link reading); LLR-406 moves under a
  new SR-251 (generation); LLR-403's discharge clause goes to a new LLR-408
  (TC-485). Ranges: SR 249 to 252, LLR 408 to 412, TC 485 to 495. The
  leftovers launched beside it from `3c33b3783`, so their amendments ride
  the fourth sitting (ranges LLR 413 to 420, TC 496 to 511). WI-1053
  needed no code: TC-504 pins the existing dormant report and LLR-398
  states it. Review: Hydrogen APPROVE, Sol one MINOR dismissed (generated
  evidence). Merged `4cb091e79`, regen `af357a570`, smoke `3724 passed,
  3 skipped`. WI-1054 (TC-508 under SR-052 and LLR-113; flat legend names
  the component node) was reviewed in two rounds: round 1 Hydrogen APPROVE,
  Sol one MINOR adopted (TC-508's Expected narrowed to one invariant);
  round 2 Hydrogen APPROVE, Sol one MINOR fixed in the record. Merged
  `b486b1ea1` (watermark TC 508; TC-504 and TC-508 both kept), regen
  `b247dc55b`, smoke `3724 passed, 3 skipped`. TC-508 sits in phase 3, so
  `check_trajectory` warns that the closed phase 3 took new content until
  the fourth sitting accepts it. New scratch folders for the operator:
  `D:/rt1053`, `D:/rt1054`. IF-231's notes (Drafted) still describe the
  reach as through the owner's design rows only: a candidate for WI-1018.
- 2026-11-22/23 (third session): WI-1051 to WI-1054 built beside WI-1056
  and merged. WI-1051 `fb782bbc5`: both reviewers APPROVE. WI-1052
  `4e2ad727a`: Sol's code-name finding adopted, IF-217's data cell
  dismissed. Smoke after it failed the membership budget (3741 over 3740),
  re-stamped 3890 `ff5b15e4a`. WI-1056 built from its approved plan;
  review round 1 Sol one MAJOR on TC-481's refusal assertions, adopted;
  round 2 APPROVE. Merged `db6f47649` (watermark SR 251 and LLR 408 by
  `--bump-ids`), regen `b819f6dcb`. Smoke `3749 passed, 3 skipped`; the
  five modules the builder saw fail plus its own: `308 passed, 1 skipped`.
  The fourth sitting, WI-1057 (filed `ca5a7d9dc`; Neon about 8 minutes):
  all 9 amendments MEANING+BLESS, 16 ACCEPT, 2 RETURN (SR-251, TC-483).
  Verdict `c8d0a4453`, recorded `d41e8069f`. Re-acceptance `e9f6362cc`
  needed no ruling. First acceptance `072f93670` flipped 15 rows. The
  parent-first step refused LLR-406's flip under the returned SR-251, so it
  is held. Closed `a6d447b76` with WI-1058 (the returns) and WI-1059 (the
  derivation gap) filed. Every drill worktree removed, `wi1048` included.
  The operator gave a standing revert ruling (§0 step 2) and asked which
  long-term fix is right (§0 step 4).
- 2026-11-23 (third session, end): the operator pushed through `80d64a5f3`
  and ruled the row-scoped copy filed: WI-1060. `docs/status.md`'s resume
  note now points at §0.
- 2026-11-23 (fourth session): WI-1058, WI-1059 and WI-1060 critiqued.
  WI-1058: Sol CHANGES-REQUESTED findings=2, Hydrogen findings=1; both
  adopted (`planmode = "none"`, one row). WI-1059: Sol findings=4,
  Hydrogen findings=1; all adopted (`single`, a Trust section, the
  outcomes settled: a hold chains, an all-held verdict refuses, a held
  flip stays owed and marked, SR-231 unchanged, LLR-338 amended). WI-1060:
  Sol findings=2, adopted (the MAJOR in part: one traced-cell contract
  across Done-when 1 to 3, its rule the plan's); Hydrogen APPROVE.
- 2026-11-23 (fourth session): WI-1059's plan approved (`50d4d3fbe` on its
  branch; "waits" for "held", the hook's tier reader made public, a
  fixpoint over the parent-first findings, SR-231 and LLR-306
  unamended). WI-1058 built (no plan); review round 1 Sol and Hydrogen
  APPROVE (bare lines; Sol's log shows it read the code and tests).
  Merged `1204486b6`, regen `6925769b1`; smoke `3751 passed, 3 skipped`
  (109 s). The fifth sitting, WI-1061 (filed `c3ab6a8ee`, corrected to a
  first-acceptance sitting `0385b759e`; Neon 321 s): SR-251, LLR-406 and
  TC-483 all RETURN (live scope, the keyless condition, an all-or-nothing
  write). Verdict `bba8aeac3` with two launcher-caused wrapper lines
  removed (§9), recorded `4e3e9bf4b`; no act owed. Closed with WI-1062
  filed. Not filed: a standing report of verdicts with waiting flips
  (WI-1059's plan, noticed, not in scope).
- 2026-11-23 (fourth session, later): WI-1059 built from its approved
  plan. The builder's dodge of OI-30 D3's lexical guard (a constant the
  guard cannot see) was replaced by a named exemption in the guard, with a
  test that the exemption is narrow (`da3b7b2e3`). Review: Hydrogen
  APPROVE; Sol two MINORs on IF-296's and IF-308's `data` naming functions,
  dismissed (interface rows are off-spine; WI-1052's precedent). Merged
  `e44ee30b6`, regen `121ce2e00`; smoke `3760 passed, 3 skipped`. WI-1062
  critiqued (both APPROVE), built; the coordinator had it keep a leading
  byte-order mark (`977c7d49f`). Review round 1: Hydrogen APPROVE, Sol one
  MINOR (the failed move's temporary-file promise was unbounded), fixed in
  `cccf4026e`; round 2 both APPROVE. Merged `3dc548e1a`, regen
  `4279a7c33`; smoke `3764 passed, 3 skipped`. The sixth sitting, WI-1063
  (filed `6a585b473`; Neon 237 s, combined): LLR-338 and TC-368
  MEANING+BLESS; SR-251, LLR-406 and TC-483 ACCEPT. Verdict `e10a261cb`,
  recorded `f16f4e361`, re-acceptance `76192dab6`, first acceptance
  `43f711b6d` (three flips in one commit). No spine row owes an act.
  WI-1060's plan approved with D4 changed (an act that writes nothing
  stays refused); WI-1060 building.
- 2026-11-23 (fourth session, later still): F-4's plan approved for slice
  1 (of five), F-7's plan approved with D13 recorded and D15 evidenced;
  both building beside WI-1060. WI-1060's builder resumed after a server
  error (HTTP 500) with its red tests committed. WI-1064 filed from F-7's
  plan.
- 2026-11-23 (fourth session, end): WI-1060 reviewed. Round 1: Hydrogen
  APPROVE; Sol (code and docs halves) two MINORs adopted (a row's acting
  reviewer read at the row; the README's deletion rule) and four
  dismissed, the migrator's record step filed as WI-1065 for the
  operator's choice. Round 2: both APPROVE. Merged trunk-first on a
  temporary branch (`0794b602e`, regen `39f7b87a4`). The unfiltered suite
  there gave `8357 passed, 31 skipped` (41:58), no failure, and trunk was
  fast-forwarded to it; suite line recorded `52efaf6c4`. F-4's slice 1 was
  reviewed: round 1 had six Sol MINORs, fixed `690824531` (LLR-424 and
  TC-534 new); round 2 had both APPROVE, recorded `286ad02b4`. F-7 was
  reviewed: round 1 had Hydrogen APPROVE and Sol six findings, one MAJOR
  (LLR-480's two obligations, split to a new LLR-483 with TC-568), fixed
  `c319d6b9f`.
- 2026-11-23 (between sessions, operator): ruled WI-1065 as refined (c)
  and recorded it in the spec and §0 step 6 — keep SR-179 unchanged; in a
  record whose act ledger carries `kept`, skip copying live over record
  copies when the record is already in the current vocabulary, and refuse
  before writing any record file (including in the registry step) when
  the record still holds earlier vocabulary. Owes its scope critique
  before build.
- 2026-11-23 (fifth session): F-4's slice 1 (WI-1024) merged `6ed2cfc28`
  (D16: `Constrains` moved into `record_rows.ROUTED_TRACED_CELLS`; the
  watermark LLR 424 and TC 534; RESYNC both entries; a three-way
  cell-by-cell registry check, no cell changed by both sides; 571 passed,
  1 skipped over the modules both sides touched), regen `263b319df`; smoke
  `3796 passed, 3 skipped`. F-7 (WI-1027): trunk merged into the branch
  (`60d44150a`: LLR-244 joined, both sides' new rows kept, WI-1064's
  specref re-pointed, F-7's RESYNC entry re-anchored at `263b319df`, since
  `check_resync` reads the change's base as the merge-base with trunk); a
  builder moved blast radius onto the tree walk for a constraining design
  row too (`interface_reach`, `coherence._route`; LLR-421 and TC-531
  amended; this repository's reach byte-identical). Review rounds 2 to 5
  (narrow): round 2 Hydrogen APPROVE, Sol two MINORs adopted; round 3 (the
  merge's resolution by `git show --remerge-diff`, and the move) Hydrogen
  APPROVE, Sol one MINOR adopted in part (the tree built once per call of
  each walk, not once per coverage call; prose corrected); round 4
  Hydrogen APPROVE, Sol one MINOR (a linearity claim the fix added)
  adopted; round 5 Sol APPROVE. Merged `0303183a3` (clean), regen
  `97d4444bd` (its message corrects the merge's: the amendments owed were
  LLR-367, LLR-244 and LLR-257); smoke `3874 passed, 3 skipped`. Worktree
  and branch removed.
- 2026-11-23 (fifth session): the seventh sitting, WI-1066 (filed
  `123cd20f5`; 31 tokens, brief 339K characters, so sitting A stays
  separate; Neon 431 s): 17 amendments MEANING+BLESS, SR-207 MEANING not
  blessed; 12 ACCEPT, TC-560 RETURN. Verdict `581275692`, recorded
  `064859662`. Re-acceptance `dbe7da595` printed LEFT OWED for SR-207 and
  sitting A's 26 rows and completed: the first ledger entry carrying
  `kept`, no revert. First acceptance `8f45c0d5c` (LLR-480 to 483, TC-561
  to 568). Closed with WI-1067 filed to answer SR-207 and TC-560.
- 2026-11-23 (fifth session, later): WI-1069 filed and critiqued with
  WI-1064, WI-1065 and WI-1067 (Sol and Hydrogen, every finding adopted,
  `d62f3c74b`; records in `docs/reviews/2026-11-23-scope-critiques/`).
  WI-1067 built (SR-207 fronted and its retirement rule stated; LLR-245
  names the constrains link, the coordinator's ruling; TC-560 drives two
  more faults; new tests shown to catch mutations, since the behaviour
  existed), round 1 Sol and Hydrogen APPROVE, merged `844b851ce`, regen
  `f78cb0a57`; smoke `3882 passed, 3 skipped`. WI-1069's plan approved;
  WI-1064's plan approved (D3: SR-246, LLR-358, TC-397 left unamended;
  D7: a re-parent is caught by the standing finding in the hook), built,
  round 1 Sol and Hydrogen APPROVE. WI-1065's plan approved (D3 whole-run
  refusal; D7 the link step never opens the scratchpad), built, round 1
  Hydrogen APPROVE and Sol three MINORs ruled (§0 step 2). The hand-off
  written at the session's end with two builders still running (§0).
- 2026-11-23/24 (sixth session): WI-1064 merged `42519b754` (review
  recorded at the merge: Sol and Hydrogen APPROVE; the builder's
  `test_snapshot_readers` red not reproduced on trunk), regen `fb07bcaba`;
  smoke `3886 passed, 3 skipped`. WI-1069 review round 1: Hydrogen APPROVE;
  Sol, split in code and documents halves (the whole brief was 164K), one
  MAJOR in both (the RESYNC guidance: an act taken on a lane but not landed
  is refused at landing, since the merge slot re-judges each lane commit;
  now "take and land", with the recovery) and one MINOR (LLR-484's lone
  accepted group stays unlabelled; TC-571 names it; the `Drafted` collapse
  left to OI-71's case), both adopted, fixed `a8d4baad9`; round 2 both
  APPROVE. The builder's smoke re-stamp 3890 -> 4060 and new in-process
  module confirmed. Merged trunk-first on a temporary branch (`d4bc87a41`,
  regen `db107c829`); the unfiltered suite there gave `8514 passed, 31
  skipped` (36:10), no failure; trunk fast-forwarded. WI-1065 round 2:
  Hydrogen APPROVE, Sol one MINOR (a backslash-escaped backtick opened a
  code span), adopted, red first, fixed `54579f85e` (TC-427's method names
  the cases); round 3 both APPROVE. Merged `e489f8a03` (status.md's
  generated queue line took trunk's), regen `6fc3042b8`; smoke `3927
  passed, 3 skipped`. Worktrees wi1064, wi1065 and wi1069 removed, with
  `D:/review-tmp/2026-11-23-wi1065` and `-wi1069`.
- 2026-11-24 (sixth session): WI-1068 (sitting A) re-scoped `fbd50be29`:
  the 38 slice-1 tokens plus the 16 rows WI-1064, WI-1065, WI-1067 and
  WI-1069 owe (39 amendments, 15 first acceptances, 32 SRs); the brief
  387,509 characters, under the split bound, so one sitting; it shows the
  three link-only rows and all 21 constrains links.
- 2026-11-24 (sixth session): the eighth sitting, WI-1068 (Neon 589 s,
  combined): 15 amendments blessed (SR-211 CLARITY; SR-178, SR-207, SR-245,
  SR-247, SR-249, LLR-245, LLR-357, LLR-359, LLR-369, LLR-403, TC-195,
  TC-396, TC-427, TC-480 MEANING+BLESS), 24 MEANING not blessed (the 21
  link rows, since the brief shows neither the linked interface nor a
  link-only row's text, confirmed from the brief; LLR-167, TC-161; TC-398;
  four link rows also dropped clauses); 11 ACCEPT, 4 RETURN (TC-530,
  TC-571, LLR-423, TC-533). Verdict `51c6db6eb`, recorded `87746787d`,
  re-acceptance `86cb4f806` (LEFT OWED the 24, no revert), first
  acceptance `d4554561b`. Closed `d35dc2a52` with WI-1070 and WI-1071
  filed; both critiqued (Sol and Hydrogen, every finding adopted; the
  session-variable home settled on LLR-423), with this hand-off.
- 2026-11-24 (seventh session): WI-1070's and WI-1071's plans approved (D1
  to D12, D1 to D13 confirmed; TC-398's wording routed to WI-1071). Their
  findings filed as WI-1072 (a judged cell's identity-shaped line enters
  the binding) and WI-1073 (the component view header's placement
  sentence), `369f87dc4`. Trunk's `trace.py --strict` was red on LLR-484's
  "such as" since the eighth sitting's flip (§9); amended `855b4388f`.
  F-4's slice 2 built (36 of CMP-007's 38 interfaces reached; IF-049 and
  IF-144 carried to slice 3; IF-002, IF-003 and IF-016 added to slice 1's
  rows on the coordinator's answer).
- 2026-11-24 (seventh session): WI-1071 review round 1: Hydrogen APPROVE;
  Sol four MINORs (LLR-039's guide-edit clause bounded to a derived change,
  LLR-047's "dev-setup", LLR-300's one-obligation claim corrected in the
  Deliverable, TC-571's test asserting values), fixed `8c448c988`; round 2
  both APPROVE. Merged `b3570fbce`, regen `6d6605835`; smoke `3933 passed,
  3 skipped`. Slice 2 review round 1: Hydrogen APPROVE; Sol four MINORs,
  three adopted (LLR-019 "admitted", LLR-014's print rule, TC-586's
  locations) and LLR-495's parent dismissed; round 2 both APPROVE. Merged
  `88e589103` (watermark LLR 495, TC 588 from the branch, WI 1073 from
  trunk; three-way cell check clean), regen `d7e3a57df`; smoke `3936
  passed, 3 skipped`. WI-1070 review round 1: Sol and Hydrogen APPROVE (the
  deferred-import window's re-stamp 44 -> 46 confirmed). Merged
  `35adac5c0`, regen `7c9c5c940`; smoke `3956 passed, 3 skipped`.
- 2026-11-24 (seventh session): the ninth sitting, WI-1074 (filed
  `ee3f5288e`; 60 tokens, brief 344,194 characters; Neon 587 s, combined):
  49 amendments blessed (26 CLARITY, 23 MEANING+BLESS), every row with a
  moved link among them; LLR-014 MEANING (its unmeasured-budget line
  against IF-004), answered in F-4's slice 3; 10 ACCEPT. Verdict
  `efcdbed4f`, recorded `e8c7896c1`, re-acceptance `ed5ea710a` (LEFT OWED
  LLR-014), first acceptance `8fb0840df`, closed `9e8eb6e57`; smoke `3956
  passed, 3 skipped`. WI-1072 and WI-1073 critiqued (Sol and Hydrogen,
  every finding adopted: `planmode`, WI-1072's Trust section),
  `d1571e8fc`. F-4's slice 3, WI-1045 (plan first) and WI-1073 building.
- 2026-11-24 (seventh session, later): WI-1073 built (the component view
  header's placement sentence), review Sol and Hydrogen APPROVE, merged
  `bd3f004a9`, regen `1e8b2a28f`; smoke `3956 passed, 3 skipped`. WI-1072's
  plan approved (refuse at compose; D6's condition failed, so reservation
  refuses non-composed identity lines too), built; round 1 Hydrogen
  APPROVE, Sol two MINORs (the exact-match rule, the RESYNC guidance),
  adopted; round 2 both APPROVE. Merged `33407fb30` (RESYNC kept both
  entries), regen `0de9125ad`; smoke `3993 passed, 3 skipped`; a real
  amendment brief composes under the new check. WI-1045's plan approved
  (D1 to D12; the identity function stays in `acceptance_record`), built
  (33 definitions moved byte for byte into `landing_rules.py`, 989 -> 689
  SLOC); round 1 Hydrogen APPROVE, Sol one MINOR (the RESYNC names),
  adopted; round 2 both APPROVE. Merged `3bd545635` (163 passed over the
  modules it and WI-1072 share), regen `10d9ccc13`; smoke `3994 passed, 3
  skipped`. F-4's slice 3 built (71 of 76 CMP-008 interfaces, LLR-014
  answered, 48 tests); round 1 in five sessions (Sol code, C1, C2;
  Hydrogen C1, C2): Hydrogen APPROVE, Sol seven MINORs adopted; round 2
  both APPROVE. Merged `eb96d6298` (no slice-3 file imports a moved name),
  regen `3a187cd39`; smoke `4014 passed, 3 skipped`. WI-1075 filed
  `e12781779` from slice 3's IF-144 proposal and critiqued (Sol four
  findings, Hydrogen one, all adopted), with this hand-off.
