#!/usr/bin/env python3
"""amendment_brief.py — the AMENDMENT brief's evidence: the spine rows whose
approved text moved after they were approved, shown against the accepted
anchor, with the identity of each row's judged text and what each verdict owes
next.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

Moved here whole and unchanged from `adjudicate_brief.py`, the composer, so
that module stays under the size ratchet. Every rule that module's docstring
states governs this arm too: no claim under judgement as a premise, no
half-filled brief, a refusal is a hold. `adjudicate_brief` routes the
`amendment` brief to `amendment_values` and composes it there; this module
neither composes nor routes.

WHAT ELSE LIVES HERE, AND WHY. The arm reads five things the first-approval
arm reads as well: the row's declared scope (`adjudicates`), the tier
questions' one home (`tier_questions`), the tier -> registry join
(`_REGISTRY_OF`, whose unchained tiers are this arm's) with the dial per tier
(`_loop_approves`), and the copy stamps (`_copy_stamp_lines`). They sit here
rather than in the composer because the import runs one way: the composer
imports this module, and nothing here imports the composer (the import graph
admits no cycle, a deferred import included). `JUDGED_TEXT` is the identity
line this arm states; the composer's binding reader reads it from here.
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

# The TC registry, one of the tiers `_REGISTRY_OF` joins; the composer's
# red-TC brief reads it from here too.
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
# digest of its approved text (`acceptance_record.approved_text_digest`).
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
    """`({baseline, rows, aftermath}, None)` for the spine rows whose approved
    text moved after they were approved, or `(None, reason)`; the values also
    report the amended needs and SRs under `plan_briefs.HAT_PARENTS`, never a
    slot.

    `{baseline}` is the SNAPSHOT STAMP, and the substitution is the whole point
    of this assembler existing. The slot asks for "the accepted anchor this diff
    is measured against"; the old derivation resolved, for a row that never
    flipped, to the amendment commit ITSELF — presenting the text under
    judgement as its own accepted anchor, which is precisely the failure rule 1
    exists to prevent. `docs/archive/last_approved/` is an anchor that is
    provably NOT the text under judgement: the mirror invariant means it can
    only have been written by copying a live registry in a reviewed approval
    commit.

    `{rows}` is `trace.reattest_model`'s APPROVED cells — the same model behind
    `trace.py --approve` and `open-items.html`, so the judge, the brief and the
    owner surface can never show three different diffs. Traced cells are
    deliberately excluded: §A5.1 rules them non-attesting, and a judge asked to
    rule "meaning or clarity" on a re-pointed `Module` cell is being asked a
    question the ruling already answers. The need, assumption and surrogate
    tiers, which that model does not hold, are read beside it from the same
    recorded copy (`_unchained_amended_rows`; OI-100 gap 1, WI-791), so a row
    the widened mint routes is briefed rather than held.

    NO SNAPSHOT IS A HOLD, AND IT SAYS WHY. A repo that has never signed has no
    accepted anchor at all, so "did this amendment change the meaning?" is not
    the question its rows pose — a FIRST APPROVAL is. Refusing names that
    exactly, rather than fabricating an anchor (rule 1) or rendering a
    before/after with an empty before (rule 2). The stamp itself is advisory:
    off git, or before the snapshot's own commit lands, it is empty and the
    baseline line says so rather than naming a date.

    WHICH ROWS IS THE ROW'S OWN `Adjudicates` SCOPE, intersected with the
    model — `first_approval_values`' rule, for its reason. The model is
    REPO-WIDE: it walks every SR, so a brief built from it alone handed each
    amendment row every drifted approved row in the tree, and each verdict had
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
    brief shows, the digest of that row's approved text as the brief's own
    reader loads it (`acceptance_record.approved_text_digest`), so the binding
    records the text this sitting judged.

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
            "no {} snapshot exists yet, so nothing has been approved — every row "
            "here poses a FIRST-APPROVAL question rather than a "
            "meaning-or-clarity one, and there is no accepted anchor to measure "
            "an amendment against".format(baseline_snapshot.SNAPSHOT_DIR)
        )
    reg = tr.load_registries(root / "docs")
    model = tr.reattest_model(root, reg.srs, reg.llrs, reg.tcs)
    lines, tiers, chained = _amended_rows(model, scope)
    more, more_tiers, unchained = _unchained_amended_rows(root, scope)
    gone, gone_tiers, removed, unknown = _removed_amended_rows(root, scope)
    if unknown:
        why = "the scope names ({}), which neither the live registries nor their {} copy hold, so it names no row to rule on: re-mint the row"
        return None, why.format(", ".join(unknown), baseline_snapshot.SNAPSHOT_DIR)
    lines, tiers = lines + more + gone, tiers | more_tiers | gone_tiers
    if not lines:
        # One refusal for every way the SCOPED population empties, naming the
        # scope: a repo-wide "nothing to judge" beside it would be two answers
        # to one question (`first_approval_values`' rule).
        return None, (
            "none of the {} row(s) this adjudication was minted over ({}) still "
            "carries approved text that differs from its {} copy — re-anchored, "
            "withdrawn or renumbered since the mint, awaiting a FIRST approval, "
            "or moved only TRACED cells — so there is no amendment in its scope "
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
        "rows": "\n".join(lines),
        "aftermath": _aftermath(root, tiers),
        "questions": questions,
        "identity": _identity(root, chained, unchained + removed),
        # The amended needs make this a decomposition round (`plan_briefs`);
        # the amended SRs' needs join its parents.
        plan_briefs.HAT_PARENTS: ((), needs, [r for k, r in chained if k == "SR"]),
    }, None


