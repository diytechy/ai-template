+++
id = "WI-1058"
title = "WI-1057's verdict answered: SR-251's trigger fronted, and TC-483 covers LLR-406's key insertion and sorted append"
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

Built on the maintenance branch `maint/wi-1058`, cut from `refactor_again`
at `8db60ba58`, with the commit hooks on and planning `none`, as the row
states. No id minted, no status moved and no act taken. No decisions
record: every choice made is stated by a spine row. The specref (WI-1057's
verdict) is cleared at close, as a terminal row's is.

- `f05b6fd78`: the build: SR-251's and TC-483's text, the two tests, the
  regenerated evidence and the regenerated views.
- The commit after it: this close-out.

**1. SR-251's trigger.** `requirement` now reads "When requested, the
delivered harness shall rewrite the parts of each test case's evidence cell
under the declared tests root as the test files' declarations of that case
make them, keeping every other part of the cell as written." One `shall`,
the event trigger fronted, nothing between `shall` and `rewrite`. Two
absolutes the absolute-term rule reported on this row are bounded by naming
their domain, the meaning unchanged: "every other part" becomes "every other
part of the cell" in the requirement, and "a rewrite that would change
anything else" becomes "anything else in the registry" in the acceptance
criteria. `trace.py --strict`'s absolute-term count fell from 421 to 419
(SR 140 to 138), and SR-251 has none left. The acceptance criteria,
rationale and coincident otherwise stand: each describes what a requested
run does, and none states the trigger differently. Every acceptance clause
is driven by a TC-483 test, item 4.

**2. A case with no evidence key gains one through the writer.**
`test_a_case_with_no_evidence_key_gains_one_and_no_other_byte_moves` runs
the regeneration command over a registry whose middle case, TC-002, has one
declared test and no evidence key. A header comment and a current case come
before it; it holds a multi-line prose cell with a line reading
`evidence = "tests/test_x.py"`; a closing comment and a current case come
after it. The command prints `trace: evidence regenerated for TC-002` alone,
the registry re-reads with TC-002's evidence `tests/test_b.py`, that key's
line appears once, and taking it out gives the registry's text as written,
byte for byte. The check does not fix where the line goes, so it asserts
what LLR-406 states (the case gains a key, every other byte is kept) and no
more. The existing emptied-cell test already gave a key to the last case of
a two-case registry; this one places the keyless case where a misplaced
line or a key read inside a string would show.

**3. Missing declared tests are appended in sorted order.**
`test_missing_declared_tests_are_appended_in_sorted_order` tags TC-001 on
three tests that one file defines in the order `test_c`, `test_a`,
`test_b`, and on `tests/test_z.py`, the one part the cell names, which sorts
after them. After the command the cell reads `tests/test_z.py;
tests/test_m.py::test_a; tests/test_m.py::test_b; tests/test_m.py::test_c`:
appended after the kept part, joined by `; `, in sorted order.

**4. TC-483's text and evidence.** `method` adds the two scenarios and
`expected` their outcomes: "The keyless case gains an evidence key naming
its declared test, the command names that case alone, and with that key's
one line taken out the registry's bytes are as written. The three missing
tests are appended after the named one, joined by a semicolon and a space,
in sorted order." Two inherited clauses are corrected under the row rules.
"The command names the case it changed" sat on the first registry, whose
test does not read the command's output; it now sits on the emptied-cell
scenario, whose test asserts the line naming both changed cases. "The
command exits 0" is cut: neither LLR-406 nor SR-251 states an exit code
(the test still asserts it). No text this row writes names a code file,
function, symbol or flag. LLR-406's text is unchanged: read upward against
the reworded SR-251 it states the same obligation in detail, its command
being the request. TC-483 claims nothing beyond the two. Every SR-251
acceptance clause and every LLR-406 clause the verdict named is driven:

