#!/usr/bin/env python3
"""amendment_brief.py — the AMENDMENT brief's evidence: the spine rows whose
accepted text or adjudicated links moved after they were accepted, shown
against the accepted anchor, with the identity of each row's judged text and what each verdict owes
next.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

Moved here whole and unchanged from `adjudicate_brief.py`, the composer, so
that module stays under the size ratchet. Every rule that module's docstring
states governs this arm too: no claim under judgement as a premise, no
half-filled brief, a refusal is a hold. `adjudicate_brief` routes the
`amendment` brief to `amendment_values` and composes it there; this module
neither composes nor routes.

WHAT ELSE LIVES HERE, AND WHY. The arm reads five things the first-acceptance
arm reads as well: the row's declared scope (`adjudicates`), the tier
questions' one home (`tier_questions`), the tier -> registry join
(`_REGISTRY_OF`, whose unchained tiers are this arm's) with the dial per tier
(`_loop_accepts`), and the copy stamps (`_copy_stamp_lines`). They sit here
rather than in the composer because the import runs one way: the composer
imports this module, and nothing here imports the composer (the import graph
admits no cycle, a deferred import included). `JUDGED_TEXT` is the identity
line this arm states; the composer's binding reader reads it from here.

THE ROWS A MOVED LINK NAMES (WI-1070). A row with a moved adjudicated link is
shown with its whole accepted text, and each id its moved links name is
listed once as context (`_linked_rows`), by its tier's identifying cells
(`LINKED_TIERS`), clipped at `LINKED_CLIP` and outside every identity. An
interface's stated contract is read through the architecture component's
contract harvest, imported where it is read.

Component: CMP-008
"""

from __future__ import annotations

import re
from pathlib import Path

import acceptance_record
import agent_common as ac
import baseline_snapshot
import plan_briefs
import prompts
import spine_carrier
from kitlib import sitting as ksitting
from kitlib import spine as kspine

# The TC registry, one of the tiers `_REGISTRY_OF` joins; the composer's
# evidence-gap brief reads it from here too.
TC_REGISTRY = "docs/test/test-cases.toml"


def adjudicates(row):
    """The registry row ids this adjudication's act is SCOPED to — the `;`-joined
    `Adjudicates` cell as a set; empty when the row declares none.

    The typed companion to `declared_brief`, and typed for the same reason:
    `Brief` says which judgement is asked for, this says over WHAT, and an
    assembler that re-derives its population live needs both or it re-derives a
    wider question than the mint asked (WI-572 REVIEW-A). Reading it from the
    mint's title or `## Context` prose instead is the WI-417 fold — prose
    carrying control flow — which is why it is a `wi_convert` column. Its
    tokens are `kitlib.sitting.scope_tokens`', the merge's own reading.

    Implements: SR-146, LLR-167"""
    return set(ksitting.scope_tokens(row.get("Adjudicates")))


# The amendment brief's identity line, one per row it shows: the row and the
# digest of its accepted text and adjudicated links
# (`acceptance_record.accepted_text_digest`).
JUDGED_TEXT = "JUDGED-TEXT"


# --- the tier questions, composed from one home (WI-854) ----------------------

#: The ONE home of the questions an adjudicator puts to a spine row, per tier,
#: shipped beside the prompt templates and resolved script-relatively as they
#: are, so a brief composes them in a repo with no skills installed. The
#: spine-authoring skill points here and holds no copy. Its filename is
#: declared once in `prompts.KIT_FRAGMENTS`, which the prompt catalogue
#: digests, so an edit to the home stales that catalogue (WI-882).
QUESTIONS_HOME = prompts.PROMPTS / prompts.SPINE_QUESTIONS
# The line under each section heading naming the tiers it serves; `*` is every
# tier.
_TIERS_LINE = re.compile(r"<!-- tiers: ([A-Z* ]+) -->")
ANY_TIER = "*"


def _question_sections(text):
    """`(sections, None)` — each `## ` section of the home as `(tiers, text)`,
    its tiers line dropped — or `([], heading)` naming the first section
    with no tiers line. Text before the first heading is not a section.

    Implements: SR-146, LLR-167"""
    sections = []
    for chunk in re.split(r"(?m)^(?=## )", text)[1:]:
        heading, _, rest = chunk.partition("\n")
        marker, _, body = rest.partition("\n")
        match = _TIERS_LINE.fullmatch(marker.strip())
        if match is None:
            return [], heading
        sections.append((frozenset(match.group(1).split()), heading + "\n" + body))
    return sections, None


