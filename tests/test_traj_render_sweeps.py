"""gen_trajectory.py — the closure sweeps over EVERY emitter (WI-277: split
verbatim from tests/test_gen_trajectory.py along the WI-280 production seams;
this module's subject is `traj_render.py`, swept rather than sampled).

Its siblings pin one emitter at a time. These tests instead walk
`_every_emitter_document` (or the emitter source itself) and assert a CLOSED
property: every concept fill comes from one declared vocabulary, every node role
uses one interaction idiom, every wired selector resolves to a focusable
element, every painted vocabulary member is explained in words, and every hex
constant / CSS fill token is classified and floor-checked. The value is the
closure — a new emitter that forgets the idiom reds here, which a per-view test
by construction cannot do.
"""

import collections
import re

from conftest import load_script
from traj_fixtures import (
    _css_var,
    _every_emitter_document,
    _palette_vocabularies,
    _style_surfaces,
    _wcag,
    gen,
    html_of,
    make_repo,
    with_bundle,
    with_gate,
)


# --- WI-300 / SR-053: the last two uniformity anchors get a child LLR + TC -----
# U5/U3/U1 were bound by WI-292/294/295. U2 and U4 pass structurally but were
# never BOUND, so the coarse `TC-054` critique kept re-judging them by eye. These
# two tests are their cores.

# Hexes that legitimately appear in the shipped document without being a concept
# fill. Each entry names WHY, because the temptation when this test reds is to
# widen the list rather than fix the emitter — and a widened allowlist is exactly
# how a second colour vocabulary gets in.
U2_NON_CONCEPT_HEXES = {
    # `--ring`'s CSS fallback: the literal a browser uses when an emitter this
    # repo has not written yet emits a node with no computed ring ink
    # (_ring_ink's docstring states the degrade-gracefully intent). It lives in a
    # `<style>` block, so it genuinely is a paint surface — the one real entry.
    "#f59e0b",
}


def test_u2_every_concept_fill_comes_from_one_declared_vocabulary(tmp_path):
    """dashboard-uniformity.md U2 (WI-300 core): one status/phase/type colour
    vocabulary means every concept's fill is looked up from a declared palette —
    so the same concept CANNOT render two hexes, because there is only one place
    the hex can come from.

    The defect this catches is an emitter painting a concept with a LITERAL, and
    a literal is invisible to every check that reasons over the palette dicts
    (U5's collision sweep and `_ring_ink`'s enumeration both walk the DICTS).
    The How-SW `component` badge was exactly that — a four-kind vocabulary
    declaring three, with the fourth a bare `#475569` inside `cmp_block`.
    """
    gt = load_script("gen_trajectory")

    declared = set()
    for name in dir(gt):
        if not name.isupper():
            continue
        value = getattr(gt, name)
        members = value.values() if isinstance(value, dict) else value
        if isinstance(value, (dict, tuple, list)):
            declared |= {
                v.lower() for v in members if isinstance(v, str) and v.startswith("#")
            }
    assert len(declared) >= 15, "vocabulary lookup found nothing: {}".format(declared)

    for label, page in _every_emitter_document(tmp_path):
        # A `--token:#hex` definition is the theme layer (surfaces, text,
        # borders), not a concept encoding — declared once in the CSS by design.
        tokens = {
            h.lower() for h in re.findall(r"--[\w-]+:\s*(#[0-9a-fA-F]{3,8})", page)
        }
        # Only where a hex actually PAINTS. WI-311 re-hued three values, and the
        # rendered palette-rationale prose still NAMES the retired ones to
        # explain why they were retired — a whole-document scan read those as
        # emitters and would have grown `U2_NON_CONCEPT_HEXES` by one entry per
        # retirement, which is the "widen the list rather than fix it" trap that
        # list's own comment warns about. Scoping to paint surfaces makes prose
        # structurally out of scope instead.
        painted = []
        for surface in _style_surfaces(page):
            painted += re.findall(r"#[0-9a-fA-F]{6}\b", surface)
        for attr in ("fill", "stroke", "stop-color", "flood-color"):
            painted += re.findall(attr + r'="(#[0-9a-fA-F]{6})"', page)
        assert painted, "vacuous — no painted hex found in {}".format(label)
        stray = {
            h.lower()
            for h in painted
            if h.lower() not in declared
            and h.lower() not in tokens
            and h.lower() not in U2_NON_CONCEPT_HEXES
        }
        assert not stray, (
            "in the {} render, hex(es) belong to no declared vocabulary and no "
            "theme token — an emitter is painting a concept with a literal, "
            "which is a second colour vocabulary by another name: {}".format(
                label, sorted(stray)
            )
        )


