"""THE ACCEPTANCE RECORD — what an amendment IS, and the mirror it is measured
against.

The boundary, in one sentence, because a decomposition that cannot say where its
line is has not drawn one: **everything here compares TWO GIT TREES cell by cell
to answer whether attested text has moved away from the copy recording its
acceptance; everything left in `check_trajectory.py` asks what the registries say
TODAY.** Nothing in this module reads the working tree, and the free-name census
proves it rather than the docstring claiming it — the whole module's only
non-builtin dependencies are `spine_carrier` (which carrier a spine registry
uses) and one `git -C <root> … or None` primitive — and, for the held status
at the end of the module, `kitlib.authority`'s rung tables.

WHAT IT OWNS. `SR-178` (text that has moved away from its acceptance record is
reported) and `SR-179` (the record can only ever be written by copying live
text), plus the staged `Hat-Refs` arm of the same amendment comparison
(`SR-161`, `LLR-202`), which is that comparison applied to one traced cell:

    the cell split      `SPINE_TRACED_CELLS` / `SPINE_APPROVED_CELLS`,
                        `spine_cell_class`, `traced_cells` — the §A5.1 owner
                        ruling that decides which cells arm a re-attest window
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

WHY THE JUDGE IS STILL NOT THE WRITER. `LLR-178`'s attested rationale places the
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

Contracts: IF-091, IF-129, IF-196 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-091: the staged spine-amendment set, offered as a call.
    `staged_spine_amendments(root, base, head)` returns one record per
    approved-text spine row amended between the two trees WITHOUT its status
    moving — `{"registry", "id", "approved": {cell: (before, after)},
    "traced": {...}}` — and `AMENDMENT_CSVS` names the registries and id
    columns that walk covers: the requirement, design and test tiers, the need
    tier and the assumption registry's two tiers (OI-100, WI-791). Which two trees is a parameter, so the same call answers
    the index-against-HEAD question and the commit-against-commit one. It
    classifies and stops: which traced cells oblige an act is the caller's
    ruling, not this module's. A new row is not an amendment, a row whose
    status moved is a deliberate call this does not second-guess, and any
    missing git context degrades to `[]` rather than raising.
    THE SAME WALK ANSWERS THE APPROVAL-ACT QUESTIONS (owner ruling 2026-09-01).
    `staged_approval_acts(root, base, head)` returns the rows that CROSSED into
    an approval claim or arrived already making one — precisely the set the
    amendment reader exempts, over the WIDER `APPROVAL_ACT_CSVS` universe that
    adds the SN tier — and `staged_drafted_rows` returns the rows a lane
    added, amended, or moved into `Drafted`. `lane_approval_refusal(root, base, head)`
    is the judgement over the first: the text refusing a work branch that
    performs the approval act, or None. It fails CLOSED on an unreadable
    snapshot delta, the opposite pole from its readers' silent degrade, because
    a refusal is where the conservative direction belongs. All four share
    `_spine_row_sides`, so no reader can be the only one that sees a row.
    `merge_approval_refusal(root, base, head, metas, adjudication, *, trunk)`
    is the merge slot's one call: a lane's delta through `lane_approval_refusal`, an
    adjudication's flips through its first-approval scope, and its
    re-attestations — read from the act ledger entries the delta added — through
    `reattest_scope_refusal`, which refuses by name every re-attested row
    outside the `Adjudicates` scope of the amendment rows the lane claims, and
    `held_reattest_refusal`, which refuses by name every row re-attested on a
    rung the dial at `trunk` (the commit the merge lands on) holds unless the
    row is approved at the act and the act entry names a verdict file that
    rules the row CLARITY (`verdict_rulings` reads its `- [CLARITY] <id>`
    lines).
Contract IF-129: the ONE cell-comparison basis.
    `split_changed_cells(registry_path, id_col, before_row, live_row)` returns
    `{"approved": {cell: (before, after)}, "traced": {cell: (before, after)}}`
    for a single row, excluding the id column (a join key, not content) and
    `Status` (the flip the caller is asking about) structurally, at the callee.
    Every reader of "what changed on this row" joins here, so the staged
    amendment guard and a snapshot comparison cannot disagree about which cells
    are content or which half of the remainder arms an act. The dependency runs
    one way only: nothing in this module imports the readers that call it.
Contract IF-196: the held status, read from a delta. `staged_status_moves(root,
    base, head, paths)` returns every change to a status cell of an off-spine
    registry in `HELD_STATUS_REGISTRIES` between two trees, or between `base`
    and the index when `head` is None - a changed cell, and a row added or
    removed with a status - as `{"registry", "id", "before", "after"}`,
    an absent side reading ""; `head` may be a tree, and `paths` narrows the
    registries to those among them. The needs file is read for its stakeholder
    tier alone (`STATUS_TABLES`). `merge_status_moves(root, parents)` is the
    index's moves against the first of `parents` that differ from EVERY one of
    them - a staged merge result's own - and `pending_status_moves(root)` the
    moves of the commit in progress, merge or not. `committed_status_moves(root,
    rev)` is the same as `staged_status_moves` for one commit against its first
    parent, or the empty tree for a root commit, across the spine registries
    too, the needs tier included, each row once. `held_status_lines(dial,
    moves)` returns one line naming the registry, the row and the rung of every
    move whose rung the dial holds, a registry the rung map does not name read
    as held; `held_status_refusal(dial, moves)` joins them into the refusal,
    or returns None. A delta git cannot read is `[]`; a registry
    side that does not parse is one move naming the registry.

THE RULING SYNC (WI-790; OI-102 Q3) is the third two-tree rule here, and the
one with no dial: a commit that takes an open item out of `pending` must, in
the same diff, update the Done-when of every work item open in its PARENT tree
whose `needs` cites that item, or close or remove that row
(`ruling_sync_lines`). It reads one commit and its parent and nothing further,
so it never skips for missing history; the pre-commit hook asks it of HEAD and
the staged tree (`staged_ruling_sync_lines`), and the merge slot of every lane
commit and its first parent (`commit_ruling_sync_lines`) — one function over
two trees in both places. It decides only that mechanical condition: whether
the change carries the ruling, and whether a row's other fields must move, is
the reviewer's judgement.

The same rule couples the owner's OVERRULE of a delegated decision to work
(WI-818): a commit that sets a decisions-record entry `owner = "overruled"`
must, in the same diff, file or amend a queued or active work item whose spec
cites the entry (`overrule_sync_lines`, read by `ruling_sync_lines`, so both
places ask it with no second step or rung).

TEXT THEN ACT (WI-806; OI-101 Q2, amended for landings by the owner's README
Q-8 answer) is the fourth: a commit that writes the approval record changes, as
its own, no cell of an approval-act row but `Status` and adds or removes no row
(`text_then_act_lines`), so amend-plus-flip is no longer approval. The hook
asks it of the staged tree (`staged_text_then_act_lines`, a squash landing
judged by the commits it folds in) and the merge slot of each lane commit
(`commit_text_then_act_lines`); both share the ruling sync's parent reader.
"""

import tomllib
from pathlib import PurePosixPath

try:
    import spine_carrier
    from kitlib import authority as _kitauthority
    from kitlib import decisions as _kitdecisions
    from kitlib import git as _kitgit
    from kitlib import registry as _kitregistry
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier
    from kitlib import authority as _kitauthority
    from kitlib import decisions as _kitdecisions
    from kitlib import git as _kitgit
    from kitlib import registry as _kitregistry
    from kitlib import spine as _kitspine

# `git -C <root> <args>` stdout on success, else None (git absent, not a repo,
# no such object). Every scan below degrades to None so the whole tier is a
# silent no-op outside a git checkout. The alias — rather than a body — is the
# `check.py` idiom: `kitlib.git` is the declared one home for this pattern, and
# the `stdin` batch argument that used to make this look like a different
# function is a parameter there since WI-521 slice 1.
_git = _kitgit.git_out


