"""integrate.py — what the merge slot ADMITS, and the four gates in front of it.

One of four modules `WI-521` slice 2 carved out of the 3,520-line
`test_integrate.py` monolith (M-06); the family and the rule for what is shared
are in `tests/integrate_fixtures.py`. Everything here answers one question about
a branch the slot is looking at — *may this land?* — before the station protocol
of `test_integrate_station.py` gets to move it:

  * **the OUTCOME is the folder** (WI-387, §A3) — a close is read off the
    directory the claimed specs landed in, `docs/archive/work/` included; a
    landing in an OPEN folder, in two folders at once, or in none names no
    outcome at all rather than guessing one.
  * **the R1 mint refusal** (WI-397) — a finished branch whose `docs/work/`
    delta ADDS a spec carrying an id it never claimed cannot merge, because
    minting is a serial trunk-side act and two lanes cannot see each other's
    trees. Driven on one topology built both ways (with and without the minted
    file), plus the shapes that must stay ADMITTED — a terminal-outcome move
    into `complete/` and `cancelled/`, a handback's return to `queued/` with its
    bar-inert `.patch`, and a TRUNK-side mint taken after the claim (free by
    construction: it is in the merge base, not in the branch's delta) — and the
    rename trap that makes `--no-renames` load-bearing rather than tidy.
  * **the verdict gate** (RULING-7) — the dialed review artifact must be
    present, must parse as APPROVE, and must be FRESH: a verdict whose last
    commit predates a later code commit on the branch is a stale APPROVE and
    does not clear the gate. Fragment (`docs/log.d/`) and review commits are
    excluded from "code", and so is the mechanical refresh commit (WI-386: it
    lands AFTER the review by construction, so counting it as code would make
    the gate unpassable) — bookkeeping cannot stale a good verdict.
  * **the declared bar** (§4) — a missing `docs/stack.ini`, an absent
    `[product] test`, or a declared-but-EMPTY one is a REFUSAL, never a skip.
  * **the BRANCH tree's own harness** (WI-368, relocated by WI-386) — which
    copy of `trunk_step.py` runs, probed across the layouts an invoker can be
    standing in.
  * **the RULING-6 window audit** — a non-merge trunk commit touching product
    paths is flagged by sha; bookkeeping surfaces and `--no-ff` merges are not.
"""

import os

from conftest import env_gate_skipif
from integrate_fixtures import (
    T_BASE,
    T_CODE,
    T_LATER,
    T_VERDICT,
    VERDICT_APPROVE,
    _commit,
    _git,
    _rev,
    claim_repo,
    git_repo,
    integ,
    write_spec,
)

# The vocabulary's own home (WI-483): imported as a package, since `load_script`
# loads one `scripts/*.py` and `scripts/` is already on sys.path by here.
import kitlib.registry as kit_registry  # noqa: E402  (after the fixture import)
import kitlib.station as kit_station  # noqa: E402  (after the fixture import)

pytestmark = env_gate_skipif("git")


# --- 2b. the OUTCOME is the folder (WI-387, §A3) ------------------------------


