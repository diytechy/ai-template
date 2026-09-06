"""The shared test API for the gen_trajectory family (WI-277).

`tests/test_gen_trajectory.py` was a 5,359-line monolith. WI-277 split it along
the WI-280 production seams into `test_traj_{parse,graph,views,panels,render,
render_sweeps,status}.py` plus the facade module — and the split surfaced one
thing that genuinely belongs to no single module: the fixture builders.

`_every_emitter_document` alone composes `make_repo`, `with_bundle`,
`_flat_bundle`, `tiered_repo` + `TIER_UNION_WIS`, `containerize`,
`_how_sw_flat`, `with_stage`, `gen` and `html_of` — builders whose natural homes
land in four different split modules — and it is called from both
`test_traj_render_sweeps` and `test_traj_graph`. A test module importing another
test module would put collection order in the dependency graph, so the shared
surface lives here instead: no `test_` prefix, therefore never collected, and
imported the way `conftest` is.

What lives here is exactly what MORE THAN ONE split module uses (measured, not
guessed). Anything used by a single module moved with that module.

Never let this file accrete: a helper that only one module calls belongs in that
module, and a helper this file grows for a second caller must be justified the
same way.
"""

import re

from conftest import ROOT, SCRIPTS, run_py
from trajectory_cli import run_trajectory


from traj_core_fixtures import (  # noqa: F401
    FRAME,
    GOOD_WIS,
    LLRS,
    SN_MD,
    SRS,
    TCS,
    WI_HEADER,
    make_repo,
    write_frame,
    write_stage,
    write_wis,
)


def gen(root, *args):
    return run_trajectory(root, *args)


def html_of(root):
    return (root / "PROJECT_STATE.html").read_text(encoding="utf-8")


# The How-SW source fixture (WI-455): a REAL `src/m.py` the AST scan
# inventories as module `src/m` with public symbols add/sub — the replacement
# for the retired committed-MODULE-MAP markdown fixture (`sw_modules` and
# `arch_inventory` read the source tree now, not docs/architecture.md).
ARCH_SRC = '''"""Demo module."""


def add(a, b):
    """Adds."""
    return a + b


def sub(a, b):
    """Subtracts."""
    return a - b
'''


def write_arch_src(root):
    """Write the `src/m` demo module the default `[paths] src` profile scans."""
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "src" / "m.py").write_text(ARCH_SRC, encoding="utf-8")


def if_row(iid, owner, consumers, channel="call", **cells):
    """One `[interface.IF-###]` TOML table (the carrier since WI-443).

    A helper rather than a header constant: under TOML there IS no header, an
    absent key IS the empty cell, and building rows by hand in six fixtures is
    how a schema change quietly diverges between them. Since OI-67 the row is
    one `owner` — the providing thing, read verbatim, in the same spelling
    `consumers` uses (a list; a bare string is taken as one endpoint) — plus a
    `channel` from the closed vocabulary; `provider`, `req_refs`, `signal` and
    `sr_refs` left the row entirely, and `status` is its one maturity cell.
    """
    if isinstance(consumers, str):
        consumers = [consumers]
    lines = [
        "[interface.{}]".format(iid),
        'owner = "{}"'.format(owner),
        "consumers = [{}]".format(", ".join('"%s"' % c for c in consumers)),
        'channel = "{}"'.format(channel),
        'version = "v1"',
        'status = "{}"'.format(cells.pop("status", "Approved")),
    ]
    lines += ['{} = "{}"'.format(k, v) for k, v in sorted(cells.items())]
    return "\n".join(lines) + "\n\n"


def cmp_row(cid, name, state="built", **cells):
    """One `[component.CMP-###]` TOML table (the carrier since WI-443)."""
    lines = [
        "[component.{}]".format(cid),
        'name = "{}"'.format(name),
        'category = "{}"'.format(cells.pop("category", "software")),
        'state = "{}"'.format(state),
    ]
    lines += ['{} = "{}"'.format(k, v) for k, v in sorted(cells.items())]
    return "\n".join(lines) + "\n\n"


def gen_okf(root):
    return run_py([SCRIPTS / "gen_okf.py", "--root", root], cwd=root)


def with_bundle(root):
    """make_repo + the OKF bundle the Knowledge tab consumes (gen_okf over the
    same registries), so the dashboard has a real docs/okf/ to render."""
    make_repo(root)
    assert gen_okf(root).returncode == 0
    assert (root / "docs" / "okf" / "system-requirements" / "SR-001.md").exists()
    return root