# The three spine registries the first-approval mint (`staged_drafted_rows`),
# the test-first walk and the retired flip read, each with its id column. The
# amend-without-flip warn (WI-316) and the amendment mint read this set until
# WI-791; extending them to needs was "its own decision rather than a side
# effect", and OI-100 (ruled 2026-10-03) made it — so they read the sibling
# `AMENDMENT_CSVS` below, and this constant keeps its three tiers for the
# readers whose scope did not move. The approval-act readers below are a
# different question and DO cover SN — `APPROVAL_ACT_CSVS`.
SPINE_CSVS = (
    ("docs/requirements/system-requirements.toml", "SR-ID"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID"),
    ("docs/test/test-cases.toml", "TC-ID"),
)

# THE APPROVAL-ACT RUNG'S OWN SET: the spine three PLUS the need tier
# (WI-572 REVIEW-A round 028). SN is a SPINE tier — `spine_carrier.SPINE_TABLE`
# names it, its rows carry the same `status` vocabulary, and the DevStg-Reqs
# rung the human-approval dial holds for the owner is exactly the SN half — so a
# lane flipping `SN-###` Drafted -> Approved is the WORST case of the act the
# owner's 2026-09-01 ruling moved to the adjudicator, not an exempt one. It was
# excluded only by the older section-as-state reading recorded at
# `baseline_snapshot._claims_approval`, which the `status` cell retired.
#
# A SEPARATE CONSTANT rather than a widened `SPINE_CSVS` because the two
# questions have different scopes on purpose: `SPINE_CSVS` is the amendment
# warn's and the intake mint's universe (`intake.py`, `check_trajectory.py`
# re-export), and silently widening those is the side effect the comment above
# refuses. Only the refusal walk reads this one.
#
# THE ASSUMPTIONS REGISTRY'S TWO TIERS JOIN IT (SR-191, SR-192). An assumption
# or a surrogate is approved content recorded like every other, and approving
# one means reading the requirements that rely on it, which one lane does not
# hold: a lane's merge approving one is refused, and the act that does approve
# one rides its own reviewed commit.
# Implements: SR-191, SR-192, LLR-220
APPROVAL_ACT_CSVS = SPINE_CSVS + (
    ("docs/requirements/stakeholder-needs.toml", "SN-ID"),
    ("docs/requirements/assumptions.toml", "DA-ID"),
    ("docs/requirements/assumptions.toml", "SUR-ID"),
)

# THE OTHER SIDE OF THAT BOUNDARY, DECLARED RATHER THAN LEFT AS AN ABSENCE.
# `baseline_snapshot.SNAPSHOTTED` names eight registries whose `Status` a
# snapshot anchors; `APPROVAL_ACT_CSVS` above names the five the refusal walks.
# The remaining three are OUT OF SCOPE OF THE APPROVAL-ACT RUNG, and that is a
# ruling rather than an oversight: the interface, external-frame and component
# registries are OFF-SPINE, their approval cells are governed by OI-30 D3, and
# the 2026-09-01 ruling scopes this rung to SPINE rows — so a lane moving an
# interface, frame or component row's `status` is not performing the act
# `lane_approval_refusal` refuses, and widening to them is OI-30's call.
#
# WHY A CONSTANT AND NOT A COMMENT. The hazard the review named is a tier that
# joins `SNAPSHOTTED` and reaches NO approval reader — silently, because these
# two lists sit hundreds of lines apart in different modules. Naming the
# exclusions makes the two sets a closed statement:
# `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT`, pinned by
# `tests/test_acceptance_record.py`. A new tier therefore cannot be added
# without landing on one side or the other by a deliberate edit.
# THE AMENDMENT WALK'S UNIVERSE (OI-100 gap 1, ruled 2026-10-03; WI-791): every
# tier an approval act can bless. An amendment is text moving away from its
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
# about exactly the rows the merge will route to an adjudicator. The hat arm
# stays structurally silent on these tiers: none carries `Hat-Refs`.
# Implements: SR-178, LLR-158
AMENDMENT_CSVS = APPROVAL_ACT_CSVS

OUTSIDE_THE_APPROVAL_ACT = (
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


def _spine_rows_at(root, rev_prefix, rel_path, id_col):
    """{id: row} of a spine registry on ONE side of the two-tree scan, read
    through whichever carrier that side actually uses — TOML first, CSV as the
    fallback. `rev_prefix` is a `git show` prefix: `"HEAD:"`,
    `"abc123:"`, or `":"` for the index.

    Each side resolves independently, and that is the point rather than a
    convenience: across the cutover commit the old side is CSV and the new side
    is TOML, so this scan compares the two carriers CELL FOR CELL and reports
    any row whose approved text did not survive. The carrier change is then not
    exempt from the amendment guard — it is checked by it, independently of the
    converter's own round-trip proof. A silent-no-op degrade (`{}`) is kept for
    a side that has neither carrier, which is the pre-registry history case."""
    for cand in _spine_carriers(rel_path):
        text = _git(root, ["show", rev_prefix + cand])
        if text is None:
            continue
        rows = spine_carrier.rows_from_text(text, id_col, "." + cand.rsplit(".", 1)[1])
        if rows is None:
            continue  # unreadable is not empty — try the other carrier
        return {rid: row for rid, row in rows.items() if not str(rid).endswith("-000")}
    return {}


# The §A5.1 cell split (OWNER RULING 2026-07-31, docs/concurrency-v2.md; WI-380).
# Only what is APPROVED arms the re-attest warn. Traceability is TRACED, not
# approved: re-pointing an LLR at the module the code moved to amends no
# attested prose. WI-280 paid for the conflation — 19 `Module` cells followed
# moved code -> 11 owning SRs flipped off `Approved` -> the gate dropped DevStg-Impl->DevStg-Tests -> a
# approve brief and four review rounds, for a change that altered no requirement.
#
# BOTH halves are declared per registry, and the RESIDUAL RULE FAILS SAFE: a
# column in neither set is treated as APPROVED. A column added to a registry
# after this table was written can therefore only ever be too loud — a spurious
# window someone sees and dismisses — never silently un-approved, which would
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
# re-attest window directly. Classifying it approved instead would arm a window
# on every row of the re-tier campaign, which is the noise that gets a window
# ignored — and the campaign's re-statements touch `Requirement` anyway, which
# IS approved, so nothing escapes attestation by this choice.
#
# `Hat-Refs` (SR and LLR) joins the TRACED half at WI-484, and the classification
# is the load-bearing half of shipping the cell rather than a footnote. Three
# reasons, in the order that decides it: (1) it is the same SHAPE of pointer as
# `SN-Refs`/`Boundary-Refs` — which declared row in another registry bears on this
# one — carrying no prose either side; (2) the residual would classify it APPROVED,
# so the phase-2 backfill would arm a re-attest window on every row it touched,
# which is precisely the 148-row noise `Boundary-Refs` was classified out of; and
# (3) the owner's own sequencing note prices this ruling — the cell "is NOT
# anticipated to be an attested cell, so it can be tacked on AFTER the sitting
# without re-opening anything signed", which is only true if it is classified here.
# It is deliberately NOT in `intake.ROUTED_TRACED_CELLS`: re-pointing `SN-Refs`
# may have moved SCOPE, which is a judgement adjudication exists to make, while a
# hat re-point restates which lens the row is attributable to and moves no
# obligation. If phase 5's amend-without-flip arm ever wants that routing, it is
# one line — added on evidence, not in advance.
#
# THE ASSUMPTION TIER'S POINTERS JOIN IT (LLR-225), on the same argument: a
# requirement's `DA-Refs` and a test case's `Assumption-Refs` name rows in
# another registry, and a need's `Stakeholder-Refs` and `Source` name the
# stakeholders it serves and the document it was drawn from. Each re-points
# without moving anything the row asserts.
# Implements: SR-189, SR-190, SR-193, SR-197, LLR-225
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
        }
    ),
    # `SR-Refs` is here BY RULING (WI-388, closing WI-380 REVIEW-A finding 3 —
    # the cell §A5.1 left unclassified): it is the same shape of pointer as
    # the ruled-traced `SN-Refs`/`Verifies` — which SR owns this decomposition
    # row — and re-pointing it changes no attested prose on either side.
    # Whether the re-point moved scope is exactly the judgement the
    # adjudication kind exists to make, so a changed `SR-Refs` ROUTES to
    # adjudication (intake.ROUTED_TRACED_CELLS) like its two siblings; it
    # never arms a re-attest window directly.
    "docs/requirements/low-level-requirements.toml": frozenset(
        {
            "Module",
            "CodeSymbol",
            "TestRefs",
            "Component",
            "Phase",
            "SR-Refs",
            "Hat-Refs",
        }
    ),
    "docs/test/test-cases.toml": frozenset(
        {"Verifies", "Evidence", "Automated", "Phase", "Assumption-Refs"}
    ),
    "docs/requirements/stakeholder-needs.toml": frozenset(
        {"Stakeholder-Refs", "Source"}
    ),
}
# The approved half. (The SR tier's `SupersededBy` column — approved by ruling
# at WI-388 — retired with the supersession tombstone class, D-4 ruling
# 2026-08-14b; the CMP registry's own SupersededBy is a separate, still-owed
# item.) The assumption tier's STATEMENTS join it by name rather than by the
# residual (LLR-225): a requirement's `Coincident` waiver and `Form`, and a test
# case's declared `Inputs`, `MaxAge`, `Sampling`, `SampleSize` and
# `AcceptanceRule`, each a claim the row makes. `Delivered-With` joins the
# approved half under LLR-222: changing which siblings jointly deliver the need
# changes the requirement's own argument, rather than merely re-pointing trace.
# An observation case's cadence cells `Trigger`, `Rubric` and `MinWorkItems`
# join by name too (WI-784), keeping the residual's reading: like `MaxAge` and
# `Inputs`, each states how the row's claim is judged or kept current.
# Implements: SR-193, SR-194, SR-198, LLR-222, LLR-225
SPINE_APPROVED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset(
        {
            "Title",
            "Requirement",
            "Rationale",
            "AcceptanceCriteria",
            "Permutations",
            "Priority",
            "Verification",
            "Delivered-With",
            "Coincident",
            "Form",
        }
    ),
    "docs/requirements/low-level-requirements.toml": frozenset(
        {"Title", "Detail", "Rationale"}
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
# off-spine registry declared one, so every off-spine cell counted as approved
# through the residual. Two cells are pointers: an interface's `BridgedBy`
# names the assumptions bridging it, and an assumption's `ObstacleHats` names
# the perspectives its obstacle came from. Every other off-spine cell stays
# approved content (an interface's `Coincident`, a stakeholder's name,
# description and party, a crossing's `System`, an entity's `Mediates`, and the
# rest of the assumption and surrogate cells), because each states something
# the row asserts rather than pointing at another row.
# Implements: SR-211, SR-214, LLR-225
OFFSPINE_TRACED_CELLS = {
    "docs/requirements/interfaces.toml": frozenset({"BridgedBy"}),
    "docs/requirements/assumptions.toml": frozenset({"ObstacleHats"}),
}


def spine_cell_class(csv_path, column):
    """`"traced"` for a column §A5.1 rules traceability, else `"approved"`.

    The residual is deliberate and fails SAFE: an unclassified column — one
    added to a registry after the ruling — reads as approved and keeps arming
    the warn. See SPINE_TRACED_CELLS.

    KEYED BY THE REGISTRY, NOT BY ITS FILENAME. The two tables above are keyed
    on paths that carry a carrier SUFFIX, and the callers do not agree on which
    one: a staged-diff scan names whichever file git reported, while a live read
    names the constant. Under the CSV carrier a `.toml`-keyed lookup misses, and
    a miss here does not red — every column reads `approved`, so a traced-only
    edit arms a re-attest window that was ruled not to. `stem` drops the suffix,
    which is what `spine_carrier` exists to make possible.

    Implements: SR-178, LLR-158
    """
    return "traced" if column in traced_cells(csv_path) else "approved"


def traced_cells(csv_path):
    """The §A5.1 traced column set declared for this registry, carrier-suffix
    insensitive — `frozenset()` for a registry that declares none.

    Extracted from `spine_cell_class` (its own body, unchanged) because a second
    caller needs the SET rather than one column's class: the Hat-Refs arm below
    asks whether this TIER carries the column at all, which a per-column class
    cannot answer (an absent column classes `approved`, the fail-safe residual,
    and would make every TC amendment warn about a cell that tier does not
    have)."""
    key = spine_carrier.stem(csv_path)
    tables = SPINE_TRACED_CELLS | OFFSPINE_TRACED_CELLS
    traced = {spine_carrier.stem(k): v for k, v in tables.items()}
    return traced.get(key, frozenset())


# --- the §A5.1 cell comparison ------------------------------------------------
# WHAT WAS HERE AND WHY IT IS GONE (owner directive 2026-08-15). SN-029's digest
# engine — `normative_text`, `sn_normative_text`, `digest`, `current_digests` and
# their two exclusion sets — lived here for ~107 lines, reserved for an on-row
# `TextHash`/`HashedOn` writer (repo-lock D-1's anchor half) that was never
# built. That half is RULED unnecessary complexity: an approval now records what
# it blessed by COPYING the registries to `docs/archive/last_approved/`
# (`baseline_snapshot.py`), and a copy needs no canonical text to hash, no
# separator that cannot occur in a cell, and no second exclusion list.
#
# `split_changed_cells` below is what survived, and it is the better half: it
# answered the same question the digest did — which cells moved, approved or
# traced — while also returning the before/after pairs a brief has to render
# anyway. It is PUBLIC because `baseline_snapshot.is_drifted` reads it as the
# drift basis, so the snapshot comparison and the amend-without-flip warn can
# never disagree about what "normative" means.

# The Status values whose ROW TEXT is approved — the population the
# amend-without-flip guard scans. ONE MEMBER SINCE D-9 STEP 5, and it is a
# CONTRACTION OF SPELLING, NOT OF SCOPE: the set used to hold `verified` and
# `planned` because the pair split one rung ("text blessed, evidence
# established" vs "text blessed, evidence pending"), and OI-30 D1 folded them
# into the single `Approved`. `Drafted` does not belong: nothing has been
# blessed, so there is nothing to amend behind a human's back. `Founded`
# does not either, and its exclusion is DELIBERATE rather than pending: the rung
# is COMPUTED from a row's children existing, so a cell reading it is not a
# second attestation of the row's own text — the `Approved` claim underneath it
# is the one this guard watches. Lowercase, matching the guard's own
# normalisation.
# (`Modified` used to be listed here as excluded-because-the-marker-is-already-set;
# it retired at D-9 step 7 and the exclusion retired with it.)
# Implements: SR-178, LLR-158
_APPROVED_TEXT = frozenset({"approved"})


def split_changed_cells(csv_path, id_col, head, row):
    """One row's changed cells, split into the §A5.1 halves with their
    before/after: `{"approved": {cell: (before, after)}, "traced": {...}}`.
    The id column and `Status` are not content (the id is the join key; Status
    is the flip the caller is asking about), so neither is compared.

    Implements: SR-178, LLR-158
    """
    changed = {"approved": {}, "traced": {}}
    for key in set(head) | set(row):
        if key in (id_col, "Status"):
            continue
        before, after = (head.get(key) or ""), (row.get(key) or "")
        if before != after:
            changed[spine_cell_class(csv_path, key)][key] = (before, after)
    return changed


def _spine_revs(root, base, head, touches=()):
    """`(changed-paths, old-prefix, new-prefix)` for the two trees the spine scan
    compares, or None when git cannot answer (the silent-no-op degrade).

    The prefixes are `git show` arguments: `"HEAD:"`, `"abc123:"`, or `":"` for
    the INDEX. `head=None` means the index — the `--staged` hook case, and the
    default. Any other value is a commit-ish, which is what §A5.2's trigger
    needs: adjudication is minted from *a trunk commit that changed an approved
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
    approval-act reader passes `APPROVAL_ACT_CSVS`, which adds the SN tier. The
    parameter exists so the two scopes are one walk with one set of carrier and
    `--no-renames` rules rather than two walks that could drift.

    Extracted at WI-572 rather than copied: that row's lane refusal and its
    first-approval trigger ask two more questions of the SAME diff
    `staged_spine_amendments` already reads (which rows FLIPPED, which arrived
    `Drafted`), and a second walk would be a second place for the
    `--no-renames`/carrier-resolution/`-000` rules to drift out of agreement.
    Yields nothing when git cannot answer or nothing relevant moved — the
    silent-no-op degrade `_spine_revs` owns."""
    revs = _spine_revs(
        root,
        base,
        head,
        touches=sorted(c for p, _ in registries for c in _spine_carriers(p)),
    )
    if revs is None:
        return
    staged_names, old_rev, new_rev = revs
    for csv_path, id_col in registries:
        # The record names the carrier file that ACTUALLY changed, not the
        # constant: the constant carries a suffix, and reporting
        # `system-requirements.toml` for a repo whose staged diff touched
        # `system-requirements.csv` names a file that does not exist — in a
        # record an adjudication row quotes back to a human.
        touched = [c for c in _spine_carriers(csv_path) if c in staged_names]
        if not touched:
            continue
        before_rows = _spine_rows_at(root, old_rev, csv_path, id_col)
        after_rows = _spine_rows_at(root, new_rev, csv_path, id_col)
        yield touched[0], id_col, before_rows, after_rows, csv_path


def _claims_approval(row):
    """True when a spine row's `Status` claims approval or above.

    The vocabulary's one home is `kitlib.spine`; this names the PAIR (`Approved`
    and the computed `Founded` above it) so the approval-act readers below ask
    one question instead of each restating which rungs count as blessed. Note
    the deliberate difference from `_APPROVED_TEXT`, three hundred lines up:
    that set is the amend-without-flip guard's, and excludes `Founded` because a
    computed rung is not a second attestation of the row's own text. Here the
    question is "does this cell CLAIM approval", and `Founded` does."""
    return _kitspine.is_approved(row) or _kitspine.is_founded(row)


def _approval_act(registry, rid, before, row):
    """The approval act ONE row performs across the two sides, or None.

    The per-row half of `staged_approval_acts` below, extracted so the walk
    around it is "visit every row of every changed registry" and the judgement
    is stated once, in one place, for both shapes. The two arms answer the same
    question from two directions — text that was never blessed is now blessed —
    and reading them side by side is how the mirror in that docstring stays
    checkable.

    An id-less row is not a row (the `-000` template placeholder and a blank
    key both land here); a de-approval and an unchanged status both fall
    through to None, which is the subtraction that docstring states."""
    if not rid:
        return None
    if before is None:
        # A row absent on the base side. `before_rows` is `{}` for a newly
        # ADDED registry too, which is why the born arm still answers there: a
        # registry that arrives with approved rows in it is the same
        # unblessed-text-now-blessed event.
        if not _claims_approval(row):
            return None
        act, was = "born", ""
    elif not _claims_approval(before) and _claims_approval(row):
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


def staged_approval_acts(root, base="HEAD", head=None):
    """Every APPROVAL ACT a spine delta performs between two trees:

        [{"registry": <carrier path>, "id": <row id>, "act": "flip" | "born",
          "before": <status>, "after": <status>}]

    An act is a row crossing INTO an approval claim (`act = "flip"` — `Drafted`
    → `Approved`/`Founded`) or a row that ARRIVES already claiming one
    (`act = "born"`, absent on the base side). Both are the same event seen from
    two directions: text that was never blessed is now blessed, and the
    `docs/archive/last_approved/` copy that anchors it is owed.

    THE READING IS THE MIRROR OF `staged_spine_amendments`, deliberately: that
    one reports rows whose approved text moved while Status stood still and
    EXEMPTS a moved Status ("a deliberate call this does not second-guess"); this
    one reports THE EXEMPTED SET MINUS THE DE-APPROVALS. The two share
    `_spine_row_sides` so they cannot disagree about which rows exist, and the
    subtraction is stated rather than left to the reader because a mirror
    claiming to be exact and then carving out a case is two sentences that
    disagree.

    A DE-APPROVAL IS NOT AN ACT, and that is the subtraction. `Approved` →
    `Drafted` withdraws a claim; it blesses nothing, so it owes no snapshot and
    refuses no merge. It is not dropped on the floor either — `staged_drafted_rows`
    reports it as an amended `Drafted` row, so the first-approval mint raises the
    re-approval it now owes. Same direction as
    `baseline_snapshot._approval_transition`, which asks the live-vs-snapshot
    form of this question.

    ITS UNIVERSE IS `APPROVAL_ACT_CSVS`, the four SPINE registries — SN, SR,
    LLR, TC — and the assumptions registry's two tiers, and not `SPINE_CSVS`,
    which is the amendment warn's three. SN is
    covered because it is a spine tier carrying the same `status` vocabulary and
    is the half of DevStg-Reqs the human-approval dial holds, so a lane flipping
    a need is the worst case of this act rather than an exempt one (round 028).
    The three OFF-SPINE registries stay out; see `OUTSIDE_THE_APPROVAL_ACT`.

    Owner ruling 2026-09-01 (WI-572): the act this reports is the ADJUDICATOR's,
    performed on the serial trunk side. `approval_delta` directly below reads it
    ONCE for `merge_approval_refusal`, which applies either the ordinary-lane ban
    or the adjudication row's recorded scope at `integrate._approval_act_refusal`
    — this reader does not itself cross the `IF-091` seam, and the seam does not
    declare that it does.

    Returns [] when not applicable; any missing git context is a silent no-op,
    like `staged_spine_amendments`."""
    out = []
    for registry, _id_col, before_rows, after_rows, _csv in _spine_row_sides(
        root, base, head, APPROVAL_ACT_CSVS
    ):
        for rid, row in after_rows.items():
            act = _approval_act(registry, rid, before_rows.get(rid), row)
            if act:
                out.append(act)
    return out


def rows_at(root, rev, rel_path, id_col):
    """`{id: row}` of one spine registry at commit `rev`, or `{}` when the
    registry is absent there under either carrier — `_spine_rows_at`, the row
    reader behind every two-tree scan in this module, offered for a walk along
    history (`check_test_first.first_approval_commits`).

    Public so a history reader parses a row the way the approval-act refusal
    does, through the same carrier resolution and the same `-000` filter,
    rather than growing a second reader of the registries at a revision."""
    return _spine_rows_at(root, rev + ":", rel_path, id_col)


def approval_acts_between(registry, before_rows, after_rows):
    """The approval acts `after_rows` perform against `before_rows`, in
    `staged_approval_acts`' record shape: every row that crossed into an
    approval claim (`flip`) or arrived already making one (`born`).

    THE HISTORY FORM OF THE SAME RULE. `staged_approval_acts` reads its two
    sides from two trees; a walk along trunk carries each commit's rows forward
    as the next commit's before side, so it asks the question of two row maps
    instead and reads each registry once per commit that touches it. The act
    itself is `_approval_act` in both, so the history and the lane refusal
    cannot disagree about which change blessed a row."""
    acts = []
    for rid, row in after_rows.items():
        act = _approval_act(registry, rid, before_rows.get(rid), row)
        if act:
            acts.append(act)
    return acts


# How `git diff --name-status` letters read as the ACT a branch performed on the
# snapshot. Worded from the letter rather than assumed, because the record is
# read by a human deciding why their merge stopped, and a branch that DELETES a
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


def approval_delta(root, base, head):
    """`(row acts, worded snapshot acts, refusal)` for one merge delta."""
    acts = staged_approval_acts(root, base, head)
    out = _git(
        root, ["diff", "--name-status", "--no-renames", base, head, "--", SNAPSHOT_DIR]
    )
    if out is None:
        return (
            [],
            [],
            (
                "cannot read {}'s {} delta against {}, so whether this branch wrote "
                "the approval record is unknowable; nothing was merged".format(
                    head, SNAPSHOT_DIR, str(base)[:10]
                )
            ),
        )
    return acts, sorted(_snapshot_acts(out)), None


def first_approval_scope(metas):
    """The typed scope of claimed first-approval rows, or None for another kind."""
    first = [meta for _name, meta in metas if meta.get("brief") == "first-approval"]
    if not first:
        return None
    values = [meta.get("adjudicates") for meta in first]
    if any(not isinstance(value, list) for value in values):
        return frozenset()
    return frozenset(
        str(rid).strip() for value in values for rid in value if str(rid).strip()
    )


def adjudication_approval_refusal(scope, delta):
    """Refuse a first-approval act that exceeds its recorded row scope."""
    acts, snapshot_files, refusal = delta
    if refusal:
        return refusal
    if not scope:
        return (
            "first-approval adjudication declares an EMPTY `Adjudicates` scope; "
            "the merge cannot know which rows its approval act may reach; nothing "
            "was merged"
        )
    outside = [act for act in acts if act["id"] not in scope]
    acted_registries = {act["registry"] for act in acts}
    written = {
        line.partition(" ")[2][len(SNAPSHOT_DIR) + 1 :] for line in snapshot_files
    }
    snapshot_registries = written - SNAPSHOT_OWN_FILES
    widened = sorted(snapshot_registries - acted_registries)
    missing = sorted(acted_registries - snapshot_registries)
    if not outside and not widened and not missing:
        return None
    lines = [
        "  {} is OUTSIDE `Adjudicates` scope ({})".format(
            act["id"], ";".join(sorted(scope))
        )
        for act in outside
    ]
    lines += [
        "  snapshot WIDENED to {} without an approved row".format(r) for r in widened
    ]
    lines += [
        "  {} was approved WITHOUT its anchoring snapshot".format(r) for r in missing
    ]
    # THE REMEDY, PER ARM. The three lines above say what the delta did; a
    # session reading only those learns it is stopped and not what to do — and
    # the WIDENED arm in particular is reached by following the brief exactly
    # (its `--approves` is fixed before the verdict, so a batch that returns a
    # registry's rows in full still names it). Each arm's repair is stated
    # where the stop is read.
    return (
        "first-approval adjudication exceeds the approval act recorded on its "
        "`Adjudicates` row: the merge admits only scoped flips and exactly their "
        "registry snapshots; nothing was merged:\n{}\nRemedy — WIDENED: "
        "`--approves` named a registry this act flipped nothing in (its rows "
        "were all RETURNED); drop that token and re-take the snapshot, so the "
        "copy blesses only text this act approved. WITHOUT ITS ANCHOR: the flip "
        "landed with no copy behind it; add that registry to `--approves`. "
        "OUTSIDE SCOPE: the row is another adjudication's; restore its `Status` "
        "byte-exact.".format("\n".join(lines))
    )


def merge_approval_refusal(root, base, head, metas, adjudication, *, trunk):
    """Apply one derived approval delta to its actor's authorization rule: an
    adjudication's flips to its first-approval scope, and its re-attestations
    to its amendment scope (`reattest_scope_refusal`) and, on a rung `trunk`'s
    dial holds, to the CLARITY verdict the act names (`held_reattest_refusal`).
    `trunk` is the commit the merge lands on: the authority the act lands under,
    which the merge base is not once trunk has moved since the lane forked."""
    delta = approval_delta(root, base, head)
    if adjudication:
        refusal = reattest_scope_refusal(
            root, base, head, metas, delta
        ) or held_reattest_refusal(root, trunk, base, head, delta)
        if refusal:
            return refusal
        scope = first_approval_scope(metas)
        if scope is not None or delta[0]:
            return adjudication_approval_refusal(scope or frozenset(), delta)
        return delta[2]
    return lane_approval_refusal(root, base, head, delta)


def amendment_scope(metas):
    """The rows the claimed AMENDMENT adjudications ruled: the union of their
    `Adjudicates` cells, empty when none is claimed. A first-approval row's
    scope is its flips, not a re-attestation's.

    Implements: SR-178, LLR-278"""
    return frozenset(
        str(rid).strip()
        for _name, meta in metas
        if meta.get("brief") == "amendment"
        and isinstance(meta.get("adjudicates"), list)
        for rid in meta["adjudicates"]
        if str(rid).strip()
    )


def _ledger_acts(root, rev):
    """The act ledger's `[[act]]` entries at `rev`, `[]` where it is absent, or
    None when it does not parse (IF-220 is the ledger's shape)."""
    text = _git(root, ["show", "{}:{}/{}".format(rev, SNAPSHOT_DIR, SNAPSHOT_ACTS)])
    if text is None:
        return []
    try:
        acts = tomllib.loads(text).get("act", [])
    except tomllib.TOMLDecodeError:
        return None
    return acts if isinstance(acts, list) else None


def reattested_between(root, base, head):
    """`(ids, refusal)`: the row ids the act-ledger entries `head` added over
    `base` re-attested, or a refusal naming the ledger when either side does
    not parse. An entry is added when its `seq` is not in `base`'s ledger.

    Implements: SR-178, LLR-278"""
    before, after = _ledger_acts(root, base), _ledger_acts(root, head)
    if before is None or after is None:
        return frozenset(), (
            "the act ledger {}/{} does not parse at {}, so which rows this "
            "merge re-attests is unknowable; nothing was merged".format(
                SNAPSHOT_DIR, SNAPSHOT_ACTS, base if before is None else head
            )
        )
    seen = {act.get("seq") for act in before if isinstance(act, dict)}
    return frozenset(
        str(rid)
        for act in after
        if isinstance(act, dict) and act.get("seq") not in seen
        for rid in act.get("reattested") or []
    ), None


def _wrote_ledger(delta):
    """Did the approval delta write the act ledger? A re-attestation moves no
    cell, so the ledger entries are the only trace of one."""
    return any(line.endswith("/" + SNAPSHOT_ACTS) for line in delta[1])


def reattest_scope_refusal(root, base, head, metas, delta=None):
    """Refuse an adjudication's act re-attesting a row outside the `Adjudicates`
    scope of the amendment rows it claims — by name — or None.

    A re-attestation moves no cell, so the flips the first-approval arm
    judges cannot show it; the act ledger names the rows each act re-attested,
    and the entries the merge adds are the acts this branch took. An amendment
    row's scope is the rows its verdict ruled, so re-anchoring any other row
    re-blesses text nobody judged. A lane claiming no amendment row has no
    re-attestation scope at all. Only read when the delta wrote the ledger.

    Implements: SR-178, LLR-278"""
    if not _wrote_ledger(delta or approval_delta(root, base, head)):
        return None
    ids, refusal = reattested_between(root, base, head)
    if refusal:
        return refusal
    scope = amendment_scope(metas)
    outside = sorted(ids - scope)
    if not outside:
        return None
    return (
        "the adjudication's act re-attests rows OUTSIDE the `Adjudicates` scope "
        "of its amendment row(s) ({}); nothing was merged:\n{}\nRemedy: a "
        "re-attestation re-anchors text as judged, so it names only rows the "
        "amendment ruled. Re-take the snapshot with `--reattests` naming those "
        "rows alone; a drifted row outside them is another act's to judge.".format(
            ";".join(sorted(scope)) or "none claimed",
            "\n".join("  {} re-attested OUTSIDE the scope".format(r) for r in outside),
        )
    )


# The two row tags of an amendment verdict, in the brief's own grammar
# (`prompts/adjudicate-amendment.template.md`): `- [MEANING|CLARITY] <row-id> ...`.
# Read with string methods: this module's import surface is pinned
# (`tests/test_acceptance_record.py`), and one prefix test needs no `re`.
_VERDICT_TAGS = {"- [MEANING]": "MEANING", "- [CLARITY]": "CLARITY"}


def _ruled_row(line):
    """`(word, row id)` for one verdict row line, else None."""
    head = line.strip()
    for tag, word in _VERDICT_TAGS.items():
        rest = head[len(tag) :].split() if head.startswith(tag) else []
        if rest:
            return word, rest[0]
    return None


def verdict_rulings(text):
    """`{row id: "MEANING" | "CLARITY"}` read off an amendment verdict's row
    lines; a row ruled both ways reads MEANING, the brief's fail-toward-meaning
    rule.

    Implements: SR-178, LLR-278"""
    out = {}
    for word, rid in filter(None, map(_ruled_row, (text or "").splitlines())):
        if out.get(rid) != "MEANING":
            out[rid] = word
    return out


def _tier_of(rid):
    """`(registry, id column)` of the amendment-walk tier row `rid` belongs to,
    read off its prefix, or `(None, None)`."""
    return next(
        ((r, col) for r, col in AMENDMENT_CSVS if rid.startswith(col[:-2])),
        (None, None),
    )


def _held_row(dial, rid):
    """Does `dial` hold the rung row `rid`'s tier is approved into? A row of a
    tier the amendment walk does not name is held, the direction every
    authority read fails."""
    rel, _col = _tier_of(rid)
    rung = _kitauthority.rung_for(rel) if rel else None
    return rung is None or _kitauthority.holds_under(dial, rung)


def _below_approval(root, head, rid):
    """Is row `rid` below approval, or absent, at `head`? Such a row carries no
    signature for a CLARITY ruling to carry over (SR-228)."""
    rel, col = _tier_of(rid)
    row = _spine_rows_at(root, head + ":", rel, col).get(rid) if rel else None
    return row is None or not _claims_approval(row)


def _held_row_line(root, head, rid, act, rulings):
    """The refusal line for one held-rung re-attested row, or None: a row below
    approval at the act, an act naming no verdict, or a verdict that does not
    rule the row CLARITY."""
    if _below_approval(root, head, rid):
        return (
            "  {} is below approval (or absent) at the act, so it carries no "
            "signature to re-attest".format(rid)
        )
    if not str(act.get("verdict") or "").strip():
        return "  {} re-attested on a held rung, and act {} names no verdict".format(
            rid, act.get("seq")
        )
    if rulings.get(rid) != "CLARITY":
        return "  {} is not ruled CLARITY by {}".format(rid, act["verdict"])
    return None


def _held_act_lines(root, head, dial, act):
    """The refusal lines for one act entry's held-rung re-attestations, the
    named verdict read at `head` (`_held_row_line` judges each row)."""
    held = sorted(str(r) for r in act.get("reattested") or [] if _held_row(dial, r))
    if not held:
        return []
    verdict = str(act.get("verdict") or "").strip()
    rulings = (
        verdict_rulings(_git(root, ["show", "{}:{}".format(head, verdict)]))
        if verdict
        else {}
    )
    lines = (_held_row_line(root, head, rid, act, rulings) for rid in held)
    return [line for line in lines if line]


def held_reattest_refusal(root, trunk, base, head, delta=None):
    """Refuse an adjudication's act re-attesting a row on a HELD rung unless
    the act names the verdict that ruled the row CLARITY — or None.

    OI-100 gap 2 (ruled 2026-10-03, WI-791) amends ruled decision 2's held arm
    by one case: a CLARITY verdict approves no new text, it records that the
    owner's signature still describes the row, so an independent adjudicator
    session may re-attest it. The act names its verdict (`intake.py snapshot
    --verdict`), so the act ledger records which ruling carried the signature
    over and the owner's surface lists it for audit. A MEANING row stays the
    owner's to sign, and a row below approval carries no signature to carry
    over (SR-228). The dial is read at `trunk`, the commit the merge lands on:
    the merge slot judges a branch before its in-slot refresh, so the merge base
    can predate a hold trunk has since declared (Sol review 1, WI-791). Only
    ledger entries this merge adds are judged, so the owner's own acts on trunk
    never reach this rule. The judgement is the session's: this only records
    and refuses.

    Implements: SR-178, LLR-278"""
    if not _wrote_ledger(delta or approval_delta(root, base, head)):
        return None
    before, after = _ledger_acts(root, base), _ledger_acts(root, head)
    if before is None or after is None:
        return None  # `reattest_scope_refusal` names the unreadable ledger
    dial = _kitauthority.dial_at(root, trunk)
    seen = {act.get("seq") for act in before if isinstance(act, dict)}
    lines = []
    for act in after:
        if isinstance(act, dict) and act.get("seq") not in seen:
            lines += _held_act_lines(root, head, dial, act)
    if not lines:
        return None
    return (
        "the adjudication's act re-attests rows on a rung the dial HOLDS for a "
        "human without a verdict that rules them CLARITY; nothing was merged:\n"
        "{}\nRemedy: on a held rung only a row the session ruled CLARITY is "
        "its own to re-attest, and the act names that verdict (`intake.py "
        "snapshot --reattests <ROW-ID> --verdict <verdict file>`). A MEANING "
        "row is recommended to the owner, never re-attested by a "
        "session.".format("\n".join(lines))
    )


def lane_approval_refusal(root, base, head, delta=None):
    """Why a WORK BRANCH's delta may not merge because it performs an APPROVAL
    ACT — the refusal text, or None when it performs none.

    THE ACT IS THE ADJUDICATOR'S, ON TRUNK (owner ruling 2026-09-01). A worker
    lane AUTHORS `Drafted` SN/SR/LLR/TC rows and AMENDS cell text on any such
    row, including approved ones. In those four spine registries
    (`APPROVAL_ACT_CSVS`) it does not flip a `Status` into `Approved`/`Founded`
    or mint a row already claiming one; it does not write `SNAPSHOT_DIR`. The
    off-spine three (`OUTSIDE_THE_APPROVAL_ACT`) stay outside this rung — their
    approval cells are OI-30 D3's. Two reasons, both the owner's. CONTEXT:
    approving a row means reading its whole chain — the parent SR, the sibling
    LLRs, the tests — which one work item does not hold. CONCURRENCY: two lanes
    touching the spine conflict at merge and the snapshot must not move across
    a workstream, whereas a serial trunk-side act cannot conflict.

    HERE RATHER THAN IN THE MERGE SLOT, on `LLR-178`'s separation — the writer
    must not also be the judge of its own writes, and by the same token the
    coordinator that merges is not the reader that decides what a spine delta
    did. `integrate._approval_act_refusal` supplies the merge base and the rung's
    place in the ladder; the reading and the wording are this module's, beside
    the two-tree walk and the mirror rules they share their material with.

    A DE-APPROVAL IS NOT AN ACT, and neither is an amendment to an approved row:
    the lane may make both, and the amendment adjudication the intake mints at
    this same merge is what judges the second. THE HONEST BOUND is
    `integrate._minted_id_refusal`'s: this defeats the accident and a lane that
    drifts, not a lane that means to — a branch could still write a flip through
    some file nothing here reads.

    Fails closed on an unreadable snapshot delta: an unread diff is not an
    empty one. `staged_approval_acts`' own degrade is the opposite direction
    (silence outside a git checkout) and is deliberate — it is a READER, and the
    refusal that consumes it is where the fail-closed posture belongs.

    Implements: SR-178, LLR-158
    """
    acts, snapshot_files, refusal = delta or approval_delta(root, base, head)
    if refusal:
        return refusal
    if not acts and not snapshot_files:
        return None
    lines = [
        "  {} {} in {}".format(
            act["id"],
            "flipped {} -> {}".format(act["before"] or "(absent)", act["after"])
            if act["act"] == "flip"
            else "was minted born {}".format(act["after"]),
            act["registry"],
        )
        for act in acts
    ]
    lines += ["  {}".format(name) for name in snapshot_files]
    return (
        "{} performs an APPROVAL ACT in its own delta - and the approval act is "
        "the ADJUDICATOR's, on the serial trunk side, never a work lane's (owner "
        "ruling 2026-09-01; PROCESS.md §4). A lane AUTHORS `Drafted` "
        "SN/SR/LLR/TC rows and assumption and surrogate rows, and AMENDS their "
        "cell text; in those registries it does not "
        "flip a `Status` into `Approved`/`Founded` or mint a row already "
        "claiming one, and it does not write {}/. Approving means reading the "
        "row's whole chain, which one "
        "work item does not hold, and a trunk-side act cannot conflict with a "
        "second lane the way this one can. Leave the rows `Drafted`: the "
        "first-approval adjudication minted at this merge is what reads the "
        "chain, flips and takes the snapshot, on trunk. Nothing was "
        "merged:\n{}".format(head, SNAPSHOT_DIR, "\n".join(lines))
    )


def staged_drafted_rows(root, base="HEAD", head=None):
    """Every `Drafted` spine row a delta ADDS or AMENDS between two trees:

        [{"registry": <carrier path>, "id": <row id>, "act": "added" | "amended",
          "changed": {cell: (before, after)}}]

    The first-approval trigger's input (WI-572): a lane authors `Drafted` rows
    and amends their text, and what it hands the adjudicator is exactly this set
    — the rows whose text is now waiting on a first approval nobody has given.
    `changed` is empty on an `added` row (there is no before side to diff) and
    carries BOTH §A5.1 halves on an `amended` one, because below approval the
    split buys nothing: no cell of a `Drafted` row was ever blessed, so none of
    them is "traced-only" relative to a signature.

    A row that is `Drafted` on the after side only. A row that LEFT `Drafted`
    is an approval act (`staged_approval_acts`); every row that ENTERED it is
    reported here as `amended`, even when only Status moved. The withdrawal
    itself still blesses nothing and remains absent from `staged_approval_acts`,
    but the resulting Drafted row now awaits the adjudicator's approval just as
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
            changed = dict(split["approved"])
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

    One record per APPROVED-TEXT spine row (`_APPROVED_TEXT` — `Approved`, into
    which `Verified` and `Planned` both folded at D-9 step 5) amended between the
    two trees without its status moving, each cell sorted into the §A5.1 halves with its before/after:

        {"registry": <csv path>, "id": <row id>,
         "approved": {cell: (before, after)}, "traced": {cell: (before, after)}}

    WHICH TWO TREES is a parameter, and WI-388 needs it to be: `head=None` (the
    default) compares the INDEX against `base`, which is the hook's `--staged`
    question, but §A5.2 mints adjudication from a **trunk commit**, and a commit
    is not the index — `staged_spine_amendments(root, "HEAD~1", "HEAD")` asks
    the post-commit question the dispatcher actually has to ask. Both arms are
    tested.

    A record may carry a traced change with NO approved change. Only the
    `SN-Refs`/`Verifies`/`SR-Refs` subset of those is the WI-388 case (§A5.1
    routes a re-point of what a requirement answers to, what a test claims to
    cover, or which SR owns an LLR — the last ruled traced at WI-388 — to
    adjudication); a `Module`/`CodeSymbol`/`TestRefs`/`Component`/`Phase`
    change is simply silent — traced, not pending, nothing owed. Rows are parsed
    with the csv module over the full file text on each side (spine cells are
    long; never line-split). Returns [] when not applicable; any missing git
    context is a silent no-op, like staged_findings. A NEW row (id absent on the
    base side) is not an amendment; a row whose Status moved (to `Drafted`,
    `Founded`, anything) made a deliberate call this does not
    second-guess — `staged_approval_acts` is the reader for the half of that
    exemption which BLESSES text, over the same walk.

    THE TWO-TREE WALK IS `_spine_row_sides`, shared since WI-572 rather than
    inlined here, so this reader and the two approval-act readers above it
    cannot disagree about which registries and rows the delta contains. Its
    universe is `AMENDMENT_CSVS` since WI-791 (OI-100 gap 1): the need,
    assumption and surrogate tiers join the three spine tiers."""
    # Each row answers for its OWN cells (owner ruling 2026-08-17m): the
    # sanctioned amend path is flipping the AMENDED row itself in the same
    # commit — a Status that moved is exempted below. The retired chain
    # reading's owning-SR exemption (a parent flip sanctioning a silent
    # child amendment) is gone with the doctrine: a child whose approved
    # cells change while its own Status still claims approval warns,
    # whatever its parent does.

    out = []
    for registry, id_col, head_rows, staged_rows, csv_path in _spine_row_sides(
        root, base, head, AMENDMENT_CSVS
    ):
        if not head_rows or not staged_rows:
            continue  # first commit / newly added registry — nothing attested yet
        for rid, row in staged_rows.items():
            changed = _amended_cells(csv_path, id_col, rid, head_rows.get(rid), row)
            if changed:
                out.append(dict(changed, registry=registry, id=rid))
    return out


def _amended_cells(csv_path, id_col, rid, head, row):
    """One row's `split_changed_cells` when it is an AMENDMENT — present on
    both sides, reading the same approved-text Status on both, with a cell
    moved — else None. `staged_spine_amendments`' per-row judgement, extracted
    unchanged at WI-791 to keep the walk under the complexity bar."""
    if not rid or rid.endswith("-000") or head is None:
        return None
    head_status = (head.get("Status") or "").strip().lower()
    cur_status = (row.get("Status") or "").strip().lower()
    # APPROVED-TEXT STATES, both sides, and the SAME one. Since D-9
    # step 5 that is the single value `Approved`; before the fold it was
    # `Verified` OR `Planned`, and requiring the SAME one on both sides
    # is what kept a legitimate rung move from reading as an amendment.
    # A status that MOVED between the two sides is still exempt,
    # unchanged: that is a deliberate call this does not second-guess.
    if head_status != cur_status or head_status not in _APPROVED_TEXT:
        return None
    changed = split_changed_cells(csv_path, id_col, head, row)
    return changed if changed["approved"] or changed["traced"] else None


def staged_spine_findings(root):
    """The amend-without-flip warn (WI-316; warn-first, `--staged` only), scoped
    by WI-380 to APPROVED cells only.

    A staged diff that changes the approved cells of a spine row whose Status
    reads the same approved-text value (`Approved`, since D-9 step 5) in both
    HEAD and the stage has amended attested prose without re-blessing it — the
    write-time discipline the old RE-ATTESTATION-PENDING commit-message prose
    never had. One warning per amended row, naming the changed cells. A row
    whose only changes are TRACED (§A5.1) is silent here by ruling; it still
    appears in `staged_spine_amendments`, which is where WI-388 picks it up.
    Index-vs-HEAD by construction — this is the hook's question, so it takes no
    rev arguments; the post-commit view is `staged_spine_amendments`'s."""
    return [
        "{}: approved cell(s) {} amended while Status stays put — a "
        "post-attestation amendment owes a fresh human read (process.md §7). "
        "Since D-9 step 7 there is no marker to set: either commit the amendment "
        "on its own and re-attest it in the NEXT commit with `intake.py "
        "snapshot --reattests {}` (text first, the act second: a commit that "
        "writes the record changes no other spine cell), or the change rides "
        "as SNAPSHOT DRIFT until the next sitting — "
        "visible on the re-attest brief and open-items.html, but not "
        "blessed".format(a["id"], ", ".join(sorted(a["approved"])), a["id"])
        for a in staged_spine_amendments(root)
        if a["approved"]
    ]


# The perspective cell the arm below watches. ONE NAME, stated once: the column
# is `Hat-Refs` at both tiers that carry it (WI-484 phase 0's ruling), and the
# arm reads `traced_cells` rather than this constant to decide WHICH tiers those
# are, so adding the column to a third registry extends the guard with it.
HAT_REFS_CELL = "Hat-Refs"


def staged_hat_refs_findings(root):
    """THE AMEND-WITHOUT-FLIP GUARD'S SECOND ARM (OI-32 phase 5, OI-33's
    surviving residue) — warn-first, `--staged` only, never an exit code.

    A row whose APPROVED cells moved while its `Hat-Refs` cell did not has been
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
    a `git blame` line time cannot tell an approved cell from a traced one.
    `split_changed_cells` can, so this arm reads it — which is why `Hat-Refs`
    was CLASSIFIED traced at both tiers rather than left to the residual.

    THE BASELINE IS THE ONE THE GUARD IT JOINS ALREADY USES: HEAD versus the
    index, via `staged_spine_amendments`, over rows reading the same
    approved-text Status on both sides. Two consequences, both deliberate and
    both HONEST VACUITY rather than coverage:

      * A row with NO baseline is not guarded. A row absent from HEAD (newly
        minted, this commit) has nothing to compare, and a row below approval
        has blessed nothing to amend behind a human's back — the same population
        rule `staged_spine_amendments` documents, inherited rather than
        re-litigated here.
      * A TIER with no `Hat-Refs` column is silent structurally (the TC tier
        today), not by an allowlist.

    NOT THE `last_approved` SNAPSHOT, and the trade is worth recording: that
    baseline would make the finding STAND until answered, where this one is a
    single warn at the commit that earns it. It was declined on OI-33's own
    timing argument — the party who knows whether the perspectives moved is the
    one making the change, at the moment they make it — and on the ruling's
    words, "same shape, same home, warn-first". The standing half of the same
    question is already carried for APPROVED cells by snapshot drift; if this
    warn is measured to be ignored, promoting it to a drift-tier finding is the
    next rung, on evidence.

    AN EMPTY `Hat-Refs` CELL STILL FIRES. A cell that was never filled and a
    cell deliberately left empty (`SR-015`, `SR-040` — both argued and correct)
    are indistinguishable to a reader, and the guard's question is whether the
    set was RE-EXAMINED, which an unchanged empty cell does not answer.

    Implements: SR-161, LLR-202
    """
    return [
        "{}: approved cell(s) {} amended while {} stayed put — the row's "
        "substance moved and its perspective record did not, so the derived "
        "component/knowledge view keeps answering from the old lenses "
        "(process.md §7; OI-32 phase 5). Re-read the row's hats and either "
        "update {} in this commit or leave it deliberately — an unchanged cell "
        "cannot say which".format(
            a["id"], ", ".join(sorted(a["approved"])), HAT_REFS_CELL, HAT_REFS_CELL
        )
        for a in staged_spine_amendments(root)
        if a["approved"]
        and HAT_REFS_CELL in traced_cells(a["registry"])
        and HAT_REFS_CELL not in a["traced"]
    ]


# The `last_approved` snapshot's root, repo-relative. RESTATED rather than
# imported from `baseline_snapshot`: the import edge runs the other way (that
# module reads `split_changed_cells` from here), and a back-import would make
# the pair un-loadable. One string, pinned equal by
# tests/test_baseline_snapshot.py — the F5 plumbing-duplication sanction, with
# the behavioural pin the D-7 ruling requires.
SNAPSHOT_DIR = "docs/archive/last_approved"

# The snapshot's prose stamp: rendered for a human, PARSED BY NOTHING, and with
# no live counterpart to mirror.
SNAPSHOT_README = "README.md"

# The snapshot's act ledger (`baseline_snapshot.ACTS`, restated for the reason
# the directory is, and pinned equal by tests/test_baseline_snapshot.py): the
# typed record of each approval act, and like the README a file with no live
# counterpart. These two are the snapshot's own files; every other file under
# the root is a registry copy the mirror rules compare with live.
SNAPSHOT_ACTS = "acts.toml"
SNAPSHOT_OWN_FILES = frozenset({SNAPSHOT_README, SNAPSHOT_ACTS})


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

    A bare `intake.py snapshot` is no repair here: it copies only a registry
    the act authorises, so with no `Status` move it copies nothing, and it
    refuses any approved row whose text differs from the recorded copy unless
    `--reattests` names it. So the finding names the two repairs that work:
    put the blessed copy back, or take a fresh act whose arguments carry the
    authority for this registry and name the rows it re-attests. The
    `--approves` token is the registry's STEM: `baseline_snapshot.
    resolve_registry` takes a canonical rel, filename or stem, and a CSV
    carrier's live path is none of those, so the path itself would refuse."""
    return (
        "Repair: restore the copy that was blessed, or take a fresh reviewed "
        'approval act that re-copies it — `intake.py snapshot --approves "{}=<REF>" '
        "--reattests <ROW-ID>[,<ROW-ID>...]`, naming each approved row whose "
        "text differs from the copy; a bare `intake.py snapshot` copies nothing "
        "here or refuses the drift".format(PurePosixPath(live_rel).stem)
    )


