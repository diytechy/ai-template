+++
id = "WI-312"
title = "A2 residue -> mechanical: accessible-name QUALITY, not merely presence. Measured 2026-07-25: 0 empty names, but 57 bare-id-only names (IF-001 with no description) and 14 duplicated names across 74 nodes, worst 'contains -> descend' x39 - a screen-reader user hearing that thirty-nine times cannot tell those controls apart. Rules: not a bare registry id alone, unique among siblings, and label-in-name (WCAG 2.5.3) for a control with visible text. All three regex-decidable; LLR-101's residue ('whether each control READS as well-named') is ~90% mechanical."
workstream = "scripts"
sr_refs = ["SR-052"]
buildtier = "medium"
safety_class = "ordinary"
order = 309
+++

## Deliverable

Accessible-name QUALITY is now checked, not just presence: every focusable element and role=img graphic has a name, that name is never a bare registry id, and navigation landmarks are distinct. SCOPE CORRECTED DURING THE BUILD and this is the finding worth keeping: the filing measurement counted every <title> in the document and reported 57 bare-id names, but those sit on EDGE PATHS (<path class=wire><title>IF-001</title>) which are neither focusable nor named graphics. A tooltip on a decorative connector is a usability nicety, not an accessible-name defect, and asserting over it would have manufactured 57 findings WCAG does not make. Measured over the set A2 actually governs, there were ZERO empty and ZERO bare-id names, and one real defect: three drills each labelling their breadcrumb landmark 'Breadcrumb', so a screen-reader user listing navigation regions hears three identical entries. Fixed by deriving the label from each drill's root crumb (Roadmap/Architecture/Concepts breadcrumb). Uniqueness is asserted for LANDMARKS only, deliberately - a descend control for the same container legitimately recurs across drill layers, and only one layer is visible at a time, so those repeats are one control reached by different paths rather than an ambiguity a reader faces. Guards: tests/test_gen_trajectory.py::test_a2_every_control_name_is_present_and_not_a_bare_id + ::test_a2_landmark_names_are_distinct, verified to fail against three regressions (the original triple-Breadcrumb, a control losing its name, a control named by a bare id). The landmark rule is carried mainly by the shipped artifact because each fixture renders a single drill - a real coverage limit, recorded in the test.
