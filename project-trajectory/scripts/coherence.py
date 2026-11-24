"""THE COHERENCE RULES — do the loaded registry rows agree with each other?

The sibling of `census.py` (*what do the registries LACK?*) and `pending.py`
(*what does the OPERATOR hold?*), answering the third question the same engine used
to answer inline: **does every id a row cites name a row that exists, and does
every row have the children its tier requires?**

WHY THESE AND NOT trace.py's OTHER FORTY `*_findings` FUNCTIONS (the boundary,
stated because a decomposition that cannot say where its line is has not drawn
one). Everything here is a JOIN ACROSS ROWS: the rule needs two rows, or a row
and a set derived from other rows, to have an opinion at all. What stays in
`trace.py` is everything that does not —

  * per-row PROSE inspection (form, EARS, provenance, paraphrase, the AC and
    tiering advisories): one row in, findings out;
  * CARRIER sweeps (`structure_findings`, `integrity_findings`,
    `enum_integrity_findings`, `placeholder_findings`, `schema_findings`):
    these ask about the FILE and the raw pre-filter rows, and they are the half
    of the checker that knows a registry is a CSV or a TOML;
  * the report/console renderers, the acceptance + watermark machinery, and the
    CLI.

`trace.analyze` composes both halves and stays their only caller, so nothing
here is reachable except through the engine that always ran it.

THE ONE I/O EXCEPTION IS NAMED, NOT BURIED. `knowledge_pack_advisories`
resolves a `docs/knowledge/` ref to a real file, so it touches the filesystem —
the single rule in this module that does. It cannot move to the loader: the
paths come out of the rows. `analyze`'s docstring has always said "no I/O" and
this call has always been inside it; the extraction states the exception rather
than leaving a reader to find it.

Stdlib only. A PLAIN SIBLING and deliberately not a `kitlib` module: this
package must stay import-clean of the rest of `scripts/`
(`tests/test_bootstrap.py::test_bootstrap_imports_only_the_common_package`),
and while every rule here happens to import only `kitlib.spine` today, these
are the CHECKER's rules — the scaffolder has no business importing them, and
`census.py` recorded the same reasoning one slice earlier.

The row's `Implements:` tag sits on `spine_orphan_findings` below, not here: a
tag names the code that delivers a row, and the module holds more than that
row's rules.

Component: CMP-006
"""

import re
from dataclasses import dataclass

try:
    from kitlib.spine import (
        DIMENSION_STRATEGIES,
        id_number,
        interface_reach,
        is_accepted,
        is_drafted,
        is_example,
        is_founded,
        llr_exempt,
        llrs_under,
        parse_dimensions,
        phase_num,
        refs,
        sn_cited_ids,
    )
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib.spine import (
        DIMENSION_STRATEGIES,
        id_number,
        interface_reach,
        is_accepted,
        is_drafted,
        is_example,
        is_founded,
        llr_exempt,
        llrs_under,
        parse_dimensions,
        phase_num,
        refs,
        sn_cited_ids,
    )


