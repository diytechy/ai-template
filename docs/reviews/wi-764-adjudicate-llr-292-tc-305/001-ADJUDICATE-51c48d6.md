# WI-764 adjudication: LLR-292, TC-305 (first approval) at 51c48d6

Adjudicator: Claude Opus 5.5, independent; directed none of WI-758.
Read: the brief's chain (SR-054, its LLR-055/099/100/105/115/116/117/119/120/285
siblings, their TCs), `project-trajectory/scripts/rendering/traj_graph.py`,
`tests/test_traj_lanes.py`, `docs/rubrics/dashboard-usability.md` (T8 and its
header), WI-758's row and Deliverable, and the Sonnet reviews r1/r2.

- [APPROVE] LLR-292 -> the emitter shall draw no two distinct edges overlapping along a segment or joining end-to-end outside a shared actual terminal, in the freshly emitted How, When, Process and System-context SVGs including every drill layer; sharing a node id does not excuse a join off the port; crossing count is explicitly not claimed -> upward it realizes the "follow any edge" clause of SR-054's legibility bar as concretized by rubric T8, whose text now names lane separation test-bound to this row; sideways it takes exactly the clause LLR-120 marks "DELIBERATELY NOT" and leaves crossing minimization with LLR-055/TC-055, so no anchor is held twice; downward TC-305 checks the outcome on emitted geometry -> ready: a closed, observable obligation with its scope named. The channel/terminal-reservation sentence is design direction verified only through its outcome, which is the right verification for it.
- [APPROVE] TC-305 -> generate the dashboard in memory from the live registries with the current emitter, sweep every emitted path in dag/sw/context/process (every inline SVG, drill layers included), flag collinear positive overlap and authored-vertex joins between distinct wires except at a point both share as a terminal, assert each view has wires, and pin the oracle on the x=452 overlap, x=220 join, a perpendicular crossing, a separated pair, a shared terminal with and without a shared run, and a corner join -> `tests/test_traj_lanes.py` does exactly this (`_violations`, `_shared_run`, the two oracle tests); r1 recorded it red against the base router (2 failed: dag, sw); I ran it green here; the arch section emits no routed wires, so the four views are every wired view this repo's artifact draws -> ready.

Non-blocking observation (not a finding against these rows, which state their
scope honestly): the rubric's T8 preamble still lists the Knowledge graph among
wired diagrams, while LLR-292/TC-305 do not cover it and the rubric now tells a
critic to judge crossings only. This repo renders no Knowledge tab, so nothing
is unwatched here today; a probe of the emitter fixtures found the tiered
knowledge drill clean (4 wires, 0 collisions) and the flat knowledge fixture
emitting no edges at all. Worth a change-intake look if the kit's Knowledge
graph is ever in this repo's artifact.

Commands run (worktree build/wi-764 at 51c48d6e):
- `pytest -q -n 2 tests/test_traj_lanes.py tests/test_traj_graph.py --basetemp $TEMP/wi764`: `37 passed in 54.66s`
- scratch probe applying `_violations` to every fresh `_every_emitter_document` SVG: 0 collisions in every SVG carrying wires (flat-dag, knowledge-tiered, tiered-drill, how-sw-drill, how-sw-flat, process incl. the 13-wire station SVG)

OUTCOME: APPROVE rows=2
