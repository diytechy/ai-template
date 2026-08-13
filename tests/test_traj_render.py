"""gen_trajectory.py — the render primitives and the design system (WI-277:
split verbatim from tests/test_gen_trajectory.py along the WI-280 production
seams; this module's subject is `traj_render.py`).

The shared emitter vocabulary rather than any one view: the WAI-ARIA tablist
(keyboard + roving tabindex) and the tab/panel emitter helpers, the per-node
`<title>` tooltip escaping, and the declared design system — the WCAG floors on
node fills, ring ink and containment arrows, the type/weight/radius scales, the
ΔE separation between colour vocabularies, the T6 theme-lock family machinery,
and the focusable-drill a11y invariants (including the one asserted against this
repo's own shipped dashboard).
"""

import re

from conftest import ROOT, SCRIPTS, load_script
from traj_fixtures import (
    ARCH_MD,
    if_row,
    SRS,
    TIER_UNION_WIS,
    _every_emitter_document,
    _flat_bundle,
    _layer_with,
    _palette_vocabularies,
    _style_surfaces,
    _wcag,
    gen,
    gen_okf,
    html_of,
    make_repo,
    tiered_repo,
    with_bundle,
    with_gate,
)


# --- review 019: the WI-102 per-node <title> tooltip contract, pinned -----------


def _view_svg(text, marker):
    """The first SVG body after `marker` — one rendered view's node markup."""
    return text.split(marker, 1)[1].split("</svg>", 1)[0]


def test_svg_nodes_carry_escaped_title_tooltips(tmp_path):
    """Review 019 (on WI-102): the tooltip/a11y contract was untested — the one
    changed assertion made <title> optional, so a regression dropping it from
    any of the four emitters stayed green. Pin each emitter: every node <g>
    carries a <title> child, and the tip renders markup-hostile row content
    escaped."""
    make_repo(
        tmp_path,
        wis_body=(
            "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
            "WI-002,Harness <fast & loose>,scripts,SR-001,WI-001,active,harness\n"
        ),
    )
    # a markup-hostile SR title flows into the icicle and the OKF concept graph
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        SRS.replace("Core add", "Core add & <check>"), encoding="utf-8"
    )
    # the How-SW graph needs the module map + a declared seam (hostile external)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (tmp_path / "docs" / "requirements" / "interfaces.toml").write_text(
        if_row("IF-001", "Provides", "src/m", "pip & git", "cli"),
        encoding="utf-8",
    )
    assert gen_okf(tmp_path).returncode == 0  # the Knowledge tab's bundle
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = html_of(tmp_path)

    # arch_icicle: every cell carries a <title>; the SR tip renders escaped.
    ice = _view_svg(text, 'id="ice"')
    assert ice.count("<title>") == ice.count('class="cell') > 0
    assert "<title>SR-001 — Core add &amp; &lt;check&gt;</title>" in ice

    # dag_svg: every WI node carries a <title> = id — escaped title (status).
    dag = _view_svg(text, 'id="dag-view"')
    assert dag.count("<title>WI-") == 2
    assert "<title>WI-002 — Harness &lt;fast &amp; loose&gt; (active)</title>" in dag

    # sw_graph: node tips are kind-suffixed and escaped (module + external).
    sw = _view_svg(text, 'id="sw"')
    assert "<title>src/m (module)</title>" in sw
    assert "<title>pip &amp; git (external)</title>" in sw

    # Knowledge tab (collapsed drill, WI-159): every concept block carries a
    # <title> = id — title (type); the markup-hostile SR title is escaped. The
    # concept blocks live in the hidden descend layers, so scan the whole section
    # (not just the first svg, which is the type-summary root layer).
    know = text.split('id="know"', 1)[1].split("</section>", 1)[0]
    assert know.count('class="block') > 0  # concept/type blocks rendered
    assert (
        "<title>SR-001 — Core add &amp; &lt;check&gt; (System Requirement)</title>"
        in know
    )


# --- WI-273 / SR-052 (M-3): the tabs are a real WAI-ARIA tablist ---------------


def test_tabs_are_an_aria_tablist(tmp_path):
    # M-3: the view switcher used visual `.active` state only — a screen reader
    # was never told which view is selected or how buttons and panels relate. The
    # always-present arch/dag tabs now carry the full ARIA tabs pattern: a labelled
    # tablist, aria-selected on the tabs, tabpanel back-references, and a roving
    # tabindex (only the selected tab is in the tab sequence).
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'role="tablist"' in text and 'aria-label="Dashboard views"' in text
    # the initial (arch) tab is selected and the sole tab stop
    assert (
        '<button class="active" role="tab" id="tab-arch" data-tab="arch" '
        'aria-controls="arch" aria-selected="true" tabindex="0">'
    ) in text
    # every other tab starts unselected and out of the roving sequence
    assert (
        '<button role="tab" id="tab-dag" data-tab="dag" aria-controls="dag" '
        'aria-selected="false" tabindex="-1">'
    ) in text
    # panels are tabpanels wired to their tab; the inactive one is hidden
    assert (
        '<section id="arch" class="panel active" role="tabpanel" '
        'aria-labelledby="tab-arch">'
    ) in text
    assert (
        '<section id="dag" class="panel" role="tabpanel" '
        'aria-labelledby="tab-dag" hidden>'
    ) in text


def test_extra_tabs_carry_the_same_tab_semantics(tmp_path):
    # A dynamically-added tab (here How-SW, gated on a committed module map) gets
    # the identical role=tab / aria-controls / hidden-tabpanel wiring, starting
    # unselected — not just the visual button.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert (
        '<button role="tab" id="tab-sw" data-tab="sw" aria-controls="sw" '
        'aria-selected="false" tabindex="-1">'
    ) in text
    assert (
        '<section id="sw" class="panel" role="tabpanel" '
        'aria-labelledby="tab-sw" hidden>'
    ) in text


def test_every_tab_controls_a_labelled_panel(tmp_path):
    # The ARIA wiring must be complete for EVERY tab the dashboard emits: each
    # role=tab's aria-controls names a role=tabpanel whose aria-labelledby points
    # back at the tab's id. Rendered with the full optional set (How-SW + Process
    # + Knowledge) so a future tab that forgets the pattern trips here.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (tmp_path / "docs" / "gate").write_text(
        "# DERIVED GATE - generated by scripts/derive_gate.py\n"
        "# basis: SN=1 SR=2 LLR=3 TC=4 drafts=0 computed=DevBar-Tests per-phase=(none)\n"
        "DevBar-Tests\n",
        encoding="utf-8",
    )
    assert gen_okf(tmp_path).returncode == 0
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)

    tabs = re.findall(r'<button[^>]*role="tab"[^>]*>', text)
    assert len(tabs) >= 5, tabs  # arch, dag, sw, know, process
    controls = {}  # panel id -> controlling tab id
    for t in tabs:
        tid = re.search(r'id="(tab-[^"]+)"', t).group(1)
        ctl = re.search(r'aria-controls="([^"]+)"', t).group(1)
        assert re.search(r'aria-selected="(true|false)"', t), t
        assert re.search(r'tabindex="(0|-1)"', t), t
        assert ctl not in controls, "two tabs control the same panel: " + ctl
        controls[ctl] = tid

    panels = re.findall(r'<section[^>]*role="tabpanel"[^>]*>', text)
    labelled = set()
    for p in panels:
        pid = re.search(r'id="([^"]+)"', p).group(1)
        lbl = re.search(r'aria-labelledby="([^"]+)"', p).group(1)
        assert pid in controls, "panel with no controlling tab: " + pid
        assert controls[pid] == lbl, (pid, lbl)  # the two cross-reference
        labelled.add(pid)
    # a bijection: exactly one tabpanel per tab, and vice versa
    assert labelled == set(controls)


