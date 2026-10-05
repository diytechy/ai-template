# Dispute 1: ruling (independent, Claude Opus) on WI-818 at `b31498e2`

Adjudicator: an independent Claude Opus session. I wrote none of WI-818's code
(Claude Opus builder), none of its rows (GPT Terra), and none of its reviews
(Codex 6.1 Sol, rounds 1 to 4). My calls are final (OI-103 Q3).

Ruled here:

- Sol's round-4 MAJOR: `owner#cleanup` and `owner-cleanup` share one record;
- the builder's four high-risk decisions, D-001, D-004, D-005 and D-014;
- the rows, as far as they do not depend on the change this ruling owes.

Read: CLAUDE.md; the WI-818 spec in full; `docs/decisions/wi-818.toml`;
`sol-review-r1.md` to `-r4.md`; the `spine-authoring` skill; the two briefs
(`review-tmp/wave15/brief-wi818-first-r1.md` and `-amend-r1.md`); and the code
named below, at `HEAD` and at trunk `c0caea09`.

## Basis (probed, not trusted)

- **The collision, at HEAD and at trunk.** `record_path` at `HEAD` maps
  `owner#cleanup`, `owner-cleanup` and `owner/cleanup` all to
  `docs/decisions/owner-cleanup.toml`. Trunk's `record_path` (`c0caea09`)
  replaced only `/`, so there `owner#cleanup` wrote `owner#cleanup.toml`, a file
  of its own. `owner/cleanup` and `owner-cleanup` already shared a file on
  trunk. Both readings are from `review-tmp/adj818/probe1.py`, which loads both
  versions of the module.
- **Branch names with `#` are real git names.** `git check-ref-format --branch
  'owner#cleanup'` accepts the name, and `git branch 'owner#cleanup'` creates
  the branch on this Windows box.
- **The kit itself never makes such a name.**
  - `dispatch._branch_for` names a lane `wi-<spec stem>`, a single segment
    built from a spec filename.
  - `agent_loop` passes the session tag through `sanitize_train`, which only
    accepts `[A-Za-z0-9][A-Za-z0-9._-]*`. That tag is the `run` handed to
    `session_note`.
  - So `#` and `/` reach `record_path` only from a branch a person named, and
    only in `integrate._decision_record_refusal`, which passes the raw branch.
- **Sol's harm does not come from the collision.** `probe1.py` runs Sol's
  sequence three ways:
  1. A first commit overrules D-001 and amends its citing row.
  2. A second commit rewrites D-001's `decided` text and keeps
     `owner = "overruled"`.
  3. The sequence is run with the run names `owner#cleanup`/`owner-cleanup`,
     then `owner/cleanup`/`owner-cleanup`, and then with **one** run name for
     both commits, so no collision at all.

  All three pass, at the staged check and against the commit's parent. A
  verdict is not bound to the text it judged, so any commit can change a judged
  decision under a standing verdict. The collision is only one way to make such
  a commit. It is not the cause (separate finding F2).
- **What the collision does do.** The two harms below are real. Both already
  existed on trunk for `/` and for a reused branch name.
  - Two runs write one file, so the second run overwrites or merges into the
    first run's record.
  - The merge slot's "a close owes its record" rung reads
    `record_path(branch)` off the branch's tree
    (`integrate.py:2918`). It can therefore be satisfied by *another* run's
    record, once that record is on trunk.

  Round 4's D-013 adds `#` to that class.
- **The fix costs nothing elsewhere.** On a scratch `git archive` of `HEAD`
  (`review-tmp/adj818/head`), I changed `record_path` to:
  - keep trunk's `/` -> `-`;
  - raise `ValueError` for any other character in `_RUN_EXCLUDED`.

  Then I ran `test_decision_overrule.py`, `test_decisions_to_review.py`,
  `test_decision_record.py`, `test_decision_record_merge.py` and
  `test_agent_loop.py`. The result is `3 failed, 220 passed`. The three that
  fail are exactly the tests that pin round 4's mapping:
  - `test_the_run_name_alphabet_is_what_git_refuses_plus_two_delimiters`;
  - `test_a_run_name_carrying_the_citation_delimiter_has_one_citation`;
  - the `owner.toml#D-002` case of
    `test_the_citation_reads_every_run_name_the_record_path_writes`.

  Nothing else depends on mapping `#` to `-`.