def tier_questions(tiers):
    """`(text, None)`: the home's sections serving any of `tiers` (its
    every-tier sections included), in the home's order, or `(None, reason)`.

    NO FALLBACK. An absent or unreadable home, a section with no tiers line,
    or a judged tier no section serves refuses the brief (rule 2): a judge
    handed a brief with its questions missing reads the gap as "nothing to
    ask", and there is no second copy of them to fall back on.

    Implements: SR-146, LLR-167
    """
    path = QUESTIONS_HOME
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, "the tier questions' home {} cannot be read: {}".format(path, exc)
    sections, bad = _question_sections(prompts.strip_dispatcher_block(text))
    if bad is not None:
        return (
            None,
            "the tier questions' home {}: section {!r} declares no tiers".format(
                path, bad
            ),
        )
    served = set().union(*(declared for declared, _body in sections))
    missing = [] if ANY_TIER in served else sorted(set(tiers) - served)
    if missing or not sections:
        return None, "the tier questions' home {} declares no questions for {}".format(
            path, ", ".join(missing) or "any tier"
        )
    return "\n\n".join(
        body.rstrip()
        for declared, body in sections
        if ANY_TIER in declared or declared & set(tiers)
    ), None


# --- the amendment brief (SN-029; routed at D-9 step 4b) ----------------------


