# 001: ADJUDICATE (independent, Claude Opus), first approval of the WI-818 rows at `be8633c0`

Adjudicator: an independent Claude Opus session, the author of
`dispute-1-ruling.md` (`7caf54ea`). I wrote none of WI-818's code (Claude Opus
builder) and none of its rows (GPT Terra). Brief:
`review-tmp/wave15/brief-wi818-first-r2.md`, read in full. The rows are
LLR-303, LLR-304, TC-319 and TC-320 under SR-225.

## Basis (probed, not trusted)

- **The tip.** The lane `HEAD` is `be8633c0`, on trunk `c0caea09`, which has
  not moved. The range `7caf54ea..HEAD` is three commits:
  - `a1c88eef`, the build;
  - `ffe37bca`, the spine;
  - `be8633c0`, Sol round 5 (SOUND).

  I read the whole diff of code and tests in that range.
- **The dispute change is built as ruled.**
  - `record_path` maps `/` to `-` and raises `ValueError` for `#` or a
    git-refused character.
  - `integrate._decision_record_refusal` reads that error as an absent record.
    The refusal text moved to `kitlib.decisions.missing_record_refusal` (D-015).
    It names the run and the `ValueError`, and integrate.py's baseline was
    re-stamped down, 1554 to 1551.
  - Inside the merge ladder, `owed` cannot be false under a recording dial.
    `_merge_refusal` only reaches the rung with every claimed spec resolved to
    an outcome. So the rung's `if owed` arm (mutant R7 below) is an equivalent
    mutant in context, not a gap.
- **Base.** I made a fresh `git archive` of `be8633c0` at
  `review-tmp/adj818/head`. Running `test_decision_overrule.py`,
  `test_decisions_to_review.py`, `test_decision_record.py`,
  `test_ruling_sync.py`, `test_decision_record_merge.py`,
  `test_gen_open_items.py` and `test_traj_status.py` gives **228 passed**.
- **Mutants, rerun on that archive.** The harnesses are `mutate.py`,
  `mutate2.py` and `mutate3.py` in `review-tmp/adj818/`. Every mutant that
  survived at `b31498e2` is now killed by a node TC-319 or TC-320 cites:
  - **P6** (`_open_spec` admits `-000`): killed by
    `test_an_example_spec_does_not_discharge_an_overrule`.
  - **P11, P11b, P11c** (a parse refusal dropped, reordered or appended):
    killed by
    `test_an_unparseable_record_beside_a_cited_overrule_is_still_refused`.
  - **P4** (`git_show` reads a listed but unreadable blob as absent): killed by
    `test_ruling_sync.py::test_a_parent_the_repository_cannot_read_is_refused_by_name`,
    which TC-319 now cites.
  - **N1, N3, N4, N8, N9, N10, N11**: each killed by its new
    `test_the_migrator_*` node.

  The rest are killed too: P1 to P5, P7 to P10, P13, P14, N2, N5 to N7, N12 to
  N14, and R1 to R6 and R8 (the dispute change: `#` folded back, git-refused
  folded, `/` refused, the rung passing an unnameable name, the refusal losing
  its reason or its path, U+00A0 folded).

  Three still survive, and none breaks a claim:
  - P12 (the redundant `(?!\d)` lookahead): equivalent;
  - P15 (records in subdirectories): no row claims them;
  - R7 (the `if owed` arm): equivalent in the ladder, as above.

## Verdicts

- [APPROVE] LLR-303 -> the overrule sync's lossless path reader, its blob
  reader that refuses an unreadable or non-UTF-8 path, the open-specification
  filter, and the owed and refused lines, in their stated order, at the staged
  and per-commit admission points -> SR-225's acceptance asks for the coupling
  and the fail-closed parse at both admission points, and TC-319 cites a node
  that kills each mutant of each clause -> ready. Every clause is true of the
  code at `be8633c0` and held, and the cells have not moved since the ruling.
- [APPROVE] LLR-304 -> the retired-key migrator. It reads the old vocabulary
  only to migrate it, cuts the text into whole top-level statements across
  every string form and comment, rewrites or drops only the verdict
  assignment, refuses any re-parse that differs in more than the verdict keys
  (NaN included), keeps line endings, and the CLI names what it leaves and
  fails on an unparseable record -> SR-225's acceptance asks for a migration
  that keeps string contents, keeps an unknown value for a person, and refuses
  a wider rewrite. Each of the seven clauses that no test held at `b31498e2`
  is now held by a TC-320 node -> ready.
