+++
id = "WI-711"
title = "TC-296 Method: state the standing reason the sweep excludes the committed dashboard, not its status"
workstream = "process"
sr_refs = ["SR-054"]
specref = ""
buildtier = "quick"
priority = 3
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Deliverable

Done by the coordinator as the batch-D adjudicator drafted it (a one-clause authoring edit to Drafted TC-296): its method's parenthesis now states the standing reason the sweep leaves the committed dashboard out (the case asserts the current emitter, which only a document rendered now evidences; the committed artifact's freshness is SR-070's contract), not the row's own status. TC-296 stays Drafted, and its first approval goes to the next spine-acts batch.

## Context

Drafted by WI-704 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

IN SCOPE — one cell, amended in place with status left `Drafted`, then the
first-approval adjudication the merge's sweep mints.

1. `TC-296.method`: the parenthetical "(the committed dashboard is an older
   renderer's markup, so it is left out)" states the row's own status at
   authoring time, and it is false at HEAD (`gen_trajectory.py --check`
   reports the dashboard up to date) while the test still excludes the
   shipped document. Keep the exclusion; state why it stands: the case
   asserts the CURRENT emitter, which only a document rendered now can
   evidence, whereas the committed artifact evidences whichever renderer
   last wrote it and its freshness is SR-070's contract. A reader with no
   history must not be able to reconstruct a correction from the cell.

OUT OF SCOPE: the test itself (it already sweeps the fresh fixtures only),
LLR-285 (approved), and whether the shipped artifact should ALSO be swept —
that would be a new claim, not a re-wording.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-055 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/rendering/traj_views.py :: build_html/_nav/when_view] tests: (see TC-055) — Dashboard usability rendering
- LLR-099 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/rendering/traj_panels.py;project-trajectory/scripts/rendering/traj_render.py :: know_view/sw_view/_render_drill] tests: (see TC-102) — Default-density start-collapse (T2 core)
- LLR-100 [project-trajectory/scripts/rendering/traj_render.py :: _render_drill/DRILL_SCRIPT] tests: (see TC-103) — Detail-in-context breadcrumb (T3 core)
- LLR-105 [project-trajectory/scripts/rendering/traj_render.py :: _ring_ink/_ring_style/_cedge_marker] tests: (see TC-108) — Interactive-control contrast in both themes (T5 core)
- LLR-115 [project-trajectory/scripts/gen_trajectory.py;project-trajectory/scripts/rendering/traj_panels.py :: build_html/_next_work_html/_nav] tests: (see TC-120) — Task findability - labelled entry within one tab switch (T1…
- LLR-116 [project-trajectory/scripts/rendering/traj_render.py :: _svg_fit_style/SHRINK_FLOOR] tests: (see TC-121) — Viewport-fit by scale-to-fit with a legibility floor (T7 co…

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-011 scripts/gen_trajectory -> scripts/check: exit-code 0 clean or vacuous · 1 invalid registry, stale HTML, or stale status snapshot under --check
- IF-024 docs/work/ -> scripts/gen_trajectory;external:downstream adopter: file None
- IF-052 scripts/traj_parse <- scripts/rendering/traj_panels: call traj_parse._stage_value: the stage field of docs/stage, or None (the Process tab's omit condition)
- IF-056 scripts/check_trajectory <- scripts/gen_trajectory: call check_trajectory loaders: validate, read_registry_rows, load_wis, load_known_srs, read_trajectory_enabled, WI…
- IF-071 scripts/schedule <- scripts/gen_trajectory: call load_registry_rows, load_wis, frontier, evaluate; empty when the module is absent
- IF-083 scripts/check_trajectory <- scripts/rendering/traj_views: call check_trajectory joins: read_rows, load_seams, component_top_view, _norm_module, _split_refs, SR_CSV, TOP_VIE…
