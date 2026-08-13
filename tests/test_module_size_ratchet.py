"""The no-new-monolith ratchet — repo-review-2026-07-22 H-2 (growth sensor).

The per-function complexity ratchet (test_complexity_ratchet.py) freezes how
hard any one function is to read. This is its file-scale sibling: it freezes how
large the kit's biggest scripts are, so the six coordinators the 2026-07-22 deep
review flagged as "beyond maintainable review scale" cannot silently grow while
the real decomposition (WI-280) is deferred.

Any kit script whose line count exceeds THRESHOLD must have an EXACT baseline
entry below. The census may only tighten by default:

- A baselined module grew, or a NEW module crossed THRESHOLD without a baseline:
  the fix is DECOMPOSITION (WI-280), not a baseline bump. A deliberate bump is a
  reviewed baseline edit whose reason lands in the WI/session log — never a
  drive-by. Moving lines into a new module is exactly the intended escape hatch:
  the new module stays under THRESHOLD (or earns its own reviewed baseline) and
  the shrunk one re-stamps downward.
- A module improved below its baseline (or dropped under THRESHOLD, or was
  renamed/removed): re-stamp its entry downward — or delete it — in the same
  commit, so the ratchet only ever tightens.

This is a growth SENSOR, not an approval of the current sizes. WI-280 is the
scoped decomposition that pays this debt down; every entry here is active
architectural debt, not a target.
"""

import pathlib

from conftest import SCRIPTS

# A module larger than this must be baselined. Chosen 2026-07-22 to sit above
# agent_common.py (then 1223) / agent_route.py (1181) so only the six
# coordinators the review named were frozen; a routine edit to a mid-size script
# does not trip the ratchet, but a mid-size script growing into a new monolith
# does. That is exactly what agent_common.py then did — it crossed at Phase 2b
# and has its own entry below — so the parenthetical above is the threshold's
# HISTORY, not a live census; the live census is `_census()`.
THRESHOLD = 1500

