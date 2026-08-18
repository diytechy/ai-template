"""The shared test API for the gen_trajectory family (WI-277).

`tests/test_gen_trajectory.py` was a 5,359-line monolith. WI-277 split it along
the WI-280 production seams into `test_traj_{parse,graph,views,panels,render,
render_sweeps,status}.py` plus the facade module — and the split surfaced one
thing that genuinely belongs to no single module: the fixture builders.

`_every_emitter_document` alone composes `make_repo`, `with_bundle`,
`_flat_bundle`, `tiered_repo` + `TIER_UNION_WIS`, `containerize`,
`_how_sw_flat`, `with_gate`, `gen` and `html_of` — builders whose natural homes
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

import csv
import re
from pathlib import Path

from conftest import ROOT, SCRIPTS, load_script, run_py


WI_HEADER = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"

# A small but branching spine, so the icicle exercises multi-child subtrees and
# the taller-cell label path; SR-001 Approved + SR-002 Drafted -> 50% definition.
SN_MD = """# Stakeholder Needs (SN-###)

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Do the thing well. | Users need it. | M | works end to end. |
"""

SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Core add,SN-001,"Shall add.",R,"add works",,M,Test,Approved
SR-002,Core sub,SN-001,"Shall subtract.",R,"sub works",,M,Test,Drafted
"""

LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Adder,src/m,add,"a+b",(see TC),Approved
LLR-002,SR-001,Adder edge,src/m,add,"overflow guard",(see TC),Approved
LLR-003,SR-002,Subber,src/m,sub,"a-b",(see TC),Approved
"""

TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,call add,Smoke,"a=1",ok,Yes,Approved
TC-002,LLR-001,Unit,call add,Smoke,"a=2",ok,Yes,Approved
TC-003,LLR-002,Unit,call add,Full,"a=3",ok,Yes,Approved
TC-004,SR-002;LLR-003,Unit,call sub,Full,"a=4",ok,No,Drafted
"""

# A diamond DAG: WI-001 -> {WI-002, WI-003} -> WI-004; WI-003 also carries a
# soft (advisory, ~-prefixed) edge after WI-002 — dashed in the render, never
# a rank constraint.
GOOD_WIS = (
    "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
    "WI-002,Harness,scripts,SR-001,WI-001,active,harness green\n"
    "WI-003,Subtraction,scripts,SR-002,WI-001;~WI-002,queued,the subber\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped\n"
)

# The BlockRef a `blocked` fixture row gets when its header declares no column
# for one: since Phase 5 the impediment pointer is what MAKES a row blocked, so
# it cannot be left empty the way the CSV era could.
BLOCKREF = "docs/gate/attest-SR-001.md"


def write_wis(root, wis_body=GOOD_WIS, header=WI_HEADER):
    """Write the fixture work items into the registry's one home — `docs/work/`
    spec files, status = directory (the CSV home retired at
    concurrency-restructure Phase 5, RULING-4).

    The CSV-shaped `wis_body`/`header` inputs stay: they are the compact,
    readable way to state a registry in a test, and the ROW ORDER they declare is
    reproduced through the `order` frontmatter key the folder reader sorts on.
    Two statuses need translating, because the folder form encodes them
    differently rather than as a word in a cell:

      * `blocked` has no directory — a blocked item is a `queued/` spec carrying
        a `blockref`, which is what schedule.py derives the "blocked" disposition
        and gen_trajectory's pending block from;
      * `active` is `active/<branch>/`, one level deeper, so the spec is written
        and then MOVED exactly as `integrate.py claim` files a claim.

    Re-writing an id replaces its spec (fixtures re-seed freely); the file for a
    previous status is removed first so status = directory stays single-homed.
    """
    wc = load_script("wi_convert")
    cols = next(csv.reader([header.strip("\n")]))
    work = root / "docs" / "work"
    work.mkdir(parents=True, exist_ok=True)
    for order, cells in enumerate(csv.reader(wis_body.splitlines()), 1):
        if not cells:
            continue
        row = dict.fromkeys(wc.COLUMNS, "")
        row.update({c: (v or "") for c, v in zip(cols, cells) if c in row})
        status = row["Status"] or "queued"
        if status == "blocked":
            row["Status"] = "queued"
            row["BlockRef"] = row["BlockRef"] or BLOCKREF
        elif status == "active":
            row["Status"] = "queued"  # relocated to active/<branch>/ below
        wid = row["WI-ID"]
        for old in list(work.glob("*/{}-*.md".format(wid))) + list(
            work.glob("active/*/{}-*.md".format(wid))
        ):
            old.unlink()
        relpath = wc.write_spec_file(work, row, order=order)
        if status == "active":
            claim = work / "active" / wid.lower() / Path(relpath).name
            claim.parent.mkdir(parents=True, exist_ok=True)
            (work / relpath).replace(claim)