def test_tab_controller_does_keyboard_and_roving_tabindex(tmp_path):
    # The ARIA tabs pattern is behavioural: Arrow/Home/End move + activate with a
    # roving tabindex, and aria-selected + panel `hidden` stay in sync. The suite
    # runs no browser, so the controller wiring is asserted as source (the render
    # critique validates it live).
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "querySelector('nav.tabs')" in text
    assert "querySelectorAll('[role=tab]')" in text
    for key in (
        "'ArrowRight'",
        "'ArrowLeft'",
        "'ArrowDown'",
        "'ArrowUp'",
        "'Home'",
        "'End'",
    ):
        assert key in text, key
    assert "setAttribute('aria-selected', on ? 'true' : 'false')" in text
    assert "panel.hidden = !on" in text
    assert "t.tabIndex = on ? 0 : -1" in text
    assert "tab.focus()" in text  # focus follows the roving selection


def test_tab_button_and_panel_helpers_emit_the_aria_pattern():
    gt = load_script("gen_trajectory")
    b = gt.tab_button("xy", "Label X")
    for frag in (
        'role="tab"',
        'id="tab-xy"',
        'data-tab="xy"',
        'aria-controls="xy"',
        'aria-selected="false"',
        'tabindex="-1"',
        ">Label X</button>",
    ):
        assert frag in b, frag
    assert gt.tab_panel_open("xy") == (
        '<section id="xy" class="panel" role="tabpanel"'
        ' aria-labelledby="tab-xy" hidden>'
    )


# --- WI-144: the 042-CRITIQUE rubric-meeting build round (dashboard-*.md) -------
# Regression guards for the six rubric-meeting fixes (A4/U4/A3/U3/U1 done here;
# T2 knowledge-density is the round's handed-off remainder). These guard the build
# against regressions; they are NOT the owner-gated formal TC-HARDEN cases (the
# per-<text> WCAG parse / dead-selector / legend-per-fill TCs route via §5 intake).


def test_a4_node_fills_meet_the_wcag_floor():
    # dashboard-accessibility.md A4: every node fill keeps >= 4.5:1 for its label
    # text. Node text is #fff except the queued status (dark #0f172a on the light
    # gray), so every fill in the shared palette must clear the floor with one of
    # those two — the darkened palette this build lands.
    gt = load_script("gen_trajectory")
    white_fills = set(gt.STATUS_FILL.values()) - {gt.STATUS_FILL["queued"]}
    white_fills |= set(gt.TIER_FILL.values())
    white_fills |= set(gt.SW_NODE_FILL.values())
    white_fills |= set(gt.OKF_TYPE_FILL.values())
    white_fills |= set(gt.PHASE_ACCENTS)
    for fill in sorted(white_fills):
        assert _wcag("#ffffff", fill) >= 4.5, (fill, _wcag("#ffffff", fill))
    # the queued fill carries dark text instead
    assert _wcag("#0f172a", gt.STATUS_FILL["queued"]) >= 4.5


def test_a4_every_emitted_dashboard_contrast_pair_meets_floor():
    """TC-HARDEN: computed colors must catch badge/boundary/focus regressions."""
    gt = load_script("gen_trajectory")
    for status, fill in gt.STATUS_FILL.items():
        ink = "#0f172a" if status == "queued" else "#ffffff"
        assert _wcag(ink, fill) >= 4.5, (status, ink, fill)
    for fill in gt.PHASE_ACCENTS:
        assert _wcag("#ffffff", fill) >= 4.5, fill
    assert _wcag("#64748b", "#ffffff") >= 3
    assert _wcag("#64748b", "#0f172a") >= 3
    assert _wcag("#b45309", "#ffffff") >= 3


def test_every_emitted_interactive_selector_matches_a_node(tmp_path):
    """TC-HARDEN: controller selectors must not silently target dead markup."""
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert re.search(r'class="block[^>]*data-wi="WI-\d+"', page)
    assert re.search(r'class="block[^>]*data-node="[^"]+"', page)
    assert re.search(r'class="block[^>]*data-node="[^"]+"(?![^>]*data-wi=)', page)


def test_every_multifill_panel_emits_a_palette_bijection_legend(tmp_path):
    """TC-HARDEN: every phase fill is explained exactly once in the When legend."""
    gt = load_script("gen_trajectory")
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    # WI-294b: the phase legend is the `.legend` div immediately following the
    # When drill's summary paragraph (no more bespoke `phaselegend` marker class).
    anchor = "faint lines preserve the full-map context.</p>"
    legend = page.split(anchor, 1)[1].split("</div>", 1)[0]
    swatches = re.findall(r'<i style="background:(#[0-9a-f]{6})">', legend)
    assert set(swatches) == set(gt.PHASE_ACCENTS[: len(swatches)])
    assert swatches
    assert len(swatches) == len(set(swatches))


def test_a3_status_glyph_pairs_every_status_fill(tmp_path):
    # dashboard-accessibility.md A3 (no info by colour alone): a drill work-item
    # block pairs its status fill with a shape-distinct glyph in the visible label.
    gt = load_script("gen_trajectory")
    # One glyph per STATUS, not per fill (WI-272). Six statuses share four
    # swatches, so pairing glyphs with fills would have left `deferred`/`blocked`
    # — the two that share `queued`'s swatch — with no non-colour cue at all,
    # which is precisely the case A3 exists for.
    assert set(gt.STATUS_GLYPH) == set(gt.STATUS_BUCKET)
    assert set(gt.STATUS_BUCKET.values()) == set(gt.STATUS_FILL)
    assert len(set(gt.STATUS_GLYPH.values())) == len(gt.STATUS_GLYPH), (
        "two statuses share a glyph — the shape cue stops distinguishing them"
    )
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    leaf = _layer_with(html_of(tmp_path), 'data-tier="work-item"')
    labels = re.findall(r'class="blab">([^<]*)</tspan>', leaf)
    assert labels, "no work-item blocks rendered"
    glyphs = set(gt.STATUS_GLYPH.values())
    for lab in labels:
        assert lab[0] in glyphs, lab  # every leaf label is glyph-prefixed


def test_u4_when_drill_blocks_wire_to_the_detail_panel(tmp_path):
    # dashboard-{uniformity U4, usability T3, accessibility A1}: the When drill's
    # leaf blocks advertise their bare id (`data-wi`) and the page wires
    # click/focus-for-detail to them — the panel was previously dead (`#dag .wi`
    # matched zero drill blocks).
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert re.search(r'class="block[^"]*"[^>]*data-wi="WI-\d+"', view)
    assert ".block[data-wi]" in view  # the wiring loop targets the drill blocks


