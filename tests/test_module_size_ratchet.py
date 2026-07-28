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

# A module larger than this must be baselined. Set above agent_common.py (1223)
# / agent_route.py (1181) so only the six coordinators the review named are
# frozen; a routine edit to a mid-size script does not trip the ratchet, but a
# mid-size script growing into a new monolith does.
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
    "gen_trajectory.py": 5192,
    # +11 (3452 -> 3463), WI-284: _regenerate_disposition_artifacts also runs
    # `gen_trajectory.py --status` at integrate/blocked-disposition so a closed
    # id drops from the generated frontier automatically (and the disposition
    # passes its own status-map floor — WI-283's core). Reviewed bump, log 2026-07-23.
    # +70 (3463 -> 3533), WI-287: the integrator's spec close-ritual at done-flip
    # (_wi_specrefs + _archive_closed_specs + the SpecRef='' clear) so a terminal
    # WI clears its SpecRef and archives its spec — no more stranded R-F debt.
    # New behaviour, reviewed bump (log 2026-07-23). Re-stamp downward with WI-280.
    # -1 (3533 -> 3532), WI-285: _run_combined_bar delegates stack.ini
    # test-command resolution to agent_common._declared_test_command (logic moved
    # OUT to that CMP-004 shared-primitives module — no CMP-004→CMP-001 check
    # import) and drops the now-unused `import shlex` — a tightening re-stamp.
    # +6 (3532 -> 3538), WI-285 rework (REVIEW-A MAJOR): _run_combined_bar wraps
    # the bar launch in `except OSError` so a declared-but-missing binary is a RED
    # bar the integrator reworks (SR-008), not a FileNotFoundError that crashes the
    # walk-away dispatcher after the worker is ready. Reviewed bump. Re-stamp
    # downward with WI-280.
    # +76 (3538 -> 3614), WI-286: the worktree harness-interpreter fix —
    # _harness_floor_failures (preflight the ≥3.11 floor before any worker/bar
    # runs) + _activate_root_venv (point the dispatcher and every child at the
    # repo's shared .venv by absolute path) + _run_combined_bar's {py}=venv, so a
    # venv-less train worktree stops resolving ambient 3.8. New behaviour, reviewed
    # bump (reason here + in docs/log.md at integrate). Re-stamp downward with WI-280.
    # +13 (3614 -> 3627), WI-286 rework (REVIEW-A MAJOR): _harness_floor_failures
    # now FAILS CLOSED on a missing/incomplete root .venv instead of falling back to
    # the ambient interpreter — an ambient Python can clear the version floor yet
    # lack the pinned requirements-dev tools (a false green). The extra branch +
    # explicit message replace the old ambient-fallthrough. Reviewed bump. Re-stamp
    # downward with WI-280.
    # +86 (3682 -> 3768), WI-288: `_relink_archived_specs` +
    # `_redirected_link_target` — archival now redirects inbound markdown links to
    # the moved spec, resolving each link by PATH relative to its own file so one
    # rule covers every link depth. Without it archival strands a dangling link
    # (live 2026-07-24 on WI-281, WI-274 identical) that only surfaces on the
    # composed tree. Split into two functions because the single version measured
    # C901 11 and this ratchet's sibling says SIMPLIFY, don't bump — so the size
    # cost here bought a complexity baseline that stayed empty. New behaviour,
    # reviewed bump; reason in docs/log.md 2026-07-24. Re-stamp down with WI-280.
    # +121 (3768 -> 3889), WI-289: the two per-train RE-STAMPED data-file
    # resolvers — `_regen_dupes_census` (regenerate the fingerprinted census
    # from the merged tree via --emit-census, keeping the hand-authored header)
    # and `_restamp_linecount_baselines` (rewrite ONLY the numbers to the
    # merged actuals, preserving every rationale comment), plus the in-process
    # regen dispatch. These files conflict on EVERY parallel compose and both
    # sides are stale once merged, so taking a side is always wrong — this is
    # what forced the hand-integration of WI-274/276/282. New behaviour,
    # reviewed bump; reason in docs/log.md 2026-07-24. Re-stamp down w/ WI-280.
    # -4 (3889 -> 3885), WI-304: the four pre-existing `dupes` blocks are gone,
    # extracted rather than sanctioned — `_run_captured` states the subprocess
    # capture contract once for seven call sites, `_regen_failure` the regen
    # family's shared failure verdict for two. Ratcheted DOWN: the two helpers'
    # docstrings cost less than the repetition they replaced, and the five raw
    # `[-N:]` tail slices now route through `_failure_tail`. Re-stamp down with
    # WI-280.
    # +21 (3885 -> 3906), WI-304 rework after adversarial review. The bump is
    # entirely COMMENT: why `_run_combined_bar` keeps a raw bounded tail (it runs
    # the DOWNSTREAM repo's declared command, whose grammar we do not own, and
    # `_failure_tail` truncates jest/go failures to their FAIL header), why
    # `_failure_tail` is safe only in the regen family, and the `**extra` caveat.
    # That prose is load-bearing: this exact mistake was just made and shipped, so
    # the note is what stops the next author re-applying it. Reviewed bump.
    # +17 (3906 -> 3923), WI-322: the owner surface joins _DISPOSITION_REGEN
    # (a disposition edits its inputs, so it must regenerate before its own
    # commit faces the floor) and _regenerate_pending retargets from the retired
    # markdown splice to gen_open_items. Reviewed bump, log 2026-07-26.
    # +105 (3923 -> 4028), WI-353: the mirror half of the archival ritual —
    # `_rebase_moved_spec_links` re-relativises the MOVED spec's own outbound
    # links, which the inbound loop structurally cannot reach (it rewrites a link
    # whose TARGET moved; here the targets did not move, the document did). The
    # bump is smaller than it looks: the two rewriters were folded onto one
    # primitive (`_rewrite_md_links`) and one shared link-shape test
    # (`_resolvable_link`), because the same-file duplication the new half created
    # made `check_dupes` red and F5 never covers a same-file copy. Reviewed bump,
    # log 2026-07-28. Re-stamp downward with WI-280.
    # +15 (4028 -> 4043), WI-348: every text write declares its newline policy,
    # so a generated repo artifact is LF on every platform. Path.write_text
    # cannot express that on the 3.11 floor (the newline= kwarg is 3.13+), so
    # each site becomes the two-line open() form. Partly REPAID in the same
    # change: the two atomic-JSON writers were extracted to _atomic_json, which
    # retires a census sanction. Reviewed bump, log 2026-07-28.
    "agent_dispatch.py": 4042,
    "agent_loop.py": 3042,
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
    "trace.py": 2847,
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
    # This is the SIXTH consecutive upward bump with no decomposition between
    # them, and the trend is now the argument, not the individual bumps: the five
    # entries above each justify themselves and the module is still 2590 lines of
    # SHIPPED surface (bootstrap MAPPING -> every adopting repo, run by the
    # shipped pre-commit hook). WI-280 already names this module as its concrete
    # next slice; what this entry adds is that the cost is compounding at roughly
    # +90 lines per slice, which is the number to weigh against the
    # scaffold-surface change a real extraction costs. Reviewed bump, log
    # 2026-07-28.
    "check_trajectory.py": 2590,
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
    "bootstrap.py": 2007,
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