def amendment_values(root, row):
    """`({baseline, rows, aftermath}, None)` for the spine rows whose accepted
    text moved after they were accepted, or `(None, reason)`; the values also
    report the amended needs and SRs under `plan_briefs.HAT_PARENTS`, never a
    slot.

    `{baseline}` is the SNAPSHOT STAMP, and the substitution is the whole point
    of this assembler existing. The slot asks for "the accepted anchor this diff
    is measured against"; the old derivation resolved, for a row that never
    flipped, to the amendment commit ITSELF — presenting the text under
    judgement as its own accepted anchor, which is precisely the failure rule 1
    exists to prevent. `docs/archive/last_accepted/` is an anchor that is
    provably NOT the text under judgement: the mirror invariant means it can
    only have been written by copying a live registry in a reviewed acceptance
    commit.

    `{rows}` is `trace.reaccept_model`'s ACCEPTED cells and its moved
    ADJUDICATED LINKS (the routed traced cells, marked `(link)`) — the same
    model behind `trace.py --accept` and `open-items.html`, so the judge, the
    brief and the operator surface can never show three different diffs. A
    link is shown because an act naming the row records it with the row's
    accepted text: unshown, blessing the text would carry the link into the
    record unjudged (WI-1069), so a row whose only change is a link is shown
    too. Every other trace cell is deliberately excluded: §A5.1 rules them
    outside acceptance, and a judge asked to rule "meaning or clarity" on a
    moved `Phase` cell is being asked a question the ruling already answers.
    A scoped row with nothing to judge is named after the blocks, never
    dropped unnamed (`_not_shown_lines`). The need, assumption and surrogate
    tiers, which that model does not hold, are read beside it from the same
    recorded copy (`_unchained_amended_rows`; OI-100 gap 1, WI-791), so a row
    the widened mint routes is briefed rather than held. A row with a moved
    link also lists its unmoved accepted cells (`_unmoved_cells`), since the
    question a link asks is about the row's whole text.

    `{linked}` lists once each id the shown rows' moved links name, as
    context outside every identity (`_linked_rows`; WI-1070).

    NO SNAPSHOT IS A HOLD, AND IT SAYS WHY. A repo that has never signed has no
    accepted anchor at all, so "did this amendment change the meaning?" is not
    the question its rows pose — a FIRST ACCEPTANCE is. Refusing names that
    exactly, rather than fabricating an anchor (rule 1) or rendering a
    before/after with an empty before (rule 2). The stamp itself is advisory:
    off git, or before the snapshot's own commit lands, it is empty and the
    baseline line says so rather than naming a date.

    WHICH ROWS IS THE ROW'S OWN `Adjudicates` SCOPE, intersected with the
    model — `first_acceptance_values`' rule, for its reason. The model is
    REPO-WIDE: it walks every SR, so a brief built from it alone handed each
    amendment row every drifted accepted row in the tree, and each verdict had
    to count its own rows by hand and list the rest as excluded (three
    adjudications that each named one row were each handed the same twenty).
    The mint writes the rows it routes into the cell; the live model answers
    for those rows only, so a row re-anchored since the mint drops out and a
    scope with nothing left REFUSES by name. A row with NO scope refuses too:
    reading the empty cell as "everything" is the widening itself.

    THE ANCHOR IS STAMPED PER REGISTRY. A refresh copies only the registries
    its act authorises, so the copies were written at different commits, and
    the directory's newest write named one registry's copy as the provenance of
    all of them. `{baseline}` names, for each registry shown, the commit that
    last wrote ITS copy.

    `{identity}` states one `JUDGED-TEXT: <row id> <digest>` line per row the
    brief shows for judgement, the digest of that row's accepted text and
    adjudicated links as the brief's own reader loads it
    (`acceptance_record.accepted_text_digest`), so the binding records the
    text this sitting judged; a row `{linked}` lists has none.

    Implements: SR-146, SR-178, LLR-167, LLR-359
    """
    import trace as tr

    root = Path(root)
    scope = adjudicates(row)
    if not scope:
        return None, (
            "this amendment adjudication declares no `Adjudicates` scope, so the "
            "rows the merge routed to it are unknown — and an unstated boundary "
            "read as 'every drifted row in the repo' is the widening this cell "
            "exists to make unrepresentable. Re-mint the row, or rule on it by "
            "hand"
        )
    if not baseline_snapshot.exists(root):
        return None, (
            "no {} snapshot exists yet, so nothing has been accepted — every row "
            "here poses a FIRST-ACCEPTANCE question rather than a "
            "meaning-or-clarity one, and there is no accepted anchor to measure "
            "an amendment against".format(baseline_snapshot.SNAPSHOT_DIR)
        )
    reg = tr.load_registries(root / "docs")
    model = tr.reaccept_model(root, reg.srs, reg.llrs, reg.tcs)
    lines, tiers, chained, links = _amended_rows(model, scope)
    more, more_tiers, unchained = _unchained_amended_rows(root, scope)
    gone, gone_tiers, removed, unknown = _removed_amended_rows(root, scope)
    if unknown:
        why = "the scope names ({}), which neither the live registries nor their {} copy hold, so it names no row to rule on: re-mint the row"
        return None, why.format(", ".join(unknown), baseline_snapshot.SNAPSHOT_DIR)
    lines, tiers = lines + more + gone, tiers | more_tiers | gone_tiers
    shown = [rid for _kind, rid in chained] + [r[0] for r in unchained + removed]
    if not lines:
        # One refusal for every way the SCOPED population empties, naming the
        # scope: a repo-wide "nothing to judge" beside it would be two answers
        # to one question (`first_acceptance_values`' rule).
        return None, (
            "none of the {} row(s) this adjudication was minted over ({}) still "
            "carries accepted text or an adjudicated link that differs from its "
            "{} copy — re-anchored, withdrawn or renumbered since the mint, "
            "awaiting a FIRST acceptance, or moved only trace cells no "
            "adjudicator judges — so there is no amendment in its scope "
            "to rule on".format(
                len(scope), ", ".join(sorted(scope)), baseline_snapshot.SNAPSHOT_DIR
            )
        )
    questions, why = tier_questions(tiers)
    if questions is None:
        return None, why
    needs = [r[0] for r in unchained if r[2] == "SN-ID"]
    return {
        "baseline": _amendment_baseline(root, tiers),
        "rows": "\n".join(lines + _not_shown_lines(scope, shown)),
        "linked": _linked_rows(root, links, shown),
        "aftermath": _aftermath(root, tiers),
        "questions": questions,
        "identity": _identity(root, chained, unchained + removed),
        # The amended needs make this a decomposition round (`plan_briefs`);
        # the amended SRs' needs join its parents.
        plan_briefs.HAT_PARENTS: ((), needs, [r for k, r in chained if k == "SR"]),
    }, None


def _amended_rows(model, scope):
    """`(lines, tiers, shown, links)`: the before/after of each moved accepted
    cell and each moved adjudicated link of every row IN `scope` the model
    holds, the spine tiers those rows sit in, the `(tier, row id)` each block
    shows, and `[(row id, its moved links)]` for the rows with one, in block
    order, for the listing of the rows they name (`_linked_rows`).

    ONE BLOCK PER ROW, naming every chain it hangs under. The model groups by
    owning SR, so a row with two parents sits in two entries with the same
    cells; rendered per entry, a one-row scope showed its row twice and the
    verdict's `rows=N` could not be counted against the brief."""
    chains, cells_of = _scoped_chain_rows(model, scope)
    lines = []
    for (kind, rid), sids in chains.items():
        head = "- {} {} (chain of {})".format(kind, rid, ", ".join(sids))
        lines += _cell_block(head, *cells_of[(kind, rid)])
    links = [(rid, cells_of[(k, rid)][1]) for k, rid in chains if cells_of[(k, rid)][1]]
    return lines, {kind for kind, _rid in chains}, list(chains), links