def test_u3_phase_legend_renders_through_the_shared_legend_component(tmp_path):
    """dashboard-uniformity.md U1/U3 (WI-294b, 119-CRITIQUE): the When tab's
    phase-accent key used to be a bespoke `span.ph`/`.phaselegend` idiom — a
    smaller swatch (.55rem vs .8rem), an inline "Phase accent:" prefix, and
    placement inside the drill's summary paragraph rather than below the card
    like every other legend (the status legend on the SAME tab, and the
    Knowledge/How-SW legends). It now renders through the identical
    `.legend`/`<i>` component those use."""
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    # the bespoke idiom is gone: no per-emitter swatch rule, no chip markup
    assert "span.ph" not in page
    assert "phaselegend" not in page
    assert 'class="ph"' not in page
    # the phase key now emits the shared component's exact markup shape
    assert re.search(
        r'<div class="legend">(<span><i style="background:#[0-9a-f]{6}"></i>[^<]+</span>)+</div>',
        page,
    )


# WI-309: the U1 residue ("whether the resulting sizes read as visually
# uniform") was undecidable only because the scale was never DECLARED. Declare
# it and the question becomes set membership — which is this test.

# The three families, and why there are three rather than one. A `rem` inside an
# SVG would resize labels out of boxes whose geometry is fixed px; an `em` sizes
# against its parent, which is the point for inline `code`. Claiming "one scale"
# across them would be false, so the invariant is "every size names a declared
# step", not "every size shares one unit".
TYPE_SCALE_FAMILIES = {
    "node (px, fixed SVG geometry)": ["--nlabel", "--nsub", "--nhead"],
    "page (rem, scales with root)": [
        "--tiny",
        "--xsmall",
        "--small",
        "--body",
        "--lead",
        "--display",
        "--hero",
    ],
    "relative (em, sizes against parent)": ["--rel"],
}


def test_u1_every_font_size_resolves_to_a_declared_scale_step(tmp_path):
    """dashboard-uniformity.md U1 core (WI-309): one declared type scale.

    Before this, 18 raw literals sat against 5 tokens — `.7rem`/`.75rem`,
    `.9`/`.95`/`.98rem`, `1.05`/`1.1rem`, `8.5px`/`9px` each being near-duplicate
    steps for ONE role, 3-7% apart. No reader distinguishes those; no rule
    justified them; and "do the sizes read as uniform?" cannot be answered about
    a scale nobody wrote down.
    """
    declared = {t for fam in TYPE_SCALE_FAMILIES.values() for t in fam}

    for label, page in _every_emitter_document(tmp_path):
        # every declared step is defined exactly once, with a real value
        for token in declared:
            defs = re.findall(
                re.escape(token) + r"\s*:\s*([0-9.]+(?:px|rem|em))\s*;", page
            )
            assert len(defs) == 1, (label, token, defs)

        used = []
        for surface in _style_surfaces(page):
            used += re.findall(r"font-size\s*:\s*([^;}\"']+)", surface)
        assert used, "vacuous — no font-size found in {}".format(label)

        raw = sorted({v.strip() for v in used if not v.strip().startswith("var(")})
        assert not raw, (
            "in the {} render, font-size(s) bypass the declared scale: {} — add a "
            "step with a stated role, or reuse the nearest one".format(label, raw)
        )
        unknown = sorted(
            {
                v.strip()
                for v in used
                if v.strip().startswith("var(")
                and re.sub(r"var\(\s*|\s*\)", "", v.strip()) not in declared
            }
        )
        assert not unknown, (label, unknown)

    # ...and the declared set stays SMALL. A scale that grows a step per call
    # site is not a scale; this is the pressure that forces the merge decision.
    assert len(declared) <= 12, sorted(declared)


# WI-310: the U3 residue ("spacing, exact visual weight") measured as drift —
# 8 stroke-widths, 7 opacities, 5 corner radii, with FIVE stroke widths doing the
# single job "draw a connector". Same declare-then-assert shape as the type scale.
WEIGHT_TOKENS = {
    "stroke-width": ["--w-hair", "--w-node", "--w-line", "--w-emph"],
    "opacity": [
        "--o-wash",
        "--o-dim",
        "--o-ghost",
        "--o-soft",
        "--o-muted",
        "--o-full",
    ],
    "border-radius": ["--r-chip", "--r-ctl", "--r-card", "--r-pill"],
}


def test_u3_every_weight_value_resolves_to_a_declared_token(tmp_path):
    """dashboard-uniformity.md U3 core (WI-310): one declared token per role for
    the properties that carry visual weight.

    `stroke-opacity` is checked under `opacity` deliberately — it is the same
    scale applied to a stroke, and letting it keep its own literals would leave
    the exact hole this closes.
    """
    for label, page in _every_emitter_document(tmp_path):
        for prop, tokens in WEIGHT_TOKENS.items():
            for token in tokens:
                defs = re.findall(re.escape(token) + r"\s*:\s*([^;]+);", page)
                assert len(defs) == 1, (label, token, defs)

            used = []
            for surface in _style_surfaces(page):
                # (?<![-\w]) so `stroke-opacity` is not eaten by `opacity`
                used += re.findall(
                    r"(?<![-\w])" + re.escape(prop) + r"\s*:\s*([^;}\"']+)", surface
                )
                if prop == "opacity":
                    used += re.findall(r"stroke-opacity\s*:\s*([^;}\"']+)", surface)
            if not used:
                continue  # this render does not exercise the property
            raw = sorted({v.strip() for v in used if not v.strip().startswith("var(")})
            assert not raw, (
                "in the {} render, {} value(s) bypass the declared tokens: {} — "
                "name the role or reuse the nearest step".format(label, prop, raw)
            )
            unknown = sorted(
                {
                    re.sub(r"var\(\s*|\s*\)", "", v.strip())
                    for v in used
                    if re.sub(r"var\(\s*|\s*\)", "", v.strip()) not in tokens
                }
            )
            assert not unknown, (label, prop, unknown)


def test_u3_svg_corner_radii_match_the_declared_scale(tmp_path):
    """U3 core, the SVG half (WI-310): `rx` is a presentation attribute and
    cannot read a CSS custom property portably, so `SVG_RX` is its declaration
    and this closes the loop — asserting the DECLARATION against both the source
    literals and every rendered document, so the tuple cannot quietly disagree
    with what the emitters actually draw.
    """
    gt = load_script("gen_trajectory")
    declared = set(gt.SVG_RX)
    assert declared, "SVG_RX is empty"

    # WI-280: the emitters live across gen_trajectory.py and its traj_* split
    # siblings now, so the literal scan follows them (one corpus, same rule).
    src = "".join(
        p.read_text(encoding="utf-8")
        for p in sorted(SCRIPTS.glob("traj_*.py")) + [SCRIPTS / "gen_trajectory.py"]
    )
    in_source = set(re.findall(r'\brx="([0-9.]+)"', src))
    assert in_source <= declared, (
        "rect template(s) draw an undeclared corner radius {} — add the role to "
        "SVG_RX or reuse a declared step".format(sorted(in_source - declared))
    )
    assert in_source, "vacuous — no rx literal found in the emitters"

    for label, page in _every_emitter_document(tmp_path):
        rendered = set(re.findall(r'\brx="([0-9.]+)"', page))
        assert rendered <= declared, (label, sorted(rendered - declared))


# WI-311: the U5 residue ("near-duplicate but non-identical hues") turned out to
# be the SAME arithmetic the phase check already did, on a set nobody had
# widened. Two floors, both judgements, both recorded here rather than in a
# commit message:
#
#   WITHIN a vocabulary — 15. Every member can sit beside every other in one
#   legend, so the bar is the strict one the phase accents already met.
#   ACROSS vocabularies — 12. Two colours from different vocabularies meet less
#   often (a status fill and a phase accent share no legend), so the bar is
#   lower — but not absent, because 120-CRITIQUE reported a reader conflating
#   exactly such a pair. 12 clears every confirmed conflation without forcing a
#   wholesale re-hue; the closest surviving pair is 12.5.
U5_FLOOR_WITHIN, U5_FLOOR_CROSS = 15.0, 12.0

