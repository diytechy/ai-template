"""The landing admits only reserved identities, on both landing routes, and
lands the carrier's fold (TC-402).

A landing judges the carrier-space ids it adds (live in the lane's tip, not
live in its merge base with trunk; a hand squash also judges its staged tree
over HEAD) against the retirement records and the carrier's records naming
its claimed work item; a retired number, even inside its own reservation, and
every other added id outside those records are refused before it lands, and
so is a missing carrier, an unreadable claim, and a record only the landing
carries. An id live in the landing that a retirement record the landing
brings names is refused even when it is not added (live at the lane's base,
retired, then authored again); a pair trunk already held passes. Each
landing also lands the fold of the carrier tip it read: the merge slot treats
a lane whose watermark lags the carrier as not merge-ready and refreshes it in
the slot, and a hand squash folds in the staged squash, its pre-commit step
refusing while the staged watermark still lags. A station refresh whose only
conflict is the watermark resolves it by the same fold.

Every fixture is a real git repository built like the merge slot's own tests
(`tests/integrate_fixtures.py`): a trunk claiming WI-401 onto `wi-401`, a
lane worktree that closes it, and, for the slot, the stub harness the station
tests use, so the slot's order and topology are real and the bar is not what
is measured. The carrier is planted by git plumbing (`conftest.
plant_id_carrier`), so these cases judge the landing, not the reserve verb.

Three cases characterize what held before the landing check was built, each
naming the wrong implementation it would catch. Real git and the merge slot per case, so this
module is registered slow (`tests/conftest.py` SLOW_MODULES); its in-process
pins are test_id_carrier.py's landing and fold-lag cases.
"""

import os
import subprocess

import pytest
from conftest import (
    ROOT,
    SCRIPTS,
    env_gate_skipif,
    load_script,
    plant_id_carrier,
    reservation_records,
    reserved_watermark,
    run_py,
    watermark_marks,
    write_lf,
)
from integrate_fixtures import (
    T_CODE,
    T_LATER,
    T_VERDICT,
    _commit,
    _git,
    _rev,
    claim_repo,
    declare_generated,
    integ,
    refused,
)

pytestmark = env_gate_skipif("git")

TRACE = load_script("trace")
WATERMARK = "docs/id-watermark"
SR_REGISTRY = "docs/requirements/system-requirements.toml"
STEP = [SCRIPTS / "check.py", "--run-steps", "reserved-ids"]
FOLD = [SCRIPTS / "trace.py", "--root", ".", "--fold-ids"]
TRUNK_SPACES = {"WI", "OI", "DP"}

# The station's stub harness (the shape test_integrate_station.py uses): a
# trunk step and a green bar that record nothing this module reads.
STUB_TRUNK_STEP = "import sys\nsys.exit(0)\n"
STUB_CHECK_GREEN = 'print("  PASS  tests+coverage   0.1s")\n'

OWN = ("SR", 6, 7, "WI-401")
OTHER = ("SR", 8, 9, "WI-402")


def _rows(*numbers):
    """A system-requirements registry holding `SR-<n>` for each number."""
    return "".join(
        '[requirement.SR-{:03d}]\ntitle = "t"\nstatus = "Drafted"\n\n'.format(n)
        for n in numbers
    )


def _trunk(home, harness=True, sr_mark=5, attributes=None, sr_rows=(), records=()):
    """A trunk with WI-401 claimed onto `wi-401` and a full watermark (SR at
    `sr_mark`); with `harness`, the station's stub harness and declared bar,
    with `attributes`, that `.gitattributes`, with `sr_rows`, those SR
    rows live, and with `records`, a retirement record for each of those SR
    numbers beside its still-live row (a pair an earlier kit let land); each
    committed before the claim so the trunk and the lane carry the same."""
    home.mkdir(parents=True, exist_ok=True)
    root = claim_repo(home)
    write_lf(root, WATERMARK, reserved_watermark({"WI": 401, "SR": sr_mark}))
    if sr_rows:
        write_lf(root, SR_REGISTRY, _rows(*sr_rows))
    for number in records:
        _retire(root, number)
        write_lf(root, SR_REGISTRY, _rows(*sr_rows))
    if attributes is not None:
        write_lf(root, ".gitattributes", attributes)
    if harness:
        write_lf(root, ".gitignore", "out/\n")
        write_lf(root, "docs/stack.ini", "[product]\ntest = {py} -m pytest -q\n")
        declare_generated(root)
        write_lf(root, "docs/review-policy", "0\n")
        write_lf(root, "scripts/trunk_step.py", STUB_TRUNK_STEP)
        write_lf(root, "scripts/check.py", STUB_CHECK_GREEN)
    _commit(root, "chore: the watermark and the harness", when=T_CODE)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    return root


