#!/usr/bin/env python3
"""Interface-registry rules: seam connectivity, contract bodies and seam-TC coverage.

Three rules over `docs/requirements/interfaces.toml` and the `Contracts:`
declarations in the source tree: connectivity coverage
(`interface_findings`, warn-first), the armed definition gate
(`contract_body_findings`), and seam-TC coverage with its migration allowlist
`docs/if-tc-coverage-allow` (`if_tc_coverage_findings`, and the allowlist's
hygiene and parse rules). Their inputs come from `arch_inputs`;
``trajectory_arch`` re-exports them for ``check_trajectory``.

Component: CMP-006

Contracts: IF-317 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-317: the interface-registry rule surface ``trajectory_arch``
re-exports. Each rule takes a repository root and returns finding strings,
`[]` when `[checks] interfaces_check = false` or its input is vacuous:
`interface_findings`, `contract_body_findings`, `unchecked_contract_rows`,
`if_tc_coverage_findings`, `if_tc_allow_hygiene_findings` and
`if_tc_allow_parse_findings`. `parse_if_tc_allow(text)` gives the
allowlist's entries and its declared seed count, and `read_if_tc_allow(root)`
the ids it exempts with their reasons. The caller decides each finding's
severity, and the module performs no writes.
"""

import ast
import re
import sys
from pathlib import Path

try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

from arch_inputs import (
    IF_CSV,
    IF_ID_RE,
    TC_CSV,
    _arch_scan_profile,
    _norm_module,
    arch_inventory,
    load_ifs,
    load_seams,
    read_interfaces_check_enabled,
)

try:
    import gen_arch_map
except ImportError:
    try:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gen_arch_map
    except ImportError:
        gen_arch_map = None


# The seam-TC coverage migration allowlist (OI-43 ruled (a), WI-488) — see
# `read_if_tc_allow`.
IF_TC_ALLOW = "docs/if-tc-coverage-allow"
# The allowlist's machine-readable baseline: how many of its entries are the
# SEEDED population (which shares one reason, stated once in the header). Past
# that count an entry is an addition and must carry its own ` — <reason>`.
IF_TC_SEED_RE = re.compile(r"^#\s*seed-count:\s*(\d+)\s*$")


def _contracts_grammar_findings(root):
    """Marker-grammar findings over the declared scan root, or `[]` where the
    tree cannot be read.

    Degrades to silence on a missing `gen_arch_map`, files-mode or an absent
    scan root, exactly as `arch_inventory` does — a detector that crashed in a
    scaffold would be removed from the floor, which is the same outcome as not
    having it."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "contracts_grammar_findings"):
        return []
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    if not src_dir.is_dir():
        return []
    found = []
    for path in sorted(src_dir.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        found.extend(
            gen_arch_map.contracts_grammar_findings(path.name, tree, text.splitlines())
        )
    # The file owners — registries, config, hooks — read through the same
    # grammar (OI-67 slice 2), so a lossy marker in a header is named too.
    if hasattr(gen_arch_map, "file_grammar_findings"):
        for owner, path in _owner_files(root):
            found.extend(gen_arch_map.file_grammar_findings(owner, path))
    return found


def _owner_files(root):
    """`gen_arch_map.owner_files` over the live registry; `[]` when the
    generator is absent or predates the file-owner scan."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "owner_files"):
        return []
    return gen_arch_map.owner_files(root, spine_carrier.load(root / IF_CSV, "IF-ID"))


def _file_owner_declarations(root, out):
    """`{owner: {IF ids}}` declared by the file owners' headers; a header the
    grammar refuses is reported into `out` and read as declaring nothing."""
    declared = {}
    for owner, path in _owner_files(root):
        try:
            ids, _bodies = gen_arch_map.file_contracts(path)
        except gen_arch_map.ContractsGrammarError as exc:
            out.append("{}: {}".format(owner, exc))
            continue
        if ids:
            declared[owner] = set(ids)
    return declared


