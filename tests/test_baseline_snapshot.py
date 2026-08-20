"""baseline_snapshot.py — the `last_approved` snapshot (owner directive
2026-08-15; docs/plans/2026-08-15-baseline-snapshot-design.md).

The mechanism replaces a DERIVED baseline (a git walk for the newest commit at
which a row read `Approved`) with a copied one. Its whole value rests on four
properties, and each gets a red->green test here:

  * drift is measured against the copy, over a real tree, and only RATIFIED
    cells arm it;
  * an approval whose snapshot copy does not claim approval is UNANCHORED —
    the case that is only decidable because the copy is a WHOLE FILE carrying
    each row's own `Status`;
  * the mirror invariant catches a hand-edited, partial, or copy-then-amend
    snapshot in the commit that does it;
  * the FIRST snapshot cannot be created by accident — not by the mechanical
    flip, and not by any loop module, hook, or `check.py`.

Fixtures are built by copying THIS repo's real registries into a tmp tree
rather than by writing miniature ones: the mechanism's failure modes are about
carriers, whole-file copying and cell classification, and a hand-rolled
two-row fixture would exercise none of them honestly.
"""

import shutil
import subprocess

from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

SNAP = load_script("baseline_snapshot")
CT = load_script("check_trajectory")

SR_REL = "docs/requirements/system-requirements.toml"


def _tree(tmp_path):
    """A tmp repo carrying this repo's seven real registries at their real
    paths. Everything the module reads resolves off `root`, so nothing else of
    the repo needs to come along."""
    root = tmp_path / "repo"
    for rel in SNAP.SNAPSHOTTED:
        src = ROOT / rel
        if not src.is_file():
            continue
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    return root


def _seeded(tmp_path):
    """`_tree` plus its first snapshot — the post-signing steady state every
    reader test starts from."""
    root = _tree(tmp_path)
    SNAP.copy_live(root, seed=True)
    return root


def _rewrite(root, rel, old, new):
    """One substring edit to a live registry, asserted to have actually
    changed something — a fixture that silently matched nothing would make
    every assertion below vacuously true."""
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, "fixture substring not found: " + old
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _first_row_at(root, status):
    """`(id, row)` of the first SR carrying `status`, from the LIVE tree."""
    spine_carrier = load_script("spine_carrier")
    for row in spine_carrier.load(root / SR_REL, "SR-ID", keep_examples=False):
        if (row.get("Status") or "").strip().lower() == status:
            return row["SR-ID"], row
    raise AssertionError("no SR at status " + status + " in the fixture")


# --- vacuity: the only honest empty state -------------------------------------


def test_with_no_snapshot_every_reader_is_vacuous_by_ABSENCE_not_by_silence(tmp_path):
    # The pre-signing state, which is also every fresh adopter's state. `None`
    # rather than `{}` is the whole point: `{}` claims "the snapshot recorded no
    # rows", which a drift reader would read as "nothing is anchored" and red
    # the entire spine.
    root = _tree(tmp_path)
    assert SNAP.exists(root) is False
    assert SNAP.load_all(root) is None
    assert SNAP.unanchored_findings(root) == []
    # ...and the None sentinel is collapsed in exactly ONE place, so no caller
    # has to invent its own `or {}`.
    assert SNAP.rows_for(None, SR_REL, "SR-ID") == {}


def test_a_SCAFFOLDED_but_unsigned_snapshot_is_VACUOUS_TOO(tmp_path):
    """THE STATE EVERY FRESH ADOPTER SHIPS IN, and the one a directory-existence
    test gets wrong. `bootstrap.py` scaffolds `docs/archive/last_approved/` with
    its README and nothing else, deliberately — so a vacuum keyed on the
    DIRECTORY would report all eight tiers missing in every new repo on day one,
    which is precisely the reds-everything failure the design defers arming to
    avoid. The vacuum is keyed on "holds no registry" instead. (Found when the
    producer was first wired to trace.py — adversarial round 2, 2026-08-15.)"""
    root = _tree(tmp_path)
    snap = SNAP.snapshot_root(root)
    snap.mkdir(parents=True)
    (snap / "README.md").write_text("# stamp\n", encoding="utf-8")
    assert SNAP.exists(root) is True  # the directory really is there...
    assert SNAP.unanchored_findings(root) == []  # ...and it still claims nothing
    # The pin is only worth having if bootstrap really does scaffold it so.
    boot = (SCRIPTS / "bootstrap.py").read_text(encoding="utf-8")
    assert "docs/archive/last_approved/README.md" in boot


