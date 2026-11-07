+++
id = "WI-995"
title = "The review test set is derived from the row's SRs through the test-file tags; an empty or partial set, or a code-touching row naming no SR, refuses"
workstream = "process"
sr_refs = ["SR-241", "SR-156", "SR-154"]
specref = ""
needs = ["WI-994", "WI-997", "OI-125"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

The review test set is derived, never typed: `review_set.py` walks the row's
SRs, their LLRs and every TC verifying either to the tagged test files, and
refuses a code-touching row naming no SR, an empty or a partial set, and an
unreadable input, by name. `attest` and `review_brief.py review` lose `--tests`,
the unattended draw compares against the derived set, and an empty set renders
no pytest line. LLR-367 and TC-413 to TC-420 are approved; SR-241, LLR-207,
LLR-313, LLR-341, LLR-344, TC-132, TC-333 and TC-371 re-attested, at the lane's
acts under sitting 006.

## Context

P8's three rows (WI-992's filing, the review-churn plan's item 13): row 1 is WI-994, row 2 WI-995 and row 3 WI-996; "row N" below names them so.

P8's second row (WI-992; review-churn plan item 13, "Which tests" and the
integrator's notes on the scoped set, ruled as a whole in revision 35; the
revision 36 tree-walk ruling; OI-120 ruled (a) on each call, 2026-11-02).
Today a review bar's named tests are chosen by whoever asks for the
attestation. This row derives them from the spine instead: the TCs that
verify the work item's SRs directly, unioned with the TCs that verify the
LLRs under those SRs, then the test files whose `Implements:` lines name
those TCs (row 1's reader). It refuses an empty or partial set and refuses a
code-touching row that names no SR (OI-120 Q3), and it never falls back to
the whole bar.

**Needs.** `WI-994` (P8 row 1: the test-file TC tag on the `Implements:`
line and its one reader) and `WI-997` (this repository's test files tagged,
and tags held equal to the evidence cells). This row is that reader's first
consumer: without tags, every TC
in scope reads as untagged and every code-touching row is refused as
partial. Satisfied already: one work item per lane (item 15, landed; RESYNC
"One work item per lane"), so a lane has exactly one claimed row whose
`sr_refs` the set is derived from; the review attestation and its
consumers (WI-956, WI-957, WI-958, landed). P8 row 3 (the strict-mark
commit check) needs this row: its marked tests are proven on the review
bar that runs this set.

**Anchor.** SR-241 (a review brief renders only over a verified record that
the declared review bar and the named test set passed). This row decides
what the named test set is. The producer is SR-156's attestation
(LLR-207, `integrate.py attest`) and the unattended consumer is SR-154's
draw gate (LLR-344). Whether the derivation is a new LLR under SR-241 or an
amendment of SR-241 (or of LLR-341, LLR-207 and LLR-344) is the in-lane
adjudicator's ruling. The spine change set states behaviour, never code
(the 2026-10-11 ruling).

### Where the set comes from today (measured 2026-11-03 on `c57796e63`)

- `integrate.py attest --branch B --bar review --tests T...`: `--tests` is
  `nargs="*"`, default `[]` (`integrate.py:3757`). `_run_review_bar` runs
  `[bars] review`, then, if any tests are named, `[product] test` with the
  paths appended and its own `--basetemp`. `_attest_commit` writes
  `tests=<sha256 of the sorted, normalized paths | none>` into the
  `Bar-Green:` line (`kitlib/verdict.py` `tests_digest`). The list is
  whatever the operator typed.
- `review_brief.py review --tests T...`: required, `nargs="+"`
  (`review_brief.py:1169`); `Round` refuses an empty tuple. The render
  checks `kverdict.review_attestation(root, sha, tests)` (digest equality)
  and prints the paths into the reviewer's pytest line (`_run_lines`).
- The unattended loop, `agent_loop.review_draw_gate`
  (`agent_loop.py:3378`, `:3384`), checks `review_attestation(root,
  "HEAD", [])` and attests with `integrate.attest(root, branch, "review",
  [])`. **Unattended review draws run no named tests at all today**, only
  `[bars] review`.
- The coordinator hand-picks the list (coordinator-cycle `SKILL.md`
  Iterate step 1; `references/recipes.md` section 1 step 1 and section 6,
  three places, plus the trap at line 1264: "`attest --tests` names test
  files that exist").
- `[bars]` has exactly one key, `review`, in both homes:
  `docs/stack.ini:1366` (`python project-trajectory/scripts/run_menu.py
  smoke`) and `project-trajectory/stack.ini.template:255` (`python
  scripts/check.py --jobs 0 --tier smoke`). Its one reader is
  `integrate._review_bar_command`. This row adds no key.
- The smoke tier is not a substitute: `tests/conftest.py` `SLOW_MODULES`
  keeps 139 of the 269 `tests/test_*.py` modules out of it (the plan's
  revision 23 figure was 122 of 232).

### The spine the set walks (measured)

- 138 SRs, 330 LLRs, 357 TCs, all `Approved`. No LLR carries a parent link
  (0 of 330; the LLR keys are `sr_refs`, `title`, `module`, `code_symbol`,
  `detail`, `test_refs`, `status`, `component`, `phase`, `rationale`,
  `hat_refs`), so today the SR → LLR walk is one level through `sr_refs`.
  31 LLRs name more than one SR.
- 6 SRs have no LLR (SR-034, SR-036, SR-114, SR-184, SR-185, SR-186); each is
  reached by a TC that verifies it directly. 10 TCs verify an SR with no LLR
  beside it (TC-034, TC-035, TC-036, TC-149, TC-158, TC-209, TC-210, TC-211,
  TC-275, TC-385); the plan's revision 18 list had 9, before TC-385. No SR
  and no LLR is verified by nothing.
- TC evidence cells (read with `kitlib.spine.evidence_items`): 349 name only
  paths under `tests/`; 1 (TC-325) names tests and
  `project-trajectory/hooks/pre-commit`; 7 name no test path: TC-035
  (`.github/workflows/test.yml`), TC-036 (`project-trajectory/ADOPTING.md`),
  TC-055 (`docs/reviews/074-CRITIQUE.md`), and TC-209, TC-210, TC-211 and
  TC-279 (`docs/test/inspection-procedures.md` anchors). TC-279 has no
  `verifies` (it tests assumption DA-011), so no row's set reaches it. The
  cells name 217 distinct test files, and every named path exists.
- Test-file tags: 0 of 269 test modules carry an `Implements:` line naming
  a TC. The one hit, `tests/test_gen_arch_map.py:612`, is a string literal
  inside an assertion. 116 modules mention a TC id in free text, reaching
  142 of the 357 live TC ids (154 ids in all; 12 are fixtures or retired).
  Row 1 closes this gap; this row reads only what row 1's reader returns.
- The size of the set by evidence cells (a proxy until the tags land):
  per SR, median 2 test files, maximum 34 (SR-156); 5 SRs reach no test
  file (SR-036, SR-114, SR-184, SR-185, SR-186). Queued rows: WI-802 14
  files, WI-908 11, WI-910 and WI-964 7, WI-982 and WI-983 5, WI-991 6,
  WI-992 12, WI-993 7, and WI-684 none (SR-036 only, an inspection TC).
- Rows that name no SR: 9 of the 32 open rows in `queued`, `draft` and
  `deferred` (WI-000 excluded): WI-795 and WI-827 (queued, both owner
  acts), and WI-625, WI-812, WI-814, WI-815, WI-819, WI-820 and WI-832
  (deferred). By title, six of the deferred seven would touch code, and
  each would be refused at its first attest until it names its SRs. The
  2026-10-20 count was 8 of 36. No lane is claimed on trunk today
  (`git ls-files docs/work/active` is empty).

### The derivation (one function, stated once)

Inputs, all read from the tree the caller hands it (the lane checkout,
which `attest` has already checked equals the index): the lane's one
claim copy (`docs/work/active/<branch>/WI-*.md`) and its `sr_refs`; the SR,
LLR and TC registries; `[paths] src` and `[paths] tests` from
`docs/stack.ini` (the existing reader and its `src`/`tests` defaults); row
1's tag reader over the tests root; and the lane's changed paths since its
merge base with the declared trunk (`trunk` in `docs/process.toml`, the
existing reader).

- **S** = the claim copy's `sr_refs`.
- **L** = every LLR whose `sr_refs` names an SR in S. This is the SR → LLR
  walk, one level today. It has one home, so item 5's schema lane, which
  adds the parent-LLR link, extends it to children in one place (revision
  36: "a child LLR's tests never drop out of the scoped set unseen").
- **T** = every TC, of any status (a TC being written in the lane
  included), whose `verifies` names an SR in S or an LLR in L. A TC that
  verifies an IF beside them is included through its SR or LLR. Widening
  by interface (F's blast radius) is not this row's.
- Each TC in T falls in exactly one class:
  - **tagged:** some test file's `Implements:` line names it. Its tagged
    files join the set, and any non-test evidence items it declares
    (TC-325's hook file) are listed beside the set;
  - **untagged, executable evidence:** its evidence cell names a path
    under `[paths] tests`, but no file's tag names it. This is a **gap**;
  - **declared non-executable evidence:** untagged, and its evidence names
    only paths outside the tests root that exist in the tree (an inspection
    record, a CI workflow, a document, a critique record; revision 35
    keeps these cells authored). It is listed beside the set, never run
    and never judged here;
  - **no evidence:** untagged, and its evidence cell names no path, or
    names a path the tree lacks. This is a **gap**.
- More gaps: an SR in S that no TC in T verifies, directly or through an
  LLR in L (a row with SRs but no LLRs is fine while a TC verifies the SR
  directly); an LLR in L that no TC verifies.
- **The set** is the sorted union of tagged test files. **Partial** means
  at least one gap, whether or not that union is empty, and names every
  gap. **Empty** means that union is empty with no gap. OI-125 Q2 ruled
  (a) (2026-11-03): the gaps reach every LLR under the row's SRs, so a row
  building one LLR waits for its siblings' failing tests.
- **Code-touching** means the lane's changed paths (merge base to the
  staged tree) include one under `[paths] src` or `[paths] tests`. Every
  other path is not code. In this repository, `project-trajectory/hooks/`,
  `ci/`, the templates, skills and docs are not code under this rule. That
  matches the traced product as `CLAUDE.md` states it
  (`project-trajectory/scripts` + `tests/`).

The answer is one of four:
- **refused, names no SR:** code-touching and S empty (OI-120 Q3);
- **refused, malformed:** an SR in S the SR registry lacks, or an input
  that cannot be read (below);
- **refused, empty** or **refused, partial:** code-touching, naming each
  gap (the SR or LLR verified by nothing; the TC with no tagged file and
  the test path its evidence names; the TC whose evidence path is
  missing);
- **the set:** the test files plus the listed non-executable evidence.
  For a row that is not code-touching, gaps are reported, not refused,
  and an empty set is allowed. The plan's refusal is scoped to
  code-touching lanes (integrator's notes, revision 18). A spine-only lane
  legitimately leaves TCs untested before `DevStg-Impl`. Such a row's
  review bar is `[bars] review` alone, as the loop's is today.

The set is an addition to the floor, never a replacement for it. The smoke
tier (inside `[bars] review`) and the landing bar stay as they are (plan
item 13: "The scoped set is the gate's addition, not a replacement").

### What changes for each caller

- **`integrate.py attest`** derives the set from the lane it resolves,
  before any bar runs, as its other preflight refusals do. `--tests`
  retires: the ruling is a derived set, never a hand list. A refusal
  leaves the branch and the index as they were. Green, it runs `[bars]
  review` and then the derived files through `[product] test`, records
  their digest in the existing `Bar-Green:` grammar (unchanged), and
  prints the set and the listed non-executable evidence.
- **The loop** (`review_draw_gate`) checks the tip's record against the
  derived set instead of `[]`, and attests through the same derivation. A
  derivation refusal takes the existing red route: no round, rework with
  the refusal named, counted toward `[build] red_rounds_max`, and at the
  cap the partial close and its disposition (OI-70: partial is the only
  stop). So a code-touching row naming no SR closes partial, and its
  disposition drafts a successor that names its SRs. No new route.
- **`review_brief.py review`**: `--tests` retires. The render takes its
  list from the same derivation over the lane checkout, and the existing
  digest check binds it to the record: a list that differs from the
  attested one refuses, naming both digests, so a working-tree edit can
  only refuse, never render another set. A derivation refusal refuses the
  render with the same text. An empty set renders the brief with no pytest
  line and says that the row's set is empty because the row touches no
  code. A pytest line with no paths would run the whole suite, which is
  the fallback the ruling forbids.
- **The coordinator** (this repository's `coordinator-cycle` skill and
  recipes, synced copies included) stops typing `--tests`. A spine step
  that adds TC rows before their tests exist is either committed without
  an attestation (registry text) or staged into the attest that carries
  those tests; the first attest after it must hold their tagged tests, or
  it refuses as partial. That is the TC-first order item 13 restores. A
  partial refusal is fixed in the lane (tag the test, or write it). A
  names-no-SR refusal is fixed by amending the row's `sr_refs` on trunk.
- **An adopter** sees `attest` and `review_brief.py review` without
  `--tests`. The unattended loop's review bar now also runs the tests
  tagged for the row's SRs. A code-touching row with no `sr_refs` is
  refused, as are an empty or partial set. One RESYNC entry states this.
  It is not a third forced migration: tagging (row 1's entry) and naming
  SRs on code rows (OI-120 Q3) are the adopter's work, and no key, record
  or file format changes.

### Scope-critique pre-answers

- **S1.** The deliverables are (1) the derivation and its refusals,
  (2) its three consumers (`attest`, the draw gate, the render), (3) the
  coordinator-cycle text and (4) the RESYNC entry. They land in that order
  in one lane. They stay one row because (2) has to switch all three
  consumers together: the record's digest changes meaning, and a consumer
  still comparing against `[]` or a hand list would re-attest on every
  draw or refuse every render. (1) alone changes no behaviour, and (3) and
  (4) describe (2).
- **S2.** The derived set gains authority over a gate: what the review bar
  runs, and whether `attest` attests. See `## Trust`.
- **S3.** The open input spaces each get an enumerated rule above and in
  the Trust ruling: the claim copy's states; SR ids; an SR with no LLR; an
  LLR or SR with no TC; the four TC classes (tagged, untagged executable,
  declared non-executable, no evidence); the changed-path space
  (code-touching against everything else); unreadable inputs. Row 1's
  reader owns the tag grammar's own malformed states, and its refusals
  pass through unchanged.
- **S4.** `single`: a Trust section, three script families
  (`integrate.py`, `agent_loop.py`, `review_brief.py`) plus the
  `kitlib.spine` join, two CLI seams (IF-154, IF-288) and the in-process
  seam IF-173, and a promise over an input space.
- **S5.** One output, the named tests and their digest in the review
  record, now depends on new inputs (the claim copy's `sr_refs`, the three
  registries, the tags, `[paths]`, the merge base) and no longer on an
  operator's argument. Four values join `attest`'s refusal domain
  (names-no-SR, malformed, empty, partial). The new boundary is the lane
  machinery reading the spine. The pure walk belongs beside
  `kitlib.spine.module_tests` (the kernel, CMP-006, which reads rows only);
  the tree read lives in one CMP-008 home that all three consumers call.
  The plan names both and declares the interface data-cell amendments
  (IF-154 and IF-288 lose `--tests`; IF-173's vocabulary, if the loop's
  call changes shape).
- **S6.** `needs` = row 1. No new package, tool or service.
- **S7 (what this row does not do).** It does not define or apply the tag
  grammar (row 1), add the strict-mark check or `[bars] red_mark` (row 3),
  widen the set by interface (item 11's derived blast radius), walk
  parent-LLR links (item 5's schema lane adds the field and extends the
  one walk), verify non-executable evidence (the typed evidence contract,
  item 13's later work), generate TC evidence cells from tags (item 5),
  or change `[bars] review`, the landing bar, the smoke tier or
  `trace.py --tests-for`.

## Done-when

- [x] One derivation, with one home for its SR → LLR walk, returns the set
      or exactly one of the refusals above, from the lane's claim copy, the
      SR, LLR and TC registries, row 1's tag reader, `[paths]` and the
      lane's changed paths since its merge base with the declared trunk.
      A TC in T falls in exactly one of the four classes. An SR verified
      only by a direct TC, as SR-034 and SR-184 are, yields that TC's
      tagged files (or its listed non-executable evidence) with no gap.
- [x] A code-touching row whose claim copy names no SR is refused by name
      and never runs the whole bar. A row that is not code-touching and
      names no SR runs `[bars] review` alone with an empty set.
- [x] A code-touching row is refused as **partial** by name for each gap:
      an SR in scope that no TC verifies, directly or through its LLRs;
      an LLR in scope that no TC verifies; a TC in scope whose evidence
      names a test path but that no test file's `Implements:` line names;
      a TC in scope that no file tags and whose evidence names no path, or
      a missing one. It is refused as **empty** only when no tagged file
      is reached and no gap exists; a row with both is partial, naming
      every gap. A TC whose evidence is only an existing inspection record,
      CI file or document (TC-035, TC-036, TC-209) is listed, not run,
      and is not a gap. Scope is every LLR under the row's SRs, sibling
      LLRs the row does not build included (OI-125 Q2 (a)).
- [x] For a row that is not code-touching, gaps are reported and never
      refused.
- [x] `integrate.py attest` takes no `--tests`. It derives the set before
      any bar runs (a refusal leaves the branch and index unchanged), runs
      `[bars] review` and then the derived files, records their digest in
      the unchanged `Bar-Green:` grammar, and prints the set and the
      listed evidence.
- [x] `agent_loop.review_draw_gate` compares the tip's record against the
      derived set. A derivation refusal takes the existing red route
      (rework naming it, counted by the red cap). A regression shows a
      draw over a code-touching lane with an untagged TC drawing no round.
- [x] `review_brief.py review` takes no `--tests`. It renders the derived
      list, refuses a record whose digest differs (naming both digests)
      and a derivation refusal, and renders an empty set with no pytest
      line. Its refusal hint names `attest` without `--tests`.
- [x] The coordinator-cycle skill and its recipes (both synced copies)
      drop every `--tests`, retire the "`attest --tests` names test files
      that exist" trap, and state the spine-step order and how each
      refusal is fixed.
- [x] The row's spine change set (the derivation's LLR under SR-241, or
      SR-241's amendment, as the in-lane adjudicator rules; LLR-207,
      LLR-341 and LLR-344 amended for the retired list; IF-154, IF-288
      and, if touched, IF-173 data cells; TCs for each refusal arm)
      passes in-lane adjudication.
- [x] RESYNC_PACK: one entry anchored at the landing commit. `attest` and
      `review_brief.py review` lose `--tests`; the review bar runs the
      row's tagged tests; a code-touching row names its SRs or is
      refused, and an empty or partial set refuses. No data, key or
      record format migrates. Row 1's entry (the tags) is the
      precondition. Kit-owned overwrite: the touched scripts.
- [x] Coverage bound: the promise reaches the claim copies, registries,
      tags, `[paths]` declarations and lane diffs that supported workflows
      and the kit's own routes produce (filing and claiming a row, in-lane
      spine authoring and acts, tagging tests, `attest`, the loop's
      draw), as `project-trajectory/PROCESS.md` §6 "Review threat model"
      bounds a spec's promise. Hand-edited kit-written state (a claim copy
      or a `Bar-Green:` line edited by hand), hand-chosen path aliases
      (case or separator spellings of a tests root) and sub-second timing
      windows are outside it.
- [x] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Critique dispositions

Round 1 (fresh Sol, 2026-11-04): CHANGES-REQUESTED, one MINOR.

- **S3, adopted.** The derivation now reads "**Partial** means at least one
  gap, whether or not that union is empty, and names every gap. **Empty**
  means that union is empty with no gap", and the Done-when refers to that
  rule, so a lane with both reads one refusal.

## Trust

The derived review test set gains authority over a gate: it decides what
the review bar runs and whether `attest` writes the review record that the
render and the loop's draw require. The guard follows
`project-trajectory/PROCESS.md` §3, "When a guard is owed": the inputs are
files in the lane's tree, read at the staged tree, which `attest` has
checked equals the worktree.

- **Producers and their failed writes:**
  - *The claim copy* (`docs/work/active/<branch>/WI-*.md`). It is written
    by `spec_move` at claim through the format's one writer (IF-159), which
    re-parses before it returns, and it is edited in the lane by people
    and models. A supported route never leaves it unparseable. A
    model-written edit can (agent-written repo content is in scope), and
    that refuses by name.
  - *The SR, LLR and TC registries.* They are authored by people and
    models, and their parse and integrity are already checked at the
    commit hook (`trace.py --strict-integrity`). A file that does not parse
    refuses by name.
  - *The test-file tags.* Authored; row 1's reader and its refusals govern
    them.
  - *`[paths]` and `trunk`.* Read through their existing readers with
    their existing defaults and refusals (an undeclared `trunk` already
    refuses, TC-369).
- **Consumers newly given the authority, by path:**
  - `project-trajectory/scripts/integrate.py`: `attest`,
    `_attest_preflight` (the derivation runs there) and `_run_review_bar`
    (runs the derived files).
  - `project-trajectory/scripts/agent_loop.py`: `review_draw_gate` (the
    comparison and the red route), reaching `integrate.attest` in-process
    (IF-173).
  - `project-trajectory/scripts/review_brief.py`: `_cmd_review`,
    `_review_bar_refusal`, `Round` (an empty set allowed) and `_run_lines`
    (no pytest line for an empty set).
  - `project-trajectory/scripts/kitlib/spine.py`: the pure walk, beside
    `evidence_items` and `module_tests`, whose readings it reuses.
- **Unchanged readers, under their established contracts:**
  `kitlib/verdict.py` (`tests_digest`, `format_bar_green`,
  `review_attestation`, `read_bar_attestation`; IF-175's grammar is
  unchanged), the merge slot's `refresh` (`tests=()`, the landing bar),
  `trace.py --tests-for` (`module_tests`, evidence-based, SR-221),
  `check.py`'s tiers and `tests/conftest.py`'s tiering.
- **The ruling** (one, shared by the three consumers; fail closed):
  - The claim copy is absent, there is more than one, or its frontmatter
    does not parse → refused, naming the path.
  - `sr_refs` is absent or `[]` → names no SR: refused if code-touching,
    otherwise an empty set.
  - `sr_refs` is not a list of id strings, or names an SR the registry
    lacks → refused, naming the id.
  - A registry, `docs/stack.ini` or the trunk declaration cannot be read
    or does not parse → refused, naming the file.
  - Row 1's reader refuses → refused with its text.
  - Otherwise, the four-way answer above. The set never widens to the
    whole bar and never drops a TC in scope silently. An empty set for a
    row that is not code-touching runs `[bars] review` alone and renders
    no pytest line.
- **What the set binds to:** the staged tree at `attest`, through the
  record's existing digest; the lane checkout at the render and the draw,
  where a different derived list refuses (a working-tree edit cannot pass
  another set). The render and the draw recompute the list only to name
  and compare it. The record is still the only evidence that the bar
  passed, which answers rubric B3.
- **Bound:** the set is tree-bound, so a lane that edits its own inputs (its
  claim copy's `sr_refs`, a tag, a TC row) changes its own set. Those edits
  are in the reviewed diff, an approved TC row is not removed without an
  act, and the landing bar is unchanged. This row adds no guard against a
  lane narrowing its own `sr_refs` (S7; see the notes' open question 4).