def interface_findings(root):
    """Architecture-connectivity coverage warns (S5/WI-056; process.md §8), all
    warn-first — the caller prints them and they never change the exit code, at
    any gate. Returns the warn strings ([] when opted out or vacuous).

    Ruled opt-out, default-on: fires even with an empty/absent `interfaces.csv`
    (a multi-module arch-map with no declared seams reads "connectivity
    undeclared"); silenced only by `[checks] interfaces_check = false` or a ≤1-module
    inventory (nothing to connect).

    Implements: SR-159, LLR-042
    """
    if not read_interfaces_check_enabled(root):
        return []
    inventory, declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect (or no arch-map yet) — vacuous
    ifs = load_seams(root)
    out = []
    if not ifs:
        return [
            "connectivity undeclared: the {}-module architecture declares no "
            "interfaces — add IF-### rows to {}, or set docs/process.toml "
            "[checks] interfaces_check = false".format(len(inventory), IF_CSV)
        ]

    inv_norm = {_norm_module(m): m for m in inventory}
    inv_norm.pop("", None)
    endpoints, provides, consumes = set(), set(), set()
    sources, sinks = set(), set()
    for r in ifs:
        producer = _norm_module(r["owner"])
        consumer_ns = {_norm_module(c) for c in r["far"]} & set(inv_norm)
        endpoints.update(consumer_ns)
        if producer in inv_norm:
            endpoints.add(producer)
        # The honesty valve: a `source`/`sink` FIRST word in Notes marks the
        # row's own side a deliberate source (consumes nothing) / sink (provides
        # nothing), so it doesn't breed a boilerplate opposite-facing row. Since
        # WI-455 the marked side is named by the ROLE rather than by a column:
        # `source` marks the OWNER, `sink` marks the CONSUMERS — which is what
        # the two words meant when both were read off `ThisProject`.
        marker = r["notes"].split()
        first = marker[0].rstrip(":;,.") if marker else ""
        if first == "source":
            sources.add(producer)
        elif first == "sink":
            sinks.update(_norm_module(c) for c in r["far"])
        # Producer -> consumer credit, read off the resolved sides.
        if producer in inv_norm:
            provides.add(producer)
        consumes.update(consumer_ns)

    for n in sorted(inv_norm):
        module = inv_norm[n]
        if n not in endpoints:
            out.append(
                "connectivity undeclared: module {!r} is in the arch-map but no "
                "IF-### row names it".format(module)
            )
            continue
        if n not in consumes and n not in sources:
            out.append(
                "module {!r} declares no Consumes seam (mark it `source` in its "
                "IF row Notes if it deliberately consumes nothing)".format(module)
            )
        if n not in provides and n not in sinks:
            out.append(
                "module {!r} declares no Provides seam (mark it `sink` in its IF "
                "row Notes if it deliberately provides nothing)".format(module)
            )

    # Seam-TC citation: each declared IF id should be cited by >=1 TC (the rung-2
    # seam-TC rule, and process.md §8's "every interface is backed by an SR and a
    # contract/fixture test").
    #
    # THE ARMING KEY HAS NOW MOVED TWICE, AND THE THIRD SPELLING IS "ALL ROWS".
    # It first read `Status == Active`, which armed EXACTLY the 5 rows already
    # TC-cited — zero findings by construction. WI-443 re-keyed it to
    # `Stability == Stable` (103 of 108 uncited). WI-442 retired `Stability` for
    # `Approval`, and copying the shape forward as `Approval == "approved"` would
    # have reproduced the ORIGINAL tautology in a new column: every row reads
    # `draft` today, so the rule would arm on nothing and report a clean zero.
    #
    # So it arms on EVERY real IF row, and the maturity column drops out of the
    # rule entirely. That is the honest reading of the obligation anyway — an
    # interface is backed by a contract test or it is not; how settled its
    # contract is was never the question — and it is the one spelling that cannot
    # be silently disarmed by a vocabulary change.
    #
    # SUMMARISED, not one line per row, and that is a deliberate ergonomic choice
    # rather than a softening: this function runs in the shipped pre-commit hook,
    # where 103 warn lines is a check nobody reads and therefore a check that does
    # not work. One line carries the count, which is the number that has to fall.
    #
    # STAYS PURE WARN-FIRST, FOREVER, EVEN UNDER --strict — the promotable half
    # split off at WI-488 (OI-43 ruled (a)) into `if_tc_coverage_findings` below,
    # which reports only the seams NOT on the migration allowlist. This line keeps
    # reporting the TOTAL uncited count (allowlisted seams included) so the whole
    # debt stays visible even once the actionable subset goes quiet.
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    uncited = [r["id"] for r in ifs if r["id"] not in tc_cited]
    if uncited:
        shown = ", ".join(uncited[:5])
        out.append(
            "{} IF seam(s) are cited by no TC (a seam should carry a "
            "contract/fixture test, process.md §8){}: {}".format(
                len(uncited), " — first 5" if len(uncited) > 5 else "", shown
            )
        )

    # Marker-grammar honesty (OI-66): the `Contracts:` marker must OPEN its line
    # and parse as an id list, which is what stops prose that DENIES a
    # declaration from making one. Tightening a shipped grammar may not lose an
    # adopter's seams in silence, so both lossy forms — a marker-shaped line
    # whose id list will not parse, and a `Contracts:` carrying ids mid-line —
    # are reported by name. Warn-first: on this repo the count is zero, and on
    # an upgrading repo it is the migration list.
    out.extend(_contracts_grammar_findings(root))

    # Docstring citation: a `Contracts: IF-###` a script declares (harvested into
    # the arch-map) must exist in the registry; and, once the convention is in
    # use, a registry IF whose OWNER declares no matching citation warns too.
    registry_ids = {r["id"] for r in ifs}
    file_declared = _file_owner_declarations(root, out)
    for module, ids in sorted(declared_contracts.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "module {!r} docstring declares Contracts: {} but no such IF-### "
                "row exists".format(module, iid)
            )
    for owner, ids in sorted(file_declared.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "{!r} header declares Contracts: {} but no such IF-### row "
                "exists".format(owner, iid)
            )
    if declared_contracts or file_declared:  # reverse direction, once opted in
        out.extend(
            _owner_exact_findings(
                ifs,
                inv_norm,
                declared_contracts,
                file_declared,
                dict(_owner_files(root)),
            )
        )
    return out