def _cell_block(head, cells, links=(), unmoved=None):
    """One shown row's block: `head`, then each accepted cell's name and its
    before and after, then each moved adjudicated link the same way, its name
    marked `(link)`; an empty side is shown as `(empty)`. A row with a moved
    link then lists its `unmoved` accepted cells under `UNMOVED`, verbatim as
    judged text is, `(none)` when every one moved (WI-1070).

    Implements: SR-146, LLR-167"""
    lines = [head]
    named = list(cells) + [(name + " (link)", b, a) for name, b, a in links]
    for name, before, after in named:
        lines += ["  - " + name, "    - before: " + (before or "(empty)")]
        lines.append("    - after: " + (after or "(empty)"))
    if unmoved is not None:
        lines.append(UNMOVED)
        lines += ["    - {}: {}".format(n, t) for n, t in unmoved] or ["    - (none)"]
    return lines


# The label over a linked row's unmoved accepted cells, after its moved ones.
UNMOVED = (
    "  - Unmoved accepted cells (with the cells above, the row's whole accepted text):"
)


def _scoped_chain_rows(model, scope):
    """`(chains, cells_of)`: each row IN `scope` with a moved accepted cell or
    a moved adjudicated link to show, keyed `(tier, row id)`, mapped to the SR
    chains it hangs under and to `(accepted cells, links, unmoved cells)`. A
    row whose only moved cells are links is shown: blessing it records the
    link, so the sitting must see it (WI-1069). Other trace cells are not
    shown. Split out of `_amended_rows` so the selection and the rendering
    each stay under the complexity limit.

    Implements: SR-146, LLR-167"""
    chains, cells_of = {}, {}
    for entry in model:
        for chain_row in entry["rows"]:
            cells, links, unmoved = _judged_cells(chain_row)
            if chain_row["id"] not in scope or not (cells or links):
                continue
            key = (chain_row["kind"], chain_row["id"])
            chains.setdefault(key, []).append(entry["id"])
            cells_of[key] = (cells, links, unmoved)
    return chains, cells_of


def _judged_cells(chain_row):
    """`(accepted cells, links, unmoved)`: the moved cells of one model row a
    sitting judges, its accepted cells and its adjudicated links, each as the
    model's `(name, before, after)` triples, and, for a row with a moved link,
    its other accepted cells (`_unmoved_cells`), else None.

    Implements: SR-146, LLR-167"""
    accepted = chain_row.get("accepted") or frozenset()
    routed = chain_row.get("routed") or frozenset()
    cells = chain_row["cells"]
    moved = [c for c in cells if c[0] in accepted]
    links = [c for c in cells if c[0] in routed]
    return moved, links, (_unmoved_cells(chain_row, moved) if links else None)


def _unmoved_cells(chain_row, moved):
    """`[(name, text)]`, by name: the nonempty accepted cells of a shown row
    that did not move, as its live row reads them. With the moved cells'
    `after`, they are the row's whole accepted text, which a link is judged
    against (WI-1070): a link-only row's diff alone holds none of it. Classed
    as the judged-text identity classes them
    (`acceptance_record.spine_cell_class`), the id and `Status` left out as it
    leaves them out, so every cell listed is in the row's identity.

    Implements: SR-146, LLR-167"""
    kind, full = chain_row["kind"], chain_row.get("full") or {}
    rel, skip = _REGISTRY_OF[kind], {kind + "-ID", "Status"} | {c[0] for c in moved}
    return [
        (name, str(value))
        for name, value in sorted(full.items())
        if name not in skip
        and value
        and acceptance_record.spine_cell_class(rel, name) == "accepted"
    ]


# The line naming the scoped rows a brief does not show, after its blocks. It
# does not open with `- `, so no count of shown rows reads it.
NOT_SHOWN = "Scoped, nothing to judge (not shown; rule no line for them): {}."


def _not_shown_lines(scope, shown):
    """`[line]` naming each id of `scope` not in `shown`, after a blank line,
    or `[]`: a scoped row with nothing to judge is named, never dropped
    unnamed (WI-1069).

    Implements: SR-146, LLR-167"""
    idle = sorted(set(scope) - set(shown))
    return ["", NOT_SHOWN.format(", ".join(idle))] if idle else []


# --- the rows the moved links name (WI-1070) ----------------------------------