# --- the bootstrap guard ------------------------------------------------------


def test_copy_live_REFUSES_to_create_the_snapshot_without_seed(tmp_path):
    # The first snapshot blesses whatever text it copies, so it must ride the
    # owner's reviewed signing commit and nothing else. Refusal, not creation.
    root = _tree(tmp_path)
    try:
        SNAP.copy_live(root)
    except SystemExit as exc:
        assert "REFUSED" in str(exc) and "--seed" in str(exc)
    else:
        raise AssertionError("copy_live created the snapshot without --seed")
    assert not SNAP.snapshot_root(root).exists()


def test_the_mechanical_flip_is_vacuous_before_the_first_signing(tmp_path):
    # The other half of the same rule, and the one a hard refusal would break:
    # `intake._apply_flips` must NOT fail for want of a snapshot, or the
    # adjudication path dies in every repo that has not signed yet.
    root = _tree(tmp_path)
    assert SNAP.exists(root) is False  # so intake's guard short-circuits
    intake_src = (SCRIPTS / "intake.py").read_text(encoding="utf-8")
    assert "if flipped and baseline_snapshot.exists(root):" in intake_src


def test_seed_is_unreachable_from_every_loop_module_and_hook():
    """THE SEED PIN (design §F1). `--seed` writes the record that a human
    blessed the spine. Nothing that runs unattended may be able to reach it —
    not the loop, not the dispatcher, not a hook, not `check.py`. A grep, and
    deliberately a grep: the property is "this token does not appear", which no
    call-graph analysis states more directly."""
    watched = [
        SCRIPTS / name
        for name in (
            "agent_loop.py",
            "dispatch.py",
            "agent_session.py",
            "agent_route.py",
            "check.py",
            "integrate.py",
            "handback.py",
        )
    ] + sorted((ROOT / "project-trajectory" / "hooks").iterdir())
    offenders = []
    for path in watched:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in ("--seed", "seed=True"):
            if token in text:
                offenders.append("{}: {}".format(path.name, token))
    assert not offenders, (
        "the snapshot SEED is reachable from an unattended path — the first "
        "snapshot must be the owner's deliberate act: " + ", ".join(offenders)
    )
    # The pin is only worth having if the token really is the reachable one.
    assert "--seed" in (SCRIPTS / "intake.py").read_text(encoding="utf-8")


# --- copy_live's own contract -------------------------------------------------


def test_the_copy_is_byte_for_byte_and_preserves_repo_relative_paths(tmp_path):
    root = _seeded(tmp_path)
    base = SNAP.snapshot_root(root)
    for rel in SNAP.SNAPSHOTTED:
        if not (root / rel).is_file():
            continue
        copied = base / rel
        assert copied.is_file(), rel + " was not copied"
        assert copied.read_bytes() == (root / rel).read_bytes(), rel


def test_a_stale_other_carrier_file_is_DELETED_in_the_same_act(tmp_path):
    # Without this, `spine_carrier.resolve` hard-fails with "exists under BOTH
    # carriers" on the very next read of the snapshot — the mechanism bricked by
    # a carrier change it was supposed to survive.
    root = _seeded(tmp_path)
    base = SNAP.snapshot_root(root)
    stale = base / "docs/requirements/system-requirements.csv"
    stale.write_text("SR-ID,Title,Status\nSR-001,x,Approved\n", encoding="utf-8")
    # Both carriers present: the resolver refuses, which is the state to clear.
    spine_carrier = load_script("spine_carrier")
    try:
        spine_carrier.resolve(base / SR_REL)
    except SystemExit as exc:
        assert "BOTH carriers" in str(exc)
    else:
        raise AssertionError("the dual-carrier state did not refuse")
    SNAP.copy_live(root)
    assert not stale.exists(), "the stale carrier survived a re-copy"
    assert spine_carrier.resolve(base / SR_REL) is not None


# --- drift --------------------------------------------------------------------


