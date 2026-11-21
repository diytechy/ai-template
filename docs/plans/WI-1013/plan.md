# WI-1013 plan: a delegated run records only scope readings and design choices no spine row states

Planned on branch `maint/wi-1013` at `0d67302bd`, a maintenance branch cut
from trunk `refactor_again` at that commit. A maintenance-branch build: no
plan critique or pass record. Read in full: the row and its scope critique,
the specref (`docs/reviews/2026-11-20-decisions-overlap/README.md`), SR-225,
LLR-283, LLR-284, IF-256, TC-293, the "Delegated decisions record" layer of
`PROCESS_OPTIONS.md`, the shipped `decisions.template.toml`,
`kitlib.decisions.session_note` and its tests.

## The construction

The routing table in `PROCESS_OPTIONS.md` "Delegated decisions record" stays
the one home of which calls go in a record. Its two copies follow it: the
template's header says what the table now keeps and leaves out, and
`session_note` stops restating any route and sends the session to the table.
`session_note(mode, run)` keeps its signature, so IF-256 is unchanged, and
`kitlib/decisions.py` still reads no file. No state, domain value or
boundary is added.

### The one home: `PROCESS_OPTIONS.md`

The "Route on the action" paragraph and its table become, word for word:

> **Route on the action, never on confidence.** The initial table, which the
> operator may adjust, covers the calls a build or adjudication session makes
> under a recording dial through the kit's routes:
>
> | The action | Route |
> |---|---|
> | irreversible or external (a push, deleting reviewed text, a purchase), a ruled open item, the acceptance dial | the exits — never decided under delegation |
> | a reading of scope (how far the spec, a Done-when item or a requirement reaches), or a design choice no spine row states | decide, and record it |
> | a choice a spine row states, whether the run wrote, amended or found the row | decide; the row is its record |
> | the conduct of the run: who reviewed and in which round, commit grouping or order, a re-stamp whose own ledger carries its reason, working around a tool or environment failure | decide; the commit and the log fragment carry it |
> | scratch work, regenerating a generated file | decide silently |
>
> A review finding's outcome routes by what it changes: one that selects a
> design no spine row states is recorded. A call no row names is not
> recorded unless it is one of the two kinds the record keeps, or the
> ratchet below promotes it.

The `escalate-first` sentence, the one-way confidence ratchet and the
safety-boundary sentence after it stay byte for byte. The file is
byte-watched: the `byte-budget-guard` skill measures it before and after, and
its row in that skill (both copies) is re-stamped.

### The template's header: `decisions.template.toml`

The doctrine sentence names the table as the one home, and a paragraph
follows it:

```
# WHAT GOES HERE: a reading of scope, and a design choice no spine row states.
# NOT HERE: a choice a spine row states, whether the run wrote, amended or
# found the row (the row is its record); the conduct of the run, such as who
# reviewed and in which round, commit grouping or order, a re-stamp whose own
# ledger carries its reason, or working around a tool or environment failure
# (the commit and the log fragment carry it). A review finding's outcome
# counts by what it changes. Any other call stays out unless low confidence or
# a reviewer's dissent promotes it.
```

The example entry and every other header line are unchanged, so
`record_findings` still reads the template as sound.

### The instruction: `kitlib.decisions.session_note`

The sentence "the format and the routing rules are the process options'
\"Delegated decisions record\" layer. Write one [decision.D-<n>] table per
call that touched a registry, the spine or a kit file, or that you are
unsure of" becomes:

> Its format and its routing table, the one home for which calls go in it,
> are process-options.md "Delegated decisions record": read the table there.
> It leaves two kinds of call to record: a reading of scope, and a design
> choice no spine row states. Write one [decision.D-<n>] table per call of
> either kind, or that you are unsure of,

and the rest of the note (the required keys, the operator values left unset,
the hoist, the record is not an exit, the commit-before-close rule and the
`escalate-first` sentence) is unchanged. "Or that you are unsure of" is the
ratchet's low-confidence arm the note already carried, kept so the ratchet
reaches the session unchanged.

### The rows

- **LLR-283** (`Accepted`): its detail's `session_note` clause names the
  routing table's home, the two kinds left to record with a call the session
  is unsure of, and that the note restates none of the table's routes. Text
  only; the status stays `Accepted` and the row shows as drift for the
  operator's re-accept. Its `module` and `code_symbol` do not change.
- **TC-293** (`Accepted`): clauses (g) and (i) of its method gain the arms
  below, text only, for the same re-accept. Its evidence already names the
  whole of `tests/test_decision_record.py`.
- **SR-225** and **IF-256**: unchanged. No id is minted.

### The RESYNC entry

One `###` block at the end of `RESYNC_PACK.md` §4: what the routing now
leaves out (a choice a spine row states; the conduct of the run), what it
keeps, the note's new content, and that nothing migrates: existing records
stay valid as written, and `docs/decisions/run-000-example.toml` keeps the
old header until copied over. Kit-owned files to overwrite:
`scripts/kitlib/decisions.py`, `decisions.template.toml`,
`PROCESS_OPTIONS.md`.

## The arms the tests pin

In `tests/test_decision_record.py` (TC-293), written first and red until the
build commit:

1. **The note** (clause (i)): under `record`, `session_note` names
   `process-options.md "Delegated decisions record"` and both kinds left to
   record, and carries neither "touched a registry" nor "kit file"; each kind
   it names is found, whitespace-normalized, in that section of
   `PROCESS_OPTIONS.md` and in the template's header, so the note cannot name
   a kind its home does not hold.
2. **The home and the header** (clause (g)): the section and the header each
   say "the row is its record" and "the commit and the log fragment carry
   it"; the section keeps "The confidence ratchet is one-way" and no longer
   holds the route "touches a registry, the spine or a kit-owned file".

The existing note test (the path, every required key, the hoist, the
operator values, the `escalate-first` sentence) and the session-body tests
keep passing unchanged.

## How each Done-when item is met

1. A choice a spine row states is not recorded: the table's third row and
   the header's NOT HERE sentence; arm 2.
2. The conduct of the run is not recorded, and a review finding's outcome
   routes by what it changes: the table's fourth row and the sentence under
   it, and the header; arm 2.
3. What is left is stated plainly, with the default and the bound: the
   table's second row, the sentence under the table (default), the
   paragraph before it (bound), and the header's WHAT GOES HERE sentence.
4. The note names the home and the two kinds and drops the old routing:
   `session_note`; arm 1.
5. The ratchet is unchanged: its paragraph is untouched; arm 2 pins it, and
   the note keeps "or that you are unsure of".
6. Existing records stay as written: nothing under `docs/decisions/` is
   edited.
7. The RESYNC entry, as above.
8. LLR-283 amended, text only; SR-225 untouched.

## Tests run

`tests/test_decision_record.py`, `tests/test_decisions_to_review.py`,
`tests/test_decision_overrule.py`, `tests/test_ruling_sync.py`
(`trace.py --tests-for` on `kitlib/decisions.py`), the other direct
importers of `kitlib.decisions` (`tests/test_policy_one_home.py`,
`tests/test_done_when_blessing.py`), and the whole-tree
`tests/test_import_layers.py`, `tests/test_module_size_ratchet.py`,
`tests/test_dogfood_sync.py`, plus the byte-cap tests in
`tests/test_bootstrap.py` for the re-stamped skill.
