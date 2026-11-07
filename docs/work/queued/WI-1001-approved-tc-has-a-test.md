+++
id = "WI-1001"
title = "An approved automated test case with no tagged test is a strict finding, so an approved chain cannot stand undelivered with every bar green"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/specs/WI-1001.md"
needs = ["WI-997", "WI-1000", "WI-999"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Context

Filed by hand on 2026-11-05 (attended), routed by OI-127's ruling. See the
spec of record for why. One deliverable, anchored on SR-157.

It needs WI-997, because with no tags every TC would read as untested. It
needs WI-1000 and WI-999, because TC-165 and TC-166 hold debt evidence and no
tag, so each must have a declared test or have retired before this check can
land green. Debt evidence exempts nothing: a note in the cell is not a test,
and no exception mechanism is added. OI-129 holds both rows, so this row
waits until it is ruled and they close.

The scope critique's two questions are settled here: a case whose evidence
names a debt row reads as any other untested case, and the window where a
case is approved before its test exists is the sequence in `## Trust`.

The architectural delta. `tc_tag_findings` gains one finding value,
`<TC>: no test declares it`. The value depends on a case's `status` and
`automated` cells and on the tag set `gen_arch_map.read_test_tags` returns.
The two cells are new inputs to that output, from rows the function already
loads. The stage is not an input: severity stays `--strict`, which each bar
chooses as it does today. The existing seams suffice: IF-131 for the tag read,
IF-263 for the findings (its data line names the new value at intent), and
IF-009 for the exit code. No new state, boundary, file, dial or reader is
added.

## Done-when

- [ ] An Approved TC with `automated = "Yes"` and no test declaring it is a
      WARN, and an ERROR under `--strict`, reading `<TC>: no test declares
      it`, by the ruling in `## Trust`.
- [ ] Severity follows the sequence in `## Trust`, reusing the WI-997
      finding's gating: no new state, dial or allowance.
- [ ] TC-035's `automated` cell reads `No`. It is the Analysis case over
      SR-114, its method is reading the CI matrix result, and no test can
      declare it. `automated` is a traced cell, so this owes no sitting.
- [ ] It lands green on trunk: 0 findings, with no exception. TC-165 and
      TC-166 each have a declared test or have retired, through WI-1000 and
      WI-999.
- [ ] The text that reads otherwise changes with it: `PROCESS.md` §3, the
      test-file tag paragraph of `docs/registry-machinery-reference.md`, the
      module docstring of `check_trajectory.py`, and `trace.py`'s
      `Automated=Yes` schema message, which offers a script path or a
      procedure link.
- [ ] Regressions name each arm. Temporal arms: a Drafted case holding the
      `(owed by the tests commit)` note reads no finding; a case tagged while
      Drafted stays clean when it flips to Approved; an Approved case with no
      tag warns in a plain run and errors under `--strict`; and in a
      bootstrapped scaffold the same case warns and exits 0 at `DevStg-Tests`,
      fails at `DevStg-Impl`, and is clean once tagged. Input arms: each row
      of the ruling's table in `## Trust`.
- [ ] RESYNC entry. The finding reaches adopters through the kit-owned
      `scripts/trajectory_arch.py`, so the entry is owed and is a forced
      migration, past the earlier entry's "no second one follows". It states
      the sequence in `## Trust`, and what to do with each case the finding
      names: tag a test, or set `automated = "No"` on a human procedure.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Trust

This row gives two files authority over a gate. A test file's tags and a TC
row's `status` and `automated` cells together decide a finding that fails
`check_trajectory.py --strict`, and through it each bar under Consumers.
Guards follow `project-trajectory/PROCESS.md` §3, "When a guard is owed": both
producers are files people and models write, so reading them is guarded, and
the existing readers already do that. This row adds no second reader and no
new validation.

**Producers.**

- **Test files under `[paths] tests`.** A builder or a person writes them in
  a commit; no kit script does. A commit the hook refuses leaves no tag on the
  branch, which reads as no declaration. A tag in the wrong place or form is
  refused as `misplaced` or `malformed`. A partial file that will not decode
  or parse is refused as `unreadable`.
- **The TC registry, `docs/test/test-cases.toml`** or its legacy CSV carrier.
  A person or a model writes the rows; `gen_cases.py` only prints Drafted rows
  to paste. `status` reaches Approved through the act commit here, and through
  a reviewed Status-change commit at an adopter. A failed act leaves no commit,
  so the committed row stays Drafted. A carrier that does not parse, or two
  carriers at once, stops the read in `spine_carrier`.

**Consumers** (found by grepping `tc_tag_findings`, `read_test_tags`,
`check_trajectory.py` and the `trajectory` step across
`project-trajectory/scripts`, `project-trajectory/hooks`,
`project-trajectory/ci`, `scripts` and `docs/stack.ini`).

| Consumer (path) | Reads | Effect |
|---|---|---|
| `project-trajectory/scripts/trajectory_arch.py` `tc_tag_findings` | tags, TC rows | owns the ruling; the one new line of output |
| `project-trajectory/scripts/gen_arch_map.py` `read_test_tags` | test files | unchanged; the one tag reader |
| `project-trajectory/scripts/check_trajectory.py` `main` | the finding list | unchanged: WARN plain, ERROR under `--strict`, beside the WI-997 finding |
| `project-trajectory/scripts/check.py` `trajectory` step | `docs/stage` | unchanged: adds `--strict` from `DevStg-Impl`; `_step_stage` keeps a `--run-steps` run with no `--stage` plain |
| `project-trajectory/hooks/pre-commit` | that step, with no `--stage` | unchanged: WARN, never a refusal |
| `project-trajectory/scripts/integrate.py` `_run_bar` and `attest` | `check.py`, or `[bars] review` | unchanged: a strict finding is a red bar |
| `project-trajectory/ci/` workflow template | `check.py` | unchanged: strict from `DevStg-Impl` |
| `docs/stack.ini` `[run] smoke` and `trajectory` | `check_trajectory.py --strict` | unchanged: strict at every bar in this repo |
| `project-trajectory/scripts/review_set.py` `_tags` | tags, TC rows | unchanged: it does not read this finding. Its gap for an untagged case is the same fact, read for a row's scope |

**Ruling.** One ruling, owned by `tc_tag_findings`; every other consumer takes
its output. A case is eligible when `status` reads Approved or Founded
(`kitlib.spine.is_approved`, `is_founded`) and `automated`, stripped and
case-folded, equals `yes`, which is `trace.py`'s reading. It binds to the tree
the check runs on, and reads declarations only: a test's outcome stays the
harness's answer, so a tagged test that is still strictly red counts.

| Input state | Reading |
|---|---|
| no TC registry, or no tests root | vacuous, the WI-997 guards unchanged |
| a registry that cannot be read | the run stops in `spine_carrier`, as now |
| a `-000` row | not loaded |
| a Drafted case | not eligible; the WI-997 equality check still holds it |
| `automated` anything but `yes` (`No`, blank, an absent column, another word) | not eligible; `No` and blank stay the release checklist's |
| eligible, with a tag | clean |
| eligible, no tag, an `Evidence` part in a file refused as `unreadable` | no finding here: the refusal already names that file at the same severity |
| eligible, no tag, any other cell: a note, empty, a whole-file part, a part outside the tests root, a path the tree lacks | `<TC>: no test declares it` |
| a misplaced or malformed tag | no declaration: the tag's own finding, and this one when it was the case's only tag |

A part under the tests root with no tag also reads `evidence without a tag`,
and one tag clears both.

**The sequence.** The finding has no stage input, so each checkpoint below is
the existing `--strict` choice. Nothing here weakens the final requirement:
each case ends tagged, or the bar stays red.

| Checkpoint | Case | Finding and severity |
|---|---|---|
| Lane, intent commit | Drafted, note in `evidence` | none |
| Lane, tests commit, before the act | Drafted, tag and part | none |
| Lane, the act | Approved, tagged | none: a lane's ordinary order never meets the finding |
| This repo, an act ahead of its tests (out of order) | Approved, no tag | ERROR at the next `run.cmd smoke`, cleared by the tag |
| Adopter, below `DevStg-Impl`, TCs signed in batches | Approved, no test | WARN from `check.py` and the hook; exit unchanged |
| Adopter, the commit approving the last Drafted case | Approved, no test | WARN from the hook, so it commits; `derive_stage` now reads `DevStg-Impl` |
| Adopter, at `DevStg-Impl` or later | Approved, no test | ERROR from `check.py`, so CI, `[bars] review` and `_run_bar` are red; a plain commit stays WARN |
| Adopter, once a tagged failing test lands | Approved, tagged | none |

The strict reading is repo-wide, as the WI-997 finding's is. So at an adopter
a lane cannot go green by tagging only its own cases. The supported route is
`PROCESS.md` §4's test-first order taken up front: the first work at
`DevStg-Impl` lands a failing test, with its tag and `Evidence` part, for
every approved automated case. `docs/stage` is the minimum over the phases
that have earned a rung, so a phased adopter meets the ERROR when its last
such phase reaches `DevStg-Impl`.

**Bound.** The promise reaches what supported workflows and the kit's own
routes produce (`project-trajectory/PROCESS.md` §6, "Review threat model").
It says a test declares the case, never that the test verifies it: a tag that
misstates its test is a review's to catch. `[checks] trajectory_check = false`
turns the whole check off, as it does today.