def test_a_ratified_cell_moving_under_an_approved_row_is_DRIFT(tmp_path):
    root = _seeded(tmp_path)
    sid, _row = _first_row_at(root, "approved")
    snapshot = SNAP.load_all(root)
    before = SNAP.rows_for(snapshot, SR_REL, "SR-ID")
    live = {
        r["SR-ID"]: r for r in load_script("spine_carrier").load(root / SR_REL, "SR-ID")
    }
    # Green first: a freshly copied tree has drifted nowhere. Without this the
    # assertion below could pass on a comparison that always says "changed".
    assert not SNAP.is_drifted(SR_REL, "SR-ID", live[sid], before)
    _rewrite(root, SR_REL, live[sid]["Title"], live[sid]["Title"] + " (amended)")
    live2 = {
        r["SR-ID"]: r for r in load_script("spine_carrier").load(root / SR_REL, "SR-ID")
    }
    assert SNAP.is_drifted(SR_REL, "SR-ID", live2[sid], before)
    assert set(SNAP.drifted_cells(SR_REL, "SR-ID", live2[sid], before)) == {"Title"}


def test_a_TRACED_cell_moving_is_NOT_drift(tmp_path):
    # The WI-388 ruling, unchanged by the new baseline: re-pointing what a
    # requirement answers to routes to ADJUDICATION and never arms a re-attest
    # window. If this ever flips, the re-tier campaign arms a window on every
    # row it touches, which is the noise that gets a window ignored.
    root = _seeded(tmp_path)
    snapshot = SNAP.load_all(root)
    before = SNAP.rows_for(snapshot, SR_REL, "SR-ID")
    sid, row = _first_row_at(root, "approved")
    moved = dict(row, Phase="99")  # `Phase` is declared TRACED for the SR tier
    assert CT.spine_cell_class(SR_REL, "Phase") == "traced"
    assert not SNAP.is_drifted(SR_REL, "SR-ID", moved, before)


def test_a_row_below_approval_can_never_be_drifted(tmp_path):
    # It has made no claim to fall from. A Drafted row differing from its snapshot
    # copy is work in progress, not a broken attestation. The live registries
    # carry no Drafted row since the 2026-08-20 signing, so the fixture makes
    # its own (first SR flipped pre-seed) rather than borrowing one.
    root = _tree(tmp_path)
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    SNAP.copy_live(root, seed=True)
    snapshot = SNAP.load_all(root)
    before = SNAP.rows_for(snapshot, SR_REL, "SR-ID")
    sid, row = _first_row_at(root, "drafted")
    amended = dict(row, Title=(row.get("Title") or "") + " (amended)")
    assert amended["Title"] != before[sid].get("Title")
    assert not SNAP.is_drifted(SR_REL, "SR-ID", amended, before)


def test_status_itself_is_never_the_amendment(tmp_path):
    # `Status` is the MARKER, not the content: folding it into the comparison
    # would make every flip look like an amendment and every real amendment
    # invisible behind its own flip.
    root = _seeded(tmp_path)
    before = SNAP.rows_for(SNAP.load_all(root), SR_REL, "SR-ID")
    sid, row = _first_row_at(root, "approved")
    assert not SNAP.is_drifted(SR_REL, "SR-ID", dict(row, Status="Approved"), before)


# --- the OFF-SPINE tiers, which carry no `Status` at all -----------------------
#
# `SNAPSHOTTED` copies interfaces/external/components precisely because their
# maturity cells move only by human hand. Until adversarial round 2 (2026-08-15)
# `_claims_approval` read `Status` alone, so every one of those rows answered
# False, was never drift-compared, and the copies recorded nothing anyone would
# ever look at. These tests are the pin that this cannot silently return.

IF_REL = "docs/requirements/interfaces.toml"
CMP_REL = "docs/requirements/components.toml"