def tc_citation_findings(tcs, spine_ids, ifs, da_ids=frozenset()):
    """Every TC citation orphan rule, as ``[(at_fault_id, finding), ...]``.

    The vocabulary is SR/LLR spine ids **plus** `IF-###` seam ids (WI-065). The
    seam-TC rule (process-options.md "Intra-repo interfaces & the architecture
    graph") asks an `Active` seam to be cited by a TC, and `check_trajectory`
    reads that citation out of **this same cell** — so rejecting `IF-###` here
    made the documented citation unsatisfiable: it passed one check and orphaned
    under the other. Ruled in favour of ONE citation cell rather than a second
    column: a TC states everything it verifies in one place, and trace already
    loads `interfaces.csv`, so the join is free.

    Two rules keep the widened vocabulary from becoming a hole: an unresolvable
    IF token is as wrong as an unknown SR, and a seam citation **supplements**
    the spine citation — a TC naming only seam ids no longer says which
    requirement it discharges.

    A TC MAY EVIDENCE ASSUMPTIONS INSTEAD (SR-197). `Assumption-Refs` names the
    domain assumptions it evidences, resolved against `da_ids`, the declared
    assumption rows; an entry naming anything else fails here, naming the TC.
    A TC is reported as verifying nothing only when BOTH cells are empty: a
    test of an assumption can stand alone where no requirement is its subject,
    and it is evidence all the same. The seam rule reads `Verifies` alone, so a
    seam cited beside an assumption still owes the requirement it discharges.

    Implements: SR-197, LLR-229"""
    if_ids = {r["IF-ID"] for r in ifs}
    out = []
    for r in tcs:
        tid = r["TC-ID"]
        verified = refs(r.get("Verifies"))
        assumed = refs(r.get("Assumption-Refs"))
        if not verified and not assumed:
            out.append((tid, f"TC {tid} verifies nothing"))
        elif verified and not spine_ids & set(verified):
            out.append(
                (
                    tid,
                    f"TC {tid} cites only seam id(s) — a seam citation "
                    "supplements the spine citation, so name the SR and/or LLR "
                    "this test verifies",
                )
            )
        for x in verified:
            if x not in spine_ids and x not in if_ids:
                out.append((tid, f"TC {tid} references unknown {x}"))
        out += [
            (
                tid,
                f"TC {tid} Assumption-Refs names {x}, which is not a declared "
                "assumption",
            )
            for x in assumed
            if x not in da_ids
        ]
    return out


def _repo_id(r):
    return r.get("REPO-ID") or r.get("MOD-ID")


def _sr_orphan_findings(srs, llr_sr_refs, tc_refs, sn_ids):
    """The SR tier's rules, as ``[(at_fault_id, finding), ...]``."""
    out = []
    for r in srs:
        sid = r["SR-ID"]
        # A Drafted SR is being drafted requirement-first (derived-gate model §3):
        # exempt from the child-completeness rules (no LLR / no TC) so it lives in
        # the live spine without orphaning. Its SN linkage and every integrity
        # rule still apply.
        draft = is_drafted(r)
        analytic = llr_exempt(r)
        if not draft and not analytic and sid not in llr_sr_refs:
            out.append(
                (
                    sid,
                    f"SR {sid} has no LLR (and VerificationMethod not in "
                    "Analysis/Inspection/Vouch)",
                )
            )
        if not draft and sid not in tc_refs:
            out.append((sid, f"SR {sid} has no test (TC)"))
        sn_parents = refs(r.get("SN-Refs"))
        # DevStg-Reqs's "every SR links >=1 SN", machine-checked — but only when the SN
        # registry actually provides real ids (a project without a needs file,
        # or one holding only -000 placeholders, has no SN tier to link yet).
        if sn_ids and not sn_parents:
            out.append((sid, f"SR {sid} links no SN (every SR needs >=1 SN-Ref)"))
        for u in sn_parents:
            if sn_ids and u not in sn_ids:
                out.append((sid, f"SR {sid} references unknown {u}"))
    return out


def _llr_orphan_findings(llrs, sr_ids, tc_refs):
    """The LLR tier's rules, as ``[(at_fault_id, finding), ...]``. Its no-test
    rule is a design row's discharge: any live case naming the row in
    `Verifies` discharges it, whatever its kind, and a Drafted row owes none.

    Implements: SR-248, LLR-408"""
    out = []
    for r in llrs:
        lid = r["LLR-ID"]
        parents = refs(r.get("SR-Refs"))
        if not parents:
            out.append((lid, f"LLR {lid} has no SR parent"))
        for p in parents:
            if p not in sr_ids:
                out.append((lid, f"LLR {lid} references unknown {p}"))
        # A Drafted LLR is exempt from the child-completeness (no TC) rule, like a
        # Drafted SR — its SR parent + id integrity still apply (derived-gate §3).
        if not is_drafted(r) and lid not in tc_refs:
            out.append((lid, f"LLR {lid} has no test (TC)"))
    return out


