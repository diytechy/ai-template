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
    # +2 (2973 -> 2975), WI-381: the plain launch's entry follows the rename —
    # `_drive_entry` imports the sibling as `dispatch` (drive.py -> dispatch.py,
    # lane.py extracted; docs/concurrency-v2.md §A4.2) and its docstring names
    # the split. Two docstring lines, no logic. Reviewed bump, log fragment
    # 2026-08-02 (WI-381). Re-stamp down with WI-280.
    "agent_loop.py": 2975,
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
    "trace.py": 2930,
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
    "check_trajectory.py": 3428,
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
    "check.py": 1548,
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
    "bootstrap.py": 2267,
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
    "agent_common.py": 1792,
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
    # +1 (2125 -> 2126), WI-381: the refresh docstring names its two callers
    # after the split (the dispatcher's drain / lane.py's refresh subprocess)
    # — one comment line, no logic. Reviewed bump, log fragment 2026-08-02
    # (WI-381). Re-stamp down with WI-280.
    "integrate.py": 2126,
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
