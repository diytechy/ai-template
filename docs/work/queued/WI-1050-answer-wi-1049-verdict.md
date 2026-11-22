+++
id = "WI-1050"
title = "WI-1049's verdict answered: LLR-244 and LLR-257 re-amended without code names, TC-457, TC-468 and TC-475 made ready"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-212", "SR-217"]
needs = []
specref = "docs/reviews/wi-1049-adjudicate-second-sitting/001-ADJUDICATE-d5cb626.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
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
records. The amended text this row re-lands is at `468c91fd9`
(`git show 468c91fd9:docs/requirements/low-level-requirements.toml`): F-2's
(WI-1022) for LLR-244 and WI-1042's for LLR-257. Until this row merges, both
rows describe the code as it was before those items.

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

- [ ] LLR-244's `detail` states the contract-body reachability and the
      files-mode fallback that `468c91fd9` states, naming no function,
      parameter or file (`homes` and the call signature gone). Text only;
      its status stays `Accepted`.
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
- [ ] The tests behind TC-428, TC-429 and TC-475 have one home each: the
      scope critique picks between narrowing TC-475 to the failing-test
      case and pointing TC-428 and TC-429 at LLR-395, or retiring TC-428
      and TC-429 for TC-475, and the row does that.
- [ ] No row text this branch writes names a code file, function or symbol.
      The Deliverable lists every act owed for adjudication.