# tier <-> okf is a DECLARED mirror: one concept wearing two label systems, so
# the pair is exempt by design rather than by convenience.
U5_MIRROR = {
    ("tier", "sn"): ("okf", "Stakeholder Need"),
    ("tier", "sr"): ("okf", "System Requirement"),
    ("tier", "llr"): ("okf", "Low-Level Requirement"),
    ("tier", "tc"): ("okf", "Test Case"),
}


def _u5_is_mirror(va, ka, vb, kb):
    return U5_MIRROR.get((va, ka)) == (vb, kb) or U5_MIRROR.get((vb, kb)) == (va, ka)


def test_u5_pairwise_deltae_holds_within_and_across_every_vocabulary():
    """dashboard-uniformity.md U5 core, the residue half (WI-311).

    `test_u5_phase_accents_clear_a_pairwise_deltae_floor` already applied ΔE —
    but only inside `PHASE_ACCENTS`, which is why "a reader perceives a collision
    the identity check misses" could be written off as perceptual. It is not: it
    is the same formula on the set nobody widened. When this was first run it
    found three real conflations, worst 8.6.
    """
    gt = load_script("gen_trajectory")
    vocabs = _palette_vocabularies(gt)
    flat = [(v, k, h) for v, d in vocabs.items() for k, h in d.items()]
    assert len(flat) >= 20, "vacuous — too few declared colours: {}".format(len(flat))

    worst = []
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            va, ka, ha = flat[i]
            vb, kb, hb = flat[j]
            if _u5_is_mirror(va, ka, vb, kb):
                assert ha == hb, ("a declared mirror must be byte-equal", ha, hb)
                continue
            floor = U5_FLOOR_WITHIN if va == vb else U5_FLOOR_CROSS
            d = _delta_e76(ha, hb)
            if d < floor:
                worst.append((round(d, 1), floor, va, ka, ha, vb, kb, hb))
    assert not worst, (
        "colour pair(s) below the perceptual floor — a reader cannot reliably "
        "tell these apart: {}".format(sorted(worst))
    )


# WI-312: the A2 residue ("whether each control READS as well-named"). Presence
# was already checked; QUALITY was not, and quality is largely mechanical.
#
# SCOPE, corrected during the build and worth stating: A2 governs INTERACTIVE
# elements and meaningful graphics. The first measurement counted every `<title>`
# in the document and reported 57 bare-id names — but those sit on EDGE PATHS
# (`<path class="wire"><title>IF-001</title>`), which are neither focusable nor
# named graphics. A tooltip on a decorative connector is a usability nicety, not
# an accessible-name defect, and asserting over it would have manufactured 57
# findings that WCAG does not make. Measured over the right set, the real defect
# was one: three drills each labelling their breadcrumb landmark "Breadcrumb".
_BARE_ID = re.compile(r"(?:WI|SR|SN|LLR|TC|IF|CMP)-\d+")


def _named_controls(html):
    """`[(kind, name), …]` for every focusable element and role=img graphic."""
    out = []
    for m in re.finditer(r"<(g|svg|button|nav)\b([^>]*)>", html):
        tag, attrs = m.group(1), m.group(2)
        if not (
            'tabindex="0"' in attrs or 'role="img"' in attrs or tag in ("button", "nav")
        ):
            continue
        aria = re.search(r'aria-label="([^"]*)"', attrs)
        if aria:
            out.append((tag, aria.group(1)))
            continue
        tail = html[m.end() : m.end() + 400]
        title = re.match(r"\s*<title>([^<]*)</title>", tail)
        if title:
            out.append((tag, title.group(1)))
            continue
        text = re.sub(r"<[^>]+>", "", tail.split("</" + tag + ">")[0]).strip()
        out.append((tag, text))
    return out


def test_a2_every_control_name_is_present_and_not_a_bare_id(tmp_path):
    """dashboard-accessibility.md A2 core, the QUALITY half (WI-312).

    A name that is merely present can still be useless. Two rules that hold
    everywhere: a control must HAVE a name, and that name must not be a bare
    registry id — `IF-001` tells a screen-reader user nothing about what the
    control is or does.
    """
    for label, page in _every_emitter_document(tmp_path):
        controls = _named_controls(page)
        # 10, not a bigger round number: the smallest fixture legitimately
        # renders 18 controls, and a floor tuned to the largest render would
        # fail honest small projects rather than catch a vacuous sweep.
        assert len(controls) >= 10, "vacuous — {} found {} controls".format(
            label, len(controls)
        )
        unnamed = [c for c in controls if not c[1].strip()]
        assert not unnamed, (label, "controls with no accessible name", unnamed[:5])
        bare = [c for c in controls if _BARE_ID.fullmatch(c[1].strip())]
        assert not bare, (
            "in the {} render, control(s) are named by a bare registry id, which "
            "says nothing about what they are: {}".format(label, bare[:5])
        )


def test_a2_landmark_names_are_distinct(tmp_path):
    """A2 quality, the uniqueness half (WI-312).

    Scoped to LANDMARKS (`<nav>`), deliberately. A screen-reader user listing a
    page's navigation regions hears their names as a flat list, so two called
    "Breadcrumb" are indistinguishable — which is exactly what three drills
    each emitting `aria-label="Breadcrumb"` produced.

    NOT asserted document-wide: a descend control for the same container
    legitimately appears in several drill layers, and only one layer is visible
    at a time, so those repeats are the same control reached by different paths
    rather than an ambiguity a reader ever faces.

    Note this rule is carried mainly by the SHIPPED artifact: each fixture below
    renders a single drill, so only a document with two or more navs exercises
    it (the `< 2` skip). That is a real coverage limit — verified by reverting
    the fix, which fails here only once the dashboard is regenerated.
    """
    for label, page in _every_emitter_document(tmp_path):
        names = re.findall(r"<nav\b[^>]*aria-label=\"([^\"]*)\"", page)
        if len(names) < 2:
            continue
        assert len(set(names)) == len(names), (
            "in the {} render, navigation landmarks share a name — a reader "
            "listing them cannot tell which is which: {}".format(label, sorted(names))
        )


def test_u1_process_tab_type_scale_matches_the_shared_tokens(tmp_path):
    """dashboard-uniformity.md U1 (WI-295, 119-CRITIQUE MINOR): the Process tab's
    SVG labels used to hardcode 12px/9.5px/13px/13px, deviating from the
    --nlabel:10px/--nsub:8.5px every other emitter (icicle/dag/knowledge)
    shares. `.stgt`/`.stgn` are the same per-node-label role as --nlabel/--nsub
    and reuse them directly; `.slotname` (WI-389: the station cycle's emphasized
    merge-slot node, the successor of the hoops' `.hubname` headline role) gets
    the ONE documented scale step --nhead — never an independently drifting
    magic number."""
    with_gate(tmp_path, "DevBar-Tests")  # the Process tab's render condition
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    assert "--nhead:" in css
    assert "#process .stgt{fill:var(--text);font-size:var(--nlabel)" in css
    assert "#process .stgn{fill:var(--muted);font-size:var(--nsub)" in css
    assert "#process .slotname{fill:#fff;font-size:var(--nhead)" in css
    # no ad-hoc px sizes remain on these selectors
    for selector in (".stgt", ".stgn", ".slotname"):
        rule = re.search(r"#process " + re.escape(selector) + r"\{([^}]*)\}", css)
        assert rule, selector
        assert "px" not in rule.group(1), (selector, rule.group(1))


