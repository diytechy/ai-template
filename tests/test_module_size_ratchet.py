"""The no-new-monolith ratchet — repo-review-2026-07-22 H-2 (growth sensor).

The per-function complexity ratchet (test_complexity_ratchet.py) freezes how
hard any one function is to read. This is its file-scale sibling: it freezes how
large the kit's biggest scripts are, so the six coordinators the 2026-07-22 deep
review flagged as "beyond maintainable review scale" cannot silently grow while
the real decomposition is deferred.

THE DEBT OWNER IS `WI-521`, AND IT IS THE FIRST OWNER SCOPED TO THIS FILE'S OWN
AXIS. The chain, kept because it is the argument: this file directed its active
debt to `WI-280` for months after that item CLOSED, and WI-280's scope was the
dashboard plus `bootstrap.main` — not the remaining baseline. A ratchet whose
commentary names a closed item tells the next author that the debt is somebody's
when it is nobody's, which is the one thing a growth sensor must not do.
`WI-483` took the ownership then (repo review 2026-08-19, H-05) and CLOSED
2026-08-24 having paid down the axis it was scoped for — the seven-module import
cycle is gone, the lifecycle band is layered and asserted, and four
complexity-baseline entries were deleted — which is precisely NOT this file's
axis (see the dispute below). It handed the pointer to `WI-508`, the live
architectural-remapping program.

TWO THINGS ENDED THAT PATTERN RATHER THAN CONTINUING IT. First, a close-time
re-point is a PROMISE and a filed row is a FACT: it has been honoured once,
deliberately and with the defect named, and leaning on it again makes this
sensor's honesty depend on a future session remembering. Second, `WI-508` was no
better matched to this axis than its predecessor — it is a CONSOLIDATION program
(minimize duplicated behaviour) while this file measures module SIZE, which is
decomposition; it inherited the pointer for being the live architectural program,
not for being scoped to what is measured here. So `WI-521` was FILED to own the
axis, the pointer moved to it while `WI-508` was still open, and `WI-508`'s
eventual close now has nothing to re-point. `WI-521` carries the baseline below,
M-06's four test monoliths, and the requirements-side evidence for which modules
are wide and why — and if IT ever closes, the pointer moves in the same commit,
which is the rule it inherited.

Any kit script whose line count exceeds THRESHOLD must have an EXACT baseline
entry below. The census may only tighten by default:

- A baselined module grew, or a NEW module crossed THRESHOLD without a baseline:
  the fix is DECOMPOSITION (WI-521), not a baseline bump. A deliberate bump is a
  reviewed baseline edit whose reason lands in the WI/session log — never a
  drive-by. Moving lines into a new module is exactly the intended escape hatch:
  the new module stays under THRESHOLD (or earns its own reviewed baseline) and
  the shrunk one re-stamps downward.
- A module improved below its baseline (or dropped under THRESHOLD, or was
  renamed/removed): re-stamp its entry downward — or delete it — in the same
  commit, so the ratchet only ever tightens.

This is a growth SENSOR, not an approval of the current sizes. WI-521 is the
scoped row that pays this debt down; every entry here is active
architectural debt, not a target.

THE AXIS DISPUTE IS RULED (OI-68, 2026-08-30, ruled 1c). The owner's `OI-16`
correction — "the monolith risk was always about FUNCTION size and complexity,
not file length" — is honoured not by retiring this sensor but by RE-BASING it:
this file measures module SIZE and `tests/test_complexity_ratchet.py` measures
FUNCTION complexity, two axes both worth watching, and both stay armed. What the
re-base fixes is that a RAW line count over this tree partly measured
DOCUMENTATION (roughly half the kit scripts are comment and docstring by house
style), which is why WI-448 could demand a reviewed bump on `bootstrap.py` after
it shed two duplicated helper bodies and gained a MAPPING declaration block. So
`_all_modules` now counts SLOC — non-blank, non-comment, non-docstring — via
`check_complexity.module_sloc`, the one definition of a source line the
complexity sensor also reads. That shared definition is the ONLY axis the two
sensors now hold in common: they differ in BOTH what they measure AND which
files they cover. This size ratchet measures module SIZE over the kit scripts
only (`conftest.SCRIPTS`, recursing into packages since 2026-08-21); the
complexity sensor measures function COMPLEXITY and, since WI-538 widened its
`DEFAULT_INCLUDE`, also censuses `tests/`. The ruling kept this ratchet
scripts-only on purpose, so the trees genuinely diverge — do not read the shared
`module_sloc` as a shared census surface. Nothing was deleted and no pointer
moved: the ruling was arm-and-re-base, not retire. The debt owner is still
`WI-521`.
"""

import ast
import pathlib

from check_complexity import module_sloc
from conftest import SCRIPTS

# A module whose SLOC exceeds this must be baselined. RE-BASED 2026-08-30
# (OI-68 ruled 1c, WI-538) from 1500 RAW lines to 1000 SLOC: the axis moved from
# physical lines to code (see the module docstring and `_all_modules`), so the
# threshold moved with it. 1000 was chosen from the measurement the re-base itself
# supplies — the nine modules the raw-1500 census baselined score 1081–3364 SLOC
# (intake.py the smallest member at 1081), and the largest NON-member is
# traj_panels.py at 891, so any threshold in 900–1000 preserves EXACTLY that nine.
# 1000 re-stamps the current watch set onto the code axis without deleting an
# entry or admitting a new one, which is the ruling's "full re-stamp, nothing
# deleted". A routine edit to a mid-size script does not trip the ratchet; a
# mid-size script growing into a new monolith does. The live census is `_census()`.
THRESHOLD = 1000

