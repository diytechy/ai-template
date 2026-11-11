# Handoff: vocabulary migration, then the functional changes

Written 2026-11-11 for two readers. The owner reviews it and writes a decision
into each `Owner:` line. The next session reads it cold, with no access to the
conversation that produced it, cuts a branch and makes the changes.

It sits beside `README.md`, the review this work came from. Read that first if
a claim here needs its evidence; sections are cited as README §N.

## 1. Where things stand

| | |
|---|---|
| Repository | `C:\Projects\ai-template`, trunk `refactor_again`, at `7fa851f33` |
| Primary checkout | untouched by this work |
| This work | worktree `C:\Projects\ai-template-wt-test-tiers`, branch `proposal/test-tiers`, **committed locally, not pushed**: 90 changed files, 5 new files |
| Interpreter | `C:\Projects\ai-template\.venv\Scripts\python.exe` (the worktree has no venv) |
| How it was run | from outside the repository root, on purpose, so the repository's own skills and workflow did not drive it. No work item, no lane claim |

The branch holds two things (README, "How to review this branch"):

1. **A prototype of change-scoped checks**: `run.cmd iterate`, a 16-test
   canary set, 22 tests. Repo-local; no shipped file.
2. **A rename of three settings** and the words around them, with its
   `RESYNC_PACK.md` entry and a new Checks section in the shipped glossary.

Verified: the unfiltered suite passed after the rename apart from one
line-count ratchet, since fixed; the modules the later edits touch were re-run
green; the four strict lints pass. The record is README §5.

Three things the next session must know before touching the branch:

- **It is committed with the commit hook bypassed,** at the owner's direction
  on 2026-11-11: this is a maintenance branch, and the standard conventions
  (hooks, lane claims, work items) are set aside for it. That permission was
  given for this branch. Ask before applying it to another.
- **The hook would have refused it.** Three floor steps (`cli-reference`,
  `interface-reference`, `trajectory-map`) report stale generated views,
  because help text, contract text and a dashboard panel were reworded. The
  views are still stale in the commit. They regenerate with
  `trunk_step.py --regen` when the work reaches trunk; a claimed lane is
  exempt from those steps and an unclaimed branch is not.
- **It is not pushed.** The commit protects the work from a removed worktree,
  not from the machine.
- **To discard it all:** `git worktree remove --force
  C:\Projects\ai-template-wt-test-tiers`, then `git branch -D
  proposal/test-tiers`.

## 2. Decisions the owner has made

- The 16-test canary set is accepted as a first cut.
- `[bars]` does not belong in `docs/stack.ini`, and the word means nothing
  from outside. Renamed and re-homed (README §12).
- `red_mark` was ambiguous. Now `[product] expected_failure_marker`.
- `red_rounds_max` did not say what happens at the limit. Now `[build]
  stop_lane_after_consecutive_commit_check_failures`.
- A shipped contract changing is not a reason to hold back. Re-syncs are fine;
  clarity and right placement in the template come first.
