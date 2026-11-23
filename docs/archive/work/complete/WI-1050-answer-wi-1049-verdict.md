+++
id = "WI-1050"
title = "WI-1049's verdict answered: LLR-257 re-amended without code names, TC-457, TC-468 and TC-475 made ready"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-217"]
needs = ["WI-1023"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1050`, cut from `refactor_again` at
`5d3a7c52c`, with the commit hooks on. No status moved, no act was taken and
no id was minted. The specref (WI-1049's verdict) is cleared at close, as a
terminal row's is. No decisions record was needed: TC-475's choice was
settled at the scope critique, and nothing else called for a design call.

- `de2c1de3b`: LLR-257's Detail, TC-457 and its new test, TC-468's Method,
  TC-475 narrowed and TC-428's and TC-429's `Verifies`, the tests' tags,
  the regenerated evidence and the regenerated views. The hook passed (29
  steps, all PASS).
- The commit after it: the close-out, this Deliverable, the move to
  `complete/` and the log fragment.

**LLR-257** (Accepted; Detail only, so it drifts). The Detail re-lands
WI-1042's amendment (`468c91fd9`) sentence by sentence, with every carrier
name taken out, the accepted text's own included, so the cell names no code
file, function, module or symbol. It states what `468c91fd9` states:

- the acceptance-record reading: when each requirement, and each pair of a
  test case and a requirement it names, was first accepted is read from the
  acceptance record, never by replaying the registries, over the commits
  that wrote the act ledger or the record's copies at its current path.
  "record_acceptances takes ... (baseline_snapshot's one ledger walk, given
  those copies)" now reads "found by the act ledger's one history walk
  widened to those copies", and each commit's copies are read against every
  parent's "through the shared row reader and acceptance-act rule" (it named
  the module holding them);
- the re-pointing date: a pair is new at the act whose copy first holds the
  test case accepted while it names the requirement, directly or through a
  design row, so a re-pointing is dated at the act that re-accepts it; a
  side-branch act is ordered where it reached trunk and named by its own
  commit;
- the cut rule, in its own words where `468c91fd9` cited a bare `(D3)`:
  nothing before the record's first commit at its current path is read, in
  any earlier spelling, "since no reader is kept for a spelling the record
  has left behind and its history is cut cleanly there rather than
  translated"; what the cut's copies carry is at or before it while its
  ledger records an act, and unread beside no ledger, an empty one or a
  malformed one;
- the gap rule: a commit that flips a row or brings a new pair without a
  ledger entry, or whose ledger or its parent's is malformed, is a gap whose
  content is unread, never a pass and never dated at a later act, as is a
  row reading accepted at the tip that no act accepted.

The rest is `468c91fd9`'s, its function names restated as what they do: the
start (`[checks] test_first_since`, "read as text" where it named the reader
it sits beside), the landing (an `Implements:` line read with "the one
back-link grammar the reverse back-link scan defines" where it named the
generator), the judgement, the unreadable cases, and "The harness's checks
gain a warn-only built-in step `test-first`" where it named the harness
script. No obligation is added or dropped. The test-first check is
unchanged since `468c91fd9`, and so is the back-link grammar; the edits F-3
made since in the record's readers (a comment, two docstrings, and the
snapshot copy read with its retired cells) leave every rule LLR-257 states
as it was. The commit hook warns, as it should, that the amendment rides as
snapshot drift until the sitting, and that LLR-257's `Hat-Refs` did not
move with its Detail; the row carries no `Hat-Refs` cell, and its
perspective did not change, so none was added.

**TC-457** (Drafted; Method, Expected, Evidence). LLR-396's clause "A file
that cannot be read or decoded is absent" now has a test,
`test_a_file_that_cannot_be_read_or_decoded_is_absent`
(`tests/test_component_headers.py`, tagged `TC-457`): a path that cannot be
read (a directory stands at it, the repository's usual unreadable fixture)
and a file whose bytes are not UTF-8 though it holds an exact declaring
line, each once as a Python module and once as a shell script, so both of
the reader's carriers are driven. Each reads as absent ("declares no
component"), and the read raises nothing. The Method gains the four files
and the Expected their outcome; the Evidence, regenerated from the tags,
gains the test.

**TC-468** (Drafted; Method only). "Driven on real git repositories whose
acts are taken with copy_live" now reads "Driven on real git repositories in
which each acceptance act is taken as the kit takes one: the registries'
copies are written into the acceptance record and the act's entry is
appended to its ledger, in the act's own commit", which is what the tests'
act helper does.

**TC-475, TC-428, TC-429** (the scope critique's choice). TC-475 (Drafted)
keeps only the failing-test case. Its Method writes one Accepted automated
case and one test that validly declares it and fails, runs the test to see
it fail, then runs the trajectory check under strict checking; its Expected
reads the case clean (no undeclared-case finding, no Evidence equality
finding, exit 0), since the rule reads declarations, not test outcomes. The
thirteen tests TC-428 and TC-429 cite carry only their own tag (`TC-428` or
`TC-429`, already there beside `TC-475`), and the module comment above them
says which case pins what. TC-475's regenerated Evidence is the one test,
`test_a_declared_test_that_fails_leaves_its_case_clean`; TC-428's and
TC-429's Evidence regenerated byte-identical. TC-428 and TC-429 (Accepted)
read `Verifies = SR-157; LLR-395`, no other cell changing. LLR-395's
`test_refs` already read `TC-475; TC-428; TC-429`.

**No code names in row text.** No text this branch writes names a code
file, function, module or symbol. The one identifier-shaped token in
LLR-257 is the process settings key `[checks] test_first_since`, a
configuration key an adopter sets.

**Red first.** The new test passed on its first run
(`1 passed, 13 deselected in 0.24s`), since the reader already catches both
errors. It was then shown to fail under three mutations of the component
reader in `gen_arch_map.py`, each reverted before any commit: the docstring
reader without its read guard, `1 failed, 13 deselected in 0.36s` (the
unreadable module raised); the header reader without its read guard,
`1 failed, 13 deselected in 0.41s` (the unreadable shell script raised
`PermissionError`); both guards narrowed to `OSError`,
`1 failed, 13 deselected in 0.40s` (the undecodable module raised
`UnicodeDecodeError`).

**Tests.**

- No script module changed, so no other module imports a changed one. The
  modules holding the tests tagged TC-428, TC-429, TC-457, TC-468 and
  TC-475 (`test_trajectory_arch`, `test_component_headers`,
  `test_check_test_first`), the registry readers `test_cell_classes`,
  `test_evidence_join`, `test_parent_first` and `test_id_watermark`, and the
  whole-tree tests `test_import_layers`, `test_module_size_ratchet` and
  `test_dogfood_sync`:
  `399 passed, 1 skipped, 18 warnings in 118.73s (0:01:58)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 12 --basetemp D:/rt1050/t <the 10 modules listed>" rev="de2c1de3b (its tree before the commit)" -->
- `trace.py --root . --strict`: `orphans=0 integrity=0` (exit 0).
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="de2c1de3b (with the close-out's tree, before its commit)" -->
- `check_trajectory.py --root . --strict`, exit 0:
  `check_trajectory: clean (1051 work item(s), 920 done (88%), 37 cancelled, graph acyclic).`
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="de2c1de3b (with the close-out's tree, before its commit)" -->
- `scripts/check_resync.py`: "OK, no shipped path changed", so no RESYNC
  entry is owed.
- The commit checks, `run_menu.py smoke`, exit 0:
  `3724 passed, 3 skipped, 18 warnings in 144.86s (0:02:24)`. Its budget line reads CPU 785.9 s against 540, a WARN only, not
  charged to the lane; wall 145.6 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="de2c1de3b (with the close-out's tree, before its commit)" -->

**Byte deltas** (none budgeted or watched):
`docs/requirements/low-level-requirements.toml` 560,183 -> 561,276 (+1,093);
`docs/test/test-cases.toml` 695,822 -> 693,716 (-2,106);
`tests/test_component_headers.py` 13,110 -> 14,085 (+975);
`tests/test_trajectory_arch.py` 141,397 -> 141,339 (-58).

**What the third sitting owes from this branch.**

- LLR-257's amendment (Detail; a drifted `Accepted` row): the text WI-1049
  ruled MEANING and would not bless, now without `record_acceptances`,
  `baseline_snapshot`, the bare `(D3)` or any other carrier name.
- TC-428's and TC-429's `Verifies` change (each adds LLR-395), a routed
  traced change on accepted rows.
- The first acceptance of TC-457 (verifying LLR-396), TC-468 (LLR-257) and
  TC-475 (LLR-395), the three rows WI-1049 returned.

LLR-244's amendment is F-3's (WI-1023), taken at its merge; the same sitting
judges it beside LLR-257.

**Review** (the coordinator, 2026-11-22; queue-drill HANDOFF §4 step 4).
Round 1 over `5d3a7c52c..11f981f61`, the generated views and this spec's
copies withheld and the spec at the tip given whole, each reviewer told to
judge every changed row as the third sitting will and given LLR-257's text
at `468c91fd9` and its accepted text to compare clause by clause. Gemini
Hydrogen (`gemini-4-hydrogen-low`, the Antigravity CLI) read the prose:
APPROVE, no findings. OpenAI Sol (`gpt-6.1-sol`, low) read the whole diff:
one MAJOR and one NIT. The MAJOR (TC-457's `evidence` names a test file and
function, against the no-code-names rule) is dismissed: `evidence` is the
generated pointer cell whose content is test node ids by definition
(`trace.py --regen-evidence` writes it from the test files' tags), and the
rule the sittings apply covers the prose cells; WI-1049's sitting accepted
sixteen test cases whose evidence names test functions. The NIT (the log
fragment said one test module changed; two did) is fixed with this record.

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, to answer
the second automated adjudication sitting's verdict (WI-1049,
`docs/reviews/wi-1049-adjudicate-second-sitting/001-ADJUDICATE-d5cb626.md`,
Gemini Neon). The sitting blessed 23 amendments and accepted 22 rows, but
ruled two amendments MEANING without the bless mark and returned three test
cases. Its act was refused (SR-207) while the two unblessed rows drifted in
the design registry it copies.

**The operator's ruling (2026-11-22, given in the coordinator's session):**
revert the two unblessed amendments to their accepted text, take WI-1049's
act, and re-land both amendments through this row, with the returned rows
answered, for a third sitting. So, in the commit that files this row,
LLR-244's and LLR-257's `detail` went back to the text the accepted copy
records. The amended text is at `468c91fd9`
(`git show 468c91fd9:docs/requirements/low-level-requirements.toml`): F-2's
(WI-1022) for LLR-244 and WI-1042's for LLR-257. Until they are re-landed,
both rows describe the code as it was before those items.

