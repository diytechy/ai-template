"""gen_trajectory.py — the Knowledge / Process / landing panels (WI-277: split
verbatim from tests/test_gen_trajectory.py along the WI-280 production seams;
this module's subject is `traj_panels.py`).

The three panel families that hang off their own data source: the Knowledge tab
(the committed OKF bundle, incl. the SR-089 `>3` type-tiering rule), the Process
tab (docs/gate + the two circular working-loop diagrams, and the WCAG floors the
hub/loop paint has to clear), and the landing hero + "Next work" card that names
the ready frontier.
"""

import html
import re
import shutil

from conftest import ROOT, load_script
from traj_fixtures import (
    ARCH_MD,
    SMALL_WIS,
    _css_var,
    _flat_bundle,
    _wcag,
    gen,
    gen_okf,
    html_of,
    make_repo,
    with_bundle,
    with_gate,
)


# --- WI-070: the Knowledge tab consumes the committed OKF bundle ----------------


def test_knowledge_tab_renders_from_bundle(tmp_path):
    # C4: with a committed docs/okf/ bundle the dashboard gains the Knowledge tab
    # — typed concepts, each concept's DESCRIPTION embedded and a link-OUT to its
    # docs/okf/<tier>/<id>.md full body (the middle-path embedding, ruling #15).
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="know"' in text and 'id="know"' in text
    # WI-159: the make_repo bundle spans SN/SR/LLR/TC = 4 types (> 3), so the tab
    # opens START-COLLAPSED as the shared type-tiered drill (one block per OKF
    # type, each a descend container), NOT the flat exploded concept graph.
    assert 'class="drill"' in text and 'data-tier="okf-type"' in text
    assert 'class="knode"' not in text  # the wall-of-nodes flat graph is gone
    assert "System Requirement" in text and "Stakeholder Need" in text
    # the concept nodes live in the descend layers, keyed for the detail aside
    assert 'data-node="SN-001"' in text and 'data-node="SR-001"' in text
    # the description is embedded in the detail data...
    assert "Shall add." in text
    # ...and the link-out points at a file that actually exists beside the HTML.
    href = "docs/okf/system-requirements/SR-001.md"
    assert href in text
    assert (tmp_path / href).exists()
    # the GENERATED banner line is bundle plumbing, never rendered as content.
    assert "a reference copy, not the source of truth" not in text
    # the responsive shell still holds with the extra tab present.
    assert '<meta name="viewport" content="width=device-width' in text
    assert "@media (max-width:760px)" in text


def test_knowledge_tab_omitted_and_byte_identical_without_bundle(tmp_path):
    # The vacuity guarantee: with no docs/okf/ the tab is omitted and the artifact
    # is byte-for-byte what it was before this view existed. Proven by round-trip:
    # render bundle-less, add the bundle (tab appears), remove it, re-render ==
    # the original bytes exactly.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    without = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'data-tab="know"' not in without

    assert gen_okf(tmp_path).returncode == 0
    assert gen(tmp_path).returncode == 0
    assert b'data-tab="know"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    shutil.rmtree(tmp_path / "docs" / "okf")
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == without


def test_knowledge_tab_is_byte_deterministic(tmp_path):
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first


def test_check_stays_stable_through_regen_with_bundle(tmp_path):
    # No new --check exclusion: layout is computed from the sorted bundle at
    # generation time, so a fresh render passes --check.
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    fresh = gen(tmp_path, "--check")
    assert fresh.returncode == 0 and "up to date" in fresh.stdout


def test_malformed_okf_concept_is_skipped_with_warn(tmp_path):
    # A hand-broken bundle file must never crash the dashboard: it is skipped
    # with a stderr warn and the rest of the graph still renders.
    with_bundle(tmp_path)
    (tmp_path / "docs" / "okf" / "system-requirements" / "SR-001.md").write_text(
        "not a valid concept — no frontmatter\n", encoding="utf-8"
    )
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipping malformed OKF concept" in proc.stderr
    text = html_of(tmp_path)
    assert 'data-tab="know"' in text  # still renders
    assert 'data-node="SR-002"' in text  # the surviving concept is still a node


