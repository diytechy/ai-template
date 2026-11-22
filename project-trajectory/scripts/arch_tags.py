#!/usr/bin/env python3
"""Tag crosschecks: `Implements:` tags against design rows, test-file tags against test cases.

Two rules over declarations written beside the code and the tests. The
CodeSymbol crosscheck (`codesymbol_crosscheck_findings`, warn-first) holds
each live LLR's `Implements:` tag site to its row's `Module` and `CodeSymbol`
cells. The test-file tag rule (`tc_tag_findings`) reports each refused tag,
each difference between a test case's tags and its `Evidence` cell, and each
accepted automated case no test declares. Their inputs come from
`arch_inputs`; ``trajectory_arch`` re-exports them for ``check_trajectory``.

Component: CMP-006

Contracts: IF-318 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-318: the tag rule surface ``trajectory_arch`` re-exports.
`codesymbol_crosscheck_findings(root)` returns one finding string per
`Implements:` tag site that its row's `CodeSymbol` and `Module` cells do not
contain, `[]` in files mode, with no source root or with no design rows to
compare. `tc_tag_findings(root, tests_dir)` returns each refused tag as
`<file>:<line>: <shape>: <detail>`, then the tag and evidence differences,
then the accepted automated cases no test declares, `[]` with no test-case
registry. Both read `gen_arch_map`'s walks, and neither writes.
"""

import re
import sys
from pathlib import Path

try:
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import spine as _kitspine

import spine_carrier
from arch_inputs import LLR_CSV, TC_CSV, _arch_scan_profile, _norm_module, _split_refs

try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None


# --- Implements-tag vs CodeSymbol crosscheck (WI-502; OI-53 ruled (d)) --------
# The 2026-08-21 closing review found the CodeSymbol dozen (WI-501) by hand:
# resolve every `Implements:` tag's ENCLOSING def/class and compare it against
# its row's `CodeSymbol`/`Module` claim. This promotes that manual method into
# a continuous warn-first finding, so the next stale batch is measured rather
# than rediscovered by campaign. WARN-FIRST FOREVER by the ruling — no
# allowlist, no `--strict` arm — because it checks a TRACED, not ACCEPTED,
# cell (process.md §8's `Module`/`CodeSymbol`/`TestRefs` "traced, not
# accepted" posture, cited at check_trajectory.py:77) and a mismatch is
# routine drift, not a defect to gate a commit over.
#
# ONE HOME for the AST walk (WI-486): `gen_arch_map.implements_report` builds
# the (tag site -> enclosing symbol) map and the known-symbol-name set; this
# function only compares them against the registry, the way `arch_inventory`
# already consumes `gen_arch_map.scan_inventory` rather than re-walking trees.
_CODESYMBOL_SPLIT_RE = re.compile(r"[/;]|\s\+\s")


def _codesymbol_candidates(cell):
    """A `CodeSymbol` cell's symbol names, trimmed. `CodeSymbol` is authored
    prose-adjacent, not a strict machine grammar — measured across the live
    registry it mixes `/` (`run/classify`), `;` (`tier_legend...; STATUS_GLYPH`)
    and a spaced ` + ` (`PHASE_ACCENTS + _ring_ink`) as the same "and also"
    join, sometimes in one cell. Splitting on all three costs nothing when a
    candidate is real prose rather than a name — an unmatched fragment simply
    never satisfies containment — and undercounts nothing a single-character
    splitter would have caught, so the wider split is the conservative one."""
    return [c.strip() for c in _CODESYMBOL_SPLIT_RE.split(cell or "") if c.strip()]