## Ruling on dispute 1: Sol's MAJOR is UPHELD; D-013 as built is REJECTED. A change is owed.

- **D-013 created a new silent collision when it did not need to.** Round 3's
  problem was that `#` was both a run-name character and the citation
  delimiter. D-013 fixed that by mapping `#` to `-`. The mapping is lossy for a
  git-valid character. A branch carrying `#` now writes, without a word, the
  file of the branch carrying `-` in the same place.
- **Refusing `#` gives the same single parse without that cost.** It is better
  on every count the owner rules on:
  - **Fail closed.** A name the record cannot carry without loss is refused,
    never folded into someone else's file. The mapping fails open.
  - **No degenerate path.** Folding two names into one is a degenerate
    normalization. A refusal adds no fallback.
  - **Least migration.** Every git-valid branch name without `#` keeps exactly
    trunk's path (`/` -> `-`, nothing else changes). No record of any adopter
    moves.
    - D-013's mapping renames a `#`-named record, which its own RESYNC entry
      tells adopters to do.
    - Under the refusal, a trunk-era `#`-named record behaves as it does at
      `HEAD`: its entries cannot be cited, and an overrule of one is refused
      until the file is renamed. So no adopter is worse off than the lane
      already makes them.
  - **One parse is kept.** The citation class still excludes `#`, so the first
    `#` after `docs/decisions/` ends the path. No record name can carry `#`, so
    that one parse is also the right one.
  - **The cost is nothing in practice.** D-013's own reason for the mapping is
    that "no lane name in this kit produces" `#`. That is the case for refusing
    it: the refusal reaches only a branch a person named by hand, and only under
    a recording dial, at the merge slot.
- **The coordinator's other candidates are worse.**
  - **(i) An injective escape** (percent-encoding). It moves every slash-named
    record (this repo's `build-wi-557.toml`, and every adopter's). That is a
    forced migration this WI does not need. It also leaves reuse of one branch
    name colliding, so it does not fix the single point of failure either.
    That point is that a record's identity is a branch name, and branch names
    are reusable (F1).
  - **(iii) Accept as residue.** That keeps a fail-open this lane introduced,
    when a fail-closed shape costs a few lines.
  - **(iv) A `run` key checked against the writing branch.** It needs a new
    required key, so every record migrates. It needs the hook to read the
    current branch, which is wrong on a detached HEAD and at the merge slot's
    replay. And it still does not separate two lanes that reuse one name. It
    belongs with F1, if anywhere.
- **The `/` class stays a stated residue, and it is not this lane's to fix.**
  It predates WI-818: trunk's template already claimed "(a `/` becomes `-`), so
  two lanes never write one file", which was false. Fixing it moves records,
  which is the owner's call. F1 below names who files it.

### The change owed (to the builder; then to the row author)

**Code.**

1. `kitlib/decisions.py`, `record_path(run)`:
   - `/` becomes `-`, exactly as on trunk.
   - A run name carrying any other character of `_RUN_EXCLUDED` (`#` and the
     characters git refuses) raises `ValueError`. The message names the run and
     each such character, and says the record cannot be named by it, so the
     branch must be renamed.
   - No character is rewritten except `/`.
   - Keep `_RUN_EXCLUDED` and `_CITATION_RE` as they are. The citation class
     still excludes `#`.
   - Update the alphabet comment, the record_path docstring, the module
     docstring's "ONE FILE PER RUN" paragraph, and the IF-255 and IF-256
     contract text in the same docstring.
   - The "ONE FILE PER RUN" paragraph must stop claiming that two lanes never
     write one file. State the residue instead: `a/b` and `a-b`, and a reused
     branch name, share a record.
2. `integrate._decision_record_refusal`. After the `config_conflicts` check,
   wrap `record_path(branch)`:
   - On `ValueError`, return a refusal naming the branch and the exception's
     text, ending "; nothing was merged", whenever `kdecisions.owed(mode,
     outcomes)` holds. A record that cannot be named is an absent record.
   - Otherwise return None.
