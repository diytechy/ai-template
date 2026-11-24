"""THE ACCEPTANCE RECORD — what an amendment IS, and the mirror it is measured
against.

The boundary, in one sentence, because a decomposition that cannot say where its
line is has not drawn one: **everything here compares TWO GIT TREES cell by cell
to answer whether accepted text has moved away from the copy recording its
acceptance; everything left in `check_trajectory.py` asks what the registries say
TODAY.** Nothing in this module reads the working tree, and the free-name census
proves it rather than the docstring claiming it — the whole module's only
non-builtin dependencies are `spine_carrier` (which carrier a spine registry
uses) and one `git -C <root> … or None` primitive. The held-status readers,
and the held-rung rule with them, live in `held_status.py` (IF-196), which
imports this module one way.

WHAT IT OWNS. `SR-178` (text that has moved away from its acceptance record is
reported) and `SR-179` (the record can only ever be written by copying live
text), plus the staged `Hat-Refs` arm of the same amendment comparison
(`SR-161`, `LLR-202`), which is that comparison applied to one traced cell:

    the cell split      `SPINE_TRACED_CELLS` / `SPINE_ACCEPTED_CELLS`,
                        `spine_cell_class`, `traced_cells` — the §A5.1 owner
                        ruling that decides which cells arm a re-accept window
    the comparison      `_spine_rows_at`, `_spine_revs`, `split_changed_cells`,
                        `staged_spine_amendments` — the one basis an amendment
                        is measured by (`LLR-158`)
    the warns           `staged_spine_findings`, `staged_hat_refs_findings`
    the mirror          `_snapshot_survives`, `staged_snapshot_findings`,
                        `_snapshot_write_revs`, `committed_snapshot_findings` —
                        the invariant that the record is only ever written by
                        copy (`LLR-178`), in staged AND committed form

WHY IT IS A MODULE (WI-521, slice 1 — and the argument is not line count). The
requirements say so from a direction the size ratchet cannot see. `WI-508`'s two
blind derivations built a minimal module map from the requirement text alone,
neither able to see this tree, and **both** gave the acceptance record a module
of its own (team A's `A2`, team B's `M06`) while the live layout fused it into
the checker — 8 of `check_trajectory`'s 13 fused obligation pairs run through
`SR-178`/`SR-179`. Mechanically, the reach-through was already visible:
`baseline_snapshot.py` (the writer) and `intake.py` (the mint) each imported a
~5,000-line validator to get at the comparison basis and the mirror guard, which
is the same shape `WI-483` slice 1 cut when a render leaf imported a merge
coordinator for two constants.

WHY THE JUDGE IS STILL NOT THE WRITER. `LLR-178`'s accepted rationale places the
mirror invariant away from `baseline_snapshot` because "the writer must not also
be the judge of its own writes". That separation is unchanged and is the reason
this module is NOT folded into `baseline_snapshot.py`: it sits beside the writer,
not inside it, and `check_trajectory.main` remains the aggregation that joins its
findings to the failure set.

NOT `kitlib`, on the hard rule that kept `census.py` and `pending.py` out: every
module of that package must stay import-clean of the rest of `scripts/`
(`tests/test_bootstrap.py::test_bootstrap_imports_only_the_common_package`), and
this one imports the `spine_carrier` sibling by construction — resolving a
registry at a revision means asking which carrier that revision used.

`check_trajectory.py` re-exports every name below under its former spelling, so
no caller moved and its CLI behaviour is byte-identical; the `Implements:` tags
travel with the code they annotate.

Stdlib only.

Component: CMP-006

Contracts: IF-091, IF-129 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-091: the staged spine-amendment set, offered as a call.
    `staged_spine_amendments(root, base, head)` returns one record per
    accepted-text spine row amended between the two trees WITHOUT its status
    moving — `{"registry", "id", "accepted": {cell: (before, after)},
    "traced": {...}}` — and `AMENDMENT_CSVS` names the registries and id
    columns that walk covers: the requirement, design and test tiers, the need
    tier and the assumption registry's two tiers (OI-100, WI-791). Which two trees is a parameter, so the same call answers
    the index-against-HEAD question and the commit-against-commit one. It
    classifies and stops: which traced cells oblige an act is the caller's
    ruling, not this module's. A new row is not an amendment, a row whose
    status moved is a deliberate call this does not second-guess, and any
    missing git context degrades to `[]` rather than raising.
    THE SAME WALK ANSWERS THE ACCEPTANCE-ACT QUESTIONS (operator ruling 2026-09-01).
    `staged_acceptance_acts(root, base, head)` returns the rows that CROSSED into
    an acceptance claim or arrived already making one — precisely the set the
    amendment reader exempts, over the WIDER `ACCEPTANCE_ACT_CSVS` universe that
    adds the SN tier — and `staged_drafted_rows` returns the rows a lane
    added, amended, or moved into `Drafted`. `lane_acceptance_refusal(root, base, head)`
    words the refusal of a delta writing the acceptance record with no act a
    verdict could back, or None. It fails CLOSED on an unreadable
    snapshot delta, the opposite pole from its readers' silent degrade, because
    a refusal is where the conservative direction belongs. All four share
    `_spine_row_sides`, so no reader can be the only one that sees a row.
    `merge_acceptance_refusal(root, base, head, metas, *, trunk)`
    is the merge slot's one call: every lane's acts through
    `backed_act_refusal` - each backed by a recorded verdict over its own rows
    (operator ruling 6, 2026-10-07) - a record written with no act through
    `lane_acceptance_refusal`, and, when any claimed row in `metas` records a
    scope, the flips through its first-acceptance scope besides, and its
    re-acceptances — read from the act ledger entries the delta added — through
    `reaccept_scope_refusal`, which refuses by name every re-accepted row
    outside the `Adjudicates` scope of the amendment rows the lane claims. A
    held rung is the lane rule's (`held_status`, IF-196), not this call's.
    THE RECORD AS THE LANDING RULES READ IT (WI-1045). `landing_rules`
    reads the record through these, and through IF-129's two, and nothing
    else of this module: `_spine_rows_at(root, prefix, registry, id_col)`,
    a tier's live rows at a tree, `{}` where the tree lists no carrier;
    `_tier_reads(root, prefix, registry, id_col, under="")`, each carrier of
    a tier the tree lists, as `(path, rows, failure)`;
    `_snapshot_copy_rows(root, rev, registry, id_col)` -> `(rows, failure)`,
    the record's copy of that tier, `(None, None)` when the tree lists none
    and a failure naming the copy, the revision and whether it cannot be read
    or does not parse; `_reaccepted_added(root, base, head)` ->
    `(entries, failure)`, the act-ledger entries `head` adds over `base` in
    file order, or the failure naming the ledger, the revision and which;
    `_tier_of(row id)` -> `(registry, id column)` or `(None, None)`;
    `PARENT_FIRST_CSVS`, the need, requirement, design and test tiers;
    `_commit_parents(root, rev, question, first=False)` -> `(parents,
    lines)`, a commit's parents read off its object, an unreadable one a
    line; `_empty_tree(root)`, the empty tree's id, or None off git. Each
    reads git and writes nothing.
Contract IF-129: the ONE cell-comparison basis.
    `split_changed_cells(registry_path, id_col, before_row, live_row)` returns
    `{"accepted": {cell: (before, after)}, "traced": {cell: (before, after)}}`
    for a single row, excluding the id column (a join key, not content) and
    `Status` (the flip the caller is asking about) structurally, at the callee.
    Every reader of "what changed on this row" joins here, so the staged
    amendment guard and a snapshot comparison cannot disagree about which cells
    are content or which half of the remainder arms an act. The dependency runs
    one way only: nothing in this module imports the readers that call it.
    `accepted_text_digest(registry_path, id_col, row)` is the row's
    judged-text identity on the same basis: `sha256:` and 16 lowercase hex
    over the row's nonempty cells `spine_cell_class` classes accepted and its
    nonempty routed traced cells (`record_rows.routed_cells`), the id column
    and `Status` excluded, serialized as sorted JSON. So a carrier change, an
    empty cell against an absent one, a status move or a move of a traced cell
    no adjudicator judges leaves it unchanged, and any accepted cell's or
    routed link's move changes it.
WHAT LEFT, AND WHERE (WI-1045). The rules the coordinator's landing runs on
top of this comparison live in `landing_rules.py` (CMP-008, IF-308's home):
the ruling sync (WI-790), the parent-first commit judgement and the trunk
mint's settled-amendment filter and held-act arms. They read this module
through IF-091's readers and IF-129's two, and the import runs one way. What
stays here is the spine's: the two-tree comparison, the mirror rules, the
merge slot's acceptance-act refusal and the judged-text identity its readers
share.

TEXT THEN ACT (WI-806) is a separate judgement with its own module,
`text_then_act.py` (WI-892), which shares `_commit_parents`, the per-commit
rules' parent reader, kept here as its one home.
"""

import hashlib
import json
import tomllib
from pathlib import PurePosixPath

try:
    import record_rows
    import spine_carrier
    from kitlib import done_when as _kitdone
    from kitlib import git as _kitgit
    from kitlib import sitting as _kitsitting
    from kitlib import verdict as _kitverdict
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import record_rows
    import spine_carrier
    from kitlib import done_when as _kitdone
    from kitlib import git as _kitgit
    from kitlib import sitting as _kitsitting
    from kitlib import verdict as _kitverdict
    from kitlib import spine as _kitspine

# `git -C <root> <args>` stdout on success, else None (git absent, not a repo,
# no such object). Every scan below degrades to None so the whole tier is a
# silent no-op outside a git checkout. The alias — rather than a body — is the
# `check.py` idiom: `kitlib.git` is the declared one home for this pattern, and
# the `stdin` batch argument that used to make this look like a different
# function is a parameter there since WI-521 slice 1.
_git = _kitgit.git_out