# RE-BASED TO SLOC 2026-08-30 (OI-68 ruled 1c, WI-538). Every VALUE below is now
# SLOC (non-blank, non-comment, non-docstring), measured by
# `check_complexity.module_sloc` — NOT raw physical lines. The one-time raw->SLOC
# map, on record: trace 6005->3364, agent_loop 4100->2519, check_trajectory
# 4653->2223, bootstrap 3166->1571, integrate 2655->1265, agent_common 2690->1262,
# gen_arch_map 2230->1262, check 2466->1163, intake 1990->1081. The per-entry
# comments beneath each key are the RAW-LINE-ERA history — every `+N (a -> b)`
# delta is a raw-line delta — kept verbatim as the reviewed record the ruling
# preserves ("nothing deleted"); they are NOT rewritten to SLOC, because a dated
# record rewritten to numbers that did not exist on its date would falsify it.
# The raw deltas are history; the SLOC value on the key line is the live baseline.
# Re-stamp DOWNWARD as the decomposition program lands; an UPWARD re-stamp is the
# reviewed-baseline-edit escape hatch (see the module docstring) and must name
# its WI right here.
#
# THE DEBT OWNER IS NAMED ONCE, IN THE MODULE DOCSTRING, AND IT IS `WI-521`.
# Entries below carry dated notes that still read "re-stamp down with WI-280";
# those are RECORDS of the bump they sit beside — each names the log entry that
# reviewed it — and rewriting a dated record to cite an item that did not exist
# on its date would falsify it. They are not re-pointed for the same reason this
# repo does not restate a rule in five files: the owner has one home, above.
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
    # -1 (4633 -> 4632), WI-297 dedupe: the DevStg-Impl `dupes` step flagged the per-site
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
    # line per Drafted SR (approval owed) and per Modified SR (re-attest
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
    # ("attended", "single-approve") are no longer a vocabulary — the loop asks
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
    # +29 (3202 -> 3231) 2026-08-21, WI-491 (OI-46 ruled (2a)): the launch
    # banner surfaces `out/subagent-gate.log`'s tail count — a small
    # `_subagent_gate_log_count` reader (reading the log's literal filename
    # rather than importing `subagent_gate` for its `LOG_NAME`, to avoid a
    # new CMP-008 -> CMP-007 cross-component seam for one string) and one
    # conditional `print` in `print_run_banner`. Reviewed bump, reason in
    # docs/log.d/2026-08-20-program-grind.md.
    # Earlier: +40 (3162 -> 3202) 2026-08-21, WI-487: the back-link campaign — literal
    # `Implements:` declarations added near the symbols this module's own live
    # LLR rows already name (docstring/comment lines only, no executable
    # change). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md.
    # Earlier: WI-433 (the blackout ships DISABLED): +2 (3160 -> 3162). Two lines of the
    # module docstring's dial description — the scaffold's shipped value changed
    # and the sentence that stated it had to change with it, or the docstring
    # would assert a default the template no longer carries.
    # +9 (3231 -> 3240) 2026-08-21, review batch-close W-21:
    # `_subagent_gate_log_count` returns `(decisions, fail_open)` instead of a
    # bare total, and the banner prints both. OI-46 (2a) asked for the
    # fail-open allows to be VISIBLE, and one number cannot do that — 500
    # routine allows plus one fail-open reads exactly like 501 routine allows,
    # so the single event the ruling wanted surfaced was the one the count
    # could not distinguish. Reviewed bump, reason in
    # docs/log.d/2026-08-20-program-grind.md.
    # +222 (3240 -> 3462) 2026-08-23, WI-483 slice 5 — a DECLARATION bump on a
    # module that got structurally simpler, the `bootstrap.py` shape this
    # file's own header records as the owner's OI-16 counterexample. `main`
    # fell 402 -> 152 lines and OFF the complexity census (27 -> under 10); what
    # replaced it is five typed records (`LoopContext` frozen and total,
    # `LoopRun` its mutable half, plus `RoutingSetup`/`SessionSetup`/
    # `SessionPolicies`) whose 60-odd bare field declarations are the bump's
    # bulk, and thirteen extracted startup functions carrying the comments that
    # used to sit inline in `main`. The complexity ratchet — the axis this
    # program pays down — went DOWN by one whole entry. Reviewed bump, reason
    # in docs/log.d/2026-08-23-wi483-agent-loop-engine.md.
    # +152 (3462 -> 3614) 2026-08-23, WI-483 slice 6 — the same DECLARATION
    # shape, one slice later and smaller. `session_bookkeeping` (325 lines /
    # C901 31 — the kit's most complex surviving function) and `run_iteration`
    # (326 / 20) both fell OFF the complexity census; both entries are DELETED
    # in the same commit. The two functions themselves shed 651 -> 148 lines
    # between them, and what replaced them is twenty module-level functions
    # plus three frozen decision records (`PageConsequence`, `RoundSubstance`,
    # `LimitWait`) — signature lines and the docstrings that used to be inline
    # comment blocks are the whole bump. Reviewed bump, reason in
    # docs/log.d/2026-08-23-wi483-bookkeeping-engines.md.
    "agent_loop.py": 2519,  # +53 (4047 -> 4100) 2026-08-30, WI-535 (telemetry first, dial off): `family_context_telemetry` reads the session id and context occupancy/window/percent straight off the process's own JSON result, per family — no mint, no resume, no adapter — and `session_meta` gains the four columns it feeds. NEW BEHAVIOUR: today's one-shot ANTHROPIC calls already carry enough (`session_id`, `usage`, `modelUsage`) to compute this without any launch change; OPENAI/OPENCODE stay blank until a later WI's per-family adapter lands. Reviewed bump, reason in docs/log.d/WI-535-adjudicator-telemetry-first.md. Earlier: +425 (3622 -> 4047, post ruff-format + the composer extractions the policy/complexity guards asked for) 2026-08-30, WI-548 (the stall-guard plan C1/C2/C4/C5/C7): NEW BEHAVIOUR, not drift - the route-aware stall split (note_review_draw_failure + the judging arm), the C2 review-owed exit and its marker trio (write/clear/stop), the C4 liveness probe pair (probe_route/select_with_probe, kept beside the draw it guards), the C5 relaxed rung and its recording, and the C7 brief-slot resolvers (process_doc_path/trunk_name). Roughly half the bump is docstrings stating WHY each guard exists (the WI-521 incident); the engine gains no second responsibility. Reviewed bump, reason in docs/log.d/WI-548-stall-guard.md. Earlier:+8 (3614 -> 3622) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md.
    # +30 (2206 -> 2236), WI-065: `tc_citation_findings` — the TC-`Verifies`
    # rules lifted out of `analyze` so the cell could accept `IF-###` seam ids.
    # Most of the bump is that helper's docstring, which is where the RULING now
    # lives (one citation cell, not a second column) — the part a successor
    # would otherwise have to reconstruct from two disagreeing checkers. The
    # extraction also ratcheted `analyze`'s complexity DOWN 53 -> 50. Reviewed
    # bump, log 2026-07-25. Re-stamp downward with WI-280.
    # +381 (2236 -> 2617; the last +38 is the adversarial-review fix pass: F1 --since fail-fast, F4 BOM strip, F7 resolved-sha provenance, F8 ownerless-child warns), WI-316: the re-attestation brief (--approve modified)
    # — per-cell before/after for every Modified SR's chain against its
    # git-derived attested baseline (+ --since), the is_modified predicate, and
    # the two warn-tier lints (Modified-exempt status advisory; the
    # modified-chain orphaned-child warn). The brief is the sitting's
    # instrument — a sitting cannot bless a delta it cannot see — and rides the
    # existing --approve generator mode rather than a new surface. New
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
    # the docstring on `approval_check`, which records the constraint that makes
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
    # nonexistent successor, the Drafted-not-exempt statement). The shipped
    # guard the ruling asked for, not monolith drift. Reviewed bump,
    # log 2026-07-29. Re-stamp down with WI-280.
    # +14 (2895 -> 2909), WI-401: `sn_cited_ids` — the SN-Refs coverage parse
    # named so the SN-coverage gate rung's F5 duplicate in spine_rules.py has a
    # pinnable twin (test_rule_sync), plus the two seam comments tying the
    # orphan listing to the gate rung. Reviewed bump, log 2026-08-02.
    # +10 (2909 -> 2919), WI-402: phase_approved_findings tightens to
    # numeric-only (owner ruling 2026-08-01) — the docstring now records WHY
    # (the two literal joins a prefixed cell silently disarms, and the
    # grandfathering stance that keeps phase_num digit-extract), which is the
    # reason a successor must not "simplify" the rule back to the parse.
    # Reviewed bump, log 2026-08-02.
    # +11 (2919 -> 2930), WI-408 (WI-401 REVIEW-A finding 2): sn_all_ids — the
    # SN id-universe scrape, previously an inline one-liner duplicated in
    # spine_rules.py with NO test_rule_sync pin, extracted to a named twin so
    # the third SN policy duplicate is pinned like its siblings. The growth is
    # the docstring recording the whole-text sharp edge (an approved prose
    # mention caps the gate at DevStg-Below). Reviewed bump, log 2026-08-02.
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
    # approve sitting brief this module builds — the surface a human reads
    # BEFORE approving. The helper is verbatim in traj_parse and gen_okf too
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
    # `docs/trajectory-check: off`; as a DevStg-Impl step they would never run in a DevStg-Reqs
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
    # All 25 Modified rows would render as "awaiting its FIRST approval" and
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
    # that changed carrier has no `Approved` revision in it and all 25 amended
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
    "trace.py": 3364,  # +7 (5998 -> 6005) 2026-08-29, WI-534 (OI-67, the arms the split surfaced): DOCSTRING ONLY — IF-166's body (`docs/test/report.html`, the `--html` render medium beside IF-146's `report.md`) stated beside the code that writes it; no executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi534-if-arms.md. Earlier: +86 (5912 -> 5998) 2026-08-29, WI-533 follow-up (cross-family review F2 + F7): two holes in the IF tier's own integrity rules, both closed where the rule is decided. F2 — a row whose owner is `external:` AND whose far side names no in-tree endpoint passed every rule on the tier: the reachability advisory exempts an external owner (an external party has no design row), and that exemption was the row's LAST rule, so a crossing between two external parties sat here owing its definition nowhere — the armed gate states our reading of an external surface in the header of the kit module that FACES it, and such a row has none. It is now a strict finding beside the id-shaped-owner rule, with `_far_endpoints` (the far side as endpoints; both carriers hand a `;`-joined string, `value_to_cell` joining a TOML array on `;`). F7 — the retired-cell rule asked the wrong question twice: it tested the VALUE, per ROW, where the retired shape is the KEY'S PRESENCE and presence is a property of the REGISTRY. `_cell_present` is DELETED and `_retired_cell_findings` replaces it: one read through `spine_carrier.columns` (the union of keys rows set under TOML, the header under CSV — the one reader that answers "which columns does this registry use" for both carriers) and one finding per retired key naming the rows that carry it. That closes the live hole a value test leaves on the legacy CSV carrier, where a retired column sits in the HEADER of every row and stays silent as long as nobody fills it in. Roughly half the bump is the two docstrings: which mechanism owns the two shapes this rule deliberately does NOT re-check (`spine_carrier.load` already refuses an explicit-empty cell and a cell that is itself a table over every TOML registry, this tier included, so a second copy here would be a second copy of a rule that already fires), and why a row with NO far side is left to the warn-first advisory rather than double-reported. `interface_findings` LEFT the complexity census in the same commit (11 -> under the limit). Reviewed bump. Earlier: +14 (5898 -> 5912) 2026-08-29, WI-533 (OI-67 slice 6): `_IF_RETIRED_CELLS` + `_cell_present` and the strict retired-cell arm inside `interface_findings` (the five cells OI-67 took off the row are the wrong SHAPE wherever they still appear), `if_legacy_contract_advisories` DELETED (-19), and `structure_findings` reading through `kitlib.spine.csv_body` so a CSV owner's `#` declaration header is a header and not ten one-column rows. Net +14 after the deletion. Reviewed bump, reason in docs/log.d/2026-08-29-wi533-arm-the-gate.md. Earlier: +16 (5882 -> 5898) 2026-08-29, WI-531 (OI-67 slice 4): DOCSTRING PLUS A TWO-LINE COMMENT on `_IF_CONNECTIVE_RE` (a `--since` flag is not the connective) — the split rows of OI-67 slice 4 state their `Contract IF-###:` bodies beside the code (IF-145 the exit code the harness gates on, IF-146 the report medium; IF-127 and IF-116 collapsed into IF-075 and IF-101); no executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi531-if-row-split.md. Earlier: +55 (5827 -> 5882) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +8 (5819 -> 5827) 2026-08-29, WI-528 (OI-67 ruled (a)): net of a larger swap — the IF tier's id-typed owner rule (`if_ownership_advisories`), the `Req-Refs` back-link and the derivability pipe (`if_provider_advis`, its report section) LEFT with the cells they read, and `interface_findings` took their place with three rules: the far side is exactly one of `Requestors`/`Consumers` (strict), the owner is one THING and never an id (strict), and a module-shaped owner reaches a requirement through a design row or an `Implements:` line (warn, via `_implementing_modules`). The five form rules moved from `Contract` to `Data` unchanged. Reviewed bump, reason in docs/log.d/2026-08-29-wi528-if-row-shape.md. Earlier: +141 (5678 -> 5819; the pass measured +139 before `ruff format` reflowed one line of it) 2026-08-24, WI-518 (the off-spine census — docs/log.d/2026-08-24-oi62-rule-and-spine-approval.md, MAJOR-2): `intake.py snapshot` copies the off-spine tiers (`interfaces.toml`, `external.toml`, `components.toml`) wholesale, and `reattest_lines` had no rendering for them at all. Producers: `OFFSPINE_CENSUS_TIERS`, `_offspine_row_diff` (whole-row equality per off-spine FILE, not the spine's approved/traced cell split — a COUNT, not a cell-level attestation surface), `_offspine_ruling_pointer` (the `WI-###`/`OI-###` tokens in commits that touched the file since the snapshot), `offspine_census_rows` (the data half, consumed by both this module's markdown and `gen_open_items.py`'s HTML, the `reattest_model`/`reattest_lines` shape) and `offspine_census_lines` (the markdown renderer, wired into `reattest_lines` right after the derived stamps so it reaches the reader whether or not the SPINE window is open). Reviewed bump, reason in docs/log.d/2026-08-24-wi518-offspine-census.md. Earlier: +57 (5621 -> 5678) 2026-08-24, WI-514 (the SR-177 anchor-text gap): `truncate_cell` (a shared, explicit-marker truncation the HTML renderer imports rather than re-deriving), `_anchor_lines` (the anchor SR's own Requirement/Rationale, rendered unconditionally for every entry — the row shape `owes()`'s WI-513 widening still could not put on the page, because an `Approved`, undrifted SR with its whole amendment in a `Drafted` child never entered `entry["rows"]` at all), and the `truncate_cell` calls threaded through `_full_row_bullets`/`_cell_diff_lines`. Reviewed bump, reason in docs/log.d/2026-08-24-wi514-brief-carries-text.md. Earlier: +68 (5553 -> 5621) 2026-08-24, WI-513 (the OI-61-sitting owes() gap): `owes()` gained the chain-wide `Drafted` arm and its explanatory comment, `_entry_kind` was re-signatured to answer for the whole chain (not the SR alone) with its docstring's new paragraph, the row-building loop grew the `drafted` flag/state on every branch (added/changed/removed/no-baseline), and `reattest_lines`' markdown renderer gained the `state == "drafted"` arm plus the `Drafted, never approved` suffix on `added`/`changed`. Reviewed bump, reason in docs/log.d/2026-08-24-owes-widening-and-b-brief.md. Earlier: +229 (5324 -> 5553; the pass measured +228 before `ruff format` reflowed one line of it) 2026-08-24, WI-512 (OI-61 ruled (d) plus its sub-question): the FIFTH `Contract` rule — the first on this tier that reads CONTENT rather than form — and the `VerifiedBy` resolution rule. Producers: the four token grammars (`_IF_CALL_RE`/`_IF_DOTTED_RE`/`_IF_CONST_RE`/`_IF_PATH_RE` plus the filename-tail set), `contract_symbol_surface` (the guarded `gen_arch_map.implements_report` read), `_symbol_resolves`, `contract_named_tokens`, `_if_named_symbol_advisories` and `if_verified_by_advisories`. DECOMPOSITION WAS CONSIDERED AND DECLINED, which this hatch exists to record: the pure half (the regexes, `contract_named_tokens`, `_symbol_resolves`) would sit honestly in `trace_text.py` beside `if_provider_advisories`, but it would put four of one rule-family's five members in a different module from the four form rules they extend and from the constants block that documents all of them — and the other half genuinely cannot move, since it reads the AST surface and the tree exactly as `if_endpoint_class_advisories` above it does. Roughly half of the +228 is the recorded WHY, and it is load-bearing in the specific way this ratchet allows for: every narrowing in `_symbol_resolves` is a false-positive class the rule DECLINES to invent (another library's symbols, the registry's own column notation, English slashes, a filename read as an attribute), each of which fired on the live registry before it was narrowed — 39 findings became 7, and the one the rule was ruled for (`SCHED_*`) survived every narrowing. Reviewed bump, reason in docs/log.d/2026-08-24-wi512-contract-generalization.md. Earlier: Reviewed bump, reason in docs/log.d/2026-08-23-wi455-rename-and-shed.md. +2 (5322 -> 5324; the pass measured +5 before `ruff format` reflowed three lines of it) 2026-08-23, WI-455: the IF tier sheds `Direction`/`ThisProject`/`Counterpart` for `Provider`/`Consumers` — the schema and enum blocks lose a column each, and the two endpoint advisories gain the module-shaped filter the `Provider` cell needs (it legitimately holds a file medium or an `external:` party, where "matches no LLR Module" is noise by construction). Earlier: Reviewed bump, reason in the log. +6 (5316 -> 5322)
    # 2026-08-23, WI-511: `_wi_ids` now scans `kitlib.registry.spec_roots`
    # (docs/work AND its docs/archive/work sibling, WI-504's relocated
    # terminal history) instead of hardcoding `docs / "work"` — a spec minted
    # and closed to the archive in one commit was an id the watermark's own
    # live-id justification could not see, refusing an honestly-justified
    # mark rise with no way to satisfy it short of a second commit.
    # RE-STAMPED DOWN -57 (5373 -> 5316) 2026-08-23, WI-483
    # slice 4 (program shape item 5, the engine splits): the cross-row join
    # rules left for the new sibling `scripts/coherence.py` (425 lines, under
    # THRESHOLD, no entry of its own) — the four-tier orphan rules,
    # `tc_citation_findings`, the PB/REPO/CMP back-link and membership
    # resolutions, the knowledge-pack resolution, the `PhaseScope` delivery
    # filter and the `--require-verified` status criterion. This is the escape
    # hatch the docstring names, and it is a NET shrink DESPITE the slice also
    # typing two attribute bags: `Registries` became a frozen dataclass and
    # `Findings` a mutable one, which costs ~75 declaration lines this file
    # counts and buys the guarantee that a field cannot spring into existence at
    # a call site (the two `getattr(reg, ..., [])` defensive reads are gone).
    # Earlier: -87 (5460 -> 5373) 2026-08-23, WI-448
    # slice 3: the spine ROW vocabulary this module duplicated against
    # spine_rules.py — `load_csv`, `is_approved`, `is_founded`, `LLR_EXEMPT` +
    # `llr_exempt`, `phase_num`, `sn_all_ids`, `sn_cited_ids` — moved to the one
    # shipped home `kitlib/spine.py` and became eight re-export lines under one
    # comment block; `sn_draft_ids`'s wrapper became a direct bind to the
    # carrier. Recorded DOWN in the same commit rather than left as headroom,
    # per this file's rule. Reason in
    # docs/log.d/2026-08-23-wi448-spine-policy-pair.md.
    # Earlier: +1 (5459 -> 5460) 2026-08-23, WI-505: the two
    # `--approve` brief headers gain the ruled generated-header wording
    # ("GENERATED ... — do not hand-edit; cite ...", OI-56 (a)) — one word
    # each, reason in docs/log.d/2026-08-23-wi505-staleness-headers.md.
    # Earlier: +2 (5457 -> 5459) 2026-08-23, WI-499: ruff format re-wrapped two lines the rename lengthened; zero semantic change. Earlier: +96 (5361 -> 5457) 2026-08-22, WI-503: the re-attestation brief splits into a regenerated CURRENT.md plus immutable dated briefs. New: current_approval_brief (the fixed-name replacement for newest_approval_brief), mint_approval_brief + its CLI body (--mint-approval-brief/--mint-date), and the writer-mode exit-code fix (a WRITER failure now sys.exit()s instead of a bare return main() never reads). Reviewed bump, reason in docs/log.d/2026-08-22-wi503-approval-brief-split.md. Earlier: RE-STAMPED DOWN -8 (5369 -> 5361) 2026-08-22, WI-448 slice 2: the local `_utf8_console` body became a one-line import of the shipped `kitlib.config.utf8_console`. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +4 (5365 -> 5369) 2026-08-21, WI-498 slice 5 recovery: DOCSTRING ONLY, zero executable change — two half-applied sweep sites where the mechanical `derive_gate` -> `spine_rules` rename was applied to a sentence naming a symbol the SAME slice deleted, which is strictly worse than the stale name it replaced: it points a reader at a live module for a function that is not in it. Both now name the mechanism that actually carries the rule today — OI-30 D2 stands on the stage axis as an ABSENCE (`spine_stage` returns the Release rung for nothing), and LLR/TC `Drafted` is read by `spine_rules.spine_stage`, not by the deleted `sr_bar`/`maturity_gate`. The +4 is the two corrections costing a line each plus the rewrap; a symbol citation that cannot be resolved is the defect this repo's F5 pin culture exists to prevent, so it is paid for rather than trimmed. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +191 (5174 -> 5365) 2026-08-21, review batch-close W-1:
    # HARDENING THE VERB THE PREVIOUS STAMP BOUGHT, and the growth is the same
    # pipe again rather than a new concern. The 2026-08-21 adversarial round
    # executed four attacks against the correction record and all four were
    # ACCEPTED (hand-typed record; chained second correction; a ruling that does
    # not exist; a second record erasing the first from the parse). The record's
    # authority now resolves OUTSIDE the file it guards, which is what costs the
    # lines: `parse_corrections` + a list-valued `read_corrections` (the record
    # is append-only), `ruled_open_item_texts` + `_ruling_names` (the cited id
    # must be a `ruled` open item naming the space AT the corrected value —
    # value, not space, because OI-47's own prose mentions `SR=999` as census
    # noise and a space-only rule would have authorized the forged SR raise),
    # `_one_correction_findings` / `_correction_record_findings` (the standing
    # arms, which run whether or not a mark moved — a forged raise
    # self-justifies from the NEXT commit, so a check that only ran at the
    # raising commit went quiet exactly one commit too early), and
    # `committed_corrections` (the git baseline that makes a committed record
    # immutable). Roughly half the bump is the reasoning above stated where the
    # next reader hits it. Decomposition is NOT indicated: every one of these is
    # a watermark rule sitting inside the watermark section beside the four it
    # joins, and the module's split axis (`trace_text.py`) takes PURE row
    # predicates — these read two files and git.
    # Earlier: +181 (4993 -> 5174; the last +2 is `ruff format` unwrapping
    # one call after the stamp, the WI-473/WI-483 trap hit again — measured
    # POST-format) 2026-08-21, WI-492: OI-47 ruled (e) —
    # the recorded-correction verb. THE SAME PIPE, NOT A NEW CONCERN:
    # `read_corrections`/`correct_watermark`/`_cmd_correct_mark` sit directly
    # beside the `read_watermark`/`bump_watermark`/`_cmd_bump_ids` triple they
    # extend, so this is wiring living where its pipe already lives — the shape
    # every watermark entry below already establishes. Roughly half the bump is
    # the two docstrings recording WHY a correction is matched by the EXACT
    # `(was, now)` pair rather than by ruling id alone (a bare ruling-id match
    # would let one ruling justify an unbounded climb, not the single correction
    # it actually authorized — the replay this verb exists to refuse) and why
    # `correct_watermark` never reads `live_max_ids` (a correction is not an
    # allocation and must not be justifiable by one, or the one-shot guard would
    # be gameable by minting a live row first). 14 of the 181 are a DECOMPOSITION
    # inside this same file, not a size increase to defend: `main`'s two writer
    # flags (`--bump-ids`, `--correct-mark`) moved into a `_writer_mode` helper
    # so the dispatcher's own McCabe count stayed at the ceiling rather than
    # crossing it (the `resolve_plan`/`floor_notice` WI-473 precedent, applied
    # here rather than argued past). Reviewed bump, reason in the log. Earlier +4 (4989 -> 4993) 2026-08-21, WI-490: OI-45 rules (b) RETIRE
    # THE MECHANICAL-APPROVAL ARM — `is_founded`'s docstring stopped calling
    # "whether an authored `Founded` is itself an error" open. D-9 consequence 2
    # SPLITS: whether a tool ever WRITES the cell stays open, but whether an
    # AGENT-authored `Founded` is an error is answered (sanctioned, under the
    # declared human-approval level). Docstring-only, no predicate moved.
    # Reviewed bump, reason in the log. Earlier: +28 (4961 -> 4989) 2026-08-21, WI-487: the back-link campaign — literal `Implements:` declarations added near ten already-anchored symbols (docstring/comment lines only, no executable change; two of the twelve ids first placed here — both LLR-005 — were removed at the same close as a dishonest tag: its registry `code_symbol` names a function-local, not a real module-scope binding, so no placement in this file honestly carried it). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +200 (4761 -> 4961) 2026-08-20, WI-484: the hats layer joins the checker. THREE PRODUCERS PLUS WIRING, and the producers are why this is not a trace_text.py split: `load_hat_names` READS A FILE (the roster's table keys), so it belongs in the loading layer beside `load_provenance_allow` and cannot live in the pure-row-predicate sibling; `hat_findings` is a RESOLUTION over a second registry, the exact shape of `sr_boundary_findings` twenty lines up, and moving it would put one registry-resolution rule in a different module from its siblings; `effective_hats` is a join over SR parents, which needs the parent index this module builds — and it is CALLED, not reserved: the coverage arm counts EFFECTIVE sets, so a design row inheriting its parent's hats is covered rather than reported unattributed (the reading that would otherwise push authors toward the copy-down the derivation forbids; 220/237 by cells vs 178/238 by effective sets on this repo's own spine). Roughly two thirds of the bump is reasoning a sitting must be able to overturn: why a SECOND reader of hats.toml is safe (it answers "is this name declared" — `hats.py` stays the sole validator of roster CONTENT — and the import that would have avoided it runs against the declared crossing, which would mint a component-level cycle to save a tomllib.load), why the coverage arm is advisory forever while the resolution arm gates immediately, and why BOTH advisories are gated on the cell being in use (a fresh scaffold ships 16 hats and no Hat-Refs, so an ungated pair greets a first-run adopter with sixteen perspectives called ceremony). The report section is a `_hat_report_section` helper rather than a branch in `render_report`, following `_frame_report_section`: that assembler sits at the complexity ratchet's ceiling, so the section that renders conditionally lifts out of it — the C901 census is UNCHANGED by this WI as a result. `exit_code` gains ONE arm, deliberately: a dangling hat name is a dangling reference and gates like every other. The honest reading remains that trace.py owes a decomposition for its SIZE (WI-280), not for this WI. Measured POST-`ruff format`, which reflowed one call in this session's own edit after the first stamp — the same trap the WI-483 entry records. Reviewed bump, reason in the log. Earlier: +3 (4758 -> 4761) 2026-08-20, WI-448: same as check.py — `_git_out` shed to `kitlib.git`, the guarded import added, `subprocess` no longer imported here. Reviewed bump, reason in the log. Earlier: +127 (4631 -> 4758) 2026-08-20, the batch-close iterate pass (adversarial round: ROUND-OPUS CRITICAL-1/3, MAJOR-4/6/11, MINOR-19). FIVE separate corrections, and the reason they land together is that they are one finding chain — the approval record's arming, its writer's authority, its brief's provenance and its exception surface's honesty. Executable delta ~30 lines: the committed-mirror producer joins the existing integrity pipe (3 lines), `approval_stamp` renders beside the baseline stamp in the re-attestation brief (14), `_DERIVED_STAMP_PREFIXES` + `_without_derived_stamps` exclude both derived lines from `approval_check`'s freshness compare (11, and it DELETES a false-red that fired on every commit), and `read_provenance_allow`/`provenance_allow_parse_findings` split the allow parse into entries + UNPARSED so a dropped line is reported rather than silently counted as zero (~35). The rest is the reasoning a sitting must be able to overturn: why the committed mirror compares at each copy's OWN WRITING COMMIT rather than against the working tree (the working-tree form reds every pending amendment, and that lag IS the signal — the rule that would have been wrong), why the brief's stamp line said something `stamp()` cannot know, and why parse honesty is integrity-class. `exit_code` untouched. The honest reading remains that trace.py owes a decomposition for its SIZE (WI-280), not for this pass. Reviewed bump, reason in the log. Earlier +116 (4515 -> 4631), WI-485 (OI-41 ARM 1, ruled 2026-08-20): the allow-file entry grammar gains a REQUIRED `OI-###`, checked on the always-on integrity floor. WIRING PLUS ONE PARSER, and the parser is why it is not a decomposition: `load_provenance_allow` already read this file here, in the LOADING layer, and the finding must turn on the SAME parse as the suppression or the grammar that reports and the grammar that silences drift apart — so `parse_provenance_allow` REPLACES that reader's body and `load_provenance_allow` becomes a one-line key-set view of it. Moving the pair to a sibling would put the exception reader in one module and the exception CONSUMER (`is_allowed`, the six advisory call sites) in another. The other two arms of the same ruling deliberately did NOT land here: the session-log declaration and the vacuity count live in gen_open_items.py (1060 lines, under THRESHOLD — the escape this ratchet documents), which is the surface they report on. Roughly two thirds of the bump is docstring: why the id is a POSITION rather than a mention, why a field ships hard where the sibling arms ship warn-first, and why the row's STATE is not an arm here (ruled-but-unexecuted is a legal transient, and the count contradiction it can hide is ARM 3's, which names the same entries once rather than twice). `exit_code` untouched — the findings join the existing integrity pipe at its existing severity. The honest reading remains that trace.py owes a decomposition for its SIZE (WI-280), not for this WI. Reviewed bump, reason in the log. Earlier +5 (4510 -> 4515), WI-466: the verified-triple summary-line fix. The print guard read `(demonstrated_verified or attested_verified)`, so a nonzero mechanized-only count — the common case — silently dropped the whole triple once the other two legs drained to zero (found live at re-tier v2 S3, log 2026-08-16e, when SR-034/SR-036 flipped Modified and took the registry's only demonstrated-verified rows with them). The guard now reads `(mechanized_verified or demonstrated_verified or attested_verified)`; the +5 is that widened condition plus the four-line comment recording WHY (a bare fix here would read as arbitrary to the next reader who has to decide whether zeros-included is safer). Display-only, no gating logic touched. Reviewed bump, reason in the log. Earlier -1 2026-08-20, WI-476 (M-07): ruff's F841 flagged `exts, bifs, rels = reg.exts, reg.bifs, reg.rels` in render_console as dead — that unpacking was never read again in the function — so the line is deleted rather than suppressed; a real shrink, re-stamped down in the same commit per this file's own rule. Earlier -4 2026-08-20 (same act): ruff format normalized the step-7 edits after the stamp — measured post-format, recorded down. Earlier +77 2026-08-20: D-9 migration steps 7+8 — `Modified` retires and `Founded` arms, in one act because the enum must equal the live predicate set at every commit. NET of a DELETION: `is_modified` goes, `is_founded` arrives, so the executable delta is ~4 lines (the predicate swap, `llr_status_advisories`' exemption, `reattest_model.owes` losing an arm, `--require-verified` accepting the newly armed value, and the two-line arming of the approval-record pipe). The rest is the reasoning a sitting must be able to overturn, and it is the expensive half BY DESIGN: why the marker could only retire AFTER its snapshot-backed successor had run live beside it through the owner's signing act (the ordering that makes this safe is invisible in the diff), why the UNANCHORED rule and the MIRROR invariant arm together as ONE integrity pipe rather than two, why arming a word may not LOWER a derived gate, and why the `--approve modified` CLI scope deliberately did NOT move with the value. Reviewed bump. Earlier +32 2026-08-18: the citation-frame detector corrected against two adversarial reviews (log 2026-08-18n). WIRING plus the exception reader: three import entries across both blocks; `load_provenance_allow`'s docstring recording the MEASUREMENT that forced token scope — the cell-scoped key was hiding 67 unadjudicated tokens over 22 live rows behind entries that each justified one parenthetical, while docs/test/report.md asserted none existed; `if_note_advisories` filtering per token instead of per cell; and the off-spine (CMP/EXT) join with the comment recording why those tiers share the spine's counter rather than taking a pipe of their own. The predicates live in trace_text.py, which stays at 1344 lines under THRESHOLD — the escape this ratchet documents. `exit_code` untouched: the advisory tier cannot gate and the gating class-1 rule keeps its severity, only its message text moved. Earlier +108 2026-08-18: the provenance ruling — NO citation frame in a living registry cell (owner ruling, in-session). WIRING plus ONE LOCAL PRODUCER, and the split is deliberate: the spine predicate is pure and lives in trace_text.py (`provenance_advisories`, which stays at 1162 lines, under THRESHOLD — the escape this ratchet documents), so this module gains only its join (the two import entries, the analyze() call with its comment, one Findings field, its two readbacks, the report.md section with its "None." fallback, the render_console loop entry). The producer that could NOT move is `if_note_advisories` (~40 lines with its docstring): it is an INTERFACE rule composing with the interface rules already in this file, and moving it would put half the IF tier's checks in another module — the same reasoning the WI-442 frame entry records below. The rest is `load_provenance_allow` (~28 lines), the reviewed exception reader for `docs/provenance-allow`, placed in the LOADING layer beside the other file reads because an exception list is an input to load, not a finding — analyze() stays pure. Most of both docstrings is the reasoning a sitting must be able to overturn: why the list is not a second home for provenance, and why the IF reason cells are a separate arm from the Contract arm (a `Notes` cell that ARGUES is that cell working correctly, so the Contract connective and 500-char rules must not follow it there). `exit_code` untouched, so the advisory tier physically cannot gate — the three pre-existing gating class-1 findings keep their severity exactly. The honest reading remains that trace.py owes a decomposition for its SIZE (WI-280), not for this ruling. Reviewed bump, reason in the log (2026-08-18 provenance-rule fragment). Earlier +26 2026-08-18: the artifact-voice rule reaches the NEED tier (owner directive, log 2026-08-18k) — WIRING ONLY, the sixth time this exact shape has been recorded here. The predicate is a pure row rule and lives in trace_text.py (`sn_artifact_advisories`, which stays at 983 lines, well under THRESHOLD — the escape this ratchet documents); this module gains only the join — the two import entries, the analyze() call with its comment, one Findings field, its two readbacks, the report.md section with its "None." fallback, and the render_console loop entry. The extra ~6 over the usual wiring cost is `load_registries` keeping the needs WHOLE (`reg.sn_needs`) beside the two-key `raw_sns` projection, with the comment recording why: a text rule fed the projection — or `folded_needs` — scans a blank cell on every row and reports a clean tier it never looked at, which is the same trap the +33 entry below records one rule over. Zero deleted lines. `exit_code` untouched, so the advisory tier physically cannot gate. Reviewed bump, reason in the log (2026-08-18k). Earlier +33 2026-08-18: the SN enum-floor gap closes (log 2026-08-18h) — `load_registries` projects needs into the `SN-ID`/`Status` shape (`raw_sns`) and `analyze()` folds `enum_integrity_findings` over SN BESIDE `raw`, not into it (`raw` also feeds the id-integrity and placeholder sweeps, which `sn_integrity_findings` already owns for the need tier). The declared `ENUM_FIELDS["SN"]["Status"]` finally has a mechanism: `status = "Bananas"` on a need was silently approved at every bar. Deliberately NOT read through `spine_carrier.folded_needs` — the fold projects onto SN_CORE, which has no `status` key, so a check reading it passes vacuously; the comment in place records the trap. Reviewed bump, reason in the log (2026-08-18h). Earlier +20 2026-08-18 (merge of the EARS branch into the pre-brief pass): the EARS statement-pattern advisory (log 2026-08-18a) — WIRING ONLY, the fifth time this exact shape has been recorded here. The predicate is a pure row rule and lives in trace_text.py (`ears_advisories`); this module gains only the join — the two import entries, the analyze() call with its comment, one Findings field, its two readbacks, the report.md section with its "None." fallback, the render_console loop entry and the summary counter. Zero deleted lines. `exit_code` untouched, so the advisory tier physically cannot gate. The two branches re-stamped this entry independently (+20 here, +16 below) and the merged file carries BOTH changes, so 4239 is the measured sum rather than either stamp. Reviewed bump, reason in the log (2026-08-18a). Earlier +16 2026-08-18: +16 2026-08-18: the desk round's F11 and F12. F12 (+12): `sr_chain_drifts`' docstring conceded that a `Modified` child "never counts as drifted", which — after the 2026-08-17m ruling retired `modified_chain_advisories` WHOLE — read as an admission that the retired "no resolvable owning SR" arm had no successor. MEASURED on a planted tree instead of reasoned about: the ORPHAN rules already cover every sub-case and GATE under `--strict`, where the retired arm only warned, so nothing is owed. The bump is that measurement recorded in place, because the next reader of this docstring would otherwise rebuild a detector the repo already has — the same regenerate-a-retired-thing failure the entries below record. F11 (+4): `render_watermark`'s — `render_watermark`'s generated header promised "the highest id ever allocated in each space" UNSCOPED, while `EXT = 5` is correct only for the v2 numbering and `external.toml:82` cites v1 EXT-005/007/008 in a live cell, so the next three EXT mints re-point ids the same file names. The header now SCOPES the guarantee to the space as currently numbered and sends superseded numberings to the registry, which is where they can actually be recorded. Prose-only, in the one place every adopter reads it (the shipped `id-watermark.template` carries the same lines). Reviewed bump, reason in the log (2026-08-17w). Earlier +25 2026-08-17: the sitting-3 item-17 ruling (log 2026-08-17n) — the depth-0 frame tiers B/EXT/REL join WATERMARK_SPACES and external.toml joins `_offspine_ids`' sweep (three registry rows plus the comment recording why — the same mint-lands-WITH-its-guard shape as WI-454's +9 below), the missing-space finding gains the fix command it lacked, and `_mark_history_findings` gains the first-seed exemption: a space's FIRST committed mark is a SEED that may stand above max(live), because the ids it must cover include rows deleted before the space was guarded (B-06/B-07, cut 2026-08-16q) — most of the bump is that reasoning recorded in place, and over-seeding is the fail-safe direction (wastes numbers, never re-points history). Reviewed bump, reason in the log (2026-08-17n). Earlier -90 2026-08-17: owner ruling 2026-08-17m (the cell reading) — `modified_chain_advisories` retired WHOLE (function, call site, report-fallback clause): it told an author to flip the parent SR for a child amendment, and the ruling says a child flipping never impacts the parent — a `Modified` child under an `Approved` SR is a legitimate cell-level state, surfaced by the snapshot-drift arm once seeded, not by invalidating the parent's signature. Its complexity-ratchet entry retired with it; recorded down rather than left as headroom. Earlier +18 2026-08-16: the verification-coherence advisory (log 2026-08-16p) — WIRING ONLY, the fourth time this exact shape has been recorded here. The predicate is a pure row rule and lives in trace_text.py (`verification_coherence_advisories`, which stays at 819 lines — well under THRESHOLD, the escape this ratchet documents); this module gains only the join — the two import entries, the analyze() call, one Findings field, its two readbacks, the report.md section with its "None." fallback, and the render_console loop entry. Zero deleted lines. `exit_code` untouched, so the advisory tier physically cannot gate. NOT DECOMPOSABLE further: one producer joining an existing pipe in the module that owns the pipe (the 2026-08-15j and re-tier v2 S2/S5 precedents below). The honest reading remains that trace.py owes a decomposition for its SIZE (WI-280), not for this WI. Reviewed bump, reason in the log (2026-08-16p). Earlier +2 NET 2026-08-16: re-tier v2 S5 (WI-464) — WIRING ONLY for the ThisProject-derivability advisory (`if_this_project_advisories`: an IF row's owner-side endpoint disagreeing with its owner LLR's `Module`, the pre-condition for DROPPING the column at wi455). The predicate is a pure row rule and lives in trace_text.py with its two helpers, per the WI-329 decomposition; this module gains only the join — the import entries, the analyze() call, one Findings field, the report.md section with its "None." fallback, and the render_console loop entry. The net is +2 rather than +24 because the SAME change MOVED three definitions OUT to trace_text.py (-22): `_MODULE_EXTS`/`_norm_module` (the predicate compares the same two module-naming conventions, so the alternative was a FOURTH copy of the normalizer) and `EXTERNAL_ENDPOINT_PREFIX` with its rationale block (the endpoint value grammar is a text rule, and `_module_shaped` has to skip a marked endpoint too). trace.py imports all three back and keeps `_norm_module` as a local alias, so no call site moved; trace_text.py stays well under THRESHOLD, which is exactly the escape this ratchet documents. `exit_code` untouched, so the advisory tier physically cannot gate. Reviewed bump, reason in the log (re-tier v2 S5). Earlier +36 2026-08-16: re-tier v2 S2 (WI-464, log 2026-08-16d) — WIRING ONLY for the two one-decision tiering advisories. The predicates themselves live in trace_text.py, honouring the WI-329 decomposition (`sr_artifact_advisories` + `sr_fanout_advisories` are pure row predicates in the sibling, which stays under THRESHOLD); this module gains only the join — the import pair, two Findings fields, the analyze() fill, the two report.md sections with their "None." fallbacks, and the render_console loop entries. Zero deleted lines; `exit_code` untouched, so the advisory tier physically cannot gate. Not decomposable further: this is two producers joining the pipe in the module that owns the pipe (the 2026-08-15j precedent directly below). The honest reading remains that trace.py owes a decomposition for its SIZE (WI-280), not for this WI. Reviewed bump, reason in the log (2026-08-16d). Earlier +16 2026-08-15: the sitting sweep's M3 fix (owner-ruled) — the chain-consistency advisory and its two docstrings stop claiming the amendment is "invisible to the re-attest sitting" on the old grounds and state the REAL mechanism instead: `is_drifted` fires only for a row whose live Status claims approval, so a `Modified` child under an `Approved` parent is caught by NEITHER the marker arm nor the drift arm — the second read's M3 verdict INVERTED when D-9's fold deleted `is_planned`, and the bump is the reasoning that stops the next reader re-discharging a warn that is now true by construction. Reviewed bump, reason in the log (sitting-sweep entry). Earlier +15 2026-08-15: D-9 migration step 5 — THE RENAME (log 2026-08-15m). The words moved (`Draft`->`Drafted`, `Verified`/`Planned`->`Approved`, `Planned` FOLDED per OI-30 D1) and `is_planned` was DELETED rather than re-keyed, so the net is small; the bump is the reasoning that has to travel with a rename a review sitting must be able to overturn — why `Modified` survives to step 7, why the retired words are named in place rather than silently gone, and (in `spine_rules`) why `maturity_bar` re-keys onto the ONE ladder table with a spine-only default so the rename cannot lower the derived gate. Reviewed bump, reason in the log (2026-08-15m). Earlier +27 2026-08-15 (log 2026-08-15j): adversarial round 2's F2 — `unanchored_findings` was DEFINED AND CALLED BY NOTHING, so an approval could bypass the `last_approved` record and no live check would say so. It is wired here as an ALWAYS-ON ADVISORY pipe (`findings.snapshot_advisories`), filled after `analyze()` for the same reason the id-watermark rules are: it reads the filesystem, and `analyze()`'s "Pure … No I/O" contract is only worth having while it stays true. Roughly two thirds of the bump is the comment recording why the rule is advisory TODAY and armed at migration step 7 — a deferral that reads as a softening unless the reason (against a pre-seed or pre-rename snapshot it reds every row, and a check that reds everything gets switched off) travels with it. NOT DECOMPOSABLE: this is one producer joining an existing pipe in the module that owns the pipe. Reviewed bump, reason in the log (2026-08-15j). Earlier -47 2026-08-15 (log 2026-08-15h): the DEAD carrier-aware history readers `_rows_at` and `_toml_rows_text` are deleted, honouring the note the entry below left rather than letting it age into a reservation. Step 4 left them with no caller in any module and said so; a grep at this session found the only readers were their own three tests, which go with them. Nothing is lost: `check_trajectory._spine_rows_at` is the surviving `git show` reader and the cutover suite still exercises the D-5 hazard where the reader actually lives. Recorded DOWN rather than left as headroom for the next regression to hide in. Earlier +18 net 2026-08-15: D-9 migration step 4 (log 2026-08-15g) — the baseline moves out of git history and onto disk. DELETED: `_attested_baseline` (the walk for the newest still-`Approved` revision — dead BY CONSTRUCTION once an amendment stops flipping its row, which is what D-9 does), `_changed_cells` and its Approved->Modified suppression (retired, never re-keyed: `split_changed_cells` excludes `Status` structurally), `_DECLARED_BASELINE_RE` + `declared_since`, and the whole `--since` CLI surface — 108 lines out. ADDED: the drift selector (`sr_chain_drifts`), the snapshot-baselined model, the approved/traced two-group brief rendering, and the `_RESERVED_APPROVAL_SCOPES` closed set whose `_scope_srs` now REFUSES a scope matching nothing instead of emitting a brief that reads "nothing to approve" at exit 0. The net is nearly flat because most of what came out was code and most of what went in is the reasoning a sitting has to be able to overturn — including the block naming `_rows_at`/`_toml_rows_text` as DEAD rather than describing them as reserved, which is the mistake the retired `current_digests` docstring made. Reviewed bump, reason in the log (2026-08-15g). Earlier +123 2026-08-15: D-9 migration steps 1-2 (plan §A, log 2026-08-15g) — the `Status` vocabulary is CLOSED at its live truth and routed to the INTEGRITY floor rather than the schema tier, because `--strict-schema` runs only at DevStg-Impl and a closure that never executes below the top bar is a claim with no mechanism (correction C1). That is `STATUS_VALUES`, `INTEGRITY_ENUM_COLS`, the new `enum_integrity_findings` producer and the LLR tier's FIRST `ENUM_FIELDS` entry of any kind. Plus `is_planned` and `_entry_kind`: `Approved` sat on 14 live spine rows while no predicate in the kit recognized it — it read identically to `Bananas` — so the re-attest model gained a third kind rather than mislabelling approved-text-awaiting-evidence as a re-attest. Roughly half the bump is the docstrings recording WHY the enum closes at four values now and narrows later, and why the integrity pipe rather than the schema one; those are the numbers a review sitting has to be able to overturn. Reviewed bump, reason in the log (2026-08-15g). Earlier +136 2026-08-15: the interface rework steps 5+7 — the two checks the owner's rulings CREATED, both warn-first. `if_ownership_advisories` enforces "exactly one owner per interface" over a POLYMORPHIC id (Q1: an `SR-###` or an `LLR-###`, resolved against whichever registry the prefix names, because requirements and design rows decompose the same thing at different levels). `if_carriage_advisories` is the obligation Q3 created rather than an option taken: the moment a link may point at its own tier, `IF-A carried by IF-B carried by IF-A` is representable, so the carriage graph is checked to resolve, to be acyclic (reported once per row on the cycle, not once per traversal) and to stay inside a stated depth bound. Roughly half the bump is the two docstrings recording WHY the owner is not `Req-Refs` and why the depth bound is provisional — the numbers a review sitting has to be able to overturn. NOT DECOMPOSABLE INTO A SIBLING here for the same reason WI-442's frame tier was not: these are interface rules composing with the interface rules already in this file, and moving them would put half the tier's checks in another module. The honest reading remains that this file owes a decomposition for its SIZE (WI-280), not for this WI. Reviewed bump, reason in the log (2026-08-15e). Earlier +35 2026-08-15: the interface rework step 3 — `docs/declared-absences` gets its THIRD reader (`test_dogfood_sync` and `check_doc_refs` are the other two, and one-fact-one-home is the whole reason that file exists). An endpoint naming a declared absence is neither rot nor external: the layer is opt-in and switched off, and the row is honest about what the module would read if it were on. Worked case: `docs/requirements/performance-budgets.csv`, absent because §9's perf layer is off, reason already written down one directory up — naming it would have been the checker demanding the repo delete a true statement. Reviewed bump, reason in the log (2026-08-15e). Earlier +36 2026-08-15: the interface rework steps 1-2 (owner ruling 2026-08-15a, plan §4) — `Direction` joins ENUM_FIELDS carrying its RULED meaning (flow/coverage, never ownership: Q2), and the endpoint classifier stops GUESSING externality from spelling. The guess was the defect: anything without a slash or an extension "read as an external actor", so `agent CLI` was silently fine and `docs/subagent-gate` (a real path, dead since the policy moved to process.toml) was a finding — and a rot that happened to look like a name would have been silently fine too. The `external:` value-prefix replaces the guess with a claim someone made, and an unmarked unresolvable endpoint in EITHER column is now named. About two thirds of the bump is the comment recording why a prefix beat a column (rides the carrier, cannot drift from the cell it qualifies). Reviewed bump, reason in the log (2026-08-15e). Earlier +20 2026-08-14: WI-451 slice 2 act 5 — the ruled ASPECT closed vocabulary joins ENUM_FIELDS with the decision-10 reasoning that makes it readable (why 25 of 31 Area values were DROPPED rather than remapped, and why a blank cell is normal rather than a gap — a checker whose vocabulary looks arbitrary is a checker the next author widens). Reviewed bump, reason in the log fragment. Earlier -114 2026-08-14: WI-451 slice 2 — the SR-tier supersession machinery (sr_supersession_findings + its three helpers and the integrity-floor call) retired with the 26-row tombstone-class deletion (D-4 ruling 2026-08-14b); recorded down rather than left as headroom for the next regression to hide in. Earlier +9 2026-08-14: WI-454 — `_offspine_ids` learns the WI-443 TOML homes of interfaces + components: minting IF-121/122 past a mark of 120 produced NO finding, the exact vacuous-space defect class the function's own docstring records for OI-26, so the mint lands WITH its guard (two registry rows + the comment recording the find; reviewed bump, reason in the log fragment); earlier +260 2026-08-14: WI-442 — the depth-0 FRAME joins the checker: three tiers loaded off external.toml, their required-field/enum schema rows, the entity/crossing/tie-back resolution rules (`frame_findings` + `tieback_findings`, a --strict failure class of their own), SN-037's SR->boundary rule at its two severities (`sr_boundary_findings`: resolution hard, coverage a summary advisory) and the report section that reads them out. The last +21 is the adversarial round: the zero-entity false green becomes a finding, and three comments that overclaimed (a "costs nothing" that is six parses, a "the ONE collision" that is three) say what is true instead. REVIEWED BUMP, NOT A DECOMPOSITION, and the choice is stated rather than assumed: this file is already 2.4x THRESHOLD and has a split precedent (trace_text.py), so the ratchet's preferred escape was available and was NOT taken — the frame tier is ~90 lines of rules plus their reasoning, splitting it out would put the boundary checks in a second module from the spine checks they compose with, and the honest reading is that trace.py owes a decomposition for its SIZE rather than for this WI. Reason in the log; earlier +221 2026-08-13: WI-443 — the IF/CMP schema tier (required fields, closed vocabularies), the four IF Contract negative rules, and the untagged-endpoint classifier, all warn-first; +8 the adversarial round's refutation recorded in schema_advisories' docstring (reviewed bumps, reasons in the log)
    # +132 (1926 -> 2058; the last +10 is the F4 BOM hardening: read_rows utf-8-sig + git-show strips), WI-316: staged_spine_findings — the amend-without-
    # flip warn (--staged): content cells of an Approved spine row changed
    # without the Modified marker. (As written, this warn was SUPPRESSED when the
    # owning SR flipped in the same commit — the chain reading. That suppression
    # was DELETED by the 2026-08-17m cell ruling; the clause is kept in the past
    # tense because the -39 stamp below is what paid for its removal, and a
    # ratchet reason that silently re-describes retired behaviour as current is
    # the drift this file exists to prevent.) The write-time discipline the
    # RE-ATTESTATION-PENDING prose convention never had. Reviewed bump, log
    # 2026-07-26. Re-stamp downward with WI-280.
    # +5 (2058 -> 2063), WI-322: approval_brief_findings reads open-items ROWS
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
    # +93 (3098 -> 3191), WI-380: the §A5.1 approved-vs-traced cell split — the
    # two declared classification tables (one per spine registry, both halves
    # named), `spine_cell_class` with the fail-safe residual, the extracted
    # `split_changed_cells`, and the `staged_spine_amendments` seam WI-388
    # consumes. Most of the delta is the tables and the comment recording WHY
    # the residual falls to approved (a new column may be too loud, never
    # silently un-approved). The rule stays beside its only consumer for the
    # WI-349 reason — moving it to a sibling would separate a rule from the
    # single scan it governs. Reviewed bump, reason here and in
    # docs/log.d/WI-380-approved-vs-traced-cell-split.md. Re-stamp down with
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
    # docs/log.d/WI-380-approved-vs-traced-cell-split.md. Re-stamp down with
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
    # arch-map regeneration (SR-006), so a lane that adds a module reds its own
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
    # `SR-Refs` -> traced/routed, SR `SupersededBy` -> approved confirmed) —
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
    # `attestation_findings` (the DRIFT rung: an Approved row whose normative
    # text no longer digests to what was accepted), `attestation_integrity_
    # findings` (the ledger's own shape), `staged_attestation_rewrite_findings`
    # (append-only) — plus `normative_text`/`sn_normative_text`/`digest` and the
    # excluded-column contract that says WHICH cells are normative. This is the
    # biggest single bump the module has taken and it buys the anchor the whole
    # ordinal rests on: without a recorded digest, "has this been approved" is
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
    "check_trajectory.py": 2245,  # RE-STAMPED DOWN -2 (2247 -> 2245 SLOC) 2026-09-01, WI-552 close: ruff format canonicalization of this WI's own touched file; no executable change. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +24 (2223 -> 2247 SLOC) 2026-09-01, WI-552 (OI-70/OI-73): the typed OI-edge resolution (_predecessor_errors, load_known_ois, OPEN_ITEMS_REL) and dead_dependency_findings extending to partial (OI-73). Reviewed bump, reason in docs/log.d/WI-552-adjudicator-two-exit-close.md. Earlier: +15 (4638 -> 4653) 2026-08-29, WI-533 follow-up (cross-family review F1, CRITICAL): the armed gate was DISARMED BY ONE MALFORMED BODY. `_declaration_sites` caught `gen_arch_map.ContractsGrammarError` for the WHOLE scan and answered `(None, [])` — "there is no declaration surface" — so an empty `Contract IF-###:` opener anywhere in the tree silenced every other row's verdict, and the refusal itself was reported by nobody (reproduced: `--strict` exited 0 with byte-identical output to a clean tree). It now passes `scan_contracts` the per-source arm (`grammar_errors=`), returns the refusals as `problems`, and `contract_body_findings` emits the gate's FOURTH shape, one finding per refused source, at its own severity. A refused source is absent from `sites` rather than entered as declaring nothing, which would hand its rows to the reverse check's warn instead. Executable growth is ~10 lines; the rest is the two docstrings recording the fourth shape and why an UNREADABLE source stays out of `problems` (it is the reference's own list, and `arch_inventory`'s skip). `_file_owner_declarations`' own `except ContractsGrammarError` is NOT redundant and stays: it calls `file_contracts` directly for the reverse check, a different call path from this harvest. Reviewed bump. Earlier: +158 (4480 -> 4638) 2026-08-29, WI-533 (OI-67 slice 6): THE ARMED DEFINITION GATE — `_declaration_sites` (every declaring source through the one harvester the reference uses, modules keyed by normalized path and file owners as the registry spells them) and `contract_body_findings` (one rule, three shapes: declared-not-stated, an external-owned row no far-side module states, a stray declaration on a source that is not the owner; WARN plain, ERROR under --strict, the seam-TC promotion's idiom and opt-out), wired at the same call site. Roughly half the bump is the docstring recording what stays a WARN (an owner that declares nothing) and why. NOT DECOMPOSABLE as a unit: it is one rule over the loader and reverse-check surface this module already holds. `read_rows` now reads through `kitlib.spine.csv_rows` (a leading `#` header is a header). Reviewed bump, reason in docs/log.d/2026-08-29-wi533-arm-the-gate.md. Earlier: +36 (4444 -> 4480) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +78 (4366 -> 4444) 2026-08-29, WI-529 (OI-67 slice 2): the reverse check becomes OWNER-EXACT — `_owner_exact_findings` (a row's owner, module or file, must be the source that declares it; every inventory module judged, an `external:` owner skipped, an unresolvable owner falling back to the id-global read), `_owner_files` and `_file_owner_declarations` (the file owners' headers read through `gen_arch_map.file_contracts`, a grammar refusal reported and read as declaring nothing), and the marker-grammar honesty arm extended over the file headers. One checker, one seam rule; the id-global hole the OI-66 build round named is closed here. Reviewed bump, reason in docs/log.d/2026-08-29-wi529-header-non-python.md. Earlier: RE-STAMPED DOWN -2 (4368 -> 4366) 2026-08-29, WI-528 (OI-67 ruled (a)): `load_ifs` no longer takes the design tier's module map — the owner is the row's own cell, one spelling, nothing derived — and `load_seams` lost the join; the row now resolves its far side as `requestors`/`consumers` plus `far`, whichever is set. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +41 (4327 -> 4368) 2026-08-29, WI-527 (OI-66 ruled (a)): `_contracts_grammar_findings` reports the two lossy marker forms — a marker-shaped line whose id list will not parse, and a `Contracts:` carrying ids mid-line. It is here rather than in the generator because a detector nobody CALLS is the silent drop it exists to prevent, and this is the module that already walks the declared scan root for the docstring-vs-registry arm it sits beside. Degrades to silence on files-mode or a missing scan root, exactly as `arch_inventory` does. Reviewed bump, reason in docs/log.d/2026-08-29-wi527-contract-header.md. Earlier: RE-STAMPED DOWN -636 (4963 -> 4327)  # RE-STAMPED DOWN -636 (4963 -> 4327) 2026-08-25, WI-521 slice 1: THE FIRST PAYMENT ON THIS FILE'S OWN AXIS, and the module's own stamps had been asking for it — four of them recorded "whether `check_trajectory` is still ONE checker" as a live question and declined to answer it. The answer is no, and the cut is the one the REQUIREMENTS asked for rather than the one line count suggests: `acceptance_record.py` (758 lines, under THRESHOLD so it opens no entry) takes the two-tree spine comparison and the snapshot mirror — `SPINE_CSVS`/`SPINE_TRACED_CELLS`/`SPINE_APPROVED_CELLS`, `spine_cell_class`, `traced_cells`, `_spine_rows_at`, `_spine_revs`, `split_changed_cells`, `staged_spine_amendments`, `staged_spine_findings`, `staged_hat_refs_findings`, `_snapshot_survives`, `staged_snapshot_findings`, `_snapshot_write_revs`, `committed_snapshot_findings` — moved VERBATIM, 677 lines, plus a header. WI-508's two blind derivations each gave the acceptance record a module of its own (A's `A2`, B's `M06`) from the requirement text alone, and 8 of this module's 13 fused obligation pairs run through `SR-178`/`SR-179`; mechanically, `intake.py` and `baseline_snapshot.py` were each importing a ~5,000-line validator to reach it. The moved block's only non-builtin dependencies were `spine_carrier` and one git primitive, which is the seam being real rather than carved. Every name is re-exported here, so no caller moved and the CLI is byte-identical (6 driven paths + 60 API probes, capture-diffed empty against HEAD after the harness self-diffed empty twice). The remaining -8 against the bare 677 is the sibling import block, the re-export list, and `_git`'s body folding into `kitlib.git.git_out`. Reviewed re-stamp DOWN, reason in docs/log.d/2026-08-25-wi521-slice1-acceptance-record.md. Earlier: +60 (4903 -> 4963) 2026-08-25, WI-519: the allow-file parse-honesty arm carried to `docs/if-tc-coverage-allow`, the third of the three declared exception readers that dropped a malformed DECLARING line silently (`docs/provenance-allow` and `docs/kernel-modules-allow` already had the arm; this row extends it, without merging any of the five parsers). `_parse_if_tc_allow_full` is the whole parse (entries, seed, unparsed) behind `parse_if_tc_allow`'s pinned 2-tuple wrapper (kept exactly as it was: `test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set` unpacks it), and `if_tc_allow_parse_findings` is the new consumer, riding `if_tc_coverage_findings`' own `[checks] interfaces_check` opt-out and WARN-plain/ERROR-under-`--strict` severity (wired at the same call site, main()'s `if_tc_errors` block) — deliberately NOT its ≤1-module vacuity, since a malformed line is a fact about the file, not about whether the coverage rule currently has anything to say. Roughly half the bump is the two docstrings recording why the wrapper's arity could not grow. Reviewed bump, reason in docs/log.d/2026-08-25-wi519-allow-file-parse-honesty.md. Earlier: +23 (4880 -> 4903) 2026-08-23, WI-455: the IF tier's orientation moves INTO `load_ifs`, which now resolves each row into `provider` + `consumers` once (plus `load_seams`, the one live-registry call every seam view makes, so no consumer can forget the design-tier join and silently lose the derivable providers). `interface_findings` and `_declared_seam_pairs` got SIMPLER for it — the complexity ratchet records `interface_findings` 22 -> 20 in this same commit — and the bump is the two docstrings that have to travel with a schema change: which two keys replaced which three, and why the pairs are now taken across the row's whole endpoint set rather than across two named cells. NOT DECOMPOSABLE as a unit: it is one loader and one credit rule. Reviewed bump, reason in docs/log.d/2026-08-23-wi455-rename-and-shed.md. Earlier: +115 (4765 -> 4880) 2026-08-23, WI-484 phase 5: the amend-without-flip guard gains its `Hat-Refs` ARM — `staged_hat_refs_findings` (a row whose approved cells moved while its perspective record did not) plus `traced_cells`, extracted from `spine_cell_class` because the arm needs the SET rather than one column's class (an absent column classes `approved` under the fail-safe residual, so without it every amended test case would warn about a cell its registry does not have). The PREDICATE is ten lines; the rest is the two docstrings that have to travel with a warn-first rule — why the comparison is by CELL CLASS rather than by line (the measured blame-granularity defect one function over), which baseline was chosen and which was declined, and the two honest vacuities the population inherits — plus the blind-spot paragraph now stated on `backlog_staleness_findings` (the line-granular clock, its measured instance, and why "blame only approved lines" is the WRONG filter rather than merely an expensive one). NOT DECOMPOSABLE as a unit: it is a second arm of one guard, reading the one amendment set, and splitting it out would put half of one rule in another module — though the module is now 4880 lines and whether `check_trajectory` is still ONE checker remains the live question earlier stamps left open. Reviewed bump, reason in docs/log.d/2026-08-23-wi484-amend-guard.md. Earlier: RE-STAMPED DOWN -26 (4791 -> 4765) 2026-08-23, WI-448 slice 4: three helper bodies became one-line re-exports of the shipped package - `_process_check` (`kitlib.config.process_check`), `_split_refs` and `_norm_module`/`_MODULE_EXTS` (`kitlib.spine`) - and the now-unused `tomllib` import went with them. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +146 (4645 -> 4791) 2026-08-23, WI-502 (OI-53 ruled (d)): the Implements-tag vs CodeSymbol crosscheck — `codesymbol_crosscheck_findings` + `_codesymbol_site_finding` + `_codesymbol_candidates`, the registry-side half of the mechanized cross-check (the AST half lives in gen_arch_map.py's `implements_report`/`declaration_sites`/`_scope_index`/`_top_level_targets`, the one shared grammar home). Roughly a third of the bump is the docstrings explaining the mismatch/unresolvable vocabulary and why containment reads both directions of the dotted path. Reviewed bump, reason in docs/log.d/2026-08-23-wi502-codesymbol-crosscheck.md. Earlier: +8 (4637 -> 4645) 2026-08-23, WI-499: `APPROVAL_VIEW_RE` and the `is_approval` prose-signal regex each gain a one-line comment explaining why `ratif`/`approv` survive in these two patterns after the rename (the `docs/ratify/` path, and live-prose detection). Reviewed bump, reason in docs/log.d/2026-08-23-wi499-approval-vocabulary.md. Earlier: +13 (4624 -> 4637) 2026-08-22, WI-504: terminal history's relocation to `docs/archive/work/` (OI-55 ruled (a)) — `WI_ARCHIVE_WORK` plus its reason comment, and `_head_spec_status_map`'s HEAD tree read widened to scan both prefixes (a status transition INTO the new archive home must still be visible to the staged-registry ratchets; the OLD `docs/work`-only pathspec would have read every future close as a spec that vanished rather than one that closed). `_staged_spec_registry`'s `changed` gate widened the same way, for symmetry with the read it gates. Reviewed bump, reason in docs/log.d/2026-08-22-wi504-history-relocation.md. Earlier: RE-STAMPED DOWN -7 (4631 -> 4624) 2026-08-22, WI-448 slice 2: the local `_utf8_console` body became a one-line import of the shipped `kitlib.config.utf8_console`. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +135 (4496 -> 4631) 2026-08-22, WI-494: the declared-kernel seam exemption (OI-48 ruled (d)). `_parse_kernel_allow`/`read_kernel_modules`/`kernel_allow_parse_findings` (a new `docs/kernel-modules-allow` reader, the `docs/provenance-allow` parse-honesty idiom: required reason, malformed entries dropped and reported), the third earlier exit in `_cross_component_scan` (an edge into a declared kernel module is not a seam, checked before the seam-coverage/overlap split), and the docstring updates across `cross_component_findings`/`component_findings`/`_cross_component_scan` recording the new silent case. Roughly a third of the bump is doc comments explaining the reuse-provision grammar and the one-directional exemption. NOT DECOMPOSABLE as a unit for the same reason the WI-498 slice 4 entry gives — one checker, shared vocabulary — so the module keeps growing; whether `check_trajectory` is still one checker stays the same open question that entry left unanswered. Reviewed bump, reason in docs/log.d/2026-08-22-wi494-kernel-exemption.md. Earlier: +98 (4398 -> 4496) 2026-08-21, WI-498 slice 4: the phase-drop detector re-keyed from the bar axis to the stage axis. The block measures 217 lines of which 64 are comment or blank, and the bump is mostly those: the ANCHOR TRANSLATION TABLE and its derivation (check_vocab: allow - a closed `[p]-[reqs]` anchor records `DevStg-LLReqs`, not the rung it shares a spelling with — two rungs off, in the direction that makes the detector under-report), the live-vs-settled reasoning at `phase_stages` (an EVENT detector must read the field the drafts are in, while SELECTION keeps the field they are excluded from), and the ABSTENTION at the three repo-global rungs, which is the only part that is not a direct re-key. Executable growth is `phase_stages` (a lazy sibling import that degrades to vacuous, replacing `read_derived_phases`' basis-line regex) and the generalization of the predecessor-shape rule from two fixed levels to whatever rungs a phase recorded. NOT DECOMPOSABLE as a unit — it is one detector, and its halves share the anchor vocabulary — but the module is now 4496 lines and has grown at five of the last six stamps, so whether `check_trajectory` is still ONE checker is a live question this slice deliberately does not answer. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +103 (4295 -> 4398) 2026-08-21, review batch-close W-4 and W-12. W-12 (+24) splits a `;`-joined endpoint cell into its several endpoints in `_declared_seam_pairs`, via a small `_seam_endpoints` helper, so this reader stops disagreeing with `trace.py` about the same cells. W-4 (+79): the seam-TC allowlist stops being growable in silence. `parse_if_tc_allow` (the ordered parse plus the `# seed-count:` header key), `if_tc_allow_growth`, the reason-required-past-the-seed rule inside `read_if_tc_allow`, and the growth arm in `if_tc_allow_hygiene_findings` — the review executed the one-line edit that greens the gate (append the bare id; lexically identical to the 120 seeded lines; no hygiene line, no test, no reason). Roughly half the bump is the reasoning at the two readers. Sits in the seam-TC section beside the two functions it serves; nothing here is a second concern. Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +199 (4096 -> 4295) 2026-08-21, WI-488: the seam-TC coverage promotion (OI-43 ruled (a)) — `if_tc_coverage_findings` (the promotable half, WARN plain/ERROR under `--strict` from DevStg-Tests+), `if_tc_allow_hygiene_findings` (stale/unknown allowlist entries, warn-only forever) and `read_if_tc_allow` (the `docs/if-tc-coverage-allow` parser), plus the doc comments explaining why `interface_findings`' own total-uncited line stays unclaimed by any `Implements:` line (the Approved `LLR-042` this promotion outruns) and why the ≤1-module arch-map vacuity is shared rather than widened. Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +54 (4042 -> 4096) 2026-08-21, WI-487: the back-link campaign — literal `Implements:` declarations added near thirteen already-anchored symbols (docstring/comment lines only, no executable change). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +24 (4018 -> 4042) 2026-08-20, WI-484: DECLARATION ONLY, zero executable change — `Hat-Refs` joins SPINE_TRACED_CELLS at both row tiers, with the comment block recording why the classification is the load-bearing half of shipping the cell: the residual reads an unclassified column as APPROVED, so leaving it out would arm a re-attest window on every row the backfill touches, which is exactly the noise `Boundary-Refs` was classified out of. The LLR frozenset reflows to one-per-line at seven members. Reviewed bump, reason in the log. Earlier: -227 (4245 -> 4018) 2026-08-20, WI-448: the same 270-line spec-folder reader moved to `kitlib/registry.py`, and `_first_declared_line` became a re-export of `kitlib.config.first_declared_line`. The module keeps its OWN `_process_check` policy reader deliberately — the shared package owns the declared-LINE rule, not this checker's fail-direction. Re-stamped DOWNWARD in the same commit. Earlier: +114 (4131 -> 4245) 2026-08-20, the batch-close iterate pass (ROUND-OPUS CRITICAL-3 / ROUND-SOL MAJOR-2): the mirror invariant reaches COMMITTED state. The staged rule is keyed on a snapshot file being IN the commit, so a forged copy that LANDED — hooks bypassed — was invisible to every run afterwards, forever. `committed_snapshot_findings` + `_snapshot_write_revs` answer the same question of history instead (~75 lines with two subprocess calls total, via `git cat-file --batch-check`: identical content has an identical object id, so comparing ids IS the byte comparison), and `_git` gains an optional stdin. NOT DECOMPOSABLE into a sibling: this is the staged rule's other half, sharing its constants, its README exemption and its degrade posture — splitting them would put one half of one invariant in another module. Most of the bump is the docstring recording which comparison was REFUSED and why (snapshot-vs-live in the working tree reds every pending amendment). Reviewed bump, reason in the log. Earlier +56 2026-08-20: WI-479 (repo-review 2026-08-19
    # M-03) — the warn-first concise-Title advisory at registry validation:
    # `_TITLE_CONCISE_MAX`, `_title_length_warns` (OPEN_STATUSES-scoped,
    # summarised into one line rather than one per row — the same call the
    # IF-coverage rule already made) wired into `validate()`, plus the new
    # docstring bullet and the constant's rationale block. Never a failure,
    # never a reword of a filed title. Reviewed bump, reason in the log
    # (2026-08-20 WI-479). Earlier +17 2026-08-20: D-9 migration step 7 — PROSE AND SEVERITY ONLY, zero executable lines. `staged_snapshot_findings` gains its second severity (warn at the staged hook, ERROR on trace.py's integrity floor — design §F3 risk 3), which is wired one module over; the producer is untouched. The bump is the note recording WHY the warn is kept rather than raised (the hook invokes the staged pass with `|| true`, so the warn alone never blocked anything) plus the amend-without-flip message, which told an author to set a marker that no longer exists. Reviewed bump. Earlier MEASURED at the 2026-08-18 WI-455 merge: the two branches re-stamped this entry independently (+8 to 4177 on trunk, -119 to 4050 on the landing branch) and the merged file carries BOTH changes, so 4058 is the measured sum rather than either stamp. Trunk's +8: +8 2026-08-18: stale-carrier docstring corrections (log 2026-08-18h) — `staged_spec_registry`'s subject stops being called "the staged WI CSV" (it reads name listings, and a status change is a RENAME between docs/work/ status dirs — no row parsed), and the WI-349 block comment that QUOTED that sentence as its premise is corrected with it rather than left as a dangling citation; the surviving C0-control rationale is unchanged. Prose only, zero behavior. Reviewed bump, reason in the log (2026-08-18h). The landing branch's -119: RE-STAMPED DOWN -119 2026-08-18: WI-455 (landed) — net of the `ruff format` catch-up the landing carried (the lane hook could not run it: ruff is not importable by the hook's system python). Composed of: the dead `ast` import deleted with the AST delta machinery, the dead `ARCH_MD = "docs/architecture.md"` constant deleted with the file it named (no reader left), and the WI-399 committed-vs-disk delta family (_has_internal_import/_would_be_inventoried/shipped_modules/added_module_findings) retired when arch_inventory went AST-direct (one walk, no mirror), partly offset by the guarded gen_arch_map import and the named-modules containment message; recorded down rather than left as headroom. Earlier -39 2026-08-17: owner ruling 2026-08-17m (the cell reading) — `staged_spine_amendments` sheds the owning-SR exemption machinery (`_index_rows`/`_flagged_sr`/`_owners`): a parent flip no longer sanctions a silent child amendment — the amended row itself must flip (the status-moved exemption, unchanged). Stricter in exactly the direction the ruling points; its complexity entry retired under the limit; recorded down rather than left as headroom. Earlier +43 2026-08-16: the adversarial round's F3 — `branch_length_findings` + `_SLUG_CHARS_MIRROR`, the hand-filed half of the MAX_PATH cliff WI-462's minted-path cap could not see: dispatch derives the git branch from the on-disk spec stem VERBATIM, so a queued/draft/deferred filename past id+'-'+SLUG_CHARS re-opens the cliff unwatched. Warn-only, never the exit code; the mirror constant is deliberate (importing wi_convert for one number would mint a new cross-component seam) and tests/test_rule_sync.py pins the copies equal. Reviewed bump, reason in the log (2026-08-16b). Earlier +3 2026-08-15: the sitting sweep's M3 fix — the amend-without-flip guard's message stops saying "the sitting never sees the change" (false the moment the approved snapshot is seeded: an unmarked amendment under a still-Approved row is exactly what drift DOES catch) and says what is true in both eras: unmarked, the change surfaces only as drift once a seed exists, never as the re-attest it owes. Reviewed bump, reason in the log (sitting-sweep entry). Earlier +2 2026-08-15: D-9 migration step 5 — THE RENAME (log 2026-08-15m). The words moved (`Draft`->`Drafted`, `Verified`/`Planned`->`Approved`, `Planned` FOLDED per OI-30 D1) and `is_planned` was DELETED rather than re-keyed, so the net is small; the bump is the reasoning that has to travel with a rename a review sitting must be able to overturn — why `Modified` survives to step 7, why the retired words are named in place rather than silently gone, and (in `spine_rules`) why `maturity_bar` re-keys onto the ONE ladder table with a spine-only default so the rename cannot lower the derived gate. Reviewed bump, reason in the log (2026-08-15m). Earlier +36 2026-08-15 (log 2026-08-15j): adversarial round 2's F2 second half — the MIRROR INVARIANT was blind to DELETION. `staged_snapshot_findings` exited silently on a snapshot file removed in the commit, so the cheapest laundering was never to forge the record but to remove the page: `unanchored_findings` reports a row whose copy reads below it, and deleting the copy deletes exactly that evidence. The new arm fires when a registry is deleted WHILE THE REST OF THE RECORD STANDS, and stays silent when the whole record goes — retirement and the wholesale replacement §A1 describes are both legitimate, and a rule that fired on them would make its own design undeployable. `_snapshot_survives` is the two-line tree probe that decides which case it is (index vs commit-ish, matching `_spine_revs`' prefix contract). NOT DECOMPOSABLE: an arm added to the loop that owns the invariant. Reviewed bump, reason in the log (2026-08-15j). Earlier -92 2026-08-15: D-9 migration step 4 (log 2026-08-15g) — SN-029's digest ENGINE deletes whole: `normative_text`, `sn_normative_text`, `digest`, `current_digests`, `_DIGEST_SEP`, `_DIGEST_EXCLUDED`, `_SN_ROW_RE` and the comment block that reserved them for an on-row `TextHash`/`HashedOn` writer, ruled unnecessary complexity by the owner. An approval now records what it blessed by COPYING the registries, and a copy needs no canonical text to hash. `split_changed_cells` is what survived, and it is the better half — it answered the same question AND returns the before/after pairs a brief renders anyway. Recorded DOWN rather than left as headroom. Earlier +74 2026-08-15: D-9 migration step 3 (log 2026-08-15g) — `staged_snapshot_findings`, the MIRROR INVARIANT: in any commit that touches the `last_approved` snapshot, every touched file must be byte-identical to its live counterpart in that same commit. It is the guard that makes "the only way to write the snapshot is to copy the live registry" a DECIDABLE property rather than a convention, and it is the replacement for the co-mutation guard repo-lock D-1's anchor half would have needed — a stronger rule for less code, since a hand edit, a partial copy and a copy-then-amend-live all fail one comparison. `_split_changed_cells` is PUBLIC now (`split_changed_cells`): `baseline_snapshot` reads it as the drift basis, which is the whole reason no second cell-comparison rule had to be written. Reviewed bump, reason in the log (2026-08-15g). Earlier +25 2026-08-15: D-9 migration step 2 (log 2026-08-15g) — the amend-without-flip guard stops being blind to `Approved`. It compared verified→verified, so attested PROSE could be rewritten under a `Approved` row and no surface said so; `_APPROVED_TEXT` names the two states whose text is approved and the guard now requires the SAME one on both sides (a status that MOVED stays exempt — that is a deliberate call this does not second-guess). The comment block on `_flagged_sr` records the opposite per-site decision and why: that set is an EXEMPTION, so adding `Approved` there would have made the guard quieter on the very rows step 2 exists to surface. Reviewed bump, reason in the log (2026-08-15g). Earlier -3 2026-08-14: WI-451 slice 2 — the SupersededBy SPINE_APPROVED_CELLS entry retired with the tombstone class (D-4, 2026-08-14b). Earlier +11 net 2026-08-14: WI-442 — `Boundary-Refs` joins the §A5.1 traced half with the ruling that put it there (reviewed bump, reason in the log), against -6 from the retirement below. Earlier, RE-STAMPED DOWN — WI-191's anti-duplication rationale arm and its `_proposed_rationale_present` helper retired with the `Stability` column they armed on, and the seam-TC rule stopped filtering on a maturity value; recorded down rather than left as headroom for the next regression to hide in. Earlier +40 2026-08-13: WI-445 — OI-21's phase-anchor archetype reads BOTH the canonical [phase]-[reqs|tests] and the retired [g1|g2] spelling, plus the bar-level table and the reworded drop message (reviewed bump, reason in the log); earlier +25 2026-08-13: WI-443 — the seam-TC rule re-keyed off the retired IF Status onto Stability, summarised (reviewed bump, reason in the log); earlier +20 2026-08-13: WI-440 review fixes — the lazy covered-pairs read + the one-scan-per-run cache (reviewed bump, reason in the log)
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
    # set is {DevStg-Reqs,DevStg-Tests,DevStg-Impl} and not the {DevStg-Impl} family's, why the index check is its
    # own step rather than folded into skills-sync, why --skills is passed
    # explicitly (the default is a vacuous pass), and why neither step joins
    # _TRUNK_FRESHNESS_STEPS. Trimmed once before stamping (1649 -> 1638) by
    # merging the two step rationales into one block. Reviewed bump; re-stamp
    # down with WI-280, which owns this module's decomposition.
    # NEW MONOLITH 2026-08-24, WI-512 (OI-61 ruled (a), second step): 1591 -> 1682, crossing THRESHOLD for the first time. The generated CLI reference — `_add_argument_calls`, `_option_record`, `scan_cli`, `build_cli_reference`, `_cli_doc_exit`, its marker pair and its `--cli-doc` flag. It rides THIS module rather than a new `gen_cli_reference.py` on the ruling's own words and on the one-home rule: it is the same AST walk `scan_inventory` already does, one step further, over the same `_walk_roots`/`module_contracts`/`splice_region` the file owns — a second module would have duplicated all four and owed a new LLR/TC/IF chain for a surface this one already declares. Freezing it here is the ratchet working as designed: a mid-size script grew into a monolith, and the next edit answers for it. Reviewed baseline, reason in docs/log.d/2026-08-24-wi512-contract-generalization.md.
    "gen_arch_map.py": 1262,  # +7 (2223 -> 2230) 2026-08-29, OI-67 arms pass: `main` composes its three report/splice modes instead of dispatching into the first — six of the seven lines are the comment stating the defect the shape now prevents (`--cli-doc X --contracts-doc Y --check` reported X and exited 0 over a stale Y, a green verdict on a document nothing opened). The complexity entry re-stamps DOWN 21 -> 19 in the same commit. Reviewed bump. Earlier: +30 (2193 -> 2223) 2026-08-29, WI-533 follow-up (cross-family review F1, CRITICAL): `scan_contracts` gains the PER-SOURCE grammar arm the armed gate needs — pass `grammar_errors=[]` and a `ContractsGrammarError` from ONE source is recorded as `(source, message)` and the walk continues; pass nothing and it raises exactly as before, so `--contracts-doc` stays loud (a reference that silently omitted a source it could not parse would report a clean, fresh document over a tree it had not read). The two carriers share ONE policy through `_grammar_refusal` rather than writing the arm twice — which also keeps the walk's branch count where the complexity ratchet froze it, the decomposition escape that file prefers over a bump. The module walk's marker read moved inside the arm too: both halves of the grammar can refuse, and a module that declares NOTHING is still skipped before its bodies are read, so a bare `Contract IF-###:` in an undeclaring module keeps the refusal it had. Reviewed bump. Earlier: +10 (2183 -> 2193) 2026-08-29, WI-531 (OI-67 slice 4): DOCSTRING ONLY — the split rows of OI-67 slice 4 state their `Contract IF-###:` bodies beside the code (IF-150, the --check exit code split off the cli row IF-010); no executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi531-if-row-split.md. Earlier: +39 (2144 -> 2183) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +134 (2010 -> 2144) 2026-08-29, WI-529 (OI-67 slice 2): the contract header reaches every owner — `header_lines` (the `#` comment block of a TOML/INI/CSV/shell/extensionless file, a `#!` line skipped, or the first `<!-- -->` block of a Markdown file), `file_contracts` (the same marker and body grammar over those lines; `_contract_bodies` extracted from `module_contract_bodies` so both carriers share ONE parser), `owner_files` (the registry's file owners, a directory through its README), `file_grammar_findings` (`_grammar_findings_over` extracted likewise), and `scan_contracts` / `build_contract_reference` / `_contracts_doc_exit` taking the file owners beside the module walk. NOT decomposed, for the reason this file keeps giving: one grammar, one parser, one home — the WI-527 stamp's own argument — and splitting the header reader from the docstring reader would put the two carriers of one grammar in two modules. Reviewed bump, reason in docs/log.d/2026-08-29-wi529-header-non-python.md. Earlier: RE-STAMPED DOWN -20 (2030 -> 2010) 2026-08-29, WI-528 (OI-67 ruled (a)): `load_seam_modules` retired with the derivation it served; `_seam_edges` and `build_dependency_diagram` read the owner off the row and draw the edge the way the information runs (into the owner on a requestors row). Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +348 (1682 -> 2030) 2026-08-29, WI-527 (OI-66 ruled (a)): the contract header's whole mechanism lands in the module that already owns the `Contracts:` harvest — the anchored marker grammar (`_MARKER_RE`, `_marker_ids`, `_marker_text`), the body parser (`module_contract_bodies` and its four refusals), the reference renderer (`scan_contracts`, `build_contract_reference`) and the `--contracts-doc` mode (`_contracts_doc_exit`). NOT decomposed, and the reason is the one this file keeps asking for: every piece reads the SAME AST walk over the same docstring, and splitting the marker grammar from the body grammar would put two halves of one parser in two modules — the `--cli-doc` sibling (+189 at WI-512) sits here for the identical reason and is the precedent. Roughly a third of the bump is the refusals and their prose: a body before the marker, an undeclared id, a duplicate, and an HTML comment that could close the generated document's own end marker. The last +36 is the post-build adversarial round: no UNDECLARED id may survive in the marker's tail (a partial parse declared one seam and dropped the other in silence), a body is ordered against the marker declaring ITS id rather than the first marker in the file, a marker line ends a body so it cannot be swallowed into one, and `_md_safe` defangs comment delimiters in BOTH generated references so a module summary cannot close the document's own end marker. Before that, +2 accepted a TRAILING FULL STOP after the id list, which is ordinary writing and safe where a trailing `and`/comma is not: nothing can follow it, so accepting it cannot drop an id. Reviewed bump, reason in docs/log.d/2026-08-29-wi527-contract-header.md.
    "check.py": 1163,  # +8 (2458 -> 2466) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +75 (2383 -> 2458) 2026-08-29, WI-527 (OI-66 ruled (a)): the `interface-reference` freshness step, on `cli-reference`'s exact shape, plus the absent-declared-artifact arm in `staged_divergence` — a `[generated]` row naming a file that does not exist read GREEN for every artifact in the kit, because each freshness step is deliberately vacuous on an absent target, so deleting a declared artifact disarmed its own gate in silence. That arm closes the hole for all eleven declared artifacts, not just the new one, and it keys on TRACKED-but-absent rather than merely missing so a fresh scaffold — which has generated nothing yet — stays silent. The +6 over that reads HEAD as well as the index: `git ls-files` is the INDEX, and a STAGED deletion has already left it, so the arm went quiet on exactly the commit-bound case it exists for. Reviewed bump, reason in docs/log.d/2026-08-29-wi527-contract-header.md. Earlier: +32 (2351 -> 2383)  # +32 (2351 -> 2383) 2026-08-24, WI-512 (OI-61 ruled (a), second step): the `cli-reference` freshness step for the newly declared `[generated]` CLI reference — the step tuple, the `CLI_REFERENCE_DOC` constant, the `BUILTIN_STEP_NAMES` row and the `_TRUNK_FRESHNESS_STEPS` membership. The executable delta is ~18 lines; the rest records the one wiring decision a reader would otherwise re-derive, and it is the decision that separates this artifact from `skills-index`/`prompt-catalog`: its SOURCE is code a work branch edits, so standing it down on a branch would normally leave it ungated on the only side that can fix it — and it does not, because it joined `trunk_step.py --regen` in the same change. Reviewed bump, reason in docs/log.d/2026-08-24-wi512-contract-generalization.md. Earlier: +19 (2332 -> 2351) 2026-08-23, WI-484 phase 3: the `component-view` freshness step (the step tuple, its `BUILTIN_STEP_NAMES` registration and its `_TRUNK_FRESHNESS_STEPS` membership) for the newly declared `[generated]` component view. Three executable lines plus the ten that record why the step lands in the same change as the artifact it enforces: the whole argument for retiring `DetailDoc` was that a generated view is stale-DETECTABLE where a prose file is not, and that argument is only true while this step exists. Reviewed bump, reason in docs/log.d/2026-08-23-wi484-component-view.md. Earlier: +6 (2326 -> 2332) 2026-08-22, WI-504: `docs/archive/work/*` joins the doc-navigability `--ignore` list beside `docs/work/*` — a terminal spec's body is DATA (a verbatim historical Deliverable record), not navigable prose, wherever it lives, and the archive move (OI-55 ruled (a)) put the terminal three one directory outside the existing ignore. One row plus its reason comment. Reviewed bump, reason in docs/log.d/2026-08-22-wi504-history-relocation.md. Earlier: -2 (2328 -> 2326) ruff format tightened two multi-line calls in the same commit's approval-immutable addition. Earlier: +152 (2176 -> 2328) 2026-08-22, WI-503: the re-attestation brief immutability enforcer (approval_immutability, _is_dated_approval_brief, _approval_immutable_mode, the --approval-immutable flag, the approval-immutable step tuple and its BUILTIN_STEP_NAMES row) — the sibling of staged_divergence that reads the STAGED tree and refuses any change other than a plain add to an existing dated docs/ratify/ brief. Reviewed bump, reason in docs/log.d/2026-08-22-wi503-approval-brief-split.md. Earlier: RE-STAMPED DOWN -8 (2184 -> 2176) 2026-08-22, WI-448 slice 2: the local `_utf8_console` body became a one-line import of the shipped `kitlib.config.utf8_console`. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +44 (2140 -> 2184) 2026-08-22, WI-498 PROGRAM CLOSE, review item W-12: the retired-tag alias table resolves BY MEANING. The executable delta is TWO table values (`G2` and `DevBar-Tests` -> `DevStg-Impl`) plus the warning's added clause; the rest is the record, and it is load-bearing in exactly the way this ratchet's escape hatch exists for, because the value looks wrong until the reason is read: a retired tag named a BAR the repo had CLEARED, the bar was a MIN over every in-scope row, so the `DevStg-Tests` bar was reached only by a fully decomposed and TC'd spine (check_vocab: allow) - the `DevStg-Impl` RUNG, three above the word it shares. `_LEGACY_BAR_THRESHOLD` had that rule written down for `gates =` lists and this table took the SPELLING, so `--gate G2` selected 12 steps where the equivalent arrival selects 26, silently dropping `traceability`, `tests+coverage`, `lint`, `format` and ten others behind one line of reassurance. Composition for `gates =` lists is UNCHANGED (every entry lands on the threshold it did before); only the current-stage direction moves. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md; re-stamp down with WI-280. Earlier: +13 (2127 -> 2140) 2026-08-22, WI-498 PROGRAM CLOSE, review item W-1: OI-31's ruled promotion is TAKEN — the `staged-divergence` plan step now passes `--strict`, so a regenerated-but-unstaged generated artifact REFUSES the commit instead of warning past it. The executable delta is four lines (the flag on the step's argv, wrapped); the rest is the wiring record OI-31 asked for and the message branch that stops the step telling an operator it "does not block a commit today" when it now does. The close's adversarial round drove the exact tree the warn-only posture let through (stage a registry edit, regenerate `docs/stage`, skip the `git add`: every freshness step green over bytes the commit does not contain), which is the CRITICAL this closes. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md; re-stamp down with WI-280. Earlier: RE-STAMPED DOWN -44 (2171 -> 2127) 2026-08-21, WI-498 slice 5: the `derived-gate` freshness step and its two registrations retire with the file they guarded, and `_derive_stage`'s subprocess body moves to `kitlib.stage.derive_via_subprocess` - homed there by its SECOND consumer (`agent_common.spine_stage_of`), because copying it would have minted an F5 duplicate in which a plan selector and an approval authority drift apart in silence. What stays here is this module's FAILURE POLICY, which is the half that differs. Re-stamped downward in the same commit, per this file's rule. Earlier: +7 (2164 -> 2171) 2026-08-21, WI-498 slice 4: COMMENT ONLY, zero executable change. The `docs/gate` hand-off record is corrected where slice 2 left it. Slice 2 enumerated the file's surviving readers as two event detectors plus three display sites; this slice cut both detectors over and, doing so, found a SIXTH reader that enumeration missed - `agent_common.spine_stage_of`, which is not display at all but the input to `human_holds`, i.e. who may approve. The note now names all four survivors and says which class each is in, because the reason the freshness step stays wired is that one of them decides approval authority, not that three of them draw pages. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: RE-STAMPED DOWN -173 (2337 -> 2164) 2026-08-21, WI-498 slice 2 (OI-51): selection re-keys to AT OR ABOVE the derived stage, and the bar axis is DELETED from this module with the membership rule it served. Gone: BAR_REQS/BAR_TESTS/BAR_RELEASE, BAR_ORDER, GATES, bar_ord, _resolve_bar_alias's bar wording, GATE_FILE and the four `# basis:` regexes, _window_ord, _basis_counts, resolve_gate, window_open, product_floor, floor_plan, floor_notice, advisory_plan, run_advisory and ADVISORY_EXCLUDE. The last seven are the PRODUCT FLOOR and the ADVISORY TIER, and they retire because their cause is gone rather than because anyone traded them away: both existed to compensate for a derived bar that one drafted row could collapse, and `docs/stage` is derived over the SETTLED spine, so drafting cannot lower selection for any step. What was ADDED against that is small and is named here so the net is not read as pure subtraction: `at_or_above` (the one comparison), `resolve_stage` + `_derive_stage` (the common reader, with the subprocess deriver that keeps the never-import-a-sibling rule), `_step_threshold` + `_LEGACY_BAR_THRESHOLD` (the `from-stage` key and the `gates =` translation an adopter's file still needs) and `_warn_retired_flag_spelling`. Re-stamped down in the same commit, per this file's rule. Earlier: +17 (2320 -> 2337) 2026-08-21, WI-498 slice 1: the `derived-stage` step - the freshness guard on `docs/stage`, the stage axis's own derived cache - plus its `BUILTIN_STEP_NAMES` registration and its `_TRUNK_FRESHNESS_STEPS` membership. The step tuple is six lines and the two registrations are one each; the remaining nine record the two wiring decisions a reviewer would otherwise have to re-derive, and both are deliberate SAMENESS rather than novelty: it takes the same three bar tags and the same trunk-lane stand-down as `derived-gate` because the two files are derived from the same rows by the same predicates, and a repo where one is guarded and the other is not is a repo where they can silently disagree. The registration line is the one the FULL suite catches and a targeted run cannot - an unregistered built-in name lets a downstream `[step:derived-stage]` APPEND a second step under a kit name instead of being refused (the WI-486 lesson, applied without being re-learned). This entry re-stamps DOWN with slice 2, which deletes the bar constants and the axis they select on. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +3 (2317 -> 2320) 2026-08-21, review batch-close W-21: `--gate`'s help now states that product-layer steps are selected at max(the passed bar, the ex-draft floor), so passing a LOWER bar does not drop them — behaviour that was deliberate and undocumented. Three lines of help is the whole change. Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +7 (2310 -> 2317) 2026-08-21, WI-487: the back-link campaign — literal `Implements:` declarations added near four already-anchored symbols (docstring/comment lines only, no executable change). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +146 (2164 -> 2310) 2026-08-20, WI-473 (repo review C-01): the PRODUCT-REGRESSION FLOOR — `product_floor` (reads `ex-draft=` off the basis line this module already parses for `window_open`), `floor_plan` (the product-layer steps the derived bar dropped, built from the FLOOR bar's own table, never by filtering this gate's — advisory_plan's BLOCKER-4 lesson), `floor_notice` and three wiring lines in main(). Executable delta ~35 lines; the rest is the reasoning, and it is load-bearing in exactly the way this ratchet's escape hatch exists for, because the SHAPE of the fix was contested by the tree: (a) why the floor is DERIVED from `ex-draft` rather than a stored high-water mark — process.md §4 pre-authorizes "a second, derived high-water number shown BESIDE the honest one", and `spine_rules.compute` already ruled the axis against new state; (b) what "monotonic" is and is NOT being claimed (drafting can never lower it; approving a less-mature row or demoting an approved one still can, both reviewed human-held acts visible in a tracked derived file's diff — which IS the sanction for a deliberate lowering); and (c) why the review's other suggestion (infer the floor from configured product commands) cannot ship, since BUILTIN_PRODUCT gives every scaffold configured commands from minute one and `pytest` on an empty tree exits 5. TWO decompositions rather than a complexity re-stamp, both measured: `floor_notice` returns a newline-terminated string instead of taking a branch in main(), and `resolve_plan` lifts the whole three-tier plan construction (gating / floor / advisory, whose ORDER is the load-bearing part) out of main() — which a nested `steps_at` def had taken 16 -> 17. Measured after: main is EXACTLY 16 again, so tests/test_complexity_ratchet.py is untouched by this change, and the +16 lines that decomposition cost are inside this bump. Reviewed bump, reason in the log (docs/log.d/2026-08-20-program-grind.md); re-stamp down with WI-280. Earlier: +3 (2161 -> 2164) 2026-08-20, WI-448: `_git_out`'s body moved to `kitlib.git.git_out` and the guarded package import replaced it — net +3 because the import guard is five lines and the shed body was fourteen against a six-line pointer comment. Reviewed bump, reason in the log. Earlier: +32 2026-08-20: WI-486 (OI-42 ruled (e)) — the `backlink-coverage` step joins the process floor at DevStg-Tests/DevStg-Impl. The code delta is ~18 lines (the command list, the `--strict-backlinks` promotion beside the two that already ride that ladder, and the step tuple); the rest records what a reviewer would otherwise re-derive — why the step reports rather than gates as shipped (the dial is 0), and why the "all" pre-commit gate is EXCLUDED from the strict promotion exactly as `trajectory`/`vocabulary` are. The scan itself is NOT here: it lives in `gen_arch_map.py` beside the `Implements:` grammar it shares, which is the decomposition the ratchet prefers, taken as far as it goes. The 32nd line is the `BUILTIN_STEP_NAMES` registration, which the FULL suite caught and the targeted runs could not: an unregistered built-in name lets a downstream `[step:backlink-coverage]` silently APPEND a second step under a kit name instead of being refused. Reviewed bump; re-stamp down with WI-280. Earlier +33 2026-08-20: D-9 migration step 7 — `_BASIS_RE`'s `modified=` group becomes OPTIONAL and `_basis_counts` is extracted as the one home for the absent-means-zero reading (~6 executable lines). The rest records the ASYMMETRY, which is the whole content of the change: `spine_rules` stopped EMITTING the field because the value cannot exist under the closed enum, while this consumer keeps HONOURING it for gate files this kit did not produce — requiring it would miss on today's own docs/gate and disarm the detector entirely, dropping it would throw away the window detector's one CONCLUSIVE arm for every repo mid-migration. Reviewed bump. Earlier +212 2026-08-18 (MEASURED 1884 -> 2096): OI-31 ruled option (b) — the `staged-divergence` step. check.py has no index concept, so all nine freshness gates read the WORKING TREE and an author who regenerates without staging gets an honest green over a stale commit (measured at 3b8d306d, where PROJECT_STATE.html was modified in the worktree, absent from the index, and the committed tree failed the very gate that guarded it). ~55 lines are mechanism (_generated_census reading docs/stack.ini `[generated]` with optionxform=str, _declared_generated's prefix/exact match, staged_divergence's four degradation exits + the `git diff --name-only -z` compare, the CLI mode and its `--strict` refusal); the rest is the recorded WHY, and it is load-bearing in the specific way this ratchet's escape hatch is for: the ruling's OWN honest gap (an artifact STAGED WHILE STALE is invisible to this and needs option (a)) is written into the step's docstring AND its runtime message, because "a check whose limits are undocumented is how the last false green survived", and the three wiring decisions a reviewer would otherwise have to re-derive (warn-only with the promotion deliberately unwired, every bar, and NOT in _TRUNK_FRESHNESS_STEPS) live at the step tuple. Trimmed once before stamping (2086 -> 2084) by merging the step comment's opening into the pointer at staged_divergence(); +12 back for `_divergence_mode`, which exists because main() sat AT its complexity baseline and the two new branches took it 16 -> 18 — decomposed rather than re-stamped, so tests/test_complexity_ratchet.py is untouched by this change. Reviewed bump, reason in the log (2026-08-18, docs/log.d/2026-08-18-divergence-step.md); re-stamp down with WI-280. Earlier RE-STAMPED DOWN -22 2026-08-18 (-19 for the retirement below, -3 from the `ruff format` catch-up the landing carried): WI-455 (landed) — the arch-map committed-map freshness step retired (arch_cmd + the step tuple; the [arch-map] mode validation stays); recorded down rather than left as headroom. Earlier +19 2026-08-18: the one-vocabulary rename (owner ruling; log 2026-08-18d) — the `DevBar-*` prefix retires and the SAME `DevStg-*` token names both readings, the verb carrying the axis. This module gains only the ALIAS ROWS that keep an adopter's literal value working across the re-sync (three entries plus the comment recording why the Release row resolves to `DevStg-Impl` and not `DevStg-Release` — the one mapping that is not a prefix swap, because that bar closed the Impl rung). Zero behaviour change: a canonical value resolves exactly as before. Reviewed bump, reason in the log (2026-08-18d). Earlier +8 2026-08-15: D-9 migration step 5 — THE RENAME (log 2026-08-15m). The words moved (`Draft`->`Drafted`, `Verified`/`Planned`->`Approved`, `Planned` FOLDED per OI-30 D1) and `is_planned` was DELETED rather than re-keyed, so the net is small; the bump is the reasoning that has to travel with a rename a review sitting must be able to overturn — why `Modified` survives to step 7, why the retired words are named in place rather than silently gone, and (in `spine_rules`) why `maturity_bar` re-keys onto the ONE ladder table with a spine-only default so the rename cannot lower the derived gate. Reviewed bump, reason in the log (2026-08-15m). Earlier +71 2026-08-15: WI-460 — the SILENT-SKIP GUARD (missing_tool_banner + _skipped_product_steps, wired into the two lenient hook entry points). ~15 lines are the guard; the rest is the recorded WHY, and it is load-bearing here: this repo's four late defects all traced to a bar that was not running, two of them to a SKIP nobody read, and the docstring is where the REFUSAL alternative is written down as the owner's call rather than silently declined (reviewed bump, reason in the log); earlier +23 2026-08-14: WI-454 — the need-form step (SN-033's declared checker) joins the process floor at every bar, and most of the bump is the comment stating why it NEVER gains --strict there: promoting a form heuristic over approved stakeholder prose to a gate is an owner ruling, and the wiring is where that boundary had to be recorded (reviewed bump, reason in the log fragment); earlier +145 2026-08-13: WI-445 — OI-21's bar vocabulary, the bar_ord/_window_ord ordinal lookups replacing the lexical gate comparisons, the retired-tag alias layer with its deprecation posture, and the vocabulary step (reviewed bump, reason in the log)
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
    # STORED the enum word beside the template's `human_approval_through =
    # 4`, and since the readers prefer the ordinal, every repo that chose a
    # non-default posture scaffolded FULLY ATTENDED with no diagnostic
    # anywhere. The word is TRANSLATED now, not stored — `LEGACY_APPROVAL`
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
    # +15 2026-08-13: WI-439 review fix — the tracked-file anchor probe + the
    # three-cause warning wording (reviewed bump, reason in the log).
    # WI-446: +20 (2767 -> 2787). Two MAPPING rows registering the hats layer
    # (SN-036 / OI-19) — the roster template and the `hats.py` reader its
    # importer needs — plus their reason comments and the two docstring lines in
    # the kit-contents listing. Registration, not monolith drift: the layer's
    # own code is a new module under THRESHOLD, and a MAPPING row is the only
    # way a scaffold ever receives a file. Reviewed bump; re-stamp down with
    # WI-280.
    # M-05 fix (repo review 2026-08-19, WI-476): this key was a DUPLICATE dict
    # entry above ("bootstrap.py": 2808, immediately preceding this comment) —
    # a re-stamp that appended a fresh key instead of updating this one in
    # place. Python's dict-literal evaluation silently kept only this later
    # entry (2808 was dead weight), which is exactly the class of defect this
    # baseline can no longer hide: see test_baseline_has_no_duplicate_keys
    # below, which parses this file's own AST rather than trusting the runtime
    # dict. Merged into this single entry; the bound value does not change —
    # 2859 was already the effective baseline, and the composed-sum accounting
    # below already threads the WI-439-review-fix (+15) and WI-446 (+20) deltas
    # through the 2026-08-18 merge math, so no history is lost by the merge.
    "bootstrap.py": 1571,  # +13 (3153 -> 3166) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +7 (3146 -> 3153) 2026-08-25, WI-521 slice 1: one MAPPING row for `scripts/acceptance_record.py` plus the six comment lines recording why the scaffold cannot skip it — `check_trajectory.py` imports it UNGUARDED and joins its findings to the failure set, so a copy without it cannot run the checker at all, which is a harder dependency than the optional `gen_arch_map` beside it. The same declaration shape WI-483 slices 3 and 4 and WI-520 each took here; the manifest is the one home for what ships, so a new sibling costs this file a row by construction. Reviewed bump, reason in docs/log.d/2026-08-25-wi521-slice1-acceptance-record.md. Earlier: +8 (3138 -> 3146) 2026-08-25, WI-520: one MAPPING
    # row for `scripts/kitlib/secret_classes.py` (the credential class
    # vocabulary `check_privacy.py` and `agent_common.py` now both read) plus
    # the six comment lines saying why it ships — the same must-be-whole
    # shape as every other `kitlib/` module row above. DECLARATION ONLY, no
    # logic moved. Reviewed bump, reason in
    # docs/log.d/2026-08-25-wi520-secret-class-vocabulary.md.
    # Earlier: +6 (3132 -> 3138) 2026-08-23, WI-483 slice 4:
    # one MAPPING row for `scripts/coherence.py` plus the five comment lines
    # saying why it ships. DECLARATION ONLY — no logic moved and no behaviour
    # changed; the identical shape WI-483 slice 3 took for `scripts/pending.py`
    # (+8) the day before. Reviewed bump, reason in
    # docs/log.d/2026-08-23-wi483-engine-splits.md.
    # Earlier: +6 (3126 -> 3132) 2026-08-23, WI-448 slice 5 (the
    # lane close): the module's SECOND declared duplicate goes. `_toml_scalar`'s
    # 11-line body becomes a binding to `kitlib.spine.toml_value` and the OI-3
    # brief is emitted through `kitlib.spine.toml_fields` keyed by the shipped
    # schema of record — so CODE left this file and what replaced it is a
    # fail-closed guard (an undeclared key raises instead of writing a brief that
    # renders empty) plus the paragraphs recording that the WI-431 entry above is
    # now HISTORY: "bootstrap.py runs before the kit is copied and can import no
    # sibling" was overturned by D-8's inversion in slice 1, and the pin that
    # premise justified is deleted. A reviewed bump on the axis this row's own
    # complaint below calls the wrong one — the file got simpler and longer.
    # Reason in docs/log.d/2026-08-23-wi448-close.md.
    # Earlier: +1 (3125 -> 3126) 2026-08-23, WI-455 slice 5: one MAPPING row shipping `scripts/traj_context.py` (the System-context view) to an adopter, plus the module name in the gen_trajectory sibling-set docstring line — the set copies together or a scaffold ImportErrors on its first render. Reviewed bump, reason in docs/log.d/2026-08-23-wi455-context-view.md. Earlier: +1 (3124 -> 3125) 2026-08-23, WI-484 phase 3: one MAPPING row shipping `scripts/gen_components.py` to an adopter (plus the generator's name in the module-list docstring, same line). Reviewed bump, reason in docs/log.d/2026-08-23-wi484-component-view.md. Earlier: +8 (3116 -> 3124) 2026-08-23, WI-483 slice 3:
    # one MAPPING row for `scripts/pending.py` plus the seven comment lines
    # saying why it ships (traj_status.py, gen_open_items.py and dispatch.py
    # all import it, the first two unguarded, so a scaffold without it cannot
    # render the owner surface at all — the `schedule.py` omission class).
    # Declaration only; no code moved into this file or out of it, and the
    # axis complaint recorded below applies unchanged: this is a manifest
    # growing, which is what a manifest does. Reviewed bump, reason in
    # docs/log.d/2026-08-23-wi483-bad-edges.md.
    # Earlier: +7 (3109 -> 3116) 2026-08-23, WI-448 slice 3:
    # one MAPPING row for `scripts/kitlib/spine.py` plus the six comment lines
    # saying why it ships (trace.py, trace_text.py and spine_rules.py are all
    # in this list and all resolve the row vocabulary through it now, so the
    # package must arrive whole — the `schedule.py` omission class). Declaration
    # only; no code moved into this file or out of it, and what the row REGISTERS
    # is a net subtraction elsewhere in the kit (87 lines out of trace.py alone).
    # The axis complaint recorded below applies unchanged: this is a manifest
    # growing, which is what a manifest does. Reviewed bump, reason in
    # docs/log.d/2026-08-23-wi448-spine-policy-pair.md.
    # Earlier: +55 (3054 -> 3109) 2026-08-23, WI-499: `_migrate_dial_key_name` joins `migrate_legacy_config` (called before `_migrate_dial_ordinal` so a repo on BOTH the retired key name and the retired 0-4 ordinal gets both fixed in one `--migrate-config` pass) plus the `LEGACY_ATTESTATION_KEY` constant it reads. Reviewed bump, reason in docs/log.d/2026-08-23-wi499-approval-vocabulary.md. Earlier: +12 (3042 -> 3054) 2026-08-22, WI-504: the terminal three (`complete/cancelled/partial`) leave the scaffolded `docs/work/` skeleton for `docs/archive/work/` (OI-55 ruled (a)) — GITKEEP_DIRS re-keyed to the new paths plus the reason comment explaining why the active workspace now scaffolds only draft/active/deferred, and the header docstring's manifest + inventory lines updated to match. Declaration only; no code moved into this file or out of it. Reviewed bump, reason in docs/log.d/2026-08-22-wi504-history-relocation.md. Earlier: +12 (3030 -> 3042) 2026-08-22, WI-500 (the test-evidence carrier): two MAPPING rows and their reason comments - `scripts/kitlib/evidence.py` (the record format and the source surface its claim binds to; `kitlib/stage.py` imports it, so the must-arrive-whole rule applies to the package again) and `scripts/record_test_evidence.py` (the ONLY sanctioned producer of `docs/test/evidence`, shipped because a rung whose producer stayed in the kit repo would be a rung no adopter could ever earn) - plus the new script in the header docstring's inventory line. Declaration only; no code moved into this file or out of it. The axis complaint recorded below applies unchanged: this is a manifest growing, which is what a manifest does. Reviewed bump, reason in docs/log.d/2026-08-22-wi500-test-evidence-carrier.md. Earlier: +7 (3023 -> 3030) 2026-08-22, WI-483 slice 2: one MAPPING row for `scripts/census.py` plus the six comment lines saying why it ships (dispatch.py, intake.py and adjudicate_brief.py all import it, the first two unguarded, so a scaffold without it cannot run the walk-away loop — the `schedule.py` omission class). Declaration only; no code moved into this file or out of it. The axis complaint recorded below applies unchanged: this is a manifest growing, which is what a manifest does. Reviewed bump, reason in docs/log.d/2026-08-22-wi483-lifecycle-scc.md. Earlier: RE-STAMPED DOWN -1 (3024 -> 3023) 2026-08-21, WI-498 slice 5 recovery: the module docstring's "What it creates in the destination" manifest still listed `docs/gate <- gate.template` one line above the `docs/stage` row that REPLACED it — a half-applied sweep in the first thing a reader of this script sees, and a promise the MAPPING (which lost the row correctly) no longer keeps. Deleting the stale line is the whole delta; recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +78 (2946 -> 3024) 2026-08-21, WI-498 slice 5 (folding WI-493): `_migrate_dial_ordinal` joins `--migrate-config`, plus the `LEGACY_DIAL_ORDINALS` table it reads. A MANIFEST AND A MIGRATOR, which is what this file is: the scaffold row `("gate.template", "docs/gate")` was DELETED in the same act, so the manifest half is a net subtraction. The migrator is ~20 executable lines; the rest states why it rides a legacy-FILE command at all (the value is already in `process.toml` and only its VOCABULARY is old, but this is the one command an adopter is told to run at re-sync, and the alternative is the reader warning on every run forever), why it reads the value off the LINE rather than parsing TOML (this module parses none - it is the one script runnable from a bare download), and why an out-of-range number is LEFT ALONE with a note rather than guessed at (a migrator that picked a value would be making an approval-authority decision). Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +20 (2926 -> 2946) 2026-08-21, WI-498 slice 1: three MAPPING rows and their reason comments - `scripts/kitlib/stage.py`, `scripts/derive_stage.py`, and `stage.template` -> `docs/stage` - plus the new artifact in the header docstring's what-it-creates list and the new script in its inventory line. Declaration only: no code moved into this file or out of it. The comments carry the must-arrive-whole rule for a three-module chain (derive_stage imports spine_rules AND kitlib.stage, and all three are in this list), which is the `schedule.py` omission class the rows exist to prevent. The axis complaint recorded below applies unchanged: this is a manifest growing, which is what a manifest does. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +6 (2920 -> 2926) 2026-08-21, WI-498 slice 0: one MAPPING row for `scripts/kitlib/ladder.py` plus the five comment lines saying why it ships (spine_rules, agent_common and traj_status are all in this list and all import it now, so the package must arrive whole - the `schedule.py` omission class, again). Declaration only; no code moved into this file and none moved out, and what the row REGISTERS is a net SUBTRACTION elsewhere in the kit (two literal restatements of the stage ladder deleted). The axis complaint recorded below applies unchanged: this is a manifest growing, which is what a manifest does. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +16 (2904 -> 2920) 2026-08-21, WI-487: the back-link campaign — literal `Implements:` declarations added near five already-anchored symbols (docstring/comment lines only, no executable change). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +5 (2899 -> 2904) 2026-08-20, WI-483: one MAPPING row for `scripts/kitlib/station.py` plus the four comment lines saying why it ships (the scripts that import it are already in the list, so the package must arrive whole - the `schedule.py` omission class). Declaration only; no code moved into this file and none moved out. The axis complaint recorded on the entry below applies again and unchanged: this is a manifest growing, which is what a manifest does. Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +40 (2859 -> 2899) 2026-08-20, WI-448 (D-8/OI-16, the common-module inversion) — AND THIS ENTRY IS THE RATCHET MEASURING THE WRONG AXIS, which is the owner's own correction (OI-16: the monolith risk was always FUNCTION size and complexity, not file length). What grew: the four `scripts/kitlib/*.py` MAPPING rows with the ~20-line comment stating why that block is the whole downstream risk surface of the ruling, plus the guarded import of the package. What SHRANK inside the same file: two duplicated helper bodies (`_first_declared_line`, `_utf8_console`) became one-line re-exports. So the file got a DECLARATION longer and an IMPLEMENTATION shorter, and the check asked for a reviewed bump on the declaration. Bumped deliberately; reason in docs/log.d/2026-08-20-program-grind.md. Earlier: MEASURED at the 2026-08-18 WI-455 merge: the two branches re-stamped this entry independently (+13 to 2878 on trunk, net -19 to 2846 on the landing branch) and the merged file carries BOTH changes, so 2859 is the measured sum rather than either stamp. Trunk's +13: +13 2026-08-18: docs/work README joins the scaffold — one MAPPING row with its reason comment, and the header docstring's status-dir list corrected to include `partial` (reviewed bump, reason in the log fragment 2026-08-18-work-registry-readme). The landing branch's net -19: RE-STAMPED DOWN -23 2026-08-18 (the dead `configparser` import deleted with the arch-map profile probe, plus): WI-455 (landed) commit 3 — docs/architecture.md leaves MAPPING and initialize_generated_docs re-gates on docs/status.md (the arch_cmd/profile-probe block retired). Earlier +4 2026-08-18: WI-455 (landed) — RUNTIME_FLOWS.template.md joins MAPPING (one row + three comment lines: the sitting-2 decision-8 flows move; reviewed bump, reason in the WI-455 log fragment). Earlier +17 2026-08-15: D-9 migration step 3 (log 2026-08-15g) — two MAPPING rows and their reasoning: `baseline_snapshot.py` joins the shipped script manifest (a sibling import of `intake.py`, so a scaffold without it cannot adjudicate at all — the WI-379 failure class), and the `last_approved` README template scaffolds the snapshot directory with PROSE ONLY. The second comment records why an adopter receives an empty snapshot rather than a pre-filled one: a copied snapshot would claim a human blessed text they have never seen. Reviewed bump, reason in the log (2026-08-15g). Earlier +4 2026-08-14: WI-454 — check_need_form.py joins the shipped script manifest with its reason (one MAPPING row + three comment lines; the docstring listing absorbed the name on its existing check_* line — the WI-392 shape; reviewed bump, reason in the log fragment); earlier +10 2026-08-14: WI-442 — external.toml joins MAPPING, the scaffold docstring and the boundary-vs-interface explanation an adopter reads first (reviewed bump, reason in the log); earlier +6 2026-08-13: WI-445 — check_vocab.py joins the shipped script manifest with its reason (reviewed bump, reason in the log); composed at the 2026-08-13 serial merge: WI-439 (+26) + its review fix (+15, the tracked-anchor probe) + WI-446's MAPPING rows (+20); measured, reasons above and at each contributing WI
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
    # Then +95 (2166 -> 2261), SN-029: the ORDINAL's one home — `approval_
    # level` (with `LEGACY_APPROVAL_LEVEL` mapping the retired enum and
    # `APPROVAL_FALLBACK` naming the conservative default), `human_holds`
    # (the single comparison every consumer makes, including the ruling that
    # both ENDS of the ordinal are absolute), `keep_nondependent` and
    # `spine_stage_of`. Five consumers stopped string-comparing policy words;
    # the growth is the definition plus the reasoning for the two ends.
    # Reviewed bump.
    # Then +90 (2261 -> 2351), SN-029 REVIEW round 1. The review drove the
    # ordinal's own defects: `LEGACY_APPROVAL` states all THREE dials a
    # retired enum word meant instead of collapsing it to a level (translating
    # `single-approve` to "level 2" silently gave it a per-tier hold it never
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
    # runs, so `4 < 4` let the SHIPPED DEFAULT self-approve the final gate).
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
    "agent_common.py": 1262,  # +12 (2678 -> 2690) 2026-08-30, WI-535 (telemetry first, dial off): `write_session_log`'s header-key tuple gains the four columns `session_meta` now writes (`session-id`, `context-used`, `context-window`, `context-pct`), and `regenerate_index`'s generated table gains a `Ctx %` column reading the same field. Reviewed bump, reason in docs/log.d/WI-535-adjudicator-telemetry-first.md. Earlier: +18 (2660 -> 2678) 2026-08-30, WI-548: EXIT_REVIEW_OWED = 9 appended at the end of the exit alphabet with its parked-not-decided rationale, and the session-log header gains the typed "timeout" (wall|idle, C3) and "heterogeneity" (relaxed, C5) keys. Reviewed bump, reason in docs/log.d/WI-548-stall-guard.md. Earlier: +1 (2659 -> 2660) 2026-08-29, WI-533 (OI-67 slice 6): `_read_csv_rows` reads through `kitlib.spine.csv_rows` (one comment-skipping CSV reader for every kit consumer); the import line is the one net line. Reviewed bump, reason in docs/log.d/2026-08-29-wi533-arm-the-gate.md. Earlier: +16 (2643 -> 2659) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +9 (2634 -> 2643) 2026-08-25, WI-520: the credential class vocabulary's one home — `_SECRET_RES` becomes a comprehension over `kitlib.secret_classes.SECRET_CLASSES` (the same table `check_privacy.py`'s enforcement floor reads) instead of six hand-copied literals, plus the import and the comment recording why (the WI-508 alignment pass measured the two hand-copies disagreeing, in both directions, on four of five driven samples). One behavioural change: a PEM private-key block is now redacted, where it previously passed through as an "unknown token shape". Reviewed bump, reason in docs/log.d/2026-08-25-wi520-secret-class-vocabulary.md. Earlier: +3 (2631 -> 2634) 2026-08-23, WI-509 (OI-59 ruled (a)+(c)): the three `--migrate-config` remediation messages now spell the kit-relative `project-trajectory/scripts/bootstrap.py` path instead of a bare `scripts/bootstrap.py` an adopter's own repo never has (the kit-path invariant). Comment/string-literal wording only, zero behavioural change. Reviewed bump, reason in docs/log.d/2026-08-23-wi509-kit-path-invariant.md. Earlier: +4 (2627 -> 2631) 2026-08-23, WI-499: ruff format re-wrapped lines the rename lengthened; zero semantic change. Earlier: +30 (2597 -> 2627) 2026-08-23, WI-499 (the retired-word rename): the dial-key migration work — `LEGACY_ATTESTATION_KEY` (the retired key spelling, check_vocab: allow), `approval_through`'s loud legacy-key fallback arm, and splitting the accidentally-collided `APPROVAL_RUNGS` name into `APPROVAL_DIAL_RUNGS` (the dial vocabulary) versus the pre-existing off-spine `APPROVAL_RUNGS` dict the mechanical rename had silently shadowed. Reviewed bump, reason in docs/log.d/2026-08-23-wi499-approval-vocabulary.md. Earlier: RE-STAMPED DOWN -4 (2601 -> 2597) 2026-08-22, WI-448 slice 2: the local `_utf8_console` body became a one-line alias onto the shipped `kitlib.config.utf8_console`, which this module already imports under its guard. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +183 (2418 -> 2601) 2026-08-21, WI-498 slice 5 (folding WI-493): the APPROVAL DIAL re-keys from the 0-4 tier ordinal to a `DevStg-*` rung, and `spine_stage_of` cuts from a regex over a comment on `docs/gate` to the self-healing common reader. EXECUTABLE DELTA IS ROUGHLY A WASH and slightly negative: `DIAL_HOLDS` - a 20-line declared table mapping five levels onto rung sets - is DELETED outright, because under one vocabulary the dial and the stage are the SAME ladder and the comparison becomes `stage_ord(stage) <= stage_ord(dial)`; what replaced it is one line. What GREW is the record, and it is load-bearing in exactly the way this ratchet's escape hatch exists for, because three separate things would otherwise have to be re-derived by the next reader. (a) WHY THE TABLE COULD RETIRE RATHER THAN BE RE-KEYED - OI-21 ruled shape (i) precisely because two vocabularies needed bridging, and shape (i)'s own argument against the older `stage < level` arithmetic was that it compared two ladders that happened to line up; the equivalence was DRIVEN for all five former levels before the table was deleted, and the entry says so. (b) THE MIGRATION WINDOW, which cost two defects to get right: `PROCESS_KEY_LEGACY_VALUES` plus `_in_legacy_window`, whose docstring records that `True == 1` and `2.0 == 2` both slip into a window they were never in and that an unhashable value RAISES out of `config_conflicts`, which promises three callers it never does. (c) THE VOCABULARY ARM replacing the retired `(0, 4)` range row, with the note that a misspelled rung is the same hazard the range existed for. The dial's own "THE DIAL DOES NOT MOVE" block was REWRITTEN, not appended to: it now records that the dial moved here, deliberately, which is what WI-493's spec asked for. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +6 (2412 -> 2418) 2026-08-21, WI-498 slice 4: COMMENT ONLY, zero executable change. The `read_declared` re-export stops being documented as the reader for `docs/gate` — the gate schedule map's reader E, a documented reader no call site has ever used, which made a scheduling inventory of that file read one reader deeper than it is. The correction is longer than the false claim it replaces because it records WHY the claim could never have been true (the file is a deliberate NON-row in `PROCESS_KEYS` twenty lines below), so the next census does not re-add it. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: RE-STAMPED DOWN -2 (2414 -> 2412) 2026-08-21, WI-498 slice 0: the `LADDER_RUNGS` literal frozenset — the eight rung strings restated here under the retired F5 no-shared-module rule and held equal to `spine_rules.STAGE_ORDER` by a test pin — became a one-line import of `kitlib.ladder.LADDER_RUNGS`. Net -2 only because the restatement was replaced by the comment explaining why it is gone; the point is the pin retiring, not the two lines. Re-stamped downward in the same commit, per this file's rule. Earlier: +24 (2390 -> 2414) 2026-08-21, WI-487: the back-link campaign — literal `Implements:` declarations added near six already-anchored symbols (docstring/comment lines only, no executable change). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: -233 (2623 -> 2390) 2026-08-20, WI-448: the 270-line spec-folder registry reader this module carried VERBATIM moved to `kitlib/registry.py` (one of three identical copies — and the copy that had silently DRIFTED one comment line from the other two, which a behavioural pin could not see), and `read_declared` became a re-export of `kitlib.config.read_declared`. Re-stamped DOWNWARD in the same commit, per this file's rule. Earlier: +15 2026-08-20: WI-486 (OI-42 ruled (e)) — the new `[checks] backlink_coverage_min` dial joins PROCESS_ONLY_KEYS (it was born in process.toml, so it has no legacy file and cannot be double-declared) and PROCESS_KEY_RANGES at 0-100. Two table rows; the rest is the reason they are REQUIRED rather than optional — the dial's reader (`gen_arch_map.read_backlink_min`) answers 0/report-only for anything it cannot read, because a threshold has no conservative default to fail toward, so a quoted `backlink_coverage_min = "50"` would silently disarm a bar the repo believes it declared. This table is where that gets loud. Reviewed bump. Earlier +69 2026-08-15: D-9 step 5 follow-ons, second commit (log 2026-08-15m): OI-30 D3's ladder-derived approval authority — `APPROVAL_RUNGS` beside `DIAL_HOLDS` as its off-spine sibling plus `human_approves` mirroring `human_holds`. NOT DECOMPOSABLE: this is one predicate and one table joining the module that already owns the dial, its sibling table and the predicate it mirrors; homing it elsewhere would put half the approval policy in a second file. Most of the bump is the reasoning the sitting must be able to overturn — why the OVERTURNED declared-list proposal was overturned (the registry-to-rung association already exists in `spine_rules`), why an unmapped registry is HELD, and the writer-side contract, which is stated at the predicate because the kit ships no automated approval writer for it to sit on. Reviewed bump, reason in the log (2026-08-15m). Earlier +72 2026-08-13: WI-445 — OI-21's DIAL_HOLDS/LADDER_RUNGS declared dial-to-ladder mapping replacing the `stage < level` arithmetic, with the argument for where the two inserted rungs land (reviewed bump, reason in the log)
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
    "integrate.py": 1270,  # +5 (1265 -> 1270 SLOC) 2026-09-01, WI-552 (OI-70/OI-73): the ready-frontier check threads oi_status so a WI gated on a ruled OI is not read as never-ready (OI-73). Reviewed bump, reason in docs/log.d/WI-552-adjudicator-two-exit-close.md. Earlier: +2 (2653 -> 2655) 2026-08-31, supervisor trunk-lane fix after the first loop-driven merge post WI-548: COMMENT ONLY beside a one-name set change - out/agent-loop.lock (the loop's own coordinator lock) joins _RESIDUE_OUT_FILES; the C6 shed had removed WI-547's three streams and the lock alone held the lane (UNLOAD INCOMPLETE, exit 1). Reviewed bump, reason in the 2026-08-31 log fragment. Earlier: +27 (2626 -> 2653, post ruff-format) 2026-08-30, WI-548 (C6): the loop's OWN artifacts join the declared unload residue - out/run-logs/ (clipped copies tracked under docs/iteration/) and the out/review-owed marker - plus the prefix-aware directory sweep. Measured 2026-08-30: every mechanized lane ended UNLOAD INCOMPLETE over exactly these. Reviewed bump, reason in docs/log.d/WI-548-stall-guard.md. Earlier: +14 (2612 -> 2626) 2026-08-29, WI-534 (OI-67, the arms the split surfaced): DOCSTRING ONLY — IF-173's body (this module as the in-process library `dispatch`, `handback` and `lane` drive, the reverse of IF-055) stated beside the code; no executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi534-if-arms.md. Earlier: +7 (2605 -> 2612) 2026-08-29, WI-531 (OI-67 slice 4): DOCSTRING ONLY — the split rows of OI-67 slice 4 state their `Contract IF-###:` bodies beside the code (IF-154, the subcommand argv split off the exit-code row IF-080); no executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi531-if-row-split.md. Earlier: +8 (2597 -> 2605) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +19 (2578 -> 2597) 2026-08-22, WI-504: `branch_outcomes` reads BOTH `docs/work/` and its new archive sibling (OI-55 ruled (a)) — a close's terminal move now lands one directory deeper under `docs/archive/work/<outcome>/`, so the outcome-dir index into the split path is stated per-prefix rather than assumed constant, plus `docs/archive/work/` joins `_ADJUDICATION_SURFACES` so a disposition lane's own terminal move does not fall off the no-bar path. Reviewed bump, reason in docs/log.d/2026-08-22-wi504-history-relocation.md. Earlier: +9 (2569 -> 2578) 2026-08-22, WI-483 slice 2 — AND THE EXECUTABLE CHANGE WAS A NET DELETION. `_partial_report_refusal` lost its deferred `import handback`, its inline `+++` regex and its `ac.read_toml_text` call: the report's path, frontmatter parse and refusal all come from `kitlib.station` now, one call each. What grew is the DECLARATION — the single-line `from kitlib.station import ...` became a nine-line parenthesised list, and the function's docstring gained the paragraph recording which import was cut and why the writes stayed in `handback`. That import was a back edge of the five-module strongly connected component, so the bump buys the last edge of the cycle. Reviewed bump, reason in docs/log.d/2026-08-22-wi483-lifecycle-scc.md. Earlier: +3 (2566 -> 2569) 2026-08-21, WI-498 slice 5 recovery: COMMENT ONLY, and the executable change was a DELETION. `_ADJUDICATION_SURFACES` — a pathspec allowlist matched against `git diff --name-only` — still carried the literal `"docs/gate"` row after slice 5 deleted that file. A dead pathspec is silent in the dangerous direction: it cannot match, so it quietly NARROWS the no-bar path and fails adjudication lanes toward the full ~11-minute bar for no reason anybody could see. The row is gone and NO successor row replaces it, because `docs/stage` is declared `[generated]` and that set already joins this tuple at read time — so the comment now says that explicitly, since the next reader's obvious move is to re-add the successor by hand and silently duplicate the join. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +24 (2542 -> 2566) 2026-08-21, WI-487: the back-link campaign — literal `Implements:` declarations added near three already-anchored symbols (docstring/comment lines only, no executable change). Reviewed bump, reason in docs/log.d/2026-08-20-program-grind.md. Earlier: +12 (2530 -> 2542) 2026-08-20, WI-390 (concurrency-v2 program close, §A9.1 connectivity): a `Contracts: IF-055, IF-080` docstring paragraph, declaring the two seams (this module's read through schedule.py's pure frontier library, and this module's own CLI) that sat in the interface registry with no script declaring them - part of the drift the deletion ledger names as owed to this row, not to any single builder. Prose only; no behaviour moved. Reviewed bump, reason in the log (2026-08-20). Earlier: -11 (2541 -> 2530) 2026-08-20, WI-483 (repo review 2026-08-19 H-02, slice 1): the three terminal lane outcomes and the `Bar-Green:` attestation label moved to `kitlib/station.py`, and the "exactly ONE declared status directory, or none" decision moved with them as `outcome_of` - a pure function over a set of directory names. Reading the branch tree stays here, because that is the EFFECT; deciding what the read means is policy and is now testable without a repository. The point was never the nine lines: this module was the only home of a vocabulary its READERS needed, so the dashboard imported a merge coordinator to draw three labels - an edge of the seven-module import cycle. Re-stamped DOWNWARD in the same commit, per this file's rule. Earlier: +9 2026-08-18: the one-vocabulary rename (owner ruling; log 2026-08-18d) — the `DevBar-*` prefix retires and the SAME `DevStg-*` token names both readings, the verb carrying the axis. This module gains only the ALIAS ROWS that keep an adopter's literal value working across the re-sync (three entries plus the comment recording why the Release row resolves to `DevStg-Impl` and not `DevStg-Release` — the one mapping that is not a prefix swap, because that bar closed the Impl rung). Zero behaviour change: a canonical value resolves exactly as before. Reviewed bump, reason in the log (2026-08-18d). Earlier +7 2026-08-16: the adversarial round's F11 — the claim oracle's docstring gains the SCOPE OF "CONTENT" paragraph the WI-461 lesson owed it: every compare runs over COMMITTED BLOBS, so the repo's own clean filters define what content is, and an EOL-only edit normalized away by core.autocrlf is rightly invisible to a commit-scoped oracle (scaffolded repos pin this via the shipped .gitattributes). Prose only; no behavior moved. Reviewed bump, reason in the log (2026-08-16b). Earlier +32 2026-08-13: WI-445 — OI-21 break 3, the WI `bar:` retired-tag translation and the ladder-position (not lexical max) strictest-bar fold (reviewed bump, reason in the log)
    # `spine_rules.py` HAS NO ENTRY: 800 lines, far under the 1500 threshold, and the
    # third enter/delete cycle in five slices ENDS HERE — by the DELETION slices 1,
    # 2 and 3 each predicted rather than by the bump each declined. It was 1,523 as
    # `derive_gate.py`, holding two axes; WI-498 slice 5 deleted the bar axis, the
    # `docs/gate` writer and the whole CLI, and renamed what survives for what it
    # actually is — the spine's row predicates and rung fall-through. The module
    # oscillated around this threshold for exactly as long as it carried a second
    # job, which is the reading the ratchet was reporting all along.
    # (the deleted slice-2 tombstone, kept because the prediction it records is
    # the reason this entry exists at all:)
    # spine_rules.py: ENTRY DELETED 2026-08-21, WI-498 slice 2 — it fell to
    # 1467, back under THRESHOLD, exactly as the entry it replaces predicted
    # ("slice 2 removes the bar ordinals ... re-stamp down there"). Removed
    # rather than re-stamped low, per this file's rule that an entry under
    # the threshold is not kept as headroom.
    #   THE DROP IS SMALLER THAN THAT NOTE EXPECTED, and the reason is the
    # honest one rather than a shortfall: only the production-dead
    # STAGE_BAR/stage_to_bar crossing table died here. The bar ORDINALS,
    # BAR_NAMES, BAR_ORDER and the alias table stay, because this module
    # still WRITES docs/gate for the detectors that read its committed
    # history (phase-drop, tier signal — slice 4). They go with the file, at
    # slice 5's migration; expect the larger drop there.
    "intake.py": 1177,  # RE-STAMPED DOWN -2 (1179 -> 1177 SLOC) 2026-09-01, WI-552 REVIEW-A rework (009): a later ruff/format pass (blank-line normalization) shrank this WI's own touched file below its stamped baseline; the ratchet compares exact-equality in both directions, so the un-restamped baseline left the smoke bar red. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Reason in docs/log.d/WI-552-adjudicator-two-exit-close.md. Earlier: +3 (1176 -> 1179 SLOC) 2026-09-01, WI-552 REVIEW-A rework (cancelled-close refusal gap): the refusal invariant now reads the durable `dispose:` TITLE prefix (new `owes_successor` + `_DISPOSITION_TITLE_PREFIX`, single-sourced with the two early-close title builders) instead of the `brief == "disposition"` proxy that missed the brief-LESS cancelled arm — `specref` could not serve, the close clears it before the merge-side guard runs. Reviewed bump, reason in docs/log.d/WI-552-adjudicator-two-exit-close.md. Earlier: +2 (1174 -> 1176 SLOC) 2026-09-01, WI-552 close: ruff format canonicalization (blank-line normalization) of this WI's own touched file; no executable change. Reviewed bump, reason in docs/log.d/WI-552-adjudicator-two-exit-close.md. Earlier: +93 (1081 -> 1174 SLOC) 2026-09-01, WI-552 (OI-70/OI-73): the OI-70/OI-73 mint arms: _mint_open_item/next_oi_id/_inject_open_item (exit B), _replace_inbound_edges/_apply_supersede (inbound-edge replacement), the disposition refusal invariant, and _write_context extracted from _mint. Reviewed bump, reason in docs/log.d/WI-552-adjudicator-two-exit-close.md. Earlier: +5 (1985 -> 1990) 2026-08-30, unattended-run decision 26: a minted successor's Context carries the adjudicator's scope prose after its draft block verbatim (WI-544 review round 2 - the cells alone carry no boundary or exclusion); reviewed bump. Earlier: +1 (1984 -> 1985) 2026-08-30, unattended-run decision 25: `_draft_row` now copies a drafted successor's `supersedes` cell (LLR-161 lineage) - the row schema carried the column and the draft validator accepted the key, but the writer never wrote it, so every minted successor lost its thread; one assignment, reviewed bump. Earlier: +7 (1977 -> 1984) 2026-08-29, WI-533 follow-up (cross-family review F5): `_locate_spine_rows` reads its CSV carrier through `kitlib.spine.csv_body` like every other kit loader — read RAW, a `#` declaration header's first line became `rows[0]`, so the registry had no `Status` column, every staged row read as ABSENT and the brief reported nothing to adjudicate. The lines are the package import (both arms of the existing try/except), the `io` import beside the local `csv` one, and the four-line comment naming the trap. Reviewed bump. Earlier +14 (1963 -> 1977) 2026-08-29, WI-530 (OI-67 slice 3): DOCSTRING ONLY — the `Contract IF-###:` bodies this module owns moved out of the registry cells into its header, the one home the ruling names, and its `Contracts:` marker was trimmed to exactly the rows the registry owns to it. No executable line changed. Reviewed bump, reason in docs/log.d/2026-08-29-wi530-cell-pass.md. Earlier: +4 (1959 -> 1963) 2026-08-29, WI-528 (OI-67 ruled (a)): the seam lines a brief lists beside a touched file read the far side by its DIRECTION — `Requestors` (drawn `<-`) or `Consumers` (`->`) — plus the typed `Channel`/`Data` pair, in place of the retired `Provider`/`Contract`; the four lines are the direction arrow and the two-key far-side read in the filter. Reviewed bump, reason in docs/log.d/2026-08-29-wi528-if-row-shape.md. Earlier: -1 (1960 -> 1959) 2026-08-23, WI-455: the seam lines a brief lists beside a touched file read `Provider`/`Consumers` instead of the three retired cells, and the consumers cell is a list to scan. Reviewed bump, reason in docs/log.d/2026-08-23-wi455-rename-and-shed.md. Earlier: +23 (1937 -> 1960) 2026-08-22, WI-504: terminal history moved to `docs/archive/work/` (OI-55 ruled (a)), so every by-hand terminal-folder read now unions the active workspace and its archive sibling rather than a bare `docs/work/<status_dir>` glob — the `ARCHIVE_WORK` constant, the new `_terminal_hits` helper both `_closed_spec` and `_disposition_drafts` now call through, the `_cmd_sweep` recovery walk re-keyed onto it, and `next_wi_id`'s id-taken sweep widened to both roots (the watermark stays the primary floor; this is belt-and-suspenders against the filename sweep). NOT DECOMPOSABLE as a unit — one helper serving four call sites is the point. Reviewed bump, reason in docs/log.d/2026-08-22-wi504-history-relocation.md. Earlier: RE-STAMPED DOWN -3 (1940 -> 1937) 2026-08-22, WI-483 slice 2: the two deferred `import dispatch` statements and their blank lines went with the census extraction — the module now reads `census.parse_red_tc` / `census.gap_census` off a module-level sibling import, so the mint no longer reaches back up into the scheduling composer. Recorded DOWN in the same commit rather than left as headroom, per this file's rule. Earlier: +39 (1901 -> 1940) 2026-08-21, WI-498 slice 4 (folding WI-497): `_gate_moved` becomes `_stage_moved` — a two-point delta of `docs/stage`'s HEADLINE FIELD across the two git trees, parsed through `kitlib.stage.parse`, replacing a `splitlines()[0]` of `docs/gate` that had been reading the static do-not-hand-edit header and answering False unconditionally since the derived-gate migration. THE EXECUTABLE HALF IS ROUGHLY A WASH (a guarded kitlib import, and a loop that returns early on either side being unreadable instead of comparing two Nones); the bump is the record of a defect that was silent for a whole vocabulary generation — what it read, why line 0 stopped being the value, and why the fix is a FIELD rather than a better line index. A dead mechanism that leaves no note behind is how it gets rebuilt. Reviewed bump, reason in docs/log.d/2026-08-21-wi498-stage-unification.md. Earlier: +37 (1864 -> 1901) 2026-08-21, WI-490: OI-45 rules (b)
    # RETIRE THE MECHANICAL-APPROVAL ARM, executed. Docstring/comment-only,
    # no executable line moved: `_apply_flips`, `flip_verified`,
    # `adjudication_action`, `_cmd_adjudicate` (+ its CLI help text) and
    # `_cmd_snapshot` stop presenting the (a)/(b) resolution as an open
    # question and state the RULED shape instead — OI-45 is the record, the
    # refusal is permanent, and the "the ruling could restore a writer here"
    # hedge is gone. Per the ruling's own scope note, every touched surface
    # states the retirement is of the SCRIPT, not of agent judgment: an LLM
    # session or adjudicator may still move a Status cell through the
    # reviewed-commit path for spine content past the declared
    # human-approval level. Reviewed bump, reason in the log. Earlier +5
    # (1859 -> 1864) 2026-08-20, the batch-close iterate pass. A NET of a deletion: the `--approves REF` argument and its docstring paragraph arrive (ROUND-OPUS CRITICAL-2 / ROUND-SOL CRITICAL-1 — `intake.py snapshot` re-blessed arbitrary text with no authority check, executed end-to-end as a two-commit laundering path), while `_apply_flips`' unreachable write-and-copy block LEAVES with the dead arm (ROUND-OPUS MINOR-12: it had been unreachable since the D-9 step-7 refusal replaced the silent skip, and a source-grep test was pinning a guard on it). The gate itself lives in `baseline_snapshot` where the writer is; what lands here is the CLI surface plus the record of why approval authority was deliberately not mechanized (OI-45). Reviewed bump, reason in the log. Earlier +2 2026-08-20 (same act): ruff format normalized the step-7 edits after the stamp — measured post-format. Earlier +43 2026-08-20: D-9 migration step 7 — `if status != "Modified": continue` resolves into the explicit refusal its own comment promised (~12 executable lines: the idempotent `Approved` skip split off from a SystemExit that names the row and quotes its status). The rest is the OPEN QUESTION recorded in place rather than left for the next reader to re-derive: the one state this act ever moved FROM is retired, so the path now writes nothing, and the two candidate resolutions (re-bless drifted text under loop-hold, or retire the arm) are stated with the reason the fail-closed order is refuse-now — candidate (a) is the widest laundering surface in the kit. Reviewed bump. Earlier +8 2026-08-18: the one-vocabulary rename (owner ruling; log 2026-08-18d) — the `DevBar-*` prefix retires and the SAME `DevStg-*` token names both readings, the verb carrying the axis. This module gains only the ALIAS ROWS that keep an adopter's literal value working across the re-sync (three entries plus the comment recording why the Release row resolves to `DevStg-Impl` and not `DevStg-Release` — the one mapping that is not a prefix swap, because that bar closed the Impl rung). Zero behaviour change: a canonical value resolves exactly as before. Reviewed bump, reason in the log (2026-08-18d). Earlier +10 2026-08-15: the sitting sweep's two floor fixes, found when the suite first ran on the repo's own 3.11.9 venv. (1) `_rewrite_toml_statuses` read the registry with `Path.read_text(newline="")` — a signature that exists only from Python 3.13, so the D-9 flip writer raised TypeError on the kit's own declared 3.11 floor; the byte-preserving contract is kept via open(newline="") and the comment names the trap the suite already documented (test_generated_newlines: read_text(newline=) is 3.13+). (2) main() gains the `_utf8_console()` call every other kit CLI already makes — intake was the one CLI without it, so its refusal banners hit a Windows pipe as cp1252 and broke any UTF-8 reader (run_py's documented contract). Reviewed bump, reason in the log (sitting-sweep entry). Earlier +14 2026-08-15: D-9 step 5 follow-ons, second commit (log 2026-08-15m): `_cmd_snapshot` records WHY the snapshot path needs no `human_approves` refusal under OI-30 D3 — a COPY records a human's decision and never makes one — and names the obligation the next command that writes an `approval` would inherit. Comment only; no behaviour moved. Reviewed bump, reason in the log (2026-08-15m). Earlier +5 2026-08-15: D-9 migration step 5 — THE RENAME (log 2026-08-15m). The words moved (`Draft`->`Drafted`, `Verified`/`Planned`->`Approved`, `Planned` FOLDED per OI-30 D1) and `is_planned` was DELETED rather than re-keyed, so the net is small; the bump is the reasoning that has to travel with a rename a review sitting must be able to overturn — why `Modified` survives to step 7, why the retired words are named in place rather than silently gone, and (in `spine_rules`) why `maturity_bar` re-keys onto the ONE ladder table with a spine-only default so the rename cannot lower the derived gate. Reviewed bump, reason in the log (2026-08-15m). Earlier +64 2026-08-15: D-9 migration step 3 (log 2026-08-15g) — the snapshot becomes a WRITER here, and both callers live in this module by ruling: `_apply_flips` copies the registries after the status write (the ordering is load-bearing — the snapshot must capture the flip, or the unanchored rule reads backwards) and the `snapshot` subcommand fills the slot the retired `attest` command reserved. Roughly half is the comment recording why the mechanical arm is VACUOUS BY ABSENCE rather than a refusal: a hard failure for want of a snapshot would break adjudication in every repo that has not signed yet. `_rewrite_toml_statuses` was EXTRACTED in the same act rather than bumping the complexity ratchet — the carrier-specific write is a self-contained job with its own refusal. Reviewed bump, reason in the log (2026-08-15g). Earlier +2 2026-08-14: ruff-format catch-up — three lane worktrees' hooks skipped the format step (ruff not importable by their system python), trunk's hook then bit on the drift; mechanical reformat, no behavior change (reviewed bump, reason in the log); earlier +38 2026-08-13: WI-445 — OI-21 break 3, normalize_bar replacing the `.upper()` match that would have refused every correctly-authored DevStg-* value (reviewed bump, reason in the log); earlier +3 2026-08-13: WI-443 — the components/interfaces reads move to spine_carrier.load (reviewed bump, reason in the log)
}