def test_u4_one_interaction_idiom_per_node_role_across_every_emitter(tmp_path):
    """dashboard-uniformity.md U4 (WI-300 core): one interaction idiom per
    structure, narrowed (per the ruling) to ATTRIBUTE parity — runtime behaviour
    parity would need a browser harness.

    Two roles exist and each must be spelled ONE way everywhere:

    * an **identified** node (icicle `.cell`, flat-DAG `.wi`, knowledge `.knode`)
      advertises its registry id through `data-id`;
    * a **detail-bearing** drill node (`.block`, in both the When and How-SW
      drills) advertises its detail-map key through `data-node`.

    And every node of either role is made focusable the same way — `tabindex="0"`
    on the group. The failure this forbids is a new emitter inventing `data-key`
    or a hand-rolled focus mechanism: two spellings of one interaction, which is
    what U4 exists to catch.
    """
    roles = {
        "cell": "data-id",
        "wi": "data-id",
        "knode": "data-id",
        "block": "data-node",
    }
    seen = collections.Counter()
    for label, page in _every_emitter_document(tmp_path):
        for tag in re.findall(r"<g\b[^>]*>", page):
            cls = re.search(r'class="([^"]*)"', tag)
            if not cls:
                continue
            kind = cls.group(1).split()[0]
            if kind not in roles:
                continue
            seen[kind] += 1
            assert 'tabindex="0"' in tag, (
                "in {}, a {} node is not focusable the shared way: {}".format(
                    label, kind, tag[:120]
                )
            )
            assert roles[kind] + '="' in tag, (
                "in {}, a {} node does not carry its role's declared attribute "
                "{}: {}".format(label, kind, roles[kind], tag[:120])
            )
            # ...and does not ALSO carry the other role's attribute, which would
            # be one node addressed two ways.
            for attr in set(roles.values()) - {roles[kind]}:
                assert attr + '="' not in tag, (label, kind, attr, tag[:120])
    # EVERY declared node kind must actually have rendered. Without this the
    # sweep degrades silently into "the emitters this fixture happened to run"
    # — the exact vacuity the A2 review caught, and the reason a `knode`
    # regression slipped past this test's first draft.
    missing = sorted(set(roles) - set(seen))
    assert not missing, (
        "no node rendered for kind(s) {} — the sweep is blind to them, so it "
        "cannot claim they share the idiom (seen: {})".format(missing, dict(seen))
    )


# --- WI-313 / SR-052: bind A1/A3/A4 — the last undecomposed accessibility -----
# anchors, same shape as the U-anchor bindings above: declare the set, assert
# membership, sweep every emitter, and state the narrowing in the owning LLR.

# A1, the closure half. The page's interactivity is exactly what its emitted JS
# WIRES, so the selector list is DERIVED from the document's own
# `querySelectorAll` calls rather than hand-copied — a selector newly wired in
# an emitter fails the test until it is classified here, which is the closure
# the per-element A1 tests above (drill blocks, tabs) do not give. A `control`
# entry's matches receive per-element activation listeners (click / focus /
# dblclick / keydown), so every element they match must be keyboard-focusable;
# each non-control entry states why its matches are not focus stops.
A1_WIRED_SELECTORS = {
    ".block": "control",
    ".block[data-node]": "control",
    ".block[data-node]:not([data-wi])": "control",
    ".block[data-wi]": "control",
    ".cell": "control",
    ".wi": "control",
    ".knode": "control",
    "[data-descend]": "control",
    "[role=tab]": "control",
    ".edge": "hover-dim target — classes toggled on it, no listener attaches",
    ".wire[data-from][data-to]": (
        "focused-trace target (WI-434) — the controller reads its endpoints and "
        "toggles trace-in/trace-out on it; the wire itself takes no listener, and "
        "the reader reaches the same relationship through its two focusable blocks"
    ),
    ".trace-status": (
        "the focused-trace summary's live region (WI-434) — written to, never "
        "activated; the selection it reports is driven from the focusable blocks"
    ),
    ".kedge": "hover-dim target, the knowledge-graph spelling",
    ".layer": "drill-layer bookkeeping — shown/hidden, never a focus stop",
    ".view, .tablescroll": "scroll containers — scroll-cue listeners only",
    ".drill:not([data-ready])": "controller root marker, not a control",
    "nav.crumbs": "breadcrumb landmark — its controls are runtime <button>s",
    "nav.tabs": "tablist container — activation is delegated via closest()",
}