def _sn_orphan_findings(sn_ids, sr_sn_refs, sn_draft):
    """The need tier's one rule, as ``[(at_fault_id, finding), ...]``.

    A Drafted SN (section-as-state, §4a) is being drafted requirement-first and
    is exempt from the child-completeness rule, like a Drafted SR. The gate
    half of this rule is spine_rules's SN-coverage rung (WI-401): same
    cited set (sn_cited_ids), same Drafted exemption — this lists the ids,
    that caps the level, and neither fires twice on one fact."""
    return [
        (u, f"SN {u} has no SR")
        for u in sorted(sn_ids)
        if u not in sr_sn_refs and u not in sn_draft
    ]


def spine_orphan_findings(
    srs, llrs, tcs, ifs, sr_ids, llr_ids, sn_ids, sn_draft, da_ids=frozenset()
):
    """The child-completeness and parent-resolution rules over the four spine
    tiers: an SR with no LLR / no TC / no SN, an LLR with no SR parent / no TC,
    a TC citing an id that does not exist, and an SN nothing cites. Pure.

    Returns `(findings, at-fault ids)` — the id set is what the rendered views
    (outline / graph / HTML) flag, so they mark the same nodes the text lists.
    EVERY TIER SPEAKS THE `(at_fault_id, finding)` PAIR that
    `tc_citation_findings` already spoke, so the id is collected in ONE place
    instead of at eight append sites that each had to remember to.

    Emission ORDER — SR, LLR, TC, SN — is the report's and the console's, and
    tests compare it, so the concatenation below is load-bearing, not stylistic.

    `da_ids` is the declared assumption rows, which a TC's `Assumption-Refs`
    resolve against (`tc_citation_findings`); empty, every citation of one is
    unknown. The child-completeness rules read `Verifies` alone: evidence about
    an assumption is not a test of the requirement relying on it.

    Implements: SR-157, LLR-201
    """
    llr_sr_refs = {x for r in llrs for x in refs(r.get("SR-Refs"))}
    tc_refs = {x for r in tcs for x in refs(r.get("Verifies"))}
    pairs = (
        _sr_orphan_findings(srs, llr_sr_refs, tc_refs, sn_ids)
        + _llr_orphan_findings(llrs, sr_ids, tc_refs)
        + tc_citation_findings(tcs, sr_ids | llr_ids, ifs, da_ids)
        + _sn_orphan_findings(sn_ids, sn_cited_ids(srs), sn_draft)
    )
    return [f for _, f in pairs], {rid for rid, _ in pairs}


def budget_backlink_findings(pbs, budget_targets):
    """Performance budgets (process.md §9) sit off the spine but stay traceable:
    each row's Refs must resolve to a real SR or LLR id. A file path no longer
    resolves: the design rows' `Module` cell it was read against retired at
    WI-1023, and a budget names the requirement it bounds, never the file.
    Pure; extracted outward from `analyze` at WI-483."""
    budget_findings = []
    for r in pbs:
        pid = r["PB-ID"]
        targets = refs(r.get("Refs"))
        if not targets:
            budget_findings.append(f"PB {pid} back-links nothing (Refs is empty)")
        for x in targets:
            if x not in budget_targets:
                budget_findings.append(f"PB {pid} references unknown {x}")
    return budget_findings


def delegation_findings(mods, sr_ids):
    """Coordinator module registry (MULTI_REPO.md, the multi-repo layer) sits off the
    spine like PB, but its DelegatedSRs stay traceable *within* the coordinator
    repo: each must name a real coordinator SR (delegation is at the SR tier,
    §3.1). The cross-boundary link (a module SN's ParentRef back to this SR) points
    into another repo, so no single trace.py run validates it — that reconciliation
    is the deferred cross-repo join. An external/reused part referenced only via the
    IF-### catalog may delegate nothing, so an empty back-link is allowed here.

    Pure; extracted outward from `analyze` at WI-483."""
    module_findings = []
    for r in mods:
        mid = _repo_id(r)
        for x in refs(r.get("DelegatedSRs")):
            if x not in sr_ids:
                module_findings.append(
                    f"{mid.split('-')[0]} {mid} delegates unknown {x}"
                )
    return module_findings