def staged_snapshot_findings(root, base="HEAD", head=None):
    """THE MIRROR INVARIANT (snapshot design §F3), as warn strings.

    > In any commit that touches a file under `docs/archive/last_approved/`,
    > that file must be byte-identical to its live counterpart in that same
    > commit.

    The snapshot is the record of what a human blessed, and it is just files —
    nothing about a text file stops someone editing it. This is the guard, and
    it is exact rather than heuristic: a legitimate `copy_live` satisfies it
    ALWAYS, by construction, because the copy is byte-for-byte and rides the
    same commit as the write. FOUR failures fail it — a hand edit (snapshot
    differs from live), a partial copy (one file mirrored, its sibling not), a
    copy-then-amend-live (the copy landed but the live file moved on before the
    commit closed), and a partial DELETION (one registry removed from the record
    while the rest of it stands — added at adversarial round 2, 2026-08-15,
    which found the deletion path exiting silently and so left as an erasure the
    invariant did not watch).

    The consequence worth stating plainly: **the only way to write text into
    the snapshot is to write it into the live registry first** — an approval,
    in a reviewed commit, exactly as ruled.

    Index-vs-HEAD by default (the hook's question); `head` takes a commit-ish
    for the post-commit view, matching `staged_spine_amendments`' shape. Silent
    no-op when git cannot answer or no snapshot file moved — the same degrade
    every other scan here takes.

    **TWO SEVERITIES SINCE D-9 MIGRATION STEP 7, which is what the design asked
    for** (§F3 risk 3: *"warn at the staged hook, ERROR on the integrity
    floor"*). This producer is unchanged and returns plain strings; the
    `--staged` loop below still prints them as warns, AND `trace.py` appends
    them to `findings.integrity`, so they fail `--strict-integrity` — the
    always-on floor the pre-commit hook runs at every gate. The staged warn is
    kept rather than replaced because it is the EARLIER of the two reads: it
    names the file while the author is still in the commit, where the fix is one
    `intake.py snapshot` away. The pre-commit hook invokes the staged pass with
    `|| true`, so the warn alone never blocked anything — which is exactly why
    the arming had to add a second severity rather than raise this one.

    Implements: SR-179, LLR-178
    """
    revs = _spine_revs(root, base, head)
    if revs is None:
        return []
    staged_names, _old_rev, new_rev = revs
    prefix = SNAPSHOT_DIR + "/"
    out = []
    for name in sorted(n for n in staged_names if n.startswith(prefix)):
        live_rel = name[len(prefix) :]
        # The README is PROSE (design §F8) — a stamp for a human, parsed by
        # nothing — and the act ledger is the snapshot's own record of its
        # acts; neither has a live counterpart to mirror. Excluding them by
        # name rather than by "no counterpart exists" keeps a genuinely missing
        # registry loud.
        if live_rel in SNAPSHOT_OWN_FILES:
            continue
        snap_text = _git(root, ["show", new_rev + name])
        live_text = _git(root, ["show", new_rev + live_rel])
        if snap_text is None:
            # DELETED from the snapshot in this commit. Silent ONLY when the
            # whole record went with it — retiring the mechanism, or the
            # wholesale replacement §A1 describes, are both legitimate and
            # neither leaves a hole. A single registry deleted while the rest of
            # the record stands IS a hole, and it is the cheapest possible
            # laundering: `unanchored_findings` reports a row whose copy reads
            # below it, so removing the copy outright removed the evidence
            # instead. (Adversarial round 2, 2026-08-15.)
            if _snapshot_survives(root, new_rev):
                out.append(
                    "{} was DELETED from the {} snapshot while the rest of the "
                    "record still stands — a registry removed from the record of "
                    "what was approved is not a smaller record, it is a missing "
                    "one; the snapshot is replaced WHOLESALE at a signing, never "
                    "trimmed a file at a time".format(name, SNAPSHOT_DIR)
                )
            continue
        if live_text is None:
            out.append(
                "{} is in the {} snapshot but {} does not exist in this commit — "
                "a snapshot file with no live counterpart is a record of text "
                "the repo no longer has".format(name, SNAPSHOT_DIR, live_rel)
            )
        elif snap_text != live_text:
            out.append(
                "{} is NOT byte-identical to {} in this commit — the snapshot is "
                "the record of what a human blessed, so it may only ever be "
                "written by copying the live file (`intake.py snapshot`). A hand "
                "edit, a partial copy and a copy-then-amend-live all land "
                "here. {}".format(name, live_rel, _mirror_repair(live_rel))
            )
    return out


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


