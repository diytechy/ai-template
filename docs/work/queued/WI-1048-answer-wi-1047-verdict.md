+++
id = "WI-1048"
title = "WI-1047's verdict answered: LLR-373 and TC-081 corrected, the six returned rows made ready for a second sitting"
workstream = "process"
sr_refs = ["SR-157", "SR-159", "SR-168", "SR-169"]
needs = []
specref = "docs/reviews/wi-1047-adjudicate-f2-sitting/001-ADJUDICATE-3cd2513.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-22 from WI-1047's adjudication sitting (Gemini
Neon, verdict at `42df09628`). The sitting ruled 20 amendments re-acceptable
and 13 rows ACCEPT, but its act is refused: two amended `Accepted` LLRs it
ruled MEANING and would not bless still drift in the design registry the act
copies, and the snapshot will not absorb drifted text no act names
(SR-207). Until they are corrected and judged, no act can copy that registry,
and F-3's batch act cannot run. This row answers the verdict's findings, so
that a second sitting over everything still owed can accept it in one act.

**The two MEANING rows (blocking).**

- **LLR-373** (Accepted): its amended Detail says `gen_components` places
  seams by the files' `Component:` declarations. That contradicts its sibling
  LLR-199 and TC-435, which state that, since WI-1022, a seam is placed from
  its endpoint cells alone (component ids), even when the join answers an
  empty map. The fix is LLR-373's text: the join lists each component's
  modules; seams are placed from endpoints. Check the code agrees before
  changing a word.
- **LLR-080** (Accepted): its amended Detail renders interface seams in the
  dashboard view only, and the architecture map's dependency diagram draws
  imports only. Its one verifying test case, TC-081 (Accepted), was not
  updated and still asserts seams render in both views. The fix is TC-081's
  method and expected cells, matched to LLR-080 and to the tests it names as
  evidence.

**The six returned rows (Drafted; not blocking F-3).**

- **LLR-393, LLR-394, TC-455, TC-456** (WI-1014): each names implementation
  carriers (module, constant and function names) in its requirement text,
  against the brief's naming rules (§0, §3; the rule F-8, WI-1028, will
  enforce). Rewrite each as a contract that survives a refactor; traced
  cells (`module`, `code_symbol`, evidence) keep the names.
- **TC-463** (WI-1022): the only test case verifying LLR-398, it leaves five
  of LLR-398's clauses unverified: warn-plain versus fail-`--strict`
  gating, the `interfaces_check` opt-out, vacuity with no scan surface, the
  refusal of a body in a file with no `Contracts:` marker, and a listed
  Python file read through its docstring. Cover each, by extending TC-463 or
  by new `Drafted` test cases, each citing a test that exists (WI-1022's
  round fixes added several).
- **LLR-395** (WI-1019): returned because no test case verifies it. TC-428
  and TC-429 (Accepted) carry its evidence but verify SR-157 only, and the
  parent-first rule refuses re-pointing an accepted test case at a `Drafted`
  LLR, which is why WI-1038 waits for LLR-395's acceptance: a circle. Break
  it with a new `Drafted` test case verifying LLR-395, citing the tests of
  its rule, so both can be accepted together. Say in the Deliverable whether
  WI-1038 is still needed afterwards.

## Done-when

- [ ] LLR-373's Detail states the join and the seam placement as the code
      does, consistent with LLR-199 and TC-435 (text only; it drifts).
- [ ] TC-081's method and expected cells state LLR-080's rendering, and its
      evidence tests assert exactly that (text only; it drifts).
- [ ] LLR-393, LLR-394, TC-455 and TC-456 name no implementation carrier in
      their requirement text.
- [ ] Each of LLR-398's five clauses above is verified by a test case citing
      an existing test.
- [ ] A `Drafted` test case verifies LLR-395.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; the
      Deliverable lists every row changed and what a second sitting owes.