def _approved_offspine(tmp_path, rel, id_col, cell, live_value):
    """A seeded tree in which the FIRST row of `rel` reads approved-or-above on
    its own maturity cell, on BOTH sides of the comparison.

    The flip happens BEFORE the seed deliberately: every shipped IF and CMP row
    reads `Drafted` today, so a fixture that approved nothing would assert
    against a predicate that is False for the honest reason, and pass while
    proving nothing."""
    root = _tree(tmp_path)
    _rewrite(
        root,
        rel,
        '{} = "{}"'.format(cell.lower(), live_value[0]),
        '{} = "{}"'.format(cell.lower(), live_value[1]),
    )
    SNAP.copy_live(root, seed=True)
    rows = load_script("spine_carrier").load(root / rel, id_col, keep_examples=False)
    claiming = [r for r in rows if SNAP._claims_approval(r)]
    assert claiming, "fixture: no row claims approval on " + cell
    return root, claiming[0], [r for r in rows if not SNAP._claims_approval(r)]


def test_an_APPROVAL_cell_tier_is_drift_compared_like_the_spine(tmp_path):
    # IF (and the depth-0 frame) carry `Status` — the same cell as the spine
    # since 2026-08-17; they used to carry `Approval`, which is why this
    # off-spine drift comparison needed finding at all.
    root, row, unclaimed = _approved_offspine(
        tmp_path, IF_REL, "IF-ID", "Status", ("Drafted", "Approved")
    )
    before = SNAP.rows_for(SNAP.load_all(root), IF_REL, "IF-ID")
    assert not SNAP.is_drifted(IF_REL, "IF-ID", row, before)  # green first
    moved = dict(row, Contract=(row.get("Contract") or "") + " (amended)")
    assert SNAP.is_drifted(IF_REL, "IF-ID", moved, before)
    assert set(SNAP.drifted_cells(IF_REL, "IF-ID", moved, before)) == {"Contract"}
    # ...and a row that has NOT been approved still cannot drift: it has made no
    # claim to fall from, exactly as a Drafted SR cannot.
    assert unclaimed, "fixture: every row was approved, so the negative is vacuous"
    still_draft = dict(unclaimed[0], Contract="rewritten entirely")
    assert not SNAP.is_drifted(IF_REL, "IF-ID", still_draft, before)


def test_a_STATE_cell_tier_is_drift_compared_like_the_spine(tmp_path):
    # CMP carries `Status` too, whose ladder semantics are derive_gate's, not a
    # second set written here — `Approved` and `Founded` are the values that
    # table maps to Approved-or-above.
    root, row, _unclaimed = _approved_offspine(
        tmp_path, CMP_REL, "CMP-ID", "Status", ("Drafted", "Founded")
    )
    before = SNAP.rows_for(SNAP.load_all(root), CMP_REL, "CMP-ID")
    assert not SNAP.is_drifted(CMP_REL, "CMP-ID", row, before)  # green first
    moved = dict(row, Name=(row.get("Name") or "") + " (renamed)")
    assert SNAP.is_drifted(CMP_REL, "CMP-ID", moved, before)


def test_the_claimed_sets_are_DERIVED_from_derive_gates_one_ruled_table():
    """The anti-duplication pin. A hand-written literal set here would be a
    rival answer to "is this row settled", agreeing with `derive_gate` until
    someone edits one of them — and the ladder table is the declared one home."""
    dg = load_script("derive_gate")
    claimed = (dg.APPROVED, dg.FOUNDED)
    assert SNAP._APPROVAL_CELL_CLAIMED == frozenset(
        k for k, v in dg.BIF_MATURITY.items() if v in claimed
    )
    assert SNAP._STATE_CELL_CLAIMED == frozenset(
        k for k, v in dg.CMP_MATURITY.items() if v in claimed
    )
    # The values Sol's round-2 repro asked about, stated outright so a table
    # edit that silently drops one has to come through this line. Title-case
    # since the registries speak the one enum; the predicate lower-cases before
    # the lookup, which is what lets the tables stay lowercase-keyed.
    assert SNAP._claims_approval({"Status": "Approved"})
    assert SNAP._claims_approval({"Status": "Founded"})
    assert not SNAP._claims_approval({"Status": "Drafted"})
    # The RETIRED CMP words claim nothing — `planned`/`verified` left the
    # vocabulary rather than being renamed, and a stray cell still carrying one
    # must read as unsettled rather than resolving through a stale table row.
    assert not SNAP._claims_approval({"Status": "verified"})
    assert not SNAP._claims_approval({"Status": "built"})