def committed_snapshot_findings(root):
    """THE MIRROR INVARIANT OVER THE COMMITTED TREE — the half `staged_snapshot_
    findings` cannot reach (adversarial round, 2026-08-20: ROUND-OPUS CRITICAL-3
    / ROUND-SOL MAJOR-2).

    The staged rule is keyed on a snapshot file being IN THE COMMIT. That makes
    it exact and cheap, and it makes its blind spot exact too: once a forged or
    stale copy has LANDED — hooks bypassed, or a commit made outside them — no
    later run stages a snapshot file, so nothing ever looks at it again. The
    divergence is silent forever, which is the opposite of what a record of what
    a human blessed is for.

    So this asks the same question of history rather than of the index: for every
    file under the snapshot root, **was it a copy of its live counterpart at the
    commit that last wrote it?** That framing is what makes the rule safe to run
    ALWAYS, and the alternative shape — comparing the snapshot to live in the
    WORKING TREE — is the one to refuse: the snapshot is deliberately behind live
    while an amendment is pending, and that lag IS the signal (see
    `baseline_snapshot`'s header). A rule that redded every pending amendment
    would be switched off within a day. Here, live moving on afterwards changes
    nothing: the comparison is pinned to the snapshot's own writing commit, so a
    legitimate copy stays green forever and a forgery stays red forever.

    Blob-identity via `git cat-file --batch-check` rather than two `git show`s
    per file: git names identical content with the identical object id, so
    comparing object ids IS the byte comparison, at two subprocesses total.

    Degrades to `[]` off git, on any git failure, and for an untracked snapshot
    (a scaffold that has committed nothing has no committed state to judge)."""
    revs = _snapshot_write_revs(root)
    if not revs:
        return []
    prefix = SNAPSHOT_DIR + "/"
    pairs, specs = [], []
    for name, rev in sorted(revs.items()):
        if not name.startswith(prefix):
            continue
        live_rel = name[len(prefix) :]
        # The README and the act ledger have no live counterpart, exactly as in
        # the staged rule — excluded by name so a genuinely missing registry
        # stays loud.
        if live_rel in SNAPSHOT_OWN_FILES:
            continue
        pairs.append((name, live_rel, rev))
        specs += ["{}:{}".format(rev, name), "{}:{}".format(rev, live_rel)]
    if not pairs:
        return []
    batch = _git(
        root, ["cat-file", "--batch-check=%(objectname)"], stdin="\n".join(specs) + "\n"
    )
    if batch is None:
        return []
    ids = batch.splitlines()
    if len(ids) != len(specs):
        return []  # unparseable batch: an unanswerable question makes no finding
    out = []
    for i, (name, live_rel, rev) in enumerate(pairs):
        snap_id, live_id = ids[2 * i].strip(), ids[2 * i + 1].strip()
        if snap_id.endswith("missing"):
            # The commit that last named this path DELETED it. That is the
            # staged rule's subject (a partial deletion is caught in the commit
            # that does it) and not a mirror question — there is no copy left to
            # compare.
            continue
        if live_id.endswith("missing"):
            out.append(
                "{} was written into the {} snapshot at {} where {} did not "
                "exist — a snapshot file with no live counterpart in its own "
                "writing commit is a record of text the repo never had".format(
                    name, SNAPSHOT_DIR, rev[:8], live_rel
                )
            )
        elif snap_id != live_id:
            out.append(
                "{} is NOT byte-identical to {} at {}, the commit that last "
                "wrote it — the snapshot is the record of what a human blessed, "
                "so it may only ever be written by copying the live file "
                "(`intake.py snapshot`). This divergence has LANDED. {}".format(
                    name, live_rel, rev[:8], _mirror_repair(live_rel)
                )
            )
    return out


