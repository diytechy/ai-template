#!/usr/bin/env python3
"""The cross-component seam check: an import between components needs a declared interface row.

`cross_component_findings` reports each internal import edge whose endpoints
sit in disjoint components and that no interface row covers;
`cross_component_advisories` reports, warn-only, each edge an endpoint in
several components silences. An edge into a module declared in
`docs/kernel-modules-allow` is neither. The edges come from
`arch_inputs.arch_inventory` and resolve through
`gen_arch_map.resolve_import`; membership is
`kitlib.spine.module_components`. One scan per root per run, held in
`_SCAN_CACHE`. ``trajectory_arch`` re-exports the rule for
``check_trajectory``, and `arch_components` runs it inside
`component_findings`.

Contracts: IF-319 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-319: the seam rule surface ``trajectory_arch`` re-exports and
`arch_components` composes. `cross_component_findings(root)` and
`cross_component_advisories(root)` return finding strings from one cached
scan per root; the advisories are `[]` when `[checks] components_check =
false`, and the findings leave that dial to their caller.
`read_kernel_modules(root)` gives the declared kernel as `{module key:
reason}`, empty when the file is absent, and
`kernel_allow_parse_findings(root)` names the first line its grammar cannot
read. A `gen_arch_map` without `resolve_import` or `package_paths` leaves both
tiers silent. The module performs no writes.
"""

import sys
from pathlib import Path

try:
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import spine as _kitspine

import spine_carrier
from arch_inputs import (
    CMP_CSV,
    IF_CSV,
    LLR_CSV,
    _arch_scan_profile,
    _norm_module,
    arch_inventory,
    load_cmps,
    load_seams,
    read_components_check_enabled,
)

try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None


# The declared shared-kernel surface (OI-48 ruled (d), WI-494) — see
# `read_kernel_modules`. The reuse provision's home: a small declared file,
# consistent with the `docs/*-allow` idiom `provenance-allow` and
# `if-tc-coverage-allow` already established, over a `[checks]`-side list —
# a per-entry recorded REASON is the point, and `docs/process.toml` carries
# dials, not reasoned prose.
KERNEL_ALLOW = "docs/kernel-modules-allow"
KERNEL_ALLOW_SEP = " — "


def _declared_seam_pairs(root):
    """The IF registry's endpoint pairs, normalized and stored BOTH ways — a
    seam is one declared relationship, whichever side authored the row.

    A MULTI-ENDPOINT SIDE IS SEVERAL ENDPOINTS, and every combination is a
    declared pair. `trace.py` has split on `;` since IF-097 (the comment there
    names it); this reader did not, so the two readers of the same cells
    disagreed — 14 of 249 pairs carried an unsplit, non-existent module name as
    an endpoint after WI-469 took the population from one row to seven
    (2026-08-21 review, M-14). Latent, but the failure it sets up is expensive
    in the wrong direction: a real cross-component import whose seam row plainly
    names both modules is reported as having no declared seam, and the cheapest
    fix available to that author is to duplicate or delete a correct row.

    PAIRS ARE TAKEN ACROSS THE ROW'S WHOLE ENDPOINT SET since WI-455, not across
    two named cells. On a row whose consumers are a measured READER SET over one
    medium (`IF-029`, `IF-035`, `IF-037`, `IF-047`, `IF-072`) that is what keeps
    the reader-to-reader pairs the two-cell shape used to produce, now stated as
    what they always were: one declared relationship among all of the seam's
    endpoints."""
    covered = set()
    for r in load_seams(root):
        ends = _norm_endpoints([r["owner"]] + r["far"])
        for a in ends:
            for b in ends:
                if a != b:
                    covered.add((a, b))
                    covered.add((b, a))
    return covered


def _norm_endpoints(endpoints):
    """The normalized module keys of an endpoint list, empties dropped — so a
    blank side contributes no pair, exactly as before. Each entry may itself be
    a `;`-joined cell (`kitlib.spine.seam_endpoints` splits those): an endpoint
    may legitimately contain a space (`external:downstream adopter`) or a
    comma, so `;` stays the only separator."""
    out = []
    for endpoint in endpoints:
        for part in _kitspine.seam_endpoints(endpoint):
            normalized = _norm_module(part)
            if normalized:
                out.append(normalized)
    return out