def _owner_exact_findings(
    ifs, inv_norm, declared_contracts, file_declared, file_owners
):
    """OWNER-EXACT (OI-67 slice 2): the row's owner is the source that must
    declare it — a module's `Contracts:` line, or a file's header. An id
    declared on some OTHER module used to pass; that is the id-global hole the
    build round named, closed here. Every module in the INVENTORY is judged,
    not only the declaring ones — an owner that declares nothing at all is the
    plainest miss. An `external:` owner has nothing to scan; a directory with
    no README or an owner the tree cannot resolve falls back to the id-global
    read rather than warning about a header nobody could write."""
    out = []
    by_module = {_norm_module(m): ids for m, ids in declared_contracts.items()}
    all_declared = set().union(*declared_contracts.values(), *file_declared.values())
    for r in ifs:
        owner, iid = r["owner"], r["id"]
        if not owner or owner.startswith("external:"):
            continue
        norm = _norm_module(owner)
        if norm in inv_norm:
            if iid not in by_module.get(norm, set()):
                out.append(
                    "IF {} is owned by {!r}, but that module's Contracts: line "
                    "does not declare it — the owner is the one declaration "
                    "site".format(iid, owner)
                )
        elif owner in file_owners:
            if iid not in file_declared.get(owner, set()):
                out.append(
                    "IF {} is owned by {!r}, but that file's header declares "
                    "no Contracts: line naming it — the owner is the one "
                    "declaration site".format(iid, owner)
                )
        elif iid not in all_declared:
            out.append(
                "IF {} is in the registry but no source declares it via a "
                "Contracts: line".format(iid)
            )
    return out


# --- the armed definition gate (OI-67 slice 6) --------------------------------


