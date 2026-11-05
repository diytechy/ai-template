+++
id = "WI-997"
title = "This repository's test files carry their test-case tags, seeded from the evidence cells, and a strict finding holds tags and evidence cells equal until the evidence column is generated"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages"
needs = ["WI-994", "OI-125"]
buildtier = "medium"
safety_class = "ordinary"
planmode = "single"
priority = 5
+++

## Context

The tag-migration row WI-994's Migration section splits out, filed before
WI-994's claim (its scope critique's S1 finding, adopted). "Row 1" below is
WI-994, "row 2" WI-995. Row 1 ships the tag grammar and its reader and tags
nothing. This row tags this repository's test files and holds the two homes of
one fact equal: OI-125 Q1 ruled (a) on 2026-11-03 that test-file tags and TC
evidence cells are checked equal as a strict finding, the check retired when
item 5 generates the evidence column. Row 2 needs this row: it refuses a
partial set, and with no tags every TC in scope reads as untagged.

**Measured** (row 1's Context, trunk `c57796e63`, and 2026-11-04 on
`b0a0026b1`): 357 live TCs, 350 naming a `tests/` file in `evidence`; about
1970 distinct test nodes in 154 files, and 146 TCs with a file-only part,
across 219 of 269 test files. Of the evidence parts, 2020 name a function, 5
a method, 20 a parametrized case and 169 a file; 8 name no test file (CI,
inspection, review and text records). 19 nodes name no def in their file, and
TC-165 and TC-166 carry a parenthetical instead of a path. 1309 of 5792 test
functions have a docstring, so most tags add one.

**Anchor.** SR-157, as row 1: a tag and a cell that disagree are a broken join
the harness names. The in-lane spine change is one LLR under SR-157 stating
the equality rule, with its TCs.

**Architectural delta (S5).** No new state and no new boundary. It adds two
values to the finding domain (evidence without a tag, a tag without evidence),
and its output depends only on what `check_trajectory` already reads once row 1
has landed: the tests root and the TC rows.

## The seed rule

Row 1's rule, for this repository and for adopters alike: a file-only evidence
part becomes a module-docstring tag in that file, and a `file::node` part a tag
in that test's docstring. A part naming a parametrized case seeds its test,
since a test's tag covers all its cases. Free-text TC mentions in the tests are
never a source: 408 of 541 file-level pairs have none.

## The equality rule

For each live TC, Draft included, take its evidence parts that name a path
under the declared tests root, each reduced to `path`, `path::name` or
`path::Class::name` (a `[case]` suffix dropped). That set must equal the node
ids row 1's reader returns for the TC. A part outside the tests root (a CI,
inspection, review or text record) is outside the rule. Each difference is one
finding naming the TC and the node:

1. **Evidence without a tag:** a part no tag declares.
2. **Tag without evidence:** a tag no part names.

The evidence parts are read by the reader `trace.py` already uses for that
cell; no second parse of the cell.

## Done-when

- [ ] **The tags.** Every evidence part under the tests root is seeded by the
      seed rule, by a scripted edit that is not shipped. The script's before
      and after are shown equivalent: each changed file's AST, docstrings
      aside, is unchanged, and the collected test count is unchanged. The
      result is stated in the log.
- [ ] **The stale parts.** No live TC's `evidence` holds a node naming no def,
      or a part that is not a path. Each of the 19 nodes, and TC-165's and
      TC-166's parentheticals, is repointed at the test that verifies the case
      (a traced-only change, re-anchored in the lane), and each is recorded in
      the lane's decisions. Where no test verifies the case, the row stops and
      reports it: that is a finding about the TC, not a cell edit.
- [ ] **The check.** `check_trajectory.py`, through `trajectory_arch.py` beside
      row 1's findings, reports the equality rule's two findings: a WARN, and
      an ERROR under `--strict`, the idiom row 1 uses. It is vacuous with no
      tests root or no TC registry. It lands green on trunk: 0 findings.
- [ ] **Regressions.** Each finding is named; a parametrized part matches its
      test's tag; a part outside the tests root is ignored; a file-only part
      matches a module-docstring tag and not a test's tag; a Draft TC is
      judged.
- [ ] **The lane's own routine.** The recipes state that a lane writes a
      test's tag and its evidence part in one commit, since the bar runs the
      check under `--strict`.
- [ ] **Sizes.** A size or complexity row the tags move is re-stamped per row
      in the commit that moves it, never by a full `--restamp`.
- [ ] **Spine.** One LLR under SR-157 states the equality rule in contract
      voice, with no code named in the row text, and TCs verify each arm. The
      set passes in-lane adjudication.
- [ ] **RESYNC entry** in `project-trajectory/RESYNC_PACK.md`, anchored at the
      trunk commit carrying the check: what changed, the two findings, that
      the check retires when the evidence column is generated, and what to do:
      seed your tags by the seed rule before re-syncing past this entry, since
      a repository with evidence cells and no tags reads one finding per part
      from `DevStg-Impl`. That is the forced migration OI-120 call 2 accepted;
      no second one. No setting and no schema changes.
- [ ] **The retirement** is written where item 5's work will read it: the
      check's own header comment names the generated evidence column as its
      end. This row builds no retirement.
- [ ] Coverage bound: the promise reaches the tags and evidence cells supported
      workflows produce: a builder or an LLM-applied re-sync writing a tag, and
      a TC row authored through a lane (`project-trajectory/PROCESS.md` §6
      "Review threat model"). Row 1's bound holds for the tags.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B). The reviewers
      judge the seed script's result through its equivalence evidence, the
      check, and a sample of the tags, not each of about 2100 edits.

## Trust

The check adds no authority to release, skip or pass anything: it can only add
a finding. Under `--strict` that finding refuses the commit bar, and an
adopter's gate from `DevStg-Impl`, so both carriers take part in a gate
(`project-trajectory/PROCESS.md` §3, "When a guard is owed"). Row 2 reads the
tags alone and relies on this check to keep them true.

- **Producers:** test files, written by a builder or an LLM-applied re-sync,
  and TC `evidence` cells, written by the spine author, the builder or the
  coordinator in a lane. No shipped script writes either. A failed write is a
  file left part edited, which row 1's unreadable finding or the registry's
  parse names.
- **Consumers:** `check_trajectory.py`, through `trajectory_arch.py`, run by
  `run.cmd smoke` and `check.py`. Nothing else reads the comparison.
- **Ruling, one for both carriers:** absent carriers (no tests root, no TC
  registry) are vacuous; equal homes pass; any difference is a named finding;
  a file row 1's reader refuses is reported by row 1 at the same severity, and
  this check adds nothing for it.

## Scope critique, pre-answered

- **S1.** One deliverable, kept together on purpose: the check is red without
  the tags, and the tags are unguarded without the check. The tags commit
  first, the check after them, in one lane. It lands alone, and open lanes
  rebase onto it.
- **S4.** `single`: a `## Trust` section, and a promise over an input space.
- **S6.** `needs` WI-994 (the reader and grammar) and OI-125 (Q1's ruling).
  Stdlib only.
- **B4.** No owner act and no credential in this row.
