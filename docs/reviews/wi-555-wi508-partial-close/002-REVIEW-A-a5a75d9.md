# WI-555 — REVIEW-A

Reviewed `git diff contract_split...HEAD -- .` with the requested record and
generated-artifact exclusions. Worst failure classes: silent wrong close record,
fail-open admission of an unfinished lane, and loss of the preserved WI-508 work.

## What I verified

- The actual outcome path is contradictory to the new Deliverable: the current
  tree contains `docs/work/active/wi508-architectural-remap/WI-508-architectural-remap-program.md`, but no
  `docs/handbacks/WI-508-wi508-architectural-remap.md`, no WI-508 spec under
  `docs/work/partial/`, and no WI-568 queued spec.
- I drove the shipped admission path, not a primitive file probe:
  `integrate._claimed_specs(root, "wi508-architectural-remap")` returned
  `[("WI-508", "WI-508-architectural-remap-program.md")]`, while
  `integrate.branch_outcomes(...)` returned `({}, ["WI-508-architectural-remap-program.md"])` and
  `_merge_refusal(...)` returned `"... left claimed spec(s) without exactly ONE declared state directory ...; nothing was merged"`.
  Thus every WI Done-when item is UNCOVERED: partial/report, partial merge,
  disposition successor, and phantom-head clearance.
- `python` is unavailable in this environment; the equivalent `python3
  project-trajectory/scripts/check.py --jobs 0` Check summary ended
  `RESULT: PASS`. The independently run `python3 project-trajectory/scripts/trace.py
  --strict-integrity` final line was `Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0 verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=11 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=162 interface-findings=0 provenance-findings=1 paraphrase-advisories=3. Report -> docs/test/report.md`.

## Findings

- [MAJOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:15 -> the newly closed WI asserts that OI-71(c) converted and integrated WI-508, yet the shipped tree still has WI-508 claimed in `docs/work/active/`, lacks the required immutable handback report and terminal `partial/` spec, and the real `integrate._merge_refusal` refuses it as outcome-less; this falsely records all four Done-when conditions as complete and leaves the held lane unmergeable -> perform the OI-71(c) close through `handback.close_partial`, land its report/spec move and disposition WI-568 via the normal merge flow, then make this Deliverable describe that resulting committed state (or restore WI-555 to active until it exists) -> @owner

VERDICT: CHANGES-REQUESTED findings=1