# Every DOM-selecting API the emitted JS may use, in any quote style. The
# adversarial review defeated the first draft (querySelectorAll + single
# quotes only) with five other spellings, two of which the emitters already
# use (querySelector('nav.crumbs'), closest('[role=tab]')).
_SELECTOR_CALL = re.compile(
    r"(?:querySelectorAll|querySelector|closest|matches)\(\s*(['\"`])(.*?)\1\s*\)"
)


def _wired_selectors(html):
    """Every selector the document's own scripts pass to a DOM-selecting API —
    and a loud failure on a NON-LITERAL selector argument, which the static
    derivation cannot see and therefore must not silently allow."""
    out = set()
    for script in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S):
        out |= {m.group(2) for m in _SELECTOR_CALL.finditer(script)}
        dynamic = re.findall(
            r"(?:querySelectorAll|querySelector|closest|matches)\(\s*[^'\"`)]", script
        )
        assert not dynamic, (
            "a DOM-selecting call takes a non-literal selector — the A1 closure "
            "cannot classify what it cannot read; use a literal: " + repr(dynamic)
        )
    return out


def _open_tags(html):
    """(tag, attrs) for every open tag in the MARKUP — scripts stripped first
    (the TC-104 decoy lesson: embedded JSON prose fakes markup), and the attr
    scan is quote-aware so a `>` inside an attribute value cannot truncate it."""
    markup = re.sub(r"<script\b.*?</script>", "", html, flags=re.S)
    return re.findall(r"<(\w+)((?:[^>\"]|\"[^\"]*\")*)>", markup)


def _a1_selector_matches(sel, attrs):
    """Match the tiny selector grammar the emitters use — `.cls`, `[attr]`,
    `[attr=v]`, and a trailing `:not([attr])`. A richer selector must extend
    this matcher deliberately (the fullmatch assert makes that loud)."""
    m = re.fullmatch(
        r"(?:\.(?P<cls>[\w-]+))?(?P<conds>(?:\[[\w-]+(?:=[\w-]+)?\])*)"
        r"(?::not\(\[(?P<neg>[\w-]+)\]\))?",
        sel,
    )
    assert m, "selector grammar not handled by this matcher: " + sel
    if m.group("cls"):
        cls = re.search(r'class="([^"]*)"', attrs)
        if not cls or m.group("cls") not in cls.group(1).split():
            return False
    for name, val in re.findall(r"\[([\w-]+)(?:=([\w-]+))?\]", m.group("conds")):
        if val:
            if not re.search(re.escape(name) + r'="' + re.escape(val) + r'"', attrs):
                return False
        elif name + '="' not in attrs:
            return False
    if m.group("neg") and m.group("neg") + '="' in attrs:
        return False
    return True


def _a1_focusable(tag, attrs):
    """Keyboard-focusable: explicit `tabindex="0"`, or natively tab-ordered — a
    `<button>` (the roving-tabindex tabs stay buttons), or an `<a href>` (the
    LLR-101 lesson: a native SVG link carries no tabindex and needs none)."""
    return (
        'tabindex="0"' in attrs or tag == "button" or (tag == "a" and "href=" in attrs)
    )


