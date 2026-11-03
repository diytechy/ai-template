"""The id carrier on real repositories: the reserve verb's first use, a lost
compare-and-swap, sequential and stale-base reservations, a reservation after
a ruled correction, and the fold of a conflicted watermark (TC-401).

Every fixture is a real git repository whose trunk holds the claims the verb
reads, with each lane a linked worktree of it, because the carrier is one ref
shared by every worktree of a repository: that sharing, and git's own ref lock,
are what make two lanes' reservations disjoint. Under the floor-briefing
procedure two lanes cut from different trunk commits each drew "the next
number" from their own base and collided; there was no verb to separate them.

Real git, worktrees and merges per case, so this module is registered slow
(`tests/conftest.py` SLOW_MODULES); its in-process pin is test_id_carrier.py.
"""

import subprocess
import sys

import pytest
from conftest import (
    ID_CARRIER_REF,
    SCRIPTS,
    declare_trunk,
    env_gate_skipif,
    fixture_commit,
    fixture_git,
    load_script,
    pin_autocrlf,
    reservation_records,
    reserved_watermark,
    run_py,
    watermark_marks,
    write_lf,
)

pytestmark = [env_gate_skipif("git")]

TRACE = load_script("trace")
WATERMARK = "docs/id-watermark"
SR_REGISTRY = "docs/requirements/system-requirements.toml"
LOST_RACE = "another reservation moved the carrier; re-run"

# A ruled open item authorizing `SR = 20`, the shape the correction verb's
# authority check resolves (the ruling names the space at the value).
RULED_OI = """[open_item.OI-7]
title = "The mis-seeded SR watermark"
status = "ruled"
raised = "2026-11-01"
one_line = "the one-time correction lands SR = 20"
decision = \"\"\"SR ids up to 20 were allocated before the mark existed, so
the mark is corrected to SR = 20.\"\"\"
"""


def _trunk(home, marks=None):
    """A trunk on `main` claiming WI-001 and WI-002 and carrying a committed
    watermark (SR 5, TC 3 by default): the repository every lane is cut from."""
    root = home / "primary"
    root.mkdir(parents=True)
    fixture_git(root, "init", "-q")
    pin_autocrlf(root)
    fixture_git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    declare_trunk(root, "main")
    for n in (1, 2):
        wi = "WI-{:03d}".format(n)
        write_lf(
            root,
            "docs/work/active/wi-{:03d}/{}-x.md".format(n, wi),
            '+++\nid = "{}"\n+++\n'.format(wi),
        )
    base = {"SR": 5, "TC": 3, "WI": 2, "OI": 7}
    base.update(marks or {})
    write_lf(root, WATERMARK, reserved_watermark(base))
    fixture_commit(root, "seed: two claims and the watermark")
    return root


def _lane(root, n, base="main"):
    """Lane `wi-00<n>`, a linked worktree of the trunk cut from `base`."""
    lane = root.parent / "lane-wi-{:03d}".format(n)
    fixture_git(root, "worktree", "add", "-q", "-b", lane.name[5:], str(lane), base)
    return lane


def _reserve(where, wi, counts):
    """`trace.py --reserve-ids` run as a subprocess in `where`."""
    return run_py(
        [SCRIPTS / "trace.py", "--root", str(where), "--reserve-ids", wi, counts],
        cwd=where,
    )


def _reserved(where, wi, counts):
    proc = _reserve(where, wi, counts)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc


def _carrier(root):
    """The carrier tip's watermark text."""
    return fixture_git(root, "show", "{}:{}".format(ID_CARRIER_REF, WATERMARK))


def _tip(root):
    proc = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "-q", "--verify", ID_CARRIER_REF],
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip() or None


def _ranges(text, wi):
    return [r for r in reservation_records(text) if r[3] == wi]


def _disjoint(records):
    spans = sorted((s, lo, hi) for s, lo, hi, _wi in records)
    return all(
        a[0] != b[0] or a[2] < b[1] for a, b in zip(spans, spans[1:], strict=False)
    )


def test_first_reservation_seeds_the_carrier_from_trunk(tmp_path):
    root = _trunk(tmp_path)
    lane = _lane(root, 1)
    assert _tip(root) is None
    _reserved(lane, "WI-001", "SR=2")
    tip = _tip(root)
    assert tip is not None
    # One orphan commit whose tree is the one file.
    assert fixture_git(root, "rev-list", "--count", tip) == "1"
    assert fixture_git(root, "ls-tree", "-r", "--name-only", tip) == WATERMARK
    carrier = _carrier(root)
    assert reservation_records(carrier) == [("SR", 6, 7, "WI-001")]
    assert (watermark_marks(carrier)["SR"], watermark_marks(carrier)["TC"]) == (7, 3)
    # The verb folded the carrier into the lane's file, and left it uncommitted.
    working = (lane / WATERMARK).read_text(encoding="utf-8")
    assert reservation_records(working) == [("SR", 6, 7, "WI-001")]
    assert WATERMARK in fixture_git(lane, "status", "--porcelain")


