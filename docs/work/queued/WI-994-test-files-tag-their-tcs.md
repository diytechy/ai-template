+++
id = "WI-994"
title = "Test files name their test cases on the existing Implements: line, read by the one back-link reader, which refuses a malformed tag and an unknown test case"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages"
needs = ["OI-120", "OI-125"]
buildtier = "medium"
safety_class = "ordinary"
planmode = "single"
priority = 5
+++

## Context

P8's three rows (WI-992's filing, the review-churn plan's item 13): row 1 is WI-994, row 2 WI-995 and row 3 WI-996; "row N" below names them so.

P8 row 1 of 3 (WI-992; review-churn plan item 13, phase 1). OI-120 ruled
(a) on each call on 2026-11-02 (coordinator-2026-11-02 D-006). Call 1 says
the test-file TC tag is the existing `Implements:` line, with one grammar and
one reader for code and tests. Call 2 accepts the forced adopter migration
"adopters tag their test files", stated in a RESYNC entry. Rows 2 (the review
test set derived from the tags and the row's SRs) and 3 (the strict-mark
commit check) follow. Row 2 needs this row.

**Why it is owed.** The plan's scoped review set selects tests per TC
(revision 17), and revision 8 made the link point up: test files name their
TC, and TC rows stop naming test files. Revision 32 (Fable) found that no tag
grammar or reader exists, so "the tags lane's spec fixes the grammar and its
one reader before any file is tagged". Row 2's scoped set and, later, item
5's generated evidence column both read through that reader. Revision 35
allows a tag on a test function, which replaces the evidence cells' `::`
node form.

**The one reader already exists, and it already admits TC ids.**
`gen_arch_map.backlink_ids(line)` is the kit's one definition of a
back-link (WI-486, OI-42 (b)+(e); LLR-204; offered for reading history as
IF-199). A declaration is the literal `IMPLEMENTS_MARKER` opening its line
(`_DECL_OPENING`: only whitespace, comment markers or quotes before it),
followed on the same line by ids matching `IMPLEMENTS_RE`, which is
`(?:SR|LLR|SN|TC)-\d+`. Its readers, found by grep for `backlink_ids`,
`scan_backlinks`, `implements_report`, `declaration_sites` and
`IMPLEMENTS_MARKER`:

- `gen_arch_map.implements()`, the map's Implements column.
- `gen_arch_map.scan_backlinks` / `backlink_report`, the reverse-coverage
  number. It counts LLR ids only and is driven by `check.py`'s
  `backlink-coverage` step.
- `gen_arch_map.declaration_sites` / `implements_report`, the AST reader
  for `.py` files. Its callers are `trajectory_arch.codesymbol_crosscheck_findings`
  (through `check_trajectory`), which filters to LLR ids,
  `trace._implementing_modules` and `trace.contract_symbol_surface`.
- `check_test_first.first_implementation_commits`, the SR-217 history read
  over the IF-199 grammar.