def test_the_SN_tier_is_COPIED_but_claims_nothing_BY_DECISION():
    """Design §B7, restated as a test so the omission cannot be mistaken for an
    oversight.

    The REASON changed on 2026-08-17 and the test is worth more for it: needs
    used to carry no maturity key, so the claim predicate had nothing to read
    and the omission proved itself. They now carry `status`, so the omission is
    a live choice — and what holds it is `SNAPSHOT_TIERS`, pinned below. Wiring
    SN drift to that cell is deliberately a separate pass; until then this is
    the line that would go red if someone wired it by accident."""
    assert SNAP.NEEDS_REL in SNAP.SNAPSHOTTED
    assert not any(rel == SNAP.NEEDS_REL for rel, _col in SNAP.SNAPSHOT_TIERS)


# --- unanchored, both directions ----------------------------------------------


def test_an_approved_row_ABSENT_from_the_snapshot_is_unanchored(tmp_path):
    root = _seeded(tmp_path)
    assert SNAP.unanchored_findings(root) == []  # green first
    sid, row = _first_row_at(root, "approved")
    # Delete the row from the SNAPSHOT copy: the live tree still claims it.
    snap_sr = SNAP.snapshot_root(root) / SR_REL
    text = snap_sr.read_text(encoding="utf-8")
    head, sep, _rest = text.partition("[requirement." + sid + "]")
    assert sep, "fixture: the row header was not found in the snapshot copy"
    nxt = _rest_after_row(_rest)
    snap_sr.write_text(head + nxt, encoding="utf-8")
    found = SNAP.unanchored_findings(root)
    assert any(sid in f and "ABSENT" in f for f in found), found


def _rest_after_row(rest):
    """Everything from the NEXT `[requirement.` header onward — a crude but
    honest row delete for a fixture (the module under test never writes TOML)."""
    marker = "\n[requirement."
    at = rest.find(marker)
    return rest[at + 1 :] if at >= 0 else ""


def test_an_approval_whose_snapshot_copy_reads_BELOW_approval_is_unanchored(tmp_path):
    """THE CASE THE WHOLE DESIGN EXISTS FOR, and the strongest single argument
    for whole-file copying: the snapshot keeps each row's own `Status`, so a
    live row reading approved whose copy reads `Drafted` is provably an approval
    that never rode a copy. Row extraction would have deleted this evidence."""
    root = _seeded(tmp_path)
    sid, _row = _first_row_at(root, "approved")
    snap_sr = SNAP.snapshot_root(root) / SR_REL
    text = snap_sr.read_text(encoding="utf-8")
    head, sep, rest = text.partition("[requirement." + sid + "]")
    assert sep
    rest = rest.replace('status = "Approved"', 'status = "Drafted"', 1)
    snap_sr.write_text(head + sep + rest, encoding="utf-8")
    found = SNAP.unanchored_findings(root)
    assert any(sid in f and "Drafted" in f for f in found), found


def test_a_registry_missing_from_an_EXISTING_snapshot_is_reported(tmp_path):
    # Vacuity has exactly one state and it is "no directory". Once the directory
    # exists, a hole inside it is a gap in the record, not an empty repo.
    root = _seeded(tmp_path)
    (SNAP.snapshot_root(root) / SR_REL).unlink()
    found = SNAP.unanchored_findings(root)
    assert any("is missing from the" in f and SR_REL in f for f in found), found


def test_an_unparseable_snapshot_REFUSES_rather_than_reading_as_empty(tmp_path):
    """`None` and `{}` are opposite claims. An empty read here means "no row was
    ever approved", which turns a broken file into a clean bill on every row.
    Unlike git history, a snapshot file is on disk and a person can fix it."""
    root = _seeded(tmp_path)
    (SNAP.snapshot_root(root) / SR_REL).write_text(
        "this is not [ toml", encoding="utf-8"
    )
    try:
        SNAP.load_all(root)
    except SystemExit as exc:
        assert "does not parse" in str(exc)
    else:
        raise AssertionError("an unreadable snapshot was reported as an empty one")


# --- the mirror invariant -----------------------------------------------------


def _git_tree(tmp_path):
    skip_without_env_gates("git")
    git = shutil.which("git")
    root = _tree(tmp_path)

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(root), *a], capture_output=True, text=True
        )

    run_git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    SNAP.copy_live(root, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "seed")
    return root, run_git