def test_u1_node_labels_share_one_type_scale(tmp_path):
    # dashboard-uniformity.md U1: one shared node-label / sub-label size across the
    # emitters — declared once as CSS vars, referenced (no per-emitter px override).
    # The icicle + knowledge rules render in any bundle repo; the drill `.blab`
    # rule needs a tiered (drill) render.
    with_bundle(tmp_path / "bundle")
    assert gen(tmp_path / "bundle").returncode == 0
    css = html_of(tmp_path / "bundle")
    assert "--nlabel:" in css and "--nsub:" in css
    assert "#ice .cell text { fill:#fff; font-size:var(--nlabel)" in css
    assert "#knowgraph .knode text{fill:#fff;font-size:var(--nlabel)" in css
    # the specific per-emitter node-label overrides this build removed are gone
    assert "#ice .cell text { fill:#fff; font-size:10px" not in css
    assert "#knowgraph .knode text{fill:#fff;font-size:9px" not in css

    tiered_repo(tmp_path / "drill", TIER_UNION_WIS)
    assert gen(tmp_path / "drill").returncode == 0
    assert ".blab{font-size:var(--nlabel)" in html_of(tmp_path / "drill")


def _lab(hexcolor):
    """CIE L*a*b* for a `#rrggbb` string, sRGB D65 (matches the palette comment's
    deltaE convention). Pure-Python — no numpy dependency for one small check."""
    h = hexcolor.lstrip("#")
    rgb = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92 for c in rgb]
    r, g, b = [c * 100 for c in rgb]
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    xn, yn, zn = 95.047, 100.0, 108.883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _delta_e76(h1, h2):
    l1, a1, b1 = _lab(h1)
    l2, a2, b2 = _lab(h2)
    return ((l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5


def test_u5_no_hex_reused_across_unrelated_colour_vocabularies():
    """dashboard-uniformity.md U5 (WI-292, 119-CRITIQUE BLOCKER): one hue must
    carry one meaning across the whole document. Hex-collision half of the core:
    no value may repeat across STATUS_FILL / TIER_FILL / OKF_TYPE_FILL /
    SW_NODE_FILL / PHASE_ACCENTS EXCEPT the intentional TIER_FILL<->OKF_TYPE_FILL
    SN/SR/LLR/TC mirror (one concept, two label systems) and the CSS `--accent`
    token, which PHASE_ACCENTS must also never equal (the focus/hover ring is
    painted in `--accent`, so a phase sharing it makes that phase's ring
    invisible — 119-CRITIQUE A4/T5)."""
    gt = load_script("gen_trajectory")
    tier_to_type = {
        "sn": "Stakeholder Need",
        "sr": "System Requirement",
        "llr": "Low-Level Requirement",
        "tc": "Test Case",
    }
    for tier, type_name in tier_to_type.items():
        assert gt.TIER_FILL[tier] == gt.OKF_TYPE_FILL[type_name], (
            tier,
            type_name,
        )  # the mirror must pair the SAME concept, not merely reuse the same set
    mirror = set(gt.TIER_FILL[t] for t in tier_to_type)

    vocabs = {
        "status": set(gt.STATUS_FILL.values()),
        "tier+type": mirror
        | {gt.OKF_TYPE_FILL["Interface"], gt.OKF_TYPE_FILL["Process Guide"]},
        "sw": set(gt.SW_NODE_FILL.values()),
        "phase": set(gt.PHASE_ACCENTS),
    }
    names = list(vocabs)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            collide = vocabs[names[i]] & vocabs[names[j]]
            assert not collide, (names[i], names[j], collide)

    accent_light, accent_dark = "#4f46e5", "#818cf8"
    for fill in gt.PHASE_ACCENTS:
        assert fill.lower() not in (accent_light, accent_dark), fill


def test_u5_phase_accents_clear_a_pairwise_deltae_floor():
    """U5 core, pairwise half: PHASE_ACCENTS is judged as a rendered legend where
    every swatch can sit beside every other one, so the floor is PAIRWISE, not
    merely adjacent-in-declaration-order — the exact metric gap (WI-247's
    validator checked adjacent pairs only) that let two indistinguishable violets
    ship (075-CRITIQUE T5 / 119-CRITIQUE precursor)."""
    gt = load_script("gen_trajectory")
    accents = gt.PHASE_ACCENTS
    worst = min(
        _delta_e76(accents[i], accents[j])
        for i in range(len(accents))
        for j in range(i + 1, len(accents))
    )
    assert worst >= 15, worst


def test_a4_ring_ink_clears_the_3to1_floor_against_every_node_fill():
    """dashboard-accessibility.md A4 (WI-299, 119-CRITIQUE BLOCKER) +
    dashboard-usability.md T5: `_ring_ink` picks whichever of white/near-black
    contrasts more against a fill, so it must clear the 3:1 UI-boundary floor for
    EVERY fill the dashboard actually uses — not just the ones a hand-picked
    example happened to check."""
    gt = load_script("gen_trajectory")
    fills = (
        set(gt.STATUS_FILL.values())
        | set(gt.TIER_FILL.values())
        | set(gt.OKF_TYPE_FILL.values())
        | set(gt.SW_NODE_FILL.values())
        | set(gt.PHASE_ACCENTS)
    )
    for fill in sorted(fills):
        ink = gt._ring_ink(fill)
        # WI-317: the ink set is CLOSED, not incidental — the containment-arrow
        # markers are emitted one per ink, so a third value would ship an arrow
        # head with no marker to paint it.
        assert ink in gt.RING_INKS, (fill, ink, gt.RING_INKS)
        assert _wcag(ink, fill) >= 3, (fill, ink, _wcag(ink, fill))


def _theme_tokens(css, name):
    """The light and dark values of a CSS custom property, in that order (light
    `:root` first, then the `prefers-color-scheme: dark` block) — the same
    two-value shape `test_drill_focus_ring_is_distinct_from_the_active_accent`
    relies on."""
    vals = re.findall(r"--{}:(#[0-9a-f]{{3,8}})".format(name), css)
    assert len(vals) == 2, (name, vals)
    return vals


def _cedge_paint(rule_value, block_ring, accent):
    """Resolve what a browser paints for a `.cedge` shaft/head declaration, given
    the host block's inline `--ring` (absent for a theme-token fill) and the
    theme's `--accent`. Mirrors CSS `var()` fallback: `var(--ring,X)` takes the
    block's ring when it declares one, else X."""
    m = re.fullmatch(r"var\(--ring,(.+)\)", rule_value)
    if m:
        return block_ring or _cedge_paint(m.group(1), block_ring, accent)
    if rule_value == "var(--accent)":
        return accent
    assert rule_value.startswith("#"), rule_value  # a fixed hue, resolved as-is
    return rule_value


def test_t5_containment_arrow_clears_the_3to1_floor_against_every_host_fill(tmp_path):
    """dashboard-usability.md T5 / LLR-105 (WI-317, found by the WI-305 train's
    critique 2026-07-26): the containment arrow — the `.cedge` shaft plus its
    `cedgearrow` marker head — is painted INSIDE the host block, over that
    block's own fill, and it is the affordance a reader must find to descend a
    tier. So T5's 3:1 UI-boundary floor applies to it exactly as it applied to
    the focus ring WI-299 fixed, and the failure mode is the identical one:
    a single fixed hue (`var(--accent)`) vanishes on whichever fill happens to
    match it — measured 1.06:1 in light (#4f46e5 on the phase-1 #0369a1) and
    1.99:1 in dark (#818cf8 on the same fill). The paint must derive from the
    host fill's contrast-safe control token (`--ring`, LLR-105's machinery), and
    the arithmetic must close over EVERY declared fill, not a sampled one."""
    gt = load_script("gen_trajectory")
    shaft = re.search(r"\.drill \.cedge\{[^}]*stroke:([^;]+);", gt.DRILL_STYLE).group(1)
    head = re.search(r"\.drill \.cedgehead\{fill:([^;]+);", gt.DRILL_STYLE).group(1)

    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    accents = _theme_tokens(css, "accent")

    # 1. Arithmetic over the CLOSED vocabulary: every fill a descendable block can
    #    carry, in both themes — the LLR-105 closure, not a hand-picked example.
    fills = (
        set(gt.STATUS_FILL.values())
        | set(gt.TIER_FILL.values())
        | set(gt.OKF_TYPE_FILL.values())
        | set(gt.SW_NODE_FILL.values())
        | set(gt.PHASE_ACCENTS)
    )
    for fill in sorted(fills):
        ring = gt._ring_ink(fill)
        for accent in accents:
            for paint in (
                _cedge_paint(shaft, ring, accent),
                _cedge_paint(head, ring, accent),
            ):
                assert _wcag(paint, fill) >= 3, (fill, paint, _wcag(paint, fill))

    # 2. The theme-token fills (`var(--surface)` containers) keep the fallback
    #    paint, so it must clear the floor against the resolved surface too.
    for surface, accent in zip(_theme_tokens(css, "surface"), accents):
        for paint in (
            _cedge_paint(shaft, None, accent),
            _cedge_paint(head, None, accent),
        ):
            assert _wcag(paint, surface) >= 3, (surface, paint, _wcag(paint, surface))

    # 3. RENDERED, not merely declared: every emitted arrow sits in a block whose
    #    marker head resolves to that block's own ring (a shared head painted from
    #    one hue is exactly the defect — the shaft alone passing is not enough).
    blocks = [b for b in css.split('<g class="block ') if 'class="cedge"' in b]
    assert blocks, "no containment arrows emitted"
    for b in blocks:
        block = b.split("</g>", 1)[0]
        ring = re.search(r"--ring:(#[0-9a-f]{6})", block)
        marker = re.search(r'class="cedge"[^>]*marker-end="url\(#([^)]+)\)"', block)
        assert marker, block[:200]
        mdef = re.search(
            r'<marker id="{}"[^>]*?(?: style="--ring:(#[0-9a-f]{{6}})")?>'.format(
                re.escape(marker.group(1))
            ),
            css,
        )
        assert mdef, marker.group(1)
        assert mdef.group(1) == (ring.group(1) if ring else None), (
            marker.group(1),
            mdef.group(1),
            ring.group(1) if ring else None,
        )


# --- T6 theme-lock (WI-314): the anchor's mechanized core --------------------
#
# "Every surface's background/text token resolves from one theme set; no mid-page
# inversion" (the WI-300 per-anchor table, residue NONE). The measurable content
# is FAMILY PAIRING, not "no literals": a fixed status swatch carrying fixed
# white ink is theme-locked *correctly* — it never flips, and neither does its
# ink. What inverts a page is a MIXED pair (a theme-varying ink on a fixed fill,
# or fixed ink on a theme-varying surface) or a SECOND theme mechanism scoped
# below `:root`. Those are what these guards forbid.
T6_HOST_DERIVED_TOKENS = {
    # `--ring` is stamped per node (`_ring_style`) and per marker (`_cedge_marker`)
    # FROM the host fill, so it is invariant-with-an-invariant-host and varying-
    # with-a-varying-host by construction — dual by design, not unclassified.
    # Its pairing obligation is the 3:1 floor LLR-105/TC-108 own.
    "--ring",
}


def _theme_families(css):
    """`(varying, invariant)` — the CSS custom properties that change with the
    theme versus those deliberately declared once. Derived from the emitted
    document (the dark block's override set IS the definition of varying), never
    hand-listed, so a new token joins a family by existing."""
    root = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
    light = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root))
    dark_block = re.search(
        r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{(.*?)\}", css, re.S
    ).group(1)
    dark = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);?", dark_block))
    assert not set(dark) - set(light), (
        "the dark block overrides token(s) `:root` never declares — a surface "
        "that exists in only one theme: {}".format(sorted(set(dark) - set(light)))
    )
    return set(dark), set(light) - set(dark)


