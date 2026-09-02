"""THE ACCEPTANCE RECORD — what an amendment IS, and the mirror it is measured
against.

The boundary, in one sentence, because a decomposition that cannot say where its
line is has not drawn one: **everything here compares TWO GIT TREES cell by cell
to answer whether attested text has moved away from the copy recording its
acceptance; everything left in `check_trajectory.py` asks what the registries say
TODAY.** Nothing in this module reads the working tree, and the free-name census
proves it rather than the docstring claiming it — the whole module's only
non-builtin dependencies are `spine_carrier` (which carrier a spine registry
uses) and one `git -C <root> … or None` primitive.

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

Contracts: IF-091, IF-129 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-091: the staged spine-amendment set, offered as a call.
    `staged_spine_amendments(root, base, head)` returns one record per
    approved-text spine row amended between the two trees WITHOUT its status
    moving — `{"registry", "id", "approved": {cell: (before, after)},
    "traced": {...}}` — and `SPINE_CSVS` names the registries and id columns
    that walk covers. Which two trees is a parameter, so the same call answers
    the index-against-HEAD question and the commit-against-commit one. It
    classifies and stops: which traced cells oblige an act is the caller's
    ruling, not this module's. A new row is not an amendment, a row whose
    status moved is a deliberate call this does not second-guess, and any
    missing git context degrades to `[]` rather than raising.
    THE SAME WALK ANSWERS THE APPROVAL-ACT QUESTIONS (owner ruling 2026-09-01).
    `staged_approval_acts(root, base, head)` returns the rows that CROSSED into
    an approval claim or arrived already making one — precisely the set the
    amendment reader exempts — and `staged_drafted_rows` returns the rows a lane
    added, amended, or moved into `Drafted`. `lane_approval_refusal(root, base, head)`
    is the judgement over the first: the text refusing a work branch that
    performs the approval act, or None. It fails CLOSED on an unreadable
    snapshot delta, the opposite pole from its readers' silent degrade, because
    a refusal is where the conservative direction belongs. All four share
    `_spine_row_sides`, so no reader can be the only one that sees a row.
Contract IF-129: the ONE cell-comparison basis.
    `split_changed_cells(registry_path, id_col, before_row, live_row)` returns
    `{"approved": {cell: (before, after)}, "traced": {cell: (before, after)}}`
    for a single row, excluding the id column (a join key, not content) and
    `Status` (the flip the caller is asking about) structurally, at the callee.
    Every reader of "what changed on this row" joins here, so the staged
    amendment guard and a snapshot comparison cannot disagree about which cells
    are content or which half of the remainder arms an act. The dependency runs
    one way only: nothing in this module imports the readers that call it.
"""

try:
    import spine_carrier
    from kitlib import git as _kitgit
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier
    from kitlib import git as _kitgit
    from kitlib import spine as _kitspine

# `git -C <root> <args>` stdout on success, else None (git absent, not a repo,
# no such object). Every scan below degrades to None so the whole tier is a
# silent no-op outside a git checkout. The alias — rather than a body — is the
# `check.py` idiom: `kitlib.git` is the declared one home for this pattern, and
# the `stdin` batch argument that used to make this look like a different
# function is a parameter there since WI-521 slice 1.
_git = _kitgit.git_out


# The three spine registries the staged amend-without-flip warn (WI-316) watches,
# each with its id column. The SN tier is not listed: its rows were section-as-state
# when this was written and now carry their own `status`, but the warn has never
# been extended to them and doing so is its own decision, not a side effect.
SPINE_CSVS = (
    ("docs/requirements/system-requirements.toml", "SR-ID"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID"),
    ("docs/test/test-cases.toml", "TC-ID"),
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
SPINE_TRACED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset(
        {"SN-Refs", "Boundary-Refs", "Hat-Refs", "Phase", "Aspect", "Lifecycle"}
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
        {"Verifies", "Evidence", "Automated", "Phase"}
    ),
}
# The approved half. (The SR tier's `SupersededBy` column — approved by ruling
# at WI-388 — retired with the supersession tombstone class, D-4 ruling
# 2026-08-14b; the CMP registry's own SupersededBy is a separate, still-owed
# item.)
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
        }
    ),
    "docs/requirements/low-level-requirements.toml": frozenset(
        {"Title", "Detail", "Rationale"}
    ),
    "docs/test/test-cases.toml": frozenset(
        {"Method", "Expected", "Parameters", "Level", "Tier"}
    ),
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
    traced = {spine_carrier.stem(k): v for k, v in SPINE_TRACED_CELLS.items()}
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