- One word for one thing across the whole kit, in agreement with the glossary.
- The remaining vocabulary work goes on its own branch (owner had no strong
  view; this session's recommendation).
- The overnight runner should be removed (§6, item B8).
- This is a maintenance branch. It does not follow the repository's standard
  conventions, and its commit bypassed the hook.

## 3. What the owner is asked to decide

Each item has a recommendation. Write the decision on its `Owner:` line.

**D1. Keep this branch?** Recommended: yes, as the base the next branch is cut
from.
Owner: yes. Committed 2026-11-11 with the hook bypassed; the three generated
views were not regenerated.

**D2. The terms in §4.** Eight glossary entries are drafted, three of them for
things that had no obvious name. Edit them in place.
Owner:

**D3. Old records.** Three renames change a format that is already written
into history (commit trailers, session-log headers, a work-item key).
Recommended: new records use the new form, and the readers accept both forms.
The alternative is a clean break, after which lanes in flight must re-attest
and archived records stop verifying.
Owner:

**D4. Names of existing tests.** 100 evidence entries in 20 test-case rows
name a test whose function or file name carries an old word. Recommended:
rename the 12 test files and their functions along with the code, and update
the evidence cells in the same change, since a half-renamed suite is the
inconsistency the owner asked to remove. The cheaper alternative is to leave
existing test names and apply the vocabulary to new tests only.
Owner:

**D5. The 13 approved rows** whose text uses an old word (README §12).
Changing approved text is an amendment. Recommended: amend the wording on the
migration branch and let the landing mint the adjudication rows, each a
wording-only change.
Owner:

**D6. What a commit must pass.** `[required-checks] commit` is `"smoke"`
today. Recommended: `"iterate"`, together with D7.
Owner:

**D7. What a landing must pass.** Today a hand landing runs the smoke tier and
the unfiltered suite runs once per leg. Recommended: the unfiltered suite once
per landing, declared as `[required-checks] landing` with a reader.
Owner:

**D8. The overnight runner.** Recommended: remove the launcher (the first row
of the table in B8) with the migration, and decide the other three rows with
B9.
Owner:

**D9. Order.** Recommended: vocabulary first (§4, §5), then the functional
changes in the order of §6.
Owner:

## 4. The glossary, drafted

The shipped glossary (`project-trajectory/GLOSSARY.md`) says one term names
one concept, and that an entry states which word is kept where two were used.
Its Checks section already holds seven entries from this branch: required
checks, commit checks, landing checks, gate checks, check suite,
expected-failure marker, commit-check failure cap.

The two old words name more things than those. Scripts and tests hold 219
distinct names carrying "bar" or "red", 2,709 occurrences. Below is one draft
entry for each remaining thing. `Alternatives` lists other names considered.
The drafts name other entries in plain words; link them when they go into
the glossary.

### 4.1 checks attestation

> The line in a commit message recording that a named set of checks passed on
> a named tree: `Checks-Passed: tree=<sha> work=<sha> checks=<commit|landing|none>
> tests=<digest|none> <summary>`. `integrate.py attest` writes it for the
> commit checks and the station refresh writes it for the
> landing checks; the merge slot re-derives both ids from
> git before it trusts one. Formerly the "bar attestation", written
> `Bar-Green: ... bar=<review|landing|no-bar>`; **checks attestation** is kept,
> and a trailer in the earlier form still verifies.

- Renames: trailer key `Bar-Green` to `Checks-Passed`; field `bar=` to
  `checks=`; values `review` to `commit`, `landing` unchanged, `no-bar` to
  `none`; CLI `attest --bar review` to `attest --checks commit`.
- Alternatives: `Checks-Green:` keeps the kit's green idiom. `Verified:` is
  taken by row status.

Owner:

### 4.2 failed-checks record

> The two header lines a build's session log carries when its
> commit checks failed: the build commit they refused and a
> one-line summary. The commit-check failure cap
> counts these since the last passing attestation. Formerly the "red record";
> **failed-checks record** is kept.

- Renames: headers `# bar-red:` and `# bar-summary:` to `# checks-failed:`
  and `# checks-summary:`; `red_rounds` to `failed_rounds`; `red_record`,
  `format_red_record`, `parse_red_record` likewise; `EXIT_RED_CAP` to
  `EXIT_CHECK_FAILURE_CAP`; `red_cap_check` to `failure_cap_check`.
- Alternatives: "failure record" is shorter but does not say what failed.

Owner:

### 4.3 landing stage

> The stage a work item pins its landing checks to. A row
> claimed to deliver evidence at a stage is checked at that stage even if the
> repository's derived stage moves while its lane is in flight. Declared in
> the work item as `landing_stage`. Formerly the item's `bar`; **landing
> stage** is kept.

- Renames: the work-item key `bar` to `landing_stage`; `WI_BARS`,
  `_lane_bar_directives`, `_declared_bar_or_refusal`, `bar_gate`.
- Scope: no live work item declares the key; 31 archived ones do, with values
  `DevStg-Reqs`, `DevStg-Tests`, `DevStg-Impl`. The reader must keep reading
  `bar` in archived files, as it already reads the retired `g1`/`g2`/`g3`
  values.
- Alternatives: `checks_stage`; `gate`, which the kit already uses for the
  stage gates and would overload.

Owner:

### 4.4 evidence gap

> A test case that is not approved although every requirement it verifies is
> cited by a work item recorded done: the work is closed and its evidence is
> not. The gap census names each one, and the landing mints an adjudication
> row for it. Formerly a "red TC"; **evidence gap** is kept.

- Renames: `red_tc_census`, `parse_red_tc`, `red_tc_values`,
  `RED_TC_PREFIX`, `ADJUDICATE_RED_TC`, `_TC_NOT_RED`.
- Why this word: the census that finds them is already the gap census.
- Alternatives: "unproven test case"; "unverified test case", which collides
  with the row status Verified.

Owner:

### 4.5 attest settings (the reader of the two declared values)

Not a glossary term: a code name. `kitlib/red_mark.py` holds the reader for
the commit checks' suite and the expected-failure marker, and the marker's
counting rules.

- Proposed: module `kitlib/expected_failure.py`; class `Bars` to
  `AttestSettings`, with fields `commit_checks` and `marker` in place of
  `review` and `red_mark`; `read_bars` to `read_attest_settings`. In
  `kitlib/config.py`, `red_rounds_max()` to `commit_check_failure_cap()`.
- Registry: LLR-368 binds the module and these symbols; LLR-343 binds
  `red_rounds_max`.

Owner:

### 4.6 stage, not bar, for the retired dial

Not a new term. The kit once had a "bar" dial for stage thresholds and
retired it for the stage ladder (`DevStg-*`). The word survives in readers of
the retired spelling and in a few live names.

- Proposed: live names say stage or rung (`sr_bar` and `sn_bar` to `sr_stage`
  and `sn_stage`, `maturity_bar` to `maturity_stage`, `stage_to_bar` and
  `normalize_bar` likewise, the dashboard's "rung bar" to "rung strip" if it
  names the graphic). Names that exist only to read the retired spelling keep
  the retired word and say so (`_LEGACY_BAR_THRESHOLD`, `_RETIRED_BARS`,
  `RETIRED_BAR_ALIASES`, the `DevBar-*` aliases).
- Needs a look by whoever does it: `trace.py` and `kitlib/config.py`, to
  confirm each `*_bar` name is the stage and not something else.

Owner:

### 4.7 failed, not red, in running prose

Not a glossary term: a usage rule for the glossary's preamble.

> A run of checks **passes** or **fails**. "Red" and "green" are not used for
> either, except once, where `process.md` names the red, green, refactor
> cycle.

- Applies to prose, comments and messages. For test names see D4.

Owner:

### 4.8 minimum or standard, not bar, for a threshold

Not a glossary term. Where "bar" is plain English for a threshold ("the
shipped bar", "raise the bar"), write the specific thing: minimum, standard,
level. 109 lines of shipped prose hold the bare word; 32 are in the
coordinator's recipes (see B8, which may remove them).

Owner:

## 5. Doing the migration

Cut a new branch from this one.

**Order.** Glossary first, then one concept at a time in the order of §4, the
persisted formats before the names that only code sees. Run the checks below
after each concept, not at the end.

**Persisted formats, if D3 is "accept both".**

- Trailer: the verifier is `kitlib/verdict.py` (`_ATTEST_RE`, `BAR_NAMES`,
  `LANDING_BARS`, `format_bar_green`). Write the new form only. Parse both.
  Map old values on read (`review` to `commit`, `no-bar` to `none`). Test
  that a lane holding old-form trailers still reads as attested, and that the
  failure cap counts across a mix.
- Session-log headers: `kitlib/verdict.py` (`RED_KEYS`, `_BAR_RED_RE`,
  `_BAR_SUMMARY_RE`). Same rule.
- Work-item key: `intake.py` and `integrate.py` each hold a copy of the
  reader (`normalize_bar`, `_RETIRED_BARS`). Read `landing_stage`, then `bar`.

**Registry edits the renames force.**

- 11 design rows bind a module or symbol that is renamed: LLR-152, 154, 159,
  167, 188, 207, 231, 341, 343, 344, 368. These are traced cells; editing
  them is not a text amendment.
- Evidence cells: every renamed test function or file (D4).
- The 13 approved rows of D5: SN-005, SR-221, SR-241, LLR-207, 260, 291,
  343, 344, 368, TC-132, 375, 376, 417.

**Checks to run after each concept.** All from the worktree root.

```
python project-trajectory/scripts/trace.py --strict
python project-trajectory/scripts/check_trajectory.py --strict
python project-trajectory/scripts/check_docs.py --root . --stale
python scripts/check_resync.py
python project-trajectory/scripts/check.py --path-triggered
python -m ruff format --check project-trajectory/scripts tests
python -m ruff check project-trajectory/scripts tests
python -m pytest -q -p no:cacheprovider -n 6 <the modules the change names>
```

Then the unfiltered suite once at the end (33 to 45 minutes on this box).

**Traps this session walked into.** Each cost a failed run.

1. *One-home tests.* `test_stack_profile.py` fails any script that parses
   `docs/stack.ini` itself. Use `kitlib.config.read_stack_ini`.
2. *Exact line counts.* `test_module_size_ratchet.py` pins the code-line
   count of nine modules, in both directions. A reworded message that wraps
   onto a new line fails it. Keep such edits line-neutral; do not re-stamp.
3. *Tags and evidence must agree.* A new test carrying `Implements: TC-NNN`
   must be added to that test case's evidence cell, or
   `check_trajectory.py --strict` refuses.
4. *Byte budgets.* `CLAUDE.md` and three shipped files have stamped sizes in
   `skills/byte-budget-guard/SKILL.md`. Any edit to them needs the table
   re-stamped, and the skill's own row with it.
5. *Skill mirrors.* `.claude/skills` and `.agents/skills` are byte-identical
   copies of `project-trajectory/skills`. Copy after every edit.
6. *Dogfooded copies.* `docs/specs/README.md` must match its shipped
   template. A sweep that skips `docs/specs` breaks `test_dogfood_sync.py`.
7. *The prompt catalogue.* Editing a prompt template makes
   `project-trajectory/prompts/CATALOG.md` stale. Regenerate with
   `gen_prompt_catalog.py`; the hook checks it on every commit.
8. *A re-sync entry is required* for any change under `project-trajectory/`,
   anchored `[since <trunk base sha>]`. `check_resync.py` refuses without it.
9. *A `[product]` key cannot be appended.* Insert it under the existing
   header. Appended after another section it parses and reads as undeclared.
10. *Automated word replacement breaks grammar and over-reaches.* It turned
    "the docs/gate BAR axis" into "CHECKS axis", which was the retired dial
    and not a check. Replace by concept, and read every changed line.
11. *The box is shared.* Other projects' agent sessions run on it. The same
    test tier read 234 s and 417 s minutes apart. Never run two timing runs
    at once; prefer counts and CPU-seconds.

## 6. Functional changes, in order of value

These come from the review (README §§3, 7, 9, 11) and from the owner's
feedback since. None is made on this branch. Figures marked (reviewer) were
produced by a reviewing sub-agent and spot-checked, not recomputed.

**B1. Make the inner loop cheap and the landing deep.** The owner's first
complaint. Set `[required-checks] commit = "iterate"`. Give `landing` a
reader and run the unfiltered suite once per landing, on the staged squash.
Replace the hand-landing line in the coordinator recipes that runs the smoke
tier. Evidence: 69% of 1,489 lane commits change no source or test file and
still run 3,499 tests; a median of 10 attestations per lane (reviewer); for
the commits that do run tests, the selection's median is 111 test functions.
Depends on D6, D7. Proposed prose: README §8.

**B2. Stop one lint re-reading history.** `check_trajectory.py --strict`
takes two to five minutes; with its walk over every loop commit stubbed and
one scan computed once it took 12.9 s. The commit hook runs the same script,
so each commit pays twice. Cache the per-commit answer by commit id, or move
the report to the audit. Both files are shipped and one is in the line-count
ratchet. README §7. Until this lands, B1 saves less than it should.

**B3. Retire the smoke tier's bookkeeping.** Once commits run a selection,
the in-process tier is only the fallback. Remove `SLOW_MODULES`, `max-tests`,
`[smoke-budget]` and its roughly 900 lines of stamp history, and the nested
whole-tree collection inside `test_smoke_budget.py`. 73 commits have changed
`max-tests`.

**B4. Build a scaffold once per worker.** The `scaffold` fixture runs
`bootstrap.py` as a subprocess for each of about 500 tests, 4 to 5 s each on
this box. Copy a prebuilt one. The largest single cut to the landing checks,
and it also shrinks the canary set's 30 to 40 s.

**B5. Change the prose that only adds tests.** Nothing in the method merges
or retires a test. Proposed wording for six passages and one new rule is in
README §8. Owner ruling needed: reviewers will read it as weakening.

**B6. CI.** Jobs have a 20-minute timeout for a suite that takes 33 minutes or
more locally, and the root conftest halves the worker count even with the CPU cap
off. A review of 2026-11-05 reports no green run since 2026-10-14; this
session could not check, since `gh` is not installed. Check the Actions tab
first. Then run the iterate checks on push and the matrix nightly or on a
pull request, as the shipped template already does.

**B7. Scope the commit hook by what changed.** It runs 34 checks and about
41 interpreter launches on every commit, records-only ones included
(reviewer). `check.py` already has the `paths =` machinery.

**B8. Remove the overnight runner.** The owner's view: it was only ever for
long-running changes to this repository, and a dedicated session started
outside the repository root does that better.

| Set | What | Size |
|---|---|---|
| The launcher | `scripts/coordinator/overnight_legs.py`, `headless-leg.md`, `coordinator-relaunch.{cmd,sh}` | 773 lines; 40 test functions in 3 test files (1,217 lines) |
| The coordinator's other repo-local tools | the rest of `scripts/coordinator/`: `codex_call.py` and five small scripts | about 1,300 lines; 29 test functions in 3 test files |
| The coordinator's shipped guard | `coordinator_guard.py`, `kitlib/guard_hooks.py` | 2,036 lines; 85 test functions in 2 test files |
| Its prose | the `coordinator-cycle` skill and its recipes, `kit-builder.md` | 22,800 words; 7 test files pin it |

  The launcher is mentioned in the system requirements, the design rows and
  the test cases (four lines between them), in `docs/runtime-flows.md`,
  `docs/stack.ini`, `kitlib/provenance.py` (which recognises its commits)
  and four test modules besides its own. Removing it retires those rows,
  which is an amendment. Not sized here, because it was not traced: whether
  the session, adjudication and usage modules (`session_service.py`,
  `session_keep.py`, `session_adapters.py`, `adjudicate_brief.py`,
  `adjudicate_act.py`, `usage_ingest.py`; about 7,700 lines and 400 test
  functions) serve only this coordinator or the shipped loop too. That
  question is B9's.

**B9. Separate the kit from the machinery that builds it.** About half of
`project-trajectory/scripts` by line count is the unattended multi-agent
station and its own record-keeping, and 127 of 130 modules ship to every
adopter in one flat list (reviewer). An adopter who wants the three stated
goals needs none of it. Only 25 import edges run from the traceability core
into it (reviewer). Cut those and give bootstrap a real install profile.
This is a smaller decision than open item OI-130 and worth more: the
re-score there shows one partition winning under every objective, and none
addresses the 19 duplicated policy behaviours.

**B10. End the standing pause.** `docs/work/pause` is a one-day review hold
from 2026-09-04. Every claim since costs three commits.

**B11. Stop committing the dashboard.** `PROJECT_STATE.html` is in 2,041 of
4,717 commits, and about 95% of the files under `docs/` are records that the
link checks re-read on every run (reviewer).

**B12. Give the ratchets headroom or delete them.** The line-count ratchet
is 2,107 lines for 4 tests and has been edited in 410 commits (reviewer). It
taxes every edit and its baselines rose anyway.

**B13. Fix what the kit says about itself.** `CLAUDE.md` gives the suite as
"~10 min" (it is 33 or more) and says the lane refresh runs the full checks
in the merge slot (the lane history holds 367 commit attestations and no
landing one). `docs/gate-policy.md` contradicts `docs/process.toml` on the
approval dial (reviewer). "No commit bypasses" the hooks, while three shipped
scripts commit without them (reviewer).

**B14. Push.** Trunk is 16 commits ahead of its remote. The unsquashed lane
history is 4,586 commits ahead of its remote, whose tip is 2026-10-05. The
machine crashed on 2026-11-07. `origin/HEAD` is still `main`, last touched
2026-07-17.

## 7. Getting the template onto other repositories

The owner's goal is a template that forces interlinked documentation and
layered architecture, with hooks matched to need. The order below is this
session's suggestion for reaching a kit that can be applied elsewhere.

1. **Vocabulary** (§4, §5), so that what an adopter reads is consistent.
2. **Cheap inner loop** (B1, B2), so that working in the kit is not the
   bottleneck for everything after.
3. **Core and station apart** (B9, B8), so that an adopter installs the part
   the vision describes. This is the step that decides how much of the rest
   an adopter ever sees.
4. **Two of the three goals are the least enforced today** (README §11).
   Layering is "no import cycles" plus an ordering among five modules, and
   two of its instruments cannot see inside packages. The commit hook
   ignores the stage ladder, and formatting blocks from the first commit
   while lint and tests arrive at the seventh rung of eight. Decide what the
   kit should enforce for an adopter on day one, and make the hook do that.
5. **A first-day pass on a clean machine.** A review of 2026-11-05 simulated
   one: 183 minutes of required reading, a documented setup command that
   fails on Ubuntu, and four refused commits (reviewer, not re-run here).
6. **Then re-sync the pilots.** Two downstream repositories are evident,
   `gilbert` and `FileBackup`; FileBackup's re-sync has been owed since
   2026-10-02 and is blocked on known kit defects (reviewer).

Owner, on this order:

## 8. For the next session

- Start outside the repository root, as this session did, unless the owner
  says otherwise. The repository's `CLAUDE.md` and skills describe a workflow
  the owner has chosen not to use for this work.
- Never read `OWNER_SCRATCHPAD.md`. The repository marks it owner-only.
- Work in a worktree. Leave the primary checkout alone.
- Commit only when the owner asks. The owner allowed bypassing the hook on
  this maintenance branch; confirm before doing the same on the next one.
- The owner's decisions are on the `Owner:` lines above. An empty line means
  undecided: ask, do not assume the recommendation.
- This file and `README.md` are the whole record. The measurements behind
  them were taken in a temporary directory and are not kept.