def _lane_path(root, branch="wi-401"):
    return root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / branch


def _close(root, files, branch="wi-401", wi="WI-401", slug="widget"):
    """Build and CLOSE the lane in its own worktree: `files` (`{rel: text}`)
    and the claimed spec's move to `complete/`, one commit. Returns the lane
    worktree."""
    wt = _lane_path(root, branch)
    _git(root, "worktree", "add", "-q", str(wt), branch)
    for rel, text in files.items():
        write_lf(wt, rel, text)
    src = wt / "docs" / "work" / "active" / branch / "{}-{}.md".format(wi, slug)
    dst = wt / "docs" / "work" / "complete" / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        src.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
        encoding="utf-8",
        newline="\n",
    )
    _git(wt, "rm", "-q", src.relative_to(wt).as_posix())
    _commit(wt, "{}: build + close".format(wi), when=T_VERDICT)
    return wt


# Each refused landing-table row: (carrier records or None for no carrier,
# the lane's SR rows, the lane's own records, the words the refusal names).
REFUSED = {
    "no-record": ([("TC", 1, 1, "WI-402")], (6,), [], ("SR-006", "WI-401")),
    "another-wis-record": ([OTHER], (8,), [], ("SR-008", "WI-401")),
    "retired-number": ([OWN], (3,), [OWN], ("SR-003", "WI-401")),
    "no-carrier": (None, (6,), [], ("SR-006", "WI-401")),
    "landing-only-record": (
        [("SR", 6, 6, "WI-401")],
        (6,),
        [("SR", 6, 6, "WI-401"), ("SR", 7, 7, "WI-401")],
        ("# reservation: SR 7-7 (WI-401)",),
    ),
}
NAMES_THE_VERB = {"no-record", "another-wis-record", "retired-number", "no-carrier"}


def _case(home, case, harness=True):
    """A trunk and a closed lane in the shape of one refused landing-table
    row; the carrier planted first, the lane's watermark its fold plus the
    lane's own records."""
    carrier, numbers, own, _named = REFUSED[case]
    root = _trunk(home, harness=harness)
    if carrier is not None:
        top = max([5] + [r[2] for r in carrier])
        plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": top}, carrier))
    records = sorted(set(own) | set(carrier or []))
    top = max([5, *numbers] + [r[2] for r in records])
    _close(
        root,
        {
            SR_REGISTRY: _rows(*numbers),
            WATERMARK: reserved_watermark({"WI": 401, "SR": top}, records),
        },
    )
    return root


RETIRE = [SCRIPTS / "retire.py"]
RESERVE = [SCRIPTS / "trace.py", "--root", ".", "--reserve-ids"]
RETIRED_RECORD = "docs/log.d/retired/SR-006.md"
BASE_RETIRED_RECORD = "docs/log.d/retired/SR-003.md"


