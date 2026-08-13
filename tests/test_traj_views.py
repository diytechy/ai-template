"""gen_trajectory.py — the What / When / How-SW views (WI-277: split verbatim
from tests/test_gen_trajectory.py along the WI-280 production seams; this
module's subject is `traj_views.py`).

One view family per section: the How-SW panel (module map, interface seams,
containerization by component and its nesting), the When roadmap's
phase→workstream→work-item tiering (WI-272 status carry, the drill/breadcrumb
descent, the collapse thresholds), and the What icicle's own scale-earned
collapse plus the T7/T4 fit contracts — scale-to-fit with a legibility floor,
and no label ink outside the block it belongs to.
"""

import html
import re

from conftest import ROOT, load_script
from traj_fixtures import (
    ARCH_MD,
    CONT_ARCH,
    CONT_CMPS,
    CONT_LLRS,
    IF_HDR,
    LLRS,
    SMALL_WIS,
    TIER_HDR,
    TIER_UNION_WIS,
    _layer_with,
    containerize,
    gen,
    html_of,
    make_repo,
    tiered_repo,
)


def test_how_sw_view_renders_from_the_module_map(tmp_path):
    # WI-039: with a committed symbol-mode module map, PROJECT_STATE gains the
    # How (SW architecture) view — a view of the code-map view; without one
    # (files-mode / absent) the tab is simply omitted.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert "How (SW architecture)" not in html_of(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="sw"' in text and "How (SW architecture)" in text
    assert "src/m" in text and "add" in text


def test_cycle_refuses_to_render(tmp_path):
    make_repo(
        tmp_path,
        "WI-001,A,scripts,,WI-002,queued,d\nWI-002,B,scripts,,WI-001,queued,d\n",
    )
    proc = gen(tmp_path)
    assert proc.returncode == 1 and "cycle" in proc.stderr
    assert not (tmp_path / "PROJECT_STATE.html").exists()


# --- WI-056: the How-SW panel becomes a real interface graph --------------------


def test_how_sw_graph_renders_seams(tmp_path):
    # With a committed module map AND declared seams, the How-SW panel gains the
    # interface graph (module + file + external nodes, IF-labeled edges); the
    # render is byte-deterministic so --check stays stable.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (tmp_path / "docs" / "requirements" / "interfaces.csv").write_text(
        IF_HDR
        + 'IF-001,Provides,src/m,downstream adopter,"cli",SR-001,v1,Stable,Active,,\n'
        + 'IF-002,Consumes,src/m,docs/stack.ini,"reads",SR-001,v1,Stable,Active,,\n',
        encoding="utf-8",
    )
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "How (SW architecture)" in text
    assert "IF-001" in text and "swarrow" in text  # a labeled edge + the marker
    assert "downstream adopter" in text and "stack.ini" in text  # ext + file nodes
    first = text
    assert gen(tmp_path).returncode == 0
    assert html_of(tmp_path) == first  # deterministic


def test_how_sw_stays_a_table_without_seams(tmp_path):
    # No IF rows -> the panel keeps the bare module table (graph earned by seams);
    # no graph marker leaks into the render.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "How (SW architecture)" in text
    assert "swarrow" not in text


# --- WI-073/FB5: the containerized How-SW top view -----------------------------


def sw_section(root):
    return html_of(root).split('id="sw"', 1)[1].split("</section>", 1)[0]


def _sw_layer_with(sw, marker):
    """The SVG of the first How-SW drill `.layer` whose blocks carry `marker`."""
    for _lid, svg in re.findall(
        r'<div class="layer" data-layer="(sw-\d+)"[^>]*>(.*?)</div>', sw, re.S
    ):
        if marker in svg:
            return svg
    raise AssertionError("no sw layer contains " + marker)


def test_how_sw_containerizes_when_components_contain_modules(tmp_path):
    # With a CMP layer that contains modules, the How-SW panel becomes the
    # containerized Simulink-style drill top view (≤10 items), not the flat table.
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert 'class="cmptree"' in sw and 'class="drill"' in sw
    root = _sw_layer_with(sw, 'data-tier="component"')
    assert root.count('data-tier="component"') == 2  # two top-level components
    assert root.count('data-tier="component" data-descend=') == 2  # each descends
    assert "Top view: 2 item" in sw
    # descending CMP-001 reveals its modules + its intra + boundary seams.
    inside = _sw_layer_with(sw, "scripts/mod_a")
    assert "scripts/mod_a" in inside
    assert "IF-003" in inside  # intra-component seam (mod_a -> mod_b)
    assert "IF-004" in inside and "stack.ini" in inside  # boundary seam to a file hub


def test_boundary_aggregation_dedupes_cross_component_edges(tmp_path):
    # IF-001 and IF-002 both cross CMP-001 -> CMP-002; at the top level they
    # aggregate to ONE deduplicated component-to-component wire naming both ids.
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    root = _sw_layer_with(sw_section(tmp_path), 'data-tier="component"')
    titles = re.findall(r'<path class="wire"[^>]*><title>(.*?)</title>', root)
    assert len(titles) == 1  # one aggregated cross-component wire
    assert "IF-001, IF-002" in titles