def _close_to(root, branch, directory, wi="WI-401", slug="widget", archive=False):
    """Move `branch`'s claimed spec into `directory` on the branch — the move
    that both finishes the lane and states its outcome. `archive=True` closes
    into `docs/archive/work/<directory>/` (WI-504, OI-55 ruled (a)): the
    terminal home since 2026-08-22, one directory deeper."""
    _git(root, "checkout", "-q", branch)
    work_root = "docs/archive/work" if archive else "docs/work"
    dest = root / work_root.replace("/", os.sep) / directory
    dest.mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/{}/{}-{}.md".format(branch, wi, slug),
        "{}/{}/{}-{}.md".format(work_root, directory, wi, slug),
    )
    _commit(root, "close: {} -> {}".format(wi, directory), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")


def test_the_outcome_is_read_off_the_folder_the_specs_landed_in(tmp_path):
    # Three outcomes, one read, no state file — and the read must DISCRIMINATE,
    # so all three are driven on identical branches that differ only in which
    # folder the closing commit moved the spec into.
    for directory, outcome in (
        ("complete", "merged"),
        ("cancelled", "cancelled"),
        ("partial", "partial"),
    ):
        home = tmp_path / directory
        home.mkdir()
        root = claim_repo(home)
        assert integ.claim(root, "WI-401", "wi-401") == 0
        _close_to(root, "wi-401", directory)
        assert integ.finished_branches(root) == ["wi-401"]
        assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": outcome}, [])


def test_the_outcome_is_read_off_the_archive_home_too(tmp_path):
    """WI-504 (OI-55 ruled (a)): a close that lands its terminal move under
    `docs/archive/work/<outcome>/` — the new home, one directory deeper —
    reads exactly like the pre-migration `docs/work/<outcome>/` close.
    `branch_outcomes` indexes the outcome directory per-prefix rather than at
    a fixed offset, which is exactly what this drives."""
    for directory, outcome in (
        ("complete", "merged"),
        ("cancelled", "cancelled"),
        ("partial", "partial"),
    ):
        home = tmp_path / ("archive-" + directory)
        home.mkdir()
        root = claim_repo(home)
        assert integ.claim(root, "WI-401", "wi-401") == 0
        _close_to(root, "wi-401", directory, archive=True)
        assert integ.finished_branches(root) == ["wi-401"]
        assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": outcome}, [])


def test_a_close_into_an_OPEN_folder_names_no_outcome_at_all(tmp_path):
    """SR-144 made every outcome terminal. A lane that closes into `queued/`,
    `draft/` or `deferred/` used to read as a handback — the row went straight
    back on the frontier, and only a `blockref` stopped the driver claiming and
    closing it forever. Those three are gone from `OUTCOME_DIRS`, so such a
    close now names NOTHING and the merge refuses: stopping early is a state
    with a name and a report, not a return to the queue."""
    for directory in ("queued", "draft", "deferred"):
        home = tmp_path / ("open-" + directory)
        home.mkdir()
        root = claim_repo(home)
        assert integ.claim(root, "WI-401", "wi-401") == 0
        _close_to(root, "wi-401", directory)
        outcomes, unresolved = integ.branch_outcomes(root, "wi-401")
        assert outcomes == {}, directory
        assert unresolved == ["WI-401-widget.md"], directory
        _outcomes, refusal = integ._merge_refusal(root, "wi-401", ["WI-401"])
        assert refusal is not None and "exactly ONE declared state" in refusal


def test_a_lane_cannot_close_into_the_restructured_folder(tmp_path):
    """The fourth terminal STATUS is deliberately not a fourth lane OUTCOME
    (2026-09-02 restructure plan §1.6). `restructured` is filed by a
    consolidation judgement on trunk — a lane that could close into it would be
    asserting that another row's scope had been absorbed, a judgement it is
    structurally not holding — so `OUTCOME_DIRS`, `Outcome` and
    `kitlib.station.CLAIMED_OUTCOMES` are all unchanged, and a lane that tries it names
    no outcome and the merge refuses, exactly as a close into `queued/` does.

    Also drives the other half, which IS a live shape: a restructured spec
    sitting in the archive on TRUNK — where the consolidation put it — must not
    disturb an unrelated lane's outcome read. `outcome_of` ignores directories
    it does not declare rather than raising, and this is what proves it."""
    root = claim_repo(tmp_path)
    absorbed = root / "docs" / "archive" / "work" / "restructured" / "WI-402-old.md"
    absorbed.parent.mkdir(parents=True, exist_ok=True)
    absorbed.write_text(
        '+++\nid = "WI-402"\ntitle = "absorbed"\n+++\n'
        "\n## Deliverable\n\nRestructured into WI-401.\n",
        encoding="utf-8",
        newline="\n",
    )
    _git(root, "add", "-A")
    _commit(root, "consolidate: WI-402 absorbed into WI-401", when=T_CODE)
    assert integ.claim(root, "WI-401", "wi-401") == 0

    # The trunk-side restructured row is inert for this lane's read...
    _close_to(root, "wi-401", "complete", archive=True)
    assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": "merged"}, [])
    # BOTH sides of the split, so a revert of either one reds this: the STATUS
    # vocabulary declares the folder...
    assert kit_registry.SPEC_STATUS_DIRS["restructured"] == "restructured"
    # ...and the lane-outcome vocabulary deliberately does not.
    assert "restructured" not in integ.OUTCOME_DIRS
    assert "restructured" not in kit_station.CLAIMED_OUTCOMES
    assert "restructured" not in kit_station.OUTCOME_DIRS
    assert integ.outcome_of({"restructured"}) is None

    # ...and a lane that CLOSES into it states nothing, so the merge refuses.
    home = tmp_path / "lane-close"
    home.mkdir()
    other = claim_repo(home)
    assert integ.claim(other, "WI-401", "wi-401") == 0
    _close_to(other, "wi-401", "restructured", archive=True)
    outcomes, unresolved = integ.branch_outcomes(other, "wi-401")
    assert outcomes == {} and unresolved == ["WI-401-widget.md"]
    _outcomes, refusal = integ._merge_refusal(other, "wi-401", ["WI-401"])
    assert refusal is not None and "exactly ONE declared state" in refusal


def test_a_claimed_spec_that_landed_TWICE_names_no_outcome_either(tmp_path):
    # The other half of "exactly one folder". A basename-keyed dict let the last
    # `ls-tree` line win — plain alphabetical precedence, which puts `queued`
    # (handback, no verdict owed) ahead of `complete` (merged, an APPROVE owed),
    # so a contradiction resolved silently toward the answer that SKIPS the
    # gate. REVIEW-A round 1 drove all three pairs. Fail-closure now lives where
    # the outcome is read, not in another script's duplicate-id rung.
    for first, second in (("complete", "partial"), ("cancelled", "partial")):
        home = tmp_path / (first + "-" + second)
        home.mkdir()
        root = claim_repo(home)
        assert integ.claim(root, "WI-401", "wi-401") == 0
        _git(root, "checkout", "-q", "wi-401")
        src = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
        text = src.read_text(encoding="utf-8")
        for directory in (first, second):
            dst = root / "docs" / "work" / directory / "WI-401-widget.md"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text, encoding="utf-8", newline="\n")
        _git(root, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
        _commit(root, "close: WI-401 into two folders at once", when=T_VERDICT)
        _git(root, "checkout", "-q", "main")

        outcomes, unresolved = integ.branch_outcomes(root, "wi-401")
        assert outcomes == {} and unresolved == ["WI-401-widget.md"], (first, second)
        refusal = integ.integrate_one(root, "wi-401", "smoke")
        assert "exactly ONE declared state directory" in refusal
        assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


def test_a_claimed_spec_that_landed_nowhere_names_no_outcome(tmp_path):
    # Fail closed. A branch that DELETED its claimed spec is finished by the
    # active/-is-empty read but has stated nothing, and guessing an outcome for
    # it would let unreviewed work merge as if it had been approved.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    _git(root, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(root, "close: delete the spec instead of moving it", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert integ.branch_outcomes(root, "wi-401") == ({}, ["WI-401-widget.md"])
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "exactly ONE declared state directory" in refusal
    assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


# --- 2c. the R1 mint refusal (WI-397) ----------------------------------------


def _mint_repo(home, minted=None, directory="complete"):
    """A claimed branch that CLOSED its own spec into `directory` — and, when
    `minted` is given, filed a spec for that id in the same commit.

    One builder for both sides of the rung, so "the same branch with the foreign
    spec removed" is literally the same topology minus one file rather than a
    second fixture that happens to look similar."""
    home.mkdir(parents=True, exist_ok=True)
    root = claim_repo(home)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    if minted is not None:
        write_spec(root, "queued", minted, slug="found-mid-flight", specref="seed.txt")
    dest = root / "docs" / "work" / directory
    dest.mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/{}/WI-401-widget.md".format(directory),
    )
    _commit(root, "close: WI-401 -> {}".format(directory), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")
    return root


def test_a_branch_that_mints_a_foreign_id_is_refused_at_the_merge_slot(tmp_path):
    # RULING R1 (owner, 2026-08-01). Two lanes cannot see each other's trees, so
    # a branch-side `max(id) + 1` collides by construction — it happened twice in
    # one session. The rung makes it unrepresentable at the one point every lane
    # passes through, and the refusal has to be ACTIONABLE: the foreign id, the
    # path that carries it, the claimed set it was judged against, and the rule.
    root = _mint_repo(tmp_path / "minted", minted="WI-777")

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal is not None
    assert "WI-777" in refusal
    assert "docs/work/queued/WI-777-found-mid-flight.md" in refusal
    assert "NEVER MINTS A WORK-ITEM ID" in refusal
    assert "(WI-401)" in refusal  # the claimed set, so the judgement is checkable
    assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


def test_the_same_branch_without_the_minted_spec_is_admitted(tmp_path):
    # The other half of the same topology: a rung that refused everything would
    # pass the test above. Driven twice — the rung itself says None, and the SLOT
    # gets past it to the NEXT refusal (this fixture declares no `[product] test`),
    # which is what proves the admission is in situ and not just in the helper.
    root = _mint_repo(tmp_path / "clean", minted=None)

    claimed = integ._claimed_wi_ids(root, "wi-401")
    assert claimed == ["WI-401"]
    assert integ._minted_id_refusal(root, "wi-401", claimed) is None
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "no [product] test declaration" in refusal
    assert "NEVER MINTS" not in refusal


def test_a_branchs_own_terminal_outcome_move_is_admitted(tmp_path):
    # The move that CLOSES a lane re-ADDS the spec under its terminal folder, so
    # a rung reading adds naively would refuse every branch that ever finished.
    # Both terminal folders, because both are that move.
    for directory in ("complete", "cancelled"):
        root = _mint_repo(tmp_path / directory, directory=directory)
        claimed = integ._claimed_wi_ids(root, "wi-401")
        added = [
            ln
            for ln in _git(
                root,
                "diff",
                "--name-status",
                "--no-renames",
                _rev(root, "main"),
                "wi-401",
                "--",
                "docs/work",
            ).splitlines()
            if ln.startswith("A")
        ]
        # The move really is an ADD on this side — the admission is the rung
        # reading the id, not the diff happening to be empty.
        assert added == ["A\tdocs/work/{}/WI-401-widget.md".format(directory)], added
        assert integ._minted_id_refusal(root, "wi-401", claimed) is None, directory


def test_a_partial_close_its_report_and_its_artefact_are_admitted(tmp_path):
    # The third outcome (§A3 as amended by SR-144). A partial close ADDS its own
    # spec back under `partial/`, writes an immutable per-close REPORT under
    # docs/handbacks/, and may drop a bar-inert `.patch` beside it. None of the
    # three is a mint: the closed spec's id is claimed, and neither the report
    # nor the artefact carries a spec filename at all — the report deliberately
    # lives OUTSIDE docs/work/ so `spec_files`' rglob never walks it.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    (root / "docs" / "work" / "partial").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/partial/WI-401-widget.md",
    )
    report = root / "docs" / "handbacks" / "WI-401-wi-401.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "\n".join(
            [
                "+++",
                'wi = "WI-401"',
                'branch = "wi-401"',
                'claimed_outcome = "partial"',
                'reason = "stopped early"',
                'commit_range = "aaa..bbb"',
                'suggested_tier = "medium"',
                'keep_commits = ["aaa"]',
                "discard_commits = []",
                "+++",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    patch = root / "docs" / "work" / "handback" / "wi-401.patch"
    patch.parent.mkdir(parents=True, exist_ok=True)
    patch.write_text("--- a/x\n+++ b/x\n", encoding="utf-8", newline="\n")
    _commit(root, "partial: WI-401 -> partial/", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": "partial"}, [])
    assert integ._minted_id_refusal(root, "wi-401", ["WI-401"]) is None
    # ...and the keep/discard rung passes on a report that declares the split.
    assert integ._partial_report_refusal(root, "wi-401", {"WI-401": "partial"}) is None


def test_a_trunk_side_mint_after_the_claim_is_not_the_branchs(tmp_path):
    # The other half of the ruling, and the half a rung reading the WHOLE tree
    # would get wrong: trunk-side minting stays exactly as free as it was. It is
    # free by CONSTRUCTION rather than by exemption — whatever trunk did sits in
    # the merge BASE, so it is not in the branch's delta at all.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    write_spec(root, "queued", "WI-500", slug="filed-on-trunk", specref="seed.txt")
    _commit(root, "file WI-500 on the trunk", when=T_LATER)
    _close_to(root, "wi-401", "complete")

    # The id really is present on trunk and really is not the branch's.
    assert (root / "docs" / "work" / "queued" / "WI-500-filed-on-trunk.md").is_file()
    assert integ._minted_id_refusal(root, "wi-401", ["WI-401"]) is None


# --- 2c-bis. the APPROVAL-ACT refusal (owner ruling 2026-09-01) --------------


_SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase,Aspect,Hat-Refs\n"
)


def _sr(status, req="the drafted text"):
    return 'SR-001,Adder,SN-001,"{}","why","ac",,C,Test,{},1,,hat.MAINTAINER\n'.format(
        req, status
    )


def _spine_lane(
    home,
    *,
    flip=False,
    born=False,
    snapshot=False,
    safety="ordinary",
    adjudicates=(),
    first_approval=True,
):
    """A claimed branch that authored a `Drafted` SR — and then, per flag,
    performed one of the three shapes of approval act on it.

    One builder for every arm so "the same lane that only authored" is literally
    the same topology minus one write, rather than a second fixture that happens
    to look similar (`_mint_repo`'s rule, one section up)."""
    home.mkdir(parents=True, exist_ok=True)
    root = claim_repo(
        home,
        safety=safety,
        brief=(
            "first-approval" if safety == "adjudication" and first_approval else None
        ),
        adjudicates=adjudicates,
    )
    reg = root / "docs" / "requirements"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "system-requirements.csv").write_text(
        _SR_HEADER + _sr("Drafted"), encoding="utf-8", newline="\n"
    )
    _commit(root, "spine: the attested baseline", when=T_BASE)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    rows = _SR_HEADER + _sr("Approved" if flip else "Drafted", "the AMENDED text")
    if born:
        rows += (
            'SR-002,New req,SN-001,"fresh","why","ac",,C,Test,Approved,1,,'
            "hat.MAINTAINER\n"
        )
    (reg / "system-requirements.csv").write_text(rows, encoding="utf-8", newline="\n")
    if snapshot:
        snap = root / "docs" / "archive" / "last_approved" / "docs" / "requirements"
        snap.mkdir(parents=True, exist_ok=True)
        (snap / "system-requirements.csv").write_text(
            rows, encoding="utf-8", newline="\n"
        )
    _commit(root, "WI-401: touch the spine", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    _close_to(root, "wi-401", "complete")
    return root


def test_a_lane_that_flips_a_status_to_approved_is_refused_at_the_merge_slot(tmp_path):
    # Owner ruling 2026-09-01. The act — the flip, and the snapshot that anchors
    # it — is the ADJUDICATOR's, on the serial trunk side: approving a row means
    # reading its whole chain, which one work item does not hold, and a
    # trunk-side act cannot conflict with a second lane. This happened once for
    # real (WI-508 slice 6, four rows at `580df781`) and the next review round
    # returned CHANGES-REQUESTED against exactly those flips.
    root = _spine_lane(tmp_path / "flip", flip=True)

    assert integ._adjudication_lane(root, "wi-401") is False
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal is not None
    assert "APPROVAL ACT" in refusal
    assert "SR-001 flipped Drafted -> Approved" in refusal
    assert "Leave the rows `Drafted`" in refusal  # actionable, not just a verdict
    assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


def test_a_scoped_adjudication_lane_may_land_its_flip_and_snapshot(tmp_path):
    root = _spine_lane(
        tmp_path / "adjudication",
        flip=True,
        snapshot=True,
        safety="adjudication",
        adjudicates=("SR-001",),
    )

    assert integ._adjudication_lane(root, "wi-401") is True
    assert integ._approval_act_refusal(root, "wi-401") is None
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "no [product] test declaration" in refusal
    assert "APPROVAL ACT" not in refusal


def test_a_first_approval_adjudication_with_no_scope_is_refused(tmp_path):
    root = _spine_lane(tmp_path / "empty-scope", flip=True, safety="adjudication")

    refusal = integ._approval_act_refusal(root, "wi-401")
    assert refusal is not None
    assert "EMPTY `Adjudicates` scope" in refusal


def test_a_scoped_return_only_adjudication_needs_no_approval_act(tmp_path):
    root = _spine_lane(
        tmp_path / "return-only",
        safety="adjudication",
        adjudicates=("SR-001",),
    )

    assert integ._approval_act_refusal(root, "wi-401") is None


def test_a_scoped_flip_without_its_snapshot_is_refused(tmp_path):
    root = _spine_lane(
        tmp_path / "unanchored",
        flip=True,
        safety="adjudication",
        adjudicates=("SR-001",),
    )

    refusal = integ._approval_act_refusal(root, "wi-401")
    assert refusal is not None
    assert (
        "system-requirements.csv was approved WITHOUT its anchoring snapshot" in refusal
    )


def test_an_adjudication_kind_alone_does_not_authorise_a_flip(tmp_path):
    root = _spine_lane(
        tmp_path / "actor-only",
        flip=True,
        safety="adjudication",
        first_approval=False,
    )

    refusal = integ._approval_act_refusal(root, "wi-401")
    assert refusal is not None
    assert "EMPTY `Adjudicates` scope" in refusal


def test_an_adjudication_cannot_flip_a_row_outside_its_scope(tmp_path):
    root = _spine_lane(
        tmp_path / "outside",
        flip=True,
        snapshot=True,
        safety="adjudication",
        adjudicates=("SR-002",),
    )

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal is not None
    assert "SR-001 is OUTSIDE `Adjudicates` scope (SR-002)" in refusal
    assert _rev(root, "HEAD") != _rev(root, "wi-401")


def test_an_adjudication_snapshot_cannot_widen_beyond_its_flips(tmp_path):
    root = _spine_lane(
        tmp_path / "wide-snapshot",
        flip=True,
        snapshot=True,
        safety="adjudication",
        adjudicates=("SR-001",),
    )
    _git(root, "checkout", "-q", "wi-401")
    snap = root / "docs" / "archive" / "last_approved" / "docs" / "test"
    snap.mkdir(parents=True, exist_ok=True)
    (snap / "test-cases.toml").write_text("[cases]\n", encoding="utf-8", newline="\n")
    _commit(root, "WI-401: widen the approval snapshot", when=T_LATER)
    _git(root, "checkout", "-q", "main")

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal is not None
    assert "snapshot WIDENED to docs/test/test-cases.toml" in refusal
    assert _rev(root, "HEAD") != _rev(root, "wi-401")


def test_unreadable_actor_frontmatter_fails_toward_the_approval_refusal(tmp_path):
    root = _spine_lane(tmp_path / "unreadable", flip=True, safety="adjudication")
    claimed = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    claimed.write_text("not frontmatter\n", encoding="utf-8")

    assert integ._adjudication_lane(root, "wi-401") is False
    refusal = integ._approval_act_refusal(root, "wi-401")
    assert refusal is not None
    assert "SR-001 flipped Drafted -> Approved" in refusal


def test_a_lane_that_mints_a_row_born_approved_is_refused(tmp_path):
    # The second measured shape, and the one a flip-only rung would miss whole:
    # four lanes (WI-483, WI-500, WI-501, WI-507) minted rows that ARRIVED
    # `Approved`, so no Status ever moved and the approval brief never saw them.
    root = _spine_lane(tmp_path / "born", born=True)

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "SR-002 was minted born Approved" in refusal
    assert _rev(root, "HEAD") != _rev(root, "wi-401")


def test_a_lane_that_writes_the_approval_snapshot_is_refused(tmp_path):
    # The third: the copy under `docs/archive/last_approved/` IS the signature
    # since the mechanical writer retired (OI-45 ruled (b)), so a lane that
    # writes it has approved whatever text was live at that moment — which is
    # how a spine-only act came to re-seal off-spine drift (WI-571). The rung
    # names the files, because "you wrote the snapshot" is not something a lane
    # can act on at 3am.
    root = _spine_lane(tmp_path / "snap", snapshot=True)

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "wrote docs/archive/last_approved/" in refusal
    assert _rev(root, "HEAD") != _rev(root, "wi-401")


def test_a_lane_that_only_authors_and_amends_drafted_rows_is_admitted(tmp_path):
    # THE OTHER HALF, and the half that makes this a rule instead of a ban on
    # touching the spine: authoring `Drafted` rows and amending cell text is
    # exactly what the ruling leaves to the lane. Driven twice — the rung itself
    # says None, and the SLOT gets past it to the NEXT refusal (this fixture
    # declares no `[product] test`), which is what proves the admission is in
    # situ rather than only in the helper.
    root = _spine_lane(tmp_path / "clean")

    assert integ._approval_act_refusal(root, "wi-401") is None
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "no [product] test declaration" in refusal
    assert "APPROVAL ACT" not in refusal


def test_a_trunk_side_approval_after_the_claim_is_not_the_lanes(tmp_path):
    # The mirror of the R1 rung's own trunk-side arm, and the property that
    # keeps the ruling from banning approval outright: the adjudicator's act
    # happens on trunk, so it sits in the merge BASE and is not in the branch's
    # delta at all. Free by construction, not by exemption.
    root = _spine_lane(tmp_path / "trunk")
    reg = root / "docs" / "requirements" / "system-requirements.csv"
    reg.write_text(_SR_HEADER + _sr("Approved"), encoding="utf-8", newline="\n")
    _commit(root, "spine: the adjudicator approves SR-001 on trunk", when=T_LATER)

    # The flip really is on trunk and really is not the branch's.
    assert "Approved" in reg.read_text(encoding="utf-8")
    assert integ._approval_act_refusal(root, "wi-401") is None


def test_the_mint_is_seen_even_when_git_would_report_it_as_a_rename(tmp_path):
    # Why the diff is read `--no-renames`, driven rather than asserted. Rename
    # detection is free to pair the branch's own close (a DELETE under
    # `active/`) with the minted file — spec files are short and near-identical
    # — and then the mint arrives as one `R` record with no add left to see.
    # Here the minted spec is a BYTE COPY of the claimed one while the closed
    # copy was edited, so the pairing is unambiguous and reproducible.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    src = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    original = src.read_text(encoding="utf-8")
    (root / "docs" / "work" / "queued" / "WI-777-copy.md").write_text(
        original, encoding="utf-8", newline="\n"
    )
    dest = root / "docs" / "work" / "complete" / "WI-401-widget.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        original.replace("A widget, shipped.", "A widget, shipped, at last."),
        encoding="utf-8",
        newline="\n",
    )
    _git(root, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(root, "close: WI-401 -> complete, and mint WI-777", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    # The trap, MEASURED: with rename detection on, the mint appears in exactly
    # one record and that record is an `R` (git pairs it with the delete side of
    # the close). The only ADD left is the branch's own legitimate close — so an
    # add-reader would see nothing wrong and merge the collision.
    detected = _git(
        root,
        "diff",
        "--name-status",
        "-M",
        _rev(root, "main"),
        "wi-401",
        "--",
        "docs/work",
    )
    minted = [ln for ln in detected.splitlines() if "WI-777" in ln]
    assert len(minted) == 1 and minted[0].startswith("R"), detected
    assert "A\tdocs/work/complete/WI-401-widget.md" in detected, detected

    refusal = integ._minted_id_refusal(root, "wi-401", ["WI-401"])
    assert refusal is not None and "WI-777" in refusal


VERDICT_CHANGES = """# Review A — WI-401

Model: test/reviewer

- [MAJOR] src/widget.py:1 -> the value is wrong -> return 2
- [MINOR] src/widget.py:1 -> no docstring -> add one

VERDICT: CHANGES-REQUESTED findings=2
"""


def verdict_repo(tmp_path, policy="1"):
    """A trunk carrying the declared review-policy dial, plus a work branch with
    one code commit on it (pinned at T_CODE)."""
    root = git_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "review-policy").write_text(policy + "\n", encoding="utf-8", newline="\n")
    _commit(root, "declare the review policy", when=T_BASE)
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: the widget", when=T_CODE)
    return root


def write_verdict(root, text, when):
    path = root / "docs" / "reviews" / "WI-401-REVIEW-A.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "review: WI-401 REVIEW-A", when=when)


def test_verdict_is_not_required_at_review_policy_zero(tmp_path):
    # The dial off is a real configuration, not a loophole: at 0 the harness
    # gates ARE the bar and the queue asks for no verdict artifact.
    root = verdict_repo(tmp_path, policy="0")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_a_required_verdict_absent_from_the_branch_refuses_by_name(tmp_path):
    # Fail-closed and ACTIONABLE: the refusal names the exact path the branch
    # must carry, so the remedy needs no lookup.
    root = verdict_repo(tmp_path, policy="1")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "docs/reviews/WI-401-REVIEW-A.md" in refusal
    assert "absent from wi-401" in refusal


def test_a_changes_requested_verdict_refuses(tmp_path):
    # Present is not enough — the machine line is PARSED (score_reviews), so a
    # verdict that asked for changes cannot clear the gate by existing.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_CHANGES, when=T_VERDICT)

    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "is not an APPROVE" in refusal
    assert "CHANGES-REQUESTED" in refusal


def test_an_approve_that_did_not_judge_this_tree_does_not_count(tmp_path):
    # GOVERNING = TREE IDENTITY (OI-76, ruled 2026-08-31). This used to be a
    # TIME comparison — "the verdict's commit is no older than the branch's last
    # non-record commit" — and the ruling dissolved it into an identity: a
    # verdict names the tree it judged or it does not count. The observable
    # behaviour on THIS input is unchanged (real code committed after the
    # APPROVE is the stale pass that must not clear the gate); what changed is
    # that there is no longer an ordering rule to get wrong, so the case where
    # the old comparison silently promoted a stale APPROVE — a re-run round
    # after a trivial edit — cannot arise.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: change the widget after the review", when=T_LATER)

    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "does not name the branch's current tree" in refusal


def test_an_approve_that_names_the_current_tree_passes(tmp_path):
    # The green path of the same rule — asserted alongside the case above so the
    # identity is proven to have two answers, not one.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_the_legacy_rollup_path_warns_while_it_clears(tmp_path, capsys):
    # THE MIGRATION WINDOW (the plan's §6). An adopter holding a hand-authored
    # rollup keeps merging — and hears about it. The WARN is the whole point of
    # the window: a deprecation nobody is told about is a deprecation that never
    # happens, and this is the path an adopter is actually on.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None
    err = capsys.readouterr().err
    assert "LEGACY hand-authored rollup" in err
    assert "migration window" in err


def test_a_later_log_fragment_commit_does_not_stale_a_good_verdict(tmp_path):
    # The `:(exclude)docs/log.d` half of the freshness pathspec. A branch drops
    # its §5.1 log fragment as the LAST thing it does, routinely after the
    # review — if bookkeeping counted as code, the honest flow would stale its
    # own verdict every time and the gate would be unpassable. The previous test
    # (a real src/ commit at the same later stamp DOES stale it) is what proves
    # this is an exclusion rather than a broken comparison.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    fragment = root / "docs" / "log.d" / "WI-401-widget.md"
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text("## WI-401 — the widget\n", encoding="utf-8", newline="\n")
    _commit(root, "log: WI-401 fragment", when=T_LATER)

    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_only_the_merged_outcome_owes_a_verdict(tmp_path):
    # KEYED OFF THE OUTCOME, NOT THE CLAIM (WI-387, §A3). One repo, one missing
    # verdict, three answers: `merged` asserts the work is done and owes an
    # APPROVE; `cancelled` and `handback` assert the opposite and owe none.
    # Reading the requirement off the claim would deadlock the commonest
    # handback cause on itself — a review escalation is exactly the case where
    # no APPROVE exists, so the lane could not return the work it failed to get
    # approved.
    root = verdict_repo(tmp_path, policy="1")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is not None
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "cancelled"}) is None
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "handback"}) is None
    # ...and a MIXED branch is gated on its merged constituent alone.
    mixed = {"WI-401": "handback", "WI-402": "merged"}
    assert "WI-402-REVIEW-A.md" in integ._verdict_gate(root, "wi-401", mixed)