Every one of them scans `[paths] src` (`project-trajectory/scripts` here),
never `[paths] tests`. So nothing reads test -> TC today. `trace.py` reads
only TC -> test, through each TC row's `evidence` cell, and `trace.py
--tests-for` (SR-221, LLR-263) reads the same cells.

**Why a test file needs a narrower placement rule than a code file.** A
test file holds fixture text, so a line scan misreads it. Run over every
`.py` under `tests/`, `backlink_ids` harvests 4 lines in 2 files today
(`tests/test_gen_arch_map.py` 3 and `tests/test_trajectory_arch.py` 1). All
4 are fixture strings naming SR and LLR ids, and none is a docstring or a
comment. A line reader would report each one as a test-file tag naming a
requirement, which is 4 false refusals. So, for Python, the reader reads
docstrings by AST, and comments by `tokenize`, and never reads a string
literal that is not a docstring. The per-line grammar stays the one in
`backlink_ids`.

**Re-measured counts** (2026-11-03, trunk `c57796e63`; commands and scripts
in the notes beside this draft):

| What | Plan / handoff figure | Today |
|---|---|---|
| Test files (`tests/**/test_*.py`) | 231–237 | 269 (279 `.py` under `tests/`) |
| Test files mentioning any TC id, free text | 99–107 | 116 (154 distinct ids, 142 of them live) |
| Test files carrying an `Implements:` TC tag | none | 0 |
| Live TC rows | 316 | 357, all `Approved` |
| TC rows whose `evidence` names a `tests/` file | 314 of 316 | 350 of 357 (the 7 others are CI, inspection, review or text records: TC-035, 036, 055, 209, 210, 211, 279) |
| Evidence parts naming a test node with `::` | 185 cells | 2045 parts in 235 TCs, 1970 distinct nodes in 154 files |
| TCs with a file-only `tests/` evidence part | – | 146 |
| Distinct test files named by any evidence cell | – | 219 (of 269) |
| Evidence `::` nodes that resolve to no def in the named file | – | 19 (stale) |
| Evidence parts that are not a bare path | – | 2 (TC-165 and TC-166, `(to be extended at implementation)`) |
| (evidence file, TC) pairs whose file never mentions the TC in free text | – | 408 of 541 |
| Test functions / with a docstring / test files with a module docstring | – | 5792 / 1309 / 269 of 269 |
| Docstring or comment `Implements:` declarations under `tests/` | – | 0 (so the check lands green) |
| Source files declaring a TC id on `Implements:` | – | 0 (SN: 0) |
| The review bar's test list | hand-picked `--tests` | still hand-named: `integrate.py attest --bar review --tests <files>` runs `[bars] review`, then the named files through `[product] test`; `review_brief.py review --tests` must repeat the attested list (coordinator-cycle `references/recipes.md`, the review-brief step) |

The free-text mentions do not track the evidence cells: 408 of 541
file-level pairs have no mention. So the tags are seeded from the evidence
cells, never from the prose (see Migration).

**Anchor.** SR-157, "spine and work-registry rules red the harness verdict":
the harness reports every declared spine rule violation, broken joins and
form faults included, naming the at-fault row and cell. A test-file tag is a
spine edge (test file -> TC; the plan's `pointer-rules.md` "names its TC").
A tag naming no live TC is a broken join, and a tag the grammar refuses is a
form fault. This row adds that rule. The in-lane spine change is one new LLR
under SR-157 (the tag rule and its refusals) with its TCs. LLR-204 stays the
code-side grammar's row under SR-163. The scoped set that gives the tags
their purpose is row 2's, under SR-241.

**Architectural delta (S5).** This row adds no state. It adds four values
to the finding domain: a misplaced tag, a malformed tag, an unknown TC and
an unreadable file.
It adds one new input to `check_trajectory`'s output, the files under the
declared tests root. It crosses no new boundary: `check_trajectory`
(trajectory_arch) already calls `gen_arch_map` over IF-131, "the
seam-declaration grammar the spine checks read". The lane adds the reader to
that row's `data` cell, or files a new IF row if in-lane adjudication rules
it a separate seam.

## The grammar (settled here)

One token, one opening rule and one id list, shared with code. A test file
differs only in which ids it names and where the reader looks.

- **The line.** `backlink_ids`'s rule, unchanged: `Implements:` opens the
  line, with nothing before it but whitespace, comment markers or quotes.
  In a test file the text after the token must be exactly one or more
  `TC-<digits>` ids separated by commas (whitespace allowed), with nothing
  else on the line. Example: `Implements: TC-201, TC-202`.
- **Read positions, Python** (a `test_*.py` or `*_test.py` file under the
  declared `[paths] tests` root, pytest's default `python_files`):
  - the **module docstring**, where a tag covers every test in the file.
    Its node id is the repo-relative path, e.g. `tests/test_trace.py`;
  - the **docstring of a test**, where a tag covers that test. A test is a
    `test*` function at module scope, or a `test*` method of a `Test*` class
    nested only in `Test*` classes. Its node id is
    `path::name` or `path::Class::name`, the form the evidence cells use
    today. A parametrized test's tag covers all its cases.
  - Tags at both levels union. A test function repeating its module's TC is
    not a finding.
- **Read positions, any other stack.** A non-`.py` test file whose
  extension is in `BACKLINK_EXTS`, under the tests root: every line is read
  at file level (the `scan_backlinks` posture; the kit parses no other
  language). Per-test granularity is the Python reference's. Another stack
  supplies its own per-test form later, if it wants one.
- **Everything else, closed.** Under the tests root, an `Implements:`
  declaration in any other docstring (a helper, fixture or class
  docstring), or in any comment, in any `.py` file is **refused as
  misplaced**. That includes `conftest.py` and fixture modules. It is never
  silently ignored. A string literal that is not a docstring is never a
  declaration (fixture text). A backtick-quoted `Implements:` is a mention,
  as for code.

**What the reader refuses.** Each finding names the file, the line and the
shape.

1. **Misplaced**: a declaration outside a read position (above).
2. **Malformed**: in a read position, an `Implements:` line that opens its
   line but whose list is not TC ids only. That covers an empty list; a
   trailing comma or a list wrapped onto the next line; an SN, SR or LLR id
   (a test names the case it runs, and what that case verifies is the TC
   row's `verifies` cell); and prose, `and` or a range after the ids. It
   also covers a read-position line where the token follows prose and a TC
   id follows the token (`"""Checks X. Implements: TC-12"""`, the one-line
   docstring shape). `backlink_ids` declares nothing there, so without this
   refusal the tag would drop out with no word. The message says to put the
   token at the start of its own line.
3. **Unknown**: an id that no live TC row carries in the TC registry (read
   through `spine_carrier`, so either carrier). A `-000` example id is not
   a live row, so a tag naming one is refused. A Draft TC is live, so
   tagging a test before its TC is approved is fine (TC-first).
4. **Unreadable**: a test file under the tests root that cannot be decoded
   as UTF-8 or parsed. It is refused by name, never read as carrying no
   tags.

**What it does NOT do** (each is another row's):

- It never refuses an **untagged** test file or an **untagged TC**. Row 2's
  scoped set refuses a set that reaches a TC with no tagged test and no
  declared non-executable evidence.
- It does not compare tags with the `evidence` cells, and it does not
  generate the evidence column. The generated column is item 5 (phase 3).
  OI-125 Q1 ruled (a): the migration row checks the two homes equal in the
  meantime (Migration).
- It does not change `trace.py --tests-for` (SR-221), which keeps reading
  the evidence cells, or any review-bar input. The derived review set is
  row 2's, and the strict marks are row 3's.
- It changes no code-file reading: the map column, the reverse coverage, the
  CodeSymbol crosscheck and `check_test_first` read exactly what they read
  today. A source file naming a TC id is not refused (0 do today, and
  nothing reads it).

## Migration

**This row tags none of this repository's test files.** WI-997, a
measured follow-up row, tags them. It is filed before this row's claim; it
needs this one, and must land before row 2's gate is enabled here, because
row 2 refuses a partial set. Why not in this row:

- **Size.** Seeding the tags from the evidence cells is about 1970
  test-function docstring tags (1309 of 5792 test functions have a
  docstring today, so most need one added) plus module-docstring tags for
  146 TCs, across 219 files. Reviewed in the same diff as the reader, that
  edit would bury the reader's review (Review bar A+B).
- **It is not purely mechanical.** 19 evidence nodes name no def in their
  file, and TC-165 and TC-166 carry a parenthetical instead of a path. Each
  needs a judgement: either the cell or the test is wrong.
- **Two homes in the meantime.** Until item 5 generates the evidence
  column, the tags and the cells state one fact twice. OI-125 Q1 ruled (a)
  (2026-11-03): the migration row checks them equal as a strict finding
  before row 2 reads the tags, and the check retires when item 5 lands.

The seed rule for that row and for adopters is the same. A file-only
evidence part becomes a module-docstring tag in that file. A `file::node`
part becomes a tag in that test's docstring.

## Done-when

- [ ] **The reader.** `project-trajectory/scripts/gen_arch_map.py` gains one
      test-tag reader beside `declaration_sites`. It is built on
      `IMPLEMENTS_MARKER` and the `_DECL_OPENING` rule `backlink_ids`
      applies: no second token and no second opening rule. It takes the
      declared tests root and the set of live TC ids, and returns
      `{TC id: sorted node ids}` plus a findings list, each finding naming
      file, line and shape. It is pure apart from reading the files.
      `backlink_ids`, `scan_backlinks`, `declaration_sites` and
      `implements_report` keep their signatures and outputs. A regression
      asserts that `implements_report` and `scan_backlinks` over
      `project-trajectory/scripts` give the same output before and after.
- [ ] **The grammar.** The reader implements "The grammar (settled here)"
      exactly: the Python read positions (module docstring; a test's
      docstring, with `path::name` / `path::Class::name` node ids); the
      file-level line reading for non-`.py` test files in `BACKLINK_EXTS`;
      the union of levels; and the four refusals: misplaced, malformed
      (each listed shape, the token-after-prose one-liner included), unknown
      (`-000` included) and unreadable.
- [ ] **The surface.** `check_trajectory.py`, through `trajectory_arch.py`
      beside the CodeSymbol crosscheck, reads the tests root (`[paths]
      tests`, through the existing `_tests_dir` reader) and the live TC ids.
      It prints each finding as a WARN, and as an ERROR under `--strict`, the
      `contract_body_findings` idiom. So this repository's commit bar
      (`run.cmd smoke`, which runs `check_trajectory.py --strict`) refuses
      the commit, and an adopter's gate refuses it from `DevStg-Impl`, the
      rung where `check.py` adds `--strict` (below it, a WARN). The check is vacuous with no tests root
      or no TC registry and no tags. It lands green on trunk: 0 findings
      measured. Its added wall time on the bar is measured and stated in
      the log (the scratch prototype read all 279 files in about 1.3 s).
- [ ] **Regressions** (`tests/test_gen_arch_map.py`, and the
      `check_trajectory` / `trajectory_arch` suite for the surface):
      - each read position yields its node ids;
      - each refusal shape is named;
      - a fixture string inside a test file that opens a line with
        `Implements: SR-001` yields no tag and no finding (the live
        `tests/test_gen_arch_map.py` shape);
      - a one-line test docstring `"""Checks X. Implements: TC-1"""` is
        refused as malformed;
      - a `# Implements: TC-1` comment above a test is refused as
        misplaced;
      - a file that does not parse is refused as unreadable;
      - a test file tagging a Draft TC is clean;
      - a tag naming a TC absent from the registry is refused.