# The three spine registries the first-acceptance mint (`staged_drafted_rows`),
# the test-first walk and the retired flip read, each with its id column. The
# amend-without-flip warn (WI-316) and the amendment mint read this set until
# WI-791; extending them to needs was "its own decision rather than a side
# effect", and OI-100 (ruled 2026-10-03) made it — so they read the sibling
# `AMENDMENT_CSVS` below, and this constant keeps its three tiers for the
# readers whose scope did not move. The acceptance-act readers below are a
# different question and DO cover SN — `ACCEPTANCE_ACT_CSVS`.
SPINE_CSVS = (
    ("docs/requirements/system-requirements.toml", "SR-ID"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID"),
    ("docs/test/test-cases.toml", "TC-ID"),
)

# THE ACCEPTANCE-ACT RUNG'S OWN SET: the spine three PLUS the need tier
# (WI-572 REVIEW-A round 028). SN is a SPINE tier — `spine_carrier.SPINE_TABLE`
# names it, its rows carry the same `status` vocabulary, and the DevStg-Reqs
# rung the operator-acceptance dial holds for the operator is exactly the SN half — so a
# lane flipping `SN-###` Drafted -> Accepted is the WORST case of the act the
# operator's 2026-09-01 ruling moved to the adjudicator, not an exempt one. It was
# excluded only by the older section-as-state reading recorded at
# `baseline_snapshot._claims_acceptance`, which the `status` cell retired.
#
# A SEPARATE CONSTANT rather than a widened `SPINE_CSVS` because the two
# questions have different scopes on purpose: `SPINE_CSVS` is the amendment
# warn's and the intake mint's universe (`intake.py`, `check_trajectory.py`
# re-export), and silently widening those is the side effect the comment above
# refuses. Only the refusal walk reads this one.
#
# THE ASSUMPTIONS REGISTRY'S TWO TIERS JOIN IT (SR-191, SR-192). An assumption
# or a surrogate is accepted content recorded like every other, and accepting
# one means reading the requirements that rely on it, which one lane does not
# hold: a lane's merge accepting one is refused, and the act that does accept
# one rides its own reviewed commit.
# Implements: SR-191, SR-192, LLR-220
ACCEPTANCE_ACT_CSVS = SPINE_CSVS + (
    ("docs/requirements/stakeholder-needs.toml", "SN-ID"),
    ("docs/requirements/assumptions.toml", "DA-ID"),
    ("docs/requirements/assumptions.toml", "SUR-ID"),
)

# THE OTHER SIDE OF THAT BOUNDARY, DECLARED RATHER THAN LEFT AS AN ABSENCE.
# `baseline_snapshot.SNAPSHOTTED` names eight registries whose `Status` a
# snapshot anchors; `ACCEPTANCE_ACT_CSVS` above names the five the refusal walks.
# The remaining three are OUT OF SCOPE OF THE ACCEPTANCE-ACT RUNG, and that is a
# ruling rather than an oversight: the interface, external-frame and component
# registries are OFF-SPINE, their acceptance cells are governed by OI-30 D3, and
# the 2026-09-01 ruling scopes this rung to SPINE rows — so a lane moving an
# interface, frame or component row's `status` is not performing the act
# `lane_acceptance_refusal` refuses, and widening to them is OI-30's call.
#
# WHY A CONSTANT AND NOT A COMMENT. The hazard the review named is a tier that
# joins `SNAPSHOTTED` and reaches NO acceptance reader — silently, because these
# two lists sit hundreds of lines apart in different modules. Naming the
# exclusions makes the two sets a closed statement:
# `SNAPSHOTTED == ACCEPTANCE_ACT_CSVS + OUTSIDE_THE_ACCEPTANCE_ACT`, pinned by
# `tests/test_acceptance_record.py`. A new tier therefore cannot be added
# without landing on one side or the other by a deliberate edit.
# THE AMENDMENT WALK'S UNIVERSE (OI-100 gap 1, ruled 2026-10-03; WI-791): every
# tier an acceptance act can bless. An amendment is text moving away from its
# blessing, so the tiers whose text an act blesses are exactly the tiers whose
# amendment owes a meaning-or-clarity judgement — the needs, the assumptions and
# the surrogates among them, which the walk left out until WI-616's need edits
# merged and minted nothing. An ALIAS, not a second literal, so the two sets
# cannot drift apart; a SIBLING of `SPINE_CSVS`, not a widening of it, so that
# constant's other readers keep their three tiers.
#
# THE PRE-COMMIT WARN'S SCOPE IS THIS SET TOO, decided in the same change: the
# warn (`staged_spine_findings`) and the mint (`intake._routed_amendments`) read
# one walk, `staged_spine_amendments`, so the author is warned at the commit
# about exactly the rows the merge will route to an adjudicator. The mint then
# drops the rows the merged range re-accepted and left equal to their snapshot
# copies (`landing_rules.settled_amendments`, LLR-364); the warn reads the
# unfiltered walk, because it fires before any act. The hat arm stays
# structurally silent on these tiers: none carries `Hat-Refs`.
# Implements: SR-178, LLR-158
AMENDMENT_CSVS = ACCEPTANCE_ACT_CSVS

OUTSIDE_THE_ACCEPTANCE_ACT = (
    "docs/requirements/interfaces.toml",
    "docs/requirements/external.toml",
    "docs/requirements/components.toml",
)

# --- the spine carrier -------------------------------------------------------
# The vocabulary and both readers live in `spine_carrier.py`, imported as a
# sibling — see that module's docstring for why it is ONE home and how that
# amends the F5 ruling.
SPINE_TABLE = spine_carrier.SPINE_TABLE
SPINE_COLUMN = spine_carrier.SPINE_COLUMN
_spine_stem = spine_carrier.stem
_spine_carriers = spine_carrier.carriers
# A TIER's carrier set and its text reader are `spine_carrier`'s, never listed
# here: the needs file's tiers sit under the need carriers (its legacy `.md`
# included), every other tier under the row carriers (WI-841 round 6).
_tier_carriers = spine_carrier.tier_carriers


def _spine_rows_at(root, rev_prefix, rel_path, id_col):
    """{id: row} of a spine registry on ONE side of the two-tree scan, read
    through whichever carrier that side actually uses (`spine_carrier`'s tier
    carriers, in preference order). `rev_prefix` is a `git show` prefix: `"HEAD:"`,
    `"abc123:"`, or `":"` for the index.

    Each side resolves independently, and that is the point rather than a
    convenience: across the cutover commit the old side is CSV and the new side
    is TOML, so this scan compares the two carriers CELL FOR CELL and reports
    any row whose accepted text did not survive. The carrier change is then not
    exempt from the amendment guard — it is checked by it, independently of the
    converter's own round-trip proof. A silent-no-op degrade (`{}`) is kept for
    a side that has neither carrier, which is the pre-registry history case;
    a carrier that cannot be read or does not parse is skipped for the next
    (`_snapshot_copy_rows` is the reader that refuses one)."""
    for _path, rows, _failure in _tier_reads(root, rev_prefix, rel_path, id_col):
        if rows is not None:
            return {r: row for r, row in rows.items() if not str(r).endswith("-000")}
    return {}


def _tier_reads(root, prefix, rel_path, id_col, under=""):
    """Each carrier of one tier the tree at `prefix` lists, in preference
    order, as `(path, rows, failure)`: `rows` its `{id: row}`, or None with
    `failure` "cannot be read" (listed, but its blob cannot be read) or "does
    not parse". `under` is prefixed to each carrier path (the snapshot's
    copies). The one carrier loop: `_spine_rows_at` skips a failed carrier,
    `_snapshot_copy_rows` refuses on it.

    Implements: SR-246, LLR-358"""
    for cand in _tier_carriers(rel_path, id_col):
        path = under + cand
        try:
            text = _kitgit.git_show(root, prefix, path)
        except _kitgit.UnreadableBlob:
            yield path, None, "cannot be read"
            continue
        if text is None:
            continue
        suffix = "." + cand.rsplit(".", 1)[1]
        rows = spine_carrier.tier_rows_from_text(text, id_col, suffix)
        yield path, rows, None if rows is not None else "does not parse"


# The §A5.1 cell split (OPERATOR RULING 2026-07-31, docs/concurrency-v2.md; WI-380).
# Only what is ACCEPTED arms the re-accept warn. Traceability is TRACED, not
# accepted: re-pointing an LLR at the module the code moved to amends no
# accepted prose. WI-280 paid for the conflation — 19 `Module` cells followed
# moved code -> 11 owning SRs flipped off `Accepted` -> the gate dropped DevStg-Impl->DevStg-Tests -> an
# acceptance brief and four review rounds, for a change that altered no requirement.
#
# BOTH halves are declared per registry, and the RESIDUAL RULE FAILS SAFE: a
# column in neither set is treated as ACCEPTED. A column added to a registry
# after this table was written can therefore only ever be too loud — a spurious
# window someone sees and dismisses — never silently un-accepted, which would
# be a MISSED window nobody sees. `tests/test_trajectory_staged.py` pins both
# halves of that: the unknown-column behaviour, and that every column of the
# live and shipped-template headers is classified here (so a new column cannot
# ride in on the residual unnoticed).
#
# `Boundary-Refs` (SR) joins the TRACED half at WI-442, on `SN-Refs`' own argument
# rather than a new one: it is the same SHAPE of pointer — which declared
# boundary crossing does this requirement state an observable at — it carries no
# prose either side, and whether a re-point moved SCOPE is exactly the judgement
# the adjudication kind exists to make. So a changed `Boundary-Refs` ROUTES to
# adjudication (intake.ROUTED_TRACED_CELLS) beside `SN-Refs`; it never arms a
# re-accept window directly. Classifying it accepted instead would arm a window
# on every row of the re-tier campaign, which is the noise that gets a window
# ignored — and the campaign's re-statements touch `Requirement` anyway, which
# IS accepted, so nothing escapes acceptance by this choice.
#
# `Hat-Refs` (SR and LLR) joins the TRACED half at WI-484, and the classification
# is the load-bearing half of shipping the cell rather than a footnote. Three
# reasons, in the order that decides it: (1) it is the same SHAPE of pointer as
# `SN-Refs`/`Boundary-Refs` — which declared row in another registry bears on this
# one — carrying no prose either side; (2) the residual would classify it ACCEPTED,
# so the phase-2 backfill would arm a re-accept window on every row it touched,
# which is precisely the 148-row noise `Boundary-Refs` was classified out of; and
# (3) the operator's own sequencing note prices this ruling — the cell "is NOT
# anticipated to be an accepted cell, so it can be tacked on AFTER the sitting
# without re-opening anything signed", which is only true if it is classified here.
# It is deliberately NOT in `intake.ROUTED_TRACED_CELLS`: re-pointing `SN-Refs`
# may have moved SCOPE, which is a judgement adjudication exists to make, while a
# hat re-point restates which lens the row is attributable to and moves no
# obligation. If phase 5's amend-without-flip arm ever wants that routing, it is
# one line — added on evidence, not in advance.
#
# `Constrains` (SR and LLR) joins the TRACED half at WI-1024, on `SR-Refs`' own
# argument: it names the interface whose behaviour the row states, a pointer
# into another registry carrying no prose. A changed one ROUTES to
# adjudication (intake.ROUTED_TRACED_CELLS), because whether the row's text
# states the behaviour across the interface it now names is the sitting's
# judgement. A design row's `Dimensions` and `OutOfDomain` are statements the
# row makes, the behaviour's input set and what the interface does outside it,
# so they join the ACCEPTED half, as the SR tier's `Permutations` did.
#
# THE ASSUMPTION TIER'S POINTERS JOIN IT (LLR-225), on the same argument: a
# requirement's `DA-Refs` and a test case's `Assumption-Refs` name rows in
# another registry, and a need's `Stakeholder-Refs` and `Source` name the
# stakeholders it serves and the document it was drawn from. Each re-points
# without moving anything the row asserts.
# Implements: SR-189, SR-190, SR-193, SR-197, LLR-225, LLR-420
SPINE_TRACED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset(
        {
            "SN-Refs",
            "Boundary-Refs",
            "Hat-Refs",
            "Phase",
            "Aspect",
            "Lifecycle",
            "DA-Refs",
            "Constrains",
        }
    ),
    # `SR-Refs` is here BY RULING (WI-388, closing WI-380 REVIEW-A finding 3 —
    # the cell §A5.1 left unclassified): it is the same shape of pointer as
    # the ruled-traced `SN-Refs`/`Verifies` — which SR owns this decomposition
    # row — and re-pointing it changes no accepted prose on either side.
    # Whether the re-point moved scope is exactly the judgement the
    # adjudication kind exists to make, so a changed `SR-Refs` ROUTES to
    # adjudication (intake.ROUTED_TRACED_CELLS) like its two siblings; it
    # never arms a re-accept window directly.
    # `Module`, `CodeSymbol` and `Component` left the design tier's schema at
    # WI-1023 and STAY CLASSED TRACED: the approval snapshot and every revision
    # before the removal still carry them, and a column this table does not
    # name reads as accepted, so dropping the names would turn the removal, a
    # traced change ("trace cells removed, requirement text unchanged"), into
    # an accepted-text amendment of every accepted design row.
    "docs/requirements/low-level-requirements.toml": frozenset(
        {
            "Module",
            "CodeSymbol",
            "TestRefs",
            "Component",
            "Phase",
            "SR-Refs",
            "Hat-Refs",
            "Constrains",
        }
    ),
    "docs/test/test-cases.toml": frozenset(
        {"Verifies", "Evidence", "Automated", "Phase", "Assumption-Refs"}
    ),
    "docs/requirements/stakeholder-needs.toml": frozenset(
        {"Stakeholder-Refs", "Source"}
    ),
}
# The accepted half. (The SR tier's `SupersededBy` column — accepted by ruling
# at WI-388 — retired with the supersession tombstone class, D-4 ruling
# 2026-08-14b; the CMP registry's own SupersededBy is a separate, still-owed
# item.) The assumption tier's STATEMENTS join it by name rather than by the
# residual (LLR-225): a requirement's `Coincident` waiver and `Form`, and a test
# case's declared `Inputs`, `MaxAge`, `Sampling`, `SampleSize` and
# `AcceptanceRule`, each a claim the row makes. `Delivered-With` joins the
# accepted half under LLR-222: changing which siblings jointly deliver the need
# changes the requirement's own argument, rather than merely re-pointing trace.
# An observation case's cadence cells `Trigger`, `Rubric` and `MinWorkItems`
# join by name too (WI-784), keeping the residual's reading: like `MaxAge` and
# `Inputs`, each states how the row's claim is judged or kept current.
# Implements: SR-193, SR-194, SR-198, LLR-222, LLR-225, LLR-420
SPINE_ACCEPTED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset(
        {
            "Title",
            "Requirement",
            "Rationale",
            "AcceptanceCriteria",
            "Permutations",
            "Priority",
            "VerificationMethod",
            "Delivered-With",
            "Coincident",
            "Form",
        }
    ),
    # `Parent` (WI-1027) joins by name: which row a child decomposes is what
    # its detail is read against, so a re-parent is an amendment of the row
    # (decisions record maint-wi-1027 D-001).
    "docs/requirements/low-level-requirements.toml": frozenset(
        {"Title", "Detail", "Rationale", "Parent", "Dimensions", "OutOfDomain"}
    ),
    "docs/test/test-cases.toml": frozenset(
        {
            "Method",
            "Expected",
            "Parameters",
            "Level",
            "Tier",
            "Inputs",
            "MaxAge",
            "Sampling",
            "SampleSize",
            "AcceptanceRule",
            "Trigger",
            "Rubric",
            "MinWorkItems",
        }
    ),
}