def _flat_bundle(root):
    """make_repo + a hand-written <= 3-type OKF bundle (SN + SR only), so the
    Knowledge graph stays below the `>3` type threshold and renders flat."""
    make_repo(root)
    okf = root / "docs" / "okf"
    for tier, cid, ctype in (
        ("stakeholder-needs", "SN-001", "Stakeholder Need"),
        ("system-requirements", "SR-001", "System Requirement"),
        ("system-requirements", "SR-002", "System Requirement"),
    ):
        d = okf / tier
        d.mkdir(parents=True, exist_ok=True)
        (d / (cid + ".md")).write_text(
            '---\ntype: "{}"\ntitle: "{} title"\ndescription: "desc {}"\n'
            "---\n# {}\n".format(ctype, cid, cid, cid),
            encoding="utf-8",
        )
    return root


# The four-module containment source tree (WI-455): real `scripts/mod_*.py`
# files plus a declared `[paths] src = scripts` profile, inventoried as
# `scripts/mod_a`..`mod_d` — the replacement for the retired CONT_ARCH
# markdown fixture.
CONT_MODULES = (
    ("mod_a", "Module A.", "run", "x"),
    ("mod_b", "Module B.", "go", ""),
    ("mod_c", "Module C.", "gen", ""),
    ("mod_d", "Module D.", "emit", ""),
)


def write_cont_src(root):
    """Write the 4-module `scripts/` tree + the stack.ini profile that scans it."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    for name, summary, fn, args in CONT_MODULES:
        (root / "scripts" / (name + ".py")).write_text(
            '"""{}"""\n\n\ndef {}({}):\n    """{}"""\n    return None\n'.format(
                summary, fn, args, summary
            ),
            encoding="utf-8",
        )
    ini = root / "docs" / "stack.ini"
    ini.parent.mkdir(parents=True, exist_ok=True)
    ini.write_text("[paths]\nsrc = scripts\n", encoding="utf-8")


CONT_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component
LLR-001,SR-001,A,scripts/mod_a,run,d,(see TC),Approved,CMP-001
LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Approved,CMP-001
LLR-003,SR-002,C,scripts/mod_c,gen,d,(see TC),Approved,CMP-002
LLR-004,SR-002,D,scripts/mod_d,emit,d,(see TC),Approved,CMP-002
"""

CONT_CMPS = cmp_row("CMP-001", "Core") + cmp_row("CMP-002", "Gen")

# Two seams a->c and b->c both cross CMP-001 -> CMP-002 (must aggregate to ONE
# deduplicated edge); IF-003 is intra-CMP-001, IF-004 a boundary to a file hub.
CONT_IFS = (
    if_row("IF-001", "scripts/mod_a", "scripts/mod_c")
    + if_row("IF-002", "scripts/mod_b", "scripts/mod_c")
    + if_row("IF-003", "scripts/mod_a", "scripts/mod_b")
    + if_row("IF-004", "docs/stack.ini", "scripts/mod_a", "file")
)


def containerize(root):
    """make_repo + a 4-module source tree (real files, WI-455), two software
    components tagging them via LLR Component tags, and the cross/intra/
    boundary seams."""
    make_repo(root)
    req = root / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(CONT_LLRS, encoding="utf-8")
    (req / "components.toml").write_text(CONT_CMPS, encoding="utf-8")
    (req / "interfaces.toml").write_text(CONT_IFS, encoding="utf-8")
    write_cont_src(root)
    return root


# --- a small registry fixture (<= 3 phases AND <= 3 workstreams) --------------
# Below both tiering thresholds `when_view` returns None, so the flat SVG DAG
# renders (the phase->workstream->work-item tiering is earned by scale).
SMALL_WIS = (
    "WI-001,Root,scripts,SR-001,,done,the adder\n"
    "WI-002,Mid,scripts,SR-001,WI-001,active,harness\n"
    "WI-003,Sub,scripts,SR-002,WI-001,queued,the subber\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped\n"
)

# Four SR phases (v1..v4 — the CLI is label-agnostic, so a downstream vN still
# tiers), so a WI's phase is derived from the SR it delivers.
TIER_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase\n"
    'SR-001,P1,SN-001,"r",R,"a",,M,Test,Approved,v1\n'
    'SR-002,P2,SN-001,"r",R,"a",,M,Test,Approved,v2\n'
    'SR-003,P3,SN-001,"r",R,"a",,M,Test,Approved,v3\n'
    'SR-004,P4,SN-001,"r",R,"a",,M,Test,Approved,v4\n'
)

TIER_HDR = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"

