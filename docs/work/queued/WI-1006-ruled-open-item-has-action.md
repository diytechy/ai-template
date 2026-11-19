+++
id = "WI-1006"
title = "run.cmd audit reports each ruled open item with no action planned, done or handed on to a later open item"
workstream = "process"
sr_refs = ["SR-148"]
specref = "docs/specs/WI-1006.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request). The spec of
record holds the rule, why it reads text rather than `needs`, and the numbers
a prototype measured on this repo. Its scope critique is owed before a claim.

No SR states this today. The critique decides whether one is owed, or whether
IF-073's registry contract carries it.

## Done-when

- [ ] A check reports, warn-only, each `ruled` open item that has none of: a
      work item in an open or complete directory whose text names it; a later
      open item naming it that is `pending`, or `ruled` and itself covered;
      a `follow_up` cell. The rule is the spec's.
- [ ] The open-items template's header documents the optional `follow_up`
      cell and asks a follow-up item to name the item it continues; the `-000`
      row shows it. This repo's registry follows.
- [ ] `run.cmd audit` runs the check, and a finding does not change its exit
      code.
- [ ] The four ruled items it reports at filing (OI-35, OI-79, OI-89, OI-90)
      each gain a `follow_up` cell or a citing row, so it lands with 0
      findings.
- [ ] Regressions name each arm: covered by a draft, queued, active, deferred
      or complete row; not covered by a cancelled, partial or restructured
      row; handed to a pending item; handed through a ruled item
      that is itself covered; a cycle of ruled items with no row; a
      `follow_up` cell; no registry (vacuous); a registry that does not parse
      (stops, as the readers do).
- [ ] A RESYNC entry if the check ships to adopters: a new optional key, no
      forced migration.

## Critique dispositions

Round 1 (Gemini Argon, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1006.md`): CHANGES-REQUESTED,
two MAJORs and one MINOR. All three are adopted, and none grows the row.

- **S4, the planning ruling: adopted as `planmode = "single"`.** The check
  judges every ruled item against every work item and every other open item,
  and it touches three modules, so a short plan precedes the code.
- **S5, the architectural delta: adopted.** The spec of record's
  "Architectural delta" settles each of the three questions:
  - the anchor is SR-148 (Accepted), which already carries the ruling sync
    (LLR-298) and pending citation integrity (LLR-299). A new design row,
    LLR-370, states the check. No SR is minted;
  - IF-073's contract, in its row and in the registry's header, carries the
    optional `follow_up` cell and the cover rule. The check lives in modules
    that already read the registry: the rule in `kitlib/spine.py`, the read in
    `pending.py`, and the report as `gen_open_items.py --ruled-cover`. No
    module, seam or interface row is added;
  - the check ships, because all three modules and the open-items template
    are kit-owned. So Done-when item 6's RESYNC entry is owed: a new optional
    key, nothing forced.
- **S3, the input space: adopted.** The spec of record's "What is matched,
  exactly" closes the token boundary (`OI-35` never matches `OI-350`), which
  text is scanned (the whole work-item file, not its `specref` target), the
  `-000` rows, an item naming itself, the statuses, and when `follow_up`
  counts as set.

One reading is settled here as well. Done-when item 1 says "a later open
item", but the rule it defers to says "another open item" and compares no
dates. That is why item 5 can ask for a cycle.
