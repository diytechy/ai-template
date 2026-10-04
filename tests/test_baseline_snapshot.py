"""baseline_snapshot.py — the `last_approved` snapshot (owner directive
2026-08-15; docs/plans/2026-08-15-baseline-snapshot-design.md).

The mechanism replaces a DERIVED baseline (a git walk for the newest commit at
which a row read `Approved`) with a copied one. Its whole value rests on five
properties, and each gets a red->green test here:

  * drift is measured against the copy, over a real tree, and only APPROVED
    cells arm it;
  * an approval whose snapshot copy does not claim approval is UNANCHORED —
    the case that is only decidable because the copy is a WHOLE FILE carrying
    each row's own `Status`;
  * the mirror invariant catches a hand-edited, partial, or copy-then-amend
    snapshot in the commit that does it;
  * the FIRST snapshot cannot be created by accident — not by the mechanical
    flip, and not by any loop module, hook, or `check.py`;
  * a REFRESH carries drifted approved text only for the rows its act flips or
    re-attests, never for a row beside them (SR-207, TC-240).

Fixtures are built by copying THIS repo's real registries into a tmp tree
rather than by writing miniature ones: the mechanism's failure modes are about
carriers, whole-file copying and cell classification, and a hand-rolled
two-row fixture would exercise none of them honestly.
"""

import inspect
import re
import shutil
import subprocess
from pathlib import Path

import pytest

# The tree helpers are shared with the in-process drift corners split out to
# `test_baseline_drift.py`.
from baseline_snapshot_fixtures import _first_row_at, _rewrite, _seeded, _tree
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
AR = load_script("acceptance_record")

SR_REL = "docs/requirements/system-requirements.toml"


def _seeded_with_a_drafted_sr(tmp_path):
    """A standing snapshot with one SR still below approval."""
    root = _tree(tmp_path)
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    SNAP.copy_live(root, seed=True)
    return root


def _append_new_approved_sr(root, sid):
    """Add a row to the LIVE SR registry that arrives already `Approved` — the
    shape that authorises a copy of its registry without any `Status` MOVE,
    because there is no snapshot copy of it to move from."""
    path = root / SR_REL
    row = (
        '\n[requirement.{}]\ntitle = "A row that arrives already approved"\n'
        'requirement = "The fixture shall carry a row with no snapshot copy."\n'
        'rationale = "The new-row arm of the authority question, driven."\n'
        'acceptance_criteria = "The row is present and claims approval."\n'
        'priority = "S"\nverification = "Test"\nstatus = "Approved"\nphase = 1\n'
    ).format(sid)
    with path.open("ab") as fh:
        fh.write(row.encode("utf-8"))


def test_approves_format_and_parse_share_one_multi_registry_syntax():
    approves = {
        "docs/test/test-cases.toml": "WI-572",
        "docs/requirements/low-level-requirements.toml": "WI-572",
    }
    rendered = SNAP.format_approves(approves)
    assert rendered == (
        "docs/requirements/low-level-requirements.toml=WI-572;"
        "docs/test/test-cases.toml=WI-572"
    )
    assert SNAP.parse_approves(rendered) == approves


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
    # The pin is only worth having if the bootstrap manifest really ships it.
    manifest = (SCRIPTS / "kitlib" / "bootstrap_manifest.py").read_text(
        encoding="utf-8"
    )
    assert "docs/archive/last_approved/README.md" in manifest


def test_the_shipped_README_describes_the_writer_that_exists():
    """The README scaffolded into every adopter's snapshot directory says how
    the record is written. The mechanical flip inside `intake.py adjudicate`
    that it once named as a second writer retired, and an amended row that
    still reads `Approved` is re-copied only when `--reattests` names it — so
    a README naming neither sends the adopter to a writer that is gone and a
    command that refuses."""
    tpl = SCRIPTS.parent / "registries" / "last-approved-README.template.md"
    text = tpl.read_text(encoding="utf-8")
    assert "mechanical flip" not in text
    assert "intake.py snapshot --reattests <ROW-ID>" in text
    # ONE writer, and both of its acts: the first approval rides a Status move.
    assert "One writer only: `scripts/intake.py snapshot`" in text
    assert "**A first approval** — move the row's `Status` to `Approved`" in text
    # A session on a rung the gate authority released DOES re-attest, so the
    # old blanket prohibition on the loop was false and must not come back.
    assert "unattended loop" not in text


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


def test_the_mechanical_flip_TOUCHES_NO_SNAPSHOT_AT_ALL(tmp_path):
    """RE-POINTED 2026-08-20 (the batch review's MINOR-12). This asserted the
    source string `if flipped and baseline_snapshot.exists(root):` — a guard on
    a `copy_live` call that had been UNREACHABLE since the D-9 step-7 refusal
    replaced the silent skip, so the test read as coverage of a path nothing
    could execute. The dead block is deleted; what is pinned now is the property
    that matters, driven rather than grepped: the mechanical path writes no
    snapshot, before OR after the first signing.

    The vacuity half survives with it — `_apply_flips` must not fail for want of
    a snapshot, or the adjudication path dies in every repo that has not signed
    yet, which is every fresh adopter."""
    intake = load_script("intake")
    root = _tree(tmp_path)
    assert SNAP.exists(root) is False
    # An already-blessed row is the ONE state this act tolerates. It returns
    # empty, raises nothing, and creates no record.
    sid, _row = _first_row_at(root, "approved")
    located, tables = intake._locate_spine_rows(root, {sid})
    assert intake._apply_flips(root, tables, located) == []
    assert not SNAP.snapshot_root(root).exists(), "the mechanical path seeded a record"
    # ...and with a record standing, it still writes nothing into it.
    SNAP.copy_live(root, seed=True)
    stamped = {p: p.read_bytes() for p in SNAP.snapshot_root(root).rglob("*.toml")}
    _rewrite(root, SR_REL, 'title = "', 'title = "amended ')
    located, tables = intake._locate_spine_rows(root, {sid})
    assert intake._apply_flips(root, tables, located) == []
    assert {p: p.read_bytes() for p in SNAP.snapshot_root(root).rglob("*.toml")} == (
        stamped
    ), "the mechanical path re-blessed text"
    # The ONE live `copy_live` caller in intake is the human path, and it is not
    # behind an `exists` guard — the guard belongs to the writer now.
    intake_src = (SCRIPTS / "intake.py").read_text(encoding="utf-8")
    assert intake_src.count("baseline_snapshot.copy_live(") == 1
    assert "root, seed=args.seed, approves=approves, reattests=reattests" in intake_src


# --- the authority gate on a REFRESH (2026-08-20) -----------------------------
# The hole the adversarial round executed end-to-end: `copy_live` refused only to
# CREATE the record, so after the first signing it re-blessed whatever text it was
# pointed at. Three tests for the three authorised paths, one for the laundering
# scenario itself.


def test_a_TRACED_only_refresh_needs_no_authority_at_all(tmp_path):
    """The common case, and the one that must stay free of a flag: the
    WI-482/WI-452 class (a `Module`/`CodeSymbol`/`TestRefs` re-point) moves no
    approved text, so the gate never fires. And since WI-571 it also authorises
    NO copy — a traced re-point flips no Status and is named by nothing, so the
    snapshot's whole-file copy of that registry simply lags live until a real
    approval rides it. Harmless: traced cells are never drift- or
    unanchored-compared, so a lagging copy of one changes no verdict."""
    root = _seeded(tmp_path)
    llr_rel = "docs/requirements/low-level-requirements.toml"
    before_llr = (SNAP.snapshot_root(root) / llr_rel).read_bytes()
    _rewrite(root, llr_rel, 'code_symbol = "', 'code_symbol = "renamed_')
    assert SNAP.refresh_refusal(root) == ""  # never refused...
    assert SNAP.copy_live(root) == []  # ...and authorises no copy
    assert (SNAP.snapshot_root(root) / llr_rel).read_bytes() == before_llr