def test_no_cmp_renders_flat_view_byte_identical(tmp_path):
    # The vacuity guarantee: render flat (no CMP layer), add the containment
    # (panel changes), remove it, re-render == the original flat bytes exactly.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(CONT_ARCH, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    flat = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'class="cmptree"' not in flat

    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(CONT_LLRS, encoding="utf-8")
    (req / "components.csv").write_text(CONT_CMPS, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    assert b'class="cmptree"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (req / "components.csv").unlink()
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == flat


def test_containerized_view_is_deterministic_and_check_stable(tmp_path):
    # Built from sorted inputs, no clocks -> a second render is byte-identical and
    # --check passes (no new freshness exclusion).
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0


def test_nested_components_render_inside_their_parent(tmp_path):
    # A CMP with PartOf renders as a nested component block inside its parent's
    # descend layer, and only the top-level root is a first-view item.
    containerize(tmp_path)
    req = tmp_path / "docs" / "requirements"
    (req / "components.csv").write_text(
        CONT_CMPS + "CMP-003,Sub,software,,built,,CMP-001,,\n", encoding="utf-8"
    )
    (req / "low-level-requirements.csv").write_text(
        CONT_LLRS.replace(
            "LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-001",
            "LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-003",
        ),
        encoding="utf-8",
    )
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    # Still two top-level items (CMP-001 with CMP-003 nested inside, and CMP-002).
    assert "Top view: 2 item" in sw
    assert "CMP-003" in sw  # the nested child is rendered (inside CMP-001)


def test_meta_component_top_view_smoke():
    # Over the real meta repo: 5 right-sized software components, 0 uncontained,
    # within the bound, and sw_containment renders the containerized panel.
    ct = load_script("check_trajectory")
    v = ct.component_top_view(ROOT)
    assert v["count"] <= ct.TOP_VIEW_MAX
    assert v["uncontained"] == []
    assert len(v["top_roots"]) == 5
    gt = load_script("gen_trajectory")
    cont = gt.sw_containment(ROOT, gt.sw_modules(ROOT))
    assert cont is not None
    tab, panel = cont
    assert 'data-tab="sw"' in tab and 'class="cmptree"' in panel


# --- WI-087 / SR-051 (rev WI-141): the tiered, Simulink-style drill-down views --
# The When roadmap tiers into phase -> workstream -> work-item block
# LAYERS once a tier holds > 3 members:
# each layer is an SVG diagram of blocks with input/output ports, the aggregated
# cross-tier edges wired between ports (the deduped union of child edges), a
# container block double-clicked (or Enter/Space) to DESCEND one layer and a
# breadcrumb to return (superseding the old <details> expand). A registry below the
# thresholds renders byte-identically to the flat SVG DAG.


# --- WI-272 (review M-2): the registry statuses, four swatches, no rewriting ----
# The `blocked` row below is stated in the CSV-shaped fixture vocabulary and
# `write_wis` files it the way the folder registry encodes it since Phase 5: a
# `queued/` spec carrying a `blockref`. So five statuses reach the render, and
# `blocked` is a DISPOSITION derived from the pointer rather than a word in a
# cell — see the two tests below for what that costs the dashboard.

SIX_STATUS_WIS = (
    "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
    "WI-002,Harness,scripts,SR-001,WI-001,active,\n"
    "WI-003,Release,docs,SR-002,WI-002,queued,\n"
    "WI-004,Someday,docs,SR-002,WI-002,deferred,parked on purpose\n"
    "WI-005,Waiting,docs,SR-002,WI-002,blocked,needs an upstream decision\n"
    "WI-006,Dropped,docs,SR-002,WI-002,cancelled,won't build\n"
    "WI-007,Sketch,docs,SR-002,WI-002,draft,\n"
)


def test_wi272_deferred_and_blocked_are_never_rewritten_as_queued(tmp_path):
    """review M-2: the dashboard used to clamp every unknown status to `queued`
    — and not just for the swatch. The clamp ran BEFORE the tooltip, the
    accessible name, and the detail JSON were built, so a `deferred` row's own
    detail said `"status": "queued"`. Parked-by-choice and impeded-by-something
    are not ordinary queue work, and this is the repo's advertised state surface,
    so that mislabelling mis-prioritizes real work.

    Sharing a swatch is fine and stays (minting two more hues would worsen the
    live U5 near-duplicate residue); rewriting the STATUS is the defect.
    """
    make_repo(tmp_path, SIX_STATUS_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)

    # All six statuses — `blocked` included: since Phase 5 it is DERIVED
    # (`queued/` + a `blockref` key, no directory of its own), and the
    # dashboard's `_wi_status` derives it so the render keeps the distinction
    # this test exists to protect.
    for status in (
        "done",
        "active",
        "queued",
        "draft",
        "deferred",
        "blocked",
        "cancelled",
    ):
        assert 'data-status="{}"'.format(status) in page, (
            "no node carries data-status={} — the DOM lost the true status".format(
                status
            )
        )
        assert '"status": "{}"'.format(status) in page, (
            "the detail JSON never reports {} — it is being rewritten".format(status)
        )
    # the hover title names the row's own status, not its bucket
    assert "WI-004 — Someday (deferred)" in page
    assert "WI-005 — Waiting (blocked)" in page
    # ...and `deferred` shares `queued`'s swatch, deliberately and visibly: the
    # legend names the grouping rather than leaving the shared colour to imply
    # it is queued, and it still spells out the impeded state in words + glyph.
    gt = load_script("gen_trajectory")
    assert gt.STATUS_BUCKET["deferred"] == gt.STATUS_BUCKET["blocked"] == "queued"
    assert "not started" in page
    for glyph in (gt.STATUS_GLYPH["deferred"], gt.STATUS_GLYPH["blocked"]):
        assert glyph in page, "the legend must show the glyph that tells them apart"


def test_wi272_status_is_carried_through_the_tiered_drill_too(tmp_path):
    # The flat DAG and the tiered drill are separate emitters; M-2 named both.
    # The drill's leaf label is glyph-prefixed per STATUS, so `deferred`,
    # `blocked` (derived from queued+blockref since Phase 5), `draft` and
    # `cancelled`
    # differ from `queued` there without any colour at all.
    tiered_repo(tmp_path, TIER_UNION_WIS + SIX_STATUS_WIS.replace("WI-00", "WI-01"))
    assert gen(tmp_path).returncode == 0
    gt = load_script("gen_trajectory")
    # Every WORK-ITEM block across every layer. Two narrowings, both learned by
    # getting them wrong: `_layer_with` returns one layer, so it saw only the
    # first phase/workstream group (done + active — the glyph assertion would
    # have passed vacuously); and `.blab` is the label class of EVERY drill
    # block, so a bare class scan also pulls in phase/workstream containers and
    # the whole How-SW drill, none of which have a status to prefix.
    labels = re.findall(
        r'data-tier="work-item"[^>]*data-label="([^"]*)"', html_of(tmp_path)
    )
    assert labels, "no work-item blocks rendered"
    glyphs = set(gt.STATUS_GLYPH.values())
    assert all(lab[0] in glyphs for lab in labels), labels
    # the parked/terminal minority glyphs actually reached the drill, so this is
    # not vacuous (both would be ○ if the emitter clamped to the bucket)
    assert any(lab[0] == gt.STATUS_GLYPH["deferred"] for lab in labels), labels
    assert any(lab[0] == gt.STATUS_GLYPH["blocked"] for lab in labels), labels
    assert any(lab[0] == gt.STATUS_GLYPH["cancelled"] for lab in labels), labels
    assert any(lab[0] == gt.STATUS_GLYPH["draft"] for lab in labels), labels


def test_when_view_tiers_by_phase_above_threshold(tmp_path):
    # > 3 phases -> the When view starts at a layer of 4 phase blocks, each a
    # descend container carrying the per-phase color accent; the count is surfaced.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert "Tiered roadmap: 4 phase(s), 4 workstream(s)" in view
    assert view.count('data-tier="phase"') == 4  # one block per phase
    # each phase block is a descend container (double-click / Enter to drill in)
    assert view.count('data-tier="phase" data-descend=') == 4
    # the per-phase colour accent legend renders through the shared component
    # (WI-294b: no longer a bespoke `span.ph` chip idiom)
    assert '<div class="legend"><span><i style="background:' in view


def test_when_view_parent_edge_is_deduped_union_of_child_edges(tmp_path):
    # The two v1->v2 child edges (WI-001->WI-003 and WI-002->WI-003) aggregate to
    # ONE parent block wire equal to their deduped union, carried as the wire title.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    phase_layer = _layer_with(html_of(tmp_path), 'data-tier="phase"')
    wire_titles = re.findall(
        r'<path class="wire"[^>]*><title>(.*?)</title>', phase_layer
    )
    # crossing phase pairs v1->v2, v2->v3, v2->v4 -> three aggregated wires
    assert len(wire_titles) == 3
    assert "WI-001→WI-003, WI-002→WI-003" in wire_titles  # deduped union, one wire


def test_when_view_nests_workstream_tier_inside_a_phase(tmp_path):
    # Within a phase that holds > 3 workstreams the workstream tier fires, nesting
    # phase -> workstream -> work item as descend layers; below the threshold flat.
    body = (
        "WI-001,A1,scripts,SR-001,,done,d,\n"
        "WI-002,A2,docs,SR-001,,done,d,\n"
        "WI-003,A3,unattended,SR-001,,done,d,\n"
        "WI-004,A4,self-adoption,SR-001,,done,d,\n"  # v1 spans 4 workstreams
        "WI-005,B1,scripts,SR-002,WI-001,active,d,\n"  # v2, one workstream -> flat
        "WI-006,C1,scripts,SR-003,WI-005,queued,d,\n"
        "WI-007,D1,scripts,SR-004,WI-006,queued,d,\n"
    )
    tiered_repo(tmp_path, body)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert view.count('data-tier="phase"') == 4  # 4 phase blocks at the root layer
    # only v1 (4 workstreams) explodes into a workstream layer -> 4 workstream blocks
    assert view.count('data-tier="workstream"') == 4
    assert "Scripts / harness" in view  # workstream label on a sub-block


def test_when_view_workstream_tier_when_phases_flat(tmp_path):
    # <= 3 phases but > 3 workstreams -> the workstream tier fires at the TOP
    # (the "or at the top when phases <= 3" rule); phases stay flat.
    body = (
        "WI-001,A,scripts,,,done,d,\n"
        "WI-002,B,docs,,WI-001,active,d,\n"
        "WI-003,C,unattended,,WI-001,queued,d,\n"
        "WI-004,D,self-adoption,,WI-002;WI-003,queued,d,\n"
        "WI-005,E,deliverable,,WI-004,queued,d,\n"  # five workstreams, all unphased
    )
    make_repo(tmp_path, body, header=TIER_HDR)  # default SRs (no Phase) -> unphased
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert "Tiered roadmap: 1 phase(s), 5 workstream(s)" in view
    assert view.count('data-tier="workstream"') == 5  # one block per workstream
    assert 'data-tier="phase"' not in view  # phases stay flat


def test_when_view_below_thresholds_returns_none_flat_dag(tmp_path):
    # <= 3 phases and <= 3 workstreams -> when_view returns None, so the caller keeps
    # the flat SVG DAG (the tiering is earned by scale). The rendered dashboard shows
    # the flat DAG with no drill layers.
    make_repo(tmp_path, SMALL_WIS)  # 2 workstreams, unphased -> 1 phase
    gt = load_script("gen_trajectory")
    ct = load_script("check_trajectory")
    wis, _ = ct.load_wis(ct.read_rows(tmp_path / ct.WI_CSV))
    assert gt.when_view(tmp_path, wis) is None
    assert gen(tmp_path).returncode == 0
    assert 'class="drill"' not in html_of(tmp_path)  # flat DAG, no tiered drill


def test_wi296_interaction_copy_matches_the_emitter_that_actually_ran(tmp_path):
    """WI-296: the When explainer must describe the emitter that RAN, not a promise
    only one of them keeps.

    Neighbourhood highlighting belongs to the FLAT emitter — the controller walks
    `.wi`/`.edge` nodes only `dag_svg` produces. The sentence used to claim it
    unconditionally, so above the `>3` rule (where the tiered drill view renders and
    those node sets are empty) the dashboard promised an interaction it did not have.

    Note what this does NOT do: the flat `.wi` path is live and is the default for a
    small/newly-scaffolded repo, so its copy — and its emitter — stay exactly as they
    were. 117-CRITIQUE read the empty `.wi` set in the meta-repo's own render as dead
    code; deleting it would have broken the When tab for every downstream adopter.
    """
    # small registry -> flat DAG -> the neighbourhood promise is TRUE and kept
    make_repo(tmp_path, SMALL_WIS)  # 2 workstreams, unphased -> 1 phase
    assert gen(tmp_path).returncode == 0
    flat = html_of(tmp_path)
    assert 'class="drill"' not in flat
    assert 'class="wi ' in flat  # the flat emitter really is the live one here
    assert "highlight its neighbourhood" in flat
    assert "Double-click</strong> a container" not in flat

    # a registry above the >3 rule -> tiered drill -> the copy describes descending
    tiered = tmp_path / "tiered"
    tiered.mkdir()
    tiered_repo(tiered, TIER_UNION_WIS)
    assert gen(tiered).returncode == 0
    drill = html_of(tiered)
    assert 'class="drill"' in drill
    assert "Double-click</strong> a container" in drill
    assert "the breadcrumb returns to any ancestor" in drill
    # the promise the tiered render cannot keep is gone
    assert "highlight its neighbourhood" not in drill


def test_when_view_is_deterministic_and_check_stable(tmp_path):
    # Sorted inputs, no clocks -> a re-render is byte-identical and --check passes.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0


# --- SR-051 rev (WI-141): the three interface-wired / descend-a-layer contracts --


def test_when_view_seams_wire_to_block_ports(tmp_path):
    # Each block carries an input port (left-middle) and an output port
    # (right-middle); each aggregated edge is a wire whose endpoints ATTACH to those
    # ports (Simulink-style), not free-floating text.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    root = _layer_with(html_of(tmp_path), 'data-tier="phase"')  # the phase layer
    out_ports = {
        round(float(cx), 1)
        for cx in re.findall(
            r'<circle class="port out(?: wire-port)?" cx="([\d.]+)"', root
        )
    }
    in_ports = {
        round(float(cx), 1)
        for cx in re.findall(
            r'<circle class="port in(?: wire-port)?" cx="([\d.]+)"', root
        )
    }
    assert out_ports and in_ports  # both port kinds render
    wire_ds = re.findall(r'<path class="wire" d="([^"]+)"', root)
    assert wire_ds  # at least one wire
    wires = []
    for d in wire_ds:
        nums = [float(v) for v in re.findall(r"-?[\d.]+", d)]
        wires.append((nums[0], nums[-2]))
    # The start attaches on the OUT port; the arrow-bearing END lands PORT_R + 2
    # px short of the IN-port center so its arrowhead clears the port ring
    # (WI-249 render fix) — still "at" the port, just outside its circle.
    gt = load_script("gen_trajectory")
    end_gap = gt.PORT_R + 2
    in_ends = {round(cx - end_gap, 1) for cx in in_ports}
    for x1, x2 in wires:  # every wire leaves an OUT port and enters an IN port
        assert round(float(x1), 1) in out_ports
        assert round(float(x2), 1) in in_ends


def test_when_view_double_click_descends_a_layer(tmp_path):
    # A container block descends one layer on double-click (keyboard alt: Enter /
    # Space on the focused block); its data-descend names a real child layer.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    m = re.search(r'data-tier="phase" data-descend="(when-\d+)"', view)
    assert m and 'data-layer="{}"'.format(m.group(1)) in view  # target layer exists
    # focusable + labelled + a keyboard alternative to the pointer
    assert 'tabindex="0" role="button"' in view
    assert "addEventListener('dblclick'" in view
    assert "addEventListener('keydown'" in view and "e.key==='Enter'" in view


def test_when_view_breadcrumb_restores_parent(tmp_path):
    # The drill carries a breadcrumb whose crumb click truncates the trail back to
    # that ancestor (restoring the parent view); the root crumb is declared.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert '<nav class="crumbs"' in view and 'data-root-crumb="Roadmap"' in view
    assert "trail=trail.slice(0,i+1)" in view  # crumb click restores the ancestor


# --- SR-056 (WI-143): the decomposition render-polish contracts ------------------


def test_decomposition_one_arrow_per_containment_edge(tmp_path):
    # Each descend container (a containment edge) renders EXACTLY one horizontal
    # parent->child arrow (class="cedge"), making containment explicit rather than
    # implied by the descend interaction alone.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    phase_layer = _layer_with(html_of(tmp_path), 'data-tier="phase"')
    containers = phase_layer.count("data-descend=")  # 4 phase containers
    assert containers == 4
    assert phase_layer.count('class="cedge"') == containers  # one arrow each, no more


def test_tier_column_honors_declared_width_bound(tmp_path):
    # The tier column is a declared value (MAX_TIER_COL), not an adjective: every
    # block honours it, and a content-light layer renders NARROWER than the bound
    # (right-sized, not the former uniform column).
    gt = load_script("gen_trajectory")
    assert isinstance(gt.MAX_TIER_COL, int) and gt.MAX_TIER_COL > 0
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    widths = [
        int(w)
        for w in re.findall(
            r'<rect x="[\d.]+" y="[\d.]+" width="(\d+)" height="\d+" rx="8"',
            html_of(tmp_path),
        )
    ]
    assert widths  # blocks render
    assert all(w <= gt.MAX_TIER_COL for w in widths)  # never exceeds the bound
    assert any(w < gt.MAX_TIER_COL for w in widths)  # right-sized where content allows


def test_persistent_hover_highlight_keyed_to_last_node(tmp_path):
    # The persistent-highlight contract: every block is keyed by a data-node id; the
    # controller records the last-hovered/focused node (data-hl) and never clears on
    # exit (no mouseleave/mouseout in the drill controller) -> no flash-on-exit.
    gt = load_script("gen_trajectory")
    assert "addEventListener('mouseover'" in gt.DRILL_SCRIPT
    assert "setAttribute('data-hl'" in gt.DRILL_SCRIPT  # keyed to the last node
    assert "mouseleave" not in gt.DRILL_SCRIPT and "mouseout" not in gt.DRILL_SCRIPT
    assert ".block.hl" in gt.DRILL_STYLE  # the persistent highlight style
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert re.search(r'class="block[^"]*"[^>]*data-node="', view)  # blocks are keyed


def test_drill_overviews_trace_one_nodes_incoming_and_outgoing_edges(tmp_path):
    # WI-434: an overview no longer asks the reader to decode every aggregated
    # wire with equal emphasis. Each wire names its source and destination; the
    # shared controller selects a node, dims unrelated cards, and separately
    # emphasizes prerequisites flowing in and dependents flowing out. Text and
    # arrow glyphs carry the two meanings in addition to colour.
    gt = load_script("gen_trajectory")
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    phase_layer = _layer_with(html_of(tmp_path), 'data-tier="phase"')
    wires = re.findall(
        r'<path class="wire"[^>]*data-from="([^"]+)" data-to="([^"]+)"',
        phase_layer,
    )
    assert wires and all(source != target for source, target in wires)
    assert "selectDefault()" in gt.DRILL_SCRIPT
    assert "classList.add('trace-in')" in gt.DRILL_SCRIPT
    assert "classList.add('trace-out')" in gt.DRILL_SCRIPT
    assert "trace-muted" in gt.DRILL_SCRIPT
    assert "← Needs:" in gt.DRILL_SCRIPT and "Unlocks →" in gt.DRILL_SCRIPT
    page = html_of(tmp_path)
    assert "→ selected: prerequisites" in page
    assert "selected → dependents" in page
    assert 'aria-live="polite"' in page
    assert page.count('data-focused-trace="true"') == 1  # this fixture earns When
    assert 'data-focused-trace="true"' in gt._render_drill(
        "sw", "root", "Architecture", [("root", "<svg></svg>")]
    )
    assert 'data-focused-trace="true"' not in gt._render_drill(
        "archdrill", "root", "What", [("root", "<svg></svg>")]
    )
    assert 'data-drill="archdrill" data-focused-trace' not in page


def test_when_and_how_drills_use_bounded_orthogonal_wires_and_explicit_ports():
    """WI-435: selected paths must remain attributable in the rendered geometry.

    Curves produced acute cusps at lane changes, and several edges sharing one
    centre port merged before reaching the node. Drill wires are rectilinear;
    shared interfaces expose one connector circle per edge; and the focused
    direction markers are large enough to remain visible beside those circles.
    """
    gt = load_script("gen_trajectory")
    _tab, sw = gt.sw_containment(ROOT, gt.sw_modules(ROOT))
    ct = load_script("check_trajectory")
    wis, integrity = ct.load_wis(ct.read_registry_rows(ROOT / ct.WI_CSV))
    assert not integrity
    when = gt.when_view(ROOT, wis)
    assert when is not None

    for panel in (sw, when):
        wires = re.findall(r'<path class="wire" d="([^"]+)"', panel)
        assert wires
        assert all(set(re.findall(r"[A-Za-z]", d)) <= {"M", "L"} for d in wires)

    target_ports = re.findall(
        r'<circle class="port in wire-port" cx="[^"]+" cy="([^"]+)" '
        r'data-from="[^"]+" data-to="cmp:CMP-004"',
        sw,
    )
    assert len(target_ports) == 3
    assert len(set(target_ports)) == 3
    assert "stroke-linejoin:round" in gt.DRILL_STYLE

    marker_sizes = {
        marker: float(size)
        for marker, size in re.findall(
            r'<marker id="([^"]+-drillarrow-(?:in|out))"[^>]*markerWidth="([^"]+)"',
            sw,
        )
    }
    assert marker_sizes
    assert set(marker_sizes.values()) == {12.0}
    marker_ids = re.findall(r'<marker id="([^"]+)"', sw)
    assert len(marker_ids) == len(set(marker_ids))
    assert "marker-end:var(--arrow-in)" in gt.DRILL_STYLE
    assert "marker-end:var(--arrow-out)" in gt.DRILL_STYLE


def test_leaf_wi_block_surfaces_delivery_phase(tmp_path):
    # OI-10 fix: the leaf work-item block's hover title carries the delivery Phase,
    # so it stays visible when the phase tier is flat but a workstream tier drills in.
    body = (
        "WI-001,A1,scripts,SR-001,,done,d,\n"
        "WI-002,A2,docs,SR-001,,done,d,\n"
        "WI-003,A3,unattended,SR-001,,done,d,\n"
        "WI-004,A4,self-adoption,SR-001,,done,d,\n"  # v1 spans 4 workstreams -> tiers
    )
    tiered_repo(tmp_path, body)  # all v1 (SR-001 Phase=v1), <=3 phases so phase flat
    assert gen(tmp_path).returncode == 0
    # the leaf work-item block's hover title carries the delivery phase (· v1)
    assert re.search(r"<title>WI-001 — [^<]*\(done\) · v1</title>", html_of(tmp_path))


# Four one-module components -> the How-SW top view exceeds the > 3 threshold.
FOUR_CMP_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component
LLR-001,SR-001,A,scripts/mod_a,run,d,(see TC),Verified,CMP-001
LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-002
LLR-003,SR-002,C,scripts/mod_c,gen,d,(see TC),Verified,CMP-003
LLR-004,SR-002,D,scripts/mod_d,emit,d,(see TC),Verified,CMP-004
"""

FOUR_CMPS = (
    "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
    "CMP-001,Core,software,,built,,,,\n"
    "CMP-002,Two,software,,built,,,,\n"
    "CMP-003,Three,software,,built,,,,\n"
    "CMP-004,Four,software,,built,,,,\n"
)


def test_how_sw_collapses_above_component_threshold(tmp_path):
    # > 3 top-level components -> the root layer holds four component blocks, each a
    # descend container (double-click / Enter to explode into its modules).
    containerize(tmp_path)
    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(FOUR_CMP_LLRS, encoding="utf-8")
    (req / "components.csv").write_text(FOUR_CMPS, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert "Top view: 4 item" in sw
    root = _sw_layer_with(sw, 'data-tier="component"')
    assert root.count('data-tier="component" data-descend=') == 4  # four descend blocks


def test_meta_tiered_when_view_smoke():
    # Over the real meta repo (4 workstreams > 3): the When view tiers into a
    # workstream block layer with work-item blocks at the bottom tier, rendered as a
    # wired drill diagram.
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_registry_rows(ROOT / ct.WI_CSV))
    assert not integrity
    view = gt.when_view(ROOT, wis)
    assert view is not None
    assert 'class="drill"' in view and 'data-tier="workstream"' in view
    assert 'data-tier="work-item"' in view  # work items are the bottom tier
    assert 'class="port in"' in view and 'class="wire"' in view  # interface-wired


def test_u3_sw_drill_has_a_legend_and_a_wired_detail_aside(tmp_path):
    # dashboard-uniformity.md U3: the How-SW drill gets the same legend + detail
    # aside its sibling When drill has (fills were explained nowhere; no aside).
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert 'class="legend"' in sw and 'id="sw-detail"' in sw
    assert "module" in sw and "external actor" in sw  # node-kind legend entries
    assert ".block[data-node]" in sw  # the detail wiring targets the sw blocks


# --- WI-306 / SR-054 T2: the What icicle earns its tiering by scale -----------
# 119-CRITIQUE MAJOR: the landing What view rendered the WHOLE spine at leaf
# scale (one unit per TC), opening as a multi-screen wall while the three wired
# tabs correctly opened at a summary layer. Capping DEPTH would not have fixed
# it - height is leaf-proportional, so stopping at the SR lane still stacks one
# unit per SR - so the summary has to be a coarser TIER: one block per SN,
# descend on click, earned above the SR-089 `>3` rule like its sibling views.

_T2_SN_HEADER = (
    "# Stakeholder Needs (SN-###)\n\n"
    "| SN-ID | Need | Why it matters | Priority | Acceptance intent |\n"
    "|---|---|---|---|---|\n"
)


def _spine_with_sns(root, n):
    """Rewrite the fixture spine to span `n` SNs, each with one SR/LLR/TC - the
    scale knob the `>3` rule turns on."""
    req = root / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(
        _T2_SN_HEADER
        + "".join(
            "| SN-{i:03d} | Need {i}. | Matters {i}. | M | works {i}. |\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        + "".join(
            'SR-{i:03d},Req {i},SN-{i:03d},"Shall {i}.",R,"ac {i}",,M,Test,'
            "Verified\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
        + "".join(
            'LLR-{i:03d},SR-{i:03d},Low {i},src/m.py,f{i},"d {i}",(see TC),'
            "Verified\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
        "Evidence,Status\n"
        + "".join(
            'TC-{i:03d},SR-{i:03d};LLR-{i:03d},Unit,m {i},Smoke,"p","e {i}",Yes,'
            "tests/t.py::t{i},Verified\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )


def test_t2_what_icicle_starts_collapsed_above_the_sn_threshold(tmp_path):
    # Above the `>3` rule the What view is a start-collapsed drill: one descend
    # block per SN in the root layer, one child layer each, and the deep TC cells
    # sit in HIDDEN child layers - not in the initially-shown root, which is the
    # wall the anchor forbids.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-drill="archdrill"' in text
    assert text.count('data-descend="archl-sn-') == 8
    assert text.count('data-layer="archl-sn-') == 8
    root_layer = text.split('data-layer="arch-root"', 1)[1].split("</div>", 1)[0]
    assert "SN-001" in root_layer
    assert "TC-001" not in root_layer  # no leaf cells in the opening view


def test_t2_small_spine_keeps_the_flat_icicle(tmp_path):
    # At or below 3 SNs the tiering is NOT earned: the flat icicle renders, so a
    # small project never pays for a drill it cannot need - the same symmetry the
    # When and Knowledge views hold to.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 3)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-drill="archdrill"' not in text
    assert "TC-001" in text  # deep cells render inline, unhidden


# --- WI-307 / SR-054 T7 + T4: every diagram scales to fit, with a floor -------
# 119-CRITIQUE T7 and the WI-305 train critique (T7 + T4): every emitted SVG
# carried a FIXED pixel width, so at 390px all four views demanded "Scroll
# sideways to see the full view" and cut off right-side lanes, and the How graph
# clipped `CMP-002 - Generators` mid-label. A viewBox alone cannot fix that - the
# fixed width pins the rendered size. These guards hold the responsive sizing on
# EVERY emitter (the defect was per-wrapper, so a per-view test would miss a
# fourth emitter added later) and pin the legibility floor that keeps the fix
# from trading T7 for T4.

_FIT_RE = re.compile(
    r'style="width:100%;max-width:(\d+)px;min-width:(\d+)px;height:auto"'
)


def test_t7_every_emitted_svg_scales_to_fit(tmp_path):
    # Derived from the emitted document, not a hand list: EVERY <svg> must carry
    # the responsive style, and none may keep a bare fixed width. A new emitter
    # that forgets it fails here.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    svgs = re.findall(r"<svg\b[^>]*>", text)
    assert svgs, "vacuous - no svg emitted"
    missing = [t[:90] for t in svgs if "width:100%" not in t]
    assert not missing, "svg(s) without responsive sizing: {}".format(missing)
    # A fixed width with no fit style is the exact pre-fix shape.
    assert not re.findall(r'<svg viewBox="[^"]*" width="\d+"(?! style=)', text)


def test_t7_shrink_floor_keeps_labels_legible(tmp_path):
    # The floor is the T4 half: pure scale-to-fit would squeeze a wide graph into
    # 390px and shrink a 12px label past readable, so min-width pins how far the
    # diagram may shrink. Assert the emitted ratio matches the declared constant
    # rather than re-hardcoding it (one home for the number).
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    pairs = _FIT_RE.findall(html_of(tmp_path))
    assert pairs, "vacuous - no responsive svg found"
    for natural, floor in pairs:
        expected = int(float(natural) * gt.SHRINK_FLOOR)
        assert abs(int(floor) - expected) <= 1, (natural, floor, expected)
    assert 0 < gt.SHRINK_FLOOR < 1


# --- WI-318 / SR-054 T4: no label ink outside the block it belongs to ---------
# 121-CRITIQUE MAJOR: the What/Architecture root layer drew each SN's whole need
# as the block's sub-label, unwrapped — one centred line that began outside the
# left edge of its box and ran past the right one, at 390px AND at 1680px, so the
# text was unreadable AS a label and broke the box too. `_tier_col_width` cannot
# absorb it: it clamps at MAX_TIER_COL, so a 400-character need asks for a 2000px
# column and gets 172.
#
# The binding is the T4 anchor's mechanizable floor, stated geometrically and
# swept over the EMITTED document: every `<tspan>` a drill block renders must fit
# inside that block's own rect, horizontally and vertically. Deliberately not a
# per-view assertion — the defect lives in the one shared label emitter that feeds
# four views, so a fifth view added later is covered without touching this test.
_BLOCK_RE = re.compile(r'<g class="block\b.*?</g>', re.S)

_BRECT_RE = re.compile(
    r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"'
)

_BTEXT_RE = re.compile(r'<text x="[-\d.]+" y="([-\d.]+)"[^>]*>(.*?)</text>', re.S)

_BSPAN_RE = re.compile(
    r'<tspan x="([-\d.]+)" dy="([-\d.]+)" class="(blab|bsub)">([^<]*)</tspan>'
)

# Conservative vertical glyph extents as a fraction of the declared font size:
# enough of an over-estimate that a real render cannot exceed them.
_ASCENT, _DESCENT = 0.8, 0.25


def _label_boxes(html_text):
    """Every drill-block label line as (block, class, text, ink-rect, block-rect),
    measured from the emitted markup with the emitter's own declared per-character
    widths and the font sizes the emitted CSS declares."""
    gt = load_script("gen_trajectory")
    size = {
        cls: float(re.search(r"--{}:([\d.]+)px".format(var), html_text).group(1))
        for cls, var in (("blab", "nlabel"), ("bsub", "nsub"))
    }
    per_char = {"blab": gt._BLAB_CH, "bsub": gt._BSUB_CH}
    out = []
    for block in _BLOCK_RE.findall(html_text):
        rect = _BRECT_RE.search(block)
        text = _BTEXT_RE.search(block)
        if not rect or not text:
            continue
        rx, ry, rw, rh = (float(v) for v in rect.groups())
        baseline = float(text.group(1))
        node = re.search(r'data-node="([^"]*)"', block)
        for x, dy, cls, raw in _BSPAN_RE.findall(text.group(2)):
            baseline += float(dy)
            # Entities are ONE glyph: measuring `&#x27;` as six characters would
            # invent overflow on every apostrophe.
            width = len(html.unescape(raw)) * per_char[cls]
            cx = float(x)
            out.append(
                (
                    node.group(1) if node else "?",
                    cls,
                    raw,
                    (
                        cx - width / 2,
                        baseline - size[cls] * _ASCENT,
                        cx + width / 2,
                        baseline + size[cls] * _DESCENT,
                    ),
                    (rx, ry, rx + rw, ry + rh),
                )
            )
    return out


_LONG_NEED = (  # the real SN-001, the row the critic read at 390px and 1680px
    "A team can drop the kit into a new or existing repo and get a working "
    "gated, requirement-traced process without hand-building the tooling."
)


def _spine_with_a_long_need(root, n=8):
    """The tiered spine fixture with ONE realistic sentence-length need, so the
    sweep below is exercised against the shape that actually overflowed."""
    _spine_with_sns(root, n)
    sn = root / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(
        sn.read_text(encoding="utf-8").replace("| Need 1. |", "| " + _LONG_NEED + " |"),
        encoding="utf-8",
    )


def test_t4_no_block_label_renders_outside_its_own_box(tmp_path):
    make_repo(tmp_path)
    _spine_with_a_long_need(tmp_path)
    assert gen(tmp_path).returncode == 0
    boxes = _label_boxes(html_of(tmp_path))
    assert boxes, "vacuous - no drill block labels emitted"
    # Non-vacuity with teeth: the sentence-length need must actually be in there,
    # or this sweep proves nothing about the defect it was written for.
    assert any(_LONG_NEED.split()[0] in raw for _n, _c, raw, _i, _b in boxes)
    outside = [
        (node, cls, raw, ink, box)
        for node, cls, raw, ink, box in boxes
        if ink[0] < box[0] or ink[1] < box[1] or ink[2] > box[2] or ink[3] > box[3]
    ]
    assert not outside, "label ink outside its block: {}".format(outside[:4])


def test_t4_a_sentence_length_sub_label_wraps_and_ellipsizes(tmp_path):
    # The fix path itself: too long for one line -> a second line, then an
    # ellipsis. (The full string keeps its homes on the block: <title>,
    # aria-label, data-summary.)
    make_repo(tmp_path)
    _spine_with_a_long_need(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    block = next(
        b for b in _BLOCK_RE.findall(text) if 'data-node="SN-001"' in b and "…" in b
    )
    subs = re.findall(r'class="bsub">([^<]*)</tspan>', block)
    assert len(subs) == 2, subs
    assert subs[0] and not subs[0].endswith("…")  # broke on a word, not mid-word
    assert subs[1].endswith("…")
    assert _LONG_NEED.startswith(html.unescape(subs[0]))
    assert _LONG_NEED in text  # the whole need still reads, via <title>/summary


def test_t4_a_short_sub_label_keeps_the_two_line_grid(tmp_path):
    # The wrap is earned by length, not applied to everything: a sub that already
    # fits renders on the untouched two-line grid.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    block = next(
        b for b in _BLOCK_RE.findall(html_of(tmp_path)) if 'data-node="SN-002"' in b
    )
    assert 'dy="-2" class="blab"' in block and 'dy="13" class="bsub"' in block
    assert len(re.findall(r'class="bsub"', block)) == 1


def test_fit_lines_breaks_on_words_then_ellipsizes():
    gt = load_script("gen_trajectory")
    assert gt._fit_lines("", 10, 2) == []
    assert gt._fit_lines("short", 10, 2) == ["short"]  # untouched when it fits
    assert gt._fit_lines("one two three", 8, 2) == ["one two", "three"]
    # More text than the budget holds: the last line ends in an ellipsis and no
    # line exceeds the budget.
    got = gt._fit_lines("aa bb cc dd ee ff gg", 8, 2)
    assert got == ["aa bb cc", "dd ee f…"], got
    assert all(len(line) <= 8 for line in got)
    # A single word longer than the budget is cut, never allowed to run past.
    assert gt._fit_lines("supercalifragilistic", 8, 2) == ["supercal", "ifragil…"]
