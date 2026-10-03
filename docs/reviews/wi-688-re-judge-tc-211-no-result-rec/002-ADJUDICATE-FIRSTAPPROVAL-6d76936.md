# ADJUDICATE (first approval): WI-688, LLR-297 and TC-312 at 6d769360

An independent spine adjudicator (Claude Opus) judged this batch. It directed none of WI-688's
steps 1-2 build and none of its fix round. The judgement used the kit brief composed for this
lane's merge, read in the lane as the owner directed on 2026-10-03 (S11). The adjudicator read
the chain SR-161, LLR-183, LLR-202, LLR-297, TC-178, TC-198 and TC-312 against
`project-trajectory/scripts/hats.py` (`read_record`, `derive_record`, `render_record`,
`write_record`, `record_findings`, `_cmd_record` and their helpers), `tests/test_hats_record.py`,
PROCESS.md §1's new sentences, the spine-authoring skill's (c3), and the step-2 record. Codex
Luna's MAJOR at 7733e2bf (authorship) is answered at 6d769360: the code refuses a first write
without `--by` and refuses a record that has lost either field. The adjudicator confirmed this
by reading the code and by running the tests.

Baseline: `tests/test_hats_record.py` gave 18 passed. The adjudicator then mutation-probed
`hats.py` on a scratch copy of the tree, outside the lane, against the unchanged test file. Of
14 single-point mutations, each against a clause LLR-297 or TC-312 states, **12 survived (18
passed)**. Only two were killed: CONFLICT-on-produced removed, and subject dropped on refresh.

| # | Mutation | Clause it breaks | Result |
|---|---|---|---|
| P1 | an LLR or TC row contributes no parent | LLR-297 "parents ... through SR-Refs, Verifies and a verified LLR's SR-Refs" | survived |
| P2 | a TC verifying an LLR contributes nothing | same | survived |
| P3 | one context merged from all parent needs | LLR-297 "never merged across sibling needs"; TC-312 "applicability per parent need" | survived |
| P4 | declared tags widen only the first parent context | TC-312 "declared tags widen every parent context" | survived |
| P5 | the parents STALE check is deleted | LLR-297 "STALE is a ... parent set that regeneration would change" | survived |
| P6 | every write, a refresh included, re-stamps recorded_on with today | TC-312 "a recorded_on date that a refresh keeps" | survived (the test refreshes on the same day) |
| P7 | plain `write_text` replaces `write_atomic` | LLR-297 "The file is written atomically" | survived |
| P8 | a missing entry for a hat that does not apply is not reported | LLR-297 STALE "a derived field ... that regeneration would change" | survived |
| P11 | a refresh drops the declared tags | LLR-297 "a rewrite keeps [no_finding] together with the scope fields" | survived |
| P12 | `applies_when` is left out of the STALE comparison | LLR-297 STALE on a derived field (`applies_when` is one of the three) | survived |
| P13 | MISSING judged on the stored `produced` | LLR-297 "MISSING and CONFLICT are judged on the regeneration" | survived |
| P9 | CONFLICT on produced removed | (pinned) | killed |
| P10 | subject dropped on refresh | (pinned) | killed |

P14 (an undeclared parent need no longer refused) also survived. LLR-297 does not state that
refusal, so it is not a finding. The behaviour is defensible as it stands.

- [RETURN] LLR-297 -> hats.py record writes and checks the per-decomposition perspective record: [decomposition] scope, derived parents, and per roster hat the derived applicable, applies_when and produced plus an authored no_finding; it reports MISSING, STALE and CONFLICT warn-first, refuses an unknown row or a non-record, and is vacuous without a roster -> upward, it answers exactly the half of SR-161 that LLR-183 states as NOT DISCHARGED; sideways, it does not overlap LLR-183 (the row cell) or LLR-202 (the staged guard); the code matches the text clause for clause except at two points -> not ready: (A) the text says the tool writes the file "beside the decomposition record it describes, named <stem>.perspectives.toml", but the code writes to whatever path it is given and enforces neither the name nor the location, so the row states as the tool's behaviour a convention that only the skill states; (B) the text lists "the record it describes (subject)" among what the table holds, with no "optional" (unlike the tags in the same sentence), but the code writes no subject when none is given and accepts a record without one; separately, five of its clauses are verified by nothing (P1/P2, P3, P5, P11, P13 above; P7, P8 and P12 also), and those are fixed under TC-312 below.
- [RETURN] TC-312 -> over a three-hat temporary tree, prove each derivation, refusal, authorship rule, finding class, vacuity and CLI exit code that LLR-297 states -> downward to tests/test_hats_record.py: two clauses that the Method itself asserts are proven by tests that cannot fail ("declared tags widen every parent context": P4 survives because the test has one parent; "a recorded_on date that a refresh keeps": P6 survives because the refresh happens on the same day), and LLR-297's parents-through-LLR/TC, never-merged, parent-set STALE, MISSING-on-regeneration, tags-kept, atomic-write, applies_when-STALE and new-hat clauses are verified by nothing -> not ready: a Method claim the evidence cannot fail is a false claim, and the parent clauses left unverified are load-bearing (the step-2 record scopes TC rows, and per-need applicability is the rule the planner brief shares).