def _paint_family(value, varying):
    """`"varying"`, `"invariant"`, or None (not a colour) for one paint value —
    resolving `var(--token)` through the family split above."""
    value = value.strip()
    m = re.match(r"var\(\s*(--[\w-]+)", value)
    if m:
        if m.group(1) in T6_HOST_DERIVED_TOKENS:
            return None
        return "varying" if m.group(1) in varying else "invariant"
    return (
        "invariant" if re.match(r"#[0-9a-fA-F]{3,8}$|rgba?\(|hsla?\(", value) else None
    )


def _css_rules(css):
    return [
        (m.group(1).strip(), m.group(2))
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css)
    ]


def _decl(body, prop):
    m = re.search(r"(?:^|[;\s])" + prop + r"\s*:\s*([^;}]+)", body)
    return m.group(1).strip() if m else None


def test_t6_theme_lock_has_one_mechanism_and_no_mixed_family_pair(tmp_path):
    """dashboard-usability.md T6 / LLR-117 (WI-314): the dashboard renders in one
    theme at a time, applied to the whole page — no tab, panel, or node flips to
    the opposite theme mid-view. Mechanized as the two ways that can actually
    break: a theme mechanism scoped below `:root` (a second
    `prefers-color-scheme` block, or a per-component `color-scheme`), and a
    surface/ink pair drawn from two different theme families.

    Swept over EVERY emitter, not one fixture, for the A2 review's reason: a
    document walk judges only what its fixture renders, and the emitter that
    does not render is where the violation hides."""
    gt = load_script("gen_trajectory")
    vocabulary = (
        set(gt.STATUS_FILL.values())
        | set(gt.TIER_FILL.values())
        | set(gt.OKF_TYPE_FILL.values())
        | set(gt.SW_NODE_FILL.values())
        | set(gt.PHASE_ACCENTS)
    )
    nodes, pairs, seen, text_fills = 0, 0, set(), {}
    for label, page in _every_emitter_document(tmp_path):
        css = "\n".join(re.findall(r"<style>(.*?)</style>", page, re.S))
        varying, invariant = _theme_families(css)
        assert varying and invariant, (label, sorted(varying), len(invariant))

        # 1. ONE mechanism, at the root. A second block — or one scoped to a
        #    component — is precisely a mid-page seam.
        blocks = re.findall(
            r"@media\s*\([^)]*prefers-color-scheme[^)]*\)\s*\{\s*([^\s{]+)", css
        )
        assert blocks == [":root"], (label, blocks)
        schemes = [
            s.strip() for s in re.findall(r"([^{}]*)\{[^{}]*color-scheme\s*:", css)
        ]
        assert schemes == [":root"], (label, schemes)

        # 2. The page's own surface pair follows the theme — if `body` painted a
        #    fixed background or ink, the whole document would be theme-locked to
        #    one side while every card kept flipping.
        body_rule = next(
            b for s, b in _css_rules(css) if s.split(",")[0].strip() == "body"
        )
        for prop in ("background", "color"):
            assert _paint_family(_decl(body_rule, prop), varying) == "varying", (
                label,
                prop,
                _decl(body_rule, prop),
            )
        pairs += _assert_no_mixed_css_rule(label, css, varying)
        nodes += _assert_no_mixed_svg_node(label, page, varying)
        _collect_css_text_fills(page, css, varying, text_fills)
        # 6. No ad-hoc theme-locked SURFACE. Every rect fill is either a theme
        #    token (it flips) or a member of a declared colour vocabulary (a
        #    node, deliberately invariant, and A4's arithmetic already owns its
        #    ink). A literal outside both would be a fixed panel — the seam a
        #    reader crosses that the pair checks above cannot see, because a
        #    background rect carries no text of its own.
        for fill in set(re.findall(r'<rect\b[^>]*fill="([^"]+)"', page)):
            assert fill.startswith("var(") or fill in vocabulary, (label, fill)
            seen.add(_paint_family(fill, varying))
    for sel, (fams, hosts) in sorted(text_fills.items()):
        assert len(fams) == 1, (sel, fams)  # one rule, one family, every emitter
        # a text paint with a host anywhere in the sweep must match that host's
        # family; one with no host anywhere lands on the page and must follow it
        assert hosts == fams if hosts else fams == {"varying"}, (sel, fams, hosts)
    assert pairs >= 1, "vacuous — no bg/ink rule pair classified at all"
    assert nodes >= 50, "vacuous — only {} node pair(s) classified".format(nodes)
    assert len(text_fills) >= 4, "vacuous — {} css text fill(s)".format(len(text_fills))
    # both families must actually occur, or the sweep proves nothing about mixing
    assert {"varying", "invariant"} <= seen, seen