@pytest.mark.parametrize("first_use", [False, True], ids=["moved", "first-use"])
def test_a_lost_race_refuses_with_nothing_written(
    tmp_path, monkeypatch, capsys, first_use
):
    root = _trunk(tmp_path)
    lane_a, lane_b = _lane(root, 1), _lane(root, 2)
    if not first_use:
        _reserved(lane_b, "WI-002", "SR=1")
    stale = _tip(root)
    _reserved(lane_b, "WI-002", "SR=1")  # B moves (or creates) the carrier
    moved = _tip(root)
    assert moved != stale
    before = (lane_a / WATERMARK).read_bytes()
    carrier = getattr(TRACE, "id_carrier", None)
    if carrier is None:
        pytest.fail("trace.py does not compose the id carrier module")
    # A read the tip before B moved it: its swap must lose, not overwrite.
    monkeypatch.setattr(carrier, "carrier_tip", lambda *_a, **_k: stale)
    monkeypatch.setattr(
        sys,
        "argv",
        ["trace.py", "--root", str(lane_a), "--reserve-ids", "WI-001", "SR=1"],
    )
    try:
        TRACE.main()
        code = 0
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
    _out, err = capsys.readouterr()
    assert code == 1, err
    assert LOST_RACE in err, err
    assert _tip(root) == moved
    assert (lane_a / WATERMARK).read_bytes() == before


def test_sequential_reservations_are_disjoint(tmp_path):
    root = _trunk(tmp_path)
    lane_a, lane_b = _lane(root, 1), _lane(root, 2)
    _reserved(lane_a, "WI-001", "SR=2,TC=1")
    _reserved(lane_b, "WI-002", "SR=2,TC=1")
    _reserved(lane_a, "WI-001", "SR=1")  # a second sitting in one lane
    carrier = _carrier(root)
    records = reservation_records(carrier)
    assert _disjoint(records), records
    assert _ranges(carrier, "WI-001") == [
        ("SR", 6, 7, "WI-001"),
        ("SR", 10, 10, "WI-001"),
        ("TC", 4, 4, "WI-001"),
    ]
    # Each starts one above the carrier's mark at its turn.
    assert _ranges(carrier, "WI-002") == [
        ("SR", 8, 9, "WI-002"),
        ("TC", 5, 5, "WI-002"),
    ]


def test_stale_base_reservations_are_disjoint(tmp_path):
    root = _trunk(tmp_path)
    lane_a = _lane(root, 1)  # cut while trunk's SR mark is 5
    write_lf(root, WATERMARK, reserved_watermark({"SR": 8, "TC": 3, "WI": 2, "OI": 7}))
    fixture_commit(root, "trunk: SR mark 8")
    lane_b = _lane(root, 2)  # cut after the mark moved
    _reserved(lane_b, "WI-002", "SR=2")
    _reserved(lane_a, "WI-001", "SR=2")
    carrier = _carrier(root)
    assert _ranges(carrier, "WI-002") == [("SR", 9, 10, "WI-002")]
    assert _ranges(carrier, "WI-001") == [("SR", 11, 12, "WI-001")]
    working = (lane_a / WATERMARK).read_text(encoding="utf-8")
    assert ("SR", 11, 12, "WI-001") in reservation_records(working)
    assert watermark_marks(working)["SR"] == 12