# --- THE HELD STATUS: which status cells a delta moves (SR-208, SR-210) ------
# The approval level names the rungs a human still approves, and the approval
# act above is already refused for the SPINE. The off-spine registries carry
# status cells of their own that no automated path was stopped from changing,
# so a declared hold on their rung was a claim rather than a control. The two
# readers below make it a control: the same two-tree comparison as the spine
# walk, read over the status cell of every row of every off-spine registry, and
# the judgement of the result against a dial. The loop's writers and the merge
# slot refuse on it (`agent_common.loop_held_status_refusal`,
# `integrate._held_status_refusal`); the history check reports on it
# (`check_trajectory.loop_held_status_findings`).
#
# THE UNIVERSE IS DECLARED, separately from the rung map, and that separation
# is load-bearing: a registry here that the map does not name is HELD (an
# unmapped status is one nobody has released), which a universe derived FROM
# the map could never express. The frame carries three tiers in one file and
# the assumptions registry two, so the reader walks every table of the file
# rather than one tier by id column. The off-spine registries are TOML only
# (each was converted, or born, under that carrier), and the example `-000`
# rows are never statuses anyone approved.
#
# THE NEEDS FILE IS SHARED: it carries the stakeholder list (off-spine, so
# here) beside the needs (a spine tier, walked by the spine half of
# `committed_status_moves` through `APPROVAL_ACT_CSVS`). `STATUS_TABLES` narrows
# its read to the stakeholder table, so each tier is read by exactly one walk
# and no need is reported twice; both tiers are judged at the needs rung
# (`kitlib.authority.rung_for`).
NEEDS_REGISTRY = "docs/requirements/stakeholder-needs.toml"
HELD_STATUS_REGISTRIES = (
    "docs/requirements/external.toml",
    "docs/requirements/interfaces.toml",
    "docs/requirements/components.toml",
    "docs/requirements/assumptions.toml",
    NEEDS_REGISTRY,
)
STATUS_TABLES = {NEEDS_REGISTRY: (spine_carrier.OFFSPINE_TABLE["STK-ID"],)}