def test_a_clean_copy_satisfies_the_mirror_invariant(tmp_path):
    # Green first, and it must be green by CONSTRUCTION: a legitimate copy is
    # byte-for-byte and rides the same commit, so this can never warn.
    root, run_git = _git_tree(tmp_path)
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Approved"')
    SNAP.copy_live(root)
    run_git("add", "-A")
    assert CT.staged_snapshot_findings(root) == []


def test_a_HAND_EDITED_snapshot_fails_the_mirror_invariant(tmp_path):
    root, run_git = _git_tree(tmp_path)
    snap_sr = SNAP.snapshot_root(root) / SR_REL
    snap_sr.write_text(
        snap_sr.read_text(encoding="utf-8") + "\n# a human edited the record\n",
        encoding="utf-8",
    )
    run_git("add", "-A")
    found = CT.staged_snapshot_findings(root)
    assert any("byte-identical" in f and SR_REL in f for f in found), found


def test_a_PARTIAL_copy_fails_the_mirror_invariant(tmp_path):
    # The realistic slip: the live registry is amended and one snapshot file is
    # refreshed by hand while its sibling is forgotten.
    root, run_git = _git_tree(tmp_path)
    # RE-POINTED AT D-9 STEP 5: the first move was Verified->Planned, two live
    # values that FOLDED into one. Any real cell edit serves — this uses the
    # Title cell, which is ratified text and therefore exactly what a snapshot
    # is supposed to record.
    _rewrite(root, SR_REL, 'title = "', 'title = "amended ')
    shutil.copyfile(root / SR_REL, SNAP.snapshot_root(root) / SR_REL)
    # ...and now the live file moves AGAIN before the commit closes.
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    run_git("add", "-A")
    found = CT.staged_snapshot_findings(root)
    assert any("byte-identical" in f for f in found), found


def test_a_snapshot_file_DELETED_while_the_record_STANDS_fails_the_mirror(tmp_path):
    """The erasure the invariant did not watch (adversarial round 2, 2026-08-15).
    The deletion path exited silently, so the cheapest laundering was not to
    forge the record but to remove the page: `unanchored_findings` reports a row
    whose copy reads below it, and deleting the copy deletes that evidence."""
    root, run_git = _git_tree(tmp_path)
    (SNAP.snapshot_root(root) / SR_REL).unlink()
    run_git("add", "-A")
    found = CT.staged_snapshot_findings(root)
    assert any("DELETED" in f and SR_REL in f for f in found), found


def test_deleting_the_WHOLE_record_is_SILENT(tmp_path):
    """The other side of the same rule, and why it is 'while the rest stands'
    rather than 'never delete': retiring the mechanism, and the wholesale
    replacement §A1 describes, both remove files legitimately and neither leaves
    a hole. A rule that fired here would make its own design undeployable."""
    root, run_git = _git_tree(tmp_path)
    shutil.rmtree(SNAP.snapshot_root(root))
    run_git("add", "-A")
    assert CT.staged_snapshot_findings(root) == []


def test_the_snapshot_rules_are_ARMED_on_traces_INTEGRITY_floor():
    """D-9 MIGRATION STEP 7 — the arming, from both ends.

    This test used to assert the OPPOSITE and said so: the rule reached the
    advisory printer and was pinned OUT of `exit_code`, "the design arms it at
    migration step 7". This is that step, so the pin inverts.

    BOTH snapshot rules arm together, because they are one property read from
    two directions: UNANCHORED asks "did every approval ride a copy" and the
    MIRROR invariant asks "is every copy a copy". Either one alone leaves the
    record forgeable.

    Half source pin, half behavioural, and the split is deliberate: WHICH pipe
    a producer joins is a wiring fact only the source states, while the
    SEVERITY of that pipe is a real behaviour `exit_code` can be driven on.
    """
    trace = load_script("trace")
    text = (SCRIPTS / "trace.py").read_text(encoding="utf-8")
    # WIRING: both producers are called, and both land in the integrity list.
    assert "baseline_snapshot.unanchored_findings(" in text
    assert "check_trajectory.staged_snapshot_findings(" in text
    assert "findings.integrity += findings.snapshot_findings" in text
    # ...and NOT in the advisory printer any more, which is the half that
    # would otherwise leave the old severity standing beside the new one.
    printer = text.split("for a in (", 1)[1].split("):", 1)[0]
    assert "snapshot" not in printer, printer

    # SEVERITY, driven rather than read: an integrity finding fails the
    # always-on floor. `--strict-integrity` is the command the pre-commit hook
    # and the DevStg-Reqs `registry-integrity` step both run.
    class _Args:
        strict = False
        strict_integrity = True

    findings = trace.Findings()
    findings.integrity = []
    assert trace.exit_code(findings, _Args()) == 0
    findings.integrity = ["SR-001 reads Status=Approved but is ABSENT from ..."]
    assert trace.exit_code(findings, _Args()) == 1