def _duplicate_baseline_keys():
    """Every BASELINE dict key that appears more than once, parsed from THIS
    file's own SOURCE via `ast` rather than read off the runtime dict object.

    M-05 (repo review 2026-08-19): a plain `BASELINE = {...}` dict literal
    cannot see its own duplicates — Python's evaluation silently keeps only
    the LAST value for a repeated key, so a re-stamp that accidentally
    appends a fresh entry instead of updating the existing one in place
    leaves the earlier one dead with nothing pointing at it (this is exactly
    what happened to `bootstrap.py` until this fix, and the F601 lint was the
    only thing that noticed). Parsing the source's AST sees BOTH key nodes
    even though the runtime dict only ever binds one — which is what turns a
    duplicate into a hard error instead of a silent overwrite."""
    source = pathlib.Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=__file__)
    for node in ast.walk(tree):
        is_baseline_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "BASELINE" for t in node.targets
        )
        if not is_baseline_assign:
            continue
        seen = set()
        dupes = []
        for key_node in node.value.keys:
            if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                if key_node.value in seen:
                    dupes.append(key_node.value)
                seen.add(key_node.value)
        return dupes
    raise AssertionError("no `BASELINE = {...}` assignment found in this file")


def test_baseline_has_no_duplicate_keys():
    # M-05: a duplicate key must be a hard error at review time, not a value
    # that quietly dies under Python's last-wins dict-literal semantics — the
    # defect that let a `bootstrap.py` re-stamp silently orphan its
    # predecessor until ruff's F601 happened to notice. This parses the
    # SOURCE (see `_duplicate_baseline_keys`), so it would catch a future
    # duplicate even though the evaluated `BASELINE` dict itself cannot.
    dupes = _duplicate_baseline_keys()
    assert not dupes, (
        "BASELINE declares the same module key more than once: {} — merge into "
        "ONE entry (a deliberate re-stamp, reason in the log; never a quiet "
        "pick between the two values).".format(sorted(set(dupes)))
    )