def _status_cells(text, tables=None):
    """`{row id: status}` of a registry text (of its `tables` only, when named),
    the `-000` example rows dropped (never statuses anyone approved), or None
    when it does not parse: `{}` is a registry with no status rows, None one
    that cannot be read, and the two are opposite claims."""
    cells = spine_carrier.status_cells(text, tables)
    if cells is None:
        return None
    return {rid: status for rid, status in cells.items() if not rid.endswith("-000")}


def _status_delta(path, before_text, after_text):
    """The status moves one registry makes between two sides: a changed cell,
    and a row added or removed WITH a status. A side that does not parse is
    ONE move naming the registry, never an empty delta: a delta nobody can read
    is not a delta that moved nothing."""
    tables = STATUS_TABLES.get(path)
    before = {} if before_text is None else _status_cells(before_text, tables)
    after = {} if after_text is None else _status_cells(after_text, tables)
    if before is None or after is None:
        return [{"registry": path, "id": "(unparseable)", "before": "", "after": ""}]
    return [
        {
            "registry": path,
            "id": rid,
            "before": before.get(rid, ""),
            "after": after.get(rid, ""),
        }
        for rid in sorted(set(before) | set(after))
        if before.get(rid) != after.get(rid)
    ]


def _offspine_status_moves(root, base, head, watched):
    """Every status move in `watched` between the two sides `_spine_revs` names
    (`head=None` is the index)."""
    revs = _spine_revs(root, base, head, touches=watched)
    if revs is None:
        return []
    changed, old, new = revs
    moves = []
    for path in watched:
        if path in changed:
            moves += _status_delta(
                path, _git(root, ["show", old + path]), _git(root, ["show", new + path])
            )
    return moves