def test_the_README_is_prose_and_is_exempt_from_the_mirror(tmp_path):
    # Design §F8 / repo-lock D-10's tripwire: the stamp is rendered, never
    # parsed, and has no live counterpart to mirror. If it were not exempt, a
    # signing commit would warn about its own README every time.
    root, run_git = _git_tree(tmp_path)
    (SNAP.snapshot_root(root) / "README.md").write_text("# stamp\n", encoding="utf-8")
    run_git("add", "-A")
    assert CT.staged_snapshot_findings(root) == []


def test_the_snapshot_dir_constant_has_one_value_in_both_homes():
    # `check_trajectory` restates the path rather than importing it (the import
    # edge runs the other way). Duplicated PLUMBING is sanctioned; a duplicated
    # constant with no behavioural pin is how the two silently point at
    # different directories.
    assert CT.SNAPSHOT_DIR == SNAP.SNAPSHOT_DIR


# --- the premise, ported from the retired digest suite ------------------------


def test_the_amendment_seam_is_BLIND_to_an_amend_plus_flip(tmp_path):
    """WHY A BASELINE OUTSIDE THE LIVE FILE IS FORCED — ported verbatim in
    substance from `tests/test_attestation_digest.py`, which retired with the
    digest machinery it covered. The reasoning it drives is unchanged and is
    the whole premise of the snapshot.

    `check_trajectory.staged_spine_amendments` — the function that MINTS an
    amendment adjudication — fires only when the row's status is unchanged
    across the two trees. So an amendment that flips its row in the SAME commit
    (the sanctioned path, and under D-9 the only path) is invisible to it. A
    baseline derived from that seam, or from the git walk that keyed off the
    flip, therefore cannot see the very change a sitting exists to judge. The
    snapshot is a baseline that is provably NOT the text under judgement,
    because the mirror invariant proves it was copied in an approval commit."""
    root, run_git = _git_tree(tmp_path)
    sid, row = _first_row_at(root, "approved")
    # Amend a ratified cell AND flip the row, in one staged change.
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended)")
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    run_git("add", "-A")
    seam = [a for a in CT.staged_spine_amendments(root) if a["id"] == sid]
    assert seam == [], "the seam saw an amend+flip it is documented to miss"
    # The snapshot, by contrast, still holds the pre-amendment text — which is
    # exactly the baseline the seam cannot supply.
    before = SNAP.rows_for(SNAP.load_all(root), SR_REL, "SR-ID")
    assert before[sid]["Title"] == row["Title"]


# --- the CLI surface ----------------------------------------------------------


def test_intake_snapshot_subcommand_seeds_then_refreshes(tmp_path):
    root = _tree(tmp_path)
    bare = run_py([SCRIPTS / "intake.py", "--root", str(root), "snapshot"], cwd=root)
    assert bare.returncode != 0, bare.stdout + bare.stderr
    assert "REFUSED" in (bare.stdout + bare.stderr)
    seeded = run_py(
        [SCRIPTS / "intake.py", "--root", str(root), "snapshot", "--seed"], cwd=root
    )
    assert seeded.returncode == 0, seeded.stdout + seeded.stderr
    assert "SEEDED" in seeded.stdout
    again = run_py([SCRIPTS / "intake.py", "--root", str(root), "snapshot"], cwd=root)
    assert again.returncode == 0, again.stdout + again.stderr
    assert "SEEDED" not in again.stdout
