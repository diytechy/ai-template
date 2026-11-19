# WI-1001 plan: an accepted automated test case with no test declaring it is a finding

Planned on the maintenance branch `maint/wi-1001`, cut from trunk
`refactor_again` at `b696b6c36`. `planmode = "single"`; on a maintenance
branch the plan takes no critique round and no pass record.

Read in full: the row `docs/work/queued/WI-1001-approved-tc-has-a-test.md`,
its spec of record `docs/specs/WI-1001.md` (its `## Trust` and its critique
dispositions), `tc_tag_findings` and `_tag_evidence_findings` in
`trajectory_arch.py`, `read_test_tags` in `gen_arch_map.py`, the tag tests in
`tests/test_trajectory_arch.py`, SR-157, LLR-365, LLR-366, TC-035, TC-165,
TC-166, TC-407 to TC-412, IF-131 and IF-263.

## The spec is consistent

The critique is settled: five findings, all adopted, and a confirming round
with none. The row, the Trust ruling and the Done-when agree on one reading,
with two notes of spelling, not of scope:

- The spec writes `Approved` and `kitlib.spine.is_approved`. The status word
  is now `Accepted` and the predicate `is_accepted`; they mean the same rows.
- Its needs are met: WI-997, WI-999 and WI-1000 are archived complete, and
  OI-129 is ruled.

## Measured at `b696b6c36`

Through `spine_carrier` and `read_test_tags`: 380 live test cases, 374
Accepted and automated, 6 Accepted and not. No tag finding. The rule would
name one case: **TC-035** (evidence `.github/workflows/test.yml`). TC-165 and
TC-166 each have a declared test now (WI-1000 and WI-999), so the "0 findings,
with no exception" landing needs only TC-035's `automated` cell set to `No`.

## The construction

One new helper in `trajectory_arch.py`, called once from `tc_tag_findings`,
inside the branch that already runs only when the tests root exists:

```
_undeclared_case_findings(rows, tags, refused) -> ["<TC>: no test declares it", ...]
```

- **Eligible:** `is_accepted(row) or is_founded(row)`, and `automated`
  stripped and case-folded equals `yes`.
- **Clean:** `tags.get(tc)` is non-empty. `read_test_tags` puts only valid
  declarations in that map, so a misplaced or malformed tag is no declaration.
- **Silent:** an eligible case with any `Evidence` part (read by
  `evidence_items`) in a file refused as `unreadable`. That file's refusal is
  already a finding at the same severity.
- **Otherwise** one finding, sorted by test-case id, after the equality lines.

The rows, the tag map and the refused set are the ones `tc_tag_findings`
already holds, so there is no second reader, no new dial, state or allowance.
`check_trajectory.main` already prints every `tc_tag_findings` line as a WARN,
or collects it as an ERROR under `--strict`, so the new value takes the WI-997
finding's gating unchanged. The vacuous cases (no registry, no tests root,
`-000` rows not loaded) are the existing guards.

The equality helper's retirement comment stays true: the new helper does not
compare against the cells, and it stays when the equality check retires.

## Files

| File | Change |
|---|---|
| `project-trajectory/scripts/trajectory_arch.py` | the helper and its one call; `tc_tag_findings`' docstring; the IF-263 contract body names the new output |
| `project-trajectory/scripts/check_trajectory.py` | module docstring's test-file tag paragraph |
| `project-trajectory/scripts/trace.py` | the `Automated=Yes` schema message names a tagged test, or `Automated=No` for a procedure, not a script path or a procedure link |
| `project-trajectory/PROCESS.md` | §3's test-file tag bullet states the rule |
| `docs/registry-machinery-reference.md` | the test-file tag paragraph: a case with neither a tag nor a part is now a finding when accepted and automated |
| `project-trajectory/RESYNC_PACK.md` | a forced-migration entry: the sequence and the two remedies |
| `docs/requirements/interfaces.toml` | IF-263's `data` names the new finding (the row is Drafted) |
| `docs/test/test-cases.toml` | TC-035 `automated = "No"` (a traced cell); TC-428 and TC-429, Drafted |
| `tests/test_trajectory_arch.py` | the regressions below; one existing assertion that reads otherwise |
| `tests/test_module_size_ratchet.py` | `trajectory_arch.py` re-stamped if its line count moves (and `trace.py` if the message's line count moves) |
| `docs/interface-reference.md` | regenerated from the IF-263 contract body |

## The arms the tests pin

**TC-428, the ruling's table** (one test per row unless noted):

| Arm | Reading |
|---|---|
| no TC registry; no tests root | no finding, exit 0 |
| a registry that does not parse | the run stops in `spine_carrier`, no finding line |
| a `-000` row, Accepted and automated, untagged | no finding |
| a Drafted case, untagged | not eligible; with a part under the root the equality finding alone |
| `automated` `No`, another word, absent key, blank (legacy CSV cell) | not eligible |
| eligible (Accepted and Founded, `automated` in another case), tagged | clean |
| eligible, untagged, a part in an unreadable file | the `unreadable` finding alone |
| eligible, untagged: a note, no cell, a whole-file part, a part outside the root, a path the tree lacks | `<TC>: no test declares it` |
| a misplaced or a malformed tag the case's only one | that tag's finding and this one |
| a misplaced tag beside a valid one | that tag's finding only |
| an untagged part under the root | `evidence without a tag` and this one; one tag clears both |

**TC-429, the sequence:**

- the lane's order: a Drafted case holding the `(owed by the tests commit)`
  note reads nothing; tagged while Drafted it is clean; flipped to Accepted it
  stays clean;
- out of order: the same case Accepted with no tag warns in a plain run (exit
  0) and errors under `--strict` (exit 1);
- a bootstrapped scaffold: the case warns and exits 0 at `DevStg-Tests`,
  fails at `DevStg-Impl`, and is clean once tagged.

The one existing assertion that changes: the untagged half of
`test_a_note_only_cell_has_no_part_and_a_tag_on_it_is_a_finding` asserted an
exit of 0 for an Accepted automated case with a note and no tag. That case is
now this row's finding, so the half asserts what it is about, no equality
finding.

## Registry rows

- **TC-035:** `automated` `Yes` to `No`, traced, so it owes no sitting. It
  then reads as a manual case on the release checklist.
- **TC-428, TC-429:** new, Drafted, verifying SR-157 and IF-263. No LLR states
  the new rule and none is allotted; SR-157's acceptance takes a rule added at
  its declaration site into its scope.
- **IF-263:** `data` names the new value (Drafted row, so no amendment).

## Commits

1. this plan;
2. the tests, red for the right reason;
3. the code, the ratchet re-stamp and the regenerated interface reference;
4. the registry rows;
5. the docs and the RESYNC entry;
6. the close-out.
