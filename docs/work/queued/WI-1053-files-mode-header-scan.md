+++
id = "WI-1053"
title = "In files mode the one-contract-body check reports itself dormant; LLR-398 says why headers are not scanned alone"
workstream = "process"
sr_refs = ["SR-159"]
needs = []
specref = "docs/archive/work/complete/WI-1048-answer-wi-1047-verdict.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from
WI-1048's Deliverable ("a question for later"). LLR-398 states what the
one-body check scans: listed header files join the contract-body surface
only while the scan profile is not in its files mode and the declared
source root is present. In files mode, or with the source root absent, there
is no surface at all, so a configuration file or registry header the scan
profile lists is not held to one body per interface. The header list exists
to put such files on the surface, and files mode is the profile of a
project whose source the symbol scan does not read, so a files-mode adopter
may expect its listed headers checked. Changing that is a code and row
change; WI-1048 kept to stating what the code does.

**Settled at the scope critique (2026-11-22), from the repository.**
`stack.ini.template` documents files mode as the declaration "no Python
source here", seeded by a non-Python bootstrap, which keeps the
source-scanning layers "dormant rather than passing vacuously". In files
mode the source tree is not parsed for contract bodies, so holding only the
listed headers to one body per interface would certify a partial surface:
a header's body could repeat one in source the scan never read. So this row
takes the conservative branch. The check says it is dormant, as the other
layers files mode keeps dormant do, and the rationale says why. Reading
contract bodies from a non-Python tree's comment headers would be a feature
of its own, filed if an adopter asks. The row gives no file authority over
a hold, an act or a gate.

## Done-when

- [ ] In files mode, and with the declared source root absent, the
      one-contract-body check reports itself dormant where the strict
      check reports its findings, as the layers files mode keeps dormant
      do, instead of passing in silence; if it already does, the row cites
      where. A test covers each of the two cases and the symbols mode with
      the root present.
- [ ] LLR-398's rationale states why listed headers are not scanned alone
      in files mode, and any text its detail needs for the dormant report.
      Its amendment is text only and listed as owed to adjudication.