def test_a_malformed_review_policy_fails_closed(tmp_path):
    # A dial nobody can parse must never read as "0 = no review required". The
    # refusal quotes what it read, because the typo is the whole diagnosis.
    root = verdict_repo(tmp_path, policy="sometimes")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "docs/review-policy is not an integer" in refusal
    assert "sometimes" in refusal and "fail closed" in refusal


# --- 4. the declared bar (§4): undeclared is a refusal, never a skip ----------


def _stack_ini(tmp_path, text):
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stack.ini").write_text(text, encoding="utf-8", newline="\n")
    return tmp_path


def test_an_absent_stack_ini_is_a_refusal(tmp_path):
    (tmp_path / "docs").mkdir()
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None and "docs/stack.ini is absent" in refusal


def test_a_stack_ini_without_a_product_test_key_is_a_refusal(tmp_path):
    # A [product] section that declares format/lint but no test is a repo whose
    # bar was never stated. Skipping it is how `bar_failures: 0` came to mean
    # "nothing ran" (the §4.4 fail-open lesson).
    _stack_ini(tmp_path, "[product]\nformat = ruff format --check src\n")
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None and "no [product] test declaration" in refusal


def test_a_declared_but_empty_test_command_is_a_refusal(tmp_path):
    # The sharpest edge: the key EXISTS, so a "did they declare it?" check would
    # pass. An empty command is a misconfiguration, and it is named as one.
    _stack_ini(tmp_path, "[product]\ntest =\n")
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None and "declared but EMPTY" in refusal


