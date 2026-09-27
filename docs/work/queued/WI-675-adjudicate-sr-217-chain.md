+++
id = "WI-675"
title = "adjudicate: LLR-257, SR-217, TC-250 - approved cells amended by WI-650; judge whether scope moved"
workstream = "process"
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-217"]
needs = ["WI-650"]
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-257", "SR-217", "TC-250"]
priority = 2
+++

## Context

WI-650 carried out OI-87's ruling, option (a) plus the owner's addition, and
amended three approved rows in place to the code it built, status left
`Approved` and nothing re-anchored, so each row now differs from its copy in
`docs/archive/last_approved/` (LLR-257's copy is the text WI-669 re-anchored).

The amended attesting cells:

- SR-217 `requirement`: the report covers a requirement whose implementation
  landed while any of its test cases was not yet approved FOR IT, which takes
  in both a test case approved after the landing and one not approved at all.
- SR-217 `rationale`: argues association-aware approval (dated from its own
  approval alone, an approved test case re-pointed at code already written
  lends it an order it never had) and the warning (an unapproved test case's
  passing run shows only that the code does what unapproved text says).
- SR-217 `acceptance_criteria`: a test case is approved for a requirement at
  the earliest commit in which it reads approved AND names the requirement or
  one of its design rows; a landed requirement's report also names each of
  its test cases that does not read approved; each named test case carries a
  warning that its result may not reflect the intended behaviour.
- LLR-257 `detail`: `first_approval_commits` now walks the requirement
  registry only; the new `first_association_commits` walks the test-case and
  design registries together and dates each (test case, requirement) pair,
  a design row's `SR-Refs` read at each commit; a pair first shown at an
  older-carrier move is dated at or before it; `history_unreadable` holds the
  design registry to both older-carrier rules; `test_first_findings` names
  unapproved test cases on the report line with the warning.
- TC-250 `method` and `expected`: the re-pointing clauses (directly, and
  through a re-pointed design row), the unapproved-test-case clause (reported
  for a landed requirement, not for an unlanded one), the warning on every
  named test case, and `--strict` refusing it; the design registry's
  older-carrier and start-before-TOML cases reported unreadable, and a
  design-row association dated at or before that move, exactly after it.

Where the owner's addition sits: an SR-217 clause, not a derived row. SN-042's
acceptance already demands that each requirement's test cases be "defined and
approved before its implementation is accepted" and that "an implementation
accepted ahead of its test cases is reported", so a test case never approved
is the parent's own case at its widest rather than content a lens added; and
a second row would split one report, on one interface (IF-198), across two
rows deciding the same thing. Judge that placement with the rows.

Traced pointer cell moved on the same rows, which re-opens no attestation but
appears in the brief: LLR-257 `code_symbol` gains `first_association_commits`.
No interface row changed: IF-198's exit-code contract is unchanged (a finding
still exits 0, and 1 only under `--strict`).

The approval dial reads `human_approval_through` in `docs/process.toml`; what
a MEANING verdict owes next on each tier is derived from it, and the amendment
brief states it. SR-217 carries SN-042's reserved rule (spine map D6), so its
tier may be held for the owner.

## Done-when

- Each amended row is ruled MEANING or CLARITY, with the verdict recorded
  where the amendment brief puts it.
- A MEANING row whose new text is blessable is re-anchored in its own commit,
  naming exactly these rows; one that is not gets its corrective work drafted
  in `## Dispositions`.
