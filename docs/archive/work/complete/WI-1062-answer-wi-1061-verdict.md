+++
id = "WI-1062"
title = "WI-1061's verdict answered: SR-251's chain states its live scope, the keyless condition and an all-or-nothing write"
workstream = "process"
specref = ""
sr_refs = ["SR-251"]
needs = []
buildtier = "medium"
planmode = "none"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Built on the maintenance branch `maint/wi-1062`, cut from `refactor_again`
at `3db0c6823`, with the commit hooks on and planning `none`, as the row
states. No id minted, no status moved and no act taken. No decisions
record: every choice made is stated by a spine row. The specref (WI-1061's
verdict) is cleared at close, as a terminal row's is.

- `6c082f5d5`: the build: SR-251's, LLR-406's and TC-483's text, the writer
  swap, the three tests, the regenerated evidence and the regenerated views.
- The commit after it: this close-out, carrying also the RESYNC entry the
  writer swap owes. `check_resync.py` is a smoke step, not a hook step, so
  the build commit passed its hook without one, and the smoke step refused
  the build's tree until the entry was added (Tests, below).
- `4eb965137`: a correction of this Deliverable's hook step count.
- The commit after it: the coordinator's addition before review, item 6
  below: the writer keeps a leading byte-order mark, with its test, TC-483's
  text, the evidence, the RESYNC entry's sentence and this record.

**1. SR-251.** `requirement` now reads "When requested, the delivered
harness shall rewrite the parts under the declared tests root of the
evidence cell of each test case the test-case registry holds as the test
files' declarations of that case make them, keeping every other part of the
cell as written." One `shall`, the trigger in front. The acceptance criteria
gain two clauses: "a run reports the cases it changed, and a declaration
naming a case the test-case registry does not hold adds nothing to the
registry and is not reported as changed", and "a rewrite interrupted while
it writes leaves the registry's bytes as they were before it or as fully
rewritten, never partly written". The first half of the first clause states
the report LLR-406 already described, so that "not reported as changed"
has a report to stand outside of. The rationale gains why the scope stops at
the registry (a retired case leaves it, and a test file still declaring it
is the declaration rule's finding under SR-157, not this writer's) and why
the file is replaced whole; "in place" is gone from it. The coincident is
unchanged: it describes the trace the column carries and agrees with both.
`trace.py --strict` counts 419 absolute-term advisories before and after
(SR 138), and SR-251 has none: each `never` it carries sits in a clause that
names the registry.

**2. LLR-406.** Its first sentence opens "For each test case the test-case
registry holds", SR-251's words, and "live" is gone from the row. It adds
"A declaration naming a case the test-case registry does not hold adds
nothing to the registry."; "a case with no evidence key gains one only when
its declarations supply a part, so a keyless case no declaration names stays
keyless and unchanged"; "The registry is then replaced whole by an
all-or-nothing write: the rewritten registry is written in full beside it
and moved into its place in one step, and a move that fails leaves the
registry's bytes as they were and no copy beside it, so an interrupted write
leaves the registry as it was or as fully rewritten, never partly written.";
and the command "reports the cases it changed, a case the test-case registry
does not hold never among them". The rationale says why the scope, the
keyless condition and the whole replacement hold. LLR-406's flip held under
WI-1057's verdict is void, as the Context states; the row goes to the next
sitting with its chain.

**3. The writer.** `write_evidence` in
`project-trajectory/scripts/arch_tags.py` ends with `write_atomic(path,
text)`, imported from `kitlib.observation`, in place of
`path.write_text(text, encoding="utf-8", newline="")`. Both modules are
CMP-006, so the call crosses no component boundary; IF-315 is the contract
it calls, and `tests/test_import_layers.py` passes. The stop rule did not
fire. The text is the one the writer built from the lines it read, joined
with the line end it read (`\r\n` or `\n`); `write_atomic` opens its
temporary file with `newline="\n"`, which translates nothing, and writes
UTF-8, as the in-place write did. An ad hoc check outside the repository,
not committed, regenerated a CRLF registry holding a non-ASCII comment and a
multi-line string through the tip's writer: the bytes came back as written
less the one changed cell, with no bare LF, and nothing was left beside the
registry. No second writer. The module's, `evidence_regen`'s and
`write_evidence`'s docstrings say what the code now does. A leading
byte-order mark is kept too, since item 6.