# The tiers an adjudicated link names, in listing order: `(id prefix, word,
# registry, id column, identifying cells)`. Measured over every routed cell
# (`record_rows.ROUTED_TRACED_CELLS`): a link names a need, a boundary
# crossing, a requirement, a design row or an interface, and no other tier.
# Each tier's cells are its title where its schema has one and the cell that
# states what the row is; an interface adds its stated contract
# (`_stated_contracts`), its `Data` cell standing in when none is stated.
LINKED_TIERS = (
    ("SN", "need", "docs/requirements/stakeholder-needs.toml", "SN-ID", ("Need",)),
    (
        "B",
        "boundary crossing",
        "docs/requirements/external.toml",
        "B-ID",
        ("Direction", "Entity", "Carries"),
    ),
    (
        "SR",
        "requirement",
        "docs/requirements/system-requirements.toml",
        "SR-ID",
        ("Title", "Requirement"),
    ),
    (
        "LLR",
        "design row",
        "docs/requirements/low-level-requirements.toml",
        "LLR-ID",
        ("Title", "Detail"),
    ),
    (
        "IF",
        "interface",
        "docs/requirements/interfaces.toml",
        "IF-ID",
        ("Channel", "Owner", "Data"),
    ),
)
# The bound on one listed cell, in characters after its whitespace collapses:
# every need, crossing, requirement, title and data cell shows whole, and 95%
# of stated contracts and 92% of design-row details (measured on this kit at
# WI-1070); a longer cell keeps its opening, where a row states what it is.
LINKED_CLIP = 2400
# The listing's one line when the shown rows move no link.
LINKED_NONE = "(no moved link in this brief names a row)"
_ID_RE = re.compile(r"^([A-Z]+)-(\d+)$")


def _linked_rows(root, links, shown):
    """`{linked}`: each id the moved `links` name, before or after, listed
    once in tier then id order, naming the shown rows, cells and sides that
    name it, with its tier's identifying cells (`_listed_row`); `LINKED_NONE`
    when no shown row moved a link. `links` is `_amended_rows`' `[(row id,
    [(cell, before, after)])]`; `shown` the ids shown for judgement.

    CONTEXT, NOT JUDGED. The question a link asks, whether the row's text
    states what the link now points at, cannot be answered from its ids; the
    named row's text answers it. It is judged at its own tier, so no listed
    row has a judged-text identity line, and each listed cell is shown on one
    line, so none of its text can read as one.

    Implements: SR-146, LLR-167"""
    named = {}
    for rid, moved in links:
        for cell, before, after in moved:
            sides = {}
            for side, value in (("before", before), ("after", after)):
                for target in kspine.refs(value):
                    sides.setdefault(target, []).append(side)
            for target, which in sides.items():
                named.setdefault(target, []).append(
                    "{} {} ({})".format(rid, cell, ", ".join(which))
                )
    if not named:
        return LINKED_NONE
    rows = _named_tier_rows(root, named, shown)
    lines = []
    for target in sorted(named, key=_listing_order):
        lines += _listed_row(target, "; ".join(named[target]), rows, shown)
    return "\n".join(lines)


def _listing_order(rid):
    """A named id's place in the listing: its tier's, then its number."""
    match = _ID_RE.match(rid)
    prefixes = [t[0] for t in LINKED_TIERS]
    if match is None or match.group(1) not in prefixes:
        return (len(prefixes), 0, rid)
    return (prefixes.index(match.group(1)), int(match.group(2)), rid)


def _tier_of(rid):
    """The `LINKED_TIERS` entry `rid`'s prefix names, or None."""
    match = _ID_RE.match(rid)
    return next((t for t in LINKED_TIERS if match and t[0] == match.group(1)), None)


def _named_tier_rows(root, named, shown):
    """`{id prefix: {row id: live row}}` for each tier a listed id that is not
    shown for judgement names, each registry loaded once (the needs file
    through its own tier loader); `EXT` the entities a crossing names, and
    `CONTRACT` the stated contracts of the named interfaces.

    Implements: SR-146, LLR-167"""
    wanted = {t[0] for t in map(_tier_of, set(named) - set(shown)) if t}
    rows = {}
    for prefix, _word, rel, id_col, _cells in LINKED_TIERS:
        if prefix in wanted:
            rows[prefix] = {r.get(id_col): r for r in _load_tier(root, rel, id_col)}
    if "B" in rows:
        ext = _load_tier(root, "docs/requirements/external.toml", "EXT-ID")
        rows["EXT"] = {r.get("EXT-ID"): r for r in ext}
    if "IF" in rows:
        rows["CONTRACT"] = _stated_contracts(root, set(named) & set(rows["IF"]))
    return rows