3. `agent_brief.decision_record_note` needs no change. Its `run` is the
   sanitized session tag, which cannot carry an excluded character.

**Tests, red first at `b31498e2`.**

- `tests/test_decision_overrule.py`:
  - Rewrite `test_the_run_name_alphabet_is_what_git_refuses_plus_two_delimiters`.
    It keeps the git pin, then asserts, for every ASCII character and the
    non-ASCII probes:
    - `/` maps to `-`;
    - each character of `GIT_REFUSED | {"#"}` makes `record_path("a" + ch +
      "b")` raise `ValueError`;
    - every other character is kept: `docs/decisions/a<ch>b.toml`.

    It is red at `HEAD`, because `#` maps.
  - Replace `test_a_run_name_carrying_the_citation_delimiter_has_one_citation`
    with `test_a_run_name_carrying_the_citation_delimiter_has_no_record`. It
    asserts:
    - `record_path("owner#cleanup")` and `record_path("owner.toml#D-002")` raise
      `ValueError` naming `#`;
    - `record_path("owner-cleanup") == "docs/decisions/owner-cleanup.toml"`.

    It is red at `HEAD`. Keep the one-parse assertion in this form: a spec
    citing `docs/decisions/owner.toml#D-002` discharges `owner.toml`'s D-002,
    and no other record.
  - Drop `"owner.toml#D-002"` from the parametrize list of
    `test_the_citation_reads_every_run_name_the_record_path_writes`.
- `tests/test_decision_record_merge.py` (TC-294's file): add
  `test_a_branch_name_no_record_can_carry_is_refused`.
  - Under `decision_recording = "record"`, a lane branch `owner#cleanup` closes
    complete.
  - Its tree carries `docs/decisions/owner-cleanup.toml`.
  - The lane is refused, and the refusal names the branch and `#`.

  It is red at `HEAD`, which finds the mapped file and passes.

**Shipped prose.**

- `decisions.template.toml` line 8: replace "(a `/` or `#` becomes `-`), so
  two lanes never write one file" with wording that is true:
  - a `/` becomes `-`;
  - a branch name carrying `#` has no record and is refused at the merge under
    a recording dial;
  - `a/b` and `a-b` share one file.
- The RESYNC_PACK entry: replace the sentence that renames `#` records. It
  should say that a branch carrying `#` is refused at the merge under a
  recording dial, and that a record of yours named with `#` cannot be cited
  until you rename it.
- `docs/decisions/wi-818.toml`: correct D-010 and D-013 to the refusal.
  D-013 stays high-risk for the owner.

**Cells the change makes untrue.** The row author amends these after the build.

- **LLR-283 `detail`.** Two sentences:
  - "record_path(run) is DECISIONS_DIR/<run>.toml under docs/decisions, each
    character outside the shared run-name alphabet becoming -; that alphabet
    excludes /, # and ..." It now reads that `/` becomes `-` and that a run name
    carrying `#` or a git-refused character raises ValueError.
  - "because # is never kept". It now reads "because no record name carries
    #".
- **LLR-284 `detail`.** This row is approved. It gains the clause that a branch
  name `record_path` refuses is treated as an absent record (refused when
  owed). Its next adjudication is a MEANING re-attestation.
- **TC-294 `method` and `evidence`.** Approved. They gain the case and the node
  above.
- **TC-319 `method` and `evidence`.** "with its refused ASCII characters plus /
  and # mapped while Unicode whitespace is kept; # has one citation parse" now
  reads "/ mapped, # and git's refused ASCII characters refused, Unicode
  whitespace kept; one citation parse". The renamed node replaces the old one.
- **IF-256 `data` and `notes`.** `record_path` raises `ValueError` for a run
  name it cannot carry. The row is Drafted.

No SR-225 cell depends on the change. The acceptance says "without its record
at its run's path", and that stays true for a name with no path.

## The four high-risk decisions

- **D-001 (the overrule check rides the ruling-sync step): ACCEPTED.**
  - `ruling_sync_lines` now calls `overrule_sync_lines` on every diff. It is
    not gated on the open-items registry changing. Mutant P13 gated it, and 12
    tests went red.
  - The same function serves the hook's `ruling-sync` step and the merge slot's
    per-commit walk.
  - It is the OI-102 Q3 shape the spec names, and it adds no step, rung or flag
    an adopter must enable.
  - Like the open-item arm, it judges a merge commit against its first parent.
    That is inherited and approved behaviour (LLR-298), not a new choice.
- **D-004 (the citing row changed in the same commit, queued or active only):
  ACCEPTED.**
  - The spec says "files or amends ... in the same commit", which names an act,
    not a standing citation.
  - The filter is exact: mutants P5 (archive admitted) and P9 (any changed path
    admitted) are killed. P10 (citations read from the parent tree) is killed
    by 9 tests.
  - A spec moved from queued to active in the same commit counts, because
    `--no-renames` lists the new path.
- **D-005 (an unreadable record in the commit's tree refuses; an unreadable
  parent overrules nothing): ACCEPTED.**
  - Failing closed on the resulting side is the owner's rule. P7 (parse error
    skipped) is killed.
  - Reading the parent as overruling nothing is the strict reading: the repair
    owes every overrule it shows. P8 (parent raises instead) is killed.
  - Refusing the parent too would strand the repair of a record broken before
    this rule.
  - One gap, in tests rather than in the decision: a parse refusal is dropped
    when the same commit's owed overrules are all cited (P11). It is owed below
    under TC-319.