def test_a_declared_test_command_passes_the_bar_declaration_check(tmp_path):
    _stack_ini(tmp_path, "[product]\ntest = {py} -m pytest -q\n")
    assert integ._declared_bar_or_refusal(tmp_path) is None


def test_a_declared_toolchain_without_its_venv_refuses_the_bar(tmp_path):
    # WI-361: the re-homed WI-286 floor. A repo that DECLARES the pinned toolchain
    # (requirements-dev.txt) but has no ./.venv would otherwise run the composed-
    # tree bar on the ambient interpreter, whose green may be false. The queue
    # refuses instead, loudly and by name, before it composes anything.
    _stack_ini(tmp_path, "[product]\ntest = {py} -m pytest -q\n")
    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None
    assert "harness floor REFUSES" in refusal
    assert "no runnable ./.venv" in refusal and "dev-setup --install" in refusal


def test_a_scaffold_that_declares_no_toolchain_still_runs_the_bar(tmp_path):
    # The arming boundary from the wired side: the SAME venv-less root without the
    # declaration is not refused. This is the property the whole venv-less fixture
    # fleet (including the e2e scaffolds in this file) depends on.
    _stack_ini(tmp_path, "[product]\ntest = {py} -m pytest -q\n")
    assert integ._declared_bar_or_refusal(tmp_path) is None