def _amended_rows(model, scope):
    """`(lines, tiers, shown)`: the approved-cell before/after of each drifted
    row IN `scope`, the spine tiers those rows sit in, and the `(tier, row id)`
    each block shows.

    ONE BLOCK PER ROW, naming every chain it hangs under. The model groups by
    owning SR, so a row with two parents sits in two entries with the same
    cells; rendered per entry, a one-row scope showed its row twice and the
    verdict's `rows=N` could not be counted against the brief."""
    chains, cells_of = _scoped_chain_rows(model, scope)
    lines = []
    for (kind, rid), sids in chains.items():
        head = "- {} {} (chain of {})".format(kind, rid, ", ".join(sids))
        lines += _cell_block(head, cells_of[(kind, rid)])
    return lines, {kind for kind, _rid in chains}, list(chains)


def _cell_block(head, cells):
    """One shown row's block: `head`, then each approved cell's name and its
    before and after, an empty side shown as `(empty)`.

    Implements: SR-146, LLR-167"""
    lines = [head]
    for name, before, after in cells:
        lines += ["  - " + name, "    - before: " + (before or "(empty)")]
        lines.append("    - after: " + (after or "(empty)"))
    return lines


def _scoped_chain_rows(model, scope):
    """`(chains, cells_of)`: each drifted row IN `scope` with approved cells
    to show, keyed `(tier, row id)`, mapped to the SR chains it hangs under
    and to those approved cells. Split out of `_amended_rows` so the selection
    and the rendering each stay under the complexity bar."""
    chains, cells_of = {}, {}
    for entry in model:
        for chain_row in entry["rows"]:
            approved = chain_row.get("approved") or frozenset()
            cells = [c for c in chain_row["cells"] if c[0] in approved]
            if chain_row["id"] not in scope or not cells:
                continue
            key = (chain_row["kind"], chain_row["id"])
            chains.setdefault(key, []).append(entry["id"])
            cells_of[key] = cells
    return chains, cells_of


# The amended tiers the requirement-chain model does not hold (OI-100 gap 1,
# WI-791): the need tier and the assumption registry's two tiers, each
# `(kind, registry, id column)`. The mint routes their amendments since WI-791,
# so the brief must render them or every such row would refuse as "nothing in
# scope" and hold for a human.
_UNCHAINED_TIERS = (
    ("SN", "docs/requirements/stakeholder-needs.toml", "SN-ID"),
    ("DA", "docs/requirements/assumptions.toml", "DA-ID"),
    ("SUR", "docs/requirements/assumptions.toml", "SUR-ID"),
)