# Measured 2026-07-22 (len(text.splitlines()); files end with a newline, so this
# equals `wc -l`). These six are the review's H-2 modules. Re-stamp DOWNWARD as
# WI-280 decomposes them; an UPWARD re-stamp is the reviewed-baseline-edit escape
# hatch (see the module docstring) and must name its WI right here.
BASELINE = {
    # +76 (4511 -> 4587), WI-284: the generated Ready-frontier block — the
    # scheduler-derived forward-looking WI list that makes the forward-only
    # cascade structurally impossible (a `done` WI can't linger in status.md).
    # New behaviour, not monolith drift (the reviewed-bump escape the ratchet
    # documents; reason in docs/log.md 2026-07-23). Re-stamp downward with WI-280.
    # +11 (4587 -> 4598), WI-293: the A4 dark-theme hub-contrast fix — a
    # theme-invariant `--hub` token (white-on-fill was 2.98:1 in dark via
    # --accent) plus the rationale comment that keeps a successor palette change
    # off it. Nearly all of the bump is that comment; the code delta is 3 lines.
    # Reviewed bump, reason in docs/log.md 2026-07-24. Re-stamp down with WI-280.
    # +17 (4598 -> 4615), WI-296: the When explainer's interaction sentence is
    # now chosen by which emitter ran ($dag_interaction). It promised
    # "hover to highlight its neighbourhood" unconditionally, but that is the
    # FLAT emitter's behaviour — above the >3 rule the tiered drill renders and
    # the `.wi`/`.edge` sets the controller walks are empty. Most of the bump is
    # the comment recording that the flat path is LIVE (the small-project
    # default) and must not be deleted. Reviewed bump, log 2026-07-24.
    # +9 (4615 -> 4624), WI-297: `_svg_role` picks each emitted <svg>'s container
    # role from its BODY — group when it holds a focusable node, img only for a
    # genuinely non-interactive graphic — closing the children-presentational
    # role=img over 1,146 focusable descendants (A2). The +9 IS the helper; the
    # six call sites are a net wash (each gained a `body =` line and lost format
    # args). Deciding once from content, rather than hand-setting the role at six
    # sites, is what stops a future emitter reintroducing it — so the rule's
    # "decompose, don't bump" preference is met by not duplicating: the full
    # rationale lives in LLR-101, not in the docstring. Reviewed bump, reason in
    # docs/log.md 2026-07-25. Re-stamp down with WI-280.
    # +9 (4624 -> 4633), WI-297 correction: adversarial review refuted the first
    # pass — focusability is not only `tabindex`, since a native SVG <a href> is
    # tab-ordered without one, so the loops diagram kept role=img over 9 links.
    # The bump is the `_FOCUSABLE` pattern plus the comment recording WHY the
    # predicate has two shapes, which is the part a successor would otherwise
    # "simplify" straight back into the defect. Reviewed bump, log 2026-07-25.
    # -1 (4633 -> 4632), WI-297 dedupe: the G3 `dupes` step flagged the per-site
    # svg wrapper the WI-297 edits had left duplicated across dag/sw/know, so the
    # three now share `_svg_wrap`, which also folds `_svg_role` in — a call site
    # can no longer emit a container without the content-driven role. Ratcheted
    # DOWN, not sanctioned: the dedupe repaid both bumps above and one line more.
    # +97 (4632 -> 4729), WI-292/294/295/299 (119-CRITIQUE): new behaviour, not
    # bloat — `_ring_ink`/`_ring_style` compute a per-fill contrast-safe
    # highlight colour (one shared mechanism used by all four SVG emitters,
    # replacing two independently-drifting hardcoded hues), the reassigned
    # STATUS_FILL/TIER_FILL/OKF_TYPE_FILL/SW_NODE_FILL/PHASE_ACCENTS palette
    # carries the WHY-not-WHAT rationale for each de-collision, and the new
    # `--nhead` token gets its one documented-scale-step comment. Reviewed
    # bump, reason in docs/log.md 2026-07-25.
    # +62 (4729 -> 4791), WI-273 (SR-052, review M-3): the dashboard tabs became a
    # real WAI-ARIA tablist (role/aria-selected/aria-controls + tabpanel wiring, a
    # roving tabindex, and an arrow/Home/End keyboard controller). That fix lives
    # unavoidably in this module's HTML_TEMPLATE and its tab-emit helpers. The
    # train stamped 4573 off its OWN base (4511) and its compose re-stamped 4660
    # off the WI-293 baseline (4598) — both stale by integrate time, which is the
    # re-stamp-off-own-base conflict WI-289 tracks. Resolved to the ACTUAL
    # integrated count and keeping BOTH rationale chains rather than picking a
    # side. Reviewed bump, log 2026-07-25. Re-stamp downward with WI-280.
    # +11 (4791 -> 4802), WI-300 (U2 core): SW_NODE_FILL grows from a one-line
    # dict to a documented four-entry one, absorbing the `component` badge fill
    # that had been a bare literal inside `cmp_block`. Ten of the eleven lines
    # are the comment recording WHY an undeclared vocabulary member is a defect
    # (it is invisible to U5's collision sweep and to `_ring_ink`'s enumeration
    # alike) — the part a successor would otherwise inline straight back.
    # Reviewed bump, log 2026-07-25. Re-stamp downward with WI-280.
    # +70 (4802 -> 4872), WI-272 (review M-2): the six-status registry
    # vocabulary stops being rewritten into four. The code delta is small — a
    # `_wi_status` (true status) beside `_wi_st` (fill bucket), two glyphs, a
    # `data-status` attribute per node — and most of the bump is the
    # STATUS_BUCKET table's comment, which records WHY the grouping is kept
    # (minting two more hues would worsen the live U5 near-duplicate residue)
    # and WHY the clamp was a defect rather than a shared swatch (it ran before
    # the tooltip, accessible name, and detail JSON were built, so a parked row
    # SAID queued). Reviewed bump, log 2026-07-25. Re-stamp down with WI-280.
    # +16 (4872 -> 4888), WI-309 (U1 core): the type scale becomes DECLARED —
    # eleven steps in three documented families (node px / page rem / relative
    # em) replacing 18 raw font-size literals, of which four groups were
    # near-duplicate steps for one role 3-7% apart. The line delta is the
    # declarations plus the comment stating why three families rather than one
    # (a rem inside an SVG resizes labels out of fixed-px boxes) — the part a
    # successor would otherwise 'simplify' back into a single unit. Every call
    # site got SHORTER (a literal became a var()). Reviewed bump, log 2026-07-25.
    # +34 (4888 -> 4922), WI-310 (U3 core): fourteen weight/alpha/corner tokens
    # plus the SVG_RX declaration, retiring 8 stroke-widths / 7 opacities / 5
    # radii / 6 rx values — of which FIVE stroke widths were doing the single
    # job 'draw a connector'. Most of the delta is the two comments: the role
    # each token names, and WHY SVG_RX is a declaration the test enforces rather
    # than a value spliced into the rect templates (splicing with `+` rebinds
    # .format to the last fragment — a real bug this WI hit and backed out).
    # Reviewed bump, log 2026-07-25. Re-stamp downward with WI-280.
    # +6 (4922 -> 4928), WI-312 (A2 name-quality core): the three drills stop
    # labelling their breadcrumb landmark `Breadcrumb` and derive a distinct
    # name from the root crumb. One line of code; the rest is the comment on
    # WHY a present, correct name can still be useless (a screen-reader user
    # listing landmarks hears three identical entries). Reviewed bump.
    # +15 (4928 -> 4943), WI-313 (A3 core): two colour-alone defect fixes found
    # on first measurement — the What-tab tier legend hardcoded a stale TC
    # swatch (#047857, by then STATUS_FILL["done"]) and now derives from
    # TIER_FILL; and the flat How-SW seam graph encoded node KIND by fill with
    # no legend at all (only the containment drill had one), and gains the
    # shared `.legend` component. Half the delta is the two comments stating
    # the defect each block exists to prevent. Reviewed bump, log 2026-07-26.
    # +9 (4943 -> 4952), WI-313 rework (adversarial review F1): the emitted JS
    # tierColor/statusColor maps are SUBSTITUTED from TIER_FILL/STATUS_FILL —
    # the hand-copied literals kept the same stale tc hex the legend fix
    # missed, one screen further down. Most of the delta is the comment naming
    # that finding; the maps themselves got shorter. Reviewed bump, log
    # 2026-07-26.
    # +55 (4952 -> 5007; the last +4 is the F2 fix: the Modified projection line names --since for pre-regime streaks and the committed-brief home docs/ratify/), WI-316: pending-projection source (e) — one pointer
    # line per Draft SR (ratification owed) and per Modified SR (re-attest
    # owed), the surface that puts a pending re-attest on the owner's one
    # review surface instead of commit-message prose. New behaviour (the
    # projection gains a durable source), not monolith drift. Reviewed bump,
    # log 2026-07-26. Re-stamp downward with WI-280.
    # +105 (5007 -> 5112), WI-305 (SR-054 T1, 119-CRITIQUE): the landing "Next
    # work" surface — `_next_work_html` names the scheduler's ready frontier (the
    # SAME derivation IF-071 projects to status.md) on the hero, so "find the
    # next work" costs zero tab switches instead of a drill through nested When
    # blocks; waiting WIs carry their blocking predecessor. New behaviour (the
    # T1 defect had NO path at all), not monolith drift. Most of the delta is the
    # helper plus the comment recording WHY the surface exists and its
    # graceful-degrade posture. Reviewed bump, log 2026-07-26. Re-stamp downward
    # with WI-280.
    # +44 (5112 -> 5156), WI-306: the What icicle earns its tiering by scale -
    # panel() extracted so a subtree renders as its own drill layer, plus the
    # start-collapsed SN root layer above the SR-089 >3 rule. 119-CRITIQUE T2
    # MAJOR: the landing view opened the whole spine at LEAF scale (one unit per
    # TC) while the three wired tabs opened at a summary. Most of the delta is
    # the comment stating why capping depth does NOT fix a leaf-proportional
    # height. Reviewed bump, log 2026-07-26. Re-stamp down with WI-280.
    # +30 (5156 -> 5186), WI-307: _svg_fit_style + SHRINK_FLOOR, applied in the
    # three SVG wrappers so EVERY diagram scales to fit its container instead of
    # pinning a fixed pixel width (T7: all four 390px views demanded sideways
    # scroll; T4: the How graph clipped CMP-002 mid-label). Nearly all of the
    # delta is the comment explaining why a viewBox alone cannot fix it and why
    # the floor exists - pure scale-to-fit trades T7 for T4. Reviewed bump, log
    # 2026-07-26. Re-stamp down with WI-280.
    # +50 (5186 -> 5236), WI-317: the containment/descend arrow takes the same
    # per-fill --ring ink as the focus ring (T5, measured 1.06:1 light / 1.99:1
    # dark on the phase-1 fill). The code is small - _cedge_marker, a RING_INKS
    # constant, a per-layer marker dict; most of the delta is the comment on WHY
    # one marker per ink exists at all, i.e. that marker content renders from the
    # defs tree and cannot see the referencing node's custom properties. Without
    # that recorded, the next reader collapses the markers back into one and
    # silently restores the defect. Reviewed bump, log 2026-07-26. Re-stamp down
    # with WI-280.
    # -130 (5236 -> 5106), WI-322: the markdown-splice half of the pending
    # projection retired with docs/open-items.md (run_pending, _splice_pending,
    # _mask_machine_local and their marker constants). pending_block STAYS — it
    # is still the one derivation of what is pending; gen_open_items imports it
    # rather than growing a second opinion. Ratchet moving DOWN, which is the
    # direction WI-280 wants.
    # +40 (5106 -> 5146), WI-318: the shared drill label emitter FITS a sub-label
    # to the column it is drawn in instead of emitting it raw (`_fit_lines`, plus
    # a branch on how many sub lines came back). Bounded by construction — one
    # helper, one call site each side — and the alternative was worse for size:
    # every emitter budgeting its own sub is four copies of the same arithmetic.
    # Reviewed bump, log 2026-07-26. Re-stamp down with WI-280.
    # +46 (5146 -> 5192), WI-319: the next-work card stops budgeting its title by
    # character count (`_next_work_title` + the `_title_clause` split lifted out of
    # `_clip_title`, so the card and the status.md line share one clause extractor
    # instead of forking), plus five CSS rules for the native disclosure. Reviewed
    # bump, log 2026-07-26. Re-stamp down with WI-280.
    # +11 (5192 -> 5203), Phase 2b: this module reads the registry THROUGH
    # schedule/check_trajectory, so the second home costs it no loader at all —
    # the eleven lines are `docs/work` joining the `_asof` git-log source list
    # and the loop panel asking for whichever home exists (`wi_home`) instead of
    # hardcoding the CSV path, plus the comments saying why. The smallest
    # possible edit for a migration this size, which is the point of reading
    # through the sibling rather than parsing here. Re-stamp down with WI-280.
    # +53 (5203 -> 5256), Phase 3 (§5.6): `_pause_pending` surfaces a tracked
    # docs/work/pause in the pending block — declared `since` verbatim, no
    # clock, fail-closed rendering on a malformed file — plus the module
    # docstring's (f) purity-lettering entry for it. Reviewed bump,
    # log 2026-07-29. Re-stamp down with WI-280.
    # +25 (5256 -> 5281), WI-346: the DEDUPLICATION grew the file, which is the
    # WI-345 shape again. The code shrank — three re-derived SR/LLR/TC row
    # filters collapsed into one `_spine(root, skip_example=False)` and two
    # five-keyword `subprocess.run` capture blocks into one `_run_captured` —
    # but each helper now carries the docstring stating the contract its copies
    # left implicit (row order is the `--check` byte contract; `-000` is the
    # pending projection's rule; OSError propagates so callers own the off-git
    # degrade). Nine census sanctions went dead for +25 lines of prose.
    # Re-stamp down with WI-280.
    # -321 (5281 -> 4960), Phase 5 C2 (2026-07-29): the machine-local advisory
    # machinery left with the dispatcher — the refs/llm reservation/conflict/
    # quarantine/stranded-train pending sources, the run-state ask, the
    # PENDING_LOCAL_LABEL split and its mask. pending_block is now a pure
    # function of the committed tree. Ratcheted DOWN.
    # +1 (4960 -> 4961), Phase 5 item 3/C4 (2026-07-29): _blocked_pending's
    # docstring records the derived-blocked rule (queued + blockref — blocked
    # has no directory). Reviewed bump.
    # +6 (4961 -> 4967), Phase 5 C4 (2026-07-29): _wi_status DERIVES blocked
    # (queued + blockref) so the dashboard keeps the WI-272/M-2 distinction
    # the folder model would otherwise have erased — found by the fixture
    # conversion, fixed rather than re-grounded away. Reviewed bump.
    # +70 (4967 -> 5037), WI-323: corridor-aware lane routing — `_route_edges`
    # keeps a per-diagram ledger of the lane hops it has already placed and
    # `_detour_d` prefers a lane that is clear of every box AND of every occupied
    # corridor, with `_lane_candidates` offering a short outboard stack behind each
    # band edge so the pushed-off wire steps 10px rather than jumping a band. Half
    # the bump is the two new helpers (`_lane_seg`, `_corridor_clash`) and half is
    # the prose recording WHY the ledger cannot regress the T8 through-box floor and
    # how `_LANE_SEP` was dialled against the shipped render. Reviewed bump,
    # log 2026-07-29. Re-stamp down with WI-280.
    # +158 (5037 -> 5195), WI-366: the PORT HARNESS the WI-323 advisory critique's
    # first follow-up asked for — a shared port's strands rise to their
    # `_FAN_PITCH`-spaced heights over `_PORT_LEAD` px and coast to a staggered
    # turn-off before any routing bend, so the fan step is the RENDERED pitch and a
    # steep pair gets a horizontal gap too. ~55 lines are five small helpers
    # (`_harness_seg`, `_lead_rung`, `_port_strands`, `_harness_ends`, `_routed_dx`,
    # `_spliced_harness`) — the last four extracted so `_route_edges` stays under the
    # C901 bar rather than earning a complexity baseline entry, which cost lines to
    # save branches. The rest is prose recording WHY a control-point-only fan damped
    # to ~2.6px, why the turn-off ORDER (furthest traveller first) is load-bearing,
    # where the rung cap's residue lands, and the measured before/after at the two
    # named sites. Reviewed bump, log 2026-07-30. Re-stamp down with WI-280.
    # +79 (5195 -> 5274), WI-367: the same critique's SECOND follow-up — every
    # emitted diagram declared its viewBox as the LAYOUT box while the router sends
    # a wrap-around lane around the outside of its own endpoint boxes, so at rank 0
    # / the last rank the viewport clipped the U-turn. `_svg_frame` measures the
    # outboard ink off the BODY (like `_svg_role` before it) and grows the box to
    # it. ~35 lines are the three helpers (`_path_xs`, `_ink_overflow`,
    # `_svg_frame`) and the two call sites shrank; the rest is the comment that
    # ANSWERS the critique's open question (clip, not routing margin) with the
    # measured user-unit extents, and records why the ink is not shrunk to the box
    # instead — that would push the U-turn back through its own endpoint box, the
    # defect WI-257 removed. Reviewed bump, log 2026-07-30. Re-stamp down with WI-280.
    # -579 (5274 -> 4695), WI-280 S2: the pure layout/routing core
    # (_dag_ranks/_reorder/_layered_layout, _port_fan, the whole WI-253/WI-323/
    # WI-366 wire-router block) moved verbatim to the new sibling traj_graph.py
    # (614 lines, under THRESHOLD — no entry of its own). The +5 against the
    # bare move is the facade's re-export/docstring plumbing (the import block
    # comment + the split sentence). Ratcheted DOWN: the decomposition this
    # ratchet was holding the door open for.
    # -391 (4695 -> 4304), WI-280 S3: the parse/sources layer — the spine/OKF/
    # arch-map/gate readers, WORKSTREAM_LABELS, project vision/name, the
    # _run_captured/_asof/_git capture seam, and the guarded `schedule` import's
    # one home — moved verbatim to the new sibling traj_parse.py (434 lines,
    # under THRESHOLD). Ratcheted DOWN.
    # -836 (4304 -> 3468), WI-280 S4: the SVG/HTML rendering primitives — esc/
    # SCROLL_CUE/_hscroll, the declared colour+weight vocabularies (TIER/STATUS/
    # SW/OKF/PHASE, SVG_RX, ring inks), the responsive svg wrappers, the tab
    # helpers, and the shared drill renderer (_drill_layer_svg/_render_drill) —
    # moved verbatim to the new sibling traj_render.py (906 lines, under
    # THRESHOLD). Ratcheted DOWN.
    # -1087 (3468 -> 2381), WI-280 S5: the What/When/How-SW views — arch_icicle,
    # the flat DAG (dag_svg/_dag_layout + its constants), the How-SW seam graph
    # (sw_graph/_sw_node) and containment drill (sw_containment), _wi_status/
    # _wi_st, the tiered when_view (+_wi_phases/DEFAULT_PHASE), and the
    # _sw_panel/_cmp_panel tab panels — moved verbatim to the new sibling
    # traj_views.py (1141 lines, under THRESHOLD). Ratcheted DOWN.
    # -470 (2381 -> 1911), WI-280 S7 (built before S6 — _next_work_title calls
    # _title_clause, so the status module must exist first): the --status
    # snapshot + pending projection — the STATUS_MD markers, _gate_facts/
    # _spine_counts, the open-item one-liners, the blocked/spine/pause pending
    # sources, pending_block/status_block, the Ready-frontier lines and
    # _splice_status/run_status — moved verbatim to traj_status.py (508 lines,
    # under THRESHOLD; the facade docstring gains the sibling clause, +3); main's --status arm calls traj_status.run_status.
    # Ratcheted DOWN.
    # -969 (1911 -> 942), WI-280 S6: the Knowledge / Process / Next-work panels
    # — know_graph + the type-tiered know_view/_know_panel, the Process tab
    # (lifecycle x gates, the resume loop, the SR-055 working-loop hoops), and
    # the landing-hero Next-work card — moved verbatim to traj_panels.py (1016
    # lines, under THRESHOLD). What remains here IS the facade: the docstring,
    # the guarded ct import + sibling re-exports, OUT_HTML/ASOF_RE,
    # HTML_TEMPLATE, build_html and main. ENTRY RETIRES: 942 is under
    # THRESHOLD, so per the module rule the baseline is deleted rather than
    # re-stamped — the H-2 monolith this ratchet froze is decomposed.
    # (Round-1 review correction: this entry first read 941/-970; the ratchet's
    # own metric, len(text.splitlines()), measures 942 at that commit.)
    #
    # (agent_dispatch.py and its whole bump history retired with the module
    # at concurrency-restructure Phase 5 - the dispatcher deleted wholesale;
    # the surviving integrator is integrate.py, below this threshold.)
    # +30 (3042 -> 3072), WI-345: `fresh_verdict_path`, `read_verdict` and
    # `launcher_exe` — the managed-session verdict plumbing and the launcher
    # probe, each stated once instead of once per arm. Extraction-grows-the-file
    # again, and here it also BOUGHT complexity: route_session dropped 13 -> 11
    # (re-stamped below). The docstrings carry the reasons the duplicates had
    # lost — the pre-plant rule (repo-review 2026-07-21 M-22) existed in the
    # review arm only, so the critique arm's `unlink` read as a stray line.
    # Reviewed bump, log 2026-07-28.
    # +4 (3072 -> 3076), concurrency-restructure Phase 2c-i: the one-word
    # re-point of the §7 continuation re-check from `schedule.load_rows` to
    # `schedule.load_registry_rows` (the dual-read resolution), plus the three
    # comment lines saying WHY — reading the CSV directly answers EMPTY in a
    # folder-registry tree, which would silently disarm the re-check rather
    # than fail it. The code delta is one identifier. Reviewed bump; the whole
    # entry re-stamps with WI-280.
    # +1 (3076 -> 3077), Phase 3 (§5.1): the worker-prompt rule redirects a
    # branch's session record to a docs/log.d/ fragment and drops the stale
    # work-items.csv mention carried since Phase 2c. Reviewed bump,
    # log 2026-07-29. Re-stamp down with WI-280.
    # -69 (3077 -> 3008), Phase 5 item 1 (2026-07-29): the dispatcher's
    # presence in THIS file leaves with agent_dispatch.py — the ~45-line
    # re-export block, the --jobs/--worker-iterations/--poll-seconds args, and
    # the plain-launch dispatch_run branch (now a refusal naming
    # `integrate.py claim`). Ratcheted DOWN; the deeper item-2 shrink
    # (WORKER_PROMPT re-grounding, --train) re-stamps again when it lands.
    # -3 (3008 -> 3005), Phase 5 C2 (2026-07-29): the dual-plan flag path's two
    # _write_runstate calls left with docs/run-state (stop banner + exit code
    # carry the outcome). Ratcheted DOWN.
    # -6 (3005 -> 2999), Phase 5 item 2/C3 (2026-07-29): the shrink-in-place
    # re-grounding — module docstring rewritten onto the §2.3 claim model,
    # WORKER_PROMPT loses its Train:/Base: trailers and llm/train naming,
    # --train becomes the optional session tag defaulting to the current
    # branch name (flattened), TRAIN_BRANCH_PREFIX re-export gone. Ratcheted
    # DOWN.
    # +7 (2999 -> 3006), Phase 5 item 3/C4 (2026-07-29): build_scope_srs and
    # critique_control re-point from direct-CSV reads (empty in the folder
    # tree — the silent-disarm defect found at C1's census classification)
    # through load_wi_registry; the bump is the docstring recording the
    # defect. Reviewed bump.
    # +20 (3006 -> 3026), WI-374: the plain-launch DRIVE mode — the loop body
    # lives in the new sibling drive.py (deliberately NOT here: this module is
    # a named H-2 decomposition target); the bump is the delegation
    # (_drive_entry), the docstring re-grounding (plain launch drives instead
    # of refusing), and _coordinator_lock — the acquire/report/register
    # sequence extracted to ONE home so the two lock sites cannot drift.
    # Reviewed bump, log 2026-07-31.
    # -53 (3026 -> 2973), WI-383: session grouping REMOVED rather than wired
    # (docs/concurrency-v2.md §A6.1) — the §7 continuation re-check, the
    # `exit 10 ASSIGNMENT-END` arm, the worker's `sched` scheduler view and the
    # `schedule` import all go with it. The only multi-WI assignment left is the
    # spine batch the dispatcher admits, whose constituents are homogeneous by
    # construction: the one case the guard never refused. Ratcheted DOWN.
    # +12 (2973 -> 2985), WI-381: the plain launch's entry follows the rename
    # — `_drive_entry` imports the sibling as `dispatch` (drive.py ->
    # dispatch.py, lane.py extracted; docs/concurrency-v2.md §A4.2) — and the
    # `--lanes` flag joins the argparse surface (the §A4.3 dial's CLI rung).
    # Reviewed bump, log fragment 2026-08-02 (WI-381). Re-stamp down with
    # WI-280.
    # +22 (2985 -> 3007), WI-388: the worker prompt's Context block (consumer
    # 2 of intake.context_block) — computed fresh at claim, advisory, one new
    # instruction line; the lazy import keeps a stripped copy launchable.
    # Reviewed bump, log fragment 2026-08-02 (WI-388). Re-stamp down with
    # WI-280.
    # +7 (3007 -> 3014), SN-028: the four policy dials re-pointed at
    # `declared_policy` plus the three re-exports the sibling modules read.
    # Reviewed bump. Then -85 (3014 -> 2929), plan §8: the WORKER / REVIEWER /
    # CRITIQUE prompt constants left this module for
    # `project-trajectory/prompts/*.template.md`, loaded through prompts.py.
    # A RE-STAMP DOWN, which this ratchet requires in the same commit — the
    # assertion fires on shrink too, exactly so a monolith cannot quietly keep
    # a generous ceiling after the work that earned it moved out. What is left
    # here is the lazy loader and its cache; the prose is a diff away.
    # Then +3 (2929 -> 2932), SN-028 REVIEW round 1: the operator-facing
    # banner strings named files that no longer exist.
    # Then +14 (2932 -> 2946), SN-029: the mode words the loop compared against
    # ("attended", "single-ratify") are no longer a vocabulary — the loop asks
    # `human_holds` for the LEVEL and `keep_nondependent` for the orthogonal
    # drain policy, computed once in `main` and carried on the context rather
    # than re-derived at each of the five sites that used to string-compare.
    # Reviewed bump.
    # Then +75 (2946 -> 3021), SN-026/SN-032: the ADJUDICATE routing phase (its
    # own `route_intent` arm — cross-family like the reviewers, tier pinned by
    # the row's measured estimate, deliberately deaf to the implementer's
    # escalation overrides), `adjudicating` + `row_routing` (the row's two
    # routing facts, extracted rather than inlined — which took `route_session`
    # BELOW the complexity limit and deleted its baseline entry), and
    # `prompt_source` for the telemetry. Reviewed bump; the counterweight is
    # that the same slice DROPPED two complexity baselines.
    # Then -1 (3021 -> 3020), the same slice: `ruff format`'s reflow
    # after the SN-028..032 edits (the `format` step is advisory at this gate but
    # the tree is kept formatted anyway). Mechanical; no behaviour moved.
    # +12 (3020 -> 3032), D-5 step 2d: the sibling-import guard and the two SR/TC
    # reads moving to spine_carrier.load. Pure plumbing; no behaviour change.
    # +48 (3032 -> 3080), WI-424: `session_body` — the ADJUDICATE-or-assignment
    # fork BOTH routing arms take, extracted rather than inlined twice so the
    # refusal-and-fall-back rule has one home, and shaped so `route_session`
    # keeps its single call and stays off the complexity baseline. The
    # assemblers themselves are a new module (`adjudicate_brief.py`), which is
    # why this is 48 lines and not 250. Reviewed bump.
    # Then +78 (3080 -> 3158), WI-424 review round 2 (B3 + M5): the fail-CLOSED
    # hold for a declared brief the kit cannot compose (an adjudication row must
    # never dispatch as a builder), and `adjudication_bookkeeping` — the
    # validation arm proving the session RULED rather than merely committed.
    # The arm is its own function precisely so `session_bookkeeping`, already at
    # complexity 31, gains no branch: its guard sits inside the callee.
    # WI-432 (the six check toggles fold into process.toml): +2 (3158 -> 3160).
    # `live-status` is the ONE of the six read through the coordinator layer, so
    # it costs a `declared_policy` swap and the comment saying why — no local
    # reader here, which is the whole point of the F5 split recorded below.
    # WI-433 (the blackout ships DISABLED): +2 (3160 -> 3162). Two lines of the
    # module docstring's dial description — the scaffold's shipped value changed
    # and the sentence that stated it had to change with it, or the docstring
    # would assert a default the template no longer carries.
    "agent_loop.py": 3162,
    # +30 (2206 -> 2236), WI-065: `tc_citation_findings` — the TC-`Verifies`
    # rules lifted out of `analyze` so the cell could accept `IF-###` seam ids.
    # Most of the bump is that helper's docstring, which is where the RULING now
    # lives (one citation cell, not a second column) — the part a successor
    # would otherwise have to reconstruct from two disagreeing checkers. The
    # extraction also ratcheted `analyze`'s complexity DOWN 53 -> 50. Reviewed
    # bump, log 2026-07-25. Re-stamp downward with WI-280.
    # +381 (2236 -> 2617; the last +38 is the adversarial-review fix pass: F1 --since fail-fast, F4 BOM strip, F7 resolved-sha provenance, F8 ownerless-child warns), WI-316: the re-attestation brief (--ratify modified)
    # — per-cell before/after for every Modified SR's chain against its
    # git-derived attested baseline (+ --since), the is_modified predicate, and
    # the two warn-tier lints (Modified-exempt status advisory; the
    # modified-chain orphaned-child warn). The brief is the sitting's
    # instrument — a sitting cannot bless a delta it cannot see — and rides the
    # existing --ratify generator mode rather than a new surface. New
    # capability, not monolith drift; the largest WI-316 bump and a named
    # WI-280 decomposition candidate (the reattest emitter is an extractable
    # unit). Reviewed bump, log 2026-07-26. Re-stamp downward with WI-280.
    # +91 (2617 -> 2708), WI-322: reattest_model is SPLIT OUT of reattest_lines
    # so one computation feeds two renderers — the markdown brief here and the
    # generated open-items.html. The alternative was a second copy of the git
    # archaeology in the new module, which is the paraphrase-not-decompose
    # failure the kit preaches against. Markdown output proven byte-identical
    # across the refactor. Reviewed bump, log 2026-07-26.
    # +70 (2708 -> 2778), WI-321: the stand-alone-requirement lint
    # (`standalone_sr_advisories`) plus its OWN advisory pipe — report section,
    # console line, summary counter — rather than folding it into the AC pipe,
    # whose `ac-advisories` counter would then be naming a finding that is not
    # one. Paid for partly in place: the five per-pipe console loops collapsed
    # into one over their ordered concatenation, which also kept
    # `render_console` off the complexity ratchet. Reviewed bump, log
    # 2026-07-26. Re-stamp downward with WI-280.
    # +29 (2778 -> 2807), WI-327: the stand-alone rule widened from the SR to the
    # whole spine and promoted from advisory to a gating finding — a shared
    # PROVENANCE_COLS table, one loop over three registries, and the docstring
    # recording WHY the SR-only scope was wrong (26 LLR + 8 TC + 9 SR cells the
    # rule could not see, still growing while it was green). Reviewed bump, log
    # 2026-07-27. Re-stamp downward with WI-280.
    # +5 (2807 -> 2812), WI-328: the LLR gains a `Rationale` column. One data line
    # (the SR's `Rationale` joins REQUIRED_FIELDS — every row already carries one,
    # so it guards zero-to-zero) and four comment lines recording why the LLR's
    # stays OPTIONAL while the SR's does not: a short decomposition row's why IS
    # its parent SR's, so requiring one everywhere manufactures the restatement the
    # column exists to prevent. That asymmetry is exactly what a successor would
    # re-litigate from the code alone. Reviewed bump, log 2026-07-27.
    # +196 (2812 -> 3008), WI-328: the requirement-FORM tier (six gating rules)
    # and the paraphrase advisory, beside the stand-alone rule they complete —
    # all three answer "is this row readable and decidable on its own", and
    # splitting them across modules would make a reader check two places for
    # one answer. REVIEWED BUMP, and the largest single one this module has
    # taken: the honest fix is the WI-280 extraction of the whole spine-row
    # TEXT concern into a sibling (the agent_common/plan_runner precedent),
    # which is filed rather than done inline because it moves the scaffold
    # surface (bootstrap MAPPING, README kit-contents, test file lists) and
    # this WI lands inside an open attestation window. Log 2026-07-27.
    # -323 (3026 -> 2703), WI-329: the debt above is PAID. The four pure text
    # predicates and the row primitives they share moved to trace_text.py, which
    # stays under THRESHOLD and needs no entry of its own. This is the escape the
    # ratchet documents and prefers — decomposition, not a bump — and it lands
    # 109 lines BELOW the pre-WI-328 baseline of 2812, so the census tightens
    # rather than merely stops growing. Proven behaviour-preserving by the three
    # golden files staying byte-identical.
    # +3 (2703 -> 2706), WI-348: three report writers take the two-line LF form.
    # +142 (2706 -> 2848), WI-325: the re-attestation brief gets the freshness
    # gate every other generated surface here already had. Most of the bump is
    # the docstring on `ratify_check`, which records the constraint that makes
    # this different from its siblings: the brief SELF-STAMPS its baseline, so
    # the compare must reuse the one the FILE declares and must not re-derive —
    # re-deriving is the WI-322 BLOCKER, where a regeneration collapsed 43
    # chain-row diffs to 18 while --check certified the loss. A successor who
    # "simplifies" that comment away removes the reason the code is shaped this
    # way. Reviewed bump, log 2026-07-28. Re-stamp downward with WI-280.
    # +9 (2847 -> 2856), WI-347: `_full_row_bullets` — the whole-row renderer the
    # re-attestation brief used identically in its no-baseline and added-row arms.
    # Same extraction-grows-the-file shape as bootstrap.py above. Reviewed bump,
    # log 2026-07-28.
    # +39 (2856 -> 2895), WI-364 (owner-ruled error tier 2026-07-29): the
    # LLR-cites-superseded-SR integrity rule (`_llr_supersession_findings`) and
    # the contract docstring stating the TC carve-out, plus the adversarial
    # review's three refinements (dedupe a repeated cite, never name a
    # nonexistent successor, the Draft-not-exempt statement). The shipped
    # guard the ruling asked for, not monolith drift. Reviewed bump,
    # log 2026-07-29. Re-stamp down with WI-280.
    # +14 (2895 -> 2909), WI-401: `sn_cited_ids` — the SN-Refs coverage parse
    # named so the SN-coverage gate rung's F5 duplicate in derive_gate.py has a
    # pinnable twin (test_rule_sync), plus the two seam comments tying the
    # orphan listing to the gate rung. Reviewed bump, log 2026-08-02.
    # +10 (2909 -> 2919), WI-402: phase_ratified_findings tightens to
    # numeric-only (owner ruling 2026-08-01) — the docstring now records WHY
    # (the two literal joins a prefixed cell silently disarms, and the
    # grandfathering stance that keeps phase_num digit-extract), which is the
    # reason a successor must not "simplify" the rule back to the parse.
    # Reviewed bump, log 2026-08-02.
    # +11 (2919 -> 2930), WI-408 (WI-401 REVIEW-A finding 2): sn_all_ids — the
    # SN id-universe scrape, previously an inline one-liner duplicated in
    # derive_gate.py with NO test_rule_sync pin, extracted to a named twin so
    # the third SN policy duplicate is pinned like its siblings. The growth is
    # the docstring recording the whole-text sharp edge (a ratified prose
    # mention caps the gate at G0). Reviewed bump, log 2026-08-02.
    # +44 (2930 -> 2974), SN-029: `docs/requirements/attestations.csv` joins the
    # registry schema (loader row + column contract) so the ledger the
    # attestation rungs read is traced like every other spine registry rather
    # than being a file only one checker knows about. Reviewed bump.
    # Then +20 (2974 -> 2994), SN-029 REVIEW round 1: `_resolvable` guards the
    # ledger-first baseline. An `AcceptedCommit` git cannot resolve (a rebase
    # or squash rewrote the sha, a shallow clone, the off-git placeholder) made
    # `_rows_at` answer {} — so every current row classified as `added` and the
    # brief said "everything here is new", with `no_baseline_reason` EMPTY, so
    # the honest degrade written for exactly this case never rendered.
    # Reviewed bump.
    # Then -51 (2994 -> 2943), D-1 REMOVAL HALF (docs/repo-lock.md, owner ruling
    # 2026-08-09): `_ledger_baseline` and the `_resolvable` guard above go with
    # `attestations.csv`, and `_attested_baseline` is once again the git
    # derivation alone. Re-stamped DOWNWARD in the same commit, per this file's
    # own rule — a shrink is re-stamped, never left standing as headroom.
    # Then +34 (2943 -> 2977), the SN shape fix (2026-08-09): `_sn_prose` gains
    # the duplicated `_sn_fields` helper, which resolves an SN row's four prose
    # fields BY TABLE SHAPE instead of at fixed Core-needs offsets. All ten
    # Edge-case rows had been publishing their Lifecycle word as the need
    # (SN-013 rendered "Provision") with an always-empty acceptance, in the
    # ratify sitting brief this module builds — the surface a human reads
    # BEFORE ratifying. The helper is verbatim in traj_parse and gen_okf too
    # (F5; a shared module was rejected 2026-07-12), censused as
    # `markdown-table` 11 -> 13, and pinned by value in test_rule_sync.
    # Reviewed bump: the growth is a named rule replacing an inline one, not
    # new responsibility.
    # Then +245 (2977 -> 3222), the ID WATERMARK (2026-08-09): live_max_ids,
    # read_watermark, watermark_findings, render_watermark, bump_watermark,
    # committed_watermark and their --bump-ids wiring. Reviewed bump, and this
    # is the home ON PURPOSE: the two rules are integrity-class, and trace.py's
    # `--strict-integrity` pass is the only always-on floor the pre-commit hook
    # runs at every gate. In check_trajectory they would sit behind
    # `docs/trajectory-check: off`; as a G3 step they would never run in a G1
    # repo like this one. Note the check is appended in main(), NOT in
    # analyze() — that function's contract is "Pure … No I/O" and it stays true.
    # 3222 -> 3248 in the same reviewed bump: the complexity ratchet refused
    # `live_max_ids` at 18 ("simplify these, do not bump"), so it decomposed into
    # four small readers (_csv_ids / _sn_ids / _wi_ids / _dp_ids) and `--bump-ids`
    # moved out of main() into _cmd_bump_ids. More LINES, less complexity — which
    # is the trade this pair of ratchets exists to force.
    # Then +87 (3248 -> 3335), the ADVERSARIAL REVIEW of the watermark
    # (2026-08-09). Two BLOCKERs and three MAJORs, all fail-open, all fixed
    # here: `bump_watermark` caught read_watermark's refusal and rebuilt the
    # file from the live max — the documented remediation DESTROYED the record;
    # monotonicity read `HEAD:` only, so a merge resolved `--ours` silently
    # dropped the other branch's marks; nothing bounded a mark UPWARD, so one
    # edited digit retired a space's guard forever; `_csv_ids` took the first
    # id-SHAPED cell rather than the id COLUMN, hiding a row's own id behind a
    # reference column (and crashing on a ragged row, since surplus cells land
    # under DictReader's `None` key as a list). `watermark_findings` split into
    # `_mark_covers_live_findings` + `_mark_history_findings` because the
    # complexity ratchet refused it at 11 — decompose, do not bump.
    # Then +10 (3335 -> 3345), the watermark advisory's MISLABEL: the
    # "monotonicity NOT checked" notice was appended to `findings.advisories`,
    # the ACCEPTANCE-CRITERIA lint's pipe — so every repo without a committed
    # mark reported `ac-advisories=1` about a row whose AcceptanceCriteria was
    # fine, and printed a watermark message under a heading about acceptance
    # criteria. The comment where `advisories` is built already forbade exactly
    # this ("a shared count would say ac-advisories about a finding that is not
    # one"). Its own pipe + counter, per that rule.
    # Then +131 (3345 -> 3476), D-5 step 1 (docs/repo-lock.md, owner ruling
    # 2026-08-10): the CARRIER-AWARE BASELINE READ. `_rows_at` resolves the
    # carrier a revision actually used — TOML first, CSV as the fallback —
    # because the spine is moving to TOML and a read that knows only the live
    # carrier gets None back at every pre-migration revision, which this
    # function's own contract turns into "nothing existed = an empty baseline".
    # All 25 Modified rows would render as "awaiting its FIRST ratification" and
    # be re-blessed with NO diff, silently. D-5 flags it as the one thing that
    # must not be forgotten, and this is the module where forgetting it lands.
    # REVIEWED BUMP, not monolith drift, and the split is worth stating: ~57
    # lines are the two F5 constants (SPINE_TABLE + SPINE_COLUMN, pinned equal
    # to check_trajectory's copies and to migrate_carrier's writer by
    # test_rule_sync), ~50 are docstring recording WHY the resolution order and
    # the None-vs-{} distinction are load-bearing, and the executable delta is
    # ~24 lines. Decompose-don't-bump does not apply: the alternative is a
    # shared module, which is the _kitcommon shape the F5 ruling rejected at
    # WI-078. Re-stamp downward with WI-280, and again once the CSV fallback
    # can be dropped — it is dead weight the day no supported baseline predates
    # the cutover, and it should not outlive its reason.
    # Then -86 (3476 -> 3390), D-5 step 2: the vocabulary and both readers moved
    # to the `spine_carrier.py` sibling (OWNER RULING 2026-08-10, repo-lock D-6,
    # amending the F5 rejection of a shared module). Most of the bump above was
    # the stated key map and the docstring justifying it; both now have ONE
    # home, and this module keeps only the git shell and the `-000` filter,
    # which is its own rule and not the carrier's. Net against pre-D-5: +47.
    # Then +14 (3390 -> 3404), D-5 step 2d: the SN tier joins the carrier.
    # `sn_draft_ids` dispatches on which carrier wrote the text (a heading scan
    # over TOML finds no headings, reports ZERO drafts, and FLOATS the gate) and
    # `_sn_prose` drops its copy of the edge-case fold. The fold's other two
    # copies went with it, in traj_parse and gen_okf.
    # Then +35 (3404 -> 3439), D-5 step 3 (the CUTOVER): `_attested_baseline`'s
    # git-log pathspec names BOTH carriers — without it the log of a registry
    # that changed carrier has no `Verified` revision in it and all 25 amended
    # rows render "no attested baseline", the exact fail-open step 1 exists to
    # prevent, reached by a second door; `_sn_ids` reads the need tier through
    # the carrier instead of a markdown-row regex that matches nothing under
    # TOML; and both needs-file reads resolve the carrier rather than testing
    # one suffix for existence.
    # Then -38 (3439 -> 3401), WI-422 (the measured dead-symbol sweep): the orphaned `_sn_fields` copy. D-5 step 2d collapsed the drifting
    # triplet onto `spine_carrier.folded`, but the three copies were left
    # behind with no caller; this is the residue, not a behaviour change.
    # Then +27 (3401 -> 3428), the ADVERSARIAL REVIEW of the carrier cutover,
    # BLOCKER 1 — the ELEVENTH UNWIRED READER, and a live false green.
    # `live_max_ids` swept `docs/requirements/*.csv` + `docs/test/*.csv` by
    # LOCATION, so D-5 moved SR/LLR/TC out from under it and rule 2 of the
    # watermark ("no live id exceeds its mark") went VACUOUS on three of the four
    # spine tiers — the tiers with NO minter, where that rule is the only guard
    # there is. It was not theoretical: LLR-167 and TC-161 were minted after the
    # cutover and stood above their marks with zero findings reported. The new
    # `_spine_ids` reads through `spine_carrier` (resolve whichever carrier is
    # live) rather than assuming a suffix, so moving a file cannot un-wire the
    # scan again. Twenty of the 27 lines are the docstring recording that
    # failure mode — the executable delta is ~7. Not decomposable: this IS the
    # decomposition, one reader per id source beside `_csv_ids`/`_sn_ids`/
    # `_wi_ids`/`_dp_ids`.
    # Then +21 (3428 -> 3449), 2026-08-12: THE SAME HOLE, ONE CARRIER BATCH
    # LATER. Batch-2 (WI-431) moved `open-items` off CSV, so `_csv_ids`' glob
    # stopped matching it and the watermark went vacuous for the `OI` space
    # too — found the way the last one was, by minting past the mark and
    # getting NO finding (OI-26 live against a mark of 14, `--strict` silent).
    # `_offspine_ids` reads through `spine_carrier` for the same reason. Again
    # mostly docstring: the executable delta is ~6. Not decomposable, for the
    # reason directly above — this IS the decomposition. THE PATTERN IS NOW
    # TWICE-OBSERVED AND WORTH NAMING: every carrier move silently un-wires
    # whichever id scan globbed the old suffix, and nothing generic catches it
    # (a scan that finds no registry reads zero rather than refusing). A third
    # occurrence should build that guard instead of adding a fourth reader.
    "trace.py": 3678,  # +221 2026-08-13: WI-443 — the IF/CMP schema tier (required fields, closed vocabularies), the four IF Contract negative rules, and the untagged-endpoint classifier, all warn-first; +8 the adversarial round's refutation recorded in schema_advisories' docstring (reviewed bumps, reasons in the log)
    # +132 (1926 -> 2058; the last +10 is the F4 BOM hardening: read_rows utf-8-sig + git-show strips), WI-316: staged_spine_findings — the amend-without-
    # flip warn (--staged): content cells of a Verified spine row changed
    # without the Modified marker, suppressed when the owning SR flips in the
    # same commit (the attestation unit). The write-time discipline the
    # RE-ATTESTATION-PENDING prose convention never had. Reviewed bump, log
    # 2026-07-26. Re-stamp downward with WI-280.
    # +5 (2058 -> 2063), WI-322: ratify_brief_findings reads open-items ROWS
    # instead of parsing markdown sections. Reviewed bump, log 2026-07-26.
    # +72 (2063 -> 2135), WI-349: cell_integrity_errors — the physical-line rule
    # `staged_findings` has documented in its own docstring since it was written
    # and nothing enforced. It belongs HERE and not in a sibling: it is checked on
    # the raw rows this module already reads, and it exists only because THIS
    # module's staged-close scan compares HEAD line-wise, so moving it away would
    # separate a rule from the single assumption it protects. About two thirds of
    # the bump is the docstring recording the 2026-07-28 demonstration and why it
    # is an error rather than a warn. Reviewed bump, log 2026-07-28. Re-stamp
    # downward with WI-280 — and note this module has now taken four upward bumps
    # in a row with no decomposition between them, which is a cost the WI-280
    # deferral is quietly accruing rather than an argument that each bump was
    # wrong.
    # +360 (2135 -> 2495), WI-352 + WI-344 + the WI-349 rework, in one slice
    # because they are one file and each forced the next. The reconciler itself
    # is ~200 lines of which most is the docstring recording WHY the done side is
    # scoped to live specs (measured: 38 unactionable findings over the archive)
    # and why the trailer signal never gates. WI-344's extractions REMOVED code
    # from three functions and dropped two below the C901 limit; the net is still
    # +360 because the new check is new behaviour.
    #
    # THE ARGUMENT AGAINST EXTRACTING, since WI-349's entry said the next
    # addition should have to make one: a new sibling module is a SCAFFOLD-SURFACE
    # change (bootstrap MAPPING, README kit-contents, test_bootstrap file lists,
    # the dogfood-sync structural lock), which is why WI-328's spec deferred the
    # same move; the reconciler also reads this module's own registry loader,
    # OPEN_STATUSES, spec-lifecycle constants and `_git`, so the seam is not free.
    # That is a reason to schedule it, not a reason it is fine: this is now the
    # FIFTH consecutive upward bump on this module with no decomposition between
    # them, and check_trajectory.py is hereby the concrete next slice of WI-280 —
    # named with its measured number rather than left as a general intention.
    # +93 (2497 -> 2590), WI-354: R-E resolved only the PATH half of a
    # `doc#anchor` SpecRef, so a row could cite a heading that does not exist and
    # read as traceable (WI-326 did, for two days). The anchor half plus the
    # near-miss reporter is the new behaviour; the rule itself was EXTRACTED to
    # `specref_findings` rather than folded in line, which put `ssot_findings`
    # back under the C901 limit instead of buying another complexity baseline —
    # so the growth is new behaviour, not accreted branching.
    #
    # +23 (2590 -> 2613), WI-354 follow-up: 131-REVIEW-A's BLOCKER 1 — a bare
    # `#anchor` SpecRef, and one naming a DIRECTORY, both resolved CLEAN because
    # the rule returned early on an empty path and trusted `exists()`. Two
    # findings and their reasons; the corrected `nearest_anchor` rationale is the
    # rest.
    #
    # THE TREND, stated so it is re-derivable rather than counted by hand. Every
    # recorded baseline for this module, in order:
    #   1926 -> 2048 -> 2058 -> 2063 -> 2135 -> 2495 -> 2497 -> 2590 -> 2613
    # That is the EIGHTH increase, +687 total, mean +86 per increase. Two
    # corrections 131-REVIEW-A forced, both worth keeping: the entry above said
    # "FIFTH" because the 2495 -> 2497 step was never given a transition comment
    # (it was a review fix), so the count silently skipped one — and "roughly +90
    # per slice" was unsupportable because "slice" was never defined, with the
    # per-slice mean landing anywhere from 95 to 133 depending on how the two
    # WI-316 commits and the +2 are grouped. The unit here is now the one thing
    # that is unambiguous and countable from this list: a BASELINE INCREASE.
    #
    # The trend is the argument, not the individual bumps: each entry above
    # justifies itself and the module is still 2590 lines of SHIPPED surface
    # (bootstrap MAPPING -> every adopting repo, run by the shipped pre-commit
    # hook). WI-280 already names this module as its concrete next slice; what
    # this entry adds is the compounding rate to weigh against the
    # scaffold-surface change a real extraction costs. Reviewed bump, log
    # 2026-07-28.
    #
    # +435 (2613 -> 3048), Phase 2b of the concurrency restructure: the registry
    # gains a second HOME (docs/work/ spec files) and this module is the copy of
    # the reader that SPEAKS — it reports a malformed spec and refuses a tree
    # carrying both homes at once, where schedule.py and agent_common.py stay
    # silent. Three parts, none of them accreted branching:
    #   ~228  the F5-duplicated spec-folder reader, identical in all three
    #         scripts (see agent_common.py's entry below for why it is copied);
    #   ~110  the git plumbing the CSV's assumptions do not survive —
    #         `_head_spec_status_map` (status at HEAD from `ls-tree` PATHS, no
    #         blob read), `_spec_paths` / `_spec_row_times` (per-open-row
    #         staleness), `_staged_spec_registry` (close detection from a staged
    #         RENAME), and `_path_commit_time`'s row-history mode;
    #   the rest  is the rationale for each, including the measurement that
    #         `--follow` ALONE does not preserve a row's staleness clock across a
    #         status move — the flag the design note named, which turned out to
    #         need `--diff-filter=AM` beside it.
    # This is the module the previous entry named as WI-280's concrete next
    # slice, and this bump does not weaken that: it makes it larger and more
    # urgent. What it is not is drift — every line is the second registry home,
    # and the whole of it re-stamps DOWN at Phase 5 when the CSV home retires.
    # Reviewed bump; reason here and in the Phase 2b session record.
    # +15 (3048 -> 3063), Phase 2c-i: `spec_registry_dir` learns that a `-000`
    # EXAMPLE spec does not decide which registry home is authoritative — the
    # kit's own `-000` rule, applied to the folder home so `bootstrap` can
    # scaffold the exemplar ADDITIVE beside the CSV. Measured before writing it:
    # without the rule a fresh scaffold gets an empty registry AND a
    # two-registries-present error on its first check. Twelve of the fifteen
    # lines are the docstring recording that, and the whole verbatim block
    # re-stamps DOWN at Phase 5 with the CSV home. Reviewed bump.
    # +59 (3063 -> 3122), Phase 3 (§5.4): critique selection stops trusting the
    # serial-number filename convention (a next-number race under concurrency)
    # — `_critique_git_times` (one batched git log, measured 0.09 s vs 1.35 s
    # per-path on this repo) plus the git-time -> mtime -> name ladder and the
    # docstring stating both naming generations. Reviewed bump, log 2026-07-29.
    # Re-stamp down with WI-280.
    # -22 (3122 -> 3100), Phase 5 C2 (2026-07-29): run_state_findings (the
    # WI-115 stale-end-state warn) retired with docs/run-state — no writer, no
    # file, no staleness to warn about. Ratcheted DOWN; the CSV-plumbing
    # down-stamp still lands with Phase 5 item 3.
    # -51 (3100 -> 3049), Phase 5 item 3/C4 (2026-07-29): the CSV home's
    # plumbing — spec_registry_dir, the dual-read fallback, registry_cell_
    # errors' WI-home wiring, _wi_row_times' blame half, _staged_wi_registry's
    # line-diff half and the migration-commit CSV fallback. The Phase 2b/2c-i
    # bumps above are repaid. Ratcheted DOWN.
    # -10 (3049 -> 3039), Phase 5 item 3/C4 follow-through (2026-07-29): the
    # unreachable `status-vocab` and `blocked-ref` ssot rules retired —
    # status is the spec's directory (loader-refused if unknown) and blocked
    # is derived, so no row can reach either. Ratcheted DOWN.
    # +8 (3039 -> 3047), WI-271 retirement (owner ruling 2026-07-29, the
    # handoff-2026-07-28c §3 disposition): the un-defer trigger moved into
    # `staged_findings`'s docstring — docstring lines only, no code. Reviewed
    # bump, log 2026-07-29. Re-stamp down with WI-280.
    # +30 (3047 -> 3077), WI-362 narrowed (owner ruling 2026-07-29): warn-text +
    # docstring statement of the rename blind spot, no detection engineering;
    # +4 of it the review correction that points the hint at the WI's own
    # docs/work/ spec file — the SpecRef target can never clear the warn.
    # Re-stamp down with WI-280.
    # +21 (3077 -> 3098), WI-280 slice 11: `_render_surface_paths` watches the
    # WHOLE dashboard generator FAMILY (gen_trajectory.py + its `traj_*.py`
    # split siblings), not the facade alone. Required, not drift: after the
    # split every emitter lives in a sibling, so a facade-only surface would
    # have silently retired the render-critique-staleness warn — the check
    # would still run and always pass. Most of the delta is the two fallback
    # arms and the comment recording that. Reviewed bump, reason here and in
    # docs/log.d/WI-280-bounded-core-decomposition.md.
    # +93 (3098 -> 3191), WI-380: the §A5.1 ratified-vs-traced cell split — the
    # two declared classification tables (one per spine registry, both halves
    # named), `spine_cell_class` with the fail-safe residual, the extracted
    # `_split_changed_cells`, and the `staged_spine_amendments` seam WI-388
    # consumes. Most of the delta is the tables and the comment recording WHY
    # the residual falls to ratified (a new column may be too loud, never
    # silently un-ratified). The rule stays beside its only consumer for the
    # WI-349 reason — moving it to a sibling would separate a rule from the
    # single scan it governs. Reviewed bump, reason here and in
    # docs/log.d/WI-380-ratified-vs-traced-cell-split.md. Re-stamp down with
    # WI-280.
    # +39 (3191 -> 3230), WI-380 REVIEW-A round 1: the MAJOR was a false SHIPPED
    # contract (the module docstring still promised "content cells", the exact
    # phrase §A5 quotes as the defect) and the MINOR was a seam whose record was
    # consumable but whose scan was not callable at §A5.2's trunk-COMMIT
    # trigger. Both are corrections of what this row already shipped, not new
    # scope: `_spine_revs` + the `base`/`head` pair make the rev range
    # expressible (driven: post-commit the default returns [] and
    # `(root, "HEAD~1", "HEAD")` returns the record), and the rest is the
    # docstring truth-telling the review demanded. The extraction held the scan
    # at C901 20 — no complexity bump. Reviewed bump, reason here and in
    # docs/log.d/WI-380-ratified-vs-traced-cell-split.md. Re-stamp down with
    # WI-280.
    # +18 (3098 -> 3116), WI-384: the six-state model. The DELETION is real —
    # `parse_spec_status`'s disposition cross-check and both of its raise paths
    # are gone — and the growth is the vocabulary that replaced them: two more
    # SPEC_STATUS_DIRS rows, KNOWN_STATUSES exploded onto one line per status
    # by the formatter, and the comments recording WHY `draft/` must be a
    # DECLARED directory (id reservation) rather than a scratch folder. Net of
    # comments the module shrank. Reviewed bump, log 2026-08-01. Re-stamp down
    # with WI-280.
    # +3 (3116 -> 3119), WI-384 REVIEW-A round 1: the MAJOR finding. The ruled
    # reason for declaring `draft/` — that an undeclared folder is invisible to
    # `max(id) + 1` — was driven and REFUTED (the mint reads filenames through
    # an unfiltered walk and sees it either way), so the F5 block comment now
    # states what is actually blind: the duplicate-id guard and the dashboard.
    # Three COMMENT lines, zero code tokens; correcting a false rationale in
    # place is cheaper than letting it ship. Reviewed bump, log 2026-08-01.
    # +21 net (3230 -> 3251), WI-384 merging trunk `8c4d5f78`: NOT a new bump
    # and not a side picked. WI-380 and WI-384 re-stamped this module from the
    # same base 3098 on parallel branches — 3230 and 3119 — and the merge
    # conflicted here. Resolved by RE-MEASURING the merged file with the
    # census's own metric (`len(text.splitlines())` = 3251), which is exactly
    # 3098 + WI-380's +132 + WI-384's +21: the two changes are disjoint, so
    # the arithmetic is a check on the resolution rather than a coincidence.
    # Both reason chains above are preserved verbatim; neither WI's record
    # was dropped to make the number fit. Re-stamp down with WI-280.
    # +10 (3251 -> 3261), WI-387: the `## Handback` section joins the spec body
    # grammar in this F5 copy — identical text to the other two by construction
    # (tests/test_wi_loader_sync.py). Reviewed bump, log 2026-08-01.
    # +98 (3261 -> 3359), WI-399: the knowledge⇒component containment rule
    # gains its EARLY firing point (`shipped_modules`/`added_module_findings`) —
    # the shipped-module delta a work branch can see without the trunk-owned
    # arch-map regeneration (SR-133), so a lane that adds a module reds its own
    # bar, not the station's. The rule belongs beside its siblings in
    # `component_findings` (one containment home, the F5 stance) rather than in
    # a new module that would itself owe registration; the stack.ini reads
    # collapsed onto one `_stack_ini_get` (shrinking `_tests_dir` and killing a
    # sanctioned dupe block), and roughly half the remaining bump is the
    # mechanism comment recording WHY the firing point moved (WI-374/WI-387,
    # twice-driven). Reviewed bump, log fragment docs/log.d 2026-08-02; re-stamp
    # down with WI-280.
    # +69 (3359 -> 3428), WI-399 rework (REVIEW-A finding 1): the delta now
    # mirrors build_map's symbol-emptiness skip (`_would_be_inventoried` +
    # `_has_internal_import`) — without it a bare `__init__.py` or comment-only
    # module redded --strict FOREVER (the regeneration skips it from the map, so
    # the delta could never empty: accidental new policy). Files mode returns
    # empty by design (finding 2 — a real files-mode map has no module headers,
    # the whole family is dormant there), and an absolute [paths] src scans the
    # path it names (finding 3). Drift-pinned by the differential tests that run
    # the real generator. Reviewed bump; re-stamp down with WI-280.
    # +25 (3428 -> 3453), WI-388: the `Bar` loader-table column + the
    # `## Context` body-grammar clip (both F5-mirrored edits), and the two
    # unclassified-cell RULINGS recorded at the §A5.1 split's home (LLR
    # `SR-Refs` -> traced/routed, SR `SupersededBy` -> ratified confirmed) —
    # most of the bump is that recorded reasoning. Reviewed bump, log fragment
    # 2026-08-02 (WI-388). Re-stamp down with WI-280.
    # +78 (3453 -> 3531), WI-388 consumer 3: the pack-citation warn
    # (`knowledge_pack_findings` + `_declared_packs` + `_spec_text_for`) —
    # warn-ONLY, the LLR.Component -> CMP.Knowledge join re-derived under this
    # module's F5 independence (the shipped hook imports no sibling).
    # Reviewed bump, log fragment 2026-08-02 (WI-388). Re-stamp down with
    # WI-280.
    # Then +22 (3531 -> 3553), SN-031: `partial` joins the status/terminal vocabularies and the
    # `Supersedes` column joins the F5-copied schema. Reviewed bump.
    # Then +272 (3553 -> 3825), SN-029: the attestation LEDGER's three rungs —
    # `attestation_findings` (the DRIFT rung: a Verified row whose normative
    # text no longer digests to what was accepted), `attestation_integrity_
    # findings` (the ledger's own shape), `staged_attestation_rewrite_findings`
    # (append-only) — plus `normative_text`/`sn_normative_text`/`digest` and the
    # excluded-column contract that says WHICH cells are normative. This is the
    # biggest single bump the module has taken and it buys the anchor the whole
    # ordinal rests on: without a recorded digest, "has this been ratified" is
    # re-derived from git history at every read. Reviewed bump; this module is
    # now the kit's largest and is the first WI-280 decomposition candidate.
    # Then +5 (3825 -> 3830), same slice: the ledger's errors are held in their
    # OWN local and folded in at both exits, because the rung runs BEFORE the
    # WI-vacuity return (a corrupt ledger in a repo with no work items must
    # still fail) and `errors` is not bound until after it.
    # Then +146 (3830 -> 3976), SN-029 REVIEW round 1 + SN-030 rung 3. The
    # review's three ledger holes: a `git rm`/`git mv` of the ledger returned
    # CLEAN from all three rungs at once (the strongest form of rewriting was
    # the one form the guard could not see — now an explicit removal finding,
    # with `--no-renames` so a move shows its old path), a ledger row keyed on
    # an id that is not a current spine row anchored NOTHING while reading as a
    # clean ledger (the ghost anchor, with `superseded` added to the decision
    # vocabulary as the way to retire one without deleting a row), and the
    # `--staged` arm skipped the integrity rung at the one moment it is cheap
    # to fix. Plus `queue_conflict_findings` (SN-030's mechanical
    # queue-conflict pre-filter — warn-only, never the exit code). Reviewed
    # bump; this module remains the first WI-280 decomposition candidate.
    # Then -1 (3976 -> 3975), the same slice: `ruff format`'s reflow
    # after the SN-028..032 edits (the `format` step is advisory at this gate but
    # the tree is kept formatted anyway). Mechanical; no behaviour moved.
    # Then +16 (3975 -> 3991), same pass: `_clip_title` bounds the
    # queue-conflict finding text. A WI title here is routinely a
    # multi-thousand-character paragraph, so interpolating two raw ones
    # produced a ~6 KB stderr line per pair — a warn nobody can read is a warn
    # that does not exist. The duplicated open-status set folded into the
    # module's existing `OPEN_STATUSES` in the same pass (WI-347).
    # Then -193 (3991 -> 3798), D-1 REMOVAL HALF (docs/repo-lock.md, owner ruling
    # 2026-08-09): the ledger's three rungs and their readers are DELETED —
    # `attestation_findings`, `attestation_integrity_findings`,
    # `staged_attestation_rewrite_findings`, `read_attestations`,
    # `newest_attestations`, `_report_attestations`, the two constants and both
    # `main` wirings. The +272 bump above is the one being paid back, and this
    # is the honest reason it never should have been taken: the ledger held ZERO
    # real rows for its whole life. What is KEPT is the part that was right —
    # `normative_text`, `sn_normative_text`, `digest`, `current_digests` — which
    # the anchor half re-homes onto the artifact's own row. This module is still
    # the kit's largest and still the first WI-280 decomposition candidate;
    # -193 narrows the gap, it does not close it.
    # Then +89 (3798 -> 3887), D-5 step 1: the same carrier-aware read, on the
    # two-tree amendment scan this module owns (`_spine_rows_at`, `_spine_stem`,
    # `_spine_carriers` and the F5 constant pair). Smaller than trace.py's +131
    # because the ruling's argument is stated ONCE, beside trace.py's copy, and
    # pointed at from here — two copies of a RULING is how two copies start
    # disagreeing about it. It also REPLACES three hand-rolled `git show` +
    # csv.DictReader blocks with one call, which is why `staged_spine_amendments`
    # got simpler rather than larger (complexity 19 -> 18, re-stamped down in
    # tests/test_complexity_ratchet.py). The scan now compares CSV on the old
    # side to TOML on the new one across the cutover, so that commit is checked
    # by the guard rather than invisible to it. Still the kit's largest module
    # and still the first WI-280 candidate.
    # Then -58 (3887 -> 3829), D-5 step 2: same move to `spine_carrier.py`.
    # Net against pre-D-5: +32 — the git shell for the two-tree read, which is
    # this module's own and does not belong in a pure carrier module.
    # Then +6 (3829 -> 3835), D-5 step 3 (the CUTOVER): `current_digests` reads
    # the three tiers through the carrier (a CSV parse of TOML returns nothing,
    # and an empty digest map says "nothing to re-attest") and resolves the
    # needs file instead of testing one suffix.
    # Then +60 (3835 -> 3895), same commit: `_blame_row_times` grows its TOML
    # arm. A registry ROW is one line under CSV and a whole TABLE under TOML, so
    # the blame walk splits into a shared line reader plus one shape per
    # carrier — and the TOML side takes the NEWEST commit over a table's lines,
    # because an amendment edits a value line and leaves the header alone. Read
    # with the CSV rule the map keys on `[requirement.SR-001]`, every lookup
    # misses, and the backlog-staleness warn passes having checked nothing.
    # Then +2 (3895 -> 3897), WI-426 (D-7): `_staged_wi_registry`'s docstring
    # cited the duplication census as the thing that forced the WI-344
    # extraction. The census is deleted, so the docstring now carries the
    # reason that OUTLIVES it (F5 buys cross-SCRIPT copy-ability, never a
    # fourth copy inside one module). Comment only; zero code delta.
    # +10 (3897 -> 3907), WI-424: the `Brief` column joins the F5-duplicated
    # spec-folder reader's two schema tables. Verbatim in all three copies
    # (agent_common/schedule/check_trajectory), so the same +10 lands here,
    # in agent_common below, and in the un-ratcheted schedule.py.
    # Then -14 (3907 -> 3893), WI-422 (the measured dead-symbol sweep):
    # `KNOWN_STATUSES` (zero readers; OPEN_STATUSES/TERMINAL_STATUSES are the
    # live vocabulary) and the inert `SPEC_EXAMPLE` copy. Then +8 (3893 ->
    # 3901), same WI: `current_digests` carries the repo-lock D-1 pointer
    # saying WHY the anchor engine has no writer yet, so the NEXT sweep reads
    # it in the code instead of re-deriving it. Comment only; zero code delta.
    # Then +10 (3901 -> 3911), WI-429: a BUG FIX and the reason it was invisible.
    # `module_components` normalized the whole `LLR.Module` cell as one key, so a
    # `;`-joined `a.py;b.py` produced one nonsense key and tagged NEITHER module.
    # Two live rows were already losing their CMP tags this way, silently — a
    # membership map missing an entry reads exactly like a module nobody tagged —
    # and the WI-429 repoint of 13 rows turned it into a red. +1 line of code (a
    # loop over the split cell); the other 9 record the D-6 failure mode in the
    # reader that had not learned the cell's shape, because the next reader of a
    # joined cell needs to find that written down and not re-derive it.
    # WI-431 (batch-2 carrier, repo-lock §8.1): +2 (3911 -> 3913). The
    # open-items brief lint reads through `spine_carrier` instead of
    # `read_rows`, so an unparseable decision queue refuses instead of going
    # vacuously clean. Two lines; no behaviour beyond the carrier.
    # WI-432 (owner 2026-08-11, overturning WI-423): +44 (3913 -> 3957). The
    # F5 price of folding the six check toggles into docs/process.toml, PAID
    # HERE AND DECLARED rather than argued down: this module is copied ALONE
    # into repos that carry no coordinator layer, so it grows its own
    # `_process_check` — 24 lines, of which 10 are executable and 12 are the
    # docstring recording the fail-LOUD direction — plus the TOML-first arm on
    # each of the three readers. Reviewed bump; tests/test_rule_sync.py pins
    # this copy against gen_okf's and subagent_gate's by value (D-7).
    # WI-440 (OI-14's third do-not-wait): +73 (3957 -> 4030). The cross-CMP
    # rule's overlap guard was authoring-silenceable fail-open — tagging a
    # module into MORE components monotonically REDUCED findings (measured on
    # this repo: 64 of 97 classifiable edges suppressed by set overlap, 17 via a
    # multi-tagged endpoint) — so the overlap now REPORTS as its own warn-only
    # advisory instead of suppressing. The line cost is mostly DECOMPOSITION
    # rather than new behaviour: the edge walk moved out to
    # `_classifiable_edges`, the IF-endpoint read to `_declared_seam_pairs`, and
    # the tier decision to `_cross_component_scan`, which is what let the
    # complexity ratchet DELETE `cross_component_findings`' entry instead of
    # bumping it. The rest is the two docstrings recording why the direction is
    # the fix and why the advisory must never join the exit code.
    "check_trajectory.py": 4075,  # +25 2026-08-13: WI-443 — the seam-TC rule re-keyed off the retired IF Status onto Stability, summarised (reviewed bump, reason in the log); earlier +20 2026-08-13: WI-440 review fixes — the lazy covered-pairs read + the one-scan-per-run cache (reviewed bump, reason in the log)
    # NEW ENTRY, +25 (1498 -> 1523), WI-357: the two-stage work-branch claim
    # signal — the on-disk fast path plus the branch-history probe that
    # survives the §2.3 close commit (git log -1 over the claim path), with
    # the fail-toward-trunk comment a successor would otherwise "simplify"
    # back into the defect, and the review-measured breadth/cost notes on the
    # residual. check.py sat 2 lines under THRESHOLD before the fix; even the
    # zero-comment form crossed it, so this is the crossing recorded, not
    # growth approved. Reviewed bump, log 2026-07-29. Re-stamp down with
    # WI-280.
    # +1 (1523 -> 1524), WI-384: the claim-signal docstring line that says the
    # close moves specs to their TERMINAL directory rather than "archives"
    # them. One wrapped comment line. Reviewed bump, log 2026-08-01.
    # +24 (1523 -> 1547), WI-386: `--trunk-lane`, the ONE deliberate exception
    # to the rule the WI-357 entry above added. The station protocol moves the
    # only mechanical bar in the loop onto the branch, so the branch's tree
    # becomes the trunk's tree and owes the freshness gates the lane rule
    # stands down. Without the flag those seven steps SKIP and the integrator
    # reads any SKIP as a refusal, so the refresh could never go green — the
    # flag MAKES the mechanical bar possible (REVIEW-A round 1 corrected the
    # direction stated here: it does not rescue the bar from a false pass).
    # 13 of the 26 added lines (24 net) are the argparse help and the comment
    # recording why an opt-in override to a fail-closed rule is safe — the text
    # a successor would otherwise delete as redundant — with 4 more in the
    # module usage docstring; the behaviour is one flag, one module global, one
    # `or`. (Round 2 corrected that count from "eleven of the 24", which erred
    # in this entry's own favour.) Reviewed bump, reason here and in
    # docs/log.d/WI-386-station-protocol.md. Re-stamp down with WI-280.
    # +25 net (1523 -> 1548), WI-386 merging trunk `979d8e09`: NOT a new bump
    # and not a side picked — the same shape WI-384 hit on this file one merge
    # earlier, and resolved the same way. WI-384 and WI-386 re-stamped from the
    # same base 1523 on parallel branches (1524 and 1547) and the merge
    # conflicted here. Resolved by RE-MEASURING the merged file with the
    # census's own metric (`len(text.splitlines())` = 1548), which is exactly
    # 1523 + WI-384's +1 + WI-386's +24: the two changes are disjoint (a
    # docstring line and a flag), so the arithmetic CHECKS the resolution
    # rather than merely agreeing with it. Both reason chains above are
    # preserved verbatim; neither WI's record was dropped to make the number
    # fit. Re-stamp down with WI-280.
    # Then +8 (1548 -> 1556), SN-031: the doc-navigability step ignores `docs/handbacks/*` — the
    # per-close reports are DATA, and orphan-warning every lane close is
    # how a checker earns the ignore that makes it useless. Reviewed bump.
    # Then +4 (1552 -> 1556), WI-426 (D-7): the `[step:dupes]` example in
    # `extra_steps`' docstring pointed at a script the kit no longer ships, and
    # two more docstrings justified themselves by what the census had caught.
    # Re-worded onto reasons that survive the teardown, with the ruling named
    # so the next reader does not re-derive it. Comment only; zero code delta.
    # Then +82 (1556 -> 1638), WI-427: SN-010 is a UNIVERSAL ("every generated
    # artifact carries a --check freshness contract") and two declared
    # `[generated]` artifacts falsified it — skills/INDEX.csv and
    # prompts/CATALOG.md each had a working --check that ran NOWHERE. The two
    # steps that make the need true land here, in the one table that owns the
    # gate sets, because that is where every sibling freshness step lives; a
    # step declared anywhere else is the 130-REVIEW-A failure (an adopter's
    # older stack.ini blocking every commit with `no step named`). Most of the
    # 82 is the reasoning this row was required to record in code — why the gate
    # set is {G1,G2,G3} and not the {G3} family's, why the index check is its
    # own step rather than folded into skills-sync, why --skills is passed
    # explicitly (the default is a vacuous pass), and why neither step joins
    # _TRUNK_FRESHNESS_STEPS. Trimmed once before stamping (1649 -> 1638) by
    # merging the two step rationales into one block. Reviewed bump; re-stamp
    # down with WI-280, which owns this module's decomposition.
    "check.py": 1638,
    # +1 (1916 -> 1917), WI-279: one MAPPING row registering the new
    # scripts/check_coverage.py kit gate so it ships downstream — a required
    # one-line registration, not monolith growth (the reviewed-bump escape the
    # ratchet documents; not a drive-by). Re-stamp downward with WI-280.
    # +59 (1917 -> 1976), WI-097/OI-4: `write_kit_license` + `KIT_LICENSE_HEADER`,
    # so every scaffold carries the Apache-2.0 text the copy-in step redistributes
    # under (§4(a)) — new REQUIRED behaviour, and roughly two-thirds of the bump is
    # the header prose stating what the license does NOT cover (the adopter's own
    # code), which is the part that stops a scaffold reading as an over-claim.
    # `main()` took no new branch: the writer reports its own outcome, so the
    # complexity ratchet held at 41. Reviewed bump; re-stamp downward with WI-280.
    # +10 (1976 -> 1986), WI-097 follow-up: the full suite caught what smoke could
    # not — a fresh PRIVACY-CHECKED scaffold reds on the copyright holder's real
    # name in docs/kit-license. Fixed by moving attribution out of the License
    # instrument (stock Apache appendix placeholder, real holder in the root
    # NOTICE) into ONE header line carrying `privacy-ok`, plus the comment saying
    # why that marker is legitimate here and must stay the only one. Reviewed bump.
    # +17 (1986 -> 2003), WI-322: the scaffolded OI-3 brief becomes a registry
    # ROW written with csv.writer (a brief cell carries commas), and bootstrap
    # seeds the generated owner surface so a fresh scaffold passes its own
    # freshness gate. Reviewed bump, log 2026-07-26.
    # +4 (2003 -> 2007), WI-329: trace_text.py joins MAPPING beside trace.py (which
    # imports it, so a scaffold missing it ImportErrors on the first check) plus the
    # comment saying why they copy together. Reviewed bump, log 2026-07-27.
    # +10 (2007 -> 2017), WI-347: `copy_if_new` (the write-once scaffold copy, 3
    # call sites) and `_skill_rel` (the refreshed-path identity the write and
    # delete arms both report). An EXTRACTION that grows the file, which is the
    # normal shape here and not a contradiction: two named helpers with docstrings
    # cost more lines than the three inline copies they replace, and buy the
    # thing lines cannot — one home for the rule. Reviewed bump, log 2026-07-28.
    # +36 (2017 -> 2053), Phase 2c-i: the registry's SECOND home ships. Three
    # MAPPING rows (the `wi_convert.py` kit script, the `WI-000` work-spec
    # template, and the `orphans-allow` declaration that keeps a fresh scaffold
    # warning-free — a work spec is a registry entry, not a page anyone
    # navigates to), the three `docs/work/` status directories in GITKEEP_DIRS,
    # and the docstring inventory lines for all of it. The orphans-allow row is
    # the FULL SUITE's correction to a smoke-green tree: `test_profile`'s ten
    # scaffold-green permutations caught the orphan warning the targeted tests
    # could not see. Required registration plus its reasons, not monolith growth
    # — the same shape as the WI-279 and WI-329 rows above. Reviewed bump;
    # re-stamp downward with WI-280.
    # +19 (2052 -> 2071), Phase 3 (§5.1): the trunk_step.py MAPPING row, the
    # docs/log.d/ GITKEEP_DIRS entry, and the docstring inventory lines — the
    # same required-registration shape as the WI-279/WI-329/2c-i rows above.
    # Reviewed bump, log 2026-07-29. Re-stamp down with WI-280.
    # +7 (2071 -> 2078), Phase 4: the integrate.py MAPPING row + docstring
    # inventory lines - the same required-registration shape. Reviewed bump,
    # log 2026-07-29. Re-stamp down with WI-280.
    # +7 (2078 -> 2085), WI-374: the drive.py MAPPING row + docstring
    # inventory lines - the same required-registration shape. Reviewed bump,
    # log 2026-07-31. Re-stamp down with WI-280.
    # +5 (2085 -> 2090), WI-280 S2: the traj_graph.py MAPPING row + its
    # copied-together comment + the docstring inventory line — the same
    # required-registration shape as the WI-329/WI-374 rows above. Reviewed
    # bump; the WI-280 log fragment carries the reason.
    # +1 (2090 -> 2091), WI-280 S3: the traj_parse.py MAPPING row (the S2
    # comment covers the family). Reviewed bump.
    # +1 (2091 -> 2092), WI-280 S4: the traj_render.py MAPPING row. Reviewed
    # bump.
    # +1 (2092 -> 2093), WI-280 S5: the traj_views.py MAPPING row. Reviewed
    # bump.
    # +1 (2093 -> 2094), WI-280 S7: the traj_status.py MAPPING row. Reviewed
    # bump.
    # +2 (2094 -> 2096), WI-280 S6: the traj_panels.py MAPPING row + the
    # docstring inventory line wrapping onto two. Reviewed bump.
    # +128 (2096 -> 2224), WI-280 slice 10: main()'s decomposition — the
    # extraction-grows-the-file shape this module has taken before (WI-347's
    # entry states it): nine named phase functions plus the two typed records
    # (ScaffoldPlan / CopyOutcome) cost their own `def` lines and docstrings,
    # and buy what lines cannot — main() drops from 380 straight-line lines at
    # complexity 41 to a ~40-line sequencer, and its complexity entry is
    # DELETED rather than re-stamped. Output proven byte-identical (scaffold
    # byte-compare suites + a pre/post --dry-run stdout diff). Reviewed bump,
    # reason here and in docs/log.d/WI-280-bounded-core-decomposition.md.
    # +8 (2224 -> 2232), WI-379: the schedule.py MAPPING row plus the comment
    # stating WHY it is load-bearing (integrate.py's claim ladder and drive.py's
    # cycle import it UNGUARDED, so a scaffold without it could not claim work
    # at all). Required registration, not monolith growth - the same shape as
    # the trunk_step/integrate/drive rows above. Reviewed bump, log 2026-07-31.
    # +9 (2232 -> 2241), WI-384: three more scaffolded status directories
    # (draft/, cancelled/, complete/) in GITKEEP_DIRS plus the comment stating
    # why `draft/` is scaffolded for a reason beyond visibility — a spec under
    # an undeclared directory never enters the registry, so the duplicate-id
    # guard and the dashboard go blind to the id it holds. Required
    # registration, not monolith growth: the same
    # shape as the MAPPING rows above. Reviewed bump, log 2026-08-01.
    # +2 (2241 -> 2243), WI-384 REVIEW-A round 1: the same corrected rationale
    # in the GITKEEP_DIRS comment. Two comment lines, zero code tokens.
    # Reviewed bump, log 2026-08-01.
    # +7 (2243 -> 2250), WI-387: the scaffold registration of the new sibling
    # handback.py — one MAPPING row, its four-line reason, and two docstring
    # lines in the kit-contents listing. Required registration, not monolith
    # growth: the same shape as the trunk_step/integrate/drive rows above (and
    # the omission this repo learned to fear — a scaffold-surface change that
    # ships without its MAPPING row breaks every fresh scaffold while the kit's
    # own tree stays green). Reviewed bump, log 2026-08-01.
    # +7 (2250 -> 2257), WI-393: the scaffold registration of the new sibling
    # spec_move.py (the link-aware move ritual) — one MAPPING row, its
    # four-line reason, and two docstring lines in the kit-contents listing.
    # Required registration, not monolith growth: exactly the WI-387 handback
    # shape directly above. Reviewed bump, log fragment 2026-08-01 (WI-393).
    # +1 (2257 -> 2258), WI-392: the scaffold registration of the new sibling
    # check_figures.py (declared-figure provenance) — one MAPPING row; the
    # docstring listing absorbed the name on its existing check_* line.
    # Required registration, not monolith growth: the WI-393/WI-387 shape
    # directly above. Reviewed bump, log fragment 2026-08-01 (WI-392).
    # +9 (2258 -> 2267), WI-381: the dispatcher-split scaffold registration —
    # the drive.py MAPPING row becomes dispatch.py + lane.py rows (the WI-280
    # lesson: a MAPPING omission breaks every fresh scaffold while this repo
    # stays green), and the docstring listing carries the two names. Required
    # registration, not monolith growth: the WI-392/WI-393 shape directly
    # above. Reviewed bump, log fragment 2026-08-02 (WI-381).
    # +11 (2267 -> 2278), WI-388: the intake.py MAPPING row + its kit-contents
    # listing entry — the scaffold surface gained the unified intake mint.
    # Reviewed bump, log fragment 2026-08-02 (WI-388). Re-stamp down with
    # WI-280.
    # +165 (2278 -> 2443), SN-028: the scaffolder is where a migration has to
    # live if adopters are never to meet the mixed-config refusal un-aided —
    # `set_process_key` (a LINE rewrite, since stdlib has no TOML writer and
    # the file's header is most of its value), the `LEGACY_CONFIG` table,
    # `migrate_legacy_config`, the `--migrate-config` mode and its report.
    # Against it: four MAPPING rows and two of the three appliers' bodies
    # deleted. Reviewed bump. Re-stamp down with WI-280.
    # Then +89 (2443 -> 2532), SN-028 REVIEW round 1: `set_process_key`
    # returns THREE states, not a bool — the migrator deleted a legacy file on
    # the strength of a write that never happened and reported success,
    # destroying a declared `privacy_check = true`. Plus `add_if_missing` (so a
    # conversion is total), the `_locate_process_key` split that keeps both
    # halves under the complexity ceiling, and the prompt-template MAPPING rows.
    # Then +14 (2535 -> 2549), SN-031: `docs/work/partial/` and `docs/handbacks/` scaffolded, and the
    # module docstring re-pointed at the surfaces that actually ship.
    # Reviewed bump.
    # Then +6 (2549 -> 2555), SN-029: `attestations.csv` and the
    # `adjudicate-amendment` brief template join the scaffold MAPPING — two
    # rows, no new logic. Reviewed bump.
    # Then +92 (2555 -> 2647), SN-029 REVIEW round 1 BLOCKER: `--gate-policy`
    # STORED the enum word beside the template's `human_ratification_through =
    # 4`, and since the readers prefer the ordinal, every repo that chose a
    # non-default posture scaffolded FULLY ATTENDED with no diagnostic
    # anywhere. The word is TRANSLATED now, not stored — `LEGACY_RATIFICATION`
    # (F5-duplicated from agent_common, pinned by test_rule_sync because this
    # module imports no kit sibling) plus `_migrate_gate_policy`, the one
    # legacy file whose single word expands to three dials and so cannot be a
    # `LEGACY_CONFIG` row. Reviewed bump.
    # Then +7 (2647 -> 2654), the same slice: `ruff format`'s reflow
    # after the SN-028..032 edits (the `format` step is advisory at this gate but
    # the tree is kept formatted anyway). Mechanical; no behaviour moved.
    # Then +2 (2654 -> 2656), same pass: the scaffolded deviation register
    # stopped naming the retired `gate_policy` key.
    # Then -2 (2656 -> 2654), D-1 REMOVAL HALF: the attestations-ledger MAPPING
    # row goes with the registry — an adopter scaffolds no second attestation
    # home, and the anchor columns arrive in the spine templates instead.
    # Then +6 (2654 -> 2660), the id watermark's MAPPING row + its docstring
    # inventory line: a fresh scaffold MUST ship docs/id-watermark, because an
    # absent mark is an error rather than "no id is taken".
    # Then +30 (2660 -> 2690), same review: `docs/id-watermark` is now exempt
    # from `--force`. Every other scaffold target is a template to fill or is
    # regenerable from the tree; this one is the only record of ids that were
    # DELETED, so forcing the fresh-scaffold marks over a live repo frees them
    # for silent re-use and nothing can rebuild what was lost.
    # Then +31 (2690 -> 2721), the same feature's SHIPPED-SCAFFOLD defect:
    # `raise_watermark` plus its call from the stack profile. The non-Python
    # profile appends OI-3 while `id-watermark.template` ships `OI = 2`, so
    # every node/other-stack scaffold failed its own `trace.py --strict` on the
    # adopter's first run — the exact opposite of SN-001's "green out of the
    # box". Raise-only, because a mark may legally stand above the live maximum
    # (that headroom is what retires a deleted id) but must never fall.
    # +11 (2721 -> 2732), D-5 step 2: two MAPPING rows and the reason each is
    # copied — `spine_carrier.py` (a sibling import, so the trace_text.py rule
    # applies verbatim: a scaffold without it ImportErrors on the first check)
    # and `migrate_carrier.py` (every adopting repo migrates too, and an
    # adopter who cannot run the round-trip proof takes the conversion on
    # faith). Nine of the eleven lines are those reasons; the code delta is 2.
    # Then -1 (2732 -> 2731), WI-426 (D-7): the `check_dupes.py` MAPPING row
    # and its name in the docstring's scaffold listing are gone with the
    # script. Re-stamped DOWN in the same commit, per the standing rule that a
    # deletion shrinks a module and a generous ceiling silently permits regrowth.
    # +4 (2731 -> 2735), WI-424: `adjudicate_brief.py` joins MAPPING beside
    # prompts.py — the module that FILLS the shipped briefs is as required
    # downstream as the briefs themselves.
    # Then -12 (2735 -> 2723), WI-422 (the measured dead-symbol sweep): `prompt_text` — the free-text sibling of `prompt_choice`, born with no
    # caller and never given one.
    # WI-431 (batch-2 carrier, repo-lock §8.1): +33 (2723 -> 2756). The
    # scaffolded OI-3 brief moves from a 12-cell POSITIONAL tuple written by
    # `csv.writer` to KEYED cells appended as a TOML table. The growth is the
    # keys — a positional tuple aligned to a header is the shape that silently
    # shifts when a column moves, and TOML has no header to align to — plus the
    # paragraph declaring WHY this file carries its own two-line emitter:
    # `bootstrap.py` runs before the kit is copied and can import no sibling
    # (repo-lock §8.2), and `tests/test_rule_sync.py` pins the key set against
    # the converter so the declared duplication cannot drift. Net +31 after the
    # `csv`/`io` imports the CSV writer needed went with it.
    # WI-432: +13 (2754 -> 2767). Six LEGACY_CONFIG rows and the paragraph
    # saying which coercer preserves which legacy vocabulary. bootstrap grows
    # NO local TOML reader — it only converts and deletes, so it never reads
    # these keys, which is why the F5 cost lands in the three checkers instead.
    # WI-439 (OI-27 defect 1): +26 (2767 -> 2793). REVIEWED BUMP, the escape
    # hatch this docstring documents — not monolith drift. The no-git stamp path
    # shipped an anchorless `unknown (kit not a git checkout)` SILENTLY at exit 0
    # (the loud stamp warning branches on `dirty`, hard-coded False there), so
    # the one adopter with no re-sync anchor at all was the only one never told.
    # The delta is a `KIT_VERSION_UNKNOWN` constant (one home for the label, so
    # the warner and both return paths cannot disagree — that disagreement IS the
    # defect), one `elif` in `write_stamps`, and the warning text, which is long
    # because it must name the consequence and the fix while the operator still
    # knows which kit they downloaded. Decomposing bootstrap.py to buy back 26
    # lines is WI-280's job, not a stamp fix's. Re-stamp downward with WI-280.
    "bootstrap.py": 2808,  # +15 2026-08-13: WI-439 review fix — the tracked-file anchor probe + the three-cause warning wording (reviewed bump, reason in the log)
    # WI-446: +20 (2767 -> 2787). Two MAPPING rows registering the hats layer
    # (SN-036 / OI-19) — the roster template and the `hats.py` reader its
    # importer needs — plus their reason comments and the two docstring lines in
    # the kit-contents listing. Registration, not monolith drift: the layer's
    # own code is a new module under THRESHOLD, and a MAPPING row is the only
    # way a scaffold ever receives a file. Reviewed bump; re-stamp down with
    # WI-280.
    "bootstrap.py": 2828,  # composed at the 2026-08-13 serial merge: WI-439 (+26) + its review fix (+15, the tracked-anchor probe) + WI-446's MAPPING rows (+20); measured, reasons above and at each contributing WI
    # NEW ENTRY, +228 (1423 -> 1651), Phase 2b of the concurrency restructure
    # (docs/concurrency-restructure.md §7): the spec-folder work-item reader,
    # which crosses this module over THRESHOLD for the first time. It is one
    # verbatim copy of a reader that also lands in schedule.py and
    # check_trajectory.py — the F5/WI-291 pattern, where a shared module was
    # rejected (owner ruling 2026-07-12) so each script stays independently
    # copy-able, and DRIFT is closed by tests/test_wi_loader_sync.py instead of
    # by extraction. So the honest description is not "agent_common grew" but
    # "the registry has two homes during the migration": roughly two thirds of
    # the 228 is the docstring and the format's rules, and the whole entry
    # RETIRES at Phase 5 when the CSV home goes and the reader is the only one
    # left. Re-stamp DOWN then — this is the one baseline here with a scheduled
    # end date. Reviewed bump; reason here and in the Phase 2b session record.
    # +15 (1651 -> 1666), Phase 2c-i: the SAME `-000` authority rule as
    # check_trajectory's entry above — one of the three verbatim copies, so the
    # number is identical by construction and a divergence here would itself be
    # the drift `tests/test_wi_loader_sync.py` exists to catch. Retires with
    # this whole entry at Phase 5. Reviewed bump.
    # +54 (1666 -> 1720), Phase 3 (§5.6): `tracked_pause` — the TOML reader for
    # the tracked docs/work/pause (fail-closed on malformation) — and
    # `pause_reason` learning the second home so the retired-in-place
    # dispatcher can never resume on a home swap. The legacy-home half retires
    # with the dispatcher at Phase 5. Reviewed bump, log 2026-07-29.
    # -2 (1720 -> 1718), Phase 5 item 1 (2026-07-29): docstring edits only —
    # the dispatcher references in the module docstring, harness_python and
    # _declared_test_command re-worded for the deleted module. The scheduled
    # BIG down-stamp here (the +228/+15 CSV-reader entries above) lands with
    # Phase 5 item 3, not this commit.
    # -25 (1718 -> 1693), Phase 5 item 1/C2 (2026-07-29): _write_runstate and
    # SANCTIONED_TRAIN_SUBJECT_PREFIXES retired with docs/run-state and the
    # commit-msg train floor; END_STATES/docstring re-words. Ratcheted DOWN.
    # -17 (1693 -> 1676), Phase 5 item 2/C3 (2026-07-29): pause_reason's legacy
    # untracked-home half retired (tracked docs/work/pause is the one home),
    # resolve_coordinator_dials dropped the dispatcher jobs dial, the
    # llm/train branch-equality preflight re-grounded on the claim model, and
    # TRAIN_BRANCH_PREFIX left. Ratcheted DOWN.
    # -22 (1664 -> 1642), Phase 5 item 3/C4 (2026-07-29): THE scheduled
    # down-stamp — the dual-read resolution (spec_registry_dir + the CSV
    # fallback) collapsed to the folder-only read; the +228/+15 entries above
    # are repaid. Ratcheted DOWN.
    # +58 (1642 -> 1700), WI-361 (2026-07-29): harness_floor_failures — the
    # WI-286 fail-closed floor re-homed from the deleted dispatcher onto the
    # surviving integrate.py bar seam, plus the arming-boundary docstring
    # (arms only where requirements-dev.txt declares the pinned toolchain).
    # A restored guarantee with its contract stated, not monolith drift;
    # ~2/3 is docstring. Reviewed bump, log 2026-07-29. Re-stamp down with
    # WI-280.
    # +20 (1700 -> 1720), the grind-close census extraction: worktree_records
    # — the ONE shared porcelain walk — after check_dupes caught
    # integrate._worktree_holding re-implementing primary_worktree_root's
    # parse (extraction, not sanction: the WI-304 precedent). integrate.py
    # shrank 9 in the same move. Reviewed bump, log 2026-07-29. Re-stamp
    # down with WI-280.
    # +8 (1720 -> 1728), WI-384: the six-state vocabulary in the F5 reader copy
    # — two more SPEC_STATUS_DIRS rows and the comment recording the two
    # terminals and the id-reservation reason, minus the disposition validator
    # this row deleted. Identical text to the other two copies by construction
    # (tests/test_wi_loader_sync.py). Reviewed bump, log 2026-08-01. Re-stamp
    # down with WI-280.
    # +3 (1728 -> 1731), WI-384 REVIEW-A round 1: the corrected `draft/`
    # rationale in this copy of the F5 block — identical text to the other two
    # by construction (tests/test_wi_loader_sync.py). Three comment lines, zero
    # code tokens. Reviewed bump, log 2026-08-01.
    # +10 (1731 -> 1741), WI-387: the `## Handback` section joins the spec body
    # grammar (`SPEC_HANDBACK` + the four-line partition in
    # `parse_spec_deliverable`) so a returned WI can say in trunk what remains.
    # Identical text to the other two F5 copies by construction
    # (tests/test_wi_loader_sync.py). Reviewed bump, log 2026-08-01. Re-stamp
    # down with WI-280.
    # +43 (1741 -> 1784), WI-398: `_failure_tail` re-anchored on the failing
    # step's OWN banner-to-end window (found by the name the FIRST FAIL line
    # carries, extracted as `_own_step_window` — the C901 ratchet's preferred
    # shape) instead of the LAST FAIL line — which check.py's closing summary
    # re-prints at any --jobs, so the old window was structurally always
    # summary rows and never the step's error text (three lost diagnoses of
    # one WI-387 red). Roughly half the bump is the docstring history that
    # keeps a successor from "simplifying" back to last-FAIL. Reviewed bump,
    # log fragment 2026-08-01 (WI-398). Re-stamp down with WI-280.
    # +8 (1784 -> 1792), WI-405: the known-limit clause in `_own_step_window`'s
    # docstring (WI-398 REVIEW-A finding 1) — bar-shaped text EMBEDDED in a
    # step's own captured output can misanchor the window; the kept full log is
    # the refresh path's authority. Eight docstring lines, zero code tokens;
    # the three hostile shapes are pinned in test_agent_common_harness.py.
    # Reviewed bump, log fragment 2026-08-02 (WI-405). Re-stamp down with
    # WI-280.
    # +32 (1792 -> 1824), WI-381: `dispatch_lock_path` (the ONE home for the
    # lock the dispatcher holds and `integrate claim` now requires — §A4.1's
    # authority flip needs holder and requirer to name the same file by
    # construction), `_open_lock_fd` (the open+flock primitive extracted so
    # integrate's dispatch-lock rung shares it instead of copying it), and
    # the `lanes` dial row in AGENT_LOOP_DIALS. Reviewed bump, log fragment
    # 2026-08-02 (WI-381). Re-stamp down with WI-280.
    # +15 (1824 -> 1839), WI-388: the F5-mirrored loader edits (`Bar` column,
    # `SPEC_CONTEXT` + its clip in `parse_spec_deliverable`). Reviewed bump,
    # log fragment 2026-08-02 (WI-388). Re-stamp down with WI-280.
    # +174 (1839 -> 2013), SN-028: docs/process.toml, the ONE policy home.
    # `read_toml` + `process_config` + `declared_policy` + `config_conflicts` +
    # the PROCESS_KEYS migration table — most of the growth is the table and
    # the prose that has to survive here, because this module is where the
    # dual-read window's precedence and the hard mixed-config refusal are
    # DEFINED for every consumer (dispatch, intake and integrate each read
    # policy without passing through agent_loop.main). Reviewed bump; the
    # counterweight is ~10 one-word files and their five ad-hoc parsers
    # retiring. Re-stamp down with WI-280.
    # Then +120 (2013 -> 2133), SN-028 REVIEW round 1: the review drove five
    # file shapes where the sh hooks and `tomllib` DISAGREED about the privacy
    # gate — three of them fail-OPEN. Two grammars read one file, so the file's
    # SHAPE became a checked contract (`process_shape_findings`) rather than a
    # convention, `_coerce` stopped substituting a default for a wrong-typed
    # dial, and `config_conflicts` grew the shape + type findings. Most of the
    # delta is the reasoning, which is the part that must not be lost.
    # Then +33 (2133 -> 2166), SN-031: `partial/` declared in the F5-triplicated status table, the
    # `Supersedes` lineage column, `read_toml_text`, and the prose each
    # needs. Reviewed bump.
    # Then +95 (2166 -> 2261), SN-029: the ORDINAL's one home — `ratification_
    # level` (with `LEGACY_RATIFICATION_LEVEL` mapping the retired enum and
    # `RATIFICATION_FALLBACK` naming the conservative default), `human_holds`
    # (the single comparison every consumer makes, including the ruling that
    # both ENDS of the ordinal are absolute), `keep_nondependent` and
    # `spine_stage_of`. Five consumers stopped string-comparing policy words;
    # the growth is the definition plus the reasoning for the two ends.
    # Reviewed bump.
    # Then +90 (2261 -> 2351), SN-029 REVIEW round 1. The review drove the
    # ordinal's own defects: `LEGACY_RATIFICATION` states all THREE dials a
    # retired enum word meant instead of collapsing it to a level (translating
    # `single-ratify` to "level 2" silently gave it a per-tier hold it never
    # had), `human_holds` compares STRICTLY LESS-THAN against a cumulative
    # count, an out-of-range level FALLS BACK rather than clamping (`-1`
    # clamped to 0 — the one input that read as LESS human involvement than
    # asked for), and `PROCESS_ONLY_KEYS`/`PROCESS_KEY_RANGES` +
    # `_key_value_findings` give the process.toml-only dials the type check the
    # legacy-file dials already had. Reviewed bump; most of the delta is the
    # reasoning for the two ends of the ordinal.
    # Then +26 (2351 -> 2377), SN-032: `prompt_fingerprint` and the two session
    # telemetry keys it feeds (`prompt-template`, `prompt-sha`) — a session's
    # instruction becomes auditable after the fact without keeping every
    # rendered prompt on disk. Reviewed bump.
    # Then +63 (2377 -> 2440), the FINAL review's fix pass: `final_review` and
    # `complete_review` gained the READERS they shipped without — three
    # declared, type-checked dials that no code consulted, so the promised
    # final human read and the promised clean-close spot-check both happened
    # exactly never. Plus the level-4 restore in `human_holds` (a fully
    # verified spine is stage 4, which is precisely when a gate-advance row
    # runs, so `4 < 4` let the SHIPPED DEFAULT self-ratify the final gate).
    # Reviewed bump.
    # +10 (2440 -> 2450), WI-424: the `Brief` column, the F5 copy of the same
    # two-table edit recorded at check_trajectory.py above.
    # Then -4 (2450 -> 2446), WI-422 (the measured dead-symbol sweep): the inert `SPEC_EXAMPLE` copy (F5 twin of the check_trajectory entry
    # above; the live `-000` rule is an id-suffix test, not this literal).
    # WI-432: +20 (2446 -> 2466). Six PROCESS_KEYS rows plus the paragraph
    # recording why they sit in THAT table rather than PROCESS_ONLY_KEYS (each
    # has a legacy file, so each can be double-declared, and the mixed-config
    # refusal + --migrate-config both key off these rows).
    # WI-433: +1 (2466 -> 2467). The `BLACKOUT_RE` header comment states what a
    # fresh scaffold ships; the template stopped shipping the owner's window, so
    # the comment stops claiming it does.
    "agent_common.py": 2467,
    # NEW ENTRY, WI-387 — integrate.py crossed THRESHOLD (1418 -> 1588) adding
    # the third terminal outcome. The extraction the ratchet asks for was TAKEN
    # FIRST, not argued away: `hand_back` and `quarantine`, the largest unit and
    # the only genuinely separable one, ship as the new sibling handback.py (261
    # lines, under THRESHOLD, its own MAPPING/README/test-list rows) — exactly
    # the WI-374 precedent that put the drive loop in drive.py rather than into
    # agent_loop.py. What remains is irreducibly this module's own: the CLAIM
    # (inverted to commit-tree -> branch -> trunk, plus `_abandoned_claim`, the
    # shape recogniser that lets a crashed claim be re-cut instead of hand-
    # repaired — this is what DELETED `drive._stranded_claims`), the outcome
    # READ the merge slot gates on (`OUTCOME_DIRS` + `branch_outcomes`), and
    # `_verdict_gate` re-keyed off the outcome. Splitting any of those out would
    # put half of one decision in another file. Reviewed bump, reason in
    # docs/log.md 2026-08-01; re-stamp DOWN with WI-390's deletions (the §A9.1
    # discipline) or with WI-280.
    # +50 (1588 -> 1638), WI-387 REVIEW-A round 1, both MAJORs landing here or
    # beside here. `_abandoned_claim` gained the fourth fact that actually
    # establishes "no work was built on this branch" — the tip's diff against
    # its own parent must touch only the RULING-6 bookkeeping surfaces — plus
    # the exact `_claim_subject` comparison and the `wi_id` it needs for it;
    # the re-claim now prints the deleted sha and its restore command; and
    # `branch_outcomes` collects per-basename outcome SETS so a spec in two
    # folders refuses instead of silently resolving toward the outcome that
    # skips the verdict gate. The rest is the claim docstring, whose two false
    # sentences were replaced by the measured three-window account and the
    # measured list of what the plumbing commit bypasses — record correction,
    # which this program pays for in prose or pays for later. Reviewed bump,
    # log 2026-08-01.
    # +5 (1638 -> 1643), same round: the fourth fact reuses the RULING-6 allowed
    # set, so a repo that declares no `[generated]` artifacts fails CLOSED there
    # (its own claim commits carry the regeneration and stop looking like claim
    # commits). Five comment lines saying so, because the failure DIRECTION is
    # the part a successor would otherwise have to rediscover. Reviewed bump,
    # log 2026-08-01.
    # +34 (1643 -> 1677), REVIEW-A round 2: two more reports-success-on-failure
    # shapes closed. `git branch -D`'s return code is read and the HOLDER named
    # (it refuses a branch a worktree has checked out, and announcing a deletion
    # that did not happen is what hid the rename mis-parse next door); and the
    # content fact narrows from "only bookkeeping surfaces" — under which a
    # commit adding just a log fragment was convicted and the fragment lost — to
    # what the claim actually WRITES: this WI's spec move into active/<branch>/,
    # required, plus declared generated paths, nothing else. Reviewed bump,
    # log 2026-08-01.
    # +15 (1677 -> 1692), same round: the orphan-deletion block extracted to
    # `_drop_abandoned` because reading the return code pushed `claim` to C901
    # 11. Extraction over a complexity baseline - the ratchet's stated
    # preference - and the helper carries the WHY of both the printed sha and
    # the checked code. Reviewed bump, log 2026-08-01.
    # +41 net (1692 -> 1733), WI-387 merging trunk `4fb02de4`: NOT a new bump
    # and not a side picked. The auto-merge kept 1692 - trunk carried no
    # integrate.py entry at all, because ITS copy was 1449, under THRESHOLD - so
    # the stamp had to be re-measured rather than trusted. Resolved by measuring
    # the merged file with the census's own metric (`len(text.splitlines())` =
    # 1733) and checking the arithmetic: base `6b22f169` 1418, + this branch's
    # +274, + WI-378's +31 (the `_verdict_gate` docstring census), + the 10-line
    # bridge paragraph the conflict resolution added = 1733 exactly. The sum
    # CHECKS the resolution rather than agreeing with it: dropping either side's
    # paragraph to clear the conflict would show up here as a shortfall. Both
    # reason chains survive - WI-378 had none to preserve at this entry, and
    # every WI-387 line above is intact. Re-stamp DOWN with WI-390.
    # +157 (1733 -> 1890), WI-397: the RULING R1 mint refusal, and the two
    # extractions the other two ratchets asked for on the way. The rung itself
    # (`_minted_id_refusal`) is ~25 lines of code under ~55 of docstring, and
    # that ratio IS the justification: it is three git reads, while WHY they are
    # those reads - the branch's own merge-base delta, so trunk minting stays as
    # free as it is today; adds only; `--no-renames` because rename detection
    # hides a mint inside the branch's own close (driven, not asserted, in
    # tests/test_integrate.py) - is what a successor would otherwise rediscover
    # from the id collision that caused the ruling. It belongs HERE and nowhere
    # else: a refusal of the merge slot, `_claim_refusal`'s shape at the other
    # end of the lane's life. The rest is DEDUPLICATION, not bulk: `_spec_id`
    # replaces the inline filename split in `_claimed_specs` (one home for
    # filename->id, since the rung's question is "is this id in that set");
    # `_name_status` replaces the `--name-status` walk duplicated into
    # `_abandoned_claim` (check_dupes convicted the copy - deleted rather than
    # censused); and `_merge_refusal` lifts the slot's whole ladder out of
    # `integrate_one`, which the new rung had pushed to C901 11 - the extraction
    # this ratchet prefers over a bigger complexity number, the `_drop_abandoned`
    # precedent from WI-387. Reviewed bump, log 2026-08-01; re-stamp DOWN with
    # WI-390's deletions.
    # +56 (1890 -> 1946), WI-393: the claim's move becomes the link-aware
    # ritual, and the RITUAL ITSELF went to the new sibling spec_move.py (under
    # THRESHOLD - the WI-374/WI-387 escape this ratchet documents), NOT here.
    # What lands here is only what belongs to the claim: the `spec_move.move_spec`
    # call replacing the bare `git mv` (with the comment naming the 2026-08-01
    # driven instance), and the widened content fact in `_abandoned_claim` -
    # the conviction must now recognise the relink writes inside a crashed
    # claim's one commit, and it does so by ORACLE (`_relinked_exactly`:
    # byte-for-byte against `spec_move.expected_relink` over the commit's own
    # move pair), not by widening to "any .md edit" - the round-2 narrowing
    # lesson kept. `_claim_delta` is the same clause's C901 extraction (the
    # diff-walk classification out of `_abandoned_claim`, which the new arm had
    # pushed to 14 - the `_drop_abandoned`/`_merge_refusal` precedent). Driven
    # both ways in tests/test_integrate.py: the relinked crash re-cuts, the
    # non-relink .md edit still convicts. Reviewed bump, log fragment
    # 2026-08-01 (WI-393); re-stamp DOWN with WI-390's deletions.
    # +31 (1946 -> 1977), WI-398: `_keep_refused_output` — a refused refresh
    # retains its FULL output at root/out/run-logs/refresh-refused-<branch>.log
    # (outside the lane worktree, so the undo's reset and `_shed_residue`
    # cannot sweep the evidence) and the refusal message names the path. One
    # file per branch, overwritten; deliberately NO rotation/indexing (the
    # WI-398 scope guard), stated in the docstring that is most of the bump.
    # Reviewed bump, log fragment 2026-08-01 (WI-398). Re-stamp down with
    # WI-280.
    # +102 (1977 -> 2079), WI-400: the unload's DECLARED tool-residue shed.
    # Every worker-built lane in the 2026-08-01 drain ended UNLOAD INCOMPLETE
    # over the identical six ignored paths (caches + the generated trace
    # report), because `_shed_residue` covers only what the refresh's own bar
    # added. `_unload_branch` now sheds the short enumerated declared set
    # (`_RESIDUE_DIR_NAMES`/`_RESIDUE_FILES` + `_is_declared_residue` +
    # `_shed_declared_residue`/`_sweep_residue_dirs`, split per this file's
    # extraction precedent) then re-reads the dirt and still refuses on any
    # remainder, naming it; plus the step-out-of-the-lane guard before
    # `git worktree remove` (the WI-397 close's half-unregistered lane).
    # Roughly half the bump is the docstrings/comments that keep the shed
    # narrow. Reviewed bump, log fragment 2026-08-02 (WI-400). Re-stamp down
    # with WI-280.
    # +24 (2079 -> 2103), WI-403: the abandoned-claim oracle's byte-clean
    # reads. WI-393 REVIEW-A finding 1 drove `_relinked_exactly` excusing a
    # trailing-newline-only hand edit and a whole-file CRLF relay, because its
    # reads went through `ac.git`'s text-mode `.strip()`/EOL-fold.
    # `_blob_bytes` (raw `git cat-file blob`) plus the strict-decode compare
    # makes the docstring's "byte-for-byte" literally true; most of the bump
    # is the two docstrings stating the property honestly. Reviewed bump, log
    # fragment 2026-08-02 (WI-403). Re-stamp down with WI-280.
    # +22 (2103 -> 2125), WI-407: the WI-400 REVIEW-A follow-ups on the shed.
    # `ignored_files`' backslash normalization gated to Windows (on POSIX the
    # replace MINTED an alias onto a tracked path - finding 1, driven);
    # `docs/test/report.html` joins `_RESIDUE_FILES` on the wi-402 lane
    # measurement (finding 2); `_sweep_residue_dirs` gains the ignored lock
    # (`git check-ignore`, finding 3). All but four lines are the docstrings
    # and comments recording why each guard exists. Reviewed bump, log
    # fragment 2026-08-02 (WI-407). Re-stamp down with WI-280.
    # +126 (2125 -> 2251), WI-381: the §A4.1 authority flip and the spine
    # batch. The claim's `safety_class != ordinary` refusal arm is DELETED
    # (admission is the dispatcher's decision); what closes the hand-CLI hole
    # is `_dispatch_lock` — the claim REQUIRES out/agent-loop.lock, so a hand
    # claim during live lanes is unrepresentable rather than refused — and
    # `claim`/`_claim_refusal`/`_abandoned_claim`/`_claim_delta` go
    # batch-aware (§A4: all spine WIs admit together as ONE claim commit;
    # `_relinked_exactly` takes the whole move remap). `integrate()` gains the
    # `branches=` restriction so the dispatcher merges each lane's branch as
    # its own refresh completes. Most of the delta is the docstrings stating
    # the authority model. Reviewed bump, log fragment 2026-08-02 (WI-381).
    # Re-stamp down with WI-280.
    # +102 (2251 -> 2353), WI-388: the adjudication no-bar arm + the `bar`
    # strictness key — `_lane_bar_directives` (the claimed rows' say over the
    # refresh bar, read off the same trunk claim the slot reads), `_refresh_bar`
    # (the extraction that keeps `refresh` under the complexity ratchet),
    # `_run_bar`'s --gate pin — and the post-merge INTAKE arm: the one honest
    # hook point where `intake.intake_after_merge` mints inside the held slot
    # (§A5.2; the mint helper itself is the new sibling intake.py, kept under
    # the ratchet's threshold). Reviewed bump, log fragment 2026-08-02
    # (WI-388). Then +64 (2353 -> 2417), WI-388 REVIEW-A finding 1: the no-bar
    # arm's diff-scope rung (`_ADJUDICATION_SURFACES` +
    # `_adjudication_scope_ok`) — the kind alone never earns the no-bar path;
    # the branch's non-refresh delta must stay on the §A5.2 surfaces or the
    # full bar runs. Re-stamp down with WI-280.
    # +9 (2417 -> 2426), SN-028: the verdict gate reads the reviewer dial
    # through `declared_policy` and folds `config_conflicts` in ahead of it —
    # the merge slot must not pick one of two declared homes. Reviewed bump.
    # Re-stamp down with WI-280.
    # Then +45 (2426 -> 2471), SN-031: `OUTCOME_DIRS` re-mapped onto the three TERMINAL outcomes, the
    # keep/discard rung (`_partial_report_refusal`) a live incident
    # bought, and `docs/handbacks/` on the adjudication no-bar surface.
    # Reviewed bump.
    # Then +5 (2471 -> 2476), SN-029: `docs/requirements/attestations.csv` joins
    # the adjudication no-bar diff scope — an adjudication records its verdict
    # in the ledger, so the ledger must be a surface that arm may touch.
    # Reviewed bump.
    # Then -1 (2476 -> 2475), the same slice: `ruff format`'s reflow
    # after the SN-028..032 edits (the `format` step is advisory at this gate but
    # the tree is kept formatted anyway). Mechanical; no behaviour moved.
    # NEW ENTRY (2026-08-08). intake.py crosses the 1500-line monolith
    # threshold for the first time, at 1575. What put it over is the FINAL
    # review's fix pass: `_mint_shape_refusal` (no mint may write a row the
    # scheduler cannot classify — the red-TC draft was emitting
    # `adjudication` + `planmode=dual`, which reads UNCLASSIFIED, so the row
    # was minted and then permanently parked while the census reported the gap
    # as handled) and `_complete_spot_checks` (the clean-close sample that
    # `complete_review` had promised and nothing implemented). Both are
    # genuinely this module's job — it is the one place a row is created — so
    # this is a reviewed ENTRY, not a decomposition dodged: the module is now
    # the fourth over the threshold and belongs in WI-280's queue behind
    # check_trajectory.py.
    # +2 (1575 -> 1577) in the same pass:  extracted so R3's
    # no-recursion test is one predicate rather than a copy in each close arm
    # (WI-347 rules an intra-file copy a defect however small).
    # ENTRY DELETED, -85 (1577 -> 1492), D-1 REMOVAL HALF (docs/repo-lock.md,
    # owner ruling 2026-08-09): `next_att_id`, `record_attestations`,
    # `_cmd_attest` and the `attest` subparser go with `attestations.csv`, and
    # intake.py drops back UNDER THRESHOLD. Deleted rather than re-stamped, per
    # this file's own instruction ("or delete them if now <= THRESHOLD") — the
    # entry existed to name a monolith, and there is no longer one to name. It
    # re-enters as a NEW ENTRY if the anchor half puts it back over.
    # Then +9 (2475 -> 2484), the id watermark's RULING-6 hole: `intake` raises
    # the mark in the same bookkeeping commit that files a minted spec, but
    # `docs/id-watermark` was in neither BOOKKEEPING_PREFIXES nor [generated],
    # so an integrator run that minted anything flagged its OWN bookkeeping and
    # failed the queue on a false red. Nine of the lines are the comment
    # arguing why the path is bookkeeping and not generated.
    # Then +8 (2484 -> 2492), D-5 step 3: `_ADJUDICATION_SURFACES` names BOTH
    # carrier paths per spine tier — it is a pathspec allowlist matched against
    # `git diff --name-only`, and a repo that has not migrated stages the `.csv`
    # name.
    # WI-431 (batch-2 carrier): +1 (2492 -> 2493). One pathspec row, so the
    # adjudication-scope allowlist names BOTH open-items carriers — an
    # allowlist that names one suffix fails the lane toward the full bar on a
    # migrated repo, invisibly.
    "integrate.py": 2493,
    # NEW ENTRY, 1503, D-5 step 2d — the re-entry the D-1 removal note above
    # predicted, arriving from the CARRIER half rather than the anchor half:
    # "it re-enters as a NEW ENTRY if the anchor half puts it back over."
    # intake.py fell to 1496 when the attestation ledger was deleted and its
    # entry was removed rather than left standing as headroom; the sibling
    # import guard plus the two spine reads moving to spine_carrier.load put it
    # at 1503, three lines over THRESHOLD.
    #
    # Recorded rather than shaved, and the three lines are the point: trimming a
    # comment to land at 1499 would buy a green by editing the GUARD instead of
    # the thing it measures, which is the habit this file exists to prevent. The
    # honest reading is that intake.py is a monolith again by the kit's own
    # definition and is a WI-280 decomposition candidate on that basis — the
    # threshold means what it says or it means nothing.
    # Then +67 (1503 -> 1570), D-5 step 4: the Status writer gains its TOML arm
    # — a LINE REWRITE on bootstrap.set_process_key's pattern, plus the refusal
    # that fires when a located row's status line cannot be found (reporting a
    # flip that was not written is a ratification the registry does not carry).
    # Both carriers' writers now live here because both are live: an adopting
    # repo that has not run migrate_carrier is still on CSV.
    # Then +22 (1570 -> 1592), same commit: `_live_registry` — the existence
    # PROBES behind a minted row's SpecRef resolve the carrier instead of
    # testing one suffix. A `.toml`-only probe in a repo still on CSV minted
    # every gap row with an EMPTY SpecRef, which integrate then refuses at
    # merge: a failure moved from authoring time to merge time.
    # Then +71 (1592 -> 1663), the cutover's adversarial review: the TOML Status
    # writer becomes STRING-AWARE. A physical-line rewrite edited a
    # `status = ...` line inside a multi-line requirement cell, left the row's
    # real status at `Modified`, and returned True — reporting a ratification it
    # had not made while corrupting attested prose. Tracking multi-line
    # delimiter state is what a line rewrite over TOML costs; the alternative
    # (re-serialising) costs the comments and the ordering. Two further refusals
    # land here too: an absent `status` key (absent is not "not Modified"), and
    # the newline style the file arrived with, preserved rather than normalised.
    # It also DISSOLVED the `toml-line-rewrite` census block — the scanner is no
    # longer bootstrap's, which is the honest reading of what changed.
    # +6 (1663 -> 1669), WI-424: every adjudication mint site now DECLARES
    # which brief it is asking for (one line each), plus the row projection.
    # The mint is what knows which judgement it wants; inferring it later
    # from SpecRef is provably ambiguous.
    # Then -8 (1669 -> 1661), WI-422 (the measured dead-symbol sweep): `_rev7` — WI-416 took title-token authority off the disposition mint
    # and left the resolver behind.
    # +9 (1661 -> 1670), WI-424 review round 2 (B3): the two report-less mint
    # arms (a cancellation, a clean-close spot check) now declare NO brief and
    # say why. A false declaration would page a human for routine work, because
    # a declared-but-uncomposable brief is a hold.
    "intake.py": 1673,  # +3 2026-08-13: WI-443 — the components/interfaces reads move to spine_carrier.load (reviewed bump, reason in the log)
}