# Two v1 WIs both feed the single v2 WI -> the v1->v2 parent edge is the deduped
# union of two child edges. Phases: v1={001,002}, v2={003}, v3={004}, v4={005}.
TIER_UNION_WIS = (
    "WI-001,A,scripts,SR-001,,done,d,\n"
    "WI-002,B,docs,SR-001,,done,d,\n"
    "WI-003,C,unattended,SR-002,WI-001;WI-002,queued,d,\n"
    "WI-004,D,self-adoption,SR-003,WI-003,queued,d,\n"
    "WI-005,E,scripts,SR-004,WI-003,queued,d,\n"
)


def _layer_with(view, marker):
    """The SVG of the first drill `.layer` whose blocks carry `marker` (a drill
    layer div holds only its SVG — no nested divs — so the split is clean)."""
    for _lid, svg in re.findall(
        r'<div class="layer" data-layer="(when-\d+)"[^>]*>(.*?)</div>', view, re.S
    ):
        if marker in svg:
            return svg
    raise AssertionError("no layer contains " + marker)


def tiered_repo(root, wis_body, header=TIER_HDR, srs=TIER_SRS):
    """make_repo + a phase-carrying SR registry (the WI phase is derived from the
    SRs a work item delivers)."""
    make_repo(root, wis_body, header=header)
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        srs, encoding="utf-8"
    )
    return root


def with_stage(root, stage="DevStg-Tests", wis_body=GOOD_WIS, header=WI_HEADER):
    """make_repo + a derived-format `docs/stage` — the Process tab's render
    condition (it was `docs/gate` until WI-498 slice 5 retired the bar axis)."""
    make_repo(root, wis_body, header=header)
    return write_stage(root, stage)


# The pre-slice-5 name. `test_traj_render.py` and `test_traj_render_sweeps.py`
# still import it and are out of scope for this change; re-point them when they
# are next touched, then delete this line.
with_gate = with_stage


def _wcag(fg, bg):
    def lum(h):
        h = h.lstrip("#")
        chan = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
        f = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chan]
        return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]

    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def _css_var(css, name, dark=False):
    """The value of custom property `name` as declared for the light (`:root`) or
    dark (`prefers-color-scheme: dark`) theme in the emitted stylesheet. Dark
    falls back to the light declaration, which is what the cascade does when the
    dark block does not override the token."""
    if dark:
        block = css.split("prefers-color-scheme: dark", 1)[1].split("}", 1)[0]
        hit = re.search(re.escape(name) + r":\s*(#[0-9a-fA-F]{3,8})", block)
        if hit:
            return hit.group(1)
    root = css.split(":root", 1)[1]
    return re.search(re.escape(name) + r":\s*(#[0-9a-fA-F]{3,8})", root).group(1)


def _style_surfaces(html):
    """Only where a font-size actually PAINTS: `<style>` blocks and inline
    `style=` attributes. The rendered document also *quotes* CSS inside prose
    (a registry Detail cell explaining a past palette fix names
    `font-size:13px`), and a naive whole-document scan reads that as a
    declaration — judging documentation as if it were code."""
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    blocks += re.findall(r'style="([^"]*)"', html)
    return blocks


def _palette_vocabularies(gt):
    """`{name: {key: hex}}` for every declared colour vocabulary."""
    return {
        "status": dict(gt.STATUS_FILL),
        "tier": dict(gt.TIER_FILL),
        "okf": dict(gt.OKF_TYPE_FILL),
        "sw": dict(gt.SW_NODE_FILL),
        "phase": {str(i): h for i, h in enumerate(gt.PHASE_ACCENTS)},
    }


def _how_sw_flat(root):
    """Declared seams but no containerization — the FLAT `sw_graph`.

    `containerize` earns the containment drill instead, so a sweep carrying only
    that fixture never renders `sw_graph`'s own `<style>` block. This is the
    third emitter a whole-document sweep has silently missed (after `knode` and
    the per-layer drill read), which is why `_every_emitter_document` is the one
    place that list lives."""
    make_repo(root)
    write_arch_src(root)
    (root / "docs" / "requirements" / "interfaces.toml").write_text(
        if_row("IF-001", "src/m", "downstream adopter", "cli")
        + if_row("IF-002", "docs/stack.ini", "src/m", "file"),
        encoding="utf-8",
    )
    return root