def _spine_row_sides(root, base, head):
    """`(registry, id_col, before_rows, after_rows)` per spine registry the two
    trees actually differ in — THE ONE two-tree spine walk, shared by every
    reader below it.

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
        touches=sorted(c for p, _ in SPINE_CSVS for c in _spine_carriers(p)),
    )
    if revs is None:
        return
    staged_names, old_rev, new_rev = revs
    for csv_path, id_col in SPINE_CSVS:
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

    Owner ruling 2026-09-01 (WI-572): the act this reports is the ADJUDICATOR's,
    performed on the serial trunk side. Its ONE consumer is `lane_approval_refusal`
    directly below, which words the refusal `integrate._approval_act_refusal`
    returns against a worker branch's own delta — this reader does not itself
    cross the `IF-091` seam, and the seam does not declare that it does.

    Returns [] when not applicable; any missing git context is a silent no-op,
    like `staged_spine_amendments`."""
    out = []
    for registry, _id_col, before_rows, after_rows, _csv in _spine_row_sides(
        root, base, head
    ):
        for rid, row in after_rows.items():
            if not rid:
                continue
            before = before_rows.get(rid)
            if before is None:
                # A row absent on the base side. `before_rows` is `{}` for a
                # newly ADDED registry too, which is why the born arm still
                # answers there: a registry that arrives with approved rows in
                # it is the same unblessed-text-now-blessed event.
                if _claims_approval(row):
                    out.append(
                        {
                            "registry": registry,
                            "id": rid,
                            "act": "born",
                            "before": "",
                            "after": (row.get("Status") or "").strip(),
                        }
                    )
                continue
            if not _claims_approval(before) and _claims_approval(row):
                out.append(
                    {
                        "registry": registry,
                        "id": rid,
                        "act": "flip",
                        "before": (before.get("Status") or "").strip(),
                        "after": (row.get("Status") or "").strip(),
                    }
                )
    return out


# How `git diff --name-status` letters read as the ACT a branch performed on the
# snapshot. Worded from the letter rather than assumed, because the record is
# read by a human deciding why their merge stopped, and a branch that DELETES a
# stale `SNAPSHOT_DIR` file reported as one it "wrote" is a false sentence in the
# one artifact that explains the stop. An unrecognised letter is still named —
# the file changed, and which way is the part this does not know.
_SNAPSHOT_ACT = {"A": "wrote", "M": "rewrote", "D": "deleted"}


def _snapshot_acts(name_status):
    """`["wrote <path>", ...]` for a `--name-status` block: one line per
    `SNAPSHOT_DIR` file the delta touched, worded by its status letter."""
    for line in name_status.splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or not parts[-1].strip():
            continue
        letter = parts[0].strip()[:1]
        yield "{} {}".format(_SNAPSHOT_ACT.get(letter, "changed"), parts[-1].strip())