def _retire(tree, number):
    """Retire SR-<number> in `tree` through the retirement command."""
    name = "SR-{:03d}".format(number)
    proc = run_py(RETIRE + [name, "--reason", "replaced", "--root", "."], cwd=tree)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def _reauthored_retired_id(root, number=6):
    """A closed lane that retires SR-<number> through the retirement command
    and authors a different SR-<number>: every step a supported route. SR-006
    is first reserved through the reserve verb (SR 6-6) and authored in the
    lane; any other number is one the lane's base already holds live.
    Returns the worktree."""
    wt = _close(root, {"widget.txt": "1" + chr(10)})

    def author(title):
        write_lf(wt, SR_REGISTRY, _rows(number).replace('title = "t"', title))

    def reserve():
        proc = run_py(RESERVE + ["WI-401", "SR=1"], cwd=wt)
        assert proc.returncode == 0, proc.stdout + proc.stderr

    first = (reserve, lambda: author('title = "the first obligation"'))
    steps = (*(first if number == 6 else ()), lambda: _retire(wt, number))
    steps += (lambda: author('title = "a different obligation"'),)
    for n, step in enumerate(steps):
        step()
        _commit(wt, "WI-401: lane step {}".format(n), when=T_VERDICT + 1 + n)
    held = _git(root, "ls-tree", "-r", "--name-only", "wi-401", "--", "docs/log.d")
    assert "docs/log.d/retired/SR-{:03d}.md".format(number) in held.split()
    assert "a different obligation" in _git(root, "show", "wi-401:" + SR_REGISTRY)
    return wt


def _squash(root, branch="wi-401"):
    _git(root, "merge", "--squash", "-q", branch)


def _step(root):
    proc = run_py(STEP, cwd=root)
    return proc.returncode, proc.stdout + proc.stderr


def _named(case):
    words = REFUSED[case][3]
    return words + ("--reserve-ids",) if case in NAMES_THE_VERB else words


def _trace(name):
    """One landing seam of trace.py, or this test's own failure while unbuilt."""
    if not hasattr(TRACE, name):
        pytest.fail("trace.py has no {}".format(name))
    return getattr(TRACE, name)


# --- the sweep and the judgement's seams -----------------------------------------


def test_the_extracted_sweep_equals_the_working_sweep_for_every_carrier_space(
    tmp_path,
):
    """Implements: TC-402"""
    # On this repository. The working tree's two registry directories are
    # staged into a private index and written as a tree, so the comparison is
    # exact whatever is uncommitted: a carrier-space reader that reads outside
    # docs/requirements and docs/test makes the extracted sweep miss its ids.
    env = dict(os.environ, GIT_INDEX_FILE=str(tmp_path / "index"))

    def git(*args):
        proc = subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, text=True, env=env
        )
        assert proc.returncode == 0, proc.stderr
        return proc.stdout.strip()

    git("read-tree", "HEAD")
    git("add", "-A", "--", "docs/requirements", "docs/test")
    tree = git("write-tree")
    live_ids, live_ids_at = _trace("live_ids"), _trace("live_ids_at")
    working = {(s, n) for s, n in live_ids(ROOT) if s not in TRUNK_SPACES}
    extracted = {(s, n) for s, n in live_ids_at(ROOT, tree) if s not in TRUNK_SPACES}
    assert working and extracted == working


def test_a_minus_000_placeholder_is_never_added(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False)
    base = _rev(root, "HEAD")
    write_lf(root, SR_REGISTRY, _rows(0))
    _commit(root, "a placeholder row", when=T_LATER)
    placeholder = _rev(root, "HEAD")
    judge = _trace("landing_id_refusal")
    assert judge(root, placeholder, base, ["WI-401"]) is None
    # The control: a real id added the same way, with no carrier, is refused.
    write_lf(root, SR_REGISTRY, _rows(0, 6))
    _commit(root, "a real row", when=T_LATER + 1)
    assert judge(root, _rev(root, "HEAD"), base, ["WI-401"])


def test_landing_fold_lag_reads_a_commit_and_an_index_tree(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False)
    held = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, held)
    write_lf(root, WATERMARK, held)
    _commit(root, "trunk: the carrier's fold", when=T_LATER)
    lag = _trace("landing_fold_lag")
    assert lag(root, "HEAD") == []
    plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": 9}, [OWN, OTHER]))
    assert any("SR 8-9 (WI-402)" in ln for ln in lag(root, "HEAD"))
    # The staged form: the index's tree is judged the same way.
    write_lf(root, WATERMARK, reserved_watermark({"WI": 401, "SR": 9}, [OWN]))
    _git(root, "add", WATERMARK)
    tree = _git(root, "write-tree").strip()
    assert any("SR 8-9 (WI-402)" in ln for ln in lag(root, tree))


