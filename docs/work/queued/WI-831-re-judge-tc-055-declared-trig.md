+++
id = "WI-831"
title = "re-judge TC-055: declared trigger fired [sha256:463ba32184eb] at merge a8458c2"
workstream = "process"
sr_refs = ["SR-054"]
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-055"]
+++

## Context

The merge checkpoint at a8458c2 found observation test case TC-055 due for re-judging.

- What changed: its declared trigger component:CMP-009 fired after its work-item floor.
- Method: A fresh, family-heterogeneous CRITIQUE session (LLR-048/LLR-082 loop) adjudicates the generated PROJECT_STATE.html against docs/rubrics/dashboard-usability.md, receiving the rubric + SN/SR intent + the rendered PNG matrix from scripts/dashboard-shots/shoot.mjs (widths x themes x tabs) as the artifact recipe and never the implementer's self-assessment; VERDICT machine line cites numbered anchors.
- Expected: APPROVE citing numbered anchors. The rubric is the single home of the live-vs-retired anchor set: its header states the live set, and each retired anchor carries its retirement and binding in place. A verdict cites only anchors the rubric lists live, never a retired one; a clause a test now holds is verified through the LLR/TC chain the registry records, not by a verdict. Standing limit, so this row is never read as live coverage: the verdict recorded in Evidence is re-judged when no result of it is on record or when the record passes its declared max_age, and otherwise only when its declared trigger fires after its closed-work floor, never on every commit. This row's assurance is therefore as old as its latest recorded verdict, and a clause needing assurance newer than that is one to bind to a test rather than to re-judge here.
- Rubric: docs/rubrics/dashboard-usability.md
- Declared inputs: docs/rubrics/dashboard-usability.md; SR-054; LLR-055; project-trajectory/scripts/gen_trajectory.py; project-trajectory/scripts/rendering
- Result lifetime: 90 days
- Latest result: TC-055.2026-10-05T034207Z.toml (pass, observed 2026-10-05T03:42:07Z, expires 2027-01-03T03:42:07Z)
- Inputs digest at a8458c2: sha256:463ba32184ebfc750d94953db21d81d4407ac1316fbe20af6f9e13c6636d47b0

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-055 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-055 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/rendering/traj_views.py :: build_html/_nav/when_view] tests: (see TC-055) — Dashboard usability rendering
- LLR-099 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/rendering/traj_panels.py;project-trajectory/scripts/rendering/traj_render.py :: know_view/sw_view/_render_drill] tests: (see TC-102) — Default-density start-collapse (T2 core)
- LLR-100 [project-trajectory/scripts/rendering/traj_render.py :: _render_drill/DRILL_SCRIPT] tests: (see TC-103) — Detail-in-context breadcrumb (T3 core)
- LLR-105 [project-trajectory/scripts/rendering/traj_render.py :: _ring_ink/_ring_style/_cedge_marker] tests: (see TC-108) — Interactive-control contrast in both themes (T5 core)
- LLR-115 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/rendering/traj_panels.py :: build_html/_next_work_html/_nav/_blocked_item/_waiting_item/_next_work_item/_next_work_none] tests: (see TC-120) — Task findability - labelled entry within one tab switch (T1…
- LLR-116 [project-trajectory/scripts/rendering/traj_render.py :: _svg_fit_style/MIN_RENDERED_NODE_LABEL_PX/NODE_TYPE_PX] tests: (see TC-121) — Viewport-fit by scale-to-fit with a legibility floor (T7 co…

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-011 scripts/gen_trajectory -> scripts/check: exit-code 0 clean or vacuous · 1 invalid registry, stale HTML, or stale status snapshot under --check
- IF-024 docs/work/ -> scripts/gen_trajectory;external:downstream adopter: file None
- IF-052 scripts/traj_parse <- scripts/rendering/traj_panels: call traj_parse._stage_value: the stage field of docs/stage, or None (the Process tab's omit condition)
- IF-056 scripts/check_trajectory <- scripts/gen_trajectory: call check_trajectory loaders: validate, read_registry_rows, load_wis, load_known_srs, read_trajectory_enabled, WI…
- IF-071 scripts/schedule <- scripts/gen_trajectory: call load_registry_rows, load_wis, frontier, evaluate; empty when the module is absent
- IF-083 scripts/check_trajectory <- scripts/rendering/traj_views: call check_trajectory joins: read_rows, load_seams, component_top_view, _norm_module, _split_refs, SR_CSV, TOP_VIE…