def test_meta_okf_bundle_renders_the_knowledge_graph():
    # Smoke test over the real meta-repo bundle (~219 concepts): the graph builds,
    # is typed, and every sampled link-out resolves to a committed file.
    gt = load_script("gen_trajectory")
    kg = gt.know_graph(ROOT)
    assert kg is not None
    svg, details = kg
    assert len(details) > 200
    assert details["SR-038"]["type"] == "System Requirement"
    assert "knowarrow" in svg
    for cid in ("SN-001", "SR-038", "TC-038"):
        assert (ROOT / details[cid]["href"]).exists()


# --- WI-159: the Knowledge graph obeys the SR-089 `>3` start-collapsed rule ------
# The T2 density fix: a bundle spanning > 3 OKF types opens COLLAPSED as the shared
# When/How-SW type-tiered drill (one block per type, descend into its concepts); a
# bundle of <= 3 types stays the flat concept graph (the tiering is earned by scale).


def _know_section(text):
    """The whole Knowledge <section> (all drill layers, incl. the hidden ones)."""
    return text.split('id="know"', 1)[1].split("</section>", 1)[0]


def test_knowledge_graph_collapses_above_type_threshold(tmp_path):
    # > 3 OKF types (the make_repo bundle spans SN/SR/LLR/TC) -> the Knowledge tab
    # opens as the shared type-tiered drill, reusing the When/How collapse
    # mechanism (`class="drill"`, one descend container per OKF type), NOT the flat
    # exploded concept graph. The WI-070 richness (descriptions + link-outs) and
    # the `>3`-earned collapse both hold.
    gt = load_script("gen_trajectory")
    with_bundle(tmp_path)
    assert gt.know_view(tmp_path) is not None  # collapse earned by > 3 types
    assert gen(tmp_path).returncode == 0
    know = _know_section(html_of(tmp_path))
    assert 'class="drill"' in know  # the shared drill mechanism, single-sourced
    assert 'class="knode"' not in know  # not the flat wall-of-nodes
    # the root layer is one descend container per OKF type (SN/SR/LLR/TC = 4)
    assert know.count('data-tier="okf-type" data-descend=') == 4
    # concepts live in the descend layers, wired (data-node) to the detail aside
    assert 'data-node="SR-001"' in know
    assert "Shall add." in know  # description survives the collapse
    assert "docs/okf/system-requirements/SR-001.md" in know  # link-out survives


def test_knowledge_graph_stays_flat_at_or_below_type_threshold(tmp_path):
    # <= 3 OKF types -> know_view returns None and the flat concept graph renders
    # (byte-identical path), exactly as when_view keeps the flat DAG below its
    # thresholds. The tiering is earned by scale, so a small bundle stays legible flat.
    gt = load_script("gen_trajectory")
    _flat_bundle(tmp_path)
    assert gt.know_view(tmp_path) is None  # <= 3 types -> no collapse
    assert gen(tmp_path).returncode == 0
    know = _know_section(html_of(tmp_path))
    assert 'class="knode"' in know  # the flat concept graph
    assert 'data-id="SR-001"' in know  # flat nodes carry data-id
    assert 'data-tier="okf-type"' not in know  # no type-tiered collapse


# --- WI-085 / SR-050: the Process reference tab ---------------------------------


def test_process_tab_renders_three_panels_from_live_data(tmp_path):
    # SR-050: with a docs/gate the dashboard gains the Process tab — the three
    # linked panels, each joining a canonical data source (docs/gate, the spine
    # registries, the docs/work/ registry) rather than restating hand-set numbers.
    # WI-389: panel 2 is the station cycle (the concurrency-v2 flow that now
    # ships), replacing the pre-station serial resume-loop chips.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="process"' in text and 'id="process"' in text
    # the three panels are present and titled
    assert "Artifact lifecycle × gates" in text
    assert "The station cycle" in text
    assert "Slices → phase → gates" in text
    # panel 1 joins the spine registries (make_repo: 1 SN, 2 SR / 1 Verified,
    # 3 LLR, 4 TC) — live counts, not prose
    assert "1 SN" in text
    assert "2 SR · 1 verified" in text
    assert "3 LLR" in text and "4 TC" in text
    assert "1 of 2 SR verified" in text
    # the pre-station picture is gone: the serial resume-loop chips and their
    # escalation bullets do not survive the redraw (their successors are the
    # handback outcome and the surface arm, asserted by the station tests).
    assert "The resume loop" not in text
    assert "Page the human" not in text
    # panel 3 states the two bars and joins the WI registry (4 WIs, 1 done)
    assert "commit bar" in text and "gate bar" in text
    assert "4 work items · 1 done." in text
    # still fully offline with the new tab present
    low = text.lower()
    assert "http://" not in low and "https://" not in low