def test_a1_every_wired_interaction_selector_matches_only_focusable_elements(
    tmp_path,
):
    """dashboard-accessibility.md A1 core (WI-313): every element the page wires
    an interaction to is reachable by keyboard.

    The per-element tests above check KNOWN controls (drill leaves, tabs); what
    none of them assert is the CLOSURE — that the set of wired selectors and the
    set of focusable elements cannot drift apart. Deriving the selectors from
    the emitted JS closes it from one side (a new wired selector fails until
    classified); asserting every declared selector is seen and every control
    selector matches somewhere closes it from the other (a stale entry, or a
    sweep gone blind, also fails).
    """
    seen_selectors = set()
    matched = collections.Counter()
    for label, page in _every_emitter_document(tmp_path):
        wired = _wired_selectors(page)
        unclassified = wired - set(A1_WIRED_SELECTORS)
        assert not unclassified, (
            "in the {} render, the page wires selector(s) this test has no "
            "focusability classification for — decide control vs container and "
            "add them to A1_WIRED_SELECTORS: {}".format(label, sorted(unclassified))
        )
        seen_selectors |= wired
        tags = _open_tags(page)
        for sel, role in A1_WIRED_SELECTORS.items():
            if role != "control" or sel not in wired:
                continue
            for tag, attrs in tags:
                if _a1_selector_matches(sel, attrs):
                    matched[sel] += 1
                    assert _a1_focusable(tag, attrs), (
                        "in the {} render, a wired control is not keyboard-"
                        "focusable: {} matched <{}{}>".format(
                            label, sel, tag, attrs[:120]
                        )
                    )
    stale = set(A1_WIRED_SELECTORS) - seen_selectors
    assert not stale, (
        "classified selector(s) never appeared in any render — the entry is "
        "stale or the sweep is blind: {}".format(sorted(stale))
    )
    unexercised = {s for s, r in A1_WIRED_SELECTORS.items() if r == "control"} - set(
        matched
    )
    assert not unexercised, (
        "control selector(s) matched no element anywhere — vacuous: {}".format(
            sorted(unexercised)
        )
    )


def test_a1_focus_walk_follows_document_order(tmp_path):
    """A1's "sensible order" residue, narrowed to what is assertable (the
    WI-300 ruling's recorded recommendation): document order IS emission order,
    and the focus walk follows document order as long as nothing carries a
    positive tabindex. The only values the page may use are `0` (join the walk
    in document order) and `-1` — and every `-1` must sit on a tablist button,
    where the WI-273 roving-tabindex controller owns the order via arrow keys.
    Whether that order FEELS sensible is the perceptual half the ruling dropped,
    stated in LLR-112 as the scope narrowing.
    """
    for label, page in _every_emitter_document(tmp_path):
        seen = 0
        for tag, attrs in _open_tags(page):
            ti = re.search(r"tabindex\s*=\s*\"?(-?\d+)\"?", attrs)
            if not ti:
                continue
            seen += 1
            assert ti.group(1) in ("0", "-1"), (
                "in the {} render, a positive tabindex reorders the focus "
                "walk: <{}{}>".format(label, tag, attrs[:120])
            )
            if ti.group(1) == "-1":
                assert tag == "button" and 'role="tab"' in attrs, (
                    "in the {} render, tabindex=-1 outside the roving tablist "
                    "removes a control from the walk: <{}{}>".format(
                        label, tag, attrs[:120]
                    )
                )
        assert seen, "vacuous — no tabindex found in {}".format(label)


# A3 (no information by colour alone), the closure half. The status glyphs and
# the flat-DAG fallback are owned above; what was never asserted is that EVERY
# vocabulary member that paints is explained somewhere in words.
def _legend_swatches(html):
    """[(resolved-hex-or-raw-value, label), …] for every legend swatch, with
    `var()` resolved against the document's own token definitions — the status
    legend paints via `var(--done)` etc., and a raw hex scan under-reports it."""
    tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", html))
    out = []
    for m in re.finditer(r'<i style="background:([^"]+)"></i>\s*([^<]*)', html):
        value = m.group(1).strip()
        var = re.fullmatch(r"var\((--[\w-]+)\)", value)
        if var:
            value = tokens.get(var.group(1), value)
        out.append((value.lower(), m.group(2).strip()))
    return out