def staged_status_moves(root, base="HEAD", head=None, paths=None):
    """Every change to a status cell of an off-spine registry between two trees,
    or between `base` and the index when `head` is None — rows added or removed
    with a status included, as `{"registry", "id", "before", "after"}` (an
    absent side is ""). `head` may be a commit or a TREE: a plumbing writer asks
    about the tree it is about to commit, before any commit names it. `paths`,
    when given, narrows the registries to those among them (a path-scoped
    commit takes nothing else). `[]` when git cannot answer.

    Implements: SR-208, LLR-246
    """
    watched = list(HELD_STATUS_REGISTRIES)
    if paths is not None:
        named = {str(p).replace("\\", "/").strip() for p in paths}
        watched = [p for p in watched if p in named]
    return _offspine_status_moves(root, base, head, watched) if watched else []


def merge_status_moves(root, parents):
    """The status moves a STAGED MERGE RESULT makes of its own: each move of the
    index against the first of `parents` whose new value also differs from
    every other parent's. A status the merged side already carried was judged
    in the commit that made it and arrives with it; a value NEITHER side
    carried - a conflict resolution, a hand edit mid-merge - was written by
    this commit, and is judged here. `[]` when git cannot answer.

    Implements: SR-208, LLR-246
    """
    own = None
    for parent in parents:
        moves = staged_status_moves(root, parent)
        keys = {(m["registry"], m["id"]) for m in moves}
        own = (
            moves
            if own is None
            else [m for m in own if (m["registry"], m["id"]) in keys]
        )
    return own or []


def pending_status_moves(root):
    """The status moves the commit being made in `root` makes of its OWN: the
    index against HEAD, or, while a merge is in progress, `merge_status_moves`
    against HEAD and MERGE_HEAD. Read through git alone. An octopus merge's
    further heads are not read, so a status only they carried reads as the
    merge's own: the held direction.

    Implements: SR-208, LLR-246
    """
    merging = _git(root, ["rev-parse", "-q", "--verify", "MERGE_HEAD"])
    if merging and merging.strip():
        return merge_status_moves(root, ["HEAD", merging.strip()])
    return staged_status_moves(root)


def held_status_lines(dial, moves):
    """One line per move whose registry's rung `dial` holds for a human, naming
    the registry, the row, the move and the rung — THE judgement both the
    refusal below and the history check read, so the two cannot disagree about
    which move is held.

    A registry the rung map does not name is HELD whatever the dial says:
    nobody has ruled which rung governs it, and the only safe answer to that is
    the human's (the `agent_common.human_approves` fail-safe, applied to a
    delta instead of an intent)."""
    lines = []
    for move in moves:
        rung = _kitauthority.rung_for(move["registry"])
        if rung is None or _kitauthority.holds_under(dial, rung):
            lines.append(
                "{} {} {} -> {} (rung {})".format(
                    spine_carrier.stem(move["registry"]).rsplit("/", 1)[-1],
                    move["id"],
                    move["before"] or "(absent)",
                    move["after"] or "(removed)",
                    rung or "unmapped, so held",
                )
            )
    return lines


def held_status_refusal(dial, moves):
    """The refusal naming every move `held_status_lines` holds, or None.

    Implements: SR-208, LLR-246
    """
    held = held_status_lines(dial, moves)
    if not held:
        return None
    return (
        "the loop may not change a status the approval level holds for a human "
        "(human_approval_through = {}): {} - a held status moves only in a "
        "person's own reviewed commit".format(dial, "; ".join(held))
    )


def _empty_tree(root):
    """The empty tree's id in this repository's hash, or None off git — what a
    ROOT commit is compared with."""
    out = _git(root, ["hash-object", "-t", "tree", "--stdin"], stdin="")
    return out.strip() if out and out.strip() else None


def committed_status_moves(root, rev):
    """Every status move `rev` made against its FIRST parent — or against the
    empty tree when it has none — across the spine registries and the off-spine
    ones, in `staged_status_moves`' shape. A merge commit's first-parent delta
    is the merged work's, which is why the history check skips merges and
    visits the merged commits instead.

    Implements: SR-210, LLR-249
    """
    parent = _git(root, ["rev-parse", "--verify", "--quiet", rev + "^1"])
    base = parent.strip() if parent and parent.strip() else _empty_tree(root)
    if base is None:
        return []
    moves = _offspine_status_moves(root, base, rev, list(HELD_STATUS_REGISTRIES))
    for registry, _id_col, before, after, _csv in _spine_row_sides(
        root, base, rev, APPROVAL_ACT_CSVS
    ):
        for rid in sorted(set(before) | set(after)):
            was = ((before.get(rid) or {}).get("Status") or "").strip()
            now = ((after.get(rid) or {}).get("Status") or "").strip()
            if was != now:
                moves.append(
                    {"registry": registry, "id": rid, "before": was, "after": now}
                )
    return moves


# --- THE RULING SYNC: a ruling updates the rows that cite it (WI-790) ---------
# OI-102 Q3, ruled 2026-10-03: a commit-time block over ONE diff, a commit
# against its own parent, with no history walk and no second path. The
# trigger is the registry state (a row going from `pending` to anything else,
# a deleted pending row included), never page membership; the citing set is
# read from the PARENT tree, so dropping the `needs` token in the ruling's own
# commit discharges nothing. Every terminal state discharges the obligation —
# a closed row has no criteria left to update — because a terminal row lives
# under the archive, so a row the commit moved there or removed is satisfied.
OPEN_ITEMS_REGISTRY = "docs/requirements/open-items.toml"
WORK_DIR = "docs/work"
ARCHIVE_WORK_DIR = "docs/archive/work"
_PENDING = "pending"


def _tree_specs(root, rev):
    """`{WI id: path}` of every spec in a tree (`rev` None is the index), or
    None when git cannot list it. A `-000` example is never a row.

    Implements: SR-148, LLR-298
    """
    roots = [WORK_DIR, ARCHIVE_WORK_DIR]
    if rev is None:
        out = _git(root, ["ls-files", "--"] + roots)
    else:
        out = _git(root, ["ls-tree", "-r", "--name-only", rev, "--"] + roots)
    if out is None:
        return None
    specs = {}
    for path in out.splitlines():
        name = path.rsplit("/", 1)[-1]
        wid = "-".join(name.split("-")[:2])
        if name.startswith("WI-") and name.endswith(".md") and not wid.endswith("-000"):
            specs[wid] = path
    return specs


class _UnreadableBlob(Exception):
    """A path its tree lists whose blob git cannot read (a partial clone
    offline, a damaged object store). The ruling sync refuses it by name:
    a failed read is never an absent file (A1)."""


def _show(root, prefix, path):
    """The text of `prefix + path` (`prefix` a `git show` prefix: `"<rev>:"` or
    `":"` for the index), None when the tree does not list the path; raises
    `_UnreadableBlob` when it lists the path but its blob cannot be read.

    Implements: SR-148, LLR-298
    """
    text = _git(root, ["show", prefix + path])
    if text is not None:
        return text
    if prefix == ":":
        listed = _git(root, ["ls-files", "--", path])
    else:
        listed = _git(root, ["ls-tree", "--name-only", prefix[:-1], "--", path])
    if listed is None or listed.strip():
        raise _UnreadableBlob(prefix + path)
    return None


def _registry_states(root, prefix):
    """`{OI id: status}` of the open-items registry in ONE tree (`prefix` a
    `git show` prefix), read through whichever carrier that tree uses (TOML,
    else CSV — `spine_carrier`'s resolution, as `_spine_rows_at` reads a spine
    registry): `{}` when the tree has neither, None when it does not parse.
    `-000` example rows are dropped.

    Implements: SR-148, LLR-298
    """
    for cand in _spine_carriers(OPEN_ITEMS_REGISTRY):
        text = _show(root, prefix, cand)
        if text is None:
            continue
        rows = spine_carrier.rows_from_text(text, "OI-ID", "." + cand.rsplit(".", 1)[1])
        if rows is None:
            return None
        return {
            rid: (row.get("Status") or "").strip()
            for rid, row in rows.items()
            if not str(rid).endswith("-000")
        }
    return {}


def _ruled_items(before, after):
    """The open items `pending` in `before` and not in `after` (two
    `_registry_states` maps), or None when either side does not parse
    (unreadable is not unchanged).

    Implements: SR-148, LLR-298
    """
    if before is None or after is None:
        return None
    return sorted(
        oid
        for oid, state in before.items()
        if state.lower() == _PENDING and after.get(oid, "").lower() != _PENDING
    )


def _citing_rows(root, base, specs, ruled):
    """`[(WI id, [ruled OI ids it cites], spec text)]` for every row OPEN in
    the `base` tree (under `docs/work/`) whose `needs` cites a ruled item.

    Implements: SR-148, LLR-298
    """
    rows = []
    for wid, path in sorted(specs.items()):
        if not path.startswith(WORK_DIR + "/"):
            continue  # under the archive: terminal, nothing owed
        text = _show(root, base + ":", path)
        try:
            data, _body = _kitregistry.parse_spec_frontmatter(text or "", path)
        except ValueError:
            continue  # a malformed spec is the validator's finding, not this rule's
        needs = ";".join(str(t) for t in data.get("needs") or [])
        cited = [o for o in _kitspine.split_pred_edges(needs)[1] if o in ruled]
        if cited:
            rows.append((wid, cited, text))
    return rows


def _sync_gap(root, new_prefix, head_path, before_text):
    """Why one citing row is out of sync in the new tree, or None when it is
    satisfied: removed, closed (moved under the archive), or open with a
    non-empty Done-when section whose RAW text differs from the parent's (A1:
    read from the raw spec text; whether the change carries the ruling is the
    reviewer's judgement, not this rule's).

    Implements: SR-148, LLR-298
    """
    if head_path is None or not head_path.startswith(WORK_DIR + "/"):
        return None
    after = _raw_done_when(_show(root, new_prefix, head_path))
    if not after:
        return "it keeps no Done-when"
    if after == _raw_done_when(before_text):
        return "its Done-when is unchanged"
    return None


def _raw_done_when(text):
    """A spec's Done-when section as raw text, outer blank lines trimmed."""
    return "\n".join(_kitregistry.done_when_section(text or "")).strip()


def ruling_sync_lines(root, base, head=None):
    """One line per (row, item) the diff `base` -> `head` leaves out of sync
    (`head` None is the index): an open item leaves `pending` while a work item
    open in `base` cites it in `needs`, and the same diff neither updates that
    row's Done-when (non-empty afterwards, and its raw section changed) nor
    closes or removes the row. The registry is read through either carrier.
    `[]` when nothing leaves `pending`. A diff git cannot read is a line,
    never a skip. The diff's overrules are judged too (`overrule_sync_lines`).

    Implements: SR-148, LLR-298
    """
    args = ["diff", "--name-only", "--no-renames"]
    args += ["--cached", base] if head is None else [base, head]
    names = _git(root, args)
    if names is None:
        return [
            "cannot read the diff against {}, so whether it rules an open item "
            "is unknown".format(base)
        ]
    changed = names.splitlines()
    try:
        lines = []
        if set(_spine_carriers(OPEN_ITEMS_REGISTRY)) & set(changed):
            lines = _judged_lines(root, base, head)
        return lines + overrule_sync_lines(root, base, head, changed)
    except _UnreadableBlob as exc:
        return [
            "{} is listed in its tree but its contents cannot be read (a partial "
            "clone offline or a damaged object store), so whether this commit "
            "rules an open item or overrules a decision is unknown; fetch it and "
            "retry".format(exc)
        ]