- [RETURN] TC-319 -> drive the overrule coupling through every case its
  evidence names -> each cited node exists and passes, and the cases are true
  of the code -> not ready, because the clause added this round misstates two
  cases:
  - "a record that does not parse is refused even when cited" says the
    unparseable record is the cited one. The node's case is an overrule in
    *another* record that is cited.
  - "an unreadable parent is refused by name" names the commit half of the
    cited node and leaves out the half LLR-303's clause rests on: a blob the
    tree lists but the store cannot read.

  Replacement `method` cell, byte-exact, for the row author:

```text
Drive staged and committed decision-record transitions over git repositories: a new overrule without a changed queued or active citer is refused by the staged ruling-sync path; an unchanged citer, an archived citer, a citation for another entry, and a token with following digits do not discharge it; a newly filed queued row, an amended queued row and an amended active row discharge it; an entry already overruled before the diff owes nothing; and merge admission refuses a no-verify overrule commit even when a later commit adds the citer, while accepting a lane whose overrule commit carries the citer; a touched resulting record that does not parse is refused at staged and merge admission naming the record and a later syntax repair that drops its verdict does not launder the lane; a repair of an unparseable parent record owes every overrule it shows; and an overrule beside the retired key still owes its citer; a decision record whose path git would quote is judged for both normal and unparseable transitions; a changed citing specification whose path git would quote discharges; generated citations for every retained run-name character discharge at staged and merge admission; and surrounding prose does not make whitespace or a slash part of a valid citation; the run-name alphabet is pinned against git, / mapped, # and git's refused ASCII characters refused, Unicode whitespace kept; one citation parse; a non-UTF-8 decision-record path is refused by name wherever read, while an unread one is not; a touched record that does not parse is still refused when the same commit's overrule of another record is cited, and its refusal precedes any missing-citer line; a queued -000 example specification citing the entry does not discharge it; and a blob its tree lists but the store cannot read is refused by name, never read as absent.
```

  It is the live cell with only its last three clauses rewritten. `evidence`
  is unchanged.
- [RETURN] TC-320 -> drive the migrator through every case its evidence
  names -> each cited node exists, passes and kills its mutant -> not ready.
  The clauses added this round carry a typo, and most give no expected result:
  - "pass --check.;" is stray punctuation;
  - "a numeric retired value; a quoted retired key; a note holding a lone
    quote ..." names inputs without saying what each must produce, so the cell
    does not state the obligation the nodes hold.

  The ruling's own sketch of this clause was a list of fragments, so the defect
  started there; I correct it here. Replacement `method` cell, byte-exact, for
  the row author:

```text
Run the decisions-record migration over in-memory record text and a temporary decisions directory: recognized reviewed values become confirmed while their review notes and all unrelated bytes remain, recognized not-reviewed values disappear, a reviewed line beside owner disappears, an unrecognized retired value remains and is named, repeated migration changes nothing, --check reports an owed rewrite without writing it, and a write followed by --check is clean; a retired line beside an existing owner disappears; a retired line inside a multiline review note is preserved while the top-level assignment is rewritten; basic and literal multiline verdict strings are replaced whole and re-parse; and an inline-table retired key that cannot be rewritten in place is refused by the re-parse check; rewritten assignments preserve trailing comments, dropped assignments retain their comment on its own line, and a # inside a string is not a comment; and records carrying each TOML NaN form remain migration-clean and pass --check; a numeric retired value 1 becomes confirmed and 0 is dropped; a quoted retired key is rewritten as a bare one is; a lone quote inside a multiline note does not end the note, so the retired line inside it is kept, and a comment holding a quote or a bracket does not hide the retired assignment after it; the migration keeps each record's line endings and leaves a record with nothing to migrate byte-identical; and it names each retained unrecognized value and, when a record does not parse, leaves that record untouched and fails the run.
```

  It is the live cell with only the text after "and records carrying each TOML
  NaN form remain migration-clean and" rewritten. `evidence` is unchanged.

OUTCOME: RETURN rows=4

## Aftermath

- **No act now.** The brief would have me flip LLR-303 and LLR-304 in a mixed
  batch. The coordinator's direction for this sitting is to take no act when
  anything is returned, and the act is the lane's last commit. So I flip no
  `Status` and run no snapshot.
- **No `## Dispositions`.** The returns are cell text for the in-lane row
  author (the owner's S11 direction).
- **When the act is taken.** LLR-303 and LLR-304 need no further change.
  - Once both replacement cells land byte-exact and nothing else in these
    four rows moves, the act approves all four rows:
    `--approves "docs/requirements/low-level-requirements.toml=WI-818;docs/test/test-cases.toml=WI-818"`.
  - It goes together with 002's re-attestations in one snapshot.
  - Before that act, the adjudicator should confirm the landed cells are
    byte-exact. A re-run of the mutants is not needed if no code moves.