## Required fixes (to be applied in this lane, then re-judged)

### Fix 1: LLR-297 `detail`, two sentences, byte-exact

Replace this sentence:

```
hats.py record writes one TOML file beside the decomposition record it describes, named <stem>.perspectives.toml.
```

with:

```
hats.py record writes one TOML file at the path its caller names; by the convention the spine-authoring skill states and no check enforces, that path is <stem>.perspectives.toml beside the decomposition record it describes.
```

Replace this fragment:

```
Its [decomposition] table holds the scoped SR/LLR/TC ids (rows), the record it describes (subject), optional extra declared tags, who recorded the authored judgements and on which date, and the derived parents:
```

with:

```
Its [decomposition] table holds the scoped SR/LLR/TC ids (rows), optionally the record it describes (subject), optional extra declared tags, who recorded the authored judgements and on which date (recorded_by and recorded_on, both required: a first write refuses without a recorder and stamps the date, and a file lacking either is not a record), and the derived parents:
```

Every other cell of LLR-297 stays byte-exact. (A different fix is equally acceptable: make the
code refuse a record with no `subject`, and give that refusal its own test. If the builder takes
it, the second replacement keeps "the record it describes (subject)" without "optionally". The
text and the code must agree in either case.)

### Fix 2: tests/test_hats_record.py, fixture changes and eight new tests

Fixture changes (none of the 18 existing tests changes outcome):

- `NEEDS`: SN-002 gains `tags = ["ops"]`.
- `TCS`: add `[test.TC-002]` with `verifies = ["LLR-001"]` and `method = "A method."`.
- A module-level `SIBLING_ROSTER = ROSTER + ...` adds three hats:
  - `BOTH`: `'tags contains "scripts" and tags contains "ops"'`
  - `EXTRA-OPS`: `'tags contains "extra" and tags contains "ops"'`
  - `EXTRA-SCRIPTS`: `'tags contains "extra" and tags contains "scripts"'`

  Each also carries `asks` and `listens_for`.

Tests. Each must fail under the named probe of `hats.py`.

1. `test_parents_are_reached_through_llr_and_tc_rows`, parametrized: rows `["LLR-001"]` give
   parents `["SN-002"]`, `["TC-001"]` give `["SN-001"]`, and `["TC-002"]` give `["SN-002"]`.
   Kills **P1**: `_parent_srs` returns `[]` for a non-SR row. Kills **P2**: the `else
   _as_tags(target.get("SR-Refs"))` branch is replaced by `[]`.
2. `test_applicability_is_never_merged_across_sibling_needs`: write rows SR-001 and SR-002
   under `SIBLING_ROSTER`. Assert `BOTH.applicable is False`. Kills **P3**: `_record_contexts`
   returns one context holding every parent's tags.
3. `test_declared_tags_widen_each_parent_context_and_a_refresh_keeps_them`: write rows SR-001
   and SR-002 with `tags=["extra"]` under `SIBLING_ROSTER`, then refresh with
   `write_record(root, REC)`. Assert:
   - `decomposition.tags == ["extra"]`;
   - `EXTRA-OPS.applicable is True`;
   - `EXTRA-SCRIPTS.applicable is True`.

   Kills **P4**: the tags widen only the first parent context. Kills **P11**: a refresh pops
   `tags`. The existing `test_declared_tags_widen_every_parent_context` may stay; it has one
   parent and does not by itself prove "every".
4. `test_a_refresh_keeps_an_earlier_recorded_on`: write, rewrite `recorded_on` in the file to
   `"2000-01-01"`, refresh without `by`, and assert `recorded_on == "2000-01-01"`. Kills
   **P6**: `recorded_on` is stamped outside the `if by:` guard.
5. `test_a_moved_parent_set_is_stale`: write, then author SCRIPTS' no_finding. Re-point
   SR-002's `sn_refs` to `["SN-001"]` and assert that a `("STALE", text)` finding exists whose
   text starts with `"parents are now SN-001;"`. Kills **P5**: the `parents` comparison in
   `record_findings` is removed.
6. `test_missing_is_judged_on_the_regeneration`: build the tree with SR-001's `hat_refs =
   ["ALWAYS-ON", "SCRIPTS"]`, write it, then restore SR-001 to `["ALWAYS-ON"]`. Assert the
   classes are `["MISSING", "STALE"]` and that a MISSING finding names SCRIPTS. Kills **P13**:
   the MISSING test reads `have.get("produced")` instead of `want["produced"]`.
7. `test_a_moved_predicate_and_a_new_hat_are_reported`: write, then author SCRIPTS'
   no_finding. Rewrite the roster so that SCRIPTS reads `'tags contains "scripts" or tags
   contains "ops"'` and a hat `LATE` (`'tags contains "nothing-carries-this"'`) is appended.
   Assert:
   - a STALE finding starts with `"SCRIPTS: applies_when"`;
   - a STALE finding starts with `"LATE has no entry"`;
   - the classes are exactly `["STALE"]`.

   Kills **P12**: `applies_when` is left out of the `moved` comparison. Kills **P8**: an
   absent entry for a hat that does not apply returns `[]`.