def component_membership_findings(cmps, ifs, parts, assets):
    """Component registry (CMP-###, process-options.md "Component layer") sits off
    the spine like PART/ASSET, but its two structural cells stay traceable:
    PartOf (nesting — tag primitives at the finest CMP, coarser membership
    derives) and SupersededBy (lifecycle identity across a rewrite) must name
    real CMP ids. And the membership join is checked from the primitive side:
    a `Component` tag on an IF/PART/ASSET row must resolve to a real CMP row
    (the IF tier joined the sweep at WI-064 — trace.py has read the IF
    registry since WI-056, so its tags were the one unvalidated cell; a design
    row carries no tag since WI-1023, its placement derived). Named
    by TIER rather than by file: the row of record moved to `interfaces.toml`
    at WI-443, and "has read interfaces.csv since WI-056" would have been the
    kind of claim that is true only of a carrier nobody runs any more.

    Pure; extracted outward from `analyze` at WI-483."""
    cmp_ids = {r["CMP-ID"] for r in cmps}
    component_findings = []
    for r in cmps:
        cid = r["CMP-ID"]
        for col in ("PartOf", "SupersededBy"):
            for x in refs(r.get(col)):
                if x not in cmp_ids:
                    component_findings.append(f"CMP {cid} {col} references unknown {x}")
    if cmp_ids:
        for label, rows_, key in (
            ("IF", ifs, "IF-ID"),
            ("PART", parts, "PART-ID"),
            ("ASSET", assets, "ASSET-ID"),
        ):
            for r in rows_:
                for x in refs(r.get("Component")):
                    if x not in cmp_ids:
                        component_findings.append(
                            f"{label} {r[key]} Component tag references unknown {x}"
                        )
    return component_findings


def knowledge_pack_advisories(cmps, docs):
    """Knowledge-pack refs on a CMP row's `Knowledge` cell (process-options.md
    "Research track & knowledge packs"): a `docs/knowledge/<label>`-shaped ref
    names a hand-owned pack file. Resolve those to real files — a missing pack
    is a warn-only advisory, NEVER a gate finding (a pack is advisory context,
    research-knowledge.md §3a). Skill names and URLs share the cell and are not
    file-checkable, so only the `docs/knowledge/` prefix is resolved; anything
    else is left alone. Takes `docs` (not root) so a custom --docs still resolves.

    The one rule here that touches the filesystem — `is_file` on a resolved pack
    path. It is `analyze`'s single I/O-shaped rule and it was already inside the
    function whose docstring says "no I/O"; extracting it outward at WI-483
    names the exception instead of burying it (the read is existence-only, and
    the loader cannot pre-resolve it because the paths come from the rows).
    """
    knowledge_advisories = []
    kn_prefix = "docs/knowledge/"
    for r in cmps:
        cid = r["CMP-ID"]
        for ref in refs(r.get("Knowledge")):
            label = ref.replace("\\", "/")
            if not label.startswith(kn_prefix):
                continue
            label = label[len(kn_prefix) :]
            if not label:
                continue
            rel = label if label.endswith(".md") else label + ".md"
            pack_root = (docs / "knowledge").resolve()
            candidate = (pack_root / rel).resolve()
            try:
                candidate.relative_to(pack_root)
                contained = True
            except ValueError:
                contained = False
            if not contained or not candidate.is_file():
                knowledge_advisories.append(
                    f"CMP {cid} Knowledge ref '{ref}' names no pack ({kn_prefix}{rel})"
                )
    return knowledge_advisories