def test_a3_every_painted_vocabulary_member_is_explained_in_words(tmp_path):
    """dashboard-accessibility.md A3 core (WI-313): for every declared colour
    vocabulary, every member that actually PAINTS in a document resolves to a
    legend swatch labelled in words in that same document.

    The vocabularies are enumerated from the module (`_palette_vocabularies`,
    the U5 closure), so a new vocabulary cannot ship without entering this
    sweep. SCOPE, and its narrowing (LLR-113): the cue must exist in the same
    document — that it sits within eyeshot of the painted element is layout
    this does not re-assert. The JS-rendered detail-panel badge is out of scope
    because its background carries its concept as the badge's own visible text
    (`esc(d.kind)`), so that colour never carries the information alone.
    """
    gt = load_script("gen_trajectory")
    vocabs = _palette_vocabularies(gt)
    explained = collections.Counter()
    for label, page in _every_emitter_document(tmp_path):
        markup = re.sub(r"<script\b.*?</script>", "", page, flags=re.S)
        painted = " ".join(_style_surfaces(markup))
        for attr in ("fill", "stroke"):
            painted += " " + " ".join(
                re.findall(attr + r'="(#[0-9a-fA-F]{6})"', markup)
            )
        painted = painted.lower()
        worded = {h for h, lab in _legend_swatches(markup) if lab}
        for vname, members in vocabs.items():
            for key, hx in members.items():
                if hx.lower() not in painted:
                    continue
                explained[vname] += 1
                assert hx.lower() in worded, (
                    "in the {} render, {}[{}] paints {} but no legend swatch "
                    "explains that colour in words — the encoding is colour-"
                    "alone for a reader who cannot perceive it".format(
                        label, vname, key, hx
                    )
                )
    missing = set(vocabs) - set(explained)
    assert not missing, (
        "no render painted any member of vocabulary(ies) {} — the sweep is "
        "blind to them and cannot claim they are explained".format(sorted(missing))
    )


def test_a3_icicle_tier_legend_swatches_are_the_painted_tier_palette(tmp_path):
    """The defect this WI found on first measurement (the method's rule 1,
    again): the What-tab tier legend HARDCODED its four swatches, and its TC
    swatch kept a pre-WI-311 hex that had since become `STATUS_FILL["done"]` —
    so the legend labelled the done-green "TC" while the actual TC cells
    painted `TIER_FILL["tc"]`, and the document-wide check above stayed green
    only because the Knowledge tab's own legend covered the real hex. The
    legend now derives from TIER_FILL; this pins the bijection the same way
    `test_every_multifill_panel_emits_a_palette_bijection_legend` pins the
    phase legend's. Expected is built from the DICT, not a key tuple, so a
    fifth tier member missing from the legend also fails (adversarial-review
    hardening — emitter and test previously shared the same literal tuple)."""
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    legend = page.split('id="arch-detail"', 1)[1]
    legend = legend.split('<div class="legend">', 1)[1].split("</div>", 1)[0]
    entries = re.findall(r'<i style="background:(#[0-9a-f]{6})"></i>([A-Z]+)', legend)
    assert entries == [(fill, tier.upper()) for tier, fill in gt.TIER_FILL.items()], (
        entries
    )


def test_a3_js_detail_maps_mirror_the_declared_palettes(tmp_path):
    """A3, the JS half (adversarial-review finding F1): the detail-panel badge
    paints from `const tierColor` / `const statusColor` maps in the emitted
    main script. Those used to be HAND-COPIED literals — and kept the same
    stale pre-WI-311 tc hex the static legend fix eliminated, so clicking a TC
    cell rendered a badge in the done-green while the cell and the legend both
    said `TIER_FILL["tc"]`. The maps are now substituted from the constants;
    this holds every emitted copy byte-equal to the Python palettes, so a
    hand-copy cannot come back.

    FRESH-ONLY (WI-372's truth-times rule, applied at WI-384). The claim is
    about THIS emitter's substitution, and the committed `shipped` document was
    written by an older renderer against an older palette — so any RENAME in the
    vocabulary (WI-384: `retired` -> `cancelled`) reds through the stale copy
    while the emitter under test is clean, which is the exact mis-triage that
    note warns about. No replacement fixture is owed: every fresh document emits
    both maps, and the per-document `seen >= 2` floor below keeps that honest."""
    gt = load_script("gen_trajectory")
    for label, page in _every_emitter_document(tmp_path):
        if label == "shipped":
            continue
        seen = 0
        for name, expect in (
            ("tierColor", gt.TIER_FILL),
            ("statusColor", gt.STATUS_FILL),
        ):
            for m in re.finditer(r"const " + name + r" = (\{[^;]*?\});", page):
                got = dict(
                    re.findall(
                        r"[\"']?(\w+)[\"']?\s*:\s*[\"'](#[0-9a-fA-F]{6})[\"']",
                        m.group(1),
                    )
                )
                seen += 1
                assert got == dict(expect), (
                    "in the {} render, the emitted {} map disagrees with the "
                    "declared palette — a hand-copied colour vocabulary: {}".format(
                        label, name, got
                    )
                )
        assert seen >= 2, "vacuous — {} emitted no detail colour maps".format(label)