def _load_tier(root, rel, id_col):
    """One tier's live rows, example rows dropped: the needs file's through
    its carrier-aware tier loader, every other through the row loader."""
    path = Path(root) / rel
    if id_col == "SN-ID":
        return spine_carrier.load_need_tier(path, id_col, False)
    return spine_carrier.load(path, id_col, keep_examples=False)


def _stated_contracts(root, ids):
    """`{interface id: contract}` for each of `ids` whose `Contract IF-###:`
    body exactly one file on the declared surface states, read through the
    kit's own harvest (`arch_interfaces.contract_homes`, then that file's
    `gen_arch_map.file_contracts`). An id with no such file is absent, so its
    `Data` cell, the contract's home until code states one, stands in: no
    surface (files mode, no scan root), no body, two bodies, or a header the
    grammar refuses. Imported here, so the harvest runs only when a link names
    an interface.

    Implements: SR-146, LLR-167"""
    import arch_interfaces
    import gen_arch_map

    homes = arch_interfaces.contract_homes(Path(root)) or {}
    bodies, out = {}, {}
    for iid in sorted(i for i in ids if i in homes):
        rel = homes[iid]
        if rel not in bodies:
            try:
                bodies[rel] = gen_arch_map.file_contracts(Path(root) / rel)[1]
            except (OSError, UnicodeDecodeError, SyntaxError, ValueError):
                # ValueError covers the grammar's refusal (ContractsGrammarError).
                bodies[rel] = {}
        if bodies[rel].get(iid):
            out[iid] = bodies[rel][iid]
    return out


def _listed_row(rid, namers, rows, shown):
    """One listed id's lines: its head (the id, its tier's word and the rows
    naming it), then each identifying cell (`_listed_cells`), or the head
    alone ending `shown above for judgement` or `names no live row`.

    Implements: SR-146, LLR-167"""
    tier = _tier_of(rid)
    head = "- {} ({}), named by {}".format(rid, tier[1] if tier else "row", namers)
    if rid in shown:
        return [head + ": shown above for judgement"]
    row = (rows.get(tier[0]) or {}).get(rid) if tier else None
    if row is None:
        return [head + ": names no live row"]
    return [head] + [
        "  - {}: {}".format(name, _context_cell(text))
        for name, text in _listed_cells(tier, rid, row, rows)
    ]


def _listed_cells(tier, rid, row, rows):
    """`[(label, text)]`: a live named row's identifying cells, its tier's in
    order; a crossing's entity carries the entity's name when that row is
    live, and an interface's stated contract replaces its `Data` cell."""
    cells = [(name, str(row.get(name) or "")) for name in tier[4]]
    if tier[0] == "B":
        entity = (rows.get("EXT") or {}).get(row.get("Entity"))
        if entity and entity.get("Name"):
            cells[1] = ("Entity", "{} ({})".format(row.get("Entity"), entity["Name"]))
    contract = (rows.get("CONTRACT") or {}).get(rid)
    if tier[0] == "IF" and contract:
        cells[-1] = ("Contract", contract)
    return cells


def _context_cell(text):
    """A listed cell on ONE line, its whitespace collapsed, so no line of it
    reads as an identity or verdict line, clipped at `LINKED_CLIP` characters
    at the last space before the cap, the clip and the full length stated;
    `(empty)` for an empty cell.

    Implements: SR-146, LLR-167"""
    flat = " ".join(str(text).split())
    if len(flat) <= LINKED_CLIP:
        return flat or "(empty)"
    head = flat[:LINKED_CLIP]
    if flat[LINKED_CLIP] != " " and " " in head:
        head = head.rsplit(" ", 1)[0]
    return "{} … [clipped at {} of {} characters]".format(
        head.rstrip(), LINKED_CLIP, len(flat)
    )


# The amended tiers the requirement-chain model does not hold (OI-100 gap 1,
# WI-791): the need tier and the assumption registry's two tiers, each
# `(kind, registry, id column)`. The mint routes their amendments since WI-791,
# so the brief must render them or every such row would refuse as "nothing in
# scope" and hold for an operator.
_UNCHAINED_TIERS = (
    ("SN", "docs/requirements/stakeholder-needs.toml", "SN-ID"),
    ("DA", "docs/requirements/assumptions.toml", "DA-ID"),
    ("SUR", "docs/requirements/assumptions.toml", "SUR-ID"),
)