def test_a_APPROVED_amendment_with_no_flip_and_no_ref_is_REFUSED(tmp_path):
    """THE LAUNDERING SCENARIO, executed. Rewrite an Approved requirement's
    approved text, then refresh: before this gate the copy landed, the drift
    vanished and every check went green with the record rewritten to match."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    before = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (quietly rewritten)")
    refusal = SNAP.refresh_refusal(root)
    assert "REFUSED" in refusal and sid in refusal and "Title" in refusal, refusal
    try:
        SNAP.copy_live(root)
    except SystemExit as exc:
        assert "REFUSED" in str(exc)
    else:
        raise AssertionError("the unauthorised refresh was written")
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == before


def test_an_AMEND_PLUS_FLIP_authorises_ITS_OWN_row_and_no_other(tmp_path):
    """Approval is a human moving a maturity cell in a reviewed commit, and the
    copy rides it — for THE ROW THAT MOVED. Until SR-207 this test pinned the
    wider reading: one flip anywhere in a registry authorised every approved
    amendment in it, so approving one row silently blessed another row's
    unreviewed edit. The flipped row's own amendment still rides its flip; an
    amended row beside it refuses the act by name."""
    root = _seeded_with_a_drafted_sr(tmp_path)
    draft_id, draft = _first_row_at(root, "drafted")
    sid, row = _first_row_at(root, "approved", {draft_id})
    _rewrite(root, SR_REL, draft["Title"], draft["Title"] + " (amended, then approved)")
    _rewrite(root, SR_REL, 'status = "Drafted"', 'status = "Approved"')
    assert SNAP.refresh_refusal(root) == ""  # the flip carries its own amendment...
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended beside it)")
    refusal = SNAP.refresh_refusal(root)  # ...and nothing else's
    assert "REFUSED" in refusal and sid in refusal and draft_id not in refusal, refusal
    assert SNAP.refresh_refusal(root, reattests={sid}) == ""
    assert SNAP.copy_live(root, reattests={sid})
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == (
        root / SR_REL
    ).read_bytes()


def test_an_explicit_APPROVES_ref_authorises_it_and_is_RECORDED(tmp_path):
    """The escape for the shape the D-9 ladder actually has: a sitting amends an
    Approved row's text without moving its Status. The ref is not validated —
    it is a human's citation of the act — but it is NAMED, and it lands in the
    snapshot's prose stamp, which is the difference between a deliberate
    re-blessing and a helper that always said yes."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended at the sitting)")
    # The ref NAMES its registry (WI-571) and, since SR-207, clears none of its
    # rows: the amended row is named by `reattests` or the act is refused.
    assert sid in SNAP.refresh_refusal(root, {SR_REL: "sitting-4"})
    assert SNAP.refresh_refusal(root, {SR_REL: "sitting-4"}, reattests={sid}) == ""
    SNAP.copy_live(root, approves={SR_REL: "sitting-4"}, reattests={sid})
    stamp = (SNAP.snapshot_root(root) / SNAP.README).read_text(encoding="utf-8")
    assert "sitting-4" in stamp
    assert "system-requirements.toml" in stamp  # the act's scope is recorded
    assert "re-attested: " + sid in stamp  # ...and the row it re-attested
    assert "Nothing parses it" in stamp  # still prose, design §F8
    # A second recorded refresh APPENDS rather than replacing the record.
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (again)")
    SNAP.copy_live(root, approves={SR_REL: "log 2026-08-20"}, reattests={sid})
    stamp2 = (SNAP.snapshot_root(root) / SNAP.README).read_text(encoding="utf-8")
    assert "sitting-4" in stamp2 and "log 2026-08-20" in stamp2


def test_each_act_is_a_typed_ledger_entry_naming_what_it_approved_and_re_attested(
    tmp_path,
):
    """The act ledger beside the copies is the machine record of each approval
    act (SR-202, LLR-239): which rows it approved and which it re-attested, one
    entry per act. The README stays prose that nothing reads. Two acts naming
    the same row in the same words on the same day are two entries, so the
    later act is never mistaken for the earlier one."""
    root = _seeded_with_a_drafted_sr(tmp_path)
    draft_id, _draft = _first_row_at(root, "drafted")
    sid, row = _first_row_at(root, "approved", {draft_id})
    (seed,) = SNAP.read_acts(root)
    assert sid in seed["approved"] and draft_id not in seed["approved"], seed
    assert seed["reattested"] == []
    _rewrite(root, SR_REL, 'status = "Drafted"', 'status = "Approved"')
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended)")
    SNAP.copy_live(root, reattests={sid})
    _rewrite(root, SR_REL, row["Title"] + " (amended)", row["Title"] + " (twice)")
    SNAP.copy_live(root, reattests={sid})
    acts = SNAP.read_acts(root)
    assert [(a["approved"], a["reattested"]) for a in acts[1:]] == [
        ([draft_id], [sid]),
        ([], [sid]),
    ], acts
    assert len({a["seq"] for a in acts}) == 3, acts
    stamp = (SNAP.snapshot_root(root) / SNAP.README).read_text(encoding="utf-8")
    assert "Nothing parses it" in stamp


def test_an_act_that_copies_nothing_adds_no_ledger_entry(tmp_path):
    root = _seeded(tmp_path)
    SNAP.copy_live(root)  # a traced-only refresh: nothing moved, nothing copied
    assert len(SNAP.read_acts(root)) == 1


def test_a_DRAFTED_rows_amendment_is_not_absorption(tmp_path):
    """The record of what was blessed for a `Drafted` row is *nothing*, so a copy
    that carries its new text re-blesses nothing — the gate never fires. And
    since WI-571 an amendment that flips no Status and is named by nothing
    authorises no copy at all, so ordinary drafting leaves the snapshot alone."""
    root = _tree(tmp_path)
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    SNAP.copy_live(root, seed=True)
    sid, row = _first_row_at(root, "drafted")
    before_sr = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (still drafting)")
    assert SNAP.refresh_refusal(root) == ""
    assert SNAP.copy_live(root) == []
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == before_sr


# --- the copy is SCOPED to the act (WI-571) -----------------------------------
# `copy_live` used to mirror all seven registries on every refresh, so a spine
# `Status` flip re-sealed whatever off-spine drift was live at that moment and
# silently zeroed the off-spine census (the only rendering of it is computed
# against the snapshot). The copy now moves ONLY the registry the act
# authorises: the one a `Status` moved in, plus every registry `--approves`
# names. The rest keep their bytes.

IF_REL = "docs/requirements/interfaces.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"
# A non-`status` cell of the first shipped interface row — off-spine drift that
# authorises nothing, so a spine-only act must leave its snapshot copy alone.
_IF_DRIFT_FROM = "printed whole for the harness"
_IF_DRIFT_TO = "printed WHOLE for the harness"


def test_a_spine_flip_LEAVES_the_offspine_snapshot_bytes_UNTOUCHED(tmp_path):
    """The measured problem, driven: a `Status` flip in a spine registry copies
    THAT registry and no other. An off-spine registry that merely drifted in the
    same tree is NOT re-sealed, so the drift SURVIVES to its own census instead
    of being zeroed by a whole-tree copy riding a spine approval. No flag."""
    root = _seeded_with_a_drafted_sr(tmp_path)
    seed_if = (SNAP.snapshot_root(root) / IF_REL).read_bytes()
    _rewrite(root, IF_REL, _IF_DRIFT_FROM, _IF_DRIFT_TO)  # off-spine drift, live
    _rewrite(root, SR_REL, 'status = "Drafted"', 'status = "Approved"')  # the flip
    written = SNAP.copy_live(root)
    # the flipped registry moved...
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == (
        root / SR_REL
    ).read_bytes()
    assert any("system-requirements" in w for w in written)
    # ...and the off-spine one did NOT: its snapshot is still the seed bytes, and
    # it still differs from live, so the census the snapshot renders is intact.
    assert (SNAP.snapshot_root(root) / IF_REL).read_bytes() == seed_if
    assert (SNAP.snapshot_root(root) / IF_REL).read_bytes() != (
        root / IF_REL
    ).read_bytes()
    assert not any("interfaces" in w for w in written)


def test_a_STATUS_MOVE_refresh_is_STAMPED_as_a_Status_move(tmp_path):
    """WI-571 rework: a refresh authorised by a `Status` move alone (no
    `--approves` ref) copied its registry but wrote NO stamp, so that approval
    act was unauditable in the prose the stamp promises to carry. Now every
    non-seed refresh that copies a registry is recorded — the seed writes no
    stamp, so the record here is written by the flip and names the copied
    registry with `Status move`, not a ref."""
    root = _seeded_with_a_drafted_sr(tmp_path)
    stamp_path = SNAP.snapshot_root(root) / SNAP.README
    assert not stamp_path.is_file(), "the seed must not write an approval stamp"
    _rewrite(root, SR_REL, 'status = "Drafted"', 'status = "Approved"')  # the flip
    written = SNAP.copy_live(root)  # no --approves: a Status move authorises it
    assert any("system-requirements" in w for w in written)
    stamp = stamp_path.read_text(encoding="utf-8")
    assert "system-requirements.toml" in stamp  # the copied registry is named...
    assert "Status move" in stamp  # ...and its reason is the flip, not a ref
    assert "Nothing parses it" in stamp  # still prose, design §F8


def test_a_DEAPPROVAL_cannot_authorise_an_unrelated_approved_amendment(tmp_path):
    """A reverse Status move is not an approval act.

    This is the two-row Review-A regression: treating every Status difference
    as a flip copied the whole SR registry, silently absorbing the second row's
    approved amendment. The one owner predicate now recognises only a transition
    into approval, so the amendment remains refused and snapshot bytes stay put.
    """
    root = _seeded(tmp_path)
    before = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    deapproved_id, _deapproved = _first_row_at(root, "approved")
    amended_id, amended = _first_row_at(root, "approved", {deapproved_id})
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    _rewrite(root, SR_REL, amended["Title"], amended["Title"] + " (amended)")

    ledger = SNAP.refresh_ledger(root)[SR_REL]
    assert deapproved_id not in ledger["flips"]
    assert amended_id in ledger["absorbed"]
    assert "REFUSED" in SNAP.refresh_refusal(root)
    try:
        SNAP.copy_live(root)
    except SystemExit as exc:
        assert "REFUSED" in str(exc)
    else:
        raise AssertionError("a de-approval authorised an unrelated amendment")
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == before


def test_a_named_ref_copies_EXACTLY_its_registry(tmp_path):
    """The `--approves` half of the scope: a ref names its registry, and the
    copy moves that one and nothing else, even with unrelated off-spine drift in
    the same tree."""
    root = _seeded(tmp_path)
    seed_if = (SNAP.snapshot_root(root) / IF_REL).read_bytes()
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended)")  # no flip
    _rewrite(root, IF_REL, _IF_DRIFT_FROM, _IF_DRIFT_TO)  # off-spine drift, live
    written = SNAP.copy_live(root, approves={SR_REL: "the sitting"}, reattests={sid})
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == (
        root / SR_REL
    ).read_bytes()
    assert (SNAP.snapshot_root(root) / IF_REL).read_bytes() == seed_if
    assert any("system-requirements" in w for w in written)
    assert not any("interfaces" in w for w in written)