# A packaging rule that leaves the registries out of an archive of the tree.
EXPORT_IGNORE = "docs/requirements/** export-ignore\n"


def test_a_registry_an_export_ignore_rule_hides_is_still_judged(tmp_path):
    """Implements: TC-402"""
    # The judgement reads the committed registries, not an archive of them: an
    # attribute that drops a file from `git archive` must not hide an
    # unreserved id from the landing check, at the lane's tip or in a staged
    # squash.
    root = _trunk(tmp_path, harness=False, attributes=EXPORT_IGNORE)
    _close(root, {SR_REGISTRY: _rows(6)})
    judge = _trace("landing_id_refusal")
    refusal = judge(root, _rev(root, "wi-401"), _rev(root, "HEAD"), ["WI-401"])
    assert refusal and "SR-006" in refusal, refusal
    _squash(root)
    code, out = _step(root)
    assert code == 1 and "SR-006" in out and "--reserve-ids" in out, out


# --- caller 1: the merge slot -----------------------------------------------------


@pytest.mark.parametrize("case", sorted(REFUSED))
def test_the_slot_refuses_each_unreserved_landing(tmp_path, case):
    """Implements: TC-402"""
    root = _case(tmp_path, case)
    refusal = refused(root, "wi-401", "smoke")
    assert all(word in refusal for word in _named(case)), (case, refusal)


def test_the_slot_refuses_an_unreserved_id_an_export_ignore_rule_hides(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path, attributes=EXPORT_IGNORE)
    _close(root, {SR_REGISTRY: _rows(6)})
    refusal = refused(root, "wi-401", "smoke")
    assert "SR-006" in refusal and "--reserve-ids" in refusal, refusal


def test_the_slot_rung_refuses_ids_added_under_an_unreadable_claim(tmp_path):
    """Implements: TC-402"""
    # The ladder's first rung refuses an empty claim before this one, so the
    # row is driven on the rung itself.
    root = _case(tmp_path, "no-record")
    rung = getattr(integ, "_reserved_id_refusal", None)
    if rung is None:
        pytest.fail("integrate.py has no reserved-ids rung")
    refusal = rung(root, "wi-401", [])
    assert refusal and "claim" in refusal.lower(), refusal


def test_the_slot_lands_a_lane_whose_ids_sit_in_its_own_record(tmp_path):
    """Implements: TC-402"""
    # Adequacy witness: an implementation that refused every added
    # carrier-space id, or judged the records of a work item other than the
    # lane's claim, would refuse this lane.
    root = _trunk(tmp_path)
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, folded)
    _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    landed = _git(root, "show", "HEAD:" + WATERMARK)
    assert OWN in reservation_records(landed)


def test_a_code_only_lane_with_no_carrier_lands(tmp_path):
    """Implements: TC-402"""
    # Adequacy witness: an implementation that demanded a carrier, or a
    # reservation, of every landing would refuse this lane, which adds no id.
    root = _trunk(tmp_path)
    _close(root, {"widget.txt": "1\n"})
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    assert "widget.txt" in _git(root, "ls-tree", "-r", "--name-only", "HEAD").split()