def lane_approval_refusal(root, base, head):
    """Why a WORK BRANCH's delta may not merge because it performs an APPROVAL
    ACT — the refusal text, or None when it performs none.

    THE ACT IS THE ADJUDICATOR'S, ON TRUNK (owner ruling 2026-09-01). A worker
    lane AUTHORS `Drafted` spine rows and AMENDS cell text on any row, including
    approved ones. It does not flip a `Status` into `Approved`/`Founded`, does
    not mint a row already claiming one, and does not write `SNAPSHOT_DIR`. Two
    reasons, both the owner's. CONTEXT: approving a row means reading its whole
    chain — the parent SR, the sibling LLRs, the tests — which one work item does
    not hold. CONCURRENCY: two lanes touching the spine conflict at merge and the
    snapshot must not move across a workstream, whereas a serial trunk-side act
    cannot conflict.

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
    acts = staged_approval_acts(root, base, head)
    out = _git(
        root, ["diff", "--name-status", "--no-renames", base, head, "--", SNAPSHOT_DIR]
    )
    if out is None:
        return (
            "cannot read {}'s {} delta against {}, so whether this branch wrote "
            "the approval record is unknowable; nothing was merged".format(
                head, SNAPSHOT_DIR, str(base)[:10]
            )
        )
    snapshot_files = sorted(_snapshot_acts(out))
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
        "ruling 2026-09-01; PROCESS.md §4). A lane AUTHORS `Drafted` spine rows "
        "and AMENDS cell text; it does not flip a `Status` into "
        "`Approved`/`Founded`, does not mint a row already claiming one, and does "
        "not write {}/. Approving means reading the row's whole chain, which one "
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
    cannot disagree about which registries and rows the delta contains."""
    # Each row answers for its OWN cells (owner ruling 2026-08-17m): the
    # sanctioned amend path is flipping the AMENDED row itself in the same
    # commit — a Status that moved is exempted below. The retired chain
    # reading's owning-SR exemption (a parent flip sanctioning a silent
    # child amendment) is gone with the doctrine: a child whose approved
    # cells change while its own Status still claims approval warns,
    # whatever its parent does.

    out = []
    for registry, id_col, head_rows, staged_rows, csv_path in _spine_row_sides(
        root, base, head
    ):
        if not head_rows or not staged_rows:
            continue  # first commit / newly added registry — nothing attested yet
        for rid, row in staged_rows.items():
            head = head_rows.get(rid)
            if not rid or rid.endswith("-000") or head is None:
                continue
            head_status = (head.get("Status") or "").strip().lower()
            cur_status = (row.get("Status") or "").strip().lower()
            # APPROVED-TEXT STATES, both sides, and the SAME one. Since D-9
            # step 5 that is the single value `Approved`; before the fold it was
            # `Verified` OR `Planned`, and requiring the SAME one on both sides
            # is what kept a legitimate rung move from reading as an amendment.
            # A status that MOVED between the two sides is still exempt,
            # unchanged: that is a deliberate call this does not second-guess.
            if head_status != cur_status or head_status not in _APPROVED_TEXT:
                continue
            changed = split_changed_cells(csv_path, id_col, head, row)
            if changed["approved"] or changed["traced"]:
                out.append(dict(changed, registry=registry, id=rid))
    return out


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
        "Since D-9 step 7 there is no marker to set: either re-attest it in "
        "this commit and run `intake.py snapshot` in the same commit, or the "
        "change rides as SNAPSHOT DRIFT until the next sitting — visible on the "
        "re-attest brief and open-items.html, but not blessed".format(
            a["id"], ", ".join(sorted(a["approved"]))
        )
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

# The snapshot's prose stamp: rendered for a human, PARSED BY NOTHING, and so
# the one file under the snapshot root with no live counterpart to mirror.
SNAPSHOT_README = "README.md"


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
        # nothing, with no live counterpart to mirror. Excluding it by name
        # rather than by "no counterpart exists" keeps a genuinely missing
        # registry loud.
        if live_rel == SNAPSHOT_README:
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
                "here".format(name, live_rel)
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
        # The README is prose with no live counterpart (design §F8), exactly as
        # in the staged rule — excluded by name so a genuinely missing registry
        # stays loud.
        if live_rel == SNAPSHOT_README:
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
                "(`intake.py snapshot`). This divergence has LANDED: re-copy it "
                "in a reviewed commit, or restore the copy that was "
                "blessed".format(name, live_rel, rev[:8])
            )
    return out