def test_a_named_ref_mutes_ONLY_the_registry_it_names(tmp_path):
    """The secondary widening the plan names: a bare `--approves` used to short-
    circuit the whole gate (`if approves: return ""`), so one ref for one
    registry silenced all seven. The property that replaced it is about the
    COPY, not the message: a ref for the wrong registry cannot move the amended
    one's bytes. WI-584 removed the second half of the old assertion — a refusal
    NAMING the SR — because the copy it warned about is unreachable: an act
    scoped to the LLR does not write the SR, so the drift stands untouched, and
    the refusal was a block on an absorption that could not happen."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    before_sr = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended)")  # SR absorbs
    # A ref for a DIFFERENT registry does not carry the SR's amendment...
    written = SNAP.copy_live(root, approves={LLR_REL: "ref"})
    assert not any("system-requirements" in w for w in written), written
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == before_sr
    assert sid in SNAP.refresh_ledger(root)[SR_REL]["absorbed"]  # drift SURVIVES
    # ...and naming the SR itself does not move it either (SR-207): the ref
    # scopes the act to the registry, and only naming the ROW re-attests it.
    assert sid in SNAP.refresh_refusal(root, {SR_REL: "ref"})
    assert SNAP.refresh_refusal(root, {SR_REL: "ref"}, reattests={sid}) == ""


# --- the gate is scoped to the act, like the writer (WI-584) -------------------
# WI-571 scoped `copy_live` and left `refresh_refusal` global, so the gate judged
# registries the refresh would never write. The measured cost was that a
# per-registry approval could not complete its own act: the refusal listed only
# registries the caller had not ruled on, under a header saying nothing
# authorised it. The gate now judges the act's WRITE SET — with one arm kept
# unscoped, because an act that copies nothing must not exit 0 in silence.


def test_a_SCOPED_single_registry_approval_COMPLETES_over_unrelated_drift(tmp_path):
    """THE ACCEPTANCE WI-584 NAMES, driven end to end: a scoped, authorised,
    single-registry approval completes while approved text stands drifted in a
    registry the act does not touch. Before the ruling this exact call was
    REFUSED, and every row in the refusal was one the caller had not judged."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(
        root, SR_REL, row["Title"], row["Title"] + " (drift the act does not rule)"
    )
    _rewrite(root, LLR_REL, 'detail = "', 'detail = "Amended at the sitting. ')
    before_sr = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    # The row the sitting ruled, named as a re-attestation (SR-207): the ref
    # alone scopes the act to the LLR registry and clears none of its rows.
    ruled = set(SNAP.refresh_ledger(root)[LLR_REL]["absorbed"])
    assert len(ruled) == 1, ruled

    assert SNAP.refresh_refusal(root, {LLR_REL: "the sitting"}, reattests=ruled) == ""
    written = SNAP.copy_live(root, approves={LLR_REL: "the sitting"}, reattests=ruled)

    # the ruled registry is anchored...
    assert any("low-level-requirements" in w for w in written), written
    assert (SNAP.snapshot_root(root) / LLR_REL).read_bytes() == (
        root / LLR_REL
    ).read_bytes()
    # ...and the unruled one keeps BOTH its stale bytes and its visible drift,
    # which is what makes refusing on its behalf pointless.
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == before_sr
    assert sid in SNAP.refresh_ledger(root)[SR_REL]["absorbed"]


def test_an_unrelated_drift_cannot_block_a_FLIP_authorised_act_either(tmp_path):
    """The same defect on the commoner path, which is why the ruling had to be
    the general one: no `--approves` at all, just an amend-plus-flip in one
    registry while another carries drift. The global gate refused this too.

    The amendment is the FLIPPED row's own since SR-207. This test used to amend
    a different approved SR beside the flip and pass, which pinned the removed
    behaviour (any flip authorised its whole registry); the property it exists
    for — drift in registries the act does not write never blocks it — is
    unchanged."""
    root = _seeded_with_a_drafted_sr(tmp_path)
    draft_id, draft = _first_row_at(root, "drafted")
    _rewrite(
        root, IF_REL, _IF_DRIFT_FROM, _IF_DRIFT_TO
    )  # off-spine, authorises nothing
    _rewrite(root, TC_REL, 'method = """', 'method = """Amended, unruled. ')  # drift
    _rewrite(root, SR_REL, draft["Title"], draft["Title"] + " (amended)")
    _rewrite(root, SR_REL, 'status = "Drafted"', 'status = "Approved"')  # the flip

    assert SNAP.refresh_refusal(root) == ""
    written = SNAP.copy_live(root)
    assert [w for w in written if "system-requirements" in w] and not [
        w for w in written if "test-cases" in w or "interfaces" in w
    ], written


def test_an_act_that_would_copy_NOTHING_is_REFUSED_rather_than_silent(tmp_path):
    """THE ARM THAT SURVIVES THE SCOPING. Scoping the gate to the write set
    would make the laundering scenario a silent no-op — nothing is authorised,
    so nothing is written, so nothing is judged, exit 0. The drift survives
    either way (the writer has been scoped since WI-571), but exit 0 is the
    wrong answer to "you have rewritten blessed text", so an act with an EMPTY
    write set is judged over the whole ledger, as it always was."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (quietly rewritten)")
    refusal = SNAP.refresh_refusal(root)
    assert "REFUSED" in refusal and sid in refusal, refusal
    assert "would copy NOTHING" in refusal, refusal


def test_a_registry_WRITTEN_for_another_reason_still_gates_its_amendments(tmp_path):
    """The residual case the scoped gate must keep catching, and the reason it
    is not vacuous. A brand-new row arriving already `Approved` puts its registry
    in the write set — it must, or the row strands as `unanchored_findings` — so
    the copy WOULD land, carrying an unrelated approved amendment with it. That
    amendment moved no `Status` and is named by nothing, so it is refused."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended, unruled)")
    before_sr = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    _append_new_approved_sr(root, "SR-999")

    # the new row DOES put its registry in the act's write set...
    assert SR_REL in SNAP._authorised_registries(root, None, SNAP.load_all(root))
    # ...and that is exactly why the amendment riding along is refused.
    refusal = SNAP.refresh_refusal(root)
    assert "REFUSED" in refusal and sid in refusal, refusal
    assert "This act WRITES" in refusal and "system-requirements.toml" in refusal
    try:
        SNAP.copy_live(root)
    except SystemExit as exc:
        assert "REFUSED" in str(exc)
    else:
        raise AssertionError("an unruled amendment rode a new row's anchor in")
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == before_sr


def test_a_RESEED_over_a_standing_record_is_judged_over_the_WHOLE_tree(tmp_path):
    """`--seed` against a standing record writes all seven registries, so its
    write set IS the whole tree and the scoped gate is the global one. Scoping
    must not turn the re-seed into the laundering path the gate closed."""
    root = _tree(tmp_path)
    _rewrite(root, LLR_REL, 'status = "Approved"', 'status = "Drafted"')
    SNAP.copy_live(root, seed=True)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (amended)")
    _rewrite(root, LLR_REL, 'status = "Drafted"', 'status = "Approved"')  # a real flip
    # The flip alone would scope a refresh to the LLR and clear the SR's gate...
    assert SNAP.refresh_refusal(root) == ""
    # ...but a re-seed would rewrite the SR too, so it is judged and refused.
    refusal = SNAP.refresh_refusal(root, seed=True)
    assert "REFUSED" in refusal and sid in refusal, refusal
    try:
        SNAP.copy_live(root, seed=True)
    except SystemExit as exc:
        assert "REFUSED" in str(exc)
    else:
        raise AssertionError("a re-seed absorbed an unauthorised amendment")


def test_the_SEED_still_copies_the_WHOLE_tree(tmp_path):
    """The seed is unchanged: it blesses the whole tree once, on the owner's
    signing commit. Scope is a REFRESH-time property; the first copy is total."""
    root = _tree(tmp_path)
    SNAP.copy_live(root, seed=True)
    for rel in SNAP.SNAPSHOTTED:
        assert (SNAP.snapshot_root(root) / rel).is_file(), rel