# --- 4b. the BRANCH tree's own harness (WI-368, relocated by WI-386) ----------
#
# These four covered "the COMPOSED tree's copy of the harness must run, not the
# invoker's" — and the composed tree is exactly what WI-386 deleted. The
# behaviour did not go with it: the refresh regenerates and bars the BRANCH
# tree, and the invoker is still trunk-vintage whenever drive.py drives the loop
# in-process, so a branch that changes a generator must still be regenerated
# with its own copy. Coverage relocated, not deleted (the Phase 5 precedent).


def test_the_branch_trees_copy_wins_under_the_invokers_layout(tmp_path, monkeypatch):
    # The meta-repo shape: the invoker sits INSIDE --root, and the lane worktree
    # carries the same relative layout — the branch's copy must win, or a
    # branch that changed a generator is regenerated with the trunk's vintage
    # and refused by the refresh commit's own freshness floor (the WI-368 hit).
    root = tmp_path / "root"
    inv = root / "kit" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "lane"
    lane = wt / "kit" / "scripts"
    lane.mkdir(parents=True)
    (lane / "trunk_step.py").write_text("# branch\n", encoding="utf-8", newline="\n")
    got = integ._branch_tree_script(wt, root, "trunk_step.py")
    assert got == lane / "trunk_step.py"


