# Parsed dependency repair — review dispositions

The [initial Opus review](2026-09-06-redesign-p2a-opus.md) requested changes.
These decisions follow inspection of the serial mint path and its real tests;
they do not declare the queued residual sweep complete.

1. **Late source refusal / destructive restore:** decline the proposed new
   `reset --hard` and `clean` fallback. The supported mint is serial. Planned
   IDs and actual IDs both advance from the maximum filename/watermark; earlier
   groups replace pre-mint predecessor IDs with fresh successor IDs, never with
   another group's old predecessor. Each source edit preserves the parsed
   dictionary except for root `needs`, and the canonical array it writes remains
   uniquely locatable. Newly minted specs use the existing canonical spec writer.
   Thus prevalidated old specs and newly written specs remain writable when the
   final scan includes them. An unsupported concurrent external mutation does
   not justify adding a destructive cleanup path. The regression must exercise
   multiple groups and a new successor with an absorbed dependency, not merely
   assert that preflight was called.
2. **Module baseline:** accepted the bounded repair at 1453 SLOC, from 1397;
   the ratchet carries the dated reason and execution-record reference. No
   function limit changed. The initial review packet carried the worker's earlier
   undecided note; the execution document now states the supervising decision.
3. **Real refusal evidence:** add a CR-only source case. The existing parser
   accepts its normalized value, while the bounded raw-source locator refuses
   it before mint effects. This documents a safe refusal, not CR-only support.
4. **Mutation-mode documentation:** describe `apply=False` as validation without
   writes and document the serial allocator assumption at preflight.

The additional regressions passed in the combined correction run (`113 passed,
56 deselected in 16.23s`). Existing destructive recovery elsewhere in intake is
outside this repair; it is not silently endorsed by retaining it.

## Closure follow-up

The [closure review](2026-09-06-redesign-p2a-closure-opus.md) withdrew the late
restore demand after reading the real multi-group/canonical-writer evidence.
Its further findings were dispositioned as follows:

- The ratchet reasons now lead each inline history chain, with the prior
  reason explicitly behind `Earlier:`. The checker reads the numeric dictionary,
  not a trailing-comment protocol; no check was evaded by the earlier adjacent
  reason, but the inline history is now unambiguous.
- The execution record now names the real CR-only test and additional
  multi-group test. That correction landed while this review was running, so
  its supplied packet still contained the obsolete injected-test name.
- The existing refusal names the LF/CRLF source requirement and unsupported
  CR-only style. No extra conditional or recovery path was added.
- The function documents its actual parser contract. `kitlib.registry`'s
  `parse_spec_frontmatter` returns the raw `tomllib.loads` dictionary and
  requires exact `+++` fences; it neither defaults values nor accepts trailing
  fence whitespace. A hypothetical future normalizer does not justify adding
  a second authoritative parse today. The full dictionary equality remains
  the semantic safety check.
- The whole `run_iteration` body confirms no rebinding of `current_wi` between
  route selection and its metadata/bookkeeping consumers. The removed alias
  had no independent meaning; committed progress still excludes the preceding
  probe and the invocation-accounting regressions pass.

The [final Opus follow-up](2026-09-06-redesign-p2a-final-opus.md) returned
**APPROVE**, with the late destructive-recovery demand withdrawn. It inspected
the supplied code and records; it did not execute the tests or approve artifacts.