def _codesymbol_site_finding(
    rid, site, qualname, module_cell, code_symbol_cell, module_ok, known_names
):
    """One `codesymbol_crosscheck_findings` tag site, resolved to a finding
    string or `None` — split out so the caller's loop stays a plain walk
    (C901) and this comparison, the actual rule, reads as one thing. See
    `codesymbol_crosscheck_findings` for the containment/mismatch/unresolvable
    vocabulary this implements."""
    candidates = _codesymbol_candidates(code_symbol_cell)
    if not candidates:
        contained = module_ok and qualname == ""
    else:
        # Containment reads BOTH directions of the dotted path: a cell naming
        # the CLASS (`RoutingState`) is a prefix of a method's qualname, but
        # the registry just as often names the bare METHOD (`stall_verdict`,
        # no `RoutingState.` qualifier) — the rendered map's own `methods` row
        # lists them unqualified, and most live CodeSymbol cells follow that
        # convention. A suffix match covers that shape without opening the
        # door to a coincidental same-named method on an unrelated class:
        # `Foo.stall_verdict` and `Bar.stall_verdict` both satisfy a bare
        # `stall_verdict` cell, which is the map's own granularity limit, not
        # one this rule invents.
        contained = module_ok and any(
            qualname == c or qualname.startswith(c + ".") or qualname.endswith("." + c)
            for c in candidates
        )
    if contained:
        return None
    enclosing = qualname or "(module scope)"
    resolvable = any(
        c == n or n.endswith("." + c) for c in candidates for n in known_names
    )
    if candidates and not resolvable:
        return (
            "{} tag at {} encloses `{}`, but the row's CodeSymbol `{}` does "
            "not resolve to any def/class under the scanned source — "
            "unresolvable, not matched (Module `{}`)".format(
                rid, site, enclosing, code_symbol_cell, module_cell
            )
        )
    return "{} tag at {} encloses `{}`, but the row's CodeSymbol claims `{}` (Module `{}`)".format(
        rid, site, enclosing, code_symbol_cell or "(module-only)", module_cell
    )


def codesymbol_crosscheck_findings(root):
    """Every live LLR's `Implements:` tag site under the declared arch-map
    source surface (`docs/stack.ini` `[paths] src`), checked by CONTAINMENT
    against its row's `CodeSymbol` + `Module` cells: a tag inside
    `RoutingState.note_session` satisfies a cell naming `RoutingState`; a tag
    at module scope satisfies a module-only (empty `CodeSymbol`) cell. Two
    finding shapes, distinguished so a reader (and the regression tests) can
    tell "the cell names a different REAL symbol" from "the cell names
    nothing resolvable at all" (a function-local variable, or a symbol that
    is simply gone) — the WI-429 census defect this crosscheck is built to
    keep from recurring silently:

    - **mismatch**: at least one of the cell's candidate names IS a real
      def/class somewhere in the scanned surface, just not one that contains
      this tag's site.
    - **unresolvable**: none of the cell's candidate names resolve to any
      real def/class anywhere in the surface — the cell cannot be verified,
      and reporting it as a silent match would be the false-quiet defect
      `docs/enforcement-audit.md` item 5 already names for a neighboring
      grammar (`Contracts:`); this rule does not inherit that shape.

    `[]` (vacuous) when `[arch-map] mode = files` (no parser) or the LLR
    registry has no `Module`/`CodeSymbol` cells to compare against. A tag
    naming an id with no live LLR row, or an LLR id with an empty `Module`
    AND `CodeSymbol` (nothing claimed), is silently skipped — orphan/schema
    integrity is `trace.py`'s finding, not this one's."""
    if gen_arch_map is None:
        return []
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    if not src_dir.exists():
        return []
    rows = {}
    for r in spine_carrier.load(root / LLR_CSV, "LLR-ID"):
        lid = (r.get("LLR-ID") or "").strip()
        if not lid.startswith("LLR-") or lid.endswith("-000"):
            continue
        module_cell = (r.get("Module") or "").strip()
        code_symbol_cell = (r.get("CodeSymbol") or "").strip()
        if module_cell or code_symbol_cell:
            rows[lid] = (module_cell, code_symbol_cell)
    if not rows:
        return []
    sites, known_names = gen_arch_map.implements_report([src_dir])
    findings = []
    for rel, tags in sorted(sites.items()):
        file_module = _norm_module(rel)
        for lineno, ids, qualname in tags:
            for rid in ids:
                if rid not in rows:
                    continue
                module_cell, code_symbol_cell = rows[rid]
                declared_modules = {_norm_module(m) for m in _split_refs(module_cell)}
                module_ok = not declared_modules or file_module in declared_modules
                finding = _codesymbol_site_finding(
                    rid,
                    "{}:{}".format(rel, lineno),
                    qualname,
                    module_cell,
                    code_symbol_cell,
                    module_ok,
                    known_names,
                )
                if finding:
                    findings.append(finding)
    return findings


