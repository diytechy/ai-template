+++
id = "WI-526"
title = "State the finding/severity/exit protocol once, as IF-144 at the B-05 boundary (OI-64 ruled (b))"
specref = ""
workstream = "requirements"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

`IF-144`, one interface row stating the reporting protocol every delivered
checker already honours. No existing row was edited — option (b) is state-and-
sweep-nothing — and no code or test changed.

**The shape question resolved on the evidence rather than by a second ruling.**
It first read as a blocker: an interface row carries one `provider` or one
`component`, and this contract has fourteen providers whose ten restating rows
split five and five across `CMP-006` and `CMP-007`, with `SR-181` in neither.
That was the wrong axis. The protocol is not a module-to-module seam — it is
what the delivered harness presents at its **package boundary**, and all ten
restating rows cite **`B-05` unanimously**. Twenty-eight rows already carry
`interface_to_external = "B-05"`, so `IF-144` takes an established shape, and
the owner's direction had anticipated it in saying an external far side is a
boundary-line interface.

**What the row states:** a finding names its location — the at-fault row and
cell, `file:line`, or the module — unless it is population-level and no single
location exists; it carries a severity from the closed set OK / SKIP / WARN /
FAIL; an advisory class never reaches the exit code; a declared strict flag is
the only promotion from warning to failure; an absent optional input exits zero
and names the absence. `owner = SR-157`, the row that already states most of it;
`req_refs` names all ten.

**Two clauses deliberately absent, both recorded in the row's `rationale`.**
"Every degrade is named, never silent" is not stated, because `SR-181`'s
acceptance permits a silent degrade where no prior committed state exists while
`SN-008` forbids one — stating it would red an `Approved` row on the day this
one landed. And the closed set is four *dispositions*, not twelve exact tokens:
the checkers spell those four with twelve labels, and the row states the
contract they honour rather than a rename they do not.

**The row honours the rules it is written under.** First draft tripped four of
the registry's own advisories — over the 500-character ceiling at 732, an
argument in the `contract` cell, and a date stamp in `notes`. Thinned to **466
characters** with the argument moved to `rationale` and the provenance dropped.
One advisory remains and is the accepted directory-provider pattern `IF-025` and
`IF-026` already carry (`best-effort join; a module with no LLR is legitimate`).

## Context

`OI-64` ruled (b) on 2026-08-28. Ten requirement rows each carried a fragment of
this protocol as a secondary clause and none took it as its subject, so a new
checker could violate it without failing anything. The 2026-08-25 census had
already established the protocol is honoured in behaviour — 141 of 158 finding
sites name a location, no advisory reaches an exit code, 12 of 14 checkers are
vacuous on an absent optional input and say so — so the row states a delivered
property, not new work.

## Done when

- [x] One interface row states the protocol; no existing row edited.
- [x] The row sits at the boundary its requirement rows cite.
- [x] The silent-degrade guard honoured.
- [x] The row passes the registry's own contract-cell rules.
- [x] Commit bar green.