def _unchained_amended_rows(root, scope):
    """`(lines, tiers, shown)` for the drifted need, assumption and surrogate
    rows IN `scope`, each rendered like `_amended_rows`' blocks — the approved
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
    holds approved and the live registry no longer carries, in every tier the
    amendment brief serves (`baseline_snapshot.removed_rows`): each rendered as
    a removal, its approved cells as `before` and the removal as `after`; the
    tiers those rows sit in; each such row's `(row id, registry, id column,
    recorded row)`; and the scope's ids that neither a live registry nor the
    recorded copy holds.

    A removed row is in no live model, so neither the chain model nor
    `tier_owing` can show it; the recorded copy is the only home its approved
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
    loaded by `tier_owing`), each digest that row's approved text
    (`acceptance_record.approved_text_digest`).

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
            JUDGED_TEXT, rid, acceptance_record.approved_text_digest(rel, col, row)
        )
        for rid, rel, col, row in rows
    )


def _amendment_baseline(root, tiers):
    """`{baseline}`: the snapshot as the accepted anchor, with the commit that
    last wrote the copy of EACH registry the listing shows — the provenance of
    the text actually under judgement, in spine order."""
    rels = list(dict.fromkeys(r for tier, r in _REGISTRY_OF.items() if tier in tiers))
    return (
        "{} — the approved text as a human last blessed it, each registry's copy "
        "as last written:\n{}\nThis is the text BEFORE the change below; it is "
        "not the change under judgement, and it could only have been written by "
        "copying a live registry in an approval commit.".format(
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
# questions asked of it downstream — "is this tier's approval mine or the
# owner's" (`agent_common.human_approves_spine`, keyed by registry stem) and
# "what `--approves` argument does the act owe" (keyed by registry path) — are
# registry-keyed. A second, tier-keyed rung table lived here until WI-572's
# rework; it answered the same question as `agent_common.SPINE_APPROVAL_RUNGS`
# and was wired into only ONE of the two briefs that needed it.
_REGISTRY_OF = {
    "SR": "docs/requirements/system-requirements.toml",
    "LLR": "docs/requirements/low-level-requirements.toml",
    "TC": TC_REGISTRY,
    # The amendment brief's unchained tiers (OI-100, WI-791). Only the
    # amendment arm ever renders these kinds; a first-approval chain holds
    # SR, LLR and TC rows alone.
    **{kind: rel for kind, rel, _col in _UNCHAINED_TIERS},
}


def _loop_approves(root, kind):
    """Is a `Drafted` row of spine tier `kind` THIS session's to approve?

    The one place this module turns a rendered chain row's tier into the dial's
    answer. An unrecognised tier has no registry, so it is HELD — the same
    direction `human_approves_spine` fails an unmapped one."""
    registry = _REGISTRY_OF.get(kind)
    if registry is None:
        return False
    return not ac.human_approves_spine(
        Path(root) / "docs", spine_carrier.stem(registry)
    )


def _aftermath(root, tiers):
    """What each verdict owes NEXT, derived from the declared gate authority for
    the tiers actually shown (owner ruling 2026-09-01) and from ruled decision
    2's one home, `intake.adjudication_action`, as OI-100 amended it
    (2026-10-03, WI-791): on a released rung the session re-attests what it
    rules CLARITY and the MEANING rows it would bless; on a held rung it
    re-attests a CLARITY row naming its verdict, and recommends a MEANING row
    to the owner.

    THIS SLOT REPLACED A SENTENCE THAT HAD GONE FALSE. The template used to end
    "the flip, if one is owed, is the mechanical tool's act, not yours" — true
    when written, and false since OI-45 ruled (b) retired that tool
    (`intake._apply_flips` writes nothing, permanently). A MEANING verdict on a
    loop-held rung therefore ended at a brief nobody was owed, contradicting the
    loop-held doctrine itself.

    DERIVED, NOT LEFT TO THE SESSION. The dial is a repo-level declaration the
    judge would otherwise have to go read and interpret mid-verdict, which is
    the shape that produces a session confidently doing the owner's act. An
    unrecognised tier is reported as HELD, the same direction `human_holds`
    fails."""
    import intake  # ruled decision 2's one home; deferred, a leaf read

    held, mine = [], []
    for tier in sorted(tiers):
        (mine if _loop_approves(root, tier) else held).append(tier)
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
    "authority has RELEASED, so a CLARITY row is re-attested by the later act "
    "turn, and so is a MEANING row you mark `[MEANING+BLESS]`; a row you mark "
    "plain `[MEANING]` is not re-anchored."
)
_HELD_AFTERMATH = (
    "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared gate "
    "authority still HOLDS for a human. A CLARITY verdict on them {}. A MEANING "
    "verdict on them {}."
)
_HELD_ARMS = {
    "reattest": "is re-attested by the later act turn as a judgement act, "
    "naming this verdict; the act ledger records the verdict and the owner's "
    "surface lists the act for audit. The verdict is bound to the text shown "
    "here (its JUDGED-TEXT identities), so an edit to that text after this "
    "verdict refuses the act",
    "recommend": "stops at your verdict and the signature is the owner's — "
    "recommend it to the owner and do not re-anchor it",
}
