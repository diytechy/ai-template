#!/usr/bin/env python3
"""The cross-component seam check: an import between components needs a declared interface row.

`cross_component_findings` reports each internal import edge that is not
inside one component and that no interface row covers, and each edge touching
a file with no valid `Component:` declaration, as unclassified. An edge into a
module declared in `docs/kernel-modules-allow` is not a seam. The edges come
from `arch_inputs.arch_inventory` and resolve through
`gen_arch_map.resolve_import`; membership is the files' headers
(`arch_inputs.component_headers`) through `kitlib.spine.module_components`.
One scan per root per run, held in `_SCAN_CACHE`. ``trajectory_arch`` re-exports the rule for
``check_trajectory``, and `arch_components` runs it inside
`component_findings`.

Component: CMP-006

Contracts: IF-319 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-319: the seam rule surface ``trajectory_arch`` re-exports and
`arch_components` composes. `cross_component_findings(root)` returns finding
strings from one cached scan per root, and leaves the `[checks]
components_check` dial to its caller.
`read_kernel_modules(root)` gives the declared kernel as `{module key:
reason}`, empty when the file is absent, and
`kernel_allow_parse_findings(root)` names the first line its grammar cannot
read. A `gen_arch_map` without `resolve_import` or `package_paths` leaves both
tiers silent. The module performs no writes.
"""

import sys
from pathlib import Path

try:
    from kitlib import config as _kitconfig
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import config as _kitconfig
    from kitlib import spine as _kitspine