- **D-014 (a non-UTF-8 path refuses only where a sync reads it; deleting or
  renaming such a record is refused): ACCEPTED, with the edge as disclosed.**
  - It fails closed at the one blob reader every arm shares. Mutants P2
    (replacing decoder) and P3 (guard removed) are killed. Sol r4 confirmed
    that an unread non-UTF-8 path is left alone.
  - A strict listing would refuse every commit near any non-UTF-8 path in a
    repository, for a rule that reads two folders.
  - The edge is a hold, not a pass. Only a record that predates this rule can
    reach it, and the kit's own run names are ASCII slugs.
  - A second, stdin-fed blob reader to clear it would be a second reader of one
    fact. If the edge is ever met, the fix is to make `git_show` itself read
    through `git cat-file --batch`: one reader, lossless. That is not owed now.

## The rows, as far as they are independent of the change

These are preliminary. No verdict file is written and no act is taken: the
change above moves `HEAD`, and the act follows a fresh ruling at the new tip.
The mutants ran against the five decision test files plus
`test_gen_open_items.py` and `test_traj_status.py`, on a scratch archive of
`HEAD` (`review-tmp/adj818/mutate.py`, `mutate2.py`). The base is `177 passed`
or `217 passed`, depending on the set.

The surviving mutants:

| Mutant | Clause it breaks | Row |
|---|---|---|
| P6 | `_open_spec` admits a `-000` example spec as a citer | LLR-303 |
| P11, P11b, P11c | parse refusals dropped, reordered, or appended after the missing-citer lines | LLR-303 |
| N1 | a numeric retired value is not in the vocabulary | LLR-304 |
| N3 | multiline string delimiters ignored | LLR-304 |
| N4 | comments not skipped when cutting statements | LLR-304 |
| N8 | a quoted `"reviewed"` key is not matched | LLR-304 |
| N9 | `_migrate_one` reads in text mode, so CRLF is lost | LLR-304 |
| N10 | an unparseable record exits 0 | LLR-304 |
| N11 | retained values are not named | LLR-304 |
| L6 | the overruled list is not ordered | LLR-283 |
| L7 | `citing_rows` skips the archive | LLR-283 |
| L11 | the session note no longer says "set no owner key" | LLR-283, TC-293 |

P12 (the `(?!\d)` lookahead) also survives, but it is an equivalent mutant: a
greedy `\d+` already consumes every digit. It is not owed.