# THE OFF-SPINE REGISTRIES' TRACED HALF (LLR-225). Until this table no
# off-spine registry declared one, so every off-spine cell counted as accepted
# through the residual. Two cells are pointers: an interface's `BridgedBy`
# names the assumptions bridging it, and an assumption's `ObstacleHats` names
# the perspectives its obstacle came from. Every other off-spine cell stays
# accepted content (an interface's `Coincident`, a stakeholder's name,
# description and party, a crossing's `System`, an entity's `Mediates`, and the
# rest of the assumption and surrogate cells), because each states something
# the row asserts rather than pointing at another row.
# Implements: SR-211, SR-214, LLR-225
OFFSPINE_TRACED_CELLS = {
    "docs/requirements/interfaces.toml": frozenset({"BridgedBy"}),
    "docs/requirements/assumptions.toml": frozenset({"ObstacleHats"}),
}


def spine_cell_class(csv_path, column):
    """`"traced"` for a column §A5.1 rules traceability, else `"accepted"`.

    The residual is deliberate and fails SAFE: an unclassified column — one
    added to a registry after the ruling — reads as accepted and keeps arming
    the warn. See SPINE_TRACED_CELLS.

    KEYED BY THE REGISTRY, NOT BY ITS FILENAME. The two tables above are keyed
    on paths that carry a carrier SUFFIX, and the callers do not agree on which
    one: a staged-diff scan names whichever file git reported, while a live read
    names the constant. Under the CSV carrier a `.toml`-keyed lookup misses, and
    a miss here does not fail — every column reads `accepted`, so a traced-only
    edit arms a re-accept window that was ruled not to. `stem` drops the suffix,
    which is what `spine_carrier` exists to make possible.

    Implements: SR-178, LLR-158
    """
    return "traced" if column in traced_cells(csv_path) else "accepted"


def traced_cells(csv_path):
    """The §A5.1 traced column set declared for this registry, carrier-suffix
    insensitive — `frozenset()` for a registry that declares none.

    Extracted from `spine_cell_class` (its own body, unchanged) because a second
    caller needs the SET rather than one column's class: the Hat-Refs arm below
    asks whether this TIER carries the column at all, which a per-column class
    cannot answer (an absent column classes `accepted`, the fail-safe residual,
    and would make every TC amendment warn about a cell that tier does not
    have)."""
    key = spine_carrier.stem(csv_path)
    tables = SPINE_TRACED_CELLS | OFFSPINE_TRACED_CELLS
    traced = {spine_carrier.stem(k): v for k, v in tables.items()}
    return traced.get(key, frozenset())


# --- the §A5.1 cell comparison ------------------------------------------------
# WHAT WAS HERE AND WHY IT IS GONE (operator directive 2026-08-15). SN-029's digest
# engine — `normative_text`, `sn_normative_text`, `digest`, `current_digests` and
# their two exclusion sets — lived here for ~107 lines, reserved for an on-row
# `TextHash`/`HashedOn` writer (repo-lock D-1's anchor half) that was never
# built. That half is RULED unnecessary complexity: an acceptance now records what
# it blessed by COPYING the registries to `docs/archive/last_accepted/`
# (`baseline_snapshot.py`), and a copy needs no canonical text to hash, no
# separator that cannot occur in a cell, and no second exclusion list.
#
# `split_changed_cells` below is what survived, and it is the better half: it
# answered the same question the digest did — which cells moved, accepted or
# traced — while also returning the before/after pairs a brief has to render
# anyway. It is PUBLIC because `baseline_snapshot.is_drifted` reads it as the
# drift basis, so the snapshot comparison and the amend-without-flip warn can
# never disagree about what "normative" means.
#
# A ROW-TEXT IDENTITY CAME BACK, AND IT ANSWERS THAT DIRECTIVE POINT BY POINT
# (`accepted_text_digest`). A verdict about one accepted text authorizes no
# later text, so a held re-acceptance must name the text its verdict judged;
# a copy is written at the act, after the sitting, so it cannot witness what
# the sitting saw. The identity is not an on-row cell: it lives in the
# verdict's binding. It needs no separator, because JSON escapes every cell.
# And it keeps no exclusion list of its own: it hashes exactly the cells
# `spine_cell_class` classes accepted, the classes this comparison uses, and
# the routed traced cells the record already holds to the same standard
# (`record_rows.routed_cells`; WI-1069).

# The Status values whose ROW TEXT is accepted — the population the
# amend-without-flip guard scans. ONE MEMBER SINCE D-9 STEP 5, and it is a
# CONTRACTION OF SPELLING, NOT OF SCOPE: the set used to hold `verified` and
# `planned` because the pair split one rung ("text blessed, evidence
# established" vs "text blessed, evidence pending"), and OI-30 D1 folded them
# into the single `Accepted`. `Drafted` does not belong: nothing has been
# blessed, so there is nothing to amend behind an operator's back. `Founded`
# does not either, and its exclusion is DELIBERATE rather than pending: the rung
# is COMPUTED from a row's children existing, so a cell reading it is not a
# second acceptance of the row's own text — the `Accepted` claim underneath it
# is the one this guard watches. Lowercase, matching the guard's own
# normalisation.
# (`Modified` used to be listed here as excluded-because-the-marker-is-already-set;
# it retired at D-9 step 7 and the exclusion retired with it.)
# Implements: SR-178, LLR-158
_ACCEPTED_TEXT = frozenset({"accepted"})


def split_changed_cells(csv_path, id_col, head, row):
    """One row's changed cells, split into the §A5.1 halves with their
    before/after: `{"accepted": {cell: (before, after)}, "traced": {...}}`.
    The id column and `Status` are not content (the id is the join key; Status
    is the flip the caller is asking about), so neither is compared.

    Implements: SR-178, LLR-158
    """
    changed = {"accepted": {}, "traced": {}}
    for key in set(head) | set(row):
        if key in (id_col, "Status"):
            continue
        before, after = (head.get(key) or ""), (row.get(key) or "")
        if before != after:
            changed[spine_cell_class(csv_path, key)][key] = (before, after)
    return changed


