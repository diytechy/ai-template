+++
id = "WI-694"
title = "adjudicate: LLR-271, LLR-272, LLR-273, LLR-277, LLR-278, TC-269, TC-270, TC-271, TC-272, TC-278 - spine row(s) authored Drafted on merged trunk e520b6e..fe96ec6 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-271", "LLR-272", "LLR-273", "LLR-277", "LLR-278", "TC-269", "TC-270", "TC-271", "TC-272", "TC-278"]
+++

## Deliverable

Ruled in spine-acts batch C by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over four rounds (wave-5 rulings 37, 38, 44, 45). The verdict (`docs/reviews/wi-694-adjudicate-llr-271-llr-272/001-ADJUDICATE-1d84d77c.md`) ends:

    OUTCOME: RETURN rows=10

The act (ledger seq 5) was narrowed to the LLR and TC registries (ruling 38): 31 rows approved, 9 amendment rows re-attested. The SR registry was not copied, so SR-220, SR-223 and SR-224 stay Drafted, and the SR-tier amendments (WI-695's cells, SR-178) stay drifted and visible for a later act. Batch C's returns are one follow-up, drafted in WI-695's `## Dispositions` and minted at this merge.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-271 authored in `docs/requirements/low-level-requirements.toml`
- LLR-272 authored in `docs/requirements/low-level-requirements.toml`
- LLR-273 authored in `docs/requirements/low-level-requirements.toml`
- LLR-277 authored in `docs/requirements/low-level-requirements.toml`
- LLR-278 authored in `docs/requirements/low-level-requirements.toml`
- TC-269 authored in `docs/test/test-cases.toml`
- TC-270 authored in `docs/test/test-cases.toml`
- TC-271 authored in `docs/test/test-cases.toml`
- TC-272 authored in `docs/test/test-cases.toml`
- TC-278 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Follow-up: folded into WI-695's draft

The coordinator folded this draft into WI-695's `## Dispositions` draft (wave-5 ruling 45: one follow-up row for batch C's returns, one surface). The adjudicator's text stands below as the record.

The adjudication is recorded at
`docs/reviews/wi-694-adjudicate-llr-271-llr-272/001-ADJUDICATE-1d84d77c.md`,
governing line `OUTCOME: RETURN rows=10`: nine rows approved (LLR-271,
LLR-272, LLR-273, LLR-277, LLR-278, TC-269, TC-270, TC-271, TC-278) and one
returned with every cell byte-exact (TC-272). One draft, one cell; the
coordinator may fold it into an open item rather than mint it.


VERDICT THIS CONTINUES: the file above. Every one of TC-272's five evidence
pointers resolves and passed on the tree at 1d84d77c (three in
`tests/test_spine_carrier.py`, fast batch; two in
`tests/test_snapshot_readers.py`, slow batch), and LLR-277, the design row it
verifies, is approved: the return is about what the Tier cell CLAIMS, not
what the tests do.

IN SCOPE — one row, then a first-approval adjudication of it.

1. `TC-272.tier` reads `Smoke` while
   `tests/test_snapshot_readers.py::test_the_snapshot_history_reader_takes_the_needs_carrier_from_the_file`
   and
   `tests/test_snapshot_readers.py::test_a_markdown_needs_file_is_compared_like_a_toml_one`
   sit in a `tests/conftest.py` `SLOW_MODULES` member, so the Method's
   "the record's history reader ..." and "A scaffold whose needs file is
   markdown ..." arms do not run in the per-commit tier the cell claims. The
   assignment's rule and batch B's TC-204 return (WI-681, remedied by the
   TC-204/TC-274 split in WI-616) apply to the same fact. Remedy, either:
   (a) SPLIT — keep TC-272 at `Smoke` over the three in-memory pointers and
   the three in-memory sentences of its Method, and author a Full case
   (Verifies `SR-147;LLR-277;IF-112`, Level Integration, Evidence the two
   slow pointers) carrying the history-reader and markdown-scaffold
   sentences; or (b) RE-TIER — set `tier = "Full"` and keep the case whole.
   (a) keeps the carrier rule's cheap half in the commit bar, which is where
   a sniffing regression would be caught first, so it is the better of the
   two. Every other cell of TC-272 stands as adjudicated.

OUT OF SCOPE: LLR-277 (approved in this act; its chain reads incomplete until
this lands, which the derived stage carries), and the tier advisory class
LLR-260 reports for Full cases over fast modules elsewhere.