def _judged_lines(root, base, head):
    """`ruling_sync_lines` once the diff touches the registry: the ruled items,
    then each citing row. Every blob it reads goes through `_show`.

    Implements: SR-148, LLR-298
    """
    new_prefix = ":" if head is None else head + ":"
    ruled = _ruled_items(
        _registry_states(root, base + ":"), _registry_states(root, new_prefix)
    )
    if ruled is None:
        return [
            "the open-items registry does not parse on one side of the diff, "
            "so whether it rules an open item is unknown"
        ]
    if not ruled:
        return []
    return _sync_lines(root, base, head, ruled)


def _sync_lines(root, base, head, ruled):
    """The per-row half of `ruling_sync_lines`, once the ruled items are known.

    Implements: SR-148, LLR-298
    """
    base_specs, head_specs = _tree_specs(root, base), _tree_specs(root, head)
    if base_specs is None or head_specs is None:
        return ["cannot list the work items on both sides of the diff"]
    new_prefix = ":" if head is None else head + ":"
    lines = []
    for wid, cited, text in _citing_rows(root, base, base_specs, ruled):
        gap = _sync_gap(root, new_prefix, head_specs.get(wid), text)
        if gap:
            lines.append(
                "{} cites {}, which this commit takes out of pending, and {}: "
                "the ruling's commit updates the row's Done-when with the decided "
                "criteria, citing the item, or closes or removes the row".format(
                    wid, ", ".join(cited), gap
                )
            )
    return lines


# --- THE OVERRULE SYNC: an overrule files or amends its work (WI-818) --------
# The owner's overrule of a delegated decision is coupled to work the way a
# ruling is coupled to its citing row: one commit against its parent. The
# trigger is the record's state (an entry overruled in the new tree and not in
# the parent's); the act is a queued or active spec this same diff adds or
# changes whose new text cites the entry. A citation in a row the diff leaves
# untouched discharges nothing, and an archived row is not work to do.
_OPEN_WORK_DIRS = (WORK_DIR + "/queued/", WORK_DIR + "/active/")


def _open_spec(path):
    """Is `path` a queued or active work item spec (not the `-000` example)?

    Implements: SR-225, LLR-303
    """
    name = path.rsplit("/", 1)[-1]
    return (
        path.startswith(_OPEN_WORK_DIRS)
        and name.startswith("WI-")
        and name.endswith(".md")
        and not "-".join(name.split("-")[:2]).endswith("-000")
    )


def overrule_sync_lines(root, base, head, changed):
    """One line per entry the diff `base` -> `head` (`head` None is the index)
    overrules without filing or amending a queued or active work item that
    cites it as `docs/decisions/<run>.toml#D-NNN`; `changed` is the diff's
    paths. `[]` when no record in the diff gains an overrule. A side that does
    not parse overrules nothing (`kitlib.decisions.newly_overruled`).

    Implements: SR-225, LLR-303
    """
    new_prefix = ":" if head is None else head + ":"
    owed = [
        _kitdecisions.citation(rel, eid)
        for rel in changed
        if rel.startswith(_kitdecisions.DECISIONS_DIR + "/") and rel.endswith(".toml")
        for eid in _kitdecisions.newly_overruled(
            _show(root, base + ":", rel), _show(root, new_prefix, rel)
        )
    ]
    if not owed:
        return []
    cited = set()
    for path in filter(_open_spec, changed):
        cited |= _kitdecisions.citations(_show(root, new_prefix, path))
    return [
        "{} is overruled by this commit, and no queued or active work item it "
        "files or amends cites it: the overrule's commit files a work item, or "
        "amends the queued one the decision was scoped to, citing {}".format(c, c)
        for c in owed
        if c not in cited
    ]


def staged_ruling_sync_lines(root):
    """`ruling_sync_lines` for the commit being made: the index against HEAD,
    or against the empty tree before the first commit (which closes nothing).

    Implements: SR-148, LLR-298
    """
    head = _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])
    base = head.strip() if head and head.strip() else _empty_tree(root)
    if base is None:
        return ["cannot read HEAD or the empty tree, so the commit is unjudged"]
    return ruling_sync_lines(root, base)


def commit_ruling_sync_lines(root, rev):
    """`ruling_sync_lines` for one commit against its FIRST parent, read off
    the commit object itself (not `rev^1`, which a shallow boundary hides). A
    true root commit — no parent in its object — has nothing to close and
    answers `[]`; a parent the repository cannot read (a shallow clone, a
    missing object) is refused by name, never read as a root (A1).

    Implements: SR-148, LLR-298
    """
    parents, unread = _commit_parents(root, rev, "it rules an open item", first=True)
    if unread or not parents:
        return unread
    return ruling_sync_lines(root, parents[0], rev)


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


# --- TEXT THEN ACT: the spine text before the approval act (WI-806) ----------
# OI-101 Q2 (risk 6), its trunk scope amended for landings by the owner's README
# Q-8 answer, 2026-10-04: a commit that writes under `SNAPSHOT_DIR` changes, as
# its own, no cell of an `APPROVAL_ACT_CSVS` row except `Status`, and adds or
# removes no such row. The text is committed first; the act (the flips, the
# copy, the ledger and the views) second, so every byte a copy blesses was
# committed, and readable, before the commit that blesses it. Flips and their
# copy stay ONE commit (SR-140): that is the act. One function over two trees,
# asked by the pre-commit hook of the staged tree and by the merge slot of each
# lane commit, so a `--no-verify` commit is still refused before it lands.
TEXT_THEN_ACT_REMEDY = (
    "commit the text on its own first, then take the act (the `Status` flips, "
    "`intake.py snapshot` and the views it regenerates) as a second commit that "
    "changes no other spine cell and adds or removes no row"
)
SQUASH_REBASE_HINT = (
    "a squash is exempt only of a lane tip that contains HEAD, its spine and "
    "record staged as the tip's: rebase the lane onto trunk first"
)


def _text_changes(root, bases, head):
    """`{(registry, row id, what)}` the tree `head` (None: the index) writes in
    the approval-act tiers as its OWN against `bases`, its parents: `what` is a
    cell, `Status` and the id excepted, whose value differs from its value in
    EVERY parent, or `added` / `removed` for a row whose presence differs from
    every parent. Values are compared, never per-parent change labels, so a row
    only one parent carried is judged by its cells. Keyed on the registry
    constant, so the two sides of a carrier change still join.

    Implements: SR-140, LLR-302
    """
    new_prefix = ":" if head is None else head + ":"
    out = set()
    for rel, id_col in APPROVAL_ACT_CSVS:
        now = _spine_rows_at(root, new_prefix, rel, id_col)
        sides = [_spine_rows_at(root, base + ":", rel, id_col) for base in bases]
        for rid in set(now).union(*sides):
            moves = _row_text_moves(rid, now, sides, id_col)
            out |= {(rel, rid, what) for what in moves}
    return out


def _row_text_moves(rid, now, sides, id_col):
    """What row `rid` of `now` holds that no side in `sides` holds: `added` or
    `removed` when its presence differs from every side, else each cell whose
    value differs from every side's (a side without the row holds no value).

    Implements: SR-140, LLR-302
    """
    row = now.get(rid)
    if all((rid in side) != (row is not None) for side in sides):
        return ["added" if row is not None else "removed"]
    if row is None:
        return []
    cells = set(row).union(*(side.get(rid, {}) for side in sides))
    return [
        c
        for c in cells - {id_col, "Status"}
        if all(
            rid not in side or (side[rid].get(c) or "") != (row.get(c) or "")
            for side in sides
        )
    ]


def text_then_act_lines(root, bases, head=None):
    """One line naming each approval-act row the commit `head` (None: the
    index) changes as its OWN while it also writes the approval record, judged
    against `bases`, its parents: a record path or a cell counts only when it
    differs from EVERY base. So a merge is judged by what neither side carried,
    and a lane's refresh merge bringing in trunk's text and act, made as two
    commits, is not the lane's. `[]` when the commit writes no record, or
    changes only `Status`. A diff git cannot read is a line, never a skip.

    Implements: SR-140, LLR-302
    """
    writes = None
    for base in bases:
        args = ["diff", "--name-only", "--no-renames"]
        args += ["--cached", base] if head is None else [base, head]
        own = _git(root, args + ["--", SNAPSHOT_DIR])
        if own is None:
            return [
                "cannot read the diff against {}, so whether it writes the "
                "approval record is unknown".format(base)
            ]
        paths = set(own.splitlines()) - {""}
        writes = paths if writes is None else writes & paths
    rows = {}
    for rel, rid, what in sorted(_text_changes(root, bases, head) if writes else ()):
        rows.setdefault("{} {}".format(PurePosixPath(rel).stem, rid), []).append(what)
    if not rows:
        return []
    named = ("{}: {}".format(row, ", ".join(cells)) for row, cells in rows.items())
    return ["{} in a commit that writes {}".format("; ".join(named), SNAPSHOT_DIR)]


def commit_text_then_act_lines(root, rev):
    """`text_then_act_lines` for one commit against EVERY parent, read off the
    commit object (`_commit_parents`), each line naming the commit. A root
    commit has no text before it and answers `[]`; a parent the repository
    cannot read is refused by name.

    Implements: SR-140, LLR-302
    """
    parents, unread = _commit_parents(root, rev, "it mixes text and the act")
    if unread or not parents:
        return unread
    lines = text_then_act_lines(root, parents, rev)
    return ["commit {}: {}".format(rev[:10], line) for line in lines]


def _squash_lines(root, head, tip):
    """The lines of every commit `head..tip` when the index IS the squash of
    `tip` for everything this rule reads, else None: `tip` contains `head` (the
    lane was rebased onto trunk, as acts serialize) and the index's
    approval-act registries and record are byte-equal to the tip's own. So a
    squash combining two judged cells into a third, and a `SQUASH_MSG` left
    behind by an abandoned squash, exempt nothing unless the staged spine and
    record are a judged commit's.

    Implements: SR-140, LLR-302
    """
    paths = [c for rel, _ in APPROVAL_ACT_CSVS for c in _spine_carriers(rel)]
    staged = ["diff", "--cached", "--name-only", tip, "--", SNAPSHOT_DIR, *paths]
    commits = _git(root, ["rev-list", "--reverse", head + ".." + tip])
    within = _git(root, ["merge-base", "--is-ancestor", head, tip]) == ""
    if not within or _git(root, staged) != "" or commits is None:
        return None
    return sum((commit_text_then_act_lines(root, rev) for rev in commits.split()), [])


def staged_text_then_act_lines(root, squashed=()):
    """`text_then_act_lines` for the commit being made: the index against HEAD,
    or against HEAD and MERGE_HEAD while a merge is in progress.

    A SQUASH LANDING is the one commit not held to the rule (owner, README
    Q-8): it carries a lane's text and act together, and is admitted because
    the rule held on every commit it squashes. The hook checks that rather than
    assuming it, since a hand landing never meets the merge slot: `squashed`
    names the commits git's `SQUASH_MSG` lists, newest first (the caller reads
    the file, as this module reads no file). When that tip contains HEAD and
    the index's approval-act registries and record are the tip's own, each
    commit HEAD..tip is judged and the index is not (`_squash_lines`);
    otherwise the index is judged like any commit, a refusal ending with
    `SQUASH_REBASE_HINT`. Before the first commit nothing is judged.

    Implements: SR-140, LLR-302
    """
    head = (_git(root, ["rev-parse", "--verify", "--quiet", "HEAD"]) or "").strip()
    if not head:
        return []
    merging = (_git(root, ["rev-parse", "-q", "--verify", "MERGE_HEAD"]) or "").strip()
    squash = None if merging or not squashed else _squash_lines(root, head, squashed[0])
    if squash is not None:
        return squash
    lines = text_then_act_lines(root, [head] + ([merging] if merging else []))
    hint = [SQUASH_REBASE_HINT] if squashed and not merging else []
    return lines and lines + hint