def accepted_text_digest(csv_path, id_col, row):
    """The identity of the text a sitting judges on one row: `sha256:` and
    the first 16 lowercase hex of SHA-256 over its nonempty accepted cells and
    its nonempty adjudicated links (`record_rows.routed_cells`), the id column
    and `Status` excluded, serialized as sorted JSON. The cells are classed by
    `spine_cell_class`, as `split_changed_cells` classes them, so the identity
    a verdict binds and the drift that comparison reports read one split; an
    empty cell is dropped, as that comparison reads it like an absent one.

    THE LINKS ARE IN IT (WI-1069): an act naming the row records them with its
    accepted text, so a link moved after the verdict is text the verdict never
    judged, and every reader of a binding (the held act, the held-claim
    exception, the held-MEANING mint) reads it as moved text. A trace cell no
    adjudicator judges is not in it. A row carrying no link digests as it did
    before, so a binding written before the links joined still binds it; a row
    carrying one reads as moved under such a binding, and fails closed.

    Implements: SR-178, LLR-359
    """
    routed = record_rows.routed_cells(csv_path)
    cells = {
        str(key): value
        for key, value in row.items()
        if key not in (id_col, "Status")
        and value
        and (key in routed or spine_cell_class(csv_path, key) == "accepted")
    }
    text = json.dumps(cells, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    hexed = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return "sha256:" + hexed[: _kitdone._DIGEST_CHARS]


def _spine_revs(root, base, head, touches=()):
    """`(changed-paths, old-prefix, new-prefix)` for the two trees the spine scan
    compares, or None when git cannot answer (the silent-no-op degrade).

    The prefixes are `git show` arguments: `"HEAD:"`, `"abc123:"`, or `":"` for
    the INDEX. `head=None` means the index — the `--staged` hook case, and the
    default. Any other value is a commit-ish, which is what §A5.2's trigger
    needs: adjudication is minted from *a trunk commit that changed an accepted
    cell*, and a commit is not the index.

    `touches` is the caller's applicability test — the registry paths at least
    one of which must appear in the changed set for the scan to have anything to
    say. It lives HERE rather than at each call site because "git could not
    answer" and "git answered, and nothing relevant moved" produce the identical
    `return []` degrade in every consumer, and writing that pair twice is the
    intra-file duplication WI-347 rules a defect."""
    # `--no-renames` so a MOVED registry shows up as its old path too. With
    # rename detection on, `git diff --name-only` reports only the destination,
    # so `git mv docs/test/test-cases.csv elsewhere.csv` was invisible to every
    # `touches` test here. (The append-only ledger guard was the rung that found
    # this; the rule outlives it — D-1 retired the ledger, not the hazard.)
    if head is None:
        names = _git(root, ["diff", "--cached", "--name-only", "--no-renames", base])
        new_prefix = ":"
    else:
        names = _git(root, ["diff", "--name-only", "--no-renames", base, head])
        new_prefix = head + ":"
    if names is None:
        return None
    changed = set(names.splitlines())
    if touches and not any(p in changed for p in touches):
        return None
    return changed, base + ":", new_prefix


def _spine_row_sides(root, base, head, registries=SPINE_CSVS):
    """`(registry, id_col, before_rows, after_rows)` per spine registry the two
    trees actually differ in — THE ONE two-tree spine walk, shared by every
    reader below it.

    `registries` is the walk's UNIVERSE and defaults to `SPINE_CSVS`; the
    acceptance-act reader passes `ACCEPTANCE_ACT_CSVS`, which adds the SN tier. The
    parameter exists so the two scopes are one walk with one set of carrier and
    `--no-renames` rules rather than two walks that could drift.

    Extracted at WI-572 rather than copied: that row's lane refusal and its
    first-acceptance trigger ask two more questions of the SAME diff
    `staged_spine_amendments` already reads (which rows FLIPPED, which arrived
    `Drafted`), and a second walk would be a second place for the
    `--no-renames`/carrier-resolution/`-000` rules to drift out of agreement.
    Yields nothing when git cannot answer or nothing relevant moved — the
    silent-no-op degrade `_spine_revs` owns."""
    revs = _spine_revs(
        root,
        base,
        head,
        touches=sorted(c for p, col in registries for c in _tier_carriers(p, col)),
    )
    if revs is None:
        return
    staged_names, old_rev, new_rev = revs
    for csv_path, id_col in registries:
        # The record names the carrier file that ACTUALLY changed, not the
        # constant: the constant carries a suffix, and reporting
        # `system-requirements.toml` for a repo whose staged diff touched
        # `system-requirements.csv` names a file that does not exist — in a
        # record an adjudication row quotes back to an operator.
        touched = [c for c in _tier_carriers(csv_path, id_col) if c in staged_names]
        if not touched:
            continue
        before_rows = _spine_rows_at(root, old_rev, csv_path, id_col)
        after_rows = _spine_rows_at(root, new_rev, csv_path, id_col)
        yield touched[0], id_col, before_rows, after_rows, csv_path


# Whether a spine row's `Status` claims acceptance or above: the PAIR (`Accepted`
# and the computed `Founded` above it), so the acceptance-act readers below ask
# one question instead of each restating which rungs count as blessed. Its one
# home is `kitlib.spine.claims_acceptance`, which the parent-first rule reads
# too, so the rule and these readers agree on what counts as accepted. Note
# the deliberate difference from `_ACCEPTED_TEXT`, three hundred lines up: that
# set is the amend-without-flip guard's, and excludes `Founded` because a
# computed rung is not a second acceptance of the row's own text. Here the
# question is "does this cell CLAIM acceptance", and `Founded` does.
_claims_acceptance = _kitspine.claims_acceptance


def _acceptance_act(registry, rid, before, row):
    """The acceptance act ONE row performs across the two sides, or None.

    The per-row half of `staged_acceptance_acts` below, extracted so the walk
    around it is "visit every row of every changed registry" and the judgement
    is stated once, in one place, for both shapes. The two arms answer the same
    question from two directions — text that was never blessed is now blessed —
    and reading them side by side is how the mirror in that docstring stays
    checkable.

    An id-less row is not a row (the `-000` template placeholder and a blank
    key both land here); a de-acceptance and an unchanged status both fall
    through to None, which is the subtraction that docstring states."""
    if not rid:
        return None
    if before is None:
        # A row absent on the base side. `before_rows` is `{}` for a newly
        # ADDED registry too, which is why the born arm still answers there: a
        # registry that arrives with accepted rows in it is the same
        # unblessed-text-now-blessed event.
        if not _claims_acceptance(row):
            return None
        act, was = "born", ""
    elif not _claims_acceptance(before) and _claims_acceptance(row):
        act, was = "flip", (before.get("Status") or "").strip()
    else:
        return None
    return {
        "registry": registry,
        "id": rid,
        "act": act,
        "before": was,
        "after": (row.get("Status") or "").strip(),
    }


def staged_acceptance_acts(root, base="HEAD", head=None):
    """Every ACCEPTANCE ACT a spine delta performs between two trees:

        [{"registry": <carrier path>, "id": <row id>, "act": "flip" | "born",
          "before": <status>, "after": <status>}]

    An act is a row crossing INTO an acceptance claim (`act = "flip"` — `Drafted`
    → `Accepted`/`Founded`) or a row that ARRIVES already claiming one
    (`act = "born"`, absent on the base side). Both are the same event seen from
    two directions: text that was never blessed is now blessed, and the
    `docs/archive/last_accepted/` copy that anchors it is owed.

    THE READING IS THE MIRROR OF `staged_spine_amendments`, deliberately: that
    one reports rows whose accepted text moved while Status stood still and
    EXEMPTS a moved Status ("a deliberate call this does not second-guess"); this
    one reports THE EXEMPTED SET MINUS THE DE-ACCEPTANCES. The two share
    `_spine_row_sides` so they cannot disagree about which rows exist, and the
    subtraction is stated rather than left to the reader because a mirror
    claiming to be exact and then carving out a case is two sentences that
    disagree.

    A DE-ACCEPTANCE IS NOT AN ACT, and that is the subtraction. `Accepted` →
    `Drafted` withdraws a claim; it blesses nothing, so it owes no snapshot and
    refuses no merge. It is not dropped on the floor either — `staged_drafted_rows`
    reports it as an amended `Drafted` row, so the first-acceptance mint raises the
    re-acceptance it now owes. Same direction as
    `baseline_snapshot._acceptance_transition`, which asks the live-vs-snapshot
    form of this question.

    ITS UNIVERSE IS `ACCEPTANCE_ACT_CSVS`, the four SPINE registries — SN, SR,
    LLR, TC — and the assumptions registry's two tiers, and not `SPINE_CSVS`,
    which is the amendment warn's three. SN is
    covered because it is a spine tier carrying the same `status` vocabulary and
    is the half of DevStg-Reqs the operator-acceptance dial holds, so a lane flipping
    a need is the worst case of this act rather than an exempt one (round 028).
    The three OFF-SPINE registries stay out; see `OUTSIDE_THE_ACCEPTANCE_ACT`.

    Operator ruling 6, 2026-10-07 (WI-849): the act this reports is an independent
    adjudicator's, in the authoring lane or on trunk. `acceptance_delta` directly
    below reads it ONCE for `merge_acceptance_refusal`, which requires every act
    backed by a recorded verdict over its own rows, and an adjudication row's
    recorded scope besides, at `integrate._acceptance_act_refusal`
    — this reader does not itself cross the `IF-091` seam, and the seam does not
    declare that it does.

    Returns [] when not applicable; any missing git context is a silent no-op,
    like `staged_spine_amendments`."""
    out = []
    for registry, _id_col, before_rows, after_rows, _csv in _spine_row_sides(
        root, base, head, ACCEPTANCE_ACT_CSVS
    ):
        for rid, row in after_rows.items():
            act = _acceptance_act(registry, rid, before_rows.get(rid), row)
            if act:
                out.append(act)
    return out


def rows_at(root, rev, rel_path, id_col):
    """`{id: row}` of one spine registry at commit `rev`, or `{}` when the
    registry is absent there under either carrier — `_spine_rows_at`, the row
    reader behind every two-tree scan in this module, offered for a walk along
    history (`check_test_first.record_acceptances`, over the record's copies).

    Public so a history reader parses a row the way the acceptance-act refusal
    does, through the same carrier resolution and the same `-000` filter,
    rather than growing a second reader of the registries at a revision."""
    return _spine_rows_at(root, rev + ":", rel_path, id_col)


def acceptance_acts_between(registry, before_rows, after_rows):
    """The acceptance acts `after_rows` perform against `before_rows`, in
    `staged_acceptance_acts`' record shape: every row that crossed into an
    acceptance claim (`flip`) or arrived already making one (`born`).

    THE HISTORY FORM OF THE SAME RULE. `staged_acceptance_acts` reads its two
    sides from two trees; a walk along trunk carries each commit's rows forward
    as the next commit's before side, so it asks the question of two row maps
    instead and reads each registry once per commit that touches it. The act
    itself is `_acceptance_act` in both, so the history and the lane refusal
    cannot disagree about which change blessed a row."""
    acts = []
    for rid, row in after_rows.items():
        act = _acceptance_act(registry, rid, before_rows.get(rid), row)
        if act:
            acts.append(act)
    return acts


# How `git diff --name-status` letters read as the ACT a branch performed on the
# snapshot. Worded from the letter rather than assumed, because the record is
# read by an operator deciding why their merge stopped, and a branch that DELETES a
# stale `SNAPSHOT_DIR` file reported as one it "wrote" is a false sentence in the
# one artifact that explains the stop. An unrecognised letter is still named —
# the file changed, and which way is the part this does not know.
_SNAPSHOT_ACT = {"A": "wrote", "M": "rewrote", "D": "deleted"}


def _snapshot_acts(name_status):
    """Yields `"<verb> <path>"` for a `--name-status` block: one line per
    `SNAPSHOT_DIR` file the delta touched, worded by its status letter. A line
    with no tab-separated path is skipped — an unparseable line is not an act."""
    for line in name_status.splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or not parts[-1].strip():
            continue
        letter = parts[0].strip()[:1]
        yield "{} {}".format(_SNAPSHOT_ACT.get(letter, "changed"), parts[-1].strip())


def acceptance_delta(root, base, head):
    """`(row acts, worded snapshot acts, refusal)` for one merge delta."""
    acts = staged_acceptance_acts(root, base, head)
    out = _git(
        root, ["diff", "--name-status", "--no-renames", base, head, "--", SNAPSHOT_DIR]
    )
    if out is None:
        return (
            [],
            [],
            (
                "cannot read {}'s {} delta against {}, so whether this branch wrote "
                "the acceptance record is unknowable; nothing was merged".format(
                    head, SNAPSHOT_DIR, str(base)[:10]
                )
            ),
        )
    return acts, sorted(_snapshot_acts(out)), None


def first_acceptance_scope(metas):
    """The typed scope of claimed first-acceptance rows (a combined sitting's
    `first-acceptance:` tokens included), read through `kitlib.sitting`'s one
    claimed-row reader, or None when none scopes one."""
    scopes = [
        _kitsitting.brief_scope(meta, "first-acceptance") for _name, meta in metas
    ]
    scopes = [scope for scope in scopes if scope is not None]
    return frozenset(r for s in scopes for r in s) if scopes else None


def _registry_identity(path):
    """The acceptance-act registry a carrier path belongs to (its tier's
    canonical path, whichever of `spine_carrier.tier_carriers` names it), or
    the path itself for a file of no acceptance-act tier.

    Implements: SR-178, LLR-278"""
    hits = (rel for rel, col in ACCEPTANCE_ACT_CSVS if path in _tier_carriers(rel, col))
    return next(hits, path)


def lane_acted_set(root, base, head, delta):
    """THE ONE DERIVATION OF A LANE'S ACTED SET (WI-849, Sol r3): `(acted,
    refusal)`, `acted` being `{"accept": {row id: registry}, "reaccept": {row
    id: registry}}` - every row the lane accepted or re-accepted, with the
    registry its id's tier names (a live flip: the registry the two-tree walk
    reports), present at the head or not, so a retired row authorizes its own
    registry's copy. Acceptances are the delta's live Status transitions
    (a flip or a row born accepted) AND the `accepted` rows of the act-ledger
    entries the branch added (`_added_acts`), which name rows the snapshot
    writer carried into acceptance with no live flip - a row live-accepted at
    the base whose recorded copy still read below it. Re-acceptances are the
    ledger's (`reaccepted_between`). The scope check, the backing check and
    the copy authorization all take this one set, so an act seen by one is
    seen by all; "no act" is both kinds empty. An unreadable delta or ledger
    is the refusal, never an empty set.

    Implements: SR-178, LLR-278"""
    acts, _files, refusal = delta
    reaccepted, added = frozenset(), []
    if not refusal and _wrote_ledger(delta):  # an unwritten ledger added nothing
        reaccepted, refusal = reaccepted_between(root, base, head)
        added = _added_acts(root, base, head)
    if refusal:
        return {"accept": {}, "reaccept": {}}, refusal
    accept = {act["id"]: act["registry"] for act in acts}
    ledger = {str(r) for a in added for r in a.get("accepted") or []} - set(accept)
    accept.update({rid: _tier_of(rid)[0] for rid in ledger})
    return {
        "accept": accept,
        "reaccept": {r: _tier_of(r)[0] for r in reaccepted},
    }, None


def _copy_lines(acted, snapshot_files):
    """THE COPY AUTHORIZATION over the acted set (`lane_acted_set`): a refusal
    line for each registry copy no acted row authorizes (WIDENED) and each
    accepted row's registry with no copy (WITHOUT ITS ANCHOR), `[]` when the
    copies match the acts. The record's own files (`SNAPSHOT_OWN_FILES`) are
    not registries. Both sides compare REGISTRY IDENTITY (`_registry_identity`).

    Implements: SR-178, LLR-278"""
    written = {
        line.partition(" ")[2][len(SNAPSHOT_DIR) + 1 :] for line in snapshot_files
    }
    ident = _registry_identity
    held = [reg for kind in acted.values() for reg in kind.values() if reg]
    authorized = {ident(r) for r in held}
    copied = {ident(r) for r in written - SNAPSHOT_OWN_FILES}
    widened = sorted(
        r for r in written - SNAPSHOT_OWN_FILES if ident(r) not in authorized
    )
    accepted = acted["accept"].values()
    missing = sorted({r for r in accepted if r and ident(r) not in copied})
    return [
        "  snapshot WIDENED to {} without an accepted row".format(r) for r in widened
    ] + ["  {} was accepted WITHOUT its anchoring snapshot".format(r) for r in missing]


def adjudication_acceptance_refusal(scope, acted, delta):
    """Judge the ACTED SET (`lane_acted_set`), never a scope on its own
    (WI-849, Sol r2, r3): every accepted row - a live flip or a ledger-only
    acceptance alike - lies in `scope` (an empty scope is OUTSIDE's EMPTY
    wording; `scope` None means the lane records none, so only its copies are
    judged), and every registry copy belongs to an acted registry. A lane with
    no act and no copy meets nothing here. A registry copy is WIDENED unless
    the set holds a row there, accepted or re-accepted, so the sections of one
    combined sitting each keep their own act (WI-841); an accepted row's
    registry with no copy is WITHOUT ITS ANCHOR (`_copy_lines`). Both sides
    compare REGISTRY IDENTITY (`_registry_identity`), so every carrier path of
    an authorized registry is its act's own - the obsolete carrier's copy a
    conversion deletes included."""
    _acts, snapshot_files, refusal = delta
    if refusal:
        return refusal
    accepted = acted["accept"]
    outside = sorted(r for r in accepted if scope is not None and r not in scope)
    copies = _copy_lines(acted, snapshot_files)
    if not outside and not copies:
        return None
    where = "`Adjudicates` scope ({})".format(";".join(sorted(scope or ())))
    where = where if scope else "an EMPTY `Adjudicates` scope"
    lines = ["  {} is OUTSIDE {}".format(rid, where) for rid in outside] + copies
    # THE REMEDY, PER ARM. The three lines above say what the delta did; a
    # session reading only those learns it is stopped and not what to do — and
    # the WIDENED arm in particular is reached by following the brief exactly
    # (its `--accepts` is fixed before the verdict, so a batch that returns a
    # registry's rows in full still names it). Each arm's repair is stated
    # where the stop is read; a lane recording no scope is told of no
    # `Adjudicates` row.
    head = "the acceptance act's copies do not match its acts: the merge admits"
    if scope is not None:
        head = "first-acceptance adjudication exceeds the acceptance act recorded on its `Adjudicates` row: the merge admits only scoped flips and"
    return (
        "{} exactly their registry snapshots; nothing was merged:\n{}\nRemedy — "
        "WIDENED: `--accepts` named a registry this act flipped nothing in (its "
        "rows were all RETURNED); drop that token and re-take the snapshot, so "
        "the copy blesses only text this act accepted. WITHOUT ITS ANCHOR: the "
        "flip landed with no copy behind it; add that registry to `--accepts`."
        "{}".format(
            head,
            "\n".join(lines),
            " OUTSIDE SCOPE: the row is another adjudication's; restore its "
            "`Status` byte-exact."
            if outside
            else "",
        )
    )


def merge_acceptance_refusal(root, base, head, metas, *, trunk):
    """Apply one derived acceptance delta to THE ONE ACTOR RULE (operator ruling 6,
    2026-10-07; WI-849): a lane's acts are admitted when every act is backed
    by a recorded verdict judging that act's own rows (`backed_act_refusal`),
    in whatever lane it is taken, and the snapshot copies exactly the
    registries those acts moved. A lane any of whose claimed rows records a
    scope (`kitlib.sitting.bounds_acts`: an adjudication-kind row, or a row
    scoping a first acceptance or an amendment) is bounded besides, whatever
    else it claims: its flips by the first-acceptance scope, its re-acceptances
    by the amendment scope (`reaccept_scope_refusal`). The bound is read off
    `metas`, never off a caller's flag, so a mixed lane keeps its adjudication
    row's scope (Sol r1 MAJOR 1); unreadable claims never reach here, the
    merge slot refuses them. A held rung is not judged here: every lane commit
    is judged against the dial committed on trunk by the lane rule that rides
    the merge slot's lane-commit walk (`held_status.commit_held_acceptance_lines`),
    so `trunk`, the commit the merge lands on, is read by no rule of this
    function. The scope, backing and copy checks all judge ONE acted set
    (`lane_acted_set`: the ledger's acceptances and re-acceptances and the live
    transitions), so an act recorded only in the ledger is judged by each.

    Implements: SR-178, LLR-278"""
    delta = acceptance_delta(root, base, head)
    acted, refusal = lane_acted_set(root, base, head, delta)
    if refusal:
        return refusal
    scope = None
    if any(_kitsitting.bounds_acts(meta) for _name, meta in metas):
        scope = first_acceptance_scope(metas) or frozenset()
        refusal = _kitsitting.malformed_refusal(metas)
        refusal = refusal or reaccept_scope_refusal(acted, metas)
    elif not any(acted.values()):
        return lane_acceptance_refusal(root, base, head, delta)
    added = _added_acts(root, base, head)
    refusal = refusal or _kitsitting.unrecorded_refusal(root, head, added)
    refusal = refusal or backed_act_refusal(root, base, head, acted, delta)
    return refusal or adjudication_acceptance_refusal(scope, acted, delta)


def backed_act_refusal(root, base, head, acted, delta):
    """THE ACTOR TEST at the merge slot (operator ruling 6, 2026-10-07; WI-849):
    why a lane's acceptance acts may not merge, or None. Every act must be backed
    by a RECORDED verdict among the bindings the branch carries that judged
    that act's own rows: each row it flips or mints accepted ruled ACCEPT in a
    first-acceptance part, each row it re-accepts ruled CLARITY, or MEANING with
    the bless mark, in an amendment part (the one reader,
    `kitlib.sitting.judged_rows`). It replaces "is every claimed spec of the adjudication
    kind?" as the test of who may act: the act is an independent
    adjudicator's, taken in the authoring lane or on trunk.

    The acts are the lane's one acted set (`lane_acted_set`): the act-ledger
    entries the branch added AND the delta's own flips, so a flip that wrote no
    ledger entry and a ledger acceptance no flip shows are judged alike. The judgement
    is WI-841's one reader (`kitlib.sitting.uncovered_refusal` over
    `recorded_at`), so a missing, failed, invalid or other-rows verdict refuses
    alike, worded with the acts by `lane_acceptance_refusal`. Independence rests
    on that reader: an outcome reads `recorded` only through
    `adjudicate_brief.record_outcome`, which a route calls after it ran the
    adjudication as its own call; no record names the session that authored a
    row, so the merge cannot compare the two sessions itself.

    Implements: SR-178, LLR-158"""
    acts = [
        {"accepted": sorted(acted["accept"]), "reaccepted": sorted(acted["reaccept"])}
    ]
    reason = _kitsitting.uncovered_refusal(root, base, head, acts)
    return reason and lane_acceptance_refusal(root, base, head, delta, reason)


def amendment_scope(metas):
    """The rows the claimed AMENDMENT adjudications ruled: the union of their
    `Adjudicates` cells and of a combined sitting's `amendment:` tokens, empty
    when none is claimed. A first-acceptance row's scope is its flips, not a
    re-acceptance's.

    Implements: SR-178, LLR-278"""
    return frozenset(
        rid
        for _name, meta in metas
        for rid in _kitsitting.brief_scope(meta, "amendment") or ()
    )


def _ledger_read(root, rev):
    """`(acts, failure)`: the act ledger's `[[act]]` entries at `rev` (IF-220 is
    the ledger's shape). `([], None)` when the tree does not list it;
    `(None, "cannot be read")` when it lists it but its blob cannot be read;
    `(None, "does not parse")` when its text is not a ledger. The one reader
    that tells those three apart; `_ledger_acts` is its older two-valued view.

    Implements: SR-178, LLR-364"""
    try:
        text = _kitgit.git_show(root, rev + ":", SNAPSHOT_DIR + "/" + SNAPSHOT_ACTS)
    except _kitgit.UnreadableBlob:
        return None, "cannot be read"
    if text is None:
        return [], None
    try:
        acts = tomllib.loads(text).get("act", [])
    except tomllib.TOMLDecodeError:
        return None, "does not parse"
    return (acts, None) if isinstance(acts, list) else (None, "does not parse")


def _ledger_acts(root, rev):
    """The act ledger's `[[act]]` entries at `rev`, `[]` where it is absent, or
    None when it does not parse (IF-220 is the ledger's shape). A ledger whose
    blob cannot be read reads as absent here, the merge rung's contract;
    `_ledger_read` is the reader that refuses it."""
    acts, failure = _ledger_read(root, rev)
    return [] if failure == "cannot be read" else acts


def _reaccepted_added(root, base, head):
    """`(entries, failure)`: the ledger entries `head` added over `base`, in
    file order, or the ledger's path, revision and what went wrong when either
    side cannot be read or does not parse.

    Implements: SR-178, LLR-364"""
    sides = []
    for rev in (base, head):
        acts, failure = _ledger_read(root, rev)
        if failure:
            path = SNAPSHOT_DIR + "/" + SNAPSHOT_ACTS
            return [], "{} {} at {}".format(path, failure, rev)
        sides.append(acts)
    return added_ledger_entries(sides[1], [sides[0]]), None


def _reaccepted_ids(before, after):
    """The row ids re-accepted by the ledger entries of `after` whose `seq`
    `before` does not hold.

    Implements: SR-178, LLR-278"""
    added = added_ledger_entries(after, [before])
    return frozenset(str(r) for a in added for r in a.get("reaccepted") or [])


def _snapshot_copy_rows(root, rev, rel_path, id_col):
    """`(rows, failure)`: `{id: row}` of the snapshot's copy of one tier at
    `rev`, through its carriers in preference order. `(None, None)` when the
    tree lists no copy; a listed copy that cannot be read or does not parse is
    a failure naming its path and revision, never an absence (which
    `_spine_rows_at` reads all three as).

    Implements: SR-178, LLR-364"""
    under = SNAPSHOT_DIR + "/"
    for path, rows, failure in _tier_reads(root, rev + ":", rel_path, id_col, under):
        if failure:
            return None, "{} {} at {}".format(path, failure, rev)
        return rows, None
    return None, None


def reaccepted_between(root, base, head):
    """`(ids, refusal)`: the row ids the act-ledger entries `head` added over
    `base` re-accepted, or a refusal naming the ledger when either side does
    not parse. An entry is added when its `seq` is not in `base`'s ledger.

    Implements: SR-178, LLR-278"""
    before, after = _ledger_acts(root, base), _ledger_acts(root, head)
    if before is None or after is None:
        return frozenset(), (
            "the act ledger {}/{} does not parse at {}, so which rows this "
            "merge re-accepts is unknowable; nothing was merged".format(
                SNAPSHOT_DIR, SNAPSHOT_ACTS, base if before is None else head
            )
        )
    return _reaccepted_ids(before, after), None


def _wrote_ledger(delta):
    """Did the acceptance delta write the act ledger? A re-acceptance moves no
    cell, so the ledger entries are the only trace of one."""
    return any(line.endswith("/" + SNAPSHOT_ACTS) for line in delta[1])


def reaccept_scope_refusal(acted, metas):
    """Refuse an adjudication's act re-accepting a row outside the `Adjudicates`
    scope of the amendment rows it claims — by name — or None.

    A re-acceptance moves no cell, so the flips the first-acceptance arm
    judges cannot show it; the acted set (`lane_acted_set`) carries the rows
    the act-ledger entries this branch added re-accepted. An amendment
    row's scope is the rows its verdict ruled, so re-anchoring any other row
    re-blesses text nobody judged. A lane claiming no amendment row has no
    re-acceptance scope at all.

    Implements: SR-178, LLR-278"""
    scope = amendment_scope(metas)
    outside = sorted(set(acted["reaccept"]) - scope)
    if not outside:
        return None
    return (
        "the adjudication's act re-accepts rows OUTSIDE the `Adjudicates` scope "
        "of its amendment row(s) ({}); nothing was merged:\n{}\nRemedy: a "
        "re-acceptance re-anchors text as judged, so it names only rows the "
        "amendment ruled. Re-take the snapshot with `--reaccepts` naming those "
        "rows alone; a drifted row outside them is another act's to judge.".format(
            ";".join(sorted(scope)) or "none claimed",
            "\n".join("  {} re-accepted OUTSIDE the scope".format(r) for r in outside),
        )
    )


# An amendment verdict's row rulings: the reader lives in `kitlib.verdict`
# (WI-841 round 5); the name stays here for its callers.
verdict_rulings = _kitverdict.verdict_rulings


def _tier_of(rid):
    """`(registry, id column)` of the amendment-walk tier row `rid` belongs to,
    read off its prefix, or `(None, None)`."""
    return next(
        ((r, col) for r, col in AMENDMENT_CSVS if rid.startswith(col[:-2])),
        (None, None),
    )


def _added_acts(root, base, head):
    """The act-ledger entries `head` adds over `base`, `[]` when either side
    does not parse (`reaccept_scope_refusal` names that).

    Implements: SR-178, LLR-278"""
    before, after = _ledger_acts(root, base), _ledger_acts(root, head)
    if before is None or after is None:
        return []
    return added_ledger_entries(after, [before])


def added_ledger_entries(entries, parents):
    """The act-ledger `entries` whose `seq` no ledger in `parents` holds: the
    ones a commit adds over its parents (each parent a list of entries, `[]`
    where it has no ledger). Compared by number, never by content, so a second
    act identical to the first is still an act of its own; an entry that is
    not a table is skipped on every side. The one reading of "the entries a
    commit adds", shared by the acceptance record's readers and the snapshot's
    commit rule and accepted-risk anchor.

    Implements: SR-178, LLR-278"""
    held = {a.get("seq") for parent in parents for a in parent if isinstance(a, dict)}
    return [a for a in entries if isinstance(a, dict) and a.get("seq") not in held]


def lane_acceptance_refusal(root, base, head, delta=None, reason=None):
    """Why a lane's delta may not merge because it performs an ACCEPTANCE ACT no
    verdict was asked to back - the refusal text, or None when it performs no
    act and writes no record. The merge slot words both refusals here: a record
    written with no act behind it, and acts `backed_act_refusal` found unbacked,
    its `reason` appended.

    THE ACT IS AN INDEPENDENT ADJUDICATOR'S, IN THE AUTHORING LANE OR ON TRUNK
    (operator ruling 6, 2026-10-07, superseding the trunk-side clause of the
    2026-09-01 ruling). A lane AUTHORS `Drafted` SN/SR/LLR/TC rows and AMENDS
    cell text on any such row, including accepted ones; its acts - a `Status`
    flipped into `Accepted`/`Founded`, a row minted already claiming one, a
    re-acceptance - merge only when `backed_act_refusal` finds each backed by
    a recorded verdict that judged its own rows. A copy under `SNAPSHOT_DIR`
    with no flip and no re-acceptance behind it is an act no verdict can
    back, and this is its refusal. The off-spine three
    (`OUTSIDE_THE_ACCEPTANCE_ACT`) stay outside this rung - their acceptance cells
    are OI-30 D3's.

    HERE RATHER THAN IN THE MERGE SLOT, on `LLR-178`'s separation - the writer
    must not also be the judge of its own writes, and by the same token the
    coordinator that merges is not the reader that decides what a spine delta
    did. `integrate._acceptance_act_refusal` supplies the merge base and the rung's
    place in the ladder; the reading and the wording are this module's, beside
    the two-tree walk and the mirror rules they share their material with.

    A DE-ACCEPTANCE IS NOT AN ACT, and neither is an amendment to an accepted row:
    the lane may make both, and the amendment adjudication the intake mints at
    this same merge is what judges the second. THE HONEST BOUND is
    `integrate._minted_id_refusal`'s: this defeats the accident and a lane that
    drifts, not a lane that means to - a branch could still write a flip through
    some file nothing here reads.

    Fails closed on an unreadable snapshot delta: an unread diff is not an
    empty one. `staged_acceptance_acts`' own degrade is the opposite direction
    (silence outside a git checkout) and is deliberate - it is a READER, and the
    refusal that consumes it is where the fail-closed posture belongs.

    Implements: SR-178, LLR-158
    """
    acts, snapshot_files, refusal = delta or acceptance_delta(root, base, head)
    if refusal or not (acts or snapshot_files):
        return refusal
    lines = [
        "  {} {} in {}".format(
            act["id"],
            "flipped {} -> {}".format(act["before"] or "(absent)", act["after"])
            if act["act"] == "flip"
            else "was minted born {}".format(act["after"]),
            act["registry"],
        )
        for act in acts
    ] + ["  {}".format(name) for name in snapshot_files]
    return (
        "{} performs an ACCEPTANCE ACT no recorded verdict backs. The act is an "
        "independent adjudicator's, never the session's that authored the rows, "
        "in the authoring lane or on trunk (operator ruling 6, 2026-10-07; "
        "PROCESS.md §4): that session leaves SN/SR/LLR/TC, assumption and "
        "surrogate rows `Drafted` and does not write {}/. Leave the rows "
        "`Drafted` for the first-acceptance adjudication minted at this merge, "
        "or back each act with an adjudicator's recorded verdict over its rows. "
        "Nothing was merged:\n{}\n{}".format(
            head, SNAPSHOT_DIR, "\n".join(lines), reason or ""
        )
    ).rstrip()


def staged_drafted_rows(root, base="HEAD", head=None):
    """Every `Drafted` spine row a delta ADDS or AMENDS between two trees:

        [{"registry": <carrier path>, "id": <row id>, "act": "added" | "amended",
          "changed": {cell: (before, after)}}]

    The first-acceptance trigger's input (WI-572): a lane authors `Drafted` rows
    and amends their text, and what it hands the adjudicator is exactly this set
    — the rows whose text is now waiting on a first acceptance nobody has given.
    `changed` is empty on an `added` row (there is no before side to diff) and
    carries BOTH §A5.1 halves on an `amended` one, because below acceptance the
    split buys nothing: no cell of a `Drafted` row was ever blessed, so none of
    them is "traced-only" relative to a signature.

    A row that is `Drafted` on the after side only. A row that LEFT `Drafted`
    is an acceptance act (`staged_acceptance_acts`); every row that ENTERED it is
    reported here as `amended`, even when only Status moved. The withdrawal
    itself still blesses nothing and remains absent from `staged_acceptance_acts`,
    but the resulting Drafted row now awaits the adjudicator's acceptance just as
    an authored Drafted row does.

    Returns [] when not applicable; silent no-op on missing git context."""
    out = []
    for registry, id_col, before_rows, after_rows, csv_path in _spine_row_sides(
        root, base, head
    ):
        for rid, row in after_rows.items():
            if not rid or not _kitspine.is_drafted(row):
                continue
            before = before_rows.get(rid)
            if before is None:
                out.append(
                    {"registry": registry, "id": rid, "act": "added", "changed": {}}
                )
                continue
            split = split_changed_cells(csv_path, id_col, before, row)
            changed = dict(split["accepted"])
            changed.update(split["traced"])
            entered_drafted = not _kitspine.is_drafted(before)
            if changed or entered_drafted:
                out.append(
                    {
                        "registry": registry,
                        "id": rid,
                        "act": "amended",
                        "changed": changed,
                    }
                )
    return out


def staged_spine_amendments(root, base="HEAD", head=None):
    """The structured amendment set behind the amend-without-flip warn (WI-316,
    narrowed by WI-380) — the seam adjudication (WI-388) consumes.

    One record per ACCEPTED-TEXT spine row (`_ACCEPTED_TEXT` — `Accepted`, into
    which `Verified` and `Planned` both folded at D-9 step 5) amended between the
    two trees without its status moving, each cell sorted into the §A5.1 halves with its before/after:

        {"registry": <csv path>, "id": <row id>,
         "accepted": {cell: (before, after)}, "traced": {cell: (before, after)}}

    WHICH TWO TREES is a parameter, and WI-388 needs it to be: `head=None` (the
    default) compares the INDEX against `base`, which is the hook's `--staged`
    question, but §A5.2 mints adjudication from a **trunk commit**, and a commit
    is not the index — `staged_spine_amendments(root, "HEAD~1", "HEAD")` asks
    the post-commit question the dispatcher actually has to ask. Both arms are
    tested.

    A record may carry a traced change with NO accepted change. Only the
    `SN-Refs`/`Verifies`/`SR-Refs` subset of those is the WI-388 case (§A5.1
    routes a re-point of what a requirement answers to, what a test claims to
    cover, or which SR owns an LLR — the last ruled traced at WI-388 — to
    adjudication); a `TestRefs`/`Phase` change, or the removal of a retired
    `Module`/`CodeSymbol`/`Component` cell, is simply silent — traced, not pending, nothing owed. Rows are parsed
    with the csv module over the full file text on each side (spine cells are
    long; never line-split). Returns [] when not applicable; any missing git
    context is a silent no-op, like staged_findings. A NEW row (id absent on the
    base side) is not an amendment; a row whose Status moved (to `Drafted`,
    `Founded`, anything) made a deliberate call this does not
    second-guess — `staged_acceptance_acts` is the reader for the half of that
    exemption which BLESSES text, over the same walk.

    THE TWO-TREE WALK IS `_spine_row_sides`, shared since WI-572 rather than
    inlined here, so this reader and the two acceptance-act readers above it
    cannot disagree about which registries and rows the delta contains. Its
    universe is `AMENDMENT_CSVS` since WI-791 (OI-100 gap 1): the need,
    assumption and surrogate tiers join the three spine tiers."""
    # Each row answers for its OWN cells (operator ruling 2026-08-17m): the
    # sanctioned amend path is flipping the AMENDED row itself in the same
    # commit — a Status that moved is exempted below. The retired chain
    # reading's owning-SR exemption (a parent flip sanctioning a silent
    # child amendment) is gone with the doctrine: a child whose accepted
    # cells change while its own Status still claims acceptance warns,
    # whatever its parent does.

    out = []
    for registry, id_col, head_rows, staged_rows, csv_path in _spine_row_sides(
        root, base, head, AMENDMENT_CSVS
    ):
        if not head_rows or not staged_rows:
            continue  # first commit / newly added registry — nothing accepted yet
        for rid, row in staged_rows.items():
            changed = _amended_cells(csv_path, id_col, rid, head_rows.get(rid), row)
            if changed:
                out.append(dict(changed, registry=registry, id=rid))
    return out


def _amended_cells(csv_path, id_col, rid, head, row):
    """One row's `split_changed_cells` when it is an AMENDMENT — present on
    both sides, reading the same accepted-text Status on both, with a cell
    moved — else None. `staged_spine_amendments`' per-row judgement, extracted
    unchanged at WI-791 to keep the walk under the complexity limit."""
    if not rid or rid.endswith("-000") or head is None:
        return None
    head_status = (head.get("Status") or "").strip().lower()
    cur_status = (row.get("Status") or "").strip().lower()
    # ACCEPTED-TEXT STATES, both sides, and the SAME one. Since D-9
    # step 5 that is the single value `Accepted`; before the fold it was
    # `Verified` OR `Planned`, and requiring the SAME one on both sides
    # is what kept a legitimate rung move from reading as an amendment.
    # A status that MOVED between the two sides is still exempt,
    # unchanged: that is a deliberate call this does not second-guess.
    if head_status != cur_status or head_status not in _ACCEPTED_TEXT:
        return None
    changed = split_changed_cells(csv_path, id_col, head, row)
    return changed if changed["accepted"] or changed["traced"] else None


def staged_spine_findings(root):
    """The amend-without-flip warn (WI-316; warn-first, `--staged` only), scoped
    by WI-380 to ACCEPTED cells only.

    A staged diff that changes the accepted cells of a spine row whose Status
    reads the same accepted-text value (`Accepted`, since D-9 step 5) in both
    HEAD and the stage has amended accepted prose without re-blessing it — the
    write-time discipline the old RE-ATTESTATION-PENDING commit-message prose
    never had. One warning per amended row, naming the changed cells. A row
    whose only changes are TRACED (§A5.1) is silent here by ruling; it still
    appears in `staged_spine_amendments`, which is where WI-388 picks it up.
    Index-vs-HEAD by construction — this is the hook's question, so it takes no
    rev arguments; the post-commit view is `staged_spine_amendments`'s."""
    return [
        "{}: accepted cell(s) {} amended while Status stays put — a "
        "post-acceptance amendment owes a fresh operator read (process.md §7). "
        "Since D-9 step 7 there is no marker to set: either commit the amendment "
        "on its own and re-accept it in the NEXT commit with `intake.py "
        "snapshot --reaccepts {}` (text first, the act second: a commit that "
        "writes the record changes no other spine cell), or the change rides "
        "as SNAPSHOT DRIFT until the next sitting — "
        "visible on the re-accept brief and open-items.html, but not "
        "blessed".format(a["id"], ", ".join(sorted(a["accepted"])), a["id"])
        for a in staged_spine_amendments(root)
        if a["accepted"]
    ]


# The perspective cell the arm below watches. ONE NAME, stated once: the column
# is `Hat-Refs` at both tiers that carry it (WI-484 phase 0's ruling), and the
# arm reads `traced_cells` rather than this constant to decide WHICH tiers those
# are, so adding the column to a third registry extends the guard with it.
HAT_REFS_CELL = "Hat-Refs"


def staged_hat_refs_findings(root):
    """THE AMEND-WITHOUT-FLIP GUARD'S SECOND ARM (OI-32 phase 5, OI-33's
    surviving residue) — warn-first, `--staged` only, never an exit code.

    A row whose ACCEPTED cells moved while its `Hat-Refs` cell did not has been
    amended without re-examining which perspectives bear on it. The component
    view is DERIVED from these cells (OI-32 ruled (d)), and a derived view is
    only as true as its rows: a generated artifact can be perfectly FRESH and
    still carry a wrong answer, because freshness compares the artifact to its
    regeneration and never asks whether the source was right. This is the one
    thing generation cannot do.

    THE COMPARISON IS BY CELL CLASS, NOT BY FILE OR LINE, and that is the whole
    design. The measured instance is `backlog_staleness_findings`, which blames
    the SR registry by LINE: the phase-2 backfill wrote an INFORMATIVE cell on
    55 rows, re-dated five open WIs' cited rows and raised seven warns, because
    a `git blame` line time cannot tell an accepted cell from a traced one.
    `split_changed_cells` can, so this arm reads it — which is why `Hat-Refs`
    was CLASSIFIED traced at both tiers rather than left to the residual.

    THE BASELINE IS THE ONE THE GUARD IT JOINS ALREADY USES: HEAD versus the
    index, via `staged_spine_amendments`, over rows reading the same
    accepted-text Status on both sides. Two consequences, both deliberate and
    both HONEST VACUITY rather than coverage:

      * A row with NO baseline is not guarded. A row absent from HEAD (newly
        minted, this commit) has nothing to compare, and a row below acceptance
        has blessed nothing to amend behind an operator's back — the same population
        rule `staged_spine_amendments` documents, inherited rather than
        re-litigated here.
      * A TIER with no `Hat-Refs` column is silent structurally (the TC tier
        today), not by an allowlist.

    NOT THE `last_accepted` SNAPSHOT, and the trade is worth recording: that
    baseline would make the finding STAND until answered, where this one is a
    single warn at the commit that earns it. It was declined on OI-33's own
    timing argument — the party who knows whether the perspectives moved is the
    one making the change, at the moment they make it — and on the ruling's
    words, "same shape, same home, warn-first". The standing half of the same
    question is already carried for ACCEPTED cells by snapshot drift; if this
    warn is measured to be ignored, promoting it to a drift-tier finding is the
    next rung, on evidence.

    AN EMPTY `Hat-Refs` CELL STILL FIRES. A cell that was never filled and a
    cell deliberately left empty (`SR-040`, argued and correct)
    are indistinguishable to a reader, and the guard's question is whether the
    set was RE-EXAMINED, which an unchanged empty cell does not answer.

    Implements: SR-161, LLR-202
    """
    return [
        "{}: accepted cell(s) {} amended while {} stayed put — the row's "
        "substance moved and its perspective record did not, so the derived "
        "component/knowledge view keeps answering from the old lenses "
        "(process.md §7; OI-32 phase 5). Re-read the row's hats and either "
        "update {} in this commit or leave it deliberately — an unchanged cell "
        "cannot say which".format(
            a["id"], ", ".join(sorted(a["accepted"])), HAT_REFS_CELL, HAT_REFS_CELL
        )
        for a in staged_spine_amendments(root)
        if a["accepted"]
        and HAT_REFS_CELL in traced_cells(a["registry"])
        and HAT_REFS_CELL not in a["traced"]
    ]


# The `last_accepted` snapshot's root, repo-relative. RESTATED rather than
# imported from `baseline_snapshot`: the import edge runs the other way (that
# module reads `split_changed_cells` from here), and a back-import would make
# the pair un-loadable. One string, pinned equal by
# tests/test_baseline_snapshot.py — the F5 plumbing-duplication sanction, with
# the behavioural pin the D-7 ruling requires.
SNAPSHOT_DIR = "docs/archive/last_accepted"

# The snapshot's prose stamp: rendered for a human, PARSED BY NOTHING, and with
# no live counterpart to mirror.
SNAPSHOT_README = "README.md"

# The snapshot's act ledger (`baseline_snapshot.ACTS`, restated for the reason
# the directory is, and pinned equal by tests/test_baseline_snapshot.py): the
# typed record of each acceptance act, and like the README a file with no live
# counterpart. These two are the snapshot's own files; every other file under
# the root is a registry copy the mirror rules compare with live.
SNAPSHOT_ACTS = "acts.toml"
SNAPSHOT_OWN_FILES = frozenset({SNAPSHOT_README, SNAPSHOT_ACTS})
_LEDGER = SNAPSHOT_DIR + "/" + SNAPSHOT_ACTS


def _snapshot_survives(root, new_rev):
    """True when ANYTHING at all remains under the snapshot root in the new tree.

    The two arms are the two things `new_rev` can be (`_spine_revs`' contract):
    `":"` is the INDEX, which `ls-files --cached` reads and where a staged
    deletion has already removed the entry; anything else is `"<rev>:"`, whose
    tree `ls-tree -r` reads. Degrades to False on any git failure, which is the
    quiet direction — an unanswerable question must not manufacture a finding.

    Implements: SR-179, LLR-178
    """
    if new_rev == ":":
        out = _git(root, ["ls-files", "--cached", "--", SNAPSHOT_DIR])
    else:
        out = _git(
            root, ["ls-tree", "-r", "--name-only", new_rev[:-1], "--", SNAPSHOT_DIR]
        )
    return bool(out and out.strip())


def _mirror_repair(live_rel):
    """The repair a snapshot-mirror finding prescribes, for the registry whose
    copy diverged.

    A bare `intake.py snapshot` is no repair here: it writes only a registry
    the act authorises, so with no `Status` move it writes nothing, and it
    carries no drifted row the act does not name. So the finding names the two
    repairs that work: put the blessed copy back, or take a fresh act whose
    arguments carry the authority for this registry and name the rows it
    re-accepts. The `--accepts` token is the registry's STEM:
    `baseline_snapshot.resolve_registry` takes a canonical rel, filename or
    stem, and a CSV carrier's live path is none of those, so the path itself
    would refuse."""
    return (
        "Repair: restore the copy that was blessed, or take a fresh reviewed "
        'acceptance act that writes it — `intake.py snapshot --accepts "{}=<REF>" '
        "--reaccepts <ROW-ID>[,<ROW-ID>...]`, naming each accepted row whose "
        "text the copy should take from live; a bare `intake.py snapshot` "
        "writes nothing here".format(PurePosixPath(live_rel).stem)
    )


def staged_snapshot_findings(root, base="HEAD", head=None):
    """THE MIRROR INVARIANT (snapshot design §F3; at the row since WI-1060), as
    warn strings.

    > In any commit that writes a registry's copy under
    > `docs/archive/last_accepted/`, that copy must be the copy that commit's
    > acceptance act writes: the previous copy with exactly the rows the act
    > names taken from the live registry in that same commit, and every other
    > row placed by the row rule (`record_rows`).

    The snapshot is the record of what an operator blessed, and it is just files —
    nothing about a text file stops someone editing it. This is the guard, and
    it is exact rather than heuristic: a legitimate `copy_live` satisfies it
    ALWAYS, by construction, because the act's named rows are read from the
    act-ledger entries the commit adds and the rest from its parent and its own
    live text. It fails a hand edit, a partial copy, a copy-then-amend-live, an
    unnamed row's drift carried in, a named row copied with an edit and a row
    dropped that no act retired, each named by its row; and a partial DELETION —
    a copy, or the act ledger, removed while the rest of the record stands
    (adversarial round 2, 2026-08-15: the deletion path exited silently). A
    record whose act ledger holds no entry carrying `kept` was written whole by
    the writer before WI-1060, and a copy it writes is judged as it was written:
    byte-identical to its live counterpart in the same commit, so an existing
    record needs no migration.

    The consequence worth stating plainly: **the only way to write text into
    the snapshot is to write it into the live registry first** — an acceptance,
    in a reviewed commit, naming its rows.

    Index-vs-HEAD by default (the hook's question; during a merge, the act
    ledger entries the merge brings in over HEAD name their rows too, so an act
    the other side took is carried, not refused); `head` takes a
    commit-ish for the post-commit view, matching `staged_spine_amendments`'
    shape. Silent no-op when git cannot answer or no snapshot file moved — the
    same degrade every other scan here takes.

    **TWO SEVERITIES SINCE D-9 MIGRATION STEP 7, which is what the design asked
    for** (§F3 risk 3: *"warn at the staged hook, ERROR on the integrity
    floor"*). This producer returns plain strings; the `--staged` loop prints
    them as warns, AND `trace.py` appends them to `findings.integrity`, so they
    fail `--strict-integrity` — the always-on floor the pre-commit hook runs at
    every gate.

    Implements: SR-179, LLR-178
    """
    revs = _spine_revs(root, base, head)
    if revs is None:
        return []
    staged_names, _old_rev, new_rev = revs
    prefix = SNAPSHOT_DIR + "/"
    names = sorted(n for n in staged_names if n.startswith(prefix))
    if not names:
        return []
    # Against the first parent alone, so the entries a merge brings in name
    # their rows: the other side's act wrote those rows, and the merge carries
    # them (`added_acts_findings` judged those entries on their own branch).
    parents = [base]
    named, by_row = record_rows.tree_acts(
        root, _LEDGER, {0: (parents, new_rev[:-1])}, added_ledger_entries
    )[0]
    out = []
    for name in names:
        if name[len(prefix) :] == SNAPSHOT_README:
            continue
        out += _staged_copy_lines(root, name, parents, new_rev, named, by_row)
    return out


def _written(root, name, parents, new_rev, named):
    """`record_rows.written_problems` over this record, with this module's cell
    comparison: the faults of the copy `name` tree `new_rev` writes, at the row.

    Implements: SR-179, LLR-178"""
    args = (root, SNAPSHOT_DIR, name, parents, new_rev, named, split_changed_cells)
    return record_rows.written_problems(*args)


def _staged_copy_lines(root, name, parents, new_rev, named, by_row):
    """`staged_snapshot_findings`' judgement of one file under the record."""
    live_rel = name[len(SNAPSHOT_DIR) + 1 :]
    snap_text = _git(root, ["show", new_rev + name])
    if snap_text is None:
        # DELETED from the snapshot in this commit. Silent ONLY when the whole
        # record went with it — retiring the mechanism, or the wholesale
        # replacement §A1 describes. A single copy, or the act ledger, deleted
        # while the rest of the record stands IS a hole: `unanchored_findings`
        # reads a copy, and the ledger says which acts were taken and where the
        # row-by-row judgement begins. (Adversarial round 2, 2026-08-15.)
        if not _snapshot_survives(root, new_rev):
            return []
        return [
            "{} was DELETED from the {} snapshot while the rest of the record "
            "still stands — a file removed from the record of what was accepted "
            "is not a smaller record, it is a missing one; the snapshot is "
            "replaced WHOLESALE at a signing, never trimmed a file at a "
            "time".format(name, SNAPSHOT_DIR)
        ]
    if live_rel == SNAPSHOT_ACTS:
        return []
    live_text = _git(root, ["show", new_rev + live_rel])
    if live_text is None:
        return [
            "{} is in the {} snapshot but {} does not exist in this commit — "
            "a snapshot file with no live counterpart is a record of text the "
            "repo no longer has".format(name, SNAPSHOT_DIR, live_rel)
        ]
    if by_row:
        problems = _written(root, name, parents, new_rev[:-1], named)
    else:
        problems = [] if snap_text == live_text else ["the whole file differs"]
    return [
        "{} is NOT byte-identical to what this commit's act writes from {}: {} — "
        "the snapshot is the record of what an operator blessed, so it may only "
        "ever be written by an act copying from live the rows it names "
        "(`intake.py snapshot`). A hand edit, a partial copy and a "
        "copy-then-amend-live all land here. {}".format(
            name, live_rel, problem, _mirror_repair(live_rel)
        )
        for problem in problems
    ]


def committed_snapshot_findings(root):
    """THE MIRROR INVARIANT OVER THE COMMITTED TREE — the half `staged_snapshot_
    findings` cannot reach (adversarial round, 2026-08-20: ROUND-OPUS CRITICAL-3
    / ROUND-SOL MAJOR-2).

    The staged rule is keyed on a snapshot file being IN THE COMMIT. That makes
    it exact and cheap, and it makes its blind spot exact too: once a forged or
    stale copy has LANDED — hooks bypassed, or a commit made outside them — no
    later run stages a snapshot file, so nothing ever looks at it again.

    So this asks the same question of history rather than of the index: for every
    registry copy under the snapshot root, **was it, at the commit that last
    wrote it, the copy that commit's act writes?** — judged at the row when the
    act ledger at that commit's parent, or an entry the commit adds, carries
    `kept` (WI-1060), and otherwise as it was written: byte-identical to its
    live counterpart there. That framing is what makes the rule safe to run
    ALWAYS, and the alternative shape — comparing the snapshot to live in the
    WORKING TREE — is the one to refuse: the snapshot is deliberately behind
    live while an amendment is pending, and that lag IS the signal (see
    `baseline_snapshot`'s header). Live moving on afterwards changes nothing:
    the comparison is pinned to the copy's own writing commit, so a legitimate
    copy keeps passing forever and a forgery keeps failing forever.

    Git is asked in batches: one `cat-file --batch` for every act ledger the
    judgement reads, one `--batch-check` comparing object ids for the copies
    judged whole (identical content has the identical id, so comparing ids IS
    the byte comparison), and one blob read per copy judged at the row.

    Degrades to `[]` off git, on any git failure, and for an untracked snapshot
    (a scaffold that has committed nothing has no committed state to judge).

    Implements: SR-179, LLR-178"""
    revs = _snapshot_write_revs(root)
    if not revs:
        return []
    prefix = SNAPSHOT_DIR + "/"
    pairs = [
        (name, name[len(prefix) :], rev)
        for name, rev in sorted(revs.items())
        if name.startswith(prefix) and name[len(prefix) :] not in SNAPSHOT_OWN_FILES
    ]
    trees = {rev: ([rev + "^"], rev) for _n, _l, rev in pairs}
    acts = record_rows.tree_acts(root, _LEDGER, trees, added_ledger_entries)
    out = _whole_file_lines(root, [p for p in pairs if not acts[p[2]][1]])
    for name, live_rel, rev in (p for p in pairs if acts[p[2]][1]):
        problems = _written(root, name, [rev + "^"], rev, acts[rev][0])
        out += [
            "{} is NOT byte-identical to what its act wrote from {} at {}, the "
            "commit that last wrote it: {} — the snapshot is the record of what an "
            "operator blessed, so it may only ever be written by an act copying "
            "from live the rows it names (`intake.py snapshot`). This divergence "
            "has LANDED. {}".format(
                name, live_rel, rev[:8], problem, _mirror_repair(live_rel)
            )
            for problem in problems
        ]
    return out


def _whole_file_lines(root, pairs):
    """The committed rule's wording for copies written whole
    (`record_rows.whole_file_faults`): each `(name, live rel, rev)` must be
    byte-identical to its live counterpart at `rev`.

    Implements: SR-179, LLR-178"""
    return [
        "{} was written into the {} snapshot at {} where {} did not exist — a "
        "snapshot file with no live counterpart in its own writing commit is a "
        "record of text the repo never had".format(name, SNAPSHOT_DIR, rev[:8], live)
        if fault == "absent"
        else "{} is NOT byte-identical to {} at {}, the commit that last wrote it "
        "— the snapshot is the record of what an operator blessed, so it may only "
        "ever be written by copying the live file (`intake.py snapshot`). This "
        "divergence has LANDED. {}".format(name, live, rev[:8], _mirror_repair(live))
        for name, live, rev, fault in record_rows.whole_file_faults(root, pairs)
    ]


def _snapshot_write_revs(root):
    """`{snapshot path: the rev that last wrote it}` over the COMMITTED history,
    or None when git cannot answer.

    One `git log --name-only` over the snapshot root answers for every file at
    once: history is walked newest-first, so the FIRST commit that names a path
    is the one that last wrote it. `--no-renames` for the reason `_spine_revs`
    gives — a moved registry must show up under its old path too."""
    log = _git(
        root,
        ["log", "--format=%x01%H", "--name-only", "--no-renames", "--", SNAPSHOT_DIR],
    )
    if log is None:
        return None
    out, rev = {}, None
    for line in log.splitlines():
        if line.startswith("\x01"):
            rev = line[1:].strip()
            continue
        name = line.strip()
        if name and rev and name not in out:
            out[name] = rev
    return out


def _empty_tree(root):
    """The empty tree's id in this repository's hash, or None off git — what a
    ROOT commit is compared with."""
    out = _git(root, ["hash-object", "-t", "tree", "--stdin"], stdin="")
    return out.strip() if out and out.strip() else None


# The parent-first rule's registries: the four spine tiers of the acceptance-act
# set (the need, requirement, design and test tiers), read by
# `landing_rules.parent_first_tiers` and, as its marked spine, by `held_status`.
PARENT_FIRST_CSVS = tuple(
    (path, col) for path, col in ACCEPTANCE_ACT_CSVS if col in SPINE_TABLE
)


def _commit_parents(root, rev, question, first=False):
    """`(parents, lines)` for one commit, read off the commit object itself
    (not `rev^1`, which a shallow boundary hides): its parents, or only the
    first when `first`, with `[]` lines when each is readable. A commit git
    cannot read, or a parent missing from the repository (a shallow clone, a
    missing object), is one line naming it and `question`, never read as a
    root (A1). A true root commit is `([], [])`. The one parent reader of the
    two per-commit rules the merge slot walks a lane with.

    Implements: SR-148, SR-140, LLR-298, LLR-302
    """
    body = _git(root, ["cat-file", "commit", rev])
    if body is None:
        return [], ["cannot read commit {}, so it is unjudged".format(rev)]
    head = body.split("\n\n", 1)[0].splitlines()
    parents = [line.split()[1] for line in head if line.startswith("parent ")]
    parents = parents[:1] if first else parents
    for parent in parents:
        if _git(root, ["cat-file", "-e", parent + "^{commit}"]) is None:
            return [], [
                "commit {}'s parent {} cannot be read in this repository (a "
                "shallow clone or a missing object), so whether {} is unknown; "
                "fetch the parent and retry".format(rev[:10], parent[:10], question)
            ]
    return parents, []