def test_an_out_of_root_invoker_probes_the_known_layouts(tmp_path, monkeypatch):
    # The kit-source-against-a-scaffold shape (this suite's own e2e fixtures):
    # SCRIPTS is not under --root, so the relative-layout join cannot apply and
    # the scaffold's scripts/ copy is found by the known-layout probe.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "check.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "lane"
    (wt / "scripts").mkdir(parents=True)
    (wt / "scripts" / "check.py").write_text(
        "# branch\n", encoding="utf-8", newline="\n"
    )
    got = integ._branch_tree_script(wt, tmp_path / "repo", "check.py")
    assert got == wt / "scripts" / "check.py"


def test_a_branch_tree_without_the_script_falls_back_to_the_invoker(
    tmp_path, monkeypatch
):
    # A branch that predates the script (or carries no harness at all) must
    # still integrate: the invoker's copy is the declared fallback, not a crash
    # and not a silent skip.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "lane"
    wt.mkdir()
    got = integ._branch_tree_script(wt, tmp_path / "repo", "trunk_step.py")
    assert got == inv / "trunk_step.py"


def test_run_trunk_step_executes_the_branch_trees_copy(tmp_path, monkeypatch):
    # The seam itself, non-vacuous against the pre-fix wiring: the invoker's
    # copy exits 3, the branch tree's writes a sentinel — so a pass proves
    # WHICH copy ran, not merely that something exited 0.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text(
        "import sys\n\nsys.exit(3)\n", encoding="utf-8", newline="\n"
    )
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    root = tmp_path / "repo"
    root.mkdir()
    wt = tmp_path / "lane"
    (wt / "scripts").mkdir(parents=True)
    (wt / "scripts" / "trunk_step.py").write_text(
        'from pathlib import Path\n\nPath("sentinel.txt").write_text("branch\\n")\n',
        encoding="utf-8",
        newline="\n",
    )
    code, out = integ._run_trunk_step(wt, root)
    assert code == 0, out
    assert (wt / "sentinel.txt").read_text(encoding="utf-8") == "branch\n"