- [ ] **One home for the rule, in text.** `project-trajectory/PROCESS.md`
      §3's back-link bullet replaces "test names embed the verified ID"
      with the tag rule: test files name their test cases on the same
      `Implements:` line, in the module docstring or a test's docstring.
      `project-trajectory/AGENTS.template.md` ("Back-link to requirements")
      and `project-trajectory/EXAMPLE.md` §5 (its Rust test gains
      `// Implements: TC-001`, file-level) follow it and link to it. The
      byte budgets are checked with the `byte-budget-guard` skill.
      `docs/registry-machinery-reference.md` (the TC tier) and
      `docs/enforcement-audit.md` (beside the back-link row) name the new
      rule and its enforcer.
- [ ] **Spine.** One LLR under SR-157 states the test-file tag rule and its
      four refusals in contract voice, with no code named in the row text,
      and TCs verify each arm. The IF row carrying the trajectory checks'
      read of `gen_arch_map` (IF-131) names the reader in its `data` cell,
      or in-lane adjudication rules a new IF row. The set passes in-lane
      adjudication. The new reader's own `Implements:` line names SR-157
      and the new LLR.
- [ ] **RESYNC entry** in `project-trajectory/RESYNC_PACK.md`, anchored at
      the trunk commit carrying the reader: "Test files name their test
      cases on the `Implements:` line". **What changed:** the grammar above,
      its read positions, and the four refusals in `check_trajectory`
      (`--strict` errors). **What to do (forced migration, owner ruling
      OI-120 call 2):** overwrite `scripts/gen_arch_map.py`,
      `scripts/check_trajectory.py` and `scripts/trajectory_arch.py`, and
      take the PROCESS.md and AGENTS.md text. Then **tag your test files**:
      for each TC whose `evidence` names a test file, add `Implements:
      TC-NNN` to that file's module docstring; for each `file::test` node,
      add it to that test's docstring. Nothing refuses an untagged test at
      this entry, but the review test set that a later entry ships refuses
      a TC with no tagged test. So tag before re-syncing past it. Fix any
      misplaced or malformed tag the check now reports, including a
      one-line docstring whose token follows prose. No setting and no
      registry schema changes, and your evidence cells stay as they are.