def _assert_no_mixed_css_rule(label, css, varying):
    """3. No CSS rule pairs a background and an ink from two families. Stated
    plainly rather than dressed up: the page CSS has exactly ONE rule that
    declares a classifiable background AND ink today — `body` (the rest pair an
    ink with `background:none`) — so this check's value is prospective, and the
    sweep's weight is carried by 4 and 5. The one badge idiom that pairs both
    inline is composed in JS from the invariant vocabulary, where A4's
    arithmetic (LLR-114) already owns the pairing."""
    pairs = 0
    for sel, body in _css_rules(css):
        bg = _decl(body, "background(?:-color)?")
        ink = _decl(body, "color")
        fams = {_paint_family(bg or "", varying), _paint_family(ink or "", varying)}
        if bg and ink and None not in fams:
            pairs += 1
            assert len(fams) == 1, (label, sel[:70], bg, ink, fams)
    return pairs


def _assert_no_mixed_svg_node(label, html, varying):
    """4. Same rule for every emitted SVG node: an inline rect fill and the
    inline text fill drawn on it must come from one family."""
    nodes = 0
    for g in re.findall(r"<g\b[^>]*>.*?</g>", html, re.S):
        rect = re.search(r'<rect\b[^>]*fill="([^"]+)"', g)
        text = re.search(r'<text\b[^>]*fill="([^"]+)"', g)
        if not (rect and text):
            continue
        fams = {
            _paint_family(rect.group(1), varying),
            _paint_family(text.group(1), varying),
        }
        if None in fams:
            continue
        nodes += 1
        assert len(fams) == 1, (label, rect.group(1), text.group(1), fams)
    return nodes


def _collect_css_text_fills(html, css, varying, into):
    """5. The CSS-driven half: an SVG text fill declared in a rule, paired
    against the family its host nodes actually paint in the artifact — derived
    per selector, not a hand-copied list.

    Accumulated ACROSS the sweep before judging, because "this selector has no
    host rect here" is ambiguous in a single document: it means either "the
    paint lands on the page background" (`#ice .lane-head`) or "this emitter
    does not render those nodes" (`#ice .cell` in the shipped artifact, where
    WI-306's start-collapsed drill replaced the flat icicle). Only a selector
    with no host anywhere is the former."""
    for sel, body in _css_rules(css):
        fill = _decl(body, "fill")
        if not fill or not re.search(r"\btext\b|\btspan\b", sel):
            continue
        fam = _paint_family(fill, varying)
        if fam is None:
            continue
        host = re.sub(r"\s+(?:text|tspan)\b.*$", "", sel.split(",")[0].strip())
        seen_fam, seen_hosts = into.setdefault(sel, (set(), set()))
        seen_fam.add(fam)
        seen_hosts |= _host_rect_families(html, host, varying)


def _host_rect_families(html, selector, varying):
    """The paint families of the rects belonging to `#id .cls[.cls2]` in the
    emitted document — the host surface a CSS-declared text fill lands on.
    Empty when the selector names no rect-bearing node (a lane head, an arrow
    marker), which is itself the signal that the paint sits on the page."""
    m = re.match(r"#([\w-]+)\s+\.([\w.-]+)$", selector)
    if not m:
        return set()
    region = html.split('id="{}"'.format(m.group(1)), 1)
    if len(region) < 2:
        return set()
    wanted = set(m.group(2).split("."))
    fams = set()
    for g in re.findall(r"<g\b[^>]*>.*?</g>", region[1].split("</svg>", 1)[0], re.S):
        cls = re.search(r'class="([^"]*)"', g)
        rect = re.search(r'<rect\b[^>]*fill="([^"]+)"', g)
        if not (cls and rect) or not wanted <= set(cls.group(1).split()):
            continue
        fam = _paint_family(rect.group(1), varying)
        if fam:
            fams.add(fam)
    return fams


def test_u3_ring_token_is_the_one_highlight_idiom_across_every_emitter(tmp_path):
    """dashboard-uniformity.md U3/U4 (WI-294a, 119-CRITIQUE): the hover/focus
    highlight ring used to be `var(--accent)` in the drill emitters (When/How-SW)
    but a hardcoded `#f59e0b` amber in the icicle/flat-DAG/knowledge emitters —
    two idioms for the same "this node is highlighted" concept. All four now
    read the SAME `--ring` custom property (with each emitter's old hue kept
    only as the CSS fallback), and each node carries its own computed `--ring`
    value inline so the ring clears contrast against ITS fill specifically."""
    tiered_repo(tmp_path / "drill", TIER_UNION_WIS)
    assert gen(tmp_path / "drill").returncode == 0
    css = html_of(tmp_path / "drill")
    assert ".drill .block:focus rect{stroke:var(--ring,var(--accent))" in css
    assert ".drill .block.hl rect{stroke:var(--ring,var(--accent))" in css
    assert "#ice .cell.hl rect { stroke:var(--ring,#f59e0b)" in css
    assert "#dag .wi.hl rect { stroke:var(--ring,#f59e0b)" in css
    # every emitter actually stamps a per-node --ring value, not just the CSS
    assert re.search(r'class="cell [^"]*"[^>]*style="--ring:#[0-9a-f]{6}"', css)
    assert re.search(r'class="block [^"]*"[^>]*style="--ring:#[0-9a-f]{6}"', css)

    # the Knowledge tab's top-view `.knode` flat graph only renders for a
    # <= 3-type OKF bundle (_flat_bundle) — with_bundle's SN/SR/LLR/TC spans 4
    # types, which earns the tiered drill above the threshold instead (T2).
    _flat_bundle(tmp_path / "flat")
    assert gen(tmp_path / "flat").returncode == 0
    know_css = html_of(tmp_path / "flat")
    assert "#knowgraph .knode.hl rect{stroke:var(--ring,#f59e0b)" in know_css
    assert re.search(r'class="knode"[^>]*style="--ring:#[0-9a-f]{6}"', know_css)