def _all_modules():
    """{path relative to scripts/, posix: SLOC} for EVERY kit script, packages
    included.

    MEASURES SLOC SINCE 2026-08-30 (OI-68 ruled 1c) — non-blank, non-comment,
    non-docstring physical lines, via `check_complexity.module_sloc`, the one
    definition of a source line the complexity sensor also reads. It counted
    `len(text.splitlines())` (raw physical lines) until then, but roughly half
    this tree is prose by house style, so a raw count partly measured
    documentation — the owner's OI-16 correction, ruled here. The complexity
    sensor keeps the FUNCTION axis; this keeps the module-SIZE axis, now on code.

    RECURSIVE SINCE 2026-08-21 (review M-27 / Sol 6). It globbed `scripts/*.py`
    non-recursively and keyed on the bare filename, so the whole of
    `scripts/kitlib/` — the shipped shared-helper package this very batch
    created — was invisible to the census: `kitlib/registry.py` could have grown
    to 3,000 lines with this file green. Worse, a package module could not EARN
    a baseline either, contradicting this file's own escape-hatch rule that a
    new module "stays under THRESHOLD or earns its own reviewed baseline".
    Keying by relative path is what makes both halves work."""
    root = pathlib.Path(SCRIPTS)
    return {
        path.relative_to(root).as_posix(): module_sloc(path.read_text(encoding="utf-8"))
        for path in sorted(root.rglob("*.py"))
    }


