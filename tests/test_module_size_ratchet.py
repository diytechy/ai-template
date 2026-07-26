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
    "gen_trajectory.py": 4928,
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
    "agent_dispatch.py": 3906,
    "agent_loop.py": 3042,
    # +30 (2206 -> 2236), WI-065: `tc_citation_findings` — the TC-`Verifies`
    # rules lifted out of `analyze` so the cell could accept `IF-###` seam ids.
    # Most of the bump is that helper's docstring, which is where the RULING now
    # lives (one citation cell, not a second column) — the part a successor
    # would otherwise have to reconstruct from two disagreeing checkers. The
    # extraction also ratcheted `analyze`'s complexity DOWN 53 -> 50. Reviewed
    # bump, log 2026-07-25. Re-stamp downward with WI-280.
    "trace.py": 2236,
    "check_trajectory.py": 1926,
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
    "bootstrap.py": 1986,
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