def test_the_slot_lands_a_code_only_lane_after_trunk_deletes_an_id_it_based_on(
    tmp_path,
):
    """Implements: TC-402"""
    # The slot reaches this lane unrefreshed (the second branch of a drain):
    # an id trunk deleted after the lane's base is still live at the lane's
    # tip, and it is trunk's change, never one the lane adds.
    root = _trunk(tmp_path, sr_rows=(3,))
    _close(root, {"widget.txt": "1\n"})
    write_lf(root, SR_REGISTRY, "")
    _commit(root, "landed: SR-003 retired by another lane", when=T_LATER)
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    landed = _git(root, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert "widget.txt" in landed
    assert "SR-003" not in _git(root, "show", "HEAD:" + SR_REGISTRY)


def test_the_slot_refuses_a_retired_id_re_authored_inside_its_own_reservation(
    tmp_path,
):
    """Implements: TC-402"""
    # Range membership alone would admit it: SR-006 sits in the lane's own
    # record, and only its retirement record says the number is spent.
    root = _trunk(tmp_path)
    _reauthored_retired_id(root)
    refusal = refused(root, "wi-401", "smoke")
    assert "SR-006" in refusal and RETIRED_RECORD in refusal, refusal


def test_the_slot_refuses_an_id_its_base_held_retired_and_re_authored(tmp_path):
    """Implements: TC-402"""
    # SR-003 is live at the lane's base and live again at its tip, so it is
    # never an added id; only the retirement record the lane adds says the
    # number is spent.
    root = _trunk(tmp_path, sr_rows=(3,))
    _reauthored_retired_id(root, number=3)
    refusal = refused(root, "wi-401", "smoke")
    assert "SR-003" in refusal and BASE_RETIRED_RECORD in refusal, refusal


def test_the_slot_lands_a_lane_beside_a_retired_id_trunk_already_holds_live(
    tmp_path,
):
    """Implements: TC-402"""
    # Adequacy witness: an implementation that refused every live id a
    # retirement record names would refuse every landing after such a pair
    # reached trunk; this lane changes nothing about SR-003.
    root = _trunk(tmp_path, sr_rows=(3,), records=(3,))
    folded = reserved_watermark({"WI": 401, "SR": 6}, [("SR", 6, 6, "WI-401")])
    plant_id_carrier(root, folded)
    _close(root, {SR_REGISTRY: _rows(3, 6), WATERMARK: folded})
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    assert "SR-006" in _git(root, "show", "HEAD:" + SR_REGISTRY)


def test_the_dispatchers_drain_refreshes_a_lane_whose_watermark_lags_the_carrier(
    tmp_path, capfd
):
    """Implements: TC-402"""
    # The station's speculative half asks the slot's own readiness question:
    # a lane refreshed before another lane reserved lags the carrier, so the
    # drain refreshes it outside the slot and the slot never refreshes it in
    # the held slot (the pessimistic sequence).
    root = _trunk(tmp_path)
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, folded)
    _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": 9}, [OWN, OTHER]))
    capfd.readouterr()
    assert load_script("dispatch")._drain(root, "smoke") == 0
    out = capfd.readouterr().out
    assert "is not merge-ready" not in out, out
    landed = _git(root, "show", "HEAD:" + WATERMARK)
    assert {OWN, OTHER} <= set(reservation_records(landed)), landed


def test_the_slot_folds_a_carrier_moved_after_the_lanes_refresh(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path)
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, folded)
    _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    # Another lane reserves after this lane's refresh.
    plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": 9}, [OWN, OTHER]))
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    landed = _git(root, "show", "HEAD:" + WATERMARK)
    assert {OWN, OTHER} <= set(reservation_records(landed)), landed
    assert watermark_marks(landed)["SR"] == 9


def test_a_code_only_lane_lands_with_the_carriers_fold(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path)
    plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": 9}, [OTHER]))
    _close(root, {"widget.txt": "1\n"})
    assert integ.integrate_one(root, "wi-401", "smoke") is None
    landed = _git(root, "show", "HEAD:" + WATERMARK)
    assert OTHER in reservation_records(landed), landed
    assert watermark_marks(landed)["SR"] == 9


def _watermark_conflict(root):
    """A closed lane and a trunk that each rewrote the watermark from a common
    base (different marks and basis lines), so merging trunk into the lane
    conflicts on it."""
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN], basis="SR=7")
    plant_id_carrier(root, folded)
    wt = _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    write_lf(
        root,
        WATERMARK,
        reserved_watermark({"WI": 401, "SR": 9}, basis="SR=9 WI=401"),
    )
    _commit(root, "docs: the trunk bumped the watermark", when=T_LATER)
    return wt