- [ ] **Not in this row**, stated in the RESYNC entry and the log: this
      repository's own tags (the migration follow-up), the derived review
      set and its refusals (row 2), the strict-mark commit check and
      `[bars] red_mark` (row 3), and the generated evidence column (item 5).
- [ ] Coverage bound: the promise reaches the test files, TC registries and
      `[paths] tests` declarations that supported workflows and the kit's
      own routes produce: a builder or an LLM-applied re-sync writing tags,
      a TC row authored or retired through a lane, and `bootstrap.py`'s
      scaffold. This follows `project-trajectory/PROCESS.md` §6 "Review
      threat model". Outside it: a non-Python test file whose fixture text
      opens a line with the token (the file-level arm reads every line, and
      the kit parses no other language); a test collected under a
      non-default pytest `python_files` or class pattern; hand-chosen
      aliases of a TC id (case, zero-padding); and a tests root reached
      through a symlink.
- [ ] WI-997, the tag-migration row, is filed on trunk before this row is
      claimed. It needs this row, seeds this repository's tags (Migration), and checks
      test-file tags and TC evidence cells equal as a strict finding, the
      check retired when item 5 generates the column (OI-125 Q1 (a)).
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Trust

A tag adds no authority to release, skip or pass anything: it can only add a
finding. Under `--strict` that finding refuses the commit bar, and an adopter's
gate from `DevStg-Impl`, so a test file takes part in a gate
(`project-trajectory/PROCESS.md` §3, "When a guard is owed"). Authority to
select tests arrives in row 2, whose `## Trust` section names this reader as
its producer. That is why this reader fails closed now.