def _declaration_sites(root):
    """`({key: (source_as_written, ids, bodies)}, problems)` — every source in
    the tree that declares a seam, read through the one harvester the
    interface reference uses (`gen_arch_map.scan_contracts`): the modules under
    the declared scan root, keyed by normalized module path (`scripts/check`),
    and the file owners the registry names, keyed by the owner as the registry
    spells it (`docs/stack.ini`, `hooks/pre-commit`). `problems` is
    `[(source, message)]` for every header the contract GRAMMAR refused, so a
    refusal is reported rather than read as "declares nothing" — and, above
    all, rather than DISARMING the gate: the refusal used to be caught for the
    whole scan and answered with `(None, [])`, so one malformed body anywhere
    in the tree silenced every other row's verdict too (adversarial review
    2026-08-29, F1). A refused source is absent from `sites` rather than
    entered as declaring nothing, which would hand its rows to the reverse
    check's warn instead of this gate's finding. A source the scan could not
    READ is deliberately NOT in `problems`: that is the reference's own "could
    not read" list and `arch_inventory`'s skip. `(None, problems)` when there
    is no surface to read — files-mode, an absent scan root, no generator
    beside this script — the `arch_inventory` posture (`_no_surface_reason`)."""
    if _no_surface_reason(root):
        return None, []
    src, _mode = _arch_scan_profile(root)
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    owner_files = _owner_files(root)
    refused = []
    records, _unreadable = gen_arch_map.scan_contracts(
        [src_dir], owner_files, grammar_errors=refused
    )
    file_names = {owner for owner, _path in owner_files}
    sites = {}
    for rel, _summary, ids, bodies in records:
        key = rel if rel in file_names else _norm_module(rel)
        sites[key] = (rel, set(ids), set(bodies))
    return sites, refused


def _no_surface_reason(root):
    """Why `_declaration_sites` has no surface to read, or None when it has
    one: files-mode, an absent scan root, or no generator beside this
    script."""
    if gen_arch_map is None or not hasattr(gen_arch_map, "scan_contracts"):
        return "gen_arch_map.py is not beside this script"
    src, mode = _arch_scan_profile(root)
    if mode == "files":
        return "[arch-map] mode = files reads no source headers"
    if not (root / src.strip().replace("\\", "/").rstrip("/")).is_dir():
        return "the scan root {!r} is absent".format(src.strip())
    return None


def unchecked_contract_rows(root):
    """One line naming how many IF rows the armed definition gate
    (`contract_body_findings`) passed without judging, and why; `[]` when it
    judged them all or the gate is opted out. Every row, where there is no
    surface to read; otherwise each `external:`-owned row whose far side names
    no in-tree module to state it. Warn-only: it changes no verdict, it only
    stops a vacuous pass reading as a checked one."""
    if not read_interfaces_check_enabled(root):
        return []
    rows = load_seams(root)
    why = _no_surface_reason(root)
    if why is None:
        why = "external-owned, and no in-tree module on the far side states them"
        rows = [
            r
            for r in rows
            if r["owner"].startswith("external:")
            and all(e.startswith("external:") for e in r["far"])
        ]
    if not rows:
        return []
    return ["contract bodies not checked for {} IF row(s): {}".format(len(rows), why)]