def test_a_refresh_conflicting_only_on_the_watermark_is_resolved_by_the_fold(
    tmp_path,
):
    """Implements: TC-402"""
    root = _trunk(tmp_path)
    wt = _watermark_conflict(root)
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert integ.trunk_is_ancestor(root, "wi-401")
    text = (wt / WATERMARK).read_text(encoding="utf-8")
    assert not any(m in text for m in ("<<<<<<<", "=======", ">>>>>>>")), text
    assert watermark_marks(text)["SR"] == 9
    assert OWN in reservation_records(text)


def test_a_watermark_conflict_beside_another_conflict_still_refuses(tmp_path):
    """Implements: TC-402"""
    # Adequacy witness: an implementation that treated any conflict set
    # holding the watermark as settled once the watermark was folded would
    # commit over the product file's conflict here instead of refusing.
    root = _trunk(tmp_path)
    wt = _watermark_conflict(root)
    write_lf(wt, "contested.txt", "branch side\n")
    _commit(wt, "WI-401: the branch's take on product code", when=T_VERDICT + 1)
    write_lf(root, "contested.txt", "trunk side\n")
    _commit(root, "docs: the trunk's take on product code", when=T_LATER + 1)
    work_tip = _rev(root, "wi-401")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None and "CONFLICTS" in refusal, refusal
    assert _rev(root, "wi-401") == work_tip
    assert _git(wt, "status", "--porcelain").strip() == ""


def test_a_registry_conflict_beside_the_watermark_refuses_with_the_merge_undone(
    tmp_path,
):
    """Implements: TC-402"""
    # Two lanes appending rows to one registry conflict there as well as on the
    # watermark: the refresh refuses and undoes the merge rather than folding
    # the watermark over a conflicted registry.
    root = _trunk(tmp_path)
    wt = _watermark_conflict(root)
    write_lf(wt, SR_REGISTRY, _rows(6, 7, 10))
    _commit(wt, "WI-401: a third row", when=T_VERDICT + 1)
    write_lf(root, SR_REGISTRY, _rows(8, 9))
    _commit(root, "docs: another lane's rows", when=T_LATER + 1)
    work_tip = _rev(root, "wi-401")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None and "CONFLICTS" in refusal, refusal
    assert _rev(root, "wi-401") == work_tip
    assert _git(wt, "status", "--porcelain").strip() == ""


# --- caller 2: the hand squash --------------------------------------------------


@pytest.mark.parametrize("case", sorted(REFUSED))
def test_the_hand_squash_refuses_each_unreserved_landing(tmp_path, case):
    """Implements: TC-402"""
    root = _case(tmp_path, case, harness=False)
    _squash(root)
    code, out = _step(root)
    assert code == 1, out
    assert all(word in out for word in _named(case)), (case, out)


def test_the_hand_squash_passes_ids_in_its_own_record(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False)
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, folded)
    _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    _squash(root)
    code, out = _step(root)
    assert code == 0 and "reserved-ids" in out, out


def test_the_hand_squash_refuses_ids_added_under_an_unreadable_claim(tmp_path):
    """Implements: TC-402"""
    # No local branch contains the squashed tip, so no claim can be read.
    root = _trunk(tmp_path, harness=False)
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, folded)
    wt = _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    tip = _rev(root, "wi-401")
    _git(root, "worktree", "remove", "--force", str(wt))
    _git(root, "branch", "-D", "wi-401")
    _git(root, "merge", "--squash", "-q", tip)
    code, out = _step(root)
    assert code == 1 and "claim" in out.lower(), out


def test_the_hand_squash_refuses_a_retired_id_re_authored_inside_its_own_reservation(
    tmp_path,
):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False)
    _reauthored_retired_id(root)
    _squash(root)
    code, out = _step(root)
    assert code == 1 and "SR-006" in out and RETIRED_RECORD in out, out