| Clause | TC-483 test |
|---|---|
| a named tests-root part kept, an unnamed one removed, a missing declared test added | the evidence-column test; the two new tests |
| a part outside the root, a note, a part in an unreadable file kept | the evidence-column test |
| only those cells change; a case with no key gains one, every other byte kept | the evidence-column test; the keyless-case test |
| appended nodes joined by `; ` in sorted order, two or more | the sorted-append test |
| an emptied cell loses its key; the command names the cases it changed | the emptied-cell test |
| a rewrite that would change anything else is refused, nothing written | the quoted-key test |
| a run over current cells changes nothing | the evidence-column test |
| no registry or no tests root: nothing written, the input named | the missing-input test |

`trace.py --root . --regen-evidence` printed `trace: evidence regenerated
for TC-483`, appending the two new tests, in sorted order, after the four
already in its cell.

**5. Each test bites.** Both new tests passed on the code as it stood: the
behaviour exists. Each was shown to bite under a temporary mutation of
`project-trajectory/scripts/arch_tags.py`, run red, then reverted with
`git checkout --` and never committed. Each row's module count is the whole
of `tests/test_llr_trace_cells.py` run under that mutation, after the
evidence was regenerated.

| Mutation | Red line | Module |
|---|---|---|
| A1: `write_evidence` adds a blank line after the inserted key (`new + [""]`); the re-read guard passes it | `E  assert '# Test cases.../test_c.py"\n' == '# Test cases.../test_c.py"\n'`, the diff a `+ ` line after `"Drafted"` | `2 failed, 18 passed`: the new test and the emptied-cell test |
| A2: `_table_spans` stops tracking multi-line strings (`open_delim = None`), so the prose line reads as a key | `E  AssertionError: assert 'arch_tags: REFUSED - the evidence rewrite of ...\docs\test\test-cases.toml did not re-read as the generated cells and nothing else; nothing written' == 0` | `1 failed, 19 passed`: the new test alone |
| B1: `generated_evidence` sorts the appended nodes in reverse | `E  - .py::test_a; tests/test_m.py::test_b; tests/test_m.py::test_c"` against `E  + .py::test_c; tests/test_m.py::test_b; tests/test_m.py::test_a"` | `1 failed, 19 passed`: the new test alone |
| B2: `generated_evidence` joins with `;` and no space | `E  + test_z.py;tests/test_m.py::test_a;tests/test_m.py::test_b;tests/test_m.py::test_c"` | `2 failed, 18 passed`: the new test and the evidence-column test |

**Tests.** No kit module changed, so no importer runs beyond these.

- `tests/test_llr_trace_cells.py` at the base, before any change:
  `18 passed in 8.99s`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_llr_trace_cells.py" rev="8db60ba58" -->
- `tests/test_llr_trace_cells.py`, `tests/test_import_layers.py`,
  `tests/test_module_size_ratchet.py` and `tests/test_dogfood_sync.py`:
  `75 passed, 1 skipped in 11.68s`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_llr_trace_cells.py tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_dogfood_sync.py" rev="f05b6fd78 (its tree before the commit)" -->
- `trace.py --root . --strict`, exit 0:
  `orphans=0 integrity=0`, 419 absolute-term advisories (SR 138).
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="f05b6fd78 (its tree before the commit)" -->
- `check_trajectory.py --root . --strict`, exit 0:
  `check_trajectory: clean (1057 work item(s), 927 done (88%), 37 cancelled, graph acyclic).`
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="f05b6fd78 (its tree before the commit)" -->
- The commit hook passed on `f05b6fd78`.
- `run_menu.py smoke`, exit 0, with the close-out's tree: `trace.py
  --strict` `orphans=0 integrity=0`; `check_trajectory: clean (1057 work
  item(s), 928 done (88%), 37 cancelled, graph acyclic).`; `check_docs: OK -
  3663 doc(s), 3826 intra-repo link(s), 0 broken.`; `check_resync: OK, no
  shipped path changed`; the tier
  `3751 passed, 3 skipped, 18 warnings in 120.43s (0:02:00)`. Its budget
  line reads CPU 750.8 s against 540, a WARN only, not charged to the lane;
  wall 121.0 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="f05b6fd78 (with the close-out's tree, before its commit)" -->

**Byte deltas** (none budgeted or watched), base `8db60ba58` to
`f05b6fd78`: `docs/requirements/system-requirements.toml` 323,437 ->
323,468 (+31), `docs/test/test-cases.toml` 703,314 -> 704,135 (+821),
`tests/test_llr_trace_cells.py` 25,515 -> 28,148 (+2,633).
<!-- fig: derived="git cat-file -s at 8db60ba58 and f05b6fd78" -->

**Owed to the next sitting:** the first acceptances of SR-251 and TC-483.
LLR-406's text did not change, so its flip stays owed under WI-1057's
verdict and is not re-judged.

**Left as found:** trace's advisory that SR-251 declares no `form`
(SR-248 to SR-251 were filed without one, and the fourth sitting raised no
finding on it), and TC-483's closing clause that every cell of this
repository's registry is current, which the fourth sitting listed among the
row's claims without a finding.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, to answer
the fourth automated adjudication sitting's verdict (WI-1057, Gemini Neon,
the specref). That sitting blessed all nine amendments and accepted 16 of
18 rows. It returned two, both on SR-251's chain, and its `## Dispositions`
draft names this row's scope.

