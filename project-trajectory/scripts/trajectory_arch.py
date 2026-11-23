#!/usr/bin/env python3
"""Architecture seams, components, contracts, and spec-boundary decisions.

This module is the architecture rule surface ``check_trajectory`` imports. It
composes five modules beneath it and re-exports their names: `arch_inputs`
(registry paths, dials, loaders, the declared scan profile and the source
inventory), `arch_interfaces` (interface connectivity, contract bodies and
seam-to-test coverage), `arch_tags` (the test-file tag rule and the
evidence column generated from the tags), `arch_seams` (cross-component edges and the declared kernel)
and `arch_components` (component containment, the How-SW top view and the
derivation record). It keeps one rule of its own, spec interface citations.
Trajectory lifecycle, phase, staleness, and CLI composition stay in
``check_trajectory``.

Component: CMP-006

``check_trajectory`` imports and re-exports this module's
architecture rule surface, which this module composes from `arch_inputs`,
`arch_interfaces`, `arch_tags`, `arch_seams` and `arch_components` and its own
spec-boundary rule. Inputs are a repository root, the spine/config files
beneath it and, for `tc_tag_findings`, the test files under the declared tests
root, whose tags it holds equal to the TC rows' `Evidence` cells and requires
of each accepted automated TC; outputs are normalized inventories or finding
strings. One function writes, `write_evidence`, the generated evidence column
into the test-case registry (`trace.py --regen-evidence` calls it); no module
of the surface exposes a command-line entry point.
"""

import re
import sys
from pathlib import Path

try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

from arch_inputs import (
    CMP_CSV,
    CMP_ID_RE,
    IF_CSV,
    IF_ID_RE,
    LLR_CSV,
    SPECS_DIR,
    TC_CSV,
    _MODULE_EXTS,
    _arch_scan_profile,
    _first_declared_line,
    _norm_module,
    _process_check,
    _split_refs,
    _stack_ini_get,
    arch_inventory,
    component_headers,
    implements_index,
    load_cmps,
    load_ifs,
    load_seams,
    read_components_check_enabled,
    read_interfaces_check_enabled,
)
from arch_interfaces import (
    IF_TC_ALLOW,
    IF_TC_SEED_RE,
    _contracts_grammar_findings,
    _declaration_sites,
    _external_body_findings,
    _header_declarations,
    _header_files,
    _no_surface_reason,
    _parse_if_tc_allow_full,
    _uniqueness_findings,
    contract_body_findings,
    contract_homes,
    if_tc_allow_growth,
    if_tc_allow_hygiene_findings,
    if_tc_allow_parse_findings,
    if_tc_coverage_findings,
    interface_findings,
    parse_if_tc_allow,
    read_if_tc_allow,
    unchecked_contract_rows,
)
from arch_tags import (
    evidence_regen,
    evidence_regen_report,
    generated_evidence,
    tc_tag_findings,
    write_evidence,
)
from arch_seams import (
    KERNEL_ALLOW,
    KERNEL_ALLOW_SEP,
    _SCAN_CACHE,
    _classifiable_edges,
    _cross_component_scan,
    _call_cover,
    _parse_kernel_allow,
    cross_component_findings,
    kernel_allow_parse_findings,
    read_kernel_modules,
)
from arch_components import (
    TOP_VIEW_MAX,
    _cmp_roots,
    component_findings,
    component_top_view,
    derivation_record_findings,
    knowledge_packs,
)


# --- specs act on declared interface boundaries (WI-191) -----------------------
_IF_TOKEN_RE = re.compile(r"\bIF-\d+\b")
_INTERFACES_HEADING_RE = re.compile(r"(?im)^[ \t]*##[ \t]+Interfaces\b.*$")
# The intra-module escape hatch (PROCESS.md §8 scoping): a spec whose WIs act only
# within one module states that instead of inventing a seam.
_INTRA_MODULE_RE = re.compile(
    r"intra-module|single-module|no (?:cross-module )?seam|no interface|no cross-module",
    re.I,
)


def _spec_interfaces_section(text):
    """The body of a spec's `## Interfaces` section (between that heading and the
    next `## ` heading / EOF), or None when the spec has no such heading — the
    unarmed case that keeps the check vacuous-until-armed."""
    m = _INTERFACES_HEADING_RE.search(text)
    if not m:
        return None
    rest = text[m.end() :]
    nxt = re.search(r"(?m)^[ \t]*##[ \t]+", rest)
    return rest[: nxt.start()] if nxt else rest


def _armed_specs(root):
    """The live `docs/specs/` files that are real specs-of-record, sorted.

    The skip rule is a POLICY — the specs README documents the convention in
    prose and `WI-000` is the inert example, so neither is an armed spec — and it
    was stated at both walk sites. WI-344's `spec-scan` block; stating it once
    means a change to what counts as armed cannot land in one checker and not the
    other. Empty (never an error) when there is no specs dir."""
    specs = root / SPECS_DIR
    if not specs.is_dir():
        return []
    return [
        path
        for path in sorted(specs.glob("*.md"))
        if path.name.lower() != "readme.md" and not path.stem.endswith("-000")
    ]