**LLR-244 moved to F-3 (WI-1023), 2026-11-22.** F-3 amends LLR-244 again on
top of F-2's text, so its review round 1 took the finding (its F5): F-3
rewrites LLR-244's `detail` with F-2's and its own behaviour and no code
names, and the coordinator takes that text at F-3's merge. This row keeps
LLR-257 and the three returned test cases. It lands after F-3 (`needs`),
so that the third sitting judges both rows together, and its repairs land
together in one branch, since one sitting judges them in one act.

**TC-475's choice, settled at the scope critique (2026-11-22).** Both
critics chose, and the coordinator adopted, the narrower of the verdict's
two ways: TC-475 keeps only the failing-test case (a validly declared test
that still fails leaves its case clean), and TC-428 and TC-429, both
`Accepted`, add LLR-395 to their `Verifies`, keeping their tests and their
homes. WI-1038's parent-first refusal no longer stands, since WI-1049's act
accepted LLR-395. The `Verifies` change is a routed traced change on
accepted rows, owed to the third sitting.

The findings, quoted from the verdict:

- **LLR-244** (MEANING, not blessed): "reachability moved from owner module
  to contract-body file with a files-mode component fallback, changing the
  obligation; NOT blessed because the amendment added a new implementation
  parameter symbol `homes` (`if_reached_srs(ifs, llrs, homes)` and
  `(homes, from the definition gate's scan)`), violating §0 ('an amendment
  adds no name the rule forbids') and §3."
- **LLR-257** (MEANING, not blessed): "acceptance provenance, re-pointing
  dating, cut handling and gap handling all changed; NOT blessed because the
  amendment added forbidden implementation carrier names
  (`record_acceptances` and `baseline_snapshot`) in violation of §0 and §3
  and introduced an unanchored external reference `(D3)` that a cold reader
  cannot resolve."
- **TC-457** (RETURN): "omits any case exercising LLR-396's explicit clause
  'A file that cannot be read or decoded is absent' ... add an
  unreadable/undecodable file case asserting it reads as absent."
- **TC-468** (RETURN): "its Method names the Python implementation function
  `copy_live` ... restate without `copy_live`."
- **TC-475** (RETURN): "copies verbatim all 10 evidence nodes and prose of
  live Accepted sibling TC-428 plus all 3 evidence nodes and prose of live
  Accepted sibling TC-429 while adding only one new test ... either retire
  TC-428 and TC-429 if TC-475 supersedes them, or narrow TC-475 to the
  failing-test case and point TC-428/TC-429 at LLR-395." WI-1038 was
  cancelled because the parent-first rule refused re-pointing accepted
  TC-428 and TC-429 at a `Drafted` LLR-395; WI-1049's act accepts LLR-395,
  so that refusal no longer stands.

## Done-when

- [x] LLR-257's `detail` states the acceptance-record reading, the
      re-pointing date, the cut rule and the gap rule that `468c91fd9`
      states, without `record_acceptances`, `baseline_snapshot` or a bare
      `(D3)`; a cut rule it keeps says what it is in its own words. Text
      only; its status stays `Accepted`.
- [x] TC-457 covers LLR-396's clause that a file which cannot be read or
      decoded is absent: a test drives an unreadable and an undecodable
      file through the declared-component reader and asserts each reads
      as absent without raising, and TC-457's Method, Expected and Evidence
      name the case.
- [x] TC-468's Method names no function, module or symbol.
- [x] The tests behind TC-428, TC-429 and TC-475 have one home each:
      TC-475's Method, Expected and Evidence name only the failing-test
      case, its other tests are no longer tagged to it, and TC-428 and
      TC-429 add LLR-395 to their `Verifies`, no other cell changing.
- [x] No row text this branch writes names a code file, function or symbol.
      The Deliverable lists every act owed for adjudication.