def _parse_kernel_allow(root):
    """`(entries, unparsed)` for `docs/kernel-modules-allow` — the whole parse,
    both halves, the `docs/provenance-allow` split (`trace.read_provenance_allow`):
    `entries` is `[(normalized module key, reason, lineno)]`; `unparsed` is
    `[(lineno, line)]` for every DECLARING line the grammar dropped, so a
    malformed entry is reported rather than silently read as an empty file
    (`kernel_allow_parse_findings`).

    Grammar: one non-blank, non-`#`-comment line per entry, `<module path> —
    <reason>` (an em dash, space each side — the same separator
    `docs/provenance-allow` uses). A REASON IS REQUIRED, unlike
    `docs/if-tc-coverage-allow`'s migration seed: OI-48's reuse provision is
    a deliberate recorded act every time, never a bare-baseline default, so
    there is no seeded-population exception here. A line with no separator,
    or an empty module or reason on either side of it, DECLARES NOTHING — it
    is dropped (fail-safe: absence of a valid declaration grants no
    exemption) and counted as unparsed."""
    path = Path(root) / KERNEL_ALLOW
    if not path.is_file():
        return [], []
    out, unparsed = [], []
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if KERNEL_ALLOW_SEP not in line:
            unparsed.append((lineno, line))
            continue
        head, reason = line.split(KERNEL_ALLOW_SEP, 1)
        module = _norm_module(head.strip())
        reason = reason.strip()
        if not module or not reason:
            unparsed.append((lineno, line))
            continue
        out.append((module, reason, lineno))
    return out, unparsed


def read_kernel_modules(root):
    """`{normalized module key: reason}` — the declared shared-kernel surface
    (OI-48 ruled (d), 2026-08-21; executed WI-494). Absent file, or a file
    with no parseable entries: empty dict — the FAIL-SAFE DEFAULT the ruling
    requires, since an empty mapping exempts nothing and every edge stays
    policed by the ordinary cross-component rule.

    `_cross_component_scan` treats an import edge whose DESTINATION resolves
    into this set as not a seam at all — neither a finding nor the
    multi-membership advisory — because the module is a declared shared
    kernel: consumed across components BY DESIGN, and re-declaring that fact
    edge-by-edge (the WI-064 seam registry) would restate "everyone imports
    the shared helper" once per caller (OI-48's option (b), priced and
    declined). The exemption is ONE-DIRECTIONAL: an edge OUT of a kernel
    module — a kernel module importing a non-kernel sibling — is not
    exempted here and stays fully policed, because a shared kernel importing
    outward is the one shape a layered system forbids regardless of who
    calls it (WI-448's dedicated bootstrap-manifest test polices the literal
    kitlib case already; this rule polices any OTHER declared kernel the
    same way going forward).

    NEVER A KITLIB HARDCODE — the reuse provision's whole point: any future
    shared module whose real consumers span components takes this same
    declared path, one entry, one recorded reason, a deliberate act rather
    than a default."""
    return {module: reason for module, reason, _ in _parse_kernel_allow(root)[0]}


def kernel_allow_parse_findings(root):
    """PARSE HONESTY for `docs/kernel-modules-allow`, the
    `provenance_allow_parse_findings` idiom: a declaring line the grammar
    cannot read is an explicit finding naming it, not a silent drop — the
    other half of "declares nothing" is that it also grants no exemption,
    and a malformed line that still reads like a live entry to a human is
    the state most worth reporting. Reported at the FIRST unparsed line with
    a count, not all of them, for the same reason `provenance_allow_parse_findings`
    does: the fix is the same edit for every one.

    Shares `component_findings`' WARN-plain / ERROR-under-`--strict`
    promotion and its `[checks] components_check` opt-out — this file is
    part of the components layer, not a spine-integrity surface, so it rides
    that gate rather than the always-on floor `docs/provenance-allow` uses."""
    _entries, unparsed = _parse_kernel_allow(root)
    if not unparsed:
        return []
    lineno, line = unparsed[0]
    return [
        "{}:{}: this line DECLARES a kernel module and the grammar cannot "
        "read it ({} such line(s)) — `{}`. An entry is `<module path>{}"
        "<reason>` and BOTH fields are required — a bare module path or a "
        "missing separator suppresses nothing".format(
            KERNEL_ALLOW, lineno, len(unparsed), line[:80], KERNEL_ALLOW_SEP
        )
    ]


