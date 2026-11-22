+++
id = "WI-1050"
title = "WI-1049's verdict answered: LLR-257 re-amended without code names, TC-457, TC-468 and TC-475 made ready"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-217"]
needs = ["WI-1023"]
specref = "docs/reviews/wi-1049-adjudicate-second-sitting/001-ADJUDICATE-d5cb626.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, to answer
the second automated adjudication sitting's verdict (WI-1049,
`docs/reviews/wi-1049-adjudicate-second-sitting/001-ADJUDICATE-d5cb626.md`,
Gemini Neon). The sitting blessed 23 amendments and accepted 22 rows, but
ruled two amendments MEANING without the bless mark and returned three test
cases. Its act was refused (SR-207) while the two unblessed rows drifted in
the design registry it copies.

**The operator's ruling (2026-11-22, given in the coordinator's session):**
revert the two unblessed amendments to their accepted text, take WI-1049's
act, and re-land both amendments through this row, with the returned rows
answered, for a third sitting. So, in the commit that files this row,
LLR-244's and LLR-257's `detail` went back to the text the accepted copy
records. The amended text is at `468c91fd9`
(`git show 468c91fd9:docs/requirements/low-level-requirements.toml`): F-2's
(WI-1022) for LLR-244 and WI-1042's for LLR-257. Until they are re-landed,
both rows describe the code as it was before those items.

**LLR-244 moved to F-3 (WI-1023), 2026-11-22.** F-3 amends LLR-244 again on
top of F-2's text, so its review round 1 took the finding (its F5): F-3
rewrites LLR-244's `detail` with F-2's and its own behaviour and no code
names, and the coordinator takes that text at F-3's merge. This row keeps
LLR-257 and the three returned test cases. It lands after F-3 (`needs`),
so that the third sitting judges both rows together, and its repairs land
together in one branch, since one sitting judges them in one act.

**TC-475's choice, settled at the scope critique (2026-11-22).** Both
critics chose, and the coordinator adopted, the narrower of the verdict's
two ways: TC-475 keeps only the failing-test case (a validly declared test
that still fails leaves its case clean), and TC-428 and TC-429, both
`Accepted`, add LLR-395 to their `Verifies`, keeping their tests and their
homes. WI-1038's parent-first refusal no longer stands, since WI-1049's act
accepted LLR-395. The `Verifies` change is a routed traced change on
accepted rows, owed to the third sitting.

The findings, quoted from the verdict:

- **LLR-244** (MEANING, not blessed): "reachability moved from owner module
  to contract-body file with a files-mode component fallback, changing the
  obligation; NOT blessed because the amendment added a new implementation
  parameter symbol `homes` (`if_reached_srs(ifs, llrs, homes)` and
  `(homes, from the definition gate's scan)`), violating §0 ('an amendment
  adds no name the rule forbids') and §3."
- **LLR-257** (MEANING, not blessed): "acceptance provenance, re-pointing
  dating, cut handling and gap handling all changed; NOT blessed because the
  amendment added forbidden implementation carrier names
  (`record_acceptances` and `baseline_snapshot`) in violation of §0 and §3
  and introduced an unanchored external reference `(D3)` that a cold reader
  cannot resolve."
- **TC-457** (RETURN): "omits any case exercising LLR-396's explicit clause
  'A file that cannot be read or decoded is absent' ... add an
  unreadable/undecodable file case asserting it reads as absent."
- **TC-468** (RETURN): "its Method names the Python implementation function
  `copy_live` ... restate without `copy_live`."
- **TC-475** (RETURN): "copies verbatim all 10 evidence nodes and prose of
  live Accepted sibling TC-428 plus all 3 evidence nodes and prose of live
  Accepted sibling TC-429 while adding only one new test ... either retire
  TC-428 and TC-429 if TC-475 supersedes them, or narrow TC-475 to the
  failing-test case and point TC-428/TC-429 at LLR-395." WI-1038 was
  cancelled because the parent-first rule refused re-pointing accepted
  TC-428 and TC-429 at a `Drafted` LLR-395; WI-1049's act accepts LLR-395,
  so that refusal no longer stands.

## Done-when

- [ ] LLR-257's `detail` states the acceptance-record reading, the
      re-pointing date, the cut rule and the gap rule that `468c91fd9`
      states, without `record_acceptances`, `baseline_snapshot` or a bare
      `(D3)`; a cut rule it keeps says what it is in its own words. Text
      only; its status stays `Accepted`.
- [ ] TC-457 covers LLR-396's clause that a file which cannot be read or
      decoded is absent: a test drives an unreadable and an undecodable
      file through the declared-component reader and asserts each reads
      as absent without raising, and TC-457's Method, Expected and Evidence
      name the case.
- [ ] TC-468's Method names no function, module or symbol.
- [ ] The tests behind TC-428, TC-429 and TC-475 have one home each:
      TC-475's Method, Expected and Evidence name only the failing-test
      case, its other tests are no longer tagged to it, and TC-428 and
      TC-429 add LLR-395 to their `Verifies`, no other cell changing.
- [ ] No row text this branch writes names a code file, function or symbol.
      The Deliverable lists every act owed for adjudication.
