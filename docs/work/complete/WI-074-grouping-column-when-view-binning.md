+++
id = "WI-074"
title = "Grouping column + When-view binning"
workstream = "scripts"
needs = ["WI-030", "~WI-073"]
order = 73
+++

## Deliverable

P1 (2026-07-11): the grouping column + the When-view DAG binned by it. check_trajectory.load_wis reads a new grouping column - a mutable grouping tag in the Workstream precedent, no vocabulary check (legacy CSV reads empty; never-breaking). work-items.template.csv + the meta registry gain the column; the meta was backfilled honestly (WI-053..059 working-surface-restructure, WI-067..070 capability-expansion, WI-071..073 owner-feedback, WI-074..076 grouping-batch; every other row empty - no retroactive invention). gen_trajectory's When-view binner bins the WI DAG into collapsed native <details> grouping containers - the WHEN-axis mirror of the FB5 sw_containment idiom: members in a table (WI/Title/Status/Delivers/After), group-crossing predecessor edges aggregated to one deduplicated container-to-container edge (contributing WI edges listed), ungrouped WIs flat; a ungrouped registry returns None -> the flat SVG DAG renders byte-identically. Deliberately no right-sizing bound (efforts bounded by construction, one re-attestation sitting each). PROCESS_OPTIONS phase paragraph + template explainer row. No spine change: an optional grouping column mirrors Workstream and the binned render sits inside SR-038's roadmap-DAG claim (verified against SR-037/SR-038 text). Tests in test_gen_trajectory.py (containerize, flat, byte-identical, dedupe, --check-stable, meta smoke) + test_trajectory.py (never-breaking).