def _census():
    """{module path relative to scripts/: SLOC} for every kit script over
    THRESHOLD, packages included."""
    return {name: lines for name, lines in _all_modules().items() if lines > THRESHOLD}


def test_the_census_sees_inside_packages():
    """The blindness itself, pinned — not merely the consequence.

    A count-only assertion would go quiet the moment the package moved or was
    renamed, which is the same failure it is here to prevent, so this names the
    package and asserts the census reaches it. No `kitlib/*` entry appears in
    BASELINE because none of the five is anywhere near THRESHOLD (the largest,
    `registry.py`, is a few hundred SLOC); baselines are for modules OVER the line, and
    seeding sub-threshold entries would trip this file's own shrink arm on the
    next commit. What matters is that one CAN now be seen and baselined."""
    modules = _all_modules()
    assert "kitlib/registry.py" in modules, sorted(modules)
    assert len([m for m in modules if m.startswith("kitlib/")]) >= 5
    over = {
        m: n for m, n in modules.items() if m.startswith("kitlib/") and n > THRESHOLD
    }
    assert not over, (
        "a kitlib module crossed THRESHOLD: {} — it now needs a reviewed "
        "BASELINE entry keyed by its scripts-relative path, exactly like a "
        "top-level module.".format(over)
    )


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
            "module(s) grew past baseline — decompose (WI-521), do not bump "
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