- **[RETURN] LLR-303** -> the overrule sync's readers, filter and refusals ->
  every clause is true of the code, and P1 to P5, P7 to P10, P13 and P14 are
  killed -> not ready, for three reasons:
  - "returns parse refusals before one missing-citer refusal line" is held by
    no test (P11, P11b, P11c);
  - "accepts a non-example work specification" is held by no test (P6);
  - "raises UnreadableBlob when a listed blob cannot be read" is held only by
    `tests/test_ruling_sync.py::test_a_parent_the_repository_cannot_read_is_refused_by_name`,
    which TC-319 does not cite.

  Owed to the builder, in `tests/test_decision_overrule.py`:
  - `test_an_unparseable_record_beside_a_cited_overrule_is_still_refused`. One
    staged diff in which `wi-050.toml` newly overrules D-002, with its citing
    spec, and `wi-090.toml` does not parse. It yields exactly `[the wi-090 parse
    line]`. Without the citing spec it yields `[the wi-090 parse line, the
    wi-050 missing-citer line]`, in that order.
  - `test_an_example_spec_does_not_discharge_an_overrule`. A queued
    `WI-000-example.md` citing the entry leaves the overrule refused.

  Owed to the row author: TC-319 `evidence` adds those two nodes and the
  `test_ruling_sync.py` node above.
- **[RETURN] TC-319** -> the overrule coupling at staged and merge admission ->
  the method is true of the code except for the alphabet clause, which the
  change rewrites -> not ready. Its `method` and `evidence` change with the
  dispute change and with LLR-303's owed tests. I re-judge it at the new tip.
- **[RETURN] LLR-304** -> the migrator -> every clause is true of the code
  (N2, N5 to N7 and N12 to N14 are killed). Seven clauses are held by no test.
  Owed to the builder, in `tests/test_decision_overrule.py`:
  - `test_the_migrator_reads_a_numeric_retired_value`: `reviewed = 1` becomes
    `owner = "confirmed"` and `reviewed = 0` is dropped (N1).
  - `test_the_migrator_reads_a_multiline_note_holding_a_lone_quote`: `review =
    """a "quoted\nreviewed = true\n"""` beside a top-level `reviewed = true`
    keeps the note byte-exact and rewrites only the top-level line (N3).
  - `test_the_migrator_reads_past_a_comment_holding_a_quote_or_bracket`: a
    comment line `# the owner's "call [see` before `reviewed = true` still
    rewrites it (N4).
  - `test_the_migrator_rewrites_a_quoted_retired_key`: `"reviewed" = true` and
    `'reviewed' = "yes"` each become `owner = "confirmed"` (N8).
  - `test_the_migrator_cli_keeps_a_records_line_endings`. A CRLF record is
    rewritten with every line still ending `\r\n`, and a CRLF record with
    nothing to migrate is left byte-identical (N9).
  - `test_the_migrator_cli_names_what_it_leaves_and_fails_on_an_unparseable_record`.
    Stdout names the file and entry of a `reviewed = "maybe"`. A record that
    does not parse exits 1, is named "left untouched", and keeps its bytes
    (N10, N11).
- **[RETURN] TC-320** -> the migration's cases -> its method is true of the
  code -> not ready until the six nodes above are in its `evidence`. Its
  `method` gains: "a numeric retired value; a quoted retired key; a note
  holding a lone quote and a comment holding a quote or bracket; line endings
  kept; retained values named and an unparseable record failing the run".
