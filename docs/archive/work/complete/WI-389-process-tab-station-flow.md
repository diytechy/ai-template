+++
id = "WI-389"
title = "RULED 2026-07-31 (docs/concurrency-v2.md, owner direction 2026-07-31) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. Land the concurrency-v2 flow in PROJECT_STATE.html's PROCESS TAB, so the dashboard's method reference shows the process the state actually moves through. Filed as its own row at the owner's direction: it is a render change with its own critique surface, and folding it into WI-381 or WI-386 would hide a visual deliverable inside a scripts row. TODAY the tab renders the WI-250 two-intersecting-hoops picture (traj_panels.py §the Process tab, WI-085/SR-050/SR-055): an intake loop and a human-decision loop overlapping at one shared LLM_Agent hub, fully server-computed with fixed trig and .1f rounding so the --check freshness byte-compare stays stable. That render predates the station model and does not show it. WHAT MUST APPEAR: the lane/station cycle (claim -> build -> refresh -> merge slot -> merge -> unload) with the merge slot drawn as the serial waist that only one branch occupies; the SPINE BARRIER (lanes drain, the batch runs alone, one window, one owner sitting); and the three TERMINAL OUTCOMES converging on the merge, since 'every lane ends in a merge' is the property most worth making visible - a reader who sees three arrows into one merge cannot come away thinking a branch may hang. RESPECT THE EXISTING CONSTRAINTS, they are not incidental: server-computed geometry only (no clock, no randomness, sorted output) or the --check byte-compare breaks and the dashboard reds its own freshness gate; the WI-085 anti-duplication ruling limits in-view prose to relationships no single doc states as one picture, everything else LINKS to its canonical home; and a data-less repo must render identically. Note gen_trajectory.py sits at 949 lines under the per-module size ratchet with traj_panels.py already split out at WI-280, so this render belongs in traj_panels.py and must not re-grow the facade. VERIFY BY LOOKING AT PIXELS, not by reading source: use the render-dashboard-critique skill across the declared width/theme matrix. That is the lesson of the WI-250 redesign this replaces - the prior render laid the loops out as CSS-grid racetracks and a render critique judged the actual pixels, finding the flow direction invisible (a border is not a directed cycle) and the junction reading as a box off to the side rather than the point where the loops meet. A diagram of a concurrency model is exactly the kind of thing that reads correct in source and wrong on screen. RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
needs = ["WI-381", "WI-386", "WI-387"]
+++

## Deliverable

Shipped 2026-08-02, work commit 56dc580d. SpecRef-clock re-validated first
(the standing WARN): the post-mint amendment to docs/concurrency-v2.md
(f822e336, 2026-08-01) restates only the §B2 "Specs mirror it" archive prose
(OI-11 ruled (a)); §A2/§A3/§A4/§A8 — the flow this row draws — are untouched,
so the row stood as written.

The Process tab's panel 2 is now THE STATION CYCLE, one directed closed SVG
ring in `traj_panels.py` (`_station_svg`/`_station_panel`, replacing the WI-250
hoops and the pre-station resume-loop chips): dispatcher tick → claim → lane
build (stacked-shadow multiplicity) → the three terminal outcomes converging
as three arrows into the station refresh (merge trunk in · trunk_step · bar →
Bar-Green @ branch tip) → the sub-second MERGE SLOT drawn as the serial waist
(the one emphasized node, on the `--hub`-renamed `--slot` theme-invariant
token; "serial · one branch at a time · ancestor check → --no-ff merge") →
trunk advance → the post-merge intake mint (amendment · disposition · drafts)
→ back to the tick. The SPINE BARRIER is a gate glyph on the admission edge;
the bounded lost-race retry is the one dashed edge; the admission arms,
exclusive kinds, empty-frontier ladder and red-bar/handback notes ride the esc
list. Constraints held: server-computed fixed geometry (`.1f`, sorted, no
clocks), links via existence probes, byte-identical data-less render, `--check`
stable, no external assets, facade un-grown (gen_trajectory 950→952, only the
`--slot` token comment + the re-export rename; the render lives in
traj_panels.py, 984→1145, under the 1500 ratchet threshold).