8. `test_an_interrupted_write_leaves_the_previous_record_whole`: write and keep the bytes.
   Monkeypatch `hats.write_atomic` to `functools.partial(kitlib.observation.write_atomic,
   replace=boom)`, where `boom` raises `OSError("interrupted")`. Assert that a second write
   raises that error and that the file bytes are unchanged. Kills **P7**: `write_record` calls
   `path.write_text` directly.

The adjudicator validated this set on a scratch copy. With the fixtures and the eight tests
added, the file gives 28 passed on 6d769360's `hats.py`, and every probe P1-P8 and P11-P13 is
killed (1 to 3 failed each).

### Fix 3: TC-312 `method`, byte-exact replacement of the whole cell

```
Over a temporary tree with a three-hat roster (one always, one reached by a parent need's tag, one reached by nothing), widened by conjunctive hats where a case needs one, and SR, LLR and TC rows, write a record and assert: applicability per parent need and production from the rows' own Hat-Refs, as derived; parents reached from an LLR through its SR-Refs, from a TC through an SR it verifies and from a TC through a verified LLR's SR-Refs; a hat whose predicate needs facts from two sibling needs does not apply; declared tags widen every parent context, shown by hats only the first or only the second parent need reaches with the tag, and a refresh keeps the tags; an unknown row, a first write without rows and a first write naming no recorder (--by) refuse; a written record carries recorded_by and a recorded_on date, a refresh keeps an earlier recorded_on, and a record missing either refuses; an applicable hat with nothing recorded is MISSING until a no_finding is written, and the no_finding and subject survive a refresh; the not-applicable and no-finding entries parse differently; a Hat-Refs edit makes the record STALE and the kept no_finding a CONFLICT, and an edit that removes a hat's only production makes it MISSING as well as STALE; a moved parent set, a moved applies_when and a newly declared hat that does not apply are each STALE; a no_finding on a not-applicable hat is a CONFLICT; an entry for a hat removed from the roster is kept on rewrite and reported STALE; a write interrupted at the final replace leaves the previous record byte-identical; a malformed record refuses; an absent roster writes no perspectives and checks vacuous; the CLI exits 0 with findings, 1 under --strict, 0 once they are answered, and 2 when --check is given write inputs.
```

Every other cell of TC-312 stays byte-exact. The `evidence` cell, `tests/test_hats_record.py`,
already covers the new tests.

OUTCOME: RETURN rows=2

## Re-judgement after fix round 2 (2c6cfe29)

Re-judged 2026-10-03 by the same independent adjudicator (Claude Opus), on the lane at
2c6cfe29. `hats.py` is byte-unchanged since 6d769360.

Applied text, checked against this verdict by parsing the registries:
- LLR-297 `detail`: both Fix 1 replacements are present and both old sentences are gone. Apart
  from those two substitutions, LLR-297 equals its 6d769360 form, and every other LLR row is
  unchanged.
- TC-312 `method`: equals the Fix 3 block byte for byte. Every other TC-312 cell, and every other
  TC row, is unchanged.
- The new sentence in Fix 1 is true of the code. `write_record` writes to the `rel` it is given.
  The convention it names is the one the spine-authoring skill's (c3) states ("next to its
  decomposition record"). `subject` is written only when given, and `read_record` refuses a
  record that lacks `recorded_by` or `recorded_on`.

Tests: the lane's `tests/test_hats_record.py` with `tests/test_hats.py` gave 116 passed. The
mutation probes were re-run independently against the lane's test file, on a scratch copy of the
tree. Every one of P1-P13 is killed (P1: 3 failed; each of the others: 1 failed). P14 survives,
as before; LLR-297 does not state it, so it is not a finding.

- [APPROVE] LLR-297 -> hats.py record writes, at the caller's path, a perspective record holding rows, an optional subject and tags, a required recorded_by/recorded_on, and parents derived through SR-Refs, Verifies and a verified LLR's SR-Refs; per roster hat it writes applicability derived per parent need, applies_when and own-Hat-Refs production, plus an authored no_finding; it reports MISSING, STALE and CONFLICT warn-first, refuses an unknown row or a non-record, and is vacuous without a roster -> it answers the half of SR-161 that LLR-183 leaves NOT DISCHARGED, without overlapping LLR-183 or LLR-202, and TC-312 now verifies every clause -> ready: the text and the code agree clause for clause, and the debt it leaves (the dual-plan round) is stated.
- [APPROVE] TC-312 -> over a temporary tree, prove each derivation, refusal, authorship rule, finding class, retention rule, the atomic write, vacuity and the CLI exit codes that LLR-297 states -> every Method clause maps to a test in tests/test_hats_record.py, and each of the 13 load-bearing mutations makes at least one test fail -> ready: no clause the Method claims is proven by a test that cannot fail.

OUTCOME: APPROVE rows=2
