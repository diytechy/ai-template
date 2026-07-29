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
    "gen_trajectory.py": 4967,
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
    "agent_loop.py": 3006,
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
    "trace.py": 2856,
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
    "check_trajectory.py": 3039,
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
    "bootstrap.py": 2078,
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
    "agent_common.py": 1642,
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