- **TC-313 (amendment): MEANING. I would bless it.**
  - `method` before: drive the ruling transitions, through to the merge-ladder
    case.
  - `method` after: the same, plus a citing row git would quote is judged at
    both admission points, and a non-UTF-8 citing row is refused by name.
  - Not the same: a case was added.
  - The new clause is true. It is held by its two cited nodes:
    - P1b (`git_paths` reading git's plain, quoted listing) kills
      `test_a_citing_row_whose_path_git_would_quote_is_still_judged`, along
      with the four quote and non-UTF-8 tests of TC-319;
    - P2 (a replacing decoder) kills
      `test_a_citing_row_whose_path_is_not_utf8_is_refused_never_skipped`.
  - It does not depend on the change. I re-attest it at the act.
- **SR-225 (amendment): MEANING. Its `requirement` is not one I would bless as
  written.**
  - Before, everything was scoped to the dial. After, the acceptance says
    "Whatever the dial" for reporting, the verdict and the overrule refusal.
  - The new `requirement` cell still lists "refusing an overrule unless ..."
    inside the colon list of "where the declared decision-recording dial asks
    for a record, holding each delegated run to that record". A builder working
    from that cell alone may gate the refusal on the dial. The leading
    "preserve ... work coupling" is not an observable obligation that rules
    this out.
  - Every acceptance clause is true of the code except one: "a session ... is
    told ... that it leaves owner unset" is held by no test (L11).

  Replacement `requirement` cell, byte-exact, for the row author:

```text
The delivered loop content shall keep the owner's verdict on each delegated decision coupled to the work that acts on it and each delegated run to its record: whatever the declared decision-recording dial, reporting without refusing a record entry that omits a required disclosure field or leaves one blank, listing each entry the owner has not yet seen and each overruled entry with the open work that carries it, and refusing an overrule unless its transition change files or amends open work that cites the entry; and, where that dial asks for a record, refusing to integrate a closing lane whose record is absent, naming where it belongs.
```

  The other SR-225 cells I would bless once L11's assertion lands.
- **LLR-283 (amendment): MEANING. Not yet blessable.**
  - Its `detail` changes with the dispute change.
  - Independently, two clauses are held by no test: "Each list ... orders
    hoisted entries first and then by id" for the overruled list (L6), and
    "adds the citing work item and state folder ... through citing_rows" for an
    archived citer (L7). SR-225 asks for "every citing work item".
  - Owed to the builder, in `tests/test_decisions_to_review.py` (cited whole
    by TC-293, so no `evidence` change):
    - `test_overruled_entries_list_hoisted_first_then_by_id`;
    - `test_an_archived_citing_row_is_shown_with_its_state_folder`, in which a
      citer under `docs/archive/work/complete/` renders as `WI-NNN (complete)`.
- **TC-293 (amendment): MEANING. Its text is true and I would bless it once
  (i)'s "owner unset" is held.**
  - Owed to the builder: in `tests/test_decision_record.py`,
    `test_the_session_note_names_the_path_only_under_a_recording_dial` asserts
    that the note under `record` says to set no owner key (L11).
  - The file is cited whole, so no cell changes.

## Separate findings (not owed by WI-818; for the coordinator to file)

- **F1: a record's identity is a reusable, lossy name.** These share one file:
  - `a/b` and `a-b` (on trunk, before this lane);
  - two lanes that reuse one branch name.

  The second run overwrites the first, and the merge slot's "owes its record"
  rung is met by the other run's record once that record is on trunk. Any fix
  moves record paths, which is a forced migration and the owner's call.
  Owner: the coordinator files it as a pending open item for the owner, with a
  queued WI against SR-225 drafted beside it.
- **F2: a verdict is not bound to the decision it judged.** A commit may
  rewrite an entry's `decided`, `alternative`, `reversal_cost` or
  `why_not_escalated` while its `owner` key stays. A confirmed or overruled
  verdict then stands on text the owner never read. Reproduced in one run
  (`probe1.py`, "samerun"). WI-790's `reviewed` had the same property.

  A commit-against-parent fix fits the owner's rules. The ruling sync would
  refuse a commit that changes a disclosure field of an entry whose parent
  carries `owner`, unless the same commit removes that `owner` key. No history
  walk and no marker are needed.

  Owner: the coordinator files it as a queued WI against SR-225.

## Aftermath

No act. The coordinator runs the build above. The row author then lands the
cells named above plus SR-225's replacement. A fresh adjudication at the new
tip writes 001 and 002 and takes one act. Committed here: this ruling only.

RULING: dispute-1=UPHELD (D-013 REJECTED; change owed: refuse `#` in record_path) D-001=ACCEPT D-004=ACCEPT D-005=ACCEPT D-014=ACCEPT rows=RETURN(LLR-303,LLR-304,TC-319,TC-320,SR-225,LLR-283,TC-293) bless-pending=TC-313