**4. Tests**, in `tests/test_llr_trace_cells.py`, each tagged TC-483:

- (a) `test_a_declaration_naming_a_case_the_registry_does_not_hold_adds_nothing`:
  a test file declares TC-009, which the registry does not hold, beside a
  stale TC-001. The registry reads as written with TC-001's cell rewritten
  and nothing else, and the command prints
  `trace: evidence regenerated for TC-001` alone.
- (b) `test_a_keyless_case_no_declaration_names_stays_keyless_and_unchanged`:
  TC-002 has no evidence key and no test declares it, beside a current
  TC-001. The command's output does not name TC-002, and the registry's
  bytes are unchanged.
- (c) `test_a_failed_replacement_leaves_the_registry_and_no_copy_beside_it`:
  the replace step `write_atomic` takes as an argument is substituted by
  one that records its source and target and raises `OSError`. The registry
  writer, called directly, raises it; the substitute saw one call, from a
  file in the registry's own directory holding the full rewrite, to the
  registry; the registry's bytes are unchanged and its directory holds the
  registry alone.

(c) calls the writer rather than the command: the command reaches its own
instance of the module, which a substitution on the test's instance does
not touch. Its first draft drove the command; the base red below is the
substitution's own line, which fails before any call, so it stands for
both drafts, and the in-place red was run on the test as committed.

**Red first, (c).** At the base, the three tests: (a) and (b) passed, and
(c) failed with `E       AttributeError: module 'arch_tags' has no
attribute 'write_atomic'`, `1 failed, 2 passed, 20 deselected in 7.61s`.
With the import added and today's in-place write kept, (c) failed with
`E       Failed: DID NOT RAISE OSError` (the in-place write went through
with no replace step), `1 failed, 22 deselected in 0.54s`. With the write
swapped it passes.

**Bite, (a) and (b).** Both passed on the code as it stood: the behaviour
existed. Each was shown red under temporary mutations of `arch_tags.py`,
applied by a scratch script outside the repository, run, then reverted by
copying back the built file and confirming it identical with `cmp`; none was
committed. Each module count is the whole of `tests/test_llr_trace_cells.py`
under that mutation, after the evidence was regenerated.