THE VOCABULARY IS DERIVED, NOT PINNED TO ITSELF (the 2026-08-01 review's
constraint): outcome names + their declaring spec dirs from
`integrate.OUTCOME_DIRS`, the attestation label from `integrate.BAR_GREEN`,
the exclusive kinds in rank order from `schedule._KIND_CONCURRENCY`/`_KIND_RANK`;
the two label sets with no exported constant (`_ADMISSION_ARMS`, the intake
trigger words) are held by sync pins against `dispatch._kind_action` over
every kind × gate-policy level and `intake.tier_signal` + the mint arms'
callables (tests/test_traj_panels.py, the WI-389 station suite — red-first,
9 failed before the render existed).

VERIFIED BY PIXELS (render-dashboard-critique matrix: 36 shots, light+dark ×
390/1280/1680, read back, plus 2x station crops from the 1680 pair): the ring
reads as a directed cycle with three arrowheads converging on the refresh, the
slot pops white-on-#4f46e5 in both themes, the barrier gates the admission
edge, 390px scales without horizontal overflow. Two findings driven out
before close: the refresh card's attestation note truncated mid-token at the
34-char budget (now "green ⇒ Bar-Green @ branch tip", whole), and the
lost-race dashed edge emerged from under the slot card's shadow (start moved
clear). PROJECT_STATE.html is not committed on this branch (§5.2
trunk-owned); the station refresh regenerates it at merge.

Registration: the station refresh convicted the original "none owed"
judgment — the derived-vocabulary imports are CROSS-COMPONENT (traj_panels
CMP-002 → integrate/schedule CMP-004) and owed declared seams. Reworked
2026-08-02 (station red, one rework commit): IF-093 (traj_panels Consumes
integrate.OUTCOME_DIRS + BAR_GREEN; Notes carries the `sink` marker — a
render leaf provides nothing across components) and IF-094 (traj_panels
Consumes schedule's kind tables) in docs/requirements/interfaces.csv, the
single-line `Contracts: IF-093, IF-094` docstring citation in traj_panels
(the WI-381 wrapped-paragraph trap avoided), and TC-056's Verifies extended
with both IF ids — its evidence tests are the sync pins that genuinely drive
the seams (the WI-388 finding-4 lesson). Proven by scratch-regen: arch map
regenerated rc=0, then `check_trajectory.py --strict` rc=0 with both
cross-component ERRORs gone and the WARN list at trunk baseline minus the
now-named traj_panels connectivity WARN; `trace.py --strict
--no-placeholders --html --require-verified --strict-schema` rc=0
(interfaces=91, interface-findings=0); docs/architecture.md restored
un-committed (§5.2 trunk-owned). The TRACED pointer cells follow the code
(TC-051/TC-056 Evidence → the real test nodes in tests/test_traj_panels.py;
LLR-056 CodeSymbol → process_panel/_station_panel). DEVIATION, recorded for
WI-390: the RATIFIED
prose of SR-050/SR-055/LLR-051/LLR-056/TC-051/TC-056 still describes the
resume-loop/hoops picture — amending it is the program close's spine scope,
not this ordinary row's.

Watched on 56dc580d: tests/test_traj_panels.py 34 passed in 6.12s
<!-- fig: cmd="python -m pytest -q tests/test_traj_panels.py" rev=56dc580d -->;
smoke 663 passed / 6 skipped in 13.14s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=56dc580d -->;
full suite 1959 passed / 10 skipped in 317.08s (0:05:17)
<!-- fig: cmd="python -m pytest -q -n auto" rev=56dc580d -->;
`check_trajectory.py --strict` rc=0 · `check_doc_refs.py --strict` rc=0 ·
`check_figures.py --strict` rc=0.