def contract_body_findings(root):
    """THE ARMED DEFINITION GATE (OI-67 slice 6). Every interface row must be
    STATED — declared on its owner's `Contracts:` marker and given a
    `Contract IF-###:` body there — because under the one-owner shape the body
    is the definition's only home: a row with no body is an interface with no
    definition. Returns finding strings; the caller prints them WARN plain and
    promotes them to ERROR under `--strict`, the `if_tc_coverage_findings`
    idiom, sharing its `[checks] interfaces_check` opt-out.

    ONE RULE, FOUR SHAPES. (1) The owner declares the id and states no body —
    "declared, not stated", the reference's own debt line, now a finding.
    (2) An `external:`-owned row is declared and stated by the kit module on
    its FAR SIDE — the consumer that reads the external surface, or the
    requestor that drives it — because the external party's header is not
    ours to write and that module is the one in-tree home of OUR READING of
    the surface; where the far side names several kit modules any one of them
    may state it. (3) A stray declaration — a source declaring an id the
    registry owns to a different in-tree source — because the owner is the
    ONE declaration site and a second copy is a second definition waiting to
    disagree; a far-side module stating an external-owned row is not stray.
    (4) A source whose header the contract GRAMMAR refuses — an empty
    `Contract IF-###:` opener, a body before its marker, a duplicate body, a
    body carrying an HTML comment — because nobody can read what it states:
    its declared rows count as unstated, and the refusal is named once per
    source rather than once per row it takes down with it.

    WHAT STAYS A WARN, on record: an owner that declares NOTHING is the
    owner-exact reverse check's finding (`_owner_exact_findings`, warn-only),
    not this gate's — the ruled rule is "a DECLARED seam with no body", and
    promoting the undeclared case would fail every fixture and adopter row
    whose owner has not yet been headed at all, which is the migration list
    rather than a defect in a stated definition. The dodge that leaves —
    never declare, never owe a body — is visible in that warn and in the
    reference's summary line, and is the owner's to promote. Vacuous where
    there is no surface (files-mode, an absent scan root), the
    `arch_inventory` posture; an unreadable source is the reference's own
    list, not a finding here."""
    if not read_interfaces_check_enabled(root):
        return []
    sites, refused = _declaration_sites(root)
    if sites is None:
        return []
    out = [
        "{!r} declares seams but its header is refused by the contract "
        "grammar: {} — its declared rows count as unstated".format(rel, msg)
        for rel, msg in refused
    ]
    ifs = load_seams(root)
    file_names = {owner for owner, _path in _owner_files(root)}

    def site_key(owner):
        return owner if owner in file_names else _norm_module(owner)

    owner_key = {}
    for r in ifs:
        if r["owner"] and not r["owner"].startswith("external:"):
            owner_key.setdefault(r["id"], site_key(r["owner"]))
    external_far = {}
    for r in ifs:
        iid, owner = r["id"], r["owner"]
        if not owner:
            continue  # trace.py's required-cell finding
        if owner.startswith("external:"):
            far = [site_key(e) for e in r["far"] if not e.startswith("external:")]
            external_far[iid] = set(far)
            out.extend(_external_body_findings(sites, iid, owner, far))
            continue
        site = sites.get(site_key(owner))
        if site is None:
            continue  # declares nothing, or unresolvable: the reverse check's warn
        rel, ids, bodies = site
        if iid in ids and iid not in bodies:
            out.append(
                "IF {} is declared by its owner {!r} but states no `Contract {}:` "
                "body there — an interface with no definition".format(iid, rel, iid)
            )
    out.extend(_stray_declaration_findings(sites, owner_key, external_far))
    return out


def _external_body_findings(sites, iid, owner, far):
    """The external arm of `contract_body_findings`: `far` is the row's far
    side as site keys (kit modules only); silent when none faces it or one
    states the body, a finding otherwise."""
    if not far or any(k in sites and iid in sites[k][2] for k in far):
        return []
    declared = [sites[k][0] for k in far if k in sites and iid in sites[k][1]]
    if declared:
        return [
            "IF {} is owned by {!r}; its far side {!r} declares it but states no "
            "`Contract {}:` body — our reading of an external surface is stated "
            "by the kit module that faces it".format(iid, owner, declared[0], iid)
        ]
    return [
        "IF {} is owned by {!r} and no far-side kit module states it — our "
        "reading of an external surface lives in the header of the module that "
        "faces it ({})".format(iid, owner, ", ".join(sorted(far)) or "none named")
    ]


def _stray_declaration_findings(sites, owner_key, external_far):
    """The stray arm of `contract_body_findings`: a source declaring an id the
    registry owns to a different in-tree source, or an external-owned id whose
    far side it is not."""
    out = []
    for key, (rel, ids, _bodies) in sorted(sites.items()):
        for iid in sorted(ids):
            if iid in external_far:
                if key not in external_far[iid]:
                    out.append(
                        "{!r} declares IF {}, an external-owned seam whose far side "
                        "it is not — our reading of an external surface is stated "
                        "by the module that faces it".format(rel, iid)
                    )
                continue
            home = owner_key.get(iid)
            if home is None or home == key or home not in sites:
                continue  # unowned (trace's finding), the owner, or unresolvable
            out.append(
                "{!r} declares IF {}, which the registry owns to {!r} — the owner is "
                "the one declaration site; a second copy is a second "
                "definition".format(rel, iid, sites[home][0])
            )
    return out