The findings, quoted from the verdict:

- **SR-251** (RETURN): "`Requirement` buries its event trigger between
  `shall` and the verb (`shall, on request, rewrite…`), which is the exact
  buried-condition trap §2(b2) forbids; because regeneration runs only on
  explicit request rather than ubiquitously during checks, front the
  trigger in event-driven EARS form (e.g., `When requested, the delivered
  harness shall rewrite…`)."
- **TC-483** (RETURN): it "leaves two explicit clauses of LLR-406
  unverified — (1) 'a case with no evidence key gains one' is exercised
  only in pure cell generation ('an empty cell with one declaration') and
  never through the TOML registry file writer inserting a new evidence key
  into a row that lacks one while preserving every other byte, and (2) 'a
  declared node the cell lacks is appended, joined by a semicolon and a
  space, in sorted order' is exercised with only a single missing declared
  node, leaving multi-node `; ` joining and sorted ordering unverified."

**LLR-406 is held.** The sitting ruled LLR-406 ACCEPT, and WI-1057's
derived act listed its flip. The commit hook's parent-first step refused
it under SR-251, which stays `Drafted`, so the act was taken without it.
Its flip stays owed under WI-1057's verdict. Once a later sitting accepts
SR-251, `compose_act` over that verdict lists it again, provided LLR-406's
text has not changed. So this row leaves LLR-406's text alone unless a fix
here needs it changed. If it does, LLR-406 goes back to a sitting with the
other rows.

Both rows are `Drafted`, so their text may change freely; neither is an
amendment.

**Why one row.** SR-251's wording and TC-483's two tests could each land
alone, but they land together as one branch before the fifth sitting. The
sitting judges SR-251's chain whole, and LLR-406's held flip waits on that
chain, so a sitting that saw only one of the two repairs would return the
chain again. **Planning** is `none`: the wording fix and two precisely
stated tests specify the whole diff.

## Done-when

- [x] SR-251's requirement opens with its event trigger ("When requested,
      the delivered harness shall ..."), with one `shall` and nothing
      between it and its verb. Its acceptance criteria, rationale and
      coincident still agree with it.
- [x] A test drives the regeneration through the registry writer over a
      test-case registry with a live case that has no evidence key. The
      case gains the key, and every other byte of the registry stays as
      written. It is tagged TC-483.
- [x] A test appends two or more missing declared tests, declared out of
      sorted order, to one case. They land joined by a semicolon and a
      space, in sorted order. It is tagged TC-483.
- [x] TC-483's method and expected name both cases, with evidence
      regenerated from the tags. No text this row writes names a code file,
      function, symbol or flag.
- [x] Each test is shown failing first, or, where the behaviour already
      exists, shown to bite by a mutation of the code it drives, recorded
      in the Deliverable and never committed. The Deliverable lists the
      rows owed to the next sitting: SR-251 and TC-483 first acceptances,
      LLR-406 only if its text changed.
