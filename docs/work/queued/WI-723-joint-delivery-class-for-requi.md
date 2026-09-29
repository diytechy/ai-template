+++
id = "WI-723"
title = "Joint-delivery class for requirements (OI-97 (a)): a delivered_with cell, SR-193's chain amended, the nine rows classified"
workstream = "scripts"
specref = "docs/requirements/open-items.toml"
sr_refs = ["SR-193"]
needs = []
buildtier = "medium"
priority = 3
safety_class = "spine"
+++

## Context

OI-97 ruled 2026-09-28: option (a), with the owner's directions below. Approved
SR-193 classifies a requirement as bridged (it cites the assumptions its
argument relies on), coincident (a waiver saying its own specification alone
delivers its needs) or unclassified. Nine approved rows fit none honestly.
Each is one link of a need that several requirements deliver together:
SR-015, SR-024, SR-033, SR-111, SR-129, SR-174, SR-177, and the labelled
derived SR-223 and SR-225 (wave-5 ruling 47).

The owner's directions:

- **No inheritance.** A joint requirement does not inherit its siblings'
  assumptions. Assumptions stand on their own, each coupled to the
  requirements that cite it. An assumption's needs stay derived only from the
  requirements citing it directly. One assumption may already be cited by
  several requirements, and a requirement may already cite several
  assumptions, so nothing new is needed for that.
- **Alignment is the adjudicator's to check.** The worry is that siblings
  drift apart. An adjudicator judging a joint row is asked to read its
  siblings and their assumptions and check they line up. That is a question
  on the adjudicator's list, not a mechanized rule.
- **Changing `delivered_with` re-opens the requirement's attestation**, as
  declaring or changing the `coincident` waiver does, so the row is
  requalified. The owner called this a trial: back it off if it causes too
  much iteration.

Scope:

- **Amend in place** (status left Approved, for the next spine-acts batch):
  - SR-193 `requirement` and `acceptance_criteria` gain the class. A
    requirement naming in `delivered_with` the requirements that, with it,
    deliver its needs is classified joint. A sibling that is not a declared
    SR fails the check, naming the requirement (as an undeclared assumption
    does). A sibling sharing none of the row's needs is reported. Changing the
    cell re-opens the row's attestation.
  - LLR-222 (schema, carrier, template), LLR-223 (the classification) and
    TC-220 / TC-222 follow.
  - The drafter decides how the class combines with the other two and argues
    it. A suggested starting point: joint with `da_refs` is legitimate (a link
    can also rest on a world premise); joint with a `coincident` waiver
    contradicts itself and is reported without failing, like "both".
- **Build:**
  - the `delivered_with` key in `kitlib/spine.py`'s SR tuple, the carrier
    (`spine_carrier.py`, `migrate_carrier.py`) and
    `registries/system-requirements.template.toml`;
  - the class in `assumption_rules.py` (`SR_CLASSES`,
    `sr_classification_advisories`);
  - the per-need view (`traj_parse.need_assumptions`, `traj_views`) counting it;
  - the attestation re-open.
- **Classify the nine:** write `delivered_with` on each of the nine rows, with
  each sibling list argued from that row's rationale. The breakdown given to
  the owner is a starting reading, not the answer:
  - SR-015 with SR-157;
  - SR-033 with SR-006 and SR-049;
  - SR-111 with SR-036 and SR-011;
  - SR-174 with SR-148 and SR-170;
  - SR-177 with SR-156 and SR-170;
  - and so on for the rest.

  This re-opens their attestation, so the nine go to the next spine-acts batch.
- **Adjudicator guidance:** add the alignment question to the `spine-authoring`
  skill's question list. Beside it, add the tier check the owner's unease
  points at. SRs are boundary-driven. A joint row that still states a
  behaviour at a boundary is a real SR delivering its need jointly. A row
  whose output crosses no boundary and is consumed only by a sibling
  requirement is a design decision and belongs at LLR.
- **Adopter note:** a RESYNC_PACK entry for the new optional cell. There is no
  new failure: the tier is warn-only until `assumption_gate` is armed.