def make_repo(root, wis_body=GOOD_WIS, readme=True, header=WI_HEADER):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(TCS, encoding="utf-8")
    write_wis(root, wis_body, header)
    if readme:
        (root / "README.md").write_text(
            '# demoproj\n\n<a id="vision"></a>\n'
            "**PROJECT-VISION:** Stay correct over time.\n\n## What\n",
            encoding="utf-8",
        )
    return root


def gen(root, *args):
    return run_py([SCRIPTS / "gen_trajectory.py", "--root", root, *args], cwd=root)


def html_of(root):
    return (root / "PROJECT_STATE.html").read_text(encoding="utf-8")


ARCH_MD = """# Architecture

<!-- BEGIN GENERATED MODULE MAP -->
### `src/m`
_Demo module._

| Public item | Summary | Implements |
|---|---|---|
| `add(a, b)` | Adds. |  |
| `sub(a, b)` | Subtracts. |  |
<!-- END GENERATED MODULE MAP -->
"""


def if_row(iid, direction, this, counterpart, contract="call", **cells):
    """One `[interface.IF-###]` TOML table (the carrier since WI-443).

    A helper rather than a header constant: under TOML there IS no header, an
    absent key IS the empty cell, and building rows by hand in six fixtures is
    how a schema change quietly diverges between them."""
    lines = [
        "[interface.{}]".format(iid),
        'direction = "{}"'.format(direction),
        'this_project = "{}"'.format(this),
        'counterpart = "{}"'.format(counterpart),
        'contract = "{}"'.format(contract),
        'signal = "{}"'.format(cells.pop("signal", "discrete")),
        'sr_refs = ["{}"]'.format(cells.pop("sr_refs", "SR-001")),
        'version = "v1"',
        'approval = "{}"'.format(cells.pop("approval", "approved")),
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


CONT_ARCH = """# Architecture
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_Module A._

| Public item | Summary | Implements |
|---|---|---|
| `run(x)` | Runs. |  |

### `scripts/mod_b`
_Module B._

| Public item | Summary | Implements |
|---|---|---|
| `go()` | Go. |  |

### `scripts/mod_c`
_Module C._

| Public item | Summary | Implements |
|---|---|---|
| `gen()` | Gen. |  |

### `scripts/mod_d`
_Module D._

| Public item | Summary | Implements |
|---|---|---|
| `emit()` | Emit. |  |
<!-- END GENERATED MODULE MAP -->
"""

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
    if_row("IF-001", "Provides", "scripts/mod_a", "scripts/mod_c")
    + if_row("IF-002", "Provides", "scripts/mod_b", "scripts/mod_c")
    + if_row("IF-003", "Provides", "scripts/mod_a", "scripts/mod_b")
    + if_row("IF-004", "Consumes", "scripts/mod_a", "docs/stack.ini", "reads")
)


def containerize(root):
    """make_repo + a 4-module arch-map, two software components tagging them via
    LLR Component tags, and the cross/intra/boundary seams."""
    make_repo(root)
    req = root / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(CONT_LLRS, encoding="utf-8")
    (req / "components.toml").write_text(CONT_CMPS, encoding="utf-8")
    (req / "interfaces.toml").write_text(CONT_IFS, encoding="utf-8")
    (root / "docs" / "architecture.md").write_text(CONT_ARCH, encoding="utf-8")
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


def with_gate(root, gate="DevStg-Tests", wis_body=GOOD_WIS, header=WI_HEADER):
    """make_repo + a derived-format docs/gate (comment header, then the runnable
    gate value) — the Process tab's render condition."""
    make_repo(root, wis_body, header=header)
    (root / "docs" / "gate").write_text(
        "# DERIVED GATE - generated by scripts/derive_gate.py\n"
        "# basis: SN=1 SR=2 LLR=3 TC=4 drafted=0 computed={g} per-phase=(none)\n"
        "{g}\n".format(g=gate),
        encoding="utf-8",
    )
    return root


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
    (root / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (root / "docs" / "requirements" / "interfaces.toml").write_text(
        if_row("IF-001", "Provides", "src/m", "downstream adopter", "cli")
        + if_row("IF-002", "Consumes", "src/m", "docs/stack.ini", "reads"),
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
        ("process", lambda p: with_gate(p, "DevStg-Tests")),
    ):
        root = tmp_path / label
        root.mkdir(parents=True, exist_ok=True)
        build(root)
        assert gen(root).returncode == 0, label
        docs.append((label, html_of(root)))
    return docs