def test_process_current_gate_highlight_follows_docs_gate(tmp_path):
    # The current-gate highlight reflects docs/gate: a stage is `now` iff the
    # gate value falls in its declared gate span.
    with_gate(tmp_path, "G1")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "Current gate: <b>G1</b>" in text
    assert 'class="stg now" data-gates="G1"' in text  # SN
    assert 'class="stg now" data-gates="G1→G2"' in text  # SR
    assert 'class="stg" data-gates="G2"' in text  # LLR not yet
    assert 'class="stg" data-gates="G3"' in text  # code+tests not yet

    (tmp_path / "docs" / "gate").write_text("G3\n", encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "Current gate: <b>G3</b>" in text
    assert 'class="stg" data-gates="G1"' in text  # SN no longer highlighted
    assert 'class="stg now" data-gates="G2→G3"' in text  # TC
    assert 'class="stg now" data-gates="G3"' in text  # code+tests


def test_process_link_outs_prefer_the_scaffolded_docs(tmp_path):
    # Link-outs resolve in THIS repo: the scaffolded docs/ copies win when
    # present (the downstream case); with neither present the scaffolded
    # default is emitted (what bootstrap writes).
    with_gate(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert 'href="docs/process.md"' in html_of(tmp_path)  # the default

    (tmp_path / "docs" / "process.md").write_text("# process\n", encoding="utf-8")
    (tmp_path / "docs" / "process-options.md").write_text("# opts\n", encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'href="docs/process.md"' in text
    assert 'href="docs/process-options.md"' in text


def test_process_wi_counts_join_work_items(tmp_path):
    # Panel 3's numbers are a live join over the WI registry (total + done counts).
    with_gate(tmp_path, "G2", SMALL_WIS)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "4 work items · 1 done." in text


def test_process_tab_omitted_and_byte_identical_without_gate(tmp_path):
    # The vacuity guarantee (the Knowledge-tab idiom): with no docs/gate the tab
    # is omitted and the artifact is byte-for-byte what it was before this view
    # existed. Proven by round-trip: render gate-less, add the gate (tab
    # appears), remove it, re-render == the original bytes exactly.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    without = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'data-tab="process"' not in without

    (tmp_path / "docs" / "gate").write_text("G1\n", encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    assert b'data-tab="process"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    (tmp_path / "docs" / "gate").unlink()
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == without


def test_process_tab_is_byte_deterministic_and_check_stable(tmp_path):
    # Sorted inputs, no clocks -> a second render is byte-identical and --check
    # passes fresh / trips stale (no new freshness exclusion).
    with_gate(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0
    # a gate flip is content: --check must trip until regenerated
    (tmp_path / "docs" / "gate").write_text("G3\n", encoding="utf-8")
    stale = gen(tmp_path, "--check")
    assert stale.returncode == 1 and "STALE" in stale.stderr


def test_meta_process_tab_smoke():
    # Over the real meta repo: the panel renders, the banner matches the real
    # docs/gate, and every link-out resolves (here the kit masters, since the
    # meta-repo scaffolds no docs/process.md).
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_registry_rows(ROOT / ct.WI_CSV))
    assert not integrity
    out = gt.process_panel(ROOT, wis, gt.spine_stats(ROOT))
    assert out is not None
    tab, panel = out
    assert 'data-tab="process"' in tab
    gate = gt._gate_value(ROOT)
    assert gate and "Current gate: <b>{}</b>".format(gate) in panel
    hrefs = set(re.findall(r'href="([^"]+)"', panel))
    assert "project-trajectory/PROCESS.md" in hrefs
    for href in hrefs:
        assert (ROOT / href).exists(), href


# --- WI-389: the station/lane cycle (docs/concurrency-v2.md, ruled 2026-07-31) --
# The station model replaced the WI-250 two-intersecting-hoops picture. The 2026-
# 08-01 diagram review's constraint governs this suite: the stage vocabulary must
# never again pin the dashboard to itself — every assertable stage name is either
# DERIVED in the panel from the shipped module's own constant (integrate.
# OUTCOME_DIRS, integrate.BAR_GREEN, schedule's kind tables) or, where a label
# has no exported constant, held by a sync pin against the module it mirrors
# (dispatch._kind_action, intake.tier_signal), so drift reds.


def _station_div(text):
    """The `<div class="station">…</div>` block (Panel 2), balanced across its
    nested `<div>`s, sliced from the rendered panel/HTML."""
    start = text.index('<div class="station">')
    depth, i = 0, start
    while i < len(text):
        if text.startswith("<div", i):
            depth += 1
        elif text.startswith("</div>", i):
            depth -= 1
            if depth == 0:
                return text[start : i + len("</div>")]
        i += 1
    raise AssertionError("unbalanced station div")


def test_process_tab_renders_the_station_cycle(tmp_path):
    # WI-389: the Process tab draws the station/lane model as one self-contained
    # SVG — the ring claim → lane build → (terminal outcomes) → station refresh
    # → merge slot → trunk advance → intake mint → dispatcher tick, drawn as a
    # single directed closed cycle.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "The station cycle" in text
    station = _station_div(text)
    assert 'class="stationsvg"' in station
    # the ring stations, present and in source order (the flow reads clockwise)
    ring = (
        "Dispatcher tick",
        "Claim",
        "Lane build",
        "Station refresh",
        "Merge slot",
        "Trunk advance",
        "Intake mint",
    )
    at = -1
    for stg in ring:
        assert ">" + stg + "<" in station, stg
        nxt = station.index(">" + stg + "<")
        assert nxt > at, "ring order broken at " + stg
        at = nxt
    # one directed closed cycle, every edge arrow-headed
    assert station.count('data-cycle="closed"') == 1
    # 6 ring edges + the dashed lost-race retry, plus one fan-out AND one fan-in
    # per declared terminal outcome. Derived rather than stamped: the literal 13
    # was correct for three outcomes and became a bare number to bump when a
    # fourth landed, which teaches a reader to bump it rather than to ask whether
    # the new outcome is actually drawn.
    n_outcomes = len(set(load_script("integrate").OUTCOME_DIRS.values()))
    assert station.count('marker-end="url(#stnarrow)"') == 7 + 2 * n_outcomes
    assert 'class="stedge alt" data-edge="slot-refresh"' in station  # lost race
    # still fully offline
    low = text.lower()
    assert "http://" not in low and "https://" not in low


def test_station_outcomes_derive_from_the_integrator(tmp_path):
    # THE SYNC PIN for §A3: the terminal-outcome cards are DERIVED from
    # integrate.OUTCOME_DIRS — the same one-home read the merge slot uses — and
    # EVERY one converges on the station refresh (one arrow each into one merge:
    # a reader cannot come away thinking a branch may hang). If the integrator's
    # outcome vocabulary moves, the render follows it.
    #
    # This assertion used to pin the count at three, and that pin was the bug it
    # was meant to prevent: when `partial/` landed the count went to four, the
    # hand-tuned layout indexed [0..2] and simply stopped drawing the fourth
    # card, and the only thing that noticed was this test failing on a number.
    # A count is not the property — COVERAGE is. The loop below now fails if any
    # declared outcome is missing a card or either of its two edges, whatever
    # the count, so a fifth outcome is caught the same way a fourth was.
    integ = load_script("integrate")
    outcomes = sorted(set(integ.OUTCOME_DIRS.values()))
    assert outcomes, "the integrator declares no terminal outcome at all"
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    station = _station_div(html_of(tmp_path))
    for outcome in outcomes:
        assert ">" + outcome + "<" in station, outcome
        # each outcome converges on the refresh — the fan-in edge exists
        assert 'data-edge="{}-refresh"'.format(outcome) in station, outcome
        # and the build stage fans out into it
        assert 'data-edge="build-{}"'.format(outcome) in station, outcome
    # the outcome notes carry the declaring spec directories, also derived
    for status_dir in integ.OUTCOME_DIRS:
        assert status_dir + "/" in station, status_dir


def test_station_slot_is_the_serial_waist(tmp_path):
    # The merge slot renders exactly once, as the emphasized (filled) node, and
    # says what makes it the waist: serial, one branch at a time, the ancestor
    # check. The slot fill is the theme-invariant --slot token (the A4 lesson).
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    station = _station_div(text)
    assert station.count('class="slot"') == 1
    assert "one branch at a time" in station
    assert "ancestor" in station
    assert "fill:var(--slot)" in text


def test_station_refresh_pins_the_bar_attestation(tmp_path):
    # THE SYNC PIN for §A2: the refresh card carries the shipped attestation
    # label (integrate.BAR_GREEN, the trailer the merge slot verifies) and the
    # refresh sequence the integrator actually runs (merge trunk in, trunk_step,
    # the bar) — derived/pinned, never folklore.
    integ = load_script("integrate")
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    station = _station_div(html_of(tmp_path))
    assert integ.BAR_GREEN.rstrip(":") in station
    assert "trunk_step" in station
    assert "merge trunk in" in station


def test_station_barrier_and_admission_arms_pin_to_the_dispatcher(tmp_path):
    # THE SYNC PIN for §A4/§A8: the spine barrier is visible, its exclusive-kind
    # vocabulary is derived from schedule's ruled tables, and the admission-arm
    # labels the panel hardcodes (they have no exported constant) are pinned to
    # dispatch._kind_action over every kind x gate-policy level — a renamed or
    # added arm reds here before the dashboard can drift.
    sched = load_script("schedule")
    disp = load_script("dispatch")
    tp = load_script("traj_panels")
    levels = ("attended", "single-ratify", "autonomous")
    truth = {
        disp._kind_action(kind, level)
        for kind in sched._KIND_CONCURRENCY
        for level in levels
    }
    assert set(tp._ADMISSION_ARMS) == truth
    # the exclusive kinds the barrier holds for, derived in rank order
    exclusive = [
        k
        for k in sorted(sched._KIND_CONCURRENCY, key=lambda k: (sched._KIND_RANK[k], k))
        if sched._KIND_CONCURRENCY[k] == sched.CONCURRENCY_EXCLUSIVE
    ]
    assert tp._exclusive_kinds() == exclusive
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "Spine barrier" in text
    station = _station_div(text)
    assert "spine barrier" in station  # the glyph label on the tick→claim edge
    for arm in truth:
        assert arm in text, arm
    for kind in exclusive:
        assert kind in text, kind


def test_station_intake_arm_pins_to_the_intake_mint(tmp_path):
    # THE SYNC PIN for §A5.2: the intake arm's trigger labels mirror intake.py's
    # shipped mint machinery. The pins are behavioral where a name is only a
    # literal inside the module: tier_signal must RECOGNIZE the amendment and
    # handback triggers (distinct tiering), and the three merge-slot draft arms
    # plus the dispatcher's rung-1 census handoff must exist as callables — a
    # reshaped intake reds here.
    ink = load_script("intake")
    disp = load_script("dispatch")
    assert ink.tier_signal("amendment", rows_touched=4) == "strong"
    assert ink.tier_signal("amendment", rows_touched=1) == "medium"
    assert ink.tier_signal("handback", reason="NEEDS-HUMAN wanted") == "strong"
    for arm in (
        ink._amendment_drafts,
        ink._handback_drafts,
        ink._disposition_drafts,
        ink.intake_after_merge,
        ink.mint_gap_rows,
        disp.gap_census,
    ):
        assert callable(arm)
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    station = _station_div(text)
    for word in ("amendment", "disposition", "draft"):
        assert word in station, word
    assert "gap census" in text  # the empty-frontier ladder, rung 1


def test_station_links_resolve():
    # Over the real meta repo (where every canonical home exists): each linked
    # stage resolves, and the station's canonical homes are the ones the flow
    # actually lands on — the WI registry (claim/intake), the log (the merged
    # record), and the owner surface (the surfaced ratification cards).
    gt = load_script("gen_trajectory")
    station = gt._station_panel(ROOT)
    hrefs = re.findall(r'href="([^"]+)"', station)
    assert hrefs, "station stages should link to their canonical homes"
    for href in hrefs:
        assert (ROOT / href).exists(), href
    for home in ("docs/work", "docs/log.md", "docs/open-items.html"):
        assert 'href="{}"'.format(home) in station, home


def test_station_byte_identical_without_data(tmp_path):
    # The station structure is the method's, not the repo's data: the block
    # renders byte-for-byte the same whether the registry is minimal or
    # work-item-rich (a data-less repo renders byte-identically).
    minimal = tmp_path / "min"
    minimal.mkdir()
    with_gate(minimal, "G2")
    assert gen(minimal).returncode == 0
    rich = tmp_path / "rich"
    rich.mkdir()
    with_gate(rich, "G2", SMALL_WIS)
    assert gen(rich).returncode == 0
    assert _station_div(html_of(minimal)) == _station_div(html_of(rich))


def test_a4_no_sub_label_opacity_discount(tmp_path):
    # A4: the emitted CSS must not discount sub-label text opacity (which dropped
    # the effective contrast below the floor). No `.sub`/`.bsub`/`.slotsub`
    # `{ ... opacity }` — the rule the old `.hubsub` joined in WI-293 (a
    # surviving `fill-opacity:.85` put the dark-theme sub-label at 2.57:1);
    # WI-389's redraw renamed the emphasized node hub → slot, same guard.
    # Fixture is with_gate, not with_bundle: `.slotsub` only exists once the
    # Process tab renders, so under with_bundle this guard was vacuous for it.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    assert ".slotsub{" in css, "Process tab did not render — guard would be vacuous"
    assert re.search(r"\.(?:sub|bsub|slotsub)\s*\{[^}]*opacity", css) is None


def test_a4_theme_token_fills_behind_white_text_meet_the_floor(tmp_path):
    """TC-HARDEN (WI-293): a fill declared as a THEME TOKEN must clear the floor
    in BOTH themes, not just the one it was designed in.

    The sibling A4 tests check palette CONSTANTS (STATUS_FILL, PHASE_ACCENTS, …),
    so a `fill:var(--token)` whose value differs per theme was invisible to them —
    which is exactly how the Process hub (now the merge slot, WI-389) shipped
    white-on-#818cf8 at 2.98:1 in dark while measuring 6.29:1 in light. Any token
    used as a fill behind white text is checked against both declarations here.
    """
    with_gate(tmp_path, "G2")  # the Process tab's render condition
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    # every custom property used as a fill under a white-text selector
    white_text_fill_tokens = {"--slot"}
    assert "fill:var(--slot)" in css, "slot fill token missing from emitted CSS"
    for token in sorted(white_text_fill_tokens):
        for dark in (False, True):
            value = _css_var(css, token, dark=dark)
            ratio = _wcag("#ffffff", value)
            assert ratio >= 4.5, (token, "dark" if dark else "light", value, ratio)


def test_a4_slot_fill_is_not_the_page_accent(tmp_path):
    """WI-293 regression guard: --accent is tuned as INK on the page background
    and lightens in dark theme, so re-pointing the slot fill at it silently
    reintroduces the 2.98:1 defect. The merge slot keeps its own token."""
    with_gate(tmp_path, "G2")  # the Process tab's render condition
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    slot_rule = re.search(r"#process \.slot rect\{([^}]*)\}", css)
    assert slot_rule, "slot rect rule missing"
    assert "var(--accent)" not in slot_rule.group(1), slot_rule.group(1)


def test_t1_hero_names_the_active_work_item(tmp_path):
    # dashboard-usability T1 (048): the landing hero names the in-flight work item
    # (id + title) so finding "the next work" costs zero tab switches. WI-002 is
    # the active row in GOOD_WIS.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    hero = text.split('class="hero"', 1)[1].split("</section>", 1)[0]
    assert 'class="sub nowat"' in hero
    assert "WI-002" in hero and "Harness" in hero  # id + title on the hero


def test_t1_hero_active_line_absent_when_nothing_is_active(tmp_path):
    # T1: no active WI -> no hero active line (empty markup, not a stray label).
    wis = (
        "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
        "WI-002,Release,docs,SR-002,WI-001,queued,shipped\n"
    )
    make_repo(tmp_path, wis)
    assert gen(tmp_path).returncode == 0
    assert 'class="sub nowat"' not in html_of(tmp_path)


# --- WI-305 (SR-054 T1): the landing "Next work" surface -----------------------
# 119-CRITIQUE's MAJOR: "find the next work" had no path — with 0 active rows
# nothing marked "you are here" and the only route to a queued item was drilling
# nested When blocks. The fix surfaces the scheduler's ready frontier (the SAME
# derivation IF-071 projects to status.md) on the landing view. The scheduler
# fails a bare row closed as `unclassified`, so these fixtures carry the minimal
# SafetyClass=ordinary signal (mirroring test_trajectory._FRONTIER_HEADER).
NW_HEADER = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SafetyClass\n"
)


def _hero_of(root):
    text = html_of(root)
    return text.split('class="hero"', 1)[1].split("</section>", 1)[0]


def test_t1_next_work_names_the_ready_frontier_with_zero_active(tmp_path):
    # The exact critique bad case: nothing is active, yet the next work must be
    # named ON THE LANDING VIEW (zero tab switches), not buried in the When drill.
    wis = (
        "WI-001,Bootstrap,scripts,SR-001,,done,adder,ordinary\n"
        "WI-002,Harness,scripts,SR-001,WI-001,queued,harness,ordinary\n"
        "WI-003,Subtraction,scripts,SR-002,WI-001,queued,subber,ordinary\n"
    )
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    hero = _hero_of(tmp_path)
    # no active row -> the old nowat line is absent, but the next-work path exists
    assert 'class="sub nowat"' not in hero
    assert 'class="card nextwork"' in hero
    assert "Next work" in hero
    # both dependency-ready WIs are named on the landing surface
    assert "WI-002" in hero and "WI-003" in hero
    # a `done` WI never appears as next work
    assert "WI-001" not in hero.split('class="nwlist"', 1)[1].split("</ul>", 1)[0]


def test_t1_next_work_annotates_the_blocking_predecessor(tmp_path):
    # A queued WI whose hard predecessor is not yet done is surfaced WITH the
    # predecessor that blocks it (the critique's "named, with their blocking
    # predecessor").
    wis = (
        "WI-001,Groundwork,scripts,SR-001,,queued,ground,ordinary\n"
        "WI-002,Release,docs,SR-002,WI-001,queued,shipped,ordinary\n"
    )
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    hero = _hero_of(tmp_path)
    assert 'class="card nextwork"' in hero
    assert "WI-001" in hero and "WI-002" in hero  # ready + waiting both listed
    assert 'class="nwafter"' in hero and "after WI-001" in hero


def test_t1_next_work_says_all_done_when_drained(tmp_path):
    # A drained registry does not render an empty surface — it says so, so the
    # landing view still answers "what's next" (nothing).
    wis = (
        "WI-001,Bootstrap,scripts,SR-001,,done,adder,ordinary\n"
        "WI-002,Release,docs,SR-002,WI-001,done,shipped,ordinary\n"
    )
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    hero = _hero_of(tmp_path)
    assert 'class="card nextwork"' in hero
    assert "All work items are done." in hero
    assert 'class="nwlist"' not in hero


# --- WI-319 / SR-054 T4: the next-work card fits its title to the CARD ---------
# 121-CRITIQUE MINOR: the card spent a fixed 60-character budget whatever width it
# had, so WI-308 read "…tiering expo…" — cut mid-word at 1680px with the card half
# empty, and nothing visible to act on. HTML already fits text to the space
# available; the budget was the only thing preventing it. `_NEXT_WORK_TITLE` now
# bounds ONE item's height rather than its text, and where it bites the remainder
# discloses through a native `<details>` (operable by pointer and keyboard, no
# script — its operability is HTML semantics, which is what makes it assertable
# from the markup at all).
_NW_LONG = (  # 109 chars — the real WI-308 clause the critic read
    "Triage the 22 dangling doc references WI-062's tiering exposed, "
    "then wire [step:doc-refs] into docs/stack.ini"
)


def _nw_items(root):
    hero = _hero_of(root)
    return hero.split('class="nwlist"', 1)[1].split("</ul>", 1)[0]


def test_t4_next_work_title_is_not_budgeted_by_character_count(tmp_path):
    # The reported shape: a clause the old fixed budget cut at 60 characters now
    # renders WHOLE, with no ellipsis anywhere in the list.
    wis = 'WI-001,"{}",docs,SR-001,,queued,d,ordinary\n'.format(_NW_LONG)
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    items = _nw_items(tmp_path)
    assert len(_NW_LONG) > 60, "vacuous - the fixture must exceed the old budget"
    assert html.unescape(items).count(_NW_LONG) == 1
    assert "…" not in items


def test_t4_an_over_bound_next_work_title_discloses_operably(tmp_path):
    # Past the bound the card still does not dead-end: a native disclosure, a
    # VISIBLE cue on it, and the whole clause present — head and remainder
    # rejoining exactly, so opening it reads continuously.
    gt = load_script("gen_trajectory")
    clause = "Bound the seam ".join(str(i) for i in range(40))
    assert len(clause) > gt._NEXT_WORK_TITLE
    make_repo(
        tmp_path,
        "WI-001,{},docs,SR-001,,queued,d,ordinary\n".format(clause),
        header=NW_HEADER,
    )
    assert gen(tmp_path).returncode == 0
    items = _nw_items(tmp_path)
    assert "<details><summary>" in items and "</details>" in items
    assert 'class="nwrev"' in items  # the cue a reader can see and click
    head, rest = items.split('<span class="nwrev">', 1)
    head = html.unescape(head.split("<details><summary>", 1)[1])
    rest = html.unescape(rest.split("</summary>", 1)[1].split("</details>", 1)[0])
    assert head + rest == clause  # nothing lost, and it rejoins cleanly
    assert head.rstrip() == head and rest.startswith(" ")  # cut at a word
    # The reveal must not depend on script (a static file opened from disk) nor be
    # hidden by the emitter's own CSS.
    css = html_of(tmp_path)
    assert ".nwt summary { cursor:pointer" in css
    assert re.search(r"\.nwt summary\s*\{[^}]*display:none", css) is None


# --- WI-315 (SR-054 T1 binding): the three core reading tasks each reach a
# LABELLED entry point within one tab switch of the landing view ----------------
# WI-300's option-(f) pattern applied to T1, the last SR-054 anchor whose
# mechanizable half had no owner. The 2026-07-26 owner ruling reworded T1 off the
# word "obvious" onto an operational gloss: each of the three core reading tasks
# (find the project state / the next work / how the parts connect) is reachable in
# <= 1 tab switch from the landing view, its entry point a LABELLED nav control or
# a NAMED landing surface. The design constraint (the whole lesson of 119-CRITIQUE's
# MAJOR): assert against the RENDERED artifact carrying real registry data, never
# the nav skeleton — a next-work surface that renders NOTHING on a zero-active
# registry passes a skeleton check but fails the reader. So the fixture reproduces
# the artifact the critic failed: zero active rows (all queued), plus a committed
# module map (ARCH_MD) so the How-SW view (task 3) is present.
T1_ALL_QUEUED = (
    "WI-001,Bootstrap the adder,scripts,SR-001,,queued,adder,ordinary\n"
    "WI-002,Wire the harness,scripts,SR-001,WI-001,queued,harness,ordinary\n"
)


def _landing_dashboard(root):
    """Render the dashboard on the T1 failure condition — zero active rows plus a
    module map, so all three reading tasks' entry points are present — and return
    (hero, navbar), the two slices of the emitted document a reader lands on."""
    make_repo(root, T1_ALL_QUEUED, header=NW_HEADER)
    (root / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(root).returncode == 0
    html = html_of(root)
    hero = html.split('class="hero"', 1)[1].split("</section>", 1)[0]
    navbar = html.split('nav class="tabs"', 1)[1].split("</nav>", 1)[0]
    return hero, navbar


def test_t1_three_core_reading_tasks_reach_labelled_entry_points(tmp_path):
    hero, navbar = _landing_dashboard(tmp_path)
    # The exact 119-CRITIQUE state: nothing is active, so the "you are here" line
    # is absent — yet every task below must still reach a labelled entry point.
    assert 'class="sub nowat"' not in hero

    # Task 1 — find the project state: NAMED landing surfaces, 0 tab switches.
    assert '<div class="label">Definition completeness</div>' in hero
    assert '<div class="label">Execution</div>' in hero

    # Task 2 — find the next work: a NAMED landing surface (0 switches) that
    # carries actual content, not an empty region (the 119-CRITIQUE defect — the
    # surface exists in the emitter but rendered nothing on zero-active data).
    assert 'class="card nextwork"' in hero
    assert '<div class="label">Next work</div>' in hero
    nwlist = hero.split('class="nwlist"', 1)[1].split("</ul>", 1)[0]
    assert "WI-001" in nwlist  # the dependency-ready WI is named, not an empty box

    # Task 3 — find how the parts connect: a LABELLED nav control (1 switch),
    # sitting directly in the tab bar — never behind a descend/expand.
    assert 'data-tab="sw"' in navbar
    assert "How (SW architecture)" in navbar
