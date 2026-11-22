+++
id = "WI-1053"
title = "A files-mode adopter's listed header files are held to one contract body per interface, or the rule says why not"
workstream = "process"
sr_refs = ["SR-159"]
needs = []
specref = "docs/archive/work/complete/WI-1048-answer-wi-1047-verdict.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
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

## Done-when

- [ ] The scope critique settles the question with evidence (which adopter
      profiles run in files mode, and what their listed headers hold), and
      the row is built to that answer: either listed headers join the
      surface in files mode, with LLR-398 amended and a test for each
      profile, or LLR-398's rationale states why files mode scans none.
- [ ] Either way, an amendment to an accepted row is text only and listed
      as owed to adjudication.