def _unchained_amended_rows(root, scope):
    """`(lines, tiers, shown)` for the drifted need, assumption and surrogate
    rows IN `scope`, each rendered like `_amended_rows`' blocks — the accepted
    cells' before/after against the recorded copy
    (`baseline_snapshot.tier_owing`) — and `shown`, each such row's
    `(row id, registry, id column, live row)`.

    Implements: SR-146, LLR-167"""
    snapshot = baseline_snapshot.load_all(root)
    lines, shown, rows = [], set(), []
    for kind, rel, id_col in _UNCHAINED_TIERS:
        owing = baseline_snapshot.tier_owing(root, [(rel, id_col)], snapshot)
        for rid, why, cells, row in owing:
            if rid not in scope or why != "DRIFTED":
                continue
            shown.add(kind)
            rows.append((rid, rel, id_col, row))
            lines += _cell_block("- {} {}".format(kind, rid), cells)
    return lines, shown, rows


def _removed_amended_rows(root, scope):
    """`(lines, tiers, shown, unknown)` for the scoped rows the recorded copy
    holds accepted and the live registry no longer carries, in every tier the
    amendment brief serves (`baseline_snapshot.removed_rows`): each rendered as
    a removal, its accepted cells as `before` and the removal as `after`; the
    tiers those rows sit in; each such row's `(row id, registry, id column,
    recorded row)`; and the scope's ids that neither a live registry nor the
    recorded copy holds.

    A removed row is in no live model, so neither the chain model nor
    `tier_owing` can show it; the recorded copy is the only home its accepted
    text has left. A removed row of a tier this brief does not serve drops.

    Implements: SR-146, LLR-167"""
    snapshot = baseline_snapshot.load_all(root)
    removed, unknown = baseline_snapshot.removed_rows(root, scope, snapshot)
    lines, tiers, shown = [], set(), []
    gone = "({})".format(baseline_snapshot.ROW_REMOVED)
    for rel, id_col, rid, cells, row in removed:
        kind = id_col[: -len("-ID")]
        if kind in _REGISTRY_OF:
            head = "- {} {} {}".format(kind, rid, gone)
            lines += _cell_block(head, [(n, b, gone) for n, b, _a in cells])
            tiers.add(kind)
            shown.append((rid, rel, id_col, row))
    return lines, tiers, shown, unknown


def _identity(root, chained, unchained):
    """`{identity}`: one `JUDGED-TEXT: <row id> <digest>` line per row the
    brief shows, the requirement-chain rows (`(tier, row id)`, read from the
    live registry the chain model reads) and the unchained ones (already
    loaded by `tier_owing`), each digest that row's accepted text and
    adjudicated links (`acceptance_record.accepted_text_digest`).

    Implements: SR-178, LLR-359"""
    rows, loaded = list(unchained), {}
    for kind, rid in chained:
        rel, id_col = _REGISTRY_OF[kind], kind + "-ID"
        if rel not in loaded:
            loaded[rel] = {
                r.get(id_col): r
                for r in spine_carrier.load(
                    Path(root) / rel, id_col, keep_examples=False
                )
            }
        rows.append((rid, rel, id_col, loaded[rel][rid]))
    return "\n".join(
        "{}: {} {}".format(
            JUDGED_TEXT, rid, acceptance_record.accepted_text_digest(rel, col, row)
        )
        for rid, rel, col, row in rows
    )


def _amendment_baseline(root, tiers):
    """`{baseline}`: the snapshot as the accepted anchor, with the commit that
    last wrote the copy of EACH registry the listing shows — the provenance of
    the text actually under judgement, in spine order."""
    rels = list(dict.fromkeys(r for tier, r in _REGISTRY_OF.items() if tier in tiers))
    return (
        "{} — the accepted text as an operator last blessed it, each registry's copy "
        "as last written:\n{}\nThis is the text BEFORE the change below; it is "
        "not the change under judgement, and it could only have been written by "
        "copying a live registry in an acceptance commit.".format(
            baseline_snapshot.SNAPSHOT_DIR, _copy_stamp_lines(root, rels)
        )
    )


def _copy_stamp_lines(root, rels):
    """One `  - <registry>: copied <date> (commit <rev>)` line per registry in
    `rels`, each naming the commit that last wrote THAT registry's copy — a
    refresh copies only what its act authorises, so the directory's newest
    write is one copy's provenance, not every copy's.

    Implements: SR-146, LLR-273"""
    lines = []
    for rel in rels:
        rev, date = baseline_snapshot.stamp(root, rel)
        lines.append(
            "  - {}: {}".format(
                rel,
                "copied {} (commit {})".format(date, rev)
                if rev
                else "not yet committed, so no copy stamp",
            )
        )
    return "\n".join(lines)