- **Producers:** test files, written by a builder in a lane or by an
  LLM-applied re-sync. No script writes them. A failed write is a file left
  part edited: undecodable, unparseable, or a tag cut short.
- **Consumers:** the new reader in `gen_arch_map.py`, read through
  `trajectory_arch.py` by `check_trajectory.py`, which `run.cmd smoke` and
  `check.py` run. Nothing else reads it in this row.
- **Ruling, one for every consumer:** no tests root or no TC registry is
  vacuous; an untagged file is no finding; a valid tag maps its node ids; a
  misplaced, malformed or unknown tag is a finding naming file, line and shape;
  a file that cannot be decoded or parsed is a finding, never "no tags". A
  finding is a WARN, and an ERROR under `--strict`.

## Critique dispositions

Round 1 (fresh Sol, 2026-11-04): CHANGES-REQUESTED, three MINORs.

- **S2, adopted.** The Context's denial of gate authority is replaced by the
  `## Trust` section above, which reads "so a test file takes part in a gate"
  and consolidates the existing behaviour; no check is added.
- **S5, adopted.** The delta now reads "four values to the finding domain: a
  misplaced tag, a malformed tag, an unknown TC and an unreadable file".
- **S1, adopted.** The Done-when now reads "WI-997, the tag-migration row, is
  filed on trunk before this row is claimed", and WI-997 is filed with this
  disposition, needing this row. WI-995 needs WI-997, so it lands before row
  2's gate.

The S6 pre-answer's `needs` was stale beside the frontmatter and is corrected.

## Scope critique, pre-answered

- **S1.** There is one landable deliverable: the reader, its check and its
  regressions. The text, the spine rows and the RESYNC entry are true only
  once it lands, so they ride with it. The migration of this repository's
  tests is split off as its own row (Migration).
- **S2.** A tag can refuse a gate and can pass nothing (`## Trust`). Row 2
  carries the authority to select tests.
- **S3.** Closed coverage. Read positions are an enumerated set, every other
  declaration under the tests root is refused (deny by default), non-docstring
  string literals are excluded by construction (AST), and the four refusals
  are enumerated. The bound is stated in the Coverage bound item.
- **S4.** `single`: it touches two script families (`gen_arch_map`,
  `check_trajectory` / `trajectory_arch`) and promises behaviour over an
  input space.
- **S5.** Context, "Architectural delta". The change is in scope, on an
  existing seam.
- **S6.** `needs = ["OI-120", "OI-125"]`, the ruled calls that fix the token
  and the interim check. No
  queued row touches these files (grep of `docs/work/queued` and
  `docs/work/active`). It is stdlib only (`ast`, `tokenize`, `re`), with no
  ledger row.
- **S7.** No mechanism beyond the ruled reader and its refusals. Each
  refusal has a reachable scenario: a misplaced comment tag or a one-line
  docstring tag drops a test out of row 2's set with no word; a retired TC
  leaves a dangling tag; an unparseable file would read as "no tags".
- **B4.** No owner act and no credential in this row.