# Test-file tags and `Evidence` cells are two homes of one fact, and this check
# holds them equal only until the evidence column is generated from the tags.
# That work deletes this helper and its one call in `tc_tag_findings`. Nothing
# here builds the retirement.
def _tag_evidence_findings(rows, tags, refused, tests_dir):
    """Each difference between a live TC's tags and its `Evidence` parts under
    `tests_dir`, as `<TC>: evidence without a tag: <node>` or `<TC>: tag without
    evidence: <node>`, sorted by TC, then node.

    `rows` are the live TC rows, `tags` is `read_test_tags`' map, and `refused`
    holds the files it could not read, whose parts name nothing it could see, so
    they add no finding here. A part is its path, or its path and node with any
    `[case]` dropped; a part outside `tests_dir` is outside the rule.

    Implements: SR-157, LLR-366"""
    prefix = "".join(p + "/" for p in Path(tests_dir.replace("\\", "/")).parts)
    found = []
    for row in rows:
        tc = (row.get("TC-ID") or "").strip()
        parts = {
            path + "::" + node.split("[", 1)[0] if node else path
            for path, node in _kitspine.evidence_items(row.get("Evidence"))
            if path.startswith(prefix) and path not in refused
        }
        declared = set(tags.get(tc, ()))
        found += [(tc, n, "evidence without a tag") for n in parts - declared]
        found += [(tc, n, "tag without evidence") for n in declared - parts]
    return ["{}: {}: {}".format(tc, kind, n) for tc, n, kind in sorted(found)]


def _undeclared_case_findings(rows, tags, refused):
    """`<TC>: no test declares it` for each accepted or founded case whose
    `Automated` cell reads `yes`, stripped and case-folded as `trace.py` reads
    it, that no tag in `tags` names, sorted by TC.

    The cell decides nothing else: a note, no cell, a part outside the tests
    root and a path the tree lacks all read the same. A case with an `Evidence`
    part in a file `refused` as unreadable adds nothing, since that file's
    refusal is already a finding. It reads declarations only, so a tagged test
    still failing is clean here. It stays when the equality check retires.

    Implements: SR-157, LLR-395"""
    found = []
    for row in rows:
        tc = (row.get("TC-ID") or "").strip()
        owed = _kitspine.is_accepted(row) or _kitspine.is_founded(row)
        owed = owed and (row.get("Automated") or "").strip().casefold() == "yes"
        if not owed or tags.get(tc):
            continue
        parts = _kitspine.evidence_items(row.get("Evidence"))
        if not any(path in refused for path, _node in parts):
            found.append(tc)
    return ["{}: no test declares it".format(tc) for tc in sorted(found)]


def tc_tag_findings(root, tests_dir):
    """Each refused test-file tag under `tests_dir`, the declared tests root, as
    a `<file>:<line>: <shape>: <detail>` string, then each difference between the
    tags and the `Evidence` cells (`_tag_evidence_findings`), then each accepted
    automated case no tag declares (`_undeclared_case_findings`).
    `check_trajectory` owns the declared-root read, so the value is handed in.

    `[]` (vacuous) with no TC registry, and with no tests root, which
    `read_test_tags` walks as no files and the comparison must not read as every
    part untagged. `[arch-map] mode = files` is no reason to be vacuous: this
    reads test files, not the source surface. A registry holding only `-000` rows
    is not vacuous either, so every tag there is unknown. No `hasattr` guard,
    unlike the other architecture rules' `gen_arch_map` reads: a stale sibling
    must fail loudly, since "no tags" is the reading this rule refuses. A
    placeholder row is not loaded, so it owes no declaration.

    Implements: SR-157, LLR-365, LLR-366"""
    if gen_arch_map is None or spine_carrier.resolve(root / TC_CSV) is None:
        return []
    rows = spine_carrier.load(root / TC_CSV, "TC-ID", False)
    live_tcs = {(r.get("TC-ID") or "").strip() for r in rows}
    tags, findings = gen_arch_map.read_test_tags(root, tests_dir, live_tcs)
    lines = [
        "{}:{}: {}: {}".format(f["file"], f["line"], f["shape"], f["detail"])
        for f in findings
    ]
    if (root / tests_dir).is_dir():
        refused = {f["file"] for f in findings if f["shape"] == "unreadable"}
        lines += _tag_evidence_findings(rows, tags, refused, tests_dir)
        lines += _undeclared_case_findings(rows, tags, refused)
    return lines