# --- seam-TC coverage promotion + its migration allowlist (OI-43 ruled (a),
# WI-488) -------------------------------------------------------------------


def _parse_if_tc_allow_full(text):
    """`(entries, seed, unparsed)` — the whole parse, both halves, the
    `docs/provenance-allow` split (`trace.read_provenance_allow`): `entries`
    and `seed` are exactly `parse_if_tc_allow`'s return (kept as a separate,
    pinned-arity wrapper below since `tests/test_trajectory_arch.py` unpacks
    it as a 2-tuple); `unparsed` is `[(lineno, line)]` for every DECLARING
    line the grammar dropped — not blank, not a `#`-comment, and whose first
    token does not parse as an `IF-###` id — so a malformed entry is reported
    rather than silently read as an empty file
    (`if_tc_allow_parse_findings`)."""
    entries = []
    seed = None
    unparsed = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            m = IF_TC_SEED_RE.match(line)
            if m and seed is None:
                seed = int(m.group(1))
            continue
        head, _, reason = line.partition(" — ")
        token = head.split()[0] if head.split() else ""
        if IF_ID_RE.fullmatch(token):
            entries.append((token, reason.strip() or None))
        else:
            unparsed.append((lineno, line))
    return entries, seed, unparsed


def parse_if_tc_allow(text):
    """`([(id, reason-or-None), ...] in file order, declared seed count or
    None)` for one allowlist file's TEXT.

    The SEED COUNT is a machine-readable header key, `# seed-count: <int>`,
    naming how many of the entries below are the migration BASELINE — the
    population measured when the promotion was seeded, which shares one reason
    stated once in the header rather than repeated per line. Entries past that
    count are ADDITIONS, and an addition is a judgment someone made, so it
    carries its own ` — <reason>`. A file that declares no seed count has no
    baseline to grow past; every entry is then read as seeded, which is what an
    adopter's freshly-seeded file looks like before it has ever grown.

    `_parse_if_tc_allow_full` is the same parse plus the malformed-line half;
    this wrapper's 2-tuple return is pinned by
    `test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set`, so it stays
    exactly as it was rather than growing a third element."""
    entries, seed, _unparsed = _parse_if_tc_allow_full(text)
    return entries, seed


