# Required checks by claim: an inner loop whose cost follows the change

Outside review, 2026-11-11, at trunk `7fa851f33`. Written from outside the
repository's own workflow at the owner's request: no work item was filed and
no lane claimed. It is committed on a maintenance branch with the commit hook
bypassed, at the owner's direction. The branch `proposal/test-tiers` holds a
working prototype (section 5) and a rename of three settings (section 12);
everything else here is a recommendation, section 13 included. `HANDOFF.md`,
beside this file, is what the next session works from: the decisions waiting
on the owner, the drafted glossary entries and the ordered list of changes.

A note on words. The kit called a set of checks a change must pass a "bar"
(commit bar, review bar, landing bar). This branch renames those to "commit
checks" and "landing checks", and this document uses the new words throughout,
including where it quotes text the rename touched.

## How to review this branch

The branch is 90 changed files and 5 new files, in one commit, in two parts that
can be taken or dropped separately.

| Part | Where | Size | Read first |
|---|---|---|---|
| The diagnosis and the model | sections 1 to 4 here | 10 minutes | section 1 |
| The prototype | `scripts/check_iterate.py`, `tests/canary.txt`, `tests/test_check_iterate.py`, three small edits (`pytest.ini`, `tests/conftest.py`, `[run] iterate`) | about 1,100 new lines, no shipped file | section 5, then run `run.cmd iterate` |
| The rename | 30 kit files, their 8 skill mirrors, 37 test files, about a dozen repo files | about 1,400 lines changed, most of it wording | section 12, then the two templates and the `RESYNC_PACK.md` entry |

Decisions that are the owner's, none of which this branch takes:

1. Whether a commit must pass `iterate` instead of `smoke`: one word,
   `[required-checks] commit` in `docs/process.toml`.
2. Whether a landing runs the unfiltered suite (section 9, item 3). Take it
   with decision 1 or not at all.
3. The canary set's membership (`tests/canary.txt`). Accepted as a first cut.
4. The `check_trajectory.py` history walk (section 7).
5. Amending the 13 approved rows that still use the old words (section 12).
6. The terms for the rest of the vocabulary, and whether that migration is
   its own change (section 13).

## 1. Summary

The suite is not slow because the deep run happens too often. It is slow
because the cheap run is not cheap, and it runs on every commit.

- Every commit must pass the "smoke" tier, 3,499 of 7,973 tests (44%), plus
  four lints. On this workstation, loaded the way it normally is, the tier
  took 4 to 7 minutes and the lints another 3 to 6.
- The tier is defined by what a test costs (in-process, so "cheap") and not by
  what it shows. That makes it grow with the code, and it leaves out every
  end-to-end run, so it answers neither "does my change work" nor "does the
  product still work".
- 69% of lane commits change only records and state the lints already hold.
  They run all of it anyway.
- The process only adds tests. Nothing in it merges, retires or budgets them,
  and the one cap that exists is raised by the commit that trips it.

The fix is to name each set of required checks for the claim it supports and
let its cost scale with that claim:

| Checks | Claim | Runs | Cost grows with |
|---|---|---|---|
| **iterate** | this change works, and nothing is obviously broken | the lints, beside the tests the change names and a fixed canary set | the change |
| **landing** | this work item integrates | the unfiltered suite, once, on the tree that lands | the suite |
| **release** | the kit is verified | the suite with coverage, the budget audit, the OS matrix | the suite and the matrix |

The repository already holds every part the iterate checks need: the diff
reader, the spine's module-to-test links, the test-file tags and the
`Implements:` lines. They were never joined, because `PROCESS_OPTIONS.md`
rejects test selection outright.

## 2. Measurements

Taken on the owner's 24-thread workstation while other projects' agent
sessions were running on it, which is its normal state. Wall times here move
with that load; counts do not.

| What | Reading |
|---|---|
| Tests collected | 7,973 (collection alone: 14 s) |
| Smoke tier | 3,499 tests, 44% of the suite |
| Smoke tier wall, default 50% CPU cap | 234 s |
| Smoke tier wall, cap off, box busier | 417 s |
| Repo's own quiet reading (stack.ini, 2026-10-21) | 55 s wall, 335 CPU-s |
| Smoke tier limits today | 3,550 tests, 540 CPU-s, 600 s wall; warn-only |
| Smoke tier limits when set (2026-07-23) | 349 tests, 60 s wall, about 7 s measured |
| `trace.py --strict` | 14 to 18 s |
| `check_trajectory.py --strict` | 118 to 300+ s |
| `check_docs.py --stale` | 15 to 24 s |
| `check_resync.py` | 1 to 5 s |
| Full suite, repo's own records | 16 min (10-17), 23 min (10-20), 28 to 31 min (11-03) |
| Slow tier alone, this session | 4,474 tests in 38 min |