@dataclass(frozen=True)
class PhaseScope:
    """The delivery filter, resolved once: the requested phase labels (None when
    unfiltered) and the foundation phase every filter includes.

    The foundation (minimum) phase is never phase-deferred — it is in scope for
    every delivery filter, which is exactly what a blank Phase bought before the
    phase back-fill (the phase doctrine, process.md §4). Digit-parse (`v2`/`2` ->
    2 — the same parse spine_rules uses) so the minimum compares numerically; an
    all-blank downstream registry has no parseable phase, so the blank rule below
    still carries it. The `tag in phases` match stays literal (CLI label-agnostic).

    A RECORD WITH A METHOD, not a closure, at WI-483: `in_phase` used to be a
    nested def inside `analyze`, and ruff's C901 charges a nested def's branches
    to its enclosing function — so the filter cost `analyze` its complexity
    without being reusable or testable on its own.
    """

    phases: object = None
    foundation: object = None

    @classmethod
    def of(cls, srs, phase_arg):
        return cls(
            phases=set(refs(phase_arg)) if phase_arg else None,
            foundation=min(
                (n for n in (phase_num(s) for s in srs) if n is not None), default=None
            ),
        )

    def covers(self, r):
        """In scope when there is no filter, the SR's Phase is blank (downstream
        compat), its phase is listed, or it is the foundation (minimum) phase."""
        tag = (r.get("Phase") or "").strip()
        if self.phases is None or not tag or tag in self.phases:
            return True
        n = phase_num(r)
        return n is not None and n == self.foundation


def status_criterion_findings(srs, scope):
    """The `--require-verified` DevStg-Impl status criterion, phase-scoped.
    Returns `(findings, phase-deferred notices)`. Pure; extracted outward from
    `analyze` at WI-483 — the caller decides WHETHER the criterion runs, this
    states what it IS."""
    status_findings = []
    phase_deferred = []
    for r in srs:
        # The DevStg-Impl status rule applies to every accepted SR regardless of
        # Verification method — matching spine_rules.sr_gate, which already
        # demands is_accepted for any decomposed SR before DevStg-Impl with no
        # per-method carve-out (WI-259, review-2026-07-21 M-5: a Demonstration/
        # Analysis/Inspection SR left Implemented can never derive DevStg-Impl yet used
        # to pass this Test-only check — the two scripts disagreeing about the
        # gate is the false-pass the kit exists to prevent). A Drafted SR is
        # pre-acceptance (below DevStg-Reqs, derived-gate §3): it makes no acceptance
        # claim yet, so the rule stands down — surfaced in the draft count so
        # the exemption stays auditable. Pinned equivalent to sr_gate's
        # is_accepted-for-decomposed rule by test_rule_sync.
        if is_drafted(r):
            continue
        if not scope.covers(r):
            phase_deferred.append(
                f"SR {r['SR-ID']} (Phase={r.get('Phase', '').strip()}) — "
                "status check deferred to its own phase"
            )
            continue
        # `is_founded` JOINS THE PASS TEST AT D-9 STEP 8, mirroring
        # `spine_rules.spine_stage`'s Impl->Release discriminator: `Founded`
        # is `Accepted` PLUS a demonstration, so a row at the top rung has
        # more than cleared a rule that asks whether its text is blessed.
        # Reading `is_accepted` alone would have made arming the word FLAG
        # the rows that reached it — an arming that fails what it promotes.
        #
        # WHAT THIS LEAVES, stated because it is not obvious: under the
        # closed enum every live value now either stands the rule down
        # (`Drafted`) or passes it, so this finding is UNREACHABLE-BY-CELL
        # for a conformant repo — the `--require-verified` twin of the
        # stage-axis gap OI-30 D2 ceilinged on the bar axis. It still fires,
        # and must, for an OUT-OF-VOCABULARY value: a downstream repo
        # mid-migration whose rows read `Modified` or `Implemented` is
        # exactly the case that must not pass a DevStg-Impl gate silently.
        # The integrity floor names that cell too; two findings on one fault
        # is the right count here, because they answer different questions
        # ("this word is not in the vocabulary" vs "this row is not blessed").
        if not (is_accepted(r) or is_founded(r)):
            val = (r.get("Status") or "").strip()
            method = (r.get("VerificationMethod") or "").strip() or "(blank)"
            status_findings.append(
                f"SR {r['SR-ID']} is VerificationMethod={method} but Status="
                f"{val or '(blank)'} (DevStg-Impl requires Accepted for every accepted "
                "SR regardless of method — the magic Status values are matched "
                "case-insensitively, so this is a real mismatch, not a casing "
                "near-miss)"
            )
    return status_findings, phase_deferred