def test_a_reservation_after_a_ruled_correction_starts_above_it(tmp_path):
    root = _trunk(tmp_path)
    lane_a = _lane(root, 1)
    _reserved(lane_a, "WI-001", "SR=1")  # the carrier exists, SR at 6
    write_lf(root, "docs/requirements/open-items.toml", RULED_OI)
    proc = run_py(
        [SCRIPTS / "trace.py", "--root", str(root), "--correct-mark", "SR", "20"]
        + ["OI-7"],
        cwd=root,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    fixture_commit(root, "trunk: the ruled SR correction")
    lane_b = _lane(root, 2)
    _reserved(lane_b, "WI-002", "SR=1")
    carrier = _carrier(root)
    assert _ranges(carrier, "WI-002") == [("SR", 21, 21, "WI-002")]
    assert TRACE.parse_corrections(carrier).get("SR") == [(5, 20, "OI-7")]


def test_a_reservation_in_a_lane_behind_trunk_commits_through_the_integrity_floor(
    tmp_path,
):
    # Trunk mints a work item and raises a carrier-space mark with no record
    # after the lane is cut. The lane's folded watermark carries only what its
    # records justify, so the commit the recipe orders passes the floor the
    # pre-commit hook runs; trunk's marks reach the lane with its next refresh.
    root = _trunk(tmp_path)
    lane = _lane(root, 1)
    write_lf(root, "docs/work/active/wi-003/WI-003-x.md", '+++\nid = "WI-003"\n+++\n')
    write_lf(root, WATERMARK, reserved_watermark({"SR": 5, "TC": 9, "WI": 3, "OI": 7}))
    fixture_commit(root, "trunk: WI-003 minted, TC raised")
    _reserved(lane, "WI-001", "SR=1")
    write_lf(
        lane, SR_REGISTRY, '[requirement.SR-006]\ntitle = "t"\nstatus = "Drafted"\n'
    )
    fixture_git(lane, "add", "-A")
    floor = run_py(
        [SCRIPTS / "trace.py", "--root", str(lane), "--strict-integrity"], cwd=lane
    )
    assert floor.returncode == 0, floor.stdout + floor.stderr
    fixture_commit(lane, "WI-001: the reserved row and the folded watermark")
    working = (lane / WATERMARK).read_text(encoding="utf-8")
    marks = watermark_marks(working)
    assert (marks["SR"], marks["TC"], marks["WI"]) == (6, 3, 2), marks
    assert reservation_records(working) == [("SR", 6, 6, "WI-001")]


def test_the_claim_folder_reader_reads_each_lanes_work_items_at_a_revision(tmp_path):
    # The one reader the reserve verb's claim check and the hand squash's
    # work-item read share: a spec under a slashed lane name is that lane's,
    # and a file the claim never writes names no work item.
    from kitlib import git as kgit

    root = _trunk(tmp_path)
    seeded = fixture_git(root, "rev-parse", "HEAD").strip()
    write_lf(root, "docs/work/active/feature/x/WI-003-y.md", "+++\n+++\n")
    write_lf(root, "docs/work/active/wi-001/WI-009.md", "residue\n")
    write_lf(root, "docs/work/active/wi-001/notes.txt", "residue\n")
    write_lf(root, "docs/work/active/WI-010-loose.md", "residue\n")
    fixture_commit(root, "claim: WI-003 and some residue")
    assert kgit.claimed_specs(root, "HEAD") == [
        ("feature/x", "WI-003", "WI-003-y.md"),
        ("wi-001", "WI-001", "WI-001-x.md"),
        ("wi-002", "WI-002", "WI-002-x.md"),
    ]
    assert kgit.claimed_specs(root, seeded, "wi-002") == [
        ("wi-002", "WI-002", "WI-002-x.md")
    ]
    assert kgit.claimed_specs(root, seeded, "feature/x") == []
    assert kgit.claimed_specs(root, "no-such-revision") is None


def test_fold_ids_on_a_conflicted_watermark(tmp_path):
    root = _trunk(tmp_path)
    lane = _lane(root, 1)
    _reserved(lane, "WI-001", "SR=2")
    write_lf(
        lane,
        SR_REGISTRY,
        "".join(
            '[requirement.SR-00{}]\ntitle = "t"\nstatus = "Drafted"\n\n'.format(n)
            for n in (6, 7)
        ),
    )
    fixture_commit(lane, "WI-001: two reserved SR rows and the folded watermark")
    write_lf(
        root,
        WATERMARK,
        reserved_watermark({"SR": 9, "TC": 3, "WI": 2, "OI": 7}, basis="SR=9"),
    )
    fixture_commit(root, "trunk: SR mark 9")
    merge = subprocess.run(
        ["git", "-C", str(lane), "merge", "-q", "--no-commit", "main"],
        capture_output=True,
        text=True,
    )
    assert merge.returncode != 0, "the fixture's merge was meant to conflict"
    assert "<<<<<<<" in (lane / WATERMARK).read_text(encoding="utf-8")
    proc = run_py([SCRIPTS / "trace.py", "--root", str(lane), "--fold-ids"], cwd=lane)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (lane / WATERMARK).read_text(encoding="utf-8")
    assert not any(m in text for m in ("<<<<<<<", "=======", ">>>>>>>")), text
    assert (watermark_marks(text)["SR"], watermark_marks(text)["TC"]) == (9, 3)
    assert reservation_records(text) == [("SR", 6, 7, "WI-001")]
    basis = [ln for ln in text.splitlines() if ln.startswith("# basis:")]
    assert basis and "SR=7" in basis[0].split(), basis