def _classifiable_edges(root):
    """Yield `(src, dst, src_cmps, dst_cmps)` for every internal import edge
    the cross-CMP rules can classify — both endpoints normalized, both carrying
    at least one REAL CMP membership.

    The vacuity guards live here, so every caller inherits them: no internal
    imports, no real CMP rows, an endpoint with no `Component`-tag membership
    (coverage is the containment rule's job, not this one's), an import that
    resolves to no inventory module, to several, or to the importing module
    itself, and a `gen_arch_map` too old to resolve one (IF-131: every entry
    point is optional at the call site, and a missing one silences the rule).

    Each import is the token `gen_arch_map.internal_imports` wrote, bare
    (`agent_route`), dotted (`kitlib.spine`) or relative (`.registry`), and
    `gen_arch_map.resolve_import` is its one resolution, the one the
    dependency diagram draws by. Whether an importer is a package, which a
    relative import starts from, is read from its file through
    `gen_arch_map.package_paths`, not guessed from the modules under it. Looking the whole token up by its last path
    segment, as this rule once did, missed every dotted and relative import,
    so no edge into a package was ever checked.

    Implements: SR-159, LLR-374
    """
    names, _contracts, imports = arch_inventory(root)
    resolve = getattr(gen_arch_map, "resolve_import", None)
    package_paths = getattr(gen_arch_map, "package_paths", None)
    if not imports or resolve is None or package_paths is None:
        return
    cmp_ids = {c["id"] for c in load_cmps(spine_carrier.load(root / CMP_CSV, "CMP-ID"))}
    if not cmp_ids:
        return
    raw = _kitspine.module_components(spine_carrier.load(root / LLR_CSV, "LLR-ID"))
    membership = {n: tags & cmp_ids for n, tags in raw.items()}
    modules = {_norm_module(m) for m in names} - {""}
    src, _mode = _arch_scan_profile(root)
    scan_dir = root / src.strip().replace("\\", "/").rstrip("/")
    packages = {_norm_module(p) for p in package_paths([scan_dir])}
    for src in sorted(imports):
        src_n = _norm_module(src)
        src_cmps = membership.get(src_n, set())
        if not src_cmps:
            continue
        for token in sorted(imports[src]):
            dst_n = resolve(token, src_n, modules, packages)
            dst_cmps = membership.get(dst_n, set())
            if dst_cmps and dst_n != src_n:
                yield src_n, dst_n, src_cmps, dst_cmps


_SCAN_CACHE = {}


