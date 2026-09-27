+++
id = "WI-674"
title = "adjudicate: LLR-259, TC-252 - spine rows authored Drafted by WI-577 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-259", "TC-252"]
+++

## Context

Filed by hand at WI-577's integration (the integrator merges by hand, so
intake's first-approval mint arm did not run). WI-577 carried out OI-82's
ruling on the owner's approval brief and, because no spine row stated that
rendering, authored these two rows Drafted (arbitration ruling 10 of
`docs/reviews/2026-09-26-wave3/ARBITRATION.md`), so that IF-224 is cited by a
test case rather than allowlisted:

- LLR-259 authored in `docs/requirements/low-level-requirements.toml`, under
  SR-139 (the builder named SR-049 as the alternative parent; judge it)
- TC-252 authored in `docs/test/test-cases.toml`, verifying SR-139, LLR-259
  and IF-224

Outcomes: read each row's WHOLE CHAIN — the parent SR, the sibling LLRs, the
test cases — and either APPROVE (move the rows' `Status` to `Approved` and
take the anchoring snapshot, `python project-trajectory/scripts/intake.py
snapshot --approves "<REGISTRY>=<this row>"`, in ONE reviewed commit on this
lane) or RETURN with findings, drafting the follow-up in a `## Dispositions`
section of THIS spec. The design and test tiers are released to the
adjudicator (`human_approval_through` holds only DevStg-Needs, or
DevStg-Boundary once the C1 sitting lands).

## Done-when

- A verdict is committed under `docs/reviews/` at the path the brief names,
  with one `APPROVE` or `RETURN` line for each of LLR-259 and TC-252 and
  exactly one `OUTCOME: APPROVE|RETURN rows=2` line, in a commit carrying this
  row's `WI:` trailer.
- Each approved row's `Status` moves from `Drafted` to `Approved` with no other
  registry cell changed, and `intake.py snapshot --approves` names only the
  registries holding an approved row, in one reviewed commit after the verdict
  commit.
- Each returned row keeps every cell byte-exact, and this spec's
  `## Dispositions` section drafts its follow-up.