# --- 5. the RULING-6 window audit --------------------------------------------


def test_audit_flags_a_non_merge_trunk_commit_touching_product_paths(tmp_path, capsys):
    # RULING-6: product changes reach the trunk only through the integrator's
    # merge. A direct commit is named by sha AND by the path that convicted it,
    # so the finding is reviewable without re-running git.
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    (root / "src").mkdir()
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: straight onto the trunk", when=T_CODE)
    sha = _rev(root, "HEAD")

    assert integ.audit(root, base) == 1
    err = capsys.readouterr().err
    assert sha[:10] in err
    assert "src/widget.py" in err


def test_audit_passes_a_window_of_bookkeeping_commits_only(tmp_path, capsys):
    # The coordinator's own surfaces — the claim move, the fragment drop, the
    # compiled log — are content-free serial bookkeeping and are exactly what
    # the integrator itself commits during a run.
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    write_spec(root, "queued", "WI-401")
    _commit(root, "claim: bookkeeping", when=T_CODE)
    fragment = root / "docs" / "log.d" / "WI-401-widget.md"
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text("## WI-401 — the widget\n", encoding="utf-8", newline="\n")
    _commit(root, "log: fragment", when=T_VERDICT)
    (root / "docs" / "log.md").write_text(
        "# Log\n\n## WI-401 — the widget\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "log: compile", when=T_LATER)

    assert integ.audit(root, base) == 0
    assert "audit clean" in capsys.readouterr().out


def test_audit_allows_product_changes_that_arrive_by_a_no_ff_merge(tmp_path, capsys):
    # The permitted shape, and the reason the audit reads `--first-parent
    # --no-merges`: the merge commit itself is excluded, and the branch's own
    # commits are not on the trunk's first-parent chain. A rule that flagged
    # these would flag the integrator's entire purpose.
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "src").mkdir()
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: the widget", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "--no-ff", "-m", "integrate: merge wi-401 (WI-401)", "wi-401")

    assert (root / "src" / "widget.py").is_file()  # the product change did land
    assert integ.audit(root, base) == 0
    assert "audit clean" in capsys.readouterr().out