def read_if_tc_allow(root):
    """`{IF-### id: reason-or-None}` from `docs/if-tc-coverage-allow` — the
    seam-TC coverage migration allowlist. Absent file: empty dict.

    Grammar, deliberately the cheap kind: one non-blank, non-`#`-comment line
    per entry, the first whitespace-run-delimited token an `IF-###` id,
    optionally followed by ` — <reason>`. FAIL-SOFT IN THE LOUD DIRECTION, the
    `docs/provenance-allow` rule: a line whose first token does not parse as an
    IF-### id declares nothing and is dropped, so the worst a malformed entry
    can do is leave the finding it was meant to silence still reported — never
    the reverse.

    AN ADDITION BEYOND THE DECLARED SEED NEEDS A REASON, and a bare one
    SUPPRESSES NOTHING — the same fail-soft-loud direction. The 2026-08-21
    review measured why: a new seam fails `--strict`, and the one-line edit that
    greened it was appending its bare id, which was lexically indistinguishable
    from the 120 seeded lines and produced no hygiene signal, no test failure
    and no reason anyone could review. The list is a burn-down; growth has to
    cost a sentence."""
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return {}
    entries, seed = parse_if_tc_allow(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    out = {}
    for i, (token, reason) in enumerate(entries):
        if seed is not None and i >= seed and not reason:
            continue
        out[token] = reason
    return out


def if_tc_allow_growth(root):
    """`([(id, reason-or-None), ...], seed)` — the entries past the declared
    seed count, and that count (None when the file declares none)."""
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return [], None
    entries, seed = parse_if_tc_allow(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    return ([] if seed is None else entries[seed:]), seed


def if_tc_coverage_findings(root):
    """The PROMOTABLE half of seam-TC coverage (OI-43 ruled (a), WI-488): an IF
    seam cited by no TC — the rung-2 seam-TC rule `interface_findings` already
    reports informationally, in full — becomes an ERROR when it is NOT on the
    migration allowlist `docs/if-tc-coverage-allow`. Returns the finding
    string(s) ([] when clean or opted out); the caller prints them WARN plain
    and promotes them to ERROR under `--strict` (DevStg-Tests+), the
    `component_findings` idiom.

    THE ALLOWLIST IS A MIGRATION DEVICE, NOT A PERMANENT EXEMPTION SURFACE. It
    was seeded at the population measured when the ruling executed (the file's
    own header carries the exact count, command and revision) — the standing
    rule that no list edit makes a check pass (session-protocol skill §2) governs every
    entry: adding one to silence a genuinely NEW uncited seam is ACCEPTING what
    it measures, not laundering it, and should carry its own reason. An
    allowlisted seam still counts in `interface_findings`' total; it simply does
    not error here. `if_tc_allow_hygiene_findings` reports — never blocks — a
    listed seam that has since gained a TC, so a shrinking list (the declared
    burn-down) stays visible rather than silently absorbed.

    Opt-out shares `interface_findings`' `[checks] interfaces_check` dial —
    same data, same switch — AND its ≤1-module arch-map vacuity: the promoted
    rule must arm on no MORE than the warn it promotes, so a `files`-mode or
    single-module adopter that never saw this warn does not suddenly see this
    error. Widening scope is a second, unruled change riding a severity one.

    DELIBERATELY UNCLAIMED — this function declares no back-link at all.
    `LLR-042` (`SR-159`) is
    `Accepted`, and its own `detail` says the connectivity layer emits its
    findings "without changing exit status" — true of `interface_findings`,
    which this function does not touch, and now FALSE of the seam-TC rule this
    function promotes. Amending an Accepted cell overrides acceptance (the
    sitting's act, the SR-006/LLR-060 precedent, WI-473); minting a fresh
    Drafted LLR under `SR-159` was considered and declined for the same reason
    that session gave first — `SR-159` is phase 1, and a Drafted child would
    drag that phase's derived stage down as a side effect of unrelated work. So
    the built behaviour is ahead of its requirement on purpose, recorded as
    owed on WI-488's own spec rather than claimed here.
    """
    if not read_interfaces_check_enabled(root):
        return []
    inventory, _declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect — vacuous, the interface_findings gate
    ifs = load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))
    if not ifs:
        return []
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    allow = read_if_tc_allow(root)
    new_uncited = [
        r["id"] for r in ifs if r["id"] not in tc_cited and r["id"] not in allow
    ]
    if not new_uncited:
        return []
    shown = ", ".join(new_uncited[:5])
    return [
        "{} IF seam(s) have no citing TC and are not on the migration allowlist "
        "({}) — cite the seam from a TC, or add a reasoned entry to the "
        "allowlist (process.md §8; OI-43/WI-488){}: {}".format(
            len(new_uncited),
            IF_TC_ALLOW,
            " — first 5" if len(new_uncited) > 5 else "",
            shown,
        )
    ]