def spec_interface_findings(root):
    """WI-191 — a spec-of-record acts on DECLARED interface boundaries. A spec's
    `## Interfaces` section must cite only IF-### seams that resolve in
    `interfaces.toml` (the one seam home, PROCESS.md §8). WARN plain / ERROR
    under `--strict` (DevStg-Tests+), like `component_findings`; the caller owns
    that promotion.

    THE ANTI-DUPLICATION ARM RETIRED AT WI-442, AND IT IS NOT A SILENT DROP.
    Until decision 4 this function also demanded a rationale on the citation line
    of any `Stability = Experimental` seam — the forced nearest-existing-IF
    search. Its arming input was DELETED: the slimmed tier has one maturity
    field with two values, and neither means what `Experimental` meant ("proposed
    and not yet pinned by a second consumer"). Re-keying onto `acceptance ==
    "draft"` was the obvious move and is the WRONG one: it silently changes the
    predicate to "not yet accepted", which on this repo's registry arms 113 of
    113 rows instead of 5, and it does so at a severity that ERRORS under
    --strict. A rule whose blast radius multiplies twentyfold while its sentence
    stays the same is not the same rule.

    So the arm is GONE rather than approximated, and its loss is a recorded
    finding of the re-tier (log entry, WI-442) with a home at sitting 3: if the
    forced search is worth keeping, it needs a value that means "proposed",
    which is a vocabulary decision (D-9/decision 12), not a checker's to invent.

    **Vacuous-until-armed:** a spec with no `## Interfaces` heading is skipped, so
    existing specs and downstream repos keep passing until they adopt the section.
    An armed section that cites no resolvable IF-### AND states no intra-module
    escape (PROCESS.md §8) is itself a finding — an empty-ceremony section."""
    specs = root / SPECS_DIR
    if not specs.is_dir():
        return []
    if_rows = {r["id"]: r for r in load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))}
    out = []
    for path in _armed_specs(root):
        section = _spec_interfaces_section(
            path.read_text(encoding="utf-8", errors="replace")
        )
        if section is None:
            continue  # unarmed — no `## Interfaces` section
        rel = "{}/{}".format(SPECS_DIR, path.name)
        ids = list(dict.fromkeys(_IF_TOKEN_RE.findall(section)))
        if not ids:
            if not _INTRA_MODULE_RE.search(section):
                out.append(
                    "{}: `## Interfaces` cites no IF-### and states no "
                    "intra-module escape — cite the seam(s) the WI acts on, or "
                    "state the intra-module case (PROCESS.md §8)".format(rel)
                )
            continue
        for iid in ids:
            if iid not in if_rows:
                out.append(
                    "{}: `## Interfaces` cites {} which resolves to no row in "
                    "{}".format(rel, iid, IF_CSV)
                )
    return out


__all__ = (
    "_first_declared_line",
    "_process_check",
    "_split_refs",
    "TC_CSV",
    "IF_CSV",
    "LLR_CSV",
    "CMP_CSV",
    "SPECS_DIR",
    "TOP_VIEW_MAX",
    "IF_ID_RE",
    "KERNEL_ALLOW",
    "KERNEL_ALLOW_SEP",
    "IF_TC_ALLOW",
    "IF_TC_SEED_RE",
    "CMP_ID_RE",
    "read_interfaces_check_enabled",
    "read_components_check_enabled",
    "_MODULE_EXTS",
    "_norm_module",
    "load_ifs",
    "load_seams",
    "_contracts_grammar_findings",
    "_header_files",
    "_header_declarations",
    "arch_inventory",
    "component_headers",
    "interface_findings",
    "_declaration_sites",
    "_no_surface_reason",
    "unchecked_contract_rows",
    "contract_body_findings",
    "_external_body_findings",
    "_uniqueness_findings",
    "contract_homes",
    "_parse_if_tc_allow_full",
    "parse_if_tc_allow",
    "read_if_tc_allow",
    "if_tc_allow_growth",
    "if_tc_coverage_findings",
    "if_tc_allow_hygiene_findings",
    "if_tc_allow_parse_findings",
    "tc_tag_findings",
    "generated_evidence",
    "evidence_regen",
    "evidence_regen_report",
    "write_evidence",
    "implements_index",
    "load_cmps",
    "_cmp_roots",
    "component_top_view",
    "knowledge_packs",
    "_stack_ini_get",
    "_arch_scan_profile",
    "_call_cover",
    "_parse_kernel_allow",
    "read_kernel_modules",
    "kernel_allow_parse_findings",
    "_classifiable_edges",
    "_SCAN_CACHE",
    "_cross_component_scan",
    "cross_component_findings",
    "derivation_record_findings",
    "component_findings",
    "_IF_TOKEN_RE",
    "_INTERFACES_HEADING_RE",
    "_INTRA_MODULE_RE",
    "_spec_interfaces_section",
    "_armed_specs",
    "spec_interface_findings",
)