def test_the_refusal_reaches_the_CLI_and_the_flag_clears_it(tmp_path):
    """End-to-end over the public path — `intake.py snapshot` is what a human
    and a worker actually run, and the review's laundering path went through it.
    A tmp tree carrying only the registries is enough: the command touches
    nothing else."""
    root = _seeded(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (laundered)")
    proc = run_py([SCRIPTS / "intake.py", "--root", root, "snapshot"], cwd=root)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "REFUSED" in proc.stdout + proc.stderr
    approves = ["--approves", "system-requirements.toml=sitting-4"]
    proc = _snapshot_cli(root, *approves)  # the registry alone clears no row
    assert proc.returncode != 0 and sid in proc.stderr, proc.stdout + proc.stderr
    proc = _snapshot_cli(root, *approves, "--reattests", sid)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "APPROVED BY: system-requirements.toml=sitting-4" in proc.stdout
    assert "RE-ATTESTED: " + sid in proc.stdout


def _snapshot_cli(root, *args):
    """`intake.py snapshot` run over `root` the way a person or a session runs it."""
    return run_py([SCRIPTS / "intake.py", "--root", root, "snapshot", *args], cwd=root)


# --- row-level refusal (SR-207, LLR-245; TC-240) -------------------------------
# The refusal used to be decided per REGISTRY: a `Status` flip anywhere in a
# registry, or an `--approves` ref naming it, authorised every approved amendment
# in it, so approving one row blessed another row's unreviewed edit. It is decided
# per ROW now: the act's absorbed rows, minus the rows it flips, minus the rows it
# names with `--reattests`, must be empty. Every case is parameterized off
# `SNAPSHOT_TIERS` itself, so a tier added there later — the assumptions
# registry's two — runs through these same cases with no edit here.

_SPINE_CARRIER = load_script("spine_carrier")


def _ids(id_col, n):
    """`n` fixture row ids for one tier, far above any live id (`SR-9001`...)."""
    prefix = id_col[: -len("ID")]
    return ["{}9{:03d}".format(prefix, i) for i in range(1, n + 1)]


def _block(id_col, rid, status, title):
    """One appended TOML row of tier `id_col`: a `title`, which is an approved
    cell on every compared tier, and a `status` that claims approval or not."""
    return '\n[{}.{}]\ntitle = "{}"\nstatus = "{}"\n'.format(
        _SPINE_CARRIER.REGISTRY_TABLE[id_col], rid, title, status
    )


def _append(root, rel, text):
    """Append rows to a live registry as bytes (line endings untouched, as in
    `_rewrite`), creating it for a tier whose file this tree does not carry."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as fh:
        fh.write(text.encode("utf-8"))


def _approve(root, rel, id_col, rid, title):
    """The approval act's own `Status` move on one appended row."""
    _rewrite(
        root,
        rel,
        _block(id_col, rid, "Drafted", title),
        _block(id_col, rid, "Approved", title),
    )


def _last_stamp_line(root):
    text = (SNAP.snapshot_root(root) / SNAP.README).read_text(encoding="utf-8")
    return text.strip().splitlines()[-1]


def _shared_file_pairs():
    """`(registry, approved tier, drifted tier)` for every registry holding more
    than one tier: each tier approves while the next one round drifts."""
    by_rel = {}
    for rel, col in SNAP.SNAPSHOT_TIERS:
        by_rel.setdefault(rel, []).append(col)
    return [
        pytest.param(rel, cols[i], cols[(i + 1) % len(cols)], id=cols[i])
        for rel, cols in by_rel.items()
        if len(cols) > 1
        for i in range(len(cols))
    ]


_TIERS = [pytest.param(rel, col, id=col) for rel, col in SNAP.SNAPSHOT_TIERS]
_SHARED = _shared_file_pairs()


def test_the_row_rule_is_driven_over_EVERY_compared_tier():
    """The parameter lists ARE `SNAPSHOT_TIERS`, and hold every tier TC-240
    names: the spine's three, interfaces, components, the frame's three, the
    assumptions registry's two (assumptions and surrogates, which share one
    file), and the needs file's two (needs and stakeholders). The cases below take their parameters from the table itself, so
    nothing here can drift from the table that decides which rows are
    compared."""
    assert [tuple(p.values) for p in _TIERS] == list(SNAP.SNAPSHOT_TIERS)
    named = {"SR-ID", "LLR-ID", "TC-ID", "IF-ID", "CMP-ID", "EXT-ID", "B-ID", "REL-ID"}
    named |= {"DA-ID", "SUR-ID", "SN-ID", "STK-ID"}
    assert named <= {col for _rel, col in SNAP.SNAPSHOT_TIERS}
    assert _SHARED, "no registry holds two tiers, so the shared-file case is vacuous"


@pytest.mark.parametrize("rel,id_col", _TIERS)
def test_a_drifted_row_outside_the_act_REFUSES_it_until_the_act_names_it(
    tmp_path, rel, id_col
):
    """Row A is approved while row B of the same tier carries drifted approved
    text. The act is refused naming B and the cell; naming the registry alone in
    `--approves` does not clear B and copies nothing; naming B with
    `--reattests` clears it, and the act's record names B."""
    a, b = _ids(id_col, 2)
    seeded = _block(id_col, a, "Drafted", "Row A") + _block(
        id_col, b, "Approved", "Row B"
    )
    root, _git = _git_tree(tmp_path, lambda r: _append(r, rel, seeded))
    _approve(root, rel, id_col, a, "Row A")
    _rewrite(root, rel, 'title = "Row B"', 'title = "Row B, rewritten unread"')
    recorded = (SNAP.snapshot_root(root) / rel).read_bytes()
    named = "{} {}: Title".format(rel, b)
    ref = ["--approves", Path(rel).name + "=the-sitting"]

    bare = _snapshot_cli(root)
    assert bare.returncode != 0 and named in bare.stderr, bare.stdout + bare.stderr
    by_registry = _snapshot_cli(root, *ref)
    assert by_registry.returncode != 0, by_registry.stdout + by_registry.stderr
    assert named in by_registry.stderr, by_registry.stderr
    assert (SNAP.snapshot_root(root) / rel).read_bytes() == recorded

    by_row = _snapshot_cli(root, *ref, "--reattests", b)
    assert by_row.returncode == 0, by_row.stdout + by_row.stderr
    assert (SNAP.snapshot_root(root) / rel).read_bytes() == (root / rel).read_bytes()
    assert "re-attested: " + b in _last_stamp_line(root), _last_stamp_line(root)


@pytest.mark.parametrize("rel,approved_col,drifted_col", _SHARED)
def test_in_a_SHARED_file_one_tiers_drift_refuses_anothers_approval(
    tmp_path, rel, approved_col, drifted_col
):
    """Tiers sharing one file share one record copy, so a per-file authority
    let an approval in one tier carry another tier's drift."""
    (a,) = _ids(approved_col, 1)
    (b,) = _ids(drifted_col, 1)
    seeded = _block(approved_col, a, "Drafted", "Row A") + _block(
        drifted_col, b, "Approved", "Row B"
    )
    root, _git = _git_tree(tmp_path, lambda r: _append(r, rel, seeded))
    _approve(root, rel, approved_col, a, "Row A")
    _rewrite(root, rel, 'title = "Row B"', 'title = "Row B, rewritten unread"')
    proc = _snapshot_cli(root)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "{} {}: Title".format(rel, b) in proc.stderr, proc.stderr


def test_an_act_with_NO_drift_outside_it_refreshes_as_before(tmp_path):
    """The rule costs an act that carries no unattested drift nothing: one row
    approved in every compared tier at once, no flag, every registry copied."""
    rows = {(rel, col): _ids(col, 1)[0] for rel, col in SNAP.SNAPSHOT_TIERS}

    def prepare(root):
        for (rel, col), rid in rows.items():
            _append(root, rel, _block(col, rid, "Drafted", "Row A"))

    root, _git = _git_tree(tmp_path, prepare)
    for (rel, col), rid in rows.items():
        _approve(root, rel, col, rid, "Row A")
    proc = _snapshot_cli(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for rel, _col in SNAP.SNAPSHOT_TIERS:
        assert (SNAP.snapshot_root(root) / rel).read_bytes() == (
            root / rel
        ).read_bytes(), rel
    assert "Status move" in _last_stamp_line(root)


def test_SEVEN_drifted_rows_are_ALL_named_with_none_cut_off(tmp_path):
    """The refusal is the list a person works through; a capped list hides the
    rows past the cap until the first ones are dealt with."""
    a, *seven = _ids("SR-ID", 8)
    seeded = _block("SR-ID", a, "Drafted", "Row A") + "".join(
        _block("SR-ID", rid, "Approved", "Row " + rid) for rid in seven
    )
    root, _git = _git_tree(tmp_path, lambda r: _append(r, SR_REL, seeded))
    for rid in seven:
        _rewrite(root, SR_REL, 'title = "Row {}"'.format(rid), 'title = "Rewritten"')
    lines = ["{} {}: Title".format(SR_REL, rid) for rid in seven]
    refusal = SNAP.refresh_refusal(root)  # the whole-ledger arm...
    assert all(line in refusal for line in lines) and "more row" not in refusal
    _approve(root, SR_REL, "SR-ID", a, "Row A")  # ...and an act approving A
    proc = _snapshot_cli(root)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert [line for line in lines if line not in proc.stderr] == [], proc.stderr
    assert "more row" not in proc.stderr, proc.stderr


def test_a_drifted_NEED_refuses_the_act_until_the_act_names_it(tmp_path):
    """The needs file's two tiers are compared tiers (SR-207): an approved need
    whose text moved refuses an act copying the needs registry, naming the need
    and the cell, however the registry is named; `--reattests SN-###` clears it,
    copies the registry and records the need in the act ledger."""
    root, _git = _git_tree(tmp_path)
    needs = SNAP.NEEDS_REL
    assert (needs, "SN-ID") in SNAP.SNAPSHOT_TIERS
    assert (needs, "STK-ID") in SNAP.SNAPSHOT_TIERS
    _rewrite(root, needs, 'why = "', 'why = "Amended, unread. ')
    recorded = (SNAP.snapshot_root(root) / needs).read_bytes()
    ref = ["--approves", Path(needs).name + "=the-sitting"]
    proc = _snapshot_cli(root, *ref)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "{} SN-001: Why".format(needs) in proc.stderr, proc.stderr
    assert (SNAP.snapshot_root(root) / needs).read_bytes() == recorded
    proc = _snapshot_cli(root, *ref, "--reattests", "SN-001")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (SNAP.snapshot_root(root) / needs).read_bytes() == (
        root / needs
    ).read_bytes()
    assert "SN-001" in SNAP.read_acts(root)[-1]["reattested"]


def test_parse_reattests_reads_comma_joined_row_ids_of_compared_tiers():
    assert SNAP.parse_reattests(None) == frozenset()
    assert SNAP.parse_reattests(" SR-012, LLR-061 ,,B-02, SN-001,STK-01") == {
        "SR-012",
        "LLR-061",
        "B-02",
        "SN-001",
        "STK-01",
    }
    # A work item and the `;` of the `--approves` idiom each name no row of a
    # compared tier; a refusal beats a re-attestation that matched nothing
    # while reading as though it had.
    for bad in ("WI-635", "SR-012;LLR-061", "sr-012"):
        with pytest.raises(SystemExit):
            SNAP.parse_reattests(bad)


def test_a_reattested_id_that_names_NO_row_is_refused(tmp_path):
    """A typo in `--reattests` would otherwise put a row nobody read into the
    act's record. Driven through `copy_live`, the writer every act passes."""
    root = _seeded(tmp_path)
    recorded = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    with pytest.raises(SystemExit) as refused:
        SNAP.copy_live(root, reattests={"SR-9999"})
    assert "REFUSED" in str(refused.value) and "SR-9999" in str(refused.value)
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == recorded


@pytest.mark.parametrize("rel,id_col", _TIERS)
def test_a_REMOVED_approved_row_is_absorbed_like_an_amendment(tmp_path, rel, id_col):
    """Deleting an approved row changes the record as surely as rewriting it:
    the copy drops the text a human blessed. The ledger reads the recorded rows
    as well as the live ones, so a removal is absorbed in every compared tier,
    those sharing a file included."""
    (b,) = _ids(id_col, 1)
    block = _block(id_col, b, "Approved", "Row B")
    root = _tree(tmp_path)
    _append(root, rel, block)
    SNAP.copy_live(root, seed=True)
    _rewrite(root, rel, block, "")
    assert b in SNAP.refresh_ledger(root)[rel]["absorbed"]


def test_a_REMOVED_approved_row_REFUSES_the_act_until_the_act_names_it(tmp_path):
    """Row A is approved while row B, approved and recorded, is deleted from the
    live registry. A flip scoped the registry and the copy carried the deletion
    into the record unnamed. Now the act is refused naming B as removed, a ref
    for the registry does not clear it, and naming B in `--reattests` is how the
    act blesses the removal: the record drops B and its stamp names B."""
    a, b = _ids("SR-ID", 2)
    removed = _block("SR-ID", b, "Approved", "Row B")
    seeded = _block("SR-ID", a, "Drafted", "Row A") + removed
    root, _git = _git_tree(tmp_path, lambda r: _append(r, SR_REL, seeded))
    _approve(root, SR_REL, "SR-ID", a, "Row A")
    _rewrite(root, SR_REL, removed, "")
    recorded = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    named = "{} {}: removed".format(SR_REL, b)
    ref = ["--approves", "system-requirements.toml=the-sitting"]

    bare = _snapshot_cli(root)
    assert bare.returncode != 0 and named in bare.stderr, bare.stdout + bare.stderr
    by_registry = _snapshot_cli(root, *ref)
    assert by_registry.returncode != 0, by_registry.stdout + by_registry.stderr
    assert named in by_registry.stderr, by_registry.stderr
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == recorded

    by_row = _snapshot_cli(root, *ref, "--reattests", b)
    assert by_row.returncode == 0, by_row.stdout + by_row.stderr
    copy = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    assert copy == (root / SR_REL).read_bytes() and b.encode() not in copy
    assert "re-attested: " + b in _last_stamp_line(root), _last_stamp_line(root)


def test_a_SEED_takes_no_reattests_and_names_no_phantom_row(tmp_path):
    """A first signing blesses the whole tree and writes no stamp, so there is
    nothing to re-attest and nowhere to record it. `--reattests` on a seed is
    refused, a nonexistent id first of all, before the directory is created;
    and a re-seed over a standing record refuses it too."""
    root = _tree(tmp_path)
    sid, _row = _first_row_at(root, "approved")
    for ids in ("SR-9999", sid):
        proc = _snapshot_cli(root, "--seed", "--reattests", ids)
        assert proc.returncode != 0, proc.stdout + proc.stderr
        assert "REFUSED" in proc.stderr and ids in proc.stderr, proc.stderr
        assert not SNAP.snapshot_root(root).exists()
    SNAP.copy_live(root, seed=True)
    recorded = (SNAP.snapshot_root(root) / SR_REL).read_bytes()
    proc = _snapshot_cli(root, "--seed", "--reattests", sid)
    assert proc.returncode != 0 and "REFUSED" in proc.stderr, proc.stderr
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() == recorded


def test_an_UNREADABLE_record_takes_no_reattests_either(tmp_path):
    """The repair path copies the whole tree as a first signing, because a
    record that does not parse cannot be compared, and it writes no stamp. So
    `--reattests` is refused there too, a nonexistent id included, and the
    repair itself still runs without the flag."""
    root = _seeded(tmp_path)
    snap_sr = SNAP.snapshot_root(root) / SR_REL
    snap_sr.write_text("this is not [ toml", encoding="utf-8")
    sid, _row = _first_row_at(root, "approved")
    for ids in ("SR-9999", sid):
        proc = _snapshot_cli(root, "--reattests", ids)
        assert proc.returncode != 0, proc.stdout + proc.stderr
        assert "REFUSED" in proc.stderr and ids in proc.stderr, proc.stderr
        assert snap_sr.read_text(encoding="utf-8") == "this is not [ toml"
    repair = _snapshot_cli(root)
    assert repair.returncode == 0, repair.stdout + repair.stderr
    assert snap_sr.read_bytes() == (root / SR_REL).read_bytes()


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
            "agent_brief.py",
            "agent_policy.py",
            "dispatch.py",
            "agent_session.py",
            "session_adapters.py",
            "session_service.py",
            "session_keep.py",
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

    The flip happens BEFORE the seed deliberately, and only where the registry
    still carries a non-claiming row to flip: when this fixture was written
    every shipped IF and CMP row read `Drafted`, so a fixture that approved
    nothing would have asserted against a predicate that is False for the
    honest reason. The owner approved all four CMP rows on 2026-08-22, so for
    CMP the live registry ALREADY carries claiming rows and there is nothing
    to flip — the closing `assert claiming` keeps the anti-vacuity teeth
    either way."""
    root = _tree(tmp_path)
    old = '{} = "{}"'.format(cell.lower(), live_value[0])
    if old.encode("utf-8") in (root / rel).read_bytes():
        _rewrite(
            root,
            rel,
            old,
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
    # CMP carries `Status` too, whose ladder semantics are spine_rules's, not a
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
    rival answer to "is this row settled", agreeing with `spine_rules` until
    someone edits one of them — and the ladder table is the declared one home."""
    dg = load_script("spine_rules")
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


def test_the_needs_files_two_tiers_are_COMPARED_tiers():
    """Needs carry `status` in the spine's words, and so do the stakeholders
    beside them, so both tiers are compared with their recorded copy like
    every other: the drift read, the refresh refusal, `--reattests`, the act
    ledger and the unanchored rule all walk `SNAPSHOT_TIERS`, which lists them
    (`NEED_TIERS`)."""
    assert SNAP.NEEDS_REL in SNAP.SNAPSHOTTED
    assert set(SNAP.NEED_TIERS) <= set(SNAP.SNAPSHOT_TIERS)
    assert SNAP._claims_approval({"Status": "Approved"})


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


def test_an_approved_NEED_or_STAKEHOLDER_without_its_anchor_is_unanchored(tmp_path):
    """The unanchored rule covers the needs file's two tiers: an approved need
    the record does not hold, and an approved stakeholder whose recorded copy
    reads below approval, are each an approval that never rode a copy."""
    root = _seeded(tmp_path)
    needs = SNAP.NEEDS_REL
    assert SNAP.unanchored_findings(root) == []
    path = root / needs
    with path.open("ab") as fh:
        fh.write(b'\n[need.SN-9001]\nstatus = "Approved"\nneed = "Unrecorded."\n')
    copy = SNAP.snapshot_root(root) / needs
    text = copy.read_bytes()
    at = text.index(b"[stakeholder.STK-01]")
    head, tail = text[:at], text[at:]
    tail = tail.replace(b'status = "Approved"', b'status = "Drafted"', 1)
    copy.write_bytes(head + tail)
    findings = SNAP.unanchored_findings(root)
    assert any(
        f.startswith("SN-9001 reads Status=Approved but is ABSENT") for f in findings
    ), findings
    assert any(
        f.startswith("STK-01 reads Status=Approved but its") and "Status=Drafted" in f
        for f in findings
    ), findings


def test_a_registry_missing_from_an_EXISTING_snapshot_is_reported(tmp_path):
    # Vacuity has exactly one state and it is "no directory". Once the directory
    # exists, a hole inside it is a gap in the record, not an empty repo.
    root = _seeded(tmp_path)
    (SNAP.snapshot_root(root) / SR_REL).unlink()
    found = SNAP.unanchored_findings(root)
    assert any("is missing from the" in f and SR_REL in f for f in found), found


@pytest.mark.parametrize(
    "rel,with_live",
    [
        pytest.param(SR_REL, True, id="SR-copy-deleted"),
        pytest.param(SR_REL, False, id="SR-deleted-with-its-copy"),
        pytest.param(IF_REL, True, id="IF-copy-deleted-no-approved-row"),
        pytest.param(IF_REL, False, id="IF-deleted-with-its-copy"),
    ],
)
def test_an_ESTABLISHED_registry_missing_from_the_record_is_ALWAYS_reported(
    tmp_path, rel, with_live
):
    """The no-copy-before-first-approval exception belongs to the registry that
    joined the record after it was first signed, and to it alone. For an
    established registry the hole is reported whatever its live rows claim:
    deleting the registry together with its copy leaves no row claiming
    approval, and a rule reading only the claims would let the deletion erase
    its own evidence."""
    assert SNAP.FIRST_COPY_AT_APPROVAL == (ASSUMPTIONS_REL,)
    root = _seeded(tmp_path)
    (SNAP.snapshot_root(root) / rel).unlink()
    if not with_live:
        (root / rel).unlink()
    found = SNAP.unanchored_findings(root)
    assert any("is missing from the" in f and rel in f for f in found), found


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


def _git_tree(tmp_path, prepare=None):
    """A real git repo over `_tree`, seeded and committed. `prepare(root)`, when
    given, shapes the live registries BEFORE the seed, so the rows it adds are
    part of what the first signing blessed."""
    skip_without_env_gates("git")
    git = shutil.which("git")
    root = _tree(tmp_path)
    if prepare is not None:
        prepare(root)

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


def test_a_SCOPED_refresh_leaves_the_UNTOUCHED_offspine_mirror_GREEN(tmp_path):
    """WI-571 against the mirror: a spine flip copies only the spine registry,
    so the off-spine registry it did NOT copy keeps its seed-commit bytes. Both
    mirror rules stay green with no flag, because each is pinned to the file it
    judges — the untouched file is never in the commit (staged) and still matches
    live at ITS OWN writing commit, the seed (committed). "An untouched file is
    not written." """
    root, run_git = _git_tree(tmp_path)
    seed_if = (SNAP.snapshot_root(root) / IF_REL).read_bytes()
    _rewrite(root, IF_REL, _IF_DRIFT_FROM, _IF_DRIFT_TO)  # off-spine drift, live
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')  # the flip
    SNAP.copy_live(root)  # no flag: the flip authorises the SR copy
    run_git("add", "-A")
    # The SR snapshot rode the flip and matches live; the interfaces snapshot was
    # never staged, so the staged rule has nothing to fault.
    assert CT.staged_snapshot_findings(root) == []
    run_git("commit", "-m", "spine flip; off-spine drift left standing")
    # The interfaces snapshot's writing commit is STILL the seed, where it
    # matched live byte-for-byte, so the committed rule is green too.
    assert CT.committed_snapshot_findings(root) == []
    # And the drift survived the act — the census is intact, not zeroed.
    assert (SNAP.snapshot_root(root) / IF_REL).read_bytes() == seed_if
    assert (SNAP.snapshot_root(root) / IF_REL).read_bytes() != (
        root / IF_REL
    ).read_bytes()


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
    # Title cell, which is approved text and therefore exactly what a snapshot
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


_WORKED_SR = """
[requirement.SR-001]
title = "The worked row"
requirement = "The system shall record what a human approved."
rationale = "Without a record of what was blessed, an approval cannot be audited."
acceptance_criteria = "A copy of the registry exists under docs/archive/last_approved/."
priority = "M"
verification = "Test"
status = "Approved"
"""


def test_a_HOLE_in_the_snapshot_REDS_A_REAL_STRICT_INTEGRITY_RUN(scaffold):
    """THE ARMING, DRIVEN THROUGH THE COMMAND (2026-08-20, the batch review's
    CRITICAL-1). The pin below this one reads `trace.py`'s SOURCE for the string
    `findings.integrity += findings.snapshot_findings`, and the review executed
    two plausible routing refactors that keep every such string in place while
    the floor stops firing — the approval-record rules disarmed with the whole
    suite green. A grep cannot tell you what a program does.

    So this runs the real command over a real repo: bootstrap a scaffold, put ONE
    approved requirement in it, seed the record, and then punch the exact hole the
    rule exists to catch — an approved row with no copy. `--strict-integrity` is
    what the pre-commit hook and the DevStg-Reqs `registry-integrity` step both
    run.

    THE GREEN BASELINE IS LOAD-BEARING: every step before the hole asserts exit
    0, so the red at the end can only be the hole. And the summary's own
    `integrity=1` is asserted, not just the exit code — that is what pins the
    finding to the ALWAYS-ON pipe rather than to `--strict-schema`, which runs at
    DevStg-Impl alone and would leave the rule inert for every repo below the top
    bar."""
    sr = scaffold / SR_REL
    sr.write_text(sr.read_text(encoding="utf-8") + _WORKED_SR, encoding="utf-8")
    # A hand-authored id owes the watermark; recording it keeps the baseline green
    # for the one reason that is not this rule's business.
    assert run_py(["scripts/trace.py", "--bump-ids"], cwd=scaffold).returncode == 0
    green = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert green.returncode == 0, green.stdout + green.stderr
    seed = run_py(["scripts/intake.py", "snapshot", "--seed"], cwd=scaffold)
    assert seed.returncode == 0, seed.stdout + seed.stderr
    seeded = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert seeded.returncode == 0, seeded.stdout + seeded.stderr
    # ...and now the record loses the row it blessed.
    snap_sr = SNAP.snapshot_root(scaffold) / SR_REL
    text = snap_sr.read_text(encoding="utf-8")
    snap_sr.write_text(text[: text.index("[requirement.SR-001]")], encoding="utf-8")
    holed = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    out = holed.stdout + holed.stderr
    assert holed.returncode == 1, out
    assert "SR-001 reads Status=Approved but is ABSENT" in out, out
    assert "integrity=1" in out, out


def test_the_snapshot_rules_are_ARMED_on_traces_INTEGRITY_floor():
    """D-9 MIGRATION STEP 7 — the arming, from both ends.

    SECONDARY SINCE 2026-08-20. The behavioural pin above is the one that speaks
    for the floor; these source assertions survive as the cheap statement of
    WHICH pipe each producer joins, which is a wiring fact no execution reports
    as directly. They are not evidence that the floor fires.

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
    assert "baseline_snapshot.record_findings(" in text
    assert "unanchored_findings(root)" in inspect.getsource(SNAP.record_findings)
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


# --- the mirror over COMMITTED state (2026-08-20) -----------------------------
# The staged rule is keyed on a snapshot file being IN the commit, so a forgery
# that has LANDED is invisible to every run afterwards. These pin the half that
# closes it — and, just as importantly, the half that must NOT fire.


def test_a_LANDED_forgery_reds_EVERY_LATER_RUN_though_nothing_is_staged(tmp_path):
    """ROUND-OPUS CRITICAL-3 / ROUND-SOL MAJOR-2, driven end to end: commit a
    hand-edited snapshot with the hook bypassed, then ask the always-on floor
    again with a clean index. Before this rule the answer was exit 0, forever."""
    root, run_git = _git_tree(tmp_path)
    # Green first, over the committed state the seed just made.
    assert CT.committed_snapshot_findings(root) == []
    snap_sr = SNAP.snapshot_root(root) / SR_REL
    snap_sr.write_text(
        snap_sr.read_text(encoding="utf-8")
        + '\n[requirement.SR-999]\nstatus = "Approved"\n',
        encoding="utf-8",
    )
    run_git("add", "-A")
    # The staged rule DOES see it in the commit that does it...
    staged = CT.staged_snapshot_findings(root)
    assert any("byte-identical" in f for f in staged)
    # ...and prescribes a repair that works: a bare `intake.py snapshot`
    # copies nothing here or refuses the drift, so it names the arguments.
    assert any(_prescribes_a_working_repair(f, SR_REL) for f in staged), staged
    run_git("commit", "-m", "forge")
    # ...and this is the blind spot: with the index clean, it has nothing to say.
    assert CT.staged_snapshot_findings(root) == []
    found = CT.committed_snapshot_findings(root)
    assert any("LANDED" in f and SR_REL in f for f in found), found
    assert any(_prescribes_a_working_repair(f, SR_REL) for f in found), found


def _prescribes_a_working_repair(finding, live_rel):
    """A mirror finding's repair is either restoring the blessed copy or an
    explicit fresh act naming its authority for the registry concerned — and
    that authority is a `--approves` token the snapshot CLI's own resolver
    accepts for THIS registry, so the prescribed command does not refuse."""
    m = re.search(r'--approves "([^"]*)"', finding)
    return (
        "restore the copy that was blessed" in finding
        and "--reattests <ROW-ID>" in finding
        and m is not None
        and list(SNAP.parse_approves(m.group(1))) == [SNAP.resolve_registry(live_rel)]
    )


def test_the_mirror_repair_names_a_registry_the_resolver_accepts_per_carrier():
    """`resolve_registry` accepts a registry's canonical rel, filename or stem,
    and a CSV carrier's live path is none of those. The repair clause is
    written for whichever carrier diverged, so its `--approves` token must
    resolve for both — parsed here through the real resolver, in process."""
    for live_rel in (SR_REL, SR_REL[: -len(".toml")] + ".csv"):
        repair = AR._mirror_repair(live_rel)
        m = re.search(r'--approves "([^"]*)"', repair)
        assert m, repair
        assert list(SNAP.parse_approves(m.group(1))) == [SR_REL], repair


def test_a_PENDING_AMENDMENT_leaves_the_committed_mirror_GREEN(tmp_path):
    """THE RULE THAT WOULD HAVE BEEN WRONG, refused deliberately. Comparing the
    snapshot to live in the WORKING TREE reds every pending amendment — and the
    lag between an amendment and its approval is the signal the whole
    mechanism exists to render. The comparison is pinned to the commit that
    WROTE each copy, so live moving on afterwards is silent here."""
    root, run_git = _git_tree(tmp_path)
    _rewrite(root, SR_REL, 'title = "', 'title = "amended ')
    run_git("add", "-A")
    run_git("commit", "-m", "an amendment awaiting its sitting")
    assert (SNAP.snapshot_root(root) / SR_REL).read_bytes() != (
        root / SR_REL
    ).read_bytes(), "fixture: the tree and the record must actually differ"
    assert CT.committed_snapshot_findings(root) == []


def test_the_committed_mirror_is_SILENT_off_git_and_before_any_commit(tmp_path):
    # The degrade every scan here takes: an unanswerable question makes no
    # finding. A seeded but uncommitted snapshot has no committed state to judge.
    root = _seeded(tmp_path)
    assert CT.committed_snapshot_findings(root) == []


def test_a_LANDED_forgery_reds_A_REAL_STRICT_INTEGRITY_RUN(scaffold):
    """The same property through the command the hook runs, over a scaffold that
    really commits — the wiring half of 1c, since a producer nothing calls is
    worth nothing."""
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        return subprocess.run([git, "-C", str(scaffold), *a], capture_output=True)

    sr = scaffold / SR_REL
    sr.write_text(sr.read_text(encoding="utf-8") + _WORKED_SR, encoding="utf-8")
    assert run_py(["scripts/trace.py", "--bump-ids"], cwd=scaffold).returncode == 0
    assert (
        run_py(["scripts/intake.py", "snapshot", "--seed"], cwd=scaffold).returncode
        == 0
    )
    if not (scaffold / ".git").is_dir():
        run_git("init")
    pin_autocrlf(scaffold)
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "seed")
    green = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert green.returncode == 0, green.stdout + green.stderr
    snap_sr = SNAP.snapshot_root(scaffold) / SR_REL
    snap_sr.write_text(
        snap_sr.read_text(encoding="utf-8").replace(
            "The worked row", "The row nobody blessed"
        ),
        encoding="utf-8",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "hooks bypassed")
    red = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    out = red.stdout + red.stderr
    assert red.returncode == 1, out
    assert "LANDED" in out and "integrity=1" in out, out


def test_approval_stamp_names_the_commit_that_MOVED_A_STATUS_CELL(tmp_path):
    """The provenance the re-attestation brief promises its reader (MAJOR-4).
    `stamp` moves on ANY snapshot write, including a refresh that absorbs an
    amendment approving no new maturity; this one moves only when a maturity cell
    does. (Since WI-571 a traced-only refresh writes NOTHING, so the write that
    exercises the distinction is a named amendment, not a traced re-point.)"""
    root, run_git = _git_tree(tmp_path)
    seeded = SNAP.approval_stamp(root)[0]
    assert seeded, "the seeding commit wrote every status line there is"
    # An amendment absorbed under a ref: the record is re-written for the named
    # registry, but no maturity cell moves.
    ssid, srow = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, srow["Title"], srow["Title"] + " (amended)")
    SNAP.copy_live(root, approves={SR_REL: "the sitting"}, reattests={ssid})
    run_git("add", "-A")
    run_git("commit", "-m", "an amendment absorbed under a ref")
    assert SNAP.stamp(root)[0] != seeded, "the write stamp must follow any write"
    assert SNAP.approval_stamp(root)[0] == seeded, "no status cell moved"
    # ...and now one does.
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    run_git("add", "-A")
    run_git("commit", "-m", "a maturity cell moves")
    assert SNAP.approval_stamp(root)[0] not in ("", seeded)


def test_the_README_is_prose_and_is_exempt_from_the_mirror(tmp_path):
    # Design §F8 / repo-lock D-10's tripwire: the stamp is rendered, never
    # parsed, and has no live counterpart to mirror. If it were not exempt, a
    # signing commit would warn about its own README every time.
    root, run_git = _git_tree(tmp_path)
    (SNAP.snapshot_root(root) / "README.md").write_text("# stamp\n", encoding="utf-8")
    run_git("add", "-A")
    assert CT.staged_snapshot_findings(root) == []


def test_the_act_ledger_is_exempt_from_the_mirror(tmp_path):
    # The ledger is the snapshot's own record of its acts, with no live
    # counterpart, so neither mirror rule compares it with one: the seed commit
    # carrying it and a later act appending to it stay green.
    root, run_git = _git_tree(tmp_path)
    assert (SNAP.snapshot_root(root) / SNAP.ACTS).is_file()
    assert CT.committed_snapshot_findings(root) == []
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (re-attested)")
    SNAP.copy_live(root, reattests={sid})
    run_git("add", "-A")
    assert CT.staged_snapshot_findings(root) == []
    run_git("commit", "-m", "an act")
    assert CT.committed_snapshot_findings(root) == []


def test_the_act_ledger_name_has_one_value_in_both_homes():
    # `acceptance_record` restates the name for the reason it restates the
    # directory: the import edge runs the other way.
    assert load_script("acceptance_record").SNAPSHOT_ACTS == SNAP.ACTS


# --- the act ledger fails CLOSED (second review of WI-632) --------------------
# The accepted-risk anchor reads acts by their `seq`, so a ledger whose numbers
# repeat loses the later act exactly as the prose-stamp reader did, and a cell
# of the wrong type can crash the read. Any malformed ledger is refused whole:
# the reader never guesses which entries to keep.

_GOOD_ACT = (
    '[[act]]\nseq = 1\ndate = "2026-09-26"\napproved = ["SR-001"]\nreattested = []\n'
)
_BAD_LEDGERS = {
    "not TOML": "[[act]\nseq = 1\n",
    "act not a list": 'act = "SR-001"\n',
    "entry not a table": "act = [1]\n",
    "duplicate seq": _GOOD_ACT + _GOOD_ACT,
    "decreasing seq": _GOOD_ACT.replace("seq = 1", "seq = 2") + _GOOD_ACT,
    "seq not an integer": _GOOD_ACT.replace("seq = 1", 'seq = "1"'),
    "seq a boolean": _GOOD_ACT.replace("seq = 1", "seq = true"),
    "seq below one": _GOOD_ACT.replace("seq = 1", "seq = 0"),
    "seq missing": _GOOD_ACT.replace("seq = 1\n", ""),
    "date missing": _GOOD_ACT.replace('date = "2026-09-26"\n', ""),
    "date not a date": _GOOD_ACT.replace('"2026-09-26"', '"yesterday"'),
    "date a datetime": _GOOD_ACT.replace('"2026-09-26"', "2026-09-26T10:00:00"),
    "approved not a list": _GOOD_ACT.replace('["SR-001"]', '"SR-001"'),
    "approved holds a number": _GOOD_ACT.replace('["SR-001"]', "[1]"),
    "approved missing": _GOOD_ACT.replace('approved = ["SR-001"]\n', ""),
    "reattested not a list": _GOOD_ACT.replace("reattested = []", "reattested = 3"),
    "reattested missing": _GOOD_ACT.replace("reattested = []\n", ""),
    "id not an id": _GOOD_ACT.replace('"SR-001"', '"sr 1"'),
}


@pytest.mark.parametrize("defect", sorted(_BAD_LEDGERS))
def test_a_malformed_act_ledger_is_refused_whole(defect):
    text = _BAD_LEDGERS[defect]
    assert SNAP.acts_problems(text), defect
    with pytest.raises(SNAP.ActLedgerError):
        SNAP.parse_acts(text)


def test_a_well_formed_act_ledger_parses_in_file_order():
    second = _GOOD_ACT.replace("seq = 1", "seq = 3").replace(
        'date = "2026-09-26"', "date = 2026-09-27"
    )
    text = _GOOD_ACT + "\n" + second
    assert SNAP.acts_problems(text) == []
    assert SNAP.parse_acts(text) == [
        {"seq": 1, "date": "2026-09-26", "approved": ["SR-001"], "reattested": []},
        {"seq": 3, "date": "2026-09-27", "approved": ["SR-001"], "reattested": []},
    ]
    assert SNAP.acts_problems("") == [] and SNAP.parse_acts(None) == []


def test_a_ledger_entry_may_name_the_verdict_that_ruled_it():
    """OI-100 gap 2 (WI-791): an act may name the verdict file that ruled its
    re-attested rows. The field is optional, so every entry written before it
    still parses in its old shape; when present it is a non-empty path."""
    named = _GOOD_ACT + 'verdict = "docs/reviews/v.md"\n'
    assert SNAP.acts_problems(named) == []
    (entry,) = SNAP.parse_acts(named)
    assert entry["verdict"] == "docs/reviews/v.md"
    assert "verdict" not in SNAP.parse_acts(_GOOD_ACT)[0]
    for bad in ('verdict = ""\n', "verdict = 3\n"):
        problems = SNAP.acts_problems(_GOOD_ACT + bad)
        assert problems and "`verdict`" in problems[0], problems


def test_a_reattesting_act_records_its_verdict_and_refuses_a_bad_one(tmp_path):
    """`copy_live(..., verdict=)` writes the verdict into the act's ledger entry.
    A verdict needs re-attested rows to rule, and must name a file in the tree:
    a typo would otherwise land a ruling nobody can open in the record."""
    root, _run_git = _git_tree(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (clarified)")
    with pytest.raises(SystemExit) as no_rows:
        SNAP.copy_live(root, approves={SR_REL: "x"}, verdict="docs/reviews/v.md")
    assert "names no re-attested row" in str(no_rows.value), no_rows.value
    with pytest.raises(SystemExit) as no_file:
        SNAP.copy_live(root, reattests={sid}, verdict="docs/reviews/v.md")
    assert "docs/reviews/v.md" in str(no_file.value), no_file.value
    verdict = root / "docs" / "reviews" / "v.md"
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text(
        "- [CLARITY] {} title -> same\n\nVERDICT: CLARITY rows=1\n".format(sid),
        encoding="utf-8",
    )
    proc = _snapshot_cli(root, "--reattests", sid, "--verdict", "docs/reviews/v.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "VERDICT: docs/reviews/v.md" in proc.stdout, proc.stdout
    last = SNAP.read_acts(root)[-1]
    assert last["reattested"] == [sid] and last["verdict"] == "docs/reviews/v.md"


def test_a_verdict_path_is_recorded_repo_relative_with_forward_slashes(tmp_path):
    """Sol review 1, MINOR 1 (WI-791): the merge slot reads the recorded verdict
    with `git show <rev>:<path>`, which resolves only the repository's own
    forward-slash spelling. A Windows-spelt or absolute path that names the file
    is recorded in that spelling, so a valid CLARITY act is not refused."""
    root, _run_git = _git_tree(tmp_path)
    sid, row = _first_row_at(root, "approved")
    verdict = root / "docs" / "reviews" / "v.md"
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text("- [CLARITY] {} title -> same\n".format(sid), "utf-8")
    for spelt in ("docs\\reviews\\v.md", str(verdict), "./docs/reviews/v.md"):
        _rewrite(root, SR_REL, row["Title"], row["Title"] + " +")
        row["Title"] += " +"
        SNAP.copy_live(root, reattests={sid}, verdict=spelt)
        assert SNAP.read_acts(root)[-1]["verdict"] == "docs/reviews/v.md", spelt


def test_a_verdict_outside_the_repository_is_refused(tmp_path):
    """LLR-245: the act ledger records a verdict by its repository path, so a
    verdict file outside the repository is refused although it exists, and
    the ledger does not move."""
    root, _run_git = _git_tree(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (clarified)")
    outside = tmp_path / "v.md"
    outside.write_text("- [CLARITY] {} title -> same\n".format(sid), "utf-8")
    acts = len(SNAP.read_acts(root))
    with pytest.raises(SystemExit) as refused:
        SNAP.copy_live(root, reattests={sid}, verdict=str(outside))
    assert "not a file in the tree" in str(refused.value), refused.value
    assert len(SNAP.read_acts(root)) == acts


def test_a_malformed_ledger_refuses_the_act_before_the_record_moves(tmp_path):
    """The refusal comes before any copy or stamp: a person fixes the ledger
    and re-runs, and the record they fix is the record that stood."""
    root = _seeded_with_a_drafted_sr(tmp_path)
    ledger = SNAP.snapshot_root(root) / SNAP.ACTS
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + "\n" + _GOOD_ACT, encoding="utf-8"
    )
    base = SNAP.snapshot_root(root)
    before = {p: p.read_bytes() for p in base.rglob("*") if p.is_file()}
    _rewrite(root, SR_REL, 'status = "Drafted"', 'status = "Approved"')
    with pytest.raises(SystemExit) as refused:
        SNAP.copy_live(root)
    assert SNAP.ACTS in str(refused.value), refused.value
    after = {p: p.read_bytes() for p in base.rglob("*") if p.is_file()}
    assert after == before


def test_a_malformed_ledger_REDS_A_REAL_STRICT_INTEGRITY_RUN(scaffold):
    """Reported where the record's other integrity faults are: the always-on
    `--strict-integrity` floor the pre-commit hook runs."""
    sr = scaffold / SR_REL
    sr.write_text(sr.read_text(encoding="utf-8") + _WORKED_SR, encoding="utf-8")
    assert run_py(["scripts/trace.py", "--bump-ids"], cwd=scaffold).returncode == 0
    seed = run_py(["scripts/intake.py", "snapshot", "--seed"], cwd=scaffold)
    assert seed.returncode == 0, seed.stdout + seed.stderr
    green = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert green.returncode == 0, green.stdout + green.stderr
    ledger = SNAP.snapshot_root(scaffold) / SNAP.ACTS
    ledger.write_text(
        ledger.read_text(encoding="utf-8").replace("seq = 1", "seq = 0"),
        encoding="utf-8",
    )
    red = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    out = red.stdout + red.stderr
    assert red.returncode == 1, out
    assert SNAP.ACTS in out and "integrity=1" in out, out


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
    # Amend an approved cell AND flip the row, in one staged change.
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


# --- the assumptions registry inside the approval act (SR-191, SR-192, LLR-220;
# TC-218) -----------------------------------------------------------------------
# The registry holds two approvable tiers, and each is recorded exactly as every
# other approved row is: a lane may not approve one, the act that does rides its
# own reviewed commit and writes the registry's first copy, and an amendment
# afterwards is drift from that copy. The record here predates the registry, as
# it does in any repository that signed before adopting the tier, so the first
# copy is the approval act's.

ASSUMPTIONS_REL = "docs/requirements/assumptions.toml"
_AR = load_script("acceptance_record")

# One real row per tier, in the tier's own cells, and the approved cell an
# amendment afterwards moves.
_TIER_ROWS = {
    "DA-ID": (
        "DA-9001",
        "assumption",
        '\n[assumption.DA-9001]\neffect_at = ["B-01"]\n'
        'assumption = "Row X"\nholds_when = "Always."\nobstacle = "Never."\n'
        'status = "Drafted"\nstanding = "active"\n',
        "Assumption",
    ),
    "SUR-ID": (
        "SUR-9001",
        "description",
        '\n[surrogate.SUR-9001]\nname = "A stand-in"\nemulates = ["EXT-001"]\n'
        'description = "Row X"\nstatus = "Drafted"\n',
        "Description",
    ),
}
_ASSUMPTION_TIERS = [
    pytest.param(ASSUMPTIONS_REL, col, id=col) for col in ("DA-ID", "SUR-ID")
]


def _without_the_registry(root):
    """`_git_tree`'s prepare hook: the record is signed before the registry
    exists, so the tree it seeds carries none."""
    path = root / ASSUMPTIONS_REL
    if path.is_file():
        path.unlink()


def _head(run_git):
    return run_git("rev-parse", "HEAD").stdout.strip()


@pytest.mark.parametrize("rel,id_col", _ASSUMPTION_TIERS)
def test_an_assumption_tier_row_is_approved_only_inside_the_approval_act(
    tmp_path, rel, id_col
):
    rid, key, block, cell = _TIER_ROWS[id_col]
    assert (rel, id_col) in SNAP.SNAPSHOT_TIERS
    assert (rel, id_col) in _AR.APPROVAL_ACT_CSVS
    root, run_git = _git_tree(tmp_path, _without_the_registry)
    assert not (SNAP.snapshot_root(root) / rel).exists()
    _append(root, rel, block)
    run_git("add", "-A")
    run_git("commit", "-m", "draft the row")
    drafted = _head(run_git)

    # Before the first approval the registry has no copy, and the
    # unanchored-record rule reports nothing for it.
    assert [f for f in SNAP.unanchored_findings(root) if rel in f or rid in f] == []

    # A LANE whose delta approves the row is refused at the merge slot, by name.
    _rewrite(root, rel, 'status = "Drafted"', 'status = "Approved"')
    run_git("add", "-A")
    run_git("commit", "-m", "a lane approves the row")
    head = _head(run_git)
    refusal = _AR.merge_approval_refusal(root, drafted, head, [], False, trunk=head)
    assert refusal and rid in refusal and rel in refusal, refusal
    # ...and an approval with no copy behind it is the hole the rule reports.
    assert any(rel in f for f in SNAP.unanchored_findings(root))
    run_git("reset", "-q", "--hard", drafted)

    # THE APPROVAL ACT: the flip and the record's refresh in one reviewed
    # commit, which writes the registry's first copy and passes the mirror.
    _rewrite(root, rel, 'status = "Drafted"', 'status = "Approved"')
    written = SNAP.copy_live(root)
    assert "{}/{}".format(SNAP.SNAPSHOT_DIR, rel) in written, written
    run_git("add", "-A")
    assert CT.staged_snapshot_findings(root) == []
    run_git("commit", "-m", "approve the row")
    assert CT.committed_snapshot_findings(root) == []
    assert SNAP.unanchored_findings(root) == []
    assert (SNAP.snapshot_root(root) / rel).read_bytes() == (root / rel).read_bytes()

    # The approved row amended afterwards is drift from its copy.
    _rewrite(root, rel, '{} = "Row X"'.format(key), '{} = "Row X, amended"'.format(key))
    record = SNAP.rows_for(SNAP.load_all(root), rel, id_col)
    (live,) = _SPINE_CARRIER.load(root / rel, id_col, keep_examples=False)
    assert SNAP.is_drifted(rel, id_col, live, record)
    assert set(SNAP.drifted_cells(rel, id_col, live, record)) == {cell}
    assert "{} {}: {}".format(rel, rid, cell) in SNAP.refresh_refusal(root)