def _cross_component_scan(root):
    """`(findings, advisories)` over the classifiable import edges — the two
    tiers of the cross-CMP rule, computed in ONE pass so they can never disagree
    about which edge is which.

    A **finding** (unchanged since WI-064) is an edge whose endpoint component
    sets are DISJOINT and which no declared IF-### row covers.

    An **advisory** (WI-440, OI-14) is an edge the overlap guard SUPPRESSES only
    because an endpoint is tagged into more than one component: the sets
    intersect, no IF row covers the pair, and `len(cmps) > 1` somewhere. That
    edge would be a finding under a partition where each module belongs to one
    component, so the multi-membership is EVIDENCE ABOUT THE PARTITION (the file
    splits, the shared part is its own component, or the boundary is drawn
    wrong) rather than a licence to stay quiet. Reporting it reverses the
    direction of the old rule, where authoring one more `Component` tag
    monotonically silenced the check — a fail-open the author controls.

    An edge whose endpoints are single-tagged into the SAME component is
    ordinary intra-component wiring and is neither.

    A THIRD, EARLIER exit (OI-48 ruled (d), WI-494): an edge whose
    DESTINATION is a declared shared-kernel module (`read_kernel_modules`) is
    not a seam at all — neither a finding nor the multi-membership advisory.
    Checked before the overlap split, so a kernel module that still carries a
    residual multi-tag is not ALSO advised about (the advisory exists to
    surface undeclared candidates; a module already declared kernel is a
    settled candidate, not an open one). One-directional by construction —
    the exemption keys on `dst_n`, never `src_n`, so an edge OUT of a kernel
    module stays exactly as policed as any other edge.

    ONE scan per run, cached per root: the two public wrappers used to each
    trigger their own scan from `main`, so the two tiers were computed from two
    separate reads of the same registries — the exact could-disagree state this
    function's contract forbids (and a review round demonstrated with a
    mid-run registry change). The cache makes the docstring's "computed in ONE
    pass" literally true for the process's lifetime.
    """
    cached = _SCAN_CACHE.get(str(root))
    if cached is not None:
        return cached
    # `covered` and `kernel` are resolved LAZILY: with zero classifiable edges
    # the old rule never read interfaces.csv (or now kernel-modules-allow) at
    # all, and an unreadable file must not turn a vacuous scan into a crash
    # (review finding, extended to the new surface for the same reason).
    covered = None
    kernel = None
    findings, advisories = [], []
    for src_n, dst_n, src_cmps, dst_cmps in _classifiable_edges(root):
        if covered is None:
            covered = _declared_seam_pairs(root)
        if (src_n, dst_n) in covered:
            continue
        if kernel is None:
            kernel = read_kernel_modules(root)
        if dst_n in kernel:
            continue
        edge = "{} ({}) -> {} ({})".format(
            src_n,
            "/".join(sorted(src_cmps)),
            dst_n,
            "/".join(sorted(dst_cmps)),
        )
        if src_cmps & dst_cmps:
            multi = [m for m, c in ((src_n, src_cmps), (dst_n, dst_cmps)) if len(c) > 1]
            if multi:
                advisories.append(
                    "multi-component module(s) {} suppress the cross-component "
                    "seam rule on import {} — the shared tag, not a declared "
                    "IF-### row, is what silences this edge; split the module, "
                    "give the shared part its own component, or declare the "
                    "seam in {} (advisory only — never the exit "
                    "code)".format(", ".join(multi), edge, IF_CSV)
                )
            continue
        findings.append(
            "cross-component import {} has no declared IF-### seam — declare "
            "the interface row in {} or retag the membership, or set "
            "docs/process.toml [checks] components_check = false".format(edge, IF_CSV)
        )
    _SCAN_CACHE[str(root)] = (findings, advisories)
    return findings, advisories


def cross_component_findings(root):
    """The cross-CMP-edge-without-IF rule (WI-064; the AXES accepted model's
    "Enforceability" ruling, process-options.md "Component layer"): an internal
    import edge whose endpoints belong to *different* CMP-### components must be
    covered by a declared IF-### row — an undeclared cross-component coupling is
    a finding, mechanized from the same committed artifacts the other component
    rules read. The CALLER gates the opt-out (`component_findings` shares
    `[checks] components_check`) and the WARN-plain / ERROR-under-`--strict`
    promotion. See `_cross_component_scan` for the tier split (this is tier one)
    and `_classifiable_edges` for the vacuity guards this rule inherits —
    including the DELIBERATE vacuousness for an endpoint carrying no
    `Component` tag, which stays the containment rule's job, not this one's.
    Since OI-48 (WI-494) an edge into a declared shared-kernel module
    (`read_kernel_modules`, `docs/kernel-modules-allow`) is exempted here
    before either tier — see `_cross_component_scan`'s "THIRD, EARLIER exit".

    Implements: SR-159, LLR-067
    """
    return _cross_component_scan(root)[0]


def cross_component_advisories(root):
    """The multi-membership overlap advisory (WI-440, OI-14's third
    do-not-wait): the edges the overlap guard silences because an endpoint
    carries more than one `Component` tag — see `_cross_component_scan`.

    WARN-ONLY, never the exit code, not even under `--strict`: this reports a
    question about the PARTITION, and no partition has been ruled yet, so it
    must not block. Shares `component_findings`' `[checks] components_check`
    opt-out, which the caller does NOT gate for it — this function does."""
    if not read_components_check_enabled(root):
        return []
    return _cross_component_scan(root)[1]
