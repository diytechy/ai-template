+++
id = "WI-528"
title = "The interface row shape in code: owner, channel, data; five cells retired; the kit's registry converted (OI-67 slice 1)"
workstream = "architecture"
sr_refs = ["SR-159", "SR-157"]
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The interface row is ONE OWNER, its FAR SIDE, and a TYPED STATEMENT, and every
reader and check reads it that way. Record:
[../../../log.d/2026-08-29-wi528-if-row-shape.md](../../../log.d/2026-08-29-wi528-if-row-shape.md);
the shape of record is the plan's §1, whose decisions 8 (the far side names
the direction — `requestors` | `consumers`, exactly one, the owner's own
addition mid-slice) and 9 (header-first for parallel work) this slice added.

**Schema.** `Owner` (a path or `external:` party, never an id), `Channel`
(closed, `kitlib.spine.IF_CHANNELS`), `Version`, `Status` required; exactly
one of `Requestors`/`Consumers`; `Data` optional (≤160, the five form rules
moved onto it); `Contract` legacy and counted by one advisory. `Provider`,
`Req-Refs`, `Signal`, `SignalNote` retired from the vocabulary.

**Readers.** `seam_owner`/`seam_requestors`/`seam_consumers`/`seam_far_side`
replace `seam_provider` and the design-tier join; `load_ifs`, the declared
pairs, component placement, the arch-map and dashboard seam graphs (arrows
drawn the way the information runs), the planning-brief surface, the OKF
export, the intake seam lines and the release checklist all read the new
cells. `trace.interface_findings` checks the far-side rule and the owner's
shape (strict) and its reachability through a design row or an `Implements:`
line (warn).

**The kit's registry** converted: 136 rows, `owner` folded from the stated
provider or the LLR's module (21 published media named by hand), `channel`
seeded from the per-row classification, the far side seeded from the channel
(70 requestors / 66 consumers), the header rewritten. Templates and the field
table pulled forward so the shipped kit describes the cells the code reads.

**Not this slice, stated:** the seeded `channel` and far side are
classifications confirmed in slice 3; `contract` cells (136) and the moot
ownership notes leave in slice 3; `PROCESS.md` §8 and the reference docs are
slice 5; the gate arms at slice 6.