import spine_carrier
from arch_inputs import (
    CMP_CSV,
    IF_CSV,
    _arch_scan_profile,
    _norm_module,
    arch_inventory,
    component_headers,
    load_cmps,
    load_seams,
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
KERNEL_ALLOW_SEP = _kitconfig.DECLARED_SEP  # the one declared-file separator


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
    entries, unparsed = _kitconfig.declared_entries(Path(root) / KERNEL_ALLOW)
    out = []
    for lineno, head, reason, line in entries:
        module = _norm_module(head)
        if not module or not reason:
            unparsed.append((lineno, line))
            continue
        out.append((module, reason, lineno))
    return out, sorted(unparsed)


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
    — both endpoints normalized, each with the REAL CMP ids its files' headers
    declare, an empty set for a module with no valid declaration.

    The vacuity guards live here, so every caller inherits them: no internal
    imports, no real CMP rows, an import that resolves to no inventory module,
    to several, or to the importing module itself, and a `gen_arch_map` too old
    to resolve one (IF-131: every entry point is optional at the call site, and
    a missing one silences the rule). An endpoint with no declaration is NOT a
    guard: it is yielded, for the caller to report as unclassified.

    Each import is the token `gen_arch_map.internal_imports` wrote, bare
    (`agent_route`), dotted (`kitlib.spine`) or relative (`.registry`), and
    `gen_arch_map.resolve_import` is its one resolution, the one the
    dependency diagram draws by. Whether an importer is a package, which a
    relative import starts from, is read from its file through
    `gen_arch_map.package_paths`, not guessed from the modules under it. Looking the whole token up by its last path
    segment, as this rule once did, missed every dotted and relative import,
    so no edge into a package was ever checked.

    Implements: SR-159, LLR-374, LLR-067
    """
    names, _contracts, imports = arch_inventory(root)
    resolve = getattr(gen_arch_map, "resolve_import", None)
    package_paths = getattr(gen_arch_map, "package_paths", None)
    if not imports or resolve is None or package_paths is None:
        return
    cmp_ids = {c["id"] for c in load_cmps(spine_carrier.load(root / CMP_CSV, "CMP-ID"))}
    if not cmp_ids:
        return
    # An import's endpoints are the Python modules the inventory walks, so only
    # their declarations place an edge: a declared `b.sh` on `b.py`'s key must
    # not lend its component to an undeclared `b.py` (the Trust ruling).
    declared = component_headers(root)[0]
    raw = _kitspine.module_components(
        {path: cmp for path, cmp in declared.items() if path.endswith(".py")}
    )
    membership = {n: tags & cmp_ids for n, tags in raw.items()}
    modules = {_norm_module(m) for m in names} - {""}
    src, _mode = _arch_scan_profile(root)
    scan_dir = root / src.strip().replace("\\", "/").rstrip("/")
    packages = {_norm_module(p) for p in package_paths([scan_dir])}
    for src in sorted(imports):
        src_n = _norm_module(src)
        for token in sorted(imports[src]):
            dst_n = resolve(token, src_n, modules, packages)
            if dst_n and dst_n != src_n:
                yield (
                    src_n,
                    dst_n,
                    membership.get(src_n, set()),
                    membership.get(dst_n, set()),
                )


_SCAN_CACHE = {}


def _edge_label(src_n, src_cmps, dst_n, dst_cmps):
    return "{} ({}) -> {} ({})".format(
        src_n,
        "/".join(sorted(src_cmps)) or "no component",
        dst_n,
        "/".join(sorted(dst_cmps)) or "no component",
    )


def _cross_component_scan(root):
    """The cross-CMP rule's findings over the internal import edges, in one
    pass.

    THE TRUST RULING FIRST (WI-1021): an edge with an endpoint whose header
    declares no valid component cannot be judged, so it is reported as
    UNCLASSIFIED before the declared seams and the kernel are read — never
    treated as internal, covered or exempt.

    Then an edge whose module pair a declared IF-### row covers is silent, and
    so is an edge whose DESTINATION is a declared shared-kernel module
    (`read_kernel_modules`, OI-48 ruled (d), WI-494): consumed across
    components by design, it is not a seam. One-directional by construction —
    the exemption keys on `dst_n`, never `src_n`, so an edge OUT of a kernel
    module stays exactly as policed as any other edge.

    An edge is INTERNAL only when both endpoints sit in the same one component.
    Every other edge is a finding. Two files can share a module key
    (`check.py` and `check.sh`), so a key can carry two components; such an
    edge is not internal, and a second declaration on a shared key cannot
    silence an edge the way a second design-row tag once did (the
    multi-membership advisory, WI-440, retired with that cause).

    ONE scan per run, cached per root, so two callers in one process can never
    read two answers from one tree.
    """
    cached = _SCAN_CACHE.get(str(root))
    if cached is not None:
        return cached
    # `covered` and `kernel` are resolved LAZILY: with no edge to judge the rule
    # never reads interfaces.toml or kernel-modules-allow, and an unreadable
    # file must not turn a vacuous scan into a crash.
    covered = None
    kernel = None
    findings = []
    for src_n, dst_n, src_cmps, dst_cmps in _classifiable_edges(root):
        edge = _edge_label(src_n, src_cmps, dst_n, dst_cmps)
        if not src_cmps or not dst_cmps:
            findings.append(
                "cross-component import {} is unclassified: a module in no "
                "component cannot be judged — declare its component in its "
                "`Component:` header (process.md §8), or set docs/process.toml "
                "[checks] components_check = false".format(edge)
            )
            continue
        if covered is None:
            covered = _declared_seam_pairs(root)
            kernel = read_kernel_modules(root)
        if (src_n, dst_n) in covered or dst_n in kernel:
            continue
        if len(src_cmps) == 1 and src_cmps == dst_cmps:
            continue
        findings.append(
            "cross-component import {} has no declared IF-### seam — declare "
            "the interface row in {} or the component in the header, or set "
            "docs/process.toml [checks] components_check = false".format(edge, IF_CSV)
        )
    _SCAN_CACHE[str(root)] = findings
    return findings


def cross_component_findings(root):
    """The cross-CMP-edge-without-IF rule (WI-064; the AXES accepted model's
    "Enforceability" ruling, process-options.md "Component layer"): an internal
    import edge that is not inside one CMP-### component must be covered by a
    declared IF-### row — an undeclared cross-component coupling is a finding,
    mechanized from the same committed artifacts the other component rules
    read — and an edge touching a module whose header declares no valid
    component is reported as unclassified. The CALLER gates the opt-out
    (`component_findings` shares `[checks] components_check`) and the
    WARN-plain / ERROR-under-`--strict` promotion. See `_cross_component_scan`
    for the classification and `_classifiable_edges` for the vacuity guards.
    An edge into a declared shared-kernel module (`read_kernel_modules`,
    `docs/kernel-modules-allow`, OI-48, WI-494) is exempted once both ends
    are declared.

    Implements: SR-159, LLR-067
    """
    return _cross_component_scan(root)