# --- THE REQUIREMENT-TO-INTERFACE RELATION (variant F's fourth row, WI-1024) ---
# A requirement or design row names the interfaces whose behaviour it states
# in its `Constrains` cell; a design row may state that behaviour's input set
# beside it (`Dimensions`, the permutation grammar) and what the interface
# does outside that set (`OutOfDomain`, one sentence). Every interface reaches
# a test case the harness runs through such a row or through a test case
# naming it, and a test case names an interface only where that differs from
# what the rows it verifies already constrain. Joins across rows, so they live
# here; `trace.analyze` decides each one's severity.

# One sentence: one line, ending in a full stop, with no sentence ending inside,
# which is a full stop, question mark or exclamation mark followed by a space
# and more text, whatever its case.
_INTERIOR_SENTENCE_END = re.compile(r"[.!?]\s+\S")


def _one_sentence(text):
    """Whether `text` reads as one sentence, the out-of-domain cell's shape."""
    return (
        "\n" not in text
        and text.endswith(".")
        and not _INTERIOR_SENTENCE_END.search(text)
    )


def _dimensions_problem(spec):
    """Why the permutation grammar refuses `spec`, or None."""
    try:
        _dims, strategy = parse_dimensions(spec)
    except ValueError as exc:
        return str(exc)
    if strategy is not None and strategy not in DIMENSION_STRATEGIES:
        return "unknown strategy: {}".format(strategy)
    return None


def _live_ifs(ifs):
    """The live interface rows by id, the `-000` example excluded."""
    return {
        iid: r
        for r in ifs
        if (iid := str(r.get("IF-ID") or "").strip()) and not is_example(iid)
    }


def constrains_findings(srs, llrs, ifs):
    """The `Constrains` cell and its two companion cells, as finding strings
    that join the strict failure set: an id naming no live interface row, on a
    requirement or a design row; a `Dimensions` cell the permutation grammar
    refuses; an `OutOfDomain` cell that is not one sentence; and either
    companion cell on a design row with no `Constrains` cell. An empty list
    never reaches here: the carrier refuses an explicit empty cell on read.

    Implements: SR-157, LLR-417, LLR-418
    """
    live = _live_ifs(ifs)
    out = []
    for col, rows in (("SR-ID", srs), ("LLR-ID", llrs)):
        for r in rows:
            out += [
                "{} Constrains names {}, which is no live interface row".format(
                    r[col], iid
                )
                for iid in refs(r.get("Constrains"))
                if iid not in live
            ]
    for r in llrs:
        out += _companion_findings(r)
    return out


def _companion_findings(r):
    """One design row's companion-cell findings: either cell on a row
    constraining nothing, a `Dimensions` cell the grammar refuses, an
    `OutOfDomain` cell that is not one sentence. `constrains_findings`'
    per-row step."""
    rid, named = r["LLR-ID"], refs(r.get("Constrains"))
    cells = {c: (r.get(c) or "").strip() for c in ("Dimensions", "OutOfDomain")}
    if not named:
        return [
            "{} carries {} but constrains no interface: the cell states a "
            "behaviour across an interface the Constrains cell names".format(rid, c)
            for c, value in cells.items()
            if value
        ]
    out = []
    problem = _dimensions_problem(cells["Dimensions"]) if cells["Dimensions"] else None
    if problem:
        out.append(
            "{} Dimensions does not parse in the permutation grammar: {}".format(
                rid, problem
            )
        )
    if cells["OutOfDomain"] and not _one_sentence(cells["OutOfDomain"]):
        out.append(
            "{} OutOfDomain is not one sentence: one line, ending in a full stop, "
            "with no sentence ending inside".format(rid)
        )
    return out