def _census():
    """{module_name: line_count} for every kit script over THRESHOLD."""
    census = {}
    for path in sorted(pathlib.Path(SCRIPTS).glob("*.py")):
        lines = len(path.read_text(encoding="utf-8").splitlines())
        if lines > THRESHOLD:
            census[path.name] = lines
    return census


def test_module_sizes_exactly_match_the_committed_baseline():
    census = _census()
    grew = {
        name: (BASELINE.get(name), lines)
        for name, lines in census.items()
        if lines > BASELINE.get(name, 0)
    }
    improved = {
        name: (baseline, census.get(name))
        for name, baseline in BASELINE.items()
        if census.get(name, 0) < baseline
    }
    message = []
    if grew:
        message.append(
            "module(s) grew past baseline — decompose (WI-280), do not bump "
            "(a deliberate bump is a reviewed baseline edit, reason in the log): "
            + "; ".join(
                "{} baseline {} -> now {}".format(
                    name, base or "absent (new monolith)", now
                )
                for name, (base, now) in sorted(grew.items())
            )
        )
    if improved:
        message.append(
            "module(s) shrank below baseline — re-stamp these entries downward "
            "(or delete them if now <= {}) in this same commit: ".format(THRESHOLD)
            + "; ".join(
                "{} baseline {} -> now {}".format(
                    name, base, now if now else "under {}".format(THRESHOLD + 1)
                )
                for name, (base, now) in sorted(improved.items())
            )
        )
    assert not message, "\n".join(message)