def if_tc_allow_hygiene_findings(root):
    """`docs/if-tc-coverage-allow` hygiene (WI-488) — WARN-ONLY, never the exit
    code, not even under `--strict`: unlike a NEW uncited seam, a STALE entry is
    never a defect to fix under pressure. Two shapes:

    - a listed seam has since gained a TC citation — burn-down PROGRESS, so
      pruning the entry is housekeeping, not a fix owed to a failing build;
    - a listed id resolves to no live IF-### row (retired/renumbered).

    Kept structurally apart from `if_tc_coverage_findings` so a shrinking
    allowlist can never itself be mistaken for a new finding, and so this
    class can never gate even by an unintended promotion of that function.
    Shares that function's ≤1-module arch-map vacuity: reporting a listed
    seam as stale is meaningless while the coverage rule it tracks never arms.

    DELIBERATELY UNCLAIMED — see `if_tc_coverage_findings`' own note on why no
    back-link declaration names `LLR-042` here.
    """
    if not read_interfaces_check_enabled(root):
        return []
    allow = read_if_tc_allow(root)
    grown, seed = if_tc_allow_growth(root)
    # `grown` is consulted for the early return too: an addition the reader
    # DROPPED (no reason) leaves `allow` empty while the file still grew, and
    # that is exactly the state most worth reporting.
    if not allow and not grown:
        return []
    inventory, _declared_contracts, _imports = arch_inventory(root)
    if len(inventory) <= 1:
        return []
    ifs = load_ifs(spine_carrier.load(root / IF_CSV, "IF-ID"))
    all_ids = {r["id"] for r in ifs}
    tc_cited = set()
    for r in spine_carrier.load(root / TC_CSV, "TC-ID"):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    out = []
    unknown = sorted(i for i in allow if i not in all_ids)
    if unknown:
        shown = ", ".join(unknown[:5])
        out.append(
            "{} {} entries name no live IF-### row (retired/renumbered){}: {}".format(
                len(unknown),
                IF_TC_ALLOW,
                " — first 5" if len(unknown) > 5 else "",
                shown,
            )
        )
    if grown:
        # GROWTH IS REPORTED EVEN WHEN EVERY ADDITION IS REASONED, because the
        # list's declared direction is DOWN. A reasoned addition is legitimate
        # and still worth a sitting's attention; an unreasoned one suppresses
        # nothing (see `read_if_tc_allow`) and is named here rather than
        # vanishing silently.
        unreasoned = [i for i, reason in grown if not reason]
        out.append(
            "{} {} entr{} stand past the declared seed of {} — the list is a "
            "burn-down, so growth is a sitting's business{}: {}".format(
                len(grown),
                IF_TC_ALLOW,
                "y" if len(grown) == 1 else "ies",
                seed,
                " ({} carr{} no reason and therefore suppress nothing)".format(
                    len(unreasoned), "ies" if len(unreasoned) == 1 else "y"
                )
                if unreasoned
                else "",
                ", ".join(i for i, _ in grown[:5]),
            )
        )
    stale = sorted(i for i in allow if i in tc_cited)
    if stale:
        shown = ", ".join(stale[:5])
        out.append(
            "{} {} entries are now cited by a TC — prune them (burn-down "
            "progress, never a defect){}: {}".format(
                len(stale), IF_TC_ALLOW, " — first 5" if len(stale) > 5 else "", shown
            )
        )
    return out


def if_tc_allow_parse_findings(root):
    """PARSE HONESTY for `docs/if-tc-coverage-allow`, the
    `kernel_allow_parse_findings` idiom (WI-519): a declaring line the grammar
    cannot read is an explicit finding naming it, not a silent drop — the
    other half of "declares nothing" is that it also grants no exemption, and
    a malformed line that still reads like a live entry to a human is the
    state most worth reporting. Reported at the FIRST unparsed line with a
    count, not all of them, for the same reason `provenance_allow_parse_findings`
    does: the fix is the same edit for every one.

    Shares `if_tc_coverage_findings`' `[checks] interfaces_check` opt-out —
    deliberately NOT its ≤1-module arch-map vacuity, unlike that function and
    `if_tc_allow_hygiene_findings`: a malformed line is a fact about the FILE,
    not about whether the tree is currently large enough for the coverage
    rule to have anything to say, the same reasoning
    `kernel_allow_parse_findings` gives for riding only `components_check`
    and not the top-view bound."""
    if not read_interfaces_check_enabled(root):
        return []
    path = Path(root) / IF_TC_ALLOW
    if not path.is_file():
        return []
    _entries, _seed, unparsed = _parse_if_tc_allow_full(
        path.read_text(encoding="utf-8-sig", errors="replace")
    )
    if not unparsed:
        return []
    lineno, line = unparsed[0]
    return [
        "{}:{}: this line DECLARES a seam-TC exception and the grammar cannot "
        "read it ({} such line(s)) — `{}`. An entry's first token is an "
        "IF-### id, optionally followed by ` — <reason>`; a token that does "
        "not parse as IF-### suppresses nothing".format(
            IF_TC_ALLOW, lineno, len(unparsed), line[:80]
        )
    ]