def companion_counts(llrs, ifs):
    """`(rows, counts)`: the design rows constraining an interface without a
    `Dimensions` or an `OutOfDomain` cell, sorted, and `{channel: [with both,
    without one or both]}` over every (design row, constrained interface) pair,
    keyed by that interface's channel.

    Implements: SR-157, LLR-419
    """
    live = _live_ifs(ifs)
    missing, counts = set(), {}
    for r in llrs:
        named = [i for i in refs(r.get("Constrains")) if i in live]
        both = all((r.get(c) or "").strip() for c in ("Dimensions", "OutOfDomain"))
        if named and not both:
            missing.add(r["LLR-ID"])
        for iid in named:
            channel = (live[iid].get("Channel") or "").strip() or "(none)"
            counts.setdefault(channel, [0, 0])[0 if both else 1] += 1
    return sorted(missing), counts


def companion_advisories(llrs, ifs, shown=10):
    """One warning line for the design rows that constrain an interface
    without both companion cells, counted by channel and the first `shown`
    named. Warn-first by the operator's ruling (2026-11-21): it never joins
    an exit code.

    Implements: SR-157, LLR-419
    """
    missing, counts = companion_counts(llrs, ifs)
    if not missing:
        return []
    names = ", ".join(missing[:shown]) + (
        ", +{} more".format(len(missing) - shown) if len(missing) > shown else ""
    )
    by_channel = ", ".join(
        "{} {}/{}".format(ch, n[0], n[1]) for ch, n in sorted(counts.items())
    )
    return [
        "constrains: {} design row(s) constrain an interface without both a "
        "Dimensions and an OutOfDomain cell ({}); per constrained interface's "
        "channel, with both/without: {}. Reported, never failing --strict".format(
            len(missing), names, by_channel
        )
    ]


def _runs(tc):
    """Whether the harness runs a test case: every case but an observation,
    whose `Automated` cell reads No (the kit's one observation marker)."""
    return (tc.get("Automated") or "").strip().lower() != "no"


def interface_coverage(srs, llrs, tcs, ifs):
    """`{IF id: route}` for each live interface, the route by which its reach
    (`kitlib.spine.interface_reach`) holds a test case the harness runs:
    `design row` through a design row constraining it, else `requirement`
    through a constraining requirement or the design rows under it, else
    `case` through a case naming it or verifying a row observed at it, else
    `observation` when its reach holds observation cases alone, else
    `unreached`.

    Implements: SR-157, LLR-421
    """
    runs = {
        str(t.get("TC-ID") or "").strip()
        for t in tcs
        if _runs(t) and not is_example(str(t.get("TC-ID") or ""))
    }
    by_row = {}
    for t in tcs:
        tid = str(t.get("TC-ID") or "").strip()
        for x in refs(t.get("Verifies")):
            by_row.setdefault(x, set()).add(tid)
    constrains = _constrains_by_row(srs, llrs)
    return {
        iid: _route(iid, rows, cases, constrains, by_row, runs, llrs)
        for iid, (rows, cases) in interface_reach(ifs, srs, llrs, tcs).items()
    }


def _route(iid, rows, cases, constrains, by_row, runs, llrs):
    """One interface's route (`interface_coverage`): through the cases of the
    design rows constraining it, else of the requirements constraining it and
    the design rows under them, else of its whole reach."""
    named = [r for r in rows if iid in constrains.get(r, ())]
    via_llr = {c for r in named if r.startswith("LLR-") for c in by_row.get(r, ())}
    via_sr = set()
    for r in (r for r in named if r.startswith("SR-")):
        for x in [r] + [row["LLR-ID"] for row in llrs_under([r], llrs)]:
            via_sr |= by_row.get(x, set())
    for route, reached in (
        ("design row", via_llr),
        ("requirement", via_sr),
        ("case", set(cases)),
    ):
        if reached & runs:
            return route
    return "observation" if cases else "unreached"