def test_a3_css_status_tokens_mirror_status_fill(tmp_path):
    """A3, the token half: the DAG status legend paints via `var(--done)` etc.,
    while the nodes paint the STATUS_FILL constants directly — so a drift
    between the CSS token block and the Python dict mislabels the legend the
    same way the hardcoded tier legend did. Holds the four status tokens equal
    to STATUS_FILL in `:root` and asserts the dark block does NOT override them
    (they are theme-invariant by design)."""
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    for status, fill in gt.STATUS_FILL.items():
        assert _css_var(css, "--" + status) == fill, (status, fill)
    dark = css.split("prefers-color-scheme: dark", 1)[1].split("}", 1)[0]
    for status in gt.STATUS_FILL:
        assert "--" + status + ":" not in dark, (
            "--{} is overridden in dark — the status vocabulary is declared "
            "theme-invariant".format(status)
        )


def _brace_body(text, open_index):
    """The text between a `{` at open_index and its matching `}`."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : i]
    return text[open_index + 1 :]


def _wiring_bodies(script, sel):
    """The for-loop bodies that iterate the elements `querySelectorAll(sel)`
    yields — both emitted shapes: the immediate `for(const x of …qSA('sel')){}`
    loop, and `const NAME = […qSA('sel')…]` followed by `for(const x of NAME)`
    loops elsewhere in the same script."""
    bodies = []
    for m in re.finditer(r"querySelectorAll\('" + re.escape(sel) + r"'\)", script):
        head = script[max(0, m.start() - 100) : m.start()]
        if re.search(r"for\s*\(\s*const\s+\w+\s+of\s+[\w.\[\]? ]*$", head):
            bodies.append(_brace_body(script, script.index("{", m.end())))
            continue
        assign = re.search(r"const\s+(\w+)\s*=[^;{]*$", head)
        if assign:
            for lm in re.finditer(
                r"for\s*\(\s*const\s+\w+\s+of\s+" + assign.group(1) + r"\s*\)\s*\{",
                script,
            ):
                bodies.append(_brace_body(script, lm.end() - 1))
    return bodies


def test_a1_every_wired_control_pairs_click_with_focus_or_keydown(tmp_path):
    """A1's OPERABLE half, statically (adversarial-review finding F5): the
    ruling's A1 core is "natively focusable or tabindex + a KEY HANDLER", and
    the first binding quietly dropped the key-handler half claiming it needed a
    browser. It does not: the same static read that derives the selectors can
    assert that every control-selector wiring loop that attaches a mouse
    activation (`click`/`dblclick`) also attaches a keyboard-reachable path
    (`focus`, whose handler does the same work in these emitters, or
    `keydown`). Runtime behaviour equivalence is still not driven — that
    narrowing stands — but mouse-only wiring can no longer ship silently.
    Runtime-created controls (the breadcrumb buttons) are native <button>s,
    where a click listener IS keyboard-operable, and stay out of scope."""
    paired = 0
    for label, page in _every_emitter_document(tmp_path):
        for script in re.findall(r"<script\b[^>]*>(.*?)</script>", page, re.S):
            for sel, role in A1_WIRED_SELECTORS.items():
                if role != "control":
                    continue
                bodies = "".join(_wiring_bodies(script, sel))
                if not bodies:
                    continue
                if "addEventListener('click'" in bodies or (
                    "addEventListener('dblclick'" in bodies
                ):
                    paired += 1
                    assert (
                        "addEventListener('focus'" in bodies
                        or "addEventListener('keydown'" in bodies
                    ), (
                        "in the {} render, {} wires a mouse activation with no "
                        "keyboard path beside it: {}".format(label, sel, bodies[:200])
                    )
    assert paired >= 4, (
        "vacuous — only {} control wiring loops with a mouse activation were "
        "found across the sweep".format(paired)
    )


# Every hex-bearing UPPERCASE constant in the emitter, with the role that says
# WHICH floor applies to it. `fill-vocabulary` members are backgrounds (label ink
# 4.5:1, focus ring 3:1); a `control-ink` member is the foreground painted on
# those fills, so it is floor-checked in the other direction by the ring/arrow
# tests and closed here against `_ring_ink`'s reachable outputs (WI-317). A new
# constant fails the sweep until it is classified.
A4_HEX_CONSTANT_ROLES = {
    "STATUS_FILL": "fill-vocabulary",
    "TIER_FILL": "fill-vocabulary",
    "OKF_TYPE_FILL": "fill-vocabulary",
    "SW_NODE_FILL": "fill-vocabulary",
    "PHASE_ACCENTS": "fill-vocabulary",
    "RING_INKS": "control-ink",
}


def test_a4_the_vocabulary_sweep_is_closed_and_every_member_clears_the_floors():
    """dashboard-accessibility.md A4 closure (WI-313). The sibling A4 tests own
    the arithmetic; what none of them owned is the SET — each sweeps a
    hand-copied list of the palette constants, so a sixth vocabulary could ship
    outside every floor check. Reflection closes it: every UPPERCASE
    module-level collection holding hex members must be one of the five
    declared vocabularies (a new one fails here until it joins
    `_palette_vocabularies` and the A4/U5 sweeps), and every member of the
    REFLECTED set must clear both floors — 4.5:1 for its label ink and 3:1 for
    its computed focus ring — so a new vocabulary enters the arithmetic by
    existing, not by being remembered.
    """
    gt = load_script("gen_trajectory")

    def _flatten(value):
        """Every string reachable inside a constant — nested dicts/tuples/
        lists/sets and bare strings included, because the adversarial review
        defeated the flat-dict-only draft with a per-theme dict-of-dicts (the
        WI-293 shape), a tuple-of-tuples, a set, and a bare string constant."""
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for v in value.values():
                yield from _flatten(v)
        elif isinstance(value, (tuple, list, set, frozenset)):
            for v in value:
                yield from _flatten(v)

    found = {}
    for name in dir(gt):
        if not name.isupper():
            continue
        strings = list(_flatten(getattr(gt, name)))
        # ANY hex form counts as hex-bearing (3/4/6/8 digits) — a shorthand or
        # alpha member must not escape the closure by being oddly spelled.
        hexes = [s for s in strings if re.fullmatch(r"#[0-9a-fA-F]{3,8}", s)]
        if hexes:
            found[name] = hexes
    assert set(found) == set(A4_HEX_CONSTANT_ROLES), (
        "the hex-bearing constant set changed — a new constant must declare its "
        "ROLE in A4_HEX_CONSTANT_ROLES (and a new colour vocabulary must also "
        "join _palette_vocabularies and the A4/U5 sweeps) before it ships: "
        "{}".format(sorted(found))
    )
    # Every member must be CANONICAL 6-digit lowercase — the contrast
    # arithmetic below is only defined for that form, so a shorthand or
    # alpha-carrying member fails here rather than shipping unmeasured.
    for name, hexes in found.items():
        bad = [h for h in hexes if not re.fullmatch(r"#[0-9a-f]{6}", h)]
        assert not bad, (name, "non-canonical hex member(s)", bad)
    # Label ink is white everywhere except the one declared exception: `queued`
    # is the light-gray fill that carries dark slate ink (see
    # test_a4_node_fills_meet_the_wcag_floor, which states the same rule).
    dark_ink_fills = {gt.STATUS_FILL["queued"]}
    fills = []
    for name, hexes in sorted(found.items()):
        if A4_HEX_CONSTANT_ROLES[name] != "fill-vocabulary":
            continue
        fills.extend(hexes)
        for fill in hexes:
            ink = "#0f172a" if fill in dark_ink_fills else "#ffffff"
            assert _wcag(ink, fill) >= 4.5, (name, fill, ink, _wcag(ink, fill))
            ring = gt._ring_ink(fill)
            assert _wcag(ring, fill) >= 3, (name, fill, ring, _wcag(ring, fill))
    # A `control-ink` constant is measured the other way round — it is painted ON
    # the fills, so its floors are the ring/arrow ones the sibling tests own; what
    # closes HERE is that the set is exactly what `_ring_ink` can choose (WI-317
    # emits one containment-arrow marker per ink, so an unreachable member is dead
    # markup and a reachable non-member would ship an arrow head with no marker).
    for name in [n for n, r in A4_HEX_CONSTANT_ROLES.items() if r == "control-ink"]:
        assert set(found[name]) == {gt._ring_ink(f) for f in fills}, (
            name,
            sorted(found[name]),
            sorted({gt._ring_ink(f) for f in fills}),
        )


# A4, the theme-token half (adversarial-review finding F4): LLR-114 claims the
# floors cover "emitted theme tokens", but the only token test hand-maintained
# a set of one ({"--hub"}) — the exact hand-copied-list defect the LLR says it
# closed. Same cure as A1's selectors: DERIVE the set from the emitted CSS and
# force a classification, so a new `fill:var(--x)` fails until a human states
# its role — and the roles that carry white text get the both-themes floor.
A4_FILL_TOKEN_ROLES = {
    # WI-389: the Process tab's emphasized node is the merge slot (--hub renamed
    # --slot with the station-cycle redraw); same white-text-fill role and floor.
    "--slot": "white-text-fill",  # the merge-slot rect, white label on it
    "--accent": "ink",  # barrier-glyph TEXT colour, not a fill behind text
    "--muted": "ink",  # sub-label / edge text colour
    "--text": "ink",  # body text colour used as SVG fill
    "--surface": "container-fill",  # component boxes; dark --text sits on it
    # WI-317: the containment-arrow head is FILLED with the per-node control ink.
    # Not a background — its floor is 3:1 against the host node fill, owned by
    # test_t5_containment_arrow_clears_the_3to1_floor_against_every_host_fill.
    "--ring": "control-ink",
}


def test_a4_every_css_fill_token_is_classified_and_floor_checked(tmp_path):
    """Every theme token the emitted CSS uses as a `fill:` must be classified
    in A4_FILL_TOKEN_ROLES; `white-text-fill` roles clear 4.5:1 under white in
    BOTH themes (the WI-293 lesson — a per-theme token passed light and shipped
    2.98:1 in dark), and `container-fill` roles keep the page's own `--text`
    readable on them in both themes."""
    with_gate(tmp_path, "G2")  # the Process tab renders --slot, the widest set
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    used = set(re.findall(r"fill:\s*var\((--[\w-]+)", css))
    assert used, "vacuous — no fill:var() token found"
    unclassified = used - set(A4_FILL_TOKEN_ROLES)
    assert not unclassified, (
        "fill token(s) with no declared role — classify before shipping: {}".format(
            sorted(unclassified)
        )
    )
    for token, role in A4_FILL_TOKEN_ROLES.items():
        if role == "white-text-fill":
            for dark in (False, True):
                value = _css_var(css, token, dark=dark)
                assert _wcag("#ffffff", value) >= 4.5, (token, dark, value)
        elif role == "container-fill":
            for dark in (False, True):
                surface = _css_var(css, token, dark=dark)
                text = _css_var(css, "--text", dark=dark)
                assert _wcag(text, surface) >= 4.5, (token, dark, surface, text)


def test_u3_knowledge_edge_stroke_uses_the_shared_muted_token(tmp_path):
    # dashboard-uniformity U3 (048 MINOR): the knowledge-graph directed edge shares
    # the drill `.wire` stroke idiom (the `--muted` token), not a hardcoded hex
    # that diverged from `.wire` in light mode.
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    # WI-310: the width is now the shared `--w-line` connector token rather than
    # a bare 1.5 — same claim (one idiom), one more literal retired.
    assert (
        "#knowgraph .kedge{fill:none;stroke:var(--muted);stroke-width:var(--w-line);}"
        in css
    )
    assert "#knowgraph .kedge{fill:none;stroke:#94a3b8" not in css