def test_the_hand_squash_refuses_an_id_its_base_held_retired_and_re_authored(
    tmp_path,
):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False, sr_rows=(3,))
    _reauthored_retired_id(root, number=3)
    _squash(root)
    code, out = _step(root)
    assert code == 1 and "SR-003" in out and BASE_RETIRED_RECORD in out, out


def test_the_hand_squash_refuses_another_lanes_number_after_that_lane_landed(
    tmp_path,
):
    """Implements: TC-402"""
    # A stale-base lane (SR 8-8 reserved) drafted SR-007, another lane's
    # number. That lane lands SR-006 and SR-007 first; the squash conflicts on
    # the registry and is resolved keeping this lane's SR-007. Over HEAD the
    # number is already live, so only the lane's own delta over its merge base
    # shows it as this lane's addition. Trunk's SR-006 stays trunk's.
    root = _trunk(tmp_path, harness=False)
    records = [("SR", 6, 7, "WI-402"), ("SR", 8, 8, "WI-401")]
    held = reserved_watermark({"WI": 401, "SR": 8}, records)
    plant_id_carrier(root, held)
    mine = _rows(7, 8).replace('title = "t"', 'title = "mine"', 1)
    _close(root, {SR_REGISTRY: mine, WATERMARK: held})
    write_lf(root, SR_REGISTRY, _rows(6, 7))
    write_lf(root, WATERMARK, held)
    _commit(root, "land: WI-402's rows", when=T_LATER)
    proc = subprocess.run(
        ["git", "-C", str(root), "merge", "--squash", "wi-401"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0, proc.stdout
    write_lf(root, SR_REGISTRY, _rows(6) + mine)
    _git(root, "add", SR_REGISTRY, WATERMARK)
    code, out = _step(root)
    assert code == 1 and "SR-007" in out and "WI-401" in out, out
    assert "SR-006" not in out, out


def test_a_hand_squash_folds_a_carrier_moved_after_the_lanes_fold(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False)
    folded = reserved_watermark({"WI": 401, "SR": 7}, [OWN])
    plant_id_carrier(root, folded)
    _close(root, {SR_REGISTRY: _rows(6, 7), WATERMARK: folded})
    plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": 9}, [OWN, OTHER]))
    _squash(root)
    code, out = _step(root)
    assert code == 1, out
    assert "SR 8-9 (WI-402)" in out and "--fold-ids" in out, out
    proc = run_py(FOLD, cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _git(root, "add", WATERMARK)
    code, out = _step(root)
    assert code == 0, out
    _commit(root, "land: WI-401 squashed", when=T_LATER)
    landed = _git(root, "show", "HEAD:" + WATERMARK)
    assert {OWN, OTHER} <= set(reservation_records(landed)), landed
    assert watermark_marks(landed)["SR"] == 9


def test_a_code_only_squash_passes_with_no_reservation(tmp_path):
    """Implements: TC-402"""
    root = _trunk(tmp_path, harness=False)
    _close(root, {"widget.txt": "1\n"})
    _squash(root)
    code, out = _step(root)
    assert code == 0 and "reserved-ids" in out, out
    # With a carrier, the staged watermark must first hold its fold.
    plant_id_carrier(root, reserved_watermark({"WI": 401, "SR": 9}, [OTHER]))
    code, out = _step(root)
    assert code == 1, out
    proc = run_py(FOLD, cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _git(root, "add", WATERMARK)
    code, out = _step(root)
    assert code == 0, out


def test_the_pre_commit_hook_runs_the_reserved_ids_step():
    """Implements: TC-402"""
    # The squash step only guards a hand landing if the shipped hook's batched
    # floor runs it, beside held-status.
    hook = (SCRIPTS.parent / "hooks" / "pre-commit").read_text(encoding="utf-8")
    line = next(
        ln for ln in hook.splitlines() if ln.startswith('"$PY"') and "--run-steps" in ln
    )
    steps = line.split("--run-steps", 1)[1].split()[0].split(",")
    assert "reserved-ids" in steps and "held-status" in steps
    check = load_script("check")
    assert "reserved-ids" in check.BUILTIN_STEP_NAMES