def _constrains_by_row(srs, llrs):
    """`{row id: {IF ids}}`: each requirement's and design row's `Constrains`."""
    out = {r["SR-ID"]: set(refs(r.get("Constrains"))) for r in srs}
    out.update({r["LLR-ID"]: set(refs(r.get("Constrains"))) for r in llrs})
    return out


COVERAGE_ROUTES = ("design row", "requirement", "case", "observation", "unreached")


def coverage_line(srs, llrs, tcs, ifs):
    """The one count line for interface coverage: how many interfaces reach a
    test case the harness runs through a constraining design row, a
    constraining requirement or a naming case alone, how many by observation
    alone, and how many not at all.

    Implements: SR-157, LLR-421
    """
    routes = interface_coverage(srs, llrs, tcs, ifs)
    count = {r: sum(1 for v in routes.values() if v == r) for r in COVERAGE_ROUTES}
    return (
        "interface coverage: {} interface(s): {} through a constraining design "
        "row, {} through a constraining requirement, {} through a naming test "
        "case, {} by observation alone, {} unreached".format(
            len(routes), *(count[r] for r in COVERAGE_ROUTES)
        )
    )


def coverage_advisories(srs, llrs, tcs, ifs):
    """The interfaces whose reach holds no test case the harness runs, each
    named: those reached by observation cases alone on their own line.
    Reported, not yet failing the strict check.

    Implements: SR-157, LLR-421
    """
    routes = interface_coverage(srs, llrs, tcs, ifs)
    out = []
    for route, what in (
        (
            "unreached",
            "reach no test case through a row constraining them or a case naming them",
        ),
        ("observation", "are reached by observation cases alone"),
    ):
        ids = sorted((i for i, v in routes.items() if v == route), key=id_number)
        if ids:
            out.append(
                "interface coverage: {} interface(s) {}: {}. Reported, not yet "
                "failing --strict".format(len(ids), what, ", ".join(ids))
            )
    return out


def repeat_findings(srs, llrs, tcs):
    """Each interface a test case's `Verifies` names that every design row and
    requirement the same case verifies already names in its `Constrains` cell:
    the name repeats them, per (case, row) pair. A case verifying no design row
    or requirement repeats nothing.

    Implements: SR-157, LLR-422
    """
    constrains = _constrains_by_row(srs, llrs)
    out = []
    for t in tcs:
        cited = refs(t.get("Verifies"))
        rows = [x for x in cited if x.startswith(("SR-", "LLR-"))]
        for iid in (x for x in cited if x.startswith("IF-")):
            if rows and all(iid in constrains.get(x, ()) for x in rows):
                out.append(
                    "{} names {}, which every row it verifies already "
                    "constrains ({}): a test case names an interface only where "
                    "it differs from its rows'".format(t["TC-ID"], iid, ", ".join(rows))
                )
    return out


def constrains_rules(srs, llrs, tcs, ifs, interfaces_check=True):
    """`(findings, advisories)`: the requirement-to-interface rules as the
    checker composes them. The cell findings fail the strict check; the
    missing companion cells, the repeated names and, unless the process
    settings turn the interface checks off, the interface coverage report
    are advisories.

    Implements: SR-157, LLR-417, LLR-418, LLR-419, LLR-421, LLR-422
    """
    advisories = companion_advisories(llrs, ifs) + [
        "repeat: {}. Reported, not yet failing --strict".format(f)
        for f in repeat_findings(srs, llrs, tcs)
    ]
    if interfaces_check:
        advisories += coverage_advisories(srs, llrs, tcs, ifs)
    return constrains_findings(srs, llrs, ifs), advisories
