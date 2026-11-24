+++
id = "WI-1075"
title = "A census test holds every shipped checker to IF-144's absent-input and advisory rules"
workstream = "process"
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, from
WI-1024's slice 3 record (`docs/plans/WI-1024/slice-3.md` on `maint/wi-1024` until that slice merges, section 6 item 2), which measured
IF-144 and proposed this row; the coordinator took the proposal.

IF-144 (`Drafted`, off-spine) is the severity protocol every shipped
checker claims: (1) a finding names its location unless it is
population-level; (2) a finding carries one of four severities; (3) an
advisory never reaches the exit code, a declared strict flag being the only
promotion; (4) an absent optional input exits 0 and names the absence. No
design row states it and no test drives it as a protocol, so F-4 (WI-1024)
cannot reach it through a constraining row, and its slice 5 makes an
unreached interface fail `--strict`.

The slice's measure: 18 checkers claim the protocol (the 17 `check_*`
scripts and the traceability check), not the 14 IF-144's notes count. Parts
1 and 2 cannot be driven on every checker by one census test (about 158
emission sites; the severity labels vary and IF-144's rationale declines to
freeze them). Part 3 can be driven partly and part 4 cheaply. Today a census
would fail on three carve-outs the code argues (the flows check's required
document, the traceability check's id watermark, the privacy scan's
git-only modes) and on two defects: the complexity census does not name an
absent baseline, and prints `FAIL` in its warn mode.

**Order.** Before WI-1024's slice 5, so IF-144 is reached when coverage
turns strict.

## Done-when

- [ ] A design row (a new `Drafted` LLR under the SR the plan names) states
      parts 3 and 4 for every shipped checker found by glob, so a new
      checker joins by default, with a carve-out table of the three argued
      exceptions, each with its reason; its `constrains` cell names IF-144.
- [ ] A census test (a new `Drafted` TC) drives part 4 on every checker and
      part 3 on every checker with an advisory class, red first against
      today's two complexity-census defects, which this row fixes.
- [ ] IF-144's text states parts 1 and 2 as judged at review rather than
      tested, and its notes count the checkers it covers.
- [ ] The rows keep the three row rules; a RESYNC entry for the shipped
      checker change.
