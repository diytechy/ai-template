# P2a execution — parsed dependency mutation

Date: 2026-09-06
Baseline: `83f2c7aa990a757729e7847816d40a8cdc2afcc7`

## Scope and authority

This slice repairs the remaining WI-582/OI-77 dependency mutation defect. OI-73
rules that minting a successor replaces inbound hard dependencies on the row it
supersedes. Completed WI-552 accepted that behavior. OI-77 then ruled that the
mutation must read the dependency value already parsed from TOML and remain a
surgical edit, with a multiline `needs` value as acceptance evidence. Queued
WI-582 Done-when 2 retains the same obligation.

Approved SN-027, SR-144, LLR-161 and TC-156 govern recoverable lane closure and
successor lineage. They do not themselves state inbound-edge replacement; this
slice does not broaden their claims or change an approval.

## Reproduction

At the baseline, `_open_specs` parsed a multiline TOML array successfully and
`_repointed_needs` derived the correct successor list. The write path then
applied `_SPEC_NEEDS_RE`, whose dot did not cross lines. A direct temporary-tree
probe returned `changed = []` and left the terminal predecessor in parsed
`needs`. A successful single-line probe also changed every CRLF in the file to
LF because the reader normalized newlines and the writer forced `newline="\n"`.

## Change

`intake._replace_needs_value` now locates candidate array spans only within the
validated frontmatter. For each candidate and closing bracket it substitutes
the already-derived new list and asks `tomllib` to parse the result. It accepts
the shortest span only when the result equals the original parsed dictionary
with exactly root `needs` changed. Quoted or escaped keys work through the same
path; assignments in strings, comments or nested tables cannot satisfy that
semantic equality. No second TOML value parser or whole-frontmatter writer was
added.

`_open_specs` retains raw newline bytes for the source edit while parsing a
newline-normalized copy. The writer changes only the accepted array span and
uses the original newline mode, preserving the complete prefix, suffix,
comments outside the value, body and CRLF style.

The mint prevalidates every existing dependent edit using the planned successor
IDs before `_write_draft`, open-item minting or any state mutation. An
unlocatable or non-unique declared target returns a typed refusal with no reset
or cleanup, so unrelated dirty work cannot be erased. The same renderer is used
for prevalidation and the authoritative write. The dead `_OI_ID_RE`, which had
no reader after `next_oi_id` moved to `trace.live_max_ids`, was removed.

## Evidence

- `tests/test_intake.py::test_the_mint_repoints_a_multiline_crlf_needs_value_surgically`
  drives the real intake mint. It carries a multiline CRLF dependency, a quoted
  fake assignment, a leading comment, an inline comment after the array and a
  body; only the dependency array changes and the resulting edge names the
  minted successor.
- `tests/test_intake.py::test_parsed_semantics_select_the_quoted_root_key_over_a_nested_key`
  proves a quoted root key is selected while a nested namesake is untouched.
- `tests/test_intake.py::test_a_cr_only_dependency_edit_refuses_before_any_mint_effect`
  exercises a real unlocatable source and proves the future WI is not written,
  the old bytes remain and unrelated untracked work survives. This replaces the
  initial injected-failure test; CR-only source is safely refused, not supported.
- `tests/test_intake.py::test_the_mint_handles_new_successors_across_multiple_repoint_groups`
  drives a real merge/mint with multiple lineage groups, the shared dependent's
  union, and post-mint rewrites of the newly created canonical successor specs.
- The existing one-to-one, consolidation, split, union, sibling and announcement
  cases remain green.

Initial validation after formatting (before the additional review regressions):

```text
python -m pytest -q tests/test_intake.py
62 passed in 15.48s

python -m pytest -q tests/test_complexity_ratchet.py
1 passed in 0.08s

ruff check project-trajectory/scripts/intake.py tests/test_intake.py
All checks passed!
```

After review corrections, the full intake and worker-policy modules plus the
capped-document checks passed together: `113 passed, 56 deselected in 16.23s`.
The [review dispositions](../reviews/2026-09-06-redesign-p2a-dispositions.md)
explain why the supported serial path does not need another destructive
rollback branch. Full-suite results belong to the supervising execution record.

The supervising review deliberately restamped the module-size baseline from
1397 to 1453 SLOC, a `+56` product SLOC delta, with the reason beside the value
in `tests/test_module_size_ratchet.py`. The accepted addition is the bounded
source-span replacement and no-effect prevalidation; no function-complexity
ceiling changed. This is a repair-specific baseline decision, not a P0 census
restamp or permission to relax future checks.

## Remaining WI-582 work

This slice does not claim WI-582 complete. Its stage-currency test exemption and
`check_trajectory.validate` docstring correction remain. IF-176 declares the
schedule-to-trace seam, but its direct real/absent-registry TC remains explicitly
listed in `docs/if-tc-coverage-allow`. No queue, registry, approval, snapshot or
archive state changed here.