| Mutation | Red line | Module |
|---|---|---|
| a1: the tags are read for every declared id, and `evidence_regen` returns a cell for one the registry does not hold; the writer writes nothing for it | `E       AssertionError: assert ['trace: evid...-001, TC-009'] == ['trace: evid...d for TC-001']` | `1 failed, 22 passed in 6.34s`: (a) alone |
| a2: as a1, and the writer appends a table for that case at the registry's end, the re-read guard off | `E       assert '[test.TC-001.../test_r.py"\n' == '[test.TC-001.../test_a.py"\n'`, the diff `+ [test.TC-009]`, `+ evidence = "tests/test_r.py"` | `2 failed, 21 passed in 6.05s`: (a) and the quoted-key test |
| b1: a keyless case is returned as changed whatever its declarations, and the writer gives it `evidence = ""` | `E       AssertionError: assert 'arch_tags: REFUSED - the evidence rewrite of ...\docs\test\test-cases.toml did not re-read as the generated cells and nothing else; nothing written' == 0` | `1 failed, 22 passed in 6.17s`: (b) alone, the re-read guard refusing the empty key |
| b2: as b1, the re-read guard off | `E       AssertionError: assert 'TC-002' not in 'trace: evid...for TC-002\n'` | `2 failed, 21 passed in 5.88s`: (b) and the quoted-key test |
| b3: as b2, and the writer reports only the cases left with a part | `E       assert b'[test.TC-00...idence = ""\n' == b'[test.TC-00...= "Drafted"\n'` | `3 failed, 20 passed in 5.82s`: (b), the emptied-cell test and the quoted-key test |

**5. TC-483's text and evidence.** `method` adds "regenerate a registry
whose one case names a removed test while another test file declares a case
the registry does not hold; regenerate a registry holding a current case and
a case with no evidence key that no test file declares; through the
registry writer, regenerate a case naming a removed test with the step that
moves the rewritten registry into place made to fail". `expected` adds "The
case the registry does not hold adds nothing: the registry's bytes change in
the stale case's cell alone, and the command names that case alone. The
keyless case no test file declares stays keyless, the command does not name
it, and the registry's bytes are unchanged. With the move failing, the
rewritten registry had been written in full beside the registry, the
registry's bytes are unchanged and no copy is left beside it."
`trace.py --root . --regen-evidence` printed `trace: evidence regenerated
for TC-483` and appended the three tests to its cell; that run went through
the new write, and the registry's diff was that one line.

**The three rows side by side.** LLR-406 against SR-251: the same scope
words ("each test case the test-case registry holds", "a case the test-case
registry does not hold"); the keyless condition is LLR-406's detail of
SR-251's "a declared test the cell lacks is added" and "a run over cells
already current changes nothing", a keyless case no declaration names being
current already; the whole replacement is SR-251's interrupted-rewrite
clause, the copy beside the registry and the failed move being LLR-406's
detail of it; both state the report of changed cases. TC-483 against both:
each clause its expected adds is a clause of LLR-406, and each clause the
verdict named is driven:

| Clause (SR-251 acceptance, LLR-406) | TC-483 test |
|---|---|
| each case the registry holds; a declaration naming a case it does not hold adds nothing and is not reported | (a) |
| a run reports the cases it changed | the emptied-cell test, the keyless-case test, (a) |
| a keyless case gains a key only when its declarations supply a part, and one no declaration names stays keyless and unchanged | the keyless-case test, (b) |
| replaced whole: written in full beside it, moved in one step; a failed move leaves the bytes and no copy | (c) |
| an interrupted rewrite leaves the bytes as before or as fully rewritten | (c) for before; each writing test for fully rewritten |
| a run over current cells changes nothing | the evidence-column test, (b) |

The clauses earlier sittings judged are driven as WI-1058's table states. No
text this row writes names a code file, function, symbol or flag.

**6. The byte-order mark (the coordinator's addition before review).** The
writer read the registry with a leading byte-order mark stripped and wrote
UTF-8 without one, at the base as after the writer swap (an ad hoc check,
not committed, regenerated a registry opening with one through each). A
registry is hand-authored and a Windows editor can leave one, so for such a
file LLR-406's "keeps every other byte of the registry" was false by three
bytes. The coordinator ruled it fixed here, inside the row's own stated
behaviour, rather than filed.

- **The writer.** `write_evidence` reads the registry as UTF-8, sets a
  leading mark aside before splitting the lines (`removeprefix`, the mark
  being what it removed), and writes it back in front of the rewritten
  text: `write_atomic(path, bom + text)`. A file without one gains none.
  `write_atomic` is unchanged: it encodes the text as UTF-8, and the mark's
  character encodes to the same three bytes. The re-read guard reads the
  text without the mark, as before. A first form set the mark with a
  conditional expression; the hook's `complexity` step refused it
  (`check_complexity: FAIL - project-trajectory/scripts/arch_tags.py::write_evidence cognitive None -> 16. SIMPLIFY`),
  so the branch was taken out rather than the baseline bumped, and the
  step then read `check_complexity: OK - 171 row(s) over 15, unchanged
  from baseline.`
- **The test**, tagged TC-483:
  `test_a_registry_opening_with_a_byte_order_mark_keeps_it`. A registry
  opening with the mark holds a comment, a current TC-001 and a stale
  TC-002. The command prints `trace: evidence regenerated for TC-002`
  alone, and the registry's bytes are the mark followed by the text as
  written with TC-002's cell alone rewritten.
- **Red first**, against the writer as `4eb965137` holds it:
  `E       assert b'# Test case.../test_b.py"\n' == b'\xef\xbb\xb.../test_b.py"\n'`,
  `At index 0 diff: b'#' != b'\xef'`,
  `1 failed, 23 deselected in 0.56s`. Green once the writer keeps the mark.
  The ad hoc CRLF and mark checks above, rerun on the fixed writer: the CRLF
  registry came back as before, and the mark was kept.
- **TC-483.** `method` adds "regenerate a registry that opens with a
  byte-order mark and holds a comment, a current case and a stale case";
  `expected` adds "The registry that opens with a byte-order mark keeps it
  and every other byte, its stale case's cell alone rewritten, and the
  command names that case alone." Evidence regenerated from the tags:
  `trace: evidence regenerated for TC-483`.
- **No new clause.** LLR-406's "keeps every other byte of the registry" and
  SR-251's "only those cells of the test-case registry change" each cover
  the mark, which is a byte of the registry and no cell, so neither row
  changes. The expected clause claims nothing beyond them.

| Clause (SR-251 acceptance, LLR-406) | TC-483 test |
|---|---|
| only those cells change; every other byte of the registry is kept, a leading byte-order mark included | the keyless-case test, the byte-order-mark test |

Checks for item 6, on its tree before its commit (base `4eb965137`):

- `tests/test_llr_trace_cells.py`, `tests/test_import_layers.py`,
  `tests/test_module_size_ratchet.py` and `tests/test_dogfood_sync.py`:
  `79 passed, 1 skipped in 15.30s`, on the writer as committed (and
  `79 passed, 1 skipped in 17.92s` on its first form).
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_llr_trace_cells.py tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_dogfood_sync.py" rev="4eb965137 with item 6's change" -->
- The other two modules importing `arch_tags`, `tests/test_trajectory_arch.py`
  and `tests/test_gen_arch_map.py`: `283 passed in 123.00s (0:02:03)` on
  the writer as committed.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_trajectory_arch.py tests/test_gen_arch_map.py" rev="4eb965137 with item 6's change" -->
- `trace.py --root . --strict`, exit 0: `orphans=0 integrity=0`, 419
  absolute-term advisories (SN 31, SR 138, LLR 250), unchanged.
  `check_trajectory.py --root . --strict`: `check_trajectory: clean (1059
  work item(s), 930 done (88%), 37 cancelled, graph acyclic).`
  `check_resync.py`: `check_resync: OK, 1 shipped path(s) changed; entry
  anchored at 3db0c68236b6aa3355ebebc20d887c0e03224d32`, the entry gaining
  one sentence on the mark.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict; python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="4eb965137 with item 6's change" -->
- `run_menu.py smoke`, exit 0: `trace.py --strict` `orphans=0
  integrity=0`; `check_trajectory: clean (1059 work item(s), 930 done
  (88%), 37 cancelled, graph acyclic).`; `check_docs: OK - 3669 doc(s),
  3827 intra-repo link(s), 0 broken.`; `check_resync: OK, 1 shipped path(s)
  changed; entry anchored at 3db0c68236b6aa3355ebebc20d887c0e03224d32`; the
  tier `3755 passed, 3 skipped, 18 warnings in 93.81s (0:01:33)`, on the
  writer as committed. Its budget line reads CPU 568.1 s against 540, a
  WARN only; wall 94.5 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="4eb965137 with item 6's change and its regenerated views" -->
- Byte deltas from `4eb965137`: `docs/test/test-cases.toml` +354,
  `project-trajectory/scripts/arch_tags.py` +191,
  `tests/test_llr_trace_cells.py` +1,195,
  `project-trajectory/RESYNC_PACK.md` +129; none budgeted or watched.
  <!-- fig: derived="git cat-file -s at 4eb965137 against the working-tree size before item 6's commit" -->

**Tests.** pytest ran under the worktree's Python 3.11, its temporary files
under `%TEMP%`.

- `tests/test_llr_trace_cells.py` at the base, before any change:
  `20 passed in 7.92s`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_llr_trace_cells.py" rev="3db0c6823" -->
- `tests/test_llr_trace_cells.py`, `tests/test_trajectory_arch.py` and
  `tests/test_gen_arch_map.py` (the modules importing `arch_tags`, and
  `trace.py --tests-for`'s list for it), with `tests/test_import_layers.py`,
  `tests/test_module_size_ratchet.py` and `tests/test_dogfood_sync.py`:
  `361 passed, 1 skipped in 132.90s (0:02:12)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_llr_trace_cells.py tests/test_trajectory_arch.py tests/test_gen_arch_map.py tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_dogfood_sync.py" rev="6c082f5d5 (its tree before the commit, the views not yet regenerated)" -->
- After the RESYNC entry, `tests/test_resync_pack.py` and
  `tests/test_check_resync.py`: `38 passed in 11.84s`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_resync_pack.py tests/test_check_resync.py" rev="6c082f5d5 with the close-out's RESYNC entry" -->
- `trace.py --root . --strict`, exit 0: `orphans=0 integrity=0`, 419
  absolute-term advisories (SN 31, SR 138, LLR 250), as at the base.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="3db0c6823 and 6c082f5d5 (its tree before the commit)" -->
- `check_trajectory.py --root . --strict`, exit 0:
  `check_trajectory: clean (1059 work item(s), 929 done (88%), 37 cancelled, graph acyclic).`
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="6c082f5d5 (its tree before the commit)" -->
- `scripts/check_resync.py` on the build's tree:
  `check_resync: REFUSED project-trajectory/scripts/arch_tags.py: no RESYNC_PACK.md entry added for this change`;
  with the entry: `check_resync: OK, 1 shipped path(s) changed; entry
  anchored at 3db0c68236b6aa3355ebebc20d887c0e03224d32`.
- The commit hook passed on `6c082f5d5`, each of its 29 steps `PASS`. On
  the close-out `9c30268a7` it first refused (`status-map` and
  `trajectory-map`: the spec's move left `docs/status.md` and
  `PROJECT_STATE.html` stale), then passed, all 29 steps, once
  `trunk_step.py --root . --regen` had regenerated them.
- `run_menu.py smoke`, exit 0, with the close-out's tree: `trace.py
  --strict` `orphans=0 integrity=0`; `check_trajectory: clean (1059 work
  item(s), 930 done (88%), 37 cancelled, graph acyclic).`; `check_docs: OK -
  3669 doc(s), 3827 intra-repo link(s), 0 broken.`; `check_resync: OK, 1
  shipped path(s) changed; entry anchored at
  3db0c68236b6aa3355ebebc20d887c0e03224d32`; the tier
  `3754 passed, 3 skipped, 18 warnings in 127.52s (0:02:07)`. Its budget
  line reads CPU 773.1 s against 540, a WARN only, not charged to the lane;
  wall 128.3 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="6c082f5d5 (with the close-out's tree, before its commit)" -->
- `check_docs.py --root .` after the move: `check_docs: OK - 3669 doc(s),
  3827 intra-repo link(s), 0 broken.` The moved spec holds no relative
  link.
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root ." rev="6c082f5d5 (with the close-out's tree, before its commit)" -->

**Byte deltas** (none budgeted or watched), base `3db0c6823` to
`6c082f5d5`: `docs/requirements/system-requirements.toml` 323,468 ->
324,121 (+653), `docs/requirements/low-level-requirements.toml` 564,152 ->
565,065 (+913), `docs/test/test-cases.toml` 704,135 -> 705,245 (+1,110),
`project-trajectory/scripts/arch_tags.py` 15,093 -> 15,667 (+574),
`tests/test_llr_trace_cells.py` 28,148 -> 31,529 (+3,381); and in the
close-out, `project-trajectory/RESYNC_PACK.md` 758,126 -> 759,566 (+1,440).
<!-- fig: derived="git cat-file -s at 3db0c6823 and 6c082f5d5; the RESYNC pack's working-tree size before the close-out's commit" -->

**Owed to the next sitting:** the first acceptances of SR-251, LLR-406 and
TC-483, the chain whole.

**Left as found:**

- trace's advisory that SR-251 declares no `form`, as WI-1058 left it.
- TC-483's closing clause that every cell of this repository's registry is
  current, as WI-1058 left it.
- The hook's `readability` step warns, report-only and not gating,
  `flag-axis worsened project-trajectory/scripts/arch_tags.py:
  boolean-literal call sites 0 -> 2 (+2)` on each commit touching the
  module. The two sites are the registry loads passing `False`, which the
  base already held; this row added none, so the module's missing entry in
  the flag-axis baseline is the base's, not this change's.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, to answer
the fifth automated adjudication sitting's verdict (WI-1061, Gemini Neon,
the specref). That sitting judged SR-251's chain whole, after WI-1058
answered the fourth sitting's two returns, and returned all three rows.
Its `### Dispositions` draft names this row's scope.

The findings, in short (the specref quotes them in full):

- **SR-251 and LLR-406 disagree on scope.** SR-251 rewrites "each test
  case's evidence cell", while LLR-406 rewrites "each live test case". The
  sitting asks both to say the same thing, and to say what happens to a
  case outside that scope.
- **LLR-406's keyless clause is unconditional.** "A case with no evidence
  key gains one" contradicts the identity clause for a keyless case that no
  declaration names. It gains a key only when a declaration supplies a part.
- **No all-or-nothing write.** SR-251 carries the integrity-recoverability
  concern (`hat_refs`) for a registry rewritten in place, but neither row
  says what an interrupted write leaves behind.
- **TC-483** verifies none of the three.

**What "live" means here, as the code reads it.** The regeneration reads
the cases the test-case registry holds. A retired case is deleted from the
registry, so no row stays behind for the rewrite to touch. The case outside
the scope is a test file that still declares a case the registry no longer
holds. The rewrite adds no row for it and names no such case. The rows
state it that way, and the test drives it.

**The write.** Today the writer writes the registry in place. The kit
already has one all-or-nothing file writer (`kitlib/observation.py`'s
`write_atomic`, under SR-199 and LLR-234): it writes a temporary file
beside the target, then moves it into place in one replace. The registry
writer reuses it rather than adding a second one. It keeps the file's own
line endings, which the writer reads and writes back. If reusing it would
cross a component boundary that no interface row declares, the builder
stops and reports before writing one.

**LLR-406 and WI-1057's held flip.** The fourth sitting accepted LLR-406
and the fifth returned it. Its flip, held under WI-1057's verdict, is
therefore void: no act takes it from that verdict. LLR-406 goes to the next
sitting with its chain, and its flip comes from that sitting's verdict.

**Why one row.** As at WI-1058, the sitting judges the chain whole, so the
three rows' repairs land together as one branch before the next sitting.
**Planning** is `none`: one writer swap, wording settled here, and tests
stated below.

## Done-when

- [x] SR-251's requirement and acceptance criteria scope the rewrite to the
      test cases the registry holds. A declaration naming a case the
      registry does not hold adds nothing and is not reported as changed.
      The acceptance criteria add that an interrupted rewrite leaves the
      registry's bytes as they were before or as fully rewritten, never
      partly written. One `shall`, the event trigger kept in front.
- [x] LLR-406 says the same about scope, gives a case with no evidence key
      a key only when its declarations supply a part (a keyless case no
      declaration names stays keyless and unchanged), and states that the
      registry is replaced whole by an all-or-nothing write.
- [x] The registry writer writes through the kit's one all-or-nothing file
      writer, keeping the file's line endings and encoding. No second
      writer is added.
- [x] Tests, each tagged TC-483: a declaration naming a case the registry
      does not hold changes nothing and is not named; a keyless case that no
      declaration names stays keyless and the registry's bytes are
      unchanged; a replace step that fails leaves the registry's bytes
      unchanged and no temporary file behind. A new behaviour is shown
      failing first; one that already holds is shown to bite by a mutation,
      recorded in the Deliverable and never committed.
- [x] TC-483's method and expected name the three cases, with evidence
      regenerated from the tags. No text this row writes names a code file,
      function, symbol or flag; each child stays inside its parent. The
      Deliverable lists the rows owed to the next sitting: SR-251, LLR-406
      and TC-483 first acceptances.