def test_a3_flat_dag_fallback_also_prefixes_the_status_glyph(tmp_path):
    # dashboard-accessibility A3 (046-REVIEW-A): the <=3-tier flat `dag_svg`
    # fallback (a small registry that never tiers) must encode status by the same
    # visible glyph the drill uses, not by fill hue alone. GOOD_WIS renders flat.
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)  # 4 WIs, 2 workstreams, no phases -> flat SVG DAG
    assert gen(tmp_path).returncode == 0
    dag = html_of(tmp_path).split('id="dag-view"', 1)[1].split("</svg>", 1)[0]
    wids = re.findall(r'class="wid">([^<]*)</tspan>', dag)
    assert wids, "no flat-DAG work-item labels rendered"
    glyphs = set(gt.STATUS_GLYPH.values())
    for lab in wids:
        assert lab[0] in glyphs, lab  # every id label is glyph-prefixed


def test_a1_drill_leaf_blocks_are_keyboard_focusable(tmp_path):
    # dashboard-accessibility A1 (048 BLOCKER): a leaf drill block carries a
    # click/focus detail handler (`.block[data-wi]`/`[data-node]`), so it must be
    # keyboard-focusable — not only the descend containers. Every block is now
    # `tabindex="0"`, and a leaf `data-wi` block is reachable by keyboard.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    leaf = _layer_with(html_of(tmp_path), 'data-tier="work-item"')
    blocks = re.findall(r"<g (class=\"block[^>]*)>", leaf)
    assert blocks, "no leaf work-item blocks rendered"
    for b in blocks:
        assert 'tabindex="0"' in b, b  # focusable
    # and the leaf carrying the panel wiring is itself focusable (not a container)
    assert re.search(r'tabindex="0"[^>]*data-wi="WI-\d+"', leaf)


def _svg_subtrees(text):
    """(open-tag, body) for every EMITTED <svg> — the views nest no <svg> inside
    another, so a non-greedy split is exact once the decoys are gone.

    Two decoys, both found by adversarial review of the first draft. The embedded
    JSON <script> blobs carry registry prose that can contain a literal `<svg>`
    (LLR-101's own text does), which both invents a phantom subtree and greedily
    swallows ~112 KB up to the next real `</svg>` — hiding a real container from
    the walk. So strip <script> regions first, and require the tag to carry at
    least one attribute (every emitted svg has viewBox/class; a bare `<svg>` in
    prose has none)."""
    text = re.sub(r"<script\b.*?</script>", "", text, flags=re.S)
    return re.findall(r"(<svg\s[^>]*>)(.*?)</svg>", text, re.S)


def _focusable_count(body):
    """Focusable descendants of an svg body: `tabindex` in any quoting, plus SVG
    `<a href>`, which is natively tab-ordered and so carries no tabindex."""
    return len(re.findall(r"tabindex\s*=|<a\s[^>]*href\s*=", body, re.I))


def _named(tag, body):
    """Does this svg have an accessible name? `aria-label` on the element, or a
    FIRST-DIRECT-CHILD <title> — per SVG-AAM a <title> nested inside a <g> names
    that <g>, not the svg, so accepting any descendant <title> would pass an
    unnamed graphic."""
    return "aria-label=" in tag or re.match(r"\s*<title[\s>]", body) is not None


def test_a2_no_focusable_node_sits_inside_a_children_presentational_svg(tmp_path):
    # dashboard-accessibility A2 (WI-297): role="img" is CHILDREN-PRESENTATIONAL —
    # ARIA expects the subtree pruned — so a graph holding focusable nodes must not
    # declare it, or the per-node <title>s A2 rests on may never reach a screen
    # reader and the nodes may be unreachable. Measured before the fix: 1,146 of the
    # document's 1,150 tabindex elements sat inside a role="img" subtree.
    #
    # This is the mechanized core of A2 and the reason the 116/004/118 critiques
    # split: they argued about container NAMING while the ROLE was pruning the
    # children. It asserts the invariant over the WHOLE emitted document, so any
    # future emitter that adds focusable nodes under role="img" fails here.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    subtrees = _svg_subtrees(text)
    assert subtrees, "no <svg> emitted"
    assert _focusable_count(text), "fixture emitted no focusable nodes — vacuous pass"
    for tag, body in subtrees:
        if 'role="img"' in tag:
            assert not _focusable_count(body), (
                "role=img (children-presentational) over focusable descendants: " + tag
            )
            # a genuinely non-interactive graphic still owes its own name
            assert _named(tag, body), "role=img with no accessible name: " + tag


def test_a2_role_predicate_counts_native_links_as_focusable():
    # The unit half, and the regression guard for the defect adversarial review
    # found in the first draft: focusability is NOT only `tabindex`. An SVG <a> with
    # an href is natively tab-ordered and so carries none, and a tabindex-only
    # predicate classified the loops diagram (9 linked stage cards, each with a
    # <title>) as a non-interactive graphic — leaving role="img" over exactly the
    # elements A2 protects. Also pins the quoting-agnostic and no-false-positive
    # halves, since `esc()` renders prose links as `&lt;a href`.
    gt = load_script("gen_trajectory")
    assert (
        gt._svg_role('<a href="docs/status.md" class="stg"><title>x</title></a>')
        != "img"
    )
    assert gt._svg_role('<g tabindex="0"><title>n</title></g>') != "img"
    assert gt._svg_role("<g tabindex=0></g>") != "img"
    assert gt._svg_role("<g tabindex = '0'></g>") != "img"
    # a genuinely static graphic still earns img, and escaped prose cannot forge a hit
    assert (
        gt._svg_role('<path d="M0 0"/><text>&lt;a href="x"&gt; in prose</text>')
        == "img"
    )


def test_a2_the_repos_own_shipped_dashboard_holds_the_invariant():
    # The document walk above can only judge the emitters its FIXTURE renders —
    # adversarial review measured that at 2 of 6, and the one genuine violation
    # lived in an emitter the fixture never rendered. This asserts the same
    # invariant over the artifact this repo actually ships, which exercises every
    # emitter that really renders (the loops diagram among them).
    #
    # The invariant is "not children-presentational", NOT "is role=group": dropping
    # the role (inheriting the SVG-AAM graphics-document default) or declaring
    # role="graphics-document" satisfies A2 equally, and the test must not pin one
    # implementation when LLR-101 does not.
    shipped = ROOT / "PROJECT_STATE.html"
    if not shipped.is_file():
        import pytest

        pytest.skip("no committed dashboard in this checkout")
    subtrees = _svg_subtrees(shipped.read_text(encoding="utf-8"))
    assert len(subtrees) >= 10, "decoy-stripping went wrong: {}".format(len(subtrees))
    offenders = [
        (tag[:80], _focusable_count(body))
        for tag, body in subtrees
        if 'role="img"' in tag and _focusable_count(body)
    ]
    assert not offenders, "children-presentational role over focusables: {}".format(
        offenders
    )
    assert sum(_focusable_count(b) for _, b in subtrees), "vacuous — no focusables"