def _every_emitter_document(tmp_path):
    """`[(label, html), ...]` covering EVERY emitter that really renders.

    The A2 adversarial review's lesson, generalized: a document walk can only
    judge the emitters its fixture happens to render, and it measured the then-
    current fixture at 2 of 6 — the one genuine violation lived in an emitter
    that never rendered, so the test passed while the defect shipped. A
    whole-document uniformity check has exactly that failure mode, so it sweeps
    the union: the artifact this repo ships (the loops diagram, the How-SW
    graph, the tiered drill) plus fixtures for the emitters a meta-repo's own
    dashboard does not exercise. Note BOTH knowledge fixtures — `with_bundle`'s
    four OKF types earn the tiered drill, so only `_flat_bundle` (<= 3 types)
    renders the flat `.knode` concept graph, and a sweep with just the former is
    blind to that emitter.

    TWO TRUTH-TIMES (WI-372). The list is not homogeneous, and a caller has to
    know which one it is asserting over:

    - **`shipped`** is the COMMITTED `PROJECT_STATE.html` — markup an OLDER
      renderer wrote. Generated artifacts belong to the trunk lane
      (concurrency-restructure §5.2; `check.py` skips the freshness gates on a
      work branch), so off trunk this document legitimately lags the code under
      test. Asserting over it is a COMPATIBILITY PIN — "the invariant holds for
      the markup already in a reader's hands" — never "this emitter satisfies
      it". It is simply ABSENT in a checkout with no committed dashboard, so a
      caller that reads it should still be meaningful fresh-only — with one
      MEASURED exception, T6, called out below.
    - **Every other label** is FRESH: built into `tmp_path` and rendered by
      THIS run's `gen_trajectory.py`, so it is a property of the code under
      test.

    The trap that mixture sets is the CALLER's to disarm, and deliberately so
    (the shared fresh-emitting fixture was considered and rejected — owner
    ruling 2026-07-30, log.md Decisions). A change that TIGHTENS an invariant
    reds through the stale shipped copy rather than through the emitter it
    changed: the failure names an older renderer's markup while the code under
    test is clean. So when the assertion is about the CURRENT emitter, filter
    at the call site and supply a fixture for whatever shape the shipped copy
    used to contribute — `test_svg_viewbox_contains_every_routed_wire` is the
    worked example (`if lb != "shipped"`, plus `WRAPAROUND_WIS` for the
    outboard lane it lost).

    Every OTHER call site keeps `shipped` on purpose: the U1-U4 / A1-A3 / T6
    uniformity-and-accessibility sweeps and T8's through-box sweep. Most keep
    it as the pin above — their invariants hold in the older markup TODAY,
    which is an observation about the committed artifact, not a guarantee it
    carries forward.

    **T6 is the exception, and it is the one that will bite.**
    `test_t6_theme_lock_has_one_mechanism_and_no_mixed_family_pair` does not
    merely PIN the shipped document, it is LOAD-BEARING on it: its non-vacuity
    floor `nodes >= 50` reaches only 33 node pairs over the seven fresh
    fixtures (measured 2026-07-30 by running the test itself against a
    dashboard-less `ROOT`), so filtering `shipped` out there reds the test on a
    floor that has nothing to do with the emitter anyone changed. Its
    replacement fixture comes FIRST and the filter second — the same order the
    worked example above uses; the difference is that it already HAD a fixture
    to hand and T6 does not, so here the fixture is the work.

    **When a keeper reds, read the failing LABEL first:** `shipped` means
    regenerate the dashboard on trunk (or exclude it, above); any other label
    means the emitter really regressed. That triage reads the PER-DOCUMENT
    assertions, which all format `label` into their message. T6 is the
    exception here too: its closing assertions run AFTER the sweep loop, over a
    `text_fills` dict accumulated ACROSS documents and keyed by CSS SELECTOR,
    so a shipped-vs-fresh disagreement surfaces there as
    `('#dag .wi text', {'invariant', 'varying'})` — the selector, never the
    label (measured the same day, by lagging that one rule in a copy of the
    committed dashboard).

    The same pin is made without this helper by
    `test_a2_the_repos_own_shipped_dashboard_holds_the_invariant`, which reads
    the committed file directly and skips when it is absent.
    """
    docs = []
    shipped = ROOT / "PROJECT_STATE.html"
    if shipped.is_file():
        docs.append(("shipped", shipped.read_text(encoding="utf-8")))
    for label, build in (
        ("flat-dag", lambda p: make_repo(p)),
        ("knowledge-tiered", lambda p: with_bundle(p)),
        ("knowledge-flat", lambda p: _flat_bundle(p)),
        ("tiered-drill", lambda p: tiered_repo(p, TIER_UNION_WIS)),
        ("how-sw-drill", lambda p: containerize(p)),
        ("how-sw-flat", _how_sw_flat),
        ("process", lambda p: with_stage(p, "DevStg-Tests")),
    ):
        root = tmp_path / label
        root.mkdir(parents=True, exist_ok=True)
        build(root)
        assert gen(root).returncode == 0, label
        docs.append((label, html_of(root)))
    return docs