Growth, from git history:

| Date | Test functions | Test lines | Script modules | Script lines |
|---|---:|---:|---:|---:|
| 2026-07-15 | 812 | 15,525 | 25 | 19,667 |
| 2026-08-15 | 2,384 | 60,473 | 59 | 52,681 |
| 2026-09-15 | 3,334 | 89,855 | 84 | 77,099 |
| 2026-10-15 | 4,955 | 130,006 | 119 | 107,553 |
| 2026-11-11 | 5,996 | 164,423 | 130 | 117,648 |

About 1,000 test functions a month. Since mid-September the tests grew by
75,000 lines against 40,000 for the scripts.

Where the smoke tier's time goes: 92 tests (under 5% of those with a
measurable duration) carry 45% of it, and the ten costliest modules carry
58%. Eight of those ten test the review, adjudication, planning and session
machinery, not the adopter-facing checks.

## 3. Why it got this way

**The tier is defined by exclusion.** `tests/conftest.py` marks every test
`smoke` unless its module is in `SLOW_MODULES`. A new test is in the
per-commit checks by default. `session-protocol` §3 says so and calls it the
intent.

**The cap raises itself.** 73 commits have changed the membership ceiling
`max-tests` since 2026-07-23, taking it from 450 to 3,550. The documented response to
tripping it is to raise it in the same commit
(`coordinator-cycle/references/recipes.md`, "A build whose in-process tests
take the smoke tier past `max-tests` re-stamps the ceiling in that commit").
Builders are told not to reduce the count ("never to fold parametrized cases
into one looping test to stay under the smoke tier's `max-tests`").

**The time limit was loosened when it kept biting.** A 60 s wall budget
(WI-281) needed three further re-tiers to hold (WI-496, WI-652, WI-869) and
was then replaced by 540 CPU-seconds, reported only and judged by
`run.cmd audit` (WI-940). Two reviewers read the handoffs since: they carry
"judge at the next audit" forward and record no audit.

**Selection was ruled out, so the tier is the only cheap layer.**
`PROCESS_OPTIONS.md`, "Phase cadence": *Test-impact selection ("run only the
relevant tests") is rejected: a missed transitive dependency passes silently
and the coverage floor breaks.* Both reasons hold for what a landing must pass
and neither holds for an inner loop. The deep run still happens, so a miss is
caught later, not never. Coverage is only judged at the full tier. And the smoke
tier is itself a subset that misses dependencies: it drops the
subprocess-driven modules, 142 of 275.

**The checks run on commits that cannot break a test.** `recipes.md`: "Run
the commit checks on every commit, docs-only ones included." Replaying the last
1,500 commits of `archive/lanes`: 1,027 of 1,489 (69%) change nothing but
records and lint-held state.

**The process adds tests and never removes them.** At least one test case per
requirement row, a failing test before each behaviour, a regression test for
every accepted review finding, in-process "pins" for every module moved to
the slow set, a hook warning for a fix with no test delta, and per-module
coverage floors. "Nothing is deleted or weakened" appears in the tier
comments as a virtue.

**One lint re-reads history on every run.** See section 7.

## 4. The model

Three sets of required checks, each named for its claim. A green is only ever
quoted with the checks that produced it.

**iterate** answers two questions in one run.

- *Does the change work?* The tests the change names: a changed test file;
  the tests that import, load or run a changed script; the tests the spine
  links to it; the tests that name a changed non-Python file.
- *Is the product still alive?* A fixed canary set, one end-to-end happy path
  per capability, capped by count. It is chosen for what it shows, so it
  includes the bootstrap, harness and hook runs the smoke tier excludes.

A change made only of records runs the lints and no test. A change the
selection cannot be honest about (pytest.ini, a conftest hook) widens to the
in-process tier and says so. Every path the selection could not map is
printed.

**landing** is the unfiltered suite, once per work item, on the tree that lands.
This is where a dependency the iterate checks missed is caught. Count those
catches: that number is the measure of whether the selector is good enough,
and the response to a miss is to improve the selection, not to widen the
default.

**release** is the suite with coverage, `run.cmd audit`, and the CI matrix.

What makes this hold where the smoke budget did not:

1. The iterate checks have no number to re-stamp. Their focus is derived from
   the diff, and their canary set is a count cap with a one-in, one-out rule.
2. Nothing asks an inner-loop run to be a proof. The smoke tier kept growing
   because every omission from it read as a risk.
3. The deep run moves to a point where it happens once.

## 5. What this branch adds

Two separate things. The prototype below is repo-local and changes no shipped
kit file. The rename in section 12 does change shipped files, and carries its
`RESYNC_PACK.md` entry.

| File | What |
|---|---|
| `scripts/check_iterate.py` | The iterate step: reads the change, selects, prints its plan, runs the lints beside one pytest run |
| `tests/canary.txt` | The canary set, 16 nodes, one per capability |
| `tests/conftest.py` | Marks listed nodes `canary`; `CANARY_MAX = 20` |
| `pytest.ini` | Registers the `canary` marker |
| `docs/stack.ini` | `[run] iterate`, so `run.cmd iterate` works |
| `tests/test_check_iterate.py` | 21 in-process tests of the selection and the canary cap |

Not changed by the prototype: `[run] smoke`, what a commit must pass (still
`smoke`), `SLOW_MODULES`, the budget. Every existing check behaves as before.

Checked before the commit, with the primary checkout's interpreter.

*The prototype alone, before the rename:*

- `python scripts/check_iterate.py` on the branch's own change, which widens
  because it edits `pytest.ini`: the four lints green, and the in-process
  tier with the canary set 3,530 passed, 3 skipped.
- The commit hook's floor, run by hand without committing
  (`check.py --path-triggered`, then its 14-step `--run-steps` list): PASS.
- The slow tier (`-m slow`): 4,447 passed, 26 skipped, 1 failed, in 38
  minutes. The failure was this branch's own:
  `test_stack_profile.py::test_the_stack_ini_parse_is_one_home` caught
  `check_iterate.py` parsing `docs/stack.ini` with its own `ConfigParser`
  where the kit has one reader. Fixed to call `kitlib.config.read_stack_ini`.

That failure is a fair specimen of what the iterate checks cannot see. No test
names `check_iterate.py` except its own, so a focused run stays green; a
census that scans every script found it. One escape in one change, caught
by the deep run, is the arrangement working as section 4 describes.

*The whole branch, after the rename:*

- The unfiltered suite: 7,997 passed, 29 skipped, 1 failed, in 33 minutes.
  The failure was the exact line-count ratchet: the reworded messages made
  `agent_loop.py` four lines longer. Made line-neutral, not re-stamped.
- After that fix and the last wording changes, the modules they touch were
  re-run: 748 passed and 1 skipped across 14 modules, then 184 passed and 1
  skipped across the 9 that read the live test-case registry. The whole
  suite was not repeated after those last edits.
- `trace.py --strict`, `check_trajectory.py --strict`, `check_docs.py
  --stale` and `check_resync.py`: green on the final tree. The re-sync check
  accepts the new entry.
- The hook's path-triggered checks (complexity, duplication, readability):
  PASS. `ruff format --check` and `ruff check`: clean.
- The hook's 14-step floor: 11 pass. `cli-reference`, `interface-reference`
  and `trajectory-map` report their generated views stale, because help
  text, contract text and a dashboard panel were reworded. A work branch
  does not commit generated views; they regenerate at the trunk step. The
  stand-down that covers a claimed lane does not cover this unclaimed
  branch, which is why the steps fire here.
- The second escape of the same kind as the first: four tests added during
  the rename carried their `Implements: TC-` tags, and
  `check_trajectory.py --strict` refused until the two test cases' evidence
  cells named them. They now do (TC-382, TC-421).

How the selection works, in the order it applies:

1. Records (`docs/reviews`, `docs/plans`, `docs/log.d`, handoffs, and so on)
   and lint-held state (`docs/work`, the generated views) select nothing.
2. A changed test file selects itself.
3. A changed script selects the tests that name it (an import, a
   `load_script` call, a `<name>.py` literal, directly or through a shared
   helper) and the tests `kitlib.spine.module_tests` links to it, which is
   the map `trace.py --tests-for` prints. A test file that lists more than
   12 script names is an inventory (`test_bootstrap.py` lists 94), and its
   list does not count.
4. A script whose tests hold more than 150 test functions is narrowed by
   the definitions the diff touches: its own `test_<module>*.py` files, the
   tests that mention a touched definition, and the evidence of the test
   cases that verify the design rows (`LLR-`) on that definition's
   `Implements:` line. A change outside every definition keeps the whole
   set.
5. A changed non-Python file selects the tests that name it.
6. `pytest.ini`, the coverage and requirements files, and a conftest hook
   widen to `-m "smoke or canary"`.

## 6. Does the selection pick the right tests

Replayed against history, on today's test tree.

**Individual lane commits** (1,489 commits of `archive/lanes`, each one a
real inner-loop step):

| Outcome | Commits | Share |
|---|---:|---:|
| Runs no test: records or lint-held state only | 1,027 | 69% |
| Focused on the tests the change names | 441 | 30% |
| Canary set only: no test names the change | 19 | 1% |
| Widens to the in-process tier | 2 | 0.1% |

For the 460 commits that run tests, the focused selection (before the 16
canary nodes are added) is:

| | Test functions | Share of the suite |
|---|---:|---:|
| Median | 111 | 1.8% |
| 75th percentile | 664 | 11.0% |
| 90th percentile | 1,728 | 28.7% |

63% of them select 300 test functions or fewer, and 88% select 1,500 or
fewer. Today each of the 1,489 runs 3,499 tests. Narrowing a shared module
by the definitions touched is what moves the upper end: without it the 75th
percentile is 1,426 and the 90th is 2,774.

Of the 167 commits that changed both source and tests, the selection made
from the source paths alone included 91% of the test files the commit
changed, and all of them in 75% of commits. The file missed most often is
`test_import_layers` (12 times), the import ratchet.

**One-definition changes, timed.** The test run alone, no lints, on the same
loaded box under the default 50% CPU cap. Each change was described to the
selector (the file, and one function whose body it touches) and the command
it produced was run. All four passed.

| Change | Test files naming the module | Selected, canary included | Wall |
|---|---:|---:|---:|
| `check_figures.py`, `main` | 2 | 43 tests | 43 s |
| `agent_common.py`, `interpreter_version` | 46 | 36 tests | 30 s |
| `trace.py`, `_cmd_tests_for` | 79 | 278 tests in 10 files | 192 s |
| `held_status.py`, `committed_status_moves` | 6 | 111 tests in 4 files | 201 s |

The smoke tier, which each of these runs today, took 234 s and 417 s in the
same session, before the builder's "affected modules" on top.

The two slow rows are slow for a different reason than breadth. Their own
tests build a scaffold or a git repository per case, and 30 to 40 s of every
row is the canary set doing the same. Selection fixes how many tests run; it
does not fix what one such test costs. That is item 5 of section 9.

Trying every top-level definition in the largest shared modules, one at a
time: a one-definition change in `intake.py` selects a median of 153 test
functions (90th percentile 334) of the 1,386 that name the module;
`check.py` 270 (387) of 2,160; `agent_loop.py` 265 (492) of 1,198;
`bootstrap.py` 78 (161) of 1,152.

What none of this shows: a regression in a test the change does not name.
Only the landing checks' escape count can measure that, which is why section 4
asks for it.

## 7. One lint dominates the commit checks, and it is re-reading history

`check_trajectory.py --strict` took between 118 s and over 300 s across
five runs, against 1 to 24 s for each other lint. Profile of a 159 s run:

| Share | What |
|---:|---|
| 56% | `loop_held_status_findings`: visits every loop commit in history (235 today), about five git calls and two registry parses each, 1,180 git processes in all |
| 14% | `arch_inventory`: the same scan of all 130 modules, run 5 times |
| 10% | `tc_tag_findings`: parses every test file |

The first is an advisory that never changes the exit code, and its answer
for a given commit cannot change: the function judges each commit "against
the dial in its own tree". It still runs in full every time, and it grows
with every loop commit.

With that walk stubbed and `arch_inventory` computed once, the same run took
**12.9 s**. Two changes, both behaviour-preserving:

- cache the per-commit result by commit id, keyed also on the judging
  code's own digest, somewhere under the git directory; or move the report
  to `run.cmd audit`;
- compute the inventory once per `main()`.

The commit hook pays the same cost again. Its floor runs this script as the
`trajectory` step: 106 s and 121 s in two runs here, the longest of its 14
steps by a factor of two and a half. So every commit, records-only ones
included, waits about two minutes in the hook and then again in the commit
checks.

Not done here: both files are shipped kit scripts, one is in the exact
line-count ratchet, and the cache's home is the owner's call. Until this
lands, an iterate run is lint-bound at two to five minutes however small
the change.

## 8. Proposed text

These are the passages that create the behaviour. None is applied on this
branch.

**`project-trajectory/PROCESS_OPTIONS.md`, "Phase cadence".** Replace the
sentence beginning "Test-impact selection" with:

> Test selection ("run the tests this change names") is the **inner loop**,
> never evidence for a landing. A selection can miss a dependency, so a green from
> it supports one claim only: this change works. The unfiltered suite still
> runs before a change lands, which is where a miss is caught, and coverage
> is judged there. A project whose suite is slow adds a selected run and a
> small fixed canary set per commit; it does not grow its smoke tier.

**`session-protocol` §3, "End green".** Replace the paragraph from "It must
pass before each commit" through "re-stamp deliberately, reason in the log)"
with:

> Three sets of required checks, each named for the claim it supports. Quote
> a green with the checks that produced it.
>
> - **iterate** (`run.cmd iterate`), before each commit: the lints, beside
>   the tests this change names and the canary set. A change of records
>   alone runs no test. It prints what it could not map; that is information,
>   not a failure.
> - **landing**, once per work item, on the tree that lands: the unfiltered
>   suite. A red here on something iterate passed is recorded as an escape.
> - **release**, at phase close: the suite with coverage, and `run.cmd
>   audit`.
>
> The canary set (`tests/canary.txt`) is fixed-size. A new entry past the
> cap replaces one. Do not run the unfiltered suite inside a build round.

**`CLAUDE.md`, "Self-test before claiming done".** The same three in three
sentences, with the stale figures removed ("~10 min on a quiet box" is
now 28 to 31 min; "the lane refresh runs the full bar … in the merge slot"
describes a path with no run recorded since 2026-09-05).

**`recipes.md`.** Replace "Run the commit checks on every commit, docs-only
ones included" with "A commit of records alone runs the lints; `run.cmd
iterate` decides, do not decide by hand." Delete the instruction never to
fold parametrized cases, and the instruction to re-stamp `max-tests` in the
tripping commit.

**`kit-builder.md`.** Replace "Run your affected modules and the whole smoke
tier at `-n 2`" with "Run `run.cmd iterate`."

**`coordinator-cycle`, the convergence map.** After "maps every accepted
finding to a regression test that fails on the pre-fix code", add: "A
finding extends an existing test's cases before it adds a test function. A
finding in a guard for a case no caller can produce is answered by removing
the guard."

**A rule that removes tests.** The process has none. Proposed, for
`PROCESS.md` beside its pairwise-combination rule:

> A test earns its place by the behaviour it would catch breaking. A test
> that pins how a refactor was carried out (a verbatim move, a retired name
> staying retired, a split keeping its line count) is removed when the work
> item that needed it lands. A test file whose cases differ only in input
> is one parametrized test.

## 9. Changes this branch does not make, in order of value

Which event reads which setting today, because what a commit must pass and
what a landing must pass are separate mechanisms, and only the first is a
declared setting:

| Event | What decides its tests | What runs today |
|---|---|---|
| A lane commit (`integrate.py attest`) | `[required-checks] commit` in the lane's own `docs/process.toml`, which names a line under `[check-suites]` in its `docs/stack.ini`; then the row's derived test files | the lints, the whole smoke tier, the derived files |
| A landing through the merge slot (`integrate.py refresh`, `integrate`) | `check.py --tier all --trunk-lane`; it reads no declared setting | not in use: the lane history holds 367 `bar=review` attestations and no `bar=landing` |
| A landing by hand (`git merge --squash`), which is every recent one | the literal `run_menu.py smoke` line in `recipes.md` | the lints and the smoke tier on the staged squash |
| Leg close-out | `recipes.md` | the unfiltered suite, in two halves, when code changed |

So item 1 below changes the first row only. A landing keeps running the smoke
tier until item 3 changes the recipe line or the merge slot is used again,
and the two belong together: once a lane commit runs a selection, the landing
is the only place a missed dependency can be caught.

1. **Set `[required-checks] commit = "iterate"`.** One word in
   `docs/process.toml`; `[check-suites]` in `docs/stack.ini` already declares
   the suite. `integrate.py attest` already runs the named suite and then the
   row's derived test set; today the first half is the whole smoke tier. The test reviewer counted a median of 10 attestations per lane.
2. **The two `check_trajectory.py` fixes** in section 7.
3. **Run the unfiltered suite once per landing**, on the staged squash, and
   record it with the existing `Bar-Green:` trailer as `bar=landing`. Then
   the per-leg "full suite in two halves" run goes.
4. **Retire `SLOW_MODULES`, `max-tests` and the stamp history.** Once the
   iterate checks are what a commit must pass, the in-process tier is only the
   widening fallback and needs no membership ceiling. That removes about
   390 lines of `tests/conftest.py`, about 900 comment lines of
   `docs/stack.ini`, a nested whole-tree collection inside every smoke run
   (`test_smoke_budget.py`), and the re-stamp commits.
5. **A scaffold built once per worker.** The `scaffold` fixture runs
   `bootstrap.py` as a subprocess for each of about 500 tests, at 4 to 5 s
   each on this box. `PROCESS_OPTIONS.md` records this as "not-yet-built".
   The `hooked_checkout` template copy in `tests/conftest.py` is the
   pattern. This is the largest single cut to the landing checks.
6. **CI by moment**, as the shipped template already does: the iterate
   checks on push, the matrix nightly or on a pull request. The root conftest
   halves xdist workers even with the CPU cap off, so a 4-core runner gets
   two workers for a suite that takes half an hour on twelve; the rolling
   review of 2026-11-05 reports no green CI run since 2026-10-14. Worth
   checking in the Actions tab before anything else here.
7. **Path-scope the commit hook** the same way. By the hooks reviewer's
   count it runs 34 checks and about 41 interpreter launches on every
   commit, records-only ones included.

## 10. Risks

- **A missed dependency.** Certain to happen sometimes. It is caught at the
  landing checks. If the escape count is high, the selection is too narrow for
  that module: raise `HUB_FUNCTIONS` so it is not narrowed, or add it to the
  widening list.
- **Narrowing by definition name** is the weakest link. A private helper no
  test mentions selects only the module's own test files. The plan prints
  each narrowing so it can be judged.
- **The canary set is a first cut**, chosen by one reader from test names.
  Its membership should be the owner's.
- **Static naming misses dynamic loads.** A test that builds a script name
  at run time is invisible. A recorded map (which files each test opened,
  taken during a landing run) would be exact; it is a second step, not a
  prerequisite.

## 11. Beyond the tests

Findings from the same review that bear on the test problem without being
part of it. Counts marked (reviewer) were produced by a reviewing sub-agent
and spot-checked, not recomputed.

**Half of what ships is not the product the vision describes.** By line
count, about 51% of `project-trajectory/scripts` is the adopter-facing core
(registries and trace, architecture map and doc checks, the gate harness,
the dashboard, the scaffold). About 49% is the unattended multi-agent
station and the records it keeps about itself: sessions, lanes, merge,
mint, verdicts, approvals, attestation (reviewer). 127 of 130 modules ship
to every adopter in one flat list; the bootstrap profiles trim document
sections only. Of the 92 substantive work items landed since 2026-10-05,
72 changed that station and 12 changed something an adopter not running it
would notice (reviewer's classification). The ten costliest smoke modules
all test it.

This is why the suite grows faster than the kit: the process generates
machinery, the machinery needs tests, and the tests slow the process that
generates it. Three earlier reviews reached the same conclusion
(2026-09-05, 2026-10-11, 2026-11-05) and the script tree grew from 82 to
130 modules between the first and now.

A core/station split is a smaller decision than OI-130 and worth more to
the test problem. Only 25 import edges run from the core into the station
(reviewer); cutting them and giving bootstrap a real install profile would
let the core be tested, shipped and reasoned about alone. The re-score
shows P5 winning under every objective, and no candidate partition
addresses the 19 duplicated policy behaviours.

**Of the three stated goals, two are the least mechanised.**

- *Layered architecture.* The enforced rule is "no import cycles" plus an
  ordering among five lifecycle modules. 125 of 130 modules have no declared
  layer. Two instruments are blind to packages: the view rule matches
  `traj_*` and `gen_*` on the dotted name and so skips everything under
  `rendering/`, and the seam check resolves imports by bare stem and so
  skips `kitlib/` (reviewer; consistent with HEAD's own handoff). This
  review's import probe found the practical consequence: the reverse
  dependency closure of a typical module reaches 75% of the test suite, so
  "what could this change affect" has no useful structural answer, which is
  why the selector in section 5 works from names and not from the graph.
- *Hooks that drive the right level of capability.* The commit hook ignores
  the stage ladder and runs the same 34 checks on every commit. The gate
  plan is graduated, but inverted for a new adopter: formatting blocks from
  the first commit, while lint and tests join only at the seventh rung of
  eight. The agent-side hooks ship as inert examples, and the committed
  `.claude/settings.json` is empty (reviewer).

The same links that demand tests can select them. That is the stated vision
applied to testing, and it is what `check_iterate.py` does with the spine.

**Cost outside the test run.**

- `docs/work/pause` is a one-day review hold from 2026-09-04. It is still
  there, so every claim costs three commits: unpause, claim, restore
  byte-identical.
- `PROJECT_STATE.html` is committed in 2,041 of 4,717 commits.
- `docs/` holds about 5,000 files, 95% of them records, and the link and
  reference checks parse all of them on every run (reviewer).
- `docs/status.md` reports 1,141 delegated decisions awaiting the owner's
  review.

**Unpushed work.** Trunk is 16 commits ahead of `origin/refactor_again`.
`archive/lanes`, the unsquashed lane history, is 4,586 commits ahead of
its remote, whose tip is dated 2026-10-05, so five weeks of it exist on
this machine only. The handoffs
record a machine crash on 2026-11-07. `origin/HEAD` is still `main`, last
touched 2026-07-17.

## 12. Three settings were renamed

Done on this branch at the owner's direction, after the review above. The
reason is in `docs/process.toml`'s own header: that file is the one home for
policy dials, and `docs/stack.ini` is the product toolchain, "not a process
dial". `[bars] review` was a process dial in the toolchain file, under a word
the shipped glossary never defines.

| Was | Is | File |
|---|---|---|
| `[bars] review = <shell line>` | `[required-checks] commit = "<suite>"` | `docs/process.toml` |
| | `[check-suites] <suite> = <shell line>` | `docs/stack.ini` |
| `[bars] red_mark` | `[product] expected_failure_marker` | `docs/stack.ini` |
| `[build] red_rounds_max` | `[build] stop_lane_after_consecutive_commit_check_failures` | `docs/process.toml` |

What each is, in plain words:

- **`[required-checks] commit`** names the set of checks every commit on a
  work branch must pass. The policy file says which; `[check-suites]` in the
  stack file says how this stack runs it.
- **`[product] expected_failure_marker`** is the text the test framework uses
  to mark a test that is expected to fail. New tests go in under it before
  the code that makes them pass, and none may remain at a landing.
- **`[build] stop_lane_after_consecutive_commit_check_failures`** is the
  number of consecutive build rounds whose commit checks fail before the
  worker stops and the lane is closed partial. It never counted review
  rounds, which the old name suggested.

Three choices made along the way:

- **The suites live in `[check-suites]`, not `[run]`.** In this repository
  `[run]` is an actions menu, but in the shipped template it is the adopter's
  product launch menu (`serve`, `iso`), so check commands do not belong there.
  Here each suite's line still points at a run-menu action, so the command
  keeps one home.
- **Only `commit` is declared.** `landing` and `release` were proposed and are
  not in the table, because nothing reads them: the merge slot runs
  `check.py --tier all` by construction, and a setting no reader enforces is
  the kind this repository has learned not to ship. They belong with the
  change in section 9, item 3, which gives `landing` a reader.
- **The old names are refused, never read.** A `[bars]` section is ignored,
  and the refusal says so when it is still declared. A `[build]
  red_rounds_max` still declared is refused at preflight naming the new key:
  read as absent it would silently restore the shipped 3.

The shipped glossary now defines the terms, in a new Checks section, and
says which earlier word each replaces. Its existing entry for "landing" is why
the checks before a lane reaches trunk are "landing checks", not "merge
checks".

The words followed, in prose, comments, messages and tests: "commit bar" and
"review bar" read "commit checks", "landing bar" reads "landing checks", "gate
bar" reads "gate checks", "red mark" reads "expected-failure marker".

**Left as they were, on purpose:**

- *Persisted names.* The trailer `Bar-Green: ... bar=review`, the verb
  `attest --bar review`, the session-log headers `# bar-red:` and
  `# bar-summary:`, and `EXIT_RED_CAP`. The lane history holds 367 of the
  trailers, and a lane in flight must keep reading. Renaming them means a
  reader that accepts both forms.
- *Python names a requirement row binds.* `kitlib/red_mark.py`, `Bars`,
  `read_bars`, its `.review` and `.red_mark` fields, `kconfig.red_rounds_max`
  and the test files named for them. `trace.py` refuses a design row whose
  symbol does not bind, so renaming these means editing those rows.
- *Thirteen approved rows whose text uses an old word:* SN-005, SR-221,
  SR-241, LLR-207, LLR-260, LLR-291, LLR-343, LLR-344, LLR-368, TC-132,
  TC-375, TC-376, TC-417. Changing approved text is an amendment, which is
  the adjudication step's to mint, not an edit to make outside it.
- *The bare word.* "Bar" alone still appears on 109 lines of shipped prose
  and templates outside the re-sync history: 32 in the coordinator's recipes,
  and many in its plain sense of a threshold. In the two config templates it
  survives only inside the trailer's name and a note about a retired
  spelling.
- *Records and generated views.* Reviews, logs, plans, handoffs and
  `docs/status.md` keep the words they were written in.
  `docs/cli-reference.md`, `docs/interface-reference.md` and
  `PROJECT_STATE.html` regenerate at the trunk step, as for any lane.

**What the two-file declaration costs,** from reworking the test fixtures:

- A `[product]` key cannot be appended to a file the way a `[bars]` block
  could. A second `[product]` header does not parse, and a key appended after
  some other section lands in that section silently and reads as undeclared.
- One declaration is now two staged files, so a lane that changes what its
  commits must pass stages both.
- The ways it can be undeclared roughly doubled: the attest refusal table
  went from 5 cases to 12, since the name, the suite's line and the retired
  section can each be wrong on its own.

An adopter meets all three once, at the re-sync. The entry in
`RESYNC_PACK.md` gives the four hand edits.

## 13. The rest of the vocabulary

The owner's preference is one word for one thing across the board, in
agreement with the glossary. Section 12 does that for the settings and the
compound terms. What is left is larger than it looks, because the two old
words each name several different things:

| The thing | Today's words | Where |
|---|---|---|
| The record in a commit that checks passed | `Bar-Green:`, `bar=review`, `bar=landing`, `bar=no-bar`, `attest --bar review`, `BarAttestation` | commit trailers (367 in the lane history), one CLI flag, code |
| The record that a run failed | `# bar-red:`, `# bar-summary:`, `red_rounds`, `red_record`, `EXIT_RED_CAP` | session-log headers, code |
| The reader of the two declared values | `kitlib/red_mark.py`, `Bars`, `read_bars`, `.review`, `.red_mark` | code, and the design rows that bind those names |
| The stage a work item pins its landing checks to | the `bar` key | 31 archived work-item files, code |
| The retired stage dial | `sr_bar`, `maturity_bar`, `STAGE_BAR`, "bar axis", "rung bar", `DevBar-*` | readers of retired spellings, the dashboard |
| A test case not approved though the work it verifies is closed | "red TC", `red_tc_census`, `parse_red_tc` | the gap census and its adjudication brief |
| A failing run, in general | "red", "goes red", "a red bar" | prose, comments, test names |
| A threshold, in plain English | "raise the bar", "the shipped bar" | prose |

Counted in the scripts and tests alone: 219 distinct names carry one of the
two words, 2,709 occurrences. Shipped prose and templates hold the bare word
on a further 109 lines, and 13 approved rows use an old word in their text.

That is a vocabulary migration, not a rename, and the glossary is where it
starts: one entry per row of the table above, each saying which word is kept.
Three of those rows change a persisted format, so their readers have to
accept both forms for as long as old records and lanes in flight exist.
Recommended as its own change, after the terms are agreed, so that this
branch stays reviewable.