# The spine tier a chain row's `kind` names -> the registry it lives in. The
# ONE join this module owns: a rendered chain row carries its tier, and both
# questions asked of it downstream — "is this tier's acceptance mine or the
# operator's" (`agent_common.operator_accepts_spine`, keyed by registry stem) and
# "what `--accepts` argument does the act owe" (keyed by registry path) — are
# registry-keyed. A second, tier-keyed rung table lived here until WI-572's
# rework; it answered the same question as `agent_common.SPINE_ACCEPTANCE_RUNGS`
# and was wired into only ONE of the two briefs that needed it.
_REGISTRY_OF = {
    "SR": "docs/requirements/system-requirements.toml",
    "LLR": "docs/requirements/low-level-requirements.toml",
    "TC": TC_REGISTRY,
    # The amendment brief's unchained tiers (OI-100, WI-791). Only the
    # amendment arm ever renders these kinds; a first-acceptance chain holds
    # SR, LLR and TC rows alone.
    **{kind: rel for kind, rel, _col in _UNCHAINED_TIERS},
}


def _loop_accepts(root, kind):
    """Is a `Drafted` row of spine tier `kind` THIS session's to accept?

    The one place this module turns a rendered chain row's tier into the dial's
    answer. An unrecognised tier has no registry, so it is HELD — the same
    direction `operator_accepts_spine` fails an unmapped one."""
    registry = _REGISTRY_OF.get(kind)
    if registry is None:
        return False
    return not ac.operator_accepts_spine(
        Path(root) / "docs", spine_carrier.stem(registry)
    )


def _aftermath(root, tiers):
    """What each verdict owes NEXT, derived from the declared gate authority for
    the tiers actually shown (operator ruling 2026-09-01) and from ruled decision
    2's one home, `intake.adjudication_action`, as OI-100 amended it
    (2026-10-03, WI-791): on a released rung the session re-accepts what it
    rules CLARITY and the MEANING rows it would bless; on a held rung it
    re-accepts a CLARITY row naming its verdict, and recommends a MEANING row
    to the operator.

    THIS SLOT REPLACED A SENTENCE THAT HAD GONE FALSE. The template used to end
    "the flip, if one is owed, is the mechanical tool's act, not yours" — true
    when written, and false since OI-45 ruled (b) retired that tool
    (`intake._apply_flips` writes nothing, permanently). A MEANING verdict on a
    loop-held rung therefore ended at a brief nobody was owed, contradicting the
    loop-held doctrine itself.

    DERIVED, NOT LEFT TO THE SESSION. The dial is a repo-level declaration the
    judge would otherwise have to go read and interpret mid-verdict, which is
    the shape that produces a session confidently doing the operator's act. An
    unrecognised tier is reported as HELD, the same direction `operator_holds`
    fails."""
    import intake  # ruled decision 2's one home; deferred, a leaf read

    held, mine = [], []
    for tier in sorted(tiers):
        (mine if _loop_accepts(root, tier) else held).append(tier)
    parts = []
    if mine:
        parts.append(_RELEASED_AFTERMATH.format("/".join(mine)))
    if held:
        arms = {v: intake.adjudication_action(True, v) for v in ("CLARITY", "MEANING")}
        parts.append(
            _HELD_AFTERMATH.format(
                "/".join(held), _HELD_ARMS[arms["CLARITY"]], _HELD_ARMS[arms["MEANING"]]
            )
        )
    return "\n\n".join(parts)


# The aftermath's wording per dial arm. The ARM each verdict takes on a held
# rung is `intake.adjudication_action`'s answer, read above, never restated.
# The sitting ends at its committed verdict (WI-912, revisions 32 and 36): the
# act is a later act turn, so each arm says what the verdict must record for
# that act, never an act of its own.
_RELEASED_AFTERMATH = (
    "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared gate "
    "authority has RELEASED, so a CLARITY row is re-accepted by the later act "
    "turn, and so is a MEANING row you mark `[MEANING+BLESS]`; a row you mark "
    "plain `[MEANING]` is not re-anchored."
)
_HELD_AFTERMATH = (
    "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared gate "
    "authority still HOLDS for an operator. A CLARITY verdict on them {}. A MEANING "
    "verdict on them {}."
)
_HELD_ARMS = {
    "reaccept": "is re-accepted by the later act turn as a judgement act, "
    "naming this verdict; the act ledger records the verdict and the operator's "
    "surface lists the act for audit. The verdict is bound to the text shown "
    "here (its JUDGED-TEXT identities), so an edit to that text after this "
    "verdict refuses the act",
    "recommend": "stops at your verdict and the signature is the operator's — "
    "recommend it to the operator and do not re-anchor it",
}
